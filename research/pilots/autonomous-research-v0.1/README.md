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
- HMAC-signed ledger checkpoint for exact tail/count verification when the key is protected outside researcher authority
- second evaluator implementation for cross-code-path reproduction
- Unix-user process-boundary integration test with runtime-hidden synthetic data
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

Not yet fully demonstrated here:

- strong sandbox / VM / container isolation for arbitrary adversarial researcher code; a narrower separate-Unix-UID boundary is now CI-tested
- immutable durable ledger storage; HMAC checkpoints detect tail/count mismatch only while the checkpoint/key remain separately protected
- sandboxing of arbitrary generated Python, because v0.1 deliberately does not execute arbitrary candidate code
- an independently authored/model-reviewed second evaluator; current second implementation provides implementation diversity only

These limits must remain visible. Passing this test suite is evidence about the tested invariants only.

## Relation to Horizontal Reaction

This code does not read or modify Horizontal Reaction datasets, results, specifications, or holdout status.

In particular, it does not access `DATA-HR-003`.

## Adversarial self-review

See [ADVERSARIAL_REVIEW_2026-09-27.md](ADVERSARIAL_REVIEW_2026-09-27.md) for concrete weaknesses found after the first 18-test implementation passed CI and the hardening changes that followed.

## Deterministic fuzz/property review

See [FUZZ_REVIEW_2026-09-27.md](FUZZ_REVIEW_2026-09-27.md). The current suite covers a 672-candidate declared-grammar grid, 1,000 seeded invalid mutations, and 300 valid strict-JSON round trips. It also preserves the known limitation that a self-contained local hash chain cannot detect deletion of its final suffix without an external checkpoint.

## Source-informed model red-team

See [MODEL_REDTEAM_REVIEW_2026-09-27.md](MODEL_REDTEAM_REVIEW_2026-09-27.md) and [MODEL_REDTEAM_ATTACKS_v01.json](MODEL_REDTEAM_ATTACKS_v01.json). Against the pre-fix baseline, the evidence run reproduced three uncaught failures: enum type confusion, huge-integer float conversion, and lone-surrogate receipt serialization. The repaired branch passes the 15-case model attack corpus. The corpus is explicitly NOT_INDEPENDENT.

## Process boundary and second implementation

See [BOUNDARY_REVIEW_2026-09-28.md](BOUNDARY_REVIEW_2026-09-28.md).

Current evidence includes:

- 672-candidate agreement between two separately coded evaluator implementations;
- runtime-hidden synthetic data unreadable by a researcher probe running under a separate Unix UID;
- candidate API still available while dataset-selection injection and future-outcome feature access are rejected;
- signed ledger checkpoint tests that detect the previously documented suffix-truncation condition when the key/checkpoint are protected outside researcher authority.

These are narrow engineering results. They do not establish a market edge, full sandbox security, durable immutable storage, or independent reviewer/model replication.


## Phase A exit / Phase B protocol

Phase A exit decision:

- [PHASE_A_EXIT_REVIEW_2026-09-28.md](PHASE_A_EXIT_REVIEW_2026-09-28.md)
- status: `PASS_FOR_PHASE_B_SYNTHETIC_ONLY`

Frozen Phase B protocol:

- [PHASE_B_PROTOCOL_v0.1.md](PHASE_B_PROTOCOL_v0.1.md)
- machine-readable freeze: [phase_b_protocol.json](phase_b_protocol.json)

Phase B implementation now includes:

- `phase_b_core.py` — 240-strategy space and hidden-seed STABLE / WEAKENING / BREAK synthetic worlds;
- `phase_b_search.py` — host-owned budget, round, ledger, selection, and one-shot final gate;
- `phase_b_baselines.py` — random and deterministic adaptive baselines.

No official Phase B benchmark result is recorded by these implementation tests.


## Phase B execution readiness

The frozen AI researcher contract and `RUN_MANIFEST_PHASE_B_AI_v0.1.json` are merged and CI-verified, but no official AI adaptive result has been produced.

See [PHASE_B_EXECUTION_READINESS_2026-09-28.md](PHASE_B_EXECUTION_READINESS_2026-09-28.md).

Current blocker:

```text
EXECUTION_BLOCKED_CLEAN_RESEARCHER_UNAVAILABLE
```

This is an execution-capability state, not a scientific negative result. The host-aware chat/session must not be reused as the official researcher after inspecting generator code.

## Phase B official baseline preparation

Before any official baseline result, seed-reveal timing was clarified by:

- [PHASE_B_PROTOCOL_AMENDMENT_v0.1.1.md](PHASE_B_PROTOCOL_AMENDMENT_v0.1.1.md)
- [phase_b_protocol_amendment_v0.1.1.json](phase_b_protocol_amendment_v0.1.1.json)

The hidden seed remains unrevealed until random baseline, deterministic adaptive baseline, and AI adaptive researcher are all complete for the world, unless the run family is explicitly closed without the AI method.

Official non-AI baseline execution is prepared by:

- `phase_b_official_baselines.py`
- `.github/workflows/phase-b-official-baselines.yml`

The workflow is manual-only. It separates host state (raw seeds/checkpoint key) from metric-bearing baseline results into distinct artifacts and does not print baseline metrics to workflow logs.

See [PHASE_B_OFFICIAL_RUN_STATUS.md](PHASE_B_OFFICIAL_RUN_STATUS.md).
