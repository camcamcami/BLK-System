"""BLK-SYSTEM-167 post-run reconciliation for BLK-SYSTEM-166.

This deterministic fixture consumes the exact BLK-SYSTEM-166 decision/execution
package and emits clean post-run reconciliation evidence. It records that no
observed failure requires BLK-SYSTEM-168 hardening, without granting reusable
production blk-link authority, RTM generation, drift rejection, coverage truth,
protected-body access, runtime/tooling, source/Git mutation, or signer/storage/
ledger reuse.
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
from production_blk_link_rtm_trace_closure_decision_execution_166 import (
    APPROVAL_ID_166,
    DECISION_EXECUTION_PACKAGE_ID_166,
    DECISION_EXECUTION_SCOPE_166,
    DECISION_EXECUTION_STATUS_166,
    EXACT_EXCLUDED_AUTHORITIES_166 as BLK166_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS_166 as BLK166_PROOF_OBLIGATIONS,
    EXECUTION_RECORD_ID_166,
    NEXT_REQUIRED_AUTHORITY_166 as BLK166_NEXT_REQUIRED_AUTHORITY,
    RUN_ID_CONSUMED_166,
    SELECTED_FRONTIER_166 as BLK166_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS_166 as BLK166_SIDE_EFFECT_FLAGS,
)

RECONCILIATION_STATUS_167 = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_RUN_RECONCILED_CLEAN_AFTER_BLK166"
RECONCILIATION_PACKAGE_ID_167 = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-RUN-RECONCILIATION-167-001"
RECONCILIATION_SCOPE_167 = "POST_RUN_RECONCILIATION_ONLY_CLEAN_RECORD_NO_NEW_RUNTIME_AUTHORITY"
SELECTED_FRONTIER_167 = "production_blk_link_rtm_trace_closure_post_run_reconciliation_167"
NEXT_FRONTIER_167 = "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_CAPABILITY_AFTER_CLEAN_RECONCILIATION_NOT_GRANTED"
CANONICAL_BLK166_DECISION_EXECUTION_PACKAGE_HASH = "sha256:408f720d5b58a6addb5251fb3bb6142b5583a030af419e4d5cba9d85c72d6297"
CANONICAL_BLK166_DECISION_EXECUTION_REQUEST_HASH = "sha256:83cb113bd5799174dfa95df0a667f78d7951100b11092208eeb3fce5cd9ea042"
CANONICAL_BLK166_EXECUTION_RECORD_HASH = "sha256:d1c3d267fba4d3ce144a63d54dc60057f917867eb2f27b3aad6998a9d2899889"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-16T19:05:00+10:00")

SIDE_EFFECT_FLAGS_167 = (
    "observed_failure_hardening_performed",
    "reusable_blk_link_authority_granted",
    "production_blk_link_authorized_beyond_exact_record",
    "production_blk_link_live_execution_performed",
    "runtime_rtm_generation_authorized",
    "rtm_generated",
    "reusable_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
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

EXACT_EXCLUDED_AUTHORITIES_167 = {
    "OBSERVED_FAILURE_HARDENING_WITHOUT_OBSERVED_FAILURE",
    "POST_RUN_RECONCILIATION_AS_RUNTIME_AUTHORITY",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_LIVE_RUNTIME_EXECUTION_BEYOND_RECORD_ONLY_EVIDENCE",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
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

EXACT_PROOF_OBLIGATIONS_167 = {
    "BLK166_DECISION_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK166_EXECUTION_RECORD_IDENTITY_AND_HASH_BOUND",
    "BLK165_REQUEST_PACKAGE_IDENTITY_BOUND_THROUGH_BLK166",
    "RUN_ID_CONSUMPTION_RECONCILED_AS_RECORD_ONLY_EVIDENCE",
    "CLEAN_RECORD_ONLY_EVIDENCE_CLASSIFIED",
    "NO_OBSERVED_FAILURE_REQUIRING_BLK168_HARDENING",
    "ROADMAP_NEXT_FRONTIER_RECONCILED_AFTER_CLEAN_RUN",
    "CURRENT_STATE_INDEX_RECONCILED_AFTER_CLEAN_RUN",
    "REUSABLE_BLK_LINK_AUTHORITY_EXCLUDED",
    "RTM_GENERATION_NOT_AUTHORIZED_BY_RECONCILIATION",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "OPERATOR_SELECTION_REQUIRED_BEFORE_ANY_NEXT_CAPABILITY",
}

_DECISION_EXECUTION_PACKAGE_KEYS = frozenset(
    {
        "decision_execution_status",
        "decision_execution_package_id",
        "operator_identity",
        "decision_execution_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_review_package_id",
        "upstream_review_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "approval_id",
        "run_id_consumed",
        "decision_result",
        "decided_at",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_decision_captured",
        "one_run_id_consumed_in_record_only_evidence",
        "decision_execution_request_hash",
        "execution_record_id",
        "execution_record",
        "execution_record_hash",
        "production_blk_link_rtm_trace_closure_record_emitted",
        "next_required_authority",
        "operator_decision_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "decision_execution_package_hash",
        *BLK166_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_RECORD_KEYS = frozenset(
    {
        "execution_record_id",
        "consumed_run_id",
        "approval_id",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "trace_closure_authority",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "recorded_at",
        "reusable_blk_link_authority_granted",
        "rtm_generated",
        "rtm_drift_rejection_performed",
        "active_vault_hash_comparison_performed",
        "coverage_truth_established",
        "protected_body_reads",
        "public_ledger_mutation",
        "execution_record_hash",
    }
)

_RECONCILIATION_CONTEXT_KEYS = frozenset(
    {
        "reconciliation_package_id",
        "operator_identity",
        "reconciliation_scope",
        "selected_frontier",
        "upstream_decision_execution_package_id",
        "upstream_decision_execution_package_hash",
        "upstream_execution_record_id",
        "upstream_execution_record_hash",
        "run_id_consumed",
        "approval_id",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "reconciled_at",
        "stale",
        "replayed",
        "observed_failure_requires_168",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS_167,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk166_decision_execution_package_reviewed",
        "clean_record_only_evidence_reconciled",
        "no_observed_failure_requires_168",
        "roadmap_vocabulary_reconciled",
        "current_state_index_reconciled",
        "record_only_trace_closure_preserved",
        "no_reusable_blk_link_authority_claim",
        "rtm_generation_not_authorized",
        "drift_rejection_excluded",
        "active_vault_hash_comparison_excluded",
        "coverage_truth_excluded",
        "protected_body_reads_excluded",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)


def valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(
    execution166: dict[str, Any], **overrides: Any
) -> dict[str, Any]:
    context = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_167,
        "operator_identity": execution166["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_167,
        "selected_frontier": SELECTED_FRONTIER_167,
        "upstream_decision_execution_package_id": execution166["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": execution166["decision_execution_package_hash"],
        "upstream_execution_record_id": execution166["execution_record_id"],
        "upstream_execution_record_hash": execution166["execution_record_hash"],
        "run_id_consumed": execution166["run_id_consumed"],
        "approval_id": execution166["approval_id"],
        "beo_id": execution166["beo_id"],
        "beb_id": execution166["beb_id"],
        "exact_trace_identities": list(execution166["exact_trace_identities"]),
        "reconciled_at": "2099-05-16T15:48:00+10:00",
        "stale": False,
        "replayed": False,
        "observed_failure_requires_168": False,
        "operator_attestation": {
            "exact_blk166_decision_execution_package_reviewed": True,
            "clean_record_only_evidence_reconciled": True,
            "no_observed_failure_requires_168": True,
            "roadmap_vocabulary_reconciled": True,
            "current_state_index_reconciled": True,
            "record_only_trace_closure_preserved": True,
            "no_reusable_blk_link_authority_claim": True,
            "rtm_generation_not_authorized": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_167),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_167),
    }
    for flag in SIDE_EFFECT_FLAGS_167:
        context[flag] = False
    context.update(overrides)
    return context


def build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(
    decision_execution_package166: dict[str, Any], reconciliation_context: dict[str, Any]
) -> dict[str, Any]:
    execution = _validate_blk166_decision_execution_package(decision_execution_package166)
    context = _validate_reconciliation_context_167(reconciliation_context, execution)
    trace_identities = list(execution["exact_trace_identities"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS_167,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_167,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE_167,
        "selected_frontier": SELECTED_FRONTIER_167,
        "upstream_decision_execution_package_id": execution["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": execution["decision_execution_package_hash"],
        "upstream_execution_record_id": execution["execution_record_id"],
        "upstream_execution_record_hash": execution["execution_record_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "approval_id": execution["approval_id"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": trace_identities,
        "reconciled_at": context["reconciled_at"],
        "stale": False,
        "replayed": False,
        "clean_record_only_evidence_reconciled": True,
        "observed_failure_requires_168": False,
        "current_state_index_reconciled": True,
        "roadmap_reconciled": True,
        "record_only_trace_closure_preserved": True,
        "next_frontier": NEXT_FRONTIER_167,
        "reconciliation_context_hash": _canonical_hash(context),
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_167),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_167),
    }
    for flag in SIDE_EFFECT_FLAGS_167:
        package[flag] = False
    package["reconciliation_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "reconciliation_package_hash"}
    )
    return package


def _validate_blk166_decision_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("decision_execution_package166 must be a dictionary")
    unknown = sorted(set(package) - _DECISION_EXECUTION_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"decision_execution_package166 rejects unexpected field {unknown[0]!r}")
    missing = sorted(_DECISION_EXECUTION_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"decision_execution_package166 missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("decision_execution_package_hash"), "decision_execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "decision_execution_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("decision_execution_package_hash does not match submitted BLK-166 package")
    if submitted_hash != CANONICAL_BLK166_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("package must match canonical BLK-166 decision execution package")
    record = _validate_execution_record_166(normalized.get("execution_record"))
    if record["execution_record_hash"] != normalized.get("execution_record_hash"):
        raise ValueError("execution_record_hash must match nested BLK-166 record")
    expected = {
        "decision_execution_status": DECISION_EXECUTION_STATUS_166,
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_166,
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_166,
        "selected_frontier": BLK166_SELECTED_FRONTIER,
        "upstream_authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-001",
        "upstream_authority_request_package_hash": "sha256:858ecad7e6806932745501acfca4ac53c6912668a0fc5ce0a27ba097951cda3d",
        "upstream_review_package_id": "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
        "upstream_review_package_hash": "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9",
        "upstream_execution_package_id": "METADATA-TRACE-CLOSURE-EXECUTION-161-001",
        "upstream_execution_package_hash": "sha256:05283f1deacf1b0fc478bb99f198f7ed18911eca4cdcac1b7d5a9c24d695cb2f",
        "upstream_trace_closure_record_id": "METADATA-TRACE-CLOSURE-RECORD-161-001",
        "upstream_trace_closure_record_hash": "sha256:2ecb6d2a56e53d9460e0c91320393ae8246aed76d1bd5a1e3237584d79e0e940",
        "approval_id": APPROVAL_ID_166,
        "run_id_consumed": RUN_ID_CONSUMED_166,
        "decision_execution_request_hash": CANONICAL_BLK166_DECISION_EXECUTION_REQUEST_HASH,
        "execution_record_id": EXECUTION_RECORD_ID_166,
        "execution_record_hash": CANONICAL_BLK166_EXECUTION_RECORD_HASH,
        "production_blk_link_rtm_trace_closure_record_emitted": True,
        "next_required_authority": BLK166_NEXT_REQUIRED_AUTHORITY,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "expired": False,
        "replayed": False,
        "stale": False,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("package must match canonical BLK-166 decision execution package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("decision execution package trace identities must match canonical BLK-166 package")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("decision execution package trace identities must match canonical BLK-166 package")
    for flag in BLK166_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"decision execution package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK166_PROOF_OBLIGATIONS, "decision_execution_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK166_EXCLUDED_AUTHORITIES, "decision_execution_package excluded_authorities")
    return normalized


def _validate_execution_record_166(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("execution_record must be a dictionary")
    unknown = sorted(set(record) - _EXECUTION_RECORD_KEYS)
    if unknown:
        raise ValueError(f"execution_record rejects unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_RECORD_KEYS - set(record))
    if missing:
        raise ValueError(f"execution_record missing field {missing[0]!r}")
    normalized = deepcopy(record)
    submitted_hash = _required_hash(normalized.get("execution_record_hash"), "execution_record_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_record_hash"})
    if submitted_hash != recomputed or submitted_hash != CANONICAL_BLK166_EXECUTION_RECORD_HASH:
        raise ValueError("execution_record_hash does not match canonical BLK-166 record")
    expected = {
        "execution_record_id": EXECUTION_RECORD_ID_166,
        "consumed_run_id": RUN_ID_CONSUMED_166,
        "approval_id": APPROVAL_ID_166,
        "upstream_authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-001",
        "upstream_authority_request_package_hash": "sha256:858ecad7e6806932745501acfca4ac53c6912668a0fc5ce0a27ba097951cda3d",
        "trace_closure_authority": "EXACT_OPERATOR_APPROVED_PRODUCTION_TRACE_CLOSURE_RECORD_ONLY",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("execution_record must match canonical BLK-166 record")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("execution_record trace identities must match canonical BLK-166 record")
    for flag in (
        "reusable_blk_link_authority_granted",
        "rtm_generated",
        "rtm_drift_rejection_performed",
        "active_vault_hash_comparison_performed",
        "coverage_truth_established",
        "protected_body_reads",
        "public_ledger_mutation",
    ):
        if normalized.get(flag) is not False:
            raise ValueError(f"execution_record {flag} must remain false")
    return normalized


def _validate_reconciliation_context_167(context: Any, execution: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("reconciliation_context must be a dictionary")
    unknown = sorted(set(context) - _RECONCILIATION_CONTEXT_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_RECONCILIATION_CONTEXT_KEYS - set(context))
    if missing:
        raise ValueError(f"reconciliation_context missing field {missing[0]!r}")
    normalized = deepcopy(context)
    for key in (
        "reconciliation_package_id",
        "operator_identity",
        "reconciliation_scope",
        "selected_frontier",
        "upstream_decision_execution_package_id",
        "upstream_decision_execution_package_hash",
        "upstream_execution_record_id",
        "upstream_execution_record_hash",
        "run_id_consumed",
        "approval_id",
        "beo_id",
        "beb_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("reconciliation_package_id") != RECONCILIATION_PACKAGE_ID_167:
        raise ValueError(f"reconciliation_package_id must be {RECONCILIATION_PACKAGE_ID_167}")
    if normalized.get("operator_identity") != execution["operator_identity"]:
        raise ValueError("operator_identity must match BLK-166 decision execution package")
    if normalized.get("reconciliation_scope") != RECONCILIATION_SCOPE_167:
        raise ValueError(f"reconciliation_scope must be {RECONCILIATION_SCOPE_167}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER_167:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER_167}")
    expected = {
        "upstream_decision_execution_package_id": execution["decision_execution_package_id"],
        "upstream_decision_execution_package_hash": execution["decision_execution_package_hash"],
        "upstream_execution_record_id": execution["execution_record_id"],
        "upstream_execution_record_hash": execution["execution_record_hash"],
        "approval_id": execution["approval_id"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-166 decision execution package")
    if normalized.get("run_id_consumed") != RUN_ID_CONSUMED_166:
        raise ValueError(f"run_id_consumed must be {RUN_ID_CONSUMED_166}")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != execution["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-166 decision execution package")
    if normalized.get("observed_failure_requires_168") is not False:
        raise ValueError("observed_failure_requires_168 must be false for clean BLK-167 reconciliation")
    for flag in SIDE_EFFECT_FLAGS_167:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("stale", "replayed"):
        if normalized.get(flag) is not False:
            raise ValueError(f"reconciliation context must not be {flag}")
    reconciled_at = _parse_timestamp(normalized.get("reconciled_at"), "reconciled_at")
    if reconciled_at <= FIXTURE_EVALUATION_AT.astimezone(reconciled_at.tzinfo):
        raise ValueError("reconciliation context must not be calendar-stale")
    normalized["operator_attestation"] = _validate_attestation_167(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(
        normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_167, "proof_obligations"
    )
    normalized["excluded_authorities"] = _required_exact_set(
        normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_167, "excluded_authorities"
    )
    return normalized


def _validate_attestation_167(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown = sorted(set(value) - _ATTESTATION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_ATTESTATION_KEYS - set(value))
    if missing:
        raise ValueError(f"operator_attestation missing field {missing[0]!r}")
    _scan_value_strings(value, "operator_attestation", scan_keys=False)
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized
