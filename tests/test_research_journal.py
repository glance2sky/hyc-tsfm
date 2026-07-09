from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from research_journal import (  # type: ignore
    append_event,
    build_experiment_event,
    build_file_record,
    build_literature_event,
    build_observation_event,
    build_structure_proposal_event,
    ensure_branch_journal,
)


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

    def test_build_observation_event_tracks_indicators_and_takeaway(self) -> None:
        event = build_observation_event(
            branch="electricity-hyc",
            git_branch="research/electricity-hyc",
            summary="Observed gate saturation in adapter input fusion",
            reason="Validation loss plateaued while fusion gate values collapsed near 0.",
            stage="training",
            indicators={
                "fusion_gate_mean": "0.03",
                "adapter_grad_norm": "1.8e-4",
                "backbone_grad_norm": "0.0",
            },
            takeaway="Input fusion is under-utilizing the adapter signal.",
        )

        self.assertEqual(event["event_type"], "observation")
        self.assertEqual(event["observation"]["stage"], "training")
        self.assertEqual(event["observation"]["indicators"]["fusion_gate_mean"], "0.03")
        self.assertIn("under-utilizing", event["observation"]["takeaway"])

    def test_build_literature_event_captures_paper_and_actionable_conclusion(self) -> None:
        event = build_literature_event(
            branch="electricity-hyc",
            git_branch="research/electricity-hyc",
            title="Example Paper on Adapter Gating",
            source="https://example.org/paper",
            finding="Collapsed gates can be mitigated with residual bypass or temperature scaling.",
            implication="Consider adding a residual bypass around the gate.",
        )

        self.assertEqual(event["event_type"], "literature")
        self.assertEqual(event["literature"]["title"], "Example Paper on Adapter Gating")
        self.assertIn("residual bypass", event["literature"]["implication"])

    def test_build_structure_proposal_event_links_target_and_evidence(self) -> None:
        event = build_structure_proposal_event(
            branch="electricity-hyc",
            git_branch="research/electricity-hyc",
            summary="Add residual bypass around input fusion gate",
            reason="Observed gate saturation and literature both suggest the adapter path is being over-suppressed.",
            target="input_fusion_gate",
            expected_effect="Improve adapter signal flow without changing the frozen backbone.",
            evidence_refs=[
                "research/activity/electricity-hyc.md#observation-1",
                "research/activity/electricity-hyc.md#literature-1",
            ],
        )

        self.assertEqual(event["event_type"], "structure_proposal")
        self.assertEqual(event["proposal"]["target"], "input_fusion_gate")
        self.assertEqual(len(event["proposal"]["evidence_refs"]), 2)

    def test_append_event_renders_observation_and_proposal_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ensure_branch_journal(root, "electricity-hyc")
            observation = build_observation_event(
                branch="electricity-hyc",
                git_branch="research/electricity-hyc",
                summary="Observed low gradient flow in hyperbolic encoder",
                reason="Gradient norms stayed near zero for multiple steps.",
                stage="training",
                indicators={"encoder_grad_norm": "9.0e-6"},
                takeaway="The encoder may be over-constrained or under-connected.",
            )
            proposal = build_structure_proposal_event(
                branch="electricity-hyc",
                git_branch="research/electricity-hyc",
                summary="Insert residual projection before Lorentz mapping",
                reason="Increase learnable Euclidean flexibility before hyperbolic projection.",
                target="lorentz_encoder",
                expected_effect="Improve gradient flow into the hyperbolic adapter stack.",
                evidence_refs=["obs-1"],
            )

            append_event(root, "electricity-hyc", observation)
            append_event(root, "electricity-hyc", proposal)

            md_text = (root / "research" / "activity" / "electricity-hyc.md").read_text(encoding="utf-8")
            self.assertIn("encoder_grad_norm", md_text)
            self.assertIn("lorentz_encoder", md_text)
            self.assertIn("Improve gradient flow", md_text)


if __name__ == "__main__":
    unittest.main()
