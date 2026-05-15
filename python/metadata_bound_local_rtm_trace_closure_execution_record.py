"""BLK-SYSTEM-132 metadata-bound local RTM trace-closure execution record.

This deterministic fixture consumes the exact BLK-SYSTEM-131 approval-capture
package and reserved future run ID to emit one local, non-authoritative RTM
trace-closure record. It does not authorize production/reusable blk-link,
generate RTM, reject drift, compare active-vault hashes, establish coverage
truth, read protected bodies, mutate target/source/Git state, run
BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_trace_closure_approval_capture import (
    APPROVAL_CAPTURE_PACKAGE_ID as BLK131_APPROVAL_CAPTURE_PACKAGE_ID,
    APPROVAL_ID as BLK131_APPROVAL_ID,
    DECISION_RESULT as BLK131_DECISION_RESULT,
    DECISION_SCOPE as BLK131_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as BLK131_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK131_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID as BLK131_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK131_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK131_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK131_SIDE_EFFECT_FLAGS,
    STATUS as BLK131_STATUS,
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

EXECUTION_STATUS = "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_FOR_EXACT_BLK131_APPROVAL"
EXECUTION_PACKAGE_ID = "RTM-TRACE-CLOSURE-EXECUTION-132-001"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001"
TRACE_CLOSURE_RECORD_ID = "RTM-TRACE-CLOSURE-RECORD-132-001"
SELECTED_FRONTIER = "metadata_bound_local_rtm_trace_closure_execution_record"
EXECUTION_SCOPE = "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_EXECUTION_RECORD_ONLY"
NEXT_REQUIRED_AUTHORITY = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED"
CANONICAL_BLK131_APPROVAL_CAPTURE_PACKAGE_HASH = "sha256:c41c8bd4e7b5aba387a0db5b439d9bb664a1610f70eaff50488ed6cceabbbba0"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T12:28:50+10:00")

SIDE_EFFECT_FLAGS = (
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
    "BLK131_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND",
    "BLK130_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK131",
    "BLK129_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK130",
    "APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW",
    "EXECUTION_REQUEST_WINDOW_AND_HASH_BOUND",
    "RUN_ID_CONSUMED_IN_LOCAL_EVIDENCE_ONLY",
    "LOCAL_TRACE_CLOSURE_RECORD_HASH_BOUND",
    "LOCAL_RECORD_NON_AUTHORITATIVE_ONLY",
    "PRODUCTION_BLK_LINK_NOT_AUTHORIZED",
    "RTM_GENERATION_NOT_PERFORMED",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
}

_APPROVAL_PACKAGE_KEYS = frozenset(
    {
        "approval_capture_status",
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "approval_id",
        "future_run_id",
        "decision_result",
        "decision_hash",
        "decided_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "approval_decision_captured",
        "human_rtm_trace_closure_approval_granted",
        "future_local_rtm_trace_closure_execution_approved",
        "future_run_id_consumed",
        "next_required_authority",
        "operator_approval_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "approval_capture_package_hash",
        *BLK131_SIDE_EFFECT_FLAGS,
    }
)

_REQUEST_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_to_consume",
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
        "exact_blk131_approval_reviewed",
        "run_id_consumed_once_for_local_trace_closure_record",
        "local_trace_closure_record_only_not_production_blk_link",
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


def build_metadata_bound_local_rtm_trace_closure_execution_record(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Emit a local/non-authoritative trace-closure record for the exact BLK-131 approval."""

    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    trace_identities = list(approval["exact_trace_identities"])
    execution_request_hash = _canonical_hash(request)
    trace_record_body = {
        "trace_closure_record_id": TRACE_CLOSURE_RECORD_ID,
        "trace_closure_status": "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_ONLY",
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_execution_package_id": approval["upstream_execution_package_id"],
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": trace_identities,
        "run_id_consumed": RUN_ID_CONSUMED,
        "hash_binding_mode": "METADATA_HASH_ONLY_NO_ACTIVE_VAULT_COMPARISON_NO_PROTECTED_BODY_READS",
        "local_record_authority": "LOCAL_NON_AUTHORITATIVE_EVIDENCE_ONLY",
        "production_blk_link_authorized": False,
        "production_blk_link_executed": False,
        "rtm_generated": False,
        "rtm_generation_authorized": False,
        "rtm_drift_rejection_authorized": False,
        "rtm_drift_rejection_performed": False,
        "drift_decision_made": False,
        "active_vault_hash_comparison_performed": False,
        "coverage_claim_promoted": False,
        "coverage_matrix_generated": False,
        "coverage_truth_established": False,
        "protected_body_reads": False,
        "protected_body_copy_attempted": False,
        "protected_body_hashing_attempted": False,
        "signer_key_material_access": False,
        "cryptographic_signing": False,
        "immutable_storage_write": False,
        "public_ledger_mutation": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "blk_pipe_blk_test_codex_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
    }
    trace_closure_record = {
        **trace_record_body,
        "trace_closure_record_hash": _canonical_hash(trace_record_body),
    }
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "execution_request_hash": execution_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_execution_package_id": approval["upstream_execution_package_id"],
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": trace_identities,
        "trace_closure_record_id": TRACE_CLOSURE_RECORD_ID,
        "trace_closure_record": trace_closure_record,
        "trace_closure_record_hash": trace_closure_record["trace_closure_record_hash"],
        "local_rtm_trace_closure_record_emitted": True,
        "rtm_trace_closure_status": "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_ONLY",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


def _validate_approval_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("approval_package must be a dictionary")
    unknown = sorted(set(package) - _APPROVAL_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"approval_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_APPROVAL_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"approval_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("approval_capture_package_hash"), "approval_capture_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "approval_capture_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("approval_capture_package_hash does not match submitted BLK-131 package")
    if submitted_hash != CANONICAL_BLK131_APPROVAL_CAPTURE_PACKAGE_HASH:
        raise ValueError("approval package must match canonical BLK-131 approval capture")
    expected = {
        "approval_capture_status": BLK131_STATUS,
        "approval_capture_package_id": BLK131_APPROVAL_CAPTURE_PACKAGE_ID,
        "decision_scope": BLK131_DECISION_SCOPE,
        "selected_frontier": BLK131_SELECTED_FRONTIER,
        "upstream_authority_request_package_id": "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001",
        "upstream_authority_request_package_hash": "sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2",
        "upstream_execution_package_id": "BEO-PUBLICATION-EXECUTION-129-001",
        "upstream_execution_package_hash": "sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c",
        "publication_record_hash": "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "approval_id": BLK131_APPROVAL_ID,
        "future_run_id": BLK131_FUTURE_RUN_ID,
        "decision_result": BLK131_DECISION_RESULT,
        "next_required_authority": BLK131_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("approval package must match canonical BLK-131 approval capture")
    if normalized.get("approval_decision_captured") is not True:
        raise ValueError("approval decision must be captured")
    if normalized.get("human_rtm_trace_closure_approval_granted") is not True:
        raise ValueError("human RTM trace-closure approval must be captured")
    if normalized.get("future_local_rtm_trace_closure_execution_approved") is not True:
        raise ValueError("future local trace-closure execution must be approved")
    if normalized.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-131 approval must reserve but not consume future run id")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"approval package must not be {flag}")
    for flag in BLK131_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"approval package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK131_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK131_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    return normalized


def _validate_execution_request(request: Any, approval: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"execution_request missing field {missing[0]!r}")
    normalized = deepcopy(request)
    for key in (
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_to_consume",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if normalized.get("operator_identity") != approval["operator_identity"]:
        raise ValueError("operator_identity must match BLK-131 approval package")
    if normalized.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    expected = {
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_to_consume": approval["future_run_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-131 approval package")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    decided_at = _parse_timestamp(approval.get("decided_at"), "approval.decided_at")
    approval_expires = _parse_timestamp(approval.get("expires_at"), "approval.expires_at")
    if requested_at < decided_at:
        raise ValueError("execution request must not predate approval decision")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at >= approval_expires or expires_at > approval_expires:
        raise ValueError("execution request window must end within BLK-131 approval expiry")
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
