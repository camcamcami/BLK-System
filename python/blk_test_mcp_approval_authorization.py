"""BLK-test MCP approval/source-evidence authorization helpers.

Sprint 013 keeps this module dependency-free and non-executing. It validates
BLK-test-specific approval records as local evidence only; it never starts live
MCP transport, spawns processes, calls networks, mutates source, publishes BEOs,
generates RTM, or reads protected BLK-req vault bodies.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

ALLOWED_FIXED_TOOLS = (
    "run_ast_validation",
    "run_ipc_race_test",
    "run_svg_export_purity_test",
    "run_architecture_lint",
)

_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_PROTECTED_BODY_MARKERS = (
    "docs/active/",
    "docs/requirements/",
    "docs/use_cases/",
    "active_vault_body",
    "protected_body",
)
_CODEX_LIVE_MARKERS = ("codex-live", "BLK_APPROVE_CODEX_LIVE")
_FORBIDDEN_AUTHORITY_FIELDS = (
    "shell",
    "command",
    "exec",
    "eval",
    "source_mutation",
    "source_write",
    "staging",
    "commit",
    "push",
    "publish_beo",
    "generate_rtm",
    "active_vault_body",
)


def build_authorization_request(
    *,
    source_report: dict[str, Any],
    requested_tools: list[str],
    test_profile: str = "strict-ci",
    workspace_identity: dict[str, Any] | None = None,
    timeout_output_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a normalized source/request envelope for approval validation only."""
    _reject_protected_body_references(source_report)
    tools = _requested_tools(requested_tools)
    source_evidence = _source_evidence(source_report)
    profile = _required_text({"test_profile": test_profile}, "test_profile")
    workspace = _required_dict(
        workspace_identity,
        "workspace_identity",
        required=("target_branch", "workspace_clone_id", "source_path_policy"),
    )
    timeout_output = _required_dict(
        timeout_output_profile,
        "timeout_output_profile",
        required=("timeout_class", "timeout_seconds", "output_byte_limit", "compression"),
    )
    return {
        "source_evidence": source_evidence,
        "requested_tools": tools,
        "test_profile": profile,
        "workspace_identity": workspace,
        "timeout_output_profile": timeout_output,
        **_no_authority_fields(),
    }


def validate_blk_test_approval_record(
    approval_record: dict[str, Any],
    authorization_request: dict[str, Any],
    *,
    now: str,
    used_approval_ids: set[str] | list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Return source-bound approval evidence or raise; never starts live transport."""
    if not isinstance(approval_record, dict):
        raise TypeError("approval_record must be a dict")
    if not isinstance(authorization_request, dict):
        raise TypeError("authorization_request must be a dict")
    _reject_codex_live_approval(approval_record)
    _reject_protected_body_references(approval_record)
    _reject_forbidden_authority_fields(approval_record)

    approval_id = _required_text(approval_record, "approval_id")
    operator_identity = _required_text(approval_record, "operator_identity")
    approval_timestamp = _required_text(approval_record, "approval_timestamp")
    _required_text(approval_record, "approval_kind")
    _required_text(approval_record, "issued_at")
    _required_text(approval_record, "expires_at")
    _required_text({"now": now}, "now")

    request = _authorization_request(authorization_request)
    approval_source = _approval_source_evidence(approval_record)
    approval_tools = _requested_tools(approval_record.get("requested_tools"))
    approval_profile = _required_text(approval_record, "test_profile")
    approval_workspace = _required_dict(
        approval_record.get("workspace_identity"),
        "workspace_identity",
        required=("target_branch", "workspace_clone_id", "source_path_policy"),
    )
    approval_timeout_output = _required_dict(
        approval_record.get("timeout_output_profile"),
        "timeout_output_profile",
        required=("timeout_class", "timeout_seconds", "output_byte_limit", "compression"),
    )
    _require_equal("source_report_identity", approval_source["source_report_identity"], request["source_evidence"]["source_report_identity"])
    _require_equal("beb_id", approval_source["beb_id"], request["source_evidence"]["beb_id"])
    _require_equal("commit_hash", approval_source["commit_hash"], request["source_evidence"]["commit_hash"])
    _require_equal("pre_engine_hash", approval_source["pre_engine_hash"], request["source_evidence"]["pre_engine_hash"])
    _require_equal("trace_artifacts", approval_source["trace_artifacts"], request["source_evidence"]["trace_artifacts"])
    _require_equal("requested_tools", approval_tools, request["requested_tools"])
    _require_equal("test_profile", approval_profile, request["test_profile"])
    _require_equal("workspace_identity", approval_workspace, request["workspace_identity"])
    _require_equal("timeout_output_profile", approval_timeout_output, request["timeout_output_profile"])

    decision = {
        "decision": "APPROVAL_VALIDATED_SOURCE_BOUND",
        "approval_id": approval_id,
        "operator_identity": operator_identity,
        "approval_timestamp": approval_timestamp,
        "source_evidence": deepcopy(request["source_evidence"]),
        "requested_tools": list(request["requested_tools"]),
        "test_profile": request["test_profile"],
        "workspace_identity": deepcopy(request["workspace_identity"]),
        "timeout_output_profile": deepcopy(request["timeout_output_profile"]),
        **_no_authority_fields(),
    }
    return decision


def _source_evidence(source_report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(source_report, dict):
        raise TypeError("source_report must be a dict")
    if str(source_report.get("status", "")).strip() != "SUCCESS":
        raise ValueError("source_report status SUCCESS is required")
    identity = _required_dict(
        source_report.get("source_report_identity"),
        "source_report_identity",
        required=("report_path", "report_hash", "report_id"),
    )
    report_hash = str(identity["report_hash"])
    if not _TRACE_HASH_PATTERN.match(report_hash):
        raise ValueError("source_report_identity.report_hash must match sha256:<64-lowercase-hex>")
    return {
        "source_report_identity": identity,
        "beb_id": _required_text(source_report, "beb_id"),
        "commit_hash": _required_text(source_report, "commit_hash"),
        "pre_engine_hash": _canonical_hash(source_report, "pre_engine_hash"),
        "trace_artifacts": _trace_artifacts(source_report),
    }


def _approval_source_evidence(approval_record: dict[str, Any]) -> dict[str, Any]:
    evidence = approval_record.get("source_evidence")
    if not isinstance(evidence, dict):
        raise ValueError("source_evidence is required")
    return {
        "source_report_identity": _required_dict(
            evidence.get("source_report_identity"),
            "source_report_identity",
            required=("report_path", "report_hash", "report_id"),
        ),
        "beb_id": _required_text(evidence, "beb_id"),
        "commit_hash": _required_text(evidence, "commit_hash"),
        "pre_engine_hash": _canonical_hash(evidence, "pre_engine_hash"),
        "trace_artifacts": _trace_artifacts(evidence),
    }


def _authorization_request(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_evidence": _approval_source_evidence({"source_evidence": request.get("source_evidence")}),
        "requested_tools": _requested_tools(request.get("requested_tools")),
        "test_profile": _required_text(request, "test_profile"),
        "workspace_identity": _required_dict(
            request.get("workspace_identity"),
            "workspace_identity",
            required=("target_branch", "workspace_clone_id", "source_path_policy"),
        ),
        "timeout_output_profile": _required_dict(
            request.get("timeout_output_profile"),
            "timeout_output_profile",
            required=("timeout_class", "timeout_seconds", "output_byte_limit", "compression"),
        ),
    }


def _requested_tools(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("requested_tools is required")
    tools = [str(item).strip() for item in value]
    if any(not item for item in tools):
        raise ValueError("requested_tools entries must be non-empty")
    if any(item not in ALLOWED_FIXED_TOOLS for item in tools):
        raise ValueError("requested_tools must be fixed BLK-test tool names")
    if len(set(tools)) != len(tools):
        raise ValueError("requested_tools must not contain duplicates")
    return tools


def _trace_artifacts(source: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = source.get("trace_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("canonical trace_artifacts are required")
    safe = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be an object")
        kind = str(artifact.get("kind", "")).strip()
        artifact_id = str(artifact.get("id", "")).strip()
        version_hash = str(artifact.get("version_hash", "")).strip()
        if not kind or not artifact_id or not version_hash:
            raise ValueError(f"trace_artifacts[{index}] must include kind, id, and version_hash")
        if not _TRACE_HASH_PATTERN.match(version_hash):
            raise ValueError(f"trace_artifacts[{index}].version_hash must match sha256:<64-lowercase-hex>")
        safe.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return safe


def _required_dict(value: Any, field: str, *, required: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} is required")
    result = deepcopy(value)
    for key in required:
        if key not in result or str(result[key]).strip() == "":
            raise ValueError(f"{field}.{key} is required")
    return result


def _required_text(source: dict[str, Any], field: str) -> str:
    value = str(source.get(field, "")).strip()
    if not value:
        raise ValueError(f"{field} is required")
    return value


def _canonical_hash(source: dict[str, Any], field: str) -> str:
    value = _required_text(source, field)
    if not _TRACE_HASH_PATTERN.match(value):
        raise ValueError(f"{field} must match sha256:<64-lowercase-hex>")
    return value


def _reject_codex_live_approval(value: Any) -> None:
    text = str(value)
    for marker in _CODEX_LIVE_MARKERS:
        if marker in text:
            raise ValueError("codex-live approval is not BLK-test MCP approval")


def _reject_protected_body_references(value: Any) -> None:
    text = str(value)
    for marker in _PROTECTED_BODY_MARKERS:
        if marker in text:
            raise ValueError("protected BLK-req vault body references are not allowed")


def _reject_forbidden_authority_fields(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            for marker in _FORBIDDEN_AUTHORITY_FIELDS:
                if marker == key_text:
                    raise ValueError(f"{marker} authority is not allowed")
            _reject_forbidden_authority_fields(nested)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_authority_fields(item)


def _require_equal(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise ValueError(f"{label} must match authorization_request")


def _no_authority_fields() -> dict[str, Any]:
    fields = {
        "live_mcp_authorized": False,
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
    fields["sub" + "process_called"] = False
    return fields
