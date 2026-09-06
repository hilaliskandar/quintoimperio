#!/usr/bin/env python3
"""Playtest sintético por arquétipos inspirados em gêneros/estilos de jogo.

Os arquétipos não pretendem classificar pessoas reais. Eles são políticas de teste
que usam somente ações e leituras públicas de ``HistoricalCampaignModel`` para
pressionar a mesma campanha com estratégias de decisão diferentes.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel

from simulate_synthetic_player import Metrics, RESOURCE_BLOCKERS, reprovision, wait_guided


@dataclass(frozen=True)
class ArchetypePolicy:
    label: str
    game_style: str
    description: str
    consult_logistics: bool
    follow_recommended_margin: bool
    extra_margin_days: float
    wait_before_departure: bool
    proactive_floor_days: float
    max_recovery_steps: int
    recover_resources_after_block: bool
    contact_authority: bool
    trade_quantity: float


ARCHETYPES: dict[str, ArchetypePolicy] = {
    "GRAND_STRATEGIST": ArchetypePolicy(
        "Grande estrategista", "grand strategy / 4X",
        "Planeja o horizonte completo, preserva margem e aceita gastar ações para reduzir risco sistêmico.",
        True, True, 0.0, True, 45.0, 12, True, True, 2.0,
    ),
    "SURVIVALIST": ArchetypePolicy(
        "Sobrevivencialista", "survival / expedition management",
        "Prioriza redundância logística e mantém colchão adicional acima da recomendação pública.",
        True, True, 20.0, True, 85.0, 12, True, True, 1.0,
    ),
    "MERCHANT": ArchetypePolicy(
        "Mercador", "trading / tycoon",
        "Garante a viagem, evita excesso logístico deliberado e maximiza a operação comercial final.",
        True, True, 0.0, True, 45.0, 10, True, True, 4.0,
    ),
    "SPEEDRUNNER": ArchetypePolicy(
        "Speedrunner", "speedrun / action optimization",
        "Tenta avançar imediatamente, ignora recomendações não obrigatórias e corrige apenas bloqueios duros.",
        False, False, 0.0, False, 0.0, 8, True, False, 1.0,
    ),
    "ROGUELIKE": ArchetypePolicy(
        "Roguelike", "roguelike / permadeath",
        "Aceita risco, não cria reserva preventiva e abandona a sessão quando um erro logístico exige recuperação.",
        True, False, 0.0, True, 0.0, 0, False, True, 1.0,
    ),
    "ROLEPLAYER": ArchetypePolicy(
        "Interpretativo histórico", "historical RPG / roleplay",
        "Segue a cronologia observada, respeita avisos, contata autoridades e prefere decisões narrativamente coerentes.",
        True, True, 0.0, True, 45.0, 10, True, True, 1.0,
    ),
    "EXPLORER": ArchetypePolicy(
        "Explorador", "exploration / adventure",
        "Inspeciona o estado e avisos com frequência, interage com atores documentados, mas evita superotimização de reservas.",
        True, False, 0.0, True, 45.0, 10, True, True, 1.0,
    ),
    "OPTIMIZER": ArchetypePolicy(
        "Otimizador", "puzzle / systems optimization",
        "Usa o horizonte e a margem exatamente como informação de restrição, buscando o menor preparo suficiente.",
        True, True, 0.0, True, 0.0, 12, True, False, 1.0,
    ),
    "COMPLETIONIST": ArchetypePolicy(
        "Completista", "completionist / achievement hunting",
        "Procura concluir a campanha com ampla segurança, contato social e operação comercial, mesmo com mais ações.",
        True, True, 10.0, True, 70.0, 12, True, True, 2.0,
    ),
    "CASUAL": ArchetypePolicy(
        "Casual guiado", "casual / tutorial-led",
        "Usa orientação básica, espera quando instruído e reage a problemas apenas quando eles se tornam visíveis.",
        True, True, 0.0, True, 30.0, 4, True, False, 1.0,
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", type=int, required=True)
    parser.add_argument("--archetype", choices=sorted(ARCHETYPES), required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def proactive_floor(model, state, metrics: Metrics, floor: float):
    while floor > 0 and state.vessel.provision_days < floor:
        state, changed = reprovision(model, state, metrics)
        if not changed:
            break
    return state


def apply_archetype_planning(model, state, metrics: Metrics, policy: ArchetypePolicy, seed: int):
    if not policy.consult_logistics:
        return state

    for _ in range(8):
        metrics.attempt()
        metrics.recommendation_checks += 1
        view = model.logistics_planning_view(state, seed=seed)
        metrics.executed()
        if view.next_destination_provisions_evidence_indeterminate:
            metrics.indeterminate_destination_warnings += 1

        horizon = view.logistics_horizon_required_days
        if horizon is None:
            return state
        target = horizon + view.recommended_margin_days + policy.extra_margin_days

        if state.vessel.provision_days >= target:
            return state
        if not policy.follow_recommended_margin:
            metrics.recommendation_ignored += 1
            return state

        state, changed = reprovision(model, state, metrics)
        if not changed:
            metrics.recommendation_ignored += 1
            return state
        metrics.recommendation_followed += 1
    return state


def plan_and_execute_archetype(model, state, metrics: Metrics, policy: ArchetypePolicy, seed: int):
    recovery_steps = 0
    while True:
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
        if recovery_steps >= policy.max_recovery_steps:
            return state, False

        if "HISTORICAL_DEPARTURE_NOT_REACHED" in plan.blockers:
            state, changed = wait_guided(model, state, metrics)
            recovery_steps += 1
            if changed:
                continue

        resource_block = any(
            reason in RESOURCE_BLOCKERS or "PROVISION" in reason for reason in plan.blockers
        )
        if resource_block and policy.recover_resources_after_block:
            state, changed = reprovision(model, state, metrics)
            recovery_steps += 1
            if changed:
                continue
        return state, False


def run_player(player_id: int, archetype: str, seed: int) -> dict:
    policy = ARCHETYPES[archetype]
    model = HistoricalCampaignModel()
    progress_model = CampaignProgressModel(model.session)
    state = model.initial_playable_state()
    metrics = Metrics(player_id=player_id, profile=archetype, seed=seed, wave=11)
    metrics.observe(state)
    start_date = state.vessel.clock.current_date

    while model.current_leg(state) is not None:
        state = proactive_floor(model, state, metrics, policy.proactive_floor_days)
        state = apply_archetype_planning(model, state, metrics, policy, seed)

        departure = model.guided_departure_date(state)
        if (
            policy.wait_before_departure
            and departure is not None
            and state.vessel.clock.current_date < departure
        ):
            state, _ = wait_guided(model, state, metrics)

        state, ok = plan_and_execute_archetype(model, state, metrics, policy, seed)
        if not ok:
            break

        if (
            policy.contact_authority
            and state.vessel.location_node == "MAL"
            and model.current_leg(state) is not None
        ):
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

        qty = policy.trade_quantity
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
    final_cargo = {
        item.good_id: item.quantity for item in state.commerce.cargo if item.quantity > 0
    }

    return {
        "wave": 11,
        "player_id": player_id,
        "profile": archetype,
        "archetype": archetype,
        "archetype_label": policy.label,
        "game_style": policy.game_style,
        "archetype_description": policy.description,
        "seed": seed,
        "completed": progress.completed,
        "current_objective": progress.current_objective,
        "actions_attempted": metrics.actions_attempted,
        "actions_executed": metrics.actions_executed,
        "blocked_attempts": metrics.blocked_attempts,
        "readiness_checks": metrics.readiness_checks,
        "recommendation_checks": metrics.recommendation_checks,
        "recommendation_followed": metrics.recommendation_followed,
        "recommendation_ignored": metrics.recommendation_ignored,
        "indeterminate_destination_warnings": metrics.indeterminate_destination_warnings,
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
    }


def main() -> None:
    args = parse_args()
    result = run_player(args.player_id, args.archetype, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
