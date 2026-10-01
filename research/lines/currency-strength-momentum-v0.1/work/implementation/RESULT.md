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
| 7. Gate CLI, capture preflight, ledger-first hash, identity and network boundary | PARTIAL | Closed-gate no-read behavior and synthetic gate/capture checks pass. No raw full-history snapshot was captured or parsed. Human freeze is now recorded; independent audit, Integrator gate, trusted receipt channel, and OS/process isolation are unresolved. |
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
- The receipt code checks structure and byte identities; it does not authenticate the human, auditor, or Integrator cryptographically or isolate files at the OS level.

### Limitations and unresolved gates

1. **Packet C is bounded and partial.** Full-history coverage, historical publication time, and revision/vintage availability are UNKNOWN. Do not infer continuity from the one-month probe.
2. **Search-result exposure disclosure.** Packet C reports an incidental observation exposure. Packet D did not repeat or use it. E/Integrator must review the disclosure before any outcome access.
3. **Human freeze does not open the outcome gate.** The exact SPEC bytes are frozen, but independent E audit, I2 gate PASS, receipt authentication/isolation, access-ledger assignment, and a separate X instruction remain outstanding.
4. **Receipt authenticity and isolation.** Trusted receipt/signing, ACL, and process-isolation controls remain unresolved. The JSON validator alone is insufficient authorization.
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
- The follow-up commit is restricted to Packet D's `work/implementation/**` allowlist. Exact branch head, nine-file path allowlist, and remote blob readback are recorded after the update.
