# Adversarial evaluator review — 2026-09-27

Status: ENGINEERING_FINDINGS_RECORDED  
Scientific effect: NONE  
Market data used: NONE  
Target: Autonomous Research Pilot v0.1 Phase A evaluator

## Purpose

After the first Phase A evaluator implementation passed 18 local tests and GitHub Actions, the implementation was reviewed from the perspective of an optimizing researcher trying to improve the reported score without improving a valid candidate.

This review is intentionally preserved because a green test suite is not evidence that the evaluator boundary is complete.

## Baseline reviewed

Main commit:

- `1be7b24939796a3369be75d5970702dc4ba41739`

CI evidence:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36323398546
- result: 18 tests / OK

## Finding A1 — raw JSON parser boundary was underspecified

### Observation

The evaluator validated Python dictionaries correctly, but the first implementation did not provide a strict raw-JSON entrypoint.

Standard Python JSON parsing can accept behaviors that are undesirable at a scientific boundary, including:

- duplicate object keys, where later values silently replace earlier values;
- non-standard `NaN` / `Infinity` constants unless explicitly rejected.

### Risk

The candidate visible to a reviewer could be textually ambiguous while the parsed object used by the evaluator has one silently selected value.

This is an evaluator-input integrity issue, not a trading result.

### Correction

Add `load_candidate_json()` with:

- duplicate-key rejection at every object level;
- explicit rejection of non-standard NaN/Infinity constants;
- normal candidate validation after parsing.

### Regression tests

- duplicate top-level key
- duplicate nested feature key
- NaN
- positive Infinity
- negative Infinity

## Finding A2 — signed zero could evade duplicate fingerprinting

### Observation

Python distinguishes the serialized forms `0.0` and `-0.0`, while they are behaviorally equivalent for the threshold comparisons used by this Phase A grammar.

The first canonical fingerprint therefore could assign different strategy fingerprints to equivalent thresholds.

### Risk

A search process could consume additional trial budget while appearing to generate distinct strategies.

At large automated-search scale, duplicate-accounting errors distort the effective number of trials and therefore the interpretation of selection pressure.

### Correction

Normalize signed zero to `0.0` during finite-number normalization before strategy fingerprinting.

### Regression test

Two candidates differing only by threshold `0.0` versus `-0.0` must share a strategy fingerprint.

## Finding A3 — public evaluator signature exposed dataset-selection authority

### Observation

The first public function was:

```python
evaluate(candidate, rows=...)
```

The current Phase A data are synthetic, so this did not expose market evidence. However, the interface expresses the wrong future authority boundary: the researcher-facing call should not choose the dataset being used for evaluation.

### Risk

If this interface were reused with adaptive-validation or final-holdout data, dataset selection could accidentally become part of researcher-controlled state.

### Correction

Split the interface:

- public `evaluate(candidate, ...)` uses the host-owned Phase A dataset;
- private/internal `_evaluate_on_rows(...)` exists for evaluator tests and future host-side orchestration.

This is an API-level guardrail only. Python naming is not a security boundary; eventual hidden-data isolation still requires process/container authority separation.

### Regression test

The public `evaluate()` signature must not contain a `rows` parameter.

## Finding A4 — ledger append semantics were not tamper-evident

### Observation

The first ledger helper opened JSONL in append mode, but an earlier line could be edited without detection.

### Risk

Trial history is part of the scientific evidence in adaptive search. Undetected deletion or modification of failed candidates would invalidate trial-count and selection-history claims.

### Correction

Each ledger record now contains:

- `previous_event_hash`
- event payload
- `event_hash`

Before appending, the existing chain is verified.

### Boundary

This detects ordinary local edits. It does not provide immutable storage.

A user with full filesystem authority can still rewrite the entire file and recompute all hashes. Stronger persistence / external anchoring remains open.

### Regression test

Modify an existing event without updating its hash; both ledger verification and the next append must fail.

## Finding A5 — transformed-feature overflow was not explicitly checked

### Observation

Dataset inputs were required to be finite, but subtracting two very large finite values can overflow to infinity.

### Risk

A derived feature could become non-finite even when each source datum passed validation.

### Correction

Require each transformed feature value to remain finite before applying the candidate threshold.

### Regression test

A lag difference of `1e308 - (-1e308)` must be rejected rather than scored.

## Hardening test result before repository CI

Local standard-library test run:

```text
Ran 25 tests
OK
```

Repository CI still must verify the committed hardening bytes.

## Interpretation

The main result of this review is methodological:

```text
green evaluator tests
!=
complete evaluator boundary
```

The first implementation passed all of its intended tests, yet a second adversarial reading still found several concrete integrity weaknesses.

This supports the prior-art lesson from OpenEvolve and related systems: stronger automated search increases the importance of repeated evaluator attack/review, not just strategy-generation capability.

## Remaining attack surface

Still not established:

- OS/process isolation of hidden datasets;
- protection against a researcher process calling private Python functions if it shares the same interpreter;
- immutable or externally anchored trial ledger;
- second independent evaluator implementation;
- model-driven red-team generation of malformed but schema-valid candidates;
- denial-of-service / resource exhaustion behavior;
- numeric behavior under very large but allowed candidate-search populations;
- statistical correctness of later adaptive-search selection.

## Decision boundary

Do not use this hardening round as permission to expose unused market evidence.

The next valid step remains evaluator-integrity testing on synthetic data.
