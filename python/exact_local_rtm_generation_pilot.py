"""Exact local RTM generation pilot bound to BLK-089 approval.

The fixture consumes one exact future-run ID from the BLK-SYSTEM-089 approval
decision and emits deterministic local RTM evidence. It remains local-only and
non-authoritative: no drift rejection, protected-body reads, external ledger
mutation, signer/storage access, target/source/Git mutation, or runtime tooling.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_generation_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT as BLK089_DECISION_RESULT,
    EXACT_EXCLUDED_AUTHORITIES as BLK089_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK089_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID as BLK089_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK089_NEXT_REQUIRED_AUTHORITY,
    SIDE_EFFECT_FLAGS as BLK089_SIDE_EFFECT_FLAGS,
    STATUS as BLK089_STATUS,
    _scan_string,
)
from rtm_authority_request_after_beo_pilot import (
    _enforce_exact_keys,
    _parse_timestamp,
    _required_false,
    _required_hash,
    _require_dict,
    _validate_exact_set,
)

EXECUTION_STATUS = "LOCAL_RTM_GENERATION_PILOT_EXECUTED_FOR_EXACT_BLK089_APPROVAL"
EXECUTION_PACKAGE_ID = "RTM-GENERATION-PILOT-EXECUTION-090-001"
RUN_ID_CONSUMED = "RUN-BLK-SYSTEM-088-RTM-GENERATION-001"
RTM_ID = "RTM-090-001"
SELECTED_FRONTIER = "exact_local_rtm_generation_pilot"
EXECUTION_SCOPE = "EXACT_LOCAL_RTM_GENERATION_PILOT_ONLY"
NEXT_REQUIRED_AUTHORITY = "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED"

SIDE_EFFECT_FLAGS = (
    "drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "protected_body_reads",
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
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "PROTECTED_BLK_REQ_BODY_READ",
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
    "BLK089_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
    "APPROVAL_INTERVAL_BOUND_TO_EXECUTION_WINDOW",
    "RUN_ID_CONSUMED_EXACTLY_ONCE_IN_LOCAL_FIXTURE",
    "LOCAL_RTM_LEDGER_HASH_BOUND",
    "BEO_AND_TRACE_HASH_EVIDENCE_BOUND",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "FUTURE_DRIFT_REJECTION_AUTHORITY_REQUEST_REQUIRED",
}

_APPROVAL_REQUIRED_KEYS = {
    "approval_decision_status",
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "decision_result",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "pilot_publication_artifact_hash",
    "trace_artifacts",
    "pilot_publication_artifact",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "approval_id",
    "future_run_id",
    "decided_at",
    "expires_at",
    "approval_decision_captured",
    "human_rtm_generation_approval_granted",
    "future_local_rtm_generation_pilot_approved",
    "future_run_id_consumed",
    "rtm_status",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "approval_decision_package_hash",
    *BLK089_SIDE_EFFECT_FLAGS,
}

_REQUEST_KEYS = {
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id_to_consume",
    "rtm_id",
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

_ATTESTATION_KEYS = {
    "exact_blk089_approval_reviewed",
    "run_id_consumed_once_for_local_rtm_generation",
    "local_rtm_generation_only_not_external_ledger",
    "drift_rejection_excluded",
    "protected_body_reads_excluded",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}


def build_exact_local_rtm_generation_pilot(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    trace_artifacts = deepcopy(approval["trace_artifacts"])
    pilot_artifact = deepcopy(approval["pilot_publication_artifact"])
    ledger_body = {
        "rtm_id": RTM_ID,
        "rtm_status": "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE",
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "pilot_publication_artifact_hash": approval["pilot_publication_artifact_hash"],
        "trace_artifacts": deepcopy(trace_artifacts),
        "hash_binding_mode": "LOCAL_HASH_ONLY_NO_PROTECTED_BODY_READS",
        "drift_review_state": "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
        "external_ledger_state": "NOT_APPENDED_LOCAL_FIXTURE_ONLY",
        "protected_body_reads": False,
        "drift_rejection_authorized": False,
        "drift_decision_made": False,
    }
    local_ledger = {**ledger_body, "rtm_ledger_hash": _canonical_hash(ledger_body)}
    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_decision_package_hash": approval["approval_decision_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "upstream_authority_request_package_id": approval["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": approval["upstream_authority_request_package_hash"],
        "upstream_execution_package_id": approval["upstream_execution_package_id"],
        "upstream_execution_package_hash": approval["upstream_execution_package_hash"],
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "pilot_publication_artifact_hash": approval["pilot_publication_artifact_hash"],
        "trace_artifacts": trace_artifacts,
        "pilot_publication_artifact": pilot_artifact,
        "rtm_id": RTM_ID,
        "rtm_status": "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE",
        "rtm_authority": "EXACT_LOCAL_PILOT_ONLY",
        "local_rtm_ledger": local_ledger,
        "rtm_ledger_hash": local_ledger["rtm_ledger_hash"],
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


def _validate_approval_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "approval_package")
    _enforce_exact_keys(package, _APPROVAL_REQUIRED_KEYS, "approval_package")
    package_hash = _required_hash(package.get("approval_decision_package_hash"), "approval_decision_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("approval_decision_package_hash does not match submitted BLK-089 package")
    if package.get("approval_decision_status") != BLK089_STATUS:
        raise ValueError("approval package must be BLK-089 approval decision")
    if package.get("approval_decision_package_id") != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError("approval_decision_package_id must match BLK-089")
    if package.get("approval_id") != APPROVAL_ID or package.get("future_run_id") != BLK089_FUTURE_RUN_ID:
        raise ValueError("approval package must carry exact BLK-089 approval/run IDs")
    if package.get("decision_result") != BLK089_DECISION_RESULT:
        raise ValueError("approval package must approve one future local RTM generation pilot")
    if package.get("rtm_status") != "APPROVAL_DECISION_CAPTURED_NOT_GENERATED" or package.get("rtm_generated") is not False:
        raise ValueError("BLK-089 approval decision must not already generate RTM")
    if package.get("future_run_id_consumed") is not False:
        raise ValueError("BLK-089 approval future run ID must not be consumed yet")
    if package.get("next_required_authority") != BLK089_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-089 package must require exact local RTM generation pilot")
    for flag in BLK089_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), BLK089_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK089_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    return package


def _validate_execution_request(request: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_exact_keys(request, _REQUEST_KEYS, "execution_request")
    if request.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if request.get("operator_identity") != approval["operator_identity"]:
        _scan_string(str(request.get("operator_identity")), "operator_identity")
        raise ValueError("operator_identity must match BLK-089 approval package")
    _scan_string(request["operator_identity"], "operator_identity")
    if request.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if request.get("approval_decision_package_id") != approval["approval_decision_package_id"]:
        raise ValueError("approval_decision_package_id must match BLK-089 approval package")
    if request.get("approval_decision_package_hash") != approval["approval_decision_package_hash"]:
        raise ValueError("approval_decision_package_hash must match BLK-089 approval package")
    if request.get("approval_id") != approval["approval_id"]:
        raise ValueError("approval_id must match BLK-089 approval package")
    if request.get("run_id_to_consume") != approval["future_run_id"] or request.get("run_id_to_consume") != RUN_ID_CONSUMED:
        raise ValueError("run_id_to_consume must match approved BLK-089 future run ID")
    if request.get("rtm_id") != RTM_ID:
        raise ValueError(f"rtm_id must match {RTM_ID}")
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    decided_at = _parse_timestamp(approval["decided_at"], "approval.decided_at")
    approval_expires_at = _parse_timestamp(approval["expires_at"], "approval.expires_at")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if requested_at < decided_at:
        raise ValueError("requested_at must not precede approval decision")
    if requested_at >= approval_expires_at:
        raise ValueError("requested_at must be before approval expiry")
    if expires_at > approval_expires_at:
        raise ValueError("execution window must not exceed approval expiry")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(request.get(flag), flag)
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
