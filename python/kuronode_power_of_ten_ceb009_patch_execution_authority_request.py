"""CEB_009 patch execution authority-request fixture.

This module converts the BLK-SYSTEM-063 blocked patch execution preflight into a
review package for a future explicit human decision. It does not capture approval,
patch Kuronode, invoke BLK-pipe, start Codex or BLK-test MCP, scan a live
checkout, launch Electron, run smoke tests, execute TypeScript tooling, publish
BEO/CEO artifacts, generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_ceb009_patch_execution_preflight import (
    BLOCK_REASON as PREFLIGHT_BLOCK_REASON,
    EXACT_EXCLUDED_AUTHORITIES as PREFLIGHT_EXACT_EXCLUDED_AUTHORITIES,
    PREFLIGHT_MARKER,
    PREFLIGHT_STATUS,
    TARGET_BRANCH,
    TARGET_HEAD_SHA,
    TARGET_PATH,
    TARGET_REPO_IDENTITY,
)

AUTHORITY_REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_READY_FOR_HUMAN_DECISION_NOT_EXECUTED"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_FIXTURE_ONLY"
AUTHORITY_REQUEST_SCOPE = "CEB_009_PATCH_EXECUTION_AUTHORITY_REQUEST_REVIEW_ONLY"
AUTHORITY_REQUEST_MARKER = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_AUTHORITY_REQUEST_BOUNDARY"
DECISION_REQUIRED = "EXPLICIT_HUMAN_PATCH_EXECUTION_DECISION_REQUIRED"

REQUIRED_FUTURE_APPROVAL_OBLIGATIONS = {
    "EXACT_OPERATOR_APPROVAL_ID_REQUIRED",
    "EXACT_RUN_ID_REQUIRED",
    "EXPIRY_REQUIRED",
    "REPLAY_LEDGER_REQUIRED",
    "OPERATOR_STOP_REQUIRED",
    "ROLLBACK_EXPECTATION_REQUIRED",
    "CLEANUP_EXPECTATION_REQUIRED",
    "OUTPUT_BOUND_REQUIRED",
    "OUTCOME_DOCUMENT_REQUIRED",
    "HOSTILE_REVIEW_REQUIRED",
    "NO_PATCH_EXECUTED_BY_REQUEST",
    "NO_RUNTIME_VALIDATION_BY_REQUEST",
}
REQUIRED_FUTURE_VALIDATION_PROFILE_IDS = {
    "kuronode-power-of-ten-static-fixture-only",
    "ceb009-smoke-timeout-path-static-review-fixture-only",
}
EXACT_EXCLUDED_AUTHORITIES = set(PREFLIGHT_EXACT_EXCLUDED_AUTHORITIES) | {
    "HUMAN_PATCH_APPROVAL_CAPTURED",
    "PATCH_EXECUTION_AUTHORIZED",
    "PATCH_EXECUTION_REQUEST_EXECUTED",
    "VALIDATION_PROFILE_COMMAND_EXECUTION",
    "CEO_009_PUBLICATION",
}

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "authority_request_scope",
    "preflight_hash",
    "expected_preflight_status",
    "expected_preflight_marker",
    "approval_captured",
    "requested_at",
    "future_approval_obligations",
    "future_validation_profile_ids",
    "operator_note",
    "evidence_ref",
    "excluded_authorities",
}
_PREFLIGHT_KEYS = {
    "preflight_status",
    "preflight_scope",
    "preflight_marker",
    "request_id",
    "operator_identity",
    "requested_at",
    "envelope_hash",
    "envelope_status",
    "integrity_hardening_markers",
    "remediation_packet_hash_recomputed",
    "target_repo_identity",
    "target_branch",
    "target_head_sha",
    "target_path",
    "allowed_modified_files",
    "allowed_new_files",
    "required_remediation_obligations",
    "proof_markers",
    "excluded_authorities",
    "execution_blocked",
    "block_reason",
    "explicit_human_patch_approval_present",
    "approval_granted",
    "patch_executed",
    "patch_applied",
    "source_mutation_performed",
    "git_mutation_performed",
    "blk_pipe_invoked",
    "codex_started",
    "blk_test_mcp_started",
    "live_kuronode_scan_performed",
    "live_kuronode_source_validation_performed",
    "electron_launched",
    "smoke_test_executed",
    "timeout_path_waited",
    "typescript_tooling_executed",
    "package_manager_invoked",
    "network_accessed",
    "protected_body_read",
    "beo_published",
    "rtm_generated",
    "coverage_claimed",
    "production_isolation_claimed",
    "preflight_hash",
}
_SIDE_EFFECT_FLAGS = {
    "explicit_human_patch_approval_present",
    "approval_granted",
    "patch_executed",
    "patch_applied",
    "source_mutation_performed",
    "git_mutation_performed",
    "blk_pipe_invoked",
    "codex_started",
    "blk_test_mcp_started",
    "live_kuronode_scan_performed",
    "live_kuronode_source_validation_performed",
    "electron_launched",
    "smoke_test_executed",
    "timeout_path_waited",
    "typescript_tooling_executed",
    "package_manager_invoked",
    "network_accessed",
    "protected_body_read",
    "beo_published",
    "rtm_generated",
    "coverage_claimed",
    "production_isolation_claimed",
}

_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_LAUNDERING_RE = re.compile(
    r"approved[_\s-]*for[_\s-]*live[_\s-]*execution|runtime[_\s-]*(?:pilot|execution)[_\s-]*(?:approved|authorized|authorised|allowed)|"
    r"patch[_\s-]*(?:approved|granted|authorized|authorised|applied|execution|kuronode)|approval[_\s-]*(?:granted|captured|inherited)|"
    r"human[_\s-]*approval[_\s-]*(?:captured|accepted)|execute[_\s-]*(?:patch|runner)|invoke[_\s-]*blk[-_\s]*pipe|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s-]*run[_\s-]*test:?smoke|test:?smoke|"
    r"electron[_\s-]*(?:launch|started|executed)|smoke[_\s-]*test[_\s-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s]*pipe|blk[-_\s]*test[_\s-]*mcp|beo[_\s-]*publication|authoritative[_\s-]*beo|ceo[_\s-]*009|"
    r"rtm(?:id|generation|generated)?|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|protected[_\s-]*blk[-_\s]*req[_\s-]*body|"
    r"private[_\s-]*key|api[_\s-]*key|bearer|production[_\s-]*(?:sandbox|isolation)",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)


def default_ceb009_patch_execution_authority_request(preflight: dict[str, Any]) -> dict[str, Any]:
    """Return a valid review-only authority-request package request."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-064-CEB009-PATCH-EXECUTION-AUTHORITY-REQUEST-001",
        "operator_identity": "discord:684235178083745819",
        "authority_request_scope": AUTHORITY_REQUEST_SCOPE,
        "preflight_hash": _required_hash(preflight.get("preflight_hash"), "preflight.preflight_hash"),
        "expected_preflight_status": PREFLIGHT_STATUS,
        "expected_preflight_marker": PREFLIGHT_MARKER,
        "approval_captured": False,
        "requested_at": "2026-05-11T07:26:00+10:00",
        "future_approval_obligations": sorted(REQUIRED_FUTURE_APPROVAL_OBLIGATIONS),
        "future_validation_profile_ids": sorted(REQUIRED_FUTURE_VALIDATION_PROFILE_IDS),
        "operator_note": "human-decision request package only; no approval accepted and no execution performed",
        "evidence_ref": "BLK-SYSTEM-064-local-authority-request-fixture",
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }


def build_ceb009_patch_execution_authority_request(*, preflight: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic human-decision request without authorizing execution."""

    validated_preflight = _validate_preflight(preflight)
    validated_request = _validate_request(request, validated_preflight)
    authority_request = {
        "authority_request_status": AUTHORITY_REQUEST_STATUS,
        "authority_request_scope": AUTHORITY_REQUEST_SCOPE,
        "authority_request_marker": AUTHORITY_REQUEST_MARKER,
        "decision_required": DECISION_REQUIRED,
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "requested_at": validated_request["requested_at"],
        "preflight_hash": validated_preflight["preflight_hash"],
        "preflight_status": PREFLIGHT_STATUS,
        "preflight_marker": PREFLIGHT_MARKER,
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "future_approval_obligations": sorted(REQUIRED_FUTURE_APPROVAL_OBLIGATIONS),
        "future_validation_profile_ids": sorted(REQUIRED_FUTURE_VALIDATION_PROFILE_IDS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "approval_captured": False,
        "execution_authorized": False,
        "patch_executed": False,
        "patch_applied": False,
        "source_mutation_performed": False,
        "git_mutation_performed": False,
        "blk_pipe_invoked": False,
        "codex_started": False,
        "blk_test_mcp_started": False,
        "live_kuronode_scan_performed": False,
        "live_kuronode_source_validation_performed": False,
        "electron_launched": False,
        "smoke_test_executed": False,
        "timeout_path_waited": False,
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
    authority_request["authority_request_hash"] = _canonical_hash(
        {key: value for key, value in authority_request.items() if key != "authority_request_hash"}
    )
    return authority_request


def _validate_preflight(preflight: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(preflight, dict):
        raise ValueError("preflight must be a dictionary")
    supplied_hash = _required_hash(preflight.get("preflight_hash"), "preflight.preflight_hash")
    recomputed_hash = _canonical_hash({key: value for key, value in preflight.items() if key != "preflight_hash"})
    if supplied_hash != recomputed_hash:
        raise ValueError("preflight hash mismatch after recomputation")
    for key, value in preflight.items():
        if key in {
            "preflight_hash",
            "preflight_status",
            "preflight_scope",
            "preflight_marker",
            "request_id",
            "envelope_status",
            "integrity_hardening_markers",
            "required_remediation_obligations",
            "proof_markers",
            "excluded_authorities",
            "block_reason",
        }:
            continue
        if key not in _PREFLIGHT_KEYS:
            _reject_laundering(key, "preflight")
        _reject_laundering(value, "preflight")
    _enforce_keys(preflight, _PREFLIGHT_KEYS, "preflight")
    if preflight.get("preflight_status") != PREFLIGHT_STATUS:
        raise ValueError("preflight must have BLK-SYSTEM-063 blocked status")
    if preflight.get("preflight_marker") != PREFLIGHT_MARKER:
        raise ValueError("preflight marker must match BLK-SYSTEM-063 refusal boundary")
    if preflight.get("execution_blocked") is not True or preflight.get("block_reason") != PREFLIGHT_BLOCK_REASON:
        raise ValueError("preflight must remain blocked pending human approval")
    _validate_target(preflight)
    _validate_exact_string_set(
        preflight.get("excluded_authorities"),
        PREFLIGHT_EXACT_EXCLUDED_AUTHORITIES,
        "preflight excluded_authorities must match exact denied authority set",
    )
    for flag in sorted(_SIDE_EFFECT_FLAGS):
        if preflight.get(flag) is not False:
            raise ValueError(f"preflight contains side effect: {flag}")
    validated = deepcopy(preflight)
    validated["preflight_hash"] = recomputed_hash
    return validated


def _validate_request(request: dict[str, Any], preflight: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority request must be a dictionary")
    for key, value in request.items():
        if key not in _REQUEST_KEYS:
            _reject_laundering(key, "authority request")
        if key not in {
            "request_status",
            "request_id",
            "authority_request_scope",
            "expected_preflight_status",
            "expected_preflight_marker",
            "future_approval_obligations",
            "future_validation_profile_ids",
            "excluded_authorities",
        }:
            _reject_laundering(value, "authority request")
    _enforce_keys(request, _REQUEST_KEYS, "authority request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be CEB_009 patch execution authority request fixture only")
    if _required_string(request.get("authority_request_scope"), "authority_request_scope") != AUTHORITY_REQUEST_SCOPE:
        raise ValueError("authority_request_scope must be review-only")
    if _required_hash(request.get("preflight_hash"), "preflight_hash") != preflight["preflight_hash"]:
        raise ValueError("preflight_hash does not match submitted preflight")
    if request.get("expected_preflight_status") != PREFLIGHT_STATUS:
        raise ValueError("expected_preflight_status must match BLK-SYSTEM-063 blocked status")
    if request.get("expected_preflight_marker") != PREFLIGHT_MARKER:
        raise ValueError("expected_preflight_marker must match BLK-SYSTEM-063 marker")
    if request.get("approval_captured") is not False:
        raise ValueError("approval capture is not accepted in BLK-SYSTEM-064")
    _validate_exact_string_set(
        request.get("future_approval_obligations"),
        REQUIRED_FUTURE_APPROVAL_OBLIGATIONS,
        "future_approval_obligations must match exact proof obligation set",
    )
    _validate_exact_string_set(
        request.get("future_validation_profile_ids"),
        REQUIRED_FUTURE_VALIDATION_PROFILE_IDS,
        "future_validation_profile_ids must match exact fixture-only profile set",
    )
    _validate_exact_string_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities must match exact denied authority set")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "requested_at": _required_string(request.get("requested_at"), "requested_at"),
    }


def _validate_target(value: dict[str, Any]) -> None:
    if value.get("target_repo_identity") != TARGET_REPO_IDENTITY:
        raise ValueError("target_repo_identity must match exact Kuronode fixture target")
    if value.get("target_branch") != TARGET_BRANCH:
        raise ValueError("target_branch must be main")
    head = _required_string(value.get("target_head_sha"), "target_head_sha")
    if not _COMMIT_RE.match(head) or head != TARGET_HEAD_SHA:
        raise ValueError("target_head_sha must match exact CEB_009 fixture target head")
    target_path = _required_string(value.get("target_path"), "target_path")
    if _PROTECTED_RE.search(_decode_path_text(target_path)):
        raise ValueError("target_path rejects protected BLK-req body reference")
    if target_path != TARGET_PATH:
        raise ValueError("target_path must be scripts/smoke_test.ts")
    if value.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must match exact future patch target")
    if value.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty")


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
        decoded_path = _decode_path_text(value)
        normalized = _normalize_text(value)
        if _PROTECTED_RE.search(decoded_path):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if _LAUNDERING_RE.search(normalized):
            raise ValueError(f"{label} rejects authority-laundering text")
        if _HASH_RE.match(value):
            return


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
    compact = re.sub(r"[^a-zA-Z0-9]+", " ", spaced)
    return compact.replace("\\", "/")
