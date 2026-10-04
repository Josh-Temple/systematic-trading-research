---
id: IMPL-CSM-D-001
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PARTIAL_WITH_GAPS
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
---

# Packet D — outcome-blind deterministic implementation result

## Status

**PARTIAL_WITH_GAPS.** The deterministic core, synthetic tests, fixed configuration, operator notes, and source adapter for the current Packet C metadata/calendar are implemented. The exact Packet C lock, schema metadata, and expected calendar pass integration checks using generated synthetic CSV rows. No historical ECB observations or outcomes were read by Packet D. Full-history capture/execution remains unauthorized and untested; the market-outcome gate remains CLOSED.

## Initial preparation authority snapshot (pre-freeze)

- Repository: `Josh-Temple/systematic-trading-research`.
- `main_sha`: `1bba695ea252863c3b7366b8b910aa36e211c325`, freshly read from `refs/heads/main` on 2026-10-01.
- User-pinned `proposal_ref`: `36240da15fc83120d12d081c227f3e0dd8badaaa`; its parent was the recorded `main_sha`. Main and proposal remain separate refs.
- Architecture PR #31 currently reviewed at `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`. The Packet D branch is stacked on this architecture head; no merge to main was made.
- Fresh-read main files: `README.md`, `docs/RESEARCH_PRINCIPLES.md`, `schema/v0.1/README.md`. Root `AGENTS.md` returned 404.
- Fresh-read proposal files: line `README.md`, `ARCHITECTURE_REVIEW_2026-10-01.md`, `SPEC-CSM-002-v01.md`, `DEC-CSM-002.md`, Packets A–D, `references/GITHUB_PRIOR_ART_2026-10-01.md`, and `references/SOURCE_REVIEW_2026-10-01.md`.
- Exact proposed specification identity: Git blob SHA-1 `a073e77dec14337ee20609ed6136e50a8c1e76e2`; file SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`.

### Architecture-base update receipt

The architecture PR advanced from the pinned proposal ref to `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`, adding six reviewed commits. The changes updated prior-art/source-reuse review and Packets A/C; Packet D, `SPEC-CSM-002-v01`, and `DEC-CSM-002` were unchanged. The D branch integrates that current architecture head as its PR base while preserving the user-pinned proposal ref for the implementation contract. Main remained at `1bba695ea252863c3b7366b8b910aa36e211c325`.

### Packet C integration receipt

A fresh follow-up read found Packet C branch `work/csm-source-qualification-20261001` at `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`; its draft PR is [#35](https://github.com/Josh-Temple/systematic-trading-research/pull/35), based on the same architecture head. Packet D verified these current artifact identities:

| Packet C artifact | Git blob SHA-1 | File SHA-256 |
|---|---|---|
| `work/source-qualification/source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| `work/source-qualification/probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| `work/source-qualification/expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |

Packet C reports `PARTIAL_WITH_GAPS`: a bounded November 2009 route/schema/calendar check passed, while full-history coverage, historical publication time, and revision/vintage access remain UNKNOWN. Packet C also discloses an incidental search-result observation exposure that makes its evidence validity PARTIAL. Packet D did not retrieve, repeat, reproduce, or use those observations. This disclosure remains for E/Integrator review; it does not open the market gate.

## Implemented deliverables

- `work/implementation/csm.py`: Packet C source-lock and 32-column schema adapter; expected-calendar identity validation; exact-ratio signal selection; fixed calendar grid; event-ledger persistence/hash before outcomes; fixed bootstrap and metrics; temporal receipt, gate, capture, and network checks.
- `work/implementation/test_csm.py`: synthetic/toy tests plus a Packet C artifact integration test using synthetic CSV rows only.
- `work/implementation/fixtures/toy_cases.json`: explicitly synthetic toy vectors.
- `work/implementation/config.json`: one frozen-spec identity mirror; no search or parameter overrides.
- `work/implementation/RUNBOOK.md`, `ENVIRONMENT.md`, `TEST_MATRIX.md`, `TEST_LOG.txt`.

## Work matrix

| Packet item | Status | Result |
|---|---|---|
| 1. Pure parsing/validation; signal, target, metrics, receipt separation | PASS for synthetic core and Packet C adapter | The adapter checks seven exact ECB series, quote dimensions, units, decimal scales, status, schema, and source identities. Its CSV rows are generated synthetic values. |
| 2. EUR constant, USD inclusion, inversion, quote direction, 56 pairs, numeraire invariance | PASS | Synthetic exact-ratio tests establish the raw-extrema/all-56-pair identity and catch incorrect simple-return subtraction. |
| 3. Exact ties, unique extrema, EUR/USD winner/loser, 28 directions, pair-average rank | PASS | Required polarity, tie, direction, and ranking edge cases pass using synthetic inputs. |
| 4. Full grid, boundaries, missing data, no rollback/compression | PASS for logic and C calendar identity | Tests preserve the month grid. The exact C calendar file, 4,331 expected dates, date-stream/month-end hashes, and 203 month-end map validate. This does not prove a rate exists on every expected date. |
| 5. Prefix/future invariance and temporal receipt boundary | PASS for synthetic logic | Future suffix changes do not alter prior signal; fake availability and executable-timing claims are rejected. |
| 6. Fixed circular bootstrap, type 7, missing slots, sufficiency and decisions | PASS | Fixed 12-slot circular blocks, 10,000 replicates, seed, partial-year behavior, zero-valid failure, and decision boundaries pass synthetic checks. |
| 7. Gate CLI, capture preflight, ledger-first hash, identity and network boundary | PARTIAL_WITH_GAPS | The prior 4f739d9 head had only structural receipt checks. The current follow-up adds signed E/I2 identity checks, raw-byte source-lock binding, atomic staging, and fault tests; current I2 remains CLOSED, E remains BLOCKED, and production trust/OS/storage controls are unresolved. No raw full-history snapshot was captured or parsed. |
| 8. Stable identity, fixed config, test log, guarantees, no unused search features | PASS for preparation artifacts | Config drift is rejected; CLI exposes artifact paths only; code/test/environment and outputs receive hashes. |
| 9. No-access receipt and discrepancies for Integrator | PASS | This result records the current C dependency, the incident disclosed by C, all access boundaries, and remaining gates. |

## Initial verification and access receipt (pre-freeze)

- Python 3.12.14; standard library only.
- `python3 -m py_compile csm.py test_csm.py` — passed.
- `python3 -m unittest -v test_csm.py` with the three exact Packet C artifact paths set — **42 tests passed**.
- Packet C integration verifies the three pinned Git blob identities, validates source-lock/schema/calendar metadata, and parses only generated synthetic CSV rows. The C probe-response rows and `OBS_VALUE` fields were not loaded by Packet D.
- Packet D did not request market data, calculate rankings/forward returns/strategy metrics, or generate performance plots. No broker, live/paper order, Horizontal Reaction/H3, DATA-HR-003, Autonomous Pilot input, web UI, or MCP was accessed.
- The D CLI test confirms a CLOSED gate returns before reading its synthetic sentinel data file or creating an output directory.

```yaml
packet_d_actual_market_observations_read_or_used: false
packet_d_full_history_retrieved: false
packet_d_historical_rankings_computed: false
packet_d_forward_returns_computed_from_market_data: false
packet_d_strategy_metrics_computed_from_market_data: false
packet_c_metadata_and_calendar_read: true
synthetic_csv_rows_used_for_c_adapter_test: true
market_outcome_gate: CLOSED
scientific_status: NOT_APPLICABLE
```

## Facts, interpretation, and limitations

### Facts

- The frozen screen fixes eight currencies, seven non-EUR ECB series, all 56 directed pairs, one-month formation/target periods, a fixed month grid, and a 12-slot circular moving-block bootstrap.
- Packet C's source lock is `QUALIFIED_BOUNDED_ROUTE_ONLY`, identifies seven `D.{CCY}.EUR.SP00.A` series, and permits status `A`. Historical same-day availability and revision/vintage access remain UNKNOWN.
- The adapter checks C's exact ordered 32-column metadata schema and binds the source-lock identity, probe-metadata hash, calendar file hash, date-list hash, and monthly endpoint hash. CSV value parsing is exercised only with synthetic rows.
- The official calendar artifact defines 4,331 expected open dates and 203 monthly endpoints from 2009-11 through 2026-09. It is independent of observed prices; gaps are not filled or shifted.
- The source interface does not claim that the ECB reference values were available for executable entry. `AVAILABLE_AT` remains UNKNOWN and costs/carry/financing remain UNOBSERVED.

### Interpretation

- The pure math, grid logic, and current bounded source-interface adapter are ready for independent code review. They do not establish full-history executability or a scientific result.
- Packet C's partial evidence and disclosed observation exposure remain a downstream review item. Packet D treats those artifacts as metadata/schema/calendar only and keeps the outcome gate closed.
- At the prior head `4f739d9cc2b21c138771afec4a728bf2b57060ba`, the receipt validator checked structure and byte identities but did not authenticate human/auditor/Integrator identity. The outcome-blind correction below supersedes that implementation. Neither version provides OS-level file/process isolation.

### Limitations and unresolved gates

1. **Packet C is bounded and partial.** Full-history coverage, historical publication time, and revision/vintage availability are UNKNOWN. Do not infer continuity from the one-month probe.
2. **Search-result exposure disclosure.** Packet C reports an incidental observation exposure. Packet D did not repeat or use it. E/Integrator must review the disclosure before any outcome access.
3. **Human freeze does not open the outcome gate.** The exact SPEC bytes are frozen, but independent E audit, I2 gate PASS, receipt authentication/isolation, access-ledger assignment, and a separate X instruction remain outstanding.
4. **Receipt authenticity and isolation.** The correction implements cryptographic receipt verification, but trusted production keys and OS-level allowlist/isolation controls remain unresolved. The validator alone is not a complete deployment boundary.
5. **No actual history run.** Full-history coverage, missing/status distributions, raw-capture identity, metrics, and end-to-end output were not tested against real source bytes.

## Recommendations for E / Integrator

- Review the exact D code/test hashes with the exact C artifact identities recorded above. Inspect the C disclosure without reproducing observation snippets; retain the gate as CLOSED pending a documented decision.
- Independently audit exact-ratio tie handling, quote direction, missing-grid semantics, bootstrap rules, event-ledger ordering, and the no-output-before-gate path.
- Resolve trusted approval identity and OS/file/process isolation before any full-history read.
- Require a later authorized run to verify full-history coverage, status/missing/duplicate distributions, and revisions against the exact lock and calendar. Any operational failure remains `NOT_APPLICABLE`, not a negative strategy finding.

## Initial changed paths and identities (pre-freeze upload)

All D changes are under `work/implementation/**`. No main write, merge, force-push, shared spec/reference change, or other worker path change was made.

SHA-256 values for the eight other deliverables are recorded below. The `RESULT.md` digest is recorded in the final remote readback receipt because embedding a file's own digest would change it.

| Deliverable | SHA-256 |
|---|---|
| `work/implementation/csm.py` | `dfd42a29e4cd042ad44ce9461d29246c0609bee401463cd21b82e0f0d6a37267` |
| `work/implementation/test_csm.py` | `69693bba8efbfa37e64c0fe08be332d583a15b9f8f4d3c99652e70acba634171` |
| `work/implementation/config.json` | `5624c22c2ccad339cacc72b34d877eea5b0160ac7715f10d269ea984aa443ad1` |
| `work/implementation/fixtures/toy_cases.json` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |
| `work/implementation/RUNBOOK.md` | `5630c47255d7ad9665590c34c1017456af00596282a3ac540e46c5449b5e57ac` |
| `work/implementation/ENVIRONMENT.md` | `e9bf206a3fb46a0f03ad044db8a48b4cbcde7211146643164e12786d2d0f3740` |
| `work/implementation/TEST_MATRIX.md` | `a893af14752e04f4d3101190c16288ed12b345c61f0fa3720280cc7529d3b4f2` |
| `work/implementation/TEST_LOG.txt` | `2bb7c59b82f22b14e04151bdb2b2d6b8e69cdf72967c3e4ffea41d30a4433fd5` |
| `work/implementation/RESULT.md` | see the follow-up receipt below; a file cannot embed its own final digest |

## Post-freeze refresh and verification

### Fresh-read and contract receipt

- Fresh `main_sha`: `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c`. Compared with the prior recorded main `1bba695ea252863c3b7366b8b910aa36e211c325`, the only change is `research/lines/INDEX.md`; it explicitly keeps this research line on a non-main branch. This does not alter D's scientific or implementation inputs.
- Main files re-read: `README.md` (blob `3428fa1b67db3bc0f3d3d61cddb951773d75351b`), `docs/RESEARCH_PRINCIPLES.md` (blob `3338e5948de34da763fd14113afba43945fd6683`), and `schema/v0.1/README.md` (blob `01f67f3e301b5e7091ceaf9f06d7cd75b703f136`).
- The line remained on architecture ref `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`; the original user-pinned proposal ref `36240da15fc83120d12d081c227f3e0dd8badaaa` is retained separately. The line README, work README, architecture review, proposal SPEC, DEC-CSM-002, Packet D, Packet I, and required GITHUB_PRIOR_ART / SOURCE_REVIEW references were freshly read at their applicable refs.
- Human decision `HDEC-CSM-002-20261001` accepted the pre-freeze SPEC blob `a073e77dec14337ee20609ed6136e50a8c1e76e2` / SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`. Frozen SPEC identity: freeze-record commit `4ac1e797c777f33a467ec73b250401886d160e80`, blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`. A direct byte comparison confirmed the specification body is unchanged; only lifecycle frontmatter records the freeze.
- Packet C was freshly read at head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`. D used only its source-lock, probe-metadata, and expected-calendar artifacts; the exact blob and SHA-256 identities are listed in the Packet C integration receipt above.
- The frozen file and `DEC-CSM-003-FREEZE-20261001` were read from I PR #37 at head `677341e8185bf38b5cc6d4490260ddefb72eb561`; the freeze-decision blob is `04860b4f92af2295331637eec8ade5a3ac66af32`.

### D refresh

- Updated `config.json`, implementation SPEC identity constants/validation, and the config test to pin the frozen SPEC, retain the accepted pre-freeze identity and human decision, and reject an open market-access state.
- The science configuration remains unchanged: universe, formation/target periods, sample dates, signal, source role, bootstrap, thresholds, and decision rule remain fixed.
- Frozen status is distinct from execution permission. `market_outcome_access` remains closed pending I2 gate PASS and a separate X instruction. This D PR grants no market-data access and emits no gate PASS.
- Refreshed environment: Python 3.12.14 / CPython on Linux 6.18.44; Python standard library only. `python3 -m py_compile csm.py test_csm.py` passed. The exact Packet C metadata/calendar integration suite `python3 -m unittest -v test_csm.py` passed **42/42 tests** in 0.221s.
- SHA-256 for the eight D deliverables other than this result file:

| Path | SHA-256 |
|---|---|
| `work/implementation/csm.py` | `5a47700f7024e19a39f4dd1688bf343a132a21946672ac4a034aa51d0d8ebdd2` |
| `work/implementation/test_csm.py` | `70650ded3dec9e94d78f88f14691454cebf63a2b0155de5cb11df7bd2fe1a5ff` |
| `work/implementation/config.json` | `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` |
| `work/implementation/fixtures/toy_cases.json` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |
| `work/implementation/RUNBOOK.md` | `5f3348c0ddb93d8b57a6e406ce91d5ae7e022f0253eeb584c5d790115a817d4a` |
| `work/implementation/ENVIRONMENT.md` | `008085f4816178605e3fbed12ad26ce37fde3df6b908a41eb5ff17b8f42021b0` |
| `work/implementation/TEST_MATRIX.md` | `d000996f9bb381f9e99c9cd00c03e77a8f61d7a5fa73ff3ce0c1831d129ad670` |
| `work/implementation/TEST_LOG.txt` | `d8431198a09c8d343bdbf01ea330de75286373495331d0acb9cb92d3069816f2` |

The final `RESULT.md` SHA-256 and all nine remote Git blob identities are reported in PR #34 and the final readback receipt.

### Remote readback receipt

- At D branch head `c82c5cca33c77eff3003f50816baecaab4fbe1f3`, compared against base `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`, the complete diff was exactly the nine allowlisted `work/implementation/**` files.
- All nine files were fetched from that head and matched their local bytes exactly. Their Git blob SHA-1s at that readback were:

| Path | Git blob SHA-1 |
|---|---|
| `work/implementation/RESULT.md` (before this receipt was added) | `1484c09c2fe205838531b206756ee78823c62f38` |
| `work/implementation/csm.py` | `f1eddb69b988c57a3ce39e654261e94f5c5e7d52` |
| `work/implementation/test_csm.py` | `f3e5006c2931e9d459504142f270253571d3fb82` |
| `work/implementation/config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` |
| `work/implementation/fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` |
| `work/implementation/RUNBOOK.md` | `939447e212555dceb0d5090d39a4eaee46f86d1a` |
| `work/implementation/ENVIRONMENT.md` | `7313a07849b8104bd154bf991c27a85049b5fa04` |
| `work/implementation/TEST_MATRIX.md` | `fc767c84cb036a73ad3ac8dd600beba0ad603504` |
| `work/implementation/TEST_LOG.txt` | `2cdf9f479c6294fd0f5d44300b3d834c3b5462a3` |

This receipt changes only `RESULT.md`. The final branch head and fresh readback of the receipt-bearing `RESULT.md` are verified again after this update; the final file's own digest is recorded in PR #34 to avoid self-reference.

### Follow-up access and gate receipt

```yaml
packet_d_actual_market_observations_read_or_used: false
packet_d_full_history_retrieved: false
packet_d_historical_rankings_computed: false
packet_d_forward_returns_computed_from_market_data: false
packet_d_strategy_metrics_computed_from_market_data: false
packet_c_source_lock_probe_metadata_expected_calendar_read: true
packet_c_probe_response_rows_or_obs_value_read: false
synthetic_csv_rows_used_for_c_adapter_test: true
human_spec_freeze_recorded: true
independent_e_audit_complete: false
integrator_i2_gate: BLOCKED_CLOSED
market_outcome_access: CLOSED
scientific_status: NOT_APPLICABLE
```

The known limitations remain: full-history coverage, historical publication time, revisions/vintage, and actual missing/status distributions are unknown; Packet C and Integrator observation-exposure disclosures still need disposition; durable access ledger, trusted receipt authentication, and OS/file/process isolation are unresolved. No instruction was issued to X.

## Pull request receipt

- Draft PR: [#34](https://github.com/Josh-Temple/systematic-trading-research/pull/34), not merged.
- Base: `research/csm-architecture-review-20261001` at `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`.
- Branch: `work/csm-implementation-20261001`.
- The follow-up is restricted to Packet D's `work/implementation/**` allowlist. The final head and receipt-bearing remote blobs are verified after this update and recorded in PR #34.

## Outcome-blind correction follow-up (2026-10-02)

### Current result

**D status: `PARTIAL_WITH_GAPS`. Scientific status: `NOT_APPLICABLE`. I2 remains CLOSED; no market data was captured, no outcome was calculated, no gate PASS was emitted, and no X instruction was issued.** The current config remains valid and frozen: SPEC blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`, `freeze_status: FROZEN`. This is not a pre-freeze blocker.

### Changes made

1. **Signal event ledger:** each event records `a`, `b`, formation endpoints, per-currency score identities, input hashes, score calculation spec ID, and formation/calendar skip reasons. Scores use the exact `q(start)/q(end)` ratio used for ordering; their identities bind the two formation input values and frozen SPEC identity. Ledger bytes are formed from formation/calendar inputs only. Target endpoint values and availability are first accessed after the ledger has been written, flushed, fsynced, and hash-verified. Synthetic tests mutate and remove target values and confirm the ledger bytes remain identical.
2. **Receipt authenticity:** the production validator verifies separate signed E auditor and Integrator envelopes using trusted RSA public keys, checks role, signer principal, signature, key validity/revocation, receipt expiry, and exact D/SPEC/environment/source identities. The current I2 and E identities are pinned in code. The current I2 record is CLOSED and current E audit is PARTIAL_WITH_GAPS / BLOCKED, so these exact records cannot authorize a run. Synthetic tests cover unknown keys, placeholder and missing identities, absent/expired receipts, mismatched identities, and invalid signatures.
3. **Source-lock bytes:** the runtime hashes and parses the same raw source-lock byte buffer. The signed gate and capture manifest bind both its canonical object hash and raw-byte SHA-256. A semantically identical JSON file with different whitespace is rejected when its raw hash differs from the signed receipt.
4. **Save failures:** capture bytes are staged, validated, flushed, fsynced, and promoted without overwriting existing files. Calculation outputs are staged in a temporary same-filesystem directory, file hashes are checked, and the directory is promoted only after validation. The final success receipt is created only after promotion and parent fsync. Synthetic fault injection covers write, flush, file fsync, capture hash, rename, promotion, parent fsync, and success-receipt promotion. Failed cases leave no final successful output receipt.
5. **Security and operations:** `RUNBOOK.md` and `ENVIRONMENT.md` explicitly distinguish Python process audit hooks from OS-level isolation. They require a filesystem allowlist, OS-level file/process isolation, durable output storage, a persistent append-only access/attempt ledger, and a named outcome-access operator. D does not assign a real operator or production key.

### Current external identities and unresolved conditions

- I2 current record: PR #37 head `677341e8185bf38b5cc6d4490260ddefb72eb561`; `gate.json` blob `ba1670b0c13ec58e806838949a80574a5cbab6c4`, SHA-256 `54b7984b9853ee6a7b848d6fb473d6aeb7bc1f52c2d94d6c74ed13f43cc28dd6`; `GATE.md` blob `03707f1aa346945a368e98881e8aa6f99ae91fb9`, SHA-256 `d901a7726355916088ade7ed32e129a241a360cbbcd220a01319413650d9465d`. State is `CLOSED`, access false.
- E current audit: PR #38 head `d1335b29eeb01cdd4b71cd5ded62033b8468e539`, ID `AUDIT-CSM-E-20261002`; status `PARTIAL_WITH_GAPS`, recommendation `BLOCKED`. Result blob/SHA-256: `f29a5d38b16b54734a47c719c09922a461ee3fe4` / `c0df6ce468558e22eff57056ecf88ac9b5817a67fdcedef3e9aa028878177c35`. Matrix blob/SHA-256: `3ada00d887bc76f88c777d2a40ea410077e3e594` / `a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7`.
- **Trusted key root — GAP.** Owner: Integrator-designated platform/security administrator. Check: provision the authorized auditor and Integrator public keys at `/etc/csm-002/trusted-keys.json`, record key fingerprints, roles, validity and revocation state, and verify root ownership and non-writable group/world mode. No production keys were created or assigned by D; the file and signer identities are unverified here.
- **Filesystem/process isolation — GAP.** Owner: execution-platform/security owner, to be named by the Integrator. Check: provide a versioned OS-enforced allowlist/sandbox profile, then run negative probes for disallowed file reads/writes and process creation as the restricted runner identity. The Python audit hook is not evidence of this control.
- **Durable output and access ledger — GAP.** Owner: storage/platform and research-operations owners, to be named by the Integrator. Check: provision protected persistent storage, restart the runner, read back hashes, and verify an append-only attempt/access record including denials, input/output identities, retries, timestamps, and operator.
- **Outcome-access operator — GAP.** Owner: Integrator. Check: name the individual by full name and stable account ID, verify their access role, and include them in the signed I2 receipt and durable ledger. No person was assigned by D.
- Other existing gaps remain: Packet C is `PARTIAL_WITH_GAPS` and does not establish full-history coverage, historical publication time, or vintage; calendar authority still needs independent confirmation; the disclosed observation exposures and missing original pre-proposal user brief remain unresolved. They are not scientific results.

### Verification provenance

- **Reporter claims from the earlier D head:** the PR body and pre-correction RESULT described 42/42 tests and asserted that the event ledger preceded outcome computation. Packet E independently reproduced those 42 tests and its synthetic oracle at old D head `4f739d9cc2b21c138771afec4a728bf2b57060ba`; it identified the missing score identities, unsigned receipt acceptance, raw source-lock binding gap, and save-failure gap.
- **Direct reproduction for this correction:** this work executed the complete updated D suite using Python 3.12.14 and the three exact metadata-only Packet C refs listed in TEST_MATRIX/TEST_LOG. The observed command, exit status, test count, and individual test names are recorded in TEST_LOG. This is direct execution of D tests, not a new independent Packet E audit.
- **Remote readback:** after push, every changed D file is fetched from the exact PR #34 head, then its content, Git blob SHA-1, SHA-256, and path allowlist are checked. Packet E has not yet re-audited the corrected head; its prior BLOCKED recommendation remains the current independent audit state.

### Updated D artifact identities

Expected identities for the current D deliverables are below; the same values are recomputed from the exact remote PR #34 head during readback. `RESULT.md` does not embed its own digest; its exact final blob and SHA-256 are recorded in the completion response and PR #34.

| D artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `csm.py` | `95cf059a5e0d5b6742dfa885fce7b37c58f2362c` | `4db33063f0388b8b7ec0613fff8228a4aa3cb00b94855a557c5abcd3b86f4104` |
| `test_csm.py` | `e287ab6923d073058cfa0e5e7be46b9ea5bc537a` | `3499c6cf4bc52f5052c7ed76ef92da41c272cbb6a31980a51801372775f1f66f` |
| `config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` | `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1` |
| `fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |
| `RUNBOOK.md` | `3142c0291aa979bb80c28d71b4e47fc7408591ab` | `7fa355a6b071567ff6d4ea4290033f5635fc44b64159af2438acae69ecc14948` |
| `ENVIRONMENT.md` | `bf6d5b4c0381e967226ee0996736d858b524b8eb` | `8290c920ea74a05ef759281bcba2792f446f7cc53774f319bf9a57ec5e1e7d8f` |
| `TEST_MATRIX.md` | `03633916f0190925a01d6b26e5146956e657c31f` | `7cfbd342057ce8a9517fbbf44e464fb05beb60e6de82e47f4e1d8643e7da4bce` |
| `TEST_LOG.txt` | `c70e610064f92ba15527fb7f99b8796607a9a91f` | `84a6a88673b0502b53bf3b2eb0ca100d101d8bd57cfab3da08695285fc399f44` |


## Hardening follow-up — 2026-10-04

### Purpose

Resolve the two code-level blockers independently reproduced by Packet E at D head `6dccd49ee21e4ac29f55162f93ef3e65aa7a5779` without changing the frozen scientific contract:

1. stale mutable I/E identity pins in D;
2. compound final-directory-fsync plus rollback-deletion failure leaving `run-receipt.json`.

### Code-level resolution

**Non-circular I/E binding**

Production validation no longer embeds current I or E commit SHAs.

Instead, the trusted Integrator-signed I2 envelope must carry a structurally valid immutable I2 identity for PR #37 with:
- exact 40-hex head and Git-blob identities;
- exact SHA-256 identities;
- `gate_status=PASS`;
- `market_outcome_access=true`.

The separately trusted auditor-signed E attestation must identify PR #38 with:
- exact current result/matrix blob and SHA identities;
- `status=PASS`;
- `recommendation=ALLOW_I2`.

Crucially, the E signature must independently bind:
- the exact current D file-hash map;
- the exact current environment identity;
- frozen SPEC SHA-256;
- exact source-lock raw-byte SHA-256;
- expected-calendar SHA-256.

The Integrator gate independently binds the same D/runtime/source/calendar identities plus the named operator, run ID and access-ledger identity.

This removes the D -> I/E-head hard-code cycle while keeping stale evidence fail-closed.

**Final SUCCESS receipt commit**

The output promotion sequence now:
1. validates/fsyncs the staged tree;
2. renames the completed tree;
3. fsyncs the parent;
4. reads the pending success payload;
5. removes `_completion-pending.json`;
6. fsyncs the destination directory to persist the non-success marker removal;
7. publishes `run-receipt.json` with `atomic_write_verified` as the **last fallible success-path operation**.

No fallible success-path operation follows final SUCCESS receipt publication.

If final receipt publication fails, `atomic_write_verified` removes the receipt before D reports failure. Even if the outer failed-attempt directory deletion also fails, the residual directory has no `run-receipt.json` and cannot be interpreted as a successful run.

### Regression coverage

Three regressions were added:

- `test_compound_final_fsync_and_rollback_delete_failure_never_leaves_success_receipt`
- `test_dynamic_signed_i_and_e_identities_do_not_require_code_pin_update`
- `test_signed_e_attestation_must_bind_current_d_hashes`

The first reproduces the exact compound failure class reported by the prior independent E audit.

### Verification

Synthetic verification was executed in an audit-only GitHub Actions wrapper outside D's allowlist.

- audit wrapper PR: #49
- workflow: `CSM D synthetic verification`
- workflow run: `37165967827`
- D code/test head under test: `ab2c7adcb6669efe48fe3e4570f670a623295d57`
- exact Packet C metadata head: `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`
- Packet C source-lock/probe-metadata/expected-calendar SHA-256 checks: PASS
- Python compile: PASS
- full D synthetic suite: **56/56 PASS; 0 failed; 0 skipped**
- market outcome access: **none**

### Status after D follow-up

**D code-level status: READY_FOR_INDEPENDENT_E_REAUDIT.**

The two prior E code-level blockers above are addressed in D and directly covered by synthetic regressions.

This is not an E PASS and does not open I2.

Still outside D / unresolved:
- production trust-key provisioning and protected root-owned trust store;
- OS-level isolation and filesystem allowlist;
- durable output destination and restart readback;
- persistent append-only access/attempt ledger;
- named outcome-access operator;
- full-history source readiness and observed missing/status distribution;
- external calendar authority;
- historical publication timing and revision/vintage;
- human disposition of prior observation-exposure disclosures.

No market price/history, ranking, forward return, strategy metric, P/L, Sharpe, or performance plot was accessed or calculated.
