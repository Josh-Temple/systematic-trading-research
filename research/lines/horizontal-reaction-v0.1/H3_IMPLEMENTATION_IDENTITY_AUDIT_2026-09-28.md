# H3 implementation identity audit — 2026-09-28

Status: PRE_OUTCOME_AUDIT_COMPLETE_WITH_BLOCKING_MISMATCHES

Scope: Horizontal Reaction / HYP-HR-003 pre-execution preparation only.

This audit does not access or compute DATA-HR-003 outcomes. It does not compute touch-to-+15m returns, CONFIRMED-vs-UNCONFIRMED contrasts, or bootstrap output.

## Purpose

The frozen H3 specification inherits the existing first-touch generator, v0.1 confirmation rule, and D4-compatible quote-side convention. The repository review identified that these were not fully reconstructable from GitHub text alone.

This audit recovers the exact historical implementation and records what is established versus what remains unresolved before H3 may execute.

## Fresh source reads

Fresh-read sources:

- `SPEC-HR-001-v01` in GitHub.
- `SPEC-HR-002-v01` and `RUN-HR-006` in GitHub.
- `SPEC-HR-003-v01`, `EXP-HR-007`, `DATA-HR-003`, and `DEC-HR-003` in GitHub.
- Horizontal Reaction Strategy v0.1 — Chat Branch Preregistration, Drive ID `1Uaq7dhaR2sJVXIp8yM4KqH12gvsZlnPhtRbxErA1pUA`, revision `ANLCKQmIHzvxJI2e2ike-vW7ZNZRrGunufwMcBcjy2_sxTeXfLANsAYP7r7YYtwWvo1Opua6l4iEkni16X1Bsz8CT66VTalNwhJo7Pd8UI4`.
- Horizontal Reaction — Confirmation Selection Effect Preregistration — Post-H2 v1, Drive ID `1GRa035N5FX3F59_wM2T11VFuv3aL85YZghmvaCeTJ0g`, revision `ANLCKQnJyP7_pm0iR8Tq1KIple04tEee-vnwF7RB9SuGhLZt_fAV0wTUpC0sfeOmeLTkyyZWusSu5OIDLCxcJWvXeMKnPT2g00hQZS8z0HU`.
- Horizontal Reaction — Confirmation Selection Effect Source Preparation Handoff v1, Drive ID `1QPwXqAcp1fzPm6VXelMLDMyist02-sSSDQ1lkrpsoSg`, revision `ANLCKQl7GEONhGA6zeB6JVcxlC2p-3TWmWIb_bk3Q_ztIeCaHDt7jNrYaz14mQrnpGeF8wkbSuXU377S5mDS1k1eM7MX45WSDr5gUI54BwA`.
- Horizontal Reaction — 2026H2 Reproducibility Code and Result v3.
- 2026-09-23 reproducibility package and SHA manifest.

## Exact implementation identity recovered

The H1/H2 touch generator source was recovered directly from Drive:

- title: `run_v01.py`
- Drive ID: `1nWSPnCI-cVn0miZuQZrgm9ihWc6ap3NO`
- SHA-256 from recovered bytes:
  `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`

The 2026-09-23 SHA manifest independently records the same hash for:

`H2_frozen_touch_generator_run_v01.py`

The H2 frozen replay calculation code imports this generator and records its own calculation script SHA-256:

`6e881b417ee7d211b995404222f59fa3f4888af5c6fa5d5fa6e2dd370600f540`

Therefore the generator implementation used by the H2 replay is now byte-identifiable.

## Recovered generator behavior

### Support / resistance

For each candidate bar, support and resistance use the immediately preceding 60 observed M1 bars:

- support = minimum prior-60 Low;
- resistance = maximum prior-60 High.

The candidate bar itself is excluded from these two extrema.

### Gamma in the executed implementation

The executed `build_session_events()` does not calculate Gamma from only the preceding 60 bars.

It builds a cumulative absolute-close-change prefix across the full loaded M1 sequence and, at candidate index `global_i`, uses:

`gamma = abs_change_prefix[global_i] / (global_i - 1)`

The prefix at `global_i` includes the close change ending at the candidate bar itself.

This is materially different from a simple reading of the frozen prose, which states that Gamma is computed from observations available strictly before the candidate minute and does not specify an expanding-history origin.

### Touch / fresh approach

Support touch requires all of:

- support interaction is not locked;
- no support interaction is pending;
- previous M1 Close is above the support-zone upper boundary;
- current M1 Low reaches or crosses that upper boundary.

Resistance touch is the mirror condition:

- not locked;
- no pending interaction;
- previous Close below resistance-zone lower boundary;
- current High reaches or crosses that lower boundary.

If both support and resistance touch on the same bar, the bar is marked ambiguous and neither touch is added to the normal touch population in this implementation path.

### Confirmation

A touch cannot confirm on the same M1 bar. Confirmation is checked only on a later bar.

LONG confirms when a later completed bar closes above the zone upper boundary frozen at touch time.

SHORT confirms when a later completed bar closes below the zone lower boundary frozen at touch time.

The signal-available timestamp is the confirming bar timestamp plus 60 seconds.

### Failed interaction and reset

A pending support interaction that decisively closes through the far support boundary without confirmation is cleared and locked; resistance is handled symmetrically.

A locked support interaction becomes eligible again only after a later whole bar has Low above the then-current support-zone upper boundary.

A locked resistance interaction becomes eligible again only after a later whole bar has High below the then-current resistance-zone lower boundary.

The reset check therefore uses the dynamically recalculated zone for the current bar rather than the original frozen interaction zone.

### Same-bar dual confirmation

After generating confirmations, events sharing the same confirmation-bar timestamp are treated as ambiguous and excluded from the clean confirmed-event list.

This behavior matters for H3 because its frozen specification requires a binary CONFIRMED / UNCONFIRMED classification for every eligible touch. The retrieved H3 text does not explicitly state whether a touch that reaches a mechanically qualifying confirmation on a bar that is later excluded as a same-bar dual confirmation should be classified CONFIRMED or UNCONFIRMED.

No safe default is inferred here.

## D4 / H2 quote-side convention recovered

The H2 frozen replay uses the recovered generator touch output and then locates the first raw BID/ASK quote inside the touch bar.

For LONG:

- touch is detected when BID reaches the support zone;
- touch price for the direction-aware outcome uses ASK;
- +15m endpoint uses the first quote at or after touch-quote timestamp + 15 minutes;
- endpoint price uses BID.

For SHORT:

- touch is detected when BID reaches the resistance zone;
- touch price uses BID;
- +15m endpoint uses ASK.

This reconstructs the D4/H2 direction-aware quote-side convention referenced by H3.

## Generator context identity recovered

The H2 reproducibility package contains `H2_M1_Generator_Input_Manifest_135files_v1.csv/json`.

The manifest records:

- 135 M1 files used by the frozen replay;
- 75 files as `PRETOUCH_GENERATOR_CONTEXT`;
- 60 files as `FROZEN_H2_SELECTED_SESSION`;
- first generator-context date: 2025-12-31;
- first selected H2 session: 2026-04-13;
- last selected H2 session: 2026-07-09;
- raw SHA recheck: 135/135.

Because the executed Gamma is an expanding cumulative statistic, generator output depends on this history origin and the complete ordered set of earlier M1 bars, not only on a local 60-bar warm-up.

## Blocking mismatch 1 — temporal semantics

The frozen prose says the candidate minute uses observations strictly before that minute.

The executed generator instead uses a Gamma value whose cumulative numerator includes the Close change ending at the candidate bar. The same candidate bar's Low/High is then used to identify a touch, and the H2 replay searches for the first touch quote inside that M1 minute.

Therefore the executed generator uses information from the completed candidate bar when defining the zone for an event occurring inside that bar.

This is a temporal-information mismatch and must be treated as a potential lookahead / temporal leakage issue. It is not resolved by the fact that H1/H2 reproduced the same historical outputs.

## Blocking mismatch 2 — source-preparation warm-up scope

The current H3 source-preparation handoff says to acquire only deterministic warm-up/boundary context required by the existing 60-bar horizontal generator.

That is insufficient to reproduce the historical implementation as recovered because Gamma depends on the entire loaded M1 prefix.

Before H3 execution, the allowed generator-history origin must be established from existing pre-outcome evidence. It must not be selected after viewing DATA-HR-003 outcomes.

A plausible source-preserving route is to continue from the already frozen H2 generator input identity through 2026-07-09 and append post-2026-07-10 first-party M1 source in chronological order, but this audit does not authorize that choice as a new scientific rule.

## Blocking mismatch 3 — binary confirmation classification edge case

H3 requires every eligible touch to be classified CONFIRMED or UNCONFIRMED.

The legacy generator has an explicit same-confirmation-bar ambiguity rule that removes multiple confirmations sharing one bar from the clean event list.

The frozen H3 text does not state how such touches map into the required binary classification.

This must be resolved from an existing pre-outcome source or by human decision before execution. It must not be inferred after outcomes are available.

## What is established

- Exact legacy generator bytes and SHA-256 are recovered.
- H2 replay's use of that generator is independently documented.
- Support/resistance, touch, reset, confirmation, and D4/H2 quote-side mechanics are recoverable from the code.
- H2 generator input context is identified as 135 raw M1 files spanning 2025-12-31 through 2026-07-09, with 75 context files and 60 selected H2 sessions.
- No H3 outcome was accessed or computed in this audit.

## What is not established

- That the legacy Gamma implementation matches the intended frozen prose.
- That the current-bar Gamma dependency is scientifically acceptable for the intended real-time event definition.
- The exact H3 generator-history origin after 2026-07-09.
- The binary H3 classification of the legacy same-confirmation-bar ambiguity case.
- H3 source gate PASS, 60-session maturity, any H3 result, or any H3 scientific classification.

## Required next step

Do not run H3 outcomes yet.

Before execution, resolve the three blocking mismatches above without using DATA-HR-003 outcomes.

Any correction to Gamma temporal semantics or history origin that changes event generation must be treated as a specification/implementation change, not silently described as reproduction of the legacy generator.

If the exact frozen H3 test is retained despite the legacy implementation behavior, its scientific interpretation must explicitly state the temporal-information limitation.

