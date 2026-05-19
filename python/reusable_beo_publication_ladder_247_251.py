"""BLK-SYSTEM-247..251 reusable BEO publication review ladder.

This compact ladder consumes the BLK-SYSTEM-246 verifier-only BLK-test oracle
reconciliation and builds a reusable BEO publication review kernel.  It is
metadata-only and per-run exact-approval oriented: it does not publish a BEO,
sign, write immutable storage, mutate a public ledger, execute rollback,
generate RTM, reject drift, read protected bodies, dispatch BLK-pipe/Codex, run
BLK-test MCP transport, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering


class ReusableBeoPublicationValidationError(ValueError):
    """Raised when a reusable BEO publication review package is unsafe."""


_EXPECTED_ORACLE_RECONCILIATION_HASH = "sha256:f82286e8763dbd7abe4011f83dd5f8a732f9bb6393b241b493bd5fb909d701aa"
_EXPECTED_ORACLE_INTEGRATION_HASH = "sha256:2e0e21e4d73b97cdc2b68dff790b08e992904f2547b50c6fe020bd2f47ed21a9"
_EXPECTED_247_REQUEST_HASH = "sha256:618c44897b37ab57b7a5686975e250be920712661a4d8faca853691f07c7ec97"
_EXPECTED_248_CONTRACT_HASH = "sha256:3b497c69f5519b4f2da3d5dea9fb7381826f7e0bdcb8f4308a8af7329749a66a"
_EXPECTED_249_PILOT_HASH = "sha256:3997db15a2ab37efc453de0333801e1f87b1ed176f289d6cb60e8f06e5d529ec"
_EXPECTED_249_CANDIDATE_RECORD_HASH = "sha256:8d689a781076701ccb0f6872e3c4bce7fed478f90f7b1736fc7f6bb9da1f12af"
_EXPECTED_250_INTEGRATION_HASH = "sha256:aedf2cc2c89245c8f3298abec40ee55439d25c67ad932909116e90466934d158"
_EXPECTED_251_RECONCILIATION_HASH = "sha256:4e2acbff751aae66dda868d1e4e06c56b0f210b624a2affa7e4c658bda25dddd"
_NEXT_FRONTIER = "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED"
_ORACLE_VERDICTS = ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"]
_PUBLICATION_RECORD_STATES = [
    "READY_FOR_OPERATOR_REVIEW",
    "BLOCKED_BY_ORACLE_VERDICT",
    "BLOCKED_PENDING_EXACT_APPROVAL",
]
_REQUIRED_CANDIDATE_HASHES = (
    "beo_draft_hash",
    "beb_l2_package_hash",
    "blk_pipe_report_hash",
    "oracle_record_hash",
    "signature_receipt_hash",
    "storage_receipt_hash",
    "ledger_receipt_hash",
)
_DENIED_AUTHORITIES = [
    "REUSABLE_BEO_PUBLICATION_AUTHORITY_WITHOUT_PER_RUN_EXACT_APPROVAL",
    "BEO_PUBLICATION_FROM_BLK_TEST_PASS_ALONE",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_KEY_MATERIAL_ACCESS_OR_REUSE",
    "IMMUTABLE_STORAGE_WRITE_OR_REUSE",
    "PUBLIC_LEDGER_APPEND_OR_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "PRODUCTION_BLK_LINK",
    "DRIFT_REJECTION",
    "COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BEB_DISPATCH",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
]
_RECORD_ONLY_POLICY = {
    "metadata_only": True,
    "beo_published": False,
    "signer_key_material_accessed": False,
    "cryptographic_signature_generated": False,
    "immutable_storage_written": False,
    "public_ledger_mutated": False,
    "rollback_executed": False,
    "revocation_executed": False,
    "supersession_executed": False,
    "rtm_generated": False,
    "protected_body_accessed": False,
    "target_source_git_mutation": False,
    "blk_pipe_blk_test_codex_runtime": False,
}
_CONTRACT_RULES = {
    "per_run_exact_approval_required": True,
    "blk_test_pass_is_not_publication_approval": True,
    "candidate_requires_oracle_reconciliation_hash": True,
    "candidate_requires_beo_draft_hash": True,
    "record_only_policy_required": True,
    "no_signer_storage_ledger_side_effects": True,
}
_EXPECTED_247_SIDE_EFFECTS = {
    "reusable_beo_publication_authorized": False,
    "future_run_authorized": False,
    "beo_published": False,
    "signer_reuse_authorized": False,
    "storage_reuse_authorized": False,
    "ledger_reuse_authorized": False,
    "rollback_revocation_supersession": False,
    "beo_closeout_execution": False,
    "rtm_generation": False,
    "production_blk_link": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "protected_body_access": False,
    "beb_dispatch": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_EXPECTED_248_SIDE_EFFECTS = dict(_EXPECTED_247_SIDE_EFFECTS)
_EXPECTED_249_SIDE_EFFECTS = dict(_EXPECTED_248_SIDE_EFFECTS, public_ledger_mutated=False, cryptographic_signature_generated=False)
_EXPECTED_250_SIDE_EFFECTS = dict(_EXPECTED_249_SIDE_EFFECTS)
_EXPECTED_251_SIDE_EFFECTS = dict(_EXPECTED_250_SIDE_EFFECTS)

_ALLOWED_KEYS_ORACLE_RECONCILIATION = {
    "sprint",
    "status",
    "markers",
    "integration_hash",
    "reconciled_state",
    "next_frontier",
    "side_effects",
    "reconciliation_hash",
}
_ALLOWED_KEYS_247 = {
    "sprint",
    "status",
    "markers",
    "oracle_reconciliation_hash",
    "publication_scope",
    "required_candidate_inputs",
    "denied_authorities",
    "side_effects",
    "request_hash",
}
_ALLOWED_KEYS_248 = {
    "sprint",
    "status",
    "markers",
    "request_hash",
    "contract_rules",
    "publication_record_states",
    "required_candidate_inputs",
    "record_only_policy",
    "denied_authorities",
    "side_effects",
    "contract_hash",
}
_ALLOWED_KEYS_249 = {
    "sprint",
    "status",
    "markers",
    "contract_hash",
    "candidate_record",
    "side_effects",
    "candidate_record_hash",
    "pilot_hash",
}
_ALLOWED_KEYS_250 = {
    "sprint",
    "status",
    "markers",
    "candidate_record_hash",
    "loop_effect",
    "accepted_record_states",
    "side_effects",
    "integration_hash",
}
_ALLOWED_KEYS_251 = {
    "sprint",
    "status",
    "markers",
    "integration_hash",
    "reconciled_state",
    "next_frontier",
    "side_effects",
    "reconciliation_hash",
}
_ALLOWED_CANDIDATE_RECORD_KEYS = {
    "record_id",
    "beo_id",
    "beb_id",
    "oracle_verdict",
    "publication_record_state",
    "evidence_inputs",
    "receipt_hashes",
    "operator_notes",
    "record_only_policy",
}
_ALLOWED_EVIDENCE_INPUT_KEYS = {
    "beo_draft_hash",
    "beb_l2_package_hash",
    "blk_pipe_report_hash",
    "oracle_record_hash",
}
_ALLOWED_RECEIPT_HASH_KEYS = {
    "signature_receipt_hash",
    "storage_receipt_hash",
    "ledger_receipt_hash",
}


def sample_beo_publication_candidate_inputs() -> dict[str, Any]:
    """Return safe metadata for one exact BEO publication review dry-run."""

    return {
        "beo_id": "BEO-BLK-SYSTEM-249-DRY-RUN-001",
        "beb_id": "BEB-BLK-SYSTEM-249-DRY-RUN-001",
        "beo_draft_hash": "sha256:" + "5" * 64,
        "beb_l2_package_hash": "sha256:" + "6" * 64,
        "blk_pipe_report_hash": "sha256:" + "7" * 64,
        "oracle_record_hash": "sha256:" + "8" * 64,
        "signature_receipt_hash": "sha256:" + "9" * 64,
        "storage_receipt_hash": "sha256:" + "a" * 64,
        "ledger_receipt_hash": "sha256:" + "b" * 64,
        "oracle_verdict": "PASS",
        "operator_notes": "metadata-only review record; no signer, storage, ledger, runtime, mutation, or RTM",
    }


def build_reusable_beo_publication_request_247(oracle_reconciliation_package: dict[str, Any]) -> dict[str, Any]:
    """Scope reusable BEO publication as a request, not a grant."""

    _validate_oracle_reconciliation(oracle_reconciliation_package)
    package = {
        "sprint": "BLK-SYSTEM-247",
        "status": "REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_247_REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED",
            "ORACLE_PASS_IS_NOT_PUBLICATION_APPROVAL",
            "NO_SIGNER_STORAGE_LEDGER_RUN_AUTHORITY",
        ],
        "oracle_reconciliation_hash": oracle_reconciliation_package["reconciliation_hash"],
        "publication_scope": "reusable_beo_publication_review_kernel_request_only",
        "required_candidate_inputs": list(_REQUIRED_CANDIDATE_HASHES),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_EXPECTED_247_SIDE_EFFECTS),
    }
    package["request_hash"] = _hash_package(package)
    _validate_247_request(package)
    return _deepcopy(package)


def build_reusable_beo_publication_contract_248(request_package: dict[str, Any]) -> dict[str, Any]:
    """Define the reusable publication review contract without publishing."""

    _validate_247_request(request_package)
    package = {
        "sprint": "BLK-SYSTEM-248",
        "status": "REUSABLE_BEO_PUBLICATION_CONTRACT_READY_PER_RUN_EXACT_APPROVAL",
        "markers": [
            "BLK_SYSTEM_248_REUSABLE_BEO_PUBLICATION_CONTRACT_READY",
            "PER_RUN_EXACT_APPROVAL_REQUIRED",
            "RECORD_ONLY_POLICY_CLOSED",
        ],
        "request_hash": request_package["request_hash"],
        "contract_rules": dict(_CONTRACT_RULES),
        "publication_record_states": list(_PUBLICATION_RECORD_STATES),
        "required_candidate_inputs": list(_REQUIRED_CANDIDATE_HASHES),
        "record_only_policy": dict(_RECORD_ONLY_POLICY),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_EXPECTED_248_SIDE_EFFECTS),
    }
    package["contract_hash"] = _hash_package(package)
    _validate_248_contract(package, request_package["request_hash"])
    return _deepcopy(package)


def build_exact_beo_publication_dry_run_249(
    contract_package: dict[str, Any], candidate_inputs: dict[str, Any]
) -> dict[str, Any]:
    """Build one exact metadata-only BEO publication review dry-run record."""

    _validate_248_contract(contract_package)
    candidate = _normalize_candidate_inputs(candidate_inputs)
    state = "READY_FOR_OPERATOR_REVIEW" if candidate["oracle_verdict"] == "PASS" else "BLOCKED_BY_ORACLE_VERDICT"
    record = {
        "record_id": "BEO-PUBLICATION-DRY-RUN-249-001",
        "beo_id": candidate["beo_id"],
        "beb_id": candidate["beb_id"],
        "oracle_verdict": candidate["oracle_verdict"],
        "publication_record_state": state,
        "evidence_inputs": {key: candidate[key] for key in _ALLOWED_EVIDENCE_INPUT_KEYS},
        "receipt_hashes": {key: candidate[key] for key in _ALLOWED_RECEIPT_HASH_KEYS},
        "operator_notes": candidate["operator_notes"],
        "record_only_policy": dict(_RECORD_ONLY_POLICY),
    }
    package = {
        "sprint": "BLK-SYSTEM-249",
        "status": "EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY_NOT_PUBLISHED",
        "markers": [
            "BLK_SYSTEM_249_EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY",
            "ONE_EXACT_CANDIDATE_RECORD_ONLY",
            "NO_REAL_SIGNER_STORAGE_LEDGER_SIDE_EFFECTS",
        ],
        "contract_hash": contract_package["contract_hash"],
        "candidate_record": record,
        "side_effects": dict(_EXPECTED_249_SIDE_EFFECTS),
    }
    package["candidate_record_hash"] = _hash_package(record)
    package["pilot_hash"] = _hash_package(package)
    _validate_249_pilot(package, contract_package["contract_hash"])
    return _deepcopy(package)


def integrate_beo_publication_review_250(pilot_package: dict[str, Any]) -> dict[str, Any]:
    """Integrate BEO publication review evidence back into the loop kernel."""

    _validate_249_pilot(pilot_package)
    package = {
        "sprint": "BLK-SYSTEM-250",
        "status": "BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY",
        "markers": [
            "BLK_SYSTEM_250_BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY",
            "BEO_PUBLICATION_REVIEW_AFTER_ORACLE_EVIDENCE_ONLY",
            "NO_RTM_OR_BLK_LINK_TRUTH_PROMOTION",
        ],
        "candidate_record_hash": pilot_package["candidate_record_hash"],
        "loop_effect": "BEO publication candidate can be reviewed after oracle evidence but cannot publish, sign, store, ledger, mutate, or generate RTM",
        "accepted_record_states": list(_PUBLICATION_RECORD_STATES),
        "side_effects": dict(_EXPECTED_250_SIDE_EFFECTS),
    }
    package["integration_hash"] = _hash_package(package)
    _validate_250_integration(package, pilot_package["candidate_record_hash"])
    return _deepcopy(package)


def reconcile_reusable_beo_publication_frontier_251(integration_package: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the reusable BEO publication review kernel and select RTM frontier."""

    _validate_250_integration(integration_package)
    package = {
        "sprint": "BLK-SYSTEM-251",
        "status": "REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY",
        "markers": [
            "BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY",
            "REUSABLE_PUBLICATION_KERNEL_READY_NO_BLANKET_AUTHORITY",
            _NEXT_FRONTIER,
        ],
        "integration_hash": integration_package["integration_hash"],
        "reconciled_state": "reusable_beo_publication_review_kernel_ready_per_run_exact_approval_no_blanket_publication",
        "next_frontier": _NEXT_FRONTIER,
        "side_effects": dict(_EXPECTED_251_SIDE_EFFECTS),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_251_reconciliation(package, integration_package["integration_hash"])
    return _deepcopy(package)


def _validate_oracle_reconciliation(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_ORACLE_RECONCILIATION, "oracle reconciliation")
    _require_hash(package, "reconciliation_hash", "oracle reconciliation")
    if package.get("reconciliation_hash") != _EXPECTED_ORACLE_RECONCILIATION_HASH:
        raise ReusableBeoPublicationValidationError("oracle reconciliation reconciliation_hash mismatch")
    if package.get("integration_hash") != _EXPECTED_ORACLE_INTEGRATION_HASH:
        raise ReusableBeoPublicationValidationError("oracle reconciliation integration_hash mismatch")
    if package.get("status") != "PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY":
        raise ReusableBeoPublicationValidationError("oracle reconciliation status mismatch")
    if package.get("next_frontier") != "NEXT_FRONTIER_REUSABLE_BEO_PUBLICATION_REQUEST_NOT_GRANTED":
        raise ReusableBeoPublicationValidationError("oracle reconciliation next_frontier mismatch")
    _require_side_effects(package, {
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
    }, "oracle reconciliation")
    _reject_laundering(package, "oracle reconciliation")


def _validate_247_request(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_247, "request package")
    _require_hash(package, "request_hash", "request package")
    if package.get("request_hash") != _EXPECTED_247_REQUEST_HASH:
        raise ReusableBeoPublicationValidationError("request package request_hash mismatch")
    _require_status(package, "REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED_NOT_GRANTED", "request package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_247_REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED",
        "ORACLE_PASS_IS_NOT_PUBLICATION_APPROVAL",
        "NO_SIGNER_STORAGE_LEDGER_RUN_AUTHORITY",
    ], "request package")
    if package.get("oracle_reconciliation_hash") != _EXPECTED_ORACLE_RECONCILIATION_HASH:
        raise ReusableBeoPublicationValidationError("request package oracle_reconciliation_hash mismatch")
    if package.get("publication_scope") != "reusable_beo_publication_review_kernel_request_only":
        raise ReusableBeoPublicationValidationError("request package publication_scope mismatch")
    if package.get("required_candidate_inputs") != list(_REQUIRED_CANDIDATE_HASHES):
        raise ReusableBeoPublicationValidationError("request package required_candidate_inputs mismatch")
    _require_exact_denials(package.get("denied_authorities"), "request package")
    _require_side_effects(package, _EXPECTED_247_SIDE_EFFECTS, "request package")
    _reject_laundering(package, "request package")


def _validate_248_contract(package: dict[str, Any], expected_request_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_248, "contract package")
    _require_hash(package, "contract_hash", "contract package")
    if package.get("contract_hash") != _EXPECTED_248_CONTRACT_HASH:
        raise ReusableBeoPublicationValidationError("contract package contract_hash mismatch")
    _require_status(package, "REUSABLE_BEO_PUBLICATION_CONTRACT_READY_PER_RUN_EXACT_APPROVAL", "contract package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_248_REUSABLE_BEO_PUBLICATION_CONTRACT_READY",
        "PER_RUN_EXACT_APPROVAL_REQUIRED",
        "RECORD_ONLY_POLICY_CLOSED",
    ], "contract package")
    if expected_request_hash and package.get("request_hash") != expected_request_hash:
        raise ReusableBeoPublicationValidationError("contract package request_hash mismatch")
    if package.get("request_hash") != _EXPECTED_247_REQUEST_HASH:
        raise ReusableBeoPublicationValidationError("contract package request_hash mismatch")
    if package.get("contract_rules") != _CONTRACT_RULES:
        raise ReusableBeoPublicationValidationError("contract package contract_rules mismatch")
    if package.get("publication_record_states") != _PUBLICATION_RECORD_STATES:
        raise ReusableBeoPublicationValidationError("contract package publication_record_states mismatch")
    if package.get("required_candidate_inputs") != list(_REQUIRED_CANDIDATE_HASHES):
        raise ReusableBeoPublicationValidationError("contract package required_candidate_inputs mismatch")
    if package.get("record_only_policy") != _RECORD_ONLY_POLICY:
        raise ReusableBeoPublicationValidationError("contract package record_only_policy mismatch")
    _require_exact_denials(package.get("denied_authorities"), "contract package")
    _require_side_effects(package, _EXPECTED_248_SIDE_EFFECTS, "contract package")
    _reject_laundering(package, "contract package")


def _validate_249_pilot(package: dict[str, Any], expected_contract_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_249, "pilot package")
    _require_hash(package, "pilot_hash", "pilot package")
    if package.get("pilot_hash") != _EXPECTED_249_PILOT_HASH:
        raise ReusableBeoPublicationValidationError("pilot package pilot_hash mismatch")
    _require_status(package, "EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY_NOT_PUBLISHED", "pilot package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_249_EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY",
        "ONE_EXACT_CANDIDATE_RECORD_ONLY",
        "NO_REAL_SIGNER_STORAGE_LEDGER_SIDE_EFFECTS",
    ], "pilot package")
    if expected_contract_hash and package.get("contract_hash") != expected_contract_hash:
        raise ReusableBeoPublicationValidationError("pilot package contract_hash mismatch")
    if package.get("contract_hash") != _EXPECTED_248_CONTRACT_HASH:
        raise ReusableBeoPublicationValidationError("pilot package contract_hash mismatch")
    _require_side_effects(package, _EXPECTED_249_SIDE_EFFECTS, "pilot package")
    record = package.get("candidate_record")
    if not isinstance(record, dict):
        raise ReusableBeoPublicationValidationError("pilot package candidate_record must be a dictionary")
    _validate_candidate_record(record)
    if not _is_hash(package.get("candidate_record_hash")):
        raise ReusableBeoPublicationValidationError("pilot package candidate_record_hash missing")
    if package.get("candidate_record_hash") != _EXPECTED_249_CANDIDATE_RECORD_HASH:
        raise ReusableBeoPublicationValidationError("pilot package candidate_record_hash mismatch")
    if _hash_package(record) != package.get("candidate_record_hash"):
        raise ReusableBeoPublicationValidationError("pilot package candidate_record_hash mismatch")
    _reject_laundering(package, "pilot package")


def _validate_250_integration(package: dict[str, Any], expected_candidate_record_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_250, "integration package")
    _require_hash(package, "integration_hash", "integration package")
    if package.get("integration_hash") != _EXPECTED_250_INTEGRATION_HASH:
        raise ReusableBeoPublicationValidationError("integration package integration_hash mismatch")
    _require_status(package, "BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY", "integration package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_250_BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY",
        "BEO_PUBLICATION_REVIEW_AFTER_ORACLE_EVIDENCE_ONLY",
        "NO_RTM_OR_BLK_LINK_TRUTH_PROMOTION",
    ], "integration package")
    if expected_candidate_record_hash and package.get("candidate_record_hash") != expected_candidate_record_hash:
        raise ReusableBeoPublicationValidationError("integration package candidate_record_hash mismatch")
    if package.get("candidate_record_hash") != _EXPECTED_249_CANDIDATE_RECORD_HASH:
        raise ReusableBeoPublicationValidationError("integration package candidate_record_hash mismatch")
    if package.get("loop_effect") != "BEO publication candidate can be reviewed after oracle evidence but cannot publish, sign, store, ledger, mutate, or generate RTM":
        raise ReusableBeoPublicationValidationError("integration package loop_effect mismatch")
    if package.get("accepted_record_states") != _PUBLICATION_RECORD_STATES:
        raise ReusableBeoPublicationValidationError("integration package accepted_record_states mismatch")
    _require_side_effects(package, _EXPECTED_250_SIDE_EFFECTS, "integration package")
    _reject_laundering(package, "integration package")


def _validate_251_reconciliation(package: dict[str, Any], expected_integration_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_251, "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    if package.get("reconciliation_hash") != _EXPECTED_251_RECONCILIATION_HASH:
        raise ReusableBeoPublicationValidationError("reconciliation package reconciliation_hash mismatch")
    _require_status(package, "REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY", "reconciliation package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY",
        "REUSABLE_PUBLICATION_KERNEL_READY_NO_BLANKET_AUTHORITY",
        _NEXT_FRONTIER,
    ], "reconciliation package")
    if expected_integration_hash and package.get("integration_hash") != expected_integration_hash:
        raise ReusableBeoPublicationValidationError("reconciliation package integration_hash mismatch")
    if package.get("integration_hash") != _EXPECTED_250_INTEGRATION_HASH:
        raise ReusableBeoPublicationValidationError("reconciliation package integration_hash mismatch")
    if package.get("reconciled_state") != "reusable_beo_publication_review_kernel_ready_per_run_exact_approval_no_blanket_publication":
        raise ReusableBeoPublicationValidationError("reconciliation package reconciled_state mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise ReusableBeoPublicationValidationError("reconciliation package next_frontier mismatch")
    _require_side_effects(package, _EXPECTED_251_SIDE_EFFECTS, "reconciliation package")
    _reject_laundering(package, "reconciliation package")


def _normalize_candidate_inputs(candidate_inputs: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate_inputs, dict):
        raise ReusableBeoPublicationValidationError("candidate inputs must be a dictionary")
    allowed = {
        "beo_id",
        "beb_id",
        "oracle_verdict",
        "operator_notes",
        *_REQUIRED_CANDIDATE_HASHES,
    }
    extra = sorted(set(candidate_inputs) - allowed)
    if extra:
        raise ReusableBeoPublicationValidationError(f"candidate inputs unsupported field {extra[0]!r}")
    candidate = _deepcopy(candidate_inputs)
    for identity_key, prefix in (("beo_id", "BEO-"), ("beb_id", "BEB-")):
        value = candidate.get(identity_key)
        if not isinstance(value, str) or not value.startswith(prefix) or len(value) > 80:
            raise ReusableBeoPublicationValidationError(f"{identity_key} must be an exact short {prefix} identifier")
    for key in _REQUIRED_CANDIDATE_HASHES:
        if not _is_hash(candidate.get(key)):
            raise ReusableBeoPublicationValidationError(f"{key} must be canonical sha256")
    if candidate.get("oracle_verdict") not in _ORACLE_VERDICTS:
        raise ReusableBeoPublicationValidationError("oracle_verdict must be one of PASS, FAIL, INCONCLUSIVE, BLOCKED")
    notes = candidate.get("operator_notes")
    if not isinstance(notes, str) or len(notes) > 240:
        raise ReusableBeoPublicationValidationError("operator_notes must be a short string")
    _reject_laundering(candidate, "candidate inputs")
    return candidate


def _validate_candidate_record(record: dict[str, Any]) -> None:
    _require_allowed_keys(record, _ALLOWED_CANDIDATE_RECORD_KEYS, "candidate record")
    if record.get("record_id") != "BEO-PUBLICATION-DRY-RUN-249-001":
        raise ReusableBeoPublicationValidationError("candidate record record_id mismatch")
    if record.get("oracle_verdict") not in _ORACLE_VERDICTS:
        raise ReusableBeoPublicationValidationError("candidate record oracle_verdict mismatch")
    if record.get("publication_record_state") not in _PUBLICATION_RECORD_STATES:
        raise ReusableBeoPublicationValidationError("candidate record publication_record_state mismatch")
    expected_state = "READY_FOR_OPERATOR_REVIEW" if record.get("oracle_verdict") == "PASS" else "BLOCKED_BY_ORACLE_VERDICT"
    if record.get("publication_record_state") != expected_state:
        raise ReusableBeoPublicationValidationError("candidate record oracle verdict and publication record state mismatch")
    evidence = record.get("evidence_inputs")
    if not isinstance(evidence, dict):
        raise ReusableBeoPublicationValidationError("candidate record evidence_inputs must be a dictionary")
    _require_allowed_keys(evidence, _ALLOWED_EVIDENCE_INPUT_KEYS, "candidate evidence_inputs")
    if set(evidence) != _ALLOWED_EVIDENCE_INPUT_KEYS:
        raise ReusableBeoPublicationValidationError("candidate record evidence_inputs missing required hash")
    receipts = record.get("receipt_hashes")
    if not isinstance(receipts, dict):
        raise ReusableBeoPublicationValidationError("candidate record receipt_hashes must be a dictionary")
    _require_allowed_keys(receipts, _ALLOWED_RECEIPT_HASH_KEYS, "candidate receipt_hashes")
    if set(receipts) != _ALLOWED_RECEIPT_HASH_KEYS:
        raise ReusableBeoPublicationValidationError("candidate record receipt_hashes missing required hash")
    for mapping, label in ((evidence, "evidence_inputs"), (receipts, "receipt_hashes")):
        for key, value in mapping.items():
            if not _is_hash(value):
                raise ReusableBeoPublicationValidationError(f"candidate record {label} {key} must be canonical sha256")
    if record.get("record_only_policy") != _RECORD_ONLY_POLICY:
        raise ReusableBeoPublicationValidationError("candidate record record_only_policy mismatch")
    notes = record.get("operator_notes")
    if not isinstance(notes, str) or len(notes) > 240:
        raise ReusableBeoPublicationValidationError("candidate record operator_notes must be a short string")
    _reject_laundering(record, "candidate record")


def _require_allowed_keys(package: dict[str, Any], allowed: set[str], label: str) -> None:
    if not isinstance(package, dict):
        raise ReusableBeoPublicationValidationError(f"{label} must be a dictionary")
    extra = sorted(set(package) - allowed)
    if extra:
        raise ReusableBeoPublicationValidationError(f"{label} unsupported field {extra[0]!r}")


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise ReusableBeoPublicationValidationError(f"{label} {key} missing")
    expected = _hash_package({k: v for k, v in package.items() if k != key})
    if package[key] != expected:
        raise ReusableBeoPublicationValidationError(f"{label} {key} mismatch")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise ReusableBeoPublicationValidationError(f"{label} status mismatch")


def _require_exact_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise ReusableBeoPublicationValidationError(f"{label} markers mismatch")


def _require_exact_denials(value: Any, label: str) -> None:
    if not isinstance(value, list) or value != _DENIED_AUTHORITIES:
        raise ReusableBeoPublicationValidationError(f"{label} denied_authorities mismatch")
    if len(value) != len(set(value)):
        raise ReusableBeoPublicationValidationError(f"{label} denied_authorities must not contain duplicates")


def _require_side_effects(package: dict[str, Any], expected: dict[str, bool], label: str) -> None:
    side_effects = package.get("side_effects")
    if side_effects != expected:
        for key, value in (side_effects or {}).items():
            if expected.get(key) is False and value is not False:
                raise ReusableBeoPublicationValidationError(f"{label} {key} must remain false")
        raise ReusableBeoPublicationValidationError(f"{label} side_effects mismatch")


def _reject_laundering(value: Any, label: str) -> None:
    errors = scan_for_authority_laundering(value, path=label)
    if errors:
        raise ReusableBeoPublicationValidationError(f"{label} forbidden authority wording: {errors[0]}")


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
