"""Pure, outcome-agnostic mechanics for SPEC-JP225-IMOM-001-v01."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import isfinite
from statistics import mean
from typing import Iterable, Sequence
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")


class AmbiguousTrade(ValueError):
    pass


class DegenerateSample(ValueError):
    pass


@dataclass(frozen=True)
class Contract:
    code: str
    last_trading_day: date


@dataclass(frozen=True)
class Trade:
    timestamp: datetime
    price: float
    source_order: int | None = None


@dataclass(frozen=True)
class Observation:
    trade_date: date
    contract: str
    early_return: float
    late_return: float
    signed_return: float | None
    signed_points: float | None


def quarterly_front(asof: date, contracts: Sequence[Contract]) -> Contract:
    eligible = sorted(
        (c for c in contracts if c.last_trading_day >= asof),
        key=lambda c: (c.last_trading_day, c.code),
    )
    if not eligible:
        raise ValueError("NO_FRONT_CONTRACT")
    return eligible[0]


def same_front_across_dates(previous: date, current: date, contracts: Sequence[Contract]) -> str | None:
    a = quarterly_front(previous, contracts)
    b = quarterly_front(current, contracts)
    return b.code if a.code == b.code else None


def _validate_trade(t: Trade) -> None:
    if t.timestamp.tzinfo is None:
        raise ValueError("NAIVE_TIMESTAMP")
    if not isfinite(float(t.price)) or t.price <= 0:
        raise ValueError("INVALID_PRICE")
    if t.source_order is not None and (type(t.source_order) is not int or t.source_order < 0):
        raise ValueError("INVALID_SOURCE_ORDER")


def first_trade_at_or_after(
    trades: Iterable[Trade], boundary: datetime, max_delay_seconds: int = 60
) -> Trade | None:
    if boundary.tzinfo is None:
        raise ValueError("NAIVE_BOUNDARY")
    if max_delay_seconds != 60:
        raise ValueError("UNFROZEN_MAPPING_WINDOW")

    end = boundary + timedelta(seconds=max_delay_seconds)
    candidates: list[Trade] = []
    for trade in trades:
        _validate_trade(trade)
        if boundary <= trade.timestamp <= end:
            candidates.append(trade)

    if not candidates:
        return None

    earliest = min(t.timestamp for t in candidates)
    tied = [t for t in candidates if t.timestamp == earliest]
    if len(tied) == 1:
        return tied[0]

    prices = {float(t.price) for t in tied}
    if len(prices) == 1:
        # Same-time duplicates with identical prices do not change the mapped price.
        return sorted(tied, key=lambda t: t.source_order if t.source_order is not None else -1)[0]

    if any(t.source_order is None for t in tied):
        raise AmbiguousTrade("AMBIGUOUS_SAME_TIME_TRADES")

    orders = [t.source_order for t in tied]
    if len(set(orders)) != len(orders):
        raise AmbiguousTrade("AMBIGUOUS_SOURCE_ORDER")

    return min(tied, key=lambda t: int(t.source_order))


def _boundary(d: date, hour: int, minute: int) -> datetime:
    return datetime(d.year, d.month, d.day, hour, minute, tzinfo=JST)


def build_observation(
    previous_date: date,
    current_date: date,
    contract: str,
    trades: Iterable[Trade],
) -> Observation | None:
    trade_list = list(trades)
    p_prev = first_trade_at_or_after(trade_list, _boundary(previous_date, 15, 30))
    p_0930 = first_trade_at_or_after(trade_list, _boundary(current_date, 9, 30))
    p_1500 = first_trade_at_or_after(trade_list, _boundary(current_date, 15, 0))
    p_1530 = first_trade_at_or_after(trade_list, _boundary(current_date, 15, 30))
    if any(x is None for x in (p_prev, p_0930, p_1500, p_1530)):
        return None
    assert p_prev and p_0930 and p_1500 and p_1530

    early = p_0930.price / p_prev.price - 1.0
    late = p_1530.price / p_1500.price - 1.0

    if early > 0:
        signed_return = late
        signed_points = p_1530.price - p_1500.price
    elif early < 0:
        signed_return = -late
        signed_points = p_1500.price - p_1530.price
    else:
        signed_return = None
        signed_points = None

    return Observation(
        trade_date=current_date,
        contract=contract,
        early_return=early,
        late_return=late,
        signed_return=signed_return,
        signed_points=signed_points,
    )


def ols_beta(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float]:
    if len(xs) != len(ys) or len(xs) < 2:
        raise DegenerateSample("INSUFFICIENT_REGRESSION_ROWS")
    if not all(isfinite(float(v)) for v in (*xs, *ys)):
        raise DegenerateSample("NONFINITE_REGRESSION_VALUE")
    mx, my = mean(xs), mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom <= 0:
        raise DegenerateSample("ZERO_PREDICTOR_VARIANCE")
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    alpha = my - beta * mx
    return alpha, beta


class LCG:
    def __init__(self, seed: int):
        self.x = seed & 0xFFFFFFFF

    def index(self, n: int) -> int:
        if n <= 0:
            raise ValueError("EMPTY_POPULATION")
        self.x = (1664525 * self.x + 1013904223) & 0xFFFFFFFF
        return int((self.x / 2**32) * n)


def linear_percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("EMPTY_BOOTSTRAP")
    if not 0 <= q <= 1:
        raise ValueError("INVALID_QUANTILE")
    pos = (len(sorted_values) - 1) * q
    lo = int(pos)
    hi = min(len(sorted_values) - 1, lo + 1)
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def bootstrap_beta(
    observations: Sequence[Observation],
    reps: int = 10_000,
    seed: int = 2252025,
) -> tuple[float, float, int]:
    if reps != 10_000 or seed != 2252025:
        raise ValueError("UNFROZEN_BETA_BOOTSTRAP")
    if len(observations) < 2:
        raise DegenerateSample("INSUFFICIENT_BOOTSTRAP_ROWS")
    rng = LCG(seed)
    stats: list[float] = []
    invalid = 0
    n = len(observations)
    for _ in range(reps):
        sample = [observations[rng.index(n)] for _ in range(n)]
        try:
            _, beta = ols_beta(
                [o.early_return for o in sample],
                [o.late_return for o in sample],
            )
            stats.append(beta)
        except DegenerateSample:
            invalid += 1
    if invalid > reps * 0.01:
        raise DegenerateSample("BOOTSTRAP_DEGENERATE")
    if not stats:
        raise DegenerateSample("NO_VALID_BOOTSTRAP")
    stats.sort()
    return linear_percentile(stats, 0.025), linear_percentile(stats, 0.975), invalid


def bootstrap_signed_mean(
    observations: Sequence[Observation],
    reps: int = 10_000,
    seed: int = 2252026,
) -> tuple[float, float]:
    if reps != 10_000 or seed != 2252026:
        raise ValueError("UNFROZEN_SIGN_BOOTSTRAP")
    values = [o.signed_return for o in observations if o.signed_return is not None]
    if not values:
        raise DegenerateSample("NO_SIGN_TRADES")
    rng = LCG(seed)
    stats: list[float] = []
    n = len(values)
    for _ in range(reps):
        stats.append(mean(values[rng.index(n)] for _ in range(n)))
    stats.sort()
    return linear_percentile(stats, 0.025), linear_percentile(stats, 0.975)


def evaluate_sample(observations: Sequence[Observation], min_rows: int) -> dict:
    n = len(observations)
    if n < min_rows:
        return {"status": "INSUFFICIENT_EVENTS", "n": n}

    alpha, beta = ols_beta(
        [o.early_return for o in observations],
        [o.late_return for o in observations],
    )
    beta_lo, beta_hi, invalid = bootstrap_beta(observations)
    signed = [o.signed_return for o in observations if o.signed_return is not None]
    if not signed:
        return {"status": "NO_SIGN_TRADES", "n": n}
    signed_mean = mean(signed)
    sign_lo, sign_hi = bootstrap_signed_mean(observations)

    supported = beta > 0 and beta_lo > 0 and signed_mean > 0 and sign_lo > 0
    return {
        "status": "SUPPORTED" if supported else "NOT_SUPPORTED",
        "n": n,
        "alpha": alpha,
        "beta": beta,
        "beta_ci": [beta_lo, beta_hi],
        "bootstrap_invalid": invalid,
        "sign_n": len(signed),
        "sign_mean": signed_mean,
        "sign_ci": [sign_lo, sign_hi],
    }
