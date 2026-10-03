---
id: RL-FXMP-001
type: ResearchLine
created_at: 2026-10-03
status: PRE_OUTCOME_RESEARCH
relations: []
---

# FX monetary-policy alignment v0.1

## Question

価格モメンタムで選ばれた最強通貨－最弱通貨について、直前の相対的な金融政策方向が価格方向と一致している場合、逆方向の場合より翌月spot returnが高いかを検証する。

## Scope

- currencies: AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD
- initial policy source family: BIS central bank policy rates, `BIS,WS_CBPOL,1.0`
- planned relation to price signal: existing currency-strength-momentum lineのprice-selected pairを変更せず、独立に固定したpolicy featureを付加する
- evidence role: EXPLORATORY_DISCOVERY only
- broker/live trading: out of scope

## Boundary

このlineは既存 `RL-CSM-001` の結果を見て作るpost-hoc filterではない。2026-10-03時点でRL-CSM-001はUNTESTEDかつmarket outcome gate CLOSEDであることをfresh readしてから作成した。

本lineの仕様も未凍結であり、market outcome accessを許可しない。
