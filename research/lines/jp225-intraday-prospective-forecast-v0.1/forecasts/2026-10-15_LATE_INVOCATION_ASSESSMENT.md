---
type: LateInvocationAssessment
event_id: XPF-JP225-20261015
assembled_at: 2026-10-15T08:12:21.546+09:00
information_cutoff: 2026-10-15T08:00:00+09:00
pre_cutoff_pre_registration: MISSING
pre_cutoff_quantitative_snapshot: MISSING
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# 2026-10-15 JP225: late invocation and source assessment

**Not an 08:00 forecast.** The user requested this after 08:00 JST; the fresh-read GitHub branch at c577768b54a0a928b62d83bf2301bab5f576685c had no Oct 15 event. We did **not** backdate a registration or claim a pre-cutoff numerical freeze. This assessment and the A1/A2/A3 records are created in a single **late, pre-09:00 exploratory** issuance commit. The earliest report dates precede 08:00, but the pages were **accessed after 08:00**, and no prior byte-level captures exist. These are intentionally marked as provenance deviations. No after-08:00 publication and no Oct 15 Japanese cash opening or outcome was used to choose values.

**Protocol:** Oct 15 scheduled JPX trading day (https://www.jpx.co.jp/calendar/202610.html); 08:00 JST information cutoff, 09:00 to 15:30 JST exact XM MT5 JP225Cash midpoint is the *formal reference*. No XM actual data by owner choice; public news is contextual proxy. Science UNTESTED, specification PROPOSED_NOT_FROZEN, scored cohort CLOSED, NO_TRADE.

## Facts from dated pre-08:00 publications, retrieved after the cutoff

- OSE Nikkei 225 Dec future night close **66,480** at 06:00 JST on Oct 15, **-1,680** versus prior future settlement, 1,264.29 below yesterday's cash close 67,744.29. Dated report 06:03 JST: https://minkabu.jp/news/4635705. The gap primarily influences the **opening**; no evidence it continues during 09:00 to 15:30.
- US close, dated report **05:36 JST**, Nasdaq **26,692.87 (-1.88%)**, S&P500 **7,718.94 (-1.11%)**, Dow **51,621.48 (-0.09%)**, CME Nikkei **66,630** around 05:25 JST: https://fx.minkabu.jp/news/381582. Venue and observation time differ from OSE.
- 06:20 JST New York recap: USDJPY **158.33** (~flat), U.S. ten-year **5.19% (-0.02 percentage points)**, Nov WTI **95.09 USD (+0.95)**, U.S. September headline CPI MoM **+0.6%**: https://www.oanda.jp/lab-education/market_news/mn_1038953_202610150620/. US CPI annual **3.7% vs 3.6% forecast**, core **2.6% vs 2.5% forecast**, dated 04:29 JST: https://s.kabutan.jp/news/n202610150055/.
- GitHub main pinned at `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`: exact XM JP225 EMA **UNTESTED/WAITING_FOR_XM_STAGE1_DATA**; OANDA 2017 persistence **PERSIST5_PROXY_NOT_SUPPORTED_2017** (https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md); U.S. lead proxy **STOPPED/USLEAD_PROXY_NOT_SUPPORTED_2015** (https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md).

## Exploratory quantitative decision, after-cutoff only

| System | P(up, 09:00 to 15:30) | Forecast log-return |
| --- | ---: | ---: |
| B0 neutral | 0.50 | 0 bps |
| A1 public futures proxy | 0.49 | -3 bps |
| A2 plus published U.S. macro/equity/FX | 0.45 | -12 bps |
| A3 plus status-preserving repository evidence | **0.47** | **-7 bps** |

**A3: mildly bearish, very low confidence, NO_TRADE**. These are subjective candidate guesses, **not statistically calibrated probabilities**. The gap does not automatically imply post-open continuation. A3 moderates A2 because historical proxy/EMA sources do not validate a stronger bearish forecast. No model training, coefficient selection or adjustment from Oct 6/8/9/13/14 exploratory results occurred.

Explicit flags: LATE_ISSUANCE_AFTER_0800, NO_PRE_CUTOFF_PRE_REGISTRATION, NO_PRE_CUTOFF_QUANTITATIVE_SNAPSHOT, PUBLISHED_PRE_CUTOFF_SOURCES_RETRIEVED_POST_CUTOFF, EXACT_XM_0800_INPUT_UNAVAILABLE, PUBLIC_NON_XM_MARKET_CONTEXT_USED_FOR_EXPLORATORY_DRY_RUN.

For any later review, if qualified XM exact start/end quotes are unavailable, preserve formal outcome `MARKET_OUTCOME_UNAVAILABLE`, null return and `scores={}`. Any cash-index comparison is a *separate* PUBLIC_PROXY_REVIEW, not an XM substitute. No trading or rules changes.
