"""BLK-SYSTEM-257..260 exact BEO publication approval ladder.

The active BLK-SYSTEM-256 frontier says RTM / production ``blk-link`` drift and
coverage must stay blocked until exact authoritative BEO publication evidence
exists. This ladder scopes the next bounded movement without treating a generic
"execute next sprints" directive as publication approval.

It consumes the reusable BEO publication review reconciliation (BLK-SYSTEM-251)
and the drift/coverage reconciliation (BLK-SYSTEM-256), emits an exact approval
contract, evaluates the current operator text, and reconciles the frontier as
still not granted when the exact publication approval text is missing.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from rtm_blk_link_drift_coverage_ladder_252_256 import (
    _validate_beo_251 as _validate_upstream_beo_251,
    _validate_256_reconciliation as _validate_upstream_drift_256,
)


class ExactBeoPublicationApprovalValidationError(ValueError):
    """Raised when exact BEO publication approval evidence is unsafe."""


_EXPECTED_BEO_251_RECONCILIATION_HASH = "sha256:4e2acbff751aae66dda868d1e4e06c56b0f210b624a2affa7e4c658bda25dddd"
_EXPECTED_DRIFT_256_RECONCILIATION_HASH = "sha256:de39b2ece921871e31c6c7892d1fbbd971c15ec68f2db6dd67c3d7c7db1f4e5f"
_EXPECTED_OLD_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED"
_NEXT_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED"
_CANONICAL_REQUEST_257_HASH = "sha256:a406ef82b236d5cabbd0aede735ee2d9149f6d1b80245ca335496dfb5d8ce218"
_CANONICAL_CONTRACT_258_HASH = "sha256:b8e47c5343bfd73e2db4d1b6eabcc474c2140080339cd98c857356024b2e9581"
_CANONICAL_PREFLIGHT_259_HASH = "sha256:09df68a4bd7dae47deb4001a7c7dcb0870b6b084fc20c1eb822e6939e02d58f2"
_CANONICAL_RECONCILIATION_260_HASH = "sha256:e66022d4906aeb4749407a6c0557c66813f099d2ebec37f87ef2c51a784317a9"
_GENERIC_OPERATOR_DIRECTIVE_HASH = "sha256:4ee4a961ddd80211744db26350b60dc6c244f9ecab9de652ea59c39bb88a766e"
_REQUEST_SCOPE = "request exact operator approval text before any BEO publication finality package can be built"
_GENERIC_BLOCKED_RESULT = "generic_or_non_exact_operator_text_does_not_capture_publication_approval"
_EXACT_TEXT_SEEN_RESULT = "exact_text_seen_but_this_sprint_records_preflight_only_and_requires_separate_capture"
_RECONCILED_STATE = "exact_beo_publication_request_and_contract_ready_but_approval_capture_and_run_not_granted"

EXACT_OPERATOR_APPROVAL_TEXT_258 = (
    "APPROVE BLK-SYSTEM-258 EXACT BEO PUBLICATION APPROVAL PREFLIGHT ONLY; "
    "NO SIGNER STORAGE LEDGER RUN; NO RTM; NO PRODUCTION BLK-LINK; NO PROTECTED BODY."
)

_SIDE_EFFECTS = {
    "operator_approval_captured": False,
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

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_PUBLICATION_APPROVAL",
    "OPERATOR_APPROVAL_CAPTURE",
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

_APPROVAL_RULES = {
    "exact_text_required": True,
    "generic_next_sprints_directive_is_not_publication_approval": True,
    "approval_capture_not_performed_by_this_ladder": True,
    "run_id_not_reserved_or_consumed": True,
    "signer_storage_ledger_run_not_performed": True,
    "rtm_and_production_blk_link_remain_blocked": True,
}

_ALLOWED_KEYS_257 = {
    "sprint", "status", "markers", "beo_reconciliation_hash", "drift_coverage_reconciliation_hash",
    "request_scope", "required_exact_operator_approval_text", "approval_rules", "denied_authorities",
    "side_effects", "request_hash",
}
_ALLOWED_KEYS_258 = {
    "sprint", "status", "markers", "request_hash", "exact_operator_approval_text", "approval_rules",
    "denied_authorities", "side_effects", "contract_hash",
}
_ALLOWED_KEYS_259 = {
    "sprint", "status", "markers", "contract_hash", "operator_text_status", "operator_text_hash",
    "evaluation_result", "denied_authorities", "side_effects", "preflight_hash",
}
_ALLOWED_KEYS_260 = {
    "sprint", "status", "markers", "preflight_hash", "reconciled_state", "next_frontier",
    "denied_authorities", "side_effects", "reconciliation_hash",
}


def build_exact_beo_publication_run_request_257(beo_reconciliation: dict[str, Any], drift_reconciliation: dict[str, Any]) -> dict[str, Any]:
    _validate_beo_reconciliation(beo_reconciliation)
    _validate_drift_reconciliation(drift_reconciliation)
    package = {
        "sprint": "BLK-SYSTEM-257",
        "status": "EXACT_BEO_PUBLICATION_RUN_REQUEST_READY_NOT_APPROVED",
        "markers": [
            "BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY",
            "GENERIC_OPERATOR_DIRECTIVE_NOT_PUBLICATION_APPROVAL",
            "NO_SIGNER_STORAGE_LEDGER_RUN",
        ],
        "beo_reconciliation_hash": beo_reconciliation["reconciliation_hash"],
        "drift_coverage_reconciliation_hash": drift_reconciliation["reconciliation_hash"],
        "request_scope": _REQUEST_SCOPE,
        "required_exact_operator_approval_text": EXACT_OPERATOR_APPROVAL_TEXT_258,
        "approval_rules": dict(_APPROVAL_RULES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["request_hash"] = _hash_package(package)
    _validate_257_request(package)
    return _deepcopy(package)


def build_exact_beo_publication_operator_approval_contract_258(request_package: dict[str, Any]) -> dict[str, Any]:
    _validate_257_request(request_package)
    package = {
        "sprint": "BLK-SYSTEM-258",
        "status": "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY",
        "markers": [
            "BLK_SYSTEM_258_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY",
            "EXACT_APPROVAL_TEXT_REQUIRED",
            "APPROVAL_CAPTURE_NOT_PERFORMED",
        ],
        "request_hash": request_package["request_hash"],
        "exact_operator_approval_text": EXACT_OPERATOR_APPROVAL_TEXT_258,
        "approval_rules": dict(_APPROVAL_RULES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["contract_hash"] = _hash_package(package)
    _validate_258_contract(package, request_package["request_hash"])
    return _deepcopy(package)


def evaluate_exact_beo_publication_operator_approval_259(contract_package: dict[str, Any], operator_text: str) -> dict[str, Any]:
    _validate_258_contract(contract_package)
    if not isinstance(operator_text, str) or not operator_text.strip():
        raise ExactBeoPublicationApprovalValidationError("operator_text must be a non-empty string")
    if operator_text != EXACT_OPERATOR_APPROVAL_TEXT_258:
        _reject_freeform_laundering(operator_text, "operator_text")
        text_status = "NOT_EXACT_APPROVAL_TEXT"
        status = "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL"
        result = _GENERIC_BLOCKED_RESULT
    else:
        text_status = "EXACT_TEXT_MATCHED_BUT_CAPTURE_NOT_PERFORMED"
        status = "EXACT_OPERATOR_APPROVAL_TEXT_MATCHED_NOT_CAPTURED"
        result = _EXACT_TEXT_SEEN_RESULT
    package = {
        "sprint": "BLK-SYSTEM-259",
        "status": status,
        "markers": [
            "BLK_SYSTEM_259_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_PREFLIGHT_RECORDED",
            "NO_APPROVAL_CAPTURE_OR_RUN_ID_CONSUMPTION",
            "NO_BEO_PUBLICATION_FINALITY",
        ],
        "contract_hash": contract_package["contract_hash"],
        "operator_text_status": text_status,
        "operator_text_hash": _hash_text(operator_text),
        "evaluation_result": result,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["preflight_hash"] = _hash_package(package)
    _validate_259_preflight(package, contract_package["contract_hash"])
    return _deepcopy(package)


def reconcile_exact_beo_publication_approval_frontier_260(preflight_package: dict[str, Any]) -> dict[str, Any]:
    _validate_259_preflight(preflight_package)
    package = {
        "sprint": "BLK-SYSTEM-260",
        "status": "EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED",
            "EXACT_OPERATOR_APPROVAL_TEXT_REQUIRED_BEFORE_PUBLICATION_RUN",
            _NEXT_FRONTIER,
        ],
        "preflight_hash": preflight_package["preflight_hash"],
        "reconciled_state": _RECONCILED_STATE,
        "next_frontier": _NEXT_FRONTIER,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_260_reconciliation(package, preflight_package["preflight_hash"])
    return _deepcopy(package)


def _validate_beo_reconciliation(package: dict[str, Any]) -> None:
    try:
        _validate_upstream_beo_251(package)
    except ValueError as exc:
        raise ExactBeoPublicationApprovalValidationError(f"BEO 251 upstream validation failed: {exc}") from exc
    if package.get("reconciliation_hash") != _EXPECTED_BEO_251_RECONCILIATION_HASH:
        raise ExactBeoPublicationApprovalValidationError("BEO 251 reconciliation_hash mismatch")
    _reject_freeform_laundering(package, "BEO 251 reconciliation")


def _validate_drift_reconciliation(package: dict[str, Any]) -> None:
    try:
        _validate_upstream_drift_256(package)
    except ValueError as exc:
        raise ExactBeoPublicationApprovalValidationError(f"drift 256 upstream validation failed: {exc}") from exc
    if package.get("reconciliation_hash") != _EXPECTED_DRIFT_256_RECONCILIATION_HASH:
        raise ExactBeoPublicationApprovalValidationError("drift 256 reconciliation_hash mismatch")
    if package.get("next_frontier") != _EXPECTED_OLD_FRONTIER:
        raise ExactBeoPublicationApprovalValidationError("drift 256 next_frontier mismatch")
    _reject_freeform_laundering(package, "drift 256 reconciliation")


def _validate_257_request(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_257, "request package")
    _require_status(package, "EXACT_BEO_PUBLICATION_RUN_REQUEST_READY_NOT_APPROVED", "request package")
    _require_markers(package, [
        "BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY",
        "GENERIC_OPERATOR_DIRECTIVE_NOT_PUBLICATION_APPROVAL",
        "NO_SIGNER_STORAGE_LEDGER_RUN",
    ], "request package")
    if package.get("beo_reconciliation_hash") != _EXPECTED_BEO_251_RECONCILIATION_HASH:
        raise ExactBeoPublicationApprovalValidationError("request package BEO reconciliation_hash mismatch")
    if package.get("drift_coverage_reconciliation_hash") != _EXPECTED_DRIFT_256_RECONCILIATION_HASH:
        raise ExactBeoPublicationApprovalValidationError("request package drift reconciliation_hash mismatch")
    if package.get("required_exact_operator_approval_text") != EXACT_OPERATOR_APPROVAL_TEXT_258:
        raise ExactBeoPublicationApprovalValidationError("request package exact approval text mismatch")
    _require_approval_rules(package, "request package")
    _require_denials(package, "request package")
    _require_side_effects(package, "request package")
    _require_hash(package, "request_hash", "request package")
    if _hash_package({k: v for k, v in package.items() if k != "request_hash"}) != package.get("request_hash"):
        raise ExactBeoPublicationApprovalValidationError("request package request_hash mismatch")
    if package.get("request_hash") != _CANONICAL_REQUEST_257_HASH:
        raise ExactBeoPublicationApprovalValidationError("request package must match canonical BLK-SYSTEM-257 request_hash")
    if package.get("request_scope") != _REQUEST_SCOPE:
        _reject_freeform_laundering(package.get("request_scope"), "request package request_scope")
        raise ExactBeoPublicationApprovalValidationError("request package request_scope mismatch")


def _validate_258_contract(package: dict[str, Any], expected_request_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_258, "contract package")
    _require_status(package, "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY", "contract package")
    _require_markers(package, [
        "BLK_SYSTEM_258_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY",
        "EXACT_APPROVAL_TEXT_REQUIRED",
        "APPROVAL_CAPTURE_NOT_PERFORMED",
    ], "contract package")
    if expected_request_hash and package.get("request_hash") != expected_request_hash:
        raise ExactBeoPublicationApprovalValidationError("contract package request_hash mismatch")
    if package.get("exact_operator_approval_text") != EXACT_OPERATOR_APPROVAL_TEXT_258:
        raise ExactBeoPublicationApprovalValidationError("contract package exact_operator_approval_text mismatch")
    _require_approval_rules(package, "contract package")
    _require_denials(package, "contract package")
    _require_side_effects(package, "contract package")
    _require_hash(package, "contract_hash", "contract package")
    if _hash_package({k: v for k, v in package.items() if k != "contract_hash"}) != package.get("contract_hash"):
        raise ExactBeoPublicationApprovalValidationError("contract package contract_hash mismatch")
    if package.get("request_hash") != _CANONICAL_REQUEST_257_HASH:
        raise ExactBeoPublicationApprovalValidationError("contract package must bind canonical BLK-SYSTEM-257 request_hash")
    if package.get("contract_hash") != _CANONICAL_CONTRACT_258_HASH:
        raise ExactBeoPublicationApprovalValidationError("contract package must match canonical BLK-SYSTEM-258 contract_hash")


def _validate_259_preflight(package: dict[str, Any], expected_contract_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_259, "preflight package")
    if package.get("status") not in {
        "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL",
        "EXACT_OPERATOR_APPROVAL_TEXT_MATCHED_NOT_CAPTURED",
    }:
        raise ExactBeoPublicationApprovalValidationError("preflight package status mismatch")
    _require_markers(package, [
        "BLK_SYSTEM_259_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_PREFLIGHT_RECORDED",
        "NO_APPROVAL_CAPTURE_OR_RUN_ID_CONSUMPTION",
        "NO_BEO_PUBLICATION_FINALITY",
    ], "preflight package")
    if expected_contract_hash and package.get("contract_hash") != expected_contract_hash:
        raise ExactBeoPublicationApprovalValidationError("preflight package contract_hash mismatch")
    if package.get("operator_text_status") not in {"NOT_EXACT_APPROVAL_TEXT", "EXACT_TEXT_MATCHED_BUT_CAPTURE_NOT_PERFORMED"}:
        raise ExactBeoPublicationApprovalValidationError("preflight package operator_text_status mismatch")
    _require_hash(package, "operator_text_hash", "preflight package")
    if package.get("status") == "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL":
        if package.get("operator_text_status") != "NOT_EXACT_APPROVAL_TEXT" or package.get("evaluation_result") != _GENERIC_BLOCKED_RESULT:
            raise ExactBeoPublicationApprovalValidationError("preflight package blocked status correlation mismatch")
    elif package.get("status") == "EXACT_OPERATOR_APPROVAL_TEXT_MATCHED_NOT_CAPTURED":
        if package.get("operator_text_status") != "EXACT_TEXT_MATCHED_BUT_CAPTURE_NOT_PERFORMED" or package.get("operator_text_hash") != _hash_text(EXACT_OPERATOR_APPROVAL_TEXT_258) or package.get("evaluation_result") != _EXACT_TEXT_SEEN_RESULT:
            raise ExactBeoPublicationApprovalValidationError("preflight package exact-text status correlation mismatch")
    _require_denials(package, "preflight package")
    _require_side_effects(package, "preflight package")
    _require_hash(package, "preflight_hash", "preflight package")
    if _hash_package({k: v for k, v in package.items() if k != "preflight_hash"}) != package.get("preflight_hash"):
        raise ExactBeoPublicationApprovalValidationError("preflight package preflight_hash mismatch")
    if package.get("contract_hash") != _CANONICAL_CONTRACT_258_HASH:
        raise ExactBeoPublicationApprovalValidationError("preflight package must bind canonical BLK-SYSTEM-258 contract_hash")
    if package.get("preflight_hash") != _CANONICAL_PREFLIGHT_259_HASH:
        raise ExactBeoPublicationApprovalValidationError("preflight package must match canonical BLK-SYSTEM-259 preflight_hash")
    _reject_freeform_laundering(package.get("evaluation_result"), "preflight package evaluation_result")


def _validate_260_reconciliation(package: dict[str, Any], expected_preflight_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_260, "reconciliation package")
    _require_status(package, "EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED", "reconciliation package")
    _require_markers(package, [
        "BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED",
        "EXACT_OPERATOR_APPROVAL_TEXT_REQUIRED_BEFORE_PUBLICATION_RUN",
        _NEXT_FRONTIER,
    ], "reconciliation package")
    if expected_preflight_hash and package.get("preflight_hash") != expected_preflight_hash:
        raise ExactBeoPublicationApprovalValidationError("reconciliation package preflight_hash mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise ExactBeoPublicationApprovalValidationError("reconciliation package next_frontier mismatch")
    _require_denials(package, "reconciliation package")
    _require_side_effects(package, "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    if _hash_package({k: v for k, v in package.items() if k != "reconciliation_hash"}) != package.get("reconciliation_hash"):
        raise ExactBeoPublicationApprovalValidationError("reconciliation package reconciliation_hash mismatch")
    if package.get("preflight_hash") != _CANONICAL_PREFLIGHT_259_HASH:
        raise ExactBeoPublicationApprovalValidationError("reconciliation package must bind canonical BLK-SYSTEM-259 preflight_hash")
    if package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_260_HASH:
        raise ExactBeoPublicationApprovalValidationError("reconciliation package must match canonical BLK-SYSTEM-260 reconciliation_hash")
    if package.get("reconciled_state") != _RECONCILED_STATE:
        _reject_freeform_laundering(package.get("reconciled_state"), "reconciliation package reconciled_state")
        raise ExactBeoPublicationApprovalValidationError("reconciliation package reconciled_state mismatch")


def _require_allowed_keys(value: Any, allowed: set[str], label: str) -> None:
    if not isinstance(value, dict):
        raise ExactBeoPublicationApprovalValidationError(f"{label} must be a dictionary")
    extras = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if extras:
        raise ExactBeoPublicationApprovalValidationError(f"{label} unsupported field {extras[0]!r}")
    if missing:
        raise ExactBeoPublicationApprovalValidationError(f"{label} missing field {missing[0]!r}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise ExactBeoPublicationApprovalValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise ExactBeoPublicationApprovalValidationError(f"{label} markers mismatch")


def _require_approval_rules(package: dict[str, Any], label: str) -> None:
    if package.get("approval_rules") != _APPROVAL_RULES:
        _reject_freeform_laundering(package.get("approval_rules"), f"{label} approval_rules")
        raise ExactBeoPublicationApprovalValidationError(f"{label} approval_rules mismatch")


def _require_denials(package: dict[str, Any], label: str) -> None:
    denials = package.get("denied_authorities")
    if not isinstance(denials, list):
        raise ExactBeoPublicationApprovalValidationError(f"{label} denied_authorities must be a list")
    if denials != list(_DENIED_AUTHORITIES) or len(denials) != len(set(denials)):
        _reject_freeform_laundering(denials, f"{label} denied_authorities")
        raise ExactBeoPublicationApprovalValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects(package: dict[str, Any], label: str) -> None:
    if package.get("side_effects") != _SIDE_EFFECTS:
        raise ExactBeoPublicationApprovalValidationError(f"{label} side_effects mismatch")


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise ExactBeoPublicationApprovalValidationError(f"{label} {key} must be canonical sha256")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        raise ExactBeoPublicationApprovalValidationError(f"{label} forbidden authority wording: {findings[0]}")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(ch in "0123456789abcdef" for ch in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
