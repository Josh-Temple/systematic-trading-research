---
audit_id: AUDIT-CSM-E-20261002-REAUDIT-01
status: PARTIAL_WITH_GAPS
scientific_status: NOT_APPLICABLE
recommendation: BLOCKED
i2_gate_status: BLOCKED_CLOSED
market_outcome_access: false
audit_date: 2026-10-02
---

# Packet E independent re-audit of current Packet D

## Decision

This audit covers Packet D commit 6dccd49ee21e4ac29f55162f93ef3e65aa7a5779 and the exact nine D artifacts listed below. All supplied opening refs were freshly fetched from GitHub; they matched the user's start refs. The D test suite was independently rerun, and an E-authored synthetic oracle was run against those exact D bytes and the current permitted metadata.

Overall status is PARTIAL_WITH_GAPS and recommendation is BLOCKED. I2 remains BLOCKED / CLOSED and market_outcome_access remains false. This report grants no gate PASS, access permission, execution authorization, or instruction to X. Scientific status is NOT_APPLICABLE.

Two code-level changes reported by D are independently reproduced: formation-score identities are target-value and target-availability invariant in the pre-outcome ledger; and synthetic signed-receipt/raw-source-byte controls reject the tested invalid cases. The current D validator nevertheless pins an obsolete I2 identity and the historical E identity. D's runbook and test log also state those obsolete refs. The new current I2 identity and this audit identity cannot be accepted by that D code. In addition, a compound final-directory-fsync and rollback-deletion fault leaves a success receipt in the destination after promotion reports failure. These are open D follow-up items.

The code-level outcome is distinct from operational readiness. OS-level isolation, filesystem allowlisting, durable protected output, a persistent append-only access/attempt ledger, a named operator, and production trust-key distribution have no evidence in the reviewed D artifacts. Calendar authority, full-period source coverage, missing/status distribution, historical publication timing and revision/vintage remain unresolved. The original pre-proposal human brief is absent from the reviewed receipts.

## Independence, access scope, and limits

I re-read the specified GitHub refs and file contents directly from the repository. D's RESULT, tests and logs were treated as reporter claims until reproduced. The replay used a separate temporary work directory containing the exact D snapshot; the oracle was authored for this re-audit and used only synthetic rows and the explicitly permitted metadata files.

Read: main repository guidance; the exact architecture proposal ref and Packet E instructions; current A, B, C, D and I refs; A/B literature and prior-art deliverables; C source-lock, probe-metadata and expected-calendar metadata only; all nine D artifacts; current I gate, frozen SPEC and reconciliation/freeze lineage documents; and the historical E result/matrix for historical comparison only.

C access was restricted to source-lock.json, probe-metadata.json and expected-calendar.json. C RESULT, raw probe CSV and OBS_VALUE were not read. No market prices/history, rankings, forward returns, strategy outcomes, P/L, Sharpe or performance plots were accessed, generated or calculated. No H3, DATA-HR-003, Autonomous Pilot, broker, live/paper inputs or X instructions were accessed or issued. No C observation value, calendar entry, count or distribution is reproduced here.

This is a code/contract and synthetic audit. It does not establish external calendar authority, causal execution timing, historical data readiness, market performance or operational security. The audit binds to the exact refs and hashes below; any D, C, frozen SPEC or current I gate change invalidates the corresponding input-bound conclusions.

## Nine-item audit matrix summary

| Item | Status | Finding |
|---|---|---|
| 1. Human contract, freeze and lineage | GAP | The accepted pre-freeze SPEC and frozen SPEC have identical scientific body bytes, and the freeze receipt is present. The original pre-proposal brief is absent; current main routes the line to a different branch than the user-designated architecture proposal. |
| 2. Pair mathematics and synthetic oracle | PASS | Independent exact-ratio/Fraction and Decimal checks agree with D on directed-pair identity, numeraire change, quote/log orientation, tie and EUR/USD cases. |
| 3. Calendar, missingness, endpoint scope and vintage | GAP | D's declared calendar metadata and internal consistency can be checked; external authority, full-history coverage and observed missing/status, timing and revision/vintage evidence remain unresolved. |
| 4. Outcome-blind formation ledger and temporal leakage | PASS | Synthetic changes to target values and target availability leave pre-outcome ledger bytes identical; outcomes reject an absent/unverified persisted ledger. Static review found no target-driven selection, bfill, compressed-date shift or after-entry ranking path. |
| 5. Bootstrap and decision boundaries | PASS | Independent synthetic circular-bootstrap and boundary checks match the frozen method's deterministic settings. The audit does not make a market inference. |
| 6. Gate, receipt identity, raw input bytes and persistence failures | GAP | Test-key signature controls and raw-byte binding reproduce; exact current I/E identities are stale in D. A compound rollback fault leaves a success receipt. Production keys and persistent controls are absent. |
| 7. Isolation, output boundary and access accountability | GAP | Code has process-local restrictions and status-only CLI output, but no OS isolation, filesystem allowlist, durable ledger, holdout separation or named operator evidence. |
| 8. A/B/C/D evidence and contract preservation | GAP | A/B are indirect evidence; B artifacts remain outside the line path and on a diverged base; C is partial; D's contract-preserving code is testable but the listed source and operations gaps remain. |
| 9. Omission review and recommendation | PASS | Findings are separated into code-level resolution, code-level gaps and external requirements. Recommendation is BLOCKED; no access gate or scientific result is issued. |

Detailed evidence and next checks are in AUDIT_MATRIX.csv.

## Fresh refs and ref comparison

The supplied opening refs all matched the GitHub state at the audit start. No silent substitution was needed.

| Input | Exact ref at fresh read | State |
|---|---|---|
| main | a765b33fc0915fdfdcf21287a4418aca4f5b8b7c | matched |
| Architecture PR #31 | e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | matched; open draft; used as proposal_ref |
| A / PR #33 | 5e45377b890877ff18275a7fbd4371ffe80c92ba | matched |
| B / PR #32 | c756805692658c99394ca71f88203ba224e78c3c | matched |
| C / PR #35 | 9870c710c3cba7bb9226c9eee8ec36687b96fd9d | matched |
| D / PR #34 | 6dccd49ee21e4ac29f55162f93ef3e65aa7a5779 | matched |
| historical E / PR #38 | d1335b29eeb01cdd4b71cd5ded62033b8468e539 | matched before this re-audit write |
| I / PR #37 | c2fdbc1f2a9fcccc32717b130a36433819aaa2fa | matched |

main_sha and proposal_ref are distinct. The fresh main README, research principles and schema guide matched the proposal branch copies. The main index routes the currency-strength line to research/currency-strength-momentum-v0.1; that branch and its provisional SPEC-CSM-001 were not read or used as the contract. The requested e0f42a proposal remains the contract source for this audit.

## I2 gate identity

The current I PR #37 head is c2fdbc1f2a9fcccc32717b130a36433819aaa2fa. Both gate files were fetched at that exact head and their Git blob and SHA-256 identities were recomputed from bytes.

| Current I file | Git blob SHA-1 | SHA-256 |
|---|---|---|
| work/integration/gate.json | bd6db786a3a1aafe7ce0864def41d5e13123447c | 036498e34b85ecbe9fef4c9a6c452b906ee6e680ffe4a08924cb3e3b11fdcbb3 |
| work/integration/GATE.md | 28ef6e0c006c08fb721ca6100323f283d5cb84c3 | 4c8bd37622e412eac5ae806841f40bb61e9ce8b4de2d2ede834ff0521988d387 |

The exact current gate reports BLOCKED / CLOSED with market_outcome_access=false. This audit preserves that state. Current I reconciliation also records HYP UNTESTED, EXP NOT_RUN and DATA NOT_CAPTURED_FOR_EXPERIMENT.

## D implementation findings and reporter-claim comparison

### Identity-bound D snapshot

All nine paths below were fetched from D head 6dccd49ee21e4ac29f55162f93ef3e65aa7a5779. For every path, the Git blob SHA-1 and raw-byte SHA-256 matched the user-supplied identity. D reported 53/53 tests; that claim was treated as unverified until the independent rerun recorded in TEST_LOG.txt.

| D artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| work/implementation/csm.py | 95cf059a5e0d5b6742dfa885fce7b37c58f2362c | 4db33063f0388b8b7ec0613fff8228a4aa3cb00b94855a557c5abcd3b86f4104 |
| work/implementation/test_csm.py | e287ab6923d073058cfa0e5e7be46b9ea5bc537a | 3499c6cf4bc52f5052c7ed76ef92da41c272cbb6a31980a51801372775f1f66f |
| work/implementation/config.json | a1c1e140f8c0844fc554ae6fcd975bcb5e610770 | 9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1 |
| work/implementation/RUNBOOK.md | 3142c0291aa979bb80c28d71b4e47fc7408591ab | 7fa355a6b071567ff6d4ea4290033f5635fc44b64159af2438acae69ecc14948 |
| work/implementation/ENVIRONMENT.md | bf6d5b4c0381e967226ee0996736d858b524b8eb | 8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f |
| work/implementation/RESULT.md | 98e36e22a797806d1ee66438825d7a75f42ff21a | 91fba806a72a9d4e103b535d4acc10b525476f7901700ff1279845bfff2a6923 |
| work/implementation/TEST_MATRIX.md | 03633916f0190925a01d6b26e5146956e657c31f | 7cfbd342057ce8a9517fbbf44e464fb05beb60e6de82e47f4e1d8643e7da4bce |
| work/implementation/TEST_LOG.txt | c70e610064f92ba15527fb7f99b8796607a9a91f | 84a6a88673b0502b53bf3b2eb0ca100d101d8bd57cfab3da08695285fc399f44 |
| work/implementation/fixtures/toy_cases.json | 4e925eabb4d88772806f0e109c15680f17d73a31 | 08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c |

### Independently reproduced changes and remaining code gaps

- Formation score identity: D's event ledger includes a score identity for each currency. The E oracle generated synthetic formation data, changed target values, then removed target availability; serialized ledger bytes stayed identical in both cases. An outcome calculation with an absent ledger and wrong expected digest was rejected. This independently resolves the old E score-identity finding at the code/test level.
- Signature verification: a valid synthetic RSA envelope signed by a configured test key was accepted only for the configured role and principal. Wrong role, wrong principal, unknown key, revoked key and expired envelope cases failed closed. These test keys are synthetic fixtures; this does not establish production key provisioning.
- Raw source-lock bytes: D reads the lock into a byte buffer, hashes that exact buffer and parses the same buffer. A semantically equivalent JSON document with different raw bytes was rejected in the oracle. The permitted C metadata files' exact byte identities also matched.
- Current identity mismatch: D's CURRENT_I2_GATE_EXPECTED constant and RUNBOOK/TEST_LOG pin PR #37 head 677341e8185bf38b5cc6d4490260ddefb72eb561, gate.json blob ba1670b0c13ec58e806838949a80574a5cbab6c4 and SHA-256 54b7984b9853ee6a7b848d6fb473d6aeb7bc1f52c2d94d6c74ed13f43cc28dd6. Current I is c2fdbc1f2a9fcccc32717b130a36433819aaa2fa with gate.json blob bd6db786a3a1aafe7ce0864def41d5e13123447c and SHA-256 036498e34b85ecbe9fef4c9a6c452b906ee6e680ffe4a08924cb3e3b11fdcbb3. D's CURRENT_E_AUDIT_EXPECTED pins historical audit AUDIT-CSM-E-20261002 at PR #38 head d1335b29eeb01cdd4b71cd5ded62033b8468e539, result blob f29a5d38b16b54734a47c719c09922a461ee3fe4 / SHA-256 c0df6ce468558e22eff57056ecf88ac9b5817a67fdcedef3e9aa028878177c35 and matrix blob 3ada00d887bc76f88c777d2a40ea410077e3e594 / SHA-256 a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7. The E oracle signed synthetic envelopes identifying the current I files and the new E audit ID. It independently confirmed rejection of the current I identity, current E identity, missing gate and unfrozen gate. The new audit ID is AUDIT-CSM-E-20261002-REAUDIT-01, so the pinned E identity is also stale.
- D follow-up is required. D's code pins, RUNBOOK.md and TEST_LOG.txt need an identity-refresh design and accurate current refs. The design must avoid a circular requirement in which the audit's final hashes depend on a D head that itself must embed those same final audit hashes. After a D change, create a fresh D identity and repeat the E checks against it. I2 stays closed throughout.
- Persistence faults: the single injected write, flush, fsync, rename and promotion failures tested by D's suite and the E oracle did not promote false success in the tested isolated cases. E also tested a compound fault: the destination parent fsync fails after directory promotion, then rollback deletion fails. D suppresses the rollback deletion error; promotion reports failure while the final run directory and run-receipt.json remain. This is a reproduced GAP because a success receipt remains after failed promotion. D must either make rollback cleanup reliable or ensure the final receipt cannot be interpreted as success after any failed promotion; add a compound-fault regression test.
- Trust store: D expects /etc/csm-002/trusted-keys.json and rejects missing/untrusted test identities as configured. The production trust store and production key fingerprints/roles/principals/validity/revocation evidence were not present. The local synthetic key cannot close that gap.
- Current gate: current I gate JSON/Mardown identity and status were freshly fetched. D's stale constants prevent an exact current positive binding. Do not use the D self-report or prior E's 42/42 and 5/5 results as substitutes for this re-audit.

### Prior E findings, retained historically

Old E remains audit AUDIT-CSM-E-20261002 at old E commit d1335b29eeb01cdd4b71cd5ded62033b8468e539. Its result/matrix identities are f29a5d38b16b54734a47c719c09922a461ee3fe4 / c0df6ce468558e22eff57056ecf88ac9b5817a67fdcedef3e9aa028878177c35 and 3ada00d887bc76f88c777d2a40ea410077e3e594 / a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7. That result remains PARTIAL_WITH_GAPS / BLOCKED for its old D input 4f739d9cc2b21c138771afec4a728bf2b57060ba. It was not edited or reused as the current finding.

The former missing-score-identity finding is independently resolved in current D's code and synthetic behavior. Signed receipt and source-lock raw-byte controls are independently present and pass the synthetic cases, with current identity pins and production key distribution still open. The persistence implementation closes the tested single-failure cases but the compound rollback case above remains open. Calendar/source authority, full-period readiness, isolation, operator/access-ledger evidence, exposure disposition, B artifact placement/base and original-brief traceability remain open.

## External and lineage requirements

D's RUNBOOK assigns roles, but the reviewed artifacts contain no named owners or proof for the following conditions:

| Requirement | Proposed owner recorded in D | Evidence present |
|---|---|---|
| Filesystem allowlist and OS-level file/process isolation | Execution-platform/security owner, to be named by Integrator | No sandbox policy or denial probes |
| Durable protected output destination | Storage/platform owner, to be named by Integrator | No provisioned destination or restart/readback proof |
| Persistent append-only access/attempt ledger, including denied attempts | Research operations/security owner, to be named by Integrator | No durable location, retention or tamper-evidence proof |
| Named outcome-access operator | Integrator | No named person and stable account ID |
| Production trust-key distribution | Platform/security staff | No provisioned trust store or independently checked fingerprints |

The current process-local audit hook is not OS isolation and does not enforce a filesystem allowlist. A local attempt directory is not an append-only durable ledger. No holdout separation is evidenced.

Calendar metadata internal consistency is not an external-authority check. Keep external calendar authority, complete source coverage, missing/status distribution, publication timing and revision/vintage unresolved. No values from C were reproduced. A later review needs a separately approved metadata-only verification plan before any source-readiness claim can be raised.

A/B prior-art deliverables were read at their exact PR heads and are indirect evidence; their constructs do not directly estimate the frozen question. C remains PARTIAL and only its three permitted metadata artifacts were read. B's five artifacts remain in repository-root work/github-prior-art and PR #32 diverges from the architecture base (ahead 5, behind 6; merge base 36240da15fc83120d12d081c227f3e0dd8badaaa). The original human brief remains absent. These lineage issues require their respective owners and cannot be repaired by E within its allowlist.

## Input identity inventory

Git blob SHA-1 is computed over Git's blob framing plus bytes; SHA-256 is over raw file bytes. Exact artifact hashes bind the contents read. Ref heads and repository URLs are recorded in the preceding tables. A/B and C identities below are supporting artifacts used for item 8, not market observations.

### Authority and contract inputs

| Input at ref | Git blob SHA-1 | SHA-256 |
|---|---|---|
| main README.md at a765b33fc0915fdfdcf21287a4418aca4f5b8b7c | 3428fa1b67db3bc0f3d3d61cddb951773d75351b | e1998c1c98837fbaa40db5053503bac44629441f0c38eb73bbd82193c39aa784 |
| main docs/RESEARCH_PRINCIPLES.md at a765b33fc0915fdfdcf21287a4418aca4f5b8b7c | 3338e5948de34da763fd14113afba43945fd6683 | de9834b15c5bcdb053ad36516c616c7148b83f943c5010f469b4ce6939727825 |
| main schema/v0.1/README.md at a765b33fc0915fdfdcf21287a4418aca4f5b8b7c | 01f67f3e301b5e7091ceaf9f06d7cd75b703f136 | d7a6251531c9b53c4bb9d2c24b4f6fcfb2efd71f942f3edfeb57d4fb36b9bf40 |
| line README at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 5798a1636397dfa4677e958040ba9423aac2e062 | 7c55476deef9385f664b28000b767f2c6594decedc22521cc6e283f305e2a27b |
| ARCHITECTURE_REVIEW at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 0efdcaebe18eba9636a2f503ae5d58988df2a933 | 91409b9abd4320ef0e2caefc7a8b1b7a8d4e7f8c9b12995095feabaab8f14cf9 |
| accepted pre-freeze SPEC at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | a073e77dec14337ee20609ed6136e50a8c1e76e2 | e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90 |
| DEC-CSM-002 at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 10c96c99256c528fd717d7f9ca0af9e91efe0123 | 04f8df43694d6c459c91e57719249fe8273258853d83c242c7dd5d256b58d381 |
| Packet E instructions at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 7df322670d35444779e85c0f8520a696f523ae0c | 584d8f1a8dec349d49bd2b33b28dfda466e83afb0e0ea4c37e36507769df7ce6 |
| Packet D instructions at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 8838213541357a107124e27b557ef940a8b092e5 | 38d6e782d9430a3b977e8174febd6dd3a0623f125b30ec3984bb92eb763196c1 |
| Packet I instructions at e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff | 5b97f38755526e31132bd56429606fc16f33125b | d99ca0f695deff99b3150655ab3f65aa847b3b098ba0cb9806dc05cdc0efa896 |
| frozen SPEC at I head c2fdbc1f2a9fcccc32717b130a36433819aaa2fa | 7fe114e2fcfa33b0565b51c717455abd8837d5d9 | a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2 |

### Current I lineage inputs

| Input at I head c2fdbc1f2a9fcccc32717b130a36433819aaa2fa | Git blob SHA-1 | SHA-256 |
|---|---|---|
| work/integration/HYP-CSM-002.md | 944580c5cecae5dd556b809540951cd194a8e1a3 | ebe14de472e848aba972d3754f3959eae01ef524ef254538891d99d549f4eca9 |
| work/integration/EXP-CSM-002.md | 51ea9d2f0e8ec7202c31b3ce72f361f950ec1317 | 67e777b38a81a17851ba15855cdb323f404f15d6e72fd3b80dabecc221bafe3e |
| work/integration/DATA-CSM-002.md | 04c5cf30fc0e3551ce5c9be0e58f651709546d74 | 167c6472dcd3329c9843c2d7fb44a709d4ad004acd66a578998841b6b7791ae4 |
| work/integration/HCON-CSM-002.md | eb38572e9c8c2a25e980ef488f5984c8b81a3f17 | e47804b54bc7e45edfca65f28ea49514905b04e21f7c7a2a5b0f69328b067cb6 |
| work/integration/RECONCILIATION.md | 518fb7762f64aa2b9742e4913011d9ce53ca6a62 | ecad2f14bc7f00345fa97bedee060db58423a76c7fec6b19516e040462f554a7 |
| work/integration/DEC-CSM-002-POST-PREPARATION.md | b0b3849b87a75c1de77b0b2e38a9e1afcb167720 | bb32fa3dd1d5389c14cc923a84ecdb67452fc855ea00a517e7ebbabf2f731aed |
| work/integration/DEC-CSM-002-POST-D.md | 384fc8b6225479165da3bbf774107f7b9a874812 | b2e8fde050c195af679c00c39a4f8e26142a046bf7a058567146b075b97851d8 |
| work/integration/DEC-CSM-002-POST-E.md | dfb0d374c1fe4089c3f52a7878f36554e647d978 | 61d494361e842716402bd33a8546415f5ad8daa65f93f9526ed0bcb627171d4e |
| work/integration/FREEZE.md | 04860b4f92af2295331637eec8ade5a3ac66af32 | c90fdd621f1691ff7343d15a5a989b115d1f9d750da58ab706d288f89710fdc7 |
| work/integration/gate.json | bd6db786a3a1aafe7ce0864def41d5e13123447c | 036498e34b85ecbe9fef4c9a6c452b906ee6e680ffe4a08924cb3e3b11fdcbb3 |
| work/integration/GATE.md | 28ef6e0c006c08fb721ca6100323f283d5cb84c3 | 4c8bd37622e412eac5ae806841f40bb61e9ce8b4de2d2ede834ff0521988d387 |

### A and B supporting evidence

| Input at exact PR head | Git blob SHA-1 | SHA-256 |
|---|---|---|
| A PR #33 literature/RESULT.md at 5e45377b890877ff18275a7fbd4371ffe80c92ba | 51bb89bc83dab3db6aad7b3df773b7ca586e9b63 | ebc8f57347f48a7df5f89fb2671ce94a85bfbcd9b6314182ffd4fff4150f5bad |
| A PR #33 literature/EVIDENCE_TABLE.csv at 5e45377b890877ff18275a7fbd4371ffe80c92ba | d52d1659c87fdab23f8ee58014b277c1343ae92a | 09868fe1e657c069c9ca6f6b98584c3b75921e9651daf00ab08568c51c582cc8 |
| A PR #33 literature/SEARCH_LOG.md at 5e45377b890877ff18275a7fbd4371ffe80c92ba | 0e36124fd5f395a3434b38a62033c6a264c834f4 | 55e7b8caebbad949d4fa19b3aca12ba8bb0d4b9a2e4423f86da26d924b62e993 |
| B PR #32 work/github-prior-art/RESULT.md at c756805692658c99394ca71f88203ba224e78c3c | b835541c78f826237ee30d7e87aff42636ccb5d1 | f01fb52bdb96866391147a3b0cad7a7de6608c5cfd8932551bc2cf1ffb863238 |
| B PR #32 work/github-prior-art/REPOSITORY_MATRIX.csv at c756805692658c99394ca71f88203ba224e78c3c | f66cbcc0dc816a51b6a019e6ca7914818723951a | 012141caf12d3d622ad14214f83e5918227ab751e4e95698230d05c936346ba2 |
| B PR #32 work/github-prior-art/FAILURE_TEST_CHECKLIST.md at c756805692658c99394ca71f88203ba224e78c3c | 698ee44ca0305b75e04edde9a58e48d752e26739 | 7af96fd3c63cfea6af38e07180ac8d407476b6c1d434674bc424104e3e582cd1 |
| B PR #32 work/github-prior-art/run_toy_checks.py at c756805692658c99394ca71f88203ba224e78c3c | 4fdc64d059b52117163d5b75eb03f1eff83d102f | 9b9fc0e59517d8533ac94f4521e857391b5e48f69c2faf20cc31fb74cacd5bd4 |
| B PR #32 work/github-prior-art/TOY_CHECK_OUTPUT.txt at c756805692658c99394ca71f88203ba224e78c3c | a99ef2794c45a2fb58efcfb91fc1ce13af4df90b | 42103b5fb900f3c3ddf4265bed05f3e7280c494223c4aea32b6792aea38f8181 |

### Permitted C metadata

| Input at C PR #35 head 9870c710c3cba7bb9226c9eee8ec36687b96fd9d | Git blob SHA-1 | SHA-256 |
|---|---|---|
| work/source/source-lock.json | 81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf | ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71 |
| work/source/probe-metadata.json | 21aa9149b7b7db9b07f1aa3a4bf0312675a166bd | 1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533 |
| work/source/expected-calendar.json | 6ed720353472ba6f35391936c536d46fb6ae8c66 | 6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4 |

### Historical E artifacts

| Historical input | Git blob SHA-1 | SHA-256 |
|---|---|---|
| old PR #38 work/independent-audit/RESULT.md at d1335b29eeb01cdd4b71cd5ded62033b8468e539 | f29a5d38b16b54734a47c719c09922a461ee3fe4 | c0df6ce468558e22eff57056ecf88ac9b5817a67fdcedef3e9aa028878177c35 |
| old PR #38 work/independent-audit/AUDIT_MATRIX.csv at d1335b29eeb01cdd4b71cd5ded62033b8468e539 | 3ada00d887bc76f88c777d2a40ea410077e3e594 | a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7 |

The historical E findings were used only to distinguish old code findings from current reproduced results. The old E status was not altered, relabeled or applied to current D.

## Commands and next verification

Independent executions, runtime identity and fault results are recorded in TEST_LOG.txt. The complete D suite was run from exact fetched D bytes with only the three permitted C metadata files available. The E oracle validates the recorded D, I, frozen SPEC and C identities before running synthetic tests.

Before any I2 reconsideration, D must resolve current I/E identity binding and the compound rollback-receipt fault, then publish a fresh exact D identity and obtain a new independent E audit. The D/I owners must keep the gate closed while that sequence is pending. Separately, Integrator/platform/security/storage/research-operations owners must provide the operating controls and evidence listed above; source readiness and human/lineage gaps need their own evidence and dispositions.

## E deliverable identities

All four paths are confined to work/independent-audit/**.

| Deliverable | Git blob SHA-1 | SHA-256 |
|---|---|---|
| work/independent-audit/AUDIT_MATRIX.csv | 0f66ee9a73b13f6c74c6e342c807049f1da79040 | d3e8c2fcda5a209774d297b08d14a6fabc6aecb63ededb2a61a5e609a68034f5 |
| work/independent-audit/toy_oracle.py | a489c6feddfe3fd8787bc253cc08004a1a9ff325 | 973eb3d70859f00c9d5da42dddf2c899d408a64dcd4867396b6ce129fbe3e514 |
| work/independent-audit/TEST_LOG.txt | 0fb4a4be8f2ac04f8ed971fe95e8df8460ad7982 | 9d8aefe03c6aa6b83ee6f300b82380991efa54876b1581e2b79d98d752e16f4d |
| work/independent-audit/RESULT.md | Exact-head Git blob and SHA-256 are recorded in the completion readback because a file cannot embed its own final digest. |

The completion record must confirm the exact remote head, all four read-back byte comparisons, Git blob SHA-1/SHA-256 identities, and the allowlist-only diff.
