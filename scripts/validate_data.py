#!/usr/bin/env python3
"""Validate historical data and simulation configuration without game-engine dependencies."""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SIMULATION = ROOT / "simulation"
SOURCES = ROOT / "docs" / "sources.md"

EVIDENCE = {"A", "B", "C", "D"}
EVIDENCE_SCOPE = {"NODE_DIRECT", "REGIONAL", "NETWORK", "LATER_PERIOD_ANALOGY"}
BOOLS = {"", "TRUE", "FALSE"}
KNOWLEDGE_PERSPECTIVES = {"PLAYER", "CROWN"}
PILOT_COMPETENCE = {"CONFIRMED"}

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def read_csv(name: str, directory: Path = DATA) -> list[dict[str, str]]:
    path = directory / name
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return []

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            fail(f"{path.relative_to(ROOT)}: missing header")
            return []

        rows: list[dict[str, str]] = []
        for line_no, row in enumerate(reader, start=2):
            table = str(path.relative_to(ROOT))
            if None in row:
                fail(f"{table}:{line_no}: extra CSV fields: {row[None]}")
                continue
            if any(value is None for value in row.values()):
                fail(f"{table}:{line_no}: missing CSV fields")
                continue
            for key, value in row.items():
                if value != value.strip():
                    fail(f"{table}:{line_no}: whitespace around field {key!r}: {value!r}")
            row["__line__"] = str(line_no)
            rows.append(row)
        return rows


def unique(rows: list[dict[str, str]], field: str, table: str) -> set[str]:
    seen: set[str] = set()
    for row in rows:
        value = row.get(field, "")
        line = row["__line__"]
        if not value:
            fail(f"{table}:{line}: empty {field}")
        elif value in seen:
            fail(f"{table}:{line}: duplicate {field}={value}")
        else:
            seen.add(value)
    return seen


def source_ids() -> set[str]:
    if not SOURCES.exists():
        fail("docs/sources.md missing")
        return set()
    text = SOURCES.read_text(encoding="utf-8")
    return set(re.findall(r"^\| `([A-Z0-9_]+)` \|", text, flags=re.MULTILINE))


def validate_sources(rows: list[dict[str, str]], table: str, allowed: set[str]) -> None:
    for row in rows:
        line = row["__line__"]
        raw = row.get("source_id", "")
        if not raw:
            fail(f"{table}:{line}: empty source_id")
            continue
        for source in raw.split("|"):
            if source not in allowed:
                fail(f"{table}:{line}: unknown source_id={source}")


def validate_period(row: dict[str, str], table: str) -> None:
    line = row["__line__"]
    values: dict[str, int] = {}
    for field in ("period_from", "period_to"):
        raw = row.get(field, "")
        if not raw:
            continue
        if not raw.isdigit():
            fail(f"{table}:{line}: {field} must be a year or blank, got {raw!r}")
            continue
        values[field] = int(raw)
    if values.get("period_from", -10**9) > values.get("period_to", 10**9):
        fail(f"{table}:{line}: period_from is later than period_to")


def validate_evidence(rows: list[dict[str, str]], table: str) -> None:
    for row in rows:
        line = row["__line__"]
        grade = row.get("evidence_grade", row.get("evidence_strength", ""))
        if grade and grade not in EVIDENCE:
            fail(f"{table}:{line}: invalid evidence value {grade!r}")
        scope = row.get("evidence_scope", "")
        if scope and scope not in EVIDENCE_SCOPE:
            fail(f"{table}:{line}: invalid evidence_scope {scope!r}")


def validate_nodes(rows: list[dict[str, str]]) -> None:
    for row in rows:
        line = row["__line__"]
        lat, lon = row.get("latitude", ""), row.get("longitude", "")
        if bool(lat) != bool(lon):
            fail(f"nodes.csv:{line}: latitude/longitude must both be filled or both blank")
        if lat and lon:
            try:
                lat_f, lon_f = float(lat), float(lon)
            except ValueError:
                fail(f"nodes.csv:{line}: invalid coordinate pair {lat!r}, {lon!r}")
            else:
                if not -90 <= lat_f <= 90 or not -180 <= lon_f <= 180:
                    fail(f"nodes.csv:{line}: coordinate out of range")
        if row.get("coordinate_confidence") == "HIGH" and not lat:
            fail(f"nodes.csv:{line}: HIGH coordinate confidence with empty coordinates")
        if row.get("node_type") == "NAVIGATION_POINT" and row.get("market_scale") not in {"", "NONE"}:
            warn(f"nodes.csv:{line}: navigation point has a non-empty market scale")


def validate_bool(rows: list[dict[str, str]], table: str, fields: tuple[str, ...]) -> None:
    for row in rows:
        for field in fields:
            if field in row and row[field] not in BOOLS:
                fail(f"{table}:{row['__line__']}: invalid boolean {field}={row[field]!r}")


def validate_voyage_observations(
    rows: list[dict[str, str]], node_ids: set[str], route_by_id: dict[str, dict[str, str]]
) -> None:
    unique(rows, "observation_id", "voyage_observations.csv")
    for row in rows:
        line = row["__line__"]
        route_id = row["route_id"]
        if route_id not in route_by_id:
            fail(f"voyage_observations.csv:{line}: unknown route_id={route_id}")
            continue
        if row["departure_node"] not in node_ids or row["arrival_node"] not in node_ids:
            fail(f"voyage_observations.csv:{line}: unknown node reference")
            continue
        route = route_by_id[route_id]
        if (row["departure_node"], row["arrival_node"]) != (
            route["origin_node"], route["destination_node"]
        ):
            fail(f"voyage_observations.csv:{line}: endpoints do not match {route_id}")
        try:
            departure = date.fromisoformat(row["departure_date"])
            arrival = date.fromisoformat(row["arrival_date"])
        except ValueError:
            fail(f"voyage_observations.csv:{line}: invalid ISO date")
            continue
        elapsed = (arrival - departure).days
        if elapsed <= 0:
            fail(f"voyage_observations.csv:{line}: arrival must be after departure")
        try:
            recorded = int(row["observed_days"])
        except ValueError:
            fail(f"voyage_observations.csv:{line}: observed_days must be integer")
        else:
            if recorded != elapsed:
                fail(
                    f"voyage_observations.csv:{line}: observed_days={recorded} "
                    f"but dates imply {elapsed}"
                )


def validate_knowledge_rules(rows: list[dict[str, str]], nodes: list[dict[str, str]]) -> None:
    mappings: set[tuple[str, str]] = set()
    for row in rows:
        line = row["__line__"]
        perspective = row["perspective"]
        if perspective not in KNOWLEDGE_PERSPECTIVES:
            fail(f"simulation/knowledge_rules.csv:{line}: invalid perspective={perspective}")
        key = (perspective, row["source_value"])
        if key in mappings:
            fail(f"simulation/knowledge_rules.csv:{line}: duplicate mapping {key}")
        mappings.add(key)
        for field in ("geo", "nav", "market", "political"):
            try:
                value = int(row[field])
            except ValueError:
                fail(f"simulation/knowledge_rules.csv:{line}: {field} must be integer")
                continue
            if not 0 <= value <= 4:
                fail(f"simulation/knowledge_rules.csv:{line}: {field} outside 0..4")

    for node in nodes:
        player_key = ("PLAYER", node["player_default_knowledge"])
        crown_key = ("CROWN", node["known_to_portugal_1497"])
        if player_key not in mappings:
            fail(f"simulation/knowledge_rules.csv: missing mapping {player_key} used by {node['node_id']}")
        if crown_key not in mappings:
            fail(f"simulation/knowledge_rules.csv: missing mapping {crown_key} used by {node['node_id']}")


def validate_navigation_rules(rows: list[dict[str, str]], route_ids: set[str]) -> None:
    reference_routes = []
    for row in rows:
        line = row["__line__"]
        rule_type = row["rule_type"]
        key = row["key"]
        value = row["value"]
        if rule_type == "REFERENCE_ROUTE":
            if key not in route_ids:
                fail(f"simulation/navigation_rules.csv:{line}: unknown reference route {key}")
            if value == "1":
                reference_routes.append(key)
        else:
            try:
                numeric = float(value)
            except ValueError:
                fail(f"simulation/navigation_rules.csv:{line}: value must be numeric")
                continue
            if numeric < 0:
                fail(f"simulation/navigation_rules.csv:{line}: negative value")
    if len(reference_routes) != 1:
        fail("simulation/navigation_rules.csv: exactly one REFERENCE_ROUTE with value=1 is required")


def validate_pilots(
    pilots: list[dict[str, str]],
    pilot_routes: list[dict[str, str]],
    node_ids: set[str],
    route_ids: set[str],
) -> None:
    pilot_ids = unique(pilots, "pilot_id", "pilots.csv")
    for row in pilots:
        if row["available_node"] not in node_ids:
            fail(f"pilots.csv:{row['__line__']}: unknown available_node={row['available_node']}")

    seen_pairs: set[tuple[str, str, str, str]] = set()
    for row in pilot_routes:
        line = row["__line__"]
        if row["pilot_id"] not in pilot_ids:
            fail(f"pilot_routes.csv:{line}: unknown pilot_id={row['pilot_id']}")
        if row["route_id"] not in route_ids:
            fail(f"pilot_routes.csv:{line}: unknown route_id={row['route_id']}")
        if row["competence"] not in PILOT_COMPETENCE:
            fail(f"pilot_routes.csv:{line}: invalid competence={row['competence']}")
        key = (row["pilot_id"], row["route_id"], row["period_from"], row["period_to"])
        if key in seen_pairs:
            fail(f"pilot_routes.csv:{line}: duplicate pilot-route period {key}")
        seen_pairs.add(key)


def validate_travel_rules(rows: list[dict[str, str]]) -> None:
    required = {
        ("PROVISIONS", "DAY_EQUIVALENT_PER_TRAVEL_DAY"),
        ("WEAR", "OCEANIC_PER_DAY"),
        ("WEAR", "COASTAL_OCEANIC_PER_DAY"),
        ("WEAR", "DEFAULT_PER_DAY"),
        ("DEPARTURE", "MIN_CONDITION"),
    }
    seen: set[tuple[str, str]] = set()
    for row in rows:
        line = row["__line__"]
        key = (row["rule_type"], row["key"])
        if key in seen:
            fail(f"simulation/travel_rules.csv:{line}: duplicate rule {key}")
        seen.add(key)
        try:
            value = float(row["value"])
        except ValueError:
            fail(f"simulation/travel_rules.csv:{line}: value must be numeric")
            continue
        if value < 0:
            fail(f"simulation/travel_rules.csv:{line}: negative value")
    missing = required - seen
    for key in sorted(missing):
        fail(f"simulation/travel_rules.csv: missing required rule {key}")


def main() -> int:
    nodes = read_csv("nodes.csv")
    goods = read_csv("goods.csv")
    node_goods = read_csv("node_goods.csv")
    routes = read_csv("routes.csv")
    route_goods = read_csv("route_goods.csv")
    voyage_observations = read_csv("voyage_observations.csv")
    pilots = read_csv("pilots.csv")
    pilot_routes = read_csv("pilot_routes.csv")
    navigation_rules = read_csv("navigation_rules.csv", SIMULATION)
    knowledge_rules = read_csv("knowledge_rules.csv", SIMULATION)
    travel_rules = read_csv("travel_rules.csv", SIMULATION)

    node_ids = unique(nodes, "node_id", "nodes.csv")
    good_ids = unique(goods, "good_id", "goods.csv")
    route_ids = unique(routes, "route_id", "routes.csv")
    known_sources = source_ids()

    if not known_sources:
        fail("no source IDs found in docs/sources.md")

    validate_nodes(nodes)
    validate_bool(goods, "goods.csv", ("simulation_only",))
    validate_bool(node_goods, "node_goods.csv", ("restricted", "documented_presence"))

    for table, rows in (
        ("nodes.csv", nodes),
        ("goods.csv", goods),
        ("node_goods.csv", node_goods),
        ("routes.csv", routes),
        ("route_goods.csv", route_goods),
        ("voyage_observations.csv", voyage_observations),
        ("pilots.csv", pilots),
        ("pilot_routes.csv", pilot_routes),
    ):
        validate_evidence(rows, table)
        validate_sources(rows, table, known_sources)
        for row in rows:
            validate_period(row, table)

    for row in node_goods:
        line = row["__line__"]
        if row["node_id"] not in node_ids:
            fail(f"node_goods.csv:{line}: unknown node_id={row['node_id']}")
        if row["good_id"] not in good_ids:
            fail(f"node_goods.csv:{line}: unknown good_id={row['good_id']}")

    route_by_id = {row["route_id"]: row for row in routes}
    for row in routes:
        line = row["__line__"]
        if row["origin_node"] not in node_ids:
            fail(f"routes.csv:{line}: unknown origin_node={row['origin_node']}")
        if row["destination_node"] not in node_ids:
            fail(f"routes.csv:{line}: unknown destination_node={row['destination_node']}")

    for row in route_goods:
        line = row["__line__"]
        if row["route_id"] not in route_ids:
            fail(f"route_goods.csv:{line}: unknown route_id={row['route_id']}")
            continue
        if row["origin_node"] not in node_ids or row["destination_node"] not in node_ids:
            fail(f"route_goods.csv:{line}: unknown node reference")
        if row["good_id"] not in good_ids:
            fail(f"route_goods.csv:{line}: unknown good_id={row['good_id']}")
        route = route_by_id[row["route_id"]]
        if (row["origin_node"], row["destination_node"]) != (
            route["origin_node"],
            route["destination_node"],
        ):
            fail(
                f"route_goods.csv:{line}: endpoints do not match {row['route_id']} "
                f"({route['origin_node']}->{route['destination_node']})"
            )

    validate_voyage_observations(voyage_observations, node_ids, route_by_id)
    validate_navigation_rules(navigation_rules, route_ids)
    validate_knowledge_rules(knowledge_rules, nodes)
    validate_pilots(pilots, pilot_routes, node_ids, route_ids)
    validate_travel_rules(travel_rules)

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)

    if errors:
        print(f"validation failed: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1

    print(
        "validation OK: "
        f"{len(nodes)} nodes, {len(goods)} goods, {len(node_goods)} node-goods, "
        f"{len(routes)} routes, {len(route_goods)} route-goods, "
        f"{len(voyage_observations)} voyage observations, "
        f"{len(pilots)} pilots, {len(pilot_routes)} pilot-routes; "
        f"{len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
