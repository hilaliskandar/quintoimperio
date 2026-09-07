#!/usr/bin/env python3
"""Sensibilidade da projeção de carena documentada em Anjediva."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from quintoimperio.domain import ReturnCampaignModel
from diagnose_return_from_mvp import (
    ARCHETYPES_DIAGNOSTIC,
    apply_documented_provisions,
    complete_mvp_state,
)


SEED = 23004
REPAIR_POINTS = (0.0, 1.0, 2.0, 5.0, 10.0)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def run_return(state, requested_repair: float):
    model = ReturnCampaignModel()
    state = model.activate_return(state)
    repair_effect = 0.0
    repair_days = 0
    routes = []
    blocker = None

    while state.active_expedition_id == model.RETURN_EXPEDITION_ID:
        state, _ = apply_documented_provisions(model, state)

        if requested_repair > 0 and model.documented_stop_can_repair(state):
            result = model.repair_at_documented_stop(state, requested_repair)
            if result.executed:
                repair_effect += result.service_result.effect
                repair_days += result.service_result.days_spent
                state = result.state_after

        departure = model.guided_departure_date(state)
        if departure is not None and state.vessel.clock.current_date < departure:
            waited = model.wait_for_guided_departure(state)
            if not waited.executed:
                blocker = list(waited.reasons)
                break
            state = waited.state_after

        leg = model.current_leg(state)
        if leg is None:
            blocker = ["RETURN_ACTIVE_WITHOUT_LEG"]
            break
        plan = model.plan_current_leg(state, seed=SEED)
        if not plan.feasible:
            blocker = list(plan.blockers)
            break
        routes.append(leg.route_id)
        state = model.execute_voyage(state, plan)

    return {
        "requested_repair_points": requested_repair,
        "repair_effect": round(repair_effect, 4),
        "repair_days": repair_days,
        "completed": state.active_expedition_id is None and state.vessel.location_node == "BRG",
        "routes_completed": routes,
        "blockers": blocker or [],
        "final_location": state.vessel.location_node,
        "final_date": state.vessel.clock.current_date.isoformat(),
        "final_condition": round(state.vessel.condition, 4),
        "chronology_mode": state.chronology_mode.value,
    }


def main():
    args = parse_args()
    cases = []
    for archetype in ARCHETYPES_DIAGNOSTIC:
        state, completed = complete_mvp_state(archetype, SEED)
        if not completed:
            continue
        for points in REPAIR_POINTS:
            cases.append(
                {
                    "archetype": archetype,
                    "seed": SEED,
                    "mvp_final_condition": round(state.vessel.condition, 4),
                    "result": run_return(state, points),
                }
            )

    summary = {}
    for points in REPAIR_POINTS:
        subset = [c for c in cases if c["result"]["requested_repair_points"] == points]
        summary[str(points)] = {
            "eligible": len(subset),
            "completed": sum(c["result"]["completed"] for c in subset),
            "blockers": sorted(
                {b for c in subset for b in c["result"].get("blockers", [])}
            ),
        }

    report = {
        "diagnostic": "P1_ANJEDIVA_CAREENING_SENSITIVITY_WITH_SANTA_MARIA",
        "seed": SEED,
        "repair_points": list(REPAIR_POINTS),
        "summary": summary,
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
