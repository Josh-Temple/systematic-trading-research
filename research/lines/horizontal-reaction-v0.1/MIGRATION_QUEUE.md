# Horizontal Reaction Migration Queue

Updated: 2026-09-27
Phase: 3
Status: IN_PROGRESS

## Purpose

Migrate the remaining Horizontal Reaction Strategy v0.1 history into Knowledge Base v0.1 without changing the scientific record.

The canonical trunk has already been created:

- RL-HR-001
- HYP-HR-001
- SPEC-HR-001-v01
- DATA-HR-001
- EXP-HR-001
- RUN-HR-001
- RES-HR-001
- INT-HR-001
- DEC-HR-001

Do not rewrite those artifacts merely to normalize wording.

If a factual conflict is found, record it in the task result and stop before modifying the existing artifact.

## Operating rules

1. Fresh-read GitHub main before each work batch.
2. Read `docs/KNOWLEDGE_BASE_V0.1.md`, `schema/v0.1/README.md`, and the existing Horizontal Reaction line.
3. Use the actual Google Drive / Project source documents as evidence.
4. Do not use chat memory as evidence for current scientific state.
5. Preserve source terminology where possible.
6. Separate:
   - source fact,
   - migration interpretation,
   - unknown / unsupported field.
7. Use `UNKNOWN` / `UNVERIFIED` rather than filling gaps.
8. Do not turn a blocked run into a negative scientific result.
9. Do not turn an exploratory diagnostic into confirmatory evidence.
10. Do not change holdout/sample roles after outcome access.
11. Do not modify scientific rules, thresholds, parameters, or interpretations.
12. No broker/live-trading actions.
13. Do not update `CURRENT.md` until MIG-HR-007.

## ID reservation

Use these IDs unless the source forces an additional entity.

### MIG-HR-001 — Source Pack recovery

- EXP-HR-002
- RUN-HR-002
- RES-HR-002

Purpose:
Represent the 2026H1 persistent Source Pack recovery and identity validation.

Primary source:
`Horizontal Reaction Strategy v0.1 — 2026H1 Source Pack Recovery Result (Chat Branch)`

Required distinctions:

- recovery/qualification is not a new trading test
- D1-D5 were deliberately NOT_RUN in this work
- underlying per-file content identity matched even though packaging differed
- preserve aggregate-SHA limitation
- DATA-HR-001 remains the scientific sample; create a new Dataset entity only if the source establishes a materially different dataset identity rather than a recovered packaging/artifact

Expected experiment_kind:
`SOURCE_QUALIFICATION`

### MIG-HR-002 — Blocked D1-D5 replay attempt

- EXP-HR-003
- RUN-HR-003
- RES-HR-003
- DIAG-HR-001 if useful for checked/not-checked scope

Primary source:
`Horizontal Reaction Strategy v0.1 — D1-D5 Diagnostic Replay Result (Chat Branch)`

Required state:

- execution_status = BLOCKED
- D1-D5 = NOT_RUN
- do not infer any scientific explanation
- preserve ERR_BLOCKED_BY_CLIENT and source-identity boundary
- no substitute data were used

This artifact must remain historical after later successful diagnostics.

### MIG-HR-003 — Independent exploratory Data diagnostic

- EXP-HR-004
- RUN-HR-004
- RES-HR-004
- DIAG-HR-002

Primary source:
`Horizontal Reaction Strategy v0.1 — Data Exploratory Diagnostic Result — 2026H1 v1`

Required state:

- experiment_kind = DIAGNOSTIC
- confirmatory evidence = NO
- population = fixed 2,685-trade consumed sample
- no population change / exclusions / parameter tuning / rule change
- preserve that the executed 35-code-cell notebook was not located as a retrievable artifact
- distinguish same-timestamp midpoint comparison from formal D5
- preserve diagnostic blind spots / not-established statements

Do not turn exploratory subgroup findings into new rules.

### MIG-HR-004 — Successful D1-D5 diagnostic / integrated H1 decomposition

Reserved IDs:

- EXP-HR-005
- RUN-HR-005
- RES-HR-005
- DIAG-HR-003
- INT-HR-002

Find the strongest canonical source(s) in Google Drive.

The current Project Brief reports at least:

- D1 touch→entry mean +0.331R
- D4 touch→15m mean +0.125R
- D2 entry→15m no-barrier mean -0.205R
- session-clustered 95% CI -0.304 to -0.114
- D3 stopped-trade +15m mean -1.034R
- 54.7% of stop trades recross entry within 15m after stop
- midpoint gross mean -0.0413R
- BID/ASK net mean -0.2016R
- spread drag 0.1603R
- current interpretation: MULTIPLE_DRIVERS / INCONCLUSIVE

But do not use this queue as evidence. Locate and read the canonical source documents and record their URLs/IDs.

INT-HR-002 should supersede INT-HR-001 only if the source explicitly supports the newer interpretation.

### MIG-HR-005 — 2026H2 Unconditional Touch Replication

Reserved IDs:

- HYP-HR-002 if a distinct hypothesis is explicit
- SPEC-HR-002-v01
- DATA-HR-002
- EXP-HR-006
- RUN-HR-006
- RES-HR-006
- INT-HR-003 if needed
- DEC-HR-002 if needed

Locate preregistration and result sources in Drive.

The Project Brief reports a frozen 60-session replication and classification `NO_UNCONDITIONAL_TOUCH_SUPPORT`.

Do not use that summary as the only evidence if the canonical result exists.

Record whether this experiment tests the same HYP-HR-001 or a narrower/new hypothesis. Do not invent HYP-HR-002 unless supported.

### MIG-HR-006 — Post-H2 Confirmation Selection Effect preregistration

Reserved IDs:

- HYP-HR-003 if source establishes a distinct hypothesis
- SPEC-HR-003-v01
- DATA-HR-003
- EXP-HR-007
- DEC-HR-003 if needed

Primary known Drive source:
`Horizontal Reaction — Confirmation Selection Effect Preregistration — Post-H2 v1`

Current source state should remain `WAITING_FOR_MATURITY` if still supported by fresh source.

Important:

- do not compute outcomes
- do not inspect/open outcome data beyond what the preregistration/source gate already authorizes
- preserve the rule that touch outcome / CONFIRMED-vs-UNCONFIRMED comparison / bootstrap is forbidden before maturity and source gate PASS
- if DATA-HR-003 is still unused, its role should reflect its actual scientific role without marking it consumed

### MIG-HR-007 — Current integrated state

After MIG-HR-001 through MIG-HR-006 are complete and read back:

Create/update only then:

- final current Interpretation ID if needed
- final current Decision ID if needed
- `CURRENT.md`

CURRENT.md must be derived only from migrated canonical IDs.

It should expose:

- current scientific classification
- active/frozen specification(s)
- 2026H1 consumed boundary
- current next test
- forbidden same-sample rescue
- known historical blocked/failed artifacts
- current waiting/hold state for Post-H2 work
- superseded interpretations

If migrated sources conflict, do not resolve silently. Add a projection conflict and report it.

## Validation after each task

For every new artifact:

- read back from GitHub
- verify all referenced entity IDs exist or are explicitly reserved for a later task
- verify execution/evidence/scientific status are not conflated
- verify source URL/title is recorded
- verify no source statement was strengthened

## Completion report

For each MIG-HR task report:

- created paths
- commit SHA(s)
- source documents used
- fields left UNKNOWN/UNVERIFIED
- any schema friction discovered
- any factual conflict with existing canonical trunk

Do not change the schema merely because a source is awkward to fit. Record schema friction for integration review.
