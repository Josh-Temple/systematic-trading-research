# WORK Instruction — Phase B Official AI Adaptive Run

Repository: `Josh-Temple/systematic-trading-research`

Purpose: execute the frozen Phase B AI adaptive method against the exact six synthetic worlds used by official non-AI baseline run `36440428881`, without exposing host secrets or baseline results to the clean researcher.

This is synthetic-only. Do not access Horizontal Reaction H3, DATA-HR-003, or any market data.

## 1. Fresh-read preflight

Before any execution, fresh read:

- current `main` SHA;
- `PHASE_B_PROTOCOL_v0.1.md`;
- `PHASE_B_PROTOCOL_AMENDMENT_v0.1.1.md`;
- `RUN_MANIFEST_PHASE_B_AI_v0.1.json`;
- `PHASE_B_AI_HOST_BINDING_v0.1.json`;
- `PHASE_B_AI_RELAY_PREP_STATUS_2026-09-29.md`;
- `PHASE_B_OFFICIAL_RUN_STATUS.md`;
- `phase_b_official_ai_relay.py`.

Expected preparation merge at creation of this runbook:

`bc5dc61445291b83ac0c2bb782d9cd131ef32183`

If current `main` differs, review the diff before execution. Do not assume a newer revision is equivalent.

Confirm:

- official non-AI baseline run `36440428881` remains completed successfully;
- official AI adaptive result is still NONE;
- run family remains `ARP-B-AI-v0.1-2026-09-28`;
- model identity remains `OpenAI / GPT-5.6 Sol`;
- candidate grammar, budget, feedback schema, final selection, world IDs, and market-data prohibition are unchanged.

## 2. Retrieve host-state artifact only

From official baseline workflow run `36440428881`, retrieve only:

`phase-b-host-state-36440428881`

Expected artifact metadata:

- artifact ID: `10978375830`;
- digest: `sha256:bd4c6f3152dc9ade13cb9f8eaa742d249176bcebfc2fc7089717db9c3f1b6e3b`.

Extract its:

- `host_state.json`;
- `commitments.json`.

Do not retrieve, open, inspect, summarize, or pass to another model:

`phase-b-baseline-results-36440428881`

Expected forbidden result artifact ID: `10978125983`.

Do not print or paste the contents of `host_state.json` into chat, logs, Slack, GitHub, or researcher-visible files.

## 3. Prepare a genuinely clean researcher

The researcher must be a separate GPT-5.6 Sol session/process with:

- no repository access;
- no Project context;
- no host filesystem access;
- no connected GitHub/Drive/Slack or similar tools;
- no generator code;
- no hidden seed;
- no host-state artifact;
- no baseline-result artifact;
- no baseline metrics or selected candidates;
- no market data;
- no previous Phase B host discussion in its conversation context.

Do not use the host-aware WORK session as the researcher.

Provide the clean researcher only:

1. exact contents of `PHASE_B_AI_RESEARCHER_INSTRUCTION_v0.1.md`;
2. the relay-generated BOOTSTRAP metadata;
3. one relay-generated round packet at a time.

The clean researcher must return one JSON object only for each round.

## 4. Start the host relay

Run from:

`research/pilots/autonomous-research-v0.1`

Use a new, previously nonexistent output directory.

Example:

```bash
python phase_b_official_ai_relay.py \
  --host-state /secure/path/host_state.json \
  --commitments /secure/path/commitments.json \
  --output-root /secure/path/phase_b_ai_official_run \
  --researcher-model "GPT-5.6 Sol" \
  --confirm-clean-boundary
```

Do not redirect private output into repository paths or public logs.

The relay must validate the frozen host-state SHA-256 before emitting the first researcher-visible packet.

Expected bound host-state hash:

`8636d5a696987a12a5db76fdd696fa4ff7916d4d5eb2521fd13c56e5019bdf4d`

If validation fails, stop. Do not substitute another seed, world, artifact, or run.

## 5. Round exchange

For each emitted `ROUND_PACKET_READY`:

1. copy only the packet JSON to the clean researcher;
2. receive one JSON response;
3. paste only that response into the host relay;
4. terminate the pasted response with the literal line:
   `END_RESPONSE`.

Do not edit the candidate proposals unless the response is syntactically corrupted in transport. If transport corruption occurs, stop rather than silently reconstructing scientific content.

The researcher-visible feedback must contain only the frozen fields:

- `candidate_id`;
- `validity_status`;
- `duplicate`;
- `adaptive_mean_return`;
- `coarse_rejection_reason`.

Do not provide extra diagnostics, raw outcomes, dataset hashes, final outcomes, baseline information, or host metadata.

## 6. Completion and private outputs

The official method covers all six frozen worlds.

A normal completion status is:

`COMPLETE_PENDING_COMPARISON`

The private output contains metric-bearing AI summaries and ledgers. Do not expose those contents to the clean researcher.

The public session status may be read and recorded because it contains execution metadata without metric values.

Do not compare baseline versus AI performance until all six AI world runs complete and the private outputs are durably preserved.

## 7. Failure semantics

The relay is fail-closed.

If it halts after creating the output root:

- preserve the output root;
- do not reuse it;
- do not silently restart;
- do not create extra submissions;
- do not repeat a final holdout evaluation;
- do not alter protocol or candidate rules;
- record an incident before deciding whether a new official attempt or new run family is permitted.

A failed execution is an operational result, not a negative scientific result.

## 8. Post-run repository record

After a normal completion, update the repository with metadata only.

Record:

- exact main SHA used;
- run family ID;
- execution date/time;
- execution status;
- six-world completion status;
- private output identity/hash if available;
- ledger verification status;
- clean-researcher model/boundary attestation;
- baseline results read = NO during researcher execution;
- market data used = NONE;
- Phase C = NOT AUTHORIZED.

Do not commit or quote:

- adaptive metric values;
- final metric values;
- baseline metric values;
- selected candidates;
- seeds;
- checkpoint keys;
- private ledgers.

Create a PR for the metadata-only execution record, verify CI, and merge if clean.

## 9. Stop condition

Stop immediately if any of the following occurs:

- the clean researcher gains repository/host/baseline access;
- wrong model identity is used;
- host-state commitment does not match;
- baseline-result artifact is opened before researcher completion;
- researcher-visible packet includes fields outside the frozen contract;
- an existing output root would be reused;
- market data or DATA-HR-003 is accessed;
- protocol or budget drift is detected.

Do not rescue the run by changing conditions after observing adaptive feedback.
