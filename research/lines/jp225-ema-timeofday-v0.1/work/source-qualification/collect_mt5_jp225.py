"""Outcome-blind XM MT5 JP225Cash raw-history collector.

Requires:
    pip install MetaTrader5

Run only with an already installed/logged-in local MetaTrader 5 terminal.
The script does not accept or persist credentials and does not calculate strategy outcomes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import MetaTrader5 as mt5

COLLECTOR_VERSION = "JP225_SOURCE_COLLECTOR_v0.1"
DEFAULT_SYMBOL = "JP225Cash"
DEFAULT_START = "2024-11-29T00:00:00"
DEFAULT_END = "2026-10-02T00:00:00"


def parse_utc_request(text: str) -> datetime:
    # This timezone is the request convention documented by the MT5 Python API.
    # Returned raw integer timestamps are preserved and qualified separately.
    return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def public_namedtuple(obj: Any, excluded: set[str] | None = None) -> dict[str, Any]:
    excluded = excluded or set()
    if obj is None:
        return {}
    d = obj._asdict() if hasattr(obj, "_asdict") else {}
    return {k: v for k, v in d.items() if k not in excluded}


def write_structured_array(path: Path, array: Any) -> int:
    names = list(array.dtype.names or [])
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(names)
        for row in array:
            w.writerow([row[name].item() if hasattr(row[name], "item") else row[name] for name in names])
    return len(array)


def append_ticks_by_day(path: Path, symbol: str, start: datetime, end: datetime) -> tuple[int, list[str]]:
    total = 0
    names: list[str] | None = None
    cursor = start
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        while cursor < end:
            day_end = min(cursor + timedelta(days=1), end)
            ticks = mt5.copy_ticks_range(symbol, cursor, day_end, mt5.COPY_TICKS_ALL)
            if ticks is None:
                raise RuntimeError(f"copy_ticks_range failed at {cursor}: {mt5.last_error()}")
            current_names = list(ticks.dtype.names or [])
            if names is None:
                names = current_names
                writer.writerow(names)
            elif current_names != names:
                raise RuntimeError("tick schema changed during collection")
            for row in ticks:
                writer.writerow([row[name].item() if hasattr(row[name], "item") else row[name] for name in names])
            total += len(ticks)
            cursor = day_end
    return total, names or []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default=DEFAULT_SYMBOL)
    ap.add_argument("--start", default=DEFAULT_START)
    ap.add_argument("--end", default=DEFAULT_END)
    ap.add_argument("--out", default="jp225_mt5_raw")
    args = ap.parse_args()

    start = parse_utc_request(args.start)
    end = parse_utc_request(args.end)
    if end <= start:
        raise SystemExit("end must be after start")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if not mt5.initialize():
        raise SystemExit(f"mt5.initialize failed: {mt5.last_error()}")

    try:
        version = mt5.version()
        terminal = public_namedtuple(mt5.terminal_info(), excluded={"path", "data_path", "commondata_path"})
        account = public_namedtuple(
            mt5.account_info(),
            excluded={
                "login", "name", "company", "balance", "credit", "profit", "equity",
                "margin", "margin_free", "margin_level", "assets", "liabilities",
                "commission_blocked"
            },
        )

        if not mt5.symbol_select(args.symbol, True):
            raise RuntimeError(f"symbol_select failed: {args.symbol} {mt5.last_error()}")
        symbol = public_namedtuple(mt5.symbol_info(args.symbol))

        rates = mt5.copy_rates_range(args.symbol, mt5.TIMEFRAME_M1, start, end)
        if rates is None:
            raise RuntimeError(f"copy_rates_range failed: {mt5.last_error()}")

        m1_path = out / "m1_raw.csv"
        tick_path = out / "ticks_raw.csv"
        m1_rows = write_structured_array(m1_path, rates)
        tick_rows, tick_fields = append_ticks_by_day(tick_path, args.symbol, start, end)

        metadata = {
            "collector_version": COLLECTOR_VERSION,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "request_bounds": {"start": args.start, "end": args.end, "request_timezone": "UTC_per_MT5_Python_docs"},
            "mt5_version": version,
            "terminal": terminal,
            "account": {"server": account.get("server"), "currency": account.get("currency")},
            "symbol": symbol,
            "m1_rows": m1_rows,
            "m1_fields": list(rates.dtype.names or []),
            "tick_rows": tick_rows,
            "tick_fields": tick_fields,
            "timestamp_semantics": "UNVERIFIED_PRESERVE_RAW_INTEGERS",
            "strategy_outcomes_calculated": False,
        }
        meta_path = out / "metadata.json"
        meta_path.write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")

        manifest = {
            p.name: {"sha256": sha256_file(p), "bytes": p.stat().st_size}
            for p in (m1_path, tick_path, meta_path)
        }
        (out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        print(json.dumps({
            "status": "RAW_COLLECTION_COMPLETE",
            "output_dir": str(out.resolve()),
            "m1_rows": m1_rows,
            "tick_rows": tick_rows,
            "timestamp_semantics": "UNVERIFIED",
            "strategy_outcomes_calculated": False,
        }, indent=2))
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()
