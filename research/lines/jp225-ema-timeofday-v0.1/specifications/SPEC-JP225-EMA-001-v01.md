---
id: SPEC-JP225-EMA-001-v01
type: StrategyExperimentSpecification
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-03
status: DRAFT_PRE_OUTCOME
market_outcome_access: false
---

# JP225 M1 EMA5/EMA200 Time-of-Day — Specification v0.1

## 1. Instrument and source

Target execution instrument: XM MT5 `JP225Cash`.

Source qualification must record broker/entity/account server name, terminal build, exact symbol, digits/tick size/contract size if exposed, server timestamp semantics and timezone/DST rule, bar/tick coverage, export method/time, and raw file hashes. Do not infer server timezone from visual clock resemblance.

## 2. Data roles

- Warm-up: history beginning no later than 2024-12-01 and at least 1,000 valid quoted M1 bars before first evaluated signal.
- Discovery: 2025-01-01 through 2025-12-31 UTC after timestamps are resolved.
- Holdout: 2026-01-01 through 2026-09-30 UTC.

Holdout bytes may be preserved early if needed, but no outcome-bearing calculation, plot, signal count, event count, or summary may be produced before a discovery advancement decision is durably recorded.

## 3. Signal series

Preferred signal series is broker chart-equivalent BID M1. If reconstructed from BID ticks, the implementation must verify or explicitly leave unresolved whether it matches the XM chart-bar semantic. Missing minutes are not forward-filled and session gaps remain gaps.

## 4. EMA semantics

For span N: `alpha = 2 / (N + 1)`.

`EMA_t = alpha * close_t + (1 - alpha) * EMA_(t-1)`.

Seed: first valid close in the warm-up stream. EMAs do not reset at session boundaries.

Spans: fast=5, slow=200. No alternatives are evaluated in v0.1.

## 5. Crossover events

Signal timestamp is M1 bar close time.

Long: prior EMA5 <= prior EMA200 and current EMA5 > current EMA200.

Short: prior EMA5 >= prior EMA200 and current EMA5 < current EMA200.

Events are not deleted because another crossover occurs before the horizon. This is an event study; overlapping-event dependence is reported and inference clusters by date.

## 6. Comparator

Price/EMA200 comparator:

- long: prior close <= prior EMA200 and current close > current EMA200;
- short: prior close >= prior EMA200 and current close < current EMA200.

## 7. Executable quote mapping

Entry is the first valid quote strictly after signal close and within 60 seconds.

- long entry = ASK
- short entry = BID

Targets are signal close +5, +15, +30 minutes.

Exit is first valid quote at or after target and no later than target +60 seconds.

- long exit = BID
- short exit = ASK

Missing entry => `NO_EXECUTABLE_ENTRY_QUOTE`.
Missing target => `NO_EXECUTABLE_TARGET_QUOTE`.
No imputation.

## 8. Metrics

Direction = +1 long, -1 short.

`net_points = direction * (exit_price - entry_price)`.

Report also midpoint gross diagnostic, quoted entry/exit spread, net bps relative to entry midpoint, and win indicator.

Primary metric: mean +15m quote-net directional points.

Supporting: median, win rate, event count, distinct Asia/Tokyo dates, day-cluster bootstrap 95% interval, overlap count/share, and break-even additional round-trip cost when defined.

No annualized Sharpe or account-level P/L in v0.1.

## 9. Time classification

Use signal close timestamp.

Selectable:
- `ALL`
- `TOKYO_OPEN_30`: 08:45 <= Asia/Tokyo < 09:15
- `TOKYO_CLOSE_30`: 15:15 <= Asia/Tokyo < 15:45

Descriptive only:
- `OSE_NIGHT_OPEN_30`: 17:00 <= Asia/Tokyo < 17:30
- `US_CASH_OPEN_60`: 09:30 <= America/New_York < 10:30
- `OTHER`

No new clock boundary may be discovered from 2025 outcomes.

## 10. Discovery advancement rule

Run 2025 once after source and implementation gates pass.

A selectable candidate advances only if:

1. >=100 valid executable events;
2. >=60 distinct Asia/Tokyo calendar dates;
3. mean +15m quote-net points > 0;
4. day-cluster bootstrap 95% lower bound > 0.

If multiple qualify, select the largest mean. Ties within 0.01 point use broader-window order: ALL, TOKYO_OPEN_30, TOKYO_CLOSE_30.

If none qualifies: `NO_ADVANCEMENT`; do not open holdout.

## 11. Holdout

Test only the selected candidate on 2026-01-01 through 2026-09-30.

Support requires:

1. >=50 executable events;
2. >=30 distinct Asia/Tokyo dates;
3. mean +15m quote-net points > 0;
4. day-cluster bootstrap 95% lower bound > 0.

Insufficient events => `INSUFFICIENT_HOLDOUT_EVENTS`.

Secondary horizons/comparator cannot rescue the primary holdout.

## 12. Bootstrap

Resample Asia/Tokyo calendar dates with replacement, retaining all events in each sampled date.

- replications: 10,000
- seed: 2255200
- percentile interval: 2.5%, 97.5%

## 13. Source fallback

Do not silently replace XM JP225Cash with Dukascopy JPN.IDX/JPY, Nikkei 225 futures, ^N225, TradingView history, or another broker CFD. A proxy requires a separate instrument definition and cannot establish XM execution-specific economics.

## 14. Forbidden rescue

After outcomes are seen, do not alter EMA lengths, windows, horizon, side, weekday, stop/target, slope/volatility/news filters, warm-up, quote mapping, or sample dates to rescue v0.1.

## 15. Live boundary

No order placement, account connection, leverage selection, or position sizing is authorized.
