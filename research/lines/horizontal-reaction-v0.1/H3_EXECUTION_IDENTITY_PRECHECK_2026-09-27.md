# H3 execution identity precheck — 2026-09-27

Status: **OUTCOME-BLIND PRE-EXECUTION REVIEW — HOLD FOR SPECIFICATION / IMPLEMENTATION CONFLICT**

Scope: Horizontal Reaction Strategy v0.1 / Post-H2 Confirmation Selection Effect (`HYP-HR-003`, `SPEC-HR-003-v01`, `EXP-HR-007`)

This record was created before H3 maturity and without reading or computing `DATA-HR-003` touch outcomes, CONFIRMED/UNCONFIRMED outcome comparisons, the primary contrast, or bootstrap output.

## Fresh-read code identity

Recovered from the persistent 2026H1 Source Pack:

- file: `run_v01.py`
- Drive file ID: `1nWSPnCI-cVn0miZuQZrgm9ihWc6ap3NO`
- bytes: `24350`
- SHA-256 in `persistent_artifact_manifest.csv`: `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`
- SHA-256 recomputed from the fresh retrieval in this review: `9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd`
- hash match: **PASS**

Source Pack: https://drive.google.com/drive/folders/1dd9IL9--BxlwITVOoXHHuwB3TouNtslv

`RUN-HR-006` records the H2 script `run_unconditional_replication_fast.py` with SHA-256 `6e881b417ee7d211b995404222f59fa3f4888af5c6fa5d5fa6e2dd370600f540`. Its reproducibility source imports the recovered `run_v01.py` and builds the H2 unconditional-touch population from `build_session_events(...)["touches"]`.

H2 reproducibility source: https://docs.google.com/document/d/1j_tpgHdw6CdXbe7rNwC2PTxxZUB1MOKs85Z4QQ-xDFM/edit

## Rules recovered from the exact code

These are code-path observations, not new strategy rules.

- Support / resistance use the preceding 60 M1 bars: `all_bars[global_i - 60:global_i]`.
- Support touch requires no lock/pending interaction, previous Close above the current zone, and current bar Low reaching the zone. Resistance is symmetric.
- If both zones touch on the same bar, the code records ambiguity and creates neither touch.
- A pending support touch confirms only on a later Close above its stored upper boundary; resistance confirms on a later Close below its stored lower boundary.
- A failed interaction remains locked until a whole later bar is beyond the zone; support unlock is `Low > zone_hi`, resistance unlock is `High < zone_lo`.
- Same-confirmation-bar multiple confirmations are marked ambiguous and excluded from the clean confirmed-event list.
- H2 D4 quote sides are LONG touch/open ASK -> +15m BID; SHORT touch/open BID -> +15m ASK. Direction-aware bps are `sign * (close - open) / open * 10000`.

## Material specification / implementation conflict

The exact historical implementation does **not** match the frozen prose for Gamma.

`SPEC-HR-001-v01` requires Gamma to use consecutive M1 Close changes available strictly before candidate minute `t`. `SPEC-HR-002-v01` repeats the same strictly-pre-candidate boundary. The 2026H1 Execution Result also states that Gamma used pre-candidate observed consecutive closes.

The preserved execution path instead builds an expanding prefix of absolute Close changes and then calculates:

`gamma = abs_change_prefix[global_i] / (global_i - 1)`

At candidate index `global_i`, `abs_change_prefix[global_i]` includes `abs(all_bars[global_i]["c"] - all_bars[global_i - 1]["c"])`. The same `all_bars[global_i]` is the candidate/touch bar whose Low or High is then used to decide whether a touch occurred.

Therefore the executed Gamma depends on the candidate bar Close rather than only observations strictly before that candidate bar. It is also an expanding-history prefix calculation rather than a 60-bar Gamma window. The separate helper `zone_and_gamma()` does not resolve the conflict because the executed `run()` path uses `build_session_events()` with the prefix calculation.

An outcome-free synthetic boundary check confirmed that changing only the candidate bar Close changes the executed Gamma while the strictly-prior calculation is unchanged.

## Consequences

This review does **not** recompute H1 or H2 market outcomes and does not reclassify their scientific results. It does establish an unresolved implementation-fidelity conflict:

1. the frozen specifications describe a strictly pre-candidate Gamma;
2. the preserved historical generator includes the candidate bar Close in Gamma;
3. H2 explicitly reused that recovered generator;
4. H3 requires the unchanged existing generator while also inheriting the frozen strategy definitions.

The repository must therefore not treat the historical generator as proven to be an exact implementation of the strictly-pre-candidate Gamma definition until this conflict is resolved.

## H3 execution boundary

There is no safe automatic choice between preserving the exact historical code path and changing Gamma to satisfy the frozen prose. Either choice changes what is being asserted about specification identity.

H3 must **not** be executed merely because 60 sessions mature. Before any H3 outcome access, a versioned decision must resolve which authority governs the H3 generator and what that implies for the existing preregistration. If resolution changes the frozen H3 protocol, `DATA-HR-003` must remain unused until the required versioning / preregistration boundary is satisfied.

No H3 outcome was accessed in this review.

## Additional unresolved implementation detail

`SPEC-HR-003-v01` requires every eligible touch to be classified as exactly `CONFIRMED` or `UNCONFIRMED`. The historical generator separately excludes same-confirmation-bar multiple confirmations as ambiguous. The reviewed sources do not yet specify how such a touch maps into H3's binary groups. This must not be guessed.

## Next action

Before H3 outcome access, create a versioned decision addressing:

1. Gamma authority: frozen strictly-pre-candidate definition versus exact historical code behavior;
2. implications for H1/H2 implementation-fidelity claims;
3. whether H3 can still execute under the existing preregistration or requires a newly versioned preregistration;
4. mapping of historical same-confirmation-bar ambiguity into H3's required binary classification.

Until then, outcome-blind source/sample preparation may continue, but H3 outcome computation is not execution-ready.
