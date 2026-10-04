---
type: CurrentProjection
research_line_id: RL-JP225-IMOM-001
projection_generated_at: 2026-10-05
---

# Current State

Operational state: **SOURCE_QUALIFICATION_PARTIAL_WITH_GAPS / PREPURCHASE**.

- hypothesis: UNTESTED;
- JPX/DataCube market outcomes accessed: NO;
- 2025 confirmation outcomes accessed: NO;
- 2026 holdout outcomes accessed: NO;
- source qualification: PARTIAL_WITH_GAPS;
- specification: FROZEN_PRE_OUTCOME (v0.1 + v0.1.1 + v0.1.2 source amendment);
- deterministic implementation: SYNTHETIC_TESTS_PENDING_POST_PACKET_A_CHANGE;
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

**PARTIAL_WITH_GAPS / PREPURCHASE_QUALIFICATION_COMPLETE**

PASS is not available before actual 2025 files exist because Packet A still requires:

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

## Next action

Rerun synthetic CI after the v0.1.2 implementation binding change.

After CI passes, the next external dependency is DataCube acquisition/use-category resolution. The one-shot 2025 confirmation remains locked.
