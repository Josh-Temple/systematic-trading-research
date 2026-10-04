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


---

## Append-only refresh — 2026-10-04

Fresh public DataCube product-page review resolved the catalog-level series identity: 日経225mini 歩み値（ティック）, series/item route future_tick_19_YYYYMM. The public route has a monthly period selector; it does not expose twelve distinct month-specific URLs. The exact 2025-01 through 2025-12 period selections are listed in DATACUBE_2025_PURCHASE_MANIFEST.json, with purchase_status NOT_PURCHASED.

Current public tier rates are ¥330/month (individual self-use/academic), ¥6,600/month (corporate self-use), and ¥19,800/month (external distribution), each displayed tax-included. Twelve-month displayed totals are ¥3,960, ¥79,200, and ¥237,600. No checkout was opened. The public page says the formal total is confirmed after account-address entry.

The current DataCube FAQ says analysis results alone are within self-use, while data used as support or provided in reconstructable form is external distribution. The exact category for the planned public file hashes, public schema, coverage counts, and an unaffiliated individual research project remains unresolved. See JPX_LICENSE_CLARIFICATION_DRAFT_2026-10-04.md (not sent). The FAQ states 60 days and five download attempts; the manual describes direct-to-device downloads. No separate local-copy retention period was found.

The outcome-blind local validator and synthetic tests are now available in DATACUBE_LOCAL_QUALIFICATION_RUNBOOK.md, validate_datacube_2025.py, and ../implementation/test_datacube_validator.py. The 2025 date/contract table is a derived metadata calendar and requires independent validation.

Integrity correction: one public JPX 2025 futures quote snippet was exposed in a search result during this run. No values were retained or analyzed, but the line must not be called outcome-unviewed. No DataCube target file or 2026 market file was accessed. See OUTCOME_ACCESS_INCIDENT_2026-10-04.md. Keep the confirmation locked; final Packet A PASS is blocked pending owner disposition.
