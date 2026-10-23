---
type: ResearchLine
research_line_id: RL-JP225-PROSPECTIVE-001
status: PROPOSED_NOT_FROZEN
created_at: 2026-10-05
---

# JP225 Intraday Prospective Forecast v0.1

## Purpose

Run a prospectively timestamped JP225 forecast-and-review loop parallel in method to the USD/JPY prospective forecast line, while keeping it scientifically separate from existing JP225 strategy research.

The candidate asks whether a frozen AI forecasting system can predict the sign of the same-day XM MT5 `JP225Cash` move from 09:00 JST to 15:30 JST better than simple baselines and a market-only AI comparator.

This is a forecast-quality experiment, not a trading strategy and not an order-execution system.

## Separation from existing JP225 lines

This line must not rewrite, tune, or consume the evaluation boundaries of:

- `jp225-ema-timeofday-v0.1`;
- `jp225-us-lead-reversal-v0.1`;
- the quarantined/deferred JP225 intraday-momentum / DataCube work preserved in PR #59.

Existing research may enter A3 only through a pinned, status-preserving pre-cutoff repository snapshot. UNTESTED, negative/null, proxy-only, BLOCKED, consumed, and quarantined labels must remain intact.

## Candidate event

- timezone: Asia/Tokyo;
- eligible date: scheduled JPX cash-equity trading day;
- forecast information cutoff / intended issuance: 08:00 JST;
- target start: 09:00 JST;
- target end: 15:30 JST;
- reference instrument: exact XM MT5 `JP225Cash`;
- reference quote: qualified best Bid/Ask midpoint;
- primary probabilistic target: whether 15:30 midpoint is above 09:00 midpoint;
- primary score: Brier score.

JPX currently defines cash-equity sessions as 09:00–11:30 and 12:30–15:30. This market-calendar role does not imply that JPX cash-index data are interchangeable with XM `JP225Cash`.

## Comparison family

- B0: neutral no-change baseline.
- A1: JP225 market-only AI.
- A2: JP225 market + frozen cross-market/fundamentals/news AI.
- A3: A2 plus pinned status-preserving relevant repository research.

Primary comparison: A3 versus A1.
Baseline sanity: A3 versus B0.
Research-layer comparison: A3 versus A2.

## Cohort

- frozen benchmark: 60 matched valid events;
- challenger reviews after matched events 20 and 40;
- v0.1 benchmark remains unchanged through event 60;
- no early stop because results look favorable or unfavorable.

## Current boundary

The exact XM source/readiness gate has not passed. Therefore the line starts as PROPOSED_NOT_FROZEN.

Before the first scored event, exact XM symbol identity, Bid/Ask timestamp semantics, JST/server-time mapping, endpoint quote retrieval, append-preserving records, and deterministic scoring must pass the readiness gate.

Until then, same-day forecasts may be recorded only as exploratory prospective dry runs clearly marked NOT_IN_COHORT. Missing exact XM outcome data must be recorded as unavailable rather than replaced with another provider or index.

No broker order, paper order, position sizing, or live-capital action is authorized.
