from copy import deepcopy
import re

from blk_tactical_profile_registry import (
    build_profile_selection_record,
    validate_profile_selection_record,
)

GOVERNANCE_ID = "blk_system_target_repo_execution_governance_pattern"
GOVERNANCE_STATUS = "TARGET_REPO_EXECUTION_GOVERNANCE_L0_L1_FIXTURE_ONLY"
GOVERNANCE_MATURITY = "L0_L1_DOCTRINE_FIXTURE_ONLY"
READY = "TARGET_REPO_GOVERNANCE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
BLOCKED = "TARGET_REPO_GOVERNANCE_BLOCKED"

GOVERNANCE_STAGES = (
    "request_package",
    "profile_selection",
    "approval_envelope",
    "preflight_refusal",
    "approval_capture",
    "blk_pipe_invocation_boundary",
    "validation_evidence",
    "hostile_audit",
    "target_repo_closeout",
)

DENIED_AUTHORITIES = (
    "NO_GOVERNANCE_RECORD_RUNTIME_AUTHORITY",
    "NO_TARGET_REPO_SCAN_AUTHORITY",
    "NO_TARGET_REPO_MUTATION_AUTHORITY",
    "NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY",
    "NO_APPROVAL_ENVELOPE_RETARGETING_AUTHORITY",
    "NO_LIVE_CODEX_EXECUTION_AUTHORITY",
    "NO_BLK_PIPE_EXECUTION_AUTHORITY",
    "NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY",
    "NO_BEO_PUBLICATION_AUTHORITY",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY",
    "NO_PROTECTED_BLK_REQ_BODY_READS",
    "NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY",
    "NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM",
)

SIDE_EFFECT_FLAGS = (
    "governance_record_runtime_authority_granted",
    "target_repo_scan_authorized",
    "target_repo_mutation_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "approval_envelope_retargeting_authorized",
    "live_codex_execution_authorized",
    "blk_pipe_execution_authorized",
    "production_blk_test_mcp_authorized",
    "beo_publication_authorized",
    "rtm_generation_authorized",
    "protected_body_reads_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

TOP_LEVEL_KEYS = {
    "governance_id",
    "governance_status",
    "governance_maturity",
    "governing_docs",
    "required_stage_order",
    "target_identity",
    "profile_selection_record",
    "approval_envelope",
    "target_boundaries",
    "stop_conditions",
    "hostile_review_checklist",
    "denied_authorities",
    "evaluation",
    "validation_errors",
    *SIDE_EFFECT_FLAGS,
}

TARGET_IDENTITY_KEYS = {
    "target_repo_id",
    "target_repo_absolute_path",
    "target_branch",
    "target_head_sha",
    "observed_remote_head_sha",
    "target_identity_status",
}

APPROVAL_ENVELOPE_KEYS = {
    "request_id",
    "approval_id",
    "run_id",
    "expires_at_utc",
    "replay_policy",
    "approval_scope",
    "operator_identity",
}

TARGET_BOUNDARY_KEYS = {
    "source_allowlist",
    "protected_denylist",
    "validation_profiles",
}

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

FORBIDDEN_NORMALIZED_MARKERS = (
    "approvedforliveexecution",
    "approvedforruntimeexecution",
    "runtimeexecutionapproved",
    "runtimeexecutionauthorized",
    "runtimeapproval",
    "profileselectiongrantsruntimeauthority",
    "governancerecordgrantsruntimeauthority",
    "approvalenveloperetargetingisallowed",
    "approvalretargetingallowed",
    "targetreposcanauthorized",
    "targetscanauthorized",
    "livetargetscanauthorized",
    "targetrepomutationauthorized",
    "targetmutationauthorized",
    "bebdispatchauthorized",
    "beodispatchauthorized",
    "beocloseoutexecutionauthorized",
    "livecodexexecutionauthorized",
    "codexexecutionauthorized",
    "blkpipeexecutionauthorized",
    "productionblktestmcpisauthorized",
    "productionblktestmcpauthorized",
    "authoritativebeopublication",
    "beopublicationauthorized",
    "beopublicationauthority",
    "publishbeo",
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
)

DEFAULT_TARGET_IDENTITY = {
    "target_repo_id": "kuronode-v1-fixture",
    "target_repo_absolute_path": "/__BLK_FIXTURE__/target/Kuronode-v1",
    "target_branch": "main",
    "target_head_sha": "a" * 40,
    "observed_remote_head_sha": "a" * 40,
    "target_identity_status": "EXACT_TARGET_IDENTITY_REQUIRED_NOT_RESOLVED_BY_FIXTURE",
}

DEFAULT_APPROVAL_ENVELOPE = {
    "request_id": "BLK-SYSTEM-081-TARGET-REPO-GOVERNANCE-REQUEST-FIXTURE",
    "approval_id": "FUTURE_EXPLICIT_APPROVAL_REQUIRED_NOT_GRANTED",
    "run_id": "FUTURE_ONE_RUN_ID_REQUIRED_NOT_CONSUMED",
    "expires_at_utc": "2099-01-01T00:00:00Z",
    "replay_policy": "future_run_id_must_be_one_use_and_durably_recorded",
    "approval_scope": "future approval must bind exact repo, path, branch, local head, remote head, allowlist, validation profiles, profile selection, request ID, approval ID, run ID, expiry, replay policy, and stop conditions",
    "operator_identity": "future_explicit_operator_identity_required",
}

DEFAULT_TARGET_BOUNDARIES = {
    "source_allowlist": [
        "src/**/*.ts",
        "src/**/*.tsx",
        "tests/**/*.ts",
        "tests/**/*.tsx",
    ],
    "protected_denylist": [
        ".git/**",
        "node_modules/**",
        "dist/**",
        "build/**",
        "coverage/**",
        ".env*",
        "secrets/**",
        "docs/active/**",
    ],
    "validation_profiles": [
        "kuronode-power-of-ten-static",
        "kuronode-typecheck-strict",
        "kuronode-eslint-zero-warning",
    ],
}

DEFAULT_STOP_CONDITIONS = [
    "missing explicit future approval envelope",
    "target path, branch, local head, or remote head mismatch",
    "expired or replayed approval ID or run ID",
    "profile selection treated as target scan or mutation authority",
    "validation profile replaced by command-shaped shell string",
    "attempt to move into BEB dispatch, BEO closeout, publication, trace-matrix, or drift-decision frontiers",
    "attempt to read protected BLK-req bodies or protected target paths",
]

DEFAULT_HOSTILE_REVIEW_CHECKLIST = [
    "exact target identity preserved",
    "profile selection remains review-only",
    "approval envelope does not retarget stale evidence",
    "preflight refusal blocks absent, stale, expired, replayed, or mismatched authority",
    "BLK-pipe invocation boundary is described but not executed",
    "validation evidence uses repository-owned profile names only",
    "BEB/BEO, publication, RTM, protected-body, tooling, and sandbox authority remain denied",
]


def build_target_repo_execution_governance_record():
    record = {
        "governance_id": GOVERNANCE_ID,
        "governance_status": GOVERNANCE_STATUS,
        "governance_maturity": GOVERNANCE_MATURITY,
        "governing_docs": ["BLK-001", "BLK-003", "BLK-004", "BLK-058", "BLK-078", "BLK-080", "BLK-081"],
        "required_stage_order": list(GOVERNANCE_STAGES),
        "target_identity": deepcopy(DEFAULT_TARGET_IDENTITY),
        "profile_selection_record": build_profile_selection_record(),
        "approval_envelope": deepcopy(DEFAULT_APPROVAL_ENVELOPE),
        "target_boundaries": deepcopy(DEFAULT_TARGET_BOUNDARIES),
        "stop_conditions": list(DEFAULT_STOP_CONDITIONS),
        "hostile_review_checklist": list(DEFAULT_HOSTILE_REVIEW_CHECKLIST),
        "denied_authorities": list(DENIED_AUTHORITIES),
        "evaluation": READY,
        "validation_errors": [],
    }
    for flag in SIDE_EFFECT_FLAGS:
        record[flag] = False
    return record


def validate_target_repo_execution_governance_record(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be a dictionary"]

    _validate_closed_schema(record, TOP_LEVEL_KEYS, "governance", errors)
    _expect_scalar(record, "governance_id", GOVERNANCE_ID, errors)
    _expect_scalar(record, "governance_status", GOVERNANCE_STATUS, errors)
    _expect_scalar(record, "governance_maturity", GOVERNANCE_MATURITY, errors)
    if record.get("required_stage_order") != list(GOVERNANCE_STAGES):
        errors.append("required_stage_order must exactly match target-repo governance stages")
    _validate_governing_docs(record.get("governing_docs"), errors)
    _validate_target_identity(record.get("target_identity"), errors)
    _validate_profile_selection(record.get("profile_selection_record"), errors)
    _validate_approval_envelope(record.get("approval_envelope"), errors)
    _validate_target_boundaries(record.get("target_boundaries"), errors)
    _validate_required_strings(record.get("stop_conditions"), "stop_conditions", errors)
    _validate_required_strings(record.get("hostile_review_checklist"), "hostile_review_checklist", errors)
    _validate_denied_authorities(record.get("denied_authorities"), "denied_authorities", errors)
    _validate_side_effect_flags(record, errors)
    _scan_for_laundering(record, "governance", errors)
    return errors


def evaluate_target_repo_execution_governance_record(record):
    evaluated = deepcopy(record) if isinstance(record, dict) else {"input": record}
    errors = validate_target_repo_execution_governance_record(record)
    for flag in SIDE_EFFECT_FLAGS:
        evaluated[flag] = False
    evaluated["validation_errors"] = errors
    evaluated["evaluation"] = BLOCKED if errors else READY
    return evaluated


def _validate_target_identity(identity, errors):
    if not isinstance(identity, dict):
        errors.append("target_identity must be a dictionary")
        return
    _validate_closed_schema(identity, TARGET_IDENTITY_KEYS, "target_identity", errors)
    _require_keys(identity, TARGET_IDENTITY_KEYS, "target_identity", errors)
    for key in TARGET_IDENTITY_KEYS:
        if not isinstance(identity.get(key), str) or not identity.get(key):
            errors.append(f"target_identity.{key} must be a non-empty string")
    path = identity.get("target_repo_absolute_path")
    if isinstance(path, str):
        if not path.startswith("/"):
            errors.append("target_identity.target_repo_absolute_path must be an absolute path string")
        normalized_path = path.replace("\\", "/")
        if "/../" in normalized_path or normalized_path.endswith("/.."):
            errors.append("target_identity.target_repo_absolute_path must not contain traversal")
    for key in ("target_head_sha", "observed_remote_head_sha"):
        value = identity.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
            errors.append(f"target_identity.{key} must be a 40-character lowercase hex commit SHA")
    if identity.get("target_head_sha") != identity.get("observed_remote_head_sha"):
        errors.append("target_identity.observed_remote_head_sha must match target_head_sha until fresh approval names the observed remote head")


def _validate_profile_selection(selection, errors):
    if not isinstance(selection, dict):
        errors.append("profile_selection_record must be a dictionary")
        return
    nested_errors = validate_profile_selection_record(selection)
    for error in nested_errors:
        errors.append(f"profile_selection_record invalid: {error}")
    expected = {
        "selection_status": "PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY",
        "selected_profile_id": "kuronode-typescript",
        "selected_profile_source_doc": "BLK-058",
        "selected_profile_architecture_doc": "BLK-078",
    }
    for key, value in expected.items():
        if selection.get(key) != value:
            errors.append(f"profile_selection_record.{key} must be {value!r}")


def _validate_approval_envelope(approval, errors):
    if not isinstance(approval, dict):
        errors.append("approval_envelope must be a dictionary")
        return
    _validate_closed_schema(approval, APPROVAL_ENVELOPE_KEYS, "approval_envelope", errors)
    _require_keys(approval, APPROVAL_ENVELOPE_KEYS, "approval_envelope", errors)
    for key in APPROVAL_ENVELOPE_KEYS:
        if not isinstance(approval.get(key), str) or not approval.get(key):
            errors.append(f"approval_envelope.{key} must be a non-empty string")
    expires = approval.get("expires_at_utc")
    if isinstance(expires, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", expires):
        errors.append("approval_envelope.expires_at_utc must be an explicit UTC timestamp string")
    replay = approval.get("replay_policy")
    if isinstance(replay, str) and "one_use" not in replay:
        errors.append("approval_envelope.replay_policy must require one_use replay protection")


def _validate_target_boundaries(boundaries, errors):
    if not isinstance(boundaries, dict):
        errors.append("target_boundaries must be a dictionary")
        return
    _validate_closed_schema(boundaries, TARGET_BOUNDARY_KEYS, "target_boundaries", errors)
    _require_keys(boundaries, TARGET_BOUNDARY_KEYS, "target_boundaries", errors)
    _validate_required_strings(boundaries.get("source_allowlist"), "target_boundaries.source_allowlist", errors)
    _validate_required_strings(boundaries.get("protected_denylist"), "target_boundaries.protected_denylist", errors)
    _validate_profile_names(boundaries.get("validation_profiles"), "target_boundaries.validation_profiles", errors)


def _validate_governing_docs(values, errors):
    required = {"BLK-001", "BLK-003", "BLK-004", "BLK-058", "BLK-078", "BLK-080", "BLK-081"}
    if not isinstance(values, list) or not values:
        errors.append("governing_docs must be a non-empty list")
        return
    if set(values) != required or len(values) != len(required):
        errors.append(f"governing_docs must exactly match {sorted(required)!r}")
    for value in values:
        if not isinstance(value, str) or not re.fullmatch(r"BLK-\d{3}", value):
            errors.append(f"governing_docs entry must be a BLK doc ID: {value!r}")


def _validate_required_strings(values, path, errors):
    if not isinstance(values, list) or not values:
        errors.append(f"{path} must be a non-empty list")
        return
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value:
            errors.append(f"{path}[{index}] must be a non-empty string")


def _validate_profile_names(values, path, errors):
    if not isinstance(values, list) or not values:
        errors.append(f"{path} must be a non-empty list")
        return
    for value in values:
        if not isinstance(value, str):
            errors.append(f"{path} entries must be strings")
            continue
        lowered = value.lower()
        if any(marker in lowered for marker in COMMAND_MARKERS):
            errors.append(f"{path} contains forbidden command-shaped profile name {value!r}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
            errors.append(f"{path} profile name must be repository-owned kebab-case metadata: {value!r}")


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


def _validate_side_effect_flags(record, errors):
    for flag in SIDE_EFFECT_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{flag} must be False")


def _validate_closed_schema(mapping, allowed_keys, path, errors):
    if not isinstance(mapping, dict):
        errors.append(f"{path} must be a dictionary")
        return
    for key in sorted(set(mapping) - allowed_keys, key=str):
        errors.append(f"{path} unsupported key {key!r}")


def _require_keys(mapping, required_keys, path, errors):
    for key in sorted(required_keys):
        if key not in mapping:
            errors.append(f"{path}.{key} is required")


def _expect_scalar(mapping, key, expected, errors):
    if mapping.get(key) != expected:
        errors.append(f"{key} must be {expected!r}")


def _scan_for_laundering(value, path, errors):
    if path.endswith(".denied_authorities") or path == "governance.denied_authorities":
        return
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if key_text == "denied_authorities" or (isinstance(nested, bool) and nested is False):
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
    if normalized_key in {"deniedauthorities", "approvalenvelope", "approvalid", "approvalscope"}:
        return False
    high_risk_suffixes = (
        "authorized",
        "authority",
        "approved",
        "runtimeauthority",
        "executionauthority",
    )
    return any(normalized_key.endswith(suffix) for suffix in high_risk_suffixes)


def _normalize(text):
    return re.sub(r"[^a-z0-9]+", "", _split_camel(str(text)).lower())


def _split_camel(text):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
