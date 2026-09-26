# Prior Repository Review — DVC reproducibility boundary

## Metadata

- Repository: `treeverse/dvc` — https://github.com/treeverse/dvc
- Review date: 2026-09-26 UTC
- Reviewed default branch state: `main` at `56e59829512ff134aa269099a2099587b810b4dd` (GitHub read); runtime verification uses released DVC `3.67.1`, not a build of that commit.
- Purpose: data and ML pipeline definitions, content tracking, cache, and experiment execution. This review evaluates ordinary `dvc repro`; experiment isolation is noted separately.
- Maturity: multi-year code and tests; the 2020 lockfile serialization test, 2023 removal of lockfile 1.0 support, and 2024 run-cache push/pull reversal document continuing changes ([commits](#20-sources-reviewed)).

## 1. What problem is this repository solving?

**FACT:** DVC defines stages in `dvc.yaml`, records dependency/output checksums in `dvc.lock`, and uses them to decide whether to run or restore a stage. It versions data outside Git with DVC cache and remotes. [Repro docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md), [file docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/dvc-files.md).

**INTERPRETATION:** This is a reproducible workflow system with conditional execution and storage, not an immutable snapshot of every byte the process observes.

## 2. Canonical source of truth

**FACT:** `dvc.yaml` supplies command, working directory, declared dependencies/parameters/outputs and frozen setting; `dvc.lock` serializes command, declared dependency/parameter and output state after a run. Git versions these files when users commit them; cache stores output content separately. [Serializer](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/serialize.py), [internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md).

**INTERPRETATION:** Definition, observed state and actual executed input set are different authorities. The generated lock entry can be internally consistent with the current workspace while historically false for the output.

## 3. Current repository structure

Relevant implementation: `dvc/stage/__init__.py` controls changed checks, run and save; `dvc/stage/serialize.py` writes pipeline/lock entries; `dvc/repo/reproduce.py` walks stages and writes lockfile. `tests/func/repro/test_repro.py` has frozen/reproduction tests. Docs reside in `treeverse/dvc.org`. [Stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py), [reproduce](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/repo/reproduce.py), [tests](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/tests/func/repro/test_repro.py).

## 4. Knowledge / data model

Entities are stages, declared deps/params/outs, workspace files, lock entries, output cache objects and optional run-cache entries. A lock entry holds paths, hash types/checksums, sizes and stage command, rather than an execution transaction, environment image or failure taxonomy. Local hashes may be MD5; cloud entries can use provider ETag/checksum and optional `version_id`; imported DVC repositories can carry `rev_lock`. These identifiers have different scopes. [Serializer](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/serialize.py), [DVC files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/dvc-files.md).

## 5. Research lifecycle

**FACT:** Users define and run stages, inspect status/results, and commit definitions/lock with Git if desired. Run cache can reuse results for matching declared inputs/params/commands under deterministic-command assumptions; `--no-run-cache` opts out. Queued/temp experiments use a copied workspace in `.dvc/tmp/exps` at queue time, with shared cache and stated untracked/gitignored caveats. [Repro](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md), [internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md), [experiments](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/experiment-management/running-experiments.md).

**LIMITATION:** This workflow does not itself encode hypothesis adjudication, scientific interpretation or current valid knowledge.

## 6. Experiment reproducibility

### Guarantee Matrix

Classification concerns the default `dvc repro` path and declared stage scope; STRONG does not mean end-to-end scientific reproducibility.

| Property | Assessment | Evidence and boundary |
| --- | --- | --- |
| Pipeline definition | **STRONG** | `dvc.yaml` specifies declared stage fields; lock records command and declared params/deps/outs. Git commit can version the definition. Undeclared process behavior is outside this model. [Serializer](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/serialize.py). |
| Code-at-start identity | **NOT GUARANTEED** | Declared `code.py` is hashed during `save_deps` after command. Independent concurrent edit produced output `1` while lock held edited-code MD5. Undeclared code is not captured. [Stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py); [reproduction below](#independent-reproduction). |
| Input-at-start identity | **NOT GUARANTEED** | The same timing applies to declared files; post-run hash need not represent the bytes read. A file might even change between several reads. Declaring all effective inputs is the user's responsibility. [Stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py); reproduction. |
| External / remote data identity | **PARTIAL** | DVC tracks declared external paths and remote provider hashes/version IDs where available; external outputs are not versioned by DVC. Mutable remote state, provider-specific ETags and unpinned accesses inside commands limit exact identity. No live remote race test here. [External docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/pipelines/external-dependencies-and-outputs.md), [DVC files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/dvc-files.md). |
| Environment identity | **NOT GUARANTEED** | Serialized stage fields do not contain a mandatory runtime/package/OS/container/hardware digest. Environment can be declared as extra inputs by users; DVC's lock alone does not prove it. [Serializer](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/serialize.py). |
| Output identity | **PARTIAL** | Declared output's post-run hash/size is recorded and content can be cached/restored. This identifies observed output bytes, but does not prove that those bytes arose from recorded inputs; unlisted outputs and nondeterminism escape. [Stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py), [internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md). |
| Recorded lineage correctness | **NOT GUARANTEED** | Independent #11058 reproduction shows output from old code paired with new code hash; independent #11004 reproduction shows a frozen output paired with a refreshed dep hash. [Details below](#independent-reproduction). |
| Concurrent modification | **NOT GUARANTEED** | `.dvc/tmp/lock` and `rwlock` coordinate DVC operations, but did not prevent an ordinary editor/process from altering a dependency mid-run in the test. [Internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md); reproduction. |
| Rerun semantics | **PARTIAL** | Changed checks and run cache can skip/restore; `--force` and `--no-run-cache` affect execution. A false lock association caused a subsequent `dvc repro` skip, independently observed. Run cache assumes deterministic commands. [Stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py), [repro docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md). |
| Failure recording | **PARTIAL** | Failure stops dependent execution by default; `--keep-going` and `--ignore-errors` alter continuation. Error/CLI status exists, but no first-class immutable failed-run manifest or scientific negative-result record was verified in this review. [Repro docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md). |

**FACT:** Current main calls `Stage.run` before `Stage.save`; `save_deps` obtains dependency state after execution. `Stage.changed` checks stage definition, deps and outputs; `Stage.reproduce(force=True)` bypasses unchanged skip. A frozen stage does not execute its command but can still reach save with force. [Stage source](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py).

**LIMITATION:** The local test is DVC 3.67.1 and a controlled file dependency; it does not establish all versions, every dependency backend or every experiment execution mode. A proposed pre-run hash patch would improve start-state reporting but cannot alone guarantee the exact bytes read later during a mutable run.

### Independent reproduction

**FACT — #11058, REPRODUCED:** In a new Git/DVC directory under `/tmp`, installed `dvc==3.67.1`; `code.py` sets `value = 1`, writes a `started` marker, waits for a `continue` marker, then writes `out.txt` from the in-memory value. Defined stage `dvc stage add -n concurrent -d code.py -o out.txt python code.py`. Ran `dvc repro` in background; after `started`, changed source to `value = 2`, created `continue`, waited for success. MD5 before edit: `bf2d8cb4b39287d8ca67c66c07cf6ce9`; after edit: `13f2406e1a75a3b4d9f16bf85602dfea`. `out.txt` was `1`; `dvc.lock` dependency MD5 was **after-edit** `13f2406e1a75a3b4d9f16bf85602dfea`. `dvc status` said “Data and pipelines are up to date”; second `dvc repro` said “Stage 'concurrent' didn't change, skipping”. This independently verifies the reporter's causal case, without relying on their assertion. Fixture is local scratch, not committed to the research repo.

**FACT — #11004, REPRODUCED:** In a separate fresh directory, stage copied `in.txt` (`one`) to `out.txt`; ran it and froze it. Changed `in.txt` to `two`, then ran `dvc repro -f`. Frozen command did not run: output remained `one`, output MD5 remained `5bbf5a52328e7439ae6e719dfe712200`; lock dep MD5 changed from `5bbf5a52328e7439ae6e719dfe712200` to `c193497a1a06b2c72230e6146ff47080`. DVC emitted a frozen warning. This confirms the main source path in the released version.

## 7. Negative / failed research

**FACT:** Repro errors are operational failures and affect continuation flags. No first-class searchable rejected hypothesis/null result was found in the reviewed lockfile/stage path. **LIMITATION:** Absence across the entire DVC ecosystem is not established; users can version arbitrary reports and metrics in Git/DVC. [Repro docs](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md).

## 8. Current knowledge vs history

**FACT:** Git revisions can preserve historical definitions and locks; workspace/current lock represents current pipeline state. **INTERPRETATION:** There is no built-in adjudicated status of “valid scientific knowledge” versus superseded interpretation in these primitives; Git history is history of artifacts, not evidence validation.

## 9. AI / agent role

No AI, agent or MCP integration was established as a DVC core guarantee in inspected paths. An agent invoking the CLI inherits the same stage, lock and cache boundaries; model reasoning is not encoded as proof of input/output causality. **LIMITATION:** This is scoped to core DVC and reviewed documentation.

## 10. Deterministic execution boundary

DVC runs user-defined commands and uses deterministic checksums/declared graph for invalidation. It does not make arbitrary commands deterministic. Its run cache assumes the same declared inputs and command yield the same result; use `--no-run-cache` when inappropriate. [Internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md), [repro](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md).

## 11. Human-facing interface

CLI (`stage add`, `repro`, `status`, `freeze`), YAML/lockfile and docs expose declared provenance and operational state. The independently observed “up to date” message can coexist with historically wrong causal association; users must inspect beyond headline status.

## 12. AI-facing retrieval

Structured YAML and Git history permit targeted retrieval of declared stages and revisions. No built-in MCP, semantic index or evidence-grade retrieval semantics were verified. This is a scope observation, not a claim that integrations cannot exist.

## 13. Issues / discussions findings

- [#11058](https://github.com/treeverse/dvc/issues/11058) is open; reporter demonstrated post-run dep hash mismatch in DVC 3.67.1. A commenter supported analysis and [#11062](https://github.com/treeverse/dvc/pull/11062) proposes pre-run dependency snapshot plus a regression test, but the PR is open/unmerged in this read. No maintainer acceptance or merged correction was established. Our separate runtime test confirms the bug's core behavior in 3.67.1; PR assertions and proposed test are not proof of a fix on main.
- [#11004](https://github.com/treeverse/dvc/issues/11004) is open. Maintainer `skshetry` [responded](https://github.com/treeverse/dvc/issues/11004#issuecomment-3964148502) that freeze should prevail even with force and observed longstanding behavior. [#11084](https://github.com/treeverse/dvc/pull/11084) is an open/unmerged proposed fix with a regression test and author-reported test results; it is not a current-main guarantee. We independently reproduced the mismatch in 3.67.1.

## 14. Commit-history findings

**FACT:** [2020 serialization tests](https://github.com/treeverse/dvc/commit/afc183f4e79ade8aa9d463cb14ffb6baa3504537) and [2023 lockfile 1.0 removal](https://github.com/treeverse/dvc/commit/3959c5137383c6ff3f8e71dc086460dee98d1f3f) show format/test evolution. [Run-cache push/pull default in May 2024](https://github.com/treeverse/dvc/commit/0a813bbcbcc96f80e2e2d0e262fc5dbbc559217f) was followed by [reversion to `--no-run-cache` default in July 2024](https://github.com/treeverse/dvc/commit/417e6d4b768393d4aa8694819122aab04c808966). **LIMITATION:** Commit titles establish changes, not undocumented motives or runtime safety across all versions.

## 15. Failure cases / abandoned approaches

The two reproduced cases are distinct: a moving input during normal execution and forced save of a frozen stage without executing. The 2024 run-cache default reversal is an observable policy change, not evidence that run caching as a whole was abandoned. No claim that proposed fixes are merged.

## 16. Strengths

Explicit declarative graph; inspectable lockfile with content metadata; output caching and restoration; versionable definitions/results; opt-out for run cache; separate experiment workspace mode. These controls are useful within their declared-input boundary and improve routine rerun discipline.

## 17. Limitations

No atomic capture of code/input bytes actually consumed in ordinary `repro`; incomplete coverage of undeclared dependencies and environment; provider-specific remote identifiers; output hashes do not prove causality; no scientific decision/negative-result model in inspected primitives. Local reproduction confirms two concrete lineage failures, but not their frequency in production or status in future releases.

## 18. Transferable lessons

| Classification | Lesson and reason |
| --- | --- |
| **STRONG_COMMON_PRINCIPLE** | Provenance artifact existence does not prove provenance correctness: two independent runtime tests paired recorded dep state with older output. |
| **STRONG_COMMON_PRINCIPLE** | Specify identity at definition, execution start/actual reads, and save separately; source call order and observed race make these observably different. |
| **PLAUSIBLE_PATTERN** | Snapshot isolated inputs and validate no mutation during execution, then tie output to immutable run ID; queued experiment copies offer a partial contrasting design, not a verified universal solution. |
| **PROJECT_SPECIFIC** | DVC's cache/checksum conventions and frozen/force semantics are tool-specific; translate guarantees, not file formats. |
| **DO_NOT_COPY** | Treat `dvc.lock` or an “up to date” status as proof that an output came from recorded code/data; both reproducers refute that inference. |

**INTERPRETATION:** These findings support the provisional distinctions among generated state, evidence correctness and computation correctness. No counterexample overturns a stated provisional principle. DVC's structured lock and cache do show that imperfect lineage can coexist with useful reproducibility controls, so principles should state scope rather than dismiss such controls wholesale.

## 19. Questions for cross-repository synthesis

How do other systems bind an immutable input snapshot to execution and post-run outputs? Can a concurrent mutation be detected without falsely claiming “bytes actually read”? How are remote objects/version IDs and environment images pinned? How are failed runs and negative scientific results retained independently of cache/status? Does a run-manifest system prove lineage, or merely serialize final state?

## 20. Sources reviewed

- Project fresh reads: [README](https://github.com/Josh-Temple/systematic-trading-research/blob/main/README.md), [ROADMAP](https://github.com/Josh-Temple/systematic-trading-research/blob/main/docs/ROADMAP.md), [RESEARCH_PRINCIPLES](https://github.com/Josh-Temple/systematic-trading-research/blob/main/docs/RESEARCH_PRINCIPLES.md), [prior-art README](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/README.md), [TEMPLATE](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/TEMPLATE.md), [WORK_QUEUE](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/WORK_QUEUE.md), [CANDIDATE_SCAN](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/CANDIDATE_SCAN.md), and all three completed reviews ([Trading Second Brain](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/trading-second-brain.md), [zestoles/quant](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/zestoles-quant.md), [Epsilon Quant Research](https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/prior-art/epsilon-quant-research.md)); current project main at start `4ceb5479f950c4534a16bfefa3dac9fa882cc927`.
- DVC pinned code: [stage](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/__init__.py), [serialization](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/stage/serialize.py), [reproduce](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/repo/reproduce.py), [dependency base](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/dvc/dependency/base.py), [functional tests](https://github.com/treeverse/dvc/blob/56e59829512ff134aa269099a2099587b810b4dd/tests/func/repro/test_repro.py).
- Official docs: [repro](https://github.com/treeverse/dvc.org/blob/main/content/docs/command-reference/repro.md), [internal files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/internal-files.md), [external dependencies/outputs](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/pipelines/external-dependencies-and-outputs.md), [DVC files](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/project-structure/dvc-files.md), [experiments](https://github.com/treeverse/dvc.org/blob/main/content/docs/user-guide/experiment-management/running-experiments.md).
- Issues, proposed patches and historical commits linked in sections 13–14. Reproducer observations are from isolated DVC 3.67.1 local runs described above, not upstream tests.

## Review status

**PARTIAL.** Central normal-run and frozen/force failures were independently reproduced and aligned with current-main code. Remote identity under live mutation, failure-record persistence and experiment mode under concurrent modification were not independently tested; proposed fixes remain unmerged in this read. No design decision is made here.
