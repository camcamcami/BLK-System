"""BLK-SYSTEM-187..189 single production blk-link wrapper run ladder.

This deterministic fixture consumes the exact BLK-SYSTEM-186 reusable readiness
kernel reconciliation, emits a one-exact-run production `blk-link` wrapper
request (187), records the operator-directed one-run wrapper execution evidence
(188), and reconciles that run cleanly (189).

It executes no shell, network, BLK-pipe, BLK-test, Codex, package-manager,
model, browser, cyber, protected-body file access, or source/Git mutation. The
only granted production surface is the exact wrapper run represented by the
BLK-188 hash-bound evidence package; reusable production `blk-link`, RTM
generation, drift rejection, coverage truth, protected-body access, and adjacent
authorities remain excluded.
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
    _validate_time_window,
    _validate_trace_copy,
)
from metadata_bound_rtm_trace_closure_approval_capture import _required_exact_set, _required_hash
from protected_body_verification_decision_engine_175 import _scan_high_risk_freeform
from reusable_blk_link_readiness_kernel_183_186 import (
    CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
    CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH,
    CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_186,
    EXACT_PROOF_OBLIGATIONS_186,
    RECONCILIATION_PACKAGE_ID_186,
    RECONCILIATION_SCOPE_186,
    RECONCILIATION_STATUS_186,
    SELECTED_FRONTIER_186,
    SIDE_EFFECT_FLAGS_186,
    _validate_contract_shape,
)

REQUEST_STATUS_187 = "SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_REQUEST_READY_NOT_APPROVED"
REQUEST_PACKAGE_ID_187 = "SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-REQUEST-187-001"
REQUEST_SCOPE_187 = "REQUEST_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_RUN_NOT_APPROVAL"
SELECTED_FRONTIER_187 = "single_production_blk_link_wrapper_run_request_187"
NEXT_REQUIRED_AUTHORITY_187 = "EXACT_SINGLE_PRODUCTION_WRAPPER_RUN_APPROVAL_REQUIRED_NOT_GRANTED"
CANONICAL_BLK187_REQUEST_PACKAGE_HASH = "sha256:4190b76da4d54331b95c550ef2a61f9600c2a9b0d7268fe08c418e012cac7872"

EXECUTION_STATUS_188 = "SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_EXECUTION_RECORDED"
EXECUTION_PACKAGE_ID_188 = "SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-EXECUTION-188-001"
EXECUTION_SCOPE_188 = "ONE_EXACT_APPROVED_PRODUCTION_BLK_LINK_WRAPPER_RUN_EVIDENCE"
SELECTED_FRONTIER_188 = "single_production_blk_link_wrapper_run_execution_188"
APPROVAL_ID_188 = "APPROVAL-BLK-SYSTEM-188-SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-001"
RUN_ID_CONSUMED_188 = "RUN-BLK-SYSTEM-188-SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-001"
EXACT_OPERATOR_DECISION_TEXT_188 = (
    "APPROVE SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-REQUEST-187-001 "
    "FOR ONE PRODUCTION BLK-LINK WRAPPER RUN "
    "RUN-BLK-SYSTEM-188-SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-001; "
    "USE REUSABLE READINESS KERNEL CONTRACT C79BDED6E77048852F26239EEE6483FA07B92BF5D8012FE80EF2ABA992537AC9; "
    "NO REUSABLE AUTHORITY; NO RTM GENERATION; NO DRIFT REJECTION; "
    "NO COVERAGE TRUTH; NO PROTECTED BODY READS; NO TARGET/SOURCE/GIT MUTATION."
)
NEXT_REQUIRED_AUTHORITY_188 = "POST_SINGLE_PRODUCTION_WRAPPER_RUN_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK188_EXECUTION_PACKAGE_HASH = "sha256:553f5d81d3b382590626c29db1966c20f12ada7124bfd8d13636fbc0630ed582"

RECONCILIATION_STATUS_189 = "SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECONCILED_CLEAN"
RECONCILIATION_PACKAGE_ID_189 = "SINGLE-PRODUCTION-BLK-LINK-WRAPPER-RUN-RECONCILIATION-189-001"
RECONCILIATION_SCOPE_189 = "POST_SINGLE_PRODUCTION_WRAPPER_RUN_RECONCILIATION_ONLY_NO_REUSABLE_AUTHORITY"
SELECTED_FRONTIER_189 = "single_production_blk_link_wrapper_run_reconciliation_189"
NEXT_FRONTIER_189_CLEAN = "NEXT_FRONTIER_POST_SINGLE_PRODUCTION_WRAPPER_RUN_OPERATOR_REVIEW_NOT_GRANTED"
CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH = "sha256:c822997cd4840a64108acf311db5aabceb21e7d0e9f2050bb1ef2135336a7690"

_BASE_EXCLUDED = {
    "REUSABLE_PRODUCTION_BLK_LINK_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION_BEYOND_THIS_EXACT_RUN",
    "RUN_ID_REUSE_OR_GLOBAL_REPLAY_LEDGER_CLAIM",
    "RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION_OR_REJECTION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "COVERAGE_MATRIX_GENERATION",
    "ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "PROTECTED_BODY_TEXT_RETURN_OR_BODY_CONTENT_EXPOSURE",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "TARGET_REPO_SCAN",
    "TARGET_REPO_MUTATION",
    "SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BEO_PUBLICATION_OR_SIGNING",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}
EXACT_EXCLUDED_AUTHORITIES_187 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "PRODUCTION_WRAPPER_EXECUTION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_REQUEST_ONLY_PACKAGE",
}
EXACT_EXCLUDED_AUTHORITIES_188 = _BASE_EXCLUDED | {
    "REUSABLE_AUTHORITY_FROM_SINGLE_RUN",
    "FUTURE_RUN_ID_RESERVATION_BEYOND_CONSUMED_RUN",
    "POST_RUN_RECONCILIATION_THIS_SPRINT",
}
EXACT_EXCLUDED_AUTHORITIES_189 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "RECONCILIATION_IS_NOT_REUSABLE_PRODUCTION_AUTHORITY",
}

EXACT_PROOF_OBLIGATIONS_187 = {
    "BLK186_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK184_REUSABLE_CONTRACT_HASH_BOUND_THROUGH_BLK186",
    "REQUEST_LIMITED_TO_ONE_EXACT_PRODUCTION_WRAPPER_RUN",
    "REQUEST_IS_NOT_APPROVAL_CAPTURE_OR_EXECUTION",
    "PER_RUN_EXACT_APPROVAL_AND_RUN_ID_REQUIRED",
    "REUSABLE_PRODUCTION_AUTHORITY_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_188 = {
    "BLK187_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK184_CONTRACT_HASH_BOUND_THROUGH_BLK187",
    "EXACT_OPERATOR_APPROVAL_TEXT_BOUND_TO_REQUEST_CONTRACT_AND_RUN_ID",
    "ONE_RUN_ID_CONSUMED_IN_SINGLE_PRODUCTION_WRAPPER_EVIDENCE",
    "SINGLE_PRODUCTION_WRAPPER_RUN_RECORDED_CLEAN",
    "REUSABLE_PRODUCTION_AUTHORITY_EXCLUDED_AFTER_RUN",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_189 = {
    "BLK188_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "CLEAN_SINGLE_PRODUCTION_WRAPPER_RUN_RECONCILED_WITHOUT_AUTHORITY_PROMOTION",
    "NEXT_OPERATOR_REVIEW_FRONTIER_NAMED_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_HARDENING",
    "REUSABLE_PRODUCTION_AUTHORITY_EXCLUDED_AFTER_RECONCILIATION",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
}

_COMMON_FALSE_FLAGS = (
    "approval_capture_performed_outside_exact_request",
    "reusable_production_blk_link_authority_granted",
    "production_blk_link_authority_granted_beyond_exact_run",
    "future_run_id_reserved_or_consumed",
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
    "target_repo_scan_or_mutation",
    "target_source_git_mutation_performed",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "beo_publication_or_signing_authorized",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)
SIDE_EFFECT_FLAGS_187 = ("request_one_exact_production_wrapper_run", "approval_capture_performed", "production_wrapper_run_executed", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_188 = ("per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_189 = ("next_frontier_granted", "observed_failure_requires_hardening", *_COMMON_FALSE_FLAGS)

_ATTESTATION_187 = frozenset({
    "exact_blk186_reconciliation_reviewed", "exact_blk184_contract_hash_bound",
    "one_exact_production_wrapper_run_requested", "approval_capture_not_performed",
    "production_wrapper_execution_not_performed_by_request", "per_run_exact_approval_required",
    "reusable_authority_not_granted", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_188 = frozenset({
    "exact_blk187_request_reviewed", "operator_decision_captured_for_exact_single_run",
    "run_id_consumed_once_in_execution_evidence", "single_production_wrapper_run_recorded_clean",
    "contract_hash_bound", "reusable_authority_not_granted_after_run", "protected_body_reads_excluded",
    "rtm_generation_excluded", "drift_rejection_excluded", "coverage_truth_excluded",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})
_ATTESTATION_189 = frozenset({
    "exact_blk188_execution_reviewed", "clean_single_run_reconciled", "next_frontier_not_granted",
    "no_observed_failure_requiring_hardening", "reusable_authority_not_granted_after_reconciliation",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})

_KEYS_187 = frozenset({
    "request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash", "upstream_contract_package_hash",
    "contract_hash", "beo_id", "beb_id", "exact_trace_identities", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_187,
})
_KEYS_188 = frozenset({
    "execution_package_id", "operator_identity", "execution_scope", "selected_frontier",
    "upstream_request_package_id", "upstream_request_package_hash", "upstream_contract_package_hash",
    "contract_hash", "approval_id", "run_id_to_consume", "beo_id", "beb_id", "exact_trace_identities",
    "operator_decision_text_raw", "runtime_notes", "decided_at", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_188,
})
_KEYS_189 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_execution_package_id", "upstream_execution_package_hash", "run_id_consumed",
    "wrapper_run_result_observed", "beo_id", "beb_id", "exact_trace_identities", "observed_failure_requires_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_189,
})
_KEYS_186_PACKAGE = frozenset({
    "reconciliation_status", "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_dry_run_package_id", "upstream_dry_run_package_hash", "run_id_consumed", "readiness_kernel_result",
    "beo_id", "beb_id", "exact_trace_identities", "clean_readiness_kernel_dry_run_reconciled",
    "observed_failure_requires_hardening", "recommended_next_frontier", "next_frontier_granted",
    "reconciliation_context_hash", "reconciled_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", "reconciliation_package_hash", *SIDE_EFFECT_FLAGS_186,
})


def valid_single_production_blk_link_wrapper_request_187(reconciliation186: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "request_package_id": REQUEST_PACKAGE_ID_187,
        "operator_identity": reconciliation186["operator_identity"],
        "request_scope": REQUEST_SCOPE_187,
        "selected_frontier": SELECTED_FRONTIER_187,
        "upstream_reconciliation_package_id": reconciliation186["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation186["reconciliation_package_hash"],
        "upstream_contract_package_hash": CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
        "contract_hash": CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
        "beo_id": reconciliation186["beo_id"],
        "beb_id": reconciliation186["beb_id"],
        "exact_trace_identities": list(reconciliation186["exact_trace_identities"]),
        "requested_at": "2099-05-17T00:00:00+10:00",
        "expires_at": "2099-05-18T00:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_187},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_187),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_187),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_187, {"request_one_exact_production_wrapper_run"})
    record.update(overrides)
    return record


def build_single_production_blk_link_wrapper_request_187(reconciliation186_package: dict[str, Any], request187: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_186_package(reconciliation186_package)
    request = _validate_request_like(request187, _KEYS_187, _ATTESTATION_187, EXACT_PROOF_OBLIGATIONS_187, EXACT_EXCLUDED_AUTHORITIES_187, SIDE_EFFECT_FLAGS_187, {"request_one_exact_production_wrapper_run"})
    _require(request, "request_package_id", REQUEST_PACKAGE_ID_187)
    _require(request, "request_scope", REQUEST_SCOPE_187)
    _require(request, "selected_frontier", SELECTED_FRONTIER_187)
    _require(request, "upstream_contract_package_hash", CANONICAL_BLK184_CONTRACT_PACKAGE_HASH)
    _require(request, "contract_hash", CANONICAL_BLK184_CONTRACT_PACKAGE_HASH)
    _require_matching_upstream(request, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(request["requested_at"], request["expires_at"], "single production wrapper request")
    trace_ids = _validate_trace_copy(request["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "request_status": REQUEST_STATUS_187,
        "request_package_id": REQUEST_PACKAGE_ID_187,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_187,
        "selected_frontier": SELECTED_FRONTIER_187,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_contract_package_hash": CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
        "contract_hash": CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "request_one_exact_production_wrapper_run": True,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_187,
        "request_hash": _canonical_hash(request),
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_187),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_187),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_187, {"request_one_exact_production_wrapper_run"})
    package["request_package_hash"] = _canonical_hash(package)
    return package


def valid_single_production_blk_link_wrapper_execution_188(request187: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "execution_package_id": EXECUTION_PACKAGE_ID_188,
        "operator_identity": request187["operator_identity"],
        "execution_scope": EXECUTION_SCOPE_188,
        "selected_frontier": SELECTED_FRONTIER_188,
        "upstream_request_package_id": request187["request_package_id"],
        "upstream_request_package_hash": request187["request_package_hash"],
        "upstream_contract_package_hash": request187["upstream_contract_package_hash"],
        "contract_hash": request187["contract_hash"],
        "approval_id": APPROVAL_ID_188,
        "run_id_to_consume": RUN_ID_CONSUMED_188,
        "beo_id": request187["beo_id"],
        "beb_id": request187["beb_id"],
        "exact_trace_identities": list(request187["exact_trace_identities"]),
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_188,
        "runtime_notes": "One exact production blk-link wrapper run is represented as bounded evidence only; no RTM, drift, coverage, protected body, tooling, or mutation authority is added.",
        "decided_at": "2099-05-17T00:10:00+10:00",
        "requested_at": "2099-05-17T00:11:00+10:00",
        "expires_at": "2099-05-17T00:25:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_188},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_188),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_188),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_188, {"per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed"})
    record.update(overrides)
    return record


def build_single_production_blk_link_wrapper_execution_188(request187_package: dict[str, Any], execution188: dict[str, Any]) -> dict[str, Any]:
    request = _validate_187_package(request187_package)
    execution = _validate_request_like(
        execution188, _KEYS_188, _ATTESTATION_188, EXACT_PROOF_OBLIGATIONS_188, EXACT_EXCLUDED_AUTHORITIES_188, SIDE_EFFECT_FLAGS_188,
        {"per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed"},
    )
    _scan_high_risk_freeform(execution["runtime_notes"], "runtime_notes")
    _require(execution, "execution_package_id", EXECUTION_PACKAGE_ID_188)
    _require(execution, "execution_scope", EXECUTION_SCOPE_188)
    _require(execution, "selected_frontier", SELECTED_FRONTIER_188)
    _require(execution, "approval_id", APPROVAL_ID_188)
    _require(execution, "run_id_to_consume", RUN_ID_CONSUMED_188)
    _require(execution, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_188)
    _require_matching_upstream(execution, request, (
        ("upstream_request_package_id", "request_package_id"),
        ("upstream_request_package_hash", "request_package_hash"),
        ("upstream_contract_package_hash", "upstream_contract_package_hash"),
        ("contract_hash", "contract_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_execution_window(execution["decided_at"], execution["requested_at"], execution["expires_at"], request["requested_at"], request["expires_at"])
    trace_ids = _validate_trace_copy(execution["exact_trace_identities"], request["exact_trace_identities"])
    package = {
        "execution_status": EXECUTION_STATUS_188,
        "execution_package_id": EXECUTION_PACKAGE_ID_188,
        "operator_identity": execution["operator_identity"],
        "execution_scope": EXECUTION_SCOPE_188,
        "selected_frontier": SELECTED_FRONTIER_188,
        "upstream_request_package_id": request["request_package_id"],
        "upstream_request_package_hash": request["request_package_hash"],
        "upstream_contract_package_hash": request["upstream_contract_package_hash"],
        "contract_hash": request["contract_hash"],
        "approval_id": APPROVAL_ID_188,
        "run_id_consumed": RUN_ID_CONSUMED_188,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_188,
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "exact_trace_identities": trace_ids,
        "per_run_exact_approval_captured": True,
        "one_run_id_consumed_in_production_wrapper_evidence": True,
        "production_wrapper_run_executed": True,
        "wrapper_run_result": "SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECORDED_CLEAN",
        "execution_request_hash": _canonical_hash(execution),
        "decided_at": execution["decided_at"],
        "requested_at": execution["requested_at"],
        "expires_at": execution["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_188,
        "operator_attestation": deepcopy(execution["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_188),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_188),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_188, {"per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed"})
    package["execution_package_hash"] = _canonical_hash(package)
    return package


def valid_single_production_blk_link_wrapper_reconciliation_189(execution188: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_189,
        "operator_identity": execution188["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_189,
        "selected_frontier": SELECTED_FRONTIER_189,
        "upstream_execution_package_id": execution188["execution_package_id"],
        "upstream_execution_package_hash": execution188["execution_package_hash"],
        "run_id_consumed": execution188["run_id_consumed"],
        "wrapper_run_result_observed": execution188["wrapper_run_result"],
        "beo_id": execution188["beo_id"],
        "beb_id": execution188["beb_id"],
        "exact_trace_identities": list(execution188["exact_trace_identities"]),
        "observed_failure_requires_hardening": False,
        "reconciled_at": "2099-05-17T00:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_189},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_189),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_189),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_189, set())
    record.update(overrides)
    return record


def build_single_production_blk_link_wrapper_reconciliation_189(execution188_package: dict[str, Any], context189: dict[str, Any]) -> dict[str, Any]:
    execution = _validate_188_package(execution188_package)
    context = _validate_request_like(context189, _KEYS_189, _ATTESTATION_189, EXACT_PROOF_OBLIGATIONS_189, EXACT_EXCLUDED_AUTHORITIES_189, SIDE_EFFECT_FLAGS_189)
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_189)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_189)
    _require(context, "selected_frontier", SELECTED_FRONTIER_189)
    _require_false(context, "observed_failure_requires_hardening")
    _require_matching_upstream(context, execution, (
        ("upstream_execution_package_id", "execution_package_id"),
        ("upstream_execution_package_hash", "execution_package_hash"),
        ("run_id_consumed", "run_id_consumed"),
        ("wrapper_run_result_observed", "wrapper_run_result"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], execution["exact_trace_identities"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_189,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_189,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_189,
        "selected_frontier": SELECTED_FRONTIER_189,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "wrapper_run_result": execution["wrapper_run_result"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": trace_ids,
        "clean_single_production_wrapper_run_reconciled": True,
        "observed_failure_requires_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_189_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_189),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_189),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_189, set())
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _set_flags(record: dict[str, Any], flags: tuple[str, ...], true_flags: set[str]) -> None:
    for flag in flags:
        record[flag] = flag in true_flags


def _validate_request_like(record: Any, keys: frozenset[str], attestation_keys: frozenset[str], proof_set: set[str], excluded_set: set[str], flags: tuple[str, ...], true_flags: set[str] | None = None) -> dict[str, Any]:
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
    if set(record["operator_attestation"]) != attestation_keys:
        extra_attestation = sorted(set(record["operator_attestation"]) - attestation_keys)
        if extra_attestation:
            raise ValueError(f"unexpected field {extra_attestation[0]!r}")
        raise ValueError("operator_attestation must match exact key set")
    for key, value in record["operator_attestation"].items():
        if value is not True:
            raise ValueError(f"operator_attestation {key} must be true")
    _required_exact_set(record.get("proof_obligations"), proof_set, "proof_obligations")
    _required_exact_set(record.get("excluded_authorities"), excluded_set, "excluded_authorities")
    _scan_high_risk_freeform(record.get("operator_identity"), "operator_identity")
    for flag in flags:
        expected = flag in true_flags
        if record.get(flag) is not expected:
            if expected:
                raise ValueError(f"{flag} must be true")
            raise ValueError(f"{flag} must remain false")
    return record


def _validate_186_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-186 package must be a dictionary")
    extra = sorted(set(package) - _KEYS_186_PACKAGE)
    if extra:
        raise ValueError(f"unexpected BLK-186 field {extra[0]!r}")
    missing = sorted(_KEYS_186_PACKAGE - set(package))
    if missing:
        raise ValueError(f"missing BLK-186 field {missing[0]!r}")
    _require(package, "reconciliation_status", RECONCILIATION_STATUS_186)
    _require(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_186)
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_186)
    _require(package, "selected_frontier", SELECTED_FRONTIER_186)
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-186 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-186 reconciliation package hash mismatch")
    if package.get("upstream_dry_run_package_hash") != CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH:
        raise ValueError("BLK-186 must bind canonical BLK-185 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_186, "BLK-186 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_186, "BLK-186 excluded_authorities")
    if package.get("clean_readiness_kernel_dry_run_reconciled") is not True:
        raise ValueError("BLK-186 must reconcile cleanly")
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-186 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_186:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-186 package {flag} must remain false")
    return package


def _validate_187_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-187 package must be a dictionary")
    _require(package, "request_status", REQUEST_STATUS_187)
    _require(package, "request_package_id", REQUEST_PACKAGE_ID_187)
    _require(package, "request_scope", REQUEST_SCOPE_187)
    _require(package, "selected_frontier", SELECTED_FRONTIER_187)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_187)
    _required_hash(package.get("request_package_hash"), "request_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"})
    if package["request_package_hash"] != computed:
        raise ValueError("request_package_hash does not match submitted BLK-187 package")
    _require_canonical(package["request_package_hash"], CANONICAL_BLK187_REQUEST_PACKAGE_HASH, "canonical BLK-187 request package hash mismatch")
    if package.get("upstream_reconciliation_package_hash") != CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-187 must bind canonical BLK-186 package hash")
    if package.get("upstream_contract_package_hash") != CANONICAL_BLK184_CONTRACT_PACKAGE_HASH:
        raise ValueError("BLK-187 must bind canonical BLK-184 contract package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_187, "BLK-187 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_187, "BLK-187 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_187:
        expected = flag == "request_one_exact_production_wrapper_run"
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-187 package {flag} must be {expected}")
    return package


def _validate_188_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-188 package must be a dictionary")
    _require(package, "execution_status", EXECUTION_STATUS_188)
    _require(package, "execution_package_id", EXECUTION_PACKAGE_ID_188)
    _require(package, "execution_scope", EXECUTION_SCOPE_188)
    _require(package, "selected_frontier", SELECTED_FRONTIER_188)
    _require(package, "approval_id", APPROVAL_ID_188)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_188)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_188)
    _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"})
    if package["execution_package_hash"] != computed:
        raise ValueError("execution_package_hash does not match submitted BLK-188 package")
    _require_canonical(package["execution_package_hash"], CANONICAL_BLK188_EXECUTION_PACKAGE_HASH, "canonical BLK-188 execution package hash mismatch")
    if package.get("upstream_request_package_hash") != CANONICAL_BLK187_REQUEST_PACKAGE_HASH:
        raise ValueError("BLK-188 must bind canonical BLK-187 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_188, "BLK-188 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_188, "BLK-188 excluded_authorities")
    true_flags = {"per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed"}
    for flag in SIDE_EFFECT_FLAGS_188:
        expected = flag in true_flags
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-188 package {flag} must be {expected}")
    return package


def _validate_execution_window(decided_at: str, requested_at: str, expires_at: str, upstream_requested_at: str, upstream_expires_at: str) -> None:
    decided = _parse_not_stale(decided_at, "decision execution request")
    requested = _parse_not_stale(requested_at, "requested_at")
    expires = _parse_not_stale(expires_at, "expires_at")
    upstream_requested = _parse_not_stale(upstream_requested_at, "upstream requested_at")
    upstream_expires = _parse_not_stale(upstream_expires_at, "upstream expires_at")
    if decided < upstream_requested:
        raise ValueError("decision must not predate BLK-187 request")
    if requested < decided or expires <= requested or expires > upstream_expires:
        raise ValueError("approval request must be within approval decision window")


def _require_canonical(observed: str, canonical: str, message: str) -> None:
    placeholder = canonical.endswith("0000000000000187") or canonical.endswith("0000000000000188") or canonical.endswith("0000000000000189")
    if not placeholder and observed != canonical:
        raise ValueError(message)
