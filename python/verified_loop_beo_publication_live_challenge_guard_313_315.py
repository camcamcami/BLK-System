"""BLK-SYSTEM-313..315 live refreshed BEO challenge non-approval guard.

The refreshed BLK-SYSTEM-311 short-``Approve`` challenge is live. A generic
operator directive sent during that live window is not approval and must not be
laundered into approval capture, run-ID movement, BEO closeout, publication,
signer/storage/ledger action, RTM, ``blk-link``, protected-body access,
runtime/tooling, or target/source/Git mutation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from verified_loop_beo_publication_approval_request_306_309 import (
    _DENIED_AUTHORITIES,
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _parse_timestamp,
    _require_allowed_keys,
    _require_ascii_string,
    _require_denied_authorities,
    _require_hash,
    _require_hash_field,
    _require_operator_discord_id,
    _require_side_effects,
    hash_package,
)
from verified_loop_beo_publication_refresh_challenge_310_312 import (
    EXPECTED_310_EXPIRED_ATTEMPT_HASH,
    EXPECTED_311_REFRESH_CHALLENGE_HASH,
    EXPECTED_312_RECONCILIATION_HASH,
    NEXT_FRONTIER_312,
    VerifiedLoopBeoPublicationRefreshChallengeValidationError,
    validate_verified_loop_beo_publication_refreshed_approval_challenge_311,
    validate_verified_loop_beo_publication_refreshed_challenge_reconciliation_312,
)


class VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(ValueError):
    """Raised when BLK-SYSTEM-313..315 live challenge guard evidence is unsafe."""


EXPECTED_313_LIVE_DIRECTIVE_HASH: str | None = "sha256:cbb7e08f7706289f353302d97a13578f9e05ae5628ce74d8242d4eb14bced942"
EXPECTED_314_SHORT_APPROVE_GUARD_HASH: str | None = "sha256:d4738258e0e9580144f3254f915ff799165169ac781de21eec6e960848b49101"
EXPECTED_315_RECONCILIATION_HASH: str | None = "sha256:a120abbca3e6226d27bc26241234fc811a880c568d51456343183370237a243c"
NEXT_FRONTIER_315 = NEXT_FRONTIER_312

_LIVE_DIRECTIVE_CLASSIFICATION_313 = "live_generic_sprint_directive_not_approval"
_GUARD_RESULT_314 = "NO_EXACT_SHORT_APPROVE_MATCH"
_RECONCILED_STATE_315 = "live_refreshed_challenge_non_approval_reconciled_approval_required"

_MARKERS_313 = (
    "BLK_SYSTEM_313_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED",
    "LIVE_GENERIC_OPERATOR_DIRECTIVE_NOT_APPROVAL",
    "NO_APPROVAL_CAPTURE_OR_CHALLENGE_CONSUMPTION",
)
_MARKERS_314 = (
    "BLK_SYSTEM_314_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_SHORT_APPROVE_GUARD_READY",
    "ONLY_EXACT_SHORT_APPROVE_CAN_FEED_FUTURE_CAPTURE_PACKAGE",
    "NO_APPROVAL_CAPTURE_OR_CHALLENGE_CONSUMPTION",
)
_MARKERS_315 = (
    "BLK_SYSTEM_315_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED",
    NEXT_FRONTIER_315,
    "NO_APPROVAL_CAPTURE_OR_CHALLENGE_CONSUMPTION",
)

_SIDE_EFFECTS_313 = {
    "live_unbound_directive_recorded": True,
    "short_approve_guard_evaluated": False,
    "live_non_approval_reconciled": False,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_314 = {
    "live_unbound_directive_recorded": True,
    "short_approve_guard_evaluated": True,
    "live_non_approval_reconciled": False,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_315 = {
    "live_unbound_directive_recorded": True,
    "short_approve_guard_evaluated": True,
    "live_non_approval_reconciled": True,
    **_FALSE_SIDE_EFFECTS,
}

_KEYS_313 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "expired_attempt_hash",
        "refresh_challenge_hash",
        "refresh_reconciliation_hash",
        "operator_identity",
        "operator_statement_hash",
        "operator_statement_classification",
        "observed_at",
        "challenge_issued_at",
        "challenge_expires_at",
        "required_short_approval_reply_hash",
        "statement_matches_short_approve",
        "challenge_remains_live",
        "denied_authorities",
        "side_effects",
        "live_directive_hash",
    }
)
_KEYS_314 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "expired_attempt_hash",
        "refresh_challenge_hash",
        "refresh_reconciliation_hash",
        "live_directive_hash",
        "operator_identity",
        "observed_at",
        "challenge_issued_at",
        "challenge_expires_at",
        "required_short_approval_reply_hash",
        "statement_matches_short_approve",
        "guard_result",
        "capture_allowed",
        "future_capture_package_required",
        "challenge_remains_live",
        "denied_authorities",
        "side_effects",
        "short_approve_guard_hash",
    }
)
_KEYS_315 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "expired_attempt_hash",
        "refresh_challenge_hash",
        "refresh_reconciliation_hash",
        "live_directive_hash",
        "short_approve_guard_hash",
        "reconciled_state",
        "next_frontier",
        "capture_allowed",
        "challenge_remains_live",
        "denied_authorities",
        "side_effects",
        "reconciliation_hash",
    }
)


def _translate_error(exc: Exception) -> VerifiedLoopBeoPublicationLiveChallengeGuardValidationError:
    return VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(str(exc))


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(f"{context} must be a dictionary")
    return value


def _require_operator_identity(value: Any) -> dict[str, str]:
    identity = _require_dict(value, "operator_identity")
    try:
        _require_allowed_keys(identity, frozenset({"platform", "discord_user_id"}), "operator_identity")
        if identity.get("platform") != "discord":
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("operator platform mismatch")
        _require_operator_discord_id(identity.get("discord_user_id"))
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    return deepcopy(identity)


def _require_discord_operator(value: Any) -> str:
    try:
        return _require_operator_discord_id(value)
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc


def _require_expected_hash(package: dict[str, Any], field: str, expected: str | None, context: str) -> None:
    try:
        _require_hash_field(package, field, context)
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    if expected is not None and package[field] != expected:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(f"{context} canonical hash mismatch")


def _require_live_observation_window(challenge: dict[str, Any], observed_at: Any) -> None:
    try:
        observed = _parse_timestamp(observed_at, "observed_at")
        issued = _parse_timestamp(challenge["issued_at"], "challenge_issued_at")
        expires = _parse_timestamp(challenge["expires_at"], "challenge_expires_at")
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    if observed < issued:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("refreshed approval challenge not yet live")
    if observed >= expires:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("refreshed approval challenge no longer live")


def _scan_operator_statement(operator_statement: Any) -> str:
    try:
        statement = _require_ascii_string(operator_statement, "operator_statement")
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    if not statement.strip():
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("operator_statement must be non-empty")
    if statement == "Approve":
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(
            "live bound Approve must use the approval-capture package"
        )
    findings = scan_for_authority_laundering(statement, "operator_statement", _DENIED_AUTHORITIES)
    if findings:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("; ".join(findings))
    return statement


def record_live_verified_loop_beo_publication_non_approval_directive_313(
    refresh_challenge_311: dict[str, Any],
    reconciliation_312: dict[str, Any],
    *,
    operator_statement: str,
    operator_discord_id: str,
    observed_at: str,
) -> dict[str, Any]:
    """Record a live generic directive as non-approval for the refreshed challenge."""

    try:
        challenge = validate_verified_loop_beo_publication_refreshed_approval_challenge_311(refresh_challenge_311)
        reconciliation = validate_verified_loop_beo_publication_refreshed_challenge_reconciliation_312(
            reconciliation_312,
            challenge,
        )
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    if reconciliation["refresh_challenge_hash"] != challenge["refresh_challenge_hash"]:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("challenge/reconciliation binding mismatch")
    operator_id = _require_discord_operator(operator_discord_id)
    if operator_id != challenge["operator_identity"]["discord_user_id"]:
        raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError("operator identity mismatch")
    statement = _scan_operator_statement(operator_statement)
    _require_live_observation_window(challenge, observed_at)

    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED_NOT_APPROVAL",
        "markers": list(_MARKERS_313),
        "approval_request_hash": challenge["approval_request_hash"],
        "expired_attempt_hash": challenge["expired_attempt_hash"],
        "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        "refresh_reconciliation_hash": reconciliation["reconciliation_hash"],
        "operator_identity": deepcopy(challenge["operator_identity"]),
        "operator_statement_hash": _hash_text(statement),
        "operator_statement_classification": _LIVE_DIRECTIVE_CLASSIFICATION_313,
        "observed_at": observed_at,
        "challenge_issued_at": challenge["issued_at"],
        "challenge_expires_at": challenge["expires_at"],
        "required_short_approval_reply_hash": challenge["short_approval_reply_hash"],
        "statement_matches_short_approve": False,
        "challenge_remains_live": True,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_313),
    }
    package["live_directive_hash"] = hash_package(package)
    return validate_live_verified_loop_beo_publication_non_approval_directive_313(package)


def validate_live_verified_loop_beo_publication_non_approval_directive_313(
    directive_313: dict[str, Any],
) -> dict[str, Any]:
    directive = _require_dict(directive_313, "live non-approval directive")
    try:
        _require_allowed_keys(directive, _KEYS_313, "live non-approval directive")
        if directive.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED_NOT_APPROVAL":
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("live non-approval directive status mismatch")
        if tuple(directive.get("markers", ())) != _MARKERS_313:
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("live non-approval directive markers mismatch")
        expected = {
            "expired_attempt_hash": EXPECTED_310_EXPIRED_ATTEMPT_HASH,
            "refresh_challenge_hash": EXPECTED_311_REFRESH_CHALLENGE_HASH,
            "refresh_reconciliation_hash": EXPECTED_312_RECONCILIATION_HASH,
            "operator_statement_classification": _LIVE_DIRECTIVE_CLASSIFICATION_313,
            "challenge_issued_at": "2026-05-21T14:45:00+10:00",
            "challenge_expires_at": "2026-05-21T20:45:00+10:00",
            "required_short_approval_reply_hash": _hash_text("Approve"),
        }
        for field, value in expected.items():
            if directive.get(field) != value:
                raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(
                    f"live non-approval directive {field} mismatch"
                )
        if directive.get("statement_matches_short_approve") is not False:
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("statement match must remain false")
        if directive.get("challenge_remains_live") is not True:
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("challenge must remain live")
        _require_hash(directive.get("operator_statement_hash"), "operator_statement_hash")
        _require_denied_authorities(directive.get("denied_authorities"), "live non-approval directive")
        _require_side_effects(directive.get("side_effects"), _SIDE_EFFECTS_313, "live non-approval directive")
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    _require_operator_identity(directive.get("operator_identity"))
    _require_live_observation_window(
        {
            "issued_at": directive["challenge_issued_at"],
            "expires_at": directive["challenge_expires_at"],
        },
        directive.get("observed_at"),
    )
    _require_expected_hash(directive, "live_directive_hash", EXPECTED_313_LIVE_DIRECTIVE_HASH, "live non-approval directive")
    return deepcopy(directive)


def build_verified_loop_beo_publication_live_short_approve_guard_314(
    directive_313: dict[str, Any],
    refresh_challenge_311: dict[str, Any],
) -> dict[str, Any]:
    """Build the exact-short-Approve guard result for a live non-approval directive."""

    directive = validate_live_verified_loop_beo_publication_non_approval_directive_313(directive_313)
    try:
        challenge = validate_verified_loop_beo_publication_refreshed_approval_challenge_311(refresh_challenge_311)
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    linked = {
        "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        "expired_attempt_hash": challenge["expired_attempt_hash"],
        "operator_identity": challenge["operator_identity"],
        "challenge_issued_at": challenge["issued_at"],
        "challenge_expires_at": challenge["expires_at"],
        "required_short_approval_reply_hash": challenge["short_approval_reply_hash"],
    }
    for field, value in linked.items():
        if directive.get(field) != value:
            raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(f"short Approve guard {field} mismatch")

    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_SHORT_APPROVE_GUARD_RECORDED_NOT_APPROVED",
        "markers": list(_MARKERS_314),
        "approval_request_hash": directive["approval_request_hash"],
        "expired_attempt_hash": directive["expired_attempt_hash"],
        "refresh_challenge_hash": directive["refresh_challenge_hash"],
        "refresh_reconciliation_hash": directive["refresh_reconciliation_hash"],
        "live_directive_hash": directive["live_directive_hash"],
        "operator_identity": deepcopy(directive["operator_identity"]),
        "observed_at": directive["observed_at"],
        "challenge_issued_at": directive["challenge_issued_at"],
        "challenge_expires_at": directive["challenge_expires_at"],
        "required_short_approval_reply_hash": directive["required_short_approval_reply_hash"],
        "statement_matches_short_approve": False,
        "guard_result": _GUARD_RESULT_314,
        "capture_allowed": False,
        "future_capture_package_required": True,
        "challenge_remains_live": True,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_314),
    }
    package["short_approve_guard_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_live_short_approve_guard_314(package, directive)


def validate_verified_loop_beo_publication_live_short_approve_guard_314(
    guard_314: dict[str, Any],
    directive_313: dict[str, Any] | None = None,
) -> dict[str, Any]:
    directive = None
    if directive_313 is not None:
        directive = validate_live_verified_loop_beo_publication_non_approval_directive_313(directive_313)
    guard = _require_dict(guard_314, "live short Approve guard")
    try:
        _require_allowed_keys(guard, _KEYS_314, "live short Approve guard")
        if guard.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_SHORT_APPROVE_GUARD_RECORDED_NOT_APPROVED":
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("short Approve guard status mismatch")
        if tuple(guard.get("markers", ())) != _MARKERS_314:
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("short Approve guard markers mismatch")
        expected = {
            "expired_attempt_hash": EXPECTED_310_EXPIRED_ATTEMPT_HASH,
            "refresh_challenge_hash": EXPECTED_311_REFRESH_CHALLENGE_HASH,
            "refresh_reconciliation_hash": EXPECTED_312_RECONCILIATION_HASH,
            "challenge_issued_at": "2026-05-21T14:45:00+10:00",
            "challenge_expires_at": "2026-05-21T20:45:00+10:00",
            "required_short_approval_reply_hash": _hash_text("Approve"),
            "statement_matches_short_approve": False,
            "guard_result": _GUARD_RESULT_314,
            "capture_allowed": False,
            "future_capture_package_required": True,
            "challenge_remains_live": True,
        }
        for field, value in expected.items():
            if guard.get(field) != value:
                raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(f"short Approve guard {field} mismatch")
        _require_denied_authorities(guard.get("denied_authorities"), "live short Approve guard")
        _require_side_effects(guard.get("side_effects"), _SIDE_EFFECTS_314, "live short Approve guard")
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    _require_operator_identity(guard.get("operator_identity"))
    _require_live_observation_window(
        {"issued_at": guard["challenge_issued_at"], "expires_at": guard["challenge_expires_at"]},
        guard.get("observed_at"),
    )
    if directive is not None:
        linked = {
            "live_directive_hash": directive["live_directive_hash"],
            "operator_identity": directive["operator_identity"],
            "observed_at": directive["observed_at"],
        }
        for field, value in linked.items():
            if guard.get(field) != value:
                raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(f"short Approve guard {field} mismatch")
    _require_expected_hash(guard, "short_approve_guard_hash", EXPECTED_314_SHORT_APPROVE_GUARD_HASH, "live short Approve guard")
    return deepcopy(guard)


def reconcile_verified_loop_beo_publication_live_challenge_guard_315(
    guard_314: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile a live non-approval guard back to the same bound-Approve frontier."""

    guard = validate_verified_loop_beo_publication_live_short_approve_guard_314(guard_314)
    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED_APPROVAL_REQUIRED",
        "markers": list(_MARKERS_315),
        "approval_request_hash": guard["approval_request_hash"],
        "expired_attempt_hash": guard["expired_attempt_hash"],
        "refresh_challenge_hash": guard["refresh_challenge_hash"],
        "refresh_reconciliation_hash": guard["refresh_reconciliation_hash"],
        "live_directive_hash": guard["live_directive_hash"],
        "short_approve_guard_hash": guard["short_approve_guard_hash"],
        "reconciled_state": _RECONCILED_STATE_315,
        "next_frontier": NEXT_FRONTIER_315,
        "capture_allowed": False,
        "challenge_remains_live": True,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_315),
    }
    package["reconciliation_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_live_challenge_guard_reconciliation_315(package, guard)


def validate_verified_loop_beo_publication_live_challenge_guard_reconciliation_315(
    reconciliation_315: dict[str, Any],
    guard_314: dict[str, Any] | None = None,
) -> dict[str, Any]:
    guard = None
    if guard_314 is not None:
        guard = validate_verified_loop_beo_publication_live_short_approve_guard_314(guard_314)
    reconciliation = _require_dict(reconciliation_315, "live challenge guard reconciliation")
    try:
        _require_allowed_keys(reconciliation, _KEYS_315, "live challenge guard reconciliation")
        if reconciliation.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED_APPROVAL_REQUIRED":
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("live challenge guard reconciliation status mismatch")
        if tuple(reconciliation.get("markers", ())) != _MARKERS_315:
            raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("live challenge guard reconciliation markers mismatch")
        expected = {
            "expired_attempt_hash": EXPECTED_310_EXPIRED_ATTEMPT_HASH,
            "refresh_challenge_hash": EXPECTED_311_REFRESH_CHALLENGE_HASH,
            "refresh_reconciliation_hash": EXPECTED_312_RECONCILIATION_HASH,
            "reconciled_state": _RECONCILED_STATE_315,
            "next_frontier": NEXT_FRONTIER_315,
            "capture_allowed": False,
            "challenge_remains_live": True,
        }
        for field, value in expected.items():
            if reconciliation.get(field) != value:
                raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(
                    f"live challenge guard reconciliation {field} mismatch"
                )
        _require_denied_authorities(reconciliation.get("denied_authorities"), "live challenge guard reconciliation")
        _require_side_effects(reconciliation.get("side_effects"), _SIDE_EFFECTS_315, "live challenge guard reconciliation")
    except VerifiedLoopBeoPublicationRefreshChallengeValidationError as exc:
        raise _translate_error(exc) from exc
    if guard is not None:
        linked = {
            "live_directive_hash": guard["live_directive_hash"],
            "short_approve_guard_hash": guard["short_approve_guard_hash"],
        }
        for field, value in linked.items():
            if reconciliation.get(field) != value:
                raise VerifiedLoopBeoPublicationLiveChallengeGuardValidationError(
                    f"live challenge guard reconciliation {field} mismatch"
                )
    _require_expected_hash(
        reconciliation,
        "reconciliation_hash",
        EXPECTED_315_RECONCILIATION_HASH,
        "live challenge guard reconciliation",
    )
    return deepcopy(reconciliation)
