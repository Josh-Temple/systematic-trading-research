# Knowledge Base v0.1 Design

Updated: 2026-09-27
Status: DRAFT_FOR_PILOT
Phase: 2

## 1. Purpose

Knowledge Base v0.1 is the minimum research representation required to migrate and reconstruct one complete systematic-trading research lineage.

The first pilot is Horizontal Reaction Strategy v0.1.

The design is intentionally small. It does not attempt to model every future research workflow.

## 2. Design goals

The v0.1 structure must make it possible to answer, without relying on chat history:

1. What was the hypothesis?
2. What was fixed before the result was observed?
3. Which data were used, and in what scientific role?
4. What exactly was run?
5. Did execution succeed?
6. Is the evidence valid?
7. What did the result show?
8. How was the result interpreted?
9. What decision followed?
10. What is currently believed?
11. Which older conclusions were superseded, invalidated, corrected, or merely historical?
12. Which diagnostics were performed, and what did they actually guarantee?

## 3. Core principles inherited from Phase 1

v0.1 implements the following constraints from `research/prior-art/SYNTHESIS_V0.2.md`.

- current state and historical record are separate
- negative / rejected / invalidated / failed / insufficient-evidence states remain discoverable
- result, interpretation, and decision are different artifacts
- provenance scope is explicit
- knowledge correctness, evidence correctness, and computation correctness are separate
- final holdout is outside adaptive search
- data visibility is part of scientific authority
- diagnostic PASS is bounded evidence, not absence proof
- temporal availability semantics belong to the experiment specification where relevant
- backtest correctness and live-execution parity are separate questions
- generated retrieval/navigation surfaces are not evidence authority

## 4. Directory layout

The first pilot should use one research-line-local tree.

```text
research/
  lines/
    <research-line-slug>/
      LINE.md
      CURRENT.md
      hypotheses/
      specifications/
      datasets/
      experiments/
      runs/
      results/
      interpretations/
      decisions/
      diagnostics/
```

Why research-line-local rather than global entity folders:

- one complete lineage is easy to inspect from a phone or GitHub UI
- entity ownership is obvious
- cross-project indexes are not needed yet
- later generated global indexes can scan these folders

## 5. Canonical vs derived artifacts

### Canonical historical artifacts

The following are canonical research history once finalized:

- Hypothesis
- Specification
- Dataset record
- Experiment
- Run manifest
- Result
- Interpretation
- Decision
- Diagnostic record

Corrections should normally create a new artifact or version that explicitly references the earlier artifact.

### Derived current-state artifact

`CURRENT.md` is a projection.

It should answer:

- current scientific state
- active interpretation
- active decision
- consumed data boundaries
- next admissible test
- known invalid / superseded evidence

It is not the authority by itself.

Its frontmatter must list the Decision / Interpretation IDs from which it was derived.

## 6. Core entity types

### 6.1 ResearchLine

Purpose:
Define the long-lived research question and scope.

Required fields:

- `id`
- `type: ResearchLine`
- `title`
- `status`
- `created_at`
- `scope`
- `current_projection`

### 6.2 Hypothesis

Purpose:
Record the claim being tested without rewriting it after results.

Required fields:

- `id`
- `type: Hypothesis`
- `research_line_id`
- `created_at`
- `statement`
- `status`
- relations

### 6.3 Specification

Purpose:
Freeze the scientific conditions that govern an experiment.

Required fields:

- `id`
- `type: Specification`
- `research_line_id`
- `version`
- `frozen_at`
- `freeze_status`
- `tests_hypothesis`
- `data_roles_allowed`
- `outcome_definition`
- `metrics`
- `stopping_or_kill_conditions`

Optional but important where applicable:

- signal timestamp semantics
- information availability semantics
- execution timestamp semantics
- resampling / merge rules
- side / bid-ask conventions
- parameter-search permission
- holdout access rule

A specification used by a run must not be silently edited afterward.

### 6.4 Dataset

Purpose:
Identify data and its scientific role separately from the run using it.

Required fields:

- `id`
- `type: Dataset`
- `research_line_id`
- `provider`
- `instrument`
- `time_range`
- `granularity`
- `role`
- `consumption_status`
- `may_influence_future_search`
- `identity_evidence`

Allowed initial roles:

- `DEVELOPMENT`
- `ADAPTIVE_VALIDATION`
- `FINAL_HOLDOUT`
- `CONSUMED_HOLDOUT`
- `HISTORICAL_ONLY`

The same underlying bytes may have different scientific roles in different experiments. Dataset identity and dataset-use role must therefore not be treated as the same concept.

For v0.1, a Dataset record can contain a default role, while an Experiment/Run must record the actual role used.

### 6.5 Experiment

Purpose:
Represent the intended test.

Required fields:

- `id`
- `type: Experiment`
- `research_line_id`
- `tests_hypothesis`
- `uses_specification`
- `planned_dataset_uses`
- `created_at`
- `experiment_kind`

Candidate experiment kinds:

- `EXPLORATORY`
- `CONFIRMATORY`
- `REPLICATION`
- `DIAGNOSTIC`
- `SOURCE_QUALIFICATION`

An Experiment is not a Run. One intended experiment may have failed, blocked, corrected, or repeated runs.

### 6.6 Run

Purpose:
Record one concrete execution attempt.

Required fields are machine-readable and stored as a YAML manifest.

At minimum:

- `run_id`
- `experiment_id`
- `specification_id`
- `dataset_uses`
- `code_identity`
- `started_at`
- `completed_at`
- `execution_status`
- `outputs`
- `provenance_guarantees`

A run with `FAILED` or `BLOCKED` is still a durable research artifact.

### 6.7 Result

Purpose:
Record observed outputs separately from interpretation.

Required fields:

- `id`
- `type: Result`
- `run_id`
- `observed_at`
- `execution_status`
- `evidence_validity`
- `scientific_status`
- `headline_metrics`
- `artifact_refs`
- `diagnostic_refs`

Initial independent status dimensions:

#### execution_status

- `NOT_RUN`
- `SUCCESS`
- `FAILED`
- `BLOCKED`

#### evidence_validity

- `VALID`
- `INVALID`
- `PARTIAL`
- `UNVERIFIED`

#### scientific_status

- `EXPLORATORY`
- `TESTING`
- `SUPPORTED`
- `NOT_SUPPORTED`
- `INCONCLUSIVE`
- `SUPERSEDED`

These labels are v0.1 candidates. The pilot may revise them.

### 6.8 Interpretation

Purpose:
Explain what one or more Results mean without modifying the Results.

Required fields:

- `id`
- `type: Interpretation`
- `research_line_id`
- `interprets_results`
- `created_at`
- `claim`
- `confidence_or_boundary`
- `alternatives_considered`
- relations

Interpretation may be revised by creating a later Interpretation that `supersedes` the earlier one.

### 6.9 Decision

Purpose:
Record an explicit scientific/operational research decision.

Examples:

- continue
- stop
- deprioritize
- replicate
- hold for more evidence
- freeze current specification
- mark evidence invalid
- consume holdout

Required fields:

- `id`
- `type: Decision`
- `research_line_id`
- `created_at`
- `based_on`
- `decision`
- `reason`
- `effect_on_current_state`
- `next_allowed_actions`
- `forbidden_actions`

Past decisions remain historical even when superseded.

## 7. Optional supporting entity — Diagnostic

Diagnostics are important but are not part of the minimum causal lineage.

A Diagnostic record must include:

- `diagnostic_id`
- `target_run`
- `tool`
- `tool_version`
- `checked_scope`
- `coverage`
- `overrides`
- `result`
- `known_blind_spots`
- `not_tested`
- `evidence_refs`

A PASS without scope is invalid as a v0.1 diagnostic record.

## 8. Relations

v0.1 starts with a deliberately small relation vocabulary.

- `tests_hypothesis`
- `uses_specification`
- `uses_dataset`
- `produced_by_run`
- `interprets_result`
- `supports`
- `contradicts`
- `supersedes`
- `invalidates`
- `corrects`
- `derived_from`

Relations use stable entity IDs, not filenames alone.

New relation types require a concrete pilot need.

## 9. Stable IDs

IDs are human-readable and stable.

Recommended pattern:

```text
RL-<LINE>-NNN
HYP-<LINE>-NNN
SPEC-<LINE>-NNN-vNN
DATA-<LINE>-NNN
EXP-<LINE>-NNN
RUN-<LINE>-NNN
RES-<LINE>-NNN
INT-<LINE>-NNN
DEC-<LINE>-NNN
DIAG-<LINE>-NNN
```

For Horizontal Reaction, the line code can be `HR`.

Example only:

```text
RL-HR-001
HYP-HR-001
SPEC-HR-001-v01
EXP-HR-001
RUN-HR-001
RES-HR-001
```

Do not encode mutable scientific status in the ID.

## 10. Immutability policy

v0.1 does not make the whole repository append-only.

Instead:

### Freeze after use

- Specification once referenced by a Run
- Run manifest after execution is finalized
- Result after evidence is finalized

Corrections create a new artifact or explicit correction relation.

### Append / supersede

- Interpretation
- Decision

### Mutable / regenerable

- CURRENT.md
- indexes
- generated summaries
- future web/search projections

### Raw source

Prefer immutable/content-addressed identity where practical.

Do not claim immutability when only Git history exists.

## 11. Provenance guarantee model

A run records what is actually known.

Candidate values for each guarantee:

- `CAPTURED`
- `NOT_CAPTURED`
- `NOT_APPLICABLE`
- `UNVERIFIED`

Initial guarantee fields:

- `definition_identity`
- `code_at_start_identity`
- `input_snapshot_identity`
- `external_data_pinned`
- `environment_identity`
- `output_identity`
- `concurrent_mutation_prevented`
- `causal_lineage_independently_checked`

This avoids a misleading single `reproducible=true`.

## 12. Temporal semantics

Do not create a universal time ontology in v0.1.

A Specification should include only the time semantics needed by the experiment.

For market-data research, candidate fields are:

- `source_timestamp_semantics`
- `information_available_at`
- `signal_decision_time`
- `execution_time_semantics`
- `resampling_or_merge_rule`

The Horizontal Reaction pilot should use only the fields needed for M1 signal data and raw BID/ASK Tick execution data.

## 13. Current projection

`CURRENT.md` should contain:

- research_line_id
- projection_generated_at
- derived_from_decisions
- derived_from_interpretations
- current_scientific_status
- current_interpretation
- active_specification
- consumed_data_boundaries
- current_next_test
- current_forbidden_reuses
- known_invalid_or_superseded_evidence

If two canonical decisions conflict, CURRENT.md must not silently choose one. The conflict should be exposed.

## 14. Fit check against Horizontal Reaction

The design was checked against the existing Horizontal Reaction source set without migrating it.

The lineage needs to accommodate at least:

- source qualification / recovery
- exact source identity and hash evidence
- an initial negative strategy result
- exploratory diagnostics on a consumed sample
- an attempted D1-D5 replay that could not run because source identity/data access was unavailable
- later source recovery
- later diagnostic replay/integration
- current multi-driver interpretation
- consumed-sample restrictions
- later unused/forward evidence

No additional entity type was required for these cases.

Important consequence:

A failed replay is represented as:

```text
Experiment
→ Run(execution_status=BLOCKED or FAILED)
→ Result(evidence_validity=UNVERIFIED/PARTIAL as appropriate)
```

It is not represented as a negative scientific result.

This distinction is central to the pilot.

## 15. Pilot acceptance criteria

Knowledge Base v0.1 passes Phase 2 only if the Horizontal Reaction pilot can be reconstructed from GitHub alone and the following questions have unambiguous answers:

1. Which specification governed each result?
2. Which dataset role was used?
3. Which sample is consumed?
4. Which run failed versus which scientific hypothesis was not supported?
5. Which evidence was later corrected or superseded?
6. Which interpretation is current?
7. Which historical interpretations remain discoverable?
8. Which next tests are scientifically permitted?
9. What does each provenance or diagnostic record actually guarantee?
10. Can an AI retrieve current evidence without confusing historical positive/invalidated findings with current state?

## 16. Deferred design

Not part of v0.1:

- graph database
- vector database
- MCP
- global cross-line ontology
- web UI
- automatic current-state generator
- automatic invalidation propagation engine
- live broker integration
- generalized market-event temporal ontology

Add these only after the pilot demonstrates a concrete need.
