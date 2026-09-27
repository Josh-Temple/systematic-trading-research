# Human-facing Web UI v0.1

Updated: 2026-09-28
Status: COMPLETE
Phase: 4

## Purpose

Provide a human-readable view over the canonical research files without creating a second source of truth.

The initial UI is intentionally scoped to one line:

- Horizontal Reaction Strategy v0.1

The UI must help a reviewer understand the current state before exploring historical evidence.

## Authority model

The website is a **derived view**.

Canonical authority remains under:

`research/lines/`

The UI must:

- link back to canonical files,
- expose when evidence is historical, exploratory, blocked, superseded, consumed, or unresolved,
- never silently adjudicate source conflicts,
- never turn a derived summary into scientific authority.

## v0.1 information architecture

One mobile-first research-line page with five sections:

1. **Current**
   - current scientific state
   - next admissible test
   - forbidden reuse / rescue
   - unresolved conflict banner

2. **Evidence**
   - H1 execution-aware result
   - H1 diagnostics
   - H2 unconditional-touch result
   - H3 preregistered pending test

3. **Timeline**
   - frozen specification
   - H1 result
   - source recovery
   - blocked replay
   - exploratory diagnostics
   - H2 blocked attempt
   - H2 completed replication
   - H3 freeze / waiting state

4. **Data boundaries**
   - consumed H1 sample
   - consumed H2 sample
   - unused Post-H2 final holdout

5. **Decisions / provenance**
   - no-rescue decisions
   - run/source provenance boundaries
   - canonical links

## Visual rules

- mobile-first
- no dashboard-card wall
- off-white background
- strong dark-navy typography
- restrained muted red / blue / yellow accents
- wide whitespace
- visible section rules and hierarchy
- status text must remain readable without color
- no chart if a chart would suggest unsupported precision

## Current-page hierarchy

Top of page should answer in this order:

1. What is this research line?
2. What is currently known?
3. Is there an unresolved conflict?
4. What can happen next?
5. What data must not be reused?

Historical detail comes after those answers.

## Status semantics

Use labels that mirror canonical meanings.

Examples:

- NOT SUPPORTED
- EXPLORATORY
- BLOCKED
- CONSUMED
- FINAL HOLDOUT / UNUSED
- WAITING FOR MATURITY
- SOURCE CONFLICT

Do not use generic green/red success/failure language for scientific conclusions.

## v0.1 data source

Phase 4 v0.1 may use a generated static projection file under `web/data/`.

This projection is noncanonical and must contain canonical GitHub links for every displayed research object.

Automatic index generation belongs to Phase 5. v0.1 should not introduce a build framework merely to avoid a small generated projection.


## Projection consistency and source commit

The static Web projection must record the already-merged canonical research commit from which it was refreshed:

`meta.canonicalSourceCommit`

The public page displays that commit in the authority section. The value identifies the canonical research snapshot used for the projection; it does not make the Web file canonical.

`.github/scripts/validate-research-consistency.mjs` and `.github/workflows/research-consistency.yml` provide a fail-closed structural/projection check. The validator:

- parses structured Horizontal Reaction records and rejects duplicate stable IDs or missing structured ID references;
- requires Result records to keep `execution_status`, `evidence_validity`, and `scientific_status` as independent valid dimensions;
- compares H1/H2/H3 headline state and metrics, dataset roles, H1 source-conflict state, and blocked-record semantics against the static Web projection;
- verifies repository-local Web links and timeline record links;
- fails if canonical Horizontal Reaction records changed after `canonicalSourceCommit`;
- runs negative self-tests proving that a deliberate headline-metric mismatch and a missing canonical link are detected.

This CI is not a scientific recomputation and must not be described as one.

### Update procedure

When canonical Horizontal Reaction research changes:

1. merge and verify the canonical research change first;
2. fresh-read that new `main` commit;
3. refresh the Web projection from that canonical state without changing scientific meaning;
4. set `meta.canonicalSourceCommit` to the already-merged canonical commit;
5. run the consistency CI and public Web validation;
6. only then merge the Web synchronization change.

A canonical-only change is expected to make the consistency check fail until the derived Web projection is refreshed. This is intentional. Do not bypass the failure by pointing `canonicalSourceCommit` at an unmerged or unrelated commit.

## Acceptance criteria

The initial page passes if, on a mobile screen, a reviewer can determine within a short read:

- H1 frozen strategy result was not supported.
- Current H1 diagnostic interpretation is MULTIPLE_DRIVERS / INCONCLUSIVE and has an unresolved historical source conflict.
- H2 unconditional-touch replication was not supported.
- H3 is waiting for maturity and its outcomes must not be accessed yet.
- H1 and H2 samples are consumed.
- H3 final holdout remains unused.
- blocked executions are historical operational events, not negative scientific evidence.
- canonical evidence is one tap away.

## Deferred

Not part of this UI version:

- global search
- full entity browser
- automatic Markdown parser
- cross-line index
- graphs/network visualization
- authentication
- live market data
- broker integration
- MCP
