"""Synthetic-only tests; never import or connect to the actual MetaTrader5 package."""
import ast
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import collect_mt5_eurjpy_source_probe as c

class FakeTicks(list):
    dtype = SimpleNamespace(names=c.EXPECTED_TICK_FIELDS)


def ticks(bid=100.0, ask=101.0):
    return FakeTicks([dict(time=1234567890,bid=bid,ask=ask,last=0.0,
                           volume=0,time_msc=1234567890123,flags=6,volume_real=0.0)])


def fake_mt5():
    return SimpleNamespace(initialize=Mock(return_value=True),shutdown=Mock(),
        symbol_select=Mock(return_value=True),symbols_get=Mock(return_value=[]),
        symbol_info=Mock(return_value=SimpleNamespace(name='EURJPY',swap_long=1,swap_short=-1,swap_rollover3days=3)),
        terminal_info=Mock(return_value=SimpleNamespace(build=123,maxbars=100)),
        account_info=Mock(return_value=SimpleNamespace(server='SYNTHETIC_SERVER')),
        copy_ticks_range=Mock(return_value=ticks()),COPY_TICKS_ALL=0,
        version=Mock(return_value=(1,2,3)),__version__='synthetic')


class CollectorTest(unittest.TestCase):
    def run_fake(self, mt5, out):
        with patch.dict(sys.modules,{'MetaTrader5':mt5}),patch.object(sys,'argv',['collector','--out',str(out)]),patch('builtins.print'):
            c.main()
    def test_fixed_calendar(self):
        expected=['2026-01-16','2026-07-17','2026-10-02']
        fridays=[p for p in c.PROBES_JST if 'friday' in p[0]]
        self.assertEqual([p[1][:10] for p in fridays],expected)
        for _,start,_ in fridays:
            dt=c.parse_aware(start)
            self.assertEqual(dt.weekday(),4)
            self.assertLess(dt.date().isoformat(),'2026-10-07')
    def test_thursday_friday_adjacent(self):
        self.assertEqual(c.parse_aware(c.PROBES_JST[3][1])-c.parse_aware(c.PROBES_JST[0][1]),timedelta(days=1))
        self.assertEqual(c.parse_aware(c.PROBES_JST[0][1]).weekday(),3)
    def test_existing_windows_unchanged(self):
        self.assertEqual([p[1][:10] for p in c.PROBES_JST[:3]],['2026-01-15','2026-07-15','2026-10-06'])
    def test_window_and_utc_mapping(self):
        for _,start,end in c.PROBES_JST:
            a,b=c.parse_aware(start),c.parse_aware(end)
            self.assertEqual((a.hour,a.minute,b.hour,b.minute),(8,14,8,16))
            self.assertEqual(b-a,timedelta(minutes=2))
            self.assertEqual(c.to_utc(start).tzinfo,timezone.utc)
            self.assertEqual((c.to_utc(start).hour,c.to_utc(start).minute),(23,14))
            self.assertEqual(c.to_utc(start).date(),a.date()-timedelta(days=1))
        with self.assertRaises(ValueError): c.to_utc('2026-01-16T08:14:00')
    def test_schema_and_valid_quotes(self):
        c.validate_tick_array(ticks())
        c.validate_tick_array(FakeTicks())
        with self.assertRaises(RuntimeError): c.validate_tick_array(None)
        bad=FakeTicks();bad.dtype=SimpleNamespace(names=('bid','ask'))
        with self.assertRaises(RuntimeError): c.validate_tick_array(bad)
    def test_invalid_quotes_fail_closed(self):
        for bid,ask in [(0,1),(-1,1),(2,1),(1,0),(float('nan'),1),(1,float('inf'))]:
            with self.subTest(bid=bid,ask=ask),self.assertRaises(RuntimeError): c.validate_tick_array(ticks(bid,ask))
    def test_raw_epoch_bounds(self):
        self.assertEqual(c.raw_time_bounds(ticks()),dict(first_time=1234567890,last_time=1234567890,first_time_msc=1234567890123,last_time_msc=1234567890123))
        self.assertTrue(all(v is None for v in c.raw_time_bounds(FakeTicks()).values()))
    def test_sensitive_fields_not_accessed(self):
        class Account:
            server='SYNTHETIC_SERVER'
            def __getattr__(self,key): raise AssertionError('sensitive field accessed: '+key)
        self.assertEqual(c.ACCOUNT_FIELDS,('server',))
        self.assertEqual(c.allowlist(Account(),c.ACCOUNT_FIELDS),{'server':'SYNTHETIC_SERVER'})
        forbidden={'login','name','password','balance','equity','margin','path','data_path'}
        self.assertFalse(forbidden.intersection(c.ACCOUNT_FIELDS+c.TERMINAL_FIELDS))
    def test_serialization_manifest_and_utc_requests(self):
        mt5=fake_mt5()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'attempt';self.run_fake(mt5,out)
            metadata=json.loads((out/'metadata.json').read_text())
            self.assertEqual(metadata['collector_version'],'FXNS_EURJPY_SOURCE_PROBE_v0.2')
            self.assertEqual(len(metadata['tick_probes']),6)
            self.assertEqual(metadata['returned_timestamp_semantics'],'UNVERIFIED_PRESERVE_RAW_TIME_AND_TIME_MSC')
            self.assertEqual(metadata['commission_status'],'UNVERIFIED_NOT_INFERRED_FROM_ACCOUNT_HISTORY')
            for p in metadata['tick_probes'][3:]:
                self.assertEqual((p['purpose'],p['intended_weekday']),('FRIDAY_EXIT_FEASIBILITY','Friday'))
                self.assertEqual(p['first_time_msc'],1234567890123)
            rows=list(csv.DictReader((out/'tick_probes_raw.csv').read_text().splitlines()))
            self.assertEqual(len(rows),6);self.assertEqual(rows[0]['time'],'1234567890')
            manifest=json.loads((out/'sha256_manifest.json').read_text())
            self.assertEqual(set(manifest),{'tick_probes_raw.csv','metadata.json'})
            for name,item in manifest.items():
                raw=(out/name).read_bytes()
                self.assertEqual(item,{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
            for call in mt5.copy_ticks_range.call_args_list:
                self.assertEqual(call.args[0],'EURJPY')
                self.assertEqual(call.args[1].tzinfo,timezone.utc)
                self.assertEqual(call.args[2].tzinfo,timezone.utc)
            mt5.shutdown.assert_called_once()
            with self.assertRaises(FileExistsError): self.run_fake(mt5,out)
    def test_no_symbol_substitution(self):
        mt5=fake_mt5();mt5.symbol_select.return_value=False
        mt5.symbols_get.return_value=[SimpleNamespace(name='EURJPYm'),SimpleNamespace(name='OTHER')]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError,'EXACT_SYMBOL_IDENTITY_REQUIRES_PRE_FREEZE_DECISION'):
                self.run_fake(mt5,Path(tmp)/'attempt')
        mt5.copy_ticks_range.assert_not_called();mt5.account_info.assert_not_called()
        mt5.symbol_select.assert_called_once_with('EURJPY',True)
    def test_suffix_argument_rejected_before_connection(self):
        mt5=fake_mt5()
        with patch.dict(sys.modules,{'MetaTrader5':mt5}),patch.object(sys,'argv',['collector','--symbol','EURJPYm']),patch('sys.stderr'):
            with self.assertRaises(SystemExit): c.main()
        mt5.initialize.assert_not_called()
    def test_no_outcome_or_order_api(self):
        tree=ast.parse(Path(c.__file__).read_text())
        names={n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='mt5'}
        self.assertEqual(names,{'initialize','shutdown','symbol_select','symbols_get','symbol_info','terminal_info','account_info','copy_ticks_range','COPY_TICKS_ALL','version','__version__'})
        self.assertNotIn('log',{n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute)})
        # Path joining uses /; only allow the existing file-path operands.
        divisions=[n for n in ast.walk(tree) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div)]
        self.assertTrue(all(isinstance(n.left,ast.Name) and n.left.id=='out' and isinstance(n.right,ast.Constant) and isinstance(n.right.value,str) for n in divisions))
