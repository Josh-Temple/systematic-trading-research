# Specification Draft v0.1 — USD/JPY Daily Breakout

Status: DRAFT / NOT_FROZEN / HUMAN_BOUNDARY
Market outcome access under this specification: NO

## Research question

Under a predeclared USD/JPY daily breakout rule and small-account execution constraints, does a deterministic trend-following candidate produce after-cost outcomes that justify further prospective observation, relative to preregistered comparators?

This question is not yet confirmatory because the exit architecture, sample, comparators, metric thresholds, and accepted data source remain incomplete.

## Candidate signal

Instrument: USD/JPY.
Bar boundary: New York 17:00, DST-aware.
Price side for signal: Bid OHLC from one accepted reference feed.

Long signal at review t: latest completed daily Bid close > maximum Bid high of the immediately preceding 20 completed daily bars, excluding the signal day.
Short signal at review t: latest completed daily Bid close < minimum Bid low of the immediately preceding 20 completed daily bars, excluding the signal day.
Equality produces no signal.

ATR: Wilder ATR(14), using TR=max(high-low, abs(high-prev_close), abs(low-prev_close)); initialize with arithmetic mean of first 14 TR values, then recursive Wilder update. No signal until both the 20-bar breakout lookback and ATR initialization are available.

## Review and entry

Normal human review: 20:00 JST on eligible weekdays.
Execution candidate: first available executable quote from 20:00:00 through 20:05:00 JST after the signal is known.
Quote side: long entry Ask; short entry Bid.
If no quote exists in the window, SKIP. Do not delay-fill outside the window.

20:00 JST is intentionally delayed from the New York 17:00 daily close by roughly 13–14 hours depending on U.S. DST. Historical replay must use that actual delay.

## Risk mechanics

Initial stop distance: 2 x ATR(14) from actual executable entry price.
Long stop below entry; short stop above entry.
Stop is never widened to satisfy minimum size.
No fixed take-profit.
No trailing stop.
No averaging down, martingale, rescue hedging, or discretionary override.

## Position count and sizing candidate

Maximum one open position per broker account.
Candidate live capital context: XM Micro 10,000 JPY and Matsui FX 10,000 JPY, subject to later explicit human confirmation.
Draft effective-leverage cap: 2x self-equity.
Draft per-trade planned-loss budget: 50 JPY per account when used alone; when both accounts take the same directional exposure, combined planned loss must remain <=50 JPY, which may make one or both brokers SKIP.
Broker minimum/step constraints are applied by rounding quantity down. Minimum size never forces a tighter stop.

These monetary limits are risk-control proposals, not evidence-derived optimal parameters and not yet accepted live authority.

## Exit architecture — unresolved

Exactly one of the following must be chosen before outcome access:

A. WEEKEND_FLAT: no Friday new entry; force close Friday 23:00 JST; opposite signal may close earlier; remove the 10-check time exit.

B. TEN_CHECK_HOLD: no Friday forced close; close on opposite signal or at the 10th weekday 20:00 review after entry; entry-day review is check 0.

Current status: NO_SAFE_DEFAULT / HUMAN_BOUNDARY.

## Re-entry

No immediate same-review reversal. After an exit, a later review may create a new candidate only if the normal signal rule is satisfied.

## Broker-specific execution

XM and Matsui are evaluated separately for executable prices, size constraints, swap and fees. Broker execution differences must not change the scientific signal definition.

## Pre-outcome work still required

1. Human selects exit architecture.
2. Qualify exact reference and execution data sources.
3. Freeze historical sample and warm-up period.
4. Freeze cash and USD/JPY buy-and-hold comparators plus a prospective-risk comparison method.
5. Freeze cost model and broker-specific swap/slippage handling.
6. Freeze primary metric(s), numeric decision thresholds and stopping/kill conditions.
7. Add synthetic tests for DST, lookback exclusion, missing data, execution delay and exit precedence.

## Interpretation boundary

A profitable historical replay would not by itself establish future profitability. A negative/null result remains valid. No parameter, lookback, stop multiple, weekday, time, subset, broker, or exit architecture may be changed after outcome inspection and retested on the same sample as if confirmatory.

## Live boundary

No broker connection, automatic order submission, automatic live position sizing, or live-capital authorization is created by this document.