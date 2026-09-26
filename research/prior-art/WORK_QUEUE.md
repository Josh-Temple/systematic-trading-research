# Prior-Art Work Queue

Updated: 2026-09-27

## Purpose

Long-running WORK sessions are used primarily for breadth-oriented evidence gathering, repetitive inspection, and focused verification tasks that do not require changing the canonical design.

Canonical design decisions, cross-repository synthesis, and schema changes remain outside the WORK role until evidence has been reviewed.

## Current state

Deep reviews completed:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research

Breadth scan completed:

- WORK-PA-001 — 21-candidate prior-art scan
- Result: `research/prior-art/CANDIDATE_SCAN.md`
- Commit supplied by WORK: `0c99b2e3444e6bc8cbc27b64f40e62eb901ce760`

Current recommended deep-review sequence:

1. RD-Agent
2. DVC
3. Freqtrade

Suggested split:

- Separate Research session: RD-Agent deep review
- WORK: DVC focused reproducibility / lockfile review
- Later: Freqtrade deep review
- Integration / synthesis: main project session

## WORK-PA-001 — Broad prior-art candidate scout

Status: COMPLETE

### Result

21 repositories were screened.

High-priority candidates included:

- microsoft/RD-Agent
- treeverse/dvc
- freqtrade/freqtrade
- microsoft/qlib
- kedro-org/kedro
- nautechsystems/nautilus_trader
- nkaz001/hftbacktest

See `CANDIDATE_SCAN.md`.

## WORK-PA-002 — DVC reproducibility boundary review

Status: READY

### Goal

Deep-review `treeverse/dvc` as a counterexample to the assumption that a lockfile or run manifest automatically guarantees full experiment reproducibility.

The main question is:

> What does DVC actually guarantee about run identity, input identity, dependency state, and output provenance, and where do those guarantees stop?

### Required fresh reads

Before starting, fresh-read:

- `Josh-Temple/systematic-trading-research` current main
- `README.md`
- `docs/ROADMAP.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `research/prior-art/README.md`
- `research/prior-art/TEMPLATE.md`
- `research/prior-art/CANDIDATE_SCAN.md`
- completed prior-art reviews

Do not use past-chat repository state as current state.

### DVC evidence to inspect

At minimum:

- DVC pipeline / stage definition
- `dvc.lock` semantics
- dependency / output hashing
- reproducibility / rerun mechanism
- external / remote data behavior
- cache semantics
- experiment-related features if materially relevant
- Issues and PRs involving lockfile correctness, concurrent modification, stale dependencies, or mis-associated outputs
- relevant commit history and redesigns

Start from, but do not blindly accept, the candidate-scan leads:

- Issue #11058 — reported mismatch between execution-time dependency and recorded post-run hash
- Issue #11004 — frozen-stage dependency hash concerns
- older versioning / pipeline history where useful

### Verification question

Try to determine whether the following distinct properties are separately guaranteed:

1. **Definition identity**
   - Which pipeline / command / params were intended?

2. **Input-at-start identity**
   - Exactly which bytes / files / data versions were read when execution began?

3. **Code-at-start identity**
   - Which code version actually executed?

4. **Concurrent-modification safety**
   - What happens if code or dependency files change during a run?

5. **Output identity**
   - Which outputs were produced?

6. **Recorded lineage correctness**
   - Are recorded hashes guaranteed to correspond to the exact inputs that produced the outputs?

7. **External-data identity**
   - What happens when a dependency is outside Git or mutable remotely?

8. **Environment identity**
   - What is and is not captured about packages, OS, runtime, container, hardware?

Do not collapse these into a single label such as “reproducible”.

### Issue / bug handling

For every reported bug:

- distinguish reporter claim from independently confirmed behavior
- inspect maintainers' responses
- determine whether it was accepted, rejected, fixed, still open, or superseded
- identify affected versions / branches where possible
- inspect tests / fixes if merged

If feasible in the WORK environment, perform a minimal local reproduction of a key issue.

If not feasible, explicitly mark it `NOT_REPRODUCED` rather than implying confirmation.

### Comparison target

Use DVC to test these current provisional ideas:

- provenance artifact existence does not equal provenance correctness
- immutable-ish metadata does not necessarily freeze the actual runtime input set
- generated state should not automatically become canonical evidence
- reproducibility controls need explicit guarantee boundaries
- knowledge correctness, evidence correctness, and computation correctness are distinct

Do not modify those principles; only evaluate them.

### Output

Create:

`research/prior-art/dvc.md`

Use `TEMPLATE.md` as the base structure.

Add a focused section:

`Guarantee Matrix`

with rows for:

- pipeline definition
- code identity
- input identity
- external data
- environment
- output identity
- concurrent modification
- rerun
- failure recording

For each, classify:

- STRONG
- PARTIAL
- NOT GUARANTEED
- NOT VERIFIED

with evidence.

### Review status

Use:

- COMPLETE
- PARTIAL
- BLOCKED

Do not use COMPLETE if central guarantees remain based only on documentation or unverified Issue claims.

### Allowed changes

Change only:

- `research/prior-art/dvc.md`

Do not change:

- ROADMAP
- RESEARCH_PRINCIPLES
- prior-art README/index
- existing reviews
- Knowledge Base schema
- Horizontal Reaction materials

### End report

Report:

- saved path
- commit SHA
- Review status
- whether Issue #11058 was independently reproduced
- strongest confirmed DVC guarantee
- most important guarantee gap
- any finding that contradicts the current provisional principles

## Later WORK candidates

After WORK-PA-002 is reviewed:

- collect material Issues / commits for Freqtrade
- compare provenance fields across reviewed repositories
- build a failure-pattern catalogue
- test which proposed principles have independent support
- identify counterexamples to current-state/history separation
- compare DVC / DataLad / Kedro provenance boundaries

These tasks should not independently change canonical schema or scientific rules.
