# JP225 prospective forecast record hash audit — 2026-10-08

## Scope and observation

This is an offline, structural/integrity finding, **not** market outcome evaluation.
No 2026-10-08 post-cutoff information was used as a forecast input. No forecast
numbers, issued forecast file, scientific specification, or trading rule were
changed in this audit.

Source: the new `work/implementation/validate_issued_forecasts.py` run under
`forecast_core.canonical_sha256`, excluding the stored `canonical_sha256` field,
after `record_contract.validate_forecast_record` and event filename checks.

Validated CI:
- push: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37702043456 — SUCCESS
- PR: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37702047574 — SUCCESS

## 2026-10-08 exploratory event

All three newly issued records passed their record contracts, event identity,
and exact canonical SHA-256 recomputation:

| Record | SHA-256 | Result |
| --- | --- | --- |
| 2026-10-08_A1_forecast.json | `8a797f78ecb795bb1987214985c885c725b13557d345526699d4aabfc052e054` | PASS |
| 2026-10-08_A2_forecast.json | `558aa8a281fd4f349927dd24ee374ba7f51853f7bfc4861ef3739733230ae412` | PASS |
| 2026-10-08_A3_forecast.json | `5bc8648ce3c4ab3cb08c4972096b2852bbd26ec79e18bf48f12637f321395914` | PASS |

All preserve `2026-10-08T08:21:45+09:00` as a late issuance and the
`2026-10-08T08:00:00+09:00` information cutoff.
The formal scored cohort stays CLOSED, scientific status UNTESTED,
and event `EXPLORATORY_PROSPECTIVE_NOT_IN_COHORT`.

## Pre-existing 2026-10-06 hash mismatches

The original issued files pass structural record validation but **do not
match** the repository's current canonical hash function:

| Record | Stored hash | Recomputed canonical hash |
| --- | --- | --- |
| 2026-10-06_A1_forecast.json | `896dc8c36fd59288043a6d5d5c16077c90650fe9ad7b7b95fe7ebb4534f7a7ec` | `2685d45ffe0e4de2962a8336b7fe716404394683c10b7fe24d6213f1acef0712` |
| 2026-10-06_A2_forecast.json | `10468c6cbb8913376d2e2ef9a223369b1648bae9cff7c7fd0154c6a6f3e85286` | `52eb90353d69271e257425a7105eb891f1bd2815b47d64119fd20ff5ec78cfeb` |
| 2026-10-06_A3_forecast.json | `a961ee449ceb34ba630723c6fc6010a78b72e87c2f3a66614d7f9e8caa8248e9` | `390ac06dbd72282f20cb4793159e529ed7dd2036d132ae8a4dbd22c87248bcf5` |

**Classification: LEGACY_HASH_MISMATCH_NOT_RECONCILED.**
The discrepancy establishes a difference under the currently specified
canonical calculation; it does **not** establish manipulation, corruption,
or the historical algorithm used to create the stored hashes.
The 10/06 files were not edited.

The validator preserves these historical mismatches visibly as
`LEGACY_HASH_MISMATCH` warnings and refuses to treat them as integrity
passes. Newly issued records from 2026-10-08 onward fail the job on
a canonical-hash mismatch.

## Follow-up boundary

If a separate bounded audit reconstructs the 10/06 hashing algorithm,
record that finding in a new append-only artifact, with the original issue
records intact. Do not silently replace hashes or rewrite issued forecasts.
This finding alone does not justify changing probability inputs, weights,
forecast time, or any scientific evaluation condition.

No market returns, public proxy outcomes, or exact XM results were inspected
for this audit. No trading action was taken.
