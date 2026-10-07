"""Outcome-blind source probe for XM MT5 EURJPY.

Collects only small fixed BID/ASK tick windows plus non-sensitive source metadata.
It does NOT calculate returns, signals, strategy P/L, or place orders.
Requires an already installed and logged-in MetaTrader 5 terminal on Windows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

VERSION = "FXNS_EURJPY_SOURCE_PROBE_v0.2"
SYMBOL = "EURJPY"
JST = ZoneInfo("Asia/Tokyo")

# Fixed before formal prospective scoring. These are source/time-schema probes only.
PROBES_JST = (
    ("winter_2026", "2026-01-15T08:14:00+09:00", "2026-01-15T08:16:00+09:00"),
    ("summer_2026", "2026-07-15T08:14:00+09:00", "2026-07-15T08:16:00+09:00"),
    ("autumn_2026", "2026-10-06T08:14:00+09:00", "2026-10-06T08:16:00+09:00"),
    ("winter_friday_2026", "2026-01-16T08:14:00+09:00", "2026-01-16T08:16:00+09:00"),
    ("summer_friday_2026", "2026-07-17T08:14:00+09:00", "2026-07-17T08:16:00+09:00"),
    ("autumn_friday_2026", "2026-10-02T08:14:00+09:00", "2026-10-02T08:16:00+09:00"),
)

SYMBOL_FIELDS = (
    "name",
    "digits",
    "point",
    "trade_tick_size",
    "trade_contract_size",
    "volume_min",
    "volume_step",
    "spread_float",
    "swap_long",
    "swap_short",
    "swap_rollover3days",
    "trade_calc_mode",
)
TERMINAL_FIELDS = ("build", "maxbars")
ACCOUNT_FIELDS = ("server",)
EXPECTED_TICK_FIELDS = (
    "time",
    "bid",
    "ask",
    "last",
    "volume",
    "time_msc",
    "flags",
    "volume_real",
)


def parse_aware(text: str) -> datetime:
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return dt


def to_utc(text: str) -> datetime:
    return parse_aware(text).astimezone(timezone.utc)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def allowlist(obj: Any, fields: Iterable[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for field in fields:
        out[field] = getattr(obj, field, None) if obj is not None else None
    return out


def raw_time_bounds(arr: Any) -> dict[str, int | None]:
    if arr is None or len(arr) == 0:
        return {"first_time": None, "last_time": None, "first_time_msc": None, "last_time_msc": None}
    return {
        "first_time": int(arr[0]["time"]),
        "last_time": int(arr[-1]["time"]),
        "first_time_msc": int(arr[0]["time_msc"]),
        "last_time_msc": int(arr[-1]["time_msc"]),
    }


def validate_tick_array(arr: Any) -> None:
    if arr is None:
        raise RuntimeError("TICK_ACQUISITION_FAILED")
    fields = tuple(arr.dtype.names or ())
    if fields != EXPECTED_TICK_FIELDS:
        raise RuntimeError(f"TICK_SCHEMA_FAILURE:{fields!r}")
    for row in arr:
        bid = float(row["bid"])
        ask = float(row["ask"])
        if not (math.isfinite(bid) and math.isfinite(ask)) or bid <= 0 or ask <= 0 or bid > ask:
            raise RuntimeError("INVALID_BID_ASK_ROW")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", choices=[SYMBOL], default=SYMBOL)
    ap.add_argument("--out", default="fxns_eurjpy_mt5_source_probe")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)

    import MetaTrader5 as mt5

    if not mt5.initialize():
        raise SystemExit("MT5_INITIALIZE_FAILED")

    try:
        if not mt5.symbol_select(args.symbol, True):
            candidates = sorted(
                s.name for s in (mt5.symbols_get() or [])
                if "EURJPY" in s.name.upper().replace("/", "")
            )
            print(json.dumps({"status": "EXACT_SYMBOL_IDENTITY_REQUIRES_PRE_FREEZE_DECISION",
                              "eurjpy_like_symbol_names": candidates}))
            raise RuntimeError(
                "EXACT_SYMBOL_IDENTITY_REQUIRES_PRE_FREEZE_DECISION; "
                f"Exact candidate symbol {args.symbol!r} unavailable; "
                f"EURJPY-like visible symbols={candidates!r}. No substitution performed."
            )

        symbol_info_obj = mt5.symbol_info(args.symbol)
        symbol_info = allowlist(symbol_info_obj, SYMBOL_FIELDS)
        if symbol_info.get("name") != SYMBOL:
            raise RuntimeError("EXACT_SYMBOL_IDENTITY_FAILED")

        terminal = allowlist(mt5.terminal_info(), TERMINAL_FIELDS)
        account = allowlist(mt5.account_info(), ACCOUNT_FIELDS)

        raw_path = out / "tick_probes_raw.csv"
        probe_meta: list[dict[str, Any]] = []
        with raw_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["probe_id", *EXPECTED_TICK_FIELDS])
            for probe_id, start_jst, end_jst in PROBES_JST:
                start_utc = to_utc(start_jst)
                end_utc = to_utc(end_jst)
                ticks = mt5.copy_ticks_range(
                    args.symbol,
                    start_utc,
                    end_utc,
                    mt5.COPY_TICKS_ALL,
                )
                validate_tick_array(ticks)
                for row in ticks:
                    writer.writerow([
                        probe_id,
                        *[
                            row[name].item() if hasattr(row[name], "item") else row[name]
                            for name in EXPECTED_TICK_FIELDS
                        ],
                    ])
                probe_meta.append({
                    "probe_id": probe_id,
                    "purpose": "FRIDAY_EXIT_FEASIBILITY" if "friday" in probe_id else "SOURCE_TIME_SCHEMA",
                    "intended_weekday": parse_aware(start_jst).strftime("%A"),
                    "request_start_jst": start_jst,
                    "request_end_jst": end_jst,
                    "request_start_utc": start_utc.isoformat(),
                    "request_end_utc": end_utc.isoformat(),
                    "rows": len(ticks),
                    **raw_time_bounds(ticks),
                })

        metadata = {
            "collector_version": VERSION,
            "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            "scientific_outcomes_calculated": False,
            "strategy_returns_calculated": False,
            "orders_placed": False,
            "request_time_convention": "UTC-aware datetimes per MetaTrader5 Python API",
            "returned_timestamp_semantics": "UNVERIFIED_PRESERVE_RAW_TIME_AND_TIME_MSC",
            "mt5_version": mt5.version(),
            "package_version": mt5.__version__,
            "terminal": terminal,
            "account": {"server": account.get("server")},
            "symbol": symbol_info,
            "commission_status": "UNVERIFIED_NOT_INFERRED_FROM_ACCOUNT_HISTORY",
            "other_costs_status": "UNVERIFIED_NOT_CALCULATED",
            "swap_metadata_status": "PRESERVED_FROM_SYMBOL_INFO_NOT_YET_ECONOMICALLY_QUALIFIED",
            "tick_probes": probe_meta,
        }
        meta_path = out / "metadata.json"
        meta_path.write_text(json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8")

        manifest = {}
        for p in (raw_path, meta_path):
            manifest[p.name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
        manifest_path = out / "sha256_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        print(json.dumps({
            "status": "SOURCE_PROBE_COLLECTION_COMPLETE",
            "symbol": SYMBOL,
            "probe_count": len(PROBES_JST),
            "tick_rows": sum(p["rows"] for p in probe_meta),
            "scientific_outcomes_calculated": False,
            "orders_placed": False,
            "commission_status": metadata["commission_status"],
        }, indent=2))
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Do not print raw MT5 errors or quote values into logs.
        print(json.dumps({
            "status": "FAIL",
            "error_class": type(exc).__name__,
            "scientific_outcomes_calculated": False,
            "orders_placed": False,
        }))
        raise SystemExit("Preserve the failed local directory; do not use it as qualified source data") from None
