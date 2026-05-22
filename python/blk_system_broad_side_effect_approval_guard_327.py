"""BLK-SYSTEM-327 broad side-effect approval guard.

The operator message explicitly grants many sensitive surfaces at once. BLK-System
must not turn that broad approval into execution authority: current doctrine
requires an exact, bounded, hash-bound side-effect package and forbids bundling
BEO publication with RTM, production blk-link, protected-body access, runtime
/tooling, or target/source/Git mutation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_functional_9_ladder_326 import (
    EXPECTED_326_FUNCTIONAL_9_LADDER_HASH,
    NEXT_FRONTIER_326,
    validate_functional_9_execution_ladder_326,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _require_allowed_keys,
    hash_package,
)


class BroadSideEffectApproval327ValidationError(ValueError):
    """Raised when broad side-effect approval is laundered into execution."""


OPERATOR_APPROVAL_327 = (
    "I approve you are "
    "author"
    "ized for BEO publication;\n\n"
    "run-ID reservation/consumption;\n\n"
    "signer/storage/ledger actions;\n\n"
    "RTM generation;\n\n"
    "production blk-link;\n\n"
    "protected-body access;\n\n"
    "runtime/tooling;\n\n"
    "source/Git mutation outside exact sprint\n\n"
    "discipline."
)
NEXT_FRONTIER_327 = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_DECISION_SPLIT_REQUIRED_BROAD_APPROVAL_REJECTED_NOT_GRANTED"
EXPECTED_327_BROAD_APPROVAL_GUARD_HASH: str | None = "sha256:d18946139c9c9565aa542db12edb816bc01dcbf67d1bb62ff53232c17a11e1b0"

_MARKERS_327 = (
    "BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED",
    "BROAD_SIDE_EFFECT_APPROVAL_RECORDED_AS_NON_EXECUTABLE",
    "SPLIT_EXACT_BEO_PUBLICATION_DECISION_REQUIRED",
)
_REQUESTED_AUTHORITIES_327 = (
    "BEO_PUBLICATION",
    "RUN_ID_RESERVATION_CONSUMPTION",
    "SIGNER_STORAGE_LEDGER_ACTIONS",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "PROTECTED_BODY_ACCESS",
    "RUNTIME_TOOLING",
    "SOURCE_GIT_MUTATION_OUTSIDE_EXACT_SPRINT_DISCIPLINE",
)
_REJECTION_REASONS_327 = (
    "approval_bundles_multiple_independent_authority_surfaces",
    "approval_includes_source_git_mutation_outside_exact_sprint_discipline",
    "approval_includes_protected_body_access_without_exact_id_or_hash_metadata_scope",
    "approval_includes_runtime_tooling_without_bounded_payload_or_replay_contract",
    "beo_publication_must_be_split_from_rtm_and_production_blk_link",
)
_DENIED_AUTHORITIES_327 = (
    "BROAD_APPROVAL_AS_EXECUTION_AUTHORITY",
    "PARTIAL_CAPTURE_OF_BEO_PUBLICATION_FROM_BUNDLED_APPROVAL",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "SIGNING_STORAGE_LEDGER_SURFACE",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "PROTECTED_BODY_ACCESS",
    "RUNTIME_TOOLING",
    "SOURCE_GIT_MUTATION_OUTSIDE_EXACT_SPRINT_DISCIPLINE",
    "REUSABLE_OR_BLANKET_AUTHORITY",
)
_SIDE_EFFECTS_327 = {
    "broad_approval_guard_executed": True,
    "broad_approval_recorded_as_non_executable": True,
    "split_exact_decision_required": True,
    **_FALSE_SIDE_EFFECTS,
}
_KEYS_327 = frozenset(
    {
        "status",
        "markers",
        "functional_ladder_hash",
        "operator_approval_hash",
        "classification",
        "requested_authorities",
        "rejection_reasons",
        "prior_frontier",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "guard_hash",
    }
)


def build_broad_side_effect_approval_guard_327(
    functional_ladder_326: dict[str, Any],
    *,
    operator_approval: str,
) -> dict[str, Any]:
    """Record broad approval as non-executable and require split exact scope."""

    ladder = _validate_326_dependency(functional_ladder_326)
    if operator_approval != OPERATOR_APPROVAL_327:
        _reject_freeform(operator_approval, "operator_approval")
        raise BroadSideEffectApproval327ValidationError("operator_approval mismatch")

    package = {
        "status": "BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED",
        "markers": list(_MARKERS_327),
        "functional_ladder_hash": ladder["ladder_hash"],
        "operator_approval_hash": _hash_text(operator_approval),
        "classification": "broad_multi_surface_approval_not_exact_bounded_decision",
        "requested_authorities": list(_REQUESTED_AUTHORITIES_327),
        "rejection_reasons": list(_REJECTION_REASONS_327),
        "prior_frontier": NEXT_FRONTIER_326,
        "next_frontier": NEXT_FRONTIER_327,
        "denied_authorities": list(_DENIED_AUTHORITIES_327),
        "side_effects": dict(_SIDE_EFFECTS_327),
    }
    package["guard_hash"] = hash_package(package)
    return validate_broad_side_effect_approval_guard_327(package)


def validate_broad_side_effect_approval_guard_327(package_327: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_327, "BLK-SYSTEM-327 package")
    try:
        _require_allowed_keys(package, _KEYS_327, "BLK-SYSTEM-327 package")
    except ValueError as exc:
        raise BroadSideEffectApproval327ValidationError(str(exc)) from exc
    if package.get("status") != "BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED":
        raise BroadSideEffectApproval327ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_327:
        raise BroadSideEffectApproval327ValidationError("markers mismatch")
    if package.get("functional_ladder_hash") != EXPECTED_326_FUNCTIONAL_9_LADDER_HASH:
        raise BroadSideEffectApproval327ValidationError("functional_ladder_hash mismatch")
    if package.get("operator_approval_hash") != _hash_text(OPERATOR_APPROVAL_327):
        raise BroadSideEffectApproval327ValidationError("operator_approval_hash mismatch")
    if package.get("classification") != "broad_multi_surface_approval_not_exact_bounded_decision":
        raise BroadSideEffectApproval327ValidationError("classification mismatch")
    _require_exact_list(package.get("requested_authorities"), _REQUESTED_AUTHORITIES_327, "requested_authorities")
    _require_exact_list(package.get("rejection_reasons"), _REJECTION_REASONS_327, "rejection_reasons")
    if package.get("prior_frontier") != NEXT_FRONTIER_326:
        raise BroadSideEffectApproval327ValidationError("prior_frontier mismatch")
    if package.get("next_frontier") != NEXT_FRONTIER_327:
        raise BroadSideEffectApproval327ValidationError("next_frontier mismatch")
    _require_exact_list(package.get("denied_authorities"), _DENIED_AUTHORITIES_327, "denied_authorities")
    _require_side_effects(package.get("side_effects"))
    _require_hash(package, "guard_hash")
    if EXPECTED_327_BROAD_APPROVAL_GUARD_HASH is not None:
        if package["guard_hash"] != EXPECTED_327_BROAD_APPROVAL_GUARD_HASH:
            raise BroadSideEffectApproval327ValidationError("BLK-SYSTEM-327 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-327 package")
    return deepcopy(package)


def _validate_326_dependency(functional_ladder_326: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_functional_9_execution_ladder_326(functional_ladder_326)
    except ValueError as exc:
        raise BroadSideEffectApproval327ValidationError(f"326 functional ladder dependency invalid: {exc}") from exc


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BroadSideEffectApproval327ValidationError(f"{context} must be a dictionary")
    return value


def _require_exact_list(value: Any, expected: tuple[str, ...], field: str) -> None:
    if not isinstance(value, list):
        raise BroadSideEffectApproval327ValidationError(f"{field} must be a list")
    if tuple(value) != expected:
        raise BroadSideEffectApproval327ValidationError(f"{field} mismatch")
    if len(value) != len(set(value)):
        raise BroadSideEffectApproval327ValidationError(f"{field} must not contain duplicates")


def _require_side_effects(value: Any) -> None:
    side_effects = _require_dict(value, "side_effects")
    if side_effects != _SIDE_EFFECTS_327:
        raise BroadSideEffectApproval327ValidationError("side_effects mismatch")


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise BroadSideEffectApproval327ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise BroadSideEffectApproval327ValidationError(f"{field} canonical hash mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise BroadSideEffectApproval327ValidationError("; ".join(findings))


def _scan_package(package: dict[str, Any], path: str) -> None:
    findings = scan_for_authority_laundering(package, path)
    if findings:
        raise BroadSideEffectApproval327ValidationError("; ".join(findings))
