# E — FXNS 2026-10-10 Wave 統合・保留記録

確認日: 2026-10-09 JST（計画日2026-10-10を実行・承認日とみなさない）
判定: **HOLD_NO_MERGE / B_EXACT_HEAD_AUDIT_MISSING**。Eは新しいコードをマージしていない。
研究branch research/fx-news-sentiment-v0.1: b1b31e5f1344c86c816f934a695a8583eb1bf4eb
main: 33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3

## 1. GitHubからの直接確認
- A最終候補 PR #88 (OPEN/DRAFT): HEAD ecabf673e923fccb202cc22d2e4a39291e74a2ee、tree 3fa284e10741617e23b4bb49511b58c1b15596f7。GitHub APIでPR、全変更パス、A報告書とblobを直接確認。
- A全変更3パスはallowlist内。work/implementation/event_ledger.py (blob 87ce391ddf53a0f3f792eb7d4859de6733118ea4)、test_event_ledger.py (1e6ca255299152071915ecb5d80d8f8320c1788d)、2026-10-10/A_FXNS_OUTER_ENVELOPE_RESULT.md (3b65e5583189f5191e8bae344a48287a36fec8bd)。いずれもresearch/lines/fx-news-sentiment-v0.1以下。
- A GitHub Actions run 37935320699、job 113835792703、head_sha ecabf673...、completed/success。decoded job logをEが直接確認。Python 3.13.16、FXNS_OFFLINE_RESULT: run=94; failures=0; errors=0; skipped=0; successful=True。syntax compile成功。**E自身によるPython再実行ではない**。
- CI checkoutのPR merge commit 5076559fbd57ef91b96dba42a1dafcb8f51429bf のtreeも3fa284e10741617e23b4bb49511b58c1b15596f7で、#88候補treeと一致。parentsは研究branch b1b31e5... とA候補 ecabf673...。
- .github/workflows/fxns-gdelt-source-probe.yml blob 620581df64cf247c293781389bd7386df391f30e を直接確認。PR paths triggerでsocket-denied offline driverとcompileallを使用。Eはworkflowを起動せず、OS全体のネットワーク遮断まで証明しない。
- A別候補 PR #87 (OPEN/DRAFT) HEAD 46c33885d908e7a4719b5d0bce6b85583ef302d1 は別SHA・別tree、旧93/93の候補。#88と混同・両方マージしない。
- **2026-10-10 Waveの独立B監査**: GitHub最新PR一覧（#90が最新）に、#88 exact HEAD ecabf673... に対する独立監査成果を確認できず。今回のB判定は NOT_AVAILABLE / NOT_VERIFIED。旧B PR #84 は旧A PR #82 (c8c2d3bb...) のPASS_SCOPEDであり、新候補には適用できない。

## 2. 実装上の限定成果と未決条件
Aのouter envelopeで正確なrecord/record_sha256二key、辞書型、小文字64-hex digest、hash整合性、破損JSON、blocked偽装とnested record検証を合成試験したことはCIから確認。正常LONG/NO_TRADE/blockedを含む94件の実行結果はA scopedの証拠のみ。Bによる同一HEADの独立反証・変更差分確認がないため、Eの統合PASSにはしない。
同一event IDで通常.jsonと.blocked.jsonが別々に共存できる問題は仕様判断待ち。cross-fileの排他・優先順位は無断導入しない。特権者が整合したrecord全体とhashを差し替える攻撃に対する真正性・作成者認証、protected append-only ledgerも未保証。

## 3. Dの出典判断と既存の負の証拠
D PR #89 (OPEN/DRAFT) HEAD 2082303a098079fb4788bb7d3c81ae259c342123、変更はsource-probe/assurance/2026-10-10/decision/D_GDELT_DOC_CONTINUE_OR_STOP_DECISION.md 一件のみ（blob bd7d3ffa0c6abbda8e05b3252c737f0e63ea4fc7）。直接readbackした。
旧#75/#81の負証拠を維持。取得完了12:20:26 JSTは08:00 cutoff後、HTTP200 raw12→別offline replay retained10、429比較要求あり。DOCのfirst-seen、時点網羅性、UTC境界、index revisionの保証は未成立。Dの人間向け意思決定資料は承認ではなくSOURCE_QUALIFICATION_BLOCKEDのまま。

## 4. Eの判断と次の最小条件
- **マージなし**: A #88/#87、D #89、#63、#85、main、CSMには統合しない。#88をDraft保持。Bが不在のためHOLD。
- 将来#88最終exact HEADと同一treeのsafe offline CI、全changed paths、nested/outer悪意あるnegative fixturesを独立Bが監査し、同一HEADのPASS_SCOPEDを独立Draft PRへ保存・readbackして初めてE再監査を検討。HEAD/base変更時は再監査。B未了でEが代行PASSしない。
- 次の未決人間判断: (1) 同一event IDの跨ファイル競合の仕様改訂要否、(2) 固定GDELT DOC契約のfirst-seen/網羅性/改訂保証を権威ある証拠で取得できるか。無理なら正式cohort停止か明示的pre-freeze再設計の審議。いずれも今回は未承認。
- 研究状態: UNTESTED / PROPOSED_NOT_FROZEN / formal cohort CLOSED / SOURCE_QUALIFICATION_BLOCKED / XM延期。market_outcome_access=falseを維持。実市場価格、実ニュース分類、XM/MT5、ECB観測値、returns、P/L、orders、売買を取得・評価しない。

## 5. 実行と保存
Eが実行: GitHubのrefs/PR/changed paths/code blob/workflow/commit/tree/Actions job logの読込と本判定。Aの試験はログの観測でありE再実行なし。B監査・HTTP実ソース要求・OS試験・人間承認・コード統合は未実施。
この新Draft PRにはresearch/lines/fx-news-sentiment-v0.1/work/integration/2026-10-10/next-wave/E_FXNS_HOLD_RECEIPT.md のみを保存。main、研究branch、workflow、SPEC、PROMPT/SCHEMA、raw/manifest、shared CURRENT、gate、scheduled tasksには触れない。