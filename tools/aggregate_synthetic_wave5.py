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
        raise SystemExit("Nenhum resultado da onda 5 encontrado")

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "wave","player_id","profile","seed","reserve_request_days","completed","current_objective",
        "actions_attempted","actions_executed","blocked_attempts","readiness_checks","voyage_actions",
        "waits","reprovision_actions","reprovision_total","reserve_actions","reserve_days_added",
        "reserve_failed","reserve_skipped_no_documented_service","access_negotiations","trade_actions",
        "elapsed_days","final_date","final_location","chronology_mode","counterfactual","min_provisions",
        "min_condition","capital_final","recovered_after_block","first_block_action"
    ]
    with args.csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["player_id"]))

    blockers = Counter()
    locations = Counter()
    profiles = defaultdict(list)
    for row in rows:
        blockers.update(row.get("blockers", {}))
        locations[row["final_location"]] += 1
        profiles[row["profile"]].append(row)

    completed = sum(1 for row in rows if row["completed"])
    counterfactual = sum(1 for row in rows if row["counterfactual"])
    summary = {
        "wave": 5,
        "reserve_request_days": rows[0]["reserve_request_days"],
        "n_players": len(rows),
        "completed": completed,
        "completion_rate": completed / len(rows),
        "counterfactual": counterfactual,
        "counterfactual_rate": counterfactual / len(rows),
        "median_actions": statistics.median(row["actions_attempted"] for row in rows),
        "median_blocks": statistics.median(row["blocked_attempts"] for row in rows),
        "min_provisions": min(row["min_provisions"] for row in rows),
        "reserve_actions": sum(row["reserve_actions"] for row in rows),
        "reserve_days_added": round(sum(row["reserve_days_added"] for row in rows), 2),
        "reserve_failed": sum(row["reserve_failed"] for row in rows),
        "reserve_skipped_no_documented_service": sum(row["reserve_skipped_no_documented_service"] for row in rows),
        "top_blockers": blockers.most_common(),
        "final_locations": dict(locations.most_common()),
        "profiles": {
            profile: {
                "n": len(items),
                "completed": sum(1 for row in items if row["completed"]),
                "counterfactual": sum(1 for row in items if row["counterfactual"]),
                "median_actions": statistics.median(row["actions_attempted"] for row in items),
                "median_blocks": statistics.median(row["blocked_attempts"] for row in items),
                "reserve_actions": sum(row["reserve_actions"] for row in items),
                "reserve_days_added": round(sum(row["reserve_days_added"] for row in items), 2),
            }
            for profile, items in sorted(profiles.items())
        },
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
