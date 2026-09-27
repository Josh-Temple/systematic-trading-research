# Autonomous AI Trading Research Methods — Supplemental Prior-Art Review

Date: 2026-09-27  
Status: SUPPLEMENTAL_FOCUSED_REVIEW  
Scope: AI-assisted / autonomous quantitative research methodology  
Phase impact: Phase 1 remains closed; this review supplies additional evidence for later autonomous-research design and does not reopen the Phase 1 exit decision.

## 1. Research question

How far can an AI system be allowed to autonomously:

1. generate trading / factor hypotheses,
2. implement them,
3. choose the next experiment,
4. interpret prior experiments,
5. modify its own research procedure,

without turning adaptive search, evaluator bugs, model pretraining knowledge, or result gaming into false evidence of edge?

This review is about **research method**, not whether any public system has proven durable live-trading alpha.

No public example reviewed here establishes persistent real-money excess returns under independently audited production execution.

## 2. Evidence classes used here

- **PUBLIC_CODE_CONFIRMED** — behavior or architecture checked in public repository source.
- **PUBLIC_ISSUE_REPORTED** — concrete failure or concern documented in a public Issue; not automatically an independently reproduced fact.
- **PAPER_REPORTED** — claim or experiment described by a paper / official research page.
- **PUBLIC_CODE_NOT_LOCATED** — no matching authoritative implementation was found in the GitHub search performed for this review. This does not prove that no code exists.
- **PROJECT_INTERPRETATION** — implication drawn for systematic-trading-research.

Performance claims are not upgraded merely because code is public.

## 3. Case study — Microsoft RD-Agent / RD-Agent(Q)

Repository:

- https://github.com/microsoft/RD-Agent

Existing deep review:

- [rd-agent.md](rd-agent.md)

### FACT — adaptive research loop is real

The existing project deep review already confirms in current source that RD-Agent has an explicit loop connecting:

```text
hypothesis
→ experiment
→ deterministic Qlib execution
→ metrics
→ LLM feedback / SOTA decision / bandit state
→ later proposal
```

The important prior-art value is therefore not a demo prompt but a real adaptive research architecture.

### FACT — historical/pretraining knowledge was challenged publicly

Issue #1177:

- https://github.com/microsoft/RD-Agent/issues/1177

The issue asks whether an LLM can bring knowledge of later market history into an apparently historical experiment because the model was pretrained after that period.

The maintainer response says the agent is not given precise temporal boundaries or dataset splits and points to later out-of-sample experiments whose 2024–2025 test periods are completely or nearly after the relevant model cutoffs.

**Boundary:** this is a documented mitigation and additional test, not proof that all pretraining-derived contamination is impossible.

### FACT — the search controller itself can contain silent metric defects

Issue #1451:

- https://github.com/microsoft/RD-Agent/issues/1451

The report identifies two defects in the default quant bandit metric extraction at the reviewed commit:

1. an annualized-return metric key contains a trailing space and silently falls back to zero;
2. a field called `sharpe` is calculated as annualized return divided by drawdown, not using volatility.

Because missing metrics default silently and exceptions can collapse to empty metrics, a controller can continue operating while a material part of the intended reward vector is absent.

Status at review time: open issue.

### PROJECT_INTERPRETATION

RD-Agent strengthens three existing principles:

- adaptive-validation results are allowed to influence search; final holdout results must not;
- AI decision authority must be separated from deterministic numerical execution;
- the **controller / evaluator metric plumbing** is itself part of the scientific instrument and requires tests.

A sophisticated research loop can be scientifically wrong even when each agent interaction appears reasonable.

## 4. Case study — AlphaAgent

Paper:

- KDD 2025, DOI 10.1145/3711896.3736838
- https://arxiv.org/abs/2502.16789

Repository reviewed:

- https://github.com/RndmVariableQ/AlphaAgent

Current repository head observed during this review:

- `b42cb397025510da44355db9dcf278304321f589`

### PAPER_REPORTED — restrict generative freedom

The AlphaAgent paper combines LLM alpha generation with regularization intended to discourage:

- duplication of known factor structure,
- mismatch between hypothesis and factor expression,
- excessive expression complexity.

This is important methodologically because it does **not** treat unconstrained natural-language creativity as the objective.

### PUBLIC_CODE_CONFIRMED — current implementation has evolved

The current public repository is no longer merely a frozen paper implementation. It contains a factor DSL, FactorZoo, optional LLM mining, data pipelines, and factor-similarity machinery.

For example, current `alphaagent/factor/zoo/similarity.py` computes candidate similarity to existing factors by mean daily cross-sectional Pearson correlation.

This differs from treating source-code syntax alone as novelty.

### LIMITATION

The current repository has evolved after the KDD paper, so a current-code observation should not be retroactively attributed to the exact 2025 experiment.

No independent live-trading validation was established by this review.

### PROJECT_INTERPRETATION

A useful starting search space for autonomous trading research is likely:

```text
bounded observable inputs
+ explicit operators / DSL
+ temporal rules
+ structural / behavioral duplicate checks
```

rather than arbitrary Python strategy generation.

This reduces the number of ways an agent can accidentally create hidden state, future access, or unreviewable complexity.

## 5. Case study — QuantaAlpha

Paper:

- https://arxiv.org/abs/2602.07085

Repository:

- https://github.com/signalprime/quantaalpha

Current repository head observed during this review:

- `1074ec27d6c11559e0dd2fa6da04f7f6163b7a3f`

### PAPER_REPORTED / PUBLIC_CODE_CONFIRMED — trajectory-level search

QuantaAlpha treats an end-to-end research attempt as a trajectory and supports:

- diversified initialization,
- mutation,
- crossover,
- reuse of stronger trajectory segments,
- structured factor constraints.

The public trajectory code persists prior trajectories and can select parents for mutation or crossover.

### PUBLIC_CODE_CONFIRMED — deterministic factor guardrails exist

Current `FactorRegulator` checks factor expressions for:

- parsability,
- duplicated subtree size,
- free-argument / variable ratios,
- expression symbol length,
- number of base features.

This is a useful example of putting deterministic constraints around an LLM-generated search space.

### LIMITATION — architecture evidence is stronger than performance evidence

AutoScientist-Quant later identifies evaluation leakage problems in reused agentic quant evaluation infrastructure and explicitly separates feedback data from final held-out test data.

Therefore QuantaAlpha is useful prior art for **search architecture**, but its headline backtest results should not be treated here as independent proof that the search procedure reliably discovers live edge.

## 6. Case study — AutoScientist-Quant

Official research page:

- https://research.google/pubs/autoscientist-quant-self-evolving-coding-agents-for-automatic-research-in-quantitative-investment/

Paper:

- https://arxiv.org/abs/2608.28632

GitHub status in this review:

- **PUBLIC_CODE_NOT_LOCATED** in the GitHub searches performed on 2026-09-27.

### PAPER_REPORTED — research direction itself is adaptive

The controller can choose among actions such as:

- improve a prior line,
- combine lines,
- pivot to a new direction,
- stop,

and also choose the parent research node and how much candidate-generation budget to spend.

This moves autonomy above individual factor generation and into research allocation.

### PAPER_REPORTED — feedback and final test are explicitly separated

The paper defines an adaptive feedback window and a disjoint held-out test window.

The final candidate/library is selected without observing final test performance; the held-out test is evaluated after search.

### PAPER_REPORTED — two lookahead defects were found in inherited evaluation code

The paper reports correcting two defects in reused evaluation infrastructure before final evaluation:

1. information metrics used a wider/full-sample span instead of the declared evaluation segment;
2. a failed segment filter could cause evaluation over the wrong span.

This is one of the strongest lessons from the reviewed systems:

```text
mature evaluation code
!=
correct evaluation code
```

### PROJECT_INTERPRETATION

The controller may be adaptive; the scientific boundary around it should not be.

An autonomous controller can choose research actions only inside a frozen envelope that determines:

- what information it may see,
- what it may edit,
- budget / trial accounting,
- evaluator identity,
- final-holdout access,
- promotion authority.

## 7. Case study — STAR Analyst

Paper / preprint source:

- SSRN: STAR Analyst: Self-Tuning Alpha Research
- written May 2026, posted June 2026

GitHub status in this review:

- **PUBLIC_CODE_NOT_LOCATED** in the GitHub searches performed on 2026-09-27.

### PAPER_REPORTED — the research scaffold can itself evolve

STAR moves the editable object beyond a factor or strategy. A metacognitive layer can revise the research scaffold used by the alpha researcher.

The reported design keeps evaluation data and host-side evaluation outside the researcher's ordinary control.

### LIMITATION

Without an authoritative public implementation located in this review, the exact permission boundary could not be independently audited from code.

This case therefore has lower implementation-verification strength than RD-Agent, AlphaAgent, QuantaAlpha, or autoresearch.

### PROJECT_INTERPRETATION

Self-improvement of the research procedure is plausible, but should be introduced only after the system has a trusted evaluator and explicit editable-surface boundary.

The agent must not simultaneously be allowed to rewrite:

- search policy,
- evaluator,
- final data access,
- and scientific promotion rules.

## 8. Case study — Karpathy autoresearch

Repository:

- https://github.com/karpathy/autoresearch

Current head observed during this review:

- `228791fb499afffb54b46200aca536f79142f117`

### PUBLIC_CODE_CONFIRMED — unusually small autonomous loop

The default design deliberately has three main surfaces:

- `prepare.py` — fixed data/evaluation utilities;
- `train.py` — agent-editable experiment code;
- `program.md` — human-editable research instructions.

The agent repeatedly edits `train.py`, runs a fixed-time experiment, checks one validation metric, keeps improvements, and resets regressions.

This is a strong example of reducing the edit surface instead of building a large agent organization first.

### PUBLIC_ISSUE_REPORTED — a prose-only read-only boundary is insufficient

Issue #599:

- https://github.com/karpathy/autoresearch/issues/599

The reporter gives a concrete reproducer showing that an agent controlling `train.py` can make the reported validation metric improve without genuinely improving the model.

Reported routes include:

- bypassing real optimizer work;
- short-circuiting or replacing the call to the fixed evaluator;
- lack of evaluation-data fingerprinting;
- a printed metric not being causally bound to code/data/model state.

The important point is not malicious intent. An optimizer that is allowed to edit the path by which it is scored creates a form of Goodhart pressure even if the LLM is simply following its objective.

### PUBLIC_ISSUE_REPORTED — the metric itself can be wrong

Issue #384 reports a byte-counting defect in the core BPB evaluation path that could make scores artificially better for some token representations.

This is independent of agent gaming: the fixed evaluator can simply be wrong.

### PROJECT_INTERPRETATION

For autonomous trading research:

```text
"agent may not edit evaluator.py"
```

is weaker than:

```text
trusted host process
launches evaluator
against immutable/fingerprinted candidate + data
and records a structured result receipt
```

The agent should not control the command path that defines what was actually evaluated.

## 9. Case study — The Validation Bottleneck

Repository:

- https://github.com/bwuebben/validation-bottleneck

Current head observed during this review:

- `e5e39bf8536cccec78b59cb1dd6e39b2ca4ef8f4`

Working paper:

- *The Validation Bottleneck: Alpha Discovery When Hypotheses Are Free* (2026)

### PUBLIC_CODE_CONFIRMED — preregistration is represented by repository history

The repository contains:

- raw generation corpora,
- prompts,
- call metadata,
- content hashes,
- analysis specifications,
- frozen model-specific evaluation walls,
- evaluation code,
- derived results,
- integrity / number-checking scripts.

The stated sequence is:

```text
generation corpus archived
→ model evaluation walls frozen
→ analysis specification committed
→ outcome performance inspected
```

This is materially stronger evidence than a document that merely says the analysis was preregistered.

### PAPER_REPORTED / PUBLIC_CODE_CONFIRMED — model pretraining creates a different leakage boundary

Experiment 1 tests models asked to roleplay historical dates and finds that a substantial fraction of supposedly novel proposals match predictors already present in later literature.

The core methodological warning is:

```text
historical market data cutoff
!=
historical researcher knowledge cutoff
```

For LLM-generated ideas, a backtest ending in 2010 is not automatically a clean 2010-style discovery experiment if the model was trained years later.

### PUBLIC_CODE_CONFIRMED — trial count can be made enumerable

Experiment 2 constrains candidate generation to a known grammar, making the candidate universe / attempted trial count explicitly auditable.

The paper then applies multiple-testing control and compares machine-selected candidates to random draws from the same grammar.

### PUBLIC_CODE_CONFIRMED — verification machinery found publication errors

The repository's number-checking workflow was introduced/used after cold reviews found arithmetic/reporting errors, including a wrong count and a mislabeled regression statistic.

This is a useful negative result about research operations:

```text
careful researcher
+ reproducible code
!=
error-free paper
```

Independent recomputation remains useful even late in the process.

### LIMITATION

This is a 2026 working paper, not treated here as independently replicated or as final peer-reviewed consensus.

Some full Experiment 2 rescoring requires external public factor data.

## 10. Cross-case findings

### F1. Autonomous hypothesis generation is no longer the hard part

Across RD-Agent, AlphaAgent, QuantaAlpha, AutoScientist-Quant, STAR, and autoresearch, the technical pattern for repeated generation / implementation / evaluation is now well established.

The difficult boundary is whether the resulting evidence remains scientifically interpretable after many adaptive trials.

### F2. The evaluator must be outside the agent's effective write authority

Strengthened by:

- autoresearch Issue #599,
- autoresearch evaluator bug reports,
- RD-Agent reward-extraction Issue #1451,
- AutoScientist-Quant's reported lookahead repairs,
- existing DVC provenance findings in this project.

A trustworthy architecture should distinguish:

```text
researcher process
candidate artifact
trusted evaluator process
evaluation data
result receipt
scientific promotion gate
```

not merely `AI code` versus `Python code`.

### F3. Evaluator correctness is a separate research object

Evaluator code needs:

- version identity,
- tests,
- known guarantee boundary,
- known blind spots,
- correction / invalidation links.

If an evaluator defect is later discovered, child results may need to become `INVALID`, `PARTIAL`, or `UNVERIFIED` without rewriting their historical existence.

### F4. Agent visibility is a scientific permission

The current project principle that final holdout must not feed adaptive search is strongly supported.

For a future autonomous loop, every data/result surface should have an operational answer to:

- may the agent read this?
- may this result affect the next proposal?
- may this result affect the research policy?
- may the agent request reruns?

### F5. LLM training cutoff adds a boundary not captured by ordinary holdout metadata

Ordinary temporal backtesting prevents market-data future leakage.

It does not prevent the LLM from knowing:

- later papers,
- famous anomalies,
- historical events,
- later-developed factor families.

Therefore autonomous **discovery novelty** and trading **predictive validation** are different claims.

Strong evidence of predictive validity should prefer:

- post-model-cutoff data where available,
- genuinely prospective observation,
- or models/vintages with an auditable knowledge cutoff.

Historical samples can still be useful for development and mechanism study; their role must be described correctly.

### F6. Trial accounting becomes more important as generation becomes cheaper

If an AI creates hundreds or thousands of candidates, selection itself becomes the experiment.

Record at minimum:

- generated candidate count,
- executed candidate count,
- failed / invalid candidate count,
- family / search-space membership,
- feedback seen before each generation,
- selection rule,
- stopping rule.

Do not preserve only the winning lineage.

### F7. Structured search should precede free-form strategy coding

AlphaAgent / QuantaAlpha show the benefit of explicit expression structures and deterministic guardrails.

For the first autonomous trading-search pilot, a bounded DSL / declarative strategy specification is easier to audit than unrestricted Python.

Free-form code generation can still be used to implement a frozen declarative candidate behind trusted tests.

### F8. Search memory should preserve failures and near-misses without turning them into evidence

Trajectory memory can reduce duplicate work.

However, stored failed/partial results must carry status so that retrieval does not convert:

- failed execution,
- invalid evidence,
- scientific rejection,
- exploratory near-miss

into one undifferentiated optimization signal.

### F9. The research policy can eventually become editable, but only under a frozen meta-boundary

STAR / AutoScientist / autoresearch point toward humans editing the research instructions rather than individual strategies.

That direction is plausible, but the system should first freeze what the research agent **cannot** change:

- evaluator,
- final holdout,
- evidence status semantics,
- maximum authority,
- execution / capital risk controls.

## 11. Suggested progression for systematic-trading-research

This is a method-development sequence, not a new schema.

### Stage 1 — AI implementation assistant

Human fixes:

- research question,
- specification,
- sample,
- evaluation.

AI writes / repairs implementation.

Trusted code runs the experiment.

### Stage 2 — AI candidate generator inside a fixed search space

Human fixes:

- mechanism family,
- available features,
- operators,
- temporal semantics,
- adaptive-validation dataset,
- budget,
- promotion rule.

AI generates candidates.

Every candidate is logged, not only survivors.

### Stage 3 — AI chooses the next experiment

AI can use prior **adaptive-validation** results to decide:

- refine,
- combine,
- pivot,
- stop.

Final holdout remains inaccessible.

### Stage 4 — bounded self-improvement of research policy

AI may revise an explicitly editable research-policy artifact.

It still cannot alter:

- evaluator,
- final data,
- evidence-status definitions,
- live risk controls.

### Stage 5 — prospective / live shadow

Frozen survivors run on data that was not available during search.

No capital allocation is required for this stage.

### Stage 6 — separately governed execution

Only after research validity, execution semantics, costs, operational reliability, and risk rules have their own evidence should deterministic order execution be considered.

Research-agent autonomy does not automatically grant trading authority.

## 12. Fit with current systematic-trading-research

No immediate schema change is justified by this review.

Knowledge Base v0.1 already has key fields / concepts for:

- dataset scientific role,
- `may_influence_future_search`,
- final vs consumed holdout,
- separate Run / Result / Interpretation / Decision,
- provenance guarantee scope,
- diagnostic guarantee boundaries.

The main new evidence is **operational**, not ontological:

1. a future agent runner must enforce information visibility, not merely document it;
2. the evaluator should run outside the agent's editable process;
3. candidate/evaluator/data/result identities should be bound into a run receipt;
4. model knowledge cutoff should be recorded when autonomous novelty/discovery claims depend on it;
5. adaptive candidate/trial count should be recorded at the search-controller level.

These should be tested in a future autonomous-research pilot before changing the canonical v0.1 schema.

## 13. What not to conclude

This review does **not** establish that:

- any reviewed public project has durable live-trading alpha;
- LLM-generated factors outperform human research prospectively;
- multi-agent systems are intrinsically better than one well-scoped agent;
- more autonomous search should be enabled before evaluation integrity is solved;
- a good backtest plus public code is evidence of production profitability;
- post-cutoff validation eliminates all forms of selection bias or regime dependence.

## 14. Practical implication

The credible near-term target is not:

```text
AI directly trades autonomously
```

but:

```text
human defines research mandate / risk boundary
→ AI explores and implements inside a bounded search space
→ trusted evaluator computes evidence
→ AI receives only permitted adaptive feedback
→ final holdout / prospective evidence remains isolated
→ deterministic systems handle any later execution and risk enforcement
```

The expected human contribution moves upward from individual entry decisions toward:

- choosing research domains,
- defining acceptable evidence,
- deciding capital/risk limits,
- deciding when a research line deserves confirmation or abandonment.

That is consistent with the public methods reviewed here, while avoiding the stronger claim that the human becomes scientifically unnecessary.

## 15. Sources reviewed

### Existing project evidence

- `research/prior-art/SYNTHESIS_V0.2.md`
- `research/prior-art/rd-agent.md`
- `research/prior-art/freqtrade.md`
- `research/prior-art/dvc.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `docs/KNOWLEDGE_BASE_V0.1.md`

### External primary / near-primary sources

- Microsoft RD-Agent repository, Issue #1177, Issue #1451
- RndmVariableQ/AlphaAgent repository and KDD 2025 paper
- signalprime/quantaalpha repository and arXiv 2602.07085
- Google Research AutoScientist-Quant page and arXiv 2608.28632
- STAR Analyst SSRN preprint
- karpathy/autoresearch repository, Issue #599, Issue #384
- bwuebben/validation-bottleneck repository and bundled 2026 working paper

## Review status

**SUPPLEMENTAL / PARTIAL**

Strongest evidence:

- public-code confirmation of multiple autonomous/adaptive research loops;
- concrete evaluator/controller failure reports in mature public projects;
- public replication archive showing preregistration, exact trial accounting, model-cutoff controls, and post-publication correction tooling;
- AutoScientist-Quant's explicit report that inherited evaluation code contained lookahead defects.

Remaining gaps:

- independent reproduction of the major performance claims was not performed here;
- no authoritative public implementation of AutoScientist-Quant or STAR Analyst was located in the GitHub search used for this review;
- long-horizon audited live-capital performance remains unverified;
- evaluator isolation has not yet been implemented and stress-tested in systematic-trading-research.
