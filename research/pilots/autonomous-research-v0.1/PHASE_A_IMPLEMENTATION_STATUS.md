# Phase A implementation status

Date: 2026-09-28  
Status: PARTIAL — PROCESS_BOUNDARY_AND_SECOND_IMPLEMENTATION_CI_VERIFIED

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

The following Phase A questions remain open or only partially resolved:

- the source-informed model red-team is not independent;
- a separate-Unix-UID hidden-data boundary is demonstrated, but stronger sandbox/container/VM isolation is not;
- HMAC checkpoints detect ledger tail/count mismatch only while the key/checkpoint are separately protected; durable immutable persistence is not established;
- a second implementation reproduces the current grammar, but it was authored in the same research session and is not an independent reviewer/model replication;

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

## Hardening CI verification

Verified run:

- workflow: `Autonomous pilot Phase A`
- run: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36323723347
- head: `898c27131627765bcc166282c3fdc3d7e063b450`
- result: `25 tests / OK`

This strengthens evidence for the tested parser, identity, duplicate, numerical-finiteness, and local-ledger integrity invariants.

It does **not** change the overall Phase A status from PARTIAL. Process-level hidden-data isolation, an actual model-driven adversarial attack, stronger persistence, and independent evaluator reproduction remain open.

## Deterministic fuzz/property round

GitHub Actions run `36324025330` passed `31 tests / OK` on commit `a2762f17593c1af789f90504ebe506b224556be2`.

The expanded suite includes:

- 672 combinations from the declared candidate grammar;
- 300 seeded valid JSON round trips;
- 1,000 seeded invalid candidate mutations;
- result-hash stability checks;
- strict ledger duplicate-key / NaN rejection;
- an explicit test demonstrating that local hash-chain suffix truncation is **not** detectable without an external anchor.

See `FUZZ_REVIEW_2026-09-27.md`.

This is stronger engineering evidence, but Phase A remains PARTIAL.

## Source-informed model red-team round

A source-informed GPT-5.6 Sol attack pass generated `MODEL_REDTEAM_ATTACKS_v01.json` with 15 cases. The corpus is explicitly `NOT_INDEPENDENT`.

Historical baseline reproduction from `dd62d8b541cf95e0f5bb85faf96cfe7ab03ae449` produced an intentionally failing Actions run (`36324571918`) with three reproduced uncaught errors:

- unhashable enum value -> `TypeError`;
- ~1,000-digit threshold -> `OverflowError`;
- lone-surrogate candidate ID -> `UnicodeEncodeError` during receipt hashing.

A deep-nesting attack did **not** reproduce as a new defect; the existing parser boundary already rejected it.

After hardening, Actions run `36324471014` passed `35 tests / OK` including the 15-case model attack corpus.

See `MODEL_REDTEAM_REVIEW_2026-09-27.md`.

Phase A remains PARTIAL because process isolation, stronger ledger persistence, and independent evaluator reproduction are still open.

## Process boundary, second implementation, and checkpoint round

Starting main for this round:

- `ef73fc5941d54c6d65e4408b838c327d7dafe800`

### Second implementation

`independent_evaluator.py` implements the current Phase A grammar through a separate code path and does not import `evaluator.py`.

Cross-implementation tests compare the full 672-candidate declared grammar grid and selected invalid candidates.

Result on the combined suite:

```text
Ran 43 tests
OK
```

This is implementation diversity only. It is not clean-room or independently authored/model-reviewed validation.

### Process boundary

GitHub Actions run `36329764162` succeeded with a runtime-generated hidden synthetic dataset.

The researcher probe ran as Unix user `nobody` and observed:

- hidden dataset direct read: DENIED;
- valid candidate API: AVAILABLE;
- dataset-selection injection: REJECTED;
- future-outcome feature source: REJECTED;
- `scientific_status: NOT_APPLICABLE`.

Two preceding runs (`36329677330`, `36329709767`) failed before the probe could execute because the `nobody` user could not traverse the GitHub Actions workspace path to open the probe script. The fix copied only the public probe to a traversable temporary directory. The hidden dataset remained permission-restricted.

These are implementation/debugging failures, not scientific negative results.

### Signed ledger checkpoint

The evaluator now supports an HMAC-SHA256 checkpoint binding exact event count and last event hash.

Tests verify that:

- unchanged ledger state passes;
- suffix truncation fails checkpoint verification;
- appended tail fails;
- wrong key fails;
- tampered checkpoint fails.

This does not create immutable storage by itself. The assurance exists only if the key and trusted checkpoint remain outside researcher authority.

### Latest verified branch CI

- run: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36329864992
- result: `43 tests / OK`

See `BOUNDARY_REVIEW_2026-09-28.md`.

Phase A remains PARTIAL. Phase B is not authorized by this status record.
