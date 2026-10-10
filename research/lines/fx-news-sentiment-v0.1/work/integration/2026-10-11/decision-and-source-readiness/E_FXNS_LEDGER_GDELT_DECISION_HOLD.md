# E — FXNS台帳・GDELT根拠の統合判定（2026-10-11 JST）

**結論：`FXNS_DECISION_READINESS_ADVANCED / LEDGER_CONTRACT_HUMAN_DECISION_REQUIRED / SOURCE_QUALIFICATION_BLOCKED / HOLD_NO_MERGE`。** 新しい意思決定資料と提供元による運用上の説明を受領したが、台帳方式の承認、固定DOC sourceの適格化、formal cohortの開放、取引評価への進行はいずれも認めない。本E自身は試験・GDELT DOC API呼出し・実記録の再取得・実取引を行っていない。

## 1. 受領の範囲とexact identity（GitHubで本Eが独立に再取得）

- Repository: `Josh-Temple/systematic-trading-research`。本報告の作成前のFXNS研究branch `research/fx-news-sentiment-v0.1` / [#63](https://github.com/Josh-Temple/systematic-trading-research/pull/63)：HEAD `24ef9c37e6255126a957f38cfa7470cd150ed594`、tree `123f6d539c29f188e489bcc1492b632f5c9514d7`、OPEN/Draft。本報告はこのコミットから分離したreport-only branchに保存し、研究branchにmergeしない。
- `main` HEAD `33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3`、tree `be858570de929678a219660cb8f0b3d26b038516`。不変・変更禁止。
- 新A [#105](https://github.com/Josh-Temple/systematic-trading-research/pull/105)：OPEN/Draft、base `research/fx-news-sentiment-v0.1`、head `cda9bcec3ddbd352845c77fa73bb60d28e6b1cab`、tree `e3a94b11038f3a37aab8230911945f9dad352c3b`、report blob `b4e7d951778e1d9d8f4ba1648b205561a0fff7df`。変更パスは `research/lines/fx-news-sentiment-v0.1/work/assurance/2026-10-11/ledger-decision-readiness/A_FXNS_LEDGER_DECISION_READINESS.md` **1件のみ**。実報告本文をexact refで直接読んだ。
- 新B [#106](https://github.com/Josh-Temple/systematic-trading-research/pull/106)：OPEN/Draft、同研究branch base、head `d29afe155210234ef137d8928a1564408179a0f7`、tree `3bfe63e4636fdf7782a198588621ae886529dc2f`、report blob `6781e3ed32d32814c07df0b2acb39e13506612fe`。変更パスは `research/lines/fx-news-sentiment-v0.1/work/source-probe/assurance/2026-10-11/fixed-doc-authority/B_GDELT_FIXED_DOC_AUTHORITY_REVIEW.md` **1件のみ**。実報告本文をexact refで直接読んだ。
- 既存設計[#94](https://github.com/Josh-Temple/systematic-trading-research/pull/94) head `f4b7614839de653cf3644d0c4f22bc694483afc4`、既存DOC判断[#89](https://github.com/Josh-Temple/systematic-trading-research/pull/89) head `2082303a098079fb4788bb7d3c81ae259c342123` と両reportの実本文を照合。A/Bの追加内容と歴史的判断を区別した。
- 過去のFXNS E [#103](https://github.com/Josh-Temple/systematic-trading-research/pull/103) head `dd31e48fcea7524eef929cac07fd568d446b1f4f`、報告blob `c32ae64555b768b4b248df57ae392ed2e2dd8d8b` は以前の#99統合の証拠で、今回のA/B受領とは異なる。
- 旧A[#99](https://github.com/Josh-Temple/systematic-trading-research/pull/99)は**すでに研究branchへmerge済み**。現行`event_ledger.py` blob `3faa396953c7cb951d32d1f3521ea303010e8598`、`test_event_ledger.py` blob `e4bf1a3c8ab6d47c86fb92483d71768e87ab3a05`を研究branch exact refで直接照合。旧独立B[#101](https://github.com/Josh-Temple/systematic-trading-research/pull/101)は旧#99 exact treeの **synthetic-only `PASS_SCOPED` / 独立ローカル再実行 `NOT_RERUN`**。今回のA/Bに対する新たなコード受入PASSには転用しない。

## 2. Aの受入：`DESIGN_REVIEWABLE / NOT_IMPLEMENTED / NOT_EXECUTED`

A #105は#94の三案（①二形式維持・曖昧IDの停止、②単一正本、③明示的な競合解決）を**選択せず**、T01–T16の合成受入oracleを具体化した。通常→blocked／逆順、並列書込、部分write、fsync/rename直前直後のcrash、再起動、旧二重記録のmigration/rollback、古いreader・cache、権限ある主体の全record＋digest整合書換えの負例を定義。これは新しい設計価値であり、**試験の実行ではない**（`NOT_EXECUTED / NOT_RERUN`）。

現在のwriterは通常`<event_id>.json`とblocked`<event_id>.blocked.json`に別々の`xb`で記録し、各ファイルの単独確認ではID全体の排他を保証しない。既存#99の修正は一つのpersisted JSON object内部の**重複member拒否**であり、同じIDの二形式間の競合ではない。canonical record SHA-256は不整合検知の助けになるが、整合する全record＋digestの特権的書換えから作成者・履歴を証明しない。電子署名、鍵保管、独立append-only監査、ACL、原子的更新は、今後の承認・実装・独立監査を要する。

**E判断**：`LEDGER_CONTRACT_HUMAN_DECISION_REQUIRED`。方式と旧記録の隔離・移行規則を人間が明示承認するまで、新仕様・移行・コードmergeを禁止する。#105自体はDraftの報告でありmergeしない。

## 3. Bの受入：新一次資料はあるが`SOURCE_QUALIFICATION_BLOCKED`

B #106の固定DOC契約に対する7条件判定は、(a)母集団・網羅性 `PARTIAL`、(b)`seendate`のimmutable first-seen `NOT_ESTABLISHED`、(c)as-of再現・遡及改訂 `NOT_ESTABLISHED`、(d)UTC端点/サーバ処理時刻 `PARTIAL`、(e)250上限/HTTP429/容量 `PARTIAL`、(f)08:00 JST以前の完全受領 `NOT_ESTABLISHED`、(g)raw保全と将来監査 `PARTIAL`。一次文書に保証のない条件は推定で補わない。

本Eは公式の[GDELT DOC 2.0 API Debuts!（2017-06-20）](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)と[Scaling GDELT For A New Era（2026-04-18）](https://blog.gdeltproject.org/scaling-gdelt-for-a-new-era-migrating-to-spanner-with-agentic-interactive-gemini/)をDOC live APIへのアクセスなしに別途確認した。2026年の提供元記事は、旧基盤の負荷に伴うAPI要求の選別・破棄が必要になっていた旨を説明している。**これは提供元レベルの運用上の反証**であり、この特定DOC endpointや保存済み429の原因、移行完了、個別のSLA、first-seen、as-of網羅性を保証・証明しない。旧#89の継続／中止／別途pre-freeze再設計の人間判断がなお必要。

**Bの閲覧範囲逸脱を独立記録**：#106が自主申告したとおり、metadata-only閲覧の想定範囲を越え、既存`offline_validation.json`全体（実headlineのtitle/URLを含む）を取得した。Bは値の分類・転記・利用を行っていないと申告する。本Eはこの記録を**clean compliance として受け入れず**、`RESTRICTED_METADATA_READ_DEVIATION_REPORTED / HUMAN_DISPOSITION_PENDING`として残す。本E自身はその実recordを開かず、再取得もしていない。原記録の削除・改変はしない。逸脱への扱いは独立した人的判断を要する。

**E判断**：`SOURCE_QUALIFICATION_BLOCKED / formal prospective cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN`。query、provider、24h window、`sort=dateasc`、`artlist`、`MAXRECORDS=250`、08:00 cutoffを変えない。HTTP429を解消した／時刻以前に取得した／網羅性を証明した、とは扱わない。

## 4. 別系統のCSMを混同しない

- CSM候補[#90](https://github.com/Josh-Temple/systematic-trading-research/pull/90) OPEN/Draft、HEAD `94e7719839dcacf281d7d479c597222582f0d920`、tree `32e851594810e51a3aefd05ca7cdc17af341885d`。
- 前C[#100](https://github.com/Josh-Temple/systematic-trading-research/pull/100) の実report blob `77ae8da0da43078b12c45e0359ae4ba6f326ffa4`：完全exact checkoutとruntime-local metadata実bytesの確認不成立につき `BLOCKED_ENVIRONMENT / NOT_EXECUTED`、`testsRun=0`、failure/error/skip `NOT_OBSERVED`。62テスト定義は試験成功ではない。
- 前D[#102](https://github.com/Josh-Temple/systematic-trading-research/pull/102) の実report blob `7a4a1a124047396557c907419a43b5a92fb31399`：#100後の独立確認は `BLOCKED / NOT_RERUN / HOLD_NO_MERGE`。2026-10-11の新C実行receipt、新D実行receiptは今回のPR検索で確認されていない。`NO_NEW_C_EXECUTION / D_NOT_STARTED`、同じ内容のE再発行なし。
- 前E[#104](https://github.com/Josh-Temple/systematic-trading-research/pull/104) をCSMの既存HOLDとして維持。現在のCSM I2 [#37](https://github.com/Josh-Temple/systematic-trading-research/pull/37) HEAD `9162cae4f2e64ee3da07517f12a16092cc170161` にある実 `work/integration/gate.json`（`research/lines/currency-strength-momentum-v0.1/`配下）Git blob `19442215345b35b0db3910c01acd910a5d57889b`は `state=BLOCKED`、`gate_status=CLOSED`、`market_outcome_access=false`。**CSM E-only新PRは作らない**。

## 5. 旧CIと今回の非実行、Eの終端条件

- 既存FXNS #99のActions [run 38006886615](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/38006886615) / job `114077610920`は本Eがdecoded job logを直接読んだ。checkoutは旧#99のPR merge ref `14f0580c647dfecb7059c125441b06f5759d3833`、Python 3.13.16、**96 tests / failures=0 / errors=0 / skipped=0**、compile success。旧B #101の同一tree検証は過去の独立監査証拠。本EがCIを再実行したわけではない。今回の#105/#106は報告だけで新テスト・CIなし、A T01–T16は未実行。
- 新たなコード候補、独立Bコード監査、承認済台帳契約はないため、このWaveの**FXNS code mergeなし**。過去#99を二度mergeしない。source/prospective cohort/CSM I2/outcome/XM/market history/実分類/注文/取引はいずれも解除しない。
- **人間が決める次の事項**：①同一IDの三案・既存二重記録の移行と隔離・真正性/保管責任、②固定DOCに必要なDOC固有の真正な保証取得の可能性と継続/停止/別途承認するpre-freeze再設計、③B閲覧境界逸脱の処理、④CSM exact #90完全Git checkoutと隔離Python 3.12+・metadata実ファイルを安全に供給する所有者の特定。
- CSM再開は供給者が完全な正規Git treeとruntime-local三metadata SHAを証明し、Cが**実際に**`py_compile`と`unittest -v`を実行して正確な結果を別reportで保存し、その後Dが別Chat・別branchで監査したときのみ。成功してもsyntheticだけでI2は開かない。

**書込・readback契約**：EはFXNS側の**この1 report**だけを最新研究branchから派生した独立branchへ作成する。PRはOPEN/Draftに保ち、mergeしない。report commit・tree・report blob・全changed paths・base/headを保存後に独立に読み戻してGitHub PR本文に追記する（Git commit SHAを同一commitのfile本文内に自己埋込みすることはできない）。本reportが証明する範囲は2026-10-11 JST時点に再取得した証拠に限る。
