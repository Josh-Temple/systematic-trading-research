---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261020
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-20T23:06:34.266+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
original_issuance_integrity: CURRENT_20261020_HASHES_SEPARATELY_READABLE_BUT_BRANCH_BLOCKED_BY_20261016
---

# JP225 — 2026-10-20 after-close PUBLIC Nikkei 225 cash-index proxy diagnostic

## Evidence boundaries, timing and original forecast provenance

**Not the formal exact XM outcome.** The designated instrument for the v0.1 prospective benchmark is XM MT5 `JP225Cash` qualified Bid/Ask 09:00 and 15:30 JST midpoints. These were NOT obtained by owner direction. The separate formal review `2026-10-20_review.json` therefore retains `MARKET_OUTCOME_UNAVAILABLE`, null quotes, null return, null `y_up`, and empty formal `scores={}`.

The latest three forecast JSONs were originally created with `issued_at=2026-10-20T08:40:47.923+09:00` and published at GitHub commit `685fd8e227b7fdf7bb61f44c2e16739251dfd918` at **08:40:54 JST**, before the 09:00 opening. The **08:00 cutoff was already missed**; no pre-08:00 pre-registration or numerical snapshot exists. Articles published before 08:00 were retrieved after cutoff, without the historical raw-page 08:00 bytes. This makes the event permanently **LATE_ISSUANCE_AFTER_0800 / EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT** and **ineligible** for formal 60-event scoring.

The branch remains **BLOCKED_INTEGRITY** by the October 16 issuance: original `2026-10-16_A1/A2/A3_forecast.json` have 512-character malformed SHA-256 fields, documented in `2026-10-16_INTEGRITY_FAILURE_RECEIPT.md`. Original faulty records remain immutable; the current review neither removes nor waives the validator failure. October 20's new hashes do not establish a passing branch validator.

## Post-close official Nikkei 225 cash-index observations

| Observation | October 20, 2026 |
| --- | ---: |
| Opening at 09:00 JST | **64,755.49** |
| High at 09:00 | **64,822.22** |
| Low at 15:02 | **63,807.15** |
| Closing at 15:30 JST | **64,075.42** |
| **Close minus open** | **-680.07 points** |
| Close minus previous JPX cash session close Oct 19 64,916.70 | **-841.28 points** |
| Published previous-close-to-close percentage | **-1.30%** |

**The research interval is 09:00→15:30, not previous close→close.** The latter -841.28 and -1.30% are not the target.

Cash-index nonformal **proxy** simple intraday return: `100*(64075.42/64755.49 - 1) = -1.05021211%`.

Cash-index nonformal **proxy** intraday log return: `10000*ln(64075.42/64755.49) = -105.576575829415 bps`, rounded **-105.58 bps**. This corresponds to **proxy_y_up=0** for the separate public cash index ONLY.

Sources observed **after** the close:
- Nikkei official daily summary https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261020&idx=nk225 (October 20 OHLC, -841.28 previous cash close)
- Nikkei Oct 19 prior-cash-session summary https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261019&idx=nk225 (64,916.70 prior close)
- Public historical price cross-check https://jp.investing.com/indices/japan-ni225-historical-data (Oct 20 open/high/low/close)
- Original late exploratory issuance https://github.com/Josh-Temple/systematic-trading-research/commit/685fd8e227b7fdf7bb61f44c2e16739251dfd918
- Existing Oct 16 evidence https://github.com/Josh-Temple/systematic-trading-research/blob/3c3a06d24b0234a4c53fcbc7d6cdc58bf609b080/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-16_INTEGRITY_FAILURE_RECEIPT.md

## Strictly nonformal frozen prediction comparison

Frozen during the **late-issued, pre-09:00** October 20 forecast:

| System | Original P(up) | Original forecast bps | Public-proxy Brier (y=0) | Public-proxy absolute error bps | Proxy direction |
| --- | ---: | ---: | ---: | ---: | --- |
| B0 | 0.50 | 0 | 0.2500 | 105.58 | Neutral; no directional prediction |
| A1 | 0.49 | -2 | 0.2401 | 103.58 | Mildly DOWN, matches proxy direction |
| A2 | 0.50 | 0 | 0.2500 | 105.58 | Neutral; no directional prediction |
| A3 | 0.50 | 0 | 0.2500 | 105.58 | Neutral; no directional prediction |

Nonformal definitions: `public_proxy_brier = (p_up-0)^2` and `public_proxy_absolute_error_bps = |forecast_bps - -105.576575829415|`. These **are not XM scores** and must not be aggregated with the formal prospective 60-event cohort. The uncalibrated p-values do not constitute known hit probabilities.

### Results (facts)

- The publicly published Nikkei cash-index return between the 09:00 opening and 15:30 close was **-105.58 bps**, so the observed direction was DOWN.
- Original A1 forecast a tiny decline (-2 bps, p(up)=0.49), which aligned in **direction** with the published index proxy but **underestimated magnitude by 103.58 bps**.
- Original A2 and A3 (and B0) were neutral at p(up)=0.50 and 0bps. These do **not** count as successful directional predictions; their public-proxy absolute magnitude errors were 105.58 bps.
- A1 single-event proxy Brier was 0.2401 vs neutral's 0.2500: too little evidence for relative forecasting skill.

### Tentative interpretation and decision

The pre-08:00-dated market reports had a mildly negative Osaka future overnight, U.S. Nasdaq strength, a weaker yen, elevated oil and U.S. Treasury yields; these signals were mixed. A subsequent declining Japanese cash market does not prove which of these inputs forecasted a post-opening sell-off. The candidate's **neutral** main A3 forecast and weakly negative A1 did not anticipate the full -1.05% cash intraday decline.

**Decision:** No prospective cohort admission, no adjustment to forecasts/returns/probabilities/hashes or source/timing rules, no optimization based on this single outcome, no claimed strategy edge, no live/paper trading or P/L. Keep `UNTESTED / PROPOSED_NOT_FROZEN / SCORED_COHORT_CLOSED / NO_TRADE`. Preserve the October 16 malformed issuance and continued CI FAIL pending independently accepted append-preserving repair.
