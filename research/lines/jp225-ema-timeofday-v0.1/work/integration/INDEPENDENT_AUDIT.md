# JP225 independent integration audit — 2026-10-04

## FACT — fresh reconstruction

Repository main read via GitHub branch endpoint and fresh clone: `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c`.

All four JP225 PRs were open, draft and GitHub-reported mergeable when first read:

| PR | Role | Base | Head | Local review |
|---|---|---|---|---|
| #42 | architecture | main @ a765b33 | c42f1ce130d49f0aeadcec7010b58627093cb95d | PASS with explicit freeze receipt/acquisition clarification |
| #44 | deterministic implementation | #42 @ c42f1ce | a4f797f4c579d204a1df27a7e63c781640e5e230 | core PASS; hardening required and implemented here |
| #45 | source precheck/collector | #42 @ c42f1ce | 48ede9665b91b308310fee47b97bcfa81c66cdae | old collector FAIL safety review; corrected code synthetic PASS; actual source PARTIAL_WITH_GAPS |
| #48 | proxy findings | #44 @ a4f797f | ed443608d9b778256ed4f5f5ed7a369871a3ee2f | source/accounting/negative classification PASS; original exact bootstrap reproducibility PARTIAL_WITH_GAPS |

Actual graph: main -> #42 -> #44 -> #48, with #45 branching from #42. #44 has 2 commits; #45 has 3; #48 has 27. All local per-PR diffs and commit histories were read. Ordinary local merge of #45 into #48 succeeded without conflicts; inherited CURRENT projection came from #48. No original PR branches/history were rewritten, and no force push was used. This integrating branch preserves both parents.

Fresh open Issues/PRs and latest Actions were queried. Only open non-PR Issue returned was #41 (separate FX monetary-policy proposal). No JP225 head had a check run when queried. Latest repository Actions successes were other research lines and **do not validate JP225**. Main branch endpoint reported `protected=false` with no required status checks; repository rulesets endpoint returned `[]`. No administrative setting was changed or assumed.

Read: Research Principles, Roadmap, Lines Index, complete JP225 line/packets/specification/hypothesis/decisions/prior art, implementation/tests/overlap receipts, source qualification/collectors, and all proxy monthly receipts.

## Research states remain distinct

| State | Exact XM | OANDA midpoint proxy |
|---|---|---|
| HYPOTHESIS | HYP-JP225-EMA-001 UNTESTED | historical continuation candidates only |
| SPECIFICATION | original c42f1ce bytes frozen by SPEC_FREEZE.json; old draft header retained as history | 2019 and 2018 separate preregistration artifacts |
| DATA | no local XM files/terminal accessed | exact consumed 2018/2019/partial-2020 public blobs reread |
| SOURCE QUALIFICATION | PARTIAL_WITH_GAPS | generator expands midpoint candles; no BID/ASK economics |
| IMPLEMENTATION | synthetic-only hardening | independent retrospective source replay |
| EXPERIMENT | Packet C NOT EXECUTED | historical proxy studies already consumed |
| RESULT | none | adverse results retained |
| INTERPRETATION | no profitability conclusion | no stable broad continuation/close-window support established |
| DECISION | WAITING_FOR_XM_STAGE1_DATA; Packet C locked | no rescue searches or promotion to XM |

## XM specification/code audit

No EMA parameter, selectable/descriptive window, sample date, primary horizon or selection threshold was changed. Original specification still has DRAFT_PRE_OUTCOME in its bytes; this integrator freezes exactly those bytes via the separate receipt under the explicit task instruction. A changed specification hash blocks the manifest builder.

Confirmed from code: standard alpha 2/(N+1), first-close initialization, continuous state, equality crossover boundaries, price/EMA200 comparator, no fabricated missing M1 rows, signal-close classification, Asia/Tokyo and America/New_York IANA rules, strict-after entry and at/after target within 60s, long ASK->BID and short BID->ASK, fixed horizon, daily clusters/seed/reps, discrete percentile indices, minimum counts/dates, fixed tie break and NO_ADVANCEMENT.

Gaps in old #44: primitive functions did not implement warm-up enforcement/raw identity/source gates; quote NaN/invalid prices could pass; a candidate string alone was not a durable holdout authorization. New Stage 1/2 and Discovery wrappers enforce these before calculations. New holdout loader validates a pinned decision hash, true advancement, 2025 sample, Packet A/audit PASS, exact bindings and reproducible candidate selection **before invoking the reader**. No concrete holdout parser exists now, and no holdout was read/calculated.

Discrete bootstrap convention is explicitly pinned in STAGE2_PLAN before XM outcomes. Date order is normalized; original generic test only checked repeated calls. Added independent synthetic boundary, privacy, source-binding, loader noninvocation, one-shot and algebra tests.

Calendar-end execution windows extending into 2026 are explicit missing/boundary-unavailable windows; they cannot be acquired to complete a 2025 event. This follows the current stricter user instruction and is an acquisition-safety clarification, not a new trading filter.

## Proxy source and chronology audit

Fresh external repository: FutureSharks/financial-data, commit `7ba1d404aa8b0e1c0f71321acebadcbfb9bcca8d`. Read generator `pyfinancialdata/oanda_prices.py`, README and generator history. Generator was introduced in `f609cab` and constructs UTC UNIX month boundaries, requests M1 candles and expands `candle['mid']`. Hence **midpoint**, not BID, ASK or XM. Source format alone cannot establish actual broker execution.

`PROXY_REPLAY.json` binds all 29 monthly raw blobs to path, Git blob and independent SHA-256 (2018:12, 2019:12, 2020:5). Git blob identity was recomputed from byte content. 2018/2019 receipt source identities match their raw files. Row totals: 300680 / 250276 / 117975, respectively. No fresh samples beyond these consumed years were accessed.

Git ancestry/order, not created_at fields:

- `40f6033` commits 2020 result plus the 2019 frozen single-close-window specification.
- Its descendants `f177fc0` ... `4688320` introduce 2019 monthly receipts.
- `7fd6dcf` commits failed 2019 result plus the distinct ALL 2018 slope specification.
- Its descendants `7cfbd24` ... `ed67a0c` introduce 2018 monthly receipts.
- `ed44360` records the 2018 conclusion/algebra proof.

This establishes preregistration **commit ordering**. Git does not prove there was no earlier off-repository human access; that stronger claim is not independently verifiable.

### Independent arithmetic/accounting

| Study | Events | Valid | Missing exact bars | JST dates | Mean gross points | Wins |
|---|---:|---:|---:|---:|---:|---:|
| 2019 single close-window | 161 | 99 | 62 | 65 | 0.93030303 | 53 |
| 2019 ALL baseline | 5126 | 3503 | 1623 | 293 | -0.17881816 | 1633 |
| 2018 ALL slope/unfiltered | 5940 | 4958 | 982 | 305 | 0.23741428 | 2423 |

The raw replay matches every combined daily count/win/sum (maximum daily sum difference 0.0) for 2019 primary/ALL and both 2018 filtered/unfiltered receipts. Month carry-state and exact entry/target accounting are consistent. Missing events remain missing; no exact bar is imputed.

Independent Python Random(2255200), 10,000 replications gives 2019 primary CI approximately [-2.8842,5.1099] and 2018 ALL [-0.3937,0.8889]. These have the **same negative classification**, but do not exactly reproduce the old stored intervals [-2.9103,5.0836] / [-0.3830,0.8841]. The original proxy execution RNG implementation/code/environment is not preserved. Seed/reps alone do not establish exact computational reproducibility. Historical numbers are **not overwritten**. Independent intervals are explicitly audit-only reconstructions.

### Slope redundancy

For F prior <= S prior:

F_current-S_current = (a_fast-a_slow)*(x-S_prior)+(1-a_fast)*(F_prior-S_prior).

With standard EMA alpha 0<a_slow<a_fast<=1, a strictly positive cross implies x>S_prior, so S_current-S_prior=a_slow*(x-S_prior)>0. Reverse inequalities prove short. The original proof is valid for 5/200; it generalizes to alpha_fast=1 too. This is structural, not a market coincidence. Independent synthetic state enumeration and raw 2018 set identity both pass. Floating precision can blur near-equality for extreme values, so algebra is the mathematical claim; actual consumed-source events were also verified identical.

### Data snooping / adverse preservation

2020 14:45–15:15 was selected after multiple inspected time cuts and is exploratory/multiple-comparison exposed. Its unadjusted best-window interval is not confirmatory. 2019 specifies one candidate; ALL/open/comparator are predeclared context only and do not replace it. 2019 failed. 2018 was a separate ALL mechanism, not close-window rescue; thresholds are in its ancestor specification. No new strategy/window/threshold was adopted in this task.

Original negative result, result table, receipts, interpretation and decision files are unchanged. Read PROCEDURAL_DEVIATION.md: the audit helper's initial 2018 subgroup output exceeded scope, was excluded from admissible evidence, and is explicitly acknowledged. This prevents claiming flawless process compliance.

## RESULT

Synthetic tests, compilation, raw proxy source/accounting and algebra pass. Full test log and executable hashes: TEST_LOG.txt. No actual XM signal/outcome, 2026 count/chart/return or parameter comparison was produced.

Source qualification still PARTIAL_WITH_GAPS; original proxy exact bootstrap provenance still incomplete. Overall audit: **PARTIAL_WITH_GAPS / PRE_XM_HARDENING_IMPLEMENTED**, not a blanket independent scientific PASS.

## DECISION / integration plan

Keep #42/#44/#45/#48 and the new integration PR **draft**. Do not merge merely because GitHub reports mergeability. Original #45's unsafe collector is corrected only in this integration branch; use this branch's complete directory. Prospective merge order, after outstanding independent review: #42 -> #44, then #45 and #48 (both depend on #42/#44 as applicable), then the integrating hardening branch. Alternatively a reviewed merge of the complete integration branch can preserve the two parent histories; explicitly close redundant original PRs only after remote-main verification. Never squash away source preregistration ordering or force push.

If original PRs are merged individually, their transient unsafe collector must not be advertised or run before integrating the correction. Prefer reviewing the complete combined branch and its scientific labels before any publication.

## BLOCKER / NEXT HUMAN ACTION

**WAITING_FOR_XM_STAGE1_DATA**. This Work environment cannot access the user's local XM terminal. Run the revised Stage 1 collector once on Windows and provide its immutable four-file ZIP. Do not provide password/login. Source-time/BID/coverage review may require a subsequent minimal redacted check; Stage 2 event-adjacent local tick collection is a second acquisition stage. Stage 1 alone is not sufficient for Discovery returns.
