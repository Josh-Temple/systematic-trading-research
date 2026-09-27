# Human-facing Web UI v0.1

Updated: 2026-09-27
Status: IMPLEMENTING
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
