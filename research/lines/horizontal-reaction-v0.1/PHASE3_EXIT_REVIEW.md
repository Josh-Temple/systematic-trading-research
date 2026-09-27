# Phase 3 Exit Review — Horizontal Reaction v0.1 Pilot

Date: 2026-09-27
Status: PASS_WITH_RECORDED_SOURCE_CONFLICT

## Decision

**PASS — Horizontal Reaction Strategy v0.1 can be reconstructed from GitHub alone with the known source conflict explicitly exposed.**

Phase 3 exit does not require resolving every historical source disagreement. It requires that current state, historical state, scientific boundaries, and unresolved conflicts be represented without silent reconciliation.

## Scope reviewed

Fresh-read from current GitHub main:

- research line root and CURRENT.md
- HYP-HR-001 through HYP-HR-003
- SPEC-HR-001-v01 through SPEC-HR-003-v01
- DATA-HR-001 through DATA-HR-003
- EXP-HR-001 through EXP-HR-007
- all migrated Run / Result records including blocked attempts
- DIAG-HR-001 through DIAG-HR-003
- INT-HR-001 through INT-HR-003
- DEC-HR-001 through DEC-HR-003
- schema/v0.1 pilot checklist

## Pilot checklist result

### A. Lineage completeness — PASS

- ResearchLine exists.
- Original/frozen hypothesis is represented.
- Governing specifications are represented and versioned.
- Distinct H1, H2, and prospective Post-H2 datasets are represented.
- Intended experiments are separated from concrete Run attempts.
- Blocked H1 and H2 execution attempts are preserved.
- Interpretations reference their Results.
- Decisions reference their evidence.
- CURRENT.md derives from explicit Decision and Interpretation IDs.

### B. Scientific boundary — PASS

- 2026H1 remains CONSUMED_HOLDOUT.
- 2026H2 unconditional-touch sample remains CONSUMED_HOLDOUT.
- Post-H2 DATA-HR-003 remains FINAL_HOLDOUT / UNUSED.
- Exploratory H1 diagnostics remain EXPLORATORY.
- Blocked source/replay attempts are not represented as negative scientific results.
- Later successful runs do not erase blocked attempts.
- Same-sample rescue is explicitly forbidden.
- The next admissible test is distinct from prohibited rescue search.

### C. Provenance — PASS WITH KNOWN UNVERIFIED FIELDS

Captured where source-backed:

- provider / instrument / timeframe / granularity
- BID/ASK execution semantics
- source hashes and source-identity evidence where available
- output references and selected output hashes
- calculation-script hash for completed H2 replication

Still UNKNOWN / UNVERIFIED where sources do not establish them:

- several run timestamps
- H1 analysis-code identity
- several environment identities
- some causal-lineage guarantees
- final H2 raw Tick per-file hash values in the migrated source text
- Post-H2 final sample identity and source hashes

These remain explicitly unknown rather than inferred.

### D. Status separation — PASS

The pilot now cleanly distinguishes:

- execution failure / block
- evidence validity
- scientific support / non-support
- exploratory result
- no scientific outcome

Pilot refinement:

`scientific_status: NOT_APPLICABLE` is now allowed for source qualification or blocked attempts that produced no scientific outcome.

### E. Diagnostic scope — PASS

Diagnostics record:

- checked scope
- coverage
- known blind spots
- not-tested dimensions
- evidence references

The H1 ledger midpoint exercise is explicitly not formal D5.

The historical blocked D1-D5 attempt remains separate from later exploratory D1-D5 work.

### F. Human usability — PASS BY STRUCTURAL REVIEW

A reviewer can reconstruct the line primarily from:

1. LINE.md
2. CURRENT.md
3. referenced current Interpretation / Decision
4. underlying Result / Run / Dataset records

CURRENT.md answers:

- what is currently supported/not supported
- which samples are consumed
- what failed operationally
- what interpretation is current
- what conflict remains open
- what test is allowed next
- what actions remain forbidden

This is a structural review, not a timed independent-user usability study.

### G. AI retrieval safety — PASS AT DOCUMENT-MODEL LEVEL

The migrated structure explicitly prevents the following semantic collapses:

- historical positive observation -> current support
- blocked execution -> negative scientific result
- consumed holdout -> unused sample
- exploratory diagnostic -> confirmatory evidence
- unknown provenance -> inferred guarantee

Automated retrieval enforcement is not yet implemented; that belongs to later index/MCP phases.

## Schema refinements discovered by the pilot

Three concrete v0.1 refinements were required.

### 1. Hypothesis link is conditional

SOURCE_QUALIFICATION and descriptive/operational DIAGNOSTIC experiments may not directly test a scientific hypothesis.

Rule:

- use a real Hypothesis ID when a hypothesis is directly tested
- use `NOT_APPLICABLE` when no hypothesis test occurs
- use `UNKNOWN` only when the fact is genuinely unknown

### 2. Scientific status may be NOT_APPLICABLE

A valid Result can represent:

- source qualification
- blocked execution
- operational gate result

without producing a scientific hypothesis outcome.

This must not be forced into SUPPORTED / INCONCLUSIVE / TESTING.

### 3. Provenance guarantee may be PARTIAL

Some source records capture part, but not all, of an identity guarantee.

`PARTIAL` is permitted only when captured and missing portions are described explicitly.

### 4. Multiple Run attempts per Experiment

A single frozen Experiment may have multiple concrete attempts.

The optional suffix:

- `RUN-...-ATTEMPT-N`
- `RES-...-ATTEMPT-N`

is permitted for historical attempt preservation without inventing a new Experiment.

## Open source conflict

MIG-HR-004 preserved a material discrepancy between:

- 2026-09-13 Data D1-D5 exploratory replay
- 2026-09-23 diagnostic report / Project Brief

The sources differ on:

- endpoint availability
- D2-D5 sample counts
- several estimates
- classification:
  - EDGE_LOST_BEFORE_ENTRY
  - MULTIPLE_DRIVERS / INCONCLUSIVE

No retrieved source explicitly establishes that the later record invalidates the earlier one.

Therefore:

- both remain historical evidence
- CURRENT.md uses the Project Brief's stated current classification
- the discrepancy is explicitly exposed
- the Knowledge Base does not silently adjudicate it

This is an unresolved evidence conflict, not a migration failure.

## Post-H2 holdout state

HYP-HR-003 / SPEC-HR-003-v01 / EXP-HR-007 remain WAITING_FOR_MATURITY.

DATA-HR-003 remains:

- FINAL_HOLDOUT
- UNUSED
- source identity not yet finalized

No outcome computation or inspection was performed during migration.

## Phase 3 exit condition

Roadmap condition:

> Horizontal ReactionをGitHubだけで追跡して、研究状態を誤解なく再構成できること。

Assessment:

**PASS**

The current GitHub representation is sufficient to reconstruct:

- frozen v0.1 rules
- H1 negative execution result
- source-recovery history
- blocked D1-D5 attempt
- exploratory diagnostics
- unresolved D1-D5 source conflict
- H2 negative unconditional-touch replication
- consumed sample boundaries
- Post-H2 preregistration and current maturity hold
- current permitted / forbidden next actions

## Phase 3 result

`PHASE_3_EXIT = PASS_WITH_RECORDED_SOURCE_CONFLICT`

The conflict remains open by design.

No additional migration work is required before proceeding to the human-facing UI phase.
