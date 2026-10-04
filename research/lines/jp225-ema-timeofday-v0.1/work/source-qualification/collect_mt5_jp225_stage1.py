"""Lightweight outcome-blind Stage 1 collector for XM MT5 JP225Cash.

Collects:
- warm-up + 2025 M1 bars only;
- a few fixed BID/ASK tick probe windows;
- non-sensitive terminal/server/symbol metadata;
- SHA-256 manifest.

It does NOT calculate EMA, signals, forward returns, P/L, or 2026 holdout outcomes.
Requires an already installed and logged-in MetaTrader 5 terminal on Windows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from stage1_contract import (SYMBOL, START, END, PROBES, SYMBOL_FIELDS,
                             allowlist, boundary_check, M1_FIELDS, TICK_FIELDS)

VERSION = "JP225_STAGE1_v0.2"
DEFAULT_SYMBOL = "JP225Cash"
DEFAULT_START = "2024-11-29T00:00:00"
DEFAULT_END = "2025-12-31T23:59:00"



def utc(text: str) -> datetime:
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_array(path: Path, arr: Any) -> int:
    fields = list(arr.dtype.names or [])
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for row in arr:
            w.writerow([
                row[name].item() if hasattr(row[name], "item") else row[name]
                for name in fields
            ])
    return len(arr)


def first_last_raw_time(arr: Any) -> dict[str, int | None]:
    if arr is None or len(arr) == 0:
        return {"first_time": None, "last_time": None}
    return {"first_time": int(arr[0]["time"]), "last_time": int(arr[-1]["time"])}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", choices=[SYMBOL], default=SYMBOL)
    ap.add_argument("--out", default="jp225_mt5_stage1")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)

    import MetaTrader5 as mt5

    if not mt5.initialize():
        raise SystemExit("MT5_INITIALIZE_FAILED")

    try:
        version = mt5.version()
        terminal = allowlist(mt5.terminal_info(), ('build', 'maxbars'))
        account = allowlist(mt5.account_info(), ('server',))

        if not mt5.symbol_select(args.symbol, True):
            candidates = [
                s.name for s in (mt5.symbols_get() or [])
                if "JP225" in s.name.upper()
            ]
            raise RuntimeError(
                f"Exact symbol {args.symbol!r} unavailable. "
                f"JP225-like symbols visible={candidates!r}. "
                "No automatic substitution performed."
            )

        symbol_info = allowlist(mt5.symbol_info(args.symbol), SYMBOL_FIELDS)
        if symbol_info["name"] != SYMBOL:
            raise RuntimeError("EXACT_SYMBOL_IDENTITY_FAILED")

        start, end = utc(DEFAULT_START), utc(DEFAULT_END)
        rates = mt5.copy_rates_range(args.symbol, mt5.TIMEFRAME_M1, start, end)
        if rates is None:
            raise RuntimeError("M1_ACQUISITION_FAILED")
        boundary_check(rates)
        if tuple(rates.dtype.names or ()) != M1_FIELDS:
            raise RuntimeError("M1_SCHEMA_FAILURE")

        m1_path = out / "m1_warmup_2025_raw.csv"
        m1_rows = write_array(m1_path, rates)

        probe_path = out / "tick_probes_raw.csv"
        probe_meta = []
        header_written = False
        with probe_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            tick_fields: list[str] | None = None
            for probe_id, start_s, end_s in PROBES:
                ticks = mt5.copy_ticks_range(
                    args.symbol, utc(start_s), utc(end_s), mt5.COPY_TICKS_ALL
                )
                if ticks is None:
                    raise RuntimeError(
                        "TICK_PROBE_ACQUISITION_FAILED"
                    )
                boundary_check(ticks, tick=True)
                if tuple(ticks.dtype.names or ()) != TICK_FIELDS:
                    raise RuntimeError("TICK_SCHEMA_FAILURE")
                fields = list(ticks.dtype.names or [])
                if tick_fields is None:
                    tick_fields = fields
                elif fields != tick_fields:
                    raise RuntimeError("tick schema changed between fixed probes")
                if not header_written:
                    writer.writerow(["probe_id", *fields])
                    header_written = True
                for row in ticks:
                    writer.writerow([
                        probe_id,
                        *[
                            row[name].item() if hasattr(row[name], "item") else row[name]
                            for name in fields
                        ],
                    ])
                probe_meta.append({
                    "probe_id": probe_id,
                    "request_start": start_s,
                    "request_end": end_s,
                    "rows": len(ticks),
                    **first_last_raw_time(ticks),
                })

        metadata = {
            "collector_version": VERSION,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "strategy_outcomes_calculated": False,
            "holdout_2026_requested": False,
            "request_time_convention": "UTC_datetimes_per_MT5_Python_API",
            "returned_timestamp_semantics": "UNVERIFIED_PRESERVE_RAW_INTEGER_TIME",
            "mt5_version": version,
            "package_version": mt5.__version__,
            "collector_sha256": sha256_file(Path(__file__)),
            "contract_sha256": sha256_file(Path(__file__).with_name("stage1_contract.py")),
            "bar_price_identity": "UNKNOWN",
            "source_review": None,
            "terminal": terminal,
            "account": {
                "server": account.get("server"),
            },
            "symbol": symbol_info,
            "m1_request": {
                "start": DEFAULT_START,
                "end_inclusive": DEFAULT_END,
                "rows": m1_rows,
                **first_last_raw_time(rates),
            },
            "tick_probes": probe_meta,
        }
        meta_path = out / "metadata.json"
        meta_path.write_text(
            json.dumps(metadata, indent=2, default=str), encoding="utf-8"
        )

        manifest = {}
        for p in (m1_path, probe_path, meta_path):
            manifest[p.name] = {
                "sha256": sha256_file(p),
                "bytes": p.stat().st_size,
            }
        manifest_path = out / "sha256_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        print(json.dumps({
            "status": "STAGE1_RAW_COLLECTION_COMPLETE",
            "m1_rows": m1_rows,
            "tick_probe_rows": sum(p["rows"] for p in probe_meta),
            "holdout_2026_requested": False,
            "strategy_outcomes_calculated": False,
        }, indent=2))
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        code = str(exc) if isinstance(exc, ValueError) and str(exc) in ("BOUNDARY_VIOLATION", "TIMESTAMP_IDENTITY_VIOLATION") else "COLLECTION_FAILED"
        print(json.dumps({"status": "FAIL", "violation": code, "strategy_outcomes_calculated": False}))
        raise SystemExit("Preserve partial directory locally; do not use it for research") from None
