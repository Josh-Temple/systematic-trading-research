---
id: AUDIT-FXMP-INFERENCE-20261004-01
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: PENDING_CI
execution_status: NOT_RUN
evidence_validity: NOT_APPLICABLE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: derived_from
    target: DIAG-FXMP-INFERENCE-001
---

# Independent inference audit

Exact input head under audit: `c9e9df2b346cb2c0f8e70c558d7f91bf8a994a73`.

The audit uses an independently written oracle for type-7 percentile semantics, a fixed known circular-block draw, known synthetic ALIGNED/OPPOSED differences, insufficient-evidence handling, and empty-primary-group fail-closed behavior.

No FX market outcome is accessed.
