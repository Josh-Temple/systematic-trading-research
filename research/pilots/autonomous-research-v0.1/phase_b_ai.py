"""Host-side Phase B AI-search contract.

This module exposes only protocol-permitted round packets to a researcher callback.
It is not itself a process sandbox. Official runs must execute the researcher in a
separate environment that cannot read repository/generator/hidden-data files.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import phase_b_core
from phase_b_search import PhaseBProtocolError, SearchHost


Researcher = Callable[[dict[str, Any]], dict[str, Any]]


def _candidate_space_view(protocol: dict[str, Any]) -> dict[str, Any]:
    space = protocol["candidate_space"]
    return {
        "sources": list(space["sources"]),
        "transforms": [
            {"name": item["name"], "lags": list(item["lags"])}
            for item in space["transforms"]
        ],
        "operators": list(space["operators"]),
        "thresholds": list(space["thresholds"]),
        "sides": list(space["sides"]),
        "position_sizes": list(space["position_sizes"]),
        "strategy_count": int(space["strategy_count"]),
    }


def make_round_packet(
    *,
    world_id: str,
    round_number: int,
    remaining_budget: int,
    prior_feedback: list[dict[str, Any]],
) -> dict[str, Any]:
    protocol = phase_b_core.load_protocol()
    return {
        "protocol_id": protocol["protocol_id"],
        "world_id": world_id,
        "round": round_number,
        "rounds_total": int(protocol["search"]["rounds"]),
        "remaining_budget": remaining_budget,
        "max_proposals_this_round": int(
            protocol["search"]["max_proposals_per_round"]
        ),
        "candidate_space": _candidate_space_view(protocol),
        "prior_feedback": list(prior_feedback),
        "feedback_fields": list(protocol["feedback"]["fields"]),
        "final_selection": dict(protocol["final_selection"]),
        "forbidden": {
            "market_data": True,
            "raw_adaptive_outcomes": True,
            "final_outcomes_before_close": True,
            "hidden_seed": True,
            "repository_or_generator_access": True,
            "arbitrary_candidate_code": True,
        },
        "response_contract": {
            "type": "object",
            "keys": ["stop", "proposals"],
            "max_proposals": int(protocol["search"]["max_proposals_per_round"]),
        },
    }


def _parse_response(response: Any, max_proposals: int) -> tuple[bool, list[dict[str, Any]]]:
    if not isinstance(response, dict):
        raise PhaseBProtocolError("researcher response must be an object")
    if set(response) != {"stop", "proposals"}:
        raise PhaseBProtocolError("researcher response keys must be stop/proposals")
    if not isinstance(response["stop"], bool):
        raise PhaseBProtocolError("researcher stop must be boolean")
    proposals = response["proposals"]
    if not isinstance(proposals, list):
        raise PhaseBProtocolError("researcher proposals must be a list")
    if len(proposals) > max_proposals:
        raise PhaseBProtocolError("researcher exceeded per-round proposal limit")
    if any(not isinstance(candidate, dict) for candidate in proposals):
        raise PhaseBProtocolError("every proposal must be a JSON object")
    return response["stop"], proposals


def run_ai_search(
    *,
    world: phase_b_core.HiddenWorld,
    run_id: str,
    ledger_path: str | Path,
    checkpoint_key: bytes,
    researcher: Researcher,
) -> dict[str, Any]:
    """Run one AI method/world under the frozen host accounting.

    The callback receives only make_round_packet() output. It must be backed by a
    clean external model process for an official run.
    """
    protocol = phase_b_core.load_protocol()
    rounds = int(protocol["search"]["rounds"])
    max_per_round = int(protocol["search"]["max_proposals_per_round"])

    host = SearchHost(
        run_id=run_id,
        method="AI",
        world=world,
        ledger_path=ledger_path,
        checkpoint_key=checkpoint_key,
    )

    prior_feedback: list[dict[str, Any]] = []
    round_packets: list[dict[str, Any]] = []

    for round_number in range(1, rounds + 1):
        remaining = host.max_submissions - host.submission_count
        packet = make_round_packet(
            world_id=world.world_id,
            round_number=round_number,
            remaining_budget=remaining,
            prior_feedback=prior_feedback,
        )
        round_packets.append(packet)

        try:
            stop, proposals = _parse_response(
                researcher(packet),
                max_proposals=max_per_round,
            )
        except PhaseBProtocolError:
            host.close_round(round_number, reason="MALFORMED_RESEARCHER_RESPONSE")
            for later in range(round_number + 1, rounds + 1):
                host.close_round(later, reason="RESEARCHER_STOPPED_AFTER_MALFORMED_RESPONSE")
            break

        for candidate in proposals:
            feedback = host.submit(
                round_number=round_number,
                candidate=candidate,
            ).as_dict()
            prior_feedback.append(
                {
                    "round": round_number,
                    "submission_index": host.submission_count,
                    **feedback,
                }
            )

        reason = "RESEARCHER_STOP" if stop else "COMPLETE"
        host.close_round(round_number, reason=reason)

        if stop:
            for later in range(round_number + 1, rounds + 1):
                host.close_round(later, reason="RESEARCHER_STOPPED")
            break

    summary = host.finalize()
    return {
        "summary": summary,
        "researcher_visible_round_packets": round_packets,
        "researcher_feedback_history": prior_feedback,
    }
