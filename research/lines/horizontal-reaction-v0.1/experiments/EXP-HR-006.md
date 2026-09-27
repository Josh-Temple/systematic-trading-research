---
id: EXP-HR-006
type: Experiment
research_line_id: RL-HR-001
created_at: 2026-09-13
experiment_kind: CONFIRMATORY
tests_hypothesis: HYP-HR-002
uses_specification: SPEC-HR-002-v01
planned_dataset_uses:
  - dataset_id: DATA-HR-002
    role_at_freeze: UNUSED_EVALUATION_AT_FREEZE
relations:
  - type: tests_hypothesis
    target: HYP-HR-002
  - type: uses_specification
    target: SPEC-HR-002-v01
  - type: uses_dataset
    target: DATA-HR-002
---

# 2026H2 Unconditional Touch Replication

## Purpose

Test the explicit HYP-HR-002 on the frozen 60-session sample using the preregistered all-first-touch population and touch-to-+15-minute outcome.

## Source / status boundary

The preregistration labels this a Gold Trade Lab proposed confirmatory test. The completed source labels it confirmatory relative to that preregistration and explicitly states that Studio Lab canonical status was not modified.

Two runs are represented: an earlier fail-closed attempt before outcome computation and a later completed run after source recovery. They are not combined. The earlier blocked attempt is RUN-HR-006-ATTEMPT-1 / RES-HR-006-ATTEMPT-1; the final run is RUN-HR-006 / RES-HR-006.

## Related artifacts

- HYP-HR-002
- SPEC-HR-002-v01
- DATA-HR-002
- RUN-HR-006-ATTEMPT-1
- RES-HR-006-ATTEMPT-1
- RUN-HR-006
- RES-HR-006
- INT-HR-003
- DEC-HR-002
