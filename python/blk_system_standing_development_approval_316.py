"""BLK-SYSTEM-316 standing BLK-System development approval.

This package records the operator's direction to remove expiring approval-clock
UX for BLK-System development. It is a repository-development approval record,
not runtime/publication side-effect evidence: it performs no BEO publication,
run-ID movement, signer/storage/ledger action, RTM generation, production
``blk-link``, protected-body access, runtime/tooling, Kuronode mutation, or
production-isolation claim.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_OPERATOR_DISCORD_ID,
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _parse_timestamp,
    _require_allowed_keys,
    _require_hash_field,
    _require_operator_discord_id,
    _require_side_effects,
    hash_package,
)


class StandingDevelopmentApproval316ValidationError(ValueError):
    """Raised when BLK-SYSTEM-316 standing-development approval is unsafe."""


OPERATOR_STATEMENT_316 = (
    "Get rid of this whole approval time clock, its ridiculous. "
    "You have my approval to work on all of blk-system"
)
EXPECTED_316_OBSERVED_AT = "2026-05-21T19:09:37+10:00"
EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH: str | None = "sha256:87e904afb73319fc0c0dd73ea914f428afdc9c3e035642ae0f2af55ed51782f5"
NEXT_FRONTIER_316 = "NEXT_FRONTIER_BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_ACTIVE_NO_TIME_CLOCK"

_MARKERS_316 = (
    "BLK_SYSTEM_316_STANDING_BLK_SYSTEM_DEVELOPMENT_APPROVAL_RECORDED",
    "NO_EXPIRING_APPROVAL_TIME_CLOCK_FOR_BLK_SYSTEM_DEVELOPMENT",
    NEXT_FRONTIER_316,
)

_SCOPE_LIMITS_316 = {
    "applies_to_blk_system_repository_development": True,
    "uses_expiring_time_clock": False,
    "requires_tdd_hostile_review_and_closeout": True,
    "does_not_grant_beo_publication_or_run_id_movement": True,
    "does_not_grant_kuronode_mutation": True,
    "does_not_grant_runtime_or_external_side_effects": True,
}

_SIDE_EFFECTS_316 = {
    "blk_system_development_approval_recorded": True,
    "approval_time_clock_retired_for_blk_system_development": True,
    "blk_system_repository_development_unblocked_from_time_clock": True,
    **_FALSE_SIDE_EFFECTS,
}

_KEYS_316 = frozenset(
    {
        "status",
        "markers",
        "operator_identity",
        "operator_statement_hash",
        "observed_at",
        "time_clock_required",
        "approval_time_clock_retired_for_blk_system_development",
        "scope",
        "scope_limits",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "standing_development_approval_hash",
    }
)
_FORBIDDEN_CLOCK_KEYS = frozenset(
    {
        "issued_at",
        "expires_at",
        "challenge_issued_at",
        "challenge_expires_at",
        "short_approval_reply",
        "short_approval_reply_hash",
        "challenge_nonce",
        "challenge_hash",
    }
)
_DENIED_AUTHORITIES_316 = (
    "KURONODE_SOURCE_GIT_MUTATION",
    "BEB_DISPATCH_WITHOUT_EXACT_PAYLOAD",
    "BEO_CLOSEOUT_EXECUTION_BY_THIS_RECORD",
    "BEO_PUBLICATION_BY_THIS_RECORD",
    "BEO_PUBLICATION_SIDE_EFFECT_APPROVAL_BY_STANDING_DEVELOPMENT_RECORD",
    "RUN_ID_MOVEMENT_BY_STANDING_DEVELOPMENT_RECORD",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "SIGNER_STORAGE_LEDGER_REUSE",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "DRIFT_REJECTION",
    "COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_ACCESS",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME_BY_THIS_RECORD",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)


def _translate_error(exc: Exception) -> StandingDevelopmentApproval316ValidationError:
    return StandingDevelopmentApproval316ValidationError(str(exc))


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise StandingDevelopmentApproval316ValidationError(f"{context} must be a dictionary")
    return value


def _require_operator_identity(value: Any) -> dict[str, str]:
    identity = _require_dict(value, "operator_identity")
    try:
        _require_allowed_keys(identity, frozenset({"platform", "discord_user_id"}), "operator_identity")
        if identity.get("platform") != "discord":
            raise StandingDevelopmentApproval316ValidationError("operator platform mismatch")
        _require_operator_discord_id(identity.get("discord_user_id"))
    except ValueError as exc:
        raise _translate_error(exc) from exc
    return deepcopy(identity)


def _require_observed_at(value: Any) -> str:
    try:
        _parse_timestamp(value, "observed_at")
    except ValueError as exc:
        raise _translate_error(exc) from exc
    return str(value)


def _require_exact_operator_statement(value: Any) -> str:
    if value != OPERATOR_STATEMENT_316:
        raise StandingDevelopmentApproval316ValidationError("exact operator statement mismatch")
    findings = scan_for_authority_laundering(value, "operator_statement")
    if findings:
        raise StandingDevelopmentApproval316ValidationError("; ".join(findings))
    return str(value)


def _require_denied_authorities_316(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise StandingDevelopmentApproval316ValidationError("denied_authorities must be a list")
    if tuple(value) != _DENIED_AUTHORITIES_316:
        raise StandingDevelopmentApproval316ValidationError("denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise StandingDevelopmentApproval316ValidationError("denied_authorities must not contain duplicates")
    return tuple(value)


def _require_scope_limits_316(value: Any) -> dict[str, bool]:
    limits = _require_dict(value, "scope_limits")
    try:
        _require_allowed_keys(limits, frozenset(_SCOPE_LIMITS_316), "scope_limits")
    except ValueError as exc:
        raise _translate_error(exc) from exc
    if limits != _SCOPE_LIMITS_316:
        raise StandingDevelopmentApproval316ValidationError("scope_limits mismatch")
    return deepcopy(limits)


def record_blk_system_standing_development_approval_316(
    *,
    operator_statement: str,
    operator_discord_id: str,
    observed_at: str,
) -> dict[str, Any]:
    """Record standing BLK-System development approval without an expiry clock."""

    statement = _require_exact_operator_statement(operator_statement)
    try:
        operator_id = _require_operator_discord_id(operator_discord_id)
    except ValueError as exc:
        raise _translate_error(exc) from exc
    if operator_id != EXPECTED_OPERATOR_DISCORD_ID:
        raise StandingDevelopmentApproval316ValidationError("operator identity mismatch")
    observed = _require_observed_at(observed_at)

    package = {
        "status": "BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_RECORDED_NO_TIME_CLOCK",
        "markers": list(_MARKERS_316),
        "operator_identity": {
            "platform": "discord",
            "discord_user_id": operator_id,
        },
        "operator_statement_hash": _hash_text(statement),
        "observed_at": observed,
        "time_clock_required": False,
        "approval_time_clock_retired_for_blk_system_development": True,
        "scope": "BLK-System repository development under TDD, hostile review, lean closeout, exact-path commit discipline",
        "scope_limits": deepcopy(_SCOPE_LIMITS_316),
        "next_frontier": NEXT_FRONTIER_316,
        "denied_authorities": list(_DENIED_AUTHORITIES_316),
        "side_effects": dict(_SIDE_EFFECTS_316),
    }
    package["standing_development_approval_hash"] = hash_package(package)
    return validate_blk_system_standing_development_approval_316(package)


def validate_blk_system_standing_development_approval_316(record_316: dict[str, Any]) -> dict[str, Any]:
    """Validate the standing BLK-System development approval record."""

    record = _require_dict(record_316, "standing development approval record")
    extra_clock_keys = sorted(set(record) & _FORBIDDEN_CLOCK_KEYS)
    if extra_clock_keys:
        raise StandingDevelopmentApproval316ValidationError(
            f"standing approval record must not reintroduce time clock keys {extra_clock_keys!r}"
        )
    try:
        _require_allowed_keys(record, _KEYS_316, "standing development approval record")
    except ValueError as exc:
        raise _translate_error(exc) from exc
    if record.get("status") != "BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_RECORDED_NO_TIME_CLOCK":
        raise StandingDevelopmentApproval316ValidationError("status mismatch")
    if tuple(record.get("markers", ())) != _MARKERS_316:
        raise StandingDevelopmentApproval316ValidationError("markers mismatch")
    _require_operator_identity(record.get("operator_identity"))
    if record.get("observed_at") != EXPECTED_316_OBSERVED_AT:
        raise StandingDevelopmentApproval316ValidationError("observed_at mismatch")
    _require_observed_at(record.get("observed_at"))
    if record.get("operator_statement_hash") != _hash_text(OPERATOR_STATEMENT_316):
        raise StandingDevelopmentApproval316ValidationError("operator_statement_hash mismatch")
    if record.get("time_clock_required") is not False:
        raise StandingDevelopmentApproval316ValidationError("time_clock_required must be false")
    if record.get("approval_time_clock_retired_for_blk_system_development") is not True:
        raise StandingDevelopmentApproval316ValidationError("approval time clock retirement mismatch")
    if record.get("next_frontier") != NEXT_FRONTIER_316:
        raise StandingDevelopmentApproval316ValidationError("next_frontier mismatch")
    _require_scope_limits_316(record.get("scope_limits"))
    _require_denied_authorities_316(record.get("denied_authorities"))
    try:
        _require_side_effects(record.get("side_effects"), _SIDE_EFFECTS_316, "standing development approval record")
        _require_hash_field(record, "standing_development_approval_hash", "standing development approval record")
    except ValueError as exc:
        raise _translate_error(exc) from exc
    findings = scan_for_authority_laundering(record, "standing_development_approval_record")
    if findings:
        raise StandingDevelopmentApproval316ValidationError("; ".join(findings))
    if EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH is not None:
        if record["standing_development_approval_hash"] != EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH:
            raise StandingDevelopmentApproval316ValidationError("standing development approval canonical hash mismatch")
    canonical = hash_package(
        {
            key: value
            for key, value in record.items()
            if key != "standing_development_approval_hash"
        }
    )
    if canonical != record["standing_development_approval_hash"]:
        raise StandingDevelopmentApproval316ValidationError("standing development approval canonical hash mismatch")
    return deepcopy(record)
