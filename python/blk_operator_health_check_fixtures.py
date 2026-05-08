"""Inert Track I health-check boundary fixtures for BLK-System."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

BOUNDARY_FIXTURE = "HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY"
PROFILE_FIXTURE = "HEALTH_CHECK_PROFILE_FIXTURE_ONLY"
RESULT_FIXTURE = "HEALTH_CHECK_RESULT_FIXTURE_ONLY"
ESCALATION_FIXTURE = "HEALTH_CHECK_ESCALATION_FIXTURE_ONLY"
NOT_EXECUTED = "HEALTH_CHECKS_NOT_EXECUTED"
NO_AUTHORITY = "HEALTH_CHECK_AUTHORITY_NOT_GRANTED"

ALLOWED_HEALTH_CHECK_CANDIDATES = [
    ["go", "test", "./..."],
    ["go", "vet", "./..."],
    ["python3", "-m", "unittest", "discover", "python", "test_*.py"],
    ["python3", "-m", "unittest", "python.test_active_doctrine_review_gates"],
    ["git", "status", "--short", "--branch"],
]

_ALLOWED_CANDIDATES = {
    ("go", "test", "./..."): ("go_toolchain_readiness", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
    ("go", "vet", "./..."): ("go_vet_readiness", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
    ("python3", "-m", "unittest", "discover", "python", "test_*.py"): (
        "python_unittest_readiness",
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
    ),
    ("python3", "-m", "unittest", "python.test_active_doctrine_review_gates"): (
        "active_doctrine_gate_readiness",
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
    ),
    ("git", "status", "--short", "--branch"): ("git_clean_state_advisory", "ADVISORY_ONLY"),
}

SIDE_EFFECT_FLAGS = [
    "command_executed",
    "sub" + "process_started",
    "network_called",
    "file_read",
    "git_called",
    "package_manager_called",
    "source_mutated",
    "approval_captured",
    "protected_body_read",
    "active_vault_scanned",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
]

_PROFILE_ALLOWED_KEYS = {
    "check_id",
    "category",
    "classification",
    "argv",
    "description",
    "expected_evidence_ref",
    "network_denied",
    "package_manager_denied",
    "protected_vault_denied",
    "approval_required_for_execution",
    "metadata",
    *SIDE_EFFECT_FLAGS,
}
_RESULT_ALLOWED_KEYS = {
    "check_id",
    "classification",
    "status",
    "evidence_ref",
    "evidence_hash",
    "stdout_excerpt",
    "stderr_excerpt",
    "exit_code",
    "redaction_applied",
    "health_check_pass_grants_authority",
    *SIDE_EFFECT_FLAGS,
}
_RESULT_FIXTURE_KEYS = {
    "fixture_id",
    "result_fixture",
    "boundary_fixture",
    "authority",
    "execution_status",
    "check_id",
    "classification",
    "status",
    "evidence_ref",
    "evidence_hash",
    "stdout_excerpt",
    "stderr_excerpt",
    "exit_code",
    "raw_output_embedded",
    "redaction_applied",
    "health_check_pass_grants_authority",
    *SIDE_EFFECT_FLAGS,
}

_STATUS_VALUES = {
    "BLOCKED_NOT_EXECUTED",
    "PASS_SUPPLIED_BY_CALLER",
    "FAIL_SUPPLIED_BY_CALLER",
    "UNKNOWN_SUPPLIED_BY_CALLER",
}
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
MAX_ID_CHARS = 128
MAX_REF_CHARS = 512
MAX_EXCERPT_CHARS = 1000
MAX_ESCALATION_RESULTS = 20
MAX_TOTAL_EXCERPT_CHARS = 4000

_FORBIDDEN_EXACT_KEYS = {
    "active_vault_path",
    "approval_capture",
    "artifact_text",
    "body",
    "body_excerpt",
    "body_hash_input",
    "command",
    "command_line",
    "content",
    "coverage_matrix",
    "coverage_status",
    "drift",
    "drift_decision",
    "drift_rejection",
    "env",
    "environment",
    "file_path",
    "key_material",
    "ledger",
    "markdown",
    "path",
    "private_key",
    "protected_path",
    "publication",
    "raw_artifact",
    "requirement_body",
    "rtm",
    "rtm_authority",
    "rtm_id",
    "secret",
    "shell",
    "signer",
    "text",
    "token",
    "use_case_body",
}
_FORBIDDEN_TOKENS = {
    "active",
    "body",
    "command",
    "content",
    "coverage",
    "drift",
    "env",
    "environment",
    "ledger",
    "markdown",
    "path",
    "private",
    "protected",
    "publication",
    "published",
    "rtm",
    "secret",
    "shell",
    "signer",
    "text",
    "token",
    "vault",
}
_SECRET_PATTERNS = [
    "GITHUB_TOKEN",
    "AUTHORIZATION:",
    "API_KEY",
    "SECRET=",
    "SSH_AUTH_SOCK",
    ".ENV",
    "PRIVATE_KEY",
    "TOKEN=",
]
_FORBIDDEN_COMMANDS = {
    "bash",
    "sh",
    "zsh",
    "fish",
    "pwsh",
    "powershell",
    "cmd",
    "curl",
    "wget",
    "ssh",
    "scp",
    "nc",
    "ncat",
    "telnet",
    "npm",
    "pip",
    "pip3",
    "uv",
}
_GIT_MUTATIONS = {
    "commit",
    "push",
    "reset",
    "checkout",
    "stash",
    "clean",
    "revert",
    "merge",
    "rebase",
    "switch",
    "restore",
}
_PROTECTED_ARG_TOKENS = ("docs/active", "protected", "vault", "requirement_body", "use_case_body")


def build_health_check_profile_fixture(profile: dict[str, Any], *, fixture_id: str) -> dict[str, Any]:
    """Normalize a caller-supplied health-check profile as inert metadata only."""

    fixture_id = _bounded_required_string(fixture_id, "fixture_id", MAX_ID_CHARS)
    if not isinstance(profile, dict):
        raise ValueError("profile must be a dictionary")
    _reject_forbidden_fields_recursive(profile, "profile", allowed_top_level=_PROFILE_ALLOWED_KEYS)
    _reject_unsupported_fields(profile, _PROFILE_ALLOWED_KEYS, "profile")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(profile.get(flag, False), flag)

    argv = _validated_argv(profile.get("argv"))
    category, classification = _ALLOWED_CANDIDATES[tuple(argv)]
    if profile.get("category") != category:
        raise ValueError("category does not match argv candidate")
    if profile.get("classification") != classification:
        raise ValueError("classification does not match argv candidate")
    for flag in ("network_denied", "package_manager_denied", "protected_vault_denied", "approval_required_for_execution"):
        if profile.get(flag) is not True:
            raise ValueError(f"{flag} must be true")

    output = {
        "fixture_id": fixture_id,
        "profile_fixture": PROFILE_FIXTURE,
        "boundary_fixture": BOUNDARY_FIXTURE,
        "authority": NO_AUTHORITY,
        "execution_status": NOT_EXECUTED,
        "check_id": _bounded_required_string(profile.get("check_id"), "check_id", MAX_ID_CHARS),
        "category": category,
        "classification": classification,
        "argv": argv,
        "description": _bounded_required_string(profile.get("description"), "description", MAX_REF_CHARS),
        "expected_evidence_ref": _bounded_required_string(
            profile.get("expected_evidence_ref"), "expected_evidence_ref", MAX_REF_CHARS
        ),
        "network_denied": True,
        "package_manager_denied": True,
        "protected_vault_denied": True,
        "approval_required_for_execution": True,
        "health_check_pass_grants_authority": False,
    }
    for flag in SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_health_check_result_fixture(
    result: dict[str, Any], *, fixture_id: str, excerpt_max_chars: int = 320
) -> dict[str, Any]:
    """Normalize caller-supplied health-check result evidence without executing checks."""

    fixture_id = _bounded_required_string(fixture_id, "fixture_id", MAX_ID_CHARS)
    if not isinstance(result, dict):
        raise ValueError("result must be a dictionary")
    _reject_forbidden_fields_recursive(result, "result", allowed_top_level=_RESULT_ALLOWED_KEYS)
    _reject_unsupported_fields(result, _RESULT_ALLOWED_KEYS, "result")
    _validate_excerpt_limit(excerpt_max_chars)
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(result.get(flag, False), flag)
    if result.get("health_check_pass_grants_authority") is not False:
        raise ValueError("health_check_pass_grants_authority must be false")
    status = _bounded_required_string(result.get("status"), "status", MAX_ID_CHARS)
    if status not in _STATUS_VALUES:
        raise ValueError(f"unsupported status: {status}")
    classification = _bounded_required_string(result.get("classification"), "classification", MAX_ID_CHARS)
    if classification not in {"ADVISORY_ONLY", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"}:
        raise ValueError("classification is not supported for result fixtures")
    stdout_excerpt = _bounded_excerpt(
        _safe_excerpt_string(result.get("stdout_excerpt"), "stdout_excerpt"), excerpt_max_chars
    )
    stderr_excerpt = _bounded_excerpt(
        _safe_excerpt_string(result.get("stderr_excerpt"), "stderr_excerpt"), excerpt_max_chars
    )
    output = {
        "fixture_id": fixture_id,
        "result_fixture": RESULT_FIXTURE,
        "boundary_fixture": BOUNDARY_FIXTURE,
        "authority": NO_AUTHORITY,
        "execution_status": NOT_EXECUTED,
        "check_id": _bounded_required_string(result.get("check_id"), "check_id", MAX_ID_CHARS),
        "classification": classification,
        "status": status,
        "evidence_ref": _bounded_required_string(result.get("evidence_ref"), "evidence_ref", MAX_REF_CHARS),
        "evidence_hash": _required_hash(result.get("evidence_hash"), "evidence_hash"),
        "stdout_excerpt": stdout_excerpt,
        "stderr_excerpt": stderr_excerpt,
        "exit_code": _optional_exit_code(result.get("exit_code")),
        "raw_output_embedded": False,
        "redaction_applied": _required_bool(result.get("redaction_applied"), "redaction_applied"),
        "health_check_pass_grants_authority": False,
    }
    if output["redaction_applied"] is not True:
        raise ValueError("redaction_applied must be true")
    for flag in SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_health_check_escalation_fixture(results: list[dict[str, Any]], *, package_id: str) -> dict[str, Any]:
    """Package bounded health-check result fixtures for operator escalation."""

    package_id = _bounded_required_string(package_id, "package_id", MAX_ID_CHARS)
    if not isinstance(results, list) or not results:
        raise ValueError("results must be a non-empty list")
    if len(results) > MAX_ESCALATION_RESULTS:
        raise ValueError(f"too many results: maximum is {MAX_ESCALATION_RESULTS}")
    normalized = [_validate_result_fixture(item) for item in results]
    total = sum(len(item["stdout_excerpt"]) + len(item["stderr_excerpt"]) for item in normalized)
    if total > MAX_TOTAL_EXCERPT_CHARS:
        raise ValueError("bounded excerpts exceed total package limit")
    output = {
        "package_id": package_id,
        "package_fixture": ESCALATION_FIXTURE,
        "boundary_fixture": BOUNDARY_FIXTURE,
        "authority": NO_AUTHORITY,
        "execution_status": NOT_EXECUTED,
        "result_count": len(normalized),
        "result_ids": [item["fixture_id"] for item in normalized],
        "check_ids": [item["check_id"] for item in normalized],
        "statuses": [item["status"] for item in normalized],
        "classifications": [item["classification"] for item in normalized],
        "evidence_refs": [item["evidence_ref"] for item in normalized],
        "evidence_hashes": [item["evidence_hash"] for item in normalized],
        "stdout_excerpts": [item["stdout_excerpt"] for item in normalized],
        "stderr_excerpts": [item["stderr_excerpt"] for item in normalized],
        "raw_output_embedded": False,
        "health_check_pass_grants_authority": False,
    }
    for flag in SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def _validate_result_fixture(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise ValueError("result must be a dictionary")
    _reject_forbidden_fields_recursive(result, "result fixture", allowed_top_level=_RESULT_FIXTURE_KEYS)
    _reject_unsupported_fields(result, _RESULT_FIXTURE_KEYS, "result fixture")
    if result.get("result_fixture") != RESULT_FIXTURE:
        raise ValueError("result_fixture must be HEALTH_CHECK_RESULT_FIXTURE_ONLY")
    if result.get("boundary_fixture") != BOUNDARY_FIXTURE:
        raise ValueError("boundary_fixture must be HEALTH_CHECK_BOUNDARY_FIXTURE_ONLY")
    if result.get("authority") != NO_AUTHORITY:
        raise ValueError("result authority must be HEALTH_CHECK_AUTHORITY_NOT_GRANTED")
    if result.get("execution_status") != NOT_EXECUTED:
        raise ValueError("execution_status must be HEALTH_CHECKS_NOT_EXECUTED")
    _bounded_required_string(result.get("fixture_id"), "fixture_id", MAX_ID_CHARS)
    _bounded_required_string(result.get("check_id"), "check_id", MAX_ID_CHARS)
    if result.get("classification") not in {"ADVISORY_ONLY", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"}:
        raise ValueError("result classification is unsupported")
    if result.get("status") not in _STATUS_VALUES:
        raise ValueError("result status is unsupported")
    _bounded_required_string(result.get("evidence_ref"), "evidence_ref", MAX_REF_CHARS)
    _required_hash(result.get("evidence_hash"), "evidence_hash")
    stdout_excerpt = _safe_excerpt_string(result.get("stdout_excerpt"), "stdout_excerpt")
    stderr_excerpt = _safe_excerpt_string(result.get("stderr_excerpt"), "stderr_excerpt")
    if len(stdout_excerpt) > MAX_EXCERPT_CHARS or len(stderr_excerpt) > MAX_EXCERPT_CHARS:
        raise ValueError("bounded excerpt exceeds maximum size")
    if result.get("raw_output_embedded") is not False:
        raise ValueError("raw_output_embedded must be false")
    if result.get("redaction_applied") is not True:
        raise ValueError("redaction_applied must be true")
    if result.get("health_check_pass_grants_authority") is not False:
        raise ValueError("health_check_pass_grants_authority must be false")
    _optional_exit_code(result.get("exit_code"))
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(result.get(flag), flag)
    return deepcopy(result)


def _validated_argv(value: Any) -> list[str]:
    if isinstance(value, str):
        raise ValueError("argv must be a fixed list, not a shell string")
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ValueError("argv must be a non-empty list of strings")
    lowered = [item.lower() for item in value]
    if lowered[0] in _FORBIDDEN_COMMANDS:
        raise ValueError("argv uses a forbidden command category")
    if lowered[0] in {"python", "python3", "node"} and any(item in {"-c", "-e"} for item in lowered[1:]):
        raise ValueError("argv uses an inline interpreter wrapper")
    if lowered[0] == "go" and len(lowered) > 1 and lowered[1] == "get":
        raise ValueError("argv uses a package retrieval command")
    if lowered[0] == "git" and (len(lowered) < 2 or lowered[1] in _GIT_MUTATIONS):
        raise ValueError("argv uses forbidden Git mutation authority")
    joined = " ".join(lowered)
    if any(token in joined for token in _PROTECTED_ARG_TOKENS):
        raise ValueError("argv attempts protected-vault or body/path scanning")
    candidate = tuple(value)
    if candidate not in _ALLOWED_CANDIDATES:
        raise ValueError("argv candidate is not allowlisted")
    return list(value)


def _reject_forbidden_fields_recursive(
    value: Any, context: str, *, allowed_top_level: set[str] | None = None
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if allowed_top_level is None or key_text not in allowed_top_level:
                if _is_forbidden_key(key_text):
                    raise ValueError(f"{context} rejects forbidden field: {key}")
                _reject_forbidden_fields_recursive(nested, context)
            else:
                _reject_forbidden_fields_recursive(nested, context)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_fields_recursive(item, context)
    elif isinstance(value, str):
        _reject_secret_or_environment_leakage(value)


def _is_forbidden_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    if normalized in _FORBIDDEN_EXACT_KEYS:
        return True
    tokens = {part for part in normalized.split("_") if part}
    if tokens & _FORBIDDEN_TOKENS:
        return True
    composites = {
        "active_vault",
        "protected_vault",
        "private_key",
        "key_material",
        "beo_publication",
        "rtm_status",
    }
    return any(composite in normalized for composite in composites)


def _reject_unsupported_fields(value: dict[str, Any], allowed: set[str], context: str) -> None:
    for key in value:
        if key not in allowed:
            raise ValueError(f"{context} unsupported field: {key}")


def _bounded_excerpt(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def _validate_excerpt_limit(value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or not 24 <= value <= MAX_EXCERPT_CHARS:
        raise ValueError(f"excerpt_max_chars must be between 24 and {MAX_EXCERPT_CHARS}")


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    _reject_secret_or_environment_leakage(value)
    return value


def _bounded_required_string(value: Any, field: str, max_chars: int) -> str:
    text = _required_string(value, field).strip()
    if len(text) > max_chars:
        raise ValueError(f"{field} must be at most {max_chars} characters")
    return text


def _safe_excerpt_string(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    _reject_secret_or_environment_leakage(value)
    return value


def _reject_secret_or_environment_leakage(value: str) -> None:
    upper = value.upper()
    if any(pattern in upper for pattern in _SECRET_PATTERNS):
        raise ValueError("secret or environment leakage is rejected")


def _required_hash(value: Any, field: str) -> str:
    text = _required_string(value, field).strip()
    if not _HASH_RE.match(text):
        raise ValueError(f"{field} must be sha256:<64 lowercase hex characters>")
    return text


def _required_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _required_false(value: Any, field: str) -> None:
    if value is not False:
        raise ValueError(f"{field} must be false")


def _optional_exit_code(value: Any) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("exit_code must be an integer or null")
    return value
