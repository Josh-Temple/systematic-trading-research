# Autonomous Research Pilot v0.1 — Phase A implementation

Status: IMPLEMENTATION_CANDIDATE  
Scientific effect: NONE  
Market data: NONE

This directory implements the first narrow slice of `docs/AUTONOMOUS_RESEARCH_PILOT_V0.1_DRAFT.md`.

The purpose is to test evaluator integrity before autonomous search is allowed to inspect any unused market evidence.

## What is implemented

- declarative candidate grammar
- strict JSON input parser that rejects duplicate keys and non-standard NaN/Infinity constants
- strict rejection of unknown fields
- bounded feature/operator/lag/position choices
- finite-number checks
- dataset timestamp and finite-value validation
- deterministic signal compilation and metric recomputation
- rejection of empty/all-constant/non-finite/unbounded signals
- canonical candidate hash
- strategy fingerprint independent of candidate ID / note
- duplicate detection hook
- evaluator source identity
- dataset identity
- structured evaluation receipt
- hash-chained JSONL ledger helper with integrity verification before append
- adversarial unit tests
- deterministic grammar enumeration and seeded mutation/property tests

The evaluator does not execute candidate-supplied Python, shell commands, paths, or URLs. The public `evaluate()` entrypoint also does not accept dataset rows; dataset selection belongs to the host-side evaluator authority.

## Explicitly tested attack classes

The test suite covers:

- NaN / infinity threshold
- extreme position size
- missing required fields
- forbidden future source
- resampling / filesystem / network / code fields
- fabricated metric field
- malformed parser shape
- all-constant signal
- malformed compiled signal length
- non-finite compiled signal
- unbounded compiled signal
- invalid / duplicate timestamp ordering
- duplicate strategy under different candidate metadata
- candidate key-order canonicalization
- dataset identity mutation
- evaluator identity hashing primitive
- ledger append behavior
- failed evaluator input remaining `scientific_status: NOT_APPLICABLE`

## Run locally

From this directory:

```bash
python -m unittest -v
```

The implementation uses only the Python standard library.

## Scientific boundary

A `VALID` Phase A receipt does **not** mean that a trading hypothesis is supported.

All Phase A receipts use:

```text
scientific_status = NOT_APPLICABLE
```

because the test concerns evaluator integrity, not market edge.

`execution_status`, `validity_status`, and `scientific_status` remain distinct.

## Important limitations

This is not yet a full Phase A exit.

Not yet demonstrated here:

- OS/process-level isolation between a future researcher agent and hidden evaluator data
- immutable ledger storage; the ledger is now locally hash-chained and detects ordinary edits, but a filesystem owner can still rewrite the whole file and recompute the chain
- sandboxing of arbitrary generated Python, because v0.1 deliberately does not execute arbitrary candidate code
- adversarial testing by an actual autonomous model against the evaluator source
- independent second implementation of the evaluator

These limits must remain visible. Passing this test suite is evidence about the tested invariants only.

## Relation to Horizontal Reaction

This code does not read or modify Horizontal Reaction datasets, results, specifications, or holdout status.

In particular, it does not access `DATA-HR-003`.

## Adversarial self-review

See [ADVERSARIAL_REVIEW_2026-09-27.md](ADVERSARIAL_REVIEW_2026-09-27.md) for concrete weaknesses found after the first 18-test implementation passed CI and the hardening changes that followed.

## Deterministic fuzz/property review

See [FUZZ_REVIEW_2026-09-27.md](FUZZ_REVIEW_2026-09-27.md). The current suite covers a 672-candidate declared-grammar grid, 1,000 seeded invalid mutations, and 300 valid strict-JSON round trips. It also preserves the known limitation that a self-contained local hash chain cannot detect deletion of its final suffix without an external checkpoint.
