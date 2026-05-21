"""BLK-SYSTEM-306..309 verified-loop BEO publication approval request.

This module consumes BLK-SYSTEM-305 verified-loop BEO publication review
evidence and emits a deterministic request-only package for future operator
approval. It prepares a short `Approve` challenge artifact, but it does not
capture approval, reserve or consume a run ID, execute a BEO closeout, publish a
BEO, reuse signer/storage/ledger authority, generate RTM, run production
blk-link, read protected bodies, start tooling, or mutate target/source/Git
state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any


class VerifiedLoopBeoPublicationApprovalRequestValidationError(ValueError):
    """Raised when approval-request evidence crosses an authority boundary."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_TIMESTAMPTZ_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

EXPECTED_OPERATOR_DISCORD_ID = "684235178083745819"
EXPECTED_306_REQUEST_ID = "BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-001"
EXPECTED_306_CHALLENGE_NONCE = "BEO-APPROVAL-NONCE-BLK-SYSTEM-306-001"
EXPECTED_306_REQUESTED_AT = "2026-05-21T12:30:00+10:00"
EXPECTED_306_EXPIRES_AT = "2026-05-21T13:00:00+10:00"
EXPECTED_306_CHALLENGE_HASH = "sha256:1e1dd479f39401670d3c2e375b4124027baae9f0686f0da7863888bd141741af"
EXPECTED_306_APPROVAL_REQUEST_HASH = "sha256:becd296289dc4ba965a04e4e498202a9b6e708b0f697fcd3431049125985c939"
EXPECTED_307_CONTRACT_HASH = "sha256:1a12d788d0032a44200b557d6cfa525e8d8e180ddda900d243f9faf9395f2ce0"
EXPECTED_308_CHALLENGE_RECORD_HASH = "sha256:931728d4fbb34f4310cae79ccd7c64462cc61b630d0c8409918c94955c5b0434"
EXPECTED_309_RECONCILIATION_HASH = "sha256:0f9c754a31db778ed2cf377d389da75459a81a4bd55626cfe8b82a2542ab1e83"
_MAX_REQUEST_WINDOW_SECONDS = 60 * 60
EXPECTED_305_RECONCILIATION_HASH = "sha256:02a3f5dc842961419965af4bb8f4e5c827a300c6207582d16f9e20cf7416a219"
EXPECTED_305_REVIEW_RECORD_HASH = "sha256:a035198eccffa8da7d9b567019c5b3806bdfb2bbe5786b016b4809757d39f667"
EXPECTED_305_REVIEW_REQUEST_HASH = "sha256:89cd2d11ee5c00ecbb9938f92a7d06a1cc07bc34b741ab92ec7321f3ae1dad0d"
EXPECTED_305_CONTRACT_HASH = "sha256:95bcc1203eb588104c5d19108a7ee8f9a3ce3d8537f3058d72061ea6ff0ae209"
EXPECTED_305_VERIFICATION_RECONCILIATION_HASH = "sha256:7eb8fc4820cc541594479e1ab166164ea2ad0ca60c2a8571a213ecfbee0e8ac1"
EXPECTED_305_REUSABLE_BEO_RECONCILIATION_HASH = "sha256:4e2acbff751aae66dda868d1e4e06c56b0f210b624a2affa7e4c658bda25dddd"

NEXT_FRONTIER_309 = "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CAPTURE_AND_BOUNDED_EXECUTION_REQUIRED_NOT_GRANTED"

_MARKERS_305 = (
    "BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
    "VERIFIED_LOOP_BEO_REVIEW_READY_NOT_PUBLICATION_AUTHORITY",
    "NEXT_EXACT_BEO_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED",
)
_MARKERS_306 = (
    "BLK_SYSTEM_306_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY",
    "SHORT_APPROVE_CHALLENGE_PREPARED_NOT_CAPTURED",
    "BEO_PUBLICATION_EXECUTION_STILL_DENIED",
)
_MARKERS_307 = (
    "BLK_SYSTEM_307_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY",
    "APPROVAL_CAPTURE_REQUIRES_FUTURE_EXACT_PACKAGE",
    "RUN_ID_RESERVATION_STILL_DENIED",
)
_MARKERS_308 = (
    "BLK_SYSTEM_308_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED",
    "APPROVAL_STATE_PENDING_NOT_CAPTURED",
    "PUBLICATION_EXECUTION_NOT_READY",
)
_MARKERS_309 = (
    "BLK_SYSTEM_309_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED",
    "NEXT_EXACT_APPROVAL_CAPTURE_AND_BOUNDED_EXECUTION_REQUIRED_NOT_GRANTED",
    "REQUEST_ONLY_NO_PUBLICATION_AUTHORITY",
)

_FORBIDDEN_ID_SEGMENTS = frozenset(
    {
        "APPROVED",
        "AUTHORIZED",
        "AUTHORISED",
        "GRANTED",
        "GREENLIT",
        "PERMITTED",
        "ALLOWED",
        "CAPTURED",
        "RESERVED",
        "CONSUMED",
        "REUSED",
        "PUBLISHED",
        "EXECUTED",
        "SIGNED",
        "STORED",
        "LEDGERED",
    }
)

_DENIED_AUTHORITIES = (
    "APPROVAL_CAPTURE_IN_THIS_PACKAGE",
    "GENERIC_APPROVE_AS_UNBOUND_AUTHORITY",
    "APPROVAL_REUSE",
    "RUN_ID_RESERVATION",
    "RUN_ID_CONSUMPTION",
    "BEO_CLOSEOUT_EXECUTION",
    "AUTHORITATIVE_BEO_PUBLICATION_EXECUTION",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "SIGNER_KEY_MATERIAL_ACCESS_OR_REUSE",
    "IMMUTABLE_STORAGE_WRITE_OR_REUSE",
    "PUBLIC_LEDGER_APPEND_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "DRIFT_REJECTION",
    "COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_ACCESS",
    "BEB_DISPATCH",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)

_FALSE_SIDE_EFFECTS = {
    "approval_captured": False,
    "approval_reuse": False,
    "generic_approve_captured": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "challenge_consumed": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "authoritative_beo_publication": False,
    "reusable_beo_publication": False,
    "signer_reuse": False,
    "signer_key_material_accessed": False,
    "signature_generated": False,
    "storage_reuse": False,
    "immutable_storage_written": False,
    "ledger_reuse": False,
    "public_ledger_mutated": False,
    "rollback_revocation_supersession": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "beb_dispatch": False,
    "blk_test_transport_started": False,
    "blk_pipe_runtime": False,
    "codex_runtime": False,
    "runtime_tooling_executed": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_SIDE_EFFECTS_306 = {
    "approval_request_prepared": True,
    "challenge_artifact_prepared": True,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_307 = {
    "approval_request_prepared": True,
    "challenge_artifact_prepared": True,
    "approval_request_contract_prepared": True,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_308 = {
    "approval_request_prepared": True,
    "challenge_artifact_prepared": True,
    "approval_request_contract_prepared": True,
    "challenge_recorded": True,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_309 = {
    "approval_request_prepared": True,
    "challenge_artifact_prepared": True,
    "approval_request_contract_prepared": True,
    "challenge_recorded": True,
    "approval_request_reconciled": True,
    **_FALSE_SIDE_EFFECTS,
}

_EXPECTED_305_SIDE_EFFECTS = {
    "review_request_prepared": True,
    "review_contract_prepared": True,
    "review_recorded": True,
    "review_reconciled": True,
    "beo_publication_approval_captured": False,
    "approval_reuse": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "authoritative_beo_publication": False,
    "reusable_beo_publication": False,
    "signer_reuse": False,
    "signer_key_material_accessed": False,
    "signature_generated": False,
    "storage_reuse": False,
    "immutable_storage_written": False,
    "ledger_reuse": False,
    "public_ledger_mutated": False,
    "rollback_revocation_supersession": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "beb_dispatch": False,
    "blk_test_transport_started": False,
    "blk_pipe_runtime": False,
    "codex_runtime": False,
    "runtime_tooling_executed": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_APPROVAL_CAPTURE_RULES = {
    "exact_request_hash_required": True,
    "exact_operator_identity_required": True,
    "exact_nonce_required": True,
    "exact_short_reply_hash_required": True,
    "request_window_must_be_live": True,
    "capture_allowed_in_this_package": False,
    "generic_unbound_approve_allowed": False,
    "operator_reply_can_mutate_state_in_this_package": False,
}
_EXECUTION_PREREQUISITES = {
    "explicit_approval_capture_required_before_execution": True,
    "future_execution_package_required": True,
    "one_fresh_run_id_required": True,
    "run_id_reserved_by_request": False,
    "run_id_consumed_by_request": False,
    "signature_receipt_required_before_publication": True,
    "signature_generated_by_request": False,
    "immutable_storage_receipt_required_before_publication": True,
    "immutable_storage_written_by_request": False,
    "public_ledger_receipt_required_before_publication": True,
    "public_ledger_appended_by_request": False,
    "publication_execution_allowed_by_request": False,
}
_REQUIRED_PARENT_HASH_FIELDS = (
    "review_reconciliation_hash",
    "review_record_hash",
    "review_request_hash",
    "review_contract_hash",
    "verification_reconciliation_hash",
    "reusable_beo_reconciliation_hash",
)

_KEYS_305 = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "review_request_hash",
        "review_record_hash",
        "verification_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "review_result",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)
_OPERATOR_KEYS = frozenset({"platform", "discord_user_id"})
_CHALLENGE_KEYS = frozenset(
    {
        "challenge_nonce",
        "bound_request_id",
        "bound_operator_discord_id",
        "bound_review_reconciliation_hash",
        "required_reply",
        "required_reply_hash",
        "requested_at",
        "expires_at",
        "short_approve_is_approval_now",
        "future_capture_package_required",
        "challenge_hash",
    }
)
_KEYS_306 = frozenset(
    {
        "status",
        "markers",
        "request_id",
        "requested_at",
        "expires_at",
        "expired",
        "operator_identity",
        "challenge",
        "review_reconciliation_hash",
        "review_record_hash",
        "review_request_hash",
        "review_contract_hash",
        "verification_reconciliation_hash",
        "reusable_beo_reconciliation_hash",
        "approval_scope",
        "required_parent_hashes",
        "denied_authorities",
        "side_effects",
        "approval_request_hash",
    }
)
_KEYS_307 = frozenset(
    {
        "status",
        "markers",
        "approval_request_hash",
        "review_reconciliation_hash",
        "challenge_hash",
        "operator_identity",
        "approval_capture_rules",
        "execution_prerequisites",
        "denied_authorities",
        "side_effects",
        "contract_hash",
    }
)
_DECISION_WINDOW_KEYS = frozenset({"requested_at", "expires_at"})
_KEYS_308 = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "approval_request_hash",
        "review_reconciliation_hash",
        "challenge_hash",
        "recorded_at",
        "operator_identity",
        "approval_state",
        "approval_captured",
        "publication_execution_ready",
        "required_reply_hash",
        "decision_window",
        "side_effects",
        "challenge_record_hash",
    }
)
_KEYS_309 = frozenset(
    {
        "status",
        "markers",
        "contract_hash",
        "approval_request_hash",
        "challenge_record_hash",
        "review_reconciliation_hash",
        "challenge_hash",
        "approval_state",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _without_hash(package: dict[str, Any], field: str) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in package.items() if key != field}


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(package) - allowed)
    if extras:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
            f"{context} unsupported field(s): {', '.join(extras)}"
        )
    missing = sorted(allowed - set(package))
    if missing:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
            f"{context} missing field(s): {', '.join(missing)}"
        )


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} hash mismatch for {field}")


def _require_ascii_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value or any(ord(ch) > 127 for ch in value):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be a non-empty ASCII string")
    return value


def _require_exact_id(value: Any, prefix: str, context: str) -> str:
    value = _require_ascii_string(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be an exact ID with prefix {prefix}")
    segments = value.split("-")
    forbidden = sorted(
        token for token in _FORBIDDEN_ID_SEGMENTS
        if any(token in segment for segment in segments)
    )
    if forbidden:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
            f"{context} contains forbidden authority segment(s): {', '.join(forbidden)}"
        )
    return value


def _require_exact_value(value: Any, expected: str, context: str) -> None:
    if value != expected:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} canonical value mismatch")


def _require_operator_discord_id(value: Any) -> str:
    if not isinstance(value, str) or any(ch not in "0123456789" for ch in value):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("operator discord ID must use ASCII digits")
    if value != EXPECTED_OPERATOR_DISCORD_ID:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("operator discord ID mismatch")
    return value


def _parse_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMPTZ_RE.match(value):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
            f"{context} must be an ISO-8601 timestamp with timezone"
        )
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be parseable") from exc
    if parsed.tzinfo is None:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must include timezone")
    return parsed


def _validation_now(tzinfo) -> datetime:
    return datetime.now(tz=tzinfo)


def _require_time_window(start: Any, end: Any, start_name: str = "requested_at", end_name: str = "expires_at") -> None:
    parsed_start = _parse_timestamp(start, start_name)
    parsed_end = _parse_timestamp(end, end_name)
    if parsed_end <= parsed_start:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{end_name} must be after {start_name}")
    if (parsed_end - parsed_start).total_seconds() > _MAX_REQUEST_WINDOW_SECONDS:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("request window exceeds maximum TTL")


def _require_live_request_window(start: Any, end: Any, context: str) -> None:
    parsed_start = _parse_timestamp(start, "requested_at")
    parsed_end = _parse_timestamp(end, "expires_at")
    now = _validation_now(parsed_end.tzinfo)
    if now < parsed_start:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} request window not yet live")
    if now >= parsed_end:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} request window expired/stale")


def _require_timestamp_within(value: Any, start: Any, end: Any, context: str) -> None:
    parsed_value = _parse_timestamp(value, context)
    parsed_start = _parse_timestamp(start, "requested_at")
    parsed_end = _parse_timestamp(end, "expires_at")
    if parsed_value < parsed_start or parsed_value >= parsed_end:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} must be within request window")


def _require_side_effects(value: Any, expected: dict[str, bool], context: str) -> None:
    if value != expected:
        if isinstance(value, dict):
            for key, expected_value in expected.items():
                if expected_value is False and value.get(key) is not False:
                    raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
                        f"{context} side_effects {key} must remain false"
                    )
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} side_effects mismatch")


def _require_denied_authorities(value: Any, context: str) -> None:
    if not isinstance(value, list):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} denied_authorities must be a list")
    if value != list(_DENIED_AUTHORITIES):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"{context} denied_authorities contains duplicates")


def _validate_operator_identity(value: Any) -> dict[str, str]:
    identity = _require_dict(value, "operator_identity")
    _require_allowed_keys(identity, _OPERATOR_KEYS, "operator_identity")
    if identity.get("platform") != "discord":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("operator platform mismatch")
    _require_operator_discord_id(identity.get("discord_user_id"))
    return _deepcopy(identity)


def _validate_challenge(challenge: Any, request_id: str, review_hash: str, operator_id: str) -> dict[str, Any]:
    item = _require_dict(challenge, "challenge")
    _require_allowed_keys(item, _CHALLENGE_KEYS, "challenge")
    _require_exact_id(item.get("challenge_nonce"), "BEO-APPROVAL-NONCE-", "challenge nonce")
    _require_exact_value(item.get("challenge_nonce"), EXPECTED_306_CHALLENGE_NONCE, "challenge_nonce")
    if item.get("bound_request_id") != request_id:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge request binding mismatch")
    if item.get("bound_operator_discord_id") != operator_id:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge operator binding mismatch")
    if item.get("bound_review_reconciliation_hash") != review_hash:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge review hash binding mismatch")
    if item.get("required_reply") != "Approve":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge required reply mismatch")
    if item.get("required_reply_hash") != _hash_text("Approve"):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge required reply hash mismatch")
    _require_time_window(item.get("requested_at"), item.get("expires_at"))
    if item.get("short_approve_is_approval_now") is not False:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("short Approve must not be approval now")
    if item.get("future_capture_package_required") is not True:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("future capture package must be required")
    _require_hash_field(item, "challenge_hash", "challenge")
    if item["challenge_hash"] != EXPECTED_306_CHALLENGE_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge canonical hash mismatch")
    return _deepcopy(item)


def _validate_305_reconciliation(package: dict[str, Any]) -> dict[str, Any]:
    candidate = _require_dict(package, "BLK-SYSTEM-305 reconciliation")
    _require_allowed_keys(candidate, _KEYS_305, "BLK-SYSTEM-305 reconciliation")
    if candidate.get("reconciliation_hash") != EXPECTED_305_RECONCILIATION_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("BLK-SYSTEM-305 canonical reconciliation hash mismatch")
    _require_hash_field(candidate, "reconciliation_hash", "BLK-SYSTEM-305 reconciliation")
    expected = {
        "status": "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
        "markers": list(_MARKERS_305),
        "contract_hash": EXPECTED_305_CONTRACT_HASH,
        "review_request_hash": EXPECTED_305_REVIEW_REQUEST_HASH,
        "review_record_hash": EXPECTED_305_REVIEW_RECORD_HASH,
        "verification_reconciliation_hash": EXPECTED_305_VERIFICATION_RECONCILIATION_HASH,
        "reusable_beo_reconciliation_hash": EXPECTED_305_REUSABLE_BEO_RECONCILIATION_HASH,
        "review_result": "READY_FOR_EXACT_APPROVAL_REQUEST",
        "reconciled_state": "verified_loop_beo_publication_review_ready_for_exact_approval_request_not_granted",
        "next_frontier": "NEXT_FRONTIER_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_REQUIRED_NOT_GRANTED",
    }
    for field, value in expected.items():
        if candidate.get(field) != value:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"BLK-SYSTEM-305 {field} mismatch")
    _require_side_effects(candidate.get("side_effects"), _EXPECTED_305_SIDE_EFFECTS, "BLK-SYSTEM-305")
    return _deepcopy(candidate)


def build_verified_loop_beo_publication_approval_request_306(
    review_reconciliation_305: dict[str, Any],
    *,
    request_id: str,
    requested_at: str,
    expires_at: str,
    operator_discord_id: str,
    challenge_nonce: str,
) -> dict[str, Any]:
    """Build the request-only package for future exact operator approval."""

    review = _validate_305_reconciliation(review_reconciliation_305)
    request_id = _require_exact_id(request_id, "BEO-APPROVAL-REQUEST-", "request_id")
    _require_exact_value(request_id, EXPECTED_306_REQUEST_ID, "request_id")
    operator_id = _require_operator_discord_id(operator_discord_id)
    challenge_nonce = _require_exact_id(challenge_nonce, "BEO-APPROVAL-NONCE-", "challenge_nonce")
    _require_exact_value(challenge_nonce, EXPECTED_306_CHALLENGE_NONCE, "challenge_nonce")
    _require_time_window(requested_at, expires_at)
    _require_exact_value(requested_at, EXPECTED_306_REQUESTED_AT, "requested_at")
    _require_exact_value(expires_at, EXPECTED_306_EXPIRES_AT, "expires_at")
    _require_live_request_window(requested_at, expires_at, "approval request")
    challenge = {
        "challenge_nonce": challenge_nonce,
        "bound_request_id": request_id,
        "bound_operator_discord_id": operator_id,
        "bound_review_reconciliation_hash": review["reconciliation_hash"],
        "required_reply": "Approve",
        "required_reply_hash": _hash_text("Approve"),
        "requested_at": requested_at,
        "expires_at": expires_at,
        "short_approve_is_approval_now": False,
        "future_capture_package_required": True,
    }
    challenge["challenge_hash"] = hash_package(challenge)
    request = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY_NOT_GRANTED",
        "markers": list(_MARKERS_306),
        "request_id": request_id,
        "requested_at": requested_at,
        "expires_at": expires_at,
        "expired": False,
        "operator_identity": {"platform": "discord", "discord_user_id": operator_id},
        "challenge": challenge,
        "review_reconciliation_hash": review["reconciliation_hash"],
        "review_record_hash": review["review_record_hash"],
        "review_request_hash": review["review_request_hash"],
        "review_contract_hash": review["contract_hash"],
        "verification_reconciliation_hash": review["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": review["reusable_beo_reconciliation_hash"],
        "approval_scope": "request_operator_approval_for_one_verified_loop_beo_publication_path",
        "required_parent_hashes": list(_REQUIRED_PARENT_HASH_FIELDS),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_306),
    }
    request["approval_request_hash"] = hash_package(request)
    return validate_verified_loop_beo_publication_approval_request_306(request, review)


def validate_verified_loop_beo_publication_approval_request_306(
    approval_request_306: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    review = _validate_305_reconciliation(review_reconciliation_305)
    request = _require_dict(approval_request_306, "approval request")
    _require_allowed_keys(request, _KEYS_306, "approval request")
    if request.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY_NOT_GRANTED":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request status mismatch")
    if tuple(request.get("markers", ())) != _MARKERS_306:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request markers mismatch")
    request_id = _require_exact_id(request.get("request_id"), "BEO-APPROVAL-REQUEST-", "request_id")
    _require_exact_value(request_id, EXPECTED_306_REQUEST_ID, "request_id")
    _require_time_window(request.get("requested_at"), request.get("expires_at"))
    _require_exact_value(request.get("requested_at"), EXPECTED_306_REQUESTED_AT, "requested_at")
    _require_exact_value(request.get("expires_at"), EXPECTED_306_EXPIRES_AT, "expires_at")
    _require_live_request_window(request.get("requested_at"), request.get("expires_at"), "approval request")
    if request.get("expired") is not False:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request expired must be false")
    identity = _validate_operator_identity(request.get("operator_identity"))
    challenge = _validate_challenge(
        request.get("challenge"),
        request_id,
        review["reconciliation_hash"],
        identity["discord_user_id"],
    )
    if challenge.get("requested_at") != request.get("requested_at") or challenge.get("expires_at") != request.get("expires_at"):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("challenge window must match approval request window")
    expected = {
        "review_reconciliation_hash": review["reconciliation_hash"],
        "review_record_hash": review["review_record_hash"],
        "review_request_hash": review["review_request_hash"],
        "review_contract_hash": review["contract_hash"],
        "verification_reconciliation_hash": review["verification_reconciliation_hash"],
        "reusable_beo_reconciliation_hash": review["reusable_beo_reconciliation_hash"],
    }
    for field, value in expected.items():
        if request.get(field) != value:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"approval request {field} mismatch")
    if request.get("approval_scope") != "request_operator_approval_for_one_verified_loop_beo_publication_path":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request scope mismatch")
    if request.get("required_parent_hashes") != list(_REQUIRED_PARENT_HASH_FIELDS):
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request parent hash list mismatch")
    _require_denied_authorities(request.get("denied_authorities"), "approval request")
    _require_side_effects(request.get("side_effects"), _SIDE_EFFECTS_306, "approval request")
    _require_hash_field(request, "approval_request_hash", "approval request")
    if request["approval_request_hash"] != EXPECTED_306_APPROVAL_REQUEST_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request canonical hash mismatch")
    return _deepcopy(request)


def build_verified_loop_beo_publication_approval_request_contract_307(
    approval_request_306: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    contract = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY",
        "markers": list(_MARKERS_307),
        "approval_request_hash": request["approval_request_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
        "operator_identity": _deepcopy(request["operator_identity"]),
        "approval_capture_rules": dict(_APPROVAL_CAPTURE_RULES),
        "execution_prerequisites": dict(_EXECUTION_PREREQUISITES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS_307),
    }
    contract["contract_hash"] = hash_package(contract)
    return validate_verified_loop_beo_publication_approval_request_contract_307(contract, request, review_reconciliation_305)


def validate_verified_loop_beo_publication_approval_request_contract_307(
    approval_contract_307: dict[str, Any],
    approval_request_306: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    contract = _require_dict(approval_contract_307, "approval request contract")
    _require_allowed_keys(contract, _KEYS_307, "approval request contract")
    if contract.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request contract status mismatch")
    if tuple(contract.get("markers", ())) != _MARKERS_307:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request contract markers mismatch")
    expected = {
        "approval_request_hash": request["approval_request_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
    }
    for field, value in expected.items():
        if contract.get(field) != value:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"approval request contract {field} mismatch")
    if contract.get("operator_identity") != request["operator_identity"]:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request contract operator mismatch")
    if contract.get("approval_capture_rules") != _APPROVAL_CAPTURE_RULES:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval capture rules mismatch")
    if contract.get("execution_prerequisites") != _EXECUTION_PREREQUISITES:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("execution prerequisites mismatch")
    _require_denied_authorities(contract.get("denied_authorities"), "approval request contract")
    _require_side_effects(contract.get("side_effects"), _SIDE_EFFECTS_307, "approval request contract")
    _require_hash_field(contract, "contract_hash", "approval request contract")
    if contract["contract_hash"] != EXPECTED_307_CONTRACT_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request contract canonical hash mismatch")
    return _deepcopy(contract)


def record_verified_loop_beo_publication_approval_challenge_308(
    approval_contract_307: dict[str, Any],
    approval_request_306: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
    *,
    recorded_at: str,
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_approval_request_contract_307(
        approval_contract_307,
        approval_request_306,
        review_reconciliation_305,
    )
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    _require_timestamp_within(recorded_at, request["requested_at"], request["expires_at"], "recorded_at")
    record = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED_NOT_APPROVED",
        "markers": list(_MARKERS_308),
        "contract_hash": contract["contract_hash"],
        "approval_request_hash": request["approval_request_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
        "recorded_at": recorded_at,
        "operator_identity": _deepcopy(request["operator_identity"]),
        "approval_state": "PENDING_NOT_CAPTURED",
        "approval_captured": False,
        "publication_execution_ready": False,
        "required_reply_hash": request["challenge"]["required_reply_hash"],
        "decision_window": {"requested_at": request["requested_at"], "expires_at": request["expires_at"]},
        "side_effects": dict(_SIDE_EFFECTS_308),
    }
    record["challenge_record_hash"] = hash_package(record)
    return validate_verified_loop_beo_publication_approval_challenge_308(record, contract, request, review_reconciliation_305)


def validate_verified_loop_beo_publication_approval_challenge_308(
    challenge_record_308: dict[str, Any],
    approval_contract_307: dict[str, Any],
    approval_request_306: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_approval_request_contract_307(
        approval_contract_307,
        approval_request_306,
        review_reconciliation_305,
    )
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    record = _require_dict(challenge_record_308, "approval challenge record")
    _require_allowed_keys(record, _KEYS_308, "approval challenge record")
    if record.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED_NOT_APPROVED":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge status mismatch")
    if tuple(record.get("markers", ())) != _MARKERS_308:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge markers mismatch")
    expected = {
        "contract_hash": contract["contract_hash"],
        "approval_request_hash": request["approval_request_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
        "required_reply_hash": request["challenge"]["required_reply_hash"],
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError(f"approval challenge {field} mismatch")
    _require_timestamp_within(record.get("recorded_at"), request["requested_at"], request["expires_at"], "recorded_at")
    if record.get("operator_identity") != request["operator_identity"]:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge operator mismatch")
    if record.get("approval_state") != "PENDING_NOT_CAPTURED":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge state must remain pending")
    if record.get("approval_captured") is not False:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge must not mark approval captured")
    if record.get("publication_execution_ready") is not False:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge must not make publication ready")
    window = _require_dict(record.get("decision_window"), "decision_window")
    _require_allowed_keys(window, _DECISION_WINDOW_KEYS, "decision_window")
    if window != {"requested_at": request["requested_at"], "expires_at": request["expires_at"]}:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge decision window mismatch")
    _require_side_effects(record.get("side_effects"), _SIDE_EFFECTS_308, "approval challenge")
    _require_hash_field(record, "challenge_record_hash", "approval challenge")
    if record["challenge_record_hash"] != EXPECTED_308_CHALLENGE_RECORD_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval challenge canonical hash mismatch")
    return _deepcopy(record)


def reconcile_verified_loop_beo_publication_approval_request_309(
    approval_contract_307: dict[str, Any],
    approval_request_306: dict[str, Any],
    challenge_record_308: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_approval_request_contract_307(
        approval_contract_307,
        approval_request_306,
        review_reconciliation_305,
    )
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    challenge = validate_verified_loop_beo_publication_approval_challenge_308(
        challenge_record_308,
        contract,
        request,
        review_reconciliation_305,
    )
    reconciliation = {
        "status": "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED",
        "markers": list(_MARKERS_309),
        "contract_hash": contract["contract_hash"],
        "approval_request_hash": request["approval_request_hash"],
        "challenge_record_hash": challenge["challenge_record_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
        "approval_state": challenge["approval_state"],
        "reconciled_state": "verified_loop_beo_publication_approval_request_ready_not_granted",
        "next_frontier": NEXT_FRONTIER_309,
        "side_effects": dict(_SIDE_EFFECTS_309),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_verified_loop_beo_publication_approval_request_reconciliation_309(
        reconciliation,
        contract,
        request,
        challenge,
        review_reconciliation_305,
    )


def validate_verified_loop_beo_publication_approval_request_reconciliation_309(
    reconciliation_309: dict[str, Any],
    approval_contract_307: dict[str, Any],
    approval_request_306: dict[str, Any],
    challenge_record_308: dict[str, Any],
    review_reconciliation_305: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_verified_loop_beo_publication_approval_request_contract_307(
        approval_contract_307,
        approval_request_306,
        review_reconciliation_305,
    )
    request = validate_verified_loop_beo_publication_approval_request_306(approval_request_306, review_reconciliation_305)
    challenge = validate_verified_loop_beo_publication_approval_challenge_308(
        challenge_record_308,
        contract,
        request,
        review_reconciliation_305,
    )
    reconciliation = _require_dict(reconciliation_309, "approval request reconciliation")
    _require_allowed_keys(reconciliation, _KEYS_309, "approval request reconciliation")
    if reconciliation.get("status") != "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED":
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request reconciliation status mismatch")
    if tuple(reconciliation.get("markers", ())) != _MARKERS_309:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request reconciliation markers mismatch")
    expected = {
        "contract_hash": contract["contract_hash"],
        "approval_request_hash": request["approval_request_hash"],
        "challenge_record_hash": challenge["challenge_record_hash"],
        "review_reconciliation_hash": request["review_reconciliation_hash"],
        "challenge_hash": request["challenge"]["challenge_hash"],
        "approval_state": "PENDING_NOT_CAPTURED",
        "reconciled_state": "verified_loop_beo_publication_approval_request_ready_not_granted",
        "next_frontier": NEXT_FRONTIER_309,
    }
    for field, value in expected.items():
        if reconciliation.get(field) != value:
            raise VerifiedLoopBeoPublicationApprovalRequestValidationError(
                f"approval request reconciliation {field} mismatch"
            )
    _require_side_effects(reconciliation.get("side_effects"), _SIDE_EFFECTS_309, "approval request reconciliation")
    _require_hash_field(reconciliation, "reconciliation_hash", "approval request reconciliation")
    if reconciliation["reconciliation_hash"] != EXPECTED_309_RECONCILIATION_HASH:
        raise VerifiedLoopBeoPublicationApprovalRequestValidationError("approval request reconciliation canonical hash mismatch")
    return _deepcopy(reconciliation)
