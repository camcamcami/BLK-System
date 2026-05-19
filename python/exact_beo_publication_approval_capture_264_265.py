"""BLK-SYSTEM-264..265 exact BEO publication approval capture package.

This package consumes the BLK-SYSTEM-257..260 exact BEO publication approval
preflight ladder and the BLK-SYSTEM-261..263 sprint-package selection guard. It
records the operator's exact contract text and reconciles the next frontier while
preserving no run, signer/storage/ledger, RTM, production blk-link, protected-body,
runtime/tooling, or source/Git side effects.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_sprint_package_granularity_guard_261_263 import _validate_selection_263
from exact_beo_publication_approval_ladder_257_260 import (
    EXACT_OPERATOR_APPROVAL_TEXT_258,
    _validate_258_contract,
    _validate_260_reconciliation,
)


class ExactBeoPublicationApprovalCaptureValidationError(ValueError):
    """Raised when BLK-SYSTEM-264..265 approval-capture evidence is unsafe."""


EXPECTED_OPERATOR_IDENTITY_264 = "discord:684235178083745819"
EXPECTED_SELECTION_HASH_263 = "sha256:b3fbfbc3ba4384a4b60143f9ff66aae41ddfe156eed4706575f48c645861cbc8"
EXACT_OPERATOR_APPROVAL_TEXT_HASH_264 = "sha256:" + hashlib.sha256(
    EXACT_OPERATOR_APPROVAL_TEXT_258.encode("utf-8")
).hexdigest()
_NEXT_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_PACKAGE_REQUIRED_NOT_EXECUTED"
_CAPTURE_SCOPE = "exact_operator_text_record_for_future_exact_beo_run_package_only"
_RECONCILED_STATE = "exact_operator_text_recorded_no_run_executed"
_CANONICAL_CAPTURE_264_HASH = "sha256:cdf22534b46214ebf8b57a580c183536f289e15a1e482d7726638e0628237399"
_CANONICAL_RECONCILIATION_265_HASH = "sha256:c20f5a0a39383fbfdd811d15aab4f56fae7973d2ddf4f22d9e6b3337c7ca9b21"

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_PUBLICATION_APPROVAL",
    "APPROVAL_REUSE_OR_RETARGETING",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "AUTHORITATIVE_BEO_PUBLICATION_FINALITY",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_STORAGE_LEDGER_RUN_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
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

_SIDE_EFFECTS_AFTER_CAPTURE = {
    "operator_approval_captured": True,
    "approval_reused": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "authoritative_beo_publication_finalized": False,
    "beo_published": False,
    "beo_closeout_execution": False,
    "cryptographic_signature_generated": False,
    "immutable_storage_written": False,
    "public_ledger_appended": False,
    "signer_storage_ledger_reuse": False,
    "rollback_revocation_supersession_execution": False,
    "rtm_generation": False,
    "production_blk_link_execution": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "protected_body_read_copy_parse_hash_scan_mutation": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "beb_dispatch": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_ALLOWED_CAPTURE_KEYS = {
    "sprint", "status", "markers", "contract_hash", "approval_reconciliation_hash", "selection_hash",
    "operator_identity", "operator_text_hash", "captured_at", "capture_scope", "denied_authorities",
    "side_effects", "approval_capture_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "approval_capture_hash", "reconciled_state", "next_frontier",
    "denied_authorities", "side_effects", "reconciliation_hash",
}


def capture_exact_beo_publication_operator_approval_264(
    contract_package: dict[str, Any],
    approval_reconciliation_260: dict[str, Any],
    selection_package_263: dict[str, Any],
    *,
    operator_text: str,
    operator_identity: str,
    captured_at: str,
) -> dict[str, Any]:
    """Capture exact operator text without executing publication or reserving a run."""

    try:
        _validate_258_contract(contract_package)
        _validate_260_reconciliation(approval_reconciliation_260)
        _validate_selection_263(selection_package_263)
    except ValueError as exc:
        raise ExactBeoPublicationApprovalCaptureValidationError(str(exc)) from exc

    if operator_text != EXACT_OPERATOR_APPROVAL_TEXT_258:
        _reject_freeform_laundering(operator_text, "operator_text")
        raise ExactBeoPublicationApprovalCaptureValidationError("operator_text must match exact operator approval text")
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise ExactBeoPublicationApprovalCaptureValidationError("operator_identity mismatch for BLK-SYSTEM-264")
    _require_timezone_timestamp(captured_at)

    package = {
        "sprint": "BLK-SYSTEM-264",
        "status": "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED_NO_RUN",
        "markers": [
            "BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED",
            "NO_RUN_ID_RESERVED_OR_CONSUMED",
            "NO_SIGNER_STORAGE_LEDGER_RUN",
        ],
        "contract_hash": contract_package["contract_hash"],
        "approval_reconciliation_hash": approval_reconciliation_260["reconciliation_hash"],
        "selection_hash": selection_package_263["selection_hash"],
        "operator_identity": operator_identity,
        "operator_text_hash": _hash_text(operator_text),
        "captured_at": captured_at,
        "capture_scope": _CAPTURE_SCOPE,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_AFTER_CAPTURE),
    }
    package["approval_capture_hash"] = _hash_package(package)
    _validate_capture_264(package)
    return _deepcopy(package)


def reconcile_exact_beo_publication_approval_capture_265(capture_package: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the captured approval text into the next run-package frontier."""

    _validate_capture_264(capture_package)
    package = {
        "sprint": "BLK-SYSTEM-265",
        "status": "EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED_RUN_NOT_EXECUTED",
        "markers": [
            "BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED",
            _NEXT_FRONTIER,
            "NO_BEO_PUBLICATION_FINALITY",
        ],
        "approval_capture_hash": capture_package["approval_capture_hash"],
        "reconciled_state": _RECONCILED_STATE,
        "next_frontier": _NEXT_FRONTIER,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_AFTER_CAPTURE),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_265(package, capture_package["approval_capture_hash"])
    return _deepcopy(package)


def _validate_capture_264(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_CAPTURE_KEYS, "capture package")
    _require_status(package, "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED_NO_RUN", "capture package")
    _require_markers(package, [
        "BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED",
        "NO_RUN_ID_RESERVED_OR_CONSUMED",
        "NO_SIGNER_STORAGE_LEDGER_RUN",
    ], "capture package")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package operator_identity mismatch")
    if package.get("operator_text_hash") != EXACT_OPERATOR_APPROVAL_TEXT_HASH_264:
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package operator_text_hash mismatch")
    _require_timezone_timestamp(package.get("captured_at"))
    if package.get("capture_scope") != _CAPTURE_SCOPE:
        _reject_freeform_laundering(package.get("capture_scope"), "capture package capture_scope")
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package capture_scope mismatch")
    _require_denials(package, "capture package")
    _require_side_effects_after_capture(package, "capture package")
    _require_hash(package, "contract_hash", "capture package")
    _require_hash(package, "approval_reconciliation_hash", "capture package")
    _require_hash(package, "selection_hash", "capture package")
    if package.get("selection_hash") != EXPECTED_SELECTION_HASH_263:
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package canonical BLK-SYSTEM-263 selection_hash mismatch")
    _require_hash(package, "approval_capture_hash", "capture package")
    if package.get("approval_capture_hash") != _hash_package({k: v for k, v in package.items() if k != "approval_capture_hash"}):
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package approval_capture_hash mismatch")
    if _CANONICAL_CAPTURE_264_HASH and package.get("approval_capture_hash") != _CANONICAL_CAPTURE_264_HASH:
        raise ExactBeoPublicationApprovalCaptureValidationError("capture package canonical BLK-SYSTEM-264 hash mismatch")
    _reject_freeform_laundering(package, "capture package")


def _validate_reconciliation_265(package: dict[str, Any], expected_capture_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "reconciliation package")
    _require_status(package, "EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED_RUN_NOT_EXECUTED", "reconciliation package")
    _require_markers(package, [
        "BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED",
        _NEXT_FRONTIER,
        "NO_BEO_PUBLICATION_FINALITY",
    ], "reconciliation package")
    if expected_capture_hash is not None and package.get("approval_capture_hash") != expected_capture_hash:
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package approval_capture_hash mismatch")
    if package.get("reconciled_state") != _RECONCILED_STATE:
        _reject_freeform_laundering(package.get("reconciled_state"), "reconciliation package reconciled_state")
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package reconciled_state mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package next_frontier mismatch")
    _require_denials(package, "reconciliation package")
    _require_side_effects_after_capture(package, "reconciliation package")
    _require_hash(package, "approval_capture_hash", "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    if package.get("reconciliation_hash") != _hash_package({k: v for k, v in package.items() if k != "reconciliation_hash"}):
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_CAPTURE_264_HASH and package.get("approval_capture_hash") != _CANONICAL_CAPTURE_264_HASH:
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package canonical BLK-SYSTEM-264 hash mismatch")
    if _CANONICAL_RECONCILIATION_265_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_265_HASH:
        raise ExactBeoPublicationApprovalCaptureValidationError("reconciliation package canonical BLK-SYSTEM-265 hash mismatch")
    _reject_freeform_laundering(package, "reconciliation package")


def _require_allowed_keys(package: Any, allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} must be a dictionary")
    extras = sorted(set(package) - allowed)
    missing = sorted(allowed - set(package))
    if extras:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} unsupported field {extras[0]!r}")
    if missing:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} missing field {missing[0]!r}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} markers mismatch")


def _require_denials(package: dict[str, Any], label: str) -> None:
    denials = package.get("denied_authorities")
    if not isinstance(denials, list):
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} denied_authorities must be a list")
    if denials != _DENIED_AUTHORITIES or len(denials) != len(set(denials)):
        _reject_freeform_laundering(denials, f"{label} denied_authorities")
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects_after_capture(package: dict[str, Any], label: str) -> None:
    if package.get("side_effects") != _SIDE_EFFECTS_AFTER_CAPTURE:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} side_effects mismatch")


def _require_timezone_timestamp(value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise ExactBeoPublicationApprovalCaptureValidationError("captured_at must be a timezone-aware ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ExactBeoPublicationApprovalCaptureValidationError("captured_at must be a timezone-aware ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExactBeoPublicationApprovalCaptureValidationError("captured_at must be timezone-aware")


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} {key} must be canonical sha256")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        raise ExactBeoPublicationApprovalCaptureValidationError(f"{label} forbidden authority wording: {findings[0]}")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(ch in "0123456789abcdef" for ch in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
