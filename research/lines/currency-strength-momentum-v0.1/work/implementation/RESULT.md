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

## Executive status

**PARTIAL_WITH_GAPS.** The deterministic core, synthetic test harness, fixed config, operator notes, environment record, test log, and full-scope matrix are implemented. The official source adapter and calendar integration remain blocked because Packet C's `source-lock.json` and expected calendar are not yet available. No market-data run was attempted. This is an implementation result, not a scientific result.

## Fresh-read and authority receipt

- Repository: `Josh-Temple/systematic-trading-research`.
- `main_sha`: `1bba695ea252863c3b7366b8b910aa36e211c325` (fresh `commits/main` read on 2026-10-01).
- `proposal_ref`: `research/csm-architecture-review-20261001` at exact head `36240da15fc83120d12d081c227f3e0dd8badaaa`; its parent is the recorded `main_sha` above. The two refs are distinct and the proposal is not treated as main authority.
- Architecture PR: [#31](https://github.com/Josh-Temple/systematic-trading-research/pull/31), draft/open when checked; the specified SHA is its head. The D branch was created from that exact SHA.
- Main `README.md`, `docs/RESEARCH_PRINCIPLES.md`, and `schema/v0.1/README.md` were read from main. Root `AGENTS.md` returned 404.
- Proposal-ref reads: line `README.md`, `ARCHITECTURE_REVIEW_2026-10-01.md`, `SPEC-CSM-002-v01.md`, `DEC-CSM-002.md`, `PACKET_A_LITERATURE.md`, `PACKET_B_GITHUB_PRIOR_ART.md`, `PACKET_C_SOURCE_QUALIFICATION.md`, this Packet D, `references/GITHUB_PRIOR_ART_2026-10-01.md`, and `references/SOURCE_REVIEW_2026-10-01.md`.
- Exact proposed specification identity: Git blob SHA-1 `a073e77dec14337ee20609ed6136e50a8c1e76e2`; file SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`.
- C dependency check on 2026-10-01: the branch search returned no `work/csm-source-qualification-20261001` branch and the specified `work/source-qualification/source-lock.json` path returned 404 at that ref. The required post-C fresh read and real adapter integration test are therefore BLOCKED; synthetic work proceeded as Packet D permits.

## Implemented deliverables

- `work/implementation/csm.py`: standard-library parser/identity checks, exact-ratio signal selection, pair log return, fixed calendar grid, pre-outcome event ledger and hash, fixed bootstrap, metrics, decision boundaries, temporal-receipt checks, gate/capture preflight, local loader, output hashes, and network/subprocess audit hook.
- `work/implementation/test_csm.py`: synthetic-only tests for all component behaviors and failure boundaries.
- `work/implementation/fixtures/toy_cases.json`: explicitly labeled synthetic toy vectors; no market data.
- `work/implementation/config.json`: one exact proposed SPEC mirror, with no horizon/search/threshold overrides.
- `work/implementation/RUNBOOK.md`, `ENVIRONMENT.md`, `TEST_LOG.txt`, and `TEST_MATRIX.md`.

## Work matrix

| Packet item | Status | Result |
|---|---|---|
| 1. Pure parsing/validation; separate signal, target, metrics, receipt | PASS for pure core; source adapter integration BLOCKED | Decimal positivity/finite checks, unit/status identity, date ordering, duplicates, plus distinct signal/target/metric/receipt functions. |
| 2. EUR/USD, inversion, quote direction, raw extrema vs 56 pairs, numeraire invariance | PASS | Synthetic tests establish the exact ratio identity and catch the incorrect simple-return subtraction. |
| 3. Exact ties, unique extrema, EUR/USD winner/loser, 28 directions, equal pair-average | PASS | Fraction-based exact ratio comparisons and all required synthetic polarity cases pass. The 28-direction example is only a toy orientation, not a broker quote convention. |
| 4. Full grid, date boundaries, holiday/weekend input, missing data, no rollback/shift | PASS for grid logic; official calendar BLOCKED | Expected dates are consumed verbatim; missing calendar/data slots remain in place. C's official operating-day artifact is absent. |
| 5. Prefix truncation, future perturbation, shared-boundary receipt | PASS for synthetic logic | Earlier selections remain unchanged; receipt validation refuses fabricated `AVAILABLE_AT` and same-reference executable claims. |
| 6. Metrics, fixed 12-slot circular bootstrap, type 7, missing grid, sufficiency/rules | PASS | Fixed 10,000 replicates and seed, missing-slot retention, partial final year, zero-valid failure, and 120 / 0.80 decision boundaries are tested. |
| 7. Local loader, preflight, ledger-first hash, gate, network boundary, output identities | PARTIAL_WITH_GAPS | Gate-closed CLI and capture/event identity checks pass. Real source-lock, calendar, and authorized full-history integration were not available or attempted. |
| 8. Stable identity, fixed config, test log, guarantees, no unused search features | PASS for preparation artifacts | Config drift fails; CLI has no scientific tuning switches; environment/code/config/test and output hashes are recorded by the runner. Final hashes must be reissued after C adapter integration and E audit. |
| 9. No-access receipt and Integrator recommendations | PASS | No-access receipt and unresolved adapter/receipt-boundary issues are recorded below. |

Full test-to-scope mapping is in `TEST_MATRIX.md`.

## Verification performed

- Environment: Python 3.12.14; standard library only.
- Commands: `python3 -m py_compile csm.py test_csm.py`; `python3 -m unittest -v test_csm.py`.
- Result: **41 tests passed**. Full output is preserved in `TEST_LOG.txt`.
- CLI gate test supplies a synthetic sentinel in a data file and a CLOSED gate. The CLI returns before reading that data file, emits no sentinel/rate/ranking/metric, and creates no output directory.
- Synthetic event-ledger test confirms outcome calculation fails if the ledger is missing, then succeeds only after exact ledger bytes are persisted and hash-checked.
- The runner preserves post-gate failures as operational `attempt-status.json` receipts with `scientific_status: NOT_APPLICABLE`; it does not map a loader/bootstrap failure to a negative result.
- No real ECB values, prices, historical rankings, forward returns, strategy metrics, or performance plots were retrieved or calculated. No network, broker, live/paper order, Horizontal Reaction/H3, DATA-HR-003, or Autonomous Pilot market input was accessed.

## No-access receipt

```yaml
actual_market_data_accessed: false
historical_rankings_computed: false
forward_returns_computed_from_market_data: false
strategy_performance_metrics_computed: false
market_outcome_gate: CLOSED
synthetic_or_toy_values_used_for_component_tests: true
synthetic_pair_log_return_used_only_for_component_test: true
external_market_data_requests: 0
scientific_status: NOT_APPLICABLE
```

## Facts, interpretation, and limitations

### Facts

- The proposed spec requires fixed monthly endpoints, eight currencies, all 56 directed pairs, a one-month formation and target, a 12-calendar-slot circular moving-block bootstrap, and the stated sufficiency/decision rules.
- This implementation compares `q(old)/q(new)` as exact rational numbers derived from decimal input, so exact extrema ties do not depend on floating-point/log rounding.
- The source parser constructs EUR as synthetic `q=1`; it accepts only the seven non-EUR source currencies.
- Missing endpoint dates or currencies do not roll back to an earlier observation and do not compress the target-month grid.
- The local source adapter currently expects a generic source-lock mapping (`series_by_currency`, `csv_field_map`, `unit_by_currency`, `status_policy`, `source_transport`). C's authoritative lock was unavailable at the dependency check.

### Interpretation

- The pure math and calendar-grid behavior are ready for independent review, but this is not evidence that the proposed screen is executable against the ECB source.
- The gate enforces exact identities and required approval fields. It is not a cryptographic identity system and does not provide operating-system isolation. A trusted receipt channel, ACL, and isolated runner must be resolved before any actual full-history read.
- The adapter field names are an implementation interface, not a change to canonical science or a claim about ECB's eventual wire schema. C may require a bounded adapter adjustment once its source lock is available.

### Limitations / unresolved discrepancies

1. **C source-lock and calendar absent:** exact ECB status codes, CSV schema, unit labels, transport, expected TARGET dates, and calendar hash remain UNKNOWN. No defaults were invented. Reconcile the adapter with C's completed artifacts, then add the required integration tests.
2. **Specification still proposed:** `DEC-CSM-002` says `HUMAN_BOUNDARY`; the gate remains CLOSED. The code does not authorize outcome access merely because it exists or its tests pass.
3. **Receipt authenticity:** the CLI checks receipt structure and hashes, but an authorized human/auditor/Integrator identity is not cryptographically verified. The next gate must specify a trusted signing/ACL mechanism or explicitly block execution until one exists.
4. **Calendar authority:** tests prove that the code follows the supplied date map; they do not prove that dates are official TARGET operating-day endpoints.
5. **No market execution:** full-history loader behavior, coverage, statuses, and end-to-end output hashes have not been exercised against real source bytes. No scientific finding follows from this preparation work.

## Recommendations for E / Integrator

- After C completes, fresh-read its exact source-lock and calendar commit, check all seven series/unit/status/field mappings, and add a metadata-only adapter integration test under `work/implementation/**`. If the source lock requires different fields, change the adapter only and rerun the entire synthetic suite.
- Have E independently review the exact implementation/test hashes, exact-ratio tie logic, pair direction, missing-grid and bootstrap semantics, event-ledger ordering, and the production CLI's no-output-before-gate behavior.
- Keep the market gate CLOSED until the human freeze, C source/calendar identities, E audit, I gate, exact code/environment/test identities, and a trusted receipt/file-isolation boundary are all present.
- Treat any adapter or code correction as an implementation revision before outcome access. Do not interpret a blocked source or failed test as a negative strategy result.

## Changed paths and identity

All changed paths are under the Packet D write allowlist `work/implementation/**`. No merge, force-push, shared CURRENT/spec/reference update, or other worker path change was made.

Local SHA-256 before upload:

| Deliverable | SHA-256 |
|---|---|
| `work/implementation/csm.py` | `e47913deb5f138264d253bdee984736c0b59420103b6f7d8d3bead325f31f958` |
| `work/implementation/test_csm.py` | `8b73d149101ad038d448654be2602e364e3d02f956a5df4792d9445fbc0bc98c` |
| `work/implementation/config.json` | `5624c22c2ccad339cacc72b34d877eea5b0160ac7715f10d269ea984aa443ad1` |
| `work/implementation/fixtures/toy_cases.json` | `08e0cb95402f5110bcfac494e590cb2d57fd033dde2e5d79a038454526c39f6c` |
| `work/implementation/RUNBOOK.md` | `964bfed5a8246b9c4a36939216f8ae2fdc60fea80d02e99c1902a52cb0db2fd7` |
| `work/implementation/ENVIRONMENT.md` | `c612f279cdc49b79fada3303d6bb8144067010dfcae72cb538c78b853b8830fd` |
| `work/implementation/TEST_MATRIX.md` | `a1d856e8dba58b6ea50d3e669d9dc112e1fdd1a932880b396e1224dcf2c13701` |
| `work/implementation/TEST_LOG.txt` | `e161d272ce696fd5c5c06e5304a3f03ff5368089f90cf4af9ac61093c30945d9` |
| `work/implementation/RESULT.md` | Exact digest is reported with the final remote readback because embedding a file's own hash would alter that file. |

After upload, every deliverable will be fetched from the exact remote branch head and compared byte-for-byte with the local file. The final result records the branch head, PR URL, and `RESULT.md` digest.
