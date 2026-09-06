#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", type=Path, required=True)
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    return p.parse_args()


def main():
    args = parse_args()
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(args.input_dir.rglob("*.json"))]
    if not rows:
        raise SystemExit("Nenhum resultado da onda 3 encontrado")

    fields = [
        "wave","player_id","profile","seed","completed","current_objective",
        "actions_attempted","actions_executed","blocked_attempts","readiness_checks",
        "voyage_actions","waits","reprovision_actions","reprovision_total",
        "information_attempts","information_executed","information_rumor",
        "information_merchant_contact","information_pilot_consultation",
        "service_unknown_encounters","service_retries_after_information",
        "service_unknown_resolved","service_unknown_unresolved","elapsed_days",
        "final_date","final_location","chronology_mode","counterfactual",
        "min_provisions","min_condition","capital_final","recovered_after_block"
    ]
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["player_id"]))

    blockers = Counter()
    locations = Counter()
    profiles = defaultdict(list)
    for row in rows:
        blockers.update(row.get("blockers", {}))
        locations[row["final_location"]] += 1
        profiles[row["profile"]].append(row)

    summary = {
        "wave": 3,
        "n_players": len(rows),
        "completed": sum(r["completed"] for r in rows),
        "completion_rate": sum(r["completed"] for r in rows) / len(rows),
        "counterfactual": sum(r["counterfactual"] for r in rows),
        "counterfactual_rate": sum(r["counterfactual"] for r in rows) / len(rows),
        "information_attempts": sum(r["information_attempts"] for r in rows),
        "information_executed": sum(r["information_executed"] for r in rows),
        "service_unknown_encounters": sum(r["service_unknown_encounters"] for r in rows),
        "service_retries_after_information": sum(r["service_retries_after_information"] for r in rows),
        "service_unknown_resolved": sum(r["service_unknown_resolved"] for r in rows),
        "service_unknown_unresolved": sum(r["service_unknown_unresolved"] for r in rows),
        "median_actions": statistics.median(r["actions_attempted"] for r in rows),
        "median_blocks": statistics.median(r["blocked_attempts"] for r in rows),
        "top_blockers": blockers.most_common(),
        "final_locations": dict(locations.most_common()),
        "profiles": {
            profile: {
                "n": len(items),
                "completed": sum(r["completed"] for r in items),
                "counterfactual": sum(r["counterfactual"] for r in items),
                "information_attempts": sum(r["information_attempts"] for r in items),
                "service_unknown_resolved": sum(r["service_unknown_resolved"] for r in items),
            }
            for profile, items in sorted(profiles.items())
        },
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
