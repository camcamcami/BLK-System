"""BLK-SYSTEM-139 active-vault hash-comparison approval capture.

This deterministic fixture captures exact operator approval for the BLK-SYSTEM-138
metadata/hash-only active-vault comparison request. It reserves one future run ID
for BLK-SYSTEM-140 but does not consume the run, perform comparison, read/hash
protected bodies, generate RTM, reject drift, mutate source/Git state, run
tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK138_AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES as BLK138_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK138_PROOF_OBLIGATIONS,
    REQUEST_STATUS as BLK138_REQUEST_STATUS,
    SIDE_EFFECT_FLAGS as BLK138_SIDE_EFFECT_FLAGS,
)
from active_vault_hash_comparison_decision_package import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

STATUS = "ACTIVE_VAULT_HASH_COMPARISON_APPROVAL_CAPTURED_FOR_EXACT_BLK138_REQUEST_NOT_EXECUTED"
APPROVAL_CAPTURE_PACKAGE_ID = "ACTIVE-VAULT-HASH-COMPARISON-APPROVAL-CAPTURE-139-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-138-ACTIVE-VAULT-HASH-COMPARISON-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001"
DECISION_SCOPE = "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_APPROVAL_CAPTURE_ONLY_NOT_EXECUTION"
SELECTED_FRONTIER = "active_vault_hash_comparison_metadata_hash_only_approval_capture"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_REQUIRED_NOT_RUN"
EXACT_OPERATOR_APPROVAL_TEXT = (
    "APPROVE ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-138-001 "
    "FOR ONE FUTURE METADATA-HASH-ONLY ACTIVE-VAULT COMPARISON RUN "
    "RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001; "
    "NO PROTECTED BODY READS; NO RTM GENERATION; NO DRIFT REJECTION; NO MUTATION."
)

SIDE_EFFECT_FLAGS = (
    "active_vault_hash_comparison_performed",
    "active_vault_metadata_read_performed",
    "future_run_id_consumed",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_executed",
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
    "ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_THIS_SPRINT",
    "ACTIVE_VAULT_METADATA_READ_THIS_SPRINT",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
    "FUTURE_RUN_ID_CONSUMPTION_THIS_SPRINT",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION",
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
    "BEO_PUBLICATION_OR_SIGNING",
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK138_AUTHORITY_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK137_DECISION_PACKAGE_BOUND_THROUGH_BLK138",
    "HUMAN_APPROVAL_CAPTURED_FOR_EXACT_METADATA_HASH_ONLY_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK138_REQUEST",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "COMPARISON_NOT_PERFORMED_BY_APPROVAL_CAPTURE",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_APPROVAL_CAPTURE",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_EXACT_COMPARISON_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "requested_authority",
        "upstream_decision_package_id",
        "upstream_decision_package_hash",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "request_future_exact_metadata_hash_only_active_vault_comparison_approval",
        "approval_capture_performed",
        "active_vault_hash_comparison_performed",
        "next_required_authority",
        "authority_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "authority_request_package_hash",
    }
)

_DECISION_KEYS = frozenset(
    {
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_decision_package_id",
        "upstream_decision_package_hash",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
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
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk138_request_reviewed",
        "approval_limited_to_one_future_metadata_hash_only_comparison",
        "future_run_id_reserved_not_consumed",
        "comparison_not_executed_by_this_decision",
        "protected_body_reads_excluded",
        "rtm_generation_excluded",
        "drift_rejection_excluded",
        "coverage_truth_excluded",
        "reusable_blk_link_excluded",
        "signer_storage_ledger_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)


def build_active_vault_hash_comparison_approval_capture(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    request = _validate_request_package(request_package)
    decision = _validate_approval_decision(approval_decision, request)
    trace_identities = list(request["exact_trace_identities"])
    package = {
        "approval_capture_status": STATUS,
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_decision_package_id": request["upstream_decision_package_id"],
        "upstream_decision_package_hash": request["upstream_decision_package_hash"],
        "upstream_reconciliation_package_id": request["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": request["upstream_reconciliation_package_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "exact_trace_identities": trace_identities,
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "future_metadata_hash_only_active_vault_comparison_approved": True,
        "future_run_id_consumed": False,
        "active_vault_hash_comparison_performed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "approval_decision_hash": _canonical_hash(decision),
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["future_metadata_hash_only_active_vault_comparison_approved"] = True
    package["approval_capture_package_hash"] = _canonical_hash(package)
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request package must be a dictionary")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"request package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    actual_hash = _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("authority_request_package_hash does not match submitted BLK-138 package")
    if package.get("authority_request_package_id") != BLK138_AUTHORITY_REQUEST_PACKAGE_ID:
        raise ValueError("authority_request_package_id must match exact BLK-138 package")
    if package.get("request_status") != BLK138_REQUEST_STATUS:
        raise ValueError("request_status must match BLK-138 request status")
    _required_exact_set(package.get("proof_obligations"), BLK138_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK138_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK138_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_approval_decision(decision: Any, request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise ValueError("approval decision must be a dictionary")
    unknown = sorted(set(decision) - _DECISION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_DECISION_KEYS - set(decision))
    if missing:
        raise ValueError(f"approval decision missing fields: {missing}")
    if decision.get("operator_approval_text_raw") != EXACT_OPERATOR_APPROVAL_TEXT:
        raise ValueError("operator approval text must match exact approval string")
    scan_copy = {
        k: v
        for k, v in decision.items()
        if k not in {"operator_approval_text_raw", "operator_attestation", "proof_obligations", "excluded_authorities"}
    }
    _scan_value_strings(scan_copy, "approval_decision", allow_selected=True)
    expected = {
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_decision_package_id": request["upstream_decision_package_id"],
        "upstream_decision_package_hash": request["upstream_decision_package_hash"],
        "upstream_reconciliation_package_id": request["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": request["upstream_reconciliation_package_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
    }
    for key, value in expected.items():
        if decision.get(key) != value:
            raise ValueError(f"{key} must be {value!r}")
    if decision.get("operator_identity") != request.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-138 request package")
    if decision.get("exact_trace_identities") != request.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-138 request package")
    _validate_exact_trace_identities(decision.get("exact_trace_identities"))
    decided_at = _parse_timestamp(decision.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(decision.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if decided_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("approval decision must not be calendar-stale")
    if decision.get("expired") is not False:
        raise ValueError("approval decision must not be expired")
    if decision.get("replayed") is not False:
        raise ValueError("approval decision must not be replayed")
    if decision.get("stale") is not False:
        raise ValueError("approval decision must not be stale")
    attestation = decision.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown_attestation = sorted(set(attestation) - _ATTESTATION_KEYS)
    if unknown_attestation:
        raise ValueError(f"unexpected field {unknown_attestation[0]!r}")
    missing_attestation = sorted(_ATTESTATION_KEYS - set(attestation))
    if missing_attestation:
        raise ValueError(f"operator_attestation missing fields: {missing_attestation}")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
    _required_exact_set(decision.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(decision.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if decision.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(decision)
