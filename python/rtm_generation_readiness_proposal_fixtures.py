"""Proposal-only RTM generation readiness fixture construction.

The helpers here normalize already-supplied published-BEO input fixtures and
already-supplied active-vault hash metadata backend fixtures into a deterministic
local proposal shape. They do not inspect protected artifacts, create RTM
artifacts, create coverage matrices, make drift decisions, publish BEOs, mutate
source, or contact external services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_PROPOSAL_STATUS = "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY"
_INPUT_STATUS = "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
_INPUT_PUBLICATION = "PUBLISHED_INPUT_FIXTURE_ONLY"
_BACKEND_STATUS = "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
_METADATA_SOURCE = "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_RTM_AUTHORITY = "PROPOSAL_ONLY_NOT_AUTHORIZED"
_READY_STATE = "READY_FOR_LATER_RTM_APPROVAL"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ALLOWED_BEO_STATUSES = {"PASS", "FAIL"}

_FORBIDDEN_KEYS = {
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
    "rtm_id",
    "rtm_ledger",
    "rtm_output",
    "generated_at",
    "generation_commit",
    "coverage" + "_matrix",
    "coverage" + "_status",
    "coverage" + "_claim",
    "drift",
    "drift" + "_status",
    "drift" + "_decision",
    "drift" + "_rejection",
    "drift" + "_rejected",
    "signature",
    "ledger_id",
    "publication_authority",
    "published_at",
    "beo_publication_authority",
    "key_material",
    "key_material_value",
    "private_key",
    "secret",
    "secret_value",
    "token",
    "host_key",
}
_FALSE_INPUT_FLAGS = [
    "publication_performed",
    "signature_generated",
    "key_material_accessed",
    "immutable_storage_written",
    "public_ledger_mutated",
    "rollback_executed",
    "active_vault_read",
    "protected_body_read",
    "rtm_created",
    "matrix_created",
    "drift_decision_made",
]
_FALSE_BACKEND_FLAGS = [
    "active_vault_scanned",
    "active_vault_read",
    "protected_body_read",
    "body_copied",
    "body_hashed",
    "rtm_created",
    "matrix_created",
    "drift_decision_made",
    "publication_performed",
    "source_mutated",
]


def build_rtm_generation_readiness_proposal_fixture(
    published_beo_input: dict[str, Any],
    *,
    active_vault_backend_fixture: dict[str, Any],
    proposal_request: dict[str, Any],
    proposal_id: str,
) -> dict[str, Any]:
    """Build a proposal-only RTM readiness fixture without runtime authority."""

    proposal_id = _required_string(proposal_id, "proposal_id")
    published = _validate_published_beo_input(published_beo_input)
    backend = _validate_active_vault_backend_fixture(active_vault_backend_fixture)
    request = _validate_proposal_request(
        proposal_request,
        expected_input_id=published["input_id"],
        expected_beo_hash=published["beo_hash"],
        expected_backend_manifest_hash=backend["backend_manifest_hash"],
    )
    readiness_records = _readiness_records(published["trace_artifacts"], backend["metadata_records"])

    return {
        "proposal_id": proposal_id,
        "proposal_status": _PROPOSAL_STATUS,
        "input_id": published["input_id"],
        "source_input_status": _INPUT_STATUS,
        "beo_id": published["beo_id"],
        "beo_hash": published["beo_hash"],
        "beb_id": published["beb_id"],
        "beo_status": published["beo_status"],
        "publication_receipt_hash": published["publication_receipt_hash"],
        "backend_manifest_hash": backend["backend_manifest_hash"],
        "backend_approval_hash": backend["backend_approval_hash"],
        "trace_artifacts": deepcopy(published["trace_artifacts"]),
        "metadata_record_identities": _metadata_record_identities(backend["metadata_records"]),
        "readiness_records": readiness_records,
        "proposal_request": request,
        "generation_approval_required": True,
        "rtm_generation_authorized": False,
        "rtm_status": _NOT_GENERATED,
        "rtm_authority": _RTM_AUTHORITY,
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


def _validate_published_beo_input(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("published_beo_input must be a dictionary")
    _reject_forbidden_fields_recursive(value, "published_beo_input")
    if _required_string(value.get("input_status"), "input_status") != _INPUT_STATUS:
        raise ValueError("input_status must be PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
    if _required_string(value.get("publication_receipt_scope"), "publication_receipt_scope") != _INPUT_STATUS:
        raise ValueError("publication_receipt_scope must be PUBLISHED_BEO_INPUT_FIXTURE_ONLY")
    if _required_string(value.get("beo_publication"), "beo_publication") != _INPUT_PUBLICATION:
        raise ValueError("beo_publication must be PUBLISHED_INPUT_FIXTURE_ONLY")
    if _required_string(value.get("rtm_status"), "rtm_status") != _NOT_GENERATED:
        raise ValueError("published input rtm_status must be NOT_GENERATED")
    for flag in _FALSE_INPUT_FLAGS:
        _required_false(value.get(flag), flag)

    receipt = value.get("publication_receipt")
    if not isinstance(receipt, dict):
        raise ValueError("publication_receipt must be a dictionary")

    normalized = {
        "input_id": _required_string(value.get("input_id"), "input_id"),
        "beo_id": _required_string(value.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(value.get("beo_hash"), "beo_hash"),
        "beb_id": _required_string(value.get("beb_id"), "beb_id"),
        "beo_status": _required_string(value.get("beo_status"), "beo_status"),
        "publication_receipt_hash": _required_hash(
            receipt.get("publication_receipt_hash"), "publication_receipt_hash"
        ),
        "trace_artifacts": _trace_artifacts(value.get("trace_artifacts")),
    }
    if normalized["beo_status"] not in _ALLOWED_BEO_STATUSES:
        raise ValueError("beo_status must be PASS/FAIL")
    return normalized


def _validate_active_vault_backend_fixture(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("active_vault_backend_fixture must be a dictionary")
    _reject_forbidden_fields_recursive(value, "active_vault_backend_fixture")
    if _required_string(value.get("backend_status"), "backend_status") != _BACKEND_STATUS:
        raise ValueError("backend_status must be ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
    if _required_string(value.get("rtm_status"), "rtm_status") != _NOT_GENERATED:
        raise ValueError("backend rtm_status must be NOT_GENERATED")
    for flag in _FALSE_BACKEND_FLAGS:
        _required_false(value.get(flag), flag)

    approval = value.get("backend_approval")
    if not isinstance(approval, dict):
        raise ValueError("backend_approval must be a dictionary")
    manifest_hash = _required_hash(value.get("backend_manifest_hash"), "backend_manifest_hash")
    return {
        "manifest_id": _required_string(value.get("manifest_id"), "manifest_id"),
        "backend_manifest_hash": manifest_hash,
        "backend_approval_hash": _required_hash(
            approval.get("approval_record_hash"), "approval_record_hash"
        ),
        "metadata_records": _metadata_records(value.get("downstream_hash_metadata_records")),
    }


def _validate_proposal_request(
    value: dict[str, Any],
    *,
    expected_input_id: str,
    expected_beo_hash: str,
    expected_backend_manifest_hash: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("proposal_request must be a dictionary")
    _reject_forbidden_fields_recursive(value, "proposal_request")
    normalized = {
        "proposal_request_hash": _required_hash(value.get("proposal_request_hash"), "proposal_request_hash"),
        "authorization_request_hash": _required_hash(
            value.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "operator_identity": _required_string(value.get("operator_identity"), "operator_identity"),
        "request_scope": _required_string(value.get("request_scope"), "request_scope"),
        "request_timestamp": _required_string(value.get("request_timestamp"), "request_timestamp"),
        "approved_input_id": _required_string(value.get("approved_input_id"), "approved_input_id"),
        "approved_beo_hash": _required_hash(value.get("approved_beo_hash"), "approved_beo_hash"),
        "approved_backend_manifest_hash": _required_hash(
            value.get("approved_backend_manifest_hash"), "approved_backend_manifest_hash"
        ),
        "generation_approval_required": _required_true(
            value.get("generation_approval_required"), "generation_approval_required"
        ),
        "rtm_generation_authorized": _required_false(
            value.get("rtm_generation_authorized"), "rtm_generation_authorized"
        ),
        "expired": _required_false(value.get("expired"), "expired"),
        "replayed": _required_false(value.get("replayed"), "replayed"),
        "stale": _required_false(value.get("stale"), "stale"),
    }
    if normalized["request_scope"] != _PROPOSAL_STATUS:
        raise ValueError("request_scope must be RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY")
    if normalized["approved_input_id"] != expected_input_id:
        raise ValueError("approved_input_id does not match published-BEO input")
    if normalized["approved_beo_hash"] != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match published-BEO input")
    if normalized["approved_backend_manifest_hash"] != expected_backend_manifest_hash:
        raise ValueError("approved_backend_manifest_hash does not match backend fixture")
    return normalized


def _metadata_records(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("downstream_hash_metadata_records must be a non-empty list")
    normalized: list[dict[str, str]] = []
    for record in value:
        if not isinstance(record, dict):
            raise ValueError("downstream_hash_metadata_records must contain objects")
        _reject_forbidden_fields_recursive(record, "downstream_hash_metadata_records")
        if _required_string(record.get("metadata_source"), "metadata_source") != _METADATA_SOURCE:
            raise ValueError("metadata_source must be ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY")
        _required_false(record.get("body_included"), "body_included")
        _required_false(record.get("body_read"), "body_read")
        normalized.append(
            {
                "kind": _required_string(record.get("kind"), "kind"),
                "id": _required_string(record.get("id"), "id"),
                "version_hash": _required_hash(record.get("version_hash"), "version_hash"),
                "metadata_source": _METADATA_SOURCE,
            }
        )
    return normalized


def _trace_artifacts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("trace_artifacts must be a non-empty list")
    normalized: list[dict[str, str]] = []
    for artifact in value:
        if not isinstance(artifact, dict):
            raise ValueError("trace_artifacts must contain objects")
        _reject_forbidden_fields_recursive(artifact, "trace_artifacts")
        normalized.append(
            {
                "kind": _required_string(artifact.get("kind"), "trace_artifacts.kind"),
                "id": _required_string(artifact.get("id"), "trace_artifacts.id"),
                "version_hash": _required_hash(
                    artifact.get("version_hash"), "trace_artifacts.version_hash"
                ),
            }
        )
    return normalized


def _readiness_records(
    trace_artifacts: list[dict[str, str]], metadata_records: list[dict[str, str]]
) -> list[dict[str, str]]:
    metadata_by_identity = {(record["kind"], record["id"]): record for record in metadata_records}
    readiness: list[dict[str, str]] = []
    for artifact in trace_artifacts:
        metadata = metadata_by_identity.get((artifact["kind"], artifact["id"]))
        if metadata is None:
            raise ValueError("missing hash metadata for trace artifact")
        if metadata["version_hash"] != artifact["version_hash"]:
            raise ValueError("metadata version_hash mismatch for trace artifact")
        readiness.append(
            {
                "kind": artifact["kind"],
                "id": artifact["id"],
                "trace_version_hash": artifact["version_hash"],
                "metadata_version_hash": metadata["version_hash"],
                "readiness_state": _READY_STATE,
            }
        )
    return readiness


def _metadata_record_identities(records: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {"kind": record["kind"], "id": record["id"], "version_hash": record["version_hash"]}
        for record in records
    ]


def _reject_forbidden_fields_recursive(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in _FORBIDDEN_KEYS:
                raise ValueError(f"{label} rejects forbidden field: {key}")
            _reject_forbidden_fields_recursive(nested, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_fields_recursive(item, f"{label}[{index}]")


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


def _required_true(value: Any, field: str) -> bool:
    if value is not True:
        raise ValueError(f"{field} must be true")
    return True
