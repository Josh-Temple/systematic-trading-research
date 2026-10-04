---
id: RESULT-JP225-PROXY-OANDA-2020
type: ExploratoryResult
research_line_id: RL-JP225-EMA-001
created_at: 2026-10-04
status: EXPLORATORY_PROXY_ONLY
scientific_status: NOT_CONFIRMATORY
xm_execution_evidence: false
---

# OANDA JP225 M1 proxy exploration — 2020 partial-year

## Purpose and boundary

The exact XM MT5 `JP225Cash` source remains unavailable in the Chat execution environment. At the human's instruction to continue with available data, a public OANDA-derived JP225 M1 dataset was used as a **proxy exploratory screen only**.

This result is not Packet C, does not satisfy the XM source gate, and must not be interpreted as XM spread-aware profitability evidence.

## Source

Repository: `FutureSharks/financial-data`

README states that JP225 is among the 2005–2020 instruments sourced from OANDA.

The repository's `oanda_prices.py` requests candles using UTC UNIX boundaries, receives OANDA UNIX timestamps, and converts those values with `pandas.to_datetime(..., unit='s')`. Time-of-day diagnostics therefore treat the stored timestamps as UTC.

2020 source blobs:

- `c0620e4944ef0368c5b845252375696849322949`
- `e49c72f09c390c41edbff83efa8767058b934650`
- `01b07fa0b5792c03a09a398b03ba7dfb3b7ba257`
- `53930fa5db482dc290435f55c77047d851a741cc`
- `d9869a3ebb4c9f5f8814eabcb3da50e83ac8bb0e`

Observed combined coverage after timestamp deduplication:

- rows: 117,975
- first: 2020-01-01 23:00 UTC
- last: 2020-05-14 07:59 UTC

Important: despite the year path, this snapshot is only a partial 2020 sample through May 14.

## Calculation

- M1 close series
- EMA spans 5 and 200
- recursive EMA, alpha = 2/(N+1)
- first 1,000 rows treated as warm-up
- crossover signal at bar close
- gross proxy entry = next exact M1 bar open
- gross proxy exit = exact bar open 15 minutes after signal close
- missing required timestamps are not imputed
- no BID/ASK spread, commission, slippage, or XM markup
- cluster bootstrap by Asia/Tokyo calendar date
- 5,000 bootstrap replications, seed 2255200

This bar-open proxy is not the frozen XM tick-execution mapping and is therefore separately labeled.

## EMA5/EMA200 results

| Window | Valid n | Dates | Mean gross points | Median | Win rate | Day-cluster 95% CI |
|---|---:|---:|---:|---:|---:|---|
| ALL | 2,096 | 113 | +1.1533 | 0.0 | 47.76% | [-0.5503, +2.9981] |
| 08:45–09:15 JST | 71 | 38 | -4.2887 | -1.7 | 47.89% | [-18.2067, +10.9364] |
| 09:00–09:30 JST | 78 | 34 | -5.4833 | -7.2 | 39.74% | [-17.0250, +8.3870] |
| 14:45–15:15 JST | 59 | 35 | +23.3254 | +3.2 | 54.24% | [+5.4435, +48.0456] |

Total EMA crossover events: 2,377. Valid +15m events: 2,096. Missing exact-entry/target-bar events: 281.

## Price/EMA200 comparator

| Window | Valid n | Dates | Mean gross points | Day-cluster 95% CI |
|---|---:|---:|---:|---|
| ALL | 4,634 | 113 | +0.4090 | [-0.4235, +1.2775] |
| 08:45–09:15 JST | 166 | 50 | -3.8145 | [-9.2460, +1.9252] |
| 09:00–09:30 JST | 170 | 45 | -3.2741 | [-8.7447, +2.8270] |
| 14:45–15:15 JST | 123 | 45 | +10.3244 | [+2.9373, +19.7452] |

## Interpretation

### Fact

The broad all-time EMA5/EMA200 proxy result is small and statistically compatible with zero. Tokyo opening windows are not positive in this sample.

The 14:45–15:15 JST historical-close diagnostic is materially positive on this sample for both EMA5/EMA200 and the simpler price/EMA200 comparator.

### Interpretation

The close-window observation is a candidate-generating exploratory result only. It was inspected among multiple time cuts after seeing the 2020 outcomes, so it cannot be promoted to a validated time filter from this sample.

The fact that the simpler price/EMA200 comparator is also positive reduces confidence that EMA(5) itself is the essential mechanism.

### Limits

- not XM
- not BID/ASK executable economics
- partial 2020 only
- COVID-era market regime
- historical trading-session structure differs from current JPX hours
- 2020 time-window selection is exploratory and multiple-comparison exposed
- no claim of net profitability

## Next action

Freeze the exact 14:45–15:15 JST candidate before reading 2019 OANDA JP225 outcomes and perform one historical temporal replication under the separate specification `OANDA_2019_REPLICATION_SPEC.md`.
