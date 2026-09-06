#!/usr/bin/env python3
"""Playtest sintético por arquétipos inspirados em gêneros/estilos de jogo."""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel
from simulate_synthetic_player import Metrics, RESOURCE_BLOCKERS, reprovision, wait_guided

@dataclass(frozen=True)
class ArchetypePolicy:
    label: str; game_style: str; description: str
    consult_logistics: bool; follow_recommended_margin: bool; extra_margin_days: float
    wait_before_departure: bool; proactive_floor_days: float; max_recovery_steps: int
    recover_resources_after_block: bool; contact_authority: bool; trade_quantity: float

ARCHETYPES = {
"GRAND_STRATEGIST": ArchetypePolicy("Grande estrategista","grand strategy / 4X","Planeja horizonte completo e reduz risco sistêmico.",True,True,0,True,45,12,True,True,2),
"SURVIVALIST": ArchetypePolicy("Sobrevivencialista","survival / expedition management","Mantém redundância logística acima da recomendação.",True,True,20,True,85,12,True,True,1),
"MERCHANT": ArchetypePolicy("Mercador","trading / tycoon","Garante viagem e prioriza operação comercial final.",True,True,0,True,45,10,True,True,4),
"SPEEDRUNNER": ArchetypePolicy("Speedrunner","speedrun / action optimization","Avança imediatamente e corrige apenas bloqueios duros.",False,False,0,False,0,8,True,False,1),
"ROGUELIKE": ArchetypePolicy("Roguelike","roguelike / permadeath","Aceita risco e abandona após falha logística que exija recuperação.",True,False,0,True,0,0,False,True,1),
"ROLEPLAYER": ArchetypePolicy("Interpretativo histórico","historical RPG / roleplay","Segue cronologia, avisos e contatos documentados.",True,True,0,True,45,10,True,True,1),
"EXPLORER": ArchetypePolicy("Explorador","exploration / adventure","Consulta avisos, mas evita superotimização de reservas.",True,False,0,True,45,10,True,True,1),
"OPTIMIZER": ArchetypePolicy("Otimizador","puzzle / systems optimization","Busca o menor preparo suficiente indicado pelo sistema.",True,True,0,True,0,12,True,False,1),
"COMPLETIONIST": ArchetypePolicy("Completista","completionist / achievement hunting","Procura conclusão com ampla segurança e contato social.",True,True,10,True,70,12,True,True,2),
"CASUAL": ArchetypePolicy("Casual guiado","casual / tutorial-led","Segue orientação básica e reage a problemas visíveis.",True,True,0,True,30,4,True,False,1),
}

def parse_args():
    p=argparse.ArgumentParser(); p.add_argument('--player-id',type=int,required=True); p.add_argument('--archetype',choices=sorted(ARCHETYPES),required=True); p.add_argument('--seed',type=int,required=True); p.add_argument('--output',type=Path,required=True); return p.parse_args()

def proactive_floor(model,state,metrics,floor):
    while floor>0 and state.vessel.provision_days<floor:
        state,changed=reprovision(model,state,metrics)
        if not changed: break
    return state

def apply_planning(model,state,metrics,policy,seed):
    if not policy.consult_logistics: return state
    for _ in range(8):
        metrics.attempt(); metrics.recommendation_checks+=1; view=model.logistics_planning_view(state,seed=seed); metrics.executed()
        if view.next_destination_provisions_evidence_indeterminate: metrics.indeterminate_destination_warnings+=1
        horizon=view.logistics_horizon_required_days
        if horizon is None: return state
        target=horizon+view.recommended_margin_days+policy.extra_margin_days
        if state.vessel.provision_days>=target: return state
        if not policy.follow_recommended_margin: metrics.recommendation_ignored+=1; return state
        state,changed=reprovision(model,state,metrics)
        if not changed: metrics.recommendation_ignored+=1; return state
        metrics.recommendation_followed+=1
    return state

def plan_execute(model,state,metrics,policy,seed):
    recovery=0
    while True:
        metrics.attempt(); plan=model.plan_current_leg(state,seed=seed)
        if plan.feasible:
            metrics.executed(); metrics.attempt(); state=model.execute_voyage(state,plan); metrics.executed(); metrics.voyage_actions+=1; metrics.observe(state); return state,True
        metrics.blocked(plan.blockers)
        if recovery>=policy.max_recovery_steps: return state,False
        if 'HISTORICAL_DEPARTURE_NOT_REACHED' in plan.blockers:
            state,changed=wait_guided(model,state,metrics); recovery+=1
            if changed: continue
        resource_block=any(r in RESOURCE_BLOCKERS or 'PROVISION' in r for r in plan.blockers)
        if resource_block and policy.recover_resources_after_block:
            state,changed=reprovision(model,state,metrics); recovery+=1
            if changed: continue
        return state,False

def run_player(player_id,archetype,seed):
    policy=ARCHETYPES[archetype]; model=HistoricalCampaignModel(); progress_model=CampaignProgressModel(model.session); state=model.initial_playable_state(); metrics=Metrics(player_id=player_id,profile=archetype,seed=seed,wave=12); metrics.observe(state); start=state.vessel.clock.current_date
    while model.current_leg(state) is not None:
        state=proactive_floor(model,state,metrics,policy.proactive_floor_days); state=apply_planning(model,state,metrics,policy,seed)
        departure=model.guided_departure_date(state)
        if policy.wait_before_departure and departure is not None and state.vessel.clock.current_date<departure: state,_=wait_guided(model,state,metrics)
        state,ok=plan_execute(model,state,metrics,policy,seed)
        if not ok: break
        if policy.contact_authority and state.vessel.location_node=='MAL' and model.current_leg(state) is not None:
            metrics.attempt(); contacted=model.contact_authority(state)
            if contacted.executed: metrics.executed(); state=contacted.state_after
            else: metrics.blocked(contacted.reasons)
            metrics.observe(state)
    if state.vessel.location_node=='CAL':
        metrics.attempt(); access=model.negotiate_access(state)
        if access.executed: metrics.executed(); metrics.access_negotiations+=1; state=access.state_after
        else: metrics.blocked(access.reasons)
        qty=policy.trade_quantity
        while qty>=1:
            metrics.attempt(); bought=model.buy(state,'PEPPER',qty,seed=seed)
            if bought.executed: metrics.executed(); metrics.trade_actions+=1; state=bought.state_after; break
            metrics.blocked(bought.reasons); qty-=1
    progress=progress_model.progress(state); summary=progress_model.summary(state); events=state.voyage_event_history
    return {'wave':12,'player_id':player_id,'archetype':archetype,'archetype_label':policy.label,'game_style':policy.game_style,'seed':seed,'completed':progress.completed,'actions_attempted':metrics.actions_attempted,'actions_executed':metrics.actions_executed,'blocked_attempts':metrics.blocked_attempts,'recommendation_checks':metrics.recommendation_checks,'recommendation_followed':metrics.recommendation_followed,'recommendation_ignored':metrics.recommendation_ignored,'indeterminate_destination_warnings':metrics.indeterminate_destination_warnings,'blockers':dict(sorted(metrics.blockers.items())),'voyage_actions':metrics.voyage_actions,'waits':metrics.waits,'reprovision_actions':metrics.reprovision_actions,'reprovision_total':round(metrics.reprovision_total,2),'elapsed_days':(state.vessel.clock.current_date-start).days,'final_date':state.vessel.clock.current_date.isoformat(),'final_location':state.vessel.location_node,'chronology_mode':state.chronology_mode.value,'counterfactual':state.chronology_mode is ChronologyMode.COUNTERFACTUAL,'min_provisions':round(metrics.min_provisions,2),'min_condition':round(metrics.min_condition,2),'voyage_events':len(events),'positive_provision_events':sum(e.provision_delta>0 for e in events),'negative_provision_events':sum(e.provision_delta<0 for e in events),'timing_events':sum(e.extra_days>0 for e in events),'net_event_provision_delta':round(sum(e.provision_delta for e in events),2),'capital_final':round(summary.capital_index,4)}

def main():
    a=parse_args(); r=run_player(a.player_id,a.archetype,a.seed); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(r,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
