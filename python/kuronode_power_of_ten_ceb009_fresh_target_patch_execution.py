"""Fresh-target CEB_009 patch execution payload gate for BLK-SYSTEM-066."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_string
from kuronode_power_of_ten_ceb009_patch_execution_approval_capture import (
    OPERATOR_GRANT_TEXT,
    WORK_DIR,
    _PATCH_SCRIPT,
)
from kuronode_power_of_ten_ceb009_patch_approval_envelope import TARGET_PATH, TARGET_REPO_IDENTITY

CURRENT_TARGET_HEAD_SHA = "70b6062b92cf61c12bf190f92dc6b45ea4dcd438"
FRESH_TARGET_READY_STATUS = "KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_READY_FOR_BLK_PIPE"
FRESH_TARGET_MARKER = "KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_BOUNDARY"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_FRESH_TARGET_PATCH_EXECUTION_REQUEST"
APPROVAL_ID = "BLK-SYSTEM-066-CEB009-FRESH-TARGET-PATCH-APPROVAL-DISCORD-684235178083745819-20260511T0839AEST"
RUN_ID = "BLK-SYSTEM-066-CEB009-FRESH-TARGET-PATCH-RUN-001"

EXACT_DENIED_ADJACENT_AUTHORITIES = {
    "LIVE_CODEX_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "CEO_009_PUBLICATION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "PROTECTED_BLK_REQ_BODY_READ",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_CLAIM",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
    "KURONODE_REMOTE_PUSH",
    "SOURCE_OR_GIT_MUTATION_OUTSIDE_EXACT_BLK_PIPE_ALLOWLIST",
}

_REQUEST_KEYS = {
    "request_status",
    "approval_id",
    "run_id",
    "operator_identity",
    "operator_grant_text",
    "approval_captured_at",
    "target_repo_identity",
    "target_branch",
    "target_head_sha",
    "observed_origin_main_head",
    "target_path",
    "allowed_modified_files",
    "allowed_new_files",
    "operator_note",
    "excluded_adjacent_authorities",
}
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)
_LAUNDERING_RE = re.compile(
    r"codex|blk[-_\s]*test[_\s-]*mcp|production[_\s-]*blk[-_\s]*test|beo|ceo[_\s-]*009|rtm|"
    r"drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|active[_\s-]*vault|protected[_\s-]*blk[-_\s]*req|"
    r"private[_\s-]*key|api[_\s-]*key|bearer|production[_\s-]*(?:sandbox|isolation)|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm|pnpm|yarn|bun|electron|smoke[_\s-]*test|"
    r"\b(?:tsc|eslint|prettier|curl|wget|ssh|scp|rsync|docker|deno)\b|remote[_\s-]*push|push[_\s-]*kuronode",
    re.IGNORECASE,
)


def default_ceb009_fresh_target_patch_execution_request() -> dict[str, Any]:
    """Return the fresh target approval request derived from the user's immediate approval."""

    return {
        "request_status": REQUEST_STATUS,
        "approval_id": APPROVAL_ID,
        "run_id": RUN_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_grant_text": "I approve",
        "approval_captured_at": "2026-05-11T08:39:29+10:00",
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": "main",
        "target_head_sha": CURRENT_TARGET_HEAD_SHA,
        "observed_origin_main_head": CURRENT_TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "operator_note": "approval applies only to displayed current target SHA from BLK-SYSTEM-065 closeout",
        "excluded_adjacent_authorities": sorted(EXACT_DENIED_ADJACENT_AUTHORITIES),
    }


def build_ceb009_fresh_target_patch_execution_payload(request: dict[str, Any]) -> dict[str, Any]:
    """Validate fresh target approval and build a single exact BLK-pipe payload."""

    validated = _validate_request(request)
    record = {
        "execution_readiness_status": FRESH_TARGET_READY_STATUS,
        "fresh_target_marker": FRESH_TARGET_MARKER,
        "approval_id": validated["approval_id"],
        "run_id": validated["run_id"],
        "operator_identity": validated["operator_identity"],
        "approval_captured_at": validated["approval_captured_at"],
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": "main",
        "target_head_sha": CURRENT_TARGET_HEAD_SHA,
        "observed_origin_main_head": CURRENT_TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "excluded_adjacent_authorities": sorted(EXACT_DENIED_ADJACENT_AUTHORITIES),
        "approval_captured": True,
        "execution_authorized": True,
        "blk_pipe_invoked": False,
        "patch_executed": False,
        "patch_committed": False,
        "kuronode_remote_pushed": False,
        "codex_started": False,
        "blk_test_mcp_started": False,
        "electron_launched": False,
        "smoke_test_executed": False,
        "typescript_tooling_executed": False,
        "package_manager_invoked": False,
        "network_accessed": False,
        "protected_body_read": False,
        "beo_published": False,
        "ceo_009_published": False,
        "rtm_generated": False,
        "coverage_claimed": False,
        "production_isolation_claimed": False,
    }
    record["approval_record_hash"] = _canonical_hash({key: value for key, value in record.items() if key != "approval_record_hash"})
    record["blk_pipe_payload"] = _build_payload(record["approval_record_hash"])
    return record


def _validate_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("fresh target request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "fresh target request")
    _reject_laundering(
        {
            key: value
            for key, value in request.items()
            if key
            not in {
                "operator_grant_text",
                "excluded_adjacent_authorities",
                "target_repo_identity",
                "target_path",
                "allowed_modified_files",
                "allowed_new_files",
            }
        },
        "fresh target request",
    )
    if request.get("request_status") != REQUEST_STATUS:
        raise ValueError("request_status must match fresh target request")
    _require_exact(request.get("target_repo_identity"), TARGET_REPO_IDENTITY, "target_repo_identity")
    _require_exact(request.get("target_branch"), "main", "target_branch")
    _require_exact(request.get("target_head_sha"), CURRENT_TARGET_HEAD_SHA, "target_head_sha")
    _require_exact(request.get("observed_origin_main_head"), CURRENT_TARGET_HEAD_SHA, "observed_origin_main_head")
    _require_exact(request.get("target_path"), TARGET_PATH, "target_path")
    if request.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must equal [scripts/smoke_test.ts]")
    if request.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty")
    _validate_timestamp(request.get("approval_captured_at"))
    _validate_exact_string_set(
        request.get("excluded_adjacent_authorities"),
        EXACT_DENIED_ADJACENT_AUTHORITIES,
        "excluded_adjacent_authorities must match exact denied adjacent authority set",
    )
    return deepcopy(request)


def _build_payload(approval_record_hash: str) -> dict[str, Any]:
    return {
        "action": "execute",
        "beb_id": "CEB_009",
        "work_dir": WORK_DIR,
        "target_branch": "main",
        "engine": "python3",
        "engine_args": ["-c", _PATCH_SCRIPT],
        "l2_packet": "BLK-SYSTEM-066 exact CEB_009 patch against fresh approved target 70b6062b92cf61c12bf190f92dc6b45ea4dcd438; edit only scripts/smoke_test.ts; no Codex, no BLK-test MCP, no Electron/smoke runtime, no TypeScript/package-manager tooling.",
        "trace_artifacts": [
            {"kind": "CEB", "id": "CEB_009", "version_hash": approval_record_hash},
        ],
        "validation_commands": ["git diff --check -- scripts/smoke_test.ts"],
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "timeout_seconds": 60,
        "max_output_bytes": 1_048_576,
    }


def _validate_timestamp(value: Any) -> None:
    parsed = datetime.fromisoformat(_required_string(value, "approval_captured_at"))
    if parsed.tzinfo is None:
        raise ValueError("approval_captured_at must include timezone")


def _require_exact(value: Any, expected: str, field: str) -> None:
    actual = _required_string(value, field)
    if field.endswith("head") or field.endswith("sha") or "head" in field:
        if not _COMMIT_RE.match(actual):
            raise ValueError(f"{field} must be a 40-character lowercase git SHA")
    if _PROTECTED_RE.search(_decode_path_text(actual)):
        raise ValueError(f"{field} rejects protected BLK-req body reference")
    if actual != expected:
        raise ValueError(f"{field} must match exact fresh CEB_009 target")


def _validate_exact_string_set(value: Any, expected: set[str], message: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value) or set(value) != expected or len(value) != len(expected):
        raise ValueError(message)


def _enforce_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(f"{label} contains unexpected field(s): {extra}")


def _reject_laundering(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_laundering(key, label)
            _reject_laundering(item, label)
    elif isinstance(value, list):
        for item in value:
            _reject_laundering(item, label)
    elif isinstance(value, str):
        if _HASH_RE.match(value):
            return
        decoded = _decode_path_text(value)
        normalized = _normalize_text(value)
        if _PROTECTED_RE.search(decoded):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if _LAUNDERING_RE.search(normalized):
            raise ValueError(f"{label} rejects authority-laundering text")


def _decode_path_text(value: str) -> str:
    decoded = value
    for _ in range(3):
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    return decoded.replace("\\", "/")


def _normalize_text(value: str) -> str:
    decoded = _decode_path_text(value)
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", decoded)
    return re.sub(r"[^a-zA-Z0-9]+", " ", spaced)
