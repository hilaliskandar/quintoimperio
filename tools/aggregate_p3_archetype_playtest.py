#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_GROUPS = 11
EXPECTED_SESSIONS_PER_GROUP = 20
EXPECTED_SEEDS = 20


def med(values):
    return statistics.median(values) if values else None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", type=Path, required=True)
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    p.add_argument("--paired-csv", type=Path, required=True)
    args = p.parse_args()

    rows = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(args.input_dir.rglob("*.json"))]
    by_arch = defaultdict(list)
    by_seed = defaultdict(list)
    blockers = Counter()
    for row in rows:
        by_arch[row["archetype"]].append(row)
        by_seed[row["seed"]].append(row)
        blockers.update(row.get("blockers", {}))

    expected_total = EXPECTED_GROUPS * EXPECTED_SESSIONS_PER_GROUP
    if len(rows) != expected_total or len(by_arch) != EXPECTED_GROUPS:
        raise SystemExit(f"Bateria P3 incompleta: {len(rows)} sessões / {len(by_arch)} grupos")
    if any(len(values) != EXPECTED_SESSIONS_PER_GROUP for values in by_arch.values()):
        raise SystemExit("Bateria P3 incompleta por arquétipo")
    if len(by_seed) != EXPECTED_SEEDS or any(len(values) != EXPECTED_GROUPS for values in by_seed.values()):
        raise SystemExit("Pareamento P3 incompleto por seed")

    waves = {int(row["wave"]) for row in rows}
    if len(waves) != 1:
        raise SystemExit(f"Bateria mistura ondas: {sorted(waves)}")
    wave = next(iter(waves))

    fields = [
        "wave", "player_id", "archetype", "archetype_label", "game_style", "seed", "completed",
        "actions_attempted", "actions_executed", "blocked_attempts", "recommendation_checks",
        "recommendation_followed", "recommendation_ignored", "indeterminate_destination_warnings",
        "voyage_actions", "waits", "reprovision_actions", "reprovision_total", "access_negotiations",
        "trade_actions", "elapsed_days", "final_date", "final_location", "chronology_mode",
        "counterfactual", "min_provisions", "min_condition", "voyage_events",
        "positive_provision_events", "negative_provision_events", "timing_events",
        "net_event_provision_delta", "capital_final", "archetype_switches", "archetype_sequence",
    ]
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item["seed"], item["archetype"])):
            serialized = dict(row)
            serialized["archetype_sequence"] = json.dumps(row.get("archetype_sequence", []), ensure_ascii=False)
            writer.writerow(serialized)

    paired = []
    for seed, items in sorted(by_seed.items()):
        completed = sorted(row["archetype"] for row in items if row["completed"])
        failed = sorted(row["archetype"] for row in items if not row["completed"])
        paired.append(
            {
                "seed": seed,
                "completed_n": len(completed),
                "failed_n": len(failed),
                "completed_archetypes": "|".join(completed),
                "failed_archetypes": "|".join(failed),
                "min_provisions_median": med([row["min_provisions"] for row in items]),
                "min_condition_median": med([row["min_condition"] for row in items]),
            }
        )
    with args.paired_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(paired[0]))
        writer.writeheader()
        writer.writerows(paired)

    summary = {
        "wave": wave,
        "design": "paired-seed-p3-cabral-to-cannanore",
        "seeds": sorted(by_seed),
        "n_sessions": len(rows),
        "completion_rate": sum(row["completed"] for row in rows) / len(rows),
        "completed": sum(row["completed"] for row in rows),
        "top_blockers": blockers.most_common(),
        "archetypes": {},
        "seeds_summary": paired,
    }
    for name, items in sorted(by_arch.items()):
        group_blockers = Counter()
        for row in items:
            group_blockers.update(row.get("blockers", {}))
        summary["archetypes"][name] = {
            "n": len(items),
            "completed": sum(row["completed"] for row in items),
            "completion_rate": sum(row["completed"] for row in items) / len(items),
            "median_capital_final": med([row["capital_final"] for row in items]),
            "median_blocked": med([row["blocked_attempts"] for row in items]),
            "median_min_provisions": med([row["min_provisions"] for row in items]),
            "median_min_condition": med([row["min_condition"] for row in items]),
            "median_archetype_switches": med([row.get("archetype_switches", 0) for row in items]),
            "top_blockers": group_blockers.most_common(),
        }

    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
