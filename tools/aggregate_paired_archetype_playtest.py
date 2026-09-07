#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path

def med(v): return statistics.median(v) if v else None

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input-dir',type=Path,required=True); p.add_argument('--csv',type=Path,required=True); p.add_argument('--summary',type=Path,required=True); p.add_argument('--paired-csv',type=Path,required=True); a=p.parse_args()
    rows=[json.loads(x.read_text(encoding='utf-8')) for x in sorted(a.input_dir.rglob('*.json'))]
    by_arch=defaultdict(list); by_seed=defaultdict(list); blockers=Counter()
    for r in rows: by_arch[r['archetype']].append(r); by_seed[r['seed']].append(r); blockers.update(r.get('blockers',{}))
    if len(rows)!=200 or len(by_arch)!=10 or any(len(v)!=20 for v in by_arch.values()): raise SystemExit('Bateria incompleta por arquétipo')
    if len(by_seed)!=20 or any(len(v)!=10 for v in by_seed.values()): raise SystemExit('Pareamento incompleto por seed')
    fields=['wave','player_id','archetype','archetype_label','game_style','seed','completed','actions_attempted','actions_executed','blocked_attempts','recommendation_checks','recommendation_followed','recommendation_ignored','indeterminate_destination_warnings','voyage_actions','waits','reprovision_actions','reprovision_total','elapsed_days','final_date','final_location','chronology_mode','counterfactual','min_provisions','min_condition','voyage_events','positive_provision_events','negative_provision_events','timing_events','net_event_provision_delta','capital_final']
    a.csv.parent.mkdir(parents=True,exist_ok=True)
    with a.csv.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(sorted(rows,key=lambda r:(r['seed'],r['archetype'])))
    paired=[]
    for seed,it in sorted(by_seed.items()):
        completed=sorted(r['archetype'] for r in it if r['completed']); failed=sorted(r['archetype'] for r in it if not r['completed'])
        paired.append({'seed':seed,'completed_n':len(completed),'failed_n':len(failed),'completed_archetypes':'|'.join(completed),'failed_archetypes':'|'.join(failed),'min_provisions_median':med([r['min_provisions'] for r in it]),'min_condition_median':med([r['min_condition'] for r in it])})
    with a.paired_csv.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(paired[0])); w.writeheader(); w.writerows(paired)
    summary={'wave':15,'design':'paired-seed','seeds':sorted(by_seed),'n_sessions':len(rows),'completion_rate':sum(r['completed'] for r in rows)/len(rows),'completed':sum(r['completed'] for r in rows),'top_blockers':blockers.most_common(),'archetypes':{},'seeds_summary':paired}
    for n,it in sorted(by_arch.items()):
        ib=Counter(); [ib.update(r.get('blockers',{})) for r in it]
        summary['archetypes'][n]={'n':20,'completed':sum(r['completed'] for r in it),'completion_rate':sum(r['completed'] for r in it)/20,'median_blocked':med([r['blocked_attempts'] for r in it]),'median_min_provisions':med([r['min_provisions'] for r in it]),'median_min_condition':med([r['min_condition'] for r in it]),'top_blockers':ib.most_common()}
    a.summary.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
