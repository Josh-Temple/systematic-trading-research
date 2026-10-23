---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261014
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-14T20:56:17+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 2026-10-14 after-close public Nikkei 225 cash-index PROXY diagnostic

## 1. Instrument and forecast custody

**This document is not an XM `JP225Cash` outcome or official research Brier score.** The designated formal target is exact XM MT5 `JP225Cash` qualified Bid/Ask midpoint, 09:00→15:30 JST; qualified XM data were not retrieved, per owner's instruction.

The formal `2026-10-14_review.json` separately preserves `MARKET_OUTCOME_UNAVAILABLE`, `start_quote=null`, `end_quote=null`, `realized_return_bps=null`, `y_up=null`, `scores={}`. Public Nikkei cash-index calculations here **cannot** be substituted or admitted into the formal scored 60-event cohort.

Pre-registration committed Oct 14 at **07:52:53 JST** (`c91afbb0f3d07699498d6fd9409a9c6eadff4ff4`), after its nominal `registered_at=07:52:00` in text. Numeric A1/A2/A3 predictions were immutable before the information cutoff, committed at **07:54:33 JST** (`5c841d151b150afdbd2670887e74d7b45f62620d`). A1/A2/A3 formal exploratory JSONs were committed simultaneously at **08:01:02 JST** (`f4e81827cee0b462bfb7fa386e46ca59149dfebc`), before the 09:00 session began; JSON internal `issued_at=08:00:56.398 JST` is distinct from actual GitHub commit/publication time.

All after-close prices were reviewed after 15:30; no issued forecast was changed or re-inferred from market outcomes.

## 2. Official published Nikkei 225 cash-index OHLC (post-close only)

Official Nikkei source: https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261014&idx=nk225 ; https://indexes.nikkei.co.jp/nkave/archives/data?list=daily (updated 2026.10.14).

| Item | Cash-index observation |
| --- | ---: |
| Date | Wednesday 2026-10-14 |
| 09:00 opening | **67,942.23** |
| Session high | **68,408.14** at 13:31 JST |
| Session low | **67,533.10** at 15:05 JST |
| 15:30 closing | **67,744.29** |
| Close minus 09:00 open | **-197.94 points** |
| Close minus Oct 13 close 67,777.52 | **-33.23 points**, around -0.05% |

**The research target is today's 09:00→15:30 interval, NOT previous close→today close.** The public cash-index proxy log return for this specified intraday interval is

`10000 * ln(67744.29 / 67942.23) = -29.176095077501916 bps`, rounded **-29.18 bps** (about -0.2913% simple intraday return). Public cash-index proxy `y_up=0` (DOWN).

## 3. Frozen forecasts vs this NONFORMAL public-index proxy

The forecasts below were **frozen prior to 08:00 JST** and were not adjusted after outcome observation.

| Model | Frozen P(up) | Frozen return (bps) | Proxy Brier if y=0 | Absolute proxy return error (bps) | Direction comparison |
| --- | ---: | ---: | ---: | ---: | --- |
| B0 neutral | 0.50 | 0 | 0.2500 | 29.18 | Neutral; no directional prediction |
| A1 public futures proxy | 0.52 | +3 | 0.2704 | 32.18 | Opposite: slightly UP vs DOWN |
| A2 market / FX / news | 0.49 | -2 | 0.2401 | 27.18 | Same: slightly DOWN vs DOWN |
| A3 repository status layer | 0.50 | 0 | 0.2500 | 29.18 | Neutral; no directional prediction |

Nonformal methods: `proxy_brier = (p_up - 0)^2`; `proxy_absolute_return_error_bps = |forecast_bps - (-29.176095077501916)|`. No calibration, trading P&L, exact-XM Brier/MAE, win-rate declaration or cohort promotion is authorized.

## 4. Results, interpretations, and decisions (distinct)

**Result:** Today's published Nikkei cash index fell **-197.94 points from its 09:00 opening**, despite the small prior-close-to-close change of -33.23 points. A1's slightly positive return forecast was opposite in sign to the public proxy. A2's slightly negative forecast matched direction, but substantially **underpredicted the magnitude**. A3/B0 were neutral and neither had a sign call. On this *single public proxy observation*, A2 has the smallest Brier and absolute error while A1 has the largest.

**Tentative interpretation:** Positive prior-night Osaka futures by 06:00 JST were not sufficient to guarantee cash-index appreciation **after** the 09:00 open. Mildly adverse U.S. conditions in A2 were consistent in sign with the subsequent down day, but nothing in this single outcome identifies which input (if any) possessed independent predictive information. This is post-outcome commentary only, not an authorization to tilt A2 downwards tomorrow or overweight futures/FX.

**Decision:** No rule, coefficients, timestamp, input route, feature selection, threshold, PR merge or trading changes. `UNTESTED`, `PROPOSED_NOT_FROZEN`, `SCORED_COHORT_CLOSED`, `NO_TRADE`. Preserve an unfavorable proxy error honestly and continue exploratory evidence capture; no source substitutions or backfills.

## 5. Provenance and independent comparison

1. Nikkei, **official daily October 14 cash index summary:** https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261014&idx=nk225
2. Nikkei, **official daily OHLC table** with 2026.10.14 row: https://indexes.nikkei.co.jp/nkave/archives/data?list=daily
3. Trader's Web, 2026-10-14 15:45 update, independent matching OHLC: https://www.traders.co.jp/index/0101
4. Frozen pre-cutoff candidate source (fixed commit): https://github.com/Josh-Temple/systematic-trading-research/blob/5c841d151b150afdbd2670887e74d7b45f62620d/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-14_PRE_CUTOFF_ASSESSMENT.md
5. Issued forecasts, A1/A2/A3, single commit: https://github.com/Josh-Temple/systematic-trading-research/commit/f4e81827cee0b462bfb7fa386e46ca59149dfebc

These public sources were consulted **only during post-close review**, not to fit or revise the frozen forecast.
