#!/usr/bin/env python3
"""Onda 8: sensibilidade da reserva logística com janela pré-partida fixa de 2 dias."""
from __future__ import annotations
import argparse, json
from datetime import date, timedelta
from pathlib import Path
from quintoimperio.domain import CampaignProgressModel, ChronologyMode, HistoricalCampaignModel, PortServiceKind
from simulate_synthetic_player import Metrics, PROFILES, RESOURCE_BLOCKERS, proactive_policy, reprovision, wait_guided
HISTORICAL_DEPARTURE=date(1497,7,8); PREDEPARTURE_DAYS=2

def parse_args():
 p=argparse.ArgumentParser(); p.add_argument('--player-id',type=int,required=True); p.add_argument('--profile',choices=sorted(PROFILES),required=True); p.add_argument('--seed',type=int,required=True); p.add_argument('--reserve-days',type=float,required=True); p.add_argument('--output',type=Path,required=True); return p.parse_args()

def prepare(model,state,m,seed,reserve,c):
 for _ in range(8):
  m.attempt(); m.readiness_checks+=1; plan=model.plan_current_leg(state,seed=seed); m.executed(); blockers=[r for r in plan.blockers if r in RESOURCE_BLOCKERS or 'PROVISION' in r]
  if not blockers: break
  state,changed=reprovision(model,state,m)
  if not changed: return state
 view=model.service_view(state,PortServiceKind.PROVISIONS)
 if view.historical_documented and view.actionable and reserve>0:
  before=float(state.vessel.provision_days); state,changed=reprovision(model,state,m,reserve)
  if changed: c['reserve_actions']+=1; c['reserve_days_added']+=max(0.0,float(state.vessel.provision_days)-before)
  else: c['reserve_failed']+=1
 else: c['reserve_skipped']+=1
 return state

def travel(model,state,m,seed):
 for _ in range(12):
  m.attempt(); plan=model.plan_current_leg(state,seed=seed)
  if plan.feasible:
   m.executed(); m.attempt(); state=model.execute_voyage(state,plan); m.executed(); m.voyage_actions+=1; m.observe(state); return state,True
  m.blocked(plan.blockers)
  if 'HISTORICAL_DEPARTURE_NOT_REACHED' in plan.blockers:
   state,changed=wait_guided(model,state,m)
   if changed: continue
  if any(r in RESOURCE_BLOCKERS or 'PROVISION' in r for r in plan.blockers):
   state,changed=reprovision(model,state,m)
   if changed: continue
  return state,False
 return state,False

def run(pid,profile,seed,reserve):
 model=HistoricalCampaignModel(); pm=CampaignProgressModel(model.session); start=HISTORICAL_DEPARTURE-timedelta(days=PREDEPARTURE_DAYS); state=model.initial_state(active_expedition_id='EXP_GAMA_1497',start_date=start); m=Metrics(pid,profile,seed,8); c={'reserve_actions':0,'reserve_days_added':0.0,'reserve_failed':0,'reserve_skipped':0}; m.observe(state)
 while model.current_leg(state) is not None:
  state=proactive_policy(model,state,m,profile); state=prepare(model,state,m,seed,reserve,c); dep=model.guided_departure_date(state)
  if profile!='IMPATIENT' and dep is not None and state.vessel.clock.current_date<dep: state,_=wait_guided(model,state,m)
  state,ok=travel(model,state,m,seed)
  if not ok: break
  if state.vessel.location_node=='MAL' and model.current_leg(state) is not None:
   m.attempt(); r=model.contact_authority(state)
   if r.executed: m.executed(); state=r.state_after
   else: m.blocked(r.reasons)
   m.observe(state)
 if state.vessel.location_node=='CAL':
  m.attempt(); r=model.negotiate_access(state)
  if r.executed: m.executed(); m.access_negotiations+=1; state=r.state_after
  else: m.blocked(r.reasons)
  qty=4.0 if profile=='TRADER' else 1.0
  while qty>=1:
   m.attempt(); b=model.buy(state,'PEPPER',qty,seed=seed)
   if b.executed: m.executed(); m.trade_actions+=1; state=b.state_after; break
   m.blocked(b.reasons); qty-=1
  m.observe(state)
 p=pm.progress(state); s=pm.summary(state)
 return {'wave':8,'predeparture_days':PREDEPARTURE_DAYS,'reserve_request_days':reserve,'player_id':pid,'profile':profile,'seed':seed,'completed':p.completed,'actions_attempted':m.actions_attempted,'blocked_attempts':m.blocked_attempts,'readiness_checks':m.readiness_checks,'blockers':dict(sorted(m.blockers.items())),'voyage_actions':m.voyage_actions,'waits':m.waits,'reprovision_actions':m.reprovision_actions,'reprovision_total':round(m.reprovision_total,2),'elapsed_days':(state.vessel.clock.current_date-start).days,'final_date':state.vessel.clock.current_date.isoformat(),'final_location':state.vessel.location_node,'chronology_mode':state.chronology_mode.value,'counterfactual':state.chronology_mode is ChronologyMode.COUNTERFACTUAL,'min_provisions':round(m.min_provisions,2),'min_condition':round(m.min_condition,2),'capital_final':round(s.capital_index,4),**{k:round(v,2) if isinstance(v,float) else v for k,v in c.items()}}

def main():
 a=parse_args(); out=run(a.player_id,a.profile,a.seed,a.reserve_days); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
