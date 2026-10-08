---
id: CSM-I2-INDEPENDENT-BLOCKING-20261009-D
type: IndependentPreOutcomeGateAudit
date: 2026-10-09
research_line_id: RL-CSM-001
status: PARTIAL_WITH_GAPS
gate_status: BLOCKED_CLOSED
market_outcome_access: false
scientific_status: NOT_APPLICABLE
hypothesis_status: UNTESTED
audited_i_pr: 37
audited_i_head: 9162cae4f2e64ee3da07517f12a16092cc170161
disposition: HOLD_FOR_E
---

# CSM I2 pre-outcome: independent blocker and identity receipt (Worker D)

## Decision and boundaries

**Independent audit judgment: PARTIAL_WITH_GAPS; authorization judgment: I2 BLOCKED / CLOSED.** Do not authorize X, market-history access, OBS_VALUE inspection, outcomes, ranking, return, strategy P/L, Sharpe, broker order, live/paper trading, or a scientific efficacy claim. HYP-CSM-002 is **UNTESTED**; DATA-CSM-002 remains PLANNED / NOT_CAPTURED_FOR_EXPERIMENT; EXP-CSM-002 remains PLANNED / NOT_RUN. Market outcome access is **false**. No such access was performed in this Worker D session.

The frozen SPEC's retrospective **latest-vintage association** question is distinct from historical real-time tradability. Source metadata PASS and synthetic/code PASS are **not** I2 PASS and not evidence of positive expected returns.

This was a **fresh GitHub blob/diff/Actions-log review**, not a new isolated local test run. New synthetic-suite execution by this worker: **NOT_RERUN**. The existing independent workflow was inspected directly; its successful test result is attributed to that workflow, not this worker.

## Exact source-of-truth refs (fresh-read and rechecked before branch creation)

| Component | Current actual PR head | Evidence scope |
| --- | --- | --- |
| I integration PR #37 (draft) | `9162cae4f2e64ee3da07517f12a16092cc170161` | Audited current I2/GATE/gate.json/CURRENT, acceptance, decisions |
| D implementation PR #34 (draft) | `3695f0a8ed085669ec3644826889f9fc953a6808` | Audited code/README-style runbook and exact code/test/config/log Git blobs |
| E independent audit PR #38 (draft) | `970ea9b77e062e7acbc67432993797a0cb4e0d01` | E RESULT, matrix, test log, preserved negative history |
| D verification wrapper PR #50 (draft) | `3a0e6c64147244dfa37f47aa91c172ef1e6a9655` | Workflow run `37166148389` success (historical CI) |
| E re-audit wrapper PR #51 (draft) | `8135e6f9d4cc7116ccdf9bfa0d73c1e535dcc506` | Run `37166456105`, job `111330239715`, exact D suite |
| E identity wrapper PR #52 (draft) | `e30c87783fc6cd949f0a0d9ca21eb5b7b3cd8362` | E canonical artifact identities; no standalone rerun here |
| CSM source-readiness PR #53 (draft) | `dbe9574e2d03d8a34e099931078ba2de43c7606c` | Metadata-only SAFE_RECEIPT and workflows; this is not Packet X |
| Earlier Packet C source lock | `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` | Source-lock / probe metadata / expected calendar used by audited D |

The frozen `SPEC-CSM-002-v01` has Git blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`, and is FROZEN. Actual fetched Git blobs: D `csm.py=dbddf33895bc565e215583ad0056c9aba5ed3c1a`; `test_csm.py=27920cfa92546aba07781915032c7bb5ae999549`; `config.json=a1c1e140f8c0844fc554ae6fcd975bcb5e610770`; `TEST_LOG.txt=4d8e6615a64ea9d5da8fc71fbbda4a4ee67db5ba`. E `RESULT.md=59ece59a96fe3f7bb9e36da5e93bc56a4ddcd7cd`, `AUDIT_MATRIX.csv=4ba6cbbddf731e5e226b56af1d4d84847c586cf5`, `TEST_LOG.txt=11e0732a261f01ee4d046801d585fa1b30bd3482`. These match the identity tables in I/E for the audited **D** head.

**Old versus current I head is material**: the E run explicitly bound I head `6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`, **not** current PR #37 head `9162cae4...`. Comparison shows **6 subsequent commits** touching I docs/decisions/gate.json/CURRENT only; D head has not changed. Current I `gate.json` blob is `19442215345b35b0db3910c01acd910a5d57889b`; current `GATE.md` blob is `4d1784b2622d54b3c91ce740c9379f98bbfc6667`. The old E run's older I gate hash is **not** a current-head signature/approval. Current I state remains independently inspected **CLOSED/false**; no evidence of a newer signed PASS gate was found in the reviewed inputs. E's code-level finding about exact D bytes may be preserved, but its older I-attestation must not be represented as a current I2 authorization.

The current I `gate.json` retains historical E/no-result subobjects with older audit/head identities as well as a newer `input_heads.E`. Readers must distinguish provenance history from the canonical current-head state; blindly reading nested historical `e_audit` as latest would be an identity error.

## What existing independent execution establishes (and what it does not)

- `https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37166456105`: directly inspected job **111330239715** steps **and job log**. It materialized exact D/C/I/SPEC inputs; **Ran 56 tests**, with successful unit-test step, and the independent E oracle printed **seven PASS checks** with no `GAP_REPRODUCED`. It bound D `3695f0a8...` and old I `6bd9ddc5...`. This is a historical independent synthetic/code validation, **not a new D rerun and not an I2 PASS**.
- `https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37166148389`: inspected successful D wrapper job steps. Its PASS does not supplant the separate E audit.
- The inspected D code `validate_gate_receipt` rejects non-PASS I2, non-ALLOW_I2 E, wrong D code/test/config/environment bytes, wrong frozen SPEC, source-lock raw bytes, calendar/probe identity, invalid key roles/signatures/expiry, and absent required operator/ledger fields. The production CLI invokes it without test-key injection; the separate synthetic test override is not a production authorization.
- E's previous two D-specific failures—circular mutable I/E code pins and compound fsync/rollback leaving a SUCCESS receipt—were retested and resolved **for D head 3695f0a8... only**. Preserve E's historical negative evidence. These are no longer current D-code blockers unless D bytes change.
- This worker confirmed the **Git blob identities** directly and checked the E CI job log, but did **not independently rerun 56 tests in a fresh runner** or provision production keys. Any claim of end-to-end production security or source efficacy would exceed this evidence.

## Source-readiness transition since I's earlier decision

PR #53 SAFE_RECEIPT (Git blob `0e27706cdb5f775d7bd302c56605a6800fa4da57`) records `overall_status=PASS`, `market_outcome_access=false`, seven fixed ECB EXR series over **2009-11-01 to 2026-09-30**, **4,331** expected open days, zero missing expected observation days/duplicates, and reviewed H holiday placeholders. It binds source lock SHA-256 `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71`, expected calendar `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4`, runner `37167525175`, and safe-receipt SHA-256 `34287530a0ce3072cf3aa5781063ce6732c79a366fabfaf50c6cf1e4358c759f`. That runner's job steps and metadata-only log were inspected; a later run `37167624319` was also successful.

The source-reported `CALENDAR_AND_VINTAGE_BOUNDARY.md` now cites official ECB/TARGET date rules and distinguishes historical point-in-time vintages (**UNVERIFIED**) from the frozen retrospective latest-vintage claim (**interpretation limitation**, not proof of contemporaneous availability). **This worker did not perform Worker C's fully independent source audit, did not reacquire ECB data, and did not inspect/print OBS_VALUE.** This is a **recorded metadata-only PASS awaiting independent reconciliation**, not an automatic upgrade to I2 and not proof of market-outcome usability. The old I gate table's full-history/calendar BLOCKED rows should be reconciled with independent C findings by E, not silently left as though PR #53 never occurred or silently changed to overall PASS.

## Residual I2 blockers and executable next steps

| Condition | Today's assessment and evidence | Responsible authority | Next permitted operation and human boundary |
| --- | --- | --- | --- |
| Trusted signing root / signer independence | **BLOCKED.** D checks role-restricted signed envelopes; code expects a fixed root-owned `/etc/csm-002/trusted-keys.json`. Test RSA material is synthetic; no provisioned trusted Integrator/auditor production keys, protected fingerprint inventory, validity/revocation record, or actual signed PASS envelopes established. Independent auditor and Integrator must not self-endorse the same evidence. | Platform/security key custodian; independent auditor; Integrator | Draft key ownership, fingerprints/roles/revocation and protection protocol; independently test a **synthetic denied** signature/role/revocation case. Human approval required for real trust-root installation and any later signed PASS. |
| I/E artifact freshness and audited-code binding | **PARTIAL_WITH_GAPS.** D code validates hashes and signed E file map. E CI binds current D but older I; production CLI has optional external `expected_current_i2_gate` / `expected_e_audit` comparison arguments that are **not populated at this CLI call site**. The signed-identity producer and admission procedure must independently establish latest trusted I/E bytes; a structurally valid signed SHA is not proof of current GitHub HEAD. | Integrator gate issuer + independent E auditor, separate roles | Publish a **pre-signing freshness checklist**, verify actual GitHub PR head/blob/digest against proposed signed envelope in isolated control-plane evidence, reject stale/revoked heads; do not patch D within this worker's allowlist. Human final disposition remains necessary. |
| OS/file/process isolation and denied paths | **BLOCKED.** D Python audit hook is process-local, not OS isolation. No enforced read/write allowlist, unprivileged runner identity/mount/ACL, subprocess/network denial, or independent negative denial probes in reviewed evidence. | Execution platform/security owner, to be named | Specify versioned sandbox policy; test forbidden paths/process/network using **synthetic files only**; independent runner attestation. Human/security sign-off before outcome access. |
| Durable output and append-only access/attempt evidence | **BLOCKED.** D synthetic atomic promotion test passes, but no provisioned protected durable output destination, restart/readback, or append-only/tamper-evident audit ledger recording **denied attempts** is established. | Storage/platform and research operations owners | Provide isolated synthetic persistence/restart/readback and append/tamper denial receipts, retention/access policy, and explicit responsible identities. Requires operational authorization before any real capture. |
| Source identity, calendar and vintage | **PARTIAL_WITH_GAPS pending C.** PR #53 metadata-only PASS and ECB/TARGET rule memo advance earlier source gaps; historical original publication/vintage remains UNVERIFIED and cannot be converted into trade-time availability. Current I still CLOSED. | Independent Worker C; source owner; Integrator E | Compare CI `37167525175`, SAFE_RECEIPT/artifact hash and source-lock against C's independent receipt without reading OBS_VALUE; reconcile only fixed retrospective claim and preserve historical limitations. Human I2 cannot follow from metadata alone. |
| Human freeze vs final outcome authorization | **BLOCKED for final approval.** `HUMAN_CONTRACT.md` records acceptance `HDEC-CSM-002-20261001` of the SPEC freeze; that is **not** an I2 outcome-access authorization. No named approved X/operator/account and no final I2 human decision. | User/authorized research sponsor + Integrator + named X | Obtain distinct explicit human disposition of all I2 evidence and designate operator/account. Do not infer acceptance from frozen SPEC or a reviewer comment. |
| Prior accidental exposure | **BLOCKED pending human disposition.** I `gate.json` records prior C search-result and Integrator current ECB page exposure disclosures. This worker did not read/reproduce exposure values. | Authorized human reviewer | Record separate human incident/evidence-validity dispositions without echoing observations; keep any holdout contamination policy intact. |
| Older B/original brief lineage | **GAP, not permission to alter SPEC.** B base/path conformance and pre-proposal brief traceability remain noted. | Original B owner / provenance reviewer | Bounded provenance resolution on separate scope; preserve frozen contract and existing negative history. |

### Non-market controls that can be advanced without unlocking I2

1. **Worker C/E**: independently verify the already produced metadata-only ECB receipt and archive hash identity, then reconcile the precise source rows in the later I gate; do **not** invoke new market-data requests here.
2. **Platform/security/research operations**: prepare a separate **synthetic-only** trust-key custody and signer-independence demonstration, OS path/process denial probes, durable readback, and append-only attempted-access test log; provide immutable evidence and exact code/run identities. This may resolve design/operational *preparation* gaps, but not authorize capture.
3. **Integrator/human**: reconcile I head freshness, signed evidence producer chain and operator/exposure dispositions; ask for an explicit separate decision only after independent evidence is assembled. No self-issued PASS.

## E handoff, recommendation and stop rule

**Recommendation: HOLD; adopt this blocker inventory into E, do not merge PR #37/#53 or open I2 based on this D report.** C's independent outcome-blind source review may narrow source-specific blockers. Preserving the existing D-code PASS on its exact audited SHA avoids needless code churn. Where I moved since E's old I head, require a fresh **current-I** gate identity comparison; never reuse old hashes as current approval.

**Stop immediately** on missing/unauthenticated production signer, missing independent E PASS attestation, no named X, insufficient OS isolation/durable ledger, unresolved exposure disposition, altered D bytes without re-audit, disputed source identity, requests to read OBS_VALUE or market outcome, or any attempt to equate metadata-only PASS with a scientific result.

Changed files for this worker: this Markdown receipt **only** under `work/integration/preoutcome-audit-2026-10-09/**`. No implementation, frozen SPEC, source-lock, market value, shared CURRENT, order execution, source download, or test workflow was modified. New tests: **NOT_RERUN**. The branch is based on exact PR #37 head above and targets `work/csm-integration-20261001`; intended PR status **DRAFT**.

Evidence: [PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37), [#34](https://github.com/Josh-Temple/systematic-trading-research/pull/34), [#38](https://github.com/Josh-Temple/systematic-trading-research/pull/38), [#50](https://github.com/Josh-Temple/systematic-trading-research/pull/50), [#51](https://github.com/Josh-Temple/systematic-trading-research/pull/51), [#52](https://github.com/Josh-Temple/systematic-trading-research/pull/52), [#53](https://github.com/Josh-Temple/systematic-trading-research/pull/53), [E job log](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37166456105), [ECB metadata job](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37167525175).
