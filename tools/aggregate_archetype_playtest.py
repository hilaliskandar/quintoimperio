#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path

def median(v): return statistics.median(v) if v else None
def mean(v): return statistics.mean(v) if v else None

def main():
 p=argparse.ArgumentParser(); p.add_argument('--input-dir',type=Path,required=True); p.add_argument('--csv',type=Path,required=True); p.add_argument('--summary',type=Path,required=True); a=p.parse_args()
 rows=[json.loads(x.read_text(encoding='utf-8')) for x in sorted(a.input_dir.rglob('*.json'))]
 if not rows: raise SystemExit('Nenhum resultado encontrado')
 by=defaultdict(list); blockers=Counter()
 for r in rows: by[r['archetype']].append(r); blockers.update(r.get('blockers',{}))
 if len(by)!=10 or any(len(v)!=20 for v in by.values()): raise SystemExit('Bateria incompleta')
 fields=['wave','player_id','archetype','archetype_label','game_style','seed','completed','actions_attempted','actions_executed','blocked_attempts','recommendation_checks','recommendation_followed','recommendation_ignored','indeterminate_destination_warnings','voyage_actions','waits','reprovision_actions','reprovision_total','elapsed_days','final_date','final_location','chronology_mode','counterfactual','min_provisions','min_condition','voyage_events','positive_provision_events','negative_provision_events','timing_events','net_event_provision_delta','capital_final']
 a.csv.parent.mkdir(parents=True,exist_ok=True)
 with a.csv.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(sorted(rows,key=lambda r:(r['archetype'],r['player_id'])))
 s={'wave':14,'n_archetypes':10,'sessions_per_archetype':20,'n_sessions':len(rows),'completed':sum(r['completed'] for r in rows),'completion_rate':sum(r['completed'] for r in rows)/len(rows),'counterfactual':sum(r['counterfactual'] for r in rows),'positive_provision_events':sum(r['positive_provision_events'] for r in rows),'negative_provision_events':sum(r['negative_provision_events'] for r in rows),'timing_events':sum(r['timing_events'] for r in rows),'top_blockers':blockers.most_common(),'archetypes':{}}
 for n,it in sorted(by.items()):
  ib=Counter(); [ib.update(r.get('blockers',{})) for r in it]
  s['archetypes'][n]={'label':it[0]['archetype_label'],'game_style':it[0]['game_style'],'n':20,'completed':sum(r['completed'] for r in it),'completion_rate':sum(r['completed'] for r in it)/20,'counterfactual':sum(r['counterfactual'] for r in it),'median_actions':median([r['actions_attempted'] for r in it]),'median_blocked':median([r['blocked_attempts'] for r in it]),'min_provisions':min(r['min_provisions'] for r in it),'min_condition':min(r['min_condition'] for r in it),'positive_provision_events':sum(r['positive_provision_events'] for r in it),'negative_provision_events':sum(r['negative_provision_events'] for r in it),'timing_events':sum(r['timing_events'] for r in it),'mean_net_event_provision_delta':mean([r['net_event_provision_delta'] for r in it]),'top_blockers':ib.most_common()}
 a.summary.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(s,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
