# Handoff — Web evidence links / projection CI — 2026-09-28

Status: **IN PROGRESS — PR #9 OPEN, CI FAILING**

Repository: `Josh-Temple/systematic-trading-research`

## Fresh state at handoff

- `main` HEAD: `f6e80707511ff4fa1622a439100b3ca97b11c5ea`
- Working branch: `followup/web-evidence-ci-20260928`
- PR: #9 — **Close web evidence links and add projection consistency CI**
- PR head at handoff: `9db17635a4863b7cfa9ce6589d119a4671cc8268`
- PR is open and GitHub reports it as mergeable.
- Do **not** merge yet: the new validation workflow is failing.

## What was completed before this handoff

### 1. H3 implementation identity audit is already on main

The repository already contains:

`research/lines/horizontal-reaction-v0.1/H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md`

This audit recovered the exact historical `run_v01.py` and recorded the following blocking issues before H3 execution:

1. Legacy Gamma temporal semantics differ from the frozen prose. The executed generator includes the candidate bar close-change in its cumulative Gamma calculation.
2. Legacy Gamma depends on an expanding M1 history prefix, so a local 60-bar warm-up is not sufficient to reproduce the historical implementation.
3. The legacy same-confirmation-bar ambiguity rule is not mapped unambiguously into H3's required binary CONFIRMED / UNCONFIRMED classification.

The audit deliberately did **not** access DATA-HR-003 outcomes, group comparisons, the primary contrast, or bootstrap results.

H3 must therefore remain blocked until those pre-outcome implementation/specification questions are resolved.

### 2. Phase 4 public deployment state is already updated on main

README, ROADMAP, and `web/VALIDATION.md` already record that:

- GitHub Pages first public deployment succeeded.
- Public URL is `https://josh-temple.github.io/systematic-trading-research/`.
- Phase 4 remains open because Android/mobile visual review and the Phase 4 exit review are not complete.

### 3. Web evidence-link improvements are implemented in PR #9

PR #9 currently changes:

- `web/index.html`
- `web/app.js`
- `web/styles.css`
- `web/data/horizontal-reaction-v0.1.js`

Implemented behavior:

- Header link formerly labelled `Canonical` is now labelled `現在の要約` because it points to `CURRENT.md`, which is a derived current projection rather than a canonical Result.
- Diagnostics now link directly to:
  - `INT-HR-002`
  - `RES-HR-005`
- Timeline entries now link to their individual Specification / Result / Decision records instead of showing only plain IDs.
- The next H3 test links directly to `EXP-HR-007`.
- The web projection records the canonical snapshot commit:
  `f6e80707511ff4fa1622a439100b3ca97b11c5ea`
- The snapshot commit is displayed in the public UI.

The scientific distinctions must remain unchanged:

- SOURCE CONFLICT remains unresolved and visible.
- BLOCKED execution must not be presented as a negative scientific result.
- NOT SUPPORTED remains distinct from BLOCKED.
- CONSUMED and UNUSED dataset roles remain explicit.

## Projection consistency CI added in PR #9

New files:

- `scripts/validate_research_projection.py`
- `.github/workflows/research-projection.yml`

Intended checks:

- parse research entity YAML/frontmatter;
- reject duplicate IDs;
- reject missing `relations.target` references;
- require Result entities to keep separate:
  - `execution_status`
  - `evidence_validity`
  - `scientific_status`;
- verify embedded GitHub research-record links exist;
- compare web H1/H2/H3 status and headline metrics against canonical records;
- compare DATA-HR-001 / 002 / 003 roles and consumption state;
- require the H1 source conflict to remain visible and unresolved;
- fail if canonical Horizontal Reaction files changed after the web projection's recorded `sourceCommit`;
- run an intentional H2 event-count mutation and require the validator to reject it.

The validator explicitly states that a PASS does **not** establish scientific validity, computational reproducibility, or absence of temporal leakage.

## Current blocker: CI failure

Latest workflow run at handoff:

- Workflow: `Validate research projection`
- Run ID: `36330794270`
- Run number: 2
- Conclusion: **failure**
- Failed step: `Validate canonical records and web projection`
- The later intentional-mutation step was skipped because the baseline validation failed first.

Immediately before this run, a parsing bug in the H2 95% CI check was fixed:

- previous condition incorrectly expected at least 3 parsed numbers;
- current code expects at least 2.

Despite that fix, baseline validation still fails.

The GitHub job metadata available in this session identified the failing step, but did not return usable job-log text. Therefore the exact remaining validator error is **not yet established**. Do not guess the cause.

## Recommended next actions

1. Fresh-read `main` and PR #9 before continuing.
2. Inspect the failed CI run `36330794270` or run `scripts/validate_research_projection.py` against PR #9 locally / in an execution environment that exposes stdout.
3. Fix only the concrete validator defect or genuine canonical/web mismatch revealed by the output.
4. Re-run CI and require both:
   - baseline canonical/web state => PASS;
   - intentional H2 metric mutation => validator FAIL, followed by restored baseline => PASS.
5. Review PR #9 diff again for accidental changes to scientific meaning.
6. If CI passes, update `docs/REVIEW_FOLLOWUP_2026-09-27.md`:
   - item 2 (projection consistency CI): mark complete only after the tests above pass;
   - item 3 (web evidence links): mark implementation complete, while preserving Android/mobile visual review as a separate Phase 4 requirement.
7. Merge PR #9 only after CI is green.
8. After merge, confirm Pages redeploy succeeds and then perform/record the remaining Android/mobile visual review before closing Phase 4.

## Boundaries for the next session

Do not:

- access H3 outcomes before maturity + source gate and the implementation-identity blockers are resolved;
- silently change Gamma semantics or generator history and call it a reproduction;
- infer a CONFIRMED / UNCONFIRMED mapping for the same-confirmation-bar ambiguity without a pre-outcome source or explicit human decision;
- resolve the H1 D1-D5 source conflict by choosing one historical source without evidence;
- treat CI success as scientific validation;
- merge PR #9 while its validation workflow is failing.

## Relevant records

- Review follow-up: `docs/REVIEW_FOLLOWUP_2026-09-27.md`
- H3 implementation audit: `research/lines/horizontal-reaction-v0.1/H3_IMPLEMENTATION_IDENTITY_AUDIT_2026-09-28.md`
- Web validation: `web/VALIDATION.md`
- H3 specification: `research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md`
- H3 experiment: `research/lines/horizontal-reaction-v0.1/experiments/EXP-HR-007.md`
- H3 dataset: `research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-003.md`
- PR #9: `https://github.com/Josh-Temple/systematic-trading-research/pull/9`
