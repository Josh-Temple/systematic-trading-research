---
id: GATE-CSM-I2-20261001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
updated_at: 2026-10-02
status: BLOCKED
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: INT-CSM-I1-20261001
  - type: derived_from
    target: AUDIT-CSM-E-20261001-REAUDIT-01
  - type: derived_from
    target: DEC-CSM-003-POST-E-REAUDIT-20261002
---

# Packet I outcome-access gate — BLOCKED / CLOSED

## Current decision

- Packet I I1: **PARTIAL_WITH_GAPS**.
- I2: **BLOCKED**; gate status **CLOSED**; market outcome access **false**.
- HYP-CSM-002 remains **UNTESTED**; scientific status **NOT_APPLICABLE**.
- E completed an independent re-audit of D's current head. Audit `AUDIT-CSM-E-20261001-REAUDIT-01` is **PARTIAL_WITH_GAPS / BLOCKED**; it does not satisfy the gate's required E PASS.
- No full-history capture or market-outcome calculation was made. No X instruction is issued.

The accepted and frozen SPEC identities remain unchanged. D's config remains FROZEN. E independently reran D's exact 53-test suite and its synthetic oracle. It confirmed outcome-blind score identities, positive/negative synthetic signature checks, and exact raw-source-lock-byte binding in the tested scope. E also found D's current I2 and E audit identity pins are stale and reproduced a compound persistence failure that leaves a success receipt after promotion reports failure. Neither finding authorizes capture.

## Current input refs

| Input | Exact ref / identity |
|---|---|
| main | `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c` |
| Architecture PR #31 | `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`, open/unmerged |
| Frozen SPEC | blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`; SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2` |
| C / PR #35 | head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` |
| D / PR #34 | head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`, open/draft/unmerged |
| E / PR #38 | head `4f683901d01fd6b5ce161c874118a34d40bcac82`, open/draft/unmerged; audit `AUDIT-CSM-E-20261001-REAUDIT-01` |
| I / PR #37 before this refresh | head `c2fdbc1f2a9fcccc32717b130a36433819aaa2fa`; this commit refreshes the E receipt |

## Current D deliverable identities

| Artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `csm.py` | `95cf059a5e0d5b6742dfa885fce7b37c58f2362c` | `4db33063f0388b8b7ec0613fff8228a4aa3cb00b94855a557c5abcd3b86f4104` |
| `test_csm.py` | `e287ab6923d073058cfa0e5e7be46b9ea5bc537a` | `3499c6cf4bc52f5052c7ed76ef92da41c272cbb6a31980a51801372775f1f66f` |
| `config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` | `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` |
| `RUNBOOK.md` | `3142c0291aa979bb80c28d71b4e47fc7408591ab` | `7fa355a6b071567ff6d4ea4290033f5635fc44b64159af2438acae69ecc14948` |
| `ENVIRONMENT.md` | `bf6d5b4c0381e967226ee0996736d858b524b8eb` | `8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f` |
| `RESULT.md` | `98e36e22a797806d1ee66438825d7a75f42ff21a` | `91fba806a72a9d4e103b535d4acc10b525476f7901700ff1279845bfff2a6923` |
| `TEST_MATRIX.md` | `03633916f0190925a01d6b26e5146956e657c31f` | `7cfbd342057ce8a9517fbbf44e464fb05beb60e6de82e47f4e1d8643e7da4bce` |
| `TEST_LOG.txt` | `c70e610064f92ba15527fb7f99b8796607a9a91f` | `84a6a88673b0502b53bf3b2eb0ca100d101d8bd57cfab3da08695285fc399f44` |
| `fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |

E independently reproduced D's 53/53 result from exact D bytes and the three permitted C metadata files. Its oracle used synthetic test cases only; this does not establish source readiness or market performance.

## Current E audit identities

| Artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `RESULT.md` | `e94a0c7ece92046d9abe5dd77d056a0291b9b461` | `69114a4c56164e36e508b46c3565f9ddc4d7ef3b5b78315cfbe8384a6228c372` |
| `AUDIT_MATRIX.csv` | `cd9625bef4f462e441d9cd581c9207d3d89331fb` | `5201506d5be8db71e281e8a59b2264cf33f9e3493621fdfc227f0d633b903062` |
| `toy_oracle.py` | `940c46da336a887b3ff7231b5f8aef747a289f30` | `1c2e7963d2891a0c5e62479c5ca51df65a71b2a89aa8566cbeec1f3ca42eb6c3` |
| `TEST_LOG.txt` | `54716715f0ea42a56b06e34924026402bf96c0e6` | `f3397bb632bbba146413e79e4adcf8b7ccf0d2a190ac3d1d3cdbe22eb64a2342` |

The audit result binds to current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779` and current I head `c2fdbc1f2a9fcccc32717b130a36433819aaa2fa`. The earlier E audit `AUDIT-CSM-E-20261002` at head `d1335b29eeb01cdd4b71cd5ded62033b8468e539` remains historical and unchanged; its findings against old D head `4f739d9cc2b21c138771afec4a728bf2b57060ba` are superseded where the new re-audit independently checked the corrected code.

## Current gate condition matrix

| Condition | Status | Evidence / open work |
|---|---|---|
| Human contract and frozen SPEC bytes | PASS | Exact acceptance and frozen identities remain verified; no science contract change. |
| D config to frozen SPEC | PASS | Current config blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` / SHA-256 `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` remains FROZEN. |
| Pair math, score-identity ledger, temporal boundary and fixed bootstrap | PASS | E's exact-ratio oracle, ledger target-invariance tests and fixed bootstrap checks passed on synthetic inputs; no market inference follows. |
| D 53-test suite | PASS | E independently reran 53 tests from the exact current D snapshot; all passed. Synthetic/code evidence only. |
| Signed receipt checks and raw source-lock bytes | GAP | Tested signatures, roles, principals, revocation/expiry and raw-byte mismatch checks passed. D's current I gate and E audit pins are stale, so exact current receipt binding fails. Production key provisioning is absent. |
| Atomic persistence and failed-promotion semantics | BLOCKED | Single injected failures passed, but compound parent-directory fsync plus rollback-deletion failure leaves `run-receipt.json` in the final directory after reported promotion failure. |
| Independent E audit satisfies the gate | BLOCKED | Current audit is complete but PARTIAL_WITH_GAPS and recommends BLOCKED, not PASS. |
| Source history, external calendar authority, missing/status and vintage readiness | BLOCKED | C qualifies bounded route/schema/calendar only. Full-history coverage, observed missing/status distribution, historical publication timing, revision/vintage and external calendar authority remain unresolved. |
| Production trust root/key distribution | BLOCKED | No production trust-store or key fingerprint/distribution evidence. |
| OS isolation, filesystem allowlist, durable destination and append-only access/attempt ledger | BLOCKED | These platform/operations controls remain unestablished. |
| Named outcome-access operator | BLOCKED | X is a role; no named person/account is assigned. |
| C and Integrator exposure dispositions | BLOCKED | Human disposition remains pending; no observation values are reproduced. |
| B artifact path/base conformance | GAP | B deliverables remain outside line-relative paths and based on an older merge-base; remediation belongs to B's owner. |
| Original pre-proposal brief traceability | GAP | Original brief is absent from repository receipts; exact SPEC acceptance/freeze remains verified. |
| Restricted-boundary and no-result controls | PASS | No market outcomes or H3/Pilot/live/broker inputs were accessed in this I refresh. |

## Required work before any I2 reconsideration

1. D must resolve current I2/E identity binding with a non-circular design, update code and operator identity references, and publish fresh exact D hashes.
2. D must fix the compound promotion/rollback failure so that failed promotion cannot leave a success receipt; add the reproduced compound fault as a regression test and rerun the full suite.
3. E must re-audit any changed D inputs. Keep the gate closed until a current E result satisfies the gate.
4. Platform/security, storage/platform and research-operations owners must provide production key, isolation, allowlist, durable output/access ledger, and named-operator evidence.
5. Source readiness and external calendar authority must be established under an approved metadata-only process. Human exposure dispositions remain required.

No capture, market-outcome access, or experiment run is approved by this record. D's test pass and E's synthetic PASS items do not open I2.

## No-result and access receipt

No market price/history, ranking, forward return, strategy metric, P/L, Sharpe, performance plot, or run/result record was read, generated, or calculated during this I refresh. No C raw probe CSV or OBS_VALUE value was read. Gate remains CLOSED; no instruction was issued to X.
