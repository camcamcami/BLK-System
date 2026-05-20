"""BLK-SYSTEM-298..301 exact BLK-test oracle verification package.

This module consumes the BLK-SYSTEM-294..297 exact quarantine-gated
BLK-003 loop execution evidence and the existing BLK-SYSTEM-242..246
verifier-only BLK-test oracle semantics. It records one metadata-only
BLK-test oracle verification package while keeping production/generic
BLK-test MCP transport disabled and preserving every adjacent authority
boundary: PASS is evidence, not approval; no planner/dispatcher/source of
truth role; no BEO closeout/publication, RTM, production blk-link,
protected-body access, source/Git mutation, live tooling, or production
isolation claim.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from blk003_quarantine_gated_loop_execution_294_297 import (
    Blk003LoopExecutionPackageValidationError,
    validate_exact_loop_execution_package_294,
    validate_exact_loop_execution_reconciliation_297,
    validate_fresh_execution_preflight_295,
    validate_quarantine_bounded_loop_execution_296,
)


class Blk003LoopOracleVerificationValidationError(ValueError):
    """Raised when exact BLK-test oracle verification evidence is unsafe."""


_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Z]+(?:-[A-Z0-9]+)+$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

NEXT_FRONTIER_301 = "NEXT_FRONTIER_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUIRED_NOT_GRANTED"
_EXPECTED_LEGACY_ORACLE_RECONCILIATION_HASH = (
    "sha256:f82286e8763dbd7abe4011f83dd5f8a732f9bb6393b241b493bd5fb909d701aa"
)

_VERDICTS = ("PASS", "FAIL", "INCONCLUSIVE", "BLOCKED")
_CONTRACT_MARKERS_298 = (
    "BLK_SYSTEM_298_EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY",
    "LOOP_EXECUTION_RECONCILIATION_REVALIDATED_FOR_BLK_TEST",
    "BLK_TEST_PASS_IS_EVIDENCE_NOT_APPROVAL",
)
_PREFLIGHT_MARKERS_299 = (
    "BLK_SYSTEM_299_EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY",
    "LOOP_AND_ORACLE_HASHES_RECHECKED",
    "BLK_TEST_TRANSPORT_REMAINS_DISABLED",
)
_RECORD_MARKERS_300 = (
    "BLK_SYSTEM_300_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED",
    "HASH_BOUND_BLK_TEST_VERDICT_EVIDENCE_ONLY",
    "PASS_DOES_NOT_AUTHORIZE_PUBLICATION_OR_RUNTIME",
)
_RECONCILIATION_MARKERS_301 = (
    "BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED",
    "VERIFIED_LOOP_EVIDENCE_READY_FOR_BEO_REVIEW_REQUEST",
    "NEXT_VERIFIED_LOOP_BEO_REVIEW_REQUIRED_NOT_GRANTED",
)

_VERIFICATION_RULES = {
    "verifier_role": "metadata_only_after_exact_loop_execution",
    "transport_start_allowed": False,
    "pass_is_evidence_not_approval": True,
    "verdict_requires_hash_bound_loop_evidence": True,
    "loop_reconciliation_must_validate_full_chain": True,
    "legacy_oracle_must_be_verifier_only": True,
}

_DENIED_SIDE_EFFECTS = {
    "production_mcp_started": False,
    "generic_mcp_started": False,
    "blk_test_transport_started": False,
    "runtime_tooling_executed": False,
    "planner_dispatcher_authority": False,
    "oracle_source_of_truth_claimed": False,
    "blk_test_pass_as_approval": False,
    "source_git_mutation": False,
    "durable_target_source_git_mutation": False,
    "protected_body_accessed": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "reusable_codex_dispatch": False,
    "broad_blk_pipe_dispatch": False,
    "package_manager_called": False,
    "network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_LEGACY_ORACLE_SIDE_EFFECTS = {
    "production_mcp_started": False,
    "generic_mcp_started": False,
    "reusable_blk_test_service_started": False,
    "runtime_tooling_executed": False,
    "planner_dispatcher_authority": False,
    "source_git_mutation": False,
    "protected_body_accessed": False,
    "beo_publication": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "oracle_source_of_truth_claimed": False,
    "beo_closeout_execution": False,
    "beo_draft_emitted": False,
}

_REQUIRED_VERIFIED_HASHES = (
    "loop_execution_reconciliation_hash",
    "execution_package_hash",
    "fresh_preflight_hash",
    "execution_record_hash",
    "oracle_reconciliation_hash",
    "result_hash",
    "dispatcher_report_hash",
    "beo_draft_hash",
    "cleanup_evidence_hash",
    "target_hash",
)
_VERIFICATION_ASSERTIONS = {
    "loop_reconciliation_revalidated": True,
    "legacy_oracle_reconciled_verifier_only": True,
    "target_hash_preserved": True,
    "beo_draft_hash_present": True,
    "cleanup_evidence_hash_present": True,
    "transport_disabled": True,
    "pass_is_evidence_not_approval": True,
    "source_git_mutation_absent": True,
    "protected_body_access_absent": True,
}

_CONTRACT_KEYS_298 = frozenset(
    {
        "status",
        "markers",
        "contract_id",
        "loop_execution_reconciliation_hash",
        "execution_package_hash",
        "fresh_preflight_hash",
        "execution_record_hash",
        "oracle_reconciliation_hash",
        "run_id",
        "result_hash",
        "dispatcher_report_hash",
        "beo_draft_hash",
        "cleanup_evidence_hash",
        "target_hash",
        "requested_at",
        "expires_at",
        "verification_rules",
        "verdict_vocabulary",
        "required_verified_hashes",
        "side_effects",
        "verification_contract_hash",
    }
)
_PREFLIGHT_KEYS_299 = frozenset(
    {
        "status",
        "markers",
        "verification_contract_hash",
        "loop_execution_reconciliation_hash",
        "observed_loop_reconciliation_hash",
        "loop_reconciliation_hash_rechecked",
        "oracle_reconciliation_hash",
        "observed_oracle_reconciliation_hash",
        "oracle_reconciliation_hash_rechecked",
        "execution_record_hash",
        "observed_execution_record_hash",
        "execution_record_hash_rechecked",
        "transport_state",
        "evaluated_at",
        "preflight_result",
        "verification_ready",
        "mcp_transport_started",
        "runtime_tooling_executed",
        "side_effects",
        "verification_preflight_hash",
    }
)
_REPORT_KEYS = frozenset(
    {
        "record_id",
        "verdict",
        "verified_at",
        "verified_hashes",
        "verification_assertions",
        "operator_notes",
        "denied_side_effects",
    }
)
_RECORD_KEYS_300 = frozenset(
    {
        "status",
        "markers",
        "verification_contract_hash",
        "verification_preflight_hash",
        "loop_execution_reconciliation_hash",
        "execution_record_hash",
        "oracle_reconciliation_hash",
        "record_id",
        "verdict",
        "blk_test_passed",
        "pass_is_approval",
        "verified_at",
        "verified_hashes",
        "verification_assertions",
        "operator_notes",
        "side_effects",
        "verification_record_hash",
    }
)
_RECONCILIATION_KEYS_301 = frozenset(
    {
        "status",
        "markers",
        "verification_contract_hash",
        "verification_preflight_hash",
        "verification_record_hash",
        "verified_loop_reconciliation_hash",
        "verified_execution_record_hash",
        "oracle_reconciliation_hash",
        "verdict",
        "blk_test_passed",
        "pass_is_approval",
        "reconciled_state",
        "next_frontier",
        "side_effects",
        "reconciliation_hash",
    }
)
_LEGACY_ORACLE_KEYS = frozenset(
    {
        "sprint",
        "status",
        "markers",
        "integration_hash",
        "reconciled_state",
        "next_frontier",
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
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be a dictionary")
    return value


def _require_allowed_keys(package: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(package) - allowed)
    if extras:
        raise Blk003LoopOracleVerificationValidationError(f"{context} unsupported field(s): {', '.join(extras)}")
    missing = sorted(allowed - set(package))
    if missing:
        raise Blk003LoopOracleVerificationValidationError(f"{context} missing field(s): {', '.join(missing)}")


def _require_hash(value: Any, context: str) -> None:
    if not isinstance(value, str) or not _HASH_RE.match(value):
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be sha256:<64 lowercase hex>")


def _require_hash_field(package: dict[str, Any], field: str, context: str) -> None:
    _require_hash(package.get(field), f"{context}.{field}")
    expected = hash_package(_without_hash(package, field))
    if package[field] != expected:
        raise Blk003LoopOracleVerificationValidationError(f"{context} hash mismatch for {field}")


def _require_ascii(value: Any, context: str) -> str:
    if not isinstance(value, str) or any(ord(ch) > 127 for ch in value):
        raise Blk003LoopOracleVerificationValidationError(f"{context} must contain ASCII characters only")
    return value


def _reject_laundering(value: Any, context: str) -> None:
    errors = scan_for_authority_laundering(value, path=context)
    if errors:
        raise Blk003LoopOracleVerificationValidationError(
            f"{context} forbidden authority wording: {'; '.join(errors[:4])}"
        )


def _require_exact_id(value: Any, prefix: str, context: str) -> None:
    if not isinstance(value, str):
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be a string")
    _require_ascii(value, context)
    if not value.startswith(prefix) or not _ID_RE.match(value):
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be an exact ID with prefix {prefix}")
    _reject_laundering(value, context)


def _parse_timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP_RE.match(value):
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be an ISO-8601 timestamp with timezone")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be parseable") from exc
    if parsed.tzinfo is None:
        raise Blk003LoopOracleVerificationValidationError(f"{context} must include timezone")
    return parsed


def _require_time_window(start: Any, end: Any, start_name: str, end_name: str) -> None:
    parsed_start = _parse_timestamp(start, start_name)
    parsed_end = _parse_timestamp(end, end_name)
    if parsed_end <= parsed_start:
        raise Blk003LoopOracleVerificationValidationError(f"{end_name} must be after {start_name}")


def _require_timestamp_within(value: Any, start: Any, end: Any, context: str) -> datetime:
    parsed_value = _parse_timestamp(value, context)
    parsed_start = _parse_timestamp(start, "window_start")
    parsed_end = _parse_timestamp(end, "window_end")
    if parsed_value < parsed_start or parsed_value > parsed_end:
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be within verification window")
    return parsed_value


def _require_at_or_after(value: Any, minimum: Any, context: str, minimum_name: str) -> None:
    parsed_value = _parse_timestamp(value, context)
    parsed_minimum = _parse_timestamp(minimum, minimum_name)
    if parsed_value < parsed_minimum:
        raise Blk003LoopOracleVerificationValidationError(f"{context} must be at or after {minimum_name}")


def _side_effects(*, contract=False, preflight=False, record=False, reconciliation=False) -> dict[str, bool]:
    return {
        "verification_contract_prepared": contract,
        "verification_preflight_recorded": preflight,
        "verification_recorded": record,
        "verification_reconciled": reconciliation,
        **_DENIED_SIDE_EFFECTS,
    }


def _expected_verified_hashes(
    contract: dict[str, Any],
    execution_record: dict[str, Any],
    loop_reconciliation: dict[str, Any],
    oracle_reconciliation: dict[str, Any],
) -> dict[str, str]:
    return {
        "loop_execution_reconciliation_hash": loop_reconciliation["reconciliation_hash"],
        "execution_package_hash": contract["execution_package_hash"],
        "fresh_preflight_hash": contract["fresh_preflight_hash"],
        "execution_record_hash": execution_record["execution_record_hash"],
        "oracle_reconciliation_hash": oracle_reconciliation["reconciliation_hash"],
        "result_hash": execution_record["result_hash"],
        "dispatcher_report_hash": execution_record["dispatcher_report_hash"],
        "beo_draft_hash": execution_record["beo_draft_hash"],
        "cleanup_evidence_hash": execution_record["cleanup_evidence_hash"],
        "target_hash": execution_record["post_execution_target_hash"],
    }


def _validate_loop_execution_stack(
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
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
        reconciliation = validate_exact_loop_execution_reconciliation_297(
            loop_execution_reconciliation_297,
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
    except Blk003LoopExecutionPackageValidationError as exc:
        raise Blk003LoopOracleVerificationValidationError(f"loop execution reconciliation invalid: {exc}") from exc
    if record.get("final_result") != "SUCCEEDED" or reconciliation.get("final_result") != "SUCCEEDED":
        raise Blk003LoopOracleVerificationValidationError("loop execution reconciliation must be successful")
    if record.get("target_hash_preserved") is not True:
        raise Blk003LoopOracleVerificationValidationError("loop execution record must preserve target hash")
    if record.get("beo_draft_recorded") is not True:
        raise Blk003LoopOracleVerificationValidationError("loop execution record must include BEO draft evidence")
    return package, preflight, record, reconciliation


def _validate_legacy_oracle_reconciliation(package: dict[str, Any]) -> dict[str, Any]:
    candidate = _require_dict(package, "legacy oracle reconciliation")
    _require_allowed_keys(candidate, _LEGACY_ORACLE_KEYS, "legacy oracle reconciliation")
    if candidate.get("status") != "PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY":
        raise Blk003LoopOracleVerificationValidationError("legacy oracle reconciliation status mismatch")
    if candidate.get("markers") != [
        "BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY",
        "PRODUCTION_BLK_TEST_MCP_TRANSPORT_STILL_NOT_GRANTED",
        "NEXT_FRONTIER_REUSABLE_BEO_PUBLICATION_REQUEST_NOT_GRANTED",
    ]:
        raise Blk003LoopOracleVerificationValidationError("legacy oracle reconciliation markers mismatch")
    if candidate.get("reconciliation_hash") != _EXPECTED_LEGACY_ORACLE_RECONCILIATION_HASH:
        raise Blk003LoopOracleVerificationValidationError("legacy oracle reconciliation canonical hash mismatch")
    _require_hash_field(candidate, "reconciliation_hash", "legacy oracle reconciliation")
    if candidate.get("side_effects") != _LEGACY_ORACLE_SIDE_EFFECTS:
        for key, value in (candidate.get("side_effects") or {}).items():
            if _LEGACY_ORACLE_SIDE_EFFECTS.get(key) is False and value is not False:
                raise Blk003LoopOracleVerificationValidationError(
                    f"legacy oracle reconciliation {key} must remain false"
                )
        raise Blk003LoopOracleVerificationValidationError("legacy oracle reconciliation side_effects mismatch")
    _reject_laundering(candidate, "legacy oracle reconciliation")
    return _deepcopy(candidate)


def build_loop_oracle_verification_contract_298(
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
    *,
    contract_id: str,
    requested_at: str,
    expires_at: str,
) -> dict[str, Any]:
    """Build the exact verifier contract without starting BLK-test MCP transport."""

    package, preflight, record, reconciliation = _validate_loop_execution_stack(
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    oracle = _validate_legacy_oracle_reconciliation(oracle_reconciliation_246)
    _require_exact_id(contract_id, "BLK-TEST-ORACLE-CONTRACT-", "contract_id")
    _require_time_window(requested_at, expires_at, "requested_at", "expires_at")
    _require_at_or_after(requested_at, record["completed_at"], "requested_at", "loop execution completed_at")
    contract = {
        "status": "EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY_NO_TRANSPORT",
        "markers": list(_CONTRACT_MARKERS_298),
        "contract_id": contract_id,
        "loop_execution_reconciliation_hash": reconciliation["reconciliation_hash"],
        "execution_package_hash": package["execution_package_hash"],
        "fresh_preflight_hash": preflight["fresh_preflight_hash"],
        "execution_record_hash": record["execution_record_hash"],
        "oracle_reconciliation_hash": oracle["reconciliation_hash"],
        "run_id": record["run_id"],
        "result_hash": record["result_hash"],
        "dispatcher_report_hash": record["dispatcher_report_hash"],
        "beo_draft_hash": record["beo_draft_hash"],
        "cleanup_evidence_hash": record["cleanup_evidence_hash"],
        "target_hash": record["post_execution_target_hash"],
        "requested_at": requested_at,
        "expires_at": expires_at,
        "verification_rules": dict(_VERIFICATION_RULES),
        "verdict_vocabulary": list(_VERDICTS),
        "required_verified_hashes": list(_REQUIRED_VERIFIED_HASHES),
        "side_effects": _side_effects(contract=True),
    }
    contract["verification_contract_hash"] = hash_package(contract)
    return validate_loop_oracle_verification_contract_298(
        contract,
        package,
        preflight,
        record,
        reconciliation,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle,
    )


def validate_loop_oracle_verification_contract_298(
    verification_contract_298: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
) -> dict[str, Any]:
    package, preflight, record, reconciliation = _validate_loop_execution_stack(
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    oracle = _validate_legacy_oracle_reconciliation(oracle_reconciliation_246)
    contract = _require_dict(verification_contract_298, "verification contract")
    _require_allowed_keys(contract, _CONTRACT_KEYS_298, "verification contract")
    if contract.get("status") != "EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY_NO_TRANSPORT":
        raise Blk003LoopOracleVerificationValidationError("verification contract status mismatch")
    if tuple(contract.get("markers", ())) != _CONTRACT_MARKERS_298:
        raise Blk003LoopOracleVerificationValidationError("verification contract markers mismatch")
    _require_exact_id(contract.get("contract_id"), "BLK-TEST-ORACLE-CONTRACT-", "contract_id")
    expected = {
        "loop_execution_reconciliation_hash": reconciliation["reconciliation_hash"],
        "execution_package_hash": package["execution_package_hash"],
        "fresh_preflight_hash": preflight["fresh_preflight_hash"],
        "execution_record_hash": record["execution_record_hash"],
        "oracle_reconciliation_hash": oracle["reconciliation_hash"],
        "run_id": record["run_id"],
        "result_hash": record["result_hash"],
        "dispatcher_report_hash": record["dispatcher_report_hash"],
        "beo_draft_hash": record["beo_draft_hash"],
        "cleanup_evidence_hash": record["cleanup_evidence_hash"],
        "target_hash": record["post_execution_target_hash"],
    }
    for field, value in expected.items():
        if contract.get(field) != value:
            raise Blk003LoopOracleVerificationValidationError(f"verification contract {field} mismatch")
    _require_time_window(contract.get("requested_at"), contract.get("expires_at"), "requested_at", "expires_at")
    _require_at_or_after(contract["requested_at"], record["completed_at"], "requested_at", "loop execution completed_at")
    if contract.get("verification_rules") != _VERIFICATION_RULES:
        raise Blk003LoopOracleVerificationValidationError("verification contract rules mismatch")
    if contract.get("verdict_vocabulary") != list(_VERDICTS):
        raise Blk003LoopOracleVerificationValidationError("verification contract verdict vocabulary mismatch")
    if contract.get("required_verified_hashes") != list(_REQUIRED_VERIFIED_HASHES):
        raise Blk003LoopOracleVerificationValidationError("verification contract required hash list mismatch")
    if contract.get("side_effects") != _side_effects(contract=True):
        raise Blk003LoopOracleVerificationValidationError("verification contract side_effects mismatch")
    _require_hash_field(contract, "verification_contract_hash", "verification contract")
    _reject_laundering(contract, "verification contract")
    return _deepcopy(contract)


def _resolve_preflight_result(
    contract: dict[str, Any],
    observed_loop_reconciliation_hash: str,
    observed_oracle_reconciliation_hash: str,
    observed_execution_record_hash: str,
    transport_state: str,
) -> str:
    if (
        observed_loop_reconciliation_hash != contract["loop_execution_reconciliation_hash"]
        or observed_execution_record_hash != contract["execution_record_hash"]
    ):
        return "EXACT_BLK_TEST_ORACLE_VERIFICATION_BLOCKED_BY_LOOP_HASH_DRIFT"
    if observed_oracle_reconciliation_hash != contract["oracle_reconciliation_hash"]:
        return "EXACT_BLK_TEST_ORACLE_VERIFICATION_BLOCKED_BY_ORACLE_HASH_DRIFT"
    if transport_state != "BLK_TEST_TRANSPORT_DISABLED_VERIFIER_ONLY":
        return "EXACT_BLK_TEST_ORACLE_VERIFICATION_BLOCKED_BY_TRANSPORT_STATE"
    return "EXACT_BLK_TEST_ORACLE_VERIFICATION_READY"


def build_loop_oracle_verification_preflight_299(
    verification_contract_298: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
    *,
    observed_loop_reconciliation_hash: str,
    observed_oracle_reconciliation_hash: str,
    observed_execution_record_hash: str,
    transport_state: str,
    evaluated_at: str,
) -> dict[str, Any]:
    """Recheck loop/oracle hashes and disabled transport before verdict evidence."""

    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    for field, value in {
        "observed_loop_reconciliation_hash": observed_loop_reconciliation_hash,
        "observed_oracle_reconciliation_hash": observed_oracle_reconciliation_hash,
        "observed_execution_record_hash": observed_execution_record_hash,
    }.items():
        _require_hash(value, field)
    _require_ascii(transport_state, "transport_state")
    _reject_laundering(transport_state, "transport_state")
    _require_timestamp_within(evaluated_at, contract["requested_at"], contract["expires_at"], "evaluated_at")
    result = _resolve_preflight_result(
        contract,
        observed_loop_reconciliation_hash,
        observed_oracle_reconciliation_hash,
        observed_execution_record_hash,
        transport_state,
    )
    preflight = {
        "status": "EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY",
        "markers": list(_PREFLIGHT_MARKERS_299),
        "verification_contract_hash": contract["verification_contract_hash"],
        "loop_execution_reconciliation_hash": contract["loop_execution_reconciliation_hash"],
        "observed_loop_reconciliation_hash": observed_loop_reconciliation_hash,
        "loop_reconciliation_hash_rechecked": observed_loop_reconciliation_hash == contract["loop_execution_reconciliation_hash"],
        "oracle_reconciliation_hash": contract["oracle_reconciliation_hash"],
        "observed_oracle_reconciliation_hash": observed_oracle_reconciliation_hash,
        "oracle_reconciliation_hash_rechecked": observed_oracle_reconciliation_hash == contract["oracle_reconciliation_hash"],
        "execution_record_hash": contract["execution_record_hash"],
        "observed_execution_record_hash": observed_execution_record_hash,
        "execution_record_hash_rechecked": observed_execution_record_hash == contract["execution_record_hash"],
        "transport_state": transport_state,
        "evaluated_at": evaluated_at,
        "preflight_result": result,
        "verification_ready": result == "EXACT_BLK_TEST_ORACLE_VERIFICATION_READY",
        "mcp_transport_started": False,
        "runtime_tooling_executed": False,
        "side_effects": _side_effects(contract=True, preflight=True),
    }
    preflight["verification_preflight_hash"] = hash_package(preflight)
    return validate_loop_oracle_verification_preflight_299(
        preflight,
        contract,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )


def validate_loop_oracle_verification_preflight_299(
    verification_preflight_299: dict[str, Any],
    verification_contract_298: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    preflight = _require_dict(verification_preflight_299, "verification preflight")
    _require_allowed_keys(preflight, _PREFLIGHT_KEYS_299, "verification preflight")
    if preflight.get("status") != "EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY":
        raise Blk003LoopOracleVerificationValidationError("verification preflight status mismatch")
    if tuple(preflight.get("markers", ())) != _PREFLIGHT_MARKERS_299:
        raise Blk003LoopOracleVerificationValidationError("verification preflight markers mismatch")
    if preflight.get("verification_contract_hash") != contract["verification_contract_hash"]:
        raise Blk003LoopOracleVerificationValidationError("verification preflight contract hash mismatch")
    for field in (
        "loop_execution_reconciliation_hash",
        "observed_loop_reconciliation_hash",
        "oracle_reconciliation_hash",
        "observed_oracle_reconciliation_hash",
        "execution_record_hash",
        "observed_execution_record_hash",
    ):
        _require_hash(preflight.get(field), f"verification preflight {field}")
    expected_result = _resolve_preflight_result(
        contract,
        preflight["observed_loop_reconciliation_hash"],
        preflight["observed_oracle_reconciliation_hash"],
        preflight["observed_execution_record_hash"],
        preflight["transport_state"],
    )
    if preflight.get("preflight_result") != expected_result:
        raise Blk003LoopOracleVerificationValidationError("verification preflight result mismatch")
    expected_flags = {
        "loop_reconciliation_hash_rechecked": (
            preflight["observed_loop_reconciliation_hash"] == contract["loop_execution_reconciliation_hash"]
        ),
        "oracle_reconciliation_hash_rechecked": (
            preflight["observed_oracle_reconciliation_hash"] == contract["oracle_reconciliation_hash"]
        ),
        "execution_record_hash_rechecked": preflight["observed_execution_record_hash"] == contract["execution_record_hash"],
        "verification_ready": expected_result == "EXACT_BLK_TEST_ORACLE_VERIFICATION_READY",
    }
    for field, expected in expected_flags.items():
        if preflight.get(field) is not expected:
            raise Blk003LoopOracleVerificationValidationError(f"verification preflight {field} mismatch")
    if preflight.get("mcp_transport_started") is not False:
        raise Blk003LoopOracleVerificationValidationError("verification preflight must not start MCP transport")
    if preflight.get("runtime_tooling_executed") is not False:
        raise Blk003LoopOracleVerificationValidationError("verification preflight must not execute runtime tooling")
    _require_timestamp_within(preflight.get("evaluated_at"), contract["requested_at"], contract["expires_at"], "evaluated_at")
    if preflight.get("side_effects") != _side_effects(contract=True, preflight=True):
        raise Blk003LoopOracleVerificationValidationError("verification preflight side_effects mismatch")
    _require_hash_field(preflight, "verification_preflight_hash", "verification preflight")
    _reject_laundering(preflight, "verification preflight")
    return _deepcopy(preflight)


def sample_loop_oracle_verification_report(
    verification_contract_298: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
    *,
    verified_at: str,
    verdict: str = "PASS",
) -> dict[str, Any]:
    """Return one safe metadata-only BLK-test oracle report for tests/docs."""

    if verdict not in _VERDICTS:
        raise Blk003LoopOracleVerificationValidationError("verdict must use closed vocabulary")
    return {
        "record_id": "BLK-TEST-ORACLE-VERIFICATION-BLK-SYSTEM-300-001",
        "verdict": verdict,
        "verified_at": verified_at,
        "verified_hashes": _expected_verified_hashes(
            verification_contract_298,
            execution_record_296,
            loop_execution_reconciliation_297,
            oracle_reconciliation_246,
        ),
        "verification_assertions": dict(_VERIFICATION_ASSERTIONS),
        "operator_notes": "metadata-only loop verification evidence; transport disabled; no mutation",
        "denied_side_effects": dict(_DENIED_SIDE_EFFECTS),
    }


def _validate_oracle_report(
    oracle_report: dict[str, Any],
    contract: dict[str, Any],
    preflight: dict[str, Any],
    execution_record: dict[str, Any],
    loop_reconciliation: dict[str, Any],
    oracle_reconciliation: dict[str, Any],
) -> dict[str, Any]:
    report = _require_dict(oracle_report, "oracle report")
    _require_allowed_keys(report, _REPORT_KEYS, "oracle report")
    _require_exact_id(report.get("record_id"), "BLK-TEST-ORACLE-VERIFICATION-", "oracle report record_id")
    if report.get("verdict") not in _VERDICTS:
        raise Blk003LoopOracleVerificationValidationError("oracle report verdict must use closed vocabulary")
    _require_timestamp_within(report.get("verified_at"), contract["requested_at"], contract["expires_at"], "verified_at")
    _require_at_or_after(report["verified_at"], execution_record["completed_at"], "verified_at", "loop execution completed_at")
    verified_hashes = _require_dict(report.get("verified_hashes"), "oracle report verified_hashes")
    if tuple(verified_hashes) != _REQUIRED_VERIFIED_HASHES:
        raise Blk003LoopOracleVerificationValidationError("oracle report verified_hashes key order or set mismatch")
    expected_hashes = _expected_verified_hashes(contract, execution_record, loop_reconciliation, oracle_reconciliation)
    for field, expected in expected_hashes.items():
        if verified_hashes.get(field) != expected:
            raise Blk003LoopOracleVerificationValidationError(f"oracle report verified hash {field} mismatch")
        _require_hash(verified_hashes[field], f"oracle report verified_hashes.{field}")
    if report.get("verification_assertions") != _VERIFICATION_ASSERTIONS:
        raise Blk003LoopOracleVerificationValidationError("oracle report verification_assertions mismatch")
    if report.get("denied_side_effects") != _DENIED_SIDE_EFFECTS:
        for key, value in (report.get("denied_side_effects") or {}).items():
            if _DENIED_SIDE_EFFECTS.get(key) is False and value is not False:
                raise Blk003LoopOracleVerificationValidationError(
                    f"oracle report denied_side_effects {key} must remain false"
                )
        raise Blk003LoopOracleVerificationValidationError("oracle report denied_side_effects mismatch")
    notes = report.get("operator_notes")
    if not isinstance(notes, str) or len(notes) > 240:
        raise Blk003LoopOracleVerificationValidationError("oracle report operator_notes must be a short string")
    compact_notes = re.sub(r"[^a-z0-9]+", "", notes.casefold())
    dangerous_notes = (
        "passapproves",
        "passauthorizes",
        "passgrants",
        "approvesbeopublication",
        "approvedforpublication",
        "beopublicationauthorized",
        "productionblklink",
        "runtimeapproved",
    )
    if any(token in compact_notes for token in dangerous_notes):
        raise Blk003LoopOracleVerificationValidationError(
            "oracle report forbidden authority wording: PASS/verdict text must not imply approval"
        )
    _reject_laundering(report, "oracle report")
    if preflight.get("verification_ready") is not True:
        raise Blk003LoopOracleVerificationValidationError("oracle report requires ready verification preflight")
    return _deepcopy(report)


def record_loop_oracle_verification_300(
    verification_contract_298: dict[str, Any],
    verification_preflight_299: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
    *,
    oracle_report: dict[str, Any],
) -> dict[str, Any]:
    """Record one metadata-only BLK-test verdict over exact loop evidence."""

    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    preflight = validate_loop_oracle_verification_preflight_299(
        verification_preflight_299,
        contract,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    package, _fresh, record, reconciliation = _validate_loop_execution_stack(
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    oracle = _validate_legacy_oracle_reconciliation(oracle_reconciliation_246)
    report = _validate_oracle_report(oracle_report, contract, preflight, record, reconciliation, oracle)
    verification_record = {
        "status": "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED",
        "markers": list(_RECORD_MARKERS_300),
        "verification_contract_hash": contract["verification_contract_hash"],
        "verification_preflight_hash": preflight["verification_preflight_hash"],
        "loop_execution_reconciliation_hash": reconciliation["reconciliation_hash"],
        "execution_record_hash": record["execution_record_hash"],
        "oracle_reconciliation_hash": oracle["reconciliation_hash"],
        "record_id": report["record_id"],
        "verdict": report["verdict"],
        "blk_test_passed": report["verdict"] == "PASS",
        "pass_is_approval": False,
        "verified_at": report["verified_at"],
        "verified_hashes": report["verified_hashes"],
        "verification_assertions": report["verification_assertions"],
        "operator_notes": report["operator_notes"],
        "side_effects": _side_effects(contract=True, preflight=True, record=True),
    }
    # Keep package referenced so local linters know the exact package was revalidated.
    if verification_record["verified_hashes"]["execution_package_hash"] != package["execution_package_hash"]:
        raise Blk003LoopOracleVerificationValidationError("verification record execution package hash mismatch")
    verification_record["verification_record_hash"] = hash_package(verification_record)
    return validate_loop_oracle_verification_record_300(
        verification_record,
        contract,
        preflight,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle,
    )


def validate_loop_oracle_verification_record_300(
    verification_record_300: dict[str, Any],
    verification_contract_298: dict[str, Any],
    verification_preflight_299: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    preflight = validate_loop_oracle_verification_preflight_299(
        verification_preflight_299,
        contract,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    _package, _fresh, execution_record, reconciliation = _validate_loop_execution_stack(
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
    )
    oracle = _validate_legacy_oracle_reconciliation(oracle_reconciliation_246)
    record = _require_dict(verification_record_300, "verification record")
    _require_allowed_keys(record, _RECORD_KEYS_300, "verification record")
    if record.get("status") != "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED":
        raise Blk003LoopOracleVerificationValidationError("verification record status mismatch")
    if tuple(record.get("markers", ())) != _RECORD_MARKERS_300:
        raise Blk003LoopOracleVerificationValidationError("verification record markers mismatch")
    expected = {
        "verification_contract_hash": contract["verification_contract_hash"],
        "verification_preflight_hash": preflight["verification_preflight_hash"],
        "loop_execution_reconciliation_hash": reconciliation["reconciliation_hash"],
        "execution_record_hash": execution_record["execution_record_hash"],
        "oracle_reconciliation_hash": oracle["reconciliation_hash"],
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise Blk003LoopOracleVerificationValidationError(f"verification record {field} mismatch")
    _require_exact_id(record.get("record_id"), "BLK-TEST-ORACLE-VERIFICATION-", "verification record record_id")
    if record.get("verdict") not in _VERDICTS:
        raise Blk003LoopOracleVerificationValidationError("verification record verdict must use closed vocabulary")
    if record.get("blk_test_passed") is not (record["verdict"] == "PASS"):
        raise Blk003LoopOracleVerificationValidationError("verification record blk_test_passed mismatch")
    if record.get("pass_is_approval") is not False:
        raise Blk003LoopOracleVerificationValidationError("verification record PASS must not be approval")
    _require_timestamp_within(record.get("verified_at"), contract["requested_at"], contract["expires_at"], "verified_at")
    verified_hashes = _require_dict(record.get("verified_hashes"), "verification record verified_hashes")
    if tuple(verified_hashes) != _REQUIRED_VERIFIED_HASHES:
        raise Blk003LoopOracleVerificationValidationError("verification record verified_hashes key order or set mismatch")
    expected_hashes = _expected_verified_hashes(contract, execution_record, reconciliation, oracle)
    for field, value in expected_hashes.items():
        if verified_hashes.get(field) != value:
            raise Blk003LoopOracleVerificationValidationError(f"verification record verified hash {field} mismatch")
    if record.get("verification_assertions") != _VERIFICATION_ASSERTIONS:
        raise Blk003LoopOracleVerificationValidationError("verification record assertions mismatch")
    if record.get("side_effects") != _side_effects(contract=True, preflight=True, record=True):
        raise Blk003LoopOracleVerificationValidationError("verification record side_effects mismatch")
    _require_hash_field(record, "verification_record_hash", "verification record")
    _reject_laundering(record, "verification record")
    return _deepcopy(record)


def reconcile_loop_oracle_verification_301(
    verification_contract_298: dict[str, Any],
    verification_preflight_299: dict[str, Any],
    verification_record_300: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile exact BLK-test oracle verification and name the next frontier."""

    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    preflight = validate_loop_oracle_verification_preflight_299(
        verification_preflight_299,
        contract,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    record = validate_loop_oracle_verification_record_300(
        verification_record_300,
        contract,
        preflight,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    reconciliation = {
        "status": "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED_VERIFIER_ONLY",
        "markers": list(_RECONCILIATION_MARKERS_301),
        "verification_contract_hash": contract["verification_contract_hash"],
        "verification_preflight_hash": preflight["verification_preflight_hash"],
        "verification_record_hash": record["verification_record_hash"],
        "verified_loop_reconciliation_hash": record["loop_execution_reconciliation_hash"],
        "verified_execution_record_hash": record["execution_record_hash"],
        "oracle_reconciliation_hash": record["oracle_reconciliation_hash"],
        "verdict": record["verdict"],
        "blk_test_passed": record["blk_test_passed"],
        "pass_is_approval": False,
        "reconciled_state": "exact_loop_execution_verified_by_blk_test_oracle_evidence_only",
        "next_frontier": NEXT_FRONTIER_301,
        "side_effects": _side_effects(contract=True, preflight=True, record=True, reconciliation=True),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_loop_oracle_verification_reconciliation_301(
        reconciliation,
        contract,
        preflight,
        record,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )


def validate_loop_oracle_verification_reconciliation_301(
    reconciliation_301: dict[str, Any],
    verification_contract_298: dict[str, Any],
    verification_preflight_299: dict[str, Any],
    verification_record_300: dict[str, Any],
    execution_package_294: dict[str, Any],
    fresh_preflight_295: dict[str, Any],
    execution_record_296: dict[str, Any],
    loop_execution_reconciliation_297: dict[str, Any],
    loop_request_contract: dict[str, Any],
    route_request_binding: dict[str, Any],
    request_path_preflight: dict[str, Any],
    request_path_reconciliation: dict[str, Any],
    approval_timing_contract: dict[str, Any],
    quarantine: dict[str, Any],
    hitl_interaction: dict[str, Any],
    promotion_or_purge_gate: dict[str, Any],
    oracle_reconciliation_246: dict[str, Any],
) -> dict[str, Any]:
    contract = validate_loop_oracle_verification_contract_298(
        verification_contract_298,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    preflight = validate_loop_oracle_verification_preflight_299(
        verification_preflight_299,
        contract,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    record = validate_loop_oracle_verification_record_300(
        verification_record_300,
        contract,
        preflight,
        execution_package_294,
        fresh_preflight_295,
        execution_record_296,
        loop_execution_reconciliation_297,
        loop_request_contract,
        route_request_binding,
        request_path_preflight,
        request_path_reconciliation,
        approval_timing_contract,
        quarantine,
        hitl_interaction,
        promotion_or_purge_gate,
        oracle_reconciliation_246,
    )
    reconciliation = _require_dict(reconciliation_301, "verification reconciliation")
    _require_allowed_keys(reconciliation, _RECONCILIATION_KEYS_301, "verification reconciliation")
    if reconciliation.get("status") != "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED_VERIFIER_ONLY":
        raise Blk003LoopOracleVerificationValidationError("verification reconciliation status mismatch")
    if tuple(reconciliation.get("markers", ())) != _RECONCILIATION_MARKERS_301:
        raise Blk003LoopOracleVerificationValidationError("verification reconciliation markers mismatch")
    expected = {
        "verification_contract_hash": contract["verification_contract_hash"],
        "verification_preflight_hash": preflight["verification_preflight_hash"],
        "verification_record_hash": record["verification_record_hash"],
        "verified_loop_reconciliation_hash": record["loop_execution_reconciliation_hash"],
        "verified_execution_record_hash": record["execution_record_hash"],
        "oracle_reconciliation_hash": record["oracle_reconciliation_hash"],
        "verdict": record["verdict"],
        "blk_test_passed": record["blk_test_passed"],
        "pass_is_approval": False,
        "reconciled_state": "exact_loop_execution_verified_by_blk_test_oracle_evidence_only",
        "next_frontier": NEXT_FRONTIER_301,
    }
    for field, value in expected.items():
        if reconciliation.get(field) != value:
            raise Blk003LoopOracleVerificationValidationError(f"verification reconciliation {field} mismatch")
    if reconciliation.get("side_effects") != _side_effects(contract=True, preflight=True, record=True, reconciliation=True):
        raise Blk003LoopOracleVerificationValidationError("verification reconciliation side_effects mismatch")
    _require_hash_field(reconciliation, "reconciliation_hash", "verification reconciliation")
    _reject_laundering(reconciliation, "verification reconciliation")
    return _deepcopy(reconciliation)
