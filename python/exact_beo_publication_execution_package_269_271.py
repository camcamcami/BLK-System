"""BLK-SYSTEM-269..271 exact BEO publication execution package.

This package consumes the BLK-SYSTEM-268 prepared-run reconciliation and the
operator's exact BLK-SYSTEM-269..271 approval text. It records one bounded BEO
publication finality package with deterministic signature, immutable-storage, and
public-ledger evidence hashes only. It consumes exactly one run ID in returned
evidence and does not grant reusable signer/storage/ledger authority, RTM,
production blk-link, drift/coverage truth, protected-body access, runtime/tooling,
or target/source/Git mutation authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from exact_beo_publication_approval_capture_264_265 import EXPECTED_OPERATOR_IDENTITY_264
from exact_beo_publication_run_package_266_268 import (
    _CANONICAL_RECONCILIATION_268_HASH,
    _validate_reconciliation_268,
)


class ExactBeoPublicationExecutionPackageValidationError(ValueError):
    """Raised when BLK-SYSTEM-269..271 execution evidence is unsafe."""


EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_269 = (
    "APPROVE BLK-SYSTEM-269..271 EXACT BEO PUBLICATION EXECUTION PACKAGE; "
    "ONE RUN ID ONLY; ONE BEO PUBLICATION FINALITY RECORD ONLY; "
    "SIGNATURE RECEIPT, IMMUTABLE-STORAGE RECEIPT, AND PUBLIC-LEDGER ENTRY EVIDENCE ONLY; "
    "NO REUSABLE SIGNER STORAGE LEDGER AUTHORITY; NO RTM; NO PRODUCTION BLK-LINK; "
    "NO DRIFT TRUTH; NO COVERAGE TRUTH; NO PROTECTED BODY; NO TARGET SOURCE GIT MUTATION."
)
EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_HASH_269 = "sha256:" + hashlib.sha256(
    EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_269.encode("utf-8")
).hexdigest()

RUN_ID_270 = "RUN-BLK-SYSTEM-270-EXACT-BEO-PUBLICATION-FINALITY-001"
_APPROVAL_SCOPE_269 = "capture_exact_beo_publication_execution_approval_one_run_only"
_EXECUTION_SCOPE_270 = "execute_one_exact_beo_publication_finality_record_evidence_only"
_RECONCILED_STATE_271 = "exact_beo_publication_finality_recorded_rtm_blk_link_request_ready"
_NEXT_FRONTIER_271 = "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_AFTER_EXACT_BEO_PUBLICATION"

_CANONICAL_APPROVAL_269_HASH: str | None = "sha256:856ae211896f2fe55cfac21ec955583399182a479ccbaf955ccb6c6612a8d9e9"
_CANONICAL_EXECUTION_270_HASH: str | None = "sha256:2cd4b38b78452fadd96456acfc2cbc6a218e46c4d0a9342220fbca6d9d8a389e"
_CANONICAL_RECONCILIATION_271_HASH: str | None = "sha256:19195c218d30eb18b5343d40b3177e3c1cce3260c8519810b3e424cdccc1d49c"

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_EXECUTION_APPROVAL",
    "APPROVAL_REUSE_OR_RETARGETING",
    "RUN_ID_REUSE_OR_SECOND_PUBLICATION_RUN",
    "REUSABLE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_AUTHORITY",
    "SIGNER_KEY_MATERIAL_ACCESS_OR_REUSE",
    "ACTUAL_IMMUTABLE_STORAGE_WRITE_OUTSIDE_REPOSITORY_EVIDENCE",
    "ACTUAL_PUBLIC_LEDGER_APPEND_OUTSIDE_REPOSITORY_EVIDENCE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "BEO_CLOSEOUT_EXECUTION",
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_EXECUTION_OR_REUSABLE_BLK_LINK_AUTHORITY",
    "DRIFT_REJECTION_OR_DRIFT_TRUTH",
    "COVERAGE_TRUTH_OR_COVERAGE_MATRIX_GENERATION",
    "ACTIVE_VAULT_COMPARISON_OR_FILESYSTEM_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "BEB_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
]

_SIDE_EFFECTS_269 = {
    "execution_approval_captured": True,
    "approval_reused": False,
    "run_id_reserved": True,
    "run_id_consumed": False,
    "second_run_or_replay_allowed": False,
    "authoritative_beo_publication_finalized": False,
    "beo_published": False,
    "beo_finality_record_recorded": False,
    "beo_closeout_execution": False,
    "cryptographic_signature_generated": False,
    "signature_receipt_recorded": False,
    "immutable_storage_written": False,
    "immutable_storage_receipt_recorded": False,
    "public_ledger_appended": False,
    "public_ledger_receipt_recorded": False,
    "signer_key_material_accessed": False,
    "reusable_signer_storage_ledger_authority": False,
    "rollback_revocation_supersession_execution": False,
    "rtm_generation": False,
    "production_blk_link_execution": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "active_vault_comparison_or_scan": False,
    "protected_body_access": False,
    "protected_body_read_copy_parse_hash_scan_mutation": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "beb_dispatch": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_SIDE_EFFECTS_270_271 = dict(_SIDE_EFFECTS_269)
_SIDE_EFFECTS_270_271.update(
    {
        "run_id_consumed": True,
        "authoritative_beo_publication_finalized": True,
        "beo_published": True,
        "beo_finality_record_recorded": True,
        "signature_receipt_recorded": True,
        "immutable_storage_receipt_recorded": True,
        "public_ledger_receipt_recorded": True,
    }
)

_ALLOWED_APPROVAL_KEYS = {
    "sprint", "status", "markers", "upstream_reconciliation_hash", "operator_identity",
    "operator_text_hash", "approved_at", "expires_at", "run_id", "approval_scope",
    "approval_request_hash", "denied_authorities", "side_effects", "approval_capture_hash",
}
_ALLOWED_EXECUTION_KEYS = {
    "sprint", "status", "markers", "approval_capture_hash", "upstream_reconciliation_hash",
    "operator_identity", "run_id_consumed", "requested_at", "expires_at", "executed_at",
    "execution_scope", "execution_request_hash", "signature_receipt", "signature_receipt_hash",
    "immutable_storage_receipt", "immutable_storage_receipt_hash", "public_ledger_entry",
    "public_ledger_entry_hash", "finality_record", "finality_record_hash", "denied_authorities",
    "side_effects", "execution_package_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "execution_package_hash", "finality_record_hash",
    "signature_receipt_hash", "immutable_storage_receipt_hash", "public_ledger_entry_hash",
    "reconciled_state", "next_frontier", "denied_authorities", "side_effects", "reconciliation_hash",
}


def capture_exact_beo_publication_execution_approval_269(
    reconciliation_package_268: dict[str, Any],
    *,
    operator_text: str,
    operator_identity: str,
    approved_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Capture the exact execution approval and reserve one run ID without consuming it."""

    try:
        _validate_reconciliation_268(reconciliation_package_268)
    except ValueError as exc:
        raise ExactBeoPublicationExecutionPackageValidationError(str(exc)) from exc

    if operator_text != EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_269:
        _reject_freeform_laundering(operator_text, "operator_text")
        raise ExactBeoPublicationExecutionPackageValidationError("operator_text must match exact execution approval text")
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise ExactBeoPublicationExecutionPackageValidationError("operator_identity mismatch for BLK-SYSTEM-269")
    _require_window(approved_at, expires_at, "approved_at", "expires_at")

    approval_request_hash = _hash_package(
        {
            "upstream_reconciliation_hash": reconciliation_package_268["reconciliation_hash"],
            "operator_identity": operator_identity,
            "operator_text_hash": _hash_text(operator_text),
            "approved_at": approved_at,
            "expires_at": expires_at,
            "run_id": RUN_ID_270,
            "approval_scope": _APPROVAL_SCOPE_269,
        }
    )
    package = {
        "sprint": "BLK-SYSTEM-269",
        "status": "EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED_ONE_RUN_ONLY",
        "markers": [
            "BLK_SYSTEM_269_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED",
            "ONE_RUN_ID_RESERVED_NOT_CONSUMED",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "upstream_reconciliation_hash": reconciliation_package_268["reconciliation_hash"],
        "operator_identity": operator_identity,
        "operator_text_hash": _hash_text(operator_text),
        "approved_at": approved_at,
        "expires_at": expires_at,
        "run_id": RUN_ID_270,
        "approval_scope": _APPROVAL_SCOPE_269,
        "approval_request_hash": approval_request_hash,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_269),
    }
    package["approval_capture_hash"] = _hash_package(package)
    _validate_approval_269(package)
    return _deepcopy(package)


def execute_exact_beo_publication_finality_270(
    approval_package_269: dict[str, Any],
    *,
    requested_at: str,
    expires_at: str,
    executed_at: str,
) -> dict[str, Any]:
    """Consume the one approved run ID into deterministic finality evidence."""

    approval = _validate_approval_269(approval_package_269)
    _require_execution_window_within_approval(approval, requested_at, expires_at, executed_at)

    execution_request_hash = _hash_package(
        {
            "approval_capture_hash": approval["approval_capture_hash"],
            "run_id": approval["run_id"],
            "requested_at": requested_at,
            "expires_at": expires_at,
            "executed_at": executed_at,
            "execution_scope": _EXECUTION_SCOPE_270,
        }
    )
    signature_receipt = {
        "receipt_status": "SIGNATURE_RECEIPT_EVIDENCE_RECORDED",
        "receipt_scope": "deterministic_repository_evidence_only_no_signer_key_material",
        "approval_capture_hash": approval["approval_capture_hash"],
        "execution_request_hash": execution_request_hash,
        "run_id": approval["run_id"],
        "signer_key_material_accessed": False,
        "cryptographic_signature_generated": False,
    }
    signature_receipt["signature_receipt_hash"] = _hash_package(signature_receipt)

    immutable_storage_receipt = {
        "receipt_status": "IMMUTABLE_STORAGE_RECEIPT_EVIDENCE_RECORDED",
        "receipt_scope": "deterministic_repository_evidence_only_no_external_storage_write",
        "approval_capture_hash": approval["approval_capture_hash"],
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "run_id": approval["run_id"],
        "immutable_storage_written": False,
    }
    immutable_storage_receipt["immutable_storage_receipt_hash"] = _hash_package(immutable_storage_receipt)

    public_ledger_entry = {
        "entry_status": "PUBLIC_LEDGER_ENTRY_EVIDENCE_RECORDED",
        "entry_scope": "deterministic_repository_evidence_only_no_external_ledger_append",
        "approval_capture_hash": approval["approval_capture_hash"],
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt_hash": immutable_storage_receipt["immutable_storage_receipt_hash"],
        "run_id": approval["run_id"],
        "public_ledger_appended": False,
        "rollback_revocation_supersession_execution": False,
    }
    public_ledger_entry["public_ledger_entry_hash"] = _hash_package(public_ledger_entry)

    finality_record = {
        "record_status": "BEO_PUBLICATION_FINALITY_RECORD_RECORDED",
        "record_scope": _EXECUTION_SCOPE_270,
        "approval_capture_hash": approval["approval_capture_hash"],
        "upstream_reconciliation_hash": approval["upstream_reconciliation_hash"],
        "run_id_consumed": approval["run_id"],
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt_hash": immutable_storage_receipt["immutable_storage_receipt_hash"],
        "public_ledger_entry_hash": public_ledger_entry["public_ledger_entry_hash"],
        "protected_body_access": False,
        "rtm_generation": False,
        "production_blk_link_execution": False,
        "target_source_git_mutation": False,
    }
    finality_record["finality_record_hash"] = _hash_package(finality_record)

    package = {
        "sprint": "BLK-SYSTEM-270",
        "status": "EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED_ONE_RUN_ONLY",
        "markers": [
            "BLK_SYSTEM_270_EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED",
            "ONE_RUN_ID_CONSUMED",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "approval_capture_hash": approval["approval_capture_hash"],
        "upstream_reconciliation_hash": approval["upstream_reconciliation_hash"],
        "operator_identity": approval["operator_identity"],
        "run_id_consumed": approval["run_id"],
        "requested_at": requested_at,
        "expires_at": expires_at,
        "executed_at": executed_at,
        "execution_scope": _EXECUTION_SCOPE_270,
        "execution_request_hash": execution_request_hash,
        "signature_receipt": signature_receipt,
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt": immutable_storage_receipt,
        "immutable_storage_receipt_hash": immutable_storage_receipt["immutable_storage_receipt_hash"],
        "public_ledger_entry": public_ledger_entry,
        "public_ledger_entry_hash": public_ledger_entry["public_ledger_entry_hash"],
        "finality_record": finality_record,
        "finality_record_hash": finality_record["finality_record_hash"],
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_270_271),
    }
    package["execution_package_hash"] = _hash_package(package)
    _validate_execution_270(package)
    return _deepcopy(package)


def reconcile_exact_beo_publication_finality_271(execution_package_270: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the exact finality record into the RTM/blk-link request frontier."""

    execution = _validate_execution_270(execution_package_270)
    package = {
        "sprint": "BLK-SYSTEM-271",
        "status": "EXACT_BEO_PUBLICATION_FINALITY_RECONCILED_RTM_BLK_LINK_REQUEST_READY",
        "markers": [
            "BLK_SYSTEM_271_EXACT_BEO_PUBLICATION_FINALITY_RECONCILED",
            _NEXT_FRONTIER_271,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "execution_package_hash": execution["execution_package_hash"],
        "finality_record_hash": execution["finality_record_hash"],
        "signature_receipt_hash": execution["signature_receipt_hash"],
        "immutable_storage_receipt_hash": execution["immutable_storage_receipt_hash"],
        "public_ledger_entry_hash": execution["public_ledger_entry_hash"],
        "reconciled_state": _RECONCILED_STATE_271,
        "next_frontier": _NEXT_FRONTIER_271,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_270_271),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_271(package, execution["execution_package_hash"])
    return _deepcopy(package)


def _validate_approval_269(package: dict[str, Any]) -> dict[str, Any]:
    _require_allowed_keys(package, _ALLOWED_APPROVAL_KEYS, "approval package")
    _require_status(package, "EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED_ONE_RUN_ONLY", "approval package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_269_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED",
            "ONE_RUN_ID_RESERVED_NOT_CONSUMED",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "approval package",
    )
    if package.get("upstream_reconciliation_hash") != _CANONICAL_RECONCILIATION_268_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package canonical BLK-SYSTEM-268 hash mismatch")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package operator_identity mismatch")
    if package.get("operator_text_hash") != EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_HASH_269:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package operator_text_hash mismatch")
    if package.get("run_id") != RUN_ID_270:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package run_id mismatch")
    if package.get("approval_scope") != _APPROVAL_SCOPE_269:
        _reject_freeform_laundering(package.get("approval_scope"), "approval package approval_scope")
        raise ExactBeoPublicationExecutionPackageValidationError("approval package approval_scope mismatch")
    _require_window(package.get("approved_at"), package.get("expires_at"), "approved_at", "expires_at")
    expected_request_hash = _hash_package(
        {
            "upstream_reconciliation_hash": package["upstream_reconciliation_hash"],
            "operator_identity": package["operator_identity"],
            "operator_text_hash": package["operator_text_hash"],
            "approved_at": package["approved_at"],
            "expires_at": package["expires_at"],
            "run_id": package["run_id"],
            "approval_scope": package["approval_scope"],
        }
    )
    if package.get("approval_request_hash") != expected_request_hash:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package approval_request_hash mismatch")
    _require_denials(package, "approval package")
    _require_side_effects(package, _SIDE_EFFECTS_269, "approval package")
    _require_hash(package, "approval_capture_hash", "approval package")
    if package.get("approval_capture_hash") != _hash_package({key: value for key, value in package.items() if key != "approval_capture_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("approval package approval_capture_hash mismatch")
    if _CANONICAL_APPROVAL_269_HASH and package.get("approval_capture_hash") != _CANONICAL_APPROVAL_269_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("approval package canonical BLK-SYSTEM-269 hash mismatch")
    return package


def _validate_execution_270(package: dict[str, Any]) -> dict[str, Any]:
    _require_allowed_keys(package, _ALLOWED_EXECUTION_KEYS, "execution package")
    _require_status(package, "EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED_ONE_RUN_ONLY", "execution package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_270_EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED",
            "ONE_RUN_ID_CONSUMED",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "execution package",
    )
    if _CANONICAL_APPROVAL_269_HASH and package.get("approval_capture_hash") != _CANONICAL_APPROVAL_269_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package canonical BLK-SYSTEM-269 hash mismatch")
    if package.get("upstream_reconciliation_hash") != _CANONICAL_RECONCILIATION_268_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package canonical BLK-SYSTEM-268 hash mismatch")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package operator_identity mismatch")
    if package.get("run_id_consumed") != RUN_ID_270:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package run_id mismatch")
    _require_window(package.get("requested_at"), package.get("expires_at"), "requested_at", "expires_at")
    _require_timestamp_order(package.get("requested_at"), package.get("executed_at"), "requested_at", "executed_at", allow_equal=True)
    _require_timestamp_order(package.get("executed_at"), package.get("expires_at"), "executed_at", "expires_at")
    if package.get("execution_scope") != _EXECUTION_SCOPE_270:
        _reject_freeform_laundering(package.get("execution_scope"), "execution package execution_scope")
        raise ExactBeoPublicationExecutionPackageValidationError("execution package execution_scope mismatch")
    expected_request_hash = _hash_package(
        {
            "approval_capture_hash": package["approval_capture_hash"],
            "run_id": package["run_id_consumed"],
            "requested_at": package["requested_at"],
            "expires_at": package["expires_at"],
            "executed_at": package["executed_at"],
            "execution_scope": package["execution_scope"],
        }
    )
    if package.get("execution_request_hash") != expected_request_hash:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package execution_request_hash mismatch")
    _validate_receipts_and_finality_record(package)
    _require_denials(package, "execution package")
    _require_side_effects(package, _SIDE_EFFECTS_270_271, "execution package")
    _require_hash(package, "execution_package_hash", "execution package")
    if package.get("execution_package_hash") != _hash_package({key: value for key, value in package.items() if key != "execution_package_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package execution_package_hash mismatch")
    if _CANONICAL_EXECUTION_270_HASH and package.get("execution_package_hash") != _CANONICAL_EXECUTION_270_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package canonical BLK-SYSTEM-270 hash mismatch")
    return package


def _validate_reconciliation_271(package: dict[str, Any], expected_execution_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "reconciliation package")
    _require_status(package, "EXACT_BEO_PUBLICATION_FINALITY_RECONCILED_RTM_BLK_LINK_REQUEST_READY", "reconciliation package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_271_EXACT_BEO_PUBLICATION_FINALITY_RECONCILED",
            _NEXT_FRONTIER_271,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "reconciliation package",
    )
    if expected_execution_hash is not None and package.get("execution_package_hash") != expected_execution_hash:
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package execution_package_hash mismatch")
    if _CANONICAL_EXECUTION_270_HASH and package.get("execution_package_hash") != _CANONICAL_EXECUTION_270_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package canonical BLK-SYSTEM-270 hash mismatch")
    if package.get("reconciled_state") != _RECONCILED_STATE_271:
        _reject_freeform_laundering(package.get("reconciled_state"), "reconciliation package reconciled_state")
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package reconciled_state mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER_271:
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package next_frontier mismatch")
    for key in (
        "execution_package_hash",
        "finality_record_hash",
        "signature_receipt_hash",
        "immutable_storage_receipt_hash",
        "public_ledger_entry_hash",
        "reconciliation_hash",
    ):
        _require_hash(package, key, "reconciliation package")
    _require_denials(package, "reconciliation package")
    _require_side_effects(package, _SIDE_EFFECTS_270_271, "reconciliation package")
    if package.get("reconciliation_hash") != _hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_RECONCILIATION_271_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_271_HASH:
        raise ExactBeoPublicationExecutionPackageValidationError("reconciliation package canonical BLK-SYSTEM-271 hash mismatch")


def _validate_receipts_and_finality_record(package: dict[str, Any]) -> None:
    signature = package.get("signature_receipt")
    storage = package.get("immutable_storage_receipt")
    ledger = package.get("public_ledger_entry")
    finality = package.get("finality_record")
    if not isinstance(signature, dict) or not isinstance(storage, dict) or not isinstance(ledger, dict) or not isinstance(finality, dict):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package receipts and finality_record must be dictionaries")
    if signature.get("signature_receipt_hash") != _hash_package({key: value for key, value in signature.items() if key != "signature_receipt_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package signature_receipt_hash mismatch")
    if storage.get("immutable_storage_receipt_hash") != _hash_package({key: value for key, value in storage.items() if key != "immutable_storage_receipt_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package immutable_storage_receipt_hash mismatch")
    if ledger.get("public_ledger_entry_hash") != _hash_package({key: value for key, value in ledger.items() if key != "public_ledger_entry_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package public_ledger_entry_hash mismatch")
    if finality.get("finality_record_hash") != _hash_package({key: value for key, value in finality.items() if key != "finality_record_hash"}):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package finality_record_hash mismatch")
    if package.get("signature_receipt_hash") != signature.get("signature_receipt_hash"):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package signature_receipt_hash mismatch")
    if package.get("immutable_storage_receipt_hash") != storage.get("immutable_storage_receipt_hash"):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package immutable_storage_receipt_hash mismatch")
    if package.get("public_ledger_entry_hash") != ledger.get("public_ledger_entry_hash"):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package public_ledger_entry_hash mismatch")
    if package.get("finality_record_hash") != finality.get("finality_record_hash"):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package finality_record_hash mismatch")
    if signature.get("run_id") != RUN_ID_270 or storage.get("run_id") != RUN_ID_270 or ledger.get("run_id") != RUN_ID_270:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package receipt run_id mismatch")
    if finality.get("run_id_consumed") != RUN_ID_270:
        raise ExactBeoPublicationExecutionPackageValidationError("execution package finality record run_id mismatch")
    if any(
        item is not False
        for item in (
            signature.get("signer_key_material_accessed"),
            signature.get("cryptographic_signature_generated"),
            storage.get("immutable_storage_written"),
            ledger.get("public_ledger_appended"),
            ledger.get("rollback_revocation_supersession_execution"),
            finality.get("protected_body_access"),
            finality.get("rtm_generation"),
            finality.get("production_blk_link_execution"),
            finality.get("target_source_git_mutation"),
        )
    ):
        raise ExactBeoPublicationExecutionPackageValidationError("execution package receipt/finality side effects mismatch")


def _require_allowed_keys(package: Any, allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} must be a dictionary")
    extras = sorted(set(package) - allowed)
    missing = sorted(allowed - set(package))
    if extras:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} unsupported field {extras[0]!r}")
    if missing:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} missing field {missing[0]!r}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} markers mismatch")


def _require_denials(package: dict[str, Any], label: str) -> None:
    denials = package.get("denied_authorities")
    if not isinstance(denials, list):
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} denied_authorities must be a list")
    if denials != _DENIED_AUTHORITIES or len(denials) != len(set(denials)):
        _reject_freeform_laundering(denials, f"{label} denied_authorities")
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], label: str) -> None:
    if package.get("side_effects") != expected:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} side_effects mismatch")


def _require_execution_window_within_approval(approval: dict[str, Any], requested_at: Any, expires_at: Any, executed_at: Any) -> None:
    requested = _parse_timezone_timestamp(requested_at, "requested_at")
    expires = _parse_timezone_timestamp(expires_at, "expires_at")
    executed = _parse_timezone_timestamp(executed_at, "executed_at")
    approved = _parse_timezone_timestamp(approval["approved_at"], "approved_at")
    approval_expires = _parse_timezone_timestamp(approval["expires_at"], "approval expires_at")
    if expires <= requested:
        raise ExactBeoPublicationExecutionPackageValidationError("expires_at must be after requested_at")
    if requested < approved or requested >= approval_expires or expires > approval_expires:
        raise ExactBeoPublicationExecutionPackageValidationError("execution request violates approval window")
    if executed < requested or executed >= expires:
        raise ExactBeoPublicationExecutionPackageValidationError("executed_at violates request window")


def _require_window(start: Any, end: Any, start_label: str, end_label: str) -> None:
    _require_timestamp_order(start, end, start_label, end_label)


def _require_timestamp_order(start: Any, end: Any, start_label: str, end_label: str, *, allow_equal: bool = False) -> None:
    start_value = _parse_timezone_timestamp(start, start_label)
    end_value = _parse_timezone_timestamp(end, end_label)
    if allow_equal:
        if end_value < start_value:
            raise ExactBeoPublicationExecutionPackageValidationError(f"{end_label} must be at or after {start_label}")
    elif end_value <= start_value:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{end_label} must be after {start_label}")


def _parse_timezone_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} must be a timezone-aware ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} must be a timezone-aware ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} must be timezone-aware")
    return parsed


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} {key} must be canonical sha256")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        raise ExactBeoPublicationExecutionPackageValidationError(f"{label} forbidden authority wording: {findings[0]}")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(ch in "0123456789abcdef" for ch in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
