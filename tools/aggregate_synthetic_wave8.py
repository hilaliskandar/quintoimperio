#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('--input-dir',type=Path,required=True); p.add_argument('--csv',type=Path,required=True); p.add_argument('--summary',type=Path,required=True); a=p.parse_args(); rows=[json.loads(x.read_text(encoding='utf-8')) for x in sorted(a.input_dir.rglob('*.json'))]
 if not rows: raise SystemExit('Nenhum resultado da onda 8 encontrado')
 a.csv.parent.mkdir(parents=True,exist_ok=True); a.summary.parent.mkdir(parents=True,exist_ok=True)
 fields=['reserve_request_days','player_id','profile','seed','completed','actions_attempted','blocked_attempts','readiness_checks','voyage_actions','waits','reprovision_actions','reprovision_total','reserve_actions','reserve_days_added','reserve_failed','reserve_skipped','elapsed_days','final_date','final_location','chronology_mode','counterfactual','min_provisions','min_condition','capital_final']
 with a.csv.open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(sorted(rows,key=lambda r:(r['reserve_request_days'],r['player_id'])))
 groups=defaultdict(list)
 for r in rows: groups[r['reserve_request_days']].append(r)
 out={'wave':8,'predeparture_days':2,'n_sessions':len(rows),'scenarios':{}}
 for reserve,items in sorted(groups.items()):
  b=Counter(); loc=Counter(); profiles=defaultdict(list)
  for r in items: b.update(r.get('blockers',{})); loc[r['final_location']]+=1; profiles[r['profile']].append(r)
  out['scenarios'][str(reserve)]={'n':len(items),'completed':sum(r['completed'] for r in items),'completion_rate':sum(r['completed'] for r in items)/len(items),'counterfactual':sum(r['counterfactual'] for r in items),'counterfactual_rate':sum(r['counterfactual'] for r in items)/len(items),'median_actions':statistics.median(r['actions_attempted'] for r in items),'median_blocks':statistics.median(r['blocked_attempts'] for r in items),'reserve_actions':sum(r['reserve_actions'] for r in items),'reserve_days_added':round(sum(r['reserve_days_added'] for r in items),2),'min_provisions':min(r['min_provisions'] for r in items),'top_blockers':b.most_common(),'final_locations':dict(loc.most_common()),'profiles':{p:{'n':len(v),'completed':sum(x['completed'] for x in v),'counterfactual':sum(x['counterfactual'] for x in v)} for p,v in sorted(profiles.items())}}
 a.summary.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
