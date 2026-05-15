"""BLK-SYSTEM-155 bounded metadata RTM / blk-link reconciliation execution.

Consumes the exact BLK-SYSTEM-154 request package and the operator's exact
BLK-SYSTEM-154-to-156 instruction to emit one bounded metadata-only
reconciliation execution record. The package consumes one run ID in returned
evidence but does not generate RTM, execute production blk-link, reject drift,
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
from metadata_bound_rtm_blk_link_reconciliation_request import (
    EXACT_EXCLUDED_AUTHORITIES as BLK154_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK154_PROOF_OBLIGATIONS,
    REQUEST_PACKAGE_ID as BLK154_REQUEST_PACKAGE_ID,
    REQUEST_STATUS as BLK154_REQUEST_STATUS,
    SIDE_EFFECT_FLAGS as BLK154_SIDE_EFFECT_FLAGS,
)

EXECUTION_STATUS = "BOUNDED_METADATA_RTM_BLK_LINK_RECONCILIATION_EXECUTED_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "BOUNDED-METADATA-RTM-BLK-LINK-RECONCILIATION-EXECUTION-155-001"
RECONCILIATION_RECORD_ID = "BOUNDED-METADATA-RTM-BLK-LINK-RECONCILIATION-RECORD-155-001"
RUN_ID = "RUN-BLK-SYSTEM-155-BOUNDED-METADATA-RTM-BLK-LINK-RECONCILIATION-001"
EXECUTION_SCOPE = "BOUNDED_METADATA_RTM_BLK_LINK_RECONCILIATION_EXECUTION_RECORD_ONLY"
SELECTED_FRONTIER = "bounded_metadata_rtm_blk_link_reconciliation_execution"
EXACT_OPERATOR_APPROVAL_TEXT_RAW = "plan and execute BLK-SYSTEM-154 to 156"
CANONICAL_BLK154_REQUEST_PACKAGE_HASH = "sha256:8b8904380c2ba38cd0df4cbbd9ebc4c75df7c4d006044c3485b6582ea5124f3f"
NEXT_REQUIRED_AUTHORITY = "POST_RECONCILIATION_REVIEW_REQUIRED_NOT_AUTHORITY"

REQUIRED_TRUE_FLAGS = (
    "approval_capture_performed",
    "future_run_id_consumed",
    "metadata_reconciliation_executed",
)

REQUIRED_FALSE_FLAGS = (
    "future_run_id_reserved",
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
    "RTM_GENERATION_BEYOND_METADATA_RECONCILIATION",
    "PRODUCTION_BLK_LINK_EXECUTION_BEYOND_RECORD_ONLY_RECONCILIATION",
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
    "BLK154_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK153_PREFLIGHT_BOUND_THROUGH_BLK154_REQUEST",
    "OPERATOR_EXACT_154_TO_156_APPROVAL_TEXT_BOUND",
    "ONE_RUN_ID_CONSUMED_IN_RECORD_ONLY_EVIDENCE",
    "RECONCILIATION_RECORD_HASH_BOUND",
    "METADATA_IDENTITIES_RECONCILED_WITHOUT_PROTECTED_BODY_ACCESS",
    "RTM_GENERATION_AND_PRODUCTION_BLK_LINK_EXECUTION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "POST_RECONCILIATION_REVIEW_REQUIRED",
}

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk154_request_reviewed",
        "operator_approved_bounded_metadata_reconciliation_only",
        "one_run_id_consumed_in_record",
        "metadata_only_reconciliation_executed",
        "no_rtm_generation_or_reusable_blk_link",
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
        "execution_package_id",
        "operator_identity",
        "operator_approval_text_raw",
        "execution_scope",
        "selected_frontier",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "upstream_authority_request_hash",
        "upstream_preflight_package_hash",
        "upstream_finality_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "run_id",
        "execute_bounded_metadata_reconciliation",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *REQUIRED_TRUE_FLAGS,
        *REQUIRED_FALSE_FLAGS,
    }
)


def valid_bounded_metadata_reconciliation_execution_request(request_package: dict[str, Any], **overrides) -> dict[str, Any]:
    request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_RAW,
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": request_package["request_package_id"],
        "upstream_request_package_hash": request_package["request_package_hash"],
        "upstream_authority_request_hash": request_package["authority_request_hash"],
        "upstream_preflight_package_hash": request_package["upstream_preflight_package_hash"],
        "upstream_finality_package_hash": request_package["upstream_finality_package_hash"],
        "beo_id": request_package["beo_id"],
        "beb_id": request_package["beb_id"],
        "exact_trace_identities": list(request_package["exact_trace_identities"]),
        "run_id": RUN_ID,
        "execute_bounded_metadata_reconciliation": True,
        "requested_at": "2099-05-16T10:00:00+10:00",
        "expires_at": "2099-05-16T11:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in sorted(_ATTESTATION_KEYS)},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in REQUIRED_TRUE_FLAGS:
        request[flag] = True
    for flag in REQUIRED_FALSE_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def build_bounded_metadata_rtm_blk_link_reconciliation_execution(
    request_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    upstream = _validate_request_package(request_package)
    request = _validate_execution_request(execution_request, upstream)
    execution_request_hash = _canonical_hash(request)
    record = {
        "record_id": RECONCILIATION_RECORD_ID,
        "consumed_run_id": RUN_ID,
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "trace_identities": list(upstream["exact_trace_identities"]),
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_preflight_package_hash": upstream["upstream_preflight_package_hash"],
        "upstream_finality_package_hash": upstream["upstream_finality_package_hash"],
        "execution_request_hash": execution_request_hash,
        "metadata_hashes_reconciled": True,
        "mismatch_count": 0,
        "mismatches": [],
        "rtm_generated": False,
        "production_blk_link_executed": False,
        "drift_rejection_performed": False,
        "coverage_truth_established": False,
        "protected_body_reads": False,
    }
    record["record_hash"] = _canonical_hash(record)
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_RAW,
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "upstream_preflight_package_hash": upstream["upstream_preflight_package_hash"],
        "upstream_finality_package_hash": upstream["upstream_finality_package_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "run_id_consumed": RUN_ID,
        "execution_request_hash": execution_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "reconciliation_record_id": RECONCILIATION_RECORD_ID,
        "reconciliation_record": record,
        "reconciliation_record_hash": record["record_hash"],
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in REQUIRED_TRUE_FLAGS:
        package[flag] = True
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package must be a dictionary")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("request_package_hash"), "request_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in normalized.items() if key != "request_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("request_package_hash does not match submitted BLK-154 package")
    if submitted_hash != CANONICAL_BLK154_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-154 request package required")
    expected = {
        "request_status": BLK154_REQUEST_STATUS,
        "request_package_id": BLK154_REQUEST_PACKAGE_ID,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "request_future_bounded_metadata_reconciliation_approval": True,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"request_package {key} must be {value}")
    _required_hash(normalized.get("authority_request_hash"), "authority_request_hash")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    _required_exact_set(normalized.get("proof_obligations"), BLK154_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK154_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK154_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"request_package {flag} must remain false")
    return normalized


def _validate_execution_request(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"execution_request missing fields: {missing}")
    _scan_value_strings(
        {
            "operator_identity": request.get("operator_identity"),
            "operator_approval_text_raw": request.get("operator_approval_text_raw"),
            "execution_package_id": request.get("execution_package_id"),
            "execution_scope": request.get("execution_scope"),
            "selected_frontier": request.get("selected_frontier"),
        },
        "execution_request",
        allow_selected=True,
    )
    expected = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_RAW,
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "upstream_preflight_package_hash": upstream["upstream_preflight_package_hash"],
        "upstream_finality_package_hash": upstream["upstream_finality_package_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "run_id": RUN_ID,
    }
    for key, value in expected.items():
        if request.get(key) != value:
            if key == "operator_approval_text_raw":
                raise ValueError("operator_approval_text_raw must match exact BLK-SYSTEM-154-156 operator approval")
            raise ValueError(f"{key} must be {value}")
    if request.get("exact_trace_identities") != upstream.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-154 request package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    if request.get("execute_bounded_metadata_reconciliation") is not True:
        raise ValueError("execute_bounded_metadata_reconciliation must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("execution request must not be calendar-stale")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
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
    for flag in REQUIRED_TRUE_FLAGS:
        if request.get(flag) is not True:
            raise ValueError(f"{flag} must be true")
    for flag in REQUIRED_FALSE_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(request)
