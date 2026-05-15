"""BLK-SYSTEM-143 metadata-bound RTM-generation execution package.

This deterministic fixture consumes the exact BLK-SYSTEM-142 RTM-generation
authority request, captures exact operator approval as preflight, assigns and
consumes one BLK-SYSTEM-143 run ID inside the returned evidence, and emits a
metadata-only RTM generation record. It does not reject drift, establish coverage
truth, run reusable production blk-link, read active-vault files, read/copy/parse
/hash/scan protected requirement bodies, mutate target/source/Git state, run
BLK-pipe/BLK-test/Codex/tooling, perform signer/storage/ledger behavior, or
claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_generation_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK142_AUTHORITY_REQUEST_PACKAGE_ID,
    CANONICAL_BLK141_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES as BLK142_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK142_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK142_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK142_REQUEST_SCOPE,
    REQUEST_STATUS as BLK142_REQUEST_STATUS,
    REQUESTED_AUTHORITY as BLK142_REQUESTED_AUTHORITY,
    SELECTED_FRONTIER as BLK142_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK142_SIDE_EFFECT_FLAGS,
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

EXECUTION_STATUS = "METADATA_BOUND_RTM_GENERATION_EXECUTED_FOR_EXACT_BLK142_APPROVAL_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "RTM-GENERATION-EXECUTION-143-001"
RTM_RECORD_ID = "RTM-GENERATION-RECORD-143-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-142-RTM-GENERATION-001"
RUN_ID = "RUN-BLK-SYSTEM-143-RTM-GENERATION-001"
SELECTED_FRONTIER = "metadata_bound_rtm_generation_execution_record"
EXECUTION_SCOPE = "EXACT_METADATA_BOUND_RTM_GENERATION_FOR_BLK142_REQUEST_RECORD_ONLY_NO_DRIFT_COVERAGE_TRUTH_PROTECTED_BODY"
NEXT_REQUIRED_AUTHORITY = "POST_RTM_GENERATION_RECONCILIATION_REQUIRED_NOT_STARTED"
EXACT_OPERATOR_APPROVAL_TEXT = (
    "Approve RTM-GENERATION-AUTHORITY-REQUEST-142-001 for BLK-SYSTEM-143 "
    "exact metadata-bound RTM generation execution package only."
)
CANONICAL_BLK142_AUTHORITY_REQUEST_PACKAGE_HASH = "sha256:62787171d735723aa9b1867b1fea8b0acdc81d6ff4d99faf7daad7a06bb2d172"
CANONICAL_BLK142_AUTHORITY_REQUEST_HASH = "sha256:277ed9ed2a6d8a3d4a17ae97bc2f1d273907fafd50ab299b29977abc7f4f2365"

SIDE_EFFECT_FLAGS = (
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
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXACT_BLK141_RECONCILIATION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
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
    "BLK142_AUTHORITY_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK142_AUTHORITY_REQUEST_HASH_BOUND",
    "BLK141_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK142",
    "EXPLICIT_OPERATOR_APPROVAL_TEXT_MATCHES_EXACT_BLK142_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_BLK142_REQUEST",
    "RUN_ID_ASSIGNED_AND_CONSUMED_INSIDE_RECORD_ONLY_EVIDENCE",
    "METADATA_BOUND_RTM_RECORD_EMITTED_FOR_EXACT_TRACE_IDENTITIES",
    "PROTECTED_BODY_NO_READ_COPY_PARSE_HASH_SCAN_GUARANTEE_BOUND",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "POST_EXECUTION_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "requested_authority",
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
        "approval_capture_performed",
        "rtm_generation_approved",
        "rtm_generated",
        "future_run_id_reserved",
        "future_run_id_consumed",
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
        *BLK142_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_REQUEST_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_authority_request_hash",
        "approval_id",
        "operator_approval_text_raw",
        "run_id",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_comparison_record_id",
        "upstream_comparison_record_hash",
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
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk142_request_reviewed",
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


def build_metadata_bound_rtm_generation_execution_package(
    authority_request_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Emit one exact BLK-SYSTEM-143 metadata-bound RTM generation record."""

    upstream = _validate_authority_request_package(authority_request_package)
    request = _validate_execution_request(execution_request, upstream)
    trace_identities = list(upstream["exact_trace_identities"])
    execution_request_hash = _canonical_hash(request)
    rtm_record = {
        "rtm_record_id": RTM_RECORD_ID,
        "generation_mode": "METADATA_BOUND_RTM_GENERATION_RECORD_ONLY",
        "consumed_run_id": RUN_ID,
        "approval_id": APPROVAL_ID,
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "upstream_reconciliation_package_id": upstream["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["upstream_reconciliation_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_comparison_record_id": upstream["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": upstream["upstream_comparison_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "trace_identities": trace_identities,
        "recorded_at": request["requested_at"],
        "active_vault_filesystem_read_performed": False,
        "protected_body_reads": False,
        "rtm_drift_rejection_performed": False,
        "coverage_truth_established": False,
        "reusable_blk_link_authority_granted": False,
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
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_status": upstream["request_status"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "approval_id": APPROVAL_ID,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT,
        "approval_capture_performed": True,
        "rtm_generation_approved": True,
        "run_id_consumed": RUN_ID,
        "run_id_consumed_in_record": True,
        "execution_request_hash": execution_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "upstream_reconciliation_package_id": upstream["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["upstream_reconciliation_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_comparison_record_id": upstream["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": upstream["upstream_comparison_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "metadata_bound_rtm_generation_executed": True,
        "rtm_record_id": RTM_RECORD_ID,
        "rtm_record": rtm_record,
        "rtm_record_hash": rtm_record["rtm_record_hash"],
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
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


def _validate_authority_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("authority request package must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"authority request package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"authority request package missing field {missing[0]!r}")
    submitted_hash = _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-142 package")
    if submitted_hash != CANONICAL_BLK142_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-142 authority request package required")
    if _required_hash(package.get("authority_request_hash"), "authority_request_hash") != CANONICAL_BLK142_AUTHORITY_REQUEST_HASH:
        raise ValueError("canonical BLK-142 authority request hash required")
    expected = {
        "request_status": BLK142_REQUEST_STATUS,
        "authority_request_package_id": BLK142_AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": BLK142_REQUEST_SCOPE,
        "selected_frontier": BLK142_SELECTED_FRONTIER,
        "requested_authority": BLK142_REQUESTED_AUTHORITY,
        "upstream_reconciliation_package_hash": CANONICAL_BLK141_RECONCILIATION_PACKAGE_HASH,
        "metadata_hashes_match": True,
        "request_future_exact_metadata_bound_rtm_generation_approval": True,
        "approval_capture_performed": False,
        "rtm_generation_approved": False,
        "rtm_generated": False,
        "future_run_id_reserved": False,
        "future_run_id_consumed": False,
        "next_required_authority": BLK142_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("canonical BLK-142 authority request package required")
    for flag in ("expired", "replayed", "stale"):
        if package.get(flag) is not False:
            raise ValueError(f"BLK-142 authority request package must not be {flag}")
    for flag in BLK142_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"authority request package {flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    _required_exact_set(package.get("proof_obligations"), BLK142_PROOF_OBLIGATIONS, "authority request proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK142_EXCLUDED_AUTHORITIES, "authority request excluded_authorities")
    _parse_timestamp(package.get("requested_at"), "authority request requested_at")
    _parse_timestamp(package.get("expires_at"), "authority request expires_at")
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
    if request.get("operator_approval_text_raw") != EXACT_OPERATOR_APPROVAL_TEXT:
        _scan_value_strings({"operator_approval_text_raw": request.get("operator_approval_text_raw")}, "execution_request", allow_selected=True)
        raise ValueError("operator approval text must match exact BLK-142 approval sentence")
    expected_from_upstream = {
        "operator_identity": upstream["operator_identity"],
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "upstream_reconciliation_package_id": upstream["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["upstream_reconciliation_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_comparison_record_id": upstream["upstream_comparison_record_id"],
        "upstream_comparison_record_hash": upstream["upstream_comparison_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": upstream["exact_trace_identities"],
    }
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    for key, value in expected_from_upstream.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must match BLK-142 authority request package")
    if request.get("execute_metadata_bound_rtm_generation") is not True:
        raise ValueError("execute_metadata_bound_rtm_generation must be true")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    upstream_requested_at = _parse_timestamp(upstream.get("requested_at"), "BLK-142 requested_at")
    upstream_expires_at = _parse_timestamp(upstream.get("expires_at"), "BLK-142 expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at < upstream_requested_at:
        raise ValueError("execution request must not predate BLK-142 request")
    if expires_at > upstream_expires_at:
        raise ValueError("execution request window must end within BLK-142 request expiry")
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
    for flag in SIDE_EFFECT_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(request)


def _require_exact_or_reject_laundering(request: dict[str, Any], key: str, expected: str) -> None:
    if request.get(key) == expected:
        return
    _scan_value_strings({key: request.get(key)}, "execution_request", allow_selected=True)
    raise ValueError(f"{key} must be {expected}")
