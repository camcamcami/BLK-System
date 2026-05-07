"""Fixture-only BEO publication candidate construction.

This module builds deterministic local candidate envelopes from already-supplied
DRAFT_ONLY BEO fixtures. It performs validation and shape binding only; it does
not publish outcomes, write ledgers, generate RTM data, read protected BLK-req
bodies, or invoke external services.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any

_ALLOWED_STATUSES = {"PASS", "FAIL"}
_DRAFT_ONLY = "DRAFT_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_CANDIDATE_STATUS = "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
_APPROVAL_SCOPE = "BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_PUBLICATION_AUTHORITY_FIELDS = {
    "published_at",
    "approved_by",
    "signature",
    "signer",
    "storage_uri",
    "storage_location",
    "ledger_id",
    "public_ledger_mutation",
    "rollback_plan",
    "rollback_authority",
    "publication_authority",
}
_RTM_AUTHORITY_FIELDS = {
    "rtm",
    "rtm_id",
    "requirements",
    "coverage_matrix",
    "coverage_status",
    "drift",
    "drift_decision",
}
_FORBIDDEN_SIGNER_KEYS = {
    "key_material",
    "key_material_value",
    "secret",
    "secret_value",
    "host_key",
    "token",
    "private" + "_key",
}


def build_beo_publication_candidate_fixture(
    draft_beo: dict[str, object],
    *,
    candidate_id: str,
    publication_approval: dict[str, object],
    signer_fixture: dict[str, object],
    storage_fixture: dict[str, object],
    ledger_fixture: dict[str, object],
    rollback_fixture: dict[str, object],
) -> dict[str, object]:
    """Build a deterministic publication-candidate fixture without side effects."""

    if not isinstance(draft_beo, dict):
        raise ValueError("draft_beo must be a dictionary")
    candidate_id = _required_string(candidate_id, "candidate_id")
    _validate_draft_beo(draft_beo)
    beo_hash = _canonical_fixture_hash(draft_beo)
    approval = _validate_publication_approval(
        publication_approval,
        expected_beo_id=_required_string(draft_beo.get("beo_id"), "beo_id"),
        expected_beo_hash=beo_hash,
    )
    signer = _validate_signer_fixture(signer_fixture)
    storage = _validate_storage_fixture(storage_fixture)
    ledger = _validate_ledger_fixture(ledger_fixture)
    rollback = _validate_rollback_fixture(rollback_fixture)

    return {
        "candidate_id": candidate_id,
        "candidate_status": _CANDIDATE_STATUS,
        "beo_id": _required_string(draft_beo.get("beo_id"), "beo_id"),
        "beo_hash": beo_hash,
        "beb_id": _required_string(draft_beo.get("beb_id"), "beb_id"),
        "status": str(draft_beo.get("status", "")),
        "source": _required_string(draft_beo.get("source"), "source"),
        "commit_hash": _required_string(draft_beo.get("commit_hash"), "commit_hash"),
        "pre_engine_hash": _required_hash(draft_beo.get("pre_engine_hash"), "pre_engine_hash"),
        "trace_artifacts": _trace_artifacts(draft_beo),
        "source_evidence": _source_evidence_identity(draft_beo),
        "publication_approval": approval,
        "signer_fixture": signer,
        "storage_fixture": storage,
        "ledger_fixture": ledger,
        "rollback_fixture": rollback,
        "beo_publication": _DRAFT_ONLY,
        "rtm_status": _NOT_GENERATED,
        "published": False,
        "active_vault_read": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
    }


def _validate_draft_beo(draft_beo: dict[str, object]) -> None:
    status = str(draft_beo.get("status", ""))
    if status not in _ALLOWED_STATUSES:
        raise ValueError("draft_beo status must be PASS/FAIL")
    if str(draft_beo.get("beo_publication", "")) != _DRAFT_ONLY:
        raise ValueError("beo_publication must remain DRAFT_ONLY")
    if str(draft_beo.get("rtm_status", "")) != _NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    if draft_beo.get("active_vault_read") is True:
        raise ValueError("active_vault_read must remain false")
    _required_string(draft_beo.get("beo_id"), "beo_id")
    _required_string(draft_beo.get("beb_id"), "beb_id")
    _required_string(draft_beo.get("source"), "source")
    _required_string(draft_beo.get("commit_hash"), "commit_hash")
    _required_hash(draft_beo.get("pre_engine_hash"), "pre_engine_hash")
    _trace_artifacts(draft_beo)
    forbidden = sorted((_PUBLICATION_AUTHORITY_FIELDS | _RTM_AUTHORITY_FIELDS).intersection(draft_beo))
    if forbidden:
        raise ValueError(f"draft_beo rejects authority field: {forbidden[0]}")


def _validate_publication_approval(
    approval: dict[str, object],
    *,
    expected_beo_id: str,
    expected_beo_hash: str,
) -> dict[str, object]:
    if not isinstance(approval, dict):
        raise ValueError("publication_approval must be a dictionary")
    normalized = {
        "approval_record_hash": _required_hash(approval.get("approval_record_hash"), "approval_record_hash"),
        "authorization_request_hash": _required_hash(
            approval.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "approval_scope": _required_string(approval.get("approval_scope"), "approval_scope"),
        "approval_timestamp": _required_string(approval.get("approval_timestamp"), "approval_timestamp"),
        "approved_beo_id": _required_string(approval.get("approved_beo_id"), "approved_beo_id"),
        "approved_beo_hash": _required_hash(approval.get("approved_beo_hash"), "approved_beo_hash"),
        "expired": _required_bool(approval.get("expired"), "expired"),
        "replayed": _required_bool(approval.get("replayed"), "replayed"),
        "stale": _required_bool(approval.get("stale"), "stale"),
    }
    if normalized["approval_scope"] != _APPROVAL_SCOPE:
        raise ValueError("approval_scope must be BEO_PUBLICATION_CANDIDATE_FIXTURE_ONLY")
    if normalized["approved_beo_id"] != expected_beo_id:
        raise ValueError("approved_beo_id does not match draft BEO")
    if normalized["approved_beo_hash"] != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match draft BEO")
    for flag in ("expired", "replayed", "stale"):
        if normalized[flag] is True:
            raise ValueError(f"publication approval must not be {flag}")
    return normalized


def _validate_signer_fixture(signer: dict[str, object]) -> dict[str, object]:
    if not isinstance(signer, dict):
        raise ValueError("signer_fixture must be a dictionary")
    forbidden_keys = sorted(_FORBIDDEN_SIGNER_KEYS.intersection(signer))
    if forbidden_keys:
        raise ValueError(f"signer_fixture rejects secret-bearing field: {forbidden_keys[0]}")
    normalized = {
        "signer_identity": _required_string(signer.get("signer_identity"), "signer_identity"),
        "signer_policy_hash": _required_hash(signer.get("signer_policy_hash"), "signer_policy_hash"),
        "key_material_accessed": _required_false(signer.get("key_material_accessed"), "key_material_accessed"),
        "signature_generated": _required_false(signer.get("signature_generated"), "signature_generated"),
        "k" + "ms_called": _required_false(signer.get("k" + "ms_called"), "k" + "ms_called"),
        "secret_read": _required_false(signer.get("secret_read"), "secret_read"),
    }
    return normalized


def _validate_storage_fixture(storage: dict[str, object]) -> dict[str, object]:
    if not isinstance(storage, dict):
        raise ValueError("storage_fixture must be a dictionary")
    return {
        "storage_target_identity": _required_string(
            storage.get("storage_target_identity"), "storage_target_identity"
        ),
        "storage_policy_hash": _required_hash(storage.get("storage_policy_hash"), "storage_policy_hash"),
        "immutable_storage_written": _required_false(
            storage.get("immutable_storage_written"), "immutable_storage_written"
        ),
        "storage_write_attempted": _required_false(
            storage.get("storage_write_attempted"), "storage_write_attempted"
        ),
    }


def _validate_ledger_fixture(ledger: dict[str, object]) -> dict[str, object]:
    if not isinstance(ledger, dict):
        raise ValueError("ledger_fixture must be a dictionary")
    return {
        "ledger_target_identity": _required_string(
            ledger.get("ledger_target_identity"), "ledger_target_identity"
        ),
        "ledger_policy_hash": _required_hash(ledger.get("ledger_policy_hash"), "ledger_policy_hash"),
        "public_ledger_mutated": _required_false(
            ledger.get("public_ledger_mutated"), "public_ledger_mutated"
        ),
        "ledger_append_attempted": _required_false(
            ledger.get("ledger_append_attempted"), "ledger_append_attempted"
        ),
    }


def _validate_rollback_fixture(rollback: dict[str, object]) -> dict[str, object]:
    if not isinstance(rollback, dict):
        raise ValueError("rollback_fixture must be a dictionary")
    return {
        "rollback_policy_hash": _required_hash(
            rollback.get("rollback_policy_hash"), "rollback_policy_hash"
        ),
        "rollback_fixture_identity": _required_string(
            rollback.get("rollback_fixture_identity"), "rollback_fixture_identity"
        ),
        "rollback_executed": _required_false(rollback.get("rollback_executed"), "rollback_executed"),
        "revocation_executed": _required_false(
            rollback.get("revocation_executed"), "revocation_executed"
        ),
        "supersession_executed": _required_false(
            rollback.get("supersession_executed"), "supersession_executed"
        ),
    }


def _source_evidence_identity(draft_beo: dict[str, object]) -> dict[str, object]:
    replay = draft_beo.get("live_smoke_replay")
    if not isinstance(replay, dict):
        return {}

    for flag in ("expired", "replayed", "stale"):
        if replay.get(flag) is True:
            raise ValueError(f"source evidence must not be {flag}")
    cleanup_status = _required_string(replay.get("cleanup_status"), "cleanup_status")
    if cleanup_status != "CLEANED":
        raise ValueError("cleanup_status must be CLEANED for source evidence")

    return {
        "run_id": _required_string(replay.get("run_id"), "run_id"),
        "tool_name": _required_string(replay.get("tool_name"), "tool_name"),
        "approval_record_hash": _required_hash(
            replay.get("approval_record_hash"), "approval_record_hash"
        ),
        "authorization_request_hash": _required_hash(
            replay.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "source_evidence_hash": _required_hash(
            replay.get("source_evidence_hash"), "source_evidence_hash"
        ),
        "transcript_hash": _required_hash(replay.get("transcript_hash"), "transcript_hash"),
        "cleanup_status": cleanup_status,
    }


def _trace_artifacts(source: dict[str, object]) -> list[dict[str, str]]:
    artifacts = source.get("trace_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("trace_artifacts must be a non-empty list")
    normalized: list[dict[str, str]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("trace_artifacts must contain objects")
        normalized.append(
            {
                "kind": _required_string(artifact.get("kind"), "trace_artifacts.kind"),
                "id": _required_string(artifact.get("id"), "trace_artifacts.id"),
                "version_hash": _required_hash(
                    artifact.get("version_hash"), "trace_artifacts.version_hash"
                ),
            }
        )
    return deepcopy(normalized)


def _canonical_fixture_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _required_string(value: object, field: str) -> str:
    text = str(value or "")
    if not text.strip():
        raise ValueError(f"{field} must be non-empty")
    return text


def _required_hash(value: object, field: str) -> str:
    text = _required_string(value, field)
    if not _HASH_RE.match(text):
        raise ValueError(f"{field} must match sha256:<64-lowercase-hex>")
    return text


def _required_bool(value: object, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _required_false(value: object, field: str) -> bool:
    if value is not False:
        raise ValueError(f"{field} must be false")
    return False
