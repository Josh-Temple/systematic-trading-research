# JP225 prospective forecast — source/readiness gate

Date: 2026-10-05
Status: PARTIAL / SCORED_COHORT_CLOSED

## Purpose

Qualify only the minimum inputs required to move SPEC-JP225-FORECAST-001-v01 from exploratory dry runs to a frozen scored prospective cohort. This is not a request to inspect historical JP225 outcomes or optimize the forecast system.

## Fresh-read inherited evidence

At main 40c1a04b793622d30e42fc298ef6a138407d46fa, the existing exact-XM JP225 EMA line is WAITING_FOR_XM_STAGE1_DATA. Exact XM MT5 JP225Cash is the free-source priority; Dukascopy JPN.IDX/JPY is rejected as an exact substitute and JPX/J-Quants DataCube is deferred under the no-paid-data policy.

Those facts permit reuse of source-acquisition mechanics, but they do not create a PASS for this forecast line.

## Gate A — exact outcome source

Required before formal scoring:

- exact XM MT5 JP225Cash symbol identity;
- XM server/account identity needed for reproducible retrieval;
- Bid/Ask tick availability;
- exact server timestamp semantics;
- server-time to UTC/JST mapping;
- deterministic retrieval around the 08:00 input cutoff and the 09:00 / 15:30 outcome endpoints;
- deterministic 1h/4h/24h lookback retrieval ending at the 08:00 cutoff;
- raw/canonical snapshot identity and hash;
- no fallback to Dukascopy, OANDA, JPX futures, or another broker for a missing formal event.

Current: NOT_PASS / inherited acquisition route remains waiting for XM Stage 1 data.

## Gate B — trading-day calendar

The event calendar must use a current authoritative JPX cash-equity calendar. The target daytime session is 09:00–11:30 and 12:30–15:30 JST. Special closures/holidays must produce NON_ELIGIBLE_SESSION rather than later discretionary exclusion.

Current: public official route identified; operational point-in-time calendar capture still to be pinned.

## Gate C — A2 point-in-time sources

Before freeze, mark every A2 field required or optional and pin an acquisition route. Candidate categories are USDJPY, qualified prior-US-session/cross-market information, BOJ/Fed settings, qualified Japan/U.S. sovereign yields, official macro releases, official communications, bounded pre-cutoff news, and official event calendars.

Current: PARTIAL / exact field list and durable news snapshot contract not yet frozen.

## Gate D — A3 repository snapshot

Before the first scored event:

- pin exact Git commit/blob refs for permitted repository research;
- include status labels verbatim;
- exclude or explicitly quarantine compromised/deferred evidence;
- prevent later repository updates from silently changing v0.1 inputs.

Current: ROUTE_AVAILABLE / final pin deferred until formal freeze.

## Gate E — record immutability and deterministic scoring

Required:

- append-preserving forecast record path;
- issued_at and information cutoff;
- canonical forecast hash;
- deterministic exact-XM start/end quote selection;
- Brier and MAE computation;
- explicit observation-state vocabulary;
- no record overwrite after issuance.

Current: SYNTHETIC_PASS. Deterministic helpers and record-contract tests pass in GitHub Actions. This does not resolve Gate A exact-XM acquisition or Gate C point-in-time source qualification.

## Dry-run policy

While any gate remains incomplete, a forecast may still be issued prospectively only as EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT.

The dry run may test workflow and error-attribution mechanics. It cannot be promoted later into the 60-event cohort, and a missing exact-XM outcome cannot be backfilled from another provider.

## Decision

SCORED_COHORT_CLOSED.

The next safe action is an exploratory forecast using an 08:00 information cutoff for the unchanged 09:00→15:30 target on an eligible JPX trading day, while exact XM acquisition remains fail-closed.
