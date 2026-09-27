# Handoff — Horizontal Reaction H3 / Web UI / Consistency CI

Date: 2026-09-28 JST  
Status: PAUSED_BY_USER  
Repository: `Josh-Temple/systematic-trading-research`  
Authoritative branch: `main`  
Fresh-read main at handoff: `c85f53f638d137b19bac0c72ca377fbeb1347983`

## 1. Purpose

This handoff records the stop point for the Horizontal Reaction H3 implementation-identity work, the human-facing Web UI work, and the canonical-record/Web consistency CI work.

Do not use this file as the current-state authority in a future session. Fresh-read `main` first, then use the canonical research records listed below.

A separate handoff exists for the Autonomous Research Pilot:

- `docs/HANDOFF_2026-09-28_AUTONOMOUS_RESEARCH_PILOT.md`

Keep that track separate from Horizontal Reaction H3. The current `main` commit `c85f53f638d137b19bac0c72ca377fbeb1347983` adds that autonomous-pilot handoff on top of the Horizontal/Web work completed here.

## 2. Current repository stage

Fresh-read `README.md` and `docs/ROADMAP.md` show:

- Phase 0 — Foundation: COMPLETE
- Phase 1 — Prior repository research: COMPLETE
- Phase 2 — Knowledge Base v0.1: COMPLETE
- Phase 3 — Horizontal Reaction pilot migration: COMPLETE
- Phase 4 — Human-facing Web UI: COMPLETE
- Phase 5 — Index and retrieval: PLANNED

The repository review follow-up is now marked complete:

- `docs/REVIEW_FOLLOWUP_2026-09-27.md`

## 3. Current Horizontal Reaction scientific state

Canonical current projection:

- `research/lines/horizontal-reaction-v0.1/CURRENT.md`

### H1

- `HYP-HR-001`: frozen execution-aware strategy was NOT SUPPORTED on the consumed 2026H1 sample.
- `DATA-HR-001`: CONSUMED_HOLDOUT.
- H1 D1-D5 exploratory sources still contain an unresolved historical conflict.
- Current integrated H1 diagnostic label remains `MULTIPLE_DRIVERS / INCONCLUSIVE`.
- The conflict is preserved in `RES-HR-005`; do not silently reconcile it.

### H2

- `HYP-HR-002`: `NO_UNCONDITIONAL_TOUCH_SUPPORT`.
- `DATA-HR-002`: CONSUMED_HOLDOUT.
- The earlier blocked H2 attempt remains a separate operational record and is not the scientific negative result.

### H3

- `HYP-HR-003`: still `WAITING_FOR_MATURITY`.
- `DATA-HR-003`: `FINAL_HOLDOUT`, `UNUSED`.
- There is no H3 Run or Result.
- No H3 touch outcome, CONFIRMED-vs-UNCONFIRMED outcome comparison, primary contrast, or bootstrap was accessed in this work.

The old source-preparation handoff recorded 2026-10-01 as the earliest possible maturity date, conditional on the next six weekdays passing the frozen structural gate. That is not a guarantee. In any future session, fresh-read the source-preparation state instead of assuming maturity from the calendar.

## 4. H3 implementation identity resolution

PR #12:

- title: `Freeze H3 implementation identity before outcome access`
- merged: YES
- merge commit: `e494ffde9072abe71cc8323828699d70ce95f8e2`

New canonical Decision:

- `research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-004.md`

Audit record:

- `research/lines/horizontal-reaction-v0.1/H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md`

### Frozen implementation reference

H3 uses the exact recovered H2 legacy generator:

- file identity: `run_v01.py`
- SHA-256: `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`

The legacy generator's Gamma implementation includes the candidate-bar Close change. This conflicts with the prose statement that candidate-minute calculations use only observations strictly before the candidate minute.

That mismatch was not erased or silently corrected.

For H3 v0.1:

- preserve the exact legacy generator bytes;
- preserve the temporal-information limitation explicitly;
- do not reinterpret an eventual H3 result as proof that the generator is leakage-free or directly live-executable.

### Generator history

The exact H2 M1 generator input through 2026-07-09 is the fixed prefix:

- first context date: 2025-12-31
- H2 input count: 135 M1 files
- 75 pre-touch context files plus 60 selected H2 sessions

For H3 preparation:

- retain that prefix unchanged;
- append later valid first-party Dukascopy BID M1 files chronologically before selected-session filtering;
- do not reset expanding Gamma at 2026-07-10;
- never choose history inclusion based on H3 touch identity, confirmation status, return, contrast, or any other outcome.

### Same-confirmation-bar handling

The recovered generator first creates confirmation events, then removes same-confirmation-bar dual confirmations from the clean execution-event list as execution ambiguity.

H3 classification is not execution replay.

For H3:

- if the original confirmation condition is mechanically satisfied, the touch is `CONFIRMED`;
- the later same-confirmation-bar execution-ambiguity filter does not turn it into `UNCONFIRMED`;
- same-confirmation-bar occurrence may be recorded separately for auditability.

## 5. H3 hard gate that remains closed

Do not create an H3 Run or access H3 outcomes until all existing gates pass.

Required before outcome access:

1. fresh-read the current H3 preregistration and source-preparation handoff;
2. freeze the first 60 structurally eligible UTC weekdays from 2026-07-10;
3. use first-party Dukascopy source only;
4. pass the M1/Tick source-identity gate;
5. persist and read back exact sample/source hashes;
6. preserve the frozen seed `20260913` and 10,000-replication bootstrap rule;
7. confirm no prior analysis of the exact H3 outcome was performed.

Until then, allowed work is outcome-blind only:

- source acquisition;
- hashes/manifests;
- structural eligibility;
- sample freeze preparation;
- code preparation consistent with `DEC-HR-004`.

## 6. Web UI work completed

PR #13:

- title: `Sync web projection with H3 implementation decision`
- merge commit: `700398a24655c562df74df779248dc7465a10d8f`

Changes included:

- synchronized Web projection with `DEC-HR-004`;
- changed the header link label from `Canonical` to `Current summary` because `CURRENT.md` is a derived projection;
- added direct H1 diagnostic links to `INT-HR-002` and `RES-HR-005`;
- made timeline record IDs direct links to their canonical records.

PR #14:

- title: `Add reproducible public mobile web validation`
- merge commit: `f4ea285755cc81e59334aeb6f60a1a5dea63d4d0`

Added:

- `.github/workflows/mobile-web-validation.yml`
- `.github/scripts/validate-public.mjs`

The public URL is:

https://josh-temple.github.io/systematic-trading-research/

Validation covers Chromium mobile contexts:

- 360×800
- 390×844
- 412×915
- mobile mode
- touch enabled

It verifies:

- HTTP 200;
- no page-level horizontal overflow;
- H1 / H2 / H3 status text;
- SOURCE CONFLICT visibility;
- BLOCKED vs NOT SUPPORTED textual distinction;
- CONSUMED vs FINAL HOLDOUT / UNUSED distinction;
- Current section before history;
- current-summary navigation;
- diagnostic evidence links;
- timeline evidence links.

Full-page screenshots were also reviewed.

Physical Android hardware was not used. This limitation is recorded rather than treated as resolved.

## 7. Phase 4 exit

PR #15:

- title: `Close Phase 4 human-facing web UI`
- merge commit: `78a3f335a6c66bcfda605f53435d3ec72cde0743`

Exit review:

- `web/PHASE4_EXIT_REVIEW.md`

Validation record:

- `web/VALIDATION.md`

Current result:

- Phase 4: COMPLETE / PASS

This means the derived human-facing interface passed its v0.1 deployment/navigation/mobile-width checks.

It does not mean:

- H1/H2 hypotheses are scientifically valid;
- H1 source conflict is resolved;
- H3 is executable;
- physical Android compatibility is exhaustively proven.

## 8. Fail-closed canonical/Web consistency CI

PR #16:

- title: `Add fail-closed research/Web consistency CI`
- merge commit: `11e9bcdd1d1ef7189a5abed6ccaa24a22be5e39a`

Added:

- `.github/workflows/research-consistency.yml`
- `.github/scripts/validate-research-consistency.mjs`

The validator checks:

- structured YAML/frontmatter parsing;
- stable-ID duplicates;
- structured ID reference targets;
- independent Result fields:
  - `execution_status`
  - `evidence_validity`
  - `scientific_status`
- H1/H2/H3 projected status and selected headline metrics;
- DATA-HR-001 / 002 consumed roles;
- DATA-HR-003 final-holdout / unused role;
- unresolved H1 source conflict;
- blocked Result semantics;
- repository-local Web evidence links;
- timeline record-to-path mapping.

It also contains negative self-tests:

- deliberate H1 trade-count mismatch must be rejected;
- deliberate missing canonical link must be rejected.

### Web source commit mechanism

`web/data/horizontal-reaction-v0.1.js` now records:

- `meta.canonicalSourceCommit = 78a3f335a6c66bcfda605f53435d3ec72cde0743`

The public authority section displays that commit.

The consistency validator fails if canonical Horizontal Reaction records changed after the recorded source commit.

This is intentionally fail-closed.

### Required update sequence after future canonical research changes

1. merge canonical research changes first;
2. fresh-read the new `main`;
3. refresh the derived Web projection from that exact canonical state;
4. set `meta.canonicalSourceCommit` to that already-merged canonical commit;
5. run research/Web consistency CI;
6. run public mobile validation when Web files changed;
7. merge the Web synchronization update.

A temporary consistency failure after a canonical-only research merge is expected until the derived Web projection is synchronized. Do not bypass it by pointing the source commit at an unmerged or unrelated commit.

The consistency CI is not a scientific recomputation.

## 9. Latest verified Actions state

The final main commit containing PR #16 is:

- `11e9bcdd1d1ef7189a5abed6ccaa24a22be5e39a`

All three workflows on that commit completed successfully:

- `Validate research and web consistency`
  - run `36334214662`
  - SUCCESS
- `Deploy research web UI`
  - run `36334214627`
  - SUCCESS
- `Validate public mobile web`
  - run `36334214633`
  - SUCCESS

The current `main` later advanced to `c85f53f638d137b19bac0c72ca377fbeb1347983` only by adding the separate Autonomous Research Pilot handoff document. That docs-only commit did not trigger these Web/Horizontal workflows.

## 10. Repository review follow-up

File:

- `docs/REVIEW_FOLLOWUP_2026-09-27.md`

Current status:

- COMPLETE

Its four work items are now recorded complete:

1. H3 execution implementation identity;
2. canonical/Web consistency CI;
3. Web evidence navigation;
4. README / public / validation state.

Do not infer that every possible repository improvement is complete. This only closes the specific review follow-up.

## 11. Open PRs observed at handoff

Fresh read found these open PRs:

### PR #8

- `Add canonical-to-Web projection validation`
- based on older main `f6e807...`
- mergeable: false at handoff

### PR #9

- `Close web evidence links and add projection consistency CI`
- based on older main `f6e807...`
- mergeable: false at handoff

PR #8 and #9 substantially overlap the functionality already merged through PR #13 and PR #16. Do not merge or close them from this handoff alone; fresh-read their diffs against current main first. They are likely cleanup candidates.

### PR #11

- `Prepare official Phase B non-AI baseline execution`
- separate Autonomous Research Pilot track
- mergeable: true at handoff

Do not modify PR #11 as part of Horizontal Reaction H3/Web continuation unless explicitly working on the autonomous-pilot track.

## 12. Clean restart procedure

When this track is resumed:

1. fresh-read current `main` and record its SHA;
2. read:
   - `docs/RESEARCH_PRINCIPLES.md`
   - `docs/KNOWLEDGE_BASE_V0.1.md`
   - `docs/ROADMAP.md`
   - `docs/REVIEW_FOLLOWUP_2026-09-27.md`
   - `research/lines/horizontal-reaction-v0.1/CURRENT.md`
   - `research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-004.md`
   - `research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md`
   - `research/lines/horizontal-reaction-v0.1/experiments/EXP-HR-007.md`
   - `research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-003.md`;
3. fresh-read the Drive H3 preregistration and source-preparation handoff before deciding whether H3 has matured;
4. if the 60-session sample is not frozen or source gate is not PASS, continue outcome-blind preparation only;
5. if both gates are genuinely satisfied, verify exact sample/source hashes and the frozen implementation identity before any outcome access;
6. preserve `DATA-HR-003` as unused until the authorized outcome run actually occurs;
7. if working on repository infrastructure rather than H3, Phase 5 is the next planned roadmap phase;
8. before new Web work, inspect PR #8/#9 against current main and decide whether they should simply be closed as superseded.

## 13. Boundaries to preserve

Do not:

- reuse `DATA-HR-001` or `DATA-HR-002` for new tuning/search;
- access H3 outcomes early;
- silently fix the legacy Gamma mismatch inside H3 v0.1;
- reset H3 generator history at 2026-07-10;
- convert same-confirmation-bar execution ambiguity into `UNCONFIRMED`;
- substitute a different data provider;
- impute missing prices;
- treat Web CI as scientific validation;
- treat physical Android validation as completed;
- mix the Autonomous Research Pilot's Phase B authority with H3 authority;
- place broker/live trades.

## 14. Stop point

The user requested that work stop and a handoff be saved.

At this stop point:

```text
Horizontal Reaction H1 = negative scientific result on consumed H1 sample
H1 diagnostic source conflict = unresolved and preserved
Horizontal Reaction H2 = NO_UNCONDITIONAL_TOUCH_SUPPORT on consumed H2 sample
H3 = WAITING_FOR_MATURITY
DATA-HR-003 = FINAL_HOLDOUT / UNUSED
H3 implementation identity = frozen outcome-blind by DEC-HR-004
Phase 4 Web UI = COMPLETE / PASS
Research/Web fail-closed consistency CI = merged and passing
Repository review follow-up = COMPLETE
Next scientific action = fresh-read maturity/source state; keep H3 outcomes closed until gates pass
Next roadmap infrastructure phase = Phase 5, only if intentionally chosen
```
