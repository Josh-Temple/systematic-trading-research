---
type: ProspectiveEventPreRegistration
event_id: XPF-JP225-20261008
research_line_id: RL-JP225-PROSPECTIVE-001
registered_at: 2026-10-08T07:53:27+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
forecast_status: PENDING
---

# JP225 prospective dry run pre-registration — 2026-10-08

## Event timing

- information cutoff / intended issuance: 2026-10-08 08:00:00 JST
- target start: 2026-10-08 09:00:00 JST
- target end: 2026-10-08 15:30:00 JST
- reference instrument: exact XM MT5 `JP225Cash` Bid/Ask midpoint
- public cash/futures data: context only; never a formal exact-XM substitute

## Scientific status

- specification: PROPOSED_NOT_FROZEN
- scored cohort: CLOSED
- this event: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
- live/paper broker action: NOT_AUTHORIZED
- forecast systems: B0 / A1 / A2 / A3 unchanged

## Eligibility

2026-10-08 is treated as a scheduled JPX cash-equity trading day based on the official JPX October 2026 calendar.

## Cutoff discipline

Only information demonstrably available at or before 08:00 JST may influence the forecast.

The following known event occurs after cutoff and must not be used as an observed value:

- 08:50 JST Japan balance of payments / securities investment releases.

The September 15-16 FOMC minutes released at 03:00 JST on 2026-10-08 are pre-cutoff information and may be used if captured before 08:00.

## Source boundary

Exact XM 08:00 market features are expected to remain unavailable through the currently qualified route. If so, preserve the missingness and mark any public-market context as exploratory proxy input rather than exact-XM A1 evidence.

This pre-registration does not authorize retroactive reconstruction after the 08:00 cutoff.
