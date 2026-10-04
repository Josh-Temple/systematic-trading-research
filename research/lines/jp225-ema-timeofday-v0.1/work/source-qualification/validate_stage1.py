"""Raw Stage 1 validation. No signals, outcomes, plots, or market values in output."""
import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from stage1_contract import (START, END, DISCOVERY_START, HOLDOUT_START, SYMBOL,
    PROBES, M1_FIELDS, TICK_FIELDS, SYMBOL_FIELDS, utc, digest, canonical)

FILES = ('metadata.json','m1_warmup_2025_raw.csv','tick_probes_raw.csv')
META_KEYS = {'collector_version','collected_at_utc','strategy_outcomes_calculated',
 'holdout_2026_requested','request_time_convention','returned_timestamp_semantics',
 'mt5_version','package_version','collector_sha256','contract_sha256','terminal',
 'account','symbol','m1_request','tick_probes','bar_price_identity','source_review'}

class Invalid(Exception): pass

def need(ok, code):
    if not ok: raise Invalid(code)

def number(v):
    try: x=float(v)
    except (TypeError,ValueError): raise Invalid('NUMERIC_PARSE_FAILURE') from None
    need(math.isfinite(x), 'NONFINITE_VALUE')
    return x

def integer(v):
    x=number(v); need(x==int(x),'NONINTEGER_VALUE'); return int(x)

def raw_rows(path, fields):
    with path.open(newline='',encoding='utf-8') as f:
        r=csv.DictReader(f)
        need(r.fieldnames == list(fields),'CSV_SCHEMA_FAILURE')
        rows=list(r)
    need(bool(rows),'EMPTY_INPUT')
    need(all(None not in row and all(v is not None for v in row.values()) for row in rows),'CSV_SCHEMA_FAILURE')
    # Safety pass over timestamps ONLY, before parsing prices or emitting counts.
    for row in rows:
        t=integer(row['time'])
        need(START<=t<HOLDOUT_START,'BOUNDARY_VIOLATION')
        if 'time_msc' in fields:
            ms=integer(row['time_msc'])
            need(START*1000<=ms<HOLDOUT_START*1000,'BOUNDARY_VIOLATION')
            need(ms//1000==t,'TIME_TIME_MSC_MISMATCH')
    return rows

def validate(folder):
    p=Path(folder); gaps=[]
    try:
        need(all((p/f).is_file() for f in (*FILES,'sha256_manifest.json')),'MISSING_FILE')
        man=json.loads((p/'sha256_manifest.json').read_text())
        need(set(man)==set(FILES),'MANIFEST_SCHEMA_FAILURE')
        for f in FILES:
            need(set(man[f])=={'sha256','bytes'},'MANIFEST_SCHEMA_FAILURE')
            need(man[f]['sha256']==digest(p/f) and man[f]['bytes']==(p/f).stat().st_size,'INTEGRITY_FAILURE')
        m=json.loads((p/'metadata.json').read_text())
        need(set(m)==META_KEYS,'METADATA_SCHEMA_OR_PRIVACY_FAILURE')
        need(set(m['account'])=={'server'} and set(m['terminal'])=={'build','maxbars'},'PRIVACY_SCHEMA_FAILURE')
        need(set(m['symbol'])==set(SYMBOL_FIELDS),'SYMBOL_SCHEMA_FAILURE')
        need(m['strategy_outcomes_calculated'] is False and m['holdout_2026_requested'] is False,'OUTCOME_BOUNDARY_FAILURE')
        need(m['collector_version']=='JP225_STAGE1_v0.2','COLLECTOR_VERSION_FAILURE')
        need(isinstance(m['package_version'],str) and bool(m['package_version']) and
             isinstance(m['mt5_version'],list) and len(m['mt5_version'])==3,'VERSION_METADATA_FAILURE')
        need(m['request_time_convention']=='UTC_datetimes_per_MT5_Python_API','REQUEST_TIME_CONVENTION_FAILURE')
        collected=datetime.fromisoformat(m['collected_at_utc'])
        need(collected.tzinfo is not None and collected.utcoffset().total_seconds()==0,'COLLECTION_TIME_FAILURE')
        for k in ('collector_sha256','contract_sha256'):
            need(isinstance(m[k],str) and len(m[k])==64 and all(c in '0123456789abcdef' for c in m[k]),'CODE_IDENTITY_MISSING')
        need(m['collector_sha256']==digest(Path(__file__).with_name('collect_mt5_jp225_stage1.py')) and
             m['contract_sha256']==digest(Path(__file__).with_name('stage1_contract.py')),'COLLECTOR_CODE_IDENTITY_FAILURE')
        need(integer(m['terminal']['build'])>0 and integer(m['terminal']['maxbars'])>0,'TERMINAL_METADATA_FAILURE')
        need(m['symbol']['name']==SYMBOL,'EXACT_SYMBOL_FAILURE')
        server=m['account']['server']
        need(isinstance(server,str) and bool(server),'SERVER_IDENTITY_MISSING')
        need(integer(m['symbol']['digits'])>=0,'SYMBOL_DIGITS_FAILURE')
        for k in ('point','trade_tick_size','trade_contract_size','volume_min','volume_step'):
            need(number(m['symbol'][k])>0,'SYMBOL_NUMERIC_FAILURE')
        need(m['m1_request']['start']=='2024-11-29T00:00:00' and
             m['m1_request']['end_inclusive']=='2025-12-31T23:59:00','REQUEST_BOUNDARY_FAILURE')
        bars=raw_rows(p/FILES[1], M1_FIELDS)
        ts=[integer(r['time']) for r in bars]
        need(all(a<b for a,b in zip(ts,ts[1:])),'M1_ORDER_OR_DUPLICATE_FAILURE')
        need(all(t%60==0 and t<=END for t in ts),'M1_UNEXPECTED_TIMESTAMP')
        for r in bars:
            o,h,l,c=[number(r[k]) for k in ('open','high','low','close')]
            need(0<l<=min(o,c)<=max(o,c)<=h,'M1_OHLC_FAILURE')
            need(all(integer(r[k])>=0 for k in ('tick_volume','spread','real_volume')),'M1_NUMERIC_FAILURE')
        need(m['m1_request']['rows']==len(bars) and m['m1_request']['first_time']==ts[0]
             and m['m1_request']['last_time']==ts[-1],'M1_METADATA_MISMATCH')
        warmup=sum(t<DISCOVERY_START for t in ts)
        if warmup<1000 or ts[0]>1733011200: gaps.append('WARMUP_COVERAGE_GAP')
        months={datetime.fromtimestamp(t, timezone.utc).month for t in ts if t>=DISCOVERY_START}
        if months!=set(range(1,13)): gaps.append('DISCOVERY_MONTH_COVERAGE_GAP')
        # Missing minutes include weekends/session closures; never impute or infer truncation.
        missing_minutes=sum(max(0,(b-a)//60-1) for a,b in zip(ts,ts[1:]))
        ticks=raw_rows(p/FILES[2], ('probe_id',*TICK_FIELDS))
        expected={i:(int(utc(a).timestamp()),int(utc(b).timestamp())) for i,a,b in PROBES}
        need(len(m['tick_probes'])==len(PROBES),'PROBE_METADATA_FAILURE')
        probe_counts={}; duplicate_count=0
        for i,(a,b) in expected.items():
            group=[r for r in ticks if r['probe_id']==i]
            meta=[r for r in m['tick_probes'] if r['probe_id']==i]
            need(len(meta)==1,'PROBE_METADATA_FAILURE')
            need(meta[0]['request_start']==next(x[1] for x in PROBES if x[0]==i) and
                 meta[0]['request_end']==next(x[2] for x in PROBES if x[0]==i),'PROBE_REQUEST_FAILURE')
            need(meta[0]['rows']==len(group),'PROBE_ROW_MISMATCH')
            probe_counts[i]=len(group)
            if not group: gaps.append('PROBE_COVERAGE_GAP'); continue
            need(meta[0]['first_time']==integer(group[0]['time']) and
                 meta[0]['last_time']==integer(group[-1]['time']),'PROBE_METADATA_MISMATCH')
            last_ms=-1; seen=set(); times=[]
            for r in group:
                t=integer(r['time']); ms=integer(r['time_msc'])
                need(a<=t<=b,'PROBE_UNEXPECTED_TIMESTAMP')
                need(ms>=last_ms,'TICK_ORDER_FAILURE'); last_ms=ms; times.append(t)
                bid,ask=number(r['bid']),number(r['ask'])
                need(0<bid<=ask,'BID_ASK_FAILURE')
                for k in ('last','volume','volume_real','flags'): need(number(r[k])>=0,'TICK_NUMERIC_FAILURE')
                key=tuple(r[k] for k in TICK_FIELDS)
                if key in seen: duplicate_count+=1
                seen.add(key)
            if times[0]>a+60 or times[-1]<b-60 or any(y-x>60 for x,y in zip(times,times[1:])):
                gaps.append('PROBE_TEMPORAL_COVERAGE_GAP')
        need(all(r['probe_id'] in expected for r in ticks),'UNKNOWN_PROBE_ID')
        if duplicate_count: gaps.append('EXACT_TICK_DUPLICATES_REVIEW_REQUIRED')
        source_identity={f:man[f]['sha256'] for f in FILES}
        need(m['source_review'] is None,'RAW_METADATA_REVIEW_MUTATION')
        review_path=p/'source_review.json'
        review=json.loads(review_path.read_text()) if review_path.is_file() else None
        # An independent source review is evidence, never inferred from server name or values.
        required={'status','raw_sha256','server','reviewer','evidence','timestamp_mapping',
                  'm1_identity','coverage','xm_identity'}
        if review is None: gaps.append('SOURCE_SEMANTICS_AND_COVERAGE_UNVERIFIED')
        else:
            need(set(review)==required,'SOURCE_REVIEW_SCHEMA_FAILURE')
            need(review['raw_sha256']==source_identity and review['server']==server,'SOURCE_REVIEW_BINDING_FAILURE')
            need(review['timestamp_mapping']=='UTC_RAW_SECONDS','UNSUPPORTED_TIMESTAMP_MAPPING')
            need(review['m1_identity']=='BID_M1_BAR_OPEN','M1_IDENTITY_UNQUALIFIED')
            need(review['status']=='PASS' and review['xm_identity'] is True and review['coverage']=='PASS', 'SOURCE_REVIEW_NOT_PASS')
            need(isinstance(review['reviewer'],str) and bool(review['reviewer']) and
                 isinstance(review['evidence'],list) and len(review['evidence'])>=3 and
                 all(isinstance(x,str) and bool(x) for x in review['evidence']),'SOURCE_REVIEW_EVIDENCE_MISSING')
            need(integer(m['symbol']['chart_mode'])==0,'CHART_MODE_NOT_BID')
        return {'status':'PARTIAL_WITH_GAPS' if gaps else 'PASS','gaps':sorted(set(gaps)),
          'raw_sha256':{**{f:man[f]['sha256'] for f in FILES},**({'source_review.json':digest(review_path)} if review is not None else {})},
          'm1':{'rows':len(bars),'first_raw_time':ts[0],'last_raw_time':ts[-1],
                'warmup_rows':warmup,'missing_minutes_including_sessions':missing_minutes},
          'tick_probe_counts':probe_counts,'exact_tick_duplicates':duplicate_count,
          'packet_a_execution_pass':False,'strategy_outcomes_calculated':False}
    except Invalid as e:
        return {'status':'FAIL','violations':[str(e)],'strategy_outcomes_calculated':False}
    except Exception:
        return {'status':'FAIL','violations':['INVALID_INPUT'],'strategy_outcomes_calculated':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('--out'); args=ap.parse_args()
    result=validate(args.folder)
    if args.out: Path(args.out).write_bytes(canonical(result))
    print(json.dumps(result,indent=2)); raise SystemExit(1 if result['status']=='FAIL' else 0)
