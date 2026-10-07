import hashlib
import json
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import Mock
from fxns import (event_schedule, validate_event_timing, validate_formal_source,
                  validate_news_window, dedupe_headlines, select_quote_at_or_after, Quote)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source-probe'))
from gdelt_schema_probe import normalize

class PreFreezeTest(unittest.TestCase):
    def test_monday_tuesday(self): self.check_day(5)
    def test_tuesday_wednesday(self): self.check_day(6)
    def test_wednesday_thursday(self): self.check_day(7)
    def test_thursday_friday(self): self.check_day(8)
    def check_day(self, day):
        c,e,x=event_schedule(date(2026,10,day))
        self.assertEqual(x-e,timedelta(hours=24))
        self.assertEqual(x.day,day+1)
        self.assertEqual((e.hour,e.minute,x.hour,x.minute),(8,15,8,15))
        validate_event_timing(c,c+timedelta(minutes=14),e,x)
    def test_friday_rejected(self):
        with self.assertRaisesRegex(ValueError,'INELIGIBLE'): event_schedule(date(2026,10,9))
    def test_weekend_rejected(self):
        for d in (10,11):
            with self.assertRaises(ValueError): event_schedule(date(2026,10,d))
    def test_holiday_no_rollover(self):
        with self.assertRaisesRegex(ValueError,'SESSION_UNAVAILABLE'):
            event_schedule(date(2026,10,8),[date(2026,10,9)])
    def test_old_monday_exit_rejected(self):
        c,e,x=event_schedule(date(2026,10,8))
        with self.assertRaisesRegex(ValueError,'SCHEDULE'): validate_event_timing(c,c,e,x+timedelta(days=3))
    def test_missing_friday_exit_quote(self):
        _,_,x=event_schedule(date(2026,10,8))
        with self.assertRaises(ValueError): select_quote_at_or_after([],x)
    def test_friday_exit_tolerance(self):
        _,_,x=event_schedule(date(2026,10,8))
        q=Quote(x+timedelta(seconds=60),100,101)
        self.assertEqual(select_quote_at_or_after([q],x),q)
        with self.assertRaises(ValueError): select_quote_at_or_after([Quote(x+timedelta(seconds=61),100,101)],x)
    def test_incomplete_source_never_classified_or_joined(self):
        classify,market=Mock(),Mock()
        for count in (250,251):
            with self.assertRaisesRegex(ValueError,'INPUT_CORPUS_COMPLETENESS_UNVERIFIED'):
                validate_formal_source({'article_count':count},source_qualified=True,acquisition_proven=True)
                classify(); market()
        classify.assert_not_called(); market.assert_not_called()
    def test_below_cap_needs_source_and_acquisition(self):
        s={'article_count':0,'completeness':'UNVERIFIED_EVEN_BELOW_CAP'}
        for kwargs in ({},{'source_qualified':True},{'acquisition_proven':True}):
            with self.assertRaisesRegex(ValueError,'BLOCKED'): validate_formal_source(s,**kwargs)
        validate_formal_source(s,source_qualified=True,acquisition_proven=True)
    def test_open_window(self):
        c,_,_=event_schedule(date(2026,10,8))
        row=dict(record_id='x',source_domain='example.com',title='Synthetic',url='https://example.com/x')
        for time in (c-timedelta(hours=24),c):
            with self.assertRaises(ValueError): validate_news_window(dict(row,gdelt_seen_at=time.isoformat()),c)
        validate_news_window(dict(row,gdelt_seen_at=(c-timedelta(seconds=1)).isoformat()),c)
    def test_core_probe_deduplication_parity(self):
        c,_,_=event_schedule(date(2026,10,8)); start=c-timedelta(hours=24)
        base=dict(url='https://example.com/a',title='Synthetic',seendate='20261007T010000Z',domain='example.com',language='English')
        rows=[base,dict(base),dict(base,url='https://example.com/b',title=' ＳＹＮＴＨＥＴＩＣ '),dict(base,url='https://example.com/a?x=1',title='Synthetic different')]
        s=normalize(json.dumps({'articles':rows}).encode(),start,c,250)
        self.assertEqual(dedupe_headlines(s['records']),s['records'])
        # Use every pre-dedupe row, independent of response order.
        mapped=[dict(url=r['url'],title=r['title'],gdelt_seen_at=s['records'][0]['gdelt_seen_at']) for r in rows]
        self.assertEqual([r['url'] for r in dedupe_headlines(mapped)],[r['url'] for r in s['records']])
        self.assertEqual(dedupe_headlines(mapped),dedupe_headlines(list(reversed(mapped))))
    def test_exact_prompt_hashes(self):
        m=json.loads((ROOT/'PROMPT_MANIFEST_v0.1.json').read_text())
        for name,digest in m['files'].items(): self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
