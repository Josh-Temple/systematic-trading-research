# B — FXNS #88 final exact-head independent audit (2026-10-10 JST)

**Independent verdict: FAIL on required outer duplicate-JSON-key rejection / HOLD_NO_MERGE.**
This report documents independent code and negative-fixture review, exact-head CI log and Git-tree comparison. It is not an independent full-suite rerun, market-source qualification, or formal-cohort authorization.

## 1. Fresh snapshot, candidate and changes

- Repository: Josh-Temple/systematic-trading-research.
- Audited [PR #88](https://github.com/Josh-Temple/systematic-trading-research/pull/88): open Draft, not merged. Candidate exact HEAD: **ecabf673e923fccb202cc22d2e4a39291e74a2ee**; exact tree: **3fa284e10741617e23b4bb49511b58c1b15596f7**.
- Base branch: research/fx-news-sentiment-v0.1, exact **b1b31e5f1344c86c816f934a695a8583eb1bf4eb** (PR #63 open/Draft). main observed **33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3**. Neither branch modified.
- Complete PR #88 changed paths (three; all A implementation allowlisted):
  - research/lines/fx-news-sentiment-v0.1/work/implementation/event_ledger.py
  - research/lines/fx-news-sentiment-v0.1/work/implementation/test_event_ledger.py
  - research/lines/fx-news-sentiment-v0.1/work/implementation/2026-10-10/A_FXNS_OUTER_ENVELOPE_RESULT.md
- Direct candidate GitHub blob identities: implementation **87ce391ddf53a0f3f792eb7d4859de6733118ea4**; test **1e6ca255299152071915ecb5d80d8f8320c1788d**; A report **3b65e5583189f5191e8bae344a48287a36fec8bd**.
- Complete Git tree API returned truncated=false (377 entries). Diff shows no changes to workflow, offline test driver, source/raw/manifest, SOURCE_CONTRACT, frozen SPEC, PROMPT/SCHEMA, or main. Source, model and outcome gates unchanged.
- Existing offline workflow: .github/workflows/fxns-gdelt-source-probe.yml, blob **620581df64cf247c293781389bd7386df391f30e**. Runner .github/scripts/fxns_offline_unittest.py, blob **25636eca0b6c282a2f7233064ec9661fc62666c0**. Read the whole workflow and runner: pull_request-driven offline unittest and compileall only, with socket connect denial before test import; no live GDELT DOC step. Process-local deny is not a production OS sandbox.

## 2. Observed GitHub Actions, distinct from B execution

- Directly retrieved run metadata, job summaries, **decoded full job log**, checked-out commit, candidate commit and trees.
- [Run 37935320699](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37935320699), job **113835792703**, event pull_request, head_sha **ecabf673e923fccb202cc22d2e4a39291e74a2ee**, run attempt 1, completed/success.
- Log checked out merge commit **5076559fbd57ef91b96dba42a1dafcb8f51429bf** with parents **b1b31e5f1344c86c816f934a695a8583eb1bf4eb** and **ecabf673e923fccb202cc22d2e4a39291e74a2ee**. Merge commit tree **3fa284e10741617e23b4bb49511b58c1b15596f7**, equal to candidate tree: this CI did test the final candidate *tree*.
- Runner Python **3.13.16**. Decoded log recorded **implementation 83 + source-probe 11 = 94 total**, Ran 94 tests, **failures=0; errors=0; skipped=0; successful=True**, syntax compile passed. These are GitHub CI observations, **not B's own 94/94 rerun**.
- Independent actual complete-suite rerun: **NOT_RERUN**. Isolated local environment could not resolve github.com when attempting git ls-remote (DNS error). Did not obtain an isolated exact checkout; did not run target event_ledger.py. Did not dispatch workflow or make any market/source API request. Older #87 (different 93-test tree), #82/#84 and prior A code-only run are **not** substituted.

## 3. Independent negative review of exact target code and fixture definitions

| Case | Exact-code/test finding |
| --- | --- |
| Outer unknown/extra market_outcome, approval, source_pass, unknown | Outer dictionary key-set test in _validate_ledger_envelope; test_outer_envelope_extra_keys_rejected_even_with_valid_digest exists and shows ok in direct CI log. |
| Missing keys; non-dict outer/record; invalid digest type/format, uppercase/short/mismatch; rehashed outer | Validator insists parsed keys are exactly record and record_sha256, record dict, valid lowercase 64-hex canonical hash. Existing negative test shows ok in CI. |
| Malformed JSON/invalid UTF-8 | verify_synthetic_event wraps JSON ValueError/UnicodeDecodeError as EventBlocked; malformed test shows ok. |
| **Outer duplicate JSON keys** | **Not rejected**: verify_synthetic_event uses plain json.loads(raw), with no object_pairs_hook. Key-set validation occurs only after JSON duplicate keys have been collapsed. **No outer duplicate-key test exists** in six newly added #88 methods. See finding below. |
| Nested classification_raw, classification_parsed, scores, decision | Existing _validate_synthetic_record still strict: reparse with validate_batch, compare parsed data, independently recompute deterministic scores/action, enforce numeric finiteness and NO_TRADE consistency. prompt_contract.py uses _unique(object_pairs_hook) for duplicate keys in *nested model output*. Existing nested adversarial cases remain in CI and show ok. |
| Blocked decision forgery | Exact blocked schema disallows decision and is_no_trade; outer-extra and rehashed-inner blocked test exists, CI ok. |
| Valid LONG, NO_TRADE and blocked receipt | New round-trip test exists, CI ok. |
| Same event ID normal .json and .blocked.json | New test positively demonstrates coexistence despite each exclusive xb write; no cross-file precedence/exclusivity established. Residual human design decision. |
| Formal issuance / market outcomes | issue_formal_event and associate_market_outcome both unconditionally raise EventBlocked; COHORT_STATE=CLOSED. No new formal issuance or outcome join path. |

### Exact-head defect: ambiguous duplicate JSON member

- Code reference: event_ledger.py blob **87ce391ddf53a0f3f792eb7d4859de6733118ea4**, verify_synthetic_event: plain **json.loads(raw)** then _validate_ledger_envelope. The latter checks **set(payload) == {record, record_sha256}** only on the parsed dictionary. Duplicate raw keys cannot be seen after parsing.
- B independently **executed only a stdlib JSON parser demonstration**, Python **3.13.5**, not the target module. The serialized input had three field occurrences: record, record_sha256 with value invalid-first, record_sha256 with value valid-last. json.loads returned only the keys record and record_sha256 and retained **valid-last**. The duplicate was not rejected.
- For an otherwise-valid synthetic record and its matching digest in the last field occurrence, inspected code shows the outer validator **does not reject the duplicated raw field**, though the proposed strict two-field serialized envelope should do so. This supports **ambiguous outer serialized data acceptance**. It does **not** claim a forged internally invalid decision passes nested validation; no full target-module runtime exploit was attempted.
- Contrast: prompt_contract.py at blob **532254a9b73d5bea2112bf058651aa3d90d3c838** calls json.loads(..., object_pairs_hook=_unique) on inner model output and raises on duplicates. That does NOT protect the outer persisted envelope.
- The exact #88 tests include malformed JSON, wrong shape/hash, extra unique keys, and blocked forgery, but do **not** contain duplicated outer record or duplicated outer record_sha256 cases. Passing 94/94 thus cannot establish this required negative condition.

**Reason for verdict:** The B Wave explicitly requires a duplicate JSON key negative case. The exact target code lacks a unique-key parser on the outer envelope, and the suite lacks this negative test. The static failure of required outer contract validation is enough to deny B PASS_SCOPED, regardless of valid final-head CI evidence. **B verdict: FAIL (specific outer contract) / HOLD_NO_MERGE**. Independent full-suite status remains NOT_RERUN, not an invented failure.

## 4. Residual limits and next controlled handoff to E

- E must **NOT merge #88** into research/fx-news-sentiment-v0.1 based on this audit. A separate authorized implementation candidate must reject duplicate keys in both outer record and record_sha256, including identical/conflicting values, while preserving existing malformed/extra/missing/nested tests. Run fresh offline Actions on **new final exact HEAD/tree**, then arrange a **new independent B audit** of that new code. Never reuse #88's successful 94/94 or different-tree #87's 93/93 as new-head approval.
- Independent finding does **not** change cross-file same-ID design: a normal and blocked receipt can coexist. Do not invent a precedence rule in B. Coherent privileged full-record+digest replacement still passes canonical hash comparison; SHA is not signer identity, protected append-only storage or authorship proof.
- FXNS remains **UNTESTED / PROPOSED_NOT_FROZEN / formal cohort CLOSED**; GDELT **SOURCE_QUALIFICATION_BLOCKED**; XM/MT5 local execution deferred; no human freeze, no live DOC requests, ECB observations, real news classifications, market outcomes, prices, P/L, orders, paper/live trades or substitute broker data.
- Report-only B; **no code, tests, workflows, source, raw, manifest, gate, main, SPEC or scheduled task modifications**. PR #88 retains independent unapproved Draft state.
- Evidence classification: **direct GitHub read** (PR/paths/blobs/CI decoded log/workflow/runner/commit/tree); **B-executed local stdlib JSON demonstration** (not target verifier); **independent static code inference** (outer duplicate acceptance); **NOT_RERUN** (complete test suite); earlier A narrative not accepted as independent proof.

**Final: FAIL / HOLD_NO_MERGE for #88 exact HEAD ecabf673e923fccb202cc22d2e4a39291e74a2ee.**
