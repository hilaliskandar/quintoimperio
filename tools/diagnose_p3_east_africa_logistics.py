#!/usr/bin/env python3
"""Sensibilidade logística P3 entre Moçambique, Melinde e Anjediva.

Não altera regras do jogo. Parte do teto atual em Lisboa, aplica a ação já
parametrizada de Vera Cruz (+5) e mede valores hipotéticos em Moçambique e
Melinde. Os candidatos são parâmetros abstratos de simulação, não quantidades
históricas.
"""
from __future__ import annotations

import json
from dataclasses import replace

from quintoimperio.domain import P3CampaignModel

SEEDS = range(24001, 24021)
MOZ_CANDIDATES = (5.0, 7.0, 9.0, 10.0, 12.0)
MAL_CANDIDATES = (10.0, 12.0, 14.0, 15.0, 18.0, 20.0)


def add_provisions(model, state, amount):
    max_onboard = float(model.session.port.rules[("PROVISION_MAX_ONBOARD", "DEFAULT")])
    return replace(
        state,
        vessel=replace(
            state.vessel,
            provision_days=min(max_onboard, state.vessel.provision_days + amount),
        ),
    )


def advance(model, state, seed):
    plan = model.plan_current_leg(state, seed=seed)
    if not plan.feasible:
        return state, False, plan
    return model.execute_voyage(state, plan), True, plan


def release(model, state):
    if state.active_stop_id is None:
        return state
    result = model.wait_for_stop_release(state)
    return result.state_after if result.executed else state


def base_to_moz(model, seed):
    state = model.initial_cabral_state(provision_days=120.0)
    state, ok, plan = advance(model, state, seed)
    if not ok:
        return state, False, f"LIS_VCR:{plan.blockers}"
    state = add_provisions(model, state, 5.0)
    state = release(model, state)
    state, ok, plan = advance(model, state, seed)
    if not ok:
        return state, False, f"VCR_MOZ:{plan.blockers}"
    return state, True, ""


def test_moz_candidate(model, base, seed, moz_amount):
    state = add_provisions(model, base, moz_amount)
    state, ok, plan = advance(model, state, seed)  # MOZ→KIL
    if not ok:
        return state, False, "MOZ_KIL"
    state = release(model, state)
    state, ok, plan = advance(model, state, seed)  # KIL→MAL
    if not ok:
        return state, False, "KIL_MAL"
    return state, True, "MAL"


def main():
    model = P3CampaignModel()
    rows = []
    moz_success = {str(int(x)): 0 for x in MOZ_CANDIDATES}
    mal_success = {
        f"{int(moz)}+{int(mal)}": 0
        for moz in MOZ_CANDIDATES
        for mal in MAL_CANDIDATES
    }
    for seed in SEEDS:
        base, ok, blocker = base_to_moz(model, seed)
        row = {"seed": seed, "base_reached_moz": ok, "base_blocker": blocker}
        if not ok:
            rows.append(row)
            continue
        row["moz_arrival_provisions"] = round(base.vessel.provision_days, 4)
        for moz in MOZ_CANDIDATES:
            at_mal, reached_mal, where = test_moz_candidate(model, base, seed, moz)
            row[f"moz_{int(moz)}_reaches_mal"] = reached_mal
            row[f"moz_{int(moz)}_stop"] = where
            if not reached_mal:
                continue
            moz_success[str(int(moz))] += 1
            row[f"moz_{int(moz)}_mal_arrival_provisions"] = round(
                at_mal.vessel.provision_days, 4
            )
            at_mal = release(model, at_mal)
            for mal in MAL_CANDIDATES:
                prepared = add_provisions(model, at_mal, mal)
                plan = model.plan_current_leg(prepared, seed=seed)
                feasible = plan.feasible and plan.route_id == "R_MAL_ANJ_CAB"
                row[f"moz_{int(moz)}_mal_{int(mal)}_anj_feasible"] = feasible
                if feasible:
                    mal_success[f"{int(moz)}+{int(mal)}"] += 1
        rows.append(row)
    result = {
        "n_seeds": len(rows),
        "moz_candidates": list(MOZ_CANDIDATES),
        "mal_candidates": list(MAL_CANDIDATES),
        "reached_moz_without_candidate": sum(r["base_reached_moz"] for r in rows),
        "moz_to_mal_success": moz_success,
        "mal_to_anj_success_by_pair": mal_success,
        "rows": rows,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
