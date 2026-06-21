from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from factory_core import EVENTS_RELATIVE, STATE_RELATIVE, load_state  # noqa: E402
from init_project import initialize  # noqa: E402
from migrate_state import migrate  # noqa: E402


class MigrationTests(unittest.TestCase):
    def test_initialize_is_idempotent_and_copies_templates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            created, files = initialize(root, "greenfield", "en", "auto", True)
            self.assertTrue(created)
            self.assertIn("docs/PRD.md", files)
            created_again, files_again = initialize(
                root, "greenfield", "en", "auto", True
            )
            self.assertFalse(created_again)
            self.assertEqual([], files_again)
            self.assertTrue((root / EVENTS_RELATIVE).is_file())

    def test_migrate_v2_and_repeat_safely(self) -> None:
        legacy = """\
mode: enhancement
current_phase: technical_design
status: in_progress
artifacts:
  prd:
    path: docs/PRD.md
    version: 2
    status: approved
    approved_by: user
  ui_input:
    path: docs/UI_INPUT.md
    version: 2
    status: approved
    approved_by: user
  ui:
    path: docs/UI.md
    version: 2
    status: approved
    approved_by: user
  tdd:
    path: docs/TDD.md
    version: 1
    status: draft
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state_path = root / STATE_RELATIVE
            state_path.parent.mkdir(parents=True)
            state_path.write_text(legacy, encoding="utf-8")
            status, backup = migrate(root)
            self.assertEqual("migrated", status)
            self.assertIsNotNone(backup)
            self.assertTrue(backup and backup.is_file())
            state = load_state(root)
            self.assertEqual(3, state["schema_version"])
            self.assertEqual("enhancement", state["project"]["mode"])
            self.assertEqual(2, state["artifacts"]["prd"]["version"])
            self.assertEqual("in_review", state["artifacts"]["prd"]["status"])
            self.assertEqual("prd", state["workflow"]["current_phase"])
            self.assertEqual("blocked", state["workflow"]["run_status"])
            self.assertTrue(state["blocked_reasons"])
            repeat, second_backup = migrate(root)
            self.assertEqual("already_v3", repeat)
            self.assertIsNone(second_backup)


if __name__ == "__main__":
    unittest.main()
