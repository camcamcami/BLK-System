"""Non-runtime CEB_009 patch approval-envelope fixture.

This module converts the BLK-SYSTEM-060 CEB_009 remediation packet into a
deterministic review-only approval envelope for a future exact-target patch. It
does not grant approval, patch Kuronode, scan a live checkout, mutate Git, launch
Electron, run the smoke test, execute TypeScript tooling, invoke package
managers, start Codex or BLK-test MCP, publish BEOs, generate RTM, or read
protected BLK-req bodies.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_ceb009_remediation_packet import READY_STATUS as REMEDIATION_READY_STATUS

READY_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_FIXTURE_ONLY"
APPROVAL_SCOPE = "KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_REVIEW_ONLY"
TARGET_REPO_IDENTITY = "github:camcamcami/Kuronode-v1"
TARGET_BRANCH = "main"
TARGET_HEAD_SHA = "cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2"
TARGET_PATH = "scripts/smoke_test.ts"
REPLAY_LEDGER_IDENTITY = "BLK-SYSTEM-061-CEB009-PATCH-APPROVAL-REPLAY-LEDGER-FIXTURE"

REQUIRED_REMEDIATION_OBLIGATIONS = {
    "CEB009_REMEDIATION_TIMEOUT_MUST_FAIL",
    "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_STREAM_ID",
    "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_AST",
    "CEB009_REMEDIATION_REMOVE_ANY_AND_TS_IGNORE",
    "CEB009_REMEDIATION_PRESERVE_CLEANUP_UNSUB_AND_CLOSE",
    "CEB009_REMEDIATION_NOT_RUNTIME_VALIDATION",
}
REQUIRED_PROOF_MARKERS = {
    "EXACT_TARGET_REPO_BOUND",
    "EXACT_TARGET_HEAD_BOUND",
    "EXACT_ALLOWED_FILE_SET_BOUND",
    "REMEDIATION_PACKET_HASH_BOUND",
    "REPLAY_PROTECTION_REQUIRED",
    "EXPIRY_REQUIRED",
    "OUTPUT_BOUND_REQUIRED",
    "OPERATOR_STOP_REQUIRED",
    "CLEANUP_REQUIRED",
    "NO_PATCH_APPLIED_THIS_SPRINT",
    "NO_RUNTIME_VALIDATION_THIS_SPRINT",
}
EXACT_EXCLUDED_AUTHORITIES = {
    "PATCH_APPROVAL_GRANTED",
    "KURONODE_SOURCE_MUTATION",
    "KURONODE_GIT_MUTATION",
    "LIVE_KURONODE_REPOSITORY_SCAN",
    "LIVE_KURONODE_SOURCE_VALIDATION",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "WALL_CLOCK_TIMEOUT_WAIT",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "SOURCE_OR_GIT_MUTATION_BY_GATE",
    "LIVE_CODEX_EXECUTION",
    "LIVE_TACTICAL_LLM_DISPATCH",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PROTECTED_BLK_REQ_BODY_READ",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_CLAIM",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

_REQUEST_KEYS = {
    "request_status",
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
    "replay_ledger_identity",
    "timeout_seconds",
    "max_output_bytes",
    "operator_stop_required",
    "cleanup_required",
    "proof_markers",
    "excluded_authorities",
    "operator_note",
}
_SIDE_EFFECT_FLAGS = {
    "patch_applied",
    "live_kuronode_scan_performed",
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
    r"approved[_\s-]*for[_\s-]*live[_\s-]*execution|runtime[_\s-]*pilot[_\s-]*approved|"
    r"patch[_\s-]*(?:approved|granted|authorized|authorised|applied)|approval[_\s-]*granted|"
    r"live[_\s-]*(?:scan|validation|patch|mutation)[_\s-]*(?:allowed|authorized|authorised|approved)|"
    r"patch[_\s-]*kuronode|edit[_\s-]*kuronode|mutate[_\s-]*kuronode|source[_\s-]*mutation|git[_\s-]*mutation|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s-]*run[_\s-]*test:?smoke|test:?smoke|"
    r"electron[_\s-]*(?:launch|started|executed)|smoke[_\s-]*test[_\s-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s]*test[_\s-]*mcp|beo[_\s-]*publication|authoritative[_\s-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|protected[_\s-]*blk[-_\s]*req[_\s-]*body|"
    r"private[_\s-]*key|api[_\s-]*key|bearer|production[_\s-]*(?:sandbox|isolation)",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)


def default_ceb009_patch_approval_request(remediation_packet: dict[str, Any]) -> dict[str, Any]:
    """Return a valid review-only patch approval-envelope request."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-061-CEB009-PATCH-APPROVAL-ENVELOPE-001",
        "operator_identity": "discord:684235178083745819",
        "approval_scope": APPROVAL_SCOPE,
        "approval_id": "BLK-SYSTEM-061-CEB009-PATCH-APPROVAL-001",
        "run_id": "BLK-SYSTEM-061-CEB009-PATCH-RUN-001",
        "requested_at": "2026-05-10T21:08:00+10:00",
        "expires_at": "2026-05-17T21:08:00+10:00",
        "remediation_packet_hash": _required_hash(remediation_packet.get("packet_hash"), "remediation_packet.packet_hash"),
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "required_remediation_obligations": sorted(REQUIRED_REMEDIATION_OBLIGATIONS),
        "replay_ledger_identity": REPLAY_LEDGER_IDENTITY,
        "timeout_seconds": 600,
        "max_output_bytes": 200000,
        "operator_stop_required": True,
        "cleanup_required": True,
        "proof_markers": sorted(REQUIRED_PROOF_MARKERS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "review-ready exact-target envelope only; no source change in this sprint",
    }


def build_ceb009_patch_approval_envelope(
    *,
    remediation_packet: dict[str, Any],
    request: dict[str, Any],
    now: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic review envelope without granting approval or patching."""

    validated_packet = _validate_remediation_packet(remediation_packet)
    validated_request = _validate_request(request, validated_packet, now=now)
    envelope = {
        "envelope_status": READY_STATUS,
        "envelope_scope": "CEB_009_PATCH_APPROVAL_ENVELOPE_FIXTURE_ONLY_NOT_APPROVED_NOT_PATCHED",
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "approval_scope": APPROVAL_SCOPE,
        "approval_id": validated_request["approval_id"],
        "run_id": validated_request["run_id"],
        "requested_at": validated_request["requested_at"],
        "expires_at": validated_request["expires_at"],
        "remediation_packet_hash": validated_request["remediation_packet_hash"],
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "required_remediation_obligations": sorted(REQUIRED_REMEDIATION_OBLIGATIONS),
        "replay_ledger_identity": REPLAY_LEDGER_IDENTITY,
        "timeout_seconds": validated_request["timeout_seconds"],
        "max_output_bytes": validated_request["max_output_bytes"],
        "operator_stop_required": True,
        "cleanup_required": True,
        "proof_markers": sorted(REQUIRED_PROOF_MARKERS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "approval_granted": False,
        "patch_applied": False,
        "live_kuronode_scan_performed": False,
        "live_kuronode_source_validation_performed": False,
        "electron_launched": False,
        "smoke_test_executed": False,
        "timeout_path_waited": False,
        "typescript_tooling_executed": False,
        "package_manager_invoked": False,
        "network_accessed": False,
        "source_mutation_performed": False,
        "git_mutation_performed": False,
        "codex_started": False,
        "blk_test_mcp_started": False,
        "protected_body_read": False,
        "beo_published": False,
        "rtm_generated": False,
        "coverage_claimed": False,
        "production_isolation_claimed": False,
    }
    envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
    return envelope


def _validate_remediation_packet(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise ValueError("remediation_packet must be a dictionary")
    if packet.get("packet_status") != REMEDIATION_READY_STATUS:
        raise ValueError("remediation packet must be BLK-SYSTEM-060 ready-not-patched output")
    _required_hash(packet.get("packet_hash"), "remediation_packet.packet_hash")
    if packet.get("target_path") != TARGET_PATH:
        raise ValueError("remediation packet must bind to scripts/smoke_test.ts")
    for flag in sorted(_SIDE_EFFECT_FLAGS):
        if packet.get(flag) is not False:
            raise ValueError(f"remediation packet contains side effect: {flag}")
    obligations = set()
    for item in packet.get("remediation_obligations", []):
        if isinstance(item, dict) and isinstance(item.get("obligation_id"), str):
            obligations.add(item["obligation_id"])
    missing = sorted(REQUIRED_REMEDIATION_OBLIGATIONS - obligations)
    if missing:
        raise ValueError(f"remediation packet missing required obligation(s): {missing}")
    return deepcopy(packet)


def _validate_request(request: dict[str, Any], packet: dict[str, Any], *, now: str | None) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "request")
    _reject_laundering(
        {
            key: value
            for key, value in request.items()
            if key
            not in {
                "excluded_authorities",
                "request_status",
                "approval_scope",
                "required_remediation_obligations",
                "proof_markers",
            }
        },
        "request",
    )
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_FIXTURE_ONLY")
    if _required_string(request.get("approval_scope"), "approval_scope") != APPROVAL_SCOPE:
        raise ValueError("approval_scope must be KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_REVIEW_ONLY")
    remediation_packet_hash = _required_hash(request.get("remediation_packet_hash"), "remediation_packet_hash")
    if remediation_packet_hash != packet["packet_hash"]:
        raise ValueError("remediation_packet_hash does not match submitted packet")
    _require_exact_string(request.get("target_repo_identity"), TARGET_REPO_IDENTITY, "target_repo_identity")
    _require_exact_string(request.get("target_branch"), TARGET_BRANCH, "target_branch")
    head = _required_string(request.get("target_head_sha"), "target_head_sha")
    if not _COMMIT_RE.match(head) or head != TARGET_HEAD_SHA:
        raise ValueError("target_head_sha must match exact CEB_009 fixture target head")
    target_path = _required_string(request.get("target_path"), "target_path")
    if _PROTECTED_RE.search(_decode_path_text(target_path)):
        raise ValueError("target_path rejects protected BLK-req body reference")
    if target_path != TARGET_PATH:
        raise ValueError("target_path must be scripts/smoke_test.ts")
    if request.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must match exact future patch target")
    if request.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty for CEB_009 patch envelope")
    _validate_exact_string_set(
        request.get("required_remediation_obligations"),
        REQUIRED_REMEDIATION_OBLIGATIONS,
        "required_remediation_obligations",
        "required_remediation_obligations must match exact remediation obligation set",
    )
    _validate_exact_string_set(request.get("proof_markers"), REQUIRED_PROOF_MARKERS, "proof_markers", "proof_markers must match exact proof marker set")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    _require_exact_string(request.get("replay_ledger_identity"), REPLAY_LEDGER_IDENTITY, "replay_ledger_identity")
    timeout_seconds = _required_int(request.get("timeout_seconds"), "timeout_seconds")
    if timeout_seconds != 600:
        raise ValueError("timeout_seconds must be 600 for the future patch envelope")
    max_output_bytes = _required_int(request.get("max_output_bytes"), "max_output_bytes")
    if max_output_bytes != 200000:
        raise ValueError("max_output_bytes must be 200000 for the future patch envelope")
    if request.get("operator_stop_required") is not True:
        raise ValueError("operator_stop_required must be true")
    if request.get("cleanup_required") is not True:
        raise ValueError("cleanup_required must be true")
    requested = _parse_time(_required_string(request.get("requested_at"), "requested_at"), "requested_at")
    expires = _parse_time(_required_string(request.get("expires_at"), "expires_at"), "expires_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")
    if now is not None and expires <= _parse_time(now, "now"):
        raise ValueError("approval envelope is expired")
    approval_id = _required_string(request.get("approval_id"), "approval_id")
    run_id = _required_string(request.get("run_id"), "run_id")
    if not approval_id.startswith("BLK-SYSTEM-061-CEB009-PATCH-APPROVAL-"):
        raise ValueError("approval_id must bind to BLK-SYSTEM-061")
    if not run_id.startswith("BLK-SYSTEM-061-CEB009-PATCH-RUN-"):
        raise ValueError("run_id must bind to BLK-SYSTEM-061")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "approval_id": approval_id,
        "run_id": run_id,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "remediation_packet_hash": remediation_packet_hash,
        "timeout_seconds": timeout_seconds,
        "max_output_bytes": max_output_bytes,
    }


def _validate_excluded_authorities(excluded: Any) -> None:
    _validate_exact_string_set(excluded, EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities", "excluded_authorities must match exact denied authority set")


def _validate_exact_string_set(value: Any, expected: set[str], label: str, message: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value) or set(value) != expected or len(value) != len(expected):
        raise ValueError(message)


def _required_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    return value


def _require_exact_string(value: Any, expected: str, label: str) -> None:
    if _required_string(value, label) != expected:
        raise ValueError(f"{label} must be {expected}")


def _parse_time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")
    return parsed


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
