---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261023
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-23T22:26:42.935+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
formal_score_status: MARKET_OUTCOME_UNAVAILABLE_EXACT_XM_NOT_ACQUIRED
source_qualification: KABUTAN_DATED_AFTER_CLOSE_OHLC_KYODO_AND_NSJ_CLOSE_CORROBORATED_OFFICIAL_DAILY_NOT_YET_UPDATED
integrity_status: CI_FAIL_20261016_ORIGINAL_ISSUED_SHA256_MALFORMED
---

# Oct 23 2026 — post-close PUBLIC Nikkei cash-index proxy review (NONFORMAL)

## 1. Scientific boundary and chronological evidence

**PUBLIC CASH INDEX, NOT XM MT5 JP225Cash.** The formal benchmark is **exact qualified XM JP225Cash 09:00→15:30 JST Bid/Ask midpoint**, not the published Nikkei 225 cash-index session. The corresponding formal `2026-10-23_review.json` therefore preserves `exact_xm_outcome_status=MARKET_OUTCOME_UNAVAILABLE`, `start_quote=null`, `end_quote=null`, `realized_return_bps=null`, `y_up=null`, `scores={}`, because the owner has not acquired qualified XM ticks. Do not migrate the descriptive proxy label and scores to the formal dataset, or to the future 60-event cohort.

Original A1/A2/A3 forecast JSON was issued at GitHub commit `8096bca567e4fd86434c0ecafa2ba56b47f8504b`, timestamp **2026-10-23 08:05:37 JST**, before 09:00 cash opening but **after strict 08:00 forecast information cutoff**. All three stored `issued_at=2026-10-23T08:05:28.715+09:00`, `p_up=0.50` and `forecast_return_bps=0`; the B0 benchmark is likewise 0.50 / 0bps. These values are immutable and unchanged.

There was **NO Oct 23 pre-08:00 preregistration, quantitative freeze, or qualified current-date 08:00 data**. A purported Oct 23 night-futures 06:00 article with unverified pre-08 publication time was **EXCLUDED**. A2's otherwise available U.S. report was **one complete U.S. session stale**, and was also not admitted as a contemporary signal. 0.50 and 0bps were issued as **missing-input neutral defaults**, not evidence of small market volatility or statistical calibration. The session is **EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT** and cannot become a formal on-time observation retroactively.

**Existing blocked integrity:** original issued 2026-10-16 A1/A2/A3 have malformed **512-character** SHA-256 instead of 64; branch CI fails at validator. Original corrupt artifacts and documented failure are intentionally retained, no suppression, original modification, merge, or backdating.

## 2. Post-close Nikkei 225 cash-index observations

The primary dated post-close market recap from **Kabutan via Livedoor News**, 2026-10-23 **16:28 JST**, reports:

| Observation | 2026-10-23 public cash-index value |
| --- | ---: |
| Opening (09:00 JST) | **62,667.05** |
| High | **62,786.89** |
| Low | **61,462.61** |
| Official cash close, as reported at 15:30 | **62,693.16** |
| **Close minus opening** | **+26.11 points** |
| Prior Oct 22 cash closing | **62,907.84** |
| **Close minus preceding day's close** | **-214.68 points (-0.34%)** |

The **2026-10-23 15:35 JST Kyodo** dispatch and **2026-10-23 Nihon Shoken Shimbun** closing recap separately corroborate the closing 62,693.16 and previous-close fall 214.68. Primary dated articles:
- https://news.livedoor.com/article/detail/32640251/ — Kabutan market close article carried at 16:28; complete daily opening/high/low/close
- https://kumanichi.com/articles/2049834 — Kyodo 15:35 close (62,693.16 and -214.68)
- https://www.nsjournal.jp/%E5%A4%A7%E5%BC%95%E3%81%91%E3%81%AE%E4%B8%BB%E8%A6%81%E5%B8%82%E5%A0%B4%E6%A0%AA%E4%BE%A1%E6%8C%87%E6%95%B0%E3%80%80%E6%97%A5%E7%B5%8C%E5%B9%B3%E5%9D%87%E6%A0%AA%E4%BE%A1%EF%BC%9A62693-16-214-68/ — Nihon Shoken Shimbun 2026-10-23 close (62,693.16 and -214.68)

**Freshness/conflict annotation:** https://indexes.nikkei.co.jp/nkave/archives/data/ was still **updated through 2026-10-22**, i.e. there was NO independently fetched official Oct 23 Nikkei data row at review. Some dynamic quote-history pages (https://stocks.monex.co.jp/JP%3A%24MNK/historical and https://jp.investing.com/indices/japan-ni225-historical-data) show inconsistent, apparently intraday-persisted Oct 23 close figures (Monex 62,261.81; Investing 62,019.50). Even some Kabutan dynamic history output carried a live intraday `62,108`, not the final close. They **conflict with three date-stamped independent post-close articles** and are excluded from this after-close calculation. This proxy row must be independently reconciled with the official Nikkei daily row when published. Do not silently switch to a conflicting snapshot or claim that Nikkei official Oct 23 OHLC was already available.

**Do not confuse return definitions**: prior-close→today-close is **-214.68 points (-0.34%)**, whereas the research interval 09:00→15:30 is **+26.11 points (positive)**.

Public-index NONFORMAL simple 09:00→15:30 return:
`100 * (62693.16/62667.05 - 1) = 0.041664638754%`, approximately **+0.04%**.

Public-index NONFORMAL log return:
`10000 * ln(62693.16/62667.05) = 4.165596145309bps`, approximately **+4.17bps**.
PUBLIC ONLY `proxy_y_up=1` (UP).

## 3. Frozen forecast vs nonformal public-index outcome

| System | Frozen subjective P(up) | Frozen predicted log return (bps) | Public-proxy Brier if y=1 | Public-proxy abs return error (bps) | Direction call |
| --- | ---: | ---: | ---: | ---: | --- |
| B0 | 0.50 | 0 | 0.25 | 4.17 | Neutral / no signed prediction |
| A1 | 0.50 | 0 | 0.25 | 4.17 | Neutral / no signed prediction |
| A2 | 0.50 | 0 | 0.25 | 4.17 | Neutral / no signed prediction |
| A3 | 0.50 | 0 | 0.25 | 4.17 | Neutral / no signed prediction |

Definitions: `proxy_brier=(p_up-1)^2`, `proxy_abs_error_bps=|forecast_bps-4.165596145309|`. These are **NONFORMAL diagnostic calculations**, NOT XM scores, not validated calibration, and not a scored cohort. With P(up)=0.50 and forecast 0bps, neither A1, A2, A3 nor B0 made a signed UP or DOWN forecast.

## 4. Result, interpretation, decision

**Observations:** The published public Nikkei average began at 62,667.05, fell to intraday low 61,462.61, and recovered to post-close reported 62,693.16, **+26.11 points (+4.17 log bps) versus today's open**, while remaining **-214.68 points versus yesterday's close**. The source disagreement on stale dynamic quote-history pages is recorded, and three post-close date-stamped articles agree on the final close.

**Result:** Morning A1, A2 and A3 were all neutral **due to insufficient time-qualified current information**, 0.50 probability and 0bps. The actual public proxy moved up slightly, but do **not** call this a directionally successful prediction. The common descriptive absolute error is 4.17bps, Brier 0.2500; comparing models on this event produces an exact tie by construction, not evidence that any one is best.

**Interpretation (not experiment evidence):** A large intraday fall and late rebound can leave very small open→close net change; the magnitude of intraday range need not equal the net log return. This one late-issued, input-incomplete public cash-index proxy observation does not establish predictability of the intraday rebound, estimate strategy profitability, or resolve data sourcing. Refrain from optimising on the narrative.

**Decision:** Keep original A1/A2/A3 JSON records and SHA untouched. Keep exact XM formal outcome **UNAVAILABLE** with null endpoints/score. Maintain research `UNTESTED`, spec `PROPOSED_NOT_FROZEN`, 60-event formal cohort `CLOSED`, `NO_TRADE`. CI `FAIL/BLOCKED_INTEGRITY` persists for immutable 2026-10-16 malformed issued hash fields; do not weaken validation or suppress it for cosmetic green checks. No features, price-source substitutions, forecast weights, thresholds, or trading permissions change from this one proxy result.

## 5. Supporting provenance links

- Post-close OHLC Kabutan/Livedoor: https://news.livedoor.com/article/detail/32640251/
- Independent closing Kyodo: https://kumanichi.com/articles/2049834
- Independent closing NSJ: https://www.nsjournal.jp/%E5%A4%A7%E5%BC%95%E3%81%91%E3%81%AE%E4%B8%BB%E8%A6%81%E5%B8%82%E5%A0%B4%E6%A0%AA%E4%BE%A1%E6%8C%87%E6%95%B0%E3%80%80%E6%97%A5%E7%B5%8C%E5%B9%B3%E5%9D%87%E6%A0%AA%E4%BE%A1%EF%BC%9A62693-16-214-68/
- Official Nikkei historical daily page, **not yet updated for Oct 23** at review: https://indexes.nikkei.co.jp/nkave/archives/data/
- Dynamic quote snapshots excluded as final daily values: https://stocks.monex.co.jp/JP%3A%24MNK/historical ; https://jp.investing.com/indices/japan-ni225-historical-data
- Original frozen-but-late issue commit: https://github.com/Josh-Temple/systematic-trading-research/commit/8096bca567e4fd86434c0ecafa2ba56b47f8504b
- Existing malformed October 16 SHA-256 evidence: https://github.com/Josh-Temple/systematic-trading-research/blob/8096bca567e4fd86434c0ecafa2ba56b47f8504b/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-16_INTEGRITY_FAILURE_RECEIPT.md
