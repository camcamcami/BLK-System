"""Fixture-only BEO publication decision package / pilot request.

This module builds deterministic local human-review packages for deciding whether a
future sprint should grant an exact one-run BEO publication pilot. It does not
publish BEOs, capture live approval, sign artifacts, write immutable storage,
append ledgers, execute rollback, generate RTM, run BLK-test/Codex/BLK-pipe, read
protected BLK-req bodies, or scan/mutate target repositories.
"""

from __future__ import annotations

from datetime import datetime
import re
from typing import Any

from authoritative_beo_publication_approval_envelope import (
    APPROVAL_ENVELOPE_READY,
    EXACT_EXCLUDED_AUTHORITIES as ENVELOPE_EXCLUDED_AUTHORITIES,
)
from authoritative_beo_publication_authority_request import _canonical_hash

DECISION_PACKAGE_READY = "BEO_PUBLICATION_DECISION_PACKAGE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PUBLISHED"
SELECTED_FRONTIER = "beo_publication_pilot_request"
DECISION_SCOPE = "BEO_PUBLICATION_DECISION_PACKAGE_ONLY_NOT_PUBLICATION_APPROVAL"
NOT_GENERATED = "NOT_GENERATED"
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
)

EXACT_EXCLUDED_AUTHORITIES = {
    "ACTUAL_AUTHORITATIVE_BEO_PUBLICATION",
    "PUBLICATION_APPROVAL_GRANTED",
    "PUBLICATION_PILOT_EXECUTION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
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
    "APPROVAL_ENVELOPE_IDENTITY_AND_HASH_BOUND",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "PUBLICATION_TARGET_IDENTITY_BOUND_WITHOUT_WRITE",
    "SIGNER_POLICY_WITHOUT_KEY_MATERIAL_BOUND",
    "STORAGE_POLICY_WITHOUT_IMMUTABLE_WRITE_BOUND",
    "LEDGER_POLICY_WITHOUT_APPEND_BOUND",
    "ROLLBACK_REVOCATION_SUPERSESSION_POLICY_WITHOUT_EXECUTION_BOUND",
    "AUDIT_BUNDLE_HASH_BOUND",
    "FRESH_APPROVAL_ID_AND_RUN_ID_REQUIRED_FOR_FUTURE_PILOT",
    "REPLAY_EXPIRY_AND_OPERATOR_STOP_CONTROLS_REQUIRED",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_REQUIRED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_PUBLICATION_PILOT",
}

_ENVELOPE_KEYS = {
    "envelope_status",
    "envelope_id",
    "operator_identity",
    "approval_scope",
    "request_id",
    "request_hash",
    "target_id",
    "target_ref",
    "candidate_id",
    "beo_id",
    "beo_hash",
    "source_evidence_hash",
    "trace_artifacts",
    "pilot_id",
    "run_id",
    "approval_id",
    "requested_at",
    "expires_at",
    "signer_policy",
    "storage_policy",
    "ledger_policy",
    "rollback_policy",
    "audit_bundle",
    "pilot_controls",
    "excluded_authorities",
    "publication_performed",
    "beo_publication",
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
    "rtm_status",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_read",
    "envelope_hash",
}

_DECISION_REQUEST_KEYS = {
    "decision_package_id",
    "operator_identity",
    "decision_scope",
    "selected_frontier",
    "requested_at",
    "expires_at",
    "exact_envelope_id",
    "exact_envelope_hash",
    "exact_beo_id",
    "exact_beo_hash",
    "exact_target_id",
    "pilot_request_id",
    "future_approval_id_candidate",
    "future_run_id_candidate",
    "approval_granted",
    "publication_approved",
    "pilot_execution_authorized",
    "expired",
    "replayed",
    "stale",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
}

_ATTESTATION_KEYS = {
    "decision_package_not_approval",
    "publication_pilot_requires_future_human_approval",
    "rtm_generation_excluded",
    "protected_body_reads_excluded",
    "no_side_effects",
}

_SIGNER_KEYS = {"signer_identity", "signer_policy_hash", "key_material_accessed", "signature_generated", "secret_read"}
_STORAGE_KEYS = {"storage_target_identity", "storage_policy_hash", "immutable_storage_written", "storage_write_attempted"}
_LEDGER_KEYS = {"ledger_target_identity", "ledger_policy_hash", "public_ledger_mutated", "ledger_append_attempted"}
_ROLLBACK_KEYS = {"rollback_fixture_identity", "rollback_policy_hash", "rollback_executed", "revocation_executed", "supersession_executed"}
_AUDIT_KEYS = {
    "audit_bundle_id",
    "audit_bundle_hash",
    "request_hash",
    "beo_hash",
    "source_evidence_hash",
    "protected_body_read",
    "rtm_generated",
    "drift_decision_made",
}
_PILOT_CONTROLS_KEYS = {
    "operator_stop_control",
    "max_output_bytes",
    "timeout_seconds",
    "single_run_only",
    "replay_protection",
    "publication_performed",
    "signature_generated",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_executed",
    "rtm_generated",
    "protected_body_read",
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
    "publicationauthority",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "beopublicationapprovalgranted",
    "publicationapprovalgranted",
    "publicationauthoritygranted",
    "approvedforpublication",
    "authoritativebeopublication",
    "publishbeo",
    "rtmgeneration",
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
    "immutablestoragewrite",
    "immutablestoragewritten",
    "publicledgerappend",
    "publicledgermutation",
    "publicledgermutated",
    "rollbackexecuted",
    "revocationexecuted",
    "supersessionexecuted",
    "signaturegenerated",
    "cryptographicsigning",
    "npmrun",
    "npminstall",
    "pnpminstall",
    "yarninstall",
    "pipinstall",
    "goget",
    "curl",
    "wget",
    "targetreposcan",
    "targetrepomutation",
    "bebdispatch",
    "beocloseoutexecution",
    "livecodexexecution",
    "blkpipeexecution",
    "blktestruntime",
    "productionsandbox",
    "hostisolation",
)

_ALLOWED_ATTESTATION_TRUE_FIELDS = set(_ATTESTATION_KEYS)


def build_beo_publication_decision_package(
    approval_envelope_package: dict[str, Any], decision_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a review-ready decision package without granting publication authority."""

    envelope = _validate_approval_envelope_package(approval_envelope_package)
    request = _validate_decision_request(decision_request, envelope)

    package = {
        "decision_status": DECISION_PACKAGE_READY,
        "decision_package_id": request["decision_package_id"],
        "operator_identity": request["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "envelope_id": envelope["envelope_id"],
        "envelope_hash": envelope["envelope_hash"],
        "beo_id": envelope["beo_id"],
        "beo_hash": envelope["beo_hash"],
        "target_id": envelope["target_id"],
        "target_ref": envelope["target_ref"],
        "candidate_id": envelope["candidate_id"],
        "source_evidence_hash": envelope["source_evidence_hash"],
        "trace_artifacts": envelope["trace_artifacts"],
        "envelope_pilot_id": envelope["pilot_id"],
        "envelope_run_id": envelope["run_id"],
        "envelope_approval_id": envelope["approval_id"],
        "signer_policy_hash": envelope["signer_policy"]["signer_policy_hash"],
        "storage_policy_hash": envelope["storage_policy"]["storage_policy_hash"],
        "ledger_policy_hash": envelope["ledger_policy"]["ledger_policy_hash"],
        "rollback_policy_hash": envelope["rollback_policy"]["rollback_policy_hash"],
        "audit_bundle_hash": envelope["audit_bundle"]["audit_bundle_hash"],
        "operator_stop_control": envelope["pilot_controls"]["operator_stop_control"],
        "pilot_replay_protection": envelope["pilot_controls"]["replay_protection"],
        "pilot_request_id": request["pilot_request_id"],
        "future_approval_id_candidate": request["future_approval_id_candidate"],
        "future_run_id_candidate": request["future_run_id_candidate"],
        "future_publication_pilot_requires_explicit_approval": True,
        "next_required_authority": "FUTURE_EXPLICIT_HUMAN_PUBLICATION_PILOT_APPROVAL_REQUIRED_NOT_GRANTED",
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "operator_attestation": request["operator_attestation"],
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "beo_publication": "DECISION_PACKAGE_ONLY_NOT_APPROVED_NOT_PUBLISHED",
        "rtm_status": NOT_GENERATED,
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "decision_package_hash"}
    )
    return package


def _validate_approval_envelope_package(envelope: dict[str, Any]) -> dict[str, Any]:
    _require_dict(envelope, "approval_envelope_package")
    _enforce_exact_keys(envelope, _ENVELOPE_KEYS, "approval_envelope_package")
    if _required_string(envelope.get("envelope_status"), "envelope_status", scan=False) != APPROVAL_ENVELOPE_READY:
        raise ValueError("approval envelope package must be BLK-060 ready for human review")
    if _required_string(envelope.get("approval_scope"), "approval_scope", scan=False) != "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_ONLY_NOT_PUBLICATION":
        raise ValueError("approval_scope must remain BLK-060 approval-envelope only")
    if _required_string(envelope.get("beo_publication"), "beo_publication", scan=False) != "APPROVAL_ENVELOPE_ONLY_NOT_PUBLISHED":
        raise ValueError("beo_publication must remain APPROVAL_ENVELOPE_ONLY_NOT_PUBLISHED")
    if _required_string(envelope.get("rtm_status"), "rtm_status", scan=False) != NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")

    for key in [
        "envelope_id",
        "operator_identity",
        "request_id",
        "target_id",
        "target_ref",
        "candidate_id",
        "beo_id",
        "pilot_id",
        "run_id",
        "approval_id",
    ]:
        _required_string(envelope.get(key), key)
    for key in ["request_hash", "beo_hash", "source_evidence_hash"]:
        _required_hash(envelope.get(key), key)
    requested_at = _parse_timestamp(envelope.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(envelope.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("envelope expires_at must be after requested_at")

    for flag in [
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
    ]:
        _required_false(envelope.get(flag), flag)
    _validate_exact_set(
        envelope.get("excluded_authorities"), ENVELOPE_EXCLUDED_AUTHORITIES, "approval_envelope_package excluded_authorities"
    )
    _validate_trace_artifacts(envelope.get("trace_artifacts"))
    _validate_policy(
        envelope.get("signer_policy"),
        _SIGNER_KEYS,
        "signer_policy",
        false_flags=("key_material_accessed", "signature_generated", "secret_read"),
        string_fields=("signer_identity",),
        hash_fields=("signer_policy_hash",),
    )
    _validate_policy(
        envelope.get("storage_policy"),
        _STORAGE_KEYS,
        "storage_policy",
        false_flags=("immutable_storage_written", "storage_write_attempted"),
        string_fields=("storage_target_identity",),
        hash_fields=("storage_policy_hash",),
    )
    _validate_policy(
        envelope.get("ledger_policy"),
        _LEDGER_KEYS,
        "ledger_policy",
        false_flags=("public_ledger_mutated", "ledger_append_attempted"),
        string_fields=("ledger_target_identity",),
        hash_fields=("ledger_policy_hash",),
    )
    _validate_policy(
        envelope.get("rollback_policy"),
        _ROLLBACK_KEYS,
        "rollback_policy",
        false_flags=("rollback_executed", "revocation_executed", "supersession_executed"),
        string_fields=("rollback_fixture_identity",),
        hash_fields=("rollback_policy_hash",),
    )
    _validate_audit_bundle(envelope.get("audit_bundle"), envelope)
    _validate_pilot_controls(envelope.get("pilot_controls"))

    envelope_hash = _required_hash(envelope.get("envelope_hash"), "envelope_hash")
    expected_hash = _canonical_hash({key: value for key, value in envelope.items() if key != "envelope_hash"})
    if envelope_hash != expected_hash:
        raise ValueError("envelope_hash does not match canonical approval envelope")
    return envelope


def _validate_decision_request(request: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "decision_request")
    _enforce_allowed_keys(request, _DECISION_REQUEST_KEYS, "decision_request")
    if _required_string(request.get("decision_scope"), "decision_scope", scan=False) != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if _required_string(request.get("selected_frontier"), "selected_frontier", scan=False) != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    for key in ["decision_package_id", "operator_identity", "pilot_request_id", "future_approval_id_candidate", "future_run_id_candidate"]:
        _required_string(request.get(key), key)
    for flag in ["approval_granted", "publication_approved", "pilot_execution_authorized"]:
        _required_false(request.get(flag), flag)
    for flag in ["expired", "replayed", "stale"]:
        if request.get(flag) is not False:
            raise ValueError(f"decision request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if _required_string(request.get("exact_envelope_id"), "exact_envelope_id") != envelope["envelope_id"]:
        raise ValueError("exact_envelope_id does not match approval envelope")
    if _required_hash(request.get("exact_envelope_hash"), "exact_envelope_hash") != envelope["envelope_hash"]:
        raise ValueError("exact_envelope_hash does not match approval envelope")
    if _required_string(request.get("exact_beo_id"), "exact_beo_id") != envelope["beo_id"]:
        raise ValueError("exact_beo_id does not match approval envelope")
    if _required_hash(request.get("exact_beo_hash"), "exact_beo_hash") != envelope["beo_hash"]:
        raise ValueError("exact_beo_hash does not match approval envelope")
    if _required_string(request.get("exact_target_id"), "exact_target_id") != envelope["target_id"]:
        raise ValueError("exact_target_id does not match approval envelope")
    if request["future_approval_id_candidate"] == envelope["approval_id"]:
        raise ValueError("future_approval_id_candidate must be fresh")
    if request["future_run_id_candidate"] == envelope["run_id"]:
        raise ValueError("future_run_id_candidate must be fresh")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_allowed_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _validate_trace_artifacts(trace_artifacts: Any) -> list[dict[str, Any]]:
    if not isinstance(trace_artifacts, list) or not trace_artifacts:
        raise ValueError("trace_artifacts must be a non-empty list")
    normalized = []
    seen = set()
    for index, artifact in enumerate(trace_artifacts):
        _require_dict(artifact, f"trace_artifacts[{index}]")
        _enforce_allowed_keys(artifact, {"kind", "id", "version_hash"}, f"trace_artifacts[{index}]")
        kind = _required_string(artifact.get("kind"), "trace artifact kind", scan=False)
        if kind not in {"REQ", "UC", "BEB", "BEO", "BLK", "EVIDENCE"}:
            raise ValueError("trace artifact kind must be REQ, UC, BEB, BEO, BLK, or EVIDENCE")
        artifact_id = _required_string(artifact.get("id"), "trace artifact id")
        _scan_text(artifact_id)
        version_hash = _required_hash(artifact.get("version_hash"), "version_hash")
        identity = (kind, artifact_id)
        if identity in seen:
            raise ValueError("trace_artifacts must not contain duplicate identities")
        seen.add(identity)
        normalized.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return normalized


def _validate_policy(
    value: Any,
    allowed_keys: set[str],
    label: str,
    *,
    false_flags: tuple[str, ...],
    string_fields: tuple[str, ...],
    hash_fields: tuple[str, ...],
) -> dict[str, Any]:
    policy = _require_dict(value, label)
    _enforce_exact_keys(policy, allowed_keys, label)
    for key in string_fields:
        _required_string(policy.get(key), key)
    for key in hash_fields:
        _required_hash(policy.get(key), key)
    for flag in false_flags:
        _required_false(policy.get(flag), flag)
    return policy


def _validate_audit_bundle(value: Any, envelope: dict[str, Any]) -> dict[str, Any]:
    audit = _require_dict(value, "audit_bundle")
    _enforce_exact_keys(audit, _AUDIT_KEYS, "audit_bundle")
    _required_string(audit.get("audit_bundle_id"), "audit_bundle_id")
    _required_hash(audit.get("audit_bundle_hash"), "audit_bundle_hash")
    if _required_hash(audit.get("request_hash"), "audit_bundle.request_hash") != envelope["request_hash"]:
        raise ValueError("audit_bundle request_hash does not match approval envelope")
    if _required_hash(audit.get("beo_hash"), "audit_bundle.beo_hash") != envelope["beo_hash"]:
        raise ValueError("audit_bundle beo_hash does not match approval envelope")
    if _required_hash(audit.get("source_evidence_hash"), "audit_bundle.source_evidence_hash") != envelope["source_evidence_hash"]:
        raise ValueError("audit_bundle source_evidence_hash does not match approval envelope")
    for flag in ["protected_body_read", "rtm_generated", "drift_decision_made"]:
        _required_false(audit.get(flag), flag)
    return audit


def _validate_pilot_controls(value: Any) -> dict[str, Any]:
    controls = _require_dict(value, "pilot_controls")
    _enforce_exact_keys(controls, _PILOT_CONTROLS_KEYS, "pilot_controls")
    _required_string(controls.get("operator_stop_control"), "operator_stop_control")
    _required_string(controls.get("replay_protection"), "replay_protection")
    for key in ["max_output_bytes", "timeout_seconds"]:
        if not isinstance(controls.get(key), int) or controls.get(key) <= 0:
            raise ValueError(f"{key} must be a positive integer")
    if controls.get("single_run_only") is not True:
        raise ValueError("single_run_only must be true")
    for flag in [
        "publication_performed",
        "signature_generated",
        "immutable_storage_written",
        "public_ledger_mutated",
        "rollback_executed",
        "rtm_generated",
        "protected_body_read",
    ]:
        _required_false(controls.get(flag), flag)
    return controls


def _validate_exact_set(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{label} entries must be strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    if set(value) != expected:
        raise ValueError(f"{label} must match exact denied authority set" if label == "excluded_authorities" else f"{label} must match exact set")


def _require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dictionary")
    return value


def _enforce_allowed_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    for key in sorted(set(value) - allowed, key=str):
        _reject_forbidden_key(str(key))
        raise ValueError(f"{label} unexpected field {key!r}")


def _enforce_exact_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    for key in sorted(allowed - set(value), key=str):
        raise ValueError(f"{label} missing required field {key!r}")
    _enforce_allowed_keys(value, allowed, label)


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


def _reject_forbidden_key(key: str) -> None:
    for variant in _decoded_text_variants(key):
        normalized = _normalize(variant)
        if any(marker in normalized for marker in _SECRET_MARKERS):
            raise ValueError("secret-bearing field")
        if any(marker in normalized for marker in _FORBIDDEN_NORMALIZED_MARKERS):
            raise ValueError("forbidden authority field")


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", _split_camel(value).lower())


def _split_camel(value: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
