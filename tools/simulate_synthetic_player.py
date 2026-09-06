#!/usr/bin/env python3
"""Executa uma sessão sintética independente do MVP e grava métricas em JSON.

Não representa um usuário humano. O perfil controla apenas heurísticas de decisão
sobre ações públicas do domínio; nenhuma regra da campanha é contornada.

Onda 1: descoberta não assistida, sem inspeção explícita de viabilidade antes da espera.
Onda 2: o jogador consulta a próxima perna antes de esperar e prepara recursos quando
os próprios bloqueios públicos do domínio indicam necessidade.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel


PROFILES = {"DISCIPLINED", "CAUTIOUS", "IMPATIENT", "FRUGAL", "TRADER"}
RESOURCE_BLOCKERS = {
    "INSUFFICIENT_PROVISIONS",
    "INSUFFICIENT_PROVISION_DAYS",
    "INSUFFICIENT_CONDITION",
}


@dataclass
class Metrics:
    player_id: int
    profile: str
    seed: int
    wave: int
    actions_attempted: int = 0
    actions_executed: int = 0
    blocked_attempts: int = 0
    readiness_checks: int = 0
    reprovision_actions: int = 0
    reprovision_total: float = 0.0
    access_negotiations: int = 0
    trade_actions: int = 0
    waits: int = 0
    voyage_actions: int = 0
    first_block_action: int | None = None
    recovered_after_block: bool = False
    min_provisions: float = 10**9
    min_condition: float = 10**9
    blockers: dict[str, int] = field(default_factory=dict)

    def observe(self, state) -> None:
        self.min_provisions = min(self.min_provisions, float(state.vessel.provision_days))
        self.min_condition = min(self.min_condition, float(state.vessel.condition))

    def attempt(self) -> None:
        self.actions_attempted += 1

    def executed(self) -> None:
        self.actions_executed += 1
        if self.first_block_action is not None:
            self.recovered_after_block = True

    def blocked(self, reasons) -> None:
        self.blocked_attempts += 1
        if self.first_block_action is None:
            self.first_block_action = self.actions_attempted
        for reason in reasons:
            self.blockers[reason] = self.blockers.get(reason, 0) + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", type=int, required=True)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--wave", type=int, choices=(1, 2), default=1)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def reprovision(model, state, metrics: Metrics, amount: float = 30.0):
    metrics.attempt()
    result = model.reprovision(state, amount)
    if result.executed:
        metrics.executed()
        metrics.reprovision_actions += 1
        metrics.reprovision_total += result.service_result.effect
        state = result.state_after
    else:
        metrics.blocked(result.reasons)
    metrics.observe(state)
    return state, result.executed


def wait_guided(model, state, metrics: Metrics):
    metrics.attempt()
    result = model.wait_for_guided_departure(state)
    if result.executed:
        metrics.executed()
        metrics.waits += 1
        state = result.state_after
    else:
        metrics.blocked(result.reasons)
    metrics.observe(state)
    return state, result.executed


def plan_and_execute(model, state, metrics: Metrics, seed: int):
    """Tenta a perna atual e recupera bloqueios usando apenas ações públicas."""
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


def proactive_policy(model, state, metrics: Metrics, profile: str):
    """Aplica apenas decisões plausíveis antes da próxima perna."""
    if profile == "CAUTIOUS":
        while state.vessel.provision_days < 85:
            state, changed = reprovision(model, state, metrics)
            if not changed:
                break
    elif profile in {"DISCIPLINED", "TRADER"}:
        if state.vessel.provision_days < 45:
            state, _ = reprovision(model, state, metrics)
    return state


def prepare_before_wait(model, state, metrics: Metrics, seed: int):
    """Onda 2: consulta viabilidade antes de consumir a janela histórica de espera.

    A inspeção usa exatamente ``plan_current_leg``. Se os bloqueios publicados
    indicarem falta de provisões, tenta reabastecer ainda antes da espera. Nenhuma
    necessidade é inferida por conhecimento interno do simulador.
    """
    for _ in range(8):
        metrics.attempt()
        metrics.readiness_checks += 1
        plan = model.plan_current_leg(state, seed=seed)
        metrics.executed()
        resource_reasons = tuple(
            reason
            for reason in plan.blockers
            if reason in RESOURCE_BLOCKERS or "PROVISION" in reason
        )
        if not resource_reasons:
            return state
        state, changed = reprovision(model, state, metrics)
        if not changed:
            return state
    return state


def run_player(player_id: int, profile: str, seed: int, wave: int) -> dict:
    model = HistoricalCampaignModel()
    progress_model = CampaignProgressModel(model.session)
    state = model.initial_state(active_expedition_id="EXP_GAMA_1497")
    metrics = Metrics(player_id=player_id, profile=profile, seed=seed, wave=wave)
    metrics.observe(state)
    start_date = state.vessel.clock.current_date

    while model.current_leg(state) is not None:
        state = proactive_policy(model, state, metrics, profile)

        departure = model.guided_departure_date(state)
        if wave == 2 and departure is not None and state.vessel.clock.current_date < departure:
            state = prepare_before_wait(model, state, metrics, seed)

        if (
            profile != "IMPATIENT"
            and departure is not None
            and state.vessel.clock.current_date < departure
        ):
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

        requested_qty = 4.0 if profile == "TRADER" else 1.0
        qty = requested_qty
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
        "wave": wave,
        "player_id": player_id,
        "profile": profile,
        "seed": seed,
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
    }


def main() -> None:
    args = parse_args()
    result = run_player(args.player_id, args.profile, args.seed, args.wave)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
