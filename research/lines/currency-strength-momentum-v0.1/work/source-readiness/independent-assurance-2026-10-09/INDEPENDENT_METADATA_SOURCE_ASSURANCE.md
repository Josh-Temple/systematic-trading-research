---
id: CSM-ECB-METADATA-INDEPENDENT-ASSURANCE-20261009-C
type: IndependentAudit
research_line_id: RL-CSM-001
created_at: 2026-10-09
status: PARTIAL_WITH_GAPS
scientific_status: NOT_APPLICABLE
market_outcome_access: false
scope: metadata_only_existing_receipt
reviewed_pr: 53
reviewed_head: dbe9574e2d03d8a34e099931078ba2de43c7606c
integration_pr: 37
integration_head: 9162cae4f2e64ee3da07517f12a16092cc170161
---

# Independent ECB seven-series metadata-only assurance — C, 2026-10-09

## Decision and boundaries

**Overall: PARTIAL_WITH_GAPS; archived metadata consistency: PASS_SCOPED; source/outcome execution permission: BLOCKED.** This is independent review of an already executed metadata-only acquisition and its recorded CI evidence, **not** a new ECB acquisition, prospective source validation, source-vintage reconstruction, independent live data rerun, or scientific/market-outcome PASS. The frozen retrospective latest-vintage claim must not be enlarged to a point-in-time, tradability, causal, or profitability claim.

- PR #53: [head `dbe9574e2d03d8a34e099931078ba2de43c7606c`](https://github.com/Josh-Temple/systematic-trading-research/pull/53), OPEN/DRAFT at review and before saving; base `work/csm-integration-20261001`.
- PR #37: [head `9162cae4f2e64ee3da07517f12a16092cc170161`](https://github.com/Josh-Temple/systematic-trading-research/pull/37), OPEN/DRAFT; **I2 BLOCKED**, `market_outcome_access=false`, HYP-CSM-002 UNTESTED.
- Reviewed receipt: `work/source-readiness/SAFE_RECEIPT.json`, Git blob `0e27706cdb5f775d7bd302c56605a6800fa4da57`.
- Reviewed checker: `work/source-readiness/source_readiness.py`, Git blob `8fc080852d97120f6ee77be25fe10a56c8286f06`; reviewed workflow blob `ca192a3aa3a6ae960355368a98543aa01c304f9e`. Both checker and workflow blobs match the CI's earlier `3d722f2f57e226ce4eb90193dc35f61f89c743ba` head **exactly**. The checked-in wrapped SAFE_RECEIPT did not yet exist at the earlier run head; do not claim it was run as an input.

## Immutable evidence linkage

| Item | Verified safe identity or observation |
| --- | --- |
| Frozen Packet C source commit | `9870c710c3cba7bb9226c9eee8ec36687b96fd9d` |
| Source-lock ID | `CSM-SOURCE-LOCK-ECB-001` |
| Source-lock JSON SHA-256 (CI `sha256sum -c` OK) | `ebfa5782568709ac026bd614f3a86494e2119ab73611b92c5ff740ef94118a71` |
| Probe metadata SHA-256 (CI OK) | `1a698a4cd6ffd26afd11ef40a1e23936216614b705bb9955b1bd15d4d6631533` |
| Locked expected-calendar JSON SHA-256 (CI OK) | `6f0b54411037c65e0e6b054018bd8a5745e54853bf13af30b1e6252ef7b778d4` |
| Passed metadata CI | [run 37167525175](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37167525175), job 111333492790, success |
| Passed CI head SHA | `3d722f2f57e226ce4eb90193dc35f61f89c743ba` |
| Inner CI receipt SHA-256 | `34287530a0ce3072cf3aa5781063ce6732c79a366fabfaf50c6cf1e4358c759f` — checked-in envelope matches exact value printed by CI |
| GitHub artifact identity | ID `11290625395`, `csm-source-readiness-metadata`; ZIP digest `sha256:423d1457c2997606742a5585e7cc665583384580b77dad30ef7a7f46f7382447`, agrees with recorded envelope and GitHub Actions artifact metadata |
| Historical initial failure | [run 37167323298](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37167323298), failure; seven series each returned 10 H placeholders classified as unreviewed unexpected dates, overall `PARTIAL_WITH_GAPS`, receipt `5734c0ed874d9c5362210e75e27c6a337e437e7eef7daae9aca902b682a24835`. Preserved. |

**Comparison method:** Live GitHub blob reads at the exact above commit refs; Actions job statuses and filtered job logs (not mere README assertions); GitHub's reported artifact identity; programmatic metadata-field and raw-response-hash comparison of all seven series against lines in the passed CI log. The seven checked-in per-series raw-response SHA-256 hashes all occurred in that CI log, and the CI-reported inner receipt SHA-256 agrees with the envelope. This does **not** prove the original raw bytes anew: no raw-response download or independently recalculated raw-byte hash was permitted. The ZIP was identified via Actions metadata but its member was **not independently extracted and byte-compared**.

## Seven locked series and fixed grid

- ECB official SDMX EXR daily keys, EUR denomination: `D.AUD.EUR.SP00.A`, `D.CAD.EUR.SP00.A`, `D.CHF.EUR.SP00.A`, `D.GBP.EUR.SP00.A`, `D.JPY.EUR.SP00.A`, `D.NZD.EUR.SP00.A`, `D.USD.EUR.SP00.A`. Exact key set matches Packet C source-lock; source agency `4F0` and expected `D/{CCY}/EUR/SP00/A` dimensions are checked by the checker. Source interval `2009-11-01` to `2026-09-30`.
- Frozen expected-open date count `4331`, first `2009-11-02`, last `2026-09-30`. Independently reconstructed the full date grid from Gregorian weekdays, Western Good Friday/Easter Monday and TARGET closed dates (1 Jan, 1 May, 25 Dec, 26 Dec). **All 4,331 generated dates matched the exact expected_open_dates list by position**; the list contains 4,331 distinct dates.
- Archived receipt for **each** of seven series: `PASS`; HTTP 200, content type `text/csv`, `schema_match=true`, 4,341 raw rows = 4,331 `OBS_STATUS=A` observation rows plus 10 `OBS_STATUS=H` blanks. Unique observation dates 4,331; `duplicate_count=0`, `missing_expected_count=0`, `unexpected_observation_date_count=0`, `invalid_holiday_placeholder_count=0`, `dimension_mismatch_count=0`, `source_agency_mismatch_count=0`. All four validity-failure counts on normal-value fields are zero. Same raw-status counts and schema SHA reported for each series. These are metadata checks, not permission to inspect the values.
- Reviewed H dates: `2009-12-25`, `2010-01-01`, `2010-04-02`, `2010-04-05`, `2011-04-22`, `2011-04-25`, `2011-12-26`, `2012-04-06`, `2012-04-09`, `2012-05-01`. Each is independently a locked TARGET-closed date; H has blank value and is excluded from expected-open observation coverage.
- Source-calendar documentary authority: [ECB long-term TARGET closure decision](https://www.ecb.europa.eu/press/pr/date/2000/html/pr001214_4.en.html), [T2 operating schedule](https://www.ecb.europa.eu/paym/target/t2/html/index.en.html), [ECB FX reference rate methodology](https://data.ecb.europa.eu/methodology/exchange-rates). The contemporary description of rates around 16:00 CET does **not** supply historical point-in-time vintage/release timestamps.

## Independent finding and unresolved gaps

1. **Observed H rows are accounted for, but future H acceptance is not strictly range-bound.** In current `source_readiness.py`, `elif status == "H": if period not in expected_set and value_text == "": ...` does not explicitly require that the date belongs to the locked source interval or a fully enumerated set of valid TARGET closure days. A synthetic out-of-window blank H row could therefore be counted as accepted. This does **not** invalidate the observed 10 reviewed H dates, but the published assurance rule and implementation are not equivalent for adversarial/future input. No code change is authorized in this C audit. Remedy outside allowlist: fail closed for H date outside [START, END], require a parsed canonical date and membership in an independently locked closed-day set; add offline negative fixtures for out-of-window, malformed and expected-open H. Reaudit exact code SHA before any gate change.
2. **Inner artifact not independently downloaded.** CI job steps passed, GitHub artifact digest, raw-hash field matches and in-repo envelope agree; actual uploaded member bytes were not retrieved. This is consistency evidence, not independent source capture.
3. **Exposure assertion has limited force.** Checked-in receipt field allowlist was inspected: no `"OBS_VALUE"` data key or direct observation-value field, `market_outcome_access=false`, `ranking_computed=false`, `returns_computed=false`, `raw_responses_persisted=false`. The checker reads value text transiently to calculate only validity counts. Its boolean output fields and log substring guard alone are not a cryptographic proof of all historical runner memory/process behavior.
4. **Historical vintage and dissemination** remain unverified. The supported estimand is retrospective/latest-vintage/synchronous association only; no historical point-in-time, real-time information set, broker execution, net profitability, or causal interpretation follows.
5. **Incidental search exposure disclosure:** A broad search for official ECB methodology during this review produced web search snippets which also contained current exchange-rate quotations. These figures were not transcribed into the report, used in calculations, compared with the research data, or used to adjust the specification; nonetheless the exposure is disclosed rather than describing this reviewer as perfectly blind to all market quotes. The source artifact inspection itself remained metadata-only. Any future independent outcome evaluator should be separate and should not rely on this reviewer's unrestricted blindness.
6. **Review is not a full test rerun.** Offline deterministic calendar-list equality, seven-series receipt structure and seven hash-field/log matches were executed in-session. The historical networked full-history checker was **not re-run**, because that would reacquire market-valued data without authorization. No new ECB data API request or broker/XM/MT5 request was made. No raw OBS_VALUE CSV was downloaded or opened.

## Required readback and E/D handoff

**Adopt now:** immutable archived metadata consistency and independently verified fixed-calendar equivalence only (`PASS_SCOPED`); preserve initial negative receipt/run and the two original CI heads. Historical CI `overall_status=PASS` is valid *only* as reported metadata-only acquisition readiness for that historical fixed snapshot.

**Hold:** source-readiness parser equivalence for untrusted future H rows (`PARTIAL_WITH_GAPS`), byte-independent verification of ZIP member, historical point-in-time/vintage claims, all formal I2/human/trusted-key/isolated-runner approvals, and all market/outcome access (`BLOCKED`). No retuning of currency sets, dates or specifications and no raw data acquisition. CSM and FXNS remain separate.

**Safety of saving this report:** The existing `csm-source-readiness.yml` pull-request path trigger covers `work/source-readiness/**`, including this report. The report's commit must therefore include `[skip ci]` to prevent an otherwise triggered ECB live full-history fetch. This safety skip is not a passing CI result; this audit is **documentation only**, and E must not remove the skip or merge/trigger the acquisition workflow until a separately authorized offline-only route exists.

**Only changed path under this C branch:** `research/lines/currency-strength-momentum-v0.1/work/source-readiness/independent-assurance-2026-10-09/INDEPENDENT_METADATA_SOURCE_ASSURANCE.md`.

**E recommendation: HOLD any source/outcome gate promotion.** Include C's bounded metadata PASS_SCOPED and specific parser and artifact-check gaps in E's disposition. D's independent I2 blocking review must proceed without relying on this source audit as an I2 approval.
