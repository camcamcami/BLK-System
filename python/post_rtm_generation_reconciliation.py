"""BLK-SYSTEM-144 post-RTM-generation reconciliation.

This deterministic fixture consumes the exact BLK-SYSTEM-143 metadata-bound RTM
-generation execution record and reconciles it as record-only evidence for the
next separately approved frontier. It does not generate additional RTM, reject
drift, establish coverage truth, run reusable production blk-link, read active
vault files, read/copy/parse/hash/scan protected requirement bodies, mutate
source/Git state, run tooling, perform signer/storage/ledger behavior, or claim
production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_generation_authority_request import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from metadata_bound_rtm_generation_execution_package import (
    APPROVAL_ID as BLK143_APPROVAL_ID,
    EXECUTION_PACKAGE_ID as BLK143_EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS as BLK143_EXECUTION_STATUS,
    NEXT_REQUIRED_AUTHORITY as BLK143_NEXT_REQUIRED_AUTHORITY,
    RTM_RECORD_ID as BLK143_RTM_RECORD_ID,
    RUN_ID as BLK143_RUN_ID,
    SELECTED_FRONTIER as BLK143_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK143_SIDE_EFFECT_FLAGS,
)

RECONCILIATION_STATUS = "POST_RTM_GENERATION_RECONCILED_FOR_EXACT_BLK143_RECORD_ONLY"
RECONCILIATION_PACKAGE_ID = "POST-RTM-GENERATION-RECONCILIATION-144-001"
RECONCILIATION_SCOPE = "POST_RTM_GENERATION_RECONCILIATION_RECORD_ONLY_NO_DRIFT_COVERAGE_TRUTH_PROTECTED_BODY"
SELECTED_FRONTIER = "post_rtm_generation_reconciliation"
CLEAN_RECONCILIATION_RESULT = "CLEAN_METADATA_BOUND_RTM_GENERATION_RECONCILED_NEXT_AUTHORITY_DECISION_NOT_GRANTED"
NEXT_FRONTIER_CLEAN = "NEXT_FRONTIER_NARROW_POST_RTM_AUTHORITY_DECISION_NOT_GRANTED"
CANONICAL_BLK143_EXECUTION_PACKAGE_HASH = "sha256:e56a2598e53fee776bc992bac24aab7217754323e66f84f28ee8bdc0d512455c"
CANONICAL_BLK143_RTM_RECORD_HASH = "sha256:cc61edf626431bc9180ea57bd1e9eda66193e9825a12eab1e2516719cd52db97"

SIDE_EFFECT_FLAGS = (
    "next_frontier_granted",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
    "additional_rtm_generation_authorized",
    "additional_rtm_generated",
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
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "ADDITIONAL_RTM_GENERATION_OR_APPROVAL",
    "RTM_GENERATION_BEYOND_EXACT_BLK143_RECORD_RECONCILIATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXISTING_RECORD_METADATA",
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
    "BLK143_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK143_RTM_RECORD_IDENTITY_AND_HASH_RECOMPUTED",
    "BLK142_REQUEST_APPROVAL_AND_RUN_ID_BOUND_THROUGH_BLK143",
    "RTM_RECORD_METADATA_ONLY_RECONCILED_WITHOUT_PROTECTED_BODY_ACCESS",
    "NO_ADDITIONAL_RTM_GENERATION_OR_APPROVAL_CAPTURE",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "ONE_NEXT_FRONTIER_NAMED_WITH_AUTHORITY_NOT_GRANTED",
}

_EXECUTION_PACKAGE_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_status",
        "upstream_authority_request_package_hash",
        "upstream_authority_request_hash",
        "approval_id",
        "operator_approval_text_raw",
        "approval_capture_performed",
        "rtm_generation_approved",
        "run_id_consumed",
        "run_id_consumed_in_record",
        "execution_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_comparison_record_id",
        "upstream_comparison_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "metadata_bound_rtm_generation_executed",
        "rtm_record_id",
        "rtm_record",
        "rtm_record_hash",
        "next_required_authority",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "execution_package_hash",
        *BLK143_SIDE_EFFECT_FLAGS,
    }
)

_RTM_RECORD_KEYS = frozenset(
    {
        "rtm_record_id",
        "generation_mode",
        "consumed_run_id",
        "approval_id",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_authority_request_hash",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_comparison_record_id",
        "upstream_comparison_record_hash",
        "beo_id",
        "beb_id",
        "trace_identities",
        "recorded_at",
        "active_vault_filesystem_read_performed",
        "protected_body_reads",
        "rtm_drift_rejection_performed",
        "coverage_truth_established",
        "reusable_blk_link_authority_granted",
        "public_ledger_mutation",
        "rtm_record_hash",
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
        "upstream_rtm_record_id",
        "upstream_rtm_record_hash",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_authority_request_hash",
        "approval_id",
        "run_id_consumed",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "metadata_bound_rtm_generation_observed",
        "rtm_record_metadata_only_observed",
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
        "exact_blk143_execution_reviewed",
        "rtm_record_hash_verified",
        "reconciliation_only_not_authority_request",
        "metadata_bound_generation_interpreted_without_drift_decision",
        "record_remains_metadata_only",
        "no_active_vault_filesystem_read",
        "no_protected_body_reads",
        "no_protected_body_copy_parse_hash_scan",
        "no_additional_rtm_generation",
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


def build_post_rtm_generation_reconciliation(execution_package: dict[str, Any], reconciliation_context: dict[str, Any]) -> dict[str, Any]:
    """Emit one exact BLK-SYSTEM-144 post-RTM-generation reconciliation package."""

    execution = _validate_execution_package(execution_package)
    context = _validate_reconciliation_context(reconciliation_context, execution)
    package = {
        "reconciliation_status": RECONCILIATION_STATUS,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_rtm_record_id": execution["rtm_record_id"],
        "upstream_rtm_record_hash": execution["rtm_record_hash"],
        "upstream_authority_request_package_id": execution["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": execution["upstream_authority_request_package_hash"],
        "upstream_authority_request_hash": execution["upstream_authority_request_hash"],
        "approval_id": execution["approval_id"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(execution["exact_trace_identities"]),
        "metadata_bound_rtm_generation_reconciled": True,
        "rtm_record_metadata_only": True,
        "reconciliation_result": CLEAN_RECONCILIATION_RESULT,
        "recommended_next_frontier": NEXT_FRONTIER_CLEAN,
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
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _validate_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("execution package must be a dictionary")
    unknown = sorted(set(package) - _EXECUTION_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"execution package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"execution package missing field {missing[0]!r}")
    _validate_rtm_record(package)
    submitted_hash = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-143 package")
    if submitted_hash != CANONICAL_BLK143_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-143 execution package required")
    expected = {
        "execution_status": BLK143_EXECUTION_STATUS,
        "execution_package_id": BLK143_EXECUTION_PACKAGE_ID,
        "selected_frontier": BLK143_SELECTED_FRONTIER,
        "approval_id": BLK143_APPROVAL_ID,
        "run_id_consumed": BLK143_RUN_ID,
        "rtm_record_id": BLK143_RTM_RECORD_ID,
        "rtm_record_hash": CANONICAL_BLK143_RTM_RECORD_HASH,
        "next_required_authority": BLK143_NEXT_REQUIRED_AUTHORITY,
        "metadata_bound_rtm_generation_executed": True,
        "approval_capture_performed": True,
        "rtm_generation_approved": True,
        "run_id_consumed_in_record": True,
    }
    for key, expected_value in expected.items():
        if package.get(key) != expected_value:
            raise ValueError("canonical BLK-143 execution package required")
    for flag in ("expired", "replayed", "stale"):
        if package.get(flag) is not False:
            raise ValueError(f"BLK-143 execution package must not be {flag}")
    for flag in BLK143_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-143 execution package {flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_rtm_record(package: dict[str, Any]) -> None:
    record = package.get("rtm_record")
    if not isinstance(record, dict):
        raise ValueError("rtm_record must be a dictionary")
    unknown = sorted(set(record) - _RTM_RECORD_KEYS)
    if unknown:
        raise ValueError(f"rtm_record rejects unexpected field {unknown[0]!r}")
    missing = sorted(_RTM_RECORD_KEYS - set(record))
    if missing:
        raise ValueError(f"rtm_record missing field {missing[0]!r}")
    record_hash = _required_hash(package.get("rtm_record_hash"), "rtm_record_hash")
    actual_record_hash = _canonical_hash({key: value for key, value in record.items() if key != "rtm_record_hash"})
    if record.get("rtm_record_hash") != record_hash or record_hash != actual_record_hash:
        raise ValueError("rtm_record_hash does not match submitted BLK-143 RTM record")
    expected = {
        "rtm_record_id": BLK143_RTM_RECORD_ID,
        "generation_mode": "METADATA_BOUND_RTM_GENERATION_RECORD_ONLY",
        "consumed_run_id": BLK143_RUN_ID,
        "approval_id": BLK143_APPROVAL_ID,
        "trace_identities": package["exact_trace_identities"],
        "active_vault_filesystem_read_performed": False,
        "protected_body_reads": False,
        "rtm_drift_rejection_performed": False,
        "coverage_truth_established": False,
        "reusable_blk_link_authority_granted": False,
        "public_ledger_mutation": False,
    }
    for key, expected_value in expected.items():
        if record.get(key) != expected_value:
            if key in {
                "active_vault_filesystem_read_performed",
                "protected_body_reads",
                "rtm_drift_rejection_performed",
                "coverage_truth_established",
                "reusable_blk_link_authority_granted",
                "public_ledger_mutation",
            }:
                raise ValueError(f"rtm_record.{key} must remain false")
            raise ValueError("canonical BLK-143 RTM record required")
    _validate_exact_trace_identities(record.get("trace_identities"))


def _validate_reconciliation_context(context: Any, execution: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("reconciliation context must be a dictionary")
    unknown = sorted(set(context) - _CONTEXT_ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_CONTEXT_ALLOWED_KEYS - set(context))
    if missing:
        raise ValueError(f"reconciliation context missing field {missing[0]!r}")
    _scan_value_strings({"operator_identity": context.get("operator_identity")}, "reconciliation_context", allow_selected=True)
    _require_exact_or_reject_laundering(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID)
    _require_exact_or_reject_laundering(context, "reconciliation_scope", RECONCILIATION_SCOPE)
    _require_exact_or_reject_laundering(context, "selected_frontier", SELECTED_FRONTIER)
    expected_scalars = {
        "operator_identity": execution["operator_identity"],
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_rtm_record_id": execution["rtm_record_id"],
        "upstream_rtm_record_hash": execution["rtm_record_hash"],
        "upstream_authority_request_package_id": execution["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": execution["upstream_authority_request_package_hash"],
        "upstream_authority_request_hash": execution["upstream_authority_request_hash"],
        "approval_id": execution["approval_id"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
    }
    for key, expected in expected_scalars.items():
        if context.get(key) != expected:
            raise ValueError(f"{key} must match BLK-143 execution package")
    if context.get("exact_trace_identities") != execution.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-143 execution package")
    _validate_exact_trace_identities(context.get("exact_trace_identities"))
    if context.get("metadata_bound_rtm_generation_observed") != execution.get("metadata_bound_rtm_generation_executed"):
        raise ValueError("metadata_bound_rtm_generation_observed must match BLK-143 execution package")
    if context.get("rtm_record_metadata_only_observed") is not True:
        raise ValueError("rtm_record_metadata_only_observed must be true")
    reconciled_at = _parse_timestamp(context.get("reconciled_at"), "reconciled_at")
    execution_requested_at = _parse_timestamp(execution.get("requested_at"), "BLK-143 requested_at")
    if reconciled_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("reconciliation context must not be calendar-stale")
    if reconciled_at < execution_requested_at:
        raise ValueError("reconciliation context must not predate BLK-143 execution")
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
        raise ValueError(f"operator_attestation missing field {missing_attestation[0]!r}")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
    _required_exact_set(context.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(context.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if context.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(context)


def _require_exact_or_reject_laundering(context: dict[str, Any], key: str, expected: str) -> None:
    if context.get(key) == expected:
        return
    _scan_value_strings({key: context.get(key)}, "reconciliation_context", allow_selected=True)
    raise ValueError(f"{key} must match exact BLK-144 reconciliation value")
