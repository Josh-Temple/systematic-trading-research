---
type: CurrentProjection
research_line_id: RL-JP225-IMOM-001
projection_generated_at: 2026-10-05
---

# Current State

Operational state: **SOURCE_QUALIFICATION_PARTIAL_WITH_GAPS / PREPURCHASE / WAITING_FOR_JPX_LICENSE_CLARIFICATION / OUTCOME_BLINDNESS_COMPROMISED**.

- hypothesis: UNTESTED;
- JPX DataCube target raw outcomes accessed: NO; external JPX 2025 quote-snippet exposure: YES (see incident record);
- 2025 target confirmation DataCube outcomes accessed: NO (target files not acquired);
- 2026 holdout outcomes accessed: NO;
- source qualification: PARTIAL_WITH_GAPS;
- specification: FROZEN_PRE_OUTCOME (v0.1 + v0.1.1 + v0.1.2 source amendment);
- deterministic implementation: SYNTHETIC_TESTS_PASS;
- 2025 confirmation: LOCKED;
- 2026 holdout: LOCKED;
- live trading authority: NONE.

## Packet A findings

Public JPX/DataCube material resolves the intended source family and most source semantics:

- Financial Derivatives / Tick / Nikkei 225 mini;
- monthly CSV delivery;
- Nikkei 225 mini product/index segment 19;
- trade_date / execution_date / security_code / time / trade_price / trade_volume / sequence No / contract_month / sco_category fields;
- millisecond timestamp representation for 2025-era OSE data;
- sequence No provides execution ordering within trade date and security code;
- contract_month is directly available as YYYYMM;
- strategy-trade rows are explicitly flagged and are excluded by v0.1.2;
- all frozen 09:30/15:00/15:30 clock points fall inside the Nikkei 225 mini day session.

Packet A also found that using the first 2025 TSE date would require a 2024-12-30 predecessor price. v0.1.2 excludes that first candidate rather than opening a 2024 monthly tick file.

## Packet A classification

**PARTIAL_WITH_GAPS / WAITING_FOR_JPX_LICENSE_CLARIFICATION / OUTCOME_BLINDNESS_COMPROMISED**

PASS is not available because Packet A still requires actual 2025 files and human gates; the outcome-access incident also requires research-owner disposition. Packet A still requires:

- exact 2025 monthly item/file identities;
- raw-file byte sizes and SHA-256;
- product-file timezone confirmation;
- real +60-second boundary coverage;
- target-file sequence-number diagnostics;
- final purchase/use category and publication boundary.

The raw DataCube files remain LOCAL_ONLY by default. Do not upload raw rows or reconstructable mapped prices to GitHub, ChatGPT, Drive or another cloud service.

See:

- work/source-qualification/PACKET_A_RESULT_2026-10-05.md
- work/source-qualification/DATACUBE_ACQUISITION_PLAN.md
- specifications/SPEC-JP225-IMOM-001-v01.2_SOURCE_AMENDMENT.md

## Post-Packet-A validation

GitHub Actions workflow `JP225 intraday momentum synthetic` passed on head `13401c0bf32ad8ebcdf13ea1bf7da0d59442d4e5` (run #34) after v0.1.2 was bound into the code identity and strategy-trade exclusion was tested.

## Next action

The next dependency is external and cannot be completed from public metadata alone:

1. confirm the applicable DataCube purchase/use category and publication boundary;
2. purchase/download the 2025 Nikkei 225 mini monthly tick files;
3. keep raw files local;
4. run coverage-only source qualification and bind exact SHA-256 identities;
5. independently review the source receipt.

The one-shot 2025 confirmation remains locked.


## 2026-10-04 public metadata refresh and integrity correction

Fresh direct review of the current J-Quants DataCube pages identified the public monthly product series as future_tick_19_YYYYMM, with a shared month selector for 2025-01 through 2025-12. All twelve periods are in DATACUBE_2025_PURCHASE_MANIFEST.json. Public display rates total ¥3,960 for the personal/academic tier, ¥79,200 for corporate self-use, or ¥237,600 for external distribution across twelve months; no single tier is selected pending JPX clarification.

The current DataCube FAQ says result-only analysis outputs may be provided within self-use, but the exact classification of the planned public hashes, schema, coverage counts, and unaffiliated individual research is not explicit. The status is LICENSE_PUBLICATION_BOUNDARY_UNRESOLVED. The inquiry draft is complete and has not been sent.

Integrity correction: an official JPX search result exposed a 2025 futures quotation snippet during this Work run. The research line is not outcome-unviewed. No quote values were recorded or used, no calculation was performed, no target DataCube files were acquired or inspected, and no 2026 market data were accessed. See work/source-qualification/OUTCOME_ACCESS_INCIDENT_2026-10-04.md. The 2025 confirmation remains locked pending owner disposition.

New local-only validator and 14 synthetic tests are in work/source-qualification/validate_datacube_2025.py and work/implementation/test_datacube_validator.py. The validator is locked from reporting Packet A PASS while the outcome-access incident remains unresolved. Raw files and any generated receipt remain local-only.
