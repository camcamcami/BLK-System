"""BLK-SYSTEM-237..241 root-doctrine gap ladder packages.

These builders turn the post-236 roadmap sequence into hash-bound, testable
packages without granting adjacent runtime authority.  The ladder deliberately
keeps the 237 Kuronode lane at route-selection/readiness because no exact
feature payload is embedded in this repo change; actual Kuronode mutation still
requires a separately approved BEB-L2 drop through BLK-pipe/Codex.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


_DENIED_SIDE_EFFECT_TRUE = {
    "kuronode_source_git_mutation",
    "live_codex_dispatch",
    "blk_pipe_runtime",
    "root_docs_modified",
    "standalone_blk_id_service_created",
    "standalone_blk_relay_service_created",
    "protected_body_access_without_exact_id",
    "broad_gateway_runtime",
    "loop_runtime_execution",
    "beo_closeout_execution",
    "reusable_codex_dispatch",
    "rtm_generation",
    "production_blk_link",
    "production_blk_test_mcp",
}

_EXPECTED_237_SIDE_EFFECTS = {
    "kuronode_source_git_mutation": False,
    "live_codex_dispatch": False,
    "blk_pipe_runtime": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
}

_EXPECTED_238_SIDE_EFFECTS = {
    "root_docs_modified": False,
    "runtime_authority_changed": False,
    "protected_body_access_without_exact_id": False,
    "rtm_generation": False,
}

_EXPECTED_239_SIDE_EFFECTS = {
    "standalone_blk_id_service_created": False,
    "standalone_blk_relay_service_created": False,
    "network_runtime_created": False,
    "approval_reuse_authorized": False,
    "rtm_generation": False,
}

_EXPECTED_240_SIDE_EFFECTS = {
    "protected_body_access_without_exact_id": False,
    "broad_gateway_runtime": False,
    "active_vault_body_scan": False,
    "source_git_mutation": False,
    "beo_publication": False,
    "rtm_generation": False,
}

_EXPECTED_241_SIDE_EFFECTS = {
    "loop_runtime_execution": False,
    "beo_closeout_execution": False,
    "reusable_codex_dispatch": False,
    "broad_blk_pipe_dispatch": False,
    "protected_body_access_without_exact_id": False,
    "rtm_generation": False,
    "production_blk_test_mcp": False,
}

_ALLOWED_GATEWAY_OPERATIONS = [
    "lint_staging_draft",
    "write_new_staging_draft",
    "promote_new_baseline_with_exact_hitl_approval",
    "retrieve_active_artifact_by_exact_id",
    "write_staged_revision_draft_from_exact_id",
    "promote_staged_revision_with_parent_hash_lock",
]


_ALLOWED_KEYS_237 = {
    "sprint",
    "status",
    "markers",
    "selected_route",
    "required_prior_markers",
    "next_exact_payload_required",
    "side_effects",
    "selection_hash",
}
_ALLOWED_KEYS_238 = {
    "sprint",
    "status",
    "markers",
    "selection_hash",
    "deviations_normalized",
    "root_docs_policy",
    "side_effects",
    "overlay_hash",
}
_ALLOWED_KEYS_239 = {
    "sprint",
    "status",
    "markers",
    "overlay_hash",
    "blk_id_scope",
    "blk_relay_scope",
    "usable_identity_now",
    "service_charter_required_before",
    "side_effects",
    "scope_hash",
}
_ALLOWED_KEYS_240 = {
    "sprint",
    "status",
    "markers",
    "scope_hash",
    "gateway_contract_hash",
    "allowed_gateway_operations",
    "approval_capture_required_per_operation",
    "protected_body_boundary",
    "side_effects",
    "gateway_slice_hash",
}
_ALLOWED_KEYS_241 = {
    "sprint",
    "status",
    "markers",
    "gateway_slice_hash",
    "iteration_contract",
    "stop_conditions",
    "side_effects",
    "loop_kernel_hash",
}
_ALLOWED_GATEWAY_CONTRACT_KEYS = {
    "sprint",
    "status",
    "readiness_review_hash",
    "markers",
    "allowed_operations",
    "operator_input_contract",
    "side_effects",
    "authorized_exact_surface",
    "contract_package_hash",
}


class LadderValidationError(ValueError):
    """Raised when a ladder package is not canonical or safe to consume."""


def build_kuronode_route_selection_237() -> dict[str, Any]:
    """Select the next exact Kuronode route without dispatching a payload."""

    package = {
        "sprint": "BLK-SYSTEM-237",
        "status": "KURONODE_FEATURE_DROP_ROUTE_SELECTED_NO_DISPATCH",
        "markers": [
            "BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY",
            "NEXT_EXACT_KURONODE_FEATURE_REQUIRES_SEPARATE_BEB_L2_APPROVAL",
            "NO_HERMES_DIRECT_KURONODE_MUTATION",
        ],
        "selected_route": "BEB-L2 -> BLK-pipe -> Codex workspace-write",
        "required_prior_markers": [
            "BLK_SYSTEM_222_BEB_L2_BLK_PIPE_CODEX_ROUTE_READY",
            "BLK_SYSTEM_223_BEB_L2_PREFLIGHT_GUARD_READY",
            "BLK_SYSTEM_225_CLEAN_WORKTREE_MANIFEST_READY",
            "BLK_SYSTEM_229_PRIVATE_BWRAP_WORKSPACE_WRITE_SETUP_READY",
            "BLK_SYSTEM_232_BEB_L2_PACKET_HELPER_READY",
            "BLK_SYSTEM_233_CODEX_PROGRESS_EVENTS_READY",
        ],
        "next_exact_payload_required": True,
        "side_effects": dict(_EXPECTED_237_SIDE_EFFECTS),
    }
    package["selection_hash"] = _hash_package(package)
    _validate_237_selection(package)
    return _deepcopy(package)


def build_root_doctrine_deviation_overlay_238(selection_package: dict[str, Any]) -> dict[str, Any]:
    """Normalize root-doctrine deviations without editing BLK-001..006."""

    _validate_237_selection(selection_package)
    package = {
        "sprint": "BLK-SYSTEM-238",
        "status": "ROOT_DOCTRINE_DEVIATION_OVERLAY_READY",
        "markers": [
            "BLK_SYSTEM_238_ROOT_DOCTRINE_DEVIATION_OVERLAY_READY",
            "BLK_001_TO_006_REMAIN_FIXED_OVERVIEW",
            "DEVIATIONS_NORMALIZED_IN_ACTIVE_ROADMAP_AND_TESTS_ONLY",
        ],
        "selection_hash": selection_package["selection_hash"],
        "deviations_normalized": [
            "split_active_vault_paths",
            "current_codex_workspace_write_argv",
            "repository_owned_validation_profiles",
            "lean_beb_l2_helper_not_full_blk003_loop",
        ],
        "root_docs_policy": "do_not_patch_BLK_001_to_006_with_sprint_state",
        "side_effects": dict(_EXPECTED_238_SIDE_EFFECTS),
    }
    package["overlay_hash"] = _hash_package(package)
    _validate_238_overlay(package, selection_package["selection_hash"])
    return _deepcopy(package)


def decide_blk_id_relay_scope_239(overlay_package: dict[str, Any]) -> dict[str, Any]:
    """Decide that blk-id/blk-relay names are boxed until a service charter."""

    _validate_238_overlay(overlay_package)
    package = {
        "sprint": "BLK-SYSTEM-239",
        "status": "BLK_ID_RELAY_SCOPE_DECIDED",
        "markers": [
            "BLK_SYSTEM_239_BLK_ID_RELAY_SCOPE_DECIDED",
            "BLK_ID_RELAY_BOXED_TARGET_ARCHITECTURE_NAMES",
            "NO_STANDALONE_ID_OR_RELAY_SERVICE_CREATED",
        ],
        "overlay_hash": overlay_package["overlay_hash"],
        "blk_id_scope": "target_architecture_name_boxed_until_service_charter",
        "blk_relay_scope": "target_architecture_name_boxed_until_service_charter",
        "usable_identity_now": [
            "exact BLK-req IDs",
            "artifact hashes",
            "operator Discord snowflake/message IDs",
            "BEB/L2/drop manifest hashes",
        ],
        "service_charter_required_before": [
            "broad reusable HITL relay",
            "approval replay ledger",
            "BEO publication service reuse",
            "RTM or blk-link drift/coverage automation",
        ],
        "side_effects": dict(_EXPECTED_239_SIDE_EFFECTS),
    }
    package["scope_hash"] = _hash_package(package)
    _validate_239_scope(package, overlay_package["overlay_hash"])
    return _deepcopy(package)


def build_hitl_gateway_completion_slice_240(
    scope_package: dict[str, Any], gateway_contract: dict[str, Any]
) -> dict[str, Any]:
    """Bind a narrow HITL gateway completion slice to the exact gateway contract."""

    _validate_239_scope(scope_package)
    _validate_gateway_contract(gateway_contract)
    package = {
        "sprint": "BLK-SYSTEM-240",
        "status": "HITL_GATEWAY_COMPLETION_SLICE_READY",
        "markers": [
            "BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY",
            "EXACT_ID_GATEWAY_OPERATIONS_ONLY",
            "APPROVAL_CAPTURE_PER_OPERATION_REQUIRED",
        ],
        "scope_hash": scope_package["scope_hash"],
        "gateway_contract_hash": gateway_contract["contract_package_hash"],
        "allowed_gateway_operations": list(_ALLOWED_GATEWAY_OPERATIONS),
        "approval_capture_required_per_operation": True,
        "protected_body_boundary": "body text may be returned only by exact-ID gateway retrieval, never by broad scans or loop planning",
        "side_effects": dict(_EXPECTED_240_SIDE_EFFECTS),
    }
    package["gateway_slice_hash"] = _hash_package(package)
    _validate_240_gateway(package, scope_package["scope_hash"])
    return _deepcopy(package)


def build_reusable_blk003_loop_kernel_241(gateway_package: dict[str, Any]) -> dict[str, Any]:
    """Create the first reusable BLK-003 loop kernel contract without runtime."""

    _validate_240_gateway(gateway_package)
    package = {
        "sprint": "BLK-SYSTEM-241",
        "status": "REUSABLE_BLK003_LOOP_KERNEL_READY",
        "markers": [
            "BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY",
            "ITERATION_STATE_APPROVAL_FAILURE_CEILING_AND_BEO_DRAFT_RULES_READY",
            "NO_LOOP_RUNTIME_EXECUTION_OR_REUSABLE_CODEX_AUTHORITY",
        ],
        "gateway_slice_hash": gateway_package["gateway_slice_hash"],
        "iteration_contract": {
            "route": "BEB-L2 -> BLK-pipe -> Codex workspace-write",
            "states": ["draft", "approved_exact_payload", "running", "needs_fix", "ready_for_beo_draft", "stopped"],
            "failure_ceiling": 3,
            "approval_required_per_iteration": True,
            "beo_draft_allowed": True,
            "beo_closeout_execution_allowed": False,
        },
        "stop_conditions": [
            "missing exact BEB-L2/drop approval",
            "target hash mismatch",
            "dirty or residue-bearing worktree",
            "private-bwrap descriptor failure",
            "three failed fix iterations",
            "protected-body request outside exact gateway operation",
        ],
        "side_effects": dict(_EXPECTED_241_SIDE_EFFECTS),
    }
    package["loop_kernel_hash"] = _hash_package(package)
    _validate_241_loop(package, gateway_package["gateway_slice_hash"])
    return _deepcopy(package)


def _validate_237_selection(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_237, "selection package")
    _require_hash(package, "selection_hash", "selection package")
    _require_status(package, "KURONODE_FEATURE_DROP_ROUTE_SELECTED_NO_DISPATCH", "selection package")
    _require_marker(package, "BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY", "selection package")
    _require_side_effects(package, _EXPECTED_237_SIDE_EFFECTS, "selection package")
    if package.get("next_exact_payload_required") is not True:
        raise LadderValidationError("selection package must require a future exact payload")
    _reject_laundering(package, "selection package")


def _validate_238_overlay(package: dict[str, Any], expected_selection_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_238, "overlay package")
    _require_hash(package, "overlay_hash", "overlay package")
    _require_status(package, "ROOT_DOCTRINE_DEVIATION_OVERLAY_READY", "overlay package")
    _require_marker(package, "BLK_SYSTEM_238_ROOT_DOCTRINE_DEVIATION_OVERLAY_READY", "overlay package")
    _require_side_effects(package, _EXPECTED_238_SIDE_EFFECTS, "overlay package")
    if expected_selection_hash and package.get("selection_hash") != expected_selection_hash:
        raise LadderValidationError("overlay package selection_hash mismatch")
    if set(package.get("deviations_normalized", [])) != {
        "split_active_vault_paths",
        "current_codex_workspace_write_argv",
        "repository_owned_validation_profiles",
        "lean_beb_l2_helper_not_full_blk003_loop",
    }:
        raise LadderValidationError("overlay package deviations_normalized mismatch")
    _reject_laundering(package, "overlay package")


def _validate_239_scope(package: dict[str, Any], expected_overlay_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_239, "scope package")
    _require_hash(package, "scope_hash", "scope package")
    _require_status(package, "BLK_ID_RELAY_SCOPE_DECIDED", "scope package")
    _require_marker(package, "BLK_SYSTEM_239_BLK_ID_RELAY_SCOPE_DECIDED", "scope package")
    _require_side_effects(package, _EXPECTED_239_SIDE_EFFECTS, "scope package")
    if expected_overlay_hash and package.get("overlay_hash") != expected_overlay_hash:
        raise LadderValidationError("scope package overlay_hash mismatch")
    if package.get("blk_id_scope") != "target_architecture_name_boxed_until_service_charter":
        raise LadderValidationError("scope package blk_id_scope mismatch")
    if package.get("blk_relay_scope") != "target_architecture_name_boxed_until_service_charter":
        raise LadderValidationError("scope package blk_relay_scope mismatch")
    _reject_laundering(package, "scope package")


def _validate_240_gateway(package: dict[str, Any], expected_scope_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_240, "gateway package")
    _require_hash(package, "gateway_slice_hash", "gateway package")
    _require_status(package, "HITL_GATEWAY_COMPLETION_SLICE_READY", "gateway package")
    _require_marker(package, "BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY", "gateway package")
    _require_side_effects(package, _EXPECTED_240_SIDE_EFFECTS, "gateway package")
    if expected_scope_hash and package.get("scope_hash") != expected_scope_hash:
        raise LadderValidationError("gateway package scope_hash mismatch")
    if package.get("allowed_gateway_operations") != _ALLOWED_GATEWAY_OPERATIONS:
        raise LadderValidationError("gateway package allowed_gateway_operations mismatch")
    if package.get("approval_capture_required_per_operation") is not True:
        raise LadderValidationError("gateway package must require per-operation approval capture")
    _reject_laundering(package, "gateway package")


def _validate_241_loop(package: dict[str, Any], expected_gateway_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_241, "loop package")
    _require_hash(package, "loop_kernel_hash", "loop package")
    _require_status(package, "REUSABLE_BLK003_LOOP_KERNEL_READY", "loop package")
    _require_marker(package, "BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY", "loop package")
    _require_side_effects(package, _EXPECTED_241_SIDE_EFFECTS, "loop package")
    if expected_gateway_hash and package.get("gateway_slice_hash") != expected_gateway_hash:
        raise LadderValidationError("loop package gateway_slice_hash mismatch")
    contract = package.get("iteration_contract")
    if not isinstance(contract, dict):
        raise LadderValidationError("loop package iteration_contract must be a dictionary")
    if contract.get("failure_ceiling") != 3:
        raise LadderValidationError("loop package failure_ceiling must be 3")
    if contract.get("approval_required_per_iteration") is not True:
        raise LadderValidationError("loop package must require per-iteration approval")
    if contract.get("beo_closeout_execution_allowed") is not False:
        raise LadderValidationError("loop package must not allow BEO closeout execution")
    _reject_laundering(package, "loop package")


def _validate_gateway_contract(gateway_contract: dict[str, Any]) -> None:
    _require_allowed_keys(gateway_contract, _ALLOWED_GATEWAY_CONTRACT_KEYS, "gateway contract")
    if not isinstance(gateway_contract, dict):
        raise LadderValidationError("gateway contract must be a dictionary")
    if gateway_contract.get("status") != "BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY":
        raise LadderValidationError("gateway contract status mismatch")
    if not _is_hash(gateway_contract.get("contract_package_hash")):
        raise LadderValidationError("gateway contract hash missing")
    if gateway_contract.get("allowed_operations") != _ALLOWED_GATEWAY_OPERATIONS:
        raise LadderValidationError("gateway contract allowed_operations mismatch")
    side_effects = gateway_contract.get("side_effects")
    for key in ("beb_dispatch", "beo_publication", "rtm_generation", "target_source_git_mutation"):
        if not isinstance(side_effects, dict) or side_effects.get(key) is not False:
            raise LadderValidationError(f"gateway contract side_effects.{key} must remain false")
    _reject_laundering(gateway_contract, "gateway contract")


def _require_allowed_keys(package: dict[str, Any], allowed_keys: set[str], context: str) -> None:
    if not isinstance(package, dict):
        raise LadderValidationError(f"{context} must be a dictionary")
    extras = sorted(set(package) - allowed_keys)
    if extras:
        raise LadderValidationError(f"{context} unsupported field(s): {', '.join(extras)}")


def _require_hash(package: dict[str, Any], hash_key: str, context: str) -> None:
    if not isinstance(package, dict):
        raise LadderValidationError(f"{context} must be a dictionary")
    submitted = package.get(hash_key)
    if not _is_hash(submitted):
        raise LadderValidationError(f"{context} missing canonical {hash_key}")
    body = {key: value for key, value in package.items() if key != hash_key}
    expected = _hash_package(body)
    if submitted != expected:
        raise LadderValidationError(f"{context} {hash_key} mismatch")


def _require_status(package: dict[str, Any], expected_status: str, context: str) -> None:
    if package.get("status") != expected_status:
        raise LadderValidationError(f"{context} status mismatch")


def _require_marker(package: dict[str, Any], marker: str, context: str) -> None:
    markers = package.get("markers")
    if not isinstance(markers, list) or marker not in markers:
        raise LadderValidationError(f"{context} marker {marker} missing")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], context: str) -> None:
    side_effects = package.get("side_effects")
    if side_effects != expected:
        bad_true = []
        if isinstance(side_effects, dict):
            bad_true = sorted(key for key in _DENIED_SIDE_EFFECT_TRUE if side_effects.get(key) is True)
        detail = f"; true denied side effects: {', '.join(bad_true)}" if bad_true else ""
        raise LadderValidationError(f"{context} side_effects mismatch{detail}")


def _reject_laundering(package: dict[str, Any], context: str) -> None:
    errors = scan_for_authority_laundering(package)
    if errors:
        raise LadderValidationError(f"{context} contains forbidden authority wording: {'; '.join(errors)}")


def _is_hash(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if not value.startswith("sha256:") or len(value) != 71:
        return False
    return all(ch in "0123456789abcdef" for ch in value[7:])


def _hash_package(package: dict[str, Any]) -> str:
    encoded = json.dumps(package, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
