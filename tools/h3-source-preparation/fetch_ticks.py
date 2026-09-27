#!/usr/bin/env python3
"""Persist complete UTC-day first-party Tick buckets, without touch lookup.

This inventory never chooses hours from events or computes any H3 outcome.
It does not declare the M1/Tick source gate PASS.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


UTC = timezone.utc
BASE = "https://jetta.dukascopy.com/v1/ticks/XAU-USD"


def inspect(raw: bytes, day: date, hour: int) -> dict:
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("tick_payload_not_object")
    times = payload.get("times") or []
    asks = payload.get("asks") or []
    bids = payload.get("bids") or []
    if not (len(times) == len(asks) == len(bids)):
        raise ValueError("inconsistent_tick_lengths")
    multiplier = float(payload.get("multiplier") or 1)
    stamp = int(payload.get("timestamp") or 0)
    ask = float(payload.get("ask") or 0)
    bid = float(payload.get("bid") or 0)
    first = last = None
    reversed_count = duplicate_count = invalid_quote_count = nonpositive_spread_count = outside_hour_count = 0
    start = datetime(day.year, day.month, day.day, hour, tzinfo=UTC).timestamp() * 1000
    for delta, ask_delta, bid_delta in zip(times, asks, bids):
        previous = stamp
        stamp += int(delta)
        ask = round(ask + float(ask_delta) * multiplier, 10)
        bid = round(bid + float(bid_delta) * multiplier, 10)
        if first is None:
            first = stamp
        else:
            reversed_count += stamp < previous
            duplicate_count += stamp == previous
        last = stamp
        invalid_quote_count += not (math.isfinite(ask) and math.isfinite(bid))
        nonpositive_spread_count += ask <= bid
        outside_hour_count += not start <= stamp < start + 3_600_000
    problems = []
    if reversed_count or outside_hour_count or invalid_quote_count or nonpositive_spread_count:
        problems.append("invalid_tick_time_or_quote")
    return {
        "quote_count": len(times), "field_identity": list(payload.keys()),
        "first_timestamp_utc": datetime.fromtimestamp(first / 1000, UTC).isoformat() if first else None,
        "last_timestamp_utc": datetime.fromtimestamp(last / 1000, UTC).isoformat() if last else None,
        "duplicate_timestamp_count": duplicate_count,
        "reversed_timestamp_count": reversed_count,
        "invalid_bid_ask_count": invalid_quote_count,
        "nonpositive_spread_count": nonpositive_spread_count,
        "outside_hour_count": outside_hour_count,
        "json_and_quote_validation": "PASS" if not problems else "FAIL",
        "validation_reasons": problems,
    }


def acquire(day: date, hour: int, root: Path) -> dict:
    url = f"{BASE}/{day.year}/{day.month}/{day.day}/{hour}"
    path = root / "raw_tick" / day.isoformat() / f"{hour:02d}.json"
    retrieved = None
    if path.exists():
        raw = path.read_bytes()
        origin = "EXISTING_READBACK"
        prior_manifest = root / f"tick_source_manifest_{day.isoformat()}.json"
        if prior_manifest.exists():
            for previous in json.loads(prior_manifest.read_text(encoding="utf-8")).get("records", []):
                if previous.get("hour") == hour and previous.get("sha256") == hashlib.sha256(raw).hexdigest():
                    retrieved = previous.get("retrieved_at_utc")
                    break
    else:
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "h3-source-preparation/1"}), timeout=45) as response:
                    raw = response.read()
                retrieved = datetime.now(UTC).isoformat()
                break
            except (TimeoutError, urllib.error.URLError) as exc:
                if attempt == 2:
                    return {"date": day.isoformat(), "hour": hour, "url": url, "status": "HOLD_FETCH", "error": str(exc)}
                time.sleep(1 + attempt)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            origin = "NEW_DOWNLOAD"
        except FileExistsError:
            raw = path.read_bytes()
            origin = "CONCURRENT_EXISTING_READBACK"
    digest = hashlib.sha256(raw).hexdigest()
    record = {
        "date": day.isoformat(), "hour": hour, "url": url,
        "relative_path": f"raw_tick/{day.isoformat()}/{hour:02d}.json",
        "retrieved_at_utc": retrieved, "origin": origin,
        "byte_count": len(raw), "sha256": digest,
        "readback_sha256_matches": hashlib.sha256(path.read_bytes()).hexdigest() == digest,
    }
    try:
        record.update(inspect(raw, day, hour))
        record["status"] = "SOURCE_RECORDED" if record["json_and_quote_validation"] == "PASS" else "HOLD_VALIDATION"
    except (ValueError, KeyError, TypeError, OverflowError) as exc:
        record.update(status="HOLD_VALIDATION", error=str(exc))
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--date", type=date.fromisoformat)
    scope.add_argument("--through", type=date.fromisoformat, help="Inventory weekdays from 2026-07-10")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    first = date(2026, 7, 10)
    end = args.date or args.through
    if end < first or end >= datetime.now(UTC).date():
        parser.error("scope must be completed UTC dates from 2026-07-10 onward")
    days = ([args.date] if args.date else [first + timedelta(days=i) for i in range((end - first).days + 1) if (first + timedelta(days=i)).weekday() < 5])
    if args.date and args.date.weekday() >= 5:
        parser.error("date must be a UTC weekday")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(acquire, day, hour, args.output) for day in days for hour in range(24)]
        records = [future.result() for future in as_completed(futures)]
    records.sort(key=lambda item: (item["date"], item["hour"]))
    for day in days:
        subset = [record for record in records if record["date"] == day.isoformat()]
        manifest = {
            "scope": "H3_OUTCOME_BLIND_FULL_DAY_TICK_SOURCE_INVENTORY",
            "date": day.isoformat(), "source_provider": "Dukascopy first-party JETTA BID/ASK Tick XAU-USD UTC",
            "hours_requested": 24, "source_gate": "NOT_EVALUATED",
            "outcome_computed": False, "confirmation_outcome_comparison": False,
            "bootstrap_run": False, "records": subset,
        }
        target = args.output / f"tick_source_manifest_{day.isoformat()}.json"
        target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"days": len(days), "hours_requested": len(records), "recorded": sum(r["status"] == "SOURCE_RECORDED" for r in records), "hold": sum(r["status"] != "SOURCE_RECORDED" for r in records), "empty_buckets": sum(r.get("quote_count") == 0 for r in records)}))


if __name__ == "__main__":
    main()
