# Phase A implementation status

Date: 2026-09-27  
Status: PARTIAL — CORE_EVALUATOR_TESTS_IMPLEMENTED

## Scope

This record covers only the first implementation slice of Autonomous Research Pilot v0.1 Phase A.

It does not report a trading result and does not consume market data.

## Implemented invariants

The implementation candidate is designed so that:

- candidates are declarative rather than executable code;
- unknown fields are rejected;
- future-like sources are outside the grammar;
- evaluator metrics are recomputed by trusted code;
- candidate-provided performance fields are rejected;
- position magnitude is bounded;
- non-finite candidate/data/signal values are rejected;
- all-constant signals are rejected in Phase A;
- malformed signal shape is rejected;
- strategy duplicates can be identified independently of candidate ID/notes;
- candidate, evaluator, and dataset identities appear in receipts;
- evaluator failures retain `scientific_status: NOT_APPLICABLE`;
- ledger writes use append mode and canonical JSONL.

## Local pre-commit test result

Command:

```bash
python -m unittest -v
```

Observed before repository write:

```text
Ran 18 tests
OK
```

This local result is not the final repository/CI verification. GitHub Actions must run the committed bytes before this slice is marked CI-verified.

## Why status remains PARTIAL

The following Phase A questions are still open:

- can a real researcher agent, after inspecting evaluator logic, find an untested scoring exploit?
- can hidden evaluator data be isolated at the process/container boundary in the eventual runner?
- can the ledger be made tamper-evident or otherwise strongly persisted?
- does a second independent evaluator reproduce the same valid-candidate score?

Therefore:

```text
CORE UNIT TEST PASS
!=
PHASE A EXIT
```

## Next admissible work

1. run the committed unit tests in GitHub Actions;
2. inspect any CI discrepancy;
3. add an adversarial model-driven evaluator attack harness without market data;
4. only after evaluator-integrity review, consider Phase B synthetic autonomous search.
