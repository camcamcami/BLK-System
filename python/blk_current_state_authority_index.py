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
    "draft_and_fixture_only",
    "offline_fixture_only",
    "doctrine_only_profile_architecture",
    "tactical_profile_registry_l0_l1_fixture_complete",
    "target_repo_governance_l0_l1_fixture_complete",
    "blk058_mechanical_enforcement_l0_l1_fixture_complete",
    "beo_publication_decision_package_l0_l1_review_fixture_complete",
    "post083_frontier_selection_l0_l1_fixture_complete",
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
    "FIXTURE_OFFLINE_LOCAL_EVIDENCE_ONLY",
    "L0_ARCHITECTURE_DOCTRINE_ONLY",
    "L0_L1_PROFILE_REGISTRY_FIXTURE_DOCTRINE",
    "L0_L1_TARGET_REPO_GOVERNANCE_FIXTURE_DOCTRINE",
    "L0_L1_BLK058_MECHANICAL_ENFORCEMENT_FIXTURE",
    "L0_L1_BEO_PUBLICATION_DECISION_PACKAGE_REVIEW_FIXTURE",
    "L0_L1_POST083_FRONTIER_SELECTION_FIXTURE",
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
    "package manager tooling authority",
    "package manager tooling is authorized",
    "production sandbox enforced",
    "production sandbox is enforced",
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
    "packagemanagerauthorized",
    "networkmodelcyberbrowsertoolingauthorized",
    "networkmodelcyberbrowsertoolingisauthorized",
    "productionsandboxisenforced",
    "productionisolationclaimed",
)

DEFAULT_SURFACES = (
    {
        "surface": "BLK-req legislative gateway",
        "state": "doctrine_and_fixture_boundary",
        "maturity": "L0_L1_DOCTRINE_FIXTURE",
        "governing_docs": ["BLK-002", "BLK-005", "BLK-006", "BLK-077"],
        "authority_cutline": "Protected bodies remain isolated. No tactical, BLK-test, BEO, RTM, Codex, health-check, or fixture helper may read, copy, parse, hash, summarize, scan, or mutate protected BLK-req bodies.",
    },
    {
        "surface": "BLK-pipe blast shield",
        "state": "local_guarded_enforcement",
        "maturity": "LOCAL_GUARDED_ENFORCEMENT_NOT_BROAD_AUTONOMY",
        "governing_docs": ["BLK-004", "BLK-077"],
        "authority_cutline": "BLK-pipe remains final mutation enforcement authority. Less-trusted or autonomous boundaries must not inherit arbitrary validation shell or broad file authority.",
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
        "state": "draft_and_fixture_only",
        "maturity": "L0_L1_DOCTRINE_FIXTURE",
        "governing_docs": ["BLK-014", "BLK-016", "BLK-021", "BLK-022", "BLK-026", "BLK-028", "BLK-077"],
        "authority_cutline": "Authoritative publication remains disabled. No signer, immutable storage, public ledger, rollback, revocation, supersession, or runtime PUBLISHED output.",
    },
    {
        "surface": "RTM / blk-link",
        "state": "offline_fixture_only",
        "maturity": "FIXTURE_OFFLINE_LOCAL_EVIDENCE_ONLY",
        "governing_docs": ["BLK-023", "BLK-027", "BLK-029", "BLK-030", "BLK-033", "BLK-077"],
        "authority_cutline": "Runtime RTM generation and drift rejection remain disabled. No protected-body reads and no public ledger mutation.",
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
            if compact_token in compact:
                findings.append(f"forbidden authority wording at {path}: {compact_token}")
        for token in FORBIDDEN_AUTHORITY_WORDING + FORBIDDEN_AUTHORITY_VALUE_WORDING:
            normalized_token = _normalize_authority_text(token)
            if normalized_token == "execution authorized":
                without_negated = normalized.replace("not execution authorized", "")
                if "execution authorized" not in without_negated:
                    continue
            if normalized_token in normalized:
                findings.append(f"forbidden authority wording at {path}: {token}")
    return _unique(findings)


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
