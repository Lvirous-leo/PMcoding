#!/usr/bin/env python3
"""Validate AI Product Factory state, artifacts, gates, and traceability."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from factory_core import (
    ARTIFACT_PATHS,
    ARTIFACT_TEMPLATES,
    PLUGIN_ROOT,
    load_state,
    validate_state_core,
)


GATE_ARTIFACTS = {
    "prd": ["prd"],
    "design": ["ui_input", "ui"],
    "technical": ["tdd"],
    "planning": ["sprint"],
    "review": ["review"],
    "release": ["release"],
}
GATE_ORDER = list(GATE_ARTIFACTS)
PLACEHOLDER_RE = re.compile(
    r"\[(?:date|name|version|write|describe|identify|state|list|"
    r"approved|iso-8601|method|payload|fields|values|purpose|"
    r"action|behavior|evidence|outcome|metric|baseline|target|window|"
    r"capability|explicit|persona|testable|rule|context|observable|"
    r"threshold|question|actor|entry|ordered|recovery|screen|component|"
    r"responsibilities|variants|regions|technical|level|scope|environment|"
    r"task|small|expected|command|output|risk|reason|sha|ready|hold|rollback)"
    r"[^\]]*\]|\b(?:TBD|TODO|FIXME)\b",
    re.IGNORECASE,
)
ID_PATTERNS = {
    "requirements": re.compile(r"\bREQ-\d{3,}\b"),
    "tasks": re.compile(r"\bTASK-\d{3,}\b"),
    "tests": re.compile(r"\bTEST-\d{3,}\b"),
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def template_metadata(template: Path) -> tuple[str, list[str]]:
    text = template.read_text(encoding="utf-8")
    match = re.search(r"<!-- apf-template\n(.*?)-->", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing template metadata: {template}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    artifact = values.get("artifact", "")
    headings = [
        item.strip()
        for item in values.get("required_headings", "").split("|")
        if item.strip()
    ]
    if not artifact or not headings:
        raise ValueError(f"incomplete template metadata: {template}")
    return artifact, headings


def section_content(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def validate_artifact(
    root: Path, key: str, record: dict[str, Any], strict: bool
) -> list[Finding]:
    findings: list[Finding] = []
    if record.get("status") == "not_applicable":
        return findings
    path = root / record.get("path", ARTIFACT_PATHS[key])
    if not path.is_file():
        findings.append(Finding("error", "artifact.missing", "Artifact is missing", str(path)))
        return findings
    template = PLUGIN_ROOT / "assets/templates" / ARTIFACT_TEMPLATES[key]
    expected_key, headings = template_metadata(template)
    if expected_key != key:
        findings.append(
            Finding("error", "template.identity", f"Template declares {expected_key}, expected {key}", str(template))
        )
    text = path.read_text(encoding="utf-8")
    for heading in headings:
        content = section_content(text, heading)
        if content is None:
            findings.append(
                Finding("error", "artifact.heading", f"Missing required heading: {heading}", str(path))
            )
        elif not content or PLACEHOLDER_RE.search(content):
            findings.append(
                Finding("error", "artifact.incomplete", f"Section is empty or unresolved: {heading}", str(path))
            )
    if record.get("status") == "approved":
        if record.get("version", 0) < 1:
            findings.append(
                Finding("error", "approval.version", "Approved artifact must have version >= 1", str(path))
            )
        if PLACEHOLDER_RE.search(text):
            findings.append(
                Finding("error", "approval.placeholder", "Approved artifact contains unresolved guidance", str(path))
            )
    if key == "sprint" and "Claude Code" not in text:
        findings.append(
            Finding("error", "ownership.implementation", "Sprint must assign implementation to Claude Code", str(path))
        )
    if strict and record.get("status") in {"draft", "in_review", "approved"}:
        if "Upstream versions:" not in text:
            findings.append(
                Finding("error", "artifact.upstream", "Artifact lacks upstream version declaration", str(path))
            )
    return findings


def selected_keys(gate: str) -> list[str]:
    keys: list[str] = []
    for name in GATE_ORDER[: GATE_ORDER.index(gate) + 1]:
        keys.extend(GATE_ARTIFACTS[name])
    return keys


def traceability_findings(root: Path, state: dict[str, Any], gate: str) -> list[Finding]:
    findings: list[Finding] = []
    texts: dict[str, str] = {}
    for key in selected_keys(gate):
        record = state["artifacts"][key]
        path = root / record["path"]
        if path.is_file():
            texts[key] = path.read_text(encoding="utf-8")
    requirements = set(ID_PATTERNS["requirements"].findall(texts.get("prd", "")))
    if gate in {"planning", "review", "release"} and not requirements:
        findings.append(Finding("error", "trace.requirement", "No requirement IDs found in PRD"))
    if gate in {"planning", "review", "release"}:
        sprint = texts.get("sprint", "")
        for req in sorted(requirements):
            if req not in sprint:
                findings.append(
                    Finding("error", "trace.plan", f"{req} is not mapped into the sprint plan")
                )
        if not ID_PATTERNS["tasks"].search(sprint):
            findings.append(Finding("error", "trace.task", "No task IDs found in sprint plan"))
        if not ID_PATTERNS["tests"].search(sprint):
            findings.append(Finding("error", "trace.test", "No test IDs found in sprint plan"))
    if gate in {"review", "release"}:
        review = texts.get("review", "")
        for req in sorted(requirements):
            if req not in review:
                findings.append(
                    Finding("error", "trace.review", f"{req} lacks review evidence")
                )
    return findings


def validate(root: Path, gate: str, strict: bool = True) -> list[Finding]:
    findings: list[Finding] = []
    try:
        state = load_state(root)
    except (OSError, ValueError) as exc:
        return [Finding("error", "state.load", str(exc))]
    for error in validate_state_core(state):
        findings.append(Finding("error", "state.invalid", error))
    for key in selected_keys(gate):
        record = state.get("artifacts", {}).get(key)
        if not record:
            findings.append(Finding("error", "state.artifact", f"Missing artifact record: {key}"))
            continue
        allowed = {"approved"}
        if key in {"ui_input", "ui"}:
            allowed.add("not_applicable")
        if record.get("status") not in allowed:
            findings.append(
                Finding(
                    "error",
                    "gate.status",
                    f"{key} must be approved or applicable; found {record.get('status')}",
                    record.get("path"),
                )
            )
        findings.extend(validate_artifact(root, key, record, strict))
    findings.extend(traceability_findings(root, state, gate))
    return findings


def render_markdown(findings: list[Finding], gate: str) -> str:
    if not findings:
        return f"# Validation Result\n\nGate `{gate}` passed.\n"
    lines = [f"# Validation Result", "", f"Gate `{gate}` failed.", ""]
    for finding in findings:
        location = f" — `{finding.path}`" if finding.path else ""
        lines.append(
            f"- **{finding.severity.upper()} {finding.code}**: {finding.message}{location}"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--gate", choices=GATE_ORDER, required=True)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-strict", action="store_true")
    args = parser.parse_args()
    findings = validate(args.root.resolve(), args.gate, strict=not args.no_strict)
    if args.format == "json":
        output = json.dumps(
            {
                "gate": args.gate,
                "passed": not findings,
                "findings": [asdict(item) for item in findings],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n"
    else:
        output = render_markdown(findings, args.gate)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
