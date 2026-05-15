"""BLK-SYSTEM-138 active-vault hash-comparison authority request.

This deterministic fixture consumes the exact BLK-SYSTEM-137 decision package
and emits a request-only package for future metadata/hash-only active-vault
comparison approval. It does not capture approval, perform comparison, read or
hash protected bodies, generate RTM, reject drift, mutate source/Git state, run
tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_decision_package import (
    DECISION_PACKAGE_ID as BLK137_DECISION_PACKAGE_ID,
    DECISION_STATUS as BLK137_DECISION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK137_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK137_PROOF_OBLIGATIONS,
    SELECTED_CAPABILITY as BLK137_SELECTED_CAPABILITY,
    SIDE_EFFECT_FLAGS as BLK137_SIDE_EFFECT_FLAGS,
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

REQUEST_STATUS = "ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_READY_NOT_APPROVED"
AUTHORITY_REQUEST_PACKAGE_ID = "ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-138-001"
REQUEST_SCOPE = "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_AUTHORITY_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER = "active_vault_hash_comparison_metadata_hash_only_authority_request"
REQUESTED_AUTHORITY = "ONE_FUTURE_METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_APPROVAL_CAPTURE"
NEXT_REQUIRED_AUTHORITY = "EXACT_ACTIVE_VAULT_HASH_COMPARISON_APPROVAL_CAPTURE_REQUIRED_NOT_EXECUTED"

SIDE_EFFECT_FLAGS = (
    "approval_capture_performed",
    "active_vault_hash_comparison_approved",
    "active_vault_hash_comparison_performed",
    "active_vault_metadata_read_performed",
    "future_run_id_reserved",
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
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_THIS_SPRINT",
    "ACTIVE_VAULT_METADATA_READ_THIS_SPRINT",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
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
    "BLK137_DECISION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK136_RECONCILIATION_PACKAGE_BOUND_THROUGH_BLK137",
    "REQUEST_LIMITED_TO_METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE",
    "COMPARISON_NOT_PERFORMED_BY_REQUEST",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_AUTHORIZED_BY_REQUEST",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_APPROVAL_CAPTURE",
}

_REQUEST_KEYS = frozenset(
    {
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_decision_package_id",
        "upstream_decision_package_hash",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "request_future_exact_metadata_hash_only_active_vault_comparison_approval",
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
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk137_decision_reviewed",
        "request_is_for_future_approval_not_approval",
        "metadata_hash_only_scope_preserved",
        "approval_capture_not_performed",
        "comparison_not_performed",
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

_DECISION_REQUIRED_KEYS = frozenset(
    {
        "decision_status",
        "decision_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "selected_capability",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_execution_record_id",
        "upstream_execution_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "next_required_authority",
        "decision_context_hash",
        "decided_at",
        "stale",
        "replayed",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "decision_package_hash",
    }
)


def build_active_vault_hash_comparison_authority_request(
    decision_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    decision = _validate_decision_package(decision_package)
    request = _validate_authority_request(authority_request, decision)
    trace_identities = list(decision["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_decision_package_id": decision["decision_package_id"],
        "upstream_decision_package_hash": decision["decision_package_hash"],
        "upstream_reconciliation_package_id": decision["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": decision["upstream_reconciliation_package_hash"],
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
        "exact_trace_identities": trace_identities,
        "request_future_exact_metadata_hash_only_active_vault_comparison_approval": True,
        "approval_capture_performed": False,
        "active_vault_hash_comparison_performed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "authority_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(package)
    return package


def _validate_decision_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("decision package must be a dictionary")
    missing = sorted(_DECISION_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"decision package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("decision_package_hash"), "decision_package_hash")
    actual_hash = _canonical_hash({k: v for k, v in package.items() if k != "decision_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("decision_package_hash does not match submitted BLK-137 package")
    if package.get("decision_package_id") != BLK137_DECISION_PACKAGE_ID:
        raise ValueError("decision_package_id must match exact BLK-137 package")
    if package.get("decision_status") != BLK137_DECISION_STATUS:
        raise ValueError("decision_status must match BLK-137 decision status")
    if package.get("selected_capability") != BLK137_SELECTED_CAPABILITY:
        raise ValueError("selected_capability must be metadata/hash-only active-vault comparison")
    _required_exact_set(package.get("proof_obligations"), BLK137_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK137_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK137_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_authority_request(request: Any, decision: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"authority request missing fields: {missing}")
    scan_request = {
        key: value
        for key, value in request.items()
        if key not in {"operator_attestation", "proof_obligations", "excluded_authorities"}
    }
    _scan_value_strings(scan_request, "authority_request", allow_selected=True)
    expected = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_decision_package_id": decision["decision_package_id"],
        "upstream_decision_package_hash": decision["decision_package_hash"],
        "upstream_reconciliation_package_id": decision["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": decision["upstream_reconciliation_package_hash"],
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must be {value!r}")
    if request.get("operator_identity") != decision.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-137 decision package")
    if request.get("exact_trace_identities") != decision.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-137 decision package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    if request.get("request_future_exact_metadata_hash_only_active_vault_comparison_approval") is not True:
        raise ValueError("request_future_exact_metadata_hash_only_active_vault_comparison_approval must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("authority request must not be calendar-stale")
    if request.get("expired") is not False:
        raise ValueError("authority request must not be expired")
    if request.get("replayed") is not False:
        raise ValueError("authority request must not be replayed")
    if request.get("stale") is not False:
        raise ValueError("authority request must not be stale")
    attestation = request.get("operator_attestation")
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
    _required_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(request)
