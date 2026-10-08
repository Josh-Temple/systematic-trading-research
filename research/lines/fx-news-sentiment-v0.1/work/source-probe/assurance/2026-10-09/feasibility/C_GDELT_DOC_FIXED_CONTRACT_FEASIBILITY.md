# C — GDELT fixed DOC contract: point-in-time, first-seen and completeness feasibility

- Review date: 2026-10-09 JST
- Role: **C, independent source-specification feasibility review**; no FXNS implementation changes
- Status: **PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED / HOLD**.
- Decision: **The currently available official DOC 2.0 ArticleList specification and preserved evidence do not establish the guarantees required for formal issuance under this exact candidate contract.** This is not a universal impossibility theorem about all GDELT services or all future implementations. Additional unapproved live probes have no authorization here.
- FXNS scientific status: **UNTESTED**; specification **PROPOSED_NOT_FROZEN**; formal cohort **CLOSED**; XM **LOCAL_XM_EXECUTION_REQUIRED (deferred)**; no market-outcome access or trading permitted.

## 1. Fixed scope and read identities

Repository: [Josh-Temple/systematic-trading-research](https://github.com/Josh-Temple/systematic-trading-research). The independently read [PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63) is OPEN/DRAFT on `research/fx-news-sentiment-v0.1`, head `202ee37d0cd3f9838b153ea361dfdeba5244a271` (fresh-read 2026-10-09 JST). The previous [source audit PR #75](https://github.com/Josh-Temple/systematic-trading-research/pull/75) remains OPEN/DRAFT at `e8f705d1bc189081666a6bae2678f3f15e8e6507`; [integration HOLD PR #79](https://github.com/Josh-Temple/systematic-trading-research/pull/79) remains OPEN/DRAFT at `fb563987e65711d49a8b9fcae2eca93d990b9a12`. Prior reports are evidence to inspect, **not** automatic approval of this review.

**Contract, unchanged:** query `(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`; DOC `mode=artlist`, `format=json`, `sort=dateasc`, 24-hour `startdatetime/enddatetime` window ending **08:00 JST**, `maxrecords=250`. Query ID `FXNS-DOC-QUERY-v01-candidate`. No alternative provider, revised query/cap/window, classification prompt, model, schema or scoring rule was introduced.

Fresh-read immutable source files on #63 head:
- `SOURCE_CONTRACT.md` blob `36dd9c9977718a8da02ae8f569cad76d4c0acd15`; `work/SOURCE_QUALIFICATION_RESULT.md` blob `829fe079a4d45edefe1347d9593f41fec34d46dd`.
- Preserved HTTP 200 manifest blob `d9ecb57f880a407bcfb55faf5e8bfd9018c5de09`; raw blob `ff5159d91bc2ead99bbd0a669e8c8079f585d9a1`; offline replay blob `08efe2a489f95e390406d07aaf044b2467c65169`.
- Preserved HTTP 429 manifest blob `fe99b74c6e4eeccb5000a6845a901d7b92c38086`; raw blob `faca354e1d0c6bf1e7fe7a7990b6015df6023b55`.
- Actual source probe `gdelt_schema_probe.py` blob `88c9ba9f0051e489ffdadd07ff5efec6b721db6f`; manifest schema blob `457937fb2f2c20b9b42d11efb3c0a1e30f7e8852`.
- Actual research-branch FXNS workflow `.github/workflows/fxns-gdelt-source-probe.yml` blob `620581df64cf247c293781389bd7386df391f30e`; offline runner `.github/scripts/fxns_offline_unittest.py` blob `25636eca0b6c282a2f7233064ec9661fc62666c0`.

Official public primary references (documentation only; **not** the DOC API endpoint):
1. [GDELT DOC 2.0 API Debuts — official specification](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/) (2017): DOC full-text query operators, `sourcelang`, `artlist`, `STARTDATETIME/ENDDATETIME`, maximum 250 results, date sorting, and description of publication-date search criteria.
2. [Announcing The GDELT Article List & RSS Feed — official GAL description](https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/) (2021): separately defined GAL records and mixed GAL `date` provenance; **GAL is not DOC `artlist` and cannot substantiate DOC `seendate` semantics.**
3. Historical separate independent [B audit in PR #75](https://github.com/Josh-Temple/systematic-trading-research/blob/e8f705d1bc189081666a6bae2678f3f15e8e6507/research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-09/B_GDELT_POINT_IN_TIME_AND_COMPLETENESS_ASSURANCE.md), read as a prior audit, not a new experiment.

## 2. Evidence: past HTTP 200/429 are *after* the time boundary

| Preserved observation | Evidence and limits |
| --- | --- |
| Fixed 250-cap HTTP **200** | Target interval `2026-10-05T23:00:00Z < t < 2026-10-06T23:00:00Z` under the local conservative open-boundary policy. Request began `2026-10-07T03:20:01.449225Z` (12:20:01 JST), finished `2026-10-07T03:20:26.968407Z` (12:20:26 JST); thus finished **over four hours after** the 2026-10-07 08:00 JST eligibility cutoff. Manifest: HTTP 200, 5,962 raw bytes, SHA-256 `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d`, `SOURCE_QUALIFICATION_BLOCKED` with original `domain/URL mismatch` error. |
| Separate offline validation | **12** saved English rows, all raw `seendate=20261006T083000Z`, **10** retained after exact-URL/normalized-title handling; **2** `NORMALIZED_TITLE` exclusions. Offline replay corrected observed `www.` comparison; it does not retroactively amend the original manifest, prove source recall, or establish the meaning or invariance of `seendate`. |
| Same window, cap=10, HTTP **429** | Began `2026-10-07T03:20:58.787434Z` and finished `2026-10-07T03:21:18.616094Z`, preserved 444 bytes and SHA-256 `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6`. The saved body asks for at most one request every five seconds. **Not a successful cap comparison;** cannot infer exhaustiveness of the 250-cap result. |

The previous B audit states that it independently recomputed both hashes (2/2 matches). C freshly **read** both raw files, both manifests and replay via GitHub but **did not independently recompute byte-level SHA-256** in this C session. The length of UTF-8 text delivered by a connector is not substituted for the manifest's byte count. No fresh API call occurred.

## 3. Seven distinct guarantee obligations

Status vocabulary is **DOCUMENTED**, **OBSERVED**, **UNVERIFIED**, **BLOCKED**, each applied to the named claim rather than the whole source.

| Obligation | Status | What follows, and what does not |
| --- | --- | --- |
| **(a) Search universe / recall** | **DOCUMENTED** for DOC operator forms and full-text ArticleList; **BLOCKED** for query-wide exhaustive coverage | Official DOC allows `OR`, quoted terms, original-language restriction and `artlist`. It searches indexed content, not just the titles later passed to the classifier. The documentation does not promise every relevant publisher article globally has been indexed, or every qualifying indexed match is emitted in a 250-row ArticleList response. A matching article body with an irrelevant title does not justify using that body for classification. |
| **(b) Raw DOC `seendate` identity and immutability** | **OBSERVED** for a `YYYYMMDDTHHMMSSZ` value in the historical 200 response; **UNVERIFIED** for immutable first-seen definition | All 12 saved rows share one value. It may be parsed by the existing local code as UTC, but neither this sample nor the cited official DOC parameter documentation defines an immutable event-level first-observation record or establishes that first seen means available to *our* pipeline. Uniform timestamps do not reveal ingestion batching or rule out backfills. |
| **(c) Publication vs observation** | **DOCUMENTED** that DOC documentation uses the term publication date for sort/range; **UNVERIFIED** equivalence to raw `seendate` | DOC `sort=dateasc` is described as sorting by publication date. A publisher's timestamp may differ from GDELT observation/indexing and receipt time. Official GAL `date` is explicitly mixed publisher/seen depending on record, but it is a different dataset; **never copy GAL's `date` contract into DOC's `seendate`**. Saved DOC ArticleList has no independently qualified publisher timestamp here. |
| **(d) Acquisition completed before 08:00 JST** | **BLOCKED** | The 200 receipt completed at 12:20:26 JST, not before 08:00. Neither raw `seendate` nor a retrospectively fixed `enddatetime` proves earlier API availability or earlier local receipt. An 08:00-ending window and an acquisition-required-*before*-08:00 have an intrinsic final-interval timing risk; docs provide no pre-cutoff snapshot or atomic close assurance. |
| **(e) Indexing delay, revisions, first-seen, later backfill** | **UNVERIFIED** | The cited official DOC document does not offer a qualified snapshot/version identifier, indexed-as-of watermark, immutability statement, or guaranteed update latency for the fixed query. A repeated historical query might differ from what was visible at the initial cutoff. This is an unproved risk, not an observation that revisions actually occurred in these 12 rows. |
| **(f) UTC and exact boundary inclusivity** | **DOCUMENTED** for precision-format `YYYYMMDDHHMMSS` and DOC search wording “after” start / “before” end; **UNVERIFIED** for `seendate` filter/equality and server timezone | Manifest start/end are explicitly UTC and the saved `seendate` strings end in `Z`; all 12 are strictly inside the range. No saved row equals the start/end. The local validator conservatively imposes strict open `start < seen < end`, which is a local decision—not proof that the DOC server filters the same underlying timestamp in UTC with those exact equality semantics. |
| **(g) `MAXRECORDS`, caps and 429** | **DOCUMENTED** 250-result maximum; **OBSERVED** 12 raw <250, 10 retained, HTTP 429 for the comparison; **BLOCKED** for exhaustive result certification | A maximum-result setting is a response ceiling, not a completeness certificate. Being below cap does not logically establish all matches returned or indexed before cutoff. A 429 response has no valid ArticleList comparison. Existing code's fail-closed `len(articles)>=limit` protects a known cap-hit case but not unseen missing rows. No retry-loop, cap change, time-split or provider switch is authorized. |

**Specific feasibility conclusion:** The **query shape is supported** by DOC documentation and a historical HTTP 200; **pre-08:00 availability, immutable first-seen, index-as-of completeness and revision behavior remain unproven**. Consequently the documented DOC contract **alone cannot satisfy** the proposed formal point-in-time/cohort eligibility contract. Do not label the API fundamentally or universally impossible; this review cannot establish impossibility of a future qualified evidence arrangement, either.

## 4. What one *approved* next evidence package can and cannot resolve

**Only proposed next substantive gate; do not collect during C:** one **separately authorized, pre-registered, prospective fixed-query acquisition-integrity receipt**, subject to independent review. The preregistration must specify the same exact query, 24-hour start/end, 08:00 JST deadline, unchanged `maxrecords=250`/sort/mode, intended runner, clock source and allowed clock error, success/failure conditions, source snapshot identity, complete HTTP status/headers/raw bytes + SHA-256, start and end wall-clock timestamps, unique append-only storage identity, retrieval of receipt after restart, original-article titles only (no article bodies), and the treatment of 429, partial requests, boundary rows and any later difference. **No API call now.** Authorization must be explicit and obtained in another session before any prospective run.

| Gap an approved package could address | Exact closing proof needed | Limit |
| --- | --- | --- |
| **Before-08:00 acquisition** | Immutable and independently reviewed raw response and actual completion timestamp **strictly earlier than** the relevant 08:00 JST cutoff on the intended pipeline, with clock trust established | This alone closes *only that day's successful receipt*, not publisher history or server-wide completeness. Any late completion is a failed attempt, not a trade or NO_TRADE observation. |
| **DOC first-seen `seendate` / UTC / endpoints** | Authoritative field-level semantics or separately approved controlled validation binding the returned field, index time, start/end equality and timezone to the same fixed query | Observed timestamp format and the GAL field are insufficient. Local conservative parsing can reject ambiguous records but cannot certify server field semantics. |
| **Completeness / max-cap / revision** | Authoritative provider-side point-in-time/exhaustiveness and index-state guarantee, or an independently approved, prospective, bounded verification protocol demonstrably adequate for the stated coverage scope; evidence of indexed-as-of and later changes if claiming revision stability | A single pre-cutoff HTTP 200 with fewer than 250 rows **cannot** prove these properties. If unavailable, retain **BLOCKED**; do not repeatedly probe without a stated contract condition each probe would close. |

These form **one governed evidence package**, **not one magic network response**. If the authoritative completeness/first-seen properties cannot be substantiated, a future human must separately decide whether to redesign the **pre-freeze** source contract or abandon the formal DOC cohort. **This C session does neither.** Arbitrary extra GDELT 200/429 samples or paperwork without exact proof obligations are low-value and must not be promoted to PASS.

## 5. Workflow safety, bounded actions and stopping decision

- Read actual `fxns-gdelt-source-probe.yml` at #63 head: a PR changing `work/source-probe/**` would trigger the **FXNS offline synthetic** workflow, not a GDELT live-probe step. It invokes `fxns_offline_unittest.py` and `compileall`. The Python test runner installs a process-level `socket.connect` deny, not an OS security sandbox. No new GitHub Actions run was started by C.
- Other workflow path triggers were inspected on the same #63 HEAD; no source-acquisition workflow was found triggered by this C-only `work/source-probe/assurance/2026-10-09/feasibility/**` report. **No source-readiness workflow, live API or workflow_dispatch should be launched**.
- Existing [run 37798966613](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798966613) / job `113385769601` showing 83/83 offline synthetic success relates to *previous PR #74*, not this report or a source guarantee. **No new independent suite executed in C**; neither prior PASS nor a new docs-triggered CI (if any) can authorize sources or market outcomes.
- **Excluded:** GDELT DOC API requests, live retries/cap probes, XM/MT5, alternative feeds, any real headline classification, EURJPY/other prices, market direction, outcomes, returns, P/L, trades, changing any fixed SPEC/prompt/schema/query/contract/raw/manifest/workflow.
- **STOP/HOLD:** unresolved cutoff receipt, first-seen mapping, exact UTC/equality, incompleteness, revisions, response cap or 429, observed SHA mismatch, source substitution, workflow drift, or absent human authorization. Preserve prior negative results unchanged.
- **E handoff:** **SOURCE_QUALIFICATION_BLOCKED** persists regardless of A/B synthetic fixes. Scientific status `UNTESTED`; `PROPOSED_NOT_FROZEN`; formal cohort `CLOSED`; no market-outcome access. A prospective receipt plus suitable authoritative semantics is a future governance gate, not C's source PASS.

## 6. Change manifest / review limits

Intended single C write under:
`research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-09/feasibility/C_GDELT_DOC_FIXED_CONTRACT_FEASIBILITY.md`

C-only Draft PR targets `research/fx-news-sentiment-v0.1`, branched from exact PR #63 head above; **not** `main`. Existing contracts, raw/manifest, code, tests, workflow, and reports are unchanged. This is a documentation/feasibility determination with preserved observational evidence, **not a rerun, certification, formal event, source qualification, or trader authorization**.
