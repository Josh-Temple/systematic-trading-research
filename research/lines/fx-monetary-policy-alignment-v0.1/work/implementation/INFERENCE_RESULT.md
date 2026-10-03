---
id: DIAG-FXMP-INFERENCE-001
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: PASS
execution_status: SUCCESS
evidence_validity: VALID_FOR_SYNTHETIC_SCOPE
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


## CI and independent audit

Combined feature + inference implementation CI:

- workflow: `FXMP outcome-blind implementation tests`
- run: `37157939932`
- result: **SUCCESS**
- tests: **22 passed / 0 failed**
- exact implementation head: `c9e9df2b346cb2c0f8e70c558d7f91bf8a994a73`

Independent inference audit:

- audit id: `AUDIT-FXMP-INFERENCE-20261004-01`
- audit run: `37158051423`
- result: **PASS**
- independently checked type-7 semantics, a fixed circular-block draw, known synthetic D, 24/24 insufficiency, empty-group bootstrap failure, and static no-network boundary.

No market outcome was accessed by either workflow.

The candidate configuration remains unfrozen until explicit human acceptance.
