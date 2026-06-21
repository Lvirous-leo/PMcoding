#!/usr/bin/env python3
"""Initialize AI Product Factory state and optional artifact templates."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from factory_core import (
    ARTIFACT_PATHS,
    ARTIFACT_TEMPLATES,
    EVENTS_RELATIVE,
    PLUGIN_ROOT,
    STATE_RELATIVE,
    append_event,
    new_state,
    save_state,
)


def initialize(
    root: Path,
    mode: str,
    response_language: str,
    depth: str,
    with_templates: bool,
) -> tuple[bool, list[str]]:
    root = root.resolve()
    state_path = root / STATE_RELATIVE
    created: list[str] = []
    if state_path.exists():
        return False, created
    state = new_state(root, mode, response_language, depth)
    save_state(root, state)
    created.append(str(STATE_RELATIVE))
    events_path = root / EVENTS_RELATIVE
    events_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.touch(exist_ok=True)
    append_event(
        root,
        "project_initialized",
        schema_version=3,
        mode=mode,
        requested_depth=depth,
    )
    created.append(str(EVENTS_RELATIVE))
    if with_templates:
        template_root = PLUGIN_ROOT / "assets/templates"
        for key, relative in ARTIFACT_PATHS.items():
            if state["artifacts"][key]["status"] == "not_applicable":
                continue
            destination = root / relative
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(template_root / ARTIFACT_TEMPLATES[key], destination)
            created.append(relative)
    return True, created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--mode",
        choices=["greenfield", "enhancement", "non-ui"],
        default="greenfield",
    )
    parser.add_argument(
        "--response-language", choices=["auto", "en", "zh"], default="auto"
    )
    parser.add_argument(
        "--depth", choices=["auto", "lite", "standard", "deep"], default="auto"
    )
    parser.add_argument("--with-templates", action="store_true")
    args = parser.parse_args()
    try:
        created_state, created = initialize(
            args.root,
            args.mode,
            args.response_language,
            args.depth,
            args.with_templates,
        )
    except (OSError, ValueError) as exc:
        print(f"Initialization failed: {exc}", file=sys.stderr)
        return 1
    if not created_state:
        print(f"Already initialized: {(args.root / STATE_RELATIVE).resolve()}")
        return 0
    print("Initialized AI Product Factory:")
    for path in created:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
