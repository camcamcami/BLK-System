"""BLK-SYSTEM-310..312 verified-loop BEO approval refresh challenge.

The BLK-SYSTEM-306..309 short-``Approve`` challenge expired before any exact
operator approval was captured. This grouped package records the latest generic
operator sprint directive as non-approval, emits a fresh bounded short-``Approve``
challenge, and reconciles back to approval-required/not-granted.

It does not capture approval, reserve or consume a run ID, execute BEO closeout,
publish a BEO, reuse signer/storage/ledger authority, generate RTM, run
production blk-link, read protected bodies, start tooling, or mutate
target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_306_APPROVAL_REQUEST_HASH,
    EXPECTED_306_CHALLENGE_HASH,
    EXPECTED_306_EXPIRES_AT,
    EXPECTED_306_REQUESTED_AT,
    EXPECTED_307_CONTRACT_HASH,
    EXPECTED_308_CHALLENGE_RECORD_HASH,
    EXPECTED_309_RECONCILIATION_HASH,
    EXPECTED_OPERATOR_DISCORD_ID,
    NEXT_FRONTIER_309,
    VerifiedLoopBeoPublicationApprovalRequestValidationError,
    _DECISION_WINDOW_KEYS,
    _DENIED_AUTHORITIES,
    _FALSE_SIDE_EFFECTS,
    _KEYS_308,
    _KEYS_309,
    _MARKERS_308,
    _MARKERS_309,
    _SIDE_EFFECTS_308,
    _SIDE_EFFECTS_309,
    _deepcopy,
    _hash_text,
    _parse_timestamp,
    _require_allowed_keys,
    _require_ascii_string,
    _require_denied_authorities,
    _require_exact_id,
    _require_exact_value,
    _require_hash,
    _require_hash_field,
    _require_operator_discord_id,
    _require_side_effects,
    hash_package,
)


class VerifiedLoopBeoPublicationRefreshChallengeValidationError(ValueError):
    """Raised when BLK-SYSTEM-310..312 refresh evidence is unsafe."""


EXPECTED_310_EXPIRED_ATTEMPT_HASH: str | None = "sha256:40279079760ad5513de916b53bd306abd2ecf3cd7bae97d2b2e79e53c25ecc92"
EXPECTED_311_REFRESH_CHALLENGE_HASH: str | None = "sha256:778d72563994ca8e32ae23f947abbe29c60457f374e953195adc1a9fe5707af4"
EXPECTED_312_RECONCILIATION_HASH: str | None = "sha256:ea1b859b7f13ea1ea55c254478e121d8f7969069e632134e6a2ddaff1ffd1a96"
EXPECTED_311_REFRESH_NONCE = "BEO-APPROVAL-REFRESH-NONCE-BLK-SYSTEM-311-001"
NEXT_FRONTIER_312 = "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED"

_REFRESH_CHALLENGE_SCOPE_311 = "refresh_short_approve_after_expired_verified_loop_beo_approval_challenge_no_execution"
_RECONCILED_STATE_312 = "verified_loop_beo_publication_refresh_challenge_ready_approval_required_not_granted"
_OPERATOR_STATEMENT_STATUS_310 = "EXPIRED_OR_UNBOUND_DIRECTIVE_NOT_APPROVAL"
_OPERATOR_STATEMENT_CLASSIFICATION_310 = "generic_sprint_directive_hash_only_not_approval"
_MAX_REFRESH_WINDOW_SECONDS = 8 * 60 * 60

_MARKERS_310 = (
    "BLK_SYSTEM_310_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
    "EXPIRED_OR_UNBOUND_OPERATOR_DIRECTIVE_NOT_APPROVAL",
    "NO_BEO_PUBLICATION_OR_RUN_ID",
)
_MARKERS_311 = (
    "BLK_SYSTEM_311_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY",
    "SHORT_APPROVE_BOUND_TO_REFRESH_CHALLENGE_HASH",
    "NO_BEO_PUBLICATION_OR_RUN_ID",
)
_MARKERS_312 = (
    "BLK_SYSTEM_312_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED",
    NEXT_FRONTIER_312,
    "NO_BEO_PUBLICATION_OR_RUN_ID",
)

_CHALLENGE_RULES_311 = {
    "operator_reply_must_equal_short_approval_reply": True,
    "refresh_challenge_hash_binds_prior_request_operator_nonce_window_and_denials": True,
    "expired_prior_challenge_required": True,
    "generic_or_unbound_operator_directive_is_not_authority": True,
    "future_capture_execution_package_required": True,
    "no_execution_or_run_id_side_effects": True,
}

_SIDE_EFFECTS_310 = {
    "expired_or_unbound_attempt_recorded": True,
    "refresh_challenge_issued": False,
    "refresh_challenge_reconciled": False,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_311 = {
    "expired_or_unbound_attempt_recorded": True,
    "refresh_challenge_issued": True,
    "refresh_challenge_reconciled": False,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_312 = {
    "expired_or_unbound_attempt_recorded": True,
    "refresh_challenge_issued": True,
    "refresh_challenge_reconciled": True,
    **_FALSE_SIDE_EFFECTS,
}

_KEYS_310 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "contract_hash",
        "prior_challenge_hash",
        "prior_challenge_record_hash",
        "prior_reconciliation_hash",
        "operator_identity",
        "operator_statement_hash",
        "operator_statement_status",
        "operator_statement_classification",
        "prior_challenge_requested_at",
        "prior_challenge_expires_at",
        "evaluated_at",
        "evaluation_result",
        "denied_authorities",
        "side_effects",
        "expired_attempt_hash",
    }
)
_KEYS_311 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "prior_reconciliation_hash",
        "prior_challenge_record_hash",
        "prior_challenge_hash",
        "expired_attempt_hash",
        "operator_identity",
        "challenge_nonce",
        "issued_at",
        "expires_at",
        "short_approval_reply",
        "short_approval_reply_hash",
        "challenge_scope",
        "challenge_rules",
        "challenge_payload_hash",
        "denied_authorities",
        "side_effects",
        "refresh_challenge_hash",
    }
)
_KEYS_312 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "prior_reconciliation_hash",
        "prior_challenge_record_hash",
        "prior_challenge_hash",
        "expired_attempt_hash",
        "refresh_challenge_hash",
        "reconciled_state",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "reconciliation_hash",
    }
)


def _translate_error(exc: Exception) -> VerifiedLoopBeoPublicationRefreshChallengeValidationError:
    return VerifiedLoopBeoPublicationRefreshChallengeValidationError(str(exc))


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(f"{context} must be a dictionary")
    return value


def _require_operator_identity(value: Any) -> dict[str, str]:
    identity = _require_dict(value, "operator_identity")
    try:
        _require_allowed_keys(identity, frozenset({"platform", "discord_user_id"}), "operator_identity")
        if identity.get("platform") != "discord":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("operator platform mismatch")
        _require_operator_discord_id(identity.get("discord_user_id"))
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    return _deepcopy(identity)


def _require_discord_operator(value: Any) -> str:
    try:
        return _require_operator_discord_id(value)
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc


def _require_refresh_window(issued_at: Any, expires_at: Any) -> None:
    try:
        issued = _parse_timestamp(issued_at, "issued_at")
        expires = _parse_timestamp(expires_at, "expires_at")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    if expires <= issued:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("expires_at must be after issued_at")
    if (expires - issued).total_seconds() > _MAX_REFRESH_WINDOW_SECONDS:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("refresh window exceeds maximum TTL")


def _scan_statement(operator_statement: Any) -> str:
    statement = _require_ascii_string(operator_statement, "operator_statement")
    if not statement.strip():
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("operator_statement must be non-empty")
    findings = scan_for_authority_laundering(statement, "operator_statement")
    if findings:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("; ".join(findings))
    return statement


def _require_expected_hash(package: dict[str, Any], field: str, expected: str | None, context: str) -> None:
    try:
        _require_hash_field(package, field, context)
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    if expected is not None and package[field] != expected:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(f"{context} canonical hash mismatch")


def _validate_prior_challenge_record_308(challenge_record_308: dict[str, Any]) -> dict[str, Any]:
    record = _require_dict(challenge_record_308, "prior challenge record")
    try:
        _require_allowed_keys(record, _KEYS_308, "prior challenge record")
        if record.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED_NOT_APPROVED":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior challenge status mismatch")
        if tuple(record.get("markers", ())) != _MARKERS_308:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior challenge markers mismatch")
        expected = {
            "contract_hash": EXPECTED_307_CONTRACT_HASH,
            "approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
            "challenge_hash": EXPECTED_306_CHALLENGE_HASH,
            "required_reply_hash": _hash_text("Approve"),
        }
        for field, value in expected.items():
            if record.get(field) != value:
                raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"prior challenge {field} mismatch")
        if record.get("approval_state") != "PENDING_NOT_CAPTURED":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior challenge state mismatch")
        if record.get("approval_captured") is not False:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior challenge must not capture approval")
        if record.get("publication_execution_ready") is not False:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior challenge must not make publication ready")
        window = _require_dict(record.get("decision_window"), "decision_window")
        _require_allowed_keys(window, _DECISION_WINDOW_KEYS, "decision_window")
        if window != {"requested_at": EXPECTED_306_REQUESTED_AT, "expires_at": EXPECTED_306_EXPIRES_AT}:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior decision window mismatch")
        _require_side_effects(record.get("side_effects"), _SIDE_EFFECTS_308, "prior challenge")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    _require_operator_identity(record.get("operator_identity"))
    _require_expected_hash(record, "challenge_record_hash", EXPECTED_308_CHALLENGE_RECORD_HASH, "prior challenge")
    return _deepcopy(record)


def _validate_prior_reconciliation_309(reconciliation_309: dict[str, Any]) -> dict[str, Any]:
    reconciliation = _require_dict(reconciliation_309, "prior reconciliation")
    try:
        _require_allowed_keys(reconciliation, _KEYS_309, "prior reconciliation")
        if reconciliation.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior reconciliation status mismatch")
        if tuple(reconciliation.get("markers", ())) != _MARKERS_309:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("prior reconciliation markers mismatch")
        expected = {
            "contract_hash": EXPECTED_307_CONTRACT_HASH,
            "approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
            "challenge_record_hash": EXPECTED_308_CHALLENGE_RECORD_HASH,
            "challenge_hash": EXPECTED_306_CHALLENGE_HASH,
            "approval_state": "PENDING_NOT_CAPTURED",
            "reconciled_state": "verified_loop_beo_publication_approval_request_ready_not_granted",
            "next_frontier": NEXT_FRONTIER_309,
        }
        for field, value in expected.items():
            if reconciliation.get(field) != value:
                raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"prior reconciliation {field} mismatch")
        _require_side_effects(reconciliation.get("side_effects"), _SIDE_EFFECTS_309, "prior reconciliation")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    _require_expected_hash(reconciliation, "reconciliation_hash", EXPECTED_309_RECONCILIATION_HASH, "prior reconciliation")
    return _deepcopy(reconciliation)


def record_expired_verified_loop_beo_publication_approval_attempt_310(
    challenge_record_308: dict[str, Any],
    reconciliation_309: dict[str, Any],
    *,
    operator_statement: str,
    operator_discord_id: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Record the expired/unbound operator statement as non-approval."""

    challenge = _validate_prior_challenge_record_308(challenge_record_308)
    reconciliation = _validate_prior_reconciliation_309(reconciliation_309)
    if reconciliation["challenge_record_hash"] != challenge["challenge_record_hash"]:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("prior challenge/reconciliation binding mismatch")
    operator_id = _require_discord_operator(operator_discord_id)
    if operator_id != challenge["operator_identity"]["discord_user_id"]:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("operator identity mismatch")
    statement = _scan_statement(operator_statement)
    window = challenge["decision_window"]
    issued = _parse_timestamp(window["requested_at"], "prior_challenge_requested_at")
    expires = _parse_timestamp(window["expires_at"], "prior_challenge_expires_at")
    evaluated = _parse_timestamp(evaluated_at, "evaluated_at")
    if evaluated < issued:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("prior approval challenge not yet issued")
    if evaluated < expires:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(
            "prior approval challenge still live; use approval-capture package instead of refresh"
        )
    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL",
        "markers": list(_MARKERS_310),
        "approval_request_hash": reconciliation["approval_request_hash"],
        "contract_hash": reconciliation["contract_hash"],
        "prior_challenge_hash": challenge["challenge_hash"],
        "prior_challenge_record_hash": challenge["challenge_record_hash"],
        "prior_reconciliation_hash": reconciliation["reconciliation_hash"],
        "operator_identity": _deepcopy(challenge["operator_identity"]),
        "operator_statement_hash": _hash_text(statement),
        "operator_statement_status": _OPERATOR_STATEMENT_STATUS_310,
        "operator_statement_classification": _OPERATOR_STATEMENT_CLASSIFICATION_310,
        "prior_challenge_requested_at": window["requested_at"],
        "prior_challenge_expires_at": window["expires_at"],
        "evaluated_at": evaluated_at,
        "evaluation_result": "operator_statement_seen_after_challenge_expiry_is_not_approval",
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_310),
    }
    package["expired_attempt_hash"] = hash_package(package)
    return validate_expired_verified_loop_beo_publication_approval_attempt_310(package)


def validate_expired_verified_loop_beo_publication_approval_attempt_310(package_310: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_310, "expired approval attempt")
    try:
        _require_allowed_keys(package, _KEYS_310, "expired approval attempt")
        if package.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("expired approval attempt status mismatch")
        if tuple(package.get("markers", ())) != _MARKERS_310:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("expired approval attempt markers mismatch")
        expected = {
            "approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
            "contract_hash": EXPECTED_307_CONTRACT_HASH,
            "prior_challenge_hash": EXPECTED_306_CHALLENGE_HASH,
            "prior_challenge_record_hash": EXPECTED_308_CHALLENGE_RECORD_HASH,
            "prior_reconciliation_hash": EXPECTED_309_RECONCILIATION_HASH,
            "operator_statement_status": _OPERATOR_STATEMENT_STATUS_310,
            "operator_statement_classification": _OPERATOR_STATEMENT_CLASSIFICATION_310,
            "prior_challenge_requested_at": EXPECTED_306_REQUESTED_AT,
            "prior_challenge_expires_at": EXPECTED_306_EXPIRES_AT,
            "evaluation_result": "operator_statement_seen_after_challenge_expiry_is_not_approval",
        }
        for field, value in expected.items():
            if package.get(field) != value:
                raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"expired approval attempt {field} mismatch")
        _require_hash(package.get("operator_statement_hash"), "operator_statement_hash")
        _require_denied_authorities(package.get("denied_authorities"), "expired approval attempt")
        _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_310, "expired approval attempt")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    _require_operator_identity(package.get("operator_identity"))
    _require_expected_hash(package, "expired_attempt_hash", EXPECTED_310_EXPIRED_ATTEMPT_HASH, "expired approval attempt")
    return _deepcopy(package)


def build_verified_loop_beo_publication_refreshed_approval_challenge_311(
    expired_attempt_310: dict[str, Any],
    *,
    operator_discord_id: str,
    challenge_nonce: str,
    issued_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Emit a fresh bounded short-Approve challenge after the prior one expired."""

    expired = validate_expired_verified_loop_beo_publication_approval_attempt_310(expired_attempt_310)
    operator_id = _require_discord_operator(operator_discord_id)
    if operator_id != expired["operator_identity"]["discord_user_id"]:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("operator identity mismatch for refresh challenge")
    try:
        nonce = _require_exact_id(challenge_nonce, "BEO-APPROVAL-REFRESH-NONCE-", "challenge_nonce")
        _require_exact_value(nonce, EXPECTED_311_REFRESH_NONCE, "challenge_nonce")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    _require_refresh_window(issued_at, expires_at)
    prior_expiry = _parse_timestamp(expired["prior_challenge_expires_at"], "prior_challenge_expires_at")
    issued = _parse_timestamp(issued_at, "issued_at")
    evaluated = _parse_timestamp(expired["evaluated_at"], "expired attempt evaluated_at")
    if issued <= prior_expiry:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("issued_at must be after prior challenge expiry")
    if issued < evaluated:
        raise VerifiedLoopBeoPublicationRefreshChallengeValidationError("issued_at must not precede expired attempt evaluation")
    challenge_payload_hash = hash_package(
        {
            "approval_request_hash": expired["approval_request_hash"],
            "prior_reconciliation_hash": expired["prior_reconciliation_hash"],
            "prior_challenge_record_hash": expired["prior_challenge_record_hash"],
            "prior_challenge_hash": expired["prior_challenge_hash"],
            "expired_attempt_hash": expired["expired_attempt_hash"],
            "operator_identity": expired["operator_identity"],
            "challenge_nonce": nonce,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "short_approval_reply": "Approve",
            "short_approval_reply_hash": _hash_text("Approve"),
            "challenge_scope": _REFRESH_CHALLENGE_SCOPE_311,
            "denied_authorities": list(_DENIED_AUTHORITIES),
        }
    )
    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        "markers": list(_MARKERS_311),
        "approval_request_hash": expired["approval_request_hash"],
        "prior_reconciliation_hash": expired["prior_reconciliation_hash"],
        "prior_challenge_record_hash": expired["prior_challenge_record_hash"],
        "prior_challenge_hash": expired["prior_challenge_hash"],
        "expired_attempt_hash": expired["expired_attempt_hash"],
        "operator_identity": _deepcopy(expired["operator_identity"]),
        "challenge_nonce": nonce,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "short_approval_reply": "Approve",
        "short_approval_reply_hash": _hash_text("Approve"),
        "challenge_scope": _REFRESH_CHALLENGE_SCOPE_311,
        "challenge_rules": dict(_CHALLENGE_RULES_311),
        "challenge_payload_hash": challenge_payload_hash,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_311),
    }
    package["refresh_challenge_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_refreshed_approval_challenge_311(package, expired)


def validate_verified_loop_beo_publication_refreshed_approval_challenge_311(
    challenge_311: dict[str, Any],
    expired_attempt_310: dict[str, Any] | None = None,
) -> dict[str, Any]:
    expired = None
    if expired_attempt_310 is not None:
        expired = validate_expired_verified_loop_beo_publication_approval_attempt_310(expired_attempt_310)
    challenge = _require_dict(challenge_311, "refresh approval challenge")
    try:
        _require_allowed_keys(challenge, _KEYS_311, "refresh approval challenge")
        if challenge.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("refresh approval challenge status mismatch")
        if tuple(challenge.get("markers", ())) != _MARKERS_311:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("refresh approval challenge markers mismatch")
        expected = {
            "approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
            "prior_reconciliation_hash": EXPECTED_309_RECONCILIATION_HASH,
            "prior_challenge_record_hash": EXPECTED_308_CHALLENGE_RECORD_HASH,
            "prior_challenge_hash": EXPECTED_306_CHALLENGE_HASH,
            "short_approval_reply": "Approve",
            "short_approval_reply_hash": _hash_text("Approve"),
            "challenge_scope": _REFRESH_CHALLENGE_SCOPE_311,
            "challenge_rules": _CHALLENGE_RULES_311,
        }
        for field, value in expected.items():
            if challenge.get(field) != value:
                raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"refresh approval challenge {field} mismatch")
        nonce = _require_exact_id(challenge.get("challenge_nonce"), "BEO-APPROVAL-REFRESH-NONCE-", "challenge_nonce")
        _require_exact_value(nonce, EXPECTED_311_REFRESH_NONCE, "challenge_nonce")
        payload_hash = hash_package(
            {
                "approval_request_hash": challenge["approval_request_hash"],
                "prior_reconciliation_hash": challenge["prior_reconciliation_hash"],
                "prior_challenge_record_hash": challenge["prior_challenge_record_hash"],
                "prior_challenge_hash": challenge["prior_challenge_hash"],
                "expired_attempt_hash": challenge["expired_attempt_hash"],
                "operator_identity": challenge["operator_identity"],
                "challenge_nonce": challenge["challenge_nonce"],
                "issued_at": challenge["issued_at"],
                "expires_at": challenge["expires_at"],
                "short_approval_reply": challenge["short_approval_reply"],
                "short_approval_reply_hash": challenge["short_approval_reply_hash"],
                "challenge_scope": challenge["challenge_scope"],
                "denied_authorities": list(_DENIED_AUTHORITIES),
            }
        )
        _require_hash(challenge.get("challenge_payload_hash"), "refresh challenge payload hash")
        if challenge.get("challenge_payload_hash") != payload_hash:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("refresh challenge payload hash mismatch")
        _require_denied_authorities(challenge.get("denied_authorities"), "refresh approval challenge")
        _require_side_effects(challenge.get("side_effects"), _SIDE_EFFECTS_311, "refresh approval challenge")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    _require_operator_identity(challenge.get("operator_identity"))
    _require_refresh_window(challenge.get("issued_at"), challenge.get("expires_at"))
    if expired is not None:
        linked = {
            "expired_attempt_hash": expired["expired_attempt_hash"],
            "operator_identity": expired["operator_identity"],
        }
        for field, value in linked.items():
            if challenge.get(field) != value:
                raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(f"refresh approval challenge {field} mismatch")
    _require_expected_hash(challenge, "refresh_challenge_hash", EXPECTED_311_REFRESH_CHALLENGE_HASH, "refresh approval challenge")
    return _deepcopy(challenge)


def reconcile_verified_loop_beo_publication_refreshed_challenge_312(
    refresh_challenge_311: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile the refreshed challenge to approval-required/not-granted."""

    challenge = validate_verified_loop_beo_publication_refreshed_approval_challenge_311(refresh_challenge_311)
    package = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        "markers": list(_MARKERS_312),
        "approval_request_hash": challenge["approval_request_hash"],
        "prior_reconciliation_hash": challenge["prior_reconciliation_hash"],
        "prior_challenge_record_hash": challenge["prior_challenge_record_hash"],
        "prior_challenge_hash": challenge["prior_challenge_hash"],
        "expired_attempt_hash": challenge["expired_attempt_hash"],
        "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        "reconciled_state": _RECONCILED_STATE_312,
        "next_frontier": NEXT_FRONTIER_312,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_312),
    }
    package["reconciliation_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_refreshed_challenge_reconciliation_312(package, challenge)


def validate_verified_loop_beo_publication_refreshed_challenge_reconciliation_312(
    reconciliation_312: dict[str, Any],
    refresh_challenge_311: dict[str, Any] | None = None,
) -> dict[str, Any]:
    challenge = None
    if refresh_challenge_311 is not None:
        challenge = validate_verified_loop_beo_publication_refreshed_approval_challenge_311(refresh_challenge_311)
    reconciliation = _require_dict(reconciliation_312, "refresh challenge reconciliation")
    try:
        _require_allowed_keys(reconciliation, _KEYS_312, "refresh challenge reconciliation")
        if reconciliation.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED":
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("refresh challenge reconciliation status mismatch")
        if tuple(reconciliation.get("markers", ())) != _MARKERS_312:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError("refresh challenge reconciliation markers mismatch")
        expected = {
            "approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
            "prior_reconciliation_hash": EXPECTED_309_RECONCILIATION_HASH,
            "prior_challenge_record_hash": EXPECTED_308_CHALLENGE_RECORD_HASH,
            "prior_challenge_hash": EXPECTED_306_CHALLENGE_HASH,
            "reconciled_state": _RECONCILED_STATE_312,
            "next_frontier": NEXT_FRONTIER_312,
        }
        for field, value in expected.items():
            if reconciliation.get(field) != value:
                raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"refresh challenge reconciliation {field} mismatch")
        _require_denied_authorities(reconciliation.get("denied_authorities"), "refresh challenge reconciliation")
        _require_side_effects(reconciliation.get("side_effects"), _SIDE_EFFECTS_312, "refresh challenge reconciliation")
    except VerifiedLoopBeoPublicationApprovalRequestValidationError as exc:
        raise _translate_error(exc) from exc
    if challenge is not None:
        linked = {
            "expired_attempt_hash": challenge["expired_attempt_hash"],
            "refresh_challenge_hash": challenge["refresh_challenge_hash"],
        }
        for field, value in linked.items():
            if reconciliation.get(field) != value:
                raise VerifiedLoopBeoPublicationRefreshChallengeValidationError(f"refresh challenge reconciliation {field} mismatch")
    _require_expected_hash(reconciliation, "reconciliation_hash", EXPECTED_312_RECONCILIATION_HASH, "refresh challenge reconciliation")
    return _deepcopy(reconciliation)
