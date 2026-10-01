# CSM-002 deterministic implementation runbook

## Current status

The implementation validates frozen `SPEC-CSM-002-v01`: Git blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9`, SHA-256 `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2`. The current config mirror says `FROZEN` and matches those bytes. Freeze is not an open blocker. The current I2 record is `CLOSED` and Packet E audit `AUDIT-CSM-E-20261002` is `PARTIAL_WITH_GAPS` / `BLOCKED`; the default validator therefore rejects outcome access. D does not grant access, capture data, calculate market results, or issue an X instruction.

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

The gate input must be a signed envelope. The I2 envelope must be signed by a trusted `integrator` key and contain a separately signed current E attestation from an `independent_auditor` key. Both use RSASSA-PKCS1-v1_5-SHA256; the verifier checks signer role, validity interval, revocation, receipt expiry (maximum 24 hours), payload signature, and exact current I2/E identities. Signed claims bind the frozen SPEC, D file hashes, runtime identity, source-lock canonical-object hash and exact raw-byte SHA-256, metadata/calendar hashes, access ledger, run ID, and named operator.

Production trust keys are not created or assigned by this D change. The runner expects `/etc/csm-002/trusted-keys.json`, a root-owned regular file that is not group/world writable. Platform/security staff must provision the auditor and Integrator public keys, their principal IDs, roles, validity intervals, and revocation state; then independently verify the provisioned fingerprints and file ownership/mode. The file is absent/unverified in this work, so production receipt validation remains unavailable and CLOSED. Synthetic test keys are accepted only by test calls; the production CLI does not enable that path.

The currently pinned I2 identity is PR #37 head `677341e8185bf38b5cc6d4490260ddefb72eb561`, gate.json blob `ba1670b0c13ec58e806838949a80574a5cbab6c4` / SHA-256 `54b7984b9853ee6a7b848d6fb473d6aeb7bc1f52c2d94d6c74ed13f43cc28dd6`, and `GATE.md` blob `03707f1aa346945a368e98881e8aa6f99ae91fb9` / SHA-256 `d901a7726355916088ade7ed32e129a241a360cbbcd220a01319413650d9465d`. Its state is CLOSED / access false. The pinned E identity is PR #38 head `d1335b29eeb01cdd4b71cd5ded62033b8468e539`, audit ID `AUDIT-CSM-E-20261002`, result blob `f29a5d38b16b54734a47c719c09922a461ee3fe4` / SHA-256 `c0df6ce468558e22eff57056ecf88ac9b5817a67fdcedef3e9aa028878177c35`, and matrix blob `3ada00d887bc76f88c777d2a40ea410077e3e594` / SHA-256 `a668e8e0f2530ef2d6a0bf1f67b86a31f9dfe28b01dd795e0b610ca191900ef7`. Its status is PARTIAL_WITH_GAPS / BLOCKED. Any later I/E update requires fresh identities and D re-audit; old receipts do not carry forward.

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

Calculation outputs are written under a same-filesystem temporary directory. Every file is fsynced and hash-checked against a completion manifest before the directory rename. Only after directory promotion and parent fsync does the runner atomically create the final success receipt. Write, flush, file/directory fsync, rename, and receipt-promotion failures are fault-injected in synthetic tests. Failed attempts remain in staging or are removed; they are not promoted as a successful run. The final destination's persistence, reader ACLs, and durable attempt logging remain external requirements above.

## Future command shape

This command is not currently authorized or runnable: the pinned I2 and E states fail closed, and the trusted production key store and external controls are not established.

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
