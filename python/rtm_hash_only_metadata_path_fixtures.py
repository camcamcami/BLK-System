"""Fixture-only RTM hash metadata path construction.

This module builds deterministic local path fixtures from already-supplied BEO
publication candidate fixtures and already-supplied hash metadata records. It
validates shape and authority flags only; it does not create RTM artifacts, make
trace judgments, read protected BLK-req bodies, publish BEOs, or invoke external
services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_CANDIDATE_STATUS = "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
_DRAFT_ONLY = "DRAFT_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_PATH_STATUS = "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"
_METADATA_SOURCE = "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
_COMPARISON_STATE = "NOT_EVALUATED_FIXTURE_ONLY"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ALLOWED_BEO_STATUSES = {"PASS", "FAIL"}
_ALLOWED_METADATA_KEYS = {
    "kind",
    "id",
    "version_hash",
    "metadata_source",
    "body_included",
    "body_read",
}
_FORBIDDEN_BODY_FIELDS = {
    "body",
    "text",
    "content",
    "markdown",
    "requirement_body",
    "use_case_body",
    "body_excerpt",
    "body_hash_input",
}
_FORBIDDEN_RTM_FIELDS = {
    "rtm",
    "rtm_id",
    "requirements",
    "coverage" + "_matrix",
    "coverage" + "_status",
    "drift",
    "drift" + "_decision",
    "drift" + "_status",
}
_FORBIDDEN_PUBLICATION_FIELDS = {
    "published_at",
    "signature",
    "ledger_id",
    "publication_authority",
}
_APPROVAL_SCOPE = "RTM_HASH_METADATA_PATH_FIXTURE_ONLY"


def build_rtm_hash_only_metadata_path_fixture(
    publication_candidate: dict[str, Any],
    *,
    hash_metadata_records: list[dict[str, Any]],
    rtm_metadata_approval: dict[str, Any],
    path_id: str,
) -> dict[str, Any]:
    """Build a deterministic fixture for a future hash-metadata RTM path."""

    path_id = _required_string(path_id, "path_id")
    candidate = _validate_publication_candidate(publication_candidate)
    metadata = _validate_hash_metadata_records(hash_metadata_records)
    approval = _validate_rtm_metadata_approval(
        rtm_metadata_approval,
        expected_candidate_id=candidate["candidate_id"],
        expected_beo_hash=candidate["beo_hash"],
    )

    return {
        "path_id": path_id,
        "path_status": _PATH_STATUS,
        "candidate_id": candidate["candidate_id"],
        "beo_id": candidate["beo_id"],
        "beo_hash": candidate["beo_hash"],
        "beb_id": candidate["beb_id"],
        "beo_status": candidate["status"],
        "beo_publication": _DRAFT_ONLY,
        "published": False,
        "rtm_status": _NOT_GENERATED,
        "rtm_authority": _PATH_STATUS,
        "trace_artifacts": deepcopy(candidate["trace_artifacts"]),
        "hash_metadata_records": metadata,
        "hash_path_records": _hash_path_records(candidate["trace_artifacts"], metadata),
        "comparison_state": _COMPARISON_STATE,
        "rtm_metadata_approval": approval,
        "active_vault_read": False,
        "protected_body_read": False,
        "rtm_created": False,
        "matrix_created": False,
        "drift_decision_made": False,
    }


def _validate_publication_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise ValueError("publication_candidate must be a dictionary")
    forbidden = sorted((_FORBIDDEN_RTM_FIELDS | _FORBIDDEN_PUBLICATION_FIELDS).intersection(candidate))
    if forbidden:
        raise ValueError(f"publication_candidate rejects authority field: {forbidden[0]}")
    if _required_string(candidate.get("candidate_status"), "candidate_status") != _CANDIDATE_STATUS:
        raise ValueError("candidate_status must be PUBLICATION_CANDIDATE_FIXTURE_ONLY")
    if _required_string(candidate.get("beo_publication"), "beo_publication") != _DRAFT_ONLY:
        raise ValueError("beo_publication must remain DRAFT_ONLY")
    if _required_string(candidate.get("rtm_status"), "rtm_status") != _NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    if candidate.get("published") is not False:
        raise ValueError("publication_candidate must not be published")
    if candidate.get("active_vault_read") is True:
        raise ValueError("active_vault_read must remain false")
    if candidate.get("protected_body_read") is True:
        raise ValueError("protected_body_read must remain false")

    normalized = {
        "candidate_id": _required_string(candidate.get("candidate_id"), "candidate_id"),
        "beo_id": _required_string(candidate.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(candidate.get("beo_hash"), "beo_hash"),
        "beb_id": _required_string(candidate.get("beb_id"), "beb_id"),
        "status": _required_string(candidate.get("status"), "status"),
        "trace_artifacts": _trace_artifacts(candidate.get("trace_artifacts")),
    }
    if normalized["status"] not in _ALLOWED_BEO_STATUSES:
        raise ValueError("publication_candidate status must be PASS/FAIL")
    return normalized


def _validate_hash_metadata_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records:
        raise ValueError("hash_metadata_records must be a non-empty list")
    normalized: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("hash_metadata_records must contain objects")
        forbidden = sorted(_FORBIDDEN_BODY_FIELDS.intersection(record))
        if forbidden:
            raise ValueError(f"hash metadata rejects protected body field: {forbidden[0]}")
        extra = sorted(set(record) - _ALLOWED_METADATA_KEYS)
        if extra:
            raise ValueError(f"hash metadata rejects unsupported field: {extra[0]}")
        if _required_string(record.get("metadata_source"), "metadata_source") != _METADATA_SOURCE:
            raise ValueError("metadata_source must be ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY")
        normalized.append(
            {
                "kind": _required_string(record.get("kind"), "kind"),
                "id": _required_string(record.get("id"), "id"),
                "version_hash": _required_hash(record.get("version_hash"), "version_hash"),
                "metadata_source": _METADATA_SOURCE,
                "body_included": _required_false(record.get("body_included"), "body_included"),
                "body_read": _required_false(record.get("body_read"), "body_read"),
            }
        )
    return deepcopy(normalized)


def _validate_rtm_metadata_approval(
    approval: dict[str, Any],
    *,
    expected_candidate_id: str,
    expected_beo_hash: str,
) -> dict[str, Any]:
    if not isinstance(approval, dict):
        raise ValueError("rtm_metadata_approval must be a dictionary")
    normalized = {
        "approval_record_hash": _required_hash(approval.get("approval_record_hash"), "approval_record_hash"),
        "authorization_request_hash": _required_hash(
            approval.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "operator_identity": _required_string(approval.get("operator_identity"), "operator_identity"),
        "approval_scope": _required_string(approval.get("approval_scope"), "approval_scope"),
        "approval_timestamp": _required_string(approval.get("approval_timestamp"), "approval_timestamp"),
        "approved_candidate_id": _required_string(
            approval.get("approved_candidate_id"), "approved_candidate_id"
        ),
        "approved_beo_hash": _required_hash(approval.get("approved_beo_hash"), "approved_beo_hash"),
        "expired": _required_bool(approval.get("expired"), "expired"),
        "replayed": _required_bool(approval.get("replayed"), "replayed"),
        "stale": _required_bool(approval.get("stale"), "stale"),
    }
    if normalized["approval_scope"] != _APPROVAL_SCOPE:
        raise ValueError("approval_scope must be RTM_HASH_METADATA_PATH_FIXTURE_ONLY")
    if normalized["approved_candidate_id"] != expected_candidate_id:
        raise ValueError("approved_candidate_id does not match candidate fixture")
    if normalized["approved_beo_hash"] != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match candidate fixture")
    for flag in ("expired", "replayed", "stale"):
        if normalized[flag] is True:
            raise ValueError(f"rtm metadata approval must not be {flag}")
    return normalized


def _hash_path_records(
    trace_artifacts: list[dict[str, str]],
    metadata_records: list[dict[str, Any]],
) -> list[dict[str, str]]:
    metadata_by_identity = {
        (record["kind"], record["id"]): record for record in metadata_records
    }
    path_records: list[dict[str, str]] = []
    for artifact in trace_artifacts:
        metadata = metadata_by_identity.get((artifact["kind"], artifact["id"]))
        path_records.append(
            {
                "kind": artifact["kind"],
                "id": artifact["id"],
                "trace_version_hash": artifact["version_hash"],
                "metadata_version_hash": metadata["version_hash"] if metadata else "",
                "comparison_state": _COMPARISON_STATE,
            }
        )
    return path_records


def _trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    normalized: list[dict[str, str]] = []
    for artifact in value:
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


def _required_string(value: Any, field: str) -> str:
    text = str(value or "")
    if not text.strip():
        raise ValueError(f"requires non-empty {field}")
    return text


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
