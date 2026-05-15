"""BLK-SYSTEM-156 post metadata RTM / blk-link reconciliation review.

Consumes the exact BLK-SYSTEM-155 bounded metadata reconciliation execution
package and emits review-only post-reconciliation evidence. It classifies the
record as clean metadata reconciliation and selects the next operator decision
frontier without granting RTM generation, production blk-link, drift rejection,
coverage truth, protected-body access, runtime, mutation, or signer/storage/
ledger reuse authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from active_vault_hash_comparison_decision_package import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from authoritative_beo_publication_authority_request import _canonical_hash
from bounded_metadata_rtm_blk_link_reconciliation_execution import (
    EXACT_EXCLUDED_AUTHORITIES as BLK155_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK155_PROOF_OBLIGATIONS,
    EXECUTION_PACKAGE_ID as BLK155_EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS as BLK155_EXECUTION_STATUS,
    RECONCILIATION_RECORD_ID as BLK155_RECONCILIATION_RECORD_ID,
    REQUIRED_FALSE_FLAGS as BLK155_REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS as BLK155_REQUIRED_TRUE_FLAGS,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

REVIEW_STATUS = "POST_METADATA_RTM_BLK_LINK_RECONCILIATION_REVIEW_COMPLETE_NOT_AUTHORITY"
REVIEW_PACKAGE_ID = "POST-METADATA-RTM-BLK-LINK-RECONCILIATION-REVIEW-156-001"
REVIEW_SCOPE = "POST_METADATA_RECONCILIATION_REVIEW_ONLY_NEXT_DECISION_NOT_GRANTED"
SELECTED_FRONTIER = "post_metadata_rtm_blk_link_reconciliation_review"
NEXT_FRONTIER = "NEXT_FRONTIER_METADATA_BOUND_RTM_GENERATION_DECISION_NOT_GRANTED"
CANONICAL_BLK155_EXECUTION_PACKAGE_HASH = "sha256:07679c9e1e0dca0d62282b5217312171349c1f4318c579f9a76d1ef277d40bc4"
CANONICAL_BLK155_RECONCILIATION_RECORD_HASH = "sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026"

SIDE_EFFECT_FLAGS = (
    "next_frontier_granted",
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
    "NEXT_FRONTIER_AUTHORITY_GRANT",
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
    "BLK155_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK155_RECONCILIATION_RECORD_IDENTITY_AND_HASH_BOUND",
    "CLEAN_METADATA_RECONCILIATION_CONFIRMED",
    "NEXT_FRONTIER_SELECTED_AS_DECISION_ONLY_NOT_AUTHORITY",
    "RTM_GENERATION_AND_PRODUCTION_BLK_LINK_EXECUTION_EXCLUDED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "ACTIVE_VAULT_FILESYSTEM_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_REUSE_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "ONE_SPRINT_CLOSEOUT_ONLY_REQUIRED",
}

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk155_execution_reviewed",
        "clean_metadata_reconciliation_confirmed",
        "next_frontier_is_decision_only",
        "no_authority_request_or_approval_emitted",
        "no_run_id_reserved_or_consumed",
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

_CONTEXT_KEYS = frozenset(
    {
        "review_package_id",
        "operator_identity",
        "review_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_reconciliation_record_id",
        "upstream_reconciliation_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "review_result",
        "next_frontier",
        "reviewed_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)


def valid_post_reconciliation_review_context(execution_package: dict[str, Any], **overrides) -> dict[str, Any]:
    context = {
        "review_package_id": REVIEW_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "review_scope": REVIEW_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution_package["execution_package_id"],
        "upstream_execution_package_hash": execution_package["execution_package_hash"],
        "upstream_reconciliation_record_id": execution_package["reconciliation_record_id"],
        "upstream_reconciliation_record_hash": execution_package["reconciliation_record_hash"],
        "beo_id": execution_package["beo_id"],
        "beb_id": execution_package["beb_id"],
        "exact_trace_identities": list(execution_package["exact_trace_identities"]),
        "review_result": "CLEAN_METADATA_RECONCILIATION_REVIEWED_NEXT_DECISION_REQUIRED",
        "next_frontier": NEXT_FRONTIER,
        "reviewed_at": "2099-05-16T12:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in sorted(_ATTESTATION_KEYS)},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def build_post_metadata_rtm_blk_link_reconciliation_review(
    execution_package: dict[str, Any], review_context: dict[str, Any]
) -> dict[str, Any]:
    execution = _validate_execution_package(execution_package)
    context = _validate_review_context(review_context, execution)
    package = {
        "review_status": REVIEW_STATUS,
        "review_package_id": REVIEW_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "review_scope": REVIEW_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_reconciliation_record_id": execution["reconciliation_record_id"],
        "upstream_reconciliation_record_hash": execution["reconciliation_record_hash"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(execution["exact_trace_identities"]),
        "review_result": context["review_result"],
        "next_frontier": NEXT_FRONTIER,
        "review_context_hash": _canonical_hash(context),
        "reviewed_at": context["reviewed_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["review_package_hash"] = _canonical_hash({key: value for key, value in package.items() if key != "review_package_hash"})
    return package


def _validate_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("execution_package must be a dictionary")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("execution_package_hash"), "execution_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-155 package")
    if submitted_hash != CANONICAL_BLK155_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-155 execution package required")
    expected = {
        "execution_status": BLK155_EXECUTION_STATUS,
        "execution_package_id": BLK155_EXECUTION_PACKAGE_ID,
        "reconciliation_record_id": BLK155_RECONCILIATION_RECORD_ID,
        "reconciliation_record_hash": CANONICAL_BLK155_RECONCILIATION_RECORD_HASH,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"execution_package {key} must be {value}")
    record = normalized.get("reconciliation_record")
    if not isinstance(record, dict):
        raise ValueError("reconciliation_record must be a dictionary")
    record_hash = _canonical_hash({key: value for key, value in record.items() if key != "record_hash"})
    if record.get("record_hash") != record_hash:
        raise ValueError("reconciliation_record_hash does not match submitted record")
    if record.get("record_hash") != CANONICAL_BLK155_RECONCILIATION_RECORD_HASH:
        raise ValueError("canonical BLK-155 reconciliation record required")
    if record.get("metadata_hashes_reconciled") is not True or record.get("mismatch_count") != 0 or record.get("mismatches") != []:
        raise ValueError("clean BLK-155 reconciliation required")
    if record.get("drift_rejection_performed") is not False or record.get("coverage_truth_established") is not False or record.get("protected_body_reads") is not False:
        raise ValueError("BLK-155 record must preserve drift/coverage/protected-body denials")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    _required_exact_set(normalized.get("proof_obligations"), BLK155_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK155_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in BLK155_REQUIRED_TRUE_FLAGS:
        if normalized.get(flag) is not True:
            raise ValueError(f"execution_package {flag} must remain true")
    for flag in BLK155_REQUIRED_FALSE_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"execution_package {flag} must remain false")
    return normalized


def _validate_review_context(context: Any, execution: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("review_context must be a dictionary")
    unknown = sorted(set(context) - _CONTEXT_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_CONTEXT_KEYS - set(context))
    if missing:
        raise ValueError(f"review_context missing fields: {missing}")
    _scan_value_strings(
        {
            "review_package_id": context.get("review_package_id"),
            "review_scope": context.get("review_scope"),
            "selected_frontier": context.get("selected_frontier"),
            "operator_identity": context.get("operator_identity"),
        },
        "review_context",
        allow_selected=True,
    )
    expected = {
        "review_package_id": REVIEW_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "review_scope": REVIEW_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_reconciliation_record_id": execution["reconciliation_record_id"],
        "upstream_reconciliation_record_hash": execution["reconciliation_record_hash"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "review_result": "CLEAN_METADATA_RECONCILIATION_REVIEWED_NEXT_DECISION_REQUIRED",
        "next_frontier": NEXT_FRONTIER,
    }
    for key, value in expected.items():
        if context.get(key) != value:
            raise ValueError(f"{key} must be {value}")
    if context.get("exact_trace_identities") != execution.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-155 execution package")
    _validate_exact_trace_identities(context.get("exact_trace_identities"))
    _parse_timestamp(context.get("reviewed_at"), "reviewed_at")
    for flag in ("expired", "replayed", "stale"):
        if context.get(flag) is not False:
            raise ValueError(f"review_context must not be {flag}")
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
