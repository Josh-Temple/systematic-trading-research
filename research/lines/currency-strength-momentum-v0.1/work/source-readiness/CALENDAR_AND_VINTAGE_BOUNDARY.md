---
id: CSM-SOURCE-CALENDAR-VINTAGE-20261004
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-04
status: QUALIFIED_FOR_FROZEN_CLAIM_SCOPE
scientific_status: NOT_APPLICABLE
market_outcome_access: false
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-004-METADATA-SOURCE-READINESS-20261004
---

# External calendar authority and vintage boundary

## Calendar authority

Official ECB sources establish both links required by the fixed expected-calendar rule:

1. ECB euro foreign exchange reference-rate methodology states that reference rates are normally updated on every working day except TARGET closing days.
   - https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html
   - https://data.ecb.europa.eu/methodology/exchange-rates

2. The ECB long-term TARGET calendar decision states that from 2002 until further notice TARGET is closed, in addition to weekends, on:
   - 1 January;
   - Good Friday;
   - Easter Monday;
   - 1 May;
   - 25 December;
   - 26 December.
   - https://www.ecb.europa.eu/press/pr/date/2000/html/pr001214_4.en.html

Current T2 documentation continues the same EUR closing-day set:
- https://www.ecb.europa.eu/paym/target/t2/html/index.en.html

Therefore the deterministic Packet C calendar rule is directly supported by official ECB/TARGET authority for the scientific date grid.

This authority defines expected publication/operating dates. It does not by itself prove that all seven observations exist on every expected date; the metadata-only full-history check addresses actual coverage separately.

## Publication and vintage boundary

Current ECB methodology states that the reference rates are normally published around 16:00 CET on working days and are based on the daily concertation procedure earlier in the day.

Packet C also recorded legacy series metadata referring to an older setting-time convention. Exact historical dissemination timestamps, methodology continuity at intraday resolution, and a point-in-time vintage archive for every historical observation remain unverified.

This uncertainty is retained. It is **not silently converted into a real-time availability claim**.

## Why vintage uncertainty is not an execution blocker for this frozen experiment

The accepted and frozen `SPEC-CSM-002-v01` does not test a historical real-time trading rule.

Its accepted claim is explicitly:
- retrospective;
- latest-vintage;
- synchronous reference-to-reference association;
- not a same-day tradability claim;
- not an information-set or causal-availability claim;
- not a net-profitability claim.

Therefore point-in-time historical publication/vintage availability is not required to calculate the exact frozen estimand.

For this experiment:
- latest-vintage official ECB history may be used if source identity, full-period coverage, statuses and immutable snapshot identity pass;
- historical release/vintage uncertainty remains a mandatory interpretation limitation;
- it continues to block any later claim that the historical signal was executable with contemporaneously public information.

## Qualification

- external calendar authority for the fixed expected-date rule: **PASS**
- current publication-process description: **PASS**
- historical point-in-time publication/vintage reconstruction: **UNVERIFIED**
- impact on frozen retrospective latest-vintage association: **LIMITATION, NOT EXECUTION BLOCKER**
- impact on causal/real-time/executable claim: **BLOCKING**
