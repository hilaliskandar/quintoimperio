#!/usr/bin/env python3
"""Sensibilidade do teto abstrato de provisões para EXP_CABRAL_1500.

O diagnóstico não altera regras. Mantém as ações documentadas VCR=5, MOZ=10 e
MAL=15 e testa apenas tetos hipotéticos de autonomia inicial/embarcada. A fonte
primária descreve a armada como provida para longo horizonte, mas os valores
abaixo são parâmetros de simulação, não conversões históricas.
"""
from __future__ import annotations

import json
from dataclasses import replace

from quintoimperio.domain import P3CampaignModel

SEEDS = range(24001, 24021)
CAPS = (120.0, 130.0, 140.0, 150.0, 160.0, 180.0)
DOCUMENTED = {"VCR": 5.0, "MOZ": 10.0, "MAL": 15.0}


def add(state, amount, cap):
    return replace(
        state,
        vessel=replace(
            state.vessel,
            provision_days=min(cap, state.vessel.provision_days + amount),
        ),
    )


def release(model, state):
    if state.active_stop_id is None:
        return state
    result = model.wait_for_stop_release(state)
    return result.state_after if result.executed else state


def run(model, seed, cap):
    state = model.initial_cabral_state(provision_days=cap)
    path = []
    while model.current_leg(state) is not None:
        node = state.vessel.location_node
        if node in DOCUMENTED and state.active_stop_id is not None:
            state = add(state, DOCUMENTED[node], cap)
        state = release(model, state)
        plan = model.plan_current_leg(state, seed=seed)
        if not plan.feasible:
            return {
                "completed": False,
                "location": state.vessel.location_node,
                "date": state.vessel.clock.current_date.isoformat(),
                "leg": model.current_leg(state).sequence if model.current_leg(state) else None,
                "route": model.current_leg(state).route_id if model.current_leg(state) else None,
                "blockers": list(plan.blockers),
                "provisions": round(state.vessel.provision_days, 4),
                "path": path,
            }
        path.append(plan.route_id)
        state = model.execute_voyage(state, plan)
    return {
        "completed": state.vessel.location_node == "CAN",
        "location": state.vessel.location_node,
        "date": state.vessel.clock.current_date.isoformat(),
        "leg": None,
        "route": None,
        "blockers": [],
        "provisions": round(state.vessel.provision_days, 4),
        "path": path,
    }


def main():
    model = P3CampaignModel()
    result = {"caps": {}, "seeds": list(SEEDS)}
    for cap in CAPS:
        rows = {str(seed): run(model, seed, cap) for seed in SEEDS}
        result["caps"][str(int(cap))] = {
            "completed": sum(row["completed"] for row in rows.values()),
            "final_locations": {
                loc: sum(r["location"] == loc for r in rows.values())
                for loc in sorted({r["location"] for r in rows.values()})
            },
            "rows": rows,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
