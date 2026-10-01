# CSM-002 implementation test matrix

Price inputs and calculation cases are synthetic/toy data. The Packet C integration test reads only the pinned source lock, probe schema metadata, and expected calendar; it creates its own synthetic CSV rows and does not read any probe response rows or `OBS_VALUE` contents.

| Packet scope | Status | Tests / implementation evidence | Remaining boundary |
|---|---|---|---|
| 1. Parse/validate; separate signal, target, metrics, and receipt | PASS for synthetic core and Packet C adapter | `ParseAndIdentityTests`; `PacketCIntegrationTests.test_exact_packet_c_artifacts_with_synthetic_csv_rows`; adapter checks exact seven series, dimensions, units, status, CSV columns, and gate/capture identity | No full-history capture or execution |
| 2. EUR constant, USD, inversion, q_b/q_a, 56-pair max, numeraire invariance | PASS | `FormulaTests` proves exact ratio identity, all 56 directed pairs, numeraire invariance, and catches the simple-return subtraction error | Synthetic algebra only |
| 3. Exact ties, unique extrema, EUR/USD winner/loser, 28 long-only distinction, equal pair average | PASS | Exact `Fraction` comparisons and required polarity, tie, direction, and rank tests | The 28-direction example is a toy orientation; no broker symbol convention is claimed |
| 4. Full grid, boundaries, missing months/endpoints/currency/status, no rollback/compression | PASS for grid logic and Packet C calendar identity | Calendar tests preserve every month slot; Packet C integration independently checks all 4,331 open dates, date-stream and month-end hashes, and the 203 month-end map | The calendar does not establish that ECB published a rate on every expected date |
| 5. Prefix invariance, future perturbation, temporal receipt limits | PASS for synthetic logic | Prefix/future-suffix perturbation and temporal receipt tests | Historical `AVAILABLE_AT` and same-day tradability remain UNKNOWN |
| 6. Fixed circular bootstrap, seed, type 7, missing slots, partial year, sufficiency and rules | PASS | Fixed 12-slot circular bootstrap, 10,000 replicates, seed, type 7, missing-slot preservation, zero-valid failure, and threshold boundary tests | No real-sample inference was run |
| 7. Gate CLI, capture preflight, ledger-before-outcome, hashes, no network | PARTIAL | Closed-gate no-read test; synthetic gate/capture identity checks; Packet C metadata hash and calendar bindings; ledger ordering and audit-hook tests | No real raw snapshot was captured or parsed. Human freeze is recorded, but independent audit, Integrator gate, trusted receipt channel, and process/file isolation remain unresolved |
| 8. Stable identity, fixed one-spec config, test log, guarantee boundaries, no unused search/execution feature | PASS for preparation artifacts | Frozen SPEC identity and human receipt are pinned; config drift and open-access state are rejected; fixed CLI; refreshed environment and test records; C artifact identities are pinned in the integration test | D code/config/test/environment identities must be independently audited before any later execution |
| 9. No-access receipt, discrepancies, Integrator recommendations | PASS | `RESULT.md` records D's no-access receipt, current C dependency, C's bounded scope, and the reported search-snippet exposure without reproducing observations | Integrator must account for that disclosure; market-outcome gate remains CLOSED |

## Verification

```bash
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/path/to/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/path/to/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/path/to/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

With the exact Packet C artifacts at the pinned blob identities, **42 tests passed** in Python 3.12.14 after the frozen SPEC identity refresh. Without those three environment variables, the 41 self-contained tests run and the external-artifact integration test is skipped. No Packet C `OBS_VALUE` was read or used by the D tests.
