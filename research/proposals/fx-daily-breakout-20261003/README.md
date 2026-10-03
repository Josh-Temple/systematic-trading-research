# USD/JPY Daily Breakout — small-capital research proposal

作成日: 2026-10-03 JST
Status: DRAFT / HUMAN_BOUNDARY / NO_MARKET_OUTCOME_ACCESS

## Purpose

XM Micro MT5 と松井証券FXを少額で利用する可能性を念頭に、USD/JPYの日足ブレイクアウト候補を、実市場の結果を見る前に検証可能な研究仕様へ近づける。

これはライブ注文指示、凍結Specification、収益性の主張ではない。ブローカー接続・注文送信・自動売買は行わない。

## Provenance

- 元草案: research/proposals/multi-asset-trend-20261002/FX_DAILY_BREAKOUT_DRAFT_2026-10-03.md
- 元草案の確認済みcommit: 6c90f2b8f6238cb5a824f4a32ed2742c2ca75262
- 分離理由: ETFの月次12か月トレンド案と、USD/JPYの日足20日ブレイクアウトは、market・horizon・signal・execution・data contractが異なるため。
- 本Proposalでは既存HR/CSMの市場入力・結果を参照せず、現在の研究原則に従って状態を分離する。

## Fixed candidate components

- Market: USD/JPY only.
- Direction: long / short symmetric.
- Daily boundary: New York 17:00, America/New_York DST-aware.
- Signal: latest completed daily Bid close strictly exceeds prior 20 completed daily Bid highs for long, or strictly falls below prior 20 lows for short. Current day is excluded.
- Equality: no signal.
- Human review time: 20:00 JST.
- Candidate execution window: first available executable Bid/Ask from 20:00 through 20:05 JST; otherwise SKIP.
- Initial stop: 2 x Wilder ATR(14) from executable entry price; never widened to fit position size.
- No fixed take-profit and no trailing stop in the current candidate.
- No martingale, averaging down, hedged rescue, or discretionary rule changes.
- Quantity must be rounded down to broker limits; if minimum size breaches risk constraints, SKIP.

## Unresolved scientific condition

The current draft contains two incompatible exit designs:

1. WEEKEND_FLAT: no new Friday entry and close any open position Friday 23:00 JST.
2. TEN_CHECK_HOLD: no forced Friday exit; close on opposite signal or at the 10th weekday 20:00 check after entry.

These are not the same strategy. The project has NO_SAFE_DEFAULT. A human must select one before market outcomes are accessed. They must not be compared on the same historical sample and then the better one promoted as if preregistered.

See HUMAN_DECISION_PACKET_2026-10-03.md.

## Entry delay is part of the strategy

New York 17:00 daily close occurs at approximately 06:00 JST during U.S. daylight saving time and 07:00 JST otherwise. A 20:00 JST review therefore intentionally introduces roughly 13–14 hours of signal-to-execution delay. This must be represented in historical replay rather than silently approximated as next-bar-open or daily-close execution.

## Current gate

Do not run market-outcome backtests yet. Before outcome access, resolve the exit design, exact reference feed, execution-price source, history period, benchmark/risk comparison, fee/swap/slippage treatment, primary metric, and numeric decision/stop thresholds.

Next concrete artifact: DATA_CONTRACT.md plus SPEC_DRAFT_v0.1.md.