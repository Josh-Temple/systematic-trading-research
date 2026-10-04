# Source qualification contract

Status: PRE_OUTCOME

## Intended source

Official JPX/OSE J-Quants DataCube historical transaction ticks for Nikkei 225 mini.

## Must be established before prices are interpreted

- exact product page/dataset ID and purchased month files;
- file format and schema;
- timezone/timestamp convention;
- contract code -> contract month mapping;
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
