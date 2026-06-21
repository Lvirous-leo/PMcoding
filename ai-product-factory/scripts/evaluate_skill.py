#!/usr/bin/env python3
"""Validate eval fixtures and run an offline lexical routing smoke test."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILLS = {
    "ai-product-factory": [
        "end to end",
        "complete product",
        "continue workflow",
        "resume",
        "from idea to",
        "产品工厂",
        "完整产品",
        "从想法到",
        "继续流程",
    ],
    "product-discovery-prd": [
        "prd",
        "requirement",
        "product idea",
        "competitor",
        "market research",
        "user problem",
        "需求",
        "产品想法",
        "竞品",
        "市场",
        "用户问题",
    ],
    "design-technical-planning": [
        "opendesign",
        "ui_input",
        "ui specification",
        "technical design",
        "tdd",
        "sprint plan",
        "设计评审",
        "技术方案",
        "开发计划",
        "任务拆分",
    ],
    "delivery-review-release": [
        "claude code",
        "implement task",
        "code review",
        "release",
        "deploy",
        "代码评审",
        "发布",
        "部署",
        "开发交接",
    ],
}


def route(prompt: str) -> str | None:
    text = prompt.casefold()
    scores = {
        skill: sum(2 if " " in term else 1 for term in terms if term.casefold() in text)
        for skill, terms in SKILLS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else None


def validate_fixture(path: Path, data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, list):
        return [f"{path}: top level must be an array"]
    seen: set[str] = set()
    for index, case in enumerate(data):
        if not isinstance(case, dict):
            errors.append(f"{path}[{index}]: case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{path}[{index}]: missing id")
        elif case_id in seen:
            errors.append(f"{path}: duplicate id {case_id}")
        else:
            seen.add(case_id)
        if path.name == "trigger-cases.json":
            if not isinstance(case.get("prompt"), str):
                errors.append(f"{path}[{index}]: missing prompt")
            expected = case.get("expected_skill")
            if expected is not None and expected not in SKILLS:
                errors.append(f"{path}[{index}]: invalid expected_skill {expected}")
        elif not any(
            key in case
            for key in ("required_sections", "expected_phase_order", "assertions")
        ):
            errors.append(f"{path}[{index}]: missing artifact or workflow expectations")
    return errors


def evaluate(root: Path) -> dict[str, Any]:
    files = sorted(root.rglob("*.json"))
    errors: list[str] = []
    triggers: list[dict[str, Any]] = []
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        errors.extend(validate_fixture(path, data))
        if path.name == "trigger-cases.json" and isinstance(data, list):
            triggers = data
    correct = 0
    false_positive = 0
    false_negative = 0
    details: list[dict[str, Any]] = []
    for case in triggers:
        actual = route(case["prompt"])
        expected = case.get("expected_skill")
        if actual == expected:
            correct += 1
        if expected is None and actual is not None:
            false_positive += 1
        if expected is not None and actual is None:
            false_negative += 1
        details.append(
            {
                "id": case["id"],
                "expected": expected,
                "actual": actual,
                "passed": actual == expected,
            }
        )
    total = len(triggers)
    return {
        "passed": not errors and all(item["passed"] for item in details),
        "fixture_files": len(files),
        "fixture_errors": errors,
        "trigger_cases": total,
        "trigger_accuracy": correct / max(1, total),
        "false_positive": false_positive,
        "false_negative": false_negative,
        "details": details,
        "note": "Lexical routing is an offline smoke test, not a model-quality benchmark.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["note"])
        print(
            f"Fixtures: {result['fixture_files']}; "
            f"trigger accuracy: {result['trigger_accuracy']:.1%}"
        )
        for error in result["fixture_errors"]:
            print(f"- {error}")
        for item in result["details"]:
            if not item["passed"]:
                print(
                    f"- {item['id']}: expected {item['expected']}, got {item['actual']}"
                )
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
