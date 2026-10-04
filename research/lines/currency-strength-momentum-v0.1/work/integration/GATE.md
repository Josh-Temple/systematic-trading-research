---
id: GATE-CSM-I2-20261001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
updated_at: 2026-10-04
status: BLOCKED
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: AUDIT-CSM-E-20261004-REAUDIT-02
---

# Packet I outcome-access gate — BLOCKED / CLOSED

## Current decision

- I2: **BLOCKED**
- gate: **CLOSED**
- `market_outcome_access=false`
- HYP-CSM-002: **UNTESTED**
- DATA-CSM-002: **PLANNED / NOT_CAPTURED_FOR_EXPERIMENT**
- EXP-CSM-002: **PLANNED / NOT_RUN**
- no X instruction is issued

The two Packet D code blockers found by the previous independent E re-audit are now independently resolved. They are no longer reasons to keep I2 closed.

I2 remains closed because source-readiness and production-execution controls are not yet evidenced.

## Frozen scientific contract

- SPEC: `SPEC-CSM-002-v01`
- Git blob: `7fe114e2fcfa33b0565b51c717455abd8837d5d9`
- SHA-256: `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`
- freeze status: **FROZEN**
- scientific body: unchanged

## Current D

PR #34:
- head: `3695f0a8ed085669ec3644826889f9fc953a6808`
- full synthetic suite independently rerun by E: **56/56 PASS**
- no market observations used

Current key D identities:

| Artifact | Git blob | SHA-256 |
|---|---|---|
| csm.py | `dbddf33895bc565e215583ad0056c9aba5ed3c1a` | `f57c859dd137bb49f23a23ddf2760681bc3ca14aa23cf82e03e2f35bc5b54535` |
| test_csm.py | `27920cfa92546aba07781915032c7bb5ae999549` | `899332a9e51018d6140a201105eccdad8154d075af1a32354776621976185bf2` |
| config.json | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` | `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` |
| RUNBOOK.md | `4168e0010060586e0301aa221ec653913ea721ea` | `bba147d4da072507ba255cb15a93a9fe0e76fda7df822fe4cfcf626501b91fb7` |
| ENVIRONMENT.md | `bf6d5b4c0381e967226ee0996736d858b524b8eb` | `8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f` |
| RESULT.md | `2b6accb202e8206bf26b5b642a5b2b564a9f639a` | `3c48c47f87634346ac4c02ff1c73a32f640b50d429f2e303d5668bb7c2eff0ea` |
| TEST_MATRIX.md | `266f4ffc51d215702a60dd077d3cd611ae81cef2` | `d5dfa2c76dcaf2c803755d0a03aac803550ce793ad84c7d35257ec899971e0ca` |
| TEST_LOG.txt | `4d8e6615a64ea9d5da8fc71fbbda4a4ee67db5ba` | `8b6f5f9c2c6527c9c1b6535ba5fdbdcd6394b2259ce947949a52720734cf3b3b` |

## Current independent E

PR #38:
- head: `970ea9b77e062e7acbc67432993797a0cb4e0d01`
- audit: `AUDIT-CSM-E-20261004-REAUDIT-02`
- status: **PARTIAL_WITH_GAPS**
- recommendation: **BLOCKED**
- workflow run: `37166456105`

Canonical E identities:

| Artifact | Git blob | SHA-256 |
|---|---|---|
| RESULT.md | `59ece59a96fe3f7bb9e36da5e93bc56a4ddcd7cd` | `3e9f6e972ce9065ba498a366daa88fbfe09bf8c1261655bf8ffdb3d4e231003f` |
| AUDIT_MATRIX.csv | `4ba6cbbddf731e5e226b56af1d4d84847c586cf5` | `c3d19bdc8f46e271aaf5e6c04741a21c1c2813864e21e23790c5b2e7aad354bd` |
| toy_oracle.py | `f75cb2311d1ac1f6c952cd080e8e3f0016033c69` | `5b62f25efdf8937d00204b65e40c0117a13cb111f3f53d5b5d9fd4701ccda0b4` |
| TEST_LOG.txt | `11e0732a261f01ee4d046801d585fa1b30bd3482` | `02cda107912c6a883cb471eb2cd86c46794930d84c0c5995beed51d9d03ba945` |

### D findings now PASS at code/synthetic scope

1. **Non-circular current I/E identity binding — PASS.**
   E verified rotating immutable I/E identities do not require a D code edit, while E evidence against different D bytes is rejected.

2. **Compound promotion/rollback semantics — PASS.**
   E reproduced the prior final-fsync + rollback-delete compound fault. Promotion failed and no SUCCESS `run-receipt.json` remained.

These findings are preserved historically under E's `history/` directory and are superseded only for this exact D head.

## Remaining blocking conditions

| Condition | Status | Required evidence |
|---|---|---|
| Frozen human contract | PASS | already fixed |
| D math / outcome-blind ledger / bootstrap | PASS | E independent synthetic audit |
| D current-gate binding design | PASS | E dynamic I/E binding checks |
| D persistence failure semantics | PASS | E compound-fault re-injection |
| Source full-history coverage | **BLOCKED** | metadata-safe evidence that required series cover the frozen source interval |
| Actual missing/status distribution | **BLOCKED** | outcome-blind source-readiness receipt; no result interpretation |
| External calendar authority | **BLOCKED** | independent authority/metadata evidence for expected reference dates |
| Historical publication/revision/vintage | **BLOCKED** | either verify or explicitly preserve latest-vintage-only boundary and prove it is consistent with the frozen claim |
| Production trust root | **BLOCKED** | provisioned trusted Integrator/auditor public keys, fingerprints, roles, validity, revocation, protected trust-store evidence |
| OS/process isolation and filesystem allowlist | **BLOCKED** | versioned policy plus negative denial probes |
| Durable output destination | **BLOCKED** | protected destination and restart/readback proof |
| Append-only/tamper-evident access/attempt ledger | **BLOCKED** | durable ledger incl. denied attempts, retries, operator and hashes |
| Named outcome-access operator | **BLOCKED** | stable approved human/account identity |
| Exposure disposition | **BLOCKED** | human disposition of prior C/Integrator observation exposures without reproducing values |

Other lineage gaps (B path/base conformance and original brief traceability) remain recorded but are not used to change the frozen scientific contract.

## Current I input identity before this refresh

The prior I head was `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`.

Its gate was correctly CLOSED:
- gate.json blob `bfa515df80fb855749d8df1e5ce9d657b8f3f495`, SHA-256 `3c57f65ede07695764fabc13964bb2d98c6b418166b687ca9662dd02cd839a4d`
- GATE.md blob `62e8399821d7e8c168672f93c1dbc7155deca4b2`, SHA-256 `4eac722fc0c34cbfecf2bca99bdbaed236c209575e3c242ec3ab8311711e5648`

E verified D rejects that CLOSED identity. No bypass exists.

## Next work

Do **not** redesign D for the two resolved findings unless its bytes change.

Next priority:
1. source-readiness / calendar / vintage qualification;
2. production execution-control evidence;
3. human exposure disposition;
4. fresh I reconciliation.

Until those are complete, no full-history capture and no market-outcome calculation are authorized.

## No-result receipt

No market history, ranking, forward return, strategy P/L, Sharpe, performance plot, broker/live/paper input or Result was read, generated or calculated in this refresh.
