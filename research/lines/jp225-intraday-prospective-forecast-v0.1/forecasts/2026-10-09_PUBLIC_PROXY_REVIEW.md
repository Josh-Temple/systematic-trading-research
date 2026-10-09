---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261009
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-09T21:58:18+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# 2026-10-09 — Nikkei 225 public cash-index proxy review (NOT XM)

## 1. Scope and source boundary

This is **post-close** diagnostic research on the public Nikkei 225 cash index, **not** the fixed exact-XM MT5 `JP225Cash` 09:00/15:30 Bid/Ask-midpoint formal outcome.

The owner chose not to retrieve XM prices. The separate `2026-10-09_review.json` records `MARKET_OUTCOME_UNAVAILABLE`, `start_quote=null`, `end_quote=null`, `realized_return_bps=null`, `y_up=null`, `scores={}`. Public prices and proxy scores **must not** be substituted into that file, the 60-event scored cohort, or any XM claim.

**Timing:** the event was pre-registered before 08:00 JST; the numerical assessment was immutable in GitHub at 07:51:35 JST, but formal A1/A2/A3 forecast JSONs were issued at **12:37:25 JST, after the 09:00 target start**. The numerical values did not change. This is an expressly **late-issued exploratory** event, not an on-time issued prospective forecast.

## 2. Verified public-index facts (research after 15:30 JST)

Official Nikkei 225, **2026-10-09** (points):

| Field | Official value |
| --- | ---: |
| Open at 09:00 JST | **68,648.50** |
| High at 15:20 JST | **69,143.45** |
| Low at 09:20 JST | **68,150.02** |
| Close at 15:30 JST | **69,030.92** |
| Change against previous day's close | **-11.19** (about -0.02%) |

**Important target distinction:** the negative -11.19 point number is *close vs prior day's close*. This research target is **today's 09:00 open to 15:30 close**, which rose by **+382.42 points**.

The separate public-cash-index proxy log return is:

`10,000 × ln(69030.92 / 68648.50) = +55.55238 bps`, approximately **+55.55 bps**; cash-index proxy `y_up = 1`.

This proxy outcome was consulted *after the close only*, not as a forecast input or forecast revision.

## 3. Strictly nonformal single-event calculations

Fixed A1/A2/A3 probabilities and return forecasts come **unchanged** from the GitHub pre-cutoff assessment and later late-issued JSONs.

| Model | Frozen P(up) | Forecast return (bps) | Proxy Brier (y=1) | Proxy absolute return error (bps) |
| --- | ---: | ---: | ---: | ---: |
| B0 neutral | 0.50 | 0 | 0.2500 | 55.55 |
| A1 (futures-only proxy) | 0.48 | -4 | 0.2704 | 59.55 |
| A2 (cross-market) | 0.44 | -10 | 0.3136 | 65.55 |
| A3 (repo status layer) | 0.46 | -7 | 0.2916 | 62.55 |

Definitions: `proxy_brier = (p_up - 1)^2`; `proxy_abs_error = abs(predicted_return_bps - 55.5523815364)`. These are **not formal XM Brier scores or formal XM return errors**, and cannot be pooled into the 60-event cohort.

## 4. Result vs interpretation vs decision

### Result

- In the public cash-index proxy, the **open-to-close direction was UP**, opposite to A1/A2/A3's below-0.50 upward probabilities and negative return forecasts.
- Each challenger underpredicted the proxy daily intraday movement and had **higher single-event proxy Brier and absolute-return error than neutral B0**.
- This does not establish that B0 is generally superior: it is **one late-issued, source-incomplete, exploratory proxy event**.

### Interpretation (tentative; NOT pre-cutoff input)

The pre-cutoff overnight Nikkei futures decline and U.S. technology weakness corresponded more clearly to a weaker **opening level** than to uninterrupted **09:00–15:30** decline. By 15:30 the public cash index had risen from the 09:00 open, despite being slightly down against the previous day's close.

A large overnight loss therefore cannot safely be equated with the signed daytime return. This is a methodological explanation of the target mismatch, **not** a post-hoc instruction to trade mean reversion, shift p(up), or alter the frozen hypothesis.

### Decision

- **No changes** to forecast files, timing, features, weights, thresholds, specification, or validation protocol.
- No calibration or demonstrated forecast skill; scientific status remains `UNTESTED`.
- Event remains permanently `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT` (formally `CLOSED`).
- Exact XM remains uncollected by owner choice; formal result remains `MARKET_OUTCOME_UNAVAILABLE`.
- **NO_TRADE**; no live/paper broker instruction.

## 5. Evidence and provenance

1. **Official primary source**, Nikkei 225 daily summary for Oct 9: https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261009&idx=nk225 — date, open, high and low times, and close/previous-close change.
2. **Official primary source**, historical daily OHLC table, updated 2026-10-09: https://indexes.nikkei.co.jp/nkave/archives/data/ — 2026-10-09 OHLC row.
3. Independent post-close confirmation, Kabutan report distributed 16:38 JST: https://minkabu.jp/stock/2914/news/4633216 — cash open/high/low/close and close-versus-previous-close.
4. Immutable pre-08:00 candidate assessment: https://github.com/Josh-Temple/systematic-trading-research/blob/f1713e620c8c558cbc4726d0f6e8f899bd3f690e/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-09_PRE_CUTOFF_ASSESSMENT.md
5. Formal late-issuance record: `2026-10-09_FORECAST_SUMMARY.md` and A1/A2/A3 JSON, with actual 12:37:25 JST issuance.

All observed post-close price facts are contained only in this *post-event proxy file*, not in the forecast itself.
