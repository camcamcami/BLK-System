"""Exact local RTM drift-rejection execution bound to BLK-093 approval.

This fixture consumes one exact future-run ID from the BLK-SYSTEM-093 approval
package and records deterministic local RTM drift-rejection evidence. It remains
local-only and non-authoritative: no runtime blk-link trace closure, no
authoritative drift decision, no active-vault hash comparison, no protected-body
reads or hashing, no external ledger mutation, no target/source/Git mutation,
and no BLK-test/Codex/BLK-pipe runtime.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_authority_request_after_beo_pilot import (
    _enforce_exact_keys,
    _parse_timestamp,
    _required_false,
    _required_hash,
    _require_dict,
    _validate_exact_set,
)
from rtm_drift_rejection_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID as BLK093_APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID as BLK093_APPROVAL_ID,
    DECISION_RESULT as BLK093_DECISION_RESULT,
    DECISION_SCOPE as BLK093_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as BLK093_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK093_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID as BLK093_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK093_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK093_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK093_SIDE_EFFECT_FLAGS,
    STATUS as BLK093_STATUS,
)
from rtm_generation_approval_decision import _scan_string as _generation_scan_string

EXECUTION_STATUS = "LOCAL_RTM_DRIFT_REJECTION_EXECUTED_FOR_EXACT_BLK093_APPROVAL"
EXECUTION_PACKAGE_ID = "RTM-DRIFT-REJECTION-EXECUTION-095-001"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001"
DRIFT_REJECTION_ID = "LOCAL-RTM-DRIFT-REJECTION-095-001"
SELECTED_FRONTIER = "exact_local_rtm_drift_rejection_execution"
EXECUTION_SCOPE = "EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_LOCAL_ONLY"
DRIFT_REJECTION_RESULT = "PILOT_LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE"
NEXT_REQUIRED_AUTHORITY = "POST_LOCAL_RTM_DRIFT_REJECTION_RECONCILIATION_REQUIRED_NOT_RUNTIME_BLK_LINK"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T00:00:00+10:00")
CANONICAL_BLK093_APPROVAL_PACKAGE_HASH = "sha256:981c8bddea6f84c339346bf00aeeef8c52f63458bf3899ca776734403a88b166"

SIDE_EFFECT_FLAGS = (
    "authoritative_drift_decision_made",
    "runtime_blk_link_trace_closure",
    "active_vault_hash_comparison_performed",
    "protected_body_reads",
    "protected_body_hashing",
    "authoritative_external_publication",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_test_codex_blk_pipe_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "REUSABLE_RUNTIME_RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "RUNTIME_BLK_LINK_TRACE_CLOSURE",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "PROTECTED_BLK_REQ_BODY_READ",
    "PROTECTED_BODY_HASHING",
    "AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "TARGET_REPO_SCAN",
    "TARGET_REPO_MUTATION",
    "SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK093_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
    "APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW",
    "RUN_ID_CONSUMED_EXACTLY_ONCE_IN_LOCAL_FIXTURE",
    "LOCAL_RTM_LEDGER_INPUT_HASH_BOUND",
    "LOCAL_RTM_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE",
    "AUTHORITATIVE_DRIFT_DECISION_NOT_MADE",
    "RUNTIME_BLK_LINK_TRACE_CLOSURE_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "POST_LOCAL_EXECUTION_RECONCILIATION_REQUIRED",
}

_APPROVAL_REQUIRED_KEYS = {
    "approval_decision_status",
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "decision_result",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "upstream_rtm_generation_package_id",
    "upstream_rtm_generation_package_hash",
    "rtm_id",
    "rtm_ledger_hash",
    "local_rtm_ledger",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "approval_id",
    "future_run_id",
    "decided_at",
    "expires_at",
    "approval_decision_captured",
    "human_rtm_drift_rejection_approval_granted",
    "future_local_rtm_drift_rejection_execution_approved",
    "future_run_id_consumed",
    "drift_rejection_status",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "approval_decision_package_hash",
    *BLK093_SIDE_EFFECT_FLAGS,
}

_EXECUTION_REQUEST_KEYS = {
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id_to_consume",
    "rtm_id",
    "requested_at",
    "expires_at",
    "expired",
    "replayed",
    "stale",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    *SIDE_EFFECT_FLAGS,
}

_ATTESTATION_KEYS = {
    "exact_blk093_approval_reviewed",
    "run_id_consumed_once_for_local_drift_rejection",
    "local_drift_rejection_only_not_runtime_blk_link",
    "authoritative_drift_decision_excluded",
    "protected_body_reads_excluded",
    "active_vault_comparison_excluded",
    "external_ledger_and_signer_storage_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_BLK093_ATTESTATION_KEYS = {
    "approval_limited_to_one_future_local_drift_rejection_execution",
    "drift_rejection_not_executed_by_this_decision",
    "exact_blk091_request_reviewed",
    "external_ledger_and_signer_storage_side_effects_excluded",
    "no_adjacent_runtime_side_effects",
    "no_drift_decision_made_by_this_decision",
    "protected_body_reads_excluded",
    "target_repo_scan_or_mutation_excluded",
}

_CANONICAL_BLK093_FIELDS = {
    "operator_identity": "discord:684235178083745819",
    "upstream_authority_request_package_id": "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001",
    "upstream_authority_request_package_hash": "sha256:88e1065154ede742ca16178bd1f0fb17f3aba5bca0f145fa47317866038b933b",
    "upstream_rtm_generation_package_id": "RTM-GENERATION-PILOT-EXECUTION-090-001",
    "upstream_rtm_generation_package_hash": "sha256:63153da083ff9b0b0783798e858162184ddfa59bd31524c7d024423c6e2e3d14",
    "rtm_id": "RTM-090-001",
    "beo_id": "BEO-054-001",
    "beo_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "target_id": "BEO-PUBLICATION-TARGET-055-001",
    "target_ref": "fixture://beo-publication-targets/055/001",
}

_TRACE_ARTIFACT_KEYS = {"kind", "id", "version_hash"}
_ALLOWED_TRACE_KINDS = {"REQ"}

_BLK095_FORBIDDEN_NORMALIZED_MARKERS = (
    "runtimeblklinktraceclosure",
    "blklinktraceclosure",
    "traceclosure",
    "authoritativedriftdecision",
    "authoritativedriftdecisionmade",
    "reusablertmdriftrejection",
    "runtimertmdriftrejection",
    "protectedbodyread",
    "protectedbodyhashing",
    "activevaulthashcomparison",
    "externalledgermutation",
    "publicledgermutation",
    "targetreposcan",
    "targetrepomutation",
    "sourcemutation",
    "gitmutation",
    "bebdispatch",
    "beocloseout",
    "blkpipe",
    "blktest",
    "codexruntime",
    "packagemanager",
    "networktooling",
    "modelservice",
    "browsertooling",
    "cybertooling",
    "productionisolation",
    "sandboxclaim",
)

_LEDGER_KEYS = {
    "rtm_id",
    "rtm_status",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "pilot_publication_artifact_hash",
    "trace_artifacts",
    "hash_binding_mode",
    "drift_review_state",
    "external_ledger_state",
    "protected_body_reads",
    "drift_rejection_authorized",
    "drift_decision_made",
    "rtm_ledger_hash",
}


def build_exact_local_rtm_drift_rejection_execution(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    local_ledger = deepcopy(approval["local_rtm_ledger"])
    trace_artifacts = deepcopy(local_ledger["trace_artifacts"])
    record_body = {
        "drift_rejection_id": DRIFT_REJECTION_ID,
        "drift_rejection_result": DRIFT_REJECTION_RESULT,
        "rtm_id": approval["rtm_id"],
        "rtm_ledger_hash": approval["rtm_ledger_hash"],
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "trace_artifacts": trace_artifacts,
        "input_drift_review_state": local_ledger["drift_review_state"],
        "output_drift_review_state": "LOCAL_DRIFT_REJECTION_RECORDED_NOT_AUTHORITATIVE",
        "hash_binding_mode": "LOCAL_HASH_ONLY_NO_PROTECTED_BODY_READS",
        "authoritative_drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
        "protected_body_reads": False,
        "protected_body_hashing": False,
        "external_ledger_state": "NOT_APPENDED_LOCAL_FIXTURE_ONLY",
    }
    record_hash = _canonical_hash(record_body)
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_decision_package_hash": approval["approval_decision_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_rtm_generation_package_id": approval["upstream_rtm_generation_package_id"],
        "upstream_rtm_generation_package_hash": approval["upstream_rtm_generation_package_hash"],
        "rtm_id": approval["rtm_id"],
        "rtm_ledger_hash": approval["rtm_ledger_hash"],
        "local_rtm_ledger": local_ledger,
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "local_rtm_drift_rejection_executed": True,
        "drift_rejection_result": DRIFT_REJECTION_RESULT,
        "local_drift_rejection_record": record_body,
        "local_drift_rejection_record_hash": record_hash,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


def _validate_approval_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "approval_package")
    _enforce_exact_keys(package, _APPROVAL_REQUIRED_KEYS, "approval_package")
    package_hash = _required_hash(package.get("approval_decision_package_hash"), "approval_decision_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("approval_decision_package_hash does not match submitted BLK-093 package")
    if package.get("approval_decision_status") != BLK093_STATUS:
        raise ValueError("approval package must be BLK-093 drift-rejection approval decision")
    for key, expected in _CANONICAL_BLK093_FIELDS.items():
        if package.get(key) != expected:
            raise ValueError(f"approval package must match canonical BLK-093 field {key}")
    if package.get("approval_decision_package_id") != BLK093_APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError("approval_decision_package_id must match BLK-093")
    if package.get("decision_scope") != BLK093_DECISION_SCOPE:
        raise ValueError("approval package must remain decision-only")
    if package.get("selected_frontier") != BLK093_SELECTED_FRONTIER:
        raise ValueError("approval package selected_frontier must be BLK-093 approval capture")
    if package.get("approval_id") != BLK093_APPROVAL_ID or package.get("future_run_id") != BLK093_FUTURE_RUN_ID:
        raise ValueError("approval package must carry exact BLK-093 approval/run IDs")
    if package.get("decision_result") != BLK093_DECISION_RESULT:
        raise ValueError("approval package must approve one future local RTM drift-rejection execution")
    if package.get("approval_decision_captured") is not True:
        raise ValueError("BLK-093 approval decision must be captured")
    if package.get("human_rtm_drift_rejection_approval_granted") is not True:
        raise ValueError("BLK-093 approval must grant future local drift-rejection execution")
    if package.get("future_local_rtm_drift_rejection_execution_approved") is not True:
        raise ValueError("BLK-093 approval must be limited to future local drift-rejection execution")
    if package.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-093 approval future run ID must not be consumed yet")
    if package.get("drift_rejection_status") != "APPROVAL_DECISION_CAPTURED_NOT_EXECUTED":
        raise ValueError("BLK-093 approval decision must not already execute drift rejection")
    if package.get("next_required_authority") != BLK093_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-093 package must require exact local drift-rejection execution")
    _validate_approval_attestation(package.get("operator_attestation"))
    decided_at = _parse_timestamp(package.get("decided_at"), "approval.decided_at")
    expires_at = _parse_timestamp(package.get("expires_at"), "approval.expires_at")
    if expires_at <= decided_at:
        raise ValueError("approval expires_at must be after approval decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    ledger = _require_dict(package.get("local_rtm_ledger"), "local_rtm_ledger")
    _validate_local_rtm_ledger(ledger, package)
    ledger_hash = _required_hash(package.get("rtm_ledger_hash"), "rtm_ledger_hash")
    expected_ledger_hash = _canonical_hash({key: value for key, value in ledger.items() if key != "rtm_ledger_hash"})
    if ledger.get("rtm_ledger_hash") != ledger_hash or ledger_hash != expected_ledger_hash:
        raise ValueError("rtm_ledger_hash does not match submitted local RTM ledger")
    for flag in BLK093_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), BLK093_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK093_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    if package_hash != CANONICAL_BLK093_APPROVAL_PACKAGE_HASH:
        raise ValueError("approval package must match canonical BLK-093 approval package hash")
    return package


def _validate_local_rtm_ledger(ledger: dict[str, Any], package: dict[str, Any]) -> None:
    _enforce_exact_keys(ledger, _LEDGER_KEYS, "local_rtm_ledger")
    expected = {
        "rtm_id": package["rtm_id"],
        "rtm_status": "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE",
        "beo_id": package["beo_id"],
        "beo_hash": package["beo_hash"],
        "target_id": package["target_id"],
        "target_ref": package["target_ref"],
        "hash_binding_mode": "LOCAL_HASH_ONLY_NO_PROTECTED_BODY_READS",
        "drift_review_state": "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
        "external_ledger_state": "NOT_APPENDED_LOCAL_FIXTURE_ONLY",
        "protected_body_reads": False,
        "drift_rejection_authorized": False,
        "drift_decision_made": False,
    }
    for key, value in expected.items():
        if ledger.get(key) != value:
            raise ValueError("local_rtm_ledger must remain pending local drift-review evidence")
    _required_hash(ledger.get("pilot_publication_artifact_hash"), "pilot_publication_artifact_hash")
    _validate_trace_artifacts(ledger.get("trace_artifacts"))


def _validate_trace_artifacts(trace_artifacts: Any) -> None:
    if not isinstance(trace_artifacts, list) or not trace_artifacts:
        raise ValueError("trace_artifacts must be a list")
    for index, artifact in enumerate(trace_artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be a dict")
        _enforce_exact_keys(artifact, _TRACE_ARTIFACT_KEYS, f"trace_artifacts[{index}]")
        kind = artifact.get("kind")
        if kind not in _ALLOWED_TRACE_KINDS:
            raise ValueError(f"trace_artifacts[{index}].kind must be an allowed trace kind")
        _scan_string(kind, f"trace_artifacts[{index}].kind")
        _scan_string(artifact.get("id"), f"trace_artifacts[{index}].id")
        _required_hash(artifact.get("version_hash"), f"trace_artifacts[{index}].version_hash")


def _validate_approval_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "approval_package.operator_attestation")
    _enforce_exact_keys(attestation, _BLK093_ATTESTATION_KEYS, "approval_package.operator_attestation")
    for key in _BLK093_ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"approval_package.operator_attestation.{key} must be true")


def _validate_execution_request(request: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_exact_keys(request, _EXECUTION_REQUEST_KEYS, "execution_request")
    if request.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if request.get("operator_identity") != approval["operator_identity"]:
        _scan_string(str(request.get("operator_identity")), "operator_identity")
        raise ValueError("operator_identity must match BLK-093 approval package")
    _scan_string(request["operator_identity"], "operator_identity")
    if request.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if request.get("approval_decision_package_id") != approval["approval_decision_package_id"]:
        raise ValueError("approval_decision_package_id must match BLK-093 approval package")
    if request.get("approval_decision_package_hash") != approval["approval_decision_package_hash"]:
        raise ValueError("approval_decision_package_hash must match BLK-093 approval package")
    if request.get("approval_id") != approval["approval_id"]:
        raise ValueError("approval_id must match BLK-093 approval package")
    if request.get("run_id_to_consume") != approval["future_run_id"] or request.get("run_id_to_consume") != RUN_ID_CONSUMED:
        raise ValueError("run_id_to_consume must match approved BLK-093 future run ID")
    if request.get("rtm_id") != approval["rtm_id"]:
        raise ValueError("rtm_id must match BLK-093 approval package")
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    decided_at = _parse_timestamp(approval["decided_at"], "approval.decided_at")
    approval_expires_at = _parse_timestamp(approval["expires_at"], "approval.expires_at")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if requested_at < decided_at:
        raise ValueError("requested_at must not precede approval decision")
    if requested_at >= approval_expires_at:
        raise ValueError("requested_at must be before approval expiry")
    if expires_at > approval_expires_at:
        raise ValueError("execution window must not exceed approval expiry")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(request.get(flag), flag)
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _scan_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    _generation_scan_string(value, label)
    normalized = _normalize_for_laundering(value)
    if any(marker in normalized for marker in _BLK095_FORBIDDEN_NORMALIZED_MARKERS):
        raise ValueError(f"{label} contains authority-laundering text")


def _normalize_for_laundering(value: str) -> str:
    decoded = str(value)
    for _ in range(5):
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    return re.sub(r"[^a-z0-9]", "", decoded.casefold())
