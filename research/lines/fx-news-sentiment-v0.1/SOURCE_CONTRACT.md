# Source contract — FX News Sentiment with ChatGPT v0.1

Status: UNRESOLVED / PRE-FREEZE

## News-source qualification

The primary external paper used DailyFX, Investing.com and FXStreet separately. That does not automatically authorize any of them for v0.1.

Packet B must determine, for each candidate provider:

- stable publication timestamp availability;
- timezone semantics;
- article edit/update behavior;
- whether historical/current content can be retrieved without post-cutoff contamination;
- robots/access constraints;
- terms relevant to storing the exact model input;
- whether public GitHub may store text, only metadata/hash, or neither;
- duplicate/syndicated-article handling;
- article identity after edits;
- operational availability from ChatGPT/manual workflow.

No provider may enter the formal source set merely because it performed well in the prior paper.

## Input preservation

Preferred order:

1. preserve exact input text privately plus SHA-256 and public metadata;
2. if exact text may be stored publicly, also save the bounded text snapshot;
3. if neither is allowed, the source is unsuitable for confirmatory reproducibility unless another lawful identity-preserving route exists.

Public repository records must never pretend that a URL alone proves what text ChatGPT saw.

## Timestamp rule

Formal news input requires an explicit publication timestamp.

- publication timestamp <= 08:00 JST cutoff;
- retrieval can occur after cutoff only if the source preserves a trustworthy publication time and the article state used is demonstrably the pre-cutoff state;
- an article materially updated after cutoff is excluded unless a pre-cutoff snapshot is available.

## XM quote-source qualification

Before formal scoring establish:

- exact symbol identity for EURJPY;
- account/server identity;
- Bid/Ask field semantics;
- server timestamp and UTC/JST mapping;
- quote retrieval route;
- 08:15 boundary selection behavior;
- weekend / maintenance / missing-quote handling;
- account commission and swap schedule relevant to the candidate holding window;
- raw source preservation and hash procedure.

If exact XM qualification fails, formal cohort remains closed. Do not silently use OANDA, Dukascopy, Yahoo, another broker, or midpoint-only public data.

## Model-input boundary

The classifier receives only the qualified article input and the currency labels it is asked to classify.

Forbidden inputs for v0.1 article classification:

- post-cutoff EURJPY prices;
- future returns;
- prior scored outcomes;
- "what happened next" summaries;
- repository performance results;
- adaptive instructions based on accumulated P&L.

The classifier may know historical facts from pretraining; this is an uncontrolled limitation and a reason to rely on prospective evaluation.
