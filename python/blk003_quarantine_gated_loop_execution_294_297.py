"""BLK-SYSTEM-294..297 exact quarantine-gated BLK-003 loop package.

This module consumes the BLK-SYSTEM-290..293 request path and records one
hash-bound, quarantine-contained loop run package. It revalidates the full
request path before each step, enforces fresh target/worktree/sandbox evidence,
keeps the failure ceiling at three attempts, requires BEO draft evidence, and
keeps durable target/source/Git state, BEO closeout, BEO publication, RTM,
production blk-link, production BLK-test MCP transport, and reusable runtime
surfaces outside this package.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk003_loop_request_path_290_293 import (
    Blk003LoopRequestPathValidationError,
    validate_beb_l2_route_request_binding_291,
    validate_loop_request_contract_290,
    validate_loop_request_path_reconciliation_293,
    validate_quarantine_gated_request_preflight_292,
)


class Blk003LoopExecutionPackageValidationError(ValueError):
    """Raised when BLK-003 exact loop execution package evidence is unsafe."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

NEXT_FRONTIER_297 = "NEXT_FRONTIER_EXACT_BLK_TEST_ORACLE_VERIFICATION_AFTER_LOOP_EXECUTION_REQUIRED_NOT_GRANTED"

_PACKAGE_MARKERS_294 = (
    "BLK_SYSTEM_294_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY",
    "LOOP_REQUEST_PATH_REVALIDATED_BEFORE_EXECUTION",
    "NO_REUSABLE_RUNTIME_OR_CODEX_DISPATCH_AUTHORITY",
)
_PREFLIGHT_MARKERS_295 = (
    "BLK_SYSTEM_295_FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY",
    "TARGET_WORKTREE_AND_SANDBOX_RECHECKED",
    "NO_RUNTIME_DISPATCH_DURING_PREFLIGHT",
)
_EXECUTION_MARKERS_296 = (
    "BLK_SYSTEM_296_QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED",
    "FAILURE_CEILING_ENFORCED_THREE_ATTEMPTS",
    "DURABLE_TARGET_SOURCE_GIT_MUTATION_BLOCKED",
)
_RECONCILIATION_MARKERS_297 = (
    "BLK_SYSTEM_297_EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED",
    "BOUND_LOOP_EXECUTION_EVIDENCE_READY_FOR_BLK_TEST",
    "NEXT_EXACT_BLK_TEST_ORACLE_VERIFICATION_REQUIRED",
)

_STOP_CONDITIONS = (
    "STOP_AFTER_THREE_FAILED_ATTEMPTS",
    "STOP_ON_TARGET_HASH_DRIFT",
    "STOP_ON_WORKTREE_OR_SANDBOX_DRIFT",
    "STOP_ON_DURABLE_TARGET_SOURCE_GIT_MUTATION_SIGNAL",
    "STOP_BEFORE_BEO_CLOSEOUT_OR_PUBLICATION",
)

_ALLOWED_PREFLIGHT_RESULTS = (
    "EXACT_LOOP_EXECUTION_PREFLIGHT_READY",
    "EXACT_LOOP_EXECUTION_BLOCKED_BY_TARGET_HASH_DRIFT",
    "EXACT_LOOP_EXECUTION_BLOCKED_BY_WORKTREE_OR_SANDBOX",
)
_ALLOWED_ATTEMPT_STATUSES = (
    "FAILED_RETRYABLE",
    "FAILED_TERMINAL",
    "SUCCEEDED",
)
_ALLOWED_FINAL_RESULTS = (
    "SUCCEEDED",
    "FAILED_TERMINAL",
    "FAILED_RETRY_LIMIT",
)

_PACKAGE_SIDE_EFFECTS_294 = {
    "execution_package_prepared": True,
    "fresh_preflight_recorded": False,
    "quarantine_workspace_mutation_recorded": False,
    "bounded_loop_execution_recorded": False,
    "blk_pipe_runtime_attempt_recorded": False,
    "live_codex_dispatch_attempt_recorded": False,
    "reusable_codex_dispatch": False,
    "broad_blk_pipe_dispatch": False,
    "approval_reuse": False,
    "durable_target_source_git_mutation": False,
    "source_git_commit_created": False,
    "beo_draft_recorded": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "production_blk_test_mcp": False,
    "package_manager_called": False,
    "network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_PREFLIGHT_SIDE_EFFECTS_295 = dict(_PACKAGE_SIDE_EFFECTS_294)
_PREFLIGHT_SIDE_EFFECTS_295["fresh_preflight_recorded"] = True
_EXECUTION_SIDE_EFFECTS_296 = dict(_PREFLIGHT_SIDE_EFFECTS_295)
_EXECUTION_SIDE_EFFECTS_296.update(
    {
        "quarantine_workspace_mutation_recorded": True,
        "bounded_loop_execution_recorded": True,
        "blk_pipe_runtime_attempt_recorded": True,
        "live_codex_dispatch_attempt_recorded": True,
        "beo_draft_recorded": True,
    }
)

_PACKAGE_KEYS_294 = frozenset(
    {
        "status",
        "markers",
        "loop_request_contract_hash",
        "route_request_binding_hash",
        "request_path_preflight_hash",
        "request_path_reconciliation_hash",
        "execution_package_id",
        "run_id",
        "request_id",
        "beb_hash",
        "l2_packet_hash",
        "manifest_hash",
        "target_hash",
        "allowed_modified_files_hash",
        "validation_profile_id",
        "trusted_root_hash",
        "trusted_workdir_hash",
        "codex_model",
        "requested_at",
        "expires_at",
        "failure_ceiling",
        "stop_conditions",
        "beo_draft_required",
        "beo_closeout_execution_allowed",
        "side_effects",
        "execution_package_hash",
    }
)
_PREFLIGHT_KEYS_295 = frozenset(
    {
        "status",
        "markers",
        "execution_package_hash",
        "route_request_binding_hash",
        "request_path_preflight_hash",
        "observed_target_hash",
        "target_hash_rechecked",
        "observed_trusted_root_hash",
        "trusted_root_hash_rechecked",
        "observed_trusted_workdir_hash",
        "trusted_workdir_hash_rechecked",
        "observed_private_bwrap_descriptor_hash",
        "sandbox_descriptor_rechecked",
        "observed_validation_profile_hash",
        "validation_profile_hash_rechecked",
        "sandbox_profile_state",
        "worktree_state",
        "evaluated_at",
        "preflight_result",
        "execution_allowed",
        "runtime_dispatch_performed",
        "side_effects",
        "fresh_preflight_hash",
    }
)
_ATTEMPT_KEYS = frozenset({"attempt", "status", "started_at", "completed_at", "report_hash"})
_RUNTIME_REPORT_KEYS = frozenset(
    {
        "run_id",
        "quarantine_workspace_id",
        "attempts",
        "final_result",
        "dispatcher_report_hash",
        "result_hash",
        "post_execution_target_hash",
        "cleanup_evidence_hash",
        "beo_draft_hash",
        "completed_at",
        "durable_target_source_git_mutation",
        "source_git_commit_created",
        "beo_closeout_executed",
        "beo_publication_performed",
        "rtm_generation_performed",
        "production_blk_link_performed",
        "package_manager_called",
        "network_model_browser_cyber_tooling",
        "production_isolation_claim",
        "reusable_codex_dispatch",
        "broad_blk_pipe_dispatch",
        "approval_reuse",
        "production_blk_test_mcp",
        "relay_network_runtime_created",
        "message_dispatch_performed",
        "protected_body_access",
        "runtime_tooling_performed",
        "prior_consumed_run_ids",
        "consumed_run_ids",
    }
)
_EXECUTION_RECORD_KEYS_296 = frozenset(
    {
        "status",
        "markers",
        "execution_package_hash",
        "fresh_preflight_hash",
        "run_id",
        "quarantine_workspace_id",
        "attempts",
        "attempt_count",
        "failure_ceiling",
        "final_result",
        "dispatcher_report_hash",
        "result_hash",
        "post_execution_target_hash",
        "target_hash_preserved",
        "cleanup_evidence_hash",
        "beo_draft_hash",
        "completed_at",
        "beo_draft_recorded",
        "beo_closeout_execution_performed",
        "side_effects",
        "execution_record_hash",
    }
)
_RECONCILIATION_KEYS_297 = frozenset(
    {
        "status",
        "markers",
        "execution_package_hash",
        "fresh_preflight_hash",
        "execution_record_hash",
        "run_id",
        "final_result",
        "result_hash",
        "dispatcher_report_hash",
        "beo_draft_hash",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)


# Filled after implementation verification; kept as constants for docs/tests to cite.
_CANONICAL_EXECUTION_PACKAGE_294_HASH: str | None = "sha256:1e2baea95f88e9a569661d36f688b2936092e47bff0b5bc784dec2314e2be95a"
_CANONICAL_FRESH_PREFLIGHT_295_HASH: str | None = "sha256:f4dd57b92af66453f9f1cb58faa359df2ba4ef329e57b41fc8d7670a553c285a"
_CANONICAL_EXECUTION_RECORD_296_HASH: str | None = "sha256:cb9bb4d9c04af2b7e82054da872a47ff6df3077fb468ba8eef32810512a3c5ed"
_CANONICAL_RECONCILIATION_297_HASH: str | None = "sha256:acf58ee2ddff633848eefc393ee65ac7de08d967c0042e8ad62c7179324efbed"


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
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(package) - allowed)
    if extras:
        raise Blk003LoopExecutionPackageValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise Blk003LoopExecutionPackageValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise Blk003LoopExecutionPackageValidationError(f"{context} hash mismatch for {field}")


def _require_ascii(value: str, context: str) -> None:
    if not isinstance(value, str) or any(ord(ch) > 127 for ch in value):
        raise Blk003LoopExecutionPackageValidationError(f"{context} must contain ASCII characters only")


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, path=context)
    if errors:
        raise Blk003LoopExecutionPackageValidationError(
            f"{context} forbidden authority wording: {'; '.join(errors[:4])}"
        )


def _require_exact_id(value: Any, prefix: str, context: str) -> None:
    if not isinstance(value, str):
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be a string")
    _require_ascii(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be an exact ID with prefix {prefix}")
    _reject_laundering(value, context)


def _parse_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP_RE.match(value):
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be an ISO-8601 timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be parseable") from exc
    if parsed.tzinfo is None:
        raise Blk003LoopExecutionPackageValidationError(f"{context} must include timezone")
    return parsed


def _require_time_window(start: Any, end: Any, start_name: str, end_name: str) -> None:
    parsed_start = _parse_timestamp(start, start_name)
    parsed_end = _parse_timestamp(end, end_name)
    if parsed_end <= parsed_start:
        raise Blk003LoopExecutionPackageValidationError(f"{end_name} must be after {start_name}")


def _require_timestamp_within(value: Any, start: Any, end: Any, context: str) -> datetime:
    parsed_value = _parse_timestamp(value, context)
    parsed_start = _parse_timestamp(start, "window_start")
    parsed_end = _parse_timestamp(end, "window_end")
    if parsed_value < parsed_start or parsed_value > parsed_end:
        raise Blk003LoopExecutionPackageValidationError(f"{context} must be within package time window")
    return parsed_value


def _validate_request_path_ready(
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        contract = validate_loop_request_contract_290(loop_request_contract)
        binding = validate_beb_l2_route_request_binding_291(
            route_request_binding,
            contract,
            approval_timing_contract,
            quarantine,
            hitl_interaction,
            promotion_or_purge_gate,
        )
        preflight = validate_quarantine_gated_request_preflight_292(
            request_path_preflight,
            contract,
            binding,
            approval_timing_contract,
            quarantine,
            hitl_interaction,
            promotion_or_purge_gate,
        )
        reconciliation = validate_loop_request_path_reconciliation_293(
            request_path_reconciliation,
            contract,
            binding,
            preflight,
            approval_timing_contract,
            quarantine,
            hitl_interaction,
            promotion_or_purge_gate,
        )
    except Blk003LoopRequestPathValidationError as exc:
        raise Blk003LoopExecutionPackageValidationError(f"request path must be ready: {exc}") from exc
    if preflight.get("request_path_ready") is not True:
        raise Blk003LoopExecutionPackageValidationError("request path must be ready before exact loop execution")
    if reconciliation.get("reconciled_state") != "REQUEST_PATH_READY_EXECUTION_NOT_GRANTED":
        raise Blk003LoopExecutionPackageValidationError("request path reconciliation must be ready before exact loop execution")
    return contract, binding, preflight, reconciliation


def build_exact_loop_execution_package_294(
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    *,
    execution_package_id: str,
    run_id: str,
    requested_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Build the exact loop execution package without dispatching runtime."""

    contract, binding, preflight, reconciliation = _validate_request_path_ready(
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    _require_exact_id(execution_package_id, "EXECUTION-PACKAGE-", "execution_package_id")
    _require_exact_id(run_id, "RUN-", "run_id")
    _require_time_window(requested_at, expires_at, "requested_at", "expires_at")
    package = {
        "status": "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY",
        "markers": list(_PACKAGE_MARKERS_294),
        "loop_request_contract_hash": contract["loop_request_contract_hash"],
        "route_request_binding_hash": binding["route_request_binding_hash"],
        "request_path_preflight_hash": preflight["preflight_hash"],
        "request_path_reconciliation_hash": reconciliation["reconciliation_hash"],
        "execution_package_id": execution_package_id,
        "run_id": run_id,
        "request_id": binding["request_id"],
        "beb_hash": binding["beb_hash"],
        "l2_packet_hash": binding["l2_packet_hash"],
        "manifest_hash": binding["manifest_hash"],
        "target_hash": binding["target_hash"],
        "allowed_modified_files_hash": binding["allowed_modified_files_hash"],
        "validation_profile_id": binding["validation_profile_id"],
        "trusted_root_hash": binding["trusted_root_hash"],
        "trusted_workdir_hash": binding["trusted_workdir_hash"],
        "codex_model": binding["codex_model"],
        "requested_at": requested_at,
        "expires_at": expires_at,
        "failure_ceiling": 3,
        "stop_conditions": list(_STOP_CONDITIONS),
        "beo_draft_required": True,
        "beo_closeout_execution_allowed": False,
        "side_effects": dict(_PACKAGE_SIDE_EFFECTS_294),
    }
    package["execution_package_hash"] = hash_package(package)
    return validate_exact_loop_execution_package_294(
        package,
        contract,
        binding,
        preflight,
        reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )


def validate_exact_loop_execution_package_294(
    execution_package: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    contract, binding, preflight, reconciliation = _validate_request_path_ready(
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    package = _require_dict(execution_package, "exact loop execution package")
    _require_allowed_keys(package, _PACKAGE_KEYS_294, "exact loop execution package")
    if package.get("status") != "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_PACKAGE_READY":
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package status mismatch")
    if tuple(package.get("markers", ())) != _PACKAGE_MARKERS_294:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package markers mismatch")
    expected_pairs = {
        "loop_request_contract_hash": contract["loop_request_contract_hash"],
        "route_request_binding_hash": binding["route_request_binding_hash"],
        "request_path_preflight_hash": preflight["preflight_hash"],
        "request_path_reconciliation_hash": reconciliation["reconciliation_hash"],
        "request_id": binding["request_id"],
        "beb_hash": binding["beb_hash"],
        "l2_packet_hash": binding["l2_packet_hash"],
        "manifest_hash": binding["manifest_hash"],
        "target_hash": binding["target_hash"],
        "allowed_modified_files_hash": binding["allowed_modified_files_hash"],
        "validation_profile_id": binding["validation_profile_id"],
        "trusted_root_hash": binding["trusted_root_hash"],
        "trusted_workdir_hash": binding["trusted_workdir_hash"],
        "codex_model": binding["codex_model"],
    }
    for field, expected in expected_pairs.items():
        if package.get(field) != expected:
            raise Blk003LoopExecutionPackageValidationError(f"exact loop execution package {field} mismatch")
    _require_exact_id(package.get("execution_package_id"), "EXECUTION-PACKAGE-", "execution_package_id")
    _require_exact_id(package.get("run_id"), "RUN-", "run_id")
    _require_time_window(package.get("requested_at"), package.get("expires_at"), "requested_at", "expires_at")
    if package.get("failure_ceiling") != 3:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package failure ceiling must be 3")
    if tuple(package.get("stop_conditions", ())) != _STOP_CONDITIONS:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package stop_conditions mismatch")
    if package.get("beo_draft_required") is not True:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package must require BEO draft evidence")
    if package.get("beo_closeout_execution_allowed") is not False:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package must not allow BEO closeout execution")
    if package.get("side_effects") != _PACKAGE_SIDE_EFFECTS_294:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution package side_effects mismatch")
    _require_hash_field(package, "execution_package_hash", "exact loop execution package")
    _reject_laundering(package, "exact loop execution package")
    return _deepcopy(package)


def _resolve_preflight_result(
    package: dict[str, Any],
    request_preflight: dict[str, Any],
    *,
    observed_target_hash: str,
    observed_trusted_root_hash: str,
    observed_trusted_workdir_hash: str,
    observed_private_bwrap_descriptor_hash: str,
    observed_validation_profile_hash: str,
    sandbox_profile_state: str,
    worktree_state: str,
) -> str:
    if observed_target_hash != package["target_hash"]:
        return "EXACT_LOOP_EXECUTION_BLOCKED_BY_TARGET_HASH_DRIFT"
    if (
        observed_trusted_root_hash != package["trusted_root_hash"]
        or observed_trusted_workdir_hash != package["trusted_workdir_hash"]
        or observed_private_bwrap_descriptor_hash != request_preflight["private_bwrap_descriptor_hash"]
        or observed_validation_profile_hash != request_preflight["validation_profile_hash"]
        or sandbox_profile_state != "PRIVATE_BWRAP_DESCRIPTOR_READY"
        or worktree_state != "CLEAN_EXACT_TARGET_WORKTREE"
    ):
        return "EXACT_LOOP_EXECUTION_BLOCKED_BY_WORKTREE_OR_SANDBOX"
    return "EXACT_LOOP_EXECUTION_PREFLIGHT_READY"


def build_fresh_execution_preflight_295(
    execution_package_294: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    *,
    observed_target_hash: str,
    observed_trusted_root_hash: str,
    observed_trusted_workdir_hash: str,
    observed_private_bwrap_descriptor_hash: str,
    observed_validation_profile_hash: str,
    sandbox_profile_state: str,
    worktree_state: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Record fresh target/worktree/sandbox evidence without dispatching runtime."""

    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    _require_hash(observed_target_hash, "observed_target_hash")
    _require_hash(observed_trusted_root_hash, "observed_trusted_root_hash")
    _require_hash(observed_trusted_workdir_hash, "observed_trusted_workdir_hash")
    _require_hash(observed_private_bwrap_descriptor_hash, "observed_private_bwrap_descriptor_hash")
    _require_hash(observed_validation_profile_hash, "observed_validation_profile_hash")
    _require_ascii(sandbox_profile_state, "sandbox_profile_state")
    _require_ascii(worktree_state, "worktree_state")
    _reject_laundering(sandbox_profile_state, "sandbox_profile_state")
    _reject_laundering(worktree_state, "worktree_state")
    _require_timestamp_within(evaluated_at, package["requested_at"], package["expires_at"], "evaluated_at")
    result = _resolve_preflight_result(
        package,
        request_path_preflight,
        observed_target_hash=observed_target_hash,
        observed_trusted_root_hash=observed_trusted_root_hash,
        observed_trusted_workdir_hash=observed_trusted_workdir_hash,
        observed_private_bwrap_descriptor_hash=observed_private_bwrap_descriptor_hash,
        observed_validation_profile_hash=observed_validation_profile_hash,
        sandbox_profile_state=sandbox_profile_state,
        worktree_state=worktree_state,
    )
    preflight = {
        "status": "FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY",
        "markers": list(_PREFLIGHT_MARKERS_295),
        "execution_package_hash": package["execution_package_hash"],
        "route_request_binding_hash": package["route_request_binding_hash"],
        "request_path_preflight_hash": package["request_path_preflight_hash"],
        "observed_target_hash": observed_target_hash,
        "target_hash_rechecked": observed_target_hash == package["target_hash"],
        "observed_trusted_root_hash": observed_trusted_root_hash,
        "trusted_root_hash_rechecked": observed_trusted_root_hash == package["trusted_root_hash"],
        "observed_trusted_workdir_hash": observed_trusted_workdir_hash,
        "trusted_workdir_hash_rechecked": observed_trusted_workdir_hash == package["trusted_workdir_hash"],
        "observed_private_bwrap_descriptor_hash": observed_private_bwrap_descriptor_hash,
        "sandbox_descriptor_rechecked": (
            observed_private_bwrap_descriptor_hash == request_path_preflight["private_bwrap_descriptor_hash"]
        ),
        "observed_validation_profile_hash": observed_validation_profile_hash,
        "validation_profile_hash_rechecked": (
            observed_validation_profile_hash == request_path_preflight["validation_profile_hash"]
        ),
        "sandbox_profile_state": sandbox_profile_state,
        "worktree_state": worktree_state,
        "evaluated_at": evaluated_at,
        "preflight_result": result,
        "execution_allowed": result == "EXACT_LOOP_EXECUTION_PREFLIGHT_READY",
        "runtime_dispatch_performed": False,
        "side_effects": dict(_PREFLIGHT_SIDE_EFFECTS_295),
    }
    preflight["fresh_preflight_hash"] = hash_package(preflight)
    return validate_fresh_execution_preflight_295(
        preflight,
        package,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )


def validate_fresh_execution_preflight_295(
    fresh_preflight: dict[str, Any],
    execution_package_294: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight = _require_dict(fresh_preflight, "fresh execution preflight")
    _require_allowed_keys(preflight, _PREFLIGHT_KEYS_295, "fresh execution preflight")
    if preflight.get("status") != "FRESH_TARGET_WORKTREE_SANDBOX_PREFLIGHT_READY":
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight status mismatch")
    if tuple(preflight.get("markers", ())) != _PREFLIGHT_MARKERS_295:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight markers mismatch")
    for field in (
        "observed_target_hash",
        "observed_trusted_root_hash",
        "observed_trusted_workdir_hash",
        "observed_private_bwrap_descriptor_hash",
        "observed_validation_profile_hash",
    ):
        _require_hash(preflight.get(field), f"fresh execution preflight {field}")
    if preflight.get("execution_package_hash") != package["execution_package_hash"]:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight package hash mismatch")
    if preflight.get("route_request_binding_hash") != package["route_request_binding_hash"]:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight binding hash mismatch")
    if preflight.get("request_path_preflight_hash") != package["request_path_preflight_hash"]:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight request preflight hash mismatch")
    expected_result = _resolve_preflight_result(
        package,
        request_path_preflight,
        observed_target_hash=preflight["observed_target_hash"],
        observed_trusted_root_hash=preflight["observed_trusted_root_hash"],
        observed_trusted_workdir_hash=preflight["observed_trusted_workdir_hash"],
        observed_private_bwrap_descriptor_hash=preflight["observed_private_bwrap_descriptor_hash"],
        observed_validation_profile_hash=preflight["observed_validation_profile_hash"],
        sandbox_profile_state=preflight["sandbox_profile_state"],
        worktree_state=preflight["worktree_state"],
    )
    if preflight.get("preflight_result") != expected_result:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight result mismatch")
    if preflight.get("preflight_result") not in _ALLOWED_PREFLIGHT_RESULTS:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight result unsupported")
    expected_flags = {
        "target_hash_rechecked": preflight["observed_target_hash"] == package["target_hash"],
        "trusted_root_hash_rechecked": preflight["observed_trusted_root_hash"] == package["trusted_root_hash"],
        "trusted_workdir_hash_rechecked": preflight["observed_trusted_workdir_hash"] == package["trusted_workdir_hash"],
        "sandbox_descriptor_rechecked": (
            preflight["observed_private_bwrap_descriptor_hash"] == request_path_preflight["private_bwrap_descriptor_hash"]
        ),
        "validation_profile_hash_rechecked": (
            preflight["observed_validation_profile_hash"] == request_path_preflight["validation_profile_hash"]
        ),
        "execution_allowed": expected_result == "EXACT_LOOP_EXECUTION_PREFLIGHT_READY",
    }
    for field, expected in expected_flags.items():
        if preflight.get(field) is not expected:
            raise Blk003LoopExecutionPackageValidationError(f"fresh execution preflight {field} mismatch")
    _require_timestamp_within(preflight.get("evaluated_at"), package["requested_at"], package["expires_at"], "evaluated_at")
    if preflight.get("runtime_dispatch_performed") is not False:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight must not dispatch runtime")
    if preflight.get("side_effects") != _PREFLIGHT_SIDE_EFFECTS_295:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight side_effects mismatch")
    _require_hash_field(preflight, "fresh_preflight_hash", "fresh execution preflight")
    _reject_laundering(preflight, "fresh execution preflight")
    return _deepcopy(preflight)


def _validate_attempts(
    attempts: Any,
    failure_ceiling: int,
    *,
    window_start: Any,
    window_end: Any,
) -> list[dict[str, Any]]:
    if not isinstance(attempts, list) or not attempts:
        raise Blk003LoopExecutionPackageValidationError("runtime report attempts must be a non-empty list")
    if len(attempts) > failure_ceiling:
        raise Blk003LoopExecutionPackageValidationError("runtime report attempts exceed failure ceiling")
    validated = []
    previous_completed: datetime | None = None
    seen_hashes: set[str] = set()
    for index, attempt in enumerate(attempts, start=1):
        item = _require_dict(attempt, f"attempt[{index}]")
        _require_allowed_keys(item, _ATTEMPT_KEYS, f"attempt[{index}]")
        if item.get("attempt") != index:
            raise Blk003LoopExecutionPackageValidationError("runtime report attempts must be sequential")
        if item.get("status") not in _ALLOWED_ATTEMPT_STATUSES:
            raise Blk003LoopExecutionPackageValidationError("runtime report attempt status unsupported")
        started = _require_timestamp_within(item.get("started_at"), window_start, window_end, f"attempt[{index}].started_at")
        completed = _require_timestamp_within(item.get("completed_at"), window_start, window_end, f"attempt[{index}].completed_at")
        if completed < started:
            raise Blk003LoopExecutionPackageValidationError("attempt completed_at must be after started_at")
        if previous_completed is not None and started < previous_completed:
            raise Blk003LoopExecutionPackageValidationError("runtime report attempts must be monotonic")
        previous_completed = completed
        _require_hash(item.get("report_hash"), f"attempt[{index}].report_hash")
        if item["report_hash"] in seen_hashes:
            raise Blk003LoopExecutionPackageValidationError("runtime report attempt hashes must be unique")
        seen_hashes.add(item["report_hash"])
        _reject_laundering(item, f"attempt[{index}]")
        validated.append(_deepcopy(item))
    return validated

def _validate_final_result(attempts: list[dict[str, Any]], final_result: Any, failure_ceiling: int) -> None:
    if final_result not in _ALLOWED_FINAL_RESULTS:
        raise Blk003LoopExecutionPackageValidationError("runtime report final_result unsupported")
    last_status = attempts[-1]["status"]
    if any(attempt["status"] == "FAILED_TERMINAL" for attempt in attempts[:-1]):
        raise Blk003LoopExecutionPackageValidationError("runtime report must stop after terminal failure")
    if final_result == "SUCCEEDED" and last_status != "SUCCEEDED":
        raise Blk003LoopExecutionPackageValidationError("runtime report final_result must match successful final attempt")
    if final_result == "FAILED_TERMINAL" and last_status != "FAILED_TERMINAL":
        raise Blk003LoopExecutionPackageValidationError("runtime report final_result must match terminal final attempt")
    if final_result == "FAILED_RETRY_LIMIT":
        if len(attempts) != failure_ceiling:
            raise Blk003LoopExecutionPackageValidationError("runtime report retry-limit result must consume failure ceiling")
        if any(attempt["status"] != "FAILED_RETRYABLE" for attempt in attempts):
            raise Blk003LoopExecutionPackageValidationError("runtime report retry-limit attempts must be retryable failures")
    if any(attempt["status"] == "SUCCEEDED" for attempt in attempts[:-1]):
        raise Blk003LoopExecutionPackageValidationError("runtime report must stop after first successful attempt")

def _validate_runtime_report(runtime_report: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    report = _require_dict(runtime_report, "runtime report")
    _require_allowed_keys(report, _RUNTIME_REPORT_KEYS, "runtime report")
    _require_exact_id(report.get("run_id"), "RUN-", "runtime report run_id")
    if report.get("run_id") != package["run_id"]:
        raise Blk003LoopExecutionPackageValidationError("runtime report run_id mismatch")
    _require_exact_id(report.get("quarantine_workspace_id"), "QUARANTINE-", "runtime report quarantine_workspace_id")
    attempts = _validate_attempts(
        report.get("attempts"),
        package["failure_ceiling"],
        window_start=package["requested_at"],
        window_end=package["expires_at"],
    )
    _validate_final_result(attempts, report.get("final_result"), package["failure_ceiling"])
    for field in (
        "dispatcher_report_hash",
        "result_hash",
        "post_execution_target_hash",
        "cleanup_evidence_hash",
        "beo_draft_hash",
    ):
        _require_hash(report.get(field), f"runtime report {field}")
    if report.get("post_execution_target_hash") != package["target_hash"]:
        raise Blk003LoopExecutionPackageValidationError("runtime report post-execution target hash must match package target hash")
    _require_timestamp_within(report.get("completed_at"), package["requested_at"], package["expires_at"], "runtime report completed_at")
    denied_true_fields = {
        "durable_target_source_git_mutation": "durable target/source/Git mutation must remain false",
        "source_git_commit_created": "source Git commit creation must remain false",
        "beo_closeout_executed": "BEO closeout execution must remain false",
        "beo_publication_performed": "BEO publication must remain false",
        "rtm_generation_performed": "RTM generation must remain false",
        "production_blk_link_performed": "production blk-link must remain false",
        "package_manager_called": "package manager must remain false",
        "network_model_browser_cyber_tooling": "network/model/browser/cyber tooling must remain false",
        "production_isolation_claim": "production-isolation claim must remain false",
        "reusable_codex_dispatch": "reusable Codex dispatch must remain false",
        "broad_blk_pipe_dispatch": "broad BLK-pipe dispatch must remain false",
        "approval_reuse": "approval reuse must remain false",
        "production_blk_test_mcp": "production BLK-test MCP must remain false",
        "relay_network_runtime_created": "relay network runtime must remain false",
        "message_dispatch_performed": "message dispatch must remain false",
        "protected_body_access": "protected-body access must remain false",
        "runtime_tooling_performed": "runtime tooling must remain false",
    }
    for field, message in denied_true_fields.items():
        if report.get(field) is not False:
            raise Blk003LoopExecutionPackageValidationError(message)
    prior_ids = report.get("prior_consumed_run_ids")
    consumed_ids = report.get("consumed_run_ids")
    if not isinstance(prior_ids, list) or not all(isinstance(item, str) for item in prior_ids):
        raise Blk003LoopExecutionPackageValidationError("prior_consumed_run_ids must be a string list")
    if not isinstance(consumed_ids, list) or not all(isinstance(item, str) for item in consumed_ids):
        raise Blk003LoopExecutionPackageValidationError("consumed_run_ids must be a string list")
    for item in [*prior_ids, *consumed_ids]:
        _require_exact_id(item, "RUN-", "consumed run id")
    if report["run_id"] in prior_ids:
        raise Blk003LoopExecutionPackageValidationError("run_id replay detected in prior ledger evidence")
    if consumed_ids != [*prior_ids, report["run_id"]]:
        raise Blk003LoopExecutionPackageValidationError("consumed_run_ids must append exactly this run_id")
    _reject_laundering(report, "runtime report")
    return _deepcopy(report)


def record_quarantine_bounded_loop_execution_296(
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    *,
    runtime_report: dict[str, Any],
) -> dict[str, Any]:
    """Record one quarantine-contained BLK-003 loop execution report."""

    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight = validate_fresh_execution_preflight_295(
        fresh_preflight_295,
        package,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    if preflight["execution_allowed"] is not True:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight is not ready")
    report = _validate_runtime_report(runtime_report, package)
    record = {
        "status": "QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED",
        "markers": list(_EXECUTION_MARKERS_296),
        "execution_package_hash": package["execution_package_hash"],
        "fresh_preflight_hash": preflight["fresh_preflight_hash"],
        "run_id": report["run_id"],
        "quarantine_workspace_id": report["quarantine_workspace_id"],
        "attempts": report["attempts"],
        "attempt_count": len(report["attempts"]),
        "failure_ceiling": package["failure_ceiling"],
        "final_result": report["final_result"],
        "dispatcher_report_hash": report["dispatcher_report_hash"],
        "result_hash": report["result_hash"],
        "post_execution_target_hash": report["post_execution_target_hash"],
        "target_hash_preserved": report["post_execution_target_hash"] == package["target_hash"],
        "cleanup_evidence_hash": report["cleanup_evidence_hash"],
        "beo_draft_hash": report["beo_draft_hash"],
        "completed_at": report["completed_at"],
        "beo_draft_recorded": True,
        "beo_closeout_execution_performed": False,
        "side_effects": dict(_EXECUTION_SIDE_EFFECTS_296),
    }
    record["execution_record_hash"] = hash_package(record)
    return validate_quarantine_bounded_loop_execution_296(
        record,
        package,
        preflight,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )


def validate_quarantine_bounded_loop_execution_296(
    execution_record: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight = validate_fresh_execution_preflight_295(
        fresh_preflight_295,
        package,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    record = _require_dict(execution_record, "quarantine-bounded loop execution record")
    _require_allowed_keys(record, _EXECUTION_RECORD_KEYS_296, "quarantine-bounded loop execution record")
    if record.get("status") != "QUARANTINE_BOUNDED_BLK003_LOOP_EXECUTION_RECORDED":
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record status mismatch")
    if tuple(record.get("markers", ())) != _EXECUTION_MARKERS_296:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record markers mismatch")
    if record.get("execution_package_hash") != package["execution_package_hash"]:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record package hash mismatch")
    if record.get("fresh_preflight_hash") != preflight["fresh_preflight_hash"]:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record preflight hash mismatch")
    if preflight["execution_allowed"] is not True:
        raise Blk003LoopExecutionPackageValidationError("fresh execution preflight is not ready")
    _require_exact_id(record.get("run_id"), "RUN-", "execution record run_id")
    if record.get("run_id") != package["run_id"]:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record run_id mismatch")
    _require_exact_id(record.get("quarantine_workspace_id"), "QUARANTINE-", "execution record quarantine_workspace_id")
    attempts = _validate_attempts(
        record.get("attempts"),
        package["failure_ceiling"],
        window_start=package["requested_at"],
        window_end=package["expires_at"],
    )
    _validate_final_result(attempts, record.get("final_result"), package["failure_ceiling"])
    if record.get("attempt_count") != len(attempts):
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record attempt_count mismatch")
    if record.get("failure_ceiling") != package["failure_ceiling"]:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record failure ceiling mismatch")
    for field in (
        "dispatcher_report_hash",
        "result_hash",
        "post_execution_target_hash",
        "cleanup_evidence_hash",
        "beo_draft_hash",
    ):
        _require_hash(record.get(field), f"quarantine-bounded loop execution record {field}")
    target_preserved = record["post_execution_target_hash"] == package["target_hash"]
    if record.get("target_hash_preserved") is not target_preserved:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record target hash flag mismatch")
    if not target_preserved:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record target hash was not preserved")
    _require_timestamp_within(record.get("completed_at"), package["requested_at"], package["expires_at"], "completed_at")
    if record.get("beo_draft_recorded") is not True:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record must include BEO draft evidence")
    if record.get("beo_closeout_execution_performed") is not False:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record must not perform BEO closeout execution")
    if record.get("side_effects") != _EXECUTION_SIDE_EFFECTS_296:
        raise Blk003LoopExecutionPackageValidationError("quarantine-bounded loop execution record side_effects mismatch")
    _require_hash_field(record, "execution_record_hash", "quarantine-bounded loop execution record")
    _reject_laundering(record, "quarantine-bounded loop execution record")
    return _deepcopy(record)


def reconcile_exact_loop_execution_package_297(
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile exact loop evidence and name the exact BLK-test frontier."""

    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight = validate_fresh_execution_preflight_295(
        fresh_preflight_295,
        package,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    record = validate_quarantine_bounded_loop_execution_296(
        execution_record_296,
        package,
        preflight,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    reconciliation = {
        "status": "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED",
        "markers": list(_RECONCILIATION_MARKERS_297),
        "execution_package_hash": package["execution_package_hash"],
        "fresh_preflight_hash": preflight["fresh_preflight_hash"],
        "execution_record_hash": record["execution_record_hash"],
        "run_id": record["run_id"],
        "final_result": record["final_result"],
        "result_hash": record["result_hash"],
        "dispatcher_report_hash": record["dispatcher_report_hash"],
        "beo_draft_hash": record["beo_draft_hash"],
        "reconciled_state": "exact_quarantine_gated_loop_execution_recorded_ready_for_blk_test_verification",
        "next_frontier": NEXT_FRONTIER_297,
        "side_effects": dict(_EXECUTION_SIDE_EFFECTS_296),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_exact_loop_execution_reconciliation_297(
        reconciliation,
        package,
        preflight,
        record,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )


def validate_exact_loop_execution_reconciliation_297(
    reconciliation_297: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
) -> dict[str, Any]:
    package = validate_exact_loop_execution_package_294(
        execution_package_294,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    preflight = validate_fresh_execution_preflight_295(
        fresh_preflight_295,
        package,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    record = validate_quarantine_bounded_loop_execution_296(
        execution_record_296,
        package,
        preflight,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    reconciliation = _require_dict(reconciliation_297, "exact loop execution reconciliation")
    _require_allowed_keys(reconciliation, _RECONCILIATION_KEYS_297, "exact loop execution reconciliation")
    if reconciliation.get("status") != "EXACT_QUARANTINE_GATED_BLK003_LOOP_EXECUTION_RECONCILED":
        raise Blk003LoopExecutionPackageValidationError("exact loop execution reconciliation status mismatch")
    if tuple(reconciliation.get("markers", ())) != _RECONCILIATION_MARKERS_297:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution reconciliation markers mismatch")
    expected_pairs = {
        "execution_package_hash": package["execution_package_hash"],
        "fresh_preflight_hash": preflight["fresh_preflight_hash"],
        "execution_record_hash": record["execution_record_hash"],
        "run_id": record["run_id"],
        "final_result": record["final_result"],
        "result_hash": record["result_hash"],
        "dispatcher_report_hash": record["dispatcher_report_hash"],
        "beo_draft_hash": record["beo_draft_hash"],
        "reconciled_state": "exact_quarantine_gated_loop_execution_recorded_ready_for_blk_test_verification",
        "next_frontier": NEXT_FRONTIER_297,
    }
    for field, expected in expected_pairs.items():
        if reconciliation.get(field) != expected:
            raise Blk003LoopExecutionPackageValidationError(f"exact loop execution reconciliation {field} mismatch")
    if reconciliation.get("side_effects") != _EXECUTION_SIDE_EFFECTS_296:
        raise Blk003LoopExecutionPackageValidationError("exact loop execution reconciliation side_effects mismatch")
    _require_hash_field(reconciliation, "reconciliation_hash", "exact loop execution reconciliation")
    _reject_laundering(reconciliation, "exact loop execution reconciliation")
    return _deepcopy(reconciliation)
