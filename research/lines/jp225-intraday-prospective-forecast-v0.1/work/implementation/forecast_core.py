from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
import hashlib
import json
from math import isfinite, log
from typing import Any, Iterable, Mapping, Sequence
from zoneinfo import ZoneInfo

TOKYO = ZoneInfo("Asia/Tokyo")
MAX_QUOTE_DELAY_SECONDS = 60
MIN_PROBABILITY = 0.01
MAX_PROBABILITY = 0.99


@dataclass(frozen=True)
class Quote:
    timestamp: datetime
    bid: float
    ask: float

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None:
            raise ValueError("quote timestamp must be timezone-aware")
        if not all(isfinite(float(x)) and float(x) > 0 for x in (self.bid, self.ask)):
            raise ValueError("bid/ask must be finite and positive")
        if self.ask < self.bid:
            raise ValueError("ask must be >= bid")

    @property
    def mid(self) -> float:
        return (float(self.bid) + float(self.ask)) / 2.0


@dataclass(frozen=True)
class EventTimes:
    forecast_cutoff: datetime
    target_start: datetime
    target_end: datetime


def _aware(value: datetime, name: str) -> None:
    if value.tzinfo is None:
        raise ValueError(f"{name} must be timezone-aware")


def intraday_event_times(
    observation_date: date,
    *,
    scheduled_jpx_trading_day: bool,
) -> EventTimes:
    if observation_date.weekday() >= 5:
        raise ValueError("JP225 intraday observation date cannot be weekend")
    if not scheduled_jpx_trading_day:
        raise ValueError("date is not a scheduled JPX cash-equity trading day")
    start = datetime.combine(observation_date, time(9, 0), TOKYO)
    end = datetime.combine(observation_date, time(15, 30), TOKYO)
    return EventTimes(forecast_cutoff=start, target_start=start, target_end=end)


def select_last_quote_at_or_before(
    quotes: Sequence[Quote],
    target: datetime,
    *,
    max_age_seconds: int = MAX_QUOTE_DELAY_SECONDS,
) -> Quote | None:
    _aware(target, "target")
    if max_age_seconds != MAX_QUOTE_DELAY_SECONDS:
        raise ValueError("unfrozen quote tolerance")
    eligible = [q for q in quotes if q.timestamp <= target]
    if not eligible:
        return None
    quote = max(eligible, key=lambda q: q.timestamp)
    if (target - quote.timestamp).total_seconds() > max_age_seconds:
        return None
    return quote


def select_first_quote_at_or_after(
    quotes: Sequence[Quote],
    target: datetime,
    *,
    max_delay_seconds: int = MAX_QUOTE_DELAY_SECONDS,
) -> Quote | None:
    _aware(target, "target")
    if max_delay_seconds != MAX_QUOTE_DELAY_SECONDS:
        raise ValueError("unfrozen quote tolerance")
    eligible = [q for q in quotes if q.timestamp >= target]
    if not eligible:
        return None
    quote = min(eligible, key=lambda q: q.timestamp)
    if (quote.timestamp - target).total_seconds() > max_delay_seconds:
        return None
    return quote


def realized_return_bps(start: Quote, end: Quote) -> float:
    return 10_000.0 * log(end.mid / start.mid)


def binary_up(start: Quote, end: Quote) -> int:
    return int(end.mid > start.mid)


def validate_probability(p: float) -> float:
    value = float(p)
    if not isfinite(value) or not MIN_PROBABILITY <= value <= MAX_PROBABILITY:
        raise ValueError(
            f"probability must be finite and in [{MIN_PROBABILITY}, {MAX_PROBABILITY}]"
        )
    return value


def validate_return_forecast_bps(value: float) -> float:
    value = float(value)
    if not isfinite(value):
        raise ValueError("forecast return must be finite")
    return value


def brier_score(p_up: float, y_up: int) -> float:
    p = validate_probability(p_up)
    if y_up not in (0, 1):
        raise ValueError("binary outcome must be 0 or 1")
    return (p - y_up) ** 2


def absolute_error_bps(forecast_return_bps: float, realized_bps: float) -> float:
    forecast = validate_return_forecast_bps(forecast_return_bps)
    realized = float(realized_bps)
    if not isfinite(realized):
        raise ValueError("realized return must be finite")
    return abs(forecast - realized)


def reject_future_information(
    items: Iterable[Mapping[str, Any]],
    cutoff: datetime,
    *,
    available_at_field: str = "available_at",
) -> None:
    _aware(cutoff, "cutoff")
    for i, item in enumerate(items):
        if available_at_field not in item:
            raise ValueError(f"source item {i} missing {available_at_field}")
        available_at = item[available_at_field]
        if not isinstance(available_at, datetime):
            raise ValueError(f"source item {i} {available_at_field} must be datetime")
        _aware(available_at, f"source item {i} {available_at_field}")
        if available_at > cutoff:
            raise PermissionError(f"source item {i} is post-cutoff information")


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
