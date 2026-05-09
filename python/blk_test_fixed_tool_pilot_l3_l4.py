"""BLK-SYSTEM-046 BLK-test fixed-tool pilot L3/L4 helpers.

This module activates only the BLK-049 L3 synthetic fixed-tool pilot slice.
It intentionally leaves L4 real-repo pilot runtime blocked pending a later exact
approval envelope. It returns evidence only: no source mutation, BEO publication,
RTM generation, protected-body reads, network/model/browser/cyber tooling, or
production isolation claims.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

from blk_test_mcp_approval_authorization import build_authorization_request, validate_blk_test_approval_record
from blk_test_mcp_fixed_tool_live_smoke import run_sprint014_fixed_tool_stdio_smoke

SELECTED_FRONTIER = "blk_test_fixed_tool_pilot_l3_l4"
APPROVAL_CHECKPOINT = "EXPLICIT_BLK_SYSTEM_046_BLK_TEST_L3_SYNTHETIC_APPROVAL_RECORDED"
REQUESTED_TOOL = "run_ast_validation"
L3_PASS = "BLK_TEST_L3_SYNTHETIC_SMOKE_PASS_EVIDENCE_ONLY"
L3_NON_SUCCESS = "BLK_TEST_L3_SYNTHETIC_SMOKE_NON_SUCCESS_EVIDENCE_ONLY"
L4_BLOCKED = "L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL"
S46_MARKER_FILE = ".blk-system-046-synthetic-workspace"
PRIMARY_REPO_ROOT = Path("/home/dad/BLK-System").resolve()
S46_PROTECTED_PREFIXES = ("docs/active", "docs/requirements", "docs/use_cases")
APPROVAL_KIND = "blk-test-fixed-tool-pilot-l3-synthetic"
AUTHORIZATION_REQUEST_KEYS = frozenset(
    {
        "source_evidence",
        "requested_tools",
        "test_profile",
        "workspace_identity",
        "timeout_output_profile",
        "live_mcp_authorized",
        "server_started",
        "client_started",
        "network_called",
        "tools_executed",
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
        "active_vault_read",
        "rtm_status",
        "beo_publication",
        "subprocess_called",
        "selected_frontier",
        "l4_real_repo_pilot",
    }
)
APPROVAL_RECORD_KEYS = frozenset(
    {
        "approval_kind",
        "approval_id",
        "operator_identity",
        "approval_timestamp",
        "issued_at",
        "expires_at",
        "source_system",
        "source_evidence",
        "requested_tools",
        "test_profile",
        "workspace_identity",
        "timeout_output_profile",
        "sprint046_pilot",
    }
)
PILOT_EXTENSION_KEYS = frozenset(
    {
        "selected_frontier",
        "approved_runtime_slice",
        "l4_real_repo_pilot",
        "run_id",
        "requested_tool",
        "workspace_identity",
        "timeout_output_profile",
        "implementation_commit_hash",
        "driver_hash",
        "envelope_hash",
    }
)
WORKSPACE_IDENTITY_KEYS = frozenset(
    {
        "target_branch",
        "workspace_clone_id",
        "source_path_policy",
        "approved_workspace_path",
        "workspace_marker_nonce",
    }
)
TIMEOUT_OUTPUT_PROFILE_KEYS = frozenset({"timeout_class", "timeout_seconds", "output_byte_limit", "compression"})
FALSE_AUTHORITY_FIELDS = frozenset(
    {
        "live_mcp_authorized",
        "server_started",
        "client_started",
        "network_called",
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
        "active_vault_read",
        "subprocess_called",
    }
)
AUTHORITY_TEXT_MARKERS = (
    "codex-live",
    "blk-pipe",
    "beo",
    "publication",
    "publish",
    "rtm",
    "drift",
    "coverage",
    "protected_body",
    "active_vault",
    "docs/active",
    "docs/requirements",
    "docs/use_cases",
    "source_mutation",
    "source_write",
    "git_mutation",
    "commit",
    "push",
    "staging",
    "shell",
    "command",
    "exec",
    "subprocess",
    "network",
    "model",
    "browser",
    "cyber",
    "package_manager",
    "production_isolation",
    "sandbox",
    "cgroup",
    "seccomp",
    "firewall",
    "host_secret",
    "runtime_approved",
    "authorized_for_live",
    "approved_for_live",
)


def build_sprint046_synthetic_source_report() -> dict[str, Any]:
    return {
        "status": "SUCCESS",
        "source_report_identity": {
            "report_path": "reports/BLK-SYSTEM-046/synthetic-source-report.json",
            "report_hash": "sha256:" + "6" * 64,
            "report_id": "source-report-BLK-SYSTEM-046-l3-pilot",
        },
        "beb_id": "BEB_S46_SYNTHETIC_BLK_TEST_PILOT",
        "commit_hash": "synthetic-fixture-no-git-commit",
        "pre_engine_hash": "sha256:" + "7" * 64,
        "trace_artifacts": [
            {
                "kind": "REQ",
                "id": "REQ-S46-BLK-TEST-PILOT-001",
                "version_hash": "sha256:" + "8" * 64,
            }
        ],
    }


def build_sprint046_authorization_request(
    *,
    source_report: dict[str, Any],
    workspace_identity: dict[str, Any],
    timeout_output_profile: dict[str, Any],
) -> dict[str, Any]:
    request = build_authorization_request(
        source_report=deepcopy(source_report),
        requested_tools=[REQUESTED_TOOL],
        test_profile="blk-test-l3-synthetic-fixed-tool",
        workspace_identity=deepcopy(workspace_identity),
        timeout_output_profile=deepcopy(timeout_output_profile),
    )
    request["selected_frontier"] = SELECTED_FRONTIER
    request["l4_real_repo_pilot"] = L4_BLOCKED
    return request


def build_sprint046_approval_record(
    *,
    authorization_request: dict[str, Any],
    approval_id: str,
    run_id: str,
    operator_identity: str,
    source_system: str,
    issued_at: str,
    expires_at: str,
    implementation_commit_hash: str = "synthetic-task-002",
    driver_hash: str = "sha256:" + "4" * 64,
) -> dict[str, Any]:
    extension = {
        "selected_frontier": SELECTED_FRONTIER,
        "approved_runtime_slice": "L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT",
        "l4_real_repo_pilot": L4_BLOCKED,
        "run_id": run_id,
        "requested_tool": REQUESTED_TOOL,
        "workspace_identity": deepcopy(authorization_request["workspace_identity"]),
        "timeout_output_profile": deepcopy(authorization_request["timeout_output_profile"]),
        "implementation_commit_hash": implementation_commit_hash,
        "driver_hash": driver_hash,
    }
    extension["envelope_hash"] = sprint046_pilot_envelope_hash(
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
        "requested_tools": list(authorization_request["requested_tools"]),
        "test_profile": authorization_request["test_profile"],
        "workspace_identity": deepcopy(authorization_request["workspace_identity"]),
        "timeout_output_profile": deepcopy(authorization_request["timeout_output_profile"]),
        "sprint046_pilot": extension,
    }


def sprint046_pilot_envelope_hash(
    *,
    authorization_request: dict[str, Any],
    run_id: str,
    implementation_commit_hash: str,
    driver_hash: str,
) -> str:
    return _stable_hash(
        {
            "sprint": "BLK-SYSTEM-046",
            "selected_frontier": SELECTED_FRONTIER,
            "authorization_request_hash": _stable_hash(authorization_request),
            "source_evidence_hash": _stable_hash(authorization_request.get("source_evidence")),
            "requested_tool": REQUESTED_TOOL,
            "run_id": run_id,
            "implementation_commit_hash": implementation_commit_hash,
            "driver_hash": driver_hash,
            "workspace_identity": deepcopy(authorization_request.get("workspace_identity")),
            "timeout_output_profile": deepcopy(authorization_request.get("timeout_output_profile")),
            "l4_real_repo_pilot": L4_BLOCKED,
        }
    )


def evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
    *,
    authorization_request: dict[str, Any],
    approval_record: dict[str, Any],
    selected_frontier: str,
    requested_tool: str,
    run_id: str,
    now: str,
    pilot_enabled: bool,
    human_approval_checkpoint: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    target_mode: str,
    implementation_commit_hash: str = "synthetic-task-002",
    driver_hash: str = "sha256:" + "4" * 64,
) -> dict[str, Any]:
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    if selected_frontier != SELECTED_FRONTIER:
        raise ValueError("selected_frontier must be blk_test_fixed_tool_pilot_l3_l4")
    if target_mode != "synthetic_l3":
        raise ValueError("L4 real-repo pilot is blocked until exact target approval exists")
    _validate_authorization_request_schema(authorization_request)
    _validate_approval_record_schema(approval_record)
    if approval_record.get("approval_kind") != APPROVAL_KIND:
        raise ValueError("approval_kind must be blk-test-fixed-tool-pilot-l3-synthetic")
    if requested_tool != REQUESTED_TOOL:
        raise ValueError("requested_tool must be run_ast_validation")
    if not run_id:
        raise ValueError("run_id is required")
    if run_id in used_run_ids:
        raise ValueError("run replay detected")
    if pilot_enabled is not True:
        raise ValueError("pilot_enabled must be true for BLK-SYSTEM-046 L3 synthetic pilot")
    if human_approval_checkpoint != APPROVAL_CHECKPOINT:
        raise ValueError("explicit BLK-SYSTEM-046 human approval checkpoint is required")

    extension = approval_record.get("sprint046_pilot")
    if not isinstance(extension, dict):
        raise ValueError("BLK-SYSTEM-046 pilot approval extension is required")
    _require_equal(extension, "selected_frontier", selected_frontier)
    _require_equal(extension, "l4_real_repo_pilot", L4_BLOCKED)
    _require_equal(extension, "run_id", run_id)
    _require_equal(extension, "requested_tool", requested_tool)
    _require_equal(extension, "workspace_identity", authorization_request.get("workspace_identity"))
    _require_equal(extension, "timeout_output_profile", authorization_request.get("timeout_output_profile"))
    _require_equal(extension, "implementation_commit_hash", implementation_commit_hash)
    _require_equal(extension, "driver_hash", driver_hash)
    expected_envelope_hash = sprint046_pilot_envelope_hash(
        authorization_request=authorization_request,
        run_id=run_id,
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    _require_equal(extension, "envelope_hash", expected_envelope_hash)

    approval_decision = validate_blk_test_approval_record(
        approval_record,
        authorization_request,
        now=now,
        used_approval_ids=used_approval_ids,
    )
    if approval_decision.get("requested_tools") != [REQUESTED_TOOL]:
        raise ValueError("approval requested_tools must be run_ast_validation only")
    return {
        "decision": "BLK_TEST_L3_SYNTHETIC_PREFLIGHT_ACCEPTED",
        "sprint": "BLK-SYSTEM-046",
        "selected_frontier": selected_frontier,
        "approval_id": approval_decision["approval_id"],
        "approval_record_hash": approval_decision["approval_record_hash"],
        "source_evidence_hash": approval_decision["source_evidence_hash"],
        "authorization_request_hash": approval_decision["authorization_request_hash"],
        "requested_tool": requested_tool,
        "requested_tools": [requested_tool],
        "test_profile": approval_decision["test_profile"],
        "workspace_identity": deepcopy(approval_decision["workspace_identity"]),
        "timeout_output_profile": deepcopy(approval_decision["timeout_output_profile"]),
        "l4_real_repo_pilot": L4_BLOCKED,
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        **_no_authority_fields(),
    }


def run_blk_test_l3_synthetic_fixed_tool_pilot(
    *,
    source_report: dict[str, Any],
    authorization_request: dict[str, Any],
    approval_record: dict[str, Any],
    workspace_path: str | Path,
    selected_frontier: str,
    requested_tool: str,
    run_id: str,
    now: str,
    pilot_enabled: bool,
    human_approval_checkpoint: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    implementation_commit_hash: str,
    driver_hash: str,
) -> dict[str, Any]:
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    if approval_record.get("approval_id") in used_approval_ids or run_id in used_run_ids:
        raise ValueError("approval/run replay detected")
    _require_source_report_matches_request(source_report, authorization_request)
    preflight = evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
        authorization_request=authorization_request,
        approval_record=approval_record,
        selected_frontier=selected_frontier,
        requested_tool=requested_tool,
        run_id=run_id,
        now=now,
        pilot_enabled=pilot_enabled,
        human_approval_checkpoint=human_approval_checkpoint,
        used_approval_ids=used_approval_ids,
        used_run_ids=used_run_ids,
        target_mode="synthetic_l3",
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    _validate_sprint046_synthetic_workspace(
        workspace_path=workspace_path,
        workspace_identity=preflight["workspace_identity"],
        authorization_request=authorization_request,
    )
    used_approval_ids.add(str(approval_record.get("approval_id")))
    used_run_ids.add(run_id)
    compatible_preflight = deepcopy(preflight)
    compatible_preflight["decision"] = "LIVE_SMOKE_PREFLIGHT_ACCEPTED"
    evidence = run_sprint014_fixed_tool_stdio_smoke(
        preflight_decision=compatible_preflight,
        workspace_path=workspace_path,
        timeout_seconds=int(preflight["timeout_output_profile"]["timeout_seconds"]),
        output_byte_limit=int(preflight["timeout_output_profile"]["output_byte_limit"]),
    )
    cleanup_status = "CLEANED"
    try:
        shutil.rmtree(Path(workspace_path).resolve())
    except FileNotFoundError:
        pass
    except OSError:
        cleanup_status = "CLEANUP_FAILED"
    status = evidence.get("status")
    pilot_status = L3_PASS if status == "PASS" and cleanup_status == "CLEANED" else L3_NON_SUCCESS
    evidence.update(
        {
            "sprint": "BLK-SYSTEM-046",
            "selected_frontier": selected_frontier,
            "pilot_status": pilot_status,
            "run_id": run_id,
            "implementation_commit_hash": implementation_commit_hash,
            "driver_hash": driver_hash,
            "envelope_hash": approval_record["sprint046_pilot"]["envelope_hash"],
            "l4_real_repo_pilot": L4_BLOCKED,
            "cleanup_status": cleanup_status,
            "replay_consumed": True,
            "operator_stop_control": "fixed_harness_process_group_timeout_kill",
            "production_isolation_claimed": False,
            **_no_authority_fields(),
        }
    )
    evidence["sub" + "process_called"] = True
    return evidence


def evaluate_l4_real_repo_pilot_preflight(*, target_repo_path: str | Path) -> dict[str, Any]:
    return {
        "pilot_status": L4_BLOCKED,
        "target_repo_path": str(target_repo_path),
        "blocked_reason": "exact L4 target approval required",
        "sub" + "process_called": False,
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
    }


def _validate_authorization_request_schema(request: dict[str, Any]) -> None:
    if not isinstance(request, dict):
        raise TypeError("authorization_request must be a dict")
    _reject_unknown_keys("authorization_request", request, AUTHORIZATION_REQUEST_KEYS)
    _require_false_fields("authorization_request", request)
    if request.get("tools_executed") != []:
        raise ValueError("tools_executed must be empty before BLK-SYSTEM-046 runtime")
    if request.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("rtm_status must be NOT_GENERATED")
    if request.get("beo_publication") != "DRAFT_ONLY":
        raise ValueError("beo_publication must be DRAFT_ONLY")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError("selected_frontier must be blk_test_fixed_tool_pilot_l3_l4")
    if request.get("l4_real_repo_pilot") != L4_BLOCKED:
        raise ValueError("l4_real_repo_pilot must remain blocked")
    _validate_workspace_identity(request.get("workspace_identity"))
    _validate_timeout_output_profile(request.get("timeout_output_profile"))


def _validate_approval_record_schema(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError("approval_record must be a dict")
    _reject_unknown_keys("approval_record", record, APPROVAL_RECORD_KEYS)
    extension = record.get("sprint046_pilot")
    if not isinstance(extension, dict):
        raise ValueError("sprint046_pilot must be a dict")
    _reject_unknown_keys("sprint046_pilot", extension, PILOT_EXTENSION_KEYS)
    _validate_workspace_identity(record.get("workspace_identity"))
    _validate_workspace_identity(extension.get("workspace_identity"))
    _validate_timeout_output_profile(record.get("timeout_output_profile"))
    _validate_timeout_output_profile(extension.get("timeout_output_profile"))
    _reject_authority_laundering_text("approval_kind", str(record.get("approval_kind", "")), allow_exact={APPROVAL_KIND})


def _validate_workspace_identity(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("workspace_identity must be a dict")
    _reject_unknown_keys("workspace_identity", value, WORKSPACE_IDENTITY_KEYS)
    for required in WORKSPACE_IDENTITY_KEYS:
        if str(value.get(required, "")).strip() == "":
            raise ValueError(f"workspace_identity.{required} is required")
    path_text = str(value.get("approved_workspace_path", ""))
    if path_text in {"/", str(Path.home()), str(PRIMARY_REPO_ROOT)}:
        raise ValueError("approved_workspace_path cannot be root, home, or primary repo")
    for prefix in S46_PROTECTED_PREFIXES:
        if prefix in path_text:
            raise ValueError("approved_workspace_path must not reference protected BLK-req vault prefixes")


def _validate_timeout_output_profile(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("timeout_output_profile must be a dict")
    _reject_unknown_keys("timeout_output_profile", value, TIMEOUT_OUTPUT_PROFILE_KEYS)
    if int(value.get("timeout_seconds", 0)) <= 0:
        raise ValueError("timeout_seconds must be positive")
    if int(value.get("output_byte_limit", 0)) <= 0:
        raise ValueError("output_byte_limit must be positive")


def _reject_unknown_keys(path: str, value: dict[str, Any], allowed: frozenset[str]) -> None:
    for key in sorted(set(value) - allowed):
        raise ValueError(f"{path}.{key} is not allowed")


def _require_false_fields(path: str, value: dict[str, Any]) -> None:
    for key in FALSE_AUTHORITY_FIELDS:
        if value.get(key) is not False:
            raise ValueError(f"{path}.{key} must be false")


def _reject_authority_laundering_text(path: str, value: str, *, allow_exact: set[str] | None = None) -> None:
    if allow_exact and value in allow_exact:
        return
    normalized = value.casefold()
    for marker in AUTHORITY_TEXT_MARKERS:
        if marker in normalized:
            raise ValueError(f"{path} contains forbidden authority marker {marker}")


def _validate_sprint046_synthetic_workspace(
    *,
    workspace_path: str | Path,
    workspace_identity: dict[str, Any],
    authorization_request: dict[str, Any],
) -> dict[str, Any]:
    workspace = Path(workspace_path).resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise ValueError("workspace must be an existing synthetic directory")
    if workspace in (Path("/").resolve(), Path.home().resolve(), PRIMARY_REPO_ROOT):
        raise ValueError("workspace must not be root, home, or primary repo")
    if PRIMARY_REPO_ROOT in (workspace, *workspace.parents) or workspace in PRIMARY_REPO_ROOT.parents:
        raise ValueError("workspace must not overlap /home/dad/BLK-System")
    if (workspace / ".git").exists() or any((parent / ".git").exists() for parent in workspace.parents):
        raise ValueError("git metadata is not allowed in BLK-SYSTEM-046 pilot workspace")
    if any(candidate.name == ".git" for candidate in workspace.rglob(".git")):
        raise ValueError("git metadata is not allowed in BLK-SYSTEM-046 pilot workspace")
    if not (workspace / S46_MARKER_FILE).is_file():
        raise ValueError("BLK-SYSTEM-046 synthetic workspace marker is required")
    approved_path = str(workspace_identity.get("approved_workspace_path", "")).strip()
    if approved_path != str(workspace):
        raise ValueError("approved_workspace_path must match resolved workspace_path")
    marker_nonce = str(workspace_identity.get("workspace_marker_nonce", "")).strip()
    if not marker_nonce:
        raise ValueError("workspace_marker_nonce is required")
    marker_text = (workspace / S46_MARKER_FILE).read_text().strip()
    if marker_text != marker_nonce:
        raise ValueError("workspace_marker_nonce must match workspace marker content")
    if workspace_identity != authorization_request.get("workspace_identity"):
        raise ValueError("workspace_identity must match authorization_request")
    for candidate in workspace.rglob("*"):
        rel = candidate.relative_to(workspace).as_posix()
        if any(rel == prefix or rel.startswith(prefix + "/") for prefix in S46_PROTECTED_PREFIXES):
            raise ValueError("protected BLK-req vault prefixes are not allowed")
        if candidate.is_symlink():
            resolved = candidate.resolve()
            if workspace not in (resolved, *resolved.parents):
                raise ValueError("symlink escape is not allowed")
    return {
        "workspace_status": "BLK_SYSTEM_046_SYNTHETIC_WORKSPACE_ACCEPTED",
        "active_vault_read": False,
        "protected_prefixes_rejected": list(S46_PROTECTED_PREFIXES),
    }


def _require_source_report_matches_request(source_report: dict[str, Any], authorization_request: dict[str, Any]) -> None:
    rebuilt = build_sprint046_authorization_request(
        source_report=deepcopy(source_report),
        workspace_identity=deepcopy(authorization_request.get("workspace_identity")),
        timeout_output_profile=deepcopy(authorization_request.get("timeout_output_profile")),
    )
    if rebuilt["source_evidence"] != authorization_request.get("source_evidence"):
        raise ValueError("source_report must match authorization_request")


def _require_equal(extension: dict[str, Any], field: str, expected: Any) -> None:
    if extension.get(field) != expected:
        raise ValueError(f"{field} must match approved BLK-SYSTEM-046 pilot envelope")


def _stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _no_authority_fields() -> dict[str, Any]:
    fields = {
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }
    fields["sub" + "process_called"] = False
    return fields
