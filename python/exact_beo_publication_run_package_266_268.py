"""BLK-SYSTEM-266..268 exact BEO publication run-package preparation.

This package consumes the BLK-SYSTEM-264..265 exact operator-text capture evidence
and prepares the next exact BEO publication run package without executing BEO
publication finality, reserving/consuming a run ID, signing, writing immutable
storage, appending a ledger, generating RTM, running production blk-link, reading
protected bodies, invoking runtime/tooling, or mutating target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from exact_beo_publication_approval_capture_264_265 import (
    EXPECTED_OPERATOR_IDENTITY_264,
    EXACT_OPERATOR_APPROVAL_TEXT_HASH_264,
    _CANONICAL_CAPTURE_264_HASH,
    _CANONICAL_RECONCILIATION_265_HASH,
    _validate_capture_264,
    _validate_reconciliation_265,
)


class ExactBeoPublicationRunPackageValidationError(ValueError):
    """Raised when BLK-SYSTEM-266..268 run-package evidence is unsafe."""


EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266 = (
    "APPROVE BLK-SYSTEM-266 EXACT BEO PUBLICATION RUN PACKAGE PREFLIGHT ONLY; "
    "NO RUN ID RESERVATION OR CONSUMPTION; NO SIGNER STORAGE LEDGER RUN; "
    "NO RTM; NO PRODUCTION BLK-LINK; NO PROTECTED BODY."
)
EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266 = "sha256:" + hashlib.sha256(
    EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266.encode("utf-8")
).hexdigest()

_NEXT_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_REQUIRED_NOT_GRANTED"
_RUN_PACKAGE_SCOPE = "prepare_exact_beo_publication_run_package_without_execution_or_run_id"
_GENERIC_BLOCKED_RESULT = "generic_package_directive_is_not_exact_beo_publication_run_approval"
_EXACT_TEXT_SEEN_RESULT = "exact_run_text_seen_but_preparation_package_does_not_execute_publication_finality"
_RECONCILED_STATE = "exact_beo_publication_run_package_prepared_execution_not_granted"

_CANONICAL_RUN_PACKAGE_266_HASH: str | None = "sha256:7815590afd45c9ab978e6bcfffa09446b870e9c17d66688c31c5ca36905e4a23"
_CANONICAL_PREFLIGHT_267_HASH: str | None = "sha256:9ed5a7ee1139be7d48df8d2a6baaee10a8a24a7bdbd7abc469b062e5b95b2e5c"
_CANONICAL_RECONCILIATION_268_HASH: str | None = "sha256:e1602b1abd0c96badb12efca01e794f48da06e6d69ab1b3d8e86b27f0e882172"

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_PUBLICATION_OR_RUN_APPROVAL",
    "APPROVAL_REUSE_OR_RETARGETING",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "AUTHORITATIVE_BEO_PUBLICATION_FINALITY",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_STORAGE_LEDGER_RUN_OR_REUSE",
    "SIGNATURE_RECEIPT_CREATION",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND",
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

_SIDE_EFFECTS_266 = {
    "operator_approval_captured": True,
    "run_package_prepared": True,
    "run_preflight_recorded": False,
    "approval_reused": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "authoritative_beo_publication_finalized": False,
    "beo_published": False,
    "beo_closeout_execution": False,
    "cryptographic_signature_generated": False,
    "signature_receipt_recorded": False,
    "immutable_storage_written": False,
    "immutable_storage_receipt_recorded": False,
    "public_ledger_appended": False,
    "public_ledger_receipt_recorded": False,
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
_SIDE_EFFECTS_267_268 = dict(_SIDE_EFFECTS_266)
_SIDE_EFFECTS_267_268["run_preflight_recorded"] = True

_ALLOWED_RUN_PACKAGE_KEYS = {
    "sprint", "status", "markers", "approval_capture_hash", "approval_capture_reconciliation_hash",
    "operator_identity", "operator_text_hash", "requested_at", "expires_at", "execution_request_hash",
    "run_package_scope", "required_exact_run_approval_text", "required_exact_run_approval_text_hash",
    "denied_authorities", "side_effects", "run_package_hash",
}
_ALLOWED_PREFLIGHT_KEYS = {
    "sprint", "status", "markers", "run_package_hash", "operator_text_status", "operator_text_hash",
    "evaluated_at", "evaluation_result", "denied_authorities", "side_effects", "preflight_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "preflight_hash", "reconciled_state", "next_frontier",
    "denied_authorities", "side_effects", "reconciliation_hash",
}


def build_exact_beo_publication_run_package_266(
    capture_package_264: dict[str, Any],
    reconciliation_package_265: dict[str, Any],
    *,
    operator_identity: str,
    requested_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Prepare the exact BEO publication run package without executing it."""

    try:
        _validate_capture_264(capture_package_264)
        _validate_reconciliation_265(reconciliation_package_265, capture_package_264["approval_capture_hash"])
    except ValueError as exc:
        raise ExactBeoPublicationRunPackageValidationError(str(exc)) from exc

    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise ExactBeoPublicationRunPackageValidationError("operator_identity mismatch for BLK-SYSTEM-266")
    _require_window(requested_at, expires_at)

    execution_request_hash = _hash_package({
        "approval_capture_hash": capture_package_264["approval_capture_hash"],
        "approval_capture_reconciliation_hash": reconciliation_package_265["reconciliation_hash"],
        "operator_identity": operator_identity,
        "operator_text_hash": capture_package_264["operator_text_hash"],
        "requested_at": requested_at,
        "expires_at": expires_at,
        "required_exact_run_approval_text_hash": EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266,
        "run_package_scope": _RUN_PACKAGE_SCOPE,
    })
    package = {
        "sprint": "BLK-SYSTEM-266",
        "status": "EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY_NOT_EXECUTED",
        "markers": [
            "BLK_SYSTEM_266_EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY",
            "NO_RUN_ID_RESERVED_OR_CONSUMED",
            "NO_SIGNER_STORAGE_LEDGER_RUN",
        ],
        "approval_capture_hash": capture_package_264["approval_capture_hash"],
        "approval_capture_reconciliation_hash": reconciliation_package_265["reconciliation_hash"],
        "operator_identity": operator_identity,
        "operator_text_hash": capture_package_264["operator_text_hash"],
        "requested_at": requested_at,
        "expires_at": expires_at,
        "execution_request_hash": execution_request_hash,
        "run_package_scope": _RUN_PACKAGE_SCOPE,
        "required_exact_run_approval_text": EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266,
        "required_exact_run_approval_text_hash": EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_266),
    }
    package["run_package_hash"] = _hash_package(package)
    _validate_run_package_266(package)
    return _deepcopy(package)


def evaluate_exact_beo_publication_run_package_preflight_267(
    run_package_266: dict[str, Any],
    *,
    operator_text: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Record preflight status for the prepared run package without execution."""

    _validate_run_package_266(run_package_266)
    if not isinstance(operator_text, str) or not operator_text.strip():
        raise ExactBeoPublicationRunPackageValidationError("operator_text must be a non-empty string")
    _require_timezone_timestamp(evaluated_at, "evaluated_at")

    if operator_text != EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266:
        _reject_freeform_laundering(operator_text, "operator_text")
        status = "BLOCKED_BY_MISSING_EXACT_BEO_PUBLICATION_RUN_APPROVAL"
        text_status = "NOT_EXACT_RUN_APPROVAL_TEXT"
        result = _GENERIC_BLOCKED_RESULT
        marker = "BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_BLOCKED"
    else:
        status = "EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_MATCHED_EXECUTION_NOT_PERFORMED"
        text_status = "EXACT_RUN_APPROVAL_TEXT_MATCHED"
        result = _EXACT_TEXT_SEEN_RESULT
        marker = "BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_EXACT_TEXT_SEEN_NO_EXECUTION"

    package = {
        "sprint": "BLK-SYSTEM-267",
        "status": status,
        "markers": [
            marker,
            "NO_RUN_ID_RESERVED_OR_CONSUMED",
            "NO_BEO_PUBLICATION_FINALITY",
        ],
        "run_package_hash": run_package_266["run_package_hash"],
        "operator_text_status": text_status,
        "operator_text_hash": _hash_text(operator_text),
        "evaluated_at": evaluated_at,
        "evaluation_result": result,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_267_268),
    }
    package["preflight_hash"] = _hash_package(package)
    _validate_preflight_267(package, run_package_266["run_package_hash"])
    return _deepcopy(package)


def reconcile_exact_beo_publication_run_package_268(preflight_package_267: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the prepared run package into the next exact execution-approval frontier."""

    _validate_preflight_267(preflight_package_267)
    package = {
        "sprint": "BLK-SYSTEM-268",
        "status": "EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED_EXECUTION_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_268_EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED",
            _NEXT_FRONTIER,
            "NO_BEO_PUBLICATION_FINALITY",
        ],
        "preflight_hash": preflight_package_267["preflight_hash"],
        "reconciled_state": _RECONCILED_STATE,
        "next_frontier": _NEXT_FRONTIER,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_267_268),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_268(package, preflight_package_267["preflight_hash"])
    return _deepcopy(package)


def _validate_run_package_266(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_RUN_PACKAGE_KEYS, "run package")
    _require_status(package, "EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY_NOT_EXECUTED", "run package")
    _require_markers(package, [
        "BLK_SYSTEM_266_EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY",
        "NO_RUN_ID_RESERVED_OR_CONSUMED",
        "NO_SIGNER_STORAGE_LEDGER_RUN",
    ], "run package")
    if package.get("approval_capture_hash") != _CANONICAL_CAPTURE_264_HASH:
        raise ExactBeoPublicationRunPackageValidationError("run package canonical BLK-SYSTEM-264 hash mismatch")
    if package.get("approval_capture_reconciliation_hash") != _CANONICAL_RECONCILIATION_265_HASH:
        raise ExactBeoPublicationRunPackageValidationError("run package canonical BLK-SYSTEM-265 hash mismatch")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise ExactBeoPublicationRunPackageValidationError("run package operator_identity mismatch")
    if package.get("operator_text_hash") != EXACT_OPERATOR_APPROVAL_TEXT_HASH_264:
        raise ExactBeoPublicationRunPackageValidationError("run package operator_text_hash mismatch")
    _require_window(package.get("requested_at"), package.get("expires_at"))
    if package.get("run_package_scope") != _RUN_PACKAGE_SCOPE:
        _reject_freeform_laundering(package.get("run_package_scope"), "run package scope")
        raise ExactBeoPublicationRunPackageValidationError("run package scope mismatch")
    if package.get("required_exact_run_approval_text") != EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266:
        _reject_freeform_laundering(package.get("required_exact_run_approval_text"), "run package required text")
        raise ExactBeoPublicationRunPackageValidationError("run package required exact approval text mismatch")
    if package.get("required_exact_run_approval_text_hash") != EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266:
        raise ExactBeoPublicationRunPackageValidationError("run package required exact approval text hash mismatch")
    expected_execution_request_hash = _hash_package({
        "approval_capture_hash": package["approval_capture_hash"],
        "approval_capture_reconciliation_hash": package["approval_capture_reconciliation_hash"],
        "operator_identity": package["operator_identity"],
        "operator_text_hash": package["operator_text_hash"],
        "requested_at": package["requested_at"],
        "expires_at": package["expires_at"],
        "required_exact_run_approval_text_hash": package["required_exact_run_approval_text_hash"],
        "run_package_scope": package["run_package_scope"],
    })
    if package.get("execution_request_hash") != expected_execution_request_hash:
        raise ExactBeoPublicationRunPackageValidationError("run package execution_request_hash mismatch")
    _require_denials(package, "run package")
    _require_side_effects(package, _SIDE_EFFECTS_266, "run package")
    _require_hash(package, "run_package_hash", "run package")
    if package.get("run_package_hash") != _hash_package({k: v for k, v in package.items() if k != "run_package_hash"}):
        raise ExactBeoPublicationRunPackageValidationError("run package run_package_hash mismatch")
    if _CANONICAL_RUN_PACKAGE_266_HASH and package.get("run_package_hash") != _CANONICAL_RUN_PACKAGE_266_HASH:
        raise ExactBeoPublicationRunPackageValidationError("run package canonical BLK-SYSTEM-266 hash mismatch")
    _reject_freeform_laundering(package, "run package")


def _validate_preflight_267(package: dict[str, Any], expected_run_package_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_PREFLIGHT_KEYS, "preflight package")
    if package.get("status") not in {
        "BLOCKED_BY_MISSING_EXACT_BEO_PUBLICATION_RUN_APPROVAL",
        "EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_MATCHED_EXECUTION_NOT_PERFORMED",
    }:
        raise ExactBeoPublicationRunPackageValidationError("preflight package status mismatch")
    if package.get("status") == "BLOCKED_BY_MISSING_EXACT_BEO_PUBLICATION_RUN_APPROVAL":
        expected_markers = [
            "BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_BLOCKED",
            "NO_RUN_ID_RESERVED_OR_CONSUMED",
            "NO_BEO_PUBLICATION_FINALITY",
        ]
        expected_text_status = "NOT_EXACT_RUN_APPROVAL_TEXT"
        expected_result = _GENERIC_BLOCKED_RESULT
    else:
        expected_markers = [
            "BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_EXACT_TEXT_SEEN_NO_EXECUTION",
            "NO_RUN_ID_RESERVED_OR_CONSUMED",
            "NO_BEO_PUBLICATION_FINALITY",
        ]
        expected_text_status = "EXACT_RUN_APPROVAL_TEXT_MATCHED"
        expected_result = _EXACT_TEXT_SEEN_RESULT
        if package.get("operator_text_hash") != EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266:
            raise ExactBeoPublicationRunPackageValidationError("preflight package exact operator_text_hash mismatch")
    _require_markers(package, expected_markers, "preflight package")
    if package.get("operator_text_status") != expected_text_status:
        raise ExactBeoPublicationRunPackageValidationError("preflight package operator_text_status mismatch")
    if package.get("evaluation_result") != expected_result:
        _reject_freeform_laundering(package.get("evaluation_result"), "preflight package evaluation_result")
        raise ExactBeoPublicationRunPackageValidationError("preflight package evaluation_result mismatch")
    if expected_run_package_hash is not None and package.get("run_package_hash") != expected_run_package_hash:
        raise ExactBeoPublicationRunPackageValidationError("preflight package run_package_hash mismatch")
    if _CANONICAL_RUN_PACKAGE_266_HASH and package.get("run_package_hash") != _CANONICAL_RUN_PACKAGE_266_HASH:
        raise ExactBeoPublicationRunPackageValidationError("preflight package canonical BLK-SYSTEM-266 hash mismatch")
    _require_timezone_timestamp(package.get("evaluated_at"), "evaluated_at")
    _require_denials(package, "preflight package")
    _require_side_effects(package, _SIDE_EFFECTS_267_268, "preflight package")
    _require_hash(package, "run_package_hash", "preflight package")
    _require_hash(package, "operator_text_hash", "preflight package")
    _require_hash(package, "preflight_hash", "preflight package")
    if package.get("preflight_hash") != _hash_package({k: v for k, v in package.items() if k != "preflight_hash"}):
        raise ExactBeoPublicationRunPackageValidationError("preflight package preflight_hash mismatch")
    if (
        package.get("status") == "BLOCKED_BY_MISSING_EXACT_BEO_PUBLICATION_RUN_APPROVAL"
        and _CANONICAL_PREFLIGHT_267_HASH
        and package.get("preflight_hash") != _CANONICAL_PREFLIGHT_267_HASH
    ):
        raise ExactBeoPublicationRunPackageValidationError("preflight package canonical BLK-SYSTEM-267 hash mismatch")
    _reject_freeform_laundering(package, "preflight package")


def _validate_reconciliation_268(package: dict[str, Any], expected_preflight_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "reconciliation package")
    _require_status(package, "EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED_EXECUTION_NOT_GRANTED", "reconciliation package")
    _require_markers(package, [
        "BLK_SYSTEM_268_EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED",
        _NEXT_FRONTIER,
        "NO_BEO_PUBLICATION_FINALITY",
    ], "reconciliation package")
    if expected_preflight_hash is not None and package.get("preflight_hash") != expected_preflight_hash:
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package preflight_hash mismatch")
    if _CANONICAL_PREFLIGHT_267_HASH and package.get("preflight_hash") != _CANONICAL_PREFLIGHT_267_HASH:
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package canonical BLK-SYSTEM-267 hash mismatch")
    if package.get("reconciled_state") != _RECONCILED_STATE:
        _reject_freeform_laundering(package.get("reconciled_state"), "reconciliation package reconciled_state")
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package reconciled_state mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package next_frontier mismatch")
    _require_denials(package, "reconciliation package")
    _require_side_effects(package, _SIDE_EFFECTS_267_268, "reconciliation package")
    _require_hash(package, "preflight_hash", "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    if package.get("reconciliation_hash") != _hash_package({k: v for k, v in package.items() if k != "reconciliation_hash"}):
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_RECONCILIATION_268_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_268_HASH:
        raise ExactBeoPublicationRunPackageValidationError("reconciliation package canonical BLK-SYSTEM-268 hash mismatch")
    _reject_freeform_laundering(package, "reconciliation package")


def _require_allowed_keys(package: Any, allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise ExactBeoPublicationRunPackageValidationError(f"{label} must be a dictionary")
    extras = sorted(set(package) - allowed)
    missing = sorted(allowed - set(package))
    if extras:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} unsupported field {extras[0]!r}")
    if missing:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} missing field {missing[0]!r}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} markers mismatch")


def _require_denials(package: dict[str, Any], label: str) -> None:
    denials = package.get("denied_authorities")
    if not isinstance(denials, list):
        raise ExactBeoPublicationRunPackageValidationError(f"{label} denied_authorities must be a list")
    if denials != _DENIED_AUTHORITIES or len(denials) != len(set(denials)):
        _reject_freeform_laundering(denials, f"{label} denied_authorities")
        raise ExactBeoPublicationRunPackageValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], label: str) -> None:
    if package.get("side_effects") != expected:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} side_effects mismatch")


def _require_window(requested_at: Any, expires_at: Any) -> None:
    requested = _parse_timezone_timestamp(requested_at, "requested_at")
    expires = _parse_timezone_timestamp(expires_at, "expires_at")
    if expires <= requested:
        raise ExactBeoPublicationRunPackageValidationError("expires_at must be after requested_at")


def _require_timezone_timestamp(value: Any, label: str) -> None:
    _parse_timezone_timestamp(value, label)


def _parse_timezone_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} must be a timezone-aware ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} must be a timezone-aware ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} must be timezone-aware")
    return parsed


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise ExactBeoPublicationRunPackageValidationError(f"{label} {key} must be canonical sha256")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        raise ExactBeoPublicationRunPackageValidationError(f"{label} forbidden authority wording: {findings[0]}")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(ch in "0123456789abcdef" for ch in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
