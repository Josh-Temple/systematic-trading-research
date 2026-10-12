# Synthetic pre-model read boundary — remediation candidate (UNMERGED)

**Status: AUTHOR-SIDE OFFLINE SYNTHETIC PASS ONLY / INDEPENDENT D PENDING / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE.**

This candidate descends from PR #110 exact commit `0faf05b453c5d7897c3566d871591b2926ba928e`. The user gave **separate, explicit approval** on 2026-10-12 for changes **only within the original `synthetic-pre-model-gate` folder** and for completely fictional offline tests in a new branch. It does not authorize use of real GitHub API traffic, actual model input, historical FX/news/ECB information, Work host permissions, CI/Actions, or merge. The four original files are preserved in PR #110; only a separate child branch is modified.

## Changes from #110

- **In-process atomicity:** the synthetic `DeliverySink` now owns one RLock and a reservation registry shared by `Boundary` instances that use that exact same sink object. Reservation, attempted publish and state transition take place within that lock. The key includes fixed policy/repository/PR/head, trusted fictional request ID, operation, and approved document path. Concurrent calls on one sink cannot release the same key twice. **Separate sinks, separate processes, restart and lost registry are NOT protected.** A real deployment MUST fail closed without an authoritative persistent registry; this prototype is not a deployment.
- **Receipt semantics:** `RESERVED` precedes publish; a normal synthetic sink return simulates ACK and is followed by `RELEASED`. An exception before or after publish is conservatively `UNKNOWN`, with **no retry**. Failure of the post-publish receipt leaves internal state UNKNOWN; an already delivered item is not relabeled BLOCKED. These are memory-only receipts, not independent durable evidence or actual delivery confirmation.
- **Trusted approval inputs:** `ApprovedDocument` requires explicit synthetic `approval_id` and exact SHA-256 of safe excerpt; mapping is copied and immutable after policy creation. Initial raw-body digest is also checked. **A matching digest or syntactically valid fabricated approval does NOT prove genuine reviewer identity, ownership, independence, material suitability, signatures, or custody.** That external requirement remains NOT_VERIFIED.
- **Metadata and Git identity:** reject logically inconsistent OPEN/merged/draft combinations. `FILE_PATHS` requires a prior trusted exact path-to-blob OID mapping; unexpected mode/tree fields are rejected, **but external tree/mode provenance is not authenticated here**. Reject free-text/oversized `policy_id` at policy construction and reject unexpected fields/type confusion.
- **Request API change:** a synthetic `approved_request_id` may be passed in addition to the original exact four request keys; `request_id` remains unapproved. It is a test identifier only, **not a signed authorization**. Two approved fictional documents can have distinct release identities. The original 22 tests retain their names and safety objectives; their approval fixture now supplies trusted synthetic approval/hash and blob mapping, and T22 expects the new `RESERVED` then `RELEASED` state sequence instead of only RELEASED. This is a deliberately documented API/test-fixture change, not a silent relaxation.

## Author-side tests (Python 3.13.5, standard library only)

In the source folder, do not run network or model connectors:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_safe_boundary
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_remediation
python -m py_compile safe_boundary.py test_safe_boundary.py test_remediation.py
```

Case-level receipts, shell exit codes, and stdout/stderr SHA-256 are in `TEST_RECEIPT.md`. Observed **22 original T-case scenarios + 14 author-reconstructed R-case scenarios + 12 additional author cases = 48/48 local synthetic cases PASS**, zero failures/errors/skips; `py_compile` succeeded. R-tests **were reimplemented from #114's textual specifications**, not the unpublished original test source; even identical R labels do not mean identical bytes or independent verification. R11's local PASS means *approval input constraints exist*, not that an actual safe excerpt was independently approved. A's tests are **not an independent D acceptance**.

No live source was read, contacted or staged by the tests. OS network-namespace restriction could **not** be established here (`unshare -n` failed with operation not permitted), so **host-level network denial remains NOT_VERIFIED**. The Python test cases use only fictional in-memory objects and no network APIs. No CI was dispatched; `[skip ci]` on the proposed commit does not constitute a passing CI job.

## Mandatory external acceptance before any expansion

1. A separate D reviews exact new head/tree/file identities and independently executes T01–T22, R01–R14 equivalents **and at least 12 new unseen adversarial cases** in a documented isolated environment. Any failure means NEEDS_REVISION.
2. Independently verify a model-inaccessible source-side broker, minimum-field GitHub query, host/tool/browser/shell/file/cache/OCR/network/multimodal denial, real custody of independently approved excerpt, durable audit/ACK and actual ingress. **No such host/security acceptance is claimed or authorized here.**
3. Independently decide #106/#108, FXNS source contract/ledger migration, CSM supply/gate, real-source qualification and research cohort. Synthetic code PASS cannot unlock them.

**Gate remains FXNS `SOURCE_QUALIFICATION_BLOCKED / formal cohort CLOSED / HYP-FXNS UNTESTED / NO_QUALIFIED_ALTERNATIVE`; CSM I2 `BLOCKED / CLOSED / market_outcome_access=false / HYP-CSM-002 UNTESTED`; `PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE`.**
