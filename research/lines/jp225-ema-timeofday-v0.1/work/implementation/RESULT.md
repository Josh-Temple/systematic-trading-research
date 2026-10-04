---
id: RESULT-JP225-EMA-B-20261003
type: WorkResult
packet_id: PKT-JP225-EMA-B
research_line_id: RL-JP225-EMA-001
status: COMPLETE
scientific_status: NOT_APPLICABLE
market_outcome_access: false
---

# Packet B — Outcome-blind implementation result

## Result

COMPLETE after self-audit repair.

The frozen calculation semantics were implemented with Python standard-library code and exercised only against synthetic fixtures. No JP225, Nikkei, XM historical, proxy-index, discovery, or holdout market data was loaded.

## Implemented

- recursive EMA with frozen seed and alpha semantics;
- EMA5/EMA200 crossover;
- close/EMA200 comparator;
- Asia/Tokyo open/close/night flags;
- America/New_York cash-open flag using IANA DST rules;
- directional BID/ASK entry and exit mapping;
- +5/+15/+30-compatible horizon mapping;
- explicit missing-entry and missing-target statuses;
- event-window overlap count/share diagnostic;
- date-cluster bootstrap with fixed seed;
- discovery advancement criteria and tie rule;
- holdout authorization lock;
- holdout decision gate.

## Test result

21/21 unit tests PASS across the two test modules.

Commands:

`python -m unittest -v test_jp225_ema_screen.py`

`python -m unittest -v test_overlap_diagnostics.py`

The first implementation pass had 20 tests. A self-audit found that the specification required an explicit event-overlap diagnostic but the initial code did not expose one. That gap was repaired before any market data was accessed, and a 21st synthetic test was added.

See `TEST_LOG.txt`.

## Important limitation

This implementation deliberately does not parse raw XM exports yet. Raw schema, timestamp/server-time semantics, chart-bar identity, and actual tick availability belong to Packet A source qualification. Writing a parser before those are established would silently embed source assumptions.

## Scientific interpretation

NOT_APPLICABLE. Passing implementation tests says nothing about whether the strategy has an edge.

## Next gate

Packet C remains locked until Packet A independently establishes a usable XM signal + BID/ASK execution source.
