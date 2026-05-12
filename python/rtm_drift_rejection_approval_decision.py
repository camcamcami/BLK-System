"""RTM drift-rejection approval-decision capture for the exact BLK-091 request.

This fixture records a human approval decision for one future local RTM
drift-rejection execution sprint. It does not execute drift rejection, make a
drift decision, compare active-vault hashes, read protected BLK-req bodies, or
mutate any external ledger/storage/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_authority_request_after_beo_pilot import (
    _enforce_exact_keys,
    _parse_timestamp,
    _required_false,
    _required_hash,
    _require_dict,
    _validate_exact_set,
)
from rtm_drift_rejection_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK091_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES as BLK091_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK091_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK091_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK091_REQUEST_SCOPE,
    REQUEST_STATUS as BLK091_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK091_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK091_SIDE_EFFECT_FLAGS,
)
from rtm_generation_approval_decision import _scan_string

STATUS = "RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK091_REQUEST_NOT_EXECUTED"
APPROVAL_DECISION_PACKAGE_ID = "RTM-DRIFT-REJECTION-APPROVAL-DECISION-093-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-091-RTM-DRIFT-REJECTION-001"
SELECTED_FRONTIER = "rtm_drift_rejection_approval_decision_capture"
DECISION_SCOPE = "RTM_DRIFT_REJECTION_APPROVAL_DECISION_ONLY_NOT_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_LOCAL_RTM_DRIFT_REJECTION_EXECUTION_REQUIRED_NOT_RUN"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T00:00:00+10:00")
CANONICAL_BLK091_AUTHORITY_REQUEST_PACKAGE_HASH = (
    "sha256:88e1065154ede742ca16178bd1f0fb17f3aba5bca0f145fa47317866038b933b"
)
CANONICAL_BLK091_OPERATOR_IDENTITY = "discord:684235178083745819"
CANONICAL_BLK091_UPSTREAM_RTM_GENERATION_PACKAGE_ID = "RTM-GENERATION-PILOT-EXECUTION-090-001"
CANONICAL_BLK091_RTM_ID = "RTM-090-001"
CANONICAL_BLK091_BEO_ID = "BEO-054-001"
CANONICAL_BLK091_TARGET_ID = "BEO-PUBLICATION-TARGET-055-001"

SIDE_EFFECT_FLAGS = (
    "rtm_drift_rejection_executed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "protected_body_reads",
    "protected_body_hashing",
    "authoritative_external_publication",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_test_codex_blk_pipe_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "RTM_DRIFT_REJECTION_EXECUTION_THIS_SPRINT",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "PROTECTED_BLK_REQ_BODY_READ",
    "PROTECTED_BODY_HASHING",
    "AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION",
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
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK091_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "HUMAN_RTM_DRIFT_REJECTION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK091_RTM_DRIFT_REJECTION",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "LOCAL_RTM_LEDGER_EVIDENCE_INHERITED_BY_HASH_ONLY",
    "DRIFT_REJECTION_NOT_EXECUTED_BY_APPROVAL_DECISION",
    "DRIFT_DECISION_NOT_MADE_BY_APPROVAL_DECISION",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_RTM_DRIFT_REJECTION_EXECUTION",
}

_REQUEST_PACKAGE_REQUIRED_KEYS = {
    "request_status",
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_rtm_generation_package_id",
    "upstream_rtm_generation_package_hash",
    "rtm_id",
    "rtm_ledger_hash",
    "local_rtm_ledger",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "drift_rejection_authority",
    "request_future_exact_drift_rejection_authority",
    "human_drift_rejection_approval_required",
    "human_drift_rejection_approval_granted",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "authority_request_package_hash",
    *BLK091_SIDE_EFFECT_FLAGS,
}

_DECISION_KEYS = {
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "approval_id",
    "future_run_id",
    "decision_result",
    "decided_at",
    "expires_at",
    "expired",
    "replayed",
    "stale",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    *SIDE_EFFECT_FLAGS,
}

_ATTESTATION_KEYS = {
    "exact_blk091_request_reviewed",
    "approval_limited_to_one_future_local_drift_rejection_execution",
    "drift_rejection_not_executed_by_this_decision",
    "no_drift_decision_made_by_this_decision",
    "protected_body_reads_excluded",
    "external_ledger_and_signer_storage_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_REQUEST_ATTESTATION_KEYS = {
    "exact_blk090_rtm_generation_package_reviewed",
    "local_rtm_ledger_evidence_bound",
    "drift_rejection_is_requested_for_future_review_not_granted",
    "no_drift_rejection_or_drift_decision_performed",
    "protected_body_reads_excluded",
    "external_ledger_and_signer_storage_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}


def build_rtm_drift_rejection_approval_decision(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    local_ledger = deepcopy(request["local_rtm_ledger"])
    operator_attestation = deepcopy(decision["operator_attestation"])
    package = {
        "approval_decision_status": STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "decision_result": DECISION_RESULT,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_rtm_generation_package_id": request["upstream_rtm_generation_package_id"],
        "upstream_rtm_generation_package_hash": request["upstream_rtm_generation_package_hash"],
        "rtm_id": request["rtm_id"],
        "rtm_ledger_hash": request["rtm_ledger_hash"],
        "local_rtm_ledger": local_ledger,
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "target_id": request["target_id"],
        "target_ref": request["target_ref"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_rtm_drift_rejection_approval_granted": True,
        "future_local_rtm_drift_rejection_execution_approved": True,
        "future_run_id_consumed": False,
        "drift_rejection_status": "APPROVAL_DECISION_CAPTURED_NOT_EXECUTED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": operator_attestation,
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_decision_package_hash"}
    )
    return package


def _validate_request_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "request_package")
    _enforce_exact_keys(package, _REQUEST_PACKAGE_REQUIRED_KEYS, "request_package")
    package_hash = _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("authority_request_package_hash does not match submitted BLK-091 package")
    if package.get("operator_identity") != CANONICAL_BLK091_OPERATOR_IDENTITY:
        raise ValueError("operator_identity must match canonical BLK-091 request package")
    if package.get("upstream_rtm_generation_package_id") != CANONICAL_BLK091_UPSTREAM_RTM_GENERATION_PACKAGE_ID:
        raise ValueError("upstream_rtm_generation_package_id must match canonical BLK-091 package")
    if package.get("rtm_id") != CANONICAL_BLK091_RTM_ID:
        raise ValueError("rtm_id must match canonical BLK-091 package")
    if package.get("beo_id") != CANONICAL_BLK091_BEO_ID:
        raise ValueError("beo_id must match canonical BLK-091 package")
    if package.get("target_id") != CANONICAL_BLK091_TARGET_ID:
        raise ValueError("target_id must match canonical BLK-091 package")
    if package.get("request_status") != BLK091_REQUEST_STATUS:
        raise ValueError("request package must be BLK-091 drift-rejection request-ready")
    if package.get("authority_request_package_id") != BLK091_REQUEST_PACKAGE_ID:
        raise ValueError("authority_request_package_id must match BLK-091")
    if package.get("request_scope") != BLK091_REQUEST_SCOPE:
        raise ValueError("request_scope must remain BLK-091 request-only")
    if package.get("selected_frontier") != BLK091_SELECTED_FRONTIER:
        raise ValueError("selected_frontier must remain BLK-091 request frontier")
    if package.get("drift_rejection_authority") != "DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED":
        raise ValueError("BLK-091 request must not already grant drift authority")
    if package.get("request_future_exact_drift_rejection_authority") is not True:
        raise ValueError("BLK-091 request must ask for future drift-rejection review")
    if package.get("human_drift_rejection_approval_required") is not True:
        raise ValueError("BLK-091 request must require human drift approval")
    if package.get("human_drift_rejection_approval_granted") is not False:
        raise ValueError("BLK-091 request must not already grant drift approval")
    if package.get("next_required_authority") != BLK091_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-091 request must still require drift-rejection approval")
    ledger = _require_dict(package.get("local_rtm_ledger"), "local_rtm_ledger")
    _validate_local_rtm_ledger(ledger, package)
    ledger_hash = _required_hash(package.get("rtm_ledger_hash"), "rtm_ledger_hash")
    expected_ledger_hash = _canonical_hash({key: value for key, value in ledger.items() if key != "rtm_ledger_hash"})
    if ledger.get("rtm_ledger_hash") != ledger_hash or ledger_hash != expected_ledger_hash:
        raise ValueError("rtm_ledger_hash does not match submitted local RTM ledger")
    for flag in BLK091_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_request_attestation(package.get("operator_attestation"))
    _validate_exact_set(package.get("proof_obligations"), BLK091_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK091_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    if package_hash != CANONICAL_BLK091_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("authority_request_package_hash must match canonical BLK-091 package")
    return package


def _validate_local_rtm_ledger(ledger: dict[str, Any], package: dict[str, Any]) -> None:
    allowed = {
        "rtm_id",
        "rtm_status",
        "beo_id",
        "beo_hash",
        "target_id",
        "target_ref",
        "pilot_publication_artifact_hash",
        "trace_artifacts",
        "hash_binding_mode",
        "drift_review_state",
        "external_ledger_state",
        "protected_body_reads",
        "drift_rejection_authorized",
        "drift_decision_made",
        "rtm_ledger_hash",
    }
    _enforce_exact_keys(ledger, allowed, "local_rtm_ledger")
    expected = {
        "rtm_id": package["rtm_id"],
        "rtm_status": "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE",
        "beo_id": package["beo_id"],
        "beo_hash": package["beo_hash"],
        "target_id": package["target_id"],
        "target_ref": package["target_ref"],
        "hash_binding_mode": "LOCAL_HASH_ONLY_NO_PROTECTED_BODY_READS",
        "drift_review_state": "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
        "external_ledger_state": "NOT_APPENDED_LOCAL_FIXTURE_ONLY",
        "protected_body_reads": False,
        "drift_rejection_authorized": False,
        "drift_decision_made": False,
    }
    for key, value in expected.items():
        if ledger.get(key) != value:
            raise ValueError("local_rtm_ledger must remain no-drift no-protected-body evidence")


def _validate_decision(decision: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(decision, "approval_decision")
    _enforce_exact_keys(decision, _DECISION_KEYS, "approval_decision")
    if decision.get("approval_decision_package_id") != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError(f"approval_decision_package_id must be {APPROVAL_DECISION_PACKAGE_ID}")
    if decision.get("operator_identity") != request["operator_identity"]:
        _scan_string(str(decision.get("operator_identity")), "operator_identity")
        raise ValueError("operator_identity must match BLK-091 request package")
    _scan_string(decision["operator_identity"], "operator_identity")
    if decision.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if decision.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if decision.get("upstream_authority_request_package_id") != request["authority_request_package_id"]:
        raise ValueError("upstream_authority_request_package_id must match BLK-091 request package")
    if decision.get("upstream_authority_request_package_hash") != request["authority_request_package_hash"]:
        raise ValueError("upstream_authority_request_package_hash must match BLK-091 request package")
    consumed_ids = {
        request["authority_request_package_id"],
        request["upstream_rtm_generation_package_id"],
        request["rtm_id"],
        request["beo_id"],
        request["target_id"],
    }
    if decision.get("approval_id") in consumed_ids:
        raise ValueError("approval_id must be fresh")
    if decision.get("future_run_id") in consumed_ids or decision.get("future_run_id") == decision.get("approval_id"):
        raise ValueError("future_run_id must be fresh")
    if decision.get("approval_id") != APPROVAL_ID:
        raise ValueError(f"approval_id must be {APPROVAL_ID}")
    if decision.get("future_run_id") != FUTURE_RUN_ID:
        raise ValueError(f"future_run_id must be {FUTURE_RUN_ID}")
    if decision.get("decision_result") != DECISION_RESULT:
        raise ValueError(f"decision_result must be {DECISION_RESULT}")
    for flag in ["expired", "replayed", "stale"]:
        if decision.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(decision.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(decision.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(decision.get(flag), flag)
    _validate_attestation(decision.get("operator_attestation"))
    _validate_exact_set(decision.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(decision.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return decision


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _validate_request_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "request_package.operator_attestation")
    _enforce_exact_keys(attestation, _REQUEST_ATTESTATION_KEYS, "request_package.operator_attestation")
    for key in _REQUEST_ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"request_package.operator_attestation.{key} must be true")
