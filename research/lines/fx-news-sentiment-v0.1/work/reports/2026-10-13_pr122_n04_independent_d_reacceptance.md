# FXNS PR #122 N04 — independent D reacceptance, 2026-10-13 JST

**Decision: D_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE**

This report is an independent D run, not A's author tests. All inputs were fictional. This does not certify real host, source selection, durable custody, model ingress, or network OS isolation.

## Frozen Git identity and evidence

- Target Draft PR #122: HEAD `c078001c2facfbbe4187e6722af0eda17618533a`, tree `92e2ad88b5e30c613e4134642a4f38ce5c363343`, parent `f544eabba26343a7dda9150ee7e0fc2f995a9e25`, base `dc8b0d310abba044c80506192117abf04c84a899`.
- Exactly 3 changed paths: `safe_boundary.py`, `test_eight_findings.py`, `TEST_RECEIPT.md` within `research/lines/fx-news-sentiment-v0.1/work/security/2026-10-11/synthetic-pre-model-gate/`.
- Six files independently fetched from the exact HEAD/path using GitHub connector base64 mode; encoding, canonical fixed-ref display URL and expected Git blob checked. Original fetched byte lengths and SHA-256 calculated independently.
- Four Python source blobs and byte SHA-256 match the Library author ZIP: `safe_boundary.py` 19,866 bytes / SHA-256 `61e642aae1fa2838ad3dc51a788956342e66fc83b1323c0010bb61efad634667`; `test_safe_boundary.py` 8,473 bytes / `7d60393dde7b7cfaac665604920c1e6c2cf89ef732b96e678c1a16ba6376c527`; `test_remediation.py` 11,788 bytes / `fe796702764637e18749c8a09cd02db8d6610cd4d6ffeada641e1317219be499`; `test_eight_findings.py` 13,176 bytes / `f9b8d72223d5ae4ded9713eb9eaacb4428909ff5c9af0f8a1275b07c23c6719e`.
- `README.md`: 9,000 bytes / SHA-256 `8e05d10080a3a8fd1d474e689581c7cf97257a69fa11450612868402366f4abe`. `TEST_RECEIPT.md`: 35,753 bytes / SHA-256 `63f97ef782703a1cdda46357cc066ed98cfac9db9b740a8193a57026b9ec291b`. Git blob IDs match Wave.
- Library author evidence `/Broad Trade Research/fxns_pr119_N04_author_remediation_20261013(1).zip`: 29,505 bytes; SHA-256 `3c2a0f541a454ab6b663892a48c68574cd2907997ff52e51fd5b0b9d1f56b094`; 22 ZIP entries, CRC valid. Original independent-D evidence ZIP: SHA-256 `5a0cd5f2ebd08c5090960b8bcb80e086273eb604e7bed8ff93829457cc9578ad`; N01–N16 fixture kept unchanged.

## Independent execution (Python 3.13.5, stdlib, scratch only)

All with `PYTHONDONTWRITEBYTECODE=1`, `python -B`. Three existing suites: `python -B -m unittest -v test_safe_boundary`: **22/22 PASS**, exit 0, stderr 3,043 bytes SHA-256 `13cd904eea72a0fcbabc2f05e57c7fc8e6d4182ebf1b9fd16bd7ed07a48298fd`; `test_remediation`: **26/26 PASS**, exit 0, stderr 3,709 bytes SHA-256 `0fa8a5eaf716a10cd208914103dac81b95181d0ca1e16cfa268426b03f752419`; `test_eight_findings`: **33/33 PASS**, exit 0, stderr 4,801 bytes SHA-256 `0c17ca421722e5a2aac1b1b98c1faf74516d3d2bb200e962c77609ccfb84100b`. The four-file `py_compile` command exit 0. Total **81/81 existing PASS**.

Unmodified prior independent-D `python -B -m unittest -v test_independent_d`: **16/16 PASS**, exit 0, stderr 2,373 bytes SHA-256 `029588af8d031c54d485caea0ab9780628038b5d8e7b47072f8d7d0612f1a871`, including N04 rejected as intended. This is our own execution, not the author's replay.

D newly wrote and executed `test_d_new_20261013.py` (SHA-256 `edfa4f0202f956236cda1a8b35e7c22316709fd2b3441b2828d0c66c99b481ae`): **16 cases; 12 PASS / 4 FAIL; exit 1**. Full raw stderr: 6,742 bytes, SHA-256 `58f0c39494ffd6d476f65cfb4fa73e7178b8f5e091eda0e093d526bd721058fd`. All six commands yielded zero-byte stdout.

## Finding — P01–P04 invalid historical audit string contents can release

In `safe_boundary.py`, `Boundary._audit().valid_entry()` (~lines 169–175) verifies historical receipt dictionaries have exact built-in dictionary/string *types*, four expected keys and expected length. It does **not** validate string *contents* of historical `state`, `reason`, `operation`, or `policy_id` against approved domains/syntax. New receipt `append()` performs such domain checks, but pre-existing entries bypass them.

Independent tests of strictly string-typed history:
- **P01 FAIL:** invalid state `RELEASED_WITHOUT_AUDIT`.
- **P02 FAIL:** invalid reason `FICTIONAL_ATTACK_PAYLOAD`.
- **P03 FAIL:** invalid operation `ACTUAL_CONNECTOR_EXFIL`.
- **P04 FAIL:** invalid policy ID `unapproved\\nraw-body-synthetic`.

**In each case** expected refuse / delivered=0 / no RELEASED. Observed returned non-None, synthetic `delivered_count=1`, registry `RELEASED`, and new `RESERVED` then `RELEASED` receipts. This constitutes **one defect family** with four independent field-level counterexamples; it does not establish a real-host exploit.

Other new cases P05–P15 passed: append forged-but-string state, duplicate new receipt, dictionary/list subclasses, mutation of valid prior audit history, ACK hash subclass, prior delivery rewrite, response page and field subclasses, bytes-subclass body. **P16** positive control with valid prior history passed. No existing fixture or expected result was edited.

Minimal synthetic replay: start with `b,s,_=fixture()`; construct history `{'state':'RELEASED_WITHOUT_AUDIT','reason':'OK','policy_id':b.policy.policy_id,'operation':'PR_METADATA'}`; initialize `r=ReceiptSink(receipts=[history])`; run `Boundary(b.policy,s,r).run(request(),metadata())`. Observe one delivery and `RELEASED`; expected no delivery. Replace the bad field in turn for P02–P04.

## Decision, storage and next action

**D_NEEDS_REVISION** regardless of 81/81 and N01–N16 successes. Ask for explicit human approval before editing implementation. Proposed fix is strict semantic validation of **all pre-existing** audit entries, consistent with permitted states/reasons/operations and policy-ID syntax, plus own negative/positive regressions. Keep historical legitimate multi-policy entries possible if specification allows them; reject malformed ones fail-closed. Preserve all current gates.

Evidence was packaged locally as `fxns_pr122_D_independent_reacceptance_20261013.zip`, 36,590 bytes, SHA-256 `d3871329e50c55fd1481df2bdeb9f50cca4abaf5df78aec916f190fa981950b5`, containing 24 entries (source, unchanged prior D fixture, new D test code, per-suite stdout/stderr, JSON individual results, case side effects, self-verifiable SHA-256 manifest). Archive CRC and all included hashes were checked. **Library upload failed** with `container_session_unavailable`; therefore permanent Library custody and Library readback are **NOT VERIFIED**, not claimed.

OS network deny **NOT VERIFIED**; no GitHub/Work pre-model gate, real append ACK, distributed exactly-once or host side-effects validated. No CI, clone, live source/news/market/broker access, actual model ingress, merge, or trading. This PR only reports findings, does not alter any source or research gate.

FXNS must remain `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN / NO_QUALIFIED_ALTERNATIVE`. CSM I2 remains `BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED`. #106/#108 human dispositions PENDING. All source and report-only PRs HOLD_NO_MERGE.
