---
id: DEC-HR-001
type: Decision
research_line_id: RL-HR-001
created_at: 2026-09-11
based_on:
  - RES-HR-001
  - INT-HR-001
decision: DO_NOT_PROMOTE_OR_RESCUE_V0_1_ON_2026H1
reason: Negative frozen execution-aware result; same-sample tuning would violate the preregistered boundary.
effect_on_current_state:
  dataset_DATA-HR-001: CONSUMED_HOLDOUT
next_allowed_actions:
  - fixed-result reproduction
  - explicit error correction
  - predefined diagnostic decomposition
  - separately frozen unused/prospective test
forbidden_actions:
  - same-sample parameter tuning
  - subset selection
  - threshold search
  - stop/target rescue
  - time-of-day rescue
relations:
  - type: derived_from
    target: RES-HR-001
---

# Decision — do not rescue v0.1 on the consumed 2026H1 sample

The frozen result does not justify further validation of v0.1 as-is on the basis of this sample.

Any follow-up strategy change must be separately frozen before accessing its evaluation outcome.

The existing 2026H1 sample remains closed for new rule selection.
