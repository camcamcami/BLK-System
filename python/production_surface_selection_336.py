"""BLK-SYSTEM-336 production surface selection package.

This module selects the next exact production-driving surface after one
BEO/RTM trace loop closed.  The selection is intentionally non-executing:
it does not start MCP transport, relay runtime, reusable loop authority,
protected-body access, source/Git mutation, BEO publication, RTM generation,
or production ``blk-link`` behavior.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


class SurfaceSelectionValidationError(ValueError):
    """Raised when the BLK-SYSTEM-336 selection package is unsafe."""


SPRINT = "BLK-SYSTEM-336"
STATUS = "PRODUCTION_BLK_TEST_MCP_SURFACE_SELECTED_NO_TRANSPORT"
PREVIOUS_FRONTIER = (
    "NEXT_FRONTIER_ONE_EXACT_BEO_TO_RTM_BLK_LINK_TRACE_CLOSED_"
    "REUSABLE_AUTHORITY_NOT_GRANTED"
)
PRIOR_RECONCILIATION_HASH = (
    "sha256:0cf714e86b0dcff83460dcaaa34597eaf8ad887934de21019fc2107ebef6dfa4"
)
SELECTED_SURFACE = "production_blk_test_mcp_transport_contract"
NEXT_FRONTIER = (
    "NEXT_FRONTIER_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_REQUIRED_NOT_GRANTED"
)

_MARKERS = (
    "BLK_SYSTEM_336_PRODUCTION_BLK_TEST_MCP_SURFACE_SELECTED",
    "PRODUCTION_BLK_TEST_MCP_NEXT_VALIDATION_BOTTLENECK",
    "PRODUCTION_BLK_TEST_MCP_TRANSPORT_STILL_NOT_GRANTED",
    NEXT_FRONTIER,
)

_SELECTION_BASIS = {
    "primary_reason": (
        "BLK-test is the next validation bottleneck after one exact BEO/RTM trace loop closed"
    ),
    "depends_on": (
        "BLK-SYSTEM-333 reconciled one hash-only RTM/blk-link trace loop; "
        "BLK-SYSTEM-301 and BLK-SYSTEM-246 left BLK-test verifier-only with transport disabled"
    ),
    "decision_rule": (
        "Prefer validation/oracle transport contract before relay runtime or reusable loop expansion"
    ),
}

_DEFERRED_SURFACES = (
    {
        "surface": "standalone_relay_runtime",
        "reason": (
            "Relay runtime can amplify messages before the validation oracle is MCP-callable"
        ),
    },
    {
        "surface": "reusable_blk003_loop_authority",
        "reason": (
            "Reusable loops should wait until BLK-test transport has a bounded contract"
        ),
    },
)

_EXPECTED_SIDE_EFFECTS = {
    "production_mcp_started": False,
    "generic_mcp_started": False,
    "reusable_blk_test_service_started": False,
    "runtime_tooling_executed": False,
    "relay_network_runtime_started": False,
    "message_dispatch_started": False,
    "reusable_blk003_loop_authority": False,
    "planner_dispatcher_authority": False,
    "oracle_source_of_truth_claimed": False,
    "source_git_mutation": False,
    "target_source_git_mutation": False,
    "protected_body_accessed": False,
    "beo_publication": False,
    "beo_closeout_execution": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "package_manager_used": False,
    "network_model_browser_cyber_tooling_used": False,
    "production_isolation_claimed": False,
}

_ALLOWED_PACKAGE_KEYS = {
    "sprint",
    "status",
    "previous_frontier",
    "prior_reconciliation_hash",
    "selected_surface",
    "next_frontier",
    "markers",
    "selection_basis",
    "deferred_surfaces",
    "side_effects",
    "selection_hash",
}
_ALLOWED_BASIS_KEYS = {"primary_reason", "depends_on", "decision_rule"}
_ALLOWED_DEFERRED_KEYS = {"surface", "reason"}


def build_production_surface_selection_336() -> dict[str, Any]:
    """Return the hash-bound surface decision package for BLK-SYSTEM-336."""

    package: dict[str, Any] = {
        "sprint": SPRINT,
        "status": STATUS,
        "previous_frontier": PREVIOUS_FRONTIER,
        "prior_reconciliation_hash": PRIOR_RECONCILIATION_HASH,
        "selected_surface": SELECTED_SURFACE,
        "next_frontier": NEXT_FRONTIER,
        "markers": list(_MARKERS),
        "selection_basis": dict(_SELECTION_BASIS),
        "deferred_surfaces": [dict(item) for item in _DEFERRED_SURFACES],
        "side_effects": dict(_EXPECTED_SIDE_EFFECTS),
    }
    package["selection_hash"] = _hash_package(package)
    validate_production_surface_selection_336(package)
    return _deepcopy(package)


def validate_production_surface_selection_336(package: dict[str, Any]) -> None:
    """Validate that a BLK-SYSTEM-336 package cannot smuggle execution authority."""

    if not isinstance(package, dict):
        raise SurfaceSelectionValidationError("surface selection package must be a dict")
    _require_allowed_keys(package, _ALLOWED_PACKAGE_KEYS, "surface selection package")
    if package.get("sprint") != SPRINT:
        raise SurfaceSelectionValidationError("sprint must be BLK-SYSTEM-336")
    if package.get("status") != STATUS:
        raise SurfaceSelectionValidationError("status mismatch")
    if package.get("previous_frontier") != PREVIOUS_FRONTIER:
        raise SurfaceSelectionValidationError("previous_frontier mismatch")
    _require_hash(package.get("prior_reconciliation_hash"), "prior_reconciliation_hash")
    if package.get("prior_reconciliation_hash") != PRIOR_RECONCILIATION_HASH:
        raise SurfaceSelectionValidationError("prior_reconciliation_hash mismatch")
    if package.get("selected_surface") != SELECTED_SURFACE:
        raise SurfaceSelectionValidationError("selected_surface mismatch")
    if package.get("next_frontier") != NEXT_FRONTIER:
        raise SurfaceSelectionValidationError("next_frontier mismatch")
    if package.get("markers") != list(_MARKERS):
        raise SurfaceSelectionValidationError("markers mismatch")
    _validate_selection_basis(package.get("selection_basis"))
    _validate_deferred_surfaces(package.get("deferred_surfaces"))
    _validate_side_effects(package.get("side_effects"))
    expected_hash = _hash_package(
        {key: value for key, value in package.items() if key != "selection_hash"}
    )
    if package.get("selection_hash") != expected_hash:
        raise SurfaceSelectionValidationError("selection_hash mismatch")
    laundering = scan_for_authority_laundering(package, "surface_selection_336")
    if laundering:
        raise SurfaceSelectionValidationError("; ".join(laundering))


def _validate_selection_basis(value: Any) -> None:
    if not isinstance(value, dict):
        raise SurfaceSelectionValidationError("selection_basis must be a dict")
    _require_allowed_keys(value, _ALLOWED_BASIS_KEYS, "selection_basis")
    laundering = scan_for_authority_laundering(value, "selection_basis")
    if laundering:
        raise SurfaceSelectionValidationError("; ".join(laundering))
    if value != _SELECTION_BASIS:
        raise SurfaceSelectionValidationError("selection_basis mismatch")


def _validate_deferred_surfaces(value: Any) -> None:
    if not isinstance(value, list):
        raise SurfaceSelectionValidationError("deferred_surfaces must be a list")
    expected = [dict(item) for item in _DEFERRED_SURFACES]
    if value != expected:
        raise SurfaceSelectionValidationError("deferred_surfaces mismatch")
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise SurfaceSelectionValidationError("deferred_surfaces entries must be dicts")
        _require_allowed_keys(item, _ALLOWED_DEFERRED_KEYS, f"deferred_surfaces[{index}]")


def _validate_side_effects(value: Any) -> None:
    if not isinstance(value, dict):
        raise SurfaceSelectionValidationError("side_effects must be a dict")
    if set(value) != set(_EXPECTED_SIDE_EFFECTS):
        raise SurfaceSelectionValidationError("side_effects keys mismatch")
    for key in _EXPECTED_SIDE_EFFECTS:
        if value.get(key) is not False:
            raise SurfaceSelectionValidationError(f"side_effects {key} must be False")


def _require_allowed_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if extra:
        raise SurfaceSelectionValidationError(
            f"{label} unsupported field(s): {', '.join(extra)}"
        )
    if missing:
        raise SurfaceSelectionValidationError(
            f"{label} missing field(s): {', '.join(missing)}"
        )


def _require_hash(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise SurfaceSelectionValidationError(f"{label} must be canonical sha256")
    if not value.startswith("sha256:") or len(value) != 71:
        raise SurfaceSelectionValidationError(f"{label} must be canonical sha256")
    if not all(ch in "0123456789abcdef" for ch in value.removeprefix("sha256:")):
        raise SurfaceSelectionValidationError(f"{label} must be canonical sha256")


def _hash_package(package: Any) -> str:
    encoded = json.dumps(package, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
