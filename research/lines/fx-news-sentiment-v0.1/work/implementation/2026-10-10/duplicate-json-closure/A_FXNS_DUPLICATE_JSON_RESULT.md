# A — FXNS persisted JSON duplicate-key closure (2026-10-10 JST)

## Status and scope

Candidate **Draft only / independent B required / HOLD_NO_MERGE**. This is an A-only implementation handoff, not B PASS, source certification, or an approval to issue signals or trade.

- Repository: `Josh-Temple/systematic-trading-research`
- New branch: `work/fxns-outer-duplicate-json-20261010-a-v1` from FXNS research base `research/fx-news-sentiment-v0.1` exact pre-write HEAD `b1b31e5f1344c86c816f934a695a8583eb1bf4eb` (PR #63).
- Ported input: old Draft PR #88 exact HEAD `ecabf673e923fccb202cc22d2e4a39291e74a2ee` (unmerged), original `event_ledger.py` blob `87ce391ddf53a0f3f792eb7d4859de6733118ea4`, original `test_event_ledger.py` blob `1e6ca255299152071915ecb5d80d8f8320c1788d`; the full original strict outer-envelope code and tests were reproduced as file content, **not merged/cherry-picked from #88**.
- Independent negative finding: old B PR #96 `FAIL/HOLD_NO_MERGE`; previous E PR #97 `HOLD_NO_MERGE`. Old #88 CI is **not** evidence for this candidate.
- Files changed against research branch are limited to `event_ledger.py`, `test_event_ledger.py` and **this** `2026-10-10/duplicate-json-closure/A_FXNS_DUPLICATE_JSON_RESULT.md`.

## Minimal change and rejection boundary

`verify_synthetic_event` parses persisted raw JSON bytes with `json.loads(..., object_pairs_hook=_unique_ledger_json_members)`. The hook raises `EventBlocked("DUPLICATE_LEDGER_JSON_MEMBER")` before any duplicate member is collapsed. The parser preserves this EventBlocked exception; malformed JSON and invalid UTF-8 remain mapped to `EventBlocked("INVALID_LEDGER_JSON")`. Scope: **any repeated member in any JSON object contained in the persisted envelope**, including outer `record` / `record_sha256` and nested objects. A separate JSON string stored inside a record remains validated by its existing strict classification parser. Duplicate values are rejected whether identical or conflicting. Unique valid JSON remains the same Python dictionaries and passes the unchanged envelope/hash/nested validators.

The code carries forward #88's existing six test methods verbatim and appends **two synthetic-only methods** with seven outer duplicate variations and nested-object / blocked-receipt variants. Cases include identical/different values, invalid-first/valid-last and valid-first/invalid-last, `approval` duplicates, and hash-valid-last bypass. Existing tests continue to cover unknown `approval`/`source_pass`/`market_outcome`, missing keys, non-dicts, hash and digest forgery, malformed/invalid UTF-8, strict raw/parsed classifications, score/decision recomputation, blocked forgery, valid LONG/NO_TRADE/blocked writer-readback, and formal/outcome unconditional rejection.

## Test provenance and required follow-up

- Before the candidate PR and GitHub Actions run exist: **CI_NOT_YET_OBSERVED; local complete-suite execution NOT_RERUN**. A local exact GitHub checkout was not available due to disabled DNS; no locally invented test results.
- Existing safe Actions workflow `.github/workflows/fxns-gdelt-source-probe.yml` (blob `620581df64cf247c293781389bd7386df391f30e`) and offline driver `.github/scripts/fxns_offline_unittest.py` (blob `25636eca0b6c282a2f7233064ec9661fc62666c0`) were directly read before use. The PR trigger runs unittest discovery in synthetic implementation and source-probe and compileall, with socket connect denied. **No workflow_dispatch** and no external source API calls. Process-local socket deny is not an OS isolation assurance.
- **Read the new PR body and Actions run/job for actual post-commit CI state.** A result is successful only when the new final HEAD/tree and actual checkout tree/log, negative test names, Python version, count and failure/error/skip are verified. B must independently audit this final exact HEAD/tree. The old #88 94/94 is historic, not reusable.

## Residual boundaries, not repaired

- Same event ID can still coexist in `.json` and `.blocked.json`; old PR #94's cross-file semantics require a later human decision. No precedence/exclusion added.
- A coherent privileged full-record + SHA-256 rewrite can remain undetected by the checksum; no signer identity, trust store, append-only storage, OS custody, production key or principal assurance claimed.
- `COHORT_STATE=CLOSED`, `issue_formal_event` and `associate_market_outcome` still fail closed. GDELT source remains `SOURCE_QUALIFICATION_BLOCKED`; FXNS `UNTESTED / PROPOSED_NOT_FROZEN`; XM deferred; no ECB observations, live DOC, model classifications, real signals, market outcomes, P/L, orders or trades. `main`, research branch, previous PRs, source/spec/workflows/manifest/prompts/gates and schedules unchanged.

**Disposition:** new A code/test candidate only. **HOLD_NO_MERGE** until new exact-tree CI and separate B PASS_SCOPED; if CI cannot be verified, classify `CI_NOT_EXECUTED/HOLD`.
