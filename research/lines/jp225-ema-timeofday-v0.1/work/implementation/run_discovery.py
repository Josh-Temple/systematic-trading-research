"""One-shot Packet C runner. Qualified XM inputs and a pinned independent gate required."""
import argparse,csv,hashlib,json,sys
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean,median
from zoneinfo import ZoneInfo
from jp225_ema_screen import (Quote,map_executable_outcome,time_flags,cluster_bootstrap_mean,
                             select_discovery_candidate)
from overlap_diagnostics import overlap_diagnostics
SQ=Path(__file__).parents[1]/'source-qualification'
sys.path.insert(0,str(SQ))
from stage1_contract import digest,canonical,HOLDOUT_START
from stage2 import read_frozen_manifest,SPEC
from validate_stage2 import validate_stage2

FLAGS=('ALL','TOKYO_OPEN_30','TOKYO_CLOSE_30','OSE_NIGHT_OPEN_30','US_CASH_OPEN_60','OTHER')

def code_identity():
    paths=[Path(__file__),Path(__file__).with_name('jp225_ema_screen.py'),
           Path(__file__).with_name('overlap_diagnostics.py'),SQ/'stage2.py',SQ/'validate_stage1.py',
           SQ/'validate_stage2.py',SQ/'stage1_contract.py']
    return hashlib.sha256(canonical({p.name:digest(p) for p in paths})).hexdigest()

def run(stage1,stage2,manifest,manifest_sha,gate_path,gate_sha,out):
    # Never infer permission from the existence of raw data.
    if digest(gate_path)!=gate_sha:raise PermissionError('GATE_IDENTITY_FAILURE')
    gate=json.loads(Path(gate_path).read_text())
    q=validate_stage2(stage1,stage2,manifest,manifest_sha)
    if q['status']!='PASS':raise PermissionError('PACKET_A_NOT_PASS')
    identity={'spec_sha256':digest(SPEC),'code_sha256':code_identity(),
              'event_manifest_sha256':manifest_sha,'stage1_sha256':q['stage1_sha256'],
              'stage2_sha256':q['stage2_sha256']}
    if (gate.get('status')!='PASS' or gate.get('independent_review')!='PASS' or
        gate.get('packet_a')!='PASS' or gate.get('sample')!='2025_DISCOVERY' or
        gate.get('binding')!=identity):raise PermissionError('DISCOVERY_GATE_CLOSED')
    m=read_frozen_manifest(manifest,manifest_sha)
    if m['code_sha256']!=digest(Path(__file__).with_name('jp225_ema_screen.py')):
        raise PermissionError('SIGNAL_CODE_CHANGED')
    if m['spec_sha256']!=digest(SPEC):raise PermissionError('SPEC_CHANGED')
    # Exclusive directory creation is the durable one-shot consumption marker.
    # A failed run cannot reuse this run ID without an explicit failure/recovery decision.
    out=Path(out)
    if out.exists(): raise PermissionError('RUN_OUTPUT_ALREADY_EXISTS')
    marker=Path(stage1)/'DISCOVERY_CONSUMED.json'
    with marker.open('xb') as f:
        f.write(canonical({'status':'STARTED_SAMPLE_CONSUMPTION','gate_sha256':gate_sha,'binding':identity}))
    out.mkdir(parents=True,exist_ok=False)
    (out/'RUN_STARTED.json').write_bytes(canonical({'status':'STARTED_SAMPLE_CONSUMPTION',
      'gate_sha256':gate_sha,'binding':identity,'sample':'2025_DISCOVERY'}))
    quotes=defaultdict(list)
    try:
        with (Path(stage2)/'event_ticks_raw.csv').open(newline='') as f:
            for row in csv.DictReader(f):
                ms=int(row['time_msc'])
                if ms>=HOLDOUT_START*1000:raise PermissionError('BOUNDARY_VIOLATION')
                quotes[int(row['request_id'])].append(Quote(datetime.fromtimestamp(ms/1000,timezone.utc),float(row['bid']),float(row['ask'])))
        requests={(r['start'],r['end']):i for i,r in enumerate(m['requests'])}
        ledger=[];grouped=defaultdict(list);missing=defaultdict(int);signals=defaultdict(list)
        for e in m['events']:
            t=e['signal_close'];dt=datetime.fromtimestamp(t,timezone.utc);flags=time_flags(dt)
            entry=e['windows'][0]
            eq=quotes[requests[(entry['start'],entry['end'])]] if entry['status']=='REQUESTED' else []
            for horizon,w in zip((5,15,30),e['windows'][1:]):
                tq=quotes[requests[(w['start'],w['end'])]] if w['status']=='REQUESTED' else []
                r=map_executable_outcome(eq+tq,dt,e['direction'],horizon)
                item={'event_id':e['event_id'],'kind':e['kind'],'signal_close':t,'direction':e['direction'],
                      'horizon':horizon,'flags':sorted(flags),'status':r.status,'net_points':r.net_points}
                if r.status=='OK':
                    entryq=next(q for q in eq if q.timestamp==r.entry_timestamp)
                    exitq=next(q for q in tq if q.timestamp==r.exit_timestamp)
                    mid_entry=(entryq.bid+entryq.ask)/2;mid_exit=(exitq.bid+exitq.ask)/2
                    item.update(gross_mid_points=e['direction']*(mid_exit-mid_entry),
                        entry_spread=r.entry_spread,exit_spread=r.exit_spread,
                        net_bps=r.net_points/mid_entry*10000,date=dt.astimezone(ZoneInfo('Asia/Tokyo')).date().isoformat())
                ledger.append(item)
                for flag in flags:
                    k=(e['kind'],flag,horizon)
                    if r.status=='OK':grouped[k].append(item)
                    else:missing[k]+=1
                    if horizon==15:signals[k].append(dt)
        metrics={};candidate_metrics={}
        for kind in ('ema','price_comparator'):
            for flag in FLAGS:
                for horizon in (5,15,30):
                    k=(kind,flag,horizon);items=grouped[k];vs=[x['net_points'] for x in items]
                    dates=defaultdict(list)
                    for x in items:dates[x['date']].append(x['net_points'])
                    ci=cluster_bootstrap_mean(dates) if dates and horizon==15 else (None,None)
                    r={'event_count':len(vs),'distinct_dates':len(dates),'missing_count':missing[k],
                       'mean_net_points':mean(vs) if vs else None,'median_net_points':median(vs) if vs else None,
                       'win_rate':sum(v>0 for v in vs)/len(vs) if vs else None,'ci_lower':ci[0],'ci_upper':ci[1],
                       'break_even_additional_round_trip_points':mean(vs) if vs and mean(vs)>0 else None}
                    if horizon==15:r['overlap_count_share']=overlap_diagnostics(signals[k])
                    metrics[f'{kind}:{flag}:{horizon}']=r
                    if kind=='ema' and horizon==15 and flag in FLAGS[:3] and vs:candidate_metrics[flag]=r
        winner=select_discovery_candidate(candidate_metrics)
        # Detect changed source/gate/code before publishing a terminal result.
        if validate_stage2(stage1,stage2,manifest,manifest_sha)!=q or code_identity()!=identity['code_sha256'] or digest(gate_path)!=gate_sha:
            raise PermissionError('INPUT_CHANGED_DURING_RUN')
        (out/'EVENT_OUTCOMES.json').write_bytes(canonical(ledger))
        result={'status':'COMPLETE','sample':'2025_DISCOVERY','metrics':metrics,'candidate_metrics':candidate_metrics,
                'decision':'ADVANCE_TO_HOLDOUT' if winner else 'NO_ADVANCEMENT','candidate':winner,
                'binding':identity,'gate_sha256':gate_sha}
        (out/'RESULT.json').write_bytes(canonical(result))
        source_sha=hashlib.sha256(canonical({'stage1':q['stage1_sha256'],'stage2':q['stage2_sha256']})).hexdigest()
        decision={'discovery_advancement':winner is not None,'sample':'2025_DISCOVERY','candidate':winner,
                  'packet_a':'PASS','independent_audit':'PASS','metrics':candidate_metrics,
                  'binding':{'spec_sha256':identity['spec_sha256'],'code_sha256':identity['code_sha256'],
                             'source_sha256':source_sha,'result_sha256':digest(out/'RESULT.json')}}
        (out/'DISCOVERY_DECISION.json').write_bytes(canonical(decision))
        (out/'sha256_manifest.json').write_bytes(canonical({p.name:digest(p) for p in out.iterdir() if p.is_file()}))
    except Exception:
        (out/'RUN_FAILED.json').write_bytes(canonical({'status':'FAILED_SAMPLE_CONSUMPTION_RESERVED','requires_recovery_decision':True}))
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('stage1','stage2','manifest','manifest_sha','gate','gate_sha','out'):ap.add_argument(name)
    a=ap.parse_args()
    try:run(a.stage1,a.stage2,a.manifest,a.manifest_sha,a.gate,a.gate_sha,a.out)
    except Exception:raise SystemExit('DISCOVERY_BLOCKED_OR_FAILED; preserve run marker; do not retry without review') from None
