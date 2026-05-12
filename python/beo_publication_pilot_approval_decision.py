"""Fixture-only BEO publication pilot approval-decision capture.

This module validates and builds deterministic local approval-decision packages for
an exact BLK-085 BEO publication pilot execution request. It records a scoped
human approval decision for one future publication-pilot execution sprint, but it
does not execute the pilot, publish BEOs, capture approval through a live external
system, access signer key material, sign artifacts, write storage, append ledgers,
execute rollback, generate RTM, run BLK-test/Codex/BLK-pipe, read protected
BLK-req bodies, or scan/mutate target repositories.
"""

from __future__ import annotations

from datetime import datetime
import re
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution_request import (
    EXACT_EXCLUDED_AUTHORITIES as REQUEST_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as REQUEST_PROOF_OBLIGATIONS,
    NOT_GENERATED,
    REQUEST_READY,
    REQUEST_SCOPE,
    SELECTED_FRONTIER as REQUEST_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as REQUEST_SIDE_EFFECT_FLAGS,
)

APPROVAL_DECISION_CAPTURED = "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK085_REQUEST_NOT_EXECUTED"
APPROVAL_DECISION_PACKAGE_ID = "BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001"
SELECTED_FRONTIER = "beo_publication_pilot_approval_decision"
DECISION_SCOPE = "BEO_PUBLICATION_PILOT_APPROVAL_DECISION_ONLY_NOT_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_BEO_PUBLICATION_PILOT_EXECUTION_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_BEO_PUBLICATION_PILOT_EXECUTION_SPRINT_REQUIRED_NOT_RUN"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")
HASH_PATTERN = r"sha256:[0-9a-f]{64}"

SIDE_EFFECT_FLAGS = (
    "publication_pilot_executed",
    "future_run_id_consumed",
    "publication_performed",
    "runtime_published_beo_output",
    "live_publication_approval_captured",
    "signature_generated",
    "key_material_accessed",
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
    "target_repo_scan_authorized",
    "target_repo_mutation_authorized",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "codex_live_execution_authorized",
    "blk_pipe_execution_authorized",
    "blk_test_runtime_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
    "source_mutation_attempted",
    "git_mutation_attempted",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "ACTUAL_AUTHORITATIVE_BEO_PUBLICATION_THIS_SPRINT",
    "PUBLICATION_PILOT_EXECUTION_PERFORMED_BY_BLK_SYSTEM_086",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_EXTERNAL_PUBLICATION_APPROVAL_CAPTURE",
    "APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
    "FUTURE_RUN_ID_CONSUMPTION",
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
    "SOURCE_OR_GIT_MUTATION",
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
    "BLK085_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "HUMAN_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_MATCHES_BLK085_FUTURE_APPROVAL_ID",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "NEXT_EXECUTION_SPRINT_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_RUN",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_PUBLICATION_PILOT_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = {
    "request_status",
    "request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
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
    "upstream_pilot_request_id",
    "upstream_future_approval_id_candidate",
    "upstream_future_run_id_candidate",
    "pilot_request_id",
    "future_approval_id_candidate",
    "future_run_id_candidate",
    "approval_required_before_execution",
    "next_required_authority",
    "requested_at",
    "expires_at",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "beo_publication",
    "rtm_status",
    "request_package_hash",
    *REQUEST_SIDE_EFFECT_FLAGS,
}

_DECISION_KEYS = {
    "approval_decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "upstream_request_package_id",
    "upstream_request_package_hash",
    "upstream_decision_package_id",
    "upstream_decision_package_hash",
    "exact_beo_id",
    "exact_beo_hash",
    "exact_target_id",
    "approved_pilot_request_id",
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
}

_ATTESTATION_KEYS = {
    "exact_blk085_request_reviewed",
    "approval_is_limited_to_one_future_pilot_execution_sprint",
    "publication_pilot_not_executed_by_this_decision",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "rtm_generation_excluded",
    "protected_body_reads_excluded",
    "target_repo_scan_or_mutation_excluded",
    "no_runtime_side_effects",
}

_CANONICAL_REQUEST_PACKAGE_FIELDS = {
    "request_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-001",
    "operator_identity": "discord:684235178083745819",
    "request_scope": REQUEST_SCOPE,
    "selected_frontier": REQUEST_SELECTED_FRONTIER,
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
    "upstream_pilot_request_id": "BEO-PUBLICATION-PILOT-REQUEST-083-001",
    "upstream_future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
    "upstream_future_run_id_candidate": "RUN-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
    "pilot_request_id": "BEO-PUBLICATION-PILOT-EXECUTION-REQUEST-085-PILOT-001",
    "future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
    "future_run_id_candidate": "RUN-BLK-SYSTEM-085-BEO-PUBLICATION-PILOT-001",
    "request_package_hash": "sha256:6dc1b6eac1d85b3a2d3b7c01eb8efa2f3f5ed0f91e04227a3a7b43554271db10",
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
    "approvedforpublication",
    "approvedforruntimeexecution",
    "publicationapproved",
    "beopubapproved",
    "abpapproved",
    "rtpbeo",
    "publicationapprovalgranted",
    "publicationauthoritygranted",
    "publicationauthorityallowed",
    "publicationauthoritypermitted",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "authoritativebeopublication",
    "publishbeo",
    "publicationgreenlit",
    "publicationallowed",
    "publicationpermitted",
    "allowedforpublication",
    "permittedforpublication",
    "pilotexecutionauthorized",
    "publicationpilotexecuted",
    "publicationpilotexecutionperformed",
    "publicationperformed",
    "runtimepublishedbeo",
    "runtimeapproval",
    "liveexecutionauthorized",
    "rtmauthorized",
    "rtmauthoritygranted",
    "rtmauthoritybeforepublicationprerequisites",
    "rtmid",
    "rtmgeneration",
    "rtmgenerated",
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
    "protectedblkreqbodyreadsauthorized",
    "targetreposcan",
    "targetrepoauthority",
    "targetrepositoryauthority",
    "targetrepoauthorized",
    "targetrepomutation",
    "bebdispatch",
    "beocloseoutexecution",
    "livecodexexecution",
    "codexapproval",
    "approvalinherited",
    "blkpipeexecution",
    "blkpipesuccess",
    "blktestruntime",
    "blktestpassapproval",
    "gitmutationauthorized",
    "gitcommitauthorized",
    "gitcommitallowed",
    "gitpushauthorized",
    "gitpushallowed",
    "sourcegitauthorized",
    "stagingauthorized",
    "stagingallowed",
    "autofixauthorized",
    "autofixallowed",
    "sourcemutationauthorized",
    "sourcemutationallowed",
    "sourcemutationattempted",
    "packagemanagerisauthorized",
    "packagemanagerauthorized",
    "packagemanagersauthorized",
    "packagemanagersareauthorized",
    "networkauthorized",
    "networkaccessauthorized",
    "networkmodelbrowsercybertoolingisauthorized",
    "networkmodelcyberbrowsertoolingauthorized",
    "modelserviceisauthorized",
    "modelserviceauthorized",
    "modelservicesauthorized",
    "browsertoolingisauthorized",
    "browsertoolingauthorized",
    "browsertoolsauthorized",
    "cybertoolingisauthorized",
    "cybertoolingauthorized",
    "cybertoolsauthorized",
    "signaturegenerated",
    "cryptographicsigning",
    "signerauthoritygranted",
    "signerauthorized",
    "storagewriteauthorized",
    "storageauthorized",
    "ledgerappendauthorized",
    "ledgerauthorized",
    "rollbackauthorized",
    "rollbackauthoritygranted",
    "productionsandboxisenforced",
    "productionsandboxauthorized",
    "productionisolationauthorized",
    "productionisolationclaimed",
    "productionisolationisclaimed",
    "claimsareauthorized",
    "isauthorized",
)


def build_beo_publication_pilot_approval_decision(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Build an exact approval-decision package without running the pilot."""

    request = _validate_request_package(request_package)
    decision = _validate_approval_decision(approval_decision, request)

    package = {
        "approval_decision_status": APPROVAL_DECISION_CAPTURED,
        "approval_decision_package_id": decision["approval_decision_package_id"],
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "decision_result": DECISION_RESULT,
        "upstream_request_package_id": request["request_package_id"],
        "upstream_request_package_hash": request["request_package_hash"],
        "upstream_decision_package_id": request["upstream_decision_package_id"],
        "upstream_decision_package_hash": request["upstream_decision_package_hash"],
        "envelope_id": request["envelope_id"],
        "envelope_hash": request["envelope_hash"],
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "target_id": request["target_id"],
        "target_ref": request["target_ref"],
        "candidate_id": request["candidate_id"],
        "source_evidence_hash": request["source_evidence_hash"],
        "trace_artifacts": request["trace_artifacts"],
        "signer_policy_hash": request["signer_policy_hash"],
        "storage_policy_hash": request["storage_policy_hash"],
        "ledger_policy_hash": request["ledger_policy_hash"],
        "rollback_policy_hash": request["rollback_policy_hash"],
        "audit_bundle_hash": request["audit_bundle_hash"],
        "operator_stop_control": request["operator_stop_control"],
        "pilot_replay_protection": request["pilot_replay_protection"],
        "approved_pilot_request_id": request["pilot_request_id"],
        "approval_id": decision["approval_id"],
        "future_run_id": decision["future_run_id"],
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_approval_granted": True,
        "publication_pilot_execution_approved_for_future_sprint": True,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": decision["operator_attestation"],
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "beo_publication": "APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED",
        "rtm_status": NOT_GENERATED,
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_decision_package_hash"}
    )
    return package


def _validate_request_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "request_package")
    # The BLK-085 request package contains fixture-owned denial/proof key names
    # such as rtm_generation_excluded. Validate the exact schema, exact hash, and
    # canonical fixture identity instead of rescanning known-safe upstream keys as
    # caller-controlled prose.
    _enforce_exact_keys(package, _REQUEST_PACKAGE_KEYS, "request_package")
    if _required_string(package.get("request_status"), "request_status", scan=False) != REQUEST_READY:
        raise ValueError("request package must be BLK-085 request-ready")
    if _required_string(package.get("request_scope"), "request_scope", scan=False) != REQUEST_SCOPE:
        raise ValueError("request package must remain BLK-085 request-gate only")
    if _required_string(package.get("selected_frontier"), "selected_frontier", scan=False) != REQUEST_SELECTED_FRONTIER:
        raise ValueError("request package selected_frontier must be beo_publication_pilot_execution_request")
    if package.get("approval_required_before_execution") is not True:
        raise ValueError("request package must require approval before execution")
    if _required_string(package.get("next_required_authority"), "next_required_authority", scan=False) != "EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED":
        raise ValueError("request package must not already grant approval")
    if _required_string(package.get("beo_publication"), "beo_publication", scan=False) != "PILOT_EXECUTION_REQUEST_ONLY_NOT_APPROVED_NOT_PUBLISHED":
        raise ValueError("request package must remain not published")
    if _required_string(package.get("rtm_status"), "rtm_status", scan=False) != NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    for flag in REQUEST_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_set(package.get("proof_obligations"), REQUEST_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), REQUEST_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    request_hash = _required_hash(package.get("request_package_hash"), "request_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"})
    if request_hash != expected_hash:
        raise ValueError("request_package_hash does not match canonical request package")
    _validate_canonical_request_fixture(package)
    return package


def _validate_approval_decision(decision: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(decision, "approval_decision")
    _enforce_exact_keys(decision, _DECISION_KEYS, "approval_decision")
    if _required_string(decision.get("decision_scope"), "decision_scope", scan=False) != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if _required_string(decision.get("selected_frontier"), "selected_frontier", scan=False) != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if _required_string(decision.get("decision_result"), "decision_result", scan=False) != DECISION_RESULT:
        raise ValueError(f"decision_result must be {DECISION_RESULT}")
    for key in [
        "approval_decision_package_id",
        "operator_identity",
        "upstream_request_package_id",
        "upstream_decision_package_id",
        "exact_beo_id",
        "exact_target_id",
        "approved_pilot_request_id",
        "approval_id",
        "future_run_id",
    ]:
        _required_string(decision.get(key), key)
    for key in ["upstream_request_package_hash", "upstream_decision_package_hash", "exact_beo_hash"]:
        _required_hash(decision.get(key), key)
    for flag in ["expired", "replayed", "stale"]:
        if decision.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(decision.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(decision.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    if decision["operator_identity"] != request["operator_identity"]:
        raise ValueError("operator_identity must match BLK-085 request package")
    if decision["upstream_request_package_id"] != request["request_package_id"]:
        raise ValueError("upstream_request_package_id does not match request package")
    if decision["upstream_request_package_hash"] != request["request_package_hash"]:
        raise ValueError("upstream_request_package_hash does not match request package")
    if decision["upstream_decision_package_id"] != request["upstream_decision_package_id"]:
        raise ValueError("upstream_decision_package_id does not match request package")
    if decision["upstream_decision_package_hash"] != request["upstream_decision_package_hash"]:
        raise ValueError("upstream_decision_package_hash does not match request package")
    if decision["exact_beo_id"] != request["beo_id"]:
        raise ValueError("exact_beo_id does not match request package")
    if decision["exact_beo_hash"] != request["beo_hash"]:
        raise ValueError("exact_beo_hash does not match request package")
    if decision["exact_target_id"] != request["target_id"]:
        raise ValueError("exact_target_id does not match request package")
    if decision["approved_pilot_request_id"] != request["pilot_request_id"]:
        raise ValueError("approved_pilot_request_id must equal BLK-085 pilot request id")
    if decision["approval_id"] != request["future_approval_id_candidate"]:
        raise ValueError("approval_id must equal BLK-085 future approval candidate")
    if decision["future_run_id"] != request["future_run_id_candidate"]:
        raise ValueError("future_run_id must equal BLK-085 future run candidate")
    consumed_ids = {
        request["request_package_id"],
        request["upstream_decision_package_id"],
        request["envelope_id"],
        request["beo_id"],
        request["target_id"],
        request["candidate_id"],
        request["upstream_pilot_request_id"],
        request["upstream_future_approval_id_candidate"],
        request["upstream_future_run_id_candidate"],
        request["pilot_request_id"],
        request["future_run_id_candidate"],
    }
    if decision["approval_decision_package_id"] in consumed_ids:
        raise ValueError("approval_decision_package_id must be fresh")
    decision_identity_values = [
        decision["approval_decision_package_id"],
        decision["approval_id"],
        decision["future_run_id"],
    ]
    if len(set(decision_identity_values)) != len(decision_identity_values):
        raise ValueError("approval decision package id must be distinct")
    if decision["approval_decision_package_id"] != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError(f"approval_decision_package_id must equal {APPROVAL_DECISION_PACKAGE_ID}")
    _validate_attestation(decision.get("operator_attestation"))
    _validate_exact_set(decision.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(decision.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return decision


def _validate_canonical_request_fixture(package: dict[str, Any]) -> None:
    for key, expected in _CANONICAL_REQUEST_PACKAGE_FIELDS.items():
        if package.get(key) != expected:
            raise ValueError("request package must match canonical BLK-085 fixture")


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


def _scan_nested(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _scan_scalar(str(key), f"{label}.{key}")
            _scan_nested(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_nested(item, f"{label}[{index}]")
    elif isinstance(value, str):
        _scan_scalar(value, label)


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
