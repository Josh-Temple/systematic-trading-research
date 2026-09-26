# Prior-Art Work Queue

Updated: 2026-09-27

## Purpose

Long-running WORK sessions are used primarily for breadth-oriented evidence gathering and repetitive inspection.

Canonical design decisions, cross-repository synthesis, and schema changes remain outside the WORK scout role until evidence has been reviewed.

## Current state

Deep reviews completed:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research

Next planned deep review:

- Backtrader MCP or another repository that provides stronger evidence for the AI ↔ deterministic experiment-engine boundary

## WORK-PA-001 — Broad prior-art candidate scout

Status: READY

### Goal

Find high-value GitHub repositories that can test, contradict, or extend the provisional principles emerging from the first three reviews.

Do not optimize for similarity to our current design. Seek counterexamples and mature alternatives.

### Search categories

1. systematic / quantitative trading research repositories with durable experiment history
2. research repositories with preregistration, provenance, experiment lineage, or negative-result retention
3. backtesting / experiment systems with explicit immutable run plans or reproducible run manifests
4. AI / MCP / agent interfaces over deterministic backtest or strategy-research engines
5. research knowledge bases with current-state vs history separation
6. mature research repositories with meaningful Issues / PR / Discussions showing redesign or failure history

### Candidate quality signals

Prefer repositories with several of:

- long-lived commit history
- multiple contributors
- meaningful closed Issues or PR discussion
- explicit redesign / migration history
- structured experiment metadata
- reproducibility / provenance mechanisms
- negative / rejected result retention
- documented failure cases
- active or historically substantial maintenance

### Avoid

- README-only demos
- repositories created recently with little history unless uniquely relevant
- generic trading bots with no research lifecycle
- pure execution systems unless they illuminate the AI/deterministic boundary
- repositories selected only because they resemble the provisional design

### Output

Create:

`research/prior-art/CANDIDATE_SCAN.md`

For each candidate record:

- owner/repo
- URL
- repository age / visible history
- primary relevance
- evidence available beyond README
- strongest reason to deep-review
- strongest limitation
- which current hypothesis it can test or contradict
- recommended priority: HIGH / MEDIUM / LOW

Target approximately 15–25 candidates if evidence quality permits.

Then propose the next 3 deep reviews, but do not modify the existing prior-art index, roadmap, research principles, or Knowledge Base schema.

### Required fresh reads

Before research, fresh-read:

- repository main
- docs/ROADMAP.md
- docs/RESEARCH_PRINCIPLES.md
- research/prior-art/README.md
- research/prior-art/TEMPLATE.md
- the three completed reviews

Do not use past-chat repository state as current state.

### Research boundary

Distinguish:

- FACT
- INTERPRETATION
- LIMITATION

Do not treat stars, popularity, or README claims as evidence of research quality.

Do not perform live trading, broker actions, or financial transactions.

## Later WORK candidates

After WORK-PA-001 is reviewed, suitable repetitive tasks may include:

- collecting material Issues / commits for selected deep-review candidates
- comparing provenance fields across reviewed repositories
- building a failure-pattern catalogue from prior-art reviews
- checking which proposed design principles have independent support
- identifying counterexamples to provisional principles

These tasks should not independently change canonical schema or scientific rules.
