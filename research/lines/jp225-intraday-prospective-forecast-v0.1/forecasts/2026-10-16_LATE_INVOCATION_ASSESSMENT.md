---
type: LateInvocationAssessment
event_id: XPF-JP225-20261016
assembled_at: 2026-10-16T08:06:56.165+09:00
information_cutoff: 2026-10-16T08:00:00+09:00
pre_cutoff_pre_registration: MISSING
pre_cutoff_quantitative_snapshot: MISSING
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# Oct 16 JP225 source review / late-issuance audit

**This is NOT an on-time 08:00 prospective forecast.** Fresh-read GitHub at initial HEAD `4d6792a09a781c2fb7bb8cc77f9c3c4bdff7cde2` contained no 2026-10-16 event. User request arrived after 08:00 JST. The source reports were published before 08:00, but fetched **after** the cutoff without a frozen pre-08:00 raw copy. No false point-in-time registration or quantitative snapshot is created. Numerical forecasts are first fixed by this post-cutoff, pre-open commit. Formal cohort eligibility is permanently prohibited.

**Research target:** Oct 16 scheduled JPX cash-equity trading day, 09:00 to 15:30 JST signed log return of exact qualified XM MT5 `JP225Cash` Bid/Ask midpoint; NOT previous close to cash close and NOT overnight OSE futures. No XM price was acquired per owner instruction. Source readiness PARTIAL, SPEC PROPOSED_NOT_FROZEN, science UNTESTED, formal scored cohort CLOSED, NO_TRADE.

## Before-08:00 published source observations (reviewed after cutoff)

1. JPX official calendar shows Friday October 16 eligible cash session: https://www.jpx.co.jp/calendar/index.html.
2. Oct 16 06:03 JST Kabutan/Minkabu report: 06:00 JST OSE Nikkei future December maturity **65,520**, **+720** versus previous futures settlement, **1,094.05** above Oct 15 cash index close 64,425.95. Night futures mini 65,530 +730, TOPIX future 4047 +32. Source: https://s.minkabu.jp/news/4637080. Futures level and previous-cash-index closing price are distinct from intraday target.
3. OANDA NY market digest published **06:20 JST**, Oct 15 U.S. closing levels: Dow **52,177.69** (+556.21), Nasdaq composite **26,713.03** (+20.16), USDJPY **158.00** (JPY firmer by 0.33), U.S. 10-year yield **5.06%** (down 0.13 percentage points), Nov WTI **USD97.97** (+2.88). Source: https://www.oanda.jp/lab-education/market_news/mn_1039183_202610160620/. Positive Dow vs almost flat Nasdaq, falling yield and rising oil do NOT form a one-sign forecast for JP225 post-open return.
4. Kyodo report **06:38 JST** quotes USDJPY 157.94 to 158.04 at NY 17:00, confirming the ~158.00 quote, but not an independent instrument midpoint at 08:00: https://kumanichi.com/articles/2047105.
5. Dated market snapshot **04:22 JST** had CME Nikkei future 65,740 around JST 04:12, a different venue/time than OSE 06:00 and cannot be conflated: https://fx.minkabu.jp/news/381737.
6. Pinned main `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`: exact-XM JP225 EMA `UNTESTED/WAITING_FOR_XM_STAGE1_DATA`; OANDA 2017 persistence proxy `PERSIST5_PROXY_NOT_SUPPORTED_2017`; US-lead reversal `STOPPED/USLEAD_PROXY_NOT_SUPPORTED_2015`. Sources: https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-ema-timeofday-v0.1/CURRENT.md; https://github.com/Josh-Temple/systematic-trading-research/blob/33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3/research/lines/jp225-us-lead-reversal-v0.1/CURRENT.md.

## Late subjective estimate, fixed once in commit

| System | P(up, cash 09:00 to 15:30) | Predicted log return |
| --- | ---: | ---: |
| B0 neutral | 0.50 | 0 bps |
| A1 public OSE proxy only | 0.51 | +2 bps |
| A2 plus cross-market/news | 0.50 | 0 bps |
| A3 plus unsupported/untested repo statuses | **0.50** | **0 bps** |

**A3 headline: neutral, no validated post-open directional advantage; NO_TRADE.** Numerical values are subjective and uncalibrated. The user did NOT get an on-time 08:00 inference. Neither adverse Oct 15 realized market outcome nor results of Oct 6/8/9/13/14 exploratory samples were used to tune weights, thresholds, feature lists, or directional probability.

Event deviations: LATE_ISSUANCE_AFTER_0800; NO_PRE_CUTOFF_PRE_REGISTRATION; NO_PRE_CUTOFF_QUANTITATIVE_SNAPSHOT; PRE_CUTOFF_PUBLISHED_SOURCES_RETRIEVED_AFTER_0800; EXACT_XM_0800_INPUT_UNAVAILABLE; PUBLIC_NON_XM_PROXY_CONTEXT.

**No Oct 16 09:00 cash opening, subsequent intraday, or 15:30 outcome was fetched to issue these predictions.** The authoritative external issuance/publication time is the timestamp of this atomic GitHub commit, distinct from JSON generation timestamp `2026-10-16T08:06:56.165+09:00`. Post-close formal XM scoring stays `MARKET_OUTCOME_UNAVAILABLE` absent qualified exact XM quote acquisition; separately published Nikkei cash-index proxy diagnostics are not substitutes.
