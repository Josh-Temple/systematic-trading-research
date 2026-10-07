#!/usr/bin/env python3
"""Outcome-blind DOC API qualification; preserve bytes before interpreting them.

No publisher body, market prices, classification or strategy outcome is fetched.
This is a source probe, NEVER an authorization to issue a formal event.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = 'https://api.gdeltproject.org/api/v2/doc/doc'
QUERY = '(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english'
QUERY_ID = 'FXNS-DOC-QUERY-v01-candidate'
MAXRECORDS = 250
UTC = timezone.utc


def stamp(dt):
    if dt.tzinfo is None:
        raise ValueError('aware timestamp required')
    return dt.astimezone(UTC).strftime('%Y%m%d%H%M%S')


def parameters(start, end, limit=MAXRECORDS):
    if end - start != timedelta(hours=24):
        raise ValueError('exact 24-hour window required')
    if not 1 <= limit <= MAXRECORDS:
        raise ValueError('invalid MAXRECORDS')
    return dict(query=QUERY, mode='artlist', maxrecords=str(limit),
                startdatetime=stamp(start), enddatetime=stamp(end),
                sort='dateasc', format='json')


def title_key(title):
    # Conservative normalized equality, NOT fuzzy semantic similarity.
    return ' '.join(unicodedata.normalize('NFKC', title).casefold().split())


def normalize(raw, start, end, limit):
    payload = json.loads(raw.decode('utf-8'))
    if not isinstance(payload, dict) or not isinstance(payload.get('articles'), list):
        raise ValueError('expected explicit articles array; missing is not an empty event')
    articles = payload['articles']
    if len(articles) >= limit:
        raise ValueError('MAXRECORDS reached before deduplication; completeness unresolved')
    records = []
    for row in articles:
        if not isinstance(row, dict):
            raise ValueError('invalid article')
        for key in ('url', 'title', 'seendate', 'domain', 'language'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError('missing field: ' + key)
        if row['language'].casefold() != 'english':
            raise ValueError('non-English result')
        if not re.fullmatch(r'\d{8}T\d{6}Z', row['seendate']):
            raise ValueError('unexpected DOC seendate format')
        seen = datetime.strptime(row['seendate'], '%Y%m%dT%H%M%SZ').replace(tzinfo=UTC)
        # Conservative open endpoints until runtime inclusivity is established.
        if not start < seen < end:
            raise ValueError('boundary/out-of-window seendate; qualification required')
        url = urllib.parse.urlsplit(row['url'])
        if url.scheme not in ('http', 'https') or not url.hostname:
            raise ValueError('invalid URL')
        if url.hostname.casefold().removeprefix('www.') != row['domain'].casefold().removeprefix('www.'):
            raise ValueError('domain/URL mismatch')
        records.append(dict(url=row['url'], title=row['title'],
                            gdelt_seen_at=seen.isoformat(), source_domain=row['domain']))
    # Stable keeper independent of response ordering. Preserve every raw duplicate.
    records.sort(key=lambda r: (r['gdelt_seen_at'], r['url'], r['title']))
    result, removed, urls, titles = [], [], set(), set()
    for r in records:
        key = title_key(r['title'])
        cause = 'EXACT_URL' if r['url'] in urls else 'NORMALIZED_TITLE' if key in titles else None
        urls.add(r['url']); titles.add(key)
        if cause:
            removed.append(dict(url=r['url'], reason=cause))
        else:
            r['record_id'] = hashlib.sha256(r['url'].encode('utf-8')).hexdigest()
            result.append(r)
    return dict(article_count=len(articles), retained_count=len(result),
                article_keys=sorted(set().union(*(r.keys() for r in articles))) if articles else [],
                records=result, excluded=removed,
                completeness='UNVERIFIED_EVEN_BELOW_CAP',
                boundary_semantics='UNVERIFIED_CONSERVATIVE_OPEN_ENDPOINTS')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='gdelt_probe')
    p.add_argument('--end', help='UTC YYYYMMDDHHMMSS; default most recent 08:00 JST cutoff')
    p.add_argument('--maxrecords', type=int, default=MAXRECORDS)
    a = p.parse_args()
    now = datetime.now(UTC)
    end = datetime.strptime(a.end, '%Y%m%d%H%M%S').replace(tzinfo=UTC) if a.end else now.replace(hour=23, minute=0, second=0, microsecond=0)
    if not a.end and end > now:
        end -= timedelta(days=1)
    start = end - timedelta(hours=24)
    params = parameters(start, end, a.maxrecords)
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=False)  # Never overwrite a prior attempt.
    url = API + '?' + urllib.parse.urlencode(params)
    m = dict(query_id=QUERY_ID, parameters=params, request_url=url,
             request_started_at=datetime.now(UTC).isoformat(), start_utc=start.isoformat(),
             end_utc=end.isoformat(), market_outcomes_accessed=False,
             formal_cohort_authorized=False, attribution='Source: GDELT Project (https://www.gdeltproject.org/). Original publishers identified by article URLs.')
    raw = None
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'systematic-trading-research-source-probe/0.2'})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                m.update(http_status=response.status, response_headers=dict(response.headers))
        except urllib.error.HTTPError as error:
            raw = error.read()
            m.update(http_status=error.code, response_headers=dict(error.headers))
        m['retrieval_completed_at'] = datetime.now(UTC).isoformat()
        (out / 'response.raw').write_bytes(raw)
        m.update(raw_path='response.raw', raw_bytes=len(raw), raw_sha256=hashlib.sha256(raw).hexdigest())
        if m['http_status'] != 200:
            raise ValueError('HTTP_NON_SUCCESS')
        summary = normalize(raw, start, end, a.maxrecords)
        (out / 'normalized.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        m.update(status='SCHEMA_PROBE_PASS_SOURCE_NOT_QUALIFIED',
                 article_count=summary['article_count'], article_keys=summary['article_keys'])
    except (ValueError, OSError, urllib.error.URLError) as error:
        m.update(status='SOURCE_QUALIFICATION_BLOCKED', error_type=type(error).__name__, error=str(error),
                 retrieval_completed_at=datetime.now(UTC).isoformat())
    (out / 'manifest.json').write_text(json.dumps(m, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in m.items() if k not in ('response_headers',)}, indent=2))
    return 0 if m['status'] == 'SCHEMA_PROBE_PASS_SOURCE_NOT_QUALIFIED' else 2

if __name__ == '__main__':
    raise SystemExit(main())
