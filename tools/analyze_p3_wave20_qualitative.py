#!/usr/bin/env python3
"""Analisa qualitativamente a wave20 P3 com a mesma matriz pareada de seeds."""
from __future__ import annotations

import json
from collections import Counter, defaultdict

from simulate_p3_archetype import PLAYTEST_ARCHETYPES, run_player

SEEDS = range(24001, 24021)


def main() -> None:
    rows = []
    for archetype in PLAYTEST_ARCHETYPES:
        for i, seed in enumerate(SEEDS, start=1):
            rows.append(run_player(i, archetype, seed, wave=20))

    by_archetype = {}
    for archetype in PLAYTEST_ARCHETYPES:
        group = [r for r in rows if r["archetype"] == archetype]
        by_archetype[archetype] = {
            "completed": sum(bool(r["completed"]) for r in group),
            "failed_seeds": [r["seed"] for r in group if not r["completed"]],
            "final_locations_failed": dict(sorted(Counter(r["final_location"] for r in group if not r["completed"]).items())),
            "blockers_failed": dict(sorted(Counter(k for r in group if not r["completed"] for k, n in r["blockers"].items() for _ in range(n)).items())),
        }

    by_seed = {}
    for seed in SEEDS:
        group = [r for r in rows if r["seed"] == seed]
        completed = [r["archetype"] for r in group if r["completed"]]
        failed = [r for r in group if not r["completed"]]
        by_seed[str(seed)] = {
            "completed_count": len(completed),
            "completed_archetypes": completed,
            "failed_archetypes": [r["archetype"] for r in failed],
            "failed_final_locations": dict(sorted(Counter(r["final_location"] for r in failed).items())),
            "failed_net_event_provision_delta": {
                r["archetype"]: r["net_event_provision_delta"] for r in failed
            },
        }

    seed_classes = defaultdict(list)
    for seed, row in by_seed.items():
        n = row["completed_count"]
        if n == len(PLAYTEST_ARCHETYPES):
            cls = "universal_success"
        elif n == 0:
            cls = "universal_failure"
        elif n <= 3:
            cls = "high_stress"
        elif n >= len(PLAYTEST_ARCHETYPES) - 2:
            cls = "low_stress"
        else:
            cls = "discriminating"
        seed_classes[cls].append(int(seed))

    output = {
        "sessions": len(rows),
        "completed": sum(bool(r["completed"]) for r in rows),
        "completion_rate": round(sum(bool(r["completed"]) for r in rows) / len(rows), 6),
        "seed_classes": dict(sorted(seed_classes.items())),
        "by_archetype": by_archetype,
        "by_seed": by_seed,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
