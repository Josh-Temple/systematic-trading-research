---
type: PublicProxyDiagnosticReview
event_id: XPF-JP225-20261021
research_line_id: RL-JP225-PROSPECTIVE-001
reviewed_at: 2026-10-21T22:01:27.854+09:00
formal_score_status: UNAVAILABLE_EXACT_XM_NOT_RETRIEVED
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
branch_integrity_status: BLOCKED_20261016_INVALID_CANONICAL_SHA256
---

# 2026-10-21 — PUBLIC Nikkei 225 cash-index proxy diagnostic (NOT XM)

## 0. Research boundary and issuance provenance

**This is post-close nonformal public Nikkei cash-index diagnostic only, NOT the formal exact XM MT5 `JP225Cash` Bid/Ask 09:00-15:30 JST midpoint outcome.** Exact XM endpoints were not acquired by owner direction; the separate formal `2026-10-21_review.json` therefore records `MARKET_OUTCOME_UNAVAILABLE`, null start/end quotes, null return/y_up, `scores={}`. Public Nikkei OHLC must not be substituted or counted among a proposed future 60-event formal cohort.

Original A1/A2/A3 forecast files were issued in GitHub commit `8584b9fcfc312ebd896dac3da07b4cf27dddc2e9` at **08:20:14 JST**, after the strict **08:00** information cutoff but before the Japanese 09:00 cash open; their internally recorded `issued_at` time is **08:20:06.058 JST**. There was **no 08:00 preregistration or quantitative freeze**. Reports originally published before 08:00 were retrieved after 08:00 without raw 08:00 archived page bytes. The event is therefore permanently **LATE_ISSUANCE_AFTER_0800 / EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT** and must not be represented as an on-time forecast.

GitHub Actions branch CI currently FAIL due to the immutable October 16 A1/A2/A3 issuance's malformed 512-character SHA-256 fields (expected 64), documented in `2026-10-16_INTEGRITY_FAILURE_RECEIPT.md`. This event's records and new review **do not cure or waive** the integrity failure; no original issued forecast is changed.

## 1. Official after-close public cash-index facts

Primary index provider:
- https://indexes.nikkei.co.jp/nkave/archives/data/ (official 2026.10.21 daily OHLC history)
- https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261021&idx=nk225 (official 2026-10-21 session summary)
- Independent OHLC check: https://jp.investing.com/indices/japan-ni225-historical-data

| Item | Official 2026-10-21 public Nikkei 225 cash index |
| --- | ---: |
| Open at 09:00 JST | **64,885.95** |
| High at 09:29 | **65,404.63** |
| Low at 13:16 | **64,558.60** |
| Close at 15:30 JST | **64,621.24** |
| **Close minus open** | **-264.71 points** |
| Previous (Oct 20) cash close | 64,075.42 |
| **Close minus previous close** | **+545.82 points, +0.85%** |

**Crucial horizon difference:** The target comparison is *09:00→15:30*; that is negative, even though the previous-close→current-close comparison was positive. The overnight opening gap is NOT the modeled intraday outcome.

Public-index intraday simple return: `100*(64621.24/64885.95 - 1) = -0.407961970195%`, approx **-0.408%**.
Public-index proxy *log* return: `10000*ln(64621.24/64885.95) = -40.879640526608 bps`, approx **-40.88 bps**. Nonformal public-only `proxy_y_up=0`.

## 2. Original late-issued forecast vs PUBLIC proxy only

| Model | Subjective frozen P(up) | Frozen forecast return bps | Public-proxy Brier if y=0 | Public-proxy absolute log error bps | Direction |
| --- | ---: | ---: | ---: | ---: | --- |
| B0 | 0.50 | 0 | 0.2500 | 40.88 | Neutral (no directional prediction) |
| A1 | 0.52 | 3 | 0.2704 | 43.88 | Opposite to DOWN proxy |
| A2 | 0.51 | 2 | 0.2601 | 42.88 | Opposite to DOWN proxy |
| A3 | 0.51 | 2 | 0.2601 | 42.88 | Opposite to DOWN proxy |

Methods: `public_proxy_brier = (p_up-0)^2`; `public_proxy_abs_return_error_bps = abs(forecast_bps - (-40.879640526608))`. **These are nonformal descriptive numbers, not formal XM Brier/MAE**, not a tested model sample, no broker execution or P/L.

### Results

- Despite a **+545.82-point previous-close change**, after the **09:00 open** the public cash index declined **264.71 points**, or **-40.88 log bps**.
- A1 predicted +3 bps (P(up)=0.52), A2 and A3 +2 bps (P(up)=0.51). All three were opposite in sign to the observed post-opening public proxy decline.
- Single-event public proxy errors: B0 40.88 bps / Brier .2500; A1 43.88 bps / .2704; A2/A3 42.88 bps / .2601. The neutral baseline looks slightly better for this observation only, not proof of long-run skill.
- These were late forecasts lacking pre-cutoff freeze, exact-XM inputs, and qualified source snapshots; never treat as official scored cohort members.

### Interpretation and decision

The overnight Osaka futures advance and U.S. Dow recovery fit a positive *opening-gap* narrative, yet the Nikkei subsequently declined in the **09:00-15:30** interval. This illustrates why opening-gap conditions cannot be treated as proven intraday continuation signals. It does NOT validate a reversal model or justify turning parameters after seeing this outcome.

**No rule, model, timing, input, provider, or weight changes.** Preserve original JSON bytes, SHA values, timestamps, source receipts and the Oct 16 independent integrity failure. Keep `UNTESTED`, `PROPOSED_NOT_FROZEN`, `SCORED_COHORT_CLOSED`, `NO_TRADE`; exact XM source remains unavailable by standing owner deferral. Independent, append-preserving remediation of October 16 integrity issue remains the most urgent next action.

## 3. Sources and provenance

1. Official public index OHLC: https://indexes.nikkei.co.jp/nkave/archives/data/
2. Official session summary: https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20261021&idx=nk225
3. Third-party matching daily open/close: https://jp.investing.com/indices/japan-ni225-historical-data
4. Pre-open issuance immutable Git commit: https://github.com/Josh-Temple/systematic-trading-research/commit/8584b9fcfc312ebd896dac3da07b4cf27dddc2e9
5. Prior integrity negative result: https://github.com/Josh-Temple/systematic-trading-research/blob/3c3a06d24b0234a4c53fcbc7d6cdc58bf609b080/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-16_INTEGRITY_FAILURE_RECEIPT.md
