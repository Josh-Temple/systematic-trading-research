---
id: DEC-CSM-003-FREEZE-20261001
type: Decision
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: ACCEPTED
decision: FREEZE_SPECIFICATION
human_decision_id: HDEC-CSM-002-20261001
based_on:
  - SPEC-CSM-002-v01
  - HCON-CSM-I1-20261001
  - GATE-CSM-I2-20261001
relations:
  - type: uses_specification
    target: SPEC-CSM-002-v01
  - type: derived_from
    target: DEC-CSM-003
---

# Human acceptance and specification freeze — 2026-10-01

## Human decision receipt

At 2026-10-01T21:35:55+09:00, the current human user replied **「承認します 進めて下さい」** to the direct request to accept SPEC-CSM-002-v01 at SHA-256 `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90`. This receipt binds the acceptance to those exact pre-freeze bytes. The repository-linked GitHub login shown for the current integration PR is `Josh-Temple`; this is an account reference, not a claim about legal identity.

Human decision ID: `HDEC-CSM-002-20261001`.

## Freeze operation and byte identities

| State | Git ref / blob | SHA-256 |
|---|---|---|
| Accepted pre-freeze SPEC | proposal `e0f42a367b0c3cc94df2bc3d5a42d8a36b17e1ff`, blob `a073e77dec14337ee20609ed6136e50a8c1e76e2` | `e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90` |
| Frozen SPEC after metadata receipt | integration commit `4ac1e797c777f33a467ec73b250401886d160e80`, blob `7fe114e2fcfa33b0565b51c717455abd8837d5d9` | `a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2` |

The acceptance covers the exact pre-freeze SPEC bytes above. To record the decision, only frontmatter lifecycle fields were changed: `status` from `HUMAN_BOUNDARY` to `ACTIVE`; `freeze_status` from `PROPOSED_NOT_FROZEN` to `FROZEN`; and new `frozen_at` and `human_decision_ref` fields. The entire body after the frontmatter is byte-for-byte unchanged. Both digests are retained so downstream identities can distinguish the accepted bytes from the metadata-frozen file.

## Decision and boundary

Freeze SPEC-CSM-002-v01 with its approved science choices, including the retrospective latest-vintage reference-to-reference association scope. HYP-CSM-002 remains UNTESTED. This human acceptance does not authorize market-data capture, computation of rankings or outcomes, an experiment run, or an instruction to X.

The I2 gate remains CLOSED. D's config at head `2271ce68039e295aa3cd50b5b2431e1a03d5dfdc` is still pinned to the pre-freeze SPEC blob/SHA-256 above; its config and downstream identities must be refreshed and checked against the post-freeze identity. Independent E audit, full-history/source readiness, exposure disposition, durable access ledger, and trusted receipt/isolation conditions remain unresolved.

The original human brief that preceded this exact proposal was not present in the reviewed repository artifacts. This receipt records only the exact acceptance stated above; it does not reconstruct that missing brief.
