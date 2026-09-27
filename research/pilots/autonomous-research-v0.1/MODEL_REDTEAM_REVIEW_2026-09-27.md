# Source-informed model red-team review — 2026-09-27

Status: REPRODUCED_AND_FIXED_PARTIAL_EVIDENCE  
Scientific effect: NONE  
Market data used: NONE  
Target: Autonomous Research Pilot v0.1 Phase A evaluator

## 1. Method

After the deterministic fuzz/property round passed, GPT-5.6 Sol was shown the evaluator source and asked, in effect, to inspect it as an optimizing/adversarial researcher rather than to generate trading ideas.

The generated attack corpus is:

- `MODEL_REDTEAM_ATTACKS_v01.json`

The corpus explicitly records:

- generator/model;
- source-informed method;
- `NOT_INDEPENDENT` status;
- pre-red-team target commit;
- no market-data use.

This is not an independent external security audit.

## 2. Clean baseline reproduction

To distinguish source-based suspicion from reproduced behavior, an evidence-only branch was created from the pre-fix main:

- baseline: `dd62d8b541cf95e0f5bb85faf96cfe7ab03ae449`
- evidence branch: `evidence/phase-a-redteam-baseline-20260927`
- added reproduction tests only
- evidence commit: `d3f558c62c6ea4a832af8c710290e4f0fd4e8bb1`

GitHub Actions:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36324571918
- result: **FAILED intentionally**
- total: 35 tests
- errors: 3

The evidence branch is not a proposed merge. Its failed run is preserved as failure evidence against the historical baseline.

## 3. Reproduced finding RT-R1 — enum type confusion

Attack:

```json
"feature": {
  "source": []
}
```

Expected boundary behavior:

```text
CandidateInvalid
```

Observed on baseline:

```text
TypeError: unhashable type: 'list'
```

Cause:

The baseline checked:

```python
if source not in _ALLOWED_SOURCES:
```

before proving that `source` was a string/hashable scalar.

### Impact

Malformed researcher input could escape the intended candidate-invalid path.

In direct evaluator mode, similar unexpected exceptions could be misclassified as evaluator failure rather than input invalidity.

### Fix

Require string type before membership checks for:

- source;
- transform;
- operator;
- side.

The model corpus also includes object/list variants on these related enum surfaces.

## 4. Reproduced finding RT-R2 — huge integer float conversion

Attack:

- syntactically valid JSON integer
- approximately 1,000 decimal digits
- used as `threshold`

Expected:

```text
CandidateInvalid
```

Observed on baseline:

```text
OverflowError: int too large to convert to float
```

Cause:

`_finite_number()` checked Python type and then called `float(value)` without converting `OverflowError` into a candidate-invalid result.

### Fix

Catch float-conversion overflow/value errors and classify them as `CandidateInvalid`.

The same rule is applied to host dataset numeric conversion, where conversion failure becomes `EvaluatorFailure`.

## 5. Reproduced finding RT-R3 — lone-surrogate candidate ID breaks receipt hashing

Attack:

- Python candidate object with `candidate_id = "\ud800"`

Observed on baseline:

```text
UnicodeEncodeError: surrogates not allowed
```

The failure occurred while hashing the result receipt.

### Why this mattered

The baseline receipt copied `candidate_id` before validating whether it was safe UTF-8 text.

Even when later validation failed, the invalid raw identifier remained inside the receipt and could break canonical UTF-8 serialization.

### Fix

- validate text as UTF-8;
- sanitize candidate ID before placing it in the base receipt;
- invalid raw IDs become `candidate_id: null` in the rejection receipt path.

## 6. Attack hypothesis that did not reproduce as a new baseline failure

### Deeply nested JSON

A depth-1500 unknown array was added to the baseline reproduction test.

Observed:

- cleanly rejected;
- no uncaught recursion failure.

Reason:

The preceding deterministic-fuzz round had already expanded JSON exception handling to include `RecursionError`.

This attack remains in the model corpus as a regression case, but it is **not** claimed as a newly discovered defect in this round.

## 7. Preventive hardening — candidate JSON byte limit

The model review also identified the absence of a pre-parse raw-text size bound.

No concrete resource-exhaustion incident was reproduced.

A 16 KiB candidate JSON limit was added as a preventive boundary because the declarative grammar does not require large payloads.

This is classified as **PREVENTIVE_HARDENING**, not a reproduced vulnerability.

## 8. Fixed-branch verification

Source-informed attack corpus:

- 15 attack cases

After the fixes, CI run:

- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/36324471014
- result: `35 tests / OK`

The tests require:

- every corpus attack to be rejected at the strict JSON boundary;
- structured attack inputs to become `INVALID`, not evaluator failures;
- candidate JSON size limit to be enforced;
- corpus provenance boundary to remain explicit.

## 9. Interpretation

This round provides a concrete example of why autonomous-research infrastructure should itself be researched iteratively:

```text
18 tests green
→ adversarial read finds A1–A5
→ 25 tests green
→ broad fuzz/property testing reaches 31 tests
→ source-informed model red-team finds three additional reproducible failures
→ fixes reach 35 tests green
```

A larger test count is not itself the objective.

The important evidence is that later review repeatedly found failure modes that earlier successful test suites did not cover.

## 10. Remaining limits

Still open:

- OS/process-level separation of researcher and hidden evaluator data;
- same-interpreter access to host-private Python functions;
- concurrent-ledger-writer semantics;
- external checkpointing against ledger tail deletion;
- independent second evaluator implementation;
- independent external red-team review;
- later adaptive-search statistical controls.

No unused market sample should be exposed on the strength of this review alone.

Phase A remains PARTIAL.
