# Prior Repository Research

Updated: 2026-09-27

## Purpose

systematic trading / quant research / AI-assisted researchの先行GitHubリポジトリを比較し、Knowledge Baseと研究基盤の設計原則を抽出する。

完成形だけでなく、設計変更・失敗・廃止された方法も研究対象とする。

## Review method

各repositoryは [TEMPLATE.md](TEMPLATE.md) を基本形式として記録する。

可能な範囲で以下を確認する。

1. README / docs
2. directory structure
3. current data model
4. experiment lifecycle
5. provenance / reproducibility
6. negative / failed result handling
7. current knowledge vs historical record
8. Issues / Discussions
9. commit history
10. major redesigns / removals
11. AI / agent boundary
12. deterministic computation boundary
13. strengths / limitations
14. transferable lessons
15. choices not to copy

## Completed deep reviews

| Repository | Primary question | Status |
|---|---|---|
| [Trading Second Brain](trading-second-brain.md) | 個人のTrading knowledgeをどう昇格・保持するか | PARTIAL — initial review complete; long-term history insufficient |
| [zestoles/quant](zestoles-quant.md) | 失敗研究、事前登録、provenanceをどう残すか | PARTIAL — deep review complete; rich failure history, short development window |
| [Epsilon Quant Research](epsilon-quant-research.md) | 大規模な研究群をどう整理・探索するか | PARTIAL — deep review complete; 7-month repo history, ~3-month knowledge-brain history |
| [DVC](dvc.md) | lockfile / run manifestが実際に何を保証するか | PARTIAL — core lineage failures independently reproduced on DVC 3.67.1 |
| [RD-Agent](rd-agent.md) | AI研究ループとfinal holdoutの境界 | PARTIAL — current-main source confirms test/backtest feedback enters adaptive loop |

## Candidate scan

Breadth scan: [CANDIDATE_SCAN.md](CANDIDATE_SCAN.md)

21 repositories were screened to identify candidates that can test or contradict the provisional principles rather than merely resemble the current design.

High-priority candidates from the scan:

- microsoft/RD-Agent
- treeverse/dvc
- freqtrade/freqtrade
- microsoft/qlib
- kedro-org/kedro
- nautechsystems/nautilus_trader
- nkaz001/hftbacktest

## Next deep reviews

Current recommended order:

1. **Freqtrade**
   - Test the sensitivity and limits of lookahead detection and simulation/live parity checks.
   - Distinguish a passing diagnostic from proof that no temporal leakage exists.

2. **Qlib or Kedro**
   - Use the result of RD-Agent / Freqtrade to choose whether the next gap is experiment tracking or provenance/versioning architecture.

DVC review is now complete enough for synthesis on its scoped question; further DVC work should target unresolved remote/environment guarantees only if needed.

## Cross-repository principles — evidence strengthening

### Strong candidate: current valid knowledge and historical record should be separated

Observed independently in Trading Second Brain, zestoles/quant, and Epsilon.

Still open: whether current state should be a single projection or multiple domain-specific routing surfaces.

### Strong candidate: past evidence should not be erased to fit the current conclusion

Observed through contradictory evidence retention, invalidated results, archived evidence, parked research, and dated decisions.

### Strong candidate: research state should be staged

Raw observation, exploratory finding, learning, decision, validated state, rejected state, and invalid evidence should not be treated as equivalent.

### Strong candidate: retrieval/navigation should not become canonical evidence

Generated indexes, semantic retrieval, summaries, and lock/status surfaces are useful views, but they should not replace the underlying evidence.

### Strong candidate: provenance artifact existence does not prove provenance correctness

This now has unusually strong evidence across multiple cases:

- zestoles/quant: deterministic measurement code and duplicated collectors produced invalid scientific conclusions despite structured records.
- Epsilon: organized canon and derived datasets still required a separate trust audit that found metric/data defects.
- DVC: on DVC 3.67.1, concurrent code modification was independently reproduced such that the output came from old code while `dvc.lock` recorded the new code hash; a subsequent repro was skipped.

Implication:

```text
recorded provenance
!=
causal provenance
```

A system must state exactly when identity is observed:

- definition time
- execution start
- actual read/use
- save/record time

and should not collapse these into one generic “reproducible” label.

### Strong candidate: knowledge correctness, evidence correctness, and computation correctness require separate checks

Evidence now comes from:

- zestoles/quant — computation/measurement bugs
- Epsilon — canon organization vs evidence trust
- DVC — provenance record vs actual execution lineage

This distinction is becoming central enough to test explicitly in future reviews.

## Important tensions emerging

### A. Current state representation

- Trading Second Brain: few durable summary files
- zestoles/quant: binding current-status document
- Epsilon: multiple canonical routing surfaces

Open question: single current projection vs domain-specific routing surfaces.

### B. Formal schema vs lightweight graph

- zestoles/quant: stronger machine-readable preregistration / ledger / fingerprint model
- Epsilon: flexible Markdown metadata + wikilink + hub graph
- Trading Second Brain: file hierarchy + promotion rules

Open question: how to combine typed lineage with low-friction human readability.

### C. Immutability strength

Artifact types need different guarantees.

Experiment result, decision, forward evidence, current projection, generated index, and raw source should not inherit one blanket “append-only” rule.

### D. Reproducibility guarantee boundaries

DVC demonstrates that a useful lockfile can still have a causal-lineage gap.

Future designs must separate:

- declared definition identity
- input-at-start identity
- actual bytes read
- concurrent-mutation safety
- output identity
- environment identity
- recorded lineage
- rerun behavior

## Synthesis questions

- What is the smallest typed research lineage we need?
- Which relations should be machine-readable: derived_from / supersedes / invalidates / corrects / uses_dataset?
- Which artifacts need content hashes?
- Which artifacts need actual immutable snapshots rather than post-run hashes?
- Should run identity include code/data/environment snapshots?
- How should external mutable data be pinned?
- How should failed runs and scientific negative results be distinguished?
- How should current valid knowledge be derived from history?
- How do we prevent AI retrieval from surfacing historical positive results as current truth?
- How do we record the guarantee boundary of diagnostics such as lookahead checks?
- How do we keep research infrastructure small enough for a personal research repository?

## Exit condition

Move to Knowledge Base v0.1 design only after the evidence is sufficient to separate:

- strong common principles
- plausible but unverified patterns
- conflicting design choices
- project-specific choices

RD-Agent is now reviewed deeply enough for the first cross-repository synthesis. Freqtrade remains the next diagnostic-boundary review.
