# Human Decision Receipt — WEEKEND_FLAT

Decision date: 2026-10-03 JST
Source: human instruction in Chat
Market outcome access before decision: NO in this proposal workflow

## Decision

The selected exit architecture is WEEKEND_FLAT.

- Friday new entries are disabled.
- Existing positions receive a forced-close request at Friday 23:00 JST unless already closed earlier by the initial stop or an opposite signal.
- The 10-weekday-check time exit is removed from the active candidate.
- TEN_CHECK_HOLD remains preserved only as the unselected historical alternative in HUMAN_DECISION_PACKET_2026-10-03.md.

## Scope of this decision

This decision fixes the exit architecture only. It does not by itself approve live trading, the draft monetary risk limits, the 20:00 JST operational schedule, a data source, historical sample, comparator, cost model, primary metric, or acceptance/rejection threshold.

## Research boundary

The selected exit architecture must not be changed after market-outcome inspection and then retested on the same historical sample as if it had been preregistered. Any later change requires a new version and an unused/prospective evaluation path.

The historical decision packet remains unchanged.