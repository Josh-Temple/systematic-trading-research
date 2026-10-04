# Scientific and market-structure prior art — 2026-10-03

Status: PRE_OUTCOME REFERENCE REVIEW

No JP225 EMA crossover outcome was calculated for this review.

## Nikkei 225 intraday structure

Yasuhiro Iwanaga (2026), "How the prior day's S&P 500 returns influence the intraday returns of Nikkei 225 futures", *Finance Research Open*, 2(2), 100108.

- DOI: https://doi.org/10.1016/j.finr.2026.100108
- article: https://www.sciencedirect.com/science/article/pii/S3050700626000204
- sample: January 2001–December 2024
- data: one-minute Nikkei 225 futures from LSEG Tick History
- reported structure: previous U.S. return is associated with reversal in the first 30 minutes and momentum in the final 30 minutes
- reported cost result: under the paper's spread/commission assumptions, the opening-reversal timing strategy remains positive/statistically significant while closing momentum does not

Relevance: intraday behavior can differ by clock interval and apparent gross effects can disappear after costs. This is not evidence for EMA5/EMA200 and does not use XM JP225Cash.

## JPX session structure

Japan Exchange Group:

- https://www.jpx.co.jp/derivatives/products/domestic/225futures/01.html
- https://www.jpx.co.jp/derivatives/rules/trading-hours/

Current published Nikkei 225 futures day session opens 08:45 JST, regular session runs to 15:40, closing auction is 15:45. Night session opens 17:00 and closes 06:00.

This supports fixing opening/closing windows from market structure before EMA outcomes are inspected.

## XM product evidence

Broker-facing material:

- https://fxplus.xmtrading.com/media/2026041501.html
- https://fxplus.xmtrading.com/market-rate/JP225Cash/

It identifies `JP225Cash`, MT5 availability, variable spread, and broad near-24-hour trading/quoting. Exact spread must be measured from the broker feed used for the test.

The actual XM MT5 instrument/server history and metadata control source qualification.

## Dukascopy mismatch

Dukascopy official page:

https://www.dukascopy.com/swiss/english/cfd/range-of-markets/cfd-indices/

It currently identifies `JPN.IDX/JPY` as "Japan 200+ Index" / "Over 200 leading Japanese firms". Identity with Nikkei 225, XM JP225Cash, or OSE Nikkei 225 futures is not established, so it is not a silent replacement source.

## EMA-specific evidence

A bounded search did not identify strong primary academic evidence that the exact M1 EMA(5)/EMA(200) crossover on Nikkei 225 / JP225Cash has a stable net edge.

That is not evidence of failure. The EMA rule enters this line as a user-specified empirical hypothesis.

## Design implication

Prior evidence supports predeclared time windows, cost-aware execution, exact source identity, a simple comparator, and an unused holdout. It does not support optimizing EMA parameters, stops, targets, or clock windows on the same sample.
