# FXNS PR #119 — 独立D再受入（2026-10-13 JST）

**D_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE**

別Chatの独立D実測。既存77/77 PASS、compile PASS。独自16件は15 PASS / 1 FAIL / 0 ERROR / 0 SKIP。Aの実測をDの成功として流用していない。新規負例は既存の単一条件に対し、別の攻撃値・状態遷移・複合故障を投入した。N01/N09/N10等は負例と正常系保全を一緒に検証する。

## 固定identity

- 対象A HEAD: `dc8b0d310abba044c80506192117abf04c84a899`
- Tree: `3da3adaae35feb802576a888fee3140f35e3ecdb`
- Parent: `3e45c2a98ab030d3a9536b169154e9855493289c`
- PR base: `8f69bded3be746f9f6b6fd1011ea8676f5d32877`
- PR head branch: `work/fxns-pr117-eight-findings-a-20261012`
- PR base branch / D report base: `work/fxns-synthetic-boundary-remediation-20261012-a`
- GitHub metadataをモデル入力前に固定identity/pathだけへ限定。PR自由文、commit message、diff、CI/Actionsは読んでいない。6ファイルはbase64から原バイトを復元しGit blob計算と照合。treeエントリーも6ファイルに限定し全てmode 100644/type blob、サイズ一致。PR #119の差分はREADME/TEST_RECEIPT/safe_boundary/test_remediation/test_eight_findingsの許可5パス。

| File | bytes | Git blob | byte SHA-256 |
|---|---:|---|---|
| safe_boundary.py | 19375 | `c7eafacc6968f9d0a3aac17a6bbcb5a8acc24d8e` | `532db4ce21aa4a6c7633fc4da31f7c371302c690f1798a5778969fa43ceb2880` |
| test_safe_boundary.py | 8473 | `a3caa8bda1eccae0b7e8ed01ff40b6cc42fb27d3` | `7d60393dde7b7cfaac665604920c1e6c2cf89ef732b96e678c1a16ba6376c527` |
| test_remediation.py | 11788 | `e8e070ab74ade1a43d2856808ecaec089953fb7a` | `fe796702764637e18749c8a09cd02db8d6610cd4d6ffeada641e1317219be499` |
| test_eight_findings.py | 10425 | `e86d41c82ed6eb35d71c39bbc8becb27d0b1630e` | `ab4fd1ca6e0ddef495d579f1f1dae7007ad5c179a6903e9b9400d80afb0bc463` |
| README.md | 9000 | `326308931acfdb466661d4180ec41690fd03556e` | `8e05d10080a3a8fd1d474e689581c7cf97257a69fa11450612868402366f4abe` |
| TEST_RECEIPT.md | 23710 | `78c30300662c2e2066793b251b4a6c36ebc5f3a1` | `754b0e85f27e9a2707b21494536de1aef0e76076c9879245ecd08c443c867ae6` |

## A証拠との整合

ZIP SHA-256 `b72c8a96d5f14b85aab4466f24920a6b6ba153be6f5b877a715d61776c673600` を再計算して一致。4 Python bytesがGitHub取得bytesと一致。Aの4コマンド8ログの原バイトハッシュとexecution.jsonが一致。77 case名/結果はD実測と一致。remote TEST_RECEIPT.md全体を取得し原バイトhashを固定。A receiptは旧tested HEADを明示し、最終HEADでPython bytesが不変なので整合する。TEST_RECEIPTのbyte差は承認済み追補に由来する。Dのログhashは独立生成であり、実行時間等によりA stderr hashとの一致を要求しない。

## 実行環境と境界

Python `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]`。OS `Linux-6.18.44-x86_64-with-glibc2.39`。working directory `/workspace/scratch/ca41ca8f1437/d_audit`。標準ライブラリと固定local moduleのみ。静的に全4ファイルを確認しnetwork API、subprocess、実データ、秘密情報参照、動的外部依存を認めなかった。完全架空fixture、python -B / PYTHONDONTWRITEBYTECODE=1。compile生成のscratch __pycache__は削除済み。

`unshare -n -- true`はexit 1 / Operation not permitted。**NETWORK_OS_ISOLATION_NOT_VERIFIED**。ネットワークprobe未実施。この不足を隔離成功へ昇格しない。実host全経路遮断、実モデル配送ACK、真のdurable receipt、分散exactly-once、独立excerpt custody、安全な実source取得は未実証。実ニュース、市場値、broker、model ingress、研究gate、main、#119/#117/#110の書換え、merge、取引は未実施。

## コマンドと原ログhash

| Invocation | exit | cases | stdout SHA-256 | stderr SHA-256 |
|---|---:|---:|---|---|
| `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_safe_boundary` | 0 | 22 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `0d2a585758dd080c4af19301fa272fe599e70f497bb503c1e9efc39f17715f1c` |
| `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_remediation` | 0 | 26 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `4bc21da8a101834fe5edf3ed6147ee1c12c43fcead610dfecf34db50a4b3a2bb` |
| `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_eight_findings` | 0 | 29 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `7e164771e79aa1fd1f77241cd19fab55b6c8ca379a0a0816da712e5a3dbc455c` |
| `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m py_compile safe_boundary.py test_safe_boundary.py test_remediation.py test_eight_findings.py` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_independent_d` | 1 | 16 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `85d708444483755fb682be68f7c1dfec3640536f328403fdb60c614736973a1f` |

## 独自負例16件

| ID | 入力条件・期待・観測 | 結果 |
|---|---|---|
| N01 | 3ページ目の重複拒否、正当な2 identity再試行許可 | PASS |
| N02 | 非文字列request ID拒否 | PASS |
| N03 | bool ACK index拒否、UNKNOWN、再送拒否 | PASS |
| N04 | 非文字列の偽造audit値拒否を期待。実際は配送1件・RELEASED・非None返却 | FAIL |
| N05 | audit履歴消去と成功返却を拒否 | PASS |
| N06 | RESERVED append後例外で配送ゼロ、再試行もゼロ | PASS |
| N07 | RELEASED append後例外でUNKNOWN、再送拒否 | PASS |
| N08 | 5者競合・ACK不一致で配送1件、全呼出し非成功 | PASS |
| N09 | UNKNOWN requestを再送拒否、別operation/requestは正当に配送 | PASS |
| N10 | RESERVED中入力改変でも検証済み出力は変化なし | PASS |
| N11 | UNKNOWN後Boundary再初期化・5再送を拒否 | PASS |
| N12 | blob/mode/tree複合不一致を拒否、清浄再試行成功 | PASS |
| N13 | 3ページcursor不連続とHEAD漂移を拒否 | PASS |
| N14 | generator部分streamを走査せず拒否 | PASS |
| N15 | 未知page schema拒否後、清浄再試行1回のみ成功 | PASS |
| N16 | 非文字列ACK hash拒否、UNKNOWN、再送拒否 | PASS |

## 欠陥と再現

N04: `Boundary._audit`はdictの型と`after[-1] == expected`を確認するが、receipt値が正確なstr型かを確認しない。任意の文字列に`__eq__`がTrueを返す非文字列を4値へ入れるReceiptSink subclassで偽造監査が受理される。`run`は非Noneを返し、配送1件、registry RELEASEDとなる。期待は非成功、配送ゼロ。既存D05/A17等のno-op拒否では捕捉されない。これは合成adapter故障に対する局所的な欠陥であり、実hostでの悪用可能性を実証していない。

修正候補: audit entryを正確な許可key集合と全値のtype strで確認し、比較前に非文字列を拒否する。既存履歴にも同じ型検証を適用する。新しい修正の実装・作者再実測・別Chat独立再受入が必要。Dはコード修正もテスト期待緩和も行っていない。

再現: 下記独立fixtureを同一4 Python bytesの隣に保存し、`PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_independent_d.IndependentD.test_N04_forged_audit_value_nonstring_equality`。exit 1のFAILとなる。全16件コマンドは上表。各caseの入力を含む完全な再現コードを末尾に保持。

## Eへの引渡しと人的判断

- A作者77 PASSの整合は確認。D既存77 PASSとcompile PASSは独立実測。
- D新規16件: 15 PASS / 1 FAIL。D受入は不合格。EはLOCAL_SYNTHETIC_PASS_SCOPEDへ繰上げ不可。
- 最終 `D_NEEDS_REVISION / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`。
- 必要な次工程はN04修正候補の承認範囲確定と、作者回帰・独立再受入。実host/source/CSM/取引の承認は別事項。本DはE統合判定を行わない。
- GitHub保存は新実測が成立したためD専用report-only Draft PR 1件1ファイル。合格が保存条件ではない。remote保存のcommit/tree/parent/blob、全文byte一致、1変更path、元PR・共有branchの非干渉は保存後のreadback receiptを参照する。確認不能ならNOT_VERIFIEDを保持する。

## 全77個別結果

- `test_T01_out_of_scope_pr`: PASS
- `test_T02_forbidden_pr_fields`: PASS
- `test_T03_doc_new_version_requires_approval`: PASS
- `test_T04_search_snippet_is_forbidden`: PASS
- `test_T05_second_page_not_released_early`: PASS
- `test_T06_post_delivery_redaction_is_not_prevention`: PASS
- `test_T07_upstream_exception_never_echoed`: PASS
- `test_T08_raw_evidence_cannot_be_written_to_public_receipt`: PASS
- `test_T09_nested_encoded_unexpected_field`: PASS
- `test_T10_unexpected_free_text_inside_known_field`: PASS
- `test_T11_document_hash_mismatch_same_ref`: PASS
- `test_T12_head_drifts_during_page_walk`: PASS
- `test_T13_truncation_or_cursor_loop`: PASS
- `test_T14_unapproved_redirect_source`: PASS
- `test_T15_multimodal_or_preview_payload`: PASS
- `test_T16_graphql_partial_with_error`: PASS
- `test_T17_unvalidated_cache_read_not_allowed`: PASS
- `test_T18_streamed_unvalidated_first_chunk`: PASS
- `test_T19_direct_connector_bypass_not_supported`: PASS
- `test_T20_prompt_injection_cannot_change_policy`: PASS
- `test_T21_audit_failure_prevents_release`: PASS
- `test_T22_approved_metadata_and_excerpt_exactly_once`: PASS
- `test_A01_three_concurrent`: PASS
- `test_A02_same_request_different_operation`: PASS
- `test_A03_different_document_same_operation`: PASS
- `test_A04_distinct_trusted_request_ids`: PASS
- `test_A05_delayed_ack_no_concurrent_duplicate`: PASS
- `test_A06_before_publish_failure`: PASS
- `test_A07_after_publish_failure_and_retry`: PASS
- `test_A08_audit_failure_after_publish`: PASS
- `test_A09_registry_unknown_disclosed_no_global_guarantee`: PASS
- `test_A10_deep_mutable_policy_reference`: PASS
- `test_A11_path_blob_and_extra_mode_tree`: PASS
- `test_A12_large_partial_stream_type_mix`: PASS
- `test_R01_race_same_sink_same_op`: PASS
- `test_R02_partial_publish_unknown_no_retry`: PASS
- `test_R03_pre_publish_error_no_false_released`: PASS
- `test_R04_approval_mapping_mutation_rejected`: PASS
- `test_R05_new_boundary_same_sink_cannot_duplicate`: PASS
- `test_R06_unapproved_request_id`: PASS
- `test_R07_nested_state_type`: PASS
- `test_R08_late_page_unapproved`: PASS
- `test_R09_cursor_loop`: PASS
- `test_R10_large_fictional_document`: PASS
- `test_R11_trusted_approval_input_required`: PASS
- `test_R12_policy_id_reject_free_text`: PASS
- `test_R13_logical_metadata_contradiction`: PASS
- `test_R14_expected_blob_pair_mismatch`: PASS
- `test_A13_distinct_approved_file_paths`: PASS
- `test_A14_unduplicated_single_metadata`: PASS
- `test_A15_valid_sink_ack_exact`: PASS
- `test_A16_delivery_recorded_ack_missing`: PASS
- `test_A17_release_audit_noop_after_publish`: PASS
- `test_A18_unicode_path_policy_rejected`: PASS
- `test_A19_foreign_object_envelope_repo_rejected`: PASS
- `test_A20_noop_publish_explicit_fake_ack`: PASS
- `test_D01_duplicate_file_identity_across_pages`: PASS
- `test_D02_duplicate_file_identity_same_page`: PASS
- `test_D03_duplicate_metadata_identity`: PASS
- `test_D04_noop_publish_no_ack`: PASS
- `test_D05_noop_audit_return`: PASS
- `test_D06_equal_but_nonstring_head_repo`: PASS
- `test_D07_equal_but_nonstring_base_repo`: PASS
- `test_D08_equal_but_nonstring_post_head`: PASS
- `test_D09_cursor_object_rejected`: PASS
- `test_D10_boolean_pr_number_rejected`: PASS
- `test_D11_bool_or_nonstring_blob_rejected`: PASS
- `test_D12_mutating_input_mapping_does_not_rewrite_approval`: PASS
- `test_D13_bytearray_body_rejected`: PASS
- `test_D14_unsafe_request_id_rejected`: PASS
- `test_D15_audit_failure_no_retry_after_publish`: PASS
- `test_D16_valid_closed_unmerged_metadata`: PASS
- `test_D17_merged_and_draft_inconsistent`: PASS
- `test_D18_unknown_nested_field_rejected`: PASS
- `test_D19_shared_registry_no_duplicate`: PASS
- `test_D20_fabricated_approval_not_independent_custody`: PASS
- `test_D21_separate_sinks_not_exactly_once`: PASS

## 独立fixture完全コード

```python
"""Independent D: fictional compound fault injections; no network or real data."""
import unittest, copy, json
from dataclasses import replace
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from safe_boundary import Boundary, DeliverySink, ReceiptSink, DeliveryAck
from test_safe_boundary import fixture, request, metadata, paths, document, page, PATH

class IndependentD(unittest.TestCase):
 def deny(self,b,s,q,x):
  self.assertIsNone(b.run(q,x));self.assertEqual(s.delivered,[])
 def test_N01_three_page_duplicate_after_distinct_identity(self):
  b,s,r=fixture();other='approved/other.txt';p=replace(b.policy,allowed_paths=frozenset({PATH,other}),expected_blob_oids={PATH:'c'*40,other:'d'*40});b=Boundary(p,s,r);x=paths();a=x['pages'][0]['items'][0];x['pages']=[page([a],next_cursor='x'),page([{'path':other,'blob_oid':'d'*40}],cursor='x',next_cursor='y'),page([dict(a)],cursor='y')];self.deny(b,s,request('FILE_PATHS'),x)
  x['pages'].pop();x['pages'][-1]['next_cursor']=None;self.assertIsNotNone(b.run(request('FILE_PATHS'),x))
 def test_N02_equal_nonstring_request_id_with_valid_response(self):
  class Equal:
   def __eq__(self,x):return True
   def __hash__(self):return 1
  b,s,r=fixture();q=request();q['approved_request_id']=Equal();self.deny(b,s,q,metadata())
 def test_N03_boolean_ack_index_matches_zero(self):
  class Forged(DeliverySink):
   def publish(self,c):super().publish(c);return DeliveryAck(False,sha256(c).hexdigest())
  b,_,r=fixture();s=Forged();b=Boundary(b.policy,s,r);self.assertIsNone(b.run(request(),metadata()));self.assertEqual(list(s._operations.values()),['UNKNOWN']);self.assertIsNone(b.run(request(),metadata()));self.assertEqual(len(s.delivered),1)
 def test_N04_forged_audit_value_nonstring_equality(self):
  class Equal:
   def __eq__(self,x):return True
  class Forged(ReceiptSink):
   def append(self,**kw):self.receipts.append({k:Equal() for k in kw})
  b,s,_=fixture();b=Boundary(b.policy,s,Forged());self.deny(b,s,request(),metadata())
 def test_N05_success_return_erases_audit_history(self):
  class Erase(ReceiptSink):
   def append(self,**kw):self.receipts[:]=[kw];return True
  b,s,_=fixture();r=Erase(receipts=[dict(state='BLOCKED',reason='BAD_TARGET',policy_id=b.policy.policy_id,operation='PR_METADATA')]);b=Boundary(b.policy,s,r);self.deny(b,s,request(),metadata())
 def test_N06_reservation_append_then_exception_retry(self):
  class Fault(ReceiptSink):
   def append(self,**kw):super().append(**kw);raise RuntimeError('fictional-after-append')
  b,s,_=fixture();b=Boundary(b.policy,s,Fault());self.deny(b,s,request(),metadata());self.deny(b,s,request(),metadata())
 def test_N07_release_append_then_exception_no_retry(self):
  class Fault(ReceiptSink):
   def append(self,**kw):super().append(**kw);\
    (_ for _ in ()).throw(RuntimeError('fictional')) if kw['state']=='RELEASED' else None
  b,s,_=fixture();b=Boundary(b.policy,s,Fault());self.assertIsNone(b.run(request(),metadata()));self.assertIsNone(b.run(request(),metadata()));self.assertEqual(len(s.delivered),1);self.assertEqual(list(s._operations.values()),['UNKNOWN'])
 def test_N08_five_contenders_lost_ack(self):
  class Lost(DeliverySink):
   def publish(self,c):super().publish(c);return DeliveryAck(9,sha256(c).hexdigest())
  b,_,r=fixture();s=Lost();b=Boundary(b.policy,s,r);barrier=Barrier(5)
  def go(i):barrier.wait(timeout=5);return Boundary(b.policy,s,r).run(request(),metadata())
  with ThreadPoolExecutor(max_workers=5) as ex:outs=list(ex.map(go,range(5)))
  self.assertEqual(outs,[None]*5);self.assertEqual(len(s.delivered),1)
 def test_N09_unknown_one_request_allows_distinct_operation_and_request(self):
  class OnceLost(DeliverySink):
   def publish(self,c):a=super().publish(c);return None if len(self.delivered)==1 else a
  b,_,r=fixture();s=OnceLost();b=Boundary(b.policy,s,r);self.assertIsNone(b.run(request(),metadata()));self.assertIsNotNone(b.run(request('FILE_PATHS'),paths()));q=request();q['approved_request_id']='SYN-second';self.assertIsNotNone(b.run(q,metadata()));self.assertIsNone(b.run(request(),metadata()));self.assertEqual(len(s.delivered),3)
 def test_N10_input_mutation_during_reserve_does_not_change_delivery(self):
  x=metadata()
  class Mutate(ReceiptSink):
   def append(self,**kw):
    if kw['state']=='RESERVED':x['pages'][0]['items'][0]['state']='FICTIONAL_FORBIDDEN';x['pages'][0]['items'][0]['body']='FICTIONAL_MARKER'
    super().append(**kw)
  b,s,_=fixture();b=Boundary(b.policy,s,Mutate());out=b.run(request(),x);self.assertIsNotNone(out);self.assertNotIn(b'FICTIONAL',out);self.assertEqual(json.loads(out)['items'][0]['state'],'OPEN')
 def test_N11_registry_boundary_reinit_after_unknown_five_replays(self):
  class Noop(DeliverySink):
   def publish(self,c):return DeliveryAck(0,sha256(c).hexdigest())
  b,_,r=fixture();s=Noop();b=Boundary(b.policy,s,r);self.assertIsNone(b.run(request(),metadata()))
  for i in range(5):self.assertIsNone(Boundary(b.policy,s,ReceiptSink()).run(request(),metadata()))
  self.assertEqual(s.delivered,[]);self.assertEqual(list(s._operations.values()),['UNKNOWN'])
 def test_N12_blob_mode_tree_mismatch_then_clean_retry(self):
  b,s,r=fixture();x=paths();x['pages'][0]['items'][0].update(blob_oid='f'*40,mode='120000',tree_oid='e'*40);self.deny(b,s,request('FILE_PATHS'),x);self.assertIsNotNone(b.run(request('FILE_PATHS'),paths()))
 def test_N13_three_page_cursor_discontinuity_and_head_drift(self):
  b,s,r=fixture();x=paths();a=x['pages'][0]['items'];x['pages']=[page(a,next_cursor='x'),page([],cursor='wrong',next_cursor='y'),page([],cursor='y')];x['post_head_oid']='e'*40;self.deny(b,s,request('FILE_PATHS'),x);x['post_head_oid']=b.policy.head_oid;self.deny(b,s,request('FILE_PATHS'),x)
 def test_N14_generator_partial_stream_never_iterated(self):
  touched=[]
  def stream():touched.append(1);yield page()
  b,s,r=fixture();x=metadata();x['pages']=stream();self.deny(b,s,request(),x);self.assertEqual(touched,[])
 def test_N15_future_page_field_rejection_then_retry(self):
  b,s,r=fixture();x=metadata();x['pages'][0]['schema_version']=99;self.deny(b,s,request(),x);self.assertEqual(s._operations,{});self.assertIsNotNone(b.run(request(),metadata()));self.assertIsNone(b.run(request(),metadata()))
 def test_N16_forged_ack_hash_equal_nonstring(self):
  class Equal:
   def __eq__(self,x):return True
  class Forged(DeliverySink):
   def publish(self,c):super().publish(c);return DeliveryAck(0,Equal())
  b,_,r=fixture();s=Forged();b=Boundary(b.policy,s,r);self.assertIsNone(b.run(request(),metadata()));self.assertEqual(list(s._operations.values()),['UNKNOWN']);self.assertIsNone(b.run(request(),metadata()));self.assertEqual(len(s.delivered),1)

```
