from __future__ import annotations

import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from evaluate_skill import evaluate, route  # noqa: E402


class EvaluateTests(unittest.TestCase):
    def test_router_smoke_cases(self) -> None:
        self.assertEqual(
            "product-discovery-prd",
            route("请分析这个产品需求，做竞品研究并写 PRD"),
        )
        self.assertEqual(
            "delivery-review-release",
            route("Ask Claude Code to implement this, then do code review"),
        )
        self.assertIsNone(route("Correct a spelling mistake"))

    def test_eval_fixtures_pass(self) -> None:
        result = evaluate(PLUGIN_ROOT / "evals")
        self.assertTrue(result["passed"], result)
        self.assertEqual(1.0, result["trigger_accuracy"])


if __name__ == "__main__":
    unittest.main()
