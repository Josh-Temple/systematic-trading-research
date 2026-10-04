---
id: RESULT-JP225-USLEAD-2015
type: HistoricalProxyDiscoveryResult
hypothesis_id: HYP-JP225-USLEAD-001
created_at: 2026-10-04
status: COMPLETE
classification: USLEAD_PROXY_NOT_SUPPORTED_2015
xm_execution_evidence: false
---

# JP225 US-Lead Opening Reversal — 2015 proxy discovery result

## Pre-outcome freeze

Specification:
`specifications/SPEC-JP225-USLEAD-001-v01.md`

The specification was committed before 2015 price-content access.

No 2014 price outcome was accessed.

## Source

Public `FutureSharks/financial-data` OANDA-derived midpoint M1:

- `SPX500_USD`
- `JP225_USD`

Source identities were recorded in quarterly feature receipts under `work/2015/`.

Usable exact-window source observations:
- U.S. regular sessions: 249
- JP 09:00–09:30 windows: 242

## Mapping

For each Japanese date:

- expected prior U.S. date = preceding calendar day, rolling weekend dates back to Friday;
- if that exact U.S. session is unavailable, exclude the Japanese date;
- no older U.S. return is carried forward through a U.S. holiday.

Excluded:
- missing expected U.S. session: 9 Japanese dates
- exactly zero U.S. regular-session return: 1 date

Final events: **232**.

## Strategy rule

- prior U.S. regular session positive -> SHORT JP225 09:00–09:30 JST
- prior U.S. regular session negative -> LONG JP225 09:00–09:30 JST

U.S. session:
- exact 09:30 America/New_York OPEN
- exact 15:59 America/New_York CLOSE

JP window:
- exact 09:00 JST OPEN
- exact 09:30 JST OPEN

No threshold or additional filter.

## Result

Primary directional return:

- n: **232**
- mean: **+0.539673 bps**
- median: **+2.749936 bps**
- win rate: **52.16%**
- bootstrap 95% interval: **[-3.792511, +4.904078]**

Directional points:

- mean: **+1.082759 points**
- median: **+5.05 points**

Descriptive diagnostics:

- raw prior-U.S.-return vs JP first-30m raw-return correlation: **-0.064530**
- unconditional LONG JP 09:00–09:30 mean: **+1.197847 bps**

## Frozen decision rule

Support required all:

1. n >= 180
2. mean directional bps > 0
3. bootstrap 95% lower bound > 0

Conditions 1 and 2 pass.

Condition 3 fails.

**Classification: USLEAD_PROXY_NOT_SUPPORTED_2015.**

## Interpretation

### FACT

The sign-based rule has a small positive gross mean but substantial uncertainty and does not clear the pre-registered support threshold.

The raw cross-market correlation has the literature-consistent negative sign, but is small in this proxy year.

The rule's mean is also below the same-year unconditional long first-30-minute mean.

### INTERPRETATION

This public OANDA midpoint CFD proxy does not reproduce a robust economically useful version of the published opening-reversal signal in 2015.

This does **not** refute Iwanaga (2026), whose study uses:
- Nikkei 225 futures rather than this CFD proxy;
- S&P 500 index rather than OANDA SPX500 CFD midpoint;
- LSEG Tick History;
- a long 2001–2024 sample;
- a fuller empirical specification.

It also does not establish anything about current XM JP225Cash net execution.

## Stop decision

Per specification:

- do not access 2014 for this v0.1 candidate;
- do not add U.S. return magnitude thresholds;
- do not add overnight-sign matching;
- do not split by weekday;
- do not add volatility/VIX/EMA filters;
- do not test the close window as a rescue;
- do not tune transaction-cost assumptions.

This v0.1 proxy candidate stops with a negative discovery classification.
