# Synthetic Test Plan

Status: PRE-OUTCOME
Selected exit architecture: WEEKEND_FLAT

These tests validate mechanics only. Passing them is not evidence of market edge.

Implemented in strategy_semantics.py / test_strategy_semantics.py:

- at least 20 prior completed bars plus one signal bar are required;
- signal-day high/low is excluded from the prior-20 breakout range;
- equality does not trigger;
- long and short comparisons are strict;
- New York 17:00 maps to 06:00 JST in U.S. daylight-saving time and 07:00 JST in standard time for representative 2026 dates;
- the proposed 20:00 JST review therefore has 14h summer / 13h winter delay;
- entry window is exactly 20:00–20:05 JST;
- WEEKEND_FLAT is the only active exit mode; TEN_CHECK_HOLD is rejected by current semantics;
- Friday 20:00 new entry is disabled;
- Monday–Thursday new entries remain eligible;
- Friday forced-close request is scheduled for 23:00 JST.

Still required before historical replay:

- ATR warm-up and first-prev-close semantics;
- stop crossing and quote-side precedence;
- missing quote / market closure behavior;
- opposite-signal close versus Friday 23:00 forced-close precedence;
- executable-price/no-quote behavior at Friday 23:00;
- broker quantity and swap integration with the already migrated quantity tests.