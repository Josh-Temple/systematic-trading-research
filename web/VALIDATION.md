# Web UI v0.1 Validation

Updated: 2026-09-27
Status: READY_FOR_FIRST_PUBLIC_DEPLOY
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

## External enablement boundary

One repository-admin action remains outside the available GitHub connector / workflow token authority:

Enable GitHub Pages for the repository with GitHub Actions as the publishing source.

After that one-time action, the existing workflow is ready to deploy `web/`.

The workflow listens to:

- pushes to main affecting `web/**`
- changes to `.github/workflows/pages.yml`
- manual `workflow_dispatch`

## Phase 4 remaining checks after first successful deployment

On the public URL:

- Android/mobile visual review
- no unexpected horizontal page overflow
- canonical-link tap test
- CURRENT section readable without scrolling through historical detail first
- SOURCE CONFLICT visible and not mistaken for resolved evidence
- BLOCKED records distinguishable from NOT SUPPORTED scientific results
- CONSUMED vs UNUSED data roles obvious without relying only on color

Phase 4 should not be closed until those checks are completed.
