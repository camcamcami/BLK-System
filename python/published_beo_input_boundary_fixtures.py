"""Fixture-only published-BEO input boundary construction.

This module builds deterministic local input envelopes from already-supplied
BEO publication candidate fixtures and already-supplied publication receipt
fixtures. It validates shape and side-effect flags only; it does not perform
BEO publication, create RTM artifacts, make trace judgments, read protected
BLK-req bodies, or invoke external services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_CANDIDATE_STATUS = "PUBLICATION_CANDIDATE_FIXTURE_ONLY"
_DRAFT_ONLY = "DRAFT_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_INPUT_STATUS = "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
_INPUT_PUBLICATION = "PUBLISHED_INPUT_FIXTURE_ONLY"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ALLOWED_BEO_STATUSES = {"PASS", "FAIL"}
_RECEIPT_SCOPE = "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
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
    "coverage" + "_claim",
    "drift",
    "drift" + "_status",
    "drift" + "_decision",
}
_FORBIDDEN_PUBLICATION_FIELDS = {
    "signature",
    "ledger_id",
    "publication_authority",
    "publication_performed",
}
_DESCRIPTOR_FALSE_FLAGS = {
    "signer_fixture": ["key_material_accessed", "signature_generated", "k" + "ms_called", "secret_read"],
    "storage_fixture": ["immutable_storage_written", "storage_write_attempted"],
    "ledger_fixture": ["public_ledger_mutated", "ledger_append_attempted"],
    "rollback_fixture": ["rollback_executed", "revocation_executed", "supersession_executed"],
}
_RECEIPT_FALSE_FLAGS = [
    "expired",
    "replayed",
    "stale",
    "signature_generated",
    "key_material_accessed",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
]
_CANDIDATE_SIDE_EFFECT_FLAGS = [
    "signature_generated",
    "key_material_accessed",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "publication_performed",
]
_SECRET_BEARING_FIELDS = {
    "key_material",
    "key_material_value",
    "private_key",
    "secret",
    "secret_value",
    "token",
    "host_key",
}


def build_published_beo_input_boundary_fixture(
    publication_candidate: dict[str, Any],
    *,
    publication_receipt: dict[str, Any],
    input_id: str,
) -> dict[str, Any]:
    """Build a deterministic published-BEO input fixture without side effects."""

    input_id = _required_string(input_id, "input_id")
    candidate = _validate_publication_candidate(publication_candidate)
    receipt = _validate_publication_receipt(
        publication_receipt,
        expected_candidate_id=candidate["candidate_id"],
        expected_beo_hash=candidate["beo_hash"],
    )

    return {
        "input_id": input_id,
        "input_status": _INPUT_STATUS,
        "candidate_id": candidate["candidate_id"],
        "source_candidate_status": _CANDIDATE_STATUS,
        "beo_id": candidate["beo_id"],
        "beo_hash": candidate["beo_hash"],
        "beb_id": candidate["beb_id"],
        "beo_status": candidate["status"],
        "commit_hash": candidate["commit_hash"],
        "pre_engine_hash": candidate["pre_engine_hash"],
        "trace_artifacts": deepcopy(candidate["trace_artifacts"]),
        "publication_receipt": receipt,
        "publication_receipt_scope": _RECEIPT_SCOPE,
        "published_input_fixture": True,
        "beo_publication": _INPUT_PUBLICATION,
        "rtm_status": _NOT_GENERATED,
        "rtm_authority": "DISABLED_NOT_GENERATED",
        "publication_performed": False,
        "signature_generated": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "active_vault_read": False,
        "protected_body_read": False,
        "rtm_created": False,
        "matrix_created": False,
        "drift_decision_made": False,
    }


def _validate_publication_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        raise ValueError("publication_candidate must be a dictionary")
    _reject_forbidden_fields(candidate, "publication_candidate")
    _reject_forbidden_fields_recursive(candidate, "publication_candidate")
    if "published_at" in candidate:
        raise ValueError("publication_candidate rejects forbidden field: published_at")
    for flag in _CANDIDATE_SIDE_EFFECT_FLAGS:
        if flag in candidate and candidate[flag] is not False:
            raise ValueError(f"publication_candidate.{flag} must be false")
    if _required_string(candidate.get("candidate_status"), "candidate_status") != _CANDIDATE_STATUS:
        raise ValueError("candidate_status must be PUBLICATION_CANDIDATE_FIXTURE_ONLY")
    if _required_string(candidate.get("beo_publication"), "beo_publication") != _DRAFT_ONLY:
        raise ValueError("beo_publication must remain DRAFT_ONLY on source candidate")
    if _required_string(candidate.get("rtm_status"), "rtm_status") != _NOT_GENERATED:
        raise ValueError("rtm_status must remain NOT_GENERATED")
    if candidate.get("published") is not False:
        raise ValueError("source candidate must not be published")
    if candidate.get("active_vault_read") is True:
        raise ValueError("active_vault_read must remain false")
    if candidate.get("protected_body_read") is True:
        raise ValueError("protected_body_read must remain false")
    for descriptor_name, flags in _DESCRIPTOR_FALSE_FLAGS.items():
        descriptor = candidate.get(descriptor_name)
        if descriptor is None:
            continue
        if not isinstance(descriptor, dict):
            raise ValueError(f"{descriptor_name} must be a dictionary")
        for flag in flags:
            if descriptor.get(flag) is not False:
                raise ValueError(f"{descriptor_name}.{flag} must be false")

    normalized = {
        "candidate_id": _required_string(candidate.get("candidate_id"), "candidate_id"),
        "beo_id": _required_string(candidate.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(candidate.get("beo_hash"), "beo_hash"),
        "beb_id": _required_string(candidate.get("beb_id"), "beb_id"),
        "status": _required_string(candidate.get("status"), "status"),
        "commit_hash": _required_string(candidate.get("commit_hash"), "commit_hash"),
        "pre_engine_hash": _required_hash(candidate.get("pre_engine_hash"), "pre_engine_hash"),
        "trace_artifacts": _trace_artifacts(candidate.get("trace_artifacts")),
    }
    if normalized["status"] not in _ALLOWED_BEO_STATUSES:
        raise ValueError("publication_candidate status must be PASS/FAIL")
    return normalized


def _validate_publication_receipt(
    receipt: dict[str, Any],
    *,
    expected_candidate_id: str,
    expected_beo_hash: str,
) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise ValueError("publication_receipt must be a dictionary")
    _reject_forbidden_fields(receipt, "publication_receipt")
    _reject_forbidden_fields_recursive(receipt, "publication_receipt")
    normalized = {
        "receipt_id": _required_string(receipt.get("receipt_id"), "receipt_id"),
        "publication_receipt_hash": _required_hash(
            receipt.get("publication_receipt_hash"), "publication_receipt_hash"
        ),
        "publication_event_hash": _required_hash(
            receipt.get("publication_event_hash"), "publication_event_hash"
        ),
        "published_input_identity": _required_string(
            receipt.get("published_input_identity"), "published_input_identity"
        ),
        "publication_receipt_scope": _required_string(
            receipt.get("publication_receipt_scope"), "publication_receipt_scope"
        ),
        "approved_candidate_id": _required_string(
            receipt.get("approved_candidate_id"), "approved_candidate_id"
        ),
        "approved_beo_hash": _required_hash(receipt.get("approved_beo_hash"), "approved_beo_hash"),
        "operator_identity": _required_string(receipt.get("operator_identity"), "operator_identity"),
        "signer_identity": _required_string(receipt.get("signer_identity"), "signer_identity"),
        "storage_receipt_hash": _required_hash(
            receipt.get("storage_receipt_hash"), "storage_receipt_hash"
        ),
        "ledger_receipt_hash": _required_hash(receipt.get("ledger_receipt_hash"), "ledger_receipt_hash"),
        "published_at": _required_string(receipt.get("published_at"), "published_at"),
    }
    if normalized["publication_receipt_scope"] != _RECEIPT_SCOPE:
        raise ValueError("publication_receipt_scope must be PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
    if normalized["approved_candidate_id"] != expected_candidate_id:
        raise ValueError("approved_candidate_id does not match candidate fixture")
    if normalized["approved_beo_hash"] != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match candidate fixture")
    for flag in _RECEIPT_FALSE_FLAGS:
        normalized[flag] = _required_false(receipt.get(flag), flag)
    return normalized


def _reject_forbidden_fields(value: dict[str, Any], label: str) -> None:
    forbidden = sorted(
        (_FORBIDDEN_BODY_FIELDS | _FORBIDDEN_RTM_FIELDS | _FORBIDDEN_PUBLICATION_FIELDS).intersection(value)
    )
    if forbidden:
        raise ValueError(f"{label} rejects forbidden field: {forbidden[0]}")


def _reject_forbidden_fields_recursive(value: Any, label: str) -> None:
    forbidden_keys = _FORBIDDEN_BODY_FIELDS | _FORBIDDEN_RTM_FIELDS | _FORBIDDEN_PUBLICATION_FIELDS | _SECRET_BEARING_FIELDS
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in forbidden_keys:
                raise ValueError(f"{label} rejects forbidden field: {key}")
            _reject_forbidden_fields_recursive(nested, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_fields_recursive(item, f"{label}[{index}]")


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
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    text = value.strip()
    if not text:
        raise ValueError(f"requires non-empty {field}")
    return text


def _required_hash(value: Any, field: str) -> str:
    text = _required_string(value, field)
    if not _HASH_RE.match(text):
        raise ValueError(f"{field} must match sha256:<64-lowercase-hex>")
    return text


def _required_false(value: Any, field: str) -> bool:
    if value is not False:
        raise ValueError(f"{field} must be false")
    return False
