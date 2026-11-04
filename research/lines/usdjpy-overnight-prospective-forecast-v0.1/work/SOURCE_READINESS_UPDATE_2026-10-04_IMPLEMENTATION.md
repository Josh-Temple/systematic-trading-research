---
type: SourceReadinessUpdate
research_line_id: RL-USDJPY-OVERNIGHT-001
created_at: 2026-10-04
status: PARTIAL_BLOCKED
scientific_effect: NONE
market_outcome_access: CLOSED
---

# Source/readiness update — deterministic core implemented

## What changed

The deterministic pre-outcome helper layer is now implemented at:

- `work/implementation/forecast_core.py`
- `work/implementation/test_forecast_core.py`
- `work/implementation/TEST_LOG_2026-10-04.txt`

Synthetic execution result:

- 19 tests PASS;
- no market data used by the tests;
- no scientific outcome calculated.

Covered mechanics include:

- timezone-aware Bid/Ask validation;
- midpoint calculation;
- Monday–Thursday overnight window;
- Sunday weekly cutoff / Monday start / Friday end;
- 60-second quote tolerance;
- exact-zero return semantics;
- probability bounds;
- Brier score;
- absolute-error calculation;
- future-information rejection;
- pre-cutoff knowledge of future scheduled events;
- canonical JSON SHA-256.

## Remaining gates

Formal scored operation remains BLOCKED by:

1. reference USD/JPY Bid/Ask source sample / endpoint qualification;
2. frozen mandatory input set;
3. durable point-in-time news snapshot contract;
4. prompt / source-set identity freeze;
5. append-only event receipt wiring around the deterministic helpers;
6. explicit human freeze of the scientific specification.

## Dukascopy retrieval attempt

The current chat/container runtime could confirm Dukascopy documentation and source semantics on the public web, including:

- JForex `IHistory.getTicks(...)`;
- historical data access;
- Bid/Ask tick semantics;
- documented `.bi5` tick encoding.

However, the runtime could not resolve the binary `datafeed.dukascopy.com` host for a bounded source sample.

This is classified as:

`EXECUTION_ENVIRONMENT_SOURCE_RETRIEVAL_BLOCKED`

It is **not**:

- evidence that Dukascopy is scientifically unsuitable;
- a negative market result;
- permission to substitute Monex/Bloomberg/another feed after outcomes.

Fresh inspection of the existing `research/fx-daily-breakout-20261003` branch found no durable raw Dukascopy sample. Its own data contract likewise leaves source acceptance unresolved.

## Current readiness

`PARTIAL_BLOCKED`

The code portion of the readiness gate advanced.

The source identity gate did not.
