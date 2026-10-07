---
type: ProspectiveForecastSummary
event_id: XPF-JP225-20261008
research_line_id: RL-JP225-PROSPECTIVE-001
information_cutoff: 2026-10-08T08:00:00+09:00
pre_cutoff_assessment_at: 2026-10-08T07:55:35+09:00
issued_at: 2026-10-08T08:21:45+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# JP225 exploratory forecast — 2026-10-08

## Issuance integrity

**Late-issued:** the 07:55:35 JST pre-cutoff preliminary assessment was stored before the information cutoff; the official forecast artifacts were issued only at 2026-10-08T08:21:45+09:00, materially after 08:00. Do not describe this as an on-time 08:00 forecast. Numerical forecasts are transcribed without re-inference. No post-08:00 market, FX, news, 08:50 macro actuals or 09:00 opening prices were used.

Canonical pre-cutoff snapshot: https://github.com/Josh-Temple/systematic-trading-research/blob/542b8ac951719672ff9e356300f6b8974b8fe293/research/lines/jp225-intraday-prospective-forecast-v0.1/forecasts/2026-10-08_PRE_CUTOFF_ASSESSMENT.md

Deviations: `LATE_ISSUANCE_AFTER_0800`, `EXACT_XM_0800_INPUT_UNAVAILABLE`, `PUBLIC_NON_XM_MARKET_CONTEXT_USED_FOR_EXPLORATORY_DRY_RUN`, `PRE_CUTOFF_ASSESSMENT_TRANSCRIBED_WITHOUT_NEW_INFERENCE`.

The original assessment did not identify a model or explicitly preserve per-system invalidation conditions; model identity is marked unobserved and those lists are empty rather than supplied after cutoff. Driver/counterevidence text only restates facts and interpretation from the pre-cutoff artifact.

## Fixed forecasts

| System | P(up) | Return forecast |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 (proxy-only) | 0.46 | -6 bps |
| A2 (exploratory) | 0.42 | -12 bps |
| A3 (exploratory) | 0.44 | -8 bps |

A3: **mildly bearish / low conviction**. Action: **NO_TRADE**.

## Preserved state

- Specification: `PROPOSED_NOT_FROZEN`; scientific status: `UNTESTED`.
- Formal scored cohort: `CLOSED`; event: `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT` (permanently not scored in the future 60-event cohort).
- Exact XM source readiness: `PARTIAL`; cutoff input status: `UNAVAILABLE`.
- Public market context is a proxy-only exploratory input; no XM input or outcome substitution is authorized.

## After 15:30 JST

Retain issued forecasts unchanged. Use qualified exact XM MT5 `JP225Cash` 09:00 and 15:30 Bid/Ask midpoint quotes only. If unavailable, record `MARKET_OUTCOME_UNAVAILABLE` with null formal start/end quotes, return, y_up, and no formal Brier/MAE. Any public Nikkei comparison must be separated as `PUBLIC_PROXY_REVIEW`. Single-day results cannot change specifications, weights or thresholds. No live/paper trade.
