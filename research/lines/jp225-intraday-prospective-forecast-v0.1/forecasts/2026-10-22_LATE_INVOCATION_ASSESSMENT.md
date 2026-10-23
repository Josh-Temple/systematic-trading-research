---
type: LateInvocationAssessment
event_id: XPF-JP225-20261022
assembled_at: 2026-10-22T08:08:01.372+09:00
information_cutoff: 2026-10-22T08:00:00+09:00
pre_cutoff_pre_registration: MISSING
pre_cutoff_quantitative_snapshot: MISSING
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
integrity: BLOCKED_HISTORICAL_OCT16
---

# Oct 22 JP225 — late pre-open exploratory assessment

**Timing fact:** Request received after 08:00 JST. At fresh GitHub read, PR #62 head `04a1cfe8e988c2fc166a680b78f6aed111793d92` included NO 2026-10-22 preregistration or quantitative forecast. This new forecast is created after the 08:00 information cutoff. No backdated content or claim of pre-08:00 fixed numbers. Verify the actual issue GitHub commit time independently; JSON `issued_at` is 2026-10-22T08:08:01.372+09:00.

**Target:** 2026-10-22 scheduled JPX regular cash day, **09:00 to 15:30 JST**, exact qualified XM MT5 `JP225Cash` Bid/Ask midpoint log return, NOT overnight futures or Japanese previous-close-to-close. Calendar https://www.jpx.co.jp/calendar/index.html.

**Source qualification:** Only pre-08:00 *published* reports informed estimates, but these were retrieved after cutoff; no immutable exact 08:00 website bytes were preserved. No actual XM 08:00 Bid/Ask/lookbacks or qualified XM 09:00/15:30 outcome source is available under established acquisition hold. This is a proxy-only exploratory candidate, permanently `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`, research `UNTESTED`, spec `PROPOSED_NOT_FROZEN`, formal 60-event cohort `CLOSED`, `NO_TRADE`.

## Facts separated from interpretation

1. MINKABU NY market update, published **2026-10-22 02:27 JST**, for market quotes observed around **02:17 JST**: CME Nikkei Dec futures **65,140 (+360)** versus Osaka reference, NY Dow **52,735.77 (+239.89)**, Nasdaq **26,773.19 (+348.37)**. https://fx.minkabu.jp/news/382250
2. A later MINKABU update, published **03:14 JST**, gives **03:04 JST** snapshots NY Dow **52,780.72 (+284.84, +0.54%)**, Nasdaq **26,740.73 (+315.91, +1.20%)**, CME Nikkei futures **65,070 (+290 vs Osaka)**, European DAX closing **25,645.04 (+1.35%)**, WTI **December** future **96.90 (-0.92)**, U.S. 10Y yield **5.107% (-0.002pp)**. https://fx.minkabu.jp/news/382254
3. These New York equity quotes are **INTERIM NY-session values**, NOT claimed final U.S. closes. No exact 06:00 Osaka night close was verifiably captured in a frozen pre-08:00 source during this run. No post-08:00-published reports or post-09:00 Japanese index observations were used for prediction.
4. Repository main pinned to `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`: exact XM EMA remains `UNTESTED / WAITING_FOR_XM_STAGE1_DATA`; US lead reversal `STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015`. These results are not a validated current directional signal. https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md ; https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md.
5. October 16 published A1/A2/A3 have malformed 512-hex-digit SHA fields; an independent report preserves original failures. Existing CI `FAIL / BLOCKED_INTEGRITY` and must not be weakened or re-labeled PASS. https://github.com/Josh-Temple/systematic-trading-research/blob/04a1cfe8e988c2fc166a680b78f6aed111793d92/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-16_INTEGRITY_FAILURE_RECEIPT.md.

## Candidate inference — subjective and uncalibrated

| System | P(up for 09:00→15:30) | Log return forecast |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 dated CME futures proxy | 0.51 | +2 bps |
| A2 interim U.S. equities/Europe/oil | 0.52 | +4 bps |
| A3 with untested/negative repository statuses | **0.51** | **+2 bps** |

A3 is **effectively neutral with tiny bullish tilt**, very low confidence; **NO_TRADE**. Subjective p-values are not calibrated, not fitted, and not revised based on 2026-10-21 or earlier exploratory proxy outcomes. A higher overnight future is primarily a possible **opening gap**, not evidence that Japanese cash will rise after 09:00. The relatively positive 03:04 snapshot is not a qualified complete 08:00 market-information set.

**Protocol deviations**: LATE_ISSUANCE_AFTER_0800; NO_PRE_CUTOFF_PRE_REGISTRATION; NO_PRE_CUTOFF_QUANTITATIVE_SNAPSHOT; PRE_CUTOFF_PUBLISHED_SOURCES_RETRIEVED_AFTER_0800_WITHOUT_RAW_0800_SNAPSHOTS; EXACT_XM_0800_INPUT_UNAVAILABLE; PUBLIC_NON_XM_PROXY_CONTEXT; US_MARKET_EARLY_INTRASESSION_QUOTES_NOT_FINAL_US_CLOSE; BRANCH_VALIDATOR_BLOCKED_BY_20261016_INVALID_SHA256_FIELDS.

## Decision

Append original forecast and this provenance once before 09:00; later preserve all forecast bytes even if outcome contradicts. No rule, feature, threshold, or model selection changes. After 15:30, keep exact XM formal `MARKET_OUTCOME_UNAVAILABLE` with null endpoints, returns and scores if data not acquired; separately mark any official public Nikkei cash-index comparisons as nonformal. Do not repair old invalid issued artifacts by overwriting or suppressing integrity validation.
