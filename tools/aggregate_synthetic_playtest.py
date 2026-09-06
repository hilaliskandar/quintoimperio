#!/usr/bin/env python3
"""Agrega resultados JSON produzidos pelos jogadores sintéticos."""

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


def median(values):
    return statistics.median(values) if values else None


def mean(values):
    return statistics.mean(values) if values else None


def main():
    args = parse_args()
    rows = []
    for path in sorted(args.input_dir.rglob("*.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    if not rows:
        raise SystemExit("Nenhum resultado sintético encontrado")

    discipline_actions = [r["actions_attempted"] for r in rows if r["profile"] == "DISCIPLINED" and r["completed"]]
    reference_actions = min(discipline_actions) if discipline_actions else min(r["actions_attempted"] for r in rows)
    for row in rows:
        row["extra_actions_vs_reference"] = row["actions_attempted"] - reference_actions

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "wave", "player_id", "profile", "seed", "completed", "current_objective",
        "actions_attempted", "actions_executed", "blocked_attempts", "readiness_checks",
        "extra_actions_vs_reference", "voyage_actions", "waits",
        "reprovision_actions", "reprovision_total", "access_negotiations",
        "trade_actions", "elapsed_days", "final_date", "final_location",
        "chronology_mode", "counterfactual", "min_provisions", "min_condition",
        "voyage_events", "capital_final", "capacity_used_final", "capacity_total",
        "knowledge_nodes", "recovered_after_block", "first_block_action",
    ]
    with args.csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["player_id"]))

    blockers = Counter()
    by_profile = defaultdict(list)
    for row in rows:
        blockers.update(row.get("blockers", {}))
        by_profile[row["profile"]].append(row)

    summary = {
        "wave": rows[0].get("wave", 1),
        "n_players": len(rows),
        "completed": sum(1 for r in rows if r["completed"]),
        "completion_rate": sum(1 for r in rows if r["completed"]) / len(rows),
        "counterfactual": sum(1 for r in rows if r["counterfactual"]),
        "counterfactual_rate": sum(1 for r in rows if r["counterfactual"]) / len(rows),
        "players_with_blocks": sum(1 for r in rows if r["blocked_attempts"] > 0),
        "recovered_after_block": sum(1 for r in rows if r["blocked_attempts"] > 0 and r["recovered_after_block"]),
        "readiness_checks": {
            "median": median([r.get("readiness_checks", 0) for r in rows]),
            "mean": mean([r.get("readiness_checks", 0) for r in rows]),
            "min": min(r.get("readiness_checks", 0) for r in rows),
            "max": max(r.get("readiness_checks", 0) for r in rows),
        },
        "actions_attempted": {
            "median": median([r["actions_attempted"] for r in rows]),
            "mean": mean([r["actions_attempted"] for r in rows]),
            "min": min(r["actions_attempted"] for r in rows),
            "max": max(r["actions_attempted"] for r in rows),
        },
        "blocked_attempts": {
            "median": median([r["blocked_attempts"] for r in rows]),
            "mean": mean([r["blocked_attempts"] for r in rows]),
            "max": max(r["blocked_attempts"] for r in rows),
        },
        "elapsed_days": {
            "median": median([r["elapsed_days"] for r in rows]),
            "mean": mean([r["elapsed_days"] for r in rows]),
            "min": min(r["elapsed_days"] for r in rows),
            "max": max(r["elapsed_days"] for r in rows),
        },
        "capital_final": {
            "median": median([r["capital_final"] for r in rows]),
            "mean": mean([r["capital_final"] for r in rows]),
            "min": min(r["capital_final"] for r in rows),
            "max": max(r["capital_final"] for r in rows),
        },
        "min_provisions": min(r["min_provisions"] for r in rows),
        "min_condition": min(r["min_condition"] for r in rows),
        "top_blockers": blockers.most_common(),
        "reference_actions": reference_actions,
        "profiles": {},
    }
    for profile, items in sorted(by_profile.items()):
        summary["profiles"][profile] = {
            "n": len(items),
            "completed": sum(1 for r in items if r["completed"]),
            "completion_rate": sum(1 for r in items if r["completed"]) / len(items),
            "median_actions": median([r["actions_attempted"] for r in items]),
            "median_blocked": median([r["blocked_attempts"] for r in items]),
            "median_readiness_checks": median([r.get("readiness_checks", 0) for r in items]),
            "median_reprovision_actions": median([r["reprovision_actions"] for r in items]),
            "median_capital_final": median([r["capital_final"] for r in items]),
            "counterfactual": sum(1 for r in items if r["counterfactual"]),
        }

    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
