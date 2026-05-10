"""Fixture-only authoritative BEO publication approval envelope.

This module validates and builds deterministic local approval-envelope / pilot-boundary
packages for a future authoritative BEO publication decision. It does not publish BEOs,
sign artifacts, write immutable storage, append public ledgers, execute rollback,
generate RTM output, or read protected BLK-req bodies.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from authoritative_beo_publication_authority_request import (
    AUTHORITY_REQUEST_READY,
    EXACT_EXCLUDED_AUTHORITIES as REQUEST_EXCLUDED_AUTHORITIES,
    _canonical_hash,
    _enforce_allowed_keys,
    _required_bool,
    _required_false,
    _required_hash,
    _required_string,
    _scan_nested,
    _validate_trace_artifacts,
)

APPROVAL_ENVELOPE_READY = "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION"
APPROVAL_SCOPE = "AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_ONLY_NOT_PUBLICATION"
TARGET_KIND = "FIXTURE_PUBLICATION_TARGET_ONLY"
NOT_GENERATED = "NOT_GENERATED"

EXACT_EXCLUDED_AUTHORITIES = {
    "ACTUAL_AUTHORITATIVE_BEO_PUBLICATION",
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
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "REUSABLE_BLK_TEST_SERVICE_STARTUP",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "LIVE_CODEX_EXECUTION",
    "SOURCE_OR_GIT_MUTATION_BY_BLK_TEST",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

_REQUEST_KEYS = {
    "request_status",
    "request_id",
    "operator_identity",
    "approval_scope",
    "candidate_id",
    "beo_id",
    "beo_hash",
    "beb_id",
    "source_evidence_hash",
    "trace_artifacts",
    "signer_policy",
    "storage_policy",
    "ledger_policy",
    "rollback_policy",
    "excluded_authorities",
    "publication_performed",
    "beo_publication",
    "runtime_published_beo_output",
    "live_publication_approval_captured",
    "signature_generated",
    "key_material_accessed",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generated",
    "rtm_status",
    "drift_decision_made",
    "protected_body_read",
    "active_vault_read",
    "request_hash",
}
_TARGET_KEYS = {
    "target_id",
    "target_kind",
    "target_ref",
    "beo_id",
    "beo_hash",
    "candidate_id",
    "source_evidence_hash",
    "immutable_storage_written",
    "public_ledger_mutated",
    "publication_performed",
    "operator_note",
}
_APPROVAL_KEYS = {
    "envelope_id",
    "operator_identity",
    "approval_scope",
    "approved_request_id",
    "approved_request_hash",
    "approved_target_id",
    "approved_beo_id",
    "approved_beo_hash",
    "source_evidence_hash",
    "pilot_id",
    "run_id",
    "approval_id",
    "requested_at",
    "expires_at",
    "expired",
    "replayed",
    "stale",
    "excluded_authorities",
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
_CONTROLS_KEYS = {
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


def build_authoritative_beo_publication_approval_envelope(
    authority_request_package: dict[str, Any],
    publication_target: dict[str, Any],
    approval_envelope: dict[str, Any],
    signer_policy: dict[str, Any],
    storage_policy: dict[str, Any],
    ledger_policy: dict[str, Any],
    rollback_policy: dict[str, Any],
    audit_bundle: dict[str, Any],
    pilot_controls: dict[str, Any],
) -> dict[str, Any]:
    """Build a publication approval-envelope fixture without publication side effects."""

    request = _validate_authority_request_package(authority_request_package)
    target = _validate_publication_target(publication_target, request)
    approval = _validate_approval_envelope(approval_envelope, request, target)
    signer = _validate_signer_policy(signer_policy)
    storage = _validate_storage_policy(storage_policy)
    ledger = _validate_ledger_policy(ledger_policy)
    rollback = _validate_rollback_policy(rollback_policy)
    audit = _validate_audit_bundle(audit_bundle, request)
    controls = _validate_pilot_controls(pilot_controls)

    envelope = {
        "envelope_status": APPROVAL_ENVELOPE_READY,
        "envelope_id": approval["envelope_id"],
        "operator_identity": approval["operator_identity"],
        "approval_scope": APPROVAL_SCOPE,
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "target_id": target["target_id"],
        "target_ref": target["target_ref"],
        "candidate_id": request["candidate_id"],
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "source_evidence_hash": request["source_evidence_hash"],
        "trace_artifacts": request["trace_artifacts"],
        "pilot_id": approval["pilot_id"],
        "run_id": approval["run_id"],
        "approval_id": approval["approval_id"],
        "requested_at": approval["requested_at"],
        "expires_at": approval["expires_at"],
        "signer_policy": signer,
        "storage_policy": storage,
        "ledger_policy": ledger,
        "rollback_policy": rollback,
        "audit_bundle": audit,
        "pilot_controls": controls,
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        "publication_performed": False,
        "beo_publication": "APPROVAL_ENVELOPE_ONLY_NOT_PUBLISHED",
        "runtime_published_beo_output": False,
        "live_publication_approval_captured": False,
        "signature_generated": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "ledger_append_attempted": False,
        "rollback_executed": False,
        "revocation_executed": False,
        "supersession_executed": False,
        "rtm_generated": False,
        "rtm_status": NOT_GENERATED,
        "drift_decision_made": False,
        "protected_body_read": False,
        "active_vault_read": False,
    }
    envelope["envelope_hash"] = _canonical_hash({k: v for k, v in envelope.items() if k != "envelope_hash"})
    return envelope


def _validate_authority_request_package(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority_request_package must be a dictionary")
    _enforce_allowed_keys(request, _REQUEST_KEYS, "authority_request_package")
    if _required_string(request.get("request_status"), "request_status") != AUTHORITY_REQUEST_READY:
        raise ValueError("authority request package must be BLK-057 request-ready")
    for flag in [
        "publication_performed",
        "runtime_published_beo_output",
        "live_publication_approval_captured",
        "signature_generated",
        "key_material_accessed",
        "immutable_storage_written",
        "public_ledger_mutated",
        "rollback_executed",
        "revocation_executed",
        "supersession_executed",
        "rtm_generated",
        "drift_decision_made",
        "protected_body_read",
        "active_vault_read",
    ]:
        _required_false(request.get(flag), flag)
    if _required_string(request.get("rtm_status"), "rtm_status") != NOT_GENERATED:
        raise ValueError("request rtm_status must remain NOT_GENERATED")
    _validate_request_exclusions(request.get("excluded_authorities"))
    trace_artifacts = _validate_request_trace_artifacts(request.get("trace_artifacts"))
    _validate_policy(request.get("signer_policy"), _SIGNER_KEYS, "authority_request_package.signer_policy", ["key_material_accessed", "signature_generated", "secret_read"])
    _validate_policy(request.get("storage_policy"), _STORAGE_KEYS, "authority_request_package.storage_policy", ["immutable_storage_written", "storage_write_attempted"])
    _validate_policy(request.get("ledger_policy"), _LEDGER_KEYS, "authority_request_package.ledger_policy", ["public_ledger_mutated", "ledger_append_attempted"])
    _validate_policy(
        request.get("rollback_policy"),
        _ROLLBACK_KEYS,
        "authority_request_package.rollback_policy",
        ["rollback_executed", "revocation_executed", "supersession_executed"],
    )
    request_hash = _required_hash(request.get("request_hash"), "request_hash")
    if request_hash != _canonical_hash({key: value for key, value in request.items() if key != "request_hash"}):
        raise ValueError("request_hash does not match canonical authority request package")
    return {
        "request_id": _required_string(request.get("request_id"), "request_id"),
        "request_hash": request_hash,
        "candidate_id": _required_string(request.get("candidate_id"), "candidate_id"),
        "beo_id": _required_string(request.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(request.get("beo_hash"), "beo_hash"),
        "source_evidence_hash": _required_hash(request.get("source_evidence_hash"), "source_evidence_hash"),
        "trace_artifacts": trace_artifacts,
    }


def _validate_request_trace_artifacts(value: Any) -> list[dict[str, str]]:
    trace_artifacts = _validate_trace_artifacts(value)
    allowed_kinds = {"REQ", "UC", "BEB", "BEO", "BLK", "EVIDENCE"}
    for artifact in trace_artifacts:
        _scan_nested({"kind": artifact["kind"], "id": artifact["id"]}, "trace_artifacts")
        if artifact["kind"] not in allowed_kinds:
            raise ValueError("trace artifact kind must be REQ, UC, BEB, BEO, BLK, or EVIDENCE")
    return trace_artifacts


def _validate_request_exclusions(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != REQUEST_EXCLUDED_AUTHORITIES
        or len(excluded) != len(REQUEST_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("authority_request_package excluded_authorities must match BLK-057 denied authority set")


def _validate_publication_target(target: dict[str, Any], request: dict[str, Any]) -> dict[str, str]:
    if not isinstance(target, dict):
        raise ValueError("publication_target must be a dictionary")
    _scan_nested(target, "publication_target")
    _enforce_allowed_keys(target, _TARGET_KEYS, "publication_target")
    if _required_string(target.get("target_kind"), "target_kind") != TARGET_KIND:
        raise ValueError("target_kind must be FIXTURE_PUBLICATION_TARGET_ONLY")
    if _required_string(target.get("beo_id"), "beo_id") != request["beo_id"]:
        raise ValueError("publication target beo_id does not match request")
    if _required_hash(target.get("beo_hash"), "beo_hash") != request["beo_hash"]:
        raise ValueError("publication target beo_hash does not match request")
    if _required_string(target.get("candidate_id"), "candidate_id") != request["candidate_id"]:
        raise ValueError("publication target candidate_id does not match request")
    if _required_hash(target.get("source_evidence_hash"), "source_evidence_hash") != request["source_evidence_hash"]:
        raise ValueError("publication target source_evidence_hash does not match request")
    for flag in ["immutable_storage_written", "public_ledger_mutated", "publication_performed"]:
        _required_false(target.get(flag), flag)
    return {
        "target_id": _required_string(target.get("target_id"), "target_id"),
        "target_ref": _required_string(target.get("target_ref"), "target_ref"),
    }


def _validate_approval_envelope(approval: dict[str, Any], request: dict[str, Any], target: dict[str, str]) -> dict[str, str]:
    if not isinstance(approval, dict):
        raise ValueError("approval_envelope must be a dictionary")
    _scan_nested({k: v for k, v in approval.items() if k not in {"approval_scope", "excluded_authorities"}}, "approval_envelope")
    _enforce_allowed_keys(approval, _APPROVAL_KEYS, "approval_envelope")
    if _required_string(approval.get("approval_scope"), "approval_scope") != APPROVAL_SCOPE:
        raise ValueError("approval_scope must be AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_ONLY_NOT_PUBLICATION")
    if _required_string(approval.get("approved_request_id"), "approved_request_id") != request["request_id"]:
        raise ValueError("approved_request_id does not match request")
    if _required_hash(approval.get("approved_request_hash"), "approved_request_hash") != request["request_hash"]:
        raise ValueError("approved_request_hash does not match request")
    if _required_string(approval.get("approved_target_id"), "approved_target_id") != target["target_id"]:
        raise ValueError("approved_target_id does not match publication target")
    if _required_string(approval.get("approved_beo_id"), "approved_beo_id") != request["beo_id"]:
        raise ValueError("approved_beo_id does not match request")
    if _required_hash(approval.get("approved_beo_hash"), "approved_beo_hash") != request["beo_hash"]:
        raise ValueError("approved_beo_hash does not match request")
    if _required_hash(approval.get("source_evidence_hash"), "source_evidence_hash") != request["source_evidence_hash"]:
        raise ValueError("approval source_evidence_hash does not match request")
    for flag in ["expired", "replayed", "stale"]:
        if _required_bool(approval.get(flag), flag) is True:
            raise ValueError(f"approval_envelope must not be {flag}")
    requested_at, expires_at = _validate_approval_timestamps(approval.get("requested_at"), approval.get("expires_at"))
    _validate_exact_exclusions(approval.get("excluded_authorities"))
    return {
        "envelope_id": _required_string(approval.get("envelope_id"), "envelope_id"),
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "pilot_id": _required_string(approval.get("pilot_id"), "pilot_id"),
        "run_id": _required_string(approval.get("run_id"), "run_id"),
        "approval_id": _required_string(approval.get("approval_id"), "approval_id"),
        "requested_at": requested_at,
        "expires_at": expires_at,
    }


def _validate_approval_timestamps(requested_value: Any, expires_value: Any) -> tuple[str, str]:
    requested_text = _required_string(requested_value, "requested_at")
    expires_text = _required_string(expires_value, "expires_at")
    requested_at = _parse_timestamp(requested_text, "requested_at")
    expires_at = _parse_timestamp(expires_text, "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= datetime.now(timezone.utc):
        raise ValueError("expires_at must be in the future")
    return requested_text, expires_text


def _parse_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp with timezone") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be an ISO-8601 timestamp with timezone")
    return parsed.astimezone(timezone.utc)


def _validate_signer_policy(signer: dict[str, Any]) -> dict[str, Any]:
    return _validate_policy(signer, _SIGNER_KEYS, "signer_policy", ["key_material_accessed", "signature_generated", "secret_read"])


def _validate_storage_policy(storage: dict[str, Any]) -> dict[str, Any]:
    return _validate_policy(storage, _STORAGE_KEYS, "storage_policy", ["immutable_storage_written", "storage_write_attempted"])


def _validate_ledger_policy(ledger: dict[str, Any]) -> dict[str, Any]:
    return _validate_policy(ledger, _LEDGER_KEYS, "ledger_policy", ["public_ledger_mutated", "ledger_append_attempted"])


def _validate_rollback_policy(rollback: dict[str, Any]) -> dict[str, Any]:
    return _validate_policy(rollback, _ROLLBACK_KEYS, "rollback_policy", ["rollback_executed", "revocation_executed", "supersession_executed"])


def _validate_policy(value: dict[str, Any], allowed: set[str], label: str, false_flags: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dictionary")
    _scan_nested(value, label)
    _enforce_allowed_keys(value, allowed, label)
    missing = sorted(allowed - set(value))
    if missing:
        raise ValueError(f"{label} missing required field: {missing[0]}")
    result: dict[str, Any] = {}
    for key, item in value.items():
        if key.endswith("_hash"):
            result[key] = _required_hash(item, key)
        elif key in false_flags:
            result[key] = _required_false(item, key)
        else:
            result[key] = _required_string(item, key)
    return result


def _validate_audit_bundle(audit: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(audit, dict):
        raise ValueError("audit_bundle must be a dictionary")
    _scan_nested(
        {key: value for key, value in audit.items() if key not in {"rtm_generated", "drift_decision_made", "protected_body_read"}},
        "audit_bundle",
    )
    _enforce_allowed_keys(audit, _AUDIT_KEYS, "audit_bundle")
    if _required_hash(audit.get("request_hash"), "request_hash") != request["request_hash"]:
        raise ValueError("audit_bundle request_hash does not match request")
    if _required_hash(audit.get("beo_hash"), "beo_hash") != request["beo_hash"]:
        raise ValueError("audit_bundle beo_hash does not match request")
    if _required_hash(audit.get("source_evidence_hash"), "source_evidence_hash") != request["source_evidence_hash"]:
        raise ValueError("audit_bundle source_evidence_hash does not match request")
    return {
        "audit_bundle_id": _required_string(audit.get("audit_bundle_id"), "audit_bundle_id"),
        "audit_bundle_hash": _required_hash(audit.get("audit_bundle_hash"), "audit_bundle_hash"),
        "request_hash": request["request_hash"],
        "beo_hash": request["beo_hash"],
        "source_evidence_hash": request["source_evidence_hash"],
        "protected_body_read": _required_false(audit.get("protected_body_read"), "protected_body_read"),
        "rtm_generated": _required_false(audit.get("rtm_generated"), "rtm_generated"),
        "drift_decision_made": _required_false(audit.get("drift_decision_made"), "drift_decision_made"),
    }


def _validate_pilot_controls(controls: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(controls, dict):
        raise ValueError("pilot_controls must be a dictionary")
    _scan_nested(
        {
            key: value
            for key, value in controls.items()
            if key
            not in {
                "publication_performed",
                "signature_generated",
                "immutable_storage_written",
                "public_ledger_mutated",
                "rollback_executed",
                "rtm_generated",
                "protected_body_read",
            }
        },
        "pilot_controls",
    )
    _enforce_allowed_keys(controls, _CONTROLS_KEYS, "pilot_controls")
    max_output_bytes = controls.get("max_output_bytes")
    timeout_seconds = controls.get("timeout_seconds")
    if not isinstance(max_output_bytes, int) or max_output_bytes <= 0 or max_output_bytes > 1_000_000:
        raise ValueError("max_output_bytes must be a bounded positive integer")
    if not isinstance(timeout_seconds, int) or timeout_seconds <= 0 or timeout_seconds > 3600:
        raise ValueError("timeout_seconds must be a bounded positive integer")
    if _required_bool(controls.get("single_run_only"), "single_run_only") is not True:
        raise ValueError("single_run_only must be true")
    result = {
        "operator_stop_control": _required_string(controls.get("operator_stop_control"), "operator_stop_control"),
        "max_output_bytes": max_output_bytes,
        "timeout_seconds": timeout_seconds,
        "single_run_only": True,
        "replay_protection": _required_string(controls.get("replay_protection"), "replay_protection"),
    }
    for flag in [
        "publication_performed",
        "signature_generated",
        "immutable_storage_written",
        "public_ledger_mutated",
        "rollback_executed",
        "rtm_generated",
        "protected_body_read",
    ]:
        result[flag] = _required_false(controls.get(flag), flag)
    return result


def _validate_exact_exclusions(excluded: Any) -> None:
    if (
        not isinstance(excluded, list)
        or not all(isinstance(item, str) for item in excluded)
        or set(excluded) != EXACT_EXCLUDED_AUTHORITIES
        or len(excluded) != len(EXACT_EXCLUDED_AUTHORITIES)
    ):
        raise ValueError("excluded_authorities must match exact denied authority set")
