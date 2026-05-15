"""BLK-SYSTEM-145 authority ladder hardening-only policy.

This deterministic fixture consumes the exact BLK-SYSTEM-144 post-RTM-generation
reconciliation package and pins a hardening-only pause. It deliberately selects
no next authority rung, requests no authority decision, performs no execution,
reads no protected bodies or active-vault files, runs no tooling, and grants no
runtime/production authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_generation_authority_request import _parse_timestamp, _required_exact_set, _required_hash, _scan_value_strings
from post_rtm_generation_reconciliation import (
    CLEAN_RECONCILIATION_RESULT as BLK144_CLEAN_RECONCILIATION_RESULT,
    NEXT_FRONTIER_CLEAN as BLK144_NEXT_FRONTIER,
    RECONCILIATION_PACKAGE_ID as BLK144_RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_SCOPE as BLK144_RECONCILIATION_SCOPE,
    RECONCILIATION_STATUS as BLK144_RECONCILIATION_STATUS,
    SELECTED_FRONTIER as BLK144_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK144_SIDE_EFFECT_FLAGS,
)

POLICY_STATUS = "AUTHORITY_LADDER_HARDENING_ONLY_AFTER_BLK144"
POLICY_PACKAGE_ID = "AUTHORITY-LADDER-HARDENING-145-001"
HARDENING_CONTEXT_ID = "AUTHORITY-LADDER-HARDENING-CONTEXT-145-001"
HARDENING_MODE = "STOP_AND_HARDEN_ONLY_NO_NEXT_AUTHORITY_DECISION"
POLICY_SCOPE = "AUTHORITY_LADDER_HARDENING_ONLY_NO_AUTHORITY_SELECTION_OR_EXECUTION"
SELECTED_FRONTIER = "authority_ladder_hardening_only"
NEXT_FRONTIER = "NEXT_FRONTIER_AUTHORITY_LADDER_HARDENING_ONLY_NO_AUTHORITY_RUNG_SELECTED"
HARDENING_RESULT = "AUTHORITY_LADDER_PAUSED_FOR_HARDENING_NO_NEW_AUTHORITY_GRANTED"
CANONICAL_BLK144_RECONCILIATION_PACKAGE_HASH = "sha256:8c3bb9b2be4efd03812c477b390c9ae0550748106f24de337cb399c5201b6127"
CANONICAL_BLK144_RECONCILIATION_CONTEXT_HASH = "sha256:66c90c7f513306acf05d1b4f49e800548318e7a2c0a47a57d1dd4bd6c546bf61"
EXPECTED_HARDENING_REASON = "STOP_AND_HARDEN_ONLY_AFTER_CLEAN_POST_RTM_RECONCILIATION"

SIDE_EFFECT_FLAGS = (
    "next_frontier_granted",
    "authority_decision_authorized",
    "authority_rung_execution_authorized",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
    "runtime_rtm_generation_authorized",
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
    "NEXT_AUTHORITY_RUNG_SELECTION",
    "NEXT_AUTHORITY_DECISION_REQUEST",
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "AUTHORITY_RUNG_EXECUTION",
    "ADDITIONAL_RTM_GENERATION_OR_APPROVAL",
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
    "BLK144_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK144_RECONCILIATION_CONTEXT_HASH_BOUND",
    "HARDENING_ONLY_MODE_EXACTLY_SELECTED",
    "NO_NEXT_AUTHORITY_RUNG_SELECTED",
    "NO_AUTHORITY_DECISION_REQUESTED",
    "NO_EXECUTION_REQUESTED",
    "RECONCILIATION_EVIDENCE_NOT_TREATED_AS_AUTHORITY",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_DRIFT_REJECTION_AND_COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "BEB_DISPATCH_BEO_CLOSEOUT_AND_PUBLICATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}

_BLK144_RECONCILIATION_KEYS = frozenset(
    {
        "reconciliation_status",
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
        "metadata_bound_rtm_generation_reconciled",
        "rtm_record_metadata_only",
        "reconciliation_result",
        "recommended_next_frontier",
        "reconciliation_context_hash",
        "reconciled_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "reconciliation_package_hash",
        *BLK144_SIDE_EFFECT_FLAGS,
    }
)

_CONTEXT_ALLOWED_KEYS = frozenset(
    {
        "hardening_context_id",
        "operator_identity",
        "hardening_mode",
        "policy_scope",
        "selected_frontier",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_reconciliation_context_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_rtm_record_id",
        "upstream_rtm_record_hash",
        "hardening_reason",
        "authority_rung_selected",
        "authority_decision_requested",
        "execution_requested",
        "hardened_at",
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
        "exact_blk144_reconciliation_reviewed",
        "hardening_only_mode_selected",
        "no_authority_rung_selected",
        "no_authority_decision_requested",
        "no_execution_requested",
        "reconciliation_evidence_is_not_authority",
        "no_active_vault_filesystem_read",
        "no_protected_body_reads",
        "no_drift_rejection_or_coverage_truth",
        "no_reusable_blk_link_authority",
        "no_beb_dispatch_or_beo_closeout",
        "no_signer_storage_ledger_side_effects",
        "no_target_source_git_mutation",
        "no_blk_pipe_blk_test_codex_tooling",
        "no_production_isolation_claim",
    }
)


def build_authority_ladder_hardening_policy(reconciliation_package: dict[str, Any], hardening_context: dict[str, Any]) -> dict[str, Any]:
    """Emit one exact BLK-SYSTEM-145 hardening-only policy package."""

    reconciliation = _validate_blk144_reconciliation_package(reconciliation_package)
    context = _validate_hardening_context(hardening_context, reconciliation)
    package = {
        "policy_status": POLICY_STATUS,
        "policy_package_id": POLICY_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "hardening_context_id": context["hardening_context_id"],
        "hardening_mode": HARDENING_MODE,
        "policy_scope": POLICY_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_rtm_record_id": reconciliation["upstream_rtm_record_id"],
        "upstream_rtm_record_hash": reconciliation["upstream_rtm_record_hash"],
        "hardening_reason": EXPECTED_HARDENING_REASON,
        "hardening_result": HARDENING_RESULT,
        "authority_rung_selected": False,
        "authority_decision_requested": False,
        "execution_requested": False,
        "reconciliation_evidence_is_authority": False,
        "next_frontier": NEXT_FRONTIER,
        "hardening_context_hash": _canonical_hash(context),
        "hardened_at": context["hardened_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["policy_package_hash"] = _canonical_hash(package)
    return package


def _validate_blk144_reconciliation_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("reconciliation package must be a dictionary")
    unknown = sorted(set(package) - _BLK144_RECONCILIATION_KEYS)
    if unknown:
        raise ValueError(f"reconciliation package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_BLK144_RECONCILIATION_KEYS - set(package))
    if missing:
        raise ValueError(f"reconciliation package missing field {missing[0]!r}")
    submitted_hash = _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    actual_hash = _canonical_hash({key: value for key, value in package.items() if key != "reconciliation_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-144 package")
    if submitted_hash != CANONICAL_BLK144_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-144 reconciliation package required")
    expected = {
        "reconciliation_status": BLK144_RECONCILIATION_STATUS,
        "reconciliation_package_id": BLK144_RECONCILIATION_PACKAGE_ID,
        "reconciliation_scope": BLK144_RECONCILIATION_SCOPE,
        "selected_frontier": BLK144_SELECTED_FRONTIER,
        "reconciliation_result": BLK144_CLEAN_RECONCILIATION_RESULT,
        "recommended_next_frontier": BLK144_NEXT_FRONTIER,
        "reconciliation_context_hash": CANONICAL_BLK144_RECONCILIATION_CONTEXT_HASH,
        "metadata_bound_rtm_generation_reconciled": True,
        "rtm_record_metadata_only": True,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("canonical BLK-144 reconciliation package required")
    for flag in ("expired", "replayed", "stale"):
        if package.get(flag) is not False:
            raise ValueError(f"BLK-144 reconciliation package must not be {flag}")
    for flag in BLK144_SIDE_EFFECT_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-144 reconciliation package {flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    return deepcopy(package)


def _validate_hardening_context(context: Any, reconciliation: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("hardening context must be a dictionary")
    unknown = sorted(set(context) - _CONTEXT_ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_CONTEXT_ALLOWED_KEYS - set(context))
    if missing:
        raise ValueError(f"hardening context missing field {missing[0]!r}")
    _scan_value_strings({"operator_identity": context.get("operator_identity")}, "hardening_context", allow_selected=True)
    _require_exact_or_reject_laundering(context, "hardening_context_id", HARDENING_CONTEXT_ID)
    _require_exact_or_reject_laundering(context, "hardening_mode", HARDENING_MODE)
    _require_exact_or_reject_laundering(context, "policy_scope", POLICY_SCOPE)
    _require_exact_or_reject_laundering(context, "selected_frontier", SELECTED_FRONTIER)
    _require_exact_or_reject_laundering(context, "hardening_reason", EXPECTED_HARDENING_REASON)
    expected_scalars = {
        "operator_identity": reconciliation["operator_identity"],
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_reconciliation_context_hash": reconciliation["reconciliation_context_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_rtm_record_id": reconciliation["upstream_rtm_record_id"],
        "upstream_rtm_record_hash": reconciliation["upstream_rtm_record_hash"],
    }
    for key, expected in expected_scalars.items():
        if context.get(key) != expected:
            raise ValueError(f"{key} must match BLK-144 reconciliation package")
    if context.get("authority_rung_selected") is not False:
        raise ValueError("authority_rung_selected must remain false")
    if context.get("authority_decision_requested") is not False:
        raise ValueError("authority_decision_requested must remain false")
    if context.get("execution_requested") is not False:
        raise ValueError("execution_requested must remain false")
    hardened_at = _parse_timestamp(context.get("hardened_at"), "hardened_at")
    reconciled_at = _parse_timestamp(reconciliation.get("reconciled_at"), "BLK-144 reconciled_at")
    if hardened_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("hardening context must not be calendar-stale")
    if hardened_at < reconciled_at:
        raise ValueError("hardening context must not predate BLK-144 reconciliation")
    if context.get("expired") is not False:
        raise ValueError("hardening context must not be expired")
    if context.get("replayed") is not False:
        raise ValueError("hardening context must not be replayed")
    if context.get("stale") is not False:
        raise ValueError("hardening context must not be stale")
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
    _scan_value_strings({key: context.get(key)}, "hardening_context", allow_selected=True)
    raise ValueError(f"{key} must match exact hardening-only value")
