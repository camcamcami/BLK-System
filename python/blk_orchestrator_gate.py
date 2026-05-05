"""Fail-closed BLK orchestration approval and BLK-test MCP design stubs.

This module is dependency-free contract code for Sprint 006. It does not run
Codex, call BLK-test MCP, open network sockets, spawn subprocesses, generate RTM,
or publish authoritative BEOs.
"""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

_ALLOWED_LOCAL_PROFILES = {"dev-smoke", "strict-ci", "codex-dry-run"}
_BLOCKED_CYBER_PROFILE = "cyber-execution"
_CODEX_LIVE_PROFILE = "codex-live"
_SUCCESS_SOURCE_STATUS = "SUCCESS"
_VALID_SOURCE_STATUSES = {
    "SUCCESS",
    "FATAL_SYSTEM_PANIC",
    "FATAL_ENGINE_FAILED",
    "INVALID_PAYLOAD",
    "SYNTAX_GATE_FAILED",
    "UNAUTHORIZED_FILE_MUTATION",
    "INVALID_REVERT_ANCHOR",
    "FATAL_OUTPUT_FLOOD",
    "ENGINE_TIMEOUT",
    "GIT_DIRTY",
    "INTERNAL_ERROR",
    "FATAL_CRASH",
    "FATAL_PYTHON_TIMEOUT",
}
_VALID_MCP_RESPONSE_STATUSES = {"PASS", "FAIL", "BLOCKED"}
_VERDICT_MCP_RESPONSE_STATUSES = {"PASS", "FAIL"}
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_TOKEN_UNSAFE_PATTERN = re.compile(r"\s")
_EVALUATE_METHOD = "blk_test.evaluate_execution"
_NOT_RUN_METHOD = "blk_test.not_run"


@dataclass(frozen=True)
class ProfileDecision:
    profile: str
    allowed: bool
    reason: str
    live_execution_authorized: bool = False
    approval_recorded: bool = False
    decision: str = "BLOCKED"


def evaluate_profile_gate(
    profile: str,
    *,
    beb_id: str,
    target_branch: str,
    trace_hash: str,
    approval_token: str | None = None,
) -> ProfileDecision:
    """Return a deterministic fail-closed decision for a BLK execution profile.

    `allowed` means the profile is executable now. `codex-live` may validate an
    explicit approval-token shape, but Sprint 006 records exact-token approval as
    audit-only and still does not authorize or perform live Codex execution.
    """
    normalized_profile = profile.strip()
    try:
        _validate_context(beb_id=beb_id, target_branch=target_branch, trace_hash=trace_hash)
    except ValueError as exc:
        return ProfileDecision(
            profile=normalized_profile,
            allowed=False,
            reason=str(exc),
            decision="BLOCKED_INVALID_CONTEXT",
        )

    if normalized_profile in _ALLOWED_LOCAL_PROFILES:
        return ProfileDecision(
            profile=normalized_profile,
            allowed=True,
            reason="profile allowed for deterministic local or fixture-only execution",
            live_execution_authorized=False,
            decision="ALLOWED_LOCAL_ONLY",
        )

    if normalized_profile == _CODEX_LIVE_PROFILE:
        expected = approval_token_for(
            beb_id=beb_id,
            target_branch=target_branch,
            trace_hash=trace_hash,
        )
        if approval_token is None:
            return ProfileDecision(
                profile=normalized_profile,
                allowed=False,
                reason="codex-live requires an exact explicit approval token",
                live_execution_authorized=False,
                decision="BLOCKED_APPROVAL_REQUIRED",
            )
        if approval_token != expected:
            return ProfileDecision(
                profile=normalized_profile,
                allowed=False,
                reason="codex-live approval token did not match beb_id, target_branch, and trace_hash",
                live_execution_authorized=False,
                decision="BLOCKED_APPROVAL_MISMATCH",
            )
        return ProfileDecision(
            profile=normalized_profile,
            allowed=False,
            reason="codex-live approval token validated for audit, but Sprint 006 records approval only and does not execute Codex",
            live_execution_authorized=False,
            approval_recorded=True,
            decision="APPROVED_BUT_NOT_EXECUTED",
        )

    if normalized_profile == _BLOCKED_CYBER_PROFILE:
        return ProfileDecision(
            profile=normalized_profile,
            allowed=False,
            reason="cyber-execution is blocked in Sprint 006 regardless of approval token",
            live_execution_authorized=False,
            decision="BLOCKED_CYBER_EXECUTION",
        )

    return ProfileDecision(
        profile=normalized_profile,
        allowed=False,
        reason=f"unknown BLK execution profile: {normalized_profile}",
        live_execution_authorized=False,
        decision="BLOCKED_UNKNOWN_PROFILE",
    )


def approval_token_for(*, beb_id: str, target_branch: str, trace_hash: str) -> str:
    """Build the exact auditable `codex-live` approval-token shape."""
    _validate_context(beb_id=beb_id, target_branch=target_branch, trace_hash=trace_hash)
    return (
        "BLK_APPROVE_CODEX_LIVE "
        f"beb_id={beb_id} target_branch={target_branch} trace_hash={trace_hash}"
    )


def build_blk_test_mcp_request(source_report: dict[str, Any], *, enabled: bool = False) -> dict[str, Any]:
    """Build a disabled-by-default BLK-test MCP request shape.

    The live send path is intentionally unavailable in Sprint 006. Passing
    `enabled=True` raises instead of opening a socket, spawning MCP, or calling a
    service. With `enabled=False`, this returns an evaluation-shaped disabled
    stub only for source reports that contain complete SUCCESS evidence.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP is disabled in Sprint 006")

    source_status = _source_status(source_report, field="status")
    beb_id = _required_text(source_report, "beb_id")
    pre_engine_hash = _required_text(source_report, "pre_engine_hash")
    trace_artifacts = _required_trace_artifacts(source_report, owner="source_report")

    if source_status != _SUCCESS_SOURCE_STATUS:
        raise ValueError(
            "BLK-test MCP evaluation request requires source_report status SUCCESS; "
            f"got {source_status}"
        )

    commit_hash = _required_text(source_report, "commit_hash")
    staged_files = _required_string_list(source_report, "staged_files")

    return {
        "enabled": False,
        "transport": "DISABLED_STUB",
        "method": _EVALUATE_METHOD,
        "source_status": source_status,
        "beb_id": beb_id,
        "commit_hash": commit_hash,
        "pre_engine_hash": pre_engine_hash,
        "staged_files": staged_files,
        "destroyed_files": _string_list(source_report.get("destroyed_files")),
        "trace_artifacts": trace_artifacts,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
        "reason": "live BLK-test MCP disabled in Sprint 006",
    }


def build_blk_test_mcp_not_run_request(
    source_report: dict[str, Any],
    *,
    enabled: bool = False,
) -> dict[str, Any]:
    """Build a disabled not-run BLK-test MCP request for non-success sources.

    This shape preserves source metadata for deterministic adapter/BEO/RTM
    fixture paths without claiming that BLK-test evaluated a source execution.
    It remains disabled and performs no live MCP transport work.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP not-run request path is disabled in Sprint 007")

    source_status = _source_status(source_report, field="status")
    if source_status == _SUCCESS_SOURCE_STATUS:
        raise ValueError(
            "SUCCESS source reports must use build_blk_test_mcp_request for "
            "evaluation-shaped disabled requests"
        )

    beb_id = _required_text(source_report, "beb_id")
    pre_engine_hash = _required_text(source_report, "pre_engine_hash")
    trace_artifacts = _required_trace_artifacts(source_report, owner="source_report")

    return {
        "enabled": False,
        "transport": "DISABLED_STUB",
        "method": _NOT_RUN_METHOD,
        "source_status": source_status,
        "beb_id": beb_id,
        "commit_hash": str(source_report.get("commit_hash", "")).strip(),
        "pre_engine_hash": pre_engine_hash,
        "staged_files": _string_list(source_report.get("staged_files")),
        "destroyed_files": _string_list(source_report.get("destroyed_files")),
        "trace_artifacts": trace_artifacts,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
        "reason": f"BLK-test did not run because BLK-pipe source_status was {source_status}",
    }


def send_blk_test_mcp_request(request: dict[str, Any], *, enabled: bool = False) -> dict[str, Any]:
    """Fail-closed send stub for future BLK-test MCP integration.

    This function deliberately performs no I/O and records that neither network
    nor subprocess execution occurred.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP send path is disabled in Sprint 006")

    return {
        "status": "BLOCKED",
        "reason": "live BLK-test MCP disabled in Sprint 006",
        "request": deepcopy(request),
        "network_called": False,
        "subprocess_called": False,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }


def map_blk_test_mcp_response(
    response: dict[str, Any],
    *,
    source_request: dict[str, Any],
) -> dict[str, Any]:
    """Normalize a future BLK-test MCP response against exact source evidence.

    PASS/FAIL-shaped data must be bound to the disabled source request that would
    have carried the source BLK-pipe SUCCESS evidence. BLOCKED mappings preserve
    source trace artifacts and remain draft/fixture-only.
    """
    source = _validated_source_request(source_request)
    status = str(response.get("status", ""))
    if status not in _VALID_MCP_RESPONSE_STATUSES:
        raise ValueError(f"unknown BLK-test MCP response status: {status}")

    if status in _VERDICT_MCP_RESPONSE_STATUSES:
        if source["source_status"] != _SUCCESS_SOURCE_STATUS:
            raise ValueError("PASS/FAIL mapping requires source_request source_status SUCCESS")
        _require_response_matches_source(response, source, "beb_id")
        _require_response_matches_source(response, source, "commit_hash")
        _require_response_matches_source(response, source, "pre_engine_hash")
        response_trace_artifacts = _trace_artifacts(response)
        if response_trace_artifacts != source["trace_artifacts"]:
            raise ValueError("response trace_artifacts must match source_request trace_artifacts")
        checks = response.get("checks")
        if not isinstance(checks, list) or not checks:
            raise ValueError("PASS/FAIL mapping requires non-empty checks")
    else:
        response_trace = response.get("trace_artifacts")
        if isinstance(response_trace, list) and response_trace:
            _trace_artifacts(response)
        checks = response.get("checks") if isinstance(response.get("checks"), list) else []

    return {
        "status": status,
        "source": "blk-test-mcp-response-shape",
        "beb_id": source["beb_id"],
        "commit_hash": source["commit_hash"],
        "pre_engine_hash": source["pre_engine_hash"],
        "trace_artifacts": deepcopy(source["trace_artifacts"]),
        "checks": deepcopy(checks),
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }


def _validate_context(*, beb_id: str, target_branch: str, trace_hash: str) -> None:
    for label, value in (("beb_id", beb_id), ("target_branch", target_branch)):
        if not value or not value.strip():
            raise ValueError(f"{label} is required")
        if _TOKEN_UNSAFE_PATTERN.search(value):
            raise ValueError(f"{label} must not contain whitespace")
    if not _TRACE_HASH_PATTERN.match(trace_hash):
        raise ValueError("trace_hash must match sha256:<64-lowercase-hex>")


def _validate_canonical_trace_hash(label: str, value: str) -> None:
    if not _TRACE_HASH_PATTERN.match(value):
        raise ValueError(f"{label} must match sha256:<64-lowercase-hex>")


def _source_status(source: dict[str, Any], *, field: str) -> str:
    status = str(source.get(field, "")).strip()
    if not status:
        raise ValueError(f"{field} is required")
    if status not in _VALID_SOURCE_STATUSES:
        raise ValueError(f"unknown BLK-pipe status: {status}")
    return status


def _required_text(source: dict[str, Any], field: str) -> str:
    value = str(source.get(field, "")).strip()
    if not value:
        raise ValueError(f"{field} is required")
    return value


def _required_string_list(source: dict[str, Any], field: str) -> list[str]:
    values = _string_list(source.get(field))
    if not values or any(not item.strip() for item in values):
        raise ValueError(f"{field} is required")
    return values


def _required_trace_artifacts(source: dict[str, Any], *, owner: str) -> list[dict[str, str]]:
    trace_artifacts = _trace_artifacts(source)
    if not trace_artifacts:
        raise ValueError(f"{owner} must include non-empty trace_artifacts")
    return trace_artifacts


def _validated_source_request(source_request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(source_request, dict):
        raise TypeError("source_request must be a dict")

    source_status = _source_status(source_request, field="source_status")
    beb_id = _required_text(source_request, "beb_id")
    pre_engine_hash = _required_text(source_request, "pre_engine_hash")
    trace_artifacts = _required_trace_artifacts(source_request, owner="source_request")
    method = str(source_request.get("method", ""))

    if source_status == _SUCCESS_SOURCE_STATUS:
        commit_hash = _required_text(source_request, "commit_hash")
        staged_files = _required_string_list(source_request, "staged_files")
    else:
        if method == _EVALUATE_METHOD:
            raise ValueError("non-SUCCESS source_request must not claim a BLK-test evaluation request")
        commit_hash = str(source_request.get("commit_hash", "")).strip()
        staged_files = _string_list(source_request.get("staged_files"))

    return {
        "source_status": source_status,
        "beb_id": beb_id,
        "commit_hash": commit_hash,
        "pre_engine_hash": pre_engine_hash,
        "staged_files": staged_files,
        "trace_artifacts": trace_artifacts,
        "method": method or (_EVALUATE_METHOD if source_status == _SUCCESS_SOURCE_STATUS else _NOT_RUN_METHOD),
    }


def _require_response_matches_source(response: dict[str, Any], source: dict[str, Any], field: str) -> None:
    if str(response.get(field, "")) != source[field]:
        raise ValueError(f"response {field} must match source_request {field}")


def _trace_artifacts(source: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = source.get("trace_artifacts")
    if not isinstance(artifacts, list):
        return []
    safe_artifacts: list[dict[str, str]] = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be an object")
        kind = str(artifact.get("kind", ""))
        artifact_id = str(artifact.get("id", ""))
        version_hash = str(artifact.get("version_hash", ""))
        if not kind or not artifact_id or not version_hash:
            raise ValueError(f"trace_artifacts[{index}] must include kind, id, and version_hash")
        _validate_canonical_trace_hash(f"trace_artifacts[{index}].version_hash", version_hash)
        safe_artifacts.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
            }
        )
    return safe_artifacts


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]
