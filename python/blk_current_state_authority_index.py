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
    "authoritative_beo_publication_authorized",
    "runtime_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "protected_blk_req_body_reads_authorized",
    "network_model_cyber_browser_tooling_authorized",
    "package_manager_authorized",
    "production_isolation_claimed",
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
    "metadata_bound_rtm_generation_approval_execution_158_complete",
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
    "L2_BOUNDED_METADATA_RTM_GENERATION_RECORD_ONLY",
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
        "state": "metadata_bound_rtm_generation_approval_execution_158_complete",
        "maturity": "L2_BOUNDED_METADATA_RTM_GENERATION_RECORD_ONLY",
        "governing_docs": ["BLK-023", "BLK-077", "BLK-079", "BLK-140", "BLK-141", "BLK-142", "BLK-143", "BLK-144"],
        "authority_cutline": (
            "BLK_SYSTEM_158_METADATA_BOUND_RTM_GENERATION_APPROVAL_EXECUTION_COMPLETE pins exact approval + bounded record-only "
            "RTM generation via METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-001 "
            "sha256:ebb20362dde1e3a2e47ed7e40586c03b77b5176e20e7d17c8559c74ef1784cfe. "
            "NEXT_FRONTIER_POST_METADATA_BOUND_RTM_GENERATION_RECONCILIATION_NOT_GRANTED. It does not grant reusable production `blk-link`; "
            "no RTM generation beyond exact record, no drift rejection, no coverage truth, no protected-body access, "
            "no target/source/Git mutation, and no signer/storage/ledger reuse."
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


def evaluate_current_state_authority_index(record=None):
    candidate = build_current_state_authority_index() if record is None else deepcopy(record)
    errors = validate_current_state_authority_index(candidate)
    candidate["evaluation"] = BLOCKED if errors else READY
    candidate["validation_errors"] = errors
    for flag in DENIED_FLAGS:
        candidate[flag] = False
    return candidate
