"""BLK-SYSTEM-102 RTM trace-closure approval-decision capture.

This fixture captures approval for exactly one future local RTM trace-closure
execution bound to BLK-SYSTEM-101. It reserves a future run ID but does not
consume it and does not execute trace closure, generate RTM, reject drift,
compare active-vault hashes, read protected bodies, mutate target/source/Git, or
run BLK-pipe/BLK-test/Codex/tooling.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_trace_closure_authority_request_after_external_beo import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK101_REQUEST_PACKAGE_ID,
    CANONICAL_BLK100_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK100_PUBLICATION_RECORD_HASH,
    EXACT_EXCLUDED_AUTHORITIES as BLK101_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK101_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK101_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK101_REQUEST_SCOPE,
    REQUEST_STATUS as BLK101_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK101_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK101_SIDE_EFFECT_FLAGS,
    _enforce_exact_keys,
    _parse_timestamp,
    _require_dict,
    _scan_value_strings,
    _validate_exact_set,
)

STATUS = "RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK101_REQUEST_NOT_EXECUTED"
APPROVAL_DECISION_PACKAGE_ID = "RTM-TRACE-CLOSURE-APPROVAL-DECISION-102-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-101-RTM-TRACE-CLOSURE-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-103-RTM-TRACE-CLOSURE-001"
SELECTED_FRONTIER = "rtm_trace_closure_approval_decision_capture"
DECISION_SCOPE = "RTM_TRACE_CLOSURE_APPROVAL_DECISION_ONLY_NOT_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_LOCAL_RTM_TRACE_CLOSURE_EXECUTION_REQUIRED_NOT_RUN"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T21:00:00+10:00")
CANONICAL_BLK101_REQUEST_PACKAGE_HASH = "sha256:b050261c1c1938423795f56427571d49dcf1d028c5811b5e3985b644cfadbcde"

SIDE_EFFECT_FLAGS = (
    "rtm_trace_closure_executed",
    "rtm_generated",
    "rtm_drift_rejection_authorized",
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
    "RUNTIME_RTM_TRACE_CLOSURE_EXECUTION_THIS_SPRINT",
    "RUNTIME_RTM_GENERATION_THIS_SPRINT",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
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
    "BLK101_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "HUMAN_RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK101_TRACE_CLOSURE",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "TRACE_CLOSURE_NOT_EXECUTED_BY_APPROVAL_DECISION",
    "RTM_GENERATION_NOT_PERFORMED_BY_APPROVAL_DECISION",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_TRACE_CLOSURE_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = {
    "request_status",
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "publication_record_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path_metadata_only",
    "target_head_sha_metadata_only",
    "requested_authority",
    "request_future_exact_rtm_trace_closure_authority",
    "rtm_trace_closure_authority",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "authority_request_package_hash",
    *BLK101_SIDE_EFFECT_FLAGS,
}

_DECISION_KEYS = {
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "approval_id",
    "future_run_id",
    "decision_result",
    "decided_at",
    "expires_at",
    "expired",
    "replayed",
    "stale",
    "operator_approval_text_raw",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    *SIDE_EFFECT_FLAGS,
}

_ATTESTATION_KEYS = {
    "exact_blk101_request_reviewed",
    "approval_limited_to_one_future_local_trace_closure_execution",
    "future_run_id_reserved_not_consumed",
    "trace_closure_not_executed_by_this_decision",
    "rtm_generation_not_performed_by_this_decision",
    "drift_rejection_excluded",
    "active_vault_hash_comparison_excluded",
    "protected_body_reads_excluded",
    "target_source_git_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}


def build_rtm_trace_closure_approval_decision(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    package = {
        "approval_decision_status": STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "publication_record_hash": request["publication_record_hash"],
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_rtm_trace_closure_approval_granted": True,
        "future_local_rtm_trace_closure_execution_approved": True,
        "future_run_id_consumed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_approval_text_raw": decision["operator_approval_text_raw"],
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_decision_package_hash"}
    )
    return package


def _validate_request_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "request_package")
    _enforce_exact_keys(package, _REQUEST_PACKAGE_KEYS, "request_package")
    submitted_hash = package.get("authority_request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-101 package")
    expected = {
        "request_status": BLK101_REQUEST_STATUS,
        "authority_request_package_id": BLK101_REQUEST_PACKAGE_ID,
        "request_scope": BLK101_REQUEST_SCOPE,
        "selected_frontier": BLK101_SELECTED_FRONTIER,
        "upstream_execution_package_hash": CANONICAL_BLK100_EXECUTION_PACKAGE_HASH,
        "publication_record_hash": CANONICAL_BLK100_PUBLICATION_RECORD_HASH,
        "requested_authority": "ONE_FUTURE_LOCAL_RTM_TRACE_CLOSURE_EXECUTION",
        "rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": BLK101_NEXT_REQUIRED_AUTHORITY,
        "authority_request_package_hash": CANONICAL_BLK101_REQUEST_PACKAGE_HASH,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("request package must match canonical BLK-101 authority request")
    if package.get("request_future_exact_rtm_trace_closure_authority") is not True:
        raise ValueError("BLK-101 request must request future trace-closure authority")
    for flag in BLK101_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"request package {flag} must remain false")
    _validate_exact_set(package.get("proof_obligations"), BLK101_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK101_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    return package


def _validate_decision(decision: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(decision, "approval_decision")
    _enforce_exact_keys(decision, _DECISION_KEYS, "approval_decision")
    for string_key in (
        "approval_decision_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "approval_id",
        "future_run_id",
        "decision_result",
    ):
        _scan_value_strings(decision.get(string_key), f"approval_decision.{string_key}")
    expected = {
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
    }
    for key, value in expected.items():
        if decision.get(key) != value:
            raise ValueError(f"{key} must match exact BLK-101 trace-closure approval decision")
    for flag in SIDE_EFFECT_FLAGS:
        if decision.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if decision.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(decision.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(decision.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    request_expiry = datetime.fromisoformat("2026-12-31T23:59:59+10:00")
    if expires_at > request_expiry:
        raise ValueError("decision window must end within BLK-101 request expiry")
    _validate_attestation(decision.get("operator_attestation"))
    _validate_exact_set(decision.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(decision.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return decision


def _validate_attestation(attestation: Any) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    _scan_value_strings(attestation, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
