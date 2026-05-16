"""BLK-SYSTEM-165 production blk-link / RTM trace-closure authority request.

This deterministic fixture consumes the exact BLK-SYSTEM-162 post metadata
trace-closure review plus BLK-SYSTEM-163/164 hardening markers and emits one
request-only package for a future exact production blk-link / RTM trace-closure
approval-capture step. It does not capture approval, reserve or consume a run ID,
execute production blk-link, generate RTM, reject drift, compare active-vault
hashes, establish coverage truth, read protected bodies, mutate target/source/Git
state, run BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_trace_closure_approval_capture import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from metadata_rtm_post_generation_ladder_159_162 import (
    EXACT_EXCLUDED_AUTHORITIES_162,
    POST_EXECUTION_REVIEW_ID_162,
    REQUIRED_FALSE_FLAGS as BLK162_REQUIRED_FALSE_FLAGS,
)

REQUEST_STATUS_165 = (
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_BLK162_REVIEW_AND_164_HARDENING_NOT_GRANTED"
)
AUTHORITY_REQUEST_PACKAGE_ID_165 = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-001"
SELECTED_FRONTIER_165 = "production_blk_link_rtm_trace_closure_authority_request_after_164_hardening"
REQUEST_SCOPE_165 = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_BLK162_REVIEW_AND_164_HARDENING_REVIEW_ONLY"
NEXT_FRONTIER_165 = "NEXT_FRONTIER_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_NOT_GRANTED"
NEXT_REQUIRED_AUTHORITY_165 = "EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_REQUIRED_NOT_CAPTURED"
CANONICAL_BLK162_REVIEW_PACKAGE_HASH = "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9"
CANONICAL_BLK161_EXECUTION_PACKAGE_HASH = "sha256:05283f1deacf1b0fc478bb99f198f7ed18911eca4cdcac1b7d5a9c24d695cb2f"
CANONICAL_BLK161_TRACE_CLOSURE_RECORD_HASH = "sha256:2ecb6d2a56e53d9460e0c91320393ae8246aed76d1bd5a1e3237584d79e0e940"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-16T13:33:10+10:00")

ACTIVE_HARDENING_MARKERS = (
    "BLK_SYSTEM_162_POST_TRACE_CLOSURE_REVIEW_COMPLETE",
    "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001",
    "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9",
    "BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED",
    "BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED",
)

SIDE_EFFECT_FLAGS_165 = (
    "production_blk_link_rtm_trace_closure_approval_captured",
    "future_run_id_reserved_or_consumed",
    "production_blk_link_rtm_trace_closure_authorized",
    "production_rtm_trace_closure_executed",
    "production_blk_link_authorized",
    "production_blk_link_executed",
    "rtm_generated",
    "rtm_generation_authorized",
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

EXACT_EXCLUDED_AUTHORITIES_165 = {
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_OR_CONSUMPTION_THIS_SPRINT",
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
    "PRODUCTION_OR_REUSABLE_BLK_LINK_EXECUTION",
    "PRODUCTION_RTM_TRACE_CLOSURE_EXECUTION",
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

EXACT_PROOF_OBLIGATIONS_165 = {
    "BLK162_REVIEW_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK161_EXECUTION_PACKAGE_HASH_BOUND_THROUGH_BLK162",
    "BLK161_TRACE_CLOSURE_RECORD_HASH_BOUND_THROUGH_BLK162",
    "BLK163_DENIED_SURFACE_HARDENING_STATE_BOUND",
    "BLK164_ACTIVE_DOC_DENIED_SURFACE_SYNC_BOUND",
    "REQUEST_ONLY_FUTURE_EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
    "NO_APPROVAL_CAPTURE_PERFORMED",
    "NO_RUN_ID_RESERVED_OR_CONSUMED",
    "NO_PRODUCTION_BLK_LINK_EXECUTION",
    "NO_RTM_GENERATION_OR_DRIFT_REJECTION",
    "NO_COVERAGE_TRUTH_OR_ACTIVE_VAULT_COMPARISON",
    "NO_PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "NO_SIGNER_STORAGE_LEDGER_OR_ROLLBACK_SIDE_EFFECTS",
    "NO_TARGET_SOURCE_GIT_MUTATION",
    "NO_BLK_PIPE_BLK_TEST_CODEX_OR_TOOLING_RUNTIME",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_APPROVAL_CAPTURE",
}

_REQUEST_KEYS = frozenset(
    {
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
        "request_future_exact_production_blk_link_rtm_trace_closure_approval",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS_165,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk162_post_trace_closure_review_consumed",
        "blk163_denied_surface_hardening_state_bound",
        "blk164_active_doc_denied_surface_sync_bound",
        "request_is_for_future_production_blk_link_rtm_trace_closure_approval_not_approval",
        "approval_capture_not_performed",
        "run_id_not_reserved_or_consumed",
        "production_blk_link_not_executed",
        "rtm_generation_not_performed",
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

_BLK162_REVIEW_KEYS = frozenset(
    {
        "review_status",
        "review_package_id",
        "operator_identity",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "review_result",
        "next_frontier",
        "next_frontier_granted",
        "reviewed_at",
        "expired",
        "replayed",
        "stale",
        "proof_obligations",
        "excluded_authorities",
        "review_context_hash",
        "review_package_hash",
        *BLK162_REQUIRED_FALSE_FLAGS,
    }
)


def valid_production_blk_link_rtm_trace_closure_authority_request_165(
    review162: dict[str, Any], **overrides: Any
) -> dict[str, Any]:
    request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID_165,
        "operator_identity": review162["operator_identity"],
        "request_scope": REQUEST_SCOPE_165,
        "selected_frontier": SELECTED_FRONTIER_165,
        "upstream_review_package_id": review162["review_package_id"],
        "upstream_review_package_hash": review162["review_package_hash"],
        "upstream_execution_package_id": review162["upstream_execution_package_id"],
        "upstream_execution_package_hash": review162["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": review162["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": review162["upstream_trace_closure_record_hash"],
        "beo_id": review162["beo_id"],
        "beb_id": review162["beb_id"],
        "exact_trace_identities": list(review162["exact_trace_identities"]),
        "active_hardening_markers": list(ACTIVE_HARDENING_MARKERS),
        "request_future_exact_production_blk_link_rtm_trace_closure_approval": True,
        "requested_at": "2099-05-16T15:30:00+10:00",
        "expires_at": "2099-05-16T15:45:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk162_post_trace_closure_review_consumed": True,
            "blk163_denied_surface_hardening_state_bound": True,
            "blk164_active_doc_denied_surface_sync_bound": True,
            "request_is_for_future_production_blk_link_rtm_trace_closure_approval_not_approval": True,
            "approval_capture_not_performed": True,
            "run_id_not_reserved_or_consumed": True,
            "production_blk_link_not_executed": True,
            "rtm_generation_not_performed": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_165),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_165),
    }
    for flag in SIDE_EFFECT_FLAGS_165:
        request[flag] = False
    request.update(overrides)
    return request


def build_production_blk_link_rtm_trace_closure_authority_request_165(
    review162: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    upstream = _validate_blk162_review_package(review162)
    request = _validate_authority_request_165(authority_request, upstream)
    request_hash = _canonical_hash(request)
    package = {
        "request_status": REQUEST_STATUS_165,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID_165,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE_165,
        "selected_frontier": SELECTED_FRONTIER_165,
        "upstream_review_package_id": upstream["review_package_id"],
        "upstream_review_package_hash": upstream["review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["upstream_trace_closure_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "active_hardening_markers": list(ACTIVE_HARDENING_MARKERS),
        "requested_authority": "ONE_FUTURE_EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
        "request_future_exact_production_blk_link_rtm_trace_closure_approval": True,
        "production_blk_link_rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "approval_capture_performed": False,
        "future_run_id_reserved_or_consumed": False,
        "production_blk_link_execution_performed": False,
        "rtm_trace_closure_executed": False,
        "next_frontier": NEXT_FRONTIER_165,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_165,
        "authority_request_hash": request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_165),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_165),
    }
    for flag in SIDE_EFFECT_FLAGS_165:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


def _validate_blk162_review_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-162 review package must be a dictionary")
    unknown = sorted(set(package) - _BLK162_REVIEW_KEYS)
    if unknown:
        raise ValueError(f"BLK-162 review package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_BLK162_REVIEW_KEYS - set(package))
    if missing:
        raise ValueError(f"BLK-162 review package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("review_package_hash"), "review_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "review_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("review_package_hash does not match submitted BLK-162 package")
    if submitted_hash != CANONICAL_BLK162_REVIEW_PACKAGE_HASH:
        raise ValueError("package must match canonical BLK-162 post trace-closure review package")
    expected = {
        "review_status": "POST_METADATA_TRACE_CLOSURE_REVIEW_COMPLETE_NOT_AUTHORITY",
        "review_package_id": POST_EXECUTION_REVIEW_ID_162,
        "selected_frontier": "post_metadata_trace_closure_review",
        "upstream_execution_package_id": "METADATA-TRACE-CLOSURE-EXECUTION-161-001",
        "upstream_execution_package_hash": CANONICAL_BLK161_EXECUTION_PACKAGE_HASH,
        "upstream_trace_closure_record_id": "METADATA-TRACE-CLOSURE-RECORD-161-001",
        "upstream_trace_closure_record_hash": CANONICAL_BLK161_TRACE_CLOSURE_RECORD_HASH,
        "review_result": "CLEAN_METADATA_TRACE_CLOSURE_REVIEWED_NEXT_FRONTIER_NOT_GRANTED",
        "next_frontier": "NEXT_FRONTIER_HARDENING_OR_OPERATOR_SELECTED_AUTHORITY_NOT_GRANTED",
        "next_frontier_granted": False,
        "expired": False,
        "replayed": False,
        "stale": False,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("package must match canonical BLK-162 post trace-closure review package")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("exact_trace_identities must match canonical BLK-162 trace metadata")
    _required_exact_set(normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_162, "BLK-162 excluded_authorities")
    for flag in BLK162_REQUIRED_FALSE_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-162 review package {flag} must remain false")
    return normalized


def _validate_authority_request_165(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"authority_request missing field {missing[0]!r}")
    normalized = deepcopy(request)
    for key in (
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
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("authority_request_package_id") != AUTHORITY_REQUEST_PACKAGE_ID_165:
        raise ValueError(f"authority_request_package_id must be {AUTHORITY_REQUEST_PACKAGE_ID_165}")
    if normalized.get("operator_identity") != upstream["operator_identity"]:
        raise ValueError("operator_identity must match canonical BLK-162 review package")
    if normalized.get("request_scope") != REQUEST_SCOPE_165:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE_165}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER_165:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER_165}")
    expected = {
        "upstream_review_package_id": upstream["review_package_id"],
        "upstream_review_package_hash": upstream["review_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["upstream_trace_closure_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match canonical BLK-162 review package")
    if normalized.get("exact_trace_identities") != upstream["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match canonical BLK-162 review package")
    if normalized.get("active_hardening_markers") != list(ACTIVE_HARDENING_MARKERS):
        raise ValueError("active_hardening_markers must match exact BLK-162/163/164 state")
    if normalized.get("request_future_exact_production_blk_link_rtm_trace_closure_approval") is not True:
        raise ValueError("request_future_exact_production_blk_link_rtm_trace_closure_approval must be true")
    for flag in SIDE_EFFECT_FLAGS_165:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"authority request must not be {flag}")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("authority request must not be calendar-expired")
    normalized["operator_attestation"] = _validate_attestation_165(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(
        normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_165, "proof_obligations"
    )
    normalized["excluded_authorities"] = _required_exact_set(
        normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_165, "excluded_authorities"
    )
    return normalized


def _validate_attestation_165(value: Any) -> dict[str, bool]:
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
