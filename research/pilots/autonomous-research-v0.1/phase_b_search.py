"""Phase B host-controlled search accounting and one-shot final selection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import evaluator
import phase_b_core


class PhaseBProtocolError(RuntimeError):
    pass


@dataclass(frozen=True)
class SubmissionFeedback:
    candidate_id: str | None
    validity_status: str
    duplicate: bool
    adaptive_mean_return: float | None
    coarse_rejection_reason: str | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "validity_status": self.validity_status,
            "duplicate": self.duplicate,
            "adaptive_mean_return": self.adaptive_mean_return,
            "coarse_rejection_reason": self.coarse_rejection_reason,
        }


def _coarse_reason(receipt: dict[str, Any]) -> str | None:
    status = receipt["validity_status"]
    if status == "DUPLICATE":
        return "DUPLICATE"
    if status == "VALID":
        return None
    diagnostics = receipt.get("diagnostics") or []
    if status == "INVALID":
        return "INVALID_CANDIDATE"
    if receipt.get("execution_status") == "FAILED":
        return "EVALUATOR_FAILURE"
    return "UNVERIFIED"


def select_best_record(records: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [
        r
        for r in records
        if r["validity_status"] == "VALID"
        and r["adaptive_mean_return"] is not None
        and r["strategy_fingerprint"]
    ]
    if not eligible:
        raise PhaseBProtocolError("no valid candidate available for final selection")
    return sorted(
        eligible,
        key=lambda r: (-r["adaptive_mean_return"], r["strategy_fingerprint"]),
    )[0]


class SearchHost:
    def __init__(
        self,
        *,
        run_id: str,
        method: str,
        world: phase_b_core.HiddenWorld,
        ledger_path: str | Path,
        checkpoint_key: bytes,
    ) -> None:
        protocol = phase_b_core.load_protocol()
        self.run_id = run_id
        self.method = method
        self.world = world
        self.ledger_path = Path(ledger_path)
        self.checkpoint_key = checkpoint_key
        self.max_submissions = int(protocol["search"]["submissions_per_world_method"])
        self.rounds = int(protocol["search"]["rounds"])
        self.max_per_round = int(protocol["search"]["max_proposals_per_round"])
        self._round_counts = {i: 0 for i in range(1, self.rounds + 1)}
        self._closed_rounds: set[int] = set()
        self._known_fingerprints: set[str] = set()
        self._records: list[dict[str, Any]] = []
        self._finalized = False

        evaluator.append_ledger(
            self.ledger_path,
            {
                "kind": "RUN_START",
                "run_id": self.run_id,
                "world_id": self.world.world_id,
                "method": self.method,
                "protocol_id": protocol["protocol_id"],
                "seed_commitment": self.world.seed_commitment,
                "generator_version": self.world.generator_version,
                "adaptive_dataset_hash": phase_b_core.dataset_hash(
                    self.world.adaptive_rows
                ),
                "final_dataset_hash_commitment": phase_b_core.dataset_hash(
                    self.world.final_rows
                ),
            },
        )

    @property
    def submission_count(self) -> int:
        return len(self._records)

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._records)

    def submit(
        self,
        *,
        round_number: int,
        candidate: dict[str, Any],
    ) -> SubmissionFeedback:
        if self._finalized:
            raise PhaseBProtocolError("run already finalized")
        if round_number not in self._round_counts:
            raise PhaseBProtocolError("round out of range")
        if round_number in self._closed_rounds:
            raise PhaseBProtocolError("round already closed")
        if self._round_counts[round_number] >= self.max_per_round:
            raise PhaseBProtocolError("round proposal limit exceeded")
        if self.submission_count >= self.max_submissions:
            raise PhaseBProtocolError("search budget exhausted")

        self._round_counts[round_number] += 1
        submission_index = self.submission_count + 1

        receipt = phase_b_core.evaluate_on_adaptive(
            self.world,
            candidate,
            known_strategy_fingerprints=self._known_fingerprints,
        )
        fingerprint = receipt.get("strategy_fingerprint")
        if fingerprint and fingerprint not in self._known_fingerprints:
            self._known_fingerprints.add(fingerprint)

        score = None
        if receipt["validity_status"] == "VALID":
            score = float(receipt["metrics"]["mean_return"])

        record = {
            "run_id": self.run_id,
            "world_id": self.world.world_id,
            "method": self.method,
            "round": round_number,
            "submission_index": submission_index,
            "candidate": candidate,
            "candidate_id": receipt.get("candidate_id"),
            "candidate_hash": receipt.get("candidate_hash"),
            "strategy_fingerprint": fingerprint,
            "validity_status": receipt["validity_status"],
            "duplicate": receipt["validity_status"] == "DUPLICATE",
            "adaptive_mean_return": score,
            "adaptive_dataset_id": receipt["dataset_id"],
            "adaptive_dataset_hash": receipt["dataset_hash"],
            "evaluator_identity": receipt["evaluator_identity"],
            "diagnostics": receipt.get("diagnostics", []),
        }
        self._records.append(record)

        evaluator.append_ledger(
            self.ledger_path,
            {
                "kind": "SUBMISSION",
                **{k: v for k, v in record.items() if k != "candidate"},
            },
        )

        return SubmissionFeedback(
            candidate_id=record["candidate_id"],
            validity_status=record["validity_status"],
            duplicate=record["duplicate"],
            adaptive_mean_return=score,
            coarse_rejection_reason=_coarse_reason(receipt),
        )

    def close_round(self, round_number: int, reason: str = "COMPLETE") -> None:
        if self._finalized:
            raise PhaseBProtocolError("run already finalized")
        if round_number not in self._round_counts:
            raise PhaseBProtocolError("round out of range")
        if round_number in self._closed_rounds:
            raise PhaseBProtocolError("round already closed")
        if any(r < round_number and r not in self._closed_rounds for r in self._round_counts):
            raise PhaseBProtocolError("rounds must close in order")
        self._closed_rounds.add(round_number)
        evaluator.append_ledger(
            self.ledger_path,
            {
                "kind": "ROUND_CLOSE",
                "run_id": self.run_id,
                "world_id": self.world.world_id,
                "method": self.method,
                "round": round_number,
                "submitted": self._round_counts[round_number],
                "reason": reason,
            },
        )

    def best_adaptive_record(self) -> dict[str, Any]:
        return select_best_record(self._records)

    def finalize(self) -> dict[str, Any]:
        if self._finalized:
            raise PhaseBProtocolError("final holdout already evaluated")
        if len(self._closed_rounds) != self.rounds:
            raise PhaseBProtocolError("all four rounds must close before final evaluation")

        selected = self.best_adaptive_record()
        final_receipt = phase_b_core.evaluate_on_final(
            self.world,
            selected["candidate"],
        )
        if final_receipt["validity_status"] != "VALID":
            raise PhaseBProtocolError("selected candidate became invalid on final dataset")

        final_score = float(final_receipt["metrics"]["mean_return"])
        evaluator.append_ledger(
            self.ledger_path,
            {
                "kind": "FINAL_EVALUATION",
                "run_id": self.run_id,
                "world_id": self.world.world_id,
                "method": self.method,
                "selected_candidate_id": selected["candidate_id"],
                "selected_candidate_hash": selected["candidate_hash"],
                "selected_strategy_fingerprint": selected["strategy_fingerprint"],
                "adaptive_mean_return": selected["adaptive_mean_return"],
                "final_mean_return": final_score,
                "final_dataset_id": final_receipt["dataset_id"],
                "final_dataset_hash": final_receipt["dataset_hash"],
                "evaluator_identity": final_receipt["evaluator_identity"],
            },
        )

        checkpoint = evaluator.create_ledger_checkpoint(
            self.ledger_path,
            self.checkpoint_key,
        )
        self._finalized = True

        return {
            "run_id": self.run_id,
            "world_id": self.world.world_id,
            "method": self.method,
            "submitted_count": self.submission_count,
            "valid_count": sum(
                1 for r in self._records if r["validity_status"] == "VALID"
            ),
            "invalid_count": sum(
                1 for r in self._records if r["validity_status"] == "INVALID"
            ),
            "duplicate_count": sum(1 for r in self._records if r["duplicate"]),
            "selected_candidate_id": selected["candidate_id"],
            "selected_strategy_fingerprint": selected["strategy_fingerprint"],
            "best_adaptive_mean_return": selected["adaptive_mean_return"],
            "final_mean_return": final_score,
            "adaptive_to_final_degradation": (
                selected["adaptive_mean_return"] - final_score
            ),
            "ledger_checkpoint": checkpoint,
        }
