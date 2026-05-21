"""BLK-SYSTEM-322 first-pass done record for BLK-001..006 and BLK-077.

This package records that the root doctrine overview set and active roadmap have
a 9.9/10 theory-complete first pass ready for operator review. It intentionally
stops short of ten-of-ten finality and grants no production side-effect authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_system_velocity_to_9_317_321 import (
    EXPECTED_321_RECONCILIATION_HASH,
    validate_blk_system_development_unblock_reconciliation_321,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _require_allowed_keys,
    hash_package,
)


class FirstPassNineNine322ValidationError(ValueError):
    """Raised when BLK-SYSTEM-322 evidence overclaims readiness or authority."""


OPERATOR_DIRECTIVE_322 = (
    "plan an execute blk-system sprint for a first pass done of "
    "blk-001 to blk-006 and the blk-system roadmap"
)
TARGET_RATING_322 = "9.9/10_not_10/10_pending_operator_review_and_verification"
NEXT_FRONTIER_322 = "NEXT_FRONTIER_9_9_FIRST_PASS_OPERATOR_REVIEW_AND_VERIFICATION_GAPS_NOT_10_OF_10"
EXPECTED_322_FIRST_PASS_HASH = "sha256:d468c253df3d5c8419a7529db4d8aaf43dd9b437562e0f276facae7d8af3d8f7"

_ROOT_DOCS = ("BLK-001", "BLK-002", "BLK-003", "BLK-004", "BLK-005", "BLK-006")
_MARKERS_322 = (
    "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
    "BLK_001_TO_006_FIRST_PASS_DONE_THEORY_ONLY",
    "BLK_077_ROADMAP_FIRST_PASS_DONE_THEORY_ONLY",
    "NOT_10_OF_10_FINAL_VERIFICATION_PENDING",
    "SIDE_EFFECT_APPROVALS_REMAIN_SEPARATE",
)
_DENIED_AUTHORITIES_322 = (
    "TEN_OF_TEN_FINALITY_CLAIM",
    "OPERATOR_REVIEW_AS_IMPLICIT_APPROVAL",
    "VERIFICATION_ACTIVITY_AS_SIDE_EFFECT_APPROVAL",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "BEO_CLOSEOUT_EXECUTION",
    "AUTHORITATIVE_BEO_PUBLICATION_EXECUTION",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "SIGNER_STORAGE_LEDGER_ACTION_OR_REUSE",
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
)
_SIDE_EFFECTS_322 = {
    "root_doctrine_first_pass_done_recorded": True,
    "roadmap_first_pass_done_recorded": True,
    "nine_point_nine_theory_done_recorded": True,
    "ten_of_ten_claimed": False,
    "operator_review_closed": False,
    "verification_activities_closed": False,
    **_FALSE_SIDE_EFFECTS,
}
_REVIEW_GAPS = (
    "operator_review_required_before_final_closeout",
    "verification_activities_required_to_close_remaining_gaps",
    "observed_gap_remediation_required_before_any_10_of_10_claim",
    "separate_exact_side_effect_decisions_required_for_BEO_RTM_blk_link_lanes",
)
_KEYS_322 = frozenset(
    {
        "status",
        "markers",
        "prior_reconciliation_hash",
        "operator_directive_hash",
        "readiness_rating",
        "root_doctrine_docs",
        "roadmap_doc",
        "completion_scope",
        "review_gap_register",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "first_pass_hash",
    }
)


def build_blk001_006_roadmap_first_pass_done_322(
    reconciliation_321: dict[str, Any],
    *,
    operator_directive: str,
    target_rating: str,
) -> dict[str, Any]:
    """Record 9.9/10 first-pass done status without closing final review gaps."""

    prior = _validate_321_dependency(reconciliation_321)
    if operator_directive != OPERATOR_DIRECTIVE_322:
        _reject_freeform(operator_directive, "operator_directive")
        raise FirstPassNineNine322ValidationError("operator_directive mismatch")
    if target_rating != TARGET_RATING_322:
        _reject_freeform(target_rating, "target_rating")
        raise FirstPassNineNine322ValidationError("target_rating must be the 9.9/10 non-final review target")

    package = {
        "status": "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY",
        "markers": list(_MARKERS_322),
        "prior_reconciliation_hash": prior["reconciliation_hash"],
        "operator_directive_hash": hash_package({"operator_directive": operator_directive}),
        "readiness_rating": "9.9/10_theory_done_pending_review",
        "root_doctrine_docs": list(_ROOT_DOCS),
        "roadmap_doc": "BLK-077",
        "completion_scope": (
            "first_pass_done_for_fixed_root_overview_docs_and_active_roadmap; "
            "not_10_of_10; final_review_and_verification_remaining"
        ),
        "review_gap_register": list(_REVIEW_GAPS),
        "next_frontier": NEXT_FRONTIER_322,
        "denied_authorities": list(_DENIED_AUTHORITIES_322),
        "side_effects": dict(_SIDE_EFFECTS_322),
    }
    package["first_pass_hash"] = hash_package(package)
    return validate_blk001_006_roadmap_first_pass_done_322(package)


def validate_blk001_006_roadmap_first_pass_done_322(package_322: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_322, "BLK-SYSTEM-322 package")
    try:
        _require_allowed_keys(package, _KEYS_322, "BLK-SYSTEM-322 package")
    except ValueError as exc:
        raise FirstPassNineNine322ValidationError(str(exc)) from exc
    if package.get("status") != "BLK_SYSTEM_322_ROOT_DOCTRINE_ROADMAP_FIRST_PASS_DONE_FOR_9_9_REVIEW_READY":
        raise FirstPassNineNine322ValidationError("status mismatch")
    if tuple(package.get("markers", ())) != _MARKERS_322:
        raise FirstPassNineNine322ValidationError("markers mismatch")
    if package.get("prior_reconciliation_hash") != EXPECTED_321_RECONCILIATION_HASH:
        raise FirstPassNineNine322ValidationError("321 reconciliation hash mismatch")
    if package.get("readiness_rating") != "9.9/10_theory_done_pending_review":
        raise FirstPassNineNine322ValidationError("readiness_rating mismatch")
    if tuple(package.get("root_doctrine_docs", ())) != _ROOT_DOCS:
        raise FirstPassNineNine322ValidationError("root_doctrine_docs mismatch")
    if package.get("roadmap_doc") != "BLK-077":
        raise FirstPassNineNine322ValidationError("roadmap_doc mismatch")
    if package.get("review_gap_register") != list(_REVIEW_GAPS):
        raise FirstPassNineNine322ValidationError("review_gap_register mismatch")
    if package.get("next_frontier") != NEXT_FRONTIER_322:
        raise FirstPassNineNine322ValidationError("next_frontier mismatch")
    _require_denied_authorities(package.get("denied_authorities"))
    _require_side_effects(package.get("side_effects"))
    _require_hash(package, "first_pass_hash")
    if package["first_pass_hash"] != EXPECTED_322_FIRST_PASS_HASH:
        raise FirstPassNineNine322ValidationError("BLK-SYSTEM-322 canonical hash mismatch")
    _scan_package(package, "BLK-SYSTEM-322 package")
    return deepcopy(package)


def _validate_321_dependency(reconciliation_321: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_blk_system_development_unblock_reconciliation_321(reconciliation_321)
    except ValueError as exc:
        raise FirstPassNineNine322ValidationError(f"321 reconciliation invalid: {exc}") from exc


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FirstPassNineNine322ValidationError(f"{context} must be a dictionary")
    return value


def _require_denied_authorities(value: Any) -> None:
    if not isinstance(value, list):
        raise FirstPassNineNine322ValidationError("denied_authorities must be a list")
    if tuple(value) != _DENIED_AUTHORITIES_322:
        raise FirstPassNineNine322ValidationError("denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise FirstPassNineNine322ValidationError("denied_authorities must not contain duplicates")


def _require_side_effects(value: Any) -> None:
    side_effects = _require_dict(value, "side_effects")
    if side_effects != _SIDE_EFFECTS_322:
        raise FirstPassNineNine322ValidationError("side_effects mismatch")


def _require_hash(package: dict[str, Any], field: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise FirstPassNineNine322ValidationError(f"{field} must be sha256:<64 hex>")
    body = {key: val for key, val in package.items() if key != field}
    if hash_package(body) != value:
        raise FirstPassNineNine322ValidationError(f"{field} canonical hash mismatch")


def _reject_freeform(value: Any, path: str) -> None:
    findings = scan_for_authority_laundering(value, path)
    if findings:
        raise FirstPassNineNine322ValidationError("; ".join(findings))


def _scan_package(package: dict[str, Any], path: str) -> None:
    findings = scan_for_authority_laundering(package, path)
    if findings:
        raise FirstPassNineNine322ValidationError("; ".join(findings))
