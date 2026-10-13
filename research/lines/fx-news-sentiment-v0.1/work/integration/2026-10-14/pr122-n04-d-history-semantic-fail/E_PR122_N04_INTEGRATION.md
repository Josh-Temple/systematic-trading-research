# FXNS PR #122 — E統合判定・人的承認票（2026-10-14 JST）

**最終判定：`E_INTEGRATED_D_FAILURE / D_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`**

本ファイルは2026-10-13 WaveのE専用・報告のみの統合成果物である。Dの実測をEが再実行したことは意味しない。合成環境の不合格を、実host上の悪用可能性の証明とも扱わない。コード修正、CI、マージ、研究/CSMゲート操作は実施しない。

## 1. 正本と確認済みidentity

- Wave正本：ChatGPT Library `/Systematic Trading Research/Work Instructions/2026-10-13_fxns_pr122_n04_independent_reacceptance_evidence_custody_and_gate_preservation_wave_instructions.md`
- Repository：`Josh-Temple/systematic-trading-research`。
- PR #122：<https://github.com/Josh-Temple/systematic-trading-research/pull/122>。Draft/open/unmerged、HEAD `c078001c2facfbbe4187e6722af0eda17618533a`、base `dc8b0d310abba044c80506192117abf04c84a899`。変更pathは指定ディレクトリ中の `safe_boundary.py`、`test_eight_findings.py`、`TEST_RECEIPT.md` の3件のみと再照合した。
- Dの別Chat報告PR #123：<https://github.com/Josh-Temple/systematic-trading-research/pull/123>。Draft/open/unmerged、HEAD `e741c09a967d0a179be9adee80aeeb93868273a6`、報告のみの単一変更path `research/lines/fx-news-sentiment-v0.1/work/reports/2026-10-13_pr122_n04_independent_d_reacceptance.md`。当該報告のGit blob `699f7ec28c75c403e02cfcce76f7994db133e503` を固定refで取得し、Dによる失敗・制限事項と照合した。
- 旧E PR #121：<https://github.com/Josh-Temple/systematic-trading-research/pull/121>。HEAD `97175b111fd7c04a99d25bbe558d33472c6508cb`、前回のN04不合格と研究停止を確認した。
- 研究branch `research/fx-news-sentiment-v0.1` の実行時取得HEAD：`24ef9c37e6255126a957f38cfa7470cd150ed594`。本E報告専用branchはこの固定SHAから作成し、共有研究branchを書き換えない。

## 2. 別ゲートの統合

| 系列 | 根拠 | 判定・範囲 |
| --- | --- | --- |
| A 証拠保全 | Library `/Broad Trade Research/fxns_pr122_A_evidence_custody_verification_20261013.md`、作者ZIP `/Broad Trade Research/fxns_pr119_N04_author_remediation_20261013(1).zip` | **`A_EVIDENCE_CUSTODY_VERIFIED`**。作者ZIP 29,505 bytes、SHA-256 `3c2a0f541a454ab6b663892a48c68574cd2907997ff52e51fd5b0b9d1f56b094`、22 entries、CRC/manifest/ログhashと修正4 Python bytesのremote一致。作者81/81 PASSおよび旧D16/16作者再演は独立D件数に加算しない。 |
| B 実host境界 | 既存設計PR #118（H19/H20含むH01–H20）を限定確認 | **`NO_NEW_EVIDENCE / DESIGN_ONLY / PLATFORM_NOT_ENFORCED`**。新しい実hostでの原文遮断、真の配送ACK、耐障害durable append等の実測は本Eの確認範囲で得られなかった。Bの実host合格を主張しない。 |
| C CSM環境 | 既存設計PR #113、Wave指定の固定gate metadataに関する既存状態 | **`OWNER_NOT_ASSIGNED / BLOCKED_ENVIRONMENT / NOT_EXECUTED / NO_NEW_EVIDENCE`**（新たな独立C-0/C-1/C-2実測やOS隔離証拠の確認なし）。実市場結果を開いていない。 |
| D 独立再受入 | 別Chat D報告PR #123、固定HEADと報告path | 既存81/81 PASS、旧N01–N16 16/16 PASS、**D新規16件のうち12 PASS・4 FAIL**。**`D_NEEDS_REVISION`**。Python 3.13.5、compile PASS。 |
| 独立D証拠保全 | PR #123の報告・留保 | D自身はZIPを生成しローカル整合確認したと報告。ZIP SHA-256 `d3871329e50c55fd1481df2bdeb9f50cca4abaf5df78aec916f190fa981950b5`。**Library upload/readbackは `container_session_unavailable` により未達**。Eは全D実行ログの原バイトを独立再検収していない。 |

B/Cは「本Eの確認範囲で新規証拠が認められない」という判定であり、未取得の全外部システムに証拠が存在しないとの断定ではない。Dの4 FAILはGitHubに保存されたD本人の独立実測報告に基づく。Eが直接再実行した件数は0。

## 3. #121からの重要な新事実

前回E #121では、PR #119の既存77件がDで通過する一方、D独立の旧負例N04（audit値の非文字列偽装）が1件失敗した。PR #122はこの型検証不足に対する作者側修正候補で、作者81件PASSと旧D16件の作者再演PASSを報告した。

今回、新しい独立DはPR #122の固定バイトに対し既存81件と旧N01–N16のすべてを通した。しかし、重複しない新規16負例中、以下の4件で想定すべき拒否が成立しなかった。

- **P01**：履歴 `state` が列挙外の文字列。
- **P02**：履歴 `reason` が列挙外の文字列。
- **P03**：履歴 `operation` が列挙外の文字列。
- **P04**：履歴 `policy_id` が構文不正な文字列。

四者とも、偽造済み既存監査レコードを渡した合成試験で `Boundary.run(...)` が非Noneを返し、`delivered_count=1`、registry `RELEASED`、`RESERVED`・`RELEASED` 追加を観測したとDが報告した。期待は拒否・配送0・非RELEASED。個別4件だが同一欠陥群の可能性が高く、独立した4根本原因と数えない。

原因候補：`safe_boundary.py` の `Boundary._audit()` 内 `valid_entry()` が履歴の辞書/key集合/値型を検査しても、既存エントリの許容値集合（`_STATES`, `_REASONS`, `_OPS`）と `policy_id` 構文を十分検査していない。正常な新規追加の `ReceiptSink.append()` と履歴受入の意味検証が一致していない。これは実hostでの悪用成立を証明しないが、局所synthetic受入を不合格にする十分な根拠である。

最小再現（D報告由来）：既存監査履歴へ `{'state':'RELEASED_WITHOUT_AUDIT','reason':'OK','policy_id':b.policy.policy_id,'operation':'PR_METADATA'}` を注入した `ReceiptSink(receipts=[history])` を使って `Boundary(b.policy,s,r).run(request(),metadata())` を呼ぶと、期待される拒否に反して `RELEASED`。同様にreason/operation/policy_idも個別反証された。すべて架空fixtureである。

## 4. 実際の判定と欠けている証明

- **`D_NEEDS_REVISION`**：新規安全負例の4 FAIL。PR #122を安全合格扱いにしてはならない。
- **`D_EVIDENCE_LIBRARY_READBACK_NOT_ESTABLISHED`**：新D ZIPのLibrary保存が完了していない。Dの失敗報告そのものは固定report-only PRで保持されるが、全ログ原バイトに対するE独立再照合は未実施。
- **`NETWORK_OS_ISOLATION_NOT_VERIFIED`**：`unshare -n` EPERMやDNS失敗はOS強制のegress deny証明とみなさない。
- **`PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`**：実hostのpre-model原文遮断、真の配送ACK、故障下でのdurable custody、cross-process exactly-once、モデルingress、source科学性の合格は別未解決。
- 旧D16件が新コードでPASSしても新規P01–P04の不合格を相殺しない。Aの作者結果と独立D結果も相殺/合算しない。

## 5. 人的承認を要する次の作業（**本E実行による承認ではない**）

1. **P01–P04への限定コード修正承認**：必要ならPR #122固定HEAD `c078001c2facfbbe4187e6722af0eda17618533a` から**別の隔離作者branch**を用意し、許可範囲を既存 `synthetic-pre-model-gate` の安全境界・回帰テスト・receiptに限定する。履歴値の列挙/構文/適法なフィールド組合せを拒否優先で検証し、正常履歴・`UNKNOWN / NO_RETRY`・部分処理・競合等を壊さないこと。PR #122本体、共有branch、既存D/E PRを書き換えない。実host、実ソース、CI、マージを許可しない。
2. **新たな独立D再受入の承認**：修正版の固定SHA/全バイトを照合し、既存81件、旧N01–N16、今回P01–P16を改変せず再実行、さらに未重複の新規12件以上を独立実装・故障注入する。期待不合格1件でfail-closed。作者の再演はD受入へ加算しない。
3. **証拠custody修復の承認・手順確定**：今回Dの未保存ZIP（報告SHA-256あり）を、正しい原バイトが再取得可能なときだけLibraryに保存し、ZIP CRC/manifest/ログhashと読戻しを確認する。単なる再生成・同名ファイルやハッシュ不一致で代替しない。入手できなければ新規独立試験による証拠再確立が必要。
4. **実host境界は別承認**：H01–H20の強制、モデル入力前の遮断、実配送ACK、耐障害書込み・分散処理保証の所有者・実験環境・観測可能性・受入条件を別途具体化。現時点でhost試験実施を承認しない。
5. **CSMとsourceの独立判断**：CSM責任者、完全exact checkout、OS隔離、C-0/C-1/C-2、FXNS代替sourceの取得権限・科学的妥当性、#106/#108の人的処分は引き続き別承認。

## 6. 絶対に解除しない状態・非実行

- FXNS：`SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / PROPOSED_NOT_FROZEN / NO_QUALIFIED_ALTERNATIVE`。
- CSM I2：`BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED`。既知固定gate blob `19442215345b35b0db3910c01acd910a5d57889b` の変更なし（本Eによる原バイト再照合なし）。
- PR #106/#108の人的最終処分：`PENDING`。PR #110/#117/#119/#120/#121/#122/#123と本E報告PR：`HOLD_NO_MERGE`。
- 実source、GDELT、ニュース、FX/ECB市場値、broker/MT5/XM、live trading、pilot、モデルingress、研究再開、source freeze、CI/Actions起動は禁止。
- 本Eの変更は**新規報告ファイル1件のみ**。設計、コード、ゲート、設定の実装は行わない。
