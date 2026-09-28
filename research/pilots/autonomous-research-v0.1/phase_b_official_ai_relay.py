"""Official Phase B clean-researcher relay.

Synthetic only. This module binds the frozen AI run family to the exact host
state used by the completed official non-AI baselines, while exposing only the
frozen researcher instruction, round packets, and permitted adaptive feedback.

It deliberately has no input for the baseline-result artifact.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any, Callable

import evaluator
import phase_b_ai
import phase_b_core
import phase_b_official_baselines as official_baselines
import phase_b_run_manifest

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
MANIFEST_PATH = HERE / "RUN_MANIFEST_PHASE_B_AI_v0.1.json"
BINDING_PATH = HERE / "PHASE_B_AI_HOST_BINDING_v0.1.json"
INSTRUCTION_PATH = HERE / "PHASE_B_AI_RESEARCHER_INSTRUCTION_v0.1.md"
MAX_RESPONSE_BYTES = 64 * 1024


class OfficialAIRelayError(RuntimeError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OfficialAIRelayError(f"{Path(path).name} must contain a JSON object")
    return value


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise OfficialAIRelayError(f"duplicate researcher-response key: {key}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise OfficialAIRelayError(
        f"non-standard researcher-response JSON constant is forbidden: {value}"
    )


def parse_researcher_response(text: str) -> dict[str, Any]:
    if not isinstance(text, str):
        raise OfficialAIRelayError("researcher response must be text")
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise OfficialAIRelayError("researcher response must be valid UTF-8") from exc
    if len(encoded) > MAX_RESPONSE_BYTES:
        raise OfficialAIRelayError("researcher response exceeds relay byte limit")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except OfficialAIRelayError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError, RecursionError) as exc:
        raise OfficialAIRelayError("researcher response is not strict JSON") from exc
    if not isinstance(value, dict):
        raise OfficialAIRelayError("researcher response root must be an object")
    return value


def validate_binding(
    binding: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    required = {
        "binding_id",
        "status",
        "run_family_id",
        "protocol_id",
        "amendment_id",
        "baseline_workflow_run_id",
        "baseline_execution_commit",
        "host_state_artifact",
        "host_state_hash",
        "forbidden_baseline_result_artifact",
        "world_ids",
        "market_data_allowed",
        "baseline_result_visibility_to_researcher",
        "host_state_visibility_to_researcher",
    }
    missing = required - set(binding)
    if missing:
        raise OfficialAIRelayError(f"host binding missing fields: {sorted(missing)}")
    if binding["binding_id"] != "ARP-B-AI-HOST-BIND-v0.1":
        raise OfficialAIRelayError("unexpected host binding id")
    if binding["status"] != "FROZEN_BEFORE_AI_RESULTS":
        raise OfficialAIRelayError("host binding is not frozen before AI results")
    if binding["run_family_id"] != manifest["run_family_id"]:
        raise OfficialAIRelayError("host binding run family mismatch")
    if binding["protocol_id"] != manifest["protocol_id"]:
        raise OfficialAIRelayError("host binding protocol mismatch")
    if binding["world_ids"] != manifest["world_ids"]:
        raise OfficialAIRelayError("host binding world ids mismatch")
    if binding["market_data_allowed"] is not False:
        raise OfficialAIRelayError("market data must remain forbidden")
    if binding["baseline_result_visibility_to_researcher"] is not False:
        raise OfficialAIRelayError("baseline result visibility must remain false")
    if binding["host_state_visibility_to_researcher"] is not False:
        raise OfficialAIRelayError("host state visibility must remain false")

    host_artifact = binding["host_state_artifact"]
    forbidden_result = binding["forbidden_baseline_result_artifact"]
    for label, item in (
        ("host_state_artifact", host_artifact),
        ("forbidden_baseline_result_artifact", forbidden_result),
    ):
        if not isinstance(item, dict):
            raise OfficialAIRelayError(f"{label} must be an object")
        if set(item) != {"id", "name", "digest"}:
            raise OfficialAIRelayError(f"{label} fields are invalid")
        if isinstance(item["id"], bool) or not isinstance(item["id"], int):
            raise OfficialAIRelayError(f"{label}.id must be an integer")
        if not isinstance(item["name"], str) or not item["name"]:
            raise OfficialAIRelayError(f"{label}.name must be non-empty")
        if (
            not isinstance(item["digest"], str)
            or not item["digest"].startswith("sha256:")
            or len(item["digest"]) != 71
        ):
            raise OfficialAIRelayError(f"{label}.digest must be sha256 metadata")

    host_hash = binding["host_state_hash"]
    if not isinstance(host_hash, str) or len(host_hash) != 64:
        raise OfficialAIRelayError("host_state_hash must be SHA-256 hex")


def validate_host_inputs(
    *,
    host_state: dict[str, Any],
    commitments: dict[str, Any],
    binding: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    official_baselines.validate_frozen_protocol()
    phase_b_run_manifest.validate_manifest(manifest, root=REPO_ROOT)
    validate_binding(binding, manifest)

    if official_baselines.sha256_json(host_state) != binding["host_state_hash"]:
        raise OfficialAIRelayError("host state hash does not match frozen binding")
    expected_commitments = official_baselines.public_commitments(host_state)
    if commitments != expected_commitments:
        raise OfficialAIRelayError("commitments do not exactly bind supplied host state")
    if commitments["host_state_hash"] != binding["host_state_hash"]:
        raise OfficialAIRelayError("commitment host-state hash mismatch")
    if host_state.get("protocol_id") != manifest["protocol_id"]:
        raise OfficialAIRelayError("host state protocol mismatch")
    if host_state.get("amendment_id") != binding["amendment_id"]:
        raise OfficialAIRelayError("host state amendment mismatch")

    checkpoint_hex = host_state.get("checkpoint_key_hex")
    if not isinstance(checkpoint_hex, str):
        raise OfficialAIRelayError("checkpoint key is missing")
    try:
        checkpoint_key = bytes.fromhex(checkpoint_hex)
    except ValueError as exc:
        raise OfficialAIRelayError("checkpoint key is not valid hex") from exc
    if len(checkpoint_key) != 32:
        raise OfficialAIRelayError("checkpoint key must be exactly 32 bytes")

    worlds = host_state.get("worlds")
    if not isinstance(worlds, list) or len(worlds) != len(manifest["world_ids"]):
        raise OfficialAIRelayError("host state world count mismatch")
    by_id = {item.get("world_id"): item for item in worlds if isinstance(item, dict)}
    if list(by_id) != manifest["world_ids"]:
        raise OfficialAIRelayError("host state world ordering/identity mismatch")

    expected_archetypes = dict(official_baselines.OFFICIAL_WORLD_SPECS)
    for world_id in manifest["world_ids"]:
        item = by_id[world_id]
        if item.get("archetype") != expected_archetypes[world_id]:
            raise OfficialAIRelayError(f"archetype mismatch for {world_id}")
        seed_hex = item.get("seed_hex")
        if not isinstance(seed_hex, str):
            raise OfficialAIRelayError(f"seed missing for {world_id}")
        try:
            seed = bytes.fromhex(seed_hex)
        except ValueError as exc:
            raise OfficialAIRelayError(f"invalid seed hex for {world_id}") from exc
        if len(seed) != 32:
            raise OfficialAIRelayError(f"seed length mismatch for {world_id}")
        if phase_b_core.seed_commitment(seed) != item.get("seed_commitment"):
            raise OfficialAIRelayError(f"seed commitment mismatch for {world_id}")


def _write_json(path: Path, value: Any, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value) + b"\n")
    os.chmod(path, mode)


def _safe_status(
    *,
    manifest: dict[str, Any],
    binding: dict[str, Any],
    state: str,
    completed_worlds: list[str],
    current_world: str | None = None,
    error_type: str | None = None,
) -> dict[str, Any]:
    return {
        "status_version": "0.1",
        "run_family_id": manifest["run_family_id"],
        "protocol_id": manifest["protocol_id"],
        "model_provider": manifest["model_provider"],
        "model_identity": manifest["model_identity"],
        "researcher_execution_boundary": manifest["researcher_execution_boundary"],
        "host_binding_id": binding["binding_id"],
        "baseline_workflow_run_id": binding["baseline_workflow_run_id"],
        "host_state_hash": binding["host_state_hash"],
        "state": state,
        "completed_worlds": list(completed_worlds),
        "current_world": current_world,
        "error_type": error_type,
        "metric_values_exposed": False,
        "baseline_results_read": False,
        "market_data_used": False,
    }


def prepare_output_root(
    *,
    output_root: str | Path,
    manifest: dict[str, Any],
    binding: dict[str, Any],
) -> Path:
    root = Path(output_root)
    if root.exists():
        raise OfficialAIRelayError(
            "output root already exists; official relay is fail-closed against restart"
        )
    root.mkdir(parents=True)
    (root / "private").mkdir()
    exchange = root / "researcher_exchange"
    exchange.mkdir()
    shutil.copyfile(INSTRUCTION_PATH, exchange / "PHASE_B_AI_RESEARCHER_INSTRUCTION_v0.1.md")
    _write_json(
        exchange / "BOOTSTRAP.json",
        {
            "run_family_id": manifest["run_family_id"],
            "protocol_id": manifest["protocol_id"],
            "model_provider": manifest["model_provider"],
            "model_identity": manifest["model_identity"],
            "researcher_execution_boundary": manifest["researcher_execution_boundary"],
            "researcher_instruction_sha256": manifest["researcher_instruction_sha256"],
            "world_ids": manifest["world_ids"],
            "search_budget": manifest["search_budget"],
            "feedback_schema": manifest["feedback_schema"],
            "market_data_allowed": False,
        },
        mode=0o644,
    )
    _write_json(
        root / "public" / "session_status.json",
        _safe_status(
            manifest=manifest,
            binding=binding,
            state="STARTED",
            completed_worlds=[],
        ),
        mode=0o644,
    )
    return root


def run_official_ai_session(
    *,
    host_state: dict[str, Any],
    commitments: dict[str, Any],
    output_root: str | Path,
    researcher: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
    binding = load_json(BINDING_PATH)
    validate_host_inputs(
        host_state=host_state,
        commitments=commitments,
        binding=binding,
        manifest=manifest,
    )
    root = prepare_output_root(
        output_root=output_root,
        manifest=manifest,
        binding=binding,
    )

    checkpoint_key = bytes.fromhex(host_state["checkpoint_key_hex"])
    by_id = {item["world_id"]: item for item in host_state["worlds"]}
    completed: list[str] = []
    private_summaries: list[dict[str, Any]] = []

    try:
        for world_id in manifest["world_ids"]:
            _write_json(
                root / "public" / "session_status.json",
                _safe_status(
                    manifest=manifest,
                    binding=binding,
                    state="WORLD_IN_PROGRESS",
                    completed_worlds=completed,
                    current_world=world_id,
                ),
                mode=0o644,
            )

            item = by_id[world_id]
            world = phase_b_core.generate_world(
                world_id=world_id,
                archetype=item["archetype"],
                seed=bytes.fromhex(item["seed_hex"]),
            )
            ledger_path = root / "private" / "ledgers" / f"{world_id}.jsonl"
            result = phase_b_ai.run_ai_search(
                world=world,
                run_id=f"{manifest['run_family_id']}:{world_id}:AI",
                ledger_path=ledger_path,
                checkpoint_key=checkpoint_key,
                researcher=researcher,
            )
            evaluator.verify_ledger_checkpoint(
                ledger_path,
                result["summary"]["ledger_checkpoint"],
                checkpoint_key,
            )
            _write_json(
                root / "private" / "results" / f"{world_id}.json",
                result["summary"],
            )
            private_summaries.append(result["summary"])
            completed.append(world_id)

        _write_json(
            root / "private" / "official_ai_summaries.json",
            {
                "run_family_id": manifest["run_family_id"],
                "protocol_id": manifest["protocol_id"],
                "host_binding_id": binding["binding_id"],
                "world_summaries": private_summaries,
            },
        )
        status = _safe_status(
            manifest=manifest,
            binding=binding,
            state="COMPLETE_PENDING_COMPARISON",
            completed_worlds=completed,
        )
        _write_json(
            root / "public" / "session_status.json",
            status,
            mode=0o644,
        )
        return status
    except Exception as exc:
        status = _safe_status(
            manifest=manifest,
            binding=binding,
            state="HALTED_FAIL_CLOSED",
            completed_worlds=completed,
            current_world=(
                manifest["world_ids"][len(completed)]
                if len(completed) < len(manifest["world_ids"])
                else None
            ),
            error_type=type(exc).__name__,
        )
        _write_json(
            root / "public" / "session_status.json",
            status,
            mode=0o644,
        )
        raise


def make_interactive_researcher(exchange_root: Path) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def researcher(packet: dict[str, Any]) -> dict[str, Any]:
        world_id = packet["world_id"]
        round_number = int(packet["round"])
        world_dir = exchange_root / world_id
        packet_path = world_dir / f"round-{round_number:02d}-packet.json"
        response_path = world_dir / f"round-{round_number:02d}-response.json"
        _write_json(packet_path, packet, mode=0o644)

        print(
            json.dumps(
                {
                    "relay": "ROUND_PACKET_READY",
                    "world_id": world_id,
                    "round": round_number,
                    "packet_path": str(packet_path),
                },
                sort_keys=True,
            )
        )
        print(canonical_json(packet).decode("utf-8"))
        print("PASTE_RESEARCHER_RESPONSE_JSON; finish with a line containing END_RESPONSE")

        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError as exc:
                raise OfficialAIRelayError(
                    "operator input ended before END_RESPONSE"
                ) from exc
            if line == "END_RESPONSE":
                break
            lines.append(line)

        response = parse_researcher_response("\n".join(lines))
        _write_json(response_path, response, mode=0o644)
        return response

    return researcher


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-state", required=True)
    parser.add_argument("--commitments", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--researcher-model", required=True)
    parser.add_argument(
        "--confirm-clean-boundary",
        action="store_true",
        help="Operator attests that the researcher has no repository/host/baseline-result access.",
    )
    args = parser.parse_args()

    manifest = phase_b_run_manifest.load_manifest(MANIFEST_PATH)
    if args.researcher_model != manifest["model_identity"]:
        raise OfficialAIRelayError("researcher model does not match frozen manifest")
    if not args.confirm_clean_boundary:
        raise OfficialAIRelayError("clean researcher boundary attestation is required")

    host_state = load_json(args.host_state)
    commitments = load_json(args.commitments)

    # Validate before creating any output or researcher-visible packet.
    binding = load_json(BINDING_PATH)
    validate_host_inputs(
        host_state=host_state,
        commitments=commitments,
        binding=binding,
        manifest=manifest,
    )

    root = Path(args.output_root)
    researcher = make_interactive_researcher(
        root / "researcher_exchange"
    )
    status = run_official_ai_session(
        host_state=host_state,
        commitments=commitments,
        output_root=root,
        researcher=researcher,
    )
    print(
        json.dumps(
            {
                "relay": "COMPLETE",
                "run_family_id": status["run_family_id"],
                "completed_worlds": status["completed_worlds"],
                "metric_values_exposed": False,
                "baseline_results_read": False,
                "market_data_used": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
