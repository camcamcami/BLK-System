"""BLK-SYSTEM-072 exact-target approval-envelope fixture for Kuronode BLK-test module pilot.

This module validates a review-only exact-target approval envelope for a future
read-only BLK-test functional-module pilot over the Kuronode workspace. It does
not approve runtime, execute BLK-test, start MCP, invoke tooling, mutate source
or Git, publish BEOs, generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any

from blk_test_kuronode_workspace_pilot_request import READY_STATUS as REQUEST_READY_STATUS

ENVELOPE_READY_STATUS = "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
APPROVAL_SCOPE = "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_REVIEW_ONLY"
ROLE_STATEMENT = "BLK-test is a BLK-System functional module, not BLK-System's test suite."
TARGET_REPO_PATH = "/home/dad/code/Kuronode-v1"
TARGET_BRANCH = "main"
TARGET_HEAD_SHA = "38e332b188e45edcb484765694112c9041ad1a3b"
WORKSPACE_STATUS = "main...origin/main [ahead 1]"
FIXED_TOOL = "run_ast_validation"
TOOL_MODE = "READ_ONLY_STATIC_AST_VALIDATION_FUTURE_RUNTIME_ONLY"

REQUIRED_ENVELOPE_PROOF_MARKERS = frozenset(
    {
        "UPSTREAM_REQUEST_HASH_RECOMPUTED",
        "EXACT_KURONODE_TARGET_BOUND",
        "FRESH_BLK_SYSTEM_072_APPROVAL_ID_REQUIRED",
        "FRESH_BLK_SYSTEM_072_RUN_ID_REQUIRED",
        "REPLAY_POLICY_REVIEW_ONLY",
        "READ_ONLY_FIXED_TOOL_FUTURE_RUNTIME_ONLY",
        "NO_RUNTIME_APPROVAL_GRANTED",
        "NO_CEB009_REUSE",
        "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
        "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
    }
)

ENVELOPE_EXCLUDED_AUTHORITIES = frozenset(
    {
        "RUNTIME_APPROVAL",
        "BLK_TEST_RUNTIME_EXECUTION_AGAINST_KURONODE",
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
        "KURONODE_SOURCE_MUTATION",
        "KURONODE_GIT_MUTATION",
        "KURONODE_REMOTE_PUSH",
        "CEB009_ARTIFACT_REUSE_AS_EXECUTABLE_FIXTURE",
        "CEB009_APPROVAL_OR_RUN_ID_REUSE",
        "BLK_SYSTEM_071_REQUEST_AS_RUNTIME_APPROVAL",
        "BLK_TEST_AS_BLK_SYSTEM_TEST_SUITE_SEMANTICS",
        "PROTECTED_BLK_REQ_BODY_READ",
        "PROTECTED_BODY_COPYING_PARSING_HASHING_SUMMARIZING_SCANNING_MUTATION_OR_DRIFT_COMPARISON",
        "AUTHORITATIVE_BEO_PUBLICATION",
        "RUNTIME_PUBLISHED_BEO_OUTPUT",
        "RUNTIME_RTM_GENERATION",
        "RTM_DRIFT_REJECTION",
        "COVERAGE_MATRIX_OR_COVERAGE_CLAIM_PROMOTION",
        "ACTIVE_VAULT_HASH_COMPARISON",
        "PUBLIC_LEDGER_MUTATION",
        "SIGNER_STORAGE_ROLLBACK_REVOCATION_SUPERSESSION_OR_RELEASE_AUTHORITY",
        "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
        "LIVE_CODEX_EXECUTION",
        "LIVE_TACTICAL_LLM_DISPATCH",
    }
)

ENVELOPE_NO_SIDE_EFFECT_FLAGS = frozenset(
    {
        "runtime_approved",
        "blk_test_runtime_executed",
        "blk_test_mcp_started",
        "subprocess_started",
        "electron_started",
        "smoke_test_started",
        "typescript_tooling_executed",
        "package_manager_invoked",
        "network_accessed",
        "model_service_accessed",
        "browser_tooling_invoked",
        "cyber_tooling_invoked",
        "kuronode_source_mutated",
        "kuronode_git_mutated",
        "kuronode_remote_pushed",
        "ceb009_artifact_reused_as_fixture",
        "ceb009_approval_or_run_id_reused",
        "protected_body_read",
        "beo_published",
        "rtm_generated",
        "drift_rejected",
        "coverage_claim_promoted",
        "active_vault_hash_" + "compared",
        "public_ledger_mutated",
        "signer_storage_rollback_authority_used",
        "production_isolation_claimed",
        "codex_started",
    }
)

_UPSTREAM_REQUEST_KEYS = frozenset(
    {
        "beo_publication",
        "blk_test_role_statement",
        "blk_test_runtime_executed",
        "ceb009_reuse_allowed",
        "coverage_claim_status",
        "excluded_authorities",
        "fixed_tool",
        "generic_mcp_authorized",
        "git_mutation_allowed",
        "historical_references_only",
        "no_side_effects",
        "operator_identity",
        "production_isolation_claimed",
        "production_mcp_authorized",
        "proof_markers",
        "protected_body_read_allowed",
        "request_hash",
        "request_id",
        "request_scope",
        "requested_at",
        "rtm_status",
        "runtime_approved",
        "source_mutation_allowed",
        "status",
        "target_branch",
        "target_head_sha",
        "target_repo_path",
        "target_scope",
        "target_workspace_label",
        "tool_mode",
        "workspace_status",
    }
)

_ENVELOPE_KEYS = frozenset(
    {
        "approval_envelope_id",
        "approval_id",
        "run_id",
        "operator_identity",
        "requested_at",
        "expires_at",
        "approval_scope",
        "blk_test_role_statement",
        "target_repo_path",
        "target_branch",
        "target_head_sha",
        "workspace_status",
        "fixed_tool",
        "tool_mode",
        "timeout_output_profile",
        "replay_policy",
        "operator_stop_control",
        "proof_markers",
        "excluded_authorities",
        "no_side_effects",
    }
)
_TIMEOUT_KEYS = frozenset({"timeout_seconds", "max_output_bytes"})
_REPLAY_KEYS = frozenset({"replay_ledger_identity", "approval_id_one_use", "run_id_one_use", "consumed_ids_rejected"})
_MAX_REVIEW_TTL = timedelta(hours=4)
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

_NAMING_RE = re.compile(
    r"BLK[-_\s]?System\s+test\s+suite|test\s+of\s+BLK[-_\s]?System|testing\s+BLK[-_\s]?System\s+with\s+Kuronode|BLK[-_\s]?System\s+itself\s+was\s+tested|BLK[-_\s]?test\s+validates\s+BLK[-_\s]?System",
    re.IGNORECASE,
)
_FORBIDDEN_RE = re.compile(
    r"APPROVED[_\s-]*FOR[_\s-]*LIVE[_\s-]*EXECUTION|runtime[_\s-]*(?:execution|approval|pilot|approved)[_\s-]*(?:is[_\s-]*)?(?:authorized|authorised|approved|allowed|granted)?|"
    r"live[_\s-]*(?:execution|validation|scan|run)[_\s-]*(?:authorized|authorised|approved|allowed|permitted|granted)|"
    r"production[_\s-]*BLK[-_\s]*test[_\s-]*MCP|generic[_\s-]*BLK[-_\s]*test[_\s-]*MCP|"
    r"BEO[_\s-]*(?:publication|is|output)?[_\s-]*(?:PUBLISHED|published|authorized|authorised|approved|allowed|enabled|granted)|authoritative[_\s-]*BEO|published[_\s-]*BEO[_\s-]*output|"
    r"RTM(?:ID|Generated|Generation)?|RTM[_\s-]*(?:generation|drift|generated|emitted)|drift[_\s-]*(?:rejection|decision)|coverage[_\s-]*(?:matrix|claim|complete|truth|is)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|docs[\\/]+active|read[_\s-]*protected[_\s-]*BLK[-_\s]*req[_\s-]*body|protected[_\s-]*body[_\s-]*read|"
    r"\b(?:npm|npx|pnpm|yarn|bun|tsc|eslint|prettier|curl|wget|ssh|scp|rsync|docker)\b|"
    r"package[-_\s]*manager|network[_\s-]*(?:allowed|authorized|authorised)|model[_\s-]*service|browser[_\s-]*tooling|cyber[_\s-]*tooling|"
    r"source[_\s-]*(?:mutation|writes?)[_\s-]*(?:allowed|authorized|authorised|approved|enabled)?|git[_\s-]*(?:push|mutation|reset|checkout|commit|stash|revert|staging|write)|"
    r"executable[_\s-]*fixture[_\s-]*input|approval[_\s-]*id|run[_\s-]*id|"
    r"production[_\s-]*(?:sandbox|isolation)[_\s-]*(?:is[_\s-]*)?(?:enforced|claimed|proven)|\.env|secret(?:s|[_\s-]*key)?|credential|token|private[_\s-]*key|api[_\s-]*key|authorization|bearer",
    re.IGNORECASE,
)
_CONSUMED_ID_RE = re.compile(r"CEB[_-]?009|CEB009|BLK-SYSTEM-07[01]|BLK-07[12]|BLK-SYSTEM-05[12]", re.IGNORECASE)


def build_kuronode_workspace_exact_target_approval_envelope(
    upstream_request_package: dict[str, Any], approval_envelope: dict[str, Any]
) -> dict[str, Any]:
    """Validate review-only approval-envelope readiness; never approves runtime."""

    request = _validate_upstream_request(upstream_request_package)
    envelope = _validate_envelope(approval_envelope)
    result = {
        "status": ENVELOPE_READY_STATUS,
        "upstream_request_status": request["status"],
        "upstream_request_hash": request["request_hash"],
        "approval_envelope_id": envelope["approval_envelope_id"],
        "approval_id": envelope["approval_id"],
        "run_id": envelope["run_id"],
        "operator_identity": envelope["operator_identity"],
        "requested_at": envelope["requested_at"],
        "expires_at": envelope["expires_at"],
        "approval_scope": APPROVAL_SCOPE,
        "blk_test_role_statement": ROLE_STATEMENT,
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "workspace_status": WORKSPACE_STATUS,
        "fixed_tool": FIXED_TOOL,
        "tool_mode": TOOL_MODE,
        "timeout_output_profile": deepcopy(envelope["timeout_output_profile"]),
        "replay_policy": deepcopy(envelope["replay_policy"]),
        "operator_stop_control": envelope["operator_stop_control"],
        "proof_markers": sorted(REQUIRED_ENVELOPE_PROOF_MARKERS),
        "excluded_authorities": sorted(ENVELOPE_EXCLUDED_AUTHORITIES),
        "no_side_effects": deepcopy(envelope["no_side_effects"]),
        "runtime_approved": False,
        "blk_test_runtime_executed": False,
        "source_mutation_allowed": False,
        "git_mutation_allowed": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "coverage_claim_status": "NOT_PROMOTED",
        "production_mcp_authorized": False,
        "generic_mcp_authorized": False,
        "protected_body_read_allowed": False,
        "ceb009_reuse_allowed": False,
        "production_isolation_claimed": False,
    }
    result["envelope_hash"] = _canonical_hash({k: v for k, v in result.items() if k != "envelope_hash"})
    return result


def _validate_upstream_request(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "upstream_request_package")
    _enforce_keys(package, _UPSTREAM_REQUEST_KEYS, "upstream_request_package")
    if package.get("status") != REQUEST_READY_STATUS:
        raise ValueError("upstream request status must be BLK-SYSTEM-071 request-ready")
    supplied_hash = _string(package.get("request_hash"), "request_hash")
    if not _HASH_RE.match(supplied_hash):
        raise ValueError("request_hash must be sha256")
    recomputed = _canonical_hash({k: v for k, v in package.items() if k != "request_hash"})
    if recomputed != supplied_hash:
        raise ValueError("upstream request hash mismatch")
    for key, expected in {
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "workspace_status": WORKSPACE_STATUS,
        "fixed_tool": FIXED_TOOL,
        "blk_test_role_statement": ROLE_STATEMENT,
    }.items():
        if package.get(key) != expected:
            raise ValueError(f"upstream request {key} mismatch")
    return package


def _validate_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    _require_dict(envelope, "approval_envelope")
    _enforce_keys(envelope, _ENVELOPE_KEYS, "approval_envelope")
    _reject_laundering({k: v for k, v in envelope.items() if k not in {"approval_envelope_id", "approval_id", "run_id", "replay_policy", "proof_markers", "excluded_authorities", "no_side_effects"}}, "approval_envelope")
    if _string(envelope["approval_envelope_id"], "approval_envelope_id") != "BLK-SYSTEM-072-KURONODE-WORKSPACE-APPROVAL-ENVELOPE-001":
        raise ValueError("approval_envelope_id must be exact BLK-SYSTEM-072 ID")
    approval_id = _string(envelope["approval_id"], "approval_id")
    run_id = _string(envelope["run_id"], "run_id")
    if approval_id != "APPROVAL-BLK-SYSTEM-072-KURONODE-WORKSPACE-001":
        raise ValueError("approval_id must be fresh BLK-SYSTEM-072 ID")
    if run_id != "RUN-BLK-SYSTEM-072-KURONODE-WORKSPACE-001":
        raise ValueError("run_id must be fresh BLK-SYSTEM-072 ID")
    if _CONSUMED_ID_RE.search(approval_id) and "BLK-SYSTEM-072" not in approval_id:
        raise ValueError("approval_id reuses consumed lineage")
    if _CONSUMED_ID_RE.search(run_id) and "BLK-SYSTEM-072" not in run_id:
        raise ValueError("run_id reuses consumed lineage")
    if not _string(envelope["operator_identity"], "operator_identity").startswith("discord:684235178083745819:"):
        raise ValueError("operator_identity mismatch")
    requested = _parse_time(_string(envelope["requested_at"], "requested_at"), "requested_at")
    expires = _parse_time(_string(envelope["expires_at"], "expires_at"), "expires_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")
    if expires - requested > _MAX_REVIEW_TTL:
        raise ValueError("expires_at exceeds maximum review TTL")
    exacts = {
        "approval_scope": APPROVAL_SCOPE,
        "blk_test_role_statement": ROLE_STATEMENT,
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "workspace_status": WORKSPACE_STATUS,
        "fixed_tool": FIXED_TOOL,
        "tool_mode": TOOL_MODE,
    }
    for key, expected in exacts.items():
        if envelope[key] != expected:
            raise ValueError(f"{key} mismatch")
    _validate_timeout(envelope["timeout_output_profile"])
    _validate_replay(envelope["replay_policy"])
    if _string(envelope["operator_stop_control"], "operator_stop_control") != "operator can stop before any separately approved future runtime begins":
        raise ValueError("operator_stop_control mismatch")
    _validate_exact_string_set(envelope["proof_markers"], REQUIRED_ENVELOPE_PROOF_MARKERS, "proof_markers")
    _validate_exact_string_set(envelope["excluded_authorities"], ENVELOPE_EXCLUDED_AUTHORITIES, "excluded_authorities")
    _validate_no_side_effects(envelope["no_side_effects"])
    return envelope


def _validate_timeout(profile: Any) -> None:
    _require_dict(profile, "timeout_output_profile")
    _enforce_keys(profile, _TIMEOUT_KEYS, "timeout_output_profile")
    if profile.get("timeout_seconds") != 30:
        raise ValueError("timeout_seconds must be 30")
    if profile.get("max_output_bytes") != 4096:
        raise ValueError("max_output_bytes must be 4096")


def _validate_replay(policy: Any) -> None:
    _require_dict(policy, "replay_policy")
    _enforce_keys(policy, _REPLAY_KEYS, "replay_policy")
    ledger = _string(policy["replay_ledger_identity"], "replay_ledger_identity")
    if ledger != "BLK-SYSTEM-072-KURONODE-WORKSPACE-REPLAY-LEDGER-REVIEW-ONLY":
        raise ValueError("replay_ledger_identity mismatch")
    for key in ["approval_id_one_use", "run_id_one_use", "consumed_ids_rejected"]:
        if policy.get(key) is not True:
            raise ValueError(f"{key} must be true")


def _validate_no_side_effects(flags: Any) -> None:
    _require_dict(flags, "no_side_effects")
    if set(flags) != ENVELOPE_NO_SIDE_EFFECT_FLAGS:
        raise ValueError("no_side_effects must contain exact required flags")
    offenders = [key for key, value in flags.items() if value is not False]
    if offenders:
        raise ValueError(f"no_side_effects must all be false: {offenders}")


def _validate_exact_string_set(values: Any, expected: frozenset[str], field: str) -> None:
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list")
    if any(not isinstance(value, str) for value in values):
        raise ValueError(f"{field} entries must be strings")
    if len(values) != len(set(values)):
        raise ValueError(f"{field} must not contain duplicates")
    if set(values) != expected:
        raise ValueError(f"{field} must match exact required set")
    if any(value.lower() in {"ok", "pass", "done"} for value in values):
        raise ValueError(f"{field} must not contain placeholders")


def _reject_laundering(value: Any, path: str, *, skip_hash: bool = False) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if skip_hash and key_text.endswith("hash"):
                continue
            if _NAMING_RE.search(key_text) or _FORBIDDEN_RE.search(key_text):
                raise ValueError(f"forbidden authority marker at {path}.{key_text}")
            _reject_laundering(item, f"{path}.{key_text}", skip_hash=skip_hash)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            _reject_laundering(item, f"{path}[{idx}]", skip_hash=skip_hash)
    elif isinstance(value, str):
        if skip_hash and _HASH_RE.match(value):
            return
        if _NAMING_RE.search(value) or _FORBIDDEN_RE.search(value):
            raise ValueError(f"forbidden authority marker at {path}")


def _require_dict(value: Any, field: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be a dict")


def _enforce_keys(value: dict[str, Any], expected: frozenset[str], field: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{field} must contain exact keys")


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _parse_time(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must be timezone-aware")
    return parsed


def _canonical_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
