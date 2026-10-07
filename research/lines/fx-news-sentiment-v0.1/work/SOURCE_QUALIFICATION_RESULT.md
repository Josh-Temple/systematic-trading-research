# Packet B source qualification — 2026-10-07

Status: PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED
Scientific status: UNTESTED; formal cohort CLOSED; no market outcomes accessed.
Fresh-read baseline: PR #63 head `87e5271fb0851d1c5701bc9f2771e363180722e2`.

## Scope and independent checks

Read the current research line, specification, prior-art summary, source preflight,
source contract, packets B/D, synthetic core/tests and XM collector/runbook directly
from the checked-out remote head. No previous conversation supplied current state.
This is an independent review of the pre-existing artifacts, not Packet D PASS on
this worker's own changes, and not a fresh replication of the literature findings.
The 24 original synthetic tests pass on Python 3.12. The pair/count rule is unchanged.
Updated checks: 29 core/prompt parser tests + 9 source/preservation tests PASS (38 total).
Both runtime raw hashes and prompt/schema file hashes independently recomputed PASS.
`git diff --check` PASS. JSON Schema library validation was not run: jsonschema is
not installed; strict contextual parsing is tested with the dependency-free parser.

## Actual runtime evidence

1. Original short-window `euro sourcelang:english` probe: HTTP 429. Original code
   discarded the error body; this first attempt has no raw-byte preservation evidence.
2. Exact candidate 24-hour DOC query with MAXRECORDS=250: HTTP 200. Preserved
   `source-probe/runtime-20261007-exact/response.raw`, 5,962 bytes,
   SHA-256 `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d`.
   Window 2026-10-05 23:00 UTC to 2026-10-06 23:00 UTC (ending October 7 08:00 JST).
   Response headers include application/json and public max-age=900.
   12 rows, all English, all seendate `20261006T083000Z`.
   Fields: domain, language, seendate, socialimage, sourcecountry, title, url, url_mobile.
   All returned times lie strictly inside the requested window; this does NOT prove
   endpoint inclusivity, general UTC semantics, first-seen immutability or completeness.
   No returned title was classified and no linked publisher page was opened.
3. Initial validator rejected www-prefixed URL hosts against bare domain fields.
   Fixed only this observed normalization difference, preserving original manifest.
   `offline_validation.json` is a separate replay, not a replacement live attempt.
   Deterministic deduplication retains 10 rows; two exclusions are logged there.
4. Same query/window with MAXRECORDS=10: HTTP 429, body 444 bytes preserved at
   `runtime-20261007-cap10/response.raw`, SHA-256
   `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6`.
   Cap comparison is UNVERIFIED, not PASS. Do not retry-loop or provider-switch.

## Query semantics: documentation versus runtime

Exact candidate: `(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`.
`mode=artlist`, `format=json`, `sort=dateasc`, `maxrecords=250`; fixed UTC window.
Terms cover currency names and the two central banks, chosen without market results.
DOC searches article text, NOT only titles. Classification still receives titles only.
Therefore a matching body may accompany an irrelevant title; retain and classify as
NOT_MENTIONED/INSUFFICIENT rather than using the article body or adaptive filtering.
Official documentation supports OR/phrase operators, original-language restriction,
explicit time ranges and a 250-record maximum. Runtime demonstrates successful
acceptance of this query, not exhaustive proof of the server's matching semantics.
Below-cap count is not proof that all matching news was returned or available in time.
The single observed time batch warrants a repeated source-only acquisition check;
no cause is inferred from it.

Important correction: DOC `artlist` and the separate GAL dataset are different routes.
GAL `date` may be publisher time OR observation time. Do not transplant that field
contract into DOC `seendate`. GAL is not an authorized fallback in this line.

## Candidate deterministic contract

- Exact 24 hours ending 08:00 JST every issuance day; Monday also uses 24 hours,
  not the interval since Thursday. No outcome-informed query refinement.
- Raw count >= 250 fails before deduplication. No clipping, top-N rescue, splitting
  windows or relevance sorting to rescue an overflow without a new pre-freeze decision.
- Malformed/missing array, field/language/time mismatch, HTTP error or incomplete
  acquisition blocks the event; it is not a scientific NO_TRADE observation.
- Sort by (seen timestamp, exact URL, title). Keep first exact URL and normalized
  title key (Unicode NFKC + casefold + whitespace collapse); preserve exclusions.
  Do not strip punctuation, tracking parameters or merge fuzzy paraphrases.
  Near-duplicate paraphrases remain separate; this is an explicit limitation.
- Preserve raw bytes before decoding, HTTP headers/status, request parameters,
  start/completion times and SHA-256. Never overwrite an earlier attempt directory.
  HTTP error bodies are also preserved. A transport failure has no fabricated body/hash.
- Attribution: Source: GDELT Project (https://www.gdeltproject.org/).
  Original publishers identified by article URLs. No publisher body/image is ingested.

## Prompt and model contract

`PROMPT_v0.1.txt`, `OUTPUT_SCHEMA_v0.1.json`, and `PROMPT_MANIFEST_v0.1.json`
are FREEZE_READY_CANDIDATE_NOT_HUMAN_FROZEN. Hash exact file bytes, final newline included.
One input object per fresh classification request; values JSON-encoded, no prior event
context, browsing/tools/memory disabled where the product permits. Preserve the actual
assembled request, raw response, timestamps, visible model and thinking/configuration
labels. A hidden model change or inaccessible product controls remain limitations.
Model identifier/configuration must be selected and recorded before human freeze;
missing observable identity or a visible change blocks issuance. No API subscription
is assumed. Synthetic tests verify parser mechanics, not ChatGPT semantic accuracy.
No actual model invocation on the fetched headlines was performed.
The strict parser rejects duplicate keys, unknown fields, malformed labels/reasons,
identity mismatch and missing/extra rows. No silent repair/retry-selection/drop.
Any invalid classification blocks the whole event; diagnostic reasons never score.

## Remaining stop gates and local handoff

GDELT SOURCE PASS is NOT granted: endpoint inclusion, UTC/first-seen interpretation,
index latency/revision and completeness remain unqualified; cap comparison got 429.
A response obtained at 12:20 JST cannot prove pipeline availability at 08:00 JST.
Formal issuance requires prospective timestamped raw acquisition evidence; either
pre-cutoff polling or a precisely justified GDELT availability rule must be reviewed
before freeze. Do not backfill this probe into a formal event.

XM requires the actual intended Windows MT5 terminal. Stop here for that gate:
run `xm-source/WINDOWS_RUNBOOK.md` locally, retain raw probe/manifest unchanged,
then independently verify exact symbol/server, time mapping and commission/swap.
No substitute quotes, market returns, account history or broker orders were accessed.

Schedule issue found independently: "next eligible day" with Mon–Thu issuance makes
Thursday exit Monday, conflicting with the stated weekend-avoidance rationale.
Resolve whether Friday is an exit-only date before human freeze, without market data.
Do not silently change the horizon in this worker.

Packet B is complete only to the available cloud/source/prompt-candidate boundary.
No full B PASS, final scientific freeze or independent D PASS is claimed.

## Evidence sources freshly opened

- https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/

The first documents DOC full-text queries, caps and date parameters; the second
is evidence for distinguishing GAL mixed date semantics, not a DOC field guarantee.
Prior provider legal/preflight conclusions were read as existing evidence and were
not independently re-adjudicated in this runtime task.
