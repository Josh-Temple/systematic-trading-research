---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261008
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-08T17:57:23+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 2026-10-08 public-cash-index proxy review

## 0. Instrument / source boundary

This **post-15:30** comparison uses the published **Nikkei 225 cash index**, not XM MT5 `JP225Cash` Bid/Ask midpoints. The user expressly deferred collecting actual XM prices; no XM retrieval was attempted. The formal, separately recorded `2026-10-08_review.json` therefore remains `MARKET_OUTCOME_UNAVAILABLE` with all formal outcome fields null and **no formal Brier/MAE**.

The event is a late-issued exploratory dry run. Its forecast values were originally saved in a preliminary assessment at **07:55:35 JST** (before the 08:00 cutoff) and copied without re-inference to formal JSONs at **08:21:45 JST** (after the intended issuance). This public outcome was checked **only after the session** and did not inform or alter those forecasts.

## 1. Publicly observed result (facts)

2026-10-08 Nikkei 225 cash index (JPY points):

| Measure | Value | Evidence |
| --- | ---: | --- |
| 09:00 opening index | 69,840.64 | Kabutan close report, 16:36 JST |
| Daily high | 69,918.20 | Kabutan close report, 16:36 JST |
| Daily low | 69,042.11 | Kabutan close report, 16:36 JST |
| 15:30 closing index | 69,042.11 | Kabutan/Fisco; separately confirmed by Nikkei official monthly historical page updated 2026-10-08 |
| Prior-close to close | -993.60 points / -1.42% | Kabutan / Fisco; **not** the 09:00-to-15:30 target |

The 09:00-to-close **cash-index proxy**, calculated as `10,000 × ln(69042.11 / 69840.64)`, is **-114.99467 bps** (approximately **-114.99 bps**); binary direction proxy `y_up = 0`. Cash-index open-to-close change is -798.53 index points. This is a **derived proxy quantity**, not a supplied/observed XM return.

The closing level is independently corroborated; a dynamically updated day-by-day official OHLC page was not used to assert the 09:00 opening quote. All facts here were researched after the end of the session.

## 2. Issued forecasts versus public proxy — nonformal diagnostics only

The issued forecast was not revised.

| System | Pre-cutoff P(up) | Forecast return | Proxy single-event Brier | Proxy absolute-return error |
| --- | ---: | ---: | ---: | ---: |
| B0 | 0.50 | 0 bps | 0.2500 | 114.99 bps |
| A1 (proxy-only) | 0.46 | -6 bps | 0.2116 | 108.99 bps |
| A2 (exploratory) | 0.42 | -12 bps | 0.1764 | 102.99 bps |
| A3 (exploratory) | 0.44 | -8 bps | 0.1936 | 106.99 bps |

Calculation: `(p_up - 0)^2` for proxy Brier; `abs(forecast_return_bps - (-114.99467))` for single-event proxy absolute error. These are **not formal scored observations** and are not the 60-event matched benchmark.

## 3. Result distinct from interpretation

**Result:** All three frozen challengers assigned below-0.50 upward probability, matching the public cash-index **down** direction. Their predicted negative return magnitudes were much smaller than the cash-index intraday move. On this single *proxy* observation, A2 has the lowest reported proxy Brier and absolute-return error among A1/A2/A3.

**Interpretation (tentative):** The pre-cutoff bearish assessment was directionally consistent with the publicly reported intraday cash-index decline. The single-event magnitude disagreement is substantial. The post-close news article provides additional narrative but is **not** evidence available at the forecast cutoff and was not used to explain away, improve, or retrofit the original forecast. One proxy observation cannot establish an edge, calibration, A2>A3 superiority, or tradability.

**Attribution limits:** Qualified XM 09:00/15:30 Bid/Ask source missing by design (not fetched); original forecast issuance was late; market-context source for A1 was proxy-only. Formal probability and return forecast error remain unassessable.

## 4. Scientific / implementation decision

- Formal outcome stays `MARKET_OUTCOME_UNAVAILABLE`; `start_quote`, `end_quote`, `realized_return_bps`, `y_up` remain null and `scores = {}`.
- No forecast file overwrite; no pre-08:00 source reconstruction from later prices or news.
- **No specification, input, weight, threshold, or baseline changes.**
- No admission to the eventual 60-event scored cohort; scientific status `UNTESTED`.
- Source readiness `PARTIAL`; live/paper trading `NO_TRADE`.

## 5. Evidence references (post-session; source-of-truth boundaries)

1. [Kabutan daily close report, 2026-10-08 16:36 JST](https://fu.minkabu.jp/news/719894): 09:00 open 69,840.64; high 69,918.20; low and close 69,042.11; previous-close change -993.60 (-1.42%).
2. [Nikkei official historical **monthly** series, updated 2026-10-08](https://indexes.nikkei.co.jp/nkave/archives/data?list=monthly): October 2026 last close 69,042.11; **does not independently verify 09:00 open**.
3. [Fisco close bulletin, published 2026-10-08 15:31 JST](https://minkabu.jp/news/4632030): previous-close change -993.60 and closing index 69,042.11.
4. Frozen forecast summary: `forecasts/2026-10-08_FORECAST_SUMMARY.md`; original timestamped assessment: `forecasts/2026-10-08_PRE_CUTOFF_ASSESSMENT.md`.

Observations and numerical diagnostics here are append-only *post-event* research records. This file is not a substitute for a formal XM review.
