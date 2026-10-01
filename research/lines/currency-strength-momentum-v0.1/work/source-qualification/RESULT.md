# Packet C — Source Qualification Result

## Status

- Execution: **SUCCESS** — all eight workstreams were completed and assessed.
- Qualification result: **PARTIAL_WITH_GAPS**.
- Evidence validity: **PARTIAL** because a web-search result incidentally exposed individual current exchange-rate observations; those values were not copied into this report, compared, or used.
- Scientific status: **NOT_APPLICABLE**. No hypothesis test or market-outcome analysis was run.
- Market-outcome gate: **CLOSED**. No full-history retrieval, strength ranking, forward return, strategy P/L, Sharpe, or parameter/period selection was performed.

## Authority and refs

- User-pinned proposal ref: `36240da15fc83120d12d081c227f3e0dd8badaaa`.
- Fresh main SHA: `1bba695ea252863c3b7366b8b910aa36e211c325`.
- At execution, the architecture proposal remained open as draft PR #31; its head had advanced to `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`. This work is based on the exact user-pinned ref and targets the architecture branch as a stacked PR.
- The branch is restricted to `research/lines/currency-strength-momentum-v0.1/work/source-qualification/**`.

Fresh required reads: repository README, `docs/RESEARCH_PRINCIPLES.md`, `schema/v0.1/README.md`, line README, `ARCHITECTURE_REVIEW_2026-10-01.md`, `SPEC-CSM-002-v01.md`, `DEC-CSM-002.md`, this Packet, and `references/SOURCE_REVIEW_2026-10-01.md`. The older `DATA-CSM-001.md` was reviewed as provisional context only, not treated as an execution contract.

## Qualified minimal route

The minimal candidate is the official ECB EXR SDMX route for the seven daily series in `source-lock.json`. In the official dataset metadata, the foreign currency is `CURRENCY`, the euro is `CURRENCY_DENOM`, and the rate is therefore foreign-currency units per one EUR. ECB codelists resolve `SP00` as Spot, suffix `A` as the code label “Average”, and status `A` as a normal value. “Average” is only the codelist label; this review does not interpret it as an average of bid and ask or as an intraday averaging rule.

For all seven probe responses, `SOURCE_AGENCY=4F0`; the official ECB `CL_ORGANISATION` codelist maps `4F0` to European Central Bank (ECB). The probe found the expected frequency, currency/base dimensions, unit label, multiplier, precision metadata, and 32-column CSV schema. Each series returned all 21 expected operating dates in November 2009, each with status `A`.

This qualifies the source identity, schema, and a bounded route/calendar example. It does **not** qualify complete coverage from November 2009 through September 2026.

## Time, history, and calendar

The November 2009 response metadata includes a legacy title-complement label of “2.15 pm (C.E.T.)”. The current ECB framework, dated 23 June 2026, describes the current setting around 14:10 CET and publication around 16:00 CET, while noting that input methods can vary with market conditions. This does not establish the historical observation, dissemination, or revision time for the full sample. Exact historical point-in-time availability, method continuity, and vintage/republication history remain **UNKNOWN**. Treat all daily records as date-only reference associations; no same-day tradability or information-set claim is supported.

The expected calendar is the weekday calendar excluding New Year’s Day, Good Friday, Easter Monday, 1 May, Christmas Day, and 26 December, under the ECB’s long-term TARGET calendar rule from 2002 until further notice. Its fixed range is 2009-11-01 through 2026-09-30, with 4,331 expected open dates. Calendar month-ends are determined from this rule, independently of observed prices. The calendar is not evidence that every expected observation exists. A missing expected open date is a data gap; an excluded weekend/holiday is scheduled closure. Do not fill gaps. A date outside this calendar is an unexpected observation and must be reviewed.

## Rights and capture decision

The official series agency has been resolved to the ECB. The ECB/ESCB statistics reuse policy permits free reuse of publicly released statistics in standard format subject to attribution, preservation of the official values/metadata without alteration, and the stated disclaimer; it excludes third-party data and notes that revisions may change statistics. The official endpoint returned standard CSV. On that evidence, a cited, byte-preserved raw ECB CSV snapshot is suitable for public capture under the policy. Derived data would need a clear source citation and a documented transformation; no derived market data is included here.

This qualification PR contains metadata, hashes, and code only. The seven exact probe responses were retained byte-for-byte in local scratch at `csm-source-qualification/probe-snapshot/`; the raw CSVs are not committed. The response sizes and SHA-256 hashes are in `PROBE_RECEIPT.md` and `probe-metadata.json`. This keeps the qualification artifacts free of displayed observation values. If a durable public snapshot is needed at the later authorized execution stage, preserve the original CSV bytes and attach the ECB citation and retrieval receipt.

No author paper or workbook was redistributed. Other providers’ reuse permissions are recorded as UNKNOWN where not resolved in this review.

## Source alternatives

`SOURCE_MATRIX.csv` compares ECB, BIS bilateral and effective-rate data, Federal Reserve H.10, FRED DEXUSEU, Dukascopy, OANDA, and the Zhang author factor-data page across the Packet’s fields. Their unknowns are explicit. No alternative provider was substituted for ECB. The existing provisional `DATA-CSM-001.md` statement that the ECB series is uniformly an average of buying and selling rates is overbroad: the suffix codelist label does not support that interpretation, and the current framework says input methods vary. The planned first date in that provisional record also remains unverified by this bounded probe.

## Execution record and incident

The only market-data requests performed by the metadata probe were for 2009-11-01 through 2009-11-30 for the seven fixed ECB keys. Two completed batches and one final audited batch queried this same bounded interval; no request extended the interval. The final batch completed at `2026-10-01T08:20:40Z`. The metadata-only probe script emits dates, status, dimensions, safe series metadata, sizes, and hashes, but not `OBS_VALUE` contents.

Separately, an official ECB currency-converter search result and a FRED series search result incidentally displayed individual observations. This was an unintended exposure during source discovery. The observations were not recorded, reproduced here, cross-compared, or used for analysis. No outcome metric was computed. This incident makes evidence validity **PARTIAL** and must be disclosed to the integrator before any outcome-access decision.

## Completion matrix

| Packet workstream | Status | Evidence / remaining limit |
|---|---|---|
| ECB exact keys, quote direction, dimensions, codes, endpoint and fallback transport | PASS | Official API/codelists and bounded schema; no full-history test |
| Historical fixing/publication method, revisions, CET/DST, vintages | GAP | Legacy 2009 metadata conflicts with current framework timing; historical availability/vintage unknown |
| Expected TARGET operating-day calendar and hash | PASS | Official long-term rule; deterministic date-only grid |
| Fixed bounded probe, status/unit/schema and receipt | PASS | 7/7 series, 21/21 expected dates each, all status A |
| Source lock and parser/missing/revision semantics | PASS | Frozen in `source-lock.json`; requires revalidation against any later schema change |
| Provider comparison | PASS | Completed; unresolved fields remain UNKNOWN, no substitutions |
| Per-series ECB provenance and reuse assessment | PASS | All seven map to ECB agency 4F0; standard CSV reuse with citation/no modification |
| Minimal route, blockers, and human choices | PASS | Route is reference-only; full-coverage and outcome gates remain closed |

## Blocking gaps and next gate

1. At an explicitly authorized X execution, verify the entire fixed history, actual missing/duplicate/status distribution, revisions, and schema against this lock. Do not infer full-history continuity from the probe.
2. Obtain an authoritative historical publication/vintage answer or retain date-only/reference-association interpretation and document the unresolved timing.
3. Confirm whether the downstream analysis requires pair conversions, factor sources, or financing assumptions; these are not source substitutions and are outside this qualification.
4. Make the integrator aware of the search-snippet exposure. Human freeze and independent audit requirements remain in force.

## Deliverables

- `RESULT.md`
- `SOURCE_MATRIX.csv`
- `source-lock.json`
- `expected-calendar.json`
- `PROBE_RECEIPT.md`
- `probe-metadata.json`
- `build_expected_calendar.py`
- `probe_ecb_metadata.py`

## Source references

- ECB exchange-rate reference framework (23 June 2026): https://www.ecb.europa.eu/stats/pdf/exchange/Frameworkfortheeuroforeignexchangereferencerates.en.pdf
- ECB long-term TARGET calendar decision (14 December 2000): https://www.ecb.europa.eu/press/pr/date/2000/html/pr001214_4.en.html
- ECB T2: https://www.ecb.europa.eu/paym/target/t2/html/index.en.html
- ECB SDMX API: https://data.ecb.europa.eu/help/api/data
- ECB EXR data API: https://data-api.ecb.europa.eu/service/data/EXR/
- ECB organization codelist, including agency code 4F0: https://data-api.ecb.europa.eu/service/codelist/ECB/CL_ORGANISATION/1.0?references=none
- ECB/ESCB statistics reuse policy: https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html
- ECB copyright and disclaimer: https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html
- BIS bilateral exchange rates: https://data.bis.org/topics/XRU
- BIS effective exchange rates: https://data.bis.org/topics/EER?lang=en
- Federal Reserve H.10: https://www.federalreserve.gov/releases/h10/hist/
- FRED DEXUSEU: https://fred.stlouisfed.org/series/DEXUSEU
- FRED API terms: https://fred.stlouisfed.org/docs/api/terms_of_use.html
- FRED legal: https://fred.stlouisfed.org/legal/
- Dukascopy historical data: https://www.dukascopy.com/wiki/en/development/data-export/
- Dukascopy terms: https://www.dukascopy.com/swiss/sk/legal-pages/terms-of-use/
- OANDA v20 introduction: https://developer.oanda.com/rest-live-v20/introduction/
- OANDA pricing endpoint: https://developer.oanda.com/rest-live-v20/pricing-ep/
- Zhang author data page: https://sites.google.com/view/zhangshaojun/data
