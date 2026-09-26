# Roadmap

Updated: 2026-09-26

## Goal

GitHubをsystematic trading researchの構造化知識の正本とし、将来的に次の3つを同じ基盤から利用できる状態を目指す。

1. 人間が研究経緯と現在の知識を理解・探索できるWeb UI
2. AIが必要な知識だけを取得できる検索 / MCP interface
3. 再現可能な実験・データ・provenanceを持つ研究基盤

ただし、WebやMCPを先に作らない。まず知識の構造と研究方法を検証する。

---

## Phase 0 — Foundation

Status: **COMPLETE**

### Objectives

- repositoryの目的と境界を固定する
- 既存Trading研究から引き継ぐ研究原則を明文化する
- 先行repository研究の方法を固定する
- 大規模なschema設計を始める前に、比較材料を蓄積する

### Deliverables

- README
- RESEARCH_PRINCIPLES
- このROADMAP
- prior-art research index
- prior-art review template

### Exit condition

Phase 1を同じ形式で開始でき、研究原則と正本の位置づけに曖昧さがないこと。

Result: **PASS**

---

## Phase 1 — Prior repository research

Status: **IN PROGRESS**

### Purpose

完成形だけを模倣せず、先人がどの問題に直面し、何を変更・廃止・維持したかを理解する。

### Initial candidates

- Trading Second Brain — initial review recorded
- zestoles/quant
- Epsilon Quant Research
- Backtrader MCP
- mcp-strategy-research-db
- Trade Terminal
- その他、調査中に見つかる高品質な候補

### Minimum review scope

各repositoryについて、可能な範囲で以下を確認する。

- README / docs
- directory structure
- data model / schema
- experiment lifecycle
- provenance
- negative / failed experiment handling
- current vs historical knowledge separation
- issues / discussions
- commit history
- major redesigns / removed approaches
- AI / agent boundary
- deterministic execution boundary
- strengths / limitations
- transferable lessons
- non-transferable project-specific choices

### Synthesis

個別事例の列挙では終わらせず、複数repositoryに共通する設計原則と、対立する設計選択を分けて記録する。

### Exit condition

少なくとも複数の異なる設計思想を比較し、Knowledge Base v0.1を作るための根拠が揃っていること。

---

## Phase 2 — Knowledge Base v0.1

Status: **PLANNED**

先行研究の結果から、最小schemaを設計する。

初期候補:

- knowledge/
- hypotheses/
- strategies/
- experiments/
- decisions/
- data/
- references/

中心となる関係の候補:

Concept
→ Hypothesis
→ Strategy Specification
→ Experiment
→ Result
→ Interpretation
→ Decision

重要: 最終schemaはPhase 1前に固定しない。

### Exit condition

1本の研究lineageを無理なく表現できる最小構造が定義されていること。

---

## Phase 3 — Horizontal Reaction pilot migration

Status: **PLANNED**

Horizontal Reaction Strategy v0.1を最初の完全移植対象にする。

移植対象には、可能な範囲で以下を含める。

- hypothesis
- preregistration / frozen specification
- data identity / provenance
- source pack
- experiment
- result
- exploratory diagnostics
- confirmatory boundary
- negative / null evidence
- rejected explanations
- current interpretation
- next test
- consumed-sample / holdout boundary

### Evaluation question

「以前より、研究経緯・現在の知識・未解決点を人間とAIが正確に追いやすくなったか」

### Exit condition

Horizontal ReactionをGitHubだけで追跡して、研究状態を誤解なく再構成できること。

---

## Phase 4 — Human-facing web UI

Status: **PLANNED**

Phase 3でKnowledge Base自体の価値が確認できた後に着手する。

初期画面候補:

- Home
- Research Lines
- Strategies
- Experiments
- Knowledge
- Data Sources
- Decisions
- Failed / Rejected

目的は見栄えではなく、研究経緯・根拠・現在状態を短時間で理解できること。

---

## Phase 5 — Index and retrieval

Status: **PLANNED**

知識量が増えてからindexを整備する。

候補:

- strategy index
- hypothesis index
- experiment index
- dataset index
- status index
- related research links

「軽量indexを先に読み、必要な本文だけ取得する」方式を優先して検証する。

---

## Phase 6 — AI interface / MCP

Status: **PLANNED**

Knowledge Baseとindexが安定してから検討する。

tool候補:

- search_hypotheses
- get_strategy
- get_experiment
- get_dataset_provenance
- get_current_decisions
- get_rejected_hypotheses
- find_related_experiments

MCPは正本ではなく、正本へのAI向けinterfaceとして扱う。

---

## Phase 7 — Broader migration

Status: **PLANNED**

Horizontal Reactionで構造が機能した後、他のTrading研究を移す。

候補:

- other GOLD research
- USDJPY
- cross-market
- macro / fundamental
- JP225

既存Drive資料は一括コピーせず、canonical / supporting / superseded / historical / duplicateを判定して移行する。

---

## Phase 8 — Research Mesh / long-running AI workflows

Status: **PLANNED**

構造が安定してから、大量作業をAIへ委譲する。

長時間モデル向き:
- repository調査
- 論文・資料の定型抽出
- 既存研究資料の分類
- provenance確認
- index更新候補作成

Research Mesh向き:
- 複数研究の統合
- 矛盾検出
- 証拠強度の批判的評価
- 共通原則の抽出
- 次の検証候補の重複・妥当性確認

AIによる大量作業を導入しても、scientific condition、holdout境界、研究状態を結果後に書き換えない。
