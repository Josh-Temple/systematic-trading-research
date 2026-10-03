"""Deterministic pre-outcome semantics for the USD/JPY daily-breakout proposal.

No market data, broker connection, signals from real prices, or orders are used here.
"""
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
JST = ZoneInfo("Asia/Tokyo")

ALLOWED_EXIT_MODES = {"WEEKEND_FLAT", "TEN_CHECK_HOLD"}


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
    """Return the proposed 20:00-20:05 JST execution window after NY close."""
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
    """Require exactly one preregistered exit architecture."""
    if mode not in ALLOWED_EXIT_MODES:
        raise ValueError("exit mode must be WEEKEND_FLAT or TEN_CHECK_HOLD")
    return mode