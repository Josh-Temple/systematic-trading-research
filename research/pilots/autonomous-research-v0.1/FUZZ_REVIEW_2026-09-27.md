# Deterministic fuzz/property review — 2026-09-27

Status: CI_VERIFIED_PARTIAL_EVIDENCE  
Scientific effect: NONE  
Market data used: NONE  
Target: Autonomous Research Pilot v0.1 Phase A evaluator

## Purpose

The first two Phase A rounds used hand-written adversarial examples.

This round broadens coverage with deterministic enumeration and seeded mutation/property testing. The goal is not to claim that the evaluator is secure; it is to test whether declared invariants survive a substantially larger input set and to preserve any remaining failure boundary.

## Reviewed implementation

Branch head initially tested:

- `a2762f17593c1af789f90504ebe506b224556be2`

GitHub Actions:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36324025330
- Python 3.12
- result: `31 tests / OK`

## Test populations

### P1 — complete declared grammar grid

672 candidate combinations were generated across:

- 2 allowed sources;
- identity plus lag-difference transforms with lags 1–5;
- 2 comparison operators;
- 2 sides;
- 7 threshold values;
- 2 position sizes.

For every candidate, the test requires:

- evaluator execution completes;
- scientific status remains `NOT_APPLICABLE`;
- validity is explicitly `VALID` or `INVALID`;
- candidate/evaluator/dataset/result identities exist;
- any valid score is finite;
- active/scored counts remain internally consistent.

Some syntactically valid candidates intentionally become `INVALID` because the resulting signal is all-constant. That is an explicit Phase A validity rule, not an execution failure.

### P2 — seeded valid JSON round-trip

300 randomly generated valid grammar candidates were serialized to JSON and passed through the strict researcher-facing JSON boundary.

The test checks equivalence between strict-JSON evaluation and direct internal-object evaluation for:

- candidate hash;
- strategy fingerprint;
- validity status;
- metrics;
- result hash.

Seed:

- `20260927`

### P3 — seeded invalid mutation campaign

1,000 candidate mutations were generated across these invalidity classes:

- unknown top-level field;
- unknown feature field;
- missing required field;
- forbidden/future-like source;
- unsupported transform;
- invalid lag;
- invalid operator;
- invalid side;
- non-finite or wrong-type threshold;
- invalid position magnitude/type;
- invalid candidate ID;
- oversized note.

Required result for every mutation:

```text
execution_status = SUCCESS
validity_status = INVALID
scientific_status = NOT_APPLICABLE
metrics = {}
```

No mutation in this campaign received a valid performance score.

## Additional boundary changes

### Researcher-facing JSON evaluation entrypoint

`evaluate_json()` was added.

It:

1. strict-parses candidate JSON;
2. rejects duplicate keys and NaN/Infinity extensions;
3. validates the declarative candidate;
4. evaluates only the host-owned Phase A dataset.

This is the intended text boundary for a future researcher process.

The direct Python-dict `evaluate()` remains useful internally, but same-process Python access is not treated as a security boundary.

### Strict ledger parser

Ledger verification now rejects:

- duplicate JSON keys;
- non-standard NaN/Infinity constants;
- malformed JSON;
- broken previous-event hash links;
- changed event contents without a matching event hash.

## Negative / boundary result — suffix truncation is not detected

A deliberate test removes the final event from an otherwise valid two-event local hash chain.

The remaining one-event file still verifies successfully.

This is expected:

```text
self-contained hash chain
!=
proof that no tail was deleted
```

Detecting suffix deletion requires an external trusted checkpoint/anchor containing at least the expected event count and/or last event hash.

The test suite preserves this behavior explicitly rather than implying that the current ledger is immutable.

## Interpretation

This round strengthens confidence in the following narrow claims:

- the declared candidate grammar behaves consistently over its enumerated grid;
- a large seeded set of malformed candidates is rejected before scoring;
- strict JSON and direct-object paths agree for generated valid candidates;
- current score outputs remain finite on the tested grammar/data;
- local ledger edits covered by the chain are detected.

It does not establish:

- process/container isolation;
- protection from a researcher with host filesystem authority;
- immutable ledger persistence;
- robustness to every possible parser/runtime edge case;
- correctness of any later financial metric;
- absence of adaptive-search overfitting;
- safety of exposing market holdout data.

## Next evaluator-integrity questions

Before Phase B, the highest-value remaining checks are:

1. generate an explicit model-driven attack corpus after showing the evaluator contract/source;
2. test a host/researcher process boundary in which the researcher cannot read hidden data or call host-private evaluation functions;
3. add an external ledger checkpoint or clearly defer it with a stronger persistence design;
4. reproduce a sample of evaluator results with an independent implementation.

Phase A remains PARTIAL.
