---
id: DEC-HR-002
type: Decision
research_line_id: RL-HR-001
created_at: 2026-09-27
based_on:
  - RES-HR-006
  - INT-HR-003
decision: CLOSE_2026H2_UNCONDITIONAL_TOUCH_REPLICATION_AS_NOT_SUPPORTED
reason: The frozen primary mean and session-clustered 95% interval satisfy the preregistered NO_UNCONDITIONAL_TOUCH_SUPPORT rule.
effect_on_current_state:
  dataset_DATA-HR-002: CONSUMED_HOLDOUT
next_allowed_actions:
  - separately preregister a materially different hypothesis on another unused sample
forbidden_actions:
  - optimize confirmation delay on consumed H1/H2 samples
  - design or test a touch-entry trading strategy on consumed H1/H2 samples
  - same-sample horizon, subset, filter, or parameter search
relations:
  - type: derived_from
    target: RES-HR-006
---

# Decision — close the 2026H2 unconditional-touch replication

The completed source says to close the unconditional-touch replication line as not supported and not to optimize confirmation delay or design a touch-entry strategy on the consumed H1/H2 samples.

A materially different future hypothesis requires a separately preregistered unused sample. This decision does not assert universal absence of a touch reaction or any trading conclusion.
