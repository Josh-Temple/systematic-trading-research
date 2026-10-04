---
audit_id: AUDIT-CSM-E-20261004-REAUDIT-02
status: PARTIAL_WITH_GAPS
scientific_status: NOT_APPLICABLE
recommendation: BLOCKED
i2_gate_status: BLOCKED_CLOSED
market_outcome_access: false
audit_date: 2026-10-04
---

# Packet E independent re-audit of hardened Packet D

## Decision

This audit binds to:

- Packet D head `3695f0a8ed085669ec3644826889f9fc953a6808`;
- current Packet I head `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`;
- Packet C metadata head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`;
- frozen `SPEC-CSM-002-v01` blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`.

**Overall status remains PARTIAL_WITH_GAPS / recommendation BLOCKED. I2 remains CLOSED and `market_outcome_access=false`.**

The reason is no longer the two Packet D code defects identified by the prior E audit. Both have been independently re-tested and are resolved in the audited D bytes.

The remaining blockers are source-readiness and production/operational controls outside the synthetic D implementation:
- external calendar authority;
- full-history source coverage and observed missing/status distribution;
- historical publication timing and revision/vintage;
- production trust-key provisioning and protected trust store;
- OS-level file/process isolation and filesystem allowlist;
- durable protected output storage and append-only attempt/access ledger;
- named outcome-access operator;
- human disposition of the prior exposure disclosures.

No market outcome was accessed or computed.

## Independent execution

Audit-only GitHub Actions wrapper:
- PR #51
- workflow: `CSM E independent re-audit 20261004`
- run: `37166456105`
- job: `111330239715`
- result: **SUCCESS**

The wrapper materialized exact Git objects for D, I, C metadata and the frozen SPEC. It did not use D's self-report as the test result.

### Exact D suite

The exact D snapshot was compiled and independently rerun with only the three permitted Packet C metadata inputs.

Result:
- **56 tests run**
- **56 passed**
- **0 failed**
- **0 skipped**

The three regressions added after the prior E finding passed:
- compound final-directory-fsync plus rollback-delete failure never leaves `run-receipt.json`;
- signed I/E identity rotation does not require a D code-pin update;
- signed E attestation must bind exact current D file hashes.

## Independent E oracle

E's separately authored oracle passed all seven current checks:

1. synthetic formula, 56-pair, quote, tie, numeraire and baseline oracle;
2. formation score-ledger target-value and target-availability invariance;
3. trusted-key, role, principal, signature, revocation and expiry controls;
4. raw source-lock bytes and dynamic signed I/E binding;
5. fault-injected atomic persistence and promotion;
6. independent fixed circular bootstrap and decision boundaries;
7. exact permitted Packet C metadata identity and internal validation.

There were **no `GAP_REPRODUCED` lines** in the current oracle run.

Oracle identity used by the successful wrapper:
- Git blob: `f75cb2311d1ac1f6c952cd080e8e3f0016033c69`
- SHA-256: `5b62f25efdf8937d00204b65e40c0117a13cb111f3f53d5b5d9fd4701ccda0b4`.

## Prior D code blockers — current disposition

### 1. Mutable I/E identity pins

**Prior result: BLOCKED. Current code-level result: PASS.**

The audited D no longer embeds mutable I/E commit SHAs as production authorization constants.

E independently verified:

- the exact current I artifact is still CLOSED and is rejected;
- a structurally valid, trusted Integrator-signed PASS I identity can rotate head/blob identities without changing D code;
- a separately trusted auditor-signed PASS E attestation can rotate its immutable artifact identities without changing D code;
- E must bind the exact D file-hash map, environment identity, frozen SPEC, source-lock raw bytes and calendar;
- tampering the audited D hash in the E attestation is rejected.

This removes the prior D→I/E commit-pin cycle without weakening D-byte binding.

This synthetic PASS does **not** supply production signing keys or create an actual PASS I/E receipt.

### 2. Compound promotion / rollback failure

**Prior result: BLOCKED. Current code-level result: PASS.**

The prior audit reproduced a failure sequence in which a final destination-directory fsync failed, rollback deletion also failed, and a SUCCESS `run-receipt.json` remained.

In the current D sequence, the pending marker is removed and directory-fsynced before the final success receipt is published. `run-receipt.json` is the final fallible success-path commit operation.

E independently re-injected the same compound class. Promotion failed as expected. Even when rollback directory deletion was also forced to fail, **no `run-receipt.json` remained**.

A failed-attempt directory may remain when deletion itself fails. It is not a successful run because it has no final SUCCESS receipt.

## Exact D identities independently bound

| Artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `csm.py` | `dbddf33895bc565e215583ad0056c9aba5ed3c1a` | `f57c859dd137bb49f23a23ddf2760681bc3ca14aa23cf82e03e2f35bc5b54535` |
| `test_csm.py` | `27920cfa92546aba07781915032c7bb5ae999549` | `899332a9e51018d6140a201105eccdad8154d075af1a32354776621976185bf2` |
| `config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` | `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` |
| `fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |
| `RUNBOOK.md` | `4168e0010060586e0301aa221ec653913ea721ea` | `bba147d4da072507ba255cb15a93a9fe0e76fda7df822fe4cfcf626501b91fb7` |
| `ENVIRONMENT.md` | `bf6d5b4c0381e967226ee0996736d858b524b8eb` | `8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f` |
| `RESULT.md` | `2b6accb202e8206bf26b5b642a5b2b564a9f639a` | `3c48c47f87634346ac4c02ff1c73a32f640b50d429f2e303d5668bb7c2eff0ea` |
| `TEST_MATRIX.md` | `266f4ffc51d215702a60dd077d3cd611ae81cef2` | `d5dfa2c76dcaf2c803755d0a03aac803550ce793ad84c7d35257ec899971e0ca` |
| `TEST_LOG.txt` | `4d8e6615a64ea9d5da8fc71fbbda4a4ee67db5ba` | `8b6f5f9c2c6527c9c1b6535ba5fdbdcd6394b2259ce947949a52720734cf3b3b` |

## Current I identity and state

Fresh I input:
- head: `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`;
- `gate.json` blob: `bfa515df80fb855749d8df1e5ce9d657b8f3f495`;
- `gate.json` SHA-256: `3c57f65ede07695764fabc13964bb2d98c6b418166b687ca9662dd02cd839a4d`;
- `GATE.md` blob: `62e8399821d7e8c168672f93c1dbc7155deca4b2`;
- `GATE.md` SHA-256: `4eac722fc0c34cbfecf2bca99bdbaed236c209575e3c242ec3ab8311711e5648`;
- gate state: **CLOSED**;
- `market_outcome_access=false`.

E verified that current CLOSED I fails the new D structural authorization check. The code-level non-circular design therefore does not bypass the gate.

## Source and operational gaps that remain blocking

### Source readiness

The three allowed Packet C metadata artifacts remain internally valid and byte-identified. This audit does not turn them into proof of:

- complete 2009-11 through 2026-09 history;
- actual missing/status distribution;
- historical publication timing;
- historical revision/vintage availability;
- independent external calendar authority.

These remain source-owner/integration work.

### Production trust and execution environment

Synthetic RSA keys establish only validator behavior.

Still absent:
- provisioned production Integrator and independent-auditor public keys;
- independently checked fingerprints, roles, validity and revocation state;
- protected root-owned/non-writable trust-store evidence;
- OS-level restricted run identity;
- filesystem allowlist and negative denial probes;
- process isolation;
- durable protected output destination and restart/readback evidence;
- persistent append-only/tamper-evident attempt/access ledger;
- named approved outcome-access operator.

### Exposure and lineage

I still records prior observation-exposure disclosures requiring disposition. E did not reproduce or read the values.

B path/base conformance and original pre-proposal brief traceability remain lineage gaps. They are not corrected by this audit.

## Recommendation

**BLOCKED — keep I2 CLOSED.**

Packet D's two prior code-level blockers are resolved for the exact audited D head.

The next I2 reconsideration should not request further D redesign for those two findings unless D bytes change. It should focus on:

1. source readiness / calendar authority / vintage evidence;
2. production trust-key and execution-isolation evidence;
3. durable destination/access-ledger and named-operator evidence;
4. human exposure disposition;
5. then a fresh Integrator gate using the audited D identity and current E result.

No full-history capture, market ranking, forward return, strategy metric, P/L, Sharpe, performance plot or X execution was performed by this audit.

## Historical preservation

The prior re-audit that reproduced the stale-pin and compound-receipt failures is preserved unchanged under:
- `history/RESULT_20261002_REAUDIT.md`;
- `history/AUDIT_MATRIX_20261002_REAUDIT.csv`;
- `history/TEST_LOG_20261002_REAUDIT.txt`.

Those negative findings remain part of the research record and are superseded only for the exact D code paths independently re-tested above.
