# Schema v0.1

Status: PILOT_VALIDATED_V0.1

This folder contains the machine-addressable conventions for Knowledge Base v0.1.

See `docs/KNOWLEDGE_BASE_V0.1.md` for rationale.

## Storage model

Narrative entities use Markdown with YAML frontmatter.

Concrete execution attempts use a YAML run manifest.

Diagnostics use a YAML record plus optional Markdown narrative if needed.

## Common frontmatter

Every Markdown entity should include:

```yaml
---
id: HYP-HR-001
type: Hypothesis
research_line_id: RL-HR-001
created_at: 2026-09-27
status: ACTIVE
relations: []
---
```

Rules:

- `id` is stable and unique.
- `type` is explicit.
- `research_line_id` is required except on the ResearchLine itself.
- dates use ISO-8601.
- references use entity IDs.
- status words must not replace the independent result status dimensions.
- unknown values are written as `UNKNOWN` or omitted only when the field is optional; do not infer them.
- use `NOT_APPLICABLE` when a required schema dimension genuinely does not apply; do not use `UNKNOWN` for non-applicability.

## Relation record

```yaml
relations:
  - type: tests_hypothesis
    target: HYP-HR-001
  - type: supersedes
    target: INT-HR-002
```

Allowed v0.1 relation types:

- tests_hypothesis
- uses_specification
- uses_dataset
- produced_by_run
- interprets_result
- supports
- contradicts
- supersedes
- invalidates
- corrects
- derived_from

## Required result status dimensions

```yaml
execution_status: SUCCESS
evidence_validity: VALID
scientific_status: NOT_SUPPORTED
```

These dimensions are independent.

`scientific_status: NOT_APPLICABLE` is valid for source qualification, blocked execution, or other records that produce no scientific outcome.

Do not encode:

`status: FAILED`

when the intended meaning could be either execution failure or scientific rejection.

## Dataset use

Every Experiment / Run should state the actual role of every dataset use.

```yaml
dataset_uses:
  - dataset_id: DATA-HR-001
    role: CONSUMED_HOLDOUT
    may_influence_future_search: false
```

The underlying Dataset may be reused in historical recomputation, but its scientific role cannot be reset from consumed to unused.

## Corrections

Do not silently rewrite finalized historical evidence.

Preferred pattern:

```yaml
relations:
  - type: corrects
    target: RES-HR-003
```

and explain the correction and affected conclusions.

## Current projection

`CURRENT.md` is derived and noncanonical.

It must list the Decision and Interpretation IDs it summarizes.

## Validation philosophy

v0.1 relies on human review plus simple future linting.

No schema-validation framework is added yet.

The first objective is to discover whether the structure is usable on Horizontal Reaction before automating validation.


## Pilot refinements

The Horizontal Reaction pilot established three v0.1 refinements:

1. `tests_hypothesis` is conditional. For SOURCE_QUALIFICATION or descriptive/operational DIAGNOSTIC experiments that do not test a scientific hypothesis, write `NOT_APPLICABLE`.
2. provenance guarantee values may use `PARTIAL` when the captured and uncaptured portions are explicitly explained.
3. repeated concrete attempts for one Experiment may use `RUN-...-ATTEMPT-N` and matching Result IDs while preserving one Experiment identity.

These refinements came from concrete migration cases and do not change the scientific record.
