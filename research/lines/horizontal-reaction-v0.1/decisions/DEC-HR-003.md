---
id: DEC-HR-003
type: Decision
research_line_id: RL-HR-001
created_at: 2026-09-27
based_on:
  - SPEC-HR-003-v01
decision: WAIT_FOR_60_SESSION_MATURITY_AND_SOURCE_GATE
reason: The preregistration and latest retrieved source-preparation handoff keep the test at WAITING_FOR_MATURITY; the first 60 structurally eligible sessions and source gate are not yet frozen/passed in the retrieved sources.
effect_on_current_state:
  experiment_EXP-HR-007: WAITING_FOR_MATURITY
  dataset_DATA-HR-003: FINAL_HOLDOUT_UNCONSUMED
next_allowed_actions:
  - exact source and sample identity precheck
  - first-party M1/Tick acquisition with per-file hashes and readback
  - structural eligibility determination
  - freeze the first 60 eligible sessions before outcomes
  - prepare calculation code without outcome access
forbidden_actions:
  - compute or view touch outcomes before 60 sessions are frozen and source gate passes
  - compare CONFIRMED and UNCONFIRMED outcomes before the gate
  - calculate PRIMARY_CONTRAST before the gate
  - run or view bootstrap output before the gate
  - change the sample, event definition, confirmation rule, horizon, thresholds, or seed
relations:
  - type: derived_from
    target: SPEC-HR-003-v01
---

# Decision — hold Post-H2 outcome access

Maintain `WAITING_FOR_MATURITY` until the preregistered 60 structurally eligible sessions are frozen and the first-party source gate passes.

This is a gate-preservation decision, not a scientific result. The final preregistered classification remains unavailable because this test has no run/result yet. Do not access outcome data before both gates pass.
