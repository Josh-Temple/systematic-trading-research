# Prior Repository Review — TEMPLATE

## Metadata

- Repository:
- URL:
- Review date:
- Reviewed commit / default branch state:
- Repository purpose:
- Maturity / activity notes:

## 1. What problem is this repository solving?

Describe the problem in the repository's own terms. Separate explicit claims from reviewer interpretation.

## 2. Canonical source of truth

- What is treated as canonical?
- Is there more than one source of truth?
- How are generated artifacts distinguished from canonical content?

## 3. Current repository structure

Summarize only the structure relevant to research, knowledge, experiments, data, results, decisions, and AI integration.

## 4. Knowledge / data model

- Main entity types
- Relationships
- Required metadata
- Status model
- Versioning model
- Indexes / manifests

## 5. Research lifecycle

Trace the actual path from idea or hypothesis to experiment, result, interpretation, and durable knowledge.

## 6. Experiment reproducibility

Check for:

- dataset identity
- code / commit identity
- config / parameters
- environment
- random seed
- output artifacts
- hashes / manifests
- rerun procedure

## 7. Negative / failed research

- Are failed experiments retained?
- Are rejected hypotheses searchable?
- Are null results first-class?
- Are infrastructure failures distinguished from scientific failures?

## 8. Current knowledge vs history

How does the project distinguish:

- current valid guidance
- superseded guidance
- historical experiment record
- exploratory observations
- confirmed findings

## 9. AI / agent role

- What can AI read?
- What can AI change?
- What can AI execute?
- Is AI-generated reasoning treated as evidence?
- How is human review handled?

## 10. Deterministic execution boundary

What is delegated to deterministic code or fixed pipelines instead of model judgment?

## 11. Human-facing interface

- README / docs
- web app / dashboard
- notebook
- CLI
- graph / search
- other

Assess whether the interface exposes provenance and research state, not only headline results.

## 12. AI-facing retrieval

- MCP
- structured index
- database queries
- embeddings / RAG
- file search
- other

Note whether retrieval is broad-context loading or targeted retrieval.

## 13. Issues / discussions findings

Record only material design problems, recurring pain points, or decisions relevant to our project.

## 14. Commit-history findings

Identify meaningful redesigns, simplifications, reversals, migrations, or deleted approaches.

Do not infer motives that are not documented.

## 15. Failure cases / abandoned approaches

What did not work, was removed, or was explicitly rejected?

## 16. Strengths

Concrete strengths supported by repository evidence.

## 17. Limitations

Concrete limitations. Distinguish project-specific limitations from general architectural risks.

## 18. Transferable lessons

Classify each lesson:

- STRONG_COMMON_PRINCIPLE
- PLAUSIBLE_PATTERN
- PROJECT_SPECIFIC
- DO_NOT_COPY

For each item, explain why.

## 19. Questions for cross-repository synthesis

List unresolved questions that should be compared against other repositories.

## 20. Sources reviewed

Record README/docs, issues, commits, files, releases, or other evidence used.

## Review status

- COMPLETE
- PARTIAL
- BLOCKED

Reason:
