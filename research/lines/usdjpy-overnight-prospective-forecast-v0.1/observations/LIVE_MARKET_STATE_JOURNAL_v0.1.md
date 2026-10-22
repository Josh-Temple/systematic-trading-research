---
type: ObservationProtocol
protocol_id: OBS-USDJPY-LIVE-STATE-001-v01
research_line_id: RL-USDJPY-OVERNIGHT-001
status: ACTIVE_OBSERVATIONAL
created_at: 2026-10-05
scientific_effect: NONE
scored_forecast_authority: NONE
broker_authority: NONE
---

# Live Market State Journal v0.1

## 1. Purpose

Maintain an append-only, point-in-time record of how the USD/JPY market state changes during the week.

This stream is intentionally separate from the frozen overnight and weekly forecast benchmarks.

It exists to answer questions such as:

- what changed between morning, Tokyo close, and pre-forecast time;
- which facts were known before a later move;
- when the working interpretation changed;
- which assumptions repeatedly failed;
- whether a later challenger should be proposed.

The journal itself is **not** confirmatory evidence of forecast skill.

## 2. Observation cadence

Default checkpoints in `Asia/Tokyo`:

- `08:30` — MORNING_STATE
- `15:00` — TOKYO_CLOSE_STATE
- `21:30` — PRE_FORECAST_STATE

Additional event-driven entries are allowed when a material event occurs, for example:

- Fed / BOJ decisions, minutes, speeches, or guidance;
- U.S./Japan macro releases;
- intervention statements or intervention;
- large yield moves;
- geopolitical / energy shocks;
- unusual USD/JPY price movement;
- source outage or data-quality incident.

Manual ad-hoc entries are also allowed.

The cadence is observational, not a scientific sampling rule. Missing a journal checkpoint does not invalidate a frozen benchmark event.

## 3. State-entry types

Allowed `checkpoint_type`:

- `MORNING_STATE`
- `TOKYO_CLOSE_STATE`
- `PRE_FORECAST_STATE`
- `EVENT_DRIVEN`
- `MANUAL`
- `CORRECTION`

Every state entry is a new artifact.

Existing entries are not silently rewritten.

## 4. Required separation inside each entry

Each entry must distinguish:

### Facts

Directly observed or source-supported items, such as:

- USD/JPY quote or bounded price state;
- U.S. 2Y / 10Y yields;
- BOJ / Fed policy facts;
- released economic data;
- official statements;
- timestamped news;
- scheduled future events known at observation time.

### Interpretation

Current model/researcher reading of those facts.

Interpretation is not a fact and must be labeled separately.

### Change since prior state

What materially changed since the previous journal entry.

If nothing material changed, record `NO_MATERIAL_CHANGE` rather than inventing a narrative.

### Current scenario map

- base case;
- strongest alternative;
- invalidation conditions;
- confidence.

Scenario language remains observational/research-oriented and is not an order instruction.

## 5. Minimum entry fields

Each entry must preserve:

- `state_id`;
- `research_line_id`;
- `observed_at`;
- `retrieved_at`;
- `checkpoint_type`;
- `source_cutoff`;
- `market_open_state`;
- `price_state`;
- `rates_state`;
- `policy_state`;
- `macro_news_facts`;
- `scheduled_events_known`;
- `source_refs`;
- `facts`;
- `interpretations`;
- `change_since_prior`;
- `base_case`;
- `alternative_case`;
- `invalidation_conditions`;
- `confidence`;
- `next_watch_items`;
- `benchmark_relation`;
- `entry_hash` where feasible.

Unknown values remain `UNKNOWN`.

Non-applicable values remain `NOT_APPLICABLE`.

## 6. Provenance requirements

For material source items preserve where feasible:

- source identity;
- URL / immutable identifier;
- publication timestamp;
- observation timestamp;
- retrieval timestamp;
- captured value or bounded summary;
- revision/vintage state;
- retrieval status.

A mutable search result or webpage must not later be re-queried and treated as identical evidence.

If a durable source snapshot cannot be preserved, record that limitation.

## 7. Append-only correction rule

Do not edit an old observation merely because later information shows it was wrong.

If an entry contains a factual or transcription error:

1. create a new `CORRECTION` entry;
2. reference the affected `state_id`;
3. identify the exact field/value corrected;
4. explain why;
5. state whether any downstream interpretation was affected.

A changed interpretation is not a correction.

It belongs in a later normal state entry.

## 8. Relationship to frozen benchmarks

The Live Market State Journal and the frozen benchmark serve different purposes.

### Journal

- may update multiple times per day;
- may change interpretation freely as new information arrives;
- is not itself scored;
- can generate challenger ideas.

### Frozen benchmark

- has fixed event definitions and score rules;
- cannot be rewritten after issuance;
- is the confirmatory/prospective comparison stream.

The journal must never overwrite a frozen forecast.

A later journal entry must never be inserted retroactively into an earlier forecast snapshot.

## 9. Journal use before a scored forecast

A pre-forecast journal entry may be used as an orientation aid.

However, for a scored forecast:

- the exact underlying qualified point-in-time source snapshot must remain available;
- the journal summary must not substitute for missing source evidence;
- any journal fact used by the forecast must be traceable to its underlying source item;
- information observed after forecast cutoff remains forbidden even if the journal later contains it.

Therefore the journal is a derived observation layer, not the canonical scored input layer.

## 10. Challenger-generation rule

Journal observations may suggest improvements.

Examples:

- repeated overreaction to one news category;
- failure to account for yield direction changes;
- recurring mismatch between policy narrative and price response;
- useful state transitions before major moves.

Any proposed improvement must:

- be labeled exploratory;
- cite the journal entries that motivated it;
- receive a new challenger/version identity;
- not rewrite the frozen v0.1 benchmark;
- not be treated as independently validated on the observations used to design it.

## 11. No trading authority

This journal does not:

- recommend or submit orders;
- set position size;
- define stop/target;
- authorize live or paper trading.

It records market state and interpretation only.

## 12. Initial operating status

Status: `ACTIVE_OBSERVATIONAL`.

The journal may start immediately because it does not open prospective outcome access or freeze scientific conditions.

The overnight and weekly scored specifications remain separately governed by their own human-freeze and readiness gates.
