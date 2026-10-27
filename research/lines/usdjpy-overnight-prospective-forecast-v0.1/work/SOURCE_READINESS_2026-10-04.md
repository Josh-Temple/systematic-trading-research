---
type: SourceReadinessReview
research_line_id: RL-USDJPY-OVERNIGHT-001
created_at: 2026-10-04
status: PARTIAL_BLOCKED
scientific_effect: NONE
market_outcome_access: CLOSED
---

# Source/readiness review — USD/JPY prospective forecast v0.1

## 1. Conclusion

Formal scored forecasting is **not ready**.

The policy/calendar side now has several strong first-party routes, but three critical gaps remain:

1. the exact USD/JPY Bid/Ask reference-feed route has not passed this line's bounded raw-source qualification;
2. news snapshot immutability / cutoff preservation is not yet implemented;
3. deterministic event validation and scoring code is not yet implemented and synthetic-tested.

Therefore:

- overnight scored issuance: NOT_AUTHORIZED;
- weekly scored issuance: NOT_AUTHORIZED;
- 2026-10-05 through 2026-10-09 remains exploratory only.

## 2. Source matrix

| Input / function | Candidate source | Status | Notes |
|---|---|---|---|
| Fed current policy | Federal Reserve FOMC statement / implementation note | PASS_SOURCE_ROUTE | First-party, timestamped releases. |
| BOJ current policy | BOJ policy pages / complementary deposit facility | PASS_SOURCE_ROUTE | First-party; current rate semantics visible. |
| U.S. 2Y / 10Y Treasury yields | U.S. Treasury Daily Par Yield Curve | PASS_SOURCE_ROUTE | First-party daily values; 2026-10-02 includes 2Y 4.83%, 10Y 5.28%. |
| BLS scheduled releases | BLS release calendar | PASS_SOURCE_ROUTE | First-party schedule; snapshot still needs persistence. |
| FOMC minutes / Fed schedule | Federal Reserve monthly calendar | PASS_SOURCE_ROUTE | First-party schedule and release timestamps. |
| BOJ scheduled speeches | BOJ speeches / press schedule | PASS_SOURCE_ROUTE | First-party schedule. |
| JGB auction schedule | Japan Ministry of Finance auction calendar | PASS_SUPPLEMENTARY | Useful scheduled catalyst route, not a daily JGB market-yield substitute. |
| Japan 2Y / 10Y daily market yields | not yet qualified | PARTIAL | MOF auction yields are not the same object as daily secondary-market yields. Do not silently substitute. |
| USD/JPY reference Bid/Ask ticks | Dukascopy candidate | BLOCKED_PENDING_SAMPLE | Prior source work supports candidacy, but this line still needs bounded sample retrieval, timestamps, fields, missingness, hash and endpoint tests. |
| Current/general FX quote for dry run | Monex / Bloomberg Línea | EXPLORATORY_ONLY | Not allowed to replace frozen reference-feed identity. |
| News | Reuters candidate bounded source set | PARTIAL | Suitable current reporting for exploration; exact point-in-time snapshot persistence and source-set rules are not yet frozen. |
| Repository research | pinned Git refs/blobs | PASS_MECHANISM_PARTIAL_CONTENT | Git can pin evidence, but exact allowed refs/source-set version must be frozen. |
| Forecast artifact storage | Git commit history | PASS_MANUAL / PARTIAL_AUTOMATION | Append-preserving manually; automated event receipt/hash not implemented. |
| Deterministic scoring | project code | NOT_IMPLEMENTED | Required before formal start. |
| Cutoff leakage tests | project tests | NOT_IMPLEMENTED | Required before formal start. |

## 3. First-party routes verified in this review

### Federal Reserve

Current policy route:

- https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a1.htm

Calendar route:

- https://www.federalreserve.gov/newsevents/2026-october.htm

Observed current facts relevant to route qualification:

- target range changed to 3.75%–4.00% on 2026-09-16;
- September 15–16 FOMC minutes scheduled for 2026-10-07 at 14:00 ET.

### Bank of Japan

Current policy / rate route:

- https://www.boj.or.jp/en/
- https://www.boj.or.jp/en/mopo/measures/term_cond/yoryo36.htm

Speech/calendar route:

- https://www.boj.or.jp/about/press/index.htm

Observed route facts:

- BOJ guideline is around 1.25% for the uncollateralized overnight call rate;
- complementary deposit facility rate is 1.25%;
- Ueda speech listed for 2026-10-06.

### U.S. Treasury

Daily par yield route:

- https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve

Observed 2026-10-02 values:

- 2-year 4.83%;
- 10-year 5.28%.

### U.S. Bureau of Labor Statistics

Release calendar:

- https://www.bls.gov/schedule/2026/10_sched_list.htm

This is appropriate for scheduled BLS-event identity.

A formal source snapshot must still preserve retrieval time and the schedule actually observed before forecast cutoff.

### Japan Ministry of Finance

JGB auction calendar:

- https://www.mof.go.jp/english/policy/jgbs/auction/calendar/2610e.htm

Useful for known auction-event schedule.

Do not treat auction-result yields as a general daily 2Y/10Y secondary-market yield series.

## 4. News route

Reuters is a plausible bounded news source for the AI news/fundamental layer because it provides timestamped event reporting and broad USD/JPY-relevant coverage.

Candidate examples inspected during the dry run include:

- weak September U.S. payrolls;
- BOJ debate over the pace of further hikes;
- Japanese intervention warnings;
- oil/geopolitical developments.

However source qualification remains PARTIAL because formal operation still requires:

1. an allowed-source rule;
2. exact retrieval timestamp;
3. captured headline/source URL/publication timestamp;
4. bounded summary or content identity used by the model;
5. a durable snapshot that is not replaced by a later re-query;
6. explicit handling when the source is unavailable.

Do not treat a later search-result page as proof of what the model saw before cutoff.

## 5. Recommended mandatory/optional split before freeze

To keep v0.1 small and fail-closed, the source-readiness implementation should consider the following candidate split.

### Candidate mandatory weekly fundamentals

- current Fed policy state;
- current BOJ policy state;
- U.S. Treasury 2-year yield;
- U.S. Treasury 10-year yield;
- frozen official-event calendar for the target week;
- bounded timestamped news snapshot.

### Candidate optional until separately qualified

- Japan 2-year daily secondary-market yield;
- Japan 10-year daily secondary-market yield;
- additional private market positioning measures;
- derived sentiment feeds.

This is a readiness recommendation, **not yet a frozen scientific amendment**.

If accepted, the specification should be amended before freeze rather than allowing missing mandatory Japanese yield fields to block every forecast.

## 6. Reference-feed gate

The most important remaining data gate is the reference USD/JPY Bid/Ask stream.

Prior work identified Dukascopy as a candidate research/reference source, but formal use here still requires a small bounded source-only retrieval that records:

- exact retrieval route;
- source timestamp timezone/semantics;
- Bid and Ask fields;
- first/last tick;
- missing/duplicate behavior;
- raw bytes or durable permitted representation;
- source hash;
- endpoint selector behavior at 22:00 / 08:00 / Monday 08:00 / Friday 22:00 JST;
- DST behavior.

No forecast outcome should be calculated as part of that qualification.

## 7. Implementation gate

Minimum code needed before scored operation:

1. event schema validator;
2. timestamp/cutoff validator;
3. deterministic midpoint calculation;
4. endpoint-selection function;
5. deterministic Brier calculation;
6. deterministic MAE calculation;
7. immutable forecast-content hash;
8. event-status state machine;
9. synthetic tests for:
   - cutoff boundary;
   - future-information rejection;
   - 60-second quote tolerance;
   - missing inputs;
   - malformed probability;
   - exact-zero return;
   - weekly endpoint boundaries;
   - DST calendar conversion;
   - scoring arithmetic.

## 8. Readiness decision

Current readiness:

`PARTIAL_BLOCKED`

Formal weekly event 1 should not start until:

- the exact scientific packet is accepted/frozen;
- reference-feed gate passes;
- mandatory-source set is frozen and all mandatory routes pass;
- news snapshots can be durably captured;
- scoring/validation code and synthetic tests pass.

The earliest clean weekly cohort start remains the candidate Sunday 2026-10-11 cutoff, subject to completing those gates beforehand.
