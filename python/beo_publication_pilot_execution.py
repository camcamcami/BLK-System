"""Exact local BEO publication pilot execution fixture.

This module consumes the BLK-SYSTEM-086 approval-decision package and emits one
hash-bound deterministic local pilot publication artifact. It deliberately does
not access signer key material, create cryptographic signatures, write immutable
storage, append ledgers, execute rollback/revocation/supersession, generate RTM,
read protected BLK-req bodies, scan or mutate target repositories, run
BLK-test/Codex/BLK-pipe, use package/network/model/browser/cyber tooling, or
claim production isolation.
"""

from __future__ import annotations

from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_approval_decision import (
    APPROVAL_DECISION_CAPTURED,
    APPROVAL_DECISION_PACKAGE_ID,
    DECISION_RESULT as APPROVAL_DECISION_RESULT,
    DECISION_SCOPE as APPROVAL_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as APPROVAL_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as APPROVAL_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as APPROVAL_NEXT_REQUIRED_AUTHORITY,
    NOT_GENERATED,
    SELECTED_FRONTIER as APPROVAL_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as APPROVAL_SIDE_EFFECT_FLAGS,
)

EXECUTION_STATUS = "BEO_PUBLICATION_PILOT_EXECUTED_FOR_EXACT_BLK086_APPROVAL_LOCAL_ONLY"
EXECUTION_PACKAGE_ID = "BEO-PUBLICATION-PILOT-EXECUTION-087-001"
SELECTED_FRONTIER = "exact_beo_publication_pilot_execution"
EXECUTION_SCOPE = "EXACT_BEO_PUBLICATION_PILOT_EXECUTION_LOCAL_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM"
NEXT_REQUIRED_AUTHORITY = "RTM_AUTHORITY_REQUEST_AFTER_PUBLISHED_BEO_PREREQUISITES_NOT_GRANTED"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")
HASH_PATTERN = r"sha256:[0-9a-f]{64}"

SIDE_EFFECT_FLAGS = (
    "authoritative_external_publication_performed",
    "live_approval_capture_performed",
    "signer_key_material_accessed",
    "cryptographic_signature_generated",
    "immutable_storage_written",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generated",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_read",
    "target_repo_scanned",
    "target_repo_mutated",
    "source_mutation_attempted",
    "git_mutation_attempted",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "codex_live_execution_authorized",
    "blk_pipe_execution_authorized",
    "blk_test_runtime_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "AUTHORITATIVE_EXTERNAL_BEO_PUBLICATION",
    "LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE",
    "APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX",
    "COVERAGE_CLAIM",
    "DRIFT_DECISION",
    "PROTECTED_BLK_REQ_BODY_READ",
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
    "BLK086_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
    "APPROVAL_ID_MATCHES_BLK086_CAPTURED_APPROVAL",
    "RUN_ID_MATCHES_BLK086_RESERVED_RUN_ID_AND_CONSUMED_ONCE",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_EXTERNAL_WRITE",
    "LOCAL_PILOT_PUBLICATION_ARTIFACT_HASH_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_AFTER_PUBLICATION_PILOT_EXECUTION",
}

_EXECUTION_REQUEST_KEYS = {
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "execute_publication_pilot",
    "authoritative_external_publication",
    "live_approval_capture",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "rtm_generation",
    "drift_rejection",
    "protected_body_reads",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
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
    "exact_blk086_approval_decision_reviewed",
    "run_id_consumed_once_for_local_pilot",
    "local_pilot_output_not_external_authoritative_publication",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "rtm_generation_excluded",
    "protected_body_reads_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_APPROVAL_PACKAGE_KEYS = {
    "approval_decision_status",
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "decision_result",
    "upstream_request_package_id",
    "upstream_request_package_hash",
    "upstream_decision_package_id",
    "upstream_decision_package_hash",
    "envelope_id",
    "envelope_hash",
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
    "approved_pilot_request_id",
    "approval_id",
    "future_run_id",
    "decided_at",
    "expires_at",
    "approval_decision_captured",
    "human_approval_granted",
    "publication_pilot_execution_approved_for_future_sprint",
    "next_required_authority",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "beo_publication",
    "rtm_status",
    "approval_decision_package_hash",
    *APPROVAL_SIDE_EFFECT_FLAGS,
}

_CANONICAL_APPROVAL_PACKAGE_FIELDS = {
    "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
    "operator_identity": "discord:684235178083745819",
    "decision_scope": APPROVAL_DECISION_SCOPE,
    "selected_frontier": APPROVAL_SELECTED_FRONTIER,
    "decision_result": APPROVAL_DECISION_RESULT,
    "upstream_request_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001",
    "upstream_request_package_hash": "sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10",
    "upstream_decision_package_id": "BEO-PUBLICATION-DECISION-PACKAGE-083-001",
    "upstream_decision_package_hash": "sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b",
    "envelope_id": "BEO-PUB-APPROVAL-ENVELOPE-055-001",
    "envelope_hash": "sha256:fde101a590798352b60dbf63b1ad78a273b8b84306894775d9caed6757fd9b47",
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
    "approved_pilot_request_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001",
    "approval_id": "APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
    "future_run_id": "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
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
    "authoritativebeopublication",
    "externalpublicationauthorized",
    "externalpublicationperformed",
    "livepublicationapprovalcapture",
    "approvalretargeting",
    "scopeexpansion",
    "signaturegenerated",
    "cryptographicsigning",
    "signerauthorized",
    "signerauthoritygranted",
    "immutablestoragewrite",
    "immutablestoragewritten",
    "storageauthorized",
    "publicledgerappend",
    "publicledgermutation",
    "ledgerauthorized",
    "rollbackexecuted",
    "rollbackauthorized",
    "rollbackauthoritygranted",
    "revocationexecuted",
    "supersessionexecuted",
    "rtmid",
    "rtmgeneration",
    "rtmgenerated",
    "rtmauthorized",
    "rtmdriftrejection",
    "activevaulthashcomparison",
    "coveragematrix",
    "coverageclaim",
    "driftdecision",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "protectedbodypath",
    "protectedbodyauthorized",
    "protectedbodyreadauthorized",
    "protectedblkreqbody",
    "targetreposcan",
    "targetrepoauthority",
    "targetrepositoryauthority",
    "targetrepomutation",
    "sourcemutationauthorized",
    "sourcemutationattempted",
    "sourcegitauthorized",
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
    "packagemanagersareauthorized",
    "networkaccessauthorized",
    "modelserviceauthorized",
    "modelservicesauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionsandboxisenforced",
    "productionisolationauthorized",
    "productionisolationclaimed",
    "claimsareauthorized",
    "isauthorized",
)


def build_beo_publication_pilot_execution(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Execute one exact deterministic local BEO publication pilot fixture."""

    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)

    artifact = {
        "publication_mode": "LOCAL_DETERMINISTIC_PILOT_ONLY",
        "published_beo_id": approval["beo_id"],
        "published_beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "source_evidence_hash": approval["source_evidence_hash"],
        "trace_artifacts": approval["trace_artifacts"],
        "signer_policy_hash": approval["signer_policy_hash"],
        "signature_status": "NOT_SIGNED_NO_KEY_MATERIAL",
        "storage_policy_hash": approval["storage_policy_hash"],
        "storage_status": "NOT_WRITTEN_LOCAL_RECEIPT_ONLY",
        "ledger_policy_hash": approval["ledger_policy_hash"],
        "ledger_status": "NOT_APPENDED_LOCAL_RECEIPT_ONLY",
        "rollback_policy_hash": approval["rollback_policy_hash"],
        "rollback_status": "NOT_EXECUTED_POLICY_BOUND_ONLY",
        "audit_bundle_hash": approval["audit_bundle_hash"],
    }
    artifact["pilot_publication_artifact_hash"] = _canonical_hash(
        {key: value for key, value in artifact.items() if key != "pilot_publication_artifact_hash"}
    )

    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_decision_package_hash": approval["approval_decision_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": approval["future_run_id"],
        "upstream_request_package_id": approval["upstream_request_package_id"],
        "upstream_request_package_hash": approval["upstream_request_package_hash"],
        "upstream_decision_package_id": approval["upstream_decision_package_id"],
        "upstream_decision_package_hash": approval["upstream_decision_package_hash"],
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_id": approval["target_id"],
        "target_ref": approval["target_ref"],
        "candidate_id": approval["candidate_id"],
        "source_evidence_hash": approval["source_evidence_hash"],
        "trace_artifacts": approval["trace_artifacts"],
        "signer_policy_hash": approval["signer_policy_hash"],
        "storage_policy_hash": approval["storage_policy_hash"],
        "ledger_policy_hash": approval["ledger_policy_hash"],
        "rollback_policy_hash": approval["rollback_policy_hash"],
        "audit_bundle_hash": approval["audit_bundle_hash"],
        "operator_stop_control": approval["operator_stop_control"],
        "pilot_replay_protection": approval["pilot_replay_protection"],
        "publication_pilot_executed": True,
        "future_run_id_consumed": True,
        "local_pilot_publication_artifact_emitted": True,
        "pilot_publication_artifact": artifact,
        "pilot_publication_artifact_hash": artifact["pilot_publication_artifact_hash"],
        "beo_publication": "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
        "rtm_status": NOT_GENERATED,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": request["operator_attestation"],
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
    _enforce_exact_keys(package, _APPROVAL_PACKAGE_KEYS, "approval_package")
    if _required_string(package.get("approval_decision_status"), "approval_decision_status", scan=False) != APPROVAL_DECISION_CAPTURED:
        raise ValueError("approval package must be BLK-086 approval-decision captured")
    if _required_string(package.get("decision_scope"), "decision_scope", scan=False) != APPROVAL_DECISION_SCOPE:
        raise ValueError("approval package must remain BLK-086 decision scope")
    if _required_string(package.get("selected_frontier"), "selected_frontier", scan=False) != APPROVAL_SELECTED_FRONTIER:
        raise ValueError("approval package selected_frontier must remain approval decision")
    if _required_string(package.get("decision_result"), "decision_result", scan=False) != APPROVAL_DECISION_RESULT:
        raise ValueError("approval package decision_result must remain future-sprint approval")
    if _required_string(package.get("next_required_authority"), "next_required_authority", scan=False) != APPROVAL_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("approval package next authority must require exact execution sprint")
    if _required_string(package.get("beo_publication"), "beo_publication", scan=False) != "APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED":
        raise ValueError("approval package must remain not published")
    if _required_string(package.get("rtm_status"), "rtm_status", scan=False) != NOT_GENERATED:
        raise ValueError("approval package rtm_status must remain NOT_GENERATED")
    if package.get("publication_pilot_executed") is not False or package.get("future_run_id_consumed") is not False:
        raise ValueError("approval package must remain not executed")
    for flag in APPROVAL_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    if package.get("approval_decision_captured") is not True:
        raise ValueError("approval decision must be captured")
    if package.get("human_approval_granted") is not True:
        raise ValueError("human approval must be granted in BLK-086 package")
    if package.get("publication_pilot_execution_approved_for_future_sprint") is not True:
        raise ValueError("publication pilot execution approval must be future-sprint scoped")
    _validate_exact_set(package.get("proof_obligations"), APPROVAL_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), APPROVAL_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    approval_hash = _required_hash(package.get("approval_decision_package_hash"), "approval_decision_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"})
    if approval_hash != expected_hash:
        raise ValueError("approval_decision_package_hash does not match canonical approval package")
    _validate_canonical_approval_fixture(package)
    return package


def _validate_execution_request(request: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_exact_keys(request, _EXECUTION_REQUEST_KEYS, "execution_request")
    execution_id = _required_string(request.get("execution_package_id"), "execution_package_id", scan=False)
    consumed_ids = {
        approval["approval_decision_package_id"],
        approval["upstream_request_package_id"],
        approval["upstream_decision_package_id"],
        approval["envelope_id"],
        approval["beo_id"],
        approval["target_id"],
        approval["candidate_id"],
        approval["approved_pilot_request_id"],
        approval["approval_id"],
        approval["future_run_id"],
    }
    if execution_id in consumed_ids:
        raise ValueError("execution_package_id must be fresh")
    if execution_id != EXECUTION_PACKAGE_ID:
        _scan_scalar(execution_id, "execution_package_id")
        raise ValueError(f"execution_package_id must equal {EXECUTION_PACKAGE_ID}")
    _required_string(request.get("operator_identity"), "operator_identity")
    if _required_string(request.get("execution_scope"), "execution_scope", scan=False) != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if _required_string(request.get("selected_frontier"), "selected_frontier", scan=False) != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    for key in ["approval_decision_package_id", "approval_id", "run_id", "beo_id", "target_id", "target_ref"]:
        _required_string(request.get(key), key, scan=False)
    for key in ["approval_decision_package_hash", "beo_hash"]:
        _required_hash(request.get(key), key)
    if request["operator_identity"] != approval["operator_identity"]:
        raise ValueError("operator_identity must match BLK-086 approval package")
    if request["approval_decision_package_id"] != approval["approval_decision_package_id"]:
        raise ValueError("approval_decision_package_id must match BLK-086 approval package")
    if request["approval_decision_package_hash"] != approval["approval_decision_package_hash"]:
        raise ValueError("approval_decision_package_hash must match BLK-086 approval package")
    if request["approval_id"] != approval["approval_id"]:
        raise ValueError("approval_id must equal BLK-086 approval id")
    if request["run_id"] != approval["future_run_id"]:
        raise ValueError("run_id must equal BLK-086 future run id")
    if request["beo_id"] != approval["beo_id"]:
        raise ValueError("beo_id must match BLK-086 approval package")
    if request["beo_hash"] != approval["beo_hash"]:
        raise ValueError("beo_hash must match BLK-086 approval package")
    if request["target_id"] != approval["target_id"]:
        raise ValueError("target_id must match BLK-086 approval package")
    if request["target_ref"] != approval["target_ref"]:
        raise ValueError("target_ref must match BLK-086 approval package")
    if request.get("execute_publication_pilot") is not True:
        raise ValueError("execute_publication_pilot must be true")
    for flag in [
        "authoritative_external_publication",
        "live_approval_capture",
        "signer_key_material_access",
        "cryptographic_signing",
        "immutable_storage_write",
        "public_ledger_mutation",
        "rollback_revocation_supersession_execution",
        "rtm_generation",
        "drift_rejection",
        "protected_body_reads",
        "target_repo_scan_or_mutation",
        "source_or_git_mutation_by_fixture",
        "blk_test_codex_blk_pipe_runtime",
        "package_network_model_browser_cyber_tooling",
        "production_isolation_claim",
    ]:
        _required_false(request.get(flag), flag)
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_canonical_approval_fixture(package: dict[str, Any]) -> None:
    for key, expected in _CANONICAL_APPROVAL_PACKAGE_FIELDS.items():
        if package.get(key) != expected:
            raise ValueError("approval package must match canonical BLK-086 fixture")


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
        raise ValueError(
            f"{label} must match exact denied authority set" if label == "excluded_authorities" else f"{label} must match exact set"
        )


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
            "signer",
            "storage",
            "ledger",
            "rollback",
            "protectedbody",
            "sourcemutation",
            "gitmutation",
            "targetrepo",
            "codex",
            "blkpipe",
            "blktest",
        )
    )
