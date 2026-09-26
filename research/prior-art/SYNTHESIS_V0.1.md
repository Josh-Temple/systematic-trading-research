# Cross-Repository Synthesis v0.1

Updated: 2026-09-27

## Scope

This synthesis compares:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research
- DVC
- RD-Agent

It also uses the breadth scan only to identify open questions; candidate-scan claims are not treated as confirmed deep-review findings.

This document does **not** define the final Knowledge Base schema.

Its purpose is to separate:

- strong common principles
- plausible patterns
- conflicting design choices
- project-specific choices
- unresolved questions

before Phase 2 design.

---

## 1. Strong common principles

### P1. Current valid knowledge and historical research should be separated

Evidence:

- Trading Second Brain separates durable memory, revisable learnings, and dated decisions.
- zestoles/quant separates current binding status from historical reports and invalidated evidence.
- Epsilon separates current routing/task/canon surfaces from archives, findings, logs, and dated handoffs.
- RD-Agent retains experiment history while deriving a current SOTA from decisions.

Implication:

Historical evidence should remain available even after the current conclusion changes.

Open design question:

Whether current state should be:

- one generated projection,
- one binding current-state document,
- or a small set of domain-specific current surfaces.

---

### P2. Negative, rejected, invalidated, and failed research must remain discoverable

Evidence:

- contradictory observations and retired decisions are retained in Trading Second Brain;
- zestoles/quant preserves REJECTED / NEEDS_MORE_EVIDENCE / invalid evidence;
- Epsilon retains PARKED / HISTORICAL / CONDEMNED material;
- RD-Agent trace can retain false-decision experiment nodes.

Implication:

A research system should not be a winners-only archive.

However, scientific rejection, infrastructure failure, invalid evidence, and insufficient evidence should not share one status.

---

### P3. Research state must be staged

Repeated pattern:

```text
observation
→ hypothesis
→ specification
→ experiment
→ result
→ interpretation
→ decision
→ current knowledge
```

Not every repository implements this exact schema, but all useful examples distinguish at least some of these states.

Implication:

The Knowledge Base should prevent a post-hoc observation from silently becoming validated knowledge.

---

### P4. Provenance artifacts do not prove provenance correctness

Strongest evidence:

#### DVC

DVC 3.67.1 was independently reproduced recording the **post-edit code hash** in `dvc.lock` while the output had been produced from the **pre-edit code**.

A subsequent repro then skipped execution as unchanged.

#### zestoles/quant

Structured research records coexisted with measurement bugs and duplicated execution paths that changed scientific conclusions.

#### Epsilon

A structured canon audit did not prevent later discovery of metric mismatch and defective derived datasets.

Implication:

```text
recorded provenance
!=
causal provenance
```

A future run identity should distinguish:

- definition-time identity
- execution-start identity
- actual input/read identity where possible
- save/record-time identity
- output identity

and state which of these are actually guaranteed.

---

### P5. Knowledge correctness, evidence correctness, and computation correctness are separate

A useful decomposition emerging across the reviews:

```text
Knowledge correctness
= is the current interpretation/status represented correctly?

Evidence correctness
= are the data/artifacts genuinely the evidence claimed?

Computation correctness
= did the implementation calculate what the specification intended?
```

Examples:

- Epsilon: knowledge organization could be correct while derived evidence was defective.
- DVC: stored metadata could be internally consistent while causal lineage was wrong.
- zestoles/quant: computation bugs invalidated research conclusions.
- RD-Agent: the loop can faithfully record experiments while the evaluation boundary is scientifically contaminated.

Implication:

One generic “verified” flag is too weak.

---

### P6. Final holdout must sit outside the adaptive research loop

RD-Agent provides the strongest current evidence.

At reviewed main:

- configured Qlib test/backtest metrics are produced during iterative factor/model runs;
- those metrics enter LLM feedback and SOTA decisions;
- they are stored in trace history;
- later hypothesis generation reads that history;
- the quant bandit also reads previous result metrics directly.

Therefore the configured test period is part of adaptive search.

An open/unmerged PR proposes validation-only iterative feedback and a separate post-loop final holdout.

Implication:

A dataset becomes a final holdout by **access semantics**, not by being named `test`.

---

### P7. AI permission boundaries must include information access and decision rights

Simple architecture:

`AI reasoning vs deterministic code`

is insufficient.

RD-Agent demonstrates that deterministic backtest execution can still feed final-evaluation metrics into adaptive AI decisions.

A more useful boundary is:

```text
AI proposal
→ deterministic implementation / computation
→ adaptive validation feedback
→ scientific promotion gate
→ final holdout
→ durable decision
```

Each boundary should state:

- what data may be read,
- what state may be changed,
- whether the output may influence further search.

---

### P8. Retrieval and navigation should be derived interfaces, not evidence authority

Evidence:

- Trading Second Brain preserves original sources rather than replacing them with summaries.
- Epsilon keeps generated indexes and gbrain noncanonical/read-only.
- DVC lock/status surfaces are useful but do not prove causal lineage.
- RD-Agent trace is useful history but cannot repair evaluation contamination.

Implication:

Future Web UI / search / MCP should be projections over canonical research entities and evidence, not independent truth sources.

---

## 2. Plausible patterns worth testing

### A. Typed machine-readable experiment metadata

Supported strongly by zestoles/quant and partly by RD-Agent.

Potential entities:

- hypothesis
- experiment
- dataset
- run
- result
- interpretation
- decision

Potential benefit:

Better machine retrieval and invalidation propagation.

Risk:

Too much schema can increase maintenance burden and encourage false precision.

---

### B. Human-readable Markdown as durable narrative

Supported strongly by Trading Second Brain and Epsilon.

Potential role:

- rationale
- interpretation
- decision explanation
- research summaries
- current maps

Risk:

Manual status surfaces can drift.

Likely direction:

Use Markdown for human meaning, but attach stable IDs and typed references to machine-readable entities.

---

### C. Current state as a projection from history

RD-Agent derives SOTA from experiment + decision history.

Epsilon and zestoles use more manually curated current-state surfaces.

Potential direction:

Prefer generating what can be generated.

Keep manual interpretation only where human judgment is genuinely required.

---

### D. Separate current-state, history, and generated indexes

Likely three distinct layers:

1. canonical research history/evidence
2. current interpretation / decisions
3. generated navigation/retrieval

This pattern appears repeatedly, though implementation differs.

---

### E. Per-artifact immutability rules

The reviews do **not** support one blanket “everything append-only” rule.

Possible distinctions:

- raw source: immutable or content-addressed
- experiment specification: frozen once run starts
- run result: immutable
- correction: new object referencing old result
- decision: append new decision rather than rewrite history
- current projection: mutable / regenerable
- generated index: disposable

This should be tested in Phase 2.

---

## 3. Conflicting design choices

### Conflict 1 — strict schema vs lightweight graph

#### zestoles/quant

Stronger structured preregistration, trial budgets, fingerprints, ledgers.

#### Epsilon

Stronger flexible Markdown navigation, hubs, frontmatter, wikilinks.

#### Trading Second Brain

Simpler folder hierarchy and knowledge-promotion rules.

Provisional conclusion:

Do not choose either extreme yet.

A likely minimal hybrid is:

- a small typed core for scientific lineage,
- Markdown narratives around it,
- generated indexes over both.

---

### Conflict 2 — one current-state surface vs several

Options observed:

- one durable summary
- one binding status page
- multiple domain-specific routing surfaces
- current state derived from decisions

Provisional conclusion:

For this project, start with **one research-line current-state projection** rather than a global monolithic status file.

Do not introduce multiple domain hubs until real scale requires them.

---

### Conflict 3 — AI-controlled scientific decision vs deterministic/human gate

RD-Agent current main allows LLM-based experiment replacement.

PR #1438 proposed deterministic statistical guardrails but was not merged.

zestoles/quant uses stronger deterministic gates and human approval at critical transitions.

Provisional conclusion:

AI may recommend interpretation or next experiments.

Scientific state transitions with holdout consequences should not be controlled solely by free-form model judgment.

---

## 4. Failure patterns seen across repositories

### F1. The control exists, but its guarantee is weaker than assumed

Examples:

- DVC lockfile
- RD-Agent named test segment
- Epsilon canon classification
- “append-only” claims in zestoles/quant

Lesson:

For every control artifact, document its **guarantee boundary**.

---

### F2. Duplicate implementation paths drift

Seen directly in zestoles/quant.

Related risk in large repositories such as Epsilon.

Lesson:

Critical scientific definitions should have one executable source where practical.

---

### F3. Current status becomes stale

Seen in Epsilon and motivating current/history separation elsewhere.

Lesson:

Generated current projections are preferable when deterministic.

Manual current state needs explicit freshness checks.

---

### F4. Failure events are recorded but causal evidence is incomplete

RD-Agent current Qlib failure path can retain failure state while dropping downstream diagnostic output.

Lesson:

Failure status and failure evidence are separate requirements.

---

### F5. Correct organization creates false confidence

Epsilon provides a clear counterexample.

Lesson:

Knowledge-base hygiene audit and scientific evidence audit should be separate.

---

### F6. Reproducibility can reproduce the same bug

zestoles/quant's measurement bug and DVC lineage issue both illustrate this.

Lesson:

Re-running the same pipeline is not independent validation of the pipeline's meaning.

---

## 5. Implications for systematic-trading-research Phase 2

These are **design constraints**, not the final schema.

### Required capabilities

The v0.1 Knowledge Base should be able to represent:

1. hypothesis
2. frozen strategy / experiment specification
3. dataset identity and role
4. run identity
5. result
6. interpretation
7. decision
8. current status
9. invalidation / correction relation
10. rejected / failed / insufficient-evidence states

### Dataset role should be explicit

At minimum:

- development / training
- adaptive validation
- final holdout
- consumed holdout / historical sample

The system should record whether a result is allowed to influence later research.

### Result status should not be one-dimensional

At minimum distinguish:

- execution success/failure
- evidence validity
- scientific interpretation/status

Example:

```text
execution = SUCCESS
evidence_validity = INVALIDATED
scientific_status = SUPERSEDED
```

### Provenance should declare scope

Do not write:

`reproducible: true`

Prefer explicit fields such as:

- code identity captured?
- input snapshot captured?
- environment captured?
- output hash captured?
- concurrent mutation prevented?
- external data pinned?
- actual execution lineage independently checked?

### Current state should be derived where possible

Candidate model:

```text
immutable-ish history
→ explicit decisions / corrections
→ generated CURRENT.md / index
```

Human interpretation remains necessary, but historical experiment records should not be rewritten to match it.

### Retrieval should default to current-valid knowledge but retain history

AI search should:

- prioritize current valid decisions,
- exclude invalidated/superseded results from default answer context,
- still search rejected/failed history to detect repeated ideas.

---

## 6. What not to build yet

Do not build yet:

- MCP server
- vector database
- graph database
- complex web dashboard
- global ontology
- automated live trading
- multi-agent orchestration specific to this repository

Reason:

The five reviewed systems show that scientific semantics and failure boundaries matter more than retrieval technology at this stage.

---

## 7. What remains before Phase 2

### High-value remaining review

Freqtrade:

- what lookahead-analysis actually detects
- known blind spots
- higher-timeframe/incomplete-candle leakage
- backtest vs live parity

This tests whether “diagnostic PASS” can be safely represented in the future Knowledge Base.

### Optional after Freqtrade

Qlib or Kedro depending on the remaining gap:

- Qlib if experiment recorder / run-history structure needs comparison
- Kedro if provenance/data versioning boundaries need comparison

### Phase 1 exit proposal

Phase 1 can likely close after:

1. Freqtrade deep review
2. one short synthesis update
3. explicit decision on the minimum Phase 2 experiment lineage

No need to exhaust every candidate before prototyping.

---

## 8. Current synthesis status

**SYNTHESIS_STATUS = PROVISIONAL_V0.1**

Enough evidence exists to define design constraints.

Not enough evidence exists to freeze the final Knowledge Base schema.

The next decisive evidence target is Freqtrade's diagnostic guarantee boundary.
