"""CEB_009 patch execution approval capture and exact BLK-pipe payload gate.

This module captures the operator approval granted after BLK-SYSTEM-064 and
prepares at most one exact BLK-pipe payload. It does not invoke BLK-pipe itself;
actual invocation remains an audited sprint step after exact-target checks pass.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash, _required_hash, _required_string
from kuronode_power_of_ten_ceb009_patch_approval_envelope import (
    TARGET_BRANCH,
    TARGET_HEAD_SHA,
    TARGET_PATH,
    TARGET_REPO_IDENTITY,
)
from kuronode_power_of_ten_ceb009_patch_execution_authority_request import (
    AUTHORITY_REQUEST_MARKER,
    AUTHORITY_REQUEST_STATUS,
    build_ceb009_patch_execution_authority_request,
    default_ceb009_patch_execution_authority_request,
)
from kuronode_power_of_ten_ceb009_patch_execution_preflight import (
    build_ceb009_patch_execution_preflight,
    default_ceb009_patch_execution_preflight_request,
)
from kuronode_power_of_ten_ceb009_patch_approval_envelope import (
    build_ceb009_patch_approval_envelope,
    default_ceb009_patch_approval_request,
)
from kuronode_power_of_ten_ceb009_remediation_packet import (
    build_ceb009_remediation_packet,
    default_ceb009_remediation_request,
)
from kuronode_power_of_ten_ceb009_static_gate_pilot import (
    build_ceb009_static_gate_pilot_report,
    default_ceb009_static_corpus,
    default_ceb009_static_request,
)

APPROVAL_CAPTURE_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURED_EXACT_TARGET_CHECKED"
APPROVED_READY_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_READY_FOR_ONE_EXACT_BLK_PIPE_PATCH_ATTEMPT"
BLOCKED_TARGET_DRIFT_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_BLOCKED_TARGET_DRIFT_NOT_EXECUTED"
APPROVAL_CAPTURE_MARKER = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_AND_RUN_BOUNDARY"
REQUEST_STATUS = "KURONODE_POWER_OF_TEN_CEB009_PATCH_EXECUTION_APPROVAL_CAPTURE_REQUEST"
WORK_DIR = "/home/dad/code/Kuronode-v1"
APPROVAL_ID = "BLK-SYSTEM-065-CEB009-PATCH-EXECUTION-APPROVAL-DISCORD-684235178083745819-20260511T0811AEST"
RUN_ID = "BLK-SYSTEM-065-CEB009-PATCH-EXECUTION-RUN-001"
OPERATOR_GRANT_TEXT = "We should capture approval and perform one exact BLK-pipe-mediated patch execution in the same sprint. I explicitly grant that authority up front."

EXACT_EXCLUDED_ADJACENT_AUTHORITIES = {
    "LIVE_CODEX_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ELECTRON_OR_SMOKE_TEST_EXECUTION",
    "WALL_CLOCK_TIMEOUT_WAIT",
    "TYPESCRIPT_TOOLING_EXECUTION",
    "PACKAGE_MANAGER_INVOCATION",
    "NETWORK_ACCESS",
    "MODEL_SERVICE_ACCESS",
    "BROWSER_OR_CYBER_TOOLING",
    "AUTHORITATIVE_BEO_PUBLICATION",
    "CEO_009_PUBLICATION",
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
    "PROTECTED_BLK_REQ_BODY_READ",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
    "SOURCE_OR_GIT_MUTATION_OUTSIDE_EXACT_BLK_PIPE_ALLOWLIST",
    "KURONODE_REMOTE_PUSH",
}

_REQUEST_KEYS = {
    "request_status",
    "approval_id",
    "run_id",
    "operator_identity",
    "operator_grant_text",
    "authority_request_hash",
    "approval_captured_at",
    "expires_at",
    "target_repo_identity",
    "target_branch",
    "target_head_sha",
    "observed_local_head",
    "observed_origin_main_head",
    "target_path",
    "allowed_modified_files",
    "allowed_new_files",
    "replay_ledger_id",
    "operator_stop_required",
    "rollback_expectation",
    "cleanup_expectation",
    "output_bound_bytes",
    "operator_note",
    "excluded_adjacent_authorities",
}

_PATCH_SCRIPT = r'''
from pathlib import Path
path = Path("scripts/smoke_test.ts")
text = path.read_text()
old = """    // Trigger path observation:\n    // We observe the IPC push instead of DOM if .joint-cell isn't ready.\n    console.log('[SMOKE] Listening for kur:projection-result...');\n    const projectionPromise = window.evaluate(() => {\n      return new Promise((resolve) => {\n        // @ts-ignore\n        const unsub = window.KuronodeAPI.onProjectionResult((result) => {\n          unsub();\n          resolve(result);\n        });\n        // Timeout guard — pipeline must respond within 30s\n        setTimeout(() => resolve({ streamId: 'timeout', _type: 'timeout' }), 30000);\n      });\n    });\n\n    // Trigger the pipeline via IntentTrigger (Preload API)\n    console.log('[SMOKE] Triggering pipeline via intentTrigger...');\n    await window.evaluate(() => {\n      // @ts-ignore\n      window.KuronodeAPI.intentTrigger({ anchors: ['Drone'], scope: 'structural' });\n    });\n\n    const result = await projectionPromise;\n    console.log('[SMOKE] Received projection result:', (result as any).streamId);\n\n    console.log('[PASS] Headless Pipeline Smoke Test Succeeded.');\n"""
new = """    // Trigger path observation:\n    // We observe the IPC push instead of DOM if .joint-cell isn't ready.\n    type ProjectionResult = { streamId: string; ast?: unknown; _type?: string };\n    type KuronodeSmokeApi = {\n      onProjectionResult: (handler: (result: unknown) => void) => () => void;\n      intentTrigger: (payload: { anchors: string[]; scope: string }) => void;\n    };\n    const isProjectionResult = (value: unknown): value is ProjectionResult => {\n      return typeof value === 'object' && value !== null && typeof (value as { streamId?: unknown }).streamId === 'string';\n    };\n    const kuronodeApi = (window as Window & { KuronodeAPI?: KuronodeSmokeApi }).KuronodeAPI;\n    if (!kuronodeApi) {\n      throw new Error('Kuronode preload API missing');\n    }\n\n    console.log('[SMOKE] Listening for kur:projection-result...');\n    const projectionPromise = window.evaluate(() => {\n      return new Promise<unknown>((resolve) => {\n        const api = (window as Window & { KuronodeAPI: KuronodeSmokeApi }).KuronodeAPI;\n        const unsub = api.onProjectionResult((result: unknown) => {\n          unsub();\n          resolve(result);\n        });\n        // Timeout guard — pipeline must respond within 30s\n        setTimeout(() => resolve({ streamId: 'timeout', _type: 'timeout' }), 30000);\n      });\n    });\n\n    // Trigger the pipeline via IntentTrigger (Preload API)\n    console.log('[SMOKE] Triggering pipeline via intentTrigger...');\n    await window.evaluate(() => {\n      const api = (window as Window & { KuronodeAPI: KuronodeSmokeApi }).KuronodeAPI;\n      api.intentTrigger({ anchors: ['Drone'], scope: 'structural' });\n    });\n\n    const result = await projectionPromise;\n    if (!isProjectionResult(result)) {\n      throw new Error('Projection result shape invalid');\n    }\n    if (result.streamId === 'timeout') {\n      throw new Error('Projection timed out before kur:projection-result');\n    }\n    if (!result.ast) {\n      throw new Error('Projection result missing ast payload');\n    }\n    console.log('[SMOKE] Received projection result:', result.streamId);\n\n    console.log('[PASS] Headless Pipeline Smoke Test Succeeded.');\n"""
if old not in text:
    raise SystemExit("expected CEB_009 smoke-test fragment not found")
path.write_text(text.replace(old, new))
print("CEB_009 smoke_test.ts patch applied")
'''.strip()

_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_PROTECTED_RE = re.compile(r"docs[\\/]+(?:active|requirements|use_cases)[\\/]+|protected[_\s-]*blk[-_\s]*req[_\s-]*body", re.IGNORECASE)
_LAUNDERING_RE = re.compile(
    r"codex|blk[-_\s]*test[_\s-]*mcp|production[_\s-]*blk[-_\s]*test|beo[_\s-]*(?:publication|published)|"
    r"authoritative[_\s-]*beo|ceo[_\s-]*009|rtm(?:id|generation|generated)?|drift[_\s-]*rejection|"
    r"coverage[_\s-]*(?:matrix|claim)|active[_\s-]*vault[_\s-]*hash|protected[_\s-]*blk[-_\s]*req[_\s-]*body|"
    r"private[_\s-]*key|api[_\s-]*key|bearer|production[_\s-]*(?:sandbox|isolation)|"
    r"run[_\s-]*(?:npm|npx|pnpm|yarn|bun)|npm[_\s-]*run[_\s-]*test:?smoke|electron[_\s-]*(?:launch|started|executed)|"
    r"smoke[_\s-]*test[_\s-]*(?:executed|passed|started)|\b(?:tsc|eslint|prettier|npm|npx|pnpm|yarn|bun|curl|wget|ssh|scp|rsync|docker|deno)\b|"
    r"remote[_\s-]*push|push[_\s-]*kuronode|publish[_\s-]*patch",
    re.IGNORECASE,
)


def default_ceb009_patch_execution_approval_capture_request(authority_request: dict[str, Any]) -> dict[str, Any]:
    """Return a default exact-head approval-capture request."""

    return {
        "request_status": REQUEST_STATUS,
        "approval_id": APPROVAL_ID,
        "run_id": RUN_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_grant_text": OPERATOR_GRANT_TEXT,
        "authority_request_hash": _required_hash(authority_request.get("authority_request_hash"), "authority_request.authority_request_hash"),
        "approval_captured_at": "2026-05-11T08:11:00+10:00",
        "expires_at": "2026-05-11T10:11:00+10:00",
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "observed_local_head": TARGET_HEAD_SHA,
        "observed_origin_main_head": TARGET_HEAD_SHA,
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "replay_ledger_id": "BLK-SYSTEM-065-CEB009-PATCH-EXECUTION-REPLAY-LEDGER-LOCAL",
        "operator_stop_required": True,
        "rollback_expectation": "BLK-pipe revert by exact pre-engine hash if execution fails after mutation",
        "cleanup_expectation": "BLK-pipe reset/clean cleanup on unauthorized mutation or validation failure",
        "output_bound_bytes": 1_048_576,
        "operator_note": "approval capture for one exact BLK-pipe patch attempt only",
        "excluded_adjacent_authorities": sorted(EXACT_EXCLUDED_ADJACENT_AUTHORITIES),
    }


def build_ceb009_patch_execution_approval_capture(*, authority_request: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Capture approval and prepare an exact BLK-pipe payload or a blocked target-drift record."""

    validated_authority = _validate_authority_request(authority_request)
    validated_request = _validate_request(request, validated_authority)
    capture = {
        "approval_capture_status": APPROVAL_CAPTURE_STATUS,
        "approval_capture_marker": APPROVAL_CAPTURE_MARKER,
        "approval_id": validated_request["approval_id"],
        "run_id": validated_request["run_id"],
        "operator_identity": validated_request["operator_identity"],
        "approval_captured_at": validated_request["approval_captured_at"],
        "expires_at": validated_request["expires_at"],
        "authority_request_hash": validated_authority["authority_request_hash"],
        "target_repo_identity": TARGET_REPO_IDENTITY,
        "target_branch": TARGET_BRANCH,
        "target_head_sha": TARGET_HEAD_SHA,
        "observed_local_head": validated_request["observed_local_head"],
        "observed_origin_main_head": validated_request["observed_origin_main_head"],
        "target_path": TARGET_PATH,
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "excluded_adjacent_authorities": sorted(EXACT_EXCLUDED_ADJACENT_AUTHORITIES),
        "approval_captured": True,
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
    if validated_request["observed_local_head"] != TARGET_HEAD_SHA or validated_request["observed_origin_main_head"] != TARGET_HEAD_SHA:
        capture["execution_readiness_status"] = BLOCKED_TARGET_DRIFT_STATUS
        capture["execution_authorized"] = False
        capture["block_reason"] = "TARGET_HEAD_DRIFT_REQUIRES_FRESH_APPROVAL"
    else:
        capture["execution_readiness_status"] = APPROVED_READY_STATUS
        capture["execution_authorized"] = True
        capture["block_reason"] = "NONE"
        capture["blk_pipe_payload"] = _build_blk_pipe_payload(validated_authority)
    capture["approval_capture_hash"] = _canonical_hash({key: value for key, value in capture.items() if key != "approval_capture_hash"})
    return capture


def build_default_ceb009_patch_execution_authority_chain() -> dict[str, Any]:
    """Build the full synthetic CEB_009 authority chain through approval capture."""

    corpus = default_ceb009_static_corpus()
    source_report = build_ceb009_static_gate_pilot_report(corpus=corpus, request=default_ceb009_static_request(corpus))
    packet = build_ceb009_remediation_packet(source_report=source_report, request=default_ceb009_remediation_request(source_report))
    envelope = build_ceb009_patch_approval_envelope(remediation_packet=packet, request=default_ceb009_patch_approval_request(packet))
    preflight = build_ceb009_patch_execution_preflight(envelope=envelope, request=default_ceb009_patch_execution_preflight_request(envelope))
    authority = build_ceb009_patch_execution_authority_request(
        preflight=preflight,
        request=default_ceb009_patch_execution_authority_request(preflight),
    )
    return build_ceb009_patch_execution_approval_capture(
        authority_request=authority,
        request=default_ceb009_patch_execution_approval_capture_request(authority),
    )


def _validate_authority_request(authority_request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(authority_request, dict):
        raise ValueError("authority_request must be a dictionary")
    supplied_hash = _required_hash(authority_request.get("authority_request_hash"), "authority_request_hash")
    recomputed_hash = _canonical_hash({key: value for key, value in authority_request.items() if key != "authority_request_hash"})
    if supplied_hash != recomputed_hash:
        raise ValueError("authority_request hash mismatch after recomputation")
    if authority_request.get("authority_request_status") != AUTHORITY_REQUEST_STATUS:
        raise ValueError("authority_request must be BLK-SYSTEM-064 ready for human decision")
    if authority_request.get("authority_request_marker") != AUTHORITY_REQUEST_MARKER:
        raise ValueError("authority_request marker mismatch")
    if authority_request.get("approval_captured") is not False or authority_request.get("execution_authorized") is not False:
        raise ValueError("upstream authority_request must not have captured approval")
    _validate_target_fields(authority_request)
    return deepcopy(authority_request)


def _validate_request(request: dict[str, Any], authority_request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("approval capture request must be a dictionary")
    _enforce_keys(request, _REQUEST_KEYS, "approval capture request")
    _reject_laundering({key: value for key, value in request.items() if key not in {"operator_grant_text", "excluded_adjacent_authorities"}}, "approval capture request")
    if request.get("request_status") != REQUEST_STATUS:
        raise ValueError("request_status must match approval capture request")
    if request.get("operator_grant_text") != OPERATOR_GRANT_TEXT:
        raise ValueError("operator_grant_text must match explicit approval grant")
    if _required_hash(request.get("authority_request_hash"), "authority_request_hash") != authority_request["authority_request_hash"]:
        raise ValueError("authority_request_hash does not match submitted authority request")
    _require_exact(request.get("target_repo_identity"), TARGET_REPO_IDENTITY, "target_repo_identity")
    _require_exact(request.get("target_branch"), TARGET_BRANCH, "target_branch")
    _require_exact(request.get("target_head_sha"), TARGET_HEAD_SHA, "target_head_sha")
    _require_exact(request.get("target_path"), TARGET_PATH, "target_path")
    if request.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must match exact CEB_009 target")
    if request.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty for CEB_009 patch execution")
    _validate_commit(request.get("observed_local_head"), "observed_local_head")
    _validate_commit(request.get("observed_origin_main_head"), "observed_origin_main_head")
    _validate_timestamps(request.get("approval_captured_at"), request.get("expires_at"))
    if request.get("operator_stop_required") is not True:
        raise ValueError("operator_stop_required must be true")
    if not isinstance(request.get("output_bound_bytes"), int) or request["output_bound_bytes"] <= 0 or request["output_bound_bytes"] > 1_048_576:
        raise ValueError("output_bound_bytes must be a positive bounded integer <= 1048576")
    _validate_exact_string_set(
        request.get("excluded_adjacent_authorities"),
        EXACT_EXCLUDED_ADJACENT_AUTHORITIES,
        "excluded_adjacent_authorities must match exact denied adjacent authority set",
    )
    return deepcopy(request)


def _validate_target_fields(value: dict[str, Any]) -> None:
    _require_exact(value.get("target_repo_identity"), TARGET_REPO_IDENTITY, "target_repo_identity")
    _require_exact(value.get("target_branch"), TARGET_BRANCH, "target_branch")
    _require_exact(value.get("target_head_sha"), TARGET_HEAD_SHA, "target_head_sha")
    _require_exact(value.get("target_path"), TARGET_PATH, "target_path")
    if value.get("allowed_modified_files") != [TARGET_PATH]:
        raise ValueError("allowed_modified_files must match exact CEB_009 target")
    if value.get("allowed_new_files") != []:
        raise ValueError("allowed_new_files must be empty")


def _build_blk_pipe_payload(authority_request: dict[str, Any]) -> dict[str, Any]:
    return {
        "action": "execute",
        "beb_id": "CEB_009",
        "work_dir": WORK_DIR,
        "target_branch": TARGET_BRANCH,
        "engine": "python3",
        "engine_args": ["-c", _PATCH_SCRIPT],
        "l2_packet": "BLK-SYSTEM-065 exact CEB_009 patch: edit only scripts/smoke_test.ts per remediation packet; no Codex, no Electron, no smoke runtime, no TypeScript/package-manager tooling.",
        "trace_artifacts": [
            {
                "kind": "CEB",
                "id": "CEB_009",
                "version_hash": authority_request["authority_request_hash"],
            }
        ],
        "validation_commands": ["git diff --check -- scripts/smoke_test.ts"],
        "allowed_modified_files": [TARGET_PATH],
        "allowed_new_files": [],
        "timeout_seconds": 60,
        "max_output_bytes": 1_048_576,
    }


def _validate_timestamps(approval_value: Any, expires_value: Any) -> None:
    approval = _parse_timestamp(approval_value, "approval_captured_at")
    expires = _parse_timestamp(expires_value, "expires_at")
    if expires <= approval:
        raise ValueError("expires_at must be later than approval_captured_at")


def _parse_timestamp(value: Any, field: str) -> datetime:
    text = _required_string(value, field)
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed


def _validate_commit(value: Any, field: str) -> None:
    text = _required_string(value, field)
    if not _COMMIT_RE.match(text):
        raise ValueError(f"{field} must be a 40-character lowercase git SHA")


def _validate_exact_string_set(value: Any, expected: set[str], message: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value) or set(value) != expected or len(value) != len(expected):
        raise ValueError(message)


def _enforce_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(f"{label} contains unexpected field(s): {extra}")


def _require_exact(value: Any, expected: str, field: str) -> None:
    actual = _required_string(value, field)
    if _PROTECTED_RE.search(_decode_path_text(actual)):
        raise ValueError(f"{field} rejects protected BLK-req body reference")
    if actual != expected:
        raise ValueError(f"{field} must match exact CEB_009 target")


def _reject_laundering(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_laundering(key, label)
            _reject_laundering(item, label)
    elif isinstance(value, list):
        for item in value:
            _reject_laundering(item, label)
    elif isinstance(value, str):
        decoded = _decode_path_text(value)
        normalized = _normalize_text(value)
        if _PROTECTED_RE.search(decoded):
            raise ValueError(f"{label} rejects protected BLK-req body reference")
        if _HASH_RE.match(value):
            return
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
