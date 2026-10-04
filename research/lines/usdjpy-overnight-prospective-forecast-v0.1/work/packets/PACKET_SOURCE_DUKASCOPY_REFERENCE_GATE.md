# Work Packet — USD/JPY Dukascopy reference-feed gate

Date: 2026-10-04 JST  
Role: Source Qualification Worker  
Scientific outcome access: **FORBIDDEN**  
Signal / forecast performance computation: **FORBIDDEN**

## 0. Purpose

Qualify a bounded USD/JPY best-Bid/Ask tick source for the prospective overnight + weekly forecast line.

This packet is source-only.

It must not answer whether USD/JPY rose or fell over a forecast horizon.

## 1. Fresh reads

Before execution, fresh-read:

- `research/lines/usdjpy-overnight-prospective-forecast-v0.1/CURRENT.md`
- `research/lines/usdjpy-overnight-prospective-forecast-v0.1/specifications/SPEC-USDJPY-FORECAST-001-v01.md`
- `research/lines/usdjpy-overnight-prospective-forecast-v0.1/specifications/SPEC-USDJPY-WEEKLY-001-v01.md`
- `research/lines/usdjpy-overnight-prospective-forecast-v0.1/work/SOURCE_READINESS_2026-10-04.md`
- `research/lines/usdjpy-overnight-prospective-forecast-v0.1/work/SOURCE_READINESS_UPDATE_2026-10-04_IMPLEMENTATION.md`
- `research/proposals/fx-daily-breakout-20261003/SOURCE_QUALIFICATION_2026-10-03.md` from branch `research/fx-daily-breakout-20261003`
- `research/proposals/fx-daily-breakout-20261003/DATA_CONTRACT.md` from that branch

Do not use memory or this packet's quoted status as current evidence.

## 2. Provider documentation

Confirm from current Dukascopy first-party documentation:

- USD/JPY instrument identity;
- historical tick access;
- timestamp semantics;
- Bid / Ask availability;
- historical-vs-demo/live caveat;
- persistence/download route if used.

Candidate first-party references:

- https://www.dukascopy.com/client/javadoc3/com/dukascopy/api/IHistory.html
- https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/overview-historical-data/
- https://www.dukascopy.com/wiki/en/development/data-export/

Record exact URLs and retrieval time.

## 3. Bounded raw sample

Retrieve only a small, predeclared sample sufficient to qualify structure.

Preferred order:

1. JForex / official historical API route;
2. official Dukascopy historical-download route if the exact file route is verified.

Do not download a broad historical period.

Suggested source-only windows:

- one active-session hour around a representative 2026 date;
- one historical standard-time date if needed to validate source UTC semantics;
- narrow windows around candidate endpoint clock times only if necessary for endpoint selector qualification.

The date choice must not be based on whether prices rose/fell.

## 4. Required raw-sample record

Persist:

- provider;
- instrument;
- retrieval route;
- retrieval UTC/JST;
- requested from/to timestamps;
- source timezone semantics;
- raw byte count;
- SHA-256;
- encoding/compression identity;
- decoded record count;
- exact field order;
- point scaling if applicable;
- first timestamp;
- last timestamp;
- whether timestamps are timezone-naive or UTC-defined at source;
- duplicate timestamp count;
- out-of-order count;
- invalid `ask < bid` count;
- non-positive price count;
- missing/unreadable file state.

Do not compute:

- start-to-end returns;
- direction;
- P/L;
- strategy signal;
- forecast score;
- Sharpe;
- hit rate.

## 5. Endpoint semantics

Using only source-structure tests and synthetic assertions, establish that project code can deterministically select:

### Overnight

- last valid tick `<= 22:00 JST`, max age 60 seconds;
- first valid tick `>= 08:00 JST`, max delay 60 seconds.

### Weekly

- first valid tick `>= Monday 08:00 JST`, max delay 60 seconds;
- first valid tick `>= Friday 22:00 JST`, max delay 60 seconds.

If the source normally has no tick in the allowed 60-second interval, do not widen the tolerance after inspecting prices.

Record the event as unavailable under the candidate rule.

## 6. DST and timezone boundary

The forecast specification is JST-fixed.

Confirm source timestamps can be transformed with timezone-aware code without hard-coded U.S. DST offsets.

Do not infer source timezone from apparent price activity.

## 7. Persistence boundary

Where permitted, preserve:

- raw bounded sample or approved durable representation;
- SHA-256;
- decoded structural sample;
- retrieval receipt.

If raw data may not be committed, preserve the hash, retrieval instructions, structural diagnostics, and retention boundary.

## 8. Pass criteria

Reference-feed source gate may be marked PASS only if:

- exact source identity is established;
- Bid and Ask are both available;
- timestamp semantics are established;
- decoded structure is deterministic;
- no invalid price-side semantics are observed in the bounded sample;
- endpoint selectors are executable under the frozen 60-second rule;
- source identity/hash/provenance can be preserved;
- no market-outcome computation was used to choose or rescue the source.

## 9. Fail / blocked classifications

Use explicit classifications:

- `PASS_SOURCE_GATE`
- `BLOCKED_RETRIEVAL_ENVIRONMENT`
- `BLOCKED_TIMESTAMP_SEMANTICS`
- `BLOCKED_PRICE_SIDE_SEMANTICS`
- `BLOCKED_PERSISTENCE`
- `REJECTED_SOURCE_STRUCTURE`

Do not translate an environment block into a scientific source rejection.

## 10. Output

Write only inside:

`research/lines/usdjpy-overnight-prospective-forecast-v0.1/work/source-qualification/**`

Minimum outputs:

- `RESULT.md`
- `SAMPLE_RECEIPT.json`
- decoder/validator code if required;
- synthetic/source-structure test log.

Do not modify the scientific specification in this packet.
