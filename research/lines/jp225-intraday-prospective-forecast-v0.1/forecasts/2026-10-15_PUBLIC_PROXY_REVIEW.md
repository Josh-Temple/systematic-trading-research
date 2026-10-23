---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261015
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-15T23:01:04+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# 2026-10-15 — Public Nikkei 225 cash-index diagnostic (NOT exact XM)

## 1. Instrument and temporal integrity

This is a **post-close, public-index proxy** comparison, not formal XM MT5 `JP225Cash` Bid/Ask-midpoint evidence. Its prices, return and numerical error statistics **MUST NOT** be entered into the formal `2026-10-15_review.json`, retroactively promoted to the 60-event scored cohort, or described as XM performance. The formal review separately records `MARKET_OUTCOME_UNAVAILABLE`, all quote/return/outcome fields `null`, and `scores={}` because qualified XM prices were not acquired by owner direction.

The October 15 invocation occurred **after the 08:00 JST information cutoff**. In particular, there was **no pre-08:00 pre-registration and no pre-08:00 numerical snapshot**. Reports with dated publications before 08:00 were retrieved after that cutoff, with no independent raw byte snapshot of their 08:00 state. The original A1/A2/A3 exploratory JSONs were published in GitHub commit `0ba67e8ea223bf6bcc7906d03e7a06a916e2cb66` at **08:12:27 JST**, before the 09:00 session opening, but **late relative to the cutoff**; their internal `issued_at` is **08:12:21.546 JST**. Both actual commit and timestamp declarations are preserved and neither pretends there was an on-time 08:00 forecast.

Original probabilities and return forecasts remain unchanged and are permanently **late-issued exploratory, not in the formal prospective cohort**.

## 2. Public post-close primary-source facts — 2026-10-15

Official Nikkei 225 cash-index daily figures, published after 15:30 on October 15:

| Measure | Value |
| --- | ---: |
| Cash 09:00 opening | **66,880.37** |
| Cash session high | **66,929.30**, at 09:00 |
| Cash session low | **64,092.74**, at 12:51 |
| Cash 15:30 close | **64,425.95** |
| Cash close minus 09:00 open | **-2,454.42 points** |
| Cash close minus October 14 close 67,744.29 | **-3,318.34 points**, -4.90% |

**The specified target is the 09:00→15:30 change, NOT the previous-day-close to today's close change.** The negative 4.90% figure above is versus the previous day's close; it is **not** the forecasted intraday move.

Public cash-index proxy intraday simple return: `100 * (64425.95/66880.37 - 1) = -3.6698660608%`.

Public cash-index proxy intraday **log return**:
`10000 * ln(64425.95/66880.37) = -373.8899879960 bps`, rounded **-373.89 bps**. Public-index-only `proxy_y_up = 0` (down).

**Primary public source**:
- Nikkei official daily summary for 2026-10-15: https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261015&idx=nk225
- Nikkei official daily OHLC historical series (updated 2026-10-15): https://indexes.nikkei.co.jp/nkave/archives/data/
- Nikkei official index list identifies Oct 15 values as closing prices: https://indexes.nikkei.co.jp/nkave/index?type=index

## 3. Frozen forecast vs NONFORMAL public-index proxy

Pre-09:00 **late-issued** subjective predictions (never altered after observing the outcome):

| System | Frozen P(up) | Forecast log return | Proxy Brier (y=0) | Absolute proxy log-return error |
| --- | ---: | ---: | ---: | ---: |
| B0 neutral | 0.50 | 0 bps | 0.2500 | 373.89 bps |
| A1 public futures proxy | 0.49 | -3 bps | 0.2401 | 370.89 bps |
| A2 cross-market/macro/news | 0.45 | -12 bps | 0.2025 | 361.89 bps |
| A3 repo status | 0.47 | -7 bps | 0.2209 | 366.89 bps |

Calculation definitions: `proxy_brier=(p_up - 0)^2`, `proxy_abs_return_error_bps=abs(forecast_bps - (-373.8899879960))`.

**These are descriptive NONFORMAL scores only**. They are neither calibrated-model probabilities nor valid XM research performance, and must not be pooled into the 60-event matched sample. A trading win rate, P&L or trade execution cannot be inferred from them.

## 4. Results, interpretation, decision

### Result

- A1, A2, and A3 all had `P(up)<0.50` and negative forecast returns when published at 08:12:27, before the cash market open; the published public cash index subsequently declined between 09:00 and 15:30. **Their directional lean aligned with this public-index proxy only.**
- Magnitudes were greatly underestimated: A1 -3 bps, A2 -12 bps, A3 -7 bps versus realized proxy -373.89 bps.
- A2 has the smallest single-event public-index proxy Brier and absolute error, but **one large-move session cannot establish relative model merit**. The subjective probabilities are close to neutral, and Brier differences are mechanically small.
- The original issue process violated the 08:00 pre-registration and pre-cutoff freeze requirements. Therefore **do not treat this event as an on-time prospective observation**, even though the formal JSON commit preceded 09:00.

### Interpretation (post-outcome, tentative)

The previously reported 06:00 OSE night futures loss (-1,680 versus futures settlement), US equity sell-off and strong US CPI were adverse opening context. The cash index continued to fall significantly **after** its 09:00 opening. This is consistent with the mild bearish direction, but it does **not** identify a reproducible relationship, prove that the U.S. macro reports predict the daily cash return, or justify changing A1/A2/A3 models. The event is source-incomplete and late-issued, so timing and data qualification gaps matter independently of outcome direction.

### Decision

- Forecast JSONs, predicted probabilities, return forecasts and hashes: **PRESERVED / IMMUTABLE**.
- Formal exact-XM outcome `MARKET_OUTCOME_UNAVAILABLE`; exact XM Bid/Ask not acquired; `scores={}` in formal review.
- Research status `UNTESTED`; specification `PROPOSED_NOT_FROZEN`; 60-event cohort `CLOSED`; event permanently `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`.
- **NO_TRADE**; no live/paper broker action, no success claims, no parameter/feature/input changes or retrospective source selection.
- Existing Oct 6 legacy hash mismatch is separate and remains unresolved.

## 5. Evidence provenance

1. Official Nikkei Oct 15 daily summary: https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261015&idx=nk225
2. Official Nikkei historical 2026-10-15 OHLC: https://indexes.nikkei.co.jp/nkave/archives/data/
3. Immutable original Oct 15 late-issued forecast/assessment commit: https://github.com/Josh-Temple/systematic-trading-research/commit/0ba67e8ea223bf6bcc7906d03e7a06a916e2cb66
4. Separate exact-XM unavailable formal review: `2026-10-15_review.json`

This public market outcome information was accessed **after 15:30 JST** during the review and never used to determine or revise the forecasts.
