# Packet B — Source qualification and prompt freeze

## Goal

Make the workflow executable without opening the formal market-outcome cohort.

## Work

1. Evaluate candidate news providers for timestamp/provenance/legal preservation.
2. Choose the smallest source set that can be reproduced prospectively.
3. Define deduplication and article-update rules.
4. Define the exact ChatGPT prompt and JSON/schema output.
5. Test prompt parsing only on synthetic/artificial news passages or source examples that are not paired with market outcomes.
6. Qualify XM EURJPY Bid/Ask collection, timestamp mapping and account costs.
7. Write final source-lock identities and fail-closed rules.

## Prompt requirements

The final prompt must:

- ask only for forward-looking EUR and JPY implications;
- forbid use of market outcomes or knowledge of later price moves;
- use fixed enum labels;
- return valid structured output;
- separate NOT_MENTIONED from INSUFFICIENT;
- not ask ChatGPT whether to trade.

## Deliverables

- qualified source matrix;
- frozen prompt + hash;
- structured-output schema;
- source manifest format;
- XM qualification result;
- revised specification fields that are currently unresolved.

## Stop

If publication timing or input identity cannot be preserved well enough, record `SOURCE_QUALIFICATION_BLOCKED` and do not create a workaround with unqualified providers.
