"""BLK-SYSTEM-279..281 RTM / blk-link drift-coverage second refresh challenge.

This grouped package records the operator's late generic approval statement after
the BLK-SYSTEM-277 refreshed short-``Approve`` challenge expired, emits a new
bounded short-``Approve`` challenge, and reconciles back to approval-required /
not-granted. It does not capture approval, reserve or consume a run ID, generate
RTM, execute production ``blk-link``, decide drift/coverage truth, read protected
bodies, invoke runtime/tooling, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from rtm_blk_link_drift_coverage_request_package_272_275 import (
    EXPECTED_OPERATOR_IDENTITY_264,
    _CANONICAL_REQUEST_272_HASH,
    _DENIED_AUTHORITIES,
    _SHORT_APPROVAL_REPLY,
    _deepcopy,
    _hash_package,
    _hash_text,
    _parse_timezone_timestamp,
    _reject_freeform_laundering,
    _require_allowed_keys,
    _require_denials,
    _require_hash,
    _require_markers,
    _require_safe_nonce,
    _require_side_effects,
    _require_status,
    _require_timestamp_order,
    _require_window,
)
from rtm_blk_link_drift_coverage_refresh_challenge_package_276_278 import (
    RtmBlkLinkDriftCoverageRefreshChallengeValidationError as _PriorRefreshError,
    _CANONICAL_EXPIRED_ATTEMPT_276_HASH,
    _CANONICAL_REFRESH_CHALLENGE_277_HASH,
    _CANONICAL_RECONCILIATION_278_HASH,
    _SIDE_EFFECTS_278,
    _validate_refresh_challenge_277,
)


class RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(ValueError):
    """Raised when BLK-SYSTEM-279..281 refresh-again evidence is unsafe."""


_SECOND_REFRESH_CHALLENGE_SCOPE_280 = "second_refresh_short_approve_after_expired_refreshed_challenge_no_execution"
_RECONCILED_STATE_281 = "rtm_blk_link_drift_coverage_second_refresh_challenge_ready_approval_required_not_granted"
_NEXT_FRONTIER_281 = "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED"
_EXPIRED_OR_UNBOUND_RESULT_279 = "operator_statement_not_bound_to_live_refresh_challenge_is_not_approval"
_EXPIRED_OR_UNBOUND_STATUS_279 = "EXPIRED_OR_UNBOUND_REFRESH_CHALLENGE_NOT_APPROVAL"

_CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH: str | None = "sha256:f499aec49dbb186dd1f89d8aa216510a68c59ab3cc0346bf084146de4071ffd0"
_CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH: str | None = "sha256:8a15f70354f5fade521197c6e954af6caa4ccb2f4bb76ec15a61121a11ed6ef6"
_CANONICAL_RECONCILIATION_281_HASH: str | None = "sha256:fc79e73c9e54b33c0c00afc8e694fd667e6035eba8b2e2d679a123001e154ce1"

_CHALLENGE_RULES_280 = {
    "operator_reply_must_equal_short_approval_reply": True,
    "second_refresh_challenge_hash_binds_request_hash_operator_identity_nonce_window_and_denials": True,
    "expired_prior_refresh_required": True,
    "unbound_or_expired_operator_statement_is_not_authority": True,
    "future_execution_requires_separate_package": True,
    "no_execution_or_run_id_side_effects": True,
}

_SIDE_EFFECTS_279 = dict(_SIDE_EFFECTS_278)
_SIDE_EFFECTS_279["expired_second_approve_attempt_recorded"] = True
_SIDE_EFFECTS_279["second_refresh_challenge_issued"] = False
_SIDE_EFFECTS_279["second_refresh_challenge_reconciled"] = False
_SIDE_EFFECTS_280 = dict(_SIDE_EFFECTS_279)
_SIDE_EFFECTS_280["second_refresh_challenge_issued"] = True
_SIDE_EFFECTS_281 = dict(_SIDE_EFFECTS_280)
_SIDE_EFFECTS_281["second_refresh_challenge_reconciled"] = True

_ALLOWED_EXPIRED_REFRESH_ATTEMPT_KEYS = {
    "sprint", "status", "markers", "request_hash", "prior_reconciliation_hash",
    "refresh_challenge_hash", "operator_identity", "operator_statement_hash",
    "operator_statement_status", "operator_statement_classification", "refresh_issued_at",
    "refresh_expires_at", "evaluated_at", "evaluation_result", "denied_authorities",
    "side_effects", "expired_refresh_attempt_hash",
}
_ALLOWED_SECOND_REFRESH_CHALLENGE_KEYS = {
    "sprint", "status", "markers", "request_hash", "prior_reconciliation_hash",
    "previous_refresh_challenge_hash", "expired_refresh_attempt_hash", "operator_identity",
    "challenge_nonce", "issued_at", "expires_at", "short_approval_reply", "challenge_scope",
    "challenge_rules", "challenge_payload_hash", "denied_authorities", "side_effects",
    "second_refresh_challenge_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "request_hash", "prior_reconciliation_hash",
    "previous_refresh_challenge_hash", "expired_refresh_attempt_hash", "second_refresh_challenge_hash",
    "reconciled_state", "next_frontier", "denied_authorities", "side_effects", "reconciliation_hash",
}


def record_expired_rtm_blk_link_drift_coverage_refresh_attempt_279(
    refresh_challenge_277: dict[str, Any],
    *,
    operator_statement: str,
    operator_identity: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Record a late/unbound statement after the refreshed challenge expired; do not approve."""

    try:
        challenge = _validate_refresh_challenge_277(refresh_challenge_277)
    except _PriorRefreshError as exc:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(str(exc)) from exc
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264 or operator_identity != challenge["operator_identity"]:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("operator_identity mismatch for BLK-SYSTEM-279")
    if not isinstance(operator_statement, str) or not operator_statement.strip():
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("operator_statement must be a non-empty string")

    if operator_statement != _SHORT_APPROVAL_REPLY:
        _reject_freeform_laundering(operator_statement, "operator_statement")

    issued = _parse_timezone_timestamp(challenge["issued_at"], "refresh issued_at")
    expires = _parse_timezone_timestamp(challenge["expires_at"], "refresh expires_at")
    evaluated = _parse_timezone_timestamp(evaluated_at, "evaluated_at")
    if evaluated < issued:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("refresh challenge was not yet issued")
    if evaluated < expires:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(
            "refresh challenge was still live; use an approval-capture package instead of refresh"
        )

    package = {
        "sprint": "BLK-SYSTEM-279",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL",
        "markers": [
            "BLK_SYSTEM_279_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
            _EXPIRED_OR_UNBOUND_STATUS_279,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": challenge["request_hash"],
        "prior_reconciliation_hash": _CANONICAL_RECONCILIATION_278_HASH,
        "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        "operator_identity": operator_identity,
        "operator_statement_hash": _hash_text(operator_statement),
        "operator_statement_status": _EXPIRED_OR_UNBOUND_STATUS_279,
        "operator_statement_classification": "generic_or_late_statement_recorded_hash_only_not_authority",
        "refresh_issued_at": challenge["issued_at"],
        "refresh_expires_at": challenge["expires_at"],
        "evaluated_at": evaluated_at,
        "evaluation_result": _EXPIRED_OR_UNBOUND_RESULT_279,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_279),
    }
    package["expired_refresh_attempt_hash"] = _hash_package(package)
    _validate_expired_refresh_attempt_279(package)
    return _deepcopy(package)


def build_rtm_blk_link_drift_coverage_second_refresh_challenge_280(
    expired_refresh_attempt_279: dict[str, Any],
    *,
    operator_identity: str,
    challenge_nonce: str,
    issued_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Emit a new bounded short-Approve challenge after the refreshed challenge expired."""

    expired_attempt = _validate_expired_refresh_attempt_279(expired_refresh_attempt_279)
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264 or operator_identity != expired_attempt["operator_identity"]:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("operator_identity mismatch for BLK-SYSTEM-280")
    _require_safe_nonce(challenge_nonce)
    _require_window(issued_at, expires_at, "issued_at", "expires_at")
    previous_expiry = _parse_timezone_timestamp(expired_attempt["refresh_expires_at"], "refresh_expires_at")
    issued = _parse_timezone_timestamp(issued_at, "issued_at")
    if issued <= previous_expiry:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(
            "issued_at must be after previous refresh challenge expiry"
        )
    _require_timestamp_order(
        expired_attempt["evaluated_at"],
        issued_at,
        "expired refresh attempt evaluated_at",
        "issued_at",
        allow_equal=True,
    )

    challenge_payload_hash = _hash_package(
        {
            "request_hash": expired_attempt["request_hash"],
            "prior_reconciliation_hash": expired_attempt["prior_reconciliation_hash"],
            "previous_refresh_challenge_hash": expired_attempt["refresh_challenge_hash"],
            "expired_refresh_attempt_hash": expired_attempt["expired_refresh_attempt_hash"],
            "operator_identity": operator_identity,
            "challenge_nonce": challenge_nonce,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "short_approval_reply": _SHORT_APPROVAL_REPLY,
            "challenge_scope": _SECOND_REFRESH_CHALLENGE_SCOPE_280,
            "denied_authorities": list(_DENIED_AUTHORITIES),
        }
    )
    package = {
        "sprint": "BLK-SYSTEM-280",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        "markers": [
            "BLK_SYSTEM_280_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY",
            "SHORT_APPROVE_BOUND_TO_SECOND_REFRESH_CHALLENGE_HASH",
            "NO_RUN_ID_OR_EXECUTION",
        ],
        "request_hash": expired_attempt["request_hash"],
        "prior_reconciliation_hash": expired_attempt["prior_reconciliation_hash"],
        "previous_refresh_challenge_hash": expired_attempt["refresh_challenge_hash"],
        "expired_refresh_attempt_hash": expired_attempt["expired_refresh_attempt_hash"],
        "operator_identity": operator_identity,
        "challenge_nonce": challenge_nonce,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "short_approval_reply": _SHORT_APPROVAL_REPLY,
        "challenge_scope": _SECOND_REFRESH_CHALLENGE_SCOPE_280,
        "challenge_rules": dict(_CHALLENGE_RULES_280),
        "challenge_payload_hash": challenge_payload_hash,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_280),
    }
    package["second_refresh_challenge_hash"] = _hash_package(package)
    _validate_second_refresh_challenge_280(package, expired_attempt["expired_refresh_attempt_hash"])
    return _deepcopy(package)


def reconcile_rtm_blk_link_drift_coverage_second_refresh_challenge_281(
    second_refresh_challenge_280: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile the second refreshed challenge to approval-required/not-granted."""

    challenge = _validate_second_refresh_challenge_280(second_refresh_challenge_280)
    package = {
        "sprint": "BLK-SYSTEM-281",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_281_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED",
            _NEXT_FRONTIER_281,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": challenge["request_hash"],
        "prior_reconciliation_hash": challenge["prior_reconciliation_hash"],
        "previous_refresh_challenge_hash": challenge["previous_refresh_challenge_hash"],
        "expired_refresh_attempt_hash": challenge["expired_refresh_attempt_hash"],
        "second_refresh_challenge_hash": challenge["second_refresh_challenge_hash"],
        "reconciled_state": _RECONCILED_STATE_281,
        "next_frontier": _NEXT_FRONTIER_281,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_281),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_281(package, challenge["second_refresh_challenge_hash"])
    return _deepcopy(package)


def _validate_expired_refresh_attempt_279(package: dict[str, Any]) -> dict[str, Any]:
    try:
        _require_allowed_keys(package, _ALLOWED_EXPIRED_REFRESH_ATTEMPT_KEYS, "expired refresh attempt package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL",
            "expired refresh attempt package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_279_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
                _EXPIRED_OR_UNBOUND_STATUS_279,
                "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
            ],
            "expired refresh attempt package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package canonical BLK-SYSTEM-272 hash mismatch")
        if package.get("prior_reconciliation_hash") != _CANONICAL_RECONCILIATION_278_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package canonical BLK-SYSTEM-278 hash mismatch")
        if package.get("refresh_challenge_hash") != _CANONICAL_REFRESH_CHALLENGE_277_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package canonical BLK-SYSTEM-277 hash mismatch")
        if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package operator_identity mismatch")
        _require_hash(package, "operator_statement_hash", "expired refresh attempt package")
        if package.get("operator_statement_status") != _EXPIRED_OR_UNBOUND_STATUS_279:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package operator_statement_status mismatch")
        if package.get("operator_statement_classification") != "generic_or_late_statement_recorded_hash_only_not_authority":
            _reject_freeform_laundering(
                package.get("operator_statement_classification"),
                "expired refresh attempt package operator_statement_classification",
            )
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package operator_statement_classification mismatch")
        if package.get("evaluation_result") != _EXPIRED_OR_UNBOUND_RESULT_279:
            _reject_freeform_laundering(package.get("evaluation_result"), "expired refresh attempt package evaluation_result")
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package evaluation_result mismatch")
        _require_timestamp_order(
            package.get("refresh_issued_at"),
            package.get("refresh_expires_at"),
            "refresh_issued_at",
            "refresh_expires_at",
        )
        _require_timestamp_order(
            package.get("refresh_expires_at"),
            package.get("evaluated_at"),
            "refresh_expires_at",
            "evaluated_at",
            allow_equal=True,
        )
        _require_denials(package, "expired refresh attempt package")
        _require_side_effects(package, _SIDE_EFFECTS_279, "expired refresh attempt package")
        _require_hash(package, "expired_refresh_attempt_hash", "expired refresh attempt package")
    except ValueError as exc:
        if isinstance(exc, RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError):
            raise
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(str(exc)) from exc
    if package.get("expired_refresh_attempt_hash") != _hash_package({key: value for key, value in package.items() if key != "expired_refresh_attempt_hash"}):
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package expired_refresh_attempt_hash mismatch")
    if _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH and package.get("expired_refresh_attempt_hash") != _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("expired refresh attempt package canonical BLK-SYSTEM-279 hash mismatch")
    return package


def _validate_second_refresh_challenge_280(
    package: dict[str, Any],
    expected_expired_refresh_attempt_hash: str | None = None,
) -> dict[str, Any]:
    try:
        _require_allowed_keys(package, _ALLOWED_SECOND_REFRESH_CHALLENGE_KEYS, "second refresh challenge package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
            "second refresh challenge package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_280_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY",
                "SHORT_APPROVE_BOUND_TO_SECOND_REFRESH_CHALLENGE_HASH",
                "NO_RUN_ID_OR_EXECUTION",
            ],
            "second refresh challenge package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package canonical BLK-SYSTEM-272 hash mismatch")
        if package.get("prior_reconciliation_hash") != _CANONICAL_RECONCILIATION_278_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package canonical BLK-SYSTEM-278 hash mismatch")
        if package.get("previous_refresh_challenge_hash") != _CANONICAL_REFRESH_CHALLENGE_277_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package canonical BLK-SYSTEM-277 hash mismatch")
        if expected_expired_refresh_attempt_hash and package.get("expired_refresh_attempt_hash") != expected_expired_refresh_attempt_hash:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package expired_refresh_attempt_hash mismatch")
        if _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH and package.get("expired_refresh_attempt_hash") != _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package canonical BLK-SYSTEM-279 hash mismatch")
        if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package operator_identity mismatch")
        _require_safe_nonce(package.get("challenge_nonce"))
        _require_window(package.get("issued_at"), package.get("expires_at"), "issued_at", "expires_at")
        if package.get("short_approval_reply") != _SHORT_APPROVAL_REPLY:
            _reject_freeform_laundering(package.get("short_approval_reply"), "second refresh challenge package short_approval_reply")
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package short_approval_reply mismatch")
        if package.get("challenge_scope") != _SECOND_REFRESH_CHALLENGE_SCOPE_280:
            _reject_freeform_laundering(package.get("challenge_scope"), "second refresh challenge package challenge_scope")
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package challenge_scope mismatch")
        if package.get("challenge_rules") != _CHALLENGE_RULES_280:
            _reject_freeform_laundering(package.get("challenge_rules"), "second refresh challenge package challenge_rules")
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package challenge_rules mismatch")
        expected_payload_hash = _hash_package(
            {
                "request_hash": package["request_hash"],
                "prior_reconciliation_hash": package["prior_reconciliation_hash"],
                "previous_refresh_challenge_hash": package["previous_refresh_challenge_hash"],
                "expired_refresh_attempt_hash": package["expired_refresh_attempt_hash"],
                "operator_identity": package["operator_identity"],
                "challenge_nonce": package["challenge_nonce"],
                "issued_at": package["issued_at"],
                "expires_at": package["expires_at"],
                "short_approval_reply": package["short_approval_reply"],
                "challenge_scope": package["challenge_scope"],
                "denied_authorities": package["denied_authorities"],
            }
        )
        if package.get("challenge_payload_hash") != expected_payload_hash:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package challenge_payload_hash mismatch")
        _require_denials(package, "second refresh challenge package")
        _require_side_effects(package, _SIDE_EFFECTS_280, "second refresh challenge package")
        _require_hash(package, "second_refresh_challenge_hash", "second refresh challenge package")
    except ValueError as exc:
        if isinstance(exc, RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError):
            raise
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(str(exc)) from exc
    if package.get("second_refresh_challenge_hash") != _hash_package({key: value for key, value in package.items() if key != "second_refresh_challenge_hash"}):
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package second_refresh_challenge_hash mismatch")
    if _CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH and package.get("second_refresh_challenge_hash") != _CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh challenge package canonical BLK-SYSTEM-280 hash mismatch")
    return package


def _validate_reconciliation_281(package: dict[str, Any], expected_second_refresh_challenge_hash: str | None = None) -> None:
    try:
        _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "second refresh reconciliation package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
            "second refresh reconciliation package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_281_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED",
                _NEXT_FRONTIER_281,
                "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
            ],
            "second refresh reconciliation package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-272 hash mismatch")
        if package.get("prior_reconciliation_hash") != _CANONICAL_RECONCILIATION_278_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-278 hash mismatch")
        if package.get("previous_refresh_challenge_hash") != _CANONICAL_REFRESH_CHALLENGE_277_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-277 hash mismatch")
        if _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH and package.get("expired_refresh_attempt_hash") != _CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-279 hash mismatch")
        if expected_second_refresh_challenge_hash and package.get("second_refresh_challenge_hash") != expected_second_refresh_challenge_hash:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package second_refresh_challenge_hash mismatch")
        if _CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH and package.get("second_refresh_challenge_hash") != _CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-280 hash mismatch")
        if package.get("reconciled_state") != _RECONCILED_STATE_281:
            _reject_freeform_laundering(package.get("reconciled_state"), "second refresh reconciliation package reconciled_state")
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package reconciled_state mismatch")
        if package.get("next_frontier") != _NEXT_FRONTIER_281:
            raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package next_frontier mismatch")
        _require_denials(package, "second refresh reconciliation package")
        _require_side_effects(package, _SIDE_EFFECTS_281, "second refresh reconciliation package")
        _require_hash(package, "reconciliation_hash", "second refresh reconciliation package")
    except ValueError as exc:
        if isinstance(exc, RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError):
            raise
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError(str(exc)) from exc
    if package.get("reconciliation_hash") != _hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}):
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_RECONCILIATION_281_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_281_HASH:
        raise RtmBlkLinkDriftCoverageSecondRefreshChallengeValidationError("second refresh reconciliation package canonical BLK-SYSTEM-281 hash mismatch")


def _clone(value: Any) -> Any:
    return deepcopy(value)
