"""CEB_009 patch execution preflight refusal fixture.

This module consumes the hardened BLK-SYSTEM-061/062 CEB_009 patch approval
envelope and deterministically refuses execution because no explicit human patch
approval has been granted. It does not patch Kuronode, invoke BLK-pipe, start
Codex or BLK-test MCP, scan a live checkout, launch Electron, run smoke tests,
execute TypeScript tooling, publish BEOs, generate RTM, or read protected BLK-req
bodies.
"""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_ceb009_patch_approval_envelope import (
    APPROVAL_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as APPROVAL_EXACT_EXCLUDED_AUTHORITIES,
    INTEGRITY_HARDENING_MARKER,
    READY_STATUS as APPROVAL_READY_STATUS,
    REQUIRED_PROOF_MARKERS,
    REQUIRED_REMEDIATION_OBLIGATIONS,
    TARGET_BRANCH,
    TARGET_HEAD_SHA,
    TARGET_PATH,
    TARGET_REPO_IDENTITY,
)

PREFLIGHT_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_BLOCKED_PENDING_HUMAN_APPROVAL_NOT_EXECUTED"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_REQUEST_FIXTURE_ONLY"
PREFLIGHT_SCOPE = "CEB_009_PATCH_EXECUTION_PREFLIGHT_REFUSAL_ONLY"
BLOCK_REASON = "EXPLICIT_HUMAN_PATCH_APPROVAL_REQUIRED"
PREFLIGHT_MARKER = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_PREFLIGHT_REFUSAL_BOUNDARY"

EXACT_EXCLUDED_AUTHORITIES = set(APPROVAL_EXACT_EXCLUDED_AUTHORITIES) | {
    "PATCH_EXECUTION_APPROVED",
    "PATCH_EXECUTION_PERFORMED",
    "BLK_PIPE_INVOCATION",
    "KURONODE_PATCH_RUNNER_STARTUP",
    "CEO_009_PUBLICATION",
}

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "preflight_scope",
    "envelope_hash",
    "expected_envelope_status",
    "expected_integrity_marker",
    "explicit_human_patch_approval_present",
    "requested_at",
    "operator_note",
    "evidence_ref",
    "excluded_authorities",
}

_ENVELOPE_KEYS = {
    "envelope_status",
    "envelope_scope",
    "request_id",
    "operator_identity",
    "approval_scope",
    "approval_id",
    "run_id",
    "requested_at",
    "expires_at",
    "remediation_packet_hash",
    "target_repo_identity",
    "target_branch",
    "target_head_sha",
    "target_path",
    "allowed_modified_files",
    "allowed_new_files",
    "required_remediation_obligations",
    "remediation_packet_hash_recomputed",
    "integrity_hardening_markers",
    "replay_ledger_identity",
    "timeout_seconds",
    "max_output_bytes",
    "operator_stop_required",
    "cleanup_required",
    "proof_markers",
    "excluded_authorities",
    "approval_granted",
    "patch_applied",
    "live_kuronode_scan_performed",
    "live_kuronode_source_validation_performed",
    "electron_launched",
    "smoke_test_executed",
    "timeout_path_waited",
    "typescript_tooling_executed",
    "package_manager_invoked",
    "network_accessed",
    "source_mutation_performed",
    "git_mutation_performed",
    "codex_started",
    "blk_test_mcp_started",
    "protected_body_read",
    "beo_published",
    "rtm_generated",
    "coverage_claimed",
    "production_isolation_claimed",
    "envelope_hash",
}

_SIDE_EFFECT_FLAGS = {
    "approval_granted",
    "patch_applied",
    "live_kuronode_scan_performed",
    "live_kuronode_source_validation_performed",
    "electron_launched",
    "smoke_test_executed",
    "timeout_path_waited",
    "typescript_tooling_executed",
    "package_manager_invoked",
    "network_accessed",
    "source_mutation_performed",
    "git_mutation_performed",
    "codex_started",
    "blk_test_mcp_started",
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
    r"patch[_\s-]*(?:approved|granted|authorized|authorised|applied|execution|kuronode)|approval[_\s-]*(?:granted|inherited)|"
    r"live[_\s-]*(?:scan|validation|patch|mutation)[_\s-]*(?:allowed|authorized|authorised|approved)|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s-]*run[_\s-]*test:?smoke|test:?smoke|"
    r"electron[_\s-]*(?:launch|started|executed)|smoke[_\s-]*test[_\s-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s]*pipe|blk[-_\s]*test[_\s-]*mcp|beo[_\s-]*publication|authoritative[_\s-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|protected[_\s-]*blk[-_\s]*req[_\s-]*body|"
    r"private[_\s-]*key|api[_\s-]*key|bearer|production[_\s-]*(?:sandbox|isolation)",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)


def default_ceb009_patch_execution_preflight_request(envelope: dict[str, Any]) -> dict[str, Any]:
    """Return a valid local request for a blocked CEB_009 patch execution preflight."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-063-CEB009-PATCH-EXECUTION-PREFLIGHT-001",
        "operator_identity": "discord:684235178083745819",
        "preflight_scope": PREFLIGHT_SCOPE,
        "envelope_hash": _required_hash(envelope.get("envelope_hash"), "envelope.envelope_hash"),
        "expected_envelope_status": APPROVAL_READY_STATUS,
        "expected_integrity_marker": INTEGRITY_HARDENING_MARKER,
        "explicit_human_patch_approval_present": False,
        "requested_at": "2026-05-11T06:58:00+10:00",
        "operator_note": "local refusal fixture; blocked pending separate explicit human decision",
        "evidence_ref": "BLK-SYSTEM-063-local-preflight-refusal-fixture",
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }


def build_ceb009_patch_execution_preflight(*, envelope: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic blocked preflight record without executing the patch."""

    validated_envelope = _validate_envelope(envelope)
    validated_request = _validate_request(request, validated_envelope)
    preflight = {
        "preflight_status": PREFLIGHT_STATUS,
        "preflight_scope": PREFLIGHT_SCOPE,
        "preflight_marker": PREFLIGHT_MARKER,
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "requested_at": validated_request["requested_at"],
        "envelope_hash": validated_envelope["envelope_hash"],
        "envelope_status": APPROVAL_READY_STATUS,
        "integrity_hardening_markers": [INTEGRITY_HARDENING_MARKER],
        "remediation_packet_hash_recomputed": True,
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "required_remediation_obligations": sorted(REQUIRED_REMEDIATION_OBLIGATIONS),
        "proof_markers": sorted(REQUIRED_PROOF_MARKERS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "execution_blocked": True,
        "block_reason": BLOCK_REASON,
        "explicit_human_patch_approval_present": False,
        "approval_granted": False,
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
        "rtm_generated": False,
        "coverage_claimed": False,
        "production_isolation_claimed": False,
    }
    preflight["preflight_hash"] = _canonical_hash({key: value for key, value in preflight.items() if key != "preflight_hash"})
    return preflight


def _validate_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(envelope, dict):
        raise ValueError("approval envelope must be a dictionary")
    supplied_hash = _required_hash(envelope.get("envelope_hash"), "envelope.envelope_hash")
    recomputed_hash = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
    if supplied_hash != recomputed_hash:
        raise ValueError("approval envelope hash mismatch after recomputation")
    for key, value in envelope.items():
        if key in {
            "envelope_hash",
            "envelope_status",
            "envelope_scope",
            "approval_scope",
            "integrity_hardening_markers",
            "excluded_authorities",
            "required_remediation_obligations",
            "proof_markers",
        }:
            continue
        if key not in _ENVELOPE_KEYS:
            _reject_laundering(key, "approval envelope")
        _reject_laundering(value, "approval envelope")
    _enforce_keys(envelope, _ENVELOPE_KEYS, "approval envelope")
    if envelope.get("envelope_status") != APPROVAL_READY_STATUS:
        raise ValueError("approval envelope must be review-ready not-approved not-patched output")
    if envelope.get("approval_scope") != APPROVAL_SCOPE:
        raise ValueError("approval_scope must remain review-only")
    if envelope.get("remediation_packet_hash_recomputed") is not True:
        raise ValueError("remediation_packet_hash_recomputed must be true")
    if INTEGRITY_HARDENING_MARKER not in envelope.get("integrity_hardening_markers", []):
        raise ValueError("integrity hardening marker required")
    if envelope.get("approval_granted") is not False:
        raise ValueError("approval_granted must remain false")
    if envelope.get("target_repo_identity") != TARGET_REPO_IDENTITY:
        raise ValueError("target_repo_identity must match exact Kuronode fixture target")
    if envelope.get("target_branch") != TARGET_BRANCH:
        raise ValueError("target_branch must be main")
    head = _required_string(envelope.get("target_head_sha"), "target_head_sha")
    if not _COMMIT_RE.match(head) or head != TARGET_HEAD_SHA:
        raise ValueError("target_head_sha must match exact CEB_009 fixture target head")
    target_path = _required_string(envelope.get("target_path"), "target_path")
    if _PROTECTED_RE.search(_decode_path_text(target_path)):
        raise ValueError("target_path rejects protected BLK-req body reference")
    if target_path != TARGET_PATH:
        raise ValueError("target_path must be scripts/smoke_test.ts")
    if envelope.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must match exact future patch target")
    if envelope.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty")
    _validate_exact_string_set(
        envelope.get("required_remediation_obligations"),
        REQUIRED_REMEDIATION_OBLIGATIONS,
        "required_remediation_obligations must match exact remediation obligation set",
    )
    _validate_exact_string_set(envelope.get("proof_markers"), REQUIRED_PROOF_MARKERS, "proof_markers must match exact proof marker set")
    _validate_exact_string_set(
        envelope.get("excluded_authorities"),
        APPROVAL_EXACT_EXCLUDED_AUTHORITIES,
        "envelope excluded_authorities must match exact denied authority set",
    )
    for flag in sorted(_SIDE_EFFECT_FLAGS):
        if envelope.get(flag) is not False:
            raise ValueError(f"approval envelope contains side effect: {flag}")
    validated = deepcopy(envelope)
    validated["envelope_hash"] = recomputed_hash
    return validated


def _validate_request(request: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("preflight request must be a dictionary")
    for key, value in request.items():
        if key not in _REQUEST_KEYS:
            _reject_laundering(key, "preflight request")
        if key not in {"request_status", "request_id", "preflight_scope", "expected_envelope_status", "expected_integrity_marker", "excluded_authorities"}:
            _reject_laundering(value, "preflight request")
    _enforce_keys(request, _REQUEST_KEYS, "preflight request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be CEB_009 patch execution preflight fixture only")
    if _required_string(request.get("preflight_scope"), "preflight_scope") != PREFLIGHT_SCOPE:
        raise ValueError("preflight_scope must be refusal only")
    if _required_hash(request.get("envelope_hash"), "envelope_hash") != envelope["envelope_hash"]:
        raise ValueError("envelope_hash does not match submitted approval envelope")
    if request.get("expected_envelope_status") != APPROVAL_READY_STATUS:
        raise ValueError("expected_envelope_status must match review-ready envelope status")
    if request.get("expected_integrity_marker") != INTEGRITY_HARDENING_MARKER:
        raise ValueError("expected_integrity_marker must match BLK-SYSTEM-062 hardening marker")
    if request.get("explicit_human_patch_approval_present") is not False:
        raise ValueError("explicit human patch approval is not accepted in BLK-SYSTEM-063")
    _validate_exact_string_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities must match exact denied authority set")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "requested_at": _required_string(request.get("requested_at"), "requested_at"),
    }


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
