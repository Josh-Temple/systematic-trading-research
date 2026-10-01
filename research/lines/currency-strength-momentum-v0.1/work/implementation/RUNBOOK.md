# CSM-002 deterministic implementation runbook

## Current state

This module implements the proposed `SPEC-CSM-002-v01` bytes from proposal ref `36240da15fc83120d12d081c227f3e0dd8badaaa` (Git blob SHA-1 `a073e77dec14337ee20609ed6136e50a8c1e76e2`; file SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`). The contract remains `PROPOSED_NOT_FROZEN`; `DEC-CSM-002` keeps the market-outcome gate closed. The calculation and adapter integration tests use synthetic/toy CSV rows only. Packet C's official source-lock, schema metadata, and expected calendar are read as metadata artifacts. This is not authorization to run on actual FX history.

The implementation performs a retrospective reference-rate association. It does not claim that the selected rates were available for executable entry. `AVAILABLE_AT` remains `UNKNOWN`; costs, carry, and financing remain `UNOBSERVED`.

## Local component verification

Use Python 3.11 or later and the standard library only:

```bash
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/path/to/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/path/to/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/path/to/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

For reproducibility, use the three artifacts from Packet C branch head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`. Without the environment variables, the 41 self-contained tests run and the exact-artifact integration test is skipped. All price rows and strategy calculations in tests are synthetic. No observation values, full-history prices, ranking, or strategy performance were read or calculated by Packet D.

## Preconditions for a future authorized run

All of the following must exist and agree before the command may read a full-history input:

1. A human contract decision that freezes the exact `SPEC-CSM-002-v01` bytes. The frozen receipt must retain the same Git blob identity recorded in `config.json`.
2. A C source lock and official expected TARGET operating-day calendar for the fixed source range. Current Packet C artifacts establish a bounded route/schema/calendar identity only; full-history coverage, historical publication times, and revision/vintage access remain unknown. The adapter maps the seven exact series, units, status, 32 CSV columns, and 203 month ends without substituting another source.
3. An independent E audit and an I Integrator gate with `gate_status: PASS`, matching the code, tests, environment, source-lock, calendar, time-range, and access-ledger identities.
4. A preserved raw-capture snapshot plus a manifest whose source-lock identity, seven series keys, and SHA-256 match the bytes that will be read.
5. A new output directory. An existing output directory means preserve the attempt and stop; do not reuse it.

The gate receipt is a structured integrity check. This implementation does not cryptographically authenticate human, auditor, or Integrator identities, nor does it enforce operating-system access controls on a raw snapshot. A future authorized runner must provide a trusted receipt channel and file ACL/process isolation. A hand-written JSON object is not sufficient authorization by itself.

## Command shape after those conditions are met

The command accepts artifact paths only; there are no horizon, universe, seed, block-length, threshold, subgroup, or sweep options.

```bash
python3 csm.py run \
  --source-csv /secure/snapshot/ecb-csvdata.csv \
  --source-lock /secure/receipts/source-lock.json \
  --probe-metadata /secure/receipts/probe-metadata.json \
  --expected-calendar /secure/receipts/expected-calendar.json \
  --capture-manifest /secure/receipts/capture-manifest.json \
  --gate-receipt /secure/receipts/integrator-gate.json \
  --output-dir /secure/runs/csm-002-attempt-001
```

The command fails before reading the data file unless the gate, source lock, probe-metadata, code/test/config identity, and environment receipt pass. It then verifies the C calendar and capture hashes, installs a process audit hook that rejects network connection and subprocess events, parses the local ECB CSV snapshot against C's exact 32-column schema and seven dimension/unit/status locks, and builds the entire target-month event grid. It writes and hashes `event-ledger.json` before any target return calculation. Primary metrics are persisted before inference; a later calculation/bootstrap failure writes `attempt-status.json` with `scientific_status: NOT_APPLICABLE`. Any data identity failure stops the attempt; it is not a negative scientific result.

After a valid gate, the output contains the per-slot log-return record, fixed metrics, bootstrap summary, and run receipt. Standard output contains status only; it does not print prices, price samples, rankings, or metrics. The primary metrics and inference files are sensitive market-derived output and must remain in the authorized output location.

## Packet C adapter integration boundary

The adapter accepts Packet C's exact `CSM-SOURCE-LOCK-ECB-001` structure and requires its accompanying `probe-metadata.json` for the ordered 32-column header. It checks all seven series keys and dimensions, quote units, decimal scales, ECB agency code, and status `A`, then maps `TIME_PERIOD` to the fixed-grid parser. The calendar adapter verifies the exact C artifact hash, 4,331 expected open dates, date-stream and month-end hashes, and all 203 month endpoints.

Integration tests pin the Packet C artifact Git blob identities and feed the adapter generated synthetic CSV rows. They do not parse Packet C's probe response rows or any historical `OBS_VALUE`. Packet C remains `PARTIAL_WITH_GAPS`; its bounded November 2009 probe does not establish full-history continuity, historical same-day availability, or revisions. The outcome gate remains closed.
