"""Signal-only manifest and event-adjacent raw tick acquisition. No returns."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
from datetime import datetime, timezone
from stage1_contract import (SYMBOL, START, HOLDOUT_START, TICK_FIELDS, SYMBOL_FIELDS,
                            canonical, digest, allowlist, boundary_check)
from validate_stage1 import validate

IMPL=Path(__file__).parents[1]/'implementation'/'jp225_ema_screen.py'
SPEC=Path(__file__).parents[2]/'specifications'/'SPEC-JP225-EMA-001-v01.md'

def freeze_manifest(folder, output):
    result=validate(folder)
    if result['status']!='PASS': raise PermissionError('STAGE1_NOT_PASS')
    freeze=json.loads((Path(__file__).parents[1]/'integration'/'SPEC_FREEZE.json').read_text())
    if digest(SPEC)!=freeze['sha256']: raise PermissionError('SPEC_IDENTITY_CHANGED')
    # Only now may we read signal prices. Loader rejects holdout before EMA calculation.
    bars=[]
    with (Path(folder)/'m1_warmup_2025_raw.csv').open(newline='') as f:
        for r in csv.DictReader(f):
            t=int(r['time'])
            if not START<=t<HOLDOUT_START: raise PermissionError('BOUNDARY_VIOLATION')
            bars.append((t,float(r['close'])))
    import sys
    sys.path.insert(0,str(IMPL.parent))
    from jp225_ema_screen import recursive_ema, crossover_directions, price_slow_crossover_directions
    prices=[p for _,p in bars]; slow=recursive_ema(prices,200)
    signals={'ema':crossover_directions(recursive_ema(prices,5),slow),
             'price_comparator':price_slow_crossover_directions(prices,slow)}
    events=[]; requests=set()
    for kind,dirs in signals.items():
        for i,d in enumerate(dirs):
            t=bars[i][0]+60
            if not d or not 1735689600<=t<HOLDOUT_START: continue
            if i<1000: raise PermissionError('INSUFFICIENT_WARMUP')
            windows=[]
            for minutes in (0,5,15,30):
                a=t+minutes*60; b=a+60
                # Do not obtain ANY 2026 ticks even for 2025 boundary events.
                # Unavailable boundary windows remain explicit, never silently dropped.
                if b>=HOLDOUT_START:
                    windows.append({'horizon_minutes':minutes,'status':'BOUNDARY_UNAVAILABLE'})
                else:
                    windows.append({'horizon_minutes':minutes,'start':a,'end':b,'status':'REQUESTED'})
                    requests.add((a,b))
            events.append({'event_id':f'{kind}:{t}:{d}','kind':kind,'signal_close':t,
                           'direction':d,'windows':windows})
    payload={'version':'JP225_STAGE2_v1','symbol':SYMBOL,'stage1':result['raw_sha256'],
      'spec_sha256':digest(SPEC),'code_sha256':digest(IMPL),'source_review_sha256':
      digest(Path(folder)/'source_review.json'),'events':events,
      'requests':[{'start':a,'end':b} for a,b in sorted(requests)],
      'strategy_outcomes_calculated':False,'holdout_requested':False}
    out=Path(output)
    out.mkdir(exist_ok=False,parents=True)
    (out/'event_manifest.json').write_bytes(canonical(payload))
    (out/'event_manifest.sha256').write_text(digest(out/'event_manifest.json')+'\n')
    # Persist and commit manifest identity before invoking collector. Do not print prices.
    return digest(out/'event_manifest.json')

def read_frozen_manifest(path, expected_sha):
    p=Path(path)
    if digest(p)!=expected_sha: raise PermissionError('MANIFEST_IDENTITY_CHANGED')
    m=json.loads(p.read_text())
    if (m.get('version')!='JP225_STAGE2_v1' or m.get('symbol')!=SYMBOL or
        m.get('strategy_outcomes_calculated') is not False or m.get('holdout_requested') is not False):
        raise PermissionError('MANIFEST_CONTRACT_FAILURE')
    expected=set(); ids=set()
    for e in m['events']:
        t=e['signal_close']
        if (type(t) is not int or not 1735689600<=t<HOLDOUT_START or
            e['direction'] not in (-1,1) or e['kind'] not in ('ema','price_comparator') or
            e['event_id']!=f"{e['kind']}:{t}:{e['direction']}" or e['event_id'] in ids):
            raise PermissionError('EVENT_CONTRACT_FAILURE')
        ids.add(e['event_id'])
        if len(e['windows'])!=4: raise PermissionError('WINDOW_CONTRACT_FAILURE')
        for minutes,w in zip((0,5,15,30),e['windows']):
            a=t+minutes*60; b=a+60
            want={'horizon_minutes':minutes,'status':'BOUNDARY_UNAVAILABLE'} if b>=HOLDOUT_START else {
                'horizon_minutes':minutes,'start':a,'end':b,'status':'REQUESTED'}
            if w!=want: raise PermissionError('WINDOW_CONTRACT_FAILURE')
            if b<HOLDOUT_START: expected.add((a,b))
    if m['requests']!=[{'start':a,'end':b} for a,b in sorted(expected)]:
        raise PermissionError('REQUEST_MANIFEST_MISMATCH')
    return m

def collect(path, expected_sha, output, api):
    m=read_frozen_manifest(path,expected_sha)  # BEFORE initialize/history API calls
    out=Path(output); out.mkdir(parents=True,exist_ok=False)
    if not api.initialize(): raise RuntimeError('MT5_INITIALIZE_FAILED')
    try:
        source_symbol=allowlist(api.symbol_info(SYMBOL),SYMBOL_FIELDS)
        if source_symbol['name']!=SYMBOL: raise PermissionError('EXACT_SYMBOL_FAILURE')
        server=allowlist(api.account_info(),('server',))
        # Same terminal/server/symbol must be independently checked against Stage 1 at qualification.
        summaries=[]
        with (out/'event_ticks_raw.csv').open('w',newline='') as f:
            w=csv.writer(f); w.writerow(['request_id',*TICK_FIELDS])
            for n,r in enumerate(m['requests']):
                ticks=api.copy_ticks_range(SYMBOL,datetime.fromtimestamp(r['start'],timezone.utc),
                      datetime.fromtimestamp(r['end'],timezone.utc),api.COPY_TICKS_ALL)
                if ticks is None: raise RuntimeError('TICK_ACQUISITION_FAILED')
                boundary_check(ticks,tick=True)
                if tuple(ticks.dtype.names or ())!=TICK_FIELDS: raise RuntimeError('TICK_SCHEMA_FAILURE')
                for row in ticks:
                    if not r['start']*1000<=int(row['time_msc'])<=r['end']*1000:
                        raise RuntimeError('REQUEST_BOUNDARY_VIOLATION')
                    w.writerow([n,*[row[k].item() if hasattr(row[k],'item') else row[k] for k in TICK_FIELDS]])
                summaries.append({'request_id':n,**r,'rows':len(ticks)})
        meta={'version':'JP225_STAGE2_v1','event_manifest_sha256':expected_sha,
              'symbol':source_symbol,'account':server,'requests':summaries,
              'strategy_outcomes_calculated':False,'holdout_requested':False,
              'source_qualification':'PARTIAL_WITH_GAPS'}
        (out/'metadata.json').write_bytes(canonical(meta))
        man={n:{'sha256':digest(out/n),'bytes':(out/n).stat().st_size} for n in ('metadata.json','event_ticks_raw.csv')}
        (out/'sha256_manifest.json').write_bytes(canonical(man))
    finally: api.shutdown()

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    f=sub.add_parser('freeze'); f.add_argument('stage1'); f.add_argument('out')
    c=sub.add_parser('collect'); c.add_argument('manifest'); c.add_argument('--expected-sha256',required=True); c.add_argument('out')
    a=ap.parse_args()
    try:
        if a.cmd=='freeze': print(freeze_manifest(a.stage1,a.out))
        else:
            # Validate BEFORE importing platform API and before connecting.
            read_frozen_manifest(a.manifest,a.expected_sha256)
            import MetaTrader5 as mt5
            collect(a.manifest,a.expected_sha256,a.out,mt5)
            print('STAGE2_RAW_COLLECTION_COMPLETE; qualification still required')
    except Exception:
        raise SystemExit('STAGE2_FAILED; preserve partial files locally; no outcome calculation authorized') from None
