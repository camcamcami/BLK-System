"""Non-runtime CEB_009 remediation packet fixture.

This module converts BLK-SYSTEM-059 CEB_009 static findings into a deterministic
review packet for a future patch. It does not scan a live Kuronode checkout, edit
Kuronode source, mutate Git, launch Electron, run the smoke test, execute
TypeScript tooling, invoke package managers, start Codex or BLK-test MCP,
publish BEOs, generate RTM, or read protected BLK-req bodies.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_ceb009_static_gate_pilot import READY_STATUS as SOURCE_READY_STATUS

READY_STATUS = "KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_READY_NOT_PATCHED"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_FIXTURE_ONLY"
TARGET_PATH = "scripts/smoke_test.ts"
CEB_ID = "CEB_009"

EXACT_EXCLUDED_AUTHORITIES = {
    "LIVE_KURONODE_REPOSITORY_SCAN",
    "LIVE_KURONODE_SOURCE_VALIDATION",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "WALL_CLOCK_TIMEOUT_WAIT",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "KURONODE_SOURCE_MUTATION",
    "KURONODE_GIT_MUTATION",
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

_REQUIRED_FINDINGS = {
    "CEB009_TIMEOUT_FALSE_PASS_RISK",
    "CEB009_RESULT_SHAPE_VALIDATION_MISSING",
    "CEB009_UNSAFE_ANY_OR_TS_IGNORE_RECORDED",
    "CEB009_TIMEOUT_BOUND_RECORDED",
    "CEB009_CLEANUP_PATH_RECORDED",
}
_SIDE_EFFECT_FLAGS = {
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
_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "target_path",
    "source_report_hash",
    "excluded_authorities",
    "operator_note",
}
_LAUNDERING_RE = re.compile(
    r"approved[_\s-]*for[_\s-]*live[_\s-]*execution|runtime[_\s-]*pilot[_\s-]*approved|"
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


def default_ceb009_remediation_request(source_report: dict[str, Any]) -> dict[str, Any]:
    """Return a valid non-runtime remediation-packet request."""

    return {
        "request_status": REQUEST_STATUS,
        "request_id": "BLK-SYSTEM-060-CEB009-REMEDIATION-PACKET-001",
        "operator_identity": "discord:684235178083745819",
        "target_path": TARGET_PATH,
        "source_report_hash": _required_hash(source_report.get("report_hash"), "source_report.report_hash"),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "operator_note": "review-ready remediation packet only; no Kuronode patch applied",
    }


def build_ceb009_remediation_packet(*, source_report: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic CEB_009 remediation packet without applying it."""

    validated_report = _validate_source_report(source_report)
    validated_request = _validate_request(request, validated_report)
    packet = {
        "packet_status": READY_STATUS,
        "packet_scope": "CEB_009_REMEDIATION_PACKET_FIXTURE_ONLY_NOT_PATCHED",
        "request_id": validated_request["request_id"],
        "operator_identity": validated_request["operator_identity"],
        "ceb_id": CEB_ID,
        "target_path": TARGET_PATH,
        "source_report_hash": validated_request["source_report_hash"],
        "source_findings": sorted(_REQUIRED_FINDINGS),
        "remediation_obligations": _remediation_obligations(),
        "typescript_fragment_guidance": _typescript_fragment_guidance(),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "patch_applied": False,
        "live_kuronode_scan_performed": False,
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
    packet["packet_hash"] = _canonical_hash({key: value for key, value in packet.items() if key != "packet_hash"})
    return packet


def _validate_source_report(source_report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(source_report, dict):
        raise ValueError("source_report must be a dictionary")
    if source_report.get("report_status") != SOURCE_READY_STATUS:
        raise ValueError("source report must be BLK-SYSTEM-059 ready-not-runtime output")
    _required_hash(source_report.get("report_hash"), "source_report.report_hash")
    identity = source_report.get("source_corpus_identity")
    if not isinstance(identity, dict) or identity.get("ceb_id") != CEB_ID:
        raise ValueError("source report must bind to CEB_009")
    for flag in sorted(_SIDE_EFFECT_FLAGS):
        if source_report.get(flag) is not False:
            raise ValueError(f"source report contains runtime side effect: {flag}")
    rules = set()
    for finding in source_report.get("ceb009_findings", []):
        if isinstance(finding, dict) and isinstance(finding.get("rule"), str):
            rules.add(finding["rule"])
    missing = sorted(_REQUIRED_FINDINGS - rules)
    if missing:
        raise ValueError(f"source report missing required CEB_009 finding(s): {missing}")
    return deepcopy(source_report)


def _validate_request(request: dict[str, Any], source_report: dict[str, Any]) -> dict[str, str]:
    if not isinstance(request, dict):
        raise ValueError("request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "request")
    _reject_laundering({key: value for key, value in request.items() if key != "excluded_authorities"}, "request")
    if _required_string(request.get("request_status"), "request_status") != REQUEST_STATUS:
        raise ValueError("request_status must be KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_FIXTURE_ONLY")
    target = _required_string(request.get("target_path"), "target_path")
    if _PROTECTED_RE.search(_decode_path_text(target)):
        raise ValueError("target_path rejects protected BLK-req body reference")
    if target != TARGET_PATH:
        raise ValueError("target_path must be scripts/smoke_test.ts")
    _validate_excluded_authorities(request.get("excluded_authorities"))
    source_report_hash = _required_hash(request.get("source_report_hash"), "source_report_hash")
    if source_report_hash != source_report["report_hash"]:
        raise ValueError("source_report_hash does not match submitted report")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "operator_identity": _required_string(request.get("operator_identity"), "operator_identity"),
        "source_report_hash": source_report_hash,
    }


def _remediation_obligations() -> list[dict[str, str]]:
    return [
        {
            "obligation_id": "CEB009_REMEDIATION_TIMEOUT_MUST_FAIL",
            "source_finding": "CEB009_TIMEOUT_FALSE_PASS_RISK",
            "requirement": "A timeout sentinel must throw or exit failure before any PASS log.",
        },
        {
            "obligation_id": "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_STREAM_ID",
            "source_finding": "CEB009_RESULT_SHAPE_VALIDATION_MISSING",
            "requirement": "The projection result must expose a validated string streamId before use.",
        },
        {
            "obligation_id": "CEB009_REMEDIATION_RESULT_SHAPE_VALIDATE_AST",
            "source_finding": "CEB009_RESULT_SHAPE_VALIDATION_MISSING",
            "requirement": "The projection result must expose an AST payload before PASS can be logged.",
        },
        {
            "obligation_id": "CEB009_REMEDIATION_REMOVE_ANY_AND_TS_IGNORE",
            "source_finding": "CEB009_UNSAFE_ANY_OR_TS_IGNORE_RECORDED",
            "requirement": "The future patch must replace @ts-ignore and any casts with typed API declarations or guards.",
        },
        {
            "obligation_id": "CEB009_REMEDIATION_PRESERVE_CLEANUP_UNSUB_AND_CLOSE",
            "source_finding": "CEB009_CLEANUP_PATH_RECORDED",
            "requirement": "The future patch must preserve listener unsubscribe and Electron close cleanup paths.",
        },
        {
            "obligation_id": "CEB009_REMEDIATION_NOT_RUNTIME_VALIDATION",
            "requirement": "This packet is not evidence that the smoke test ran or passed.",
        },
    ]


def _typescript_fragment_guidance() -> list[str]:
    return [
        "interface ProjectionResult { streamId: string; ast?: unknown; _type?: string }",
        "const isProjectionResult = (value: unknown): value is ProjectionResult => typeof value === 'object' && value !== null && typeof (value as { streamId?: unknown }).streamId === 'string';",
        "if (!isProjectionResult(result)) { throw new Error('Projection result shape invalid'); }",
        "if (result.streamId === 'timeout') { throw new Error('Projection timed out before kur:projection-result'); }",
        "if (!result.ast) { throw new Error('Projection result missing ast payload'); }",
        "Preserve listener cleanup by calling unsub() exactly once after kur:projection-result resolves.",
        "Preserve process cleanup by retaining the finally block that awaits electronApp.close().",
    ]


def _validate_excluded_authorities(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")


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


def _sha(value: Any) -> str:
    stable = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(stable).hexdigest()
