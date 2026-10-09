# C — CSM #90 exact-checkout offline execution receipt (2026-10-10 JST)

## Result and authority

**NOT_EXECUTED / BLOCKED_ENVIRONMENT / HOLD_NO_MERGE.** This is a report-only receipt. **testsRun = 0; PASS/FAIL/ERROR/SKIP = NOT_OBSERVED** (not zero observed failures). `py_compile` and `python3 -m unittest -v test_csm.py` **were not executed**. No claimed offline functional PASS, no independent signer-production assurance, no source qualification, no gate or market-outcome authorization.

The **C-0 full byte-exact Git checkout prerequisite failed**: an isolated local working directory had no Git checkout and the tested Git acquisition route could not resolve `github.com`. Although GitHub connector reads established remote commit/tree/blob identities and remote metadata SHA-256 values, those reads **do not establish an executable complete exact checkout**, and remote SHA-256 calculations are **not runtime-local file verification**. Reconstructing a partial tree by copying connector-returned fragments is expressly disallowed. Therefore C-1 was not attempted.

## Remote GitHub identities (fresh read during this session)

- Repository: `Josh-Temple/systematic-trading-research`.
- CSM source candidate: Draft/open [PR #90](https://github.com/Josh-Temple/systematic-trading-research/pull/90); base `work/csm-implementation-20261001`; source branch `work/csm-signature-separation-20261010-c`.
- **Execution target before this report:** commit `94e7719839dcacf281d7d479c597222582f0d920`; Git tree `32e851594810e51a3aefd05ca7cdc17af341885d`; parent `e28bec98badc88dfb4976bcd9804157d402f79fc`.
- PR #90 complete changed-file list (3): `work/implementation/csm.py`, `work/implementation/test_csm.py`, `work/implementation/2026-10-10/C_SIGNER_INDEPENDENCE_RESULT.md` (all under `research/lines/currency-strength-momentum-v0.1/`).
- Source code/fixture identities under `research/lines/currency-strength-momentum-v0.1/work/implementation/` from exact #90 tree:
  - `csm.py` Git blob `cc3b788d637d0bacf63d9642788a196a1feaac56`.
  - `test_csm.py` Git blob `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282`.
  - `fixtures/toy_cases.json` Git blob `4e925eabb4d88772806f0e109c15680f17d73a31` (fixture marks itself `SYNTHETIC`, `prices_are_market_data=false`).
  - `RUNBOOK.md` Git blob `4168e0010060586e0301aa221ec653913ea721ea`.
  - `config.json` Git blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770`.
- The recursive GitHub Git-tree API returned **219 tree entries, truncated=false**, and matched the five identities above. This is a **remote tree listing**, not a reconstructed local `git checkout`.

## Packet C metadata-only identities (remote verification, NOT runtime verification)

Packet C source: Draft/open [PR #35](https://github.com/Josh-Temple/systematic-trading-research/pull/35), exact head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`. Only the three allowed metadata-only JSON files were fetched through the GitHub connector, their returned UTF-8 text was hashed in the connector execution context, and their computed SHA-256 values were compared against `RUNBOOK.md`. A standalone SHA-256 implementation was checked first against the known SHA-256(`abc`) test vector.

| File (under `work/source-qualification/`) | Git blob from exact #35 | Computed SHA-256 of remote UTF-8 content | Comparison with RUNBOOK |
| --- | --- | --- | --- |
| `source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` | MATCH |
| `probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` | MATCH |
| `expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` | MATCH |

This was **not** a locally staged, read-only, independently rehashed metadata fixture set. The runtime-side prerequisite remains unsatisfied. No `response.raw`, real probe CSV, observed value, history ZIP, price, or outcome was accessed.

## Static review only — never an executed test result

- `RUNBOOK.md` requires Python 3.12+, standard library, `python3 -m py_compile csm.py test_csm.py`, and the exact `CSM_PACKET_C_SOURCE_LOCK`, `CSM_PACKET_C_PROBE_METADATA`, `CSM_PACKET_C_EXPECTED_CALENDAR` environment bindings for `python3 -m unittest -v test_csm.py`.
- `csm.py` imports shown in the exact remote file are Python standard-library modules. Its existing `_verify_signed_envelope` checks role, revocation, principal, issuance/expiry window, and RSA signature. Its existing `validate_gate_receipt` checks signed E/I2 receipt identities, source-lock raw identity, and authorization conditions; the production trust-store path remains protected. These are **code observations**, not tested behavior in this session.
- `test_csm.py` contains **62 statically enumerated `test_` method definitions**. Identified named tests include normal independent E/I keys; rejection of same principal, same public modulus under distinct key IDs, role swap/revocation/future validity, stale I/E identities, modified E signature; frozen metadata handling; and CLOSED/no-access gate tests. **None ran**; the listed test cases are not PASS.
- C-0 import-time and runtime call-graph isolation was not independently established as an executable environment guarantee. Production CLI `csm.py run` was **not** invoked. No workflow was created, edited, or dispatched.

## Local environment proof and failure log

Local runtime: **Python 3.13.5**; Git **2.47.3**. Checked on 2026-10-10 JST (local clock evidence `2026-10-10T08:55:32+09:00`).

```text
$ python3 --version
Python 3.13.5
$ git --version
git version 2.47.3
$ git ls-remote https://github.com/Josh-Temple/systematic-trading-research.git refs/heads/work/csm-signature-separation-20261010-c
fatal: unable to access 'https://github.com/Josh-Temple/systematic-trading-research.git/': Could not resolve host: github.com
[exit 128]
$ git -C /mnt/data/csm-exact-checkout-20261010 rev-parse --is-inside-work-tree
fatal: not a git repository (or any of the parent directories): .git
[exit nonzero]
local_dir_exists=True
local_git_checkout_exists=False
```

No `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git ls-tree`, or local Git blob rehash could execute from a verified checkout. The ability to see blobs through the connector is **not** a substitute for a local Git identity check.

**Not-run commands** (for future controlled execution only; not a command log):

```bash
python3 -m py_compile csm.py test_csm.py
CSM_PACKET_C_SOURCE_LOCK=/verified/metadata-only/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/verified/metadata-only/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/verified/metadata-only/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

**C-1 suite report:** `testsRun=0`; `py_compile=NOT_EXECUTED`; `unittest=NOT_EXECUTED`; failure/error/skip = `NOT_OBSERVED`; test-run start/end timestamps, test command exit codes and passing assertion logs = `NOT_APPLICABLE` because no test process was started. The only exit code observed above is for the *Git acquisition probe*, not for either planned test command.

## Non-authorizing gate and write controls

- Independently remote-read PR #37 gate artifact at `9162cae4f2e64ee3da07517f12a16092cc170161`: `work/integration/gate.json` blob `19442215345b35b0db3910c01acd910a5d57889b`; `state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`. This is the PR #37 snapshot, **not proof of current integration-branch state**.
- This C report branch is based on #90's exact target commit. The report must remain **Draft PR, report-only**, base `work/csm-signature-separation-20261010-c`. No code, tests, fixture, source, workflows, gate, or main branch changes; no merge. **Final report commit/tree differ from source execution target**; post-save GitHub readback must establish that `csm.py`, `test_csm.py` and fixture blobs remain the same.
- Source-qualification and production execution conditions remain unresolved. No real key, protected trust store, live ECB observation, outcome, XM/MT5, paper/live trade, or new source request was involved.

## Minimum conditions to retry and independent D handoff

1. Make a **complete cryptographically verifiable exact checkout** of #90 final commit available in an isolated Python >=3.12 environment; prove `git rev-parse HEAD`, `HEAD^{tree}`, `git ls-tree`, all relevant blob IDs before test execution, and that no actual source/history inputs can be opened.
2. Stage only the three PR #35 metadata JSON artifacts as read-only **actual local files**, recompute each SHA-256 from runtime bytes against `RUNBOOK.md`, and verify the import-time/test call graph and external-network/process blocking.
3. Only then run the unchanged `py_compile` and `unittest -v` commands, capture actual timestamped full logs, errors/failures/skips, named positive/negative tests and exit codes, and save a new exact-head receipt. Never relabel this unexecuted attempt as a suite PASS.
4. **Independent D may begin only after this C report-only PR is created and this report's remote blob readback is confirmed.** D should independently classify this attempt `BLOCKED / NOT_RERUN / HOLD_NO_MERGE`, absent new runtime proof. D must not reuse previous #93 as a post-C audit.

**Final decision:** `NOT_EXECUTED / BLOCKED_ENVIRONMENT / HOLD_NO_MERGE`. #90, #34, #37, #53, source, gates and `main` are not merged or modified. Formal/outcome access remains CLOSED.
