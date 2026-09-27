"""Validation helpers for the frozen Phase B AI RUN_MANIFEST."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import phase_b_core


_SHA40 = re.compile(r"^[0-9a-f]{40}$")


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_manifest(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, Any], *, root: str | Path) -> None:
    protocol = phase_b_core.load_protocol()
    required = {
        "run_family_id",
        "status",
        "model_provider",
        "model_identity",
        "researcher_instruction_path",
        "researcher_instruction_sha256",
        "candidate_space_reference",
        "protocol_id",
        "protocol_commit",
        "evaluator_commit",
        "world_ids",
        "search_budget",
        "feedback_schema",
    }
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"manifest missing fields: {sorted(missing)}")

    for key in ("run_family_id", "model_provider", "model_identity"):
        value = manifest[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be non-empty")

    if manifest["status"] != "FROZEN_BEFORE_AI_RESULTS":
        raise ValueError("manifest status must be FROZEN_BEFORE_AI_RESULTS")
    if manifest["protocol_id"] != protocol["protocol_id"]:
        raise ValueError("protocol_id mismatch")
    if not _SHA40.fullmatch(str(manifest["protocol_commit"])):
        raise ValueError("protocol_commit must be a 40-char lowercase SHA")
    if not _SHA40.fullmatch(str(manifest["evaluator_commit"])):
        raise ValueError("evaluator_commit must be a 40-char lowercase SHA")

    world_ids = manifest["world_ids"]
    if not isinstance(world_ids, list) or len(world_ids) != 6 or len(set(world_ids)) != 6:
        raise ValueError("world_ids must contain six unique IDs")

    expected_budget = {
        "submissions_per_world_method": int(
            protocol["search"]["submissions_per_world_method"]
        ),
        "rounds": int(protocol["search"]["rounds"]),
        "max_proposals_per_round": int(
            protocol["search"]["max_proposals_per_round"]
        ),
    }
    if manifest["search_budget"] != expected_budget:
        raise ValueError("search_budget does not match frozen protocol")

    if manifest["feedback_schema"] != protocol["feedback"]["fields"]:
        raise ValueError("feedback_schema does not match frozen protocol")

    instruction = Path(root) / manifest["researcher_instruction_path"]
    if not instruction.is_file():
        raise ValueError("researcher instruction file not found")
    if sha256_file(instruction) != manifest["researcher_instruction_sha256"]:
        raise ValueError("researcher instruction hash mismatch")
