# Human Decision Packet — USD/JPY Daily Breakout

Date: 2026-10-03 JST
Status: HUMAN_BOUNDARY / MARKET_OUTCOME_ACCESS=NO

## Decision required now

Choose one exit architecture before any historical market outcome is calculated.

### Option A — WEEKEND_FLAT

- Friday new entries: disabled.
- Existing position: close Friday 23:00 JST.
- Opposite signal can close earlier.
- The 10-check time exit is removed because weekly forced liquidation makes it largely unreachable.

Operational implication: avoids intentional weekend holding but turns the candidate into a short-horizon weekday strategy. Evidence about medium-horizon daily trend persistence cannot be inferred directly from this design.

### Option B — TEN_CHECK_HOLD

- Friday forced liquidation: disabled.
- Friday signals follow the same normal rule unless another explicit operational rule is chosen before outcome access.
- Exit on opposite signal or at the 10th weekday 20:00 review after entry, with entry-day review counted as check 0.

Operational implication: preserves a medium-horizon daily trend mechanism but intentionally carries weekend gap and swap exposure.

## Why there is no automatic choice

Both choices are coherent but answer different questions. Choosing based on historical P/L would violate the project rule that material scientific conditions are fixed before outcome inspection. Therefore NO_SAFE_DEFAULT applies.

## Other items still requiring human acceptance before freeze

- Whether 20:00 JST is operationally sustainable as the normal review time.
- Whether live testing, if ever authorized, may hold positions over weekends.
- Numeric acceptance / rejection thresholds for historical replay.
- Maximum tolerable live loss and whether the current draft risk budget is accepted or replaced.

These items remain UNKNOWN until explicitly decided. Market outcomes must not be used to fill them.

## Safe work that may continue before the decision

- qualify candidate data sources without computing strategy returns;
- verify broker symbol specifications and minimum quantity rules;
- implement synthetic tests for DST, strict prior-20-day exclusion, execution delay, stop evaluation, missing quotes, and position-size rounding;
- define provenance and output schema.

## Freeze rule

Once the human selects Option A or B, record the choice in a new versioned specification. Do not rewrite this packet or delete the unselected option.