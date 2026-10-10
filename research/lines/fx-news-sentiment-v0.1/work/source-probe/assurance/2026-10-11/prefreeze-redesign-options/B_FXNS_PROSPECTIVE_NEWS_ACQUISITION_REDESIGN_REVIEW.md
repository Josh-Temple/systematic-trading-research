# B — FXNS v0.1 前向きニュース取得・保全方式の独立再設計調査

- 調査日：2026-10-11 JST（公開資料の確認は2026-10-10 UTCから実施）。
- 担当：B。公開一次資料・研究仕様・実装の静的読取りによる比較設計。実取得・実装・source資格認定ではない。
- 判定：**NO_QUALIFIED_ALTERNATIVE / SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED**。
- 根拠となる人的承認：[PR #107](https://github.com/Josh-Temple/systematic-trading-research/pull/107)「6. 承認追補」。固定DOCによるformal適格化を停止し、pre-freeze再設計を比較する承認である。特定providerの採用、仕様変更、試験、再凍結は未承認。
- 変更はこの報告1ファイルのみ。B allowlist：`research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-11/prefreeze-redesign-options/**`。
- 本文の「条件付き候補」「受入条件」は将来の承認判断用であり、現在のSOURCE_CONTRACT、query、SPEC、コード、workflow、gateを置換しない。

## 1. 結論と新しい比較価値

**科学的に成立する設計の可能性はあるが、今回の証拠だけで採用可能と認定できる方式はない。** 公開資料は、商品や配信機構の存在と一部の時刻・版管理を示す。一方、必要な収録母集団、欠落検知、時点別の完全な履歴、08:00前の受信・確定、保存・AI利用権、独立監査までを一体として立証していない。「不可能と証明した」とも結論しない。

最大の分岐は、何を検証対象のニュース集合とするかである。

1. 世界の「関連するニュース全件」は、未収録の記事まで数えられないため、今回の候補に完全性を認定する根拠がない。
2. 明確な契約範囲のprovider配信全件なら、連番・確定したmanifest・再送・訂正履歴・配信遅延の仕様を条件に、限定された完全性を検証する道がある。
3. 研究者の収集器が締切前に受信・保全した集合なら、その情報集合の再現は設計できる。ただし「取り逃したニュースがない」という保証とは別であり、研究対象を明示的に変更する判断が必要である。

広いニュース仮説を維持したい場合、**版管理・欠落検知・再送を契約できるライセンス付き配信＋独立した受信保全**を追加証拠収集の第一候補とする。これはLSEG等の採用決定ではない。現行RESEARCH_LINEは有料ニュースfeedを使わない計画なので、費用条件そのものの再承認も必要になる。

無料に近い方式を重視するなら、**GEMG/GALの配信を連続捕捉し、自分の受信情報集合を対象にする別設計**が次の候補となる。ただしDOCの全文検索による記事選択と、metadata/titleだけの選択は同等ではない。小さな公式発表集合でよければ、**ECB/BOJの通信・発表feed**も検討できるが、世界のFXニュースという仮説を中央銀行発表の仮説へ狭める。

このどれにも必要な条件が整わなければ、**停止を維持する**。締切、対象集合、欠落、権利のどれかを曖昧にして前進させる案は推奨しない。

#106/#89/#81の固定DOC保証不足に対する追加価値は、別のGDELT配信・公式feed・複数の現行ライセンス商品を比較したこと、提供元観測時刻と自分の受信時刻を分離したこと、正の配信遅延と厳密な08:00 cutoffの両立条件を示したこと、方式別の採用証拠・操作単位・受入判定を具体化したことにある。既存の固定DOC報告の複製ではない。

## 2. fresh readした正本とGit identity

正本：ChatGPT Library `/Systematic Trading Research/Work Instructions/2026-10-11_fxns_approved_option1_prefreeze_redesign_deviation_and_csm_runtime_planning_wave_instructions.md`（canonical file ID `libfile_4fd90cadc5688191b3f993875697a0e6`）。同名の別ディレクトリのコピーを正本として扱わない。Bの机上比較・報告1ファイル・独立Draft・remote readback境界を適用した。

| 読取り対象 | fresh head / tree | 読んだ報告blob・確認内容 |
| --- | --- | --- |
| main | `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3` / `be858570de929678a219660cb8f0b3d26b038516` | 現在のbranch metadata。編集なし |
| FXNS #63 | `24ef9c37e6255126a957f38cfa7470cd150ed594` / `123f6d539c29f188e489bcc1492b632f5c9514d7` | OPEN/Draft。新B branchの起点。研究文書・関連実装をこのexact refで読む |
| #107 | `495fd3e9167d11d2787a4667995ee0a7cbf6c201` / `f534bc7a17b178478386f384cfa3049ecccfa6a0` | `73100d97bf94c82c0b8fb9a18c0e7e2647579997`。承認追補を含む全文 |
| #106 | `d29afe155210234ef137d8928a1564408179a0f7` / `3bfe63e4636fdf7782a198588621ae886529dc2f` | `6781e3ed32d32814c07df0b2acb39e13506612fe`。7保証の不足、2026年説明、旧逸脱申告 |
| #89 | `2082303a098079fb4788bb7d3c81ae259c342123` / `5facd84077de9e693a35cff9c72578860811c065` | `bd7d3ffa0c6abbda8e05b3252c737f0e63ea4fc7`。継続/停止の判断材料 |
| #81 | `47c51a847b13c52bfa4b117d03b87809e619afbb` / `941cfda0887200501f22fa579329f0f064bf5bee` | `0815bb3a509f0f81d4c72a24b215718cf2dbeec4`。固定契約の実現可能性不足 |

#107/#106/#89/#81はいずれもOPEN/Draft、baseはFXNS研究branch、変更は各報告1ファイル。#63の50 changed pathsはパス名だけを確認し、そこにある実raw、offline_validation、XM記録を開いていない。PRの`base_sha`は比較時の履歴を含むため、現在のmain identityにはbranch APIで確認した上記値を使った。tree inventoryにAGENTS.mdは見つからなかった。

以下のパスはすべて `research/lines/fx-news-sentiment-v0.1/` を前置し、#63 exact refで静的に読んだ。

| パス | blob | この調査への意味 |
| --- | --- | --- |
| SOURCE_CONTRACT.md | `36dd9c9977718a8da02ae8f569cad76d4c0acd15` | title/metadata入力、時刻・完全性の適格性は未確認。一般利用説明だけで第三者権利を確定しない |
| RESEARCH_LINE.md | `919767343f6f56164cafaf4919ede95cdc0383fe` | ChatGPT Plusを使い、有料news feedなしの計画。先行するfull-text fine-tuning研究の直接再現ではない |
| specifications/SPEC-FXNS-001-v01.md | `756bb399bacae8ee815ed53372f30164f078982a` | PROPOSED_NOT_FROZEN / UNTESTED、厳密な24h開区間、08:00取得・08:15前の分類/凍結 |
| CURRENT.md | `733c72aba6172d5f93897fc0f147db4897e28c32` | 古いprobe次工程の記述を実行許可とせず、#107の新しい停止方針を優先 |
| work/source-probe/gdelt_schema_probe.py | `d747160126130291963c2ae981fb9b149f98b29e` | count/cutoff/dedup/receiptの実際の意味を確認。関数の実行なし |
| work/implementation/fxns.py | `ee3fcf474077807c8f05211dc64d82d7acc49158` | 検証用フラグは提供元の資格証明ではない |
| work/implementation/event_ledger.py | `3faa396953c7cb951d32d1f3521ea303010e8598` | COHORT_STATE CLOSED。formal発行・outcome関連付けは停止、合成証拠を実source証明にしない |

workflow `.github/workflows/fxns-gdelt-source-probe.yml`（blob `620581df64cf247c293781389bd7386df391f30e`）とdriver `.github/scripts/fxns_offline_unittest.py`（blob `25636eca0b6c282a2f7233064ec9661fc62666c0`）も静的に読んだ。socket拒否付き合成suiteは実source保証ではない。新しいtests、workflow_dispatch、再実行、clone、環境変更はしていない。

### この調査自身の閲覧逸脱を隠さない

開始時のPR検索が想定外に広い結果を返し、対象外PR本文に市場結果の要約が含まれてモデルへ表示された。後に保存済みのPR inventoryを確認する際も、metadataに限定する出力処理を誤り、広いPR本文を再表示した。また、公的な技術検索・AP/Benzinga等の仕様ページの応答に、実headline/URL/記事例が混入した。意図した記事取得ではなくても、禁止情報の閲覧境界を超える経路となった。

これらの値・文章を本報告へ転載せず、分類・計算・収益性判断に用いていない。これは作成者の申告であり、認知的影響がなかったという独立証明ではない。以後の確認は既知ref/path・技術仕様に絞り、応答はmetadata/必要箇所のみを出力した。再発防止には、connector側でbodyを返さないmetadata専用取得と、記事例を事前に除く文書取得が必要である。

#106の旧申告とは別の本Waveの手続逸脱として記録する。過去rawや問題の実例を再取得・削除して影響検証しない。**PROCEDURAL_DEVIATION_RECORDED / 独立影響確認・人間の最終処分は未了**。本報告をclean compliance認定やDの独立監査結果として扱わない。

## 3. 必要な科学的保証を定義する

### 3.1 「全件」の基準と時刻の区別

母集団には、provider/source/channel、言語、記事種別、地理・媒体、対象フィールド、選択式、訂正・再配信・syndicationの扱いが必要である。現在のDOC queryは `(euro OR yen OR "European Central Bank" OR "Bank of Japan") sourcelang:english`、artlist/json/dateasc/maxrecords250。別機構で同じ文字列をtitleに当てても、DOC全文検索と同じ集合を作ったことにはならない。翻訳、抽出失敗、paywall、死んだURL、媒体の収録開始/停止も対象分布を変える。

| 記号 | 意味 | 相互に代用できない理由 |
| --- | --- | --- |
| p | publisherの公表/初稿時刻 | 配信先に届いた時刻でも、その版の内容が当時公表されていた証拠でもない |
| s | providerの観測・登録時刻 | 初回か再観測か、履歴が不変かを定義する必要。自分の受信ではない |
| v | 当該版の生成/公表/訂正時刻 | firstCreatedとversionCreatedは区別。最新版本に古いpが残ることがある |
| e | providerの配信確定時刻/連番 | 完全な連番や確定manifestがあれば配信範囲内の欠落を調べられる |
| r | 自分の受信開始・最終byte到着時刻 | request開始、HTTP Date、filenameはrの証明ではない |
| d | 自分の耐久保存・検証完了時刻 | read完了だけでは、crash後に保存物が残る保証がない |
| w | 独立監査先の受領/時刻証明 | 内容hashの存在証明。上流完全性やpublisher本人性を単独で証明しない |

「最初に観測された記事」と「最初の版」と「最初に自分へ届いた版」を分ける。article ID、version ID、URL、bytes hashも別である。更新が同URLならURL hashだけでは二つの版を識別できない。新URLでの再配信も、初回ニュースか別記事かは凍結した規則で判定する。

現在のprobeは厳密なwindowとraw_count capを調べ、below-capでも完全性をUNVERIFIEDとする。network読取完了後に保存する構造なので、そのreceipt値を耐久保存完了とみなさない。NFKC/casefold titleとURLによるdedupは、provider変更時にも自動で科学的同等になるとは限らない。ここでは修正していない。

### 3.2 UTC/JSTと08:00の実現可能性

08:00 JSTは前日の23:00 UTC。JSTはUTC+09:00として固定し、元のtimezone/offset、parse規則、UTC値、JST表示を保存する。publisherが夏時間地域の場合、現地日付だけを機械的にJSTへ読み替えない。現在の選択区間は前calendar日08:00と当日08:00の**両端を含まない**24hであり、月曜も直近24h。通常便利な半開区間に無断変更しない。秒精度やclock不確実性で端点との前後が判定できなければ、現在のequality排除と同じくfail-closedが必要になる。

cutoffをC、配信と受信・保存の遅延をL=d−sとすると、すべてのs<Cについてd<Cを保証するには、C直前の記事にも間に合う条件が必要である。**正の遅延があり、観測時刻がCへ任意に近づき得るなら、この二つの「全件」条件は一般には同時に保証できない。** 高い稼働率や速い平均速度だけでは解決しない。

将来の選択肢は、(a)締切前に受信・確定した集合を研究対象にする、(b)provider観測窓をC−gまでにし、合意した最大遅延Lmaxと時刻不確実性を覆う余裕gを置く、(c)取得締切/判断時刻を別途変更する、のいずれかである。いずれも仕様・情報集合の人間判断であり、今回採用しない。SLAが平均/percentileなら超過時はBLOCKEDにし、「必ず」を主張しない。

08:00に初めて直前24hを要求する構造では、通信完了を08:00より前にできない。連続受信はその問題を軽減するが、最後の遅延記事を解消しない。08:00後に届いたものを古いs/pだけで組み込むことは、今回の取得期限に適合しない。

08:00〜08:15には集合確定、分類、検証、署名/台帳確定の時間も必要である。実際のニュース量とChatGPT Plusの処理容量は今回計測していない。高速なfeedがあっても、この15分を自動で満たすとは結論しない。負荷時に記事を後から都合よく間引く案は事前仕様変更となる。

### 3.3 合格に必要な保証と失敗時の扱い

| 保証 | 最低限の立証対象 | 立証できない場合 |
| --- | --- | --- |
| 母集団と収録範囲 | source/channel/language/type/選択フィールドを列挙し、上流完全性とローカル捕捉完全性を分離 | 「世界全ニュース」等へ一般化しない。対象変更を承認するまでBLOCKED |
| 初回観測・実受信 | immutableな観測定義、版情報、自分のr/d、clockの誤差範囲 | pやfilenameを代用しない |
| as-of再現 | C以前に受信・確定した許諾済み版だけから入力集合を再構築 | 最新indexや後取得archiveを使って修復しない |
| 遅延/訂正/削除 | 発見、配信、更新、撤回をappend-only記録し当時版を復元 | 後の訂正で過去入力を上書きしない。保持権がなければ採用停止 |
| 時刻・端点 | UTC/JST、元offset、時計同期/不確実性、等号/精度の規則 | 境界不明やclock故障でfail-closed |
| 08:00到達 | 情報集合の定義、必要な余裕、dの上側時刻境界がC未満、分類期限の余力 | request開始や平均latencyをPASSにしない |
| caps/障害/429 | 切断・欠落・queue overflow・pagination・再送・空feedの証跡 | partial responseを成功扱いしない。締切後retryでformal救済しない |
| 権利 | headline/metadata/raw保持、派生分類、ChatGPTへの送信、独立監査、終了後保持の許諾 | public APIや有料keyだけで許諾確定しない |
| 原記録・独立監査 | bytes、hash、署名、独立保管、アクセス分離、復旧後readback | hash一致のみで真正性/完全性を認定しない |

## 4. 一次資料の出典・確認範囲

以下は2026-10-11 JSTに公的な資料として確認した範囲である。日付がない現行ページは「日付表示なし」とし、提供の広告/仕様が現在閲覧できることと、live endpointの稼働、特定契約の権利、数値SLAの充足は区別する。ニュースfeed/API、実データ、archiveファイルは呼び出していない。仕様の例が混入した逸脱は2節の通りである。

**SUPPORTED_BY_SOURCE**＝資料がその限定した事実を直接支持、**PARTIAL**＝関連要素はあるが必要な保証の全体を支持しない、**NOT_ESTABLISHED**＝今回確認した資料では立証できない。正式sourceのPASSではない。未確認は機能不存在という断定ではない。

| ID・一次資料（公開日/版） | 確認できた事実と確認範囲 | 確認できない保証 |
| --- | --- | --- |
| S01 [GDELT DOC 2.0](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)（2017-06-20） | artlistの上限250、時刻/並べ方の説明。publishedを用いる説明を確認 | seendateの不変first-ever観測、as-of index、全件enumeration、厳密端点・締切SLA |
| S02 [GAL導入](https://blog.gdeltproject.org/announcing-the-gdelt-article-list-rss-feed/)（2021-12-06） | GEMG由来のminute JSON-NLとrolling RSS、title等。dateはpublisher時刻があればそれを使い、なければ観測時刻。遅れて発見/再配信された古い記事が入り得る | dateを一律first-seenとすること、毎分必ずnonempty、upstream全件・当時版の不変性 |
| S03 [GAL historical backfile](https://blog.gdeltproject.org/gdelt-article-list-historical-backfile-2020-to-present/)（2022-01-16） | 2020年へ遡るbackfileの提供説明 | 後に作られた履歴が、当時取得できた配信物と同一であること |
| S04 [GEMG導入](https://blog.gdeltproject.org/announcing-the-global-embedded-metadata-graph/)（2020-12-01） | dateはGDELTが見た日時との説明、title/language等、UTCのminuteファイル。15分heartbeat由来の集中的出力 | immutable first-ever観測、欠けたminuteの空/障害判別、現行提供SLA |
| S05 [GKG 2.1 codebook](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)（v2.1） | record IDの時刻は15分batch作成。V2.1DATEはpublicationとの説明とfile内同一時刻の説明が併存 | 各記事の最初の受信/初観測とbatch時刻の同一性 |
| S06 [GKG page titles](https://blog.gdeltproject.org/gkg-2-0-now-includes-page-titles/)（2019年） | XMLExtrasのPAGE_TITLEというHTML-escaped値 | DOC全文検索とtitle選択の同等性 |
| S07 [GKG article metadata](https://blog.gdeltproject.org/new-gkg-2-0-article-metadata-fields/)（2016年） | publisher時刻の抽出/UTC換算。観測までminutes〜hoursの差があり得る説明 | publication=C前ならd=C前という保証 |
| S08 [GSG導入](https://blog.gdeltproject.org/announcing-the-global-similarity-graph/)（2021年） | 類似記事ペアをthresholdで選ぶgraph、観測時刻の説明、配信処理遅延の説明 | 全記事母集団。類似相手のない記事まで含む完全性 |
| S09 [GDELT About / 利用説明](https://gdeltproject.org/about.html)（日付表示なし） | GDELTがreleased datasetsの広い無償利用・出典表示付き再配布を説明 | 第三者記事本文、全publisher由来title、外部AIへの送信の権利連鎖を個別確定すること |
| S10 [GDELT capacity説明](https://blog.gdeltproject.org/scaling-gdelt-for-a-new-era-migrating-to-spanner-with-agentic-interactive-gemini/)（2026-04-18） | legacy基盤の負荷とrequest shedding、段階的移行計画の提供元説明 | 現在のDOC固有障害率、移行完了、08:00保証 |
| S11 [GDELT retrieval/Spanner説明](https://blog.gdeltproject.org/search-at-spanner-scale-retrieval-not-search-is-now-the-limiting-factor-at-scale/)（2026-06-29） | 検索後の大量retrieval/集計の制約、TV Explorer再設計の説明 | DOCの新しい完全性・時刻契約。4月説明を現在のDOC性能測定へ流用もしない |
| S12 [BigQuery time travel](https://docs.cloud.google.com/bigquery/docs/time-travel)（現行docs） | table変更履歴は既定7日、設定2〜7日 | ニュースの初公表・provider観測・自分の受信の履歴、長期cohort全体の保存 |
| S13 [ECB RSS案内](https://www.ecb.europa.eu/home/html/rss.en.html)（日付表示なし） | 発表、speeches/interviews等の公式feed案内、readerが更新を問い合わせる仕組み | 無限history、revision全版、first receipt、供給元全発表との完全性 |
| S14 [ECB copyright/disclaimer](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html)（現行） | 再利用時の条件と、著者署名付きworking papers等の例外 | 任意の素材を任意のAIへ送る許諾の一括認定 |
| S15 [BOJ RSS案内](https://www.boj.or.jp/en/tips.htm)（日付表示なし） | What's Newのdate/title RSS案内、統計情報との区別 | 配信の保持長・訂正履歴・完全性 |
| S16 [BOJ copyright](https://www.boj.or.jp/en/about/copyright.htm)（現行） | 出典条件、commercial/個別表示等の例外、変更/削除についての条件 | 本研究の商用性・AI分類/送信への適合判断 |
| S17 [LSEG Machine Readable News](https://www.lseg.com/en/data-analytics/financial-news-service/machine-readable-news)（現行商品） | Reuters/第三者newsのreal-time/歴史提供とpoint-in-timeの提供説明 | 当該契約の版・時刻・全件・締切・保持/AI権利。公開定額見積なし |
| S18 [LSEG MRN developer page](https://developers.lseg.com/en/product/news/mrn_realtime_news)（現行） | MRNリアルタイム商品・技術窓口の存在 | この研究で使えるentitlementやSLA |
| S19 [LSEG metadataのaccepted answer](https://community.developers.lseg.com/discussion/11557/mrn-webinar-jan-31-for-mrn-metadata-fields-whats-the-difference-between-versioncreated-and-fir)（公式developer community） | firstCreatedは最初のstory版、versionCreatedは当該版、UTCとの回答 | community回答を現行schema/署名契約と同格にしない。collector receiptではない |
| S20 [LSEG News catalogue](https://www.lseg.com/en/data-catalogue/news)（現行） | stream/API/bulk/archive、NLP/LLM/GenAI向け提供経路の説明 | Joshの契約でChatGPT Plusへの送信や監査共有が許されること |
| S21 [AP Media API overview](https://developer.ap.org/ap-media-api/)（現行docs） | licensed content API、textの30日範囲、Media Agent連続feedの72h範囲・next-page案内 | 保持上限後の完全復旧、無制限archive、AI権利、固定公開価格 |
| S22 [AP Content Metadata](https://developer.ap.org/ap-media-api/agent/Content_Metadata_Fields.htm)（現行docs） | versioncreated/firstcreated、expires/embargoed/pubstatus等。firstcreatedの意味はmedia種別により異なる | 記事の自分への到着、embargo前に利用してよいこと、全版履歴の保持 |
| S23 [AP Usage Instructions](https://api.ap.org/media/v/docs/Usage_Instructions_and_Restrictions.htm)（現行docs） | usageterms/ednote/個別制約・第三者権利の確認が必要な仕組み | APIを持てば全件を長期保存・AI処理できるという包括許諾 |
| S24 [RavenPack News Analytics](https://www.ravenpack.com/products/edge/data/news-analytics)（現行商品） | realtime/歴史news analytics商品、独自のannotations | raw title/全版をこの仮説で使用できる権利とschema、公開費用 |
| S25 [RavenPack Annotations](https://www.ravenpack.com/products/annotations)（現行商品） | realtime捕捉のpoint-in-time archiveを商品説明として提示 | その表示だけで自分の受信・全件・原稿保持を認定すること |
| S26 [Benzinga API docs](https://docs.benzinga.com/home)（現行） | News APIとupdatedSinceによるdelta収集の案内、license窓口 | deltaが任意の切断期間を必ず埋めること |
| S27 [Benzinga news stream](https://docs.benzinga.com/ws-reference/data-websocket/get-news-stream)（現行） | created/updated/deleted action、timestamp、heartbeatの技術仕様 | 全履歴の連番証明、最大遅延保証、元版の保存権 |
| S28 [Benzinga replay action](https://docs.benzinga.com/ws-reference/actions)（現行） | cached replayは最大100件、keyにより範囲が変わる | replay範囲を超えた切断時の完全性 |
| S29 [Benzinga AI/LLM licensing offer](https://www.benzinga.com/apis/datasets-for-training-llms-and-ai-applications/)（現行商品） | AI用にlicensed contentを提供する別の商用案内 | 普通のNews API keyがそのままAI権利を付与すること |
| S30 [Event Registry / NewsAPI.ai plans](https://newsapi.ai/plans)（現行商品） | realtime等の提供、page/token制約、表示上の月額US$90プランを確認 | 契約範囲別の総費用、時点snapshot、immutable firstseen、全版。terms本文の十分な確認ができず権利未確認 |
| S31 [NewsAPI.org pricing](https://newsapi.org/pricing)（現行） | Developerは24h遅延・開発専用。Business US$449/月、Advanced US$1,749/月、後者99.95%uptime表示 | 無料枠の本研究運用適合、日次cutoff SLA、費用総額 |
| S32 [NewsAPI.org terms](https://newsapi.org/terms)（表示更新2020-04-30） | 第三者data権利・利用/公開の制約。料金とは別に確認が必要 | title/rawの永続保持、公開研究/独立監査・ChatGPT送信の包括許諾 |
| S33 [NewsAPI.org Everything schema](https://newsapi.org/docs/endpoints/everything)（現行docs） | publishedAt UTC、pageSize最大100とpagination | publishedAtが初観測であること、ページ間snapshot固定、訂正履歴、全件PIT |
| S34 [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html)（2001年） | hashの時刻証明、時刻精度・信頼の枠組み | 元source本人性、実際の初受信、上流完全性 |
| S35 [RFC 8915 NTS](https://www.rfc-editor.org/rfc/rfc8915.html)（2020年） | 認証付き時刻同期、非対称遅延等の限界 | 時計誤差ゼロや特権writerの過去時刻捏造防止 |
| S36 [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)（現行docs） | complianceとgovernanceの権限差、version単位の保持、account削除等の限界 | 保管する内容の真正性、ライセンスに反する保存の正当化 |
| S37 [COS preregistration](https://www.cos.io/initiatives/prereg)（現行） | データを見る前の計画登録と、既知のアクセス/変更の透明化という方法論 | 登録しただけで測定やsourceが適格になること |
| S38 [Rubin, Inference and missing data](https://academic.oup.com/biomet/article-abstract/63/3/581/270932)（1976-12-01、doi:10.1093/biomet/63.3.581） | 論文abstractを確認。欠測機構を無視するには条件が必要という方法論 | FXNSで欠測がrandomであること。全文読了・実データへの検証を主張しない |
| S39 [GitHub skip workflow docs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)（現行） | commitの[skip ci]はpush/pull_requestに適用、pending checkが残り得る | pull_request_target等の別eventには適用されない。実際のrun有無は別途確認 |

費用は確認日の表示であり、税・利用量・監査共有・再配布・AI権利・archive・サポート等を含む確定見積ではない。LSEG/AP/RavenPack/Benzingaは、この調査で必要な範囲の公開固定費を立証できなかった。見積取得・契約締結・購入はしていない。Event Registryのterms `https://newsapi.ai/terms` は取得した本文が十分に読めず、確認済み許諾としない。

## 5. 方式別の保証比較

下表は公開資料による**限定した保証**の評価である。別途収集器を作った場合の想定は6節に分ける。表のSUPPORTEDは、そのセル内の狭い事項だけを指す。

| 方式 | 母集団/網羅性 | first-seen・実受信 | as-of/訂正・削除 | UTC/端点・08:00 | caps/障害 | 保存・AI権利/監査 |
| --- | --- | --- | --- | --- | --- | --- |
| 固定DOC＋自分のreceipt補完 | NOT_ESTABLISHED：250未満も全件証明なし | PARTIAL：自分のrを記録可能、sの意味未解決 | NOT_ESTABLISHED：後取得indexは当時版でない | PARTIAL：時刻指定あり。締切/等号契約は不明 | SUPPORTED_BY_SOURCE：250上限。完全な欠落検知は不明 | PARTIAL：S09、独立保全は別設計。publisher/AI権利未確定 |
| GEMG/GAL minute-file捕捉 | PARTIAL：配信ファイル集合を対象にできる。全ニュースではない | PARTIAL：GEMG seen説明。GAL date混在。rは自分で必要 | PARTIAL：捕捉bytesは復元可能。上流書換/遅延fileは不明 | PARTIAL：UTC filename。配信/commitの保証ではない | PARTIAL：DOC capを迂回する輸送。missing minuteの意味未確認 | PARTIAL：GDELT一般説明＋自前保全、第三者権利は残る |
| GKG batch＋PAGE_TITLE | PARTIAL：GKG処理対象。DOC選択と別 | PARTIAL：batch DATEは記事firstseenでない | NOT_ESTABLISHED：当時版の完全履歴未確認 | PARTIAL：batch時刻、08:00直前batchは遅れる | PARTIAL：batch download可否と完全性は別 | PARTIAL：metadataの利用説明、AI/title権利未確定 |
| GSG/派生graph | NOT_ESTABLISHED：threshold pairによる選択 | PARTIAL：観測時刻説明、rなし | NOT_ESTABLISHED：全記事・全版でない | PARTIAL：遅延説明あり、締切は不明 | NOT_ESTABLISHED：母集団の回復に使えない | PARTIAL：補助的監査に留める |
| BigQuery/後日archive検索 | PARTIAL：table内の現時点集合 | NOT_ESTABLISHED：過去DATEは実受信でない | PARTIAL：DB time travelは短期間、article vintageと別 | NOT_ESTABLISHED：当日取得の証明なし | PARTIAL：query/storage費・snapshot設計が必要 | PARTIAL：元data権利と保管権利は別 |
| ECB/BOJ公式通信RSS | PARTIAL：公式feed内、FX全ニュースでない | PARTIAL：date/titleの案内、自分のr必須 | NOT_ESTABLISHED：rolling消失/改稿の全履歴 | NOT_ESTABLISHED：遅延上限/端点なし | PARTIAL：pollingと空feed/障害の区別が必要 | PARTIAL：公式条件に例外、commercial/AI/監査の判断残る |
| LSEG MRN＋自分の受信保全 | PARTIAL：契約source/channel内 | PARTIAL：first/version区別の回答、r必須 | PARTIAL：PIT/歴史商品。契約schema/全版要確認 | PARTIAL：UTC版時刻回答。自分の締切は別 | NOT_ESTABLISHED：この研究のsequence/gap/replay/SLA未確認 | PARTIAL：AI向け提供経路あり、具体的entitlement未確認 |
| AP Media Agent＋自分の受信保全 | PARTIAL：entitled feed内 | PARTIAL：first/version metadata、r必須 | PARTIAL：版/embargo/statusと短期feed。全期間保証なし | PARTIAL：時刻metadata。公開/利用可能時点の区別必要 | SUPPORTED_BY_SOURCE：72h feed/30d text範囲。完全復旧保証は別 | PARTIAL：個別usageterms、AI/長期保存/監査契約が必要 |
| Benzinga stream＋delta＋保全 | PARTIAL：Benzingaの契約集合 | PARTIAL：update/timestamp、r必須 | PARTIAL：created/updated/deleted。過去bytesは自分で保持 | NOT_ESTABLISHED：s/最大latency/端点未確認 | SUPPORTED_BY_SOURCE：replay最大100。超過gapが残る | PARTIAL：AI用offerは存在、通常APIとの権利同一性なし |
| RavenPack PIT/analytics | PARTIAL：契約されたpremium集合 | PARTIAL：PIT capture説明、rとは別 | PARTIAL：archive説明。raw版の完全性不明 | NOT_ESTABLISHED：研究の締切条件なし | NOT_ESTABLISHED：具体的契約/復旧条件未確認 | PARTIAL：raw title/AI/独立監査権未確認 |
| NewsAPI.ai / Event Registry | PARTIAL：aggregator coverage | NOT_ESTABLISHED：immutable s/実受信仕様未確認 | NOT_ESTABLISHED：as-of版履歴未確認 | NOT_ESTABLISHED：cutoff SLAなし | PARTIAL：page/token制約、snapshot完全性未確認 | NOT_ESTABLISHED：terms十分に確認できず |
| NewsAPI.org | PARTIAL：対象sources/API結果 | SUPPORTED_BY_SOURCE：publishedAt UTCのみ。s/rは不明 | NOT_ESTABLISHED：全版履歴/時点snapshotなし | NOT_ESTABLISHED：無料24h遅延は当日取得目的に不適合 | PARTIAL：pagination。paid uptimeは全件/cutoffと別 | PARTIAL：第三者権利・公開制約。永久保存/AIは要確認 |
| 独立receipt・時刻証明・WORM単独 | NOT_ESTABLISHED：上流漏れは証明しない | PARTIAL：自身の情報集合を強くできる | PARTIAL：捕捉した版は再現できる | PARTIAL：誤差境界と締切前w/dが必要 | NOT_ESTABLISHED：失われた上流messageは復元しない | PARTIAL：証拠保全技術。取得/保持権を付与しない |

現行DOCを補完する案は比較上残すが、#107が停止した固定DOCのformal適格化を再開する理由にはならない。受信証明を足しても、DOCの完全性・seendateの意味・版履歴は埋まらない。

## 6. 候補アーキテクチャの具体像と欠陥

### 6.1 全候補に必要な受信・保存・監査の層

将来の実装候補は、(1)provider配信、(2)連続collector、(3)許諾されたrawの耐久保管、(4)独立receipt/監査先、(5)cutoff集合の固定、の順に設計する。各層が証明するものを混同しない。

collectorの原記録には、request条件、response status、許諾上必要なheaders、cursor/sequence、source/article/version ID、contentのbytes hash、receive start/end UTC、monotonic値とboot ID、durable commitのUTC、clock誤差範囲、parse結果、retry/gap/heartbeat/queue異常を残す。API key、認証headers、個人情報は公開receiptへ入れない。失敗やparse不能も記録し、成功だけを保存しない。

保存は原bytesを保全してから正規化する。記事IDと版IDを分け、更新・撤回はappend-onlyで記録する。同一版IDで異なるbytesや、一つのcursorに不一致があれば停止する。後からurlを再取得して元headlineを補完しない。post-cutoff訂正を知っても、当時の入力集合を書き換えない。

cutoff集合は許可された時刻規則を満たす既存保管物だけから作り、選択/dedup/parserのexact version、article/version/hash一覧、除外理由、集合hashを固定する。自分のreceipt基準を採用する場合でも、古い記事の再配信やversion更新を毎日新規とするかは別の事前規則が必要である。時刻基準を変更しただけで現行24h仮説の同等性が成立するとはしない。

耐久保管はversion・retention・アクセス権を監査する。署名鍵の所有者とwriter、独立監査保管の管理者を可能なら分離する。定期hash chain/Merkle rootを独立先へ送る場合、cutoff前の存在を示したいなら、独立先の時刻上側境界もC未満である必要がある。締切後のtimestampは「少なくともその時には存在」の証拠であり、ローカルの過去時刻を遡及保証しない。 独立receiptを締切前の必須条件にする場合、その転送遅延もgと確定境界の設計に含める。

RFC3161はhash存在時刻、NTSは時刻同期、Object Lockは保存後の変更制約を扱う。どれも上流の記事本人性や未収録記事の不存在を単独で証明しない。writer侵害なら、署名済みの捏造/欠落があり得る。二つのcollectorが一致しても、共通providerが落とした記事は検出できない。脅威・管理主体・network経路の独立性を文書化する。

独立監査者には、契約上認められたprivate rawへのread-onlyアクセスと、source/version/clock/manifestから入力集合を再構築する手順が必要である。公開GitHubには許諾済みmetadata/hash/コードidentityを残す設計が可能だが、hash公開だけで内容監査が済むとは言わない。公開rawを必須にして契約違反を招く案も採らない。保持義務と撤回/削除義務が衝突する場合は契約で解決し、解決できなければ採用しない。

これらは設計案であり、鍵、bucket、ACL、runtime、署名サービスを新設していない。Aの台帳/真正性設計とはinterfaceを合わせる必要があるが、本報告でAの方式を決定しない。

### 6.2 GDELTの別機構を連続捕捉する案

**GEMG/GALのminute-fileを、掲載を発見した時点から連続保存する。** file pathのUTC、取得時刻、hash、content長、HTTP結果、manifestを保全し、同pathの後の内容変更も新しい版として記録する。GALのrolling RSSは未捕捉の短時間消失を招き得るので、履歴fileのcaptureとheartbeatの証拠を中心に評価する。

強みは、DOCのtop-250 listに依存しない輸送経路と、自分が保存したmetadataのas-of再現である。GEMGのseen説明はGALの混合dateより目的に近い。ただし初回か再観測か、不変か、file更新があるか、現在の保持/配信が過去説明と同じかは未確認。15分heartbeat由来のminute集中を「missing file=空」と決めない。提供元のexpected-file manifest、no-news信号、公開時刻の上限がなければ、ファイル集合の完全性も限定される。

sourcefilterをtitle/languageで行う案では、DOC全文queryを再現できない。GKGのPAGE_TITLEやmetadataからの選択も別hypothesisとなる。本文を取得して一致させる案は、title-only研究の入力と権利・負荷を変えるため別承認になる。GSGは類似pairに入らない記事が欠けるので、全件母集団には使えない。N-gram/派生量を用いた本文推定も現行設計を保つ解決ではない。

historical backfileやBigQueryの最新queryは、過去にこのcollectorへ届いた集合を復元しない。BigQueryの短いtable time travelを長期のnews vintage保存と取り違えない。将来継続snapshotを自前保存するなら、その捕捉時点以降の証拠に限定する。

**残る欠陥**：上流recall、file欠落のoracle、version/first-seen、right chain、締切の最大lag。無料dataでも常時収集・監査・storage・復旧の費用はゼロでない。現行query/estimandに互換と認定できず、formal候補はBLOCKED。

### 6.3 ニュース提供元の公式feedを捕捉する案

ECB/BOJの公式通信feedを対象にし、既知の許可されたchannelを固定する。ここでいう候補はpress release、speech、communicationのtitle等であり、統計feed、為替レートfeed、実ECB観測値を対象にしない。RSSのdate/last modified、HTTP ETag、conditional requestは更新検知に役立つが、更新の全版・初受信・供給元全発表との一致を保証しない。

captureしたRSSの全bytesと記事ID/title版を保存すれば、自分の情報集合を再現できる可能性はある。poll間に現れて消えるitem、rolling feedからの退場、同じIDの改稿、timezone欠損を失敗条件にする。feed全件と通信section全件の照合を将来実施するなら、それ自体が新たな実ニュース閲覧であるため、今回は行っていない。

**残る欠陥**：機関発表はmedia/news reactionを含まない。媒体選択・language・記事数・時刻分布が変わり、元のFXNS効果を検証したとは言えない。BOJのcommercial/変更条件、ECBの素材別例外、外部AI送信・長期監査保持を確認する。機関数が少ないことは実装負荷を減らし得るが、科学的妥当性を自動で高めない。権利・feed完全性・新仮説の承認が必要。

### 6.4 ライセンス付き版管理配信＋独立receipt案

契約source/channelとentitlementを固定し、published/first/version/embargo/withdrawal時刻、stable IDs、sequence/cursor、再送を一体で取得する。streamを一次記録とし、archiveは欠落調査と将来の検証に使う。締切後archiveで取得した古いpublicationの記事を、当日利用できたものとして補充しない。

- **LSEG MRN**：広いnewsとPIT/歴史商品の現行説明は有望な入口。ただしfirst/versionのcommunity説明を契約保証に格上げしない。具体的delivery schema、continuity、全版archive、配信遅延、AI/監査権を入手する必要がある。
- **AP Media Agent**：first/version、embargo/statusとfeed cursorの仕様が比較に使える。72h feed/30d text範囲を超える停止・保持には別解決が必要。subscriptionでembargo素材が先に配信された場合、「一般公開news」の情報集合へ混ぜない。個別利用制約を自動審査できるかも確認する。
- **Benzinga**：created/updated/deletedがある点は単純なpublishedAt検索より監査に向く。しかし最大100件のreplayだけでは長いdisconnectやburstを埋められない。deltaの保持長・版復元・cursor確定と契約上のAI用licenseを別々に調べる。
- **RavenPack**：PIT archiveの商品説明は入口だが、raw headlines/versionsを使えるか不明。提供元のsentiment/annotationを使えば、ChatGPTによるtitle分類という測定を変える。良いsentiment値があるから置換してよいとはしない。

**残る欠陥**：公開商品説明と研究用契約の差、recallの対象限定、第三者素材の例外、entitlement変更、災害復旧、外部AI共有、費用/サポート負担。高価格と高いuptimeは08:00の因果的利用可能性を代用しない。providerのversion timeも自分のr/dではない。

RESEARCH_LINEの「有料news feedなし」を維持するなら、この案は現在の計画では選べない。費用条件を変える人間判断から始めるべきで、未公表価格を仮定して「実現可能」と結論しない。

### 6.5 一般aggregator、固定DOC補完、独立receiptのみ

NewsAPI.orgの無料Developerは24h遅延・開発用途制限があり、当日までに到着した最新情報の本運用候補としては不適合。paidプランでもpagination/publishedAt/uptimeだけではimmutable vintageを証明しない。NewsAPI.aiもpage/tokenと広いcoverageの商品説明だけではs、全版、snapshot、権利を立証できない。

固定DOCに自分のreceive timestamp・signatureを追加する案は、取れたresponseの保存を改善し得る。ただし250未満を完全とできず、後のqueryのindex状態も当時と同じとは言えない。cap変更、time split、retry、query変更による「救済」は現行仕様変更なので今回は行わない。

独立receiptを単独sourceとして考えるのも誤りである。receiptは採用する配信に必須の横断的な層であり、ニュースの母集団を提供しない。

## 7. 科学的妥当性の独立評価

### 7.1 先読みと時点情報の漏洩

後日取得した記事に古いpublication/firstCreatedがあるだけでは、当日のtitle版を知っていたことにならない。更新後headline、遅延収録、訂正・削除後の最新index、事後のtranslation、historical backfillをC前の情報へ混ぜると先読みが起き得る。これはproviderが不正という意味ではなく、測定対象と取得vintageを区別しない研究設計の問題である。

eligibilityは、契約上の利用可能時点、必要なrelease/embargo解除、採用するs/r/d、clock uncertainty、版IDを同時に満たす必要がある。embargoが残るlicensed inputを「その時一般に読めたnews」と呼ばない。rとdがC後なら、publication=C前でも取得期限を満たさない。後日訂正は監査注記であり、発行時入力の上書きではない。

historical LLM評価には、モデルが学習で記事や事後情報を知っている危険もある。将来の記事をその時保存した入力で前向きに処理する設計はその経路を減らすが、閉じたChatGPT製品の全学習履歴や非表示更新を証明はできない。model表示/設定、prompt、出力原文、受信/確定時刻を保全し、製品更新・不明挙動の停止規則を再凍結時に決める。

### 7.2 収集後の仕様変更と研究者自由度

市場outcomeを見ていなくても、入力件数、titleの内容、取得しやすい媒体を知ってからquery/provider/filter/dedupを選ぶと、事前仮説と測定を適応させる。結果が良くなる方向だけがbiasではなく、都合のよい入力分布へ選ぶことも問題になる。

qualification pilotは将来のformal cohortと分離し、許可されたsource性能・metadata目的、期間、失敗条件、閲覧担当、変更判断の時点を先に記録する。pilot収集物を後でformal第1日へ昇格させない。変更理由は科学的・運用的根拠とし、閲覧履歴も開示する。今回の逸脱を含む既知の入力接触は、独立担当と人間の処分なしに「データ未見」と宣言しない。COSの登録原則はこの透明化を支持するが、sourceを自動適格化しない（S37）。

### 7.3 取得失敗とsample selection

news burst、高負荷、災害等のときにfeed/LLMが失敗しやすければ、成功日に限定したsampleは通常日へ偏る可能性がある。これは**仮説上の経路**であり、この調査で市場との相関を観測した事実ではない。Rubinの方法論に照らしても、欠測を無視する条件を確認せずrandomと置く根拠はない（S38）。

すべての予定sessionを、cutoff、収集可否、欠落、遅延、classification未完等の理由で記録する。失敗はNO_TRADEやreturn=0に置き換えず、取得成功のformal eventと別に扱う。取得できた日の効果を推定するなら、その条件付き対象であることを明記し、全予定日へ外挿しない。

現行SPECは推奨60適格event、失敗はvalid cohortにならず、発行済みeventは保持する。将来の再設計では、calendar終了条件、成功数による終了条件、失敗率の分母、運用availabilityの評価、観測期間延長規則を事前に定義する必要がある。結果や見たいsampleが揃うまで任意に延長する案は避ける。ここで60や既存failure規則を変更していない。

### 7.4 遡及取得とリアルタイム取得は非同等

historical archiveは、後に追加/訂正されたarticle、再処理されたlanguage、stable IDの統合、後のlicensing範囲を含み得る。archiveにfirstCreatedがあっても、その時配信されたbytesの存在と自分のentitlementは別である。契約が当時のdelivery versionsを保持し、別のreceipt証拠と対応する場合だけ、限定された同等性を検証できる。

最新archiveで隙間を埋めるのは、欠落の診断にはなっても締切前取得の救済ではない。sourceが変わればreference populationも変わるため、二つの時系列を継ぎ合わせて一つの凍結済みexperimentと呼ばない。

### 7.5 再現性の範囲

再現対象を分ける。(a)原bytesと当時入力集合、(b)選択/dedup/集計の決定的処理、(c)当時のLLM出力とその確定記録、(d)同じLLMを将来再実行した結果である。

(a)(b)(c)の監査可能性を設計できても、閉じた製品や非決定的出力の(d)は一致を保証できない。再実行で結果が違っても、当時保存した出力を新結果へ差し替えない。実験再現性を「raw hashあり」だけで済ませず、仕様、parser、model/prompt、依存物、clock、entitlement、入力一覧と出力証跡を組にする。

### 7.6 再承認・再凍結の条件

現在はPROPOSED_NOT_FROZENであり、凍結済み仕様を実運用したという扱いにしない。凍結候補からの変更でも、source/query/窓/時間/版/dedup/モデル/費用に実質差があれば、変更表、旧設計との非互換点、新仮説と一般化範囲を明示する。

新SOURCE_CONTRACT、timestamp/rights/receipt定義、取得・分類締切、欠測・終了規則、独立監査、実装のexact identities、人間承認を揃えてから、新しい未使用の将来cohortを再凍結する。qualification既存rawやpilotでformal eventを作らない。source、台帳、モデル、価格sourceの各別gateが閉じていれば、どれか一つの設計承認で全体を開かない。

## 8. 技術・契約・運用・費用と証拠収集の優先順

運用負荷は本調査の設計上の推論であり、実測costや見積ではない。

| 条件付き案 | 技術的見込み | 契約/法的な未確認 | 運用・費用 | 優先する追加証拠 / 採らない条件 |
| --- | --- | --- | --- | --- |
| 版管理licensed stream＋独立保全 | sequence/版/再送を契約できれば最も直接的。ただし公開資料だけでは未成立 | 全素材title/raw、外部AI、audit、termination後保持、第三者例外 | 常時接続・support・監査・license。価格未確定、現行有料feedなしに非互換 | **広いnews仮説なら証拠収集第1候補**。signed schema、範囲manifest、gap/replay、最大lag、rights schedule、見積。取れなければ停止 |
| GEMG/GAL連続捕捉＋受信集合へ仮説変更 | file輸送とas-of保存は設計可能。upstream完全性は未成立 | metadata/titleの権利連鎖、AI/audit共有 | data無償説明、常時poll/file保存・欠落調査/監査は必要 | **有料を避ける場合の第2候補**。現在の配信・file確定/空minute・seen semantics・権利。DOCと同じ集合必須なら不適合 |
| ECB/BOJ通信feed＋新しい狭い仮説 | 小さな既知channelの捕捉は比較的単純。履歴oracleは必要 | commercial/素材例外/改変/AI/監査 | API費不明/通常公開feed、pollと保管/監査費 | 機関発表だけでよいという人間判断、feed全件/版/retention、権利。元の全FXnews仮説維持なら不適合 |
| DOC＋receiptのみ | 保存改善は可能、根本保証未解決 | GDELT/第三者/AI | 429/cap/短時間deadline調査が残る | **formal再開は推奨しない**。#107の停止維持 |
| GKG/GSG/BigQueryによる代用 | batch/graph/最新queryは対象・時刻が異なる | 派生/本文/第三者権利 | batch解析/query/storage追加 | 補助研究に留める。全件PITや現行queryの代用とするなら不適合 |
| 一般aggregator paid API | pagination/deltaだけでは版・欠落保証不足 | 永久保持/AI/公開audit不明 | 公開料金＋query/token/storage/監査 | provider署名のsnapshot/版/権利が追加されなければ順位を上げない |
| NO_QUALIFIED_ALTERNATIVEを維持 | 研究上正当な停止 | 新しい契約なし | 新規source運用なし | 予算、rights、oracle、締切、独立監査が充足しない場合の推奨 |

「最適商品」を決める根拠はない。必要証拠に対して調べる順序を示したものである。vendorへの連絡、購入、provider key発行、live pilotは今回実施していない。

## 9. 次に人間が判断する操作単位

今すぐ包括的な「研究再開」を求めない。以下を具体的な提出物・allowlist・責任者・停止条件付きで別々に判断する。承認済みなのはこの比較調査と報告だけである。

| 順序 | 承認対象となる操作 | 判断前に必要な具体的提出物 | 承認しても解禁しないもの |
| --- | --- | --- | --- |
| 1 | 本Waveと#106の閲覧逸脱の処分・独立影響確認の範囲 | 禁止内容を再生しない操作/出力記録、成果のmetadata、独立担当、検証不可範囲 | raw/実例の再取得、clean認定、市場outcome |
| 2 | 研究母集団・時刻基準・予算の選択 | 広いlicensed範囲/自分の受信集合/機関発表の差、旧query非互換、C−g等の候補、費用条件 | source資格認定、現行SPEC変更、実取得 |
| 3 | 具体的providerへの技術・利用条件照会 | 質問票、連絡先、求めるschema/rights/SLA/見積、送信する情報 | 契約締結、購入、key作成、実headline |
| 4 | 新しいSOURCE_CONTRACT/SPEC候補の作成 | 採用候補が証拠を満たした場合のみ、変更allowlist、新仮説/時刻/版/失敗/終了規則 | 実装、既存仕様の無断置換、formal cohort |
| 5 | collector/保管/署名/監査の実装と合成試験 | 正確なコードallowlist、責任者、権限、key/retention設計、下記の受入oracle | live data、production権限、merge、market access |
| 6 | source-only qualification pilot | 対象endpoint/取得期間/件数/保持権、clock/独立監査、閲覧分離、失敗規則、旧raw非使用 | 分類/取引/market outcome、formal event、後付けcohort化 |
| 7 | 独立監査とsource判定 | 契約・runtime証拠・完全性の限定・失敗全件・再構築結果、残存risk | 他gateの解禁、取引開始 |
| 8 | 新しい将来cohortへの再承認・再凍結 | 全候補/実装identity、事前登録、既知アクセス、各別gateの閉鎖解消、開始日 | 承認範囲外の市場データ/運用操作 |

3の照会はメッセージ送信を伴うため、宛先・本文まで別承認に含める。規約適合は本報告で法律判断しない。既存A/E設計と責任分離を合わせ、provider選定だけで署名鍵や保管責任者が決まったことにしない。

## 10. 後続実装・独立監査の受入条件

以下は**未実行の受入仕様**。すべてNOT_EXECUTED。将来の承認後に、各行の証拠と負例を独立監査する。必要oracleがproviderから得られない場合、「試験で問題が出なかった」を完全性証明にせずNOT_ESTABLISHEDとする。数値g、Lmax、時計誤差上限、rate/容量、pilot期間、保持期間は現在未決であり、結果を見て調整する前に合意する。

| ID | 受入条件・必要証拠 | 必須の負例と停止期待 |
| --- | --- | --- |
| 01 | source/channel/language/type/field/entitlementと排除範囲が契約・仕様に一致。対象がprovider全件か自分の受信集合か明示 | 未知channel、契約範囲の変更、全文検索/title検索の混同 → BLOCKED |
| 02 | first observation/first version/current version/配信時刻の定義・精度・不変性が署名資料で対応。metadata mappingを独立レビュー | timestamp名だけで意味を推測、sが再観測へ上書き → BLOCKED |
| 03 | stable article IDとversion ID/bytes hashを区別。rawを保持したまま版更新をappend | 同URL新headlineが旧版を上書き、同版IDでbytes不一致 → BLOCKED |
| 04 | 対象配信全件を主張するならsequence/確定manifest/snapshot等のoracleで欠落を照合 | 250件超burst、queue overflow、欠番、page途中timeout → partialをformal利用せずBLOCKED |
| 05 | paginationは固定snapshotか同等のcursor contract。timestamp同値tie、追加/削除中のページ移動を検査 | totalResultsだけで完了とする、ページ移動で漏れ/重複を見逃す → BLOCKED |
| 06 | no-newsと接続断をheartbeat/manifest等で判別。missing minuteの許容理由を証明 | 空body、404、欠けたminuteを自動でnews=0 → BLOCKED |
| 07 | cutoffはtimezone-aware UTCで計算しJSTと一致。元offset/精度も保全 | 08:00 JST≠前日23:00 UTC、publisher DST誤変換、naive datetime → BLOCKED |
| 08 | 現在の両端開区間を保持する場合、start=end境界・秒丸め・等号を独立検査。変更は事前承認 | 端点等号を採用、half-openへ暗黙変更、時刻不確実性が端点に接触 → BLOCKED |
| 09 | r_start/r_end/dとmonotonic/boot ID、同期状態・誤差境界を保存。clockの数値上限は事前合意 | clock後退、再起動でmonotonic混在、同期故障、offset上限超過 → BLOCKED |
| 10 | 採用するCと余裕g/遅延仕様が一貫。必要なr/dの時刻上側境界<Cを立証 | requestはC前だがlast byte/commitはC後、HTTP DateだけでPASS → BLOCKED |
| 11 | 保存完了はatomicity/耐久性の契約に従い、crash復旧後にbytes/hash/manifestをreadbackできる | network receiptのみ、partial write、fsync/commit未了、復旧時欠損 → BLOCKED |
| 12 | 遅延記事・更新・削除を版履歴として残し、C後に初めて受けた内容は当日集合に入れない | p/sがC前だからC後receiptを採用、訂正後titleへ過去置換 → BLOCKED |
| 13 | embargo/usage restrictionを機械的に検証し、研究の利用可能時点とpublic情報時点を区別 | embargo未解除、個別usageterms不明、entitlementなし → BLOCKED |
| 14 | reconnectはgapをoracleで埋める。再送の保持長・容量・重複処理を証明 | Benzinga型100件replayを超えるgap、AP型feed期間超過、cursor失効 → 診断記録を残しBLOCKED |
| 15 | 429/timeout/5xx/credential失効を全件記録。retryのdeadlineと限度を事前定義 | C後retryで「当日成功」へ変更、成功だけ保存、provider切替で隠す → BLOCKED |
| 16 | 選択/dedup/parserはoutcomeを見ずに凍結。同URL改稿、syndication、新URL、Unicode/空titleを検査 | 複数版を誤統合、後から都合よいkeeper、parse不能を黙って捨てる → BLOCKED |
| 17 | raw/headline/metadata、派生分類、ChatGPT Plus送信、private独立audit、公開metadata、終了後保持に明示許諾 | paid key/公開URLだけで許諾、第三者例外未確認 → BLOCKED |
| 18 | 撤回/削除要請と必要な歴史保持の手順を契約で解決。許される証跡だけ残す | WORMを理由に権利上の削除義務を無視、原稿保持不能なのに再現可能と主張 → 採用停止 |
| 19 | hash、署名、独立receipt、保管version/retention、trust store/key lifecycleを別々に監査 | writerがraw+digest+local clockを一括置換しても検出できない → 真正性未成立/BLOCKED |
| 20 | cutoff前存在を主張するなら独立wの上側境界<C。鍵/監査先の独立管理と侵害時の停止規則 | C後anchorで過去時刻を証明、同一特権者が全証拠を改変可能 → BLOCKED |
| 21 | 独立監査者がofflineの許諾済み保存物だけで当日入力一覧・hashを完全一致再構築 | 最新API再取得、archiveで欠落補充、監査先にraw閲覧権なし → NOT_ESTABLISHED/BLOCKED |
| 22 | すべての予定session・failure理由・成功分母・終了/延長規則を事前固定 | acquisition失敗をNO_TRADE/0、都合よいsession削除、任意に60成功まで延長 → BLOCKED |
| 23 | news量・burstと分類/検証時間の余力を事前定義した負荷条件で測る。08:15前に当時出力を確定 | 遅延出力、入力capの事後選択、失敗LLM出力を後で差替え → BLOCKED |
| 24 | model/prompt/schema/出力原文/確定時刻を保存。表示更新と不明なproduct変更の取扱いを事前規定 | 再実行一致を当時出力の代用、未知updateを隠す → 再現性の限界開示/必要ならBLOCKED |
| 25 | pilotとformalを分離し、既知アクセス/逸脱と変更理由を記録。独立監査と再承認後の未使用将来期間で開始 | 旧raw/pilotのcohort昇格、自己clean認定、設計承認だけでformal gate開放 → BLOCKED |

finite pilotは、そこで観測した性能と負例への挙動を示す。世界の未観測記事を含む完全性、将来の障害ゼロ、未申告のpublisher権利を数学的に証明しない。qualification判定には、契約上の範囲、検証可能なoracle、運用証拠、明示した残存riskの人間受容が併せて必要である。

## 11. 保存・readbackの範囲と維持する状態

既存open FXNS報告のmetadataと研究treeを確認し、このpre-freeze代替方式の比較を重複するB報告は見つからなかった。新規価値があるため、#63 exact headからB専用branchを作り、このallowlist内の1ファイルだけを独立Draft PRに保存する。baseは `research/fx-news-sentiment-v0.1`。旧#106/#107等を更新・mergeしない。

remote readbackでは、新PRのOPEN/Draft、base/head、head commit/tree、report blob、UTF-8全文、SHA-256、全changed paths=この1ファイル、baseとの差分を照合する。自身のcommit/hashは本文へ自己参照させず、検証後のPR本文に記録する。report pathは既存合成workflowのPR path filterに該当し得るため、報告commitへ `[skip ci]` を付け、新規runを要求せず、run metadataのみ確認する。これはworkflowの変更ではない。8本の既存workflowのtriggerを静的に確認し、pull_request_targetはなかった。skip指定の適用とpending checkの限界はS39に基づく。

**live DOC/API/feed/実記事の意図的取得、saved raw閲覧、実為替/XM/MT5/ECB観測値取得、分類、backtest、実装、tests、workflow操作、鍵/保管環境新設、merge、formal source認定は行っていない。** ただし検索・文書応答に混入した禁止情報の表示は2節の逸脱として残し、この列挙を完全な無曝露宣言には使わない。

最終状態は **SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / UNTESTED / PROPOSED_NOT_FROZEN**。条件付き候補があることと、採用資格を満たしたことは区別する。現在の証拠で正式採用を許す判断はしない。

