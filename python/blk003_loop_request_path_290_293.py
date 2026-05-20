"""BLK-SYSTEM-290..293 reusable BLK-003 loop request path packages.

These builders wire the existing BLK-003 loop kernel, BLK-ID/BLK-relay
provenance, and BLK-SYSTEM-286..289 speculative quarantine gate into a
reviewable request path. They emit deterministic, local, hash-bound evidence
only. They do not start BLK-pipe, invoke Codex, dispatch relay messages, read
protected bodies, publish BEOs, generate RTM, touch production blk-link, mutate
source/Git state, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk_root_doctrine_gap_ladder_237_241 import _validate_241_loop
from blk_speculative_quarantine_approval_286_289 import (
    SpeculativeQuarantineValidationError,
    validate_approval_timing_contract_286,
    validate_hitl_interaction_evidence_287,
    validate_promotion_or_purge_gate_289,
    validate_speculative_quarantine_evidence_288,
)


class Blk003LoopRequestPathValidationError(ValueError):
    """Raised when reusable BLK-003 loop request evidence fails closed."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_PROFILE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,80}$")
_CODEX_MODEL_RE = re.compile(r"^gpt-[0-9](?:\.[0-9])?(?:-[a-z0-9]+)?$")

CANONICAL_BLK241_LOOP_KERNEL_HASH = "sha256:c2819a7d995a791dccee0bd7ab368f40ad42296be5b777dc0a6558603728415e"
CANONICAL_BLK286_APPROVAL_TIMING_CONTRACT_HASH = "sha256:24f0cf02e473374a6af4360189bd8271acebf906a263baea541cd6db2d004d0c"

NEXT_FRONTIER_293 = "NEXT_FRONTIER_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_REQUIRED_NOT_GRANTED"

_REQUIRED_REQUEST_FIELDS = (
    "request_id",
    "beb_hash",
    "l2_packet_hash",
    "manifest_hash",
    "target_hash",
    "allowed_modified_files_hash",
    "validation_profile_id",
    "trusted_root_hash",
    "trusted_workdir_hash",
    "promotion_or_purge_gate_hash",
    "codex_model",
)
_ALLOWED_REQUEST_STATES = (
    "REQUEST_CONTRACT_READY",
    "BEB_L2_ROUTE_BOUND",
    "QUARANTINE_GATE_PREFLIGHT_READY",
    "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED",
)
_ALLOWED_PREFLIGHT_RESULTS = (
    "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION",
    "REQUEST_PATH_BLOCKED_BY_QUARANTINE_GATE",
    "REQUEST_PATH_BLOCKED_BY_TARGET_HASH_DRIFT",
)
_ALLOWED_RECONCILED_STATES = (
    "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED",
    "REQUEST_PATH_BLOCKED_GATE_OR_TARGET_DRIFT",
)
_CONTRACT_MARKERS = (
    "BLK_SYSTEM_290_BLK003_LOOP_REQUEST_CONTRACT_READY",
    "BLK003_LOOP_KERNEL_BOUND_TO_QUARANTINE_GATE",
    "REQUEST_PATH_EVIDENCE_ONLY_NO_RUNTIME_DISPATCH",
)
_BINDING_MARKERS = (
    "BLK_SYSTEM_291_BEB_L2_ROUTE_REQUEST_BINDING_READY",
    "BEB_L2_MANIFEST_TARGET_AND_GATE_HASH_BOUND",
    "ROUTE_BINDING_RECORD_ONLY_NO_DISPATCH",
)
_PREFLIGHT_MARKERS = (
    "BLK_SYSTEM_292_QUARANTINE_GATED_REQUEST_PREFLIGHT_READY",
    "QUARANTINE_GATE_AND_TARGET_HASH_RECHECKED",
    "PREFLIGHT_RECORD_ONLY_NO_RUNTIME_DISPATCH",
)
_RECONCILIATION_MARKERS = (
    "BLK_SYSTEM_293_REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED",
    "REQUEST_PATH_RECONCILED_EXECUTION_STILL_NOT_GRANTED",
    "NEXT_EXACT_PACKAGE_REQUIRED_BEFORE_RUNTIME",
)

_REQUEST_PATH_SIDE_EFFECTS = {
    "blk_pipe_runtime_started": False,
    "live_codex_dispatch_started": False,
    "relay_network_runtime_created": False,
    "message_dispatch_authorized": False,
    "approval_reuse": False,
    "target_source_git_mutation": False,
    "durable_target_mutation": False,
    "protected_body_access": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "package_manager_called": False,
    "network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_CONTRACT_KEYS = frozenset(
    {
        "status",
        "markers",
        "loop_kernel_hash",
        "approval_timing_contract_hash",
        "required_request_fields",
        "allowed_request_states",
        "quarantine_gate_required",
        "target_hash_recheck_required",
        "private_bwrap_descriptor_required_for_workspace_write",
        "separate_exact_execution_package_required",
        "side_effects",
        "loop_request_contract_hash",
    }
)
_BINDING_KEYS = frozenset(
    {
        "status",
        "markers",
        "loop_request_contract_hash",
        "approval_timing_contract_hash",
        "promotion_or_purge_gate_hash",
        "gate_outcome_state",
        "gate_allows_promotion",
        "request_id",
        "route",
        "beb_hash",
        "l2_packet_hash",
        "manifest_hash",
        "target_hash",
        "allowed_modified_files_hash",
        "validation_profile_id",
        "trusted_root_hash",
        "trusted_workdir_hash",
        "codex_model",
        "runtime_dispatch_requested",
        "side_effects",
        "route_request_binding_hash",
    }
)
_PREFLIGHT_KEYS = frozenset(
    {
        "status",
        "markers",
        "loop_request_contract_hash",
        "route_request_binding_hash",
        "promotion_or_purge_gate_hash",
        "gate_outcome_state",
        "observed_target_hash",
        "target_hash_rechecked",
        "private_bwrap_descriptor_hash",
        "validation_profile_hash",
        "preflight_result",
        "request_path_ready",
        "purge_required_or_completed",
        "runtime_dispatch_performed",
        "separate_exact_execution_package_required",
        "side_effects",
        "preflight_hash",
    }
)
_RECONCILIATION_KEYS = frozenset(
    {
        "status",
        "markers",
        "loop_request_contract_hash",
        "route_request_binding_hash",
        "preflight_hash",
        "reconciled_state",
        "next_frontier",
        "separate_exact_execution_package_required",
        "side_effects",
        "reconciliation_hash",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _without_hash(package: dict[str, Any], field: str) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in package.items() if key != field}


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise Blk003LoopRequestPathValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    _require_dict(package, context)
    extras = sorted(set(package) - allowed)
    if extras:
        raise Blk003LoopRequestPathValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise Blk003LoopRequestPathValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise Blk003LoopRequestPathValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise Blk003LoopRequestPathValidationError(f"{context} hash mismatch for {field}")


def _require_ascii(value: str, context: str) -> None:
    if not isinstance(value, str) or any(ord(ch) > 127 for ch in value):
        raise Blk003LoopRequestPathValidationError(f"{context} must contain ASCII characters only")


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, path=context)
    if errors:
        raise Blk003LoopRequestPathValidationError(
            f"{context} forbidden authority wording: {'; '.join(errors[:4])}"
        )


def _require_exact_id(value: Any, prefix: str, context: str) -> None:
    if not isinstance(value, str):
        raise Blk003LoopRequestPathValidationError(f"{context} must be a string")
    _require_ascii(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise Blk003LoopRequestPathValidationError(f"{context} must be an exact ID with prefix {prefix}")
    _reject_laundering(value, context)


def _require_profile_id(value: Any) -> None:
    if not isinstance(value, str) or not _PROFILE_ID_RE.match(value):
        raise Blk003LoopRequestPathValidationError("validation_profile_id must be lowercase profile id")
    _reject_laundering(value, "validation_profile_id")


def _require_codex_model(value: Any) -> None:
    if not isinstance(value, str) or not _CODEX_MODEL_RE.match(value):
        raise Blk003LoopRequestPathValidationError("codex_model must be an exact gpt model id")
    _reject_laundering(value, "codex_model")


def _require_exact_side_effects(package: dict[str, Any], context: str) -> None:
    if package.get("side_effects") != _REQUEST_PATH_SIDE_EFFECTS:
        raise Blk003LoopRequestPathValidationError(f"{context} side_effects mismatch")


def _validate_loop_kernel(loop_kernel: dict[str, Any]) -> dict[str, Any]:
    try:
        _validate_241_loop(loop_kernel)
    except Exception as exc:  # noqa: BLE001 - normalize upstream validation type.
        raise Blk003LoopRequestPathValidationError(f"loop kernel invalid: {exc}") from exc
    package = _deepcopy(loop_kernel)
    if package.get("loop_kernel_hash") != CANONICAL_BLK241_LOOP_KERNEL_HASH:
        raise Blk003LoopRequestPathValidationError("loop kernel canonical hash mismatch")
    side_effects = package.get("side_effects")
    for key in (
        "loop_runtime_execution",
        "reusable_codex_dispatch",
        "broad_blk_pipe_dispatch",
        "protected_body_access_without_exact_id",
        "beo_closeout_execution",
        "rtm_generation",
        "production_blk_test_mcp",
    ):
        if not isinstance(side_effects, dict) or side_effects.get(key) is not False:
            raise Blk003LoopRequestPathValidationError(f"loop kernel side_effects.{key} must remain false")
    return _deepcopy(package)


def _validate_approval_contract(approval_timing_contract: dict[str, Any]) -> dict[str, Any]:
    try:
        contract = validate_approval_timing_contract_286(approval_timing_contract)
    except SpeculativeQuarantineValidationError as exc:
        raise Blk003LoopRequestPathValidationError(f"approval timing contract invalid: {exc}") from exc
    if contract.get("approval_timing_contract_hash") != CANONICAL_BLK286_APPROVAL_TIMING_CONTRACT_HASH:
        raise Blk003LoopRequestPathValidationError("approval timing contract canonical hash mismatch")
    return contract


def _validate_gate_stack(
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = _validate_approval_contract(approval_timing_contract)
    try:
        interaction = validate_hitl_interaction_evidence_287(hitl_interaction, contract)
        quarantine_package = validate_speculative_quarantine_evidence_288(quarantine, contract, interaction)
        gate = validate_promotion_or_purge_gate_289(
            promotion_or_purge_gate,
            contract,
            quarantine_package,
            interaction,
        )
    except SpeculativeQuarantineValidationError as exc:
        raise Blk003LoopRequestPathValidationError(f"promotion/purge gate stack invalid: {exc}") from exc
    return quarantine_package, interaction, gate


def build_loop_request_contract_290(
    loop_kernel: dict[str, Any],
    approval_timing_contract: dict[str, Any],
) -> dict[str, Any]:
    """Bind the BLK-003 loop kernel to the quarantine-gate request contract."""

    loop = _validate_loop_kernel(loop_kernel)
    contract = _validate_approval_contract(approval_timing_contract)
    package = {
        "status": "BLK003_LOOP_REQUEST_CONTRACT_READY",
        "markers": list(_CONTRACT_MARKERS),
        "loop_kernel_hash": loop["loop_kernel_hash"],
        "approval_timing_contract_hash": contract["approval_timing_contract_hash"],
        "required_request_fields": list(_REQUIRED_REQUEST_FIELDS),
        "allowed_request_states": list(_ALLOWED_REQUEST_STATES),
        "quarantine_gate_required": True,
        "target_hash_recheck_required": True,
        "private_bwrap_descriptor_required_for_workspace_write": True,
        "separate_exact_execution_package_required": True,
        "side_effects": dict(_REQUEST_PATH_SIDE_EFFECTS),
    }
    package["loop_request_contract_hash"] = hash_package(package)
    return validate_loop_request_contract_290(package)


def validate_loop_request_contract_290(contract: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(contract, "loop request contract")
    _require_allowed_keys(package, _CONTRACT_KEYS, "loop request contract")
    if package.get("status") != "BLK003_LOOP_REQUEST_CONTRACT_READY":
        raise Blk003LoopRequestPathValidationError("loop request contract status mismatch")
    if tuple(package.get("markers", ())) != _CONTRACT_MARKERS:
        raise Blk003LoopRequestPathValidationError("loop request contract markers mismatch")
    if package.get("loop_kernel_hash") != CANONICAL_BLK241_LOOP_KERNEL_HASH:
        raise Blk003LoopRequestPathValidationError("loop request contract loop kernel hash mismatch")
    if package.get("approval_timing_contract_hash") != CANONICAL_BLK286_APPROVAL_TIMING_CONTRACT_HASH:
        raise Blk003LoopRequestPathValidationError("loop request contract approval timing hash mismatch")
    if tuple(package.get("required_request_fields", [])) != _REQUIRED_REQUEST_FIELDS:
        raise Blk003LoopRequestPathValidationError("loop request contract required_request_fields mismatch")
    if tuple(package.get("allowed_request_states", [])) != _ALLOWED_REQUEST_STATES:
        raise Blk003LoopRequestPathValidationError("loop request contract allowed_request_states mismatch")
    for field in (
        "quarantine_gate_required",
        "target_hash_recheck_required",
        "private_bwrap_descriptor_required_for_workspace_write",
        "separate_exact_execution_package_required",
    ):
        if package.get(field) is not True:
            raise Blk003LoopRequestPathValidationError(f"loop request contract {field} must be true")
    _require_exact_side_effects(package, "loop request contract")
    _require_hash_field(package, "loop_request_contract_hash", "loop request contract")
    _reject_laundering(package, "loop request contract")
    return _deepcopy(package)


def build_beb_l2_route_request_binding_291(
    loop_request_contract: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    *,
    request_id: str,
    beb_hash: str,
    l2_packet_hash: str,
    manifest_hash: str,
    target_hash: str,
    allowed_modified_files_hash: str,
    validation_profile_id: str,
    trusted_root_hash: str,
    trusted_workdir_hash: str,
    codex_model: str,
) -> dict[str, Any]:
    """Bind a future exact BEB-L2 request to the existing quarantine gate."""

    contract = validate_loop_request_contract_290(loop_request_contract)
    quarantine_package, _interaction, gate = _validate_gate_stack(
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    if contract["approval_timing_contract_hash"] != gate["approval_timing_contract_hash"]:
        raise Blk003LoopRequestPathValidationError("route binding approval contract mismatch")
    _require_exact_id(request_id, "REQUEST-", "request_id")
    for field_name, value in (
        ("beb_hash", beb_hash),
        ("l2_packet_hash", l2_packet_hash),
        ("manifest_hash", manifest_hash),
        ("target_hash", target_hash),
        ("allowed_modified_files_hash", allowed_modified_files_hash),
        ("trusted_root_hash", trusted_root_hash),
        ("trusted_workdir_hash", trusted_workdir_hash),
    ):
        _require_hash(value, field_name)
    _require_profile_id(validation_profile_id)
    _require_codex_model(codex_model)
    if manifest_hash != quarantine_package["manifest_hash"]:
        raise Blk003LoopRequestPathValidationError("route binding manifest_hash must match quarantine evidence")
    if target_hash != quarantine_package["target_hash_before_quarantine"]:
        raise Blk003LoopRequestPathValidationError("route binding target_hash must match quarantine evidence")
    package = {
        "status": "BEB_L2_ROUTE_REQUEST_BINDING_READY",
        "markers": list(_BINDING_MARKERS),
        "loop_request_contract_hash": contract["loop_request_contract_hash"],
        "approval_timing_contract_hash": gate["approval_timing_contract_hash"],
        "promotion_or_purge_gate_hash": gate["promotion_or_purge_gate_hash"],
        "gate_outcome_state": gate["outcome_state"],
        "gate_allows_promotion": gate["promotion_gate_opened"],
        "request_id": request_id,
        "route": "BEB-L2 -> BLK-pipe -> Codex workspace-write",
        "beb_hash": beb_hash,
        "l2_packet_hash": l2_packet_hash,
        "manifest_hash": manifest_hash,
        "target_hash": target_hash,
        "allowed_modified_files_hash": allowed_modified_files_hash,
        "validation_profile_id": validation_profile_id,
        "trusted_root_hash": trusted_root_hash,
        "trusted_workdir_hash": trusted_workdir_hash,
        "codex_model": codex_model,
        "runtime_dispatch_requested": False,
        "side_effects": dict(_REQUEST_PATH_SIDE_EFFECTS),
    }
    package["route_request_binding_hash"] = hash_package(package)
    return validate_beb_l2_route_request_binding_291(
        package,
        contract,
        approval_timing_contract,
        quarantine_package,
        hitl_interaction,
        gate,
    )


def validate_beb_l2_route_request_binding_291(
    binding: dict[str, Any],
    loop_request_contract: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_request_contract_290(loop_request_contract)
    quarantine_package, _interaction, gate = _validate_gate_stack(
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    package = _require_dict(binding, "BEB-L2 route request binding")
    _require_allowed_keys(package, _BINDING_KEYS, "BEB-L2 route request binding")
    if package.get("status") != "BEB_L2_ROUTE_REQUEST_BINDING_READY":
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding status mismatch")
    if tuple(package.get("markers", ())) != _BINDING_MARKERS:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding markers mismatch")
    if package.get("loop_request_contract_hash") != contract["loop_request_contract_hash"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding contract hash mismatch")
    if package.get("approval_timing_contract_hash") != contract["approval_timing_contract_hash"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding approval hash mismatch")
    if package.get("promotion_or_purge_gate_hash") != gate["promotion_or_purge_gate_hash"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding gate hash mismatch")
    if package.get("gate_outcome_state") != gate["outcome_state"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding gate outcome mismatch")
    if package.get("gate_allows_promotion") is not gate["promotion_gate_opened"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding gate flag mismatch")
    _require_exact_id(package.get("request_id"), "REQUEST-", "BEB-L2 route request binding request_id")
    if package.get("route") != "BEB-L2 -> BLK-pipe -> Codex workspace-write":
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding route mismatch")
    for field in (
        "beb_hash",
        "l2_packet_hash",
        "manifest_hash",
        "target_hash",
        "allowed_modified_files_hash",
        "trusted_root_hash",
        "trusted_workdir_hash",
    ):
        _require_hash(package.get(field), f"BEB-L2 route request binding {field}")
    if package.get("manifest_hash") != quarantine_package["manifest_hash"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding manifest hash mismatch")
    if package.get("target_hash") != quarantine_package["target_hash_before_quarantine"]:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding target hash mismatch")
    _require_profile_id(package.get("validation_profile_id"))
    _require_codex_model(package.get("codex_model"))
    if package.get("runtime_dispatch_requested") is not False:
        raise Blk003LoopRequestPathValidationError("BEB-L2 route request binding must not request runtime dispatch")
    _require_exact_side_effects(package, "BEB-L2 route request binding")
    _require_hash_field(package, "route_request_binding_hash", "BEB-L2 route request binding")
    _reject_laundering(package, "BEB-L2 route request binding")
    return _deepcopy(package)


def _resolve_preflight_result(gate: dict[str, Any], binding: dict[str, Any], observed_target_hash: str) -> str:
    if gate["outcome_state"] != "APPROVED_PROMOTED" or gate["promotion_gate_opened"] is not True:
        return "REQUEST_PATH_BLOCKED_BY_QUARANTINE_GATE"
    if observed_target_hash != binding["target_hash"]:
        return "REQUEST_PATH_BLOCKED_BY_TARGET_HASH_DRIFT"
    return "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION"


def build_quarantine_gated_request_preflight_292(
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    *,
    observed_target_hash: str,
    private_bwrap_descriptor_hash: str,
    validation_profile_hash: str,
) -> dict[str, Any]:
    """Evaluate the request path without starting runtime or mutating state."""

    contract = validate_loop_request_contract_290(loop_request_contract)
    _quarantine_package, _interaction, gate = _validate_gate_stack(
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    binding = validate_beb_l2_route_request_binding_291(
        route_request_binding,
        contract,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        gate,
    )
    _require_hash(observed_target_hash, "observed_target_hash")
    _require_hash(private_bwrap_descriptor_hash, "private_bwrap_descriptor_hash")
    _require_hash(validation_profile_hash, "validation_profile_hash")
    result = _resolve_preflight_result(gate, binding, observed_target_hash)
    package = {
        "status": "QUARANTINE_GATED_REQUEST_PREFLIGHT_READY",
        "markers": list(_PREFLIGHT_MARKERS),
        "loop_request_contract_hash": contract["loop_request_contract_hash"],
        "route_request_binding_hash": binding["route_request_binding_hash"],
        "promotion_or_purge_gate_hash": gate["promotion_or_purge_gate_hash"],
        "gate_outcome_state": gate["outcome_state"],
        "observed_target_hash": observed_target_hash,
        "target_hash_rechecked": observed_target_hash == binding["target_hash"],
        "private_bwrap_descriptor_hash": private_bwrap_descriptor_hash,
        "validation_profile_hash": validation_profile_hash,
        "preflight_result": result,
        "request_path_ready": result == "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION",
        "purge_required_or_completed": gate["purge_performed"],
        "runtime_dispatch_performed": False,
        "separate_exact_execution_package_required": True,
        "side_effects": dict(_REQUEST_PATH_SIDE_EFFECTS),
    }
    package["preflight_hash"] = hash_package(package)
    return validate_quarantine_gated_request_preflight_292(
        package,
        contract,
        binding,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        gate,
    )


def validate_quarantine_gated_request_preflight_292(
    preflight: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_request_contract_290(loop_request_contract)
    _quarantine_package, _interaction, gate = _validate_gate_stack(
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    binding = validate_beb_l2_route_request_binding_291(
        route_request_binding,
        contract,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        gate,
    )
    package = _require_dict(preflight, "quarantine-gated request preflight")
    _require_allowed_keys(package, _PREFLIGHT_KEYS, "quarantine-gated request preflight")
    if package.get("status") != "QUARANTINE_GATED_REQUEST_PREFLIGHT_READY":
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight status mismatch")
    if tuple(package.get("markers", ())) != _PREFLIGHT_MARKERS:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight markers mismatch")
    if package.get("loop_request_contract_hash") != contract["loop_request_contract_hash"]:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight contract hash mismatch")
    if package.get("route_request_binding_hash") != binding["route_request_binding_hash"]:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight binding hash mismatch")
    if package.get("promotion_or_purge_gate_hash") != gate["promotion_or_purge_gate_hash"]:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight gate hash mismatch")
    if package.get("gate_outcome_state") != gate["outcome_state"]:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight gate outcome mismatch")
    for field in ("observed_target_hash", "private_bwrap_descriptor_hash", "validation_profile_hash"):
        _require_hash(package.get(field), f"quarantine-gated request preflight {field}")
    expected_result = _resolve_preflight_result(gate, binding, package["observed_target_hash"])
    if package.get("preflight_result") != expected_result:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight result mismatch")
    if package.get("preflight_result") not in _ALLOWED_PREFLIGHT_RESULTS:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight result unsupported")
    ready_expected = package["preflight_result"] == "REQUEST_PATH_READY_FOR_SEPARATE_EXACT_EXECUTION"
    if package.get("request_path_ready") is not ready_expected:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight ready flag mismatch")
    if package.get("target_hash_rechecked") is not (package["observed_target_hash"] == binding["target_hash"]):
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight target hash flag mismatch")
    if package.get("purge_required_or_completed") is not gate["purge_performed"]:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight purge flag mismatch")
    if package.get("runtime_dispatch_performed") is not False:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight must not dispatch runtime")
    if package.get("separate_exact_execution_package_required") is not True:
        raise Blk003LoopRequestPathValidationError("quarantine-gated request preflight must require separate exact package")
    _require_exact_side_effects(package, "quarantine-gated request preflight")
    _require_hash_field(package, "preflight_hash", "quarantine-gated request preflight")
    _reject_laundering(package, "quarantine-gated request preflight")
    return _deepcopy(package)


def build_loop_request_path_reconciliation_293(
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    preflight: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile request-path readiness and name the next exact package."""

    contract = validate_loop_request_contract_290(loop_request_contract)
    binding = validate_beb_l2_route_request_binding_291(
        route_request_binding,
        contract,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight_package = validate_quarantine_gated_request_preflight_292(
        preflight,
        contract,
        binding,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    reconciled_state = (
        "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED"
        if preflight_package["request_path_ready"] is True
        else "REQUEST_PATH_BLOCKED_GATE_OR_TARGET_DRIFT"
    )
    package = {
        "status": "REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED",
        "markers": list(_RECONCILIATION_MARKERS),
        "loop_request_contract_hash": contract["loop_request_contract_hash"],
        "route_request_binding_hash": binding["route_request_binding_hash"],
        "preflight_hash": preflight_package["preflight_hash"],
        "reconciled_state": reconciled_state,
        "next_frontier": NEXT_FRONTIER_293,
        "separate_exact_execution_package_required": True,
        "side_effects": dict(_REQUEST_PATH_SIDE_EFFECTS),
    }
    package["reconciliation_hash"] = hash_package(package)
    return validate_loop_request_path_reconciliation_293(
        package,
        contract,
        binding,
        preflight_package,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )


def validate_loop_request_path_reconciliation_293(
    reconciliation: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    preflight: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_request_contract_290(loop_request_contract)
    binding = validate_beb_l2_route_request_binding_291(
        route_request_binding,
        contract,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight_package = validate_quarantine_gated_request_preflight_292(
        preflight,
        contract,
        binding,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    package = _require_dict(reconciliation, "loop request path reconciliation")
    _require_allowed_keys(package, _RECONCILIATION_KEYS, "loop request path reconciliation")
    if package.get("status") != "REUSABLE_BLK003_LOOP_REQUEST_PATH_RECONCILED":
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation status mismatch")
    if tuple(package.get("markers", ())) != _RECONCILIATION_MARKERS:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation markers mismatch")
    if package.get("loop_request_contract_hash") != contract["loop_request_contract_hash"]:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation contract hash mismatch")
    if package.get("route_request_binding_hash") != binding["route_request_binding_hash"]:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation binding hash mismatch")
    if package.get("preflight_hash") != preflight_package["preflight_hash"]:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation preflight hash mismatch")
    expected_state = (
        "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED"
        if preflight_package.get("request_path_ready") is True
        else "REQUEST_PATH_BLOCKED_GATE_OR_TARGET_DRIFT"
    )
    if package.get("reconciled_state") != expected_state:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation reconciled_state mismatch")
    if package.get("reconciled_state") not in _ALLOWED_RECONCILED_STATES:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation reconciled_state unsupported")
    if package.get("next_frontier") != NEXT_FRONTIER_293:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation next_frontier mismatch")
    if package.get("separate_exact_execution_package_required") is not True:
        raise Blk003LoopRequestPathValidationError("loop request path reconciliation must require separate exact package")
    _require_exact_side_effects(package, "loop request path reconciliation")
    _require_hash_field(package, "reconciliation_hash", "loop request path reconciliation")
    _reject_laundering(package, "loop request path reconciliation")
    return _deepcopy(package)
