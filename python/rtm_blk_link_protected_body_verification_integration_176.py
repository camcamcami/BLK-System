"""BLK-SYSTEM-176 RTM / blk-link protected-body verification integration.

This deterministic integration consumes the BLK-SYSTEM-175 decision package and
binds its verification record into the RTM / blk-link evidence path. It does not
generate RTM, reject drift, establish coverage truth, run production blk-link,
read protected files, mutate source/Git, run tooling, or claim production
isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_ladder_168_171 import _parse_not_stale, _validate_trace_copy
from metadata_bound_rtm_trace_closure_approval_capture import _required_exact_set, _required_hash
from protected_body_verification_decision_engine_175 import (
    CANONICAL_BLK175_DECISION_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK175_VERIFICATION_RECORD_HASH,
    DECISION_EXECUTION_PACKAGE_ID_175,
    DECISION_EXECUTION_SCOPE_175,
    DECISION_EXECUTION_STATUS_175,
    EXACT_EXCLUDED_AUTHORITIES_175,
    EXACT_PROOF_OBLIGATIONS_175,
    RUN_ID_CONSUMED_175,
    SELECTED_FRONTIER_175,
    SIDE_EFFECT_FLAGS_175,
    VERIFICATION_MATCH_RESULT_175,
    VERIFICATION_RECORD_ID_175,
    _scan_high_risk_freeform,
)

RECONCILIATION_STATUS_176 = "RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_INTEGRATED_AFTER_BLK175"
RECONCILIATION_PACKAGE_ID_176 = "RTM-BLK-LINK-PROTECTED-BODY-VERIFICATION-INTEGRATION-176-001"
RECONCILIATION_SCOPE_176 = "RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_INTEGRATION_ONLY_NO_NEW_RUNTIME_AUTHORITY"
SELECTED_FRONTIER_176 = "rtm_blk_link_protected_body_verification_integration_176"
NEXT_FRONTIER_176_CLEAN = "NEXT_FRONTIER_RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_READY_NOT_REUSABLE_AUTHORITY"
NEXT_FRONTIER_176_MISMATCH = "NEXT_FRONTIER_OPERATOR_REVIEW_OF_PROTECTED_BODY_MISMATCH_REQUIRED_NOT_DRIFT_REJECTION"
CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH = "sha256:e4be29f1cc87309f94890e420f2bec466610c0d5346f63ddd01e275a5fbf3c59"

EXACT_EXCLUDED_AUTHORITIES_176 = {
    "REUSABLE_PROTECTED_BODY_VERIFICATION_AUTHORITY",
    "PROTECTED_BODY_TEXT_RETURN_OR_BODY_CONTENT_EXPOSURE",
    "PROTECTED_BODY_FILESYSTEM_READ_BY_INTEGRATION",
    "PROTECTED_BODY_COPY_PARSE_HASH_SCAN_BY_INTEGRATION",
    "AUTHORITATIVE_DRIFT_DECISION_OR_REJECTION",
    "RTM_DRIFT_REJECTION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "REUSABLE_ACTIVE_VAULT_COMPARISON_AUTHORITY",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_LIVE_RUNTIME_EXECUTION_BEYOND_RECORD_ONLY_EVIDENCE",
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
    "OBSERVED_FAILURE_HARDENING_WITHOUT_REAL_HOSTILE_BYPASS",
}

EXACT_PROOF_OBLIGATIONS_176 = {
    "BLK175_DECISION_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK175_VERIFICATION_RECORD_HASH_RECOMPUTED_AND_BOUND",
    "BLK174_REQUEST_HASH_BOUND_THROUGH_BLK175",
    "RTM_BLK_LINK_EVIDENCE_PATH_CONSUMES_VERIFICATION_RECORD",
    "CLEAN_OR_MISMATCH_RESULT_RECONCILED_WITHOUT_DRIFT_REJECTION",
    "COVERAGE_TRUTH_NOT_ESTABLISHED_BY_INTEGRATION",
    "RTM_GENERATION_NOT_PERFORMED_BY_INTEGRATION",
    "PROTECTED_BODY_TEXT_NOT_INCLUDED_OR_RETURNED",
    "NO_OBSERVED_HOSTILE_BYPASS_REQUIRING_177_HARDENING",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}

SIDE_EFFECT_FLAGS_176 = (
    "next_frontier_granted",
    "observed_failure_requires_177_hardening",
    "protected_body_text_included",
    "protected_body_content_returned",
    "protected_body_filesystem_read_performed",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted_by_fixture",
    "protected_body_scan_attempted",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "runtime_rtm_generation_authorized",
    "rtm_generated",
    "reusable_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_live_execution_performed",
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

_ATTESTATION_176 = frozenset({
    "exact_blk175_decision_reviewed",
    "verification_record_hash_verified",
    "rtm_blk_link_evidence_path_bound_to_verification_record",
    "reconciliation_only_not_new_runtime_authority",
    "protected_body_text_not_included_or_returned",
    "rtm_generation_excluded",
    "drift_rejection_excluded",
    "coverage_truth_excluded",
    "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded",
    "no_observed_hostile_bypass_requiring_177_hardening",
    "no_production_isolation_claim",
})

_CONTEXT_KEYS_176 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_decision_execution_package_id", "upstream_decision_execution_package_hash",
    "upstream_verification_record_hash", "run_id_consumed", "beo_id", "beb_id",
    "exact_trace_identities", "protected_body_hashes_verified_observed", "mismatches_observed",
    "integration_notes", "reconciled_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_176,
})

_PACKAGE_KEYS_175 = frozenset({
    "decision_execution_status", "decision_execution_package_id", "operator_identity", "decision_execution_scope",
    "selected_frontier", "upstream_authority_request_package_id", "upstream_authority_request_package_hash",
    "upstream_reconciliation_package_hash", "upstream_decision_execution_package_hash", "approval_id",
    "run_id_consumed", "operator_decision_text_raw", "operator_decision_captured",
    "one_run_id_consumed_in_record_only_evidence", "protected_body_verification_decision_recorded",
    "protected_body_hashes_compared_from_caller_supplied_metadata", "protected_body_hashes_verified",
    "verification_result", "mismatches", "beo_id", "beb_id", "exact_trace_identities",
    "protected_body_verification_inputs", "verification_record_id", "verification_record", "verification_record_hash",
    "decision_execution_request_hash", "decided_at", "requested_at", "expires_at", "expired", "replayed", "stale",
    "next_required_authority", "operator_attestation", "proof_obligations", "excluded_authorities",
    "decision_execution_package_hash", *SIDE_EFFECT_FLAGS_175,
})


def valid_rtm_blk_link_protected_body_verification_integration_176(decision175: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_176,
        "operator_identity": decision175["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_176,
        "selected_frontier": SELECTED_FRONTIER_176,
        "upstream_decision_execution_package_id": decision175["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": decision175["decision_execution_package_hash"],
        "upstream_verification_record_hash": decision175["verification_record_hash"],
        "run_id_consumed": decision175["run_id_consumed"],
        "beo_id": decision175["beo_id"],
        "beb_id": decision175["beb_id"],
        "exact_trace_identities": list(decision175["exact_trace_identities"]),
        "protected_body_hashes_verified_observed": decision175["protected_body_hashes_verified"],
        "mismatches_observed": deepcopy(decision175["mismatches"]),
        "integration_notes": "BLK-175 verification record bound into RTM / blk-link evidence path; denied adjacent authority remains false.",
        "reconciled_at": "2099-05-16T21:50:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_176},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_176),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_176),
    }
    for flag in SIDE_EFFECT_FLAGS_176:
        record[flag] = False
    record.update(overrides)
    return record


def build_rtm_blk_link_protected_body_verification_integration_176(decision175_package: dict[str, Any], context176: dict[str, Any]) -> dict[str, Any]:
    decision = _validate_175_package(decision175_package)
    context = _validate_request_like(context176, _CONTEXT_KEYS_176, _ATTESTATION_176, EXACT_PROOF_OBLIGATIONS_176, EXACT_EXCLUDED_AUTHORITIES_176, SIDE_EFFECT_FLAGS_176)
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_176)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_176)
    _require(context, "selected_frontier", SELECTED_FRONTIER_176)
    _require_matching_upstream(context, decision, (
        ("upstream_decision_execution_package_id", "decision_execution_package_id"),
        ("upstream_decision_execution_package_hash", "decision_execution_package_hash"),
        ("upstream_verification_record_hash", "verification_record_hash"),
        ("operator_identity", "operator_identity"),
        ("run_id_consumed", "run_id_consumed"),
        ("beo_id", "beo_id"),
        ("beb_id", "beb_id"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    _scan_high_risk_freeform(context["integration_notes"], "integration_notes")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], decision["exact_trace_identities"])
    if context["protected_body_hashes_verified_observed"] is not decision["protected_body_hashes_verified"]:
        raise ValueError("protected_body_hashes_verified_observed must match BLK-175 evidence")
    if context["mismatches_observed"] != decision["mismatches"]:
        raise ValueError("mismatches_observed must match BLK-175 evidence")
    clean = bool(decision["protected_body_hashes_verified"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_176,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_176,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_176,
        "selected_frontier": SELECTED_FRONTIER_176,
        "upstream_decision_execution_package_id": decision["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": decision["decision_execution_package_hash"],
        "upstream_verification_record_id": decision["verification_record_id"],
        "upstream_verification_record_hash": decision["verification_record_hash"],
        "upstream_authority_request_package_hash": decision["upstream_authority_request_package_hash"],
        "run_id_consumed": decision["run_id_consumed"],
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
        "exact_trace_identities": trace_ids,
        "rtm_blk_link_protected_body_verification_evidence_bound": True,
        "clean_protected_body_verification_reconciled": clean,
        "protected_body_hashes_verified": clean,
        "mismatches": deepcopy(decision["mismatches"]),
        "observed_failure_requires_177_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_176_CLEAN if clean else NEXT_FRONTIER_176_MISMATCH,
        "next_frontier_granted": False,
        "integration_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_176),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_176),
    }
    for flag in SIDE_EFFECT_FLAGS_176:
        package[flag] = False
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _validate_175_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-175 package must be a dictionary")
    extra = sorted(set(package) - _PACKAGE_KEYS_175)
    if extra:
        raise ValueError(f"unexpected BLK-175 field {extra[0]!r}")
    missing = sorted(_PACKAGE_KEYS_175 - set(package))
    if missing:
        raise ValueError(f"missing BLK-175 field {missing[0]!r}")
    if package.get("decision_execution_status") != DECISION_EXECUTION_STATUS_175:
        raise ValueError("decision_execution_status must be exact BLK-175 status")
    _require(package, "decision_execution_package_id", DECISION_EXECUTION_PACKAGE_ID_175)
    _require(package, "decision_execution_scope", DECISION_EXECUTION_SCOPE_175)
    _require(package, "selected_frontier", SELECTED_FRONTIER_175)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_175)
    _required_hash(package.get("verification_record_hash"), "verification_record_hash")
    _required_hash(package.get("decision_execution_package_hash"), "decision_execution_package_hash")
    if package["verification_record_hash"] != _canonical_hash({k: v for k, v in package["verification_record"].items() if k != "verification_record_hash"}):
        raise ValueError("verification_record_hash does not match submitted BLK-175 record")
    if package["verification_record_hash"] != CANONICAL_BLK175_VERIFICATION_RECORD_HASH:
        raise ValueError("canonical BLK-175 verification record hash mismatch")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"})
    if package["decision_execution_package_hash"] != computed:
        raise ValueError("decision_execution_package_hash does not match submitted BLK-175 package")
    if package["decision_execution_package_hash"] != CANONICAL_BLK175_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-175 decision execution package hash mismatch")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_175, "BLK-175 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_175, "BLK-175 excluded_authorities")
    if package.get("verification_record_id") != VERIFICATION_RECORD_ID_175:
        raise ValueError("verification_record_id must be exact BLK-175 id")
    if package.get("verification_result") == VERIFICATION_MATCH_RESULT_175 and package.get("protected_body_hashes_verified") is not True:
        raise ValueError("verified result must set protected_body_hashes_verified true")
    for flag in SIDE_EFFECT_FLAGS_175:
        expected = flag in {
            "operator_decision_captured",
            "one_run_id_consumed_in_record_only_evidence",
            "protected_body_verification_decision_recorded",
            "protected_body_hashes_compared_from_caller_supplied_metadata",
        }
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-175 package {flag} must be {expected}")
    return package


def _validate_request_like(record: Any, keys: frozenset[str], attestation_keys: frozenset[str], proof_set: set[str], excluded_set: set[str], false_flags: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("record must be a dictionary")
    extra = sorted(set(record) - keys)
    if extra:
        raise ValueError(f"unexpected field {extra[0]!r}")
    missing = sorted(keys - set(record))
    if missing:
        raise ValueError(f"missing field {missing[0]!r}")
    if record.get("expired") is not False:
        raise ValueError("record must not be expired")
    if record.get("replayed") is not False:
        raise ValueError("record must not be replayed")
    if record.get("stale") is not False:
        raise ValueError("record must not be stale")
    if not isinstance(record.get("operator_attestation"), dict):
        raise ValueError("operator_attestation must be a dictionary")
    attestation_extra = sorted(set(record["operator_attestation"]) - attestation_keys)
    if attestation_extra:
        raise ValueError(f"unexpected field {attestation_extra[0]!r}")
    if set(record["operator_attestation"]) != attestation_keys:
        raise ValueError("operator_attestation must match exact key set")
    for key, value in record["operator_attestation"].items():
        if value is not True:
            raise ValueError(f"operator_attestation {key} must be true")
    _required_exact_set(record.get("proof_obligations"), proof_set, "proof_obligations")
    _required_exact_set(record.get("excluded_authorities"), excluded_set, "excluded_authorities")
    _scan_high_risk_freeform(record.get("operator_identity"), "operator_identity")
    for flag in false_flags:
        if record.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return record


def _require(record: dict[str, Any], key: str, expected: Any) -> None:
    if record.get(key) != expected:
        raise ValueError(f"{key} must be {expected!r}")


def _require_matching_upstream(record: dict[str, Any], upstream: dict[str, Any], pairs: tuple[tuple[str, str], ...]) -> None:
    for local_key, upstream_key in pairs:
        if record.get(local_key) != upstream.get(upstream_key):
            raise ValueError(f"{local_key} must match upstream {upstream_key}")
