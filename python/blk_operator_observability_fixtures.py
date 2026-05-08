"""Deterministic local operator observability fixtures for BLK-System.

The helpers in this module normalize already-supplied evidence dictionaries into
bounded operator status and escalation package fixtures. They do not run live
health checks, inspect files, contact services, mutate source, capture approval,
publish BEOs, generate RTM, or make drift decisions.
"""

from __future__ import annotations

import posixpath
import re
from copy import deepcopy
from typing import Any

_STATUS_FIXTURE = "OPERATOR_OBSERVABILITY_FIXTURE_ONLY"
_PACKAGE_FIXTURE = "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY"
_AUTHORITY = "OBSERVABILITY_ONLY_NOT_EXECUTION"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
MAX_STATUS_COUNT = 20
MAX_TRACE_ARTIFACTS = 20
MAX_HEALTH_CHECK_RESULT_COUNT = 20
MAX_HEALTH_CHECK_EXCERPT_CHARS = 1000
MAX_TOTAL_HEALTH_CHECK_EXCERPT_CHARS = 4000
MAX_ID_CHARS = 128
MAX_RAW_REF_CHARS = 512
MAX_EXCERPT_CHARS = 1000
MAX_TOTAL_PACKAGE_EXCERPT_CHARS = 4000

FAILURE_CLASS_ORDER = [
    "INVALID_PAYLOAD",
    "UNAUTHORIZED_MUTATION",
    "VALIDATION_FAILED",
    "OUTPUT_FLOOD",
    "INVALID_REVERT_ANCHOR",
    "DIRTY_WORKSPACE",
    "MISSING_APPROVAL",
    "STALE_OR_REPLAYED_APPROVAL",
    "PROTECTED_VAULT_REQUEST",
    "DISABLED_BLK_TEST",
    "DRAFT_ONLY_BEO",
    "RTM_NOT_GENERATED",
    "UNKNOWN_OR_MALFORMED_REPORT",
]

_CATALOG = {
    "INVALID_PAYLOAD": {
        "domain": "BLK-pipe",
        "phrase": "Blocked before execution: invalid payload",
        "action": "fix payload or brief; separate human decision required before any retry",
    },
    "UNAUTHORIZED_MUTATION": {
        "domain": "BLK-pipe",
        "phrase": "Blocked and reverted: unauthorized mutation",
        "action": "inspect workspace; separate human decision required before any retry",
    },
    "VALIDATION_FAILED": {
        "domain": "BLK-pipe",
        "phrase": "Blocked after mutation: validation failed",
        "action": "inspect validation evidence; separate human decision required before any retry",
    },
    "OUTPUT_FLOOD": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: output limit exceeded",
        "action": "inspect bounded evidence and narrow the task; separate human decision required before any retry",
    },
    "INVALID_REVERT_ANCHOR": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: revert anchor mismatch",
        "action": "stop and escalate; revert anchor mismatch requires human workspace inspection",
    },
    "DIRTY_WORKSPACE": {
        "domain": "BLK-pipe",
        "phrase": "Blocked: workspace is dirty",
        "action": "inspect workspace before retry",
    },
    "MISSING_APPROVAL": {
        "domain": "Human gate",
        "phrase": "Blocked: missing approval",
        "action": "obtain separate current human approval",
    },
    "STALE_OR_REPLAYED_APPROVAL": {
        "domain": "Human gate",
        "phrase": "Blocked: approval stale or replayed",
        "action": "obtain fresh source-bound approval",
    },
    "PROTECTED_VAULT_REQUEST": {
        "domain": "BLK-req",
        "phrase": "Blocked: protected BLK-req vault access denied",
        "action": "use approved metadata or context channel",
    },
    "DISABLED_BLK_TEST": {
        "domain": "BLK-test",
        "phrase": "Blocked: BLK-test transport disabled",
        "action": "request a separate BLK-test authority sprint if needed",
    },
    "DRAFT_ONLY_BEO": {
        "domain": "BEO",
        "phrase": "Advisory only: BEO remains draft-only",
        "action": "request separate publication authority if needed",
    },
    "RTM_NOT_GENERATED": {
        "domain": "blk-link",
        "phrase": "Advisory only: RTM not generated",
        "action": "request separate runtime RTM authority if needed",
    },
    "UNKNOWN_OR_MALFORMED_REPORT": {
        "domain": "Observability",
        "phrase": "Blocked: report is unknown or malformed",
        "action": "inspect source evidence and add supported fixture handling",
    },
}

_REPORT_ALLOWED_KEYS = {
    "failure_class",
    "source_report_id",
    "beb_id",
    "trace_artifacts",
    "raw_evidence_ref",
    "raw_evidence_hash",
    "evidence_excerpt",
    "retry_count",
    "failure_ceiling",
    "reverted",
    "dirty",
    "approval_id",
    "actor_identity",
    "command_executed",
    "file_read",
    "network_called",
    "source_mutated",
    "approval_captured",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_scanned",
}
_TRACE_ALLOWED_KEYS = {"kind", "id", "version_hash", "meta"}
_STATUS_ALLOWED_KEYS = {
    "fixture_id",
    "status_fixture",
    "authority",
    "failure_class",
    "owning_domain",
    "concise_status",
    "source_report_id",
    "beb_id",
    "trace_artifacts",
    "raw_evidence_ref",
    "raw_evidence_hash",
    "bounded_evidence_excerpt",
    "evidence_inline_bounded",
    "raw_evidence_embedded",
    "retry_count",
    "failure_ceiling",
    "failure_ceiling_remaining",
    "retry_approved_by_fixture",
    "reverted",
    "dirty",
    "human_decision_required",
    "next_operator_action",
    "approval_id",
    "actor_identity",
    "command_executed",
    "file_read",
    "network_called",
    "source_mutated",
    "approval_captured",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_scanned",
}
_SIDE_EFFECT_FLAGS = [
    "command_executed",
    "file_read",
    "network_called",
    "source_mutated",
    "approval_captured",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_scanned",
]
_HEALTH_CHECK_PACKAGE_STATUS = "HEALTH_CHECK_ESCALATION_PACKAGE_ADVISORY_ONLY"
_HEALTH_CHECK_PACKAGE_AUTHORITY = "HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY"
_HEALTH_CHECK_ALLOWED_PROFILES = {
    "git_status_short_branch",
    "active_doctrine_gate",
    "python_unittest_discovery",
    "go_test_all",
    "go_vet_all",
}
_HEALTH_CHECK_CATEGORY_BY_STATUS = {
    "PASS_ADVISORY_ONLY": "ADVISORY_PASS",
    "FAIL_ADVISORY_ONLY": "FAILED_VERIFICATION_OR_BROKEN_CODE",
    "BLOCKED_ADVISORY_ONLY": "POLICY_OR_ENVIRONMENT_BLOCKED",
}
_HEALTH_CHECK_ALLOWED_KEYS = {
    "runner_status",
    "execution_status",
    "profile_id",
    "classification",
    "argv",
    "cwd",
    "status",
    "exit_code",
    "stdout_excerpt",
    "stderr_excerpt",
    "evidence_hash",
    "raw_output_embedded",
    "redaction_applied",
    "health_check_pass_grants_authority",
    "shell_used",
    "command_executed",
    "subprocess_started",
    "workspace_mode",
    "execution_workspace",
    "source_repo_is_execution_cwd",
    "isolated_workspace_path_inside_repo",
    "isolated_workspace_copy_excludes",
    "git_metadata_fixture",
    "git_metadata_source",
    "git_optional_locks_disabled",
    "git_dir_and_work_tree_explicit",
    "git_status_cwd_is_isolated_workspace",
    "dot_git_copied_to_isolated_workspace",
    "synthetic_git_history_created",
    "clone_or_worktree_setup_used",
    "side_effect_observation_scope",
    "workspace_status_changed",
    "repo_cache_artifacts_changed",
    "source_repo_status_changed",
    "source_repo_cache_artifacts_changed",
    "repo_cache_artifacts",
    "runner_temp_containment",
    "runner_temp_path_inside_repo",
    "runner_temp_removed",
    "isolated_workspace_removed",
    "process_group_timeout_cleanup",
    "network_called",
    "package_manager_called",
    "git_mutated",
    "source_mutated",
    "approval_captured",
    "protected_body_read",
    "active_vault_scanned",
    "beo_published",
    "rtm_generated",
    "drift_decision_made",
    "production_sandbox_enforced",
    "network_firewall_enforced",
    "host_secret_isolation_enforced",
    "production_authority_granted",
}
_NON_AUTHORIZING_STRING_PREFIXES = (
    "NO_",
    "NOT_",
    "WORKSPACE_STATUS_CHANGED",
    "REPO_CACHE_ARTIFACT_CHANGE_OBSERVED",
    "PROCESS_GROUP_",
)
_ALLOWED_WORKSPACE_MODES = {"source_repo", "isolated_copy"}
_ALLOWED_EXECUTION_WORKSPACES = {
    "SOURCE_REPOSITORY",
    "ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO",
    "GIT_STATUS_ISOLATED_METADATA_FIXTURE",
}
_ALLOWED_SIDE_EFFECT_SCOPES = {
    "GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY",
    "SOURCE_STATUS_AND_CACHE_PLUS_ISOLATED_WORKSPACE_COPY_ONLY",
}
_ALLOWED_CLASSIFICATIONS = {"ADVISORY_ONLY", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"}
_EXPECTED_EXECUTABLE_BASENAME = {
    "git_status_short_branch": "git",
    "active_doctrine_gate": "python3",
    "python_unittest_discovery": "python3",
    "go_test_all": "go",
    "go_vet_all": "go",
}
_EXPECTED_CLASSIFICATION = {
    "git_status_short_branch": "ADVISORY_ONLY",
    "active_doctrine_gate": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
    "python_unittest_discovery": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
    "go_test_all": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
    "go_vet_all": "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
}
_TRUSTED_EXECUTABLE_BY_PROFILE = {
    "git_status_short_branch": "/usr/bin/git",
    "active_doctrine_gate": "/usr/bin/python3.12",
    "python_unittest_discovery": "/usr/bin/python3.12",
    "go_test_all": "/home/dad/.local/opt/go/bin/go",
    "go_vet_all": "/home/dad/.local/opt/go/bin/go",
}
_BLK_SYSTEM_REPO = "/home/dad/BLK-System"
_ISOLATED_WORKSPACE_COPY_EXCLUDES = [".git", "docs/active", "docs/requirements", "docs/use_cases"]
_EXACT_HEALTH_CHECK_LABELS = {
    "git_metadata_fixture": {"GIT_STATUS_ISOLATED_METADATA_FIXTURE", "NOT_USED"},
    "git_metadata_source": {"SOURCE_GIT_METADATA_READ_ONLY", "NOT_USED"},
    "repo_cache_artifacts": {"NO_REPO_CACHE_ARTIFACT_CHANGE_OBSERVED", "REPO_CACHE_ARTIFACT_CHANGE_OBSERVED"},
    "runner_temp_containment": {"RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO"},
    "process_group_timeout_cleanup": {
        "PROCESS_GROUP_KILL_NOT_NEEDED",
        "PROCESS_GROUP_KILL_ATTEMPTED",
        "DIRECT_CHILD_KILL_FALLBACK",
    },
}
_EXACT_FALSE_FIELDS = {
    "clone_or_worktree_setup_used",
    "synthetic_git_history_created",
    "dot_git_copied_to_isolated_workspace",
    "runner_temp_path_inside_repo",
    "isolated_workspace_path_inside_repo",
}
_EXACT_CHANGE_FIELDS = {
    "workspace_status_changed",
    "source_repo_status_changed",
    "repo_cache_artifacts_changed",
    "source_repo_cache_artifacts_changed",
}
_EXACT_NON_AUTHORIZING_VALUES = {
    "network_called": {"NOT_MEASURED_BY_PILOT"},
    "package_manager_called": {"NOT_MEASURED_BY_PILOT"},
    "git_mutated": {"NO_WORKSPACE_STATUS_CHANGE_OBSERVED", "WORKSPACE_STATUS_CHANGED"},
    "source_mutated": {"NOT_MEASURED_BY_PILOT", "WORKSPACE_STATUS_CHANGED"},
    "protected_body_read": {"NOT_MEASURED_BY_PILOT"},
    "active_vault_scanned": {"NOT_MEASURED_BY_PILOT"},
    "beo_published": {"NOT_MEASURED_BY_PILOT"},
    "rtm_generated": {"NOT_MEASURED_BY_PILOT"},
    "drift_decision_made": {"NOT_MEASURED_BY_PILOT"},
    "production_sandbox_enforced": {"NOT_ENFORCED_BY_PILOT"},
    "network_firewall_enforced": {"NOT_ENFORCED_BY_PILOT"},
    "host_secret_isolation_enforced": {"NOT_ENFORCED_BY_PILOT"},
}
_SECRET_VALUE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"GITHUB_TOKEN\s*[=:]",
        r"API[_-]?KEY\s*[=:]",
        r"AWS_ACCESS_KEY_ID\s*[=:]",
        r"SECRET\s*[=:]",
        r"TOKEN\s*[=:]",
        r"PASSWORD\s*[=:]",
        r"PASSPHRASE\s*[=:]",
        r"Authorization:\s*(?:Bearer|Basic)\s+",
        r"SSH_AUTH_SOCK\s*[=:]",
        r"\.env\b",
        r"private[-_ ]?key",
    ]
]
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
    "beo",
    "blk_pipe",
    "blk_test",
    "body",
    "clone",
    "command",
    "content",
    "drift",
    "firewall",
    "host_secret",
    "ledger",
    "markdown",
    "path",
    "private",
    "protected",
    "publication",
    "published",
    "rtm",
    "secret",
    "setup",
    "shell",
    "signer",
    "sandbox",
    "text",
    "token",
    "vault",
    "worktree",
}


def build_operator_status_fixture(
    report: dict[str, Any], *, fixture_id: str, excerpt_max_chars: int = 320
) -> dict[str, Any]:
    """Build a bounded local operator status fixture from caller-supplied evidence."""

    fixture_id = _bounded_required_string(fixture_id, "fixture_id", MAX_ID_CHARS)
    if not isinstance(report, dict):
        raise ValueError("report must be a dictionary")
    _reject_forbidden_fields_recursive(report, "report", allowed_top_level=_REPORT_ALLOWED_KEYS)
    _reject_unsupported_fields(report, _REPORT_ALLOWED_KEYS, "report")
    _validate_excerpt_limit(excerpt_max_chars)

    failure_class = _bounded_required_string(report.get("failure_class"), "failure_class", MAX_ID_CHARS)
    if failure_class not in _CATALOG:
        raise ValueError(f"unsupported failure_class: {failure_class}")
    catalog = _CATALOG[failure_class]

    for flag in _SIDE_EFFECT_FLAGS:
        _required_false(report.get(flag, False), flag)

    retry_count = _required_int(report.get("retry_count"), "retry_count", minimum=0)
    failure_ceiling = _required_int(report.get("failure_ceiling"), "failure_ceiling", minimum=1)
    if retry_count > failure_ceiling:
        raise ValueError("retry_count cannot exceed failure_ceiling")

    reverted = _required_bool(report.get("reverted"), "reverted")
    dirty = _required_bool(report.get("dirty"), "dirty")
    _validate_class_indicators(failure_class, reverted=reverted, dirty=dirty)
    trace_artifacts = _trace_artifacts(report.get("trace_artifacts"))
    excerpt = _bounded_excerpt(
        _bounded_required_string(report.get("evidence_excerpt"), "evidence_excerpt", MAX_EXCERPT_CHARS),
        excerpt_max_chars,
    )
    remaining = failure_ceiling - retry_count

    output = {
        "fixture_id": fixture_id,
        "status_fixture": _STATUS_FIXTURE,
        "authority": _AUTHORITY,
        "failure_class": failure_class,
        "owning_domain": catalog["domain"],
        "concise_status": catalog["phrase"],
        "source_report_id": _bounded_required_string(
            report.get("source_report_id"), "source_report_id", MAX_ID_CHARS
        ),
        "beb_id": _bounded_required_string(report.get("beb_id"), "beb_id", MAX_ID_CHARS),
        "trace_artifacts": trace_artifacts,
        "raw_evidence_ref": _bounded_required_string(
            report.get("raw_evidence_ref"), "raw_evidence_ref", MAX_RAW_REF_CHARS
        ),
        "raw_evidence_hash": _required_hash(report.get("raw_evidence_hash"), "raw_evidence_hash"),
        "bounded_evidence_excerpt": excerpt,
        "evidence_inline_bounded": True,
        "raw_evidence_embedded": False,
        "retry_count": retry_count,
        "failure_ceiling": failure_ceiling,
        "failure_ceiling_remaining": remaining,
        "retry_approved_by_fixture": False,
        "reverted": reverted,
        "dirty": dirty,
        "human_decision_required": True,
        "next_operator_action": _operator_action(catalog["action"], remaining=remaining, dirty=dirty),
        "approval_id": _optional_bounded_string(report.get("approval_id"), "approval_id", MAX_ID_CHARS),
        "actor_identity": _optional_bounded_string(
            report.get("actor_identity"), "actor_identity", MAX_ID_CHARS
        ),
    }
    for flag in _SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_operator_escalation_package(
    statuses: list[dict[str, Any]], *, package_id: str
) -> dict[str, Any]:
    """Build a token-bounded local escalation package from status fixtures."""

    package_id = _bounded_required_string(package_id, "package_id", MAX_ID_CHARS)
    if not isinstance(statuses, list) or not statuses:
        raise ValueError("statuses must be a non-empty list")
    if len(statuses) > MAX_STATUS_COUNT:
        raise ValueError(f"too many statuses: maximum is {MAX_STATUS_COUNT}")
    normalized = [_validate_status_fixture(status) for status in statuses]
    total_excerpt_chars = sum(len(status["bounded_evidence_excerpt"]) for status in normalized)
    if total_excerpt_chars > MAX_TOTAL_PACKAGE_EXCERPT_CHARS:
        raise ValueError("package bounded excerpts exceed total size limit")
    output = {
        "package_id": package_id,
        "package_status": _PACKAGE_FIXTURE,
        "authority": _AUTHORITY,
        "status_count": len(normalized),
        "status_ids": [status["fixture_id"] for status in normalized],
        "failure_classes": [status["failure_class"] for status in normalized],
        "owning_domains": [status["owning_domain"] for status in normalized],
        "concise_statuses": [status["concise_status"] for status in normalized],
        "human_decision_required": any(status["human_decision_required"] for status in normalized),
        "next_operator_actions": [status["next_operator_action"] for status in normalized],
        "raw_evidence_refs": [status["raw_evidence_ref"] for status in normalized],
        "raw_evidence_hashes": [status["raw_evidence_hash"] for status in normalized],
        "bounded_evidence_excerpts": [status["bounded_evidence_excerpt"] for status in normalized],
        "raw_evidence_embedded": False,
    }
    for flag in _SIDE_EFFECT_FLAGS:
        output[flag] = False
    return output


def build_health_check_escalation_package(
    results: list[dict[str, Any]], *, package_id: str
) -> dict[str, Any]:
    """Build a bounded advisory package from already-returned health-check results.

    This helper is a pure dictionary normalizer. It does not start subprocesses,
    inspect files, call Git, call network services, or mutate source.
    """

    package_id = _bounded_required_string(package_id, "package_id", MAX_ID_CHARS)
    if not isinstance(results, list) or not results:
        raise ValueError("health-check results must be a non-empty list")
    if len(results) > MAX_HEALTH_CHECK_RESULT_COUNT:
        raise ValueError(f"too many health-check results: maximum is {MAX_HEALTH_CHECK_RESULT_COUNT}")

    normalized = [_validate_health_check_result(result) for result in results]
    total_excerpt_chars = sum(
        len(result["stdout_excerpt"]) + len(result["stderr_excerpt"]) for result in normalized
    )
    if total_excerpt_chars > MAX_TOTAL_HEALTH_CHECK_EXCERPT_CHARS:
        raise ValueError("health-check package excerpts exceed total size limit")
    statuses = [result["status"] for result in normalized]
    human_decision_required = any(status != "PASS_ADVISORY_ONLY" for status in statuses)
    if human_decision_required:
        next_action = (
            "inspect failed or blocked health-check evidence; no retry or authority expansion is approved by this package"
        )
    else:
        next_action = (
            "health-check PASS is advisory only; no execution, publication, RTM, drift, protected-vault, "
            "Git mutation, or production authority is granted"
        )
    return {
        "package_id": package_id,
        "package_status": _HEALTH_CHECK_PACKAGE_STATUS,
        "authority": _HEALTH_CHECK_PACKAGE_AUTHORITY,
        "result_count": len(normalized),
        "profile_ids": [result["profile_id"] for result in normalized],
        "advisory_statuses": statuses,
        "failure_categories": [_HEALTH_CHECK_CATEGORY_BY_STATUS[status] for status in statuses],
        "exit_codes": [result["exit_code"] for result in normalized],
        "evidence_hashes": [result["evidence_hash"] for result in normalized],
        "stdout_excerpts": [result["stdout_excerpt"] for result in normalized],
        "stderr_excerpts": [result["stderr_excerpt"] for result in normalized],
        "workspace_modes": [result.get("workspace_mode") for result in normalized],
        "execution_workspaces": [result.get("execution_workspace") for result in normalized],
        "side_effect_observation_scopes": [
            result.get("side_effect_observation_scope") for result in normalized
        ],
        "human_decision_required": human_decision_required,
        "next_operator_action": next_action,
        "raw_evidence_embedded": False,
        "health_check_pass_grants_authority": False,
        "production_authority_granted": False,
        "subprocess_started_by_package_helper": False,
        "no_new_profile_ids": True,
    }


def _validate_health_check_result(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise ValueError("health-check result must be a dictionary")
    _reject_forbidden_fields_recursive(result, "health-check result", allowed_top_level=_HEALTH_CHECK_ALLOWED_KEYS)
    _reject_secret_values_recursive(result, "health-check result")
    _reject_unsupported_fields(result, _HEALTH_CHECK_ALLOWED_KEYS, "health-check result")

    profile_id = _bounded_required_string(result.get("profile_id"), "profile_id", MAX_ID_CHARS)
    if profile_id not in _HEALTH_CHECK_ALLOWED_PROFILES:
        raise ValueError(f"unknown health-check profile: {profile_id}")
    status = _bounded_required_string(result.get("status"), "status", MAX_ID_CHARS)
    if status not in _HEALTH_CHECK_CATEGORY_BY_STATUS:
        raise ValueError(f"unsupported health-check status: {status}")
    if result.get("runner_status") != "HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY":
        raise ValueError("runner_status must be HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY")
    if result.get("execution_status") != "HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE":
        raise ValueError("execution_status must be HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE")
    classification = _optional_allowed_string(result.get("classification"), "classification", _ALLOWED_CLASSIFICATIONS)
    if classification != _EXPECTED_CLASSIFICATION[profile_id]:
        raise ValueError("classification does not match fixed profile")
    if result.get("raw_output_embedded") is not False:
        raise ValueError("raw_output_embedded must be false")
    _required_bool(result.get("redaction_applied"), "redaction_applied")
    if result.get("health_check_pass_grants_authority") is not False:
        raise ValueError("health_check_pass_grants_authority must be false")
    if result.get("production_authority_granted") is not False:
        raise ValueError("production_authority_granted must be false")
    if result.get("shell_used") is not False:
        raise ValueError("shell_used must be false")
    if result.get("command_executed") is not True:
        raise ValueError("command_executed must be true for runner evidence")
    if result.get("subprocess_started") is not True:
        raise ValueError("subprocess_started must be true for runner evidence")
    git_metadata_argv = _validate_health_check_argv(profile_id, result.get("argv"))
    cwd = _validate_health_check_cwd(result.get("cwd"))
    for field in [
        "source_repo_is_execution_cwd",
        "git_optional_locks_disabled",
        "git_dir_and_work_tree_explicit",
        "git_status_cwd_is_isolated_workspace",
        "runner_temp_removed",
        "isolated_workspace_removed",
    ]:
        if field in result:
            _required_bool(result.get(field), field)
    if "isolated_workspace_copy_excludes" in result and result.get("isolated_workspace_copy_excludes") != _ISOLATED_WORKSPACE_COPY_EXCLUDES:
        raise ValueError("isolated_workspace_copy_excludes must match fixed excluded path list")
    for field in _EXACT_FALSE_FIELDS:
        _required_false(result.get(field, False), field)

    exit_code = result.get("exit_code")
    if exit_code is not None and (not isinstance(exit_code, int) or isinstance(exit_code, bool)):
        raise ValueError("exit_code must be an integer or null")
    stdout_excerpt = _bounded_string_allow_empty(
        result.get("stdout_excerpt", ""), "stdout_excerpt", MAX_HEALTH_CHECK_EXCERPT_CHARS
    )
    stderr_excerpt = _bounded_string_allow_empty(
        result.get("stderr_excerpt", ""), "stderr_excerpt", MAX_HEALTH_CHECK_EXCERPT_CHARS
    )
    _reject_secret_looking_value(stdout_excerpt, "stdout_excerpt")
    _reject_secret_looking_value(stderr_excerpt, "stderr_excerpt")
    evidence_hash = _required_hash(result.get("evidence_hash"), "evidence_hash")
    for field in [
        "network_called",
        "package_manager_called",
        "git_mutated",
        "source_mutated",
        "protected_body_read",
        "active_vault_scanned",
        "beo_published",
        "rtm_generated",
        "drift_decision_made",
        "production_sandbox_enforced",
        "network_firewall_enforced",
        "host_secret_isolation_enforced",
    ]:
        _required_non_authorizing_value(result.get(field), field)
    for field, claim in [("git_mutated", result.get("git_mutated")), ("source_mutated", result.get("source_mutated"))]:
        if claim == "WORKSPACE_STATUS_CHANGED" and status != "BLOCKED_ADVISORY_ONLY":
            raise ValueError(f"{field} change claims require BLOCKED_ADVISORY_ONLY")
    for field in _EXACT_CHANGE_FIELDS:
        claim = result.get(field, False)
        if not isinstance(claim, bool):
            raise ValueError(f"{field} must be bool")
        if claim is True and status != "BLOCKED_ADVISORY_ONLY":
            raise ValueError(f"{field} change claims require BLOCKED_ADVISORY_ONLY")
    repo_cache_artifacts_changed = result.get("repo_cache_artifacts_changed", False)
    source_repo_cache_artifacts_changed = result.get("source_repo_cache_artifacts_changed", False)
    repo_cache_artifacts = result.get("repo_cache_artifacts")
    cache_artifacts_changed = repo_cache_artifacts_changed or source_repo_cache_artifacts_changed
    if repo_cache_artifacts_changed is True and repo_cache_artifacts == "NO_REPO_CACHE_ARTIFACT_CHANGE_OBSERVED":
        raise ValueError("repo_cache_artifacts_changed contradicts repo_cache_artifacts")
    if source_repo_cache_artifacts_changed is True and repo_cache_artifacts == "NO_REPO_CACHE_ARTIFACT_CHANGE_OBSERVED":
        raise ValueError("cache artifact change evidence contradicts repo_cache_artifacts")
    if cache_artifacts_changed is False and repo_cache_artifacts == "REPO_CACHE_ARTIFACT_CHANGE_OBSERVED":
        raise ValueError("repo_cache_artifacts_changed contradicts repo_cache_artifacts")
    if result.get("git_mutated") == "WORKSPACE_STATUS_CHANGED" and not result.get("workspace_status_changed"):
        raise ValueError("git/source mutation claim requires status-change evidence")
    if result.get("source_mutated") == "WORKSPACE_STATUS_CHANGED" and not result.get("source_repo_status_changed"):
        raise ValueError("git/source mutation claim requires status-change evidence")
    if result.get("workspace_status_changed") is True and result.get("git_mutated") != "WORKSPACE_STATUS_CHANGED":
        raise ValueError("workspace status-change evidence contradicts git_mutated")
    if result.get("source_repo_status_changed") is True and result.get("source_mutated") != "WORKSPACE_STATUS_CHANGED":
        raise ValueError("source status-change evidence contradicts source_mutated")
    for field, allowed in _EXACT_HEALTH_CHECK_LABELS.items():
        if field in result:
            _optional_allowed_string(result.get(field), field, allowed)
    for field in ["approval_captured"]:
        _required_false(result.get(field), field)
    workspace_mode = _optional_allowed_string(
        result.get("workspace_mode"), "workspace_mode", _ALLOWED_WORKSPACE_MODES
    )
    if workspace_mode is None:
        raise ValueError("workspace_mode is required")
    execution_workspace = _optional_allowed_string(
        result.get("execution_workspace"),
        "execution_workspace",
        _ALLOWED_EXECUTION_WORKSPACES,
    )
    if execution_workspace is None:
        raise ValueError("execution_workspace is required")
    side_effect_observation_scope = _optional_allowed_string(
        result.get("side_effect_observation_scope"),
        "side_effect_observation_scope",
        _ALLOWED_SIDE_EFFECT_SCOPES,
    )
    if side_effect_observation_scope is None:
        raise ValueError("side_effect_observation_scope is required")
    _validate_health_check_workspace_relationships(
        profile_id,
        cwd=cwd,
        workspace_mode=workspace_mode,
        execution_workspace=execution_workspace,
        git_metadata_argv=git_metadata_argv,
        result=result,
    )
    return {
        "profile_id": profile_id,
        "status": status,
        "exit_code": exit_code,
        "stdout_excerpt": stdout_excerpt,
        "stderr_excerpt": stderr_excerpt,
        "evidence_hash": evidence_hash,
        "workspace_mode": workspace_mode,
        "execution_workspace": execution_workspace,
        "side_effect_observation_scope": side_effect_observation_scope,
    }


def _validate_status_fixture(status: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(status, dict):
        raise ValueError("status must be a dictionary")
    _reject_forbidden_fields_recursive(status, "status", allowed_top_level=_STATUS_ALLOWED_KEYS)
    _reject_unsupported_fields(status, _STATUS_ALLOWED_KEYS, "status")
    if status.get("status_fixture") != _STATUS_FIXTURE:
        raise ValueError("status_fixture must be OPERATOR_OBSERVABILITY_FIXTURE_ONLY")
    if status.get("authority") != _AUTHORITY:
        raise ValueError("status authority must be OBSERVABILITY_ONLY_NOT_EXECUTION")
    failure_class = _bounded_required_string(status.get("failure_class"), "failure_class", MAX_ID_CHARS)
    if failure_class not in _CATALOG:
        raise ValueError("status failure_class is unsupported")
    catalog = _CATALOG[failure_class]
    if status.get("owning_domain") != catalog["domain"]:
        raise ValueError("owning_domain does not match failure_class")
    if status.get("concise_status") != catalog["phrase"]:
        raise ValueError("concise_status does not match failure_class")
    _bounded_required_string(status.get("fixture_id"), "fixture_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("source_report_id"), "source_report_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("beb_id"), "beb_id", MAX_ID_CHARS)
    _bounded_required_string(status.get("raw_evidence_ref"), "raw_evidence_ref", MAX_RAW_REF_CHARS)
    _required_hash(status.get("raw_evidence_hash"), "raw_evidence_hash")
    excerpt = _bounded_required_string(
        status.get("bounded_evidence_excerpt"), "bounded_evidence_excerpt", MAX_EXCERPT_CHARS
    )
    if len(excerpt) > MAX_EXCERPT_CHARS:
        raise ValueError(f"bounded_evidence_excerpt must be at most {MAX_EXCERPT_CHARS} characters")
    if status.get("evidence_inline_bounded") is not True:
        raise ValueError("evidence_inline_bounded must be true")
    if status.get("raw_evidence_embedded") is not False:
        raise ValueError("raw_evidence_embedded must be false")
    retry_count = _required_int(status.get("retry_count"), "retry_count", minimum=0)
    failure_ceiling = _required_int(status.get("failure_ceiling"), "failure_ceiling", minimum=1)
    remaining = _required_int(status.get("failure_ceiling_remaining"), "failure_ceiling_remaining", minimum=0)
    if retry_count > failure_ceiling or remaining != failure_ceiling - retry_count:
        raise ValueError("failure ceiling fields are inconsistent")
    if status.get("retry_approved_by_fixture") is not False:
        raise ValueError("retry_approved_by_fixture must be false")
    reverted = _required_bool(status.get("reverted"), "reverted")
    dirty = _required_bool(status.get("dirty"), "dirty")
    _validate_class_indicators(failure_class, reverted=reverted, dirty=dirty)
    if status.get("human_decision_required") is not True:
        raise ValueError("human_decision_required must be true")
    expected_action = _operator_action(catalog["action"], remaining=remaining, dirty=dirty)
    if status.get("next_operator_action") != expected_action:
        raise ValueError("next_operator_action does not match failure_class and indicators")
    _trace_artifacts(status.get("trace_artifacts"))
    _optional_bounded_string(status.get("approval_id"), "approval_id", MAX_ID_CHARS)
    _optional_bounded_string(status.get("actor_identity"), "actor_identity", MAX_ID_CHARS)
    for flag in _SIDE_EFFECT_FLAGS:
        _required_false(status.get(flag), flag)
    return deepcopy(status)


def _trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    if len(value) > MAX_TRACE_ARTIFACTS:
        raise ValueError(f"trace_artifacts must contain at most {MAX_TRACE_ARTIFACTS} entries")
    out: list[dict[str, str]] = []
    identities: set[tuple[str, str]] = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("trace_artifacts entries must be dictionaries")
        _reject_forbidden_fields_recursive(item, "trace_artifacts", allowed_top_level=_TRACE_ALLOWED_KEYS)
        _reject_unsupported_fields(item, _TRACE_ALLOWED_KEYS, "trace_artifacts")
        kind = _bounded_required_string(item.get("kind"), "kind", MAX_ID_CHARS)
        artifact_id = _bounded_required_string(item.get("id"), "id", MAX_ID_CHARS)
        identity = (kind, artifact_id)
        if identity in identities:
            raise ValueError(f"duplicate trace identity: {kind}:{artifact_id}")
        identities.add(identity)
        out.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": _required_hash(item.get("version_hash"), "version_hash"),
            }
        )
    return out


def _validate_class_indicators(failure_class: str, *, reverted: bool, dirty: bool) -> None:
    if failure_class == "DIRTY_WORKSPACE" and dirty is not True:
        raise ValueError("DIRTY_WORKSPACE requires dirty true")
    if failure_class == "UNAUTHORIZED_MUTATION" and reverted is not True:
        raise ValueError("UNAUTHORIZED_MUTATION requires reverted true")


def _operator_action(base_action: str, *, remaining: int, dirty: bool) -> str:
    if remaining == 0:
        return "stop and escalate; failure ceiling reached; no retry is approved by this fixture"
    if dirty:
        return "inspect workspace before retry"
    return base_action


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
    return value


def _bounded_required_string(value: Any, field: str, max_chars: int) -> str:
    value = _required_string(value, field)
    if len(value) > max_chars:
        raise ValueError(f"{field} must be at most {max_chars} characters")
    return value


def _bounded_string_allow_empty(value: Any, field: str, max_chars: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if len(value) > max_chars:
        raise ValueError(f"{field} must be at most {max_chars} characters")
    return value


def _optional_bounded_string(value: Any, field: str, max_chars: int) -> str | None:
    if value is None:
        return None
    return _bounded_required_string(value, field, max_chars)


def _required_hash(value: Any, field: str) -> str:
    value = _required_string(value, field)
    if not _HASH_RE.match(value):
        raise ValueError(f"{field} must be sha256:<64 lowercase hex>")
    return value


def _required_int(value: Any, field: str, *, minimum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")
    return value


def _required_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be bool")
    return value


def _required_false(value: Any, field: str) -> None:
    if value is not False:
        raise ValueError(f"{field} must be false")


def _validate_health_check_argv(profile_id: str, value: Any) -> bool:
    if not isinstance(value, (list, tuple)) or not value:
        raise ValueError("argv must be a non-empty fixed profile argv list")
    argv = [_bounded_required_string(item, "argv item", MAX_RAW_REF_CHARS) for item in value]
    for item in argv:
        _reject_secret_looking_value(item, "argv")
        if _has_forbidden_runtime_text(item):
            raise ValueError("argv does not match fixed profile")
    executable = argv[0].rsplit("/", 1)[-1]
    if not _matches_profile_executable(executable, _EXPECTED_EXECUTABLE_BASENAME[profile_id]):
        raise ValueError("argv executable does not match fixed profile")
    if not _is_trusted_executable_path(profile_id, argv[0]):
        raise ValueError("argv executable path is not trusted")
    tail = tuple(argv[1:])
    allowed_tails = {
        "git_status_short_branch": {
            ("status", "--short", "--branch"),
        },
        "active_doctrine_gate": {
            ("-m", "unittest", "python.test_active_doctrine_review_gates"),
        },
        "python_unittest_discovery": {
            ("-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"),
        },
        "go_test_all": {("test", "./...")},
        "go_vet_all": {("vet", "./...")},
    }
    git_metadata_tail = (
        len(argv) == 8
        and argv[1] == "--git-dir"
        and argv[3] == "--work-tree"
        and tuple(argv[5:]) == ("status", "--short", "--branch")
    )
    if profile_id == "git_status_short_branch" and git_metadata_tail:
        git_dir = argv[2]
        work_tree = argv[4]
        if git_dir != f"{_BLK_SYSTEM_REPO}/.git" or work_tree != _BLK_SYSTEM_REPO:
            raise ValueError("argv Git-metadata paths do not match BLK-System source repository")
        return True
    if tail not in allowed_tails[profile_id]:
        raise ValueError("argv does not match fixed profile")
    return False


def _is_trusted_executable_path(profile_id: str, value: str) -> bool:
    return value == _TRUSTED_EXECUTABLE_BY_PROFILE[profile_id]


def _matches_profile_executable(executable: str, expected: str) -> bool:
    if expected == "python3":
        return executable == "python3" or re.fullmatch(r"python3\.\d+", executable) is not None
    return executable == expected


def _optional_allowed_string(value: Any, field: str, allowed: set[str]) -> str | None:
    if value is None:
        return None
    value = _bounded_required_string(value, field, MAX_RAW_REF_CHARS)
    if value not in allowed:
        raise ValueError(f"{field} is not an allowed advisory label")
    return value


def _validate_health_check_cwd(value: Any) -> str | None:
    if value is None:
        return None
    cwd = _bounded_required_string(value, "cwd", MAX_RAW_REF_CHARS)
    cwd = posixpath.normpath(cwd)
    _reject_secret_looking_value(cwd, "cwd")
    if _has_forbidden_authority_text(cwd):
        raise ValueError("cwd contains forbidden authority text")
    return cwd


def _validate_health_check_workspace_relationships(
    profile_id: str,
    *,
    cwd: str | None,
    workspace_mode: str | None,
    execution_workspace: str | None,
    git_metadata_argv: bool,
    result: dict[str, Any],
) -> None:
    if execution_workspace == "GIT_STATUS_ISOLATED_METADATA_FIXTURE" and profile_id != "git_status_short_branch":
        raise ValueError("Git metadata execution workspace is only valid for Git status profile")
    if workspace_mode == "source_repo":
        if git_metadata_argv:
            raise ValueError("Git metadata argv contradicts source workspace")
        if execution_workspace != "SOURCE_REPOSITORY":
            raise ValueError("execution_workspace contradicts workspace_mode")
        if cwd is None:
            raise ValueError("cwd is required for source workspace")
        if cwd != _BLK_SYSTEM_REPO:
            raise ValueError("cwd must match source repository for source workspace")
        if "source_repo_is_execution_cwd" not in result or result.get("source_repo_is_execution_cwd") is not True:
            raise ValueError("source_repo_is_execution_cwd contradicts source workspace")
        if result.get("side_effect_observation_scope") != "GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY":
            raise ValueError("side_effect_observation_scope contradicts source workspace")
        if result.get("git_metadata_fixture") != "NOT_USED" or result.get("git_metadata_source") != "NOT_USED":
            raise ValueError("Git metadata fixture labels are only valid for Git status profile")
        if result.get("git_optional_locks_disabled") is not False:
            raise ValueError("git_optional_locks_disabled contradicts source workspace")
        if result.get("git_dir_and_work_tree_explicit") is not False:
            raise ValueError("git_dir_and_work_tree_explicit contradicts source workspace")
        if result.get("git_status_cwd_is_isolated_workspace") is not False:
            raise ValueError("git_status_cwd_is_isolated_workspace contradicts source workspace")
    if execution_workspace == "GIT_STATUS_ISOLATED_METADATA_FIXTURE" and profile_id != "git_status_short_branch":
        raise ValueError("Git metadata execution workspace is only valid for Git status profile")
    if (
        result.get("git_metadata_fixture") == "GIT_STATUS_ISOLATED_METADATA_FIXTURE"
        or result.get("git_metadata_source") == "SOURCE_GIT_METADATA_READ_ONLY"
    ) and profile_id != "git_status_short_branch":
        raise ValueError("Git metadata fixture labels are only valid for Git status profile")
    if workspace_mode == "isolated_copy":
        if cwd is None or "/blk-system-health-check-" not in cwd or not cwd.endswith("/isolated-workspace"):
            raise ValueError("cwd must match isolated workspace for isolated workspace mode")
        if cwd.startswith(f"{_BLK_SYSTEM_REPO}/") or cwd == _BLK_SYSTEM_REPO:
            raise ValueError("cwd must not be inside source repository for isolated workspace mode")
        if result.get("source_repo_is_execution_cwd") is not False:
            raise ValueError("source_repo_is_execution_cwd contradicts isolated workspace")
        if "isolated_workspace_copy_excludes" not in result:
            raise ValueError("isolated_workspace_copy_excludes is required for isolated workspace mode")
        if result.get("isolated_workspace_copy_excludes") != _ISOLATED_WORKSPACE_COPY_EXCLUDES:
            raise ValueError("isolated_workspace_copy_excludes must match fixed excluded path list")
        if result.get("side_effect_observation_scope") != "SOURCE_STATUS_AND_CACHE_PLUS_ISOLATED_WORKSPACE_COPY_ONLY":
            raise ValueError("side_effect_observation_scope contradicts isolated workspace")
        if profile_id == "git_status_short_branch":
            if execution_workspace != "GIT_STATUS_ISOLATED_METADATA_FIXTURE":
                raise ValueError("execution_workspace contradicts workspace_mode")
            if not git_metadata_argv:
                raise ValueError("Git metadata argv is required for Git status isolated metadata mode")
            if (
                result.get("git_metadata_fixture") != "GIT_STATUS_ISOLATED_METADATA_FIXTURE"
                or result.get("git_metadata_source") != "SOURCE_GIT_METADATA_READ_ONLY"
                or result.get("git_optional_locks_disabled") is not True
                or result.get("git_dir_and_work_tree_explicit") is not True
                or result.get("git_status_cwd_is_isolated_workspace") is not True
            ):
                raise ValueError("Git metadata fixture labels must match Git status isolated metadata mode")
        elif execution_workspace != "ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO":
            raise ValueError("execution_workspace contradicts workspace_mode")


def _reject_secret_values_recursive(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for nested in value.values():
            _reject_secret_values_recursive(nested, context)
    elif isinstance(value, list):
        for nested in value:
            _reject_secret_values_recursive(nested, context)
    elif isinstance(value, str):
        for pattern in _SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                raise ValueError(f"{context} contains secret-looking value")


def _reject_secret_looking_value(value: str, field: str) -> None:
    for pattern in _SECRET_VALUE_PATTERNS:
        if pattern.search(value):
            raise ValueError(f"{field} contains secret-looking value")


def _has_forbidden_runtime_text(value: str) -> bool:
    lowered = value.lower()
    exact_forbidden = {"sh", "bash", "zsh", "fish", "curl", "wget", "ssh", "scp", "nc", "npm", "pip", "pip3"}
    basename = lowered.rsplit("/", 1)[-1]
    if lowered in exact_forbidden or basename in exact_forbidden:
        return True
    forbidden_substrings = [
        "pip install",
        "npm install",
        "go get",
        "http://",
        "https://",
        "--eval",
    ]
    return any(token in lowered for token in forbidden_substrings)


def _has_forbidden_authority_text(value: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    tokens = {part for part in normalized.split("_") if part}
    forbidden = {
        "active",
        "body",
        "drift",
        "ledger",
        "private",
        "protected",
        "publication",
        "published",
        "rtm",
        "secret",
        "signer",
        "vault",
    }
    return bool(tokens & forbidden)


def _required_non_authorizing_value(value: Any, field: str) -> None:
    if value is False:
        return
    if field in _EXACT_NON_AUTHORIZING_VALUES and isinstance(value, str) and value in _EXACT_NON_AUTHORIZING_VALUES[field]:
        return
    raise ValueError(f"{field} must remain an exact non-authorizing value")
