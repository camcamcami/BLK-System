"""Fixture-only active-vault hash metadata backend records.

The helpers here normalize already-supplied backend manifest records into a
local, deterministic fixture shape. They do not inspect protected artifacts,
perform runtime trace comparison, create RTM artifacts, publish BEOs, mutate
source, or contact external services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_BACKEND_STATUS = "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
_DOWNSTREAM_SOURCE = "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ALLOWED_RECORD_KEYS = {
    "kind",
    "id",
    "version_hash",
    "manifest_record_id",
    "backend_manifest_hash",
    "metadata_source",
    "downstream_metadata_source",
    "body_included",
    "body_read",
    "body_copied",
    "body_hashed",
    "active_vault_read",
    "active_vault_scanned",
    "protected_path_accessed",
}
_ALLOWED_APPROVAL_KEYS = {
    "approval_record_hash",
    "authorization_request_hash",
    "operator_identity",
    "approval_scope",
    "approval_timestamp",
    "approved_manifest_hash",
    "expired",
    "replayed",
    "stale",
}
_FORBIDDEN_RECORD_KEYS = {
    "active_vault_path",
    "protected_path",
    "requirements_path",
    "use_cases_path",
    "source_path",
    "file_path",
    "path",
    "body",
    "text",
    "content",
    "markdown",
    "requirement_body",
    "use_case_body",
    "body_excerpt",
    "body_hash_input",
    "raw_artifact",
    "artifact_text",
    "promote",
    "promotion_performed",
    "baseline_authorization",
    "revision_applied",
    "parent_hash_checked",
    "active_vault_written",
    "rtm",
    "rtm_id",
    "coverage" + "_matrix",
    "coverage" + "_status",
    "drift",
    "drift" + "_status",
    "drift" + "_decision",
    "published_at",
    "signature",
    "ledger_id",
    "publication_authority",
    "beo_publication",
    "rtm_created",
    "matrix_created",
    "drift_decision_made",
    "publication_performed",
    "source_mutated",
}
_FALSE_RECORD_FLAGS = {
    "body_included",
    "body_read",
    "body_copied",
    "body_hashed",
    "active_vault_read",
    "active_vault_scanned",
    "protected_path_accessed",
}


def build_active_vault_hash_metadata_backend_fixture(
    manifest_records: list[dict[str, Any]],
    *,
    backend_approval: dict[str, Any],
    manifest_id: str,
) -> dict[str, Any]:
    """Build fixture-only backend hash metadata records from supplied metadata."""

    manifest_id = _required_string(manifest_id, "manifest_id")
    records = _validate_manifest_records(manifest_records)
    manifest_hash = records[0]["backend_manifest_hash"]
    approval = _validate_backend_approval(backend_approval, expected_manifest_hash=manifest_hash)

    return {
        "manifest_id": manifest_id,
        "backend_status": _BACKEND_STATUS,
        "backend_manifest_hash": manifest_hash,
        "backend_approval": approval,
        "manifest_records": deepcopy(records),
        "downstream_hash_metadata_records": _downstream_records(records),
        "rtm_status": _NOT_GENERATED,
        "active_vault_scanned": False,
        "active_vault_read": False,
        "protected_body_read": False,
        "body_copied": False,
        "body_hashed": False,
        "rtm_created": False,
        "matrix_created": False,
        "drift_decision_made": False,
        "publication_performed": False,
        "source_mutated": False,
    }


def _validate_manifest_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records:
        raise ValueError("manifest_records must be a non-empty list")

    normalized: list[dict[str, Any]] = []
    manifest_hash = ""
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("manifest_records must contain objects")
        forbidden = sorted(_FORBIDDEN_RECORD_KEYS.intersection(record))
        if forbidden:
            raise ValueError(f"backend manifest rejects forbidden field: {forbidden[0]}")
        extra = sorted(set(record) - _ALLOWED_RECORD_KEYS)
        if extra:
            raise ValueError(f"backend manifest rejects unsupported field: {extra[0]}")
        if _required_string(record.get("metadata_source"), "metadata_source") != _BACKEND_STATUS:
            raise ValueError("metadata_source must be ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
        if _required_string(record.get("downstream_metadata_source"), "downstream_metadata_source") != _DOWNSTREAM_SOURCE:
            raise ValueError("downstream_metadata_source must be ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY")
        for flag in sorted(_FALSE_RECORD_FLAGS):
            _required_false(record.get(flag), flag)
        current_manifest_hash = _required_hash(record.get("backend_manifest_hash"), "backend_manifest_hash")
        if manifest_hash and current_manifest_hash != manifest_hash:
            raise ValueError("all backend_manifest_hash values must match")
        manifest_hash = current_manifest_hash
        normalized.append(
            {
                "kind": _required_string(record.get("kind"), "kind"),
                "id": _required_string(record.get("id"), "id"),
                "version_hash": _required_hash(record.get("version_hash"), "version_hash"),
                "manifest_record_id": _required_string(record.get("manifest_record_id"), "manifest_record_id"),
                "backend_manifest_hash": current_manifest_hash,
                "metadata_source": _BACKEND_STATUS,
                "downstream_metadata_source": _DOWNSTREAM_SOURCE,
                "body_included": False,
                "body_read": False,
                "body_copied": False,
                "body_hashed": False,
                "active_vault_read": False,
                "active_vault_scanned": False,
                "protected_path_accessed": False,
            }
        )
    return normalized


def _validate_backend_approval(approval: dict[str, Any], *, expected_manifest_hash: str) -> dict[str, Any]:
    if not isinstance(approval, dict):
        raise ValueError("backend_approval must be a dictionary")
    extra = sorted(set(approval) - _ALLOWED_APPROVAL_KEYS)
    if extra:
        raise ValueError(f"backend approval rejects unsupported field: {extra[0]}")
    normalized = {
        "approval_record_hash": _required_hash(approval.get("approval_record_hash"), "approval_record_hash"),
        "authorization_request_hash": _required_hash(
            approval.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "approval_scope": _required_string(approval.get("approval_scope"), "approval_scope"),
        "approval_timestamp": _required_string(approval.get("approval_timestamp"), "approval_timestamp"),
        "approved_manifest_hash": _required_hash(approval.get("approved_manifest_hash"), "approved_manifest_hash"),
        "expired": _required_bool(approval.get("expired"), "expired"),
        "replayed": _required_bool(approval.get("replayed"), "replayed"),
        "stale": _required_bool(approval.get("stale"), "stale"),
    }
    if normalized["approval_scope"] != _BACKEND_STATUS:
        raise ValueError("approval_scope must be ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
    if normalized["approved_manifest_hash"] != expected_manifest_hash:
        raise ValueError("approved_manifest_hash does not match backend manifest")
    for flag in ("expired", "replayed", "stale"):
        if normalized[flag] is True:
            raise ValueError(f"backend approval must not be {flag}")
    return normalized


def _downstream_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "kind": record["kind"],
            "id": record["id"],
            "version_hash": record["version_hash"],
            "metadata_source": _DOWNSTREAM_SOURCE,
            "body_included": False,
            "body_read": False,
        }
        for record in records
    ]


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"requires non-empty string {field}")
    return value


def _required_hash(value: Any, field: str) -> str:
    text = _required_string(value, field)
    if not _HASH_RE.match(text):
        raise ValueError(f"{field} must match sha256:<64-lowercase-hex>")
    return text


def _required_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _required_false(value: Any, field: str) -> bool:
    if value is not False:
        raise ValueError(f"{field} must be false")
    return False
