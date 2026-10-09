# A — FXNS synthetic ledger outer-envelope strictness (Wave plan 2026-10-10)

**Execution evidence recorded 2026-10-09 JST.** The plan date is not an execution/approval date. This is a scoped implementation receipt, not independent Role B approval.

## Immutable inputs and allowlist
- Repository: `Josh-Temple/systematic-trading-research`; Draft candidate [PR #88](https://github.com/Josh-Temple/systematic-trading-research/pull/88); base `research/fx-news-sentiment-v0.1`, exact starting SHA `b1b31e5f1344c86c816f934a695a8583eb1bf4eb` (FXNS #63).
- Before this receipt, only `research/lines/fx-news-sentiment-v0.1/work/implementation/event_ledger.py` and `.../test_event_ledger.py` changed (full PR diff checked).
- Implementation blob `87ce391ddf53a0f3f792eb7d4859de6733118ea4`; tests blob `1e6ca255299152071915ecb5d80d8f8320c1788d`.
- Code+test Git commit `e02b83a0719d0968215f03ee0c4f34c840c12811`; Git tree `a6f2f40c79de4f71ea1f3c82c3123a5f628f5a52`. This receipt commit will create a newer final HEAD; exact-final-HEAD CI must be verified separately before B.

## Implemented bounded change
- `verify_synthetic_event` now parses unreadable/invalid JSON as `EventBlocked` and requires a **dictionary outer envelope with the exact two keys** `record` and `record_sha256`.
- `record` must be a dictionary; `record_sha256` must be a lowercase 64-hex SHA-256 string **and must equal** the existing canonical hash of that record.
- On success, the **existing** `_validate_synthetic_record(record, allow_blocked=True)` remains mandatory, retaining strict nested `classification_raw` reparse, `classification_parsed` equality, deterministic EUR/JPY scores and decision, and blocked receipt shape.
- Writers still emit exactly this envelope and use exclusive create (`xb`); no new tolerance, source rule, prompt/schema/spec, eligibility, cross-file precedence, market or authorization path.

## Executed synthetic tests — code+test commit
- GitHub Actions [run 37935138562](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37935138562), job `113835188814`, `fxns-synthetic-offline`: **completed/success** on `e02b83a0719d0968215f03ee0c4f34c840c12811` / Git tree `a6f2f40c79de4f71ea1f3c82c3123a5f628f5a52`.
- Direct decoded job log: Python **3.13.16**; `python .github/scripts/fxns_offline_unittest.py`; `implementation=83`, `source-probe=11`, total `run=94; failures=0; errors=0; skipped=0; successful=True`. Syntax-compile step succeeded. Earlier scoped suite: 88. This run added **6 test methods**, not a claim of six individual adversarial variations.
- The runner invokes socket-denied synthetic tests; workflow only executes offline unit tests and Python compileall. It does not invoke the live GDELT DOC API. CI is process-local network denial, **not** production OS sandboxing.
- Six additional synthetic test methods cover: valid LONG/NO_TRADE/blocked writer+readback; surplus outer `market_outcome`/`approval`/`source_pass` and unknown field despite valid digest; absent keys, wrong payload or digest types, uppercase/short/mismatched digest, a falsely rehashed outer object; malformed JSON and invalid UTF-8; blocked-receipt outer and rehashed decision forgery; same event ID with normal `.json` **and** `.blocked.json` coexisting.
- Expected rejections and valid roundtrips were **actually exercised in GitHub Actions** on the stated code+test HEAD, not separately rerun on this local runtime (local independent execution `NOT_RERUN`).
- Formal `issue_formal_event` and `associate_market_outcome` remain unconditional `EventBlocked`; legacy nested raw/parsed/scores/decision negative tests remain in the passing 94-test suite.

## Unresolved limits / E design hold
1. **Coherent privileged replacement:** a writer with filesystem control can replace a valid entire synthetic record and recompute the SHA-256. Outer strictness and internal revalidation do **not** prove authorship, true append-only storage, authorized principal or independent provenance. Signature/protected ledger/trusted executor require separate approval and tests.
2. **Same-event-ID cross-file ambiguity observed:** normal `SYNTHETIC-FXNS-YYYYMMDD.json` and blocked `SYNTHETIC-FXNS-YYYYMMDD.blocked.json` can coexist, since each filename is independently exclusive. Intra-file duplicate writes are blocked. The protocol gives no new cross-file precedence; E must explicitly decide whether to design an additional cross-file exclusivity rule. **Do not silently add one in this Wave.**
3. **Evidence limitation:** no independent B audit yet. The code+test CI run precedes this receipt commit. Recheck the final PR HEAD / Actions run before treating this as a handoff-qualified A candidate.

## Research and safety state — unchanged
`UNTESTED / PROPOSED_NOT_FROZEN / formal cohort CLOSED / SOURCE_QUALIFICATION_BLOCKED / XM collection deferred`. No real news classification, live GDELT, ECB, XM/MT5, prices, returns, P/L, market outcomes, paper or live trades, production signal, human freeze, or alternate provider were obtained or enabled. Neither `main` nor research branch is merged by A.

**Disposition:** scoped code+test offline CI **PASS observed** on exact prior code+test SHA; A final candidate **pending its exact-head CI** after this receipt; independent Role B **NOT_RUN**; E integration **HOLD** until independent exact-head approval and all source/scientific gates remain closed.
