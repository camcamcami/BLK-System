"""BLK-SYSTEM-103 exact local RTM trace-closure execution record.

This fixture consumes the exact BLK-SYSTEM-102 future run ID and emits one
repository-local RTM trace-closure record. The result is non-authoritative local
evidence only: no protected-body reads, no active-vault hash comparison, no RTM
generation, no drift rejection, no public ledger mutation, no target/source/Git
mutation, no tooling/runtime expansion, and no production blk-link authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_trace_closure_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    CANONICAL_BLK101_REQUEST_PACKAGE_HASH,
    DECISION_RESULT as BLK102_DECISION_RESULT,
    EXACT_EXCLUDED_AUTHORITIES as BLK102_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK102_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID as BLK102_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK102_NEXT_REQUIRED_AUTHORITY,
    SIDE_EFFECT_FLAGS as BLK102_SIDE_EFFECT_FLAGS,
    STATUS as BLK102_STATUS,
    _enforce_exact_keys,
    _parse_timestamp,
    _require_dict,
    _scan_value_strings,
    _validate_exact_set,
)

EXECUTION_STATUS = "LOCAL_RTM_TRACE_CLOSURE_EXECUTED_FOR_EXACT_BLK102_APPROVAL"
EXECUTION_PACKAGE_ID = "RTM-TRACE-CLOSURE-EXECUTION-103-001"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001"
TRACE_CLOSURE_ID = "RTM-TRACE-CLOSURE-103-001"
SELECTED_FRONTIER = "exact_local_rtm_trace_closure_execution"
EXECUTION_SCOPE = "EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_RECORD_ONLY"
CANONICAL_BLK102_APPROVAL_DECISION_PACKAGE_HASH = "sha256:9211e14961b8c0f380812372d2b2a1ae091daf17709af375985f94015af0fecb"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T21:10:00+10:00")

SIDE_EFFECT_FLAGS = (
    "rtm_generated",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "protected_body_reads",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "REUSABLE_OR_PRODUCTION_BLK_LINK_AUTHORITY",
    "RUNTIME_RTM_GENERATION_BEYOND_LOCAL_TRACE_RECORD",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ",
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
    "BLK102_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
    "APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW",
    "RUN_ID_CONSUMED_EXACTLY_ONCE_IN_LOCAL_FIXTURE",
    "BLK100_PUBLICATION_RECORD_HASH_BOUND",
    "LOCAL_TRACE_CLOSURE_RECORD_HASH_BOUND",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "NO_REUSABLE_PRODUCTION_BLK_LINK_AUTHORITY_CLAIMED",
}

_APPROVAL_KEYS = {
    "approval_decision_status",
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "publication_record_hash",
    "beo_id",
    "beo_hash",
    "approval_id",
    "future_run_id",
    "decision_result",
    "decided_at",
    "expires_at",
    "approval_decision_captured",
    "human_rtm_trace_closure_approval_granted",
    "future_local_rtm_trace_closure_execution_approved",
    "future_run_id_consumed",
    "next_required_authority",
    "operator_approval_text_raw",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "approval_decision_package_hash",
    *BLK102_SIDE_EFFECT_FLAGS,
}

_REQUEST_KEYS = {
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id_to_consume",
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
    "exact_blk102_approval_reviewed",
    "run_id_consumed_once_for_local_trace_closure",
    "local_trace_closure_record_only_not_production_blk_link",
    "rtm_generation_not_performed",
    "drift_rejection_excluded",
    "active_vault_hash_comparison_excluded",
    "protected_body_reads_excluded",
    "public_ledger_mutation_excluded",
    "target_source_git_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}


def build_exact_local_rtm_trace_closure_execution(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    trace_record_body = {
        "trace_closure_id": TRACE_CLOSURE_ID,
        "trace_closure_status": "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "hash_binding_mode": "LOCAL_HASH_ONLY_NO_ACTIVE_VAULT_COMPARISON_NO_PROTECTED_BODY_READS",
        "trace_links": [
            {"kind": "BEO", "id": approval["beo_id"], "version_hash": approval["beo_hash"]},
            {
                "kind": "PUBLICATION_RECORD",
                "id": "BLK-SYSTEM-100_EXTERNAL_BEO_PUBLICATION_RECORD",
                "version_hash": approval["publication_record_hash"],
            },
        ],
        "active_vault_hash_comparison_performed": False,
        "protected_body_reads": False,
        "rtm_generated": False,
        "drift_decision_made": False,
        "rtm_drift_rejection_performed": False,
        "public_ledger_mutation": False,
    }
    trace_closure_record = {**trace_record_body, "trace_closure_record_hash": _canonical_hash(trace_record_body)}
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
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "trace_closure_id": TRACE_CLOSURE_ID,
        "trace_closure_record": trace_closure_record,
        "trace_closure_record_hash": trace_closure_record["trace_closure_record_hash"],
        "local_rtm_trace_closure_record_emitted": True,
        "rtm_trace_closure_status": "PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE",
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
    _enforce_exact_keys(package, _APPROVAL_KEYS, "approval_package")
    submitted_hash = package.get("approval_decision_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("approval_decision_package_hash does not match submitted BLK-102 package")
    expected = {
        "approval_decision_status": BLK102_STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "upstream_authority_request_package_hash": CANONICAL_BLK101_REQUEST_PACKAGE_HASH,
        "approval_id": APPROVAL_ID,
        "future_run_id": BLK102_FUTURE_RUN_ID,
        "decision_result": BLK102_DECISION_RESULT,
        "next_required_authority": BLK102_NEXT_REQUIRED_AUTHORITY,
        "approval_decision_package_hash": CANONICAL_BLK102_APPROVAL_DECISION_PACKAGE_HASH,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("approval package must match canonical BLK-102 approval decision")
    if package.get("approval_decision_captured") is not True:
        raise ValueError("approval decision must be captured")
    if package.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-102 approval must reserve but not consume future run id")
    for flag in BLK102_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"approval package {flag} must remain false")
    _validate_exact_set(package.get("proof_obligations"), BLK102_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK102_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    return package


def _validate_execution_request(request: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_exact_keys(request, _REQUEST_KEYS, "execution_request")
    for string_key in (
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_decision_package_id",
        "approval_decision_package_hash",
        "approval_id",
        "run_id_to_consume",
    ):
        _scan_value_strings(request.get(string_key), f"execution_request.{string_key}")
    expected = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": approval["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_decision_package_hash": approval["approval_decision_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_to_consume": approval["future_run_id"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must match exact BLK-102 approval package")
    for flag in SIDE_EFFECT_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    decided_at = _parse_timestamp(approval.get("decided_at"), "approval.decided_at")
    approval_expires = _parse_timestamp(approval.get("expires_at"), "approval.expires_at")
    if requested_at < decided_at:
        raise ValueError("execution request must not predate approval decision")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at >= approval_expires or expires_at > approval_expires:
        raise ValueError("execution request window must end within BLK-102 approval expiry")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_attestation(attestation: Any) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    _scan_value_strings(attestation, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
