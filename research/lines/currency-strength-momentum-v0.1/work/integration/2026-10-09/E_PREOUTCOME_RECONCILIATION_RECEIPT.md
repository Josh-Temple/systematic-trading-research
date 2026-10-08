---
id: CSM-E-PREOUTCOME-RECONCILIATION-20261009
date: 2026-10-09
worker: E
status: PARTIAL_WITH_GAPS
i2_state: BLOCKED
gate_status: CLOSED
market_outcome_access: false
integration_action: HOLD_NO_MERGE
---
# Worker E — CSM metadata assurance versus I2 authorization (2026-10-09)

## Integration decision
**PARTIAL_WITH_GAPS / HOLD.** Neither integration PR [#37](https://github.com/Josh-Temple/systematic-trading-research/pull/37) nor source-readiness PR [#53](https://github.com/Josh-Temple/systematic-trading-research/pull/53) is merged; `I2=BLOCKED`, gate `CLOSED`, `market_outcome_access=false`, HYP-CSM-002 `UNTESTED`. No runner, OBS_VALUE, ECB live API, broker/XM, outcome, returns, ranking or execution attempted in E. **No new CSM tests were run**, and no new acquisition job was triggered by E.

## Fresh identity and provenance
- `main`: `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` (unchanged).
- #37 current head `9162cae4f2e64ee3da07517f12a16092cc170161`; gate file blob `19442215345b35b0db3910c01acd910a5d57889b` directly read from this head: `state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`.
- #53 current head `dbe9574e2d03d8a34e099931078ba2de43c7606c`; `SAFE_RECEIPT.json` blob `0e27706cdb5f775d7bd302c56605a6800fa4da57` directly read, `overall_status=PASS` / `market_outcome_access=false`, source-lock SHA-256 `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71`, calendar SHA-256 `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4`.
- Independent Worker C [#78](https://github.com/Josh-Temple/systematic-trading-research/pull/78), head `20fd4d52fee72fda76f40a1a20511abc1315732e`: **archive metadata PASS_SCOPED, overall PARTIAL_WITH_GAPS**, no value inspection. Historical metadata CI `37167525175`; initial negative `37167323298` preserved. Seven fixed official ECB EXR keys and 4,331 expected dates 2009-11-01 through 2026-09-30 are provenance and missingness evidence **for that recorded snapshot**, not tradability.
- Independent Worker D [#76](https://github.com/Josh-Temple/systematic-trading-research/pull/76), head `927beace5b1e044712b7f7f574cd78bcd46a7f16`: **PARTIAL_WITH_GAPS**. Original E synthetic/independent 56/56 CI `37166456105` is historical, **NOT_RERUN here**, and attested older I `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`, not the current #37 SHA. Independent D implementation head `3695f0a8ed085669ec3644826889f9fc953a6808` is separately identified. Do not use stale signed I approval as current authorization.

## Reconciliation of stale I source labels
- #37's historical gate contains source rows marked unknown/blocked for full-history and external calendar; the subsequent #53 safe receipt plus Worker C reduces uncertainty about **historical snapshot metadata, expected calendar equivalence, locked source identity and missing/duplicate/status counts**.
- That evidence is not an update to `gate.json`, not an I2 PASS, and not evidence of same-day historical vintage availability. Worker C found the prospective H-placeholder acceptance guard fails to restrict dates to the locked range/closed-day set; archived ZIP member bytes were not independently compared; historical release/revision remains unverified. Preserved receipt and logs cannot be retroactively elevated to outcome proof.
- Historical exposure disclosures and initial negative source/implementation audits are preserved, not erased or revised; C reported incidental current quote snippets returned during a documentation search and no use of those values.

## Unresolved operational authorization blockers
1. Production trust root/key custody, issuer-vs-independent-auditor separation, protected signed envelopes and revocation inventory: **BLOCKED**.
2. Current I/E signed identity freshness: **PARTIAL**. Exact-D-code 56 tests do not sign the latest #37 head. Do not reuse old head attestation.
3. OS/filesystem/process/network isolated runner and independently verified synthetic denial probes: **BLOCKED**.
4. Protected durable output/readback, append-only tamper-evident **attempt and denial** ledger: **BLOCKED**.
5. Named X outcome-access operator, final distinct human I2 authorization and human disposition of past exposure: **BLOCKED**.
6. Source vintage, H closed-day acceptance fix/re-audit and independent artifact-member readback: **PARTIAL/BLOCKED**.

## Action boundary
A small future **synthetic-only / no-market** operational-control packet can supply named key custodian, trust signature role test, current-head freshness checklist, runner/path denial tests, durable ledger proof and separate human exposure decisions. Independently re-review before any gate change; only a *new* explicit human decision could authorize later access. Research specification remains frozen and untouched; dataset stays unused for outcomes.

## Cross-project isolation and save safety
FXNS coordinator outcome is recorded **separately** under `research/lines/fx-news-sentiment-v0.1/work/integration/2026-10-09/**`; this CSM receipt is **only** under `research/lines/currency-strength-momentum-v0.1/work/integration/2026-10-09/**`. This document does not merge FXNS/CSM or grant source/science PASS. Commit message includes **[skip ci]** as a cautious no-new-ECB-acquisition measure; if any workflow does execute, its result must be separately inspected and not represented as an authorized source rerun.

**Net-cost expected value is NOT EVALUABLE.** No human freeze I2, market-outcome access, live/paper trades or new prospective event issued.
