#!/usr/bin/env python3
"""Migrate an AI Product Factory V2 state file to V3."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from factory_core import (
    ARTIFACT_PATHS,
    STATE_RELATIVE,
    append_event,
    new_state,
    save_state,
    utc_now,
)


def scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value.strip("\"'")


def parse_legacy_yaml(text: str) -> dict[str, Any]:
    """Parse the mapping-only subset used by the V2 state example."""
    result: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, result)]
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        match = re.match(r"^(\s*)([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            continue
        indent = len(match.group(1))
        key = match.group(2)
        value = match.group(3) or ""
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if value:
            parent[key] = scalar(value)
        else:
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
    return result


def load_legacy(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = parse_legacy_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("legacy state must contain a mapping")
    return data


def migrate(root: Path) -> tuple[str, Path | None]:
    root = root.resolve()
    path = root / STATE_RELATIVE
    if not path.exists():
        raise FileNotFoundError(path)
    legacy = load_legacy(path)
    if legacy.get("schema_version") == 3:
        return "already_v3", None
    mode = legacy.get("mode", "greenfield")
    if mode not in {"greenfield", "enhancement", "non-ui"}:
        mode = "greenfield"
    state = new_state(root, mode)
    phase = legacy.get("current_phase")
    if phase in {
        "discovery",
        "prd",
        "ui_input",
        "design",
        "technical_design",
        "planning",
        "development",
        "review",
        "release",
        "completed",
    }:
        state["workflow"]["current_phase"] = phase
    legacy_status = legacy.get("status")
    if legacy_status in {"not_started", "in_progress", "blocked", "completed"}:
        state["workflow"]["run_status"] = legacy_status
    downgraded_approvals: list[str] = []
    for key, record in legacy.get("artifacts", {}).items():
        if key not in ARTIFACT_PATHS or not isinstance(record, dict):
            continue
        target = state["artifacts"][key]
        target["path"] = str(record.get("path") or target["path"])
        version = record.get("version", 0)
        target["version"] = version if isinstance(version, int) and version >= 0 else 0
        status = record.get("status", "missing")
        if status == "pending" and target["version"] == 0:
            status = "pending"
        if status in {
            "missing",
            "pending",
            "draft",
            "in_review",
            "approved",
            "invalidated",
            "not_applicable",
            "blocked",
        }:
            target["status"] = status
        target["approved_by"] = record.get("approved_by")
        if target["status"] == "approved":
            approved_at = record.get("approved_at")
            if approved_at:
                target["approved_at"] = approved_at
            else:
                target["status"] = "in_review"
                downgraded_approvals.append(key)
                state["blocked_reasons"].append(
                    f"Legacy approval for {key} lacks approved_at and requires reapproval"
                )
    if downgraded_approvals:
        phase_for_artifact = {
            "prd": "prd",
            "ui_input": "ui_input",
            "ui": "design",
            "tdd": "technical_design",
            "sprint": "planning",
            "review": "review",
            "release": "release",
        }
        first = min(
            downgraded_approvals,
            key=lambda item: list(ARTIFACT_PATHS).index(item),
        )
        state["workflow"]["current_phase"] = phase_for_artifact[first]
        state["workflow"]["run_status"] = "blocked"
        state["workflow"]["gate_status"] = "blocked"
    backup = path.with_name(f"state.v2.{utc_now().replace(':', '-')}.yaml")
    shutil.copy2(path, backup)
    save_state(root, state)
    append_event(
        root,
        "state_migrated",
        from_version=2,
        to_version=3,
        backup=str(backup.relative_to(root)),
        downgraded_approvals=downgraded_approvals,
    )
    return "migrated", backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        status, backup = migrate(args.root)
    except (OSError, ValueError) as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        return 1
    if status == "already_v3":
        print("State already uses schema version 3.")
    else:
        print(f"Migrated state to version 3. Backup: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
