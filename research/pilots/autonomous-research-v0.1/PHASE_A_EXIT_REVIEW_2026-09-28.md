# Autonomous Research Pilot v0.1 — Phase A Exit Review

Date: 2026-09-28  
Status: PASS_FOR_PHASE_B_SYNTHETIC_ONLY  
Scientific effect: NONE  
Market-data authorization: NONE  
Reviewed main: f6e80707511ff4fa1622a439100b3ca97b11c5ea

## 1. Decision

Phase A has met its originally stated evaluator-integrity pass conditions closely enough to permit **Phase B design, implementation, and synthetic-only execution**.

This decision does **not** authorize:

- historical market-data search;
- use of DATA-HR-003;
- any new unused/holdout market sample;
- broker connectivity;
- live or paper trading;
- arbitrary generated Python strategy execution;
- a claim that the evaluator is secure against all hostile code.

The allowed next scope is the synthetic autonomous-search benchmark described in docs/AUTONOMOUS_RESEARCH_PILOT_V0.1_DRAFT.md.

## 2. Why Phase A can exit

The Phase A draft defined six practical pass conditions.

### A1 — known-invalid candidates are rejected before legitimate scoring

Evidence:

- hand-written adversarial tests;
- deterministic declared-grammar coverage;
- 1,000 seeded invalid mutations;
- source-informed 15-case model red-team corpus;
- reproduced historical failures followed by regression fixes.

Relevant records:

- ADVERSARIAL_REVIEW_2026-09-27.md
- FUZZ_REVIEW_2026-09-27.md
- MODEL_REDTEAM_REVIEW_2026-09-27.md

Current result:

- supported within the tested declarative grammar and attack corpus.

Boundary:

- this does not prove rejection of every possible malformed input or hostile executable program.

### A2 — repeated deterministic evaluation is stable

Evidence:

- repeated-evaluation tests bind candidate, evaluator, dataset, metrics, and result hashes;
- seeded result-hash stability tests;
- second-code-path reproduction over the complete 672-candidate declared grammar.

Current result:

- supported for the current synthetic evaluator and grammar.

### A3 — researcher process cannot directly read hidden evaluation files

Evidence:

- runtime-hidden synthetic dataset;
- host process and researcher probe separated by Unix UID;
- hidden file mode 0600;
- researcher direct read: DENIED;
- candidate submission through Unix-domain socket: AVAILABLE.

Successful run:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36329764162

Current result:

- supported for the tested Unix file-permission/API boundary.

Boundary:

- this is not a VM/container/kernel security proof and does not authorize arbitrary generated code.

### A4 — candidate-reported metrics cannot improve evaluator score

Evidence:

- fabricated performance fields are outside the candidate grammar and rejected;
- evaluator recomputes all metrics from host-owned data;
- dataset-selection injection is rejected.

Current result:

- supported for the current declarative candidate interface.

### A5 — evaluator/data identity is bound to receipts

Evidence:

- evaluator identity is derived from evaluator source bytes;
- dataset identity/hash is recorded;
- dataset mutation changes dataset hash;
- result receipt includes candidate/evaluator/dataset/result identities.

Current result:

- supported for the current receipt implementation.

### A6 — evaluator failure is not scientific negative evidence

Evidence:

- evaluator/data failures produce execution_status = FAILED;
- validity remains UNVERIFIED;
- scientific_status = NOT_APPLICABLE;
- metrics remain empty.

Current result:

- supported by regression tests.

## 3. Deliberate exploitation requirement

The draft also states that Phase A succeeds only if the evaluation boundary survives deliberate attempts to exploit it.

The path was not a single green test run.

~~~text
18 tests green
→ adversarial review found concrete weaknesses
→ hardening
→ 25 tests green
→ deterministic fuzz/property expansion
→ 31 tests green
→ source-informed model red-team reproduced 3 additional failures
→ hardening
→ 35 tests green
→ second evaluator / process boundary / checkpoint work
→ 43 tests green
~~~

The important evidence is the preserved failure-and-repair history, not the test count.

Latest main CI after the boundary merge:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36330092658
- result: success

## 4. Open limitations that do not block synthetic Phase B

The following remain open, but they are not treated as Phase A exit blockers for **synthetic-only** Phase B.

### L1 — second evaluator is not independently authored

independent_evaluator.py is a separate code path and agrees with the primary evaluator across the enumerated grammar.

However, it was written in the same research session after the primary evaluator was visible.

Classification:

~~~text
IMPLEMENTATION_DIVERSITY
!=
INDEPENDENT_REPLICATION
~~~

Requirement:

- obtain stronger independent review before any market-data confirmation or claim that depends materially on evaluator correctness.

### L2 — ledger is not immutable durable storage

The local hash chain detects ordinary edits.

The HMAC checkpoint detects suffix truncation and appended tails when its key and trusted checkpoint are separately protected.

It does not create immutable storage by itself.

Requirement for Phase B:

- the host must preserve the complete search ledger and final checkpoint outside researcher write authority;
- the Phase B run must not be promoted if the ledger/checkpoint is missing or unverifiable.

A GitHub Actions artifact or later committed run packet may be used for the synthetic pilot, but its assurance scope must be stated accurately.

### L3 — arbitrary generated code is not sandboxed

The current grammar is declarative and non-executable.

This is a deliberate safety/scientific simplification.

Requirement:

- Phase B v0.1 must continue using the declarative grammar;
- adding arbitrary Python requires a new sandbox review and is outside the current authorization.

### L4 — red-team independence is limited

The source-informed model red-team was generated by GPT-5.6 Sol in the same research context.

It found useful failures, but it is explicitly not an external independent security audit.

Requirement:

- retain this limitation in Phase B reporting;
- do not infer general evaluator security from the current corpus.

## 5. Phase B launch gates

Phase B may be implemented now, but the first autonomous-search run should not begin until a Phase B protocol freezes all of the following before any adaptive result is observed:

1. synthetic-world generator and hidden-seed handling;
2. DEVELOPMENT / ADAPTIVE_VALIDATION / FINAL_SYNTHETIC_HOLDOUT roles;
3. candidate grammar version;
4. evaluator version;
5. search budget;
6. allowed feedback fields;
7. random-search baseline and any non-LLM baseline;
8. promotion/stopping rule;
9. complete search-ledger format;
10. final synthetic holdout one-shot rule;
11. model identity and prompt/instruction identity for the researcher;
12. run-failure semantics.

If any of these changes after adaptive results are observed, start a new run family rather than silently continuing the old one.

## 6. Phase B evidence classification

All Phase B results remain engineering/synthetic evidence.

Even a successful autonomous search result must be described as:

~~~text
synthetic autonomous-search benchmark result
~~~

not:

~~~text
market edge
trading alpha
validated strategy
~~~

Phase B cannot consume or redefine existing market holdouts.

## 7. Phase C remains closed

No historical market search is authorized by this Phase A exit review.

Before Phase C, the project must separately review at least:

- Phase B search behavior and failure modes;
- trial-accounting completeness;
- adaptive-to-final synthetic degradation;
- selection-bias controls;
- evaluator boundary changes made during Phase B;
- whether a new clean historical research line or already-consumed data should be used.

Horizontal Reaction DATA-HR-003 remains outside this pilot.

## 8. Exit conclusion

Decision:

~~~text
PHASE A: PASS_FOR_PHASE_B_SYNTHETIC_ONLY
PHASE B IMPLEMENTATION: AUTHORIZED
PHASE B SYNTHETIC RUN: AUTHORIZED ONLY AFTER PROTOCOL FREEZE
PHASE C / MARKET DATA: NOT AUTHORIZED
LIVE / BROKER EXECUTION: NOT AUTHORIZED
~~~

This is an engineering research gate, not a scientific claim about markets.
