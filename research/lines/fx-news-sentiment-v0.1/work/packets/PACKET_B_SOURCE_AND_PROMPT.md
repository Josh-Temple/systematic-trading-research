# Packet B — GDELT source qualification and ChatGPT prompt freeze

## Goal

Make the headline workflow executable without opening the formal EURJPY market-outcome cohort.

## Starting evidence

The 2026-10-07 source preflight has already:

- rejected treating historical DailyFX as a current reproducible route;
- declined Investing.com / FXStreet for the canonical v0.1 input under current preservation constraints;
- identified GDELT title/headline metadata as the preferred open-data candidate.

Do not repeat broad provider search unless GDELT fails a required gate.

## Work

1. Execute the exact GDELT DOC/Article List query in the intended runtime.
2. Verify returned title, URL, source and seen-time fields.
3. Freeze the EUR/JPY-relevant query terms and English-language rule.
4. Freeze 24-hour window semantics ending 08:00 JST.
5. Define MAXRECORDS overflow behavior that fails closed rather than silently truncating.
6. Define exact URL and near-duplicate-title handling.
7. Preserve raw GDELT response bytes + SHA-256 and required attribution.
8. Freeze the exact ChatGPT prompt and JSON output schema.
9. Test prompt parsing using synthetic headlines only.
10. Qualify XM EURJPY Bid/Ask collection, timezone mapping, and account costs.

## Prompt requirements

- forward-looking EUR and JPY implication only;
- fixed enum labels;
- headline/title metadata only;
- no later prices/outcomes;
- no trade recommendation;
- NOT_MENTIONED separate from INSUFFICIENT;
- machine-valid structured output;
- prompt identity hashed and preserved.

## Deliverables

- `SOURCE_QUALIFICATION_RESULT.md`;
- exact GDELT query template;
- source manifest schema;
- frozen prompt + SHA-256;
- output schema;
- XM qualification result;
- amended/final specification fields.

## Stop

If GDELT runtime semantics, result completeness, or exact input preservation cannot be established, record `SOURCE_QUALIFICATION_BLOCKED`. Do not silently switch provider and preserve the same protocol identity.

## Execution result — 2026-10-07

PARTIAL_WITH_GAPS / SOURCE_QUALIFICATION_BLOCKED. See
`../SOURCE_QUALIFICATION_RESULT.md`. Actual HTTP 200 response and 429 comparison
bodies/hashes preserved; prompt/output candidate and source/JSON parser tests ready.
XM requires local MT5. No full Packet B completion or formal freeze granted.
