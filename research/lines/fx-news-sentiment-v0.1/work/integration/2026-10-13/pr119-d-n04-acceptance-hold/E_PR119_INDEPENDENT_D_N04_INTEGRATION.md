# FXNS PR #119 — E integration (2026-10-13 JST)

**E_INTEGRATED_D_FAILURE / D_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE**

This report integrates the verified, independent D result into the existing hold. It changes no source code, tests, source-data contracts, CI, permissions, or research gates.

## Fixed evidence

- FXNS research base: `24ef9c37e6255126a957f38cfa7470cd150ed594`.
- A PR #119: https://github.com/Josh-Temple/systematic-trading-research/pull/119
  - Final HEAD `dc8b0d310abba044c80506192117abf04c84a899`.
  - Tree `3da3adaae35feb802576a888fee3140f35e3ecdb`; parent `3e45c2a98ab030d3a9536b169154e9855493289c`.
  - 77/77 author-side synthetic cases and compile PASS; original receipt `TEST_RECEIPT.md` blob `78c30300662c2e2066793b251b4a6c36ebc5f3a1`.
- D PR #120: https://github.com/Josh-Temple/systematic-trading-research/pull/120
  - Report-only HEAD `6f0a8716fff5e7f27cd3aaa07fcdbd5415330c55`; tree `351f9ab33978d4e6ac826c6211f04c4a430f7a41`; parent `8f69bded3be746f9f6b6fd1011ea8676f5d32877`.
  - Sole changed report: `research/lines/fx-news-sentiment-v0.1/work/security/2026-10-13/pr119-independent-d-reacceptance/D_REPORT.md`, Git blob `7f4bc2fc7af896352467e77247f6cfa3b468e6e0`, byte SHA-256 `72b42931b7418dda5e51154d8f8857766e7faaf7354d06cf39bc8a6f9d8d683f`.
  - D evidence: Library `/Broad Trade Research/fxns_pr119_D_independent_reacceptance_20261013.zip`, 50,519 bytes, SHA-256 `5a0cd5f2ebd08c5090960b8bcb80e086273eb604e7bed8ff93829457cc9578ad`.
  - E checked 25/25 archived manifest hashes, all five command exit codes, archived stdout/stderr hashes and 93 case status records against execution.json. E did not rerun D's tests.

## Independent result and technical conclusion

- D independently reran the unchanged 77 author tests: **77 PASS**, compile PASS.
- D designed and ran 16 additional synthetic tests: **15 PASS, 1 FAIL** (N04, test process exit 1).
- N04 failure: `Boundary._audit` in `safe_boundary.py` allows an audit record containing unexpected non-string value objects to satisfy dict equality checks. D observed delivery and a RELEASED state where rejection was required. This is a proven local synthetic safety-expectation violation; no claim is made about real Work host exploitability.
- Author A PASS and independent D FAIL are **distinct**; the only defensible current technical acceptance outcome is **D_NEEDS_REVISION**.
- OS egress isolation `NETWORK_OS_ISOLATION_NOT_VERIFIED`; model ingress, independent durable audit ACK, source-side selection, cross-process exact-once and approved excerpt custody `NOT_VERIFIED`.

## Required next sequence and separate human decisions

1. A separate human authorization is required to modify any code/test beyond the earlier approved author receipt update. Limit a future A correction to the known, fully fabricated `synthetic-pre-model-gate` files on a new isolated branch based on PR #119's fixed A HEAD, without changing #119, #120, #117, #110, the FXNS research branch, main, or CSM.
2. Author A must add a regression that fails before the fix and passes after the fix, with exact receipt shape/key and value-type checks in `_audit` (including historical entries and the newly appended entry). Preserve other fail-closed states, replay and UNKNOWN/NO_RETRY controls. Run the full 77 plus new regression and compile; pin all input bytes, command results, logs, and receipt.
3. A new, separate D Chat must independently verify that exact corrected SHA, rerun baseline/N04 and at least 12 newly designed synthetic negatives. A's outcomes cannot be counted as D's.
4. E may re-evaluate after a fresh D report. Even local synthetic PASS cannot remove `PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE` without independent, separately authorized actual-host boundary evidence.
5. Separately unresolved human decisions: H01–H20 actual-host/ACK/durable custody, CSM owners and C-0/C-1/C-2, individual #106/#108 disposition, FXNS ledger implementation, provider source/rights/point-in-time validation and any pilot.

## Research stop preserved

- FXNS: `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN / NO_QUALIFIED_ALTERNATIVE`.
- CSM I2: `BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED`. Existing pinned gate blob `19442215345b35b0db3910c01acd910a5d57889b` unchanged.
- #106/#108 human disposition PENDING; all synthetic/report PRs HOLD_NO_MERGE.
- No live news/GDELT/market prices/ECB data, trading, actual host/model ingress, CI, merge or gate changes are authorized or performed here.
