"""BLK-SYSTEM-242..246 production BLK-test MCP oracle ladder.

The ladder scopes verifier-only oracle semantics after the BLK-SYSTEM-241
non-runtime loop kernel.  It deliberately does not start MCP transport, run
BLK-test, dispatch BLK-pipe/Codex, mutate target repos, publish BEOs, generate
RTM, or grant production/generic BLK-test MCP authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


class OracleValidationError(ValueError):
    """Raised when a production BLK-test oracle package is unsafe."""


_VERDICTS = ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"]
_REQUIRED_EVIDENCE_HASHES = (
    "loop_iteration_record_hash",
    "blk_pipe_report_hash",
    "validation_profile_report_hash",
    "target_artifact_hash",
)
_NEXT_FRONTIER = "NEXT_FRONTIER_REUSABLE_BEO_PUBLICATION_REQUEST_NOT_GRANTED"
_EXPECTED_LOOP_KERNEL_HASH = "sha256:c2819a7d995a791dccee0bd7ab368f40ad42296be5b777dc0a6558603728415e"
_EXPECTED_REQUEST_HASH = "sha256:c4de997333a8451278b3c15ab20894ef60185b8056d5eee1d0eac93cfc38dedc"
_EXPECTED_CONTRACT_HASH = "sha256:97c3a01b083225d8d7046679ff8051522dd6aeba680d08231596c5380a267289"

_EXPECTED_LOOP_SIDE_EFFECTS = {
    "loop_runtime_execution": False,
    "beo_closeout_execution": False,
    "reusable_codex_dispatch": False,
    "broad_blk_pipe_dispatch": False,
    "protected_body_access_without_exact_id": False,
    "rtm_generation": False,
    "production_blk_test_mcp": False,
}
_ORACLE_MUST_NOT = [
    "plan work",
    "dispatch BLK-pipe or Codex",
    "mutate source or Git",
    "produce final outcome publication",
    "produce trace matrix output",
    "claim coverage or drift truth",
    "read protected BLK-req bodies",
]
_CONTRACT_RULES = {
    "role": "verifier_only",
    "transport": "not_started",
    "pass_is_not_approval": True,
    "fail_blocks_beo_draft_until_operator_review": True,
    "verdict_requires_hash_bound_inputs": True,
}

_EXPECTED_242_SIDE_EFFECTS = {
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
}
_EXPECTED_243_SIDE_EFFECTS = dict(_EXPECTED_242_SIDE_EFFECTS, oracle_source_of_truth_claimed=False)
_EXPECTED_244_SIDE_EFFECTS = dict(_EXPECTED_243_SIDE_EFFECTS)
_EXPECTED_245_SIDE_EFFECTS = dict(
    _EXPECTED_244_SIDE_EFFECTS,
    beo_closeout_execution=False,
    beo_draft_emitted=False,
)
_EXPECTED_246_SIDE_EFFECTS = dict(_EXPECTED_245_SIDE_EFFECTS)

_ALLOWED_KEYS_242 = {
    "sprint",
    "status",
    "markers",
    "loop_kernel_hash",
    "oracle_scope",
    "required_evidence_inputs",
    "oracle_must_not",
    "side_effects",
    "request_hash",
}
_ALLOWED_KEYS_243 = {
    "sprint",
    "status",
    "markers",
    "request_hash",
    "contract_rules",
    "verdict_vocabulary",
    "required_evidence_inputs",
    "side_effects",
    "contract_hash",
}
_ALLOWED_KEYS_244 = {
    "sprint",
    "status",
    "markers",
    "contract_hash",
    "oracle_record",
    "side_effects",
    "oracle_record_hash",
    "fixture_hash",
}
_ALLOWED_KEYS_245 = {
    "sprint",
    "status",
    "markers",
    "oracle_record_hash",
    "loop_effect",
    "accepted_verdicts",
    "side_effects",
    "integration_hash",
}
_ALLOWED_KEYS_246 = {
    "sprint",
    "status",
    "markers",
    "integration_hash",
    "reconciled_state",
    "next_frontier",
    "side_effects",
    "reconciliation_hash",
}
_ALLOWED_LOOP_KEYS = {
    "sprint",
    "status",
    "markers",
    "gateway_slice_hash",
    "iteration_contract",
    "stop_conditions",
    "side_effects",
    "loop_kernel_hash",
}
_ALLOWED_ORACLE_RECORD_KEYS = {
    "record_id",
    "verdict",
    "evidence_inputs",
    "operator_notes",
    "oracle_limits",
}


def sample_oracle_evidence_inputs() -> dict[str, Any]:
    """Return safe sample metadata for the metadata-only oracle fixture."""

    return {
        "loop_iteration_record_hash": "sha256:" + "1" * 64,
        "blk_pipe_report_hash": "sha256:" + "2" * 64,
        "validation_profile_report_hash": "sha256:" + "3" * 64,
        "target_artifact_hash": "sha256:" + "4" * 64,
        "verdict": "INCONCLUSIVE",
        "operator_notes": "metadata-only verifier fixture; no transport and no mutation",
    }


def build_oracle_request_242(loop_kernel_package: dict[str, Any]) -> dict[str, Any]:
    """Scope the production BLK-test MCP oracle request without granting it."""

    _validate_loop_kernel(loop_kernel_package)
    package = {
        "sprint": "BLK-SYSTEM-242",
        "status": "PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED",
            "VERIFIER_ONLY_ORACLE_AFTER_GOVERNED_LOOP_EXECUTION",
            "PRODUCTION_BLK_TEST_MCP_TRANSPORT_STILL_DISABLED",
        ],
        "loop_kernel_hash": loop_kernel_package["loop_kernel_hash"],
        "oracle_scope": "verifier_only_after_governed_loop_execution",
        "required_evidence_inputs": list(_REQUIRED_EVIDENCE_HASHES),
        "oracle_must_not": list(_ORACLE_MUST_NOT),
        "side_effects": dict(_EXPECTED_242_SIDE_EFFECTS),
    }
    package["request_hash"] = _hash_package(package)
    _validate_242_request(package, loop_kernel_package["loop_kernel_hash"])
    return _deepcopy(package)


def build_oracle_contract_243(request_package: dict[str, Any]) -> dict[str, Any]:
    """Define the verifier-only oracle contract without MCP transport."""

    _validate_242_request(request_package)
    package = {
        "sprint": "BLK-SYSTEM-243",
        "status": "PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY_NO_TRANSPORT",
        "markers": [
            "BLK_SYSTEM_243_PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY",
            "VERDICT_VOCABULARY_CLOSED",
            "NO_ORACLE_SOURCE_OF_TRUTH_CLAIM",
        ],
        "request_hash": request_package["request_hash"],
        "contract_rules": dict(_CONTRACT_RULES),
        "verdict_vocabulary": list(_VERDICTS),
        "required_evidence_inputs": list(_REQUIRED_EVIDENCE_HASHES),
        "side_effects": dict(_EXPECTED_243_SIDE_EFFECTS),
    }
    package["contract_hash"] = _hash_package(package)
    _validate_243_contract(package, request_package["request_hash"])
    return _deepcopy(package)


def build_metadata_only_oracle_fixture_244(
    contract_package: dict[str, Any], evidence_inputs: dict[str, Any]
) -> dict[str, Any]:
    """Build a metadata-only oracle record fixture from caller-supplied hashes."""

    _validate_243_contract(contract_package)
    evidence = _normalize_evidence_inputs(evidence_inputs)
    record = {
        "record_id": "BLK-TEST-ORACLE-FIXTURE-244-001",
        "verdict": evidence["verdict"],
        "evidence_inputs": {key: evidence[key] for key in _REQUIRED_EVIDENCE_HASHES},
        "operator_notes": evidence["operator_notes"],
        "oracle_limits": {
            "metadata_only": True,
            "mcp_transport_started": False,
            "source_of_truth_claimed": False,
            "protected_body_accessed": False,
        },
    }
    package = {
        "sprint": "BLK-SYSTEM-244",
        "status": "METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY",
        "markers": [
            "BLK_SYSTEM_244_METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY",
            "HASH_BOUND_EVIDENCE_INPUTS_ONLY",
            "NO_RUNTIME_BLK_TEST_OR_MCP_TRANSPORT",
        ],
        "contract_hash": contract_package["contract_hash"],
        "oracle_record": record,
        "side_effects": dict(_EXPECTED_244_SIDE_EFFECTS),
    }
    package["oracle_record_hash"] = _hash_package(record)
    package["fixture_hash"] = _hash_package(package)
    _validate_244_fixture(package, contract_package["contract_hash"])
    return _deepcopy(package)


def integrate_oracle_record_245(fixture_package: dict[str, Any]) -> dict[str, Any]:
    """Integrate the oracle record as loop evidence without execution authority."""

    _validate_244_fixture(fixture_package)
    package = {
        "sprint": "BLK-SYSTEM-245",
        "status": "BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY",
        "markers": [
            "BLK_SYSTEM_245_BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY",
            "ORACLE_VERDICT_GATES_BEO_DRAFT_READINESS_ONLY",
            "NO_PLANNER_DISPATCHER_MUTATION_OR_PUBLICATION_AUTHORITY",
        ],
        "oracle_record_hash": fixture_package["oracle_record_hash"],
        "loop_effect": "oracle verdict can gate BEO draft readiness but cannot dispatch, plan, mutate, or publish",
        "accepted_verdicts": list(_VERDICTS),
        "side_effects": dict(_EXPECTED_245_SIDE_EFFECTS),
    }
    package["integration_hash"] = _hash_package(package)
    _validate_245_integration(package, fixture_package["oracle_record_hash"])
    return _deepcopy(package)


def reconcile_oracle_frontier_246(integration_package: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the verifier-only oracle and select the next bounded frontier."""

    _validate_245_integration(integration_package)
    package = {
        "sprint": "BLK-SYSTEM-246",
        "status": "PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY",
        "markers": [
            "BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY",
            "PRODUCTION_BLK_TEST_MCP_TRANSPORT_STILL_NOT_GRANTED",
            _NEXT_FRONTIER,
        ],
        "integration_hash": integration_package["integration_hash"],
        "reconciled_state": "verifier_only_oracle_contract_and_metadata_fixture_ready_no_live_mcp",
        "next_frontier": _NEXT_FRONTIER,
        "side_effects": dict(_EXPECTED_246_SIDE_EFFECTS),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_246_reconciliation(package, integration_package["integration_hash"])
    return _deepcopy(package)


def _validate_loop_kernel(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_LOOP_KEYS, "loop package")
    _require_hash(package, "loop_kernel_hash", "loop package")
    if package.get("loop_kernel_hash") != _EXPECTED_LOOP_KERNEL_HASH:
        raise OracleValidationError("loop package loop_kernel_hash mismatch")
    if package.get("status") != "REUSABLE_BLK003_LOOP_KERNEL_READY":
        raise OracleValidationError("loop package status mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY",
        "ITERATION_STATE_APPROVAL_FAILURE_CEILING_AND_BEO_DRAFT_RULES_READY",
        "NO_LOOP_RUNTIME_EXECUTION_OR_REUSABLE_CODEX_AUTHORITY",
    ]:
        raise OracleValidationError("loop package markers mismatch")
    if package.get("side_effects") != _EXPECTED_LOOP_SIDE_EFFECTS:
        for key, value in (package.get("side_effects") or {}).items():
            if _EXPECTED_LOOP_SIDE_EFFECTS.get(key) is False and value is not False:
                raise OracleValidationError(f"loop package {key} must remain false")
        raise OracleValidationError("loop package side_effects mismatch")
    _reject_laundering(package, "loop package")


def _validate_242_request(package: dict[str, Any], expected_loop_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_242, "request package")
    _require_hash(package, "request_hash", "request package")
    _require_status(package, "PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED_NOT_GRANTED", "request package")
    _require_marker(package, "BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED", "request package")
    _require_side_effects(package, _EXPECTED_242_SIDE_EFFECTS, "request package")
    if package.get("request_hash") != _EXPECTED_REQUEST_HASH:
        raise OracleValidationError("request package request_hash mismatch")
    if expected_loop_hash and package.get("loop_kernel_hash") != expected_loop_hash:
        raise OracleValidationError("request package loop_kernel_hash mismatch")
    if package.get("loop_kernel_hash") != _EXPECTED_LOOP_KERNEL_HASH:
        raise OracleValidationError("request package loop_kernel_hash mismatch")
    if package.get("required_evidence_inputs") != list(_REQUIRED_EVIDENCE_HASHES):
        raise OracleValidationError("request package required_evidence_inputs mismatch")
    if package.get("oracle_must_not") != _ORACLE_MUST_NOT:
        raise OracleValidationError("request package oracle_must_not mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED",
        "VERIFIER_ONLY_ORACLE_AFTER_GOVERNED_LOOP_EXECUTION",
        "PRODUCTION_BLK_TEST_MCP_TRANSPORT_STILL_DISABLED",
    ]:
        raise OracleValidationError("request package markers mismatch")
    if package.get("oracle_scope") != "verifier_only_after_governed_loop_execution":
        raise OracleValidationError("request package oracle_scope mismatch")
    _reject_laundering(package, "request package")


def _validate_243_contract(package: dict[str, Any], expected_request_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_243, "contract package")
    _require_hash(package, "contract_hash", "contract package")
    _require_status(package, "PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY_NO_TRANSPORT", "contract package")
    _require_marker(package, "BLK_SYSTEM_243_PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY", "contract package")
    _require_side_effects(package, _EXPECTED_243_SIDE_EFFECTS, "contract package")
    if package.get("contract_hash") != _EXPECTED_CONTRACT_HASH:
        raise OracleValidationError("contract package contract_hash mismatch")
    if expected_request_hash and package.get("request_hash") != expected_request_hash:
        raise OracleValidationError("contract package request_hash mismatch")
    if package.get("request_hash") != _EXPECTED_REQUEST_HASH:
        raise OracleValidationError("contract package request_hash mismatch")
    if package.get("verdict_vocabulary") != _VERDICTS:
        raise OracleValidationError("contract package verdict_vocabulary mismatch")
    rules = package.get("contract_rules")
    if rules != _CONTRACT_RULES:
        raise OracleValidationError("contract package contract_rules mismatch")
    _reject_laundering(package, "contract package")


def _validate_244_fixture(package: dict[str, Any], expected_contract_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_244, "fixture package")
    _require_hash(package, "fixture_hash", "fixture package")
    if not _is_hash(package.get("oracle_record_hash")):
        raise OracleValidationError("fixture package oracle_record_hash missing")
    _require_status(package, "METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY", "fixture package")
    _require_marker(package, "BLK_SYSTEM_244_METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY", "fixture package")
    _require_side_effects(package, _EXPECTED_244_SIDE_EFFECTS, "fixture package")
    if expected_contract_hash and package.get("contract_hash") != expected_contract_hash:
        raise OracleValidationError("fixture package contract_hash mismatch")
    record = package.get("oracle_record")
    if not isinstance(record, dict):
        raise OracleValidationError("fixture package oracle_record must be a dictionary")
    _require_allowed_keys(record, _ALLOWED_ORACLE_RECORD_KEYS, "oracle record")
    if _hash_package(record) != package.get("oracle_record_hash"):
        raise OracleValidationError("fixture package oracle_record_hash mismatch")
    evidence = record.get("evidence_inputs")
    if not isinstance(evidence, dict):
        raise OracleValidationError("fixture package evidence_inputs must be a dictionary")
    if set(evidence) != set(_REQUIRED_EVIDENCE_HASHES):
        raise OracleValidationError("fixture package evidence_inputs unsupported field or missing required hash")
    for key in _REQUIRED_EVIDENCE_HASHES:
        if not _is_hash(evidence.get(key)):
            raise OracleValidationError(f"fixture package evidence_inputs {key} must be canonical sha256")
    if record.get("verdict") not in _VERDICTS:
        raise OracleValidationError("fixture package verdict must be closed vocabulary")
    limits = record.get("oracle_limits")
    if not isinstance(limits, dict) or limits != {
        "metadata_only": True,
        "mcp_transport_started": False,
        "source_of_truth_claimed": False,
        "protected_body_accessed": False,
    }:
        raise OracleValidationError("fixture package oracle_limits mismatch")
    _reject_laundering(package, "fixture package")


def _validate_245_integration(package: dict[str, Any], expected_record_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_245, "integration package")
    _require_hash(package, "integration_hash", "integration package")
    _require_status(package, "BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY", "integration package")
    _require_marker(package, "BLK_SYSTEM_245_BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY", "integration package")
    _require_side_effects(package, _EXPECTED_245_SIDE_EFFECTS, "integration package")
    if expected_record_hash and package.get("oracle_record_hash") != expected_record_hash:
        raise OracleValidationError("integration package oracle_record_hash mismatch")
    if package.get("accepted_verdicts") != _VERDICTS:
        raise OracleValidationError("integration package accepted_verdicts mismatch")
    _reject_laundering(package, "integration package")


def _validate_246_reconciliation(package: dict[str, Any], expected_integration_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_246, "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    _require_status(package, "PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY", "reconciliation package")
    _require_marker(package, "BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY", "reconciliation package")
    _require_side_effects(package, _EXPECTED_246_SIDE_EFFECTS, "reconciliation package")
    if expected_integration_hash and package.get("integration_hash") != expected_integration_hash:
        raise OracleValidationError("reconciliation package integration_hash mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise OracleValidationError("reconciliation package next_frontier mismatch")
    _reject_laundering(package, "reconciliation package")


def _normalize_evidence_inputs(evidence_inputs: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(evidence_inputs, dict):
        raise OracleValidationError("evidence inputs must be a dictionary")
    unknown_keys = sorted(set(evidence_inputs) - {*_REQUIRED_EVIDENCE_HASHES, "verdict", "operator_notes"})
    if unknown_keys:
        raise OracleValidationError(f"evidence inputs unsupported field {unknown_keys[0]!r}")
    evidence = _deepcopy(evidence_inputs)
    for key in _REQUIRED_EVIDENCE_HASHES:
        if not _is_hash(evidence.get(key)):
            raise OracleValidationError(f"evidence input {key} must be canonical sha256")
    if evidence.get("verdict") not in _VERDICTS:
        raise OracleValidationError("verdict must be one of PASS, FAIL, INCONCLUSIVE, BLOCKED")
    notes = evidence.get("operator_notes")
    if isinstance(notes, str):
        _reject_laundering(evidence, "evidence inputs")
    if not isinstance(notes, str) or len(notes) > 240:
        raise OracleValidationError("operator_notes must be a short string")
    return evidence


def _require_allowed_keys(package: dict[str, Any], allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise OracleValidationError(f"{label} must be a dictionary")
    extra = sorted(set(package) - allowed)
    if extra:
        raise OracleValidationError(f"{label} unsupported field {extra[0]!r}")


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise OracleValidationError(f"{label} {key} missing")
    expected = _hash_package({k: v for k, v in package.items() if k != key})
    if package[key] != expected:
        raise OracleValidationError(f"{label} {key} mismatch")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise OracleValidationError(f"{label} status mismatch")


def _require_marker(package: dict[str, Any], marker: str, label: str) -> None:
    markers = package.get("markers")
    if not isinstance(markers, list) or marker not in markers:
        raise OracleValidationError(f"{label} marker {marker!r} missing")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], label: str) -> None:
    side_effects = package.get("side_effects")
    if side_effects != expected:
        for key, value in (side_effects or {}).items():
            if expected.get(key) is False and value is not False:
                raise OracleValidationError(f"{label} {key} must remain false")
        raise OracleValidationError(f"{label} side_effects mismatch")


def _reject_laundering(value: Any, label: str) -> None:
    errors = scan_for_authority_laundering(value, path=label)
    if errors:
        raise OracleValidationError(f"{label} forbidden authority wording: {errors[0]}")


def _is_hash(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        return False
    return all(ch in "0123456789abcdef" for ch in value[7:])


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_package(package: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(package).encode("utf-8")).hexdigest()


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
