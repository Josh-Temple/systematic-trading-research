#!/usr/bin/env python3
"""Validate Horizontal Reaction research records and the derived Web projection.

This validator checks structural integrity and projection freshness only.
A passing run is not evidence of scientific validity or computational reproducibility.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
LINE = ROOT / "research" / "lines" / "horizontal-reaction-v0.1"
WEB_DATA = ROOT / "web" / "data" / "horizontal-reaction-v0.1.js"

ENTITY_PATHS = [
    LINE / "LINE.md",
    *(LINE / "hypotheses").glob("*"),
    *(LINE / "specifications").glob("*"),
    *(LINE / "datasets").glob("*"),
    *(LINE / "experiments").glob("*"),
    *(LINE / "runs").glob("*"),
    *(LINE / "results").glob("*"),
    *(LINE / "interpretations").glob("*"),
    *(LINE / "decisions").glob("*"),
    *(LINE / "diagnostics").glob("*"),
]

FRESHNESS_PATHS = [
    "research/lines/horizontal-reaction-v0.1/LINE.md",
    "research/lines/horizontal-reaction-v0.1/CURRENT.md",
    "research/lines/horizontal-reaction-v0.1/hypotheses",
    "research/lines/horizontal-reaction-v0.1/specifications",
    "research/lines/horizontal-reaction-v0.1/datasets",
    "research/lines/horizontal-reaction-v0.1/experiments",
    "research/lines/horizontal-reaction-v0.1/runs",
    "research/lines/horizontal-reaction-v0.1/results",
    "research/lines/horizontal-reaction-v0.1/interpretations",
    "research/lines/horizontal-reaction-v0.1/decisions",
    "research/lines/horizontal-reaction-v0.1/diagnostics",
]

REFERENCE_FIELDS = {
    "run_id",
    "experiment_id",
    "specification_id",
    "tests_hypothesis",
    "uses_specification",
    "target_run",
}
REFERENCE_LIST_FIELDS = {
    "interprets_results",
    "based_on",
    "diagnostic_refs",
    "derived_from_decisions",
    "derived_from_interpretations",
}


class ValidationFailure(Exception):
    pass


def md_frontmatter(text: str, path: Path) -> dict[str, Any] | None:
    if not text.startswith("---\n"):
        return None
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.S)
    if not match:
        raise ValidationFailure(f"{path}: malformed YAML front matter")
    value = yaml.safe_load(match.group(1))
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: YAML front matter is not an object")
    return value


def read_record(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
        return None
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        return md_frontmatter(text, path)
    value = yaml.safe_load(text)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: YAML document is not an object")
    return value


def record_id(record: dict[str, Any]) -> str | None:
    for key in ("id", "run_id", "diagnostic_id"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def collect_records() -> tuple[dict[str, tuple[Path, dict[str, Any]]], list[str]]:
    registry: dict[str, tuple[Path, dict[str, Any]]] = {}
    errors: list[str] = []
    for path in sorted(set(ENTITY_PATHS)):
        try:
            record = read_record(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: YAML parse failure: {exc}")
            continue
        if record is None:
            continue
        rid = record_id(record)
        if not rid:
            errors.append(f"{path.relative_to(ROOT)}: no id/run_id/diagnostic_id")
            continue
        if rid in registry:
            first = registry[rid][0].relative_to(ROOT)
            errors.append(f"duplicate entity id {rid}: {first} and {path.relative_to(ROOT)}")
            continue
        registry[rid] = (path, record)
    return registry, errors


def is_local_id(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and "://" not in value
        and value not in {"UNKNOWN", "UNVERIFIED", "NOT_APPLICABLE", "NONE"}
    )


def iter_references(record: dict[str, Any]):
    for relation in record.get("relations") or []:
        if isinstance(relation, dict) and is_local_id(relation.get("target")):
            yield "relations.target", relation["target"]

    for key in REFERENCE_FIELDS:
        value = record.get(key)
        if is_local_id(value):
            yield key, value

    for key in REFERENCE_LIST_FIELDS:
        values = record.get(key) or []
        if isinstance(values, list):
            for value in values:
                if is_local_id(value):
                    yield key, value

    for key in ("dataset_uses", "planned_dataset_uses"):
        values = record.get(key) or []
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict) and is_local_id(item.get("dataset_id")):
                    yield f"{key}.dataset_id", item["dataset_id"]


def validate_references(registry: dict[str, tuple[Path, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    known = set(registry)
    for rid, (path, record) in registry.items():
        for field, target in iter_references(record):
            if target not in known:
                errors.append(
                    f"{path.relative_to(ROOT)} ({rid}): {field} references missing id {target}"
                )
    return errors


def validate_result_statuses(registry: dict[str, tuple[Path, dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    required = ("execution_status", "evidence_validity", "scientific_status")
    for rid, (path, record) in registry.items():
        if record.get("type") != "Result":
            continue
        missing = [key for key in required if key not in record]
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)} ({rid}): Result missing independent status fields {missing}"
            )
    return errors


def get_record(registry: dict[str, tuple[Path, dict[str, Any]]], rid: str) -> dict[str, Any]:
    if rid not in registry:
        raise ValidationFailure(f"required canonical record missing: {rid}")
    return registry[rid][1]


def fmt_minus(value: float, decimals: int) -> str:
    text = f"{abs(float(value)):.{decimals}f}"
    return ("−" if float(value) < 0 else "") + text


def canonical_projection_expectations(
    registry: dict[str, tuple[Path, dict[str, Any]]]
) -> list[tuple[str, str]]:
    h1 = get_record(registry, "RES-HR-001")
    h2 = get_record(registry, "RES-HR-006")
    h3 = get_record(registry, "EXP-HR-007")
    d1 = get_record(registry, "DATA-HR-001")
    d2 = get_record(registry, "DATA-HR-002")
    d3 = get_record(registry, "DATA-HR-003")
    h1diag = get_record(registry, "RES-HR-005")

    h1m = h1["headline_metrics"]
    h2m = h2["headline_metrics"]
    current_diag = h1diag["headline_metrics"]["current_integrated_report"]

    h1_role = str(d1["role"]).replace("_", " ")
    h2_role = str(d2["role"]).replace("_", " ")
    h3_role = str(d3["role"]).replace("_", " ") + " / " + str(d3["consumption_status"])

    ci = h2m["primary_clustered_95ci_bps"]
    expected = [
        ("H1 status", 'status: "NOT SUPPORTED"'),
        ("H1 trades", f'["Trades", "{int(h1m["trades"]):,}"]'),
        ("H1 mean", f'["Mean", "{fmt_minus(h1m["mean_R"], 4)} R"]'),
        ("H1 profit factor", f'["Profit Factor", "{float(h1m["profit_factor"]):.3f}"]'),
        ("H1 max drawdown", f'["Max DD", "{float(h1m["max_drawdown_R"]):.2f} R"]'),
        ("H2 classification", f'status: "{h2m["classification"].replace("_", " ")}"'),
        ("H2 events", f'["Events", "{int(h2m["primary_event_count"]):,}"]'),
        ("H2 mean", f'["Mean", "{fmt_minus(h2m["primary_mean_bps"], 3)} bps"]'),
        ("H2 positive rate", f'["Positive", "{float(h2m["primary_positive_rate"]) * 100:.2f}%"]'),
        (
            "H2 interval",
            f'["95% CI", "{fmt_minus(ci[0], 3)} to {fmt_minus(ci[1], 3)} bps"]',
        ),
        ("H3 status", f'status: "{str(h3["status"]).replace("_", " ")}"'),
        ("DATA-HR-001 role", f'role: "{h1_role}"'),
        ("DATA-HR-002 role", f'role: "{h2_role}"'),
        ("DATA-HR-003 role", f'role: "{h3_role}"'),
        (
            "H1 current diagnostic classification",
            f'currentLabel: "{current_diag["current_classification_in_project_brief"]}"',
        ),
        ("H1 unresolved source conflict flag", "active: true"),
        ("H1 source conflict label", 'label: "SOURCE CONFLICT"'),
    ]
    return expected


def validate_projection_text(
    web_text: str, registry: dict[str, tuple[Path, dict[str, Any]]]
) -> list[str]:
    errors: list[str] = []
    for label, fragment in canonical_projection_expectations(registry):
        if fragment not in web_text:
            errors.append(f"Web projection mismatch: {label}; expected fragment {fragment!r}")
    return errors


def snapshot_commit(web_text: str) -> str | None:
    match = re.search(r'canonicalSnapshotCommit:\s*"([0-9a-f]{40})"', web_text)
    return match.group(1) if match else None


def validate_freshness(web_text: str) -> list[str]:
    errors: list[str] = []
    commit = snapshot_commit(web_text)
    if not commit:
        return ["web projection does not declare meta.canonicalSnapshotCommit"]

    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return [f"canonicalSnapshotCommit {commit} is not available in git history"]

    proc = subprocess.run(
        ["git", "diff", "--name-only", commit, "HEAD", "--", *FRESHNESS_PATHS],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    changed = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if changed:
        errors.append(
            "Web projection is stale relative to canonicalSnapshotCommit "
            f"{commit}; canonical research paths changed: {', '.join(changed)}"
        )
    return errors


def run_validation(check_freshness: bool = True) -> list[str]:
    registry, errors = collect_records()
    errors.extend(validate_references(registry))
    errors.extend(validate_result_statuses(registry))

    if not WEB_DATA.exists():
        errors.append(f"missing Web projection: {WEB_DATA.relative_to(ROOT)}")
        return errors

    web_text = WEB_DATA.read_text(encoding="utf-8")
    errors.extend(validate_projection_text(web_text, registry))
    if check_freshness:
        errors.extend(validate_freshness(web_text))
    return errors


def run_self_test() -> list[str]:
    failures: list[str] = []
    registry, base_errors = collect_records()
    if base_errors:
        return ["self-test precondition failed because canonical records are invalid", *base_errors]

    web_text = WEB_DATA.read_text(encoding="utf-8")
    expectations = canonical_projection_expectations(registry)
    first_fragment = expectations[0][1]
    if first_fragment not in web_text:
        failures.append("self-test could not locate baseline projection fragment")
    else:
        mutated = web_text.replace(first_fragment, 'status: "INTENTIONAL MISMATCH"', 1)
        if not validate_projection_text(mutated, registry):
            failures.append("projection mutation was not detected")

    fake_registry = dict(registry)
    sample_id = next(iter(registry))
    fake_registry["BROKEN-REF-TEST"] = (
        ROOT / "self-test.yaml",
        {
            "id": "BROKEN-REF-TEST",
            "type": "SelfTest",
            "relations": [{"type": "test", "target": "MISSING-ENTITY-SELF-TEST"}],
        },
    )
    if not validate_references(fake_registry):
        failures.append("missing relation target mutation was not detected")

    ids = [sample_id, sample_id]
    if len(ids) == len(set(ids)):
        failures.append("duplicate-id self-test construction failed")
    # collect_records performs the real duplicate-ID check. This assertion protects
    # the test itself without writing a mutated repository copy.

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run bounded in-memory negative tests after validating the real repository",
    )
    args = parser.parse_args()

    errors = run_validation(check_freshness=True)
    if errors:
        print("VALIDATION=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.self_test:
        failures = run_self_test()
        if failures:
            print("SELF_TEST=FAIL")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print("SELF_TEST=PASS")

    print("VALIDATION=PASS")
    print(
        "BOUNDARY=structural_integrity_and_web_projection_sync_only;"
        "not_scientific_validity_or_recomputation"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
