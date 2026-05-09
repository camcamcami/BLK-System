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
)

ALLOWED_STATES = {
    "doctrine_and_fixture_boundary",
    "local_guarded_enforcement",
    "fail_fast_convenience_layer",
    "repository_owned_local_profiles",
    "disabled_gated_evidence_only",
    "advisory_local_pilot",
    "review_ready_not_execution_authorized",
    "draft_and_fixture_only",
    "offline_fixture_only",
}

ALLOWED_MATURITIES = {
    "L0_L1_DOCTRINE_FIXTURE",
    "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
    "L1_L2_STYLE_PREFLIGHT_ONLY",
    "MATURE_LOCAL_PROFILE_SUPPORT",
    "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
    "ADVISORY_PILOT_ONLY",
    "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
    "FIXTURE_OFFLINE_LOCAL_EVIDENCE_ONLY",
}

FORBIDDEN_AUTHORITY_WORDING = (
    "approved_for_live_execution",
    "authoritative beo publication approved",
    "live_execution_enabled",
    "l5_production_authority",
    "rtm_drift_rejection_authorized_by_index",
    "protected_body_read_authorized_by_index",
    "production_sandbox_enforced_by_index",
    "network_tooling_authorized_by_index",
    "package_manager_authorized_by_index",
)

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

DEFAULT_SURFACES = (
    {
        "surface": "BLK-req legislative gateway",
        "state": "doctrine_and_fixture_boundary",
        "maturity": "L0_L1_DOCTRINE_FIXTURE",
        "governing_docs": ["BLK-002", "BLK-005", "BLK-006", "BLK-045"],
        "authority_cutline": "Protected bodies remain isolated. No tactical, BLK-test, BEO, RTM, Codex, health-check, or fixture helper may read, copy, parse, hash, summarize, scan, or mutate protected BLK-req bodies.",
    },
    {
        "surface": "BLK-pipe blast shield",
        "state": "local_guarded_enforcement",
        "maturity": "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
        "governing_docs": ["BLK-004", "BLK-045"],
        "authority_cutline": "BLK-pipe remains final mutation enforcement authority. Less-trusted or autonomous boundaries must not inherit arbitrary validation shell or broad file authority.",
    },
    {
        "surface": "Python adapter layer",
        "state": "fail_fast_convenience_layer",
        "maturity": "L1_L2_STYLE_PREFLIGHT_ONLY",
        "governing_docs": ["BLK-004", "BLK-045"],
        "authority_cutline": "Adapter checks reduce operator mistakes but do not replace Go enforcement and do not create sandbox, network, or host-secret-isolation claims.",
    },
    {
        "surface": "Validation profiles",
        "state": "repository_owned_local_profiles",
        "maturity": "MATURE_LOCAL_PROFILE_SUPPORT",
        "governing_docs": ["BLK-004", "BLK-045"],
        "authority_cutline": "Profiles constrain validation commands but do not grant package-manager, network, secret-reading, BLK-test, BEO, RTM, or arbitrary shell authority.",
    },
    {
        "surface": "BLK-test",
        "state": "disabled_gated_evidence_only",
        "maturity": "DISABLED_DESIGN_WITH_HISTORICAL_L3_EXCEPTION",
        "governing_docs": ["BLK-017", "BLK-018", "BLK-019", "BLK-020", "BLK-045"],
        "authority_cutline": "BLK-test returns evidence only. Production MCP remains disabled. No source mutation, publication, RTM generation, arbitrary shell, or protected body reads.",
    },
    {
        "surface": "Operator health / observability",
        "state": "advisory_local_pilot",
        "maturity": "ADVISORY_PILOT_ONLY",
        "governing_docs": ["BLK-031", "BLK-032", "BLK-033", "BLK-034", "BLK-035", "BLK-036", "BLK-037", "BLK-038", "BLK-039", "BLK-045"],
        "authority_cutline": "PASS is advisory only. Health checks do not become BLK-test verification, execution approval, or production sandbox evidence.",
    },
    {
        "surface": "Codex live-dispatch ladder",
        "state": "review_ready_not_execution_authorized",
        "maturity": "L0_L1_L2_STYLE_DISABLED_NO_L3_SMOKE",
        "governing_docs": ["BLK-040", "BLK-041", "BLK-042", "BLK-043", "BLK-044", "BLK-045"],
        "authority_cutline": "Review-ready and design-ready evidence is not execution-authorized. No live Codex subprocess, BLK-pipe dispatch from a Codex adapter, source mutation, package/network/model/cyber/browser tooling, or production isolation authority.",
    },
    {
        "surface": "BEO publication path",
        "state": "draft_and_fixture_only",
        "maturity": "L0_L1_DOCTRINE_FIXTURE",
        "governing_docs": ["BLK-014", "BLK-016", "BLK-021", "BLK-022", "BLK-026", "BLK-028", "BLK-045"],
        "authority_cutline": "Authoritative publication remains disabled. No signer, immutable storage, public ledger, rollback, revocation, supersession, or runtime PUBLISHED output.",
    },
    {
        "surface": "RTM / blk-link",
        "state": "offline_fixture_only",
        "maturity": "FIXTURE_OFFLINE_LOCAL_EVIDENCE_ONLY",
        "governing_docs": ["BLK-023", "BLK-027", "BLK-029", "BLK-030", "BLK-033", "BLK-045"],
        "authority_cutline": "Runtime RTM generation and drift rejection remain disabled. No protected-body reads and no public ledger mutation.",
    },
)


def build_current_state_authority_index(surfaces=None):
    record = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-045",
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
    }
    return record


def validate_current_state_authority_index(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    expected_scalars = {
        "index_id": INDEX_ID,
        "index_status": INDEX_STATUS,
        "roadmap_source": "BLK-045",
        "maturity": MATURITY,
    }
    for key, expected in expected_scalars.items():
        if record.get(key) != expected:
            errors.append(f"{key} must be {expected!r}")

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
        state = surface.get("state")
        maturity = surface.get("maturity")
        if state not in ALLOWED_STATES:
            errors.append(f"surface {name!r} has unsupported state {state!r}")
        if maturity not in ALLOWED_MATURITIES:
            errors.append(f"surface {name!r} has unsupported maturity {maturity!r}")
        governing_docs = surface.get("governing_docs")
        if not isinstance(governing_docs, list) or not governing_docs:
            errors.append(f"surface {name!r} must list governing docs")
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
    evaluated["runtime_authority_granted"] = False
    return evaluated


def _forbidden_wording_errors(value, path="record"):
    errors = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            errors.extend(_scan_string_forbidden(str(key), key_path))
            errors.extend(_forbidden_wording_errors(nested, key_path))
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_wording_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        errors.extend(_scan_string_forbidden(value, path))
    return errors


def _scan_string_forbidden(text, path):
    normalized = text.lower()
    return [
        f"forbidden authority wording at {path}: {token}"
        for token in FORBIDDEN_AUTHORITY_WORDING
        if token in normalized
    ]
