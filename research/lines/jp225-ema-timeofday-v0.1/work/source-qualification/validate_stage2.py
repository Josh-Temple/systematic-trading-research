"""Stage 2 structural qualification; no entry/exit returns are calculated."""
import csv,json
from pathlib import Path
from stage1_contract import canonical,digest,TICK_FIELDS,SYMBOL_FIELDS
from stage2 import read_frozen_manifest
from validate_stage1 import validate,need,number,integer,Invalid

def validate_stage2(stage1,folder,manifest,expected_sha):
    try:
        s1=validate(stage1); need(s1['status']=='PASS','STAGE1_NOT_PASS')
        m=read_frozen_manifest(manifest,expected_sha)
        need(m['stage1']==s1['raw_sha256'],'STAGE1_BINDING_FAILURE')
        p=Path(folder); man=json.loads((p/'sha256_manifest.json').read_text())
        need(set(man)=={'metadata.json','event_ticks_raw.csv'},'MANIFEST_SCHEMA_FAILURE')
        for n in man:
            need(set(man[n])=={'sha256','bytes'} and man[n]['sha256']==digest(p/n) and
                 man[n]['bytes']==(p/n).stat().st_size,'INTEGRITY_FAILURE')
        meta=json.loads((p/'metadata.json').read_text())
        need(set(meta)=={'version','event_manifest_sha256','symbol','account','requests',
                        'strategy_outcomes_calculated','holdout_requested','source_qualification'},'METADATA_SCHEMA_FAILURE')
        base=json.loads((Path(stage1)/'metadata.json').read_text())
        need(meta['version']=='JP225_STAGE2_v1' and meta['event_manifest_sha256']==expected_sha,'MANIFEST_BINDING_FAILURE')
        need(meta['symbol']==base['symbol'] and meta['account']==base['account'],'SOURCE_IDENTITY_CHANGED')
        need(meta['strategy_outcomes_calculated'] is False and meta['holdout_requested'] is False,'OUTCOME_BOUNDARY_FAILURE')
        with (p/'event_ticks_raw.csv').open(newline='') as f:
            r=csv.DictReader(f);need(r.fieldnames==['request_id',*TICK_FIELDS],'TICK_SCHEMA_FAILURE');rows=list(r)
        # Timestamp-only safety pass before touching any quote values.
        from stage1_contract import START,HOLDOUT_START
        for r in rows:
            t=integer(r['time']); ms=integer(r['time_msc'])
            need(START<=t<HOLDOUT_START and START*1000<=ms<HOLDOUT_START*1000,'BOUNDARY_VIOLATION')
            need(ms//1000==t,'TIME_TIME_MSC_MISMATCH')
        need(len(meta['requests'])==len(m['requests']),'REQUEST_METADATA_FAILURE')
        previous={}; prices_at={}; counts={i:0 for i in range(len(m['requests']))}; seen=set(); duplicates=0
        for r in rows:
            i=integer(r['request_id']);need(i in counts,'UNKNOWN_REQUEST')
            a,b=m['requests'][i]['start'],m['requests'][i]['end']; ms=integer(r['time_msc'])
            need(a*1000<=ms<=b*1000,'REQUEST_BOUNDARY_VIOLATION')
            need(ms>=previous.get(i,-1),'TICK_ORDER_FAILURE');previous[i]=ms
            bid,ask=number(r['bid']),number(r['ask']);need(0<bid<=ask,'BID_ASK_FAILURE')
            need(ms not in prices_at or prices_at[ms]==(bid,ask),'AMBIGUOUS_SAME_TIME_QUOTES')
            prices_at[ms]=(bid,ask)
            for k in ('last','volume','flags','volume_real'):need(number(r[k])>=0,'TICK_NUMERIC_FAILURE')
            key=(i,*[r[k] for k in TICK_FIELDS]);duplicates+=key in seen;seen.add(key);counts[i]+=1
        for i,r in enumerate(meta['requests']):
            need(r=={'request_id':i,**m['requests'][i],'rows':counts[i]},'REQUEST_ROW_MISMATCH')
        # Empty requests are legitimate NO_EXECUTABLE_* outcomes, not imputed data.
        return {'status':'PASS','event_manifest_sha256':expected_sha,'stage1_sha256':s1['raw_sha256'],
          'stage2_sha256':{n:man[n]['sha256'] for n in man},'empty_requests':sum(c==0 for c in counts.values()),
          'exact_duplicates_preserved':duplicates,'strategy_outcomes_calculated':False,
          'packet_a_execution_pass':True}
    except (Invalid,PermissionError) as e: return {'status':'FAIL','violations':[str(e)],'strategy_outcomes_calculated':False}
    except Exception: return {'status':'FAIL','violations':['INVALID_INPUT'],'strategy_outcomes_calculated':False}
