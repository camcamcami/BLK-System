"""Non-runtime Kuronode Power-of-Ten gate pilot approval envelope.

This module builds deterministic approval-envelope readiness for a future bounded
Kuronode Power-of-Ten gate pilot. It does not scan Kuronode, execute TypeScript
tooling, invoke package managers, mutate source/Git, start Codex or BLK-test MCP,
publish BEOs, generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

READY_STATUS = "KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
APPROVAL_SCOPE = "KURONODE_POWER_OF_TEN_GATE_PILOT_APPROVAL_ENVELOPE_ONLY"
PROFILE_NAME = "kuronode-power-of-ten-static-fixture"
PROFILE_COMMAND = "PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_kuronode_power_of_ten_static_profile -q"

EXACT_EXCLUDED_AUTHORITIES = {
    "LIVE_KURONODE_REPOSITORY_SCAN",
    "LIVE_KURONODE_SOURCE_VALIDATION",
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

_TARGET_KEYS = {
    "target_repo_identity",
    "target_branch",
    "target_head_sha",
    "target_workspace_identity",
    "target_scope",
    "operator_note",
}
_EVIDENCE_KEYS = {
    "static_profile_boundary_marker",
    "validation_profile_boundary_marker",
    "static_profile_status",
    "fixture_profile_marker",
    "profile_name",
    "profile_command_hash",
    "source_bundle_hash",
    "evidence_hash",
}
_APPROVAL_KEYS = {
    "approval_id",
    "run_id",
    "operator_identity",
    "approval_scope",
    "requested_at",
    "expires_at",
    "excluded_authorities",
}
_CONTROL_KEYS = {
    "timeout_seconds",
    "max_output_bytes",
    "replay_ledger_identity",
    "operator_stop_required",
    "cleanup_required",
    "proof_markers",
}
_REQUIRED_PROOF_MARKERS = {
    "EXACT_TARGET_BOUND",
    "REPLAY_PROTECTION_REQUIRED",
    "OUTPUT_BOUND_REQUIRED",
    "OPERATOR_STOP_REQUIRED",
    "NO_SOURCE_MUTATION_REQUIRED",
    "NO_PROTECTED_BODY_READ_REQUIRED",
}
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_LAUNDERING_RE = re.compile(
    r"approved[_\s-]*for[_\s-]*live[_\s-]*execution|runtime[_\s-]*pilot[_\s-]*approved|"
    r"live[_\s-]*(?:scan|validation)[_\s-]*(?:allowed|authorized|authorised|approved)|"
    r"kuronode[_\s-]*(?:repo|repository)[_\s-]*scan|typescript[_\s-]*(?:tooling|typecheck)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s]*test[_\s-]*mcp|beo[_\s-]*publication|authoritative[_\s-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|source[_\s-]*mutation|git[_\s-]*mutation|"
    r"protected[_\s-]*blk[-_\s]*req[_\s-]*body|private[_\s-]*key|api[_\s-]*key|bearer",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)


def build_kuronode_power_of_ten_gate_pilot_approval_envelope(
    target_package: dict[str, Any],
    readiness_evidence: dict[str, Any],
    approval_package: dict[str, Any],
    pilot_controls: dict[str, Any],
    *,
    now: str | None = None,
) -> dict[str, Any]:
    """Build readiness for human review; never execute the future pilot."""

    target = _validate_target(target_package)
    evidence = _validate_evidence(readiness_evidence)
    approval = _validate_approval(approval_package, now=now)
    controls = _validate_controls(pilot_controls)
    envelope = {
        "envelope_status": READY_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "approval_id": approval["approval_id"],
        "run_id": approval["run_id"],
        "operator_identity": approval["operator_identity"],
        "requested_at": approval["requested_at"],
        "expires_at": approval["expires_at"],
        "target_repo_identity": target["target_repo_identity"],
        "target_branch": target["target_branch"],
        "target_head_sha": target["target_head_sha"],
        "target_workspace_identity": target["target_workspace_identity"],
        "target_scope": target["target_scope"],
        "profile_name": evidence["profile_name"],
        "profile_command_hash": evidence["profile_command_hash"],
        "source_bundle_hash": evidence["source_bundle_hash"],
        "readiness_evidence_hash": evidence["evidence_hash"],
        "pilot_controls": controls,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "live_kuronode_scan_performed": False,
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
        "production_isolation_claimed": False,
    }
    envelope["envelope_hash"] = _canonical_hash({k: v for k, v in envelope.items() if k != "envelope_hash"})
    return envelope


def _validate_target(target: dict[str, Any]) -> dict[str, str]:
    _require_dict(target, "target_package")
    _reject_laundering(target, "target_package")
    _enforce_keys(target, _TARGET_KEYS, "target_package")
    head = _required_string(target.get("target_head_sha"), "target_head_sha")
    if not _COMMIT_RE.match(head):
        raise ValueError("target_head_sha must be a 40-character hex commit")
    return {
        "target_repo_identity": _required_string(target.get("target_repo_identity"), "target_repo_identity"),
        "target_branch": _required_string(target.get("target_branch"), "target_branch"),
        "target_head_sha": head,
        "target_workspace_identity": _required_string(target.get("target_workspace_identity"), "target_workspace_identity"),
        "target_scope": _required_string(target.get("target_scope"), "target_scope"),
    }


def _validate_evidence(evidence: dict[str, Any]) -> dict[str, str]:
    _require_dict(evidence, "readiness_evidence")
    _reject_laundering(evidence, "readiness_evidence")
    _enforce_keys(evidence, _EVIDENCE_KEYS, "readiness_evidence")
    _require_exact(evidence.get("static_profile_boundary_marker"), "KURONODE_TYPESCRIPT_POWER_OF_TEN_STATIC_PROFILE_BOUNDARY", "static_profile_boundary_marker")
    _require_exact(evidence.get("validation_profile_boundary_marker"), "KURONODE_POWER_OF_TEN_VALIDATION_PROFILE_REGISTRY_BOUNDARY", "validation_profile_boundary_marker")
    _require_exact(evidence.get("static_profile_status"), "KURONODE_POWER_OF_TEN_STATIC_PROFILE_PASS_FIXTURE_ONLY", "static_profile_status")
    _require_exact(evidence.get("fixture_profile_marker"), "KURONODE_POWER_OF_TEN_STATIC_FIXTURE_SELFTEST_PROFILE_REGISTERED", "fixture_profile_marker")
    if _required_string(evidence.get("profile_name"), "profile_name") != PROFILE_NAME:
        raise ValueError("profile_name must be kuronode-power-of-ten-static-fixture")
    if _required_hash(evidence.get("profile_command_hash"), "profile_command_hash") != _sha(PROFILE_COMMAND):
        raise ValueError("profile_command_hash does not match exact fixture command")
    return {
        "profile_name": PROFILE_NAME,
        "profile_command_hash": evidence["profile_command_hash"],
        "source_bundle_hash": _required_hash(evidence.get("source_bundle_hash"), "source_bundle_hash"),
        "evidence_hash": _required_hash(evidence.get("evidence_hash"), "evidence_hash"),
    }


def _validate_approval(approval: dict[str, Any], *, now: str | None) -> dict[str, str]:
    _require_dict(approval, "approval_package")
    _reject_laundering({k: v for k, v in approval.items() if k != "excluded_authorities"}, "approval_package")
    _enforce_keys(approval, _APPROVAL_KEYS, "approval_package")
    _require_exact(approval.get("approval_scope"), APPROVAL_SCOPE, "approval_scope")
    approval_id = _required_string(approval.get("approval_id"), "approval_id")
    run_id = _required_string(approval.get("run_id"), "run_id")
    if not approval_id.startswith("BLK-SYSTEM-058-KURONODE-GATE-APPROVAL-"):
        raise ValueError("approval_id must bind to BLK-SYSTEM-058")
    if not run_id.startswith("BLK-SYSTEM-058-KURONODE-GATE-RUN-"):
        raise ValueError("run_id must bind to BLK-SYSTEM-058")
    _validate_excluded_authorities(approval.get("excluded_authorities"))
    requested = _parse_time(_required_string(approval.get("requested_at"), "requested_at"), "requested_at")
    expires = _parse_time(_required_string(approval.get("expires_at"), "expires_at"), "expires_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")
    if now is not None and expires <= _parse_time(now, "now"):
        raise ValueError("approval envelope is expired")
    return {
        "approval_id": approval_id,
        "run_id": run_id,
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "requested_at": approval["requested_at"],
        "expires_at": approval["expires_at"],
    }


def _validate_controls(controls: dict[str, Any]) -> dict[str, Any]:
    _require_dict(controls, "pilot_controls")
    _reject_laundering({k: v for k, v in controls.items() if k != "proof_markers"}, "pilot_controls")
    _enforce_keys(controls, _CONTROL_KEYS, "pilot_controls")
    if controls.get("operator_stop_required") is not True:
        raise ValueError("operator_stop_required must be true")
    if controls.get("cleanup_required") is not True:
        raise ValueError("cleanup_required must be true")
    timeout = _bounded_int(controls.get("timeout_seconds"), "timeout_seconds", 1, 120)
    output = _bounded_int(controls.get("max_output_bytes"), "max_output_bytes", 1, 200000)
    markers = controls.get("proof_markers")
    if not isinstance(markers, list) or set(markers) != _REQUIRED_PROOF_MARKERS or len(markers) != len(_REQUIRED_PROOF_MARKERS):
        raise ValueError("proof_markers must include exact pilot safety markers")
    return {
        "timeout_seconds": timeout,
        "max_output_bytes": output,
        "replay_ledger_identity": _required_string(controls.get("replay_ledger_identity"), "replay_ledger_identity"),
        "operator_stop_required": True,
        "cleanup_required": True,
        "proof_markers": sorted(_REQUIRED_PROOF_MARKERS),
    }


def _validate_excluded_authorities(excluded: Any) -> None:
    if not isinstance(excluded, list) or not all(isinstance(item, str) for item in excluded):
        raise ValueError("excluded_authorities must match exact denied authority set")
    if set(excluded) != EXACT_EXCLUDED_AUTHORITIES or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES):
        raise ValueError("excluded_authorities must match exact denied authority set")


def _reject_laundering(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_laundering(str(key), label)
            _reject_laundering(item, label)
    elif isinstance(value, list):
        for item in value:
            _reject_laundering(item, label)
    elif isinstance(value, str):
        decoded = value
        for _ in range(2):
            decoded = unquote(decoded)
        if _PROTECTED_RE.search(decoded):
            raise ValueError(f"{label} contains protected BLK-req body reference")
        normalized = re.sub(r"([a-z])([A-Z])", r"\1 \2", decoded)
        normalized = re.sub(r"[^A-Za-z0-9]+", " ", normalized)
        joined = normalized.replace(" ", "")
        if _LAUNDERING_RE.search(decoded) or _LAUNDERING_RE.search(normalized) or _LAUNDERING_RE.search(joined):
            raise ValueError(f"{label} contains authority-laundering text")


def _enforce_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if missing:
        raise ValueError(f"{label} missing keys: {missing}")
    if extra:
        raise ValueError(f"{label} unsupported keys: {extra}")


def _require_dict(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dict")


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    _reject_laundering(value, label)
    return value


def _require_exact(value: Any, expected: str, label: str) -> None:
    if _required_string(value, label) != expected:
        raise ValueError(f"{label} must be {expected}")


def _required_hash(value: Any, label: str) -> str:
    text = _required_string(value, label)
    if not _HASH_RE.match(text):
        raise ValueError(f"{label} must be sha256 hash")
    return text


def _bounded_int(value: Any, label: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}")
    return value


def _parse_time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed


def _sha(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_hash(value: dict[str, Any]) -> str:
    stable = json.dumps(deepcopy(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()
