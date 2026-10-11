# C — CSM exact-checkout and isolated runtime supply: operator-ready design (2026-10-12 JST)

## Decision and evidence class

**DESIGN_READY_FOR_OWNER_ASSIGNMENT / OWNER_NOT_ASSIGNED / BLOCKED_ENVIRONMENT / NOT_EXECUTED / HOLD_NO_MERGE.**

This is a **new supply and acceptance design**, not a new CSM runtime run, a software change, a supplied sandbox, an approved authorization, or a retrospective assertion that an earlier run passed. No Git clone/bundle download, metadata-file staging, runner creation, candidate execution, Actions dispatch, CI execution, source acquisition, or market-outcome access occurred in this C task. The prior C #100 `testsRun=0` means neither `py_compile` nor `unittest` ran; failure/error/skip remain **NOT_OBSERVED**, not zero observed failures. D #102 remains an independent audit of that blocked attempt, and E #104 retains HOLD.

The increment over #100/#102/#104 is an actionable **supply-chain, isolation, custody, named-role, proof, retry, and handoff contract** for a later separately approved environment. It resolves no supply or operational gate by itself.

### Fresh remote read identities, scoped to known safe artifacts

| Target | Freshly observed 2026-10-12 JST | Meaning / limitation |
|---|---|---|
| PR #90 | OPEN / Draft / not merged; source branch `work/csm-signature-separation-20261010-c`; commit `94e7719839dcacf281d7d479c597222582f0d920`; Git tree `32e851594810e51a3aefd05ca7cdc17af341885d` | **Exact candidate target**. Git commit/tree were freshly checked through repository Git metadata; **no local checkout** was established. |
| PR #35 | OPEN / Draft / not merged; head `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` | **Separate, metadata-only provenance target**. Three JSON file contents were **not fetched** in this C task. |
| PR #100 | OPEN / Draft / not merged; head `9d431397932f3ac5fcf781d912212af1cf11eda5`; report blob `77ae8da0da43078b12c45e0359ae4ba6f326ffa4` | Direct report readback: `BLOCKED_ENVIRONMENT / NOT_EXECUTED`, attempted Git acquisition DNS failure, no verified local exact checkout. |
| PR #102 | OPEN / Draft / not merged; head `119239ad86b20578fb9e7559abfd967cf7eeb97a`; report blob `7a4a1a124047396557c907419a43b5a92fb31399` | Direct report readback: independent post-#100 `BLOCKED / NOT_RERUN / HOLD_NO_MERGE`. |
| PR #104 | OPEN / Draft / not merged; head `f9b3510d6774664d2cb8617ee7e4faca1735a262`; report blob `e0ed357e6d6b08986baae0f3c1e7f682b4f0a833` | Direct report readback: previous E HOLD; no new E receipt implied. |
| PR #37 / I2 branch | `work/csm-integration-20261001` head `9162cae4f2e64ee3da07517f12a16092cc170161`; actual `gate.json` blob `19442215345b35b0db3910c01acd910a5d57889b` | Direct safe-gate read: `state=BLOCKED`, `gate_status=CLOSED`, `market_outcome_access=false`. This must remain unchanged. |
| Current `main` | `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` | Read-only reference; no CSM promotion. |

The changed-filename lists were freshly checked: #90 has exactly three candidate changes (`csm.py`, `test_csm.py`, candidate report), whereas #100, #102, #104 each add a report only. Earlier code/blob identities recorded in #100/#102/#104 remain pinned to the **unchanged** #90 head; they were not falsely described as runtime-local hashes.

The five required #90 **inherited** file identities, established in prior exact remote-tree reports, are:

| #90 `work/implementation/` path | Expected Git blob |
|---|---|
| `csm.py` | `cc3b788d637d0bacf63d9642788a196a1feaac56` |
| `test_csm.py` | `9e0ce5025d986f2e6f6e8c4487e4e0671dd67282` |
| `fixtures/toy_cases.json` | `4e925eabb4d88772806f0e109c15680f17d73a31` |
| `config.json` | `a1c1e140f8c0844fc554ae6fcd975bcb5e610770` |
| `RUNBOOK.md` | `4168e0010060586e0301aa221ec653913ea721ea` |

The exact #90 `RUNBOOK.md` was freshly read and still specifies Python >=3.12, standard library only, the three Packet C environment variables, and **synthetic** `py_compile` / `unittest` commands. Its explicit Python audit hook is **process-local, not a filesystem, network, or OS-level isolation guarantee**. The production `csm.py run` command in that runbook is **not authorized**. The 62 `test_` definitions reported by prior reviewers are *static definitions*, not an observed test count for the proposed runtime.

## 1. Scope and decision authority: no owner silently assigned

**No actual individual or service account has been nominated, authorized, or verified** for any supply function. Candidate *roles* below are operational proposals. They are not claims of commitment.

| Function | Proposed accountable role; present owner | Minimum permissions | Immutable evidence to deliver | Must not do |
|---|---|---|---|---|
| Authorization and release scope | Integrator / human research owner; **OWNER_NOT_ASSIGNED** | Approve the exact candidate SHA, provider, data-free fixture allowance, runner budget and stop policy | A numbered, time-limited, **operation-specific** human approval naming each person/account and permitted artifact path | Infer merge, source changes, production/outcome authorization from C-test permission |
| Exact-code supply | Repository custodian; **OWNER_NOT_ASSIGNED** | Private repo **contents:read** or previously verified complete Git bundle in a protected staging zone; no PR/write credential in runner | Authenticated Git remote/bundle origin, pinned #90 commit/tree, complete object integrity check, five Git blob identities, branch-ref recheck, independent artifact SHA-256 and supply receipt | Hand credentials, unrestricted Git history or forbidden files to a general-purpose model/runner |
| Packet C metadata custody | Independent source-material custodian; **OWNER_NOT_ASSIGNED** | Read **only three known PR #35 JSON paths** in privileged staging, no response.raw, observed values, history/ZIP or extra source acquisition | Three exact Git blob IDs, SHA-256 computed **inside the final runtime mount** on actual files, path/owner/mode, sealed chain of custody | Treat earlier GitHub text hashes as actual runtime bytes; expose raw content in model prompts or logs |
| Isolation implementation | Platform/security operator; **OWNER_NOT_ASSIGNED** | Provision a dedicated ephemeral offline runner, OS namespace/container/mount/ACL/process policy; administer an allowlisted evidence sink | Signed or change-controlled policy version, UID/GID, mounts, network/process/file **negative probes with denials**, environment image/version and artifact confinement | Use Python audit hooks alone, egress environment variables alone, or an unverified runner with unrestricted repo data access |
| Execution and evidence | Separate test operator; **OWNER_NOT_ASSIGNED** | One-shot invocation of **unchanged** `py_compile` and `unittest` within approved runner; append-only run receipt | Run ID, exact argv/environment variable **names and safe local paths**, Python version, local HEAD/tree/blobs, metadata SHA-256, start/end time, commands/exit codes, full securely held stdout/stderr, test counts and named results | Run `csm.py run`, inspect market outcomes, overwrite old receipt, self-approve acceptance |
| Independent post-C acceptance | D auditor not acting as supplier/executor; **OWNER_NOT_ASSIGNED** | Read-only access to *screened* receipt, manifests, authorized exact code, denial evidence and safe logs | Independent consistency verdict, recheck of code and metadata identities, failure/retry classification and remaining gaps | Count #102 as an audit of a **future** C run or treat synthetic PASS as production credential/market access assurance |
| Durable evidence custody | Security/research operations custodian, independent of executor; **OWNER_NOT_ASSIGNED** | Write-once or append-only protected receipt/manifest store with independent read permission | Clock/source, audit-chain reference, tamper/replay protection, retention/ACL policy, after-write and restart readback | Accept a local temp directory or GitHub report alone as a durable execution ledger |

**Separation of duties:** the holder of repo/private metadata access should not be the CSM Python process identity; the executor should not own the policy or audit retention; D must not be the same actor authoring the C execution receipt. If one staff member must assume two roles, document the specific conflict and obtain an independent compensating approval **before** execution. No real production private keys are needed for these synthetic tests.

## 2. Provisioning route and complete-checkout acceptance

### Route A — preferred, if authorized: authenticated Git acquisition in an isolated custodian staging domain

1. A named repo custodian obtains the **entire authenticated Git checkout** of precisely #90 via an approved private endpoint **outside** this Chat and outside any model-accessible environment. Pin the commit, not a mutable branch name. The previous #100 attempt could not resolve `github.com`; do not claim the same route works now. A repository service account needs only minimum read permissions in the **staging** domain. Never pass its token to the test process.
2. Record origin, transport/security context, exact `HEAD`, `HEAD^{tree}`, parent, full tree validation and the relevant five blob IDs **from the genuine Git object database**. Check a branch-move race immediately before supply. Require a normal checkout of the **complete target commit**, not a hand-created directory of five files, ad-hoc copied GitHub snippets, or a changed `csm.py`.
3. Authenticate the transferred artifact with an independently recorded SHA-256 manifest and trusted delivery channel, signed/approved by a separate custodian as appropriate. Git object IDs establish repository object identity but, on their own, do not authenticate the *supply actor*, workspace permissions, or exported artifact bytes.
4. Important possible conflict: a **complete repository checkout or its `.git` history may contain data outside the CSM allowlist**. The staging custodian must inspect a metadata-only **path inventory**, without opening prohibited contents in the model, and attest that **no forbidden raw/history/outcome bytes or credential-bearing files will be readable by the subsequent Python identity**. If such denial cannot be technically enforced, **NO_EXECUTION** even when commit/tree hashes match.
5. The custodian records complete-checkout verification in a privileged staging phase; the platform mounts the **same verified source objects** read-only with an OS-enforced per-path execution allowlist and no readable credential or unrestricted `.git` history in the unprivileged Python phase. Do not misstate a selectively reconstructed tree as a locally complete checkout: preserve verifiable original Git provenance and a custody link between the staged complete checkout and every exposed file.

### Route B — authorized offline fallback: complete Git bundle + custody manifest

A named repo custodian produces a **self-contained** Git bundle at the exact authorized commit, checks completeness and `git bundle verify` plus object/tree/blob identity in a privileged environment, and transfers it by an authenticated, checksum-verified offline channel to the security operator. The operator establishes a **real full checkout** from the verified bundle within controlled staging, then applies Route A's execution-access restrictions. `git bundle verify` alone does not establish bundle completeness for the task, source authority, current branch ref, or allowed data boundary: all must be checked separately. **Do not transmit a bundle containing other forbidden Git history to the model-accessible domain.** If a truly safe full bundle cannot be created without exposing prohibited history to the intended execution identity, mark this route **NOT_FEASIBLE** until a security owner approves a stronger staging/execution split.

### Rejected substitutes

- A tar/zip of selected GitHub files, an arbitrary commit archive without its genuine Git identity proof, a fabricated `.git` directory, or a manually reconstructed partial checkout is **not** the required complete exact-checkout evidence.
- A successful GitHub connector read, PR status, Git tree API listing, previous remote SHA-256 result, `git ls-remote` alone, or `[skip ci]` is **not** an executable local checkout.
- An unreviewed GitHub Actions workflow is **not** an approved offline substitute; historical `csm-source-readiness` has a source/history-acquisition risk. This Wave must not change or dispatch workflows.

## 3. Exact verification contract before any future suite command

### C-0: evidence obtained outside the Python test identity

In the privileged verified staging checkout, collect *actual process stdout/stderr/exit*, not example command text, for the following **planned** checks. They are **NOT_EXECUTED in this task**:

```sh
# Illustrative command shapes only; do not run without separately approved sandbox.
git rev-parse --verify HEAD
git rev-parse HEAD^{tree}
git ls-tree -r --full-tree HEAD    # full listing kept in protected staging, NOT model input
git ls-tree HEAD research/lines/currency-strength-momentum-v0.1/work/implementation/
git cat-file -t 94e7719839dcacf281d7d479c597222582f0d920
git fsck --full                  # custodian-only: never expose object contents to model
```

**Acceptance:** `HEAD=94e7719839dcacf281d7d479c597222582f0d920`, `HEAD^{tree}=32e851594810e51a3aefd05ca7cdc17af341885d`, five file-path Git blobs exactly equal the table above, clean checkout/index, no unapproved modifications, no incomplete object set, signed custody manifest matches supplied bytes. Verify also that the upstream #90 PR still points to this exact SHA; if it moves, **STOP**, create a *new target authorization* and independent evidence. Verify the 3 Packet C identities from #35 **as a separate provenance chain**; do not cherry-pick #35 or silently amend #90.

### C-1: final sandbox preflight and *runtime-local* file verification

| Test | Concrete observed requirement | Fail condition |
|---|---|---|
| Python | In-runner executable reports Python >=3.12, fixed interpreter/stdlib, no packages installed; exact image/digest pinned | Version, interpreter image or module imports diverge |
| Five target files | Read-only bind mounts from the same attested #90 checkout; source/test/fixture/config/runbook Git blob inventory reconciles to C-0 | Any path maps to edited, substituted, symlink-escaped or unattested bytes |
| Three Packet C JSON **actual files** | Under a dedicated read-only metadata mount, separate from code; recompute local raw-byte SHA-256 via trusted hash utility from **the paths Python will use**; record the file's metadata, owner, mode, inode/mount and provenance | Missing/symlink/substituted file; mismatch; hashes derived from connector text instead of runtime bytes |
| File boundary | Python UID sees only approved code, toy cases, the three metadata JSONs, runtime standard library and isolated scratch; deny actual source/response, observed ECB value, history/ZIP, tick/prices, market outcomes, credentials, and arbitrary checkout history | Any direct, symlink, relative path or inherited-handle read of forbidden assets succeeds |
| Network boundary | OS-level deny for network/socket/egress and alternative connectors, not just DNS failure, a Python hook, or an env var; no token/cached data injected | Outbound or alternate-transport test succeeds, or cannot be tested independently |
| Process boundary | No child process, shell, arbitrary interpreter/import extensions, or other process outside allowlist; independently checked by a harmless synthetic denial probe | Child/privileged process starts, imports or call graph access uncontrolled paths |
| Storage / logs | Worktree read-only; all incidental `__pycache__`, tempfile and test outputs directed to isolated scratch; receipt sink protected and append-only with restart readback | Mutable source, residual secret, unbounded log exposure, or writable/overwritable run receipt |
| Test call graph | Static review of actual exact `csm.py`, `test_csm.py`, fixtures, config and imports before invocation; review for runtime imports, subprocess, filesystem/network open and dynamic execution | Unreviewed invocation or any resolved forbidden path, including import-time |
| Gate | Fresh approved safe `gate.json` check remains `BLOCKED/CLOSED/false`; suite uses **only synthetic** artifacts and no gate promotion | Any state transition toward open/market-outcome, even if tests are passing |

**Local raw-byte hash expectations, not newly observed in this task:**

| PR #35 `work/source-qualification/` artifact | Git blob from prior remote checks | Required SHA-256 computed inside final runtime |
|---|---|---|
| `source-lock.json` | `81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf` | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| `probe-metadata.json` | `21aa9149b7b7db9b07f1aa3f4bf0312675a166bd` | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| `expected-calendar.json` | `6ed720353472ba6f35391936c536d46fb6ae8c66` | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |

A separate independent operator must verify the sandbox policy version and denial-probe receipts; passing in-process Python audits alone is insufficient. The preflight must protect the **run** as well as the operator's command shell: OS confinement must remain in force during imports, tests, any threaded activity, and the evidence-writing path.

### C-2: narrowly authorized synthetic suite, only after *all* above are PASS

Planned unchanged commands from #90 RUNBOOK; **not executed here** and **not authorized by this design**:

```sh
# Execute from the verified work/implementation directory, inside the policy-bound runner.
python3 -m py_compile csm.py test_csm.py

CSM_PACKET_C_SOURCE_LOCK=/verified/metadata-only/source-lock.json \
CSM_PACKET_C_PROBE_METADATA=/verified/metadata-only/probe-metadata.json \
CSM_PACKET_C_EXPECTED_CALENDAR=/verified/metadata-only/expected-calendar.json \
  python3 -m unittest -v test_csm.py
```

Only **three frozen, read-only metadata inputs** are allowed from Packet C. The test may generate strictly synthetic rows itself. No `python3 csm.py run`, real ECB `OBS_VALUE`, real market data or history, additional source API, trade/execution tool, XM/MT5, paper/live market result, new dependency, network access, or CI. **Never alter the candidate source/test/config/fixtures to force a passing result.**

The prior `test_csm.py` statically had 62 test-method definitions. A real test-run count must be parsed from the new process output; a difference from the expected scope triggers investigation, **not** fabricated 62/62 PASS.

## 4. Evidence, stop/retry states, and independent D handoff

**Receipt fields required for each attempted run:** `run_id`; requester/approver/custodian/operator identities; approval ID and expiration; Git repo + verified candidate HEAD/tree and each safe target blob; separate #35 HEAD + three blob hashes and actual local SHA-256; signed provisioning manifest / immutable artifact digest; image and Python version; mount/ACL/seccomp/egress policy revision; import-call-graph reviewer; C-0 and C-1 probe IDs + deny results; frozen gate head/blob/status; argv + approved variable **names and paths only**; UTC start/end; exit codes for compile and unittest; observed testsRun/failures/errors/skips; named positive/negative test outcomes; full unmodified stdout/stderr stored **only in an approved screened, durable store**; output hashes and append-only storage receipt + post-restart readback; reviewer/date; and exact candidate vs report-commit separation. For model-facing summaries, permitlist fields and sanitize logs **before model ingestion**. Do not display raw forbidden artifacts or credentials in a PR, Chat, Actions log or remote result.

**State transitions for the future operation:**

1. `SUPPLY_PENDING` — all owners or authorizations missing; **no acquisition and no test**.
2. `C0_VERIFIED` — genuine complete checkout, pinned Git identities, custodian provenance, checked forbidden-history boundary. Failure => `BLOCKED_SUPPLY`; retain evidence.
3. `C1_VERIFIED` — actual metadata-local hashes, OS-level denials and allowed file graph, Python, gate, independent preflight. Failure => `BLOCKED_ISOLATION`, **never run**.
4. `C2_ATTEMPTED` — record before invocation, then execute approved synthetic commands at most once for a unique `run_id`; capture full exit/status. Test failure => `TEST_FAILED`, **no silent repair**.
5. `C_RECEIPT_DURABLE` — custody receipt saved and read back with its own identity. If durable write or readback fails => `EVIDENCE_UNVERIFIED`, not `PASS`.
6. `INDEPENDENT_D_PENDING` — after an authentic C execution report exists and readback completes, a separate D auditor evaluates exact same run and candidate. This does **not** open I2.

A retry requires a **new human-approved attempt ID**, a fresh upstream-HEAD check, new local metadata rehash, new denial probes, and an append-only linked receipt. Do not overwrite #100/#102/#104 or reuse their evidence as a new test. A stale HEAD, unequal file, unresolved identity, missing owner, untrusted bundle, any forbidden read/network/process success, test process crash, missing counters, unfiltered logs, or uncertain evidence custody is a **STOP/HOLD**, never a PASS.

### Explicit acceptance levels

| Level | This C task | Later narrowly approvable proof |
|---|---|---|
| Supply owner authorization | **OWNER_NOT_ASSIGNED** | Human-named accountable owner and independent supplier/security/operator/D with capability and expiry |
| Genuine full #90 checkout | **NOT_SUPPLIED / NOT_VERIFIED_LOCALLY** | Attested full object set, exact local HEAD/tree/five blobs, safe execution-domain link |
| Isolated Python >=3.12 runner | **NOT_PROVISIONED / NOT_VERIFIED** | OS-denied network/files/processes, negative probes, read-only code and metadata, fixed runtime |
| Three local Packet C SHA-256 | **NOT_VERIFIED_LOCALLY** | Actual three runtime-byte hashes match expected pinned values |
| Unchanged synthetic compile/test | **NOT_EXECUTED** | Full real process/exit/log counts and named positive/negative cases |
| Independent post-execution D | **NOT_STARTED** | Separate D after genuine C receipt publication; old #102 not reused |
| CSM research, integration, outcome, trading | **HOLD_NO_MERGE / I2 CLOSED / HYP-CSM-002 UNTESTED** | This Wave cannot lift these gates even with hypothetical synthetic success |

## 5. Minimum distinct human approvals / supplier decisions for E

1. **Appoint and authorize the supply owner and Git custodian**, exact #90 SHA/tree, permitted authenticated read-only repo route or complete offline bundle, acceptable protected artifact transport, retention, no model access to unchecked Git contents. Define what to do if full checkout and forbidden-file denial cannot coexist.
2. **Appoint separate Packet C metadata custodian** with permission scoped to exactly the three PR #35 JSON files, verified custody to readonly runtime mount, and no permission to fetch forbidden real/source/history bytes.
3. **Authorize a named platform/security operator to provision and verify a specific offline sandbox**, OS-level file/process/network denial and a protected durable logging service; approve negative probes and their allowlisted test payloads (synthetic only).
4. **Only after C-0/C-1 independent pass**, explicitly authorize **one execution of the unchanged #90 `py_compile` and `unittest -v`**, actual receipt retention and independent review. Do not infer this authorization from the previous design approval.
5. **Nominate independent D** to inspect the new C receipt and evidence; retain separate later decisions on production keys, source qualification, I2 outcome access, candidate merge and real market execution. These are not part of C's proposed permission.

**Terminal C judgment: `DESIGN_READY_FOR_OWNER_ASSIGNMENT / OWNER_NOT_ASSIGNED / BLOCKED_ENVIRONMENT / NOT_EXECUTED / HOLD_NO_MERGE`.** No new runtime capability was demonstrated, and no real data, metadata input content, market outcome, production key, GitHub workflow, or source/gate state was changed. This report is for E's owner/approval routing only; candidate PR #90 and earlier C/D/E reports remain unchanged.
