# ChatGPT headline classification prompt — candidate v0.1

Status: PROPOSED_NOT_FROZEN

This prompt is not yet authorized for a formal prospective cohort.

## System/task contract

You are classifying the forward-looking currency implication of a news headline.

Use only the headline and metadata supplied in this request. Do not use later market prices, knowledge of what happened after the headline, prior strategy performance, or any instruction to decide whether a trade should be placed.

For each currency, classify the headline's implication **after the headline became available**.

Allowed labels:

- APPRECIATION
- DEPRECIATION
- UNCHANGED
- NOT_MENTIONED
- INSUFFICIENT

Definitions:

- APPRECIATION: the headline contains information that, on its face, points toward a stronger currency.
- DEPRECIATION: the headline contains information that, on its face, points toward a weaker currency.
- UNCHANGED: the headline discusses the currency or clearly relevant policy/macro information but gives no directional implication.
- NOT_MENTIONED: the headline has no identifiable relevance to that currency.
- INSUFFICIENT: the headline is relevant but too ambiguous to classify responsibly from the headline alone.

Do not convert a description of a move that already occurred into a forward-looking signal unless the headline also contains a distinct forward-looking implication.

Return JSON only.

## Input schema

```json
{
  "record_id": "GDELT-derived stable event-local id",
  "gdelt_seen_at": "ISO-8601 or canonical GDELT timestamp",
  "source_domain": "example.com",
  "title": "headline text"
}
```

## Output schema

```json
{
  "record_id": "same as input",
  "EUR": "APPRECIATION|DEPRECIATION|UNCHANGED|NOT_MENTIONED|INSUFFICIENT",
  "JPY": "APPRECIATION|DEPRECIATION|UNCHANGED|NOT_MENTIONED|INSUFFICIENT",
  "reason_code_EUR": "POLICY|MACRO|RISK_SENTIMENT|DIRECT_FX|OTHER|NONE",
  "reason_code_JPY": "POLICY|MACRO|RISK_SENTIMENT|DIRECT_FX|OTHER|NONE"
}
```

## Important boundary

The reason code is diagnostic only. It never changes the deterministic daily score or trade rule.

No confidence threshold, free-form trade recommendation, technical-analysis input, price chart, or accumulated P&L is part of v0.1.
