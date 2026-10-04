# Packet A acquisition readiness — 2026-10-04

This is an append-only current-read addendum to the historical PACKET_A_RESULT_2026-10-05.md. The earlier result remains intact as a record of its scope and findings.

## Classification

**PARTIAL_WITH_GAPS / WAITING_FOR_JPX_LICENSE_CLARIFICATION**

This is a pre-purchase readiness update, not a Packet A source PASS. Product-page metadata is qualified at the catalog level. No raw DataCube files exist in this work environment and no target-file outcome was calculated. During this Work run, a JPX public search result exposed a 2025 futures quotation snippet. The research line is therefore not outcome-unviewed; see OUTCOME_ACCESS_INCIDENT_2026-10-04.md. No quote values were copied, calculated, or used.

## Fresh official DataCube product read

Directly reviewed the current public J-Quants DataCube product page, tick specification, provider list, period/pricing page, terms, usage FAQ, download FAQ, and user manual on 2026-10-04.

- Product: Financial Derivatives Information / Tick / 日経225mini　歩み値（ティック）.
- Public series/product ID: future_tick_19_YYYYMM; the route is a shared series page with month-based period selection. The public catalog does not expose twelve separate month-specific page IDs.
- Target periods: 2025-01 through 2025-12, one month per selection, each explicitly listed in DATACUBE_2025_PURCHASE_MANIFEST.json.
- Product/index segment: 19.
- Historical product coverage starts 2006-07. The product page describes monthly selection and a monthly update by the fifth business day.
- The specification lists the 11 futures tick fields and says headers from 2022-07 are lower-case; it defines Time as HHMMSSmmm and No as execution order ascending within trade date/security code. It also says No may be nonconsecutive. The specification does not state the file timezone.
- Schema is declared in the DataCube specification. The actual downloaded wrapper/extension was not tested because no sample or raw market file was downloaded.

The manifest has all twelve periods with the same confirmed product series ID and official page route, the month-specific selector dates, displayed tier prices, check time, and purchase_status=NOT_PURCHASED. This is an exact series/month selection manifest, not a fabricated set of distinct SKU IDs.

## Current displayed cost

| Published use option | Monthly price (tax included) | 12-month displayed total |
|---|---:|---:|
| Personal self-use / academic use | ¥330 | ¥3,960 |
| Corporate self-use | ¥6,600 | ¥79,200 |
| External distribution | ¥19,800 | ¥237,600 |

The product card marks each rate as tax-included. The product page says the formal checkout amount is confirmed after account-address entry, which was not entered. Terms allow bank transfer or credit card; the purchaser bears any bank-transfer fee.

## License and publication boundary

The current DataCube terms define:

- Personal self-use: individual, no business use, private-purpose-only; making provider information available on the public internet does not fit this category.
- Corporate self-use: information used only by the customer and not supplied for third-party use.
- Academic use: research only by a non-profit research organization or an individual belonging to one; published research results must not allow reconstruction of provider information.
- External distribution: uses outside the preceding categories.

The current FAQ adds that providing analysis or judgment results alone is within self-use; providing the analyzed data as support or in reconstructable form is external distribution. That language supports publication of non-reconstructable aggregate statistics, but does not explicitly classify the requested public file hashes, schema, coverage counts, and an individual research project with no nonprofit affiliation. It also does not expressly say whether those specific metadata items count as analysis results.

Accordingly, the purchase option and public-release permission remain LICENSE_PUBLICATION_BOUNDARY_UNRESOLVED. The appropriate JPX Client Services contact and complete Japanese/English inquiry draft are in JPX_LICENSE_CLARIFICATION_DRAFT_2026-10-04.md. No inquiry was sent.

## Download and local retention

The current DataCube FAQ says a purchased file is downloadable for 60 days from purchase and permits up to five download attempts. Additional attempts are not granted; a repeat purchase is required. The manual says purchased files download directly to the user's device. No separate local-copy retention limit was found on the public pages reviewed. The runbook treats local-only storage as a project hard boundary and asks JPX about the local retention/backup rule.

## Local validator and pass controls

validate_datacube_2025.py is a local-only, standard-library validator. It reads local CSV/ZIP files and writes only SOURCE_QUALIFICATION_RECEIPT.json. The receipt includes file names/relative names, byte sizes, SHA-256, schema fingerprint and match, row/date ranges, index and contract-month metadata, SCO counts, sequence diagnostics, expected front-contract presence, the three frozen boundary-window coverage counts, and unavailable dates with non-price reasons. It emits no header names, raw prices, or row-level records.

It rejects out-of-scope 2024/2026 trade/execution dates, a schema mismatch, index/product mismatch, missing or duplicate sequence IDs, out-of-order sequence IDs, missing expected contract months, and systemic ambiguity. It records individual boundary gaps as unavailable dates, which do not fail the source gate by themselves. It does not calculate any outcome measure.

The 2025 date/contract calendar is public metadata, not market data. It applies JPX's TSE closure rule, the Cabinet Office holiday list, and JPX's Nikkei 225 mini quarterly expiry rule to create TSE_2025_EXPECTED_CONTRACTS.csv. The quarter-front intervals in that file are calculated from JPX's rule and the 2025 business calendar; they are not an independently downloaded 2025 JPX schedule. Independent review must validate them before any PASS. The expected sequence is 202503 through 2025-03-13, 202506 from 2025-03-14 through 2025-06-12, 202509 from 2025-06-13 through 2025-09-11, 202512 from 2025-09-12 through 2025-12-11, and 202603 from 2025-12-12 onward. A 202603 contract label in a 2025 execution row is not 2026 market data.

The validator will not auto-confirm timezone, license, or independent review. Packet A can become PASS only if all twelve monthly files/hashes, exact schema, product/index, 2025-only execution/trade dates, explicit timezone confirmation, sequence semantics, boundary evaluation, no systemic ambiguity, JPX license/publication resolution, and independent review PASS are all present.

## Official pages checked

- Product page/series ID and current public price card: https://dc.jpx-jquants.com/ja/product/future_tick_19_YYYYMM
- Futures tick schema: https://dc.jpx-jquants.com/ja/spec/dataspec/fin_derivatives/tick/futures
- Mini tick availability list: https://dc.jpx-jquants.com/ja/spec/dataspec/fin_derivatives/tick/futures/deribatibu-mi-risuto
- Terms: https://dc.jpx-jquants.com/ja/terms-of-service
- Usage FAQ: https://dc.jpx-jquants.com/ja/spec/faq/usage
- Download FAQ and manual: https://dc.jpx-jquants.com/ja/spec/faq/data and https://dc.jpx-jquants.com/ja/spec/manual/download_data
- JPX Client Services identification: https://www.jpx.co.jp/markets/other-data-services/j-quants-datacube/
- TSE closure and Nikkei 225 mini contract rules: https://www.jpx.co.jp/english/equities/trading/domestic/01.html and https://www.jpx.co.jp/derivatives/products/domestic/225mini/01.html
- Cabinet Office holiday list: https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv

## Verification and boundaries

- Synthetic tests: 14 passed locally, using generated fixtures only.
- Existing PR CI discovers work/implementation/test_*.py; the added safety suite is included by that workflow.
- No purchase or checkout.
- No raw DataCube file or sample download.
- No raw file, row, mapped point, or reconstructable extract uploaded.
- One public JPX 2025 futures quotation snippet was exposed in a search result; this is recorded as an outcome-access incident. No 2025 price-return, direction, correlation, regression, P&L, best/worst-date, or other market-outcome calculation was performed.
- No 2026 market-data file/product was obtained or parsed.
- Frozen hypothesis, specification, thresholds, filters, and sample gates were not changed.
- Packet A final PASS is locked pending research-owner disposition of the outcome-access incident.

## Human handoff

1. Submit the prepared inquiry to JPX Client Services and wait for a written category/publication answer.
2. After the answer, select the confirmed use option and purchase only the twelve listed 2025 monthly periods; download directly to a local, non-synced PC folder.
3. Run the local validator, keep the raw files and initial receipt local, then obtain independent review before any source PASS decision.
