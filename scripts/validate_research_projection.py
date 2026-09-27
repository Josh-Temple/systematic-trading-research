#!/usr/bin/env python3
"""Validate Horizontal Reaction canonical records and the derived web projection.

This is a structural/freshness check only. A PASS does not establish scientific
validity, computational reproducibility, or absence of temporal leakage.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LINE = ROOT / "research/lines/horizontal-reaction-v0.1"
WEB_DATA = ROOT / "web/data/horizontal-reaction-v0.1.js"

SNAPSHOT_PATHS = [
    "research/lines/horizontal-reaction-v0.1/CURRENT.md",
    "research/lines/horizontal-reaction-v0.1/results/RES-HR-001.md",
    "research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md",
    "research/lines/horizontal-reaction-v0.1/results/RES-HR-006.md",
    "research/lines/horizontal-reaction-v0.1/interpretations/INT-HR-002.md",
    "research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-003.md",
    "research/lines/horizontal-reaction-v0.1/experiments/EXP-HR-007.md",
    "research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md",
    "research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-001.md",
    "research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-002.md",
    "research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-003.md",
]

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        value = yaml.safe_load(text)
        return value if isinstance(value, dict) else None
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unterminated frontmatter: {path}")
    value = yaml.safe_load(text[4:end])
    return value if isinstance(value, dict) else None


def norm(value: object) -> str:
    return re.sub(r"[ _/]+", " ", str(value).strip().upper())


def numbers(value: str) -> list[float]:
    value = value.replace("−", "-")
    out = []
    for token in re.findall(r"-?\d[\d,]*(?:\.\d+)?", value):
        out.append(float(token.replace(",", "")))
    return out


def close(a: float, b: float, tol: float) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol


def load_web_data() -> dict:
    js = (
        "global.window={};"
        "require('./web/data/horizontal-reaction-v0.1.js');"
        "process.stdout.write(JSON.stringify(window.RESEARCH_UI_DATA));"
    )
    proc = subprocess.run(
        ["node", "-e", js],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"web data load failed: {proc.stderr}")
    return json.loads(proc.stdout)


def local_path_from_github(url: str) -> Path | None:
    prefix = "https://github.com/Josh-Temple/systematic-trading-research/"
    if not url.startswith(prefix):
        return None
    rest = url[len(prefix):]
    for marker in ("blob/main/", "tree/main/"):
        if rest.startswith(marker):
            return ROOT / rest[len(marker):]
    return None


def collect_web_urls(data: dict) -> list[str]:
    urls = [
        data["line"]["canonical"],
        data["line"]["current"],
        data["current"]["conflict"]["canonical"],
        data["current"]["nextTest"]["canonical"],
        data["diagnostics"]["canonical"],
        data["canonicalBase"],
    ]
    urls.extend(h["canonical"] for h in data["hypotheses"])
    urls.extend(d["canonical"] for d in data["datasets"])
    urls.extend(href for _, href in data["diagnostics"]["records"])
    for _, _, _, refs in data["timeline"]:
        urls.extend(href for _, href in refs)
    return urls


def main() -> int:
    entity_files = sorted(LINE.rglob("*.md")) + sorted((LINE / "runs").glob("*.yaml"))
    entities: dict[str, tuple[Path, dict]] = {}

    for path in entity_files:
        try:
            meta = frontmatter(path)
        except Exception as exc:
            errors.append(f"YAML parse failed: {path.relative_to(ROOT)}: {exc}")
            continue
        if not meta or "id" not in meta:
            continue
        entity_id = str(meta["id"])
        if entity_id in entities:
            errors.append(
                f"duplicate id {entity_id}: {entities[entity_id][0].relative_to(ROOT)} and {path.relative_to(ROOT)}"
            )
        else:
            entities[entity_id] = (path, meta)

    check(bool(entities), "no research entities parsed")

    for entity_id, (path, meta) in entities.items():
        for relation in meta.get("relations", []) or []:
            if not isinstance(relation, dict):
                errors.append(f"{entity_id}: relation is not an object")
                continue
            target = relation.get("target")
            if isinstance(target, str):
                check(target in entities, f"{entity_id}: missing relation target {target}")

        if meta.get("type") == "Result":
            for field in ("execution_status", "evidence_validity", "scientific_status"):
                check(field in meta, f"{entity_id}: Result missing {field}")

    required = [
        "RES-HR-001",
        "RES-HR-005",
        "RES-HR-006",
        "EXP-HR-007",
        "DATA-HR-001",
        "DATA-HR-002",
        "DATA-HR-003",
    ]
    for entity_id in required:
        check(entity_id in entities, f"missing required entity {entity_id}")

    data = load_web_data()

    source_commit = data.get("meta", {}).get("sourceCommit")
    check(bool(re.fullmatch(r"[0-9a-f]{40}", str(source_commit or ""))), "web meta.sourceCommit must be a full commit SHA")
    if source_commit and re.fullmatch(r"[0-9a-f]{40}", source_commit):
        exists = subprocess.run(
            ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
        )
        check(exists.returncode == 0, f"sourceCommit not available in git history: {source_commit}")
        if exists.returncode == 0:
            diff = subprocess.run(
                ["git", "diff", "--quiet", source_commit, "HEAD", "--", *SNAPSHOT_PATHS],
                cwd=ROOT,
            )
            check(
                diff.returncode == 0,
                "canonical Horizontal Reaction snapshot changed after web meta.sourceCommit; refresh web projection",
            )

    for url in collect_web_urls(data):
        local = local_path_from_github(url)
        if local is not None:
            check(local.exists(), f"web canonical link target missing: {url}")

    h_by_id = {h["id"]: h for h in data["hypotheses"]}
    d_by_id = {d["id"]: d for d in data["datasets"]}

    h1 = entities["RES-HR-001"][1]
    h1_ui = h_by_id.get("HYP-HR-001", {})
    check(norm(h1_ui.get("status")) == norm(h1["scientific_status"]), "H1 status mismatch")
    h1_metrics = dict(h1_ui.get("metrics", []))
    hm = h1["headline_metrics"]
    check(numbers(h1_metrics.get("Trades", ""))[:1] == [float(hm["trades"])], "H1 trade count mismatch")
    vals = numbers(h1_metrics.get("Mean", ""))
    check(bool(vals) and close(vals[0], float(hm["mean_R"]), 5e-5), "H1 mean mismatch")
    vals = numbers(h1_metrics.get("Profit Factor", ""))
    check(bool(vals) and close(vals[0], float(hm["profit_factor"]), 5e-4), "H1 Profit Factor mismatch")
    vals = numbers(h1_metrics.get("Max DD", ""))
    check(bool(vals) and close(vals[0], float(hm["max_drawdown_R"]), 0.01), "H1 max drawdown mismatch")

    h2 = entities["RES-HR-006"][1]
    h2_ui = h_by_id.get("HYP-HR-002", {})
    h2m = h2["headline_metrics"]
    check(norm(h2_ui.get("status")) == norm(h2m["classification"]), "H2 classification mismatch")
    h2_metrics = dict(h2_ui.get("metrics", []))
    check(numbers(h2_metrics.get("Events", ""))[:1] == [float(h2m["primary_event_count"])], "H2 event count mismatch")
    vals = numbers(h2_metrics.get("Mean", ""))
    check(bool(vals) and close(vals[0], float(h2m["primary_mean_bps"]), 0.001), "H2 mean mismatch")
    vals = numbers(h2_metrics.get("Positive", ""))
    check(bool(vals) and close(vals[0], float(h2m["primary_positive_rate"]) * 100.0, 0.01), "H2 positive rate mismatch")
    vals = numbers(h2_metrics.get("95% CI", ""))
    ci = [float(x) for x in h2m["primary_clustered_95ci_bps"]]
    check(len(vals) >= 3 and close(vals[-2], ci[0], 0.001) and close(vals[-1], ci[1], 0.001), "H2 interval mismatch")

    exp = entities["EXP-HR-007"][1]
    h3_ui = h_by_id.get("HYP-HR-003", {})
    check(norm(h3_ui.get("status")) == norm(exp["status"]), "H3 status mismatch")

    data1 = entities["DATA-HR-001"][1]
    data2 = entities["DATA-HR-002"][1]
    data3 = entities["DATA-HR-003"][1]
    check(norm(d_by_id["DATA-HR-001"]["role"]) == norm(data1["role"]), "DATA-HR-001 role mismatch")
    check(norm(d_by_id["DATA-HR-002"]["role"]) == norm(data2["role"]), "DATA-HR-002 role mismatch")
    d3_role = norm(d_by_id["DATA-HR-003"]["role"])
    check(norm(data3["role"]) in d3_role and norm(data3["consumption_status"]) in d3_role, "DATA-HR-003 role/consumption mismatch")

    conflict = entities["RES-HR-005"][1]["headline_metrics"]
    check(data["current"]["conflict"]["active"] is True, "source conflict must remain visible")
    check(conflict["source_discrepancy"] == "PRESENT_UNRESOLVED", "canonical source discrepancy is not unresolved")
    expected_label = conflict["current_integrated_report"]["current_classification_in_project_brief"]
    check(data["diagnostics"]["currentLabel"] == expected_label, "diagnostic current label mismatch")

    if errors:
        print("VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"VALIDATION=PASS entities={len(entities)}")
    print("SCOPE=STRUCTURE_LINKS_WEB_PROJECTION_FRESHNESS_ONLY")
    print("SCIENTIFIC_VALIDITY=NOT_ESTABLISHED_BY_THIS_CHECK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
