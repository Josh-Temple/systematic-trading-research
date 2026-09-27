# Autonomous Research Pilot v0.1 — Draft Design

Date: 2026-09-27  
Status: DRAFT_NOT_FROZEN  
Purpose: validate autonomous research mechanics before applying them to unused market evidence  
Scientific effect: NONE — this document does not consume or redefine any existing holdout

## 1. Why this pilot exists

The immediate question is not whether an AI can generate many trading strategies.

Public evidence already shows that autonomous systems can repeatedly:

- generate hypotheses or candidate programs;
- implement candidates;
- execute experiments;
- use feedback to choose later experiments;
- maintain search trees / trajectories;
- alter research direction.

The unresolved engineering/scientific question is whether this can be done without letting the search process optimize evaluator defects, leak held-out evidence, or hide the number of failed trials.

The first pilot should therefore test the **research machinery** before using it to search for a new market edge.

Primary supporting review:

- `research/prior-art/AUTONOMOUS_AI_RESEARCH_METHODS_2026.md`

## 2. Pilot objective

Demonstrate a minimal loop in which:

1. an AI proposes candidates inside a bounded search space;
2. the AI cannot directly read or change the evaluator;
3. the AI cannot directly read hidden evaluation outcomes;
4. a trusted process evaluates every candidate;
5. every attempted candidate remains in a durable search ledger;
6. invalid / failed / duplicate candidates are distinct from scientifically poor candidates;
7. adaptive feedback can guide later proposals;
8. a sealed final evaluation can be run without having influenced search.

The pilot succeeds only if the evaluation boundary survives deliberate attempts to exploit it.

## 3. Non-goals

v0.1 does not attempt to:

- find a profitable GOLD strategy;
- use DATA-HR-003 or any other unused market holdout;
- send broker orders;
- allocate capital;
- build a full multi-agent organization;
- allow arbitrary self-modification of the evaluator;
- prove that AI-generated strategies outperform human-designed strategies;
- define a new Knowledge Base schema.

## 4. Core architecture

### 4.1 Human-controlled research contract

Before a run, the human-controlled contract fixes:

- search question;
- candidate grammar / allowed fields;
- development data visible to the researcher;
- adaptive-validation data available only through evaluator feedback;
- final evaluation data hidden from the researcher;
- search budget;
- evaluation metrics;
- invalidity conditions;
- stopping conditions;
- which feedback fields may influence later search.

Changing any of these creates a new pilot version or run family.

### 4.2 Researcher

The researcher may:

- propose a candidate;
- inspect permitted prior candidates and adaptive feedback;
- decide whether to refine, combine, pivot, or stop;
- explain the intended mechanism.

The researcher may not:

- read evaluator source during a frozen run;
- read hidden evaluation data;
- change the scoring function;
- change dataset roles;
- change the search budget after observing results;
- directly mark a candidate as scientifically accepted.

### 4.3 Candidate representation

The first implementation should prefer a declarative candidate specification rather than arbitrary executable Python.

Example shape only:

```yaml
candidate_id: CAND-0001
side: LONG
features:
  - source: close
    transform: lag_return
    lag: 5
entry:
  operator: greater_than
  threshold_ref: fixed_parameter
exit:
  kind: fixed_horizon
  bars: 10
```

The exact grammar is not frozen here.

Reasons to start declaratively:

- forbidden future references can be rejected before execution;
- candidate complexity is inspectable;
- duplicate/near-duplicate search is easier;
- the candidate cannot override score calculation;
- filesystem/network access can be absent by construction;
- evaluator code remains outside the candidate artifact.

If later research requires custom Python, free-form code should be a later privilege with a stronger sandbox and evaluator contract.

### 4.4 Trusted evaluator

The evaluator is a separate deterministic process controlled by the host, not by the researcher.

It:

- receives a candidate artifact;
- validates schema and allowed operators;
- compiles/interprets the candidate;
- loads evaluation data itself;
- computes signals and outcomes itself;
- applies cost/execution rules itself;
- recomputes metrics itself;
- rejects non-finite or structurally invalid outputs;
- returns only the feedback allowed for the current data role.

It never accepts a candidate-reported performance number as evidence.

### 4.5 Search ledger

Every proposal gets a record, including:

- candidate ID;
- parent candidate(s);
- proposal mechanism;
- candidate hash;
- researcher/model identity;
- visible feedback context;
- execution status;
- validity status;
- metrics returned;
- duplicate relation;
- reason for rejection / failure;
- whether the result influenced later search.

A discarded branch remains part of the ledger.

### 4.6 Evaluation receipt

Each execution should bind at least:

- candidate hash;
- evaluator code/version identity;
- dataset identity/hash or immutable reference;
- evaluation configuration;
- timestamps;
- execution status;
- output/result hash;
- returned metrics;
- validation diagnostics.

The receipt states its assurance scope. A local receipt is causal/process evidence, not hardware-backed proof of physical execution.

## 5. Phase A — evaluator-integrity challenge

No market edge search occurs in this phase.

Use synthetic or toy inputs and deliberately construct candidates intended to stress the evaluator.

Required challenge classes:

- NaN;
- positive/negative infinity;
- empty signal;
- all-constant signal;
- malformed vector length;
- impossible timestamps;
- forbidden future-column reference;
- invalid resampling boundary;
- extreme position/leverage value;
- missing required field;
- duplicate candidate under different formatting;
- parser edge cases;
- attempt to report a fabricated metric;
- attempt to access filesystem/network/hidden inputs where the candidate representation permits such behavior.

### Pass conditions

All known-invalid candidates must be rejected before they can receive a legitimate performance score.

Additionally:

- repeated evaluation of the same deterministic candidate produces the same result;
- the researcher process cannot read hidden evaluation files;
- changing only a candidate-reported metric cannot improve the evaluator score;
- changing evaluator/data identity changes the receipt;
- a failed evaluator run cannot be recorded as a scientific negative result.

OpenEvolve Issue #183 is the motivating failure example: evolutionary search discovered tolerance and NaN weaknesses in its evaluator and produced an impossible score.

## 6. Phase B — synthetic autonomous-search benchmark

After Phase A passes, test whether the search loop can make useful progress under controlled conditions.

### Data

Generate multiple synthetic time-series worlds with:

- a small number of planted predictive relations;
- irrelevant features;
- correlated decoy features;
- regime changes;
- realistic noise;
- transaction-cost-like penalties where appropriate.

The generator and hidden seeds are not visible to the researcher during the run.

### Data roles

Use three roles:

- DEVELOPMENT — structure/schema/examples that the researcher may inspect;
- ADAPTIVE_VALIDATION — evaluator returns bounded feedback during search;
- FINAL_SYNTHETIC_HOLDOUT — hidden and not evaluated until search stops.

### Search budget

Use a small fixed budget for v0.1.

The exact number of candidate evaluations must be frozen before the first run. A range such as 20–50 is operationally reasonable for the first engineering test, but this draft does not freeze the number.

### Baselines

Compare the autonomous search against at least:

- random candidate generation from the same grammar;
- a simple non-LLM search rule where feasible.

The purpose is not to declare a universal winner. It is to determine whether adaptive AI search adds useful search behavior under a controlled and auditable candidate budget.

### Recorded outcomes

Record:

- candidates proposed;
- candidates executed;
- invalid candidates;
- duplicates;
- search-tree depth;
- number of pivots/refinements;
- adaptive-validation best score;
- final synthetic holdout score;
- adaptive-to-final degradation;
- planted-signal recovery;
- result variance across independent seeds;
- compute / model cost;
- evaluator violations detected.

## 7. Phase C — historical market method pilot

Only after the synthetic pilot passes should the loop touch real historical market data.

This phase remains **exploratory**.

Preferred choices:

1. create a new research line with a deliberately designated development/adaptive-validation historical sample; or
2. use already-consumed historical evidence only, with an explicit statement that no new confirmatory claim can result.

Using Horizontal Reaction H1/H2 is possible only as consumed historical material and must not change the frozen Post-H2 boundary.

A clean new line is easier to interpret because Horizontal Reaction already carries a historical source conflict and specific prospective commitments.

## 8. Phase D — isolated prospective confirmation

A real edge claim requires evidence outside adaptive search.

The strongest practical boundary is data that did not exist when the candidate and protocol were frozen.

Sequence:

```text
autonomous search ends
→ candidate/specification frozen
→ no further parameter or rule changes
→ future data accumulate
→ trusted evaluator runs once under preregistered rules
→ result recorded
```

This helps with both:

- ordinary market lookahead;
- LLM pretraining knowledge of historical outcomes.

It does not solve every form of regime dependence, selection bias, or implementation risk.

## 9. Statistical search controls

Large AI search budgets make selection bias part of the experiment.

The pilot should therefore preserve enough information to support several established diagnostics.

### 9.1 Deflated Sharpe Ratio

Potential use:

- assess a selected Sharpe ratio after accounting for selection pressure and non-normal returns.

Do not use DSR as a substitute for final holdout evidence.

### 9.2 Probability of Backtest Overfitting / CSCV

Potential use:

- estimate family-level overfitting when many comparable strategy return streams have been tried.

This requires a suitable matrix of candidate performance across partitions.

### 9.3 Reality Check / SPA

Potential use:

- test whether the best of many candidates shows predictive superiority over a benchmark after data-snooping adjustment.

The precise bootstrap/dependence assumptions must be matched to the research design.

### 9.4 Multiple-hypothesis / FDR procedures

Potential use:

- when the research family produces formal test statistics/p-values for many hypotheses.

Do not manufacture p-values merely so an FDR procedure can be applied.

### 9.5 Rule

No statistical correction restores the status of a final holdout after adaptive inspection.

## 10. Feedback minimization

An adaptive evaluator should return the minimum information needed for productive search.

Potential levels, from weaker to stronger isolation:

1. full metric vector;
2. selected metric subset;
3. pass/fail against a preregistered threshold;
4. rank or coarse bucket;
5. no feedback — final holdout.

v0.1 should test whether useful search is possible with less feedback rather than defaulting to full diagnostic exposure.

## 11. Search-memory rules

The researcher may retrieve historical search records, but retrieval must preserve status.

At minimum, distinguish:

- VALID_BUT_POOR;
- INVALID;
- EXECUTION_FAILED;
- DUPLICATE;
- PROMISING_EXPLORATORY;
- SELECTED_FOR_FINAL_SYNTHETIC_TEST;
- FINAL_TESTED.

These are pilot labels, not proposed Knowledge Base schema values.

The researcher must not be shown a compact history that silently omits unsuccessful trials, because trial count and failed directions are part of the evidence.

## 12. Human decision boundary

Human intervention is required when changing:

- research question;
- candidate grammar;
- feature universe;
- temporal semantics;
- evaluator;
- dataset role;
- search budget;
- statistical promotion rule;
- final-holdout protocol;
- live-risk or execution authority.

Human approval should not be required for every individual candidate inside a frozen search contract.

That is the practical route toward a system where the human sets direction and risk boundaries while AI performs most routine research work.

## 13. Promotion gates

A candidate should not move forward merely because it has the best adaptive-validation score.

Before synthetic final evaluation:

- valid candidate;
- evaluator diagnostics pass;
- provenance receipt complete enough for the declared scope;
- within frozen search budget;
- no forbidden-data access;
- not an unrecorded duplicate.

Before real prospective evaluation:

- mechanism/specification frozen;
- all adaptive trials counted;
- historical result classified exploratory;
- relevant selection-bias diagnostics computed where applicable;
- transaction/execution assumptions explicit;
- prospective dataset role fixed before observation.

Before live capital:

- outside the scope of this pilot;
- requires a separate execution/risk validation process.

## 14. Failure conditions

Stop and repair the research machinery if any of the following occurs:

- researcher obtains final-holdout-derived information;
- candidate changes or bypasses the evaluator;
- non-finite values receive a valid score;
- result cannot be bound to candidate/evaluator/data identity;
- trial count becomes incomplete;
- failed execution is promoted as negative scientific evidence;
- final holdout is rerun after post-result changes;
- search contract changes without starting a new version.

## 15. Minimal implementation sequence

1. Define the candidate schema.
2. Build the trusted evaluator with synthetic data only.
3. Write adversarial evaluator tests.
4. Add candidate/evaluator/data/result receipts.
5. Add append-preserving search ledger.
6. Run a non-AI random-search baseline.
7. Run one AI adaptive search with the same budget.
8. Execute one sealed synthetic final evaluation.
9. Review all rejected/invalid branches.
10. Decide whether a real historical-data pilot is justified.

Do not start from multi-agent orchestration.

A single researcher agent plus a trusted evaluator is sufficient to test the central scientific boundary.

## 16. Evidence behind the design

Primary external examples:

- Microsoft RD-Agent / RD-Agent(Q) — real adaptive quant research loop; holdout/promotion boundary problems identified in current project review.
- AlphaAgent / QuantaAlpha — structured factor search and deterministic constraints.
- AutoScientist-Quant — adaptive research-direction selection with separate final evaluation.
- Karpathy autoresearch — minimal edit surface; public metric-integrity criticism.
- AlphaEvolve / OpenEvolve — evaluator-driven evolutionary search; concrete reward-hacking failure in OpenEvolve.
- AIDE — solution-tree search and full intermediate journal.
- MLE-bench — hidden-label evaluation, benchmark contamination issues, version/fairness problems.
- Validation Bottleneck — model-cutoff contamination, preregistration, enumerable trial counts, multiple-testing correction.
- Bailey et al. / White / Hansen / Harvey et al. — established selection-bias and data-snooping controls.

## 17. Current recommendation

Do not spend the next development step on:

- broker automation;
- arbitrary Python strategy generation;
- multi-agent role proliferation;
- another unused market holdout.

The smallest high-information next experiment is:

**build and attack the trusted synthetic evaluator boundary.**

If that survives, add the autonomous search loop.

If the search loop survives, then move to exploratory historical market data.

Only after that should the project expose a genuinely unused/prospective market sample.
