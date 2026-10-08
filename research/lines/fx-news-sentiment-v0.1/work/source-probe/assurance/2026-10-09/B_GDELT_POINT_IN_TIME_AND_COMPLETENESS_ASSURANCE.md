# B — GDELT DOC point-in-time and completeness boundary assurance (2026-10-09 JST)

**Result:** `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED` (source suitability for formal FXNS use: **BLOCKED**).  
**Research line:** FX News Sentiment (FXNS), `UNTESTED`, `SPEC-FXNS-001-v01 = PROPOSED_NOT_FROZEN`, formal cohort **CLOSED**.  
**Scope:** source-only, historically preserved GDELT DOC ArticleList artifacts plus official public specifications. No new GDELT API request or market-outcome access.

## 1. Review identity and immutable inputs

- Repository: `Josh-Temple/systematic-trading-research`.
- Canonical FXNS PR: [#63](https://github.com/Josh-Temple/systematic-trading-research/pull/63), `OPEN/DRAFT`; independently reread research branch head `202ee37d0cd3f9838b153ea361dfdeba5244a271` immediately before creating this report.
- `main` reference at review: `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` (not changed).
- Previous source-repair PR: [#68](https://github.com/Josh-Temple/systematic-trading-research/pull/68); its [Role A report](../../ROLE_A_SOURCE_QUALIFICATION_2026-10-08.md) is also included in pending PR [#74](https://github.com/Josh-Temple/systematic-trading-research/pull/74). Its patch is **not yet merged into the #63 research head** and is not silently assumed to govern that head.
- Existing source policy: `SOURCE_CONTRACT.md` blob `36dd9c9977718a8da02ae8f569cad76d4c0acd15`; `work/SOURCE_QUALIFICATION_RESULT.md` blob `829fe079a4d45edefe1347d9593f41fec34d46dd`.
- Fixed candidate query: `(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`; `mode=artlist`, `format=json`, `sort=dateasc`, `maxrecords=250`, exactly 24 hours ending at **08:00 JST**. Query ID `FXNS-DOC-QUERY-v01-candidate`. No term, pair, window, cap, provider, prompt or specification revised here.
- Evidence vs approval: this document is an independent **source-boundary audit**, not a human freeze, Packet D signoff, semantic classification, forward test, or scientific PASS.

## 2. Independently rechecked historical artifacts

Both existing GitHub raw files were read as bytes represented in UTF-8, and SHA-256 was independently recomputed and matched to their original manifests; the original files were **not rewritten**.

| Snapshot / manifest | HTTP / start→completion (UTC) | Byte count | SHA-256 from raw bytes = manifest | Git blob SHA |
| --- | --- | ---: | --- | --- |
| `runtime-20261007-exact` | 200 / 2026-10-07 03:20:01.449225 → 03:20:26.968407 | 5,962 | `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d` **MATCH** | `ff5159d91bc2ead99bbd0a669e8c8079f585d9a1` |
| `runtime-20261007-cap10` | 429 / 2026-10-07 03:20:58.787434 → 03:21:18.616094 | 444 | `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6` **MATCH** | `faca354e1d0c6bf1e7fe7a7990b6015df6023b55` |

- Snapshot 200 window: `2026-10-05T23:00:00Z` to `2026-10-06T23:00:00Z`; cutoff **2026-10-07 08:00 JST**. Actual historical acquisition finished **2026-10-07 12:20:26 JST**, **after the cutoff**. This raw file **must not** be treated as a prospective point-in-time cohort receipt.
- Direct offline inspection of saved 200 response: JSON `articles` array contains **12 English rows**, observed `seendate` string uniformly `20261006T083000Z`. Present fields are `domain,language,seendate,socialimage,sourcecountry,title,url,url_mobile`. No publisher article body was opened or used.
- Previously saved **separate** offline replay `offline_validation.json`: **12 input → 10 retained**, with **two `NORMALIZED_TITLE` exclusions**. This is a deterministic parsing/deduplication observation, not evidence of source exhaustiveness.
- Original HTTP 200 manifest status is `SOURCE_QUALIFICATION_BLOCKED` with `domain/URL mismatch`; offline replay addressed `www.` hostname normalization without retroactively changing the original attempt. Preserve this negative result.
- Snapshot 429 used the **same query and window** but `maxrecords=10`; it cannot establish whether the 250-cap snapshot was exhaustive. No retry loop or new request was run.

## 3. Documentation versus observations versus unsolved source properties

Authoritative public references inspected without calling the live API:
- [GDELT official DOC 2.0 API specification (2017)](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/): ArticleList, keyword/phrase/OR operators, `sourcelang`, requested time window, `MAXRECORDS` up to 250, and date-sort documented. Its publication-date wording does **not** by itself establish invariant first-observed DOC `seendate`.
- [GDELT official GAL announcement (2021)](https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/): GAL `date` can combine true publisher time and first-observed time. **GAL is not DOC `artlist`**, and its semantics cannot be imported into this source contract.

Each status below is one of `DOCUMENTED`, `OBSERVED`, `UNVERIFIED`, or `BLOCKED`; they are **dimension-specific**, not an overall approval.

| Dimension | Status | Concrete basis and limitation |
| --- | --- | --- |
| DOC ArticleList query operators, output mode, 250 maximum | **DOCUMENTED** | Official DOC specification supports these controls; no claim that 250 results is an exhaustive census. |
| `STARTDATETIME` / `ENDDATETIME` date filtering and date sorting | **DOCUMENTED** | Official DOC docs describe publication-after/before and `dateasc`; this is not proof of exact UTC or equal-to-endpoint handling of `seendate`. |
| Raw `seendate` field format and values | **OBSERVED** | All 12 saved JSON rows have a `YYYYMMDDTHHMMSSZ`-formatted field; a local parser interprets `Z` as UTC. |
| DOC `seendate` as immutable first-seen / pipeline-ready time | **UNVERIFIED** | No authoritative field-level guarantee or revision-controlled point-in-time receipt was established. `seendate` must not be equated with publisher publication time. |
| Publisher publication time for these DOC records | **UNVERIFIED** | Saved ArticleList provides no independently qualified publisher timestamp. No publisher pages fetched. |
| UTC and exact-start/end equality semantics of API filtering | **UNVERIFIED** | Stored rows lie strictly inside the requested interval; none tests equality. Conservative open boundaries in local validator are not a proof of endpoint implementation. |
| Actually acquired by intended pipeline before 08:00 JST | **BLOCKED** | Observed response completed 12:20 JST; historical `seendate` cannot prove a pre-08:00 successful acquisition. |
| Scoped query-result completeness and 250-cap sufficiency | **BLOCKED** | 12 results below 250 only demonstrates below-cap response size. Comparison with 10 was HTTP 429, so no valid cap/exhaustiveness assurance. |
| Indexing latency, index revisions, historical backfill and replay stability | **UNVERIFIED** | No authoritative guarantee or independent before/after index snapshot on the frozen boundary. Historical reconstruction may differ from what was observable in real time. |
| Preservation of saved HTTP200/429 raw and receipt hashes | **OBSERVED** | Independently recomputed both raw SHA-256 checksums; metadata/start/end/status/headers retained in manifests. No new acquisition. |
| Local fail-closed cap handling in source code | **OBSERVED** | Existing `normalize` rejects raw `len(articles) >= limit` before dedupe; code observation only, not a completeness certificate. |
| Removal of GDELT live acquisition from automated FXNS CI | **OBSERVED** | Research branch `.github/workflows/fxns-gdelt-source-probe.yml` blob `620581df64cf247c293781389bd7386df391f30e` invokes only `.github/scripts/fxns_offline_unittest.py` and compilation. CI run [37798966613](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798966613) / job `113385769601`: checkout, Python setup, network-denied tests, syntax compile; **no live GDELT probe step**. |

Important distinction: the inspected workflow and job steps show no GDELT-fetch step; this is **not** a general no-network attestation for GitHub checkout/setup, nor proof that third-party arbitrary Python code could not circumvent the process-level socket denial.

## 4. Validation, exclusions, and exact remaining gate

**This worker's direct verifications:**
1. Re-read PR #63, source contract/qualification result, both manifests, both raw responses, separate offline replay, current probe code and research-branch workflow.
2. Independently recomputed 5,962-byte and 444-byte raw SHA-256 hashes against stored manifests: **2/2 MATCH**.
3. Parsed saved historical JSON to check 12 rows, required fields, English language and reported `seendate` format. No headlines were classified or publisher content accessed.
4. Read official public DOC/GAL specifications. Did **not** query `api.gdeltproject.org`.
5. Read the successful Actions job step summaries and log from run `37798966613`: **83 tests / 0 failures / 0 errors / 0 skips**, on the *different*, unmerged PR #74 head `9ebfc57dd4060825da189b196dd044b6ffaead4f`. The job did **not** execute the live GDELT probe. **CI-LOG-REVIEWED, NOT_RERUN here**; not a source or scientific qualification.

**Deliberately not undertaken:** new live GDELT request; new retries; daily scheduling; XM/Windows/MT5 work; another provider; request-window, cap, sort or query change; market prices, real sentiment classification, returns, P&L or strategy performance; actual paper/live orders; modifying raw/manifest/source code/SPEC/prompt/schema; converting a synthetic test result into human/source approval.

**One next substantive evidence gate (requires separate explicit authorization):** an **independently reviewed, prospective point-in-time acquisition integrity receipt** for the *existing frozen candidate DOC query*: immutable record of actual pipeline receipt **before 08:00 JST**, coupled to an authoritative or separately approved qualification of DOC `seendate`, timezone/equality, index revision and scoped completeness/250-cap semantics. A later historical backfill, a <250 count, another formal document alone, or a GDELT `seendate` value cannot satisfy the gate.

**Stop conditions:** any missing pre-cutoff acquisition; unresolved first-seen/equality/completeness semantics; 429 or otherwise incomplete response; a head/raw/hash mismatch; an attempted provider substitution/query alteration; any unauthorized XM, live classification, market-outcome access or formal event issuance.

**E integration handoff:**
- Source suitability **HOLD / BLOCKED**. Keep FXNS `PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED`, `UNTESTED`, `PROPOSED_NOT_FROZEN`, cohort **CLOSED**, XM `LOCAL_XM_EXECUTION_REQUIRED` (explicitly deferred).
- Offline CI mechanics may be evaluated independently by Worker A and E, but neither this B report nor those synthetic results authorize source PASS, human freeze, Packet D PASS, or market-outcome access.
- The only change proposed by B is this standalone evidence report; **no code integration or source escalation**. Maintain historical negative evidence.

## 5. Change and access manifest

- Write allowlist: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-09/**`.
- Intended actual changed file: `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-09/B_GDELT_POINT_IN_TIME_AND_COMPLETENESS_ASSURANCE.md`.
- GitHub PR base: `research/fx-news-sentiment-v0.1`, **not `main`**.
- New live GDELT requests: **0**. New XM or market-outcome access: **0**. New ChatGPT classification invocations: **0**.
