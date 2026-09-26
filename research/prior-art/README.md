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

1. **RD-Agent**
   - Test the AI research-loop / holdout boundary.
   - Reconstruct whether evaluation results flow back into proposal generation.
   - Separate current main behavior from unmerged PR proposals.

2. **DVC**
   - Test what a run manifest / lockfile actually guarantees.
   - Examine input-at-start identity, concurrent modification, external data drift, and lockfile timing.

3. **Freqtrade**
   - Test the sensitivity and limits of lookahead detection and simulation/live parity checks.
   - Distinguish a passing diagnostic from proof that no temporal leakage exists.

This replaces the earlier assumption that the next review should necessarily be Backtrader MCP. The candidate scan found stronger, more mature counterexamples for the current questions.

## Early observations — not yet synthesized principles

### Observed in Trading Second Brain

- raw observation → revisable learning → explicit decision → durable memory の段階的昇格
- current durable knowledgeとhistorical decision logの分離
- original sourceをAI summaryで置換しない
- fact / observation / hypothesis / rule / decisionを分離する
- repository rootだけをagent permission boundaryにする
- humanが手動分類しすぎず、inboxからAIが整理する

### Observed in zestoles/quant

- machine-readable preregistration + fingerprint
- trial budgetをlineageと一緒に保持
- outputごとのprovenance sidecar
- negative / rejected / unresolvedを残す
- invalid evidenceを削除せずarchiveする
- current binding stateとhistorical resultを分離する
- unmeasurable / incomplete evidenceをPASS扱いしないfail-closed gate
- measurement implementation自体をknown-answer / sensitivity testで監査する
- duplicated execution / collector pathがspec driftを起こし、single code pathへ統合された
- “append-only”はartifact typeごとに保証強度が異なり、READMEの理念だけでは不十分

### Observed in Epsilon Quant Research

- VAULT_MAP → project map → strategy hub → findings/history の多段navigation
- TODO / active canon / STATUS と、TODO_ARCHIVE / historical findings / LOG / reports の分離
- generated hygiene indexとsemantic/graph retrievalをcanonical sourceにしない
- duplicate basename、orphan、broken link、stale TODO等をscannerで監査する
- large dataは個別shardではなくdataset family manifestでmapする
- scratchとdurable findingを分離する
- knowledge canon auditとevidence trust auditを別工程として扱う
- read-only / disposableなAI retrieval indexを使う
- NEXT / STATUS / LOG / reports でlong-running handoffの「現在」と「履歴」を分離する
- well-organized knowledge baseでもunderlying evidenceが誤っている可能性があり、data / metric / provenanceを独立監査する
- Obsidian Relay、flat note layout、overgrown TODO、scattered roots、first-corrupt-shard abort等を実運用上の問題から廃止・再設計した

## Three-repository convergence — provisional but stronger

以下は3つの独立repositoryで方向性が一致したため、Knowledge Base v0.1の有力候補原則として扱う。ただしschemaへはまだ固定しない。

1. **Current valid knowledge と historical record を分離する**
   - Trading Second Brain: MEMORY / LEARNINGS / dated decisions
   - zestoles/quant: current binding status / historical reports / archived invalid evidence
   - Epsilon: TODO / active canon / STATUS と TODO_ARCHIVE / findings / LOG / reports

2. **過去の証拠を現在の説明に合わせて消さない**
   - contradictory evidence、invalidated result、parked research、old decisionを保持する。

3. **研究状態を段階化する**
   - raw observation、exploratory finding、learning、decision、validated stateを同一視しない。

4. **Navigation / retrieval layerをcanonical evidenceそのものにしない**
   - Trading Second Brain: sourceをAI summaryで置換しない
   - zestoles/quant: generated reports / current stateとmachine evidenceを分離
   - Epsilon: generated indexes / gbrainをread-only derived layerに限定

5. **Knowledge organization と evidence validity を別々に監査する**
   - zestoles/quant: deterministic measurement implementation自体のbugが研究結論を変えた
   - Epsilon: canon整理後でもmetric mismatch / derived dataset defectが発見された
   - implication: 「整理されている」「再現できる」だけで科学的妥当性を保証しない

## Important tensions emerging

### A. Current state representation

- Trading Second Brain: 少数のdurable summary files
- zestoles/quant: binding current-status document
- Epsilon: 複数のcanonical routing surfaces

→ single current projectionとdomain-specific routing surfacesのどちらが適切か、さらに比較が必要。

### B. Formal schema vs lightweight graph

- zestoles/quant: preregistration / ledger / fingerprint等のmachine-readable modelが強い
- Epsilon: Markdown metadata + wikilink + hubによる柔軟なknowledge graphが強い
- Trading Second Brain: file hierarchy + promotion rulesが中心

→ systematic-trading-researchでは、human readabilityとtyped lineageの両立方法が主要論点。

### C. Immutability strength

- artifact typeによって必要なimmutabilityが異なる。
- “append-only repository”のような一括ルールではなく、experiment result、decision、forward evidence、current projectionごとに要件を定義する必要がある可能性が高い。

### D. Reproducibility guarantees may be weaker than their artifacts suggest

The candidate scan adds a new cross-cutting question:

- a lockfile may not guarantee input-at-start identity,
- a lookahead diagnostic may not prove absence of leakage,
- an AI research loop may still leak holdout information back into proposal generation.

The existence of a control artifact is therefore not enough; its actual guarantee must be tested.

## Synthesis questions

個別レビュー後、次を横断的に検討する。

- 複数repositoryで共通して残っている設計は何か
- 途中で撤回・簡素化された設計は何か
- research artifactの最小単位は何か
- current stateとhistoryをどう分けるか
- negative/null resultをどう発見可能にするか
- provenanceをどこまで機械可読にするか
- schemaを厳格にしすぎると何が壊れるか
- AIへ公開する知識と決定論的engineへ残す処理の境界はどこか
- Web UI / search / MCPはどの段階で導入するか
- 自分たちの研究規模で不要な複雑性は何か
- current statusはsingle projectionか、複数domain routing surfaceか
- supersedes / invalidates / corrects / derived_from をmachine-readable relationにするか
- append-only / immutabilityをどのartifact typeまで要求するか
- measurement implementationの検証をexperiment contractへ含めるか
- AI retrieval時にhistorical positive resultとcurrent invalid stateの取り違えをどう防ぐか
- generated index / semantic indexをcanonicalからどこまで切り離すか
- graph hygiene scannerをどの規模から導入するか
- knowledge canon auditとevidence trust auditを独立工程として設計するか
- datasetがCONDEMNEDになったときdownstream experimentをどうinvalidateするか
- long-running AI handoffにNEXT / STATUS / LOG / reportの分離が必要か
- run manifest / lockfileがinput-at-start identityを本当に保証するか
- diagnostic PASSを「問題不存在の証明」と誤解しないために、検査の感度と既知のblind spotをどう保存するか
- AI research loopでvalidation feedbackとfinal holdoutをどう隔離するか

## Exit condition

複数の異なる先行例から、

- strong common principles
- plausible but unverified patterns
- conflicting design choices
- project-specific choices

を分けて記録できた時点で、Knowledge Base v0.1のschema設計へ進む。
