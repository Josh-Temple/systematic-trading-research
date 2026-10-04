---
id: DEC-CSM-003-POST-E-REAUDIT-20261002
type: Decision
research_line_id: RL-CSM-001
created_at: 2026-10-02
status: BLOCKED
decision: KEEP_I2_CLOSED
based_on:
  - INT-CSM-I1-20261001
  - AUDIT-CSM-E-20261001-REAUDIT-01
  - DEC-CSM-003-POST-D-20261002
  - HDEC-CSM-002-20261001
relations:
  - type: derived_from
    target: AUDIT-CSM-E-20261001-REAUDIT-01
  - type: derived_from
    target: DEC-CSM-003-POST-D-20261002
---

# Post-E re-audit decision — keep I2 closed

## Decision

Keep I2 **BLOCKED / CLOSED** and `market_outcome_access=false`. I1 remains PARTIAL_WITH_GAPS; HYP-CSM-002 remains UNTESTED. E completed an independent re-audit of current D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779`, but reports PARTIAL_WITH_GAPS and recommends BLOCKED. No X instruction is issued. This is not a DEPRIORITIZE decision and makes no claim about market performance.

The human acceptance and frozen SPEC remain unchanged. No canonical science, hypothesis, dataset role, period, or decision rule changed.

## Current E re-audit

PR #38 head `4f683901d01fd6b5ce161c874118a34d40bcac82` is open/draft/unmerged. Audit `AUDIT-CSM-E-20261001-REAUDIT-01` independently reran D's exact 53-test suite and ran a synthetic E oracle. It confirms formation-score identities are outcome-blind under synthetic target mutations, and confirms the tested signature, role/principal, expiry/revocation and raw-source-lock-byte checks.

Two D code-level gaps remain:

1. D pins an old I2 gate head and old E audit identity. It rejects the current I gate at `c2fdbc1f2a9fcccc32717b130a36433819aaa2fa` and this E audit identity. D's RUNBOOK and TEST_LOG also cite the old refs. D must design a non-circular identity binding, refresh its constants/docs and publish a new exact D head for another E audit.
2. A compound persistence failure was reproduced: parent-directory fsync fails after promotion and rollback deletion fails, while `run-receipt.json` remains in the final destination. D must ensure failed promotion cannot leave a success receipt, then add the compound fault as a regression test.

E also retains external/source and lineage gaps: no production trust-key provisioning, OS isolation, filesystem allowlist, durable output/access-attempt ledger, or named operator; external calendar authority, full-history coverage, missing/status distribution, historical publication timing and revision/vintage remain unverified; exposure dispositions are pending; B path/base and original-brief gaps remain.

## No-result boundary

No market history, outcome, ranking, forward return, strategy metric, P/L, Sharpe or performance plot was accessed or calculated by this I update or the E audit. DATA-CSM-002 remains PLANNED / NOT_CAPTURED_FOR_EXPERIMENT; EXP-CSM-002 remains PLANNED / NOT_RUN. The gate stays CLOSED and this decision authorizes no capture or experiment.
