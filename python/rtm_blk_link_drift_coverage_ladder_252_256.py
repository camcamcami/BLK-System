"""BLK-SYSTEM-252..256 RTM / production blk-link drift-coverage ladder.

This compact ladder consumes BLK-SYSTEM-251 reusable BEO publication review
metadata and BLK-SYSTEM-194 repeatable trusted ``blk-link`` metadata. It scopes
RTM / production ``blk-link`` drift and coverage as a metadata-only verifier
request, contract, one exact dry-run, and reconciliation. It does not publish a
BEO, generate RTM, execute production ``blk-link``, reject drift, establish
coverage truth, read protected bodies, dispatch BLK-pipe/Codex/BLK-test runtime,
or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from repeatable_trusted_blk_link_190_194 import (
    CANONICAL_BLK194_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_194,
    EXACT_PROOF_OBLIGATIONS_194,
    RECONCILIATION_PACKAGE_ID_194,
    RECONCILIATION_STATUS_194,
    SIDE_EFFECT_FLAGS_194,
    _validate_package as _validate_blk_link_package,
)
from reusable_beo_publication_ladder_247_251 import _validate_251_reconciliation as _validate_upstream_beo_251


class RtmBlkLinkDriftCoverageValidationError(ValueError):
    """Raised when a drift/coverage package launders authority."""


_EXPECTED_BEO_251_RECONCILIATION_HASH = "sha256:4e2acbff751aae66dda868d1e4e06c56b0f210b624a2affa7e4c658bda25dddd"
_EXPECTED_BEO_250_INTEGRATION_HASH = "sha256:aedf2cc2c89245c8f3298abec40ee55439d25c67ad932909116e90466934d158"
_EXPECTED_BLK_LINK_194_RECONCILIATION_HASH = "sha256:30292f85d1222eb2108f0eadeec07337834e9b47d8e00fa9969aeeafb1bbf4f7"
_EXPECTED_OLD_FRONTIER = "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED"
_NEXT_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED"

_REQUIRED_METADATA_INPUTS = (
    "beo_publication_reconciliation_hash",
    "beo_publication_review_record_hash",
    "blk_link_reconciliation_hash",
    "blk_link_trace_metadata_hash",
    "blk_req_metadata_hash",
    "drift_probe_metadata_hash",
    "coverage_probe_metadata_hash",
)

_DENIED_AUTHORITIES = [
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_EXECUTION_OR_REUSABLE_BLK_LINK_AUTHORITY",
    "DRIFT_REJECTION_OR_DRIFT_TRUTH",
    "COVERAGE_TRUTH_OR_COVERAGE_MATRIX_GENERATION",
    "ACTIVE_VAULT_COMPARISON_OR_FILESYSTEM_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BEO_PUBLICATION_FROM_REVIEW_METADATA",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_REUSE",
    "BLK_TEST_PASS_AS_APPROVAL_OR_TRUTH",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "BEB_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
]

_SIDE_EFFECTS = {
    "approval_captured": False,
    "run_id_reserved": False,
    "run_id_consumed": False,
    "beo_published": False,
    "beo_closeout_execution": False,
    "signer_storage_ledger_reuse": False,
    "rtm_generation": False,
    "reusable_rtm_generation": False,
    "production_blk_link_execution": False,
    "reusable_blk_link_authority": False,
    "drift_rejection": False,
    "drift_truth": False,
    "coverage_truth": False,
    "coverage_matrix_generated": False,
    "active_vault_comparison": False,
    "protected_body_accessed": False,
    "protected_body_read_copy_parse_hash_scan_mutation": False,
    "blk_pipe_blk_test_codex_runtime": False,
    "beb_dispatch": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_RECORD_ONLY_POLICY = {
    "metadata_only": True,
    "authoritative_beo_publication_present": False,
    "rtm_generated": False,
    "production_blk_link_executed": False,
    "drift_rejected": False,
    "drift_truth_established": False,
    "coverage_truth_established": False,
    "coverage_matrix_generated": False,
    "active_vault_compared": False,
    "protected_body_accessed": False,
    "protected_body_content_included": False,
    "target_source_git_mutation": False,
}

_REQUEST_RULES = {
    "authoritative_beo_publication_required_before_truth": True,
    "metadata_only_request": True,
    "exact_future_approval_required": True,
    "no_run_id_reserved_or_consumed": True,
    "protected_body_content_forbidden": True,
}

_CONTRACT_RULES = {
    "metadata_only_inputs_required": True,
    "authoritative_beo_publication_required_before_ready_state": True,
    "per_run_exact_approval_required": True,
    "protected_body_content_forbidden": True,
    "blk_test_pass_is_not_drift_or_coverage_truth": True,
    "production_blk_link_repeatability_is_not_blanket_authority": True,
    "record_only_policy_required": True,
}

_ALLOWED_KEYS_BEO_251 = {
    "sprint", "status", "markers", "integration_hash", "reconciled_state", "next_frontier", "side_effects", "reconciliation_hash"
}
_ALLOWED_KEYS_BLK_LINK_194 = {
    "active_vault_filesystem_read_performed", "active_vault_hash_comparison_performed", "beb_dispatch_authorized",
    "beb_id", "beo_closeout_execution_authorized", "beo_id", "beo_publication_or_signing_authorized",
    "blanket_production_blk_link_authority_granted", "blk_pipe_blk_test_codex_runtime", "coverage_claim_promoted",
    "coverage_matrix_generated", "coverage_truth_established", "cryptographic_signing", "drift_decision_made",
    "exact_trace_identities", "excluded_authorities", "expired", "filesystem_ledger_written", "final_ledger_hash",
    "global_replay_ledger_claimed", "immutable_storage_write", "next_frontier_granted", "observed_failure_requires_hardening",
    "operator_attestation", "operator_identity", "package_network_model_browser_cyber_tooling",
    "production_blk_link_execution_without_per_run_approval", "production_isolation_claim", "proof_obligations",
    "protected_body_content_returned", "protected_body_copy_attempted", "protected_body_hashing_attempted_by_fixture",
    "protected_body_parsing_attempted", "protected_body_reads", "protected_body_scan_attempted", "protected_body_text_included",
    "public_ledger_mutation", "recommended_next_frontier", "reconciled_at", "reconciliation_context_hash",
    "reconciliation_package_hash", "reconciliation_package_id", "reconciliation_scope", "reconciliation_status",
    "repeat_run_count", "repeatable_trusted_blk_link_reconciled_clean", "replayed", "reusable_rtm_generation_authorized",
    "reusable_run_id_authority_granted", "rollback_revocation_supersession_execution", "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed", "rtm_generated", "runtime_rtm_generation_authorized", "selected_frontier",
    "signer_key_material_access", "source_or_git_mutation_by_fixture", "stale", "target_repo_scan_or_mutation",
    "target_source_git_mutation_performed", "trusted_repeatability_result", "trusted_repeatability_score",
    "trusted_repeatable_mechanism_established", "upstream_repeat_runs_package_hash", "upstream_repeat_runs_package_id",
}
_ALLOWED_KEYS_252 = {
    "sprint", "status", "markers", "beo_reconciliation_hash", "blk_link_reconciliation_hash",
    "surface_findings", "required_metadata_inputs", "denied_authorities", "side_effects", "surface_review_hash",
}
_ALLOWED_KEYS_253 = {
    "sprint", "status", "markers", "surface_review_hash", "request_scope", "request_rules",
    "required_metadata_inputs", "denied_authorities", "side_effects", "request_hash",
}
_ALLOWED_KEYS_254 = {
    "sprint", "status", "markers", "request_hash", "contract_rules", "record_only_policy",
    "verifier_record_states", "required_metadata_inputs", "denied_authorities", "side_effects", "contract_hash",
}
_ALLOWED_KEYS_255 = {
    "sprint", "status", "markers", "contract_hash", "verifier_record", "verifier_record_hash", "side_effects", "dry_run_hash",
}
_ALLOWED_KEYS_256 = {
    "sprint", "status", "markers", "dry_run_hash", "reconciled_state", "next_frontier", "side_effects", "reconciliation_hash",
}
_ALLOWED_RECORD_KEYS = {
    "record_id", "record_state", "beo_publication_state", "metadata_inputs", "operator_notes", "record_only_policy",
}
_ALLOWED_INPUT_KEYS = set(_REQUIRED_METADATA_INPUTS) | {"beo_publication_state", "operator_notes", "blk_req_metadata_ref"}
_RECORD_STATES = [
    "BLOCKED_BY_MISSING_AUTHORITATIVE_BEO_METADATA",
    "BLOCKED_BY_UPSTREAM_HASH_MISMATCH",
    "BLOCKED_BY_PROTECTED_BODY_RISK",
    "READY_FOR_OPERATOR_REVIEW_AFTER_EXACT_APPROVAL",
]


def sample_drift_coverage_metadata_inputs() -> dict[str, Any]:
    """Return safe metadata for one exact drift/coverage verifier dry-run."""

    return {
        "beo_publication_reconciliation_hash": _EXPECTED_BEO_251_RECONCILIATION_HASH,
        "beo_publication_review_record_hash": "sha256:" + "1" * 64,
        "blk_link_reconciliation_hash": _EXPECTED_BLK_LINK_194_RECONCILIATION_HASH,
        "blk_link_trace_metadata_hash": "sha256:" + "2" * 64,
        "blk_req_metadata_hash": "sha256:" + "3" * 64,
        "drift_probe_metadata_hash": "sha256:" + "4" * 64,
        "coverage_probe_metadata_hash": "sha256:" + "5" * 64,
        "beo_publication_state": "REVIEW_METADATA_ONLY_NOT_PUBLISHED",
        "blk_req_metadata_ref": "metadata-only BLK-req hashes supplied by caller; no body text or protected path",
        "operator_notes": "metadata-only drift coverage verifier dry-run; blocked until exact BEO publication run exists",
    }


def build_rtm_blk_link_drift_coverage_surface_review_252(beo_reconciliation: dict[str, Any], blk_link_reconciliation: dict[str, Any]) -> dict[str, Any]:
    _validate_beo_251(beo_reconciliation)
    _validate_blk_link_194(blk_link_reconciliation)
    package = {
        "sprint": "BLK-SYSTEM-252",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_COMPLETE_NOT_AUTHORITY",
        "markers": [
            "BLK_SYSTEM_252_RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_READY",
            "BEO_REVIEW_METADATA_IS_NOT_PUBLISHED_BEO",
            "BLK_LINK_REPEATABILITY_IS_PER_RUN_EXACT_APPROVAL_ONLY",
        ],
        "beo_reconciliation_hash": beo_reconciliation["reconciliation_hash"],
        "blk_link_reconciliation_hash": blk_link_reconciliation["reconciliation_package_hash"],
        "surface_findings": [
            "RTM/blk-link drift coverage can consume metadata hashes only after exact BEO publication exists",
            "BLK-test PASS, BEO review metadata, and repeatable blk-link readiness do not create truth authority",
        ],
        "required_metadata_inputs": list(_REQUIRED_METADATA_INPUTS),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["surface_review_hash"] = _hash_package(package)
    _validate_252_review(package)
    return _deepcopy(package)


def build_rtm_blk_link_drift_coverage_request_253(review_package: dict[str, Any]) -> dict[str, Any]:
    _validate_252_review(review_package)
    package = {
        "sprint": "BLK-SYSTEM-253",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED_NOT_GRANTED",
        "markers": [
            "BLK_SYSTEM_253_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED",
            "REQUEST_ONLY_NO_APPROVAL_OR_RUN_ID",
            "PROTECTED_BODY_FREE_METADATA_REQUIRED",
        ],
        "surface_review_hash": review_package["surface_review_hash"],
        "request_scope": "request future exact metadata-only drift coverage verifier after real BEO publication evidence exists",
        "request_rules": dict(_REQUEST_RULES),
        "required_metadata_inputs": list(_REQUIRED_METADATA_INPUTS),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["request_hash"] = _hash_package(package)
    _validate_253_request(package, review_package["surface_review_hash"])
    return _deepcopy(package)


def build_drift_coverage_verifier_contract_254(request_package: dict[str, Any]) -> dict[str, Any]:
    _validate_253_request(request_package)
    package = {
        "sprint": "BLK-SYSTEM-254",
        "status": "DRIFT_COVERAGE_VERIFIER_CONTRACT_READY_PER_RUN_EXACT_APPROVAL",
        "markers": [
            "BLK_SYSTEM_254_DRIFT_COVERAGE_VERIFIER_CONTRACT_READY",
            "METADATA_ONLY_VERIFIER_CONTRACT",
            "NO_TRUTH_PROMOTION_WITHOUT_EXACT_PUBLICATION_APPROVAL",
        ],
        "request_hash": request_package["request_hash"],
        "contract_rules": dict(_CONTRACT_RULES),
        "record_only_policy": dict(_RECORD_ONLY_POLICY),
        "verifier_record_states": list(_RECORD_STATES),
        "required_metadata_inputs": list(_REQUIRED_METADATA_INPUTS),
        "denied_authorities": list(_DENIED_AUTHORITIES),
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["contract_hash"] = _hash_package(package)
    _validate_254_contract(package, request_package["request_hash"])
    return _deepcopy(package)


def build_exact_metadata_only_drift_coverage_dry_run_255(contract_package: dict[str, Any], metadata_inputs: dict[str, Any]) -> dict[str, Any]:
    _validate_254_contract(contract_package)
    inputs = _normalize_metadata_inputs(metadata_inputs)
    state = (
        "READY_FOR_OPERATOR_REVIEW_AFTER_EXACT_APPROVAL"
        if inputs["beo_publication_state"] == "AUTHORITATIVE_BEO_PUBLICATION_METADATA_PRESENT"
        else "BLOCKED_BY_MISSING_AUTHORITATIVE_BEO_METADATA"
    )
    status = (
        "EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_READY_FOR_OPERATOR_REVIEW"
        if state == "READY_FOR_OPERATOR_REVIEW_AFTER_EXACT_APPROVAL"
        else "EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_BLOCKED_BY_UNPUBLISHED_BEO"
    )
    record = {
        "record_id": "RTM-BLK-LINK-DRIFT-COVERAGE-DRY-RUN-255-001",
        "record_state": state,
        "beo_publication_state": inputs["beo_publication_state"],
        "metadata_inputs": {key: inputs[key] for key in _REQUIRED_METADATA_INPUTS},
        "operator_notes": inputs["operator_notes"],
        "record_only_policy": dict(_RECORD_ONLY_POLICY),
    }
    package = {
        "sprint": "BLK-SYSTEM-255",
        "status": status,
        "markers": [
            "BLK_SYSTEM_255_EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_RECORDED",
            "BEO_PUBLICATION_REQUIRED_BEFORE_TRUTH",
            "NO_PROTECTED_BODY_OR_PRODUCTION_BLK_LINK_EXECUTION",
        ],
        "contract_hash": contract_package["contract_hash"],
        "verifier_record": record,
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["verifier_record_hash"] = _hash_package(record)
    package["dry_run_hash"] = _hash_package(package)
    _validate_255_dry_run(package, contract_package["contract_hash"])
    return _deepcopy(package)


def reconcile_drift_coverage_frontier_256(dry_run_package: dict[str, Any]) -> dict[str, Any]:
    _validate_255_dry_run(dry_run_package)
    package = {
        "sprint": "BLK-SYSTEM-256",
        "status": "RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED_BEO_PUBLICATION_REQUIRED",
        "markers": [
            "BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED",
            "BEO_PUBLICATION_RUN_SELECTED_AS_NEXT_REQUIRED_FRONTIER",
            _NEXT_FRONTIER,
        ],
        "dry_run_hash": dry_run_package["dry_run_hash"],
        "reconciled_state": "metadata_only_verifier_ready_but_blocked_until_exact_beo_publication_run_evidence_exists",
        "next_frontier": _NEXT_FRONTIER,
        "side_effects": dict(_SIDE_EFFECTS),
    }
    package["reconciliation_hash"] = _hash_package(package)
    _validate_256_reconciliation(package, dry_run_package["dry_run_hash"])
    return _deepcopy(package)


def _validate_beo_251(package: dict[str, Any]) -> None:
    try:
        _validate_upstream_beo_251(package, _EXPECTED_BEO_250_INTEGRATION_HASH)
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageValidationError(f"BEO 251 reconciliation upstream validation failed: {exc}") from exc
    if package.get("reconciliation_hash") != _EXPECTED_BEO_251_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("BEO 251 reconciliation reconciliation_hash mismatch")
    _reject_freeform_laundering(package, "BEO 251 reconciliation")


def _validate_blk_link_194(package: dict[str, Any]) -> None:
    try:
        _validate_blk_link_package(
            package,
            "reconciliation",
            RECONCILIATION_STATUS_194,
            RECONCILIATION_PACKAGE_ID_194,
            "reconciliation_status",
            "reconciliation_package_hash",
            CANONICAL_BLK194_RECONCILIATION_PACKAGE_HASH,
            EXACT_PROOF_OBLIGATIONS_194,
            EXACT_EXCLUDED_AUTHORITIES_194,
            SIDE_EFFECT_FLAGS_194,
            {"repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established"},
        )
    except ValueError as exc:
        raise RtmBlkLinkDriftCoverageValidationError(f"BLK-link 194 reconciliation upstream validation failed: {exc}") from exc
    if package.get("reconciliation_package_hash") != _EXPECTED_BLK_LINK_194_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("BLK-link 194 reconciliation hash mismatch")
    _reject_freeform_laundering(package, "BLK-link 194 reconciliation")


def _validate_252_review(package: dict[str, Any]) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_252, "surface review package")
    _require_hash(package, "surface_review_hash", "surface review package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_COMPLETE_NOT_AUTHORITY", "surface review package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_252_RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_READY",
        "BEO_REVIEW_METADATA_IS_NOT_PUBLISHED_BEO",
        "BLK_LINK_REPEATABILITY_IS_PER_RUN_EXACT_APPROVAL_ONLY",
    ], "surface review package")
    if package.get("beo_reconciliation_hash") != _EXPECTED_BEO_251_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("surface review BEO reconciliation_hash mismatch")
    if package.get("blk_link_reconciliation_hash") != _EXPECTED_BLK_LINK_194_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("surface review BLK-link reconciliation_hash mismatch")
    if package.get("required_metadata_inputs") != list(_REQUIRED_METADATA_INPUTS):
        raise RtmBlkLinkDriftCoverageValidationError("surface review required_metadata_inputs mismatch")
    _require_exact_denials(package.get("denied_authorities"), "surface review package")
    _require_side_effects(package, "surface review package")
    if _hash_package({k: v for k, v in package.items() if k != "surface_review_hash"}) != package.get("surface_review_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("surface review surface_review_hash mismatch")
    for finding in package.get("surface_findings", []):
        _reject_freeform_laundering(finding, "surface review finding")


def _validate_253_request(package: dict[str, Any], expected_review_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_253, "request package")
    _require_hash(package, "request_hash", "request package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED_NOT_GRANTED", "request package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_253_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED",
        "REQUEST_ONLY_NO_APPROVAL_OR_RUN_ID",
        "PROTECTED_BODY_FREE_METADATA_REQUIRED",
    ], "request package")
    if expected_review_hash and package.get("surface_review_hash") != expected_review_hash:
        raise RtmBlkLinkDriftCoverageValidationError("request package surface_review_hash mismatch")
    if package.get("request_rules") != _REQUEST_RULES:
        _reject_freeform_laundering(package.get("request_rules"), "request package request_rules")
        raise RtmBlkLinkDriftCoverageValidationError("request package request_rules mismatch")
    if package.get("required_metadata_inputs") != list(_REQUIRED_METADATA_INPUTS):
        raise RtmBlkLinkDriftCoverageValidationError("request package required_metadata_inputs mismatch")
    _require_exact_denials(package.get("denied_authorities"), "request package")
    _require_side_effects(package, "request package")
    if _hash_package({k: v for k, v in package.items() if k != "request_hash"}) != package.get("request_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("request package request_hash mismatch")
    _reject_freeform_laundering(package.get("request_scope"), "request package request_scope")


def _validate_254_contract(package: dict[str, Any], expected_request_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_254, "contract package")
    _require_hash(package, "contract_hash", "contract package")
    _require_status(package, "DRIFT_COVERAGE_VERIFIER_CONTRACT_READY_PER_RUN_EXACT_APPROVAL", "contract package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_254_DRIFT_COVERAGE_VERIFIER_CONTRACT_READY",
        "METADATA_ONLY_VERIFIER_CONTRACT",
        "NO_TRUTH_PROMOTION_WITHOUT_EXACT_PUBLICATION_APPROVAL",
    ], "contract package")
    if expected_request_hash and package.get("request_hash") != expected_request_hash:
        raise RtmBlkLinkDriftCoverageValidationError("contract package request_hash mismatch")
    if package.get("contract_rules") != _CONTRACT_RULES:
        _reject_freeform_laundering(package.get("contract_rules"), "contract package contract_rules")
        raise RtmBlkLinkDriftCoverageValidationError("contract package contract_rules mismatch")
    if package.get("record_only_policy") != _RECORD_ONLY_POLICY:
        raise RtmBlkLinkDriftCoverageValidationError("contract package record_only_policy mismatch")
    if package.get("verifier_record_states") != _RECORD_STATES:
        raise RtmBlkLinkDriftCoverageValidationError("contract package verifier_record_states mismatch")
    if package.get("required_metadata_inputs") != list(_REQUIRED_METADATA_INPUTS):
        raise RtmBlkLinkDriftCoverageValidationError("contract package required_metadata_inputs mismatch")
    _require_exact_denials(package.get("denied_authorities"), "contract package")
    _require_side_effects(package, "contract package")
    if _hash_package({k: v for k, v in package.items() if k != "contract_hash"}) != package.get("contract_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("contract package contract_hash mismatch")


def _validate_255_dry_run(package: dict[str, Any], expected_contract_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_255, "dry-run package")
    _require_hash(package, "dry_run_hash", "dry-run package")
    if package.get("status") != "EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_BLOCKED_BY_UNPUBLISHED_BEO":
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package status mismatch")
    _require_exact_markers(package, [
        "BLK_SYSTEM_255_EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_RECORDED",
        "BEO_PUBLICATION_REQUIRED_BEFORE_TRUTH",
        "NO_PROTECTED_BODY_OR_PRODUCTION_BLK_LINK_EXECUTION",
    ], "dry-run package")
    if expected_contract_hash and package.get("contract_hash") != expected_contract_hash:
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package contract_hash mismatch")
    _require_side_effects(package, "dry-run package")
    record = package.get("verifier_record")
    _validate_verifier_record(record)
    if not _is_hash(package.get("verifier_record_hash")):
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package verifier_record_hash must be canonical sha256")
    if _hash_package(record) != package.get("verifier_record_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package verifier_record_hash mismatch")
    if _hash_package({k: v for k, v in package.items() if k != "dry_run_hash"}) != package.get("dry_run_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package dry_run_hash mismatch")


def _validate_256_reconciliation(package: dict[str, Any], expected_dry_run_hash: str | None = None) -> None:
    _require_allowed_keys(package, _ALLOWED_KEYS_256, "reconciliation package")
    _require_hash(package, "reconciliation_hash", "reconciliation package")
    _require_status(package, "RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED_BEO_PUBLICATION_REQUIRED", "reconciliation package")
    _require_exact_markers(package, [
        "BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED",
        "BEO_PUBLICATION_RUN_SELECTED_AS_NEXT_REQUIRED_FRONTIER",
        _NEXT_FRONTIER,
    ], "reconciliation package")
    if expected_dry_run_hash and package.get("dry_run_hash") != expected_dry_run_hash:
        raise RtmBlkLinkDriftCoverageValidationError("reconciliation package dry_run_hash mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER:
        raise RtmBlkLinkDriftCoverageValidationError("reconciliation package next_frontier mismatch")
    _require_side_effects(package, "reconciliation package")
    if _hash_package({k: v for k, v in package.items() if k != "reconciliation_hash"}) != package.get("reconciliation_hash"):
        raise RtmBlkLinkDriftCoverageValidationError("reconciliation package reconciliation_hash mismatch")


def _normalize_metadata_inputs(inputs: dict[str, Any]) -> dict[str, Any]:
    _require_allowed_keys(inputs, _ALLOWED_INPUT_KEYS, "metadata inputs")
    normalized = _deepcopy(inputs)
    for key in _REQUIRED_METADATA_INPUTS:
        _require_hash(normalized, key, "metadata inputs")
    if normalized["beo_publication_reconciliation_hash"] != _EXPECTED_BEO_251_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("beo_publication_reconciliation_hash mismatch")
    if normalized["blk_link_reconciliation_hash"] != _EXPECTED_BLK_LINK_194_RECONCILIATION_HASH:
        raise RtmBlkLinkDriftCoverageValidationError("blk_link_reconciliation_hash mismatch")
    if normalized.get("beo_publication_state") != "REVIEW_METADATA_ONLY_NOT_PUBLISHED":
        raise RtmBlkLinkDriftCoverageValidationError(
            "authoritative BEO publication evidence cannot be self-attested by metadata inputs"
        )
    for key, value in normalized.items():
        if isinstance(value, str):
            _reject_freeform_laundering(value, key)
    return normalized


def _validate_verifier_record(record: Any) -> None:
    if not isinstance(record, dict):
        raise RtmBlkLinkDriftCoverageValidationError("dry-run package verifier record must be a dictionary")
    _require_allowed_keys(record, _ALLOWED_RECORD_KEYS, "dry-run package verifier record")
    if record.get("record_id") != "RTM-BLK-LINK-DRIFT-COVERAGE-DRY-RUN-255-001":
        raise RtmBlkLinkDriftCoverageValidationError("verifier record record_id mismatch")
    if record.get("record_state") != "BLOCKED_BY_MISSING_AUTHORITATIVE_BEO_METADATA":
        raise RtmBlkLinkDriftCoverageValidationError("verifier record record_state mismatch")
    if record.get("beo_publication_state") != "REVIEW_METADATA_ONLY_NOT_PUBLISHED":
        raise RtmBlkLinkDriftCoverageValidationError("verifier record beo_publication_state mismatch")
    if record.get("record_only_policy") != _RECORD_ONLY_POLICY:
        raise RtmBlkLinkDriftCoverageValidationError("verifier record record_only_policy mismatch")
    inputs = record.get("metadata_inputs")
    if not isinstance(inputs, dict):
        raise RtmBlkLinkDriftCoverageValidationError("verifier record metadata_inputs must be a dictionary")
    _require_allowed_keys(inputs, set(_REQUIRED_METADATA_INPUTS), "verifier record metadata_inputs")
    for key in _REQUIRED_METADATA_INPUTS:
        _require_hash(inputs, key, "verifier record metadata_inputs")
    _reject_freeform_laundering(record.get("operator_notes", ""), "verifier record operator_notes")
    _reject_freeform_laundering(record, "verifier record")


def _require_allowed_keys(value: Any, allowed: set[str], label: str) -> None:
    if not isinstance(value, dict):
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} must be a dictionary")
    extras = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if extras:
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} unsupported field: {extras[0]}")
    if missing:
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} missing field: {missing[0]}")


def _require_status(package: dict[str, Any], expected: str, label: str) -> None:
    if package.get("status") != expected:
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} status mismatch")


def _require_exact_markers(package: dict[str, Any], expected: list[str], label: str) -> None:
    if package.get("markers") != expected:
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} markers mismatch")


def _require_exact_denials(value: Any, label: str) -> None:
    if not isinstance(value, list):
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} denied_authorities must be a list")
    if any(not isinstance(item, str) for item in value):
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} denied_authorities must be strings")
    if len(value) != len(set(value)):
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} denied_authorities duplicate")
    if value != list(_DENIED_AUTHORITIES):
        _reject_freeform_laundering(value, f"{label} denied_authorities")
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} denied_authorities mismatch")


def _require_side_effects(package: dict[str, Any], label: str) -> None:
    effects = package.get("side_effects")
    if effects != _SIDE_EFFECTS:
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} side_effects mismatch")


def _require_false_effects(package: dict[str, Any], label: str) -> None:
    effects = package.get("side_effects")
    if not isinstance(effects, dict):
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} side_effects must be a dictionary")
    for key in (
        "reusable_beo_publication_authorized", "beo_published", "rtm_generation", "production_blk_link",
        "drift_rejection", "coverage_truth", "protected_body_access", "target_source_git_mutation",
    ):
        if effects.get(key) is not False:
            raise RtmBlkLinkDriftCoverageValidationError(f"{label} {key} must be false")


def _require_hash(package: dict[str, Any], key: str, label: str) -> None:
    if not _is_hash(package.get(key)):
        raise RtmBlkLinkDriftCoverageValidationError(f"{key} must be canonical sha256 in {label}")


def _reject_freeform_laundering(value: Any, label: str) -> None:
    findings = scan_for_authority_laundering(value)
    if findings:
        joined = "; ".join(str(f) for f in findings[:3])
        if "protected" in joined.casefold() or "docs" in joined.casefold():
            raise RtmBlkLinkDriftCoverageValidationError(f"{label} protected path or forbidden authority wording: {joined}")
        raise RtmBlkLinkDriftCoverageValidationError(f"{label} forbidden authority wording: {joined}")


def _hash_package(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 71 and value.startswith("sha256:") and all(c in "0123456789abcdef" for c in value[7:])


def _deepcopy(value: Any) -> Any:
    return deepcopy(value)
