# Phase B Protocol Amendment v0.1.1 — Seed Reveal Timing

Date: 2026-09-28  
Status: FROZEN_BEFORE_OFFICIAL_PHASE_B_RESULTS  
Amendment ID: ARP-B-v0.1.1-A1  
Parent protocol: ARP-B-v0.1

## Reason

The parent protocol states that a hidden world seed may be revealed after final synthetic holdout evaluation.

Before any official Phase B benchmark result was produced, a cross-method contamination risk was identified:

- random and deterministic baselines may finish before the AI researcher;
- revealing the world seed after the first method's final evaluation would make the later AI run reconstructable from public state if the seed became visible;
- the comparison is cleaner if all planned methods use the same committed world while the seed remains unavailable to the researcher.

## Amendment

For each Phase B world, the hidden world seed MUST NOT be revealed until **all planned methods for that world are complete**.

The planned methods for v0.1 are:

1. random-search baseline distribution;
2. deterministic adaptive baseline;
3. AI adaptive researcher.

A method is complete only after its final synthetic holdout result and required ledger/checkpoint have been persisted successfully.

If the AI adaptive researcher is abandoned, the seed may be revealed only after an explicit run-family closure record states that the AI method will not be executed.

## Host-state persistence

Before baseline execution, the host may persist the raw world seeds and checkpoint key in a separate workflow artifact or equivalent host-controlled store.

That artifact:

- is not part of researcher-visible input;
- must not be read by the AI researcher;
- must be identified by a hash/commitment in the public run manifest;
- is operational persistence, not claimed immutable or confidential against repository administrators.

The AI researcher may receive:

- world_id;
- archetype;
- seed commitment;
- protocol/evaluator identities;
- allowed adaptive feedback.

It may not receive:

- seed bytes;
- host-state artifact contents;
- baseline adaptive/final metrics;
- baseline selected candidates.

## Result visibility

Baseline result artifacts may be persisted before the AI run, but their metric-bearing contents MUST NOT be supplied to the AI researcher or included in its prompt/context.

Workflow success/failure status and non-result metadata may be observed by the orchestrator.

## Other protocol terms

All other terms of ARP-B-v0.1 remain unchanged.

This amendment was frozen before official Phase B baseline results were generated.
