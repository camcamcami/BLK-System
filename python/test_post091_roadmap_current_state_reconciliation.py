import unittest
from pathlib import Path

from blk_current_state_authority_index import build_current_state_authority_index, evaluate_current_state_authority_index

ROOT = Path(__file__).resolve().parents[1]
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
BLK092 = ROOT / "docs" / "BLK-092_post-091-roadmap-current-state-reconciliation.md"


class Post091RoadmapCurrentStateReconciliationTest(unittest.TestCase):
    def test_blk092_reconciliation_doc_pins_non_authority_boundary(self):
        self.assertTrue(BLK092.exists(), "BLK-092 reconciliation doc missing")
        text = BLK092.read_text()
        required = [
            "BLK_SYSTEM_092_POST_091_ROADMAP_CURRENT_STATE_RECONCILED",
            "POST_091_RECONCILIATION_ONLY_NO_APPROVAL_CAPTURE",
            "NEXT_EXACT_FRONTIER_AFTER_092_REQUIRES_SEPARATE_AUTHORITY_DECISION",
            "BLK_SYSTEM_092_GRANTS_NO_DRIFT_REVIEW_APPROVAL_OR_EXECUTION",
            "BLK_SYSTEM_092_GRANTS_NO_RTM_DRIFT_REJECTION_APPROVAL_OR_EXECUTION",
            "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001",
            "EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED",
            "does not capture drift-review approval",
            "does not capture RTM drift-rejection approval",
            "does not execute drift review",
            "does not execute RTM drift rejection",
            "no protected-body reads or hashing",
            "no external ledger mutation",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [])

    def test_roadmap_and_index_have_post092_reconciled_selection_markers(self):
        for path in (BLK077, BLK079):
            text = path.read_text()
            with self.subTest(path=path.name):
                required = [
                    "BLK_SYSTEM_092_POST_091_ROADMAP_CURRENT_STATE_RECONCILED",
                    "POST_091_RECONCILIATION_ONLY_NO_APPROVAL_CAPTURE",
                    "Next exact frontier after BLK-SYSTEM-092",
                    "BLK-SYSTEM-093 — RTM Drift-Rejection Approval Decision Capture",
                    "requires a separate exact sprint",
                    "does not capture drift-review approval",
                    "does not capture RTM drift-rejection approval",
                    "does not execute drift review",
                    "does not execute RTM drift rejection",
                ]
                missing = [marker for marker in required if marker not in text]
                self.assertEqual(missing, [])

    def test_executable_index_exposes_blk092_reconciliation_surface_without_authority(self):
        record = build_current_state_authority_index()
        evaluated = evaluate_current_state_authority_index(record)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}
        surface = by_surface["BLK-092 post-091 roadmap/current-state reconciliation"]
        self.assertEqual(surface["state"], "post091_roadmap_current_state_reconciliation_l0_l1_complete")
        self.assertEqual(surface["maturity"], "L0_L1_POST091_RECONCILIATION_DOCTRINE_GATE")
        self.assertIn("BLK-092", surface["governing_docs"])
        self.assertIn("docs/BLK-092_post-091-roadmap-current-state-reconciliation.md", surface["authority_cutline"])
        self.assertIn("does not capture drift-review approval", surface["authority_cutline"])
        self.assertIn("does not capture RTM drift-rejection approval", surface["authority_cutline"])
        self.assertIn("does not execute drift review", surface["authority_cutline"])
        self.assertIn("does not execute RTM drift rejection", surface["authority_cutline"])
        self.assertIn("no protected-body reads or hashing", surface["authority_cutline"])
        self.assertIn("no external ledger mutation", surface["authority_cutline"])
        for denied in [
            "no active-vault hash comparison",
            "no target-repo scan or mutation",
            "no source/Git mutation",
            "no BEB dispatch or BEO closeout execution",
            "no BLK-test/Codex/BLK-pipe runtime grant",
            "no tooling or sandbox claim",
        ]:
            self.assertIn(denied, surface["authority_cutline"])

    def test_stale_post088_next_frontier_phrases_are_not_active(self):
        stale = [
            "After BLK-SYSTEM-088, any RTM generation still requires",
            "one exact human RTM generation approval decision for the BLK-SYSTEM-088 request package",
            "These are remaining gaps after BLK-SYSTEM-088",
            "the next architecture-development movement must name an exact RTM generation approval decision",
        ]
        for path in (BLK077, BLK079):
            text = path.read_text()
            for phrase in stale:
                self.assertNotIn(phrase, text, f"{path.name} still has stale phrase {phrase}")

    def test_reconciliation_doc_has_balanced_markdown_fences(self):
        text = BLK092.read_text()
        fence = chr(96) * 3
        self.assertEqual(text.count(fence) % 2, 0)


if __name__ == "__main__":
    unittest.main()
