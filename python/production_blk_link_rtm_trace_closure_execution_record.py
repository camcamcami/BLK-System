"""BLK-SYSTEM-135 production blk-link / RTM trace-closure execution record.

This deterministic fixture consumes the exact BLK-SYSTEM-134 approval capture and
reserved run ID, then emits record-only production blk-link / RTM trace-closure
evidence for that exact run. It does not generate RTM, reject drift, compare
active-vault hashes, establish coverage truth, read protected bodies, mutate
target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, perform
signer/storage/ledger behavior, or claim production isolation.
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
from production_blk_link_rtm_trace_closure_approval_capture import (
    APPROVAL_CAPTURE_PACKAGE_ID as BLK134_APPROVAL_CAPTURE_PACKAGE_ID,
    APPROVAL_ID as BLK134_APPROVAL_ID,
    DECISION_RESULT as BLK134_DECISION_RESULT,
    DECISION_SCOPE as BLK134_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as BLK134_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK134_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID as BLK134_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK134_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK134_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK134_SIDE_EFFECT_FLAGS,
    STATUS as BLK134_STATUS,
)

EXECUTION_STATUS = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_RECORDED_FOR_EXACT_BLK134_APPROVAL_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-EXECUTION-135-001"
EXECUTION_RECORD_ID = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-135-001"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-135-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"
SELECTED_FRONTIER = "production_blk_link_rtm_trace_closure_execution_record"
EXECUTION_SCOPE = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION_RECORD_ONLY_EXACT_APPROVED_RUN"
NEXT_REQUIRED_AUTHORITY = "POST_EXECUTION_RECONCILIATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK134_APPROVAL_CAPTURE_PACKAGE_HASH = "sha256:284bd944f7e854a9c589e923908053da37e27ce9c32d841090578837111e49bf"
CANONICAL_BLK134_DECISION_HASH = "sha256:9487b2433a4b5a53ea056f7d8d1257a0292ce8cfab31c989d9de3d4bed4c31ba"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T15:08:33+10:00")

SIDE_EFFECT_FLAGS = (
    "reusable_blk_link_authority_granted",
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
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
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
    "BLK134_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND",
    "BLK133_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK134",
    "BLK132_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK133",
    "BLK132_TRACE_CLOSURE_RECORD_IDENTITY_AND_HASH_BOUND_THROUGH_BLK133",
    "APPROVAL_ID_BOUND_TO_EXACT_BLK133_REQUEST",
    "RUN_ID_CONSUMED_EXACTLY_IN_RECORD_ONLY_EVIDENCE",
    "PRODUCTION_TRACE_CLOSURE_RECORD_EMITTED_FOR_EXACT_APPROVED_RUN",
    "REUSABLE_BLK_LINK_AUTHORITY_EXCLUDED",
    "RTM_GENERATION_NOT_PERFORMED_BY_EXECUTION_RECORD",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "POST_EXECUTION_RECONCILIATION_REQUIRED_BEFORE_NEXT_AUTHORITY_RUNG",
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
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
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
        "future_production_blk_link_rtm_trace_closure_execution_approved",
        "production_blk_link_rtm_trace_closure_executed",
        "future_run_id_consumed",
        "next_required_authority",
        "operator_approval_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "approval_capture_package_hash",
        *BLK134_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_REQUEST_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_to_consume",
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
        "exact_blk134_approval_reviewed",
        "reserved_run_id_consumed_once_in_execution_record",
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


def build_production_blk_link_rtm_trace_closure_execution_record(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Consume the exact BLK-135 run ID inside record-only production trace evidence."""

    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    trace_identities = list(approval["exact_trace_identities"])
    execution_request_hash = _canonical_hash(request)
    record = {
        "execution_record_id": EXECUTION_RECORD_ID,
        "consumed_run_id": RUN_ID_CONSUMED,
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "trace_closure_authority": "EXACT_APPROVED_PRODUCTION_TRACE_CLOSURE_RECORD_ONLY",
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
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
        "upstream_trace_closure_record_id": approval["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": approval["upstream_trace_closure_record_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": trace_identities,
        "execution_record_id": EXECUTION_RECORD_ID,
        "execution_record": record,
        "execution_record_hash": record["execution_record_hash"],
        "production_blk_link_rtm_trace_closure_record_emitted": True,
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
        raise ValueError("approval_capture_package_hash does not match submitted BLK-134 package")
    if submitted_hash != CANONICAL_BLK134_APPROVAL_CAPTURE_PACKAGE_HASH:
        raise ValueError("approval package must match canonical BLK-134 approval capture")
    expected = {
        "approval_capture_status": BLK134_STATUS,
        "approval_capture_package_id": BLK134_APPROVAL_CAPTURE_PACKAGE_ID,
        "decision_scope": BLK134_DECISION_SCOPE,
        "selected_frontier": BLK134_SELECTED_FRONTIER,
        "upstream_authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001",
        "upstream_authority_request_package_hash": "sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271",
        "upstream_execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-001",
        "upstream_execution_package_hash": "sha256:548934403cd71a4eebc27c4e164a43f9e2d7f71b8cfab7765b1f51e65f44fed5",
        "upstream_trace_closure_record_id": "RTM-TRACE-CLOSURE-RECORD-132-001",
        "upstream_trace_closure_record_hash": "sha256:2b78924d8d839dff65c2137cabf09362a23feec24fa21010238ef8c48703c3ca",
        "publication_record_hash": "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "approval_id": BLK134_APPROVAL_ID,
        "future_run_id": BLK134_FUTURE_RUN_ID,
        "decision_result": BLK134_DECISION_RESULT,
        "decision_hash": CANONICAL_BLK134_DECISION_HASH,
        "future_production_blk_link_rtm_trace_closure_execution_approved": True,
        "production_blk_link_rtm_trace_closure_executed": False,
        "future_run_id_consumed": False,
        "next_required_authority": BLK134_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("approval package must match canonical BLK-134 approval capture")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("approval package trace identities must match canonical BLK-134 approval")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("approval package trace identities must match canonical BLK-134 approval")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-134 approval package must not be {flag}")
    for flag in BLK134_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"approval package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK134_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK134_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    return normalized


def _validate_execution_request(request: Any, approval: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution_request must be a dictionary")
    unknown = sorted(set(request) - _EXECUTION_REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_REQUEST_KEYS - set(request))
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
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if normalized.get("operator_identity") != approval["operator_identity"]:
        raise ValueError("operator_identity must match BLK-134 approval package")
    if normalized.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if normalized.get("run_id_to_consume") != RUN_ID_CONSUMED:
        raise ValueError(f"run_id_to_consume must be {RUN_ID_CONSUMED}")
    expected = {
        "approval_capture_package_id": approval["approval_capture_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_to_consume": approval["future_run_id"],
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_execution_package_id": approval["upstream_execution_package_id"],
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": approval["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": approval["upstream_trace_closure_record_hash"],
        "publication_record_hash": approval["publication_record_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-134 approval package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != approval["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-134 approval package")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    approval_start = _parse_timestamp(approval.get("decided_at"), "approval.decided_at")
    approval_expiry = _parse_timestamp(approval.get("expires_at"), "approval.expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at < approval_start:
        raise ValueError("execution request must not predate BLK-134 approval")
    if requested_at >= approval_expiry or expires_at > approval_expiry:
        raise ValueError("execution window must end within BLK-134 approval expiry")
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
