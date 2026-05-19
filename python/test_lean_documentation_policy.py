from pathlib import Path
import re
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
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_PACKAGE_REQUIRED_NOT_EXECUTED",
            "BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED",
            "BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED",
            "BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY",
            "BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY",
            "BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY",
            "BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED",
            "BLK_SYSTEM_259_EXACT_BEO_PUBLICATION_APPROVAL_PREFLIGHT_RECORDED",
            "BLK_SYSTEM_258_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY",
            "BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY",
                    "BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY",
            "BLK_SYSTEM_250_BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY",
            "BLK_SYSTEM_249_EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY",
            "BLK_SYSTEM_248_REUSABLE_BEO_PUBLICATION_CONTRACT_READY",
            "BLK_SYSTEM_247_REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED",
            "BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY",
            "BLK_SYSTEM_245_BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY",
            "BLK_SYSTEM_244_METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY",
            "BLK_SYSTEM_243_PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY",
            "BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED",
            "BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY",
            "BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY",
            "BLK_SYSTEM_239_BLK_ID_RELAY_SCOPE_DECIDED",
            "BLK_SYSTEM_238_ROOT_DOCTRINE_DEVIATION_OVERLAY_READY",
            "BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY",
            "BLK_SYSTEM_235_AGENT_A_CONTEXT_PACKET_PR_MERGED",
            "BLK_SYSTEM_234_REPEAT_KURONODE_FEATURE_DROP_EXECUTED",
            "BLK_SYSTEM_233_CODEX_PROGRESS_EVENTS_READY",
            "BLK_SYSTEM_232_BEB_L2_PACKET_HELPER_READY",
            "BLK_SYSTEM_231_AGENT_A_HEADER_PR_MERGED",
            "BLK_SYSTEM_230_AGENT_A_HEADER_DROP_EXECUTED",
            "BLK_SYSTEM_229_PRIVATE_BWRAP_WORKSPACE_WRITE_SETUP_READY",
            "BLK_SYSTEM_228_EXACT_KURONODE_CLEAN_WORKTREE_FEATURE_DROP_EXECUTED",
            "BLK_SYSTEM_227_EXTERNAL_CODEX_ARTIFACT_READY",
            "BLK_SYSTEM_226_KURONODE_WORKTREE_STATIC_PROFILE_READY",
            "BLK_SYSTEM_225_CLEAN_WORKTREE_MANIFEST_READY",
            "BLK_SYSTEM_224_IGNORED_RESIDUE_CLEANUP_PLAN_READY",
            "BLK_SYSTEM_223_BEB_L2_PREFLIGHT_GUARD_READY",
            "BLK_SYSTEM_222_BEB_L2_BLK_PIPE_CODEX_ROUTE_READY",
            "BLK_SYSTEM_221_FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
            "BLK_SYSTEM_220_NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED",
            "BLK_SYSTEM_219_NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED",
            "BLK_SYSTEM_218_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
            "BLK_SYSTEM_217_CODEX_EXACT_UNDO_EXERCISE_RECORDED",
            "BLK_SYSTEM_216_CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED",
            "BLK_SYSTEM_215_SUPERVISED_CODEX_KURONODE_FEATURE_LOOP_EXECUTED",
            "BLK_SYSTEM_214_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED",
            "BLK_SYSTEM_213_BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY",
            "BLK_SYSTEM_212_VALIDATION_PROFILE_RECONCILED_CLEAN",
            "BLK_SYSTEM_211_VALIDATION_PROFILE_CONTRACT_READY",
            "BLK_SYSTEM_210_VALIDATION_PROFILE_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_209_PYTHON_ADAPTER_RECONCILED_CLEAN",
            "BLK_SYSTEM_208_PYTHON_ADAPTER_CONTRACT_READY",
            "BLK_SYSTEM_207_PYTHON_ADAPTER_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_206_BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN",
            "BLK_SYSTEM_205_BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY",
            "BLK_SYSTEM_204_BLK_PIPE_SURFACE_REVIEW_READY",
            "BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN",
            "BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
            "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
            "BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY",
            "BLK_SYSTEM_199_BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN",
            "BLK_SYSTEM_198_BLK_REQ_GATEWAY_HOSTILE_INPUTS_HARDENED",
            "BLK_SYSTEM_197_BLK_REQ_EXACT_ID_LIFECYCLE_SMOKE_PASSED",
            "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
            "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
            "BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN",
            "BLK_SYSTEM_193_REPEATABLE_TRUSTED_BLK_LINK_REPEAT_RUNS_RECORDED_CLEAN",
            "BLK_SYSTEM_192_REPEATABLE_TRUSTED_BLK_LINK_LEDGER_READY",
            "BLK_SYSTEM_191_REPEATABLE_TRUSTED_BLK_LINK_CONTRACT_EMITTED",
            "BLK_SYSTEM_190_REPEATABLE_TRUSTED_BLK_LINK_POST_RUN_REVIEW_CLEAN",
            "BLK_SYSTEM_189_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECONCILED_CLEAN",
            "BLK_SYSTEM_188_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_EXECUTION_RECORDED",
            "BLK_SYSTEM_187_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_REQUEST_READY",
            "BLK_SYSTEM_186_REUSABLE_BLK_LINK_READINESS_KERNEL_RECONCILED_CLEAN",
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
        self.assertLessEqual(len(text.splitlines()), 188)
        for marker in [
            "Root-Doctrine Gap Coverage and Proposed Sequence",
            "Convenience/product lane, not a dependency",
            "Conceptual cleanup",
            "Real dependency for reusable HITL/runtime authority",
            "full reusable BLK-003 autonomous loop",
            "production BLK-test MCP",
            "reusable BEO publication",
            "RTM / production `blk-link` drift and coverage truth",
        ]:
            self.assertIn(marker, text)
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

    def test_current_state_block_has_no_duplicate_blk_system_markers(self):
        text = BLK079.read_text()
        marker_block = re.search(r"## 2\. Current State\n```text\n(.*?)\n```", text, re.DOTALL)
        self.assertIsNotNone(marker_block)
        if marker_block is None:
            self.fail("current-state marker block missing")
        markers = re.findall(r"BLK_SYSTEM_\d+_[A-Z0-9_]+", marker_block.group(1))
        duplicates = sorted({marker for marker in markers if markers.count(marker) > 1})
        self.assertEqual(duplicates, [])

    def test_new_sprints_use_one_outcome_only(self):
        for sprint in range(121, 266):
            task_outcomes = list((DOCS / "outcomes").glob(f"BLK-SYSTEM-{sprint}_task-*-outcome.md"))
            self.assertEqual(task_outcomes, [], f"BLK-SYSTEM-{sprint} has per-task outcomes")
        for sprint in range(122, 266):
            blk_docs = list(DOCS.glob(f"BLK-{sprint}_*.md"))
            self.assertEqual(blk_docs, [], f"BLK-{sprint} sprint doc should not exist")
            closeout = DOCS / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            self.assertTrue(closeout.exists(), f"BLK-SYSTEM-{sprint} closeout missing")
    def test_current_closeouts_do_not_keep_pending_verification_or_review_placeholders(self):
        for sprint in range(172, 266):
            path = DOCS / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md"
            text = path.read_text()
            lowered = text.casefold()
            for stale in [
                "pending final rerun",
                "will be patched",
                "will be rerun",
                "final hostile review pending",
                "hostile review is pending",
                "independent hostile review is pending",
                "pending final closeout verification",
                "recorded after the closeout is finalized",
                "preliminary review conclusion",
                "part of final",
                "final independent hostile review",
                "commit closeout",
                "after the full closeout pass",
                "final package verification section",
            ]:
                self.assertNotIn(stale, lowered, path.name)


if __name__ == "__main__":
    unittest.main()
