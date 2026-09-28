# Phase B Official AI Relay Preparation Status — 2026-09-29

Status: PREPARED_NOT_RUN  
Scientific effect: NONE  
Market data: FORBIDDEN  
Official AI adaptive result: NONE

## Purpose

Prepare the host-side execution boundary required to run the frozen Phase B AI researcher against the exact synthetic worlds already used by the completed official non-AI baselines.

This is an execution-layer change only. It does not alter:

- `ARP-B-v0.1`;
- candidate grammar;
- search budget;
- feedback schema;
- final-selection rule;
- model identity;
- world IDs;
- market-data authorization.

## Baseline host binding

The AI run family is bound, before any official AI adaptive result, to:

- baseline workflow run: `36440428881`;
- baseline execution commit: `82a1731751396383cbf7b20d52b50b07c0b4643f`;
- host-state artifact ID: `10978375830`;
- host-state artifact name: `phase-b-host-state-36440428881`;
- committed host-state hash: `8636d5a696987a12a5db76fdd696fa4ff7916d4d5eb2521fd13c56e5019bdf4d`.

The metric-bearing baseline result artifact is identified only so the host can explicitly treat it as forbidden researcher input. The official AI relay has no parameter for supplying that artifact and must not read it.

## Implementation boundary

`phase_b_official_ai_relay.py`:

1. validates the frozen Phase B protocol and AI run manifest;
2. validates the host binding;
3. requires the supplied host state to match the frozen SHA-256 commitment exactly;
4. requires `commitments.json` to exactly match the supplied host state;
5. reconstructs only the six frozen synthetic worlds;
6. exposes only the frozen researcher instruction and `phase_b_ai.make_round_packet()` output;
7. accepts strict-JSON researcher responses;
8. preserves the four-round / sixteen-submission host budget;
9. keeps ledgers, checkpoints, selected candidates, adaptive summaries, and final metrics in the private output path;
10. exposes only non-metric execution status in the public output path;
11. refuses to reuse an existing output root.

The CLI additionally requires:

- exact researcher model identity `GPT-5.6 Sol`;
- an operator attestation that the researcher is a clean external session with no repository, host-state, baseline-result, generator, hidden-seed, or market-data access.

## Feedback-schema correction

Pre-execution review found that `phase_b_ai.py` was adding `round` and `submission_index` to `prior_feedback`, although the frozen protocol permits only:

- `candidate_id`
- `validity_status`
- `duplicate`
- `adaptive_mean_return`
- `coarse_rejection_reason`

No official AI adaptive result had been produced.

The implementation is therefore corrected before first official AI use so researcher-visible feedback matches the already-frozen schema exactly. This is an implementation conformance repair, not a protocol amendment.

## Failure semantics

The official relay is fail-closed.

If execution halts after the output root is created:

- do not reuse that output root;
- do not silently restart the same official attempt;
- preserve the partial private ledger and public failure status;
- review the incident before authorizing another attempt.

A failure to execute is an operational result, not evidence about adaptive AI research performance.

## Clean researcher boundary

The official researcher must be a genuinely separate GPT-5.6 Sol session/process.

It may receive only:

- the frozen researcher instruction;
- BOOTSTRAP metadata produced by the relay;
- the current round packet;
- permitted feedback contained in later round packets.

It must not receive:

- this repository;
- generator code;
- `phase_b_core.py`;
- host state;
- raw seeds;
- checkpoint key;
- baseline result artifact;
- baseline metrics or selected candidates;
- raw adaptive/final rows;
- market data.

The host-aware session that prepared or operates the relay is not eligible to act as the researcher.

## Current restart point

```text
official non-AI baselines = COMPLETE
baseline metric artifact = SEALED FROM AI RESEARCHER
AI run manifest = FROZEN_BEFORE_AI_RESULTS
host binding = FROZEN_BEFORE_AI_RESULTS
official AI relay = PREPARED_NOT_RUN
official AI adaptive result = NONE
Phase C = NOT AUTHORIZED
market data = CLOSED
```

The next valid progress event is an official relay execution with a clean external GPT-5.6 Sol researcher, after the relay branch is CI-verified and merged.
