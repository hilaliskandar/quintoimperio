#!/usr/bin/env python3
"""Controle pareado do retorno com Santa Maria e carena mínima de 2 pontos."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from quintoimperio.domain import ReturnCampaignModel
from diagnose_return_from_mvp import (
    ARCHETYPES_DIAGNOSTIC,
    SEEDS,
    apply_documented_provisions,
    complete_mvp_state,
)

CARENING_POINTS = 2.0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def execute_return(state, seed: int):
    model = ReturnCampaignModel()
    state = model.activate_return(state)
    routes = []
    blockers = []
    repair_actions = 0
    provision_actions = 0

    while state.active_expedition_id == model.RETURN_EXPEDITION_ID:
        state, actions = apply_documented_provisions(model, state)
        provision_actions += actions

        if model.documented_stop_can_repair(state):
            result = model.repair_at_documented_stop(state, CARENING_POINTS)
            if result.executed:
                repair_actions += 1
                state = result.state_after

        departure = model.guided_departure_date(state)
        if departure is not None and state.vessel.clock.current_date < departure:
            waited = model.wait_for_guided_departure(state)
            if not waited.executed:
                blockers.extend(waited.reasons)
                break
            state = waited.state_after

        leg = model.current_leg(state)
        if leg is None:
            blockers.append("RETURN_ACTIVE_WITHOUT_LEG")
            break
        plan = model.plan_current_leg(state, seed=seed)
        if not plan.feasible:
            blockers.extend(plan.blockers)
            break
        routes.append(leg.route_id)
        state = model.execute_voyage(state, plan)

    return {
        "completed": state.active_expedition_id is None and state.vessel.location_node == "BRG",
        "routes_completed": routes,
        "blockers": blockers,
        "repair_actions": repair_actions,
        "provision_actions": provision_actions,
        "final_location": state.vessel.location_node,
        "final_date": state.vessel.clock.current_date.isoformat(),
        "final_condition": round(state.vessel.condition, 4),
        "chronology_mode": state.chronology_mode.value,
    }


def main():
    args = parse_args()
    cases = []
    by_archetype = defaultdict(lambda: {"mvp_completed": 0, "return_completed": 0})
    blockers = Counter()

    for archetype in ARCHETYPES_DIAGNOSTIC:
        for seed in SEEDS:
            state, mvp_completed = complete_mvp_state(archetype, seed)
            row = {
                "archetype": archetype,
                "seed": seed,
                "mvp_completed": mvp_completed,
                "mvp_final_provisions": round(state.vessel.provision_days, 4),
                "mvp_final_condition": round(state.vessel.condition, 4),
            }
            bucket = by_archetype[archetype]
            if mvp_completed:
                bucket["mvp_completed"] += 1
                result = execute_return(state, seed)
                row["return"] = result
                if result["completed"]:
                    bucket["return_completed"] += 1
                else:
                    blockers.update(result["blockers"])
            cases.append(row)

    eligible = [c for c in cases if c["mvp_completed"]]
    completed = [c for c in eligible if c.get("return", {}).get("completed")]
    report = {
        "diagnostic": "P1_RETURN_SANTA_MARIA_AND_CAREENING_WAVE19",
        "careening_points": CARENING_POINTS,
        "cases_total": len(cases),
        "mvp_completed": len(eligible),
        "return_completed": len(completed),
        "blockers": dict(sorted(blockers.items())),
        "by_archetype": dict(sorted(by_archetype.items())),
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
