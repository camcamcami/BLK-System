"""BLK-SYSTEM-047 BLK-test L4 real-repo approval-boundary helpers.

This module is intentionally preflight-only. It can prove that an exact-target L4
approval envelope is internally complete, but it cannot execute BLK-test runtime
against a real repository in this sprint.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

SPRINT = "BLK-SYSTEM-047"
APPROVAL_KIND = "blk-test-fixed-tool-pilot-l4-real-repo-readonly"
APPROVAL_CHECKPOINT = "EXPLICIT_BLK_SYSTEM_047_L4_REAL_REPO_APPROVAL_BOUNDARY_RECORDED"
REQUESTED_TOOL = "run_ast_validation"
PREFLIGHT_READY = "BLK_TEST_L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED"
BLOCKED = "L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL"
WORKSPACE_MARKER_FILE = ".blk-system-047-l4-workspace"
PRIMARY_REPO_ROOT = Path("/home/dad/BLK-System").resolve()
PROTECTED_PREFIX_PARTS = (
    ("docs", "active"),
    ("docs", "requirements"),
    ("docs", "use_cases"),
)
HOST_SECRET_PARTS = frozenset({".ssh", ".env", ".aws", ".gnupg", "credentials", "secrets", "tokens"})

REQUEST_KEYS = frozenset(
    {
        "source_evidence",
        "requested_tool",
        "test_profile",
        "target_identity",
        "workspace_identity",
        "timeout_output_profile",
        "exact_target_approval",
        "read_only_approval",
        "fixed_tool_executed",
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
        "active_vault_read",
        "beo_publication",
        "rtm_status",
        "network_called",
        "model_service_called",
        "browser_tooling_called",
        "cyber_tooling_called",
        "package_manager_called",
        "arbitrary_shell_called",
        "subprocess_called",
    }
)
APPROVAL_KEYS = frozenset(
    {
        "approval_kind",
        "approval_id",
        "operator_identity",
        "approval_timestamp",
        "issued_at",
        "expires_at",
        "source_system",
        "source_evidence",
        "requested_tool",
        "test_profile",
        "target_identity",
        "workspace_identity",
        "timeout_output_profile",
        "sprint047_l4_approval",
    }
)
EXTENSION_KEYS = frozenset(
    {
        "run_id",
        "approved_runtime_slice",
        "target_identity",
        "workspace_identity",
        "timeout_output_profile",
        "implementation_commit_hash",
        "driver_hash",
        "cleanup_obligations",
        "rollback_obligations",
        "operator_stop_control",
        "hostile_review_criteria",
        "excluded_authorities",
        "envelope_hash",
    }
)
TARGET_IDENTITY_KEYS = frozenset(
    {
        "approved_repo_path",
        "approved_source_subtree",
        "approved_branch",
        "approved_worktree_id",
    }
)
WORKSPACE_IDENTITY_KEYS = frozenset(
    {
        "approved_workspace_path",
        "workspace_clone_id",
        "workspace_marker_nonce",
        "source_path_policy",
    }
)
TIMEOUT_OUTPUT_PROFILE_KEYS = frozenset({"timeout_class", "timeout_seconds", "output_byte_limit", "compression"})
FALSE_FIELDS = frozenset(
    {
        "fixed_tool_executed",
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
        "active_vault_read",
        "network_called",
        "model_service_called",
        "browser_tooling_called",
        "cyber_tooling_called",
        "package_manager_called",
        "arbitrary_shell_called",
        "subprocess_called",
    }
)
REQUIRED_EXCLUDED_AUTHORITIES = frozenset(
    {
        "production_blktest_mcp",
        "generic_blktest_mcp",
        "arbitrary_shell",
        "source_mutation",
        "git_mutation",
        "protected_body_reads",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "network_model_browser_cyber_package_tooling",
        "production_isolation_claims",
    }
)
AUTHORITY_TEXT_MARKERS = (
    "codex",
    "blk pipe",
    "blk-pipe",
    "beo",
    "publication approved",
    "publish approved",
    "rtm",
    "drift",
    "coverage truth",
    "protected body",
    "protected_body",
    "docs/active",
    "docs/requirements",
    "docs/use_cases",
    "source mutation",
    "source_mutation",
    "source write",
    "git mutation",
    "commit approved",
    "push approved",
    "stage approved",
    "shell",
    "command",
    "network",
    "model service",
    "browser",
    "cyber",
    "package manager",
    "production isolation",
    "sandbox enforced",
    "runtime approved",
    "approved for live execution",
    "live execution approved",
)


def build_sprint047_l4_source_report(
    *,
    report_path: str,
    beb_id: str,
    commit_hash: str,
    pre_engine_hash: str,
) -> dict[str, Any]:
    return {
        "status": "SUCCESS",
        "source_report_identity": {
            "report_path": report_path,
            "report_hash": "sha256:" + "4" * 64,
            "report_id": "source-report-BLK-SYSTEM-047-l4-approval-boundary",
        },
        "beb_id": beb_id,
        "commit_hash": commit_hash,
        "pre_engine_hash": pre_engine_hash,
        "trace_artifacts": [
            {
                "kind": "REQ",
                "id": "REQ-S47-BLK-TEST-L4-APPROVAL-001",
                "version_hash": "sha256:" + "5" * 64,
            }
        ],
    }


def build_sprint047_l4_approval_request(
    *,
    source_report: dict[str, Any],
    target_identity: dict[str, Any],
    workspace_identity: dict[str, Any],
    timeout_output_profile: dict[str, Any],
) -> dict[str, Any]:
    request = {
        "source_evidence": deepcopy(source_report),
        "requested_tool": REQUESTED_TOOL,
        "test_profile": "blk-test-l4-real-repo-readonly-fixed-tool",
        "target_identity": deepcopy(target_identity),
        "workspace_identity": deepcopy(workspace_identity),
        "timeout_output_profile": deepcopy(timeout_output_profile),
        "exact_target_approval": True,
        "read_only_approval": True,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    request.update(_false_authority_fields())
    return request


def build_sprint047_l4_approval_record(
    *,
    authorization_request: dict[str, Any],
    approval_id: str,
    run_id: str,
    operator_identity: str,
    source_system: str,
    issued_at: str,
    expires_at: str,
    implementation_commit_hash: str,
    driver_hash: str,
) -> dict[str, Any]:
    extension = {
        "run_id": run_id,
        "approved_runtime_slice": "L4_REAL_REPO_PREFLIGHT_READY_NOT_EXECUTED_THIS_SPRINT",
        "target_identity": deepcopy(authorization_request["target_identity"]),
        "workspace_identity": deepcopy(authorization_request["workspace_identity"]),
        "timeout_output_profile": deepcopy(authorization_request["timeout_output_profile"]),
        "implementation_commit_hash": implementation_commit_hash,
        "driver_hash": driver_hash,
        "cleanup_obligations": ["workspace marker must match before cleanup", "no target repository cleanup by BLK-test"],
        "rollback_obligations": ["read-only pilot requires no source rollback", "source and git mutation remain forbidden"],
        "operator_stop_control": "future fixed-harness process-group timeout kill; not invoked in BLK-SYSTEM-047",
        "hostile_review_criteria": [
            "exact target identity must match",
            "replay and expiry must fail closed",
            "preflight readiness must not execute runtime",
        ],
        "excluded_authorities": sorted(REQUIRED_EXCLUDED_AUTHORITIES),
    }
    extension["envelope_hash"] = sprint047_l4_envelope_hash(
        authorization_request=authorization_request,
        run_id=run_id,
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    return {
        "approval_kind": APPROVAL_KIND,
        "approval_id": approval_id,
        "operator_identity": operator_identity,
        "approval_timestamp": issued_at,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "source_system": source_system,
        "source_evidence": deepcopy(authorization_request["source_evidence"]),
        "requested_tool": authorization_request["requested_tool"],
        "test_profile": authorization_request["test_profile"],
        "target_identity": deepcopy(authorization_request["target_identity"]),
        "workspace_identity": deepcopy(authorization_request["workspace_identity"]),
        "timeout_output_profile": deepcopy(authorization_request["timeout_output_profile"]),
        "sprint047_l4_approval": extension,
    }


def sprint047_l4_envelope_hash(
    *,
    authorization_request: dict[str, Any],
    run_id: str,
    implementation_commit_hash: str,
    driver_hash: str,
) -> str:
    return _stable_hash(
        {
            "sprint": SPRINT,
            "authorization_request_hash": _stable_hash(authorization_request),
            "source_evidence_hash": _stable_hash(authorization_request.get("source_evidence")),
            "target_identity": authorization_request.get("target_identity"),
            "workspace_identity": authorization_request.get("workspace_identity"),
            "timeout_output_profile": authorization_request.get("timeout_output_profile"),
            "requested_tool": REQUESTED_TOOL,
            "run_id": run_id,
            "implementation_commit_hash": implementation_commit_hash,
            "driver_hash": driver_hash,
            "runtime": PREFLIGHT_READY,
        }
    )


def evaluate_l4_missing_exact_target_preflight(
    *,
    target_repo_path: str | Path,
    requested_tool: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
) -> dict[str, Any]:
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    return {
        "pilot_status": BLOCKED,
        "target_repo_path": str(target_repo_path),
        "requested_tool": requested_tool,
        "blocked_reason": "complete exact L4 target approval envelope required",
        "fixed_tool_executed": False,
        "source_mutation_attempted": False,
        "git_mutation_attempted": False,
        "protected_body_read_attempted": False,
        "beo_publication_attempted": False,
        "rtm_generation_attempted": False,
        "drift_rejection_attempted": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "package_manager_called": False,
        "arbitrary_shell_called": False,
        "production_isolation_claimed": False,
        **_false_authority_fields(),
    }


def evaluate_blk_test_l4_real_repo_preflight(
    *,
    authorization_request: dict[str, Any],
    approval_record: dict[str, Any],
    requested_tool: str,
    run_id: str,
    now: str,
    pilot_enabled: bool,
    human_approval_checkpoint: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_path: str | Path,
    implementation_commit_hash: str,
    driver_hash: str,
) -> dict[str, Any]:
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    if requested_tool != REQUESTED_TOOL:
        raise ValueError("requested_tool must be run_ast_validation")
    if pilot_enabled is not False:
        raise ValueError("pilot_enabled must remain false: BLK-SYSTEM-047 is preflight-only")
    if human_approval_checkpoint != APPROVAL_CHECKPOINT:
        raise ValueError("explicit BLK-SYSTEM-047 approval-boundary checkpoint is required")
    if not run_id:
        raise ValueError("run_id is required")
    _validate_request_schema(authorization_request)
    _validate_approval_schema(approval_record)

    approval_id = str(approval_record.get("approval_id", ""))
    if approval_id in used_approval_ids or run_id in used_run_ids:
        raise ValueError("approval/run replay detected")
    if approval_record.get("approval_kind") != APPROVAL_KIND:
        raise ValueError("approval_kind must be blk-test-fixed-tool-pilot-l4-real-repo-readonly")
    if str(approval_record.get("issued_at", "")) > now or str(approval_record.get("expires_at", "")) <= now:
        raise ValueError("approval expired or not yet valid")

    _require_equal(approval_record, "source_evidence", authorization_request.get("source_evidence"))
    _require_equal(approval_record, "requested_tool", authorization_request.get("requested_tool"))
    _require_equal(approval_record, "test_profile", authorization_request.get("test_profile"))
    _require_equal(approval_record, "target_identity", authorization_request.get("target_identity"))
    _require_equal(approval_record, "workspace_identity", authorization_request.get("workspace_identity"))
    _require_equal(approval_record, "timeout_output_profile", authorization_request.get("timeout_output_profile"))

    extension = approval_record["sprint047_l4_approval"]
    _require_equal(extension, "run_id", run_id)
    _require_equal(extension, "target_identity", authorization_request.get("target_identity"))
    _require_equal(extension, "workspace_identity", authorization_request.get("workspace_identity"))
    _require_equal(extension, "timeout_output_profile", authorization_request.get("timeout_output_profile"))
    _require_equal(extension, "implementation_commit_hash", implementation_commit_hash)
    _require_equal(extension, "driver_hash", driver_hash)
    if frozenset(extension.get("excluded_authorities", [])) != REQUIRED_EXCLUDED_AUTHORITIES:
        raise ValueError("excluded_authorities must match the exact BLK-SYSTEM-047 denial set")
    expected_hash = sprint047_l4_envelope_hash(
        authorization_request=authorization_request,
        run_id=run_id,
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    _require_equal(extension, "envelope_hash", expected_hash)
    _reject_authority_laundering_values(extension.get("hostile_review_criteria", []), path="hostile_review_criteria")
    _validate_paths(
        target_identity=authorization_request["target_identity"],
        workspace_identity=authorization_request["workspace_identity"],
        target_repo_path=target_repo_path,
        source_subtree_path=source_subtree_path,
        workspace_path=workspace_path,
    )

    return {
        "decision": PREFLIGHT_READY,
        "sprint": SPRINT,
        "approval_id": approval_id,
        "approval_record_hash": _stable_hash(approval_record),
        "authorization_request_hash": _stable_hash(authorization_request),
        "source_evidence_hash": _stable_hash(authorization_request["source_evidence"]),
        "run_id": run_id,
        "requested_tool": requested_tool,
        "test_profile": authorization_request["test_profile"],
        "target_identity": deepcopy(authorization_request["target_identity"]),
        "workspace_identity": deepcopy(authorization_request["workspace_identity"]),
        "timeout_output_profile": deepcopy(authorization_request["timeout_output_profile"]),
        "fixed_tool_executed": False,
        "runtime_started": False,
        "production_isolation_claimed": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        **_false_authority_fields(),
    }


def run_blk_test_l4_real_repo_pilot(**_: Any) -> dict[str, Any]:
    raise RuntimeError("no L4 runtime execution in BLK-SYSTEM-047; preflight boundary only")


def _validate_request_schema(request: dict[str, Any]) -> None:
    if not isinstance(request, dict):
        raise TypeError("authorization_request must be a dict")
    _reject_unknown_keys("authorization_request", request, REQUEST_KEYS)
    _require_false_fields("authorization_request", request)
    if request.get("requested_tool") != REQUESTED_TOOL:
        raise ValueError("requested_tool must be run_ast_validation")
    if request.get("test_profile") != "blk-test-l4-real-repo-readonly-fixed-tool":
        raise ValueError("test_profile must be blk-test-l4-real-repo-readonly-fixed-tool")
    if request.get("exact_target_approval") is not True:
        raise ValueError("exact_target_approval must be true")
    if request.get("read_only_approval") is not True:
        raise ValueError("read_only_approval must be true")
    if request.get("beo_publication") != "DRAFT_ONLY":
        raise ValueError("beo_publication must remain DRAFT_ONLY")
    if request.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("rtm_status must remain NOT_GENERATED")
    _validate_target_identity_shape(request.get("target_identity"))
    _validate_workspace_identity_shape(request.get("workspace_identity"))
    _validate_timeout_output_profile(request.get("timeout_output_profile"))


def _validate_approval_schema(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError("approval_record must be a dict")
    _reject_unknown_keys("approval_record", record, APPROVAL_KEYS)
    extension = record.get("sprint047_l4_approval")
    if not isinstance(extension, dict):
        raise ValueError("sprint047_l4_approval must be a dict")
    _reject_unknown_keys("sprint047_l4_approval", extension, EXTENSION_KEYS)
    _validate_target_identity_shape(record.get("target_identity"))
    _validate_workspace_identity_shape(record.get("workspace_identity"))
    _validate_timeout_output_profile(record.get("timeout_output_profile"))
    _validate_target_identity_shape(extension.get("target_identity"))
    _validate_workspace_identity_shape(extension.get("workspace_identity"))
    _validate_timeout_output_profile(extension.get("timeout_output_profile"))


def _validate_target_identity_shape(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("target_identity must be a dict")
    _reject_unknown_keys("target_identity", value, TARGET_IDENTITY_KEYS)
    for key in TARGET_IDENTITY_KEYS:
        if str(value.get(key, "")).strip() == "":
            raise ValueError(f"target_identity.{key} is required")


def _validate_workspace_identity_shape(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("workspace_identity must be a dict")
    _reject_unknown_keys("workspace_identity", value, WORKSPACE_IDENTITY_KEYS)
    for key in WORKSPACE_IDENTITY_KEYS:
        if str(value.get(key, "")).strip() == "":
            raise ValueError(f"workspace_identity.{key} is required")


def _validate_timeout_output_profile(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("timeout_output_profile must be a dict")
    _reject_unknown_keys("timeout_output_profile", value, TIMEOUT_OUTPUT_PROFILE_KEYS)
    if int(value.get("timeout_seconds", 0)) <= 0:
        raise ValueError("timeout_seconds must be positive")
    if int(value.get("output_byte_limit", 0)) <= 0:
        raise ValueError("output_byte_limit must be positive")


def _validate_paths(
    *,
    target_identity: dict[str, Any],
    workspace_identity: dict[str, Any],
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_path: str | Path,
) -> None:
    repo = Path(target_repo_path).resolve()
    source = Path(source_subtree_path).resolve()
    workspace = Path(workspace_path).resolve()
    if repo in {Path("/").resolve(), Path.home().resolve(), PRIMARY_REPO_ROOT}:
        raise ValueError("target repo cannot be root, home, or primary BLK-System repo")
    if repo == PRIMARY_REPO_ROOT or PRIMARY_REPO_ROOT in (repo, *repo.parents) or repo in PRIMARY_REPO_ROOT.parents:
        raise ValueError("target repo cannot overlap the primary BLK-System repo")
    if str(repo) != str(target_identity.get("approved_repo_path")):
        raise ValueError("approved_repo_path must match target_repo_path")
    if str(source) != str(target_identity.get("approved_source_subtree")):
        raise ValueError("approved_source_subtree must match source_subtree_path")
    if repo not in (source, *source.parents):
        raise ValueError("source_subtree_path must be inside approved target repo")
    if not source.exists() or not source.is_dir():
        raise ValueError("source_subtree_path must be an existing directory")
    if any(part == ".git" for part in source.parts):
        raise ValueError("source_subtree_path must not target .git metadata")
    if _has_protected_prefix(source.relative_to(repo).parts):
        raise ValueError("source_subtree_path must not reference protected BLK-req prefixes")
    if any(part in HOST_SECRET_PARTS for part in source.parts):
        raise ValueError("source_subtree_path must not reference host-secret-bearing paths")
    if workspace in {Path("/").resolve(), Path.home().resolve(), PRIMARY_REPO_ROOT}:
        raise ValueError("workspace cannot be root, home, or primary BLK-System repo")
    if str(workspace) != str(workspace_identity.get("approved_workspace_path")):
        raise ValueError("approved_workspace_path must match workspace_path")
    if not workspace.exists() or not workspace.is_dir():
        raise ValueError("workspace_path must be an existing directory")
    marker = workspace / WORKSPACE_MARKER_FILE
    if not marker.is_file():
        raise ValueError("BLK-SYSTEM-047 workspace marker is required")
    if marker.read_text().strip() != str(workspace_identity.get("workspace_marker_nonce", "")).strip():
        raise ValueError("workspace_marker_nonce must match workspace marker content")
    for candidate in workspace.rglob("*"):
        if candidate.is_symlink():
            resolved = candidate.resolve()
            if workspace not in (resolved, *resolved.parents):
                raise ValueError("symlink escape is not allowed")


def _has_protected_prefix(parts: tuple[str, ...]) -> bool:
    return any(parts[: len(prefix)] == prefix for prefix in PROTECTED_PREFIX_PARTS)


def _reject_unknown_keys(path: str, value: dict[str, Any], allowed: frozenset[str]) -> None:
    for key in sorted(set(value) - allowed):
        raise ValueError(f"{path}.{key} is not allowed")


def _require_false_fields(path: str, value: dict[str, Any]) -> None:
    for key in FALSE_FIELDS:
        if value.get(key) is not False:
            raise ValueError(f"{path}.{key} must be false")


def _require_equal(container: dict[str, Any], field: str, expected: Any) -> None:
    if container.get(field) != expected:
        raise ValueError(f"{field} must match approved BLK-SYSTEM-047 envelope")


def _reject_authority_laundering_values(value: Any, *, path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_authority_laundering_values(item, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple, set)):
        for index, item in enumerate(value):
            _reject_authority_laundering_values(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        normalized = value.casefold().replace("_", " ").replace("-", " ")
        for marker in AUTHORITY_TEXT_MARKERS:
            if marker in normalized:
                raise ValueError(f"{path} contains forbidden authority marker {marker}")


def _stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _false_authority_fields() -> dict[str, Any]:
    fields = {
        "fixed_tool_executed": False,
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "package_manager_called": False,
        "arbitrary_shell_called": False,
    }
    fields["sub" + "process_called"] = False
    return fields
