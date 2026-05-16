"""BLK-SYSTEM-178..182 RTM / blk-link protected-body evidence follow-up ladder.

This deterministic fixture consumes the exact BLK-SYSTEM-176 protected-body
verification integration package, emits a request-only follow-up package (178),
records one metadata-only follow-up execution package (179), reconciles it (180),
exports a downstream metadata manifest (181), and reconciles that export (182).

It does not generate RTM, reject drift, establish coverage truth, run reusable or
live production blk-link, read/copy/parse/hash/scan protected bodies, mutate
source/Git/targets, run BLK-pipe/BLK-test/Codex/tooling, reuse signer/storage/
ledger authority, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_ladder_168_171 import (
    _parse_not_stale,
    _require,
    _require_false,
    _require_matching_upstream,
    _require_true,
    _validate_decision_window,
    _validate_time_window,
    _validate_trace_copy,
)
from metadata_bound_rtm_trace_closure_approval_capture import _required_exact_set, _required_hash
from protected_body_verification_decision_engine_175 import _scan_high_risk_freeform
from rtm_blk_link_protected_body_verification_integration_176 import (
    CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_176,
    EXACT_PROOF_OBLIGATIONS_176,
    RECONCILIATION_PACKAGE_ID_176,
    RECONCILIATION_SCOPE_176,
    RECONCILIATION_STATUS_176,
    SELECTED_FRONTIER_176,
    SIDE_EFFECT_FLAGS_176,
)

REQUEST_STATUS_178 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_AUTHORITY_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID_178 = "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-AUTHORITY-REQUEST-178-001"
REQUEST_SCOPE_178 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_REQUEST_ONLY_NOT_APPROVAL"
SELECTED_FRONTIER_178 = "rtm_blk_link_protected_body_evidence_followup_request_178"
NEXT_REQUIRED_AUTHORITY_178 = "EXACT_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_APPROVAL_REQUIRED_NOT_GRANTED"
CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH = "sha256:9750bb9539e5339f46c710690b2cc0dc381cd072a81c74c6fdb5d14fc657564a"

FOLLOWUP_EXECUTION_STATUS_179 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_RECORDED_FOR_EXACT_BLK178_REQUEST"
FOLLOWUP_EXECUTION_PACKAGE_ID_179 = "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-EXECUTION-179-001"
FOLLOWUP_EXECUTION_SCOPE_179 = "EXACT_METADATA_ONLY_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_RECORD_NOT_RUNTIME"
SELECTED_FRONTIER_179 = "rtm_blk_link_protected_body_evidence_followup_execution_179"
APPROVAL_ID_179 = "APPROVAL-BLK-SYSTEM-178-RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-001"
RUN_ID_CONSUMED_179 = "RUN-BLK-SYSTEM-179-RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-001"
EXACT_OPERATOR_DECISION_TEXT_179 = (
    "APPROVE RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-AUTHORITY-REQUEST-178-001 "
    "FOR ONE METADATA-ONLY FOLLOW-UP EVIDENCE RUN "
    "RUN-BLK-SYSTEM-179-RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-001; "
    "NO PROTECTED BODY READS; NO RTM GENERATION; NO RTM DRIFT REJECTION; "
    "NO COVERAGE TRUTH; NO MUTATION."
)
FOLLOWUP_STATUS_179 = "PROTECTED_BODY_VERIFICATION_EVIDENCE_LINEAGE_READY_FOR_DOWNSTREAM_METADATA_EXPORT_NOT_RTM_GENERATION"
NEXT_REQUIRED_AUTHORITY_179 = "POST_FOLLOWUP_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH = "sha256:b9de9be0944dc59e5da6e3baa096e5f88e351cd5e80291aa19feb2194c162ceb"

RECONCILIATION_STATUS_180 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_POST_EXECUTION_RECONCILED_CLEAN"
RECONCILIATION_PACKAGE_ID_180 = "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-FOLLOWUP-RECONCILIATION-180-001"
RECONCILIATION_SCOPE_180 = "POST_FOLLOWUP_EXECUTION_RECONCILIATION_ONLY_NO_NEW_AUTHORITY"
SELECTED_FRONTIER_180 = "rtm_blk_link_protected_body_evidence_followup_reconciliation_180"
NEXT_FRONTIER_180_CLEAN = "NEXT_FRONTIER_DOWNSTREAM_METADATA_EXPORT_REQUEST_NOT_GRANTED"
CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH = "sha256:23cfafe1d310a6cb5caa600dc1149c90fae257faf36193f110f519be345cdc20"

EXPORT_STATUS_181 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_DOWNSTREAM_METADATA_EXPORT_EMITTED"
EXPORT_PACKAGE_ID_181 = "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-DOWNSTREAM-METADATA-EXPORT-181-001"
EXPORT_SCOPE_181 = "DOWNSTREAM_METADATA_EXPORT_ONLY_NO_BODY_TEXT_OR_RUNTIME_AUTHORITY"
SELECTED_FRONTIER_181 = "rtm_blk_link_protected_body_evidence_metadata_export_181"
NEXT_REQUIRED_AUTHORITY_181 = "POST_EXPORT_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK181_EXPORT_PACKAGE_HASH = "sha256:d8595a2596dd79005fa1f54867085a95cd55b7e1526eab4922c58d4fa1c2a920"

RECONCILIATION_STATUS_182 = "RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_EXPORT_RECONCILED_CLEAN"
RECONCILIATION_PACKAGE_ID_182 = "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-EXPORT-RECONCILIATION-182-001"
RECONCILIATION_SCOPE_182 = "POST_EXPORT_RECONCILIATION_ONLY_NEXT_OPERATOR_DECISION_NOT_GRANTED"
SELECTED_FRONTIER_182 = "rtm_blk_link_protected_body_evidence_export_reconciliation_182"
NEXT_FRONTIER_182_CLEAN = "NEXT_FRONTIER_OPERATOR_SELECTED_RTM_BLK_LINK_DECISION_AFTER_METADATA_EXPORT_NOT_GRANTED"
CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH = "sha256:c37ca2c30c819f4c5ec342e5ed60933a0bc43d6cf87d47130bf5e5d74a1a431a"

_BASE_EXCLUDED = {
    "PROTECTED_BODY_TEXT_RETURN_OR_BODY_CONTENT_EXPOSURE",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "AUTHORITATIVE_DRIFT_DECISION_OR_REJECTION",
    "RTM_DRIFT_REJECTION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY",
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

EXACT_EXCLUDED_AUTHORITIES_178 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "FOLLOWUP_EXECUTION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_REQUEST_ONLY_PACKAGE",
}
EXACT_EXCLUDED_AUTHORITIES_179 = _BASE_EXCLUDED | {
    "RUN_ID_REUSE_AFTER_RECORD_ONLY_CONSUMPTION",
    "DOWNSTREAM_METADATA_EXPORT_THIS_SPRINT",
    "REUSABLE_FOLLOWUP_EXECUTION_AUTHORITY",
}
EXACT_EXCLUDED_AUTHORITIES_180 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "DOWNSTREAM_METADATA_EXPORT_THIS_SPRINT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
}
EXACT_EXCLUDED_AUTHORITIES_181 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "BODY_TEXT_OR_PROTECTED_PATH_IN_EXPORT_MANIFEST",
    "EXPORT_IS_NOT_RTM_GENERATION_OR_COVERAGE_TRUTH",
}
EXACT_EXCLUDED_AUTHORITIES_182 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "EXPORT_RECONCILIATION_IS_NOT_REUSABLE_AUTHORITY",
}

EXACT_PROOF_OBLIGATIONS_178 = {
    "BLK176_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK175_VERIFICATION_RECORD_HASH_BOUND_THROUGH_BLK176",
    "REQUEST_LIMITED_TO_FUTURE_EXACT_FOLLOWUP_EXECUTION_APPROVAL",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE_OR_RUNTIME_EXECUTION",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_NOT_PERFORMED_BY_REQUEST",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_NOT_PERFORMED_BY_REQUEST",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_179 = {
    "BLK178_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK176_RECONCILIATION_HASH_BOUND_THROUGH_BLK178",
    "OPERATOR_DECISION_CAPTURED_FOR_EXACT_BLK178_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_REQUEST",
    "RUN_ID_CONSUMED_ONCE_IN_RECORD_ONLY_EVIDENCE",
    "FOLLOWUP_RECORD_LIMITED_TO_METADATA_EVIDENCE",
    "PROTECTED_BODY_VERIFICATION_LINEAGE_BOUND_WITHOUT_BODY_TEXT",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_180 = {
    "BLK179_FOLLOWUP_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "CLEAN_FOLLOWUP_EXECUTION_RECONCILED_WITHOUT_AUTHORITY_PROMOTION",
    "NEXT_METADATA_EXPORT_FRONTIER_NAMED_WITH_AUTHORITY_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_HARDENING",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_181 = {
    "BLK180_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "EXPORT_MANIFEST_CONTAINS_ONLY_TRACE_IDS_AND_HASH_METADATA",
    "EXPORT_MANIFEST_HASH_BOUND_TO_PACKAGE",
    "PROTECTED_BODY_TEXT_AND_PATHS_NOT_INCLUDED",
    "EXPORT_DOES_NOT_GENERATE_RTM_REJECT_DRIFT_OR_ESTABLISH_COVERAGE_TRUTH",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_182 = {
    "BLK181_EXPORT_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "EXPORT_RECONCILED_WITHOUT_AUTHORITY_PROMOTION",
    "NEXT_OPERATOR_DECISION_NAMED_WITH_AUTHORITY_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_HARDENING",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
}

_COMMON_FALSE_FLAGS = (
    "approval_capture_performed_outside_exact_request",
    "protected_body_text_included",
    "protected_body_content_returned",
    "protected_body_filesystem_read_performed",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted_by_fixture",
    "protected_body_scan_attempted",
    "protected_body_path_disclosed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "active_vault_hash_comparison_performed",
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
SIDE_EFFECT_FLAGS_178 = _COMMON_FALSE_FLAGS + ("approval_capture_performed", "future_run_id_reserved_or_consumed")
SIDE_EFFECT_FLAGS_179 = ("operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_180 = ("next_frontier_granted", "observed_failure_requires_hardening", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_181 = ("downstream_metadata_export_emitted", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_182 = ("next_frontier_granted", "observed_failure_requires_hardening", *_COMMON_FALSE_FLAGS)

_ATTESTATION_178 = frozenset({
    "exact_blk176_reconciliation_reviewed", "request_is_for_future_approval_not_approval",
    "followup_execution_not_performed", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})
_ATTESTATION_179 = frozenset({
    "exact_blk178_request_reviewed", "operator_decision_captured_from_latest_directive",
    "run_id_consumed_once_in_record_only_evidence", "metadata_only_followup_scope_preserved",
    "protected_body_lineage_bound_without_body_text", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})
_ATTESTATION_180 = frozenset({
    "exact_blk179_execution_reviewed", "reconciliation_only_not_authority_request",
    "clean_followup_execution_reconciled", "no_observed_failure_requiring_hardening",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "reusable_blk_link_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_181 = frozenset({
    "exact_blk180_reconciliation_reviewed", "metadata_export_only_scope_preserved",
    "trace_ids_and_hashes_only", "protected_body_text_not_included_or_returned",
    "protected_body_paths_not_included", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "reusable_blk_link_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_182 = frozenset({
    "exact_blk181_export_reviewed", "clean_export_reconciled", "next_operator_decision_not_granted",
    "no_observed_failure_requiring_hardening", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})

_REQUEST_KEYS_178 = frozenset({
    "authority_request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_decision_execution_package_hash", "upstream_verification_record_hash", "beo_id", "beb_id",
    "exact_trace_identities", "request_future_exact_followup_execution_approval", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_178,
})
_REQUEST_KEYS_179 = frozenset({
    "followup_execution_package_id", "operator_identity", "followup_execution_scope", "selected_frontier",
    "upstream_authority_request_package_id", "upstream_authority_request_package_hash",
    "upstream_reconciliation_package_hash", "upstream_verification_record_hash", "approval_id", "run_id_to_consume",
    "beo_id", "beb_id", "exact_trace_identities", "protected_body_verification_lineage_hash",
    "operator_decision_text_raw", "decided_at", "requested_at", "expires_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_179,
})
_CONTEXT_KEYS_180 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_followup_execution_package_id", "upstream_followup_execution_package_hash", "run_id_consumed",
    "beo_id", "beb_id", "exact_trace_identities", "protected_body_verification_lineage_hash",
    "followup_status_observed", "rtm_blk_link_followup_recorded_observed", "observed_failure_requires_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_180,
})
_REQUEST_KEYS_181 = frozenset({
    "export_package_id", "operator_identity", "export_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_followup_execution_package_hash", "run_id_consumed", "beo_id", "beb_id",
    "exact_trace_identities", "protected_body_verification_lineage_hash", "export_notes", "exported_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_181,
})
_CONTEXT_KEYS_182 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_export_package_id", "upstream_export_package_hash", "upstream_export_manifest_hash",
    "beo_id", "beb_id", "exact_trace_identities", "protected_body_verification_lineage_hash",
    "downstream_metadata_export_emitted_observed", "observed_failure_requires_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_182,
})
_PACKAGE_KEYS_176 = frozenset({
    "reconciliation_status", "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_decision_execution_package_id", "upstream_decision_execution_package_hash",
    "upstream_verification_record_id", "upstream_verification_record_hash", "upstream_authority_request_package_hash",
    "run_id_consumed", "beo_id", "beb_id", "exact_trace_identities",
    "rtm_blk_link_protected_body_verification_evidence_bound", "clean_protected_body_verification_reconciled",
    "protected_body_hashes_verified", "mismatches", "observed_failure_requires_177_hardening", "recommended_next_frontier",
    "next_frontier_granted", "integration_context_hash", "reconciled_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", "reconciliation_package_hash", *SIDE_EFFECT_FLAGS_176,
})


def valid_rtm_blk_link_followup_authority_request_178(reconciliation176: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "authority_request_package_id": REQUEST_PACKAGE_ID_178,
        "operator_identity": reconciliation176["operator_identity"],
        "request_scope": REQUEST_SCOPE_178,
        "selected_frontier": SELECTED_FRONTIER_178,
        "upstream_reconciliation_package_id": reconciliation176["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation176["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": reconciliation176["upstream_decision_execution_package_hash"],
        "upstream_verification_record_hash": reconciliation176["upstream_verification_record_hash"],
        "beo_id": reconciliation176["beo_id"],
        "beb_id": reconciliation176["beb_id"],
        "exact_trace_identities": list(reconciliation176["exact_trace_identities"]),
        "request_future_exact_followup_execution_approval": True,
        "requested_at": "2099-05-16T22:00:00+10:00",
        "expires_at": "2099-05-17T22:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_178},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_178),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_178),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_178, set())
    record.update(overrides)
    return record


def build_rtm_blk_link_followup_authority_request_178(reconciliation176_package: dict[str, Any], request178: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_176_package(reconciliation176_package)
    request = _validate_request_like(request178, _REQUEST_KEYS_178, _ATTESTATION_178, EXACT_PROOF_OBLIGATIONS_178, EXACT_EXCLUDED_AUTHORITIES_178, SIDE_EFFECT_FLAGS_178)
    _scan_high_risk_freeform(request["operator_identity"], "operator_identity")
    _require(request, "authority_request_package_id", REQUEST_PACKAGE_ID_178)
    _require(request, "request_scope", REQUEST_SCOPE_178)
    _require(request, "selected_frontier", SELECTED_FRONTIER_178)
    _require_true(request, "request_future_exact_followup_execution_approval")
    _require_matching_upstream(request, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_decision_execution_package_hash", "upstream_decision_execution_package_hash"),
        ("upstream_verification_record_hash", "upstream_verification_record_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(request["requested_at"], request["expires_at"], "authority request")
    trace_ids = _validate_trace_copy(request["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS_178,
        "authority_request_package_id": REQUEST_PACKAGE_ID_178,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_178,
        "selected_frontier": SELECTED_FRONTIER_178,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": upstream["upstream_decision_execution_package_hash"],
        "upstream_verification_record_hash": upstream["upstream_verification_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "request_future_exact_followup_execution_approval": True,
        "approval_capture_performed": False,
        "future_run_id_reserved_or_consumed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_178,
        "authority_request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_178),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_178),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_178, set())
    package["authority_request_package_hash"] = _canonical_hash(package)
    return package


def valid_rtm_blk_link_followup_execution_record_179(request178: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "followup_execution_package_id": FOLLOWUP_EXECUTION_PACKAGE_ID_179,
        "operator_identity": request178["operator_identity"],
        "followup_execution_scope": FOLLOWUP_EXECUTION_SCOPE_179,
        "selected_frontier": SELECTED_FRONTIER_179,
        "upstream_authority_request_package_id": request178["authority_request_package_id"],
        "upstream_authority_request_package_hash": request178["authority_request_package_hash"],
        "upstream_reconciliation_package_hash": request178["upstream_reconciliation_package_hash"],
        "upstream_verification_record_hash": request178["upstream_verification_record_hash"],
        "approval_id": APPROVAL_ID_179,
        "run_id_to_consume": RUN_ID_CONSUMED_179,
        "beo_id": request178["beo_id"],
        "beb_id": request178["beb_id"],
        "exact_trace_identities": list(request178["exact_trace_identities"]),
        "protected_body_verification_lineage_hash": request178["upstream_reconciliation_package_hash"],
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_179,
        "decided_at": "2099-05-16T22:10:00+10:00",
        "requested_at": "2099-05-16T22:16:00+10:00",
        "expires_at": "2099-05-16T22:25:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_179},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_179),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_179),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_179, {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"})
    record.update(overrides)
    return record


def build_rtm_blk_link_followup_execution_record_179(request178_package: dict[str, Any], execution179: dict[str, Any]) -> dict[str, Any]:
    request178 = _validate_178_package(request178_package)
    execution = _validate_request_like(
        execution179, _REQUEST_KEYS_179, _ATTESTATION_179, EXACT_PROOF_OBLIGATIONS_179,
        EXACT_EXCLUDED_AUTHORITIES_179, SIDE_EFFECT_FLAGS_179,
        true_flags={"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"},
    )
    _scan_high_risk_freeform(execution["operator_identity"], "operator_identity")
    _require(execution, "followup_execution_package_id", FOLLOWUP_EXECUTION_PACKAGE_ID_179)
    _require(execution, "followup_execution_scope", FOLLOWUP_EXECUTION_SCOPE_179)
    _require(execution, "selected_frontier", SELECTED_FRONTIER_179)
    _require(execution, "approval_id", APPROVAL_ID_179)
    _require(execution, "run_id_to_consume", RUN_ID_CONSUMED_179)
    _require(execution, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_179)
    _require(execution, "protected_body_verification_lineage_hash", request178["upstream_reconciliation_package_hash"])
    _require_matching_upstream(execution, request178, (
        ("upstream_authority_request_package_id", "authority_request_package_id"),
        ("upstream_authority_request_package_hash", "authority_request_package_hash"),
        ("upstream_reconciliation_package_hash", "upstream_reconciliation_package_hash"),
        ("upstream_verification_record_hash", "upstream_verification_record_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_decision_window(execution["decided_at"], execution["requested_at"], execution["expires_at"], request178["requested_at"], request178["expires_at"])
    trace_ids = _validate_trace_copy(execution["exact_trace_identities"], request178["exact_trace_identities"])
    package = {
        "followup_execution_status": FOLLOWUP_EXECUTION_STATUS_179,
        "followup_execution_package_id": FOLLOWUP_EXECUTION_PACKAGE_ID_179,
        "operator_identity": execution["operator_identity"],
        "followup_execution_scope": FOLLOWUP_EXECUTION_SCOPE_179,
        "selected_frontier": SELECTED_FRONTIER_179,
        "upstream_authority_request_package_id": request178["authority_request_package_id"],
        "upstream_authority_request_package_hash": request178["authority_request_package_hash"],
        "upstream_reconciliation_package_hash": request178["upstream_reconciliation_package_hash"],
        "upstream_verification_record_hash": request178["upstream_verification_record_hash"],
        "approval_id": APPROVAL_ID_179,
        "run_id_consumed": RUN_ID_CONSUMED_179,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_179,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "rtm_blk_link_followup_recorded": True,
        "followup_status": FOLLOWUP_STATUS_179,
        "protected_body_verification_lineage_hash": execution["protected_body_verification_lineage_hash"],
        "beo_id": request178["beo_id"],
        "beb_id": request178["beb_id"],
        "exact_trace_identities": trace_ids,
        "followup_execution_request_hash": _canonical_hash(execution),
        "decided_at": execution["decided_at"],
        "requested_at": execution["requested_at"],
        "expires_at": execution["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_179,
        "operator_attestation": deepcopy(execution["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_179),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_179),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_179, {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"})
    package["followup_execution_package_hash"] = _canonical_hash(package)
    return package


def valid_rtm_blk_link_followup_post_execution_reconciliation_180(execution179: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_180,
        "operator_identity": execution179["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_180,
        "selected_frontier": SELECTED_FRONTIER_180,
        "upstream_followup_execution_package_id": execution179["followup_execution_package_id"],
        "upstream_followup_execution_package_hash": execution179["followup_execution_package_hash"],
        "run_id_consumed": execution179["run_id_consumed"],
        "beo_id": execution179["beo_id"],
        "beb_id": execution179["beb_id"],
        "exact_trace_identities": list(execution179["exact_trace_identities"]),
        "protected_body_verification_lineage_hash": execution179["protected_body_verification_lineage_hash"],
        "followup_status_observed": execution179["followup_status"],
        "rtm_blk_link_followup_recorded_observed": execution179["rtm_blk_link_followup_recorded"],
        "observed_failure_requires_hardening": False,
        "reconciled_at": "2099-05-16T22:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_180},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_180),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_180),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_180, set())
    record.update(overrides)
    return record


def build_rtm_blk_link_followup_post_execution_reconciliation_180(execution179_package: dict[str, Any], context180: dict[str, Any]) -> dict[str, Any]:
    execution = _validate_179_package(execution179_package)
    context = _validate_request_like(context180, _CONTEXT_KEYS_180, _ATTESTATION_180, EXACT_PROOF_OBLIGATIONS_180, EXACT_EXCLUDED_AUTHORITIES_180, SIDE_EFFECT_FLAGS_180)
    _scan_high_risk_freeform(context["operator_identity"], "operator_identity")
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_180)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_180)
    _require(context, "selected_frontier", SELECTED_FRONTIER_180)
    _require_false(context, "observed_failure_requires_hardening")
    _require_matching_upstream(context, execution, (
        ("upstream_followup_execution_package_id", "followup_execution_package_id"),
        ("upstream_followup_execution_package_hash", "followup_execution_package_hash"),
        ("operator_identity", "operator_identity"), ("run_id_consumed", "run_id_consumed"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
        ("protected_body_verification_lineage_hash", "protected_body_verification_lineage_hash"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], execution["exact_trace_identities"])
    _require(context, "followup_status_observed", execution["followup_status"])
    _require_true(context, "rtm_blk_link_followup_recorded_observed")
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_180,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_180,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_180,
        "selected_frontier": SELECTED_FRONTIER_180,
        "upstream_followup_execution_package_id": execution["followup_execution_package_id"],
        "upstream_followup_execution_package_hash": execution["followup_execution_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": trace_ids,
        "protected_body_verification_lineage_hash": execution["protected_body_verification_lineage_hash"],
        "followup_status": execution["followup_status"],
        "clean_followup_execution_reconciled": True,
        "observed_failure_requires_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_180_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_180),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_180),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_180, set())
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def valid_rtm_blk_link_followup_evidence_export_181(reconciliation180: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "export_package_id": EXPORT_PACKAGE_ID_181,
        "operator_identity": reconciliation180["operator_identity"],
        "export_scope": EXPORT_SCOPE_181,
        "selected_frontier": SELECTED_FRONTIER_181,
        "upstream_reconciliation_package_id": reconciliation180["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation180["reconciliation_package_hash"],
        "upstream_followup_execution_package_hash": reconciliation180["upstream_followup_execution_package_hash"],
        "run_id_consumed": reconciliation180["run_id_consumed"],
        "beo_id": reconciliation180["beo_id"],
        "beb_id": reconciliation180["beb_id"],
        "exact_trace_identities": list(reconciliation180["exact_trace_identities"]),
        "protected_body_verification_lineage_hash": reconciliation180["protected_body_verification_lineage_hash"],
        "export_notes": "Downstream metadata export includes trace ids and hashes only; no protected-body text or paths.",
        "exported_at": "2099-05-16T22:40:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_181},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_181),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_181),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_181, set())
    record.update(overrides)
    return record


def build_rtm_blk_link_followup_evidence_export_181(reconciliation180_package: dict[str, Any], export181: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_180_package(reconciliation180_package)
    export = _validate_request_like(export181, _REQUEST_KEYS_181, _ATTESTATION_181, EXACT_PROOF_OBLIGATIONS_181, EXACT_EXCLUDED_AUTHORITIES_181, SIDE_EFFECT_FLAGS_181)
    _scan_high_risk_freeform(export["operator_identity"], "operator_identity")
    _scan_high_risk_freeform(export["export_notes"], "export_notes")
    _require(export, "export_package_id", EXPORT_PACKAGE_ID_181)
    _require(export, "export_scope", EXPORT_SCOPE_181)
    _require(export, "selected_frontier", SELECTED_FRONTIER_181)
    _require_matching_upstream(export, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_followup_execution_package_hash", "upstream_followup_execution_package_hash"),
        ("operator_identity", "operator_identity"), ("run_id_consumed", "run_id_consumed"),
        ("beo_id", "beo_id"), ("beb_id", "beb_id"),
        ("protected_body_verification_lineage_hash", "protected_body_verification_lineage_hash"),
    ))
    _parse_not_stale(export["exported_at"], "export context")
    trace_ids = _validate_trace_copy(export["exact_trace_identities"], upstream["exact_trace_identities"])
    manifest = _build_export_manifest(export, trace_ids)
    package = {
        "export_status": EXPORT_STATUS_181,
        "export_package_id": EXPORT_PACKAGE_ID_181,
        "operator_identity": export["operator_identity"],
        "export_scope": EXPORT_SCOPE_181,
        "selected_frontier": SELECTED_FRONTIER_181,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_followup_execution_package_hash": upstream["upstream_followup_execution_package_hash"],
        "run_id_consumed": upstream["run_id_consumed"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "protected_body_verification_lineage_hash": upstream["protected_body_verification_lineage_hash"],
        "downstream_metadata_export_emitted": True,
        "export_manifest": manifest,
        "export_manifest_hash": _canonical_hash(manifest),
        "export_request_hash": _canonical_hash(export),
        "exported_at": export["exported_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_181,
        "operator_attestation": deepcopy(export["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_181),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_181),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_181, set())
    package["downstream_metadata_export_emitted"] = True
    package["export_package_hash"] = _canonical_hash(package)
    return package


def valid_rtm_blk_link_followup_post_export_reconciliation_182(export181: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_182,
        "operator_identity": export181["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_182,
        "selected_frontier": SELECTED_FRONTIER_182,
        "upstream_export_package_id": export181["export_package_id"],
        "upstream_export_package_hash": export181["export_package_hash"],
        "upstream_export_manifest_hash": export181["export_manifest_hash"],
        "beo_id": export181["beo_id"],
        "beb_id": export181["beb_id"],
        "exact_trace_identities": list(export181["exact_trace_identities"]),
        "protected_body_verification_lineage_hash": export181["protected_body_verification_lineage_hash"],
        "downstream_metadata_export_emitted_observed": export181["downstream_metadata_export_emitted"],
        "observed_failure_requires_hardening": False,
        "reconciled_at": "2099-05-16T22:50:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_182},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_182),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_182),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_182, set())
    record.update(overrides)
    return record


def build_rtm_blk_link_followup_post_export_reconciliation_182(export181_package: dict[str, Any], context182: dict[str, Any]) -> dict[str, Any]:
    export = _validate_181_package(export181_package)
    context = _validate_request_like(context182, _CONTEXT_KEYS_182, _ATTESTATION_182, EXACT_PROOF_OBLIGATIONS_182, EXACT_EXCLUDED_AUTHORITIES_182, SIDE_EFFECT_FLAGS_182)
    _scan_high_risk_freeform(context["operator_identity"], "operator_identity")
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_182)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_182)
    _require(context, "selected_frontier", SELECTED_FRONTIER_182)
    _require_false(context, "observed_failure_requires_hardening")
    _require_matching_upstream(context, export, (
        ("upstream_export_package_id", "export_package_id"),
        ("upstream_export_package_hash", "export_package_hash"),
        ("upstream_export_manifest_hash", "export_manifest_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
        ("protected_body_verification_lineage_hash", "protected_body_verification_lineage_hash"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], export["exact_trace_identities"])
    _require_true(context, "downstream_metadata_export_emitted_observed")
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_182,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_182,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_182,
        "selected_frontier": SELECTED_FRONTIER_182,
        "upstream_export_package_id": export["export_package_id"],
        "upstream_export_package_hash": export["export_package_hash"],
        "upstream_export_manifest_hash": export["export_manifest_hash"],
        "beo_id": export["beo_id"],
        "beb_id": export["beb_id"],
        "exact_trace_identities": trace_ids,
        "protected_body_verification_lineage_hash": export["protected_body_verification_lineage_hash"],
        "clean_export_reconciled": True,
        "observed_failure_requires_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_182_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_182),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_182),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_182, set())
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _set_flags(record: dict[str, Any], flags: tuple[str, ...], true_flags: set[str]) -> None:
    for flag in flags:
        record[flag] = flag in true_flags


def _validate_request_like(
    record: Any,
    keys: frozenset[str],
    attestation_keys: frozenset[str],
    proof_set: set[str],
    excluded_set: set[str],
    false_flags: tuple[str, ...],
    true_flags: set[str] | None = None,
) -> dict[str, Any]:
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
    _scan_high_risk_freeform(record.get("operator_identity"), "operator_identity")
    for flag in false_flags:
        expected = flag in true_flags
        if record.get(flag) is not expected:
            if expected:
                raise ValueError(f"{flag} must be true")
            raise ValueError(f"{flag} must remain false")
    return record


def _validate_176_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-176 package must be a dictionary")
    extra = sorted(set(package) - _PACKAGE_KEYS_176)
    if extra:
        raise ValueError(f"unexpected BLK-176 field {extra[0]!r}")
    missing = sorted(_PACKAGE_KEYS_176 - set(package))
    if missing:
        raise ValueError(f"missing BLK-176 field {missing[0]!r}")
    if package.get("reconciliation_status") != RECONCILIATION_STATUS_176:
        raise ValueError("reconciliation_status must be exact BLK-176 status")
    _require(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_176)
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_176)
    _require(package, "selected_frontier", SELECTED_FRONTIER_176)
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-176 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-176 reconciliation package hash mismatch")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_176, "BLK-176 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_176, "BLK-176 excluded_authorities")
    if package.get("rtm_blk_link_protected_body_verification_evidence_bound") is not True:
        raise ValueError("BLK-176 evidence must be bound")
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-176 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_176:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-176 package {flag} must remain false")
    return package


def _validate_178_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-178 package must be a dictionary")
    _require(package, "request_status", REQUEST_STATUS_178)
    _require(package, "authority_request_package_id", REQUEST_PACKAGE_ID_178)
    _require(package, "request_scope", REQUEST_SCOPE_178)
    _require(package, "selected_frontier", SELECTED_FRONTIER_178)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_178)
    _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"})
    if package["authority_request_package_hash"] != computed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-178 package")
    if package["authority_request_package_hash"] != CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-178 authority request package hash mismatch")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_178, "BLK-178 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_178, "BLK-178 excluded_authorities")
    _require_true(package, "request_future_exact_followup_execution_approval")
    if package.get("upstream_reconciliation_package_hash") != CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-178 must bind canonical BLK-176 package hash")
    for flag in SIDE_EFFECT_FLAGS_178:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-178 package {flag} must remain false")
    return package


def _validate_179_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-179 package must be a dictionary")
    _require(package, "followup_execution_status", FOLLOWUP_EXECUTION_STATUS_179)
    _require(package, "followup_execution_package_id", FOLLOWUP_EXECUTION_PACKAGE_ID_179)
    _require(package, "followup_execution_scope", FOLLOWUP_EXECUTION_SCOPE_179)
    _require(package, "selected_frontier", SELECTED_FRONTIER_179)
    _require(package, "approval_id", APPROVAL_ID_179)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_179)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_179)
    _required_hash(package.get("followup_execution_package_hash"), "followup_execution_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "followup_execution_package_hash"})
    if package["followup_execution_package_hash"] != computed:
        raise ValueError("followup_execution_package_hash does not match submitted BLK-179 package")
    if package["followup_execution_package_hash"] != CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-179 followup execution package hash mismatch")
    if package.get("upstream_authority_request_package_hash") != CANONICAL_BLK178_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("BLK-179 must bind canonical BLK-178 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_179, "BLK-179 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_179, "BLK-179 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_179:
        expected = flag in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "rtm_blk_link_followup_recorded"}
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-179 package {flag} must be {expected}")
    return package


def _validate_180_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-180 package must be a dictionary")
    _require(package, "reconciliation_status", RECONCILIATION_STATUS_180)
    _require(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_180)
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_180)
    _require(package, "selected_frontier", SELECTED_FRONTIER_180)
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-180 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-180 reconciliation package hash mismatch")
    if package.get("upstream_followup_execution_package_hash") != CANONICAL_BLK179_FOLLOWUP_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-180 must bind canonical BLK-179 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_180, "BLK-180 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_180, "BLK-180 excluded_authorities")
    if package.get("clean_followup_execution_reconciled") is not True:
        raise ValueError("BLK-180 must reconcile cleanly")
    for flag in SIDE_EFFECT_FLAGS_180:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-180 package {flag} must remain false")
    return package


def _validate_181_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-181 package must be a dictionary")
    _require(package, "export_status", EXPORT_STATUS_181)
    _require(package, "export_package_id", EXPORT_PACKAGE_ID_181)
    _require(package, "export_scope", EXPORT_SCOPE_181)
    _require(package, "selected_frontier", SELECTED_FRONTIER_181)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_181)
    _required_hash(package.get("export_package_hash"), "export_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "export_package_hash"})
    if package["export_package_hash"] != computed:
        raise ValueError("export_package_hash does not match submitted BLK-181 package")
    if package["export_package_hash"] != CANONICAL_BLK181_EXPORT_PACKAGE_HASH:
        raise ValueError("canonical BLK-181 export package hash mismatch")
    if package.get("upstream_reconciliation_package_hash") != CANONICAL_BLK180_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-181 must bind canonical BLK-180 package hash")
    if package.get("export_manifest_hash") != _canonical_hash(package.get("export_manifest")):
        raise ValueError("export manifest hash mismatch")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_181, "BLK-181 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_181, "BLK-181 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_181:
        expected = flag == "downstream_metadata_export_emitted"
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-181 package {flag} must be {expected}")
    return package


def _build_export_manifest(export: dict[str, Any], trace_ids: list[str]) -> dict[str, Any]:
    trace_evidence = []
    for identity in trace_ids:
        kind, artifact_id, version_hash = _parse_trace_identity(identity)
        _scan_high_risk_freeform(kind, "trace kind")
        _scan_high_risk_freeform(artifact_id, "trace id")
        trace_evidence.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return {
        "manifest_id": "RTM-BLK-LINK-PROTECTED-BODY-EVIDENCE-DOWNSTREAM-METADATA-MANIFEST-181-001",
        "beo_id": export["beo_id"],
        "beb_id": export["beb_id"],
        "protected_body_verification_lineage_hash": export["protected_body_verification_lineage_hash"],
        "trace_evidence": trace_evidence,
        "protected_body_text_included": False,
        "protected_body_paths_included": False,
        "rtm_generated": False,
        "drift_rejection_performed": False,
        "coverage_truth_established": False,
    }


def _parse_trace_identity(identity: str) -> tuple[str, str, str]:
    pieces = identity.split(":")
    if len(pieces) != 4 or pieces[2] != "sha256":
        raise ValueError("exact_trace_identities id must be exact")
    return pieces[0], pieces[1], "sha256:" + pieces[3]
