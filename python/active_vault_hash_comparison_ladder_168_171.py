"""BLK-SYSTEM-168..171 active-vault metadata/hash comparison ladder.

This deterministic fixture group starts from the clean BLK-SYSTEM-167 production
blk-link / RTM trace-closure reconciliation. It emits a request-only metadata/hash
active-vault comparison package (168), captures the operator's exact directive and
consumes one run ID in record-only metadata/hash comparison evidence (169),
reconciles the clean comparison (170), and emits a request-only next-authority
package for future metadata-bound drift/coverage decision approval (171).

It does not read active-vault files, read/copy/parse/hash/scan protected BLK-req
bodies, generate RTM, reject drift, establish coverage truth, run reusable
production blk-link, mutate target/source/Git state, run BLK-pipe/BLK-test/Codex
or other tooling, reuse signer/storage/ledger authority, or claim production
isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_trace_closure_approval_capture import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from production_blk_link_rtm_trace_closure_post_run_reconciliation_167 import (
    CANONICAL_BLK166_DECISION_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK166_EXECUTION_RECORD_HASH,
    RECONCILIATION_PACKAGE_ID_167,
    RECONCILIATION_STATUS_167,
)

REQUEST_STATUS_168 = "ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_READY_AFTER_CLEAN_BLK167_NOT_APPROVED"
REQUEST_PACKAGE_ID_168 = "ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-168-001"
REQUEST_SCOPE_168 = "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER_168 = "active_vault_hash_comparison_metadata_hash_only_request_168"
NEXT_REQUIRED_AUTHORITY_168 = "EXACT_APPROVAL_AND_ONE_RUN_METADATA_HASH_COMPARISON_REQUIRED_NOT_GRANTED"
CANONICAL_BLK167_RECONCILIATION_PACKAGE_HASH = "sha256:bd21f023612b74c86ded80a67c9d3e3a1f3dea6ee90342b31ca8f000dae0258c"
CANONICAL_BLK168_AUTHORITY_REQUEST_PACKAGE_HASH = "sha256:a653775c143a43b821e5443d38abc275f082b7d57a8f87f0bb50bd538b7da765"

STATUS_169 = "ACTIVE_VAULT_HASH_COMPARISON_DECISION_CAPTURED_AND_ONE_RUN_RECORDED_FOR_EXACT_BLK168_REQUEST"
DECISION_EXECUTION_PACKAGE_ID_169 = "ACTIVE-VAULT-HASH-COMPARISON-DECISION-EXECUTION-169-001"
COMPARISON_RECORD_ID_169 = "ACTIVE-VAULT-HASH-COMPARISON-RECORD-169-001"
APPROVAL_ID_169 = "APPROVAL-BLK-SYSTEM-168-ACTIVE-VAULT-HASH-COMPARISON-001"
RUN_ID_CONSUMED_169 = "RUN-BLK-SYSTEM-169-ACTIVE-VAULT-HASH-COMPARISON-001"
DECISION_EXECUTION_SCOPE_169 = "EXACT_METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_DECISION_AND_ONE_RUN_RECORD_ONLY"
SELECTED_FRONTIER_169 = "active_vault_hash_comparison_metadata_hash_only_decision_execution_169"
NEXT_REQUIRED_AUTHORITY_169 = "POST_COMPARISON_RECONCILIATION_REQUIRED_NOT_STARTED"
EXACT_OPERATOR_DECISION_TEXT_169 = (
    "APPROVE ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-168-001 FOR ONE "
    "METADATA-HASH-ONLY ACTIVE-VAULT COMPARISON RUN "
    "RUN-BLK-SYSTEM-169-ACTIVE-VAULT-HASH-COMPARISON-001; NO PROTECTED BODY READS; "
    "NO RTM GENERATION; NO DRIFT REJECTION; NO COVERAGE TRUTH; NO MUTATION."
)
MATCH_RESULT_169 = "ACTIVE_VAULT_METADATA_HASHES_MATCH_RECORDED_NOT_DRIFT_DECISION"
MISMATCH_RESULT_169 = "ACTIVE_VAULT_METADATA_HASH_MISMATCH_RECORDED_NOT_DRIFT_DECISION"
CANONICAL_BLK169_DECISION_EXECUTION_PACKAGE_HASH = "sha256:b207c76e213461d7040fa9edf78f7c30d9d45a72ec957dc31e824ba003b25c1a"
CANONICAL_BLK169_COMPARISON_RECORD_HASH = "sha256:1c7bb668c973b8624172fe07a5d6366166c4ff64110d3b9eefabb503d7ebbc9b"

RECONCILIATION_STATUS_170 = "ACTIVE_VAULT_HASH_COMPARISON_POST_RUN_RECONCILED_CLEAN_AFTER_BLK169"
RECONCILIATION_PACKAGE_ID_170 = "ACTIVE-VAULT-HASH-COMPARISON-POST-RUN-RECONCILIATION-170-001"
RECONCILIATION_SCOPE_170 = "POST_ACTIVE_VAULT_HASH_COMPARISON_RECONCILIATION_ONLY_NO_NEW_AUTHORITY"
SELECTED_FRONTIER_170 = "active_vault_hash_comparison_post_run_reconciliation_170"
NEXT_FRONTIER_170_CLEAN = "NEXT_FRONTIER_METADATA_BOUND_DRIFT_COVERAGE_DECISION_REQUEST_NOT_GRANTED"
CANONICAL_BLK170_RECONCILIATION_PACKAGE_HASH = "sha256:61fadcc8668b945131e2564094018536cc9dfa1132d2accea79063f6d177cac2"

REQUEST_STATUS_171 = "METADATA_BOUND_DRIFT_COVERAGE_DECISION_AUTHORITY_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID_171 = "METADATA-BOUND-DRIFT-COVERAGE-DECISION-AUTHORITY-REQUEST-171-001"
REQUEST_SCOPE_171 = "METADATA_BOUND_DRIFT_COVERAGE_DECISION_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER_171 = "metadata_bound_drift_coverage_decision_request_171"
NEXT_REQUIRED_AUTHORITY_171 = "EXACT_METADATA_BOUND_DRIFT_COVERAGE_DECISION_APPROVAL_REQUIRED_NOT_GRANTED"
CANONICAL_BLK171_AUTHORITY_REQUEST_PACKAGE_HASH = "sha256:51d9bedac505a86e1b92447b50edf2fe4bf0c688452d12e8d9d1d25e5fa3749e"

SIDE_EFFECT_FLAGS_168 = (
    "approval_capture_performed",
    "future_run_id_reserved_or_consumed",
    "active_vault_hash_comparison_performed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
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

SIDE_EFFECT_FLAGS_169 = tuple(
    flag for flag in SIDE_EFFECT_FLAGS_168 if flag not in {"approval_capture_performed", "future_run_id_reserved_or_consumed"}
) + (
    "operator_decision_captured",
    "one_run_id_consumed_in_record_only_evidence",
)

SIDE_EFFECT_FLAGS_170 = (
    "next_frontier_granted",
    "observed_failure_hardening_performed",
    *SIDE_EFFECT_FLAGS_168,
)

SIDE_EFFECT_FLAGS_171 = SIDE_EFFECT_FLAGS_168

_BASE_EXCLUDED = {
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_COMPARISON_BEYOND_EXACT_APPROVED_IDENTITIES",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
    "REUSABLE_ACTIVE_VAULT_COMPARISON_AUTHORITY",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
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

EXACT_EXCLUDED_AUTHORITIES_168 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_THIS_SPRINT",
}
EXACT_EXCLUDED_AUTHORITIES_169 = _BASE_EXCLUDED | {
    "DRIFT_OR_COVERAGE_INTERPRETATION_FROM_METADATA_MATCH",
    "RUN_ID_REUSE_AFTER_RECORD_ONLY_CONSUMPTION",
}
EXACT_EXCLUDED_AUTHORITIES_170 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "DRIFT_OR_COVERAGE_DECISION_BY_RECONCILIATION",
}
EXACT_EXCLUDED_AUTHORITIES_171 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "DRIFT_OR_COVERAGE_DECISION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_REQUEST_ONLY_PACKAGE",
}

EXACT_PROOF_OBLIGATIONS_168 = {
    "BLK167_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK166_DECISION_EXECUTION_HASH_BOUND_THROUGH_BLK167",
    "REQUEST_LIMITED_TO_METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE_OR_EXECUTION",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_EXECUTION",
}
EXACT_PROOF_OBLIGATIONS_169 = {
    "BLK168_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "OPERATOR_DECISION_CAPTURED_FOR_EXACT_BLK168_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_REQUEST",
    "RUN_ID_CONSUMED_ONCE_IN_RECORD_ONLY_EVIDENCE",
    "COMPARISON_LIMITED_TO_CALLER_SUPPLIED_METADATA_HASH_RECORDS",
    "ACTIVE_VAULT_FILESYSTEM_NOT_READ_OR_SCANNED",
    "METADATA_HASH_MATCH_OR_MISMATCH_RECORDED_WITHOUT_DRIFT_DECISION",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "POST_COMPARISON_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
}
EXACT_PROOF_OBLIGATIONS_170 = {
    "BLK169_DECISION_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK169_COMPARISON_RECORD_HASH_RECOMPUTED_AND_BOUND",
    "CLEAN_METADATA_HASH_COMPARISON_RECONCILED_WITHOUT_DRIFT_DECISION",
    "NEXT_FRONTIER_NAMED_WITH_AUTHORITY_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_171_HARDENING",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_171 = {
    "BLK170_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK169_COMPARISON_RECORD_HASH_BOUND_THROUGH_BLK170",
    "REQUEST_LIMITED_TO_FUTURE_METADATA_BOUND_DRIFT_COVERAGE_DECISION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE_OR_DECISION_EXECUTION",
    "DRIFT_REJECTION_AND_COVERAGE_TRUTH_NOT_PERFORMED_BY_REQUEST",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}

_REQUEST_KEYS_168 = frozenset({
    "authority_request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_decision_execution_package_hash", "upstream_execution_record_hash", "beo_id", "beb_id",
    "exact_trace_identities", "request_future_exact_metadata_hash_only_active_vault_comparison",
    "requested_at", "expires_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_168,
})

_REQUEST_KEYS_169 = frozenset({
    "decision_execution_package_id", "operator_identity", "decision_execution_scope", "selected_frontier",
    "upstream_authority_request_package_id", "upstream_authority_request_package_hash",
    "approval_id", "run_id_to_consume", "beo_id", "beb_id", "exact_trace_identities",
    "active_metadata_records", "operator_decision_text_raw", "decided_at", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_169,
})

_CONTEXT_KEYS_170 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_decision_execution_package_id", "upstream_decision_execution_package_hash",
    "upstream_comparison_record_id", "upstream_comparison_record_hash", "run_id_consumed", "beo_id", "beb_id",
    "exact_trace_identities", "metadata_hashes_match_observed", "observed_failure_requires_171_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations",
    "excluded_authorities", *SIDE_EFFECT_FLAGS_170,
})

_REQUEST_KEYS_171 = frozenset({
    "authority_request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_decision_execution_package_hash", "upstream_comparison_record_hash", "beo_id", "beb_id",
    "exact_trace_identities", "request_future_exact_metadata_bound_drift_coverage_decision_approval",
    "requested_at", "expires_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_171,
})

_ATTESTATION_168 = frozenset({
    "exact_blk167_reconciliation_reviewed", "metadata_hash_only_scope_preserved", "approval_capture_not_performed",
    "comparison_not_performed", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_169 = frozenset({
    "exact_blk168_request_reviewed", "operator_decision_captured_from_latest_directive",
    "run_id_consumed_once_in_record_only_evidence", "metadata_hash_only_scope_preserved",
    "no_active_vault_filesystem_read", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_170 = frozenset({
    "exact_blk169_execution_reviewed", "comparison_record_hash_verified", "reconciliation_only_not_authority_request",
    "clean_comparison_interpreted_without_drift_decision", "no_observed_failure_requiring_hardening",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded", "coverage_truth_excluded",
    "reusable_blk_link_excluded", "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})
_ATTESTATION_171 = frozenset({
    "exact_blk170_reconciliation_reviewed", "request_is_for_future_approval_not_approval",
    "drift_coverage_decision_not_performed", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})

_METADATA_RECORD_KEYS = frozenset({
    "kind", "id", "version_hash", "metadata_source", "body_included", "body_read", "body_copied",
    "body_hashed", "body_parsed", "body_scanned", "protected_path_accessed",
})
_METADATA_FALSE_FLAGS = ("body_included", "body_read", "body_copied", "body_hashed", "body_parsed", "body_scanned", "protected_path_accessed")


def valid_active_vault_hash_comparison_authority_request_168(reconciliation167: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "authority_request_package_id": REQUEST_PACKAGE_ID_168,
        "operator_identity": reconciliation167["operator_identity"],
        "request_scope": REQUEST_SCOPE_168,
        "selected_frontier": SELECTED_FRONTIER_168,
        "upstream_reconciliation_package_id": reconciliation167["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation167["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": reconciliation167["upstream_decision_execution_package_hash"],
        "upstream_execution_record_hash": reconciliation167["upstream_execution_record_hash"],
        "beo_id": reconciliation167["beo_id"],
        "beb_id": reconciliation167["beb_id"],
        "exact_trace_identities": list(reconciliation167["exact_trace_identities"]),
        "request_future_exact_metadata_hash_only_active_vault_comparison": True,
        "requested_at": "2099-05-16T20:30:00+10:00",
        "expires_at": "2099-05-17T20:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_168},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_168),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_168),
    }
    for flag in SIDE_EFFECT_FLAGS_168:
        record[flag] = False
    record.update(overrides)
    return record


def build_active_vault_hash_comparison_authority_request_168(reconciliation167: dict[str, Any], request168: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_blk167_reconciliation_package(reconciliation167)
    request = _validate_request_like(request168, _REQUEST_KEYS_168, _ATTESTATION_168, EXACT_PROOF_OBLIGATIONS_168, EXACT_EXCLUDED_AUTHORITIES_168, SIDE_EFFECT_FLAGS_168)
    _require(request, "authority_request_package_id", REQUEST_PACKAGE_ID_168)
    _require(request, "request_scope", REQUEST_SCOPE_168)
    _require(request, "selected_frontier", SELECTED_FRONTIER_168)
    _require_true(request, "request_future_exact_metadata_hash_only_active_vault_comparison")
    _require_matching_upstream(request, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_decision_execution_package_hash", "upstream_decision_execution_package_hash"),
        ("upstream_execution_record_hash", "upstream_execution_record_hash"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(request["requested_at"], request["expires_at"], "authority request")
    trace_ids = _validate_trace_copy(request["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS_168,
        "authority_request_package_id": REQUEST_PACKAGE_ID_168,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_168,
        "selected_frontier": SELECTED_FRONTIER_168,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": upstream["upstream_decision_execution_package_hash"],
        "upstream_execution_record_hash": upstream["upstream_execution_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "request_future_exact_metadata_hash_only_active_vault_comparison": True,
        "approval_capture_performed": False,
        "active_vault_hash_comparison_performed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_168,
        "authority_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_168),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_168),
    }
    for flag in SIDE_EFFECT_FLAGS_168:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(package)
    return package


def valid_active_vault_hash_comparison_decision_execution_169(request168: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_169,
        "operator_identity": request168["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_169,
        "selected_frontier": SELECTED_FRONTIER_169,
        "upstream_authority_request_package_id": request168["authority_request_package_id"],
        "upstream_authority_request_package_hash": request168["authority_request_package_hash"],
        "approval_id": APPROVAL_ID_169,
        "run_id_to_consume": RUN_ID_CONSUMED_169,
        "beo_id": request168["beo_id"],
        "beb_id": request168["beb_id"],
        "exact_trace_identities": list(request168["exact_trace_identities"]),
        "active_metadata_records": _metadata_records_from_trace_ids(request168["exact_trace_identities"]),
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_169,
        "decided_at": "2099-05-16T20:35:00+10:00",
        "requested_at": "2099-05-16T20:36:00+10:00",
        "expires_at": "2099-05-16T20:45:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_169},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_169),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_169),
    }
    for flag in SIDE_EFFECT_FLAGS_169:
        record[flag] = False
    record["operator_decision_captured"] = True
    record["one_run_id_consumed_in_record_only_evidence"] = True
    record["active_vault_hash_comparison_performed"] = True
    record.update(overrides)
    return record


def build_active_vault_hash_comparison_decision_execution_169(request168_package: dict[str, Any], execution169: dict[str, Any]) -> dict[str, Any]:
    request168 = _validate_168_package(request168_package)
    execution = _validate_request_like(
        execution169, _REQUEST_KEYS_169, _ATTESTATION_169, EXACT_PROOF_OBLIGATIONS_169, EXACT_EXCLUDED_AUTHORITIES_169,
        SIDE_EFFECT_FLAGS_169, true_flags={"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "active_vault_hash_comparison_performed"}
    )
    _require(execution, "decision_execution_package_id", DECISION_EXECUTION_PACKAGE_ID_169)
    _require(execution, "decision_execution_scope", DECISION_EXECUTION_SCOPE_169)
    _require(execution, "selected_frontier", SELECTED_FRONTIER_169)
    _require(execution, "approval_id", APPROVAL_ID_169)
    _require(execution, "run_id_to_consume", RUN_ID_CONSUMED_169)
    _require(execution, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_169)
    _require_matching_upstream(execution, request168, (
        ("upstream_authority_request_package_id", "authority_request_package_id"),
        ("upstream_authority_request_package_hash", "authority_request_package_hash"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_decision_window(execution["decided_at"], execution["requested_at"], execution["expires_at"], request168["requested_at"], request168["expires_at"])
    trace_ids = _validate_trace_copy(execution["exact_trace_identities"], request168["exact_trace_identities"])
    observed = _validate_active_metadata_records(execution["active_metadata_records"], trace_ids)
    record = _build_comparison_record(execution, trace_ids, observed)
    package = {
        "decision_execution_status": STATUS_169,
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_169,
        "operator_identity": execution["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_169,
        "selected_frontier": SELECTED_FRONTIER_169,
        "upstream_authority_request_package_id": request168["authority_request_package_id"],
        "upstream_authority_request_package_hash": request168["authority_request_package_hash"],
        "approval_id": APPROVAL_ID_169,
        "run_id_consumed": RUN_ID_CONSUMED_169,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_169,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "beo_id": request168["beo_id"], "beb_id": request168["beb_id"],
        "exact_trace_identities": trace_ids,
        "active_metadata_records": deepcopy(observed),
        "active_vault_hash_comparison_performed": True,
        "metadata_hashes_match": record["metadata_hashes_match"],
        "comparison_result": MATCH_RESULT_169 if record["metadata_hashes_match"] else MISMATCH_RESULT_169,
        "comparison_record_id": COMPARISON_RECORD_ID_169,
        "comparison_record": record,
        "comparison_record_hash": record["comparison_record_hash"],
        "decision_execution_request_hash": _canonical_hash(execution),
        "decided_at": execution["decided_at"], "requested_at": execution["requested_at"], "expires_at": execution["expires_at"],
        "expired": False, "replayed": False, "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_169,
        "operator_attestation": deepcopy(execution["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_169),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_169),
    }
    for flag in SIDE_EFFECT_FLAGS_169:
        package[flag] = False
    package["operator_decision_captured"] = True
    package["one_run_id_consumed_in_record_only_evidence"] = True
    package["active_vault_hash_comparison_performed"] = True
    package["decision_execution_package_hash"] = _canonical_hash(package)
    return package


def valid_active_vault_hash_comparison_post_run_reconciliation_170(execution169: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_170,
        "operator_identity": execution169["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_170,
        "selected_frontier": SELECTED_FRONTIER_170,
        "upstream_decision_execution_package_id": execution169["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": execution169["decision_execution_package_hash"],
        "upstream_comparison_record_id": execution169["comparison_record_id"],
        "upstream_comparison_record_hash": execution169["comparison_record_hash"],
        "run_id_consumed": execution169["run_id_consumed"],
        "beo_id": execution169["beo_id"], "beb_id": execution169["beb_id"],
        "exact_trace_identities": list(execution169["exact_trace_identities"]),
        "metadata_hashes_match_observed": execution169["metadata_hashes_match"],
        "observed_failure_requires_171_hardening": False,
        "reconciled_at": "2099-05-16T20:50:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_170},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_170),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_170),
    }
    for flag in SIDE_EFFECT_FLAGS_170:
        record[flag] = False
    record.update(overrides)
    return record


def build_active_vault_hash_comparison_post_run_reconciliation_170(execution169_package: dict[str, Any], context170: dict[str, Any]) -> dict[str, Any]:
    execution = _validate_169_package(execution169_package)
    context = _validate_request_like(context170, _CONTEXT_KEYS_170, _ATTESTATION_170, EXACT_PROOF_OBLIGATIONS_170, EXACT_EXCLUDED_AUTHORITIES_170, SIDE_EFFECT_FLAGS_170)
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_170)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_170)
    _require(context, "selected_frontier", SELECTED_FRONTIER_170)
    _require_false(context, "observed_failure_requires_171_hardening")
    _require_matching_upstream(context, execution, (
        ("upstream_decision_execution_package_id", "decision_execution_package_id"),
        ("upstream_decision_execution_package_hash", "decision_execution_package_hash"),
        ("upstream_comparison_record_id", "comparison_record_id"),
        ("upstream_comparison_record_hash", "comparison_record_hash"),
        ("run_id_consumed", "run_id_consumed"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], execution["exact_trace_identities"])
    if context["metadata_hashes_match_observed"] is not execution["metadata_hashes_match"]:
        raise ValueError("metadata_hashes_match_observed must match BLK-169 evidence")
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_170,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_170,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_170,
        "selected_frontier": SELECTED_FRONTIER_170,
        "upstream_decision_execution_package_id": execution["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": execution["decision_execution_package_hash"],
        "upstream_comparison_record_id": execution["comparison_record_id"],
        "upstream_comparison_record_hash": execution["comparison_record_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"], "beb_id": execution["beb_id"],
        "exact_trace_identities": trace_ids,
        "metadata_hashes_match": execution["metadata_hashes_match"],
        "clean_metadata_hash_comparison_reconciled": execution["metadata_hashes_match"],
        "observed_failure_requires_171_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_170_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_170),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_170),
    }
    for flag in SIDE_EFFECT_FLAGS_170:
        package[flag] = False
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def valid_metadata_bound_drift_coverage_decision_request_171(reconciliation170: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "authority_request_package_id": REQUEST_PACKAGE_ID_171,
        "operator_identity": reconciliation170["operator_identity"],
        "request_scope": REQUEST_SCOPE_171,
        "selected_frontier": SELECTED_FRONTIER_171,
        "upstream_reconciliation_package_id": reconciliation170["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation170["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": reconciliation170["upstream_decision_execution_package_hash"],
        "upstream_comparison_record_hash": reconciliation170["upstream_comparison_record_hash"],
        "beo_id": reconciliation170["beo_id"], "beb_id": reconciliation170["beb_id"],
        "exact_trace_identities": list(reconciliation170["exact_trace_identities"]),
        "request_future_exact_metadata_bound_drift_coverage_decision_approval": True,
        "requested_at": "2099-05-16T20:55:00+10:00",
        "expires_at": "2099-05-17T20:55:00+10:00",
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_171},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_171),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_171),
    }
    for flag in SIDE_EFFECT_FLAGS_171:
        record[flag] = False
    record.update(overrides)
    return record


def build_metadata_bound_drift_coverage_decision_request_171(reconciliation170: dict[str, Any], request171: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_170_package(reconciliation170)
    request = _validate_request_like(request171, _REQUEST_KEYS_171, _ATTESTATION_171, EXACT_PROOF_OBLIGATIONS_171, EXACT_EXCLUDED_AUTHORITIES_171, SIDE_EFFECT_FLAGS_171)
    _require(request, "authority_request_package_id", REQUEST_PACKAGE_ID_171)
    _require(request, "request_scope", REQUEST_SCOPE_171)
    _require(request, "selected_frontier", SELECTED_FRONTIER_171)
    _require_true(request, "request_future_exact_metadata_bound_drift_coverage_decision_approval")
    _require_matching_upstream(request, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_decision_execution_package_hash", "upstream_decision_execution_package_hash"),
        ("upstream_comparison_record_hash", "upstream_comparison_record_hash"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(request["requested_at"], request["expires_at"], "authority request")
    trace_ids = _validate_trace_copy(request["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS_171,
        "authority_request_package_id": REQUEST_PACKAGE_ID_171,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_171,
        "selected_frontier": SELECTED_FRONTIER_171,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": upstream["upstream_decision_execution_package_hash"],
        "upstream_comparison_record_hash": upstream["upstream_comparison_record_hash"],
        "beo_id": upstream["beo_id"], "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "request_future_exact_metadata_bound_drift_coverage_decision_approval": True,
        "approval_capture_performed": False,
        "drift_decision_made": False,
        "coverage_truth_established": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_171,
        "authority_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"], "expires_at": request["expires_at"],
        "expired": False, "replayed": False, "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_171),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_171),
    }
    for flag in SIDE_EFFECT_FLAGS_171:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(package)
    return package


def _validate_blk167_reconciliation_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-167 reconciliation package must be a dictionary")
    if package.get("reconciliation_status") != RECONCILIATION_STATUS_167:
        raise ValueError("BLK-167 reconciliation_status must be exact")
    if package.get("reconciliation_package_id") != RECONCILIATION_PACKAGE_ID_167:
        raise ValueError("BLK-167 reconciliation_package_id must be exact")
    if package.get("upstream_decision_execution_package_hash") != CANONICAL_BLK166_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-167 reconciliation package must bind BLK-166 package hash")
    if package.get("upstream_execution_record_hash") != CANONICAL_BLK166_EXECUTION_RECORD_HASH:
        raise ValueError("canonical BLK-167 reconciliation package must bind BLK-166 execution record hash")
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-167 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK167_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-167 reconciliation package hash mismatch")
    if package.get("clean_record_only_evidence_reconciled") is not True:
        raise ValueError("BLK-167 reconciliation must be clean")
    if package.get("observed_failure_requires_168") is not False:
        raise ValueError("BLK-167 observed failure flag must be false")
    return package


def _validate_168_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-168 package must be a dictionary")
    if package.get("request_status") != REQUEST_STATUS_168:
        raise ValueError("request_status must be exact BLK-168 status")
    if package.get("authority_request_package_id") != REQUEST_PACKAGE_ID_168:
        raise ValueError("authority_request_package_id must be exact BLK-168 id")
    _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"})
    if package["authority_request_package_hash"] != computed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-168 package")
    if package["authority_request_package_hash"] != CANONICAL_BLK168_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-168 authority request package hash mismatch")
    if set(package.get("proof_obligations", [])) != EXACT_PROOF_OBLIGATIONS_168:
        raise ValueError("BLK-168 proof obligations must be exact")
    if set(package.get("excluded_authorities", [])) != EXACT_EXCLUDED_AUTHORITIES_168:
        raise ValueError("BLK-168 excluded authorities must be exact")
    _require(package, "request_scope", REQUEST_SCOPE_168)
    _require(package, "selected_frontier", SELECTED_FRONTIER_168)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_168)
    _require_true(package, "request_future_exact_metadata_hash_only_active_vault_comparison")
    for flag in SIDE_EFFECT_FLAGS_168:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-168 package {flag} must remain false")
    return package


def _validate_169_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-169 package must be a dictionary")
    if package.get("decision_execution_package_id") != DECISION_EXECUTION_PACKAGE_ID_169:
        raise ValueError("decision_execution_package_id must be exact BLK-169 id")
    _required_hash(package.get("decision_execution_package_hash"), "decision_execution_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"})
    if package["decision_execution_package_hash"] != computed:
        raise ValueError("decision_execution_package_hash does not match submitted BLK-169 package")
    if package["decision_execution_package_hash"] != CANONICAL_BLK169_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-169 decision execution package hash mismatch")
    _require(package, "decision_execution_scope", DECISION_EXECUTION_SCOPE_169)
    _require(package, "selected_frontier", SELECTED_FRONTIER_169)
    _require(package, "approval_id", APPROVAL_ID_169)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_169)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_169)
    if package.get("metadata_hashes_match") is not True:
        raise ValueError("canonical BLK-169 comparison must be clean for BLK-170")
    _validate_comparison_record(package.get("comparison_record"), package)
    if package.get("comparison_record_hash") != CANONICAL_BLK169_COMPARISON_RECORD_HASH:
        raise ValueError("canonical BLK-169 comparison record hash mismatch")
    for flag in SIDE_EFFECT_FLAGS_169:
        expected = flag in {"active_vault_hash_comparison_performed", "operator_decision_captured", "one_run_id_consumed_in_record_only_evidence"}
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-169 package {flag} must be {expected}")
    return package


def _validate_170_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-170 package must be a dictionary")
    if package.get("reconciliation_package_id") != RECONCILIATION_PACKAGE_ID_170:
        raise ValueError("reconciliation_package_id must be exact BLK-170 id")
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-170 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK170_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-170 reconciliation package hash mismatch")
    if package.get("clean_metadata_hash_comparison_reconciled") is not True:
        raise ValueError("BLK-170 must be clean before BLK-171 request")
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_170)
    _require(package, "selected_frontier", SELECTED_FRONTIER_170)
    _require(package, "recommended_next_frontier", NEXT_FRONTIER_170_CLEAN)
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-170 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_170:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-170 package {flag} must remain false")
    if package.get("upstream_decision_execution_package_hash") != CANONICAL_BLK169_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-170 must bind canonical BLK-169 package hash")
    if package.get("upstream_comparison_record_hash") != CANONICAL_BLK169_COMPARISON_RECORD_HASH:
        raise ValueError("BLK-170 must bind canonical BLK-169 comparison record hash")
    return package


def _validate_request_like(record: Any, keys: frozenset[str], attestation_keys: frozenset[str], proof_set: set[str], excluded_set: set[str], false_flags: tuple[str, ...], true_flags: set[str] | None = None) -> dict[str, Any]:
    if true_flags is None:
        true_flags = set()
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
    _scan_value_strings(record.get("operator_identity"), "operator_identity")
    for flag in false_flags:
        expected = flag in true_flags
        if record.get(flag) is not expected:
            if expected:
                raise ValueError(f"{flag} must be true")
            raise ValueError(f"{flag} must remain false")
    return record


def _require(record: dict[str, Any], key: str, expected: Any) -> None:
    if record.get(key) != expected:
        value = record.get(key)
        if isinstance(value, str):
            lowered = value.lower()
            if "docs%" in lowered or "requirements" in lowered or "the system shall" in lowered or "system%20shall" in lowered:
                _scan_value_strings(value, key)
        raise ValueError(f"{key} must be {expected!r}")


def _require_true(record: dict[str, Any], key: str) -> None:
    if record.get(key) is not True:
        raise ValueError(f"{key} must be true")


def _require_false(record: dict[str, Any], key: str) -> None:
    if record.get(key) is not False:
        raise ValueError(f"{key} must be false")


def _require_matching_upstream(record: dict[str, Any], upstream: dict[str, Any], pairs: tuple[tuple[str, str], ...]) -> None:
    for local_key, upstream_key in pairs:
        if record.get(local_key) != upstream.get(upstream_key):
            raise ValueError(f"{local_key} must match upstream {upstream_key}")


def _validate_trace_copy(trace_ids: Any, expected: Any) -> list[str]:
    _validate_exact_trace_identities(trace_ids)
    if list(trace_ids) != list(expected):
        raise ValueError("exact_trace_identities id must be exact")
    return list(trace_ids)


def _validate_time_window(requested_at: str, expires_at: str, label: str) -> None:
    requested = _parse_not_stale(requested_at, label)
    expires = _parse_timestamp(expires_at, "expires_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")


def _validate_decision_window(decided_at: str, requested_at: str, expires_at: str, upstream_requested_at: str, upstream_expires_at: str) -> None:
    decided = _parse_not_stale(decided_at, "decision execution request")
    requested = _parse_timestamp(requested_at, "requested_at")
    expires = _parse_timestamp(expires_at, "expires_at")
    upstream_requested = _parse_timestamp(upstream_requested_at, "upstream requested_at")
    upstream_expires = _parse_timestamp(upstream_expires_at, "upstream expires_at")
    if decided < upstream_requested:
        raise ValueError("decision must not predate BLK-168 request")
    if requested < decided:
        raise ValueError("requested_at must not predate decided_at")
    if expires <= requested:
        raise ValueError("expires_at must be after requested_at")
    if expires > upstream_expires:
        raise ValueError("decision/execution window must end within BLK-168 request expiry")


def _parse_not_stale(raw: str, label: str) -> datetime:
    parsed = _parse_timestamp(raw, label)
    if parsed <= datetime.fromisoformat("2026-05-16T00:00:00+10:00"):
        raise ValueError(f"{label} must not be calendar-stale")
    return parsed


def _parse_trace_identity(identity: str) -> tuple[str, str, str]:
    pieces = identity.split(":")
    if len(pieces) != 4 or pieces[2] != "sha256":
        raise ValueError("exact_trace_identities id must be exact")
    return pieces[0], pieces[1], "sha256:" + pieces[3]


def _metadata_records_from_trace_ids(trace_ids: list[str]) -> list[dict[str, Any]]:
    records = []
    for identity in trace_ids:
        kind, artifact_id, version_hash = _parse_trace_identity(identity)
        records.append({
            "kind": kind,
            "id": artifact_id,
            "version_hash": version_hash,
            "metadata_source": "CALLER_SUPPLIED_ACTIVE_VAULT_HASH_METADATA_ONLY",
            "body_included": False,
            "body_read": False,
            "body_copied": False,
            "body_hashed": False,
            "body_parsed": False,
            "body_scanned": False,
            "protected_path_accessed": False,
        })
    return records


def _validate_active_metadata_records(records: Any, trace_ids: list[str]) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError("active_metadata_records must be a list")
    expected = {(_parse_trace_identity(identity)[0], _parse_trace_identity(identity)[1]): _parse_trace_identity(identity)[2] for identity in trace_ids}
    if len(records) != len(expected):
        raise ValueError("active_metadata_records must match exact identity set")
    observed = {}
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("active_metadata_records entries must be dictionaries")
        extra = sorted(set(item) - _METADATA_RECORD_KEYS)
        if extra:
            raise ValueError(f"unexpected field {extra[0]!r}")
        missing = sorted(_METADATA_RECORD_KEYS - set(item))
        if missing:
            raise ValueError(f"missing metadata field {missing[0]!r}")
        _scan_value_strings(item, "active_metadata_record")
        for flag in _METADATA_FALSE_FLAGS:
            if item.get(flag) is not False:
                raise ValueError(f"metadata {flag} must remain false")
        if item.get("metadata_source") != "CALLER_SUPPLIED_ACTIVE_VAULT_HASH_METADATA_ONLY":
            raise ValueError("metadata_source must be caller-supplied metadata only")
        _required_hash(item.get("version_hash"), "version_hash")
        key = (item.get("kind"), item.get("id"))
        if key in observed:
            raise ValueError("duplicate active_metadata_records identity")
        observed[key] = deepcopy(item)
    if set(observed) != set(expected):
        raise ValueError("active_metadata_records must match exact identity set")
    return [observed[key] for key in sorted(observed)]


def _validate_comparison_record(record: Any, package: dict[str, Any]) -> None:
    required = {
        "comparison_record_id", "run_id_consumed", "approval_id", "beo_id", "beb_id",
        "exact_trace_identities", "active_metadata_records", "metadata_hashes_match", "mismatches",
        "recorded_at", "active_vault_filesystem_read_performed", "protected_body_reads", "rtm_generated",
        "rtm_drift_rejection_performed", "drift_decision_made", "coverage_truth_established",
        "target_repo_scan_or_mutation", "comparison_record_hash",
    }
    if not isinstance(record, dict):
        raise ValueError("comparison_record must be a dictionary")
    extra = sorted(set(record) - required)
    if extra:
        raise ValueError(f"unexpected comparison_record field {extra[0]!r}")
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(f"missing comparison_record field {missing[0]!r}")
    if record["comparison_record_hash"] != _canonical_hash({k: v for k, v in record.items() if k != "comparison_record_hash"}):
        raise ValueError("comparison_record_hash does not match submitted BLK-169 comparison record")
    if record["comparison_record_hash"] != package.get("comparison_record_hash"):
        raise ValueError("nested comparison_record_hash must match top-level comparison_record_hash")
    _require(record, "comparison_record_id", COMPARISON_RECORD_ID_169)
    _require(record, "run_id_consumed", RUN_ID_CONSUMED_169)
    _require(record, "approval_id", APPROVAL_ID_169)
    _require(record, "beo_id", package["beo_id"])
    _require(record, "beb_id", package["beb_id"])
    _validate_trace_copy(record["exact_trace_identities"], package["exact_trace_identities"])
    _validate_active_metadata_records(record["active_metadata_records"], package["exact_trace_identities"])
    if record["metadata_hashes_match"] is not package.get("metadata_hashes_match"):
        raise ValueError("comparison_record metadata_hashes_match must match package")
    if record["metadata_hashes_match"] is not True or record["mismatches"] != []:
        raise ValueError("canonical BLK-169 comparison record must be clean")
    for flag in (
        "active_vault_filesystem_read_performed", "protected_body_reads", "rtm_generated",
        "rtm_drift_rejection_performed", "drift_decision_made", "coverage_truth_established",
        "target_repo_scan_or_mutation",
    ):
        if record.get(flag) is not False:
            raise ValueError(f"comparison_record {flag} must remain false")


def _build_comparison_record(execution: dict[str, Any], trace_ids: list[str], observed: list[dict[str, Any]]) -> dict[str, Any]:
    expected = {(_parse_trace_identity(identity)[0], _parse_trace_identity(identity)[1]): _parse_trace_identity(identity)[2] for identity in trace_ids}
    mismatches = []
    for item in observed:
        key = (item["kind"], item["id"])
        if item["version_hash"] != expected[key]:
            mismatches.append({"kind": item["kind"], "id": item["id"], "expected_version_hash": expected[key], "observed_version_hash": item["version_hash"]})
    record = {
        "comparison_record_id": COMPARISON_RECORD_ID_169,
        "run_id_consumed": RUN_ID_CONSUMED_169,
        "approval_id": APPROVAL_ID_169,
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(trace_ids),
        "active_metadata_records": deepcopy(observed),
        "metadata_hashes_match": not mismatches,
        "mismatches": mismatches,
        "recorded_at": execution["requested_at"],
        "active_vault_filesystem_read_performed": False,
        "protected_body_reads": False,
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
        "drift_decision_made": False,
        "coverage_truth_established": False,
        "target_repo_scan_or_mutation": False,
    }
    record["comparison_record_hash"] = _canonical_hash(record)
    return record
