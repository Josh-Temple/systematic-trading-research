# DataCube 2025 local-only acquisition and Packet A runbook

Checked against the public JPX DataCube site on 2026-10-04. This runbook does not authorize payment or market-outcome inspection.

Integrity notice: a JPX public-search result exposed a 2025 futures quotation snippet during this Work run. The research line is marked outcome-blindness-compromised in OUTCOME_ACCESS_INCIDENT_2026-10-04.md. No quote values are recorded or used. The validator can qualify local source metadata only; its final Packet A PASS gate is locked for this run.

## Status before acquisition

- Product series and its monthly selection mechanism are identified.
- Twelve monthly target periods are recorded in DATACUBE_2025_PURCHASE_MANIFEST.json.
- Purchase status is NOT_PURCHASED.
- License/publication classification is WAITING_FOR_JPX_LICENSE_CLARIFICATION.
- Do not buy or publish a receipt until JPX responds to the inquiry draft.
- No 2025 DataCube target files or target rows have been accessed. A separate public JPX 2025 quote snippet was exposed; the line is not represented as outcome-unviewed.
- No 2026 market data has been accessed.

## Official product to select

On the official product page, select “日経225mini　歩み値（ティック）”, product route/series ID future_tick_19_YYYYMM. The public page has one month-based period selector; the catalog does not expose twelve distinct month-specific URLs. Select one calendar month at a time for January through December 2025.

The page describes monthly selection, history from 2006-07, and a monthly update by the fifth business day. The specification defines the post-July-2022 lower-case CSV fields and sequence number semantics. No sample/raw file was opened or downloaded.

## Displayed prices

Public product cards show tax-included monthly prices:

| DataCube use option | Per month | 12 months |
|---|---:|---:|
| Individual self-use / academic use | ¥330 | ¥3,960 |
| Corporate self-use | ¥6,600 | ¥79,200 |
| External distribution | ¥19,800 | ¥237,600 |

The exact applicable option is not selected because the published terms and FAQ do not expressly classify the planned public source hash, schema, and coverage metadata for an unaffiliated individual research project. The FAQ says analysis results alone can be provided within self-use, while source data used as supporting material or data provided in reconstructable form is external distribution. The JPX inquiry draft asks which tier covers this exact output list. The product page says the formal total is confirmed after account-address entry; these figures are the current public display, not a checkout quote.

JPX terms list bank transfer and credit card as payment methods. A bank-transfer fee is borne by the purchaser. Do not proceed to payment before the written category answer and the human's purchase decision.

## Download timing and local storage

The current FAQ states that purchased files can be downloaded for 60 days from purchase, up to five times; JPX does not add attempts after that limit and says another purchase is required. The user manual says purchased files download directly to the user's device.

The reviewed public pages do not specify a separate retention period for an already-downloaded local copy or local backup. Ask JPX if a contractual limit is required. This research line requires raw files to remain on the human's local PC and excludes them from Work/Cloud/ChatGPT, Google Drive, public GitHub, and cloud-synced folders.

## Local directory

Create a directory outside cloud synchronization, for example:

~~~text
<local-only-root>/jp225_imom_2025_raw/
  2025-01/
  2025-02/
  ...
  2025-12/
~~~

Save each paid monthly download in its matching folder. Keep invoices and account records separately. Do not add raw CSV/ZIP files or row-level content to the repository. The validator accepts local .csv and .zip files containing CSV members.

## Run the outcome-blind validator

From the repository root, after local acquisition:

~~~bash
python research/lines/jp225-intraday-momentum-v0.1/work/source-qualification/validate_datacube_2025.py \
  --raw-dir "/absolute/local/path/jp225_imom_2025_raw"
~~~

The only report created by the validator is SOURCE_QUALIFICATION_RECEIPT.json in the raw directory. It records filenames/relative names, byte sizes, SHA-256, header fingerprint/schema match, row and date coverage metadata, product/contract/category counts, sequence diagnostics, expected contract presence, the three frozen boundary-window coverage counts, and unavailable dates with non-price reasons. It emits no header names or row-level values.

The validator reads displayed clock values for the three frozen +60-second windows, but will label timezone semantics UNCONFIRMED unless a human records a vendor-backed JST attestation. The product specification page defines Time as HHMMSSmmm but does not itself label a timezone. The inquiry draft also asks JPX to confirm the field timezone.

The expected date and quarterly front-contract map is the public-metadata file TSE_2025_EXPECTED_CONTRACTS.csv. It is derived from JPX TSE closure rules, the Cabinet Office holiday list, and JPX's Nikkei 225 mini quarterly expiry rule. The 2025 quarter-front periods are a calendar calculation from those rules, not a downloaded JPX 2025 schedule file; an independent reviewer must validate this map before PASS. It is not market price data.

## Interpretation of a receipt

- A boundary with no qualifying observation is listed as an unavailable date. Individual unavailable dates do not fail source qualification.
- Missing, duplicate, or nonmonotonic sequence values block deterministic ordering. JPX states sequence numbers can be nonconsecutive; the validator does not treat a skipped integer as an error.
- A contract-month label of 202603 may appear in a 2025 row because it is the quarterly contract identifier. It is not a 2026 market-data file.
- A timezone or license attestation is not inferred from metadata. A synthetic test pass is not a source-qualification pass.
- The validator leaves packet_a_pass=false for this run because the research-line outcome-blindness incident is unresolved. A source-only qualification receipt cannot repair that integrity incident. Independently, the 12 monthly files, schema, index/product, date scope, timezone, sequence, boundary evaluation, non-ambiguity, JPX license resolution, and independent review would also have to satisfy the coded gate.
- Keep the generated receipt local until JPX resolves the publication boundary. Only then review its repository suitability and submit it as an aggregate metadata artifact.

## Frozen exclusions

The local validator does not compute price differences, returns, sign, direction, long/short labels, correlations, beta, regression, P&L, win rate, or best/worst dates. It does not access 2026 market files, download source data to a cloud workspace, change any research threshold, or modify the 2025/2026 gates.

## Official public sources

- DataCube product series, period selector, and displayed prices: https://dc.jpx-jquants.com/ja/product/future_tick_19_YYYYMM
- Futures tick field and sequence specification: https://dc.jpx-jquants.com/ja/spec/dataspec/fin_derivatives/tick/futures
- Product availability list: https://dc.jpx-jquants.com/ja/spec/dataspec/fin_derivatives/tick/futures/deribatibu-mi-risuto
- DataCube use categories: https://dc.jpx-jquants.com/ja/terms-of-service
- DataCube result-publication FAQ: https://dc.jpx-jquants.com/ja/spec/faq/usage
- Download window and attempt-limit FAQ: https://dc.jpx-jquants.com/ja/spec/faq/data
- Download manual: https://dc.jpx-jquants.com/ja/spec/manual/download_data
- JPX TSE closure rule: https://www.jpx.co.jp/english/equities/trading/domestic/01.html
- Cabinet Office public-holiday CSV: https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
- Nikkei 225 mini quarterly expiry rule: https://www.jpx.co.jp/derivatives/products/domestic/225mini/01.html
- JPX/DataCube support contact: https://dc.jpx-jquants.com/ja/contact#contact-form
