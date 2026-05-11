"""Fixture-only remediation packet for a Kuronode lifecycle cleanup finding.

BLK-SYSTEM-074 consumes the committed BLK-SYSTEM-073 read-only BLK-test
functional-module evidence and emits a deterministic remediation packet for a
future Kuronode patch decision. It does not rerun the pilot, start BLK-test MCP,
invoke BLK-pipe/Codex, launch Electron, execute smoke/TypeScript/package-manager
tooling, mutate Kuronode source or Git state, publish BEOs, generate RTM, or read
protected BLK-req bodies.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string

READY_STATUS = "KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_READY_NOT_PATCHED"
REQUEST_STATUS = "KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_FIXTURE_ONLY"
SOURCE_SPRINT = "BLK-SYSTEM-073"
SOURCE_PILOT_STATUS = "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY"
TARGET_REPO_PATH = "/home/dad/code/Kuronode-v1"
TARGET_REPO_HEAD = "38e332b188e45edcb484765694112c9041ad1a3b"
TARGET_FINDING_PATH = "smoke_test.ts"
TARGET_PATCH_PATH = "scripts/smoke_test.ts"
TARGET_FINDING_LINE = 53
TARGET_FINDING_RULE = "LIFECYCLE_CLEANUP_REQUIRED"
RETIRED_APPROVAL_ID = "APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001"
RETIRED_RUN_ID = "RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001"
FUTURE_ID_SENTINEL = "NOT_ALLOCATED_REQUIRES_SEPARATE_AUTHORITY"

EXACT_EXCLUDED_AUTHORITIES = {
    "BLK_SYSTEM_073_RUNTIME_ID_REUSE",
    "BLK_SYSTEM_073_PILOT_RERUN",
    "LIVE_KURONODE_REPOSITORY_SCAN",
    "KURONODE_SOURCE_MUTATION",
    "KURONODE_GIT_MUTATION",
    "KURONODE_STAGING_COMMIT_PUSH_RESET_CHECKOUT_OR_CLEANUP",
    "PATCH_APPROVAL_CAPTURE",
    "BLK_PIPE_EXECUTION",
    "LIVE_CODEX_EXECUTION",
    "LIVE_TACTICAL_LLM_DISPATCH",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
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
    "DRIFT_DECISION",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "source_sprint",
    "source_evidence_hash",
    "target_repo_path",
    "target_repo_head",
    "target_patch_path",
    "finding_path",
    "finding_line",
    "finding_rule",
    "proposed_future_approval_id",
    "proposed_future_run_id",
    "excluded_authorities",
    "operator_note",
}

_FALSE_EVIDENCE_FLAGS = {
    "active_vault_read",
    "arbitrary_shell_called",
    "browser_tooling_called",
    "commit_allowed",
    "coverage_claim_promoted",
    "cyber_tooling_called",
    "generic_mcp_authority",
    "git_mutation_allowed",
    "git_mutation_detected",
    "live_codex_execution",
    "model_service_called",
    "network_called",
    "package_manager_called",
    "production_isolation_claimed",
    "production_mcp_authority",
    "protected_body_read",
    "public_ledger_mutation",
    "push_allowed",
    "reusable_service_started",
    "rtm_drift_rejection",
    "source_mutation_detected",
    "source_write_allowed",
    "staging_allowed",
    "typescript_tooling_called",
}

_LAUNDERING_RE = re.compile(
    r"approved[_\s./-]*for[_\s./-]*live[_\s./-]*execution|runtime[_\s./-]*pilot[_\s./-]*approved|"
    r"(?:patch|edit|mutate)[_\s./-]*kuronode|source[_\s./-]*mutation|git[_\s./-]*mutation|"
    r"approval[_\s./-]*(?:captured|granted|inherited)|fresh[_\s./-]*(?:approval|run)[_\s./-]*id[_\s./-]*allocated|"
    r"run[_\s./-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s./-]*run[_\s./-]*test:?smoke|test:?smoke|"
    r"electron[_\s./-]*(?:launch|started|executed)|smoke[_\s./-]*test[_\s./-]*(?:executed|passed|started)|"
    r"\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"codex|blk[-_\s./]*test[_\s./-]*mcp|production[_\s./-]*blk[-_\s./]*test|"
    r"pass[_\s./-]*(?:is|as|equals|grants|approves)[_\s./-]*(?:approval|publication|beo|rtm|coverage|drift)|"
    r"beo[_\s./-]*publication|authoritative[_\s./-]*beo|publish[_\s./-]*beo|runtime[_\s./-]*published[_\s./-]*beo|"
    r"rtm(?:id|generation|generated)?|drift[_\s./-]*rejection|coverage[_\s./-]*(?:matrix|claim)|"
    r"active[_\s./-]*vault[_\s./-]*hash[_\s./-]*comparison|protected[_\s./-]*blk[-_\s./]*req[_\s./-]*body|"
    r"private[_\s./-]*key|api[_\s./-]*key|bearer|production[_\s./-]*(?:sandbox|isolation)",
    re.IGNORECASE,
)
_PROTECTED_RE = re.compile(
    r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s./-]*blk[-_\s./]*req[_\s./-]*body",
    re.IGNORECASE,
)


def load_committed_blk_system_073_evidence(path: str | Path | None = None) -> dict[str, Any]:
    """Load the committed BLK-SYSTEM-073 runtime evidence artifact."""

    selected = Path(path) if path is not None else Path(__file__).resolve().parents[1] / "docs" / "outcomes" / "BLK-SYSTEM-073_runtime-evidence.json"
    return json.loads(selected.read_text())


def default_lifecycle_cleanup_remediation_request(evidence: dict[str, Any]) -> dict[str, Any]:
    """Return a valid fixture-only remediation-packet request."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-074-LIFECYCLE-CLEANUP-REMEDIATION-PACKET-001",
        "operator_identity": "discord:684235178083745819",
        "source_sprint": SOURCE_SPRINT,
        "source_evidence_hash": _source_evidence_hash(evidence),
        "target_repo_path": TARGET_REPO_PATH,
        "target_repo_head": TARGET_REPO_HEAD,
        "target_patch_path": TARGET_PATCH_PATH,
        "finding_path": TARGET_FINDING_PATH,
        "finding_line": TARGET_FINDING_LINE,
        "finding_rule": TARGET_FINDING_RULE,
        "proposed_future_approval_id": FUTURE_ID_SENTINEL,
        "proposed_future_run_id": FUTURE_ID_SENTINEL,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "review-ready lifecycle cleanup remediation packet only; no Kuronode patch applied",
    }


def build_lifecycle_cleanup_remediation_packet(*, evidence: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic review-ready remediation packet without applying a patch."""

    validated_evidence = _validate_source_evidence(evidence)
    validated_request = _validate_request(request, validated_evidence)
    packet = {
        "packet_status": READY_STATUS,
        "packet_scope": "KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_FIXTURE_ONLY_NOT_PATCHED",
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "source_sprint": SOURCE_SPRINT,
        "source_pilot_status": SOURCE_PILOT_STATUS,
        "source_evidence_hash": validated_request["source_evidence_hash"],
        "target_repo_path": TARGET_REPO_PATH,
        "target_repo_head": TARGET_REPO_HEAD,
        "target_patch_path": TARGET_PATCH_PATH,
        "finding": {
            "path": TARGET_FINDING_PATH,
            "line": TARGET_FINDING_LINE,
            "rule": TARGET_FINDING_RULE,
        },
        "retired_runtime_ids": {
            "approval_id": RETIRED_APPROVAL_ID,
            "run_id": RETIRED_RUN_ID,
        },
        "future_runtime_id_policy": "FRESH_IDS_REQUIRED_BY_SEPARATE_AUTHORITY_NOT_ALLOCATED",
        "remediation_obligations": _remediation_obligations(),
        "remediation_guidance": _remediation_guidance(),
        "required_future_patch_boundary": [
            "separate explicit Kuronode patch authority",
            "exact target SHA and remote-head recheck",
            "exact allowlist for scripts/smoke_test.ts or successor file",
            "Kuronode closeout review before completion",
            "fresh runtime IDs for any later BLK-test recheck",
        ],
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "pilot_rerun_performed": False,
        "kuronode_source_mutation_performed": False,
        "kuronode_git_mutation_performed": False,
        "blk_pipe_invoked": False,
        "codex_started": False,
        "electron_launched": False,
        "smoke_test_executed": False,
        "typescript_tooling_executed": False,
        "package_manager_invoked": False,
        "production_blk_test_mcp_started": False,
        "protected_body_read": False,
        "beo_published": False,
        "rtm_generated": False,
        "coverage_claim_promoted": False,
        "drift_rejection_performed": False,
    }
    packet["packet_hash"] = _canonical_hash({key: value for key, value in packet.items() if key != "packet_hash"})
    return packet


def _validate_source_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        raise ValueError("source evidence must be a dictionary")
    if evidence.get("sprint") != SOURCE_SPRINT or evidence.get("status") != "FAIL" or evidence.get("pilot_status") != SOURCE_PILOT_STATUS:
        raise ValueError("source evidence must be BLK-SYSTEM-073 FAIL evidence")
    if evidence.get("approval_id") != RETIRED_APPROVAL_ID or evidence.get("run_id") != RETIRED_RUN_ID:
        raise ValueError("source evidence must bind the retired BLK-SYSTEM-073 runtime IDs")
    if evidence.get("target_repo_path") != TARGET_REPO_PATH:
        raise ValueError("source evidence target_repo_path mismatch")
    for key in ("actual_head", "expected_head", "observed_remote_head"):
        if evidence.get(key) != TARGET_REPO_HEAD:
            raise ValueError(f"source evidence {key} mismatch")
    if evidence.get("requested_tool") != "run_ast_validation":
        raise ValueError("source evidence must bind run_ast_validation")
    if evidence.get("beo_publication") != "DRAFT_ONLY" or evidence.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("source evidence must preserve BEO/RTM non-authority")
    for flag in sorted(_FALSE_EVIDENCE_FLAGS):
        if evidence.get(flag) is not False:
            raise ValueError(f"source evidence contains prohibited side effect: {flag}")
    if not evidence.get("replay_consumed_before_runtime") is True:
        raise ValueError("source evidence must record replay consumption")
    if not evidence.get("workspace_cleanup_verified") is True:
        raise ValueError("source evidence must record workspace cleanup verification")
    findings = evidence.get("findings")
    if not isinstance(findings, list) or {
        "path": TARGET_FINDING_PATH,
        "line": TARGET_FINDING_LINE,
        "rule": TARGET_FINDING_RULE,
    } not in findings:
        raise ValueError("source evidence missing exact lifecycle cleanup finding")
    return deepcopy(evidence)


def _validate_request(request: dict[str, Any], evidence: dict[str, Any]) -> dict[str, str]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "request")
    _reject_laundering({key: value for key, value in request.items() if key != "excluded_authorities"}, "request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_LIFECYCLE_CLEANUP_REMEDIATION_PACKET_FIXTURE_ONLY")
    if _required_string(request.get("source_sprint"), "source_sprint") != SOURCE_SPRINT:
        raise ValueError("source_sprint must be BLK-SYSTEM-073")
    supplied_hash = _required_hash(request.get("source_evidence_hash"), "source_evidence_hash")
    if supplied_hash != _source_evidence_hash(evidence):
        raise ValueError("source_evidence_hash does not match submitted evidence")
    if _required_string(request.get("target_repo_path"), "target_repo_path") != TARGET_REPO_PATH:
        raise ValueError("target_repo_path mismatch")
    if _required_string(request.get("target_repo_head"), "target_repo_head") != TARGET_REPO_HEAD:
        raise ValueError("target_repo_head mismatch")
    target_patch_path = _required_string(request.get("target_patch_path"), "target_patch_path")
    if _PROTECTED_RE.search(_decode_text(target_patch_path)):
        raise ValueError("target_patch_path rejects protected BLK-req body reference")
    if target_patch_path != TARGET_PATCH_PATH:
        raise ValueError("target_patch_path must be scripts/smoke_test.ts")
    if request.get("finding_path") != TARGET_FINDING_PATH or request.get("finding_line") != TARGET_FINDING_LINE or request.get("finding_rule") != TARGET_FINDING_RULE:
        raise ValueError("request must bind exact lifecycle cleanup finding")
    for key in ("proposed_future_approval_id", "proposed_future_run_id"):
        value = _required_string(request.get(key), key)
        if value in {RETIRED_APPROVAL_ID, RETIRED_RUN_ID}:
            raise ValueError("request attempts to reuse retired BLK-SYSTEM-073 runtime ID")
        if value != FUTURE_ID_SENTINEL:
            raise ValueError("future runtime IDs are not allocated by this remediation packet")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "source_evidence_hash": supplied_hash,
    }


def _remediation_obligations() -> list[dict[str, str]]:
    return [
        {
            "obligation_id": "LIFECYCLE_CLEANUP_ADD_DETERMINISTIC_TEARDOWN",
            "source_finding": TARGET_FINDING_RULE,
            "requirement": "A future patch must make the line 53 lifecycle boundary enter deterministic teardown through a finally-style path.",
        },
        {
            "obligation_id": "LIFECYCLE_CLEANUP_ASSERT_NO_ESCAPED_PROCESS_OR_LISTENER",
            "source_finding": TARGET_FINDING_RULE,
            "requirement": "A future focused regression must prove no escaped process, IPC listener, or subscription remains after completion or failure.",
        },
        {
            "obligation_id": "LIFECYCLE_CLEANUP_PRESERVE_TIMEOUT_AS_FAILURE",
            "source_finding": TARGET_FINDING_RULE,
            "requirement": "Timeout or missing projection-result paths must fail closed before any success log or pass-like evidence.",
        },
        {
            "obligation_id": "LIFECYCLE_CLEANUP_ADD_FOCUSED_REGRESSION",
            "source_finding": TARGET_FINDING_RULE,
            "requirement": "A future patch must add or update a focused test around lifecycle cleanup rather than relying on manual smoke output.",
        },
        {
            "obligation_id": "LIFECYCLE_CLEANUP_REQUIRE_FRESH_RUNTIME_IDS_FOR_RECHECK",
            "requirement": "Any later BLK-test recheck must allocate fresh approval/run IDs under a separate authority envelope.",
        },
        {
            "obligation_id": "LIFECYCLE_CLEANUP_NOT_PATCH_AUTHORITY",
            "requirement": "This packet is review-ready remediation evidence only and is not approval to patch Kuronode.",
        },
    ]


def _remediation_guidance() -> list[str]:
    return [
        "At smoke_test.ts line 53, route lifecycle-sensitive setup through deterministic cleanup that cannot be skipped by timeout or thrown errors.",
        "Use a finally-style cleanup path for Electron/app handles, IPC subscriptions, and projection listeners; cleanup must be idempotent.",
        "Name and assert every unsubscribe/close responsibility in the future patch review so missing cleanup is visible.",
        "Preserve timeout as failure evidence; do not convert timeout or missing projection-result behavior into success output.",
        "A future recheck must use fresh BLK-test runtime IDs and a separate exact-target authority envelope.",
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
        if _PROTECTED_RE.search(decoded):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
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


def _source_evidence_hash(evidence: dict[str, Any]) -> str:
    return _canonical_hash(evidence)
