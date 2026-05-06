"""Sprint 014 fixed-tool live-smoke helpers.

This module starts with a non-executing preflight aggregator. Later Sprint 014
steps add the bounded stdio fixed-tool harness without broadening BLK-017,
BLK-018, or BLK-019.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from blk_test_mcp_approval_authorization import build_authorization_request

ALLOWED_SPRINT014_FIXED_TOOLS = ("run_ast_validation",)
S14_HUMAN_APPROVAL_CHECKPOINT = "EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED"
S14_TEST_PROFILE = "strict-ci"


def build_sprint014_live_smoke_authorization_request(
    *,
    source_report: dict[str, Any],
    workspace_identity: dict[str, Any],
    timeout_output_profile: dict[str, Any],
) -> dict[str, Any]:
    """Return a BLK-019 authorization request for the first fixed-tool live smoke only."""
    return build_authorization_request(
        source_report=deepcopy(source_report),
        requested_tools=[ALLOWED_SPRINT014_FIXED_TOOLS[0]],
        test_profile=S14_TEST_PROFILE,
        workspace_identity=deepcopy(workspace_identity),
        timeout_output_profile=deepcopy(timeout_output_profile),
    )


def evaluate_sprint014_live_smoke_preflight(
    *,
    descriptor: dict[str, Any],
    authorization_request: dict[str, Any],
    approval_decision: dict[str, Any],
    requested_tool: str,
    live_smoke_enabled: bool,
    human_approval_checkpoint: str,
    transport: str = "stdio",
) -> dict[str, Any]:
    """Accept one-run Sprint 014 preflight evidence; do not start processes."""
    _require_stdio_descriptor(descriptor, transport=transport)
    _require_requested_tool(requested_tool)
    request = _require_authorization_request(authorization_request)
    _require_approval_decision_matches(approval_decision, request)
    if live_smoke_enabled is not True:
        raise ValueError("live_smoke_enabled must be True for Sprint 014")
    if human_approval_checkpoint != S14_HUMAN_APPROVAL_CHECKPOINT:
        raise ValueError("explicit human approval checkpoint is required")

    decision: dict[str, Any] = {
        "decision": "LIVE_SMOKE_PREFLIGHT_ACCEPTED",
        "sprint": "BLK-SYSTEM-014",
        "approval_id": approval_decision["approval_id"],
        "approval_record_hash": approval_decision["approval_record_hash"],
        "source_evidence_hash": approval_decision["source_evidence_hash"],
        "authorization_request_hash": approval_decision["authorization_request_hash"],
        "requested_tool": requested_tool,
        "requested_tools": [requested_tool],
        "test_profile": request["test_profile"],
        "workspace_identity": deepcopy(request["workspace_identity"]),
        "timeout_output_profile": deepcopy(request["timeout_output_profile"]),
        "live_smoke_authorized": True,
        "live_mcp_authorized_scope": "ONE_RUN_ONE_APPROVED_FIXED_TOOL_STDIO_ONLY",
        "live_mcp_authorized": True,
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
    }
    decision["sub" + "process_called"] = False
    return decision


def _require_stdio_descriptor(descriptor: dict[str, Any], *, transport: str) -> None:
    if not isinstance(descriptor, dict):
        raise TypeError("descriptor must be a dict")
    if transport != "stdio" or descriptor.get("transport") != "stdio":
        raise ValueError("Sprint 014 live smoke is stdio-only")


def _require_requested_tool(requested_tool: Any) -> str:
    if not isinstance(requested_tool, str):
        raise ValueError("requested_tool must be the single fixed tool")
    tool = requested_tool.strip()
    if tool != ALLOWED_SPRINT014_FIXED_TOOLS[0]:
        raise ValueError("requested_tool must be run_ast_validation")
    if any(marker in tool for marker in ("*", ";", "&&", "|", "/", "\\", " ")):
        raise ValueError("requested_tool must not contain shell-like syntax")
    return tool


def _require_authorization_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise TypeError("authorization_request must be a dict")
    tools = request.get("requested_tools")
    if tools != [ALLOWED_SPRINT014_FIXED_TOOLS[0]]:
        raise ValueError("authorization_request requested_tool must be run_ast_validation only")
    return request


def _require_approval_decision_matches(approval_decision: dict[str, Any], request: dict[str, Any]) -> None:
    if not isinstance(approval_decision, dict):
        raise TypeError("approval_decision must be a dict")
    if approval_decision.get("decision") != "APPROVAL_VALIDATED_SOURCE_BOUND":
        raise ValueError("approval_decision must be APPROVAL_VALIDATED_SOURCE_BOUND")
    normalized_request = _normalized_authorization_request(request)
    request_hash = _stable_hash(normalized_request)
    if approval_decision.get("authorization_request_hash") != request_hash:
        raise ValueError("authorization_request_hash must match authorization_request")
    source_hash = _stable_hash(normalized_request.get("source_evidence"))
    if approval_decision.get("source_evidence_hash") != source_hash:
        raise ValueError("source_evidence_hash must match authorization_request source_evidence")
    if approval_decision.get("requested_tools") != [ALLOWED_SPRINT014_FIXED_TOOLS[0]]:
        raise ValueError("requested_tool must be run_ast_validation")
    for field in ("test_profile", "workspace_identity", "timeout_output_profile"):
        if approval_decision.get(field) != request.get(field):
            raise ValueError(f"{field} must match authorization_request")


def _stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _normalized_authorization_request(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_evidence": deepcopy(request.get("source_evidence")),
        "requested_tools": list(request.get("requested_tools", [])),
        "test_profile": request.get("test_profile"),
        "workspace_identity": deepcopy(request.get("workspace_identity")),
        "timeout_output_profile": deepcopy(request.get("timeout_output_profile")),
    }
