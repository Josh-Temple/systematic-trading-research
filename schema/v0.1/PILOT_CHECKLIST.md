# Knowledge Base v0.1 Pilot Checklist

Pilot: Horizontal Reaction Strategy v0.1

## A. Lineage completeness

- [ ] ResearchLine exists.
- [ ] Original/frozen hypothesis is represented.
- [ ] Governing specification(s) are represented and versioned.
- [ ] Every materially different dataset/source pack is identified.
- [ ] Intended experiments are separate from concrete run attempts.
- [ ] Failed/blocked run attempts are preserved.
- [ ] Results contain no post-hoc interpretation inside the observation section.
- [ ] Interpretations reference the Results they interpret.
- [ ] Decisions reference their evidence/interpretations.
- [ ] CURRENT.md derives from explicit Decision / Interpretation IDs.

## B. Scientific boundary

- [ ] 2026H1 consumed-sample status is explicit.
- [ ] No used sample is mislabeled as unused/final holdout.
- [ ] exploratory diagnostics are not labeled confirmatory.
- [ ] failed source-access/replay attempts are not labeled negative strategy results.
- [ ] later corrections/replays do not erase earlier failed attempts.
- [ ] next admissible test is distinguishable from prohibited rescue search.

## C. Provenance

- [ ] provider/instrument/time/granularity are captured where known.
- [ ] BID/ASK and timestamp semantics are captured where relevant.
- [ ] source identity/hash evidence is referenced.
- [ ] run manifests state what provenance guarantees are actually captured.
- [ ] UNKNOWN remains UNKNOWN where causal provenance was not established.

## D. Status separation

For every key Result:

- [ ] execution status is present.
- [ ] evidence validity is present.
- [ ] scientific status is present.

Check that the following can be represented differently:

- [ ] execution failed
- [ ] evidence invalid
- [ ] hypothesis not supported
- [ ] evidence inconclusive
- [ ] interpretation superseded

## E. Diagnostic scope

- [ ] exploratory diagnostics record their checked scope.
- [ ] diagnostic PASS/FAIL does not imply more than was checked.
- [ ] untested dimensions are explicit.
- [ ] formal D1-D5 diagnostics are distinguishable from approximate/exploratory comparisons.

## F. Human usability

From GitHub alone, a reviewer should be able to answer in under 10 minutes:

- [ ] What was tested?
- [ ] What happened?
- [ ] Which evidence is currently valid?
- [ ] What failed operationally?
- [ ] What is the current interpretation?
- [ ] What sample is consumed?
- [ ] What test is allowed next?

## G. AI retrieval safety

A fresh AI session reading only this research line should not:

- [ ] treat historical positive observations as current support
- [ ] treat invalidated evidence as valid
- [ ] treat a blocked run as a negative scientific result
- [ ] treat a consumed holdout as unused
- [ ] treat a diagnostic PASS as universal proof
- [ ] infer missing provenance guarantees

## Exit

Phase 3 pilot passes only after this checklist is exercised on the real Horizontal Reaction migration.

Schema changes discovered during the pilot must be recorded with the concrete failure they solve.
