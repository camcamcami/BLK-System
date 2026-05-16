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
            "NEXT_FRONTIER_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_REQUEST_NOT_GRANTED",
            "BLK_SYSTEM_186_REUSABLE_BLK_LINK_READINESS_KERNEL_RECONCILED_CLEAN",
            "BLK_SYSTEM_185_REUSABLE_BLK_LINK_READINESS_KERNEL_DRY_RUN_RECORDED",
            "BLK_SYSTEM_184_REUSABLE_BLK_LINK_READINESS_KERNEL_CONTRACT_EMITTED",
            "BLK_SYSTEM_183_REUSABLE_BLK_LINK_READINESS_KERNEL_DECISION_READY",
            "BLK_SYSTEM_182_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_EXPORT_RECONCILED_CLEAN",
            "BLK_SYSTEM_181_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_METADATA_EXPORT_EMITTED",
            "BLK_SYSTEM_180_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_RECONCILED_CLEAN",
            "BLK_SYSTEM_179_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_EXECUTION_RECORDED",
            "BLK_SYSTEM_178_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_AUTHORITY_REQUEST_READY",
            "BLK_SYSTEM_177_AUTHORITY_LAUNDERING_BYPASS_HARDENED",
            "BLK_SYSTEM_176_RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_INTEGRATED",
            "BLK_SYSTEM_175_PROTECTED_BODY_VERIFICATION_DECISION_EXECUTION_RECORDED",
            "BLK_SYSTEM_174_PROTECTED_BODY_VERIFICATION_DECISION_AUTHORITY_REQUEST_READY",
            "BLK_SYSTEM_173_METADATA_BOUND_DRIFT_COVERAGE_DECISION_RECONCILED_CLEAN",
            "BLK_SYSTEM_172_METADATA_BOUND_DRIFT_COVERAGE_DECISION_EXECUTION_RECORDED",
            "BLK_SYSTEM_170_ACTIVE_VAULT_HASH_COMPARISON_RECONCILED_CLEAN",
            "BLK_SYSTEM_169_ACTIVE_VAULT_HASH_COMPARISON_DECISION_EXECUTION_RECORDED",
            "BLK_SYSTEM_168_ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_READY",
            "BLK_SYSTEM_167_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_RUN_RECONCILED_CLEAN",
            "BLK_SYSTEM_166_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_DECISION_EXECUTION_RECORDED",
            "BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY",
            "BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED",
            "BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED",
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
        for sprint in range(121, 187):
            task_outcomes = list((DOCS / "outcomes").glob(f"BLK-SYSTEM-{sprint}_task-*-outcome.md"))
            self.assertEqual(task_outcomes, [], f"BLK-SYSTEM-{sprint} has per-task outcomes")
        for sprint in range(122, 187):
            blk_docs = list(DOCS.glob(f"BLK-{sprint}_*.md"))
            self.assertEqual(blk_docs, [], f"BLK-{sprint} sprint doc should not exist")
            closeout = DOCS / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            self.assertTrue(closeout.exists(), f"BLK-SYSTEM-{sprint} closeout missing")
    def test_current_closeouts_do_not_keep_pending_verification_or_review_placeholders(self):
        for sprint in range(172, 187):
            path = DOCS / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            text = path.read_text()
            for stale in [
                "Pending final rerun",
                "will be patched",
                "Final hostile review pending",
                "part of final",
                "Final independent hostile review",
                "commit closeout",
            ]:
                self.assertNotIn(stale, text, path.name)


if __name__ == "__main__":
    unittest.main()
