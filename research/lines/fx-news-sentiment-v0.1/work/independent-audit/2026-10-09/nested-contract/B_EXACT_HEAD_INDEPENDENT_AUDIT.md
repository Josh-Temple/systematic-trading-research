# B — FXNS PR #82 exact-head independent synthetic contract audit
Date: 2026-10-09 JST

## Independent disposition and narrow meaning
**PASS_SCOPED — the specified persisted nested classification/score/decision consistency repair is present, and the complete offline synthetic CI passed at the identical candidate tree.**

**Independent local Python rerun: NOT_RERUN** (the local checkout attempt `git ls-remote` failed DNS resolution for github.com). This judgment is based on direct GitHub code/blob/diff and job-log inspection, **not** on an independently executed full Python suite, live source qualification, forensic disk provenance, or author approval. The limits and additional hardening notes below do not open any scientific or trading gate.

- Audited new A candidate: [PR #82](https://github.com/Josh-Temple/systematic-trading-research/pull/82), OPEN/DRAFT, head **`c8c2d3bb6024c35426c10b0e6810857a219ab110`** (`work/fxns-nested-contract-fix-20261009-a`), base `research/fx-news-sentiment-v0.1` at **`202ee37d0cd3f9838b153ea361dfdeba5244a271`**.
- Previous full candidate: [PR #74](https://github.com/Josh-Temple/systematic-trading-research/pull/74), still OPEN/DRAFT, fixed head `9ebfc57dd4060825da189b196dd044b6ffaead4f`. Historical independent audit [#77](https://github.com/Josh-Temple/systematic-trading-research/pull/77) was PARTIAL_WITH_GAPS; previous E receipt [#79](https://github.com/Josh-Temple/systematic-trading-research/pull/79) was HOLD_NO_MERGE.
- Scope: actual records under `research/lines/fx-news-sentiment-v0.1/work/implementation/`; synthetic fixtures only. No GDELT live calls, XM/MT5, real news classification, market price/outcome, returns, trades, orders, or human freeze.

## 1. Exact Git identity and allowlist verification
GitHub complete PR file listing: #74 = **8** paths, #82 = **9** paths (old 8 plus A receipt). Fresh old-HEAD -> new-HEAD Git compare: **four commits ahead / zero behind**, with **exactly three file deltas**:
1. `work/implementation/event_ledger.py` (+31 lines; current blob `752ccd476ac8700187797a39d4efcdcf73072b8f`).
2. `work/implementation/test_event_ledger.py` (+101 lines; current blob `8995a19a48330cc8e555ad699f1d63a9481a9612`).
3. `work/implementation/2026-10-09/A_NESTED_CONTRACT_REPAIR_RESULT.md` (added; current blob `6c8b8bd1c461c4843ac9d9236fedbe910d7c70ac`).

All other #74-derived paths (source-probe code/tests/record, XM blocked readiness record, older independent audit and implementation record) are **byte-identical in the #74 and #82 Git trees**. Comparing #63/#74/#82 Git trees, the following baseline blobs are identical in all three: `CURRENT.md`, `SOURCE_CONTRACT.md`, `specifications/SPEC-FXNS-001-v01.md`, `work/PROMPT_v0.1.txt`, `work/PROMPT_MANIFEST_v0.1.json`, `work/OUTPUT_SCHEMA_v0.1.json`, and both historic GDELT 200/429 `response.raw` and `manifest.json` files. No SPEC, source contract, prompt/schema, raw/manifest, negative report, workflow, or real-market-data edits. This is Git blob identity, **not external data authenticity**.

## 2. Exact-head CI evidence (read logs, not badge)
- [Run 37859613854](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37859613854), job **113591953497** `fxns-synthetic-offline`: **completed/success**. GitHub workflow-run metadata shows `head_sha=c8c2d3bb6024c35426c10b0e6810857a219ab110`, PR #82, and base `202ee37d0cd3f9838b153ea361dfdeba5244a271`.
- Important checkout nuance: Actions actually checked out synthetic PR merge commit `87d9364995e6adb02553c33f6c88693bd56b97a3`, not the bare head. **Both commit Git tree SHA are exactly `570ef3d713a5aa55aab8c6758518595329697933`**, so the test bytes are identical to the audited head.
- Direct job log: Python **3.13.16**; `FXNS_OFFLINE_SUITE: implementation, discovered=77`; `source-probe, discovered=11`; `FXNS_OFFLINE_TOTAL_DISCOVERED: 88`; `Ran 88 tests`; `run=88; failures=0; errors=0; skipped=0; successful=True`; both compileall commands completed and job succeeded.
- Current `.github/workflows/fxns-gdelt-source-probe.yml` (misleading legacy filename, declared name “FXNS offline synthetic validation”) uses Python setup, `.github/scripts/fxns_offline_unittest.py` and `compileall` only. Driver denies standard Python socket connections before loading tests. **Process-local monkeypatch is not OS-level isolation against malicious code.** Neither source acquisition nor XM step appears in workflow.
- Prior evidence retained, not overwritten: [run 37798966613](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798966613) **83/83 success on old #74 SHA**, and earlier [run 37798633932](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798633932) **failure: 83 tests, one fixture error**. These older runs are not the present fix's proof.

## 3. Independent static review vs CI-observed adversarial fixtures
The existing `prompt_contract.validate_batch` rejects JSON duplicate keys, non-dict or additional/missing fields, non-string values, wrong record IDs, invalid EUR/JPY sentiment and reason enums, and inconsistent `NOT_MENTIONED` reason. At audited #82 HEAD, both `write_synthetic_event` and `verify_synthetic_event` call `_validate_synthetic_record`. Its new 31 lines:
- Reparse *persisted* `classification_raw` against the saved input-ID sequence using `validate_batch`; require exact equality to saved `classification_parsed` (prevents writer bypass, extra nested keys and rehashed raw/parsed divergence).
- Recompute `daily_scores(reparsed)` and `pair_action` using **unchanged** deterministic functions; require exact EUR/JPY numeric, finite (non-bool) stored scores and matching decision and `is_no_trade`. No new tolerance, threshold, query, currency, pair, model, or freeze decision.

The A-generated fixtures were **observed to PASS on exact-tree CI**, not independently rerun by B: malformed JSON; raw/parsed nested `market_outcome`; mismatched/missing parsed keys; invalid reason; shifted IDs; nested real URL; altered, bool, string, NaN, infinity, oversized scores; decision disagreeing with score; rehashed NO_TRADE -> direction. Valid LONG/NO_TRADE round trips were green, so this fix did not obviously reject the tested valid baseline events. The single-test-method count understates the adversarial subtests; CI's total 88 is the actual unittest-case count, not a per-subtest total.

Additional direct static controls observed:
| Guard | Finding and limit |
| --- | --- |
| NO_TRADE and identical event ID | `file.open("xb")` exclusive creation; prior valid alternate-decision same-ID test remains in 88-case suite. Blocks that writer's overwrite, not a privileged file rewrite. |
| Blocked preflight receipt | Separate exact blocked-receipt keys; decision and NO_TRADE flag must both be null. Rehashed blocked receipt retaining blocked type with forged decision is rejected in existing tests. |
| Synthetic source and real fields | Event record, source and model key sets are exact; synthetic reference scheme and `.invalid` URL restrictions are visible. Additional event-record price fields and real source URLs rejected by targeted CI tests. |
| Formal event/outcome | `COHORT_STATE = "CLOSED"`; `issue_formal_event` and `associate_market_outcome` unconditionally throw `EventBlocked`. No formal issuance or outcome join entry switch. |
| Future behavior | Not tested here. Neither real SOURCE PASS nor formal cohort or outcome permission follows from the synthetic suite. |

**No remaining bypass of the specifically targeted nested raw/parsed/score/decision contract was identified in the reviewed code.** This is a bounded static finding, not a proof of complete security.

## 4. Residual limitations, review notes, and separate prerequisites
- **Provenance A-C-05 remains out of scope**: the A fixture deliberately replaces a complete syntactically and semantically valid synthetic record with another valid record plus a new SHA-256, and readback succeeds. Ordinary record hash and exclusive create do not authenticate authorship or protect against privileged disk rewriting. **Do not claim tamper-proof evidence or source approval.**
- **Envelope strictness follow-up**: `verify_synthetic_event` verifies `payload["record"]` and `payload.get("record_sha256")`, but does not assert that the *outer envelope* has only those two keys. An unexpected field at this outer layer may therefore be ignored instead of rejected, even while all audited event-record and nested fields are strictly validated. This is a static additional hardening observation (no fixture independently executed), not an identified way to change the returned validated decision without also constructing a semantically coherent record. Consider an explicitly scoped hardening test before relying on file-envelope rejection as a security claim.
- A `.blocked.json` and a `.json` for the same event ID use distinct filenames; O_EXCL is per path. No cross-file event-state uniqueness/provenance guarantee is claimed. Separate design decision required before any operational ledger.
- Independent Python execution **NOT_RERUN** due to DNS failure; CI logs prove GitHub execution only. GitHub tree, author provenance, protected disk, OS sandbox, trusted key, and approval systems are not certified by this audit.
- GDELT is **`SOURCE_QUALIFICATION_BLOCKED`**; [PR #81](https://github.com/Josh-Temple/systematic-trading-research/pull/81) documents first-seen/on-time/completeness limitations, not source PASS. XM `LOCAL_XM_EXECUTION_REQUIRED` remains explicitly deferred. No new source, query, API access, or source approval.

## 5. E handoff and conditions
**B recommendation: `PASS_SCOPED` for the repaired synthetic persisted nested contract at exact PR #82 SHA `c8c2d3bb6024c35426c10b0e6810857a219ab110`.** Eligible for **E's separate conditional consideration** of integrating **#82 only** into `research/fx-news-sentiment-v0.1` if the candidate/branch head is still exact, diff/allowlist and *same-tree* offline CI remain valid, and E explicitly accepts the scoped residual provenance/envelope limitations. **Do not merge old #74 separately.** On any head/tree change, B evidence cannot be reused without re-audit. If E requires strict outer-envelope authenticity or filesystem adversary protection as acceptance criteria, HOLD and request an expressly scoped hardening Wave instead.

Regardless of E's source-code decision: **scientific `UNTESTED`, `PROPOSED_NOT_FROZEN`, formal cohort `CLOSED`, `SOURCE_QUALIFICATION_BLOCKED`, XM collection deferred, market outcome access forbidden, no live/paper trading, no final Packet D or human freeze**. Neither the report nor a future merge grants such authorization.

## 6. What B actually did
**Executed**: direct GitHub PR/commit/changed-path/tree/source-code/file identity queries; read actual exact-candidate job results and full logs; traced writer/readback functions and existing synthetic fixtures; compared old negative evidence; local `git ls-remote` checkout attempt (DNS failure).
**Not executed**: independent Python suite or new tests, new API probe, XM/MT5 collector, real LLM classification, market-outcome calculations, broker/order activity, or research-branch/main merges.
**Write scope**: one B report only under `work/independent-audit/2026-10-09/nested-contract/**`, on its own Draft PR from current FXNS research branch. No code, workflow, gate, source fixture, or saved evidence changes.
