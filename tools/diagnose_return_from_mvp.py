#!/usr/bin/env python3
"""Diagnóstico de continuidade P1 a partir de estados efetivamente concluídos do MVP."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from quintoimperio.domain import (
    CampaignProgressModel,
    HistoricalCampaignModel,
    ReturnCampaignModel,
)

from simulate_player_archetype import (
    ARCHETYPES,
    apply_planning,
    plan_execute,
    proactive_floor,
)
from simulate_synthetic_player import Metrics, wait_guided


ARCHETYPES_DIAGNOSTIC = (
    "GRAND_STRATEGIST",
    "SURVIVALIST",
    "MERCHANT",
    "ROLEPLAYER",
    "COMPLETIONIST",
)
SEEDS = (23001, 23002, 23003, 23004)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def complete_mvp_state(archetype: str, seed: int):
    policy = ARCHETYPES[archetype]
    model = HistoricalCampaignModel()
    progress_model = CampaignProgressModel(model.session)
    state = model.initial_playable_state()
    metrics = Metrics(
        player_id=0,
        profile=archetype,
        seed=seed,
        wave=17,
    )
    metrics.observe(state)

    while model.current_leg(state) is not None:
        state = proactive_floor(model, state, metrics, policy.proactive_floor_days)
        state = apply_planning(model, state, metrics, policy, seed)
        departure = model.guided_departure_date(state)
        if (
            policy.wait_before_departure
            and departure is not None
            and state.vessel.clock.current_date < departure
        ):
            state, _ = wait_guided(model, state, metrics)
        state, ok = plan_execute(model, state, metrics, policy, seed)
        if not ok:
            break
        if (
            policy.contact_authority
            and state.vessel.location_node == "MAL"
            and model.current_leg(state) is not None
        ):
            contacted = model.contact_authority(state)
            if contacted.executed:
                state = contacted.state_after

    if state.vessel.location_node == "CAL":
        access = model.negotiate_access(state)
        if access.executed:
            state = access.state_after
        qty = policy.trade_quantity
        while qty >= 1:
            bought = model.buy(state, "PEPPER", qty, seed=seed)
            if bought.executed:
                state = bought.state_after
                break
            qty -= 1

    progress = progress_model.progress(state)
    return state, progress.completed


def execute_return(state, seed: int):
    model = ReturnCampaignModel()
    state = model.activate_return(state)
    routes = []
    blockers = []
    provision_actions = 0

    initial_provisions = state.vessel.provision_days
    first_view = model.logistics_planning_view(state, seed=seed)

    while state.active_expedition_id == model.RETURN_EXPEDITION_ID:
        if model.documented_stop_can_reprovision(state):
            for _ in range(3):
                if state.vessel.provision_days >= 120.0:
                    break
                result = model.reprovision_at_documented_stop(state, 120.0)
                if not result.executed:
                    break
                provision_actions += 1
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

    completed = (
        state.active_expedition_id is None
        and state.vessel.location_node == model.RETURN_END_NODE
    )
    return {
        "completed": completed,
        "initial_provisions": round(initial_provisions, 4),
        "first_leg_required": (
            None
            if first_view.next_leg_required_days is None
            else round(first_view.next_leg_required_days, 4)
        ),
        "first_horizon_required": (
            None
            if first_view.logistics_horizon_required_days is None
            else round(first_view.logistics_horizon_required_days, 4)
        ),
        "routes_completed": routes,
        "blockers": blockers,
        "provision_actions": provision_actions,
        "final_location": state.vessel.location_node,
        "final_date": state.vessel.clock.current_date.isoformat(),
        "chronology_mode": state.chronology_mode.value,
        "final_provisions": round(state.vessel.provision_days, 4),
    }


def main():
    args = parse_args()
    cases = []
    for archetype in ARCHETYPES_DIAGNOSTIC:
        for seed in SEEDS:
            state, mvp_completed = complete_mvp_state(archetype, seed)
            row = {
                "archetype": archetype,
                "seed": seed,
                "mvp_completed": mvp_completed,
                "mvp_final_location": state.vessel.location_node,
                "mvp_final_date": state.vessel.clock.current_date.isoformat(),
                "mvp_final_provisions": round(state.vessel.provision_days, 4),
            }
            if mvp_completed:
                row["return"] = execute_return(state, seed)
            cases.append(row)

    mvp_completed_cases = [case for case in cases if case["mvp_completed"]]
    return_completed_cases = [
        case
        for case in mvp_completed_cases
        if case.get("return", {}).get("completed")
    ]
    blocker_counts = Counter()
    by_archetype = defaultdict(lambda: {"mvp_completed": 0, "return_completed": 0})
    for case in cases:
        bucket = by_archetype[case["archetype"]]
        if case["mvp_completed"]:
            bucket["mvp_completed"] += 1
            if case.get("return", {}).get("completed"):
                bucket["return_completed"] += 1
            else:
                blocker_counts.update(case.get("return", {}).get("blockers", []))

    report = {
        "diagnostic": "P1_RETURN_FROM_MVP_WAVE17",
        "archetypes": list(ARCHETYPES_DIAGNOSTIC),
        "seeds": list(SEEDS),
        "cases_total": len(cases),
        "mvp_completed": len(mvp_completed_cases),
        "return_completed": len(return_completed_cases),
        "blockers": dict(sorted(blocker_counts.items())),
        "by_archetype": dict(sorted(by_archetype.items())),
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
