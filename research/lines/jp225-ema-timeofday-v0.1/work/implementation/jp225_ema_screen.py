from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import inf
from random import Random
from statistics import mean
from typing import Mapping, Sequence
from zoneinfo import ZoneInfo

BOOTSTRAP_SEED = 2255200
BOOTSTRAP_REPS = 10_000
SELECTABLE_CANDIDATES = ("ALL", "TOKYO_OPEN_30", "TOKYO_CLOSE_30")

TOKYO = ZoneInfo("Asia/Tokyo")
NEW_YORK = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class Quote:
    timestamp: datetime
    bid: float
    ask: float

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            raise ValueError("quote timestamp must be timezone-aware")
        if self.ask < self.bid:
            raise ValueError("ask must be >= bid")


@dataclass(frozen=True)
class ExecutableOutcome:
    status: str
    entry_timestamp: datetime | None = None
    entry_price: float | None = None
    exit_timestamp: datetime | None = None
    exit_price: float | None = None
    net_points: float | None = None
    entry_spread: float | None = None
    exit_spread: float | None = None


def recursive_ema(values: Sequence[float], span: int) -> list[float]:
    if span <= 0:
        raise ValueError("span must be positive")
    if not values:
        return []
    alpha = 2.0 / (span + 1.0)
    out = [float(values[0])]
    for value in values[1:]:
        out.append(alpha * float(value) + (1.0 - alpha) * out[-1])
    return out


def crossover_directions(fast: Sequence[float], slow: Sequence[float]) -> list[int]:
    if len(fast) != len(slow):
        raise ValueError("length mismatch")
    out = [0] * len(fast)
    for i in range(1, len(fast)):
        if fast[i - 1] <= slow[i - 1] and fast[i] > slow[i]:
            out[i] = 1
        elif fast[i - 1] >= slow[i - 1] and fast[i] < slow[i]:
            out[i] = -1
    return out


def price_slow_crossover_directions(close: Sequence[float], slow: Sequence[float]) -> list[int]:
    if len(close) != len(slow):
        raise ValueError("length mismatch")
    out = [0] * len(close)
    for i in range(1, len(close)):
        if close[i - 1] <= slow[i - 1] and close[i] > slow[i]:
            out[i] = 1
        elif close[i - 1] >= slow[i - 1] and close[i] < slow[i]:
            out[i] = -1
    return out


def _in_half_open(dt: datetime, start_hm: tuple[int, int], end_hm: tuple[int, int]) -> bool:
    hm = (dt.hour, dt.minute)
    return start_hm <= hm < end_hm


def time_flags(signal_close: datetime) -> set[str]:
    if signal_close.tzinfo is None:
        raise ValueError("signal_close must be timezone-aware")
    tokyo = signal_close.astimezone(TOKYO)
    ny = signal_close.astimezone(NEW_YORK)
    flags = {"ALL"}
    if _in_half_open(tokyo, (8, 45), (9, 15)):
        flags.add("TOKYO_OPEN_30")
    if _in_half_open(tokyo, (15, 15), (15, 45)):
        flags.add("TOKYO_CLOSE_30")
    if _in_half_open(tokyo, (17, 0), (17, 30)):
        flags.add("OSE_NIGHT_OPEN_30")
    if _in_half_open(ny, (9, 30), (10, 30)):
        flags.add("US_CASH_OPEN_60")
    if len(flags) == 1:
        flags.add("OTHER")
    return flags


def map_executable_outcome(
    quotes: Sequence[Quote],
    signal_close: datetime,
    direction: int,
    horizon_minutes: int,
    max_quote_delay_seconds: int = 60,
) -> ExecutableOutcome:
    if signal_close.tzinfo is None:
        raise ValueError("signal_close must be timezone-aware")
    if direction not in (-1, 1):
        raise ValueError("direction must be -1 or +1")
    ordered = sorted(quotes, key=lambda q: q.timestamp)
    entry_deadline = signal_close + timedelta(seconds=max_quote_delay_seconds)
    entry = next((q for q in ordered if signal_close < q.timestamp <= entry_deadline), None)
    if entry is None:
        return ExecutableOutcome(status="NO_EXECUTABLE_ENTRY_QUOTE")

    target = signal_close + timedelta(minutes=horizon_minutes)
    exit_deadline = target + timedelta(seconds=max_quote_delay_seconds)
    exitq = next((q for q in ordered if target <= q.timestamp <= exit_deadline), None)
    if exitq is None:
        return ExecutableOutcome(
            status="NO_EXECUTABLE_TARGET_QUOTE",
            entry_timestamp=entry.timestamp,
            entry_price=entry.ask if direction == 1 else entry.bid,
            entry_spread=entry.ask - entry.bid,
        )

    entry_price = entry.ask if direction == 1 else entry.bid
    exit_price = exitq.bid if direction == 1 else exitq.ask
    return ExecutableOutcome(
        status="OK",
        entry_timestamp=entry.timestamp,
        entry_price=entry_price,
        exit_timestamp=exitq.timestamp,
        exit_price=exit_price,
        net_points=direction * (exit_price - entry_price),
        entry_spread=entry.ask - entry.bid,
        exit_spread=exitq.ask - exitq.bid,
    )


def cluster_bootstrap_mean(
    values_by_date: Mapping[object, Sequence[float]],
    reps: int = BOOTSTRAP_REPS,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float]:
    dates = list(values_by_date)
    if not dates:
        raise ValueError("no date clusters")
    rng = Random(seed)
    stats: list[float] = []
    for _ in range(reps):
        sample: list[float] = []
        for _ in dates:
            d = dates[rng.randrange(len(dates))]
            sample.extend(values_by_date[d])
        if not sample:
            raise ValueError("empty sampled cluster population")
        stats.append(mean(sample))
    stats.sort()
    lo_idx = max(0, int(0.025 * reps))
    hi_idx = min(reps - 1, int(0.975 * reps) - 1)
    return stats[lo_idx], stats[hi_idx]


def select_discovery_candidate(metrics: Mapping[str, Mapping[str, float]]) -> str | None:
    eligible: list[tuple[str, float]] = []
    for name in SELECTABLE_CANDIDATES:
        m = metrics.get(name)
        if not m:
            continue
        if (
            int(m.get("event_count", 0)) >= 100
            and int(m.get("distinct_dates", 0)) >= 60
            and float(m.get("mean_net_points", -inf)) > 0
            and float(m.get("ci_lower", -inf)) > 0
        ):
            eligible.append((name, float(m["mean_net_points"])))
    if not eligible:
        return None
    best_mean = max(v for _, v in eligible)
    tied = {name for name, v in eligible if best_mean - v <= 0.01}
    for name in SELECTABLE_CANDIDATES:
        if name in tied:
            return name
    raise AssertionError("unreachable")


def authorize_holdout_candidate(discovery_decision: str | None) -> str:
    if discovery_decision not in SELECTABLE_CANDIDATES:
        raise PermissionError("holdout is locked without one exact advanced candidate")
    return discovery_decision


def evaluate_holdout_gate(
    event_count: int,
    distinct_dates: int,
    mean_net_points: float,
    ci_lower: float,
) -> str:
    if event_count < 50 or distinct_dates < 30:
        return "INSUFFICIENT_HOLDOUT_EVENTS"
    if mean_net_points > 0 and ci_lower > 0:
        return "SUPPORTED_IN_HOLDOUT"
    return "NOT_SUPPORTED_IN_HOLDOUT"
