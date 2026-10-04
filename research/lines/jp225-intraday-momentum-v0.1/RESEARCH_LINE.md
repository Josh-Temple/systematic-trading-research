---
id: RL-JP225-IMOM-001
type: ResearchLine
created_at: 2026-10-04
status: PRE_OUTCOME
---

# JP225 / Nikkei 225 Intraday Momentum v0.1

## Question

Does a literature-motivated same-day intraday momentum relation survive on official OSE Nikkei 225 mini transaction data in a post-literature, previously uninspected sample?

The frozen primary relation is:

- early information return: previous eligible TSE day 15:30 JST -> current eligible TSE day 09:30 JST;
- late-day return: current day 15:00 JST -> 15:30 JST;
- same Nikkei 225 mini quarterly front contract;
- positive early return should predict positive late-day return, and negative early return should predict negative late-day return.

## Scientific boundary

This line is separate from:

- the XM `JP225Cash` EMA5/EMA200 line;
- the stopped 2015 U.S.-lead reversal proxy line;
- all consumed OANDA midpoint EMA proxy samples.

It cannot unlock the XM Packet C gate or the XM 2026 holdout.

## Source

Intended source: official JPX/OSE historical Nikkei 225 mini transaction ticks through J-Quants DataCube.

The source is true OSE transaction-price evidence, not BID/ASK execution evidence. Raw-data storage/processing follows the source contract and license boundary.

## Samples

- confirmation: calendar 2025, one-shot;
- holdout: 2026-01-01 through 2026-09-30, physically/logically unopened until 2025 advancement.

No 2024 or earlier market outcomes are needed for v0.1.

## Current state

Architecture/specification only. No DataCube market data has been acquired or inspected for this line.
