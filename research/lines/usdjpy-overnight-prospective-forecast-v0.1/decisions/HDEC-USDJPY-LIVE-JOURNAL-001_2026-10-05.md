---
type: HumanDecision
decision_id: HDEC-USDJPY-LIVE-JOURNAL-001
research_line_id: RL-USDJPY-OVERNIGHT-001
decided_at: 2026-10-05
status: ACCEPTED
scientific_effect: NONE
---

# Human decision — activate Live Market State Journal v0.1

## Decision

The user requested that, separately from frozen validation, the project should repeatedly inspect the changing market situation and preserve those observations.

This decision authorizes an append-only observational stream for USD/JPY.

## Authorized design

- fixed default observation checkpoints: 08:30, 15:00, 21:30 JST;
- additional EVENT_DRIVEN and MANUAL observations;
- separation of facts, interpretation, change-since-prior, scenarios, and confidence;
- append-only corrections;
- use for research context and challenger generation.

## Boundary

This decision does **not**:

- freeze the overnight or weekly scientific specification;
- open market-outcome access for those scored protocols;
- make journal entries confirmatory evidence;
- authorize broker trading.

The Live Market State Journal is active independently of the scored-forecast readiness gates.
