---
id: AUDIT-FXMP-INFERENCE-20261004-01
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-04
status: PASS
execution_status: SUCCESS
evidence_validity: VALID_FOR_AUDIT_SCOPE
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


## Execution result

- workflow: `FXMP independent inference audit`
- run: `37158051423`
- audited head: `c9e9df2b346cb2c0f8e70c558d7f91bf8a994a73`
- audit correction head: `8b85c0a2ab452568aaf52e29777bd273279e6a75`
- result: **PASS**

Passed checks:
- candidate config identity: block 12, 10,000 replicates, seed 20261004, 24/24 minima;
- independent type-7 percentile oracle;
- fixed known circular-block draw;
- known synthetic primary difference and interval;
- 24/24 insufficient-evidence rule;
- empty-primary-group bootstrap fail-closed;
- static no-network/no-subprocess/pandas/numpy boundary.

No market outcome was accessed.

Recommendation: inference implementation is suitable for exact human freeze, subject to the scientific choices themselves being explicitly accepted by the human user.
