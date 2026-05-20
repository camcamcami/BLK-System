"""BLK-SYSTEM-276..278 RTM / blk-link drift-coverage approval refresh challenge.

This grouped package records the operator's late ``Approve`` against the expired
BLK-SYSTEM-273 challenge as non-approval, emits a fresh bounded short-``Approve``
challenge, and reconciles back to approval-required/not-granted. It does not
capture approval, reserve or consume a run ID, generate RTM, execute production
``blk-link``, decide drift/coverage truth, read protected bodies, invoke runtime
or tooling, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from rtm_blk_link_drift_coverage_request_package_272_275 import (
    EXPECTED_OPERATOR_IDENTITY_264,
    RtmBlkLinkDriftCoverageRequestPackageValidationError as _RequestPackageError,
    _CANONICAL_CHALLENGE_273_HASH,
    _CANONICAL_REQUEST_272_HASH,
    _DENIED_AUTHORITIES,
    _EXPIRED_BLOCKED_RESULT_274,
    _SHORT_APPROVAL_REPLY,
    _SIDE_EFFECTS_274_BLOCKED,
    _deepcopy,
    _hash_package,
    _hash_text,
    _is_hash,
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
    _validate_challenge_273,
    evaluate_rtm_blk_link_drift_coverage_approval_preflight_274,
)


class RtmBlkLinkDriftCoverageRefreshChallengeValidationError(ValueError):
    """Raised when BLK-SYSTEM-276..278 refresh challenge evidence is unsafe."""


_REFRESH_CHALLENGE_SCOPE_277 = "refresh_short_approve_after_expired_prior_challenge_no_execution"
_RECONCILED_STATE_278 = "rtm_blk_link_drift_coverage_refresh_challenge_ready_approval_required_not_granted"
_NEXT_FRONTIER_278 = "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED"

_CANONICAL_EXPIRED_ATTEMPT_276_HASH: str | None = "sha256:123b60725b593ff7de8b2868f9221190c36e6255826b112e7f0b54676cc26ee9"
_CANONICAL_REFRESH_CHALLENGE_277_HASH: str | None = "sha256:e37ae3673a996e386be0c909973484f73a0ec84b409dcd75b78746645629d4e2"
_CANONICAL_RECONCILIATION_278_HASH: str | None = "sha256:69e4ad03b5b59474b6827b7c623c14c4058728b9f25e9d8bd3284796eff64c64"

_CHALLENGE_RULES_277 = {
    "operator_reply_must_equal_short_approval_reply": True,
    "refresh_challenge_hash_binds_request_hash_operator_identity_nonce_window_and_denials": True,
    "expired_prior_challenge_required": True,
    "unbound_approve_is_not_authority": True,
    "expired_refresh_challenge_is_not_authority": True,
    "future_execution_requires_separate_package": True,
    "no_execution_or_run_id_side_effects": True,
}

_SIDE_EFFECTS_276 = dict(_SIDE_EFFECTS_274_BLOCKED)
_SIDE_EFFECTS_276["expired_approve_attempt_recorded"] = True
_SIDE_EFFECTS_276["refresh_challenge_issued"] = False
_SIDE_EFFECTS_276["refresh_challenge_reconciled"] = False
_SIDE_EFFECTS_277 = dict(_SIDE_EFFECTS_276)
_SIDE_EFFECTS_277["refresh_challenge_issued"] = True
_SIDE_EFFECTS_278 = dict(_SIDE_EFFECTS_277)
_SIDE_EFFECTS_278["refresh_challenge_reconciled"] = True

_ALLOWED_EXPIRED_ATTEMPT_KEYS = {
    "sprint", "status", "markers", "request_hash", "challenge_hash", "expired_preflight_hash",
    "operator_identity", "operator_reply_hash", "operator_reply_status", "challenge_issued_at",
    "challenge_expires_at", "evaluated_at", "evaluation_result", "denied_authorities", "side_effects",
    "expired_attempt_hash",
}
_ALLOWED_REFRESH_CHALLENGE_KEYS = {
    "sprint", "status", "markers", "request_hash", "previous_challenge_hash", "expired_attempt_hash",
    "operator_identity", "challenge_nonce", "issued_at", "expires_at", "short_approval_reply",
    "challenge_scope", "challenge_rules", "challenge_payload_hash", "denied_authorities", "side_effects",
    "refresh_challenge_hash",
}
_ALLOWED_RECONCILIATION_KEYS = {
    "sprint", "status", "markers", "request_hash", "previous_challenge_hash", "expired_attempt_hash",
    "refresh_challenge_hash", "reconciled_state", "next_frontier", "denied_authorities", "side_effects",
    "reconciliation_hash",
}


def record_expired_rtm_blk_link_drift_coverage_approve_attempt_276(
    challenge_package_273: dict[str, Any],
    *,
    operator_reply: str,
    operator_identity: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Record that ``Approve`` arrived after BLK-SYSTEM-273 expired; do not approve."""

    try:
        challenge = _validate_challenge_273(challenge_package_273)
        preflight = evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply=operator_reply,
            operator_identity=operator_identity,
            evaluated_at=evaluated_at,
        )
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(str(exc)) from exc
    if preflight["operator_reply_status"] != "EXPIRED_CHALLENGE_NOT_APPROVAL":
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
            "expired challenge approval attempt requires EXPIRED_CHALLENGE_NOT_APPROVAL"
        )
    package = {
        "sprint": "BLK-SYSTEM-276",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED_NOT_APPROVAL",
        "markers": [
            "BLK_SYSTEM_276_RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED",
            "EXPIRED_CHALLENGE_NOT_APPROVAL",
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": challenge["request_hash"],
        "challenge_hash": challenge["challenge_hash"],
        "expired_preflight_hash": preflight["preflight_hash"],
        "operator_identity": operator_identity,
        "operator_reply_hash": preflight["operator_reply_hash"],
        "operator_reply_status": preflight["operator_reply_status"],
        "challenge_issued_at": preflight["challenge_issued_at"],
        "challenge_expires_at": preflight["challenge_expires_at"],
        "evaluated_at": evaluated_at,
        "evaluation_result": preflight["evaluation_result"],
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_276),
    }
    package["expired_attempt_hash"] = _hash_package(package)
    _validate_expired_attempt_276(package)
    return _deepcopy(package)


def build_rtm_blk_link_drift_coverage_refresh_challenge_277(
    expired_attempt_276: dict[str, Any],
    *,
    operator_identity: str,
    challenge_nonce: str,
    issued_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Emit a fresh bounded short-Approve challenge after the prior challenge expired."""

    expired_attempt = _validate_expired_attempt_276(expired_attempt_276)
    if operator_identity != EXPECTED_OPERATOR_IDENTITY_264 or operator_identity != expired_attempt["operator_identity"]:
        _reject_freeform_laundering(operator_identity, "operator_identity")
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("operator_identity mismatch for BLK-SYSTEM-277")
    try:
        _require_safe_nonce(challenge_nonce)
        _require_window(issued_at, expires_at, "issued_at", "expires_at")
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(str(exc)) from exc
    previous_expiry = _parse_timezone_timestamp(expired_attempt["challenge_expires_at"], "challenge_expires_at")
    issued = _parse_timezone_timestamp(issued_at, "issued_at")
    if issued <= previous_expiry:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
            "issued_at must be after previous challenge expiry"
        )
    _require_timestamp_order(
        expired_attempt["evaluated_at"],
        issued_at,
        "expired attempt evaluated_at",
        "issued_at",
        allow_equal=True,
    )

    challenge_payload_hash = _hash_package(
        {
            "request_hash": expired_attempt["request_hash"],
            "previous_challenge_hash": expired_attempt["challenge_hash"],
            "expired_attempt_hash": expired_attempt["expired_attempt_hash"],
            "operator_identity": operator_identity,
            "challenge_nonce": challenge_nonce,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "short_approval_reply": _SHORT_APPROVAL_REPLY,
            "challenge_scope": _REFRESH_CHALLENGE_SCOPE_277,
            "denied_authorities": list(_DENIED_AUTHORITIES),
        }
    )
    package = {
        "sprint": "BLK-SYSTEM-277",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        "markers": [
            "BLK_SYSTEM_277_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY",
            "SHORT_APPROVE_BOUND_TO_REFRESH_CHALLENGE_HASH",
            "NO_RUN_ID_OR_EXECUTION",
        ],
        "request_hash": expired_attempt["request_hash"],
        "previous_challenge_hash": expired_attempt["challenge_hash"],
        "expired_attempt_hash": expired_attempt["expired_attempt_hash"],
        "operator_identity": operator_identity,
        "challenge_nonce": challenge_nonce,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "short_approval_reply": _SHORT_APPROVAL_REPLY,
        "challenge_scope": _REFRESH_CHALLENGE_SCOPE_277,
        "challenge_rules": dict(_CHALLENGE_RULES_277),
        "challenge_payload_hash": challenge_payload_hash,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_277),
    }
    package["refresh_challenge_hash"] = _hash_package(package)
    _validate_refresh_challenge_277(package, expired_attempt["expired_attempt_hash"])
    return _deepcopy(package)


def reconcile_rtm_blk_link_drift_coverage_refresh_challenge_278(
    refresh_challenge_277: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile the refreshed challenge to approval-required/not-granted."""

    challenge = _validate_refresh_challenge_277(refresh_challenge_277)
    package = {
        "sprint": "BLK-SYSTEM-278",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_278_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED",
            _NEXT_FRONTIER_278,
            "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
        ],
        "request_hash": challenge["request_hash"],
        "previous_challenge_hash": challenge["previous_challenge_hash"],
        "expired_attempt_hash": challenge["expired_attempt_hash"],
        "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        "reconciled_state": _RECONCILED_STATE_278,
        "next_frontier": _NEXT_FRONTIER_278,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_278),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_reconciliation_278(package, challenge["refresh_challenge_hash"])
    return _deepcopy(package)


def _validate_expired_attempt_276(package: dict[str, Any]) -> dict[str, Any]:
    try:
        _require_allowed_keys(package, _ALLOWED_EXPIRED_ATTEMPT_KEYS, "expired attempt package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED_NOT_APPROVAL",
            "expired attempt package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_276_RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED",
                "EXPIRED_CHALLENGE_NOT_APPROVAL",
                "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
            ],
            "expired attempt package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "expired attempt package canonical BLK-SYSTEM-272 hash mismatch"
            )
        if package.get("challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "expired attempt package canonical BLK-SYSTEM-273 hash mismatch"
            )
        if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package operator_identity mismatch")
        _require_hash(package, "expired_preflight_hash", "expired attempt package")
        _require_hash(package, "operator_reply_hash", "expired attempt package")
        if package.get("operator_reply_hash") != _hash_text(_SHORT_APPROVAL_REPLY):
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package operator_reply_hash mismatch")
        if package.get("operator_reply_status") != "EXPIRED_CHALLENGE_NOT_APPROVAL":
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package operator_reply_status mismatch")
        if package.get("evaluation_result") != _EXPIRED_BLOCKED_RESULT_274:
            _reject_freeform_laundering(package.get("evaluation_result"), "expired attempt package evaluation_result")
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package evaluation_result mismatch")
        _require_timestamp_order(
            package.get("challenge_issued_at"),
            package.get("challenge_expires_at"),
            "challenge_issued_at",
            "challenge_expires_at",
        )
        _require_timestamp_order(
            package.get("challenge_expires_at"),
            package.get("evaluated_at"),
            "challenge_expires_at",
            "evaluated_at",
            allow_equal=True,
        )
        _require_denials(package, "expired attempt package")
        _require_side_effects(package, _SIDE_EFFECTS_276, "expired attempt package")
        _require_hash(package, "expired_attempt_hash", "expired attempt package")
    except _RequestPackageError as exc:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(str(exc)) from exc
    if package.get("expired_attempt_hash") != _hash_package({key: value for key, value in package.items() if key != "expired_attempt_hash"}):
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package expired_attempt_hash mismatch")
    if _CANONICAL_EXPIRED_ATTEMPT_276_HASH and package.get("expired_attempt_hash") != _CANONICAL_EXPIRED_ATTEMPT_276_HASH:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("expired attempt package canonical BLK-SYSTEM-276 hash mismatch")
    return package


def _validate_refresh_challenge_277(
    package: dict[str, Any],
    expected_expired_attempt_hash: str | None = None,
) -> dict[str, Any]:
    try:
        _require_allowed_keys(package, _ALLOWED_REFRESH_CHALLENGE_KEYS, "refresh challenge package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
            "refresh challenge package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_277_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY",
                "SHORT_APPROVE_BOUND_TO_REFRESH_CHALLENGE_HASH",
                "NO_RUN_ID_OR_EXECUTION",
            ],
            "refresh challenge package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh challenge package canonical BLK-SYSTEM-272 hash mismatch"
            )
        if package.get("previous_challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh challenge package canonical BLK-SYSTEM-273 hash mismatch"
            )
        if expected_expired_attempt_hash and package.get("expired_attempt_hash") != expected_expired_attempt_hash:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package expired_attempt_hash mismatch")
        if _CANONICAL_EXPIRED_ATTEMPT_276_HASH and package.get("expired_attempt_hash") != _CANONICAL_EXPIRED_ATTEMPT_276_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package canonical BLK-SYSTEM-276 hash mismatch")
        if package.get("operator_identity") != EXPECTED_OPERATOR_IDENTITY_264:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package operator_identity mismatch")
        _require_safe_nonce(package.get("challenge_nonce"))
        _require_window(package.get("issued_at"), package.get("expires_at"), "issued_at", "expires_at")
        if package.get("short_approval_reply") != _SHORT_APPROVAL_REPLY:
            _reject_freeform_laundering(package.get("short_approval_reply"), "refresh challenge package short_approval_reply")
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package short_approval_reply mismatch")
        if package.get("challenge_scope") != _REFRESH_CHALLENGE_SCOPE_277:
            _reject_freeform_laundering(package.get("challenge_scope"), "refresh challenge package challenge_scope")
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package challenge_scope mismatch")
        if package.get("challenge_rules") != _CHALLENGE_RULES_277:
            _reject_freeform_laundering(package.get("challenge_rules"), "refresh challenge package challenge_rules")
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package challenge_rules mismatch")
        expected_payload_hash = _hash_package(
            {
                "request_hash": package["request_hash"],
                "previous_challenge_hash": package["previous_challenge_hash"],
                "expired_attempt_hash": package["expired_attempt_hash"],
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
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package challenge_payload_hash mismatch")
        _require_denials(package, "refresh challenge package")
        _require_side_effects(package, _SIDE_EFFECTS_277, "refresh challenge package")
        _require_hash(package, "refresh_challenge_hash", "refresh challenge package")
    except _RequestPackageError as exc:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(str(exc)) from exc
    if package.get("refresh_challenge_hash") != _hash_package({key: value for key, value in package.items() if key != "refresh_challenge_hash"}):
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package refresh_challenge_hash mismatch")
    if _CANONICAL_REFRESH_CHALLENGE_277_HASH and package.get("refresh_challenge_hash") != _CANONICAL_REFRESH_CHALLENGE_277_HASH:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh challenge package canonical BLK-SYSTEM-277 hash mismatch")
    return package


def _validate_reconciliation_278(package: dict[str, Any], expected_refresh_challenge_hash: str | None = None) -> None:
    try:
        _require_allowed_keys(package, _ALLOWED_RECONCILIATION_KEYS, "refresh reconciliation package")
        _require_status(
            package,
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
            "refresh reconciliation package",
        )
        _require_markers(
            package,
            [
                "BLK_SYSTEM_278_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED",
                _NEXT_FRONTIER_278,
                "NO_RTM_BLK_LINK_PROTECTED_BODY_OR_MUTATION",
            ],
            "refresh reconciliation package",
        )
        if package.get("request_hash") != _CANONICAL_REQUEST_272_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh reconciliation package canonical BLK-SYSTEM-272 hash mismatch"
            )
        if package.get("previous_challenge_hash") != _CANONICAL_CHALLENGE_273_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh reconciliation package canonical BLK-SYSTEM-273 hash mismatch"
            )
        if _CANONICAL_EXPIRED_ATTEMPT_276_HASH and package.get("expired_attempt_hash") != _CANONICAL_EXPIRED_ATTEMPT_276_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh reconciliation package canonical BLK-SYSTEM-276 hash mismatch"
            )
        if expected_refresh_challenge_hash and package.get("refresh_challenge_hash") != expected_refresh_challenge_hash:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh reconciliation package refresh_challenge_hash mismatch")
        if _CANONICAL_REFRESH_CHALLENGE_277_HASH and package.get("refresh_challenge_hash") != _CANONICAL_REFRESH_CHALLENGE_277_HASH:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(
                "refresh reconciliation package canonical BLK-SYSTEM-277 hash mismatch"
            )
        if package.get("reconciled_state") != _RECONCILED_STATE_278:
            _reject_freeform_laundering(package.get("reconciled_state"), "refresh reconciliation package reconciled_state")
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh reconciliation package reconciled_state mismatch")
        if package.get("next_frontier") != _NEXT_FRONTIER_278:
            raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh reconciliation package next_frontier mismatch")
        _require_denials(package, "refresh reconciliation package")
        _require_side_effects(package, _SIDE_EFFECTS_278, "refresh reconciliation package")
        _require_hash(package, "reconciliation_hash", "refresh reconciliation package")
    except _RequestPackageError as exc:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError(str(exc)) from exc
    if package.get("reconciliation_hash") != _hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}):
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh reconciliation package reconciliation_hash mismatch")
    if _CANONICAL_RECONCILIATION_278_HASH and package.get("reconciliation_hash") != _CANONICAL_RECONCILIATION_278_HASH:
        raise RtmBlkLinkDriftCoverageRefreshChallengeValidationError("refresh reconciliation package canonical BLK-SYSTEM-278 hash mismatch")


def _clone(value: Any) -> Any:
    return deepcopy(value)
