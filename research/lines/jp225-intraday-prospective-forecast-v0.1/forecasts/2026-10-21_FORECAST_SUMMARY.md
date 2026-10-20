# JP225 2026-10-21 — late exploratory pre-open forecast

**Late-issued**: user invoked after 08:00 JST and no pre-08:00 pre-registration/forecast freeze existed. Reports published before 08:00 were viewed after it, without raw 08:00 snapshots. Target remains **09:00→15:30 JST** exact-XM MT5 JP225Cash qualified midpoint, not previous-close-to-close or futures overnight gap. Exact XM input/output unavailable, NO_TRADE.

| System | P(up) | Predicted log return |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 public OSE futures context | 0.52 | +3 bps |
| A2 global market/news/FX | 0.51 | +2 bps |
| A3 repo status context | **0.51** | **+2 bps** |

**Headline:** effectively neutral with a tiny positive lean; subjectively inferred, extremely low conviction, not calibrated or validated.

Time-qualified source background: Osaka overnight Nikkei Dec futures 65,210 (+810 vs prior settlement, 06:00 snapshot, published 06:03); NY Dow +529.85, Nasdaq -6.07; USDJPY 158.17 (yen +0.33), US 10Y yield 5.11% (-0.03pp), WTI crude 101.79 (-1.87). This is primarily **opening** context and has no qualified mapping to signed 09:00→15:30 return. See `2026-10-21_LATE_INVOCATION_ASSESSMENT.md` for facts, sources, deviations and interpretations.

JSON prepared at `2026-10-21T08:20:06.058+09:00`; actual publication timestamp is GitHub issue commit (independently inspect). A1 SHA-256 `7438da4c7cac58b9961bd00fb41575e4bb8af8293bb280ee138ac78965150559`; A2 `b3279b07c3c7ce652c9dc07cbcf5e83e670c89e62524b17b7458a1b4198dbe77`; A3 `09b321414e6ad3c3f3dd12849440339ed88196af20f189a077cbeed385cf7157` (each 64 hex, sorted compact ASCII JSON without `canonical_sha256`).

**INTEGRITY BLOCKED:** original October 16 forecast JSONs have malformed SHA fields and official full-branch CI fails. Today's SHA values do NOT remediate the earlier failure. Preserve the original corrupt forecast blobs and the failure receipt; no validator weakening, historical backfill, cohort admission or trade action. Science UNTESTED, SPEC PROPOSED_NOT_FROZEN, formal scored cohort CLOSED, EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT, NO_TRADE.
