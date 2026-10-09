---
type: ProspectiveForecastSummary
event_id: XPF-JP225-20261009
research_line_id: RL-JP225-PROSPECTIVE-001
pre_registered_at: 2026-10-09T07:49:42+09:00
pre_cutoff_assessment_at: 2026-10-09T07:50:37+09:00
information_cutoff: 2026-10-09T08:00:00+09:00
issued_at: 2026-10-09T12:37:25+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 exploratory forecast — 2026-10-09 — late issuance

## Integrity and temporal boundary

**This is not an on-time 08:00 forecast issuance.** This event was pre-registered before cutoff and its actual numeric candidate probabilities and return forecasts were fixed in a GitHub commit on **2026-10-09 07:51:35 JST**, but the formally issued A1/A2/A3 records were only written **after both the 08:00 cutoff and the 09:00 outcome-window start**, with `issued_at = 12:37:25 JST`.

The actual quantitative assessment content was frozen before cutoff at 07:50:37 JST. The original snapshot is [this SHA-pinned artifact](https://github.com/Josh-Temple/systematic-trading-research/blob/f1713e620c8c558cbc4726d0f6e8f899bd3f690e/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-09_PRE_CUTOFF_ASSESSMENT.md); pre-registration is `2026-10-09_PRE_REGISTRATION.md`.

**No post-08:00 news, prices, 09:00 opening, 09:00–15:30 movement or other market outcomes were used to change or re-infer the numerical forecasts or input drivers.** Only the content of that pre-cutoff preliminary assessment was transcribed, with temporal deviations and identity/hash metadata added. The formal JSONs cannot be represented as having been issued before 09:00. They remain late-issued exploratory records and shall never enter the 60-event cohort.

Explicit deviations for all A1/A2/A3 records:
- `LATE_ISSUANCE_AFTER_0800`
- `ISSUED_AFTER_0900_TARGET_START`
- `EXACT_XM_0800_INPUT_UNAVAILABLE`
- `PUBLIC_NON_XM_MARKET_CONTEXT_USED_FOR_EXPLORATORY_DRY_RUN`
- `PRE_CUTOFF_ASSESSMENT_TRANSCRIBED_WITHOUT_NEW_INFERENCE`

## Fixed B0 / A1 / A2 / A3 values

| System | Pre-cutoff P(up) | 09:00–15:30 forecast log return | Input validity |
| --- | ---: | ---: | --- |
| B0 | 0.50 | 0 bps | Neutral reference, not issued as a standalone JSON |
| A1 | **0.48** | **-4 bps** | Only public-futures proxy; not exact-XM-compliant A1 |
| A2 | **0.44** | **-10 bps** | Exploratory pre-cutoff cross-market/newspaper evidence |
| A3 | **0.46** | **-7 bps** | A2 plus state-preserving negative/unverified repository evidence |

**A3 headline: mildly bearish / low conviction.** `NO_TRADE`.

## Preserved source and scientific boundaries

- Yesterday's and previous dry-run outcomes were not used to tune probabilities, sign or forecasts.
- The Osaka Dec futures at 06:00 JST, 68,390 (-710 versus prior settlement), and U.S. prior-session tech weakness are *opening context*; the 09:00–15:30 direction is uncertain.
- Exact XM MT5 `JP225Cash` 08:00 Bid/Ask, lookbacks and outcome qualification were not collected at the research owner's direction.
- A1 is **not** a validated target-market-only XM system; it is explicitly proxy-only.
- EMA exact-XM state: `UNTESTED / WAITING_FOR_XM_STAGE1_DATA`. US-lead reversal proxy: `STOPPED / USLEAD_PROXY_NOT_SUPPORTED_2015`. Neither establishes a validated forecast edge.
- `SPEC-JP225-FORECAST-001-v01` remains `PROPOSED_NOT_FROZEN`, science `UNTESTED`, formally scored cohort `CLOSED`.
- No weights, threshold, specification, or source strategy were changed.
- No live/paper trading and no scheduled automation.

## Immutable issued JSONs and hashes

| File | Canonical SHA-256 |
| --- | --- |
| `2026-10-09_A1_forecast.json` | `9db0cfa5915e66f6a2d8e463114fa4991fd89deabca1ae0d9875db34332710e4` |
| `2026-10-09_A2_forecast.json` | `62f85bd726dc809e9c3f852aa51a1f377de35c577d43eb01ca0f011bd864e392` |
| `2026-10-09_A3_forecast.json` | `51d07bee54faaa4e3706ce9e54fe85cf24daba6ba49aba74b33bdf0f6219614c` |

For forecast issuance integrity, record-contract, filename/event match and actual JSON hashes must be verified by GitHub Actions. A failed CI must be reported, not hidden. The existing Oct 6 legacy hash mismatch remains an unrelated unresolved historical audit finding.

## After 15:30 JST

Freeze all existing forecast records. Without qualified XM `JP225Cash` 09:00/15:30 Bid/Ask quote pair, append a formal outcome-availability review with `MARKET_OUTCOME_UNAVAILABLE`, null quote/return/y_up and empty formal scores. A published Nikkei 225 open-to-close comparison may be added in a *separate* `PUBLIC_PROXY_REVIEW` only; it is not an XM substitute. No retrospective source selection, tuning or single-event rule change.
