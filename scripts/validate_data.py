#!/usr/bin/env python3
"""Validate historical data tables without adding game-engine dependencies."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCES = ROOT / "docs" / "sources.md"

EVIDENCE = {"A", "B", "C", "D"}
EVIDENCE_SCOPE = {"NODE_DIRECT", "REGIONAL", "NETWORK", "LATER_PERIOD_ANALOGY"}
BOOLS = {"", "TRUE", "FALSE"}

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return []

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            fail(f"{name}: missing header")
            return []

        rows: list[dict[str, str]] = []
        for line_no, row in enumerate(reader, start=2):
            if None in row:
                fail(f"{name}:{line_no}: extra CSV fields: {row[None]}")
                continue
            if any(value is None for value in row.values()):
                fail(f"{name}:{line_no}: missing CSV fields")
                continue
            for key, value in row.items():
                if value != value.strip():
                    fail(f"{name}:{line_no}: whitespace around field {key!r}: {value!r}")
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


def main() -> int:
    nodes = read_csv("nodes.csv")
    goods = read_csv("goods.csv")
    node_goods = read_csv("node_goods.csv")
    routes = read_csv("routes.csv")
    route_goods = read_csv("route_goods.csv")

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
        f"{len(routes)} routes, {len(route_goods)} route-goods; "
        f"{len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
