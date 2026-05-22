import ast
import unittest
from pathlib import Path

from blk_current_state_authority_index import (
    DEFAULT_SURFACES,
    DENIED_FLAGS as INDEX_DENIED_FLAGS,
    DOC_DENIAL_MARKERS,
    build_current_state_authority_index,
    evaluate_current_state_authority_index,
    validate_active_current_state_docs,
    validate_current_state_authority_index,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_current_state_authority_index.py"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"

EXPECTED_SURFACES = {
    "BLK-req legislative gateway",
    "BLK-pipe blast shield",
    "Python adapter layer",
    "Validation profiles",
    "BLK-test",
    "Operator health / observability",
    "Codex live-dispatch ladder",
    "BEO publication path",
    "RTM / blk-link",
    "Identity / relay provenance spine",
}

DENIED_FLAGS = [
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "authoritative_beo_publication_authorized",
    "reusable_beo_publication_authorized",
    "beo_publication_signer_reuse_authorized",
    "beo_publication_storage_reuse_authorized",
    "beo_publication_ledger_reuse_authorized",
    "rollback_revocation_supersession_authorized",
    "runtime_rtm_generation_authorized",
    "reusable_rtm_generation_authorized",
    "production_blk_link_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_coverage_truth_authorized",
    "active_vault_comparison_authorized",
    "protected_blk_req_body_reads_authorized",
    "protected_blk_req_body_copy_authorized",
    "protected_blk_req_body_parse_authorized",
    "protected_blk_req_body_hash_authorized",
    "protected_blk_req_body_scan_authorized",
    "target_source_git_mutation_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
]

CURRENT_REQUIRED_MARKERS = [
    "BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED",
    "NEXT_FRONTIER_BLK_SYSTEM_DEVELOPMENT_WORK_UNBLOCKED_INTERNAL_GATES_DISTINGUISHED",
    "sha256:57cdc2e0fdb4c4d5fe31ec3731eccecb5a3f34e783c6f7c51f27c0101b2bdf39",
    "BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED",
    "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_DECISION_SPLIT_REQUIRED_BROAD_APPROVAL_REJECTED_NOT_GRANTED",
    "sha256:d18946139c9c9565aa542db12edb816bc01dcbf67d1bb62ff53232c17a11e1b0",
    "BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY",
    "NEXT_FRONTIER_FUNCTIONAL_9_EXACT_BEO_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED",
    "sha256:05bf576178f5e848c2b98a70eae42873916f00ee816ce51f3744d575466cae4a",
    "BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED",
    "NEXT_FRONTIER_9_OF_10_OVERALL_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_323_BEB_L2_ROUTE_ARTIFACT_BOUNDARY_HARDENED",
    "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
    "NEXT_FRONTIER_9_9_FIRST_PASS_OPERATOR_REVIEW_AND_VERIFICATION_GAPS_NOT_10_OF_10",
    "BLK_SYSTEM_321_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED",
    "NEXT_FRONTIER_BLK_SYSTEM_9_OF_10_REPO_DEVELOPMENT_READY_SIDE_EFFECT_APPROVALS_SEPARATE_NOT_GRANTED",
    "BLK_SYSTEM_320_9_OF_10_READINESS_MATRIX_READY",
    "BLK_SYSTEM_319_DEVELOPMENT_DIRECTIVE_GUARD_RECORDED",
    "BLK_SYSTEM_318_EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY",
    "BLK_SYSTEM_317_9_OF_10_DEVELOPMENT_FRONTIER_BOUND",
    "BLK_SYSTEM_316_STANDING_BLK_SYSTEM_DEVELOPMENT_APPROVAL_RECORDED",
    "BLK_SYSTEM_315_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED",
    "BLK_SYSTEM_313_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED",
    "BLK_SYSTEM_312_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED",
    "BLK_SYSTEM_311_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY",
    "BLK_SYSTEM_310_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
    "BLK_SYSTEM_309_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED",
    "BLK_SYSTEM_308_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED",
    "BLK_SYSTEM_307_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY",
    "BLK_SYSTEM_306_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY",
    "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CAPTURE_AND_BOUNDED_EXECUTION_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
    "BLK_SYSTEM_304_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED",
    "BLK_SYSTEM_303_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY",
    "BLK_SYSTEM_302_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY",
    "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED",
    "NEXT_FRONTIER_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED",
    "BLK_SYSTEM_300_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED",
    "BLK_SYSTEM_299_EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY",
    "BLK_SYSTEM_298_EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY",
    "NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED",
    "BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED",
    "BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY",
    "BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY",
    "BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED",
    "BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY",
    "BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY",
    "BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY",
    "NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_289_PROMOTION_PURGE_STALE_GATE_READY",
    "BLK_SYSTEM_288_SPECULATIVE_QUARANTINE_EVIDENCE_READY",
    "BLK_SYSTEM_287_HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY",
    "BLK_SYSTEM_286_SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY",
    "NEXT_FRONTIER_REUSABLE_BLK003_LOOP_REQUEST_PATH_WITH_QUARANTINE_GATE_NOT_GRANTED",
    "BLK_SYSTEM_285_IDENTITY_RELAY_LOOP_EVIDENCE_READY",
    "BLK_SYSTEM_284_BLK_RELAY_ENVELOPE_CONTRACT_READY",
    "BLK_SYSTEM_283_BLK_IDENTITY_SPINE_CONTRACT_READY",
    "NEXT_FRONTIER_HITL_GATEWAY_IDENTITY_RELAY_WIRING_NOT_GRANTED",
    "BLK_SYSTEM_282_AGENT_A_REQUIREMENT_CONTEXT_SUMMARY_FEATURE_DROP_EXECUTED",
    "BLK_SYSTEM_281_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED",
    "BLK_SYSTEM_280_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY",
    "BLK_SYSTEM_279_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
    "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_278_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED",
    "BLK_SYSTEM_277_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY",
    "BLK_SYSTEM_276_RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED",
    "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_275_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED",
    "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED",
    "BLK_SYSTEM_273_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY",
    "BLK_SYSTEM_272_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY",
    "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_BOUND_APPROVE_OR_EXACT_TEXT_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_271_EXACT_BEO_PUBLICATION_FINALITY_RECONCILED",
    "BLK_SYSTEM_270_EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED",
    "BLK_SYSTEM_269_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED",
    "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_AFTER_EXACT_BEO_PUBLICATION",
    "BLK_SYSTEM_268_EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED",
    "BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_BLOCKED",
    "BLK_SYSTEM_266_EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY",
    "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED",
    "BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED",
    "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_PACKAGE_REQUIRED_NOT_EXECUTED",
    "BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY",
    "BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY",
    "BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY",
    "BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED",
    "BLK_SYSTEM_259_EXACT_BEO_PUBLICATION_APPROVAL_PREFLIGHT_RECORDED",
    "BLK_SYSTEM_258_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY",
    "BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY",
    "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED",
    "BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED",
    "BLK_SYSTEM_255_EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_RECORDED",
    "BLK_SYSTEM_254_DRIFT_COVERAGE_VERIFIER_CONTRACT_READY",
    "BLK_SYSTEM_253_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED",
    "BLK_SYSTEM_252_RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_READY",
    "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED",
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
    "BLK_SYSTEM_171_METADATA_BOUND_DRIFT_COVERAGE_DECISION_AUTHORITY_REQUEST_READY",
    "BLK_SYSTEM_170_ACTIVE_VAULT_HASH_COMPARISON_RECONCILED_CLEAN",
    "BLK_SYSTEM_169_ACTIVE_VAULT_HASH_COMPARISON_DECISION_EXECUTION_RECORDED",
    "BLK_SYSTEM_168_ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_READY",
    "BLK_SYSTEM_167_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_RUN_RECONCILED_CLEAN",
    "BLK_SYSTEM_166_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_DECISION_EXECUTION_RECORDED",
    "BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY",
    "BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED",
    "BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED",
]
RTM_REQUIRED_MARKERS = [
    "BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN",
    "BLK_SYSTEM_193_REPEATABLE_TRUSTED_BLK_LINK_REPEAT_RUNS_RECORDED_CLEAN",
    "BLK_SYSTEM_192_REPEATABLE_TRUSTED_BLK_LINK_LEDGER_READY",
    "BLK_SYSTEM_191_REPEATABLE_TRUSTED_BLK_LINK_CONTRACT_EMITTED",
    "BLK_SYSTEM_190_REPEATABLE_TRUSTED_BLK_LINK_POST_RUN_REVIEW_CLEAN",
    "BLK_SYSTEM_189_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECONCILED_CLEAN",
]


class CurrentStateAuthorityIndexTest(unittest.TestCase):
    def test_default_index_ready_for_operator_review_not_authority(self):
        record = build_current_state_authority_index()

        self.assertEqual(record["index_id"], "blk_system_current_state_authority_index")
        self.assertEqual(record["index_status"], "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX")
        self.assertEqual(record["roadmap_source"], "BLK-077")
        self.assertEqual(record["maturity"], "CURRENT_STATE_INDEX_L0_L1_ONLY")

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(evaluated["validation_errors"], [])

    def test_every_current_authority_surface_present_exactly_once_without_sprint_catalog(self):
        record = build_current_state_authority_index()
        names = [surface["surface"] for surface in record["surfaces"]]

        self.assertEqual(set(names), EXPECTED_SURFACES)
        self.assertEqual(len(names), len(set(names)))
        self.assertLessEqual(len(names), 10, "current-state index must not become a historical sprint catalog")

    def test_current_surface_cutlines_are_concise_and_non_authorizing(self):
        record = build_current_state_authority_index()
        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}

        for surface in record["surfaces"]:
            with self.subTest(surface=surface["surface"]):
                self.assertIn("BLK-077", surface["governing_docs"])
                self.assertLessEqual(
                    len(surface["authority_cutline"]),
                    900,
                    f"{surface['surface']} authority cutline is too long for lean current-state use",
                )
                self.assertNotRegex(surface["authority_cutline"], r"BLK_SYSTEM_12[0-9].*BLK_SYSTEM_13[0-9].*BLK_SYSTEM_14[0-9]")

        rtm_link = by_surface["RTM / blk-link"]
        self.assertEqual(rtm_link["state"], "rtm_blk_link_drift_coverage_281_second_refresh_challenge_reconciled_approval_required")
        self.assertEqual(rtm_link["maturity"], "L2_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_281_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_280_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_279_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_278_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN", rtm_link["authority_cutline"])
        self.assertIn("second refreshed bounded short Approve challenge", rtm_link["authority_cutline"])
        self.assertIn("No blanket production `blk-link`", rtm_link["authority_cutline"])
        self.assertIn("no RTM generation", rtm_link["authority_cutline"])
        self.assertIn("no reusable RTM generation", rtm_link["authority_cutline"])
        self.assertIn("no run-ID reservation or consumption", rtm_link["authority_cutline"])

        blk_pipe = by_surface["BLK-pipe blast shield"]
        self.assertEqual(blk_pipe["state"], "blk_pipe_bounded_enforcement_206_closed")
        self.assertEqual(blk_pipe["maturity"], "L2_BLK_PIPE_BOUNDED_NON_AUTHORIZING_ENFORCEMENT_SURFACE_CLOSED")
        self.assertIn("bounded non-authorizing enforcement surface", blk_pipe["authority_cutline"])
        self.assertIn("No broad dispatch", blk_pipe["authority_cutline"])
        self.assertIn("no production-isolation claim", blk_pipe["authority_cutline"])

        identity_relay = by_surface["Identity / relay provenance spine"]
        self.assertEqual(identity_relay["state"], "identity_relay_hitl_quarantine_gate_289_ready")
        self.assertEqual(identity_relay["maturity"], "L2_HITL_QUARANTINE_GATE_READY_NO_DURABLE_MUTATION")
        self.assertIn("BLK_SYSTEM_286_SPECULATIVE_QUARANTINE_APPROVAL_CONTRACT_READY", identity_relay["authority_cutline"])
        self.assertIn("BLK_SYSTEM_287_HITL_INTERACTION_IDENTITY_RELAY_EVIDENCE_READY", identity_relay["authority_cutline"])
        self.assertIn("BLK_SYSTEM_288_SPECULATIVE_QUARANTINE_EVIDENCE_READY", identity_relay["authority_cutline"])
        self.assertIn("BLK_SYSTEM_289_PROMOTION_PURGE_STALE_GATE_READY", identity_relay["authority_cutline"])
        self.assertIn("No relay network runtime", identity_relay["authority_cutline"])
        self.assertIn("no message dispatch", identity_relay["authority_cutline"])
        self.assertIn("no approval reuse", identity_relay["authority_cutline"])
        self.assertIn("no durable target/source/Git mutation", identity_relay["authority_cutline"])

        python_adapter = by_surface["Python adapter layer"]
        self.assertEqual(python_adapter["state"], "exact_quarantine_gated_blk003_loop_execution_297_reconciled")
        self.assertEqual(python_adapter["maturity"], "L3_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECORDED_READY_FOR_BLK_TEST")
        self.assertIn("BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED", python_adapter["authority_cutline"])
        self.assertIn("target-hash recheck", python_adapter["authority_cutline"])
        self.assertIn("private-bwrap descriptor", python_adapter["authority_cutline"])
        self.assertIn("failure ceiling 3", python_adapter["authority_cutline"])
        self.assertIn("no reusable Codex dispatch", python_adapter["authority_cutline"])
        self.assertIn("no production-isolation authority", python_adapter["authority_cutline"])

        validation_profiles = by_surface["Validation profiles"]
        self.assertEqual(validation_profiles["state"], "beb_l2_route_artifact_boundary_323_hardened")
        self.assertEqual(validation_profiles["maturity"], "L2_BEB_L2_ROUTE_ARTIFACT_BOUNDARY_HARDENED_NO_NEW_DISPATCH")
        self.assertIn("BLK_SYSTEM_323_BEB_L2_ROUTE_ARTIFACT_BOUNDARY_HARDENED", validation_profiles["authority_cutline"])
        self.assertIn("protected BEB/L2 artifact paths", validation_profiles["authority_cutline"])
        self.assertIn("processed/failed inbox dirs", validation_profiles["authority_cutline"])
        self.assertIn("BLK_SYSTEM_226_KURONODE_WORKTREE_STATIC_PROFILE_READY", validation_profiles["authority_cutline"])
        self.assertIn("BLK_SYSTEM_212_VALIDATION_PROFILE_RECONCILED_CLEAN", validation_profiles["authority_cutline"])
        self.assertIn("git diff --check -- .", validation_profiles["authority_cutline"])
        self.assertIn("local whitespace/static evidence only", validation_profiles["authority_cutline"])
        self.assertIn("no package manager", validation_profiles["authority_cutline"])
        self.assertIn("no runtime", validation_profiles["authority_cutline"])

        blk_req = by_surface["BLK-req legislative gateway"]
        self.assertEqual(blk_req["state"], "hitl_gateway_speculative_quarantine_gate_289_ready")
        self.assertEqual(blk_req["maturity"], "L2_HITL_QUARANTINE_GATE_READY_NO_DURABLE_MUTATION")
        self.assertIn("BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY", blk_req["authority_cutline"])
        self.assertIn("BLK_SYSTEM_289_PROMOTION_PURGE_STALE_GATE_READY", blk_req["authority_cutline"])
        self.assertIn("Discord component HITL", blk_req["authority_cutline"])
        self.assertIn("no broad active-vault body scan", blk_req["authority_cutline"])
        self.assertIn("No Kuronode source/Git mutation", blk_req["authority_cutline"])

        beo_path = by_surface["BEO publication path"]
        self.assertEqual(beo_path["state"], "development_authority_distinguished_328_internal_gates_not_approval_blockers")
        self.assertEqual(beo_path["maturity"], "L3_BLK_SYSTEM_DEVELOPMENT_AUTHORITY_READY_INTERNAL_GATES_DISTINGUISHED")
        self.assertIn("BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED", beo_path["authority_cutline"])
        self.assertIn("NEXT_FRONTIER_BLK_SYSTEM_DEVELOPMENT_WORK_UNBLOCKED_INTERNAL_GATES_DISTINGUISHED", beo_path["authority_cutline"])
        self.assertIn("sha256:57cdc2e0fdb4c4d5fe31ec3731eccecb5a3f34e783c6f7c51f27c0101b2bdf39", beo_path["authority_cutline"])
        self.assertIn("BLK-System development work unblocked", beo_path["authority_cutline"])
        self.assertIn("internal gates not approval blockers", beo_path["authority_cutline"])
        self.assertIn("BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED", beo_path["authority_cutline"])
        self.assertIn("NEXT_FRONTIER_EXACT_BEO_PUBLICATION_DECISION_SPLIT_REQUIRED_BROAD_APPROVAL_REJECTED_NOT_GRANTED", beo_path["authority_cutline"])
        self.assertIn("sha256:d18946139c9c9565aa542db12edb816bc01dcbf67d1bb62ff53232c17a11e1b0", beo_path["authority_cutline"])
        self.assertIn("broad multi-surface message", beo_path["authority_cutline"])
        self.assertIn("BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY", beo_path["authority_cutline"])
        self.assertIn("NEXT_FRONTIER_FUNCTIONAL_9_EXACT_BEO_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED", beo_path["authority_cutline"])
        self.assertIn("sha256:05bf576178f5e848c2b98a70eae42873916f00ee816ce51f3744d575466cae4a", beo_path["authority_cutline"])
        self.assertIn("7/10 practical baseline", beo_path["authority_cutline"])
        self.assertIn("functional 9/10 target", beo_path["authority_cutline"])
        self.assertIn("Split exact current-BEO decision", beo_path["authority_cutline"])
        self.assertIn("no run-ID reservation/consumption", beo_path["authority_cutline"])
        self.assertIn("no BEO publication", beo_path["authority_cutline"])
        self.assertIn("no reusable BEO publication", beo_path["authority_cutline"])
        self.assertIn("no RTM", beo_path["authority_cutline"])
        self.assertNotIn("capture this record", beo_path["authority_cutline"])
        self.assertNotIn("publication finality path", beo_path["authority_cutline"])
        self.assertNotIn("2026-05-21T20:45:00+10:00", beo_path["authority_cutline"])

    def test_human_index_is_lean_current_state_not_historical_ledger(self):
        text = BLK079.read_text()
        lines = text.splitlines()

        self.assertLessEqual(len(lines), 180, "BLK-079 should be an active current-state map, not a ledger")
        self.assertLessEqual(len(text), 20000, "BLK-079 active index is too large for lean documentation")
        self.assertFalse(any(len(line) > 900 for line in lines), "BLK-079 has ledger-style oversized lines")
        self.assertNotIn("Persistent doctrine gate marker: BLK-SYSTEM-079 pins", text)
        self.assertNotIn("BLK-SYSTEM-125 pins metadata-only BEB/BEO handoff completion; BLK-SYSTEM-126", text)
        self.assertNotIn("Historical next sprint selected after", text)
        self.assertIn("LEAN_CURRENT_STATE_INDEX_ACTIVE", text)
        self.assertNotIn("This sprint closeout", text)
        self.assertNotRegex(text, r"docs/outcomes/BLK-SYSTEM-\\d+_sprint-closeout\\.md")
        self.assertIn("docs/outcomes/", text)
        for surface in EXPECTED_SURFACES:
            self.assertIn(surface, text)
        for marker in CURRENT_REQUIRED_MARKERS:
            self.assertIn(marker, text)

    def test_roadmap_remains_occam_production_request_only(self):
        text = BLK077.read_text()
        self.assertIn("ROADMAP_OCCAM_PRODUCTION_ONLY", text)
        self.assertIn("BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED", text)
        self.assertIn("NEXT_FRONTIER_BLK_SYSTEM_DEVELOPMENT_WORK_UNBLOCKED_INTERNAL_GATES_DISTINGUISHED", text)
        self.assertIn("sha256:57cdc2e0fdb4c4d5fe31ec3731eccecb5a3f34e783c6f7c51f27c0101b2bdf39", text)
        self.assertIn("BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY", text)
        self.assertIn("BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED", text)
        self.assertIn("NEXT_FRONTIER_EXACT_BEO_PUBLICATION_DECISION_SPLIT_REQUIRED_BROAD_APPROVAL_REJECTED_NOT_GRANTED", text)
        self.assertIn("sha256:d18946139c9c9565aa542db12edb816bc01dcbf67d1bb62ff53232c17a11e1b0", text)
        self.assertIn("NEXT_FRONTIER_FUNCTIONAL_9_EXACT_BEO_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED", text)
        self.assertIn("sha256:05bf576178f5e848c2b98a70eae42873916f00ee816ce51f3744d575466cae4a", text)
        self.assertIn("BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED", text)
        self.assertIn("NEXT_FRONTIER_9_OF_10_OVERALL_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED", text)
        self.assertIn("sha256:18f9550996bc0388e67666237c0e95d81906ce30162c184401149eeffb31dd3e", text)
        self.assertIn("7/10 practical baseline", text)
        self.assertIn("9/10 overall target", text)
        self.assertIn("NEXT_FRONTIER_BLK_SYSTEM_9_OF_10_REPO_DEVELOPMENT_READY_SIDE_EFFECT_APPROVALS_SEPARATE_NOT_GRANTED", text)
        self.assertIn("BLK_SYSTEM_321_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED", text)
        self.assertIn("BLK_SYSTEM_320_9_OF_10_READINESS_MATRIX_READY", text)
        self.assertIn("BLK_SYSTEM_319_DEVELOPMENT_DIRECTIVE_GUARD_RECORDED", text)
        self.assertIn("BLK_SYSTEM_318_EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY", text)
        self.assertIn("BLK_SYSTEM_317_9_OF_10_DEVELOPMENT_FRONTIER_BOUND", text)
        self.assertIn("BLK_SYSTEM_316_STANDING_BLK_SYSTEM_DEVELOPMENT_APPROVAL_RECORDED", text)
        self.assertIn("sha256:7237998c0d31ba47ff4972c2177cdb545bb69fed87f3c64f403ade63b9be6d64", text)
        self.assertIn("sha256:87e904afb73319fc0c0dd73ea914f428afdc9c3e035642ae0f2af55ed51782f5", text)
        self.assertNotIn("NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED", text)
        self.assertNotIn("2026-05-21T20:45:00+10:00", text)
        self.assertNotIn("consume at most one run ID", text)
        self.assertNotIn("standing approval record, one run ID", text)
        self.assertNotIn("BLK-SYSTEM-316..325", text)
        self.assertNotIn("Capture BLK-SYSTEM-316 and execute", text)
        self.assertIn("NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CAPTURE_AND_BOUNDED_EXECUTION_REQUIRED_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUIRED_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_REUSABLE_BLK003_LOOP_REQUEST_PATH_WITH_QUARANTINE_GATE_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_HITL_GATEWAY_IDENTITY_RELAY_WIRING_NOT_GRANTED", text)
        self.assertIn("NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED", text)
        self.assertIn("sha256:8a15f70354f5fade521197c6e954af6caa4ccb2f4bb76ec15a61121a11ed6ef6", text)
        self.assertIn("2026-05-20T17:39:00+10:00", text)
        self.assertIn("2026-05-20T18:39:00+10:00", text)
        self.assertIn("NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_AFTER_EXACT_BEO_PUBLICATION", text)
        self.assertLessEqual(len(text.splitlines()), 185)
        self.assertIn("Root-Doctrine Gap Coverage and Proposed Sequence", text)
        self.assertIn("Convenience/product lane", text)
        self.assertIn("Immediate real dependency", text)
        self.assertNotIn("High-Level Roadmap to Complete BLK-System", text)

    def test_runtime_and_adjacent_authorities_are_all_denied(self):
        record = build_current_state_authority_index()

        self.assertEqual(tuple(DENIED_FLAGS), INDEX_DENIED_FLAGS)
        self.assertEqual(set(DOC_DENIAL_MARKERS), set(INDEX_DENIED_FLAGS))
        for flag in DENIED_FLAGS:
            self.assertIs(record[flag], False, flag)

        by_surface = {surface["surface"]: surface for surface in record["surfaces"]}
        self.assertIn("BLK_SYSTEM_229_PRIVATE_BWRAP_WORKSPACE_WRITE_SETUP_READY", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertIn("kernel.apparmor_restrict_unprivileged_userns=1", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertIn("blk-codex-bwrap", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertIn("No reusable Codex dispatch", by_surface["Codex live-dispatch ladder"]["authority_cutline"])
        self.assertEqual(by_surface["BLK-test"]["state"], "exact_blk_test_oracle_verification_301_reconciled")
        self.assertEqual(by_surface["BLK-test"]["maturity"], "L3_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED_VERIFIER_ONLY_NO_TRANSPORT")
        self.assertIn("BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("BLK_SYSTEM_298_EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("verifier-only", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("transport remains disabled", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("no protected-body", by_surface["RTM / blk-link"]["authority_cutline"])
        self.assertIn("no target/source/Git mutation", by_surface["RTM / blk-link"]["authority_cutline"])
        self.assertIn("no broad active-vault body scan", by_surface["BLK-req legislative gateway"]["authority_cutline"])

    def test_active_docs_cover_every_executable_denied_surface(self):
        roadmap = BLK077.read_text()
        index = BLK079.read_text()
        errors = validate_active_current_state_docs(roadmap, index)

        self.assertEqual(errors, [])
        combined = f"{roadmap}\n{index}"
        for flag, markers in DOC_DENIAL_MARKERS.items():
            with self.subTest(flag=flag):
                self.assertTrue(markers, flag)
                self.assertTrue(any(marker in combined for marker in markers), (flag, markers))

        tampered_roadmap = roadmap.replace("no BEB dispatch", "BEB dispatch omitted")
        tampered_index = index.replace("no BEB dispatch", "BEB dispatch omitted")
        tampered_errors = validate_active_current_state_docs(tampered_roadmap, tampered_index)
        self.assertTrue(any("beb_dispatch_authorized" in error for error in tampered_errors), tampered_errors)

        dangerous_doc = (
            roadmap
            + "\nproduction BLK-test MCP transport enabled; RTM generation enabled; "
            + "production blk-link enabled; protected-body access enabled"
        )
        dangerous_errors = validate_active_current_state_docs(dangerous_doc, index)
        self.assertTrue(any("forbidden authority wording" in error for error in dangerous_errors), dangerous_errors)

    def test_post103_generic_current_state_surfaces_do_not_use_pre100_stale_states(self):
        record = build_current_state_authority_index()
        states = {surface["surface"]: surface["state"] for surface in record["surfaces"]}

        self.assertNotIn("draft_and_fixture_only", states.values())
        self.assertNotIn("offline_fixture_only", states.values())
        self.assertEqual(states["BEO publication path"], "development_authority_distinguished_328_internal_gates_not_approval_blockers")
        self.assertEqual(states["RTM / blk-link"], "rtm_blk_link_drift_coverage_281_second_refresh_challenge_reconciled_approval_required")
        self.assertEqual(states["BLK-req legislative gateway"], "hitl_gateway_speculative_quarantine_gate_289_ready")
        self.assertEqual(states["BLK-pipe blast shield"], "blk_pipe_bounded_enforcement_206_closed")
        self.assertEqual(states["Python adapter layer"], "exact_quarantine_gated_blk003_loop_execution_297_reconciled")
        self.assertEqual(states["Validation profiles"], "beb_l2_route_artifact_boundary_323_hardened")
        self.assertEqual(states["BLK-test"], "exact_blk_test_oracle_verification_301_reconciled")
        self.assertEqual(states["Codex live-dispatch ladder"], "codex_private_bwrap_setup_229_descriptor_verified")

        for stale_state in ("draft_and_fixture_only", "offline_fixture_only"):
            stale_record = build_current_state_authority_index()
            stale_record["surfaces"][0]["state"] = stale_state
            errors = validate_current_state_authority_index(stale_record)
            self.assertTrue(any("unsupported state" in error for error in errors), (stale_state, errors))

    def test_unsupported_state_and_maturity_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["state"] = "LIVE_EXECUTION_ENABLED"
        record["surfaces"][1]["maturity"] = "L5_PRODUCTION_AUTHORITY"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("unsupported state" in error for error in errors))
        self.assertTrue(any("unsupported maturity" in error for error in errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_authority_laundering_keys_and_values_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "APPROVED_FOR_LIVE_EXECUTION": False,
            "notes": ["authoritative BEO publication approved"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("forbidden authority wording" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_recursive_denied_flags_and_generic_authority_claims_fail_closed(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["nested"] = {
            "live_codex_execution_authorized": True,
            "execution_authorized": True,
            "authority": "approved for runtime execution",
            "notes": ["runtime_authority_granted"],
        }

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("live_codex_execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("execution_authorized" in error for error in errors), errors)
        self.assertTrue(any("approved for runtime execution" in error for error in errors), errors)
        self.assertTrue(any("runtime_authority_granted" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_extra_authority_claim_fields_fail_closed(self):
        record = build_current_state_authority_index()
        record["approved_for_runtime_execution"] = True
        record["surfaces"][0]["approved"] = True
        record["surfaces"][0]["authorized"] = True
        record["surfaces"][0]["approval_status"] = "approved"
        record["surfaces"][0]["note"] = "live execution authorized"
        record["surfaces"][1]["authority_cutline"] = "runtime execution authorized"

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        for marker in [
            "approved_for_runtime_execution",
            "approved",
            "authorized",
            "approval_status",
            "note",
            "runtime execution authorized",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_natural_language_authority_claims_and_governing_doc_laundering_fail_closed(self):
        phrases = [
            "Live Codex execution is authorized",
            "runtime-execution-authorized",
            "Production BLK-test MCP is authorized",
            "RTM drift rejection is authorized",
            "Production sandbox is enforced",
            "BEO publication authorized",
            "Publication authority granted",
            "approved for publication",
            "greenlit for production",
            "exact-ID retrieval authorized.",
            "stagedRevisionOverwriteIsAuthorized",
            "publicAuthorityLedgerRollbackIsAuthorized",
            "BEO%20publication%20authorized",
            "publish%2542EO",
            "RTMGenerationAuthorized",
            "driftRejectionExecuted",
            "productionBlkLinkEnabled",
            "docs%2525252Frequirements%2525252Factive%2525252FREQ-001.md",
        ]
        for phrase in phrases:
            record = build_current_state_authority_index()
            record["surfaces"][0]["authority_cutline"] = phrase
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, phrase)

        for bad_doc in [{"is_authorized": True}, "approved", "runtime authority granted"]:
            record = build_current_state_authority_index()
            record["surfaces"][0]["governing_docs"].append(bad_doc)
            errors = validate_current_state_authority_index(record)
            self.assertTrue(errors, bad_doc)

    def test_validation_errors_and_active_docs_are_scanned_for_authority_laundering(self):
        record = build_current_state_authority_index()
        record["validation_errors"] = ["runtime execution authorized; approved for publication"]

        errors = validate_current_state_authority_index(record)
        evaluated = evaluate_current_state_authority_index(record)

        self.assertTrue(any("runtime execution authorized" in error for error in errors), errors)
        self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

        roadmap = BLK077.read_text()
        index = BLK079.read_text()
        tampered = roadmap + "\nruntime execution authorized; approved for publication"
        doc_errors = validate_active_current_state_docs(tampered, index)
        self.assertTrue(any("runtime execution authorized" in error or "approved for publication" in error for error in doc_errors), doc_errors)

    def test_default_denial_phrases_do_not_false_positive(self):
        record = build_current_state_authority_index()
        record["surfaces"][0]["authority_cutline"] = (
            "does not capture RTM drift-rejection approval; "
            "does not execute RTM drift rejection; "
            "no protected-body reads or hashing; "
            "no source mutation authorized; "
            "no runtime blk-link trace closure occurred"
        )
        errors = validate_current_state_authority_index(record)
        self.assertFalse(any("rtmdriftrejectionapproval" in error for error in errors), errors)
        self.assertFalse(any("source mutation authorized" in error for error in errors), errors)
        self.assertFalse(any("runtime blk-link trace closure occurred" in error for error in errors), errors)

    def test_default_record_contains_evaluation_and_evaluated_records_validate(self):
        record = build_current_state_authority_index()
        self.assertEqual(record["evaluation"], "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY")
        self.assertEqual(record["validation_errors"], [])

        evaluated = evaluate_current_state_authority_index(record)

        self.assertEqual(validate_current_state_authority_index(evaluated), [])

    def test_positive_authority_flags_fail_closed(self):
        for flag in DENIED_FLAGS:
            record = build_current_state_authority_index()
            record[flag] = True

            errors = validate_current_state_authority_index(record)
            evaluated = evaluate_current_state_authority_index(record)

            self.assertTrue(any(flag in error for error in errors), flag)
            self.assertIs(evaluated[flag], False, flag)
            self.assertEqual(evaluated["evaluation"], "CURRENT_STATE_INDEX_BLOCKED")

    def test_module_contains_no_live_surface_imports_or_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "git"}
        forbidden_calls = {"eval", "exec", "__import__", "compile", "open"}
        offenders = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                if node.module:
                    names.append(node.module.split(".")[0])
                offenders.extend(name for name in names if name in forbidden_imports)
            if isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    offenders.append(name)

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
