# JP225 EMA proxy exploration summary — 2026-10-04

## Scope

This summary covers only public OANDA-derived midpoint JP225 M1 proxy work performed because exact XM MT5 history was unavailable in the Chat environment.

It is not XM execution evidence.

## What was learned

### 2020 partial-year exploration

Broad EMA5/EMA200 +15m gross continuation:
- mean +1.1533 points
- day-cluster 95% interval [-0.5503, +2.9981]

Tokyo opening window 08:45–09:15:
- mean -4.2887
- 95% interval [-18.2067, +10.9364]

A historical-close 14:45–15:15 window looked strongly positive, but this was a post-hoc exploratory observation.

### 2019 frozen replication of the close-window observation

- valid events 99 across 65 dates
- mean +0.9303 points
- 95% interval [-2.9103, +5.0836]
- classification: HISTORICAL_PROXY_NOT_REPLICATED

The simpler price/EMA200 comparator in the same window was also near zero/negative.

### 2018 pre-frozen one-bar EMA200 slope filter

- valid events 4,958 across 305 dates
- mean +0.2374 points
- 95% interval [-0.3830, +0.8841]
- classification: SLOPE_FILTER_PROXY_NOT_SUPPORTED_2018

The filtered event set was exactly equal to the unfiltered event set because a one-bar slow-EMA slope aligned with a fast/slow EMA crossover is mathematically implied by the crossover.

## Current proxy interpretation

The evidence does **not** support:

- a broad 24-hour EMA5/EMA200 continuation edge;
- Tokyo-open EMA crossover continuation;
- the 2020 historical-close window as a stable rule;
- adding a one-bar EMA200 slope filter.

The proxy results do not prove that XM JP225Cash lacks an edge. The relevant differences include exact instrument construction, current market regime, current trading hours, and especially broker BID/ASK costs.

## Research decision

Stop parameter expansion on this proxy family.

The highest-value next empirical step is to acquire exact XM MT5 JP225Cash M1 + BID/ASK tick history and execute the already-frozen broker-specific screen.

If exact XM history cannot be acquired, the next strategy idea should be a genuinely new preregistered mechanism, not another EMA length/time-window rescue on these consumed proxy samples.
