# Synthetic Test Plan

Status: PRE-OUTCOME

These tests validate mechanics only. Passing them is not evidence of market edge.

Implemented in strategy_semantics.py / test_strategy_semantics.py:

- at least 20 prior completed bars plus one signal bar are required;
- signal-day high/low is excluded from the prior-20 breakout range;
- equality does not trigger;
- long and short comparisons are strict;
- New York 17:00 maps to 06:00 JST in U.S. daylight-saving time and 07:00 JST in standard time for representative 2026 dates;
- the proposed 20:00 JST review therefore has 14h summer / 13h winter delay;
- execution window is exactly 20:00–20:05 JST;
- exit architecture must be explicitly WEEKEND_FLAT or TEN_CHECK_HOLD; BOTH/AUTO/blank is invalid.

Still required before historical replay:

- ATR warm-up and first-prev-close semantics;
- stop crossing and quote-side precedence;
- missing quote / market closure behavior;
- opposite signal vs time-exit precedence;
- WEEKEND_FLAT Friday entry/exit boundary if that mode is selected;
- broker quantity and swap integration with the already migrated quantity tests.