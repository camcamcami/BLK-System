"""BLK-SYSTEM-166 production blk-link / RTM trace-closure decision + one-run package.

This deterministic fixture consumes the exact BLK-SYSTEM-165 request package,
captures the operator decision, consumes one run ID inside record-only metadata
trace-closure evidence, and stops at post-run reconciliation. It does not grant
reusable production blk-link authority, generate RTM, reject drift, establish
coverage truth, read protected bodies, mutate target/source/Git state, run
BLK-pipe/BLK-test/Codex/tooling, perform signer/storage/ledger behavior, or
claim production isolation.
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
from production_blk_link_rtm_trace_closure_authority_request_165 import (
    ACTIVE_HARDENING_MARKERS as BLK165_ACTIVE_HARDENING_MARKERS,
    AUTHORITY_REQUEST_PACKAGE_ID_165 as BLK165_AUTHORITY_REQUEST_PACKAGE_ID,
    CANONICAL_BLK161_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK161_TRACE_CLOSURE_RECORD_HASH,
    CANONICAL_BLK162_REVIEW_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_165 as BLK165_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS_165 as BLK165_PROOF_OBLIGATIONS,
    NEXT_FRONTIER_165 as BLK165_NEXT_FRONTIER,
    NEXT_REQUIRED_AUTHORITY_165 as BLK165_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE_165 as BLK165_REQUEST_SCOPE,
    REQUEST_STATUS_165 as BLK165_REQUEST_STATUS,
    SELECTED_FRONTIER_165 as BLK165_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS_165 as BLK165_SIDE_EFFECT_FLAGS,
)

DECISION_EXECUTION_STATUS_166 = (
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_DECISION_CAPTURED_AND_ONE_RUN_RECORDED_FOR_EXACT_BLK165_REQUEST"
)
DECISION_EXECUTION_PACKAGE_ID_166 = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-DECISION-EXECUTION-166-001"
EXECUTION_RECORD_ID_166 = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-166-001"
APPROVAL_ID_166 = "APPROVAL-BLK-SYSTEM-165-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"
RUN_ID_CONSUMED_166 = "RUN-BLK-SYSTEM-166-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"
SELECTED_FRONTIER_166 = "production_blk_link_rtm_trace_closure_decision_execution_166"
DECISION_EXECUTION_SCOPE_166 = "EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_DECISION_AND_ONE_RUN_RECORD_ONLY"
DECISION_RESULT_166 = "OPERATOR_DIRECTED_EXACT_BLK165_REQUEST_APPROVED_FOR_ONE_RECORD_ONLY_TRACE_CLOSURE_RUN"
NEXT_REQUIRED_AUTHORITY_166 = "POST_RUN_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK165_REQUEST_PACKAGE_HASH = "sha256:858ecad7e6806932745501acfca4ac53c6912668a0fc5ce0a27ba097951cda3d"
CANONICAL_BLK165_AUTHORITY_REQUEST_HASH = "sha256:2bf30208b68f9b9db9cf8dbc3740b6adc95993332808a4e634e7f1d7578f671c"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-16T18:45:00+10:00")

SIDE_EFFECT_FLAGS_166 = (
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

EXACT_EXCLUDED_AUTHORITIES_166 = {
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

EXACT_PROOF_OBLIGATIONS_166 = {
    "BLK165_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK162_REVIEW_PACKAGE_IDENTITY_BOUND_THROUGH_BLK165",
    "BLK161_EXECUTION_PACKAGE_HASH_BOUND_THROUGH_BLK165",
    "BLK161_TRACE_CLOSURE_RECORD_HASH_BOUND_THROUGH_BLK165",
    "BLK163_AND_BLK164_HARDENING_MARKERS_BOUND_THROUGH_BLK165",
    "OPERATOR_DECISION_CAPTURED_FOR_EXACT_BLK165_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_BLK165_REQUEST",
    "RUN_ID_CONSUMED_EXACTLY_IN_RECORD_ONLY_EVIDENCE",
    "PRODUCTION_TRACE_CLOSURE_RECORD_EMITTED_FOR_EXACT_APPROVED_RUN",
    "REUSABLE_BLK_LINK_AUTHORITY_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_RECORD_ONLY_EVIDENCE",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "POST_RUN_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_review_package_id",
        "upstream_review_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "active_hardening_markers",
        "requested_authority",
        "request_future_exact_production_blk_link_rtm_trace_closure_approval",
        "production_blk_link_rtm_trace_closure_authority",
        "approval_capture_performed",
        "future_run_id_reserved_or_consumed",
        "production_blk_link_execution_performed",
        "rtm_trace_closure_executed",
        "next_frontier",
        "next_required_authority",
        "authority_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "authority_request_package_hash",
        *BLK165_SIDE_EFFECT_FLAGS,
    }
)

_DECISION_EXECUTION_KEYS = frozenset(
    {
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
        "run_id_to_consume",
        "decision_result",
        "decided_at",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_decision_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS_166,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk165_request_reviewed",
        "operator_decision_captured_from_latest_directive",
        "approval_limited_to_one_record_only_production_trace_closure_run",
        "run_id_consumed_once_in_record_only_evidence",
        "production_trace_closure_record_only",
        "rtm_generation_not_performed",
        "drift_rejection_excluded",
        "active_vault_hash_comparison_excluded",
        "coverage_truth_excluded",
        "protected_body_reads_excluded",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_reusable_blk_link_authority_claim",
        "no_production_isolation_claim",
    }
)


def valid_production_blk_link_rtm_trace_closure_decision_execution_166(
    request165: dict[str, Any], **overrides: Any
) -> dict[str, Any]:
    request = {
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_166,
        "operator_identity": request165["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_166,
        "selected_frontier": SELECTED_FRONTIER_166,
        "upstream_authority_request_package_id": request165["authority_request_package_id"],
        "upstream_authority_request_package_hash": request165["authority_request_package_hash"],
        "upstream_review_package_id": request165["upstream_review_package_id"],
        "upstream_review_package_hash": request165["upstream_review_package_hash"],
        "upstream_execution_package_id": request165["upstream_execution_package_id"],
        "upstream_execution_package_hash": request165["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": request165["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": request165["upstream_trace_closure_record_hash"],
        "beo_id": request165["beo_id"],
        "beb_id": request165["beb_id"],
        "exact_trace_identities": list(request165["exact_trace_identities"]),
        "approval_id": APPROVAL_ID_166,
        "run_id_to_consume": RUN_ID_CONSUMED_166,
        "decision_result": DECISION_RESULT_166,
        "decided_at": "2099-05-16T15:35:00+10:00",
        "requested_at": "2099-05-16T15:36:00+10:00",
        "expires_at": "2099-05-16T15:44:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_decision_text_raw": "plan and execute 166 to 167 (do 168 if needed)",
        "operator_attestation": {
            "exact_blk165_request_reviewed": True,
            "operator_decision_captured_from_latest_directive": True,
            "approval_limited_to_one_record_only_production_trace_closure_run": True,
            "run_id_consumed_once_in_record_only_evidence": True,
            "production_trace_closure_record_only": True,
            "rtm_generation_not_performed": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_reusable_blk_link_authority_claim": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_166),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_166),
    }
    for flag in SIDE_EFFECT_FLAGS_166:
        request[flag] = False
    request.update(overrides)
    return request


def build_production_blk_link_rtm_trace_closure_decision_execution_166(
    request_package165: dict[str, Any], decision_execution_request: dict[str, Any]
) -> dict[str, Any]:
    upstream = _validate_blk165_request_package(request_package165)
    request = _validate_decision_execution_request_166(decision_execution_request, upstream)
    trace_identities = list(upstream["exact_trace_identities"])
    decision_execution_request_hash = _canonical_hash(request)
    record = {
        "execution_record_id": EXECUTION_RECORD_ID_166,
        "consumed_run_id": RUN_ID_CONSUMED_166,
        "approval_id": APPROVAL_ID_166,
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "trace_closure_authority": "EXACT_OPERATOR_APPROVED_PRODUCTION_TRACE_CLOSURE_RECORD_ONLY",
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "recorded_at": request["requested_at"],
        "reusable_blk_link_authority_granted": False,
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
        "active_vault_hash_comparison_performed": False,
        "coverage_truth_established": False,
        "protected_body_reads": False,
        "public_ledger_mutation": False,
    }
    record["execution_record_hash"] = _canonical_hash(
        {key: value for key, value in record.items() if key != "execution_record_hash"}
    )
    package = {
        "decision_execution_status": DECISION_EXECUTION_STATUS_166,
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_166,
        "operator_identity": request["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_166,
        "selected_frontier": SELECTED_FRONTIER_166,
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "upstream_review_package_id": upstream["upstream_review_package_id"],
        "upstream_review_package_hash": upstream["upstream_review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["upstream_trace_closure_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "approval_id": APPROVAL_ID_166,
        "run_id_consumed": RUN_ID_CONSUMED_166,
        "decision_result": DECISION_RESULT_166,
        "decided_at": request["decided_at"],
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "decision_execution_request_hash": decision_execution_request_hash,
        "execution_record_id": EXECUTION_RECORD_ID_166,
        "execution_record": record,
        "execution_record_hash": record["execution_record_hash"],
        "production_blk_link_rtm_trace_closure_record_emitted": True,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_166,
        "operator_decision_text_raw": request["operator_decision_text_raw"],
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_166),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_166),
    }
    for flag in SIDE_EFFECT_FLAGS_166:
        package[flag] = False
    package["decision_execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "decision_execution_package_hash"}
    )
    return package


def _validate_blk165_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package165 must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"request_package165 rejects unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"request_package165 missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("authority_request_package_hash"), "authority_request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "authority_request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-165 package")
    if submitted_hash != CANONICAL_BLK165_REQUEST_PACKAGE_HASH:
        raise ValueError("request package must match canonical BLK-165 authority request")
    expected = {
        "request_status": BLK165_REQUEST_STATUS,
        "authority_request_package_id": BLK165_AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": BLK165_REQUEST_SCOPE,
        "selected_frontier": BLK165_SELECTED_FRONTIER,
        "upstream_review_package_id": "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
        "upstream_review_package_hash": CANONICAL_BLK162_REVIEW_PACKAGE_HASH,
        "upstream_execution_package_id": "METADATA-TRACE-CLOSURE-EXECUTION-161-001",
        "upstream_execution_package_hash": CANONICAL_BLK161_EXECUTION_PACKAGE_HASH,
        "upstream_trace_closure_record_id": "METADATA-TRACE-CLOSURE-RECORD-161-001",
        "upstream_trace_closure_record_hash": CANONICAL_BLK161_TRACE_CLOSURE_RECORD_HASH,
        "requested_authority": "ONE_FUTURE_EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
        "production_blk_link_rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "approval_capture_performed": False,
        "future_run_id_reserved_or_consumed": False,
        "production_blk_link_execution_performed": False,
        "rtm_trace_closure_executed": False,
        "next_frontier": BLK165_NEXT_FRONTIER,
        "next_required_authority": BLK165_NEXT_REQUIRED_AUTHORITY,
        "authority_request_hash": CANONICAL_BLK165_AUTHORITY_REQUEST_HASH,
        "expired": False,
        "replayed": False,
        "stale": False,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("request package must match canonical BLK-165 authority request")
    if normalized.get("active_hardening_markers") != list(BLK165_ACTIVE_HARDENING_MARKERS):
        raise ValueError("request package must match canonical BLK-165 authority request")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("request package trace identities must match canonical BLK-165 request")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("request package trace identities must match canonical BLK-165 request")
    for flag in BLK165_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"request package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK165_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK165_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    return normalized


def _validate_decision_execution_request_166(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("decision_execution_request must be a dictionary")
    unknown = sorted(set(request) - _DECISION_EXECUTION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_DECISION_EXECUTION_KEYS - set(request))
    if missing:
        raise ValueError(f"decision_execution_request missing field {missing[0]!r}")
    normalized = deepcopy(request)
    for key in (
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
        "approval_id",
        "run_id_to_consume",
        "decision_result",
        "operator_decision_text_raw",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("decision_execution_package_id") != DECISION_EXECUTION_PACKAGE_ID_166:
        raise ValueError(f"decision_execution_package_id must be {DECISION_EXECUTION_PACKAGE_ID_166}")
    if normalized.get("operator_identity") != upstream["operator_identity"]:
        raise ValueError("operator_identity must match BLK-165 request package")
    if normalized.get("decision_execution_scope") != DECISION_EXECUTION_SCOPE_166:
        raise ValueError(f"decision_execution_scope must be {DECISION_EXECUTION_SCOPE_166}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER_166:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER_166}")
    expected = {
        "upstream_authority_request_package_id": upstream["authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["authority_request_package_hash"],
        "upstream_review_package_id": upstream["upstream_review_package_id"],
        "upstream_review_package_hash": upstream["upstream_review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["upstream_trace_closure_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-165 request package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != upstream["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-165 request package")
    if normalized.get("approval_id") != APPROVAL_ID_166:
        raise ValueError(f"approval_id must be {APPROVAL_ID_166}")
    if normalized.get("run_id_to_consume") != RUN_ID_CONSUMED_166:
        raise ValueError(f"run_id_to_consume must be {RUN_ID_CONSUMED_166}")
    if normalized.get("decision_result") != DECISION_RESULT_166:
        raise ValueError(f"decision_result must be {DECISION_RESULT_166}")
    for flag in SIDE_EFFECT_FLAGS_166:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"decision execution request must not be {flag}")
    decided_at = _parse_timestamp(normalized.get("decided_at"), "decided_at")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    upstream_requested_at = _parse_timestamp(upstream.get("requested_at"), "request165.requested_at")
    upstream_expires_at = _parse_timestamp(upstream.get("expires_at"), "request165.expires_at")
    if expires_at <= decided_at or expires_at <= requested_at:
        raise ValueError("expires_at must be after decided_at and requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("decision execution request must not be calendar-expired")
    if decided_at < upstream_requested_at:
        raise ValueError("decision must not predate BLK-165 request")
    if requested_at < decided_at:
        raise ValueError("execution request must not predate operator decision")
    if decided_at >= upstream_expires_at or requested_at >= upstream_expires_at or expires_at > upstream_expires_at:
        raise ValueError("decision/execution window must end within BLK-165 request expiry")
    normalized["operator_attestation"] = _validate_attestation_166(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(
        normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_166, "proof_obligations"
    )
    normalized["excluded_authorities"] = _required_exact_set(
        normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_166, "excluded_authorities"
    )
    return normalized


def _validate_attestation_166(value: Any) -> dict[str, bool]:
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
