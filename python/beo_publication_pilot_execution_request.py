"""Fixture-only BEO publication pilot execution request gate.

This module builds deterministic local request packages for a future explicit
human decision about one BEO publication pilot. It does not approve or execute
publication, publish BEOs, capture live approval, sign artifacts, write storage,
append ledgers, execute rollback, generate RTM, run BLK-test/Codex/BLK-pipe,
read protected BLK-req bodies, or scan/mutate target repositories.
"""

from __future__ import annotations

from datetime import datetime
import re
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_decision_package import (
    DECISION_PACKAGE_READY,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as DECISION_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as DECISION_PROOF_OBLIGATIONS,
    NOT_GENERATED,
    SELECTED_FRONTIER as DECISION_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as DECISION_SIDE_EFFECT_FLAGS,
)

REQUEST_READY = "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_READY_FOR_EXPLICIT_HUMAN_APPROVAL_NOT_EXECUTED"
SELECTED_FRONTIER = "beo_publication_pilot_execution_request"
REQUEST_SCOPE = "BEO_PUBLICATION_PILOT_EXECUTION_REQUEST_GATE_ONLY_NOT_APPROVAL_NOT_EXECUTION"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-12T00:00:00+10:00")
HASH_PATTERN = r"sha256:[0-9a-f]{64}"

SIDE_EFFECT_FLAGS = (
    "approval_granted",
    "publication_approved",
    "pilot_execution_authorized",
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

EXACT_EXCLUDED_AUTHORITIES = set(DECISION_EXCLUDED_AUTHORITIES) | {
    "PUBLICATION_PILOT_EXECUTION_APPROVAL_CAPTURE",
    "PUBLICATION_PILOT_RUN_ID_CONSUMPTION",
    "BEO_PUBLICATION_PILOT_RUNTIME",
    "SOURCE_OR_GIT_MUTATION",
}

EXACT_PROOF_OBLIGATIONS = {
    "UPSTREAM_DECISION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE",
    "FRESH_APPROVAL_ID_AND_RUN_ID_RESERVED_FOR_FUTURE_APPROVAL",
    "EXPLICIT_HUMAN_APPROVAL_REQUIRED_BEFORE_ANY_PILOT_EXECUTION",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_EXECUTION",
    "REPLAY_EXPIRY_AND_OPERATOR_STOP_CONTROLS_BOUND",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_PUBLICATION_PILOT_EXECUTION",
}

_REQUEST_KEYS = {
    "request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "requested_at",
    "expires_at",
    "upstream_decision_package_id",
    "upstream_decision_package_hash",
    "exact_beo_id",
    "exact_beo_hash",
    "exact_target_id",
    "pilot_request_id",
    "future_approval_id_candidate",
    "future_run_id_candidate",
    "approval_granted",
    "publication_approved",
    "pilot_execution_authorized",
    "publication_performed",
    "expired",
    "replayed",
    "stale",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
}

_ATTESTATION_KEYS = {
    "request_package_not_approval",
    "pilot_requires_future_explicit_human_approval",
    "publication_not_performed",
    "rtm_generation_excluded",
    "protected_body_reads_excluded",
    "no_side_effects",
}

_DECISION_PACKAGE_KEYS = {
    "decision_status",
    "decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "envelope_id",
    "envelope_hash",
    "beo_id",
    "beo_hash",
    "target_id",
    "target_ref",
    "candidate_id",
    "source_evidence_hash",
    "trace_artifacts",
    "envelope_pilot_id",
    "envelope_run_id",
    "envelope_approval_id",
    "signer_policy_hash",
    "storage_policy_hash",
    "ledger_policy_hash",
    "rollback_policy_hash",
    "audit_bundle_hash",
    "operator_stop_control",
    "pilot_replay_protection",
    "pilot_request_id",
    "future_approval_id_candidate",
    "future_run_id_candidate",
    "future_publication_pilot_requires_explicit_approval",
    "next_required_authority",
    "requested_at",
    "expires_at",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "beo_publication",
    "rtm_status",
    "decision_package_hash",
    *DECISION_SIDE_EFFECT_FLAGS,
}

_CANONICAL_DECISION_PACKAGE_FIELDS = {
    "decision_package_id": "BEO-PUBLICATION-DECISION-PACKAGE-083-001",
    "operator_identity": "discord:684235178083745819",
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
    "envelope_pilot_id": "BEO-PUBLICATION-PILOT-055-001",
    "envelope_run_id": "RUN-BLK-SYSTEM-055-PUBLICATION-PILOT-001",
    "envelope_approval_id": "APPROVAL-BLK-SYSTEM-055-BEO-PUBLICATION-001",
    "signer_policy_hash": "sha256:" + "e" * 64,
    "storage_policy_hash": "sha256:" + "f" * 64,
    "ledger_policy_hash": "sha256:" + "1" * 64,
    "rollback_policy_hash": "sha256:" + "2" * 64,
    "audit_bundle_hash": "sha256:" + "3" * 64,
    "operator_stop_control": "discord-stop-required-before-runtime",
    "pilot_replay_protection": "fresh-approval-and-run-id-required",
    "pilot_request_id": "BEO-PUBLICATION-PILOT-REQUEST-083-001",
    "future_approval_id_candidate": "APPROVAL-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
    "future_run_id_candidate": "RUN-BLK-SYSTEM-084-BEO-PUBLICATION-PILOT-001",
    "requested_at": "2099-05-12T07:30:00+10:00",
    "expires_at": "2099-05-12T08:30:00+10:00",
    "decision_package_hash": "sha256:2abdc185164bfef129f9011f53192e70c8f01af76d00ab0039c6072c4358ff5b",
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
    "publicationapproved",
    "publicationapprovalgranted",
    "publicationauthoritygranted",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "rtmauthorized",
    "rtmauthoritygranted",
    "rtmauthoritybeforepublicationprerequisites",
    "protectedbodyauthorized",
    "protectedbodyreadauthorized",
    "protectedblkreqbodyreadsauthorized",
    "pilotexecutionauthorized",
    "publicationpilotexecutionauthorized",
    "publicationpilotexecutionapproved",
    "publicationpilotexecuted",
    "publicationperformed",
    "runtimepublishedbeo",
    "publishbeo",
    "livepublicationapprovalcapture",
    "approvalcaptured",
    "signaturegenerated",
    "cryptographicsigning",
    "immutablestoragewrite",
    "immutablestoragewritten",
    "publicledgerappend",
    "publicledgermutation",
    "publicledgermutated",
    "rollbackexecuted",
    "revocationexecuted",
    "supersessionexecuted",
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
    "protectedblkreqbody",
    "targetreposcan",
    "targetrepoauthority",
    "targetrepositoryauthority",
    "targetrepoauthorized",
    "targetrepomutation",
    "bebdispatch",
    "beocloseoutexecution",
    "livecodexexecution",
    "blkpipeexecution",
    "blktestruntime",
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
)


def build_beo_publication_pilot_execution_request(
    decision_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a review-ready pilot execution request without approving or executing it."""

    upstream = _validate_decision_package(decision_package)
    request = _validate_execution_request(execution_request, upstream)

    package = {
        "request_status": REQUEST_READY,
        "request_package_id": request["request_package_id"],
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_decision_package_id": upstream["decision_package_id"],
        "upstream_decision_package_hash": upstream["decision_package_hash"],
        "envelope_id": upstream["envelope_id"],
        "envelope_hash": upstream["envelope_hash"],
        "beo_id": upstream["beo_id"],
        "beo_hash": upstream["beo_hash"],
        "target_id": upstream["target_id"],
        "target_ref": upstream["target_ref"],
        "candidate_id": upstream["candidate_id"],
        "source_evidence_hash": upstream["source_evidence_hash"],
        "trace_artifacts": upstream["trace_artifacts"],
        "signer_policy_hash": upstream["signer_policy_hash"],
        "storage_policy_hash": upstream["storage_policy_hash"],
        "ledger_policy_hash": upstream["ledger_policy_hash"],
        "rollback_policy_hash": upstream["rollback_policy_hash"],
        "audit_bundle_hash": upstream["audit_bundle_hash"],
        "operator_stop_control": upstream["operator_stop_control"],
        "pilot_replay_protection": upstream["pilot_replay_protection"],
        "upstream_pilot_request_id": upstream["pilot_request_id"],
        "upstream_future_approval_id_candidate": upstream["future_approval_id_candidate"],
        "upstream_future_run_id_candidate": upstream["future_run_id_candidate"],
        "pilot_request_id": request["pilot_request_id"],
        "future_approval_id_candidate": request["future_approval_id_candidate"],
        "future_run_id_candidate": request["future_run_id_candidate"],
        "approval_required_before_execution": True,
        "next_required_authority": "EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED",
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "operator_attestation": request["operator_attestation"],
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "beo_publication": "PILOT_EXECUTION_REQUEST_ONLY_NOT_APPROVED_NOT_PUBLISHED",
        "rtm_status": NOT_GENERATED,
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "request_package_hash"}
    )
    return package


def _validate_decision_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "decision_package")
    _enforce_exact_keys(package, _DECISION_PACKAGE_KEYS, "decision_package")
    if _required_string(package.get("decision_status"), "decision_status", scan=False) != DECISION_PACKAGE_READY:
        raise ValueError("decision package must be BLK-083 ready for human review")
    if _required_string(package.get("decision_scope"), "decision_scope", scan=False) != DECISION_SCOPE:
        raise ValueError("decision package must remain BLK-083 decision-package only")
    if _required_string(package.get("selected_frontier"), "selected_frontier", scan=False) != DECISION_SELECTED_FRONTIER:
        raise ValueError("upstream selected_frontier must be beo_publication_pilot_request")
    if package.get("future_publication_pilot_requires_explicit_approval") is not True:
        raise ValueError("decision package must require future explicit publication pilot approval")
    if _required_string(package.get("next_required_authority"), "next_required_authority", scan=False) != "FUTURE_EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED":
        raise ValueError("decision package must not grant publication pilot authority")
    if _required_string(package.get("beo_publication"), "beo_publication", scan=False) != "DECISION_PACKAGE_ONLY_NOT_APPROVED_NOT_PUBLISHED":
        raise ValueError("decision package must remain not published")
    if _required_string(package.get("rtm_status"), "rtm_status", scan=False) != NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    for flag in DECISION_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    for key in [
        "decision_package_id",
        "operator_identity",
        "envelope_id",
        "target_id",
        "target_ref",
        "candidate_id",
        "beo_id",
        "envelope_pilot_id",
        "envelope_run_id",
        "envelope_approval_id",
        "operator_stop_control",
        "pilot_replay_protection",
        "pilot_request_id",
        "future_approval_id_candidate",
        "future_run_id_candidate",
    ]:
        _required_string(package.get(key), key)
    for key in [
        "envelope_hash",
        "beo_hash",
        "source_evidence_hash",
        "signer_policy_hash",
        "storage_policy_hash",
        "ledger_policy_hash",
        "rollback_policy_hash",
        "audit_bundle_hash",
    ]:
        _required_hash(package.get(key), key)
    _parse_timestamp(package.get("requested_at"), "decision_package.requested_at")
    _parse_timestamp(package.get("expires_at"), "decision_package.expires_at")
    _validate_trace_artifacts(package.get("trace_artifacts"))
    _validate_exact_set(package.get("proof_obligations"), DECISION_PROOF_OBLIGATIONS, "decision_package proof_obligations")
    _validate_exact_set(package.get("excluded_authorities"), DECISION_EXCLUDED_AUTHORITIES, "decision_package excluded_authorities")
    decision_hash = _required_hash(package.get("decision_package_hash"), "decision_package_hash")
    expected_hash = _canonical_hash({key: value for key, value in package.items() if key != "decision_package_hash"})
    if decision_hash != expected_hash:
        raise ValueError("decision_package_hash does not match canonical decision package")
    return package


def _validate_execution_request(request: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_exact_keys(request, _REQUEST_KEYS, "execution_request")
    if _required_string(request.get("request_scope"), "request_scope", scan=False) != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if _required_string(request.get("selected_frontier"), "selected_frontier", scan=False) != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    for key in [
        "request_package_id",
        "operator_identity",
        "upstream_decision_package_id",
        "exact_beo_id",
        "exact_target_id",
        "pilot_request_id",
        "future_approval_id_candidate",
        "future_run_id_candidate",
    ]:
        _required_string(request.get(key), key)
    for key in ["upstream_decision_package_hash", "exact_beo_hash"]:
        _required_hash(request.get(key), key)
    for flag in ["approval_granted", "publication_approved", "pilot_execution_authorized", "publication_performed"]:
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
    if request["upstream_decision_package_id"] != package["decision_package_id"]:
        raise ValueError("upstream_decision_package_id does not match decision package")
    if request["upstream_decision_package_hash"] != package["decision_package_hash"]:
        raise ValueError("upstream_decision_package_hash does not match decision package")
    if request["exact_beo_id"] != package["beo_id"]:
        raise ValueError("exact_beo_id does not match decision package")
    if request["exact_beo_hash"] != package["beo_hash"]:
        raise ValueError("exact_beo_hash does not match decision package")
    if request["exact_target_id"] != package["target_id"]:
        raise ValueError("exact_target_id does not match decision package")
    _validate_canonical_decision_fixture(package)
    consumed_upstream_ids = {
        package["decision_package_id"],
        package["envelope_id"],
        package["beo_id"],
        package["target_id"],
        package["candidate_id"],
        package["envelope_pilot_id"],
        package["envelope_run_id"],
        package["envelope_approval_id"],
        package["pilot_request_id"],
        package["future_approval_id_candidate"],
        package["future_run_id_candidate"],
    }
    if request["request_package_id"] in consumed_upstream_ids:
        raise ValueError("request_package_id must be fresh")
    if request["pilot_request_id"] in consumed_upstream_ids:
        raise ValueError("pilot_request_id must be fresh")
    if request["future_approval_id_candidate"] == request["future_run_id_candidate"]:
        raise ValueError("future approval and run candidates must be distinct")
    request_identity_values = [
        request["request_package_id"],
        request["pilot_request_id"],
        request["future_approval_id_candidate"],
        request["future_run_id_candidate"],
    ]
    if len(set(request_identity_values)) != len(request_identity_values):
        raise ValueError("request identifiers must be fresh and distinct")
    if request["future_approval_id_candidate"] in consumed_upstream_ids:
        raise ValueError("future_approval_id_candidate must be fresh")
    if request["future_run_id_candidate"] in consumed_upstream_ids:
        raise ValueError("future_run_id_candidate must be fresh")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_canonical_decision_fixture(package: dict[str, Any]) -> None:
    for key, expected in _CANONICAL_DECISION_PACKAGE_FIELDS.items():
        if package.get(key) != expected:
            raise ValueError("decision package must match canonical BLK-083 fixture")


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _validate_trace_artifacts(trace_artifacts: Any) -> None:
    if not isinstance(trace_artifacts, list) or not trace_artifacts:
        raise ValueError("trace_artifacts must be a non-empty list")
    seen = set()
    for index, artifact in enumerate(trace_artifacts):
        _require_dict(artifact, f"trace_artifacts[{index}]")
        _enforce_exact_keys(artifact, {"kind", "id", "version_hash"}, f"trace_artifacts[{index}]")
        kind = _required_string(artifact.get("kind"), "trace artifact kind", scan=False)
        if kind not in {"REQ", "UC", "BEB", "BEO", "BLK", "EVIDENCE"}:
            raise ValueError("trace artifact kind must be REQ, UC, BEB, BEO, BLK, or EVIDENCE")
        artifact_id = _required_string(artifact.get("id"), "trace artifact id")
        version_hash = _required_hash(artifact.get("version_hash"), "version_hash")
        identity = (kind, artifact_id)
        if identity in seen:
            raise ValueError("trace_artifacts must not contain duplicate identities")
        seen.add(identity)


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
        raise ValueError(f"{label} must be a dictionary")
    return value


def _enforce_exact_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    for key in sorted(allowed - set(value), key=str):
        raise ValueError(f"{label} missing required field {key!r}")
    for key in sorted(set(value) - allowed, key=str):
        _reject_forbidden_key(str(key))
        raise ValueError(f"{label} unexpected field {key!r}")


def _required_string(value: Any, label: str, *, scan: bool = True) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    if scan:
        _scan_text(value)
    return value


def _required_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(HASH_PATTERN, value):
        raise ValueError(f"{label} must be a sha256 hash")
    return value


def _required_false(value: Any, label: str) -> None:
    if value is not False:
        raise ValueError(f"{label} must remain false")


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed


def _scan_text(value: str) -> None:
    for variant in _decoded_text_variants(value):
        normalized = _normalize(variant)
        lowered = variant.lower()
        if any(marker in normalized for marker in _SECRET_MARKERS):
            raise ValueError("secret-bearing field")
        if any(marker in normalized for marker in _FORBIDDEN_NORMALIZED_MARKERS) or any(
            marker in lowered for marker in ("docs/active", "docs\\active", "docs%2factive", "docs%252factive")
        ):
            raise ValueError("authority-laundering text")


def _reject_forbidden_key(key: str) -> None:
    for variant in _decoded_text_variants(key):
        normalized = _normalize(variant)
        if any(marker in normalized for marker in _SECRET_MARKERS):
            raise ValueError("secret-bearing field")
        if any(marker in normalized for marker in _FORBIDDEN_NORMALIZED_MARKERS):
            raise ValueError("forbidden authority field")


def _decoded_text_variants(value: str) -> tuple[str, ...]:
    variants = []
    current = str(value)
    for _ in range(5):
        variants.append(current)
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
        current = decoded
    return tuple(variants)


def _percent_decode_once(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))

    return re.sub(r"%([0-9a-fA-F]{2})", replace, value)


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", _split_camel(value).lower())


def _split_camel(value: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
