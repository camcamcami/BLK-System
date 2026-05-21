"""BLK-SYSTEM-317..321 velocity path toward 9/10 readiness.

This package converts BLK-SYSTEM-316 standing repository-development approval
into a bounded 9/10 development-unblock record. It prepares the next exact
no-clock side-effect decision surface, but it does not capture approval, reserve
or consume a run ID, publish a BEO, generate RTM, execute production blk-link,
read protected bodies, start runtime/tooling, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_standing_development_approval_316 import (
    EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH,
    validate_blk_system_standing_development_approval_316,
)
from rtm_blk_link_drift_coverage_refresh_challenge_package_279_281 import (
    _CANONICAL_RECONCILIATION_281_HASH,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_306_APPROVAL_REQUEST_HASH,
    EXPECTED_307_CONTRACT_HASH,
    EXPECTED_308_CHALLENGE_RECORD_HASH,
    EXPECTED_309_RECONCILIATION_HASH,
    _FALSE_SIDE_EFFECTS,
    _require_allowed_keys,
    hash_package,
)
from verified_loop_beo_publication_live_challenge_guard_313_315 import (
    EXPECTED_313_LIVE_DIRECTIVE_HASH,
    EXPECTED_314_SHORT_APPROVE_GUARD_HASH,
    EXPECTED_315_RECONCILIATION_HASH,
)
from verified_loop_beo_publication_refresh_challenge_310_312 import (
    EXPECTED_310_EXPIRED_ATTEMPT_HASH,
    EXPECTED_311_REFRESH_CHALLENGE_HASH,
    EXPECTED_312_RECONCILIATION_HASH,
)


class VelocityTo9ValidationError(ValueError):
    """Raised when BLK-SYSTEM-317..321 evidence crosses authority boundaries."""


OPERATOR_DIRECTIVE_317 = "plan and execute all blk-system sprints needed to get blk-system to 9/10"
NEXT_FRONTIER_321 = "NEXT_FRONTIER_BLK_SYSTEM_9_OF_10_REPO_DEVELOPMENT_READY_SIDE_EFFECT_APPROVALS_SEPARATE_NOT_GRANTED"
EXPECTED_317_FRONTIER_HASH = "sha256:99df97cf8a7e553ecb9a28d6a814103977caa52b3e6df1a1df3c1f6342134af8"
EXPECTED_318_REQUEST_HASH = "sha256:4425cad711a5f77d389aa4ccca9e6d0606797431d1af8031103774c183605197"
EXPECTED_319_GUARD_HASH = "sha256:fe8e9f00a09a717ba23eb998411a2b626f94029a218d789a4ad07c6f57dff4c3"
EXPECTED_320_READINESS_MATRIX_HASH = "sha256:c1f7538331042a94d6b1e8c964688a24a91b1ea64bcbbd55f814d4e03feee860"
EXPECTED_321_RECONCILIATION_HASH = "sha256:7237998c0d31ba47ff4972c2177cdb545bb69fed87f3c64f403ade63b9be6d64"

_VERIFIED_LOOP_CHAIN_HASHES = {
    "blk306_approval_request_hash": EXPECTED_306_APPROVAL_REQUEST_HASH,
    "blk307_approval_request_contract_hash": EXPECTED_307_CONTRACT_HASH,
    "blk308_approval_challenge_record_hash": EXPECTED_308_CHALLENGE_RECORD_HASH,
    "blk309_approval_request_reconciliation_hash": EXPECTED_309_RECONCILIATION_HASH,
    "blk310_expired_attempt_hash": EXPECTED_310_EXPIRED_ATTEMPT_HASH,
    "blk311_refresh_challenge_hash": EXPECTED_311_REFRESH_CHALLENGE_HASH,
    "blk312_refresh_reconciliation_hash": EXPECTED_312_RECONCILIATION_HASH,
    "blk313_live_directive_hash": EXPECTED_313_LIVE_DIRECTIVE_HASH,
    "blk314_short_approve_guard_hash": EXPECTED_314_SHORT_APPROVE_GUARD_HASH,
    "blk315_reconciliation_hash": EXPECTED_315_RECONCILIATION_HASH,
    "blk316_standing_development_approval_hash": EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH,
    "blk281_historical_rtm_reconciliation_hash": _CANONICAL_RECONCILIATION_281_HASH,
}

_DENIED_AUTHORITIES_317_321 = (
    "STANDING_DEVELOPMENT_APPROVAL_AS_SIDE_EFFECT_APPROVAL",
    "GENERIC_OPERATOR_DIRECTIVE_AS_BEO_PUBLICATION_APPROVAL",
    "GENERIC_APPROVE_AS_SIDE_EFFECT_APPROVAL",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "BEO_CLOSEOUT_EXECUTION",
    "AUTHORITATIVE_BEO_PUBLICATION_EXECUTION",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "SIGNER_STORAGE_LEDGER_ACTION_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_EXECUTION_OR_REUSABLE_AUTHORITY",
    "DRIFT_REJECTION_OR_COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_ACCESS",
    "PRODUCTION_BLK_TEST_MCP_TRANSPORT",
    "IDENTITY_RELAY_RUNTIME_MESSAGE_DISPATCH",
    "REUSABLE_BLK003_LOOP_RUNTIME_AUTHORITY",
    "BEB_DISPATCH_WITHOUT_EXACT_PAYLOAD",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)

_SIDE_EFFECTS_317 = {
    "development_frontier_bound": True,
    "side_effect_request_prepared": False,
    "development_directive_guarded": False,
    "readiness_matrix_prepared": False,
    "development_unblock_reconciled": False,
    **_FALSE_SIDE_EFFECTS,
}
_SIDE_EFFECTS_318 = dict(_SIDE_EFFECTS_317)
_SIDE_EFFECTS_318["side_effect_request_prepared"] = True
_SIDE_EFFECTS_319 = dict(_SIDE_EFFECTS_318)
_SIDE_EFFECTS_319["development_directive_guarded"] = True
_SIDE_EFFECTS_320 = dict(_SIDE_EFFECTS_319)
_SIDE_EFFECTS_320["readiness_matrix_prepared"] = True
_SIDE_EFFECTS_321 = dict(_SIDE_EFFECTS_320)
_SIDE_EFFECTS_321["development_unblock_reconciled"] = True

_CLOCK_KEYS = frozenset(
    {
        "issued_at",
        "expires_at",
        "challenge_issued_at",
        "challenge_expires_at",
        "challenge_nonce",
        "challenge_hash",
        "short_approval_reply",
        "short_approval_reply_hash",
        "approved_at",
        "approval_expires_at",
        "run_id",
    }
)

_KEYS_317 = frozenset(
    {
        "status",
        "markers",
        "standing_development_approval_hash",
        "operator_directive_hash",
        "verified_loop_chain_hashes",
        "time_clock_required",
        "decision_boundary",
        "denied_authorities",
        "side_effects",
        "frontier_hash",
    }
)
_KEYS_318 = frozenset(
    {
        "status",
        "markers",
        "frontier_hash",
        "standing_development_approval_hash",
        "verified_loop_chain_hashes",
        "decision_mode",
        "side_effect_request_scope",
        "required_future_receipts",
        "denied_authorities",
        "side_effects",
        "request_hash",
    }
)
_KEYS_319 = frozenset(
    {
        "status",
        "markers",
        "request_hash",
        "frontier_hash",
        "operator_statement_hash",
        "classification",
        "guard_result",
        "denied_authorities",
        "side_effects",
        "guard_hash",
    }
)
_KEYS_320 = frozenset(
    {
        "status",
        "markers",
        "guard_hash",
        "readiness_rating",
        "lanes",
        "denied_authorities",
        "side_effects",
        "readiness_matrix_hash",
    }
)
_KEYS_321 = frozenset(
    {
        "status",
        "markers",
        "readiness_matrix_hash",
        "reconciled_state",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "reconciliation_hash",
    }
)

_EXPECTED_LANES = {
    "repository_development": {
        "ready": True,
        "required_decision": "standing_development_approval_active",
        "next_action": "continue_exact_sprint_packages_without_expiring_approval_clocks",
    },
    "beo_publication_finality": {
        "ready": False,
        "required_decision": "separate_exact_no_clock_decision_required",
        "next_action": "capture_exact_bounded_beo_publication_side_effect_approval_before_run_id_or_receipts",
    },
    "rtm_production_blk_link_trace_closure": {
        "ready": False,
        "required_decision": "separate_exact_no_clock_decision_required",
        "next_action": "wait_for_authoritative_current_beo_metadata_then_request_metadata_only_trace_closure",
    },
    "production_blk_test_mcp_verifier_pilot": {
        "ready": False,
        "required_decision": "separate_exact_no_clock_decision_required",
        "next_action": "pilot_one_fixed_verifier_only_transport_after_beo_rtm_chain_needs_it",
    },
    "identity_relay_runtime_pilot": {
        "ready": False,
        "required_decision": "separate_exact_no_clock_decision_required",
        "next_action": "pilot_exact_message_dispatch_only_if_receipt_path_requires_live_runtime",
    },
    "reusable_blk003_loop": {
        "ready": False,
        "required_decision": "separate_exact_no_clock_decision_required",
        "next_action": "promote_narrow_per_run_loop_only_after_one_exact_chain_is_clean",
    },
}


def build_blk_system_development_frontier_317(
    standing_approval_316: dict[str, Any],
    *,
    operator_directive: str,
) -> dict[str, Any]:
    """Bind the 9/10 development frontier to BLK-SYSTEM-316 without side effects."""

    if operator_directive != OPERATOR_DIRECTIVE_317:
        _reject_freeform(operator_directive, "operator_directive")
        raise VelocityTo9ValidationError("operator_directive is not the exact 9/10 development directive")
    record_316 = _translate_316_validation(standing_approval_316)
    package = {
        "status": "BLK_SYSTEM_9_OF_10_DEVELOPMENT_FRONTIER_BOUND",
        "markers": [
            "BLK_SYSTEM_317_9_OF_10_DEVELOPMENT_FRONTIER_BOUND",
            "STANDING_DEVELOPMENT_APPROVAL_USED_FOR_REPO_WORK_ONLY",
            "SIDE_EFFECT_APPROVALS_REMAIN_SEPARATE",
        ],
        "standing_development_approval_hash": record_316["standing_development_approval_hash"],
        "operator_directive_hash": _hash_operator_statement(operator_directive),
        "verified_loop_chain_hashes": dict(_VERIFIED_LOOP_CHAIN_HASHES),
        "time_clock_required": False,
        "decision_boundary": "repo_development_unblocked_side_effects_require_separate_exact_no_clock_decisions",
        "denied_authorities": list(_DENIED_AUTHORITIES_317_321),
        "side_effects": dict(_SIDE_EFFECTS_317),
    }
    package["frontier_hash"] = hash_package(package)
    return validate_blk_system_development_frontier_317(package)


def validate_blk_system_development_frontier_317(package_317: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_317, "BLK-SYSTEM-317 package")
    _reject_clock_keys(package)
    _require_allowed(package, _KEYS_317, "BLK-SYSTEM-317 package")
    _require_status(package, "BLK_SYSTEM_9_OF_10_DEVELOPMENT_FRONTIER_BOUND")
    _require_markers(
        package,
        (
            "BLK_SYSTEM_317_9_OF_10_DEVELOPMENT_FRONTIER_BOUND",
            "STANDING_DEVELOPMENT_APPROVAL_USED_FOR_REPO_WORK_ONLY",
            "SIDE_EFFECT_APPROVALS_REMAIN_SEPARATE",
        ),
    )
    if package.get("standing_development_approval_hash") != EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH:
        raise VelocityTo9ValidationError("standing development approval canonical hash mismatch")
    if package.get("operator_directive_hash") != _hash_operator_statement(OPERATOR_DIRECTIVE_317):
        raise VelocityTo9ValidationError("operator directive hash mismatch")
    _require_verified_loop_hashes(package.get("verified_loop_chain_hashes"))
    if package.get("time_clock_required") is not False:
        raise VelocityTo9ValidationError("time_clock_required must be false")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_317)
    _require_hash(package, "frontier_hash")
    if package["frontier_hash"] != EXPECTED_317_FRONTIER_HASH:
        raise VelocityTo9ValidationError("BLK-SYSTEM-317 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-317 package")
    return deepcopy(package)


def build_exact_no_clock_side_effect_request_318(frontier_317: dict[str, Any]) -> dict[str, Any]:
    """Prepare the exact side-effect decision surface without capturing approval."""

    frontier = validate_blk_system_development_frontier_317(frontier_317)
    package = {
        "status": "EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY_NOT_APPROVED",
        "markers": [
            "BLK_SYSTEM_318_EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY",
            "NO_CLOCK_NO_APPROVAL_CAPTURE_NO_RUN_ID",
            "BEO_RTM_BLK_LINK_SIDE_EFFECTS_STILL_SEPARATE",
        ],
        "frontier_hash": frontier["frontier_hash"],
        "standing_development_approval_hash": frontier["standing_development_approval_hash"],
        "verified_loop_chain_hashes": dict(frontier["verified_loop_chain_hashes"]),
        "decision_mode": "separate_exact_no_clock_side_effect_decision_required",
        "side_effect_request_scope": "future_one_bounded_beo_publication_then_metadata_only_rtm_blk_link_trace_closure",
        "required_future_receipts": [
            "exact_side_effect_decision_record",
            "one_run_id_consumption_record",
            "signature_receipt_hash",
            "immutable_storage_receipt_hash",
            "public_ledger_entry_hash",
            "post_publication_reconciliation_hash",
        ],
        "denied_authorities": list(_DENIED_AUTHORITIES_317_321),
        "side_effects": dict(_SIDE_EFFECTS_318),
    }
    package["request_hash"] = hash_package(package)
    return validate_exact_no_clock_side_effect_request_318(package, frontier)


def validate_exact_no_clock_side_effect_request_318(
    package_318: dict[str, Any],
    frontier_317: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _require_dict(package_318, "BLK-SYSTEM-318 package")
    _reject_clock_keys(package)
    _require_allowed(package, _KEYS_318, "BLK-SYSTEM-318 package")
    _require_status(package, "EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY_NOT_APPROVED")
    _require_markers(
        package,
        (
            "BLK_SYSTEM_318_EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY",
            "NO_CLOCK_NO_APPROVAL_CAPTURE_NO_RUN_ID",
            "BEO_RTM_BLK_LINK_SIDE_EFFECTS_STILL_SEPARATE",
        ),
    )
    if frontier_317 is not None:
        frontier = validate_blk_system_development_frontier_317(frontier_317)
        if package.get("frontier_hash") != frontier["frontier_hash"]:
            raise VelocityTo9ValidationError("frontier_hash mismatch")
        if package.get("standing_development_approval_hash") != frontier["standing_development_approval_hash"]:
            raise VelocityTo9ValidationError("standing development approval hash mismatch")
    if package.get("standing_development_approval_hash") != EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH:
        raise VelocityTo9ValidationError("standing development approval hash mismatch")
    _require_verified_loop_hashes(package.get("verified_loop_chain_hashes"))
    if package.get("decision_mode") != "separate_exact_no_clock_side_effect_decision_required":
        raise VelocityTo9ValidationError("decision_mode mismatch")
    if not isinstance(package.get("required_future_receipts"), list) or len(package["required_future_receipts"]) != 6:
        raise VelocityTo9ValidationError("required_future_receipts mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_318)
    _require_hash(package, "request_hash")
    if package["request_hash"] != EXPECTED_318_REQUEST_HASH:
        raise VelocityTo9ValidationError("BLK-SYSTEM-318 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-318 package")
    return deepcopy(package)


def evaluate_development_authority_laundering_guard_319(
    request_318: dict[str, Any],
    *,
    operator_statement: str,
) -> dict[str, Any]:
    """Guard the 9/10 directive so it cannot become side-effect approval."""

    request = validate_exact_no_clock_side_effect_request_318(request_318)
    if operator_statement != OPERATOR_DIRECTIVE_317:
        _reject_freeform(operator_statement, "operator_statement")
        raise VelocityTo9ValidationError("not a development directive for BLK-SYSTEM-317..321")
    package = {
        "status": "DEVELOPMENT_DIRECTIVE_GUARDED_NOT_SIDE_EFFECT_APPROVAL",
        "markers": [
            "BLK_SYSTEM_319_DEVELOPMENT_DIRECTIVE_GUARD_RECORDED",
            "GENERIC_9_OF_10_DIRECTIVE_NOT_SIDE_EFFECT_APPROVAL",
            "NO_APPROVAL_CAPTURE_RUN_ID_OR_PUBLICATION",
        ],
        "request_hash": request["request_hash"],
        "frontier_hash": request["frontier_hash"],
        "operator_statement_hash": _hash_operator_statement(operator_statement),
        "classification": "development_directive_only_not_side_effect_approval",
        "guard_result": "SIDE_EFFECT_APPROVAL_NOT_GRANTED",
        "denied_authorities": list(_DENIED_AUTHORITIES_317_321),
        "side_effects": dict(_SIDE_EFFECTS_319),
    }
    package["guard_hash"] = hash_package(package)
    return validate_development_authority_laundering_guard_319(package, request)


def validate_development_authority_laundering_guard_319(
    package_319: dict[str, Any],
    request_318: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _require_dict(package_319, "BLK-SYSTEM-319 package")
    _reject_clock_keys(package)
    _require_allowed(package, _KEYS_319, "BLK-SYSTEM-319 package")
    _require_status(package, "DEVELOPMENT_DIRECTIVE_GUARDED_NOT_SIDE_EFFECT_APPROVAL")
    _require_markers(
        package,
        (
            "BLK_SYSTEM_319_DEVELOPMENT_DIRECTIVE_GUARD_RECORDED",
            "GENERIC_9_OF_10_DIRECTIVE_NOT_SIDE_EFFECT_APPROVAL",
            "NO_APPROVAL_CAPTURE_RUN_ID_OR_PUBLICATION",
        ),
    )
    if request_318 is not None:
        request = validate_exact_no_clock_side_effect_request_318(request_318)
        if package.get("request_hash") != request["request_hash"]:
            raise VelocityTo9ValidationError("request_hash mismatch")
        if package.get("frontier_hash") != request["frontier_hash"]:
            raise VelocityTo9ValidationError("frontier_hash mismatch")
    if package.get("operator_statement_hash") != _hash_operator_statement(OPERATOR_DIRECTIVE_317):
        raise VelocityTo9ValidationError("operator_statement_hash mismatch")
    if package.get("classification") != "development_directive_only_not_side_effect_approval":
        raise VelocityTo9ValidationError("classification mismatch")
    if package.get("guard_result") != "SIDE_EFFECT_APPROVAL_NOT_GRANTED":
        raise VelocityTo9ValidationError("guard_result mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_319)
    _require_hash(package, "guard_hash")
    if package["guard_hash"] != EXPECTED_319_GUARD_HASH:
        raise VelocityTo9ValidationError("BLK-SYSTEM-319 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-319 package")
    return deepcopy(package)


def build_blk_system_9_of_10_readiness_matrix_320(guard_319: dict[str, Any]) -> dict[str, Any]:
    """Record the 9/10 readiness matrix after the development-only guard."""

    guard = validate_development_authority_laundering_guard_319(guard_319)
    package = {
        "status": "BLK_SYSTEM_9_OF_10_READINESS_MATRIX_READY_SIDE_EFFECTS_SEPARATE",
        "markers": [
            "BLK_SYSTEM_320_9_OF_10_READINESS_MATRIX_READY",
            "REPO_DEVELOPMENT_READY_SIDE_EFFECTS_BLOCKED",
            "ONE_REAL_END_TO_END_LOOP_REQUIRES_SEPARATE_DECISIONS",
        ],
        "guard_hash": guard["guard_hash"],
        "readiness_rating": "8.5/10_repo_development_ready_side_effects_blocked",
        "lanes": deepcopy(_EXPECTED_LANES),
        "denied_authorities": list(_DENIED_AUTHORITIES_317_321),
        "side_effects": dict(_SIDE_EFFECTS_320),
    }
    package["readiness_matrix_hash"] = hash_package(package)
    return validate_blk_system_9_of_10_readiness_matrix_320(package, guard)


def validate_blk_system_9_of_10_readiness_matrix_320(
    package_320: dict[str, Any],
    guard_319: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _require_dict(package_320, "BLK-SYSTEM-320 package")
    _reject_clock_keys(package)
    _require_allowed(package, _KEYS_320, "BLK-SYSTEM-320 package")
    _require_status(package, "BLK_SYSTEM_9_OF_10_READINESS_MATRIX_READY_SIDE_EFFECTS_SEPARATE")
    _require_markers(
        package,
        (
            "BLK_SYSTEM_320_9_OF_10_READINESS_MATRIX_READY",
            "REPO_DEVELOPMENT_READY_SIDE_EFFECTS_BLOCKED",
            "ONE_REAL_END_TO_END_LOOP_REQUIRES_SEPARATE_DECISIONS",
        ),
    )
    if guard_319 is not None:
        guard = validate_development_authority_laundering_guard_319(guard_319)
        if package.get("guard_hash") != guard["guard_hash"]:
            raise VelocityTo9ValidationError("guard_hash mismatch")
    if package.get("readiness_rating") != "8.5/10_repo_development_ready_side_effects_blocked":
        raise VelocityTo9ValidationError("readiness_rating mismatch")
    _require_lanes(package.get("lanes"))
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_320)
    _require_hash(package, "readiness_matrix_hash")
    if package["readiness_matrix_hash"] != EXPECTED_320_READINESS_MATRIX_HASH:
        raise VelocityTo9ValidationError("BLK-SYSTEM-320 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-320 package")
    return deepcopy(package)


def reconcile_blk_system_development_unblock_321(matrix_320: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the 9/10 development-unblock package to the next exact frontier."""

    matrix = validate_blk_system_9_of_10_readiness_matrix_320(matrix_320)
    package = {
        "status": "BLK_SYSTEM_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED",
        "markers": [
            "BLK_SYSTEM_321_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED",
            NEXT_FRONTIER_321,
            "SIDE_EFFECT_APPROVALS_SEPARATE_NOT_GRANTED",
        ],
        "readiness_matrix_hash": matrix["readiness_matrix_hash"],
        "reconciled_state": "repo_development_ready_for_9_of_10_side_effect_lanes_waiting_exact_decisions",
        "next_frontier": NEXT_FRONTIER_321,
        "denied_authorities": list(_DENIED_AUTHORITIES_317_321),
        "side_effects": dict(_SIDE_EFFECTS_321),
    }
    package["reconciliation_hash"] = hash_package(package)
    return validate_blk_system_development_unblock_reconciliation_321(package, matrix)


def validate_blk_system_development_unblock_reconciliation_321(
    package_321: dict[str, Any],
    matrix_320: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _require_dict(package_321, "BLK-SYSTEM-321 package")
    _reject_clock_keys(package)
    _require_allowed(package, _KEYS_321, "BLK-SYSTEM-321 package")
    _require_status(package, "BLK_SYSTEM_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED")
    _require_markers(
        package,
        (
            "BLK_SYSTEM_321_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED",
            NEXT_FRONTIER_321,
            "SIDE_EFFECT_APPROVALS_SEPARATE_NOT_GRANTED",
        ),
    )
    if matrix_320 is not None:
        matrix = validate_blk_system_9_of_10_readiness_matrix_320(matrix_320)
        if package.get("readiness_matrix_hash") != matrix["readiness_matrix_hash"]:
            raise VelocityTo9ValidationError("readiness_matrix_hash mismatch")
    if package.get("next_frontier") != NEXT_FRONTIER_321:
        raise VelocityTo9ValidationError("next_frontier mismatch")
    if package.get("reconciled_state") != "repo_development_ready_for_9_of_10_side_effect_lanes_waiting_exact_decisions":
        raise VelocityTo9ValidationError("reconciled_state mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"), _SIDE_EFFECTS_321)
    _require_hash(package, "reconciliation_hash")
    if package["reconciliation_hash"] != EXPECTED_321_RECONCILIATION_HASH:
        raise VelocityTo9ValidationError("BLK-SYSTEM-321 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-321 package")
    return deepcopy(package)


def _translate_316_validation(record_316: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_blk_system_standing_development_approval_316(record_316)
    except ValueError as exc:
        raise VelocityTo9ValidationError(f"standing development approval invalid: {exc}") from exc


def _hash_operator_statement(statement: str) -> str:
    return hash_package({"operator_statement": statement})


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VelocityTo9ValidationError(f"{context} must be a dictionary")
    return value


def _reject_clock_keys(package: dict[str, Any]) -> None:
    present = sorted(set(package) & _CLOCK_KEYS)
    if present:
        raise VelocityTo9ValidationError(f"time clock or run-id keys are not allowed here: {present!r}")


def _require_allowed(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    try:
        _require_allowed_keys(package, allowed, context)
    except ValueError as exc:
        raise VelocityTo9ValidationError(str(exc)) from exc


def _require_status(package: dict[str, Any], expected: str) -> None:
    if package.get("status") != expected:
        raise VelocityTo9ValidationError("status mismatch")


def _require_markers(package: dict[str, Any], expected: tuple[str, ...]) -> None:
    if tuple(package.get("markers", ())) != expected:
        raise VelocityTo9ValidationError("markers mismatch")


def _require_verified_loop_hashes(value: Any) -> None:
    hashes = _require_dict(value, "verified_loop_chain_hashes")
    if hashes != _VERIFIED_LOOP_CHAIN_HASHES:
        raise VelocityTo9ValidationError("verified loop chain hash mismatch")


def _require_denied_authorities(value: Any) -> None:
    if not isinstance(value, list):
        raise VelocityTo9ValidationError("denied_authorities must be a list")
    if tuple(value) != _DENIED_AUTHORITIES_317_321:
        raise VelocityTo9ValidationError("denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise VelocityTo9ValidationError("denied_authorities must not contain duplicates")


def _require_side_effects(value: Any, expected: dict[str, bool]) -> None:
    side_effects = _require_dict(value, "side_effects")
    if side_effects != expected:
        raise VelocityTo9ValidationError("side_effects mismatch")


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise VelocityTo9ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise VelocityTo9ValidationError(f"{field} canonical hash mismatch")


def _require_lanes(value: Any) -> None:
    lanes = _require_dict(value, "lanes")
    if set(lanes) != set(_EXPECTED_LANES):
        raise VelocityTo9ValidationError("lanes mismatch")
    for lane, expected in _EXPECTED_LANES.items():
        lane_value = _require_dict(lanes.get(lane), f"lanes.{lane}")
        if set(lane_value) != {"ready", "required_decision", "next_action"}:
            raise VelocityTo9ValidationError("lane schema mismatch")
        if lane_value != expected:
            raise VelocityTo9ValidationError("lane decision mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise VelocityTo9ValidationError("; ".join(findings))


def _scan_package(package: dict[str, Any], path: str) -> None:
    findings = scan_for_authority_laundering(package, path)
    if findings:
        raise VelocityTo9ValidationError("; ".join(findings))
