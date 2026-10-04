# Stage 2 — frozen events, minimal tick acquisition, then Discovery

## Fixed sequence

1. Receive immutable Stage 1 bytes and verify hashes/schema. Independently establish exact XM, timestamp/BID M1 identity and coverage. Stage 1 must PASS.
2. Check `work/integration/SPEC_FREEZE.json` against unchanged specification bytes. `stage2.py freeze` loads only warm-up/2025 M1, computes EMA5/200 plus predeclared price/EMA200 comparator timestamps, and **no forward return**. No session reset or missing-bar filling; at least 1,000 earlier valid bars per evaluated event.
3. Write canonical event manifest bytes/hash. Commit the manifest hash and source/code/spec identities to GitHub **before** invoking the tick collector. Do not use performance to remove/alter events.
4. `stage2.py collect` requires that externally pinned hash, validates events and derived requests **before MT5 connection**, and retrieves only [signal, signal+60s], [+5m,+5m+60s], [+15m,+15m+60s], [+30m,+30m+60s]. Entry mapping later excludes the exact signal instant; targets include their exact instant. Identical requests are shared; no full-year archive or result calculation is present.
5. Preserve raw BID/ASK, time/time_msc, metadata and SHA-256. Exact duplicate rows remain raw; conflicting BID/ASK at the same millisecond blocks qualification rather than inventing order. Server/symbol properties must match Stage 1.
6. `validate_stage2.validate_stage2` revalidates bound Stage 1 and manifest, each tick request, quote/time/order/schema/hash/source identity and metadata counts. Empty request windows are retained as missing executable quotes. They cannot be imputed. Pin this receipt; independently review Packet A execution PASS.
7. Commit an independent `2025_DISCOVERY` gate binding exact specification hash, combined runner/code hash, event manifest, Stage 1 and Stage 2 file hashes. **Do not create that gate now; no XM data exists.**
8. Only then `run_discovery.py` may run once. An exclusive `DISCOVERY_CONSUMED.json` marker in the Stage 1 folder is written before performance calculation. Failed runs reserve consumption and require a documented recovery decision. Renaming output does not bypass the marker. Explicit copying/editing of inputs is outside this technical guard and forbidden by research policy.
9. Preserve outcome ledger, metrics, terminal decision and hashes. `NO_ADVANCEMENT` leaves holdout closed. A durable qualifying decision may authorize the separately reviewed holdout reader; no concrete holdout parser/collector is included now.

## Commands (after source qualification, not now)

From source-qualification directory:

```powershell
py stage2.py freeze <stage1-folder> <new-manifest-directory>
py stage2.py collect <event_manifest.json> --expected-sha256 <committed-hash> <new-stage2-directory>
```

`validate_stage2.py` provides a callable validator for the integrating research session. The Packet C runner accepts Stage 1, Stage 2, manifest, pinned manifest hash, independent gate, pinned gate hash and new run directory as positional arguments. Its `code_identity()` binds the actual executable module set; a bare PASS string or manifest existence cannot unlock it.

## Calendar-end policy — acquisition safety clarification

No 2026 tick may be requested, including for a late-2025 +5/+15/+30m target. A request extending into holdout is explicitly `BOUNDARY_UNAVAILABLE`. Its event remains in accounting and maps to the existing missing-entry/target status. No market values are acquired to complete it. This narrows acquisition under the user's stricter holdout instruction; it does not shift discovery dates or optimize windows.

## Calculation semantics pinned before XM outcomes

- Python 3.12 standard library, IANA Asia/Tokyo and America/New_York. Record Python/tzdata/platform identities at real execution.
- Date clusters sorted ascending for input-order independence. Random.Random(2255200), 10,000 replications; interval uses sorted indices 250 and 9749 (zero-based). This fixes the existing implementation's discrete percentile convention before XM outcomes.
- Primary selection: >=100 valid events, >=60 dates, positive mean and positive lower interval; largest mean; within 0.01 point choose ALL, then TOKYO_OPEN_30, then TOKYO_CLOSE_30. Descriptive windows/horizons/comparator never replace the primary winner.
- Quote quality must be finite positive BID<=ASK. First valid entry strictly after signal within 60s; first target at/after fixed target within 60s; no imputation.
- Report per-event gross midpoint diagnostics, BID/ASK spreads, net bps, net points; summaries include count/date/missing/mean/median/win-rate, +15m date-cluster interval and overlap. No P/L, leverage, TP/SL or optimization.

A different server-local timestamp domain, insufficient history, ambiguous quote order or unresolved source identity is a qualification blocker; it does not authorize a broker substitute.
