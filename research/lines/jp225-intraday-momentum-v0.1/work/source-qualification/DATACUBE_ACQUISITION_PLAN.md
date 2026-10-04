# J-Quants DataCube acquisition plan — pre-outcome

Status: NOT_EXECUTED

This plan is operational only. It does not authorize payment or market-outcome inspection.

## Intended purchase

Dataset:

- J-Quants DataCube
- Financial Derivatives Information
- Tick
- Nikkei 225 mini
- calendar months: 2025-01 through 2025-12

Do not purchase 2024 data for v0.1. Amendment v0.1.2 excludes the first 2025 candidate date rather than opening a December 2024 source file.

## Before payment

Confirm:

1. account/use category applicable to this project;
2. whether non-reconstructable aggregate research results may be published publicly under that category;
3. exact 2025 monthly product/item pages;
4. exact checkout price;
5. raw-file download/retention rules.

If publication rights remain ambiguous, ask JPX Client Services before purchase.

## Local raw directory

Recommended local-only structure:

jp225_imom_2025_raw/
  purchase_receipt/
  2025-01/
  ...
  2025-12/
  SOURCE_MANIFEST.json

Never commit or upload this directory.

## Outcome-blind local qualification

For each raw file, calculate only:

- filename;
- bytes;
- SHA-256;
- CSV header identity;
- row count;
- min/max execution_date and trade_date;
- set of index_type;
- set/count of contract_month;
- count of strategy vs non-strategy rows;
- duplicate/missing sequence-number diagnostics;
- counts of eligible rows in each required +60-second clock window.

Do not calculate:

- price changes;
- direction;
- returns;
- correlations;
- regression;
- trade P&L;
- best/worst dates.

## Repository receipt

Commit only a non-reconstructable receipt and manifest hash.

A future source PASS must bind the raw local files by SHA-256 before any mapped price-point file is generated.
