"""BLK-SYSTEM-153 metadata-bound RTM / blk-link reconciliation preflight.

This deterministic fixture consumes the exact BLK-SYSTEM-152 authoritative BEO
publication finality package and emits one review-only preflight for the
operator-selected metadata-bound RTM / blk-link reconciliation path. It selects
no execution authority, captures no approval, reserves no run ID, generates no
RTM, performs no production blk-link execution, rejects no drift, establishes no
coverage truth, reads no protected requirement bodies, reuses no signer/storage/
ledger authority, mutates no source/Git state, runs no tooling, and claims no
production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from active_vault_hash_comparison_decision_package import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from authoritative_beo_publication_authority_request import _canonical_hash
from authoritative_beo_publication_finality import (
    EXACT_EXCLUDED_AUTHORITIES as BLK152_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK152_PROOF_OBLIGATIONS,
    FINALITY_PACKAGE_ID as BLK152_FINALITY_PACKAGE_ID,
    FINALITY_STATUS as BLK152_FINALITY_STATUS,
    REQUIRED_FALSE_FLAGS as BLK152_REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS as BLK152_REQUIRED_TRUE_FLAGS,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

PREFLIGHT_STATUS = "METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_PREFLIGHT_READY_NOT_AUTHORITY"
PREFLIGHT_PACKAGE_ID = "METADATA-BOUND-RTM-BLK-LINK-RECONCILIATION-PREFLIGHT-153-001"
PREFLIGHT_SCOPE = "METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_PREFLIGHT_ONLY_NO_APPROVAL_OR_EXECUTION"
SELECTED_FRONTIER = "metadata_bound_rtm_blk_link_reconciliation_preflight"
REQUESTED_NEXT_PATH = "ONE_FUTURE_METADATA_BOUND_RTM_BLK_LINK_RECONCILIATION_DECISION"
NEXT_REQUIRED_AUTHORITY = "EXACT_OPERATOR_DECISION_REQUIRED_BEFORE_RTM_OR_BLK_LINK_EXECUTION"
CANONICAL_BLK152_FINALITY_PACKAGE_HASH = "sha256:fa661ce760a5df8d8c1d893a8b71b4ccbfa5b882e683e594511aa30984ba09a3"
CANONICAL_BLK152_SIGNATURE_HASH = "sha256:3e93c9707b993453e221278287357470dcef6a424068a8bfbdf058868d5e3d5f"
CANONICAL_BLK152_STORAGE_RECEIPT_HASH = "sha256:f2bf49758e082ac68eb134f0c269f6f3e0bb8e32fa096f4d3bb049020cba60f3"
CANONICAL_BLK152_LEDGER_ENTRY_HASH = "sha256:54e41a65821e6c05e203ee36734cb1a37d7a798519393c7de61b82a562f984f0"

SIDE_EFFECT_FLAGS = (
    "operator_decision_captured",
    "authority_request_emitted",
    "approval_capture_performed",
    "future_run_id_reserved",
    "future_run_id_consumed",
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
    "OPERATOR_DECISION_CAPTURE_THIS_SPRINT",
    "AUTHORITY_REQUEST_EMISSION_THIS_SPRINT",
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
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
    "BLK152_FINALITY_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK152_SIGNATURE_STORAGE_LEDGER_RECEIPTS_BOUND_AS_UPSTREAM_EVIDENCE_ONLY",
    "OPERATOR_SELECTED_METADATA_BOUND_RTM_BLK_LINK_PREFLIGHT_ONLY",
    "PREFLIGHT_IS_NOT_OPERATOR_DECISION_CAPTURE",
    "PREFLIGHT_DOES_NOT_EMIT_AUTHORITY_REQUEST_OR_APPROVAL",
    "PREFLIGHT_DOES_NOT_RESERVE_OR_CONSUME_RUN_ID",
    "FUTURE_RECONCILIATION_REQUIRES_METADATA_ONLY_IDS_AND_HASHES",
    "RTM_GENERATION_AND_PRODUCTION_BLK_LINK_EXECUTION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "ACTIVE_VAULT_FILESYSTEM_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_FUTURE_EXECUTION_RUNG",
}

REQUIRED_FUTURE_EVIDENCE = (
    "exact BLK-152 finality package hash and receipt hashes",
    "metadata-only requirement identifiers and sha256 version hashes",
    "one future operator decision naming exact reconciliation scope",
    "fresh request window and non-replay evidence before any run ID",
    "explicit adjacent-authority denial checklist before any execution package",
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk152_finality_reviewed",
        "operator_selected_preflight_only",
        "metadata_only_future_evidence_required",
        "no_operator_decision_captured",
        "no_authority_request_or_approval_emitted",
        "no_future_run_id_reserved_or_consumed",
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
        "preflight_package_id",
        "operator_identity",
        "preflight_scope",
        "selected_frontier",
        "requested_next_path",
        "upstream_finality_package_id",
        "upstream_finality_package_hash",
        "upstream_signature_hash",
        "upstream_storage_receipt_hash",
        "upstream_ledger_entry_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "metadata_only_reconciliation_preflight_requested",
        "required_future_evidence",
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


def valid_metadata_bound_rtm_blk_link_reconciliation_preflight_request(finality_package: dict[str, Any], **overrides) -> dict[str, Any]:
    request = {
        "preflight_package_id": PREFLIGHT_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_next_path": REQUESTED_NEXT_PATH,
        "upstream_finality_package_id": finality_package["finality_package_id"],
        "upstream_finality_package_hash": finality_package["finality_package_hash"],
        "upstream_signature_hash": finality_package["signature_hash"],
        "upstream_storage_receipt_hash": finality_package["storage_receipt_hash"],
        "upstream_ledger_entry_hash": finality_package["ledger_entry_hash"],
        "beo_id": finality_package["beo_id"],
        "beb_id": finality_package["beb_id"],
        "exact_trace_identities": list(finality_package["exact_trace_identities"]),
        "metadata_only_reconciliation_preflight_requested": True,
        "required_future_evidence": list(REQUIRED_FUTURE_EVIDENCE),
        "requested_at": "2099-05-16T08:00:00+10:00",
        "expires_at": "2099-05-16T09:00:00+10:00",
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


def build_metadata_bound_rtm_blk_link_reconciliation_preflight(
    finality_package: dict[str, Any], preflight_request: dict[str, Any]
) -> dict[str, Any]:
    finality = _validate_finality_package(finality_package)
    request = _validate_preflight_request(preflight_request, finality)
    package = {
        "preflight_status": PREFLIGHT_STATUS,
        "preflight_package_id": PREFLIGHT_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_next_path": REQUESTED_NEXT_PATH,
        "upstream_finality_package_id": finality["finality_package_id"],
        "upstream_finality_package_hash": finality["finality_package_hash"],
        "upstream_signature_hash": finality["signature_hash"],
        "upstream_storage_receipt_hash": finality["storage_receipt_hash"],
        "upstream_ledger_entry_hash": finality["ledger_entry_hash"],
        "beo_id": finality["beo_id"],
        "beb_id": finality["beb_id"],
        "exact_trace_identities": list(finality["exact_trace_identities"]),
        "metadata_only_reconciliation_preflight_ready": True,
        "required_future_evidence": list(REQUIRED_FUTURE_EVIDENCE),
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "preflight_request_hash": _canonical_hash(request),
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
    package["preflight_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "preflight_package_hash"}
    )
    return package


def _validate_finality_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("finality_package must be a dictionary")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("finality_package_hash"), "finality_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in normalized.items() if key != "finality_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("finality_package_hash does not match submitted BLK-152 finality package")
    if submitted_hash != CANONICAL_BLK152_FINALITY_PACKAGE_HASH:
        raise ValueError("canonical BLK-152 finality package required")
    expected = {
        "finality_status": BLK152_FINALITY_STATUS,
        "finality_package_id": BLK152_FINALITY_PACKAGE_ID,
        "signature_hash": CANONICAL_BLK152_SIGNATURE_HASH,
        "storage_receipt_hash": CANONICAL_BLK152_STORAGE_RECEIPT_HASH,
        "ledger_entry_hash": CANONICAL_BLK152_LEDGER_ENTRY_HASH,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            if key == "rtm_status":
                raise ValueError("rtm_status must remain NOT_GENERATED")
            raise ValueError(f"{key} must be {value}")
    if normalized.get("signature_receipt", {}).get("signature_hash") != CANONICAL_BLK152_SIGNATURE_HASH:
        raise ValueError("signature_receipt must match BLK-152 signature hash")
    if normalized.get("immutable_storage_receipt", {}).get("storage_receipt_hash") != CANONICAL_BLK152_STORAGE_RECEIPT_HASH:
        raise ValueError("immutable_storage_receipt must match BLK-152 storage receipt hash")
    if normalized.get("public_ledger_entry", {}).get("ledger_entry_hash") != CANONICAL_BLK152_LEDGER_ENTRY_HASH:
        raise ValueError("public_ledger_entry must match BLK-152 ledger entry hash")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    _required_exact_set(normalized.get("proof_obligations"), BLK152_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK152_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK152_REQUIRED_TRUE_FLAGS:
        if normalized.get(flag) is not True:
            raise ValueError(f"finality {flag} must remain true")
    for flag in BLK152_REQUIRED_FALSE_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"finality {flag} must remain false")
    return normalized


def _validate_preflight_request(request: Any, finality: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("preflight_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"preflight_request missing fields: {missing}")
    _scan_value_strings(
        {
            "operator_identity": request.get("operator_identity"),
            "preflight_package_id": request.get("preflight_package_id"),
            "preflight_scope": request.get("preflight_scope"),
            "selected_frontier": request.get("selected_frontier"),
            "required_future_evidence": request.get("required_future_evidence"),
        },
        "preflight_request",
        allow_selected=True,
    )
    expected = {
        "preflight_package_id": PREFLIGHT_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "requested_next_path": REQUESTED_NEXT_PATH,
        "upstream_finality_package_id": finality["finality_package_id"],
        "upstream_finality_package_hash": finality["finality_package_hash"],
        "upstream_signature_hash": finality["signature_hash"],
        "upstream_storage_receipt_hash": finality["storage_receipt_hash"],
        "upstream_ledger_entry_hash": finality["ledger_entry_hash"],
        "beo_id": finality["beo_id"],
        "beb_id": finality["beb_id"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must be {value}")
    if request.get("exact_trace_identities") != finality.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-152 finality package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    if request.get("metadata_only_reconciliation_preflight_requested") is not True:
        raise ValueError("metadata_only_reconciliation_preflight_requested must be true")
    _required_exact_set(request.get("required_future_evidence"), set(REQUIRED_FUTURE_EVIDENCE), "required_future_evidence")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("preflight request must not be calendar-stale")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"preflight request must not be {flag}")
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
