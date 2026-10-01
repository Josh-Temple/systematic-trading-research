#!/usr/bin/env python3
"""Bounded ECB metadata-only probe for 2009-11; never emits OBS_VALUE values.

The raw response is saved byte-for-byte as a local source snapshot. The script emits
only dates, status, dimensions, safe series metadata, response sizes and hashes.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import csv
import hashlib
import io
import json
import sys

CURRENCIES = ("AUD", "CAD", "CHF", "GBP", "JPY", "NZD", "USD")
DECIMALS = {"AUD": "4", "CAD": "4", "CHF": "4", "GBP": "5", "JPY": "2", "NZD": "4", "USD": "4"}
START = "2009-11-01"
END = "2009-11-30"
BASE = "https://data-api.ecb.europa.eu/service/data/EXR/D.{ccy}.EUR.SP00.A?startPeriod=2009-11-01&endPeriod=2009-11-30&format=csvdata"
EXPECTED_SCHEMA = ["KEY", "FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX", "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_CONF", "OBS_PRE_BREAK", "OBS_COM", "TIME_FORMAT", "BREAKS", "COLLECTION", "COMPILING_ORG", "DISS_ORG", "DOM_SER_IDS", "PUBL_ECB", "PUBL_MU", "PUBL_PUBLIC", "UNIT_INDEX_BASE", "COMPILATION", "COVERAGE", "DECIMALS", "NAT_TITLE", "SOURCE_AGENCY", "SOURCE_PUB", "TITLE", "TITLE_COMPL", "UNIT", "UNIT_MULT"]


def fetch_one(ccy: str, expected_dates: list[str]) -> dict:
    url = BASE.format(ccy=ccy)
    request = Request(url, headers={"Accept": "text/csv", "User-Agent": "csm-source-qualification/1.0"})
    try:
        with urlopen(request, timeout=40) as response:
            body = response.read(1_000_001)
            status = response.status
            headers = response.headers
            final_url = response.geturl()
        if len(body) > 1_000_000:
            return {"series": f"D.{ccy}.EUR.SP00.A", "error": "RESPONSE_OVER_1MB"}
        reader = csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
        schema = list(reader.fieldnames or [])
        rows = list(reader)
        dates = [row.get("TIME_PERIOD", "") for row in rows]
        unique_dates = sorted(set(d for d in dates if d))
        statuses = sorted({(row.get("OBS_STATUS") or "").strip() or "UNMARKED" for row in rows})
        dim_fields = ("FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX")
        dimensions = {field: sorted({row.get(field, "") for row in rows if row.get(field)}) for field in dim_fields}
        safe_meta_fields = ("UNIT", "UNIT_MULT", "DECIMALS", "TITLE", "TITLE_COMPL", "SOURCE_AGENCY", "SOURCE_PUB", "COMPILING_ORG", "DISS_ORG", "COLLECTION", "COVERAGE")
        series_metadata = {field: sorted({row.get(field, "") for row in rows if row.get(field)}) for field in safe_meta_fields}
        snapshot_dir = Path(__file__).with_name("probe-snapshot")
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot_path = snapshot_dir / f"ECB_EXR_D_{ccy}_EUR_SP00_A_2009-11.csv"
        body_sha = hashlib.sha256(body).hexdigest()
        if snapshot_path.exists():
            if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != body_sha:
                return {"series": f"D.{ccy}.EUR.SP00.A", "error": "EXISTING_SNAPSHOT_HASH_MISMATCH"}
        else:
            snapshot_path.write_bytes(body)
        result = {
            "series": f"D.{ccy}.EUR.SP00.A",
            "request_url": url,
            "final_url": final_url,
            "http_status": status,
            "content_type": headers.get("Content-Type", "").split(";")[0],
            "http_date": headers.get("Date"),
            "etag": headers.get("ETag"),
            "last_modified": headers.get("Last-Modified"),
            "cache_control": headers.get("Cache-Control"),
            "response_bytes": len(body),
            "response_sha256": body_sha,
            "snapshot_path": str(snapshot_path.relative_to(Path(__file__).parent)),
            "row_count": len(rows),
            "date_count": len(unique_dates),
            "duplicate_date_rows": len(dates) - len(unique_dates),
            "first_date": unique_dates[0] if unique_dates else None,
            "last_date": unique_dates[-1] if unique_dates else None,
            "dates": unique_dates,
            "dates_sha256": hashlib.sha256("\n".join(unique_dates).encode("utf-8")).hexdigest(),
            "status_codes": statuses,
            "dimensions": dimensions,
            "series_metadata": series_metadata,
            "schema": schema,
            "obs_value_column_present": "OBS_VALUE" in schema,
            "obs_value_values_extracted_or_used": False,
            "obs_value_values_emitted": False,
            "raw_snapshot_byte_exact": True,
            "matches_expected_dates": unique_dates == expected_dates,
            "matches_identity_metadata": (
                dimensions.get("FREQ") == ["D"]
                and dimensions.get("CURRENCY") == [ccy]
                and dimensions.get("CURRENCY_DENOM") == ["EUR"]
                and dimensions.get("EXR_TYPE") == ["SP00"]
                and dimensions.get("EXR_SUFFIX") == ["A"]
                and series_metadata.get("UNIT") == [ccy]
                and series_metadata.get("UNIT_MULT") == ["0"]
                and series_metadata.get("DECIMALS") == [DECIMALS[ccy]]
                and series_metadata.get("SOURCE_AGENCY") == ["4F0"]
            ),
        }
        return result
    except HTTPError as exc:
        return {"series": f"D.{ccy}.EUR.SP00.A", "error": "HTTP_ERROR", "http_status": exc.code}
    except URLError as exc:
        return {"series": f"D.{ccy}.EUR.SP00.A", "error": "URL_ERROR", "reason_type": type(exc.reason).__name__}
    except Exception as exc:
        return {"series": f"D.{ccy}.EUR.SP00.A", "error": type(exc).__name__}


def main() -> int:
    calendar_path = Path(__file__).with_name("expected-calendar.json")
    calendar_bytes = calendar_path.read_bytes()
    calendar = json.loads(calendar_bytes)
    expected_dates = [d for d in calendar["expected_open_dates"] if d.startswith("2009-11-")]
    with ThreadPoolExecutor(max_workers=7) as pool:
        rows = list(pool.map(lambda ccy: fetch_one(ccy, expected_dates), CURRENCIES))
    complete = (
        len(rows) == 7
        and all(x.get("http_status") == 200 for x in rows)
        and all(x.get("row_count") == 21 for x in rows)
        and all(x.get("duplicate_date_rows") == 0 for x in rows)
        and all(x.get("dates") == expected_dates for x in rows)
        and all(x.get("status_codes") == ["A"] for x in rows)
        and all(x.get("schema") == EXPECTED_SCHEMA for x in rows)
        and all(x.get("matches_expected_dates") is True for x in rows)
        and all(x.get("matches_identity_metadata") is True for x in rows)
    )
    output = {
        "probe_id": "CSM-C-PROBE-2009-11",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "bounded_period": {"start": START, "end": END},
        "data_values_visible": False,
        "expected_calendar_path": calendar_path.name,
        "expected_calendar_sha256": hashlib.sha256(calendar_bytes).hexdigest(),
        "expected_probe_dates": expected_dates,
        "all_series_match_expected_calendar_and_schema": complete,
        "raw_snapshots_stored_byte_exact": all(x.get("raw_snapshot_byte_exact") is True for x in rows),
        "series": rows,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if complete else 2


if __name__ == "__main__":
    sys.exit(main())
