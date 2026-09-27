---
id: DATA-HR-003
type: Dataset
research_line_id: RL-HR-001
created_at: 2026-09-23
provider: Dukascopy first-party historical data only
instrument: XAU/USD
time_range: 2026-07-10 onward; first 60 structurally eligible UTC trading weekdays; end date UNKNOWN pending maturity
granularity:
  signal: BID M1 UTC
  path: raw BID/ASK Tick UTC
role: FINAL_HOLDOUT
consumption_status: UNUSED
may_influence_future_search: false
identity_evidence:
  selected_session_list: NOT_FROZEN
  exact_m1_and_tick_source_identity: UNVERIFIED
  preregistration: https://docs.google.com/document/d/1GRa035N5FX3F59_wM2T11VFuv3aL85YZghmvaCeTJ0g/edit
  latest_source_preparation_handoff: https://docs.google.com/document/d/1QPwXqAcp1fzPm6VXelMLDMyist02-sSSDQ1lkrpsoSg/edit
relations: []
---

# Post-H2 prospective confirmation-selection sample

## Scientific role

This is the planned unused sample for the frozen Post-H2 confirmation-selection test. Its role is `FINAL_HOLDOUT`; it is not consumed and must not be marked consumed before outcome access.

## Sample maturity and identity

The candidate scan begins 2026-07-10 UTC and ends only when the first 60 structurally eligible UTC weekdays are frozen. The selected-session list is not yet frozen. The exact end date, raw source payloads, per-file hashes, and final source-gate status remain `UNKNOWN` / `UNVERIFIED`.

The latest retrieved source-preparation handoff (revision recorded in SPEC-HR-003-v01) states that as of 2026-09-23, 54 Monday-Friday dates had elapsed and the earliest possible maturity was 2026-10-01, conditional on the next six weekdays passing the structural gate. On the current migration date, 2026-09-27, that earliest possible date has not arrived. Structural exclusions may delay maturity further.

No touch outcomes, confirmation-group comparison, or bootstrap output were accessed or computed for this dataset during this migration.
