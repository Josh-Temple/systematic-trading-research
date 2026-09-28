# Phase B Official Run Status

Date: 2026-09-28  
Status: PREPARED_NOT_RUN  
Protocol: ARP-B-v0.1 + ARP-B-v0.1.1-A1  
Scientific effect: NONE  
Market data used: NONE

## Current state

The official non-AI Phase B baseline execution path is prepared but has not yet been run.

Prepared components:

- frozen parent protocol;
- pre-result seed-reveal amendment;
- synthetic world generator;
- host-controlled search accounting;
- random-search baseline;
- deterministic adaptive baseline;
- host-state / result artifact separation;
- manual-only GitHub Actions workflow.

## Official baseline scope

When explicitly started, the official batch will create six synthetic worlds:

- STABLE-01
- STABLE-02
- WEAKENING-01
- WEAKENING-02
- BREAK-01
- BREAK-02

Per world it will run:

- 200 random-search repetitions;
- 1 deterministic adaptive baseline.

Expected total method/world runs:

~~~text
6 × (200 + 1) = 1,206
~~~

Each method/world run uses the frozen 16-submission search budget and one final synthetic holdout evaluation.

## Pre-result information boundary

Before result generation the workflow creates:

- host_state.json containing raw world seeds and the HMAC checkpoint key;
- commitments.json containing only seed commitments and host-state hash.

The host-state artifact and baseline-result artifact are separate.

Workflow logs may expose:

- protocol/amendment IDs;
- world IDs/archetypes;
- seed commitments;
- host-state hash;
- run counts/status.

Workflow logs must not expose:

- raw world seeds;
- checkpoint key;
- adaptive metrics;
- final metrics;
- selected baseline candidates.

## AI contamination boundary

Under ARP-B-v0.1.1-A1, a later AI researcher must not receive:

- host-state artifact contents;
- baseline-result artifact contents;
- baseline metrics;
- baseline selected candidates.

The AI researcher may receive the frozen protocol, candidate space, world/archetype IDs, seed commitments, and only its own allowed adaptive feedback.

## Persistence boundary

GitHub Actions artifacts are operational persistence for this synthetic pilot.

They are not claimed to be:

- immutable archival storage;
- confidential from repository administrators;
- hardware-backed provenance.

Their purpose here is narrower: preserve complete run state/results while keeping them outside the researcher-visible input path.

## Launch condition

The official baseline workflow may be started only after:

1. the preparation changes are merged to main;
2. main CI for the merged preparation succeeds;
3. the workflow is invoked on that exact main revision;
4. no official Phase B adaptive result has yet been used to modify the frozen protocol.

After execution, this status record should be updated with:

- workflow run ID;
- exact commit;
- artifact IDs/names;
- safe commitment manifest;
- verification status;
- no metric values unless and until the AI adaptive researcher contamination boundary no longer applies.

## Current authorization

~~~text
OFFICIAL NON-AI BASELINE EXECUTION: PREPARED, NOT YET RUN
AI ADAPTIVE RESEARCHER: NOT YET RUN
PHASE C / MARKET DATA: NOT AUTHORIZED
~~~
