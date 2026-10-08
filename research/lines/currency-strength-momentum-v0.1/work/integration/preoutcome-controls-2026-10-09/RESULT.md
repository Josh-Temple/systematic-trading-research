# D — CSM I2 pre-outcome synthetic control verification (2026-10-09 JST)

**Decision: PARTIAL_WITH_GAPS / PASS_SCOPED for the standalone synthetic model only; I2 remains BLOCKED / CLOSED; `market_outcome_access=false`. No merge and no market-outcome authorization.**

## Exact current inputs (fresh GitHub read)
- Repository: `Josh-Temple/systematic-trading-research`.
- PR #37 (I2): `9162cae4f2e64ee3da07517f12a16092cc170161`, OPEN/DRAFT, branch `work/csm-integration-20261001`. `gate.json` Git blob `19442215345b35b0db3910c01acd910a5d57889b`: `state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`.
- PR #34 (original Packet D implementation): `3695f0a8ed085669ec3644826889f9fc953a6808`, `csm.py` Git blob `dbddf33895bc565e215583ad0056c9aba5ed3c1a`. Existing code checks signed E/I2 envelopes, role, RSA SHA-256 signature, expiry/revocation, specified I/E identities, and D/SPEC/source byte hashes. It does **not** establish a production trust root.
- PR #38 (independent E audit): `970ea9b77e062e7acbc67432993797a0cb4e0d01`, `PARTIAL_WITH_GAPS` / `BLOCKED`. Run `37166456105`, job `111330239715` independently reported `Ran 56 tests ... OK`, with `BOUND_D_HEAD=3695f0a8...` and `BOUND_I_HEAD=6bd9ddc5bc53c37aee3b0d82d1ac2c00c00fd73c`, **not** the present #37 head.
- PR #50: `3a0e6c64147244dfa37f47aa91c172ef1e6a9655`, #51: `8135e6f9d4cc7116ccdf9bfa0d73c1e535dcc506`, #52: `e30c87783fc6cd949f0a0d9ca21eb5b7b3cd8362`; these are prior CI wrappers, not newly executed by this D worker.
- PR #53 metadata-only: `dbe9574e2d03d8a34e099931078ba2de43c7606c`; independent C #78: `20fd4d52fee72fda76f40a1a20511abc1315732e`; independent I2 D #76: `927beace5b1e044712b7f7f574cd78bcd46a7f16`; E reconciliation #80: `cfc87ad57e1b6fd7d2f72d8aa7a86cc58204ac68`. The metadata-only historical receipt's PASS is not a source-vintage or I2 authorization PASS.
- New standalone model's branch base: PR #37 head `9162cae4f2e64ee3da07517f12a16092cc170161`. No Packet D production code, `gate.json`, source-lock or workflow modified.

## Executed synthetic-only experiment

Test code: `test_synthetic_controls.py`, local SHA-256 `bef93b827742930b37bb3d0089f8b3e149aa8458a975a40063bd5a4cd78902a3`; Git blob `c037c918eae219b6f47b139437b525e5538ca0bc` verified equal to the tested local file's Git object hash.

- Isolated Linux / Python 3.13.5, standard library, `python -m py_compile` **PASS**.
- `python test_synthetic_controls.py` ran **23 tests; 23 passed; 0 failures/errors/skips** (local execution only). Individual tests and reproducible invocation are in `TEST_LOG.txt`.
- The stand-alone test uses publicly known **fictional test RSA material** already in Packet D's synthetic fixture; HEAD values `a*40`, `b*40`, D hash `c*64`, approval PASS, operator and disposition are **fictional counterfactual fixtures**, not real GitHub authorizations.
- **RSA envelope tests (synthetic model only):** reject unknown/revoked/expired key, wrong role, unauthenticated signature, unsigned PASS, expired receipt, I/E head mismatch, old D hash, same principal, denied E recommendation, CLOSED gate, access false, missing final human approval/disposition and absent operator. The positive fixture proves only that the toy verifier accepts a coherent fictional envelope.
- **Path/network/process controls:** simulate read/write allowlist and denied network/child-process intents without performing real networking, unauthorized file access or child process execution; record all simulated denials.
- **Local storage:** simulated fsync, attempt hash-chain, new in-process instance readback, same-file tamper detection, full-chain rewrite detected with separately held *unprotected* anchor, and write-failure injection. This is **not an OS restart**, protected ledger, durable off-host storage, or resistance to a privileged adversary.
- No actual `csm.py` at D #34 was imported or rerun in this new branch. Do **not** attribute this 23-test result to production Packet D. GitHub Actions for the new PR: **NOT_RERUN**, deliberately skipped to avoid invoking unrelated live-source workflows. Historical 56/56 and initial negative evidence are preserved, not re-labeled as current-run evidence.

## Controls vs remaining evidence requirements

| Control | Demonstrated here | Remaining owner and required evidence |
| --- | --- | --- |
| RSA signed I/E roles and falsification | **PASS_SCOPED / independent toy verifier** | Platform/security key custodian **not named**: actual distinct key custody, fingerprints, principal separation, validity/revocation inventory, protected `/etc/csm-002/trusted-keys.json`, independent readback. Toy I and E roles use the **same published test RSA modulus**, so they cannot establish cryptographic key independence. |
| Current I/E/D freshness | **PASS_SCOPED / toy rejection plus static actual SHA comparison** | Integrator + independent E reviewer: signed statements bound to **actual current #37 SHA** and correct E/D blob/hash, independent external verification after any SHA change. Prior E attested older I. |
| Final gate and exposure | **PASS_SCOPED / toy rejection**, actual gate **CLOSED** | Separate authorized human: documented current-I approval, explicit final `market_outcome_access` decision, prior source/search incidental observation exposure disposition. No approval inferred. |
| Named outcome operator | **PASS_SCOPED / toy missing-name rejection** | Integrator must appoint and verify named X/operator with approved account and role, then include in signed receipts and log. **Not assigned**. |
| Filesystem, network, subprocess denial | **PASS_SCOPED / intent simulation only** | Execution platform/security: versioned enforced OS/ACL/mount/process/network policy and independently executed real denial probes; no such proof here. |
| Durable attempts/readback/tamper evidence | **PASS_SCOPED / temporary-file hash-chain and in-process reinit only** | Storage/security/operations: protected append-only ledger with externally protected anchors, denied-attempt coverage, immutable retention, **actual service restart** and durability verification. |
| Source metadata and publication | **Historical archive metadata PASS_SCOPED only** | Source owner + independent reviewer: H rows restricted to locked range/closed days, independent ZIP member byte-readback, historical vintage/publication/revision and external calendar authority; no live fetch in this wave. |

### Additional code-design review finding (not an executed production test)

The actual `csm.py` `_verify_signed_envelope` checks roles and principal identity *per key*, but the reviewed `validate_gate_receipt` does not visibly enforce that the auditor principal ID differs from the integrator principal ID, nor that their RSA key material is distinct. The standalone model adds the same-principal rejection; **that passing test must not be credited to the original implementation**. Independent production-code review / runtime adversarial regression belongs to a separately authorized Packet D scope. This D branch cannot modify `work/implementation/**`.

## Retained negative source, freshness and incident evidence

- #78: H placeholder acceptance lacks a strict bounded source-range/closed-day membership check; archival ZIP member bytes were **not** independently extracted; incidental current quote search snippets were disclosed (not used).
- #37's historical source rows and #53's later safe metadata receipt differ in scope/date of observation; the latter narrows archived metadata uncertainty only. Seven locked ECB EXR series / 2009-11-01–2026-09-30 / 4,331 expected open days are **provenance metadata**, not observations or outcomes. No new ECB query, OBS_VALUE, real price or return was read.
- #76 and #80 previously concluded **PARTIAL_WITH_GAPS / HOLD_NO_MERGE**. This branch does not supersede their production-control and human blockers.

## E handoff

**PARTIAL_WITH_GAPS; no gate promotion; no merge.** Only the exact 23-test standalone synthetic model is PASS_SCOPED. Do not promote a fictional signed PASS to a real signer, authentic GitHub I/E freshness, real OS denied operation, protected audit ledger or permission to calculate outcomes. Separate human and platform decisions are required; this D worker creates none. I2 remains **BLOCKED**, gate **CLOSED**, `market_outcome_access=false`, hypothesis **UNTESTED**.

Evidence: [PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37), [#34](https://github.com/Josh-Temple/systematic-trading-research/pull/34), [#38](https://github.com/Josh-Temple/systematic-trading-research/pull/38), [#53](https://github.com/Josh-Temple/systematic-trading-research/pull/53), [#76](https://github.com/Josh-Temple/systematic-trading-research/pull/76), [#78](https://github.com/Josh-Temple/systematic-trading-research/pull/78), [#80](https://github.com/Josh-Temple/systematic-trading-research/pull/80), [historical E CI](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37166456105).

No source workflow trigger, OS policy changes, broker, market outcome, actual signal, order, or live/paper trade was authorized or executed.
