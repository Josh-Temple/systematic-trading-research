---
id: SPEC-JP225-IMOM-001-v01.2
type: SpecificationAmendment
research_line_id: RL-JP225-IMOM-001
created_at: 2026-10-05
status: FROZEN_PRE_OUTCOME
market_outcome_access: false
amends:
  - SPEC-JP225-IMOM-001-v01
  - SPEC-JP225-IMOM-001-v01.1
---

# Source-semantic hardening amendment v0.1.2

This amendment was created during Packet A source qualification before any 2025/2026 JPX/DataCube market outcome was acquired or inspected.

It does not change the research mechanism, early/late clock boundaries, bootstrap rule, minimum sample size or advancement thresholds.

## A. Valid DataCube transaction

For the 2025 DataCube financial-derivatives tick schema, a transaction is eligible for the four frozen point-price mappings only when all of the following hold:

- product identity is Nikkei 225 mini (index/product segment 19);
- contract_month equals the calendar-selected quarterly contract;
- execution_date equals the expected calendar date for the boundary;
- trade_price is finite and positive;
- trade_volume is positive;
- sco_category == 0.

Rows with sco_category == 1 are strategy-trade leg executions and are excluded from point-price mapping.

## B. Same-timestamp ordering

The DataCube financial-derivatives tick specification provides No / sequence number as execution order within each trade date and security code, sorted ascending.

For multiple otherwise valid trades with the same displayed millisecond timestamp:

1. choose the lowest No;
2. if No is missing, duplicated, or cannot establish a unique order, the boundary is unavailable.

No price-based tie-break is allowed.

## C. 2025 source boundary

The 2025 confirmation must not require acquisition or inspection of 2024 tick data.

A 2025 candidate date is eligible only if its previous eligible TSE cash-market date is also in calendar year 2025.

Therefore the first 2025 TSE trading date is excluded with reason:

PREVIOUS_DATE_OUTSIDE_CONFIRMATION_SOURCE_BOUNDARY.

This is a source-boundary exclusion, not a market result.

## D. 2026 holdout predecessor

If the 2026 holdout is ever unlocked, its first candidate date may use the immediately preceding 2025 mapped 15:30 point only when that point was already preserved under the accepted 2025 source identity.

If that bound predecessor is unavailable, exclude the first holdout candidate date rather than reopening an unbound source path.

## E. Data publication boundary

Raw DataCube files, reconstructable extracts and row-level mapped prices remain local-only unless the applicable JPX use category expressly permits third-party/cloud use.

Repository artifacts may contain source hashes, schema metadata, counts and non-reconstructable aggregate scientific results only, subject to the final license decision recorded by Packet A.
