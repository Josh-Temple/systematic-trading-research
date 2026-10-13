> **PR #117 eight-findings follow-up (2026-10-12): CODE_SAVED / AUTHOR_TESTS_NOT_EXECUTED / INDEPENDENT_D_WAITING / PLATFORM_NOT_ENFORCED / HOLD_NO_MERGE.** This notice supersedes the inherited author-side PASS status of PR #117 for the NEW candidate. See the appended supplement and the updated TEST_RECEIPT.md. No local Python execution or independent security acceptance is claimed for this revision.

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


## PR #117 D01-D08 follow-up: new branch, NOT YET ACCEPTED (2026-10-12)

- Base: PR #117 branch at exact head `8f69bded3be746f9f6b6fd1011ea8676f5d32877`; original PR #110, #117, main and research branch were not modified.
- New author branch: `work/fxns-pr117-eight-findings-a-20261012`; isolated synthetic code only.
- D01-D03: reject repeated approved file `(path, blob_oid)` and repeated PR metadata identity, across all pages before a release; distinct approved file identities remain allowed.
- D04: `publish()` normal return is insufficient. The fictional in-memory `DeliveryAck` includes a byte digest and index; the boundary checks it against the actual append and unchanged previous list. Missing or forged acknowledgments become `UNKNOWN`, without retry. This is **not a real host delivery acknowledgment**.
- D05: `append()` normal return is insufficient. The boundary checks an exact additional in-memory receipt and unchanged prior entries. Unrecorded `RESERVED` prohibits delivery; an unrecorded `RELEASED` keeps the identity `UNKNOWN` without retry. No durable append-only store is implemented.
- D06-D08 and related cases: strict concrete types for repository/head/base identity, operation and MIME fields; ASCII policy paths/identities. Retained older T07 exception containment. No source-side field selection or Work-host enforcement is implemented.
- Existing `test_remediation.py` SlowSink fixture now **returns** its superclass's explicit fictional ACK. This is a declared fixture/API contract update; the test's success expectations are unchanged.
- New `test_eight_findings.py`: 29 **A-authored test definitions**, comprising D01-D21 reconstructed equivalents/limits (21) and A13-A20 (8). Unpublished earlier D fixture is unavailable and is **not byte-identical or an independent D audit**.
- All Python tests and compilation for the new revision are **NOT_EXECUTED** as of this receipt. Previous PR #117 counts (T22 + R14 + A12 = 48) are historical evidence **for the previous SHA only**, and cannot be carried forward as a new PASS.

Recommended offline commands after exact-file checkout, with a verified isolated Python >=3.12 runtime (standard library only):

```sh
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_safe_boundary
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_remediation
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_eight_findings
PYTHONDONTWRITEBYTECODE=1 python -B -m py_compile safe_boundary.py test_safe_boundary.py test_remediation.py test_eight_findings.py
```

OS network deny, actual model ingress ACK, persistent audit, independent approval custody and real adapter rejection remain `NOT_VERIFIED`. D must **WAIT** until A's new exact full head, source hashes and real passing author-run receipt are submitted. Do not merge, qualify any real source, open a research cohort, or execute trading.
