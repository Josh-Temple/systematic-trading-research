# CSM-002 implementation test matrix

All calculation, receipt, persistence, and fault-injection inputs are synthetic. Packet C is used only for the exact source-lock, schema metadata, and expected-calendar identities listed below; the suite generates synthetic CSV rows. No probe response CSV or observed values are read.

| Area | Tests / current result | Evidence established | Remaining boundary |
|---|---|---|---|
| Parsing, exact-ratio formula, quote direction, all 56 directed pairs, ties, EUR/USD, numeraire invariance | Existing `ParseAndIdentityTests` and `FormulaTests`; PASS | Frozen mathematical rules on toy vectors | No market data or strategy result |
| Calendar grid, missing data, temporal boundary, no compression | Existing calendar tests; PASS | Formation-only signals, fixed slots, target missingness handled after the pre-outcome ledger | Full-history coverage and external calendar authority remain open |
| Pre-outcome ledger and score identity | `test_pre_outcome_ledger_records_a_b_and_all_score_identities`; `test_score_ledger_is_independent_of_target_values_and_target_availability`; PASS | Every currency has a deterministic score identity, input hash, and score-spec ID; event ledger includes `a`, `b`, formation endpoints, and pre-outcome skip reason; target value/presence changes leave ledger bytes identical | Future independent Packet E review is required |
| Receipt authenticity and freshness | `test_signed_gate_receipt_accepts_only_trusted_e_and_i2_signatures`; `test_gate_rejects_arbitrary_signing_key_and_bad_signature`; `test_gate_rejects_placeholder_missing_and_expired_receipts`; current-I/E blocking tests; PASS | RSA signature, role, trusted-key lookup, expiration, exact I2/E identity, D file/environment identity, and named operator checks fail closed on synthetic envelopes | Production keys and root trust-store provisioning are absent; actual I2 remains CLOSED and E remains BLOCKED |
| Source-lock raw bytes | `test_capture_preflight_hash_and_identity`; `test_source_lock_raw_byte_identity_rejects_semantically_equal_json`; PASS | Same source-lock buffer is parsed and raw-hashed; signed raw-byte mismatch fails even when parsed JSON is semantically equal | External receipt issuer must sign the exact captured bytes |
| Capture/output write safety | Atomic capture and output fault-injection tests; PASS | Injected write, flush, file-fsync, rename, promotion, and receipt-promotion failures do not leave a final success receipt; staged output hashes are checked before promotion | Durable storage and restart readback require platform provisioning |
| Bootstrap, metrics, decision boundaries | Existing bootstrap and metrics tests; PASS | Frozen seed, block length, replicate count, percentile, missing-slot handling, and thresholds on synthetic inputs | No real-sample inference |
| Packet C metadata integration | `PacketCIntegrationTests.test_exact_packet_c_artifacts_with_synthetic_csv_rows`; PASS | Exact blob/SHA checks for source-lock, probe metadata, and calendar; metadata schema validation; generated synthetic CSV rows | C remains `PARTIAL_WITH_GAPS`; metadata does not prove full-history availability or vintage |
| No-access CLI and status boundaries | Closed-gate CLI test; PASS | Closed gate returns without reading the sentinel source file or creating the final output directory | No full-history capture/execution is authorized |

## Exact Packet C input refs

Fetched at PR #35 head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`:

| Metadata artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `work/source-qualification/source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| `work/source-qualification/probe-metadata.json` | `21aa9149b7b7db9b07f1aa3a4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| `work/source-qualification/expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |

## Verification command and count

```bash
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/path/to/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/path/to/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/path/to/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

The original 42-test suite was extended with 11 regression and fault-injection tests. The required full run is 53 tests total, with the Packet C integration test enabled (0 skips). Exact runtime, command, input refs, exit codes, and observed test summary are in `TEST_LOG.txt`.

## Status boundary

`PARTIAL_WITH_GAPS`. These tests establish synthetic implementation behavior only. They do not establish a trusted production key root, a current PASS I2 gate, a PASS E audit, OS-level isolation, a filesystem allowlist, durable output/attempt storage, a named outcome-access operator, full-history data readiness, or any scientific result. No market data was read or requested.
