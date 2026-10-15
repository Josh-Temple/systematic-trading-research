---
type: ProspectiveEventPreRegistration
event_id: XPF-JP225-20261013
research_line_id: RL-JP225-PROSPECTIVE-001
registered_at: 2026-10-13T07:55:04+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
forecast_status: PENDING
---

# JP225 pre-registration — 2026-10-13

## Fixed protocol before information cutoff

- **Eligible day:** Tuesday October 13, 2026, scheduled JPX cash-equity trading day, after October 12 Sports Day holiday. Official JPX calendar: https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html
- **Information cutoff:** `2026-10-13T08:00:00+09:00` JST.
- **Intended issuance:** at or immediately after 08:00 JST; require actual `issued_at` and explicit deviation if late.
- **Target:** 09:00–15:30 JST, cash-trading-day intraday return of qualified exact XM MT5 `JP225Cash` Bid/Ask midpoint. Overnight futures gap or prior-close-to-close return is NOT the target.
- **Systems:** unchanged candidate B0 neutral, A1 target market, A2 cross-market and macro/news, A3 repository-status-added.
- **XM:** actual XM MT5 data not collected, preserving research owner's explicit deferral. All outside-source market quotes are *proxy-only*, not exact-XM inputs or formal outcomes.
- **Scientific standing:** `SPEC-JP225-FORECAST-001-v01` `PROPOSED_NOT_FROZEN`; `UNTESTED`, source `PARTIAL`, scored cohort `CLOSED`.
- **Event class:** `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT` permanently. `NO_TRADE`; neither live nor paper broker action authorized.

## Temporal and evidentiary controls

Only information demonstrably observable or published **on or before 08:00 JST on October 13** may contribute to the forecasting snapshot. Any undated, dynamically updated, after-08:00 or post-09:00 data must be excluded. Today is the first cash-equity day after Sports Day; OSE holiday futures trading on Oct 12 is permitted contextual input, *not* a cash session or scored event.

No post-event sources, previous Oct 6/8/9 exploratory outcome fitting, rules/weight/parameter changes, implicit XM substitutes, or retroactive issuance. The numerical preliminary forecast must be frozen to GitHub before 08:00, followed by actual at/after-08:00 issuance as a distinct immutable record. If issuance is late, label it and do not hide the timestamp.

Existing preflight: PR #62 open/draft at fresh read, branch initial SHA `3552c7dcfe3302a476a51510b582e6f6e2fb92e9`, current main `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`. This document itself is not an issued numerical forecast.

After 15:30, any post-close *public cash-index* comparisons must remain strictly separate from formal XM scoring. No scored 60-event eligibility is implied.
