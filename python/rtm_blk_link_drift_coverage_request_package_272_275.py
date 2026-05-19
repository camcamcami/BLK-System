"""BLK-SYSTEM-272..275 RTM / blk-link drift-coverage request package.

This grouped package consumes the BLK-SYSTEM-271 exact BEO publication finality
reconciliation and prepares only a request/challenge/preflight/reconciliation
surface for future RTM / production ``blk-link`` drift-coverage authority. It
implements the Discord-friendly short ``Approve`` challenge contract without
capturing approval, reserving/consuming a run ID, generating RTM, executing
production ``blk-link``, deciding drift/coverage truth, reading protected bodies,
invoking runtime/tooling, or mutating target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from exact_beo_publication_approval_capture_264_265 import EXPECTED_OPERATOR_IDENTITY_264
from exact_beo_publication_execution_package_269_271 import (
    _CANONICAL_EXECUTION_270_HASH,
    _CANONICAL_RECONCILIATION_271_HASH,
    _validate_reconciliation_271,
)


class RtmBlkLinkDriftCoverageRequestPackageValidationError(ValueError):
    """Raised when BLK-SYSTEM-272..275 request evidence is unsafe."""


_SHORT_APPROVAL_REPLY = "Approve"
_REQUEST_SCOPE_272 = "request_future_metadata_only_rtm_blk_link_drift_coverage_after_beo_finality"
_CHALLENGE_SCOPE_273 = "bind_short_approve_to_exact_request_challenge_no_execution"
_GENERIC_BLOCKED_RESULT_274 = "generic_or_unbound_operator_directive_is_not_rtm_blk_link_approval"
_MATCHED_RESULT_274 = "short_approve_bound_to_challenge_but_no_execution_authority"
_EXPIRED_BLOCKED_RESULT_274 = "short_approve_seen_after_challenge_expiry_is_not_approval"
_PRE_ISSUE_BLOCKED_RESULT_274 = "short_approve_seen_before_challenge_issue_is_not_approval"
_RECONCILED_STATE_275 = "rtm_blk_link_drift_coverage_request_ready_approval_required_not_granted"
_NEXT_FRONTIER_275 = "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_BOUND_APPROVE_OR_EXACT_TEXT_REQUIRED_NOT_GRANTED"

_CANONICAL_REQUEST_272_HASH: str | None = "sha256:71a299dcecc0c2c2e5a617924ef6de67fce99cdfa96c682db1cfdd3a93295ee5"
_CANONICAL_CHALLENGE_273_HASH: str | None = "sha256:9bdd2f614f71f1506bcbe47c9ae90a21f7a28851e933a7a72e6538fc2d4e8330"
_CANONICAL_PREFLIGHT_274_HASH: str | None = "sha256:a3ab1310a900b9ee8fa99b872d782ccdfb3af4f05d4cbc135a032b913cbfa912"
_CANONICAL_RECONCILIATION_275_HASH: str | None = "sha256:91ae63a6ec9d43088c6852d2d0f0bab7bf8663c9bbc9f2c2f1f8177997acdb88"

_REQUIRED_METADATA_INPUTS = [
    "beo_finality_reconciliation_hash",
    "beo_finality_execution_hash",
    "beo_finality_record_hash",
    "signature_receipt_hash",
    "immutable_storage_receipt_hash",
    "public_ledger_entry_hash",
    "blk_req_metadata_hashes_only",
    "rtm_trace_metadata_hashes_only",
    "drift_probe_metadata_hashes_only",
    "coverage_probe_metadata_hashes_only",
]

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_RTM_BLK_LINK_APPROVAL",
    "UNBOUND_APPROVE_AS_APPROVAL",
    "APPROVE_WITHOUT_CHALLENGE_HASH_OPERATOR_IDENTITY_OR_WINDOW",
    "APPROVAL_REUSE_OR_RETARGETING",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_EXECUTION_OR_REUSABLE_BLK_LINK_AUTHORITY",
    "DRIFT_REJECTION_OR_DRIFT_TRUTH",
    "COVERAGE_TRUTH_OR_COVERAGE_MATRIX_GENERATION",
    "ACTIVE_VAULT_COMPARISON_OR_FILESYSTEM_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_REUSE_OR_FUTURE_PUBLICATION_RUN",
    "BEO_CLOSEOUT_EXECUTION",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "BEB_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
]

_SIDE_EFFECTS_BASE = {
    "request_package_prepared": True,
    "approval_challenge_issued": False,
    "approval_preflight_recorded": False,
    "short_approve_matched": False,
    "approval_captured": False,
    "approval_reused": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "rtm_generation": False,
    "reusable_rtm_generation": False,
    "production_blk_link_execution": False,
    "reusable_blk_link_authority": False,
    "drift_rejection": False,
    "drift_truth": False,
    "coverage_truth": False,
    "coverage_matrix_generated": False,
    "active_vault_comparison_or_scan": False,
    "protected_body_access": False,
    "protected_body_read_copy_parse_hash_scan_mutation": False,
    "beo_publication_or_future_publication_run": False,
    "beo_closeout_execution": False,
    "signer_storage_ledger_reuse": False,
    "rollback_revocation_supersession_execution": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "beb_dispatch": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_SIDE_EFFECTS_272 = dict(_SIDE_EFFECTS_BASE)
_SIDE_EFFECTS_273 = dict(_SIDE_EFFECTS_BASE)
_SIDE_EFFECTS_273["approval_challenge_issued"] = True
_SIDE_EFFECTS_274_BLOCKED = dict(_SIDE_EFFECTS_273)
_SIDE_EFFECTS_274_BLOCKED["approval_preflight_recorded"] = True
_SIDE_EFFECTS_274_MATCHED = dict(_SIDE_EFFECTS_274_BLOCKED)
_SIDE_EFFECTS_274_MATCHED["short_approve_matched"] = True
_SIDE_EFFECTS_275 = dict(_SIDE_EFFECTS_274_BLOCKED)

_APPROVAL_RULES_272 = {
    "short_approve_requires_challenge_hash": True,
    "short_approve_requires_operator_identity": True,
    "short_approve_requires_unexpired_window": True,
    "short_approve_is_not_generic_package_authority": True,
    "future_execution_requires_separate_package": True,
    "no_run_id_reserved_or_consumed": True,
}
_CHALLENGE_RULES_273 = {
    "operator_reply_must_equal_short_approval_reply": True,
    "challenge_hash_binds_request_hash_operator_identity_nonce_window_and_denials": True,
    "unbound_approve_is_not_authority": True,
    "expired_challenge_is_not_authority": True,
    "no_execution_or_run_id_side_effects": True,
}

_ALLOWED_REQUEST_KEYS = {
    "sprint", "status", "markers", "beo_finality_reconciliation_hash", "beo_finality_execution_hash",
    "beo_finality_record_hash", "signature_receipt_hash", "immutable_storage_receipt_hash",
    "public_ledger_entry_hash", "operator_identity", "requested_at", "expires_at", "request_scope",
    "metadata_requirements", "approval_rules", "denied_authorities", "side_effects", "request_hash",
}
_ALLOWED_CHALLENGE_KEYS = {
    "sprint", "status", "markers", "request_hash", "operator_identity", "challenge_nonce", "issued_at",
    "expires_at", "short_approval_reply", "challenge_scope", "challenge_rules", "challenge_payload_hash",
    "denied_authorities", "side_effects", "challenge_hash",
}
_ALLOWED_PREFLIGHT_KEYS = {
    "sprint", "status", "markers", "request_hash", "challenge_hash", "operator_identity", "operator_reply_hash",
    "operator_reply_status", "challenge_issued_at", "challenge_expires_at", "short_approval_reply", "evaluated_at",
    "evaluation_result", "denied_authorities", "side_effects", "preflight_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "request_hash", "challenge_hash", "preflight_hash", "reconciled_state",
    "next_frontier", "denied_authorities", "side_effects", "reconciliation_hash",
}


def build_rtm_blk_link_drift_coverage_request_272(
    reconciliation_package_271: dict[str, Any],
    *,
    operator_identity: str,
    requested_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Prepare a request-only RTM / blk-link drift-coverage package."""

    try:
        _validate_reconciliation_271(reconciliation_package_271)
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(str(exc)) from exc
    if reconciliation_package_271.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_271_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("canonical BLK-SYSTEM-271 reconciliation hash mismatch")
    if reconciliation_package_271.get("execution_package_hash") != _CANONICAL_EXECUTION_270_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("canonical BLK-SYSTEM-270 execution hash mismatch")
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("operator_identity mismatch for BLK-SYSTEM-272")
    _require_window(requested_at, expires_at, "requested_at", "expires_at")

    package = {
        "sprint": "BLK-SYSTEM-272",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_272_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY",
            "POST_BEO_FINALITY_METADATA_ONLY_REQUEST",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "beo_finality_reconciliation_hash": reconciliation_package_271["reconciliation_hash"],
        "beo_finality_execution_hash": reconciliation_package_271["execution_package_hash"],
        "beo_finality_record_hash": reconciliation_package_271["finality_record_hash"],
        "signature_receipt_hash": reconciliation_package_271["signature_receipt_hash"],
        "immutable_storage_receipt_hash": reconciliation_package_271["immutable_storage_receipt_hash"],
        "public_ledger_entry_hash": reconciliation_package_271["public_ledger_entry_hash"],
        "operator_identity": operator_identity,
        "requested_at": requested_at,
        "expires_at": expires_at,
        "request_scope": _REQUEST_SCOPE_272,
        "metadata_requirements": list(_REQUIRED_METADATA_INPUTS),
        "approval_rules": dict(_APPROVAL_RULES_272),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_272),
    }
    package["request_hash"] = _hash_package(package)
    _validate_request_272(package)
    return _deepcopy(package)


def build_rtm_blk_link_drift_coverage_approve_challenge_273(
    request_package_272: dict[str, Any],
    *,
    operator_identity: str,
    challenge_nonce: str,
    issued_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Emit a bounded short-Approve challenge without approving or executing."""

    request = _validate_request_272(request_package_272)
    if operator_identity != request["operator_identity"] or operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("operator_identity mismatch for BLK-SYSTEM-273")
    _require_safe_nonce(challenge_nonce)
    _require_window(issued_at, expires_at, "issued_at", "expires_at")
    _require_timestamp_order(request["requested_at"], issued_at, "request requested_at", "issued_at", allow_equal=True)
    _require_timestamp_order(expires_at, request["expires_at"], "challenge expires_at", "request expires_at", allow_equal=True)

    challenge_payload_hash = _hash_package(
        {
            "request_hash": request["request_hash"],
            "operator_identity": operator_identity,
            "challenge_nonce": challenge_nonce,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "short_approval_reply": _SHORT_APPROVAL_REPLY,
            "challenge_scope": _CHALLENGE_SCOPE_273,
            "denied_authorities": list(_DENIED_AUTHORITIES),
        }
    )
    package = {
        "sprint": "BLK-SYSTEM-273",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        "markers": [
            "BLK_SYSTEM_273_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY",
            "SHORT_APPROVE_BOUND_TO_CHALLENGE_HASH",
            "NO_RUN_ID_OR_EXECUTION",
        ],
        "request_hash": request["request_hash"],
        "operator_identity": operator_identity,
        "challenge_nonce": challenge_nonce,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "short_approval_reply": _SHORT_APPROVAL_REPLY,
        "challenge_scope": _CHALLENGE_SCOPE_273,
        "challenge_rules": dict(_CHALLENGE_RULES_273),
        "challenge_payload_hash": challenge_payload_hash,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_273),
    }
    package["challenge_hash"] = _hash_package(package)
    _validate_challenge_273(package, request["request_hash"])
    return _deepcopy(package)


def evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
    challenge_package_273: dict[str, Any],
    *,
    operator_reply: str,
    operator_identity: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Evaluate one operator reply against a challenge without capturing authority."""

    challenge = _validate_challenge_273(challenge_package_273)
    if operator_identity != challenge["operator_identity"] or operator_identity != EXPECTED_OPERATOR_IDENTITY_264:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("operator_identity mismatch for BLK-SYSTEM-274")
    if not isinstance(operator_reply, str) or not operator_reply.strip():
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("operator_reply must be a non-empty string")
    issued = _parse_timezone_timestamp(challenge["issued_at"], "challenge issued_at")
    evaluated = _parse_timezone_timestamp(evaluated_at, "evaluated_at")
    expires = _parse_timezone_timestamp(challenge["expires_at"], "challenge expires_at")

    if operator_reply != _SHORT_APPROVAL_REPLY:
        _reject_freeform_laundering(operator_reply, "operator_reply")
        status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        reply_status = "NOT_BOUND_APPROVE_FOR_CHALLENGE"
        result = _GENERIC_BLOCKED_RESULT_274
        side_effects = dict(_SIDE_EFFECTS_274_BLOCKED)
        marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
    elif evaluated < issued:
        status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        reply_status = "CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL"
        result = _PRE_ISSUE_BLOCKED_RESULT_274
        side_effects = dict(_SIDE_EFFECTS_274_BLOCKED)
        marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
    elif evaluated >= expires:
        status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        reply_status = "EXPIRED_CHALLENGE_NOT_APPROVAL"
        result = _EXPIRED_BLOCKED_RESULT_274
        side_effects = dict(_SIDE_EFFECTS_274_BLOCKED)
        marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
    else:
        status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_MATCHED_EXECUTION_NOT_PERFORMED"
        reply_status = "BOUND_APPROVE_FOR_CHALLENGE"
        result = _MATCHED_RESULT_274
        side_effects = dict(_SIDE_EFFECTS_274_MATCHED)
        marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_MATCHED_NO_EXECUTION"

    package = {
        "sprint": "BLK-SYSTEM-274",
        "status": status,
        "markers": [
            marker,
            "SHORT_APPROVE_REQUIRES_BOUND_CHALLENGE_HASH",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": challenge["request_hash"],
        "challenge_hash": challenge["challenge_hash"],
        "operator_identity": operator_identity,
        "operator_reply_hash": _hash_text(operator_reply),
        "operator_reply_status": reply_status,
        "challenge_issued_at": challenge["issued_at"],
        "challenge_expires_at": challenge["expires_at"],
        "short_approval_reply": challenge["short_approval_reply"],
        "evaluated_at": evaluated_at,
        "evaluation_result": result,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": side_effects,
    }
    package["preflight_hash"] = _hash_package(package)
    _validate_preflight_274(package, challenge["challenge_hash"])
    return _deepcopy(package)


def reconcile_rtm_blk_link_drift_coverage_request_275(preflight_package_274: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the request/challenge guard to approval-required/not-granted."""

    preflight = _validate_preflight_274(preflight_package_274)
    if preflight["operator_reply_status"] != "NOT_BOUND_APPROVE_FOR_CHALLENGE":
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(
            "current package reconciles only blocked preflight from non-approval directive"
        )
    package = {
        "sprint": "BLK-SYSTEM-275",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_275_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED",
            _NEXT_FRONTIER_275,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": preflight["request_hash"],
        "challenge_hash": preflight["challenge_hash"],
        "preflight_hash": preflight["preflight_hash"],
        "reconciled_state": _RECONCILED_STATE_275,
        "next_frontier": _NEXT_FRONTIER_275,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_275),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_275(package, preflight["preflight_hash"])
    return _deepcopy(package)


def _validate_request_272(package: dict[str, Any]) -> dict[str, Any]:
    _require_allowed_keys(package, _ALLOWED_REQUEST_KEYS, "request package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_NOT_GRANTED", "request package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_272_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY",
            "POST_BEO_FINALITY_METADATA_ONLY_REQUEST",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request package",
    )
    if package.get("beo_finality_reconciliation_hash") != _CANONICAL_RECONCILIATION_271_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package canonical BLK-SYSTEM-271 hash mismatch")
    if package.get("beo_finality_execution_hash") != _CANONICAL_EXECUTION_270_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package canonical BLK-SYSTEM-270 hash mismatch")
    for key in (
        "beo_finality_record_hash", "signature_receipt_hash", "immutable_storage_receipt_hash",
        "public_ledger_entry_hash", "request_hash",
    ):
        _require_hash(package, key, "request package")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package operator_identity mismatch")
    _require_window(package.get("requested_at"), package.get("expires_at"), "requested_at", "expires_at")
    if package.get("request_scope") != _REQUEST_SCOPE_272:
        _reject_freeform_laundering(package.get("request_scope"), "request package request_scope")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package request_scope mismatch")
    if package.get("metadata_requirements") != list(_REQUIRED_METADATA_INPUTS):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package metadata_requirements mismatch")
    if package.get("approval_rules") != _APPROVAL_RULES_272:
        _reject_freeform_laundering(package.get("approval_rules"), "request package approval_rules")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package approval_rules mismatch")
    _require_denials(package, "request package")
    _require_side_effects(package, _SIDE_EFFECTS_272, "request package")
    if package.get("request_hash") != _hash_package({key: value for key, value in package.items() if key != "request_hash"}):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package request_hash mismatch")
    if _CANONICAL_REQUEST_272_HASH and package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("request package canonical BLK-SYSTEM-272 hash mismatch")
    return package


def _validate_challenge_273(package: dict[str, Any], expected_request_hash: str | None = None) -> dict[str, Any]:
    _require_allowed_keys(package, _ALLOWED_CHALLENGE_KEYS, "challenge package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY_NOT_APPROVED", "challenge package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_273_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY",
            "SHORT_APPROVE_BOUND_TO_CHALLENGE_HASH",
            "NO_RUN_ID_OR_EXECUTION",
        ],
        "challenge package",
    )
    if expected_request_hash and package.get("request_hash") != expected_request_hash:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package request_hash mismatch")
    if _CANONICAL_REQUEST_272_HASH and package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package canonical BLK-SYSTEM-272 hash mismatch")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package operator_identity mismatch")
    _require_safe_nonce(package.get("challenge_nonce"))
    _require_window(package.get("issued_at"), package.get("expires_at"), "issued_at", "expires_at")
    if package.get("short_approval_reply") != _SHORT_APPROVAL_REPLY:
        _reject_freeform_laundering(package.get("short_approval_reply"), "challenge package short_approval_reply")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package short_approval_reply mismatch")
    if package.get("challenge_scope") != _CHALLENGE_SCOPE_273:
        _reject_freeform_laundering(package.get("challenge_scope"), "challenge package challenge_scope")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package challenge_scope mismatch")
    if package.get("challenge_rules") != _CHALLENGE_RULES_273:
        _reject_freeform_laundering(package.get("challenge_rules"), "challenge package challenge_rules")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package challenge_rules mismatch")
    expected_payload_hash = _hash_package(
        {
            "request_hash": package["request_hash"],
            "operator_identity": package["operator_identity"],
            "challenge_nonce": package["challenge_nonce"],
            "issued_at": package["issued_at"],
            "expires_at": package["expires_at"],
            "short_approval_reply": package["short_approval_reply"],
            "challenge_scope": package["challenge_scope"],
            "denied_authorities": list(_DENIED_AUTHORITIES),
        }
    )
    if package.get("challenge_payload_hash") != expected_payload_hash:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package challenge_payload_hash mismatch")
    _require_denials(package, "challenge package")
    _require_side_effects(package, _SIDE_EFFECTS_273, "challenge package")
    _require_hash(package, "challenge_hash", "challenge package")
    if package.get("challenge_hash") != _hash_package({key: value for key, value in package.items() if key != "challenge_hash"}):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package challenge_hash mismatch")
    if _CANONICAL_CHALLENGE_273_HASH and package.get("challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge package canonical BLK-SYSTEM-273 hash mismatch")
    return package


def _validate_preflight_274(package: dict[str, Any], expected_challenge_hash: str | None = None) -> dict[str, Any]:
    _require_allowed_keys(package, _ALLOWED_PREFLIGHT_KEYS, "preflight package")
    if expected_challenge_hash and package.get("challenge_hash") != expected_challenge_hash:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package challenge_hash mismatch")
    if _CANONICAL_REQUEST_272_HASH and package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package canonical BLK-SYSTEM-272 hash mismatch")
    if _CANONICAL_CHALLENGE_273_HASH and package.get("challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package canonical BLK-SYSTEM-273 hash mismatch")
    if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package operator_identity mismatch")
    _require_timezone_timestamp(package.get("evaluated_at"), "evaluated_at")
    issued = _parse_timezone_timestamp(package.get("challenge_issued_at"), "challenge_issued_at")
    expires = _parse_timezone_timestamp(package.get("challenge_expires_at"), "challenge_expires_at")
    evaluated = _parse_timezone_timestamp(package.get("evaluated_at"), "evaluated_at")
    if package.get("short_approval_reply") != _SHORT_APPROVAL_REPLY:
        _reject_freeform_laundering(package.get("short_approval_reply"), "preflight package short_approval_reply")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package short_approval_reply mismatch")
    status = package.get("status")
    reply_status = package.get("operator_reply_status")
    if reply_status == "BOUND_APPROVE_FOR_CHALLENGE":
        expected_status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_MATCHED_EXECUTION_NOT_PERFORMED"
        expected_marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_MATCHED_NO_EXECUTION"
        expected_result = _MATCHED_RESULT_274
        expected_effects = _SIDE_EFFECTS_274_MATCHED
    elif reply_status == "NOT_BOUND_APPROVE_FOR_CHALLENGE":
        expected_status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_result = _GENERIC_BLOCKED_RESULT_274
        expected_effects = _SIDE_EFFECTS_274_BLOCKED
    elif reply_status == "CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL":
        expected_status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_result = _PRE_ISSUE_BLOCKED_RESULT_274
        expected_effects = _SIDE_EFFECTS_274_BLOCKED
    elif reply_status == "EXPIRED_CHALLENGE_NOT_APPROVAL":
        expected_status = "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_marker = "BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED"
        expected_result = _EXPIRED_BLOCKED_RESULT_274
        expected_effects = _SIDE_EFFECTS_274_BLOCKED
    else:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package operator_reply_status mismatch")
    if status != expected_status:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package status mismatch")
    _require_markers(
        package,
        [
            expected_marker,
            "SHORT_APPROVE_REQUIRES_BOUND_CHALLENGE_HASH",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "preflight package",
    )
    if package.get("evaluation_result") != expected_result:
        _reject_freeform_laundering(package.get("evaluation_result"), "preflight package evaluation_result")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package evaluation_result mismatch")
    _require_hash(package, "operator_reply_hash", "preflight package")
    if reply_status in {
        "BOUND_APPROVE_FOR_CHALLENGE",
        "CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL",
        "EXPIRED_CHALLENGE_NOT_APPROVAL",
    } and package.get("operator_reply_hash") != _hash_text(_SHORT_APPROVAL_REPLY):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package operator_reply_hash mismatch")
    if reply_status == "BOUND_APPROVE_FOR_CHALLENGE" and not (issued <= evaluated < expires):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package challenge window mismatch")
    if reply_status == "CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL" and not (evaluated < issued):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package challenge pre-issue window mismatch")
    if reply_status == "EXPIRED_CHALLENGE_NOT_APPROVAL" and not (evaluated >= expires):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package challenge expiry window mismatch")
    _require_denials(package, "preflight package")
    _require_side_effects(package, expected_effects, "preflight package")
    _require_hash(package, "preflight_hash", "preflight package")
    if package.get("preflight_hash") != _hash_package({key: value for key, value in package.items() if key != "preflight_hash"}):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package preflight_hash mismatch")
    if (
        _CANONICAL_PREFLIGHT_274_HASH
        and reply_status == "NOT_BOUND_APPROVE_FOR_CHALLENGE"
        and package.get("preflight_hash") != _CANONICAL_PREFLIGHT_274_HASH
    ):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("preflight package canonical BLK-SYSTEM-274 hash mismatch")
    return package


def _validate_reconciliation_275(package: dict[str, Any], expected_preflight_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "reconciliation package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED", "reconciliation package")
    _require_markers(
        package,
        [
            "BLK_SYSTEM_275_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED",
            _NEXT_FRONTIER_275,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "reconciliation package",
    )
    if _CANONICAL_REQUEST_272_HASH and package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package canonical BLK-SYSTEM-272 hash mismatch")
    if _CANONICAL_CHALLENGE_273_HASH and package.get("challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package canonical BLK-SYSTEM-273 hash mismatch")
    if expected_preflight_hash and package.get("preflight_hash") != expected_preflight_hash:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package preflight_hash mismatch")
    if _CANONICAL_PREFLIGHT_274_HASH and package.get("preflight_hash") != _CANONICAL_PREFLIGHT_274_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package canonical BLK-SYSTEM-274 hash mismatch")
    if package.get("reconciled_state") != _RECONCILED_STATE_275:
        _reject_freeform_laundering(package.get("reconciled_state"), "reconciliation package reconciled_state")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package reconciled_state mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER_275:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package next_frontier mismatch")
    _require_denials(package, "reconciliation package")
    _require_side_effects(package, _SIDE_EFFECTS_275, "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    if package.get("reconciliation_hash") != _hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_RECONCILIATION_275_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_275_HASH:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("reconciliation package canonical BLK-SYSTEM-275 hash mismatch")


def _require_allowed_keys(package: Any, allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} must be a dictionary")
    extras = sorted(set(package) - allowed)
    missing = sorted(allowed - set(package))
    if extras:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} unsupported field {extras[0]!r}")
    if missing:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} missing field {missing[0]!r}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} markers mismatch")


def _require_denials(package: dict[str, Any], label: str) -> None:
    denials = package.get("denied_authorities")
    if not isinstance(denials, list):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} denied_authorities must be a list")
    if any(not isinstance(item, str) for item in denials):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} denied_authorities must be strings")
    if denials != _DENIED_AUTHORITIES or len(denials) != len(set(denials)):
        _reject_freeform_laundering(denials, f"{label} denied_authorities")
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], label: str) -> None:
    if package.get("side_effects") != expected:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} side_effects mismatch")


def _require_safe_nonce(value: Any) -> None:
    if not isinstance(value, str) or not (16 <= len(value) <= 80):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge_nonce must be a bounded ASCII token")
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
    if any(ch not in allowed for ch in value):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError("challenge_nonce contains unsafe characters")
    _reject_freeform_laundering(value, "challenge_nonce")


def _require_window(start: Any, end: Any, start_label: str, end_label: str) -> None:
    _require_timestamp_order(start, end, start_label, end_label)


def _require_timestamp_order(start: Any, end: Any, start_label: str, end_label: str, *, allow_equal: bool = False) -> None:
    start_value = _parse_timezone_timestamp(start, start_label)
    end_value = _parse_timezone_timestamp(end, end_label)
    if allow_equal:
        if end_value < start_value:
            raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{end_label} must be at or after {start_label}")
    elif end_value <= start_value:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{end_label} must be after {start_label}")


def _require_timezone_timestamp(value: Any, label: str) -> None:
    _parse_timezone_timestamp(value, label)


def _parse_timezone_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} must be a timezone-aware ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} must be a timezone-aware ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} must be timezone-aware")
    return parsed


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} {key} must be canonical sha256")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        raise RtmBlkLinkDriftCoverageRequestPackageValidationError(f"{label} forbidden authority wording: {findings[0]}")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(ch in "0123456789abcdef" for ch in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
