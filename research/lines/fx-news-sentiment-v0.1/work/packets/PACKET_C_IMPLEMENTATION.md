# Packet C — Outcome-blind deterministic implementation

## Goal

Implement everything that can be tested without historical/prospective market outcomes.

## Required implementation

- article-input record validator;
- ChatGPT-output schema validator;
- deterministic per-currency count aggregation;
- exact SNB-style score calculation;
- deterministic EURJPY LONG/SHORT/NO_TRADE rule;
- cutoff/late-issuance guard;
- append-only event-record canonicalization and SHA-256;
- exact quote-boundary selector against synthetic Bid/Ask fixtures;
- long/short executable-return calculation;
- NO_TRADE accounting;
- cost fields that fail closed when required cost identity is missing;
- cohort gate that rejects formal scoring before human freeze.

## Synthetic tests

Cover at least:

- all sentiment enum combinations;
- same-sign versus opposite-sign scores;
- zero score semantics;
- duplicated article IDs;
- post-cutoff article rejection;
- material post-cutoff update rejection;
- late ChatGPT issuance;
- quote exactly on and outside the 60-second tolerance;
- missing Bid or Ask;
- spread-aware long/short arithmetic;
- no-trade return = zero;
- mutation of an issued record;
- model-identifier change during a nominal cohort.

## Prohibited

- loading historical EURJPY outcome files;
- calculating historical strategy returns;
- using test failures to change the scientific rule unless the failure is a pure implementation contradiction.

## Exit

Implementation can be called READY_FOR_INDEPENDENT_AUDIT only when all synthetic tests pass and no market outcome was accessed.
