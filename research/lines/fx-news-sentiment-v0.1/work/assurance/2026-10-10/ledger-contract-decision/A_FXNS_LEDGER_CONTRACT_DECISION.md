# A — FXNS同一event IDのcross-file契約と真正性境界：人間向け設計判断資料

- Wave指示書：Library `/Systematic Trading Research/Work Instructions/2026-10-10_fxns_exacthead_audit_csm_offline_validation_and_gate_closure_wave_instructions.md`、Section A。
- 対象repo：`Josh-Temple/systematic-trading-research`。**調査と提案のみ。コード・仕様・ゲートは一切変更しない。**
- 本資料は2026-10-10（JST）の確認事項を記載する。計画日を試験日・承認日とみなさない。
- 直接確認：GitHubのPR状態、exact-refのGit blob・writer/reader・test実内容、研究branch HEAD。**合成suiteを本Aが独立実行したわけではない（NOT_RERUN）**。#88のCI実績は別担当の報告であり、本Aの実行実績には算入しない。

## 1. 監査対象の正確な状態

| 項目 | 確認した状態 |
| --- | --- |
| FXNS研究branch / #63 | `research/fx-news-sentiment-v0.1` = `b1b31e5f1344c86c816f934a695a8583eb1bf4eb`、未統合の研究用branch |
| FXNS正候補 #88 | OPEN / Draft / 未マージ、HEAD `ecabf673e923fccb202cc22d2e4a39291e74a2ee`、tree `3fa284e10741617e23b4bb49511b58c1b15596f7` |
| #88 code blob | `research/lines/fx-news-sentiment-v0.1/work/implementation/event_ledger.py` = `87ce391ddf53a0f3f792eb7d4859de6733118ea4` |
| #88 test blob | `research/lines/fx-news-sentiment-v0.1/work/implementation/test_event_ledger.py` = `1e6ca255299152071915ecb5d80d8f8320c1788d` |
| 旧候補 #87 | HEAD `46c33885d908e7a4719b5d0bce6b85583ef302d1`、別候補・未マージ。#88の結果と混同しない |
| 前回E #91 | HEAD `fb0c25e066d1c241ced552352bf538508f19b707`、report-only Draft、`HOLD_NO_MERGE` |

#88の全PR変更パスは次の3つ：`work/implementation/event_ledger.py`、`work/implementation/test_event_ledger.py`、`work/implementation/2026-10-10/A_FXNS_OUTER_ENVELOPE_RESULT.md`（すべて`research/lines/fx-news-sentiment-v0.1/`配下）。本Aはそのコードを参照しただけである。

## 2. 現在の挙動と証拠（静的コード確認＋既存fixture）

**確認事実：** `write_synthetic_event` は `<event_id>.json` を、`write_blocked_receipt` は `<event_id>.blocked.json` を、それぞれ `file.open("xb")` で生成する。両者は同じディレクトリの別パスに書き込み、**他方の存在確認・イベントID単位の原子的な排他判定を行わない**。既にある同一パスは `FileExistsError` となるが、異なる拡張子間では競合が起こらない。

- #88実コード：[event_ledger.py](https://github.com/Josh-Temple/systematic-trading-research/blob/ecabf673e923fccb202cc22d2e4a39291e74a2ee/research/lines/fx-news-sentiment-v0.1/work/implementation/event_ledger.py)、主に350–389行。正常記録の書込後は同一bytesの即時readbackがある。blocked receipt側はflush/fsyncするが、同等の書込後readbackはない。
- `verify_synthetic_event(file)`（同392–422行）は**与えられた1ファイル**の末尾改行、outer `{record,record_sha256}`、digest、strict nested recordを検証する。イベントIDに対応する**別拡張子のファイルを列挙・照合しない**。したがって個々のファイルが妥当でも、同一IDの意味的競合は解消しない。
- #88既存合成テスト `test_same_event_id_normal_and_blocked_files_coexist_design_hold`（[test_event_ledger.py](https://github.com/Josh-Temple/systematic-trading-research/blob/ecabf673e923fccb202cc22d2e4a39291e74a2ee/research/lines/fx-news-sentiment-v0.1/work/implementation/test_event_ledger.py)、399–416行）は、同一IDについて正常 `.json` と `.blocked.json` の**両方の生成と個別verify成功**を検査する。通常記録は合成 `LONG_EURJPY`、blocked記録の`decision`は`None`。各パスへの二重書込は例外になることも検査する。
- 旧候補 #87の `test_cross_file_same_event_id_is_unresolved_design_boundary`（375行付近）も別候補で同種の現象を検証するが、**今回の監査対象は#88**であり、#87の実績を転用しない。
- **証拠種別：** 上記は本Aによるコード・fixtureの直接静的確認。#88のPR本文が報告するGitHub Actions run `37935320699` / job `113835792703`（94/94、fail/error/skip=0）は別担当によるCI確認情報。本AはCIを再実行していない。Bのexact-head独立監査は別成果として必要。

**解釈：** 通常記録とblocked receiptは異なる意味を持つ。どちらか1つを後工程が恣意的に採用すると、「正常な判断」と「同じIDの実行拒否」が矛盾して存在する事実を見落とす可能性がある。ただし現在formal cohortはCLOSEDであり、実シグナルや市場outcomeが通っていると主張しない。

## 3. 人間に提示する未承認の3案

| 選択肢 | 意味・後工程の扱い | 互換性、再起動・競合時readback | 原子的書込・障害時の要点 | 移行・テスト負担 |
| --- | --- | --- | --- | --- |
| **① 2ファイル許容＋曖昧IDはfail-closed** | 現行ファイル名を保持。両方存在すれば「競合」として後工程を停止、いずれも優先しない。**検出・停止の契約自体は未実装** | 既存ファイルとの互換性が高い。再起動時にもID単位で2パスを列挙し、競合を再判定する必要 | 個々の`xb`を維持できるが、書込直後・再読込時・並行実行時に他方の存在を見逃さず検出する仕組みが必要。単なる先行存在確認はraceを解消しない | 低～中。reader/consumer側の競合停止、障害注入、並行書込、再起動の追加テストが必要 |
| **② 同一IDにつき単一の正本レコード** | 正常／blockedを単一のIDキーと状態で表す。先に記録された状態を固定するのか、明示的状態遷移を許すのか人間が別途決定 | 既存`.json`/`.blocked.json`の意味的統合・移行規則が必要。両方ある履歴を黙って片方へ寄せない | 単一IDの排他・原子的作成／更新、部分書込の検知と復旧、ディレクトリ永続化・再起動readbackを設計する。単純な`xb`導入だけでは状態遷移は定まらない | 高。新形式、既存競合の隔離・移行、同時書込、クラッシュ後照合、readbackを試験 |
| **③ 2ファイル＋明示的な優先順位／競合状態** | 双方の存続を認めた上で、権威ある状態（例：`CONFLICT`）または優先規則を契約化。規則は未選択であり、blocked優先などを暗黙に採用しない | 既存ファイルを残しやすい反面、過去データへの規則適用・監査可能な履歴と識別子の扱いが必要 | 記録作成と競合インデックス更新間の不整合、race、クラッシュ時の再構築、再起動後の再判定を設計 | 中～高。優先・競合状態の全組合せ、再起動、履歴移行、複数consumerでの一致試験 |

**暫定的な安全要件（承認前の提案）：** どの案でも、仕様決定・実装・否定試験・readback検証が終わるまでは、両ファイルの存在を発見した後工程が**恣意的に1件を採用しない**こと。現行コードが自動的にこの要件を満たすという意味ではない。

## 4. SHA-256の真正性境界（別の問題として切り分け）

#88のouter検証は、想定外のkeyや不正なhash等の不整合を拒否する。しかし**特権を持つ攻撃者が妥当なsynthetic record全体を書き換え、対応する`record_sha256`を再計算できるなら、この検証だけでは元データの作成主体も変更履歴も証明できない**。nested validatorを満たす整合的な置換は、hash一致という条件では検知できない。

- 記録の**整合性検査**と、独立に証明される**署名者の認証／権限**は異なる。
- 電子署名・鍵の独立管理、改変耐性のあるprotected append-only ledger、信頼された実行環境やOSアクセス制御はいずれも**将来の別設計・別監査事項**。採用・実装・運用保証を本資料では主張しない。
- `xb`・process内fsync・即時readbackは、権限ある別主体によるファイル置換を防ぐ証明でも、永続保存・障害復旧・第三者監査の十分条件でもない。

## 5. 人間への一問・次の承認境界

**質問：** 将来のformal cohort移行前に、同一event IDに関するcross-file排他・競合判定を仕様化することを承認するか。承認する場合、①2ファイル維持＋曖昧ID停止、②単一レコード契約、③2ファイル＋明示的優先／競合状態、のどれを採り、既存の競合履歴をどう移行・隔離するか。

**現在の扱い：承認未取得／設計未決／実装修復なし。** ①を直近の安全策として検討することは可能だが、本Aは①〜③のいずれも採用決定しない。決定後に別の実装Wave、並行書込・障害復旧・readbackの合成negative tests、独立監査を設ける。真正性対策の要否・鍵や実行環境の信頼境界も別の人間判断が必要。

## 6. 今回の証拠と禁止事項の結論

- **本Aが直接実施：** GitHub PR #63/#87/#88/#91、研究branch current HEAD、#88 writer/readerとtestのblob確認、同一ID共存に関する静的コード・テスト読取、三案比較。
- **本Aでは未実施：** 合成test再実行（`NOT_RERUN`）、Actions job logの新規検証、コード／SPEC／consumer実装、実source取得・実分類・市場outcome照合・XM/MT5・取引。
- **別担当の証拠：** #88はoffline CI 94/94を報告しているが、独立Bが#88 exact HEADとjob logを監査しない限り、Eによる限定統合の承認根拠にはならない。
- **維持する境界：** `UNTESTED / PROPOSED_NOT_FROZEN`、formal cohort `CLOSED`、GDELT `SOURCE_QUALIFICATION_BLOCKED`、XM延期、市場outcomeアクセス禁止。`main`やFXNS研究branchへのマージ、#88/#87への書込、source/strategyの変更なし。

**A成果判定：設計判断資料の作成（report-only）。研究・実装ゲートのPASSや人間承認ではない。**
