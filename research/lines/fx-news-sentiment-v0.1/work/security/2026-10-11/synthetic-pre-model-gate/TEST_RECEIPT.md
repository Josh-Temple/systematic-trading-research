# A — PR #110 complete-fictional offline remediation local test receipt

**Author-side only. D independent verification NOT_EXECUTED. PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE.**

- User approval: 2026-10-12 current conversation, operation ① approved exactly within the previously stated isolated synthetic scope.
- Exact parent PR #110 commit: `0faf05b453c5d7897c3566d871591b2926ba928e`; tree: `380d646e017be68ef45f57c5889c78b52fe41605`. Original branch/PR unchanged.
- Execution environment: Python 3.13.5, standard-library only, local container, **no live connections or network API invoked**. `unshare -n` attempt returned EPERM; OS-level egress restriction **NOT_VERIFIED**, so do not describe this as verified host network isolation.
- No full repository checkout, pip, GitHub wire test, Work model input, CI/Actions dispatch, real source/FX/ECB/market data, host permission, merge, or gate modification.
- Original reference Git blobs: `safe_boundary.py cfa10e14af6780659f79cf25fc9cf743844ea4d1`, `test_safe_boundary.py 97fdb367d198426c1b5da4600ec1ea3f771e9ac2`, `README.md d9261c5716aae0e85fcdaced85d2d050e516d406`, `TEST_RECEIPT.md 1ccfbaa8d71a7a090014f041008580f16894d52a`.

## Code/test file identity before remote upload

- `safe_boundary.py`: 16205 bytes, SHA-256 `a53eea879fe9f98400da7f74e48e4397e6f9d961265318079a22383879006d13`
- `test_safe_boundary.py`: 8473 bytes, SHA-256 `7d60393dde7b7cfaac665604920c1e6c2cf89ef732b96e678c1a16ba6376c527`
- `test_remediation.py`: 11781 bytes, SHA-256 `22089587705952127958a59b70aa4b44128175baf47fa9cb62cd44d70bf0bb27`
- `README.md`: 5718 bytes, SHA-256 `ed91634458efa6a37d85be896eeb5bd08a021499782e622902d2aa7e597edf13`

## Actual author-side commands and receipts

Every test invocation used `PYTHONDONTWRITEBYTECODE=1` and `python -B`. The 14 R labels reproduce *specifications*, not unpublished #114 fixture bytes.

### T — 22 cases
- Command: `python -B -m unittest -v test_safe_boundary`
- Exit: `0`; passed `22`; failures 0, errors 0, skips 0.
- stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).
- stderr SHA-256 `13cd904eea72a0fcbabc2f05e57c7fc8e6d4182ebf1b9fd16bd7ed07a48298fd` (3043 bytes).

```text
test_T01_out_of_scope_pr (test_safe_boundary.BoundarySyntheticTests.test_T01_out_of_scope_pr) ... ok
test_T02_forbidden_pr_fields (test_safe_boundary.BoundarySyntheticTests.test_T02_forbidden_pr_fields) ... ok
test_T03_doc_new_version_requires_approval (test_safe_boundary.BoundarySyntheticTests.test_T03_doc_new_version_requires_approval) ... ok
test_T04_search_snippet_is_forbidden (test_safe_boundary.BoundarySyntheticTests.test_T04_search_snippet_is_forbidden) ... ok
test_T05_second_page_not_released_early (test_safe_boundary.BoundarySyntheticTests.test_T05_second_page_not_released_early) ... ok
test_T06_post_delivery_redaction_is_not_prevention (test_safe_boundary.BoundarySyntheticTests.test_T06_post_delivery_redaction_is_not_prevention) ... ok
test_T07_upstream_exception_never_echoed (test_safe_boundary.BoundarySyntheticTests.test_T07_upstream_exception_never_echoed) ... ok
test_T08_raw_evidence_cannot_be_written_to_public_receipt (test_safe_boundary.BoundarySyntheticTests.test_T08_raw_evidence_cannot_be_written_to_public_receipt) ... ok
test_T09_nested_encoded_unexpected_field (test_safe_boundary.BoundarySyntheticTests.test_T09_nested_encoded_unexpected_field) ... ok
test_T10_unexpected_free_text_inside_known_field (test_safe_boundary.BoundarySyntheticTests.test_T10_unexpected_free_text_inside_known_field) ... ok
test_T11_document_hash_mismatch_same_ref (test_safe_boundary.BoundarySyntheticTests.test_T11_document_hash_mismatch_same_ref) ... ok
test_T12_head_drifts_during_page_walk (test_safe_boundary.BoundarySyntheticTests.test_T12_head_drifts_during_page_walk) ... ok
test_T13_truncation_or_cursor_loop (test_safe_boundary.BoundarySyntheticTests.test_T13_truncation_or_cursor_loop) ... ok
test_T14_unapproved_redirect_source (test_safe_boundary.BoundarySyntheticTests.test_T14_unapproved_redirect_source) ... ok
test_T15_multimodal_or_preview_payload (test_safe_boundary.BoundarySyntheticTests.test_T15_multimodal_or_preview_payload) ... ok
test_T16_graphql_partial_with_error (test_safe_boundary.BoundarySyntheticTests.test_T16_graphql_partial_with_error) ... ok
test_T17_unvalidated_cache_read_not_allowed (test_safe_boundary.BoundarySyntheticTests.test_T17_unvalidated_cache_read_not_allowed) ... ok
test_T18_streamed_unvalidated_first_chunk (test_safe_boundary.BoundarySyntheticTests.test_T18_streamed_unvalidated_first_chunk) ... ok
test_T19_direct_connector_bypass_not_supported (test_safe_boundary.BoundarySyntheticTests.test_T19_direct_connector_bypass_not_supported) ... ok
test_T20_prompt_injection_cannot_change_policy (test_safe_boundary.BoundarySyntheticTests.test_T20_prompt_injection_cannot_change_policy) ... ok
test_T21_audit_failure_prevents_release (test_safe_boundary.BoundarySyntheticTests.test_T21_audit_failure_prevents_release) ... ok
test_T22_approved_metadata_and_excerpt_exactly_once (test_safe_boundary.BoundarySyntheticTests.test_T22_approved_metadata_and_excerpt_exactly_once) ... ok

----------------------------------------------------------------------
Ran 22 tests in 0.002s

OK
```

### R — 14 cases
- Command: `python -B -m unittest -v test_remediation.RemediationAdversarialSyntheticTests.test_R01_... through test_R14_... (14 explicit qualified names, see case output)`
- Exit: `0`; passed `14`; failures 0, errors 0, skips 0.
- stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).
- stderr SHA-256 `3a27a5b1c9af0ce4a7ada2c5fab56243db6404f680c0c5c8383e9d2289e94cfd` (1999 bytes).

```text
test_R01_race_same_sink_same_op (test_remediation.RemediationAdversarialSyntheticTests.test_R01_race_same_sink_same_op) ... ok
test_R02_partial_publish_unknown_no_retry (test_remediation.RemediationAdversarialSyntheticTests.test_R02_partial_publish_unknown_no_retry) ... ok
test_R03_pre_publish_error_no_false_released (test_remediation.RemediationAdversarialSyntheticTests.test_R03_pre_publish_error_no_false_released) ... ok
test_R04_approval_mapping_mutation_rejected (test_remediation.RemediationAdversarialSyntheticTests.test_R04_approval_mapping_mutation_rejected) ... ok
test_R05_new_boundary_same_sink_cannot_duplicate (test_remediation.RemediationAdversarialSyntheticTests.test_R05_new_boundary_same_sink_cannot_duplicate) ... ok
test_R06_unapproved_request_id (test_remediation.RemediationAdversarialSyntheticTests.test_R06_unapproved_request_id) ... ok
test_R07_nested_state_type (test_remediation.RemediationAdversarialSyntheticTests.test_R07_nested_state_type) ... ok
test_R08_late_page_unapproved (test_remediation.RemediationAdversarialSyntheticTests.test_R08_late_page_unapproved) ... ok
test_R09_cursor_loop (test_remediation.RemediationAdversarialSyntheticTests.test_R09_cursor_loop) ... ok
test_R10_large_fictional_document (test_remediation.RemediationAdversarialSyntheticTests.test_R10_large_fictional_document) ... ok
test_R11_trusted_approval_input_required (test_remediation.RemediationAdversarialSyntheticTests.test_R11_trusted_approval_input_required) ... ok
test_R12_policy_id_reject_free_text (test_remediation.RemediationAdversarialSyntheticTests.test_R12_policy_id_reject_free_text) ... ok
test_R13_logical_metadata_contradiction (test_remediation.RemediationAdversarialSyntheticTests.test_R13_logical_metadata_contradiction) ... ok
test_R14_expected_blob_pair_mismatch (test_remediation.RemediationAdversarialSyntheticTests.test_R14_expected_blob_pair_mismatch) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.003s

OK
```

### A — 12 cases
- Command: `python -B -m unittest -v test_remediation.RemediationAdversarialSyntheticTests.test_A01_... through test_A12_... (12 explicit qualified names, see case output)`
- Exit: `0`; passed `12`; failures 0, errors 0, skips 0.
- stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).
- stderr SHA-256 `a8d358f5b0a86da09b038ee185ab43e09a1daa98c7b85137f7528205d58b8870` (1809 bytes).

```text
test_A01_three_concurrent (test_remediation.RemediationAdversarialSyntheticTests.test_A01_three_concurrent) ... ok
test_A02_same_request_different_operation (test_remediation.RemediationAdversarialSyntheticTests.test_A02_same_request_different_operation) ... ok
test_A03_different_document_same_operation (test_remediation.RemediationAdversarialSyntheticTests.test_A03_different_document_same_operation) ... ok
test_A04_distinct_trusted_request_ids (test_remediation.RemediationAdversarialSyntheticTests.test_A04_distinct_trusted_request_ids) ... ok
test_A05_delayed_ack_no_concurrent_duplicate (test_remediation.RemediationAdversarialSyntheticTests.test_A05_delayed_ack_no_concurrent_duplicate) ... ok
test_A06_before_publish_failure (test_remediation.RemediationAdversarialSyntheticTests.test_A06_before_publish_failure) ... ok
test_A07_after_publish_failure_and_retry (test_remediation.RemediationAdversarialSyntheticTests.test_A07_after_publish_failure_and_retry) ... ok
test_A08_audit_failure_after_publish (test_remediation.RemediationAdversarialSyntheticTests.test_A08_audit_failure_after_publish) ... ok
test_A09_registry_unknown_disclosed_no_global_guarantee (test_remediation.RemediationAdversarialSyntheticTests.test_A09_registry_unknown_disclosed_no_global_guarantee) ... ok
test_A10_deep_mutable_policy_reference (test_remediation.RemediationAdversarialSyntheticTests.test_A10_deep_mutable_policy_reference) ... ok
test_A11_path_blob_and_extra_mode_tree (test_remediation.RemediationAdversarialSyntheticTests.test_A11_path_blob_and_extra_mode_tree) ... ok
test_A12_large_partial_stream_type_mix (test_remediation.RemediationAdversarialSyntheticTests.test_A12_large_partial_stream_type_mix) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.011s

OK
```

### Compilation
- `python -m py_compile safe_boundary.py test_safe_boundary.py test_remediation.py` — exit 0.
- stdout and stderr empty; each SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Acceptance interpretation
- T=22/22 local PASS after explicitly declared synthetic fixture/API change.
- R=14/14 locally PASS_SCOPED; R11 only proves exact synthetic trusted approval input validation and cannot establish independent content review, and mode/tree authenticity remains external.
- A=12/12 locally PASS_SCOPED; a different sink/process/restart has NO duplicate-delivery guarantee; the risk is NOT hidden by the in-process tests.
- Overall: `LOCAL_SYNTHETIC_CANDIDATE_READY_FOR_INDEPENDENT_D / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`, **conditional on remote artifact pin and independent isolation being acceptable to D**.
- Safe excerpt custody, real GitHub field selection, durable ACK, Work host bypass, OS network deny and actual model ingress have zero performed tests and are NOT_VERIFIED.
- D must be a different author; at least 12 **unknown** new cases. Do NOT count this receipt as an independent signoff.
- #106/#108 final disposition PENDING. FXNS `SOURCE_QUALIFICATION_BLOCKED / CLOSED / UNTESTED`; CSM `BLOCKED / CLOSED / market_outcome_access=false`.
