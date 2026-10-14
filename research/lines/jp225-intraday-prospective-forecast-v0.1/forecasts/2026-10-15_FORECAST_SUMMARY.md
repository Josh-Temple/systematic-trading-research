# JP225 2026-10-15 — late exploratory issued forecast

Issue timestamp in JSON: `2026-10-15T08:12:21.546+09:00`, verified GitHub publication time must be read from this commit. **No pre-08:00 event record existed**; reports published before 08:00 were accessed after cutoff. This event is permanently exploratory, `NOT_IN_COHORT`, with lateness and provenance gaps. The fixed target is **09:00→15:30**, not overnight futures or prior-close-to-close. No XM prices were retrieved.

| System | P(up) | Forecast log-return |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 proxy-only | 0.49 | -3 bps |
| A2 US macro / cross-market | 0.45 | -12 bps |
| A3 repository state | **0.47** | **-7 bps** |

A3 is **modestly bearish, low conviction, NO_TRADE**, not a validated strategy. Negative OSE overnight future (66,480; -1,680), US Nasdaq -1.88%, U.S. CPI upside surprise and WTI crude strength are pre-08:00 *published* contexts, but 09:00 opening may incorporate much of the shock. Publication evidence and hypothesis/caveats in `2026-10-15_LATE_INVOCATION_ASSESSMENT.md`.

Canonical SHA-256 values: A1 `901b8721eb29793d199ad8fc7dd6652de45087ed88ae8adc9ad58ae057dac73d`; A2 `ec561112b9bd8e3ed691ab54416362ac0e3a2ac558e992bdaff7dffc5f684a03`; A3 `aa788ed3ff7120dc2b54c6e9b87a879afb0c2a62af0eed8e2bbc012e1cd70bf9`. Specification PROPOSED_NOT_FROZEN, science UNTESTED, 60-event formal scored cohort CLOSED. After-close public index must not substitute for exact XM outcome. No live/paper trading.
