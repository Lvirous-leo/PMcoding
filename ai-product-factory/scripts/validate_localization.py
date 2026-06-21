#!/usr/bin/env python3
"""Check Chinese explanation budgets and exact normative duplication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


DISCLAIMER_MARKERS = ("唯一执行依据", "以英文为准")
FORBIDDEN_ZH_HEADINGS = {
    "State Transitions",
    "Evidence Levels",
    "Approval Gates",
    "Artifact Status",
}


def paragraphs(text: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", text)
    result: list[str] = []
    for block in blocks:
        normalized = re.sub(r"\s+", " ", block.strip())
        if len(normalized) >= 80 and not normalized.startswith("```"):
            result.append(normalized)
    return result


def validate(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    zh_files = sorted(root.glob("skills/*/references/zh-overview.md"))
    if len(zh_files) != 4:
        errors.append(f"expected 4 Chinese overview files; found {len(zh_files)}")
    for path in zh_files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > 60:
            errors.append(f"{path}: exceeds 60 lines ({len(lines)})")
        if not all(marker in text for marker in DISCLAIMER_MARKERS):
            errors.append(f"{path}: missing English-authoritative disclaimer")
        for heading in FORBIDDEN_ZH_HEADINGS:
            if re.search(rf"^#+\s+{re.escape(heading)}\s*$", text, re.MULTILINE):
                errors.append(f"{path}: redefines normative section {heading}")
    normative_files = [
        path
        for path in root.rglob("*.md")
        if path.name != "zh-overview.md"
        and "references/examples" not in path.as_posix()
    ]
    all_paragraphs: list[str] = []
    paragraph_paths: dict[str, set[str]] = {}
    for path in normative_files:
        for paragraph in paragraphs(path.read_text(encoding="utf-8")):
            digest = hashlib.sha256(paragraph.encode("utf-8")).hexdigest()
            all_paragraphs.append(digest)
            paragraph_paths.setdefault(digest, set()).add(str(path))
    counts = Counter(all_paragraphs)
    duplicate_instances = sum(count - 1 for count in counts.values() if count > 1)
    ratio = duplicate_instances / max(1, len(all_paragraphs))
    if ratio >= 0.03:
        examples = [
            sorted(paragraph_paths[digest])
            for digest, count in counts.items()
            if count > 1
        ][:3]
        errors.append(
            f"exact normative paragraph duplication is {ratio:.2%}; examples={examples}"
        )
    return {
        "passed": not errors,
        "errors": errors,
        "zh_files": len(zh_files),
        "normative_paragraphs": len(all_paragraphs),
        "duplicate_instances": duplicate_instances,
        "duplicate_ratio": ratio,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["passed"]:
        print(
            "Localization validation passed: "
            f"{result['zh_files']} overviews, "
            f"{result['duplicate_ratio']:.2%} exact duplication."
        )
    else:
        print("Localization validation failed:")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
