# Packet A — Source Qualification Result — 2026-10-05

Role: independent source qualifier

Research line: jp225-intraday-momentum-v0.1

Market outcomes accessed: **NO**

2026 data accessed: **NO**

Classification: **PARTIAL_WITH_GAPS / PREPURCHASE_QUALIFICATION_COMPLETE**

Scientific result: **NOT_APPLICABLE**

## 1. Scope

This Packet A run inspected repository specifications and public JPX / J-Quants DataCube metadata only.

It did not:

- purchase or download 2025 Nikkei 225 mini tick files;
- inspect transaction prices from the target sample;
- calculate returns, signs, correlations, regression coefficients or strategy outcomes;
- access any 2026 raw market data.

## 2. Dataset identity resolved at catalog/specification level

Intended dataset family:

- provider: JPX Market Innovation & Research / J-Quants DataCube;
- category: Financial Derivatives Information;
- data type: Tick / transaction history;
- product: Nikkei 225 mini;
- purchase unit: one product × one month;
- file delivery: CSV;
- DataCube product/index segment: 19 for Nikkei 225 mini;
- historical availability covers 2025 and begins in 2006.

Public JPX sources:

- https://www.jpx.co.jp/markets/paid-info-derivatives/historical/01.html
- https://www.jpx.co.jp/markets/other-data-services/j-quants-datacube/index.html
- https://db-ec.jpx.co.jp/client_info/JPX_DLSITE/html/data_detail.pdf
- https://db-ec.jpx.co.jp/client_info/JPX_DLSITE/html/datacube_price.pdf

The public catalog confirms the product family and monthly purchase model, but the exact 2025 monthly item-page identifiers have not yet been bound to purchased files. This remains a gap.

## 3. Financial-derivatives tick schema resolved

The current DataCube specification for financial-derivatives futures exposes the fields required by the frozen mechanism:

- trade_date: trading date;
- execution_date: actual calendar execution date;
- index_type: product/index segment;
- security_code: 9-digit derivatives security code;
- time: transaction time in HHMMSSmmm;
- trade_price: transaction price;
- price_type: O / E / N semantics;
- trade_volume: executed quantity;
- No / sequence number: execution order within trade-date/security-code, ascending;
- contract_month: YYYYMM;
- sco_category: strategy-trade flag, available for 2025.

The specification states that 2025 data have millisecond-resolution transaction timestamps. The sequence-number field is sufficient to define a deterministic order when multiple executions share a displayed timestamp, provided the raw file contains a unique sequence number.

The exact timezone label for the financial-derivatives time field still needs to be confirmed against the downloaded 2025 sample/file documentation before PASS. The JPX derivatives trading-hours documentation is expressed in Japan time and the parallel DataCube derivatives specification uses Japan-time clock semantics, but Packet A will not infer product-file timezone identity from that alone.

## 4. Contract semantics resolved

JPX contract specifications confirm:

- Nikkei 225 mini day-session trading covers 08:45-15:45;
- quarterly contract months are March, June, September and December;
- last trading day is the business day preceding the second Friday of the contract month;
- a new contract month begins trading on the business day after the prior last trading day.

The DataCube tick schema also exposes contract_month=YYYYMM, so the experiment does not need to infer contract month from realized volume or price.

Official sources:

- https://www.jpx.co.jp/derivatives/products/domestic/225mini/01.html
- https://www.jpx.co.jp/derivatives/rules/last-trading-day/

## 5. Strategy-trade rows require explicit exclusion

The DataCube specification states that since September 2022 the financial-derivatives tick data include strategy-trade executions and expose sco_category.

Because strategy-leg prints are not the intended standalone price observation, Packet A fixes:

- sco_category == 0 only for frozen point-price mapping;
- sco_category == 1 excluded.

This change was made before any target market outcome access and is recorded in specification amendment v0.1.2.

## 6. Confirmation source-period boundary

JPX confirms that the last TSE trading day of 2024 was 2024-12-30 and the first trading day of 2025 was 2025-01-06.

The original predictor would otherwise require a 2024-12-30 15:30 price for the first 2025 date. Acquiring a December 2024 monthly tick file solely for that one predecessor would unnecessarily expose unused 2024 data.

Packet A therefore freezes a source-boundary rule before outcomes:

- a 2025 confirmation date requires its previous eligible TSE date to also be in 2025;
- the first 2025 TSE date is excluded without opening 2024 market data.

Official source:

- https://www.jpx.co.jp/english/corporate/news/news-releases/0061/20241202-01.html

## 7. License / storage boundary

Current DataCube terms distinguish:

- self/internal use: provider information is used only by the customer and is not supplied for third-party use;
- personal use: additionally requires an individual, no business use, private purposes only, and excludes making provider information available on the internet;
- academic use: limited to a non-profit research entity or a person belonging to such an entity; publication may not make the provider information reconstructable;
- external distribution: use that does not fit the above, including distribution to unspecified third parties over the internet.

Official terms:

- https://db-ec.jpx.co.jp/client_info/JPX_DLSITE/html/kiyaku.pdf

Conservative repository rule:

- raw purchased files: LOCAL_ONLY;
- no raw rows or reconstructable mapped prices in GitHub, ChatGPT, Drive or other cloud services;
- local deterministic processing only;
- repository receives hashes, schema/coverage metadata and non-reconstructable aggregate research artifacts only.

Remaining licensing gap:

The project intends to publish scientific result artifacts in a public GitHub repository. Whether the intended non-reconstructable aggregate outputs fit the user's purchase category should be confirmed with JPX before purchase or public result publication. Do not assume that a low-priced personal-use purchase automatically authorizes the full research publication workflow.

## 8. Current price-route observation

The current DataCube price list (from November 2025) lists financial-derivatives tick data per product/month at generic category rates, including a personal/academic tier.

This is a planning observation only. Checkout price and purchase category must be confirmed at acquisition time; no purchase was made in this Packet A run.

## 9. Raw-file and coverage requirements not yet satisfiable

Packet A requires a bound receipt containing:

- exact monthly item/file identities;
- byte sizes;
- SHA-256 of every purchased raw file;
- header/schema readback;
- product/index-type check;
- contract-month coverage;
- unique sequence-order validation;
- counts of valid rows in the four +60-second boundary windows;
- unavailable-date counts/reasons;
- no price-derived direction or return statistics.

None of those raw-file checks can be completed without actual purchased/downloaded 2025 files.

Therefore PASS is not scientifically or operationally available yet.

## 10. Gate decision

Current classification:

**PARTIAL_WITH_GAPS**

Resolved:

- correct official source family;
- product identity at catalog level;
- monthly CSV delivery;
- required schema fields;
- deterministic sequence field;
- contract-month field;
- quarterly contract rule;
- day-session coverage of all requested clocks;
- strategy-trade flag and exclusion rule;
- conservative local-only raw-data handling.

Unresolved:

1. exact 2025 monthly item/file IDs and downloaded file identities;
2. raw-file SHA-256 and bytes;
3. exact 2025 product-file timezone confirmation;
4. real boundary-window coverage;
5. uniqueness/completeness of sequence numbers in the target files;
6. final purchase/use category for a workflow that may publish non-reconstructable research outputs;
7. explicit JPX confirmation if cloud/third-party processing is ever desired.

## 11. Next allowed action

Do **not** run the one-shot 2025 confirmation.

The next allowed action is a bounded acquisition preparation step:

1. resolve/confirm the intended JPX purchase category;
2. purchase/download only the required 2025 Nikkei 225 mini tick months;
3. keep raw files local;
4. compute file hashes and coverage-only diagnostics locally;
5. write a source receipt without return/outcome calculations;
6. independently review that receipt.

Only after all remaining gaps close may Packet A become PASS and a separate confirmation gate be created.
