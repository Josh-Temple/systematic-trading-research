# Worker A — PR #74 exact-head independent synthetic implementation audit

- Audit date: 2026-10-09 JST.
- Repository: `Josh-Temple/systematic-trading-research`.
- **Overall disposition: PARTIAL_WITH_GAPS.** This is an **offline synthetic implementation review**, not FXNS formal Packet D approval, source qualification, human freeze, prospective outcome testing, or authority to trade.
- Audited PR: [#74](https://github.com/Josh-Temple/systematic-trading-research/pull/74), `work/fxns-no-xm-offline-verified-20261009`, **head `9ebfc57dd4060825da189b196dd044b6ffaead4f`**, OPEN/DRAFT.
- Base research branch: `research/fx-news-sentiment-v0.1`, **head `202ee37d0cd3f9838b153ea361dfdeba5244a271`** ([#63](https://github.com/Josh-Temple/systematic-trading-research/pull/63)), OPEN/DRAFT.
- Current `main` observed: `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`. **No writes to main, #63, #74, or audited code.**
- Prior D finding preserved: [#69](https://github.com/Josh-Temple/systematic-trading-research/pull/69), `da35d13179532ea1988bb476bf219662d1824e40`, **PARTIAL_WITH_GAPS** (it inspected the earlier uncorrected C head). This document **does not replace formal Packet D**.

## 1. Fresh-read scope and exact identity

Directly fetched current PR #63, #74, #70, #69 and merged #72 GitHub metadata; PR #74's complete eight changed paths; per-file Git blob SHA on pinned heads; exact `event_ledger.py`, `test_event_ledger.py`, `gdelt_schema_probe.py`, GDELT tests, prompt manifest, CURRENT, source contract, Packet D instructions and offline CI workflow/runner. Re-read PR #74 and #63 heads immediately before the audit branch write. No target-head drift was observed at that check.

All **eight PR #74 changed paths** are scoped to the earlier A/B/C/D worker areas:
1. `work/implementation/C_RESULT_2026-10-08.md` — byte-identical Git blob to C #67 (`55f0b8689d4bc5f97ee35d670cd1a418e6591291`).
2. `work/implementation/event_ledger.py` — blob `8eff6952dc247edb202cfb45576af6a8bd8bb279`, matches corrected C #70.
3. `work/implementation/test_event_ledger.py` — blob `9447d87b873f246586d045db729e568c41010244`, matches corrected C #70.
4. `work/source-probe/gdelt_schema_probe.py` — blob `d747160126130291963c2ae981fb9b149f98b29e`, matches A #68.
5. `work/source-probe/test_gdelt_schema_probe.py` — blob `1274e4c045c1d106d0dca856ffc8d1e5ac3ff15c`, matches A #68.
6. `work/source-probe/ROLE_A_SOURCE_QUALIFICATION_2026-10-08.md` — blob `70b09ac78000e6773959dbfe5a6bbc9a5bfaf73b`, matches A #68.
7. `work/xm-source/B_XM_FRIDAY_SOURCE_READINESS_2026-10-08.md` — blob `621a23c7fada781ca54fa2efa29de0c481f3f461`, matches B #66; a **blocked/readiness report**, not XM execution.
8. `work/independent-audit/2026-10-08/D_INDEPENDENT_AUDIT.md` — blob `08ce1eafbb1cccfe29bde7451a7eafe1de316ac3`, matches old D #69; prior PARTIAL remains recorded.

**Unchanged files**: PR #74 and #63 have identical blob SHA for `CURRENT.md`, `SOURCE_CONTRACT.md`, `SPEC-FXNS-001-v01.md`, `PROMPT_MANIFEST_v0.1.json`, `PROMPT_v0.1.txt`, `OUTPUT_SCHEMA_v0.1.json`, and both historical GDELT HTTP 200/429 `response.raw` and `manifest.json` files. This establishes **Git exact-blob identity across the two heads**, not independent revalidation of external-source truth. Manifest preserves prompt SHA-256 `83958924048f1455e4b2dc2b6b147f4dce83a9f5d31c0ed4f6111cec75c058e9` and schema SHA-256 `bc46262c89529f3cf22e2b992685a35816af1e3cb887d1aec8901adeee6cd4bf`; these content hashes were not independently recomputed during this A session.

## 2. CI evidence — directly observed, not self-reported

- [Successful Actions run 37798966613](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798966613) is associated by GitHub's commit workflow-runs endpoint with the **exact PR #74 head `9ebfc57...`**. Job `113385769601`, `fxns-synthetic-offline`: completed / success.
- Direct job-log readback: `FXNS_OFFLINE_SUITE: implementation, discovered=72`; `source-probe, discovered=11`; `TOTAL_DISCOVERED: 83`; `Ran 83 tests`; **`run=83; failures=0; errors=0; skipped=0; successful=True`**. Compilation step also succeeded, using Python 3.13.
- [Earlier unsuccessful run 37798633932](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798633932), job `113384598196`: **83 run, one error, 0 failures, 0 skips**, `test_no_trade_is_immutable_even_after_freeze`. Traceback showed a fixture replacement blocked by `INCONSISTENT_NO_TRADE` **before** reaching expected `FileExistsError`; not evidence that the immutable-create control itself failed. The corrected test builds a second **valid** synthetic event of the same ID and expects exclusive-create refusal. Historical FAIL remains retained.
- The current `.github/workflows/fxns-gdelt-source-probe.yml` executes only checkout, Python setup, `.github/scripts/fxns_offline_unittest.py`, and `compileall` on PR/workflow_dispatch. The runner denies normal Python socket connections before loading test modules; the workflow has **no GDELT live probe step and no XM/MT5 step**. The socket monkeypatch is process-scoped, **not a hostile-code sandbox**.
- **Independent Python rerun: NOT_RERUN.** Attempted direct `git ls-remote` for the complete checkout; the available local runtime could not resolve `github.com`. Connector-derived source blobs were reviewed statically, but no executable full checkout was assembled. CI PASS is externally observed on the exact head; it is **not** claimed as an independent re-execution in this session.

## 3. Static implementation findings (current PR #74 code)

| ID | Scoped result | Evidence / precise boundary |
| --- | --- | --- |
| A-C-01 | **PASS_SCOPED — earlier D-C-01 repair present** | `_validate_synthetic_record` is called by both `write_synthetic_event` and `verify_synthetic_event`; it checks top-level exact keys, synthetic event state and source refs, blocked-receipt semantics, fixed `market_outcome=UNAVAILABLE_NOT_REQUESTED`, model markers, prompt hashes, event timeline, decision enum and flag consistency. `issue_formal_event` and `associate_market_outcome` still unconditionally raise CLOSED-gate errors. |
| A-C-02 | **PASS_SCOPED — exclusive create of valid same-ID events** | Writer uses `open("xb")` with no overwrite option. The corrected test creates a valid opposite-decision event for the same event ID, checks `FileExistsError`, and reads back the original `NO_TRADE`. A privileged disk editor is outside the exclusive-create guarantee. |
| A-C-03 | **PASS_SCOPED — targeted negative CI** | On the exact head, CI runs tests rejecting direct top-level `market_outcome`, extra top-level price field, non-synthetic source/review reference, mismatched model marker, and rehashed versions of these selected field-level violations; a blocked preflight receipt cannot become a `NO_TRADE` decision. These are fixture-specific successes. |
| A-C-04 | **PARTIAL_WITH_GAPS — nested payload acceptance** | `_validate_synthetic_record` only checks `classification_raw` as a string list of expected length, `classification_parsed` as dictionaries whose `record_id` sequence matches, and `synthetic_scores` as a dict with `EUR`/`JPY` keys. It does **not** call the existing strict `validate_batch` on saved classification strings, require the parsed contents to equal those strings, require exact parser field keys inside parsed rows, recompute score/decision from parsed values, or validate score value types. Thus a direct caller may construct an otherwise well-shaped synthetic event with **an extra nested `market_outcome` key in `classification_parsed[0]` or arbitrary invalid JSON in `classification_raw[0]`**. This would satisfy the visible local guard predicates even though the canonical builder's parser would reject it. A recomputed outer hash would also be internally consistent. This is a **source-code deduction, NOT an executed adversarial test**; no real news, market values, or external URL were accessed. |
| A-C-05 | **PARTIAL_WITH_GAPS — provenance and historical tamper limits** | Record SHA-256 and `open("xb")` do not authenticate an independent producer or make on-disk records immutable to a privileged editor who rewrites the record and hash. A rehashed on-disk change to decision + matching `is_no_trade` need not be detected by the currently visible semantic validator. This is not a failure of the narrow exclusive-create guarantee and was partly acknowledged by old D; it bars claims of tamper-proof operational evidence. |
| A-A-01 | **PASS_SCOPED — 429 timestamp preservation** | Source-probe `main` stamps `retrieval_completed_at` after network response/error response read, writes raw bytes and hash, and in the generic exception handler stamps time only when absent. A synthetic HTTP 429 test mocks separate request-start and completion times and asserts the network-completion value is preserved. This is NOT a real prospective GDELT time guarantee. |
| A-W-01 | **PASS_SCOPED — offline workflow scope** | Current workflow and steps contain no automatic live GDELT/XM acquisition. Runtime test sandbox is limited to Python socket intercepts, so keep explicit workflow review and deny-network invariant. |

### Minimal recommended remedy (outside A's write allowlist)

On a **separate C-owned code patch**, validate the persisted `classification_raw` via existing `validate_batch(raw, ids)`; require exact equality to `classification_parsed` (including nested field allowlist), recompute `daily_scores` / `pair_action` and compare `synthetic_scores` / `decision` / `is_no_trade`. Reject unexpected nested keys and malformed strings **before** writing and during readback; add synthetic adversarial direct-writer and rehashed-readback regression tests for nested `market_outcome`, invalid classification JSON, divergent score/decision, and a tampered `NO_TRADE` to directional decision. Re-run the complete offline suite on the **new exact head**, followed by independent re-audit. Treat a disk-level adversary as out of scope unless a separate authenticated/immutable storage requirement is approved; do not call current SHA alone a trusted attestation.

## 4. Scientific boundaries and decisions for Worker E

| Axis | Current conclusion |
| --- | --- |
| Synthetic offline CI | **PASS_SCOPED** only for existing 83 tests on PR #74 exact head |
| Prior D-C-01 top-level writer/verifier bypass | **Targeted repair present**; new nested-contract gap remains |
| Overall corrected PR #74 implementation audit | **PARTIAL_WITH_GAPS** — do **not** promote to unrestricted E code integration on this audit |
| GDELT | `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED`: retrospective raw receipt and mocked 429 do not establish on-time availability, first-seen immutability or completeness |
| XM | `LOCAL_XM_EXECUTION_REQUIRED` **deferred at user request**; no Windows or MT5 operation |
| Science | `UNTESTED`; `SPEC-FXNS-001-v01 PROPOSED_NOT_FROZEN`; prompt candidate NOT human-frozen; formal prospective cohort `CLOSED` |
| Authorization | No real classifier run, market outcome/return/P&L access, data-source change, paper/live order, price series, or human freeze |

**E recommendation: DEFER unrestricted integration of the complete PR #74.** The narrow A 429 fix and B blocked-readiness document may be assessed independently as scoped candidates, while C remains held for its **nested classification/score/decision contract** repair and synthetic negatives. Retain historic negative/blocked reports; do not delete or reinterpret old D's PARTIAL. If the exact PR #74 head changes, this report is not automatically portable to a new head. No source/scientific PASS is conferred.

**Remaining blockers:** (1) enforce nested persisted-event semantics with narrow C fix and new offline pinned CI + separate audit; (2) independently repeat whole-checkout tests if an authorized network-isolated checkout is available; (3) GDELT documented/observed point-in-time source guarantee remains absent; (4) XM source work intentionally paused; (5) human freeze is absent.

## 5. Reproducibility and boundaries

Read paths under PR #74 from the pinned SHA, inspect the guarded `_validate_synthetic_record`, `write_synthetic_event`, `verify_synthetic_event`, `validate_batch`, current synthetic tests, the merged offline-only workflow, then read the *job log*, not just the job badge, for runs 37798966613 and 37798633932. This A worker did **not** edit any audited source, create fixtures with real inputs, call GDELT, request XM collection, or use outcome-bearing data. The only planned Git write is this audit receipt within `work/independent-audit/2026-10-09/pr74/**`, on an independent PR targeting the FXNS research branch.
