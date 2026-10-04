# Packet A completion checklist

This checklist preserves the source/data distinction. It does not authorize outcome analysis.

## Pre-purchase metadata

- [x] Official series ID and current product page identified: future_tick_19_YYYYMM.
- [x] All 12 target months are enumerated in the purchase manifest.
- [x] Current displayed prices and tier totals are recorded.
- [x] Download availability window and attempt limit are recorded.
- [x] Local-only acquisition and validator command are documented.
- [ ] JPX clarifies personal/academic/external category and exact public metadata scope.
- [ ] Research-line outcome-access incident is dispositioned without rewriting the historical record.

## Local source receipt

- [ ] Exactly one purchased item/file identity is mapped to each 2025 calendar month.
- [ ] Every raw file has a recorded byte size and SHA-256.
- [ ] All files match the published 11-field, lower-case CSV schema.
- [ ] Index/product identity is index_type=19.
- [ ] No trade-date or execution-date row outside 2025 is accepted; specifically no 2024/2026 row.
- [ ] Expected front-contract months (202503, 202506, 202509, 202512, 202603) are present on the applicable 2025 dates.
- [ ] Timezone is explicitly confirmed from JPX documentation or written support; it is not inferred from clock values.
- [ ] No is present, unique, ascending for the applicable trade-date/security-code stream, and unique within repeated displayed timestamps. Nonconsecutive No values are allowed by the published specification.
- [ ] Each 09:30, 15:00, and 15:30 +60-second boundary was evaluated for each expected TSE trade date.
- [ ] Individual missing dates are represented as unavailable dates with non-price reasons.
- [ ] Systemic ambiguity is absent.

## Human gates

- [ ] Use category and public output list are resolved by JPX.
- [ ] Raw files stay on the user's local device and are not uploaded.
- [ ] Independent source receipt review is PASS.
- [ ] Only after all above checks pass may Packet A be called PASS.

Current status: **PARTIAL_WITH_GAPS / WAITING_FOR_JPX_LICENSE_CLARIFICATION / OUTCOME_BLINDNESS_COMPROMISED**. Synthetic test success does not change source qualification status or repair the outcome-access incident.
