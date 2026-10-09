# C — CSM E/I signing principal and public-key separation (2026-10-10 Wave)

## Decision
**IMPLEMENTED_NOT_RUNTIME_VERIFIED / HOLD_NO_MERGE**. The constrained candidate code and new synthetic negative fixtures are committed, but **the updated production-path test suite was NOT_EXECUTED** in this session. Neither a static test count nor historical Actions runs establish the current candidate's functional PASS. The C acceptance condition remains unfulfilled until exact-HEAD offline execution and readback are recorded.

## Inputs and frozen boundary (fresh read)
- Repository: `Josh-Temple/systematic-trading-research`
- PR #34 OPEN/DRAFT; base `research/csm-architecture-review-20261001`, branch `work/csm-implementation-20261001`, head **`3695f0a8ed085669ec3644826889f9fc953a6808`** at start and pre-write.
- I2 PR #37 OPEN/DRAFT, `9162cae4f2e64ee3da07517f12a16092cc170161`; gate `BLOCKED / CLOSED / market_outcome_access=false`. No gate mutation.
- D synthetic-control PR #83 OPEN/DRAFT, toy-only 23/23 reported, not evidence of the actual `csm.py` runtime path.
- E PR #86 OPEN/DRAFT, `5debb307efd36958045401121295c619b6f1c56b`, `HOLD_NO_MERGE`.
- Historic D `TEST_LOG.txt` blob `4d8e6615a64ea9d5da8fc71fbbda4a4ee67db5ba` describes **56/56** tests of an older tree via PR #49 / run `37165967827`; **not this candidate's test result**.
- No XM/MT5, ECB history, observed market values, external-source HTTP, real news, market outcomes, or trading were accessed. The frozen SPEC, source lock, gate, workflow, runner and existing receipts were untouched.

## Candidate delta (base to scoped branch)
1. `work/implementation/csm.py`: previous Git blob `dbddf33895bc565e215583ad0056c9aba5ed3c1a` → `cc3b788d637d0bacf63d9642788a196a1feaac56`. Following **successful individual** auditor-role and integrator-role signature verification, the existing `validate_gate_receipt` now rejects equal E/I key IDs, equal trusted principal IDs, or the same mathematical RSA modulus behind distinct key IDs (even noncanonical hex aliases). Existing RSA/SHA-256, validity, revocation, signed source-lock and identity checks remain in place.
2. `work/implementation/test_csm.py`: previous Git blob `27920cfa92546aba07781915032c7bb5ae999549` → `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282`. The old fixture used one RSA modulus for both roles. The new synthetic-only fixture gives I its own generated 2048-bit test modulus and exponent, leaving E's original toy RSA pair in place. Test signatures are never production credentials.
3. Six new `GateAndReceiptTests` exercise positive separate principals/public keys, re-signed same-principal rejection, re-signed same-modulus-with-key-alias rejection, role/revocation/key-validity rejection, stale current I2/E identity mismatch, and mutated E signature. These cases call `csm.validate_gate_receipt` and, in both re-signed adversarial cases, also call the **existing** `csm._verify_signed_envelope` directly to distinguish valid individual signatures from failure of signer independence. Baseline and new tests total **62 test method definitions (static count, NOT execution)**.
4. Unchanged identity/content constraints include the outer I2 signature binding E-envelope bytes and D code hashes, `gate_status=PASS`/human freeze checks, and current I2/E status requirements. No new algorithm, alternate source or outcome override.

## Execution evidence and explicit limitations
- Remote GitHub source, current PR snapshots, full original code/test blobs and changed-path comparison: **READ**.
- Candidate `csm.py` and `test_csm.py` saved and separately fetched: **SAVED / READBACK**.
- `python3 -m py_compile csm.py test_csm.py`: **NOT_EXECUTED**.
- `python3 -m unittest -v test_csm.py` (metadata-only Packet C environment per `RUNBOOK.md`): **NOT_EXECUTED**.
- Updated-suite count/pass/fail/error/skip and exact-HEAD job logs: **UNKNOWN / NOT_RERUN**. Historical 56/56 and toy 23/23 cannot be substituted.
- No Actions workflow was invoked. The only known `csm-source-readiness` workflow has a risk of market-history acquisition, so it must not be used as an offline verification surrogate. Independent offline workflow trigger/checkout safety has not been confirmed.
- Current C result is **not** production key-custody assurance, OS/ACL denial proof, trusted key provisioning, human approval, or source-currentness/vintage validation.

## Required completion before E can treat C as scoped functional evidence
A separate authorized offline runner must check out the **exact final candidate HEAD** and read-only metadata fixtures (with known Packet C hashes), confirm no source/history/network path executes, record Python version and exact command, run `python3 -m py_compile csm.py test_csm.py` and `python3 -m unittest -v test_csm.py`, capture all normal and adversarial assertions plus number of passed/failed/errored/skipped tests and the exact checkout tree. Re-fetch code/test blobs and job logs. If any test fails or source/history access is required, **STOP/HOLD**; do not promote or merge.

## Unchanged gate and external responsibilities
**I2 BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED.** No #34/#37/#53 merge and no market-outcome access. Real separate people and key custody, root-owned trust store, OS-level isolation, durable tamper-evident attempt ledger, real restart/readback, explicit named operator, incident decision, independent current E audit, human authorization, external calendar, H placeholder, ZIP member-byte verification, and point-in-time vintage remain unresolved.
