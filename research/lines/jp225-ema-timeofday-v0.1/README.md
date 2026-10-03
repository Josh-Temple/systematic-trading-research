---
id: RL-JP225-EMA-001
type: ResearchLineIndex
created_at: 2026-10-03
status: PRE_OUTCOME_ARCHITECTURE
---

# JP225 M1 EMA5/EMA200 Time-of-Day v0.1

This research line tests a simple user-proposed short-horizon idea on XM `JP225Cash`: M1 EMA(5) crossing EMA(200), same-direction short-horizon continuation, and possible concentration in predeclared market-relevant time windows.

## Current state

No JP225 market outcome has been calculated in this line. The scientific contract is drafted before data access. The next admissible work is source qualification and outcome-blind implementation.

## Canonical entrypoints

- [RESEARCH_LINE.md](RESEARCH_LINE.md)
- [CURRENT.md](CURRENT.md)
- [hypotheses/HYP-JP225-EMA-001.md](hypotheses/HYP-JP225-EMA-001.md)
- [specifications/SPEC-JP225-EMA-001-v01.md](specifications/SPEC-JP225-EMA-001-v01.md)
- [decisions/DEC-JP225-EMA-001.md](decisions/DEC-JP225-EMA-001.md)
- [references/SCIENTIFIC_PRIOR_ART_2026-10-03.md](references/SCIENTIFIC_PRIOR_ART_2026-10-03.md)
- [work/README.md](work/README.md)

## Important source boundary

The intended execution-specific source is XM MT5 `JP225Cash` history, with M1 signal bars and BID/ASK ticks if available.

Dukascopy `JPN.IDX/JPY` is not silently substituted: Dukascopy currently describes it as a "Japan 200+ Index", not as the exact Nikkei 225 / XM JP225Cash instrument.

## Prohibited before discovery is recorded

Do not tune EMA spans, stop/target, confirmation bars, EMA200 slope, volatility filters, weekdays, ad-hoc clock windows, news filters, or long/short asymmetry.
