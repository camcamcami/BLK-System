"""BLK-SYSTEM-183..186 reusable production blk-link readiness kernel.

This deterministic fixture advances from the BLK-182 protected-body evidence
metadata-export reconciliation to a reusable production-grade `blk-link`
readiness kernel whose mechanism is reusable but whose execution authority is
still per-run and exact.

It does not grant reusable production `blk-link` authority, perform live
production `blk-link`, generate RTM, reject drift, establish coverage truth,
read/copy/parse/hash/scan protected bodies, mutate target/source/Git, run
BLK-pipe/BLK-test/Codex/tooling, reuse signer/storage/ledger authority, or claim
production isolation.
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
from rtm_blk_link_followup_ladder_178_182 import (
    CANONICAL_BLK181_EXPORT_PACKAGE_HASH,
    CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_182,
    EXACT_PROOF_OBLIGATIONS_182,
    RECONCILIATION_PACKAGE_ID_182,
    RECONCILIATION_SCOPE_182,
    RECONCILIATION_STATUS_182,
    SELECTED_FRONTIER_182,
    SIDE_EFFECT_FLAGS_182,
)

DECISION_STATUS_183 = "REUSABLE_PRODUCTION_BLK_LINK_READINESS_KERNEL_DECISION_READY_NOT_APPROVED"
DECISION_PACKAGE_ID_183 = "REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-DECISION-183-001"
DECISION_SCOPE_183 = "SELECT_REUSABLE_KERNEL_MECHANISM_PATH_NOT_AUTHORITY_GRANT"
SELECTED_FRONTIER_183 = "reusable_production_blk_link_readiness_kernel_decision_183"
NEXT_REQUIRED_AUTHORITY_183 = "REUSABLE_KERNEL_CONTRACT_EMISSION_REQUIRED_NOT_GRANTED"
CANONICAL_BLK183_DECISION_PACKAGE_HASH = "sha256:2a61d12caf1338897c09c33d1848359a3798b690ae0d627f1cc771651d251e36"

CONTRACT_STATUS_184 = "REUSABLE_PRODUCTION_BLK_LINK_READINESS_KERNEL_CONTRACT_EMITTED_NOT_AUTHORITY"
CONTRACT_PACKAGE_ID_184 = "REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-CONTRACT-184-001"
CONTRACT_SCOPE_184 = "REUSABLE_MECHANISM_CONTRACT_PER_RUN_EXACT_APPROVAL_REQUIRED"
SELECTED_FRONTIER_184 = "reusable_production_blk_link_readiness_kernel_contract_184"
NEXT_REQUIRED_AUTHORITY_184 = "ONE_EXACT_DRY_RUN_APPROVAL_REQUIRED_NOT_GRANTED"
CANONICAL_BLK184_CONTRACT_PACKAGE_HASH = "sha256:c79bded6e77048852f26239eee6483fa07b92bf5d8012fe80ef2aba992537ac9"

DRY_RUN_STATUS_185 = "REUSABLE_PRODUCTION_BLK_LINK_READINESS_KERNEL_DRY_RUN_RECORDED"
DRY_RUN_PACKAGE_ID_185 = "REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-DRY-RUN-185-001"
DRY_RUN_SCOPE_185 = "ONE_EXACT_APPROVED_READINESS_KERNEL_DRY_RUN_NO_LIVE_PRODUCTION_EXECUTION"
SELECTED_FRONTIER_185 = "reusable_production_blk_link_readiness_kernel_dry_run_185"
APPROVAL_ID_185 = "APPROVAL-BLK-SYSTEM-185-REUSABLE-BLK-LINK-READINESS-KERNEL-DRY-RUN-001"
RUN_ID_CONSUMED_185 = "RUN-BLK-SYSTEM-185-REUSABLE-BLK-LINK-READINESS-KERNEL-DRY-RUN-001"
EXACT_OPERATOR_DECISION_TEXT_185 = (
    "APPROVE REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-CONTRACT-184-001 "
    "FOR ONE READINESS-KERNEL DRY-RUN "
    "RUN-BLK-SYSTEM-185-REUSABLE-BLK-LINK-READINESS-KERNEL-DRY-RUN-001; "
    "PER-RUN EXACT APPROVAL ONLY; NO LIVE PRODUCTION BLK-LINK EXECUTION; "
    "NO REUSABLE AUTHORITY; NO PROTECTED BODY READS; NO RTM GENERATION; "
    "NO DRIFT REJECTION; NO COVERAGE TRUTH; NO MUTATION."
)
NEXT_REQUIRED_AUTHORITY_185 = "POST_DRY_RUN_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH = "sha256:41b1af8f635edb3e1d8e61cebdf95773552a6867ee2984b01eba4e509b263cc8"

RECONCILIATION_STATUS_186 = "REUSABLE_PRODUCTION_BLK_LINK_READINESS_KERNEL_DRY_RUN_RECONCILED_CLEAN"
RECONCILIATION_PACKAGE_ID_186 = "REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-RECONCILIATION-186-001"
RECONCILIATION_SCOPE_186 = "POST_DRY_RUN_RECONCILIATION_ONLY_NO_PRODUCTION_AUTHORITY"
SELECTED_FRONTIER_186 = "reusable_production_blk_link_readiness_kernel_reconciliation_186"
NEXT_FRONTIER_186_CLEAN = "NEXT_FRONTIER_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_REQUEST_NOT_GRANTED"
CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH = "sha256:f5a8bc6a27428b5fa9e20d3c0d8a4d22a8e71d6bf513be6d495c6c1f71a02e71"

_BASE_EXCLUDED = {
    "REUSABLE_PRODUCTION_BLK_LINK_AUTHORITY",
    "PRODUCTION_BLK_LINK_LIVE_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_LINK_EXECUTION_BEYOND_ONE_EXACT_FUTURE_REQUEST",
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
EXACT_EXCLUDED_AUTHORITIES_183 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "CONTRACT_EMISSION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_DECISION_PACKAGE",
}
EXACT_EXCLUDED_AUTHORITIES_184 = _BASE_EXCLUDED | {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "DRY_RUN_EXECUTION_THIS_SPRINT",
    "CONTRACT_IS_NOT_REUSABLE_AUTHORITY",
}
EXACT_EXCLUDED_AUTHORITIES_185 = _BASE_EXCLUDED | {
    "LIVE_PRODUCTION_EXECUTION_THIS_SPRINT",
    "REUSABLE_AUTHORITY_FROM_DRY_RUN",
    "FUTURE_RUN_ID_RESERVATION_BEYOND_CONSUMED_DRY_RUN",
}
EXACT_EXCLUDED_AUTHORITIES_186 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "RECONCILIATION_IS_NOT_PRODUCTION_EXECUTION_AUTHORITY",
}

EXACT_PROOF_OBLIGATIONS_183 = {
    "BLK182_EXPORT_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "REUSABLE_KERNEL_MECHANISM_PATH_SELECTED_WITH_AUTHORITY_NOT_GRANTED",
    "PER_RUN_EXACT_APPROVAL_REQUIRED_FOR_ANY_FUTURE_EXECUTION",
    "PRODUCTION_BLK_LINK_RUNTIME_NOT_PERFORMED",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_184 = {
    "BLK183_DECISION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "REUSABLE_CONTRACT_SCHEMA_EMITTED",
    "CONTRACT_REQUIRES_EXACT_APPROVAL_ID_AND_RUN_ID_PER_RUN",
    "CONTRACT_REQUIRES_CANONICAL_UPSTREAM_HASH_BINDING",
    "CONTRACT_FORBIDS_PROTECTED_BODY_TEXT_AND_PATHS",
    "CONTRACT_FORBIDS_TARGET_SOURCE_GIT_MUTATION",
    "CONTRACT_IS_MECHANISM_NOT_REUSABLE_AUTHORITY",
}
EXACT_PROOF_OBLIGATIONS_185 = {
    "BLK184_CONTRACT_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "EXACT_OPERATOR_APPROVAL_TEXT_BOUND_TO_CONTRACT_AND_RUN_ID",
    "ONE_RUN_ID_CONSUMED_IN_DRY_RUN_EVIDENCE",
    "READINESS_KERNEL_DRY_RUN_EVALUATED_WITHOUT_LIVE_PRODUCTION_EXECUTION",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_186 = {
    "BLK185_DRY_RUN_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "CLEAN_READINESS_KERNEL_DRY_RUN_RECONCILED_WITHOUT_AUTHORITY_PROMOTION",
    "NEXT_ONE_EXACT_PRODUCTION_WRAPPER_REQUEST_FRONTIER_NAMED_NOT_GRANTED",
    "NO_OBSERVED_FAILURE_REQUIRING_HARDENING",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
}

_COMMON_FALSE_FLAGS = (
    "approval_capture_performed_outside_exact_request",
    "production_blk_link_authority_granted",
    "reusable_production_blk_link_authority_granted",
    "production_blk_link_live_execution_performed",
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
SIDE_EFFECT_FLAGS_183 = ("reusable_kernel_path_selected", "approval_capture_performed", "future_run_id_reserved_or_consumed", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_184 = ("reusable_kernel_contract_emitted", "approval_capture_performed", "future_run_id_reserved_or_consumed", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_185 = ("per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_186 = ("next_frontier_granted", "observed_failure_requires_hardening", *_COMMON_FALSE_FLAGS)

_ATTESTATION_183 = frozenset({
    "exact_blk182_reconciliation_reviewed", "reusable_kernel_mechanism_path_selected",
    "per_run_exact_approval_required", "approval_capture_not_performed", "run_id_not_reserved_or_consumed",
    "production_blk_link_runtime_excluded", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})
_ATTESTATION_184 = frozenset({
    "exact_blk183_decision_reviewed", "reusable_contract_schema_emitted",
    "per_run_exact_approval_id_required", "per_run_exact_run_id_required",
    "canonical_upstream_hash_binding_required", "protected_body_text_and_paths_forbidden",
    "target_source_git_mutation_forbidden", "contract_is_not_reusable_authority",
    "production_blk_link_runtime_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "no_production_isolation_claim",
})
_ATTESTATION_185 = frozenset({
    "exact_blk184_contract_reviewed", "operator_decision_captured_for_exact_dry_run",
    "run_id_consumed_once_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated",
    "live_production_blk_link_execution_not_performed", "reusable_authority_not_granted",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})
_ATTESTATION_186 = frozenset({
    "exact_blk185_dry_run_reviewed", "clean_dry_run_reconciled", "next_frontier_not_granted",
    "no_observed_failure_requiring_hardening", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "reusable_authority_not_granted",
    "target_source_git_mutation_excluded", "blk_pipe_blk_test_codex_tooling_excluded", "no_production_isolation_claim",
})

_KEYS_183 = frozenset({
    "decision_package_id", "operator_identity", "decision_scope", "selected_frontier",
    "upstream_export_reconciliation_package_id", "upstream_export_reconciliation_package_hash",
    "upstream_export_package_hash", "upstream_export_manifest_hash", "beo_id", "beb_id",
    "exact_trace_identities", "requested_at", "expires_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_183,
})
_KEYS_184 = frozenset({
    "contract_package_id", "operator_identity", "contract_scope", "selected_frontier",
    "upstream_decision_package_id", "upstream_decision_package_hash", "upstream_export_reconciliation_package_hash",
    "beo_id", "beb_id", "exact_trace_identities", "contract_notes", "contract_emitted_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_184,
})
_KEYS_185 = frozenset({
    "dry_run_package_id", "operator_identity", "dry_run_scope", "selected_frontier",
    "upstream_contract_package_id", "upstream_contract_package_hash", "contract_hash",
    "approval_id", "run_id_to_consume", "beo_id", "beb_id", "exact_trace_identities",
    "operator_decision_text_raw", "runtime_notes", "decided_at", "requested_at", "expires_at",
    "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_185,
})
_KEYS_186 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_dry_run_package_id", "upstream_dry_run_package_hash", "run_id_consumed",
    "readiness_kernel_result_observed", "beo_id", "beb_id", "exact_trace_identities", "observed_failure_requires_hardening",
    "reconciled_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations", "excluded_authorities",
    *SIDE_EFFECT_FLAGS_186,
})
_KEYS_182_PACKAGE = frozenset({
    "reconciliation_status", "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_export_package_id", "upstream_export_package_hash", "upstream_export_manifest_hash",
    "beo_id", "beb_id", "exact_trace_identities", "protected_body_verification_lineage_hash",
    "clean_export_reconciled", "observed_failure_requires_hardening", "recommended_next_frontier", "next_frontier_granted",
    "reconciliation_context_hash", "reconciled_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", "reconciliation_package_hash", *SIDE_EFFECT_FLAGS_182,
})


def valid_reusable_blk_link_readiness_decision_183(reconciliation182: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "decision_package_id": DECISION_PACKAGE_ID_183,
        "operator_identity": reconciliation182["operator_identity"],
        "decision_scope": DECISION_SCOPE_183,
        "selected_frontier": SELECTED_FRONTIER_183,
        "upstream_export_reconciliation_package_id": reconciliation182["reconciliation_package_id"],
        "upstream_export_reconciliation_package_hash": reconciliation182["reconciliation_package_hash"],
        "upstream_export_package_hash": reconciliation182["upstream_export_package_hash"],
        "upstream_export_manifest_hash": reconciliation182["upstream_export_manifest_hash"],
        "beo_id": reconciliation182["beo_id"],
        "beb_id": reconciliation182["beb_id"],
        "exact_trace_identities": list(reconciliation182["exact_trace_identities"]),
        "requested_at": "2099-05-16T23:00:00+10:00",
        "expires_at": "2099-05-17T23:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_183},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_183),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_183),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_183, {"reusable_kernel_path_selected"})
    record.update(overrides)
    return record


def build_reusable_blk_link_readiness_decision_183(reconciliation182_package: dict[str, Any], decision183: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_182_package(reconciliation182_package)
    decision = _validate_request_like(decision183, _KEYS_183, _ATTESTATION_183, EXACT_PROOF_OBLIGATIONS_183, EXACT_EXCLUDED_AUTHORITIES_183, SIDE_EFFECT_FLAGS_183, {"reusable_kernel_path_selected"})
    _require(decision, "decision_package_id", DECISION_PACKAGE_ID_183)
    _require(decision, "decision_scope", DECISION_SCOPE_183)
    _require(decision, "selected_frontier", SELECTED_FRONTIER_183)
    _require_matching_upstream(decision, upstream, (
        ("upstream_export_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_export_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_export_package_hash", "upstream_export_package_hash"),
        ("upstream_export_manifest_hash", "upstream_export_manifest_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_time_window(decision["requested_at"], decision["expires_at"], "readiness decision")
    trace_ids = _validate_trace_copy(decision["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "decision_status": DECISION_STATUS_183,
        "decision_package_id": DECISION_PACKAGE_ID_183,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE_183,
        "selected_frontier": SELECTED_FRONTIER_183,
        "upstream_export_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_export_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_export_package_hash": upstream["upstream_export_package_hash"],
        "upstream_export_manifest_hash": upstream["upstream_export_manifest_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "reusable_kernel_path_selected": True,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_183,
        "decision_request_hash": _canonical_hash(decision),
        "requested_at": decision["requested_at"],
        "expires_at": decision["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_183),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_183),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_183, {"reusable_kernel_path_selected"})
    package["decision_package_hash"] = _canonical_hash(package)
    return package


def valid_reusable_blk_link_readiness_kernel_contract_184(decision183: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "contract_package_id": CONTRACT_PACKAGE_ID_184,
        "operator_identity": decision183["operator_identity"],
        "contract_scope": CONTRACT_SCOPE_184,
        "selected_frontier": SELECTED_FRONTIER_184,
        "upstream_decision_package_id": decision183["decision_package_id"],
        "upstream_decision_package_hash": decision183["decision_package_hash"],
        "upstream_export_reconciliation_package_hash": decision183["upstream_export_reconciliation_package_hash"],
        "beo_id": decision183["beo_id"],
        "beb_id": decision183["beb_id"],
        "exact_trace_identities": list(decision183["exact_trace_identities"]),
        "contract_notes": "Reusable mechanism contract only; every live or dry run requires exact per-run approval.",
        "contract_emitted_at": "2099-05-16T23:05:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_184},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_184),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_184),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_184, {"reusable_kernel_contract_emitted"})
    record.update(overrides)
    return record


def build_reusable_blk_link_readiness_kernel_contract_184(decision183_package: dict[str, Any], contract184: dict[str, Any]) -> dict[str, Any]:
    decision = _validate_183_package(decision183_package)
    record = _validate_request_like(contract184, _KEYS_184, _ATTESTATION_184, EXACT_PROOF_OBLIGATIONS_184, EXACT_EXCLUDED_AUTHORITIES_184, SIDE_EFFECT_FLAGS_184, {"reusable_kernel_contract_emitted"})
    _scan_high_risk_freeform(record["contract_notes"], "contract_notes")
    _require(record, "contract_package_id", CONTRACT_PACKAGE_ID_184)
    _require(record, "contract_scope", CONTRACT_SCOPE_184)
    _require(record, "selected_frontier", SELECTED_FRONTIER_184)
    _require_matching_upstream(record, decision, (
        ("upstream_decision_package_id", "decision_package_id"),
        ("upstream_decision_package_hash", "decision_package_hash"),
        ("upstream_export_reconciliation_package_hash", "upstream_export_reconciliation_package_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(record["contract_emitted_at"], "contract context")
    trace_ids = _validate_trace_copy(record["exact_trace_identities"], decision["exact_trace_identities"])
    contract = _build_contract(record, trace_ids)
    package = {
        "contract_status": CONTRACT_STATUS_184,
        "contract_package_id": CONTRACT_PACKAGE_ID_184,
        "operator_identity": record["operator_identity"],
        "contract_scope": CONTRACT_SCOPE_184,
        "selected_frontier": SELECTED_FRONTIER_184,
        "upstream_decision_package_id": decision["decision_package_id"],
        "upstream_decision_package_hash": decision["decision_package_hash"],
        "upstream_export_reconciliation_package_hash": decision["upstream_export_reconciliation_package_hash"],
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
        "exact_trace_identities": trace_ids,
        "reusable_kernel_contract_emitted": True,
        "contract": contract,
        "contract_hash": _canonical_hash(contract),
        "contract_request_hash": _canonical_hash(record),
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_184,
        "contract_emitted_at": record["contract_emitted_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(record["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_184),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_184),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_184, {"reusable_kernel_contract_emitted"})
    package["contract_package_hash"] = _canonical_hash(package)
    return package


def valid_reusable_blk_link_readiness_kernel_dry_run_185(contract184: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "dry_run_package_id": DRY_RUN_PACKAGE_ID_185,
        "operator_identity": contract184["operator_identity"],
        "dry_run_scope": DRY_RUN_SCOPE_185,
        "selected_frontier": SELECTED_FRONTIER_185,
        "upstream_contract_package_id": contract184["contract_package_id"],
        "upstream_contract_package_hash": contract184["contract_package_hash"],
        "contract_hash": contract184["contract_hash"],
        "approval_id": APPROVAL_ID_185,
        "run_id_to_consume": RUN_ID_CONSUMED_185,
        "beo_id": contract184["beo_id"],
        "beb_id": contract184["beb_id"],
        "exact_trace_identities": list(contract184["exact_trace_identities"]),
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_185,
        "runtime_notes": "Dry-run evaluates reusable readiness kernel contract only; no live production execution.",
        "decided_at": "2099-05-16T23:10:00+10:00",
        "requested_at": "2099-05-16T23:11:00+10:00",
        "expires_at": "2099-05-16T23:25:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_185},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_185),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_185),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_185, {"per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated"})
    record.update(overrides)
    return record


def build_reusable_blk_link_readiness_kernel_dry_run_185(contract184_package: dict[str, Any], dryrun185: dict[str, Any]) -> dict[str, Any]:
    contract_pkg = _validate_184_package(contract184_package)
    record = _validate_request_like(
        dryrun185, _KEYS_185, _ATTESTATION_185, EXACT_PROOF_OBLIGATIONS_185, EXACT_EXCLUDED_AUTHORITIES_185, SIDE_EFFECT_FLAGS_185,
        {"per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated"},
    )
    _scan_high_risk_freeform(record["runtime_notes"], "runtime_notes")
    _require(record, "dry_run_package_id", DRY_RUN_PACKAGE_ID_185)
    _require(record, "dry_run_scope", DRY_RUN_SCOPE_185)
    _require(record, "selected_frontier", SELECTED_FRONTIER_185)
    _require(record, "approval_id", APPROVAL_ID_185)
    _require(record, "run_id_to_consume", RUN_ID_CONSUMED_185)
    _require(record, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_185)
    _require_matching_upstream(record, contract_pkg, (
        ("upstream_contract_package_id", "contract_package_id"),
        ("upstream_contract_package_hash", "contract_package_hash"),
        ("contract_hash", "contract_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_dry_run_window(record["decided_at"], record["requested_at"], record["expires_at"], contract_pkg["contract_emitted_at"])
    trace_ids = _validate_trace_copy(record["exact_trace_identities"], contract_pkg["exact_trace_identities"])
    package = {
        "dry_run_status": DRY_RUN_STATUS_185,
        "dry_run_package_id": DRY_RUN_PACKAGE_ID_185,
        "operator_identity": record["operator_identity"],
        "dry_run_scope": DRY_RUN_SCOPE_185,
        "selected_frontier": SELECTED_FRONTIER_185,
        "upstream_contract_package_id": contract_pkg["contract_package_id"],
        "upstream_contract_package_hash": contract_pkg["contract_package_hash"],
        "contract_hash": contract_pkg["contract_hash"],
        "contract": deepcopy(contract_pkg["contract"]),
        "approval_id": APPROVAL_ID_185,
        "run_id_consumed": RUN_ID_CONSUMED_185,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_185,
        "beo_id": contract_pkg["beo_id"],
        "beb_id": contract_pkg["beb_id"],
        "exact_trace_identities": trace_ids,
        "per_run_exact_approval_captured": True,
        "one_run_id_consumed_in_dry_run_evidence": True,
        "readiness_kernel_dry_run_evaluated": True,
        "readiness_kernel_result": "READY_FOR_ONE_EXACT_PRODUCTION_WRAPPER_REQUEST_NOT_GRANTED",
        "dry_run_request_hash": _canonical_hash(record),
        "decided_at": record["decided_at"],
        "requested_at": record["requested_at"],
        "expires_at": record["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_185,
        "operator_attestation": deepcopy(record["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_185),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_185),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_185, {"per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated"})
    package["dry_run_package_hash"] = _canonical_hash(package)
    return package


def valid_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_186,
        "operator_identity": dryrun185["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_186,
        "selected_frontier": SELECTED_FRONTIER_186,
        "upstream_dry_run_package_id": dryrun185["dry_run_package_id"],
        "upstream_dry_run_package_hash": dryrun185["dry_run_package_hash"],
        "run_id_consumed": dryrun185["run_id_consumed"],
        "readiness_kernel_result_observed": dryrun185["readiness_kernel_result"],
        "beo_id": dryrun185["beo_id"],
        "beb_id": dryrun185["beb_id"],
        "exact_trace_identities": list(dryrun185["exact_trace_identities"]),
        "observed_failure_requires_hardening": False,
        "reconciled_at": "2099-05-16T23:30:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_186},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_186),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_186),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_186, set())
    record.update(overrides)
    return record


def build_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185_package: dict[str, Any], context186: dict[str, Any]) -> dict[str, Any]:
    dryrun = _validate_185_package(dryrun185_package)
    context = _validate_request_like(context186, _KEYS_186, _ATTESTATION_186, EXACT_PROOF_OBLIGATIONS_186, EXACT_EXCLUDED_AUTHORITIES_186, SIDE_EFFECT_FLAGS_186)
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_186)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_186)
    _require(context, "selected_frontier", SELECTED_FRONTIER_186)
    _require_false(context, "observed_failure_requires_hardening")
    _require_matching_upstream(context, dryrun, (
        ("upstream_dry_run_package_id", "dry_run_package_id"),
        ("upstream_dry_run_package_hash", "dry_run_package_hash"),
        ("run_id_consumed", "run_id_consumed"),
        ("readiness_kernel_result_observed", "readiness_kernel_result"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(context["reconciled_at"], "reconciliation context")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], dryrun["exact_trace_identities"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_186,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_186,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_186,
        "selected_frontier": SELECTED_FRONTIER_186,
        "upstream_dry_run_package_id": dryrun["dry_run_package_id"],
        "upstream_dry_run_package_hash": dryrun["dry_run_package_hash"],
        "run_id_consumed": dryrun["run_id_consumed"],
        "readiness_kernel_result": dryrun["readiness_kernel_result"],
        "beo_id": dryrun["beo_id"],
        "beb_id": dryrun["beb_id"],
        "exact_trace_identities": trace_ids,
        "clean_readiness_kernel_dry_run_reconciled": True,
        "observed_failure_requires_hardening": False,
        "recommended_next_frontier": NEXT_FRONTIER_186_CLEAN,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_186),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_186),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_186, set())
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


def _build_contract(record: dict[str, Any], trace_ids: list[str]) -> dict[str, Any]:
    return {
        "contract_id": "REUSABLE-PRODUCTION-BLK-LINK-READINESS-KERNEL-CONTRACT-184-001",
        "contract_mode": "REUSABLE_MECHANISM_PER_RUN_EXACT_APPROVAL_REQUIRED",
        "beo_id": record["beo_id"],
        "beb_id": record["beb_id"],
        "exact_trace_identities": list(trace_ids),
        "required_per_run_fields": [
            "exact_approval_id", "exact_run_id", "operator_identity", "operator_decision_text_raw",
            "upstream_contract_package_hash", "contract_hash", "requested_at", "expires_at",
        ],
        "allows_reusable_authority": False,
        "allows_live_production_execution_without_exact_approval": False,
        "allows_protected_body_text": False,
        "allows_protected_body_paths": False,
        "allows_rtm_generation": False,
        "allows_drift_rejection": False,
        "allows_coverage_truth": False,
        "allows_target_source_git_mutation": False,
        "requires_reconciliation_after_each_run": True,
    }


def _validate_182_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-182 package must be a dictionary")
    extra = sorted(set(package) - _KEYS_182_PACKAGE)
    if extra:
        raise ValueError(f"unexpected BLK-182 field {extra[0]!r}")
    missing = sorted(_KEYS_182_PACKAGE - set(package))
    if missing:
        raise ValueError(f"missing BLK-182 field {missing[0]!r}")
    _require(package, "reconciliation_status", RECONCILIATION_STATUS_182)
    _require(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_182)
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_182)
    _require(package, "selected_frontier", SELECTED_FRONTIER_182)
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-182 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-182 reconciliation package hash mismatch")
    if package.get("upstream_export_package_hash") != CANONICAL_BLK181_EXPORT_PACKAGE_HASH:
        raise ValueError("BLK-182 must bind canonical BLK-181 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_182, "BLK-182 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_182, "BLK-182 excluded_authorities")
    if package.get("clean_export_reconciled") is not True:
        raise ValueError("BLK-182 must reconcile cleanly")
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-182 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_182:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-182 package {flag} must remain false")
    return package


def _validate_183_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-183 package must be a dictionary")
    _require(package, "decision_status", DECISION_STATUS_183)
    _require(package, "decision_package_id", DECISION_PACKAGE_ID_183)
    _require(package, "decision_scope", DECISION_SCOPE_183)
    _require(package, "selected_frontier", SELECTED_FRONTIER_183)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_183)
    _required_hash(package.get("decision_package_hash"), "decision_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "decision_package_hash"})
    if package["decision_package_hash"] != computed:
        raise ValueError("decision_package_hash does not match submitted BLK-183 package")
    _require_canonical(package["decision_package_hash"], CANONICAL_BLK183_DECISION_PACKAGE_HASH, "canonical BLK-183 decision package hash mismatch")
    if package.get("upstream_export_reconciliation_package_hash") != CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-183 must bind canonical BLK-182 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_183, "BLK-183 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_183, "BLK-183 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_183:
        expected = flag == "reusable_kernel_path_selected"
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-183 package {flag} must be {expected}")
    return package


def _validate_184_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-184 package must be a dictionary")
    _require(package, "contract_status", CONTRACT_STATUS_184)
    _require(package, "contract_package_id", CONTRACT_PACKAGE_ID_184)
    _require(package, "contract_scope", CONTRACT_SCOPE_184)
    _require(package, "selected_frontier", SELECTED_FRONTIER_184)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_184)
    _required_hash(package.get("contract_package_hash"), "contract_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "contract_package_hash"})
    if package["contract_package_hash"] != computed:
        raise ValueError("contract_package_hash does not match submitted BLK-184 package")
    _require_canonical(package["contract_package_hash"], CANONICAL_BLK184_CONTRACT_PACKAGE_HASH, "canonical BLK-184 contract package hash mismatch")
    if package.get("upstream_decision_package_hash") != CANONICAL_BLK183_DECISION_PACKAGE_HASH:
        raise ValueError("BLK-184 must bind canonical BLK-183 package hash")
    if package.get("contract_hash") != _canonical_hash(package.get("contract")):
        raise ValueError("contract hash mismatch")
    _validate_contract_shape(package.get("contract"))
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_184, "BLK-184 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_184, "BLK-184 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_184:
        expected = flag == "reusable_kernel_contract_emitted"
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-184 package {flag} must be {expected}")
    return package


def _validate_185_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-185 package must be a dictionary")
    _require(package, "dry_run_status", DRY_RUN_STATUS_185)
    _require(package, "dry_run_package_id", DRY_RUN_PACKAGE_ID_185)
    _require(package, "dry_run_scope", DRY_RUN_SCOPE_185)
    _require(package, "selected_frontier", SELECTED_FRONTIER_185)
    _require(package, "approval_id", APPROVAL_ID_185)
    _require(package, "run_id_consumed", RUN_ID_CONSUMED_185)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_185)
    _required_hash(package.get("dry_run_package_hash"), "dry_run_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "dry_run_package_hash"})
    if package["dry_run_package_hash"] != computed:
        raise ValueError("dry_run_package_hash does not match submitted BLK-185 package")
    _require_canonical(package["dry_run_package_hash"], CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH, "canonical BLK-185 dry-run package hash mismatch")
    if package.get("upstream_contract_package_hash") != CANONICAL_BLK184_CONTRACT_PACKAGE_HASH:
        raise ValueError("BLK-185 must bind canonical BLK-184 package hash")
    if package.get("contract_hash") != _canonical_hash(package.get("contract")):
        raise ValueError("dry-run contract hash mismatch")
    _validate_contract_shape(package.get("contract"))
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_185, "BLK-185 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_185, "BLK-185 excluded_authorities")
    true_flags = {"per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated"}
    for flag in SIDE_EFFECT_FLAGS_185:
        expected = flag in true_flags
        if package.get(flag) is not expected:
            raise ValueError(f"BLK-185 package {flag} must be {expected}")
    return package


def _validate_contract_shape(contract: Any) -> None:
    if not isinstance(contract, dict):
        raise ValueError("contract must be a dictionary")
    required = {
        "contract_id", "contract_mode", "beo_id", "beb_id", "exact_trace_identities", "required_per_run_fields",
        "allows_reusable_authority", "allows_live_production_execution_without_exact_approval",
        "allows_protected_body_text", "allows_protected_body_paths", "allows_rtm_generation",
        "allows_drift_rejection", "allows_coverage_truth", "allows_target_source_git_mutation",
        "requires_reconciliation_after_each_run",
    }
    if set(contract) != required:
        raise ValueError("contract must match exact schema")
    _require(contract, "contract_mode", "REUSABLE_MECHANISM_PER_RUN_EXACT_APPROVAL_REQUIRED")
    for key in (
        "allows_reusable_authority", "allows_live_production_execution_without_exact_approval", "allows_protected_body_text",
        "allows_protected_body_paths", "allows_rtm_generation", "allows_drift_rejection", "allows_coverage_truth",
        "allows_target_source_git_mutation",
    ):
        _require_false(contract, key)
    _require_true(contract, "requires_reconciliation_after_each_run")
    required_fields = ["exact_approval_id", "exact_run_id", "operator_identity", "operator_decision_text_raw", "upstream_contract_package_hash", "contract_hash", "requested_at", "expires_at"]
    if contract.get("required_per_run_fields") != required_fields:
        raise ValueError("contract required_per_run_fields must be exact")


def _validate_dry_run_window(decided_at: str, requested_at: str, expires_at: str, contract_emitted_at: str) -> None:
    decided = _parse_not_stale(decided_at, "decision execution request")
    requested = _parse_not_stale(requested_at, "requested_at")
    expires = _parse_not_stale(expires_at, "expires_at")
    emitted = _parse_not_stale(contract_emitted_at, "contract emitted_at")
    if decided < emitted:
        raise ValueError("decision must not predate contract emission")
    if requested < decided or expires <= requested:
        raise ValueError("approval request must be within approval decision window")


def _require_canonical(observed: str, canonical: str, message: str) -> None:
    placeholder = canonical.endswith("0000000000000183") or canonical.endswith("0000000000000184") or canonical.endswith("0000000000000185") or canonical.endswith("0000000000000186")
    if not placeholder and observed != canonical:
        raise ValueError(message)
