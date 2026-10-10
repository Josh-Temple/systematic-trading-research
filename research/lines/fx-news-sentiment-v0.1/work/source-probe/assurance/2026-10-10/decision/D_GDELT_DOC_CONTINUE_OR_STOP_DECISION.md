# D — GDELT DOC固定契約の継続・停止判断資料

- 作成：2026-10-09 JST（2026-10-10 Waveの作業。**承認日・取得日ではない**）
- 担当：D（意思決定の準備のみ）
- 対象：FX News Sentiment v0.1／候補仕様 `SPEC-FXNS-001-v01`
- 出発点：FXNS研究branch `b1b31e5f1344c86c816f934a695a8583eb1bf4eb`、[PR #63](https://github.com/Josh-Temple/systematic-trading-research/pull/63)、[先行C #81](https://github.com/Josh-Temple/systematic-trading-research/pull/81)、[独立B #75](https://github.com/Josh-Temple/systematic-trading-research/pull/75)、[統合E #85](https://github.com/Josh-Temple/systematic-trading-research/pull/85)
- **現在の結論：`SOURCE_QUALIFICATION_BLOCKED / HOLD`。現行DOC `artlist`契約だけでは正式cohortへの採用を証明できない。** `UNTESTED / PROPOSED_NOT_FROZEN / formal CLOSED`、XM取得延期、market outcome禁止は維持。今回の資料は変更・追加取得・採用承認を行わない。

## 1. 5条件の判定：文書上の説明と正式利用の証明を分ける

| 必要な保証 | 既存証拠で言えること | 現在の判定・不足 |
| --- | --- | --- |
| (a) 08:00 JST前の**対象pipelineの取得完了receipt** | 保存済みHTTP 200は2026-10-07 **12:20:26 JST**に完了。実受領時刻は記録済み | **BLOCKED**。08:00前のreceiptは存在せず、遅延取得を事後的に有効化できない |
| (b) raw DOC `seendate`の意味と、独立した**初回観測時刻** | 12行で書式・値を観測。DOCの公式パラメータ説明は、`seendate`の不変なfirst-seenやpipeline到達時刻を保証していない | **UNVERIFIED**。公表時刻、GDELT観測時刻、実受領時刻を同一視できない |
| (c) indexの**その時点での網羅性**、250件上限、429 | DOCの最大250件は文書化。保存済み200はraw **12件→重複処理後10件**。比較要求（上限10）はHTTP **429** | **BLOCKED**。250件未満も429も全件取得の証明にはならない |
| (d) UTCと24時間windowの厳密な端点 | manifestはUTC指定、raw `seendate`には`Z`、既存コードは開区間の保守的判定 | **UNVERIFIED**。DOCサーバの対象field・タイムゾーン・端点等号判定は未立証 |
| (e) indexの改訂、遅延収録、後追い更新 | 保存済み単一時点の200/429とDOC説明に、as-of snapshot／改訂履歴の正式保証はない | **UNVERIFIED**。実際に改訂が起きたとの主張もしない |

保存された負の証拠：`runtime-20261007-exact/manifest.json`（blob `d9ecb57f880a407bcfb55faf5e8bfd9018c5de09`、HTTP200、raw 5962 bytes、SHA256 `17904b568f8bffc0d9f0c3048444b62c51a03e5200fc6ec4d50778fdabc2ed7d`、元の`domain/URL mismatch`を保持）、`runtime-20261007-cap10/manifest.json`（blob `fe99b74c6e4eeccb5000a6845a901d7b92c38086`、HTTP429、raw 444 bytes、SHA256 `44c03f8dd984184218c90dc7e64aed9e6e2d8b17426feb5aa7933b3c44df64c6`）。raw blobはそれぞれ `ff5159d91bc2ead99bbd0a669e8c8079f585d9a1`、`faca354e1d0c6bf1e7fe7a7990b6015df6023b55`。別のoffline replayの12→10は旧raw/manifestのエラーを遡及修正しない。前回B #75ではrawの独立SHA照合2/2一致を報告済み。**今回Dはhashを独立再計算していない。**

固定候補：`(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`、24時間、`mode=artlist`、`sort=dateasc`、`MAXRECORDS=250`、08:00 JST cutoff。既存の[Source Contract](../../../../../SOURCE_CONTRACT.md)と[PR #81判定](https://github.com/Josh-Temple/systematic-trading-research/pull/81)に従い、変更しない。GALの `date` 説明をDOCの `seendate` に流用しない。追加HTTP 200一件、または時間内の取得receipt一件だけでは(b)(c)(d)(e)を閉じない。

## 2. 人間に求める**一件の判断**（未決・未承認）

**問い：固定DOC契約のまま、(b) first-seenの権威ある定義・(c) point-in-time網羅性・(d) UTC/端点・(e) 改訂保証を満たす公式資料または独立承認可能な検証手段を入手できる見込みがあるか。**

- **見込みあり**と担当者が別途判断する場合：具体的な保証の提供者、検証範囲、費用・許諾、承認責任者と停止条件を先に示し、**別承認**のうえでのみ将来の前向き取得計画を審査する。現段階は`BLOCKED`のまま。
- **見込みなし／保証できない**場合：固定DOCによる正式cohortを**停止**するか、明示的な**pre-freeze再設計**の審議へ送るかを人間が決める。Dはどちらも選択・承認しない。仕様やproviderを勝手に変更しない。

判断の前に曖昧にすべきでない点：08:00直前までのwindowと「08:00前に取得完了」の同時要件には運用上の厳しい時刻境界がある。時刻改変、後日の取得、件数が上限未満であることを適格化の代用にしない。

## 3. 将来**明示承認後のみ**作成するprospective evidence bundle

同一の事前登録query／`artlist`／24時間／`dateasc`／250件／08:00 cutoffを固定。対象runnerと時刻源・許容時計誤差を記録し、開始・完了のUTC/JST時刻、HTTP status・headers・raw response bytes・SHA256・保存先識別子を受領時点で確定する。改変検知可能な保存、再起動後のreadback、429・不完全応答のfail-closed、同一windowの再取得とrevision扱い、`seendate`の定義、UTC/等号境界、as-of index coverageの根拠と対象範囲を記録する。**独立検証者**が何を照合したか（raw/hash/時計/first-seen/coverage/改訂）、誰が判断したかを切り分ける。受領前の資格確認と事後の独立レビューの両方が必要。ここに挙げたものは**提案であり、今回は実行していない**。

**停止条件：** first-seen/coverage/端点/改訂の保証不足、遅延receipt、HTTP429、未保存raw、ハッシュ不一致、別providerへの無断変更、正式issue/outcome連結要求。どれか一つでも該当すれば`SOURCE_QUALIFICATION_BLOCKED`、formal cohort `CLOSED`を維持。

## 4. 実行区分と変更境界

本Dで**実施**：GitHub上の#63/#81/#75/#85、現行`SOURCE_CONTRACT.md`、保存済み200/429 raw・manifest・offline replay・blobをread、従来の公式仕様レビューを区別したうえで判断資料を整理。**今回未実施**：新GDELT DOCアクセス、HTTP追加テスト、独立SHA再計算、ソース変更、XM/市場outcome/ニュース分類、売買、別provider、human承認。docs確認のために新しいlive DOC APIを呼び出していない。

変更許可範囲は `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-10/decision/**` にある**この一文書のみ**。workflow・source/manifest・query・仕様・判定ゲートは不変。Eへの引継ぎ判定は**`HOLD / SOURCE_QUALIFICATION_BLOCKED`**。
