from copy import deepcopy
import re

REGISTRY_ID = "blk_system_tactical_profile_registry"
REGISTRY_STATUS = "TACTICAL_PROFILE_REGISTRY_L0_L1_FIXTURE_ONLY"
REGISTRY_READY = "TACTICAL_PROFILE_REGISTRY_READY_FOR_REVIEW_NOT_RUNTIME"
REGISTRY_BLOCKED = "TACTICAL_PROFILE_REGISTRY_BLOCKED"
SELECTION_STATUS = "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY"
SELECTION_READY = "TACTICAL_PROFILE_SELECTION_READY_FOR_REVIEW_NOT_RUNTIME"
SELECTION_BLOCKED = "TACTICAL_PROFILE_SELECTION_BLOCKED"
LAYER_B_STANDARD_ID = "blk-system-universal-tactical-output-safety"

LAYER_B_PRINCIPLE_IDS = (
    "simple_reviewable_control_flow",
    "bounded_iteration",
    "bounded_runtime_state",
    "explicit_lifecycle_management",
    "small_hostile_reviewable_units",
    "boundary_validation",
    "checked_results_and_postconditions",
    "minimal_mutable_scope",
    "no_dynamic_execution_laundering",
    "flat_validated_data_access",
    "zero_warning_intent_under_repository_owned_profiles",
    "no_authority_laundering",
)

DENIED_AUTHORITIES = (
    "NO_PROFILE_SELECTION_RUNTIME_AUTHORITY",
    "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_KURONODE_MUTATION_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
)

DENIED_FLAGS = (
    "profile_selection_runtime_authority_granted",
    "target_repo_scan_authorized",
    "target_repo_mutation_authorized",
    "live_codex_execution_authorized",
    "blk_pipe_execution_authorized",
    "production_blk_test_mcp_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "protected_body_reads_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

REGISTRY_KEYS = {
    "registry_id",
    "registry_status",
    "architecture_anchor",
    "layer_b_standard_id",
    "layer_b_principles",
    "target_profiles",
    "denied_authorities",
    "evaluation",
    "validation_errors",
    "target_repo_scan_authorized",
    "target_repo_mutation_authorized",
    "live_codex_execution_authorized",
    "blk_pipe_execution_authorized",
    "production_blk_test_mcp_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "protected_body_reads_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
}

PRINCIPLE_KEYS = {
    "id",
    "name",
    "summary",
    "source_doc",
    "layer",
}

PROFILE_KEYS = {
    "profile_id",
    "profile_source_doc",
    "profile_architecture_doc",
    "layer",
    "target_repo_identity",
    "applicable_paths",
    "excluded_paths",
    "language_runtime_stack",
    "profile_maturity",
    "layer_b_principles",
    "layer_c_overlays",
    "validation_profiles",
    "exception_policy",
    "hostile_review_checklist",
    "stop_conditions",
    "denied_authorities",
    "authority_cutline",
}

SELECTION_KEYS = {
    "selection_id",
    "selection_status",
    "selected_profile_id",
    "selected_profile_source_doc",
    "selected_profile_architecture_doc",
    "selection_maturity",
    "selected_by",
    "selection_summary",
    "applicable_paths",
    "excluded_paths",
    "validation_profiles",
    "layer_b_standard_id",
    "layer_b_principles",
    "layer_c_overlays",
    "denied_authorities",
    "evaluation",
    "validation_errors",
    *DENIED_FLAGS,
}

FORBIDDEN_NORMALIZED_MARKERS = (
    "approvedforliveexecution",
    "approvedforruntimeexecution",
    "runtimeexecutionapproved",
    "runtimeexecutionauthorized",
    "runtimepilotapproved",
    "livepilotallowed",
    "livetargetscanauthorized",
    "targetreposcanauthorized",
    "targetscanauthorized",
    "kuronodemutationisauthorized",
    "kuronodemutationauthorized",
    "targetrepomutationauthorized",
    "livecodexexecutionauthorized",
    "codexexecutionauthorized",
    "blkpipeexecutionauthorized",
    "productionblktestmcpauthorized",
    "productionblktestmcpisauthorized",
    "productionblktestmcpauthority",
    "authoritativebeopublication",
    "beopublicationauthorized",
    "beopublicationauthority",
    "rtmgeneration",
    "rtmgenerationauthorized",
    "rtmdriftrejectionauthorized",
    "protectedblkreqbodyreadsauthorized",
    "protectedblkreqbodyreadsareauthorized",
    "protectedbodyreadsauthorized",
    "packagemanagertoolingisauthorized",
    "packagemanagerauthorized",
    "networktoolingauthorized",
    "modelservicetoolingauthorized",
    "browsertoolingauthorized",
    "cybertoolingauthorized",
    "productionsandboxisenforced",
    "productionsandboxenforced",
    "hostisolationclaimed",
    "executionauthorized",
)

FORBIDDEN_KEY_MARKERS = tuple(_normalize_key for _normalize_key in DENIED_FLAGS) + (
    "authorization",
    "authority",
    "approved",
    "authorized",
    "livescanauthorized",
    "live_scan_authorized",
    "executionauthorized",
)

COMMAND_MARKERS = (
    " ",
    "/",
    "\\",
    "http:",
    "https:",
    "&&",
    "||",
    ";",
    "`",
    "$(",
)

LAYER_B_PRINCIPLES = (
    {
        "id": "simple_reviewable_control_flow",
        "name": "Simple, reviewable control flow",
        "summary": "Avoid hidden state transitions, callback mazes, and control-flow-by-exception.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "bounded_iteration",
        "name": "Bounded iteration",
        "summary": "Retries, traversals, polling, queue drains, and convergence loops require explicit limits.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "bounded_runtime_state",
        "name": "Bounded runtime state",
        "summary": "Caches, maps, arrays, queues, listener registries, logs, and pending-operation stores must be bounded.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "explicit_lifecycle_management",
        "name": "Explicit lifecycle management",
        "summary": "Resources created by tactical output require visible teardown paths where cleanup semantics exist.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "small_hostile_reviewable_units",
        "name": "Small hostile-reviewable units",
        "summary": "Authority-sensitive functions should be small enough for focused review with validation, transformation, side effects, and reporting separated where practical.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "boundary_validation",
        "name": "Boundary validation",
        "summary": "Externally supplied data, process-boundary data, persistence records, IPC messages, parser outputs, and worker messages must be structurally validated before use.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "checked_results_and_postconditions",
        "name": "Checked results and postconditions",
        "summary": "Meaningful return values, nullable/error-shaped outputs, promises, validation results, and critical postconditions must not be ignored.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "minimal_mutable_scope",
        "name": "Minimal mutable scope",
        "summary": "Prefer local immutable values and narrow mutation windows; avoid ambient mutable singletons used to bridge architectural gaps.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "no_dynamic_execution_laundering",
        "name": "No dynamic execution laundering",
        "summary": "Tactical code must not introduce generated executable strings, reflection-like dispatch, unvalidated dynamic imports, or equivalent dynamic execution without explicit exception authority.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "flat_validated_data_access",
        "name": "Flat, validated data access",
        "summary": "Nested or external structures must be normalized or validated before authority-sensitive use.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "zero_warning_intent_under_repository_owned_profiles",
        "name": "Zero-warning intent under repository-owned profiles",
        "summary": "Warnings are blocking evidence when a repository-owned validation profile defines them as blocking; autonomous boundaries must not replace profile-owned checks with arbitrary shell.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
    {
        "id": "no_authority_laundering",
        "name": "No authority laundering",
        "summary": "Tactical quality evidence remains constraint evidence only and never permits adjacent runtime frontiers.",
        "source_doc": "BLK-078",
        "layer": "Layer B",
    },
)

DEFAULT_TARGET_PROFILE = {
    "profile_id": "kuronode-typescript",
    "profile_source_doc": "BLK-058",
    "profile_architecture_doc": "BLK-078",
    "layer": "Layer C",
    "target_repo_identity": "Kuronode-v1",
    "applicable_paths": ["**/*.ts", "**/*.tsx"],
    "excluded_paths": ["node_modules/**", "dist/**", "build/**", "coverage/**", ".git/**"],
    "language_runtime_stack": ["TypeScript", "Electron", "React", "Zustand", "ELK.js", "JointJS", "tree-sitter SysML"],
    "profile_maturity": "L0_LAYER_C_SOURCE_ONLY",
    "layer_b_principles": list(LAYER_B_PRINCIPLE_IDS),
    "layer_c_overlays": [
        "electron_ipc_boundary",
        "zustand_renderer_state_ownership",
        "elk_geometry_authority",
        "jointjs_graph_adapter_quarantine",
        "tree_sitter_sysml_wasm_lifecycle",
        "kuronode_projected_node_circuit_breaker",
    ],
    "validation_profiles": [
        "kuronode-power-of-ten-static",
        "kuronode-typecheck-strict",
        "kuronode-eslint-zero-warning",
    ],
    "exception_policy": "Layer C exceptions require separate explicit approval and hostile review; profile registration alone grants no scan, mutation, dispatch, BLK-test, BEO, or RTM authority.",
    "hostile_review_checklist": [
        "Layer A authority boundaries preserved",
        "Layer B universal principles not weakened",
        "Kuronode-specific overlays not promoted to universal core",
        "validation profile names remain repository-owned metadata and not arbitrary shell",
    ],
    "stop_conditions": [
        "attempt to treat profile selection as target scan authority",
        "attempt to treat BLK-058 as Kuronode mutation authority",
        "attempt to replace repository-owned validation profile names with command strings",
        "attempt to infer BEO, RTM, BLK-test, Codex, or sandbox authority from profile compliance",
    ],
    "denied_authorities": list(DENIED_AUTHORITIES),
    "authority_cutline": "BLK-058 is registered as a Layer C source for future approved Kuronode TypeScript work only; profile registration grants no Kuronode mutation, target scan, dispatch, BLK-test, BEO, RTM, protected-body, tooling, or sandbox authority.",
}


def build_tactical_profile_registry():
    record = {
        "registry_id": REGISTRY_ID,
        "registry_status": REGISTRY_STATUS,
        "architecture_anchor": "BLK-078",
        "layer_b_standard_id": LAYER_B_STANDARD_ID,
        "layer_b_principles": deepcopy(list(LAYER_B_PRINCIPLES)),
        "target_profiles": [deepcopy(DEFAULT_TARGET_PROFILE)],
        "denied_authorities": list(DENIED_AUTHORITIES),
        "target_repo_scan_authorized": False,
        "target_repo_mutation_authorized": False,
        "live_codex_execution_authorized": False,
        "blk_pipe_execution_authorized": False,
        "production_blk_test_mcp_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "protected_body_reads_authorized": False,
        "package_network_model_browser_cyber_tooling_authorized": False,
        "production_isolation_claimed": False,
        "evaluation": REGISTRY_READY,
        "validation_errors": [],
    }
    return record


def build_profile_selection_record():
    record = {
        "selection_id": "blk_system_profile_selection_kuronode_typescript_review_only",
        "selection_status": SELECTION_STATUS,
        "selected_profile_id": "kuronode-typescript",
        "selected_profile_source_doc": "BLK-058",
        "selected_profile_architecture_doc": "BLK-078",
        "selection_maturity": "L0_L1_PLANNING_FIXTURE_ONLY",
        "selected_by": "BLK-SYSTEM-080 fixture only",
        "selection_summary": "Review-only profile selection metadata for future approved Kuronode TypeScript work; no runtime or target authority is granted.",
        "applicable_paths": ["**/*.ts", "**/*.tsx"],
        "excluded_paths": ["node_modules/**", "dist/**", "build/**", "coverage/**", ".git/**"],
        "validation_profiles": [
            "kuronode-power-of-ten-static",
            "kuronode-typecheck-strict",
            "kuronode-eslint-zero-warning",
        ],
        "layer_b_standard_id": LAYER_B_STANDARD_ID,
        "layer_b_principles": list(LAYER_B_PRINCIPLE_IDS),
        "layer_c_overlays": list(DEFAULT_TARGET_PROFILE["layer_c_overlays"]),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "profile_selection_runtime_authority_granted": False,
        "target_repo_scan_authorized": False,
        "target_repo_mutation_authorized": False,
        "live_codex_execution_authorized": False,
        "blk_pipe_execution_authorized": False,
        "production_blk_test_mcp_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "protected_body_reads_authorized": False,
        "package_network_model_browser_cyber_tooling_authorized": False,
        "production_isolation_claimed": False,
        "evaluation": SELECTION_READY,
        "validation_errors": [],
    }
    return record


def validate_tactical_profile_registry(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    _validate_closed_schema(record, REGISTRY_KEYS, "registry", errors)
    _expect_scalar(record, "registry_id", REGISTRY_ID, errors)
    _expect_scalar(record, "registry_status", REGISTRY_STATUS, errors)
    _expect_scalar(record, "architecture_anchor", "BLK-078", errors)
    _expect_scalar(record, "layer_b_standard_id", LAYER_B_STANDARD_ID, errors)
    _validate_denied_authorities(record.get("denied_authorities"), "registry.denied_authorities", errors)
    _validate_denied_flags(record, [flag for flag in DENIED_FLAGS if flag != "profile_selection_runtime_authority_granted"], errors)

    principles = record.get("layer_b_principles")
    if not isinstance(principles, list):
        errors.append("registry.layer_b_principles must be a list")
    else:
        ids = []
        for index, principle in enumerate(principles):
            if not isinstance(principle, dict):
                errors.append(f"registry.layer_b_principles[{index}] must be a dictionary")
                continue
            _validate_closed_schema(principle, PRINCIPLE_KEYS, f"registry.layer_b_principles[{index}]", errors)
            ids.append(principle.get("id"))
            if principle.get("source_doc") != "BLK-078":
                errors.append(f"registry.layer_b_principles[{index}].source_doc must be BLK-078")
            if principle.get("layer") != "Layer B":
                errors.append(f"registry.layer_b_principles[{index}].layer must be Layer B")
        if ids != list(LAYER_B_PRINCIPLE_IDS):
            errors.append("registry.layer_b_principles must exactly match BLK-078 Layer B principle IDs")

    profiles = record.get("target_profiles")
    if not isinstance(profiles, list):
        errors.append("registry.target_profiles must be a list")
    else:
        profile_ids = []
        for index, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                errors.append(f"registry.target_profiles[{index}] must be a dictionary")
                continue
            _validate_target_profile(profile, f"registry.target_profiles[{index}]", errors)
            profile_ids.append(profile.get("profile_id"))
        if profile_ids != ["kuronode-typescript"]:
            errors.append("registry.target_profiles must register exactly kuronode-typescript")

    _scan_for_laundering(record, "registry", errors)
    return errors


def validate_profile_selection_record(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    _validate_closed_schema(record, SELECTION_KEYS, "selection", errors)
    _expect_scalar(record, "selection_status", SELECTION_STATUS, errors)
    _expect_scalar(record, "selected_profile_id", "kuronode-typescript", errors)
    _expect_scalar(record, "selected_profile_source_doc", "BLK-058", errors)
    _expect_scalar(record, "selected_profile_architecture_doc", "BLK-078", errors)
    _expect_scalar(record, "selection_maturity", "L0_L1_PLANNING_FIXTURE_ONLY", errors)
    _expect_scalar(record, "layer_b_standard_id", LAYER_B_STANDARD_ID, errors)
    if record.get("layer_b_principles") != list(LAYER_B_PRINCIPLE_IDS):
        errors.append("selection.layer_b_principles must exactly match BLK-078 Layer B principle IDs")
    _validate_profile_names(record.get("validation_profiles"), "selection.validation_profiles", errors)
    _validate_denied_authorities(record.get("denied_authorities"), "selection.denied_authorities", errors)
    _validate_denied_flags(record, DENIED_FLAGS, errors)
    _scan_for_laundering(record, "selection", errors)
    return errors


def evaluate_tactical_profile_registry(record):
    evaluated = deepcopy(record) if isinstance(record, dict) else {"input": record}
    errors = validate_tactical_profile_registry(record)
    _force_false(evaluated, [flag for flag in DENIED_FLAGS if flag != "profile_selection_runtime_authority_granted"])
    evaluated["validation_errors"] = errors
    evaluated["evaluation"] = REGISTRY_BLOCKED if errors else REGISTRY_READY
    return evaluated


def evaluate_profile_selection_record(record):
    evaluated = deepcopy(record) if isinstance(record, dict) else {"input": record}
    errors = validate_profile_selection_record(record)
    _force_false(evaluated, DENIED_FLAGS)
    evaluated["validation_errors"] = errors
    evaluated["evaluation"] = SELECTION_BLOCKED if errors else SELECTION_READY
    return evaluated


def _validate_target_profile(profile, path, errors):
    _validate_closed_schema(profile, PROFILE_KEYS, path, errors)
    expected = {
        "profile_id": "kuronode-typescript",
        "profile_source_doc": "BLK-058",
        "profile_architecture_doc": "BLK-078",
        "layer": "Layer C",
        "profile_maturity": "L0_LAYER_C_SOURCE_ONLY",
    }
    for key, value in expected.items():
        _expect_scalar(profile, key, value, errors, path)
    if profile.get("layer_b_principles") != list(LAYER_B_PRINCIPLE_IDS):
        errors.append(f"{path}.layer_b_principles must exactly match BLK-078 Layer B principle IDs")
    _validate_profile_names(profile.get("validation_profiles"), f"{path}.validation_profiles", errors)
    _validate_denied_authorities(profile.get("denied_authorities"), f"{path}.denied_authorities", errors)


def _validate_closed_schema(mapping, allowed_keys, path, errors):
    if not isinstance(mapping, dict):
        errors.append(f"{path} must be a dictionary")
        return
    for key in sorted(set(mapping) - allowed_keys, key=str):
        errors.append(f"{path} unsupported key {key!r}")


def _expect_scalar(mapping, key, expected, errors, path=None):
    location = f"{path}.{key}" if path else key
    if mapping.get(key) != expected:
        errors.append(f"{location} must be {expected!r}")


def _validate_denied_flags(mapping, flags, errors):
    for flag in flags:
        if mapping.get(flag) is not False:
            errors.append(f"{flag} must be False")


def _validate_denied_authorities(values, path, errors):
    if not isinstance(values, list):
        errors.append(f"{path} must be a list")
        return
    if any(not isinstance(value, str) for value in values):
        errors.append(f"{path} entries must all be strings")
        return
    if len(values) != len(set(values)):
        errors.append(f"{path} must not contain duplicate entries")
    if tuple(values) != DENIED_AUTHORITIES:
        missing = sorted(set(DENIED_AUTHORITIES) - set(values))
        extra = sorted(set(values) - set(DENIED_AUTHORITIES))
        errors.append(f"{path} must exactly match denied_authorities; missing={missing!r} extra={extra!r}")


def _validate_profile_names(values, path, errors):
    if not isinstance(values, list):
        errors.append(f"{path} must be a list")
        return
    for value in values:
        if not isinstance(value, str):
            errors.append(f"{path} entries must be strings")
            continue
        lowered = value.lower()
        command_like = any(marker in lowered for marker in COMMAND_MARKERS)
        if command_like:
            errors.append(f"{path} contains forbidden command-shaped profile name {value!r}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
            errors.append(f"{path} profile name must be repository-owned kebab-case metadata: {value!r}")


def _scan_for_laundering(value, path, errors):
    if path.endswith(".denied_authorities") or path == "registry.denied_authorities" or path == "selection.denied_authorities":
        return
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text == "denied_authorities" or (key_text in DENIED_FLAGS and nested is False):
                continue
            normalized_key = _normalize(key_text)
            if _is_forbidden_key(normalized_key):
                errors.append(f"forbidden authority key {path}.{key_text}")
            _scan_for_laundering(nested, f"{path}.{key_text}", errors)
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _scan_for_laundering(nested, f"{path}[{index}]", errors)
    elif isinstance(value, str):
        normalized = _normalize(value)
        scrubbed = normalized.replace("notexecutionauthorized", "")
        for marker in FORBIDDEN_NORMALIZED_MARKERS:
            if marker in scrubbed:
                errors.append(f"forbidden authority wording at {path}: {value!r}")
                break


def _is_forbidden_key(normalized_key):
    if normalized_key in {_normalize(flag) for flag in DENIED_FLAGS}:
        return True
    high_risk_suffixes = (
        "authorized",
        "authority",
        "approved",
        "approval",
        "runtimeauthority",
        "executionauthority",
    )
    allowed_container_keys = {
        "deniedauthorities",
        "authoritycutline",
    }
    if normalized_key in allowed_container_keys:
        return False
    return any(normalized_key.endswith(suffix) for suffix in high_risk_suffixes)


def _normalize(text):
    return re.sub(r"[^a-z0-9]+", "", _split_camel(str(text)).lower())


def _split_camel(text):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)


def _force_false(mapping, flags):
    if not isinstance(mapping, dict):
        return
    for flag in flags:
        mapping[flag] = False
