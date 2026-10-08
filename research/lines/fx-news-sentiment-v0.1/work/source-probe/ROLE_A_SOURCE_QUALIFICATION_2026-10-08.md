# Role A — GDELT DOC source-only qualification (2026-10-08)

## Scope / immutable baseline

- Fresh read: main `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`; PR #63 `OPEN / DRAFT`, initial source head `8d3771921fbab88ea56b913f9d6fe8d62236961c`.
- This is **source-only**. No new GDELT HTTP probe, publisher-page opening, LLM classification, EURJPY market outcome, execution, or broker action. Existing 2026-10-07 HTTP evidence is historical, **not** a prospective/cutoff-time sample.
- Changes limited to `research/lines/fx-news-sentiment-v0.1/work/source-probe/**`. Earlier raw, manifest, offline validation, CURRENT, SPEC, SOURCE_CONTRACT and prompt/schema were not modified.

## Previous bounded responses: fresh raw-byte review

| Stored attempt | HTTP | Requested window / receipt | Bytes / recalculated SHA-256 |
| --- | --- | --- | --- |
| `runtime-20261007-exact` | 200 | 2026-10-05 23:00:00 to 2026-10-06 23:00:00 UTC; retrieved starting 2026-10-07 03:20:01 UTC, completed 03:20:26 UTC | 5,962; `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d` |
| `runtime-20261007-cap10` | 429 | Identical query/window, MAXRECORDS=10; start 03:20:58 UTC, completed 03:21:18 UTC | 444; `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6` |

Fixed candidate query: `(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`; DOC `mode=artlist`, `format=json`, `sort=dateasc`, `MAXRECORDS=250`. Both raw SHA-256 values and byte counts were independently recomputed from retrieved GitHub bytes and matched existing manifests.

The HTTP 200 raw contains **12 English records**, all with `seendate=20261006T083000Z`. Previously preserved *separate* offline normalization yields 10 retained and 2 normalized-title exclusions. The historical HTTP 200 attempt's original manifest is blocked (`domain/URL mismatch` from `www.` hostname handling); later offline validation does not rewrite the original request. The 429 comparison is a rate-limit error, **not** valid cap-completeness evidence; no retry was performed here.

## Documentation and independent source dimensions

GDELT primary documents read:
- https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/

| Dimension | Source-only finding | Classification |
| --- | --- | --- |
| Parameter names / query operators | Official DOC API documents Boolean OR, phrase matching, original-language filtering, STARTDATETIME/ENDDATETIME and ArtList MAXRECORDS up to 250. | DOCUMENTED PARAMETERS ONLY |
| Timestamp representation | Raw `seendate` matches `YYYYMMDDTHHMMSSZ` and local parser interprets Z as UTC. The official START/END wording is framed as publication after/before; it does not establish equivalence to immutable DOC first-observation time or timezone interpretation for request parameters. | `seendate` format OBSERVED; semantic equivalence/parameter timezone **UNVERIFIED** |
| Publisher time | Source seen time and publisher publication time are distinct concepts; DOC docs do not establish equality, and separate GAL `date` semantics cannot be substituted. | **UNVERIFIED** |
| Boundary equality | No historical record exactly equals START or END. Local validator rejects equality conservatively, but observed API inclusivity is not established. | API EQUALITY **UNVERIFIED** |
| Actual availability before cutoff | Fixed window ends 2026-10-07 08:00 JST, whereas its saved response arrived about 12:20 JST. A same-day later pull cannot prove 08:00 availability. The identical seendates do not establish the reason for batching. | **UNVERIFIED / BLOCKED** |
| First-seen immutability, indexing delay, revisions | No trustworthy field-level guarantee or same-cutoff before/after acquisition pair; the stored snapshot has no revision-invariance proof. | **UNVERIFIED** |
| Scoped completeness | 12 is below the cap of 250, but below-cap is not exhaustiveness; 10-cap comparison got 429. | **UNVERIFIED / BLOCKED** |
| Overflow behavior in local validator | Raw count `>= limit` fails **before** dedupe; no clipping/query split/retry rescue. 10-row synthetic equality covered. | SYNTHETIC FAIL-CLOSED ONLY |
| Raw provenance | Existing 200 and 429 raw bytes, request parameters, status, headers, receipt timestamps and checksums directly rechecked. | HISTORICAL RAW INTEGRITY VERIFIED; NOT prospective integrity |

DOC is a document/full-text search service, while proposed classification input is **title metadata only**. This role performed no headline classification and no publisher-body ingestion.

## Narrow source-code defect and synthetic verification

**Reproduced defect:** after HTTP 429 has been received and its raw body saved, `gdelt_schema_probe.py` overwrites `retrieval_completed_at` with a later exception-handling timestamp. This obscures precise receipt provenance.

**Repair:** preserve the initial response-completion stamp if present. For failures with no response (e.g., transport error), preserve an explicit failure timestamp under the existing manifest field. No change to query, MAXRECORDS=250, window boundaries, timestamps used for eligibility, deduplication, source PASS logic, raw preservation or science gates.

- Test environment: Python **3.13.5**; `python -m py_compile gdelt_schema_probe.py test_gdelt_schema_probe.py` **PASS**.
- `python -m unittest discover -s . -q`: **11/11 PASS** on patched source code, run locally in a copy of the GitHub source-probe directory. Previous 9 test cases retained; two tests added (mocked 429 time preservation and invalid UTF-8 response evidence). All network calls in the tests are mocked.
- Unmodified source replay with the expanded 11-case tests: **1 FAIL** specifically for overwritten 429 completion timestamp. Non-UTF-8 receipt test already passed on baseline because `UnicodeDecodeError` is a `ValueError`; therefore no redundant code change was made.
- Original code/test git blob SHAs were verified against GitHub before reconstructing the test environment: `88c9ba9f0051e489ffdadd07ff5efec6b721db6f` / `3af6f6084803b48f6da95dc4412cafe1766990b8`.
- **CI NOT RUN / NOT CLAIMED.** The existing `.github/workflows/fxns-gdelt-source-probe.yml` also invokes a live GDELT query with a runtime-selected window on PR events. Commit has `[skip ci]` to prevent an unscheduled probe, so checks may remain pending. An independent reviewer must not treat local synthetic PASS as source qualification.

## Final determination and one next required condition

**`PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED`**. Source reachability and historical raw integrity are evidenced; DOC first-seen semantics, query-timezone/equality mapping, scoped completeness/revision stability, and actual pipeline availability at/before the frozen cutoff are **not** proven. The original separate XM gate remains `LOCAL_XM_EXECUTION_REQUIRED`.

Scientific `UNTESTED`, specification `PROPOSED_NOT_FROZEN`, formal prospective cohort **CLOSED**; human freeze / independent Packet D / market outcome access / order authority **NOT GRANTED**. A 200 response or 11 synthetic tests do not change those statuses.

**Exactly one next gate:** demonstrate and independently review **prospective point-in-time GDELT acquisition integrity** for the existing fixed DOC query, including authoritative qualification of the required timestamp/boundary/completeness semantics and immutable proof of a response actually retrieved before **08:00 JST**. Until then, stop; do not reclassify historical raw as prospective, replay failed requests, tune query/window, change provider to GAL, or access market outcomes.
