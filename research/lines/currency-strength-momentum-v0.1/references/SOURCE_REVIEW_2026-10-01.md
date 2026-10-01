---
id: REF-CSM-SOURCE-002
type: Diagnostic
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: DOCUMENTATION_REVIEW_ONLY
execution_status: SUCCESS
evidence_validity: PARTIAL
scientific_status: NOT_APPLICABLE
relations: []
---

# Data source qualification — initial assessment

履歴price dataのdownload・ranking・forward returnは未実施。以下はdocumentationで確認した範囲とqualificationすべき事項。UNKNOWNを仕様で推測して埋めない。全sourceの具体seriesのcoverage/API availabilityを検証済みとは主張しない。

## Sourceの役割

| source | 一次性・scope | frequency/history | time semantics | economics | reproducibility/automation | 判定 |
|---|---|---|---|---|---|---|
| ECB EXR | 公式administrator。7 foreign/EUR series+EUR=1の候補 | daily reference。provisional1999開始は実seriesで未確認。推奨2009-11〜2026-09も未qualification | 公表は通常16:00 CET付近、設定は14:10 CET付近。date fieldは両者のexact timestampではない。historical regime/DSTは別確認 | transaction用でない。BID/ASK・spread・slippage・carry・financing UNOBSERVED | SDMX API候補、公式download。API docs/series画面503。更新・再公表あり。snapshot/hashが必要 | Discovery候補、NOT_YET_QUALIFIED |
| BIS bilateral USD | 公式集約、source originは各seriesで確認 | exact currencies/frequency/history UNKNOWN in this review | 個別method/availability UNKNOWN | executable quote・BID/ASK・carry UNOBSERVED | portal/API/version/legalの確認が必要 | source triangulation候補。v0.1 substitute不可 |
| BIS EER | 公式だがtrade-weighted derived index | daily nominal、monthly nominal/real。broad/narrowでhistory差 | dailyもmid-week更新、monthlyは月中更新。monthly exchange inputはbusiness-day average | bilateral pairでもtradable assetでもない。BID/ASK/carryなし | trade weights/revisions/index baseのpinが必要 | raw major rankingの代用不可。factor/context用途のみ |
| Fed H.10 / FRED | Fedのbilateral reference、FREDは配信・集約。source provenanceはseries単位 | daily observations、history/quote conventionはseriesで違う。DEXUSEU候補確認 | Fedは前週dailyをMonday16:15公表、holidayは次business day。daily observation date≠daily availability | reference、BID/ASK/spread/carry/financing UNOBSERVED | Fed DDP retirement準備の告知あり。FRED routeのunit・revision/vintage、API key/termsを確認 | independence check候補、same-day signal用には不適切 |
| Dukascopy | broker/venueの一次feed、global market全体でない | history bars/ticksの公式案内。28 crossesのhistoryはUNKNOWN | timestamp timezone、bar-open/end、週末、volumeの意味は具体routeで未確認 | BID/ASK取得routeの候補。spreadは同期quoteから。slippage、commission、actual financingは別 | JForex/history routeと公開feedは区別。再配布license・欠損/revision・API安定性は未qualification | 後続economic screen候補。tick全履歴構築は不要 |
| OANDA v20 | broker一次API、account-specific tradability | official APIはhistorical pricingを案内。pair/history具体coverageは未確認 | candle time、complete flag、alignment/timezone、price component B/A/Mを固定する必要 | BID/ASK candles候補。historical quotes≠fill。実際commission/financing/slippageは別 | auth/account必要。今回接続禁止。public docsのみ | 後続source候補、今回取得不可 |
| author factor series | 著者由来の加工研究series | Zhang pageはDecember2020更新Excelを案内 | formation/availability/estimation sampleはfull text未確認 | carry/dollar/factor momentum用。execution fundingでない | mutable link、replication license/underlying vendor terms不明 | 後続factor design候補。v0.1から除外 |

全sourceに共通して、missingがholiday・no quote・retrieval failure・cessationのどれかを分ける。価格のforward fill、interpolation、provider混合は禁止。future macro controlsはrelease timestamp、vintage、revisionとas-of joinを別specで扱い、latest macroをhistoryへ渡さない。

## 確認した公式source

- [ECB reference-rate page](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)。current webpageにrate levelsが付随して表示されたがranking/return/candidate選択には使用していない。
- [ECB framework, 23 June2026](https://www.ecb.europa.eu/stats/pdf/exchange/Frameworkfortheeuroforeignexchangereferencerates.en.pdf)。referenceはtransaction向けでなく、再公表の可能性もある。quoted sourceを使う場合はmid、他の場合trade/order等も使うので、全historyを一律bid/ask平均と断定しない。
- [ECB copyright](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html)。source attributionと変換明示が必要。working-paper再出版の別扱いをrate dataへ混同しない。
- [ECB API overview](https://data.ecb.europa.eu/help/api/overview) / data help / USD EXR series画面は503。source readiness PASSの根拠にできない。
- [BIS EER metadata](https://data.bis.org/topics/EER)。[legal](https://data.bis.org/help/legal) の詳細はCの確認対象。
- [Fed H.10](https://www.federalreserve.gov/releases/h10/)、[FRED DEXUSEU](https://fred.stlouisfed.org/series/DEXUSEU)。全7 seriesやnoon定義は未確認。
- [Dukascopy historical data](https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/)。root docsのみ。route-specific clock/legal/coverageは未確認。
- [OANDA pricing](https://developer.oanda.com/rest-live-v20/pricing-ep/)、[instrument candle definition](https://developer.oanda.com/rest-live-v20/instrument-df/)。public docsのみ、auth requestなし。

## Minimal source route（候補、未実行）

ECB API base候補 `https://data-api.ecb.europa.eu/service/data/EXR/`。
7 seriesは `D.{AUD,CAD,CHF,GBP,JPY,NZD,USD}.EUR.SP00.A`。7個の別requestを候補とし、startPeriod=2009-11-01、endPeriod=2026-09-30、CSV responseのaccept/formatを公式docsでCが確認する。combined queryの順序・formatを推測しない。

Cは公式schema/metadataと7 queryのidentityを確定し、dates/status/currency/unitのみを出力するrouteを準備できる。bodyは必ずsource snapshotとして保存するがOBS_VALUEをhuman/modelのoutputへ展開しない。全historyの取得はgate PASS後のXが行う。API unavailableならofficial historical XML/CSVが同一EXRである証拠を示してIntegratorへ提案する。別providerを勝手に代用しない。

cacheでrequest結果を補う場合、source URL・retrieval time・HTTP headers/status・exact bytes/hash・format・series keys・revision/publication情報を記録。retrospective latest-vintage sourceであることを明示。hash一致はhistorical as-published証明ではない。

## Cのpre-outcome structural qualification権限

metadata-only/値を遮断したbounded probeは許可。返答が全CSVを含むconnectorなら避け、scratch scriptでdates/statusのみを取り出す。actual ratesを含むresponseをtool出力へ出さない。sample日は推奨期間の先頭2009-11の固定範囲を用い、変動の大小から日を選ばない。probeで見たdate/statusもaccess receiptに残す。最終raw dataset hashはXがcapture後に記録し、**capture後・return計算前にsource/code再照合gate**を通す。

DとEにはactual-market price bytesを渡さない。Xもraw CSVのhead/tail、plot、current strengthをhuman/modelに出さず、deterministic loaderが直接読む。これによりmetadata qualificationの段階でoutcomeを偶発的に開くことを避ける。repo全体が強いACLで隔離される保証はないため、process権限とaccess ledgerの保証範囲も記録する。

## Timeの扱い

DATEはcalendar label、TIMEはinstant、AVAILABLE_ATは公表/配信時刻として別fieldにする。現行docsのCET表記をEurope/Berlinの全history/DSTに自動置換しない。参考値associationではDATEによる同期windowだけを検査し、historical AVAILABLE_ATはUNKNOWNのまま保持できる。それをcausal tradeのtemporal PASSと呼ばない。

reference screenをhumanが確定する場合、gateのtemporal判定は `REFERENCE_ASSOCIATION_ONLY`。publication lag/revisionを含むcausal strategyにはgateを移植できない。もし人間が公表後entry testを選ぶなら新しい仕様を**結果前に**作り、D/Eを新仕様で再検証し、二つを同sampleで比較して選ばない。
