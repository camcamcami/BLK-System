"""Review-only Kuronode lifecycle cleanup patch approval envelope.

BLK-SYSTEM-075 converts the BLK-SYSTEM-074 remediation packet into a deterministic
human-review envelope for a future exact-target Kuronode patch. It does not grant
approval, invoke BLK-pipe/Codex, mutate Kuronode source or Git state, rerun
BLK-test, publish BEOs, generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import re
from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from blk_test_kuronode_lifecycle_cleanup_remediation_packet import (
    COMMITTED_GIT_METADATA_HASH as REMEDIATION_COMMITTED_GIT_METADATA_HASH,
    COMMITTED_SOURCE_EVIDENCE_FILE_SHA256 as REMEDIATION_COMMITTED_SOURCE_EVIDENCE_FILE_SHA256,
    COMMITTED_SOURCE_EVIDENCE_HASH as REMEDIATION_COMMITTED_SOURCE_EVIDENCE_HASH,
    COMMITTED_SOURCE_TREE_HASH as REMEDIATION_COMMITTED_SOURCE_TREE_HASH,
    EXACT_EXCLUDED_AUTHORITIES as REMEDIATION_EXACT_EXCLUDED_AUTHORITIES,
    PACKET_FALSE_SIDE_EFFECT_FLAGS as REMEDIATION_PACKET_FALSE_SIDE_EFFECT_FLAGS,
    READY_STATUS as REMEDIATION_READY_STATUS,
    RETIRED_APPROVAL_ID as RETIRED_BLK_SYSTEM_073_APPROVAL_ID,
    RETIRED_RUN_ID as RETIRED_BLK_SYSTEM_073_RUN_ID,
    SOURCE_PILOT_STATUS as REMEDIATION_SOURCE_PILOT_STATUS,
    SOURCE_SPRINT as REMEDIATION_SOURCE_SPRINT,
    TARGET_FINDING_LINE as REMEDIATION_TARGET_FINDING_LINE,
    TARGET_FINDING_PATH as REMEDIATION_TARGET_FINDING_PATH,
    TARGET_FINDING_RULE as REMEDIATION_TARGET_FINDING_RULE,
    _remediation_guidance,
    _remediation_obligations,
)

PATCH_APPROVAL_READY_STATUS = "KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED"
REQUEST_STATUS = "KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_FIXTURE_ONLY"
TARGET_REPO_PATH = "/home/dad/code/Kuronode-v1"
TARGET_BRANCH = "main"
TARGET_HEAD_SHA = "38e332b188e45edcb484765694112c9041ad1a3b"
ALLOWED_MODIFIED_FILES = ["scripts/smoke_test.ts"]
ALLOWED_NEW_FILES: list[str] = []
FUTURE_PATCH_APPROVAL_ID = "APPROVAL-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001"
FUTURE_PATCH_RUN_ID = "RUN-BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-001"
EXPECTED_UPSTREAM_REQUEST_ID = "BLK-SYSTEM-074-LIFECYCLE-CLEANUP-REMEDIATION-PACKET-001"
EXPECTED_OPERATOR_IDENTITY = "discord:684235178083745819"
EXPECTED_REQUEST_ID = "BLK-SYSTEM-075-KURONODE-LIFECYCLE-CLEANUP-PATCH-ENVELOPE-001"

EXACT_EXCLUDED_AUTHORITIES = {
    "PATCH_APPROVAL_GRANTED",
    "PATCH_EXECUTION",
    "BLK_PIPE_EXECUTION",
    "CODEX_EXECUTION",
    "LIVE_TACTICAL_LLM_DISPATCH",
    "KURONODE_SOURCE_MUTATION",
    "KURONODE_GIT_MUTATION",
    "KURONODE_STAGING_COMMIT_PUSH_RESET_CHECKOUT_REVERT_STASH_CLEANUP_AUTOFIX_OR_REMOTE_WRITE",
    "BLK_SYSTEM_073_RUNTIME_ID_REUSE",
    "BLK_TEST_PILOT_RERUN",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "DYNAMIC_TOOL_EXPANSION",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "PROTECTED_BLK_REQ_BODY_READ",
    "PROTECTED_BLK_REQ_BODY_COPY_PARSE_HASH_SUMMARIZE_SCAN_MUTATE_OR_DRIFT_COMPARE",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RELEASE_AUTHORITY",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_CLAIM",
    "DRIFT_DECISION",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

PATCH_FALSE_SIDE_EFFECT_FLAGS = {
    "approval_granted",
    "patch_executed",
    "runtime_validation_executed",
    "blk_pipe_invoked",
    "codex_started",
    "live_tactical_llm_dispatched",
    "kuronode_source_mutation_performed",
    "kuronode_git_mutation_performed",
    "kuronode_staging_performed",
    "kuronode_commit_performed",
    "kuronode_push_performed",
    "kuronode_reset_performed",
    "kuronode_checkout_performed",
    "kuronode_revert_performed",
    "kuronode_stash_performed",
    "kuronode_cleanup_performed",
    "kuronode_autofix_performed",
    "kuronode_remote_write_performed",
    "retired_blk_system_073_id_reused",
    "blk_test_pilot_rerun_performed",
    "production_blk_test_mcp_started",
    "generic_blk_test_mcp_started",
    "reusable_blk_test_service_started",
    "arbitrary_shell_or_caller_command_executed",
    "dynamic_tool_expansion_performed",
    "electron_launched",
    "smoke_test_executed",
    "typescript_tooling_executed",
    "package_manager_invoked",
    "network_accessed",
    "model_service_called",
    "browser_or_cyber_tooling_called",
    "protected_body_read",
    "protected_body_copied_parsed_hashed_summarized_scanned_mutated_or_drift_compared",
    "beo_published",
    "runtime_published_beo_output_emitted",
    "live_publication_approval_captured",
    "signer_key_material_accessed",
    "cryptographic_signature_generated",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_revocation_supersession_executed",
    "release_authority_exercised",
    "rtm_generated",
    "rtm_drift_rejection_performed",
    "active_vault_hash_comparison_performed",
    "coverage_matrix_generated",
    "coverage_claim_promoted",
    "drift_decision_performed",
    "production_sandbox_or_host_secret_isolation_claimed",
}

_REMEDIATION_PACKET_KEYS = {
    "packet_status",
    "packet_scope",
    "request_id",
    "operator_identity",
    "source_sprint",
    "source_pilot_status",
    "source_evidence_hash",
    "source_evidence_file_sha256",
    "target_repo_path",
    "target_repo_head",
    "target_patch_path",
    "finding",
    "retired_runtime_ids",
    "future_runtime_id_policy",
    "remediation_obligations",
    "remediation_guidance",
    "required_future_patch_boundary",
    "excluded_authorities",
    "packet_hash",
} | REMEDIATION_PACKET_FALSE_SIDE_EFFECT_FLAGS

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "requested_at",
    "expires_at",
    "remediation_packet_hash",
    "target_repo_path",
    "target_branch",
    "target_head_sha",
    "allowed_modified_files",
    "allowed_new_files",
    "patch_mechanism",
    "validation_profiles",
    "future_patch_approval_id",
    "future_patch_run_id",
    "approval_granted",
    "excluded_authorities",
    "operator_note",
}

_LAUNDERING_RE = re.compile(
    r"approved[_\s./-]*for[_\s./-]*live[_\s./-]*execution|approval[_\s./-]*(?:granted|captured|inherited)|"
    r"patch[_\s./-]*(?:approved|executed|authority[_\s./-]*granted)|(?:patch|edit|mutate)[_\s./-]*kuronode|"
    r"source[_\s./-]*(?:mutation|writes?[_\s./-]*enabled)|git[_\s./-]*(?:mutation|staging[_\s./-]*enabled)|"
    r"blk[-_\s./]*pipe[_\s./-]*(?:run|invoke|invoked|execute)|codex|live[_\s./-]*tactical|"
    r"pilot[_\s./-]*rerun[_\s./-]*(?:approved|permitted|allowed|authorized|authorised)|"
    r"run[_\s./-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s./-]*run[_\s./-]*test:?smoke|test:?smoke|"
    r"electron[_\s./-]*(?:launch|started|executed)|smoke[_\s./-]*test[_\s./-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"blk[-_\s./]*test[_\s./-]*mcp|production[_\s./-]*blk[-_\s./]*test|dynamic[_\s./-]*tool[_\s./-]*expansion|"
    r"reusable[_\s./-]*blk[-_\s./]*test[_\s./-]*service|APPROVED_FOR_LIVE_EXECUTION|"
    r"beo[_\s./-]*(?:is[_\s./-]*)?published|published[_\s./-]*beo|beo[_\s./-]*publication|authoritative[_\s./-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s./-]*(?:rejection|decision)|coverage[_\s./-]*(?:matrix|claim|truth)|"
    r"active[_\s./-]*vault[_\s./-]*hash[_\s./-]*comparison|protected[_\s./-]*blk[-_\s./]*req[_\s./-]*body|"
    r"read[_\s./-]*\.env[_\s./-]*secrets|private[_\s./-]*key|api[_\s./-]*key|bearer|production[_\s./-]*(?:sandbox|isolation)",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(
    r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s./-]*blk[-_\s./]*req[_\s./-]*body",
    re.IGNORECASE,
)
_COMPACT_LAUNDERING_TOKENS = {
    "rtmgeneration",
    "rtmid",
    "rtmgenerated",
    "activevaulthashcomparison",
    "signaturegenerated",
    "cryptographicsigning",
    "privatekey",
    "keymaterial",
    "signerkeymaterial",
    "apikey",
    "authoritativebeopublication",
    "beopubapproved",
    "abpapproved",
    "rtpbeo",
    "publishbeo",
    "approvalinherited",
    "codexapproval",
    "blkpipesuccess",
    "blktestpassapproval",
}


def default_lifecycle_cleanup_patch_approval_request(remediation_packet: dict[str, Any]) -> dict[str, Any]:
    """Return a valid review-only patch approval envelope request."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": EXPECTED_REQUEST_ID,
        "operator_identity": EXPECTED_OPERATOR_IDENTITY,
        "requested_at": "2026-05-11T14:30:00+10:00",
        "expires_at": "2026-05-18T14:30:00+10:00",
        "remediation_packet_hash": _required_hash(remediation_packet.get("packet_hash"), "remediation_packet.packet_hash"),
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "allowed_modified_files": list(ALLOWED_MODIFIED_FILES),
        "allowed_new_files": list(ALLOWED_NEW_FILES),
        "patch_mechanism": "BLK_PIPE_EXACT_TARGET_PATCH_PROPOSED_NOT_EXECUTED",
        "validation_profiles": ["kuronode-lifecycle-cleanup-focused-fixture"],
        "future_patch_approval_id": FUTURE_PATCH_APPROVAL_ID,
        "future_patch_run_id": FUTURE_PATCH_RUN_ID,
        "approval_granted": False,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "review-only exact-target envelope; remains not approved and not executed",
    }


def build_lifecycle_cleanup_patch_approval_envelope(
    *, remediation_packet: dict[str, Any], request: dict[str, Any], now: str | None = None
) -> dict[str, Any]:
    """Build a review-only exact-target approval envelope without applying a patch."""

    packet = _validate_remediation_packet(remediation_packet)
    validated = _validate_request(request, packet, now=now)
    envelope = {
        "envelope_status": PATCH_APPROVAL_READY_STATUS,
        "approval_state": "READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED",
        "request_id": validated["request_id"],
        "operator_identity": validated["operator_identity"],
        "requested_at": validated["requested_at"],
        "expires_at": validated["expires_at"],
        "remediation_packet_hash": validated["remediation_packet_hash"],
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "allowed_modified_files": list(ALLOWED_MODIFIED_FILES),
        "allowed_new_files": [],
        "patch_mechanism": "BLK_PIPE_EXACT_TARGET_PATCH_PROPOSED_NOT_EXECUTED",
        "validation_profiles": ["kuronode-lifecycle-cleanup-focused-fixture"],
        "future_patch_approval_id": FUTURE_PATCH_APPROVAL_ID,
        "future_patch_approval_id_status": "FUTURE_CANDIDATE_NOT_CONSUMED",
        "future_patch_run_id": FUTURE_PATCH_RUN_ID,
        "future_patch_run_id_status": "FUTURE_CANDIDATE_NOT_CONSUMED",
        "patch_obligations": _patch_obligations(),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in sorted(PATCH_FALSE_SIDE_EFFECT_FLAGS):
        envelope[flag] = False
    envelope["envelope_hash"] = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
    return envelope


def _validate_remediation_packet(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise ValueError("remediation_packet must be a dictionary")
    _enforce_keys(packet, _REMEDIATION_PACKET_KEYS, "remediation packet schema")
    supplied_hash = _required_hash(packet.get("packet_hash"), "remediation_packet.packet_hash")
    recomputed_hash = _canonical_hash({key: value for key, value in packet.items() if key != "packet_hash"})
    if supplied_hash != recomputed_hash:
        raise ValueError("remediation_packet_hash does not match recomputed packet")
    if packet.get("packet_status") != REMEDIATION_READY_STATUS:
        raise ValueError("remediation packet status must be KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED")
    expected_scalars = {
        "packet_scope": "KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_FIXTURE_ONLY_NOT_PATCHED",
        "request_id": EXPECTED_UPSTREAM_REQUEST_ID,
        "operator_identity": EXPECTED_OPERATOR_IDENTITY,
        "source_sprint": REMEDIATION_SOURCE_SPRINT,
        "source_pilot_status": REMEDIATION_SOURCE_PILOT_STATUS,
        "source_evidence_hash": REMEDIATION_COMMITTED_SOURCE_EVIDENCE_HASH,
        "source_evidence_file_sha256": REMEDIATION_COMMITTED_SOURCE_EVIDENCE_FILE_SHA256,
        "target_repo_path": TARGET_REPO_PATH,
        "target_repo_head": TARGET_HEAD_SHA,
        "target_patch_path": ALLOWED_MODIFIED_FILES[0],
    }
    for key, expected in expected_scalars.items():
        if packet.get(key) != expected:
            raise ValueError(f"remediation packet {key} mismatch")
    if packet.get("finding") != {
        "path": REMEDIATION_TARGET_FINDING_PATH,
        "line": REMEDIATION_TARGET_FINDING_LINE,
        "rule": REMEDIATION_TARGET_FINDING_RULE,
    }:
        raise ValueError("remediation packet finding mismatch")
    if packet.get("retired_runtime_ids") != {
        "approval_id": RETIRED_BLK_SYSTEM_073_APPROVAL_ID,
        "run_id": RETIRED_BLK_SYSTEM_073_RUN_ID,
    }:
        raise ValueError("remediation packet retired runtime ids mismatch")
    if packet.get("future_runtime_id_policy") != "FRESH_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED":
        raise ValueError("remediation packet future runtime policy mismatch")
    if packet.get("remediation_obligations") != _remediation_obligations():
        raise ValueError("remediation packet remediation obligations mismatch")
    if packet.get("remediation_guidance") != _remediation_guidance():
        raise ValueError("remediation packet remediation guidance mismatch")
    if packet.get("required_future_patch_boundary") != [
        "separate explicit Kuronode patch authority",
        "exact target SHA and remote-head recheck",
        "exact allowlist for scripts/smoke_test.ts or successor file",
        "Kuronode closeout review before completion",
        "fresh runtime IDs for any later BLK-test recheck",
    ]:
        raise ValueError("remediation packet required future patch boundary mismatch")
    if (
        not isinstance(packet.get("excluded_authorities"), list)
        or not all(isinstance(item, str) for item in packet["excluded_authorities"])
        or set(packet["excluded_authorities"]) != REMEDIATION_EXACT_EXCLUDED_AUTHORITIES
        or len(packet["excluded_authorities"]) != len(REMEDIATION_EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("remediation packet excluded authorities mismatch")
    for flag in sorted(REMEDIATION_PACKET_FALSE_SIDE_EFFECT_FLAGS):
        if packet.get(flag) is not False:
            raise ValueError(f"remediation packet contains prohibited side effect: {flag}")
    return deepcopy(packet)


def _validate_request(request: dict[str, Any], packet: dict[str, Any], now: str | None) -> dict[str, str]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_LIFECYCLE_CLEANUP_PATCH_APPROVAL_ENVELOPE_FIXTURE_ONLY")
    if _required_string(request.get("request_id"), "request_id") != EXPECTED_REQUEST_ID:
        raise ValueError("request_id mismatch")
    if _required_string(request.get("operator_identity"), "operator_identity") != EXPECTED_OPERATOR_IDENTITY:
        raise ValueError("operator_identity mismatch")
    supplied_hash = _required_hash(request.get("remediation_packet_hash"), "remediation_packet_hash")
    recomputed_hash = _canonical_hash({key: value for key, value in packet.items() if key != "packet_hash"})
    if supplied_hash != packet["packet_hash"] or supplied_hash != recomputed_hash:
        raise ValueError("remediation_packet_hash does not match recomputed packet")
    if request.get("target_repo_path") != TARGET_REPO_PATH:
        raise ValueError("target_repo_path mismatch")
    if request.get("target_branch") != TARGET_BRANCH:
        raise ValueError("target_branch mismatch")
    if request.get("target_head_sha") != TARGET_HEAD_SHA:
        raise ValueError("target_head_sha mismatch")
    if request.get("allowed_modified_files") != ALLOWED_MODIFIED_FILES:
        raise ValueError("allowed_modified_files mismatch")
    if request.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty")
    if request.get("patch_mechanism") != "BLK_PIPE_EXACT_TARGET_PATCH_PROPOSED_NOT_EXECUTED":
        raise ValueError("patch_mechanism must remain proposed-not-executed")
    if request.get("validation_profiles") != ["kuronode-lifecycle-cleanup-focused-fixture"]:
        raise ValueError("validation_profiles mismatch")
    if request.get("approval_granted") is not False:
        raise ValueError("approval_granted must be False")
    for key in ("future_patch_approval_id", "future_patch_run_id"):
        value = _required_string(request.get(key), key)
        if value in {RETIRED_BLK_SYSTEM_073_APPROVAL_ID, RETIRED_BLK_SYSTEM_073_RUN_ID}:
            raise ValueError("request attempts to reuse retired BLK-SYSTEM-073 runtime ID")
    if request.get("future_patch_approval_id") != FUTURE_PATCH_APPROVAL_ID or request.get("future_patch_run_id") != FUTURE_PATCH_RUN_ID:
        raise ValueError("future patch IDs must match review-only candidates")
    _validate_timestamps(request.get("requested_at"), request.get("expires_at"), now=now)
    for key, value in request.items():
        if key == "excluded_authorities":
            continue
        _reject_laundering(value, f"request.{key}")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "requested_at": _required_string(request.get("requested_at"), "requested_at"),
        "expires_at": _required_string(request.get("expires_at"), "expires_at"),
        "remediation_packet_hash": supplied_hash,
    }


def _validate_timestamps(requested_at: Any, expires_at: Any, now: str | None) -> None:
    requested = _parse_iso(_required_string(requested_at, "requested_at"), "requested_at")
    expires = _parse_iso(_required_string(expires_at, "expires_at"), "expires_at")
    now_dt = _parse_iso(now, "now") if now is not None else requested
    if expires <= requested or expires <= now_dt:
        raise ValueError("expires_at must be after requested_at and now")


def _parse_iso(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return parsed


def _patch_obligations() -> list[dict[str, str]]:
    return [
        {
            "obligation_id": "PATCH_ADD_DETERMINISTIC_LIFECYCLE_TEARDOWN",
            "requirement": "Future patch must route line 53 lifecycle setup through deterministic idempotent teardown.",
        },
        {
            "obligation_id": "PATCH_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER",
            "requirement": "Future patch/regression must prove no escaped process, IPC listener, or subscription remains.",
        },
        {
            "obligation_id": "PATCH_PRESERVE_TIMEOUT_AS_FAILURE",
            "requirement": "Timeout or missing projection-result paths must fail before any success evidence.",
        },
        {
            "obligation_id": "PATCH_ADD_FOCUSED_CLEANUP_REGRESSION",
            "requirement": "Future patch must include focused cleanup regression coverage.",
        },
        {
            "obligation_id": "PATCH_RUN_KURONODE_CLOSEOUT_REVIEW_BEFORE_COMPLETION",
            "requirement": "Future patch sprint must satisfy Kuronode repository closeout-review obligations before completion.",
        },
        {
            "obligation_id": "PATCH_REQUIRE_FRESH_BLK_TEST_RECHECK_IDS_AFTER_PATCH",
            "requirement": "Any later BLK-test recheck requires fresh IDs under a separate authority envelope.",
        },
    ]


def _validate_excluded_authorities(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")


def _enforce_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    extras = sorted(set(value) - expected)
    missing = sorted(expected - set(value))
    if extras or missing:
        raise ValueError(f"{label} keys mismatch: extras={extras} missing={missing}")


def _reject_laundering(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_laundering(str(key), f"{label}.{key}")
            _reject_laundering(item, f"{label}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_laundering(item, f"{label}[{index}]")
        return
    if isinstance(value, str):
        decoded = _decode_text(value)
        compact = re.sub(r"[^a-z0-9]", "", decoded.lower())
        if RETIRED_BLK_SYSTEM_073_APPROVAL_ID in decoded or RETIRED_BLK_SYSTEM_073_RUN_ID in decoded:
            raise ValueError(f"{label} contains authority-laundering text")
        if _PROTECTED_RE.search(decoded):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if compact in _COMPACT_LAUNDERING_TOKENS or any(token in compact for token in _COMPACT_LAUNDERING_TOKENS):
            raise ValueError(f"{label} contains authority-laundering text")
        if _LAUNDERING_RE.search(decoded):
            raise ValueError(f"{label} contains authority-laundering text")


def _decode_text(text: str) -> str:
    decoded = text
    for _ in range(3):
        next_value = unquote(decoded)
        if next_value == decoded:
            return decoded
        decoded = next_value
    return decoded
