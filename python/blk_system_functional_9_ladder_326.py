"""BLK-SYSTEM-326 functional 9/10 execution ladder gate.

This package converts the operator's functional 9/10 request into an exact sprint
ladder and executes the only authority-safe part now: the plan/gate record. It
does not treat the broad functional target as BEO publication, run-ID, RTM,
production blk-link, protected-body, runtime/tooling, or mutation authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_overall_9_guard_325 import (
    EXPECTED_325_OVERALL_GUARD_HASH,
    validate_overall_9_development_directive_guard_325,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _require_allowed_keys,
    hash_package,
)


class FunctionalNineLadder326ValidationError(ValueError):
    """Raised when BLK-SYSTEM-326 evidence launders functional authority."""


OPERATOR_DIRECTIVE_326 = "plan and execute all blk-system sprints to get blk-system to be functionally 9/10 overall"
NEXT_FRONTIER_326 = "NEXT_FRONTIER_FUNCTIONAL_9_EXACT_BEO_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED"
EXPECTED_326_FUNCTIONAL_9_LADDER_HASH: str | None = "sha256:05bf576178f5e848c2b98a70eae42873916f00ee816ce51f3744d575466cae4a"

_MARKERS_326 = (
    "BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY",
    "FUNCTIONAL_9_LADDER_EXECUTED_TO_CURRENT_AUTHORITY_BOUNDARY",
    "BROAD_FUNCTIONAL_9_DIRECTIVE_NOT_SIDE_EFFECT_DECISION",
)
_DENIED_AUTHORITIES_326 = (
    "BROAD_FUNCTIONAL_9_DIRECTIVE_AS_SIDE_EFFECT_DECISION",
    "CURRENT_MESSAGE_AS_CURRENT_BEO_PUBLICATION_DECISION",
    "RUN_ID_MOVEMENT",
    "BEO_CLOSEOUT_EXECUTION",
    "AUTHORITATIVE_BEO_PUBLICATION_EXECUTION",
    "REUSABLE_BEO_PUBLICATION_SURFACE",
    "SIGNER_STORAGE_LEDGER_SURFACE_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION_OR_REUSABLE_RTM_SURFACE",
    "PRODUCTION_BLK_LINK_OR_REUSABLE_SURFACE",
    "DRIFT_REJECTION_OR_COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_ACCESS",
    "PRODUCTION_BLK_TEST_MCP_TRANSPORT",
    "IDENTITY_RELAY_RUNTIME_MESSAGE_DISPATCH",
    "REUSABLE_BLK003_LOOP_RUNTIME_SURFACE",
    "BEB_DISPATCH_WITHOUT_EXACT_PAYLOAD",
    "TARGET_SOURCE_GIT_MUTATION_OUTSIDE_EXACT_BLK_SYSTEM_SPRINT_DISCIPLINE",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
    "TEN_OF_TEN_FINALITY_CLAIM",
)
_FUNCTIONAL_LADDER_326 = (
    {
        "sprint": "326",
        "phase": "functional_9_ladder_plan_and_boundary_gate",
        "objective": "record_exact_dependency_order_for_functional_9_target",
        "status": "executed_now",
        "can_execute_under_current_message": True,
        "blocker": "none_for_plan_record",
    },
    {
        "sprint": "327-329",
        "phase": "current_verified_loop_beo_publication_decision",
        "objective": "current_beo_publication_bounded_run_and_reconciliation",
        "status": "blocked",
        "can_execute_under_current_message": False,
        "blocker": "separate_exact_side_effect_decision_required",
    },
    {
        "sprint": "330-333",
        "phase": "rtm_production_blk_link_reopen_after_current_beo",
        "objective": "metadata_trace_closure_then_one_bounded_blk_link_record",
        "status": "blocked",
        "can_execute_under_current_message": False,
        "blocker": "blocked_until_current_beo_metadata_exists",
    },
    {
        "sprint": "334-336",
        "phase": "production_blk_test_mcp_transport_pilot_if_needed",
        "objective": "turn_verifier_only_oracle_into_bounded_transport_pilot_only_if_chain_needs_it",
        "status": "deferred",
        "can_execute_under_current_message": False,
        "blocker": "deferred_until_one_exact_chain_is_clean",
    },
    {
        "sprint": "337-339",
        "phase": "identity_relay_runtime_pilot_if_needed",
        "objective": "convert_local_identity_relay_evidence_to_one_bounded_runtime_pilot_only_if_needed",
        "status": "deferred",
        "can_execute_under_current_message": False,
        "blocker": "deferred_until_one_exact_chain_is_clean",
    },
    {
        "sprint": "340-343",
        "phase": "reusable_blk003_loop_runtime_decision_if_needed",
        "objective": "evaluate_reusable_loop_after_one_exact_chain_proves_repeatable_need",
        "status": "deferred",
        "can_execute_under_current_message": False,
        "blocker": "deferred_until_one_exact_chain_is_clean",
    },
    {
        "sprint": "344-347",
        "phase": "drift_coverage_truth_metadata_path_if_needed",
        "objective": "reopen_truth_surfaces_only_after_metadata_chain_and_operator_selection",
        "status": "deferred",
        "can_execute_under_current_message": False,
        "blocker": "deferred_until_metadata_chain_is_clean",
    },
)
_SIDE_EFFECTS_326 = {
    "functional_9_ladder_recorded": True,
    "functional_9_plan_boundary_executed": True,
    "functional_9_side_effect_decision_captured": False,
    "functional_9_finality_claimed": False,
    **_FALSE_SIDE_EFFECTS,
}
_KEYS_326 = frozenset(
    {
        "status",
        "markers",
        "overall_guard_hash",
        "operator_directive_hash",
        "classification",
        "current_overall_rating",
        "target_overall_rating",
        "functional_ladder",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "ladder_hash",
    }
)
_LADDER_KEYS = frozenset(
    {
        "sprint",
        "phase",
        "objective",
        "status",
        "can_execute_under_current_message",
        "blocker",
    }
)


def build_functional_9_execution_ladder_326(
    overall_guard_325: dict[str, Any],
    *,
    operator_directive: str,
) -> dict[str, Any]:
    """Record the functional-9 ladder and stop at the current cutline."""

    guard = _validate_325_dependency(overall_guard_325)
    if operator_directive != OPERATOR_DIRECTIVE_326:
        _reject_freeform(operator_directive, "operator_directive")
        raise FunctionalNineLadder326ValidationError("operator_directive mismatch")

    package = {
        "status": "BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY",
        "markers": list(_MARKERS_326),
        "overall_guard_hash": guard["guard_hash"],
        "operator_directive_hash": _hash_text(operator_directive),
        "classification": "functional_9_plan_executed_to_authority_boundary",
        "current_overall_rating": "7/10_practical_overall_baseline",
        "target_overall_rating": "9/10_functional_target_requires_exact_side_effect_chain",
        "functional_ladder": deepcopy(list(_FUNCTIONAL_LADDER_326)),
        "next_frontier": NEXT_FRONTIER_326,
        "denied_authorities": list(_DENIED_AUTHORITIES_326),
        "side_effects": dict(_SIDE_EFFECTS_326),
    }
    package["ladder_hash"] = hash_package(package)
    return validate_functional_9_execution_ladder_326(package)


def validate_functional_9_execution_ladder_326(package_326: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_326, "BLK-SYSTEM-326 package")
    try:
        _require_allowed_keys(package, _KEYS_326, "BLK-SYSTEM-326 package")
    except ValueError as exc:
        raise FunctionalNineLadder326ValidationError(str(exc)) from exc
    if package.get("status") != "BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY":
        raise FunctionalNineLadder326ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_326:
        raise FunctionalNineLadder326ValidationError("markers mismatch")
    if package.get("overall_guard_hash") != EXPECTED_325_OVERALL_GUARD_HASH:
        raise FunctionalNineLadder326ValidationError("325 overall guard hash mismatch")
    if package.get("operator_directive_hash") != _hash_text(OPERATOR_DIRECTIVE_326):
        raise FunctionalNineLadder326ValidationError("operator_directive_hash mismatch")
    if package.get("classification") != "functional_9_plan_executed_to_authority_boundary":
        raise FunctionalNineLadder326ValidationError("classification mismatch")
    if package.get("current_overall_rating") != "7/10_practical_overall_baseline":
        raise FunctionalNineLadder326ValidationError("current_overall_rating mismatch")
    if package.get("target_overall_rating") != "9/10_functional_target_requires_exact_side_effect_chain":
        raise FunctionalNineLadder326ValidationError("target_overall_rating mismatch")
    _require_functional_ladder(package.get("functional_ladder"))
    if package.get("next_frontier") != NEXT_FRONTIER_326:
        raise FunctionalNineLadder326ValidationError("next_frontier mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"))
    _require_hash(package, "ladder_hash")
    if EXPECTED_326_FUNCTIONAL_9_LADDER_HASH is not None:
        if package["ladder_hash"] != EXPECTED_326_FUNCTIONAL_9_LADDER_HASH:
            raise FunctionalNineLadder326ValidationError("BLK-SYSTEM-326 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-326 package")
    return deepcopy(package)


def _validate_325_dependency(overall_guard_325: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_overall_9_development_directive_guard_325(overall_guard_325)
    except ValueError as exc:
        raise FunctionalNineLadder326ValidationError(f"325 overall guard dependency invalid: {exc}") from exc


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FunctionalNineLadder326ValidationError(f"{context} must be a dictionary")
    return value


def _require_denied_authorities(value: Any) -> None:
    if not isinstance(value, list):
        raise FunctionalNineLadder326ValidationError("denied_authorities must be a list")
    if tuple(value) != _DENIED_AUTHORITIES_326:
        raise FunctionalNineLadder326ValidationError("denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise FunctionalNineLadder326ValidationError("denied_authorities must not contain duplicates")


def _require_side_effects(value: Any) -> None:
    side_effects = _require_dict(value, "side_effects")
    if side_effects != _SIDE_EFFECTS_326:
        raise FunctionalNineLadder326ValidationError("side_effects mismatch")


def _require_functional_ladder(value: Any) -> None:
    if not isinstance(value, list):
        raise FunctionalNineLadder326ValidationError("functional_ladder must be a list")
    expected = deepcopy(list(_FUNCTIONAL_LADDER_326))
    if value != expected:
        raise FunctionalNineLadder326ValidationError("functional_ladder mismatch or side effect boundary changed")
    if value[0].get("can_execute_under_current_message") is not True:
        raise FunctionalNineLadder326ValidationError("functional_ladder first sprint must be executable")
    for item in value[1:]:
        if item.get("can_execute_under_current_message") is not False:
            raise FunctionalNineLadder326ValidationError("functional_ladder side effect sprint cannot execute now")
        if item.get("status") not in {"blocked", "deferred"}:
            raise FunctionalNineLadder326ValidationError("functional_ladder side effect sprint must remain blocked or deferred")
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise FunctionalNineLadder326ValidationError("functional_ladder items must be dictionaries")
        try:
            _require_allowed_keys(item, _LADDER_KEYS, f"functional_ladder[{index}]")
        except ValueError as exc:
            raise FunctionalNineLadder326ValidationError(str(exc)) from exc


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise FunctionalNineLadder326ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise FunctionalNineLadder326ValidationError(f"{field} canonical hash mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise FunctionalNineLadder326ValidationError("; ".join(findings))


def _scan_package(package: dict[str, Any], path: str) -> None:
    findings = scan_for_authority_laundering(package, path)
    if findings:
        raise FunctionalNineLadder326ValidationError("; ".join(findings))
