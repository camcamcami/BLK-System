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
_VALID_MCP_RESPONSE_STATUSES = {"PASS", "FAIL", "BLOCKED"}
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_TOKEN_UNSAFE_PATTERN = re.compile(r"\s")


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

    The live send path is intentionally unavailable in Sprint 005. Passing
    `enabled=True` raises instead of opening a socket, spawning MCP, or calling a
    service.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP is disabled in Sprint 005")

    return {
        "enabled": False,
        "transport": "DISABLED_STUB",
        "method": "blk_test.evaluate_execution",
        "source_status": str(source_report.get("status", "")),
        "beb_id": str(source_report.get("beb_id", "")),
        "commit_hash": str(source_report.get("commit_hash", "")),
        "pre_engine_hash": str(source_report.get("pre_engine_hash", "")),
        "staged_files": _string_list(source_report.get("staged_files")),
        "destroyed_files": _string_list(source_report.get("destroyed_files")),
        "trace_artifacts": _trace_artifacts(source_report),
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
        "reason": "live BLK-test MCP disabled in Sprint 005",
    }


def send_blk_test_mcp_request(request: dict[str, Any], *, enabled: bool = False) -> dict[str, Any]:
    """Fail-closed send stub for future BLK-test MCP integration.

    This function deliberately performs no I/O and records that neither network
    nor subprocess execution occurred.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP send path is disabled in Sprint 005")

    return {
        "status": "BLOCKED",
        "reason": "live BLK-test MCP disabled in Sprint 005",
        "request": deepcopy(request),
        "network_called": False,
        "subprocess_called": False,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }


def map_blk_test_mcp_response(response: dict[str, Any]) -> dict[str, Any]:
    """Normalize the future live BLK-test MCP response shape into fixture terms."""
    status = str(response.get("status", ""))
    if status not in _VALID_MCP_RESPONSE_STATUSES:
        raise ValueError(f"unknown BLK-test MCP response status: {status}")
    return {
        "status": status,
        "source": "blk-test-mcp-response-shape",
        "beb_id": str(response.get("beb_id", "")),
        "commit_hash": str(response.get("commit_hash", "")),
        "pre_engine_hash": str(response.get("pre_engine_hash", "")),
        "trace_artifacts": _trace_artifacts(response),
        "checks": deepcopy(response.get("checks", [])) if isinstance(response.get("checks"), list) else [],
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
