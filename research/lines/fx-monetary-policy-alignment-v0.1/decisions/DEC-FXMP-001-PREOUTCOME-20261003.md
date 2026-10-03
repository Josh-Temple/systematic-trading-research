---
id: DEC-FXMP-001-PREOUTCOME-20261003
type: Decision
research_line_id: RL-FXMP-001
created_at: 2026-10-03
status: ACTIVE
relations:
  - type: derived_from
    target: DIAG-FXMP-SOURCE-001
  - type: derived_from
    target: REF-FXMP-SCI-001
---

# Pre-outcome decision after source and literature review

## Decision

**ADVANCE_PREPARATION_ONLY / KEEP_OUTCOME_GATE_CLOSED**

The BIS policy-rate family remains a viable first source candidate, but the naive Issue #41 sketch is not frozen.

The working specification is corrected before outcome access so that documented policy-instrument changes and no-policy-rate periods fail closed rather than being interpreted as monetary-policy momentum.

## Why

Source review found material in-sample semantic discontinuities:
- CHF representation changes in 2019;
- EUR representation changes in 2024;
- JPY has an explicit no-policy-rate period from 2013 to 2016 and multiple regime changes.

Literature review also shows that observed policy-rate changes are not equivalent to:
- monetary-policy surprises;
- Taylor-rule fundamentals;
- broad economic momentum;
- market-implied expected rates;
- structural monetary-policy shocks.

## Current admissible work

Allowed:
- raw BIS source capture/hash;
- metadata/break lock;
- source-only missingness/coverage checks;
- deterministic synthetic implementation;
- independent audit;
- human review of still-unfrozen scientific choices.

Not allowed:
- read or calculate CSM market outcomes;
- calculate ALIGNED/OPPOSED forward returns;
- choose a lookback based on observed FX performance;
- add macro variables after viewing results;
- convert a historical result directly into a trading rule.

## Human boundary before freeze

Two scientific choices remain explicitly unfrozen:

1. policy-rate lookback = proposed 3 calendar months;
2. minimum group counts = proposed 24 ALIGNED and 24 OPPOSED.

They must be accepted or changed before any outcome access. Changes made now are pre-outcome design changes; changes after outcome exposure would require a new research question/sample.
