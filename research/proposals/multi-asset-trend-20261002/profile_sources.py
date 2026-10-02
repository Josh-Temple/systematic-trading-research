"""Profile official ETF history only; never calculate signals or strategy outcomes.

Raw downloads remain in the user-selected directory, outside Git history.
Only schema, coverage, missingness and source hashes enter the manifest.
"""
import argparse
import collections
import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

SOURCES = {
    "1306": "https://www.nomura-am.co.jp/fund/etf/history/ETF_1306.csv",
    "2510": "https://www.nomura-am.co.jp/fund/etf/history/ETF_2510.csv",
    "2511": "https://www.nomura-am.co.jp/fund/etf/history/ETF_2511.csv",
    "2513": "https://www.nomura-am.co.jp/fund/etf/history/ETF_2513.csv",
    "1540": "https://kikinzoku.tr.mufg.jp/ja/data_report/historicaldata/main/01/teaserItems1/0/linkList/0/link/gold.zip",
}

def profile_csv(raw):
    for enc in ("utf-8-sig", "cp932", "utf-16"):
        try:
            content = raw.decode(enc)
            break
        except UnicodeError:
            continue
    else:
        raise ValueError("No supported encoding")
    rows = list(csv.reader(io.StringIO(content)))
    dated = []
    for i, row in enumerate(rows):
        if not row:
            continue
        value = row[0].strip()
        for fmt in ("%Y%m%d", "%Y/%m/%d", "%Y-%m-%d"):
            try:
                date = dt.datetime.strptime(value, fmt).date()
                dated.append((i, date, row))
                break
            except ValueError:
                pass
    if not dated:
        return {"encoding": enc, "csv_rows": len(rows), "date_detection": "UNRESOLVED", "preamble": rows[:6]}
    start = dated[0][0]
    width = max(len(r) for _, _, r in dated)
    dates = [d for _, d, _ in dated]
    counts = collections.Counter(dates)
    data = [r for _, _, r in dated]
    return {
        "encoding": enc, "csv_rows": len(rows), "dated_rows": len(dated),
        "date_min": min(dates).isoformat(), "date_max": max(dates).isoformat(),
        "duplicate_date_rows": sum(n - 1 for n in counts.values()),
        "exact_duplicate_rows": len(data) - len({tuple(r) for r in data}),
        "out_of_order_transitions": sum(b < a for a, b in zip(dates, dates[1:])),
        "future_date_rows": sum(d > dt.datetime.now(dt.timezone.utc).date() for d in dates),
        "weekend_rows": sum(d.weekday() >= 5 for d in dates),
        "weekend_dates": [d.isoformat() for d in dates if d.weekday() >= 5],
        "outage_2020_10_01_present": dt.date(2020, 10, 1) in counts,
        "nonempty_unparsed_rows_after_first_date": sum(bool(r) and any(c.strip() for c in r) for r in rows[start:]) - len(dated),
        "column_count": width, "header_candidates": rows[max(0, start - 3):start],
        "row_width_counts": dict(collections.Counter(len(r) for r in data)),
        "blank_by_column": [sum(j >= len(r) or not r[j].strip() for r in data) for j in range(width)],
        "numeric_quality_by_column": [numeric_quality(data, j) for j in range(1, width)],
        "calendar_completeness": "UNVERIFIED: trading calendar not joined",
        "point_in_time_vintage": "UNVERIFIED: current retrospective export",
    }

def numeric_quality(rows, j):
    from decimal import Decimal, InvalidOperation
    valid, invalid, nonfinite, nonpositive = 0, 0, 0, 0
    for row in rows:
        if j >= len(row) or not row[j].strip():
            continue
        try:
            n = Decimal(row[j].replace(',', '').strip())
            if not n.is_finite():
                nonfinite += 1
            else:
                valid += 1
                nonpositive += n <= 0
        except InvalidOperation:
            invalid += 1
    return {"column_index": j, "finite_numeric": valid, "invalid_numeric": invalid,
            "nonfinite": nonfinite, "nonpositive": nonpositive}

def fetch(code, url, directory, offline=False):
    result = {"instrument": code, "url": url, "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        path = directory / (code + (".zip" if url.endswith('.zip') else '.csv'))
        if offline:
            raw = path.read_bytes()
            result.update(retrieved_at_utc=None, mode="OFFLINE_REPROFILE")
        else:
            with urllib.request.urlopen(url, timeout=40) as response:
                raw = response.read(10_000_001)
                result.update(final_url=response.url, content_type=response.headers.get('Content-Type'))
        if len(raw) > 10_000_000:
            raise ValueError("Download exceeds 10 MB bound")
        result.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), status="FETCHED")
        if not offline:
            path.write_bytes(raw)
        if url.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                result['members'] = []
                for item in archive.infolist():
                    if item.is_dir():
                        continue
                    if item.file_size > 10_000_000:
                        raise ValueError("ZIP member exceeds 10 MB bound")
                    member = archive.read(item)
                    result['members'].append({"name": item.filename, "bytes": len(member),
                        "sha256": hashlib.sha256(member).hexdigest(),
                        "profile": profile_csv(member) if item.filename.lower().endswith('.csv') else {"status": "NON_CSV_UNPROFILED"}})
        else:
            result['profile'] = profile_csv(raw)
    except Exception as error:
        result.update(status="FAILED", error=f"{type(error).__name__}: {error}")
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--offline', action='store_true', help='Profile previously saved bytes without downloading')
    args = parser.parse_args()
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(lambda pair: fetch(*pair, args.raw_dir, args.offline), SOURCES.items()))
    manifest = {"scope": "SOURCE_QUALIFICATION_ONLY", "scientific_status": "NOT_APPLICABLE",
                "strategy_outcomes_computed": False, "sources": results}
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if any(r['status'] != 'FETCHED' for r in results):
        raise SystemExit(1)
