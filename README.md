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

**Phase 4 — Human-facing web UI: IN PROGRESS**

Phase 0 Foundation、Phase 1 prior repository research、Phase 2 Knowledge Base v0.1、Phase 3 Horizontal Reaction pilot migration は完了しています。

Horizontal Reaction Strategy v0.1 は現在、H1/H2の消費済み結果と、未使用のH3 holdoutを分離して管理しています。H3は科学的には `WAITING_FOR_MATURITY` のままですが、2026-09-27のoutcome-blindな実行コード監査でGammaの凍結仕様と保存コードの不一致が確認されたため、maturityだけでは実行できません。詳細は [H3 execution identity precheck](research/lines/horizontal-reaction-v0.1/H3_EXECUTION_IDENTITY_PRECHECK_2026-09-27.md) と [CURRENT](research/lines/horizontal-reaction-v0.1/CURRENT.md) を参照してください。

Human-facing Web UIはGitHub Pagesへ初回公開済みです。

- Public Web: https://josh-temple.github.io/systematic-trading-research/
- Current research projection: [research/lines/horizontal-reaction-v0.1/CURRENT.md](research/lines/horizontal-reaction-v0.1/CURRENT.md)
- Repository review follow-up: [docs/REVIEW_FOLLOWUP_2026-09-27.md](docs/REVIEW_FOLLOWUP_2026-09-27.md)

GitHub Pagesの公開成功とAndroid実機での視覚確認は別管理です。Android実機確認とPhase 4 exit reviewは未完了のため、Phase 4は閉じていません。

## Research rules

研究上の基本原則は [docs/RESEARCH_PRINCIPLES.md](docs/RESEARCH_PRINCIPLES.md) を参照してください。

全体計画は [docs/ROADMAP.md](docs/ROADMAP.md) を参照してください。

先行リポジトリ研究は [research/prior-art/](research/prior-art/) に保存します。

## Canonical source

このGitHubリポジトリを、今後構造化するsystematic trading research knowledgeの正本とします。

Google Drive上の既存Trading資料は、移行元・一次的な研究記録・source artifactとして参照します。内容を移植する際は、元資料の意味や研究状態を変えず、canonical / supporting / superseded / historical / duplicate を区別します。

## Safety boundary

このリポジトリは研究・知識管理を目的とします。ブローカーへの注文送信、自動売買、ライブ資金の自動ポジションサイズ決定を目的としません。
