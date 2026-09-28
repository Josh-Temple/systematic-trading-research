# Phase B Official Run Status

Execution status: OFFICIAL_NON_AI_BASELINES_COMPLETED  
Protocol: ARP-B-v0.1 + ARP-B-v0.1.1-A1  
Scientific effect: NONE  
Market data used: NONE  
AI adaptive researcher: NOT RUN  
Phase C: NOT AUTHORIZED

## Official execution — 2026-09-29 (JST)

- Workflow: `Phase B official non-AI baselines` (`workflow_dispatch`, manual-only)
- Workflow run ID: `36440428881`
- Run URL: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36440428881
- Exact execution commit: `82a1731751396383cbf7b20d52b50b07c0b4643f`
- Branch: `main`
- Triggered: 2026-09-29 00:01 JST (GitHub Actions display)
- Completed: 2026-09-29 00:03 JST (artifact creation timestamps)
- Workflow conclusion: SUCCESS
- `official-baselines` job: SUCCESS
- Official workflow dispatch count at the pre-run check: 0; this run was dispatched once. No retry or re-run was performed.
- Metric-bearing result: GENERATED AND PERSISTED; its values and selected candidates were not inspected.

## Artifact metadata only

| Artifact ID | Name | Size (bytes) | Created (UTC) | Expires (UTC) |
| --- | --- | ---: | --- | --- |
| `10978375830` | `phase-b-host-state-36440428881` | 1,540 | 2026-09-28 15:03:04 | 2026-12-27 15:01:36 |
| `10978125983` | `phase-b-baseline-results-36440428881` | 4,423,946 | 2026-09-28 15:03:07 | 2026-12-27 15:01:36 |

Both artifact metadata records identify workflow run `36440428881`, branch `main`, and execution commit `82a1731751396383cbf7b20d52b50b07c0b4643f`. Neither artifact was opened or downloaded for this status update.

Safe commitment manifest identity: `commitments.json` emitted by the workflow; its `host_state_hash` is `8636d5a696987a12a5db76fdd696fa4ff7916d4d5eb2521fd13c56e5019bdf4d`. No raw world seed or checkpoint key is recorded here.

## Verification status

- PASS: workflow and the `official-baselines` job concluded successfully; test, baseline, commitment display, and both artifact upload steps succeeded.
- PASS: the frozen runner and workflow specify six synthetic worlds, 200 random-search repetitions per world, and one deterministic adaptive baseline per world.
- PASS: workflow and runner contain no market-data input; market data used = NONE. DATA-HR-003 and Horizontal Reaction H3 were not accessed in this execution.
- PASS: the workflow has no AI adaptive researcher step; AI adaptive researcher = NOT RUN.
- PASS: log inspection found the public commitment and completion markers, and found no raw seed value, checkpoint key value, baseline metric value, or selected candidate disclosed. A test name mentioning seed derivation appeared without a seed value.
- PASS: artifact existence and run linkage were checked using metadata only. Host-state and metric-bearing result contents were not inspected.

This records baseline execution, not a finding about market edge or a comparison of baseline performance. Keep the baseline results and host state outside the later clean AI researcher's input. Phase C remains NOT AUTHORIZED.
