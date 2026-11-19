import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def load_lookup():
    path = ROOT / "skills/triage-order/scripts/lookup_order.py"
    spec = importlib.util.spec_from_file_location("lookup_order", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkshopTests(unittest.TestCase):
    def test_lookup_keeps_paid_and_pending_separate(self):
        orders = json.loads((ROOT / "fixtures/orders.json").read_text())
        output = load_lookup().summarize("1042", orders["1042"])
        self.assertEqual(output["captured_cents"], 2500)
        self.assertEqual(output["pending_cents"], 2500)

    def test_hook_accepts_only_drafts_for_its_save_tool(self):
        command = [sys.executable, str(ROOT / "hooks/protect_draft_location.py")]
        for path, status in (("1042.md", 2), ("drafts/1042.md", 0), ("drafts/../1042.md", 2)):
            with self.subTest(path=path):
                result = subprocess.run(command, input=json.dumps({
                    "tool_name": "mcp__brickbox__save_handoff", "tool_input": {"path": path},
                }), text=True, capture_output=True)
                self.assertEqual(result.returncode, status)

    def test_new_folders_keep_previous_work(self):
        with tempfile.TemporaryDirectory() as parent:
            folder = Path(parent) / "practice folder"
            command = [sys.executable, str(ROOT / "tools/start.py"), "2-before", "--at", str(folder)]
            subprocess.run(command, check=True, capture_output=True)
            note = folder / "my-work.md"
            note.write_text("keep this")
            duplicate = subprocess.run(command, capture_output=True)
            self.assertEqual(duplicate.returncode, 1)
            self.assertEqual(note.read_text(), "keep this")
            self.assertTrue((folder / ".agents/skills/triage-order/SKILL.md").exists())

    def test_rules_lab_has_a_starting_support_folder(self):
        with tempfile.TemporaryDirectory() as parent:
            folder = Path(parent) / "rule-lab"
            command = [sys.executable, str(ROOT / "tools/start.py"), "3-before", "--at", str(folder)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertTrue((folder / "support/order-1058-shipping.md").is_file())
            self.assertFalse((folder / "AGENTS.md").exists())

    def test_clef_recorder_surfaces_missing_credentials(self):
        env = os.environ.copy()
        env.pop("CLOUDFLARE_ACCOUNT_ID", None)
        env.pop("CLOUDFLARE_API_TOKEN", None)
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/measure.py"), "clef"],
            env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLOUDFLARE_ACCOUNT_ID", result.stderr)
        self.assertIn("CLOUDFLARE_API_TOKEN", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
