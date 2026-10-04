# Packet D — 2026 holdout

Locked until both are present and identity-pinned:

1. a durable 2025 confirmation decision with `IMOM_ADVANCE_TO_2026_HOLDOUT`; and
2. a separate independent review receipt with `status=PASS`, `independent_review=PASS`, scope `2026_HOLDOUT_UNLOCK`, exact decision SHA-256 and exact decision binding.

Before both receipts validate, no 2026 raw market file may be acquired, opened, parsed, counted, plotted or summarized for this line. The holdout loader must verify both receipts before it invokes the data reader.

If unlocked:

- use only 2026-01-01 through 2026-09-30;
- use the exact frozen v0.1 definitions plus the pre-outcome v0.1.1 hardening amendment;
- do not retune any clock, contract, threshold, sample or filter;
- write one terminal holdout classification.

No secondary result can rescue a failed holdout.
