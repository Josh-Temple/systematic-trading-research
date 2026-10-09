# D — CSM #90 exact-head synthetic signer-runtime independent audit (BLOCKED)

- Audit date: 2026-10-10 JST (not an execution or approval timestamp).
- Decision: **BLOCKED / HOLD_NO_MERGE**; independent *static* review completed, but this Wave's C offline execution report, exact checkout identity, test output and execution log were **not available** when D checked the current open PR list immediately before this report branch was created.
- Scope: **synthetic production-path signer separation only**. This receipt does not approve CSM integration, I2, sources, market outcome access or trading.
- Evidence classes: **REMOTE_GITHUB_READ** for code, test, PR, Git trees and gate; **STATIC_INDEPENDENT_REVIEW** for individual tests and validation flow; **NOT_EXECUTED / NOT_RERUN** for the candidate's Python test suite. Prior tests are historical citations only.

## Exact GitHub identities independently read

| Item | GitHub state / identity |
|---|---|
| Candidate PR | [#90](https://github.com/Josh-Temple/systematic-trading-research/pull/90), OPEN/DRAFT, base `work/csm-implementation-20261001`, head `work/csm-signature-separation-20261010-c` |
| Candidate code under audit | commit `94e7719839dcacf281d7d479c597222582f0d920`; Git tree `32e851594810e51a3aefd05ca7cdc17af341885d` |
| `work/implementation/csm.py` | Git blob `cc3b788d637d0bacf63d9642788a196a1feaac56` |
| `work/implementation/test_csm.py` | Git blob `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282` |
| `work/implementation/fixtures/toy_cases.json` | Git blob `4e925eabb4d88772806f0e109c15680f17d73a31` |
| `work/implementation/RUNBOOK.md` | Git blob `4168e0010060586e0301aa221ec653913ea721ea` |
| `work/implementation/config.json` | Git blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` |
| C candidate's preceding report | `work/implementation/2026-10-10/C_SIGNER_INDEPENDENCE_RESULT.md` blob `cd11e9829adffd1556ae969421947fd622415d78`; explicitly states **NOT_EXECUTED** |
| Packet C metadata-only source | PR [#35](https://github.com/Josh-Temple/systematic-trading-research/pull/35), head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` |
| Current I2 gate | PR [#37](https://github.com/Josh-Temple/systematic-trading-research/pull/37), head `9162cae4f2e64ee3da07517f12a16092cc170161`; `work/integration/gate.json` blob `19442215345b35b0db3910c01acd910a5d57889b` |

PR #90's complete changed filenames were listed: only `work/implementation/csm.py`, `work/implementation/test_csm.py`, and `work/implementation/2026-10-10/C_SIGNER_INDEPENDENCE_RESULT.md` (all under the CSM research-line prefix). No #90 HEAD movement was seen at the pre-write refresh. No separate **new C offline-execution report-only Draft PR** was present in the freshly fetched open PR list. A later C report must be independently audited afresh rather than inferred from this absence.

## Independent inspection of signed validation and adversarial test definitions (STATIC, NOT RUN)

1. In candidate `csm.py`, `_verify_signed_envelope` requires the trusted key ID, exact `RSASSA-PKCS1-v1_5-SHA256` algorithm, expected role, non-revoked key, matching principal, bounded issuance/expiration and key validity, then cryptographically verifies the signature. This is code-path inspection, **not an observed PASS**.
2. `validate_gate_receipt` checks current I2/E signed identities, source-lock raw-byte and object identities, calendar, frozen SPEC, D file hashes and environment, plus authorization fields. After separately calling `_verify_signed_envelope` for E as `independent_auditor` and I as `integrator`, lines around 637–653 reject (a) equal key IDs, (b) equal trusted `principal_id`, (c) mathematically equal RSA moduli using base-16 integer comparison even if key IDs or hex serialization differ. Static code therefore *defines* the required fail-closed separation; functional behavior remains unverified.
3. Candidate `test_csm.py` contains an explicit positive fixture with distinct principals and moduli, and named negative test methods for re-signed **same principal**, re-signed **same modulus behind distinct key IDs**, role-swap/revocation/future key validity, stale I2/E identities, and altered E signature. Both signed-collision tests explicitly call `csm._verify_signed_envelope` for the individual E/I signatures before expecting `csm.validate_gate_receipt` to reject the combined receipt. These are **source definitions**, not executed assertions.
4. Other inspected source includes tests for a CLOSED gate, unknown signing key, tampered signature and expired receipts; the integration test reads only the three environment-variable-selected Packet C metadata files when supplied, and otherwise calls `skipTest`. An apparent test-method count of 62 is **not** an execution count; `skip=0` has not been demonstrated.
5. The source review does **not** demonstrate actual independent human signers, real key custody, protected trust-store ownership, ACLs, durable append-only ledger, production restart/readback or authorization.

## Packet C metadata identity boundary

Source tree at PR #35 contains precisely the three expected **metadata-only** input blobs for this suite:

| Input | Expected / observed Git blob in #35 tree | SHA-256 stated in RUNBOOK (not independently recomputed in D) |
|---|---|---|
| `source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| `probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| `expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |

D verified the **Git tree's blob IDs and test's expected blob literals**, but did **not** claim to independently download, locally hash and execute on all three metadata files. In particular, no C-owned local file hashes or full runtime test log were available to cross-check. Do not infer an independently reproduced SHA-256 comparison or packet-validation PASS.

## Execution and prerequisite matrix

| Required evidence | D observation / decision |
|---|---|
| C report-only Draft PR under `work/implementation/2026-10-10/offline-execution/**` and remote readback | **NOT_FOUND_AT_CHECK / BLOCKED** |
| C executed exact checkout SHA/tree, `py_compile`, and `unittest -v test_csm.py` | **NOT_ESTABLISHED**. Old #90 report says NOT_EXECUTED |
| C's Python version / start-end time / test totals and fail/error/skip / exact runtime log | **NOT_AVAILABLE**. Never convert 62 static methods to 62 PASS |
| All three Packet C runtime input SHA-256 values checked from execution bytes | **NOT_ESTABLISHED** (known Git blob IDs and documented SHA-256 alone insufficient) |
| Independent D exact-head suite re-run and direct positive/negative observation | **NOT_RERUN**. Container runtime could not reach GitHub for a safe exact checkout (name resolution failed). No Actions or source-readiness workflow was triggered |
| Older toy 23/23 and old D 56/56 | **HISTORICAL_ONLY**, different test tree and no substitution for #90 |
| Candidate code logic/test *definitions* correspond to same #90 exact tree | **STATIC_MATCH** at the exact Git blobs above; not an execution result |
| Current I2 actual gate | **BLOCKED / CLOSED / `market_outcome_access=false`**, read from PR #37 `gate.json` |

**Decision rationale:** the mandatory C execution prerequisite has not been established. A static source-code match cannot demonstrate that the signed collisions are rejected at runtime or that the valid separate-key case executes without over-rejection. Consequently D's runtime assurance is **BLOCKED** (not `PASS_SCOPED`). If C submits an exact-head offline-execution report later, the reviewer must re-read its HEAD, code/test/fixture blobs, Packet C hashes, complete command and logs, then provide a **new** independent runtime decision. This document must not be retroactively upgraded to PASS.

## E handoff / non-authorizing gates

**E: HOLD_NO_MERGE for CSM #90.** Do not merge #90, #34, #37, #53 or source/gate changes on this receipt. The already-observed I2 state is `BLOCKED`, the gate is `CLOSED`, and `market_outcome_access=false`; `HYP-CSM-002 UNTESTED` remains unchanged. The production separation of actual people and cryptographic key custody, protected trust store, OS/process isolation, durable ledger, restart/readback, named X operator, incident exposure human disposition, calendar authority, source vintage/ZIP member identity, separate current E approval and explicit human authorization all remain independent open gates.

No real source records, ECB observed values, history/ZIP, external HTTP, outcome samples, trading, keys, production runner or workflow execution were touched. No code/tests/config/SPEC/source lock/gate/workflow were edited by D. This report is a scoped **independent HOLD** and is not a scientific result or release approval.
