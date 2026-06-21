#!/usr/bin/env python3
"""Shared state and file helpers for AI Product Factory scripts."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PLUGIN_ROOT / "schemas/state.schema.json"
STATE_RELATIVE = Path(".ai/product-factory/state.yaml")
EVENTS_RELATIVE = Path(".ai/product-factory/events.jsonl")

ARTIFACT_PATHS = {
    "prd": "docs/PRD.md",
    "ui_input": "docs/UI_INPUT.md",
    "ui": "docs/UI.md",
    "tdd": "docs/TDD.md",
    "sprint": ".ai/tasks/sprint-001.md",
    "review": ".ai/reviews/review-001.md",
    "release": ".ai/releases/release-001.md",
}

ARTIFACT_TEMPLATES = {
    "prd": "PRD.md",
    "ui_input": "UI_INPUT.md",
    "ui": "UI.md",
    "tdd": "TDD.md",
    "sprint": "sprint.md",
    "review": "review.md",
    "release": "release.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_data(path: Path) -> dict[str, Any]:
    """Load V3 JSON-compatible YAML or regular YAML when PyYAML is available."""
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ValueError(
                f"{path} is not JSON-compatible YAML; install PyYAML for legacy YAML"
            ) from exc
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def save_data(path: Path, data: dict[str, Any]) -> None:
    """Atomically write JSON, which is valid YAML 1.2."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    handle, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def append_event(root: Path, event: str, **details: Any) -> None:
    path = root / EVENTS_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"at": utc_now(), "event": event, **details}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def new_artifact(key: str) -> dict[str, Any]:
    return {
        "path": ARTIFACT_PATHS[key],
        "version": 0,
        "status": "missing",
        "approved_by": None,
        "approved_at": None,
        "upstream_versions": {},
        "invalidated_by": [],
    }


def new_state(
    root: Path,
    mode: str,
    response_language: str = "auto",
    requested_depth: str = "auto",
) -> dict[str, Any]:
    selected = "standard" if requested_depth == "auto" else requested_depth
    state = {
        "schema_version": 3,
        "project": {
            "name": root.name,
            "root": str(root.resolve()),
            "mode": mode,
            "response_language": response_language,
        },
        "workflow": {
            "current_phase": "discovery",
            "run_status": "not_started",
            "depth": {
                "requested": requested_depth,
                "selected": selected,
                "reason": (
                    "Default pending repository and uncertainty assessment"
                    if requested_depth == "auto"
                    else "User override"
                ),
            },
            "evidence_level": "L0",
            "decision": "UNDECIDED",
            "gate_status": "not_ready",
        },
        "artifacts": {key: new_artifact(key) for key in ARTIFACT_PATHS},
        "open_questions": [],
        "critical_assumptions": [],
        "blocked_reasons": [],
        "updated_at": utc_now(),
    }
    if mode == "non-ui":
        for key in ("ui_input", "ui"):
            state["artifacts"][key]["status"] = "not_applicable"
    return state


def enum_values(schema: dict[str, Any], name: str) -> set[str]:
    return set(schema["$defs"][name]["enum"])


def validate_state_core(state: dict[str, Any]) -> list[str]:
    """Validate invariants needed by every script without external packages."""
    schema = load_schema()
    errors: list[str] = []
    for key in (
        "schema_version",
        "project",
        "workflow",
        "artifacts",
        "open_questions",
        "blocked_reasons",
        "updated_at",
    ):
        if key not in state:
            errors.append(f"missing state field: {key}")
    if errors:
        return errors
    if state["schema_version"] != 3:
        errors.append("schema_version must be 3")
    project = state.get("project", {})
    workflow = state.get("workflow", {})
    if project.get("mode") not in enum_values(schema, "mode"):
        errors.append(f"invalid project mode: {project.get('mode')}")
    if workflow.get("current_phase") not in enum_values(schema, "phase"):
        errors.append(f"invalid current phase: {workflow.get('current_phase')}")
    if workflow.get("evidence_level") not in enum_values(schema, "evidence"):
        errors.append(f"invalid evidence level: {workflow.get('evidence_level')}")
    if workflow.get("decision") not in enum_values(schema, "decision"):
        errors.append(f"invalid decision: {workflow.get('decision')}")
    depth = workflow.get("depth", {})
    if depth.get("requested") not in {"auto", "lite", "standard", "deep"}:
        errors.append(f"invalid requested depth: {depth.get('requested')}")
    if depth.get("selected") not in {"lite", "standard", "deep"}:
        errors.append(f"invalid selected depth: {depth.get('selected')}")
    artifacts = state.get("artifacts", {})
    required_artifacts = set(ARTIFACT_PATHS)
    missing = required_artifacts - set(artifacts)
    if missing:
        errors.append(f"missing artifact records: {', '.join(sorted(missing))}")
    statuses = enum_values(schema, "artifact_status")
    for key, artifact in artifacts.items():
        status = artifact.get("status")
        if status not in statuses:
            errors.append(f"invalid artifact status for {key}: {status}")
        if status == "approved":
            if not artifact.get("approved_by") or not artifact.get("approved_at"):
                errors.append(f"approved artifact {key} lacks approval evidence")
        if status == "invalidated" and not artifact.get("invalidated_by"):
            errors.append(f"invalidated artifact {key} lacks invalidated_by")
    evidence = workflow.get("evidence_level")
    if workflow.get("decision") == "GO" and evidence not in {"L2", "L3"}:
        errors.append("GO requires evidence level L2 or L3")
    if workflow.get("decision") == "GO" and state.get("critical_assumptions"):
        errors.append("GO is incompatible with unresolved critical assumptions")
    return errors


def load_state(root: Path) -> dict[str, Any]:
    return load_data(root / STATE_RELATIVE)


def save_state(root: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    errors = validate_state_core(state)
    if errors:
        raise ValueError("; ".join(errors))
    save_data(root / STATE_RELATIVE, state)
