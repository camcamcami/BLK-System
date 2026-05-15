"""BLK-SYSTEM-142 metadata-bound RTM-generation authority request.

This deterministic fixture consumes the exact BLK-SYSTEM-141 clean
active-vault hash-comparison reconciliation and emits a request-only package for
future RTM-generation approval capture. It does not capture approval, reserve or
consume a run ID, generate RTM, reject drift, establish coverage truth, read
active-vault files, read/copy/parse/hash/scan protected requirement bodies,
mutate source/Git state, run tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_decision_package import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from active_vault_hash_comparison_post_execution_reconciliation import (
    CLEAN_RECONCILIATION_RESULT as BLK141_CLEAN_RECONCILIATION_RESULT,
    EXACT_EXCLUDED_AUTHORITIES as BLK141_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK141_PROOF_OBLIGATIONS,
    NEXT_FRONTIER_CLEAN as BLK141_NEXT_FRONTIER_CLEAN,
    RECONCILIATION_PACKAGE_ID as BLK141_RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_STATUS as BLK141_RECONCILIATION_STATUS,
    SIDE_EFFECT_FLAGS as BLK141_SIDE_EFFECT_FLAGS,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

REQUEST_STATUS = "RTM_GENERATION_AUTHORITY_REQUEST_READY_NOT_APPROVED"
AUTHORITY_REQUEST_PACKAGE_ID = "RTM-GENERATION-AUTHORITY-REQUEST-142-001"
REQUEST_SCOPE = "METADATA_BOUND_RTM_GENERATION_AUTHORITY_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER = "metadata_bound_trace_matrix_generation_authority_request"
REQUESTED_AUTHORITY = "ONE_FUTURE_METADATA_BOUND_RTM_GENERATION_APPROVAL_CAPTURE"
NEXT_REQUIRED_AUTHORITY = "EXACT_RTM_GENERATION_APPROVAL_CAPTURE_REQUIRED_NOT_EXECUTED"
CANONICAL_BLK141_RECONCILIATION_PACKAGE_HASH = "sha256:9de60a578be56d252c34ed1f9f4b9d2c3236420a9b507cacfa5d0bb02bb4d960"

SIDE_EFFECT_FLAGS = (
    "approval_capture_performed",
    "rtm_generation_approved",
    "rtm_generated",
    "future_run_id_reserved",
    "future_run_id_consumed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
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
    "beo_publication_or_signing_authorized",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RTM_GENERATION_APPROVAL_THIS_SPRINT",
    "RTM_GENERATION_EXECUTION_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_THIS_SPRINT",
    "FUTURE_RUN_ID_CONSUMPTION_THIS_SPRINT",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXACT_BLK141_RECONCILIATION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
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
    "BLK141_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK140_COMPARISON_EXECUTION_BOUND_THROUGH_BLK141",
    "CLEAN_METADATA_HASH_COMPARISON_REQUIRED",
    "REQUEST_LIMITED_TO_FUTURE_METADATA_BOUND_RTM_GENERATION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE",
    "REQUEST_DOES_NOT_RESERVE_OR_CONSUME_RUN_ID",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_APPROVAL_CAPTURE",
}

_RECONCILIATION_REQUIRED_KEYS = frozenset(
    {
        "reconciliation_status",
        "reconciliation_package_id",
        "operator_identity",
        "reconciliation_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_comparison_record_id",
        "upstream_comparison_record_hash",
        "upstream_approval_capture_package_id",
        "upstream_approval_capture_package_hash",
        "run_id_consumed",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "metadata_hashes_match",
        "mismatch_count",
        "mismatches",
        "reconciliation_result",
        "recommended_next_frontier",
        "next_frontier_granted",
        "reconciliation_context_hash",
        "reconciled_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "reconciliation_package_hash",
        *BLK141_SIDE_EFFECT_FLAGS,
    }
)

_REQUEST_KEYS = frozenset(
    {
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_reconciliation_context_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_comparison_record_id",
        "upstream_comparison_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "metadata_hashes_match",
        "request_future_exact_metadata_bound_rtm_generation_approval",
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
        "exact_blk141_reconciliation_reviewed",
        "clean_metadata_hash_comparison_verified",
        "request_is_for_future_approval_not_approval",
        "rtm_generation_not_approved_or_executed",
        "future_run_id_not_reserved_or_consumed",
        "protected_body_reads_excluded",
        "active_vault_filesystem_reads_excluded",
        "drift_rejection_excluded",
        "coverage_truth_excluded",
        "reusable_blk_link_excluded",
        "signer_storage_ledger_excluded",
        "beb_dispatch_beo_closeout_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)


def build_metadata_bound_rtm_generation_authority_request(
    reconciliation_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    reconciliation = _validate_reconciliation_package(reconciliation_package)
    request = _validate_authority_request(authority_request, reconciliation)
    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_comparison_record_id": reconciliation["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": reconciliation["upstream_comparison_record_hash"],
        "beo_id": reconciliation["beo_id"],
        "beb_id": reconciliation["beb_id"],
        "exact_trace_identities": list(reconciliation["exact_trace_identities"]),
        "metadata_hashes_match": True,
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "approval_capture_performed": False,
        "rtm_generation_approved": False,
        "rtm_generated": False,
        "future_run_id_reserved": False,
        "future_run_id_consumed": False,
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


def _validate_reconciliation_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("reconciliation package must be a dictionary")
    unknown = sorted(set(package) - _RECONCILIATION_REQUIRED_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_RECONCILIATION_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"reconciliation package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in package.items() if key != "reconciliation_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-141 package")
    if package.get("reconciliation_status") != BLK141_RECONCILIATION_STATUS:
        raise ValueError("reconciliation_status must match BLK-141 reconciliation status")
    if package.get("reconciliation_package_id") != BLK141_RECONCILIATION_PACKAGE_ID:
        raise ValueError("reconciliation_package_id must match exact BLK-141 package")
    if package.get("metadata_hashes_match") is not True or package.get("mismatch_count") != 0 or package.get("mismatches") != []:
        raise ValueError("clean BLK-141 reconciliation required")
    if submitted_hash != CANONICAL_BLK141_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-141 reconciliation package required")
    if package.get("reconciliation_result") != BLK141_CLEAN_RECONCILIATION_RESULT:
        raise ValueError("clean BLK-141 reconciliation required")
    if package.get("recommended_next_frontier") != BLK141_NEXT_FRONTIER_CLEAN:
        raise ValueError("recommended_next_frontier must be BLK-141 RTM request frontier")
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-141 next frontier must not be granted")
    if package.get("expired") is not False or package.get("replayed") is not False or package.get("stale") is not False:
        raise ValueError("BLK-141 reconciliation package must not be expired, replayed, or stale")
    _required_hash(package.get("reconciliation_context_hash"), "reconciliation_context_hash")
    _parse_timestamp(package.get("reconciled_at"), "reconciled_at")
    _required_exact_set(package.get("proof_obligations"), BLK141_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK141_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK141_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_authority_request(request: Any, reconciliation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"authority request missing fields: {missing}")
    _scan_value_strings({"operator_identity": request.get("operator_identity")}, "authority_request", allow_selected=True)
    expected = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_comparison_record_id": reconciliation["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": reconciliation["upstream_comparison_record_hash"],
        "beo_id": reconciliation["beo_id"],
        "beb_id": reconciliation["beb_id"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must match BLK-141 reconciliation package")
    if request.get("operator_identity") != reconciliation.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-141 reconciliation package")
    if request.get("exact_trace_identities") != reconciliation.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-141 reconciliation package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    if request.get("metadata_hashes_match") is not True:
        raise ValueError("metadata_hashes_match must match clean BLK-141 reconciliation")
    if request.get("request_future_exact_metadata_bound_rtm_generation_approval") is not True:
        raise ValueError("request_future_exact_metadata_bound_rtm_generation_approval must be true")
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
