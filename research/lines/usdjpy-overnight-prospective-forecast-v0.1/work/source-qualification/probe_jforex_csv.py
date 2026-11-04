#!/usr/bin/env python3
"""Inspect a fixed-schema, bounded JForex USDJPY export without analyzing market outcomes.

Inputs must be produced by JForexUsdJpyBoundedSource.java; generic widget CSV
formats have NOT been qualified. This program does not assert provider identity.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path

HEADER = ["timestamp_utc_ms", "bid", "ask", "bid_volume", "ask_volume", "instrument"]
START_MS = 1705323540000  # 2024-01-15T12:59:00Z
END_MS = 1705323660000    # 2024-01-15T13:01:00Z
MAX_BYTES = 20 * 1024 * 1024
MAX_ROWS = 100_000


def _utc_ms(value: int | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return "INVALID_EPOCH_MS"


def inspect(path: Path) -> dict:
    size = path.stat().st_size
    if size <= 0 or size > MAX_BYTES or path.suffix.lower() != ".csv":
        raise ValueError("input must be nonempty bounded .csv <= 20 MiB")
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    errors = {
        "malformed_row": 0, "wrong_instrument": 0, "invalid_timestamp": 0,
        "timestamp_outside_predeclared_window": 0, "invalid_bid_ask": 0,
        "crossed_ask_below_bid": 0, "invalid_volume": 0,
        "out_of_order_timestamps": 0,
    }
    total = 0
    duplicate_ms = 0
    seen_ms: set[int] = set()
    first_ms = last_ms = earliest_ms = latest_ms = prev_ms = None
    with path.open("r", encoding="utf-8", newline="") as stream:
        csv.field_size_limit(1024)
        reader = csv.reader(stream, strict=True)
        try:
            head = next(reader)
        except StopIteration:
            raise ValueError("missing header") from None
        if head != HEADER:
            raise ValueError("exact controlled JForex header required; generic CSV not qualified")
        for row in reader:
            total += 1
            if total > MAX_ROWS:
                raise ValueError("bounded sample exceeds 100000 rows")
            if len(row) != len(HEADER):
                errors["malformed_row"] += 1
                continue
            ts_str, bid_str, ask_str, bv_str, av_str, symbol = row
            if symbol != "USDJPY":
                errors["wrong_instrument"] += 1
            try:
                ms = int(ts_str)
                if str(ms) != ts_str:
                    raise ValueError("noncanonical integer")
            except ValueError:
                errors["invalid_timestamp"] += 1
                continue
            if not START_MS <= ms <= END_MS:
                errors["timestamp_outside_predeclared_window"] += 1
            if ms in seen_ms:
                duplicate_ms += 1
            seen_ms.add(ms)
            if prev_ms is not None and ms < prev_ms:
                errors["out_of_order_timestamps"] += 1
            prev_ms = ms
            first_ms = ms if first_ms is None else first_ms
            last_ms = ms
            earliest_ms = ms if earliest_ms is None else min(earliest_ms, ms)
            latest_ms = ms if latest_ms is None else max(latest_ms, ms)
            try:
                bid, ask, bv, av = (Decimal(v) for v in (bid_str, ask_str, bv_str, av_str))
                if not bid.is_finite() or not ask.is_finite() or bid <= 0 or ask <= 0:
                    errors["invalid_bid_ask"] += 1
                elif ask < bid:
                    errors["crossed_ask_below_bid"] += 1
                if not bv.is_finite() or not av.is_finite() or bv < 0 or av < 0:
                    errors["invalid_volume"] += 1
            except InvalidOperation:
                errors["malformed_row"] += 1
    if not total:
        status = "NO_TICKS_NOT_QUALIFIED"
    elif any(errors.values()):
        status = "BLOCKED_SOURCE_STRUCTURE"
    else:
        status = "STRUCTURE_PASS_SOURCE_GATE_STILL_BLOCKED"
    return {
        "record_type": "JFOREX_CONTROLLED_CSV_SOURCE_ONLY_RECEIPT_v0.1",
        "status": status,
        "scientific_effect": "NONE",
        "source_gate_passed": False,
        "market_outcome_access": "CLOSED",
        "formal_scoring": "NOT_AUTHORIZED",
        "provider_claim": "Dukascopy JForex history (declared; not independently verified)",
        "instrument_expected": "Instrument.USDJPY",
        "window_start_utc": _utc_ms(START_MS),
        "window_end_utc": _utc_ms(END_MS),
        "timestamp_semantics": "UTC epoch milliseconds from ITick.getTime() in controlled exporter",
        "schema": HEADER,
        "file_name": path.name,
        "compressed": False,
        "raw_byte_count": size,
        "raw_sha256": sha256,
        "decoded_record_count": total,
        "first_record_utc": _utc_ms(first_ms),
        "last_record_utc": _utc_ms(last_ms),
        "earliest_record_utc": _utc_ms(earliest_ms),
        "latest_record_utc": _utc_ms(latest_ms),
        "duplicate_timestamp_count": duplicate_ms,
        "counts": errors,
        "provider_session_verified": False,
        "acquisition_chain_of_custody_verified": False,
        "retention_license_reviewed": False,
        "reason": "CSV structure alone cannot establish authentic JForex origin, rights, or full endpoint coverage. No price changes, returns, direction or scores computed.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, type=Path)
    ap.add_argument("--receipt", required=True, type=Path)
    args = ap.parse_args()
    if args.receipt.exists():
        ap.error("receipt already exists: refuse overwrite")
    result = inspect(args.file)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "record_count": result["decoded_record_count"],
                      "source_gate_passed": False, "receipt": str(args.receipt)}))


if __name__ == "__main__":
    main()
