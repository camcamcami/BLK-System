"""BLK-SYSTEM-261..263 sprint-package granularity guard.

The active BLK-SYSTEM-260 frontier requires exact operator approval text before
any BEO publication run can proceed. This guard records a non-authorizing package
selection layer so generic "plan and execute" directives do not accidentally
advance approval/publication lanes, and so request/contract/preflight/reconcile
rungs are collapsed when they are not independently auditable.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import compact_authority_text, scan_for_authority_laundering
from blk_current_state_authority_index import DENIED_FLAGS as CURRENT_STATE_DENIED_FLAGS


class SprintPackageGranularityValidationError(ValueError):
    """Raised when a sprint-package proposal is unsafe or malformed."""


_EXACT_APPROVAL_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED"
_NEXT_FRONTIER = _EXACT_APPROVAL_FRONTIER
_EXPECTED_OPERATOR_DIRECTIVE_HASH = "sha256:34293c6b8241cc19337b9e24ed77f0e75489f0facbc017739c7ab7ff63777285"
_CANONICAL_REVIEW_261_HASH = "sha256:7c70581968eae55b6629498df2515dcb18eb7913431bd4aba9b9e5c5f42b14a6"
_CANONICAL_CONTRACT_262_HASH = "sha256:26b22fb7679f282bce29308d514d59d234110b9475a4a3223df929aedef44b99"

_SIDE_EFFECTS = {
    "operator_approval_captured": False,
    "approval_reused": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "authoritative_beo_publication_finalized": False,
    "beo_published": False,
    "beo_closeout_execution": False,
    "cryptographic_signature_generated": False,
    "immutable_storage_written": False,
    "public_ledger_appended": False,
    "rtm_generation": False,
    "production_blk_link_execution": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "protected_body_read_copy_parse_hash_scan_mutation": False,
    "beb_dispatch": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
    **{flag: False for flag in CURRENT_STATE_DENIED_FLAGS},
}

_DENIED_AUTHORITIES = [
    "GENERIC_OPERATOR_DIRECTIVE_AS_PUBLICATION_APPROVAL",
    "PAPERWORK_ONLY_MICRO_SPRINTS_AS_VELOCITY",
    "OPAQUE_AUTHORITY_BUNDLING",
    "OPERATOR_APPROVAL_CAPTURE",
    "RUN_ID_RESERVATION_OR_CONSUMPTION",
    "AUTHORITATIVE_BEO_PUBLICATION_FINALITY",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_STORAGE_LEDGER_RUN_OR_REUSE",
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_EXECUTION_OR_REUSABLE_BLK_LINK_AUTHORITY",
    "DRIFT_REJECTION_OR_DRIFT_TRUTH",
    "COVERAGE_TRUTH_OR_COVERAGE_MATRIX_GENERATION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BEB_DISPATCH",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
]

_SELECTION_RULES = {
    "roadmap_is_sprint_structure_agnostic": True,
    "collapse_internal_rungs": True,
    "require_independent_audit_boundary_for_multiple_sprints": True,
    "block_exact_approval_lane_without_exact_text": True,
    "generic_operator_directive_is_not_publication_approval": True,
    "prefer_product_or_production_movement_over_authority_treadmill": True,
    "one_closeout_per_numbered_sprint": True,
}

_ALLOWED_REVIEW_KEYS = {
    "sprint", "status", "markers", "current_frontier", "operator_directive_hash",
    "generic_directive_is_exact_approval", "recommended_lane", "denied_authorities", "side_effects",
    "review_hash",
}
_ALLOWED_CONTRACT_KEYS = {
    "sprint", "status", "markers", "review_hash", "selection_rules", "denied_authorities",
    "side_effects", "contract_hash",
}
_ALLOWED_CANDIDATE_KEYS = {
    "candidate_id", "candidate_type", "requested_sprints", "operator_directive", "frontier",
    "requires_exact_operator_approval_text", "exact_operator_approval_text_present",
    "independent_audit_boundaries", "planned_outputs", "side_effects",
}
_ALLOWED_RESULT_KEYS = {
    "sprint", "status", "markers", "contract_hash", "candidate_id", "candidate_hash", "recommended_shape",
    "decision_reasons", "next_frontier", "denied_authorities", "side_effects", "selection_hash",
}

_PAPERWORK_OUTPUTS = {"request", "contract", "preflight", "reconciliation"}
_AUTHORITY_CANDIDATE_TYPES = {"authority_execution_package", "authority_ladder"}
_PROCESS_CANDIDATE_TYPES = {"process_ladder", "process_hardening", "product_execution_package"}
_ELEVATED_COMPACT_TOKENS = (
    "beo",
    "publication",
    "approval",
    "runid",
    "signer",
    "storage",
    "ledger",
    "rtm",
    "blklink",
    "drifttruth",
    "driftrejection",
    "coveragetruth",
    "coveragematrix",
    "protectedbody",
    "bebdispatch",
    "dispatchbeb",
    "blkpipe",
    "blktest",
    "codex",
    "runtime",
    "tooling",
    "sourcemutation",
    "mutatesource",
    "gitmutation",
    "mutategit",
    "sourcegit",
    "targetsourcegit",
    "packagemanager",
    "network",
    "modelservice",
    "browser",
    "cyber",
    "productionisolation",
)


def denied_side_effects() -> dict[str, bool]:
    """Return the exact false side-effect contract for non-authorizing package selection."""
    return dict(_SIDE_EFFECTS)


def build_sprint_package_frontier_review_261(current_frontier: str, operator_directive: str) -> dict[str, Any]:
    if current_frontier != _EXACT_APPROVAL_FRONTIER:
        raise SprintPackageGranularityValidationError("current_frontier must match BLK-SYSTEM-260 active frontier")
    if not isinstance(operator_directive, str) or not operator_directive.strip():
        raise SprintPackageGranularityValidationError("operator_directive must be a non-empty string")
    directive_hash = _hash_text(operator_directive)
    if directive_hash != _EXPECTED_OPERATOR_DIRECTIVE_HASH:
        raise SprintPackageGranularityValidationError("operator_directive hash mismatch for BLK-SYSTEM-261 package")
    package = {
        "sprint": "BLK-SYSTEM-261",
        "status": "SPRINT_PACKAGE_FRONTIER_REVIEW_READY",
        "markers": [
            "BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY",
            "ROADMAP_SPRINT_STRUCTURE_AGNOSTIC_CONFIRMED",
            "GENERIC_DIRECTIVE_NOT_EXACT_APPROVAL",
        ],
        "current_frontier": current_frontier,
        "operator_directive_hash": directive_hash,
        "generic_directive_is_exact_approval": False,
        "recommended_lane": "package_granularity_guard_before_any_approval_lane_execution",
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": denied_side_effects(),
    }
    package["review_hash"] = _hash_package(package)
    _validate_review_261(package)
    return _deepcopy(package)


def build_sprint_package_granularity_contract_262(review_package: dict[str, Any]) -> dict[str, Any]:
    _validate_review_261(review_package)
    package = {
        "sprint": "BLK-SYSTEM-262",
        "status": "SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY",
        "markers": [
            "BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY",
            "COLLAPSE_NON_AUDITABLE_INTERNAL_RUNGS",
            "BLOCK_APPROVAL_LANE_WITHOUT_EXACT_TEXT",
        ],
        "review_hash": review_package["review_hash"],
        "selection_rules": dict(_SELECTION_RULES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": denied_side_effects(),
    }
    package["contract_hash"] = _hash_package(package)
    _validate_contract_262(package, review_package["review_hash"])
    return _deepcopy(package)


def evaluate_sprint_package_candidate_263(contract_package: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    _validate_contract_262(contract_package)
    _validate_candidate(candidate)

    decision_reasons: list[str] = []
    status: str
    recommended_shape: str

    if _is_publication_or_authority_candidate(candidate):
        if (
            candidate["frontier"] == _EXACT_APPROVAL_FRONTIER
            and candidate["requires_exact_operator_approval_text"]
            and not candidate["exact_operator_approval_text_present"]
        ):
            status = "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL_TEXT"
            recommended_shape = "do_not_execute_approval_lane"
            decision_reasons.append("exact_operator_approval_text_required_not_present")
            decision_reasons.append("generic_operator_directive_is_not_publication_approval")
        else:
            status = "BLOCKED_ELEVATED_PACKAGE_REQUIRES_SEPARATE_APPROVED_EXECUTION"
            recommended_shape = "separate_exact_execution_package_required"
            decision_reasons.append("elevated_candidate_is_review_only_in_granularity_guard")
            decision_reasons.append("approval_or_execution_booleans_are_not_trusted")
    elif _is_paperwork_only_candidate(candidate):
        status = "READY_AS_SINGLE_SPRINT_WITH_INTERNAL_TASKS"
        recommended_shape = "one_sprint_internal_tasks"
        decision_reasons.append("paperwork_only_micro_sprints_collapsed")
        decision_reasons.append("no_independent_audit_boundaries_present")
    elif _has_independent_boundaries(candidate):
        status = "REVIEWED_AS_MULTI_SPRINT_CANDIDATE_NOT_AUTHORITY"
        recommended_shape = "multi_sprint_candidate_requires_separate_execution_authority"
        decision_reasons.append("independent_audit_boundaries_present")
        decision_reasons.append("separate_hash_boundaries_are_reviewable")
    else:
        status = "READY_AS_SINGLE_SPRINT_WITH_INTERNAL_TASKS"
        recommended_shape = "one_sprint_internal_tasks"
        decision_reasons.append("default_collapse_to_single_bounded_capability")

    package = {
        "sprint": "BLK-SYSTEM-263",
        "status": status,
        "markers": [
            "BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY",
            "PUBLICATION_DECISION_NOT_RECORDED",
            "NOT_EXECUTION_APPROVAL",
            "ROADMAP_REMAINS_FRONTIER_AGNOSTIC_TO_SPRINT_SHAPE"
        ],
        "contract_hash": contract_package["contract_hash"],
        "candidate_id": candidate["candidate_id"],
        "candidate_hash": _hash_package(candidate),
        "recommended_shape": recommended_shape,
        "decision_reasons": decision_reasons,
        "next_frontier": _NEXT_FRONTIER,
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": denied_side_effects(),
    }
    package["selection_hash"] = _hash_package(package)
    _validate_selection_263(package, contract_package["contract_hash"])
    return _deepcopy(package)


def _is_paperwork_only_candidate(candidate: dict[str, Any]) -> bool:
    outputs = set(candidate["planned_outputs"])
    return len(candidate["requested_sprints"]) > 1 and outputs.issubset(_PAPERWORK_OUTPUTS)


def _has_independent_boundaries(candidate: dict[str, Any]) -> bool:
    return len(candidate["requested_sprints"]) > 1 and len(candidate["independent_audit_boundaries"]) >= 2


def _is_publication_or_authority_candidate(candidate: dict[str, Any]) -> bool:
    if candidate["candidate_type"] in _AUTHORITY_CANDIDATE_TYPES:
        return True
    authority_text = " ".join(
        [
            candidate["candidate_id"],
            candidate["operator_directive"],
            candidate["frontier"],
            *candidate["planned_outputs"],
            *candidate["independent_audit_boundaries"],
        ]
    ).casefold()
    compact = compact_authority_text(authority_text)
    return any(token in compact for token in _ELEVATED_COMPACT_TOKENS)


def _validate_review_261(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_REVIEW_KEYS, "review package")
    _require_status(package, "SPRINT_PACKAGE_FRONTIER_REVIEW_READY", "review package")
    _require_markers(package, [
        "BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY",
        "ROADMAP_SPRINT_STRUCTURE_AGNOSTIC_CONFIRMED",
        "GENERIC_DIRECTIVE_NOT_EXACT_APPROVAL",
    ], "review package")
    if package.get("current_frontier") != _EXACT_APPROVAL_FRONTIER:
        raise SprintPackageGranularityValidationError("review package current_frontier mismatch")
    if package.get("generic_directive_is_exact_approval") is not False:
        raise SprintPackageGranularityValidationError("review package must not treat generic directive as exact approval")
    _require_exact_false_side_effects(package.get("side_effects"), "review package")
    _require_denied_authorities(package.get("denied_authorities"), "review package")
    _require_hash(package, "review_hash", "review package")
    if package.get("review_hash") != _CANONICAL_REVIEW_261_HASH:
        raise SprintPackageGranularityValidationError("review package canonical BLK-SYSTEM-261 hash mismatch")
    _reject_freeform_laundering(package, "review package")


def _validate_contract_262(package: dict[str, Any], expected_review_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_CONTRACT_KEYS, "contract package")
    _require_status(package, "SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY", "contract package")
    _require_markers(package, [
        "BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY",
        "COLLAPSE_NON_AUDITABLE_INTERNAL_RUNGS",
        "BLOCK_APPROVAL_LANE_WITHOUT_EXACT_TEXT",
    ], "contract package")
    if expected_review_hash is not None and package.get("review_hash") != expected_review_hash:
        raise SprintPackageGranularityValidationError("contract package review_hash mismatch")
    if package.get("selection_rules") != _SELECTION_RULES:
        raise SprintPackageGranularityValidationError("contract package selection_rules mismatch")
    _require_exact_false_side_effects(package.get("side_effects"), "contract package")
    _require_denied_authorities(package.get("denied_authorities"), "contract package")
    _require_hash(package, "contract_hash", "contract package")
    if package.get("review_hash") != _CANONICAL_REVIEW_261_HASH:
        raise SprintPackageGranularityValidationError("contract package canonical BLK-SYSTEM-261 hash mismatch")
    if package.get("contract_hash") != _CANONICAL_CONTRACT_262_HASH:
        raise SprintPackageGranularityValidationError("contract package canonical BLK-SYSTEM-262 hash mismatch")
    _reject_freeform_laundering(package, "contract package")


def _validate_candidate(candidate: dict[str, Any]) -> None:
    if not isinstance(candidate, dict):
        raise SprintPackageGranularityValidationError("candidate must be a dict")
    _require_allowed_keys(candidate, _ALLOWED_CANDIDATE_KEYS, "candidate")
    _reject_freeform_laundering(candidate, "candidate")
    if not isinstance(candidate.get("candidate_id"), str) or not candidate["candidate_id"]:
        raise SprintPackageGranularityValidationError("candidate_id must be non-empty")
    if candidate.get("candidate_type") not in _AUTHORITY_CANDIDATE_TYPES | _PROCESS_CANDIDATE_TYPES:
        raise SprintPackageGranularityValidationError("candidate_type unsupported")
    if not _is_ascii_sprint_list(candidate.get("requested_sprints")):
        raise SprintPackageGranularityValidationError("requested_sprints must be a non-empty list of ASCII sprint ints")
    for field in ("requires_exact_operator_approval_text", "exact_operator_approval_text_present"):
        if type(candidate.get(field)) is not bool:
            raise SprintPackageGranularityValidationError(f"{field} must be bool")
    for field in ("independent_audit_boundaries", "planned_outputs"):
        if not isinstance(candidate.get(field), list) or not all(isinstance(item, str) and item for item in candidate[field]):
            raise SprintPackageGranularityValidationError(f"{field} must be a non-empty string list or empty list")
    _require_exact_false_side_effects(candidate.get("side_effects"), "candidate")


def _validate_selection_263(package: dict[str, Any], expected_contract_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_RESULT_KEYS, "selection package")
    if package.get("status") not in {
        "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL_TEXT",
        "BLOCKED_ELEVATED_PACKAGE_REQUIRES_SEPARATE_APPROVED_EXECUTION",
        "READY_AS_SINGLE_SPRINT_WITH_INTERNAL_TASKS",
        "REVIEWED_AS_MULTI_SPRINT_CANDIDATE_NOT_AUTHORITY",
    }:
        raise SprintPackageGranularityValidationError("selection package status invalid")
    _require_markers(package, [
        "BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY",
        "PUBLICATION_DECISION_NOT_RECORDED",
        "NOT_EXECUTION_APPROVAL",
        "ROADMAP_REMAINS_FRONTIER_AGNOSTIC_TO_SPRINT_SHAPE",
    ], "selection package")
    if expected_contract_hash is not None and package.get("contract_hash") != expected_contract_hash:
        raise SprintPackageGranularityValidationError("selection package contract_hash mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise SprintPackageGranularityValidationError("selection package next_frontier mismatch")
    if not isinstance(package.get("candidate_hash"), str) or not package["candidate_hash"].startswith("sha256:"):
        raise SprintPackageGranularityValidationError("selection package candidate_hash invalid")
    _require_exact_false_side_effects(package.get("side_effects"), "selection package")
    _require_denied_authorities(package.get("denied_authorities"), "selection package")
    _require_hash(package, "selection_hash", "selection package")
    _reject_freeform_laundering(package, "selection package")


def _require_allowed_keys(package: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = set(package) - allowed
    missing = allowed - set(package)
    if extra:
        raise SprintPackageGranularityValidationError(f"{label} unsupported field(s): {sorted(extra)}")
    if missing:
        raise SprintPackageGranularityValidationError(f"{label} missing field(s): {sorted(missing)}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise SprintPackageGranularityValidationError(f"{label} status mismatch")


def _require_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise SprintPackageGranularityValidationError(f"{label} markers mismatch")


def _require_denied_authorities(value: Any, label: str) -> None:
    if value != _DENIED_AUTHORITIES:
        raise SprintPackageGranularityValidationError(f"{label} denied_authorities mismatch")


def _require_exact_false_side_effects(value: Any, label: str) -> None:
    if value != _SIDE_EFFECTS:
        raise SprintPackageGranularityValidationError(f"{label} side_effects mismatch")


def _require_hash(package: dict[str, Any], hash_key: str, label: str) -> None:
    submitted = package.get(hash_key)
    if not isinstance(submitted, str) or not submitted.startswith("sha256:"):
        raise SprintPackageGranularityValidationError(f"{label} {hash_key} invalid")
    recomputed = _hash_package({k: v for k, v in package.items() if k != hash_key})
    if submitted != recomputed:
        raise SprintPackageGranularityValidationError(f"{label} {hash_key} mismatch")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    errors = scan_for_authority_laundering(value)
    if errors:
        raise SprintPackageGranularityValidationError(f"{label} contains forbidden authority wording: {errors[0]}")


def _is_ascii_sprint_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(type(item) is int and item > 0 for item in value)


def _hash_package(package: dict[str, Any]) -> str:
    payload = json.dumps(package, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _deepcopy(package: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(package)
