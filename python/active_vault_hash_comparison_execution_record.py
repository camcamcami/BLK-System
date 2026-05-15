"""BLK-SYSTEM-140 active-vault hash-comparison execution record.

This deterministic fixture consumes the exact BLK-SYSTEM-139 approval capture and
reserved run ID to compare caller-supplied metadata/hash records against the
approved trace identities. It emits record-only comparison evidence. It does not
read active-vault files, read/copy/parse/hash/scan protected requirement bodies,
generate RTM, reject drift, establish coverage truth, run reusable production
blk-link, mutate source/Git state, run tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_approval_capture import (
    APPROVAL_CAPTURE_PACKAGE_ID as BLK139_APPROVAL_CAPTURE_PACKAGE_ID,
    APPROVAL_ID as BLK139_APPROVAL_ID,
    FUTURE_RUN_ID as BLK139_FUTURE_RUN_ID,
    STATUS as BLK139_STATUS,
)
from active_vault_hash_comparison_decision_package import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

EXECUTION_STATUS = "ACTIVE_VAULT_HASH_COMPARISON_EXECUTED_FOR_EXACT_BLK139_APPROVAL_RECORD_ONLY"
COMPARISON_EXECUTION_PACKAGE_ID = "ACTIVE-VAULT-HASH-COMPARISON-EXECUTION-140-001"
COMPARISON_RECORD_ID = "ACTIVE-VAULT-HASH-COMPARISON-RECORD-140-001"
EXECUTION_SCOPE = "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_EXECUTION_RECORD_ONLY"
SELECTED_FRONTIER = "active_vault_hash_comparison_metadata_hash_only_execution_record"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-140-ACTIVE-VAULT-HASH-COMPARISON-001"
NEXT_FRONTIER = "NEXT_FRONTIER_POST_ACTIVE_VAULT_HASH_COMPARISON_RECONCILIATION_NOT_GRANTED"
CANONICAL_BLK139_APPROVAL_CAPTURE_PACKAGE_HASH = "sha256:695ed2b919982566d97b10244dd0b352154afe5b4fe5ea97b84173757fda4bec"
METADATA_SOURCE = "CALLER_SUPPLIED_ACTIVE_VAULT_HASH_METADATA_ONLY"
MATCH_RESULT = "ACTIVE_VAULT_METADATA_HASHES_MATCH_RECORDED_NOT_DRIFT_DECISION"
MISMATCH_RESULT = "ACTIVE_VAULT_METADATA_HASH_MISMATCH_RECORDED_NOT_DRIFT_DECISION"

SIDE_EFFECT_FLAGS = (
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
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
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXACT_APPROVED_IDENTITIES",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
    "REUSABLE_ACTIVE_VAULT_COMPARISON_AUTHORITY",
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
    "BLK139_APPROVAL_CAPTURE_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK138_AUTHORITY_REQUEST_BOUND_THROUGH_BLK139",
    "APPROVAL_ID_BOUND_TO_EXACT_BLK139_DECISION",
    "RUN_ID_CONSUMED_ONCE_IN_RECORD_ONLY_EVIDENCE",
    "COMPARISON_LIMITED_TO_APPROVED_TRACE_IDENTITIES",
    "ACTIVE_METADATA_RECORDS_MATCH_EXACT_IDENTITY_SET",
    "METADATA_HASH_COMPARISON_RECORDED_WITHOUT_DRIFT_DECISION",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_COMPARISON",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "POST_COMPARISON_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
}

_APPROVAL_PACKAGE_REQUIRED_KEYS = frozenset(
    {
        "approval_capture_status",
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
        "future_metadata_hash_only_active_vault_comparison_approved",
        "future_run_id_consumed",
        "active_vault_hash_comparison_performed",
        "next_required_authority",
        "approval_decision_hash",
        "decided_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "approval_capture_package_hash",
    }
)

_REQUEST_ALLOWED_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_to_consume",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "active_metadata_records",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "future_run_id_consumed",
        "active_vault_hash_comparison_performed",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_REQUEST_REQUIRED_KEYS = _REQUEST_ALLOWED_KEYS - {"future_run_id_consumed", "active_vault_hash_comparison_performed"}

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk139_approval_reviewed",
        "future_run_id_consumed_once_in_record",
        "metadata_hash_only_comparison_scope_preserved",
        "no_active_vault_filesystem_read",
        "no_protected_body_reads",
        "no_protected_body_copy_parse_hash_scan",
        "no_rtm_generation",
        "no_drift_rejection_or_authoritative_drift_decision",
        "no_coverage_truth",
        "no_reusable_blk_link_authority",
        "no_beb_dispatch_or_beo_closeout",
        "no_signer_storage_ledger_side_effects",
        "no_target_source_git_mutation",
        "no_blk_pipe_blk_test_codex_tooling",
        "no_production_isolation_claim",
    }
)

_METADATA_RECORD_KEYS = frozenset(
    {
        "kind",
        "id",
        "version_hash",
        "metadata_source",
        "body_included",
        "body_read",
        "body_copied",
        "body_hashed",
        "protected_path_accessed",
    }
)

_METADATA_FALSE_FLAGS = ("body_included", "body_read", "body_copied", "body_hashed", "protected_path_accessed")


def build_active_vault_hash_comparison_execution_record(
    approval_capture_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    approval = _validate_approval_capture_package(approval_capture_package)
    request = _validate_execution_request(execution_request, approval)
    expected = _expected_trace_map(approval["exact_trace_identities"])
    observed = _validate_active_metadata_records(request["active_metadata_records"], expected)
    comparison_record = _build_comparison_record(approval, request, expected, observed)
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": COMPARISON_EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_decision_package_id": approval["upstream_decision_package_id"],
        "upstream_decision_package_hash": approval["upstream_decision_package_hash"],
        "upstream_reconciliation_package_id": approval["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": approval["upstream_reconciliation_package_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": list(approval["exact_trace_identities"]),
        "active_metadata_records": deepcopy(observed),
        "active_vault_hash_comparison_performed": True,
        "metadata_hashes_match": comparison_record["metadata_hashes_match"],
        "comparison_result": MATCH_RESULT if comparison_record["metadata_hashes_match"] else MISMATCH_RESULT,
        "comparison_record_id": COMPARISON_RECORD_ID,
        "comparison_record": comparison_record,
        "comparison_record_hash": comparison_record["comparison_record_hash"],
        "execution_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_frontier": NEXT_FRONTIER,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash(package)
    return package


def _validate_approval_capture_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("approval capture package must be a dictionary")
    missing = sorted(_APPROVAL_PACKAGE_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"approval capture package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("approval_capture_package_hash"), "approval_capture_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in package.items() if key != "approval_capture_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("approval_capture_package_hash does not match submitted BLK-139 package")
    if submitted_hash != CANONICAL_BLK139_APPROVAL_CAPTURE_PACKAGE_HASH:
        raise ValueError("canonical BLK-139 approval package required")
    if package.get("approval_capture_package_id") != BLK139_APPROVAL_CAPTURE_PACKAGE_ID:
        raise ValueError("approval_capture_package_id must match exact BLK-139 package")
    if package.get("approval_capture_status") != BLK139_STATUS:
        raise ValueError("approval_capture_status must match BLK-139 status")
    if package.get("approval_id") != BLK139_APPROVAL_ID:
        raise ValueError("approval_id must match exact BLK-139 approval")
    if package.get("future_run_id") != BLK139_FUTURE_RUN_ID:
        raise ValueError("future_run_id must match exact BLK-140 run ID")
    if package.get("future_metadata_hash_only_active_vault_comparison_approved") is not True:
        raise ValueError("BLK-139 approval must approve the exact future comparison")
    if package.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-139 future run ID must not already be consumed")
    if package.get("active_vault_hash_comparison_performed") is not False:
        raise ValueError("BLK-139 must not have performed comparison")
    if package.get("expired") is not False or package.get("replayed") is not False or package.get("stale") is not False:
        raise ValueError("BLK-139 approval package must not be expired, replayed, or stale")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_execution_request(request: Any, approval: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_REQUIRED_KEYS - set(request))
    if missing:
        raise ValueError(f"execution request missing fields: {missing}")
    scan_request = {
        key: value
        for key, value in request.items()
        if key not in {"operator_attestation", "proof_obligations", "excluded_authorities", "active_metadata_records"}
    }
    _scan_value_strings(scan_request, "execution_request", allow_selected=True)
    expected_scalars = {
        "execution_package_id": COMPARISON_EXECUTION_PACKAGE_ID,
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_to_consume": RUN_ID_CONSUMED,
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
    }
    for key, expected in expected_scalars.items():
        if request.get(key) != expected:
            raise ValueError(f"{key} must be {expected!r}")
    if request.get("operator_identity") != approval.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-139 approval package")
    if request.get("exact_trace_identities") != approval.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-139 approval package")
    _validate_exact_trace_identities(request.get("exact_trace_identities"))
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    approval_decided_at = _parse_timestamp(approval.get("decided_at"), "approval decided_at")
    approval_expires_at = _parse_timestamp(approval.get("expires_at"), "approval expires_at")
    if requested_at < approval_decided_at:
        raise ValueError("requested_at must be at or after approval decided_at")
    if requested_at >= approval_expires_at:
        raise ValueError("requested_at must be before approval expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at > approval_expires_at:
        raise ValueError("expires_at must not exceed approval expires_at")
    if request.get("expired") is not False:
        raise ValueError("execution request must not be expired")
    if request.get("replayed") is not False:
        raise ValueError("execution request must not be replayed")
    if request.get("stale") is not False:
        raise ValueError("execution request must not be stale")
    if request.get("future_run_id_consumed") is True:
        raise ValueError("future_run_id_consumed must remain false before execution")
    if request.get("active_vault_hash_comparison_performed") is True:
        raise ValueError("active_vault_hash_comparison_performed must remain false before execution")
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


def _expected_trace_map(identities: list[str]) -> dict[tuple[str, str], str]:
    expected: dict[tuple[str, str], str] = {}
    for identity in identities:
        kind, artifact_id, version_hash = _parse_trace_identity(identity)
        expected[(kind, artifact_id)] = version_hash
    return expected


def _parse_trace_identity(identity: str) -> tuple[str, str, str]:
    if not isinstance(identity, str):
        raise ValueError("trace identity must be a string")
    parts = identity.split(":", 2)
    if len(parts) != 3:
        raise ValueError("trace identity must be KIND:ID:sha256")
    kind, artifact_id, version_hash = parts
    return kind, artifact_id, _required_hash(version_hash, "version_hash")


def _validate_active_metadata_records(records: Any, expected: dict[tuple[str, str], str]) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records:
        raise ValueError("active_metadata_records must be a non-empty list")
    observed_keys: set[tuple[str, str]] = set()
    normalized = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("active_metadata_records must contain objects")
        unknown = sorted(set(record) - _METADATA_RECORD_KEYS)
        if unknown:
            raise ValueError(f"unexpected metadata field {unknown[0]!r}")
        missing = sorted(_METADATA_RECORD_KEYS - set(record))
        if missing:
            raise ValueError(f"metadata record missing fields: {missing}")
        kind = _required_ascii_text(record.get("kind"), "kind")
        artifact_id = _required_ascii_text(record.get("id"), "id")
        key = (kind, artifact_id)
        if key in observed_keys:
            raise ValueError("active_metadata_records must not contain duplicates")
        observed_keys.add(key)
        if key not in expected:
            raise ValueError("metadata kind/id must match approved trace identity")
        version_hash = _required_hash(record.get("version_hash"), "version_hash")
        if record.get("metadata_source") != METADATA_SOURCE:
            raise ValueError(f"metadata_source must be {METADATA_SOURCE!r}")
        for flag in _METADATA_FALSE_FLAGS:
            if record.get(flag) is not False:
                raise ValueError(f"{flag} must remain false")
        normalized.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
                "metadata_source": METADATA_SOURCE,
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "protected_path_accessed": False,
            }
        )
    if observed_keys != set(expected):
        raise ValueError("active_metadata_records must match exact trace identity set")
    return normalized


def _build_comparison_record(
    approval: dict[str, Any], request: dict[str, Any], expected: dict[tuple[str, str], str], observed: list[dict[str, Any]]
) -> dict[str, Any]:
    matches = []
    mismatches = []
    for record in observed:
        key = (record["kind"], record["id"])
        expected_hash = expected[key]
        observed_hash = record["version_hash"]
        row = {
            "kind": record["kind"],
            "id": record["id"],
            "expected_version_hash": expected_hash,
            "observed_version_hash": observed_hash,
        }
        if observed_hash == expected_hash:
            matches.append(row)
        else:
            mismatches.append(row)
    metadata_hashes_match = not mismatches
    comparison_record = {
        "comparison_record_id": COMPARISON_RECORD_ID,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "consumed_run_id": RUN_ID_CONSUMED,
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": list(approval["exact_trace_identities"]),
        "active_metadata_records": deepcopy(observed),
        "metadata_hashes_match": metadata_hashes_match,
        "matches": matches,
        "mismatches": mismatches,
        "comparison_result": MATCH_RESULT if metadata_hashes_match else MISMATCH_RESULT,
        "recorded_at": request["requested_at"],
        "active_vault_hash_comparison_performed": True,
        "future_run_id_consumed": True,
        "active_vault_filesystem_read_performed": False,
        "protected_body_reads": False,
        "protected_body_hashing_attempted": False,
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
        "drift_decision_made": False,
        "coverage_truth_established": False,
        "public_ledger_mutation": False,
    }
    comparison_record["comparison_record_hash"] = _canonical_hash(comparison_record)
    return comparison_record


def _required_ascii_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or not value.isascii():
        raise ValueError(f"{field} must be a non-empty ASCII string")
    _scan_value_strings(value, field, allow_selected=True)
    return value
