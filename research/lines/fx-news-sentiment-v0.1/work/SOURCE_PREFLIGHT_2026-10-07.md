# Source preflight — 2026-10-07

Status: PARTIAL_WITH_GAPS / PRE-FREEZE
Scientific outcome: NOT_APPLICABLE

## Purpose

Identify a current, free, point-in-time news route that can be used by a ChatGPT Plus workflow without pretending that the historical SNB provider set is still operationally reproducible.

No EURJPY market outcome was used.

## DailyFX

The original SNB paper uses DailyFX among its provider-specific portfolios.

Current finding:
- IG states that DailyFX closed on 2024-09-04 and its analysis content moved to IG.

Decision:
- `HISTORICAL_PRIOR_SOURCE_NOT_CURRENTLY_REPRODUCIBLE`.
- Do not substitute another site using the DailyFX name and treat it as the same source.

Evidence:
- https://www.ig.com/uk/trading-strategies/dailyfx--now-get-your-trading-insights-on-ig-240906

## Investing.com

Current terms state that platform data/content may not be used, stored, reproduced, displayed, transmitted or distributed without prior written permission from Fusion Media and/or applicable providers.

Decision:
- `NOT_SELECTED_FOR_V0_1_CANONICAL_INPUT` under the current public-research preservation requirement.
- This is a source-governance decision, not a claim about editorial quality.

Evidence:
- https://www.investing.com/about-us/terms-and-conditions/
- current terms PDF linked from that page.

## FXStreet

Current general terms state that site content is protected and reproduction/retransmission/copying/redistribution is prohibited without prior authorization, apart from personal/private use. Separate content-distribution terms also include explicit restrictions around LLM/AI use.

Decision:
- `NOT_SELECTED_FOR_V0_1_CANONICAL_INPUT_WITHOUT_PERMISSION`.
- Do not rely on an ambiguous private-use theory for a confirmatory pipeline whose exact model inputs must be auditable.

Evidence:
- https://www.fxstreet.com/info/terms-conditions
- https://www.fxstreet.com/info/terms-and-conditions-products

## GDELT

GDELT states that datasets it releases are available for unlimited and unrestricted academic, commercial and governmental use and may be redistributed with attribution.

Relevant data/API properties:
- DOC 2.0 supports Article List output with article URLs and titles;
- JSON/JSONFeed/RSS output is supported;
- precise STARTDATETIME / ENDDATETIME windows are supported;
- GDELT updates in near real time;
- GDELT records include a timestamp for when an article was seen/processed;
- GDELT's article-list documentation notes that exact source publication timestamps are not always present, so "seen by GDELT" time must not be mislabeled as the publisher's publication time.

Decision:
- `PREFERRED_V0_1_SOURCE_CANDIDATE`.
- v0.1 should classify **GDELT title/headline metadata only**, not copy underlying publisher article bodies.
- availability cutoff should use the GDELT observation/ingestion timestamp, not an inferred publisher timestamp.
- the exact DOC API query, output ordering, max-record handling, deduplication, and runtime fetch must still be tested and frozen before formal scoring.

Evidence:
- https://gdeltproject.org/about.html
- https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/

## Rationale for headline-only design

Headline-only classification is not identical to the SNB full-text fine-tuned setup.

However:
- Lopez-Lira & Tang show that GPT-classified news headlines can contain forward-looking market information in U.S. equities;
- a separate FX sentiment study evaluates ChatGPT 3.5 on curated FX news headlines and reports improved sentiment classification versus FinBERT;
- headline-only GDELT inputs are materially easier to preserve point-in-time and reproduce without copying publisher article bodies.

Therefore the cleanest test of **ChatGPT Plus as an adoptable retail workflow** is a new prospective headline-based protocol, not a claim of direct SNB replication.

## Remaining gaps

Before source PASS:

1. execute the exact GDELT DOC API query in the intended runtime;
2. confirm returned title/URL/timestamp fields and timezone;
3. freeze query string and search terms;
4. define duplicate-URL and near-duplicate-title policy;
5. define behavior when records hit MAXRECORDS;
6. preserve raw GDELT response bytes/hash for each event;
7. verify that all stored GDELT-derived fields comply with attribution requirements.
