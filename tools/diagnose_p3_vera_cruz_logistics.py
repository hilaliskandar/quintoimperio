#!/usr/bin/env python3
"""Diagnóstico de sensibilidade da lacuna logística VCR→MOZ.

Não altera regras do jogo. Mede, para as seeds da wave20, quanto de autonomia
abstrata seria necessário acrescentar em Vera Cruz após a primeira perna, usando
o teto global vigente apenas como referência. Os valores testados não são fatos
históricos nem recomendações de balanceamento.
"""
from __future__ import annotations

import json
from dataclasses import replace

from quintoimperio.domain import P3CampaignModel

SEEDS = range(24001, 24021)
CANDIDATES = (0.0, 5.0, 10.0, 15.0, 20.0)


def main() -> None:
    model = P3CampaignModel()
    max_onboard = float(model.session.port.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")])
    rows = []
    for seed in SEEDS:
        state = model.initial_cabral_state(provision_days=max_onboard)
        first = model.plan_current_leg(state, seed=seed)
        if not first.feasible:
            raise SystemExit(f"Primeira perna inviável na seed {seed}: {first.blockers}")
        state = model.execute_voyage(state, first)
        wait = model.wait_for_guided_departure(state)
        if wait.executed:
            state = wait.state_after
        base = float(state.vessel.provision_days)
        plan = model.plan_current_leg(state, seed=seed)
        required = float(plan.provision_days_required)
        shortfall = max(0.0, required - base)
        candidate_results = {}
        for candidate in CANDIDATES:
            added = min(candidate, max(0.0, max_onboard - base))
            candidate_results[str(int(candidate))] = (base + added) >= required
        rows.append({
            "seed": seed,
            "after_lis_vcr": round(base, 4),
            "vcr_moz_required": round(required, 4),
            "shortfall": round(shortfall, 4),
            "candidate_feasible": candidate_results,
        })

    result = {
        "max_onboard": max_onboard,
        "n": len(rows),
        "shortfall_min": min(row["shortfall"] for row in rows),
        "shortfall_max": max(row["shortfall"] for row in rows),
        "shortfall_mean": round(sum(row["shortfall"] for row in rows) / len(rows), 4),
        "candidate_success": {
            str(int(candidate)): sum(
                row["candidate_feasible"][str(int(candidate))] for row in rows
            )
            for candidate in CANDIDATES
        },
        "rows": rows,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
