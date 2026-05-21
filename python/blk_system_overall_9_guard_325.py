"""BLK-SYSTEM-325 overall 9/10 directive guard.

This package records the operator's new practical-overall 9/10 target as
BLK-System repository-development direction only. It deliberately does not turn
that broad target into BEO publication, run-ID, RTM, production blk-link,
protected-body, runtime/tooling, or mutation authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_first_pass_9_9_322 import (
    EXPECTED_322_FIRST_PASS_HASH,
    validate_blk001_006_roadmap_first_pass_done_322,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _require_allowed_keys,
    hash_package,
)


class OverallNineGuard325ValidationError(ValueError):
    """Raised when BLK-SYSTEM-325 evidence launders side-effect authority."""


OPERATOR_DIRECTIVE_325 = "plan and execute all blk-system sprints to get blk-system to 9/10 overall"
NEXT_FRONTIER_325 = "NEXT_FRONTIER_9_OF_10_OVERALL_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED"
EXPECTED_325_OVERALL_GUARD_HASH: str | None = "sha256:18f9550996bc0388e67666237c0e95d81906ce30162c184401149eeffb31dd3e"

_MARKERS_325 = (
    "BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED",
    "OVERALL_9_TARGET_NOT_SIDE_EFFECT_APPROVAL",
    "FUNCTIONAL_9_REQUIRES_EXACT_SIDE_EFFECT_DECISION",
)
_DENIED_AUTHORITIES_325 = (
    "BROAD_9_OF_10_DIRECTIVE_AS_SIDE_EFFECT_APPROVAL",
    "OPERATOR_REVIEW_AS_SIDE_EFFECT_APPROVAL",
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
    "TARGET_SOURCE_GIT_MUTATION_OUTSIDE_EXACT_BLK_SYSTEM_SPRINT_DISCIPLINE",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
    "TEN_OF_TEN_FINALITY_CLAIM",
)
_TARGET_GAP_CLOSURE_PLAN = (
    {
        "lane": "current_verified_loop_beo_publication",
        "current_status": "request_and_review_ready_side_effect_not_granted",
        "required_decision": "separate_exact_no_clock_side_effect_decision_required",
        "side_effect_now": False,
    },
    {
        "lane": "rtm_production_blk_link_trace_closure",
        "current_status": "blocked_until_authoritative_current_beo_metadata_exists",
        "required_decision": "requires_clean_current_beo_finality_first",
        "side_effect_now": False,
    },
    {
        "lane": "reusable_runtime_surfaces",
        "current_status": "deferred_until_one_exact_chain_is_clean",
        "required_decision": "defer_broad_runtime_until_observed_need",
        "side_effect_now": False,
    },
)
_SIDE_EFFECTS_325 = {
    "overall_9_directive_guarded": True,
    "overall_9_target_selected": True,
    "overall_9_side_effect_decision_captured": False,
    "overall_9_finality_claimed": False,
    **_FALSE_SIDE_EFFECTS,
}
_KEYS_325 = frozenset(
    {
        "status",
        "markers",
        "first_pass_hash",
        "operator_directive_hash",
        "classification",
        "current_overall_rating",
        "target_overall_rating",
        "target_gap_closure_plan",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "guard_hash",
    }
)


def build_overall_9_development_directive_guard_325(
    first_pass_322: dict[str, Any],
    *,
    operator_directive: str,
) -> dict[str, Any]:
    """Classify the new overall-9 directive without granting side effects."""

    first_pass = _validate_322_dependency(first_pass_322)
    if operator_directive != OPERATOR_DIRECTIVE_325:
        _reject_freeform(operator_directive, "operator_directive")
        raise OverallNineGuard325ValidationError("operator_directive mismatch")

    package = {
        "status": "BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED",
        "markers": list(_MARKERS_325),
        "first_pass_hash": first_pass["first_pass_hash"],
        "operator_directive_hash": _hash_text(operator_directive),
        "classification": "development_directive_only_not_side_effect_approval",
        "current_overall_rating": "7/10_practical_overall_baseline",
        "target_overall_rating": "9/10_overall_requires_exact_side_effect_decision",
        "target_gap_closure_plan": deepcopy(list(_TARGET_GAP_CLOSURE_PLAN)),
        "next_frontier": NEXT_FRONTIER_325,
        "denied_authorities": list(_DENIED_AUTHORITIES_325),
        "side_effects": dict(_SIDE_EFFECTS_325),
    }
    package["guard_hash"] = hash_package(package)
    return validate_overall_9_development_directive_guard_325(package)


def validate_overall_9_development_directive_guard_325(package_325: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_325, "BLK-SYSTEM-325 package")
    try:
        _require_allowed_keys(package, _KEYS_325, "BLK-SYSTEM-325 package")
    except ValueError as exc:
        raise OverallNineGuard325ValidationError(str(exc)) from exc
    if package.get("status") != "BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED":
        raise OverallNineGuard325ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_325:
        raise OverallNineGuard325ValidationError("markers mismatch")
    if package.get("first_pass_hash") != EXPECTED_322_FIRST_PASS_HASH:
        raise OverallNineGuard325ValidationError("first pass hash mismatch")
    if package.get("operator_directive_hash") != _hash_text(OPERATOR_DIRECTIVE_325):
        raise OverallNineGuard325ValidationError("operator_directive_hash mismatch")
    if package.get("classification") != "development_directive_only_not_side_effect_approval":
        raise OverallNineGuard325ValidationError("classification mismatch")
    if package.get("current_overall_rating") != "7/10_practical_overall_baseline":
        raise OverallNineGuard325ValidationError("current_overall_rating mismatch")
    if package.get("target_overall_rating") != "9/10_overall_requires_exact_side_effect_decision":
        raise OverallNineGuard325ValidationError("target_overall_rating mismatch")
    _require_target_gap_closure_plan(package.get("target_gap_closure_plan"))
    if package.get("next_frontier") != NEXT_FRONTIER_325:
        raise OverallNineGuard325ValidationError("next_frontier mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"))
    _require_hash(package, "guard_hash")
    if EXPECTED_325_OVERALL_GUARD_HASH is not None:
        if package["guard_hash"] != EXPECTED_325_OVERALL_GUARD_HASH:
            raise OverallNineGuard325ValidationError("BLK-SYSTEM-325 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-325 package")
    return deepcopy(package)


def _validate_322_dependency(first_pass_322: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_blk001_006_roadmap_first_pass_done_322(first_pass_322)
    except ValueError as exc:
        raise OverallNineGuard325ValidationError(f"322 first pass dependency invalid: {exc}") from exc


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OverallNineGuard325ValidationError(f"{context} must be a dictionary")
    return value


def _require_denied_authorities(value: Any) -> None:
    if not isinstance(value, list):
        raise OverallNineGuard325ValidationError("denied_authorities must be a list")
    if tuple(value) != _DENIED_AUTHORITIES_325:
        raise OverallNineGuard325ValidationError("denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise OverallNineGuard325ValidationError("denied_authorities must not contain duplicates")


def _require_side_effects(value: Any) -> None:
    side_effects = _require_dict(value, "side_effects")
    if side_effects != _SIDE_EFFECTS_325:
        raise OverallNineGuard325ValidationError("side_effects mismatch")


def _require_target_gap_closure_plan(value: Any) -> None:
    if not isinstance(value, list):
        raise OverallNineGuard325ValidationError("target_gap_closure_plan must be a list")
    expected = deepcopy(list(_TARGET_GAP_CLOSURE_PLAN))
    if value != expected:
        raise OverallNineGuard325ValidationError("target_gap_closure_plan mismatch")


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise OverallNineGuard325ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise OverallNineGuard325ValidationError(f"{field} canonical hash mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise OverallNineGuard325ValidationError("; ".join(findings))


def _scan_package(package: dict[str, Any], path: str) -> None:
    findings = scan_for_authority_laundering(package, path)
    if findings:
        raise OverallNineGuard325ValidationError("; ".join(findings))
