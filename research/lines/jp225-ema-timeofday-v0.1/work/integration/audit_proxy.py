"""Independent historical proxy replay. ONLY consumed 2018/2019/2020 OANDA samples."""
import argparse,csv,io,json,subprocess,hashlib,random
from collections import defaultdict
from datetime import datetime,timedelta,timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE_COMMIT='7ba1d404aa8b0e1c0f71321acebadcbfb9bcca8d'

def git(repo,*args): return subprocess.check_output(['git','-C',str(repo),*args])

def replay(repo,year):
    rows={}; sources=[]
    for month in range(1,6 if year==2020 else 13):
        path=f'pyfinancialdata/data/currencies/oanda/JP225_USD/{year}/oanda-JP225_USD-{year}-{month}.csv'
        sha=git(repo,'rev-parse',SOURCE_COMMIT+':'+path).decode().strip()
        raw=git(repo,'cat-file','blob',sha)
        if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=sha: raise AssertionError('blob mismatch')
        rr=list(csv.DictReader(io.StringIO(raw.decode())))
        sources.append({'path':path,'blob':sha,'sha256':hashlib.sha256(raw).hexdigest(),'rows':len(rr)})
        for r in rr:
            t=datetime.fromisoformat(r['time']).replace(tzinfo=timezone.utc)
            rows.setdefault(t,(float(r['open']),float(r['close'])))
    times=sorted(rows); stats={k:{'events':0,'missing':0,'daily':defaultdict(list)} for k in (('all',) if year==2018 else ('all','open','primary'))}
    f=s=rows[times[0]][1]; equality=True
    for i,t in enumerate(times[1:],1):
        p=rows[t][1]; pf,ps=f,s
        f=p/3+pf*2/3; s=(2/201)*p+(199/201)*ps
        d=1 if pf<=ps and f>s else -1 if pf>=ps and f<s else 0
        if not d or i<1000: continue
        equality &= (s>ps if d==1 else s<ps)
        signal=t+timedelta(minutes=1); local=signal.astimezone(ZoneInfo('Asia/Tokyo'))
        hm=(local.hour,local.minute)
        kinds=['all'] if year==2018 else ['all']+(['open'] if (8,45)<=hm<(9,15) else [])+(['primary'] if (14,45)<=hm<(15,15) else [])
        entry=rows.get(signal); exitq=rows.get(signal+timedelta(minutes=15))
        for k in kinds:
            stats[k]['events']+=1
            if entry is None or exitq is None: stats[k]['missing']+=1
            else: stats[k]['daily'][local.date().isoformat()].append(d*(exitq[0]-entry[0]))
    out={}
    for k,a in stats.items():
        dates=sorted(a['daily']); values=[v for vs in a['daily'].values() for v in vs]
        sums=[sum(a['daily'][d]) for d in dates]; counts=[len(a['daily'][d]) for d in dates]
        rng=random.Random(2255200); bs=[]
        for _ in range(10000):
            ix=[rng.randrange(len(dates)) for _ in dates]
            bs.append(sum(sums[i] for i in ix)/sum(counts[i] for i in ix))
        bs.sort()
        out[k]={'events':a['events'],'missing':a['missing'],'valid':len(values),'dates':len(dates),
                'mean':sum(values)/len(values),'wins':sum(v>0 for v in values),
                'ci_python_random':[bs[250],bs[9749]],'daily':{d:{'sum':sum(a['daily'][d]),'count':len(a['daily'][d]),'wins':sum(v>0 for v in a['daily'][d])} for d in dates}}
    return {'year':year,'source_commit':SOURCE_COMMIT,'sources':sources,'rows':len(times),
            'slope_event_sets_identical':equality,'results':out}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source_repo');ap.add_argument('out');a=ap.parse_args()
    Path(a.out).write_text(json.dumps([replay(a.source_repo,y) for y in (2018,2019,2020)],indent=2))
