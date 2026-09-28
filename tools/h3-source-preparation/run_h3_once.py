#!/usr/bin/env python3
"""Execute frozen H3 once, only after the outcome-blind gate is PASS.

Do not run this program before build_h3_source_gate.py emits a 60-session freeze
packet. The runner revalidates the gate before creating any H3 touch
classification or outcome. It preserves the exact legacy generator identity and
applies H3's binary confirmation classification before the legacy
same-confirmation-bar execution filter.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import functools
import hashlib
import importlib.util
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import build_h3_source_gate as source_gate


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_legacy_generator(path: Path):
    if sha256_file(path) != source_gate.EXPECTED_GENERATOR_SHA256:
        raise ValueError("legacy_generator_identity_mismatch")
    spec = importlib.util.spec_from_file_location(
        "h3_exact_legacy_generator",
        path,
    )
    if spec is None or spec.loader is None:
        raise ValueError("legacy_generator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assemble_m1(
    legacy,
    h2_prefix_root: Path,
    m1_root: Path,
) -> tuple[
    list[dict],
    dict[str, tuple[int, int]],
    list[float],
    list[dict],
]:
    h2 = json.loads(
        (h2_prefix_root / "h2_prefix_source_identity.json").read_text()
    )
    post = json.loads((m1_root / "m1_source_manifest.json").read_text())

    records = []
    for record in h2["records"]:
        records.append(
            (
                record["date"],
                h2_prefix_root / record["relative_path"],
                record["sha256"],
            )
        )
    for record in post["records"]:
        records.append(
            (
                record["date"],
                m1_root / record["relative_path"],
                record["sha256"],
            )
        )

    if [d for d, _, _ in records] != sorted(d for d, _, _ in records):
        raise ValueError("m1_date_order_mismatch")

    all_bars = []
    source_chain = []
    for day, path, expected_sha in records:
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ValueError(f"m1_raw_identity_mismatch:{day}")
        rows = legacy.decode_m1(json.loads(raw))
        for row in rows:
            row["source_date"] = day
            all_bars.append(row)
        source_chain.append({"date": day, "sha256": expected_sha})

    all_bars.sort(key=lambda row: row["ts"])
    if any(
        all_bars[i]["ts"] >= all_bars[i + 1]["ts"]
        for i in range(len(all_bars) - 1)
    ):
        raise ValueError("global_m1_not_strictly_increasing")

    date_ranges: dict[str, list[int]] = {}
    for i, bar in enumerate(all_bars):
        date_ranges.setdefault(bar["source_date"], [i, i + 1])[1] = i + 1
    frozen_ranges = {
        key: tuple(value) for key, value in date_ranges.items()
    }

    abs_change_prefix = [0.0]
    for i in range(1, len(all_bars)):
        abs_change_prefix.append(
            abs_change_prefix[-1]
            + abs(all_bars[i]["c"] - all_bars[i - 1]["c"])
        )

    return all_bars, frozen_ranges, abs_change_prefix, source_chain


def classify_session(
    all_bars: list[dict],
    selected_date: str,
    date_ranges: dict[str, tuple[int, int]],
    abs_change_prefix: list[float],
) -> dict[str, Any]:
    """Reproduce legacy touch/confirmation state before execution filtering.

    Same-confirmation-bar touches remain CONFIRMED, as frozen by DEC-HR-004.
    """

    start_idx, end_idx = date_ranges.get(selected_date, (0, 0))
    current = all_bars[start_idx:end_idx]
    if not current:
        raise ValueError(f"missing_m1_for_selected_date:{selected_date}")

    touches: list[dict[str, Any]] = []
    ambiguous: list[dict[str, Any]] = []
    state: dict[str, dict[str, Any]] = {
        "support": {"pending": None, "locked": False},
        "resistance": {"pending": None, "locked": False},
    }

    for i, bar in enumerate(current):
        global_i = start_idx + i
        if global_i < 60:
            continue

        prior = all_bars[global_i - 60 : global_i]
        support = min(x["l"] for x in prior)
        resistance = max(x["h"] for x in prior)
        gamma = (
            abs_change_prefix[global_i] / (global_i - 1)
            if global_i > 1
            else 0.0
        )
        if not all(
            math.isfinite(x) for x in (support, resistance, gamma)
        ):
            continue

        sl, sh = support - gamma, support + gamma
        rl, rh = resistance - gamma, resistance + gamma
        prev_close = all_bars[global_i - 1]["c"]

        if state["support"]["locked"] and bar["l"] > sh:
            state["support"]["locked"] = False
        if state["resistance"]["locked"] and bar["h"] < rl:
            state["resistance"]["locked"] = False

        pending = state["support"]["pending"]
        if pending is not None and i > pending["touch_index"]:
            if bar["c"] > pending["zone_hi"]:
                pending["confirmed"] = True
                pending["confirm_bar_ts"] = bar["ts"]
                pending["signal_available_ts"] = bar["ts"] + 60_000
                pending["resolution"] = "CONFIRMED"
                state["support"]["pending"] = None
                state["support"]["locked"] = True
            elif (
                bar["c"] < pending["zone_lo"]
                and bar["h"] < pending["zone_lo"]
            ):
                pending["resolution"] = "FAILED_THROUGH_FAR_BOUNDARY"
                state["support"]["pending"] = None
                state["support"]["locked"] = True

        pending = state["resistance"]["pending"]
        if pending is not None and i > pending["touch_index"]:
            if bar["c"] < pending["zone_lo"]:
                pending["confirmed"] = True
                pending["confirm_bar_ts"] = bar["ts"]
                pending["signal_available_ts"] = bar["ts"] + 60_000
                pending["resolution"] = "CONFIRMED"
                state["resistance"]["pending"] = None
                state["resistance"]["locked"] = True
            elif (
                bar["c"] > pending["zone_hi"]
                and bar["l"] > pending["zone_hi"]
            ):
                pending["resolution"] = "FAILED_THROUGH_FAR_BOUNDARY"
                state["resistance"]["pending"] = None
                state["resistance"]["locked"] = True

        support_touch = (
            not state["support"]["locked"]
            and state["support"]["pending"] is None
            and prev_close > sh
            and bar["l"] <= sh
        )
        resistance_touch = (
            not state["resistance"]["locked"]
            and state["resistance"]["pending"] is None
            and prev_close < rl
            and bar["h"] >= rl
        )

        if support_touch and resistance_touch:
            ambiguous.append(
                {
                    "date": selected_date,
                    "touch_ts": bar["ts"],
                    "reason": "both_zone_touches_same_bar",
                }
            )
            continue

        if support_touch:
            touch = {
                "date": selected_date,
                "direction": "LONG",
                "side": "support",
                "touch_index": i,
                "touch_ts": bar["ts"],
                "support": support,
                "resistance": resistance,
                "gamma": gamma,
                "zone_lo": sl,
                "zone_hi": sh,
                "confirmed": False,
                "confirm_bar_ts": None,
                "signal_available_ts": None,
                "same_confirmation_bar": False,
                "resolution": "PENDING_AT_SESSION_END",
            }
            state["support"]["pending"] = touch
            touches.append(touch)

        if resistance_touch:
            touch = {
                "date": selected_date,
                "direction": "SHORT",
                "side": "resistance",
                "touch_index": i,
                "touch_ts": bar["ts"],
                "support": support,
                "resistance": resistance,
                "gamma": gamma,
                "zone_lo": rl,
                "zone_hi": rh,
                "confirmed": False,
                "confirm_bar_ts": None,
                "signal_available_ts": None,
                "same_confirmation_bar": False,
                "resolution": "PENDING_AT_SESSION_END",
            }
            state["resistance"]["pending"] = touch
            touches.append(touch)

    by_confirm: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for touch in touches:
        if touch["confirmed"]:
            by_confirm[int(touch["confirm_bar_ts"])].append(touch)

    for rows in by_confirm.values():
        if len(rows) > 1:
            for touch in rows:
                touch["same_confirmation_bar"] = True

    public_touches = []
    for touch in touches:
        row = dict(touch)
        row.pop("touch_index", None)
        row["classification"] = (
            "CONFIRMED" if row["confirmed"] else "UNCONFIRMED"
        )
        public_touches.append(row)

    return {
        "date": selected_date,
        "bars": len(current),
        "touches": public_touches,
        "ambiguous": ambiguous,
        "same_confirmation_bar_count": sum(
            1 for rows in by_confirm.values() if len(rows) > 1
        ),
    }


def crosscheck_with_legacy(
    legacy,
    all_bars: list[dict],
    selected_date: str,
    date_ranges: dict[str, tuple[int, int]],
    abs_change_prefix: list[float],
    classified: dict[str, Any],
) -> dict[str, Any]:
    original = legacy.build_session_events(
        all_bars,
        selected_date,
        date_ranges,
        abs_change_prefix,
    )

    projected_touches = [
        {
            "date": row["date"],
            "direction": row["direction"],
            "touch_ts": row["touch_ts"],
            "zone_lo": row["zone_lo"],
            "zone_hi": row["zone_hi"],
        }
        for row in classified["touches"]
    ]
    if projected_touches != original["touches"]:
        raise ValueError(
            f"legacy_touch_population_mismatch:{selected_date}"
        )

    by_confirm: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in classified["touches"]:
        if row["confirmed"]:
            by_confirm[int(row["confirm_bar_ts"])].append(row)

    clean = []
    for rows in by_confirm.values():
        if len(rows) == 1:
            row = rows[0]
            clean.append(
                {
                    "date": row["date"],
                    "direction": row["direction"],
                    "touch_ts": row["touch_ts"],
                    "confirm_bar_ts": row["confirm_bar_ts"],
                    "signal_available_ts": row["signal_available_ts"],
                    "zone_lo": row["zone_lo"],
                    "zone_hi": row["zone_hi"],
                }
            )
    clean.sort(key=lambda row: row["signal_available_ts"])

    original_clean = [
        {
            "date": row["date"],
            "direction": row["direction"],
            "touch_ts": row["touch_ts"],
            "confirm_bar_ts": row["confirm_bar_ts"],
            "signal_available_ts": row["signal_available_ts"],
            "zone_lo": row["zone_lo"],
            "zone_hi": row["zone_hi"],
        }
        for row in original["events"]
    ]
    if clean != original_clean:
        raise ValueError(
            f"legacy_clean_confirmation_mismatch:{selected_date}"
        )

    original_same_confirm = sum(
        1
        for row in original["ambiguous"]
        if row.get("reason") == "both_confirmations_same_bar"
    )
    if (
        classified["same_confirmation_bar_count"]
        != original_same_confirm
    ):
        raise ValueError(
            f"same_confirmation_bar_count_mismatch:{selected_date}"
        )

    original_zone_ambiguous = sum(
        1
        for row in original["ambiguous"]
        if row.get("reason") == "both_zone_touches_same_bar"
    )
    if len(classified["ambiguous"]) != original_zone_ambiguous:
        raise ValueError(
            f"same_touch_bar_ambiguity_count_mismatch:{selected_date}"
        )

    return {
        "date": selected_date,
        "touch_population_match": True,
        "legacy_clean_confirmation_match": True,
        "same_confirmation_bar_count_match": True,
        "same_touch_bar_ambiguity_count_match": True,
    }


def decode_tick(
    payload: dict,
) -> tuple[list[int], list[float], list[float]]:
    times = payload.get("times") or []
    asks = payload.get("asks") or []
    bids = payload.get("bids") or []
    if not (len(times) == len(asks) == len(bids)):
        raise ValueError("inconsistent_tick_lengths")
    if not times:
        return [], [], []

    mult = float(payload.get("multiplier") or 1)
    stamp = int(payload.get("timestamp") or 0)
    ask = float(payload.get("ask") or 0)
    bid = float(payload.get("bid") or 0)
    out_t, out_b, out_a = [], [], []

    for dt, da, db in zip(times, asks, bids):
        stamp += int(dt)
        ask = round(ask + float(da) * mult, 10)
        bid = round(bid + float(db) * mult, 10)
        if not (math.isfinite(ask) and math.isfinite(bid)):
            raise ValueError("nonfinite_tick_quote")
        out_t.append(stamp)
        out_b.append(bid)
        out_a.append(ask)

    if any(
        out_t[i] > out_t[i + 1]
        for i in range(len(out_t) - 1)
    ):
        raise ValueError("tick_time_reversal")
    return out_t, out_b, out_a


class TickStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    @functools.lru_cache(maxsize=64)
    def load(
        self,
        day: str,
        hour: int,
    ) -> tuple[list[int], list[float], list[float]]:
        path = self.root / "raw_tick" / day / f"{hour:02d}.json"
        if not path.is_file():
            return [], [], []
        return decode_tick(json.loads(path.read_bytes()))

    def load_hour_ms(
        self,
        hour_ms: int,
    ) -> tuple[list[int], list[float], list[float]]:
        from datetime import datetime, timezone

        dt = datetime.fromtimestamp(hour_ms / 1000, timezone.utc)
        return self.load(dt.strftime("%Y-%m-%d"), dt.hour)


def first_touch_quote(
    touch: dict[str, Any],
    ticks: TickStore,
) -> tuple[int, float, float] | None:
    start = int(touch["touch_ts"])
    end = start + 60_000
    hour = (start // 3_600_000) * 3_600_000

    for hour_ms in (hour, hour + 3_600_000):
        ts, bid, ask = ticks.load_hour_ms(hour_ms)
        if not ts:
            continue
        i = bisect.bisect_left(ts, start)
        j = bisect.bisect_left(ts, end)
        for k in range(i, j):
            if (
                touch["direction"] == "LONG"
                and bid[k] <= touch["zone_hi"]
            ):
                return ts[k], bid[k], ask[k]
            if (
                touch["direction"] == "SHORT"
                and bid[k] >= touch["zone_lo"]
            ):
                return ts[k], bid[k], ask[k]
    return None


def first_quote_after(
    target: int,
    ticks: TickStore,
) -> tuple[int, float, float] | None:
    hour = (target // 3_600_000) * 3_600_000
    for offset in range(73):
        ts, bid, ask = ticks.load_hour_ms(
            hour + offset * 3_600_000
        )
        if not ts:
            continue
        k = bisect.bisect_left(ts, target)
        if k < len(ts):
            return ts[k], bid[k], ask[k]
    return None


def evaluate_touch(
    touch: dict[str, Any],
    ticks: TickStore,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    touch_quote = first_touch_quote(touch, ticks)
    if touch_quote is None:
        return None, {
            "date": touch["date"],
            "direction": touch["direction"],
            "classification": touch["classification"],
            "touch_ts": touch["touch_ts"],
            "reason": "raw_touch_quote_unavailable",
        }

    endpoint = first_quote_after(
        touch_quote[0] + 15 * 60 * 1000,
        ticks,
    )
    if endpoint is None:
        return None, {
            "date": touch["date"],
            "direction": touch["direction"],
            "classification": touch["classification"],
            "touch_ts": touch["touch_ts"],
            "touch_quote_ts": touch_quote[0],
            "reason": "plus15_quote_unavailable",
        }

    sign = 1 if touch["direction"] == "LONG" else -1
    open_price = touch_quote[2] if sign == 1 else touch_quote[1]
    close_price = endpoint[1] if sign == 1 else endpoint[2]
    bps = sign * (close_price - open_price) / open_price * 10_000

    return {
        "date": touch["date"],
        "direction": touch["direction"],
        "classification": touch["classification"],
        "same_confirmation_bar": touch["same_confirmation_bar"],
        "touch_bar_ts": touch["touch_ts"],
        "confirm_bar_ts": touch["confirm_bar_ts"],
        "zone_lo": touch["zone_lo"],
        "zone_hi": touch["zone_hi"],
        "touch_quote_ts": touch_quote[0],
        "touch_bid": touch_quote[1],
        "touch_ask": touch_quote[2],
        "plus15_quote_ts": endpoint[0],
        "plus15_bid": endpoint[1],
        "plus15_ask": endpoint[2],
        "primary_bps": bps,
    }, None


def descriptive(values: list[float]) -> dict[str, Any]:
    return {
        "n": len(values),
        "mean_bps": statistics.fmean(values) if values else None,
        "median_bps": statistics.median(values) if values else None,
        "positive_rate": (
            sum(value > 0 for value in values) / len(values)
            if values
            else None
        ),
    }


def bootstrap_contrast(
    rows: list[dict[str, Any]],
    selected: list[str],
    seed: int,
    reps: int,
) -> dict[str, Any]:
    import numpy as np

    c_sums = []
    c_counts = []
    u_sums = []
    u_counts = []

    for day in selected:
        confirmed = [
            row["primary_bps"]
            for row in rows
            if row["date"] == day
            and row["classification"] == "CONFIRMED"
        ]
        unconfirmed = [
            row["primary_bps"]
            for row in rows
            if row["date"] == day
            and row["classification"] == "UNCONFIRMED"
        ]
        c_sums.append(sum(confirmed))
        c_counts.append(len(confirmed))
        u_sums.append(sum(unconfirmed))
        u_counts.append(len(unconfirmed))

    c_sums = np.asarray(c_sums, dtype=float)
    c_counts = np.asarray(c_counts, dtype=np.int64)
    u_sums = np.asarray(u_sums, dtype=float)
    u_counts = np.asarray(u_counts, dtype=np.int64)

    rng = np.random.default_rng(seed)
    idx = rng.integers(
        0,
        len(selected),
        size=(reps, len(selected)),
    )

    c_den = c_counts[idx].sum(axis=1)
    u_den = u_counts[idx].sum(axis=1)
    valid = (c_den > 0) & (u_den > 0)
    c_mean = np.divide(
        c_sums[idx].sum(axis=1),
        c_den,
        out=np.full(reps, np.nan),
        where=c_den > 0,
    )
    u_mean = np.divide(
        u_sums[idx].sum(axis=1),
        u_den,
        out=np.full(reps, np.nan),
        where=u_den > 0,
    )
    contrast = c_mean - u_mean
    valid_values = contrast[valid]
    ci = (
        np.percentile(valid_values, [2.5, 97.5]).tolist()
        if len(valid_values)
        else [None, None]
    )

    return {
        "seed": seed,
        "replications": reps,
        "valid_replications": int(valid.sum()),
        "invalid_replications": int((~valid).sum()),
        "percentile_95_interval": ci,
    }


def verify_freeze_packet(packet: dict[str, Any]) -> None:
    if packet.get("status") != "FROZEN_BEFORE_H3_OUTCOME_ACCESS":
        raise ValueError("freeze_packet_status_invalid")
    if (
        packet.get("selected_session_count") != 60
        or len(packet.get("selected_dates") or []) != 60
    ):
        raise ValueError("freeze_packet_selected_session_count_invalid")
    if (
        packet.get("bootstrap_seed") != 20260913
        or packet.get("bootstrap_replications") != 10_000
        or packet.get("bootstrap_engine")
        != "numpy.random.default_rng/PCG64"
    ):
        raise ValueError("freeze_packet_bootstrap_identity_invalid")
    if packet.get("h3_runner_sha256") != sha256_file(Path(__file__)):
        raise ValueError("freeze_packet_runner_identity_mismatch")

    expected = packet.get("freeze_packet_sha256")
    without_hash = dict(packet)
    without_hash.pop("freeze_packet_sha256", None)
    if expected != source_gate.canonical_sha256(without_hash):
        raise ValueError("freeze_packet_hash_mismatch")

    if (
        packet.get("outcome_computed") is not False
        or packet.get("bootstrap_run") is not False
    ):
        raise ValueError("freeze_packet_outcome_flag_invalid")


def run(args: argparse.Namespace) -> dict[str, Any]:
    persisted_gate = json.loads(
        args.gate_result.read_text(encoding="utf-8")
    )
    packet = persisted_gate.get("freeze_packet")
    if not isinstance(packet, dict):
        raise ValueError("no_frozen_60_session_packet")
    verify_freeze_packet(packet)

    current_gate = source_gate.build(
        SimpleNamespace(
            legacy_generator=args.legacy_generator,
            h2_prefix_root=args.h2_prefix_root,
            m1_root=args.m1_root,
            structural_manifest=args.structural_manifest,
            tick_root=args.tick_root,
            tick_verification_root=args.tick_verification_root,
            h3_runner=Path(__file__),
            independence_attestation=args.independence_attestation,
        )
    )
    if (
        current_gate.get("source_gate") != "PASS"
        or current_gate.get("status")
        != "READY_FOR_FROZEN_H3_RUN"
    ):
        raise ValueError("current_source_gate_not_pass")

    current_packet = current_gate.get("freeze_packet")
    if (
        not isinstance(current_packet, dict)
        or current_packet.get("freeze_packet_sha256")
        != packet.get("freeze_packet_sha256")
    ):
        raise ValueError(
            "freeze_packet_no_longer_matches_current_source"
        )

    args.output_dir.mkdir(parents=True, exist_ok=False)
    write_json(
        args.output_dir / "RUN_STARTED.json",
        {
            "status": "HOLDOUT_ACCESS_AUTHORIZED",
            "freeze_packet_sha256": packet[
                "freeze_packet_sha256"
            ],
            "runner_sha256": sha256_file(Path(__file__)),
            "outcome_result_written": False,
        },
    )

    legacy = load_legacy_generator(args.legacy_generator)
    (
        all_bars,
        date_ranges,
        abs_change_prefix,
        source_chain,
    ) = assemble_m1(
        legacy,
        args.h2_prefix_root,
        args.m1_root,
    )
    if (
        canonical_sha256(source_chain)
        != packet["generator_history_source_chain_sha256"]
    ):
        raise ValueError(
            "generator_history_source_chain_mismatch"
        )

    selected = packet["selected_dates"]
    classified_sessions = []
    crosschecks = []
    touches = []

    for day in selected:
        classified = classify_session(
            all_bars,
            day,
            date_ranges,
            abs_change_prefix,
        )
        crosschecks.append(
            crosscheck_with_legacy(
                legacy,
                all_bars,
                day,
                date_ranges,
                abs_change_prefix,
                classified,
            )
        )
        classified_sessions.append(
            {
                "date": day,
                "bars": classified["bars"],
                "touch_count": len(classified["touches"]),
                "confirmed_count": sum(
                    row["confirmed"]
                    for row in classified["touches"]
                ),
                "same_confirmation_bar_count": classified[
                    "same_confirmation_bar_count"
                ],
                "ambiguous_touch_bar_count": len(
                    classified["ambiguous"]
                ),
            }
        )
        touches.extend(classified["touches"])

    legacy_crosscheck_all_pass = all(
        all(value is True for key, value in row.items() if key != "date")
        for row in crosschecks
    )
    if not legacy_crosscheck_all_pass:
        raise ValueError("legacy_crosscheck_failed")

    write_json(
        args.output_dir / "classification_receipt.json",
        {
            "selected_session_count": len(selected),
            "touch_count": len(touches),
            "confirmed_count": sum(
                row["confirmed"] for row in touches
            ),
            "unconfirmed_count": sum(
                not row["confirmed"] for row in touches
            ),
            "same_confirmation_bar_touch_count": sum(
                row["same_confirmation_bar"] for row in touches
            ),
            "legacy_crosscheck_all_pass": True,
            "sessions": classified_sessions,
        },
    )

    write_json(
        args.output_dir / "OUTCOME_ACCESS_STARTED.json",
        {
            "status": "OUTCOME_ACCESS_STARTED",
            "touch_count": len(touches),
            "freeze_packet_sha256": packet[
                "freeze_packet_sha256"
            ],
        },
    )

    ticks = TickStore(args.tick_root)
    rows = []
    unavailable = []

    for event_id, touch in enumerate(touches, 1):
        row, missing = evaluate_touch(touch, ticks)
        if row is not None:
            row["event_id"] = event_id
            rows.append(row)
        else:
            missing["event_id"] = event_id
            unavailable.append(missing)

    confirmed_all = [
        row
        for row in touches
        if row["classification"] == "CONFIRMED"
    ]
    unconfirmed_all = [
        row
        for row in touches
        if row["classification"] == "UNCONFIRMED"
    ]
    confirmed_values = [
        row["primary_bps"]
        for row in rows
        if row["classification"] == "CONFIRMED"
    ]
    unconfirmed_values = [
        row["primary_bps"]
        for row in rows
        if row["classification"] == "UNCONFIRMED"
    ]

    primary_contrast = (
        statistics.fmean(confirmed_values)
        - statistics.fmean(unconfirmed_values)
        if confirmed_values and unconfirmed_values
        else None
    )
    bootstrap = bootstrap_contrast(
        rows,
        selected,
        packet["bootstrap_seed"],
        packet["bootstrap_replications"],
    )
    ci = bootstrap["percentile_95_interval"]

    if (
        primary_contrast is None
        or ci[0] is None
        or ci[1] is None
        or bootstrap["invalid_replications"]
    ):
        classification = "INCONCLUSIVE"
    elif ci[0] > 0:
        classification = "CONFIRMATION_SELECTION_EFFECT_SUPPORTED"
    elif ci[1] <= 0:
        classification = (
            "NO_CONFIRMATION_SELECTION_EFFECT_SUPPORT"
        )
    else:
        classification = "INCONCLUSIVE"

    session_summary = []
    for day in selected:
        cvals = [
            row["primary_bps"]
            for row in rows
            if row["date"] == day
            and row["classification"] == "CONFIRMED"
        ]
        uvals = [
            row["primary_bps"]
            for row in rows
            if row["date"] == day
            and row["classification"] == "UNCONFIRMED"
        ]
        session_summary.append(
            {
                "date": day,
                "confirmed_available_count": len(cvals),
                "unconfirmed_available_count": len(uvals),
                "confirmed_mean_bps": (
                    statistics.fmean(cvals) if cvals else None
                ),
                "unconfirmed_mean_bps": (
                    statistics.fmean(uvals) if uvals else None
                ),
            }
        )

    def direction_summary(direction: str) -> dict[str, Any]:
        subset = [
            row for row in rows if row["direction"] == direction
        ]
        confirmed = [
            row["primary_bps"]
            for row in subset
            if row["classification"] == "CONFIRMED"
        ]
        unconfirmed = [
            row["primary_bps"]
            for row in subset
            if row["classification"] == "UNCONFIRMED"
        ]
        return {
            "available_count": len(subset),
            "confirmed": descriptive(confirmed),
            "unconfirmed": descriptive(unconfirmed),
            "contrast_bps": (
                statistics.fmean(confirmed)
                - statistics.fmean(unconfirmed)
                if confirmed and unconfirmed
                else None
            ),
        }

    reason_set = {row["reason"] for row in unavailable}
    result = {
        "status": "COMPLETED",
        "scientific_test": (
            "HYP-HR-003_CONFIRMATION_SELECTION_EFFECT"
        ),
        "specification": "SPEC-HR-003-v01",
        "decision": "DEC-HR-004",
        "freeze_packet_sha256": packet[
            "freeze_packet_sha256"
        ],
        "selected_session_count": 60,
        "selected_dates": selected,
        "eligible_touch_count": len(touches),
        "confirmed_count": len(confirmed_all),
        "confirmed_rate": (
            len(confirmed_all) / len(touches)
            if touches
            else None
        ),
        "unconfirmed_count": len(unconfirmed_all),
        "available_outcome_count": len(rows),
        "unavailable_count": len(unavailable),
        "unavailable_reason_counts": {
            reason: sum(
                1
                for row in unavailable
                if row["reason"] == reason
            )
            for reason in sorted(reason_set)
        },
        "confirmed_outcome": descriptive(confirmed_values),
        "unconfirmed_outcome": descriptive(unconfirmed_values),
        "primary_contrast_bps": primary_contrast,
        "session_clustered_bootstrap": bootstrap,
        "result_classification": classification,
        "same_confirmation_bar_touch_count": sum(
            row["same_confirmation_bar"] for row in touches
        ),
        "long_descriptive": direction_summary("LONG"),
        "short_descriptive": direction_summary("SHORT"),
        "session_level": session_summary,
        "legacy_crosscheck_all_pass": True,
        "legacy_generator_sha256": (
            source_gate.EXPECTED_GENERATOR_SHA256
        ),
        "runner_sha256": sha256_file(Path(__file__)),
        "bootstrap_engine": "numpy.random.default_rng/PCG64",
        "no_parameter_search": True,
        "no_sample_reselection": True,
        "no_protocol_change": True,
    }

    write_json(args.output_dir / "result.json", result)

    with (
        args.output_dir / "event_level.csv"
    ).open("w", newline="", encoding="utf-8") as stream:
        fields = [
            "event_id",
            "date",
            "direction",
            "classification",
            "same_confirmation_bar",
            "touch_bar_ts",
            "confirm_bar_ts",
            "zone_lo",
            "zone_hi",
            "touch_quote_ts",
            "touch_bid",
            "touch_ask",
            "plus15_quote_ts",
            "plus15_bid",
            "plus15_ask",
            "primary_bps",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with (
        args.output_dir / "unavailable_events.csv"
    ).open("w", newline="", encoding="utf-8") as stream:
        fields = [
            "event_id",
            "date",
            "direction",
            "classification",
            "touch_ts",
            "touch_quote_ts",
            "reason",
        ]
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(unavailable)

    write_json(
        args.output_dir / "RUN_COMPLETE.json",
        {
            "status": "RUN_COMPLETE",
            "result_sha256": sha256_file(
                args.output_dir / "result.json"
            ),
            "event_level_sha256": sha256_file(
                args.output_dir / "event_level.csv"
            ),
            "unavailable_sha256": sha256_file(
                args.output_dir / "unavailable_events.csv"
            ),
            "freeze_packet_sha256": packet[
                "freeze_packet_sha256"
            ],
        },
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-result", type=Path, required=True)
    parser.add_argument("--m1-root", type=Path, required=True)
    parser.add_argument("--h2-prefix-root", type=Path, required=True)
    parser.add_argument("--tick-root", type=Path, required=True)
    parser.add_argument(
        "--tick-verification-root",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--structural-manifest",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--legacy-generator",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--independence-attestation",
        type=Path,
        required=True,
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    result = run(args)
    print(
        json.dumps(
            {
                "status": result["status"],
                "result_classification": result[
                    "result_classification"
                ],
                "primary_contrast_bps": result[
                    "primary_contrast_bps"
                ],
                "bootstrap_95ci": result[
                    "session_clustered_bootstrap"
                ]["percentile_95_interval"],
                "output_dir": str(args.output_dir),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
