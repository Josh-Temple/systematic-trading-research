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

- Phase 0 — Foundation: **COMPLETE**
- Phase 1 — Prior repository research: **COMPLETE**
- Phase 2 — Knowledge Base v0.1: **COMPLETE**
- Phase 3 — Horizontal Reaction pilot migration: **COMPLETE**
- Phase 4 — Human-facing web UI: **COMPLETE**

Horizontal Reaction Strategy v0.1 は、仮説・仕様・データ・実験・Run・Result・Interpretation・Decision・current projectionまでGitHubへ移植済みです。H1/H2のnegative result、blocked execution、consumed/unused境界、H1 D1-D5 source conflictも分離して保持しています。

Human-facing Web UI はGitHub Pagesへ公開済みで、公開URLに対するモバイル幅のブラウザ検証まで完了しています。

- Public URL: https://josh-temple.github.io/systematic-trading-research/
- Research line and proposal routing: [research/lines/INDEX.md](research/lines/INDEX.md)
- Current research projection: [research/lines/horizontal-reaction-v0.1/CURRENT.md](research/lines/horizontal-reaction-v0.1/CURRENT.md)
- Repository review follow-up: [docs/REVIEW_FOLLOWUP_2026-09-27.md](docs/REVIEW_FOLLOWUP_2026-09-27.md)
- Phase 4 exit review: [web/PHASE4_EXIT_REVIEW.md](web/PHASE4_EXIT_REVIEW.md)

Phase 4のpublic mobile validationは、GitHub Actions上のChromiumを360 / 390 / 412px幅・touch有効で実行し、スクリーンショットも目視確認しています。物理Android端末そのものでは別途確認していないため、その差はexit reviewに限界として残しています。

Separately, research/pilots/autonomous-research-v0.1/ では synthetic data only の evaluator-integrity pilot を進めています。これはHorizontal Reactionのunused holdoutを消費せず、既存研究結果を変更しません。

## Local validation

Node.js 24とPython 3.12を使い、full Git historyを取得したcheckoutで実行します。

```sh
git fetch origin main
npm ci --ignore-scripts
npm run check
python research/lines/jp225-ema-timeofday-v0.1/work/integration/run_synthetic_tests.py
```

`npm run check`は検証器のsynthetic failure testsと、既存のHorizontal Reaction正本・Web表示の整合性を確認します。未コミット・未追跡の正本文書も鮮度検査の対象です。Pages workflowはこの検証に成功したWeb artifactを公開します。

追加のsynthetic suitesとprocess boundary testの実行手順は [docs/VALIDATION.md](docs/VALIDATION.md) を参照してください。検証成功は科学的仮説の支持や、市場データへのアクセス許可を意味しません。

## Research rules

研究上の基本原則は [docs/RESEARCH_PRINCIPLES.md](docs/RESEARCH_PRINCIPLES.md) を参照してください。

全体計画は [docs/ROADMAP.md](docs/ROADMAP.md) を参照してください。

先行リポジトリ研究は [research/prior-art/](research/prior-art/) に保存します。

## Canonical source

このGitHubリポジトリを、今後構造化するsystematic trading research knowledgeの正本とします。

Google Drive上の既存Trading資料は、移行元・一次的な研究記録・source artifactとして参照します。内容を移植する際は、元資料の意味や研究状態を変えず、canonical / supporting / superseded / historical / duplicate を区別します。

## Safety boundary

このリポジトリは研究・知識管理を目的とします。ブローカーへの注文送信、自動売買、ライブ資金の自動ポジションサイズ決定を目的としません。
