import csv,hashlib,json,math,tempfile,unittest,sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
from stage1_contract import *
from validate_stage1 import validate,FILES,META_KEYS
from stage2 import freeze_manifest,read_frozen_manifest,collect
from validate_stage2 import validate_stage2
sys.path.insert(0,str(Path(__file__).parents[1]/'implementation'))
from jp225_ema_screen import Quote,recursive_ema,cluster_bootstrap_mean,map_executable_outcome
from holdout_loader import load_holdout

class Array(list):
    def __init__(self,rows,fields): super().__init__(rows);self.dtype=SimpleNamespace(names=tuple(fields))

def nt(d):return SimpleNamespace(_asdict=lambda:d)

def writecsv(p,fields,rows):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)

class Hardening(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.p=self.root/'s1';self.p.mkdir()
        self.bars=[dict(zip(M1_FIELDS,(START+i*60,100,101,99,100,2,1,0))) for i in range(1000)]
        for month in range(1,13):
            t=int(utc(f'2025-{month:02d}-15T00:00:00').timestamp())
            self.bars.append(dict(zip(M1_FIELDS,(t,100,101,99,100+(month%2)*0.5,2,1,0))))
        self.ticks=[];self.probes=[]
        for pid,a,b in PROBES:
            aa=int(utc(a).timestamp());bb=int(utc(b).timestamp())
            for t in range(aa,bb+1,60): self.ticks.append(dict(zip(('probe_id',*TICK_FIELDS),(pid,t,100,101,0,0,t*1000,6,0))))
            self.probes.append({'probe_id':pid,'request_start':a,'request_end':b,'rows':(bb-aa)//60+1,'first_time':aa,'last_time':bb})
        self.m={k:None for k in META_KEYS};self.m.update(collector_version='JP225_STAGE1_v0.2',
          strategy_outcomes_calculated=False,holdout_2026_requested=False,
          collected_at_utc='2026-10-04T00:00:00+00:00',package_version='synthetic',mt5_version=[5,1,'synthetic'],
          request_time_convention='UTC_datetimes_per_MT5_Python_API',
          collector_sha256=digest(Path(__file__).with_name('collect_mt5_jp225_stage1.py')),
          contract_sha256=digest(Path(__file__).with_name('stage1_contract.py')),
          account={'server':'XM-SYNTHETIC'},terminal={'build':5000,'maxbars':1000000},
          symbol=dict(zip(SYMBOL_FIELDS,(SYMBOL,1,0.1,0.1,1,0.01,0.01,0))),
          m1_request={'start':'2024-11-29T00:00:00','end_inclusive':'2025-12-31T23:59:00',
                      'rows':len(self.bars),'first_time':self.bars[0]['time'],'last_time':self.bars[-1]['time']},
          tick_probes=self.probes,bar_price_identity='UNKNOWN')
        self.save()
    def tearDown(self):self.tmp.cleanup()
    def save(self):
        writecsv(self.p/FILES[1],M1_FIELDS,self.bars)
        writecsv(self.p/FILES[2],('probe_id',*TICK_FIELDS),self.ticks)
        (self.p/FILES[0]).write_bytes(canonical(self.m))
        (self.p/'sha256_manifest.json').write_bytes(canonical({f:{'sha256':digest(self.p/f),'bytes':(self.p/f).stat().st_size} for f in FILES}))
    def qualified(self):
        self.save()
        review={'status':'PASS','raw_sha256':{f:digest(self.p/f) for f in FILES},
            'server':'XM-SYNTHETIC','reviewer':'synthetic-only',
            'evidence':['synthetic-clock','synthetic-bars','synthetic-coverage'],
            'timestamp_mapping':'UTC_RAW_SECONDS','m1_identity':'BID_M1_BAR_OPEN',
            'coverage':'PASS','xm_identity':True}
        (self.p/'source_review.json').write_bytes(canonical(review))
    def fail(self,code):self.assertIn(code,validate(self.p)['violations'])
    def test_unverified_partial(self):self.assertEqual(validate(self.p)['status'],'PARTIAL_WITH_GAPS')
    def test_reviewed_pass(self):self.qualified();self.assertEqual(validate(self.p)['status'],'PASS')
    def test_integrity(self):(self.p/FILES[1]).write_text('bad');self.fail('INTEGRITY_FAILURE')
    def test_holdout_before_market_parse(self):
        self.bars.append(dict(zip(M1_FIELDS,(HOLDOUT_START,'SECRET',0,0,0,0,0,0))));self.save()
        r=validate(self.p);self.assertEqual(r['violations'],['BOUNDARY_VIOLATION']);self.assertNotIn('m1',r);self.assertNotIn('SECRET',json.dumps(r))
    def test_msc_holdout(self):self.ticks[0]['time_msc']=HOLDOUT_START*1000;self.save();self.fail('BOUNDARY_VIOLATION')
    def test_duplicate_m1(self):self.bars.insert(0,self.bars[0].copy());self.save();self.fail('M1_ORDER_OR_DUPLICATE_FAILURE')
    def test_nonfinite(self):self.bars[0]['close']='nan';self.save();self.fail('NONFINITE_VALUE')
    def test_symbol(self):self.m['symbol']['name']='JP225';self.save();self.fail('EXACT_SYMBOL_FAILURE')
    def test_credentials(self):self.m['account']['login']=123;self.save();self.fail('PRIVACY_SCHEMA_FAILURE')
    def test_ask_below_bid(self):self.ticks[0]['ask']=99;self.save();self.fail('BID_ASK_FAILURE')
    def test_probe_gap(self):self.ticks.pop(5);self.probes[0]['rows']-=1;self.save();self.assertIn('PROBE_TEMPORAL_COVERAGE_GAP',validate(self.p)['gaps'])
    def test_msc_identity(self):self.ticks[0]['time_msc']+=1000;self.save();self.fail('TIME_TIME_MSC_MISMATCH')
    def test_boundary_guard(self):
        with self.assertRaisesRegex(ValueError,'BOUNDARY_VIOLATION'):boundary_check([{'time':HOLDOUT_START}])
    def test_metadata_allowlist(self):self.assertEqual(allowlist(nt({'server':'XM','password':'secret','login':1,'path':'secret'}),('server',)),{'server':'XM'})
    def test_manifest_requires_pass(self):
        with self.assertRaises(PermissionError):freeze_manifest(self.p,self.root/'event')
    def test_manifest_and_stage2(self):
        self.qualified(); sha=freeze_manifest(self.p,self.root/'event');path=self.root/'event'/'event_manifest.json'
        m=read_frozen_manifest(path,sha);self.assertFalse(m['strategy_outcomes_calculated'])
        self.assertTrue(all(r['end']<HOLDOUT_START for r in m['requests']))
        api=Mock();api.initialize.return_value=True;api.COPY_TICKS_ALL=0
        api.symbol_info.return_value=nt(self.m['symbol']);api.account_info.return_value=nt(self.m['account'])
        def ticks(symbol,a,b,flags):
            t=int(a.timestamp());return Array([dict(zip(TICK_FIELDS,(t,100,101,0,0,t*1000,6,0)))],TICK_FIELDS)
        api.copy_ticks_range.side_effect=ticks
        collect(path,sha,self.root/'s2',api)
        self.assertEqual(validate_stage2(self.p,self.root/'s2',path,sha)['status'],'PASS')
    def test_discovery_one_shot_synthetic(self):
        from run_discovery import run,code_identity
        self.qualified();sha=freeze_manifest(self.p,self.root/'event');path=self.root/'event'/'event_manifest.json'
        api=Mock();api.initialize.return_value=True;api.COPY_TICKS_ALL=0
        api.symbol_info.return_value=nt(self.m['symbol']);api.account_info.return_value=nt(self.m['account'])
        def ticks(symbol,a,b,flags):
            t=int(a.timestamp())+1
            return Array([dict(zip(TICK_FIELDS,(t,100,101,0,0,t*1000,6,0)))],TICK_FIELDS)
        api.copy_ticks_range.side_effect=ticks;collect(path,sha,self.root/'s2',api)
        q=validate_stage2(self.p,self.root/'s2',path,sha)
        from stage2 import SPEC
        binding={'spec_sha256':digest(SPEC),'code_sha256':code_identity(),
                 'event_manifest_sha256':sha,'stage1_sha256':q['stage1_sha256'],'stage2_sha256':q['stage2_sha256']}
        gate=self.root/'gate.json';gate.write_bytes(canonical({'status':'PASS','independent_review':'PASS',
                 'packet_a':'PASS','sample':'2025_DISCOVERY','binding':binding}))
        run(self.p,self.root/'s2',path,sha,gate,digest(gate),self.root/'run')
        result=json.loads((self.root/'run'/'RESULT.json').read_text())
        self.assertEqual(result['decision'],'NO_ADVANCEMENT')
        self.assertFalse(json.loads((self.root/'run'/'DISCOVERY_DECISION.json').read_text())['discovery_advancement'])
        with self.assertRaises(FileExistsError):run(self.p,self.root/'s2',path,sha,gate,digest(gate),self.root/'run2')
    def test_stage1_actual_collector_allowlist_and_end(self):
        import collect_mt5_jp225_stage1 as c
        api=Mock();api.initialize.return_value=True;api.TIMEFRAME_M1=1;api.COPY_TICKS_ALL=0
        api.__version__='synthetic';api.version.return_value=(5,1,'synthetic')
        api.terminal_info.return_value=nt({'build':1,'maxbars':1000000,'path':'PRIVATE_PATH'})
        api.account_info.return_value=nt({'server':'XM-SYNTHETIC','login':123,'name':'PRIVATE_NAME','balance':123})
        api.symbol_select.return_value=True;api.symbol_info.return_value=nt(self.m['symbol'])
        api.copy_rates_range.return_value=Array(self.bars,M1_FIELDS)
        def tick_rows(symbol,a,b,flag):
            group=[{k:r[k] for k in TICK_FIELDS} for r in self.ticks if a.timestamp()<=int(r['time'])<=b.timestamp()]
            return Array(group,TICK_FIELDS)
        api.copy_ticks_range.side_effect=tick_rows
        output=self.root/'collected'
        with patch.dict(sys.modules,{'MetaTrader5':api}),patch.object(sys,'argv',['collector','--out',str(output)]):c.main()
        meta=(output/'metadata.json').read_text()
        self.assertNotIn('PRIVATE',meta);self.assertNotIn('login',meta);self.assertNotIn('balance',meta)
        self.assertEqual(int(api.copy_rates_range.call_args.args[-1].timestamp()),END)
        self.assertEqual(validate(output)['status'],'PARTIAL_WITH_GAPS')
    def test_stage1_boundary_before_write(self):
        import collect_mt5_jp225_stage1 as c
        api=Mock();api.initialize.return_value=True;api.TIMEFRAME_M1=1;api.version.return_value=(5,1,'test')
        api.terminal_info.return_value=nt({});api.account_info.return_value=nt({})
        api.symbol_select.return_value=True;api.symbol_info.return_value=nt(self.m['symbol'])
        api.copy_rates_range.return_value=Array([{'time':HOLDOUT_START}],M1_FIELDS)
        out=self.root/'bad-collection'
        with patch.dict(sys.modules,{'MetaTrader5':api}),patch.object(sys,'argv',['collector','--out',str(out)]):
            with self.assertRaisesRegex(ValueError,'BOUNDARY_VIOLATION'):c.main()
        self.assertFalse((out/'m1_warmup_2025_raw.csv').exists());api.copy_ticks_range.assert_not_called()
    def test_stage2_rejects_tamper_before_api(self):
        path=self.root/'bad.json';path.write_text('{}');api=Mock()
        with self.assertRaises(PermissionError):collect(path,'0'*64,self.root/'s2',api)
        api.initialize.assert_not_called()
    def test_nonfinite_quote(self):
        for x in (float('nan'),float('inf'),0,-1):
            with self.assertRaises(ValueError):Quote(utc('2025-01-01'),x,101)
    def test_bootstrap_order_invariant(self):
        self.assertEqual(cluster_bootstrap_mean({2:[2],1:[1]},reps=100),cluster_bootstrap_mean({1:[1],2:[2]},reps=100))
    def test_holdout_reader_not_called(self):
        path=self.root/'decision.json';path.write_bytes(canonical({'discovery_advancement':False}))
        reader=Mock()
        with self.assertRaises(PermissionError):load_holdout(self.root/'NONEXISTENT_HOLDOUT',path,digest(path),{},reader)
        reader.assert_not_called()
    def test_bare_candidate_does_not_unlock_loader(self):
        path=self.root/'decision.json';path.write_bytes(canonical({'candidate':'ALL','discovery_advancement':True}))
        reader=Mock()
        with self.assertRaises(PermissionError):load_holdout('holdout',path,digest(path),{},reader)
        reader.assert_not_called()
    def test_slope_algebra_synthetic(self):
        # Independent state enumeration; no market data, no fitted parameter.
        for pf in (-10,0,10):
            for ps in (-10,0,10):
                for x in range(-100,101):
                    f=x/3+pf*2/3;s=x*2/201+ps*199/201
                    if pf<=ps and f>s:self.assertGreater(s,ps)
                    if pf>=ps and f<s:self.assertLess(s,ps)

if __name__=='__main__':unittest.main()
