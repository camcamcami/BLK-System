"""BLK-SYSTEM-328 development authority distinction package.

This package records the operator correction that Hermes has standing authority to
work on all BLK-System development without per-sprint/action approval. It
separates that development authority from BLK-System's internal product/runtime
requirements and evidence gates.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_broad_side_effect_approval_guard_327 import (
    EXPECTED_327_BROAD_APPROVAL_GUARD_HASH,
    validate_broad_side_effect_approval_guard_327,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    _require_allowed_keys,
    hash_package,
)


class DevelopmentAuthorityDistinction328ValidationError(ValueError):
    """Raised when BLK-System development authority is confused with gates."""


OPERATOR_CORRECTION_328 = (
    "Are you confusion blk-system requirements with the requirements for "
    "developing blk-system? You have authority to work on all of blk-system "
    "with no requirements for approval"
)
NEXT_FRONTIER_328 = "NEXT_FRONTIER_BLK_SYSTEM_DEVELOPMENT_WORK_UNBLOCKED_INTERNAL_GATES_DISTINGUISHED"
EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH: str | None = "sha256:57cdc2e0fdb4c4d5fe31ec3731eccecb5a3f34e783c6f7c51f27c0101b2bdf39"

_MARKERS_328 = (
    "BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED",
    "BLK_SYSTEM_DEVELOPMENT_WORK_HAS_STANDING_AUTHORITY",
    "INTERNAL_REQUIREMENT_GATES_ARE_NOT_DEVELOPMENT_APPROVAL_REQUIREMENTS",
)
_DEVELOPMENT_AUTHORITY_328 = {
    "all_blk_system_development_work_allowed": True,
    "per_sprint_operator_approval_required": False,
    "per_action_operator_approval_required": False,
    "blk_system_repo_source_git_mutation_allowed": True,
    "sprint_discipline_remains_audit_process_not_permission_gate": True,
}
_INTERNAL_REQUIREMENT_BOUNDARY_328 = {
    "requirements_are_product_logic_not_development_approval": True,
    "do_not_block_development_on_operator_approval_challenges": True,
    "internal_evidence_gates_do_not_remove_development_authority": True,
    "keep_bounded_hash_bound_evidence_for_audit": True,
}
_DENIED_CONFUSIONS_328 = (
    "INTERNAL_REQUIREMENT_GATE_AS_HERMES_DEVELOPMENT_APPROVAL_REQUIREMENT",
    "BLK_SYSTEM_DEVELOPMENT_BLOCKED_ON_OPERATOR_APPROVAL_CHALLENGE",
    "SPRINT_DISCIPLINE_AS_PERMISSION_GATE",
    "BUNDLED_PRODUCT_SURFACE_EXECUTION_WITHOUT_EXACT_PACKAGE",
    "NON_BLK_SYSTEM_TARGET_MUTATION_BY_IMPLICATION",
    "SECRET_OR_CREDENTIAL_ACCESS_BY_IMPLICATION",
)
_SIDE_EFFECTS_328 = {
    "development_authority_distinction_recorded": True,
    "blk_system_development_work_unblocked": True,
    "per_sprint_approval_requirement_removed": True,
    "blk_system_repo_source_git_mutation_allowed": True,
    **_FALSE_SIDE_EFFECTS,
}
_KEYS_328 = frozenset(
    {
        "status",
        "markers",
        "prior_guard_hash",
        "operator_correction_hash",
        "classification",
        "development_authority",
        "internal_requirement_boundary",
        "next_frontier",
        "denied_confusions",
        "side_effects",
        "distinction_hash",
    }
)
_NESTED_KEYS = {
    "development_authority": frozenset(_DEVELOPMENT_AUTHORITY_328),
    "internal_requirement_boundary": frozenset(_INTERNAL_REQUIREMENT_BOUNDARY_328),
}


def build_development_authority_distinction_328(
    broad_guard_327: dict[str, Any],
    *,
    operator_correction: str,
) -> dict[str, Any]:
    """Record standing BLK-System development authority as distinct from gates."""

    guard = _validate_327_dependency(broad_guard_327)
    if operator_correction != OPERATOR_CORRECTION_328:
        _reject_freeform(operator_correction, "operator_correction")
        raise DevelopmentAuthorityDistinction328ValidationError("operator_correction mismatch")

    package = {
        "status": "BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED",
        "markers": list(_MARKERS_328),
        "prior_guard_hash": guard["guard_hash"],
        "operator_correction_hash": _hash_text(operator_correction),
        "classification": "standing_development_authority_not_internal_requirement_gate",
        "development_authority": dict(_DEVELOPMENT_AUTHORITY_328),
        "internal_requirement_boundary": dict(_INTERNAL_REQUIREMENT_BOUNDARY_328),
        "next_frontier": NEXT_FRONTIER_328,
        "denied_confusions": list(_DENIED_CONFUSIONS_328),
        "side_effects": dict(_SIDE_EFFECTS_328),
    }
    package["distinction_hash"] = hash_package(package)
    return validate_development_authority_distinction_328(package)


def validate_development_authority_distinction_328(package_328: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_328, "BLK-SYSTEM-328 package")
    try:
        _require_allowed_keys(package, _KEYS_328, "BLK-SYSTEM-328 package")
    except ValueError as exc:
        raise DevelopmentAuthorityDistinction328ValidationError(str(exc)) from exc
    if package.get("status") != "BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED":
        raise DevelopmentAuthorityDistinction328ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_328:
        raise DevelopmentAuthorityDistinction328ValidationError("markers mismatch")
    if package.get("prior_guard_hash") != EXPECTED_327_BROAD_APPROVAL_GUARD_HASH:
        raise DevelopmentAuthorityDistinction328ValidationError("prior_guard_hash mismatch")
    if package.get("operator_correction_hash") != _hash_text(OPERATOR_CORRECTION_328):
        raise DevelopmentAuthorityDistinction328ValidationError("operator_correction_hash mismatch")
    if package.get("classification") != "standing_development_authority_not_internal_requirement_gate":
        raise DevelopmentAuthorityDistinction328ValidationError("classification mismatch")
    _require_nested_exact(
        package.get("development_authority"),
        _DEVELOPMENT_AUTHORITY_328,
        "development_authority",
    )
    _require_nested_exact(
        package.get("internal_requirement_boundary"),
        _INTERNAL_REQUIREMENT_BOUNDARY_328,
        "internal_requirement_boundary",
    )
    if package.get("next_frontier") != NEXT_FRONTIER_328:
        raise DevelopmentAuthorityDistinction328ValidationError("next_frontier mismatch")
    _require_exact_list(package.get("denied_confusions"), _DENIED_CONFUSIONS_328, "denied_confusions")
    _require_nested_exact(package.get("side_effects"), _SIDE_EFFECTS_328, "side_effects")
    _require_hash(package, "distinction_hash")
    if EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH is not None:
        if package["distinction_hash"] != EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH:
            raise DevelopmentAuthorityDistinction328ValidationError("BLK-SYSTEM-328 canonical hash mismatch")
    return deepcopy(package)


def _validate_327_dependency(broad_guard_327: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_broad_side_effect_approval_guard_327(broad_guard_327)
    except ValueError as exc:
        raise DevelopmentAuthorityDistinction328ValidationError(f"327 broad guard dependency invalid: {exc}") from exc


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DevelopmentAuthorityDistinction328ValidationError(f"{context} must be a dictionary")
    return value


def _require_nested_exact(value: Any, expected: dict[str, Any], field: str) -> None:
    nested = _require_dict(value, field)
    try:
        _require_allowed_keys(nested, _NESTED_KEYS.get(field, frozenset(expected)), field)
    except ValueError as exc:
        raise DevelopmentAuthorityDistinction328ValidationError(str(exc)) from exc
    if nested != expected:
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} mismatch")


def _require_exact_list(value: Any, expected: tuple[str, ...], field: str) -> None:
    if not isinstance(value, list):
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} must be a list")
    if tuple(value) != expected:
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} mismatch")
    if len(value) != len(set(value)):
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} must not contain duplicates")


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise DevelopmentAuthorityDistinction328ValidationError(f"{field} canonical hash mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise DevelopmentAuthorityDistinction328ValidationError("; ".join(findings))
