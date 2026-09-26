# Luna Work Instruction — Horizontal Reaction Phase 3 Migration

Target repository:
`Josh-Temple/systematic-trading-research`

Execute the migration queue in:

`research/lines/horizontal-reaction-v0.1/MIGRATION_QUEUE.md`

## Role

You are a migration worker, not the scientific decision maker.

Your task is to convert existing source-backed Horizontal Reaction research artifacts into the already-defined Knowledge Base v0.1 structure.

Do not redesign the schema and do not reinterpret the research.

## Start

Fresh-read GitHub main.

Then read:

- `docs/ROADMAP.md`
- `docs/RESEARCH_PRINCIPLES.md`
- `docs/KNOWLEDGE_BASE_V0.1.md`
- `schema/v0.1/README.md`
- `schema/v0.1/PILOT_CHECKLIST.md`
- all existing files under `research/lines/horizontal-reaction-v0.1/`
- `research/lines/horizontal-reaction-v0.1/MIGRATION_QUEUE.md`

Do not use prior chat memory or old SHAs as evidence of current repository state.

## Source use

Use Project files first for Project-configured Horizontal Reaction sources.

For required source documents not present in Project files, search connected Google Drive by exact title and read the actual file.

Source documents are authoritative for the migration.

Do not silently reconcile conflicting documents. Preserve the conflict and report it.

## Execution

Process MIG-HR-001 through MIG-HR-006 sequentially.

After each task:

1. create only the files required by that task,
2. commit,
3. read back,
4. verify references and statuses,
5. continue only if no factual conflict with the existing canonical trunk is found.

If a factual conflict with the existing trunk is found:

- do not edit the existing trunk,
- record the exact conflict,
- stop that task with `MIGRATION_CONFLICT`,
- continue to another independent task only if it does not depend on the conflict.

Do not execute MIG-HR-007 until 001–006 are sufficiently complete.

## Critical scientific boundaries

- blocked execution != negative scientific result
- exploratory diagnostic != confirmatory evidence
- diagnostic PASS != universal proof
- consumed sample != unused sample
- current interpretation must not erase historical interpretation
- unknown provenance must remain UNKNOWN/UNVERIFIED
- no same-sample parameter rescue
- no new trading hypothesis, filter, threshold, stop, target, or time rule
- no outcome access prohibited by an existing preregistration
- no broker or live trade action

## Output

Write results to GitHub.

At the end, report:

- status of MIG-HR-001 through MIG-HR-007
- all created paths and commits
- source documents used
- unresolved UNKNOWN/UNVERIFIED fields
- schema friction
- conflicts
- whether `CURRENT.md` was safe to create

Keep the report concise. The integration session will review all outputs before Phase 3 is closed.
