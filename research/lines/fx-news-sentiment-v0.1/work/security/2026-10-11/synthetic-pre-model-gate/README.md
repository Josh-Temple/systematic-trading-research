# Synthetic pre-model read boundary (candidate, unmerged)

**Status: OFFLINE SYNTHETIC PROTOTYPE ONLY; NOT DEPLOYED OR SECURITY ACCEPTED.**

This is a standalone, standard-library Python sketch translating D's independent
[#109 audit](https://github.com/Josh-Temple/systematic-trading-research/pull/109)
T01–T22 into an executable, isolated proof of behavior. It does not modify
`fxns.py`, `event_ledger.py`, an actual GitHub connector, a Research Work tool,
a workflow, access permissions, a source contract, or the CSM gate.

## Reproduce (local offline only)

```sh
cd research/lines/fx-news-sentiment-v0.1/work/security/2026-10-11/synthetic-pre-model-gate
PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_safe_boundary
PYTHONDONTWRITEBYTECODE=1 python -m py_compile safe_boundary.py test_safe_boundary.py
```

No `pip install`, network, credentials, GitHub API, real headlines, live source,
market data, broker, or actual model input. Tests use only made-up identifiers
and synthetic markers. A `DeliverySink` emulates the model input; a `ReceiptSink`
emulates durable audit (in-memory only).

## Behavior in tested scope

- Reject all request operations except three literal operations; reject unapproved
  repo/PR/commit and unapproved response fields, types, content/media, incomplete
  paginated results, moving HEAD, unexpected documents, and errors.
- For `PR_METADATA`, require strict selection of a fixed metadata-only schema;
  emit verified enums and exact configured identities, never input body/title.
  This **does not** implement a wire-level GitHub GraphQL query.
- For `FILE_PATHS`, require each path to be in an exact allowlist; do not emit
  even earlier pages until the whole result validates.
- For `SAFE_DOCUMENT`, verify raw *fictional* bytes against a preapproved
  digest and release only a separately approved fixed excerpt, never raw bytes.
  Safe-content approval is an external **trusted precondition**, not produced
  by this code. SHA-256 alone does not prove reviewer independence or safety.
- Commit a fixed-shape, data-free audit receipt before release; reject output
  if audit append fails. In-memory receipt is neither tamper-proof nor durable.
- Reject duplicate operation delivery within a single boundary instance.
  The prototype does not implement distributed exactly-once semantics.
- Report known previous delivery as an exposure even when presentation was
  subsequently masked.

## T01–T22 mapping and confidence

The unit test names map one-to-one to D #109's scenarios. **22/22 local
synthetic unit tests passed** in the recorded container run. This is not a CI
run, not GitHub Actions, not a real model/Work connector test, and not a live
source suitability test.

Coverage limitations, including those that a green test result MUST NOT hide:

- **T01/T02/T04/T09/T10/T16:** test in-memory schema rejection, NOT source-side
  field selection. A real API may already have delivered forbidden bytes to
  an upstream host before this boundary.
- **T05/T12/T13/T18:** exercise in-memory complete-page validation; do not prove
  atomicity under concurrent production page retrieval or live streaming.
- **T06:** an explicit post-delivery exposure trace is rejected as a clean pass;
  no real LLM receives synthetic data.
- **T07/T08/T21:** test exception text suppression, fixed receipt types, and
  audit failure in an in-process surrogate, not a hardened logging subsystem.
- **T14/T15/T17/T19/T20:** unsupported redirect, preview, cache, bypass,
  and prompt-content *paths* are rejected within this API; no network egress,
  OS capability, tool/connector bypass or platform-level input is controlled.
- **T03/T11/T22:** document hash/approved excerpt and nominal release only.
  Safe approval, non-free-text classification, reviewer role separation and
  provenance are not established in code.

## No deployment claim

Real pre-model prevention would require (a) a trusted broker separate from
research-model credentials, (b) exact GitHub source-side field selection,
(c) approval of safe document excerpts by an authorized independent reviewer,
(d) denial of connector/browser/shell/cache/preview bypass at the **host**
permission level, (e) validated audit durability, and (f) independent tests
with an externally observed actual delivery boundary. These are NOT available
or proven in the current ChatGPT Work environment by this prototype.

The research state remains `SOURCE_QUALIFICATION_BLOCKED`, formal cohort
`CLOSED`, CSM I2 `BLOCKED/CLOSED/market_outcome_access=false`. No conclusion
about real exposure impact, source qualification, model safety or market
outcomes follows from these tests.
