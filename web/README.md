# Web UI

Status: Phase 4 v0.1 implementation

## Purpose

This directory is a derived human-facing view over the canonical research records under `research/lines/`.

It is **not** a second source of truth.

Initial scope:

- Horizontal Reaction Strategy v0.1

## Files

- `index.html` — single-page shell
- `styles.css` — mobile-first visual system
- `app.js` — deterministic rendering from static projection data
- `data/horizontal-reaction-v0.1.js` — derived projection for the current research line

## Authority

Canonical scientific state remains in:

`research/lines/horizontal-reaction-v0.1/`

Every major UI block links back to its canonical GitHub artifact.

The static projection may become stale. If UI text conflicts with canonical research files, the canonical files win.

Automatic projection/index generation is deliberately deferred to Phase 5.

## Local viewing

No build step is required.

Serve this directory with any static HTTP server or deploy it as static files.

Example:

```bash
python -m http.server 8000 --directory web
```

Then open:

`http://localhost:8000/`

## GitHub Pages deployment

A manual-ready workflow is stored at:

`.github/workflows/pages.yml`

Before the first deployment, repository Pages settings must use **GitHub Actions** as the publishing source.

After that, run the `Deploy research web UI` workflow manually.

The workflow publishes only `web/`.

## Phase 4 validation

Before Phase 4 exit:

1. deploy a preview/public instance,
2. review on Android/mobile width,
3. verify every canonical link,
4. verify blocked vs negative-result language,
5. verify consumed vs unused data roles,
6. verify the H1 source conflict is visible without opening raw files,
7. confirm that the page is faster to understand than browsing the raw tree.
