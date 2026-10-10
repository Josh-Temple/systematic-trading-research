# E — FXNS PR #99 independent acceptance and research-branch integration closure (2026-10-10 JST)

## Decision: MERGED_SCOPED / NO_SOURCE_OR_OUTCOME_PROMOTION

**Only FXNS PR #99 was merged, into `research/fx-news-sentiment-v0.1`, not main.** The specific synthetic-only persisted-JSON duplicate-member repair passed a separately saved B audit and the same-tree CI check. The research remains `UNTESTED / PROPOSED_NOT_FROZEN`, formal prospective cohort `CLOSED`, GDELT `SOURCE_QUALIFICATION_BLOCKED`, and no market outcome, XM/MT5, order or trade permission follows.

### Procedural independent prerequisites

- B: Draft [PR #101](https://github.com/Josh-Temple/systematic-trading-research/pull/101), head `d9ff37d8a927c257e35da9252184a5dfbd88d449`, exact B report Git blob `330b67fa0ec9a94f6f0ed5a8cd26c757bc798796`; only one allowlisted report path `research/lines/fx-news-sentiment-v0.1/work/independent-audit/2026-10-10/duplicate-json-pr99-exacthead/B_FXNS_PR99_EXACT_HEAD_INDEPENDENT_ACCEPTANCE.md`. OPEN/Draft and directly read back. B = `PASS_SCOPED` on PR #99 exact head/tree; B's own offline rerun = `NOT_RERUN`, not a second suite pass.
- D: Draft [PR #102](https://github.com/Josh-Temple/systematic-trading-research/pull/102), head `119239ad86b20578fb9e7559abfd967cf7eeb97a`, report Git blob `7a4a1a124047396557c907419a43b5a92fb31399`, only one report in `research/lines/currency-strength-momentum-v0.1/work/independent-audit/2026-10-10/post-c100-runtime-independent/`. OPEN/Draft and directly read back. It independently audited the saved C [#100](https://github.com/Josh-Temple/systematic-trading-research/pull/100) *after* its creation, giving `BLOCKED / NOT_RERUN / HOLD_NO_MERGE`; this suffices for procedural E start, not for CSM acceptance.
- No post-C new C execution PR was identified through #102. C #100 report head `9d431397932f3ac5fcf781d912212af1cf11eda5`, blob `77ae8da0da43078b12c45e0359ae4ba6f326ffa4` still records `NOT_EXECUTED / BLOCKED_ENVIRONMENT`, testsRun=0 and failure/error/skip `NOT_OBSERVED`.

### Exact FXNS candidate, changed paths and observed CI

- Pre-merge research branch [#63](https://github.com/Josh-Temple/systematic-trading-research/pull/63) head `b1b31e5f1344c86c816f934a695a8583eb1bf4eb`. PR [#99](https://github.com/Josh-Temple/systematic-trading-research/pull/99) pre-merge OPEN/Draft, then E changed Draft to Ready; after re-read it remained OPEN/Ready, base `research/fx-news-sentiment-v0.1` at the same pre-merge head, `mergeable=true`.
- PR #99 candidate exact head `968075ff69509ec5d8b83766b488ba3a691e8e8e`, tree `123f6d539c29f188e489bcc1492b632f5c9514d7`. Independently fetched content/blob: `work/implementation/event_ledger.py` = `3faa396953c7cb951d32d1f3521ea303010e8598`; `work/implementation/test_event_ledger.py` = `e4bf1a3c8ab6d47c86fb92483d71768e87ab3a05`; `work/implementation/2026-10-10/duplicate-json-closure/A_FXNS_DUPLICATE_JSON_RESULT.md` = `0988e7bc4da1f66d0af4e7b4633527446eeea3b2` (all prefixed by `research/lines/fx-news-sentiment-v0.1/`).
- Full paginated PR #99 changed filenames: exactly the **three paths above**, and no workflow, source lock, prompt/schema, manifest, SPEC, gate, `CURRENT.md` or `main` change.
- Existing workflow blob `620581df64cf247c293781389bd7386df391f30e`, `.github/workflows/fxns-gdelt-source-probe.yml`; driver blob `25636eca0b6c282a2f7233064ec9661fc62666c0`, `.github/scripts/fxns_offline_unittest.py`. Full bytes read by E. **Clarification**: workflow includes a `workflow_dispatch` definition, contrary to the old A report wording; **no manual workflow_dispatch was invoked**. Observed CI was automatic `pull_request`, driver uses synthetic-only suites and Python process-local socket denial (not OS isolation).
- Direct Github Actions [run 38006886615](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/38006886615), job `114077610920`: `pull_request`, `head_sha=968075ff...`, completed/success, attempt 1; Python 3.13.16; discovered implementation=85, source-probe=11; `Ran 96 tests`; `failures=0; errors=0; skipped=0; successful=True`, syntax compile success. The two newly added persisted duplicate JSON test methods were each logged `ok`; individual subtest statuses are not separately reported.
- CI checked out temporary merge commit `14f0580c647dfecb7059c125441b06f5759d3833`, parents `b1b31e5f...` + `968075ff...`; its *directly fetched Git tree* is `123f6d539c29f188e489bcc1492b632f5c9514d7`, identical to candidate. B's `PASS_SCOPED` therefore covers the same exact code tree. Initial failed CI attempt on earlier candidate is not recast as PASS.

### Authorized single merge and post-merge readback

- E called only GitHub merge for PR **#99**, method `merge` (non-force), with `expected_head_sha=968075ff69509ec5d8b83766b488ba3a691e8e8e`. GitHub replied `merged=true` and merge commit `24ef9c37e6255126a957f38cfa7470cd150ed594`.
- Post-merge PR #99 is CLOSED/merged; new research head on PR #63 is `24ef9c37e6255126a957f38cfa7470cd150ed594` while #63 itself remains OPEN/Draft against main. Direct Git commit: two parents `b1b31e5f...` / `968075ff...`; tree `123f6d539c29f188e489bcc1492b632f5c9514d7`, matching audited/CI-tested tree.
- Pre/post research-branch compare: exactly the same three changed paths, ahead by 3 commits, no unexpected code/source/workflow paths. `main` remained at `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`.
- Post-merge commit-filtered pull-request workflow listing showed no new associated run. **POST_MERGE_NOT_RERUN**; the directly observed 96-test success belongs to pre-merge candidate / identical-tree CI, not a new post-merge suite.
- This E branch and separate Draft receipt are report-only evidence and must not be merged as part of #99.

### Open risks and prohibitions

- The duplicate-key defense rejects repeated members in actual persisted raw JSON via `object_pairs_hook`; nested and blocked synthetic cases and formal CLOSED guards have method-level CI evidence. It does **not** resolve the same event ID simultaneously existing in `.json` and `.blocked.json`. PR #94's fail-closed/single-canonical/priority alternatives await human approval and migration/restart/readback design.
- A coherent privileged whole-record + SHA-256 rewrite remains possible without separately controlled signing, append-only storage, custody and OS ACLs. Synthetic CI is not production security assurance.
- GDELT decision [#89](https://github.com/Josh-Temple/systematic-trading-research/pull/89) remains `SOURCE_QUALIFICATION_BLOCKED`: point-in-time/first-seen/completeness/UTC endpoints/revisions/08:00 cutoff unresolved; do not change provider/fixed query or elevate without human decision.
- No #87/#88 merge, no source or cohort promotion, no real headline classification/ECB `OBS_VALUE`, EURJPY market history, returns, XM/MT5/quotes/order/trading, or outcome access. FXNS formal cohort remains CLOSED. CSM #90/#34/#37/#53 remain unmerged and independently HOLD.

**E disposition: FXNS_SCOPED_MERGED; SCIENTIFIC_AND_SOURCE_HOLD.**