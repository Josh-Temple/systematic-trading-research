---
id: DIAG-FXMP-IMPLEMENTATION-001
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-03
status: PASS
execution_status: SUCCESS
evidence_validity: VALID_FOR_SYNTHETIC_SCOPE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-FXMP-001-v01
  - type: derived_from
    target: DIAG-FXMP-SOURCE-001
---

# Packet D — outcome-blind policy-feature implementation

## Scope

Synthetic implementation only. No CSM price observations, pair rankings, target returns or strategy metrics are inputs.

## Implemented

- exact Decimal policy-rate differences;
- ALIGNED / NEUTRAL / OPPOSED classification;
- missing and invalid source fail-closed;
- CHF 2019-06 and EUR 2024-09 instrument-switch crossing guard;
- JP 2013-04 through 2016-09 conservative no-policy monthly guard;
- deterministic ledger ordering and canonical JSON bytes;
- event fields unrelated to the feature, including synthetic future-return fields, are ignored.

## Boundary

The implementation accepts already-selected synthetic pair identities. It does not implement or reproduce the CSM price-selection algorithm and therefore cannot access its outcomes.

The proposed three-month lookback is not encoded as a hardwired scientific search rule here. Callers supply old/new policy month labels; the final frozen specification will determine them.

CI result will be appended separately. No scientific result is produced by these tests.


## CI verification — 2026-10-03

Exact PR head tested: `9e9791676b53d70a7f01ecfac42f139f9ce803b8`.

Workflow:
- name: `FXMP outcome-blind implementation tests`
- run: `37130507077`
- result: **SUCCESS**
- synthetic tests: **12 passed / 0 failed**
- compile: PASS

The tests include:
- ALIGNED / OPPOSED / NEUTRAL classification;
- exact Decimal equality;
- missing/invalid-source fail-closed behavior;
- CHF 2019-06 instrument-switch crossing;
- EUR 2024-09 instrument-switch crossing;
- JP no-policy-rate interval;
- deterministic ledger ordering;
- future/outcome field mutation and removal producing identical feature-ledger bytes.

No FX market price, price ranking, target return, P/L or performance metric was accessed by this workflow.
