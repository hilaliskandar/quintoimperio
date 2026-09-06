#!/usr/bin/env python3
"""Onda 7: sensibilidade de uma janela de preparação antes da partida histórica.

A partida observada permanece em 1497-07-08. O experimento inicia o relógio N dias
antes apenas para permitir que ações logísticas, que consomem tempo, ocorram antes
da partida. A margem logística usada é 30 dias-equivalentes, pois a onda 5 mostrou
que essa política pode atravessar escalas com evidência de provisões indeterminada.
A janela N e a margem são parâmetros de simulação, não fatos históricos.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel, PortServiceKind
from simulate_synthetic_player import Metrics, PROFILES, RESOURCE_BLOCKERS, proactive_policy, reprovision, wait_guided

RESERVE_DAYS = 30.0
HISTORICAL_DEPARTURE = date(1497, 7, 8)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--player-id', type=int, required=True)
    p.add_argument('--profile', choices=sorted(PROFILES), required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--predeparture-days', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    return p.parse_args()


def prepare(model, state, metrics, seed, counters):
    """Torna a próxima perna viável e adiciona reserva se o porto sustenta serviço."""
    for _ in range(8):
        metrics.attempt(); metrics.readiness_checks += 1
        plan = model.plan_current_leg(state, seed=seed); metrics.executed()
        resource = [r for r in plan.blockers if r in RESOURCE_BLOCKERS or 'PROVISION' in r]
        if not resource:
            break
        state, changed = reprovision(model, state, metrics)
        if not changed:
            return state
    view = model.service_view(state, PortServiceKind.PROVISIONS)
    if view.historical_documented and view.actionable:
        before = float(state.vessel.provision_days)
        state, changed = reprovision(model, state, metrics, RESERVE_DAYS)
        if changed:
            counters['reserve_actions'] += 1
            counters['reserve_days_added'] += max(0.0, float(state.vessel.provision_days) - before)
        else:
            counters['reserve_failed'] += 1
    else:
        counters['reserve_skipped'] += 1
    return state


def travel(model, state, metrics, seed):
    for _ in range(12):
        metrics.attempt(); plan = model.plan_current_leg(state, seed=seed)
        if plan.feasible:
            metrics.executed(); metrics.attempt()
            state = model.execute_voyage(state, plan); metrics.executed(); metrics.voyage_actions += 1
            metrics.observe(state); return state, True
        metrics.blocked(plan.blockers)
        if 'HISTORICAL_DEPARTURE_NOT_REACHED' in plan.blockers:
            state, changed = wait_guided(model, state, metrics)
            if changed: continue
        if any(r in RESOURCE_BLOCKERS or 'PROVISION' in r for r in plan.blockers):
            state, changed = reprovision(model, state, metrics)
            if changed: continue
        return state, False
    return state, False


def run_player(pid, profile, seed, predeparture_days):
    model = HistoricalCampaignModel(); progress_model = CampaignProgressModel(model.session)
    start_date = HISTORICAL_DEPARTURE - timedelta(days=predeparture_days)
    state = model.initial_state(active_expedition_id='EXP_GAMA_1497', start_date=start_date)
    metrics = Metrics(pid, profile, seed, 7)
    counters = {'reserve_actions': 0, 'reserve_days_added': 0.0, 'reserve_failed': 0, 'reserve_skipped': 0}
    metrics.observe(state)

    while model.current_leg(state) is not None:
        state = proactive_policy(model, state, metrics, profile)
        state = prepare(model, state, metrics, seed, counters)
        dep = model.guided_departure_date(state)
        if profile != 'IMPATIENT' and dep is not None and state.vessel.clock.current_date < dep:
            state, _ = wait_guided(model, state, metrics)
        state, ok = travel(model, state, metrics, seed)
        if not ok: break
        if state.vessel.location_node == 'MAL' and model.current_leg(state) is not None:
            metrics.attempt(); contact = model.contact_authority(state)
            if contact.executed:
                metrics.executed(); state = contact.state_after
            else:
                metrics.blocked(contact.reasons)
            metrics.observe(state)

    if state.vessel.location_node == 'CAL':
        metrics.attempt(); access = model.negotiate_access(state)
        if access.executed:
            metrics.executed(); metrics.access_negotiations += 1; state = access.state_after
        else:
            metrics.blocked(access.reasons)
        qty = 4.0 if profile == 'TRADER' else 1.0
        while qty >= 1.0:
            metrics.attempt(); buy = model.buy(state, 'PEPPER', qty, seed=seed)
            if buy.executed:
                metrics.executed(); metrics.trade_actions += 1; state = buy.state_after; break
            metrics.blocked(buy.reasons); qty -= 1.0
        metrics.observe(state)

    progress = progress_model.progress(state); summary = progress_model.summary(state)
    return {
        'wave': 7, 'predeparture_days': predeparture_days, 'reserve_request_days': RESERVE_DAYS,
        'player_id': pid, 'profile': profile, 'seed': seed, 'start_date': start_date.isoformat(),
        'completed': progress.completed, 'current_objective': progress.current_objective,
        'actions_attempted': metrics.actions_attempted, 'actions_executed': metrics.actions_executed,
        'blocked_attempts': metrics.blocked_attempts, 'readiness_checks': metrics.readiness_checks,
        'blockers': dict(sorted(metrics.blockers.items())), 'voyage_actions': metrics.voyage_actions,
        'waits': metrics.waits, 'reprovision_actions': metrics.reprovision_actions,
        'reprovision_total': round(metrics.reprovision_total, 2), 'elapsed_days': (state.vessel.clock.current_date-start_date).days,
        'final_date': state.vessel.clock.current_date.isoformat(), 'final_location': state.vessel.location_node,
        'chronology_mode': state.chronology_mode.value, 'counterfactual': state.chronology_mode is ChronologyMode.COUNTERFACTUAL,
        'min_provisions': round(metrics.min_provisions, 2), 'min_condition': round(metrics.min_condition, 2),
        'capital_final': round(summary.capital_index, 4), **{k: round(v,2) if isinstance(v,float) else v for k,v in counters.items()}
    }


def main():
    a = parse_args(); result = run_player(a.player_id, a.profile, a.seed, a.predeparture_days)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))

if __name__ == '__main__': main()
