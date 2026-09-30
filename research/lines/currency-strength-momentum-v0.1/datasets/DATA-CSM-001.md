---
id: DATA-CSM-001
type: Dataset
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: PLANNED_SOURCE_QUALIFICATION
scientific_role: EXPLORATORY_DISCOVERY
provider: European Central Bank
dataset_family: EXR
frequency: DAILY_REFERENCE_RATE
start_boundary: 1999-01-04
end_boundary: 2026-09-30
relations: []
---

# ECB major-currency daily reference-rate source

## Planned source

European Central Bank Data Portal / Data API, EXR daily reference-rate series.

Frozen currency series:

- AUD/EUR
- CAD/EUR
- CHF/EUR
- GBP/EUR
- JPY/EUR
- NZD/EUR
- USD/EUR

EUR is represented as the numeraire.

## Source limitation

ECB states that its euro foreign exchange reference rates are published for information purposes. They are averages of buying and selling rates and do not necessarily reflect rates at which market transactions occurred.

Therefore this dataset is suitable for a first price-phenomenon screen but not for claiming executable net profitability.

## Required qualification before outcome calculation

Record:

- exact retrieval URL or API query
- retrieval timestamp
- returned series keys
- observed first/last date for every series
- missing observation counts
- raw artifact identity
- SHA-256 of the preserved raw artifact
- transformation code identity

If any frozen currency series is unavailable over a material portion of the required period, stop and record the source limitation. Do not silently substitute FRED, broker data, synthetic crosses, or another provider inside v0.1.
