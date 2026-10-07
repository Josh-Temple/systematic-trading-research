# Repository improvement — 2026-10-08

## Scope and source identity

Repository: `Josh-Temple/systematic-trading-research`.

Fresh-read main: `d7532c33a841a0d8c21d1288f39230e47c413894`. The review also read current open PR metadata, branch trees, research principles, the existing prior-art synthesis and validation/deployment code. Main was rechecked before publication and had not moved.

This work improves record validation, publication and routing. It does not change scientific specifications, hypothesis parameters, market results, existing research code identities or research access gates.

## Findings and corrections

| Finding at the reviewed main | Evidence | Correction |
| --- | --- | --- |
| Pages deployment could proceed independently of a failed consistency workflow. | `pages.yml` had no validation step or dependency. | Validate before artifact upload; deployment requires that job and consumes its artifact. |
| Canonical-only changes did not trigger Pages. | Original push path filter covered Web and the Pages workflow only. | Add canonical, schema, validator and locked-dependency paths. |
| New untracked canonical content passed freshness. | An isolated synthetic untracked Markdown addition passed the original `validateSourceCommit`; the fixture was removed afterwards. Original diff covered source commit to HEAD only. | Compare working-tree bytes and list untracked additions, including ignored files inside the canonical scope. |
| Unclosed frontmatter was silently omitted. | The original parser returned null for a synthetic record without a closing delimiter. | Fail with the document path; also reject missing metadata for ID-named records. |
| A misspelled Result type bypassed status validation; Result/Run status conflicts passed. | Both were accepted by the original structure validator using synthetic metadata only. | Validate ID/type/line identity and Result/Run execution consistency. Non-successful runs cannot acquire a scientific outcome. |
| A branch could certify itself by naming an unmerged source commit. | Original freshness check required HEAD ancestry only. | Require source ancestry in fetched `origin/main` as well. |
| Record reference/alias failures could be skipped or become unbounded recursion. | Existing scans only recognized well-formed IDs and had no cyclic-alias check. | Reject malformed relations and cyclic metadata; preserve ordinary shared aliases. |
| The thin index omitted newer branches and proposal entry points. | Current open PR metadata and branch trees contained routes absent from main's index. | Add branch-specific entry links and keep the deferred DataCube route distinct from the free-source priority. |

The same small existing validator is extended; there is no new research framework or status authority. YAML remains on the JSON schema. The dependency install is now locked to `js-yaml` 4.3.2 and `argparse` 2.0.1, with lifecycle scripts disabled. This is not a finding of a reproduced public-site exploit.

The autonomous-pilot workflow label now reflects its actual Phase A/Phase B synthetic test scope, and has a five-minute timeout. No official run command was added.

## Local verification

Environment: Node.js 24.19.0, Python 3.12.14.

| Check | Result |
| --- | --- |
| Clean locked dependency install, `npm ci --ignore-scripts` | PASS |
| New synthetic validator and publication regression fixtures | 27/27 PASS |
| Existing Horizontal Reaction/Web consistency, including its two negative self-tests | PASS; 41 records and 7 Result records |
| Autonomous pilot synthetic unittests | 83/83 PASS |
| JP225 synthetic unittests | 46/46 PASS |
| H3 source-preparation synthetic unittests | 12/12 PASS |
| Workflow YAML parsing | 7/7 PASS |
| JavaScript syntax and `git diff --check` | PASS |
| Branch-specific index entry paths | 7/7 exist in the named fresh-fetched branch trees |
| Existing cross-user process-boundary test | LOCAL_ENVIRONMENT_BLOCKED: creating AF_UNIX socket failed with `PermissionError: [Errno 1] Operation not permitted`; no successful local process-boundary claim |

The process-boundary failure is an execution-environment restriction, not a negative scientific finding. Remote validation will be recorded after the PR workflows finish.

## Boundaries and remaining work

- No new market-price source was requested or downloaded. No formal market experiment or official synthetic baseline/AI run was launched.
- Existing consumed Horizontal Reaction record summaries were read by the unchanged projection comparisons; no market outcome was recomputed. All new fixtures are synthetic.
- Existing market runners, source collectors, frozen specifications and formal holdouts are unchanged.
- The consistency checker remains specific to Horizontal Reaction. Other lines need their own contract-aware checks; this PR does not certify them.
- New Pages gating will take effect after integration into main. No deployment, merge or research-gate promotion is performed by this work.
- A blocked publication leaves the last deployed site available. It cannot make an already published snapshot current without updating the underlying projection.

Follow [VALIDATION.md](VALIDATION.md) for the exact commands and [research/lines/INDEX.md](../research/lines/INDEX.md) for line-specific entry points. The next substantive line work still requires fresh reads of its own source/approval boundaries; this repository-wide maintenance is not a substitute for source qualification.
