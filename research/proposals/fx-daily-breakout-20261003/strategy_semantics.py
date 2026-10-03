"""Deterministic pre-outcome semantics for the USD/JPY daily-breakout proposal.

No market data, broker connection, signals from real prices, or orders are used here.
"""
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
JST = ZoneInfo("Asia/Tokyo")
ACTIVE_EXIT_MODE = "WEEKEND_FLAT"


def breakout_signal(completed_bars):
    """Return LONG, SHORT, NONE, or INSUFFICIENT.

    The last bar is the signal day. The immediately preceding 20 completed
    bars form the breakout lookback; the signal-day high/low is excluded.
    """
    if len(completed_bars) < 21:
        return "INSUFFICIENT"
    prior = completed_bars[-21:-1]
    current = completed_bars[-1]
    prior_high = max(bar["high"] for bar in prior)
    prior_low = min(bar["low"] for bar in prior)
    close = current["close"]
    if close > prior_high:
        return "LONG"
    if close < prior_low:
        return "SHORT"
    return "NONE"


def ny_close_jst(ny_session_date: date) -> datetime:
    """Map New York 17:00 for a session date to timezone-aware JST."""
    local = datetime.combine(ny_session_date, time(17, 0), tzinfo=NY)
    return local.astimezone(JST)


def review_window_jst(ny_session_date: date):
    """Return the proposed 20:00-20:05 JST entry window after NY close."""
    close_jst = ny_close_jst(ny_session_date)
    start = datetime.combine(close_jst.date(), time(20, 0), tzinfo=JST)
    end = datetime.combine(close_jst.date(), time(20, 5), tzinfo=JST)
    return start, end


def review_delay_hours(ny_session_date: date) -> float:
    """Hours from New York 17:00 close to proposed 20:00 JST review."""
    close_jst = ny_close_jst(ny_session_date)
    start, _ = review_window_jst(ny_session_date)
    return (start - close_jst).total_seconds() / 3600


def validate_exit_mode(mode: str) -> str:
    """Require the human-selected WEEKEND_FLAT exit architecture."""
    if mode != ACTIVE_EXIT_MODE:
        raise ValueError("active exit mode is WEEKEND_FLAT")
    return mode


def is_new_entry_allowed(review_at_jst: datetime) -> bool:
    """Allow new entries only Monday-Thursday at the normal JST review."""
    if review_at_jst.tzinfo is None:
        raise ValueError("review time must be timezone-aware")
    local = review_at_jst.astimezone(JST)
    return local.weekday() in (0, 1, 2, 3)


def weekend_forced_exit_at(review_date_jst: date):
    """Return Friday 23:00 JST forced-close request time, otherwise None."""
    if review_date_jst.weekday() != 4:
        return None
    return datetime.combine(review_date_jst, time(23, 0), tzinfo=JST)
