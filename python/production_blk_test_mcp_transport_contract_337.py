"""BLK-SYSTEM-337 production BLK-test MCP transport contract.

The Occam package turns the BLK-SYSTEM-336 surface selection into one
minimal verifier-only stdio contract. It deliberately does not start a
server, run a client, execute tools, claim oracle truth, read protected
bodies, mutate source or Git, publish BEOs, generate RTM, run blk-link, or
expand the fixed tool set.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


class TransportContractValidationError(ValueError):
    """Raised when the BLK-SYSTEM-337 transport contract is unsafe."""


SPRINT = "BLK-SYSTEM-337"
STATUS = "PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_READY_NO_SERVER_START"
PREVIOUS_FRONTIER = (
    "NEXT_FRONTIER_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_"
    "REQUIRED_NOT_GRANTED"
)
PRIOR_SELECTION_HASH = (
    "sha256:64e618ba82233f4940d8c1ce1dc94d4a37d28127a8dd570d10b76e77e58faeab"
)
NEXT_FRONTIER = "NEXT_FRONTIER_OCCAM_END_TO_END_VALIDATION_RUN_REQUIRED_NOT_STARTED"

_MARKERS = (
    "BLK_SYSTEM_337_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_READY",
    "OCCAM_FIXED_TOOL_STDIO_CONTRACT_ONLY",
    "END_TO_END_VALIDATION_RUN_NOT_STARTED",
    NEXT_FRONTIER,
)

_TRANSPORT_PROFILE = {
    "protocol": "stdio-jsonl-mcp-subset",
    "role": "verifier_only",
    "methods": ["initialize", "tools/list", "tools/call"],
    "tool_call_shape": "fixed_registry_name_plus_empty_arguments",
    "workspace_policy": "synthetic_or_exact_future_run_workspace_only",
}
_FIXED_TOOL_REGISTRY = ["run_ast_validation"]
_VERDICT_VOCABULARY = ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"]
_REQUIRED_EVIDENCE_INPUTS = [
    {"name": "selection_hash", "hash": PRIOR_SELECTION_HASH},
    {"name": "oracle_reconciliation_hash", "hash": "sha256:" + "1" * 64},
    {"name": "trace_closure_hash", "hash": "sha256:" + "2" * 64},
    {"name": "future_run_workspace_hash", "hash": "sha256:" + "3" * 64},
]
_E2E_READINESS = {
    "contract_ready_for_exact_future_run_request": True,
    "run_started": False,
    "separate_operator_runtime_gate_required": True,
    "feature_expansion_deferred": True,
}
_EXPECTED_SIDE_EFFECTS = {
    "server_started": False,
    "client_started": False,
    "tool_executed": False,
    "generic_transport_started": False,
    "reusable_service_started": False,
    "planner_dispatcher_role": False,
    "oracle_truth_claimed": False,
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
    "prior_selection_hash",
    "next_frontier",
    "markers",
    "transport_profile",
    "fixed_tool_registry",
    "verdict_vocabulary",
    "required_evidence_inputs",
    "e2e_validation_readiness",
    "side_effects",
    "contract_hash",
}
_ALLOWED_TRANSPORT_KEYS = {
    "protocol",
    "role",
    "methods",
    "tool_call_shape",
    "workspace_policy",
}
_ALLOWED_EVIDENCE_KEYS = {"name", "hash"}
_ALLOWED_READINESS_KEYS = set(_E2E_READINESS)


def build_transport_contract_337() -> dict[str, Any]:
    """Return the hash-bound Occam transport contract package."""

    package: dict[str, Any] = {
        "sprint": SPRINT,
        "status": STATUS,
        "previous_frontier": PREVIOUS_FRONTIER,
        "prior_selection_hash": PRIOR_SELECTION_HASH,
        "next_frontier": NEXT_FRONTIER,
        "markers": list(_MARKERS),
        "transport_profile": deepcopy(_TRANSPORT_PROFILE),
        "fixed_tool_registry": list(_FIXED_TOOL_REGISTRY),
        "verdict_vocabulary": list(_VERDICT_VOCABULARY),
        "required_evidence_inputs": deepcopy(_REQUIRED_EVIDENCE_INPUTS),
        "e2e_validation_readiness": dict(_E2E_READINESS),
        "side_effects": dict(_EXPECTED_SIDE_EFFECTS),
    }
    package["contract_hash"] = _hash_package(package)
    validate_transport_contract_337(package)
    return _deepcopy(package)


def validate_transport_contract_337(package: dict[str, Any]) -> None:
    """Validate that the contract cannot smuggle runtime or expansion scope."""

    if not isinstance(package, dict):
        raise TransportContractValidationError("transport contract must be a dict")
    _require_allowed_keys(package, _ALLOWED_PACKAGE_KEYS, "transport contract")
    if package.get("sprint") != SPRINT:
        raise TransportContractValidationError("sprint must be BLK-SYSTEM-337")
    if package.get("status") != STATUS:
        raise TransportContractValidationError("status mismatch")
    if package.get("previous_frontier") != PREVIOUS_FRONTIER:
        raise TransportContractValidationError("previous_frontier mismatch")
    _require_hash(package.get("prior_selection_hash"), "prior_selection_hash")
    if package.get("prior_selection_hash") != PRIOR_SELECTION_HASH:
        raise TransportContractValidationError("prior_selection_hash mismatch")
    if package.get("next_frontier") != NEXT_FRONTIER:
        raise TransportContractValidationError("next_frontier mismatch")
    if package.get("markers") != list(_MARKERS):
        raise TransportContractValidationError("markers mismatch")
    _validate_transport_profile(package.get("transport_profile"))
    _validate_fixed_tool_registry(package.get("fixed_tool_registry"))
    if package.get("verdict_vocabulary") != list(_VERDICT_VOCABULARY):
        raise TransportContractValidationError("verdict_vocabulary mismatch")
    _validate_required_evidence_inputs(package.get("required_evidence_inputs"))
    _validate_e2e_readiness(package.get("e2e_validation_readiness"))
    _validate_side_effects(package.get("side_effects"))
    expected_hash = _hash_package(
        {key: value for key, value in package.items() if key != "contract_hash"}
    )
    if package.get("contract_hash") != expected_hash:
        raise TransportContractValidationError("contract_hash mismatch")
    laundering = scan_for_authority_laundering(package, "transport_contract_337")
    if laundering:
        raise TransportContractValidationError(
            "forbidden authority wording: " + "; ".join(laundering)
        )


def _validate_transport_profile(value: Any) -> None:
    if not isinstance(value, dict):
        raise TransportContractValidationError("transport_profile must be a dict")
    _require_allowed_keys(value, _ALLOWED_TRANSPORT_KEYS, "transport_profile")
    laundering = scan_for_authority_laundering(value, "transport_profile")
    if laundering:
        raise TransportContractValidationError(
            "forbidden authority wording: " + "; ".join(laundering)
        )
    if value != _TRANSPORT_PROFILE:
        raise TransportContractValidationError("transport_profile mismatch")


def _validate_fixed_tool_registry(value: Any) -> None:
    if value != _FIXED_TOOL_REGISTRY:
        raise TransportContractValidationError("fixed_tool_registry mismatch")


def _validate_required_evidence_inputs(value: Any) -> None:
    if not isinstance(value, list):
        raise TransportContractValidationError("required_evidence_inputs must be a list")
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise TransportContractValidationError(
                "required_evidence_inputs entries must be dicts"
            )
        _require_allowed_keys(item, _ALLOWED_EVIDENCE_KEYS, f"evidence[{index}]")
        _require_hash(item.get("hash"), f"evidence[{index}].hash")
    if value != _REQUIRED_EVIDENCE_INPUTS:
        raise TransportContractValidationError("required_evidence_inputs mismatch")


def _validate_e2e_readiness(value: Any) -> None:
    if not isinstance(value, dict):
        raise TransportContractValidationError("e2e_validation_readiness must be a dict")
    _require_allowed_keys(value, _ALLOWED_READINESS_KEYS, "e2e_validation_readiness")
    if value != _E2E_READINESS:
        raise TransportContractValidationError("e2e_validation_readiness mismatch")


def _validate_side_effects(value: Any) -> None:
    if not isinstance(value, dict):
        raise TransportContractValidationError("side_effects must be a dict")
    if set(value) != set(_EXPECTED_SIDE_EFFECTS):
        raise TransportContractValidationError("side_effects keys mismatch")
    for key in _EXPECTED_SIDE_EFFECTS:
        if value.get(key) is not False:
            raise TransportContractValidationError(f"side_effects {key} must be False")


def _require_allowed_keys(value: dict[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if extra:
        raise TransportContractValidationError(
            f"{label} unsupported field(s): {', '.join(extra)}"
        )
    if missing:
        raise TransportContractValidationError(
            f"{label} missing field(s): {', '.join(missing)}"
        )


def _require_hash(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise TransportContractValidationError(f"{label} must be canonical sha256")
    if not value.startswith("sha256:") or len(value) != 71:
        raise TransportContractValidationError(f"{label} must be canonical sha256")
    if not all(ch in "0123456789abcdef" for ch in value.removeprefix("sha256:")):
        raise TransportContractValidationError(f"{label} must be canonical sha256")


def _hash_package(package: Any) -> str:
    encoded = json.dumps(package, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
