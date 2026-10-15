---
type: ProspectiveProtocolAmendment
event_id: XPF-JP225-20261006
research_line_id: RL-JP225-PROSPECTIVE-001
decision_observed_at: 2026-10-06T07:38:00+09:00
implementation_session_observed_at: 2026-10-06T08:12:32+09:00
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
---

# 2026-10-06 timing amendment — 08:00 forecast cutoff

## Reason

The human operator stated that reliably issuing instructions after the workday starts is difficult and requested an 08:00 workflow instead.

This is an operational change made before any JP225 forecast had been issued and while the candidate specification remained `PROPOSED_NOT_FROZEN`.

## Amended timing

- forecast information cutoff / intended issuance: 08:00:00 JST
- target start: 09:00:00 JST
- target end: 15:30:00 JST
- target definition remains the exact-XM `JP225Cash` 09:00→15:30 midpoint move

The forecast time and the target-start time are intentionally different.

## 2026-10-06 handling

The human timing decision was made before 08:00 JST. Repository implementation was not completed until after 08:00 JST.

Therefore:

- no forecast for 2026-10-06 may be represented as having been issued at 08:00;
- a forecast issued after implementation may still be preserved as a workflow dry run;
- it must declare `LATE_ISSUANCE_AFTER_0800`;
- it remains `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`;
- it can never be promoted into the future 60-event scored cohort;
- only information demonstrably available at or before 08:00 may be used despite the later issuance time.

## Preservation of prior record

The original `2026-10-06_PRE_REGISTRATION.md` is intentionally not overwritten. It remains evidence of the earlier 09:00-cutoff candidate and this file records the subsequent pre-freeze amendment.
