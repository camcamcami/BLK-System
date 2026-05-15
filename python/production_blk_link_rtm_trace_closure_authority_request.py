"""BLK-SYSTEM-133 production blk-link / RTM trace-closure authority request.

This deterministic fixture consumes the exact BLK-SYSTEM-132 local,
non-authoritative RTM trace-closure execution record and emits one request-only
package for a future production blk-link / RTM trace-closure approval-capture
sprint. It does not capture approval, execute production or reusable blk-link,
generate RTM, reject drift, compare active-vault hashes, establish coverage
truth, read protected bodies, mutate target/source/Git state, run
BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_local_rtm_trace_closure_execution_record import (
    EXACT_EXCLUDED_AUTHORITIES as BLK132_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK132_PROOF_OBLIGATIONS,
    EXECUTION_PACKAGE_ID as BLK132_EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE as BLK132_EXECUTION_SCOPE,
    EXECUTION_STATUS as BLK132_EXECUTION_STATUS,
    RUN_ID_CONSUMED as BLK132_RUN_ID_CONSUMED,
    SELECTED_FRONTIER as BLK132_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK132_SIDE_EFFECT_FLAGS,
    TRACE_CLOSURE_RECORD_ID as BLK132_TRACE_CLOSURE_RECORD_ID,
)
from metadata_bound_rtm_trace_closure_approval_capture import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

REQUEST_STATUS = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_BLK132_LOCAL_RECORD_NOT_GRANTED"
AUTHORITY_REQUEST_PACKAGE_ID = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001"
SELECTED_FRONTIER = "production_blk_link_rtm_trace_closure_authority_request_after_local_record"
REQUEST_SCOPE = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_BLK132_LOCAL_RECORD_REVIEW_ONLY"
NEXT_REQUIRED_AUTHORITY = "EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_REQUIRED_NOT_CAPTURED"
CANONICAL_BLK132_EXECUTION_PACKAGE_HASH = "sha256:548934403cd71a4eebc27c4e164a43f9e2d7f71b8cfab7765b1f51e65f44fed5"
CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH = "sha256:2b78924d8d839dff65c2137cabf09362a23feec24fa21010238ef8c48703c3ca"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T13:05:32+10:00")

SIDE_EFFECT_FLAGS = (
    "production_blk_link_rtm_trace_closure_approval_captured",
    "production_blk_link_rtm_trace_closure_authorized",
    "production_rtm_trace_closure_executed",
    "production_blk_link_authorized",
    "production_blk_link_executed",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
    "PRODUCTION_OR_REUSABLE_BLK_LINK_EXECUTION",
    "PRODUCTION_RTM_TRACE_CLOSURE_EXECUTION",
    "RUNTIME_RTM_GENERATION",
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
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK132_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK132_TRACE_CLOSURE_RECORD_IDENTITY_AND_HASH_BOUND",
    "BLK131_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK132",
    "BLK130_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK131",
    "BLK129_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK130",
    "LOCAL_NON_AUTHORITATIVE_RECORD_CONSUMED_AS_PREREQUISITE_ONLY",
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_REQUESTED_FOR_FUTURE_REVIEW_NOT_CAPTURED",
    "PRODUCTION_BLK_LINK_EXECUTION_NOT_AUTHORIZED",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_PRODUCTION_TRACE_CLOSURE_APPROVAL_CAPTURE",
}

_REQUEST_KEYS = frozenset(
    {
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "upstream_approval_capture_package_id",
        "upstream_approval_capture_package_hash",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "request_future_exact_production_blk_link_rtm_trace_closure_approval",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk132_local_execution_record_reviewed",
        "local_non_authoritative_record_consumed_as_prerequisite_only",
        "request_is_for_future_production_blk_link_rtm_trace_closure_approval_not_approval",
        "approval_capture_not_performed",
        "production_blk_link_not_executed",
        "rtm_generation_not_performed",
        "drift_rejection_excluded",
        "active_vault_hash_comparison_excluded",
        "coverage_truth_excluded",
        "protected_body_reads_excluded",
        "public_ledger_mutation_excluded",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)

_BLK132_REQUIRED_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_consumed",
        "future_run_id_consumed",
        "execution_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "trace_closure_record_id",
        "trace_closure_record",
        "trace_closure_record_hash",
        "local_rtm_trace_closure_record_emitted",
        "rtm_trace_closure_status",
        "next_required_authority",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "execution_package_hash",
        *BLK132_SIDE_EFFECT_FLAGS,
    }
)


def build_production_blk_link_rtm_trace_closure_authority_request(
    blk132_execution_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a BLK-SYSTEM-133 request package from the exact BLK-132 local record."""

    upstream = _validate_blk132_execution_package(blk132_execution_package)
    request = _validate_authority_request(authority_request, upstream)
    trace_identities = list(upstream["exact_trace_identities"])
    authority_request_hash = _canonical_hash(request)
    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["trace_closure_record_hash"],
        "upstream_approval_capture_package_id": upstream["approval_capture_package_id"],
        "upstream_approval_capture_package_hash": upstream["approval_capture_package_hash"],
        "upstream_authority_request_package_id": upstream["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["upstream_authority_request_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "requested_authority": "ONE_FUTURE_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
        "request_future_exact_production_blk_link_rtm_trace_closure_approval": True,
        "production_blk_link_rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "approval_capture_performed": False,
        "production_blk_link_execution_performed": False,
        "rtm_trace_closure_executed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "authority_request_hash": authority_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


def _validate_blk132_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("blk132_execution_package must be a dictionary")
    unknown = sorted(set(package) - _BLK132_REQUIRED_KEYS)
    if unknown:
        raise ValueError(f"blk132_execution_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_BLK132_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"blk132_execution_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("execution_package_hash"), "execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("execution_package_hash does not match submitted BLK-132 package")
    if submitted_hash != CANONICAL_BLK132_EXECUTION_PACKAGE_HASH:
        raise ValueError("package must match canonical BLK-132 local trace-closure execution record")
    expected = {
        "execution_status": BLK132_EXECUTION_STATUS,
        "execution_package_id": BLK132_EXECUTION_PACKAGE_ID,
        "execution_scope": BLK132_EXECUTION_SCOPE,
        "selected_frontier": BLK132_SELECTED_FRONTIER,
        "approval_capture_package_id": "RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001",
        "approval_capture_package_hash": "sha256:c41c8bd4e7b5aba387a0db5b439d9bb664a1610f70eaff50488ed6cceabbbba0",
        "run_id_consumed": BLK132_RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "upstream_authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001",
        "upstream_authority_request_package_hash": "sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2",
        "upstream_execution_package_id": "BEO-PUBLICATION-EXECUTION-129-001",
        "upstream_execution_package_hash": "sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c",
        "publication_record_hash": "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "trace_closure_record_id": BLK132_TRACE_CLOSURE_RECORD_ID,
        "trace_closure_record_hash": CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH,
        "local_rtm_trace_closure_record_emitted": True,
        "rtm_trace_closure_status": "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_ONLY",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("package must match canonical BLK-132 local trace-closure execution record")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("exact_trace_identities must match canonical BLK-132 trace metadata")
    trace_record = normalized.get("trace_closure_record")
    if not isinstance(trace_record, dict):
        raise ValueError("trace_closure_record must be a dictionary")
    if trace_record.get("trace_closure_record_id") != BLK132_TRACE_CLOSURE_RECORD_ID:
        raise ValueError("trace_closure_record_id must match canonical BLK-132 trace closure record")
    if trace_record.get("trace_closure_record_hash") != CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH:
        raise ValueError("trace_closure_record_hash must match canonical BLK-132 trace closure record")
    recomputed_record_hash = _canonical_hash({key: value for key, value in trace_record.items() if key != "trace_closure_record_hash"})
    if recomputed_record_hash != CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH:
        raise ValueError("trace_closure_record_hash does not match submitted BLK-132 trace closure record")
    if trace_record.get("local_record_authority") != "LOCAL_NON_AUTHORITATIVE_EVIDENCE_ONLY":
        raise ValueError("BLK-132 trace closure record must remain local non-authoritative evidence")
    _required_exact_set(normalized.get("proof_obligations"), BLK132_PROOF_OBLIGATIONS, "blk132 proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK132_EXCLUDED_AUTHORITIES, "blk132 excluded_authorities")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-132 package must not be {flag}")
    for flag in BLK132_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-132 package {flag} must remain false")
    for flag in (
        "production_blk_link_authorized",
        "production_blk_link_executed",
        "rtm_generated",
        "rtm_drift_rejection_performed",
        "active_vault_hash_comparison_performed",
        "coverage_truth_established",
        "protected_body_reads",
        "public_ledger_mutation",
    ):
        if trace_record.get(flag) is not False:
            raise ValueError(f"BLK-132 trace closure record {flag} must remain false")
    return normalized


def _validate_authority_request(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
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
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "upstream_approval_capture_package_id",
        "upstream_approval_capture_package_hash",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("authority_request_package_id") != AUTHORITY_REQUEST_PACKAGE_ID:
        raise ValueError(f"authority_request_package_id must be {AUTHORITY_REQUEST_PACKAGE_ID}")
    if normalized.get("operator_identity") != upstream["operator_identity"]:
        raise ValueError("operator_identity must match BLK-132 execution package")
    if normalized.get("request_scope") != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    expected = {
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "upstream_trace_closure_record_id": upstream["trace_closure_record_id"],
        "upstream_trace_closure_record_hash": upstream["trace_closure_record_hash"],
        "upstream_approval_capture_package_id": upstream["approval_capture_package_id"],
        "upstream_approval_capture_package_hash": upstream["approval_capture_package_hash"],
        "upstream_authority_request_package_id": upstream["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": upstream["upstream_authority_request_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match canonical BLK-132 execution package")
    if normalized.get("exact_trace_identities") != upstream["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match canonical BLK-132 execution package")
    if normalized.get("request_future_exact_production_blk_link_rtm_trace_closure_approval") is not True:
        raise ValueError("request_future_exact_production_blk_link_rtm_trace_closure_approval must be true")
    for flag in SIDE_EFFECT_FLAGS:
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
    normalized["operator_attestation"] = _validate_attestation(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(
        normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations"
    )
    normalized["excluded_authorities"] = _required_exact_set(
        normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities"
    )
    return normalized


def _validate_attestation(value: Any) -> dict[str, bool]:
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
