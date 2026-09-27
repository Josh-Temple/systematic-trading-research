# Handoff — Autonomous AI Trading Research Pilot

Date: 2026-09-28  
Repository: `Josh-Temple/systematic-trading-research`  
Status: PAUSED_BY_USER  
Authoritative branch: `main`  
Fresh-read main at handoff: `11e9bcdd1d1ef7189a5abed6ccaa24a22be5e39a`

## 1. Purpose of this handoff

This file records the current state of the autonomous-research investigation and pilot so a later session can continue without reconstructing decisions from chat history.

Do not treat the SHA above as current state in a future session. Fresh-read `main` first.

The autonomous-research work is only one part of the repository. After the latest autonomous-pilot commits, unrelated Horizontal Reaction H3 / Web UI / consistency-check work continued on `main`. Those later changes must not be mistaken for autonomous-pilot changes.

## 2. Original research question

The investigation started from the question of how far an AI system can autonomously perform:

- edge / hypothesis discovery;
- implementation;
- experiment selection;
- result interpretation;
- iterative search;
- eventually execution,

while the human mainly defines research direction and bears/limits capital risk.

The public-method review found that autonomous hypothesis generation and implementation are already technically plausible. The harder problem is preserving valid evidence under fast adaptive search.

The core design principle that emerged is:

```text
human defines mandate / risk / evidence boundary
→ AI explores inside a bounded research space
→ trusted evaluator computes evidence outside AI write authority
→ only permitted adaptive feedback returns to AI
→ final holdout stays isolated
→ execution/risk remain separately governed
```

No public example reviewed was treated as proof of durable independently audited live-trading alpha.

## 3. Prior-art review completed

Primary supplemental review:

- `research/prior-art/AUTONOMOUS_AI_RESEARCH_METHODS_2026.md`

Cases reviewed include:

- Microsoft RD-Agent / RD-Agent(Q);
- AlphaAgent;
- QuantaAlpha;
- AutoScientist-Quant;
- STAR Analyst;
- Karpathy autoresearch;
- OpenEvolve / AlphaEvolve;
- AIDE;
- MLE-bench;
- The Validation Bottleneck;
- established multiple-testing / backtest-overfitting methods.

Important reusable findings:

1. evaluator quality is part of the scientific instrument;
2. an optimizer will search evaluator weaknesses even without malicious intent;
3. final-holdout isolation must be enforced operationally, not only documented;
4. LLM pretraining knowledge creates a different contamination boundary from ordinary market-data lookahead;
5. all attempted trials, failures, invalids, and duplicates matter for interpretation;
6. structured/declarative search is easier to audit than unrestricted generated Python;
7. negative engineering findings must be preserved rather than rewritten away after fixes.

## 4. Autonomous Research Pilot v0.1

Design document:

- `docs/AUTONOMOUS_RESEARCH_PILOT_V0.1_DRAFT.md`

The pilot deliberately begins with synthetic engineering validation rather than market-edge search.

### Phase A objective

Test whether an autonomous researcher can exploit or bypass the evaluator before any unused market evidence is exposed.

### Phase A major implementation files

Directory:

- `research/pilots/autonomous-research-v0.1/`

Important files:

- `evaluator.py`
- `candidate.schema.json`
- `test_evaluator.py`
- `test_fuzz_properties.py`
- `MODEL_REDTEAM_ATTACKS_v01.json`
- `test_model_redteam.py`
- `independent_evaluator.py`
- `test_independent_evaluator.py`
- `boundary_host.py`
- `researcher_probe.py`
- `run_process_boundary_test.sh`
- `test_ledger_checkpoint.py`
- `PHASE_A_IMPLEMENTATION_STATUS.md`
- `PHASE_A_EXIT_REVIEW_2026-09-28.md`
- `ADVERSARIAL_REVIEW_2026-09-27.md`
- `FUZZ_REVIEW_2026-09-27.md`
- `MODEL_REDTEAM_REVIEW_2026-09-27.md`
- `BOUNDARY_REVIEW_2026-09-28.md`

## 5. Phase A preserved failure history

The Phase A result is not simply "tests passed." Several real weaknesses were found after earlier green test suites.

### First adversarial review

After the first 18-test implementation passed CI, review found:

- raw JSON duplicate-key / NaN / Infinity boundary was underspecified;
- signed zero could evade duplicate fingerprinting;
- researcher-facing evaluator signature exposed dataset-selection authority;
- local append-only ledger was not tamper-evident;
- derived lag-difference features could overflow even when source values were finite.

These were fixed and regression-tested.

### Source-informed model red-team

A 15-case source-informed GPT-5.6 Sol corpus was generated.

Important provenance boundary:

```text
NOT_INDEPENDENT
```

Historical baseline reproduction intentionally reproduced three uncaught failures:

- unhashable enum value -> `TypeError`;
- ~1,000-digit threshold -> `OverflowError`;
- lone-surrogate candidate ID -> `UnicodeEncodeError`.

A deep-nesting hypothesis did not reproduce as a new defect because the existing parser already rejected it.

The reproduced failures were fixed and preserved in:

- `MODEL_REDTEAM_REVIEW_2026-09-27.md`

### Process-boundary debugging failures

Two CI runs failed before the boundary probe could execute:

- run `36329677330`
- run `36329709767`

Cause:

- the GitHub Actions workspace parent path was not traversable by Unix user `nobody`, so the researcher probe script could not be opened.

Correction:

- copy only the public researcher probe to a traversable temporary directory;
- keep the runtime hidden dataset permission-restricted.

These are implementation/debugging failures, not scientific negative results.

## 6. Phase A final engineering evidence

PR #7:

- `Phase A: verify process boundary and second evaluator path`
- https://github.com/Josh-Temple/systematic-trading-research/pull/7
- merged: YES
- merge commit: `f6e80707511ff4fa1622a439100b3ca97b11c5ea`

Evidence included:

- two separately coded evaluator paths agree on all 672 declared grammar candidates;
- the second implementation does not import the primary evaluator;
- this is implementation diversity, **not** independent-author/model replication;
- a researcher probe under a separate Unix UID cannot directly read the runtime-hidden synthetic dataset;
- candidate submission remains available through a Unix-domain socket;
- dataset-selection injection is rejected;
- direct future-outcome feature use is rejected;
- HMAC-SHA256 ledger checkpoints detect exact tail/count mismatch when the key/checkpoint remain outside researcher authority.

Boundary CI:

- run `36329764162`: successful Unix-user hidden-data test;
- run `36329864992`: 43 tests / OK;
- main after PR #7 merge: run `36330092658`: success.

Important limitation:

- Unix UID separation is not a general VM/container/kernel security proof;
- HMAC checkpointing is not immutable storage by itself;
- arbitrary generated Python remains outside the authorized design.

## 7. Phase A exit decision

Authoritative file:

- `research/pilots/autonomous-research-v0.1/PHASE_A_EXIT_REVIEW_2026-09-28.md`

Current status in `PHASE_A_IMPLEMENTATION_STATUS.md`:

```text
EXIT_PASS — PHASE_B_SYNTHETIC_ONLY
```

Authoritative decision:

```text
PHASE A: PASS_FOR_PHASE_B_SYNTHETIC_ONLY
PHASE B IMPLEMENTATION: AUTHORIZED
PHASE B SYNTHETIC RUN: AUTHORIZED ONLY AFTER PROTOCOL FREEZE
PHASE C / MARKET DATA: NOT AUTHORIZED
LIVE / BROKER EXECUTION: NOT AUTHORIZED
```

This is an engineering gate only. It is not evidence of market alpha.

## 8. Phase B current state

Phase B core was added in commit:

- `ab44b5a91233787d263d890a71086cd53dfd06dc`
- message: `Authorize synthetic Phase B and add frozen benchmark core`

Files include:

- `PHASE_B_PROTOCOL_v0.1.md`
- `phase_b_protocol.json`
- `phase_b_core.py`
- `phase_b_baselines.py`
- `phase_b_search.py`
- `test_phase_b_core.py`
- `test_phase_b_search.py`

The Phase A workflow passed on that main state:

- run `36331002094`: success.

### Phase B protocol is already frozen

Protocol ID:

- `ARP-B-v0.1`

Status:

- `FROZEN_BEFORE_PHASE_B_RESULTS`

Market data:

- FORBIDDEN

Candidate space:

- 240 strategy fingerprints;
- 2 sources;
- identity or lag_diff(1–5);
- 2 operators;
- 5 thresholds;
- 2 sides;
- position_size fixed at 1.0.

Search budget per world/method:

- 16 submissions;
- 4 rounds;
- max 4 proposals/round;
- INVALID consumes budget;
- DUPLICATE consumes budget.

Synthetic worlds:

- STABLE × 2 hidden seeds;
- WEAKENING × 2 hidden seeds;
- BREAK × 2 hidden seeds;
- total 6 worlds;
- 512 ADAPTIVE_VALIDATION rows/world;
- 512 FINAL_SYNTHETIC_HOLDOUT rows/world.

Baselines:

- random search: 200 repetitions/world;
- deterministic adaptive baseline;
- AI adaptive researcher.

AI run requirement:

Before the first AI adaptive result, a `RUN_MANIFEST` must freeze at least:

- model/provider identity;
- system/research instruction text or immutable hash;
- candidate-space reference;
- protocol commit;
- evaluator commit;
- world IDs;
- search budget;
- feedback schema.

Final selection is host-controlled.

The researcher does not manually choose what reaches final holdout.

Final synthetic holdout is one-shot per method/world run.

## 9. Phase B result state at handoff

At the fresh-read main used for this handoff, the pilot directory contains the frozen Phase B protocol and implementation/core files.

No dedicated Phase B benchmark-result file or run-manifest file was observed in the current pilot directory.

Therefore the safe continuation assumption is:

```text
PHASE B PROTOCOL / CORE: PRESENT
OFFICIAL PHASE B BENCHMARK RESULT: NOT YET ESTABLISHED BY THIS HANDOFF
```

A future session must fresh-read the repository and verify this before acting. Do not rely on this handoff alone if newer commits exist.

## 10. Market-data boundary

The autonomous-research pilot has not authorized market-data search.

In particular:

- do not use `DATA-HR-003` for this pilot;
- do not convert Phase B synthetic evidence into a market claim;
- do not begin historical-market Phase C automatically after a successful synthetic result;
- do not add broker/live/paper execution authority.

Horizontal Reaction H3 work continued separately on `main` after the autonomous-pilot work. Keep the two research tracks conceptually separate.

## 11. Current repository context outside this pilot

Fresh-read current main at handoff:

- `11e9bcdd1d1ef7189a5abed6ccaa24a22be5e39a`

After the autonomous-pilot Phase B core commit, `main` continued with unrelated Horizontal Reaction / Web work, including:

- H3 implementation identity freeze;
- Web projection update;
- public mobile Web validation;
- Phase 4 Web exit;
- fail-closed research/Web consistency checks.

At current main, recent checks include successful:

- `Validate research and web consistency`
- `Deploy research web UI`
- `Validate public mobile web`

Do not infer autonomous-pilot changes from these later commits.

## 12. Next-session restart procedure

On restart:

1. fresh-read current `main` and record its SHA;
2. read:
   - `PHASE_A_EXIT_REVIEW_2026-09-28.md`
   - `PHASE_A_IMPLEMENTATION_STATUS.md`
   - `PHASE_B_PROTOCOL_v0.1.md`
   - `phase_b_protocol.json`
   - `phase_b_core.py`
   - `phase_b_baselines.py`
   - `phase_b_search.py`
   - Phase B tests;
3. check whether any Phase B run manifest/result has appeared since this handoff;
4. if no official Phase B result exists, do **not** modify the frozen protocol after observing adaptive results;
5. create/freeze the AI `RUN_MANIFEST` before the first AI adaptive evaluation;
6. verify the baseline/core tests on committed bytes;
7. execute synthetic-only Phase B according to `ARP-B-v0.1`;
8. preserve every INVALID, DUPLICATE, failure, and rejected branch in the host-written ledger;
9. run the final synthetic holdout only under the frozen one-shot rule;
10. write an explicit Phase B review before discussing Phase C.

If any protocol-defining field must change after adaptive feedback has been observed, create a new run family/version rather than silently changing `ARP-B-v0.1`.

## 13. Items intentionally deferred

Do not solve these by quietly broadening Phase B:

- genuinely independent evaluator/reviewer replication;
- durable external checkpoint persistence;
- arbitrary-code sandboxing;
- market-data Phase C design;
- statistical promotion rules for real-market search;
- broker/live execution.

These remain separate design/review tasks.

## 14. Stop point

User requested the work be paused and a handoff be saved.

No further autonomous-search execution should be inferred from this document.

The clean restart point is:

```text
Phase A = EXIT PASS for synthetic-only progression
Phase B protocol/core = frozen and present
Next = fresh-read main, verify no newer Phase B result,
       then freeze RUN_MANIFEST before any AI adaptive result
Market data = still closed
```
