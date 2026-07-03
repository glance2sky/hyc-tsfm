from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from research_journal import append_event, build_experiment_event, build_file_record, ensure_branch_journal  # type: ignore


class ResearchJournalTests(unittest.TestCase):
    def test_ensure_branch_journal_creates_jsonl_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jsonl_path, md_path = ensure_branch_journal(root, "electricity-hyc")

            self.assertTrue(jsonl_path.exists())
            self.assertTrue(md_path.exists())
            self.assertIn("# Activity Journal: electricity-hyc", md_path.read_text(encoding="utf-8"))
            self.assertIn("## Timeline", md_path.read_text(encoding="utf-8"))

    def test_append_event_writes_structured_json_and_markdown_timeline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event = {
                "timestamp": "2026-07-02T10:00:00",
                "branch": "electricity-hyc",
                "event_type": "change",
                "summary": "Adjusted adapter width",
                "reason": "Test whether additional capacity improves multivariate structure modeling.",
                "files": [
                    build_file_record(
                        path="configs/branches/electricity-hyc/electricity_hyc.yaml",
                        purpose="Increase adapter_dim for the branch experiment.",
                        change_type="modified",
                    )
                ],
            }

            jsonl_path, md_path = ensure_branch_journal(root, "electricity-hyc")
            append_event(root, "electricity-hyc", event)

            rows = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(rows[0]["summary"], "Adjusted adapter width")
            md_text = md_path.read_text(encoding="utf-8")
            self.assertIn("Adjusted adapter width", md_text)
            self.assertIn("Increase adapter_dim for the branch experiment.", md_text)

    def test_build_experiment_event_includes_result_locations(self) -> None:
        event = build_experiment_event(
            branch="electricity-hyc",
            git_branch="research/electricity-hyc",
            run_id="2026-07-02_101500",
            config_path="configs/branches/electricity-hyc/electricity_hyc.yaml",
            metrics={
                "status": "keep",
                "mse": 0.1234,
                "mae": 0.2345,
                "notes": "Improved over Euclidean control.",
            },
            run_dir="runs/2026-07-02_101500",
        )

        self.assertEqual(event["event_type"], "experiment_run")
        self.assertEqual(event["result"]["metrics_path"], "runs/2026-07-02_101500/metrics.json")
        self.assertEqual(event["result"]["summary_path"], "runs/2026-07-02_101500/summary.md")
        self.assertEqual(event["result"]["status"], "keep")


if __name__ == "__main__":
    unittest.main()
