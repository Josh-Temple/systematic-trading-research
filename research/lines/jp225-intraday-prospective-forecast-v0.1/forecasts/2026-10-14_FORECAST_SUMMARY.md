---
type: ProspectiveForecastSummary
event_id: XPF-JP225-20261014
research_line_id: RL-JP225-PROSPECTIVE-001
information_cutoff: 2026-10-14T08:00:00+09:00
issued_at: 2026-10-14T08:00:56.398+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 exploratory forecast — 2026-10-14

**Research target:** 09:00→15:30 JST on a scheduled JPX cash-equity trading day, reference future *qualified exact* XM MT5 `JP225Cash` Bid/Ask midpoint. This event is NOT a formal qualified scored forecast because XM input/output sources remain unavailable.

**Precutoff custody:** pre-registration physically committed **07:52:53 JST** (`c91afbb0f3d07699498d6fd9409a9c6eadff4ff4`; earlier front-matter indicative time `07:52:00` is inaccurate), numerical assessment physically committed **07:54:33 JST** (`5c841d151b150afdbd2670887e74d7b45f62620d`). Frozen assessment: https://github.com/Josh-Temple/systematic-trading-research/blob/5c841d151b150afdbd2670887e74d7b45f62620d/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-14_PRE_CUTOFF_ASSESSMENT.md. No outcome or post-08:00 input changed B0/A1/A2/A3 values.

**JSON record generation/issue preparation timestamp:** `2026-10-14T08:00:56.398+09:00`. The atomic GitHub issue commit timestamp (inspect this commit on GitHub) is the independently auditable actual public issuance time. Those timestamps must not be silently conflated. Source cutoff remains exactly 08:00 JST; all source publications cited in the frozen assessment are at/before the cutoff.

| System | Frozen P(up) | Frozen forecast (bps) |
| --- | ---: | ---: |
| B0 | 0.50 | 0 |
| A1 (public future proxy context) | 0.52 | +3 |
| A2 (market/macro/FX/news) | 0.49 | -2 |
| A3 (A2 + preserved repo status) | **0.50** | **0** |

**Headline A3: neutral / no qualified edge; extremely low directional confidence. NO_TRADE.**

## Data quality and boundary

- Japanese Osaka Dec future overnight close 68,100 at 06:00 JST, +140 versus previous futures settlement; CME future in a distinct time/venue recorded about 68,235 at 05:20 JST. No conflation.
- U.S. Dow -0.35%, Nasdaq -0.15%, S&P -0.02%; USDJPY ~158.33; WTI ~USD94.14. All timestamped pre-cutoff public reports.
- The Japanese overnight futures gap is not the post-opening return. All market quotes are *public, non-XM proxy context*; exact XM JP225Cash Bid/Ask, lookbacks and endpoints were not acquired per the research owner's direction.
- A3 includes repository statuses `UNTESTED / WAITING_FOR_XM_STAGE1_DATA` and `STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015` with no promotion of negative/untested research into validated skill.
- Scientific status `UNTESTED`; SPEC `PROPOSED_NOT_FROZEN`; cohort `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`, formal scored cohort `CLOSED`, trading prohibited. Probabilities are subjective and uncalibrated.
- A1 is **NOT** exact-XM-compliant target-only estimator. Predictions are not a profit claim and cannot be used to authorize trade.
- No use of Oct 6/8/9/13 exploratory outcome feedback to refit the probabilities, select features, or change parameters.
- No 09:00 opening, after-open market data, 15:30 outcome or after-08:00 news was used in the numerical forecast.
- Official after-close review, if no exact XM quote, must preserve `MARKET_OUTCOME_UNAVAILABLE`, null prices/direction and empty formal `scores={}`. Public Nikkei cash-index diagnostics may appear in a separate `PUBLIC_PROXY_REVIEW.md` only.

## Forecast JSON canonical SHA-256 (excluding canonical_sha256 field)

- `2026-10-14_A1_forecast.json`: `6be8cb3c7976ba014bad85d5b2cb8cae76e4de401cfe10922acbbe97a92ba5f7`
- `2026-10-14_A2_forecast.json`: `14cc307a39414f98a8f1a806047fc21d0afe350c4f60c432fc626eeebe33fb60`
- `2026-10-14_A3_forecast.json`: `36220f03c3402d408fe3f212bfb0ba0f8cc9302a50c12b2d2333f79ce3582c39`

Preserve immutable issued records and historical 2026-10-06 legacy SHA mismatch notices; synthetic CI PASS is not scientific performance evidence.
