# Roadmap

Updated: 2026-09-27

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

Status: **COMPLETE**

### Purpose

完成形だけを模倣せず、先人がどの問題に直面し、何を変更・廃止・維持したかを理解する。

### Completed evidence

Deep reviews:

- Trading Second Brain
- zestoles/quant
- Epsilon Quant Research
- DVC
- RD-Agent
- Freqtrade

Breadth scan:

- 21 prior-art candidates screened
- HIGH candidates included RD-Agent, DVC, Freqtrade, Qlib, Kedro, NautilusTrader, hftbacktest

Current synthesis:

- `research/prior-art/SYNTHESIS_V0.2.md`
- status: `PHASE_1_FINAL_V0.2`

### Strong principles currently supported

- current valid knowledgeとhistorical researchを分ける
- negative / rejected / invalidated / failed researchを残す
- observation / hypothesis / experiment / result / interpretation / decisionを混同しない
- provenance artifactの存在とcausal provenanceの正しさを分ける
- knowledge correctness / evidence correctness / computation correctnessを別々に検査する
- final holdoutをadaptive research loopの外へ置く
- AIの権限制御には、write権限だけでなくdata visibilityとscientific decision rightsを含める
- retrieval / navigation / generated indexをcanonical evidenceにしない

これらはPhase 2の設計制約候補であり、最終schemaではない。

### Phase 1 exit

Result: **PASS**

See:

- `research/prior-art/PHASE1_EXIT_REVIEW.md`
- `research/prior-art/SYNTHESIS_V0.2.md`

Qlib / Kedro / NautilusTrader / hftbacktest remain deferred references, not blockers.

### Exit condition

以下を区別でき、Horizontal Reaction pilotへ適用可能な最小設計制約が揃うこと。

- strong common principles
- plausible but unverified patterns
- conflicting design choices
- project-specific choices

---

## Phase 2 — Knowledge Base v0.1

Status: **COMPLETE**

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

重要: 最終schemaはPhase 1で得た証拠から決定し、事前候補をそのまま採用しない。

### Current design constraints from Phase 1 — provisional

v0.1は少なくとも以下を表現できる必要がある可能性が高い。

- hypothesis
- frozen strategy / experiment specification
- dataset identity and role
- run identity
- result
- interpretation
- decision
- current status
- invalidation / correction relation
- rejected / failed / insufficient-evidence states

data role候補:

- development / training
- adaptive validation
- final holdout
- consumed holdout / historical sample

resultは少なくとも、

- execution status
- evidence validity
- scientific status

を別々に扱う方向を検証する。

### Deliverables completed

- `docs/KNOWLEDGE_BASE_V0.1.md`
- `schema/v0.1/README.md`
- entity / run / diagnostic / current projection templates
- `schema/v0.1/PILOT_CHECKLIST.md`

Result: **PASS — DRAFT_FOR_PILOT**

### Exit condition

1本の研究lineageを無理なく表現でき、人間が理解しやすく、AIがcurrent/historical stateを取り違えず、provenanceの保証範囲を明示できる最小構造が定義されていること。

Full schema validation is intentionally deferred to the Horizontal Reaction migration in Phase 3.

---

## Phase 3 — Horizontal Reaction pilot migration

Status: **COMPLETE**

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

### Result

**PASS_WITH_RECORDED_SOURCE_CONFLICT**

See:

- `research/lines/horizontal-reaction-v0.1/PHASE3_EXIT_REVIEW.md`
- `research/lines/horizontal-reaction-v0.1/CURRENT.md`

The unresolved H1 D1-D5 source discrepancy is explicitly preserved rather than silently reconciled.

### Exit condition

Horizontal ReactionをGitHubだけで追跡して、研究状態を誤解なく再構成できること.

---

## Phase 4 — Human-facing web UI

Status: **IN PROGRESS**

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

### v0.1 implementation

Initial implementation:

- `docs/WEB_UI_V0.1.md`
- `web/index.html`
- `web/styles.css`
- `web/app.js`
- `web/data/horizontal-reaction-v0.1.js`
- manual-ready GitHub Pages workflow at `.github/workflows/pages.yml`

The first screen is intentionally scoped to Horizontal Reaction v0.1 and presents:

- current scientific state
- unresolved source conflict
- next admissible test
- forbidden sample reuse
- H1/H2/H3 evidence
- data consumption boundaries
- historical blocked vs scientific results
- canonical links

The web projection is noncanonical. Phase 5 will address generated indexes / automated projection.

### Validation state

Completed:

- static UI implementation
- scientific projection cross-check against canonical H1/H2/H3 records
- all embedded canonical GitHub links verified
- JavaScript syntax checks
- DOM target/reference checks
- mobile overflow correction for long status labels

Recorded in:

- `web/VALIDATION.md`

Deployment status:

- initial first-time Pages creation attempts failed before repository-admin enablement
- Pages was subsequently enabled with GitHub Actions as the publishing source
- first successful public deployment completed in Actions run 36316165611
- the deploy job completed Checkout / Configure Pages / Upload static site / Deploy with success
- public URL: https://josh-temple.github.io/systematic-trading-research/

Remaining:

- Android/mobile visual review on the public URL
- confirm no unexpected horizontal overflow and that evidence/status distinctions remain readable
- record Phase 4 exit review

The successful deployment does not by itself close Phase 4 or establish scientific validity.

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
