# CSM-002 deterministic implementation runbook

## Current status

The implementation validates frozen `SPEC-CSM-002-v01`: Git blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`. The current config mirror says `FROZEN` and matches those bytes. Freeze is not an open blocker. The current upstream I2 record is still `CLOSED` and the latest independent E audit remains `PARTIAL_WITH_GAPS` / `BLOCKED`; D therefore remains non-authorizing. The validator no longer hard-codes mutable I/E commit identities. Instead, a trusted Integrator-signed gate must identify a PASS/OPEN I2 artifact, and a separately trusted auditor-signed E attestation must bind the exact current D file hashes, environment identity, frozen SPEC, source-lock raw bytes, and calendar identity. D does not grant access, capture data, calculate market results, or issue an X instruction.

The implementation's score ledger is formed from the two formation endpoints only. It persists `a`, `b`, formation endpoints, per-currency exact-ratio score identities (including input hashes and the score-spec ID), and formation/calendar skip reasons before target endpoint values are accessed. Missing target observations are classified only after that ledger is persisted.

## Synthetic verification

Use Python 3.12 or later and the standard library. The test-only RSA private key is synthetic and is not a production trust key.

```bash
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/path/to/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/path/to/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/path/to/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

The three exact Packet C inputs are metadata only, read from PR #35 head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`: `source-lock.json` blob `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` / SHA-256 `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71`; `probe-metadata.json` blob `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` / SHA-256 `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533`; `expected-calendar.json` blob `6ed720353472ba6f35391936c536d46fb6ae8c66` / SHA-256 `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4`.

The integration test validates those metadata identities and generates its own synthetic CSV rows. It does not retrieve or read Packet C probe-response CSVs, observed values, market history, prices, rankings, forward returns, P/L, Sharpe, or performance plots. Other test rows and signed receipts are synthetic. TEST_LOG records the exact command, runtime, refs, and observed result.

## Receipt authentication

The gate input must be a signed envelope. The I2 envelope must be signed by a trusted `integrator` key and contain a separately signed current E attestation from an `independent_auditor` key. Both use RSASSA-PKCS1-v1_5-SHA256; the verifier checks signer role, validity interval, revocation, receipt expiry (maximum 24 hours), payload signature, and immutable Git/blob/digest identities.

The binding is intentionally **non-circular**. D does not embed the current I or E commit SHA. Instead:

- the Integrator-signed gate identifies PR #37, a 40-hex current head, exact gate blob/SHA identities, `gate_status=PASS`, and `market_outcome_access=true`;
- the auditor-signed E attestation identifies PR #38, exact result/matrix blob and SHA identities, `status=PASS`, and `recommendation=ALLOW_I2`;
- E must independently bind the exact current D file-hash map, environment identity, frozen SPEC SHA-256, source-lock raw-byte SHA-256, and calendar SHA-256;
- the Integrator gate independently binds the same D/runtime/source/calendar identities plus the named operator, run ID and access-ledger identity.

Rotating I/E heads therefore does not require a D code edit, while stale E evidence against older D bytes still fails closed.

Production trust keys are not created or assigned by this D change. The runner expects `/etc/csm-002/trusted-keys.json`, a root-owned regular file that is not group/world writable. Platform/security staff must provision the auditor and Integrator public keys, their principal IDs, roles, validity intervals, and revocation state; then independently verify the provisioned fingerprints and file ownership/mode. The file is absent/unverified in this work, so production receipt validation remains unavailable and CLOSED. Synthetic test keys are accepted only by test calls; the production CLI does not enable that path.

At the time of this update, the upstream I/E repository state remains non-authorizing. That state is recorded by I/E themselves rather than pinned in D.

## External run requirements — not established by D

These controls are conditions for any later outcome-access review. D cannot prove or provision them in this PR; each remains a GAP until its owner supplies evidence.

| Requirement | Owner | Verification evidence |
|---|---|---|
| Explicit filesystem allowlist for only the approved code, frozen metadata/receipts, one authorized input snapshot, and protected output/ledger paths | Execution-platform/security owner, to be named by the Integrator | Versioned sandbox policy plus denial probes for reads/writes outside each allowlisted path |
| OS-level file and process isolation; prevent unrelated users/processes from opening the snapshot or outputs | Execution-platform/security owner, to be named by the Integrator | Separate unprivileged run identity, enforced mount/ACL and process policy, and recorded negative tests for blocked file access and process creation |
| Durable output destination, with atomic promotion and readback after runner restart | Storage/platform owner, to be named by the Integrator | Provisioned protected destination, restart/persistence check, and readback of all output hashes |
| Persistent append-only access/attempt ledger, including denied attempts, run IDs, input/output hashes, operator, timestamps, and retries | Research operations/security owner, to be named by the Integrator | Ledger location and retention policy, append-only/tamper-evidence check, and a verified test record read back from the durable store |
| Named outcome-access operator | Integrator | Before any gate review, record the person's full name and stable account ID; verify their approved role and include the identity in the signed gate and durable ledger |

The Python audit hook blocks selected network and subprocess events inside this process only. It is not OS-level isolation, a filesystem allowlist, or protection from another process. A local staged attempt directory is not a durable access ledger.

## Capture and output safety

`atomic_capture_bytes` writes a same-directory temporary file, checks the exact raw-byte SHA-256 and caller-supplied content validator, flushes and fsyncs it, then promotes it without overwriting an existing capture. The run path reads a source-lock file once into a byte buffer, parses that buffer, and uses the same bytes for raw SHA-256 validation. Capture and gate receipts bind both the canonical object hash and exact raw-byte hash; semantically equal JSON with different bytes fails if its raw hash is not the signed value.

Calculation outputs are written under a same-filesystem temporary directory. Every file is fsynced and hash-checked against a completion manifest before the directory rename. After directory promotion and parent fsync, the runner first removes and fsyncs the non-success pending marker, then publishes `run-receipt.json` as the final fallible commit operation. No fallible success-path operation follows receipt publication. Write, flush, file/directory fsync, rename, receipt-promotion, and the independently reproduced compound final-directory-fsync plus rollback-deletion failure are fault-injected in synthetic tests. A reported failure must not leave `run-receipt.json`, even if the failed-attempt directory itself cannot be removed. The final destination's persistence, reader ACLs, and durable attempt logging remain external requirements above.

## Future command shape

This command is not currently authorized or runnable: upstream I2/E remain non-authorizing, and the trusted production key store and external controls are not established.

```bash
python3 csm.py run \
  --source-csv /secure/snapshot/ecb-csvdata.csv \
  --source-lock /secure/receipts/source-lock.json \
  --probe-metadata /secure/receipts/probe-metadata.json \
  --expected-calendar /secure/receipts/expected-calendar.json \
  --capture-manifest /secure/receipts/capture-manifest.json \
  --gate-receipt /secure/receipts/signed-integrator-gate.json \
  --output-dir /secure/runs/csm-002-attempt-001
```

No command option changes the fixed universe, dates, signal, target, bootstrap, thresholds, or decision rule. A blocked or failed execution is operational evidence with `scientific_status: NOT_APPLICABLE`; it is not a negative result.
