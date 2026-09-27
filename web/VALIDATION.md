# Web UI v0.1 Validation

Updated: 2026-09-28
Status: COMPLETE
Scope: Horizontal Reaction Strategy v0.1

## Scientific projection check

Fresh canonical reads were compared against `web/data/horizontal-reaction-v0.1.js`.

Confirmed UI values include:

- H1 trades: 2,685
- H1 mean: -0.201598R
- H1 Profit Factor: 0.660341
- H1 max drawdown: 542.166368R
- H2 primary events: 4,786
- H2 mean: -1.379343686609 bps
- H2 positive rate: 46.9494358546%
- H2 clustered 95% interval: [-1.908681505831, -0.862084588075] bps
- H3: WAITING_FOR_MATURITY
- DATA-HR-001 / DATA-HR-002: CONSUMED_HOLDOUT
- DATA-HR-003: FINAL_HOLDOUT / UNUSED
- H1 source conflict remains explicitly visible

The UI does not resolve the H1 D1-D5 source discrepancy.

## Canonical-link check

Every GitHub canonical reference currently embedded in the projection was fresh-fetched successfully:

- LINE.md
- CURRENT.md
- RES-HR-001
- RES-HR-005
- RES-HR-006
- EXP-HR-007
- SPEC-HR-003-v01
- INT-HR-002
- DATA-HR-001
- DATA-HR-002
- DATA-HR-003
- research-line directory

Result: **12 / 12 accessible**

## Static implementation check

Local static checks:

- `web/app.js`: JavaScript syntax PASS
- `web/data/horizontal-reaction-v0.1.js`: JavaScript syntax PASS
- DOM IDs referenced by app.js but absent from index.html: **0**
- duplicate IDs: **0**

A potential mobile overflow risk from the long H2 status label was corrected by allowing Current-section status tags to wrap on narrow screens.

The diagnostic heading was also changed from a causal-sounding phrase to:

`v0.1の損失要因をどう見ているか`

because the canonical current classification remains `MULTIPLE_DRIVERS / INCONCLUSIVE`.

## Browser-render limitation of integration environment

A local Chromium render was attempted, but the tool runtime blocks both localhost and file URLs with:

`ERR_BLOCKED_BY_ADMINISTRATOR`

Therefore final visual validation must use the deployed public URL / Android browser rather than this container.

This is a test-environment limitation, not a site error.

## GitHub Pages deployment attempts

Workflow:

`.github/workflows/pages.yml`

Action majors were independently confirmed to exist:

- actions/checkout@v4
- actions/configure-pages@v5
- actions/upload-pages-artifact@v4
- actions/deploy-pages@v4

### Run 1

GitHub Actions run:

`36302636970`

Result:

`FAILURE`

Failure step:

`Configure Pages`

Reason:

Pages site did not yet exist.

### Run 2

GitHub Actions run:

`36302666654`

The workflow used:

`enablement: true`

to attempt first-time Pages creation.

Result:

`FAILURE`

Exact GitHub API error:

`Resource not accessible by integration`

This establishes that the repository workflow token can deploy to an existing Pages site but cannot create the Pages site for the first time.

## Pages enablement and successful deployment

The earlier repository-admin Pages enablement boundary was resolved outside the failed workflow attempts.

A later manual deployment succeeded:

GitHub Actions run:

36316165611

Result:

SUCCESS

Fresh GitHub Actions read on 2026-09-28 confirmed the deploy job and all relevant steps completed successfully:

- Checkout: success
- Configure Pages: success
- Upload static site: success
- Deploy: success

Public URL recorded for the deployment:

https://josh-temple.github.io/systematic-trading-research/

In this 2026-09-28 session, the available direct web-fetch tool could not open the public URL, so this entry does not claim a new visual/browser revalidation of the rendered page. The deployment success itself is confirmed from GitHub Actions; Android/mobile visual validation remains separate.

The workflow listens to:

- pushes to main affecting web/**
- changes to .github/workflows/pages.yml
- manual workflow_dispatch

## Public mobile browser validation — 2026-09-28

A reusable GitHub Actions validation was added:

- workflow: `.github/workflows/mobile-web-validation.yml`
- validation script: `.github/scripts/validate-public.mjs`
- successful run: `36333283755`
- artifact: `mobile-web-validation`
- artifact ID: `10937040439`
- artifact digest: `sha256:99fb138ab10070ca34540daaf8f6013064d46874645ca458920809a3886a027c`

The test used the deployed public URL, not a local file or localhost.

Mobile Chromium contexts:

- 360×800
- 390×844
- 412×915
- `isMobile=true`
- `hasTouch=true`

All three checks reported:

- HTTP 200
- title `Horizontal Reaction Strategy v0.1`
- no document/body horizontal overflow
- `SOURCE CONFLICT` present
- `BLOCKED` text present
- `NOT SUPPORTED` text present
- `CONSUMED HOLDOUT` text present
- `FINAL HOLDOUT / UNUSED` text present
- `DEC-HR-004` present
- Current section precedes the historical timeline
- `Current summary ↗` points to `CURRENT.md` and a tap opens the GitHub repository
- 2 direct diagnostic evidence links
- 10 direct timeline evidence links

The generated full-page screenshots were downloaded and visually reviewed. The 360px screenshot was also inspected in vertical sections. The main title, current-state rows, long H2 status, source-conflict panel, H1/H2/H3 evidence, diagnostics, data roles, history, and authority section remain readable without clipping or unexpected page-level overflow.

### Physical-device limitation

This validation is Chromium mobile emulation on a GitHub-hosted runner. It is not a physical Android handset and does not prove device-specific Chrome rendering, OEM font substitution, browser-toolbar behavior, or accessibility behavior on every Android device.

For Phase 4 v0.1, the mobile-browser rendering plus screenshot review is sufficient to close the web implementation phase. A later physical-device spot check can be performed if device-specific behavior becomes relevant; it is not treated as scientific evidence.

## Phase 4 exit

The remaining Phase 4 UI checks are complete for v0.1:

- public deployment: PASS
- mobile-width visual/browser validation: PASS
- no unexpected horizontal overflow: PASS
- current-state-before-history ordering: PASS
- source conflict remains explicit: PASS
- blocked execution vs negative scientific result remains textually distinct: PASS
- consumed vs unused data role remains textually distinct: PASS
- current-summary and evidence navigation links: PASS

Phase 4 result: **PASS**

See `web/PHASE4_EXIT_REVIEW.md`.

This result concerns the human-facing derived interface only. It does not validate the underlying trading hypotheses, resolve the H1 source conflict, or authorize H3 outcome access.
