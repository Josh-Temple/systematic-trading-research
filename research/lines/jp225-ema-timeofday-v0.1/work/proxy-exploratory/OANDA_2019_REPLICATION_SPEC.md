---
id: SPEC-JP225-PROXY-OANDA-2019-REPLICATION
type: HistoricalReplicationSpecification
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: FROZEN_BEFORE_2019_OUTCOME_ACCESS
xm_execution_evidence: false
---

# OANDA JP225 historical-close replication — 2019

## Why this exists

The 2020 partial-year proxy exploration produced a post-hoc positive observation for 14:45–15:15 JST. This specification freezes one exact historical replication before reading or calculating the 2019 JP225 outcome.

It is not prospective market evidence and not a substitute for XM validation. Its role is to test whether the candidate immediately collapses in a separate historical year.

## Source

Use only the public `FutureSharks/financial-data` OANDA `JP225_USD` M1 files under the 2019 directory.

Preserve every source blob SHA used.

## Signal

- M1
- EMA(5) / EMA(200)
- identical recursive EMA semantics
- first 1,000 available chronological bars as warm-up
- long: prior EMA5 <= EMA200 and current EMA5 > EMA200
- short: prior EMA5 >= EMA200 and current EMA5 < EMA200

## Primary window

Signal-close time:

`14:45 <= Asia/Tokyo < 15:15`

No other time window may be selected from 2019 outcomes.

## Outcome

Gross +15-minute directional points using the same bar proxy:

- signal close = current bar timestamp + 1 minute
- entry = next exact minute bar OPEN
- exit = exact bar OPEN 15 minutes after signal close
- missing exact bars => missing outcome, no imputation
- long signed +1, short -1

No assumed spread is subtracted because this source does not provide the XM BID/ASK spread.

## Primary replication criterion

Classify `HISTORICAL_PROXY_REPLICATED` only if all hold:

1. >= 50 valid events
2. >= 30 distinct Asia/Tokyo dates
3. mean gross +15m directional points > 0
4. day-cluster bootstrap 95% lower bound > 0

Bootstrap:

- Asia/Tokyo calendar-date clusters
- 10,000 replications
- seed 2255200
- percentile 2.5% / 97.5%

Otherwise classify `HISTORICAL_PROXY_NOT_REPLICATED` or `INSUFFICIENT_PROXY_EVENTS`.

## Comparator

Run price/EMA200 in the same 14:45–15:15 JST window descriptively. It cannot rescue the EMA result.

## Baselines

For context only, report EMA5/EMA200:

- ALL
- 08:45–09:15 JST

These baselines are not eligible to replace the primary replication window.

## Stop rule

Do not search 2019 by hour, weekday, alternative EMA, horizon, stop/target, or another window.

If the historical-close candidate fails, record the failure and stop this candidate.

If it passes, a second exact-year replication may be preregistered before accessing 2018 outcomes. Passing 2019 alone still does not establish XM tradability.
