# D — FX News Sentiment 5-role Wave independent pre-outcome audit (2026-10-08)

## 1. Result / scope

**Disposition: PARTIAL_WITH_GAPS; C requires a narrow guard before unrestricted E integration.**

This is the **D role audit of A/B/C worker changes**, **not** the formal pre-outcome Packet D approval required by FXNS Specification, not an outcome-access authorization, and not an execution-quality or profitability evaluation.

Auditor's fresh-read target (at inspection):
- Repository: `Josh-Temple/systematic-trading-research`; main `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`.
- Base FXNS [PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63), `research/fx-news-sentiment-v0.1`, HEAD `8d3771921fbab88ea56b913f9d6fe8d62236961c`, OPEN/DRAFT.
- A [PR #68](https://github.com/Josh-Temple/systematic-trading-research/pull/68), HEAD `8e55f817795a68b167f5785f6ac814c898cda11d`, `research/fxns-a-gdelt-qualification-20261008-2148jst`.
- B [PR #66](https://github.com/Josh-Temple/systematic-trading-research/pull/66), HEAD `769b94228307474fdaa91e84457c8f66390d69c5`, `research/fxns-b-xm-friday-readiness-20261008-2148jst`.
- C [PR #67](https://github.com/Josh-Temple/systematic-trading-research/pull/67), HEAD `166a8222e09dde4413b799acd92d74c4a2586c04`, `research/fxns-c-event-ledger-20261008`.

All three PRs target the same frozen-observation base branch, NOT `main`, and are unmerged as inspected. D branch starts at the exact PR #63 HEAD. This audit has not changed A/B/C code, source raw data, shared Specification/CURRENT, prompt/schema, or outcome-access policy.

## 2. Independent checks executed

1. Fresh-read Wave §D from `docs/TRADING_FIVE_ROLE_EMPIRICAL_WAVE_2026-10-08.md`, research `CURRENT.md`, `SPEC-FXNS-001-v01.md`, `SOURCE_CONTRACT.md`, prompt manifest, `PRE_FREEZE_HARDENING_RESULT.md`, XM `RESULT.md`. These agree: `UNTESTED`, `PROPOSED_NOT_FROZEN`, formal cohort `CLOSED`, no trading/order authority.
2. Fetched live GitHub PR metadata, all changed filenames, A/B/C reports, source-level per-file patches, C new `event_ledger.py` and `test_event_ledger.py`, A revised probe/tests, baseline `fxns.py`. Matched changed paths against three disjoint allowlists.
3. Fetched **exact UTF-8 content from canonical PR #63** for both prompt/schema files and historical GDELT raw response bodies; independently computed SHA-256 with a separate JavaScript implementation tested against the known `SHA256("abc")` standard vector. All four identities matched their preserved manifests:

| File | UTF-8 bytes | independently computed SHA-256 | result |
| --- | ---: | --- | --- |
| `work/PROMPT_v0.1.txt` | 1536 | `83958924048f1455e4b2dc2b6b147f4dce83a9f5d31c0ed4f6111cec75c058e9` | MATCH |
| `work/OUTPUT_SCHEMA_v0.1.json` | 1663 | `bc46262c89529f3cf22e2b992685a35816af1e3cb887d1aec8901adeee6cd4bf` | MATCH |
| `work/source-probe/runtime-20261007-exact/response.raw` | 5962 | `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d` | MATCH |
| `work/source-probe/runtime-20261007-cap10/response.raw` | 444 | `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6` | MATCH |

4. Independently counted tests in committed A/C test sources: A has 11 `test_*` methods (previous base has 9, exactly 2 added); C has 26. This verifies **test case definitions exist**, not that their runtime outputs are true.
5. Reviewed C code's formal call sites: `issue_formal_event` and `associate_market_outcome` unconditionally raise a closed-gate exception; synthetic builder rejects real headlines/URL hosts, sources not explicitly marked PASS, unknown model/config, forbidden timing and raw count >=250. These are **static source checks**, not separate Python runtime execution.

### Verification limitation

A complete source checkout and Python test execution were **not possible in this D environment**: a direct `git ls-remote https://github.com/Josh-Temple/systematic-trading-research.git` failed with DNS resolution of `github.com`. The GitHub connector provided the source bytes and PR diffs, but those were not mounted as an executable checkout. **No 11/11, 26/26, previous 53/53, or combined-suite PASS is independently claimed by this auditor.** A reports its own 11/11; C reports its own 26/26; B reports static checks and historical tests without running Python. No current GitHub Actions PASS was verified by this D report. No GDELT live probe, model call, XM/MT5 runtime operation, market outcome or broker order occurred.

## 3. Worker-by-worker disposition

### A / PR #68 — PARTIAL_WITH_GAPS; code change eligible for E review, source gate BLOCKED

Changed exactly three files under `work/source-probe/**`: appended source report, `gdelt_schema_probe.py`, `test_gdelt_schema_probe.py`. A's narrow source-code repair preserves an existing HTTP-response `retrieval_completed_at` rather than overwriting it in the later error handler, and writes a failure timestamp only if none was recorded. The two new tests cover HTTP 429 receipt time and invalid UTF-8 raw preservation. The changed code leaves the frozen query, date window, maximum-record count, source conclusion and existing raw evidence unchanged. Independently verified historical raw SHA-256 as above.

**Unresolved**: DOC seendate semantics, publisher-vs-seen time, UTC/equality, first-seen immutability, revision/indexing lag, scoped completeness, actual 08:00 JST pipeline availability. A's 2026-10-07 response was saved at ~12:20 JST and is not an on-time prospective observation. The MAXRECORDS=10 response is HTTP 429, **not** a complete result set. Source state remains `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED`.

The A PR uses `[skip ci]`; don't infer CI PASS from the author's local synthetic tests. Before integration, perform a separately scoped, network-disabled test run on the pinned A commit, and review the CI consequence of the current workflow's live source-probe behavior.

### B / PR #66 — PARTIAL_WITH_GAPS; documentation eligible for E review, XM gate BLOCKED

Exactly one appended report under `work/xm-source/**`; the collector, tests and original evidence are unchanged. B records the six fixed probe windows including three Fridays and distinguishes source-only field preservation from validated executable prices. Its 16 static/checklist checks are not broker runtime evidence.

**Required external action**: one local source-only collection using the existing v0.2 on the intended Windows XM MT5 terminal, preserving `tick_probes_raw.csv`, `metadata.json`, `sha256_manifest.json`, including failed/empty windows; then independent 08:15 coverage, time_msc/UTC/JST, duplicates/order, server/symbol, Friday session, actual-account costs. Do not provide credentials/account IDs/trade history. Until then `LOCAL_XM_EXECUTION_REQUIRED`. No substitute quote feed or Friday proxy.

### C / PR #67 — PARTIAL_WITH_GAPS; **repair recommended before E code integration**

Three new files under `work/implementation/**`: `event_ledger.py`, `test_event_ledger.py`, C report; no shared SPEC/CURRENT/prompt/schema/raw modifications. The **formal** `issue_formal_event()` and `associate_market_outcome()` paths unconditionally reject calls. The synthetic builder has explicit input shape/time/model/source checks and doesn't make network/model/broker requests.

**One source-level finding (D-C-01)**: `write_synthetic_event(event, directory)` checks only top-level `record_type == SYNTHETIC_ONLY_NOT_FORMAL`, `formal_cohort_status == CLOSED`, and `event_id` format before serializing the caller-supplied dict. It **does not require** `market_outcome == UNAVAILABLE_NOT_REQUESTED`, `source.*_ref` with `synthetic://`, or the full synthetic event shape. `verify_synthetic_event(file)` verifies an internally consistent hash and a `record_type` in two allowed labels, but also does not revalidate these fields. Thus a caller that **bypasses `build_synthetic_event()`** can save a record carrying non-synthetic/outcome-like data while retaining the `SYNTHETIC_ONLY_NOT_FORMAL` label. This is a **source-code control gap**; no actual market data was supplied or forged event executed in this audit. The dedicated formal issuance and outcome-join stubs remain CLOSED.

For robust isolation before integration, reject untrusted direct writes in both the writer and verifier or make their precondition explicit and enforceable, requiring synthetic-only field types, `market_outcome=UNAVAILABLE_NOT_REQUESTED`, synthetic source refs, coherent blocked/NO_TRADE flags, exact version/event state; test direct-writer bypass with a **fully synthetic** adversarial fixture. This narrow repair should occur on a separate C worker commit/PR, without adding real source access, strategy changes, broader abstractions or authorized cohort gates.

**Another boundary, not a defect claim**: exclusive create + a record hash is not tamper-proof against a privileged editor who rewrites data and hash together; C already says so. Until durable trusted storage is separately designed, its ledger is an illustrative synthetic prototype only.

**Before E merges C code**: independent whole-checkout Python suite and the direct-writer negative regression, plus prompt/schema identity and zero-real-source tests. The existing author-reported 26/26 is not a replacement for this.

## 4. Cross-worker / scientific boundary checks

- A/B/C PR file paths are mutually disjoint, all under their designated role-specific allowlists.
- None of their PR diffs touch `CURRENT.md`, the frozen/proposed `SPEC-FXNS-001-v01.md`, SOURCE_CONTRACT, prompt/schema, historical raw snapshots, HR/CSM/JP225 records, main or order interfaces.
- Separate **historical source byte integrity** (four SHA MATCH results) from **prospective source availability/completeness**, which remains unverified.
- Formal issuance and market outcome access stay CLOSED. No result-related rule changes, outcome-driven query tweaks, retroactive NO_TRADE changes or positive expected-return evidence were identified in the reviewed patches.
- Disjoint file paths alone do not prove combined runtime compatibility; full-suite verification and a pinned integration head are still required.

## 5. E handoff: ordered next actions

1. **A**: eligible for E to consider as narrow timestamp-handling repair, provided pinned synthetic suite reruns offline and CI doesn't trigger an unauthorized live GDELT query. Source qualification remains BLOCKED.
2. **B**: eligible as an append-only *blocked/source-readiness* report, without changing XM status or forcing redundant code changes. The actual next external action is the user's one source-only Windows XM execution.
3. **C**: **defer unrestricted integration** until D-C-01 is addressed with a direct-writer invalid-record regression and full-suite rerun on the exact head; alternatively E can explicitly exclude C from merge and preserve the review finding. No rewrite of the frozen candidate rule.
4. E must record adopted/deferred PRs, any new head and whole-suite test evidence, and the unchanged formal scientific boundaries. D **does not issue** formal Packet D PASS, SOURCE PASS, human freeze or permission to inspect/score the market.

**Overall**: A/B/C work artifact completion is confirmed, but empirical source readiness is not complete. One code-contract issue in C is identified before downstream integration. The next direct empirical dependency remains a qualified prospective GDELT pre-cutoff capture and local XM Friday tick qualification; neither was performed here.
