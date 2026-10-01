# CSM-002 implementation test matrix

Every test uses synthetic/toy values. The official ECB adapter and TARGET calendar integration remain dependent on Packet C's completed artifacts.

| Packet scope | Status | Tests / implementation evidence | Remaining boundary |
|---|---|---|---|
| 1. Parse/validate; separate signal, target, metrics, and receipt | PASS for pure core | `ParseAndIdentityTests`; distinct `parse_source_csv`, `select_extrema`, `pair_log_return`, `summarize_metrics`, receipt validators | Actual C status/unit/schema integration BLOCKED pending source lock |
| 2. EUR constant, USD, inversion, q_b/q_a, 56-pair max, numeraire invariance | PASS | `FormulaTests.test_eur_constant_usd_included_and_exact_extrema`; `test_all_56_directed_max_matches_unique_raw_max_minus_min`; `test_numeraire_invariance`; `test_quote_direction_and_simple_return_difference_bug` | None for synthetic algebra |
| 3. Exact ties, unique extrema, EUR/USD winner/loser, 28 long-only distinction, equal pair average | PASS | Exact Fraction comparisons and the corresponding six formula tests | The 28-direction orientation is only a toy canonical orientation; no broker symbol convention is claimed |
| 4. Full grid, boundaries, missing months/endpoints/currency/status, no rollback/compression | PASS for grid logic | Calendar tests preserve labels and target count, distinguish whole missing month / currency gap / missing expected endpoint, and reject inferred endpoints | Official holidays and expected TARGET dates BLOCKED pending C calendar |
| 5. Prefix invariance, future perturbation, temporal receipt limits | PASS for synthetic logic | `test_prefix_truncation_and_future_perturbation_preserve_past_signal`; `test_shared_boundary_is_reference_association_not_entry_claim` | Historical availability remains UNKNOWN |
| 6. Fixed circular bootstrap, seed, type 7, missing slots, partial year, sufficiency and decisions | PASS | `MetricsAndBootstrapTests` covers fixed 10,000-replicate wrapper, block length 12, seed, missing slots, zero-valid failure, type 7, 201-slot span / partial final year, 120 and 0.80 boundaries | No real-sample inference was run |
| 7. Gate CLI, capture preflight, ledger-before-outcome, hashes, no network | PARTIAL | Gate-closed CLI emits status only and creates no output; capture hash/identity checks; ledger ordering/hash check; audit hook; output hash code path | No run with source-lock/raw capture/calendar because C and human/E/I gates are absent; no real data read |
| 8. Stable identity, fixed one-spec config, test log, guarantee boundaries, no unused search/execution feature | PASS for preparation artifacts | `config.json` drift test; CLI has artifact-path arguments only; environment snapshot and hashes; `ENVIRONMENT.md`; full test log | Final code/environment identity must be reissued after C adapter integration and E audit |
| 9. No-access receipt, discrepancies, Integrator recommendations | PASS | `RESULT.md` records no-access receipt, proposal/main separation, adapter/calendar gates, and bounded recommendations | Revisit adapter findings after C completes |

## Current verification command

```bash
python3 -m py_compile csm.py test_csm.py
python3 -m unittest -v test_csm.py
```

Result: **41 tests passed** in Python 3.12.14. No test used external market data.
