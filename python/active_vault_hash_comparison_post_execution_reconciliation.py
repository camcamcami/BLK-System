"""BLK-SYSTEM-141 post active-vault hash-comparison reconciliation.

This deterministic fixture consumes BLK-SYSTEM-140 record-only comparison evidence
and reconciles whether the metadata/hash comparison is clean or mismatch-bearing.
It names the next single frontier without granting it. It does not read active
vault files, read/copy/parse/hash/scan protected requirement bodies, generate RTM,
reject drift, establish coverage truth, run reusable production blk-link, mutate
source/Git state, run tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_decision_package import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from active_vault_hash_comparison_execution_record import (
    COMPARISON_EXECUTION_PACKAGE_ID as BLK140_EXECUTION_PACKAGE_ID,
    COMPARISON_RECORD_ID as BLK140_COMPARISON_RECORD_ID,
    EXECUTION_STATUS as BLK140_EXECUTION_STATUS,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

RECONCILIATION_STATUS = "ACTIVE_VAULT_HASH_COMPARISON_POST_EXECUTION_RECONCILED_FOR_EXACT_BLK140_RECORD_ONLY"
RECONCILIATION_PACKAGE_ID = "ACTIVE-VAULT-HASH-COMPARISON-POST-EXECUTION-RECONCILIATION-141-001"
RECONCILIATION_SCOPE = "POST_ACTIVE_VAULT_HASH_COMPARISON_RECONCILIATION_RECORD_ONLY"
SELECTED_FRONTIER = "active_vault_hash_comparison_post_execution_reconciliation"
CANONICAL_BLK140_EXECUTION_PACKAGE_HASH = "sha256:85aa984f453d6edd8959beb51178996a9e210ba9dfbeb0627fbf75fbc5a538c8"
CLEAN_RECONCILIATION_RESULT = "CLEAN_METADATA_HASH_COMPARISON_RECONCILED_NEXT_RTM_AUTHORITY_REQUEST_NOT_GRANTED"
MISMATCH_RECONCILIATION_RESULT = "MISMATCH_METADATA_HASH_COMPARISON_RECONCILED_NOT_DRIFT_REJECTION"
NEXT_FRONTIER_CLEAN = "NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_AUTHORITY_REQUEST_NOT_GRANTED"
NEXT_FRONTIER_MISMATCH = "NEXT_FRONTIER_METADATA_HASH_MISMATCH_REMEDIATION_DECISION_NOT_GRANTED"

SIDE_EFFECT_FLAGS = (
    "next_frontier_granted",
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
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXACT_BLK140_RECORD",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
    "REUSABLE_ACTIVE_VAULT_COMPARISON_AUTHORITY",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "RUNTIME_RTM_GENERATION",
    "RTM_GENERATION_APPROVAL_CAPTURE",
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
    "BLK140_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK139_APPROVAL_CAPTURE_BOUND_THROUGH_BLK140",
    "COMPARISON_RECORD_HASH_RECOMPUTED_AND_BOUND",
    "METADATA_HASH_MATCH_OR_MISMATCH_RECONCILED_WITHOUT_DRIFT_DECISION",
    "CLEAN_COMPARISON_CAN_ONLY_NAME_REQUEST_FRONTIER_NOT_GRANT_AUTHORITY",
    "MISMATCH_COMPARISON_CAN_ONLY_NAME_REMEDIATION_DECISION_NOT_DRIFT_REJECTION",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_RECONCILIATION",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "ONE_NEXT_FRONTIER_NAMED_WITH_AUTHORITY_NOT_GRANTED",
}

_EXECUTION_REQUIRED_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_consumed",
        "future_run_id_consumed",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_decision_package_id",
        "upstream_decision_package_hash",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "active_metadata_records",
        "active_vault_hash_comparison_performed",
        "metadata_hashes_match",
        "comparison_result",
        "comparison_record_id",
        "comparison_record",
        "comparison_record_hash",
        "execution_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "next_frontier",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "execution_package_hash",
    }
)

_CONTEXT_ALLOWED_KEYS = frozenset(
    {
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
        "metadata_hashes_match_observed",
        "reconciled_at",
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
        "exact_blk140_execution_reviewed",
        "comparison_record_hash_verified",
        "reconciliation_only_not_authority_request",
        "metadata_match_or_mismatch_interpreted_without_drift_decision",
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


def build_active_vault_hash_comparison_post_execution_reconciliation(
    execution_package: dict[str, Any], reconciliation_context: dict[str, Any]
) -> dict[str, Any]:
    execution = _validate_execution_package(execution_package)
    context = _validate_reconciliation_context(reconciliation_context, execution)
    metadata_hashes_match = execution["metadata_hashes_match"]
    mismatches = deepcopy(execution["comparison_record"].get("mismatches", []))
    result = CLEAN_RECONCILIATION_RESULT if metadata_hashes_match else MISMATCH_RECONCILIATION_RESULT
    next_frontier = NEXT_FRONTIER_CLEAN if metadata_hashes_match else NEXT_FRONTIER_MISMATCH
    package = {
        "reconciliation_status": RECONCILIATION_STATUS,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_comparison_record_id": execution["comparison_record_id"],
        "upstream_comparison_record_hash": execution["comparison_record_hash"],
        "upstream_approval_capture_package_id": execution["approval_capture_package_id"],
        "upstream_approval_capture_package_hash": execution["approval_capture_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(execution["exact_trace_identities"]),
        "metadata_hashes_match": metadata_hashes_match,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "reconciliation_result": result,
        "recommended_next_frontier": next_frontier,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["next_frontier_granted"] = False
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _validate_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("execution package must be a dictionary")
    missing = sorted(_EXECUTION_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"execution package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-140 package")
    if submitted_hash != CANONICAL_BLK140_EXECUTION_PACKAGE_HASH and package.get("metadata_hashes_match") is not False:
        raise ValueError("canonical BLK-140 execution package required")
    if package.get("execution_status") != BLK140_EXECUTION_STATUS:
        raise ValueError("execution_status must match BLK-140 execution status")
    if package.get("execution_package_id") != BLK140_EXECUTION_PACKAGE_ID:
        raise ValueError("execution_package_id must match exact BLK-140 package")
    if package.get("comparison_record_id") != BLK140_COMPARISON_RECORD_ID:
        raise ValueError("comparison_record_id must match exact BLK-140 record")
    if package.get("future_run_id_consumed") is not True:
        raise ValueError("future_run_id_consumed must be true in BLK-140 record")
    if package.get("active_vault_hash_comparison_performed") is not True:
        raise ValueError("BLK-140 comparison must be performed")
    if package.get("expired") is not False or package.get("replayed") is not False or package.get("stale") is not False:
        raise ValueError("BLK-140 execution package must not be expired, replayed, or stale")
    comparison_record = package.get("comparison_record")
    if not isinstance(comparison_record, dict):
        raise ValueError("comparison_record must be a dictionary")
    record_hash = _required_hash(package.get("comparison_record_hash"), "comparison_record_hash")
    actual_record_hash = _canonical_hash({key: value for key, value in comparison_record.items() if key != "comparison_record_hash"})
    if comparison_record.get("comparison_record_hash") != record_hash or record_hash != actual_record_hash:
        raise ValueError("comparison_record_hash does not match submitted BLK-140 comparison record")
    if comparison_record.get("metadata_hashes_match") != package.get("metadata_hashes_match"):
        raise ValueError("comparison record metadata_hashes_match must match package")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_reconciliation_context(context: Any, execution: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("reconciliation context must be a dictionary")
    unknown = sorted(set(context) - _CONTEXT_ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_CONTEXT_ALLOWED_KEYS - set(context))
    if missing:
        raise ValueError(f"reconciliation context missing fields: {missing}")
    scan_context = {
        key: value
        for key, value in context.items()
        if key not in {"operator_attestation", "proof_obligations", "excluded_authorities"}
    }
    _scan_value_strings(scan_context, "reconciliation_context", allow_selected=True)
    expected_scalars = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_comparison_record_id": execution["comparison_record_id"],
        "upstream_comparison_record_hash": execution["comparison_record_hash"],
        "upstream_approval_capture_package_id": execution["approval_capture_package_id"],
        "upstream_approval_capture_package_hash": execution["approval_capture_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
    }
    for key, expected in expected_scalars.items():
        if context.get(key) != expected:
            raise ValueError(f"{key} must match BLK-140 execution package")
    if context.get("operator_identity") != execution.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-140 execution package")
    if context.get("exact_trace_identities") != execution.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-140 execution package")
    if context.get("metadata_hashes_match_observed") != execution.get("metadata_hashes_match"):
        raise ValueError("metadata_hashes_match_observed must match BLK-140 execution package")
    _validate_exact_trace_identities(context.get("exact_trace_identities"))
    _parse_timestamp(context.get("reconciled_at"), "reconciled_at")
    if context.get("expired") is not False:
        raise ValueError("reconciliation context must not be expired")
    if context.get("replayed") is not False:
        raise ValueError("reconciliation context must not be replayed")
    if context.get("stale") is not False:
        raise ValueError("reconciliation context must not be stale")
    attestation = context.get("operator_attestation")
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
    _required_exact_set(context.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(context.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if context.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(context)
