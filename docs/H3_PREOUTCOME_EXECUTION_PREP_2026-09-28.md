# H3 pre-outcome execution preparation — 2026-09-28

Status: `WAITING_FOR_MATURITY`  
Research line: `RL-HR-001`  
Hypothesis: `HYP-HR-003`  
Specification: `SPEC-HR-003-v01`  
Decision: `DEC-HR-004`  
Dataset: `DATA-HR-003 = FINAL_HOLDOUT / UNUSED`

This record captures source/execution preparation only. It is **not** an H3 Run,
Result, interpretation, sample freeze, or full source-gate PASS.

No H3 touch-to-+15-minute outcome, CONFIRMED-vs-UNCONFIRMED performance
comparison, primary contrast, or bootstrap result was computed or viewed.

## 1. Fresh-read basis

Work started from GitHub `main`:

```text
95d3d83be7c3e3ca3119d2ae31f4e6b4cd6714ef
```

The following authorities were fresh-read before implementation:

- frozen Post-H2 H3 preregistration;
- H3 source-preparation handoff;
- `SPEC-HR-003-v01`;
- `EXP-HR-007`;
- `DATA-HR-003`;
- `DEC-HR-004`;
- the prior sealed Stage A summer-hours interpretation;
- H2 reproducibility code/result;
- the exact recovered legacy `run_v01.py`.

## 2. Current maturity state

The outcome-blind structural scan through 2026-09-25 contains 56 candidate
weekdays.

Result:

```text
calendar candidates        = 56
structurally eligible       = 55
structurally ineligible     = 1
frozen selected sessions    = 0
remaining to maturity       = 5
source gate                 = NOT_EVALUATED_PENDING_MATURITY
current state               = WAITING_FOR_MATURITY
```

The sole structural exclusion remains:

```text
2026-09-07
observed M1 rows = 1,229
expected M1 rows = 1,380
missing required tradable minutes = 151
```

The 55 eligible dates are retained as the chronological eligible prefix for
auditability. They are not described as a frozen H3 sample. Under the
preregistration the exact sample is frozen only when the first 60 eligible
sessions exist.

## 3. Real persisted-source verification through 2026-09-25

The persisted Drive source archives were downloaded and rechecked without
running the H3 event/outcome calculation.

### Legacy generator

Exact identity:

```text
run_v01.py
SHA-256 = 9d655d68424624167ac9fe07fd74602fab59d7c096c3a631f36c385d6257b1dd
status = PASS
```

### Fixed H2 M1 prefix

The previously frozen generator prefix was checked from persisted source:

```text
records = 135
first date = 2025-12-31
last date = 2026-07-09
75 context + 60 frozen H2 selected sessions
identity = PASS_135_EXACT_RAW_MATCH
```

No event generation was required for this identity check.

### Post-H2 M1

For 2026-07-10 through 2026-09-25:

```text
raw M1 responses = 56
basic-validation PASS = 56 / 56
persisted byte/hash readback = PASS
structurally eligible = 55
```

### Combined generator history

The fixed H2 prefix and post-H2 M1 source were concatenated chronologically for
an outcome-blind continuity/quality check:

```text
M1 source files = 191
decoded M1 rows = 257,315
prefix last date = 2026-07-09
post-prefix first date = 2026-07-10
latest date = 2026-09-25
global timestamps strictly increasing = PASS
finite / valid OHLC = PASS
Gamma history reset at 2026-07-10 = NO
```

This verifies source/history continuity only. It does not resolve the known
legacy Gamma temporal-information limitation recorded by `DEC-HR-004`.

### Tick

All candidate weekdays were acquired as full 24-hour first-party Tick scopes,
independent of touch/confirmation identity:

```text
candidate dates = 56
expected hourly records = 1,344
raw hourly records verified = 1,344
records with original retrieval timestamp = 224
records with original timestamp UNKNOWN but exact re-fetch receipt = 1,120
empty Tick buckets retained = 82
raw timestamp/BID/ASK/spread validation = PASS
```

The 1,120 verification receipts do not rewrite the unknown original retrieval
times. They separately establish that a later first-party re-fetch matched the
stored response byte count and SHA-256 exactly.

## 4. Consumed-H2 classifier identity validation

H3 requires binary `CONFIRMED / UNCONFIRMED` classification before the
legacy same-confirmation-bar execution-ambiguity filter.

The prepared classifier was therefore validated against the **already consumed
H2 M1 prefix only**, not against DATA-HR-003 outcomes.

Observed validation:

```text
H2 selected sessions = 60
crosschecked sessions = 60
legacy touch population match = PASS
legacy clean-confirmation output match = PASS
same-confirmation-bar accounting match = PASS
same-touch-bar ambiguity accounting match = PASS
H3 post-2026-07-09 source used for this classifier validation = NO
Tick outcome used = NO
primary contrast computed = NO
bootstrap run = NO
```

This is implementation-identity evidence only.

## 5. Prepared fail-closed execution path

The following outcome-blind/gated tools are now prepared:

- `build_h3_source_gate.py`
  - recomputes source identity/quality from raw persisted bytes;
  - verifies exact H2 prefix and continuous H2 -> H3 M1 history;
  - recomputes Tick integrity rather than trusting manifest labels;
  - requires either the original retrieval timestamp or a matching exact
    re-fetch receipt for every Tick bucket;
  - does not freeze a sample with fewer than 60 eligible sessions.
- `validate_h3_classifier_h2.py`
  - validates H3 classification mechanics using consumed H2 M1 only.
- `run_h3_once.py`
  - prepared but **not executed on H3**;
  - cannot start without a passing 60-session freeze packet;
  - revalidates the full source gate before outcome access;
  - is bound to its own SHA-256 at freeze time;
  - uses a new output directory and writes run-start / outcome-access receipts;
  - preserves same-confirmation-bar events as CONFIRMED for H3 classification.
- `.github/workflows/h3-source-preparation.yml`
  - regression-tests the source/maturity/execution locks.

The full gate also requires, once the exact 60-session list exists, a fresh
independence attestation bound by SHA-256 to that exact list. The attestation
must state that no prior analysis of the exact H3 outcome was found and that the
review itself did not access the outcome.

The attestation is intentionally **not** created now because the final 60-session
sample does not yet exist.

## 6. Freeze behavior

While fewer than 60 eligible sessions exist, the gate must emit:

```text
status = WAITING_FOR_MATURITY
source_gate = NOT_EVALUATED_PENDING_MATURITY
frozen_selected_count = 0
freeze_packet = null
```

Once the first 60 eligible sessions exist, a passing freeze packet binds:

- exact 60 selected dates;
- exact H2-prefix identity;
- full post-H2 M1 identity;
- selected-session Tick identities;
- continuous generator-history source-chain hash;
- exact legacy generator SHA-256;
- H3 runner SHA-256;
- exact-sample independence-attestation SHA-256;
- bootstrap seed `20260913`;
- 10,000 replications;
- bootstrap engine `numpy.random.default_rng/PCG64`.

Any source or runner drift after that invalidates the packet.

## 7. Structural scope for the next five dates

The prior sealed summer-hours rule has been outcome-blind extended in code
through 2026-10-02 only. This covers the five candidate weekdays after
2026-09-25 that would reach 60 eligible sessions if all pass.

If any of those dates is structurally ineligible and maturity moves beyond
2026-10-02, the code fails closed. The summer-date bound must then be extended
only after another outcome-blind review of the applicable official-hours
convention. H3 outcomes must remain closed during that extension.

## 8. Current scientific boundary

Nothing in this preparation changes the scientific state:

```text
HYP-HR-003 = WAITING_FOR_MATURITY
DATA-HR-003 = FINAL_HOLDOUT / UNUSED
H3 Run = NONE
H3 Result = NONE
SOURCE_GATE = NOT_EVALUATED_PENDING_MATURITY
OUTCOME_COMPUTED = NO
CONFIRMATION_OUTCOME_COMPARISON = NO
PRIMARY_CONTRAST_COMPUTED = NO
BOOTSTRAP_RUN = NO
PROTOCOL_CHANGED = NO
PARAMETER_SEARCH = NO
SAMPLE_RESELECTION = NO
```

The source-component checks passing through 2026-09-25 are not a full H3
source-gate PASS. Maturity, exact 60-session freeze, independence review, and
the final freeze packet remain prerequisites.

## 9. Next action

After each subsequent **fully completed UTC candidate weekday**:

1. acquire first-party BID M1;
2. acquire all 24 first-party BID/ASK Tick buckets outcome-independently;
3. persist/read back raw bytes and hashes;
4. apply only the frozen structural gate;
5. update the chronological eligible count.

Stop accumulation immediately when the 60th eligible session is reached.

Then, before any H3 outcome access:

1. conduct the exact-sample independence review;
2. build and persist the full source/freeze packet;
3. read it back and confirm every component PASS;
4. only then execute `run_h3_once.py` once under the frozen preregistration.

If any required gate fails, finish `HALTED_FAIL_CLOSED`. Do not replace a date,
provider, threshold, horizon, source, bootstrap rule, or classification rule to
rescue the test.
