# A — FXNS persisted synthetic nested consistency repair (2026-10-09 JST)

## Scope and exact evidence
- Repository: `Josh-Temple/systematic-trading-research`
- New complete candidate: [Draft PR #82](https://github.com/Josh-Temple/systematic-trading-research/pull/82), targeting `research/fx-news-sentiment-v0.1`.
- Derived from old [PR #74](https://github.com/Josh-Temple/systematic-trading-research/pull/74) exact HEAD `9ebfc57dd4060825da189b196dd044b6ffaead4f`. Old #74 remains unmerged and must **not** be separately merged without fresh independent assessment.
- Code-and-test tested commit: `94b817ca97588d8dca4fc5a7433bc28d43cb830d`. This receipt-only commit will produce a subsequent final PR HEAD; check **that exact HEAD** and its Actions log before B or E acts. A successful run on an older commit is not evidence of CI on a later one.
- Old #74 -> tested code commit changed exactly `work/implementation/event_ledger.py` (+31 lines) and `work/implementation/test_event_ledger.py` (+101 lines); old eight candidate paths are inherited byte-for-byte, no other A edits.
- Existing [#77](https://github.com/Josh-Temple/systematic-trading-research/pull/77) A-C-04 / A-C-05 findings motivated this repair. [#79](https://github.com/Josh-Temple/systematic-trading-research/pull/79) previously held integration.

## Actual offline Actions evidence
- [GitHub Actions run 37859519954](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37859519954), job `113591652110` `fxns-synthetic-offline`: **completed/success** on tested code HEAD `94b817ca97588d8dca4fc5a7433bc28d43cb830d`.
- Direct job-log inspection: Python 3.13, implementation discovered 77, source-probe 11, total **88**; `Ran 88 tests`; `run=88; failures=0; errors=0; skipped=0; successful=True`. Syntax-compilation step: success.
- This is a GitHub CI execution, **not an independent local rerun**. Local direct `git ls-remote` could not resolve github.com; independent full-suite result in this session: `NOT_RERUN`.
- Historic success remains [run 37798966613](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798966613) at #74: 83/83 PASS. Historic failure remains [run 37798633932](https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37798633932): 83 tests, one fixture error. Both are **different commit evidence**, not a replacement for this run.

## Implemented control (no scientific rule change)
Both direct writer and readback call existing `_validate_synthetic_record`, which now applies **existing** `validate_batch(classification_raw, input_record_ids)` to persisted strings and requires exact equality with `classification_parsed`. This enforces strict JSON, required/only fields, enum, reason, and input identity. It then uses unchanged `daily_scores` and `pair_action` to recompute EUR and JPY scores and decision. Stored scores must be numeric, excluding `bool`, finite and **exactly** equal to deterministic recomputation; stored decision and NO_TRADE flag must match. No new tolerance/threshold/query/currency/prompt/schema/event-window alteration. Formal issue/outcome join still unconditionally raise the CLOSED gate errors.

## Negative synthetic fixtures / outcomes
Five new unittest methods (33 in `test_event_ledger.py`) exercised multiple subtests at **both** direct writer and outer-hash-recomputed file readback: invalid JSON; extra raw or parsed `market_outcome`; mismatched or missing nested fields; invalid reason and input ID; nested real URL; changed scores, `bool`, string, NaN, infinity, oversized integer; decision inconsistent with recomputed score; NO_TRADE rehashed to a directional decision without rescoring. Valid LONG and NO_TRADE round-trips continue to succeed. Same-ID exclusive create and blocked receipt tests from the prior 83 remain in the passing suite.

**Important adverse boundary**: a privileged editor can replace *all* fields with another coherent synthetic event and recompute SHA-256; the intentionally explicit test confirms the verifier cannot authenticate original authorship. The fix stops semantic inconsistencies, **not** full hostile-disk rewrite or protected-ledger provenance. Python socket blocking in CI is process-local, not a production sandbox.

## Disposition / handoff
- **A implementation and exact-code-head offline CI: PASS_SCOPED**. This is an A scope statement, **not an independent audit or final integration approval**.
- **Independent Role B: NOT_RUN in this session**. B must inspect **final PR #82 HEAD**, final Actions job logs, full PR changed paths, and negative writer/rehash fixtures in a separate Chat. Any A change after B locks a HEAD invalidates that audit.
- **E: HOLD_NO_MERGE** until B independently reports `PASS_SCOPED` on exact candidate SHA and verifies CI/all allowlist conditions. Neither #82 nor #74 is merged.
- Research state unchanged: `UNTESTED`, `PROPOSED_NOT_FROZEN`, formal cohort `CLOSED`, GDELT `SOURCE_QUALIFICATION_BLOCKED`, XM `LOCAL_XM_EXECUTION_REQUIRED` (explicitly deferred). No real news, live GDELT, real EURJPY/market outcome/returns/P&L, XM/MT5, paper/live orders or human freeze.
