"""BLK-SYSTEM-071 Kuronode workspace BLK-test module pilot request fixture.

This module creates a deterministic human-review request package for a future
read-only BLK-test functional-module pilot over the Kuronode workspace. It does
not execute BLK-test runtime, start BLK-test MCP, invoke shell/tooling, mutate
source/Git, reuse CEB_009 authority, publish BEOs, generate RTM, or read
protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
from copy import deepcopy
from typing import Any

READY_STATUS = "BLK_TEST_KURONODE_WORKSPACE_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME"
REQUEST_SCOPE = "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_REQUEST_ONLY"
TARGET_REPO_PATH = "/home/dad/code/Kuronode-v1"
TARGET_BRANCH = "main"
TARGET_HEAD_SHA = "38e332b188e45edcb484765694112c9041ad1a3b"
TARGET_WORKSPACE_LABEL = "kuronode-v1-local-workspace"
WORKSPACE_STATUS = "main...origin/main [ahead 1]"
FIXED_TOOL = "run_ast_validation"
TOOL_MODE = "READ_ONLY_STATIC_AST_VALIDATION_REQUEST_ONLY"
ROLE_STATEMENT = "BLK-test is a BLK-System functional module, not BLK-System's test suite."

REQUIRED_PROOF_MARKERS = frozenset(
    {
        "BLK_TEST_MODULE_NOT_BLK_SYSTEM_TEST_SUITE",
        "KURONODE_WORKSPACE_EXACT_TARGET_BOUND",
        "READ_ONLY_FIXED_TOOL_ONLY",
        "NO_CEB009_REUSE",
        "NO_SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
        "NO_PROTECTED_BODY_READ",
        "BEO_RTM_AND_COVERAGE_AUTHORITY_SEPARATE",
    }
)

EXACT_EXCLUDED_AUTHORITIES = frozenset(
    {
        "PRODUCTION_BLK_TEST_MCP",
        "GENERIC_BLK_TEST_MCP",
        "REUSABLE_BLK_TEST_SERVICE_STARTUP",
        "RUNTIME_BLK_TEST_EXECUTION_AGAINST_KURONODE",
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

NO_SIDE_EFFECT_FLAGS = frozenset(
    {
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
        "active_vault_hash_compared",
        "public_ledger_mutated",
        "signer_storage_rollback_authority_used",
        "production_isolation_claimed",
        "codex_started",
    }
)

_TARGET_KEYS = frozenset(
    {
        "target_repo_path",
        "target_branch",
        "target_head_sha",
        "target_workspace_label",
        "target_scope",
        "workspace_status",
    }
)
_REQUEST_KEYS = frozenset(
    {
        "request_id",
        "operator_identity",
        "requested_at",
        "request_scope",
        "blk_test_role_statement",
        "fixed_tool",
        "tool_mode",
        "proof_markers",
        "historical_references_only",
        "consumed_authority_ids_reused",
        "excluded_authorities",
        "no_side_effects",
    }
)
_HASH_PREFIX = "sha256:"
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_ISO_OFFSET_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

_NAMING_LAUNDERING_RE = re.compile(
    r"BLK[-_\s]?System\s+test\s+suite|test\s+of\s+BLK[-_\s]?System|"
    r"testing\s+BLK[-_\s]?System\s+with\s+Kuronode|BLK[-_\s]?System\s+itself\s+was\s+tested",
    re.IGNORECASE,
)
_FORBIDDEN_RE = re.compile(
    r"APPROVED[_\s-]*FOR[_\s-]*LIVE[_\s-]*EXECUTION|runtime[_\s-]*(?:execution|approval|pilot)[_\s-]*(?:is[_\s-]*)?(?:authorized|authorised|approved|allowed|granted)|"
    r"live[_\s-]*(?:execution|validation|scan)[_\s-]*(?:authorized|authorised|approved|allowed)|"
    r"production[_\s-]*BLK[-_\s]*test[_\s-]*MCP[_\s-]*(?:is[_\s-]*)?(?:authorized|authorised|approved|allowed)|"
    r"generic[_\s-]*BLK[-_\s]*test[_\s-]*MCP[_\s-]*(?:is[_\s-]*)?(?:authorized|authorised|approved|allowed)|"
    r"BEO[_\s-]*publication[_\s-]*(?:is[_\s-]*)?(?:authorized|authorised|approved|allowed)|authoritative[_\s-]*BEO|"
    r"RTM(?:ID|Generated|Generation)?|RTM[_\s-]*(?:generation|drift)|drift[_\s-]*rejection|coverage[_\s-]*(?:matrix|claim)|"
    r"active[_\s-]*vault[_\s-]*hash[_\s-]*comparison|docs[\\/]+active|read[_\s-]*protected[_\s-]*BLK[-_\s]*req[_\s-]*body|protected[_\s-]*body[_\s-]*read|"
    r"\b(?:npm|npx|pnpm|yarn|bun|tsc|eslint|prettier|curl|wget|ssh|scp|rsync|docker)\b|"
    r"package[-_\s]*manager|network[_\s-]*(?:allowed|authorized|authorised)|model[_\s-]*service|browser[_\s-]*tooling|cyber[_\s-]*tooling|"
    r"source[_\s-]*mutation[_\s-]*(?:allowed|authorized|authorised|approved)?|git[_\s-]*(?:push|mutation|reset|checkout|commit|stash|revert)|"
    r"production[_\s-]*(?:sandbox|isolation)[_\s-]*(?:is[_\s-]*)?(?:enforced|claimed|proven)|private[_\s-]*key|api[_\s-]*key|bearer",
    re.IGNORECASE,
)
_CEB_REUSE_RE = re.compile(r"CEB[_-]?009|CEB009|BLK-SYSTEM-070_task-001|blk-pipe payload|blk-pipe report", re.IGNORECASE)


def build_kuronode_workspace_pilot_request(target_package: dict[str, Any], request_package: dict[str, Any]) -> dict[str, Any]:
    """Build a non-runtime request package for future human review."""

    target = _validate_target(target_package)
    request = _validate_request(request_package)
    package = {
        "status": READY_STATUS,
        "request_scope": REQUEST_SCOPE,
        "request_id": request["request_id"],
        "operator_identity": request["operator_identity"],
        "requested_at": request["requested_at"],
        "blk_test_role_statement": ROLE_STATEMENT,
        "target_repo_path": TARGET_REPO_PATH,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "target_workspace_label": TARGET_WORKSPACE_LABEL,
        "target_scope": target["target_scope"],
        "workspace_status": WORKSPACE_STATUS,
        "fixed_tool": FIXED_TOOL,
        "tool_mode": TOOL_MODE,
        "proof_markers": sorted(REQUIRED_PROOF_MARKERS),
        "historical_references_only": deepcopy(request["historical_references_only"]),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "no_side_effects": deepcopy(request["no_side_effects"]),
        "runtime_approved": False,
        "blk_test_runtime_executed": False,
        "source_mutation_allowed": False,
        "git_mutation_allowed": False,
        "ceb009_reuse_allowed": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "coverage_claim_status": "NOT_PROMOTED",
        "production_mcp_authorized": False,
        "generic_mcp_authorized": False,
        "protected_body_read_allowed": False,
        "production_isolation_claimed": False,
    }
    package["request_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "request_hash"})
    return package


def _validate_target(target: dict[str, Any]) -> dict[str, str]:
    _require_dict(target, "target_package")
    _reject_laundering(target, "target_package")
    _enforce_keys(target, _TARGET_KEYS, "target_package")
    path = _string(target["target_repo_path"], "target_repo_path")
    if posixpath.normpath(path) != TARGET_REPO_PATH:
        raise ValueError("target_repo_path must be the exact Kuronode workspace path")
    if _string(target["target_branch"], "target_branch") != TARGET_BRANCH:
        raise ValueError("target_branch must be main")
    head = _string(target["target_head_sha"], "target_head_sha")
    if not _COMMIT_RE.match(head) or head != TARGET_HEAD_SHA:
        raise ValueError("target_head_sha must match the exact current local Kuronode HEAD")
    if _string(target["target_workspace_label"], "target_workspace_label") != TARGET_WORKSPACE_LABEL:
        raise ValueError("target_workspace_label mismatch")
    if _string(target["workspace_status"], "workspace_status") != WORKSPACE_STATUS:
        raise ValueError("workspace_status must preserve local ahead-one state")
    scope = _string(target["target_scope"], "target_scope")
    return {"target_scope": scope}


def _validate_request(request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "request_package")
    _enforce_keys(request, _REQUEST_KEYS, "request_package")
    _reject_laundering(
        {k: v for k, v in request.items() if k not in {"proof_markers", "excluded_authorities", "no_side_effects"}},
        "request_package",
    )
    request_id = _string(request["request_id"], "request_id")
    if not request_id.startswith("BLK-SYSTEM-071-KURONODE-WORKSPACE-PILOT-REQUEST-"):
        raise ValueError("request_id must bind to BLK-SYSTEM-071")
    if _CEB_REUSE_RE.search(request_id):
        raise ValueError("CEB_009 consumed authority cannot be reused")
    if not _string(request["operator_identity"], "operator_identity").startswith("discord:684235178083745819:"):
        raise ValueError("operator_identity must bind to the known operator")
    requested_at = _string(request["requested_at"], "requested_at")
    if not _ISO_OFFSET_RE.match(requested_at):
        raise ValueError("requested_at must be an offset-aware ISO timestamp")
    if _string(request["request_scope"], "request_scope") != REQUEST_SCOPE:
        raise ValueError("request_scope mismatch")
    role = _string(request["blk_test_role_statement"], "blk_test_role_statement")
    if role != ROLE_STATEMENT:
        if _NAMING_LAUNDERING_RE.search(role):
            raise ValueError("BLK-test naming boundary violated")
        raise ValueError("blk_test_role_statement must exactly preserve module naming")
    if _string(request["fixed_tool"], "fixed_tool") != FIXED_TOOL:
        raise ValueError("fixed_tool must be run_ast_validation")
    if _string(request["tool_mode"], "tool_mode") != TOOL_MODE:
        raise ValueError("tool_mode mismatch")
    _validate_proof_markers(request["proof_markers"])
    historical = _validate_historical_references(request["historical_references_only"])
    consumed = request["consumed_authority_ids_reused"]
    if not isinstance(consumed, list) or consumed:
        raise ValueError("consumed CEB_009/BLK-SYSTEM-070 authority IDs must not be reused")
    _validate_exact_string_set(request["excluded_authorities"], EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    _validate_no_side_effects(request["no_side_effects"])
    return {
        "request_id": request_id,
        "operator_identity": request["operator_identity"],
        "requested_at": requested_at,
        "historical_references_only": historical,
        "no_side_effects": request["no_side_effects"],
    }


def _validate_proof_markers(markers: Any) -> None:
    _validate_exact_string_set(markers, REQUIRED_PROOF_MARKERS, "proof_markers")
    if any(marker.lower() in {"ok", "pass", "done"} for marker in markers):
        raise ValueError("proof_markers must be meaningful, not placeholders")


def _validate_historical_references(refs: Any) -> list[str]:
    if not isinstance(refs, list) or not refs:
        raise ValueError("historical_references_only must be a non-empty list")
    result: list[str] = []
    for ref in refs:
        text = _string(ref, "historical_references_only[]")
        if _CEB_REUSE_RE.search(text):
            raise ValueError("CEB_009 artifacts may be cited only generically, not reused or named as executable inputs")
        result.append(text)
    return result


def _validate_no_side_effects(flags: Any) -> None:
    if not isinstance(flags, dict):
        raise ValueError("no_side_effects must be a dict")
    if set(flags) != NO_SIDE_EFFECT_FLAGS:
        raise ValueError("no_side_effects must contain the exact required flags")
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
        raise ValueError(f"{field} must match the exact required set")


def _reject_laundering(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if _NAMING_LAUNDERING_RE.search(key_text):
                raise ValueError("BLK-test naming boundary violated")
            if _FORBIDDEN_RE.search(key_text):
                raise ValueError(f"forbidden authority marker at {path}.{key_text}")
            _reject_laundering(item, f"{path}.{key_text}")
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            _reject_laundering(item, f"{path}[{idx}]")
    elif isinstance(value, str):
        if _NAMING_LAUNDERING_RE.search(value):
            raise ValueError("BLK-test naming boundary violated")
        if _FORBIDDEN_RE.search(value):
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


def _canonical_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return _HASH_PREFIX + hashlib.sha256(payload.encode("utf-8")).hexdigest()
