# Prior Repository Review — Trading Second Brain

## Metadata

- Repository: `kain26/trading-second-brain`
- URL: https://github.com/kain26/trading-second-brain
- Review date: 2026-09-26
- Reviewed default branch: `main`
- Reviewed head observed: `dc5244a8dd715e30c58451f703d05ec774220bda`
- Repository created: 2026-08-22
- Review status: **PARTIAL**
- Reason for PARTIAL: README、主要運用ファイル、root構造、主要commit差分、Issue一覧は確認したが、長期運用の履歴がほぼ存在せず、実運用での設計劣化・修正履歴を評価できない。

## 1. What problem is this repository solving?

### Fact

READMEでは、TradingView screenshot、broker CSV、PDF、ノート等に分散した個人のTrading情報を、AI agentが検索・比較・更新できる構造化memory layerへ変換することを目的としている。

中心メッセージは「情報を多く保存すること」ではなく、「過去情報を必要な場面で再利用できること」。

### Interpretation

これはquant research repositoryというより、**AI-managed personal trading knowledge system** に近い。

systematic-trading-researchにとって特に参考になるのは、strategy performanceそのものより、

- raw source
- revisable learning
- explicit decision
- durable memory

を分離するknowledge-promotion設計である。

## 2. Canonical source of truth

### Fact

repository root内のファイル群をAI agentが直接読み書きする設計。

主要な役割は明確に分離されている。

- `MEMORY.md`: durable trader context / stable rules
- `LEARNINGS.md`: repeated evidenceに基づくrevisable lessons
- `decisions.md`: rule/process変更のdated audit trail
- `knowledge/`: topic-specific knowledge
- `strategies/`: executable playbooks
- `journal/`: daily context / reflection
- `trades/`: structured trade records
- `research/`: original external research
- `inbox/`: unprocessed source material

AI summaryでoriginal researchやscreenshotsを上書きしないことも明示されている。

### Interpretation

「current knowledgeを一つの巨大文書に圧縮する」のではなく、**異なる耐久性の知識を別レイヤーへ置く**ことが中心設計。

## 3. Current repository structure

主要構造:

```text
AGENT_WORKFLOW.md
CLAUDE.md
MEMORY.md
LEARNINGS.md
decisions.md
knowledge/
strategies/
journal/
trades/
screenshots/
research/
inbox/
templates/
prompts/
```

この構造は「research experiment lifecycle」よりも「personal trading knowledge lifecycle」に最適化されている。

## 4. Knowledge / data model

### Explicit model

knowledge promotion:

```text
raw source
→ journal / knowledge
→ repeated evidence
→ LEARNINGS.md
→ explicit decision
→ decisions.md
→ durable context / hard rule
→ MEMORY.md
```

`decisions.md` は append-style audit trailとして設計され、status候補は `ACTIVE / TESTING / RETIRED`。

### Strength

一回の印象や感情的なtradeを、すぐdurable ruleへ昇格させない。

### Limitation

hypothesis、experiment、dataset、result、interpretation、decisionを独立entityとして厳密に表すschemaは確認できない。

systematic research用には追加設計が必要。

## 5. Research lifecycle

明示されているlifecycleは主として、

```text
source capture
→ AI extraction
→ existing knowledge cross-check
→ journal / knowledge update
→ repeated pattern
→ learning
→ decision
→ memory
```

である。

これは経験的なTrading knowledgeの育成には適するが、confirmatory experimentの事前登録、holdout管理、dataset identity、experiment IDなどは中心ではない。

## 6. Experiment reproducibility

### Observed

repositoryにはtrades、research、screenshots等を保存する場所があり、source referencesを近くに置くことを要求している。

### Not established

今回確認した範囲では、以下の標準は確認できなかった。

- dataset hash
- code commit binding
- experiment config schema
- seed
- immutable run manifest
- formal preregistration
- holdout lifecycle

したがって、systematic-trading-researchの再現性設計をこのrepoだけから借りるべきではない。

## 7. Negative / failed research

### Fact

Agent rulesは以下を要求している。

- contradictory evidenceを保存する
- one observationをgeneral ruleへ昇格させない
- uncertaintyを明示する
- unresolved questionsを捏造せず残す

`LEARNINGS.md`にはopen hypothesesの区画がある。

### Limitation

failed experiment / null result / rejected hypothesisを独立したfirst-class research objectとして管理する構造は確認できない。

## 8. Current knowledge vs history

これは本repoの強い点。

- current durable context: `MEMORY.md`
- revisable knowledge: `LEARNINGS.md`
- historical rule-change audit: `decisions.md`
- raw / daily history: `journal/`, `trades/`, original sources

という層別化がある。

systematic-trading-researchでも、**current stateとresearch historyを同じ文書に混ぜない**設計は有力。

## 9. AI / agent role

### Fact

AI agentはrepository root内で、

- inbox processing
- multimodal extraction
- classification
- existing knowledge search
- topic update/create
- source archival
- linking
- repeated-pattern detection
- daily review

を行うことを想定する。

permission boundaryとしてrepository rootだけへのread/writeを推奨している。

AIは、

- missing dataをinventしない
- hard risk ruleをsilentに変更しない
- one tradeからgeneral ruleを作らない
- original evidenceを消さない

ことを要求される。

### Interpretation

**AIに整理作業を大きく任せつつ、rule promotionには段階と人間判断を残す**設計。

これは将来のLuna Max / Research Mesh運用と相性がよい。

## 10. Deterministic execution boundary

本repoはautomatic tradingを目的としないことを明示している。

一方で、定量計算をdeterministic engineへ委譲する明示的architectureは今回確認できなかった。

この境界は別repositoryから学ぶ必要がある。

## 11. Human-facing interface

主要interfaceはGitHub Markdownとfolder structure。

Web dashboard / dedicated search UIは確認できない。

README自体は利用者向けにかなり分かりやすいが、large-scale research graphのnavigationを検証できる段階ではない。

## 12. AI-facing retrieval

現状はfile-system agent前提。

README roadmapにはlocal semantic search / embeddingsが将来項目としてあるが、現在実装済みとは確認できない。

MCP-based targeted retrievalは確認できない。

## 13. Issues / discussions findings

GitHub Issues APIで今回取得したall-state Issuesは **0件**。

したがって、Issue discussionから長期的なpain pointや設計判断を抽出することはできなかった。

## 14. Commit-history findings

主要commitを差分まで確認した。

### Sequence observed on 2026-08-22

1. `Add agent map and ingestion rules`
   - fact / observation / hypothesis / rule / decisionの区別
   - source preservation
   - knowledge promotion hierarchy

2. `Add trader memory template`
   - durable memoryを小さく保つ設計

3. `Add learning ledger`
   - repeated evidenceとopen hypothesesの中間層

4. `Add decision audit log`
   - rule changeをappend-styleで残す

5. `Protect private trading data`
   - private data boundaryを追加

6. `Add vendor-neutral AI-managed organization workflow`
   - Claude固有の入口から、複数agentを想定した `AGENT_WORKFLOW.md` へ拡張
   - humanが手動分類せず、inboxへ投入する方式を強化
   - repository rootをpermission boundaryとして明示

### Interpretation

現在構造は長い試行錯誤の末に収束したものではなく、短時間で構築された初期architectureに近い。

そのため、commit履歴から得られる有力な知見は「どの順番で関心事項を追加したか」であり、「長期運用で残った設計」ではない。

## 15. Failure cases / abandoned approaches

明示的な失敗experimentや大規模redesignは今回確認できなかった。

ただし `vendor-neutral AI-managed organization workflow` commitでは、

- humanによる手動分類中心
- agent-specific entrypointだけに依存

する方向から、

- inbox中心
- AI-managed organization
- vendor-neutral workflow

へ拡張している。

これは完全な「失敗の撤回」とまでは言えないが、運用負担をhumanからagentへ寄せる設計変更として参考になる。

## 16. Strengths

### A. Knowledge promotion hierarchy

一回のobservationをdurable ruleへ直接昇格させない。

### B. History preservation

`decisions.md` で過去ruleを上書きせず理由と証拠を残す。

### C. Original-source preservation

AI summaryより原資料を優先して残す。

### D. Fact before interpretation

multimodal inputでも抽出と解釈を分ける。

### E. Narrow agent permission

repository rootだけへの権限を推奨。

### F. Low human filing burden

humanはinboxへ投入し、分類はagentが行う思想。

## 17. Limitations

- repository lifespanが短い
- Issuesがない
- real-world operational evidenceが少ない
- systematic experiment schemaが弱い
- formal provenance / hash / run manifestがない
- holdout / preregistrationを中心としない
- MCP / structured query interfaceは未実装
- current vs historyは強いが、hypothesis → experiment → result chainは弱い

## 18. Transferable lessons

### STRONG_COMMON_PRINCIPLE candidate

**知識を耐久性で分ける**

raw observation、revisable learning、explicit decision、durable ruleを同じレイヤーに置かない。

ただし「STRONG_COMMON」と確定するには他repositoryとの比較が必要。

### PLAUSIBLE_PATTERN

**one independently maintainable knowledge unit = one file**

粒度設計として有力。ただしsystematic experimentではentity relationが増えるため、そのまま適用できるか未確認。

### PLAUSIBLE_PATTERN

**inbox + agent classification**

大量の非構造資料を取り込む場合には有効そう。ただしcanonical research artifactをAIが直接更新する場合の誤分類リスクは別途検証が必要。

### PLAUSIBLE_PATTERN

**repository-root permission boundary**

agent権限を研究workspaceに限定する考え方は再利用価値が高い。

### PROJECT_SPECIFIC

`MEMORY.md` にtrader psychologyやhard risk ruleを置く方式。

個人裁量Tradingには合うが、systematic researchのcanonical scientific stateとは分離した方がよい。

### DO_NOT_COPY

このrepositoryだけを根拠に、experiment schemaやprovenance schemaを設計すること。

再現性研究の要求が異なるため不十分。

## 19. Questions for cross-repository synthesis

次のrepositoryで確認する。

1. negative/null experimentをfirst-class objectにしているか
2. dataset / config / code / resultをimmutableに結んでいるか
3. current knowledgeとexperiment historyをどのように接続するか
4. AI agentにcanonical research stateを書かせる場合のguardrailは何か
5. human-readable Markdownとmachine-readable metadataをどう併用するか
6. long-term運用でfolder hierarchyは増えすぎないか
7. semantic search / MCP導入前にどのindexを持つべきか

## 20. Sources reviewed

- Repository metadata / root tree
- `README.md`
- `AGENT_WORKFLOW.md`
- `CLAUDE.md`
- `MEMORY.md`
- `LEARNINGS.md`
- `decisions.md`
- `templates/`
- `prompts/`
- all-state GitHub Issues list
- commit list
- major commit diffs:
  - `3b0b64c` Add agent map and ingestion rules
  - `89be0155` Add trader memory template
  - `497b7e3a` Add learning ledger
  - `e3f012bf` Add decision audit log
  - `d9dbeb96` Protect private trading data
  - `94288c12` Add vendor-neutral AI-managed organization workflow

## Review status

**PARTIAL**

Repository自体が新しく、長期運用でのIssue・redesign・failure historyが不足しているため。現在architectureの研究には有用だが、耐久性の証拠としては他repositoryとの比較が必須。
