from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from factory_core import load_state, new_state, save_state, validate_state_core  # noqa: E402


class StateTests(unittest.TestCase):
    def test_new_state_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = new_state(Path(directory), "greenfield")
            self.assertEqual([], validate_state_core(state))
            self.assertEqual("standard", state["workflow"]["depth"]["selected"])

    def test_non_ui_marks_design_artifacts_not_applicable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = new_state(Path(directory), "non-ui")
            self.assertEqual("not_applicable", state["artifacts"]["ui_input"]["status"])
            self.assertEqual("not_applicable", state["artifacts"]["ui"]["status"])

    def test_invalid_values_and_approval_evidence_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = new_state(Path(directory), "greenfield")
            state["project"]["mode"] = "unknown"
            state["artifacts"]["prd"]["status"] = "approved"
            errors = validate_state_core(state)
            self.assertTrue(any("invalid project mode" in error for error in errors))
            self.assertTrue(any("lacks approval evidence" in error for error in errors))

    def test_atomic_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = new_state(root, "enhancement", "zh", "deep")
            save_state(root, state)
            loaded = load_state(root)
            self.assertEqual(3, loaded["schema_version"])
            self.assertEqual("enhancement", loaded["project"]["mode"])
            self.assertEqual("deep", loaded["workflow"]["depth"]["selected"])


if __name__ == "__main__":
    unittest.main()
