"""BLK-SYSTEM-134 production blk-link / RTM trace-closure approval capture.

This deterministic fixture captures the human/operator approval decision for the
exact BLK-SYSTEM-133 production blk-link / RTM trace-closure authority request.
It reserves one future production trace-closure run ID but does not consume that
run, execute production or reusable blk-link, generate RTM, reject drift, compare
active-vault hashes, establish coverage truth, read protected bodies, mutate
target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim
production isolation.
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
from production_blk_link_rtm_trace_closure_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK133_AUTHORITY_REQUEST_PACKAGE_ID,
    CANONICAL_BLK132_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH,
    EXACT_EXCLUDED_AUTHORITIES as BLK133_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK133_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK133_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK133_REQUEST_SCOPE,
    REQUEST_STATUS as BLK133_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK133_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK133_SIDE_EFFECT_FLAGS,
)

STATUS = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURED_FOR_EXACT_BLK133_REQUEST_NOT_EXECUTED"
APPROVAL_CAPTURE_PACKAGE_ID = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-133-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"
SELECTED_FRONTIER = "production_blk_link_rtm_trace_closure_approval_capture"
DECISION_SCOPE = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_ONLY_NOT_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_REQUIRED_NOT_RUN"
CANONICAL_BLK133_REQUEST_PACKAGE_HASH = "sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271"
CANONICAL_BLK133_AUTHORITY_REQUEST_HASH = "sha256:6e74b6fbf64cb6188d6601b4c3434b199f6cbfe5529033bd54cc9767e7dbf158"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T14:28:54+10:00")

SIDE_EFFECT_FLAGS = (
    "production_blk_link_rtm_trace_closure_executed",
    "production_blk_link_authorized_beyond_exact_future_run",
    "future_run_id_consumed",
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
    "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_THIS_SPRINT",
    "PRODUCTION_OR_REUSABLE_BLK_LINK_EXECUTION_BEYOND_EXACT_FUTURE_RUN",
    "RUNTIME_RTM_GENERATION_THIS_SPRINT",
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
    "BLK133_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK132_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK133",
    "BLK132_TRACE_CLOSURE_RECORD_IDENTITY_AND_HASH_BOUND_THROUGH_BLK133",
    "BLK131_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK132",
    "HUMAN_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK133_PRODUCTION_TRACE_CLOSURE_REQUEST",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "PRODUCTION_TRACE_CLOSURE_NOT_EXECUTED_BY_APPROVAL_CAPTURE",
    "RTM_GENERATION_NOT_PERFORMED_BY_APPROVAL_CAPTURE",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_PRODUCTION_TRACE_CLOSURE_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
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
        "requested_authority",
        "request_future_exact_production_blk_link_rtm_trace_closure_approval",
        "production_blk_link_rtm_trace_closure_authority",
        "approval_capture_performed",
        "production_blk_link_execution_performed",
        "rtm_trace_closure_executed",
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
        *BLK133_SIDE_EFFECT_FLAGS,
    }
)

_DECISION_KEYS = frozenset(
    {
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "approval_id",
        "future_run_id",
        "decision_result",
        "decided_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_approval_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk133_request_reviewed",
        "approval_limited_to_one_future_production_blk_link_rtm_trace_closure_execution",
        "future_run_id_reserved_not_consumed",
        "production_trace_closure_not_executed_by_this_decision",
        "rtm_generation_not_performed_by_this_decision",
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


def build_production_blk_link_rtm_trace_closure_approval_capture(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Capture exact BLK-SYSTEM-134 approval for the BLK-133 request only."""

    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    trace_identities = list(request["exact_trace_identities"])
    decision_hash = _canonical_hash(decision)
    package = {
        "approval_capture_status": STATUS,
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": request["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": request["upstream_trace_closure_record_hash"],
        "publication_record_hash": request["publication_record_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "exact_trace_identities": trace_identities,
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decision_hash": decision_hash,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "approval_decision_captured": True,
        "future_production_blk_link_rtm_trace_closure_execution_approved": True,
        "production_blk_link_rtm_trace_closure_executed": False,
        "future_run_id_consumed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_approval_text_raw": decision["operator_approval_text_raw"],
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_capture_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_capture_package_hash"}
    )
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"request_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"request_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("authority_request_package_hash"), "authority_request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "authority_request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-133 package")
    if submitted_hash != CANONICAL_BLK133_REQUEST_PACKAGE_HASH:
        raise ValueError("request package must match canonical BLK-133 authority request")
    expected = {
        "request_status": BLK133_REQUEST_STATUS,
        "authority_request_package_id": BLK133_AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": BLK133_REQUEST_SCOPE,
        "selected_frontier": BLK133_SELECTED_FRONTIER,
        "upstream_execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-001",
        "upstream_execution_package_hash": CANONICAL_BLK132_EXECUTION_PACKAGE_HASH,
        "upstream_trace_closure_record_id": "RTM-TRACE-CLOSURE-RECORD-132-001",
        "upstream_trace_closure_record_hash": CANONICAL_BLK132_TRACE_CLOSURE_RECORD_HASH,
        "upstream_approval_capture_package_id": "RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001",
        "upstream_approval_capture_package_hash": "sha256:c41c8bd4e7b5aba387a0db5b439d9bb664a1610f70eaff50488ed6cceabbbba0",
        "upstream_authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001",
        "upstream_authority_request_package_hash": "sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2",
        "publication_record_hash": "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "requested_authority": "ONE_FUTURE_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
        "production_blk_link_rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": BLK133_NEXT_REQUIRED_AUTHORITY,
        "authority_request_hash": CANONICAL_BLK133_AUTHORITY_REQUEST_HASH,
        "approval_capture_performed": False,
        "production_blk_link_execution_performed": False,
        "rtm_trace_closure_executed": False,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("request package must match canonical BLK-133 authority request")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("request package trace identities must match canonical BLK-133 request")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("request package trace identities must match canonical BLK-133 request")
    if normalized.get("request_future_exact_production_blk_link_rtm_trace_closure_approval") is not True:
        raise ValueError("BLK-133 request must request future production trace-closure approval")
    for flag in BLK133_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"request package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK133_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK133_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    return normalized


def _validate_decision(decision: Any, request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise ValueError("approval_decision must be a dictionary")
    unknown = sorted(set(decision) - _DECISION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_DECISION_KEYS - set(decision))
    if missing:
        raise ValueError(f"approval_decision missing field {missing[0]!r}")
    normalized = deepcopy(decision)
    for key in (
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "approval_id",
        "future_run_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("approval_capture_package_id") != APPROVAL_CAPTURE_PACKAGE_ID:
        raise ValueError(f"approval_capture_package_id must be {APPROVAL_CAPTURE_PACKAGE_ID}")
    if normalized.get("operator_identity") != request["operator_identity"]:
        raise ValueError("operator_identity must match BLK-133 request package")
    if normalized.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    expected = {
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": request["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": request["upstream_trace_closure_record_hash"],
        "publication_record_hash": request["publication_record_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-133 request package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != request["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-133 request package")
    if normalized.get("approval_id") != APPROVAL_ID:
        raise ValueError(f"approval_id must be {APPROVAL_ID}")
    if normalized.get("future_run_id") != FUTURE_RUN_ID:
        raise ValueError(f"future_run_id must be {FUTURE_RUN_ID}")
    if normalized.get("decision_result") != DECISION_RESULT:
        raise ValueError(f"decision_result must be {DECISION_RESULT}")
    _scan_value_strings(normalized.get("decision_result"), "decision_result")
    _scan_value_strings(normalized.get("operator_approval_text_raw"), "operator_approval_text_raw")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(normalized.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    request_start = _parse_timestamp(request.get("requested_at"), "request.requested_at")
    request_expiry = _parse_timestamp(request.get("expires_at"), "request.expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    if decided_at < request_start:
        raise ValueError("approval decision must not predate BLK-133 request")
    if decided_at >= request_expiry or expires_at > request_expiry:
        raise ValueError("decision window must end within BLK-133 request expiry")
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
