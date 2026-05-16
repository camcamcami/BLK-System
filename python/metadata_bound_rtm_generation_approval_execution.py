"""BLK-SYSTEM-158 metadata-bound RTM generation approval + bounded execution.

This deterministic fixture consumes the exact BLK-SYSTEM-157 request-only
package, captures exact operator approval as execution preflight, assigns and
consumes one BLK-SYSTEM-158 run ID inside returned evidence, and emits a
metadata-only RTM generation record. It does not grant reusable production
blk-link, drift rejection, coverage truth, protected-body access, active-vault
filesystem scanning, signer/storage/ledger reuse, live tooling, or target/source
/Git mutation beyond this exact record-only evidence package.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_generation_decision_request import (
    CANONICAL_BLK156_RECONCILIATION_RECORD_HASH,
    CANONICAL_BLK156_REVIEW_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES as BLK157_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK157_PROOF_OBLIGATIONS,
    NEXT_FRONTIER as BLK157_NEXT_FRONTIER,
    NEXT_REQUIRED_AUTHORITY as BLK157_NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID as BLK157_REQUEST_PACKAGE_ID,
    REQUEST_SCOPE as BLK157_REQUEST_SCOPE,
    REQUEST_STATUS as BLK157_REQUEST_STATUS,
    REQUESTED_AUTHORITY as BLK157_REQUESTED_AUTHORITY,
    SELECTED_FRONTIER as BLK157_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK157_SIDE_EFFECT_FLAGS,
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

EXECUTION_STATUS = "METADATA_BOUND_RTM_GENERATION_APPROVAL_CAPTURED_AND_EXECUTED_FOR_EXACT_BLK157_REQUEST_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "METADATA-BOUND-RTM-GENERATION-APPROVAL-EXECUTION-158-001"
RTM_RECORD_ID = "METADATA-BOUND-RTM-GENERATION-RECORD-158-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-158-METADATA-BOUND-RTM-GENERATION-001"
RUN_ID = "RUN-BLK-SYSTEM-158-METADATA-BOUND-RTM-GENERATION-001"
SELECTED_FRONTIER = "metadata_bound_rtm_generation_approval_execution"
EXECUTION_SCOPE = "EXACT_BLK157_METADATA_BOUND_RTM_GENERATION_APPROVAL_AND_RECORD_ONLY_EXECUTION_NO_DRIFT_COVERAGE_PROTECTED_BODY"
NEXT_REQUIRED_AUTHORITY = "POST_METADATA_BOUND_RTM_GENERATION_RECONCILIATION_REQUIRED_NOT_GRANTED"
NEXT_FRONTIER = "NEXT_FRONTIER_POST_METADATA_BOUND_RTM_GENERATION_RECONCILIATION_NOT_GRANTED"
EXACT_OPERATOR_APPROVAL_TEXT_RAW = (
    "Approve METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-001 "
    "sha256:ed32e6e86952e0b67fe209115e7dba8fcf2334c218a6efbaeb69a5460cc8d556 "
    "for BLK-SYSTEM-158 exact metadata-bound RTM generation approval and bounded record-only execution."
)
CANONICAL_BLK157_REQUEST_PACKAGE_HASH = "sha256:ed32e6e86952e0b67fe209115e7dba8fcf2334c218a6efbaeb69a5460cc8d556"
CANONICAL_BLK157_DECISION_REQUEST_HASH = "sha256:06681a3744d08bb99d34864485ca83fa71d692de665e0d6ecf0a5dbb96d32fb1"

REQUIRED_TRUE_FLAGS = (
    "approval_capture_performed",
    "rtm_generation_approved",
    "rtm_generation_authorized",
    "rtm_generated",
    "metadata_bound_rtm_generation_executed",
    "rtm_record_emitted",
    "run_id_consumed_in_record",
)

REQUIRED_FALSE_FLAGS = (
    "approval_retargeting_or_scope_expansion",
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
    "APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
    "RUN_ID_REUSE_WITHOUT_SEPARATE_REPLAY_LEDGER_AUTHORITY",
    "RTM_GENERATION_BEYOND_EXACT_METADATA_BOUND_RECORD",
    "RTM_RECORD_MUTATION_BEYOND_RETURNED_EVIDENCE",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXISTING_HASH_BOUND_EVIDENCE",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION",
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
    "BLK157_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK157_DECISION_REQUEST_HASH_BOUND",
    "BLK156_REVIEW_HASH_BOUND_THROUGH_BLK157",
    "BLK155_RECONCILIATION_RECORD_HASH_BOUND_THROUGH_BLK157",
    "EXPLICIT_OPERATOR_APPROVAL_TEXT_MATCHES_EXACT_BLK157_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_BLK157_REQUEST",
    "RUN_ID_ASSIGNED_AND_CONSUMED_INSIDE_RECORD_ONLY_EVIDENCE",
    "METADATA_BOUND_RTM_RECORD_EMITTED_FOR_EXACT_TRACE_IDENTITIES",
    "EXECUTION_REQUEST_WINDOW_HASH_BOUND",
    "PROTECTED_BODY_NO_READ_COPY_PARSE_HASH_SCAN_GUARANTEE_BOUND",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "POST_GENERATION_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
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
        "next_frontier",
        "next_required_authority",
        "decision_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "request_package_hash",
        *BLK157_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_REQUEST_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "upstream_decision_request_hash",
        "approval_id",
        "operator_approval_text_raw",
        "run_id",
        "upstream_review_package_id",
        "upstream_review_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_reconciliation_record_id",
        "upstream_reconciliation_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "execute_metadata_bound_rtm_generation",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *REQUIRED_FALSE_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk157_request_reviewed",
        "explicit_operator_approval_captured_for_exact_request",
        "run_id_assigned_and_consumed_once_in_record",
        "metadata_bound_rtm_record_only",
        "trace_metadata_only_no_protected_body_copy",
        "drift_rejection_excluded",
        "coverage_truth_excluded",
        "reusable_blk_link_excluded",
        "active_vault_filesystem_reads_excluded",
        "protected_body_reads_excluded",
        "signer_storage_ledger_excluded",
        "target_source_git_mutation_excluded",
        "beb_dispatch_beo_closeout_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)


def valid_metadata_bound_rtm_generation_approval_execution_request(
    request_package: dict[str, Any], **overrides: Any
) -> dict[str, Any]:
    request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request_package["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": request_package["request_package_id"],
        "upstream_request_package_hash": request_package["request_package_hash"],
        "upstream_decision_request_hash": request_package["decision_request_hash"],
        "approval_id": APPROVAL_ID,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_RAW,
        "run_id": RUN_ID,
        "upstream_review_package_id": request_package["upstream_review_package_id"],
        "upstream_review_package_hash": request_package["upstream_review_package_hash"],
        "upstream_execution_package_id": request_package["upstream_execution_package_id"],
        "upstream_execution_package_hash": request_package["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": request_package["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": request_package["upstream_reconciliation_record_hash"],
        "beo_id": request_package["beo_id"],
        "beb_id": request_package["beb_id"],
        "exact_trace_identities": list(request_package["exact_trace_identities"]),
        "execute_metadata_bound_rtm_generation": True,
        "requested_at": "2099-05-16T13:10:00+10:00",
        "expires_at": "2099-05-16T13:40:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in sorted(_ATTESTATION_KEYS)},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def build_metadata_bound_rtm_generation_approval_execution(
    request_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    upstream = _validate_request_package(request_package)
    request = _validate_execution_request(execution_request, upstream)
    execution_request_hash = _canonical_hash(request)
    trace_identities = list(upstream["exact_trace_identities"])
    rtm_record = {
        "rtm_record_id": RTM_RECORD_ID,
        "generation_mode": "METADATA_BOUND_RTM_GENERATION_RECORD_ONLY",
        "metadata_bound_rtm_generation_executed": True,
        "consumed_run_id": RUN_ID,
        "approval_id": APPROVAL_ID,
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_decision_request_hash": upstream["decision_request_hash"],
        "upstream_review_package_id": upstream["upstream_review_package_id"],
        "upstream_review_package_hash": upstream["upstream_review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": upstream["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": upstream["upstream_reconciliation_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "trace_identities": trace_identities,
        "recorded_at": request["requested_at"],
        "active_vault_filesystem_read_performed": False,
        "protected_body_reads": False,
        "rtm_drift_rejection_performed": False,
        "coverage_truth_established": False,
        "reusable_blk_link_authority_granted": False,
        "production_blk_link_executed": False,
        "public_ledger_mutation": False,
    }
    rtm_record["rtm_record_hash"] = _canonical_hash(
        {key: value for key, value in rtm_record.items() if key != "rtm_record_hash"}
    )
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_status": upstream["request_status"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_decision_request_hash": upstream["decision_request_hash"],
        "approval_id": APPROVAL_ID,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_RAW,
        "run_id_consumed": RUN_ID,
        "execution_request_hash": execution_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "upstream_review_package_id": upstream["upstream_review_package_id"],
        "upstream_review_package_hash": upstream["upstream_review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": upstream["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": upstream["upstream_reconciliation_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "rtm_record_id": RTM_RECORD_ID,
        "rtm_record": rtm_record,
        "rtm_record_hash": rtm_record["rtm_record_hash"],
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "next_frontier": NEXT_FRONTIER,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in REQUIRED_TRUE_FLAGS:
        package[flag] = True
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"request_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"request_package missing field {missing[0]!r}")
    submitted_hash = _required_hash(package.get("request_package_hash"), "request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("request_package_hash does not match submitted BLK-157 package")
    if submitted_hash != CANONICAL_BLK157_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-157 request package required")
    if _required_hash(package.get("decision_request_hash"), "decision_request_hash") != CANONICAL_BLK157_DECISION_REQUEST_HASH:
        raise ValueError("canonical BLK-157 decision request hash required")
    expected = {
        "request_status": BLK157_REQUEST_STATUS,
        "request_package_id": BLK157_REQUEST_PACKAGE_ID,
        "request_scope": BLK157_REQUEST_SCOPE,
        "selected_frontier": BLK157_SELECTED_FRONTIER,
        "requested_authority": BLK157_REQUESTED_AUTHORITY,
        "upstream_review_package_hash": CANONICAL_BLK156_REVIEW_PACKAGE_HASH,
        "upstream_reconciliation_record_hash": CANONICAL_BLK156_RECONCILIATION_RECORD_HASH,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "next_frontier": BLK157_NEXT_FRONTIER,
        "next_required_authority": BLK157_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("canonical BLK-157 request package required")
    for flag in ("expired", "replayed", "stale"):
        if package.get(flag) is not False:
            raise ValueError(f"BLK-157 request package must not be {flag}")
    for flag in BLK157_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"request_package {flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    _required_exact_set(package.get("proof_obligations"), BLK157_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK157_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    _parse_timestamp(package.get("requested_at"), "BLK-157 requested_at")
    _parse_timestamp(package.get("expires_at"), "BLK-157 expires_at")
    return deepcopy(package)


def _validate_execution_request(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution request must be a dictionary")
    unknown = sorted(set(request) - _EXECUTION_REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"execution request missing field {missing[0]!r}")
    _scan_value_strings({"operator_identity": request.get("operator_identity")}, "execution_request", allow_selected=True)
    _require_exact_or_reject_laundering(request, "execution_package_id", EXECUTION_PACKAGE_ID)
    _require_exact_or_reject_laundering(request, "execution_scope", EXECUTION_SCOPE)
    _require_exact_or_reject_laundering(request, "selected_frontier", SELECTED_FRONTIER)
    _require_exact_or_reject_laundering(request, "approval_id", APPROVAL_ID)
    _require_exact_or_reject_laundering(request, "run_id", RUN_ID)
    if request.get("operator_approval_text_raw") != EXACT_OPERATOR_APPROVAL_TEXT_RAW:
        _scan_value_strings({"operator_approval_text_raw": request.get("operator_approval_text_raw")}, "execution_request", allow_selected=True)
        raise ValueError("operator approval text must match exact BLK-SYSTEM-158 approval sentence")
    expected_from_upstream = {
        "operator_identity": upstream["operator_identity"],
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_decision_request_hash": upstream["decision_request_hash"],
        "upstream_review_package_id": upstream["upstream_review_package_id"],
        "upstream_review_package_hash": upstream["upstream_review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_reconciliation_record_id": upstream["upstream_reconciliation_record_id"],
        "upstream_reconciliation_record_hash": upstream["upstream_reconciliation_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": upstream["exact_trace_identities"],
    }
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    for key, value in expected_from_upstream.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must match BLK-157 request package")
    if request.get("execute_metadata_bound_rtm_generation") is not True:
        raise ValueError("execute_metadata_bound_rtm_generation must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    upstream_requested_at = _parse_timestamp(upstream.get("requested_at"), "BLK-157 requested_at")
    upstream_expires_at = _parse_timestamp(upstream.get("expires_at"), "BLK-157 expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at < upstream_requested_at:
        raise ValueError("execution request must not predate BLK-157 request")
    if expires_at > upstream_expires_at:
        raise ValueError("execution request window must end within BLK-157 request expiry")
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
        raise ValueError(f"operator_attestation missing field {missing_attestation[0]!r}")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
    _required_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in REQUIRED_FALSE_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(request)


def _require_exact_or_reject_laundering(request: dict[str, Any], key: str, expected: str) -> None:
    if request.get(key) == expected:
        return
    _scan_value_strings({key: request.get(key)}, "execution_request", allow_selected=True)
    raise ValueError(f"{key} must be {expected}")
