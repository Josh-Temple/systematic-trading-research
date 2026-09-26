# Cross-Repository Synthesis v0.2

Updated: 2026-09-27

## Scope

This synthesis compares:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research
- DVC
- RD-Agent
- Freqtrade

It supersedes `SYNTHESIS_V0.1.md` as the current prior-art synthesis, while v0.1 remains historical evidence.

This document defines design constraints for Phase 2. It does **not** define the final Knowledge Base schema.

---

## 1. Strong common principles

### P1. Separate current valid knowledge from historical research

Evidence across Trading Second Brain, zestoles/quant, Epsilon, and RD-Agent supports a common distinction between:

- durable/current state,
- revisable interpretation,
- dated decisions,
- historical experiment/evidence records.

Decision for Phase 2:

The Knowledge Base must preserve history and expose current state separately.

The exact current-state projection mechanism remains a Phase 2 design choice.

---

### P2. Preserve negative, rejected, invalidated, failed, and insufficient-evidence states

These are not equivalent.

Phase 2 must not collapse them into one generic failure status.

At minimum, the model needs to distinguish:

- scientific rejection,
- insufficient evidence,
- invalid evidence,
- execution/infrastructure failure,
- superseded interpretation.

---

### P3. Keep research states distinct

The minimum scientific lineage must distinguish:

```text
Hypothesis
→ Frozen Specification
→ Experiment / Run
→ Result
→ Interpretation
→ Decision
→ Current State
```

A result is not an interpretation.
An interpretation is not a decision.
A decision must not rewrite the historical result.

---

### P4. Provenance records must declare their guarantee boundary

DVC provides the strongest direct reproduction.

A provenance file can record a hash while still misrepresenting the actual causal input that produced an output.

Therefore Phase 2 must avoid fields such as:

`reproducible: true`

without scope.

Prefer explicit guarantees:

- definition identity captured
- code identity at execution start captured
- input snapshot captured
- external data pinned
- environment captured
- output identity captured
- concurrent mutation prevented
- causal lineage independently checked

Unknown must remain unknown.

---

### P5. Separate knowledge correctness, evidence correctness, and computation correctness

These are independent dimensions.

```text
knowledge correctness
evidence correctness
computation correctness
```

Examples from prior art:

- Epsilon: organized canon, later evidence defect.
- DVC: metadata record, causal-lineage mismatch.
- zestoles/quant: repeatable computation, wrong scientific calculation.
- RD-Agent: valid experiment trace, contaminated evaluation boundary.
- Freqtrade: deterministic diagnostic agreement, semantic timing still potentially invalid.

Phase 2 must not use one generic VERIFIED flag to represent all three.

---

### P6. Final holdout must be outside adaptive search

RD-Agent demonstrates that a dataset called `test` is not a final holdout if its metrics influence:

- LLM feedback,
- next hypothesis,
- SOTA selection,
- bandit/action selection,
- parameter or strategy changes.

Phase 2 must encode dataset role and whether a result may influence future search.

Minimum roles:

- development
- adaptive_validation
- final_holdout
- consumed_holdout
- historical_only

A final-holdout result must not silently become adaptive input.

---

### P7. AI permission boundaries include information visibility and decision authority

The relevant boundary is not merely:

`AI vs code`

It is:

```text
AI proposal
→ deterministic computation
→ adaptive validation feedback
→ scientific promotion gate
→ final holdout
→ durable decision
```

For each stage, Phase 2 should be able to state:

- what data was visible,
- what state could be changed,
- whether the result was allowed to influence future search.

---

### P8. Diagnostic PASS is bounded evidence, not absence proof

Freqtrade adds a new strong principle.

Its `lookahead-analysis` can detect differences between:

- a full backtest,
- and shortened reruns around selected trades.

But PASS does not establish universal absence of temporal leakage.

The component reproduction showed that if the same semantically unavailable higher-timeframe value appears identically in both compared dataframes, column equality does not detect the availability-time violation.

Therefore:

```text
diagnostic PASS
!=
problem absence
```

Phase 2 should store:

- diagnostic name/version,
- scope checked,
- coverage/sample,
- overrides,
- known blind spots,
- untested dimensions,
- result.

---

### P9. Temporal availability semantics are part of experiment specification

Freqtrade's higher-timeframe case makes this explicit.

A feature value can be numerically present in a dataframe yet not have been available at decision time.

Therefore experiment specification must be able to describe:

- event timestamp,
- information-available timestamp,
- candle-close semantics,
- resampling/merge rule,
- signal decision timestamp,
- execution timestamp.

For the first Horizontal Reaction pilot, only the relevant subset should be implemented; do not build a universal temporal ontology yet.

---

### P10. Backtest correctness and live-execution parity are separate questions

Freqtrade's lookahead-analysis compares backtests with backtests.

Its diagnostic path also changes execution settings such as order types.

Therefore a clean diagnostic does not establish:

- live signal parity,
- fill parity,
- slippage realism,
- fee parity,
- external-state parity.

Phase 2 must allow a result to declare which environment it supports.

---

### P11. Retrieval/navigation is a derived interface, not evidence authority

Across the reviewed repositories:

- summaries,
- maps,
- generated indexes,
- semantic search,
- diagnostic tables,
- lock/status files

are useful interfaces but should not replace underlying canonical evidence.

Future Web UI / MCP should remain projections over the research record.

---

## 2. Minimum typed lineage for Phase 2

Phase 2 should begin with the smallest structure capable of representing one complete research line.

Required entity types:

1. **ResearchLine**
2. **Hypothesis**
3. **Specification**
4. **Dataset**
5. **Experiment**
6. **Run**
7. **Result**
8. **Interpretation**
9. **Decision**

Optional/generated surfaces should not be canonical entities initially:

- CURRENT.md
- indexes
- web pages
- semantic search index
- MCP responses

---

## 3. Required relations

At minimum, Phase 2 must test whether these relations are sufficient:

- `tests_hypothesis`
- `uses_specification`
- `uses_dataset`
- `produced_by_run`
- `interprets_result`
- `supports`
- `contradicts`
- `supersedes`
- `invalidates`
- `corrects`
- `derived_from`

Do not introduce more relation types unless the Horizontal Reaction pilot requires them.

---

## 4. Required independent status dimensions

A result or experiment should not have one flat status.

Test at least these dimensions:

### Execution status

- NOT_RUN
- SUCCESS
- FAILED
- BLOCKED

### Evidence validity

- VALID
- INVALID
- PARTIAL
- UNVERIFIED

### Scientific status

- EXPLORATORY
- TESTING
- SUPPORTED
- NOT_SUPPORTED
- INCONCLUSIVE
- SUPERSEDED

The exact vocabulary may change during the pilot.

The requirement is separation, not these exact labels.

---

## 5. Dataset / evidence role

Every dataset use should declare a role.

Candidate minimal roles:

- DEVELOPMENT
- ADAPTIVE_VALIDATION
- FINAL_HOLDOUT
- CONSUMED_HOLDOUT
- HISTORICAL_ONLY

Also record:

- whether result may influence future search,
- whether the data role has been consumed,
- source/provenance identity,
- relevant time window.

---

## 6. Run identity / provenance boundary

Phase 2 should test a compact run manifest containing only meaningful fields.

Candidate fields:

- run_id
- specification_id
- code_commit
- dataset_id
- dataset_role
- input_snapshot_or_hash
- environment_ref
- started_at
- completed_at
- output_artifact_refs
- output_hashes
- provenance_guarantees
- diagnostic_refs

Do not claim causal provenance when only post-run state was observed.

---

## 7. Diagnostic result model

Freqtrade shows that diagnostics need scope.

Candidate diagnostic fields:

- diagnostic_id
- diagnostic_type
- tool/version
- target_run
- checked_scope
- sample/coverage
- overrides
- result
- known_blind_spots
- not_tested
- evidence_refs

A PASS result must not be represented without its scope.

---

## 8. Current-state projection

Phase 2 should test this model:

```text
historical canonical entities
+ explicit decisions/corrections
→ generated CURRENT.md
```

CURRENT.md should be treated as a projection, not the authority.

If this is too cumbersome for Horizontal Reaction, revise after the pilot rather than adding more infrastructure.

---

## 9. Human-readable + machine-readable hybrid

Evidence supports neither pure free-form Markdown nor a heavy database-first ontology.

Phase 2 should test:

- Markdown for rationale, interpretation, and decisions,
- compact structured frontmatter or sidecar metadata for IDs/status/relations,
- generated index/current views.

Do not add a graph database or vector database in v0.1.

---

## 10. What not to build in Phase 2

Do not build:

- MCP
- vector DB
- graph DB
- complex web UI
- multi-agent framework
- live trading integration
- generalized universal schema

Phase 2 exists to validate the research representation on one real research line.

---

## 11. Phase 2 pilot target

Use **Horizontal Reaction Strategy v0.1** because it contains:

- frozen specification,
- source/data recovery history,
- consumed sample,
- negative result,
- exploratory diagnostics,
- failed/blocked replay history,
- later successful replay/integration,
- current interpretation,
- subsequent holdout work.

This makes it suitable for testing:

- supersession,
- invalidation,
- historical/current separation,
- data-role boundaries,
- negative evidence,
- failed execution vs scientific result,
- provenance.

---

## 12. Phase 1 exit decision

### Evidence sufficiency

The six deep reviews cover materially different failure classes:

- knowledge promotion
- preregistration / trial control
- large-scale knowledge organization
- causal provenance
- AI adaptive-loop / holdout leakage
- diagnostic guarantee boundaries

The breadth scan also identified further candidates, but no remaining candidate is currently necessary to answer the minimum Phase 2 design questions.

### Qlib / Kedro decision

**DEFER**

Reason:

Additional review may improve details, but no material evidence gap currently blocks a minimal Horizontal Reaction schema pilot.

### Phase 1 result

`PHASE_1_EXIT = PASS`

The project may proceed to Knowledge Base v0.1 design.

---

## 13. Synthesis status

`SYNTHESIS_STATUS = PHASE_1_FINAL_V0.2`

This synthesis is sufficient for Phase 2 entry.

It is not a claim that the architecture is permanently settled.

New evidence from the Horizontal Reaction pilot may require revising these constraints.
