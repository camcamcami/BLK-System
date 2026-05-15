from copy import deepcopy

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
    "external_beo_publication_execution_129_record_complete",
    "authority_ladder_hardening_145_complete",
}

ALLOWED_MATURITIES = {
    "L0_L1_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY",
    "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
    "L1_L2_STYLE_PREFLIGHT_ONLY",
    "MATURE_LOCAL_PROFILE_SUPPORT",
    "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
    "ADVISORY_PILOT_ONLY",
    "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
    "L2_EXACT_METADATA_BOUND_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
    "L0_L1_AUTHORITY_LADDER_HARDENING_ONLY",
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

GENERIC_FORBIDDEN_KEYS = {
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
    "is_authorized",
}

FORBIDDEN_VALUE_PHRASES = (
    "approved for runtime execution",
    "runtime execution approved",
    "runtime execution authorized",
    "live execution authorized",
    "live codex execution is authorized",
    "authoritative beo publication approved",
    "beo publication authorized",
    "publication authority granted",
    "approved for publication",
    "greenlit for production",
    "production blk-test mcp is authorized",
    "production blk test mcp is authorized",
    "rtm drift rejection is authorized",
    "protected blk req body reads authorized",
    "production sandbox is enforced",
    "exact-id retrieval authorized",
    "exact id retrieval authorized",
    "staged revision overwrite authorized",
    "public-authority ledger rollback authorized",
    "public authority ledger rollback authorized",
    "runtime_authority_granted",
)

FORBIDDEN_COMPACT_VALUE_TOKENS = {
    "approvedforliveexecution",
    "runtimeexecutionauthorized",
    "runtimeexecutionapproved",
    "liveexecutionauthorized",
    "livecodexexecutionisauthorized",
    "authoritativebeopublicationapproved",
    "beopublicationauthorized",
    "publicationauthoritygranted",
    "approvedforpublication",
    "greenlitforproduction",
    "productionblktestmcpisauthorized",
    "rtmdriftrejectionisauthorized",
    "protectedblkreqbodyreadsauthorized",
    "productionsandboxisenforced",
    "exactidretrievalauthorized",
    "stagedrevisionoverwriteisauthorized",
    "publicauthorityledgerrollbackisauthorized",
    "runtimeauthoritygranted",
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
        "authority_cutline": "Adapters remain fail-fast local convenience surfaces. They may package deterministic evidence but cannot dispatch BLK-pipe, execute Codex, mutate source, publish BEOs, generate RTM, or read protected bodies without separate authority.",
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
        "state": "external_beo_publication_execution_129_record_complete",
        "maturity": "L2_EXACT_METADATA_BOUND_EXTERNAL_BEO_PUBLICATION_EXECUTION_RECORD",
        "governing_docs": ["BLK-022", "BLK-077", "BLK-079", "BLK-127", "BLK-128", "BLK-129"],
        "authority_cutline": "BLK-129 is exact record-only external BEO publication evidence for the metadata-bound path. It is not reusable publication authority: no signer/storage/ledger, no rollback/revocation, no BEO closeout execution, no RTM generation, no drift rejection, and no protected-body access."
    },
    {
        "surface": "RTM / blk-link",
        "state": "authority_ladder_hardening_145_complete",
        "maturity": "L0_L1_AUTHORITY_LADDER_HARDENING_ONLY",
        "governing_docs": ["BLK-023", "BLK-077", "BLK-079", "BLK-140", "BLK-141", "BLK-142", "BLK-143", "BLK-144"],
        "authority_cutline": (
            "BLK_SYSTEM_145_AUTHORITY_LADDER_HARDENING_ONLY_COMPLETE pins hardening-only mode via "
            "AUTHORITY-LADDER-HARDENING-145-001 "
            "sha256:e7e5fd48217ca85ac0839897adefab0079701a333861b501c1cea1a318810103. "
            "AUTHORITY_LADDER_PAUSED_FOR_HARDENING_NO_NEW_AUTHORITY_GRANTED; "
            "NEXT_FRONTIER_AUTHORITY_LADDER_HARDENING_ONLY_NO_AUTHORITY_RUNG_SELECTED. It does not grant reusable production `blk-link`; "
            "no authority rung selected, no RTM execution, no drift rejection, no coverage truth, no protected-body access, no target/source/Git mutation, and no signer/storage/ledger behavior."
        ),
    },
)


def _compact(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def _scan_for_authority_laundering(value, path="record"):
    errors = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            key_compact = _compact(key_text)
            if key in DENIED_FLAGS or key in GENERIC_FORBIDDEN_KEYS:
                errors.append(f"{path}.{key_text} contains forbidden authority key")
            if key_compact in {_compact(item) for item in GENERIC_FORBIDDEN_KEYS}:
                errors.append(f"{path}.{key_text} contains forbidden authority key")
            if key_compact in FORBIDDEN_COMPACT_VALUE_TOKENS:
                errors.append(f"{path}.{key_text} contains forbidden authority wording")
            errors.extend(_scan_for_authority_laundering(nested, f"{path}.{key_text}"))
    elif isinstance(value, (list, tuple, set)):
        for index, nested in enumerate(value):
            errors.extend(_scan_for_authority_laundering(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        lowered = value.lower()
        compact = _compact(value)
        if lowered.strip() in {"approved", "authorized"}:
            errors.append(f"{path} contains forbidden authority wording {value!r}")
        for phrase in FORBIDDEN_VALUE_PHRASES:
            if phrase in lowered:
                errors.append(f"{path} contains forbidden authority wording {phrase!r}")
        for token in FORBIDDEN_COMPACT_VALUE_TOKENS:
            if token in compact:
                errors.append(f"{path} contains forbidden authority wording {token!r}")
    return errors


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
    errors.extend(_scan_for_authority_laundering(scan_candidate))
    return errors


def evaluate_current_state_authority_index(record=None):
    candidate = build_current_state_authority_index() if record is None else deepcopy(record)
    errors = validate_current_state_authority_index(candidate)
    candidate["evaluation"] = BLOCKED if errors else READY
    candidate["validation_errors"] = errors
    for flag in DENIED_FLAGS:
        candidate[flag] = False
    return candidate
