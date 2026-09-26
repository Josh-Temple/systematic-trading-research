# Prior Repository Review — RD-Agent

## Metadata

- Repository: `microsoft/RD-Agent`
- URL: https://github.com/microsoft/RD-Agent
- Review date: 2026-09-27
- Reviewed default branch: `main`
- Reviewed head: `484776c211e4fbbeef03e0ec00d6bbee7362a4f4`
- Repository created: 2024-04-03
- Reviewed release state: current main identifies as release 1.0.0 at reviewed head
- Primary question: Does the autonomous quant R&D loop keep iterative search feedback separate from a final holdout, and how are experiment decisions / failures recorded?
- Review status: **PARTIAL**

Reason for PARTIAL: the current source path is sufficient to confirm that configured Qlib test/backtest metrics flow into iterative feedback and later proposal generation, but a full end-to-end Qlib/Docker runtime reproduction was not performed. The proposed holdout-isolation fix remains open/draft and unmerged.

## 1. What problem is this repository solving?

### FACT

RD-Agent is an autonomous data-driven R&D framework. In the finance/Qlib scenario it repeatedly:

1. proposes a hypothesis,
2. converts it to a concrete experiment,
3. generates/changes code,
4. runs the experiment,
5. evaluates the result,
6. records experiment + feedback,
7. uses prior experiments and feedback to propose the next round.

The README explicitly describes the intended loop as hypothesis → experiment → implementation → execution → feedback → improvement.

### INTERPRETATION

Unlike the earlier prior-art examples that mainly organize durable knowledge, RD-Agent directly automates the **adaptive research loop itself**.

That makes its scientific boundary especially important: a metric used as iterative feedback is no longer an untouched final holdout metric.

## 2. Canonical source of truth

### FACT

The current loop state is represented primarily in runtime objects and persisted session/log artifacts rather than one immutable scientific ledger.

Core structures include:

- `Trace.hist`: ordered tuples of `(Experiment, ExperimentFeedback)`
- `Trace.dag_parent`: experiment parent relationships
- per-step session snapshots from `LoopBase.dump()`
- runtime logs
- Qlib/MLflow experiment artifacts
- Qlib-generated metrics loaded into `exp.result`

`Trace.sync_dag_parent_and_hist()` appends experiment + feedback for recorded rounds.

### INTERPRETATION

RD-Agent has a real experiment lineage structure, not merely chat history.

However, the structure primarily captures **what the agent tried and what feedback it produced**. It does not by itself establish that the evaluation data used in that feedback remained scientifically independent.

## 3. Current repository structure relevant to this review

Relevant current paths:

```text
rdagent/
  core/
    proposal.py
    experiment.py
  components/
    workflow/
      rd_loop.py
  app/
    qlib_rd_loop/
      conf.py
      factor.py
      quant.py
  scenarios/
    qlib/
      proposal/
        factor_proposal.py
        quant_proposal.py
        bandit.py
      developer/
        factor_runner.py
        model_runner.py
        feedback.py
      experiment/
        workspace.py
        factor_template/
          conf_baseline.yaml
          conf_combined_factors.yaml
          read_exp_res.py
```

Open/unmerged PRs materially relevant to this review:

- PR #1442 — isolate holdout evaluation from iterative research feedback
- PR #1482 — preserve missing-result diagnostic log
- PR #1438 — deterministic LLM-free statistical guardrail proposal; closed/unmerged

## 4. Knowledge / data model

### FACT — Hypothesis and feedback

`Hypothesis` stores hypothesis text and reasoning fields.

`HypothesisFeedback` stores:

- observations
- hypothesis evaluation
- new hypothesis
- reason
- decision
- optional exception / acceptability fields

### FACT — Research trace

`Trace.hist` stores each experiment and corresponding feedback. `get_sota_hypothesis_and_experiment()` and `get_sota_experiment()` search backward for experiments whose feedback has `decision=True`.

### FACT — Qlib result

For factor/model experiments, Qlib metrics are loaded into `exp.result`.

The feedback implementation reads `exp.result` and compares it with the prior SOTA result.

### INTERPRETATION

The project already has a useful typed lineage:

```text
Hypothesis
→ Experiment
→ execution result
→ Feedback
→ decision
→ Trace
→ next Hypothesis
```

The main scientific issue is therefore not absence of lineage. It is **which evaluation data enters that lineage and influences subsequent search**.

## 5. Research lifecycle

### FACT

The generic `RDLoop` executes:

```text
direct_exp_gen
→ coding
→ running
→ feedback
→ record
```

The `record` step appends the experiment and feedback to `Trace`.

### FACT — next-round dependence

For factor-only research, `QlibFactorHypothesisGen.prepare_context()` includes previous hypothesis/feedback from `Trace.hist` in the prompt for the next hypothesis.

For the joint quant loop, `QlibQuantHypothesisGen.prepare_context()` also uses previous experiments and feedback.

When action selection is `bandit`, it extracts metrics directly from the previous experiment's `exp.result`, records them in the controller, and uses them to choose whether the next action should be factor or model research.

When action selection is `llm`, previous hypothesis + feedback are explicitly provided to the LLM.

### INTERPRETATION

Evaluation results influence later research by at least two routes:

1. textual LLM feedback / history,
2. direct metric-based bandit action selection.

Therefore, any data segment used to produce `exp.result` is part of the adaptive search process.

## 6. Holdout / evaluation boundary

### Current-main evidence

This section distinguishes source-confirmed behavior from unmerged proposals.

### FACT — configured data periods

The Qlib settings define separate:

- train
- valid
- test/backtest

date ranges.

### FACT — factor runner uses configured test range during ordinary iterative `develop()`

Current `QlibFactorRunner.develop()` constructs the runtime environment using:

- `train_start/train_end`
- `valid_start/valid_end`
- **`test_start/test_end`**

It then runs the Qlib template and assigns returned metrics to:

`exp.result`

There is no separate current-main `evaluate_holdout()` path in this runner.

### FACT — model runner does the same

Current `QlibModelRunner.develop()` also passes the configured `test_start/test_end` during the iterative experiment run and stores those metrics in `exp.result`.

### FACT — Qlib template uses that test segment for evaluation/backtest

The current factor templates define:

```yaml
segments:
  train: [...]
  valid: [...]
  test: [test_start, test_end]
```

and the portfolio backtest also starts at `test_start`.

`read_exp_res.py` reads the latest recorder metrics and the portfolio analysis result and exposes them to RD-Agent.

### FACT — feedback consumes these metrics

`QlibFactorExperiment2Feedback.generate_feedback()` reads:

- current `exp.result`
- previous SOTA `result`

and sends selected metrics to the LLM, which returns:

- observations,
- feedback,
- a new hypothesis,
- reasoning,
- **Replace Best Result** decision.

The model feedback path likewise uses `exp.result`.

### FACT — the result returns to future search

The resulting feedback is stored in `Trace.hist`; subsequent hypothesis generation reads the trace.

The quant bandit path independently extracts metrics from the previous `exp.result` and uses them to choose the next research action.

### RESULT

At reviewed current main, the configured Qlib **test/backtest segment participates in iterative search feedback**.

This conclusion is confirmed by the current source path. It does not depend solely on PR #1442's description.

### Limitation

A full Docker/Qlib runtime execution was not performed in this review. The conclusion is a code-path confirmation rather than an independent end-to-end backtest reproduction.

## 7. PR #1442 — proposed final-holdout isolation

### FACT

PR #1442:

- title: `fix(qlib): isolate holdout evaluation from iterative research feedback`
- state: **open**
- draft: **true**
- merged: **false**
- created: 2026-07-20
- no substantive maintainer review/comment was found; visible comments are policy-service agreement messages

The PR changes factor research so that:

- iterative `develop()` maps Qlib's internal test/evaluation segment to the configured **validation** range,
- a separate `evaluate_holdout()` uses configured test dates,
- final holdout results are stored separately,
- final holdout runs only after the research loop returns,
- holdout result does not replace iterative search result.

It also proposes focused regression tests.

### FACT — still absent from reviewed current main

At reviewed head `484776c...`:

- current factor runner still uses configured `test_start/test_end` in `develop()`,
- there is no current-main `evaluate_holdout()`,
- `test/qlib/test_factor_holdout.py` does not exist.

### INTERPRETATION

PR #1442 identifies a genuine current-main scientific boundary issue, but its proposed fix is **not a current guarantee**.

### Additional limitation

The PR specifically changes the factor path. This review did not establish a complete equivalent final-holdout isolation design for every Qlib model/joint-optimization path.

## 8. Feedback / decision authority

### FACT

Current factor/model experiment acceptance is produced by LLM-based feedback code.

For factor research the LLM is shown selected current and SOTA metrics and returns `Replace Best Result`.

For model research the LLM receives experiment/SOTA result data and returns a boolean decision.

That decision becomes part of `HypothesisFeedback`; the trace treats `decision=True` experiments as SOTA candidates.

### FACT — deterministic guardrail proposal is not current main

PR #1438 proposed an external LLM-free deterministic guardrail with:

- locked holdout,
- Deflated Sharpe Ratio,
- trial-count adjustment,
- cost-aware conditions.

But PR #1438 is:

- closed,
- unmerged,
- not part of reviewed main.

### INTERPRETATION

Current main cleanly separates **execution code** from **LLM reasoning** at an architectural level, but not **scientific promotion authority**.

A deterministic backtest can feed an LLM-controlled acceptance/replacement decision.

Therefore:

```text
deterministic experiment execution
≠
deterministic scientific decision
```

## 9. Trial accounting / repeated search

### FACT

`Trace.hist` retains experiments and feedback, so the system has a countable research history.

The quant bandit uses prior experiment metrics repeatedly.

### NOT VERIFIED

This review did not find, in current main's standard Qlib loop:

- a preregistered maximum number of trials,
- a mandatory multiple-testing correction,
- a mandatory Deflated Sharpe gate,
- a final-holdout-once policy enforced by current main.

PR #1438 proposed some of these ideas but was not merged.

### INTERPRETATION

RD-Agent provides experiment history, but experiment history alone does not enforce statistical trial discipline.

## 10. Negative / failed research

### Strength

`Trace.hist` can retain experiments whose feedback decision is false; therefore rejected iterations can remain part of the research history rather than only keeping the winning candidate.

`ExperimentFeedback` can also represent an exception and a negative decision.

### Failure-recording limitation

Current `QlibFBWorkspace.execute()` performs:

1. `qrun`
2. `python read_exp_res.py`

but if expected result files are missing, the current-main failure return contains only `execute_qlib_log`.

The separate `execute_log`, which can contain the actual `read_exp_res.py` failure reason, is discarded on that path.

PR #1482 proposes preserving both logs and adds a regression test, but the PR is open/unmerged.

Issue #442 documents an older real-world missing-backtest-artifact failure; discussion included a user report of a CUDA/GPU failure preventing the expected artifact from being produced.

### INTERPRETATION

A system can retain a failed experiment node while still losing the **most useful causal failure evidence**.

Thus:

```text
failure record exists
≠
failure diagnosis is complete
```

## 11. Current knowledge vs history

### FACT

RD-Agent's `Trace` stores historical experiments and decisions and can locate a current SOTA by traversing accepted feedback.

### INTERPRETATION

This is closer to **history + derived current selection** than to a manually maintained current-status Markdown file.

That is an important alternative to Trading Second Brain / zestoles / Epsilon.

### Limitation

The validity of current SOTA depends on the validity of the decision/evaluation process. If test/holdout results were repeatedly reused, the trace can accurately record a scientifically contaminated selection process.

## 12. AI / agent role

AI has broad authority in the normal R&D loop:

- propose ideas,
- generate experiment definitions,
- generate/change code,
- interpret metrics,
- generate feedback,
- suggest new hypotheses,
- influence accept/replace decisions.

Qlib / Python / Docker execute the numerical experiment.

### INTERPRETATION

RD-Agent is the clearest reviewed example so far of:

```text
AI reasoning
↔ deterministic execution
↔ feedback
↔ AI reasoning
```

The main lesson is that the boundary must include **data-access and decision-rights**, not only implementation language.

## 13. Deterministic execution boundary

### FACT

The numerical Qlib experiment runs through explicit Python/Qlib configuration and environment execution.

### LIMITATION

Deterministic execution does not automatically guarantee:

- final holdout isolation,
- bounded adaptive trials,
- deterministic promote/reject decisions,
- complete failure evidence.

### Strong implication

The important boundary for our project is likely not simply:

`AI vs deterministic code`

but at least:

```text
AI proposal
deterministic implementation/test
adaptive validation feedback
scientific promotion gate
final holdout
durable decision
```

with separate permissions and data visibility.

## 14. Commit / maturity findings

### FACT

The public repository dates from 2024-04 and remains active through the reviewed 2026-09 release 1.0.0.

The project has substantial contributor activity and a large current issue/PR surface.

The README notes that pre-open-source internal commit history was not preserved when confidential code was removed.

### INTERPRETATION

This is a more mature operational codebase than the first three knowledge-base examples, but its public history still does not capture the entire design lineage.

### Limitation

A complete multi-year commit archaeology was outside this focused review. This review concentrated on the current Qlib research loop and the material PRs/issues identified by the candidate scan.

## 15. Failure cases / unmerged redesigns relevant to the question

### A. Iterative configured-test feedback

Current-main code path confirmed.

Proposed correction:
- PR #1442
- still open/draft/unmerged

### B. LLM scientific promotion vs deterministic guardrail

Current-main: LLM feedback/decision.

Proposed alternative:
- PR #1438 deterministic guardrail
- closed/unmerged

### C. Missing diagnostic output on failed experiment

Current-main workspace still drops `read_exp_res.py` log on missing-result path.

Proposed correction:
- PR #1482
- open/unmerged

### INTERPRETATION

An important prior-art pattern is visible here: useful safety/scientific improvements can exist as **unmerged design proposals** without being actual product guarantees.

Deep reviews must therefore distinguish:

```text
idea
proposal
PR
merged implementation
tested current behavior
```

## 16. Strengths

### A. Real typed R&D loop

Hypothesis, experiment, feedback and trace are explicit objects.

### B. Historical experiment trace

Accepted and rejected experiments can remain in lineage.

### C. Feedback is first-class

The next research round can explicitly learn from prior results rather than relying on hidden chat memory.

### D. Deterministic execution engine boundary

Qlib/backtest execution is separate from LLM text generation.

### E. Session/checkpoint support

The workflow persists step snapshots and can resume long-running research.

### F. Mature extensibility

Proposal, coder, runner and summarizer components are pluggable.

## 17. Limitations

### A. Configured test/backtest is reused adaptively

Confirmed in current factor/model source paths.

### B. No current-main isolated final-holdout path was verified

PR #1442 is unmerged.

### C. Scientific promotion is LLM-controlled

No mandatory deterministic statistical gate in the reviewed current Qlib path.

### D. Trial history is not the same as trial-budget control

Trace exists, but mandatory multiple-testing controls were not verified.

### E. Failure evidence can be incomplete

Current workspace discards a downstream diagnostic log in a missing-result path.

### F. Reproducibility/provenance is distributed

Qlib/MLflow/workspace/session logs exist, but this review did not verify one immutable run manifest binding code, data, environment, result and scientific status.

## 18. Feedback Boundary Matrix

| Property | Assessment | Evidence / boundary |
| --- | --- | --- |
| Train/valid/test periods explicitly configured | **STRONG** | Qlib config classes/templates have separate periods. |
| Iterative search limited to train + validation | **NOT GUARANTEED** | Current factor and model runners use configured test/backtest period during ordinary iterative runs. |
| Final holdout isolated from feedback | **NOT GUARANTEED** | No separate current-main holdout path verified; PR #1442 proposes one. |
| Previous results influence next hypothesis | **STRONG** | Trace feedback is included in later proposal context. |
| Previous metrics influence action selection | **STRONG** | Quant bandit extracts metrics from prior `exp.result`. |
| Experiment history retained | **STRONG/PARTIAL** | Trace stores experiment + feedback; durability depends on session/log persistence. |
| Rejected experiments retained | **PARTIAL** | False-decision nodes can be stored; completeness across crashes/failures not guaranteed. |
| Deterministic promote/reject gate | **NOT GUARANTEED** | Current summarizers use LLM decisions; PR #1438 was unmerged. |
| Multiple-testing/trial-budget enforcement | **NOT VERIFIED** | No mandatory standard Qlib mechanism established in this review. |
| Final holdout single-use enforcement | **NOT GUARANTEED** | No current-main enforcement found. |
| Failure reason preservation | **PARTIAL** | Exception model exists, but workspace drops `read_exp_res.py` log in one current failure path; PR #1482 unmerged. |
| Current SOTA derivable from history | **PARTIAL** | Trace derives SOTA from feedback decisions, but validity depends on evaluation integrity. |

## 19. Transferable lessons

### STRONG_COMMON_PRINCIPLE — final holdout must be outside the adaptive loop

Current-main source confirms that once configured test metrics feed:

- LLM feedback,
- SOTA replacement decisions,
- trace history,
- bandit action selection,
- later hypothesis generation,

they are no longer an untouched final holdout.

This directly strengthens the existing holdout-once principle.

### STRONG_COMMON_PRINCIPLE — data visibility is part of the AI permission boundary

Separating AI from deterministic execution is insufficient if the AI receives final-holdout-derived metrics during iterative search.

### STRONG_COMMON_PRINCIPLE — experiment history does not itself prevent p-hacking

RD-Agent has a real trace, but without an enforced final-holdout boundary and trial budget, adaptive reuse remains possible.

### PLAUSIBLE_PATTERN — current state can be derived from immutable-ish experiment history

RD-Agent's SOTA lookup is an alternative to manually curated current-status pages.

This is useful, but only if the decision process itself is trustworthy.

### PLAUSIBLE_PATTERN — split feedback into validation feedback and final adjudication

PR #1442's architecture is conceptually strong:

- validation metrics drive search,
- final holdout runs after search,
- holdout result stored separately,
- final result does not flow back into search state.

Because the PR is unmerged, this is a design candidate, not validated current practice.

### DO_NOT_COPY — treat “test” naming as proof of holdout integrity

A segment named `test` can be repeatedly consumed inside the loop.

Scientific role must be enforced by access semantics, not naming.

### DO_NOT_COPY — let the same adaptive LLM both interpret final evidence and control future search without boundary

This makes final evidence part of optimization.

### DO_NOT_COPY — count a failed experiment while discarding its diagnostic cause

Failure state and failure evidence should be separately preserved.

## 20. Questions for cross-repository synthesis

1. Should systematic-trading-research use three explicit data roles: training, adaptive validation, final holdout?
2. Should final holdout be technically inaccessible to research agents until the research line is frozen?
3. Should a final-holdout result be written to a separate immutable artifact that cannot feed proposal generation?
4. Should scientific promotion be deterministic, human-approved, or both?
5. How should trial count follow a strategy/hypothesis lineage when implementation changes?
6. Can current knowledge be deterministically projected from experiment + decision history?
7. Should rejected experiments remain in the default AI retrieval index for duplicate prevention but be excluded from current recommendation context?
8. What failure evidence must be mandatory before a failed run is considered durably recorded?
9. Should every diagnostic/result declare whether it is allowed to influence future search?
10. Should the Knowledge Base encode data-access class as metadata on every experiment/result?

## 21. Sources reviewed

### systematic-trading-research fresh reads

- current repository main before review
- `README.md`
- `docs/ROADMAP.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `research/prior-art/README.md`
- `research/prior-art/CANDIDATE_SCAN.md`
- completed prior-art reviews including DVC

### RD-Agent current main

- repository metadata and recursive tree at `484776c211e4fbbeef03e0ec00d6bbee7362a4f4`
- `README.md`
- `rdagent/core/proposal.py`
- `rdagent/components/workflow/rd_loop.py`
- `rdagent/utils/workflow/loop.py`
- `rdagent/app/qlib_rd_loop/conf.py`
- `rdagent/scenarios/qlib/proposal/quant_proposal.py`
- `rdagent/scenarios/qlib/proposal/factor_proposal.py`
- `rdagent/scenarios/qlib/proposal/bandit.py`
- `rdagent/scenarios/qlib/developer/factor_runner.py`
- `rdagent/scenarios/qlib/developer/model_runner.py`
- `rdagent/scenarios/qlib/developer/feedback.py`
- `rdagent/scenarios/qlib/experiment/factor_template/conf_baseline.yaml`
- `rdagent/scenarios/qlib/experiment/factor_template/conf_combined_factors.yaml`
- `rdagent/scenarios/qlib/experiment/factor_template/read_exp_res.py`
- `rdagent/scenarios/qlib/experiment/workspace.py`

### PRs / issues

- PR #1442 — holdout isolation proposal; open, draft, unmerged
- PR #1438 — deterministic guardrail proposal; closed, unmerged
- PR #1482 — preserve failure diagnostic log; open, unmerged
- Issue #442 — missing Qlib backtest artifact / failure diagnosis discussion

## Review status

**PARTIAL**

### Reason

The most important question — whether configured test/backtest metrics enter the iterative research loop — is strongly supported by current-main source and independently reconstructed across runner → Qlib template → result → feedback/bandit → trace → next proposal.

However:

- no full Qlib/Docker runtime reproduction was performed,
- the entire multi-year design history was not exhaustively reviewed,
- proposed fixes remain unmerged,
- final-holdout behavior across every RD-Agent scenario was not audited.

The review is therefore strong enough for cross-repository synthesis on the holdout boundary, but not a complete audit of RD-Agent as a whole.
