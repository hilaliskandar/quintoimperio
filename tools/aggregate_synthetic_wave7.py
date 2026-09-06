#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input-dir',type=Path,required=True); p.add_argument('--csv',type=Path,required=True); p.add_argument('--summary',type=Path,required=True); a=p.parse_args()
    rows=[json.loads(x.read_text(encoding='utf-8')) for x in sorted(a.input_dir.rglob('*.json'))]
    if not rows: raise SystemExit('Nenhum resultado da onda 7 encontrado')
    a.csv.parent.mkdir(parents=True,exist_ok=True); a.summary.parent.mkdir(parents=True,exist_ok=True)
    fields=['predeparture_days','reserve_request_days','player_id','profile','seed','start_date','completed','actions_attempted','blocked_attempts','readiness_checks','voyage_actions','waits','reprovision_actions','reprovision_total','reserve_actions','reserve_days_added','reserve_failed','reserve_skipped','elapsed_days','final_date','final_location','chronology_mode','counterfactual','min_provisions','min_condition','capital_final']
    with a.csv.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(sorted(rows,key=lambda r:(r['predeparture_days'],r['player_id'])))
    groups=defaultdict(list)
    for r in rows: groups[r['predeparture_days']].append(r)
    summary={'wave':7,'n_sessions':len(rows),'reserve_request_days':rows[0]['reserve_request_days'],'scenarios':{}}
    for window,items in sorted(groups.items()):
        blockers=Counter(); locations=Counter(); profiles=defaultdict(list)
        for r in items:
            blockers.update(r.get('blockers',{})); locations[r['final_location']]+=1; profiles[r['profile']].append(r)
        summary['scenarios'][str(window)]={
            'n':len(items),'completed':sum(r['completed'] for r in items),'completion_rate':sum(r['completed'] for r in items)/len(items),
            'counterfactual':sum(r['counterfactual'] for r in items),'counterfactual_rate':sum(r['counterfactual'] for r in items)/len(items),
            'median_actions':statistics.median(r['actions_attempted'] for r in items),'median_blocks':statistics.median(r['blocked_attempts'] for r in items),
            'reserve_actions':sum(r['reserve_actions'] for r in items),'reserve_days_added':round(sum(r['reserve_days_added'] for r in items),2),
            'top_blockers':blockers.most_common(),'final_locations':dict(locations.most_common()),
            'profiles':{p:{'n':len(v),'completed':sum(x['completed'] for x in v),'counterfactual':sum(x['counterfactual'] for x in v)} for p,v in sorted(profiles.items())}
        }
    a.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
