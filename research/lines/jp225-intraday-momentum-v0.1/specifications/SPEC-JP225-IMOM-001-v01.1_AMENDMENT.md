---
id: SPEC-JP225-IMOM-001-v01.1
type: SpecificationAmendment
research_line_id: RL-JP225-IMOM-001
created_at: 2026-10-04
status: FROZEN_PRE_OUTCOME
market_outcome_access: false
amends: SPEC-JP225-IMOM-001-v01
---

# Pre-outcome hardening amendment v0.1.1

This amendment was created before any JPX/DataCube market outcome was acquired or inspected.

It does not change the hypothesis, clock boundaries, contract rule, samples, bootstrap rules or advancement thresholds.

It only hardens source identity and holdout gating.

## A. Confirmation input

The one-shot confirmation runner must consume a mapped-price-point envelope, not precomputed returns or precomputed strategy P&L.

Required envelope identity:

- version = `JP225_IMOM_MAPPED_POINTS_v1`;
- sample = `2025_CONFIRMATION`;
- `source_manifest_sha256` = externally pinned source-manifest hash;
- rows contain only date/previous_date/contract and the four mapped transaction prices.

The runner recomputes early return, late return, trade sign and signed points internally.

The source-manifest hash is supplied to the runner independently of the input file and must match both the gate binding and the envelope after the gate opens.

## B. Confirmation gate

Before opening/parsing the mapped price rows, the runner must verify an exact expected SHA-256 for the independent confirmation gate.

The gate must bind:

- specification-bundle identity;
- implementation-code identity;
- mapped-input file identity;
- source-manifest identity.

The expected mapped-input SHA-256 and source-manifest SHA-256 must be supplied independently of the gate. The runner validates the gate against those expected identities **before opening the mapped input file**. Only after the gate passes and sample consumption is reserved may the runner hash and parse the mapped input.

No value may be sourced from the gate and then used to validate that same gate.

## C. Sample consumption

A consumed marker is written before mapped price rows are parsed.

A pre-existing output directory is rejected before consumption is reserved.

After consumption starts, malformed/tampered input is a failed consumed run and requires an explicit recovery decision; it is not silently rerunnable.

## D. Degenerate inference

If the full-sample regression has zero predictor variance, or more than 1% of beta-bootstrap replications are invalid because of zero sampled predictor variance:

- diagnostic status = `BOOTSTRAP_DEGENERATE`;
- advancement = false;
- terminal 2025 classification = `IMOM_NOT_SUPPORTED_2025`.

This does not authorize a modified bootstrap or threshold.

## E. 2026 holdout independent review

The 2026 reader must not be invoked from the confirmation decision alone.

Unlock requires both:

1. exact confirmation-decision SHA-256 with `IMOM_ADVANCE_TO_2026_HOLDOUT`; and
2. a separate independently authored review receipt whose exact SHA-256 is pinned and whose binding exactly matches the decision binding and decision SHA.

The review receipt must state:

- status = PASS;
- independent_review = PASS;
- scope = `2026_HOLDOUT_UNLOCK`;
- sample = `2025_CONFIRMATION`.

If either receipt fails, the holdout reader is not called.
