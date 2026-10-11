# Offline synthetic prototype — local test receipt

- **Test environment**: local isolated container, Python `3.13.5`, standard-library `unittest` and `py_compile`; no network or repository checkout.
- **Source**: D audit [PR #109](https://github.com/Josh-Temple/systematic-trading-research/pull/109), scenarios T01–T22. User explicitly approved a **new isolated synthetic-only prototype**; not approval of live tool permissions or research code changes.
- **Unit test command**: `PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_safe_boundary`
- **Compile command**: `PYTHONDONTWRITEBYTECODE=1 python -m py_compile safe_boundary.py test_safe_boundary.py`
- **Observed result**: `Ran 22 tests`, `OK` (22 successes, zero reported failures/errors/skips). Local compile succeeded. Does **not** imply GitHub Actions CI or model-host enforcement.
- **Report status**: `SYNTHETIC_SCOPED_PASS / PLATFORM_NOT_ENFORCED / INDEPENDENT_REVIEW_PENDING / HOLD_NO_MERGE`.
- **Source inputs**: entirely fictional Python fixtures. No real headlines, articles, URLs, FX data, XM/MT5, ECB OBS_VALUE, outcomes or actual model calls.
- **Gate**: `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED`; CSM `BLOCKED / CLOSED / market_outcome_access=false`; no change applied.
- **SHA-256 of checked-out candidate files**:
  - `safe_boundary.py`: `657619311e8f4045b8e60a8a71085e52782649a0dbe2dda3b52a96d267857678`
  - `test_safe_boundary.py`: `e1bc61dcd6d1b79adc086fc80d819d8186bd2afc0a2e2092f3c81ed3572ce515`
  - `README.md`: `f987c7a8c919d59152975d705c479148a2296dc1effafea5ae3de8280d6ff4db`
- **Test output SHA-256**: `81cc57d432b00f9ecf5f36ca59b8ded90b573557b3b4d6fe3433647ca3cf3686`.
- **Known limitations**: no source-side GraphQL field restriction, no actual network/OS bypass prevention, no Work tool interception, no durable or independent audit sink, no safe-document independent approval workflow, no actual model-delivery receipt. In-memory rejection is not equivalent to pre-model security across all connectors.
- **Allowed changes**: new standalone candidate directory only; no previous code/PR files changed.
- **Next acceptance**: code review against T01–T22, adversarial independent rerun with unseen synthetic cases, separate host/network feasibility review, then a narrowly scoped human approval for any deployment. Do not merge before those conditions.

## Local test stdout/stderr (synthetic only)

```
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
Ran 22 tests in 0.001s

OK
```
