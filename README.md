# systematic-trading-research

システムトレードの仮説、データ、仕様、実験、結果、解釈、判断、失敗を、後から検証過程を追跡できる形で蓄積する研究知識基盤です。

## Purpose

このリポジトリの目的は「勝てる手法集」を作ることではありません。

- 研究上の事実・解釈・仮説・判断を分離する
- 仮説から実験結果までの provenance を追跡できるようにする
- negative / null / rejected な結果も研究成果として保存する
- holdout、事前登録、データ同一性などの研究境界を維持する
- 人間がWeb UIから理解・探索できる知識基盤へ育てる
- 将来、AIが検索/MCP等を通じて同じ正本を利用できるようにする

## Current stage

**Phase 0 — Foundation**

まず先行するsystematic trading / quant researchのGitHubリポジトリを研究し、READMEだけでなく、構造、Issue、commit履歴、設計変更、失敗例まで確認します。

複数の先行例から共通する設計原則を抽出した後、最小のKnowledge Base schemaを設計します。最初から大規模な独自設計には進みません。

その後、既存研究のうち **Horizontal Reaction Strategy v0.1** を最初の完全移植対象として、構造が実際に使いやすいかを検証します。

## Research rules

研究上の基本原則は [docs/RESEARCH_PRINCIPLES.md](docs/RESEARCH_PRINCIPLES.md) を参照してください。

全体計画は [docs/ROADMAP.md](docs/ROADMAP.md) を参照してください。

先行リポジトリ研究は [research/prior-art/](research/prior-art/) に保存します。

## Canonical source

このGitHubリポジトリを、今後構造化するsystematic trading research knowledgeの正本とします。

Google Drive上の既存Trading資料は、移行元・一次的な研究記録・source artifactとして参照します。内容を移植する際は、元資料の意味や研究状態を変えず、canonical / supporting / superseded / historical / duplicate を区別します。

## Safety boundary

このリポジトリは研究・知識管理を目的とします。ブローカーへの注文送信、自動売買、ライブ資金の自動ポジションサイズ決定を目的としません。
