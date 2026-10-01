# CSM-002 deterministic implementation runbook

## Current state

This module implements the proposed `SPEC-CSM-002-v01` bytes from proposal ref `36240da15fc83120d12d081c227f3e0dd8badaaa` (Git blob SHA-1 `a073e77dec14337ee20609ed6136e50a8c1e76e2`; file SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`). The contract remains `PROPOSED_NOT_FROZEN`; `DEC-CSM-002` keeps the market-outcome gate closed. The code has only been exercised with synthetic/toy inputs. Do not run it on actual FX history in this state.

The implementation performs a retrospective reference-rate association. It does not claim that the selected rates were available for executable entry. `AVAILABLE_AT` remains `UNKNOWN`; costs, carry, and financing remain `UNOBSERVED`.

## Local component verification

Use Python 3.11 or later and the standard library only:

```bash
python3 -m unittest -v test_csm.py
python3 -m py_compile csm.py test_csm.py
```

All current test vectors are synthetic. No external source, raw market history, ranking, or strategy performance was retrieved for this work.

## Preconditions for a future authorized run

All of the following must exist and agree before the command may read a full-history input:

1. A human contract decision that freezes the exact `SPEC-CSM-002-v01` bytes. The frozen receipt must retain the same Git blob identity recorded in `config.json`.
2. A completed C source lock and official expected TARGET operating-day calendar for the fixed source range. The adapter must map the seven exact series, currency units, statuses, and CSV fields without substituting another source.
3. An independent E audit and an I Integrator gate with `gate_status: PASS`, matching the code, tests, environment, source-lock, calendar, time-range, and access-ledger identities.
4. A preserved raw-capture snapshot plus a manifest whose source-lock identity, seven series keys, and SHA-256 match the bytes that will be read.
5. A new output directory. An existing output directory means preserve the attempt and stop; do not reuse it.

The gate receipt is a structured integrity check. This implementation does not cryptographically authenticate human, auditor, or Integrator identities, nor does it enforce operating-system access controls on a raw snapshot. A future authorized runner must provide a trusted receipt channel and file ACL/process isolation. A hand-written JSON object is not sufficient authorization by itself.

## Command shape after those conditions are met

The command accepts artifact paths only; there are no horizon, universe, seed, block-length, threshold, subgroup, or sweep options.

```bash
python3 csm.py run \
  --normalized-csv /secure/snapshot/normalized.csv \
  --source-lock /secure/receipts/source-lock.json \
  --expected-calendar /secure/receipts/expected-calendar.json \
  --capture-manifest /secure/receipts/capture-manifest.json \
  --gate-receipt /secure/receipts/integrator-gate.json \
  --output-dir /secure/runs/csm-002-attempt-001
```

The command fails before reading the data file unless the gate, source lock, code/test/config identity, and environment receipt pass. It then verifies calendar and capture hashes, installs a process audit hook that rejects network connection and subprocess events, parses the local source snapshot, and builds the entire target-month event grid. It writes and hashes `event-ledger.json` before any target return calculation. Primary metrics are persisted before inference; a later calculation/bootstrap failure writes `attempt-status.json` with `scientific_status: NOT_APPLICABLE`. Any data identity failure stops the attempt; it is not a negative scientific result.

After a valid gate, the output contains the per-slot log-return record, fixed metrics, bootstrap summary, and run receipt. Standard output contains status only; it does not print prices, price samples, rankings, or metrics. The primary metrics and inference files are sensitive market-derived output and must remain in the authorized output location.

## Adapter contract still pending

The current generic adapter expects the future source lock to define:

- `id`, `spec_id`, `source_transport`;
- `series_by_currency` for the exact seven ECB keys;
- `csv_field_map` for date, series, value, unit, and status columns;
- `unit_by_currency`;
- explicit `status_policy.valid` and `status_policy.missing` lists.

This is an integration boundary to reconcile against C's completed source lock. It does not assert that ECB's eventual response schema, status codes, or unit labels use these names. If the source-lock artifact differs, revise only the adapter under this bounded work; do not change the research specification or source selection.
