"""RTM drift-rejection authority request after local RTM generation evidence.

This fixture packages BLK-SYSTEM-090 local RTM generation evidence into a future
human-review request. It does not grant, approve, execute, or simulate drift
rejection, and it performs no protected-body reads or external side effects.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from exact_local_rtm_generation_pilot import (
    EXECUTION_PACKAGE_ID as BLK090_EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE as BLK090_EXECUTION_SCOPE,
    EXECUTION_STATUS as BLK090_EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK090_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK090_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK090_NEXT_REQUIRED_AUTHORITY,
    RTM_ID as BLK090_RTM_ID,
    SELECTED_FRONTIER as BLK090_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK090_SIDE_EFFECT_FLAGS,
)
from rtm_generation_approval_decision import _scan_string
from rtm_authority_request_after_beo_pilot import (
    _enforce_exact_keys,
    _parse_timestamp,
    _required_false,
    _required_hash,
    _require_dict,
    _validate_exact_set,
)

REQUEST_STATUS = "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_READY_AFTER_LOCAL_RTM_GENERATION_NOT_GRANTED"
AUTHORITY_REQUEST_PACKAGE_ID = "RTM-DRIFT-REJECTION-AUTHORITY-REQUEST-091-001"
SELECTED_FRONTIER = "rtm_drift_rejection_authority_request"
REQUEST_SCOPE = "RTM_DRIFT_REJECTION_AUTHORITY_REQUEST_REVIEW_ONLY"
NEXT_REQUIRED_AUTHORITY = "EXPLICIT_HUMAN_RTM_DRIFT_REJECTION_APPROVAL_REQUIRED_NOT_GRANTED"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")

SIDE_EFFECT_FLAGS = (
    "drift_rejection_approved",
    "drift_rejection_authorized",
    "drift_rejection_executed",
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
    "HUMAN_DRIFT_REJECTION_APPROVAL_CAPTURE",
    "RTM_DRIFT_REJECTION_EXECUTION",
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
    "BLK090_LOCAL_RTM_GENERATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "LOCAL_RTM_LEDGER_IDENTITY_AND_HASH_BOUND",
    "BEO_AND_TARGET_HASH_EVIDENCE_BOUND",
    "DRIFT_REJECTION_REQUESTED_FOR_REVIEW_NOT_GRANTED",
    "NO_DRIFT_REJECTION_OR_DRIFT_DECISION_PERFORMED",
    "PROTECTED_BODY_NO_READ_OR_HASH_GUARANTEE_BOUND",
    "EXTERNAL_LEDGER_SIGNER_STORAGE_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_DRIFT_APPROVAL",
}

_GENERATION_REQUIRED_KEYS = {
    "execution_status",
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id_consumed",
    "future_run_id_consumed",
    "upstream_authority_request_package_id",
    "upstream_authority_request_package_hash",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "pilot_publication_artifact_hash",
    "trace_artifacts",
    "pilot_publication_artifact",
    "rtm_id",
    "rtm_status",
    "rtm_authority",
    "local_rtm_ledger",
    "rtm_ledger_hash",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "execution_package_hash",
    *BLK090_SIDE_EFFECT_FLAGS,
}

_REQUEST_KEYS = {
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_rtm_generation_package_id",
    "upstream_rtm_generation_package_hash",
    "rtm_id",
    "rtm_ledger_hash",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "request_future_exact_drift_rejection_authority",
    "human_drift_rejection_approval_granted",
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
    "exact_blk090_rtm_generation_package_reviewed",
    "local_rtm_ledger_evidence_bound",
    "drift_rejection_is_requested_for_future_review_not_granted",
    "no_drift_rejection_or_drift_decision_performed",
    "protected_body_reads_excluded",
    "external_ledger_and_signer_storage_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}


def build_rtm_drift_rejection_authority_request(
    generation_package: dict[str, Any], drift_rejection_request: dict[str, Any]
) -> dict[str, Any]:
    generation = _validate_generation_package(generation_package)
    request = _validate_request(drift_rejection_request, generation)
    local_ledger = deepcopy(generation["local_rtm_ledger"])
    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_rtm_generation_package_id": generation["execution_package_id"],
        "upstream_rtm_generation_package_hash": generation["execution_package_hash"],
        "rtm_id": generation["rtm_id"],
        "rtm_ledger_hash": generation["rtm_ledger_hash"],
        "local_rtm_ledger": local_ledger,
        "beo_id": generation["beo_id"],
        "beo_hash": generation["beo_hash"],
        "target_id": generation["target_id"],
        "target_ref": generation["target_ref"],
        "drift_rejection_authority": "DRIFT_REJECTION_REQUEST_ONLY_NOT_GRANTED",
        "request_future_exact_drift_rejection_authority": True,
        "human_drift_rejection_approval_required": True,
        "human_drift_rejection_approval_granted": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
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


def _validate_generation_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "generation_package")
    _enforce_exact_keys(package, _GENERATION_REQUIRED_KEYS, "generation_package")
    package_hash = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-090 package")
    if package.get("execution_status") != BLK090_EXECUTION_STATUS:
        raise ValueError("generation package must be BLK-090 local RTM generation")
    if package.get("execution_package_id") != BLK090_EXECUTION_PACKAGE_ID:
        raise ValueError("generation package id must match BLK-090")
    if package.get("execution_scope") != BLK090_EXECUTION_SCOPE:
        raise ValueError("generation package must remain local-only")
    if package.get("selected_frontier") != BLK090_SELECTED_FRONTIER:
        raise ValueError("generation package selected_frontier must be exact local RTM generation")
    if package.get("rtm_id") != BLK090_RTM_ID:
        raise ValueError("generation package rtm_id must match BLK-090")
    if package.get("rtm_status") != "PILOT_LOCAL_RTM_LEDGER_GENERATED_NOT_AUTHORITATIVE":
        raise ValueError("generation package must contain local RTM ledger evidence")
    if package.get("rtm_authority") != "EXACT_LOCAL_PILOT_ONLY":
        raise ValueError("generation package must remain exact local pilot only")
    if package.get("next_required_authority") != BLK090_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("generation package must require drift-rejection authority request next")
    if package.get("drift_decision_made") is not False:
        raise ValueError("BLK-090 package must not already make drift decisions")
    ledger = _require_dict(package.get("local_rtm_ledger"), "local_rtm_ledger")
    _validate_local_rtm_ledger(ledger, package)
    ledger_hash = _required_hash(package.get("rtm_ledger_hash"), "rtm_ledger_hash")
    expected_ledger_hash = _canonical_hash({key: value for key, value in ledger.items() if key != "rtm_ledger_hash"})
    if ledger.get("rtm_ledger_hash") != ledger_hash or ledger_hash != expected_ledger_hash:
        raise ValueError("rtm_ledger_hash does not match submitted local RTM ledger")
    for flag in BLK090_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), BLK090_PROOF_OBLIGATIONS, "generation_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK090_EXCLUDED_AUTHORITIES, "generation_package excluded_authorities")
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
        "pilot_publication_artifact_hash": package["pilot_publication_artifact_hash"],
        "trace_artifacts": package["trace_artifacts"],
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


def _validate_request(request: dict[str, Any], generation: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "drift_rejection_request")
    _enforce_exact_keys(request, _REQUEST_KEYS, "drift_rejection_request")
    if request.get("authority_request_package_id") != AUTHORITY_REQUEST_PACKAGE_ID:
        raise ValueError(f"authority_request_package_id must be {AUTHORITY_REQUEST_PACKAGE_ID}")
    if request.get("operator_identity") != generation["operator_identity"]:
        _scan_string(str(request.get("operator_identity")), "operator_identity")
        raise ValueError("operator_identity must match BLK-090 generation package")
    _scan_string(request["operator_identity"], "operator_identity")
    if request.get("request_scope") != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if request.get("upstream_rtm_generation_package_id") != generation["execution_package_id"]:
        raise ValueError("upstream_rtm_generation_package_id must match BLK-090 generation package")
    if request.get("upstream_rtm_generation_package_hash") != generation["execution_package_hash"]:
        raise ValueError("upstream_rtm_generation_package_hash must match BLK-090 generation package")
    for key in ["rtm_id", "rtm_ledger_hash", "beo_id", "beo_hash", "target_id", "target_ref"]:
        if request.get(key) != generation[key]:
            raise ValueError(f"{key} must match BLK-090 generation package")
    if request.get("request_future_exact_drift_rejection_authority") is not True:
        raise ValueError("request_future_exact_drift_rejection_authority must be true")
    if request.get("human_drift_rejection_approval_granted") is not False:
        raise ValueError("human_drift_rejection_approval_granted must remain false")
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"drift rejection authority request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("drift rejection authority request must not be calendar-expired")
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
