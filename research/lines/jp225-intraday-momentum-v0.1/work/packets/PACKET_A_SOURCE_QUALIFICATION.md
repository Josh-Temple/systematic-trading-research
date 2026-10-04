# Packet A — Source qualification

Role: independent source qualifier.

1. Fresh-read current main, this line's SPEC and SOURCE_CONTRACT.
2. Do not access 2026 data.
3. Resolve exact JPX DataCube Nikkei 225 mini dataset/product identity and license/storage boundary.
4. Validate timestamp and contract-code semantics without calculating price outcomes.
5. Produce a bound source receipt with raw-file hashes and coverage-only diagnostics.
6. PASS only if source semantics are adequate for the frozen point mapping.

Output must distinguish PASS, PARTIAL_WITH_GAPS and FAIL.
