---
id: SPEC-JP225-PROXY-EMA200-SLOPE-2018
type: HistoricalProxyTestSpecification
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: FROZEN_BEFORE_2018_OUTCOME_ACCESS
xm_execution_evidence: false
---

# EMA5/EMA200 cross with aligned EMA200 slope — 2018

## Question

Does requiring the slow EMA to already move in the crossover direction remove enough range-whipsaw noise for the M1 EMA(5)/EMA(200) crossover to show positive +15-minute gross continuation in a previously uncalculated OANDA JP225 historical year?

## Source

Use only `FutureSharks/financial-data` OANDA `JP225_USD` M1 files in the 2018 directory.

Preserve source blob SHAs.

## Signal

Use the same recursive EMA semantics.

Base cross:
- long: prior EMA5 <= prior EMA200 and current EMA5 > current EMA200
- short: prior EMA5 >= prior EMA200 and current EMA5 < current EMA200

Aligned-slope filter:
- long eligible only if current EMA200 > prior EMA200
- short eligible only if current EMA200 < prior EMA200

No slope magnitude threshold and no additional lookback are allowed.

## Time scope

**ALL eligible source times.**

No hour/session/weekday filter is allowed in this test.

## Outcome

Same midpoint-bar proxy:

- signal close = source M1 timestamp + 1 minute
- entry = exact next-minute OPEN
- exit = exact OPEN at signal close +15 minutes
- no imputation
- gross signed index points

## Primary criterion

Classify `SLOPE_FILTER_PROXY_SUPPORTED_2018` only if all hold:

1. >= 500 valid outcomes
2. >= 150 distinct Asia/Tokyo dates
3. mean gross +15m directional points > 0
4. day-cluster bootstrap 95% lower bound > 0

Bootstrap:
- 10,000 replications
- Asia/Tokyo calendar-date clusters
- seed 2255200

Otherwise classify `SLOPE_FILTER_PROXY_NOT_SUPPORTED_2018` or `INSUFFICIENT_PROXY_EVENTS`.

## Comparator

Report the unfiltered EMA5/EMA200 cross on the same 2018 data descriptively.

The comparator cannot rescue a failed slope-filter result.

## Cost interpretation

No spread is assumed.

If the gross result is positive, report the mean gross points as the **maximum break-even budget** for all unmeasured round-trip costs. Actual XM BID/ASK evidence is still required.

## Stop rule

Do not test:
- alternative slope lookbacks;
- slope thresholds;
- EMA variants;
- time windows;
- stop/target variants;
- side-specific rescue.

If this test fails, stop this candidate.

If it passes, freeze an exact 2017 historical replication before accessing 2017 outcomes.
