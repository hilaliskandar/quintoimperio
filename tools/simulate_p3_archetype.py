#!/usr/bin/env python3
"""Playtest sintético da tranche P3 Cabral por arquétipos.

Além dos dez arquétipos fixos já usados no MVP, ``RANDOM_PER_LEG`` sorteia
um arquétipo novo no início de cada perna alcançada. O sorteio usa um fluxo
pseudoaleatório separado da seed de risco/viagem para preservar o pareamento
dos eventos marítimos e tornar a sequência de decisões reproduzível.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from quintoimperio.domain import ChronologyMode, P3CampaignModel
from quintoimperio.domain.risk_mitigation import secure_provision_reserve_for_voyage
from simulate_player_archetype import ARCHETYPES, ArchetypePolicy, apply_planning, proactive_floor
from simulate_synthetic_player import Metrics, RESOURCE_BLOCKERS, reprovision, wait_guided

RANDOM_PER_LEG = "RANDOM_PER_LEG"
POLICIES = tuple(sorted(ARCHETYPES))
PLAYTEST_ARCHETYPES = tuple(sorted((*ARCHETYPES.keys(), RANDOM_PER_LEG)))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--player-id", type=int, required=True)
    p.add_argument("--archetype", choices=PLAYTEST_ARCHETYPES, required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--wave", type=int, default=20)
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def policy_for_leg(archetype: str, seed: int, leg_sequence: int) -> tuple[str, ArchetypePolicy]:
    if archetype != RANDOM_PER_LEG:
        return archetype, ARCHETYPES[archetype]
    rng = random.Random(seed * 1009 + leg_sequence * 9173 + 1500)
    name = rng.choice(POLICIES)
    return name, ARCHETYPES[name]


def wait_for_release(model: P3CampaignModel, state, metrics: Metrics):
    if state.active_stop_id is not None:
        metrics.attempt()
        result = model.wait_for_stop_release(state)
        if result.executed:
            metrics.executed()
            metrics.waits += 1
            state = result.state_after
        else:
            metrics.blocked(result.reasons)
        metrics.observe(state)
        return state, result.executed
    return wait_guided(model, state, metrics)


def documented_reprovision(model: P3CampaignModel, state, metrics: Metrics):
    """Usa primeiro a ação material específica da escala, quando disponível."""
    if not model.documented_cabral_stop_can_reprovision(state):
        return reprovision(model, state, metrics)
    metrics.attempt()
    result = model.reprovision_at_documented_cabral_stop(state)
    if result.executed:
        metrics.executed()
        metrics.reprovision_actions += 1
        metrics.reprovision_total += result.service_result.effect
        state = result.state_after
    else:
        metrics.blocked(result.reasons)
    metrics.observe(state)
    return state, result.executed


def resource_blocked(plan) -> bool:
    return any(
        reason in RESOURCE_BLOCKERS or "PROVISION" in reason for reason in plan.blockers
    )


def recover_documented_stop_before_wait(
    model: P3CampaignModel,
    state,
    metrics: Metrics,
    policy: ArchetypePolicy,
    seed: int,
):
    """Decide a ação one-shot antes de liberar a escala histórica.

    A ação não é automática. Perfis que seguem a recomendação logística podem
    usá-la preventivamente quando o horizonte + margem excede o estoque atual.
    Perfis que só reagem a bloqueios continuam podendo usá-la quando a própria
    perna corrente já está bloqueada por recursos.
    """
    if not model.documented_cabral_stop_can_reprovision(state):
        return state

    metrics.attempt()
    plan = model.plan_current_leg(state, seed=seed)
    if plan.feasible:
        metrics.executed()
    else:
        metrics.blocked(plan.blockers)
    blocked_need = resource_blocked(plan) and policy.recover_resources_after_block

    planned_need = False
    if policy.consult_logistics:
        metrics.attempt()
        metrics.recommendation_checks += 1
        view = model.logistics_planning_view(state, seed=seed)
        metrics.executed()
        if view.next_destination_provisions_evidence_indeterminate:
            metrics.indeterminate_destination_warnings += 1
        horizon = view.logistics_horizon_required_days
        if horizon is not None:
            target = horizon + view.recommended_margin_days + policy.extra_margin_days
            planned_need = (
                policy.follow_recommended_margin
                and state.vessel.provision_days < target
            )

    if not (blocked_need or planned_need):
        if policy.consult_logistics and not policy.follow_recommended_margin:
            metrics.recommendation_ignored += 1
        return state

    state, changed = documented_reprovision(model, state, metrics)
    if planned_need:
        if changed:
            metrics.recommendation_followed += 1
        else:
            metrics.recommendation_ignored += 1
    return state


def execute_leg(model: P3CampaignModel, state, metrics: Metrics, policy: ArchetypePolicy, seed: int):
    recovery = 0
    while True:
        metrics.attempt()
        plan = model.plan_current_leg(state, seed=seed)
        if plan.feasible:
            metrics.executed()
            metrics.attempt()
            if policy.secured_reserve_days > 0:
                secured = min(policy.secured_reserve_days, state.vessel.provision_days)
                prepared, resolved, _ = secure_provision_reserve_for_voyage(
                    model.session, state, plan, secured
                )
                state = model.execute_voyage(prepared, resolved)
            else:
                state = model.execute_voyage(state, plan)
            metrics.executed()
            metrics.voyage_actions += 1
            metrics.observe(state)
            return state, True

        metrics.blocked(plan.blockers)
        if recovery >= policy.max_recovery_steps:
            return state, False

        resource_block = resource_blocked(plan)
        if (
            resource_block
            and policy.recover_resources_after_block
            and model.documented_cabral_stop_can_reprovision(state)
        ):
            state, changed = documented_reprovision(model, state, metrics)
            recovery += 1
            if changed:
                continue

        if "HISTORICAL_STOP_NOT_RELEASED" in plan.blockers:
            state, changed = wait_for_release(model, state, metrics)
            recovery += 1
            if changed:
                continue

        if "HISTORICAL_DEPARTURE_NOT_REACHED" in plan.blockers:
            state, changed = wait_guided(model, state, metrics)
            recovery += 1
            if changed:
                continue

        if resource_block and policy.recover_resources_after_block:
            state, changed = reprovision(model, state, metrics)
            recovery += 1
            if changed:
                continue
        return state, False


def maybe_calicut_trade(model: P3CampaignModel, state, metrics: Metrics, policy: ArchetypePolicy, seed: int):
    if state.vessel.location_node != "CAL":
        return state
    metrics.attempt()
    access = model.negotiate_access(state)
    if access.executed:
        metrics.executed()
        metrics.access_negotiations += 1
        state = access.state_after
    else:
        metrics.blocked(access.reasons)
    metrics.observe(state)

    qty = policy.trade_quantity
    while qty >= 1:
        metrics.attempt()
        bought = model.buy(state, "PEPPER", qty, seed=seed)
        if bought.executed:
            metrics.executed()
            metrics.trade_actions += 1
            state = bought.state_after
            break
        metrics.blocked(bought.reasons)
        qty -= 1
    metrics.observe(state)
    return state


def run_player(player_id: int, archetype: str, seed: int, wave: int = 20) -> dict:
    model = P3CampaignModel()
    state = model.initial_cabral_playable_state()
    metrics = Metrics(player_id=player_id, profile=archetype, seed=seed, wave=wave)
    metrics.observe(state)
    start = state.vessel.clock.current_date
    sequence: list[dict[str, object]] = []
    calicut_actions_done = False

    while model.current_leg(state) is not None:
        leg = model.current_leg(state)
        assert leg is not None
        policy_name, policy = policy_for_leg(archetype, seed, leg.sequence)
        sequence.append(
            {
                "leg_sequence": leg.sequence,
                "route_id": leg.route_id,
                "archetype": policy_name,
            }
        )

        state = proactive_floor(model, state, metrics, policy.proactive_floor_days)
        state = apply_planning(model, state, metrics, policy, seed)
        state = recover_documented_stop_before_wait(model, state, metrics, policy, seed)

        departure = model.guided_departure_date(state)
        if (
            policy.wait_before_departure
            and departure is not None
            and state.vessel.clock.current_date < departure
        ):
            state, _ = wait_for_release(model, state, metrics)

        state, ok = execute_leg(model, state, metrics, policy, seed)
        if not ok:
            break

        if policy.contact_authority and state.vessel.location_node == "MAL" and model.current_leg(state) is not None:
            metrics.attempt()
            contacted = model.contact_authority(state)
            if contacted.executed:
                metrics.executed()
                state = contacted.state_after
            else:
                metrics.blocked(contacted.reasons)
            metrics.observe(state)

        if state.vessel.location_node == "CAL" and not calicut_actions_done:
            state = maybe_calicut_trade(model, state, metrics, policy, seed)
            calicut_actions_done = True

    reached_cannanore = state.vessel.location_node == "CAN" and model.current_leg(state) is None
    completed = reached_cannanore and state.chronology_mode is ChronologyMode.GUIDED
    events = state.voyage_event_history
    switches = sum(
        a["archetype"] != b["archetype"] for a, b in zip(sequence, sequence[1:])
    )

    return {
        "wave": wave,
        "player_id": player_id,
        "archetype": archetype,
        "archetype_label": (
            "Arquétipo aleatório por perna" if archetype == RANDOM_PER_LEG else ARCHETYPES[archetype].label
        ),
        "game_style": (
            "mixed random-per-leg" if archetype == RANDOM_PER_LEG else ARCHETYPES[archetype].game_style
        ),
        "seed": seed,
        "completed": completed,
        "actions_attempted": metrics.actions_attempted,
        "actions_executed": metrics.actions_executed,
        "blocked_attempts": metrics.blocked_attempts,
        "recommendation_checks": metrics.recommendation_checks,
        "recommendation_followed": metrics.recommendation_followed,
        "recommendation_ignored": metrics.recommendation_ignored,
        "indeterminate_destination_warnings": metrics.indeterminate_destination_warnings,
        "blockers": dict(sorted(metrics.blockers.items())),
        "voyage_actions": metrics.voyage_actions,
        "waits": metrics.waits,
        "reprovision_actions": metrics.reprovision_actions,
        "reprovision_total": round(metrics.reprovision_total, 2),
        "access_negotiations": metrics.access_negotiations,
        "trade_actions": metrics.trade_actions,
        "elapsed_days": (state.vessel.clock.current_date - start).days,
        "final_date": state.vessel.clock.current_date.isoformat(),
        "final_location": state.vessel.location_node,
        "chronology_mode": state.chronology_mode.value,
        "counterfactual": state.chronology_mode is ChronologyMode.COUNTERFACTUAL,
        "min_provisions": round(metrics.min_provisions, 2),
        "min_condition": round(metrics.min_condition, 2),
        "voyage_events": len(events),
        "positive_provision_events": sum(e.provision_delta > 0 for e in events),
        "negative_provision_events": sum(e.provision_delta < 0 for e in events),
        "timing_events": sum(e.extra_days > 0 for e in events),
        "net_event_provision_delta": round(sum(e.provision_delta for e in events), 2),
        "capital_final": round(state.commerce.capital_index, 4),
        "archetype_switches": switches,
        "archetype_sequence": sequence,
    }


def main() -> None:
    a = parse_args()
    result = run_player(a.player_id, a.archetype, a.seed, a.wave)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
