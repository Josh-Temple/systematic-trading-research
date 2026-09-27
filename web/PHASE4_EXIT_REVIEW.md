# Phase 4 Exit Review — Human-facing Web UI v0.1

Date: 2026-09-28
Phase: 4
Result: PASS
Scope: Horizontal Reaction Strategy v0.1 human-facing derived Web UI

## 1. Exit question

Can a user open the deployed Web UI on a mobile-width browser and distinguish the current research state, evidence, unresolved conflict, data-use boundaries, and historical blocked records while retaining direct paths back to the GitHub research records?

This review evaluates the interface and its navigation behavior. It does not evaluate trading profitability, confirm any hypothesis, resolve the H1 D1-D5 source conflict, or authorize H3 outcome access.

## 2. Deployment evidence

Public URL:

https://josh-temple.github.io/systematic-trading-research/

Relevant successful deployments:

- Actions run `36333169298`: synchronized Web projection after `DEC-HR-004`
- Actions run `36333283754`: deployment after adding the mobile validation workflow

The Pages deployment pipeline completed successfully.

## 3. Current-state and evidence projection

The Web projection shows, as explicit text:

- H1: `NOT SUPPORTED`
- H2: `NO UNCONDITIONAL TOUCH SUPPORT`
- H3: `WAITING FOR MATURITY`
- H1 D1-D5: `SOURCE CONFLICT`
- blocked execution records as `BLOCKED`
- `DATA-HR-001` / `DATA-HR-002`: `CONSUMED HOLDOUT`
- `DATA-HR-003`: `FINAL HOLDOUT / UNUSED`

The H3 projection also records that `DEC-HR-004` froze the exact legacy H2 implementation identity outcome-blind while preserving the Gamma temporal-information limitation.

No H3 touch outcome, CONFIRMED-vs-UNCONFIRMED outcome comparison, primary contrast, or bootstrap was accessed for this Web review.

## 4. Evidence navigation

PR #13 completed the previously identified navigation gaps:

- the header link is labeled `Current summary ↗`, rather than calling the derived `CURRENT.md` canonical evidence;
- diagnostics expose direct links to the current interpretation and source-conflict result;
- history entries link directly to their Specification / Result / Decision records;
- multiple records in one historical entry have separate links.

The public mobile validation observed 2 diagnostic evidence links and 10 timeline links.

## 5. Public mobile validation

Workflow:

`.github/workflows/mobile-web-validation.yml`

Script:

`.github/scripts/validate-public.mjs`

Successful Actions run:

`36333283755`

Artifact:

- name: `mobile-web-validation`
- artifact ID: `10937040439`
- digest: `sha256:99fb138ab10070ca34540daaf8f6013064d46874645ca458920809a3886a027c`

Tested Chromium mobile contexts:

- 360×800
- 390×844
- 412×915
- touch enabled
- mobile mode enabled

All three returned HTTP 200 and passed the automated checks for:

- page-level horizontal overflow
- H1/H2/H3 status text
- source-conflict visibility
- BLOCKED vs NOT SUPPORTED textual distinction
- CONSUMED vs UNUSED textual distinction
- Current section before historical detail
- current-summary tap opening the GitHub research record
- diagnostic evidence links
- timeline evidence links

## 6. Screenshot review

The full-page screenshots from the successful run were downloaded and reviewed.

The 360px rendering was additionally inspected in multiple vertical crops. Observed layout behavior:

- the large title wraps without clipping;
- current H1/H2/H3 rows remain readable;
- the long H2 status wraps inside its bordered label;
- SOURCE CONFLICT remains visually separated from ordinary evidence;
- primary evidence metrics fall into a two-column mobile grid without page overflow;
- H3 FINAL HOLDOUT / UNUSED remains explicit text;
- diagnostic rows remain readable;
- data roles use text as well as color;
- timeline labels and direct record links remain readable;
- authority/freshness information remains visible at the end of the page.

No visual defect was observed that blocks the intended v0.1 research-navigation use.

## 7. Known limitations

This is not a physical-device test.

The browser evidence comes from Playwright Chromium running on a GitHub-hosted Linux runner with mobile viewport, mobile mode, and touch enabled. It does not prove:

- OEM-specific Android font rendering;
- physical-device browser chrome behavior;
- every Android Chrome version;
- device accessibility settings;
- performance on low-memory hardware.

These are normal device-compatibility questions, not unresolved scientific-state questions. A physical Android spot check may be added later if device-specific behavior becomes relevant.

The direct Web-fetch facility available in the chat environment still could not open the GitHub Pages URL. That tool limitation is superseded for Phase 4 browser validation by the successful GitHub-hosted Chromium run, but it remains relevant when interpreting what was directly accessible from this chat runtime.

## 8. Exit assessment

Phase 4 v0.1 exit conditions are satisfied:

- a public human-facing view exists;
- the current research state is presented before historical detail;
- unresolved conflict is visible rather than silently reconciled;
- blocked execution is distinct from negative scientific evidence;
- consumed and unused samples are distinct without color-only encoding;
- direct evidence navigation is available;
- the public page is usable at the tested mobile widths without page-level overflow;
- a repeatable public-site validation path now exists.

Result: **PASS**

Phase 5 may be considered separately from this Web exit. The open repository review item for canonical-record/Web consistency CI remains a separate follow-up and is not implied complete by this Phase 4 result.
