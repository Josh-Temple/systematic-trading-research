# Prior Repository Research

Updated: 2026-09-26

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

## Initial research queue

| Repository | Primary question | Status |
|---|---|---|
| Trading Second Brain | 個人のTrading knowledgeをどう昇格・保持するか | TODO |
| zestoles/quant | 失敗研究、事前登録、provenanceをどう残すか | TODO |
| Epsilon Quant Research | 大規模な研究群をどう整理・探索するか | TODO |
| Backtrader MCP | AIと再現可能なbacktest executionをどう分離するか | TODO |
| mcp-strategy-research-db | 過去のstrategy resultをAIからどう検索するか | TODO |
| Trade Terminal | agentによる研究loopとguardrailをどう設計するか | TODO |

## Synthesis questions

個別レビュー後、次を横断的に検討する。

- 複数repositoryで共通して残っている設計は何か
- 途中で撤回・簡素化された設計は何か
- research artifactの最小単位は何か
- current stateとhistoryをどう分けているか
- negative/null resultをどう発見可能にしているか
- provenanceをどこまで機械可読にしているか
- schemaを厳格にしすぎると何が壊れるか
- AIへ公開する知識と決定論的engineへ残す処理の境界はどこか
- Web UI / search / MCPはどの段階で導入されたか
- 自分たちの研究規模で不要な複雑性は何か

## Exit condition

複数の異なる先行例から、

- strong common principles
- plausible but unverified patterns
- conflicting design choices
- project-specific choices

を分けて記録できた時点で、Knowledge Base v0.1のschema設計へ進む。
