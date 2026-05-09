from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from blk_codex_invocation_profile import validate_codex_deterministic_invocation_profile

PROFILE_ID = "codex_deterministic_dispatch_envelope"
DISPATCH_STATUS = "CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY"
TELEMETRY_AUTHORITY = "CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY"
ARTIFACT_ROOT = PurePosixPath("artifacts/codex")
MAX_PATH_LENGTH = 160
REQUIRED_APPROVAL_FIELDS = frozenset(
    {
        "approval_id",
        "source_system",
        "operator_identity",
        "message_event_id",
        "timestamp",
        "expires_at",
        "exact_approved_scope",
        "explicit_excluded_authorities",
    }
)
REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "live_codex_execution",
        "blk_pipe_dispatch",
        "production_blk_test_mcp",
        "source_mutation",
        "git_mutation",
        "protected_body_read",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "production_sandbox_claim",
    }
)
ALLOWED_VALIDATION_PROFILES = frozenset(
    {
        "python-unittest",
        "active-doctrine-gate",
        "codex-invocation-profile-test",
        "codex-dispatch-envelope-test",
        "go-test-all",
        "go-vet-all",
    }
)
REQUIRED_HOSTILE_AUDIT_CHECKS = frozenset(
    {
        "file_boundary_check",
        "validation_gate_check",
        "telemetry_advisory_check",
        "authority_non_expansion_check",
    }
)
REQUIRED_ESCALATION_CASES = frozenset(
    {
        "missing_approval",
        "policy_block",
        "validation_failure",
        "failure_ceiling",
        "malformed_telemetry",
        "denied_authority",
    }
)
FORBIDDEN_AUTHORITY_TERMS = (
    "live_codex_execution",
    "blk_pipe_dispatch",
    "production_blk_test_mcp",
    "protected_body",
    "active_vault",
    "beo_publication",
    "rtm_generation",
    "drift_rejection",
    "production_sandbox",
    "network_firewall",
    "host_secret_isolation",
    "source_mutation",
    "git_mutation",
    "package_manager",
    "network_model_cyber",
    "dispatch_started_by_envelope_helper",
    "subprocess_started_by_envelope_helper",
    "profile_grants_execution_authority",
)
FORBIDDEN_STRING_MARKERS = tuple(
    marker.casefold()
    for marker in (
        "CODEX_LIVE_APPROVAL",
        "BLK_PIPE_EXECUTION_APPROVAL",
        "BLK_TEST_PASS grants execution authority",
        "PRODUCTION_SANDBOX_ENFORCED",
        "PRODUCTION_SANDBOX_AUTHORITY",
        "NETWORK_FIREWALL_ENFORCED",
        "HOST_SECRET_ISOLATION_ENFORCED",
        "BEO_PUBLICATION_APPROVAL",
        "RTM_GENERATION_APPROVAL",
        "DRIFT_REJECTION_AUTHORITY",
        "PROTECTED_BODY_READ_ALLOWED",
        "pip install",
        "npm install",
        "curl ",
        "wget ",
        "ssh ",
    )
)
SHELLLIKE_PATH_MARKERS = ("*", "?", "[", "]", ":(", ";", "&&", "||", "|", "$", "`", "<", ">", "\n", "\r")


def build_codex_deterministic_dispatch_envelope(
    *,
    codex_profile: dict[str, Any],
    approval_provenance: dict[str, Any],
    allowed_modified_files: list[str],
    allowed_new_files: list[str],
    validation_profiles: list[str],
    telemetry_artifacts: dict[str, str],
    failure_ceiling: dict[str, Any],
    hostile_audit: dict[str, Any],
    operator_escalation: dict[str, Any],
    run_id: str,
    used_approval_ids: set[str],
    used_run_ids: set[str],
    now: str,
) -> dict[str, Any]:
    """Build a pure, non-executing Codex dispatch envelope fixture."""
    envelope = {
        "profile_id": PROFILE_ID,
        "dispatch_status": DISPATCH_STATUS,
        "codex_profile": codex_profile,
        "approval_provenance": approval_provenance,
        "allowed_modified_files": list(allowed_modified_files),
        "allowed_new_files": list(allowed_new_files),
        "validation_profiles": list(validation_profiles),
        "telemetry_artifacts": dict(telemetry_artifacts),
        "telemetry_authority": TELEMETRY_AUTHORITY,
        "failure_ceiling": dict(failure_ceiling),
        "hostile_audit": {"required_checks": list(hostile_audit.get("required_checks", []))},
        "operator_escalation": {"required_cases": list(operator_escalation.get("required_cases", []))},
        "run_id": run_id,
        "dispatch_started_by_envelope_helper": False,
        "subprocess_started_by_envelope_helper": False,
        "profile_grants_execution_authority": False,
        "live_codex_execution_authorized": False,
        "blk_pipe_dispatch_authorized": False,
        "production_blk_test_mcp_authorized": False,
        "source_mutation_authorized": False,
        "git_mutation_authorized": False,
        "protected_body_read_authorized": False,
        "protected_body_copy_authorized": False,
        "active_vault_scan_authorized": False,
        "beo_publication_authorized": False,
        "rtm_generation_authorized": False,
        "drift_rejection_authorized": False,
        "network_model_cyber_tooling_authorized": False,
        "package_manager_authorized": False,
        "production_sandbox_claimed": False,
    }
    return validate_codex_deterministic_dispatch_envelope(
        envelope, now=now, used_approval_ids=used_approval_ids, used_run_ids=used_run_ids
    )


def validate_codex_deterministic_dispatch_envelope(
    envelope: dict[str, Any],
    *,
    now: str,
    used_approval_ids: set[str],
    used_run_ids: set[str],
) -> dict[str, Any]:
    """Validate the non-authorizing dispatch envelope shape and return it unchanged."""
    if not isinstance(envelope, dict):
        raise ValueError("envelope must be a dictionary")
    if used_approval_ids is None:
        raise ValueError("used_approval_ids must be supplied for replay protection")
    if used_run_ids is None:
        raise ValueError("used_run_ids must be supplied for replay protection")
    if envelope.get("profile_id") != PROFILE_ID:
        raise ValueError("profile_id must be codex_deterministic_dispatch_envelope")
    if envelope.get("dispatch_status") != DISPATCH_STATUS:
        raise ValueError(f"dispatch_status must be {DISPATCH_STATUS}")

    validate_codex_deterministic_invocation_profile(envelope.get("codex_profile"))
    approval = _validate_approval(envelope.get("approval_provenance"), now=now)
    if approval["approval_id"] in used_approval_ids:
        raise ValueError("replayed approval id is not allowed")
    run_id = envelope.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string")
    if run_id in used_run_ids:
        raise ValueError("replayed run id is not allowed")

    _validate_file_boundaries(envelope.get("allowed_modified_files"), "allowed_modified_files")
    _validate_file_boundaries(envelope.get("allowed_new_files"), "allowed_new_files")
    _validate_validation_profiles(envelope.get("validation_profiles"))
    _validate_telemetry(envelope.get("telemetry_artifacts"))
    _validate_failure_ceiling(envelope.get("failure_ceiling"))
    _validate_required_set(
        envelope.get("hostile_audit", {}).get("required_checks"),
        REQUIRED_HOSTILE_AUDIT_CHECKS,
        "hostile_audit.required_checks",
    )
    _validate_required_set(
        envelope.get("operator_escalation", {}).get("required_cases"),
        REQUIRED_ESCALATION_CASES,
        "operator_escalation.required_cases",
    )
    if envelope.get("telemetry_authority") != TELEMETRY_AUTHORITY:
        raise ValueError("telemetry_authority must remain advisory only")
    _scan_for_authority_laundering(envelope)
    return envelope


def _validate_approval(approval: Any, *, now: str) -> dict[str, Any]:
    if not isinstance(approval, dict):
        raise ValueError("approval_provenance must be a dictionary")
    missing = sorted(REQUIRED_APPROVAL_FIELDS - set(approval))
    if missing:
        raise ValueError(f"approval_provenance missing required fields: {missing}")
    for field in REQUIRED_APPROVAL_FIELDS - {"explicit_excluded_authorities"}:
        value = approval.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"approval_provenance.{field} must be a non-empty string")
    excluded = approval.get("explicit_excluded_authorities")
    if not isinstance(excluded, list):
        raise ValueError("approval_provenance.explicit_excluded_authorities must be a list")
    missing_exclusions = sorted(REQUIRED_EXCLUDED_AUTHORITIES - set(excluded))
    if missing_exclusions:
        raise ValueError(f"approval_provenance excluded authorities incomplete: {missing_exclusions}")
    expires_at = _parse_timestamp(approval["expires_at"], "approval_provenance.expires_at")
    now_value = _parse_timestamp(now, "now")
    if expires_at <= now_value:
        raise ValueError("approval_provenance is expired")
    return approval


def _validate_file_boundaries(paths: Any, field: str) -> None:
    if not isinstance(paths, list):
        raise ValueError(f"{field} must be a list")
    for value in paths:
        _validate_repo_path(value, field)
    if field == "allowed_modified_files" and not paths:
        raise ValueError("allowed_modified_files must not be empty for dispatch envelope fixtures")


def _validate_repo_path(path: Any, field: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(f"{field} contains an empty path")
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError(f"{field} path exceeds length bound")
    if any(marker in path for marker in SHELLLIKE_PATH_MARKERS):
        raise ValueError(f"{field} contains broad/shell-like path marker: {path!r}")
    posix = PurePosixPath(path)
    if posix.is_absolute():
        raise ValueError(f"{field} must contain relative repository paths only")
    parts = posix.parts
    if path == "." or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{field} contains invalid traversal/current path")
    if ".git" in parts:
        raise ValueError(f"{field} must not reference .git")
    protected_prefixes = (
        PurePosixPath("docs/active"),
        PurePosixPath("docs/requirements"),
        PurePosixPath("docs/use_cases"),
    )
    for prefix in protected_prefixes:
        if parts[: len(prefix.parts)] == prefix.parts:
            raise ValueError(f"{field} must not reference protected BLK-req paths")
    return posix.as_posix()


def _validate_validation_profiles(profiles: Any) -> None:
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("validation_profiles must be a non-empty list")
    for profile in profiles:
        if not isinstance(profile, str) or profile not in ALLOWED_VALIDATION_PROFILES:
            raise ValueError(f"validation profile is not repository-owned/allowlisted: {profile!r}")


def _validate_telemetry(telemetry: Any) -> None:
    if not isinstance(telemetry, dict) or not telemetry:
        raise ValueError("telemetry_artifacts must be a non-empty dictionary")
    for key, path in telemetry.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("telemetry_artifacts keys must be non-empty strings")
        _validate_artifact_path(path, f"telemetry_artifacts.{key}")


def _validate_artifact_path(path: Any, field: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(f"{field} must be a non-empty relative string")
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError(f"{field} exceeds deterministic envelope length bound")
    posix = PurePosixPath(path)
    if posix.is_absolute():
        raise ValueError(f"{field} must be relative")
    parts = posix.parts
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{field} must not contain traversal segments")
    if ".git" in parts:
        raise ValueError(f"{field} must not target .git")
    if parts[:2] != ARTIFACT_ROOT.parts or len(parts) <= len(ARTIFACT_ROOT.parts):
        raise ValueError(f"{field} must be under {ARTIFACT_ROOT}/")
    return posix.as_posix()


def _validate_failure_ceiling(failure_ceiling: Any) -> None:
    if not isinstance(failure_ceiling, dict):
        raise ValueError("failure_ceiling must be a dictionary")
    max_iterations = failure_ceiling.get("max_iterations")
    if not isinstance(max_iterations, int) or not 1 <= max_iterations <= 3:
        raise ValueError("failure_ceiling.max_iterations must be an integer from 1 through 3")
    if failure_ceiling.get("on_exhaustion") != "OPERATOR_ESCALATION_REQUIRED":
        raise ValueError("failure_ceiling.on_exhaustion must require operator escalation")


def _validate_required_set(values: Any, required: frozenset[str], field: str) -> None:
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list")
    missing = sorted(required - set(values))
    if missing:
        raise ValueError(f"{field} missing required values: {missing}")


def _scan_for_authority_laundering(value: Any, path: str = "envelope") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if _looks_like_forbidden_authority_key(key_text) and child is not False:
                raise ValueError(f"forbidden authority field at {path}.{key_text}")
            _scan_for_authority_laundering(child, f"{path}.{key_text}")
    elif isinstance(value, (list, tuple, set)):
        for index, child in enumerate(value):
            _scan_for_authority_laundering(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.casefold()
        for marker in FORBIDDEN_STRING_MARKERS:
            if marker in lowered:
                raise ValueError(f"forbidden authority wording at {path}")


def _looks_like_forbidden_authority_key(key: str) -> bool:
    lowered = key.casefold()
    return any(term in lowered for term in FORBIDDEN_AUTHORITY_TERMS)


def _parse_timestamp(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a timestamp string")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601 parseable") from exc
