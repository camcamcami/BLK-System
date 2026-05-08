"""Deterministic offline RTM ledger fixtures for BLK-System.

The helper in this module consumes already-supplied published-BEO input and
active-vault hash metadata backend fixture dictionaries plus a separate RTM
specific approval fixture. It creates a local offline RTM ledger object without
reading protected bodies, scanning vault paths, publishing BEOs, touching signer
or storage systems, mutating public ledgers, rejecting drift, or inheriting prior
approvals.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any

_INPUT_STATUS = "PUBLISHED_BEO_INPUT_FIXTURE_ONLY"
_INPUT_PUBLICATION = "PUBLISHED_INPUT_FIXTURE_ONLY"
_BACKEND_STATUS = "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY"
_METADATA_SOURCE = "ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY"
_APPROVAL_SCOPE = "OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY"
_RTM_STATUS = "OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY"
_RTM_AUTHORITY = "OFFLINE_RTM_GENERATION_APPROVED_NARROW"
_COVERAGE_STATUS = "OFFLINE_RTM_COVERAGE_MATRIX_FIXTURE_ONLY"
_NOT_GENERATED = "NOT_GENERATED"
_MATCHED = "TRACE_HASH_MATCHED"
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+-][0-9]{2}:[0-9]{2})$")
_IDENTITY_RE = {
    "rtm_id": re.compile(r"^RTM-[0-9]{3}-[0-9]{3}$"),
    "approved_output_id": re.compile(r"^RTM-[0-9]{3}-[0-9]{3}$"),
    "input_id": re.compile(r"^PBI-[0-9]{3}-[0-9]{3}$"),
    "approved_input_id": re.compile(r"^PBI-[0-9]{3}-[0-9]{3}$"),
    "beo_id": re.compile(r"^BEO-[0-9]{3}-[0-9]{3}$"),
    "beb_id": re.compile(r"^BEB-[0-9]{3}-[0-9]{3}$"),
    "manifest_id": re.compile(r"^AVHM-[0-9]{3}-[0-9]{3}$"),
    "approval_id": re.compile(r"^RTM-GEN-APPROVAL-[0-9]{3}-[0-9]{3}$"),
    "operator_identity": re.compile(r"^[a-z0-9_]{3,32}$"),
}
_TRACE_KIND_RE = re.compile(r"^(REQ|UC)$")
_TRACE_ID_RE = re.compile(r"^(REQ|UC)-[0-9]{3}$")
_ALLOWED_BEO_STATUSES = {"PASS", "FAIL"}

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
_PUBLISHED_INPUT_ALLOWED_KEYS = {
    "input_id",
    "input_status",
    "beo_id",
    "beo_hash",
    "beb_id",
    "beo_status",
    "trace_artifacts",
    "publication_receipt",
    "publication_receipt_scope",
    "beo_publication",
    "rtm_status",
    *_FALSE_INPUT_FLAGS,
}
_PUBLICATION_RECEIPT_ALLOWED_KEYS = {"publication_receipt_hash"}
_BACKEND_ALLOWED_KEYS = {
    "manifest_id",
    "backend_status",
    "backend_manifest_hash",
    "backend_approval",
    "downstream_hash_metadata_records",
    "rtm_status",
    *_FALSE_BACKEND_FLAGS,
}
_BACKEND_APPROVAL_ALLOWED_KEYS = {"approval_record_hash"}
_METADATA_RECORD_ALLOWED_KEYS = {
    "kind",
    "id",
    "version_hash",
    "metadata_source",
    "body_included",
    "body_read",
}
_TRACE_ARTIFACT_ALLOWED_KEYS = {"kind", "id", "version_hash"}
_APPROVAL_ALLOWED_KEYS = {
    "approval_id",
    "approval_record_hash",
    "authorization_request_hash",
    "operator_identity",
    "approval_scope",
    "approval_timestamp",
    "approved_input_id",
    "approved_beo_hash",
    "approved_backend_manifest_hash",
    "approved_output_id",
    "generation_authorized",
    "drift_rejection_authorized",
    "expired",
    "replayed",
    "stale",
}
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
    "signature",
    "key_material",
    "key_material_value",
    "private_key",
    "secret",
    "secret_value",
    "token",
    "host_key",
    "publication_authority",
    "beo_publication_authority",
    "published_at",
    "ledger_id",
    "storage_receipt",
    "rollback_authority",
    "revocation_authority",
    "supersession_authority",
    "drift",
    "drift_status",
    "drift_decision",
    "drift_rejection",
    "drift_rejected",
    "reject_drift",
}
_FORBIDDEN_IDENTITY_FRAGMENTS = {
    "/",
    "\\",
    "\n",
    "\r",
    "\t",
    "..",
    "docs/active",
    "docs\\active",
    "docs/requirements",
    "docs\\requirements",
    "docs/use_cases",
    "docs\\use_cases",
    "active-vault",
    "active_vault",
    "protected_body",
    "protected-vault",
    "protected_vault",
    "requirement_body",
    "use_case_body",
}
_FORBIDDEN_IDENTITY_AUTHORITY_MARKERS = {
    "BEO_PUBLICATION_APPROVAL",
    "BLK_TEST_PASS",
    "BLK_PIPE_EXECUTION_APPROVAL",
    "CODEX_LIVE_APPROVAL",
    "RTM_GENERATION_READINESS_PROPOSAL_FIXTURE_ONLY",
    "PUBLISHED_BEO_INPUT_FIXTURE_ONLY",
    "ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY",
    "PUBLISHED_INPUT_FIXTURE_ONLY",
    "DRIFT_REJECTION_AUTHORIZED",
    "REJECT_DRIFT",
}
_FORBIDDEN_NORMALIZED_IDENTITY_MARKERS = {
    "BODY",
    "BODY_EXCERPT",
    "PROTECTED_BODY",
    "REQUIREMENT_BODY",
    "USE_CASE_BODY",
    "SHALL_NOT_READ_BODY",
    "DOCS_ACTIVE",
    "DOCSACTIVE",
    "DOCS_2FACTIVE",
    "DOCS2FACTIVE",
    "REQ_001_MD",
    "REQ001MD",
}


def build_offline_rtm_ledger_fixture(
    published_beo_input: dict[str, Any],
    *,
    active_vault_backend_fixture: dict[str, Any],
    generation_approval: dict[str, Any],
    rtm_id: str,
) -> dict[str, Any]:
    """Build a deterministic offline RTM ledger fixture from supplied metadata."""

    rtm_id = _required_identity_string(rtm_id, "rtm_id")
    published = _validate_published_beo_input(published_beo_input)
    backend = _validate_active_vault_backend_fixture(active_vault_backend_fixture)
    coverage_records = _coverage_records(published["trace_artifacts"], backend["metadata_records"])
    metadata_identities = _metadata_record_identities(backend["metadata_records"])
    approval = _validate_generation_approval(
        generation_approval,
        expected_input_id=published["input_id"],
        expected_beo_hash=published["beo_hash"],
        expected_publication_receipt_hash=published["publication_receipt_hash"],
        expected_backend_manifest_hash=backend["backend_manifest_hash"],
        expected_backend_approval_hash=backend["backend_approval_hash"],
        expected_output_id=rtm_id,
        trace_artifacts=published["trace_artifacts"],
        metadata_record_identities=metadata_identities,
    )
    ledger_without_hash = {
        "rtm_id": rtm_id,
        "rtm_status": _RTM_STATUS,
        "rtm_authority": _RTM_AUTHORITY,
        "coverage_matrix_status": _COVERAGE_STATUS,
        "input_id": published["input_id"],
        "beo_id": published["beo_id"],
        "beo_hash": published["beo_hash"],
        "beb_id": published["beb_id"],
        "beo_status": published["beo_status"],
        "publication_receipt_hash": published["publication_receipt_hash"],
        "manifest_id": backend["manifest_id"],
        "backend_manifest_hash": backend["backend_manifest_hash"],
        "backend_approval_hash": backend["backend_approval_hash"],
        "trace_artifacts": deepcopy(published["trace_artifacts"]),
        "metadata_record_identities": metadata_identities,
        "coverage_records": coverage_records,
        "approval_id": approval["approval_id"],
        "approval_record_hash": approval["approval_record_hash"],
        "authorization_request_hash": approval["authorization_request_hash"],
        "operator_identity": approval["operator_identity"],
        "approval_scope": _APPROVAL_SCOPE,
        "approval_timestamp": approval["approval_timestamp"],
        "generation_authorized": True,
        "drift_rejection_authorized": False,
        "protected_body_boundary": "PROTECTED_BODY_NOT_READ",
        "active_vault_boundary": "ACTIVE_VAULT_NOT_SCANNED",
        "beo_publication_boundary": "BEO_PUBLICATION_NOT_PERFORMED",
        "side_effect_boundary": "NO_SIGNER_STORAGE_OR_PUBLIC_LEDGER_SIDE_EFFECTS",
        "drift_review_state": "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
        "protected_body_read": False,
        "active_vault_scanned": False,
        "active_vault_read": False,
        "body_copied": False,
        "body_hashed": False,
        "beo_publication_performed": False,
        "signature_generated": False,
        "key_material_accessed": False,
        "immutable_storage_written": False,
        "public_ledger_mutated": False,
        "rollback_executed": False,
        "source_mutated": False,
        "drift_decision_made": False,
        "drift_rejection_made": False,
    }
    return {**ledger_without_hash, "rtm_ledger_hash": _canonical_hash(ledger_without_hash)}


def _validate_published_beo_input(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("published_beo_input must be a dictionary")
    _reject_forbidden_fields_shallow(value, "published_beo_input")
    _reject_unsupported_fields(value, _PUBLISHED_INPUT_ALLOWED_KEYS, "published_beo_input")
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
    _reject_unsupported_fields(receipt, _PUBLICATION_RECEIPT_ALLOWED_KEYS, "publication_receipt")
    _reject_forbidden_fields_recursive(receipt, "publication_receipt")
    normalized = {
        "input_id": _required_identity_string(value.get("input_id"), "input_id"),
        "beo_id": _required_identity_string(value.get("beo_id"), "beo_id"),
        "beo_hash": _required_hash(value.get("beo_hash"), "beo_hash"),
        "beb_id": _required_identity_string(value.get("beb_id"), "beb_id"),
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
    _reject_forbidden_fields_shallow(value, "active_vault_backend_fixture")
    _reject_unsupported_fields(value, _BACKEND_ALLOWED_KEYS, "active_vault_backend_fixture")
    if _required_string(value.get("backend_status"), "backend_status") != _BACKEND_STATUS:
        raise ValueError("backend_status must be ACTIVE_VAULT_HASH_METADATA_BACKEND_FIXTURE_ONLY")
    if _required_string(value.get("rtm_status"), "rtm_status") != _NOT_GENERATED:
        raise ValueError("backend rtm_status must be NOT_GENERATED")
    for flag in _FALSE_BACKEND_FLAGS:
        _required_false(value.get(flag), flag)
    approval = value.get("backend_approval")
    if not isinstance(approval, dict):
        raise ValueError("backend_approval must be a dictionary")
    _reject_unsupported_fields(approval, _BACKEND_APPROVAL_ALLOWED_KEYS, "backend_approval")
    _reject_forbidden_fields_recursive(approval, "backend_approval")
    return {
        "manifest_id": _required_identity_string(value.get("manifest_id"), "manifest_id"),
        "backend_manifest_hash": _required_hash(value.get("backend_manifest_hash"), "backend_manifest_hash"),
        "backend_approval_hash": _required_hash(
            approval.get("approval_record_hash"), "approval_record_hash"
        ),
        "metadata_records": _metadata_records(value.get("downstream_hash_metadata_records")),
    }


def _validate_generation_approval(
    value: dict[str, Any],
    *,
    expected_input_id: str,
    expected_beo_hash: str,
    expected_publication_receipt_hash: str,
    expected_backend_manifest_hash: str,
    expected_backend_approval_hash: str,
    expected_output_id: str,
    trace_artifacts: list[dict[str, str]],
    metadata_record_identities: list[dict[str, str]],
) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("generation_approval must be a dictionary")
    _reject_forbidden_fields_shallow(value, "generation_approval")
    _reject_unsupported_fields(value, _APPROVAL_ALLOWED_KEYS, "generation_approval")
    normalized = {
        "approval_id": _required_identity_string(value.get("approval_id"), "approval_id"),
        "approval_record_hash": _required_hash(value.get("approval_record_hash"), "approval_record_hash"),
        "authorization_request_hash": _required_hash(
            value.get("authorization_request_hash"), "authorization_request_hash"
        ),
        "operator_identity": _required_identity_string(value.get("operator_identity"), "operator_identity"),
        "approval_scope": _required_string(value.get("approval_scope"), "approval_scope"),
        "approval_timestamp": _required_timestamp(value.get("approval_timestamp"), "approval_timestamp"),
        "approved_input_id": _required_identity_string(value.get("approved_input_id"), "approved_input_id"),
        "approved_beo_hash": _required_hash(value.get("approved_beo_hash"), "approved_beo_hash"),
        "approved_backend_manifest_hash": _required_hash(
            value.get("approved_backend_manifest_hash"), "approved_backend_manifest_hash"
        ),
        "approved_output_id": _required_identity_string(value.get("approved_output_id"), "approved_output_id"),
    }
    if normalized["approval_scope"] != _APPROVAL_SCOPE:
        raise ValueError("approval_scope must be OFFLINE_RTM_GENERATION_APPROVAL_FIXTURE_ONLY")
    _required_true(value.get("generation_authorized"), "generation_authorized")
    for flag in ["drift_rejection_authorized", "expired", "replayed", "stale"]:
        _required_false(value.get(flag), flag)
    if normalized["approved_input_id"] != expected_input_id:
        raise ValueError("approved_input_id does not match published-BEO input")
    if normalized["approved_beo_hash"] != expected_beo_hash:
        raise ValueError("approved_beo_hash does not match published-BEO input")
    if normalized["approved_backend_manifest_hash"] != expected_backend_manifest_hash:
        raise ValueError("approved_backend_manifest_hash does not match backend fixture")
    if normalized["approved_output_id"] != expected_output_id:
        raise ValueError("approved_output_id does not match requested RTM output")

    expected_request_hash = _canonical_hash(
        {
            "approval_scope": _APPROVAL_SCOPE,
            "approved_input_id": expected_input_id,
            "approved_beo_hash": expected_beo_hash,
            "publication_receipt_hash": expected_publication_receipt_hash,
            "approved_backend_manifest_hash": expected_backend_manifest_hash,
            "backend_approval_hash": expected_backend_approval_hash,
            "approved_output_id": expected_output_id,
            "trace_artifacts": _sorted_identity_hashes(trace_artifacts),
            "metadata_record_identities": metadata_record_identities,
            "drift_rejection_authorized": False,
        }
    )
    if normalized["authorization_request_hash"] != expected_request_hash:
        raise ValueError("authorization_request_hash does not match canonical RTM generation request")
    expected_record_hash = _canonical_hash(
        {
            "approval_id": normalized["approval_id"],
            "authorization_request_hash": expected_request_hash,
            "operator_identity": normalized["operator_identity"],
            "approval_scope": _APPROVAL_SCOPE,
            "approval_timestamp": normalized["approval_timestamp"],
            "generation_authorized": True,
            "drift_rejection_authorized": False,
            "expired": False,
            "replayed": False,
            "stale": False,
        }
    )
    if normalized["approval_record_hash"] != expected_record_hash:
        raise ValueError("approval_record_hash does not match canonical RTM generation approval")
    return normalized


def _metadata_records(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("downstream_hash_metadata_records must be a non-empty list")
    normalized: list[dict[str, str]] = []
    for record in value:
        if not isinstance(record, dict):
            raise ValueError("downstream_hash_metadata_records must contain objects")
        _reject_unsupported_fields(record, _METADATA_RECORD_ALLOWED_KEYS, "downstream_hash_metadata_records")
        _reject_forbidden_fields_recursive(record, "downstream_hash_metadata_records")
        if _required_string(record.get("metadata_source"), "metadata_source") != _METADATA_SOURCE:
            raise ValueError("metadata_source must be ACTIVE_VAULT_HASH_METADATA_FIXTURE_ONLY")
        _required_false(record.get("body_included"), "body_included")
        _required_false(record.get("body_read"), "body_read")
        normalized.append(
            {
                "kind": _required_identity_string(record.get("kind"), "kind"),
                "id": _required_identity_string(record.get("id"), "id"),
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
        _reject_unsupported_fields(artifact, _TRACE_ARTIFACT_ALLOWED_KEYS, "trace_artifacts")
        _reject_forbidden_fields_recursive(artifact, "trace_artifacts")
        normalized.append(
            {
                "kind": _required_identity_string(artifact.get("kind"), "trace_artifacts.kind"),
                "id": _required_identity_string(artifact.get("id"), "trace_artifacts.id"),
                "version_hash": _required_hash(
                    artifact.get("version_hash"), "trace_artifacts.version_hash"
                ),
            }
        )
    return normalized


def _coverage_records(
    trace_artifacts: list[dict[str, str]], metadata_records: list[dict[str, str]]
) -> list[dict[str, str]]:
    trace_identities = [(artifact["kind"], artifact["id"]) for artifact in trace_artifacts]
    if len(set(trace_identities)) != len(trace_identities):
        raise ValueError("duplicate trace artifact identity")
    metadata_identities = [(record["kind"], record["id"]) for record in metadata_records]
    if len(set(metadata_identities)) != len(metadata_identities):
        raise ValueError("duplicate hash metadata identity")
    trace_set = set(trace_identities)
    metadata_set = set(metadata_identities)
    if metadata_set - trace_set:
        raise ValueError("extra hash metadata identity not present in trace artifacts")
    if trace_set - metadata_set:
        raise ValueError("missing hash metadata for trace artifact")
    metadata_by_identity = {(record["kind"], record["id"]): record for record in metadata_records}
    coverage: list[dict[str, str]] = []
    for artifact in sorted(trace_artifacts, key=lambda item: (item["kind"], item["id"])):
        metadata = metadata_by_identity[(artifact["kind"], artifact["id"])]
        if metadata["version_hash"] != artifact["version_hash"]:
            raise ValueError("metadata version_hash mismatch for trace artifact")
        coverage.append(
            {
                "kind": artifact["kind"],
                "id": artifact["id"],
                "trace_version_hash": artifact["version_hash"],
                "metadata_version_hash": metadata["version_hash"],
                "coverage_state": _MATCHED,
                "drift_review_state": "DRIFT_REVIEW_REQUIRED_NOT_REJECTED",
            }
        )
    return coverage


def _metadata_record_identities(records: list[dict[str, str]]) -> list[dict[str, str]]:
    return _sorted_identity_hashes(records)


def _sorted_identity_hashes(records: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {"kind": record["kind"], "id": record["id"], "version_hash": record["version_hash"]}
        for record in sorted(records, key=lambda item: (item["kind"], item["id"]))
    ]


def _canonical_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _reject_forbidden_fields_shallow(value: dict[str, Any], label: str) -> None:
    for key in value:
        _reject_forbidden_key(key, label)


def _reject_forbidden_fields_recursive(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            _reject_forbidden_key(key, label)
            _reject_forbidden_fields_recursive(nested, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_fields_recursive(item, f"{label}[{index}]")


def _reject_forbidden_key(key: Any, label: str) -> None:
    if not isinstance(key, str):
        raise ValueError(f"{label} rejects non-string field")
    if key.lower() in _FORBIDDEN_KEYS:
        raise ValueError(f"{label} rejects forbidden field: {key}")


def _reject_unsupported_fields(value: dict[str, Any], allowed: set[str], label: str) -> None:
    for key in value:
        if not isinstance(key, str):
            raise ValueError(f"{label} rejects non-string field")
    extra = sorted(set(value) - allowed)
    if extra:
        raise ValueError(f"{label} rejects unsupported field: {extra[0]}")


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if not value.strip():
        raise ValueError(f"requires non-empty {field}")
    return value


def _required_identity_string(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if value != value.strip():
        raise ValueError(f"{field} rejects invalid identity format")
    text = value
    normalized_authority = re.sub(r"[^A-Z0-9]+", "_", text.upper()).strip("_")
    compact_identity = re.sub(r"[^A-Z0-9]+", "", text.upper())
    for marker in _FORBIDDEN_IDENTITY_AUTHORITY_MARKERS:
        compact_marker = re.sub(r"[^A-Z0-9]+", "", marker)
        if marker in normalized_authority or compact_marker in compact_identity:
            raise ValueError(f"{field} rejects forbidden identity authority")
    for marker in _FORBIDDEN_NORMALIZED_IDENTITY_MARKERS:
        if marker in normalized_authority or marker in compact_identity:
            raise ValueError(f"{field} rejects forbidden identity marker")
    lower = text.lower()
    for marker in _FORBIDDEN_IDENTITY_FRAGMENTS:
        if marker.lower() in lower:
            raise ValueError(f"{field} rejects forbidden identity fragment")
    upper = text.upper()
    for marker in _FORBIDDEN_IDENTITY_AUTHORITY_MARKERS:
        if marker in upper:
            raise ValueError(f"{field} rejects forbidden identity authority")
    pattern = _identity_pattern_for_field(field)
    if not pattern.match(text):
        raise ValueError(f"{field} rejects invalid identity format")
    return text


def _identity_pattern_for_field(field: str) -> re.Pattern[str]:
    if field.endswith(".kind") or field == "kind":
        return _TRACE_KIND_RE
    if field.endswith(".id") or field == "id":
        return _TRACE_ID_RE
    try:
        return _IDENTITY_RE[field]
    except KeyError as exc:
        raise ValueError(f"{field} has no identity validator") from exc


def _required_hash(value: Any, field: str) -> str:
    text = _required_string(value, field)
    if not _HASH_RE.match(text):
        raise ValueError(f"{field} must match sha256:<64 lowercase hex>")
    return text


def _required_timestamp(value: Any, field: str) -> str:
    text = _required_string(value, field)
    if not _TIMESTAMP_RE.match(text):
        raise ValueError(f"{field} rejects invalid timestamp format")
    return text


def _required_false(value: Any, field: str) -> None:
    if value is not False:
        raise ValueError(f"{field} must be false")


def _required_true(value: Any, field: str) -> None:
    if value is not True:
        raise ValueError(f"{field} must be true")
