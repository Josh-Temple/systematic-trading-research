# D — Independent post-C audit of CSM PR #100 (2026-10-10 JST)

## Independent decision

**BLOCKED / NOT_RERUN / HOLD_NO_MERGE** for the synthetic production-path signer-separation candidate. C's latest finalized remote report is [PR #100](https://github.com/Josh-Temple/systematic-trading-research/pull/100), which states **NOT_EXECUTED / BLOCKED_ENVIRONMENT**. **testsRun=0; compile=NOT_EXECUTED; unittest=NOT_EXECUTED; PASS/FAIL/ERROR/SKIP=NOT_OBSERVED**. These labels do not mean observed zero failures. No signer functional PASS, CSM integration acceptance, source qualification, I2 unlock, market-outcome access, or trading permission is established.

This **new independent post-C D** is separate from [old D #93](https://github.com/Josh-Temple/systematic-trading-research/pull/93), whose commit predates PR #100. Old C #95 and E #98 are historical hold evidence, **not** a post-#100 audit.

### Chronology / temporal independence

- C #100 report commit: **2026-10-10 08:56:33 JST** (GitHub committer date 2026-10-09 23:56:33 UTC); C PR creation: **2026-10-10 08:56:41 JST** (2026-10-09 23:56:41 UTC).
- Independent D fresh GitHub reads occurred **2026-10-10 about 20:00–20:03 JST**, **after** C #100's remote publication. Actual D execution of C's Python suite: **NOT_RERUN**.
- On the pre-write fresh listing, the newest PR was #100; no later C offline-execution PR appeared. A new C execution report subsequently published must be separately audited; this receipt cannot preapprove it.

## 1. Remote Git identities and readback (direct GitHub observation)

| Item | Exact directly read identity |
| --- | --- |
| Candidate [PR #90](https://github.com/Josh-Temple/systematic-trading-research/pull/90) | OPEN/DRAFT; base `work/csm-implementation-20261001`; head branch `work/csm-signature-separation-20261010-c`; **commit `94e7719839dcacf281d7d479c597222582f0d920`**; **tree `32e851594810e51a3aefd05ca7cdc17af341885d`** |
| C [PR #100](https://github.com/Josh-Temple/systematic-trading-research/pull/100) | OPEN/DRAFT; base `work/csm-signature-separation-20261010-c` at the #90 commit above; report head **`9d431397932f3ac5fcf781d912212af1cf11eda5`**; **post-C tree `22cc72f0b0ab912ddeb967f474e7397a89f5260f`** |
| C report (GitHub fetched full text) | `research/lines/currency-strength-momentum-v0.1/work/implementation/2026-10-10/exact-checkout-execution/C_EXACT_CHECKOUT_EXECUTION_RECEIPT.md` Git blob **`77ae8da0da43078b12c45e0359ae4ba6f326ffa4`** |
| Exact #90 `csm.py` | Git blob `cc3b788d637d0bacf63d9642788a196a1feaac56` |
| Exact #90 `test_csm.py` | Git blob `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282` |
| Exact #90 `fixtures/toy_cases.json` | Git blob `4e925eabb4d88772806f0e109c15680f17d73a31` (`SYNTHETIC`, no real market data) |
| Exact #90 `RUNBOOK.md` | Git blob `4168e0010060586e0301aa221ec653913ea721ea` |
| Exact #90 `config.json` | Git blob `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` |

**Complete diff and post-C identity control:** PR #90 changed exactly the candidate `csm.py`, `test_csm.py`, and C candidate report (3 files). PR #100 changed **only its C report file** (1 file). Direct GitHub comparison of commit #90 to #100 returned exactly **one added report file**, ahead=1, behind=0. Recursive Git tree responses were **not truncated** (#90: 219 entries; #100: 221 entries). All five code/test/fixture/config/runbook blob IDs listed above were **unchanged** between these two remote Git trees. The extra Git tree entries are consistent with a newly added report and its directory; no source-code change is evidenced by this C report.

**Target vs report distinction:** C executed **no suite** against target commit/tree `94e771... / 32e851...`. Its report commit/tree `9d4313... / 22cc72...` are later documentary identities and cannot be treated as a tested checkout. This D report is a separate subsequent report commit/tree, also **not** a candidate execution identity.

## 2. Environment evidence, not-run suite, and test definitions

**C's assertions, directly read from C's saved report (not independently witnessed C process logs):**

- Reported runtime: Python 3.13.5, Git 2.47.3.
- C reported `git ls-remote https://github.com/Josh-Temple/systematic-trading-research.git refs/heads/work/csm-signature-separation-20261010-c` terminated **exit 128** with **`Could not resolve host: github.com`**.
- C reported the expected local directory existed but **was not a Git work tree**; `git rev-parse --is-inside-work-tree` failed. No verified complete local exact checkout, `git rev-parse HEAD^{tree}`, local `git ls-tree`, or local blob identity could be established.
- Consequently C expressly did **not** run `python3 -m py_compile csm.py test_csm.py` or the metadata-bound `python3 -m unittest -v test_csm.py`. No start/end runtime timestamps, suite exit codes, positive/negative assertion outcomes, or genuine candidate test logs exist in the C report. **The exit 128 belongs to Git acquisition, not to Python tests.**

**D observation:** The full C report's remote Git blob and unchanged #90 source/test blob identities were fetched independently. D did **not** have a verified independently isolated complete #90 exact checkout and runtime metadata files; D therefore performed **NOT_RERUN** and makes no claim that it independently reproduced C's DNS error. No incomplete or reconstructed local tree was treated as a qualified environment.

**Static review of actual candidate source and tests (NOT_EXECUTED):**

- `_verify_signed_envelope` in exact #90 `csm.py` checks required role, revocation, trusted principal, signing key, issuance/expiry/key-validity windows, and signature verification.
- `validate_gate_receipt` verifies E and I separately and explicitly rejects identical key IDs, the same trusted `principal_id`, and equal RSA modulus values even if hex-encoded differently (lines ~608–650). This is a **static code-path assertion**, not observed validation behavior.
- Exact `test_csm.py` contains **62 `def test_` methods** by remote-text enumeration. Named **definitions** include independent E/I synthetic key acceptance, same-principal rejection with individually valid signatures, same modulus under distinct key IDs including hex alias, role swap/revocation/future-validity rejection, stale I2/E identity rejection, tampered E signature rejection, closed gate/no-access, partial E block, and source-lock raw-byte identity. These are **not 62 PASS** and not actual negative-test logs.
- Previously reported 56/56, 23/23 or another tree's Actions success is explicitly **not current #90 runtime evidence**. No unsafe workflow was manually dispatched.

## 3. Packet C metadata-only verification: remote, not runtime

Directly fetched the following **three metadata-only** files from [PR #35](https://github.com/Josh-Temple/systematic-trading-research/pull/35), exact HEAD `9870c710c3cba7bb9226c9eee8ec36687b96fd9d`. D independently recomputed SHA-256 on the GitHub connector's returned **UTF-8 text**, using an implementation that matched the published SHA-256(`abc`) test vector. These hashes matched RUNBOOK expectations:

| File | Git blob SHA-1 | Computed remote UTF-8 SHA-256 | Match |
| --- | --- | --- | --- |
| `source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` | YES |
| `probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` | YES |
| `expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` | YES |

**Crucial non-equivalence:** GitHub remote-content hashing does **not** establish that verified actual read-only metadata files were supplied inside an executable isolated #90 checkout. **Runtime-local SHA, runtime call-graph isolation and test-run integrity remain NOT_OBSERVED**. No live ECB/CSV/ZIP/OBS_VALUE, real FX prices, historical outcome, or trading files were accessed.

## 4. Earlier evidence and current HOLD scope

- Historical [D #93](https://github.com/Josh-Temple/systematic-trading-research/pull/93) was created **before** C #100. It cannot stand in for this audit and is not relabeled post-C.
- Earlier [C #95](https://github.com/Josh-Temple/systematic-trading-research/pull/95) also reports no exact checkout and no Python suite execution; [E #98](https://github.com/Josh-Temple/systematic-trading-research/pull/98) was an earlier HOLD, not a current C acceptance.
- Independently read the actual [I2 #37](https://github.com/Josh-Temple/systematic-trading-research/pull/37) `research/lines/currency-strength-momentum-v0.1/work/integration/gate.json` at #37 exact HEAD `9162cae4f2e64ee3da07517f12a16092cc170161`, blob **`19442215345b35b0db3910c01acd910a5d57889b`**: **`state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`**. This is direct **#37 snapshot evidence**, not a claim that a different unpublished integration-branch HEAD was checked.
- Even a later genuinely successful synthetic run would **not** certify separately provisioned E/I people, actual key custody, root-owned trust store, OS ACL/isolation, append-only durable attempts, restart/readback, complete point-in-time source history/revisions/calendar, current independent E/I signatures, named operator, human approval, economic validity, market outcome, or production trading.

## 5. Decision and downstream handoff

**D outcome: BLOCKED / NOT_RERUN / HOLD_NO_MERGE.** The C report has been independently read and audited *after* its publication; therefore D's **procedural completion** can be supplied to E, while **CSM technical/runtime acceptance fails**. Do not merge PR #90, #34, #37, #53, any C/D receipt, source, gate, or main. Do not enable market outcomes, formal cohort, XM/MT5, or trades. Preserve **HYP-CSM-002 UNTESTED** and I2 **BLOCKED/CLOSED**.

To lift this narrow environment blocker, a separately authorized C runner must obtain and prove a complete byte-exact #90 Git checkout; independently rehash the three actual metadata files inside a read-only isolated runtime; check that Python 3.12+ and import/test call paths cannot reach network, market history or subprocess/source acquisition; only then run unchanged py_compile and unittest -v and retain true stdout/stderr, test cases, timestamps, exits, counts and exact checkout identities. A later execution receipt needs a **new post-C D** review; never mutate #100 or this result into a PASS.

**Report-only change control:** This D branch started from exact #90 source commit; intended PR base `work/csm-signature-separation-20261010-c`. Only this one path under `work/independent-audit/2026-10-10/post-c100-runtime-independent/` may change. Draft, no merge, no workflow edits, source-lock/manifest/gate changes or result promotion. GitHub PR head/tree, report blob and complete changed filenames must be freshly read back after save.
