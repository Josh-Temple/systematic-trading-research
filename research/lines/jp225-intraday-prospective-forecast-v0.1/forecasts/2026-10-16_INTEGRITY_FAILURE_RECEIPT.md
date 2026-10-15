---
type: IssuanceIntegrityFailureReceipt
event_id: XPF-JP225-20261016
severity: FAIL
reviewed_at: 2026-10-16T08:08:00+09:00
issued_forecast_validity: INVALID_CANONICAL_SHA256_LENGTH
cohort_status: EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT
repair_status: HASH_CORRECTION_DOCUMENTED_ORIGINALS_UNMODIFIED
---

# 2026-10-16 — Invalid SHA-256 on late exploratory forecast records

## Observed failure

The late 2026-10-16 issuance at GitHub commit `efd6c71eae5fc8d0023346797e3d4334b6a911ed`, actual GitHub commit time **08:07:02 JST** (pre-09:00 but after 08:00 information cutoff), contains malformed `canonical_sha256` fields in all three A1/A2/A3 forecast JSONs: each is **512 hexadecimal characters**, while the record verifier strictly requires **64 hexadecimal characters**. Both official Push and PR GitHub Actions **FAILED** at that commit:
- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/38821599503
- https://github.com/Josh-Temple/systematic-trading-research/actions/runs/38821606747

**Cause:** the issuance helper correctly produced the first eight SHA-256 state words but mistakenly serialized *all 64 internal prime-derived initial hash words* instead of the required first eight. The first 64 hexadecimal characters of every malformed stored field were independently recomputed using the fixed algorithm and match the canonical SHA-256 of the respective JSON payload with `canonical_sha256` excluded. Control check: recomputation of already-valid 2026-10-15 A3 returns its exact stored digest `aa788ed3ff7120dc2b54c6e9b87a879afb0c2a62af0eed8e2bbc012e1cd70bf9`.

| Immutable forecast | Original Git blob SHA | Stored digest length | Independently recomputed canonical SHA-256 |
| --- | --- | ---: | --- |
| `2026-10-16_A1_forecast.json` | `ab3cfe2544a06296610a091f64cffe27ffa4d678` | 512 | `cccaf0c231c721b11062c1f54b72fff45b9b4b299bfe3c253ba334492f0fd51b` |
| `2026-10-16_A2_forecast.json` | `2d88b01f787913df0f1b116638841e9e0244764b` | 512 | `9748011eb80d2ad6b28e8cf523a15f5b7d75083a4d4ed0a6c1a996f4c21acc06` |
| `2026-10-16_A3_forecast.json` | `f38e907f5169c1274d37b3d619f4bfd55784c3e9` | 512 | `c36201b556e704b81a1cdffdbdce1446ee634dbbe7d7fc48894e206bd9250498` |

## Forecast numbers (preserved, not certified)

| System | P(up) | Forecast return |
| --- | ---: | ---: |
| B0 | 0.50 | 0 bps |
| A1 | 0.51 | +2 bps |
| A2 | 0.50 | 0 bps |
| A3 | 0.50 | 0 bps |

These are **late-issued exploratory candidate numbers only**. There was no pre-08:00 pre-registration, pre-cutoff freeze, qualified XM input, or calibrated skill. All source reports were published pre-08:00 but retrieved afterwards. The target remains Japan cash-day 09:00 to 15:30, not prior-close to close. **No trading**.

## Decisions and provenance

1. **No silent replacement:** original three JSON files, all probabilities and returns, `issued_at` timestamps, original Git blobs and recorded malformed hash values are left **unchanged**. This follows the `forecasts/README.md` prohibition on replacing issued forecast files to correct them.
2. **No false CI claim:** this issuance is marked `INVALID_CANONICAL_SHA256_LENGTH` / `NEEDS_REVISION`; a future passing test run cannot retroactively make the original issue valid. Until a separately authorized remediation protocol, the branch validator should continue to fail on the malformed original records. DO NOT weaken the validator, ignore corrupted files, spoof hashes or misclassify warnings as integrity passes.
3. These 64-character hashes are **independent correction evidence**, not a claim that the original JSON fields were valid or revised. No Git history was rebased, no PR merged.
4. No formal prospective-cohort admission, no formal XM outcome, no P/L, no trading; keep status `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`, SPEC `PROPOSED_NOT_FROZEN`, science `UNTESTED`.
5. For repair, prefer an explicitly reviewed, append-preserving remediation protocol that preserves original blobs, names a new independent canonical record identity, and defines how a validator can recognize a superseded **invalid** issuance without silently ignoring it. Do not change existing forecast files or validator rules merely to turn CI green without independent review.

## Issue provenance

Original issuance: https://github.com/Josh-Temple/systematic-trading-research/commit/efd6c71eae5fc8d0023346797e3d4334b6a911ed

The issue was detected during the same user request after commit/push, before any formal market outcome. The negative result is intentionally retained as reproducible source/integrity evidence.

**Outcome: BLOCKED_INTEGRITY — forecast publication existed, but valid canonical issuer record was NOT established.**
