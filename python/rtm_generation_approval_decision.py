"""RTM generation approval-decision capture for the exact BLK-088 request.

This fixture records a human approval decision for one future local RTM generation
pilot. It does not generate an RTM, reject drift, read protected BLK-req bodies,
write external ledgers, access signer/storage systems, mutate target/source/Git,
or run BLK-test/Codex/BLK-pipe.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from rtm_authority_request_after_beo_pilot import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK088_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES as BLK088_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK088_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK088_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK088_REQUEST_SCOPE,
    REQUEST_STATUS as BLK088_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK088_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK088_SIDE_EFFECT_FLAGS,
    _enforce_exact_keys,
    _normalize,
    _parse_timestamp,
    _required_false,
    _required_hash,
    _required_string,
    _require_dict,
    _validate_exact_set,
)

STATUS = "RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK088_REQUEST_NOT_GENERATED"
APPROVAL_DECISION_PACKAGE_ID = "RTM-GENERATION-APPROVAL-DECISION-089-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-088-RTM-GENERATION-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-088-RTM-GENERATION-001"
SELECTED_FRONTIER = "rtm_generation_approval_decision_capture"
DECISION_SCOPE = "RTM_GENERATION_APPROVAL_DECISION_ONLY_NOT_GENERATION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_LOCAL_RTM_GENERATION_PILOT_NOT_GENERATED"
NEXT_REQUIRED_AUTHORITY = "EXACT_LOCAL_RTM_GENERATION_PILOT_REQUIRED_NOT_RUN"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")

SIDE_EFFECT_FLAGS = (
    "rtm_generated",
    "rtm_generation_executed_this_sprint",
    "drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
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
    "RUNTIME_RTM_GENERATION_THIS_SPRINT",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ",
    "AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION",
    "LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE",
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
    "BLK088_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "HUMAN_RTM_GENERATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK088_RTM_GENERATION",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "LOCAL_BEO_PILOT_EVIDENCE_INHERITED_BY_HASH_ONLY",
    "RTM_NOT_GENERATED_BY_APPROVAL_DECISION",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_RTM_GENERATION_PILOT",
}

_REQUEST_PACKAGE_REQUIRED_KEYS = {
    "request_status",
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "run_id_consumed",
    "pilot_publication_artifact_hash",
    "trace_artifacts",
    "pilot_publication_artifact",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "source_evidence_hash",
    "local_pilot_beo_publication",
    "requested_authority",
    "request_future_exact_rtm_generation_authority",
    "human_rtm_approval_required",
    "rtm_status",
    "rtm_authority",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "authority_request_package_hash",
    *BLK088_SIDE_EFFECT_FLAGS,
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
    "exact_blk088_request_reviewed",
    "approval_limited_to_one_future_local_rtm_generation_pilot",
    "rtm_not_generated_by_this_decision",
    "drift_rejection_excluded",
    "protected_body_reads_excluded",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_FORBIDDEN_NORMALIZED_MARKERS = (
    "rtmgenerated",
    "rtmgenerationnow",
    "rtmgenerationexecuted",
    "rtmid",
    "rtmdriftrejection",
    "driftrejection",
    "driftdecision",
    "activevaulthashcomparison",
    "coverageclaim",
    "docsactive",
    "protectedbody",
    "authoritativebeopublication",
    "signaturegenerated",
    "cryptographicsigning",
    "signerkeymaterial",
    "keymaterial",
    "privatekey",
    "apikey",
    "immutablestoragewrite",
    "publicledgermutation",
    "rollbackexecuted",
    "targetreposcan",
    "targetrepomutation",
    "sourcemutationauthorized",
    "gitmutationauthorized",
    "bebdispatch",
    "beocloseoutexecution",
    "livecodexexecution",
    "approvalinherited",
    "blkpipeexecution",
    "blktestruntime",
    "packagemanagerauthorized",
    "networkaccessauthorized",
    "modelserviceauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionisolationclaimed",
)


def build_rtm_generation_approval_decision(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Build an exact RTM generation approval decision without generation."""

    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    operator_attestation = deepcopy(decision["operator_attestation"])
    trace_artifacts = deepcopy(request["trace_artifacts"])
    pilot_publication_artifact = deepcopy(request["pilot_publication_artifact"])
    package = {
        "approval_decision_status": STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "decision_result": DECISION_RESULT,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "pilot_publication_artifact_hash": request["pilot_publication_artifact_hash"],
        "trace_artifacts": trace_artifacts,
        "pilot_publication_artifact": pilot_publication_artifact,
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "target_id": request["target_id"],
        "target_ref": request["target_ref"],
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_rtm_generation_approval_granted": True,
        "future_local_rtm_generation_pilot_approved": True,
        "future_run_id_consumed": False,
        "rtm_status": "APPROVAL_DECISION_CAPTURED_NOT_GENERATED",
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
    if _required_string(package.get("request_status"), "request_status", scan=False) != BLK088_REQUEST_STATUS:
        raise ValueError("request package must be BLK-088 RTM authority request-ready")
    if package.get("authority_request_package_id") != BLK088_REQUEST_PACKAGE_ID:
        raise ValueError("authority_request_package_id must match BLK-088")
    if package.get("request_scope") != BLK088_REQUEST_SCOPE:
        raise ValueError("request_scope must remain BLK-088 request-only")
    if package.get("selected_frontier") != BLK088_SELECTED_FRONTIER:
        raise ValueError("selected_frontier must remain BLK-088 request frontier")
    package_hash = _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("authority_request_package_hash does not match submitted BLK-088 package")
    if package.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("BLK-088 request must remain not generated")
    if package.get("rtm_authority") != "REQUEST_ONLY_NOT_GRANTED":
        raise ValueError("BLK-088 request must not already grant RTM authority")
    if package.get("next_required_authority") != BLK088_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-088 request must still require RTM generation approval")
    for flag in BLK088_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), BLK088_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK088_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    return package


def _validate_decision(decision: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(decision, "approval_decision")
    _enforce_exact_keys(decision, _DECISION_KEYS, "approval_decision")
    if decision.get("approval_decision_package_id") != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError(f"approval_decision_package_id must be {APPROVAL_DECISION_PACKAGE_ID}")
    if decision.get("operator_identity") != request["operator_identity"]:
        _scan_string(str(decision.get("operator_identity")), "operator_identity")
        raise ValueError("operator_identity must match BLK-088 request package")
    _scan_string(decision["operator_identity"], "operator_identity")
    if decision.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if decision.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if decision.get("upstream_authority_request_package_id") != request["authority_request_package_id"]:
        raise ValueError("upstream_authority_request_package_id must match BLK-088 request package")
    if decision.get("upstream_authority_request_package_hash") != request["authority_request_package_hash"]:
        raise ValueError("upstream_authority_request_package_hash must match BLK-088 request package")
    consumed_ids = {
        request["authority_request_package_id"],
        request["upstream_execution_package_id"],
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


def _scan_string(value: str, label: str) -> None:
    _required_string(value, label, scan=False)
    normalized = _normalize(value)
    if any(marker in normalized for marker in _FORBIDDEN_NORMALIZED_MARKERS):
        raise ValueError(f"{label} contains authority-laundering text")
