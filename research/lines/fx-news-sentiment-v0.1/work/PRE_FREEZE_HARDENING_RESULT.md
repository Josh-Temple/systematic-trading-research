# Pre-freeze hardening result — 2026-10-07

## Fresh-read start

PR #63 OPEN / DRAFT; head 6947a752361951c9973a95c389810b0a5dc0bdbb.
Remote clone matched the connector PR head. Read CURRENT, RESEARCH_LINE, SPEC,
SOURCE_CONTRACT, Packet B, source qualification result, prompt/schema/manifest,
deterministic core/parser/tests, DOC probe/runtime manifests and XM collector/runbook.
No AGENTS.md found in checkout. Commit history was reviewed. No market outcomes
were fetched, classified, calculated or inspected; no new GDELT API request was made.

## Amendment versus code repair

Scientific candidate amendment: Thursday exits Friday, not next Monday. Monday–
Thursday issuance and 08:15 targets unchanged; Friday is exit-only. This repairs the
weekend rationale while preserving a normal 24-hour horizon. No result-based choice.
Known closure at either target blocks issuance, not rescheduling. Unknown/missing
exit quote remains an immutable missing outcome and administrative review, never
zero or omission of a losing-looking event. All paths are shadow-only.

Source rule clarification: raw returned_count >= configured_MAXRECORDS (250 in
formal candidate) is INPUT_CORPUS_COMPLETENESS_UNVERIFIED before dedupe. No formal
classification, outcome join, cohort count or later rescue. Below cap is not a
completeness proof. Qualification and prospective acquisition gates remain closed.

Code repairs/extensions: offline normalize now validates its configuration and
emits the exact cap error; core gains schedule, formal-source and open-window guards
and deterministic dedupe matching the pre-existing source probe. Legacy upper-bound
and exact-URL utilities stay backward compatible but are not sufficient formal gates.
Formal runner still absent: helpers are tested contracts, not an end-to-end issuance
system. Source flags must come from audited qualification, never be inferred from count.

## Time evidence and limitation

Fresh official read: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
Sections STARTDATETIME/ENDDATETIME describe after/before with YYYYMMDDHHMMSS;
MAXRECORDS documents up to 250. Publication terminology there does not establish
precise DOC seendate/immutable first-seen semantics. Existing preserved runtime
response has seendate YYYYMMDDTHHMMSSZ (seconds, Z parsed UTC), all interior to
request. API parameter timezone guarantee and equality behavior versus this field
remain UNVERIFIED. Keep conservative strict open endpoints rather than claiming
half-open inclusion is supported. Candidate exact width: 24 hours each calendar day,
cutoff 08:00:00 JST exclusive. Equality/out-of-window records block whole event.
Neither the runtime nor docs proves publisher-time equivalence, immutable first seen,
absence of index delay/revisions, exhaustive news coverage or actual pipeline receipt
by cutoff. Prospective acquisition evidence and independent source review are required.
No extra request, retry, comparison or source substitution was attempted after 429.

## Deduplication

Retained existing DOC policy: stable sort by seen, exact URL, title; mark every seen
URL and normalized title, retaining first unseen pair. Title equality = NFKC +
casefold + whitespace collapse. Exact URL duplicates, repeated same article and
same normalized title at different URLs are excluded with existing reason logs.
No URL normalization; host www handling only checks domain consistency. Syndicated
identical titles collapse; paraphrases/different titles and tracking-URL variants
can survive. Semantic near-duplicate detection is not introduced. Hash raw bytes
before any processing and retain all exclusions and original response.

## Prompt/output approval candidate

Prompt/schema exact bytes unchanged; hashes recomputed against manifest PASS.
Sentiment and reason enums, missing/extra/duplicate fields, invalid JSON, row identity
and NOT_MENTIONED reason guards are covered by strict parser. Failure blocks the
whole event; no repair/retry selection. Before freeze select visible model identity
and observable thinking/configuration label. Execution record must retain event ID,
record ID, exact input/assembled request bytes and hashes, canonical prompt/schema
hashes, visible model, configuration label, issued_at (aware), raw structured response,
validation status and failure reason. These are host-side records, not extra classifier
fields. No hidden-version guarantee is claimed. Classifier chooses no source, query,
threshold, price prediction, BUY/SELL or position size. No real ChatGPT invocation.

## Verification

53/53 synthetic tests PASS: 44 core/prompt/schedule + 9 source/preservation.
Existing 38 tests preserved; 15 additional tests. Test log PRE_FREEZE_TEST_LOG.txt.
XM collector py_compile PASS; collector bytes unchanged; not executed.
git diff --check PASS. Prompt/schema exact-byte hashes PASS. Runtime raw hashes PASS.

## Final status and blockers

- Scientific: UNTESTED
- Specification: PROPOSED_NOT_FROZEN
- GDELT: PARTIAL_WITH_GAPS; formal gate SOURCE_QUALIFICATION_BLOCKED
- Prompt/output: FREEZE_READY_CANDIDATE; model/config selection and human freeze pending
- Synthetic implementation: PASS, 53 tests
- XM source qualification: LOCAL_XM_EXECUTION_REQUIRED
- Formal cohort: CLOSED

Open: DOC seendate meaning/UTC parameter mapping/equality/index revisions, prospective
acquisition integrity and scoped completeness qualification; XM symbol/server/time/
Friday quote feasibility/swap/commission; formal ledger/runner; independent Packet D
review and explicit human freeze. Cap comparison remains historical UNVERIFIED, but
is not a reason to weaken the fixed cap exclusion or aggressively retry it.

## Exact local XM next action (not performed here)

On intended Windows XM MT5 terminal, logged in locally, use xm-source/WINDOWS_RUNBOOK.md:
`py -m pip install MetaTrader5`, then `py collect_mt5_eurjpy_source_probe.py` in an
empty folder. Preserve tick_probes_raw.csv, metadata.json, sha256_manifest.json locally.
Do not send credentials/account identifiers. Exact EURJPY absence stops; a suffix
requires an explicit source-identity decision, no automatic substitution. Independent
review must establish time/time_msc to UTC/JST and first valid quote in [08:15,08:16],
including Friday exit session feasibility, server identity and actual account costs.
Existing three fixed probes include a Thursday but no Friday: they alone cannot
qualify Friday exit. Do not infer Friday availability from weekday scheduling;
any additional Friday source-only probe must be fixed and reviewed before execution.
No market outcomes, order submission or substitute feed is authorized by this report.


## Subsequent collector preparation update — 2026-10-07

The missing-Friday collector gap described above is superseded by xm-source/RESULT.md:
v0.2 preserves the original three windows and adds three calendar-selected Friday
windows. FRIDAY_EXIT_PROBE_READY_NOT_RUN; actual source qualification remains
LOCAL_XM_EXECUTION_REQUIRED. Historical v0.1 validation remains unchanged.
