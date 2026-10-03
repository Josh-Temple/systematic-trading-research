---
type: CurrentProjection
research_line_id: RL-JP225-EMA-001
projection_generated_at: 2026-10-04
derived_from_decisions:
  - DEC-JP225-EMA-001
  - DEC-JP225-PROXY-20261004
derived_from_interpretations:
  - RESULT-JP225-PROXY-OANDA-2019-REPLICATION
  - RESULT-JP225-PROXY-EMA200-SLOPE-2018
---

# Current State

## Main scientific status

- Exact XM hypothesis HYP-JP225-EMA-001: **UNTESTED**
- XM market outcomes accessed: **NO**
- Packet A exact XM source: **PARTIAL_WITH_GAPS**
- Packet B deterministic implementation: **COMPLETE**
- Packet C XM discovery: **LOCKED**
- 2026 XM holdout: **UNTOUCHED / LOCKED**

## Frozen XM core

- symbol: XM MT5 `JP225Cash`
- M1 EMA(5)/EMA(200) crossover
- primary horizon: +15 minutes
- quote-executable BID/ASK economics required
- 2025 discovery
- 2026-01-01 through 2026-09-30 holdout only after a valid discovery advancement

## Proxy exploratory evidence

Because exact XM data was unavailable in Chat, public OANDA-derived **midpoint** JP225 M1 data was used under separate exploratory labels.

### 2020 partial-year

Broad all-time continuation was small and not statistically separated from zero. Tokyo-open continuation was negative. A historical-close window looked positive post hoc.

### 2019 independent historical replication

The historical-close candidate failed its pre-frozen replication:

- mean +0.9303 points
- day-cluster 95% interval [-2.9103, +5.0836]
- HISTORICAL_PROXY_NOT_REPLICATED

### 2018 nearby slope-filter test

A one-bar EMA200 slope-alignment rule produced exactly the same events as the unfiltered crossover. Algebra shows this filter is structurally redundant.

The underlying 2018 broad crossover result was:

- mean +0.2374 gross points
- day-cluster 95% interval [-0.3830, +0.8841]

No robust gross continuation edge was established.

## Current interpretation

The available proxy evidence is adverse to the simple claim that M1 EMA5/EMA200 crossover has a broad, stable short-horizon continuation edge that only needs a low spread to become profitable.

It does not establish the result for current XM JP225Cash.

## Next action

Highest priority: obtain exact XM MT5 JP225Cash M1 and BID/ASK tick history using the existing outcome-blind collector, qualify timestamp/instrument semantics, then run the frozen XM 2025 discovery.

Do not continue searching EMA lengths, hours, weekdays, slope lookbacks, or exits on the consumed OANDA proxy data.
