# E — CSM 2026-10-10 Wave 署名者分離・保留記録

確認日: 2026-10-09 JST（計画日2026-10-10を実行・承認日とみなさない）
判定: **HOLD_NO_MERGE / IMPLEMENTED_NOT_RUNTIME_VERIFIED**。CSM gateはBLOCKED / CLOSED / market_outcome_access=falseを維持。
CSM I2 branch work/csm-integration-20261001: 9162cae4f2e64ee3da07517f12a16092cc170161。main: 33f3c1e5c9d4dca323618e7ac1fcadc85a338fa3。

## 1. C候補のGitHub直接確認
- C PR #90 (OPEN/DRAFT) HEAD 94e7719839dcacf281d7d479c597222582f0d920、tree 32e851594810e51a3aefd05ca7cdc17af341885d。baseは実装 #34 work/csm-implementation-20261001 HEAD 3695f0a8ed085669ec3644826889f9fc953a6808。
- C changed paths全3件はallowlist内: research/lines/currency-strength-momentum-v0.1/work/implementation/csm.py (blob cc3b788d637d0bacf63d9642788a196a1feaac56)、test_csm.py (9e0ce5025d986f2e6f6e8c4487e4e0671dd67282)、2026-10-10/C_SIGNER_INDEPENDENCE_RESULT.md (cd11e9829adffd1556ae969421947fd622415d78)。報告書の実bytesをreadback。
- Cは既存production-path validate_gate_receiptで、個別RSA署名の成功に加えて同じkey ID・trusted principal・RSA modulusのE/Iを拒否する変更、異なる架空RSA鍵の正常fixtureと6つの新たな否定/正常methodを報告。署名アルゴリズムや実gate/sourceは変えない。
- **重要な不足**: Cのpy_compileとpython3 -m unittest -v test_csm.pyはNOT_EXECUTED。新候補のGitHub ActionsもNOT_RERUN。62件はテスト定義の静的数であり実行成功数ではない。架空RSA鍵の単独算術smoke checkは本番csm.pyを直接呼んだテストではない。Eは実装のfunctional PASSを宣言しない。
- 旧#83のtoy verifier 23/23 local PASS、旧#38の56/56はそれぞれ別コード・別HEAD。新しいC candidateの試験結果に転用しない。

## 2. Gate/source/securityの直接確認と未充足
- CSM I2 PR #37、過去の監査 #76/#80/#86、metadata source #53 と監査 #78、D toy #83をGitHub PR/changed pathsで照合した。
- work/integration/gate.jsonをI2 HEADで直接取得。blob 19442215345b35b0db3910c01acd910a5d57889b。state=BLOCKED、gate_status=CLOSED、market_outcome_access=false。I2は解禁しない。
- #53/#78はmetadata-onlyで、H placeholder日付、ZIP member inner bytes、history vintage、外部calendar authority、完全性とsource currentnessは未解決。
- 実在署名者E/Iの別人性と実鍵custody、root-owned trust store、trusted keyの期限・失効、署名HEAD鮮度、OS/ACL拒否試験、tamper-evident durable append-only attempt ledger、restart/readback、独立E current-I判断、named X operator、incident exposure人間判断、別途の明示的人間承認はいずれも証拠不成立。toy署名の形式的整合で補えない。

## 3. E処置と最小次工程
- **マージなし**: #90、#34、#37、#53、gate.json、source-lock、runner、workflow、mainに変更を加えず、#90はDraft維持。I2 BLOCKED / CLOSED。HYP-CSM-002 UNTESTED。
- 安全な隔離checkoutで#90 exact HEADのコード/fixture/treeを固定した完全offline direct production-path試験を別工程で実施することが最小次工程。python3 -m py_compile csm.py test_csm.pyおよびpython3 -m unittest -v test_csm.py のPython version、run/fail/error/skip、正常・敵対fixtureとreadbackが必要。EはC未完を代行PASSしない。
- csm-source-readiness.ymlは実ECB history取得経路の可能性があるため編集・実行していない。真の鍵保管、OS権限、実source、保護ledger、独立E、人間承認はこの実行が成功しても別ゲート。
- XM/MT5、ECB実観測値、実市場outcome、方向・return・P/L・勝率・取引・orders・H3/Pilot処理は行わず、market_outcome_access=falseを保つ。

## 4. E自身の実行区分・保存境界
E直接実行: GitHubのrefs/PR/changed paths/C report blob/gate.jsonの読込とHOLD判定。他担当の既存toy 23、旧56、C鍵算術smokeは引用に限定。今回C新実装のpytest/unittest・source HTTP・Actions・実鍵/OS・マージ・人的承認は未実施。
この新Draft PRにはresearch/lines/currency-strength-momentum-v0.1/work/integration/2026-10-10/next-wave/E_CSM_HOLD_RECEIPT.mdのみ。I2ブランチ、コード、source、SPEC、raw、workflow、gate、shared CURRENTを不変更。