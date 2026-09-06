#!/usr/bin/env python3
"""Onda 5: testa reserva logística sem imputar serviços historicamente indeterminados.

Mantém a política de preparação da onda 2 e acrescenta uma única regra: depois
de tornar a próxima perna viável, solicita uma reserva adicional de 30 dias de
provisões somente quando o porto atual possui reabastecimento documentado e
acionável. A margem é parâmetro experimental, não fato histórico.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel, PortServiceKind

from simulate_synthetic_player import Metrics, PROFILES, RESOURCE_BLOCKERS, proactive_policy, reprovision, wait_guided


RESERVE_REQUEST_DAYS = 30.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", type=int, required=True)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def prepare_with_reserve(model, state, metrics: Metrics, seed: int, counters: dict[str, float]):
    """Torna a perna viável e, se possível, adiciona uma margem experimental."""
    for _ in range(8):
        metrics.attempt()
        metrics.readiness_checks += 1
        plan = model.plan_current_leg(state, seed=seed)
        metrics.executed()
        resource_reasons = tuple(
            reason for reason in plan.blockers
            if reason in RESOURCE_BLOCKERS or "PROVISION" in reason
        )
        if not resource_reasons:
            break
        state, changed = reprovision(model, state, metrics)
        if not changed:
            return state

    view = model.service_view(state, PortServiceKind.PROVISIONS)
    if not view.historical_documented or not view.actionable:
        counters["reserve_skipped_no_documented_service"] += 1
        return state

    before = float(state.vessel.provision_days)
    state, changed = reprovision(model, state, metrics, RESERVE_REQUEST_DAYS)
    if changed:
        added = float(state.vessel.provision_days) - before
        counters["reserve_actions"] += 1
        counters["reserve_days_added"] += max(0.0, added)
    else:
        counters["reserve_failed"] += 1
    return state


def plan_and_execute(model, state, metrics: Metrics, seed: int):
    recovery_steps = 0
    while recovery_steps < 12:
        metrics.attempt()
        plan = model.plan_current_leg(state, seed=seed)
        if plan.feasible:
            metrics.executed()
            metrics.attempt()
            state = model.execute_voyage(state, plan)
            metrics.executed()
            metrics.voyage_actions += 1
            metrics.observe(state)
            return state, True

        metrics.blocked(plan.blockers)
        if "HISTORICAL_DEPARTURE_NOT_REACHED" in plan.blockers:
            state, changed = wait_guided(model, state, metrics)
            recovery_steps += 1
            if changed:
                continue
        if any(reason in RESOURCE_BLOCKERS or "PROVISION" in reason for reason in plan.blockers):
            state, changed = reprovision(model, state, metrics)
            recovery_steps += 1
            if changed:
                continue
        return state, False
    return state, False


def run_player(player_id: int, profile: str, seed: int) -> dict:
    model = HistoricalCampaignModel()
    progress_model = CampaignProgressModel(model.session)
    state = model.initial_state(active_expedition_id="EXP_GAMA_1497")
    metrics = Metrics(player_id=player_id, profile=profile, seed=seed, wave=5)
    counters = {
        "reserve_actions": 0,
        "reserve_days_added": 0.0,
        "reserve_failed": 0,
        "reserve_skipped_no_documented_service": 0,
    }
    metrics.observe(state)
    start_date = state.vessel.clock.current_date

    while model.current_leg(state) is not None:
        state = proactive_policy(model, state, metrics, profile)
        departure = model.guided_departure_date(state)
        if departure is not None and state.vessel.clock.current_date < departure:
            state = prepare_with_reserve(model, state, metrics, seed, counters)
        if profile != "IMPATIENT" and departure is not None and state.vessel.clock.current_date < departure:
            state, _ = wait_guided(model, state, metrics)

        state, ok = plan_and_execute(model, state, metrics, seed)
        if not ok:
            break

        if state.vessel.location_node == "MAL" and model.current_leg(state) is not None:
            metrics.attempt()
            contacted = model.contact_authority(state)
            if contacted.executed:
                metrics.executed()
                state = contacted.state_after
            else:
                metrics.blocked(contacted.reasons)
            metrics.observe(state)

    if state.vessel.location_node == "CAL":
        metrics.attempt()
        access = model.negotiate_access(state)
        if access.executed:
            metrics.executed()
            metrics.access_negotiations += 1
            state = access.state_after
        else:
            metrics.blocked(access.reasons)
        metrics.observe(state)

        qty = 4.0 if profile == "TRADER" else 1.0
        while qty >= 1.0:
            metrics.attempt()
            bought = model.buy(state, "PEPPER", qty, seed=seed)
            if bought.executed:
                metrics.executed()
                metrics.trade_actions += 1
                state = bought.state_after
                break
            metrics.blocked(bought.reasons)
            qty -= 1.0
        metrics.observe(state)

    progress = progress_model.progress(state)
    summary = progress_model.summary(state)
    elapsed_days = (state.vessel.clock.current_date - start_date).days
    final_cargo = {item.good_id: item.quantity for item in state.commerce.cargo if item.quantity > 0}

    return {
        "wave": 5,
        "player_id": player_id,
        "profile": profile,
        "seed": seed,
        "reserve_request_days": RESERVE_REQUEST_DAYS,
        "completed": progress.completed,
        "current_objective": progress.current_objective,
        "actions_attempted": metrics.actions_attempted,
        "actions_executed": metrics.actions_executed,
        "blocked_attempts": metrics.blocked_attempts,
        "readiness_checks": metrics.readiness_checks,
        "blockers": dict(sorted(metrics.blockers.items())),
        "first_block_action": metrics.first_block_action,
        "recovered_after_block": metrics.recovered_after_block,
        "voyage_actions": metrics.voyage_actions,
        "waits": metrics.waits,
        "reprovision_actions": metrics.reprovision_actions,
        "reprovision_total": round(metrics.reprovision_total, 2),
        "access_negotiations": metrics.access_negotiations,
        "trade_actions": metrics.trade_actions,
        "elapsed_days": elapsed_days,
        "final_date": state.vessel.clock.current_date.isoformat(),
        "final_location": state.vessel.location_node,
        "chronology_mode": state.chronology_mode.value,
        "counterfactual": state.chronology_mode is ChronologyMode.COUNTERFACTUAL,
        "min_provisions": round(metrics.min_provisions, 2),
        "min_condition": round(metrics.min_condition, 2),
        "voyage_events": len(state.voyage_event_history),
        "capital_final": round(summary.capital_index, 4),
        "capacity_used_final": round(summary.capacity_used, 4),
        "capacity_total": round(summary.capacity_total, 4),
        "cargo_final": final_cargo,
        "knowledge_nodes": summary.knowledge_nodes,
        "contacted_actor_ids": list(summary.contacted_actor_ids),
        **{key: round(value, 2) if isinstance(value, float) else value for key, value in counters.items()},
    }


def main() -> None:
    args = parse_args()
    result = run_player(args.player_id, args.profile, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
