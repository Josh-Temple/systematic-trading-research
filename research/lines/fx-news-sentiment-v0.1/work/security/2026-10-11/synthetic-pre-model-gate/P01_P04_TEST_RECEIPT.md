# FXNS PR #122 P01–P04 — Author-side bounded synthetic remediation receipt

Date: 2026-10-14 JST. Source: PR #122 fixed commit `c078001c2facfbbe4187e6722af0eda17618533a` (tree `92e2ad88b5e30c613e4134642a4f38ce5c363343`). The author candidate lives on a **different branch**; PR #122 and all other existing PRs remain unchanged.

**Decision: `AUTHOR_SYNTHETIC_TESTS_PASS_SCOPED / INDEPENDENT_D_REACCEPTANCE_PENDING / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`.** This new receipt does not replace or rewrite historical `TEST_RECEIPT.md`.

## Evidence and implementation

- Previously identified independent D PR #123 failures: P01 historical `state` outside enumeration, P02 historical `reason` outside enumeration, P03 historical `operation` outside enumeration, P04 malformed `policy_id`. In PR #123 D also reported 81/81 existing PASS, old N01–N16 16/16 PASS, new 12/16 PASS. The D evidence ZIP Library upload/readback had failed and remains unverified here.
- Code fix: validate exact audit record types and field set, valid enumerations, policy-id syntax, and basic state/reason/operation semantic combinations for **all historical and newly appended entries** before acknowledging memory append. Retain `BLOCKED`/`RESERVED`/`RELEASED`/`UNKNOWN` fail-closed and in-process delivery ordering; do not authenticate history or claim real durable custody.
- Author regression: 10 new tests A25–A34 in `test_eight_findings.py`. Before applying the code fix, 43 tests ran, 7 deliberate new negative test failures (A25–A30,A33), 3 new positive controls pass. After fix, 22 `test_safe_boundary` + 26 `test_remediation` + 43 `test_eight_findings` = **91/91 PASS**, compile PASS.
- Prior D's **unchanged** N01–N16 fixture was replayed by the **author** after this fix: **16/16 PASS**. This is **not** a new independent D acceptance. Newly designed D P01–P16 full original fixture was not available for byte-exact replay.
- All code/test inputs were read from already-validated Library archives with exact SHA-256 and checked against fixed six GitHub blobs. Evidence ZIP includes original/candidate Python bytes, unchanged old D fixture, captured stdout/stderr, command exits, Python version, per-file hashes and `evidence_manifest.json`.

## Execution table

| Execution | Cases | Exit | Outcome |
| --- | ---: | ---: | --- |
| Red: new augmented `test_eight_findings` on unchanged code | 43 (7 deliberately fail) | 1 | RED as expected |
| Green: `test_safe_boundary` | 22 | 0 | PASS |
| Green: `test_remediation` | 26 | 0 | PASS |
| Green: `test_eight_findings` | 43 | 0 | PASS |
| Green: unchanged original N01–N16 fixture (author replay) | 16 | 0 | PASS |
| Green: `py_compile` of 4 Python files | separate | 0 | PASS |

Python: `3.13.5`; `PYTHONDONTWRITEBYTECODE=1`, `python -B`, no third-party dependencies. `NETWORK_OS_ISOLATION_NOT_VERIFIED`; successful offline execution does **not** certify OS-enforced network isolation. Exact executable paths, log SHA-256/size and individual case lines are captured in the evidence archive. No GitHub Actions/CI was invoked.

## Scope and hold

Only `safe_boundary.py`, `test_eight_findings.py`, and this new report file may differ from the frozen #122 HEAD. PR #122/#123/#124, #119/#120/#121, shared research branch/main, CSM and source contract remain untouched. No real upstream source, model ingress, host ACK, durable persistence, distributed exactly-once, or trading was tested. FXNS source remains `SOURCE_QUALIFICATION_BLOCKED`; CSM I2 remains `BLOCKED / CLOSED / market_outcome_access=false`; all related PRs remain `HOLD_NO_MERGE`.

**Required next:** independent new D Chat must pin this candidate's final SHA, verify all bytes and evidence, rerun full 91 existing/new author cases and old N01–N16, byte-replay P01–P16 if accessible, and implement ≥12 **new independent** adversarial synthetic cases. Any failure → `D_NEEDS_REVISION`. Even local D PASS must not release platform or research gates.
