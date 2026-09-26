---
id: SPEC-HR-001-v01
type: Specification
research_line_id: RL-HR-001
version: v0.1
created_at: 2026-09-11
frozen_at: 2026-09-11
freeze_status: FROZEN
tests_hypothesis: HYP-HR-001
data_roles_allowed:
  - UNUSED_EVALUATION_AT_FREEZE
outcome_definition: expectancy and execution-aware trade outcomes under frozen v0.1 rules
metrics:
  - trade_count
  - expectancy_R
  - win_rate
  - average_win_R
  - average_loss_R
  - profit_factor
  - max_consecutive_losses
  - max_drawdown_R
  - MAE_R
  - MFE_R
  - median_holding_time
  - target_hit_rate
  - stop_hit_rate
  - time_stop_rate
  - execution_ambiguous_count
stopping_or_kill_conditions:
  - no_same_sample_parameter_rescue
relations:
  - type: tests_hypothesis
    target: HYP-HR-001
---

# Horizontal Reaction Strategy v0.1 — Frozen Specification

## Instrument and time

- Instrument: XAU/USD spot gold.
- Base research price side: BID, unless an execution-specific specification is separately frozen.
- Base granularity: M1.
- Research timezone: UTC.
- Candidate minute uses only observations strictly before that minute.

## Horizontal zones

For candidate minute t:

- Support center S = minimum Low of the immediately preceding 60 observed M1 bars.
- Resistance center R = maximum High of the immediately preceding 60 observed M1 bars.
- Gamma = mean absolute consecutive M1 Close change computed only from observations available strictly before t.
- Support zone = [S-gamma, S+gamma].
- Resistance zone = [R-gamma, R+gamma].
- Boundary equality counts as inside the zone.

## Setup and confirmation

LONG:

1. approach support zone from above,
2. enter support zone,
3. later completed M1 Close returns above S+gamma,
4. entry at the next executable observation after that confirming close.

SHORT:

1. approach resistance zone from below,
2. enter resistance zone,
3. later completed M1 Close returns below R-gamma,
4. entry at the next executable observation after that confirming close.

If approach direction is ambiguous, setup is unavailable.

If price passes through the zone without a qualifying return-close, there is no trade.

Maximum one open position at a time.

## Stop and target

- LONG stop = S-gamma.
- SHORT stop = R+gamma.
- RISK = absolute difference between entry price and stop price.
- RISK <= 0 or non-unique reconstruction => trade unavailable.
- Target = 2.0 x RISK from entry in the favorable direction.
- No stop widening.
- No partial profit-taking.

## Time stop

Maximum holding time = 15 completed minutes after entry.

If neither stop nor target has executed by the boundary, exit at the first executable observation at or after the time-stop boundary.

## Re-entry

After a trade or ambiguous setup, no new trade from the same interaction until price clearly leaves the zone and a fresh approach from the required side occurs.

No averaging, pyramiding, hedging, or immediate reversal.

## Deliberately excluded

No:

- EMA/SMA filter
- Volume Profile filter
- prior-session volatility filter
- New York-session filter
- trend-alignment filter
- CFTC positioning filter
- JOLTS/news filter
- discretionary chart-pattern override
- threshold search
- RR search

## Scientific boundary

Any change to lookback, gamma, confirmation, stop, target, time stop, cost, or evaluation sample after outcome access creates a new version.

v0.1 must not be rewritten to fit results.

## Source

Frozen preregistration:
https://docs.google.com/document/d/1Uaq7dhaR2sJVXIp8yM4KqH12gvsZlnPhtRbxErA1pUA/edit
