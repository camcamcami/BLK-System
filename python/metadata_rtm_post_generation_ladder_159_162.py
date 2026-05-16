"""BLK-SYSTEM-159..162 metadata RTM post-generation authority ladder.

This module advances from the exact BLK-SYSTEM-158 metadata-only RTM generation
record through post-generation reconciliation, a request-only trace-closure
package, one bounded metadata trace-closure execution package, and final
post-execution review. It is deterministic local evidence only: no protected body
reads, no drift rejection, no coverage truth, no active-vault filesystem scan, no
reusable production blk-link, no signer/storage/ledger reuse, no live tooling, and
no target/source/Git mutation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_generation_approval_execution import (
    EXECUTION_PACKAGE_ID as BLK158_EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS as BLK158_EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK158_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK158_PROOF_OBLIGATIONS,
    NEXT_FRONTIER as BLK158_NEXT_FRONTIER,
    RTM_RECORD_ID as BLK158_RTM_RECORD_ID,
    REQUIRED_FALSE_FLAGS as BLK158_REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS as BLK158_REQUIRED_TRUE_FLAGS,
)
from metadata_bound_rtm_generation_decision_request import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

CANONICAL_BLK158_EXECUTION_PACKAGE_HASH = "sha256:ebb20362dde1e3a2e47ed7e40586c03b77b5176e20e7d17c8559c74ef1784cfe"
CANONICAL_BLK158_RTM_RECORD_HASH = "sha256:b13953535945223b480f156218bb68e53be82fff6d36f72a68ad7eae62674480"

RECONCILIATION_PACKAGE_ID_159 = "POST-RTM-GENERATION-RECONCILIATION-159-001"
REQUEST_PACKAGE_ID_160 = "METADATA-TRACE-CLOSURE-AUTHORITY-REQUEST-160-001"
EXECUTION_PACKAGE_ID_161 = "METADATA-TRACE-CLOSURE-EXECUTION-161-001"
TRACE_CLOSURE_RECORD_ID_161 = "METADATA-TRACE-CLOSURE-RECORD-161-001"
POST_EXECUTION_REVIEW_ID_162 = "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001"
RUN_ID_161 = "RUN-BLK-SYSTEM-161-METADATA-TRACE-CLOSURE-001"
APPROVAL_ID_161 = "APPROVAL-BLK-SYSTEM-161-METADATA-TRACE-CLOSURE-001"
EXACT_OPERATOR_APPROVAL_TEXT_161 = (
    "Approve METADATA-TRACE-CLOSURE-AUTHORITY-REQUEST-160-001 for BLK-SYSTEM-161 "
    "exact bounded metadata trace-closure execution only."
)

NEXT_FRONTIER_159 = "NEXT_FRONTIER_METADATA_TRACE_CLOSURE_AUTHORITY_REQUEST_NOT_GRANTED"
NEXT_FRONTIER_160 = "NEXT_FRONTIER_METADATA_TRACE_CLOSURE_APPROVAL_NOT_GRANTED"
NEXT_FRONTIER_161 = "NEXT_FRONTIER_POST_METADATA_TRACE_CLOSURE_REVIEW_NOT_GRANTED"
NEXT_FRONTIER_162 = "NEXT_FRONTIER_HARDENING_OR_OPERATOR_SELECTED_AUTHORITY_NOT_GRANTED"

REQUIRED_FALSE_FLAGS = (
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted",
    "protected_body_scan_attempted",
    "rtm_generation_beyond_exact_record",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_executed",
    "signer_storage_ledger_reuse_authorized",
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

_BASE_EXCLUDED = {
    "RTM_GENERATION_BEYOND_EXACT_PRIOR_RECORD",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION_BEYOND_EXACT_RECORD",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "REUSABLE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_AUTHORITY",
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

EXACT_EXCLUDED_AUTHORITIES_159 = _BASE_EXCLUDED | {"TRACE_CLOSURE_APPROVAL_CAPTURE", "TRACE_CLOSURE_EXECUTION"}
EXACT_EXCLUDED_AUTHORITIES_160 = _BASE_EXCLUDED | {"APPROVAL_CAPTURE_THIS_SPRINT", "FUTURE_RUN_ID_CONSUMPTION_THIS_SPRINT", "TRACE_CLOSURE_EXECUTION_THIS_SPRINT"}
EXACT_EXCLUDED_AUTHORITIES_161 = _BASE_EXCLUDED | {"APPROVAL_RETARGETING_OR_SCOPE_EXPANSION", "RUN_ID_REUSE_WITHOUT_SEPARATE_REPLAY_LEDGER_AUTHORITY"}
EXACT_EXCLUDED_AUTHORITIES_162 = _BASE_EXCLUDED | {"NEXT_FRONTIER_APPROVAL_CAPTURE", "NEXT_FRONTIER_EXECUTION"}

_PROOF_159 = {
    "BLK158_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK158_RTM_RECORD_HASH_BOUND",
    "METADATA_ONLY_TRACE_IDENTITIES_RECONCILED",
    "NO_PROTECTED_BODY_READS_OR_SCANS",
    "NO_DRIFT_REJECTION_OR_COVERAGE_TRUTH",
    "NEXT_REQUEST_REQUIRED_NOT_GRANTED",
}
_PROOF_160 = {
    "BLK159_RECONCILIATION_PACKAGE_HASH_BOUND",
    "REQUEST_ONLY_NO_APPROVAL_CAPTURE",
    "REQUEST_ONLY_NO_RUN_ID_CONSUMPTION",
    "METADATA_TRACE_CLOSURE_SCOPE_ONLY",
    "NO_PROTECTED_BODY_READS_OR_SCANS",
    "NO_DRIFT_REJECTION_OR_COVERAGE_TRUTH",
}
_PROOF_161 = {
    "BLK160_REQUEST_PACKAGE_HASH_BOUND",
    "EXPLICIT_OPERATOR_APPROVAL_TEXT_MATCHES_EXACT_BLK160_REQUEST",
    "RUN_ID_ASSIGNED_AND_CONSUMED_INSIDE_RECORD_ONLY_EVIDENCE",
    "METADATA_TRACE_CLOSURE_RECORD_EMITTED",
    "EXECUTION_REQUEST_WINDOW_HASH_BOUND",
    "NO_PROTECTED_BODY_READS_OR_SCANS",
    "NO_DRIFT_REJECTION_OR_COVERAGE_TRUTH",
}
_PROOF_162 = {
    "BLK161_EXECUTION_PACKAGE_HASH_BOUND",
    "BLK161_TRACE_CLOSURE_RECORD_HASH_BOUND",
    "POST_EXECUTION_RECORD_REVIEWED",
    "NEXT_FRONTIER_SELECTED_NOT_GRANTED",
    "NO_PROTECTED_BODY_READS_OR_SCANS",
    "NO_DRIFT_REJECTION_OR_COVERAGE_TRUTH",
}


def valid_post_generation_reconciliation_context_159(upstream: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    context = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_159,
        "operator_identity": upstream["operator_identity"],
        "selected_frontier": "post_metadata_rtm_generation_reconciliation",
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "upstream_rtm_record_id": upstream["rtm_record_id"],
        "upstream_rtm_record_hash": upstream["rtm_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "metadata_trace_identities_match": True,
        "reconciliation_result": "CLEAN_METADATA_RTM_GENERATION_RECONCILED_NEXT_REQUEST_REQUIRED",
        "next_frontier": NEXT_FRONTIER_159,
        "next_frontier_granted": False,
        "reviewed_at": "2099-05-16T14:10:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_159),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_159),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def build_post_generation_reconciliation_159(upstream: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    source = _validate_blk158_execution(upstream)
    ctx = _validate_reconciliation_context_159(context, source)
    package = {
        "reconciliation_status": "POST_RTM_GENERATION_RECONCILIATION_COMPLETE_RECORD_ONLY",
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID_159,
        "operator_identity": ctx["operator_identity"],
        "selected_frontier": ctx["selected_frontier"],
        "upstream_execution_package_id": source["execution_package_id"],
        "upstream_execution_package_hash": source["execution_package_hash"],
        "upstream_rtm_record_id": source["rtm_record_id"],
        "upstream_rtm_record_hash": source["rtm_record_hash"],
        "beo_id": source["beo_id"],
        "beb_id": source["beb_id"],
        "exact_trace_identities": list(source["exact_trace_identities"]),
        "metadata_trace_identities_match": True,
        "reconciliation_result": ctx["reconciliation_result"],
        "next_frontier": NEXT_FRONTIER_159,
        "next_frontier_granted": False,
        "reviewed_at": ctx["reviewed_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_159),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_159),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["reconciliation_context_hash"] = _canonical_hash(ctx)
    package["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    return package


def valid_trace_closure_authority_request_160(rec159: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    request = {
        "request_package_id": REQUEST_PACKAGE_ID_160,
        "operator_identity": rec159["operator_identity"],
        "request_scope": "REQUEST_ONLY_METADATA_TRACE_CLOSURE_AFTER_BLK159_NO_EXECUTION",
        "selected_frontier": "metadata_trace_closure_authority_request",
        "requested_authority": "ONE_FUTURE_EXACT_METADATA_TRACE_CLOSURE_APPROVAL",
        "upstream_reconciliation_package_id": rec159["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": rec159["reconciliation_package_hash"],
        "beo_id": rec159["beo_id"],
        "beb_id": rec159["beb_id"],
        "exact_trace_identities": list(rec159["exact_trace_identities"]),
        "request_future_exact_trace_closure_approval": True,
        "approval_capture_performed": False,
        "future_run_id_consumed": False,
        "next_frontier": NEXT_FRONTIER_160,
        "requested_at": "2099-05-16T14:20:00+10:00",
        "expires_at": "2099-05-16T15:20:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_160),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_160),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def build_trace_closure_authority_request_160(rec159: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_reconciliation_package_159(rec159)
    req = _validate_request_160(request, upstream)
    package = {
        "request_status": "METADATA_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_NOT_APPROVED",
        "request_package_id": REQUEST_PACKAGE_ID_160,
        "operator_identity": req["operator_identity"],
        "request_scope": req["request_scope"],
        "selected_frontier": req["selected_frontier"],
        "requested_authority": req["requested_authority"],
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "request_future_exact_trace_closure_approval": True,
        "approval_capture_performed": False,
        "future_run_id_consumed": False,
        "next_frontier": NEXT_FRONTIER_160,
        "authority_request_hash": _canonical_hash(req),
        "requested_at": req["requested_at"],
        "expires_at": req["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_160),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_160),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["request_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"})
    return package


def valid_trace_closure_execution_request_161(request160: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    request = {
        "execution_package_id": EXECUTION_PACKAGE_ID_161,
        "operator_identity": request160["operator_identity"],
        "execution_scope": "EXACT_BLK160_METADATA_TRACE_CLOSURE_EXECUTION_RECORD_ONLY",
        "selected_frontier": "metadata_trace_closure_execution_record",
        "upstream_request_package_id": request160["request_package_id"],
        "upstream_request_package_hash": request160["request_package_hash"],
        "upstream_authority_request_hash": request160["authority_request_hash"],
        "approval_id": APPROVAL_ID_161,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_161,
        "run_id": RUN_ID_161,
        "beo_id": request160["beo_id"],
        "beb_id": request160["beb_id"],
        "exact_trace_identities": list(request160["exact_trace_identities"]),
        "execute_metadata_trace_closure": True,
        "requested_at": "2099-05-16T14:30:00+10:00",
        "expires_at": "2099-05-16T15:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_161),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_161),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def build_trace_closure_execution_161(request160: dict[str, Any], execution_request: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_request_package_160(request160)
    req = _validate_execution_request_161(execution_request, upstream)
    trace_record = {
        "trace_closure_record_id": TRACE_CLOSURE_RECORD_ID_161,
        "closure_mode": "METADATA_TRACE_CLOSURE_RECORD_ONLY",
        "consumed_run_id": RUN_ID_161,
        "approval_id": APPROVAL_ID_161,
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "trace_identities": list(upstream["exact_trace_identities"]),
        "metadata_trace_closure_executed": True,
        "recorded_at": req["requested_at"],
    }
    for flag in REQUIRED_FALSE_FLAGS:
        trace_record[flag] = False
    trace_record["trace_closure_record_hash"] = _canonical_hash({k: v for k, v in trace_record.items() if k != "trace_closure_record_hash"})
    package = {
        "execution_status": "METADATA_TRACE_CLOSURE_EXECUTED_FOR_EXACT_BLK160_REQUEST_RECORD_ONLY",
        "execution_package_id": EXECUTION_PACKAGE_ID_161,
        "operator_identity": req["operator_identity"],
        "execution_scope": req["execution_scope"],
        "selected_frontier": req["selected_frontier"],
        "upstream_request_package_id": upstream["request_package_id"],
        "upstream_request_package_hash": upstream["request_package_hash"],
        "upstream_authority_request_hash": upstream["authority_request_hash"],
        "approval_id": APPROVAL_ID_161,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT_161,
        "approval_capture_performed": True,
        "metadata_trace_closure_executed": True,
        "run_id_consumed": RUN_ID_161,
        "run_id_consumed_in_record": True,
        "execution_request_hash": _canonical_hash(req),
        "requested_at": req["requested_at"],
        "expires_at": req["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "trace_closure_record_id": TRACE_CLOSURE_RECORD_ID_161,
        "trace_closure_record": trace_record,
        "trace_closure_record_hash": trace_record["trace_closure_record_hash"],
        "next_frontier": NEXT_FRONTIER_161,
        "proof_obligations": sorted(_PROOF_161),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_161),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"})
    return package


def valid_post_trace_closure_review_context_162(execution161: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    context = {
        "review_package_id": POST_EXECUTION_REVIEW_ID_162,
        "operator_identity": execution161["operator_identity"],
        "selected_frontier": "post_metadata_trace_closure_review",
        "upstream_execution_package_id": execution161["execution_package_id"],
        "upstream_execution_package_hash": execution161["execution_package_hash"],
        "upstream_trace_closure_record_id": execution161["trace_closure_record_id"],
        "upstream_trace_closure_record_hash": execution161["trace_closure_record_hash"],
        "beo_id": execution161["beo_id"],
        "beb_id": execution161["beb_id"],
        "exact_trace_identities": list(execution161["exact_trace_identities"]),
        "review_result": "CLEAN_METADATA_TRACE_CLOSURE_REVIEWED_NEXT_FRONTIER_NOT_GRANTED",
        "next_frontier": NEXT_FRONTIER_162,
        "next_frontier_granted": False,
        "reviewed_at": "2099-05-16T15:10:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_162),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_162),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def build_post_trace_closure_review_162(execution161: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_execution_package_161(execution161)
    ctx = _validate_review_context_162(context, upstream)
    package = {
        "review_status": "POST_METADATA_TRACE_CLOSURE_REVIEW_COMPLETE_NOT_AUTHORITY",
        "review_package_id": POST_EXECUTION_REVIEW_ID_162,
        "operator_identity": ctx["operator_identity"],
        "selected_frontier": ctx["selected_frontier"],
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["trace_closure_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "review_result": ctx["review_result"],
        "next_frontier": NEXT_FRONTIER_162,
        "next_frontier_granted": False,
        "reviewed_at": ctx["reviewed_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "proof_obligations": sorted(_PROOF_162),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_162),
    }
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["review_context_hash"] = _canonical_hash(ctx)
    package["review_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "review_package_hash"})
    return package


def _validate_blk158_execution(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-158 execution package must be a dictionary")
    submitted = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    recomputed = _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"})
    if submitted != recomputed:
        raise ValueError("execution_package_hash does not match submitted BLK-158 package")
    if submitted != CANONICAL_BLK158_EXECUTION_PACKAGE_HASH:
        raise ValueError("canonical BLK-158 execution package required")
    if _required_hash(package.get("rtm_record_hash"), "rtm_record_hash") != CANONICAL_BLK158_RTM_RECORD_HASH:
        raise ValueError("canonical BLK-158 RTM record hash required")
    expected = {
        "execution_status": BLK158_EXECUTION_STATUS,
        "execution_package_id": BLK158_EXECUTION_PACKAGE_ID,
        "rtm_record_id": BLK158_RTM_RECORD_ID,
        "next_frontier": BLK158_NEXT_FRONTIER,
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("canonical BLK-158 execution package required")
    for flag in BLK158_REQUIRED_TRUE_FLAGS:
        if package.get(flag) is not True:
            raise ValueError(f"BLK-158 {flag} must be true")
    for flag in BLK158_REQUIRED_FALSE_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-158 {flag} must remain false")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    _required_exact_set(package.get("proof_obligations"), BLK158_PROOF_OBLIGATIONS, "BLK-158 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), BLK158_EXCLUDED_AUTHORITIES, "BLK-158 excluded_authorities")
    return deepcopy(package)


def _validate_reconciliation_context_159(context: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "reconciliation_package_id", "operator_identity", "selected_frontier", "upstream_execution_package_id",
        "upstream_execution_package_hash", "upstream_rtm_record_id", "upstream_rtm_record_hash", "beo_id", "beb_id",
        "exact_trace_identities", "metadata_trace_identities_match", "reconciliation_result", "next_frontier",
        "next_frontier_granted", "reviewed_at", "expired", "replayed", "stale", "proof_obligations", "excluded_authorities", *REQUIRED_FALSE_FLAGS,
    }
    ctx = _validate_common_context(context, keys)
    _require_exact(ctx, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_159)
    _require_exact(ctx, "selected_frontier", "post_metadata_rtm_generation_reconciliation")
    _expect_from(ctx, upstream, {
        "operator_identity": "operator_identity", "upstream_execution_package_id": "execution_package_id",
        "upstream_execution_package_hash": "execution_package_hash", "upstream_rtm_record_id": "rtm_record_id",
        "upstream_rtm_record_hash": "rtm_record_hash", "beo_id": "beo_id", "beb_id": "beb_id", "exact_trace_identities": "exact_trace_identities",
    })
    if ctx.get("metadata_trace_identities_match") is not True:
        raise ValueError("metadata_trace_identities_match must be true")
    _require_exact(ctx, "reconciliation_result", "CLEAN_METADATA_RTM_GENERATION_RECONCILED_NEXT_REQUEST_REQUIRED")
    _require_exact(ctx, "next_frontier", NEXT_FRONTIER_159)
    _required_exact_set(ctx.get("proof_obligations"), _PROOF_159, "proof_obligations")
    _required_exact_set(ctx.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_159, "excluded_authorities")
    return ctx


def _validate_reconciliation_package_159(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-159 reconciliation package must be a dictionary")
    submitted = _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    if submitted != _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"}):
        raise ValueError("reconciliation_package_hash does not match submitted BLK-159 package")
    _require_exact(package, "reconciliation_package_id", RECONCILIATION_PACKAGE_ID_159)
    _require_exact(package, "next_frontier", NEXT_FRONTIER_159)
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_159, "excluded_authorities")
    return deepcopy(package)


def _validate_request_160(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "request_package_id", "operator_identity", "request_scope", "selected_frontier", "requested_authority",
        "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash", "beo_id", "beb_id", "exact_trace_identities",
        "request_future_exact_trace_closure_approval", "approval_capture_performed", "future_run_id_consumed", "next_frontier",
        "requested_at", "expires_at", "expired", "replayed", "stale", "proof_obligations", "excluded_authorities", *REQUIRED_FALSE_FLAGS,
    }
    req = _validate_common_context(request, keys)
    _require_exact(req, "request_package_id", REQUEST_PACKAGE_ID_160)
    _require_exact(req, "request_scope", "REQUEST_ONLY_METADATA_TRACE_CLOSURE_AFTER_BLK159_NO_EXECUTION")
    _require_exact(req, "selected_frontier", "metadata_trace_closure_authority_request")
    _require_exact(req, "requested_authority", "ONE_FUTURE_EXACT_METADATA_TRACE_CLOSURE_APPROVAL")
    _expect_from(req, upstream, {"operator_identity": "operator_identity", "upstream_reconciliation_package_id": "reconciliation_package_id", "upstream_reconciliation_package_hash": "reconciliation_package_hash", "beo_id": "beo_id", "beb_id": "beb_id", "exact_trace_identities": "exact_trace_identities"})
    if req.get("request_future_exact_trace_closure_approval") is not True:
        raise ValueError("request_future_exact_trace_closure_approval must be true")
    for flag in ("approval_capture_performed", "future_run_id_consumed"):
        if req.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    _require_exact(req, "next_frontier", NEXT_FRONTIER_160)
    _validate_window(req, None, "request")
    _required_exact_set(req.get("proof_obligations"), _PROOF_160, "proof_obligations")
    _required_exact_set(req.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_160, "excluded_authorities")
    return req


def _validate_request_package_160(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-160 request package must be a dictionary")
    submitted = _required_hash(package.get("request_package_hash"), "request_package_hash")
    if submitted != _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"}):
        raise ValueError("request_package_hash does not match submitted BLK-160 package")
    _require_exact(package, "request_package_id", REQUEST_PACKAGE_ID_160)
    _require_exact(package, "next_frontier", NEXT_FRONTIER_160)
    if package.get("approval_capture_performed") is not False or package.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-160 request package must not capture approval or consume run ID")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_160, "excluded_authorities")
    return deepcopy(package)


def _validate_execution_request_161(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "execution_package_id", "operator_identity", "execution_scope", "selected_frontier", "upstream_request_package_id",
        "upstream_request_package_hash", "upstream_authority_request_hash", "approval_id", "operator_approval_text_raw", "run_id",
        "beo_id", "beb_id", "exact_trace_identities", "execute_metadata_trace_closure", "requested_at", "expires_at", "expired", "replayed", "stale", "proof_obligations", "excluded_authorities", *REQUIRED_FALSE_FLAGS,
    }
    req = _validate_common_context(request, keys)
    _require_exact(req, "execution_package_id", EXECUTION_PACKAGE_ID_161)
    _require_exact(req, "execution_scope", "EXACT_BLK160_METADATA_TRACE_CLOSURE_EXECUTION_RECORD_ONLY")
    _require_exact(req, "selected_frontier", "metadata_trace_closure_execution_record")
    _require_exact(req, "approval_id", APPROVAL_ID_161)
    _require_exact(req, "run_id", RUN_ID_161)
    if req.get("operator_approval_text_raw") != EXACT_OPERATOR_APPROVAL_TEXT_161:
        _scan_value_strings({"operator_approval_text_raw": req.get("operator_approval_text_raw")}, "execution_request", allow_selected=True)
        raise ValueError("operator approval text must match exact BLK-SYSTEM-161 approval sentence")
    _expect_from(req, upstream, {"operator_identity": "operator_identity", "upstream_request_package_id": "request_package_id", "upstream_request_package_hash": "request_package_hash", "upstream_authority_request_hash": "authority_request_hash", "beo_id": "beo_id", "beb_id": "beb_id", "exact_trace_identities": "exact_trace_identities"})
    if req.get("execute_metadata_trace_closure") is not True:
        raise ValueError("execute_metadata_trace_closure must be true")
    _validate_window(req, upstream, "execution")
    _required_exact_set(req.get("proof_obligations"), _PROOF_161, "proof_obligations")
    _required_exact_set(req.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_161, "excluded_authorities")
    return req


def _validate_execution_package_161(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-161 execution package must be a dictionary")
    submitted = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    if submitted != _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"}):
        raise ValueError("execution_package_hash does not match submitted BLK-161 package")
    _require_exact(package, "execution_package_id", EXECUTION_PACKAGE_ID_161)
    _require_exact(package, "trace_closure_record_id", TRACE_CLOSURE_RECORD_ID_161)
    _required_hash(package.get("trace_closure_record_hash"), "trace_closure_record_hash")
    for flag in REQUIRED_FALSE_FLAGS:
        if package.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(package)


def _validate_review_context_162(context: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "review_package_id", "operator_identity", "selected_frontier", "upstream_execution_package_id", "upstream_execution_package_hash",
        "upstream_trace_closure_record_id", "upstream_trace_closure_record_hash", "beo_id", "beb_id", "exact_trace_identities",
        "review_result", "next_frontier", "next_frontier_granted", "reviewed_at", "expired", "replayed", "stale", "proof_obligations", "excluded_authorities", *REQUIRED_FALSE_FLAGS,
    }
    ctx = _validate_common_context(context, keys)
    _require_exact(ctx, "review_package_id", POST_EXECUTION_REVIEW_ID_162)
    _require_exact(ctx, "selected_frontier", "post_metadata_trace_closure_review")
    _expect_from(ctx, upstream, {"operator_identity": "operator_identity", "upstream_execution_package_id": "execution_package_id", "upstream_execution_package_hash": "execution_package_hash", "upstream_trace_closure_record_id": "trace_closure_record_id", "upstream_trace_closure_record_hash": "trace_closure_record_hash", "beo_id": "beo_id", "beb_id": "beb_id", "exact_trace_identities": "exact_trace_identities"})
    _require_exact(ctx, "review_result", "CLEAN_METADATA_TRACE_CLOSURE_REVIEWED_NEXT_FRONTIER_NOT_GRANTED")
    _require_exact(ctx, "next_frontier", NEXT_FRONTIER_162)
    _required_exact_set(ctx.get("proof_obligations"), _PROOF_162, "proof_obligations")
    _required_exact_set(ctx.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_162, "excluded_authorities")
    return ctx


def _validate_common_context(value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("context must be a dictionary")
    unknown = sorted(set(value) - keys)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(keys - set(value))
    if missing:
        raise ValueError(f"missing field {missing[0]!r}")
    normalized = deepcopy(value)
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    if normalized.get("next_frontier_granted") not in {None, False}:
        raise ValueError("next_frontier_granted must remain false")
    for flag in REQUIRED_FALSE_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    return normalized


def _require_exact(mapping: dict[str, Any], key: str, expected: str) -> None:
    if mapping.get(key) == expected:
        return
    _scan_value_strings({key: mapping.get(key)}, "metadata_ladder", allow_selected=True)
    raise ValueError(f"{key} must be {expected}")


def _expect_from(candidate: dict[str, Any], upstream: dict[str, Any], mapping: dict[str, str]) -> None:
    for key, upstream_key in mapping.items():
        if candidate.get(key) != upstream.get(upstream_key):
            raise ValueError(f"{key} must match upstream {upstream_key}")


def _validate_window(candidate: dict[str, Any], upstream: dict[str, Any] | None, label: str) -> None:
    requested_at = _parse_timestamp(candidate.get("requested_at"), f"{label} requested_at")
    expires_at = _parse_timestamp(candidate.get("expires_at"), f"{label} expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if requested_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError(f"{label} request must not be calendar-expired")
    if upstream is not None:
        upstream_requested_at = _parse_timestamp(upstream.get("requested_at"), "upstream requested_at")
        upstream_expires_at = _parse_timestamp(upstream.get("expires_at"), "upstream expires_at")
        if requested_at < upstream_requested_at:
            raise ValueError(f"{label} request must not predate upstream request")
        if expires_at > upstream_expires_at:
            raise ValueError(f"{label} request window must end within upstream request expiry")
