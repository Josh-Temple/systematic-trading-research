# Independent audit — JP225 US-Lead Opening Reversal v0.1

Date: 2026-10-04

## FACT — repository chronology

Fresh Git history from the branch shows the following order:

1. `e9616d37...` — README
2. `8b9e082d...` — hypothesis
3. `b06466c7...` — scientific prior art
4. `6d5ac244...` — frozen 2015 specification
5. `ecbdb7fd...` — CURRENT scaffold
6. `4bdc226d...` — first 2015 Q1 outcome-bearing receipt
7. Q2/Q3/Q4 receipts
8. `c19472c8...` — 2015 discovery result
9. stop decision / CURRENT / index updates

Therefore the specification commit precedes the first repository outcome-bearing 2015 receipt.

Boundary: Git history cannot independently prove that no human or external process viewed 2015 outcomes outside the repository before the freeze. The repository claim is limited to verifiable commit ordering.

## FACT — prior art

Primary motivating paper:

Yasuhiro Iwanaga (2026), "How the prior day's S&P 500 returns influence the intraday returns of Nikkei 225 futures", Finance Research Open 2(2), 100108.

DOI:
https://doi.org/10.1016/j.finr.2026.100108

Fresh public article text confirms:
- sample January 2001 through December 2024;
- one-minute Nikkei 225 futures from LSEG Tick History;
- 5,716 Japanese trading days;
- previous-day S&P 500 return predicts the first 30-minute Japanese return negatively;
- it predicts the last 30-minute return positively;
- strategy variants exploiting these patterns are reported to generate statistically significant positive excess returns.

This repository does not claim its OANDA CFD proxy reproduces the futures source or the full paper specification.

Historical JPX evidence:

JPX Derivatives Market Highlights, January 1–June 30 2015, Contract Specifications, records Nikkei 225 Futures auction trading hours as:
- 09:00–15:15 JST day session
- 16:30–03:00 night session

Source:
https://www.jpx.co.jp/english/derivatives/market-report/market-highlights/tvdivq0000004khi-att/2015_0101_0630_E.pdf

Therefore 09:00–09:30 JST is historically appropriate for the first 30 minutes of the 2015 day session.

## FACT — independent recomputation from quarterly receipts

Inputs:
- `work/2015/q1_features.json`
- `work/2015/q2_features.json`
- `work/2015/q3_features.json`
- `work/2015/q4_features.json`

Recomputed exactly according to `SPEC-JP225-USLEAD-001-v01.md`:

- U.S. exact regular sessions available: 249
- JP exact 09:00–09:30 windows available: 242
- JP dates excluded because expected prior U.S. session unavailable: 9
- exactly-zero prior U.S. return: 1
- final events: 232

Strategy:
- prior U.S. return > 0 -> SHORT JP window
- prior U.S. return < 0 -> LONG JP window

Independent result:

- mean directional return: **+0.5396726208 bps**
- median: **+2.7499355668 bps**
- win rate: **52.1551724138%**
- mean directional points: **+1.0827586207**
- median points: **+5.05**
- bootstrap 95% interval: **[-3.7925110076, +4.9040784997] bps**
- raw U.S.-return / JP first-30m correlation: **-0.0645296148**
- unconditional long first-30m mean: **+1.1978472222 bps**

Bootstrap was independently recomputed with:
- 10,000 resamples
- seed 2255001
- frozen 32-bit LCG
- linear percentile interpolation

These values match the stored discovery result to the displayed precision.

## RESULT

The stored classification is reproducible:

**USLEAD_PROXY_NOT_SUPPORTED_2015**

Support conditions:
1. n >= 180: PASS
2. mean > 0: PASS
3. bootstrap 95% lower bound > 0: FAIL

The literature-consistent negative raw correlation is present, but weak in this proxy year. The sign strategy's mean is also below the same-year unconditional long 09:00–09:30 mean.

## INTERPRETATION

This is not a contradiction of Iwanaga (2026). The source and empirical object differ materially:

- paper: Nikkei 225 futures + S&P 500 index, LSEG Tick History, 2001–2024;
- repository test: OANDA-derived midpoint JP225 CFD + SPX500 CFD, calendar 2015 only.

The proxy test says that a simple sign-only transfer of the published relationship is not robust enough in this one independent midpoint-CFD year to justify further optimization.

## DECISION

Per the frozen stop rule:

- do not read 2014 outcomes for this v0.1;
- do not add S&P magnitude thresholds;
- do not add volatility, weekday, overnight, EMA, side or stop/target filters;
- do not test the close-window rule as a rescue.

The v0.1 proxy candidate is closed as a negative result.

A future revisit requires a materially better source identity and a new preregistration, preferably exact Nikkei 225 futures or qualified XM JP225Cash BID/ASK data.
