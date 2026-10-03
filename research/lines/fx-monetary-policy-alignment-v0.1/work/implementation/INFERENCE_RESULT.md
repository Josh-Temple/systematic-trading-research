---
id: DIAG-FXMP-INFERENCE-001
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: IMPLEMENTED_AWAITING_CI
execution_status: NOT_RUN
evidence_validity: NOT_APPLICABLE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-FXMP-001-v01
---

# Outcome-blind inference implementation

## Scope

Synthetic-only implementation of the proposed primary estimand and dependence interval.

No FX market outcome is loaded, read or calculated by these tests.

## Candidate configuration

- primary estimand: mean(y | ALIGNED) - mean(y | OPPOSED)
- full calendar-slot grid retained
- circular moving-block bootstrap
- block length: 12 calendar slots
- replicates: 10,000
- seed: 20261004
- percentile: type-7 linear, 2.5/50/97.5%
- operational minimum: 24 ALIGNED and 24 OPPOSED eligible outcomes
- any bootstrap replicate with an empty primary group: inference failure, no retry

The values remain **PROPOSED_NOT_FROZEN** until explicit human acceptance.

## Synthetic test coverage

- type-7 percentile semantics;
- exact circular-grid output length;
- constant known group difference;
- insufficient evidence rule;
- NEUTRAL/missing slot retention;
- nonfinite outcome fail-closed;
- invalid classification fail-closed;
- empty primary group fail-closed;
- deterministic result under fixed seed;
- negative D maps to NOT_SUPPORTED.

CI status is recorded after execution.
