#!/usr/bin/env python3
"""Acquire first-party BID M1 source without generating touches or outcomes.

This is a source inventory, not the H3 structural gate or a research run.
The final trading-hours convention and Tick source gate are checked separately.
Raw responses are stored unchanged and never overwritten. Repeated executions
verify existing bytes and produce a new manifest instead of silently replacing
previous source identities.
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


BASE = "https://jetta.dukascopy.com/v1/candles/minute/XAU-USD/BID"
UTC = timezone.utc


def decode_m1(payload: dict) -> list[dict]:
    """Use the exact M1 delta decoding in the recovered legacy run_v01.py."""
    mult = float(payload.get("multiplier") or 1)
    scale = 1 if mult >= 1 else 10 ** abs(math.floor(math.log10(mult)))
    stamp = int(payload.get("timestamp") or 0)
    shift = int(payload.get("shift") or 1)
    values = {key: payload.get(key) or [] for key in ("times", "opens", "highs", "lows", "closes")}
    if len({len(value) for value in values.values()}) != 1:
        raise ValueError("inconsistent_m1_lengths")
    o, h, l, c = (float(payload.get(key) or 0) for key in ("open", "high", "low", "close"))
    rows = []
    for i, delta in enumerate(values["times"]):
        stamp += shift * int(delta)
        o = math.floor((o + float(values["opens"][i]) * mult) * scale + 0.5) / scale
        h = math.floor((h + float(values["highs"][i]) * mult) * scale + 0.5) / scale
        l = math.floor((l + float(values["lows"][i]) * mult) * scale + 0.5) / scale
        c = math.floor((c + float(values["closes"][i]) * mult) * scale + 0.5) / scale
        rows.append({"ts": stamp, "o": o, "h": h, "l": l, "c": c})
    return rows


def inspect(raw: bytes, day: date) -> dict:
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("m1_payload_not_object")
    rows = decode_m1(payload)
    start = datetime.combine(day, datetime.min.time(), UTC).timestamp() * 1000
    end = start + 86_400_000
    problems = []
    if not rows:
        problems.append("empty_m1")
    if any(not start <= row["ts"] < end for row in rows):
        problems.append("timestamp_outside_utc_date")
    if any(row["ts"] >= rows[i + 1]["ts"] for i, row in enumerate(rows[:-1])):
        problems.append("duplicate_or_reversed_timestamp")
    if any(row["ts"] % 60_000 != 0 for row in rows):
        problems.append("nonminute_timestamp")
    if any(
        not all(math.isfinite(row[key]) for key in ("o", "h", "l", "c"))
        or row["h"] < row["l"]
        or not row["l"] <= row["o"] <= row["h"]
        or not row["l"] <= row["c"] <= row["h"]
        for row in rows
    ):
        problems.append("invalid_ohlc")
    return {
        "row_count": len(rows),
        "first_timestamp_utc": datetime.fromtimestamp(rows[0]["ts"] / 1000, UTC).isoformat() if rows else None,
        "last_timestamp_utc": datetime.fromtimestamp(rows[-1]["ts"] / 1000, UTC).isoformat() if rows else None,
        "field_identity": list(payload.keys()),
        "basic_validation": "PASS" if not problems else "FAIL",
        "basic_validation_reasons": problems,
        "structural_eligibility": "HOLD_TRADING_HOURS_GATE_NOT_APPLIED",
    }


def acquire(day: date, root: Path) -> dict:
    url = f"{BASE}/{day.year}/{day.month}/{day.day}"
    path = root / "raw_m1" / f"{day.isoformat()}.json"
    retrieved = None
    if path.exists():
        raw = path.read_bytes()
        origin = "EXISTING_READBACK"
        prior_manifest = root / "m1_source_manifest.json"
        if prior_manifest.exists():
            for previous in json.loads(prior_manifest.read_text(encoding="utf-8")).get("records", []):
                if previous.get("date") == day.isoformat() and previous.get("sha256") == hashlib.sha256(raw).hexdigest():
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
                    return {"date": day.isoformat(), "url": url, "status": "HOLD_FETCH", "error": str(exc)}
                time.sleep(1 + attempt)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            origin = "NEW_DOWNLOAD"
        except FileExistsError:
            # Another process may have written the file. Do not replace it.
            raw = path.read_bytes()
            origin = "CONCURRENT_EXISTING_READBACK"
    digest = hashlib.sha256(raw).hexdigest()
    record = {
        "date": day.isoformat(), "url": url, "relative_path": f"raw_m1/{day.isoformat()}.json",
        "retrieved_at_utc": retrieved, "origin": origin, "byte_count": len(raw), "sha256": digest,
        "readback_sha256_matches": hashlib.sha256(path.read_bytes()).hexdigest() == digest,
    }
    try:
        record.update(inspect(raw, day))
        record["status"] = "SOURCE_RECORDED" if record["basic_validation"] == "PASS" else "HOLD_VALIDATION"
    except (ValueError, KeyError, TypeError, OverflowError) as exc:
        record.update(status="HOLD_VALIDATION", error=str(exc), structural_eligibility="HOLD")
    return record


def weekdays(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1) if (start + timedelta(days=i)).weekday() < 5]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--through", required=True, type=date.fromisoformat, help="Latest fully completed UTC date")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    start = date(2026, 7, 10)
    if args.through < start or args.through >= datetime.now(UTC).date():
        parser.error("through must be a past UTC date on or after 2026-07-10")
    dates = weekdays(start, args.through)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(acquire, day, args.output): day for day in dates}
        records = [future.result() for future in as_completed(futures)]
    records.sort(key=lambda item: item["date"])
    manifest = {
        "scope": "H3_OUTCOME_BLIND_M1_SOURCE_INVENTORY",
        "source_provider": "Dukascopy first-party JETTA BID M1 XAU-USD UTC",
        "candidate_start": start.isoformat(), "latest_candidate_date_checked": args.through.isoformat(),
        "calendar_candidate_count": len(dates), "structurally_eligible_count": None,
        "frozen_selected_count": 0, "outcome_computed": False,
        "confirmation_outcome_comparison": False, "bootstrap_run": False,
        "protocol_changed": False, "parameter_search": False, "sample_reselection": False,
        "source_gate": "NOT_EVALUATED", "current_state": "WAITING_FOR_MATURITY",
        "records": records,
    }
    target = args.output / "m1_source_manifest.json"
    target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_weekdays": len(dates), "recorded": sum(r["status"] == "SOURCE_RECORDED" for r in records), "hold": sum(r["status"] != "SOURCE_RECORDED" for r in records), "manifest": str(target)}))


if __name__ == "__main__":
    main()
