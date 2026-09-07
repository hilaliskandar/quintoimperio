#!/usr/bin/env python3
"""Diagnostico reproduzivel de STRUCTURAL_STRAIN sem alterar regras de simulacao.

O ensaio usa a rota historicamente observada Melinde-Calecute apenas como
superficie controlada porque ela admite eventos ``observed_timing_safe`` sem
mudar os 27 dias observados. Os niveis de condicao inicial sao cenarios de
estresse de simulacao, nao estados historicos documentados.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

from quintoimperio.domain import GameClock, KnowledgeLevel, TravelModel, VesselState
from quintoimperio.domain.voyage_event import VoyageEventType

ROUTE_ID = "R_MAL_CAL"
DEPARTURE = date(1498, 4, 24)
DEFAULT_CONDITIONS = (100.0, 60.0, 40.0, 36.79, 30.0, 25.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=10000)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    travel = TravelModel()
    rows: list[dict[str, object]] = []
    event_counts: Counter[str] = Counter()
    strain_seeds: set[int] = set()

    for seed in range(args.seeds):
        for start_condition in DEFAULT_CONDITIONS:
            state = VesselState(
                location_node="MAL",
                clock=GameClock(DEPARTURE),
                provision_days=120.0,
                condition=start_condition,
            )
            plan = travel.plan_voyage(
                state,
                ROUTE_ID,
                KnowledgeLevel.OPERATIONAL,
                seed=seed,
                preserve_observed_timing=True,
            )
            event_type = plan.events[0].event_type.value if plan.events else "NONE"
            event_counts[event_type] += 1
            structural = bool(
                plan.events
                and plan.events[0].event_type is VoyageEventType.STRUCTURAL_STRAIN
            )
            if structural:
                strain_seeds.add(seed)
            condition_loss = plan.events[0].condition_loss if structural else 0.0
            rows.append(
                {
                    "seed": seed,
                    "start_condition": start_condition,
                    "event_type": event_type,
                    "structural_strain": structural,
                    "event_condition_loss": condition_loss,
                    "condition_after": plan.condition_after,
                    "feasible": plan.feasible,
                    "blockers": "|".join(plan.blockers),
                    "crossed_condition_20": start_condition >= 20.0
                    and plan.condition_after < 20.0,
                    "travel_days": plan.travel_days,
                    "arrival_date": plan.arrival_date.isoformat(),
                }
            )

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    by_condition: dict[str, dict[str, object]] = {}
    for start_condition in DEFAULT_CONDITIONS:
        subset = [row for row in rows if row["start_condition"] == start_condition]
        strain = [row for row in subset if row["structural_strain"]]
        by_condition[f"{start_condition:g}"] = {
            "n": len(subset),
            "structural_strain_n": len(strain),
            "structural_strain_rate": len(strain) / len(subset),
            "crossed_condition_20_n": sum(bool(row["crossed_condition_20"]) for row in strain),
            "condition_blocker_n": sum(
                "VESSEL_CONDITION_TOO_LOW" in str(row["blockers"]) for row in strain
            ),
            "min_condition_after_structural": min(
                (float(row["condition_after"]) for row in strain),
                default=None,
            ),
        }

    summary = {
        "diagnostic": "structural-strain-v05",
        "route_id": ROUTE_ID,
        "departure": DEPARTURE.isoformat(),
        "preserve_observed_timing": True,
        "seeds": args.seeds,
        "condition_scenarios": list(DEFAULT_CONDITIONS),
        "unique_structural_strain_seeds": len(strain_seeds),
        "event_counts_across_condition_scenarios": dict(event_counts),
        "by_start_condition": by_condition,
        "interpretation_guardrail": (
            "Cenarios de condicao sao superficie de estresse de SIMULATION; "
            "nao representam estados historicos observados."
        ),
    }
    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
