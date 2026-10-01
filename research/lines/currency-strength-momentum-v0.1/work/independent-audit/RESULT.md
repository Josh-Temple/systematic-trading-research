---
id: AUDIT-CSM-E-20261002
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-02
status: PARTIAL_WITH_GAPS
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-003-FREEZE-20261001
---

# Packet E — CSM-002 independent pre-outcome audit

## Result and recommendation

**Status: PARTIAL_WITH_GAPS.** I inspected the current remote contract, A/B/C/D artifacts and I records directly, reran D's synthetic test suite, and independently checked the frozen formulas, calendar rule, bootstrap and decision boundaries with E-authored synthetic code.

**Packet E recommendation: BLOCKED.** Keep I2 **CLOSED** and market-outcome access **false**. Do not issue an X instruction. The hypothesis remains untested; this is not a DEPRIORITIZE result.

The current D configuration matches the frozen SPEC, but PR #37's current body and gate records still bind to an earlier D head/config. The D CLI checks receipt fields but has no trusted receipt authentication. The human/E disposition of two disclosed observation exposures, full-history source readiness, durable access controls and file/process isolation are also unresolved. E made no market-result calculation.

## Fresh-read receipt and refs

Read directly from GitHub on **2026-10-02 (JST)**. The current default branch is main at `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c`. The required `README.md`, `docs/RESEARCH_PRINCIPLES.md`, and `schema/v0.1/README.md` were read at that main SHA. A fresh request for the CSM line README at main returned 404, so the line is not in current main.

| Role | Branch / PR | Fresh head or ref | State / use |
|---|---|---|---|
| Current main | `main` | `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c` | Current root documentation and main ref |
| User-pinned proposal | commit | `36240da15fc83120d12d081c227f3e0dd8badaaa` | Recorded separately; not treated as current main |
| Architecture | PR [#31](https://github.com/Josh-Temple/systematic-trading-research/pull/31), `research/csm-architecture-review-20261001` | `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff` | Open, draft, unmerged; exact proposal base for E |
| A | PR [#33](https://github.com/Josh-Temple/systematic-trading-research/pull/33), `work/csm-literature-20261001` | `5e45377b890877ff18275a7fbd4371ffe80c92ba` | Open, not merged; base e0f |
| B | PR [#32](https://github.com/Josh-Temple/systematic-trading-research/pull/32), `work/csm-github-prior-art-20261001` | `c756805692658c99394ca71f88203ba224e78c3c` | Open, draft; base e0f in PR metadata |
| C | PR [#35](https://github.com/Josh-Temple/systematic-trading-research/pull/35), `work/csm-source-qualification-20261001` | `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` | Open, draft; base e0f |
| D | PR [#34](https://github.com/Josh-Temple/systematic-trading-research/pull/34), `work/csm-implementation-20261001` | `4f739d9cc2b21c138771afec4a728bf2b57060ba` | Open, draft; base e0f |
| I | PR [#37](https://github.com/Josh-Temple/systematic-trading-research/pull/37), `work/csm-integration-20261001` | `677341e8185bf38b5cc6d4490260ddefb72eb561` | Open, draft; base e0f |
| E | `work/csm-independent-audit-20261001` | Created from `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff` | Stacked on the unmerged architecture branch, as Packet E requires |

PR #31 remains unmerged, so E uses its exact head and records main separately. The branch `work/csm-independent-audit-20261001` was absent before this audit and was created from e0f. E's only repository write paths are `research/lines/currency-strength-momentum-v0.1/work/independent-audit/**`.

Fresh-read proposal files included the line README, architecture review, work README, HYP-CSM-002, SPEC-CSM-002-v01, DEC-CSM-002 and Packet E at e0f. PR #37's current HUMAN_CONTRACT, RECONCILIATION, GATE, gate.json, preparation decision, freeze decision, EXP and DATA records were read at I head 677341e. A/B/C/D artifacts below were fetched from their own heads, not inferred from I's table.

## Contract, freeze and lineage

The exact human receipt is `HDEC-CSM-002-20261001`. HUMAN_CONTRACT.md records acceptance at `2026-10-01T21:35:55+09:00` of pre-freeze SPEC SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`. At the accepted proposal ref, the file's Git blob is `a073e77dec14337ee20609ed6136e50a8c1e76e2`. E independently recomputed that SHA-256 and Git blob identity.

At I head, the frozen SPEC Git blob is `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, with SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`. E independently recomputed both hashes and compared the bytes after YAML frontmatter: the scientific body is byte-for-byte identical. Freeze metadata changes are `status`, `freeze_status`, `frozen_at`, and `human_decision_ref`.

The chronology is consistent: DEC-CSM-002 authorizes preparation only; DEC-CSM-003_PREPARATION records the earlier HUMAN_BOUNDARY state and no acceptance; HDEC-CSM-002 accepts the exact proposed bytes; DEC-CSM-003_FREEZE records the later metadata freeze. Neither acceptance nor freeze authorizes data capture or outcome calculation.

Lineage at I head is explicit: HYP-CSM-002 is UNTESTED; SPEC-CSM-002-v01 tests that hypothesis; EXP-CSM-002 uses the SPEC and DATA-CSM-002 and remains PLANNED / NOT_RUN; DATA-CSM-002 is PLANNED, EXPLORATORY_DISCOVERY, and NOT_CAPTURED_FOR_EXPERIMENT. No confirmation sample is designated or accessed.

**Gap:** HUMAN_CONTRACT.md sets `original_instruction_ref: null` and says the original user brief preceding the exact SPEC proposal was not in the reviewed repository artifacts. E can verify the exact accepted and frozen bytes, but cannot independently compare them with that absent earlier brief. This does not weaken the exact-SPEC receipt, and it does not open I2.

## A/B/C/D remote deliverables and identities

All A, B and D deliverables listed below were fetched and read at the exact heads above. For C, E read only the three permitted metadata artifacts; no other C file was fetched.

| Worker | Remote path at that worker head | Git blob SHA-1 |
|---|---|---|
| A | `research/lines/currency-strength-momentum-v0.1/work/literature/RESULT.md` | `51bb89bc83dab3db6aad7b3df773b7ca586e9b63` |
| A | `research/lines/currency-strength-momentum-v0.1/work/literature/EVIDENCE_TABLE.csv` | `d52d1659c87fdab23f8ee58014b277c1343ae92a` |
| A | `research/lines/currency-strength-momentum-v0.1/work/literature/SEARCH_LOG.md` | `0e36124fd5f395a3434b38a62033c6a264c834f4` |
| B | `work/github-prior-art/RESULT.md` | `b835541c78f826237ee30d7e87aff42636ccb5d1` |
| B | `work/github-prior-art/REPOSITORY_MATRIX.csv` | `f66cbcc0dc816a51b6a019e6ca7914818723951a` |
| B | `work/github-prior-art/FAILURE_TEST_CHECKLIST.md` | `698ee44ca0305b75e04edde9a58e48d752e26739` |
| B | `work/github-prior-art/toy_checks/run_toy_checks.py` | `4fdc64d059b52117163d5b75eb03f1eff83d102f` |
| B | `work/github-prior-art/toy_checks/TOY_CHECK_OUTPUT.txt` | `a99ef2794c45a2fb58efcfb91fc1ce13af4df90b` |
| C | `research/lines/currency-strength-momentum-v0.1/work/source-qualification/source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` |
| C | `research/lines/currency-strength-momentum-v0.1/work/source-qualification/probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` |
| C | `research/lines/currency-strength-momentum-v0.1/work/source-qualification/expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/ENVIRONMENT.md` | `7313a07849b8104bd154bf991c27a85049b5fa04` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/RESULT.md` | `19db0847eb0e2cbd629e4072f7e658eb7919d7d4` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/RUNBOOK.md` | `939447e212555dceb0d5090d39a4eaee46f86d1a` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/TEST_LOG.txt` | `2cdf9f479c6294fd0f5d44300b3d834c3b5462a3` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/TEST_MATRIX.md` | `fc767c84cb036a73ad3ac8dd600beba0ad603504` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/csm.py` | `f1eddb69b988c57a3ce39e654261e94f5c5e7d52` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` |
| D | `research/lines/currency-strength-momentum-v0.1/work/implementation/test_csm.py` | `f3e5006c2931e9d459504142f270253571d3fb82` |

Independent SHA-256 checks for C match the I metadata identities:

| C metadata artifact | SHA-256 |
|---|---|
| `source-lock.json` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| `probe-metadata.json` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| `expected-calendar.json` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |

For D's current head, E independently computed SHA-256 values: csm.py `5a47700f7024e19a39f4dd1688bf343a132a21946672ac4a034aa51d0d8ebdd2`; test_csm.py `70650ded3dec9e94d78f88f14691454cebf63a2b0155de5cb11df7bd2fe1a5ff`; config.json `9235142b336080ccd87c731d95fe266f64402c202e0de3b7e372521747cccfe1`; TEST_LOG.txt `d8431198a09c8d343bdbf01ea330de75286373495331d0acb9cb92d3069816f2`. These match D's current post-freeze TEST_LOG identities. The frozen SPEC fields in current config match the frozen blob/SHA-256 above and state `freeze_status: FROZEN`.

## Methods and independent checks

- Reviewed D's code from PR #34 head, not D's self-description alone. The source has a fixed eight-currency universe, exact Fraction comparisons for growth ratios, log pair returns, a fixed calendar grid, and the fixed circular bootstrap.
- Reran `py_compile` and the exact remote D unit/integration suite against the three C metadata files recreated from their remote bytes: **42 tests passed, 0 failed, 0 skipped**.
- Created and ran `toy_oracle.py` using only hand-authored synthetic values and the permitted C calendar/source-lock metadata. E's independent oracle covered all 56 directed pairs, common-numeraire invariance, EUR/USD orientation, exact ties, log vs simple return, missing calendar slots, future-suffix invariance, the fixed bootstrap and threshold boundaries.
- E separately reconstructed the declared weekday/holiday calendar for 2009-11 through 2026-09, then checked the full date sequence, all monthly endpoints and each recorded SHA-256. The date stream matches the calendar artifact. This confirms internal consistency with its declared rule, not the external authority of the rule.
- Compared D's extrema, all-pair maximum, pair log return, and bootstrap outputs directly against E's independently written functions on synthetic values. All matched.
- Static source review found no network client, plot generation, date-row shifting/compression, `bfill`, parameter sweep, subperiod performance search, or market-value print path. D installs a Python audit hook before parsing/calculation and the CLOSED-gate test returns before reading its sentinel CSV. The hook is not OS-level isolation.

See `AUDIT_MATRIX.csv` and `TEST_LOG.txt` for the complete item statuses and command record.

## Nine-item audit matrix summary

| # | Status | Independent conclusion |
|---|---|---|
| 1 | GAP | Accepted/frozen byte identity and research lineage verified; original pre-proposal user brief is absent from repository receipts. |
| 2 | PASS | E synthetic oracle and direct D parity checks confirm quote, numeraire, log-return, 56-pair, EUR/USD and tie algebra. |
| 3 | GAP | Expected calendar sequence and hashes independently reconstruct; external calendar authority and full-history/source vintage readiness remain open. |
| 4 | PASS | No look-ahead/date compression or post-hoc search found in D implementation; synthetic causality tests pass. |
| 5 | PASS | Fixed bootstrap, percentile, missing-slot, coverage and decision rules match an independent synthetic oracle. |
| 6 | GAP | Capture-byte check exists, but a trusted gate receipt is not authenticated or pinned to the current I2/E identities; save-failure handling lacks atomicity tests. |
| 7 | GAP | No network client or output leakage path found, but process audit hooks do not provide filesystem/process isolation or a durable access ledger. |
| 8 | GAP | B is outside the line-relative path and based on an older merge-base; D ledger omits frozen-spec-required score identities; current I D identities are stale. |
| 9 | PASS | Claim limits and blockers are stated; recommendation is BLOCKED, not a market-result decision. |

## Material findings and next checks

### Current I records contain stale D identities

PR #37's body, RECONCILIATION.md, GATE.md, gate.json and EXP-CSM-002.md still refer to D head `2271ce68039e295aa3cd50b5b2431e1a03d5dfdc` and its pre-freeze config. The current PR #34 head is `4f739d9cc2b21c138771afec4a728bf2b57060ba`; its config blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` pins frozen SPEC blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`, and `FROZEN`. D's current code/test/config hashes were also rechecked above. **Treat the current I statement “D config still pins pre-freeze SPEC” as stale.**

The older values in I's gate.json are code blob `11e4fa7729e5ec1c271a9b4b54c76de4cf049466`, test blob `965e8f49ee9d5678d1022dfb45a313d79b4655b8`, config blob `a1e49571ae30d48a502c4964c14f36cf556d15bb`, and test-log blob `0d168ef8f5d3f73a5c98cf542e109e3d9697b094`. I's recorded D head and hashes are therefore stale for current D. The freeze decision's statement about D is a historical snapshot at freeze time; it is not a current identity receipt.

This staleness does **not** change I2. At the reviewed I head, GATE.md says BLOCKED / CLOSED and gate.json says `market_outcome_access: false`; those states remain in force until the Integrator refreshes and re-evaluates its own records. E did not edit I files or issue an I2 PASS.

### Gate trust and capture identity

D's `validate_gate_receipt` requires fields including PASS, FROZEN, access authorization, fixed SPEC identities and nonempty audit/Integrator IDs. It does not authenticate those IDs, verify a signature, or pin the receipt to a trusted current gate artifact. D's own synthetic integration fixture uses `SYNTHETIC_FIXTURE_ONLY` for those IDs and the validator accepts it. The current I2 gate is CLOSED, but the code's JSON checks alone cannot prove a future receipt came from an authorized Integrator or auditor.

The capture preflight does bind `raw_snapshot_sha256` to the exact byte buffer later parsed. Probe metadata and expected-calendar bytes are checked against hashes. For the source lock, the runtime validates structure and a canonicalized object hash; it records a separate raw file hash in a start receipt, but that raw file hash is not itself tied to a trusted gate receipt. Writes use exclusive file creation and a final success receipt, but not atomic replacement; no injected storage-failure test establishes safe promotion behavior in every failure point.

### Signal and audit ledger

The mathematical implementation matched E's synthetic oracle. One contract mismatch remains: SPEC section 4 calls for an event ledger with `a`, `b`, formation endpoints, **score identities**, and skip reasons before target outcomes. D's `SignalEvent` and ledger contain pair identities, dates, status and skip reason, but no score identity/value or hash. E did not alter D files; D's owner should resolve this and E should re-audit any changed hashes.

### A/B/C findings and disclosures

- A is `PARTIAL_WITH_GAPS`. Its prior evidence distinguishes basket/excess-return, time-series, basis and single-pair spot designs. Its adverse post-2010 evidence is relevant prior information but does not estimate this fixed specification.
- B is useful third-party code/failure evidence, not an outcome for HYP-CSM-002. The current PR #32 comparison from e0 to c756 is 5 commits ahead and 6 behind, with merge base `36240da15fc83120d12d081c227f3e0dd8badaaa`. Its five deliverables are at repository-root `work/github-prior-art/**`, while Work README requires line-relative `research/lines/currency-strength-momentum-v0.1/work/**`. E did not move or edit them.
- C remains `PARTIAL_WITH_GAPS`: its lock is `QUALIFIED_BOUNDED_ROUTE_ONLY`; the permitted artifacts do not establish full-history coverage, missing/status distribution or historical vintage availability.
- PR #37 records two exposure disclosures: C's search-result snippets displayed individual current observations, and an Integrator ECB reference-rate page returned a table with individual current observations. No values are repeated here. Disposition remains pending human/E review. E did not read C's RESULT.md, probe-response CSV, any `OBS_VALUE` values, or raw market data; the C exposure is acknowledged from I's current record and the permitted metadata only.

## Claim boundary, open conditions, and allowed read scope

This audit supports only that the current D implementation matches the frozen mathematical rules in the synthetic cases run, and that the stated calendar data is internally consistent with the rule recorded in the metadata artifact. It does not support an FX outcome, current strength ranking, executable entry, profitable strategy, full-history availability, revision-free data, or independent confirmation.

Open conditions for any later I2 consideration:

1. Integrator must refresh its gate and reconciliation from current PR #34/D and current C identities; no stale hash may be carried forward.
2. D must address score identity in the event ledger, trusted receipt authentication, exact source-lock byte binding, and injected save-failure behavior, then issue new code/test/config identities for audit.
3. A trusted isolated execution location, filesystem/process controls, named outcome-access owner and durable access/attempt ledger must exist.
4. Full-history source coverage, missing/status behavior, historical availability/vintage limits, and expected-calendar authority must be resolved to the extent required by the frozen association claim.
5. Human/E must disposition both reported observation-exposure incidents without reproducing the values.

**Allowed read scope used:** main README, research principles, schema README; architecture line README, architecture review, work README, HYP-CSM-002, SPEC-CSM-002-v01, DEC-CSM-002 and Packet E at e0; A all three deliverables; B all five deliverables; C source-lock, probe metadata, expected calendar only; D all nine deliverables; I HUMAN_CONTRACT, RECONCILIATION, GATE, gate.json, DEC-CSM-003 preparation/freeze, EXP and DATA records at I head.

**Not read:** C RESULT.md, C raw probe response CSVs, `OBS_VALUE` data values, full-history/raw market data, H3/H3 datasets, DATA-HR-003, Autonomous Pilot market inputs, broker/live/paper orders, or performance/output files from any market run. No external calendar-source material was retrieved during this audit.

## E artifact identities

Local SHA-256 values before push:

| E artifact | SHA-256 |
|---|---|
| `AUDIT_MATRIX.csv` | `a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7` |
| `toy_oracle.py` | `06dc7c3798e1a3a813dd4a7e3a9b06f38f4d327a999efb33d09eb36aca32bfe5` |
| `TEST_LOG.txt` | `be7cfff4cc8279062adfcf830dcc38c53736b99e5ea63f5db0ade95a175927f1` |

The four changed paths on the E branch are limited to `work/independent-audit/RESULT.md`, `AUDIT_MATRIX.csv`, `toy_oracle.py`, and `TEST_LOG.txt`. Final result SHA-256, exact remote head, readback hashes, path diff and draft PR URL were verified from GitHub and are reported in the completion response.
