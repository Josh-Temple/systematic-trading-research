# Phase B Execution Readiness — 2026-09-28

Repository: `Josh-Temple/systematic-trading-research`  
Fresh-read main before this review: `8e164c2c51c47565d51b8417bc6323384a2419a8`  
Pilot: Autonomous Research Pilot v0.1  
Protocol: `ARP-B-v0.1`  
Status: `EXECUTION_BLOCKED_CLEAN_RESEARCHER_UNAVAILABLE`  
Scientific effect: NONE  
Market data: FORBIDDEN

## 1. Purpose

Record the exact Phase B execution boundary after the frozen AI researcher contract and run manifest were merged, so a later session does not mistake an execution-capability blocker for a scientific result or silently weaken the isolation boundary.

## 2. Verified repository state

At the main SHA above:

- Phase A remains `PASS_FOR_PHASE_B_SYNTHETIC_ONLY`.
- `ARP-B-v0.1` remains frozen before Phase B results.
- `RUN_MANIFEST_PHASE_B_AI_v0.1.json` is present and frozen before any official AI adaptive result.
- intended researcher identity is `OpenAI / GPT-5.6 Sol`.
- six world IDs, 16-submission / four-round budget, candidate-space reference, evaluator commit, and feedback schema are fixed in the manifest.
- the researcher-visible instruction is bound by SHA-256.
- the host-side AI search contract exposes only the protocol-permitted round packet and feedback fields.
- no official Phase B AI adaptive result exists.
- no Phase C / historical-market authorization exists.

## 3. Engineering verification

The merge that introduced the clean-researcher contract and run manifest is:

- `8e164c2c51c47565d51b8417bc6323384a2419a8`

The merged main workflow completed successfully.

The committed test suite includes checks that:

- researcher round packets exclude hidden seed, planted strategy, raw adaptive rows, raw final rows, and dataset hashes;
- four rounds and sixteen submissions are enforced;
- explicit stop does not reallocate unused budget;
- malformed researcher responses do not gain additional search budget;
- the frozen run-manifest instruction hash matches committed bytes;
- search budget and feedback schema drift are rejected;
- six world IDs must remain unique;
- existing Phase A / Phase B evaluator, baseline, ledger, and one-shot final tests still pass.

Observed result:

```text
Ran 70 tests
OK
```

This is engineering evidence only.

## 4. Why official AI execution is not started in this session

The current ChatGPT session has already read host-side Phase B generator code, including hidden-world construction logic.

Therefore this same session is not eligible to act as the official adaptive researcher under the frozen boundary.

Using it anyway would violate the intended separation between:

- host / evaluator knowledge; and
- researcher-visible information.

No adaptive metric has been exposed to an official AI researcher, so the run family remains uncontaminated.

## 5. Current external execution constraint

A clean external researcher process is required.

The preferred execution must satisfy all of the following:

- exact frozen researcher identity or a new run family before the first adaptive result;
- no repository access;
- no host-file access;
- no generator-code access;
- no hidden seed access;
- no raw adaptive/final outcome access;
- only the frozen round packet and permitted feedback;
- four rounds / sixteen submissions maximum;
- host-controlled final selection;
- one-shot final synthetic holdout.

At this review point, no connected execution path is available that can invoke the frozen `GPT-5.6 Sol` researcher under those restrictions without introducing a new credential/provider boundary.

This is an execution blocker, not a negative Phase B result.

## 6. GitHub-native inference check

GitHub Models is not an available fallback. GitHub's current documentation states that GitHub Models was fully retired on 2026-07-30, including its inference API.

GitHub Copilot separately supports GPT-5.6 Sol as an interactive Copilot model, but that is not the retired GitHub Models inference API and is not treated here as an already-authorized host-callable researcher endpoint.

Sources checked on 2026-09-28:

- https://docs.github.com/en/github-models
- https://docs.github.com/en/copilot/reference/ai-models/supported-models

No provider switch is made from this observation.

## 7. Safe next execution paths

Allowed next actions are limited to:

1. run the frozen researcher instruction in a genuinely clean external GPT-5.6 Sol session/process and exchange only host round packets / permitted feedback; or
2. before any AI adaptive result, establish a separately authorized model API execution path that preserves the same isolation boundary; or
3. if the actual model/provider/boundary must differ, create a new run-family manifest before observing adaptive feedback.

Do not:

- use this host-aware chat as the official researcher;
- expose generator code to the clean researcher;
- reveal hidden seeds before the relevant final evaluations;
- use historical market data;
- use DATA-HR-003;
- reinterpret this blocker as evidence against adaptive AI search;
- change `ARP-B-v0.1` after seeing adaptive results under the same run family.

## 8. Restart point

```text
Phase A = PASS_FOR_PHASE_B_SYNTHETIC_ONLY
Phase B protocol = FROZEN
AI RUN_MANIFEST = FROZEN_BEFORE_AI_RESULTS
host/researcher contract = CI VERIFIED
official AI adaptive result = NONE
scientific Phase B result = NONE
current blocker = CLEAN RESEARCHER EXECUTION PATH
market data = CLOSED
```

The next valid progress event is the first clean-researcher round under the frozen manifest, not additional strategy/protocol design.
