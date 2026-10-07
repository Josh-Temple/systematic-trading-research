# Repository validation

The checks here validate software and research-record consistency. They do not authorize a market experiment, qualify a broker feed, or establish a trading edge.

## Prerequisites

- Node.js 24 for the consistency checks and their synthetic fixtures.
- Python 3.12 for the existing synthetic suites.
- A full-history Git checkout with `refs/remotes/origin/main` available.
- Linux, Bash and `sudo` for the existing process-boundary test only.

For a normal full clone, refresh main with `git fetch origin main`. For a shallow clone, first obtain the missing history with `git fetch --unshallow origin`. Do not replace an unknown or unmerged source commit with `HEAD` to make the check pass.

## Canonical records and Web projection

Run from the repository root:

```sh
npm ci --ignore-scripts
npm run check
```

The npm lockfile pins the validation dependency and its transitive dependency. Installation does not run package lifecycle scripts. `npm test` uses synthetic metadata and temporary Git repositories; `npm run validate` reads the committed Horizontal Reaction record structure and the existing Web summary. It does not fetch prices or recompute market outcomes.

The validator rejects:

- missing or malformed entity frontmatter, invalid IDs, filename/ID mismatch, wrong entity types and line identity;
- duplicate IDs, missing structured references and malformed relations;
- invalid Result status dimensions, disagreement with its Run, and scientific outcomes attached to non-successful executions;
- invalid Run and Diagnostic references;
- cyclic YAML aliases, excessive metadata nesting and canonical symbolic links;
- a missing, non-ancestor or unmerged `canonicalSourceCommit`;
- canonical changes since that source, including staged, unstaged, deleted and newly untracked files;
- the existing checked Web metric/status/link discrepancies and unresolved-conflict mismatches.

This remains a scoped validator for Horizontal Reaction v0.1. It is not complete validation of every research line, every narrative claim or every Web element. `CURRENT.md` remains a derived projection; a new routing entry or a successful workflow does not promote a research state.

## Existing synthetic suites

JP225, from the repository root:

```sh
python research/lines/jp225-ema-timeofday-v0.1/work/integration/run_synthetic_tests.py
```

Autonomous pilot, from `research/pilots/autonomous-research-v0.1/`:

```sh
python -m unittest -v
bash run_process_boundary_test.sh
```

H3 source-preparation mechanics, from `tools/h3-source-preparation/`:

```sh
python -m unittest -v
```

These commands use synthetic fixtures. The pilot unittest suite also contains Phase B mechanics tests; it does not launch an official baseline or AI run. The H3 command does not run `run_h3_once.py` against holdout sources. The JP225 command does not acquire XM data or unlock Discovery/holdout.

## Pages publication

`.github/workflows/pages.yml` first checks the main-branch snapshot with the same locked install and `npm run check`. Only after success does it upload `web/` as the Pages artifact. A separate deployment job depends on that validation job and publishes that artifact. It does not check out another source tree.

Pages and OIDC write permissions belong only to the deployment job. Manual dispatch on a branch other than main does not pass the publication gate. The workflow also runs for relevant canonical, validation and dependency changes, so a canonical-only update cannot silently evade the check.

If validation fails, there is no new publication; the previously deployed site remains available. Follow the existing two-step canonical/projection update procedure in [WEB_UI_V0.1.md](WEB_UI_V0.1.md). A green local check does not prove that remote Actions or production deployment has succeeded.

## Design basis

This extends the existing [repository synthesis](../research/prior-art/SYNTHESIS_V0.2.md), including its DVC and Freqtrade issue/history reviews. In particular, checking the artifact that will actually be published and rejecting uncertain identity follows the recorded distinctions between artifact presence, provenance and scientific validity.

GitHub documents that dependent jobs are skipped when their required job fails: [Using jobs in a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs). The parser remains on the v4 maintenance line, pinned to the published [js-yaml 4.3.2 release](https://github.com/nodeca/js-yaml/releases/tag/4.3.2); this replaces the old unlocked 4.1.0 install. The repository's JSON-schema parser configuration is retained. This dependency update is not a claim that a public-site exploit was reproduced.
