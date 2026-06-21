from __future__ import annotations

import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from validate_localization import validate  # noqa: E402


class LocalizationTests(unittest.TestCase):
    def test_plugin_localization_budget_and_duplication(self) -> None:
        result = validate(PLUGIN_ROOT)
        self.assertTrue(result["passed"], result["errors"])
        self.assertLess(result["duplicate_ratio"], 0.03)


if __name__ == "__main__":
    unittest.main()
