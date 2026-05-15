"""BLK-SYSTEM-154 metadata-bound RTM / blk-link reconciliation request.

Consumes the exact BLK-SYSTEM-153 review-only preflight and emits a request-only
package for future bounded metadata reconciliation. This is not approval, does
not reserve a run ID, does not generate RTM, does not execute production
blk-link, does not reject drift or establish coverage truth, does not read
protected requirement bodies, does not mutate source/Git, and does not reuse
signer/storage/ledger authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from active_vault_hash_comparison_decision_package import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_blk_link_reconciliation_preflight import (
    EXACT_EXCLUDED_AUTHORITIES as BLK153_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK153_PROOF_OBLIGATIONS,
    PREFLIGHT_PACKAGE_ID as BLK153_PREFLIGHT_PACKAGE_ID,
    PREFLIGHT_STATUS as BLK153_PREFLIGHT_STATUS,
    SIDE_EFFECT_FLAGS as BLK153_SIDE_EFFECT_FLAGS,
)

REQUEST_STATUS = "METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID = "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-REQUEST-154-001"
REQUEST_SCOPE = "METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER = "metadata_bound_rtm_blk_link_reconciliation_request"
REQUESTED_AUTHORITY = "ONE_FUTURE_BOUNDED_METADATA_RTM_BLK_LINK_RECONCILIATION_APPROVAL"
NEXT_REQUIRED_AUTHORITY = "EXACT_BOUNDED_METADATA_RECONCILIATION_APPROVAL_AND_RUN_REQUIRED_NOT_GRANTED"
CANONICAL_BLK153_PREFLIGHT_PACKAGE_HASH = "sha256:06bedb092d14d483ca12e41226330dc7a2a62e3b7235f9215af9aa8e2b13f936"

SIDE_EFFECT_FLAGS = (
    "approval_capture_performed",
    "bounded_reconciliation_approved",
    "future_run_id_reserved",
    "future_run_id_consumed",
    "metadata_reconciliation_executed",
    "rtm_generation_authorized",
    "rtm_generated",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_executed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
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
    "BOUNDED_RECONCILIATION_APPROVAL_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "METADATA_RECONCILIATION_EXECUTION_THIS_SPRINT",
    "RTM_GENERATION_APPROVAL_OR_EXECUTION_THIS_SPRINT",
    "PRODUCTION_BLK_LINK_EXECUTION_THIS_SPRINT",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
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
    "BLK153_PREFLIGHT_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK152_FINALITY_BOUND_THROUGH_BLK153_PREFLIGHT",
    "REQUEST_LIMITED_TO_FUTURE_BOUNDED_METADATA_RECONCILIATION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE",
    "REQUEST_DOES_NOT_RESERVE_OR_CONSUME_RUN_ID",
    "REQUEST_DOES_NOT_EXECUTE_RECONCILIATION",
    "RTM_GENERATION_AND_PRODUCTION_BLK_LINK_EXECUTION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "ACTIVE_VAULT_FILESYSTEM_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_APPROVAL_OR_EXECUTION",
}

REQUIRED_METADATA_INPUTS = (
    "beo_id",
    "beb_id",
    "exact_trace_identities",
    "upstream_finality_package_hash",
    "upstream_signature_hash",
    "upstream_storage_receipt_hash",
    "upstream_ledger_entry_hash",
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk153_preflight_reviewed",
        "request_only_not_approval",
        "future_bounded_metadata_reconciliation_scope_named",
        "metadata_only_inputs_required",
        "no_approval_capture",
        "no_run_id_reserved_or_consumed",
        "no_reconciliation_execution",
        "no_rtm_generation_or_production_blk_link_execution",
        "no_drift_rejection_or_coverage_truth",
        "no_active_vault_filesystem_or_protected_body_access",
        "no_signer_storage_ledger_reuse",
        "no_target_source_git_mutation",
        "no_blk_pipe_blk_test_codex_tooling",
        "no_beb_dispatch_beo_closeout_or_publication",
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
        "upstream_preflight_package_id",
        "upstream_preflight_package_hash",
        "upstream_preflight_request_hash",
        "upstream_finality_package_hash",
        "upstream_signature_hash",
        "upstream_storage_receipt_hash",
        "upstream_ledger_entry_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "required_metadata_inputs",
        "request_future_bounded_metadata_reconciliation_approval",
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


def valid_metadata_bound_rtm_blk_link_reconciliation_request(preflight_package: dict[str, Any], **overrides) -> dict[str, Any]:
    request = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_preflight_package_id": preflight_package["preflight_package_id"],
        "upstream_preflight_package_hash": preflight_package["preflight_package_hash"],
        "upstream_preflight_request_hash": preflight_package["preflight_request_hash"],
        "upstream_finality_package_hash": preflight_package["upstream_finality_package_hash"],
        "upstream_signature_hash": preflight_package["upstream_signature_hash"],
        "upstream_storage_receipt_hash": preflight_package["upstream_storage_receipt_hash"],
        "upstream_ledger_entry_hash": preflight_package["upstream_ledger_entry_hash"],
        "beo_id": preflight_package["beo_id"],
        "beb_id": preflight_package["beb_id"],
        "exact_trace_identities": list(preflight_package["exact_trace_identities"]),
        "required_metadata_inputs": list(REQUIRED_METADATA_INPUTS),
        "request_future_bounded_metadata_reconciliation_approval": True,
        "requested_at": "2099-05-16T09:00:00+10:00",
        "expires_at": "2099-05-16T10:00:00+10:00",
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


def build_metadata_bound_rtm_blk_link_reconciliation_request(
    preflight_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    preflight = _validate_preflight_package(preflight_package)
    request = _validate_request(authority_request, preflight)
    package = {
        "request_status": REQUEST_STATUS,
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_preflight_package_id": preflight["preflight_package_id"],
        "upstream_preflight_package_hash": preflight["preflight_package_hash"],
        "upstream_preflight_request_hash": preflight["preflight_request_hash"],
        "upstream_finality_package_hash": preflight["upstream_finality_package_hash"],
        "upstream_signature_hash": preflight["upstream_signature_hash"],
        "upstream_storage_receipt_hash": preflight["upstream_storage_receipt_hash"],
        "upstream_ledger_entry_hash": preflight["upstream_ledger_entry_hash"],
        "beo_id": preflight["beo_id"],
        "beb_id": preflight["beb_id"],
        "exact_trace_identities": list(preflight["exact_trace_identities"]),
        "required_metadata_inputs": list(REQUIRED_METADATA_INPUTS),
        "request_future_bounded_metadata_reconciliation_approval": True,
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
    package["request_package_hash"] = _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"})
    return package


def _validate_preflight_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("preflight_package must be a dictionary")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("preflight_package_hash"), "preflight_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in normalized.items() if key != "preflight_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("preflight_package_hash does not match submitted BLK-153 package")
    if submitted_hash != CANONICAL_BLK153_PREFLIGHT_PACKAGE_HASH:
        raise ValueError("canonical BLK-153 preflight package required")
    expected = {
        "preflight_status": BLK153_PREFLIGHT_STATUS,
        "preflight_package_id": BLK153_PREFLIGHT_PACKAGE_ID,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "metadata_only_reconciliation_preflight_ready": True,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"preflight {key} must be {value}")
    _required_hash(normalized.get("preflight_request_hash"), "preflight_request_hash")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    _required_exact_set(normalized.get("proof_obligations"), BLK153_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK153_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK153_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"preflight {flag} must remain false")
    return normalized


def _validate_request(request: Any, preflight: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"authority_request missing fields: {missing}")
    _scan_value_strings(
        {
            "operator_identity": request.get("operator_identity"),
            "request_package_id": request.get("request_package_id"),
            "request_scope": request.get("request_scope"),
            "selected_frontier": request.get("selected_frontier"),
            "required_metadata_inputs": request.get("required_metadata_inputs"),
        },
        "authority_request",
        allow_selected=True,
    )
    expected = {
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_authority": REQUESTED_AUTHORITY,
        "upstream_preflight_package_id": preflight["preflight_package_id"],
        "upstream_preflight_package_hash": preflight["preflight_package_hash"],
        "upstream_preflight_request_hash": preflight["preflight_request_hash"],
        "upstream_finality_package_hash": preflight["upstream_finality_package_hash"],
        "upstream_signature_hash": preflight["upstream_signature_hash"],
        "upstream_storage_receipt_hash": preflight["upstream_storage_receipt_hash"],
        "upstream_ledger_entry_hash": preflight["upstream_ledger_entry_hash"],
        "beo_id": preflight["beo_id"],
        "beb_id": preflight["beb_id"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must be {value}")
    if request.get("exact_trace_identities") != preflight.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-153 preflight package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    _required_exact_set(request.get("required_metadata_inputs"), set(REQUIRED_METADATA_INPUTS), "required_metadata_inputs")
    if request.get("request_future_bounded_metadata_reconciliation_approval") is not True:
        raise ValueError("request_future_bounded_metadata_reconciliation_approval must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("authority request must not be calendar-stale")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"authority request must not be {flag}")
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
