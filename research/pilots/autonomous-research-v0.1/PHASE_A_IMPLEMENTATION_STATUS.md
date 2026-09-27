# Phase A implementation status

Date: 2026-09-27  
Status: PARTIAL — CORE_EVALUATOR_HARDENING_CI_PENDING

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

GitHub Actions subsequently ran the committed bytes successfully.

Verified run:

- workflow: `Autonomous pilot Phase A`
- run: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36323323224
- head: `461685e84491b980a171226ff5fda69e97e6a9db`
- result: `18 tests / OK`

This establishes the tested code-path invariants at that commit. It does not establish full evaluator isolation or Phase A exit.

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

## Adversarial hardening round

After the first CI pass, the evaluator was reviewed from the perspective of an optimizing researcher. Three concrete weaknesses were identified before any market-data use:

1. raw JSON duplicate keys / Python-style NaN or Infinity were not explicitly rejected at the input boundary;
2. signed zero could create different canonical fingerprints for behaviorally identical thresholds;
3. the public evaluator function accepted a dataset-row argument, which expressed more dataset-selection authority than the intended researcher interface should have.

The hardening branch also adds a hash-chained ledger check and transformed-feature overflow rejection.

Local hardening test result before repository CI:

```text
Ran 25 tests
OK
```

This section records an engineering/evaluator finding, not a trading result.
