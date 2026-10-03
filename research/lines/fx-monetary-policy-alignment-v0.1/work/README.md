# Work plan — FX monetary-policy alignment v0.1

## Completed pre-outcome work

### Packet A — BIS source qualification
Status: **PARTIAL_WITH_GAPS**

See `source-qualification/RESULT.md`.

### Packet B — scientific prior-art review
Status: **PARTIAL_WITH_GAPS**

See `literature/RESULT.md`.

## Next packets

### Packet C — raw source lock and coverage audit

Goal:
- retrieve official BIS WS_CBPOL bytes;
- hash the raw artifact;
- isolate M.AU/M.CA/M.CH/M.XM/M.GB/M.JP/M.NZ/M.US;
- inspect only predictor-source coverage/status/missingness;
- encode source break metadata;
- no FX price/outcome access.

### Packet D — outcome-blind implementation

Only after Packet C identifies exact raw semantics.

Implement:
- exact decimal policy changes;
- break-crossing detection;
- unavailable reason codes;
- deterministic feature-ledger serialization;
- synthetic tests proving future/outcome independence.

No market outcomes.

### Packet E — independent audit

Independently verify C/D identities and synthetic behavior.

### Packet I — integration and human freeze

Resolve source gaps and explicitly obtain the human decision on:
- 3-month policy-rate lookback;
- 24/24 group minimum;
- exact inference seed/algorithm;
- final source/break lock.

### Packet X — one-shot exploratory execution

Forbidden until I explicitly opens the outcome gate.

### Packet R — interpretation

Separate fact, interpretation and decision. A positive retrospective result is not confirmation and requires separate unused/prospective evidence.
