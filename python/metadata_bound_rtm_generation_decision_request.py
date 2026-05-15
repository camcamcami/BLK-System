"""BLK-SYSTEM-157 metadata-bound RTM generation decision request.

Consumes the exact BLK-SYSTEM-156 post-reconciliation review package and emits a
request-only package for a future exact operator approval decision on
metadata-bound RTM generation. This fixture does not capture approval, reserve or
consume a run ID, generate RTM, execute production blk-link, reject drift,
establish coverage truth, read protected bodies, mutate source/Git, run live
tooling, or reuse signer/storage/ledger authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from active_vault_hash_comparison_decision_package import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from post_metadata_rtm_blk_link_reconciliation_review import (
    EXACT_EXCLUDED_AUTHORITIES as BLK156_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK156_PROOF_OBLIGATIONS,
    NEXT_FRONTIER as BLK156_NEXT_FRONTIER,
    REVIEW_PACKAGE_ID as BLK156_REVIEW_PACKAGE_ID,
    REVIEW_STATUS as BLK156_REVIEW_STATUS,
    SIDE_EFFECT_FLAGS as BLK156_SIDE_EFFECT_FLAGS,
)

REQUEST_STATUS = "METADATA_BOUND_RTM_GENERATION_DECISION_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID = "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-001"
REQUEST_SCOPE = "METADATA_BOUND_RTM_GENERATION_DECISION_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER = "metadata_bound_rtm_generation_decision_request"
REQUESTED_AUTHORITY = "ONE_FUTURE_EXACT_METADATA_BOUND_RTM_GENERATION_APPROVAL"
NEXT_REQUIRED_AUTHORITY = "EXACT_OPERATOR_APPROVAL_REQUIRED_BEFORE_METADATA_BOUND_RTM_GENERATION"
NEXT_FRONTIER = "NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_APPROVAL_NOT_GRANTED"
CANONICAL_BLK156_REVIEW_PACKAGE_HASH = "sha256:9dcbe35946b9320fc4aaf46cfb31273e38ccf56a49249f7eac91be37278f537e"
CANONICAL_BLK156_RECONCILIATION_RECORD_HASH = "sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026"

SIDE_EFFECT_FLAGS = (
    "approval_capture_performed",
    "rtm_generation_approved",
    "rtm_generation_authorized",
    "rtm_generated",
    "rtm_record_emitted",
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
    "signer_storage_ledger_reuse_authorized",
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
    "RTM_RECORD_EMISSION_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_THIS_SPRINT",
    "FUTURE_RUN_ID_CONSUMPTION_THIS_SPRINT",
    "PRODUCTION_BLK_LINK_EXECUTION_THIS_SPRINT",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_THIS_SPRINT",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_AUTHORITY",
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
    "BLK156_REVIEW_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK155_RECONCILIATION_RECORD_BOUND_THROUGH_BLK156",
    "CLEAN_METADATA_RECONCILIATION_REQUIRED",
    "REQUEST_LIMITED_TO_FUTURE_METADATA_BOUND_RTM_GENERATION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE",
    "REQUEST_DOES_NOT_RESERVE_OR_CONSUME_RUN_ID",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "RTM_RECORD_NOT_EMITTED_BY_REQUEST",
    "PRODUCTION_BLK_LINK_EXECUTION_EXCLUDED",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_APPROVAL_CAPTURE",
}

REQUIRED_FUTURE_EVIDENCE = (
    "exact BLK-157 request package hash",
    "exact BLK-156 post-reconciliation review package hash",
    "exact BLK-155 reconciliation record hash",
    "metadata-only trace identities and version hashes",
    "fresh operator approval window before any run ID or RTM generation",
    "explicit denial checklist for drift, coverage, protected-body, production blk-link, tooling, and signer/storage/ledger reuse",
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk156_review_package_reviewed",
        "clean_metadata_reconciliation_confirmed",
        "request_is_for_future_approval_not_approval",
        "rtm_generation_not_approved_authorized_or_executed",
        "rtm_record_not_emitted",
        "future_run_id_not_reserved_or_consumed",
        "protected_body_reads_excluded",
        "active_vault_filesystem_reads_excluded",
        "no_drift_rejection_or_coverage_truth",
        "reusable_blk_link_excluded",
        "signer_storage_ledger_excluded",
        "beb_dispatch_beo_closeout_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)

_REQUEST_KEYS = frozenset(
    {
        "request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "requested_authority",
        "upstream_review_package_id",
        "upstream_review_package_hash",
        "upstream_review_context_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_reconciliation_record_id",
        "upstream_reconciliation_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "required_future_evidence",
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


def valid_metadata_bound_rtm_generation_decision_request(review_package: dict[str, Any], **overrides) -> dict[str, Any]:
    request = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_review_package_id": review_package["review_package_id"],
        "upstream_review_package_hash": review_package["review_package_hash"],
        "upstream_review_context_hash": review_package["review_context_hash"],
        "upstream_execution_package_id": review_package["upstream_execution_package_id"],
        "upstream_execution_package_hash": review_package["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": review_package["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": review_package["upstream_reconciliation_record_hash"],
        "beo_id": review_package["beo_id"],
        "beb_id": review_package["beb_id"],
        "exact_trace_identities": list(review_package["exact_trace_identities"]),
        "required_future_evidence": list(REQUIRED_FUTURE_EVIDENCE),
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "requested_at": "2099-05-16T13:00:00+10:00",
        "expires_at": "2099-05-16T14:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in sorted(_ATTESTATION_KEYS)},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def build_metadata_bound_rtm_generation_decision_request(
    review_package: dict[str, Any], decision_request: dict[str, Any]
) -> dict[str, Any]:
    review = _validate_review_package(review_package)
    request = _validate_decision_request(decision_request, review)
    package = {
        "request_status": REQUEST_STATUS,
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_review_package_id": review["review_package_id"],
        "upstream_review_package_hash": review["review_package_hash"],
        "upstream_review_context_hash": review["review_context_hash"],
        "upstream_execution_package_id": review["upstream_execution_package_id"],
        "upstream_execution_package_hash": review["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": review["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": review["upstream_reconciliation_record_hash"],
        "beo_id": review["beo_id"],
        "beb_id": review["beb_id"],
        "exact_trace_identities": list(review["exact_trace_identities"]),
        "required_future_evidence": list(REQUIRED_FUTURE_EVIDENCE),
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "next_frontier": NEXT_FRONTIER,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "decision_request_hash": _canonical_hash(request),
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
    package["request_package_hash"] = _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"})
    return package


def _validate_review_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("review_package must be a dictionary")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("review_package_hash"), "review_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in normalized.items() if key != "review_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("review_package_hash does not match submitted BLK-156 package")
    if submitted_hash != CANONICAL_BLK156_REVIEW_PACKAGE_HASH:
        raise ValueError("canonical BLK-156 review package required")
    expected = {
        "review_status": BLK156_REVIEW_STATUS,
        "review_package_id": BLK156_REVIEW_PACKAGE_ID,
        "upstream_reconciliation_record_hash": CANONICAL_BLK156_RECONCILIATION_RECORD_HASH,
        "review_result": "CLEAN_METADATA_RECONCILIATION_REVIEWED_NEXT_DECISION_REQUIRED",
        "next_frontier": BLK156_NEXT_FRONTIER,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"review_package {key} must be {value}")
    _required_hash(normalized.get("review_context_hash"), "review_context_hash")
    _required_hash(normalized.get("upstream_execution_package_hash"), "upstream_execution_package_hash")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    _required_exact_set(normalized.get("proof_obligations"), BLK156_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK156_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK156_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"review_package {flag} must remain false")
    return normalized


def _validate_decision_request(request: Any, review: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("decision_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"decision_request missing fields: {missing}")
    expected = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_review_package_id": review["review_package_id"],
        "upstream_review_package_hash": review["review_package_hash"],
        "upstream_review_context_hash": review["review_context_hash"],
        "upstream_execution_package_id": review["upstream_execution_package_id"],
        "upstream_execution_package_hash": review["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": review["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": review["upstream_reconciliation_record_hash"],
        "beo_id": review["beo_id"],
        "beb_id": review["beb_id"],
    }
    scan_on_mismatch = {"operator_identity", "request_scope", "selected_frontier", "requested_authority"}
    for key, value in expected.items():
        if request.get(key) != value:
            if key == "request_package_id":
                candidate = str(request.get(key))
                if "docs" in candidate.lower() or "system" in candidate.lower() or "%" in candidate:
                    _scan_value_strings({key: request.get(key)}, "decision_request", allow_selected=True)
            elif key in scan_on_mismatch:
                _scan_value_strings({key: request.get(key)}, "decision_request", allow_selected=True)
            raise ValueError(f"{key} must be {value}")
    if request.get("exact_trace_identities") != review.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-156 review package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    evidence = request.get("required_future_evidence")
    if isinstance(evidence, list):
        allowed_evidence = set(REQUIRED_FUTURE_EVIDENCE)
        extras = [item for item in evidence if not isinstance(item, str) or item not in allowed_evidence]
        if extras:
            _scan_value_strings({"required_future_evidence": extras}, "decision_request", allow_selected=True)
    _required_exact_set(request.get("required_future_evidence"), set(REQUIRED_FUTURE_EVIDENCE), "required_future_evidence")
    if request.get("request_future_exact_metadata_bound_rtm_generation_approval") is not True:
        raise ValueError("request_future_exact_metadata_bound_rtm_generation_approval must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("decision request must not be calendar-stale")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"decision request must not be {flag}")
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
