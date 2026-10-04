# Remote verification receipt — 2026-10-04

- Integration PR: https://github.com/Josh-Temple/systematic-trading-research/pull/54 — open/draft, GitHub-reported mergeable after computation.
- Code/audit commit: `140110fcae1bce570d7cd5280ee59377d82efc7f`.
- Preserved ordered parents: `ed443608d9b778256ed4f5f5ed7a369871a3ee2f`, `48ede9665b91b308310fee47b97bcfa81c66cdae`.
- Remote tree: `b82e150f617ae8fc683fed581c25c79cd78dcf11`; fresh git fetch/readback exactly matched the local tested index tree, including all artifact bytes.
- Remote main: `a765b33fc0915fdfdcf21287a4418aca4f5b8b7c`, unchanged. No merge performed.
- Synthetic push CI: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37167298472 — SUCCESS.
- Synthetic PR CI: https://github.com/Josh-Temple/systematic-trading-research/actions/runs/37167300295 — SUCCESS.
- PR job logs freshly read: `Ran 46 tests`, `OK`, `success: true`. Job ID 111332803802.
- Local compilation and 46/46 synthetic tests PASS. CI invoked only run_synthetic_tests.py, not historical proxy replay or XM acquisition.
- Original specification and proxy-negative artifact directories have no diff against the inherited exact #48 head.
- PRs #42/#44/#45/#48 remain unmodified draft branches. All original history is preserved; no force update.
- Current state: WAITING_FOR_XM_STAGE1_DATA. Source qualification PARTIAL_WITH_GAPS; Packet C not executed; holdout unopened.
- Remaining scientific/process limits: original proxy exact bootstrap RNG provenance and the explicitly recorded audit-helper scope deviation. See INDEPENDENT_AUDIT.md and PROCEDURAL_DEVIATION.md.

This receipt is an additive documentation commit after the tested code/audit commit; it changes no executable or research parameters.
