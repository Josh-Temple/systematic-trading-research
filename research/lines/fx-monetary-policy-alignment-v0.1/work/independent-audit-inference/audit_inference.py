#!/usr/bin/env python3
from __future__ import annotations
import ast, importlib.util, json, math, random
from pathlib import Path

LINE=Path(__file__).resolve().parents[2]
IMPL=LINE/"work"/"implementation"/"inference.py"
CFG=LINE/"work"/"implementation"/"INFERENCE_CONFIG.json"

def load_impl():
    s=importlib.util.spec_from_file_location("fxmp_inference_audited",IMPL)
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def oracle_type7(vals,p):
    vals=sorted(vals); h=(len(vals)-1)*p; lo=math.floor(h); hi=math.ceil(h); f=h-lo
    return vals[lo] if lo==hi else vals[lo]+f*(vals[hi]-vals[lo])

def oracle_draw(n,L,seed):
    r=random.Random(seed); out=[]
    for _ in range(math.ceil(n/L)):
        s=r.randrange(n); out.extend((s+j)%n for j in range(L))
    return out[:n]

def main():
    cfg=json.loads(CFG.read_text())
    assert cfg["block_length_calendar_slots"]==12
    assert cfg["bootstrap_replicates"]==10000
    assert cfg["seed"]==20261004
    assert cfg["min_aligned"]==24 and cfg["min_opposed"]==24

    tree=ast.parse(IMPL.read_text())
    imports=set()
    for n in ast.walk(tree):
        if isinstance(n,ast.Import): imports.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n,ast.ImportFrom) and n.module: imports.add(n.module.split(".")[0])
    forbidden={"urllib","requests","httpx","socket","subprocess","pandas","numpy"}
    assert not (imports & forbidden)

    m=load_impl()
    assert m.type7_percentile([0.0,10.0],0.25)==oracle_type7([0.0,10.0],0.25)==2.5
    assert m.draw_circular_indices(5,2,random.Random(7))==[2,3,1,2,3]

    grid=[]
    for i in range(24):
        grid.append({"classification":"ALIGNED","y":0.02})
        grid.append({"classification":"OPPOSED","y":0.00})
    res=m.evaluate(grid,m.InferenceConfig(block_length=12,replicates=200,seed=20261004,min_aligned=24,min_opposed=24))
    assert res["status"]=="OK"
    assert abs(res["observed_d"]-0.02)<1e-15
    assert abs(res["bootstrap"]["lower_95"]-0.02)<1e-15
    assert res["decision"]=="PROMISING_EXPLORATORY"

    small=[{"classification":"ALIGNED","y":0.01} for _ in range(23)]+[{"classification":"OPPOSED","y":0.0} for _ in range(30)]
    hold=m.evaluate(small,m.InferenceConfig(replicates=10,min_aligned=24,min_opposed=24))
    assert hold["status"]=="INSUFFICIENT_EVIDENCE" and hold["bootstrap"] is None

    pathological=[{"classification":"ALIGNED","y":0.01}]+[{"classification":"OPPOSED","y":0.0} for _ in range(4)]
    try:
        m.evaluate(pathological,m.InferenceConfig(block_length=1,replicates=20,seed=1,min_aligned=1,min_opposed=1))
    except m.InferenceError:
        empty_fail="PASS"
    else:
        raise AssertionError("empty-group bootstrap did not fail closed")

    out={
      "audit_id":"AUDIT-FXMP-INFERENCE-20261004-01",
      "audited_head":"c9e9df2b346cb2c0f8e70c558d7f91bf8a994a73",
      "result":"PASS",
      "config":cfg,
      "known_circular_draw":"PASS",
      "type7":"PASS",
      "known_difference":"PASS",
      "minimum_group_rule":"PASS",
      "empty_group_fail_closed":empty_fail,
      "static_boundary":"PASS",
      "market_outcome_accessed":False
    }
    print(json.dumps(out,sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
