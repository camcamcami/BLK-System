"""BLK-SYSTEM-190..194 repeatable trusted blk-link ladder.

This deterministic fixture consumes the clean BLK-SYSTEM-189 single production
`blk-link` wrapper reconciliation and turns it into a repeatable trusted
per-run mechanism: post-run review (190), repeatable contract (191),
caller-supplied trust ledger (192), three exact repeat-run evidence samples
(193), and clean reconciliation (194).

The mechanism is repeatable and trusted only inside the hash-bound contract:
each run still needs exact approval text, a unique run ID, nonce binding, and a
caller-supplied ledger state. It does not grant blanket/unbounded production
`blk-link`, reusable RTM generation, drift rejection, coverage truth,
protected-body access, target/source/Git mutation, BLK-pipe/BLK-test/Codex
runtime, package/network/model/browser/cyber tooling, or production-isolation
claims.
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
    _validate_trace_copy,
)
from metadata_bound_rtm_trace_closure_approval_capture import _required_exact_set, _required_hash
from protected_body_verification_decision_engine_175 import _scan_high_risk_freeform
from single_production_blk_link_wrapper_run_187_189 import (
    CANONICAL_BLK188_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_189,
    EXACT_PROOF_OBLIGATIONS_189,
    RECONCILIATION_PACKAGE_ID_189,
    RECONCILIATION_SCOPE_189,
    RECONCILIATION_STATUS_189,
    SELECTED_FRONTIER_189,
    SIDE_EFFECT_FLAGS_189,
)

REVIEW_STATUS_190 = "REPEATABLE_TRUSTED_BLK_LINK_POST_RUN_REVIEW_CLEAN"
REVIEW_PACKAGE_ID_190 = "REPEATABLE-TRUSTED-BLK-LINK-POST-RUN-REVIEW-190-001"
REVIEW_SCOPE_190 = "POST_SINGLE_RUN_OPERATOR_REVIEW_SELECT_REPEATABLE_TRUSTED_PATH_NOT_BLANKET_AUTHORITY"
SELECTED_FRONTIER_190 = "repeatable_trusted_blk_link_post_run_review_190"
NEXT_REQUIRED_AUTHORITY_190 = "REPEATABLE_TRUSTED_CONTRACT_REQUIRED_NOT_RUNTIME_AUTHORITY"
CANONICAL_BLK190_REVIEW_PACKAGE_HASH = "sha256:14dd668a8848351ebfcc05ee0bfa58ea979a6c6a861bc9b9449d86f980dc665e"

CONTRACT_STATUS_191 = "REPEATABLE_TRUSTED_BLK_LINK_CONTRACT_EMITTED"
CONTRACT_PACKAGE_ID_191 = "REPEATABLE-TRUSTED-BLK-LINK-CONTRACT-191-001"
CONTRACT_SCOPE_191 = "REPEATABLE_TRUSTED_MECHANISM_PER_RUN_EXACT_APPROVAL_AND_LEDGER_REQUIRED"
SELECTED_FRONTIER_191 = "repeatable_trusted_blk_link_contract_191"
NEXT_REQUIRED_AUTHORITY_191 = "CALLER_SUPPLIED_TRUST_LEDGER_REQUIRED_NOT_GLOBAL_REPLAY_AUTHORITY"
CANONICAL_BLK191_CONTRACT_PACKAGE_HASH = "sha256:c6d056a59f6ef0b182223c6bcac6737466a40d049cbdc8e844219fab2c7150f5"

LEDGER_STATUS_192 = "REPEATABLE_TRUSTED_BLK_LINK_CALLER_SUPPLIED_LEDGER_READY"
LEDGER_PACKAGE_ID_192 = "REPEATABLE-TRUSTED-BLK-LINK-LEDGER-192-001"
LEDGER_SCOPE_192 = "CALLER_SUPPLIED_HASH_CHAIN_LEDGER_NO_FILESYSTEM_WRITE_NO_GLOBAL_REPLAY_CLAIM"
SELECTED_FRONTIER_192 = "repeatable_trusted_blk_link_ledger_192"
NEXT_REQUIRED_AUTHORITY_192 = "THREE_EXACT_REPEAT_RUNS_REQUIRED_FOR_TRUST_SAMPLE"
CANONICAL_BLK192_LEDGER_PACKAGE_HASH = "sha256:ddff687aa4b4a67f218bb317fab47c7380b542ac538d3daf8794567f00b23140"

REPEAT_RUN_STATUS_193 = "REPEATABLE_TRUSTED_BLK_LINK_REPEAT_RUNS_RECORDED_CLEAN"
REPEAT_RUN_PACKAGE_ID_193 = "REPEATABLE-TRUSTED-BLK-LINK-REPEAT-RUNS-193-001"
REPEAT_RUN_SCOPE_193 = "THREE_EXACT_APPROVED_REPEATABLE_PRODUCTION_WRAPPER_RUNS_LEDGER_CHAINED"
SELECTED_FRONTIER_193 = "repeatable_trusted_blk_link_repeat_runs_193"
NEXT_REQUIRED_AUTHORITY_193 = "POST_REPEATABILITY_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK193_REPEAT_RUNS_PACKAGE_HASH = "sha256:318eec761911be1767b915207d86449879132545d061bbf758d6662ac2f4297e"

RECONCILIATION_STATUS_194 = "REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN_OPERATOR_USE_READY"
RECONCILIATION_PACKAGE_ID_194 = "REPEATABLE-TRUSTED-BLK-LINK-RECONCILIATION-194-001"
RECONCILIATION_SCOPE_194 = "REPEATABLE_TRUSTED_BLK_LINK_RECONCILIATION_PER_RUN_EXACT_APPROVAL_ONLY"
SELECTED_FRONTIER_194 = "repeatable_trusted_blk_link_reconciliation_194"
REPEATABLE_TRUSTED_BLK_LINK_NEXT_FRONTIER_194 = "NEXT_FRONTIER_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL_NOT_BLANKET_AUTHORITY"
CANONICAL_BLK194_RECONCILIATION_PACKAGE_HASH = "sha256:30292f85d1222eb2108f0eadeec07337834e9b47d8e00fa9969aeeafb1bbf4f7"

_BASE_EXCLUDED = {
    "BLANKET_OR_UNBOUNDED_PRODUCTION_BLK_LINK_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION_WITHOUT_PER_RUN_EXACT_APPROVAL",
    "RUN_ID_REUSE_OR_GLOBAL_REPLAY_LEDGER_CLAIM",
    "APPROVAL_REUSE_ACROSS_RUNS",
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
EXACT_EXCLUDED_AUTHORITIES_190 = _BASE_EXCLUDED | {
    "CONTRACT_EMISSION_THIS_SPRINT",
    "LEDGER_INITIALIZATION_THIS_SPRINT",
    "REPEAT_RUN_EXECUTION_THIS_SPRINT",
    "AUTHORITY_GRANTED_BY_POST_RUN_REVIEW",
}
EXACT_EXCLUDED_AUTHORITIES_191 = _BASE_EXCLUDED | {
    "LEDGER_INITIALIZATION_THIS_SPRINT",
    "REPEAT_RUN_EXECUTION_THIS_SPRINT",
    "CONTRACT_IS_NOT_BLANKET_AUTHORITY",
}
EXACT_EXCLUDED_AUTHORITIES_192 = _BASE_EXCLUDED | {
    "REPEAT_RUN_EXECUTION_THIS_SPRINT",
    "FILESYSTEM_LEDGER_WRITE",
    "GLOBAL_REPLAY_PREVENTION_CLAIM",
}
EXACT_EXCLUDED_AUTHORITIES_193 = _BASE_EXCLUDED | {
    "FUTURE_RUNS_WITHOUT_FRESH_EXACT_APPROVAL",
    "GLOBAL_REPLAY_PREVENTION_CLAIM_AFTER_SAMPLE",
    "POST_RUN_RECONCILIATION_THIS_SPRINT",
}
EXACT_EXCLUDED_AUTHORITIES_194 = _BASE_EXCLUDED | {
    "NEXT_FRONTIER_AUTHORITY_GRANT",
    "TRUSTED_MECHANISM_IS_NOT_BLANKET_AUTHORITY",
    "GLOBAL_REPLAY_PREVENTION_CLAIM_AFTER_RECONCILIATION",
}

EXACT_PROOF_OBLIGATIONS_190 = {
    "BLK189_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "SINGLE_PRODUCTION_WRAPPER_RUN_REVIEWED_CLEAN",
    "REPEATABLE_TRUSTED_PATH_SELECTED_BY_OPERATOR_REQUEST",
    "BLANKET_PRODUCTION_BLK_LINK_AUTHORITY_EXCLUDED",
    "PER_RUN_EXACT_APPROVAL_AND_UNIQUE_RUN_ID_STILL_REQUIRED",
    "RTM_DRIFT_COVERAGE_PROTECTED_BODY_MUTATION_TOOLING_EXCLUDED",
}
EXACT_PROOF_OBLIGATIONS_191 = {
    "BLK190_REVIEW_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "REPEATABLE_CONTRACT_SCHEMA_EMITTED",
    "CONTRACT_REQUIRES_EXACT_APPROVAL_ID_RUN_ID_NONCE_AND_LEDGER_PREVIOUS_HASH_PER_RUN",
    "CONTRACT_REQUIRES_CANONICAL_UPSTREAM_HASH_BINDING",
    "CONTRACT_REQUIRES_TRUST_RULES_FOR_UNIQUE_RUN_IDS_AND_HASH_CHAIN",
    "CONTRACT_FORBIDS_BLANKET_AUTHORITY_AND_PROTECTED_BODY_TEXT",
    "CONTRACT_FORBIDS_TARGET_SOURCE_GIT_MUTATION_AND_RUNTIME_TOOLING",
}
EXACT_PROOF_OBLIGATIONS_192 = {
    "BLK191_CONTRACT_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "CALLER_SUPPLIED_HASH_CHAIN_LEDGER_INITIALIZED",
    "LEDGER_GENESIS_HASH_BOUND_TO_CONTRACT_AND_UPSTREAM_REVIEW",
    "NO_FILESYSTEM_LEDGER_WRITE_OR_GLOBAL_REPLAY_CLAIM",
    "REPEAT_RUNS_NOT_EXECUTED_BY_LEDGER_INITIALIZATION",
}
EXACT_PROOF_OBLIGATIONS_193 = {
    "BLK192_LEDGER_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "THREE_EXACT_APPROVED_REPEAT_RUN_REQUESTS_VALIDATED",
    "EACH_RUN_HAS_UNIQUE_APPROVAL_ID_RUN_ID_AND_NONCE",
    "EACH_RUN_BINDS_LEDGER_PREVIOUS_HASH_AND_CANONICAL_UPSTREAM_HASH",
    "CALLER_SUPPLIED_LEDGER_CHAIN_ADVANCED_DETERMINISTICALLY",
    "TRUSTED_REPEATABILITY_SAMPLE_RECORDED_WITHOUT_ADJACENT_AUTHORITY",
}
EXACT_PROOF_OBLIGATIONS_194 = {
    "BLK193_REPEAT_RUNS_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "THREE_OF_THREE_REPEAT_RUNS_RECONCILED_CLEAN",
    "REPEATABLE_TRUSTED_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL_ONLY",
    "BLANKET_AUTHORITY_AND_GLOBAL_REPLAY_CLAIMS_EXCLUDED",
    "RTM_DRIFT_COVERAGE_PROTECTED_BODY_MUTATION_TOOLING_EXCLUDED",
}

_COMMON_FALSE_FLAGS = (
    "blanket_production_blk_link_authority_granted",
    "production_blk_link_execution_without_per_run_approval",
    "reusable_run_id_authority_granted",
    "global_replay_ledger_claimed",
    "filesystem_ledger_written",
    "protected_body_text_included",
    "protected_body_content_returned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted_by_fixture",
    "protected_body_scan_attempted",
    "active_vault_filesystem_read_performed",
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
SIDE_EFFECT_FLAGS_190 = ("single_run_reviewed_clean", "repeatable_trusted_path_selected", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_191 = ("repeatable_trusted_contract_emitted", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_192 = ("caller_supplied_trust_ledger_initialized", *_COMMON_FALSE_FLAGS)
SIDE_EFFECT_FLAGS_193 = (
    "per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed",
    "caller_supplied_ledger_advanced", *_COMMON_FALSE_FLAGS,
)
SIDE_EFFECT_FLAGS_194 = ("repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established", "next_frontier_granted", *_COMMON_FALSE_FLAGS)

_ATTESTATION_190 = frozenset({
    "exact_blk189_reconciliation_reviewed", "single_run_clean_without_observed_failure",
    "repeatable_trusted_path_selected", "per_run_exact_approval_required",
    "blanket_authority_excluded", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "target_source_git_mutation_excluded",
    "runtime_tooling_excluded",
})
_ATTESTATION_191 = frozenset({
    "exact_blk190_review_bound", "repeatable_contract_emitted", "per_run_exact_approval_required",
    "unique_run_id_required", "ledger_previous_hash_required", "canonical_upstream_hash_required",
    "blanket_authority_excluded", "protected_body_reads_excluded", "runtime_tooling_excluded",
})
_ATTESTATION_192 = frozenset({
    "exact_blk191_contract_bound", "caller_supplied_ledger_initialized",
    "genesis_hash_bound_to_contract", "filesystem_ledger_not_written", "global_replay_claim_excluded",
    "repeat_runs_not_executed", "protected_body_reads_excluded", "runtime_tooling_excluded",
})
_ATTESTATION_193 = frozenset({
    "exact_blk192_ledger_bound", "three_exact_approvals_captured", "three_unique_run_ids_consumed",
    "three_unique_nonces_bound", "ledger_hash_chain_advanced", "repeatability_sample_clean",
    "blanket_authority_excluded", "protected_body_reads_excluded", "rtm_generation_excluded",
    "drift_rejection_excluded", "coverage_truth_excluded", "target_source_git_mutation_excluded",
})
_ATTESTATION_194 = frozenset({
    "exact_blk193_repeat_runs_bound", "three_of_three_runs_clean", "repeatable_trusted_mechanism_established",
    "per_run_exact_approval_remains_required", "blanket_authority_excluded", "global_replay_claim_excluded",
    "protected_body_reads_excluded", "rtm_generation_excluded", "drift_rejection_excluded",
    "coverage_truth_excluded", "target_source_git_mutation_excluded", "runtime_tooling_excluded",
})

_KEYS_190 = frozenset({
    "review_package_id", "operator_identity", "review_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash", "upstream_execution_package_hash",
    "run_id_consumed", "wrapper_run_result_observed", "beo_id", "beb_id", "exact_trace_identities",
    "reviewed_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations",
    "excluded_authorities", *SIDE_EFFECT_FLAGS_190,
})
_KEYS_191 = frozenset({
    "contract_package_id", "operator_identity", "contract_scope", "selected_frontier",
    "upstream_review_package_id", "upstream_review_package_hash", "beo_id", "beb_id", "exact_trace_identities",
    "contract", "contract_notes", "emitted_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_191,
})
_KEYS_192 = frozenset({
    "ledger_package_id", "operator_identity", "ledger_scope", "selected_frontier",
    "upstream_contract_package_id", "upstream_contract_package_hash", "contract_hash", "beo_id", "beb_id",
    "exact_trace_identities", "ledger", "ledger_notes", "initialized_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_192,
})
_KEYS_193 = frozenset({
    "repeat_runs_package_id", "operator_identity", "repeat_run_scope", "selected_frontier",
    "upstream_ledger_package_id", "upstream_ledger_package_hash", "upstream_contract_package_hash",
    "contract_hash", "beo_id", "beb_id", "exact_trace_identities", "repeat_run_requests",
    "runtime_notes", "requested_at", "expires_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_193,
})
_KEYS_194 = frozenset({
    "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_repeat_runs_package_id", "upstream_repeat_runs_package_hash", "repeat_run_count",
    "trusted_repeatability_result", "final_ledger_hash", "beo_id", "beb_id", "exact_trace_identities",
    "observed_failure_requires_hardening", "reconciled_at", "expired", "replayed", "stale",
    "operator_attestation", "proof_obligations", "excluded_authorities", *SIDE_EFFECT_FLAGS_194,
})
_KEYS_189_PACKAGE = frozenset({
    "reconciliation_status", "reconciliation_package_id", "operator_identity", "reconciliation_scope", "selected_frontier",
    "upstream_execution_package_id", "upstream_execution_package_hash", "run_id_consumed", "wrapper_run_result",
    "beo_id", "beb_id", "exact_trace_identities", "clean_single_production_wrapper_run_reconciled",
    "observed_failure_requires_hardening", "recommended_next_frontier", "next_frontier_granted",
    "reconciliation_context_hash", "reconciled_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", "reconciliation_package_hash", *SIDE_EFFECT_FLAGS_189,
})


def valid_repeatable_trusted_blk_link_post_run_review_190(reconciliation189: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "review_package_id": REVIEW_PACKAGE_ID_190,
        "operator_identity": reconciliation189["operator_identity"],
        "review_scope": REVIEW_SCOPE_190,
        "selected_frontier": SELECTED_FRONTIER_190,
        "upstream_reconciliation_package_id": reconciliation189["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation189["reconciliation_package_hash"],
        "upstream_execution_package_hash": reconciliation189["upstream_execution_package_hash"],
        "run_id_consumed": reconciliation189["run_id_consumed"],
        "wrapper_run_result_observed": reconciliation189["wrapper_run_result"],
        "beo_id": reconciliation189["beo_id"],
        "beb_id": reconciliation189["beb_id"],
        "exact_trace_identities": list(reconciliation189["exact_trace_identities"]),
        "reviewed_at": "2099-05-17T00:40:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_190},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_190),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_190),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_190, {"single_run_reviewed_clean", "repeatable_trusted_path_selected"})
    record.update(overrides)
    return record


def build_repeatable_trusted_blk_link_post_run_review_190(reconciliation189_package: dict[str, Any], review190: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_189_package(reconciliation189_package)
    review = _validate_record(review190, _KEYS_190, _ATTESTATION_190, EXACT_PROOF_OBLIGATIONS_190, EXACT_EXCLUDED_AUTHORITIES_190, SIDE_EFFECT_FLAGS_190, {"single_run_reviewed_clean", "repeatable_trusted_path_selected"})
    _require(review, "review_package_id", REVIEW_PACKAGE_ID_190)
    _require(review, "review_scope", REVIEW_SCOPE_190)
    _require(review, "selected_frontier", SELECTED_FRONTIER_190)
    _require_matching_upstream(review, upstream, (
        ("upstream_reconciliation_package_id", "reconciliation_package_id"),
        ("upstream_reconciliation_package_hash", "reconciliation_package_hash"),
        ("upstream_execution_package_hash", "upstream_execution_package_hash"),
        ("run_id_consumed", "run_id_consumed"), ("wrapper_run_result_observed", "wrapper_run_result"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(review["reviewed_at"], "reviewed_at")
    trace_ids = _validate_trace_copy(review["exact_trace_identities"], upstream["exact_trace_identities"])
    package = {
        "review_status": REVIEW_STATUS_190,
        "review_package_id": REVIEW_PACKAGE_ID_190,
        "operator_identity": review["operator_identity"],
        "review_scope": REVIEW_SCOPE_190,
        "selected_frontier": SELECTED_FRONTIER_190,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "run_id_consumed": upstream["run_id_consumed"],
        "wrapper_run_result": upstream["wrapper_run_result"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_ids,
        "single_run_reviewed_clean": True,
        "repeatable_trusted_path_selected": True,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_190,
        "review_context_hash": _canonical_hash(review),
        "reviewed_at": review["reviewed_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(review["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_190),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_190),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_190, {"single_run_reviewed_clean", "repeatable_trusted_path_selected"})
    package["review_package_hash"] = _canonical_hash(package)
    return package


def valid_repeatable_trusted_blk_link_contract_191(review190: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    contract = _contract_body(review190)
    record = {
        "contract_package_id": CONTRACT_PACKAGE_ID_191,
        "operator_identity": review190["operator_identity"],
        "contract_scope": CONTRACT_SCOPE_191,
        "selected_frontier": SELECTED_FRONTIER_191,
        "upstream_review_package_id": review190["review_package_id"],
        "upstream_review_package_hash": review190["review_package_hash"],
        "beo_id": review190["beo_id"],
        "beb_id": review190["beb_id"],
        "exact_trace_identities": list(review190["exact_trace_identities"]),
        "contract": contract,
        "contract_notes": "Repeatable trusted blk-link requires exact approval, unique run ID, nonce, and caller-supplied ledger state per run; no protected body, RTM, drift, coverage, tooling, or mutation authority is added.",
        "emitted_at": "2099-05-17T00:50:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_191},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_191),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_191),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_191, {"repeatable_trusted_contract_emitted"})
    record.update(overrides)
    return record


def build_repeatable_trusted_blk_link_contract_191(review190_package: dict[str, Any], contract191: dict[str, Any]) -> dict[str, Any]:
    review = _validate_190_package(review190_package)
    record = _validate_record(contract191, _KEYS_191, _ATTESTATION_191, EXACT_PROOF_OBLIGATIONS_191, EXACT_EXCLUDED_AUTHORITIES_191, SIDE_EFFECT_FLAGS_191, {"repeatable_trusted_contract_emitted"})
    _scan_high_risk_freeform(record["contract_notes"], "contract_notes")
    _require(record, "contract_package_id", CONTRACT_PACKAGE_ID_191)
    _require(record, "contract_scope", CONTRACT_SCOPE_191)
    _require(record, "selected_frontier", SELECTED_FRONTIER_191)
    _validate_contract(record["contract"], review)
    _require_matching_upstream(record, review, (
        ("upstream_review_package_id", "review_package_id"), ("upstream_review_package_hash", "review_package_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _parse_not_stale(record["emitted_at"], "emitted_at")
    trace_ids = _validate_trace_copy(record["exact_trace_identities"], review["exact_trace_identities"])
    contract = deepcopy(record["contract"])
    package = {
        "contract_status": CONTRACT_STATUS_191,
        "contract_package_id": CONTRACT_PACKAGE_ID_191,
        "operator_identity": record["operator_identity"],
        "contract_scope": CONTRACT_SCOPE_191,
        "selected_frontier": SELECTED_FRONTIER_191,
        "upstream_review_package_id": review["review_package_id"],
        "upstream_review_package_hash": review["review_package_hash"],
        "beo_id": review["beo_id"],
        "beb_id": review["beb_id"],
        "exact_trace_identities": trace_ids,
        "repeatable_trusted_contract_emitted": True,
        "contract": contract,
        "contract_hash": _canonical_hash(contract),
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_191,
        "contract_request_hash": _canonical_hash(record),
        "emitted_at": record["emitted_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(record["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_191),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_191),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_191, {"repeatable_trusted_contract_emitted"})
    package["contract_package_hash"] = _canonical_hash(package)
    return package


def valid_repeatable_trusted_blk_link_ledger_192(contract191: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    genesis = _canonical_hash({
        "ledger_package_id": LEDGER_PACKAGE_ID_192,
        "upstream_contract_package_hash": contract191["contract_package_hash"],
        "contract_hash": contract191["contract_hash"],
        "operator_identity": contract191["operator_identity"],
        "ledger_scope": LEDGER_SCOPE_192,
    })
    record = {
        "ledger_package_id": LEDGER_PACKAGE_ID_192,
        "operator_identity": contract191["operator_identity"],
        "ledger_scope": LEDGER_SCOPE_192,
        "selected_frontier": SELECTED_FRONTIER_192,
        "upstream_contract_package_id": contract191["contract_package_id"],
        "upstream_contract_package_hash": contract191["contract_package_hash"],
        "contract_hash": contract191["contract_hash"],
        "beo_id": contract191["beo_id"],
        "beb_id": contract191["beb_id"],
        "exact_trace_identities": list(contract191["exact_trace_identities"]),
        "ledger": {
            "ledger_mode": "CALLER_SUPPLIED_HASH_CHAIN_NO_FILESYSTEM_WRITE",
            "genesis_ledger_hash": genesis,
            "current_ledger_hash": genesis,
            "used_run_ids": [],
            "used_approval_ids": [],
            "used_nonces": [],
            "ledger_entries": [],
        },
        "ledger_notes": "Caller-supplied ledger state is evidence for this fixture only; no filesystem ledger write or global replay prevention is claimed.",
        "initialized_at": "2099-05-17T01:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_192},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_192),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_192),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_192, {"caller_supplied_trust_ledger_initialized"})
    record.update(overrides)
    return record


def build_repeatable_trusted_blk_link_ledger_192(contract191_package: dict[str, Any], ledger192: dict[str, Any]) -> dict[str, Any]:
    contract = _validate_191_package(contract191_package)
    record = _validate_record(ledger192, _KEYS_192, _ATTESTATION_192, EXACT_PROOF_OBLIGATIONS_192, EXACT_EXCLUDED_AUTHORITIES_192, SIDE_EFFECT_FLAGS_192, {"caller_supplied_trust_ledger_initialized"})
    _scan_high_risk_freeform(record["ledger_notes"], "ledger_notes")
    _require(record, "ledger_package_id", LEDGER_PACKAGE_ID_192)
    _require(record, "ledger_scope", LEDGER_SCOPE_192)
    _require(record, "selected_frontier", SELECTED_FRONTIER_192)
    _require_matching_upstream(record, contract, (
        ("upstream_contract_package_id", "contract_package_id"), ("upstream_contract_package_hash", "contract_package_hash"),
        ("contract_hash", "contract_hash"), ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    ledger = _validate_genesis_ledger(record["ledger"], contract)
    _parse_not_stale(record["initialized_at"], "initialized_at")
    trace_ids = _validate_trace_copy(record["exact_trace_identities"], contract["exact_trace_identities"])
    package = {
        "ledger_status": LEDGER_STATUS_192,
        "ledger_package_id": LEDGER_PACKAGE_ID_192,
        "operator_identity": record["operator_identity"],
        "ledger_scope": LEDGER_SCOPE_192,
        "selected_frontier": SELECTED_FRONTIER_192,
        "upstream_contract_package_id": contract["contract_package_id"],
        "upstream_contract_package_hash": contract["contract_package_hash"],
        "contract_hash": contract["contract_hash"],
        "beo_id": contract["beo_id"],
        "beb_id": contract["beb_id"],
        "exact_trace_identities": trace_ids,
        "caller_supplied_trust_ledger_initialized": True,
        "ledger": ledger,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_192,
        "ledger_request_hash": _canonical_hash(record),
        "initialized_at": record["initialized_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(record["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_192),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_192),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_192, {"caller_supplied_trust_ledger_initialized"})
    package["ledger_package_hash"] = _canonical_hash(package)
    return package


def valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192: dict[str, Any], requested_at_start: str = "2099-05-17T01:10:00+10:00", **overrides: Any) -> dict[str, Any]:
    requests = _default_repeat_run_requests(ledger192, requested_at_start)
    record = {
        "repeat_runs_package_id": REPEAT_RUN_PACKAGE_ID_193,
        "operator_identity": ledger192["operator_identity"],
        "repeat_run_scope": REPEAT_RUN_SCOPE_193,
        "selected_frontier": SELECTED_FRONTIER_193,
        "upstream_ledger_package_id": ledger192["ledger_package_id"],
        "upstream_ledger_package_hash": ledger192["ledger_package_hash"],
        "upstream_contract_package_hash": ledger192["upstream_contract_package_hash"],
        "contract_hash": ledger192["contract_hash"],
        "beo_id": ledger192["beo_id"],
        "beb_id": ledger192["beb_id"],
        "exact_trace_identities": list(ledger192["exact_trace_identities"]),
        "repeat_run_requests": requests,
        "runtime_notes": "Three exact repeatable blk-link wrapper runs are represented with per-run approval, unique run IDs, nonce binding, and caller-supplied ledger chaining; no RTM, drift, coverage, protected body, tooling, or mutation authority is added.",
        "requested_at": requests[0]["requested_at"],
        "expires_at": requests[-1]["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_193},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_193),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_193),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_193, {"per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed", "caller_supplied_ledger_advanced"})
    record.update(overrides)
    return record


def build_repeatable_trusted_blk_link_repeat_runs_193(ledger192_package: dict[str, Any], repeat193: dict[str, Any]) -> dict[str, Any]:
    ledger_package = _validate_192_package(ledger192_package)
    record = _validate_record(repeat193, _KEYS_193, _ATTESTATION_193, EXACT_PROOF_OBLIGATIONS_193, EXACT_EXCLUDED_AUTHORITIES_193, SIDE_EFFECT_FLAGS_193, {"per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed", "caller_supplied_ledger_advanced"})
    _scan_high_risk_freeform(record["runtime_notes"], "runtime_notes")
    _require(record, "repeat_runs_package_id", REPEAT_RUN_PACKAGE_ID_193)
    _require(record, "repeat_run_scope", REPEAT_RUN_SCOPE_193)
    _require(record, "selected_frontier", SELECTED_FRONTIER_193)
    _require_matching_upstream(record, ledger_package, (
        ("upstream_ledger_package_id", "ledger_package_id"), ("upstream_ledger_package_hash", "ledger_package_hash"),
        ("upstream_contract_package_hash", "upstream_contract_package_hash"), ("contract_hash", "contract_hash"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    _validate_trace_copy(record["exact_trace_identities"], ledger_package["exact_trace_identities"])
    run_evidence, final_ledger = _build_run_evidence(ledger_package, record["repeat_run_requests"])
    package = {
        "repeat_run_status": REPEAT_RUN_STATUS_193,
        "repeat_runs_package_id": REPEAT_RUN_PACKAGE_ID_193,
        "operator_identity": record["operator_identity"],
        "repeat_run_scope": REPEAT_RUN_SCOPE_193,
        "selected_frontier": SELECTED_FRONTIER_193,
        "upstream_ledger_package_id": ledger_package["ledger_package_id"],
        "upstream_ledger_package_hash": ledger_package["ledger_package_hash"],
        "upstream_contract_package_hash": ledger_package["upstream_contract_package_hash"],
        "contract_hash": ledger_package["contract_hash"],
        "beo_id": ledger_package["beo_id"],
        "beb_id": ledger_package["beb_id"],
        "exact_trace_identities": list(ledger_package["exact_trace_identities"]),
        "repeatable_trusted_runs_executed": True,
        "repeat_run_count": len(run_evidence),
        "trusted_repeatability_result": "TRUSTED_REPEATABILITY_SAMPLE_3_OF_3_CLEAN",
        "run_evidence": run_evidence,
        "ledger": final_ledger,
        "repeat_runs_request_hash": _canonical_hash(record),
        "requested_at": record["requested_at"],
        "expires_at": record["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_193,
        "operator_attestation": deepcopy(record["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_193),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_193),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_193, {"per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed", "caller_supplied_ledger_advanced"})
    package["repeat_runs_package_hash"] = _canonical_hash(package)
    return package


def valid_repeatable_trusted_blk_link_reconciliation_194(repeat193: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_194,
        "operator_identity": repeat193["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_194,
        "selected_frontier": SELECTED_FRONTIER_194,
        "upstream_repeat_runs_package_id": repeat193["repeat_runs_package_id"],
        "upstream_repeat_runs_package_hash": repeat193["repeat_runs_package_hash"],
        "repeat_run_count": repeat193["repeat_run_count"],
        "trusted_repeatability_result": repeat193["trusted_repeatability_result"],
        "final_ledger_hash": repeat193["ledger"]["current_ledger_hash"],
        "beo_id": repeat193["beo_id"],
        "beb_id": repeat193["beb_id"],
        "exact_trace_identities": list(repeat193["exact_trace_identities"]),
        "observed_failure_requires_hardening": False,
        "reconciled_at": "2099-05-17T02:10:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_194},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_194),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_194),
    }
    _set_flags(record, SIDE_EFFECT_FLAGS_194, {"repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established"})
    record.update(overrides)
    return record


def build_repeatable_trusted_blk_link_reconciliation_194(repeat193_package: dict[str, Any], context194: dict[str, Any]) -> dict[str, Any]:
    repeat = _validate_193_package(repeat193_package)
    context = _validate_record(context194, _KEYS_194, _ATTESTATION_194, EXACT_PROOF_OBLIGATIONS_194, EXACT_EXCLUDED_AUTHORITIES_194, SIDE_EFFECT_FLAGS_194, {"repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established"})
    _require(context, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_194)
    _require(context, "reconciliation_scope", RECONCILIATION_SCOPE_194)
    _require(context, "selected_frontier", SELECTED_FRONTIER_194)
    _require_false(context, "observed_failure_requires_hardening")
    _require_matching_upstream(context, repeat, (
        ("upstream_repeat_runs_package_id", "repeat_runs_package_id"), ("upstream_repeat_runs_package_hash", "repeat_runs_package_hash"),
        ("repeat_run_count", "repeat_run_count"), ("trusted_repeatability_result", "trusted_repeatability_result"),
        ("operator_identity", "operator_identity"), ("beo_id", "beo_id"), ("beb_id", "beb_id"),
    ))
    if context["final_ledger_hash"] != repeat["ledger"]["current_ledger_hash"]:
        raise ValueError("final_ledger_hash must match BLK-193 ledger current hash")
    _parse_not_stale(context["reconciled_at"], "reconciled_at")
    trace_ids = _validate_trace_copy(context["exact_trace_identities"], repeat["exact_trace_identities"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_194,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_194,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_194,
        "selected_frontier": SELECTED_FRONTIER_194,
        "upstream_repeat_runs_package_id": repeat["repeat_runs_package_id"],
        "upstream_repeat_runs_package_hash": repeat["repeat_runs_package_hash"],
        "repeat_run_count": repeat["repeat_run_count"],
        "trusted_repeatability_result": repeat["trusted_repeatability_result"],
        "trusted_repeatability_score": "3/3",
        "final_ledger_hash": repeat["ledger"]["current_ledger_hash"],
        "beo_id": repeat["beo_id"],
        "beb_id": repeat["beb_id"],
        "exact_trace_identities": trace_ids,
        "repeatable_trusted_blk_link_reconciled_clean": True,
        "trusted_repeatable_mechanism_established": True,
        "observed_failure_requires_hardening": False,
        "recommended_next_frontier": REPEATABLE_TRUSTED_BLK_LINK_NEXT_FRONTIER_194,
        "next_frontier_granted": False,
        "reconciliation_context_hash": _canonical_hash(context),
        "reconciled_at": context["reconciled_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_194),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_194),
    }
    _set_flags(package, SIDE_EFFECT_FLAGS_194, {"repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established"})
    package["reconciliation_package_hash"] = _canonical_hash(package)
    return package


def _contract_body(review190: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_PACKAGE_ID_191,
        "contract_mode": "REPEATABLE_TRUSTED_BLK_LINK_PER_RUN_EXACT_APPROVAL",
        "upstream_review_package_hash": review190["review_package_hash"],
        "allows_repeatable_runs_with_exact_approval": True,
        "allows_blanket_authority": False,
        "allows_protected_body_text": False,
        "allows_target_source_git_mutation": False,
        "allows_rtm_generation": False,
        "required_per_run_fields": [
            "exact_approval_id", "exact_run_id", "exact_operator_decision_text", "nonce",
            "ledger_previous_hash", "canonical_upstream_hash", "requested_at", "expires_at",
        ],
        "trust_rules": [
            "unique_approval_id_not_previously_consumed",
            "unique_run_id_not_previously_consumed",
            "unique_nonce_not_previously_seen",
            "canonical_upstream_hash_binding",
            "ledger_previous_hash_must_equal_current_ledger_hash",
            "entry_hash_chains_to_previous_hash",
            "no_protected_body_text_or_path",
            "no_target_source_git_mutation",
        ],
    }


def _default_repeat_run_requests(ledger192: dict[str, Any], requested_at_start: str) -> list[dict[str, Any]]:
    if requested_at_start.startswith("2099-05-17T01:30"):
        times = [("01:30", "01:31", "01:36"), ("01:40", "01:41", "01:46"), ("01:50", "01:51", "01:56")]
    else:
        times = [("01:10", "01:11", "01:16"), ("01:20", "01:21", "01:26"), ("01:30", "01:31", "01:36")]
    requests = []
    previous_hash = ledger192["ledger"]["current_ledger_hash"]
    for index, (decided, requested, expires) in enumerate(times, start=1):
        run_id = f"RUN-BLK-SYSTEM-193-REPEATABLE-TRUSTED-BLK-LINK-{index:03d}"
        approval_id = f"APPROVAL-BLK-SYSTEM-193-REPEATABLE-TRUSTED-BLK-LINK-{index:03d}"
        nonce = f"NONCE-BLK-SYSTEM-193-REPEATABLE-TRUSTED-BLK-LINK-{index:03d}"
        request = {
            "approval_id": approval_id,
            "run_id_to_consume": run_id,
            "nonce": nonce,
            "operator_decision_text_raw": _operator_text(approval_id, run_id, nonce),
            "ledger_previous_hash": previous_hash,
            "canonical_upstream_hash": ledger192["ledger_package_hash"],
            "decided_at": f"2099-05-17T{decided}:00+10:00",
            "requested_at": f"2099-05-17T{requested}:00+10:00",
            "expires_at": f"2099-05-17T{expires}:00+10:00",
            "operator_attestation": {key: True for key in _ATTESTATION_193},
        }
        requests.append(request)
        entry = _run_evidence_entry(index, request, previous_hash)
        previous_hash = _canonical_hash(entry)
    return requests


def _operator_text(approval_id: str, run_id: str, nonce: str) -> str:
    return (
        f"APPROVE REPEATABLE-TRUSTED-BLK-LINK RUN {run_id} WITH {approval_id} AND {nonce}; "
        "PER-RUN EXACT APPROVAL ONLY; NO BLANKET AUTHORITY; NO RTM GENERATION; "
        "NO DRIFT REJECTION; NO COVERAGE TRUTH; NO PROTECTED BODY READS; NO TARGET/SOURCE/GIT MUTATION."
    )


def _build_run_evidence(ledger_package: dict[str, Any], requests: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not isinstance(requests, list) or len(requests) != 3:
        raise ValueError("repeat_run_requests must contain exactly three runs")
    ledger = deepcopy(ledger_package["ledger"])
    used_runs = set(ledger["used_run_ids"])
    used_approvals = set(ledger["used_approval_ids"])
    used_nonces = set(ledger["used_nonces"])
    evidence = []
    previous_hash = ledger["current_ledger_hash"]
    for index, request in enumerate(requests, start=1):
        _validate_run_request(request, ledger_package, previous_hash, used_runs, used_approvals, used_nonces)
        entry = _run_evidence_entry(index, request, previous_hash)
        entry["entry_hash"] = _canonical_hash(entry)
        evidence.append(entry)
        previous_hash = entry["entry_hash"]
        used_runs.add(entry["run_id_consumed"])
        used_approvals.add(entry["approval_id"])
        used_nonces.add(entry["nonce"])
        ledger["ledger_entries"].append(deepcopy(entry))
    ledger["used_run_ids"] = [entry["run_id_consumed"] for entry in evidence]
    ledger["used_approval_ids"] = [entry["approval_id"] for entry in evidence]
    ledger["used_nonces"] = [entry["nonce"] for entry in evidence]
    ledger["current_ledger_hash"] = previous_hash
    return evidence, ledger


def _run_evidence_entry(index: int, request: dict[str, Any], previous_hash: str) -> dict[str, Any]:
    return {
        "run_sequence": index,
        "approval_id": request["approval_id"],
        "run_id_consumed": request["run_id_to_consume"],
        "nonce": request["nonce"],
        "ledger_previous_hash": previous_hash,
        "canonical_upstream_hash": request["canonical_upstream_hash"],
        "operator_decision_text_raw": request["operator_decision_text_raw"],
        "decided_at": request["decided_at"],
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "per_run_exact_approval_captured": True,
        "production_wrapper_run_executed": True,
        "wrapper_run_result": "REPEATABLE_TRUSTED_BLK_LINK_WRAPPER_RUN_RECORDED_CLEAN",
        "rtm_generated": False,
        "protected_body_reads": False,
        "target_source_git_mutation_performed": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
    }


def _validate_run_request(request: Any, ledger_package: dict[str, Any], previous_hash: str, used_runs: set[str], used_approvals: set[str], used_nonces: set[str]) -> None:
    keys = {"approval_id", "run_id_to_consume", "nonce", "operator_decision_text_raw", "ledger_previous_hash", "canonical_upstream_hash", "decided_at", "requested_at", "expires_at", "operator_attestation"}
    if not isinstance(request, dict):
        raise ValueError("repeat run request must be a dictionary")
    if set(request) != keys:
        raise ValueError("repeat run request must match exact schema")
    _required_hash(request["ledger_previous_hash"], "ledger_previous_hash")
    if request["ledger_previous_hash"] != previous_hash:
        raise ValueError("ledger_previous_hash must be exact current hash")
    _require(request, "canonical_upstream_hash", ledger_package["ledger_package_hash"])
    for field in ("approval_id", "run_id_to_consume", "nonce"):
        _scan_high_risk_freeform(request[field], field)
        if not isinstance(request[field], str) or not request[field].startswith(field.split("_")[0].upper()):
            raise ValueError(f"{field} must be exact ASCII identifier text")
    if request["run_id_to_consume"] in used_runs or request["approval_id"] in used_approvals or request["nonce"] in used_nonces:
        raise ValueError("run_id_to_consume must be unique and unused")
    _require(request, "operator_decision_text_raw", _operator_text(request["approval_id"], request["run_id_to_consume"], request["nonce"]))
    if not isinstance(request["operator_attestation"], dict) or set(request["operator_attestation"]) != _ATTESTATION_193:
        raise ValueError("repeat run operator_attestation must match exact key set")
    for value in request["operator_attestation"].values():
        if value is not True:
            raise ValueError("repeat run operator_attestation values must be true")
    _validate_approval_window(request["decided_at"], request["requested_at"], request["expires_at"])


def _validate_record(record: Any, keys: frozenset[str], attestation_keys: frozenset[str], proof_set: set[str], excluded_set: set[str], flags: tuple[str, ...], true_flags: set[str]) -> dict[str, Any]:
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


def _validate_contract(contract: Any, review: dict[str, Any]) -> None:
    expected = _contract_body(review)
    if contract != expected:
        raise ValueError("contract must match exact repeatable trusted schema")


def _validate_genesis_ledger(ledger: Any, contract: dict[str, Any]) -> dict[str, Any]:
    keys = {"ledger_mode", "genesis_ledger_hash", "current_ledger_hash", "used_run_ids", "used_approval_ids", "used_nonces", "ledger_entries"}
    if not isinstance(ledger, dict) or set(ledger) != keys:
        raise ValueError("ledger must match exact genesis schema")
    if ledger["ledger_mode"] != "CALLER_SUPPLIED_HASH_CHAIN_NO_FILESYSTEM_WRITE":
        raise ValueError("ledger_mode must be caller supplied hash chain")
    expected_genesis = _canonical_hash({
        "ledger_package_id": LEDGER_PACKAGE_ID_192,
        "upstream_contract_package_hash": contract["contract_package_hash"],
        "contract_hash": contract["contract_hash"],
        "operator_identity": contract["operator_identity"],
        "ledger_scope": LEDGER_SCOPE_192,
    })
    if ledger["genesis_ledger_hash"] != expected_genesis or ledger["current_ledger_hash"] != expected_genesis:
        raise ValueError("ledger genesis/current hash must bind contract")
    if ledger["used_run_ids"] != [] or ledger["used_approval_ids"] != [] or ledger["used_nonces"] != [] or ledger["ledger_entries"] != []:
        raise ValueError("ledger genesis must be empty")
    return deepcopy(ledger)


def _validate_189_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-189 package must be a dictionary")
    extra = sorted(set(package) - _KEYS_189_PACKAGE)
    if extra:
        raise ValueError(f"unexpected BLK-189 field {extra[0]!r}")
    missing = sorted(_KEYS_189_PACKAGE - set(package))
    if missing:
        raise ValueError(f"missing BLK-189 field {missing[0]!r}")
    _require(package, "reconciliation_status", RECONCILIATION_STATUS_189)
    _require(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_189)
    _require(package, "reconciliation_scope", RECONCILIATION_SCOPE_189)
    _require(package, "selected_frontier", SELECTED_FRONTIER_189)
    _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if package["reconciliation_package_hash"] != computed:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-189 package")
    if package["reconciliation_package_hash"] != CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-189 reconciliation package hash mismatch")
    if package.get("upstream_execution_package_hash") != CANONICAL_BLK188_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-189 must bind canonical BLK-188 package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_189, "BLK-189 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_189, "BLK-189 excluded_authorities")
    if package.get("next_frontier_granted") is not False:
        raise ValueError("BLK-189 next_frontier_granted must remain false")
    for flag in SIDE_EFFECT_FLAGS_189:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-189 package {flag} must remain false")
    return package


def _validate_190_package(package: Any) -> dict[str, Any]:
    return _validate_package(package, "review", REVIEW_STATUS_190, REVIEW_PACKAGE_ID_190, "review_status", "review_package_hash", CANONICAL_BLK190_REVIEW_PACKAGE_HASH, EXACT_PROOF_OBLIGATIONS_190, EXACT_EXCLUDED_AUTHORITIES_190, SIDE_EFFECT_FLAGS_190, {"single_run_reviewed_clean", "repeatable_trusted_path_selected"})


def _validate_191_package(package: Any) -> dict[str, Any]:
    return _validate_package(package, "contract", CONTRACT_STATUS_191, CONTRACT_PACKAGE_ID_191, "contract_status", "contract_package_hash", CANONICAL_BLK191_CONTRACT_PACKAGE_HASH, EXACT_PROOF_OBLIGATIONS_191, EXACT_EXCLUDED_AUTHORITIES_191, SIDE_EFFECT_FLAGS_191, {"repeatable_trusted_contract_emitted"})


def _validate_192_package(package: Any) -> dict[str, Any]:
    return _validate_package(package, "ledger", LEDGER_STATUS_192, LEDGER_PACKAGE_ID_192, "ledger_status", "ledger_package_hash", CANONICAL_BLK192_LEDGER_PACKAGE_HASH, EXACT_PROOF_OBLIGATIONS_192, EXACT_EXCLUDED_AUTHORITIES_192, SIDE_EFFECT_FLAGS_192, {"caller_supplied_trust_ledger_initialized"})


def _validate_193_package(package: Any) -> dict[str, Any]:
    validated = _validate_package(package, "repeat runs", REPEAT_RUN_STATUS_193, REPEAT_RUN_PACKAGE_ID_193, "repeat_run_status", "repeat_runs_package_hash", CANONICAL_BLK193_REPEAT_RUNS_PACKAGE_HASH, EXACT_PROOF_OBLIGATIONS_193, EXACT_EXCLUDED_AUTHORITIES_193, SIDE_EFFECT_FLAGS_193, {"per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed", "caller_supplied_ledger_advanced"})
    if validated.get("repeat_run_count") != 3:
        raise ValueError("BLK-193 must contain exactly three repeat runs")
    return validated


def _validate_package(package: Any, label: str, status: str, package_id: str, status_key: str, hash_key: str, canonical_hash: str, proof: set[str], excluded: set[str], flags: tuple[str, ...], true_flags: set[str]) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError(f"BLK package {label} must be a dictionary")
    _require(package, status_key, status)
    id_key = f"{label.replace(' ', '_')}_package_id"
    if id_key not in package:
        id_key = "repeat_runs_package_id" if label == "repeat runs" else id_key
    _require(package, id_key, package_id)
    _required_hash(package.get(hash_key), hash_key)
    computed = _canonical_hash({k: v for k, v in package.items() if k != hash_key})
    if package[hash_key] != computed:
        raise ValueError(f"{hash_key} does not match submitted BLK package")
    if package[hash_key] != canonical_hash:
        raise ValueError(f"canonical BLK-{package_id.split('-')[-2]} {label} package hash mismatch")
    _required_exact_set(package.get("proof_obligations"), proof, f"BLK {label} proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), excluded, f"BLK {label} excluded_authorities")
    for flag in flags:
        expected = flag in true_flags
        if package.get(flag) is not expected:
            raise ValueError(f"BLK package {label} {flag} must be {expected}")
    return package


def _validate_approval_window(decided_at: str, requested_at: str, expires_at: str) -> None:
    decided = _parse_not_stale(decided_at, "decided_at")
    requested = _parse_not_stale(requested_at, "requested_at")
    expires = _parse_not_stale(expires_at, "expires_at")
    if requested < decided or expires <= requested:
        raise ValueError("approval request must be within approval decision window")


def _set_flags(record: dict[str, Any], flags: tuple[str, ...], true_flags: set[str]) -> None:
    for flag in flags:
        record[flag] = flag in true_flags
