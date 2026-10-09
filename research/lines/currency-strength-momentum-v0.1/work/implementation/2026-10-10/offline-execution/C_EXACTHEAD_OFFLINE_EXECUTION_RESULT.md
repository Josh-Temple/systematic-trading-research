# C — Exact-head CSM offline execution attempt (2026-10-10 JST)

## Decision

**NOT_EXECUTED / BLOCKED_ENVIRONMENT / HOLD_NO_MERGE.**

The exact candidate and Packet C metadata identities were obtained and verified, but the candidate's complete Python files could **not be made available as a byte-exact isolated checkout in the execution environment**. The local runtime cannot reach GitHub (the attempted Git metadata read failed at DNS), while the authenticated GitHub connector can read repository blobs but does not mount those bytes into the offline Python filesystem. We did not reconstruct a partial checkout, run a substitute toy signer, dispatch Actions, or misreport static methods as executed tests. Per Wave C stop rule, actual `py_compile` and `unittest` **were not executed**. This report is a bounded negative execution receipt, not functional verification.

## Source and checkout identity (remote GitHub directly read)

- Repository: `Josh-Temple/systematic-trading-research`.
- Candidate: [PR #90](https://github.com/Josh-Temple/systematic-trading-research/pull/90), **OPEN / DRAFT / NOT MERGED**, head branch `work/csm-signature-separation-20261010-c`, **exact execution candidate SHA** `94e7719839dcacf281d7d479c597222582f0d920`, **commit tree** `32e851594810e51a3aefd05ca7cdc17af341885d`. PR base `work/csm-implementation-20261001` at `3695f0a8ed085669ec3644826889f9fc953a6808`. Fresh checked before creating report branch.
- PR #90 complete changed paths: `work/implementation/csm.py`, `work/implementation/test_csm.py`, and `work/implementation/2026-10-10/C_SIGNER_INDEPENDENCE_RESULT.md`, each under `research/lines/currency-strength-momentum-v0.1/`.
- Exact ref `94e771...`, source blobs directly read by authenticated GitHub connector:
  - `work/implementation/csm.py`: `cc3b788d637d0bacf63d9642788a196a1feaac56`
  - `work/implementation/test_csm.py`: `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282`
  - `work/implementation/fixtures/toy_cases.json`: `4e925eabb4d88772806f0e109c15680f17d73a31`
  - `work/implementation/RUNBOOK.md`: `4168e0010060586e0301aa221ec653913ea721ea`
  - `work/implementation/config.json`: `a1c1e140f8c0844fc554ae6fcd975bcb5e610770`
- These are **remote-code-read identities, NOT a local checkout identity**; no local candidate Git checkout SHA/tree can be claimed.

## PR #35 Packet C metadata-only verification (directly performed, without raw observations)

[PR #35](https://github.com/Josh-Temple/systematic-trading-research/pull/35) remains OPEN / DRAFT, exact head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`. All three files below were fetched from **that exact ref**, with no real `response.raw`, `OBS_VALUE`, observed CSV, full-history ZIP, or market outcome fetched or parsed. Expected SHA-256 values are those in candidate `RUNBOOK.md`. SHA-256 was computed over the retrieved UTF-8 byte representation by an isolated JavaScript SHA-256 implementation; the implementation was sanity-checked against the standard `abc` digest.

| Metadata-only path under `work/source-qualification/` | Exact Git blob SHA-1 | Computed SHA-256 | Verification |
| --- | --- | --- | --- |
| `source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` | **MATCH** Git blob + runbook SHA-256 |
| `probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` | **MATCH** Git blob + runbook SHA-256 |
| `expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` | **MATCH** Git blob + runbook SHA-256 |

These checks establish remote metadata identity only, not local fixture provisioning for the Python suite.

## Static preflight (not execution proof)

- Direct source inspection of `csm.py`, `test_csm.py`, the synthetic fixture, configuration, and runbook at the candidate ref found only Python standard-library imports in the two Python files. The `csm.py` CLI `run` path is guarded by `if __name__ == "__main__"`; **we did not invoke it**.
- `PacketCIntegrationTests.test_exact_packet_c_artifacts_with_synthetic_csv_rows` uses three `CSM_PACKET_C_*` paths, verifies Git blob identity, and builds synthetic CSV rows. Without these paths this test explicitly skips, so running without the verified inputs could not meet Wave acceptance.
- The `GateAndReceiptTests` source defines **62 `test_*` methods in total (static count, NOT a test result)**. The relevant definitions call the actual `csm.validate_gate_receipt` and some call `csm._verify_signed_envelope`, including positive distinct E/I identities and negative same principal, same RSA modulus despite distinct key IDs, roles/revocation/validity, stale current identities, altered signatures, and CLOSED gate. **No assertion was executed**, so no claimed acceptance/rejection is made.
- Static `validate_gate_receipt` code verifies separate signed E/I envelopes before checking E/I principal and RSA modulus; this describes the inspected candidate logic only. Code correctness and adversarial behavior remain **UNVERIFIED AT RUNTIME**.

## Actual local environment and command record

The isolated local Python environment reported **Python 3.13.5**; `git --version` reported `2.47.3`. The pre-execution GitHub ref probe:

```text
$ git ls-remote https://github.com/Josh-Temple/systematic-trading-research.git refs/heads/work/csm-signature-separation-20261010-c
fatal: unable to access 'https://github.com/Josh-Temple/systematic-trading-research.git/': Could not resolve host: github.com
```

This was an attempt to obtain **repository metadata before any test**; it was not a market-source or workflow request. No repository content was cloned/checked out locally. The following required commands remain **NOT_EXECUTED**:

```bash
cd research/lines/currency-strength-momentum-v0.1/work/implementation
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/verified/metadata-only/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/verified/metadata-only/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/verified/metadata-only/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

**Result accounting:** execution count **0**; test result **UNKNOWN**; `pass/fail/error/skip = NOT_OBSERVED`, not `62/0/0/0`. No start/end time for a suite exists; no unittest log exists; no Actions run/job was initiated. Prior historical 56/56 and toy-only 23/23 are not evidence about this SHA. No production trust store, OS ACL, real signer key, current observed source, or actual market gate was exercised.

## Current authorization boundary (independent remote read)

CSM integration [PR #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37) at `9162cae4f2e64ee3da07517f12a16092cc170161`, `work/integration/gate.json` Git blob `19442215345b35b0db3910c01acd910a5d57889b`:
`state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`. **HYP-CSM-002 remains UNTESTED.** This receipt does not modify the gate, code, source lock, runner, SPEC, workflow, or any main/research branch. No XM/MT5, ECB observed history, GDELT live requests, news classifications, market results, strategy performance, or trading actions were performed.

## Required next action and handoff to D / E

1. Provision an **authorized offline execution environment** with a complete byte-exact checkout of **#90 SHA `94e771...` / tree `32e851...`**, ensuring the five candidate source/config/fixture blobs above match on-disk Git identities; place only the three PR #35 metadata-only files at verified read-only paths and independently rehash their on-disk bytes.
2. Validate that this particular suite imports/executes no source acquisition, network, actual observed history, or unauthorized subprocesses. In that environment run exactly the runbook commands, capture Python version, time, complete verbose test log, count/pass/fail/error/skip, source/tree/blob hashes, and each required positive/adversarial test result. If any attempt requires real data or connectivity, **STOP**.
3. **Do not change #90's implementation** to obtain a PASS in this C report. Any fix must be a new authorized implementation and re-audit. D should independently record **C NOT_EXECUTED / HOLD** unless later exact-SHA direct runtime logs are supplied and verified. E must keep **CSM HOLD_NO_MERGE** regardless of any later scoped synthetic PASS until all external security/source/human gates are independently met.

## Scope and provenance

**Directly performed:** remote GitHub reads at exact refs; Git blob identity comparison; SHA-256 comparison for the three metadata-only files; static source/test inspection; local Python/Git version check and unsuccessful DNS-level checkout probe.

**Not performed:** exact local checkout; Python `py_compile`; Python `unittest`; dynamic RSA/signature validation; real source/history use; workflow triggering; any merge.

**Report-only allowlist:** `research/lines/currency-strength-momentum-v0.1/work/implementation/2026-10-10/offline-execution/**`.
**Execution candidate SHA is not the report-commit SHA.** The report's final PR head and exact changed paths must be verified by remote readback after this commit.
