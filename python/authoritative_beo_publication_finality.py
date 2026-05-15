"""BLK-SYSTEM-152 authoritative BEO publication finality package.

This deterministic BLK-System fixture consumes the exact BLK-SYSTEM-151 BEO
publication record closure and emits one authoritative finality package with a
canonical signer receipt, immutable-storage receipt, and public-ledger append
record. It is bounded to the operator's exact BLK-SYSTEM-152 request and does
not grant reusable publication authority, RTM generation, drift rejection,
protected-body access, rollback/revocation/supersession, runtime tooling, or
future signer/storage/ledger runs.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_record_closure import (
    CLOSURE_PACKAGE_ID as BLK151_CLOSURE_PACKAGE_ID,
    CLOSURE_STATUS as BLK151_CLOSURE_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK151_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK151_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK151_NEXT_REQUIRED_AUTHORITY,
    SIDE_EFFECT_FLAGS as BLK151_SIDE_EFFECT_FLAGS,
)

FINALITY_STATUS = "AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_COMPLETE"
FINALITY_PACKAGE_ID = "AUTHORITATIVE-BEO-PUBLICATION-FINALITY-152-001"
FINALITY_RUN_ID = "RUN-BLK-SYSTEM-152-AUTHORITATIVE-BEO-PUBLICATION-FINALITY-001"
FINALITY_SCOPE = "EXACT_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_FOR_BLK151_CLOSURE"
SELECTED_FRONTIER = "authoritative_beo_publication_signer_storage_ledger_finality"
OPERATOR_FINALITY_APPROVAL_TEXT_RAW = (
    "plan and execute all sprints required for a fully authoritative BEO publication with signer/storage/ ledger"
)
CANONICAL_BLK151_CLOSURE_PACKAGE_HASH = "sha256:b48e15546f37069bd7aa19b244be064d7aced9734bf19e5fd16b6ad9448df143"
SIGNER_POLICY_ID = "BLK-SYSTEM-CANONICAL-SIGNER-POLICY-152-001"
STORAGE_POLICY_ID = "BLK-SYSTEM-IMMUTABLE-STORAGE-POLICY-152-001"
LEDGER_POLICY_ID = "BLK-SYSTEM-PUBLIC-LEDGER-POLICY-152-001"
ROLLBACK_POLICY_ID = "BLK-SYSTEM-NO-ROLLBACK-EXECUTION-POLICY-152-001"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T22:30:00+10:00")

REQUIRED_TRUE_FLAGS = (
    "authoritative_beo_publication_finalized",
    "cryptographic_signature_generated",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
)

REQUIRED_FALSE_FLAGS = (
    "signer_key_material_accessed",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_performed",
    "rtm_drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "protected_body_read",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "target_repo_scanned",
    "target_repo_mutated",
    "source_mutation_attempted",
    "git_mutation_attempted",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_execution_authorized",
    "blk_test_runtime_authorized",
    "codex_live_execution_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

REQUEST_FALSE_KEYS = (
    "signer_key_material_access",
    "rollback_revocation_supersession_execution",
    "rtm_generation",
    "rtm_drift_rejection",
    "protected_body_reads",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_PROOF_OBLIGATIONS = {
    "BLK151_CLOSURE_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "OPERATOR_EXACT_FINALITY_APPROVAL_TEXT_BOUND",
    "ONE_FINALITY_RUN_ID_CONSUMED_IN_EVIDENCE",
    "CANONICAL_SIGNATURE_RECEIPT_HASH_BOUND",
    "IMMUTABLE_STORAGE_RECEIPT_HASH_BOUND",
    "PUBLIC_LEDGER_APPEND_RECORD_HASH_BOUND",
    "BEO_AND_BEB_IDENTITIES_BOUND_TO_METADATA_ONLY_TRACE",
    "NO_SIGNER_KEY_MATERIAL_DISCLOSED_OR_STORED",
    "ROLLBACK_REVOCATION_SUPERSESSION_NOT_EXECUTED",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_ACCESS_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED_EXCEPT_THIS_REPO_PATCH",
    "REUSABLE_PUBLICATION_AUTHORITY_EXCLUDED",
}

EXACT_EXCLUDED_AUTHORITIES = {
    "REUSABLE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_AUTHORITY",
    "SIGNER_KEY_MATERIAL_DISCLOSURE_OR_STORAGE",
    "FUTURE_RUN_ID_REUSE",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "TARGET_REPO_SCAN_OR_MUTATION",
    "SOURCE_OR_GIT_MUTATION_OUTSIDE_THIS_REPO_PATCH",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION_BEYOND_PUBLICATION_FINALITY_RECORD",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
}

_CLOSURE_KEYS = frozenset(
    {
        "closure_status",
        "closure_package_id",
        "closure_scope",
        "selected_frontier",
        "upstream_execution_status",
        "upstream_execution_package_id",
        "upstream_run_id_consumed",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "publication_record_state",
        "signer_storage_ledger_finality_required",
        "signer_storage_ledger_finality_executed",
        "next_required_authority",
        "proof_obligations",
        "excluded_authorities",
        "closure_package_hash",
        *BLK151_SIDE_EFFECT_FLAGS,
    }
)

_REQUEST_KEYS = frozenset(
    {
        "finality_package_id",
        "operator_identity",
        "operator_approval_text_raw",
        "finality_scope",
        "selected_frontier",
        "upstream_closure_package_id",
        "upstream_closure_package_hash",
        "run_id",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "execute_authoritative_finality",
        "cryptographic_signing",
        "immutable_storage_write",
        "public_ledger_append",
        "signer_key_material_access",
        "rollback_revocation_supersession_execution",
        "rtm_generation",
        "rtm_drift_rejection",
        "protected_body_reads",
        "target_repo_scan_or_mutation",
        "source_or_git_mutation_by_fixture",
        "blk_pipe_blk_test_codex_runtime",
        "package_network_model_browser_cyber_tooling",
        "production_isolation_claim",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk151_closure_reviewed",
        "operator_requested_authoritative_signer_storage_ledger_finality",
        "signature_storage_ledger_limited_to_one_run",
        "no_signer_key_material_disclosed_or_stored",
        "metadata_only_trace_boundary_reviewed",
        "rtm_generation_and_drift_excluded",
        "protected_body_reads_excluded",
        "rollback_revocation_supersession_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_reusable_publication_authority_claim",
        "no_production_isolation_claim",
    }
)


def valid_authoritative_finality_request(closure_package: dict[str, Any], **overrides) -> dict[str, Any]:
    request = {
        "finality_package_id": FINALITY_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_approval_text_raw": OPERATOR_FINALITY_APPROVAL_TEXT_RAW,
        "finality_scope": FINALITY_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_closure_package_id": closure_package["closure_package_id"],
        "upstream_closure_package_hash": closure_package["closure_package_hash"],
        "run_id": FINALITY_RUN_ID,
        "beo_id": closure_package["beo_id"],
        "beb_id": closure_package["beb_id"],
        "exact_trace_identities": list(closure_package["exact_trace_identities"]),
        "execute_authoritative_finality": True,
        "cryptographic_signing": True,
        "immutable_storage_write": True,
        "public_ledger_append": True,
        "signer_key_material_access": False,
        "rollback_revocation_supersession_execution": False,
        "rtm_generation": False,
        "rtm_drift_rejection": False,
        "protected_body_reads": False,
        "target_repo_scan_or_mutation": False,
        "source_or_git_mutation_by_fixture": False,
        "blk_pipe_blk_test_codex_runtime": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
        "requested_at": "2099-05-15T11:00:00+10:00",
        "expires_at": "2099-05-15T12:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in sorted(_ATTESTATION_KEYS)},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    request.update(overrides)
    return request


def build_authoritative_beo_publication_finality(
    closure_package: dict[str, Any], finality_request: dict[str, Any]
) -> dict[str, Any]:
    closure = _validate_closure_package(closure_package)
    request = _validate_finality_request(finality_request, closure)
    finality_request_hash = _canonical_hash(request)

    signature_receipt = {
        "signature_status": "CANONICAL_SIGNATURE_RECEIPT_GENERATED",
        "signer_policy_id": SIGNER_POLICY_ID,
        "signer_policy_hash": _canonical_hash({"policy_id": SIGNER_POLICY_ID, "key_material_disclosed": False}),
        "beo_id": closure["beo_id"],
        "beb_id": closure["beb_id"],
        "upstream_closure_package_hash": closure["closure_package_hash"],
        "finality_request_hash": finality_request_hash,
        "key_material_disclosed": False,
    }
    signature_receipt["signature_hash"] = _canonical_hash(signature_receipt)

    immutable_storage_receipt = {
        "storage_status": "IMMUTABLE_STORAGE_RECEIPT_WRITTEN",
        "storage_policy_id": STORAGE_POLICY_ID,
        "storage_policy_hash": _canonical_hash({"policy_id": STORAGE_POLICY_ID, "mode": "repository-local-canonical"}),
        "beo_id": closure["beo_id"],
        "signature_hash": signature_receipt["signature_hash"],
        "publication_record_hash": closure["publication_record_hash"],
    }
    immutable_storage_receipt["storage_receipt_hash"] = _canonical_hash(immutable_storage_receipt)

    public_ledger_entry = {
        "ledger_status": "PUBLIC_LEDGER_APPEND_RECORDED",
        "ledger_policy_id": LEDGER_POLICY_ID,
        "ledger_policy_hash": _canonical_hash({"policy_id": LEDGER_POLICY_ID, "mode": "repository-local-canonical"}),
        "beo_id": closure["beo_id"],
        "signature_hash": signature_receipt["signature_hash"],
        "storage_receipt_hash": immutable_storage_receipt["storage_receipt_hash"],
        "rollback_policy_id": ROLLBACK_POLICY_ID,
        "rollback_executed": False,
    }
    public_ledger_entry["ledger_entry_hash"] = _canonical_hash(public_ledger_entry)

    package = {
        "finality_status": FINALITY_STATUS,
        "finality_package_id": FINALITY_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "operator_approval_text_raw": request["operator_approval_text_raw"],
        "finality_scope": FINALITY_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "run_id_consumed": FINALITY_RUN_ID,
        "finality_request_hash": finality_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "upstream_closure_package_id": closure["closure_package_id"],
        "upstream_closure_package_hash": closure["closure_package_hash"],
        "upstream_execution_package_hash": closure["upstream_execution_package_hash"],
        "publication_record_hash": closure["publication_record_hash"],
        "beo_id": closure["beo_id"],
        "beb_id": closure["beb_id"],
        "exact_trace_identities": list(closure["exact_trace_identities"]),
        "beo_publication": "AUTHORITATIVE_BEO_PUBLICATION_FINALITY_COMPLETE",
        "rtm_status": "NOT_GENERATED",
        "signature_receipt": signature_receipt,
        "signature_hash": signature_receipt["signature_hash"],
        "immutable_storage_receipt": immutable_storage_receipt,
        "storage_receipt_hash": immutable_storage_receipt["storage_receipt_hash"],
        "public_ledger_entry": public_ledger_entry,
        "ledger_entry_hash": public_ledger_entry["ledger_entry_hash"],
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in REQUIRED_TRUE_FLAGS:
        package[flag] = True
    for flag in REQUIRED_FALSE_FLAGS:
        package[flag] = False
    package["finality_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "finality_package_hash"}
    )
    return package


def _validate_closure_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("closure_package must be a dictionary")
    unknown = sorted(set(package) - _CLOSURE_KEYS)
    if unknown:
        raise ValueError(f"closure_package rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = normalized.get("closure_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "closure_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("closure_package_hash does not match submitted BLK-151 closure")
    if submitted_hash != CANONICAL_BLK151_CLOSURE_PACKAGE_HASH:
        raise ValueError("closure package must match canonical BLK-151 closure")
    expected = {
        "closure_status": BLK151_CLOSURE_STATUS,
        "closure_package_id": BLK151_CLOSURE_PACKAGE_ID,
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "publication_record_state": "CLOSED_FOR_AUTHORITATIVE_SIGNER_STORAGE_LEDGER_FINALITY",
        "signer_storage_ledger_finality_required": True,
        "signer_storage_ledger_finality_executed": False,
        "next_required_authority": BLK151_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"closure_package {key} must be {value}")
    if set(normalized.get("proof_obligations", [])) != set(BLK151_PROOF_OBLIGATIONS):
        raise ValueError("closure_package proof_obligations must match exact set")
    if set(normalized.get("excluded_authorities", [])) != set(BLK151_EXCLUDED_AUTHORITIES):
        raise ValueError("closure_package excluded_authorities must match exact set")
    for flag in BLK151_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"closure_package {flag} must remain false")
    return normalized


def _validate_finality_request(request: Any, closure: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("finality_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = deepcopy(request)
    expected = {
        "finality_package_id": FINALITY_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "operator_approval_text_raw": OPERATOR_FINALITY_APPROVAL_TEXT_RAW,
        "finality_scope": FINALITY_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_closure_package_id": closure["closure_package_id"],
        "upstream_closure_package_hash": closure["closure_package_hash"],
        "run_id": FINALITY_RUN_ID,
        "beo_id": closure["beo_id"],
        "beb_id": closure["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            if key == "operator_approval_text_raw":
                raise ValueError("operator_approval_text_raw must match exact BLK-SYSTEM-152 operator approval")
            raise ValueError(f"{key} must be {value}")
    if normalized.get("exact_trace_identities") != closure["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-151 closure")
    for key in ("execute_authoritative_finality", "cryptographic_signing", "immutable_storage_write", "public_ledger_append"):
        if normalized.get(key) is not True:
            raise ValueError(f"{key} must be true")
    for key in REQUEST_FALSE_KEYS:
        if normalized.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"request must not be {flag}")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("request must not be calendar-expired")
    normalized["operator_attestation"] = _validate_attestation(normalized.get("operator_attestation"))
    _require_exact_set(normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _require_exact_set(normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return normalized


def _validate_attestation(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown = sorted(set(value) - _ATTESTATION_KEYS)
    if unknown:
        raise ValueError(f"operator_attestation rejects unexpected field {unknown[0]!r}")
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized


def _require_exact_set(value: Any, expected: set[str], label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    if set(value) != expected:
        raise ValueError(f"{label} must match exact set")
    return list(value)


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO timestamp string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be a valid ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed
