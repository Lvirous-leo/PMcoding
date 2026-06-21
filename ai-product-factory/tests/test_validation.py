from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from factory_core import new_state, save_state, utc_now  # noqa: E402
from validate_artifacts import validate  # noqa: E402


def resolved_template(name: str) -> str:
    text = (PLUGIN_ROOT / "assets/templates" / name).read_text(encoding="utf-8")
    return re.sub(r"\[[^\]]+\]", "Resolved", text)


class ValidationTests(unittest.TestCase):
    def approved_prd_fixture(self, root: Path) -> dict:
        state = new_state(root, "greenfield")
        record = state["artifacts"]["prd"]
        record.update(
            {
                "version": 1,
                "status": "approved",
                "approved_by": "user",
                "approved_at": utc_now(),
            }
        )
        path = root / record["path"]
        path.parent.mkdir(parents=True)
        path.write_text(resolved_template("PRD.md"), encoding="utf-8")
        save_state(root, state)
        return state

    def test_complete_prd_gate_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.approved_prd_fixture(root)
            self.assertEqual([], validate(root, "prd"))

    def test_missing_heading_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.approved_prd_fixture(root)
            path = root / state["artifacts"]["prd"]["path"]
            text = path.read_text(encoding="utf-8").replace(
                "## Product Vision\n", ""
            )
            path.write_text(text, encoding="utf-8")
            findings = validate(root, "prd")
            self.assertTrue(
                any(item.code == "artifact.heading" for item in findings)
            )

    def test_unapproved_status_fails_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.approved_prd_fixture(root)
            state["artifacts"]["prd"]["status"] = "draft"
            state["artifacts"]["prd"]["approved_by"] = None
            state["artifacts"]["prd"]["approved_at"] = None
            save_state(root, state)
            findings = validate(root, "prd")
            self.assertTrue(any(item.code == "gate.status" for item in findings))


if __name__ == "__main__":
    unittest.main()
