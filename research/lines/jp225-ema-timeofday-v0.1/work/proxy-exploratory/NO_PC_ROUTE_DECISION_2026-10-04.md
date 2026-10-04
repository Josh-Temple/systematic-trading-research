---
id: DEC-JP225-NO-PC-ROUTE-20261004
type: Decision
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: ACTIVE
---

# No-PC continuation decision

## Constraint

The user currently cannot use a Windows PC. Exact XM MT5 JP225Cash Stage 1 therefore cannot be collected now.

Current public/mobile documentation supports chart/history viewing on mobile, while the documented historical bar/tick export path is a PC MT5 workflow. No exact mobile XM BID/ASK history export route has been established.

## Decision

Do not relax the XM source gate and do not substitute another broker as XM evidence.

Continue a separate **proxy research lane** using previously unused OANDA-derived JP225 midpoint M1 years, with a genuinely new pre-registered mechanism rather than parameter rescue on consumed 2018–2020 samples.

The exact XM line remains:
- HYPOTHESIS = UNTESTED
- Packet A = PARTIAL_WITH_GAPS
- Packet C = LOCKED
- 2026 holdout = UNTOUCHED / LOCKED

## New proxy candidate

Test one anti-whipsaw modification close to the original EMA5/EMA200 idea:

**Require the post-cross EMA ordering to persist for five complete M1 bars before entry.**

The number five is tied to the fixed fast EMA span and is not selected from market outcomes.

No time-of-day, weekday, side, volatility, stop, target, or EMA-length search is allowed.

Use 2017 as the first untouched proxy test year. If and only if it passes the frozen support criterion, freeze an exact 2016 replication before reading 2016 outcomes.
