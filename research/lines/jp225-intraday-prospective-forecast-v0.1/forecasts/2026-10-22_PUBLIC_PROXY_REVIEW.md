---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261022
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-22T21:56:39.720+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
formal_score_status: MARKET_OUTCOME_UNAVAILABLE_EXACT_XM_NOT_ACQUIRED
source_qualification: PUBLIC_MONEX_OHLC_MATCHING_NSJ_CLOSE_NIKKEI_OFFICIAL_ROW_PENDING
integrity_status: CI_FAIL_20261016_ORIGINAL_ISSUED_SHA256_MALFORMED
---

# 2026-10-22 JP225 — Public Nikkei cash-index proxy AFTER-CLOSE diagnostic

## A. Scientific status and frozen issue audit

**PUBLIC-INDEX-ONLY / NONFORMAL**. The research benchmark would target qualified exact XM MT5 `JP225Cash` Bid/Ask midpoints for the 09:00-15:30 JST regular Japanese cash session. This source was NOT acquired by owner direction. The formal review `2026-10-22_review.json` therefore preserves `exact_xm_outcome_status="MARKET_OUTCOME_UNAVAILABLE"`, `start_quote=null`, `end_quote=null`, `realized_return_bps=null`, `y_up=null`, `scores={}`. The figures below must NEVER be substituted into that formal record or enter the planned 60-event scored prospective cohort.

The immutable A1/A2/A3 predictions were issued together in GitHub commit `13e39df0fd7d2ad670c896b9d312d522ad090045`, actual commit at **2026-10-22 08:08:11 JST**; JSON `issued_at` was **08:08:01.372 JST**. The request occurred AFTER the strict 08:00 information cutoff, without Oct 22 pre-registration or quantitative freeze. Time-stamped early NY market reports were published before 08:00 but retrieved after cutoff with no 08:00 raw-byte snapshot; interim U.S. quotes were not the final U.S. session closes. This event is **LATE_ISSUANCE_AFTER_0800 / EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT**, permanently **not an on-time prospective benchmark observation**. No published Oct 22 cash opening or closing prices were used to form or adjust the issue-time forecasts.

Branch CI is still **FAIL / BLOCKED_INTEGRITY**: the original 2026-10-16_A1/A2/A3_forecast.json files contain 512-character stored `canonical_sha256` values (only 64 hexadecimal characters allowed). Those records and their `2026-10-16_INTEGRITY_FAILURE_RECEIPT.md` are retained, and current review does not waive/alter/repair those failures.

## B. After-close public cash-index data and provider freshness

Data source **Monex Securities** current Nikkei 225 historical OHLC, 2026-10-22 row:
https://stocks.monex.co.jp/JP:%24MNK/historical

Independent close and previous-close difference corroboration **Nihon Shoken Shimbun**, dated 2026-10-22:
https://www.nsjournal.jp/%E5%A4%A7%E5%BC%95%E3%81%91%E3%81%AE%E4%B8%BB%E8%A6%81%E5%B8%82%E5%A0%B4%E6%A0%AA%E4%BE%A1%E6%8C%87%E6%95%B0%E3%80%80%E6%97%A5%E7%B5%8C%E5%B9%B3%E5%9D%87%E6%A0%AA%E4%BE%A1%EF%BC%9A62907-84-1713-40/

**Freshness caveat:** official Nikkei Indexes daily data page https://indexes.nikkei.co.jp/nkave/archives/data/ had last been updated **2026-10-21** at review time and had **no 2026-10-22 row**. Today's full OHLC below is therefore based on Monex Securities, not a falsely claimed official Nikkei row. The reported closing value 62,907.84 is independently corroborated by NSJ. Original figures should be independently reaccepted if/when the Nikkei official page is updated. Nothing here counts as formal exact-XM source qualification.

| Item | PUBLIC Nikkei 225 cash index, 2026-10-22 |
| --- | ---: |
| 09:00 opening | **64,539.36** |
| Session high | **64,866.44** |
| Session low | **62,907.84** |
| 15:30 close | **62,907.84** |
| **Close minus 09:00 open** | **-1,631.52 index points** |
| Previous JPX cash close (Oct 21) | **64,621.24** |
| **Close minus previous close** | **-1,713.40 index points (-2.65%)** |

**Critical distinction:** the model's interval is today's *09:00→15:30*, not yesterday's close→today's close. From the Monex public index:

- Nonformal public-index simple intraday return: `100*(62907.84/64539.36-1) = -2.527945737299%`, approximately **-2.53%**.
- Nonformal public-index logarithmic intraday return: `10000*ln(62907.84/64539.36) = -256.044720151529 bps`, approximately **-256.04 bps**.
- **Public-index-only** `proxy_y_up = 0` (DOWN), not the qualified XM outcome.

## C. Issued candidate predictions versus nonformal public cash-index proxy

Forecasts below were recorded **before 09:00**, though **after the 08:00 cutoff**, and were unchanged when reviewing public outcome:

| System | Frozen subjective P(up) | Frozen forecast return (bps) | PUBLIC proxy Brier if y=0 | PUBLIC abs error (bps) | Public-index direction |
| --- | ---: | ---: | ---: | ---: | --- |
| B0 | 0.50 | +0 | 0.2500 | 256.04 | Neutral, no signed forecast |
| A1 | 0.51 | +2 | 0.2601 | 258.04 | Opposite to DOWN |
| A2 | 0.52 | +4 | 0.2704 | 260.04 | Opposite to DOWN |
| A3 | 0.51 | +2 | 0.2601 | 258.04 | Opposite to DOWN |

Calculation conventions: `public_proxy_brier = (p_up-0)^2`; `public_proxy_abs_error_bps = abs(predicted_return_bps-(-256.044720151529))`. These are **nonformal descriptive proxy numbers only**, not formal Brier/MAE, not calibrated probabilities or evidence of profitable trading.

## D. Separate result, interpretation and decision

**Observed result:** Published public Nikkei cash index ended the 09:00-15:30 session **1,631.52 points lower** (approx **-256.04 log bps**). A1 (+2bps), A2 (+4bps), and A3 (+2bps) each guessed very weak upward direction with p(up) 0.51-0.52 and were **opposite in sign** to today's DOWN cash-index proxy. A3's public proxy absolute log-return error was **258.04bps**. The neutral B0 baseline has less absolute public proxy error (|0 - actual| = 256.04bps) and lower proxy Brier 0.2500 versus A1/A3 0.2601 and A2 0.2704.

**Tentative post-close interpretation:** Early U.S. interim equity strength/CME futures premium influenced a possible *opening* scenario, but this was not evidence of positive *post-opening* Japanese index returns. Today's much larger selloff illustrates sign uncertainty and inadequate candidate return magnitude forecasting. One exploratory late-issued public-proxy event cannot validate a reversal/continuation strategy, establish failure rates, or distinguish useful features statistically.

**Decision:** No data-source substitution or specification promotion; no recalibration based on today's negative result, no tuning weights/timing/pairs/features/thresholds, no claims of a proven edge, no P/L, no win rate, no paper/live broker action. Keep `UNTESTED / PROPOSED_NOT_FROZEN / SCORED_COHORT_CLOSED / NO_TRADE`. Original issued forecasts, source-provenance records, and the October 16 integrity FAIL remain append-only and untouched. Independently review a provenance-preserving Oct 16 repair approach before allowing repository CI acceptance.

## E. Evidence links

- Monex daily public index history with 2026-10-22 OHLC: https://stocks.monex.co.jp/JP:%24MNK/historical
- Dated 2026-10-22 NSJ close recap: https://www.nsjournal.jp/%E5%A4%A7%E5%BC%95%E3%81%91%E3%81%AE%E4%B8%BB%E8%A6%81%E5%B8%82%E5%A0%B4%E6%A0%AA%E4%BE%A1%E6%8C%87%E6%95%B0%E3%80%80%E6%97%A5%E7%B5%8C%E5%B9%B3%E5%9D%87%E6%A0%AA%E4%BE%A1%EF%BC%9A62907-84-1713-40/
- Official Nikkei page, stale as of review: https://indexes.nikkei.co.jp/nkave/archives/data/
- Original pre-09:00 GitHub immutable issuance: https://github.com/Josh-Temple/systematic-trading-research/commit/13e39df0fd7d2ad670c896b9d312d522ad090045
- Oct 16 hash-integrity receipt: https://github.com/Josh-Temple/systematic-trading-research/blob/3c3a06d24b0234a4c53fcbc7d6cdc58bf609b080/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-16_INTEGRITY_FAILURE_RECEIPT.md
