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
    "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED",
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
    "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
    "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9",
    "blk204_surface_review_package_hash=sha256:324a218f4a6681883e6cb82d097239730386b3e290f9ed112c651eb2a7cde8d9",
    "blk205_enforcement_contract_hash=sha256:108d03e3e3f4cbb57a8fbd58691bb3e24d4cda7aad957e8ac5842d0ae52ba9d4",
    "blk206_reconciliation_package_hash=sha256:666db65980b1767f84e919491dcc54096b260d4cc91972f7b9f67281a9706fba",
    "blk207_adapter_review_package_hash=sha256:5fd1aa5428a13349a62da76bf66e5ddaeef510ab7582a12ff1f1a45cad6a2298",
    "blk208_adapter_contract_package_hash=sha256:d98159f614cb2e9c248df151efec7489eab306eeceb2d9d4a7f94b21acabdb9c",
    "blk209_adapter_reconciliation_package_hash=sha256:02a9084ec1aab3e589da5c8a7417e371d78e3e1e706b27f51fde9ab1b5b79a61",
    "blk210_profile_review_package_hash=sha256:0c754f86a9335c11610b74bb0d6f6808f9c0d9ce7afa2ab36eab7d591ffdfe32",
    "blk211_profile_contract_package_hash=sha256:b1aed5f05923afee76206c0f1b406034cb5da0b9c743686e0faa493806a6baa7",
    "blk212_profile_reconciliation_package_hash=sha256:77fa8dcc7d28b1084443169d43bff3f87e2fee85d082d0c8281e9e5807a4f905",
    "blk213_blk_test_unblock_package_hash=sha256:0cae4030ca2ff06792f80762259fcd3ab00731bf00f4ee4f4ba158f4654a0381",
    "blk214_feature_loop_package_hash=sha256:87f15b82ec5f78450e49638544d406845180ca1bdd7915be7323ae98677172e8",
    "blk215_supervised_codex_feature_loop_package_hash=sha256:4e2d6bd3c7d7d452452fa5a018a8e649e7cf614a9d33158b2232ee40c68f83a4",
    "blk216_codex_config_containment_package_hash=sha256:3e1cf8a9dcbb6dc8826d203d65b26ed01649ad1de0b6a3eda7e8d7741ec7434e",
    "blk217_codex_exact_undo_package_hash=sha256:b730e69e4126377c4f726e3bfd9648e3c6478ac6bd21aa9ddc26d221ffa7c506",
    "blk218_selected_requirement_badge_feature_hash=sha256:b5310ed5bd41c6717c733f8cfbb98de7fd03b0f37d602990e6a100b9a255f1d3",
    "blk219_native_codex_sandbox_mitigation_hash=sha256:710dd82eabda1f2d792dfc8cce2af88612603ea0b1683e5ad644bc1453312404",
    "blk220_native_codex_sandbox_repair_recheck_hash=sha256:9d63c4b7d99615db812e3751718574ce96cf101fc755af6d50ccc50d7f10146e",
    "blk221_loading_state_feature_hash=sha256:232a1f494d4edea48438273382091f3ecc61e600545026bd29f63b22f20dc8f3",
    "blk222_beb_l2_blk_pipe_codex_route_hash=sha256:52b85fd75fb2542ed9aa05ec790986bbf40e21ea178d5c6c6f07a245e10b55fa",
    "blk223_beb_l2_preflight_guard_hash=sha256:c1ee4c9bdcf76c0e315095f4f858f3e33b5d6eaee55cf3f8651d1dc3768edf84",
    "blk224_ignored_residue_cleanup_plan_hash=sha256:e2e826e979ac42106eb1c05d885bd12e471e3cc6a9042f177cc4a404c5eb90d9",
    "blk225_clean_worktree_manifest_hash=sha256:f13e65c959415edb4b44f52577ae0f94862f04bdec54347addad49c40f3e9a43",
    "blk226_kuronode_worktree_static_profile_hash=sha256:e287c7e84668b9e7a1667671c5561ee7da39bc4c614694182677b98b770805fc",
    "blk227_external_codex_artifact_hash=sha256:848df7dd040d145e955517616225c60fc24ddbea60ea982fa0599ecd2aba094c",
    "blk228_clean_worktree_feature_drop_hash=sha256:93541bf31fd0a227d94b8a34c9bccb8a95cf406a12ae98cbd8b3fb7a7038ef12",
    "blk229_private_bwrap_workspace_write_setup_hash=sha256:1cadd6e9f379bb814f86a50e22cd1e351b8961bbfb7e3c6778ca771075d5722f",
    "blk230_agent_a_header_feature_drop_hash=sha256:82c8cbfa501a1f113a5262e71f6b210c42b017884e4754b073b02f55af4ba6d1",
    "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED",
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
        self.assertLessEqual(len(names), 9, "current-state index must not become a historical sprint catalog")

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
        self.assertEqual(rtm_link["state"], "rtm_blk_link_drift_coverage_256_reconciled_beo_publication_required")
        self.assertEqual(rtm_link["maturity"], "L2_RTM_BLK_LINK_DRIFT_COVERAGE_VERIFIER_READY_BEO_PUBLICATION_REQUIRED")
        self.assertIn("BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_255_EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_RECORDED", rtm_link["authority_cutline"])
        self.assertIn("BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN", rtm_link["authority_cutline"])
        self.assertIn("blocked until exact BEO publication metadata exists", rtm_link["authority_cutline"])
        self.assertIn("No blanket production `blk-link`", rtm_link["authority_cutline"])
        self.assertIn("no reusable RTM generation", rtm_link["authority_cutline"])

        blk_pipe = by_surface["BLK-pipe blast shield"]
        self.assertEqual(blk_pipe["state"], "blk_pipe_bounded_enforcement_206_closed")
        self.assertEqual(blk_pipe["maturity"], "L2_BLK_PIPE_BOUNDED_NON_AUTHORIZING_ENFORCEMENT_SURFACE_CLOSED")
        self.assertIn("bounded non-authorizing enforcement surface", blk_pipe["authority_cutline"])
        self.assertIn("No broad dispatch", blk_pipe["authority_cutline"])
        self.assertIn("no production-isolation claim", blk_pipe["authority_cutline"])

        python_adapter = by_surface["Python adapter layer"]
        self.assertEqual(python_adapter["state"], "reusable_blk003_loop_kernel_241_ready")
        self.assertEqual(python_adapter["maturity"], "L2_REUSABLE_BLK003_LOOP_KERNEL_READY_NO_RUNTIME")
        self.assertIn("BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_235_AGENT_A_CONTEXT_PACKET_PR_MERGED", python_adapter["authority_cutline"])
        self.assertIn("BLK_SYSTEM_234_REPEAT_KURONODE_FEATURE_DROP_EXECUTED", python_adapter["authority_cutline"])
        self.assertIn("failure ceiling", python_adapter["authority_cutline"])
        self.assertIn("BEO draft", python_adapter["authority_cutline"])
        self.assertIn("workspace-write", python_adapter["authority_cutline"])
        self.assertIn("broad dispatch", python_adapter["authority_cutline"])
        self.assertIn("production-isolation authority", python_adapter["authority_cutline"])

        validation_profiles = by_surface["Validation profiles"]
        self.assertEqual(validation_profiles["state"], "kuronode_worktree_static_profile_226_ready")
        self.assertEqual(validation_profiles["maturity"], "L2_KURONODE_WORKTREE_STATIC_PROFILE_READY_NO_DISPATCH")
        self.assertIn("BLK_SYSTEM_226_KURONODE_WORKTREE_STATIC_PROFILE_READY", validation_profiles["authority_cutline"])
        self.assertIn("BLK_SYSTEM_212_VALIDATION_PROFILE_RECONCILED_CLEAN", validation_profiles["authority_cutline"])
        self.assertIn("git diff --check -- .", validation_profiles["authority_cutline"])
        self.assertIn("local whitespace/static evidence only", validation_profiles["authority_cutline"])
        self.assertIn("no package manager", validation_profiles["authority_cutline"])
        self.assertIn("no runtime", validation_profiles["authority_cutline"])

        blk_req = by_surface["BLK-req legislative gateway"]
        self.assertEqual(blk_req["state"], "hitl_gateway_completion_slice_240_ready")
        self.assertEqual(blk_req["maturity"], "L2_HITL_GATEWAY_COMPLETION_SLICE_READY_EXACT_OPERATION_ONLY")
        self.assertIn("BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY", blk_req["authority_cutline"])
        self.assertIn("BLK_SYSTEM_239_BLK_ID_RELAY_SCOPE_DECIDED", blk_req["authority_cutline"])
        self.assertIn("metadata-only exact ID mapping", blk_req["authority_cutline"])
        self.assertIn("no broad active-vault body scan", blk_req["authority_cutline"])
        self.assertIn("No Kuronode source/Git mutation", blk_req["authority_cutline"])

        beo_path = by_surface["BEO publication path"]
        self.assertEqual(beo_path["state"], "reusable_beo_publication_251_per_run_exact_approval_ready")
        self.assertEqual(beo_path["maturity"], "L2_REUSABLE_BEO_PUBLICATION_REVIEW_KERNEL_READY_PER_RUN_EXACT_APPROVAL")
        self.assertIn("BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY", beo_path["authority_cutline"])
        self.assertIn("per-run exact approval", beo_path["authority_cutline"])
        self.assertIn("no blanket publication authority", beo_path["authority_cutline"])
        self.assertIn("no signer/storage/ledger reuse", beo_path["authority_cutline"])

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
        self.assertIn("NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED", text)
        self.assertLessEqual(len(text.splitlines()), 185)
        self.assertIn("Root-Doctrine Gap Coverage and Proposed Sequence", text)
        self.assertIn("Convenience/product lane, not a dependency", text)
        self.assertIn("Real dependency for reusable HITL/runtime authority", text)
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
        self.assertEqual(by_surface["BLK-test"]["state"], "production_blk_test_mcp_oracle_246_reconciled_verifier_only")
        self.assertEqual(by_surface["BLK-test"]["maturity"], "L2_BLK_TEST_MCP_ORACLE_VERIFIER_ONLY_READY_NO_LIVE_MCP")
        self.assertIn("BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY", by_surface["BLK-test"]["authority_cutline"])
        self.assertIn("BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED", by_surface["BLK-test"]["authority_cutline"])
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
        self.assertEqual(states["BEO publication path"], "reusable_beo_publication_251_per_run_exact_approval_ready")
        self.assertEqual(states["RTM / blk-link"], "rtm_blk_link_drift_coverage_256_reconciled_beo_publication_required")
        self.assertEqual(states["BLK-req legislative gateway"], "hitl_gateway_completion_slice_240_ready")
        self.assertEqual(states["BLK-pipe blast shield"], "blk_pipe_bounded_enforcement_206_closed")
        self.assertEqual(states["Python adapter layer"], "reusable_blk003_loop_kernel_241_ready")
        self.assertEqual(states["Validation profiles"], "kuronode_worktree_static_profile_226_ready")
        self.assertEqual(states["BLK-test"], "production_blk_test_mcp_oracle_246_reconciled_verifier_only")
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
