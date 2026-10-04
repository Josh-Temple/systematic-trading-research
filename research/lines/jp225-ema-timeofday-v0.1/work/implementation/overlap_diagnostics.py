from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence


def overlap_diagnostics(
    signal_closes: Sequence[datetime],
    horizon_minutes: int = 15,
) -> tuple[int, float]:
    """Return event count/share whose forward windows overlap another event."""
    if horizon_minutes <= 0:
        raise ValueError("horizon_minutes must be positive")
    times = sorted(signal_closes)
    if any(t.tzinfo is None for t in times):
        raise ValueError("signal timestamps must be timezone-aware")
    if not times:
        return 0, 0.0

    flagged = [False] * len(times)
    horizon = timedelta(minutes=horizon_minutes)
    for i in range(len(times) - 1):
        if times[i + 1] < times[i] + horizon:
            flagged[i] = True
            flagged[i + 1] = True

    count = sum(flagged)
    return count, count / len(times)
