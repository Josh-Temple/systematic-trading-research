# Data Contract — USD/JPY Daily Breakout

Status: DRAFT / PRE-OUTCOME / NOT_ACCEPTED

## Separation of roles

Reference/signal data and broker execution evidence are distinct.

- Reference feed: defines the New York 17:00 daily Bid OHLC used for the 20-day breakout and ATR.
- Execution feed: provides executable Bid/Ask and path information needed for entry, stop, exit, spread, slippage and swap analysis.
- XM and Matsui may be evaluated separately as execution environments. A research reference feed must not be silently replaced by whichever broker history is easiest to export.

## Required inputs

| Input | Minimum fields | Purpose |
|---|---|---|
| Daily Bid bars | timestamp/open/high/low/close, timezone/boundary identity, source id | 20-day breakout and ATR |
| Executable quotes | timestamped Bid/Ask around each candidate entry and exit, plus sufficient path resolution for stop detection | executable replay |
| Trading calendar | holidays, broker unavailable intervals, DST-aware time mapping | prevent invented bars/orders |
| Symbol specification | minimum units/lot, volume step, contract size, quote currency, margin rules | broker-specific feasibility |
| Costs | spread, commission if any, swap by side/date, explicitly modeled slippage | after-cost replay |
| Provenance | source URL/provider, retrieval UTC, file hash where persistable, permissions | reproducibility |

## Time semantics

- Daily bars must represent a New York 17:00 boundary. UTC-midnight bars are not an automatic substitute.
- America/New_York daylight saving rules must be applied from a timezone database or equivalent deterministic source; do not hard-code a fixed UTC offset for all dates.
- 20:00 JST execution is a delayed action after the completed daily signal, not a same-close fill.
- If no executable quote exists in 20:00–20:05 JST, the entry is SKIP rather than filled by forward-fill or a later convenient quote.

## Bid/Ask semantics

- Signal series: Bid OHLC as currently proposed.
- Long entry uses Ask; long exit uses Bid.
- Short entry uses Bid; short exit uses Ask.
- A spread already embedded in executable entry/exit prices must not be added again as a separate duplicate charge.
- Mid prices may be used only for explicitly labeled diagnostics, never as the default execution series.

## Stop replay

Daily OHLC alone is insufficient for precise stop execution under this design. Historical acceptance requires enough intraday executable-price information to establish whether and when the stop was crossed. If path identity is unavailable, the replay is BLOCKED rather than approximated silently.

## Missing-data behavior

- Missing daily bar: no signal calculation for an affected lookback until the source/calendar discrepancy is resolved.
- Missing entry-window quote: SKIP.
- Missing stop/exit quote or unresolved broker closure: BLOCKED for that event under the current contract; do not infer from midpoint or another provider after outcomes are known.
- Do not create artificial holiday bars or carry forward a previous quote to manufacture tradability.

## Source acceptance gate

Before market-outcome computation, record: exact provider/feed, instrument identity, date coverage, daily-boundary verification, quote-side semantics, retrieval method, rights/retention boundary, missingness diagnostics, and hashes where possible.

Passing source qualification does not imply the strategy has an edge.