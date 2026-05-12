"""RTM authority request fixture after BLK-087 local BEO pilot evidence.

This module packages the completed BLK-SYSTEM-087 local publication-pilot
execution package into a deterministic request for future human RTM authority
review. It does not grant approval, generate RTM, reject drift, compare active
vault hashes, create coverage matrices, read protected bodies, publish BEOs
externally, access signer/storage/ledger systems, mutate source/Git, run
BLK-test/Codex/BLK-pipe, use package/network/model/browser/cyber tooling, or
claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution import (
    EXECUTION_PACKAGE_ID as BLK087_EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE as BLK087_EXECUTION_SCOPE,
    EXECUTION_STATUS as BLK087_EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK087_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK087_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK087_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK087_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK087_SIDE_EFFECT_FLAGS,
)

REQUEST_STATUS = "RTM_AUTHORITY_REQUEST_READY_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_NOT_GRANTED"
AUTHORITY_REQUEST_PACKAGE_ID = "RTM-AUTHORITY-REQUEST-AFTER-BEO-PILOT-088-001"
SELECTED_FRONTIER = "rtm_authority_request_after_local_beo_pilot_prerequisites"
REQUEST_SCOPE = "RTM_AUTHORITY_REQUEST_AFTER_LOCAL_BEO_PILOT_PREREQUISITES_REVIEW_ONLY"
NEXT_REQUIRED_AUTHORITY = "EXPLICIT_HUMAN_RTM_GENERATION_APPROVAL_REQUIRED_NOT_GRANTED"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")
HASH_PATTERN = r"sha256:[0-9a-f]{64}"

SIDE_EFFECT_FLAGS = (
    "human_rtm_approval_granted",
    "rtm_generation_authorized",
    "rtm_generated",
    "drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_matrix_created",
    "coverage_claim_promoted",
    "protected_body_reads",
    "authoritative_external_publication",
    "live_approval_capture_performed",
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
    "HUMAN_RTM_APPROVAL_CAPTURE",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_CREATION",
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
    "BLK087_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK087_LOCAL_PILOT_STATUS_BOUND",
    "PILOT_PUBLICATION_ARTIFACT_IDENTITY_AND_HASH_BOUND",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_EXTERNAL_WRITE",
    "LOCAL_PILOT_ONLY_NOT_EXTERNAL_AUTHORITATIVE_PUBLICATION_DISCLOSED",
    "RTM_AUTHORITY_REQUESTED_FOR_REVIEW_NOT_GRANTED",
    "RTM_GENERATION_AND_DRIFT_AUTHORITIES_EXCLUDED_UNTIL_FUTURE_APPROVAL",
    "ACTIVE_VAULT_HASH_COMPARISON_AND_COVERAGE_CLAIMS_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_RTM_GENERATION",
}

_AUTHORITY_REQUEST_KEYS = {
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "pilot_publication_artifact_hash",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "request_future_exact_rtm_generation_authority",
    "human_rtm_approval_granted",
    "rtm_generation_authorized",
    "rtm_generated",
    "drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_matrix_created",
    "coverage_claim_promoted",
    "protected_body_reads",
    "authoritative_external_publication",
    "live_approval_capture_performed",
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
    "requested_at",
    "expires_at",
    "expired",
    "replayed",
    "stale",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
}

_ATTESTATION_KEYS = {
    "exact_blk087_execution_package_reviewed",
    "local_pilot_artifact_is_not_external_authoritative_publication",
    "rtm_authority_is_requested_for_future_human_review_not_granted",
    "no_rtm_generation_or_drift_decision_performed",
    "no_active_vault_hash_comparison_or_coverage_claim",
    "protected_body_reads_excluded",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_EXECUTION_PACKAGE_KEYS = {
    "execution_status",
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id_consumed",
    "upstream_request_package_id",
    "upstream_request_package_hash",
    "upstream_decision_package_id",
    "upstream_decision_package_hash",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "candidate_id",
    "source_evidence_hash",
    "trace_artifacts",
    "signer_policy_hash",
    "storage_policy_hash",
    "ledger_policy_hash",
    "rollback_policy_hash",
    "audit_bundle_hash",
    "operator_stop_control",
    "pilot_replay_protection",
    "publication_pilot_executed",
    "future_run_id_consumed",
    "local_pilot_publication_artifact_emitted",
    "pilot_publication_artifact",
    "pilot_publication_artifact_hash",
    "beo_publication",
    "rtm_status",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "execution_package_hash",
    *BLK087_SIDE_EFFECT_FLAGS,
}

_CANONICAL_EXECUTION_FIELDS = {
    "execution_package_id": BLK087_EXECUTION_PACKAGE_ID,
    "operator_identity": "discord:684235178083745819",
    "execution_scope": BLK087_EXECUTION_SCOPE,
    "selected_frontier": BLK087_SELECTED_FRONTIER,
    "approval_decision_package_id": "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001",
    "approval_decision_package_hash": "sha256:2ade9eee61d5688c32f12cf9bec1a2668d03f091d1a14fb6eeef1c7f2f1a54b9",
    "approval_id": "APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
    "run_id_consumed": "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
    "upstream_request_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001",
    "upstream_request_package_hash": "sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10",
    "upstream_decision_package_id": "BEO-PUBLICATION-DECISION-PACKAGE-083-001",
    "upstream_decision_package_hash": "sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b",
    "beo_id": "BEO-054-001",
    "beo_hash": "sha256:" + "a" * 64,
    "target_id": "BEO-PUBLICATION-TARGET-055-001",
    "target_ref": "fixture://beo-publication-targets/055/001",
    "candidate_id": "BEO-CANDIDATE-054-001",
    "source_evidence_hash": "sha256:" + "b" * 64,
    "trace_artifacts": [
        {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "c" * 64},
    ],
    "signer_policy_hash": "sha256:" + "e" * 64,
    "storage_policy_hash": "sha256:" + "f" * 64,
    "ledger_policy_hash": "sha256:" + "1" * 64,
    "rollback_policy_hash": "sha256:" + "2" * 64,
    "audit_bundle_hash": "sha256:" + "3" * 64,
    "operator_stop_control": "discord-stop-required-before-runtime",
    "pilot_replay_protection": "fresh-approval-and-run-id-required",
}

_SECRET_MARKERS = (
    "privatekey",
    "signerkeymaterial",
    "keymaterial",
    "apikey",
    "token",
    "password",
    "passphrase",
    "secret",
)

_FORBIDDEN_NORMALIZED_MARKERS = (
    "approvedforliveexecution",
    "runtimepilotapproved",
    "livepilotallowed",
    "humanrtmapprovalgranted",
    "rtmid",
    "rtmgeneration",
    "rtmgenerated",
    "rtmauthorized",
    "rtmauthoritygranted",
    "rtmdriftrejection",
    "driftdecision",
    "activevaulthashcomparison",
    "coveragematrix",
    "coverageclaim",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "protectedbodypath",
    "protectedbodyauthorized",
    "protectedbodyreadauthorized",
    "protectedblkreqbody",
    "authoritativebeopublication",
    "externalpublicationauthorized",
    "signaturegenerated",
    "cryptographicsigning",
    "signerauthorized",
    "immutablestoragewrite",
    "publicledgerappend",
    "publicledgermutation",
    "rollbackexecuted",
    "revocationexecuted",
    "supersessionexecuted",
    "targetreposcan",
    "targetrepomutation",
    "sourcemutationauthorized",
    "sourcemutationattempted",
    "gitmutationauthorized",
    "gitcommitauthorized",
    "gitpushauthorized",
    "bebdispatch",
    "beocloseoutexecution",
    "livecodexexecution",
    "codexapproval",
    "approvalinherited",
    "blkpipeexecution",
    "blkpipesuccess",
    "blktestruntime",
    "blktestpassapproval",
    "packagemanagerauthorized",
    "packagemanagersauthorized",
    "networkaccessauthorized",
    "modelserviceauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionsandboxisenforced",
    "productionisolationauthorized",
    "productionisolationclaimed",
    "claimsareauthorized",
    "isauthorized",
)


def build_rtm_authority_request_after_beo_pilot(
    execution_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a request-only RTM authority package bound to BLK-087 evidence."""

    execution = _validate_execution_package(execution_package)
    request = _validate_authority_request(authority_request, execution)
    trace_artifacts = deepcopy(execution["trace_artifacts"])
    pilot_artifact = deepcopy(execution["pilot_publication_artifact"])
    operator_attestation = deepcopy(request["operator_attestation"])

    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "approval_decision_package_id": execution["approval_decision_package_id"],
        "approval_decision_package_hash": execution["approval_decision_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beo_hash": execution["beo_hash"],
        "target_id": execution["target_id"],
        "target_ref": execution["target_ref"],
        "source_evidence_hash": execution["source_evidence_hash"],
        "trace_artifacts": trace_artifacts,
        "pilot_publication_artifact": pilot_artifact,
        "pilot_publication_artifact_hash": execution["pilot_publication_artifact_hash"],
        "local_pilot_beo_publication": execution["beo_publication"],
        "requested_authority": "FUTURE_EXACT_RTM_GENERATION_AUTHORITY_REQUESTED_FOR_HUMAN_REVIEW",
        "request_future_exact_rtm_generation_authority": True,
        "human_rtm_approval_required": True,
        "rtm_status": "NOT_GENERATED",
        "rtm_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": operator_attestation,
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


def _validate_execution_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "execution_package")
    _enforce_exact_keys(package, _EXECUTION_PACKAGE_KEYS, "execution_package")
    if _required_string(package.get("execution_status"), "execution_status", scan=False) != BLK087_EXECUTION_STATUS:
        raise ValueError("BLK-087 package must have exact local pilot execution status")
    if _required_string(package.get("execution_scope"), "execution_scope", scan=False) != BLK087_EXECUTION_SCOPE:
        raise ValueError("BLK-087 package execution_scope must remain local-only")
    if _required_string(package.get("selected_frontier"), "selected_frontier", scan=False) != BLK087_SELECTED_FRONTIER:
        raise ValueError("BLK-087 package selected_frontier must remain exact pilot execution")
    if package.get("publication_pilot_executed") is not True:
        raise ValueError("BLK-087 package must record publication_pilot_executed true")
    if package.get("future_run_id_consumed") is not True:
        raise ValueError("BLK-087 package must record future_run_id_consumed true")
    if package.get("local_pilot_publication_artifact_emitted") is not True:
        raise ValueError("BLK-087 package must emit local pilot publication artifact")
    if _required_string(package.get("beo_publication"), "beo_publication", scan=False) != "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE":
        raise ValueError("BLK-087 package must remain local non-authoritative BEO publication")
    if _required_string(package.get("rtm_status"), "rtm_status", scan=False) != "NOT_GENERATED":
        raise ValueError("BLK-087 package rtm_status must remain NOT_GENERATED")
    if _required_string(package.get("next_required_authority"), "next_required_authority", scan=False) != BLK087_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-087 package must still require separate RTM authority request")
    for flag in BLK087_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), BLK087_PROOF_OBLIGATIONS, "execution_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), BLK087_EXCLUDED_AUTHORITIES, "execution_package excluded_authorities")
    package_hash = _required_hash(package.get("execution_package_hash"), "execution_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if package_hash != expected_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-087 package")
    artifact = _require_dict(package.get("pilot_publication_artifact"), "pilot_publication_artifact")
    artifact_hash = _required_hash(package.get("pilot_publication_artifact_hash"), "pilot_publication_artifact_hash")
    expected_artifact_hash = _canonical_hash(
        {key: value for key, value in artifact.items() if key != "pilot_publication_artifact_hash"}
    )
    if artifact_hash != expected_artifact_hash or artifact.get("pilot_publication_artifact_hash") != artifact_hash:
        raise ValueError("pilot_publication_artifact_hash does not match submitted artifact")
    _validate_canonical_execution_fixture(package)
    return package


def _validate_authority_request(request: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "authority_request")
    _enforce_exact_keys(request, _AUTHORITY_REQUEST_KEYS, "authority_request")
    request_id = _required_string(request.get("authority_request_package_id"), "authority_request_package_id", scan=False)
    consumed_ids = {
        execution["execution_package_id"],
        execution["approval_decision_package_id"],
        execution["approval_id"],
        execution["run_id_consumed"],
        execution["upstream_request_package_id"],
        execution["upstream_decision_package_id"],
        execution["beo_id"],
        execution["target_id"],
        execution["candidate_id"],
    }
    if request_id in consumed_ids:
        raise ValueError("authority_request_package_id must be fresh")
    if request_id != AUTHORITY_REQUEST_PACKAGE_ID:
        _scan_scalar(request_id, "authority_request_package_id")
        raise ValueError(f"authority_request_package_id must equal {AUTHORITY_REQUEST_PACKAGE_ID}")
    _required_string(request.get("operator_identity"), "operator_identity")
    if _required_string(request.get("request_scope"), "request_scope", scan=False) != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if _required_string(request.get("selected_frontier"), "selected_frontier", scan=False) != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    for key in ["upstream_execution_package_id", "beo_id", "target_id", "target_ref"]:
        _required_string(request.get(key), key, scan=False)
    for key in ["upstream_execution_package_hash", "pilot_publication_artifact_hash", "beo_hash"]:
        _required_hash(request.get(key), key)
    if request["operator_identity"] != execution["operator_identity"]:
        raise ValueError("operator_identity must match BLK-087 execution package")
    if request["upstream_execution_package_id"] != execution["execution_package_id"]:
        raise ValueError("upstream_execution_package_id must match BLK-087 execution package")
    if request["upstream_execution_package_hash"] != execution["execution_package_hash"]:
        raise ValueError("upstream_execution_package_hash must match BLK-087 execution package")
    if request["pilot_publication_artifact_hash"] != execution["pilot_publication_artifact_hash"]:
        raise ValueError("pilot_publication_artifact_hash must match BLK-087 execution package")
    for key in ["beo_id", "beo_hash", "target_id", "target_ref"]:
        if request[key] != execution[key]:
            raise ValueError(f"{key} must match BLK-087 execution package")
    if request.get("request_future_exact_rtm_generation_authority") is not True:
        raise ValueError("request_future_exact_rtm_generation_authority must be true")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(request.get(flag), flag)
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"authority request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("authority request must not be calendar-expired")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_canonical_execution_fixture(package: dict[str, Any]) -> None:
    for key, expected in _CANONICAL_EXECUTION_FIELDS.items():
        if package.get(key) != expected:
            raise ValueError("BLK-087 execution package must match canonical local pilot fixture")
    artifact = package["pilot_publication_artifact"]
    expected_artifact = {
        "publication_mode": "LOCAL_DETERMINISTIC_PILOT_ONLY",
        "published_beo_id": "BEO-054-001",
        "published_beo_hash": "sha256:" + "a" * 64,
        "target_id": "BEO-PUBLICATION-TARGET-055-001",
        "target_ref": "fixture://beo-publication-targets/055/001",
        "source_evidence_hash": "sha256:" + "b" * 64,
        "trace_artifacts": [
            {"kind": "REQ", "id": "REQ-001", "version_hash": "sha256:" + "c" * 64},
        ],
        "signer_policy_hash": "sha256:" + "e" * 64,
        "signature_status": "NOT_SIGNED_NO_KEY_MATERIAL",
        "storage_policy_hash": "sha256:" + "f" * 64,
        "storage_status": "NOT_WRITTEN_LOCAL_RECEIPT_ONLY",
        "ledger_policy_hash": "sha256:" + "1" * 64,
        "ledger_status": "NOT_APPENDED_LOCAL_RECEIPT_ONLY",
        "rollback_policy_hash": "sha256:" + "2" * 64,
        "rollback_status": "NOT_EXECUTED_POLICY_BOUND_ONLY",
        "audit_bundle_hash": "sha256:" + "3" * 64,
        "rtm_status": "NOT_GENERATED",
        "pilot_publication_artifact_hash": package["pilot_publication_artifact_hash"],
    }
    if artifact != expected_artifact:
        raise ValueError("BLK-087 execution package must match canonical local pilot fixture")


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _validate_exact_set(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{label} entries must be strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    if set(value) != expected:
        if label == "excluded_authorities":
            raise ValueError(f"{label} must match exact denied authority set")
        raise ValueError(f"{label} must match exact set")


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a dict")
    return value


def _enforce_exact_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = set(value) - allowed
    missing = allowed - set(value)
    authority_extra = [key for key in extra if _looks_authority_bearing(key)]
    if authority_extra:
        raise ValueError(f"{label} contains forbidden authority field")
    if extra:
        raise ValueError(f"{label} contains unexpected field")
    if missing:
        raise ValueError(f"{label} missing required field")


def _required_string(value: Any, label: str, *, scan: bool = True) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    if scan:
        _scan_scalar(value, label)
    return value


def _required_hash(value: Any, label: str) -> str:
    text = _required_string(value, label, scan=False)
    if re.fullmatch(HASH_PATTERN, text) is None:
        raise ValueError(f"{label} must be a sha256 hash")
    return text


def _required_false(value: Any, label: str) -> None:
    if value is not False:
        raise ValueError(f"{label} must remain false")


def _parse_timestamp(value: Any, label: str) -> datetime:
    text = _required_string(value, label, scan=False)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed


def _scan_scalar(value: str, label: str) -> None:
    normalized = _normalize(value)
    if any(secret in normalized for secret in _SECRET_MARKERS):
        raise ValueError(f"{label} contains secret-bearing field")
    if any(marker in normalized for marker in _FORBIDDEN_NORMALIZED_MARKERS):
        raise ValueError(f"{label} contains authority-laundering text")


def _normalize(value: str) -> str:
    decoded = value
    for _ in range(5):
        next_decoded = unquote(decoded)
        if next_decoded == decoded:
            break
        decoded = next_decoded
    return re.sub(r"[^a-z0-9]", "", decoded.casefold())


def _looks_authority_bearing(key: str) -> bool:
    normalized = _normalize(str(key))
    return any(
        marker in normalized
        for marker in (
            "approval",
            "approved",
            "authorized",
            "authority",
            "runtime",
            "publication",
            "rtm",
            "drift",
            "coverage",
            "activevault",
            "protectedbody",
            "signer",
            "storage",
            "ledger",
            "rollback",
            "sourcemutation",
            "gitmutation",
            "targetrepo",
            "codex",
            "blkpipe",
            "blktest",
        )
    )
