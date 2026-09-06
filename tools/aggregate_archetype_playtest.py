#!/usr/bin/env python3
"""Agrega a bateria de arquétipos sintéticos em CSV e resumo JSON."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def median(values):
    return statistics.median(values) if values else None


def mean(values):
    return statistics.mean(values) if values else None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(args.input_dir.rglob("*.json"))
    ]
    if not rows:
        raise SystemExit("Nenhum resultado de arquétipo encontrado")

    by_archetype = defaultdict(list)
    blockers = Counter()
    for row in rows:
        by_archetype[row["archetype"]].append(row)
        blockers.update(row.get("blockers", {}))

    expected = 20
    bad_counts = {
        name: len(items) for name, items in by_archetype.items() if len(items) != expected
    }
    if len(by_archetype) != 10 or bad_counts:
        raise SystemExit(
            f"Bateria incompleta: arquétipos={len(by_archetype)}, contagens={bad_counts}"
        )

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "wave", "player_id", "archetype", "archetype_label", "game_style",
        "seed", "completed", "current_objective", "actions_attempted",
        "actions_executed", "blocked_attempts", "recommendation_checks",
        "recommendation_followed", "recommendation_ignored",
        "indeterminate_destination_warnings", "voyage_actions", "waits",
        "reprovision_actions", "reprovision_total", "access_negotiations",
        "trade_actions", "elapsed_days", "final_date", "final_location",
        "chronology_mode", "counterfactual", "min_provisions", "min_condition",
        "voyage_events", "capital_final", "capacity_used_final", "capacity_total",
        "knowledge_nodes", "recovered_after_block", "first_block_action",
    ]
    with args.csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (r["archetype"], r["player_id"])))

    summary = {
        "wave": 11,
        "n_archetypes": len(by_archetype),
        "sessions_per_archetype": expected,
        "n_sessions": len(rows),
        "completed": sum(1 for r in rows if r["completed"]),
        "completion_rate": sum(1 for r in rows if r["completed"]) / len(rows),
        "counterfactual": sum(1 for r in rows if r["counterfactual"]),
        "players_with_blocks": sum(1 for r in rows if r["blocked_attempts"] > 0),
        "top_blockers": blockers.most_common(),
        "archetypes": {},
    }

    for name, items in sorted(by_archetype.items()):
        item_blockers = Counter()
        for item in items:
            item_blockers.update(item.get("blockers", {}))
        summary["archetypes"][name] = {
            "label": items[0]["archetype_label"],
            "game_style": items[0]["game_style"],
            "n": len(items),
            "completed": sum(1 for r in items if r["completed"]),
            "completion_rate": sum(1 for r in items if r["completed"]) / len(items),
            "counterfactual": sum(1 for r in items if r["counterfactual"]),
            "players_with_blocks": sum(1 for r in items if r["blocked_attempts"] > 0),
            "recovered_after_block": sum(
                1 for r in items if r["blocked_attempts"] > 0 and r["recovered_after_block"]
            ),
            "median_actions": median([r["actions_attempted"] for r in items]),
            "mean_actions": mean([r["actions_attempted"] for r in items]),
            "median_blocked": median([r["blocked_attempts"] for r in items]),
            "median_reprovision_actions": median([r["reprovision_actions"] for r in items]),
            "median_reprovision_total": median([r["reprovision_total"] for r in items]),
            "recommendation_checks": sum(r["recommendation_checks"] for r in items),
            "recommendation_followed": sum(r["recommendation_followed"] for r in items),
            "recommendation_ignored": sum(r["recommendation_ignored"] for r in items),
            "min_provisions": min(r["min_provisions"] for r in items),
            "min_condition": min(r["min_condition"] for r in items),
            "median_elapsed_days": median([r["elapsed_days"] for r in items]),
            "median_capital_final": median([r["capital_final"] for r in items]),
            "top_blockers": item_blockers.most_common(),
        }

    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
