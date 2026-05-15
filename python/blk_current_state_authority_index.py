from copy import deepcopy

INDEX_ID = "blk_system_current_state_authority_index"
INDEX_STATUS = "BLK_SYSTEM_CURRENT_STATE_AUTHORITY_INDEX"
READY = "CURRENT_STATE_INDEX_READY_FOR_OPERATOR_REVIEW_NOT_AUTHORITY"
BLOCKED = "CURRENT_STATE_INDEX_BLOCKED"
MATURITY = "CURRENT_STATE_INDEX_L0_L1_ONLY"

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
    "BLK-078 tactical standard profile architecture",
    "BLK-080 tactical profile registry / Layer B extraction",
    "BLK-081 target-repo execution governance pattern",
    "BLK-082 BLK-058 mechanical enforcement upgrade",
    "BLK-083 BEO publication decision package / pilot request",
    "BLK-084 post-083 frontier selection gate refresh",
    "BLK-085 BEO publication pilot execution request gate",
    "BLK-086 BEO publication pilot approval decision",
    "BLK-087 exact BEO publication pilot execution",
    "BLK-088 RTM authority request after local BEO pilot prerequisites",
    "BLK-089 RTM authority approval decision capture",
    "BLK-090 exact local RTM generation pilot",
    "BLK-091 RTM drift-review request gate",
    "BLK-092 post-091 roadmap/current-state reconciliation",
    "BLK-093 RTM drift-rejection approval decision capture",
    "BLK-094 post-093 roadmap / RTM-ladder alignment",
    "BLK-095 exact local RTM drift-rejection execution",
    "BLK-096 post-095 local RTM ladder reconciliation",
    "BLK-097 bounded BLK-test evidence refresh",
    "BLK-098 BEO publication prerequisite request after evidence refresh",
    "BLK-099 external BEO publication approval decision capture",
    "BLK-100 external BEO publication execution",
    "BLK-101 RTM trace-closure authority request",
    "BLK-102 RTM trace-closure approval decision capture",
    "BLK-103 exact local RTM trace-closure execution",
    "BLK-104 post-103 roadmap/current-state reconciliation",
    "BLK-115 production-hardening reconciliation gate",
    "BLK-058 Kuronode TypeScript tactical profile source",
)

ALLOWED_STATES = {
    "doctrine_and_fixture_boundary",
    "local_guarded_enforcement",
    "fail_fast_convenience_layer",
    "repository_owned_local_profiles",
    "disabled_gated_evidence_only",
    "advisory_local_pilot",
    "review_ready_not_execution_authorized",
    "external_beo_publication_record_only",
    "local_rtm_trace_closure_record_only",
    "doctrine_only_profile_architecture",
    "tactical_profile_registry_l0_l1_fixture_complete",
    "target_repo_governance_l0_l1_fixture_complete",
    "blk058_mechanical_enforcement_l0_l1_fixture_complete",
    "beo_publication_decision_package_l0_l1_review_fixture_complete",
    "post083_frontier_selection_l0_l1_fixture_complete",
    "beo_publication_pilot_request_gate_l0_l1_complete",
    "beo_publication_pilot_approval_decision_captured_l0_l1",
    "beo_publication_pilot_execution_local_only_complete",
    "rtm_authority_request_after_local_beo_pilot_l0_l1_review_complete",
    "rtm_generation_approval_decision_captured_l0_l1",
    "exact_local_rtm_generation_pilot_complete",
    "rtm_drift_review_request_complete",
    "post091_roadmap_current_state_reconciliation_l0_l1_complete",
    "rtm_drift_rejection_approval_decision_captured_l0_l1",
    "post093_roadmap_rtm_ladder_alignment_l0_l1_complete",
    "exact_local_rtm_drift_rejection_execution_complete",
    "post095_local_rtm_ladder_reconciliation_l0_l1_complete",
    "bounded_blk_test_evidence_refresh_complete",
    "beo_publication_prerequisite_request_after_evidence_refresh_l0_l1_complete",
    "external_beo_publication_approval_decision_captured_l0_l1",
    "external_beo_publication_execution_record_complete",
    "rtm_trace_closure_authority_request_after_external_beo_l0_l1_complete",
    "rtm_trace_closure_approval_decision_captured_l0_l1",
    "exact_local_rtm_trace_closure_execution_complete",
    "post103_roadmap_current_state_reconciliation_l0_l1_complete",
    "post103_pipe_hardening_bridge_l0_l1_complete",
    "blk_req_gateway_foundation_116_119_complete",
    "blk_req_hitl_baseline_promotion_120_complete",
    "blk_req_revision_lifecycle_122_124_complete",
    "blk_req_to_beb_beo_metadata_handoff_125_complete",
    "beo_publication_path_decision_gate_126_review_complete",
    "metadata_bound_beo_publication_prerequisite_request_127_complete",
    "blk_req_metadata_bound_publication_request_127_complete",
    "external_beo_publication_approval_capture_128_complete",
    "external_beo_publication_execution_129_record_complete",
    "metadata_bound_rtm_trace_closure_authority_request_130_complete",
    "metadata_bound_rtm_trace_closure_approval_capture_131_complete",
    "metadata_bound_local_rtm_trace_closure_execution_record_132_complete",
    "production_blk_link_rtm_trace_closure_authority_request_133_complete",
    "production_blk_link_rtm_trace_closure_approval_capture_134_complete",
    "target_profile_source_not_dispatch_authority",
}

ALLOWED_MATURITIES = {
    "L0_L1_DOCTRINE_FIXTURE",
    "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
    "L1_L2_STYLE_PREFLIGHT_ONLY",
    "MATURE_LOCAL_PROFILE_SUPPORT",
    "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
    "ADVISORY_PILOT_ONLY",
    "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
    "L2_RECORD_ONLY_EXTERNAL_BEO_PUBLICATION_NO_SIGNER_STORAGE_LEDGER",
    "L1_LOCAL_RTM_TRACE_CLOSURE_RECORD_NOT_PRODUCTION_BLK_LINK",
    "FIXTURE_OFFLINE_LOCAL_EVIDENCE_ONLY",
    "L0_ARCHITECTURE_DOCTRINE_ONLY",
    "L0_L1_PROFILE_REGISTRY_FIXTURE_DOCTRINE",
    "L0_L1_TARGET_REPO_GOVERNANCE_FIXTURE_DOCTRINE",
    "L0_L1_BLK058_MECHANICAL_ENFORCEMENT_FIXTURE",
    "L0_L1_BEO_PUBLICATION_DECISION_PACKAGE_REVIEW_FIXTURE",
    "L0_L1_POST083_FRONTIER_SELECTION_FIXTURE",
    "L0_L1_BEO_PUBLICATION_PILOT_REQUEST_GATE",
    "L0_L1_BEO_PUBLICATION_PILOT_APPROVAL_DECISION",
    "L1_EXACT_BEO_PUBLICATION_PILOT_EXECUTION_LOCAL_ONLY",
    "L0_L1_RTM_AUTHORITY_REQUEST_REVIEW_ONLY",
    "L0_L1_RTM_GENERATION_APPROVAL_DECISION",
    "L1_EXACT_LOCAL_RTM_GENERATION_PILOT",
    "L0_L1_RTM_DRIFT_REVIEW_REQUEST_ONLY",
    "L0_L1_POST091_RECONCILIATION_DOCTRINE_GATE",
    "L0_L1_RTM_DRIFT_REJECTION_APPROVAL_DECISION",
    "L0_L1_POST093_ALIGNMENT_DOCTRINE_GATE",
    "L1_EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION",
    "L0_L1_POST095_RECONCILIATION_DOCTRINE_GATE",
    "L4_EXACT_EVIDENCE_ONLY_BLK_TEST_REFRESH",
    "L0_L1_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
    "L0_L1_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION",
    "L2_EXACT_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
    "L0_L1_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_REVIEW_ONLY",
    "L0_L1_RTM_TRACE_CLOSURE_APPROVAL_DECISION",
    "L1_EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD",
    "L0_L1_POST103_RECONCILIATION_DOCTRINE_GATE",
    "L0_L1_POST103_PIPE_HARDENING_RECONCILIATION_GATE",
    "L0_L1_BLK_REQ_GATEWAY_FOUNDATION_NO_PROMOTION",
    "L1_BLK_REQ_NEW_BASELINE_PROMOTION_BACKEND",
    "L1_BLK_REQ_REVISION_LIFECYCLE_BACKEND",
    "L1_BLK_REQ_METADATA_HANDOFF_VALIDATION",
    "L0_L1_BEO_PUBLICATION_PATH_DECISION_GATE_REVIEW_ONLY",
    "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
    "L0_L1_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_DECISION",
    "L2_EXACT_METADATA_BOUND_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
    "L0_L1_METADATA_BOUND_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_REVIEW_ONLY",
    "L0_L1_METADATA_BOUND_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_DECISION",
    "L1_METADATA_BOUND_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD",
    "L0_L1_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_REVIEW_ONLY",
    "L0_L1_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_DECISION",
    "L0_LAYER_C_PROFILE_SOURCE_ONLY",
}

FORBIDDEN_AUTHORITY_WORDING = (
    "approved_for_live_execution",
    "authoritative beo publication approved",
    "approved for runtime execution",
    "runtime execution approved",
    "live_execution_enabled",
    "l5_production_authority",
    "rtm_drift_rejection_authorized_by_index",
    "protected_body_read_authorized_by_index",
    "production_sandbox_enforced_by_index",
    "network_tooling_authorized_by_index",
    "package_manager_authorized_by_index",
)

GENERIC_FORBIDDEN_AUTHORITY_KEYS = {
    "authority",
    "approved",
    "authorized",
    "approval_status",
    "execution_authorized",
    "runtime_authority",
    "live_authority",
    "publication_authorized",
    "rtm_authorized",
    "drift_authorized",
    "protected_body_read_authorized",
}

DENIED_FLAGS = (
    "runtime_authority_granted",
    "live_codex_execution_authorized",
    "blk_pipe_dispatch_authorized",
    "production_blk_test_mcp_authorized",
    "authoritative_beo_publication_authorized",
    "runtime_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "protected_blk_req_body_reads_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
)

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

FORBIDDEN_AUTHORITY_VALUE_WORDING = tuple(DENIED_FLAGS) + (
    "execution_authorized",
    "approved_for_runtime_execution",
    "runtime_execution_authorized",
    "runtime_authority",
    "live_authority",
    "live execution authorized",
    "live codex execution authorized",
    "live codex execution is authorized",
    "live codex execution authority",
    "runtime authority granted",
    "runtime execution authorized",
    "runtime execution is authorized",
    "production blk test mcp authority",
    "production blk test mcp is authorized",
    "authoritative beo publication authority",
    "authoritative beo publication is authorized",
    "rtm drift rejection authority",
    "rtm drift rejection is authorized",
    "protected blk req body reads authorized",
    "protected blk req body reads are authorized",
    "network tooling authority",
    "network tooling is authorized",
    "package manager authority",
    "package manager is authorized",
    "package managers are authorized",
    "package manager tooling authority",
    "package manager tooling is authorized",
    "model service is authorized",
    "browser tooling is authorized",
    "cyber tooling is authorized",
    "network model browser cyber tooling is authorized",
    "network model cyber browser tooling is authorized",
    "production sandbox enforced",
    "production sandbox is enforced",
    "production isolation is claimed",
    "production isolation claims are authorized",
    "git mutation authorized",
    "git mutation allowed",
    "git commit authorized",
    "git commit allowed",
    "git push authorized",
    "git push allowed",
    "staging authorized",
    "staging allowed",
    "autofix authorized",
    "autofix allowed",
    "source mutation authorized",
    "source mutation allowed",
    "git mutation authority",
    "source mutation authority",
    "target repo mutation authority",
    "protected-body reads authority",
    "protected body reads authority",
    "drift-review approval captured",
    "drift review approval captured",
    "rtm drift rejection approval captured",
    "rtm drift rejection approval granted",
    "drift-review execution approved",
    "drift rejection execution approved",
    "rtm drift rejection has been approved",
    "rtm drift rejection approved for execution",
    "runtime rtm generation approved",
    "protected blk req body reads approved",
    "active vault comparison authorized",
    "external ledger mutation authorized",
    "beb dispatch authorized",
    "beo closeout execution approved",
    "package manager allowed",
    "source mutation approved",
    "external authoritative publication approved",
    "production isolation enforced",
    "rtm drift rejection approved",
    "beb dispatch approved",
    "beo closeout authorized",
    "package manager approved",
    "authoritative drift decision made",
    "runtime blk-link trace closure occurred",
    "runtime blk link trace closure occurred",
    "runtime blk link trace closure is authorized",
    "runtime blk-link trace closure is authorized",
    "runtime blk link trace closure authorized",
    "runtime blk-link trace closure authorized",
    "runtime trace closure authorized",
    "runtime trace closure is authorized",
    "runtime blk link trace closure complete",
    "runtime blk-link trace closure complete",
    "runtime blk link trace closure is complete",
    "runtime blk-link trace closure is complete",
    "runtime trace closure complete",
    "runtime trace closure is complete",
    "runtime rtm generation authorized",
    "runtime rtm generation is authorized",
    "runtime rtm generation granted",
    "runtime rtm generation is granted",
    "authoritative beo publication granted",
    "authoritative beo publication is granted",
    "external authoritative publication granted",
    "external authoritative publication is granted",
    "authoritative drift decision is made",
    "authoritative drift decision complete",
    "authoritative drift decision is complete",
    "authoritative trace closure occurred",
    "authoritative trace closure established",
    "authoritative trace closure is established",
    "active vault hash comparison is complete",
    "active-vault hash comparison is complete",
    "active vault comparison is complete",
    "active-vault comparison is complete",
    "active vault comparison established",
    "active-vault comparison established",
    "active vault comparison is established",
    "active-vault comparison is established",
    "coverage truth established",
    "coverage truth is established",
    "coverage truth granted",
    "coverage truth is granted",
    "reusable rtm drift rejection granted",
    "reusable rtm drift rejection is granted",
    "reusable drift rejection granted",
    "active-vault hash comparison performed",
    "active vault hash comparison performed",
    "active-vault comparison performed",
    "active vault comparison performed",
    "protected-body reads are enabled",
    "protected body reads are enabled",
    "external ledger mutation performed",
    "exact-id retrieval authorized",
    "exact id retrieval authorized",
    "exact-id retrieval is authorized",
    "staged revision overwrite authorized",
    "staged revision overwrite is authorized",
    "public-authority ledger rollback authorized",
    "public authority ledger rollback authorized",
    "public-authority ledger rollback is authorized",
)

FORBIDDEN_AUTHORITY_COMPACT_WORDING = (
    "approvedforruntimeexecution",
    "runtimeexecutionauthorized",
    "runtimeexecutionisauthorized",
    "runtimeauthoritygranted",
    "livecodexexecutionauthorized",
    "livecodexexecutionisauthorized",
    "liveexecutionauthorized",
    "productionblktestmcpauthorized",
    "productionblktestmcpisauthorized",
    "authoritativebeopublicationauthorized",
    "authoritativebeopublicationisauthorized",
    "rtmdriftrejectionauthorized",
    "rtmdriftrejectionisauthorized",
    "protectedblkreqbodyreadsauthorized",
    "protectedblkreqbodyreadsareauthorized",
    "protectedbodyreadsauthorized",
    "networktoolingisauthorized",
    "networktoolingauthorized",
    "packagemanagertoolingisauthorized",
    "packagemanagertoolingauthorized",
    "packagemanagerisauthorized",
    "packagemanagersareauthorized",
    "packagemanagerauthorized",
    "networkmodelbrowsercybertoolingisauthorized",
    "networkmodelbrowsercybertoolingauthorized",
    "networkmodelcyberbrowsertoolingauthorized",
    "networkmodelcyberbrowsertoolingisauthorized",
    "modelserviceisauthorized",
    "browsertoolingisauthorized",
    "cybertoolingisauthorized",
    "productionsandboxisenforced",
    "productionisolationclaimed",
    "productionisolationisclaimed",
    "productionisolationclaimsareauthorized",
    "gitmutationauthorized",
    "gitmutationallowed",
    "gitcommitauthorized",
    "gitcommitallowed",
    "gitpushauthorized",
    "gitpushallowed",
    "stagingauthorized",
    "stagingallowed",
    "autofixauthorized",
    "autofixallowed",
    "sourcemutationauthorized",
    "sourcemutationallowed",
    "gitmutationauthority",
    "sourcemutationauthority",
    "targetrepomutationauthority",
    "protectedbodyreadsauthority",
    "driftreviewapprovalcaptured",
    "rtmdriftrejectionapprovalcaptured",
    "rtmdriftrejectionapprovalgranted",
    "driftreviewexecutionapproved",
    "driftrejectionexecutionapproved",
    "rtmdriftrejectionhasbeenapproved",
    "activevaultcomparisonauthorized",
    "bebdispatchauthorized",
    "packagemanagerallowed",
    "authoritativedriftdecisionmade",
    "runtimeblklinktraceclosureoccurred",
    "runtimeblklinktraceclosureauthorized",
    "runtimeblklinktraceclosureisauthorized",
    "runtimeblklinktraceclosurecomplete",
    "runtimeblklinktraceclosureiscomplete",
    "runtimetraceclosureauthorized",
    "runtimetraceclosureisauthorized",
    "runtimetraceclosurecomplete",
    "runtimetraceclosureiscomplete",
    "runtimertmgenerationauthorized",
    "runtimertmgenerationisauthorized",
    "runtimertmgenerationgranted",
    "runtimertmgenerationisgranted",
    "authoritativebeopublicationgranted",
    "authoritativebeopublicationisgranted",
    "externalauthoritativepublicationgranted",
    "externalauthoritativepublicationisgranted",
    "authoritativedriftdecisionismade",
    "authoritativedriftdecisioncomplete",
    "authoritativedriftdecisioniscomplete",
    "authoritativetraceclosureoccurred",
    "authoritativetraceclosureestablished",
    "authoritativetraceclosureisestablished",
    "activevaulthashcomparisoncomplete",
    "activevaulthashcomparisoniscomplete",
    "activevaultcomparisoncomplete",
    "activevaultcomparisoniscomplete",
    "activevaultcomparisonestablished",
    "activevaultcomparisonisestablished",
    "coveragetruthestablished",
    "coveragetruthisestablished",
    "coveragetruthgranted",
    "coveragetruthisgranted",
    "reusablertmdriftrejectiongranted",
    "reusablertmdriftrejectionisgranted",
    "reusabledriftrejectiongranted",
    "reusabledriftrejectionisgranted",
    "activevaulthashcomparisonperformed",
    "activevaultcomparisonperformed",
    "protectedbodyreadsenabled",
    "externalledgermutationperformed",
    "exactidretrievalauthorized",
    "exactidretrievalisauthorized",
    "stagedrevisionoverwriteauthorized",
    "stagedrevisionoverwriteisauthorized",
    "publicauthorityledgerrollbackauthorized",
    "publicauthorityledgerrollbackisauthorized",
)

DEFAULT_SURFACES = (
    {
        "surface": "BLK-req legislative gateway",
        "state": "blk_req_metadata_bound_publication_request_127_complete",
        "maturity": "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
        "governing_docs": ["BLK-002", "BLK-005", "BLK-006", "BLK-077", "BLK-116", "BLK-117", "BLK-118", "BLK-119", "BLK-120"],
        "authority_cutline": "BLK_SYSTEM_124_STAGED_REVISION_PROMOTION_COMPLETE covers exact-ID retrieval, staged revision drafts, and approval-bound staged revision promotion for BLK-req backend paths. BLK_SYSTEM_125_BEB_BEO_METADATA_HANDOFF_COMPLETE closes metadata-only BEB/BEO handoff validation: exact REQ-###/UC-### IDs and canonical version_hash values may pass as trace metadata only. EXACT_BLK_REQ_TRACE_METADATA_HANDOFF_COMPLETE_BY_125 and BEB_BEO_METADATA_HANDOFF_NO_PROTECTED_BODY_COPY_BY_125 remain closed. BLK_SYSTEM_126_BEO_PUBLICATION_PATH_DECISION_GATE_COMPLETE keeps protected bodies isolated. BLK_SYSTEM_127_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_COMPLETE packages the metadata interface and decision gate into BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001. BLK_SYSTEM_128_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_COMPLETE records BEO-PUBLICATION-APPROVAL-CAPTURE-128-001 as approval capture only. BLK_SYSTEM_129_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD_COMPLETE emits BEO-PUBLICATION-EXECUTION-129-001 as record-only external BEO publication evidence. BLK_SYSTEM_130_METADATA_BOUND_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE emits RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001 as review-only trace-closure approval request evidence. BLK_SYSTEM_131_METADATA_BOUND_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE emits RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001 as exact approval capture only. BLK_SYSTEM_132_METADATA_BOUND_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD_COMPLETE emits RTM-TRACE-CLOSURE-EXECUTION-132-001 and RTM-TRACE-CLOSURE-RECORD-132-001 as local non-authoritative trace-closure evidence only. BLK_SYSTEM_133_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE emits PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001 as request-only review evidence. BLK_SYSTEM_134_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE emits PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001 as approval capture only and reserves RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001 without consuming it. NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_PLANNING_NOT_EXECUTION_AUTHORITY. Protected bodies remain isolated from trace closure. No BEB dispatch, no BEO closeout execution; no BLK-pipe runtime dispatch, no BLK-test runtime, no RTM generation or drift rejection, no active-vault hash comparison, no coverage truth, no non-BLK-req target/source/Git mutation, no tooling, no signer/storage/public-authority-ledger/rollback behavior, and no production-isolation claim is granted.",
    },
    {
        "surface": "BLK-pipe blast shield",
        "state": "local_guarded_enforcement",
        "maturity": "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
        "governing_docs": ["BLK-004", "BLK-077", "BLK-112", "BLK-113", "BLK-114", "BLK-115"],
        "authority_cutline": "BLK-pipe remains final local mutation enforcement authority after the 112-115 hardening bridge; less-trusted or autonomous boundaries must use repository-owned validation profiles and report diagnostic evidence, but no BLK-pipe runtime dispatch, target mutation, protected-body reads, BLK-test runtime, BEO, RTM, tooling, or production isolation claim is granted.",
    },
    {
        "surface": "Python adapter layer",
        "state": "fail_fast_convenience_layer",
        "maturity": "L1_L2_STYLE_PREFLIGHT_ONLY",
        "governing_docs": ["BLK-004", "BLK-077"],
        "authority_cutline": "Adapter checks reduce operator mistakes but do not replace Go enforcement and do not create sandbox, network, or host-secret-isolation claims.",
    },
    {
        "surface": "Validation profiles",
        "state": "repository_owned_local_profiles",
        "maturity": "MATURE_LOCAL_PROFILE_SUPPORT",
        "governing_docs": ["BLK-004", "BLK-077"],
        "authority_cutline": "Profiles constrain validation commands but do not grant package-manager, network, secret-reading, BLK-test, BEO, RTM, or arbitrary shell authority.",
    },
    {
        "surface": "BLK-test",
        "state": "disabled_gated_evidence_only",
        "maturity": "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
        "governing_docs": ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-077"],
        "authority_cutline": "BLK-test returns evidence only. Production MCP remains disabled. No source mutation, publication, RTM generation, arbitrary shell, or protected body reads.",
    },
    {
        "surface": "Operator health / observability",
        "state": "advisory_local_pilot",
        "maturity": "ADVISORY_PILOT_ONLY",
        "governing_docs": ["BLK-031", "BLK-032", "BLK-033", "BLK-034", "BLK-035", "BLK-036", "BLK-037", "BLK-038", "BLK-039", "BLK-077"],
        "authority_cutline": "PASS is advisory only. Health checks do not become BLK-test verification, execution approval, or production sandbox evidence.",
    },
    {
        "surface": "Codex live-dispatch ladder",
        "state": "review_ready_not_execution_authorized",
        "maturity": "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
        "governing_docs": ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044", "BLK-077"],
        "authority_cutline": "Review-ready and design-ready evidence is not execution-authorized. No live Codex subprocess, BLK-pipe dispatch from a Codex adapter, source mutation, package/network/model/cyber/browser tooling, or production isolation authority.",
    },
    {
        "surface": "BEO publication path",
        "state": "external_beo_publication_execution_129_record_complete",
        "maturity": "L2_EXACT_METADATA_BOUND_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
        "governing_docs": ["BLK-014", "BLK-016", "BLK-021", "BLK-022", "BLK-026", "BLK-028", "BLK-077", "BLK-098", "BLK-099", "BLK-100", "BLK-104"],
        "authority_cutline": "BLK-100 produced PUBLISHED_EXTERNAL_BEO_RECORD for BEO-054-001 as historical record-only external publication evidence. BLK_SYSTEM_127_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_COMPLETE produced BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001. BLK_SYSTEM_128_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_COMPLETE added python/metadata_bound_external_beo_publication_approval_capture.py and BEO-PUBLICATION-APPROVAL-CAPTURE-128-001 as the exact approval-capture decision package. BLK_SYSTEM_129_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD_COMPLETE adds python/metadata_bound_external_beo_publication_execution.py and BEO-PUBLICATION-EXECUTION-129-001 as exact record-only publication execution evidence for the BLK-127 metadata-bound BEO, marks RUN-BLK-SYSTEM-129-EXTERNAL-BEO-PUBLICATION-001 consumed in the record, and produces execution package hash sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c. BLK_SYSTEM_130_METADATA_BOUND_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE consumes that record only as prerequisite evidence for RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001. BLK_SYSTEM_131_METADATA_BOUND_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE captures approval for that request only and reserves RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001 without consuming it. BLK_SYSTEM_132_METADATA_BOUND_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD_COMPLETE consumes that run ID inside RTM-TRACE-CLOSURE-EXECUTION-132-001 as local non-authoritative trace-closure evidence only. BLK_SYSTEM_133_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE consumes that local evidence only as prerequisite review evidence for PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001. BLK_SYSTEM_134_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE captures approval for that exact request only in PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001 and reserves RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001 without consuming it. signer/storage/ledger publication remains disabled: no signer key material, no cryptographic signing, no immutable storage, no public ledger append, no rollback/revocation/supersession, no reusable publication grant, no BEO closeout execution, no RTM inheritance, no protected-body reads, no target/source/Git mutation, no BLK-pipe/BLK-test/Codex runtime grant, no tooling, and no production isolation authority.",
    },
    {
        "surface": "RTM / blk-link",
        "state": "production_blk_link_rtm_trace_closure_approval_capture_134_complete",
        "maturity": "L0_L1_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_DECISION",
        "governing_docs": ["BLK-023", "BLK-027", "BLK-029", "BLK-030", "BLK-033", "BLK-077", "BLK-100", "BLK-101", "BLK-102", "BLK-103", "BLK-104"],
        "authority_cutline": "BLK-103 produced PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE as historical local non-authoritative trace-closure evidence. BLK_SYSTEM_130_METADATA_BOUND_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE added python/metadata_bound_rtm_trace_closure_authority_request.py and RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001 as review-only approval-request evidence bound to BEO-PUBLICATION-EXECUTION-129-001 and hash sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2. BLK_SYSTEM_131_METADATA_BOUND_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE adds python/metadata_bound_rtm_trace_closure_approval_capture.py and RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001 as exact approval-capture evidence with package hash sha256:c41c8bd4e7b5aba387a0db5b439d9bb664a1610f70eaff50488ed6cceabbbba0 and future run RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001 reserved but not consumed. BLK_SYSTEM_132_METADATA_BOUND_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD_COMPLETE adds python/metadata_bound_local_rtm_trace_closure_execution_record.py, consumes RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001 in local evidence, and emits RTM-TRACE-CLOSURE-EXECUTION-132-001 / RTM-TRACE-CLOSURE-RECORD-132-001 with package hash sha256:548934403cd71a4eebc27c4e164a43f9e2d7f71b8cfab7765b1f51e65f44fed5. BLK_SYSTEM_133_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_COMPLETE adds python/production_blk_link_rtm_trace_closure_authority_request.py and PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001 as request-only review evidence with package hash sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271. BLK_SYSTEM_134_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_COMPLETE adds python/production_blk_link_rtm_trace_closure_approval_capture.py and PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001 as approval-capture evidence with package hash sha256:284bd944f7e854a9c589e923908053da37e27ce9c32d841090578837111e49bf, approval hash sha256:9487b2433a4b5a53ea056f7d8d1257a0292ce8cfab31c989d9de3d4bed4c31ba, and future run RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001 reserved but not consumed. NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_PLANNING_NOT_EXECUTION_AUTHORITY. Production/reusable blk-link remains disabled unless a future exact execution sprint consumes the reserved run: no no runtime RTM generation authority, no RTM drift rejection, no authoritative drift decision, no active-vault hash comparison, no coverage-truth promotion, no protected-body reads, no public ledger mutation, no target/source/Git mutation, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-078 tactical standard profile architecture",
        "state": "doctrine_only_profile_architecture",
        "maturity": "L0_ARCHITECTURE_DOCTRINE_ONLY",
        "governing_docs": ["BLK-077", "BLK-078"],
        "authority_cutline": "BLK-078 Layer A, Layer B, and Layer C profile architecture is doctrine only; it does not authorize scans, mutation, dispatch, BLK-test, BEO, or RTM.",
    },
    {
        "surface": "BLK-080 tactical profile registry / Layer B extraction",
        "state": "tactical_profile_registry_l0_l1_fixture_complete",
        "maturity": "L0_L1_PROFILE_REGISTRY_FIXTURE_DOCTRINE",
        "governing_docs": ["BLK-077", "BLK-078", "BLK-080"],
        "authority_cutline": "BLK-080 completed python/blk_tactical_profile_registry.py and docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md; profile-selection registry and Layer B extraction are L0/L1 fixture/doctrine surfaces feeding target-repo execution governance, and there is no target-repo mutation, scan, BEB dispatch or BEO closeout execution, Codex, BLK-pipe, BLK-test, BEO, RTM, protected-body, tooling, or sandbox authority.",
    },
    {
        "surface": "BLK-081 target-repo execution governance pattern",
        "state": "target_repo_governance_l0_l1_fixture_complete",
        "maturity": "L0_L1_TARGET_REPO_GOVERNANCE_FIXTURE_DOCTRINE",
        "governing_docs": ["BLK-077", "BLK-078", "BLK-080", "BLK-081"],
        "authority_cutline": "BLK-081 completed python/blk_target_repo_execution_governance.py and docs/BLK-081_target-repo-execution-governance-pattern.md; target-repo execution governance is an L0/L1 fixture/doctrine surface feeding BLK-058 mechanical enforcement and future explicit frontier decisions, and there is no target-repo scan, no target-repo mutation, no BEB dispatch or BEO closeout execution, no approval retargeting, no Codex, BLK-pipe, BLK-test, BEO publication, RTM, protected-body, tooling, or sandbox authority.",
    },
    {
        "surface": "BLK-082 BLK-058 mechanical enforcement upgrade",
        "state": "blk058_mechanical_enforcement_l0_l1_fixture_complete",
        "maturity": "L0_L1_BLK058_MECHANICAL_ENFORCEMENT_FIXTURE",
        "governing_docs": ["BLK-058", "BLK-077", "BLK-078", "BLK-080", "BLK-081", "BLK-082"],
        "authority_cutline": "BLK-082 completed python/blk_058_mechanical_enforcement.py and docs/BLK-082_blk058-mechanical-enforcement-upgrade.md; BLK-058 mechanical enforcement is submitted-snippet fixture evidence only, after BLK-SYSTEM-082 the next movement requires explicit operator decision, and there is no target-repo scan, no target-repo mutation, no BEB dispatch or BEO closeout execution, no BEO publication, no RTM, no protected-body, tooling, or sandbox authority.",
    },
    {
        "surface": "BLK-083 BEO publication decision package / pilot request",
        "state": "beo_publication_decision_package_l0_l1_review_fixture_complete",
        "maturity": "L0_L1_BEO_PUBLICATION_DECISION_PACKAGE_REVIEW_FIXTURE",
        "governing_docs": ["BLK-022", "BLK-026", "BLK-057", "BLK-060", "BLK-077", "BLK-083"],
        "authority_cutline": "BLK-083 completed python/beo_publication_decision_package.py and docs/BLK-083_beo-publication-decision-package-pilot-request.md; the BEO publication decision package is an L0/L1 human-review request fixture, future explicit human publication pilot approval is still required, and there is no publication approval, no publication pilot execution, no signer/storage/ledger/rollback side effects, no RTM generation, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-084 post-083 frontier selection gate refresh",
        "state": "post083_frontier_selection_l0_l1_fixture_complete",
        "maturity": "L0_L1_POST083_FRONTIER_SELECTION_FIXTURE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-083", "BLK-084"],
        "authority_cutline": "BLK-084 completed python/blk_post083_frontier_selection_gate.py and docs/BLK-084_post-083-frontier-selection-gate-refresh.md; post-083 frontier selection is L0/L1 fixture evidence only, next logical sprint is not approval, actual higher-authority frontier execution still requires separate explicit human decision naming exactly one frontier, and there is no publication approval, no publication pilot execution, no BLK-test runtime, no Codex execution, no BLK-pipe dispatch, no RTM generation, no protected-body reads, no target-repo scan or mutation authority is granted.",
    },
    {
        "surface": "BLK-085 BEO publication pilot execution request gate",
        "state": "beo_publication_pilot_request_gate_l0_l1_complete",
        "maturity": "L0_L1_BEO_PUBLICATION_PILOT_REQUEST_GATE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-083", "BLK-084", "BLK-085"],
        "authority_cutline": "BLK-085 completed python/beo_publication_pilot_execution_request.py and docs/BLK-085_beo-publication-pilot-execution-request-gate.md; the BEO publication pilot execution request gate is L0/L1 request evidence only, explicit human publication pilot approval is still required, and there is no publication approval, no publication pilot execution, no signer/storage/ledger/rollback side effects, no RTM generation, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-086 BEO publication pilot approval decision",
        "state": "beo_publication_pilot_approval_decision_captured_l0_l1",
        "maturity": "L0_L1_BEO_PUBLICATION_PILOT_APPROVAL_DECISION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-083", "BLK-085", "BLK-086"],
        "authority_cutline": "BLK-086 completed python/beo_publication_pilot_approval_decision.py and docs/BLK-086_beo-publication-pilot-approval-decision.md; the exact BLK-085 approval decision captured approval for one future publication-pilot execution sprint, and BLK-SYSTEM-087 later consumed the reserved run ID in a local-only pilot. BLK-086 itself did not execute the pilot and remains approval-decision evidence only. External authoritative publication remains disabled; no signer/storage/ledger/rollback side effects, no RTM generation, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no package/network/model/browser/cyber tooling authority, and no production isolation claim remains active.",
    },
    {
        "surface": "BLK-087 exact BEO publication pilot execution",
        "state": "beo_publication_pilot_execution_local_only_complete",
        "maturity": "L1_EXACT_BEO_PUBLICATION_PILOT_EXECUTION_LOCAL_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-083", "BLK-085", "BLK-086", "BLK-087"],
        "authority_cutline": "BLK-087 completed python/beo_publication_pilot_execution.py and docs/BLK-087_exact-beo-publication-pilot-execution.md; the exact BLK-086-bound local publication pilot executed once and consumed RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001, producing PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE as deterministic local artifact evidence. External authoritative publication remains disabled; no signer/storage/ledger/rollback side effects, no RTM generation or drift rejection, no protected-body reads, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },

    {
        "surface": "BLK-088 RTM authority request after local BEO pilot prerequisites",
        "state": "rtm_authority_request_after_local_beo_pilot_l0_l1_review_complete",
        "maturity": "L0_L1_RTM_AUTHORITY_REQUEST_REVIEW_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-083", "BLK-085", "BLK-086", "BLK-087", "BLK-088"],
        "authority_cutline": "BLK-088 completed python/rtm_authority_request_after_beo_pilot.py and docs/BLK-088_rtm-authority-request-after-local-beo-pilot-prerequisites.md; request package RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001 records REQUEST_ONLY_NOT_GRANTED and asks for future human review only. It grants no RTM generation, no drift rejection, no active-vault hash comparison, no coverage claim, no protected-body reads, no external authoritative publication, no BEB dispatch or BEO closeout execution, no signer/storage/ledger/rollback side effects, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no package/network/model/browser/cyber tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-089 RTM authority approval decision capture",
        "state": "rtm_generation_approval_decision_captured_l0_l1",
        "maturity": "L0_L1_RTM_GENERATION_APPROVAL_DECISION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-088", "BLK-089"],
        "authority_cutline": "BLK-089 completed python/rtm_generation_approval_decision.py and docs/BLK-089_rtm-authority-approval-decision-capture.md; approval decision package RTM-GENERATION-APPROVAL-DECISION-089-001 records RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED and reserves RUN-BLK-SYSTEM-088-RTM-GENERATION-001 for one future local pilot. It did not generate RTM; no drift rejection, no protected-body reads, no external ledger mutation, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-090 exact local RTM generation pilot",
        "state": "exact_local_rtm_generation_pilot_complete",
        "maturity": "L1_EXACT_LOCAL_RTM_GENERATION_PILOT",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-088", "BLK-089", "BLK-090"],
        "authority_cutline": "BLK-090 completed python/exact_local_rtm_generation_pilot.py and docs/BLK-090_exact-local-rtm-generation-pilot.md; execution package RTM-GENERATION-PILOT-EXECUTION-090-001 consumed RUN-BLK-SYSTEM-088-RTM-GENERATION-001 and produced PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE. No drift rejection, no drift decision, no protected-body reads, no external ledger mutation, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-091 RTM drift-review request gate",
        "state": "rtm_drift_review_request_complete",
        "maturity": "L0_L1_RTM_DRIFT_REVIEW_REQUEST_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-089", "BLK-090", "BLK-091"],
        "authority_cutline": "BLK-091 completed the BLK-091 Python request fixture and BLK-091 doctrine doc; request package 091-001 records DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED plus historical as-of-BLK-091 marker EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED. BLK-SYSTEM-093 later captured exact approval and BLK-SYSTEM-095 later consumed the exact local run ID locally. It grants no reusable/runtime RTM drift-rejection grant, no authoritative drift decision, no protected-body reads or hashing, no active-vault hash comparison, no external ledger mutation, no target-repo scan or mutation, no BLK-test/Codex/BLK-pipe runtime grant, no tooling grant, and no sandbox claim.",
    },
    {
        "surface": "BLK-092 post-091 roadmap/current-state reconciliation",
        "state": "post091_roadmap_current_state_reconciliation_l0_l1_complete",
        "maturity": "L0_L1_POST091_RECONCILIATION_DOCTRINE_GATE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-089", "BLK-090", "BLK-091", "BLK-092"],
        "authority_cutline": "BLK-092 completed docs/BLK-092_post-091-roadmap-current-state-reconciliation.md and refreshed BLK-077/BLK-079 after the 089/090/091 ladder. It is reconciliation-only: it does not capture drift-review approval, does not capture RTM drift-rejection approval, does not execute drift review, does not execute RTM drift rejection, no protected-body reads or hashing, no active-vault hash comparison, no external ledger mutation, no target-repo scan or mutation, no source/Git mutation, no BEB dispatch or BEO closeout execution, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-093 RTM drift-rejection approval decision capture",
        "state": "rtm_drift_rejection_approval_decision_captured_l0_l1",
        "maturity": "L0_L1_RTM_DRIFT_REJECTION_APPROVAL_DECISION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-091", "BLK-092", "BLK-093"],
        "authority_cutline": "BLK-093 completed python/rtm_drift_rejection_approval_decision.py and docs/BLK-093_rtm-drift-rejection-approval-decision-capture.md; package RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001 records approval-decision evidence for one future local execution sprint only. It does not execute RTM drift rejection, no drift decision, no protected-body reads or hashing, no active-vault hash comparison, no external ledger mutation, no target-repo scan or mutation, no source/Git mutation, no BEB dispatch or BEO closeout execution, no BLK-test/Codex/BLK-pipe runtime grant, no tooling or sandbox claim.",
    },
    {
        "surface": "BLK-094 post-093 roadmap / RTM-ladder alignment",
        "state": "post093_roadmap_rtm_ladder_alignment_l0_l1_complete",
        "maturity": "L0_L1_POST093_ALIGNMENT_DOCTRINE_GATE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-087", "BLK-088", "BLK-089", "BLK-090", "BLK-091", "BLK-092", "BLK-093", "BLK-094"],
        "authority_cutline": "BLK-094 records LOCAL_NON_AUTHORITATIVE_RTM_PILOT_LADDER_NOT_RUNTIME_BLK_LINK_CLOSURE and aligns the local BEO/RTM pilot ladder with BLK-001: actual authoritative BEO publication prerequisites remain required for real runtime blk-link trace closure. BLK-094 itself did not execute RTM drift rejection; BLK-SYSTEM-095 later consumed the exact local run ID, and future authority rungs should be independently auditable. It grants no reusable/runtime RTM drift-rejection grant, no authoritative drift decision, no protected-body reads or hashing, no active-vault comparison, no external ledger mutation, no external BEO publication, no signer/storage/rollback effects, no target/source/Git mutation, no BEB dispatch or BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no tooling grant, and no production isolation claim.",
    },
    {
        "surface": "BLK-095 exact local RTM drift-rejection execution",
        "state": "exact_local_rtm_drift_rejection_execution_complete",
        "maturity": "L1_EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-091", "BLK-093", "BLK-094", "BLK-095"],
        "authority_cutline": "BLK-095 completed python/exact_local_rtm_drift_rejection_execution.py and docs/BLK-095_exact-local-rtm-drift-rejection-execution.md; package RTM-DRIFT-REJECTION-EXECUTION-095-001 consumed RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001 and produced PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE as local-only evidence. No reusable/runtime RTM drift-rejection grant, no authoritative drift decision, no runtime blk-link trace closure, no protected-body reads or hashing, no active-vault hash comparison, no external ledger mutation, no external BEO publication, no signer/storage/rollback effects, no target/source/Git mutation, no BEB dispatch or BEO closeout execution, no BLK-pipe/BLK-test/Codex runtime, no tooling grant, and no production isolation claim.",
    },
    {
        "surface": "BLK-096 post-095 local RTM ladder reconciliation",
        "state": "post095_local_rtm_ladder_reconciliation_l0_l1_complete",
        "maturity": "L0_L1_POST095_RECONCILIATION_DOCTRINE_GATE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-095", "BLK-096"],
        "authority_cutline": "BLK-096 records BLK_SYSTEM_096_POST_095_LOCAL_RTM_LADDER_RECONCILED and LOCAL_RTM_DRIFT_REJECTION_EVIDENCE_CONSUMED_NOT_AUTHORITY after BLK-095 consumed the local run ID. NEXT_FRONTIER_REQUIRES_EXPLICIT_OPERATOR_DECISION_AFTER_LOCAL_LADDER. It grants no runtime blk-link trace closure, no runtime RTM generation, no runtime PUBLISHED BEO output, no external authoritative publication, no signer/storage/rollback side effects, no authoritative drift decision, no active-vault hash comparison, no protected-body reads or hashing, no external ledger mutation, no target/source/Git mutation, no BEB/BEO execution, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-097 bounded BLK-test evidence refresh",
        "state": "bounded_blk_test_evidence_refresh_complete",
        "maturity": "L4_EXACT_EVIDENCE_ONLY_BLK_TEST_REFRESH",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-097"],
        "authority_cutline": "BLK-097 completed python/blk_test_kuronode_workspace_bounded_evidence_refresh.py and docs/BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md; one exact evidence-only BLK-test refresh consumed APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001 and RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001 for /home/dad/code/Kuronode-v1 at aebea51bed911c781a537d84d38b2dcb838b1368, producing BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY. It grants no production BLK-test MCP, no source/Git mutation, no BEO publication, no RTM generation, no coverage truth, no protected-body reads, no public ledger mutation, no signer/storage/rollback effects, no BLK-pipe/Codex runtime, no package/network/model/browser/cyber tooling, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-098 BEO publication prerequisite request after evidence refresh",
        "state": "beo_publication_prerequisite_request_after_evidence_refresh_l0_l1_complete",
        "maturity": "L0_L1_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-087", "BLK-097", "BLK-098"],
        "authority_cutline": "BLK-098 completed python/beo_publication_prerequisite_request_after_evidence_refresh.py and docs/BLK-098_beo-publication-prerequisite-request-after-evidence-refresh.md; package BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001 records BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED by binding BLK-SYSTEM-097 evidence sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580 and BLK-SYSTEM-087 local pilot package sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e for future external BEO publication decision only. BLK-SYSTEM-099 later captured the external BEO publication approval decision; BLK-098 itself granted no external BEO publication, no runtime PUBLISHED BEO output, no live approval capture, no signer/storage/ledger/rollback effects, no runtime RTM generation, no RTM drift rejection, no active-vault hash comparison, no protected-body reads, no target/source/Git mutation, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-099 external BEO publication approval decision capture",
        "state": "external_beo_publication_approval_decision_captured_l0_l1",
        "maturity": "L0_L1_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-098", "BLK-099"],
        "authority_cutline": "BLK-099 completed python/beo_external_publication_approval_decision.py and docs/BLK-099_external-beo-publication-approval-decision.md; package BEO-PUBLICATION-APPROVAL-DECISION-099-001 records EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED for BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001 at sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041. It captured approval for the separately scoped BLK-SYSTEM-100 external BEO publication execution sprint; BLK-SYSTEM-100 later consumed the reserved run ID. BLK-099 itself granted no signer/storage/ledger/rollback effects, no runtime RTM generation, no RTM drift rejection, no active-vault hash comparison, no protected-body reads, no target/source/Git mutation, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-100 external BEO publication execution",
        "state": "external_beo_publication_execution_record_complete",
        "maturity": "L2_EXACT_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-098", "BLK-099", "BLK-100"],
        "authority_cutline": "BLK-100 completed python/beo_external_publication_execution.py and docs/BLK-100_external-beo-publication-execution.md; package BEO-PUBLICATION-EXECUTION-100-001 records EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY, emits PUBLISHED_EXTERNAL_BEO_RECORD for BEO-054-001, consumes RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001 with run ID consumed once, and produces execution package hash sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d. It grants no run-ID reuse, no signer/storage/ledger/rollback effects, no runtime RTM generation, no RTM drift rejection, no active-vault hash comparison, no protected-body reads, no target/source/Git mutation, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-101 RTM trace-closure authority request",
        "state": "rtm_trace_closure_authority_request_after_external_beo_l0_l1_complete",
        "maturity": "L0_L1_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_REVIEW_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-100", "BLK-101"],
        "authority_cutline": "BLK-101 completed python/rtm_trace_closure_authority_request_after_external_beo.py and docs/BLK-101_rtm-trace-closure-authority-request-after-external-beo.md; package RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001 records RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED and hash sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde. It grants no approval capture, no trace-closure execution, no RTM generation, no drift rejection, no active-vault hash comparison, no protected-body reads, no public ledger mutation, no target/source/Git mutation, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-102 RTM trace-closure approval decision capture",
        "state": "rtm_trace_closure_approval_decision_captured_l0_l1",
        "maturity": "L0_L1_RTM_TRACE_CLOSURE_APPROVAL_DECISION",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-101", "BLK-102"],
        "authority_cutline": "BLK-102 completed python/rtm_trace_closure_approval_decision.py and docs/BLK-102_rtm-trace-closure-approval-decision-capture.md; package RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001 records RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK101_REQUEST_NOT_EXECUTED and reserves RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001 with hash sha256:9211e14961b8c0f380812372d2b2a1ae091daf17709af375985f94015af0fecb. It grants no execution in that sprint, no RTM generation, no drift rejection, no active-vault hash comparison, no protected-body reads, no public ledger mutation, no target/source/Git mutation, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-103 exact local RTM trace-closure execution",
        "state": "exact_local_rtm_trace_closure_execution_complete",
        "maturity": "L1_EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-101", "BLK-102", "BLK-103"],
        "authority_cutline": "BLK-103 completed python/exact_local_rtm_trace_closure_execution.py and docs/BLK-103_exact-local-rtm-trace-closure-execution.md; package RTM-TRACE-CLOSURE-EXECUTION-103-001 records LOCAL_RTM_TRACE_CLOSURE_EXECUTED_FOR_EXACT_BLK102_APPROVAL and PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE, consumes RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001 once, and produces execution package hash sha256:3aba65a44d221cba04a80cb8d1342026a095c699d5c58fe3daf5a34886ae820a plus trace-closure record hash sha256:f58d7c1d370d136c94364076339728c08c2cded30e44866fd48d7f93c0eb2d2c. It grants no reusable or production blk-link authority, no RTM drift rejection, no authoritative drift decision, no active-vault hash comparison, no protected-body reads, no public ledger mutation, no target/source/Git mutation, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-104 post-103 roadmap/current-state reconciliation",
        "state": "post103_roadmap_current_state_reconciliation_l0_l1_complete",
        "maturity": "L0_L1_POST103_RECONCILIATION_DOCTRINE_GATE",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-100", "BLK-103", "BLK-104"],
        "authority_cutline": "BLK-104 records BLK_SYSTEM_104_POST_103_ROADMAP_CURRENT_STATE_RECONCILED and NEXT_SAFE_IMPLEMENTATION_FRONTIER_GO_PROTECTED_BODY_NO_READ_REMEDIATION as priority guidance only after reconciling BLK-100 record-only publication and BLK-103 local trace closure. It grants no BLK-pipe runtime execution, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no protected-body reads, no target/source/Git mutation, no runtime/tooling, and no production isolation authority.",
    },
    {
        "surface": "BLK-115 production-hardening reconciliation gate",
        "state": "post103_pipe_hardening_bridge_l0_l1_complete",
        "maturity": "L0_L1_POST103_PIPE_HARDENING_RECONCILIATION_GATE",
        "governing_docs": ["BLK-004", "BLK-077", "BLK-079", "BLK-112", "BLK-113", "BLK-114", "BLK-115"],
        "authority_cutline": "BLK_PIPE_PRODUCTION_HARDENING_BRIDGE_112_115_COMPLETE after structured validation profile argv hardening, validation trust-boundary capability policy, and report/evidence hardening. NEXT_FRONTIER_BLK_REQ_LEGISLATIVE_GATEWAY_PLANNING_NOT_EXECUTION_AUTHORITY. It grants no BLK-pipe runtime dispatch, no target/source/Git mutation, no BLK-test runtime, no BEO publication, no RTM generation or drift rejection, no active-vault hash comparison, no protected-body reads, no package/network/model/browser/cyber tooling, no signer/storage/ledger/rollback behavior, and no production isolation claim.",
    },
    {
        "surface": "BLK-058 Kuronode TypeScript tactical profile source",
        "state": "target_profile_source_not_dispatch_authority",
        "maturity": "L0_LAYER_C_PROFILE_SOURCE_ONLY",
        "governing_docs": ["BLK-058", "BLK-077", "BLK-078"],
        "authority_cutline": "BLK-058 is a Layer C target-profile source for future approved Kuronode TypeScript work only; no Kuronode mutation, live scan, tooling execution, dispatch, BLK-test, BEO, or RTM authority is granted.",
    },
)


def build_current_state_authority_index(surfaces=None):
    record = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-077",
        "maturity": MATURITY,
        "surfaces": deepcopy(list(DEFAULT_SURFACES if surfaces is None else surfaces)),
        "runtime_authority_granted": False,
        "live_codex_execution_authorized": False,
        "blk_pipe_dispatch_authorized": False,
        "production_blk_test_mcp_authorized": False,
        "authoritative_beo_publication_authorized": False,
        "runtime_rtm_generation_authorized": False,
        "rtm_drift_rejection_authorized": False,
        "protected_blk_req_body_reads_authorized": False,
        "network_model_cyber_browser_tooling_authorized": False,
        "package_manager_authorized": False,
        "production_isolation_claimed": False,
        "evaluation": READY,
        "validation_errors": [],
    }
    return record


def validate_current_state_authority_index(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    expected_scalars = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-077",
        "maturity": MATURITY,
    }
    unknown_top_keys = sorted(set(record) - TOP_LEVEL_KEYS)
    for key in unknown_top_keys:
        errors.append(f"unsupported top-level key {key!r}")
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
        unknown_surface_keys = sorted(set(surface) - SURFACE_KEYS)
        for key in unknown_surface_keys:
            errors.append(f"surface {name!r} has unsupported key {key!r}")
        names.append(name)
        state = surface.get("state")
        maturity = surface.get("maturity")
        if state not in ALLOWED_STATES:
            errors.append(f"surface {name!r} has unsupported state {state!r}")
        if maturity not in ALLOWED_MATURITIES:
            errors.append(f"surface {name!r} has unsupported maturity {maturity!r}")
        governing_docs = surface.get("governing_docs")
        if not isinstance(governing_docs, list) or not governing_docs:
            errors.append(f"surface {name!r} must list governing docs")
        else:
            for doc in governing_docs:
                if not _is_blk_doc_id(doc):
                    errors.append(f"surface {name!r} has invalid governing doc {doc!r}")
        cutline = surface.get("authority_cutline")
        if not isinstance(cutline, str) or not cutline:
            errors.append(f"surface {name!r} must define an authority cutline")

    if set(names) != set(EXPECTED_SURFACES):
        errors.append(f"surface set mismatch: {names!r}")
    if len(names) != len(set(names)):
        errors.append("surfaces must be unique")

    errors.extend(_forbidden_wording_errors(record))
    return errors


def evaluate_current_state_authority_index(record):
    evaluated = deepcopy(record)
    errors = validate_current_state_authority_index(record)
    evaluated["validation_errors"] = errors
    evaluated["evaluation"] = BLOCKED if errors else READY
    for flag in DENIED_FLAGS:
        evaluated[flag] = False
    return evaluated


def _is_blk_doc_id(value):
    if not isinstance(value, str):
        return False
    if not value.startswith("BLK-"):
        return False
    suffix = value.removeprefix("BLK-")
    return len(suffix) == 3 and suffix.isdigit()


def _forbidden_wording_errors(value, path="record"):
    errors = []
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).lower()
            key_path = f"{path}.{key}"
            if path != "record" and normalized_key in DENIED_FLAGS:
                errors.append(f"forbidden authority wording at {key_path}: {normalized_key}")
            if normalized_key in GENERIC_FORBIDDEN_AUTHORITY_KEYS:
                errors.append(f"forbidden authority wording at {key_path}: {normalized_key}")
            if path != "record":
                errors.extend(_scan_string_forbidden(str(key), key_path))
            errors.extend(_forbidden_wording_errors(nested, key_path))
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_wording_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        errors.extend(_scan_string_forbidden(value, path))
    return errors


def _scan_string_forbidden(text, path):
    findings = []
    for candidate in _decoded_variants(str(text)):
        normalized = _normalize_authority_text(candidate)
        compact = _compact_authority_text(candidate)
        for compact_token in FORBIDDEN_AUTHORITY_COMPACT_WORDING:
            safe_compact = _strip_safe_compact_denials(compact, compact_token)
            if compact_token in safe_compact:
                findings.append(f"forbidden authority wording at {path}: {compact_token}")
        for token in FORBIDDEN_AUTHORITY_WORDING + FORBIDDEN_AUTHORITY_VALUE_WORDING:
            normalized_token = _normalize_authority_text(token)
            safe_normalized = _strip_safe_normalized_denials(normalized, normalized_token)
            if normalized_token in safe_normalized:
                findings.append(f"forbidden authority wording at {path}: {token}")
    return _unique(findings)


def _strip_safe_normalized_denials(text, token):
    safe = text
    for prefix in ("no", "not"):
        safe = safe.replace(f"{prefix} {token}", "")
    return safe


def _strip_safe_compact_denials(text, token):
    safe = text
    for prefix in ("no", "not"):
        safe = safe.replace(f"{prefix}{token}", "")
    return safe


def _normalize_authority_text(text):
    chars = []
    previous_space = False
    for char in str(text).lower():
        if char.isalnum():
            chars.append(char)
            previous_space = False
        elif not previous_space:
            chars.append(" ")
            previous_space = True
    return " ".join("".join(chars).split())


def _compact_authority_text(text):
    return "".join(char for char in str(text).casefold() if char.isalnum())


def _decoded_variants(text):
    variants = [text]
    current = text
    for _ in range(5):
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _percent_decode_once(text):
    out = []
    index = 0
    hexdigits = "0123456789abcdefABCDEF"
    while index < len(text):
        if (
            text[index] == "%"
            and index + 2 < len(text)
            and text[index + 1] in hexdigits
            and text[index + 2] in hexdigits
        ):
            out.append(chr(int(text[index + 1 : index + 3], 16)))
            index += 3
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def _unique(items):
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items
