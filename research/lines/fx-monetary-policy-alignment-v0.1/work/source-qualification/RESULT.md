---
id: DIAG-FXMP-SOURCE-001
type: Diagnostic
research_line_id: RL-FXMP-001
created_at: 2026-10-03
status: QUALIFIED_FOR_RETROSPECTIVE_SCOPE
execution_status: SUCCESS
evidence_validity: VALID_FOR_RETROSPECTIVE_SCOPE
scientific_status: NOT_APPLICABLE
tests_hypothesis: NOT_APPLICABLE
relations:
  - type: uses_specification
    target: SPEC-FXMP-001-v01
---

# Packet A — BIS policy-rate source qualification

## Scope

Metadata/source qualification only. No FX price history, price ranking, forward return, strategy return or performance metric was accessed or calculated.

## Sources freshly reviewed

Official BIS sources:

1. Central bank policy rates overview  
   https://data.bis.org/topics/CBPOL
2. Central bank policy rates data documentation, updated 18 Jun 2026  
   https://www.bis.org/statistics/cbpol/cbpol_doc.pdf
3. BIS bulk downloads  
   https://data.bis.org/bulkdownload
4. BIS SDMX REST API v2 documentation  
   https://stats.bis.org/api-doc/v2/
5. BIS permitted-use terms  
   https://data.bis.org/help/legal
6. BIS Quarterly Review 2017, "Recent enhancements to the BIS statistics"  
   https://www.bis.org/publications/qr-201709/recent-enhancements-bis-statistics

## Source-family identity

- dataflow: `BIS,WS_CBPOL,1.0`
- monthly keys confirmed by the BIS Data Portal:
  - `M.AU`
  - `M.CA`
  - `M.CH`
  - `M.XM`
  - `M.GB`
  - `M.JP`
  - `M.NZ`
  - `M.US`
- unit: per cent per year
- frequency: monthly
- monthly series are derived from daily series and correspond to the last business day of the reference month
- daily source: reported directly to BIS by member central banks
- BIS collaborated with national central banks in selecting the represented policy rate
- when a central bank communicates a target band, BIS normally shows the midpoint unless the central bank recommends another representative rate
- when the policy instrument changes, the BIS long series splices the sequence and documents breaks

The reviewed documentation and Data Portal establish coverage extending well before 2009 for all eight areas and current monthly availability through 2026 for the required family. Australia and Canada portal pages explicitly show 1976-04 and 1960-07 starts; the documentation gives 1946/1954/1985/1999-era starts or earlier for the remaining required areas.

## Bulk/API routes

Published official routes exist:

- flat CSV bulk archive: `https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip`
- BIS API v2: SDMX REST data endpoint described at `https://stats.bis.org/api-doc/v2/`

The public bulk-download page listed the Central bank policy rates flat CSV during this review.

### Raw-snapshot limitation

The tool environment used for this review could discover the official archive URL, but did not successfully materialize the ZIP bytes. Therefore:

- exact current archive SHA-256: UNKNOWN
- exact row count for the 8-series/2009-2026 slice: UNKNOWN
- actual duplicate/missing/status distribution from raw bytes: UNKNOWN
- raw-source byte identity: NOT LOCKED

This is why overall evidence validity is PARTIAL rather than VALID.

## Policy-rate identity review for the eight areas

| Currency | BIS area | Main reviewed identity in/around 2010-2026 | Material source-semantic issue |
|---|---|---|---|
| AUD | AU | cash rate target | no reviewed in-sample instrument switch |
| CAD | CA | target overnight rate | no reviewed in-sample instrument switch |
| CHF | CH | midpoint of SNB target range -> SNB policy rate from 13 Jun 2019 | yes |
| EUR | XM | MRO rate -> deposit facility steering rate from 18 Sep 2024 | yes |
| GBP | GB | Bank Rate | no reviewed in-sample instrument switch |
| JPY | JP | several regimes; explicit no-policy-rate period 4 Apr 2013–20 Sep 2016 | critical |
| NZD | NZ | official cash rate | no reviewed in-sample instrument switch |
| USD | US | midpoint of Federal Reserve target rate | no reviewed in-sample instrument switch |

### Critical finding

A naive `r(k-1)-r(k-4)` panel would mix true policy changes with changes in the represented instrument and, for Japan, periods where BIS explicitly says no policy rate was adopted.

Therefore the initial Issue #41 sketch is **not safe to freeze unchanged**.

The source-qualified proposal must fail closed when a selected currency's lookback crosses a documented policy-instrument identity change or enters a documented no-policy-rate interval.

## Latest-vintage / revision boundary

BIS publishes long spliced historical series and can update its data set and metadata. The current public documentation is sufficient for a retrospective latest-vintage association design.

It is **not** sufficient to claim that the exact current historical series and break metadata were available to a trader at each historical date.

Point-in-time vintage availability remains UNVERIFIED.

## Reuse / terms

BIS states that use of its statistics is unrestricted subject to its conditions, including source citation, no misleading implication of endorsement/affiliation, and the stated commercial-use condition. API use has separate operational terms.

If national underlying source material is reproduced, preserve the BIS/national-source attribution required by the documentation.

## Qualification result

**PARTIAL_WITH_GAPS / CONDITIONAL_SOURCE_FAMILY_ACCEPTABLE**

Supported:
- one official source family spans all eight required areas;
- monthly series keys and semantics are clear;
- units/frequency/source provenance are suitable for an outcome-blind feature;
- known policy-instrument breaks can be explicitly guarded.

Not yet established:
- byte-locked raw snapshot;
- exact 2009-2026 missing/status distribution;
- raw-hash reproducibility in the intended execution environment;
- exact historical vintage/revision availability.

## Required next source action

Before human freeze or any FX outcome access:

1. capture the official BIS flat CSV or API response in a durable location;
2. hash raw bytes;
3. extract only M.AU/M.CA/M.CH/M.XM/M.GB/M.JP/M.NZ/M.US;
4. verify coverage, duplicates, numeric validity and missing values for the required source interval;
5. encode documented break dates in a machine-readable source lock;
6. demonstrate that the proposed break-aware feature ledger can be built without reading FX target outcomes.

No source substitution is authorized if this action fails.


## Packet C raw-source preflight update — 2026-10-03

A minimal outcome-blind GitHub Actions preflight successfully downloaded the official BIS flat CSV archive and inspected only the policy-rate predictor source.

Execution identity:
- workflow run: `37130000351`
- workflow head: `6e60055b3748c4ec156deecff61114016e4c44a5`
- result: PASS
- FX price/return access: NO
- observation values emitted to logs: NO

Raw source identity:
- official URL: `https://data.bis.org/static/bulk/WS_CBPOL_csv_flat.zip`
- archive bytes: 4,134,512
- archive SHA-256: `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`
- CSV member: `WS_CBPOL_csv_flat.csv`
- uncompressed bytes: 475,596,384
- CSV SHA-256: `0ba9441232f120b4237121494e57d5faf4a087615528f411b8ecc3e1750a4ff9`

Deterministic predictor slice:
- period: 2009-09 through 2026-08
- areas: AU/CA/CH/XM/GB/JP/NZ/US
- rows: 1,592
- slice bytes: 34,192
- slice SHA-256: `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`

Coverage:
- AU/CA/CH/XM/GB/NZ/US: 204/204 monthly rows each.
- JP: 164/204 monthly rows.
- JP absent monthly rows: 2013-05 through 2016-08 inclusive, 40 months.
- present rows: zero duplicate months, zero blank OBS_VALUE, zero nonnumeric OBS_VALUE.
- observed status/confidentiality codes in the selected slice: OBS_STATUS=A and OBS_CONF=F only; their official codelist meanings remain to be locked before final freeze.

The JP row gap is consistent with the official BIS documentation stating no BOJ policy rate was adopted from 4 Apr 2013 through 20 Sep 2016. The feature rule remains stricter than row availability: any lookback interval overlapping the documented no-policy-rate interval is unavailable.

Machine-readable receipt: `SOURCE_LOCK.json`.

### Remaining gap

The Actions artifact contains the raw archive and deterministic predictor slice but expires on 2026-11-02. Hash identity is now locked, but durable long-term raw-byte preservation is not yet established. This does not justify substituting a future BIS release if its bytes differ.

### Updated qualification

**QUALIFIED_WITH_GAPS / SOURCE_IDENTITY_LOCKED / SEMANTIC_GUARDS_REQUIRED**

The source is sufficient to proceed to deterministic outcome-blind implementation and independent audit. It is not sufficient to open market-outcome access.


## Durability and SDMX code update — 2026-10-04

The exact deterministic predictor slice is now preserved in Git:

- path: `research/lines/fx-monetary-policy-alignment-v0.1/datasets/bis_cbpol_monthly_8ccy_2009-09_2026-08.csv`
- Git blob SHA-1: `1dc3057e1d370d9c56c721b9caa6d26e7cd5dfba`
- bytes: 34,192
- SHA-256: `2cf878dbd0b8a98c05db741dc40a14d0b62a7cb6c178f86121937b0d41eb7eee`

The raw BIS ZIP remains identified by SHA-256 `707f39206f7c4bc1001ea7f67b182d20e9b2d59fcf6542d0dd566a19f61d7f15`; the predictor slice required by this line no longer depends on the expiring Actions artifact.

BIS technical SDMX guidance defines the observed flags as:

- `OBS_STATUS=A`: normal value; no break in period.
- `OBS_CONF=F`: free, for publication.

The selected predictor slice contains only A/F among present rows.

### Current qualification

**QUALIFIED_FOR_RETROSPECTIVE_LATEST_VINTAGE / SOURCE_AND_SLICE_IDENTITY_LOCKED**

Remaining limitation: historical point-in-time vintage availability is not established. Therefore this source qualification does not support a real-time historical availability or causal-entry claim.
