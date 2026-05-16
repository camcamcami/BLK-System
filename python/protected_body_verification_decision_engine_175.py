"""BLK-SYSTEM-175 protected-body verification decision engine.

This module delivers a deterministic protected-body verification decision engine
without performing filesystem reads or returning protected body text. It consumes
the exact BLK-SYSTEM-174 request package and a caller-supplied protected-body hash
verification input set, then emits a hash-bound decision record for the RTM /
blk-link evidence path.

The engine compares caller-supplied expected/observed protected-body hashes only.
It does not read/copy/parse/hash/scan protected files itself, generate RTM, reject
drift, establish coverage truth, run reusable production blk-link, mutate source
or Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_authority_smuggling import compact_authority_text, decoded_authority_variants

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_ladder_168_171 import (
    _parse_not_stale,
    _validate_decision_window,
    _validate_trace_copy,
)
from metadata_bound_drift_coverage_decision_ladder_172_174 import (
    CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH,
    CANONICAL_BLK174_AUTHORITY_REQUEST_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_174,
    EXACT_PROOF_OBLIGATIONS_174,
    NEXT_REQUIRED_AUTHORITY_174,
    REQUEST_PACKAGE_ID_174,
    REQUEST_SCOPE_174,
    REQUEST_STATUS_174,
    SELECTED_FRONTIER_174,
    SIDE_EFFECT_FLAGS_174,
)
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_trace_closure_approval_capture import (
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)

DECISION_EXECUTION_STATUS_175 = "PROTECTED_BODY_VERIFICATION_DECISION_CAPTURED_AND_ONE_RUN_RECORDED_FOR_EXACT_BLK174_REQUEST"
DECISION_EXECUTION_PACKAGE_ID_175 = "PROTECTED-BODY-VERIFICATION-DECISION-EXECUTION-175-001"
VERIFICATION_RECORD_ID_175 = "PROTECTED-BODY-VERIFICATION-RECORD-175-001"
DECISION_EXECUTION_SCOPE_175 = "EXACT_PROTECTED_BODY_HASH_VERIFICATION_DECISION_RECORD_ONLY_NOT_DRIFT_OR_COVERAGE_TRUTH"
SELECTED_FRONTIER_175 = "protected_body_verification_decision_engine_175"
APPROVAL_ID_175 = "APPROVAL-BLK-SYSTEM-174-PROTECTED-BODY-VERIFICATION-DECISION-001"
RUN_ID_CONSUMED_175 = "RUN-BLK-SYSTEM-175-PROTECTED-BODY-VERIFICATION-DECISION-001"
EXACT_OPERATOR_DECISION_TEXT_175 = (
    "APPROVE PROTECTED-BODY-VERIFICATION-DECISION-AUTHORITY-REQUEST-174-001 "
    "FOR ONE CALLER-SUPPLIED PROTECTED-BODY HASH VERIFICATION DECISION RUN "
    "RUN-BLK-SYSTEM-175-PROTECTED-BODY-VERIFICATION-DECISION-001; "
    "NO BODY TEXT RETURNED; NO RTM GENERATION; NO RTM DRIFT REJECTION; "
    "NO COVERAGE TRUTH; NO MUTATION."
)
VERIFICATION_MATCH_RESULT_175 = "PROTECTED_BODY_HASHES_VERIFIED_NOT_COVERAGE_TRUTH_OR_DRIFT_REJECTION"
VERIFICATION_MISMATCH_RESULT_175 = "PROTECTED_BODY_HASH_MISMATCH_RECORDED_NOT_DRIFT_REJECTION_OR_COVERAGE_TRUTH"
NEXT_REQUIRED_AUTHORITY_175 = "RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_INTEGRATION_REQUIRED_NOT_STARTED"
CANONICAL_BLK175_VERIFICATION_RECORD_HASH = "sha256:473aa55bb75cf191879c8e88a06877ba8bdab8722707a3e51c023288911a1f95"
CANONICAL_BLK175_DECISION_EXECUTION_PACKAGE_HASH = "sha256:161cd688b92adb537483b0b00318871fc7fc3b0925e834eb950550e120950e2e"

_BASE_EXCLUDED_175 = {
    "PROTECTED_BODY_TEXT_RETURN_OR_BODY_CONTENT_EXPOSURE",
    "PROTECTED_BODY_FILESYSTEM_READ_BY_ENGINE",
    "PROTECTED_BODY_COPY_PARSE_SCAN_BY_ENGINE",
    "PROTECTED_BODY_PATH_DISCLOSURE",
    "AUTHORITATIVE_DRIFT_DECISION_OR_REJECTION",
    "RTM_DRIFT_REJECTION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "ACTIVE_VAULT_FILESYSTEM_READ_OR_SCAN",
    "REUSABLE_ACTIVE_VAULT_COMPARISON_AUTHORITY",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_LIVE_RUNTIME_EXECUTION_BEYOND_RECORD_ONLY_EVIDENCE",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "TARGET_REPO_SCAN",
    "TARGET_REPO_MUTATION",
    "SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BEO_PUBLICATION_OR_SIGNING",
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_EXCLUDED_AUTHORITIES_175 = _BASE_EXCLUDED_175 | {
    "RUN_ID_REUSE_AFTER_RECORD_ONLY_CONSUMPTION",
    "PROTECTED_BODY_VERIFICATION_REUSABLE_AUTHORITY",
    "RTM_BLK_LINK_EVIDENCE_INTEGRATION_THIS_SPRINT",
}

EXACT_PROOF_OBLIGATIONS_175 = {
    "BLK174_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK173_RECONCILIATION_HASH_BOUND_THROUGH_BLK174",
    "BLK172_DECISION_EXECUTION_HASH_BOUND_THROUGH_BLK173",
    "OPERATOR_DECISION_CAPTURED_FOR_EXACT_BLK174_REQUEST",
    "APPROVAL_ID_BOUND_TO_EXACT_REQUEST",
    "RUN_ID_CONSUMED_ONCE_IN_RECORD_ONLY_EVIDENCE",
    "PROTECTED_BODY_VERIFICATION_LIMITED_TO_CALLER_SUPPLIED_HASH_METADATA",
    "PROTECTED_BODY_TEXT_NOT_INCLUDED_OR_RETURNED",
    "PROTECTED_BODY_PATHS_NOT_INCLUDED",
    "VERIFICATION_RECORD_HASH_BOUND_TO_DECISION_PACKAGE",
    "RTM_GENERATION_DRIFT_REJECTION_COVERAGE_TRUTH_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
}

SIDE_EFFECT_FLAGS_175 = (
    "operator_decision_captured",
    "one_run_id_consumed_in_record_only_evidence",
    "protected_body_verification_decision_recorded",
    "protected_body_hashes_compared_from_caller_supplied_metadata",
    "approval_capture_performed_outside_exact_request",
    "protected_body_text_included",
    "protected_body_content_returned",
    "protected_body_filesystem_read_performed",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_parsing_attempted",
    "protected_body_hashing_attempted_by_fixture",
    "protected_body_scan_attempted",
    "protected_body_path_disclosed",
    "active_vault_filesystem_read_performed",
    "active_vault_scanned",
    "runtime_rtm_generation_authorized",
    "rtm_generated",
    "reusable_rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_live_execution_performed",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "beo_publication_or_signing_authorized",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

_ATTESTATION_175 = frozenset({
    "exact_blk174_request_reviewed",
    "operator_decision_captured_from_latest_directive",
    "run_id_consumed_once_in_record_only_evidence",
    "caller_supplied_hash_metadata_only_scope_preserved",
    "protected_body_text_not_included_or_returned",
    "protected_body_paths_not_included",
    "verification_record_hash_bound",
    "rtm_generation_excluded",
    "drift_rejection_excluded",
    "coverage_truth_excluded",
    "reusable_blk_link_excluded",
    "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
})

_REQUEST_KEYS_175 = frozenset({
    "decision_execution_package_id", "operator_identity", "decision_execution_scope", "selected_frontier",
    "upstream_authority_request_package_id", "upstream_authority_request_package_hash",
    "approval_id", "run_id_to_consume", "beo_id", "beb_id", "exact_trace_identities",
    "protected_body_verification_inputs", "operator_decision_text_raw", "decided_at", "requested_at",
    "expires_at", "expired", "replayed", "stale", "operator_attestation", "proof_obligations",
    "excluded_authorities", *SIDE_EFFECT_FLAGS_175,
})

_PROTECTED_BODY_INPUT_KEYS = frozenset({
    "kind", "id", "expected_body_hash", "observed_body_hash", "verification_source",
    "body_text_included", "body_excerpt", "protected_body_path", "body_copied", "body_parsed",
    "body_scanned", "protected_body_content_returned",
})
_PROTECTED_BODY_INPUT_FALSE_FLAGS = (
    "body_text_included", "body_copied", "body_parsed", "body_scanned", "protected_body_content_returned",
)

_PACKAGE_KEYS_174 = frozenset({
    "request_status", "authority_request_package_id", "operator_identity", "request_scope", "selected_frontier",
    "upstream_reconciliation_package_id", "upstream_reconciliation_package_hash",
    "upstream_decision_execution_package_hash", "beo_id", "beb_id", "exact_trace_identities",
    "request_future_exact_protected_body_verification_approval", "approval_capture_performed",
    "protected_body_reads", "protected_body_hashing_attempted", "coverage_truth_established",
    "rtm_drift_rejection_performed", "next_required_authority", "authority_request_hash",
    "requested_at", "expires_at", "expired", "replayed", "stale", "operator_attestation",
    "proof_obligations", "excluded_authorities", "authority_request_package_hash", *SIDE_EFFECT_FLAGS_174,
})


def valid_protected_body_verification_decision_execution_175(request174: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    record = {
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_175,
        "operator_identity": request174["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_175,
        "selected_frontier": SELECTED_FRONTIER_175,
        "upstream_authority_request_package_id": request174["authority_request_package_id"],
        "upstream_authority_request_package_hash": request174["authority_request_package_hash"],
        "approval_id": APPROVAL_ID_175,
        "run_id_to_consume": RUN_ID_CONSUMED_175,
        "beo_id": request174["beo_id"],
        "beb_id": request174["beb_id"],
        "exact_trace_identities": list(request174["exact_trace_identities"]),
        "protected_body_verification_inputs": _protected_body_inputs_from_trace_ids(request174["exact_trace_identities"]),
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_175,
        "decided_at": "2099-05-16T21:35:00+10:00",
        "requested_at": "2099-05-16T21:36:00+10:00",
        "expires_at": "2099-05-16T21:45:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {key: True for key in _ATTESTATION_175},
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_175),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_175),
    }
    for flag in SIDE_EFFECT_FLAGS_175:
        record[flag] = False
    record["operator_decision_captured"] = True
    record["one_run_id_consumed_in_record_only_evidence"] = True
    record["protected_body_verification_decision_recorded"] = True
    record["protected_body_hashes_compared_from_caller_supplied_metadata"] = True
    record.update(overrides)
    return record


def build_protected_body_verification_decision_engine_175(request174_package: dict[str, Any], decision175: dict[str, Any]) -> dict[str, Any]:
    request174 = _validate_174_package(request174_package)
    decision = _validate_request_like(
        decision175,
        _REQUEST_KEYS_175,
        _ATTESTATION_175,
        EXACT_PROOF_OBLIGATIONS_175,
        EXACT_EXCLUDED_AUTHORITIES_175,
        SIDE_EFFECT_FLAGS_175,
        true_flags={
            "operator_decision_captured",
            "one_run_id_consumed_in_record_only_evidence",
            "protected_body_verification_decision_recorded",
            "protected_body_hashes_compared_from_caller_supplied_metadata",
        },
    )
    _scan_high_risk_freeform(decision["operator_identity"], "operator_identity")
    _require(decision, "decision_execution_package_id", DECISION_EXECUTION_PACKAGE_ID_175)
    _require(decision, "decision_execution_scope", DECISION_EXECUTION_SCOPE_175)
    _require(decision, "selected_frontier", SELECTED_FRONTIER_175)
    _require(decision, "approval_id", APPROVAL_ID_175)
    _require(decision, "run_id_to_consume", RUN_ID_CONSUMED_175)
    _require(decision, "operator_decision_text_raw", EXACT_OPERATOR_DECISION_TEXT_175)
    _require_matching_upstream(decision, request174, (
        ("upstream_authority_request_package_id", "authority_request_package_id"),
        ("upstream_authority_request_package_hash", "authority_request_package_hash"),
        ("operator_identity", "operator_identity"),
        ("beo_id", "beo_id"),
        ("beb_id", "beb_id"),
    ))
    _validate_decision_window(decision["decided_at"], decision["requested_at"], decision["expires_at"], request174["requested_at"], request174["expires_at"])
    trace_ids = _validate_trace_copy(decision["exact_trace_identities"], request174["exact_trace_identities"])
    observed = _validate_protected_body_inputs(decision["protected_body_verification_inputs"], trace_ids)
    verification_record = _build_verification_record(decision, trace_ids, observed)
    verified = verification_record["protected_body_hashes_verified"]
    package = {
        "decision_execution_status": DECISION_EXECUTION_STATUS_175,
        "decision_execution_package_id": DECISION_EXECUTION_PACKAGE_ID_175,
        "operator_identity": decision["operator_identity"],
        "decision_execution_scope": DECISION_EXECUTION_SCOPE_175,
        "selected_frontier": SELECTED_FRONTIER_175,
        "upstream_authority_request_package_id": request174["authority_request_package_id"],
        "upstream_authority_request_package_hash": request174["authority_request_package_hash"],
        "upstream_reconciliation_package_hash": request174["upstream_reconciliation_package_hash"],
        "upstream_decision_execution_package_hash": request174["upstream_decision_execution_package_hash"],
        "approval_id": APPROVAL_ID_175,
        "run_id_consumed": RUN_ID_CONSUMED_175,
        "operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_175,
        "operator_decision_captured": True,
        "one_run_id_consumed_in_record_only_evidence": True,
        "protected_body_verification_decision_recorded": True,
        "protected_body_hashes_compared_from_caller_supplied_metadata": True,
        "protected_body_hashes_verified": verified,
        "verification_result": VERIFICATION_MATCH_RESULT_175 if verified else VERIFICATION_MISMATCH_RESULT_175,
        "mismatches": deepcopy(verification_record["mismatches"]),
        "beo_id": request174["beo_id"],
        "beb_id": request174["beb_id"],
        "exact_trace_identities": trace_ids,
        "protected_body_verification_inputs": deepcopy(observed),
        "verification_record_id": VERIFICATION_RECORD_ID_175,
        "verification_record": verification_record,
        "verification_record_hash": verification_record["verification_record_hash"],
        "decision_execution_request_hash": _canonical_hash(decision),
        "decided_at": decision["decided_at"],
        "requested_at": decision["requested_at"],
        "expires_at": decision["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY_175,
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_175),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_175),
    }
    for flag in SIDE_EFFECT_FLAGS_175:
        package[flag] = False
    package["operator_decision_captured"] = True
    package["one_run_id_consumed_in_record_only_evidence"] = True
    package["protected_body_verification_decision_recorded"] = True
    package["protected_body_hashes_compared_from_caller_supplied_metadata"] = True
    package["decision_execution_package_hash"] = _canonical_hash(package)
    return package


def _validate_174_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("BLK-174 package must be a dictionary")
    extra = sorted(set(package) - _PACKAGE_KEYS_174)
    if extra:
        raise ValueError(f"unexpected BLK-174 field {extra[0]!r}")
    missing = sorted(_PACKAGE_KEYS_174 - set(package))
    if missing:
        raise ValueError(f"missing BLK-174 field {missing[0]!r}")
    if package.get("request_status") != REQUEST_STATUS_174:
        raise ValueError("request_status must be exact BLK-174 status")
    if package.get("authority_request_package_id") != REQUEST_PACKAGE_ID_174:
        raise ValueError("authority_request_package_id must be exact BLK-174 id")
    _required_hash(package.get("authority_request_package_hash"), "authority_request_package_hash")
    computed = _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"})
    if package["authority_request_package_hash"] != computed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-174 package")
    if package["authority_request_package_hash"] != CANONICAL_BLK174_AUTHORITY_REQUEST_PACKAGE_HASH:
        raise ValueError("canonical BLK-174 authority request package hash mismatch")
    _require(package, "request_scope", REQUEST_SCOPE_174)
    _require(package, "selected_frontier", SELECTED_FRONTIER_174)
    _require(package, "next_required_authority", NEXT_REQUIRED_AUTHORITY_174)
    _require_true(package, "request_future_exact_protected_body_verification_approval")
    if package.get("upstream_reconciliation_package_hash") != CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("BLK-174 must bind canonical BLK-173 reconciliation package hash")
    if package.get("upstream_decision_execution_package_hash") != CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-174 must bind canonical BLK-172 decision package hash")
    _required_exact_set(package.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS_174, "BLK-174 proof_obligations")
    _required_exact_set(package.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES_174, "BLK-174 excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS_174:
        if package.get(flag) is not False:
            raise ValueError(f"BLK-174 package {flag} must remain false")
    return package


def _validate_request_like(record: Any, keys: frozenset[str], attestation_keys: frozenset[str], proof_set: set[str], excluded_set: set[str], false_flags: tuple[str, ...], true_flags: set[str] | None = None) -> dict[str, Any]:
    if true_flags is None:
        true_flags = set()
    if not isinstance(record, dict):
        raise ValueError("record must be a dictionary")
    extra = sorted(set(record) - keys)
    if extra:
        raise ValueError(f"unexpected field {extra[0]!r}")
    missing = sorted(keys - set(record))
    if missing:
        raise ValueError(f"missing field {missing[0]!r}")
    if record.get("expired") is not False:
        raise ValueError("record must not be expired")
    if record.get("replayed") is not False:
        raise ValueError("record must not be replayed")
    if record.get("stale") is not False:
        raise ValueError("record must not be stale")
    if not isinstance(record.get("operator_attestation"), dict):
        raise ValueError("operator_attestation must be a dictionary")
    attestation_extra = sorted(set(record["operator_attestation"]) - attestation_keys)
    if attestation_extra:
        raise ValueError(f"unexpected field {attestation_extra[0]!r}")
    if set(record["operator_attestation"]) != attestation_keys:
        raise ValueError("operator_attestation must match exact key set")
    for key, value in record["operator_attestation"].items():
        if value is not True:
            raise ValueError(f"operator_attestation {key} must be true")
    _required_exact_set(record.get("proof_obligations"), proof_set, "proof_obligations")
    _required_exact_set(record.get("excluded_authorities"), excluded_set, "excluded_authorities")
    _scan_high_risk_freeform(record.get("operator_identity"), "operator_identity")
    for flag in false_flags:
        expected = flag in true_flags
        if record.get(flag) is not expected:
            if expected:
                raise ValueError(f"{flag} must be true")
            raise ValueError(f"{flag} must remain false")
    return record


def _protected_body_inputs_from_trace_ids(trace_ids: list[str]) -> list[dict[str, Any]]:
    records = []
    for identity in trace_ids:
        kind, artifact_id, version_hash = _parse_trace_identity(identity)
        records.append({
            "kind": kind,
            "id": artifact_id,
            "expected_body_hash": version_hash,
            "observed_body_hash": version_hash,
            "verification_source": "CALLER_SUPPLIED_PROTECTED_BODY_HASH_METADATA_ONLY",
            "body_text_included": False,
            "body_excerpt": "",
            "protected_body_path": "",
            "body_copied": False,
            "body_parsed": False,
            "body_scanned": False,
            "protected_body_content_returned": False,
        })
    return records


def _validate_protected_body_inputs(records: Any, trace_ids: list[str]) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError("protected_body_verification_inputs must be a list")
    expected = {(_parse_trace_identity(identity)[0], _parse_trace_identity(identity)[1]): _parse_trace_identity(identity)[2] for identity in trace_ids}
    if len(records) != len(expected):
        raise ValueError("protected_body_verification_inputs must match exact identity set")
    observed = {}
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("protected_body_verification_inputs entries must be dictionaries")
        extra = sorted(set(item) - _PROTECTED_BODY_INPUT_KEYS)
        if extra:
            raise ValueError(f"unexpected protected-body input field {extra[0]!r}")
        missing = sorted(_PROTECTED_BODY_INPUT_KEYS - set(item))
        if missing:
            raise ValueError(f"missing protected-body input field {missing[0]!r}")
        for flag in _PROTECTED_BODY_INPUT_FALSE_FLAGS:
            if item.get(flag) is not False:
                raise ValueError(f"{flag} must remain false")
        if item.get("verification_source") != "CALLER_SUPPLIED_PROTECTED_BODY_HASH_METADATA_ONLY":
            raise ValueError("verification_source must be caller-supplied protected-body hash metadata only")
        if item.get("protected_body_path") != "":
            raise ValueError("protected paths must not be included")
        if item.get("body_excerpt") != "":
            raise ValueError("protected body text must not be included")
        _required_hash(item.get("expected_body_hash"), "expected_body_hash")
        _required_hash(item.get("observed_body_hash"), "observed_body_hash")
        key = (item.get("kind"), item.get("id"))
        if key in observed:
            raise ValueError("duplicate protected-body verification identity")
        if key not in expected:
            raise ValueError("protected_body_verification_inputs must match exact identity set")
        if item.get("expected_body_hash") != expected[key]:
            raise ValueError("expected_body_hash must match exact trace identity")
        _scan_high_risk_freeform(item.get("kind"), "kind")
        _scan_high_risk_freeform(item.get("id"), "id")
        observed[key] = deepcopy(item)
    if set(observed) != set(expected):
        raise ValueError("protected_body_verification_inputs must match exact identity set")
    return [observed[key] for key in sorted(observed)]


def _build_verification_record(decision: dict[str, Any], trace_ids: list[str], observed: list[dict[str, Any]]) -> dict[str, Any]:
    mismatches = []
    for item in observed:
        if item["observed_body_hash"] != item["expected_body_hash"]:
            mismatches.append({
                "kind": item["kind"],
                "id": item["id"],
                "expected_body_hash": item["expected_body_hash"],
                "observed_body_hash": item["observed_body_hash"],
            })
    record = {
        "verification_record_id": VERIFICATION_RECORD_ID_175,
        "run_id_consumed": RUN_ID_CONSUMED_175,
        "approval_id": APPROVAL_ID_175,
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
        "exact_trace_identities": list(trace_ids),
        "protected_body_verification_inputs": deepcopy(observed),
        "protected_body_hashes_verified": not mismatches,
        "mismatches": mismatches,
        "recorded_at": decision["requested_at"],
        "protected_body_filesystem_read_performed": False,
        "protected_body_text_included": False,
        "protected_body_content_returned": False,
        "rtm_generated": False,
        "rtm_drift_rejection_performed": False,
        "drift_decision_made": False,
        "coverage_truth_established": False,
        "target_repo_scan_or_mutation": False,
    }
    record["verification_record_hash"] = _canonical_hash(record)
    return record


def _parse_trace_identity(identity: str) -> tuple[str, str, str]:
    pieces = identity.split(":")
    if len(pieces) != 4 or pieces[2] != "sha256":
        raise ValueError("exact_trace_identities id must be exact")
    return pieces[0], pieces[1], "sha256:" + pieces[3]


def _require(record: dict[str, Any], key: str, expected: Any) -> None:
    if record.get(key) != expected:
        value = record.get(key)
        if isinstance(value, str):
            lowered = value.lower()
            if "docs%" in lowered or "requirements" in lowered or "the system shall" in lowered or "system%20shall" in lowered:
                _scan_value_strings(value, key)
        raise ValueError(f"{key} must be {expected!r}")


def _require_true(record: dict[str, Any], key: str) -> None:
    if record.get(key) is not True:
        raise ValueError(f"{key} must be true")


def _require_matching_upstream(record: dict[str, Any], upstream: dict[str, Any], pairs: tuple[tuple[str, str], ...]) -> None:
    for local_key, upstream_key in pairs:
        if record.get(local_key) != upstream.get(upstream_key):
            raise ValueError(f"{local_key} must match upstream {upstream_key}")


def _scan_high_risk_freeform(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    forbidden = (
        "driftrejectionexecuted", "driftrejectionauthorized", "driftdecisionauthorized",
        "coveragetruthauthorized", "coveragetruthestablished", "coveragematrixgenerated",
        "rtmgeneration", "rtmgenerated", "rtmid", "activevaulthashcomparisonauthorized",
        "beopublicationauthorized", "publishbeo", "codexapproval", "blkpipesuccess",
        "blktestpassapproval", "productionisolationclaimed", "approvedforproduction",
        "publicationauthoritygranted", "approvedforpublication", "greenlit", "allowed", "permitted",
        "rtmdriftrejectionauthorized", "rtmdriftrejectionisauthorized", "docsrequirementsactive",
    )
    for variant in decoded_authority_variants(value):
        compact = compact_authority_text(variant)
        if any(token in compact for token in forbidden):
            raise ValueError(f"authority-laundering text in {label}")
        lowered = variant.lower()
        if "docs/requirements/active" in lowered or "the system shall" in lowered:
            raise ValueError(f"authority-laundering text in {label}")
