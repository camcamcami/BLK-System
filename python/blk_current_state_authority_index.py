from copy import deepcopy

from blk_authority_smuggling import scan_for_authority_laundering

INDEX_ID = "blk_system_current_state_authority_index"
INDEX_STATUS = "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX"
READY = "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY"
BLOCKED = "CURRENT_STATE_INDEX_BLOCKED"
MATURITY = "CURRENT_STATE_INDEX_L0_L1_ONLY"

DENIED_FLAGS = (
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
)

DOC_DENIAL_MARKERS = {
    "runtime_authority_granted": ("no runtime tooling", "no BLK-pipe runtime"),
    "live_codex_execution_authorized": ("no live Codex",),
    "blk_pipe_dispatch_authorized": ("no BLK-pipe runtime",),
    "production_blk_test_mcp_authorized": ("no production BLK-test MCP", "production/generic BLK-test MCP"),
    "beb_dispatch_authorized": ("no BEB dispatch",),
    "beo_closeout_execution_authorized": ("no BEO closeout execution",),
    "authoritative_beo_publication_authorized": ("no reusable BEO publication", "no future publication run"),
    "reusable_beo_publication_authorized": ("no reusable BEO publication",),
    "beo_publication_signer_reuse_authorized": ("no signer reuse", "no reusable BEO publication/signing"),
    "beo_publication_storage_reuse_authorized": ("no storage reuse", "no reusable BEO publication/signing/storage"),
    "beo_publication_ledger_reuse_authorized": ("no ledger reuse", "no reusable BEO publication/signing/storage/ledger"),
    "rollback_revocation_supersession_authorized": ("no rollback/revocation/supersession", "rollback, revocation, or supersession execution"),
    "runtime_rtm_generation_authorized": ("no reusable RTM generation", "further RTM generation"),
    "reusable_rtm_generation_authorized": ("no reusable RTM generation",),
    "production_blk_link_authorized": ("no production `blk-link`",),
    "rtm_drift_rejection_authorized": ("no drift rejection",),
    "rtm_coverage_truth_authorized": ("no coverage truth",),
    "active_vault_comparison_authorized": ("no active-vault comparison", "no new active-vault comparison"),
    "protected_blk_req_body_reads_authorized": ("no protected-body access", "no protected BLK-req body reads"),
    "protected_blk_req_body_copy_authorized": ("copying", "reads/copying/parsing"),
    "protected_blk_req_body_parse_authorized": ("parsing", "reads/copying/parsing"),
    "protected_blk_req_body_hash_authorized": ("hashing", "parsing/hashing/scanning"),
    "protected_blk_req_body_scan_authorized": ("scanning", "hashing/scanning/mutation"),
    "target_source_git_mutation_authorized": ("no target/source/Git mutation", "no source/Git mutation"),
    "network_model_cyber_browser_tooling_authorized": ("no package/network/model/browser/cyber tooling",),
    "package_manager_authorized": ("no package/network/model/browser/cyber tooling", "package-manager"),
    "production_isolation_claimed": ("no production-isolation claim", "production-isolation claims"),
}

ACTIVE_DOC_REQUIRED_MARKERS = (
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
    "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_NATIVE_WORKSPACE_WRITE_RECHECK_OR_EXTERNAL_CONTAINMENT_NOT_GRANTED",
)

STALE_ACTIVE_DOC_MARKERS = (
    "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_EXTERNAL_CONTAINMENT_OR_HOST_ADMIN_SANDBOX_REPAIR_NOT_GRANTED",
    "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_OR_OBSERVED_FAILURE_HARDENING_NOT_GRANTED",
    "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_AVAILABLE_AFTER_UNDO_CHECK_NOT_GRANTED",
    "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_EXACT_UNDO_WITH_CODEX_PROFILE_CONTAINMENT_AVAILABLE_NOT_GRANTED",
    "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED",
    "NEXT_FRONTIER_SECOND_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED",
    "NEXT_FRONTIER_VALIDATION_PROFILES_CLOSED_BLK_TEST_SELECTION_NOT_GRANTED",
    "NEXT_FRONTIER_PYTHON_ADAPTER_CLOSED_VALIDATION_PROFILES_SELECTION_NOT_GRANTED",
    "NEXT_FRONTIER_BLK_PIPE_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED",
    "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_CAPABILITY_AFTER_CLEAN_RECONCILIATION_NOT_GRANTED",
    "NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_NOT_GRANTED",
    "NEXT_FRONTIER_HARDENING_ONLY_COMPLETE_AUTHORITY_NOT_GRANTED",
    "NEXT_FRONTIER_FURTHER_HARDENING_OR_AUTHORITY_REQUEST_NOT_GRANTED",
    "NEXT_FRONTIER_METADATA_BOUND_DRIFT_COVERAGE_DECISION_APPROVAL_NOT_GRANTED",
    "NEXT_FRONTIER_PROTECTED_BODY_VERIFICATION_DECISION_APPROVAL_NOT_GRANTED",
    "NEXT_FRONTIER_RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_READY_NOT_REUSABLE_AUTHORITY",
    "NEXT_FRONTIER_DOWNSTREAM_METADATA_EXPORT_REQUEST_NOT_GRANTED",
    "NEXT_FRONTIER_OPERATOR_SELECTED_RTM_BLK_LINK_DECISION_AFTER_METADATA_EXPORT_NOT_GRANTED",
    "NEXT_FRONTIER_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_REQUEST_NOT_GRANTED",
    "NEXT_FRONTIER_POST_SINGLE_PRODUCTION_WRAPPER_RUN_OPERATOR_REVIEW_NOT_GRANTED",
    "NEXT_FRONTIER_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL_NOT_BLANKET_AUTHORITY",
    "NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT",
    "NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED",
    "NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED",
)

EXPECTED_SURFACES = (
    "BLK-req legislative gateway",
    "BLK-pipe blast shield",
    "Python adapter layer",
    "Validation profiles",
    "BLK-test",
    "Operator health / observability",
    "Codex live-dispatch ladder",
    "BEO publication path",
    "RTM / blk-link",
)

ALLOWED_STATES = {
    "blk_req_metadata_bound_publication_request_127_complete",
    "blk_req_production_gateway_199_clean",
    "kuronode_blk_req_vault_bootstrap_200_ready",
    "kuronode_blk_req_bridge_203_clean",
    "local_guarded_enforcement",
    "blk_pipe_bounded_enforcement_206_closed",
    "python_adapter_closed_209_clean",
    "fail_fast_convenience_layer",
    "repository_owned_local_profiles",
    "validation_profiles_closed_212_clean",
    "disabled_gated_evidence_only",
    "blk_test_optional_diagnostic_unblocked_213",
    "advisory_local_pilot",
    "review_ready_not_reusable_execution_authorized",
    "codex_config_containment_drill_216_recorded",
    "codex_bounded_feature_loop_218_recorded",
    "codex_native_sandbox_mitigation_219_recorded",
    "codex_native_sandbox_repair_recheck_220_recorded",
    "authoritative_beo_publication_finality_152_complete",
    "rtm_blk_link_protected_body_verification_evidence_integrated_177_hardened",
    "rtm_blk_link_protected_body_evidence_export_reconciled_182_clean",
    "reusable_blk_link_readiness_kernel_186_clean",
    "single_production_blk_link_wrapper_run_189_clean",
    "repeatable_trusted_blk_link_194_clean",
}

ALLOWED_MATURITIES = {
    "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
    "L2_BLK_REQ_PRODUCTION_GATEWAY_READY_EXACT_OPERATION_ONLY",
    "L2_KURONODE_BLK_REQ_SIBLING_VAULT_BLUEPRINT_READY_NOT_SOURCE_MUTATION",
    "L2_KURONODE_BLK_REQ_METADATA_ID_BRIDGE_CLOSED_NOT_SOURCE_MUTATION",
    "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
    "L2_BLK_PIPE_BOUNDED_NON_AUTHORIZING_ENFORCEMENT_SURFACE_CLOSED",
    "L2_PYTHON_ADAPTER_BOUNDED_PACKAGING_SURFACE_CLOSED",
    "L1_L2_STYLE_PREFLIGHT_ONLY",
    "MATURE_LOCAL_PROFILE_SUPPORT",
    "L2_VALIDATION_PROFILES_BOUNDED_LOCAL_EVIDENCE_CLOSED",
    "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
    "L2_BLK_TEST_OPTIONAL_DIAGNOSTIC_NOT_BLOCKING_FEATURE_LOOPS",
    "ADVISORY_PILOT_ONLY",
    "L0_L1_L2_STYLE_DISABLED_NO_REUSABLE_CODEX_DISPATCH",
    "L2_CODEX_PERMISSION_PROFILE_CONTAINMENT_CONTRACT_RECORDED_NOT_RUNTIME_AUTHORITY",
    "L2_CODEX_BOUNDED_FEATURE_LOOP_RECORDED_NOT_RUNTIME_AUTHORITY",
    "L2_CODEX_NATIVE_SANDBOX_MITIGATION_RECORDED_NOT_RUNTIME_AUTHORITY",
    "L2_CODEX_NATIVE_SANDBOX_REPAIR_RECHECK_RECORDED_NOT_REUSABLE_AUTHORITY",
    "L3_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_COMPLETE",
    "L2_PROTECTED_BODY_HASH_VERIFICATION_EVIDENCE_INTEGRATED_HARDENED_NOT_REUSABLE_AUTHORITY",
    "L2_PROTECTED_BODY_EVIDENCE_METADATA_EXPORT_RECONCILED_NOT_REUSABLE_AUTHORITY",
    "L2_REUSABLE_BLK_LINK_READINESS_KERNEL_READY_PER_RUN_EXACT_APPROVAL_REQUIRED",
    "L2_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_EXECUTED_EXACT_ONCE_NO_REUSE",
    "L2_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL",
}

TOP_LEVEL_KEYS = {
    "index_id",
    "index_status",
    "roadmap_source",
    "maturity",
    "surfaces",
    "evaluation",
    "validation_errors",
    *DENIED_FLAGS,
}

SURFACE_KEYS = {
    "surface",
    "state",
    "maturity",
    "governing_docs",
    "authority_cutline",
}

DEFAULT_SURFACES = (
    {
        "surface": "BLK-req legislative gateway",
        "state": "kuronode_blk_req_bridge_203_clean",
        "maturity": "L2_KURONODE_BLK_REQ_METADATA_ID_BRIDGE_CLOSED_NOT_SOURCE_MUTATION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-116", "BLK-120"],
        "authority_cutline": (
            "BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN after BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED, "
            "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY, and BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY. "
            "Sibling vault /home/dad/BLK-req-Kuronode contains metadata-only exact ID mapping; exact-operation lifecycle remains ready through BLK-199. "
            "No Kuronode source/Git mutation, no broad Kuronode doc scan, no protected-body migration, no broad active-vault body scan, no body access without exact ID, no BEO/RTM/runtime/tooling/mutation authority."
        ),
    },
    {
        "surface": "BLK-pipe blast shield",
        "state": "blk_pipe_bounded_enforcement_206_closed",
        "maturity": "L2_BLK_PIPE_BOUNDED_NON_AUTHORIZING_ENFORCEMENT_SURFACE_CLOSED",
        "governing_docs": ["BLK-003", "BLK-004", "BLK-077", "BLK-079", "BLK-112", "BLK-113", "BLK-114", "BLK-115"],
        "authority_cutline": (
            "BLK_SYSTEM_206_BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN after "
            "BLK_SYSTEM_205_BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY and "
            "BLK_SYSTEM_204_BLK_PIPE_SURFACE_REVIEW_READY. BLK-pipe is a bounded non-authorizing enforcement surface for "
            "structured validation-profile argv, failure/denial/cleanup evidence, and exact allowlists. No broad dispatch, no target/source/Git mutation, no runtime tooling, and no production-isolation claim."
        ),
    },
    {
        "surface": "Python adapter layer",
        "state": "python_adapter_closed_209_clean",
        "maturity": "L2_PYTHON_ADAPTER_BOUNDED_PACKAGING_SURFACE_CLOSED",
        "governing_docs": ["BLK-016", "BLK-021", "BLK-077", "BLK-079"],
        "authority_cutline": (
            "BLK_SYSTEM_209_PYTHON_ADAPTER_RECONCILED_CLEAN after BLK_SYSTEM_208_PYTHON_ADAPTER_CONTRACT_READY "
            "and BLK_SYSTEM_207_PYTHON_ADAPTER_SURFACE_REVIEW_READY. Deterministic local packaging/report normalization only; "
            "no BLK-pipe dispatch, live Codex, source/Git mutation, RTM/BEO, protected-body, runtime/tooling, or production-isolation authority."
        ),
    },
    {
        "surface": "Validation profiles",
        "state": "validation_profiles_closed_212_clean",
        "maturity": "L2_VALIDATION_PROFILES_BOUNDED_LOCAL_EVIDENCE_CLOSED",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-112", "BLK-113", "BLK-114", "BLK-115"],
        "authority_cutline": (
            "BLK_SYSTEM_212_VALIDATION_PROFILE_RECONCILED_CLEAN after BLK_SYSTEM_211_VALIDATION_PROFILE_CONTRACT_READY "
            "and BLK_SYSTEM_210_VALIDATION_PROFILE_SURFACE_REVIEW_READY. Structured argv/capability labels/PASS are local diagnostic evidence only; "
            "no runtime, mutation, publication, RTM, tooling, production-isolation, BLK-pipe dispatch, or BLK-test MCP authority."
        ),
    },
    {
        "surface": "BLK-test",
        "state": "blk_test_optional_diagnostic_unblocked_213",
        "maturity": "L2_BLK_TEST_OPTIONAL_DIAGNOSTIC_NOT_BLOCKING_FEATURE_LOOPS",
        "governing_docs": ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-077", "BLK-079"],
        "authority_cutline": "BLK_SYSTEM_213_BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY. BLK-test is a BLK-System functional module, not the BLK-System test suite. Production MCP remains disabled; BLK-test evidence is optional diagnostic evidence and does not block bounded Kuronode feature loops or grant source mutation, BEO/RTM, drift/coverage, tooling, or protected-body authority.",
    },
    {
        "surface": "Operator health / observability",
        "state": "advisory_local_pilot",
        "maturity": "ADVISORY_PILOT_ONLY",
        "governing_docs": ["BLK-031", "BLK-077", "BLK-079"],
        "authority_cutline": "Health and observability outputs are advisory. A PASS is not execution approval, publication authority, RTM truth, coverage truth, sandbox evidence, or protected-body access authority.",
    },
    {
        "surface": "Codex live-dispatch ladder",
        "state": "codex_native_sandbox_repair_recheck_220_recorded",
        "maturity": "L2_CODEX_NATIVE_SANDBOX_REPAIR_RECHECK_RECORDED_NOT_REUSABLE_AUTHORITY",
        "governing_docs": ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044", "BLK-077", "BLK-079", "BLK-121", "BLK-SYSTEM-216", "BLK-SYSTEM-217", "BLK-SYSTEM-218", "BLK-SYSTEM-219", "BLK-SYSTEM-220"],
        "authority_cutline": (
            "BLK-SYSTEM-220 records workspace-write smoke passed only under runtime host-admin AppArmor userns relaxation after uidmap install; "
            "restored default blocks it again, so native workspace-write is recheck-required before use and external containment remains fallback. "
            "No one-off or reusable BLK-System live Codex subprocess/dispatch, no reusable Codex dispatch, persistent host policy, BLK-pipe dispatch, "
            "broad source mutation, package/network/model/browser/cyber tooling, or production-isolation claim."
        ),
    },
    {
        "surface": "BEO publication path",
        "state": "authoritative_beo_publication_finality_152_complete",
        "maturity": "L3_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_COMPLETE",
        "governing_docs": ["BLK-022", "BLK-077", "BLK-079", "BLK-127", "BLK-128", "BLK-129"],
        "authority_cutline": "BLK-SYSTEM-152 completed exact metadata-bound BEO publication finality with canonical signer, immutable-storage, and public-ledger receipts. This is one consumed finality package only: no reusable publication authority, rollback/revocation/supersession, BEO closeout execution, RTM generation, drift rejection, coverage truth, protected-body access, runtime tooling, or target/source/Git mutation is granted."
    },
    {
        "surface": "RTM / blk-link",
        "state": "repeatable_trusted_blk_link_194_clean",
        "maturity": "L2_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL",
        "governing_docs": ["BLK-023", "BLK-077", "BLK-079", "BLK-140", "BLK-141", "BLK-142", "BLK-143", "BLK-144"],
        "authority_cutline": (
            "BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN after "
            "BLK_SYSTEM_193_REPEATABLE_TRUSTED_BLK_LINK_REPEAT_RUNS_RECORDED_CLEAN, "
            "BLK_SYSTEM_192_REPEATABLE_TRUSTED_BLK_LINK_LEDGER_READY, "
            "BLK_SYSTEM_191_REPEATABLE_TRUSTED_BLK_LINK_CONTRACT_EMITTED, "
            "BLK_SYSTEM_190_REPEATABLE_TRUSTED_BLK_LINK_POST_RUN_REVIEW_CLEAN, and "
            "BLK_SYSTEM_189_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECONCILED_CLEAN. "
            "A repeatable trusted per-run exact-approval mechanism is boxed; No blanket production `blk-link`, no production `blk-link` without per-run exact approval, "
            "no reusable RTM generation, no drift rejection, no coverage truth, no protected-body text return, no target/source/Git mutation."
        ),
    },
)


def build_current_state_authority_index(surfaces=None):
    record = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-077",
        "maturity": MATURITY,
        "surfaces": deepcopy(list(DEFAULT_SURFACES if surfaces is None else surfaces)),
        "evaluation": READY,
        "validation_errors": [],
    }
    for flag in DENIED_FLAGS:
        record[flag] = False
    return record


def validate_current_state_authority_index(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    unknown_top_keys = sorted(set(record) - TOP_LEVEL_KEYS)
    for key in unknown_top_keys:
        errors.append(f"unsupported top-level key {key!r}")

    expected_scalars = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-077",
        "maturity": MATURITY,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

    if record.get("evaluation") not in {READY, BLOCKED, None}:
        errors.append("evaluation must be a current-state index status")
    if "validation_errors" in record and not isinstance(record.get("validation_errors"), list):
        errors.append("validation_errors must be a list")

    for flag in DENIED_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{flag} must remain false")

    surfaces = record.get("surfaces")
    if not isinstance(surfaces, list):
        errors.append("surfaces must be a list")
        surfaces = []

    names = []
    for index, surface in enumerate(surfaces):
        if not isinstance(surface, dict):
            errors.append(f"surface[{index}] must be a dictionary")
            continue
        name = surface.get("surface")
        names.append(name)
        for key in sorted(set(surface) - SURFACE_KEYS):
            errors.append(f"surface {name!r} has unsupported key {key!r}")
        if name not in EXPECTED_SURFACES:
            errors.append(f"unexpected surface {name!r}")
        if surface.get("state") not in ALLOWED_STATES:
            errors.append(f"unsupported state {surface.get('state')!r} for surface {name!r}")
        if surface.get("maturity") not in ALLOWED_MATURITIES:
            errors.append(f"unsupported maturity {surface.get('maturity')!r} for surface {name!r}")
        docs = surface.get("governing_docs")
        if not isinstance(docs, list) or not docs:
            errors.append(f"surface {name!r} governing_docs must be a non-empty list")
        elif "BLK-077" not in docs:
            errors.append(f"surface {name!r} must cite BLK-077")
        cutline = surface.get("authority_cutline")
        if not isinstance(cutline, str) or not cutline.strip():
            errors.append(f"surface {name!r} authority_cutline must be a non-empty string")
        elif len(cutline) > 900:
            errors.append(f"surface {name!r} authority_cutline exceeds lean current-state length")

    if set(names) != set(EXPECTED_SURFACES):
        errors.append("surfaces must match the lean current-state surface set exactly")
    if len(names) != len(set(names)):
        errors.append("surfaces must not contain duplicates")

    scan_candidate = {k: v for k, v in record.items() if k not in DENIED_FLAGS}
    errors.extend(scan_for_authority_laundering(scan_candidate, denied_keys=DENIED_FLAGS))
    return errors


def validate_active_current_state_docs(roadmap_text, index_text):
    errors = []
    if not isinstance(roadmap_text, str) or not isinstance(index_text, str):
        return ["active docs must be strings"]
    combined = f"{roadmap_text}\n{index_text}"

    for marker in ACTIVE_DOC_REQUIRED_MARKERS:
        if marker not in combined:
            errors.append(f"active docs missing required marker {marker!r}")
    for marker in STALE_ACTIVE_DOC_MARKERS:
        if marker in combined:
            errors.append(f"active docs contain stale marker {marker!r}")

    if set(DOC_DENIAL_MARKERS) != set(DENIED_FLAGS):
        errors.append("DOC_DENIAL_MARKERS must exactly cover DENIED_FLAGS")

    for flag in DENIED_FLAGS:
        markers = DOC_DENIAL_MARKERS.get(flag, ())
        if not markers:
            errors.append(f"{flag} has no active-doc denial marker")
            continue
        if not any(marker in combined for marker in markers):
            errors.append(f"{flag} missing active-doc denial marker {markers!r}")
    errors.extend(scan_for_authority_laundering(combined, path="active_docs", denied_keys=DENIED_FLAGS))
    return errors


def evaluate_current_state_authority_index(record=None):
    candidate = build_current_state_authority_index() if record is None else deepcopy(record)
    errors = validate_current_state_authority_index(candidate)
    candidate["evaluation"] = BLOCKED if errors else READY
    candidate["validation_errors"] = errors
    for flag in DENIED_FLAGS:
        candidate[flag] = False
    return candidate
