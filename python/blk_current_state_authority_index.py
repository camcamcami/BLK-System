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
    "BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY",
    "BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED",
    "BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED",
    "NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_NOT_GRANTED",
)

STALE_ACTIVE_DOC_MARKERS = (
    "NEXT_FRONTIER_HARDENING_ONLY_COMPLETE_AUTHORITY_NOT_GRANTED",
    "NEXT_FRONTIER_FURTHER_HARDENING_OR_AUTHORITY_REQUEST_NOT_GRANTED",
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
    "local_guarded_enforcement",
    "fail_fast_convenience_layer",
    "repository_owned_local_profiles",
    "disabled_gated_evidence_only",
    "advisory_local_pilot",
    "review_ready_not_execution_authorized",
    "authoritative_beo_publication_finality_152_complete",
    "production_blk_link_rtm_trace_closure_authority_request_165_ready",
}

ALLOWED_MATURITIES = {
    "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
    "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
    "L1_L2_STYLE_PREFLIGHT_ONLY",
    "MATURE_LOCAL_PROFILE_SUPPORT",
    "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
    "ADVISORY_PILOT_ONLY",
    "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
    "L3_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_COMPLETE",
    "L2_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_REQUEST_READY_NOT_AUTHORITY",
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
        "state": "blk_req_metadata_bound_publication_request_127_complete",
        "maturity": "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-116", "BLK-120"],
        "authority_cutline": (
            "Protected bodies remain isolated. BLK-122..127 established exact-ID retrieval, staged revision promotion, "
            "metadata-only BEB/BEO handoff, and a review-only publication prerequisite request. This does not grant "
            "protected-body reads, drift rejection, BEO closeout execution, signer/storage/ledger behavior, or target/source/Git mutation."
        ),
    },
    {
        "surface": "BLK-pipe blast shield",
        "state": "local_guarded_enforcement",
        "maturity": "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
        "governing_docs": ["BLK-003", "BLK-004", "BLK-077", "BLK-079", "BLK-115"],
        "authority_cutline": "Local guarded enforcement remains bounded by explicit validation profiles. No broad dispatch, target/source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation claim is granted by the index.",
    },
    {
        "surface": "Python adapter layer",
        "state": "fail_fast_convenience_layer",
        "maturity": "L1_L2_STYLE_PREFLIGHT_ONLY",
        "governing_docs": ["BLK-016", "BLK-021", "BLK-077", "BLK-079"],
        "authority_cutline": "Adapters remain fail-fast local convenience surfaces. They may package deterministic evidence but cannot dispatch BLK-pipe, execute Codex, mutate source, perform BEO publication, generate RTM, or read protected bodies without separate authority.",
    },
    {
        "surface": "Validation profiles",
        "state": "repository_owned_local_profiles",
        "maturity": "MATURE_LOCAL_PROFILE_SUPPORT",
        "governing_docs": ["BLK-077", "BLK-079", "BLK-112", "BLK-113", "BLK-114", "BLK-115"],
        "authority_cutline": "Repository-owned validation profiles use structured argv for local evidence. Capability labels and PASS results are diagnostic only and do not grant runtime, publication, RTM, mutation, tooling, or isolation authority.",
    },
    {
        "surface": "BLK-test",
        "state": "disabled_gated_evidence_only",
        "maturity": "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
        "governing_docs": ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-077", "BLK-079"],
        "authority_cutline": "BLK-test is a BLK-System functional module, not the BLK-System test suite. Production MCP remains disabled; evidence is evidence only and grants no source mutation, BEO publication, RTM, coverage, drift, tooling, or protected-body authority.",
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
        "state": "review_ready_not_execution_authorized",
        "maturity": "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
        "governing_docs": ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044", "BLK-077", "BLK-079"],
        "authority_cutline": "Codex dispatch remains review-ready, not execution-authorized. No live Codex subprocess, BLK-pipe dispatch, source mutation, package/network/model/browser/cyber tooling, or production-isolation claim is granted.",
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
        "state": "production_blk_link_rtm_trace_closure_authority_request_165_ready",
        "maturity": "L2_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_REQUEST_READY_NOT_AUTHORITY",
        "governing_docs": ["BLK-023", "BLK-077", "BLK-079", "BLK-140", "BLK-141", "BLK-142", "BLK-143", "BLK-144"],
        "authority_cutline": (
            "BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY binds "
            "BLK_SYSTEM_162_POST_TRACE_CLOSURE_REVIEW_COMPLETE via POST-METADATA-TRACE-CLOSURE-REVIEW-162-001 "
            "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9 plus "
            "BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED. "
            "BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED. "
            "NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_NOT_GRANTED. "
            "No approval capture, no run-ID reservation/consumption, no production `blk-link` execution, "
            "no reusable RTM generation, no drift rejection, no coverage truth, no protected-body access, "
            "no active-vault comparison, no BEO closeout execution, no target/source/Git mutation, and no signer/storage/ledger reuse."
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

    scan_candidate = {k: v for k, v in record.items() if k not in DENIED_FLAGS and k != "validation_errors"}
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
    return errors


def evaluate_current_state_authority_index(record=None):
    candidate = build_current_state_authority_index() if record is None else deepcopy(record)
    errors = validate_current_state_authority_index(candidate)
    candidate["evaluation"] = BLOCKED if errors else READY
    candidate["validation_errors"] = errors
    for flag in DENIED_FLAGS:
        candidate[flag] = False
    return candidate
