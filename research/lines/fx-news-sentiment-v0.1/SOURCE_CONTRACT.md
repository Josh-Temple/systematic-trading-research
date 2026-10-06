# Source contract — FX News Sentiment with ChatGPT v0.1

Status: PREFERRED_CANDIDATE_IDENTIFIED / NOT_FROZEN

## News source

Preferred v0.1 route: GDELT Article List / DOC API metadata.

Reason:
- GDELT states its released datasets may be used and redistributed without restriction with attribution;
- Article List outputs include article URLs/titles;
- point-in-time seen/processed timestamps exist;
- precise time-window queries are supported;
- headline metadata can be preserved without copying publisher article bodies.

This is a new prospective headline protocol, not a direct reproduction of the SNB full-text provider setup.

## Availability-time semantics

Do not infer publisher publication time when it is not explicitly known.

For formal inclusion, use the frozen GDELT observation/ingestion timestamp as the operational "available to this pipeline" time.

Required condition:
- GDELT seen timestamp <= 08:00:00 JST cutoff.

If the underlying publisher page later changes, the classifier still uses only the GDELT title metadata preserved in the event snapshot.

## Required frozen GDELT fields

At minimum:

- event-local record ID;
- GDELT seen timestamp;
- title;
- article URL;
- source domain/outlet when supplied;
- raw-response artifact hash;
- query/version identifier;
- retrieval timestamp.

## Query contract still to freeze

Packet B must establish:

- exact query string;
- language restriction;
- STARTDATETIME / ENDDATETIME semantics or equivalent;
- sort order;
- MAXRECORDS;
- what happens if the result count reaches MAXRECORDS;
- URL deduplication;
- near-duplicate title handling;
- attribution text.

Formal cohort remains closed until the intended runtime successfully fetches and preserves the exact response.

## Excluded current provider routes

For v0.1 canonical inputs, do not use without a new governance decision:

- DailyFX historical route as though it were still current;
- Investing.com content requiring restricted storage/reproduction;
- FXStreet content requiring authorization for the intended preservation/AI workflow;
- arbitrary web-search ranking as a substitute for the frozen GDELT query.

## XM quote-source qualification

Before formal scoring establish:

- exact XM symbol identity for EURJPY;
- account/server identity;
- Bid/Ask semantics;
- server timestamp and UTC/JST mapping;
- 08:15 boundary selection;
- weekend/maintenance/missing-quote handling;
- commission, swap and other relevant account costs;
- raw source preservation and hash procedure.

If exact XM qualification fails, formal cohort remains closed. Do not substitute another provider for the same cohort.

## Model-input boundary

The classifier receives only the frozen GDELT headline record and the fixed classification instructions.

Forbidden:

- post-cutoff EURJPY prices;
- future returns;
- accumulated strategy P&L;
- later article revisions;
- prior scored outcomes;
- repository performance results;
- adaptive prompt changes based on results.

Pretraining may contain historical market facts. This remains an uncontrolled model limitation and is why v0.1 is prospective.
