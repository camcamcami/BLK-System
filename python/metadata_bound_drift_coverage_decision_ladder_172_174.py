"""BLK-SYSTEM-172..174 metadata-bound drift/coverage decision ladder.

This deterministic fixture consumes the BLK-SYSTEM-171 request only under the
operator's exact directive, records one metadata-only drift/coverage decision
package (172), reconciles it (173), and emits the request-only next frontier
(174) only because the reconciliation is clean.

It does not read/copy/parse/hash/scan protected BLK-req bodies, perform RTM
drift rejection, establish coverage truth, generate RTM, run reusable
production blk-link, mutate target/source/Git state, run BLK-pipe/BLK-test/Codex
or other tooling, reuse signer/storage/ledger authority, or claim production
isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_trace_closure_approval_capture import _required_hash
from active_vault_hash_comparison_ladder_168_171 import (
    CANONICAL_BLK169_COMPARISON_RECORD_HASH,
    CANONICAL_BLK170_RECONCILIATION_PACKAGE_HASH,
    CANONICAL_BLK171_AUTHORITY_REQUEST_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_171,
    EXACT_PROOF_OBLIGATIONS_171,
    NEXT_REQUIRED_AUTHORITY_171,
    REQUEST_PACKAGE_ID_171,
    REQUEST_SCOPE_171,
    REQUEST_STATUS_171,
    SELECTED_FRONTIER_171,
    SIDE_EFFECT_FLAGS_171,
    _parse_not_stale,
    _require,
    _require_false,
    _require_matching_upstream,
    _require_true,
    _validate_decision_window,
    _validate_request_like,
    _validate_time_window,
    _validate_trace_copy,
)

DECISION_EXECUTION_STATUS_172 = "METADATA_BOUND_DRIFT_COVERAGE_DECISION_CAPTURED_AND_ONE_RUN_RECORDED_FOR_EXACT_BLK171_REQUEST"
DECISION_EXECUTION_PACKAGE_ID_172 = "METADATA-BOUND-DRIFT-COVERAGE-DECISION-EXECUTION-172-001"
DECISION_EXECUTION_SCOPE_172 = "EXACT_METADATA_BOUND_DRIFT_COVERAGE_DECISION_RECORD_ONLY_NOT_AUTHORITATIVE_DRIFT_OR_COVERAGE_TRUTH"
SELECTED_FRONTIER_172 = "metadata_bound_drift_coverage_decision_execution_172"
APPROVAL_ID_172 = "APPROVAL-BLK-SYSTEM-171-METADATA-BOUND-DRIFT-COVERAGE-DECISION-001"
RUN_ID_CONSUMED_172 = "RUN-BLK-SYSTEM-172-METADATA-BOUND-DRIFT-COVERAGE-DECISION-001"
EXACT_OPERATOR_DECISION_TEXT_172 = (
    "APPROVE METADATA-BOUND-DRIFT-COVERAGE-DECISION-AUTHORITY-REQUEST-171-001 "
    "FOR ONE METADATA-ONLY DRIFT/COVERAGE DECISION RUN "
    "RUN-BLK-SYSTEM-172-METADATA-BOUND-DRIFT-COVERAGE-DECISION-001; "
    "NO PROTECTED BODY READS; NO RTM GENERATION; NO RTM DRIFT REJECTION; "
    "NO COVERAGE TRUTH; NO MUTATION."
)
METADATA_DRIFT_STATUS_172 = "NO_METADATA_HASH_DRIFT_OBSERVED_NOT_AUTHORITATIVE_DRIFT_REJECTION"
METADATA_COVERAGE_STATUS_172 = "METADATA_TRACE_SET_COHERENT_NOT_COVERAGE_TRUTH"
NEXT_REQUIRED_AUTHORITY_172 = "POST_DECISION_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH = "sha256:f9c3a7805d9ce0ed20f76ed993fbd78238f9bef3a8f48b67d7924438821f48d7"

RECONCILIATION_STATUS_173 = "METADATA_BOUND_DRIFT_COVERAGE_DECISION_POST_RUN_RECONCILED_CLEAN_AFTER_BLK172"
RECONCILIATION_PACKAGE_ID_173 = "METADATA-BOUND-DRIFT-COVERAGE-POST-DECISION-RECONCILIATION-173-001"
RECONCILIATION_SCOPE_173 = "POST_METADATA_BOUND_DRIFT_COVERAGE_DECISION_RECONCILIATION_ONLY_NO_NEW_AUTHORITY"
SELECTED_FRONTIER_173 = "metadata_bound_drift_coverage_post_decision_reconciliation_173"
NEXT_FRONTIER_173_CLEAN = "NEXT_FRONTIER_PROTECTED_BODY_VERIFICATION_DECISION_REQUEST_NOT_GRANTED"
CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH = "sha256:6db15d27c3b32710d7700434f66242a788e56c85014e7d2a9d2e544c61c09e54"

REQUEST_STATUS_174 = "PROTECTED_BODY_VERIFICATION_DECISION_AUTHORITY_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID_174 = "PROTECTED-BODY-VERIFICATION-DECISION-AUTHORITY-REQUEST-174-001"
REQUEST_SCOPE_174 = "PROTECTED_BODY_VERIFICATION_DECISION_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER_174 = "protected_body_verification_decision_request_174"
NEXT_REQUIRED_AUTHORITY_174 = "EXACT_PROTECTED_BODY_VERIFICATION_DECISION_APPROVAL_REQUIRED_NOT_GRANTED"
CANONICAL_BLK174_AUTHORITY_REQUEST_PACKAGE_HASH = "sha256:328c0d4a99020e7764d5f5bf834eb0c3f895801f883a22a8d67d5ca0375347ef"

_BASE_EXCLUDED = {
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "PROTECTED_BODY_VERIFICATION_EXECUTION",
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
}

EXACT_EXCLUDED_AUTHORITIES_172 = _BASE_EXCLUDED | {
    "DRIFT_OR_COVERAGE_DECISION_BEYOND_METADATA_HASH_EVIDENCE",
    "PROTECTED_BODY_VERIFICATION_THIS_SPRINT",
    "RUN_ID_REUSE_AFTER_RECORD_ONLY_CONSUMPTION",
}
EXACT_EXCLUDED_AUTHORITIES_173 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "AUTHORITATIVE_DRIFT_OR_COVERAGE_PROMOTION_BY_RECONCILIATION",
}
EXACT_EXCLUDED_AUTHORITIES_174 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "PROTECTED_BODY_VERIFICATION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_REQUEST_ONLY_PACKAGE",
}

EXACT_PROOF_OBLIGATIONS_172 = {
    "BLK171_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK170_RECONCILIATION_HASH_BOUND_THROUGH_BLK171",
    "OPERATOR_DECISION_CAPTURED_FOR_EXACT_BLK171_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_REQUEST",
    "RUN_ID_CONSUMED_ONCE_IN_RECORD_ONLY_EVIDENCE",
    "DECISION_LIMITED_TO_METADATA_HASH_EVIDENCE",
    "METADATA_DRIFT_STATUS_NOT_AUTHORITATIVE_DRIFT_REJECTION",
    "METADATA_COVERAGE_STATUS_NOT_COVERAGE_TRUTH",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_173 = {
    "BLK172_DECISION_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "METADATA_BOUND_DECISION_RECONCILED_WITHOUT_AUTHORITY_PROMOTION",
    "CLEAN_DECISION_INTERPRETED_WITHOUT_AUTHORITATIVE_DRIFT_OR_COVERAGE_TRUTH",
    "NEXT_FRONTIER_NAMED_WITH_AUTHORITY_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_174_HARDENING",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_174 = {
    "BLK173_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK172_DECISION_EXECUTION_HASH_BOUND_THROUGH_BLK173",
    "REQUEST_LIMITED_TO_FUTURE_EXACT_PROTECTED_BODY_VERIFICATION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE_OR_VERIFICATION_EXECUTION",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_NOT_PERFORMED_BY_REQUEST",
    "DRIFT_REJECTION_AND_COVERAGE_TRUTH_NOT_PERFORMED_BY_REQUEST",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}

SIDE_EFFECT_FLAGS_172 = (
    "operator_decision_captured",
    "one_run_id_consumed_in_record_only_evidence",
    "metadata_bound_drift_coverage_decision_recorded",
    "approval_capture_performed_outside_exact_request",
    "active_vault_hash_comparison_performed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
    "protected_body_verification_performed",
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
SIDE_EFFECT_FLAGS_173 = (
    "next_frontier_granted",
    "observed_failure_requires_174_hardening",
    *SIDE_EFFECT_FLAGS_172,
)
SIDE_EFFECT_FLAGS_174 = tuple(
    flag for flag in SIDE_EFFECT_FLAGS_172
    if flag not in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "metadata_bound_drift_coverage_decision_recorded"}
) + ("future_run_id_reserved_or_consumed",)

_ATTESTATION_172 = frozenset({
    "exact_blk171_request_reviewed", "operator_decision_captured_from_latest_directive",
    "run_id_consumed_once_in_record_only_evidence", "metadata_hash_evidence_only_scope_preserved",
    "metadata_drift_status_not_authoritative_rejection", "metadata_coverage_status_not_coverage_truth",
    "protected_body_reads_excluded", "rtm_generation_excluded", "rtm_drift_rejection_excluded",
    "coverage_truth_excluded", "reusable_blk_link_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_173 = frozenset({
    "exact_blk172_decision_reviewed", "reconciliation_only_not_authority_request",
    "clean_metadata_bound_decision_reconciled", "no_observed_failure_requiring_hardening",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "reusable_blk_link_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_174 = frozenset({
    "exact_blk173_reconciliation_reviewed", "request_is_for_future_approval_not_approval",
    "protected_body_verification_not_performed", "protected_body_reads_excluded",
    "rtm_generation_excluded", "drift_rejection_excluded", "coverage_truth_excluded",
    "reusable_blk_link_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})

_REQUEST_KEYS_172 = frozenset({
    "decision_execution_package_id", "operator_identity", "decision_execution_scope", "selected_frontier",
    "upstream_authority_request_package_id", "upstream_authority_request_package_hash",
    "approval_id", "run_id_to_consume", "beo_id", "beb_id", "exact_trace_identities",
    "metadata_drift_status", "metadata_coverage_status", "operator_decision_text_raw",
    "decided_at", "requested_at", "expires_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_172,
})
_CONTEXT_KEYS_173 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_decision_execution_package_id", "upstream_decision_execution_package_hash",
    "run_id_consumed", "beo_id", "beb_id", "exact_trace_identities",
    "metadata_drift_status_observed", "metadata_coverage_status_observed",
    "metadata_bound_decision_recorded_observed", "observed_failure_requires_174_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_173,
})
_REQUEST_KEYS_174 = frozenset({
    "authority_request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_decision_execution_package_hash", "beo_id", "beb_id", "exact_trace_identities",
    "request_future_exact_protected_body_verification_approval", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations",
    "excluded_authorities", *SIDE_EFFECT_FLAGS_174,
})


def valid_metadata_bound_drift_coverage_decision_execution_172(request171: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_172,
        "operator_identity": request171["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_172,
        "selected_frontier": SELECTED_FRONTIER_172,
        "upstream_authority_request_package_id": request171["authority_request_package_id"],
        "upstream_authority_request_package_hash": request171["authority_request_package_hash"],
        "approval_id": APPROVAL_ID_172,
        "run_id_to_consume": RUN_ID_CONSUMED_172,
        "beo_id": request171["beo_id"], "beb_id": request171["beb_id"],
        "exact_trace_identities": list(request171["exact_trace_identities"]),
        "metadata_drift_status": METADATA_DRIFT_STATUS_172,
        "metadata_coverage_status": METADATA_COVERAGE_STATUS_172,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_172,
        "decided_at": "2099-05-16T21:05:00+10:00",
        "requested_at": "2099-05-16T21:06:00+10:00",
        "expires_at": "2099-05-16T21:15:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_172},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_172),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_172),
    }
    for flag in SIDE_EFFECT_FLAGS_172:
        record[flag] = False
    record["operator_decision_captured"] = True
    record["one_run_id_consumed_in_record_only_evidence"] = True
    record["metadata_bound_drift_coverage_decision_recorded"] = True
    record.update(overrides)
    return record


def build_metadata_bound_drift_coverage_decision_execution_172(request171_package: dict[str, Any], decision172: dict[str, Any]) -> dict[str, Any]:
    request171 = _validate_171_package(request171_package)
    decision = _validate_request_like(
        decision172, _REQUEST_KEYS_172, _ATTESTATION_172, EXACT_PROOF_OBLIGATIONS_172,
        EXACT_EXCLUDED_AUTHORITIES_172, SIDE_EFFECT_FLAGS_172,
        true_flags={"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "metadata_bound_drift_coverage_decision_recorded"},
    )
    _scan_high_risk_freeform(decision["operator_identity"], "operator_identity")
    _require(decision, "decision_execution_package_id", DECISION_EXECUTION_PACKAGE_ID_172)
    _require(decision, "decision_execution_scope", DECISION_EXECUTION_SCOPE_172)
    _require(decision, "selected_frontier", SELECTED_FRONTIER_172)
    _require(decision, "approval_id", APPROVAL_ID_172)
    _require(decision, "run_id_to_consume", RUN_ID_CONSUMED_172)
    _require(decision, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_172)
    _require(decision, "metadata_drift_status", METADATA_DRIFT_STATUS_172)
    _require(decision, "metadata_coverage_status", METADATA_COVERAGE_STATUS_172)
    _require_matching_upstream(decision, request171, (
        ("upstream_authority_request_package_id", "authority_request_package_id"),
        ("upstream_authority_request_package_hash", "authority_request_package_hash"),
        ("operator_identity", "operator_identity"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_decision_window(decision["decided_at"], decision["requested_at"], decision["expires_at"], request171["requested_at"], request171["expires_at"])
    trace_ids = _validate_trace_copy(decision["exact_trace_identities"], request171["exact_trace_identities"])
    package = {
        "decision_execution_status": DECISION_EXECUTION_STATUS_172,
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_172,
        "operator_identity": decision["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_172,
        "selected_frontier": SELECTED_FRONTIER_172,
        "upstream_authority_request_package_id": request171["authority_request_package_id"],
        "upstream_authority_request_package_hash": request171["authority_request_package_hash"],
        "approval_id": APPROVAL_ID_172,
        "run_id_consumed": RUN_ID_CONSUMED_172,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_172,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "metadata_bound_drift_coverage_decision_recorded": True,
        "metadata_drift_status": METADATA_DRIFT_STATUS_172,
        "metadata_coverage_status": METADATA_COVERAGE_STATUS_172,
        "beo_id": request171["beo_id"], "beb_id": request171["beb_id"],
        "exact_trace_identities": trace_ids,
        "decision_execution_request_hash": _canonical_hash(decision),
        "decided_at": decision["decided_at"], "requested_at": decision["requested_at"], "expires_at": decision["expires_at"],
        "expired": False, "replayed": False, "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_172,
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_172),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_172),
    }
    for flag in SIDE_EFFECT_FLAGS_172:
        package[flag] = False
    package["operator_decision_captured"] = True
    package["one_run_id_consumed_in_record_only_evidence"] = True
    package["metadata_bound_drift_coverage_decision_recorded"] = True
    package["decision_execution_package_hash"] = _canonical_hash(package)
    return package


def valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_173,
        "operator_identity": decision172["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_173,
        "selected_frontier": SELECTED_FRONTIER_173,
        "upstream_decision_execution_package_id": decision172["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": decision172["decision_execution_package_hash"],
        "run_id_consumed": decision172["run_id_consumed"],
        "beo_id": decision172["beo_id"], "beb_id": decision172["beb_id"],
        "exact_trace_identities": list(decision172["exact_trace_identities"]),
        "metadata_drift_status_observed": decision172["metadata_drift_status"],
        "metadata_coverage_status_observed": decision172["metadata_coverage_status"],
        "metadata_bound_decision_recorded_observed": decision172["metadata_bound_drift_coverage_decision_recorded"],
        "observed_failure_requires_174_hardening": False,
        "reconciled_at": "2099-05-16T21:20:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_173},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_173),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_173),
    }
    for flag in SIDE_EFFECT_FLAGS_173:
        record[flag] = False
    record.update(overrides)
    return record


def build_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172_package: dict[str, Any], context173: dict[str, Any]) -> dict[str, Any]:
    decision = _validate_172_package(decision172_package)
    context = _validate_request_like(context173, _CONTEXT_KEYS_173, _ATTESTATION_173, EXACT_PROOF_OBLIGATIONS_173, EXACT_EXCLUDED_AUTHORITIES_173, SIDE_EFFECT_FLAGS_173)
    _scan_high_risk_freeform(context["operator_identity"], "operator_identity")
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_173)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_173)
    _require(context, "selected_frontier", SELECTED_FRONTIER_173)
    _require_false(context, "observed_failure_requires_174_hardening")
    _require_matching_upstream(context, decision, (
        ("upstream_decision_execution_package_id", "decision_execution_package_id"),
        ("upstream_decision_execution_package_hash", "decision_execution_package_hash"),
        ("operator_identity", "operator_identity"),
        ("run_id_consumed", "run_id_consumed"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], decision["exact_trace_identities"])
    if context["metadata_drift_status_observed"] != decision["metadata_drift_status"]:
        raise ValueError("metadata_drift_status_observed must match BLK-172 evidence")
    if context["metadata_coverage_status_observed"] != decision["metadata_coverage_status"]:
        raise ValueError("metadata_coverage_status_observed must match BLK-172 evidence")
    _require_true(context, "metadata_bound_decision_recorded_observed")
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_173,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_173,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_173,
        "selected_frontier": SELECTED_FRONTIER_173,
        "upstream_decision_execution_package_id": decision["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": decision["decision_execution_package_hash"],
        "run_id_consumed": decision["run_id_consumed"],
        "beo_id": decision["beo_id"], "beb_id": decision["beb_id"],
        "exact_trace_identities": trace_ids,
        "metadata_drift_status": decision["metadata_drift_status"],
        "metadata_coverage_status": decision["metadata_coverage_status"],
        "clean_metadata_bound_decision_reconciled": True,
        "observed_failure_requires_174_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_173_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_173),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_173),
    }
    for flag in SIDE_EFFECT_FLAGS_173:
        package[flag] = False
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def valid_protected_body_verification_authority_request_174(reconciliation173: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "authority_request_package_id": REQUEST_PACKAGE_ID_174,
        "operator_identity": reconciliation173["operator_identity"],
        "request_scope": REQUEST_SCOPE_174,
        "selected_frontier": SELECTED_FRONTIER_174,
        "upstream_reconciliation_package_id": reconciliation173["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation173["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": reconciliation173["upstream_decision_execution_package_hash"],
        "beo_id": reconciliation173["beo_id"], "beb_id": reconciliation173["beb_id"],
        "exact_trace_identities": list(reconciliation173["exact_trace_identities"]),
        "request_future_exact_protected_body_verification_approval": True,
        "requested_at": "2099-05-16T21:25:00+10:00",
        "expires_at": "2099-05-17T21:25:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_174},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_174),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_174),
    }
    for flag in SIDE_EFFECT_FLAGS_174:
        record[flag] = False
    record.update(overrides)
    return record


def build_protected_body_verification_authority_request_174(reconciliation173: dict[str, Any], request174: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_173_package(reconciliation173)
    request = _validate_request_like(request174, _REQUEST_KEYS_174, _ATTESTATION_174, EXACT_PROOF_OBLIGATIONS_174, EXACT_EXCLUDED_AUTHORITIES_174, SIDE_EFFECT_FLAGS_174)
    _scan_high_risk_freeform(request["operator_identity"], "operator_identity")
    _require(request, "authority_request_package_id", REQUEST_PACKAGE_ID_174)
    _require(request, "request_scope", REQUEST_SCOPE_174)
    _require(request, "selected_frontier", SELECTED_FRONTIER_174)
    _require_true(request, "request_future_exact_protected_body_verification_approval")
    _require_matching_upstream(request, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_decision_execution_package_hash", "upstream_decision_execution_package_hash"),
        ("operator_identity", "operator_identity"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(request["requested_at"], request["expires_at"], "authority request")
    trace_ids = _validate_trace_copy(request["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS_174,
        "authority_request_package_id": REQUEST_PACKAGE_ID_174,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_174,
        "selected_frontier": SELECTED_FRONTIER_174,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": upstream["upstream_decision_execution_package_hash"],
        "beo_id": upstream["beo_id"], "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "request_future_exact_protected_body_verification_approval": True,
        "approval_capture_performed": False,
        "protected_body_reads": False,
        "protected_body_hashing_attempted": False,
        "coverage_truth_established": False,
        "rtm_drift_rejection_performed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_174,
        "authority_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"], "expires_at": request["expires_at"],
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_174),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_174),
    }
    for flag in SIDE_EFFECT_FLAGS_174:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(package)
    return package


def _scan_high_risk_freeform(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    compact = "".join(ch.lower() for ch in value if ch.isascii() and ch.isalnum())
    forbidden = (
        "driftrejectionexecuted", "driftrejectionauthorized", "driftdecisionauthorized",
        "coveragetruthauthorized", "coveragetruthestablished", "coveragematrixgenerated",
        "protectedbodyreadsapproved", "protectedbodyverificationapproved", "protectedbodyreadsauthorized",
        "rtmgeneration", "rtmgenerated", "activevaulthashcomparisonauthorized",
        "beopublicationauthorized", "publishbeo", "codexapproval", "blkpipesuccess",
        "blktestpassapproval", "productionisolationclaimed",
    )
    if any(token in compact for token in forbidden):
        raise ValueError(f"authority-laundering text in {label}")


def _validate_171_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-171 package must be a dictionary")
    if package.get("request_status") != REQUEST_STATUS_171:
        raise ValueError("request_status must be exact BLK-171 status")
    if package.get("authority_request_package_id") != REQUEST_PACKAGE_ID_171:
        raise ValueError("authority_request_package_id must be exact BLK-171 id")
    _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"})
    if package["authority_request_package_hash"] != computed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-171 package")
    if package["authority_request_package_hash"] != CANONICAL_BLK171_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-171 authority request package hash mismatch")
    if set(package.get("proof_obligations", [])) != EXACT_PROOF_OBLIGATIONS_171:
        raise ValueError("BLK-171 proof obligations must be exact")
    if set(package.get("excluded_authorities", [])) != EXACT_EXCLUDED_AUTHORITIES_171:
        raise ValueError("BLK-171 excluded authorities must be exact")
    _require(package, "request_scope", REQUEST_SCOPE_171)
    _require(package, "selected_frontier", SELECTED_FRONTIER_171)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_171)
    _require_true(package, "request_future_exact_metadata_bound_drift_coverage_decision_approval")
    if package.get("upstream_reconciliation_package_hash") != CANONICAL_BLK170_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-171 must bind canonical BLK-170 reconciliation package hash")
    if package.get("upstream_comparison_record_hash") != CANONICAL_BLK169_COMPARISON_RECORD_HASH:
        raise ValueError("BLK-171 must bind canonical BLK-169 comparison record hash")
    for flag in SIDE_EFFECT_FLAGS_171:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-171 package {flag} must remain false")
    return package


def _validate_172_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-172 package must be a dictionary")
    if package.get("decision_execution_package_id") != DECISION_EXECUTION_PACKAGE_ID_172:
        raise ValueError("decision_execution_package_id must be exact BLK-172 id")
    _required_hash(package.get("decision_execution_package_hash"), "decision_execution_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"})
    if package["decision_execution_package_hash"] != computed:
        raise ValueError("decision_execution_package_hash does not match submitted BLK-172 package")
    if package["decision_execution_package_hash"] != CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-172 decision execution package hash mismatch")
    _require(package, "decision_execution_scope", DECISION_EXECUTION_SCOPE_172)
    _require(package, "selected_frontier", SELECTED_FRONTIER_172)
    _require(package, "approval_id", APPROVAL_ID_172)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_172)
    _require(package, "metadata_drift_status", METADATA_DRIFT_STATUS_172)
    _require(package, "metadata_coverage_status", METADATA_COVERAGE_STATUS_172)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_172)
    if set(package.get("proof_obligations", [])) != EXACT_PROOF_OBLIGATIONS_172:
        raise ValueError("BLK-172 proof obligations must be exact")
    if set(package.get("excluded_authorities", [])) != EXACT_EXCLUDED_AUTHORITIES_172:
        raise ValueError("BLK-172 excluded authorities must be exact")
    for flag in SIDE_EFFECT_FLAGS_172:
        expected = flag in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "metadata_bound_drift_coverage_decision_recorded"}
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-172 package {flag} must be {expected}")
    if package.get("upstream_authority_request_package_hash") != CANONICAL_BLK171_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("BLK-172 must bind canonical BLK-171 package hash")
    return package


def _validate_173_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-173 package must be a dictionary")
    if package.get("reconciliation_package_id") != RECONCILIATION_PACKAGE_ID_173:
        raise ValueError("reconciliation_package_id must be exact BLK-173 id")
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-173 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-173 reconciliation package hash mismatch")
    if package.get("clean_metadata_bound_decision_reconciled") is not True:
        raise ValueError("BLK-173 must be clean before BLK-174 request")
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_173)
    _require(package, "selected_frontier", SELECTED_FRONTIER_173)
    _require(package, "recommended_next_frontier", NEXT_FRONTIER_173_CLEAN)
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-173 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_173:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-173 package {flag} must remain false")
    if package.get("upstream_decision_execution_package_hash") != CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-173 must bind canonical BLK-172 package hash")
    return package
