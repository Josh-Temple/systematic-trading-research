# Packet B — Outcome-blind implementation

Role: deterministic implementation worker.

Implement only the frozen specification using synthetic fixtures.

Required:

- quarterly-front contract calendar selection;
- roll-transition exclusion;
- exact four-boundary +60-second transaction mapping;
- early/late return calculation;
- OLS beta;
- fixed LCG bootstrap for beta;
- sign translation;
- fixed LCG bootstrap for gross mean;
- one-shot 2025 runner;
- durable sample-consumption marker;
- 2026 holdout loader that checks a bound advancement receipt before opening any holdout file.

Tests must include boundary timestamps, missing trades, ambiguous same-time trades, contract-roll dates, zero predictor variance, tampered receipts and holdout-reader-not-called cases.

Do not use market data in this packet.
