---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261013
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-13T19:42:01+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# 2026-10-13 — Public Nikkei 225 cash-index diagnostic review (NOT exact XM)

## 0. Instrument, timing and scope

This after-close diagnostic uses **official published Nikkei 225 cash-index OHLC**, not the fixed formal XM MT5 `JP225Cash` qualified Bid/Ask midpoints. The research owner instructed not to acquire actual XM prices. The separate formal `2026-10-13_review.json` therefore records `MARKET_OUTCOME_UNAVAILABLE` with `start_quote=null`, `end_quote=null`, `realized_return_bps=null`, `y_up=null`, and `scores={}`.

The exploratory forecast was pre-registered at **07:55:04 JST**; the quantitative candidate numbers and pre-cutoff sources were committed to GitHub at **07:56:35 JST**; the A1/A2/A3 immutable JSONs were committed together at **08:00:58 JST**, before the 09:00 opening. Their `issued_at` field says **08:00:01 JST**. The GitHub commit timestamp represents the auditable actual publication and is not the same as the declared record `issued_at`. This distinction is documented instead of claiming exact-second issuance at 08:00:01.

Today’s 09:00 opening, 15:30 close, and intraday market movement were accessed **only after the session** and did not inform the original frozen forecast.

## 1. Facts (source: Nikkei official published cash-index history, after 15:30)

2026-10-13:

| Fact | Published Nikkei 225 cash-index value |
| --- | ---: |
| Opening, 09:00 JST | **68,564.85** |
| High | **68,710.99** |
| Low | **67,058.56** |
| Closing, 15:30 JST | **67,777.52** |
| Close minus open | **-787.33** points |
| Close minus prior cash trading day (Oct 9) close of 69,030.92 | **-1,253.40** points, about -1.82% |

**Do not confuse** -1,253.40 previous-close-to-close with -787.33 open-to-close. The research's 09:00→15:30 comparison is based on **the latter**.

Public-cash-index **proxy** log return, not formal XM return:

`10,000 × ln(67,777.52 / 68,564.85) = -115.4943619911048 bps`; rounding to **-115.49 bps**. Public cash-index proxy binary direction `y_up=0` (down).

## 2. Pre-cutoff forecasts compared to one public proxy event (nonformal)

The frozen probabilities and forecasts were not changed after seeing the observed cash close.

| System | Frozen P(up) | Forecast return | Proxy Brier (y=0) | Proxy absolute-return error |
| --- | ---: | ---: | ---: | ---: |
| B0 neutral | 0.50 | 0 bps | 0.2500 | 115.49 bps |
| A1 proxy market only | 0.49 | -2 bps | 0.2401 | 113.49 bps |
| A2 cross-market | 0.47 | -6 bps | 0.2209 | 109.49 bps |
| A3 repo status | 0.48 | -4 bps | 0.2304 | 111.49 bps |

Methods: `proxy_brier = (p_up-0)^2`; `proxy_absolute_error = |forecast_return_bps - (-115.4943619911048)|`. These are **descriptive single-event public-index scores**, not XM model Brier/MAE and not eligible for the 60-event matched benchmark.

## 3. Result / interpretation / decision

### Result

- A1, A2 and A3 all placed `P(up)<0.5` before the cutoff. The published public cash index subsequently declined from its opening, so their predicted **direction** aligned with the public proxy.
- Their predicted decline magnitudes of **-2 to -6 bps** were substantially smaller than the observed **-115.49 bps** proxy fall, so all materially underestimated the decline.
- Within this one proxy observation, A2 had the smallest Brier and absolute error and the B0 neutral baseline the largest. These comparisons say nothing reliable about long-run superiority.

### Interpretation (tentative, strictly post-outcome)

The recorded pre-cutoff assessment noted adverse public futures opening context, mixed U.S. Dow/Nasdaq performance, higher oil, weak JPY, and substantial public mini-futures source contradictions. The price decline from open to close is consistent **in direction** with the tentative bearish view, but its magnitude exceeded that view markedly.

Today's outcome must **not** be used to claim the futures input had validated predictive power, upgrade unsupported EMA/reversal research, retune an A2/A3 probability, or select a new trading rule. Previous two public-index proxy comparisons on Oct 8 (down) and Oct 9 (up) and today were all exploratory and should not be treated as a frozen formal calibration sample.

### Decision / research gates

- Original forecast JSONs, pre-cutoff snapshots, probabilities, and hashes: **UNCHANGED**.
- Formal target: `MARKET_OUTCOME_UNAVAILABLE` by explicit XM no-acquisition choice, **not** a provider fetch failure.
- Cohort: `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT` permanently. Formal scored cohort `CLOSED`.
- Candidate spec `PROPOSED_NOT_FROZEN`; scientific verdict `UNTESTED`; source readiness `PARTIAL`.
- NO_TRADE. No feature, parameter, weights, source replacement, timing, or post-hoc performance-based rule change.
- Separate historical Oct 6 forecast-hash inconsistency remains an unresolved audit issue and was not fixed by today's diagnostic.

## 4. Sources and provenance

1. **Nikkei, official historical daily OHLC, updated 2026-10-13:** https://indexes.nikkei.co.jp/nkave/archives/data?list=daily — Oct 13 open 68,564.85, high 68,710.99, low 67,058.56, close 67,777.52; Oct 9 close 69,030.92.
2. **Nikkei official index overview, updated after close 2026-10-13:** https://indexes.nikkei.co.jp/nkave/index/profile — close 67,777.52 (-1,253.40), opening 68,564.85 at 09:00.
3. **Trader's Web, 2026-10-13 15:45 update:** https://www.traders.co.jp/index/0101 — independently matches opening 68,564.85, high 68,710.99, low 67,058.56, closing 67,777.52.
4. **Fisco closing bulletin, 2026-10-13 15:32:** https://minkabu.jp/news/4634139 — independently confirms 67,777.52 closing and -1,253.40 prior-close move.
5. Pre-outcome, SHA-pinned source and frozen probabilities: https://github.com/Josh-Temple/systematic-trading-research/blob/5804cc24264bf4a72746515bf74042fb3ef52b53/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-13_PRE_CUTOFF_ASSESSMENT.md
6. Immutable forecast issuance commit: https://github.com/Josh-Temple/systematic-trading-research/commit/cbbc15958f269806fd0600cbc1196fcc73e9e13c

**No formal XM outcome is asserted by any of the public-index figures above.**
