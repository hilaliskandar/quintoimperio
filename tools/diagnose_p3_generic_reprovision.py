#!/usr/bin/env python3
"""Audita tentativas de reabastecimento genérico no playtest P3.

O diagnóstico não altera regras nem resultados. Ele intercepta apenas a função
auxiliar de reabastecimento genérico usada pelo runner sintético e agrega onde
cada tentativa ocorre, com destaque para repetições do mesmo estado.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json

import simulate_p3_archetype as p3


original_reprovision = p3.reprovision
records: list[dict[str, object]] = []


def tracking_reprovision(model, state, metrics, amount: float = 30.0):
    before = state
    after, changed = original_reprovision(model, state, metrics, amount)
    new_blockers = {
        key: metrics.blockers.get(key, 0)
        for key in metrics.blockers
    }
    records.append(
        {
            "profile": metrics.profile,
            "seed": metrics.seed,
            "location": before.vessel.location_node,
            "date": before.vessel.clock.current_date.isoformat(),
            "provisions": round(float(before.vessel.provision_days), 4),
            "changed": bool(changed),
            "indeterminate_total_after": new_blockers.get(
                "HISTORICAL_SERVICE_EVIDENCE_INDETERMINATE", 0
            ),
        }
    )
    return after, changed


def main() -> None:
    p3.reprovision = tracking_reprovision
    results = []
    player_id = 1
    for archetype in p3.PLAYTEST_ARCHETYPES:
        for seed in range(24001, 24021):
            results.append(p3.run_player(player_id, archetype, seed, 20))
            player_id += 1

    location_counts = Counter(r["location"] for r in records)
    profile_counts = Counter(r["profile"] for r in records)
    failed_location_counts = Counter(
        r["location"] for r in records if not r["changed"]
    )

    state_keys = Counter(
        (
            r["profile"],
            r["seed"],
            r["location"],
            r["date"],
            r["provisions"],
        )
        for r in records
        if not r["changed"]
    )
    repeated = [
        {
            "profile": key[0],
            "seed": key[1],
            "location": key[2],
            "date": key[3],
            "provisions": key[4],
            "count": count,
        }
        for key, count in state_keys.items()
        if count > 1
    ]
    repeated.sort(key=lambda x: (-x["count"], x["profile"], x["seed"]))

    by_profile_location: dict[str, Counter] = defaultdict(Counter)
    for r in records:
        if not r["changed"]:
            by_profile_location[str(r["profile"])][str(r["location"])] += 1

    summary = {
        "sessions": len(results),
        "completed": sum(bool(r["completed"]) for r in results),
        "generic_reprovision_calls": len(records),
        "generic_reprovision_failed": sum(not r["changed"] for r in records),
        "calls_by_location": dict(sorted(location_counts.items())),
        "failed_by_location": dict(sorted(failed_location_counts.items())),
        "calls_by_profile": dict(sorted(profile_counts.items())),
        "failed_by_profile_location": {
            profile: dict(sorted(counts.items()))
            for profile, counts in sorted(by_profile_location.items())
        },
        "repeated_identical_failed_states_n": len(repeated),
        "repeated_identical_failed_states": repeated[:100],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
