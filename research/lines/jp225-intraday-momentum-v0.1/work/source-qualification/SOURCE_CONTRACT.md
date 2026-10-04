# Source qualification contract

Status: PRE_OUTCOME

## Intended source

Official JPX/OSE J-Quants DataCube historical transaction ticks for Nikkei 225 mini.

## Must be established before prices are interpreted

- exact product page/dataset ID and purchased month files;
- file format and schema;
- timezone/timestamp convention;
- contract code -> contract month mapping;
- authoritative 2025 TSE cash trading calendar and official OSE quarterly-contract last-trading-day mapping;
- transaction price and volume field meanings;
- whether identical timestamps have deterministic source order;
- coverage of 15:30/09:30/15:00/15:30 boundary windows;
- SHA-256 for every raw file;
- acquisition timestamp and account/source identity at non-sensitive granularity.

## Privacy / license boundary

Do not commit credentials.

Raw DataCube files are **LOCAL_ONLY by default** until the applicable terms explicitly permit cloud/GitHub storage or processing.

Repository-safe evidence should prefer:

- product/dataset identity;
- hashes;
- byte sizes;
- schema;
- row counts;
- timestamp coverage;
- contract coverage;
- qualification receipts;
- non-reconstructable aggregate results.

Do not upload raw licensed market data merely for convenience.

## Outcome blindness

Source qualification may inspect:

- file/schema metadata;
- timestamps;
- contract identifiers;
- row/coverage counts;
- non-price field availability required to establish semantics.

Before the source gate passes, it must not calculate:

- early returns;
- late returns;
- correlations;
- regression coefficients;
- strategy returns;
- direction counts derived from prices.

## Gate

Source gate is PASS only if the intended 2025 tick source can deterministically map all four required boundary requests without unresolved timestamp/product ambiguity.

Gaps in individual dates may remain and must be represented as unavailable dates; systemic ambiguity is a gate failure.


## Official pre-outcome facts already verified

The pre-outcome audit verified from JPX public materials that:

- Nikkei 225 mini trades in the OSE day session through 15:45, so all frozen 09:30/15:00/15:30 boundaries are within the regular/day-session schedule;
- quarterly contract months and the official last-trading-day rule are published by JPX;
- J-Quants DataCube offers historical OSE derivatives tick data in CSV form;
- DataCube tick data is transaction data, not BID/ASK quote history;
- product-specific schema/order semantics and the exact permitted storage/processing route remain Packet A work and must not be assumed.

These facts do not qualify the source by themselves.


## Packet A v0.1.2 source-semantic decisions

Before any market outcome access, Packet A fixes the following:

- use DataCube sequence No as the same-timestamp execution ordering key;
- exclude sco_category=1 strategy-leg prints from all four point-price mappings;
- require the expected contract_month and execution_date;
- do not acquire 2024 tick data solely to supply the predecessor for the first 2025 trading date;
- keep raw purchased DataCube files local-only until the applicable use category is confirmed.

These decisions are frozen in SPEC-JP225-IMOM-001-v01.2_SOURCE_AMENDMENT.md.
