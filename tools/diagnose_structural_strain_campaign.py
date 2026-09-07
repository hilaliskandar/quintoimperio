#!/usr/bin/env python3
"""Diagnóstico de STRUCTURAL_STRAIN ao longo da campanha Lisboa–Calecute.

Não altera parâmetros. Reutiliza políticas competentes do playtest de arquétipos e
registra, sob seeds pareadas, quando a tensão estrutural ocorre e se produz bloqueio
posterior por condição do navio.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from quintoimperio.domain import HistoricalCampaignModel
from quintoimperio.domain.risk_mitigation import secure_provision_reserve_for_voyage
from quintoimperio.domain.voyage_event import VoyageEventType
from simulate_player_archetype import ARCHETYPES, apply_planning, proactive_floor
from simulate_synthetic_player import Metrics, RESOURCE_BLOCKERS, reprovision, wait_guided

COMPETENT = (
    "GRAND_STRATEGIST",
    "SURVIVALIST",
    "MERCHANT",
    "ROLEPLAYER",
    "OPTIMIZER",
    "COMPLETIONIST",
    "CASUAL",
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--seed-start", type=int, default=30001)
    p.add_argument("--seed-count", type=int, default=1000)
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    return p.parse_args()


def execute_leg(model, state, metrics, policy, seed):
    recovery = 0
    while True:
        metrics.attempt()
        plan = model.plan_current_leg(state, seed=seed)
        if plan.feasible:
            metrics.executed()
            pre_condition = state.vessel.condition
            route_id = plan.route_id
            history_before = len(state.voyage_event_history)
            departure_date = plan.departure_date
            if policy.secured_reserve_days > 0:
                secured = min(policy.secured_reserve_days, state.vessel.provision_days)
                prepared, resolved, _ = secure_provision_reserve_for_voyage(
                    model.session, state, plan, secured
                )
                state = model.execute_voyage(prepared, resolved)
            else:
                state = model.execute_voyage(state, plan)
            resolved_events = state.voyage_event_history[history_before:]
            metrics.executed()
            metrics.voyage_actions += 1
            metrics.observe(state)
            return (
                state,
                tuple(resolved_events),
                pre_condition,
                route_id,
                departure_date,
                True,
            )

        metrics.blocked(plan.blockers)
        if recovery >= policy.max_recovery_steps:
            return (
                state,
                (),
                state.vessel.condition,
                getattr(plan, "route_id", ""),
                getattr(plan, "departure_date", state.vessel.clock.current_date),
                False,
            )
        if "HISTORICAL_DEPARTURE_NOT_REACHED" in plan.blockers:
            state, changed = wait_guided(model, state, metrics)
            recovery += 1
            if changed:
                continue
        resource_block = any(
            reason in RESOURCE_BLOCKERS or "PROVISION" in reason for reason in plan.blockers
        )
        if resource_block and policy.recover_resources_after_block:
            state, changed = reprovision(model, state, metrics)
            recovery += 1
            if changed:
                continue
        return (
            state,
            (),
            state.vessel.condition,
            getattr(plan, "route_id", ""),
            getattr(plan, "departure_date", state.vessel.clock.current_date),
            False,
        )


def run_one(archetype: str, seed: int):
    policy = ARCHETYPES[archetype]
    model = HistoricalCampaignModel()
    state = model.initial_playable_state()
    metrics = Metrics(player_id=seed, profile=archetype, seed=seed, wave=17)
    metrics.observe(state)
    rows = []

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

        state_after, events, pre_condition, route_id, departure_date, ok = execute_leg(
            model, state, metrics, policy, seed
        )
        if not ok:
            break

        structural = next(
            (e for e in events if e.event_type is VoyageEventType.STRUCTURAL_STRAIN),
            None,
        )
        if structural is not None:
            next_plan = None
            next_blocker = False
            if model.current_leg(state_after) is not None:
                next_plan = model.plan_current_leg(state_after, seed=seed)
                next_blocker = "VESSEL_CONDITION_TOO_LOW" in next_plan.blockers
            rows.append(
                {
                    "seed": seed,
                    "archetype": archetype,
                    "route_id": route_id,
                    "departure_date": departure_date.isoformat(),
                    "condition_before": round(pre_condition, 4),
                    "condition_loss_event": round(structural.condition_loss, 4),
                    "condition_after": round(state_after.vessel.condition, 4),
                    "crossed_40": state_after.vessel.condition < 40,
                    "crossed_20": state_after.vessel.condition < 20,
                    "next_leg_condition_blocker": next_blocker,
                    "next_route_id": getattr(next_plan, "route_id", "") if next_plan else "",
                }
            )
        state = state_after

        if (
            policy.contact_authority
            and state.vessel.location_node == "MAL"
            and model.current_leg(state) is not None
        ):
            contacted = model.contact_authority(state)
            if contacted.executed:
                state = contacted.state_after

    return rows, state.vessel.location_node == "CAL", round(metrics.min_condition, 4)


def main():
    args = parse_args()
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    all_rows = []
    campaigns = []
    for archetype in COMPETENT:
        for seed in range(args.seed_start, args.seed_start + args.seed_count):
            rows, reached_calicut, min_condition = run_one(archetype, seed)
            all_rows.extend(rows)
            campaigns.append(
                {
                    "seed": seed,
                    "archetype": archetype,
                    "reached_calicut": reached_calicut,
                    "min_condition": min_condition,
                    "structural_events": len(rows),
                }
            )

    fields = [
        "seed", "archetype", "route_id", "departure_date", "condition_before",
        "condition_loss_event", "condition_after", "crossed_40", "crossed_20",
        "next_leg_condition_blocker", "next_route_id",
    ]
    with args.csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_rows)

    affected_campaigns = sum(c["structural_events"] > 0 for c in campaigns)
    reached = sum(c["reached_calicut"] for c in campaigns)
    summary = {
        "seed_start": args.seed_start,
        "seed_count": args.seed_count,
        "archetypes": list(COMPETENT),
        "campaigns": len(campaigns),
        "campaigns_reaching_calicut": reached,
        "structural_events": len(all_rows),
        "campaigns_with_structural_event": affected_campaigns,
        "events_after_condition_below_40": sum(r["crossed_40"] for r in all_rows),
        "events_after_condition_below_20": sum(r["crossed_20"] for r in all_rows),
        "next_leg_condition_blockers": sum(r["next_leg_condition_blocker"] for r in all_rows),
        "minimum_condition_all_campaigns": min(c["min_condition"] for c in campaigns),
        "by_archetype": {},
        "by_route": {},
    }
    for archetype in COMPETENT:
        subset = [c for c in campaigns if c["archetype"] == archetype]
        events = [r for r in all_rows if r["archetype"] == archetype]
        summary["by_archetype"][archetype] = {
            "reached_calicut": sum(c["reached_calicut"] for c in subset),
            "campaigns": len(subset),
            "structural_events": len(events),
            "condition_blockers": sum(r["next_leg_condition_blocker"] for r in events),
            "min_condition": min(c["min_condition"] for c in subset),
        }
    for route in sorted({r["route_id"] for r in all_rows}):
        events = [r for r in all_rows if r["route_id"] == route]
        summary["by_route"][route] = {
            "events": len(events),
            "below_40": sum(r["crossed_40"] for r in events),
            "below_20": sum(r["crossed_20"] for r in events),
            "condition_blockers": sum(r["next_leg_condition_blocker"] for r in events),
        }

    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
