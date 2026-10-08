import json
import unittest
from datetime import datetime,timedelta,timezone
from gdelt_schema_probe import normalize,parameters,title_key

class GDELTTest(unittest.TestCase):
    start=datetime(2026,10,5,23,tzinfo=timezone.utc)
    end=start+timedelta(hours=24)
    def row(self, **kw):
        r=dict(url='https://example.com/a',title='Synthetic policy headline',seendate='20261006T000000Z',domain='example.com',language='English'); r.update(kw); return r
    def run_rows(self, rows, limit=250): return normalize(json.dumps(dict(articles=rows)).encode(),self.start,self.end,limit)
    def test_valid_and_empty(self):
        self.assertEqual(self.run_rows([self.row()])['retained_count'],1)
        self.assertEqual(self.run_rows([])['article_count'],0)
    def test_cap_before_dedupe(self):
        with self.assertRaises(ValueError): self.run_rows([self.row()]*10,10)
    def test_bad_fields_language_timestamp_domain_url(self):
        for kw in [dict(title=''),dict(language='Japanese'),dict(seendate='2026-10-06'),dict(domain='other.com'),dict(url='file:///a'),dict(seendate='20261005T230000Z'),dict(seendate='20261006T230000Z')]:
            with self.subTest(kw=kw),self.assertRaises(ValueError): self.run_rows([self.row(**kw)])
    def test_missing_array_not_empty(self):
        for raw in [b'{}',b'[]',b'not json']:
            with self.assertRaises(ValueError): normalize(raw,self.start,self.end,250)
    def test_stable_dedupe(self):
        rows=[self.row(),self.row(title='Changed title'),self.row(url='https://example.com/b',title='  SYNTHETIC policy headline ')]
        self.assertEqual(self.run_rows(rows), self.run_rows(list(reversed(rows))))
        self.assertEqual(self.run_rows(rows)['retained_count'],1)
    def test_unicode_key(self): self.assertEqual(title_key('Ａ  B'),title_key('a b'))
    def test_window_and_limit(self):
        self.assertEqual(parameters(self.start,self.end)['maxrecords'],'250')
        for end,limit in [(self.end,251),(self.start+timedelta(hours=72),250)]:
            with self.assertRaises(ValueError): parameters(self.start,end,limit)

class PreservationTest(unittest.TestCase):
    def test_http_error_preserved_and_nonzero(self):
        import tempfile,sys,io,hashlib,urllib.error
        from pathlib import Path
        from unittest.mock import patch
        from gdelt_schema_probe import main
        raw=b'Synthetic throttling response'
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'attempt'
            error=urllib.error.HTTPError('https://example.com',429,'rate limit',{},io.BytesIO(raw))
            with patch.object(sys,'argv',['probe','--output',str(out),'--end','20261006230000']),patch('urllib.request.urlopen',side_effect=error),patch('builtins.print'):
                self.assertEqual(main(),2)
            m=json.loads((out/'manifest.json').read_text())
            self.assertEqual((out/'response.raw').read_bytes(),raw)
            self.assertEqual(m['raw_sha256'],hashlib.sha256(raw).hexdigest())
            self.assertEqual(m['http_status'],429)
            with patch.object(sys,'argv',['probe','--output',str(out)]),self.assertRaises(FileExistsError): main()
    def test_transport_failure_does_not_fabricate_raw_hash(self):
        import tempfile,sys,urllib.error
        from pathlib import Path
        from unittest.mock import patch
        from gdelt_schema_probe import main
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'attempt'
            with patch.object(sys,'argv',['probe','--output',str(out)]),patch('urllib.request.urlopen',side_effect=urllib.error.URLError('synthetic failure')),patch('builtins.print'):
                self.assertEqual(main(),2)
            m=json.loads((out/'manifest.json').read_text())
            self.assertNotIn('raw_sha256',m)
            self.assertFalse((out/'response.raw').exists())

    def test_non_utf8_http_200_preserves_raw_manifest_and_blocks(self):
        import tempfile, sys, hashlib
        from pathlib import Path
        from unittest.mock import patch, Mock
        from gdelt_schema_probe import main
        raw = b'\xff\xfe synthetic invalid UTF-8'
        response = Mock(status=200, headers={'Content-Type': 'application/json'})
        response.read.return_value = raw
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'attempt'
            with patch.object(sys, 'argv', ['probe', '--output', str(out), '--end', '20261006230000']), patch('urllib.request.urlopen', return_value=response), patch('builtins.print'):
                self.assertEqual(main(), 2)
            manifest = json.loads((out / 'manifest.json').read_text())
            self.assertEqual(manifest['status'], 'SOURCE_QUALIFICATION_BLOCKED')
            self.assertEqual(manifest['error_type'], 'UnicodeDecodeError')
            self.assertEqual(manifest['http_status'], 200)
            self.assertEqual((out / 'response.raw').read_bytes(), raw)
            self.assertEqual(manifest['raw_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertFalse((out / 'normalized.json').exists())

    def test_http_429_preserves_network_completion_timestamp(self):
        import tempfile, sys, io, urllib.error
        from pathlib import Path
        from unittest.mock import patch
        from datetime import datetime, timedelta, timezone
        from gdelt_schema_probe import main
        from gdelt_schema_probe import UTC
        times = [datetime(2026,10,8,tzinfo=timezone.utc)+timedelta(seconds=i) for i in range(4)]
        error = urllib.error.HTTPError('https://example.com',429,'rate limit',{},io.BytesIO(b'429'))
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'attempt'
            with patch.object(sys,'argv',['probe','--output',str(out),'--end','20261006230000']), patch('urllib.request.urlopen',side_effect=error), patch('gdelt_schema_probe.datetime') as clock, patch('builtins.print'):
                clock.now.side_effect=times
                clock.strptime=datetime.strptime
                self.assertEqual(main(),2)
            manifest=json.loads((out/'manifest.json').read_text())
            self.assertEqual(manifest['request_started_at'], times[1].isoformat())
            self.assertEqual(manifest['retrieval_completed_at'], times[2].isoformat())
