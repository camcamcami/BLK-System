from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLK077 = DOCS / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = DOCS / "BLK-079_post-078-current-state-authority-index.md"
ROOT_DOCS = [
    DOCS / "BLK-001_blk-system-master-architecture.md",
    DOCS / "BLK-002_blk-req-artifact-lifecycle.md",
    DOCS / "BLK-003_blk-pipe-blk-test-orchestration.md",
    DOCS / "BLK-004_blk-pipe-v47-architecture-suite.md",
    DOCS / "BLK-005_blk-req-specification.md",
    DOCS / "BLK-006_blk-req-implementation-brief.md",
]


class LeanDocumentationPolicyTest(unittest.TestCase):
    def test_active_roadmap_is_occam_focused_and_controls_doc_burden(self):
        text = BLK077.read_text()
        required = [
            "LEAN_DOCUMENTATION_MODEL_ACTIVE",
            "NO_BLK_DOC_PER_SPRINT",
            "ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS",
            "BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE",
            "ROADMAP_OCCAM_PRODUCTION_ONLY",
            "NEXT_FRONTIER_NARROW_POST_RTM_AUTHORITY_DECISION_NOT_GRANTED",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [])
        self.assertLessEqual(len(text.splitlines()), 140)
        self.assertNotIn("task-000", text.lower())
        self.assertNotIn("task-001", text.lower())

    def test_root_docs_are_fixed_overview_not_sprint_state_surfaces(self):
        forbidden = ["BLK-SYSTEM-", "BLK-PIPE-008", "Current-State Overlay", "current-state overlay"]
        for path in ROOT_DOCS:
            text = path.read_text()
            self.assertIn("BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE", text, path.name)
            self.assertIn("stable overview/contract surface", text, path.name)
            leaks = [marker for marker in forbidden if marker in text]
            self.assertEqual(leaks, [], path.name)

    def test_current_state_index_knows_lean_policy_without_becoming_sprint_plan(self):
        text = BLK079.read_text()
        for marker in [
            "LEAN_DOCUMENTATION_MODEL_ACTIVE",
            "NO_BLK_DOC_PER_SPRINT",
            "ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS",
            "BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE",
        ]:
            self.assertIn(marker, text)
        self.assertIn("This document is not a sprint plan", text)

    def test_new_sprints_use_one_outcome_only(self):
        for sprint in (121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144):
            task_outcomes = list((DOCS / "outcomes").glob(f"BLK-SYSTEM-{sprint}_task-*-outcome.md"))
            self.assertEqual(task_outcomes, [], f"BLK-SYSTEM-{sprint} has per-task outcomes")
        for sprint in (122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144):
            blk_docs = list(DOCS.glob(f"BLK-{sprint}_*.md"))
            self.assertEqual(blk_docs, [], f"BLK-{sprint} sprint doc should not exist")
            closeout = DOCS / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            self.assertTrue(closeout.exists(), f"BLK-SYSTEM-{sprint} closeout missing")


if __name__ == "__main__":
    unittest.main()
