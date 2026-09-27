# Phase A boundary and second-implementation review — 2026-09-28

Status: CI_VERIFIED_PARTIAL_EVIDENCE  
Scientific effect: NONE  
Market data used: NONE  
Target: Autonomous Research Pilot v0.1 Phase A

## Purpose

This round addresses three remaining evaluator-integrity questions without exposing market data:

1. can a second code path reproduce primary-evaluator results?
2. can a researcher process be separated from runtime-hidden evaluator data?
3. can the known hash-chain suffix-truncation limitation be detected when an externally protected checkpoint exists?

None of these checks tests a trading hypothesis.

## Starting point

Fresh-read main before this work:

- `ef73fc5941d54c6d65e4408b838c327d7dafe800`

At that point, Phase A already included:

- strict candidate parsing and finite-value hardening;
- deterministic fuzz/property tests;
- a source-informed model red-team corpus;
- three reproduced-and-fixed model-red-team failures;
- 35-test CI evidence.

## B1 — second evaluator implementation

Added:

- `independent_evaluator.py`
- `test_independent_evaluator.py`

The second implementation does **not** import `evaluator.py`.

It separately implements:

- candidate normalization;
- grammar checks;
- dataset checks;
- identity / lag-difference feature calculation;
- threshold comparison;
- bounded position generation;
- constant-signal rejection;
- mean-return, active-count, and scored-observation calculation.

### Reproduction test

The full 672-candidate declared grammar grid is evaluated by both implementations.

For each candidate, the test requires:

- matching validity status;
- matching active count;
- matching scored-observation count;
- mean-return agreement within absolute tolerance `1e-15` for valid candidates.

Selected invalid candidates are also required to be invalid in both implementations.

### Result

GitHub Actions run:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36329864992

The combined suite passed:

```text
Ran 43 tests
OK
```

### Independence boundary

This is **implementation diversity**, not a truly independent replication.

The second implementation was created in the same research session after the primary implementation and specification were already visible. Therefore it must not be described as:

- clean-room;
- independent-author;
- independent-model;
- independent-reviewer validation.

What it does establish is narrower:

```text
two separately coded evaluator paths
agree across the enumerated Phase A grammar
on the current synthetic dataset
```

A genuinely independent implementation remains open.

## B2 — researcher/host process boundary

Added:

- `boundary_host.py`
- `researcher_probe.py`
- `run_process_boundary_test.sh`
- CI execution in `.github/workflows/autonomous-pilot-phase-a.yml`

### Test structure

At GitHub Actions runtime:

1. a hidden synthetic dataset is generated dynamically;
2. the hidden file is written outside the repository working tree;
3. file permissions are set to `0600`;
4. the host evaluator runs under the normal runner account;
5. the researcher probe runs under a separate Unix UID using `sudo -u nobody`;
6. the researcher communicates with the host only through a Unix-domain socket;
7. the researcher attempts direct hidden-file access and candidate-level boundary attacks.

The hidden values are generated at run time and are not committed to the repository.

### Researcher-side checks

The researcher probe requires all of the following:

- direct read of the hidden dataset: **DENIED**
- submission of an allowed candidate through the API: **AVAILABLE**
- attempt to add a `dataset_path` selector: **REJECTED**
- attempt to use `next_return` as a feature source: **REJECTED**
- returned receipt remains `scientific_status = NOT_APPLICABLE`

Observed CI output:

```json
{
  "dataset_id": "SYNTHETIC-PHASE-A-HIDDEN-RUNTIME",
  "dataset_selection_injection": "REJECTED",
  "direct_hidden_read": "DENIED",
  "future_outcome_source": "REJECTED",
  "scientific_status": "NOT_APPLICABLE",
  "valid_candidate_api": "AVAILABLE",
  "validity_status": "VALID"
}
```

Successful boundary run:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36329764162
- head: `c6abbab4a194bf0a6ae3653fcd243cef20cce67a`

### Preserved failed runs

Two earlier CI attempts failed before the boundary probe executed successfully:

- run `36329677330`
- run `36329709767`

The cause was operational: the GitHub Actions workspace parent path was not traversable by the `nobody` user, so the probe script itself could not be opened.

This was corrected by copying only the public probe script to a traversable temporary directory. The hidden dataset remained permission-restricted.

These failures are retained as implementation/debugging evidence. They are not scientific negative results.

### Process-boundary limits

The successful test establishes only a narrow Unix file-permission/API boundary in the GitHub-hosted runner environment.

It does **not** establish:

- VM or container isolation;
- kernel-level adversarial resistance;
- protection against every `/proc`, ptrace, namespace, resource-exhaustion, or side-channel technique;
- safety of arbitrary generated executable code;
- long-running service hardening;
- live-market or broker security.

The current candidate representation remains declarative and non-executable, which materially reduces this attack surface.

## B3 — signed ledger checkpoint

The prior fuzz review intentionally demonstrated:

```text
self-contained hash chain
!=
proof that no tail was deleted
```

A valid prefix still verifies after suffix deletion.

This round adds:

- `create_ledger_checkpoint()`
- `verify_ledger_checkpoint()`
- `test_ledger_checkpoint.py`

### Checkpoint semantics

The checkpoint binds:

- checkpoint version;
- HMAC algorithm;
- exact event count;
- exact last event hash.

The checkpoint is authenticated using HMAC-SHA256 with a key that must be held outside researcher control.

Tests require:

- unchanged ledger verifies;
- suffix truncation fails checkpoint verification;
- appended tail fails checkpoint verification;
- wrong key fails;
- altered checkpoint fields fail;
- short keys are rejected.

### Assurance boundary

This is useful only if the checkpoint key and trusted checkpoint are protected outside the researcher's authority.

If an actor can rewrite the ledger **and** obtain the HMAC key or replace the trusted checkpoint, the guarantee is lost.

Therefore this feature does not by itself establish:

- immutable storage;
- durable external anchoring;
- hardware-backed signing;
- protection from the host administrator;
- persistence across infrastructure compromise.

It converts one known local-chain blind spot into a detectable condition **when a separately protected checkpoint exists**.

## Combined result

The latest branch CI run passed:

- primary evaluator tests;
- deterministic fuzz/property tests;
- source-informed model red-team tests;
- second-implementation reproduction tests;
- signed-checkpoint tests;
- Unix-user process-boundary integration test.

Run:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36329864992
- result: `43 tests / OK`

## Interpretation

Evidence now supports these narrow engineering claims:

- the current declarative evaluator is reproducible by a separately coded implementation across the enumerated grammar;
- a researcher running under a distinct Unix UID can be denied direct access to runtime-hidden synthetic data while retaining candidate-submission access;
- candidate-level dataset selection and direct future-outcome feature use are rejected by the tested host boundary;
- a separately protected HMAC checkpoint can detect the previously documented ledger suffix-truncation condition.

It still does not support:

- a market edge;
- safe use of unused market holdouts;
- full sandbox security;
- fully independent evaluator replication;
- durable immutable research history.

## Remaining Phase A questions

The highest-value unresolved items are now narrower:

1. obtain a genuinely independent evaluator/reviewer implementation or review;
2. decide how trusted ledger checkpoints should be durably persisted outside researcher authority;
3. if arbitrary generated code is ever introduced, design a substantially stronger sandbox before allowing it;
4. define an explicit Phase A exit review before Phase B starts.

Until those are resolved or explicitly deferred with rationale:

```text
PHASE A = PARTIAL
PHASE B = NOT AUTHORIZED BY THIS REVIEW
```
