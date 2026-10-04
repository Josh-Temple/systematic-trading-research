---
id: SPEC-JP225-PROXY-PERSIST5-2017
type: HistoricalProxyTestSpecification
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: FROZEN_BEFORE_2017_OUTCOME_ACCESS
xm_execution_evidence: false
---

# EMA5/EMA200 cross + 5-bar persistence — 2017

## Research question

Does a five-complete-bar persistence requirement after an M1 EMA(5)/EMA(200) crossover reduce short-lived whipsaw enough to produce positive +15-minute gross continuation in a previously uncalculated OANDA-derived JP225 historical year?

This is a separate proxy hypothesis. It is not a change to the frozen XM v0.1 specification.

## Source

Use only public `FutureSharks/financial-data` OANDA `JP225_USD` M1 files under the 2017 directory.

Preserve:
- external repository commit/ref used;
- monthly Git blob SHA;
- row counts;
- first/last timestamps;
- source-to-result receipt.

These candles are midpoint OHLCV proxy data, not executable XM BID/ASK history.

## EMA

- input = M1 close
- EMA fast span = 5
- EMA slow span = 200
- alpha = 2/(span+1)
- recursive update
- seed both EMAs with first valid chronological close
- no session reset
- first 1,000 source rows are warm-up and cannot generate a cross event

## Base crossover

At source bar index `t`:

Long cross:
- EMA5[t-1] <= EMA200[t-1]
- EMA5[t] > EMA200[t]

Short cross:
- EMA5[t-1] >= EMA200[t-1]
- EMA5[t] < EMA200[t]

## Five-bar persistence requirement

After a base cross at bar `t`, require the next **five complete chronological source minutes** `t+1 ... t+5` to exist at exact one-minute timestamps.

Long:
- EMA5 > EMA200 on every bar t+1 through t+5.

Short:
- EMA5 < EMA200 on every bar t+1 through t+5.

If any of those five exact minute bars is missing, the candidate is classified `CONFIRMATION_GAP` and has no outcome.

If the ordering fails on any confirming bar, classify `PERSISTENCE_FAILED` and do not enter.

No requirement is placed on slope magnitude, candle color, price return, volume, or distance from EMA200.

## Signal and entry timing

For source bars, the timestamp denotes the bar open.

A bar's EMA value is knowable only after that bar completes.

For a base cross at bar `t`:
- cross knowledge time = open[t] + 1 minute;
- five confirmation bars are t+1 ... t+5;
- confirmation knowledge time = open[t+5] + 1 minute;
- entry = OPEN of exact bar t+6.

Thus entry occurs only after all five confirmation bars have completed.

## Outcome

Primary horizon:
- exact OPEN 15 minutes after the entry timestamp.

Directional gross points:
- long = exit_open - entry_open
- short = entry_open - exit_open

Requirements:
- exact entry minute must exist;
- exact target minute must exist;
- no interpolation;
- no forward fill;
- no nearest-bar substitution.

This is midpoint gross movement only. No spread, commission, slippage or XM markup is assumed.

## Time scope

ALL eligible source times.

No time-of-day selection is allowed.

## Primary support criterion

Classify `PERSIST5_PROXY_SUPPORTED_2017` only if all hold:

1. >= 500 valid outcomes;
2. >= 150 distinct Asia/Tokyo calendar dates;
3. mean +15m directional gross points > 0;
4. day-cluster bootstrap 95% lower bound > 0.

Otherwise:
- `INSUFFICIENT_PROXY_EVENTS`, or
- `PERSIST5_PROXY_NOT_SUPPORTED_2017`.

## Bootstrap

Cluster = Asia/Tokyo calendar date of entry.

Deterministic algorithm:
- 10,000 replications;
- sample dates with replacement;
- include all events belonging to each sampled date;
- seed = 2255200;
- RNG = 32-bit LCG:
  - x0 = seed unsigned 32-bit;
  - x[n+1] = (1664525*x[n] + 1013904223) mod 2^32;
  - U = x / 2^32;
- percentile interpolation = linear between adjacent sorted bootstrap means at position (N-1)*q;
- q = 0.025 and 0.975.

This fully specifies the historical proxy bootstrap and does not alter the frozen XM bootstrap implementation.

## Comparator

Report the unfiltered EMA5/EMA200 cross on 2017 using the same +15m bar-open gross outcome, for descriptive context only.

Comparator performance cannot rescue a failed persistence result.

## Cost interpretation

If mean gross points are positive, they are the maximum average round-trip cost budget before mean expectancy reaches zero in this midpoint proxy.

Do not infer actual XM net expectancy.

## Stop rule

Do not inspect or select:
- alternative persistence lengths;
- EMA lengths;
- time windows;
- weekdays;
- long-only or short-only variants;
- volatility filters;
- stop loss;
- take profit;
- trailing stop;
- different horizons.

If the primary 2017 test fails, stop this candidate.

If it passes, commit an exact 2016 replication specification before accessing 2016 outcome data.
