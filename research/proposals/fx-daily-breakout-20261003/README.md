# USD/JPY Daily Breakout — small-capital research proposal

作成日: 2026-10-03 JST
Status: DRAFT / NO_MARKET_OUTCOME_ACCESS

## Purpose

XM Micro MT5 と松井証券FXを少額で利用する可能性を念頭に、USD/JPYの日足ブレイクアウト候補を、実市場の結果を見る前に検証可能な研究仕様へ近づける。

これはライブ注文指示、凍結Specification、収益性の主張ではない。ブローカー接続・注文送信・自動売買は行わない。

## Provenance

- 元草案: research/proposals/multi-asset-trend-20261002/FX_DAILY_BREAKOUT_DRAFT_2026-10-03.md
- 元草案の確認済みcommit: 6c90f2b8f6238cb5a824f4a32ed2742c2ca75262
- 分離理由: ETFの月次12か月トレンド案と、USD/JPYの日足20日ブレイクアウトは、market・horizon・signal・execution・data contractが異なるため。
- 本Proposalでは既存HR/CSMの市場入力・結果を参照せず、現在の研究原則に従って状態を分離する。

## Human decision recorded

2026-10-03 JST に、exit architectureとして **WEEKEND_FLAT** が人間により選択された。

- Friday new entries: disabled.
- Existing position: if still open, forced-close request at Friday 23:00 JST.
- Opposite signal may close earlier at the normal 20:00 JST review.
- The former 10-weekday-check time exit is removed.

Decision record: HUMAN_DECISION_RECEIPT_2026-10-03_WEEKEND_FLAT.md.
Historical alternatives remain in HUMAN_DECISION_PACKET_2026-10-03.md and are not deleted.

## Fixed candidate components

- Market: USD/JPY only.
- Direction: long / short symmetric.
- Daily boundary: New York 17:00, America/New_York DST-aware.
- Signal: latest completed daily Bid close strictly exceeds prior 20 completed daily Bid highs for long, or strictly falls below prior 20 lows for short. Current day is excluded.
- Equality: no signal.
- Human review time: 20:00 JST.
- Candidate entry window: first available executable Bid/Ask from 20:00 through 20:05 JST; otherwise SKIP.
- Initial stop: 2 x Wilder ATR(14) from executable entry price; never widened to fit position size.
- No fixed take-profit and no trailing stop in the current candidate.
- WEEKEND_FLAT exit architecture.
- No martingale, averaging down, hedged rescue, or discretionary rule changes.
- Quantity must be rounded down to broker limits; if minimum size breaches risk constraints, SKIP.

## Entry delay is part of the strategy

New York 17:00 daily close occurs at approximately 06:00 JST during U.S. daylight saving time and 07:00 JST otherwise. A 20:00 JST review therefore intentionally introduces roughly 13–14 hours of signal-to-execution delay. This must be represented in historical replay rather than silently approximated as next-bar-open or daily-close execution.

## Current specification

Current working version: SPEC_DRAFT_v0.2.md.

The exit architecture is now fixed, but the overall specification is not frozen. Do not run market-outcome backtests yet.

Before outcome access, still resolve:

- exact reference feed and execution-price source;
- historical period and warm-up;
- Friday 23:00 executable-quote/no-quote rule;
- comparator and risk-comparison method;
- fee/swap/slippage treatment;
- primary metric and numeric decision/stop thresholds;
- remaining synthetic tests for ATR, stop path, missing data and exit precedence.

Passing synthetic tests is evidence of deterministic implementation consistency only, not market edge.