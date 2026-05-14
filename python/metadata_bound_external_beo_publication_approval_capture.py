"""BLK-SYSTEM-128 metadata-bound external BEO publication approval capture.

This fixture records an explicit human approval decision for the exact
BLK-SYSTEM-127 prerequisite request package. It reserves one future publication
execution run ID, but it does not publish, sign, write storage, append ledgers,
execute rollback/revocation/supersession, generate RTM, perform drift rejection,
read protected BLK-req bodies, run BLK-pipe/BLK-test/Codex/tooling, or mutate
source/Git/target state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_beo_publication_prerequisite_request import (
    EXACT_EXCLUDED_AUTHORITIES as BLK127_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK127_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK127_NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID as BLK127_REQUEST_PACKAGE_ID,
    REQUEST_SCOPE as BLK127_REQUEST_SCOPE,
    REQUEST_STATUS as BLK127_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK127_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK127_SIDE_EFFECT_FLAGS,
    _decoded_variants,
    _parse_timestamp,
    _reject_laundered_string,
    _required_exact_set,
    _required_hash,
    _required_string,
    _validate_exact_trace_identities,
)

STATUS = "EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURED_FOR_EXACT_BLK127_REQUEST_NOT_PUBLISHED"
APPROVAL_DECISION_PACKAGE_ID = "BEO-PUBLICATION-APPROVAL-CAPTURE-128-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-128-EXTERNAL-BEO-PUBLICATION-001"
FUTURE_PUBLICATION_EXECUTION_RUN_ID = "RUN-BLK-SYSTEM-129-EXTERNAL-BEO-PUBLICATION-001"
SELECTED_FRONTIER = "external_beo_publication_approval_capture"
DECISION_SCOPE = "EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURE_ONLY_NOT_PUBLICATION_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_EXTERNAL_BEO_PUBLICATION_EXECUTION_NOT_PUBLISHED"
NEXT_REQUIRED_AUTHORITY = "SEPARATELY_SCOPED_EXTERNAL_BEO_PUBLICATION_EXECUTION_REQUIRED_NOT_RUN"
OPERATOR_APPROVAL_TEXT_RAW = (
    "I approve external BEO publication for "
    "BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001 under BLK-SYSTEM-128"
)
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T08:52:12+10:00")
CANONICAL_BLK127_REQUEST_PACKAGE_HASH = "sha256:bc7155e48ba92167a03d5f9a1bdedb073aec956c228208c380a9053e66097273"
CANONICAL_BLK127_OPERATOR_IDENTITY = "discord:684235178083745819"
CANONICAL_BLK127_DECISION_GATE_HASH = "sha256:48e07a0565fe3bcf9c684224c9ee3e9cafb6c2319a71869bdf465bf8ea1638d7"
CANONICAL_BLK127_INTERFACE_HASH = "sha256:679e9cac1b34aef8ae619a518120e5a32209a440c682754c5ecc5cbd87dba803"
CANONICAL_BLK127_TRACE_IDENTITIES = (
    "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
)
CANONICAL_BLK127_REQUESTED_AT = "2099-05-15T08:00:00+10:00"
CANONICAL_BLK127_EXPIRES_AT = "2099-05-15T09:00:00+10:00"

SIDE_EFFECT_FLAGS = (
    "future_publication_execution_run_id_consumed",
    "external_authoritative_publication_performed",
    "runtime_published_beo_output",
    "publication_execution_performed",
    "signer_key_material_accessed",
    "cryptographic_signature_generated",
    "immutable_storage_written",
    "storage_write_attempted",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_performed",
    "rtm_drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "protected_body_read",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "target_repo_scanned",
    "target_repo_mutated",
    "source_mutation_attempted",
    "git_mutation_attempted",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_execution_authorized",
    "blk_test_runtime_authorized",
    "codex_live_execution_authorized",
    "package_network_model_browser_cyber_tooling_authorized",
    "production_isolation_claimed",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "EXTERNAL_BEO_PUBLICATION_EXECUTION_THIS_SPRINT",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "FUTURE_PUBLICATION_EXECUTION_RUN_ID_CONSUMPTION",
    "PUBLICATION_AUTHORIZED_MARKER_OUTSIDE_BLK128_DECISION_RECORD",
    "SIGNING_GRANTED_MARKER_OR_SIGNER_AUTHORITY",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNING",
    "IMMUTABLE_STORAGE_WRITE",
    "PUBLIC_LEDGER_APPEND_OR_MUTATION",
    "ROLLBACK_EXECUTION",
    "REVOCATION_EXECUTION",
    "SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX",
    "COVERAGE_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "TARGET_REPO_SCAN",
    "TARGET_REPO_MUTATION",
    "SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK127_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK127_REQUEST_STATUS_NOT_GRANTED_BOUND",
    "BLK127_DECISION_GATE_AND_METADATA_INTERFACE_BOUND",
    "HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_CAPTURED_FOR_EXACT_REQUEST",
    "OPERATOR_RAW_TEXT_AND_NORMALIZED_REQUEST_ID_BOUND",
    "APPROVAL_ID_RESERVED_FOR_BLK128_DECISION",
    "FUTURE_PUBLICATION_EXECUTION_RUN_ID_RESERVED_NOT_CONSUMED",
    "EXTERNAL_PUBLICATION_NOT_EXECUTED_BY_APPROVAL_CAPTURE",
    "PUBLICATION_AUTHORIZED_AND_SIGNING_GRANTED_MARKERS_REJECTED_OUTSIDE_RECORD",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "TARGET_REPO_AND_SOURCE_GIT_MUTATION_EXCLUDED",
    "BLK_PIPE_BLK_TEST_CODEX_TOOLING_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_EXTERNAL_PUBLICATION_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
        "request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "next_required_authority",
        "upstream_decision_id",
        "upstream_decision_gate_hash",
        "upstream_interface_id",
        "upstream_interface_hash",
        "beo_id",
        "beb_id",
        "beo_status",
        "beo_publication",
        "rtm_status",
        "rtm_authority",
        "metadata_handoff_status",
        "trace_artifacts",
        "exact_trace_identities",
        "external_beo_publication_approval_capture_requested",
        "external_beo_publication_approval_captured",
        "publication_execution_requires_separate_sprint_after_approval",
        "decision_gate_summary",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "requested_at",
        "expires_at",
        "request_package_hash",
        *BLK127_SIDE_EFFECT_FLAGS,
    }
)

_DECISION_KEYS = frozenset(
    {
        "approval_decision_package_id",
        "operator_identity",
        "operator_approval_text_raw",
        "operator_approved_request_package_id_normalized",
        "decision_scope",
        "selected_frontier",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "upstream_request_status",
        "exact_upstream_decision_id",
        "exact_upstream_decision_gate_hash",
        "exact_upstream_interface_id",
        "exact_upstream_interface_hash",
        "exact_beo_id",
        "exact_beb_id",
        "exact_trace_identities",
        "approval_id",
        "future_publication_execution_run_id",
        "decision_result",
        "decided_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk127_request_reviewed",
        "operator_text_normalized_to_exact_request_id",
        "approval_limited_to_one_future_external_publication_execution_sprint",
        "external_publication_not_executed_by_this_decision",
        "future_run_id_reserved_not_consumed",
        "metadata_only_trace_boundary_reviewed",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "rtm_generation_and_drift_excluded",
        "protected_body_reads_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)


def build_metadata_bound_external_beo_publication_approval_capture(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Build an exact approval-capture package without publication execution."""

    request_pkg = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request_pkg)
    package = {
        "approval_capture_status": STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "operator_approval_text_raw": OPERATOR_APPROVAL_TEXT_RAW,
        "operator_approved_request_package_id_normalized": BLK127_REQUEST_PACKAGE_ID,
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "decision_result": DECISION_RESULT,
        "upstream_request_package_id": request_pkg["request_package_id"],
        "upstream_request_package_hash": request_pkg["request_package_hash"],
        "upstream_request_status": request_pkg["request_status"],
        "upstream_decision_id": request_pkg["upstream_decision_id"],
        "upstream_decision_gate_hash": request_pkg["upstream_decision_gate_hash"],
        "upstream_interface_id": request_pkg["upstream_interface_id"],
        "upstream_interface_hash": request_pkg["upstream_interface_hash"],
        "beo_id": request_pkg["beo_id"],
        "beb_id": request_pkg["beb_id"],
        "exact_trace_identities": list(request_pkg["exact_trace_identities"]),
        "approval_id": APPROVAL_ID,
        "future_publication_execution_run_id": FUTURE_PUBLICATION_EXECUTION_RUN_ID,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_external_beo_publication_approval_granted": True,
        "future_external_beo_publication_execution_approved": True,
        "beo_publication_status": "APPROVAL_CAPTURED_NOT_PUBLISHED",
        "rtm_status": "NOT_GENERATED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_capture_package_hash"] = _canonical_hash(package)
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"request_package rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("request_package_hash"), "request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("request_package_hash does not match submitted BLK-127 package")
    if submitted_hash != CANONICAL_BLK127_REQUEST_PACKAGE_HASH:
        raise ValueError("request package must match canonical BLK-127 request hash")

    if normalized.get("request_status") != BLK127_REQUEST_STATUS:
        raise ValueError("request package must be BLK-127 prerequisite request-ready")
    if normalized.get("request_package_id") != BLK127_REQUEST_PACKAGE_ID:
        raise ValueError("request_package_id must match BLK-127")
    if normalized.get("request_scope") != BLK127_REQUEST_SCOPE:
        raise ValueError("request_scope must remain BLK-127 review-only")
    if normalized.get("selected_frontier") != BLK127_SELECTED_FRONTIER:
        raise ValueError("request package must match BLK-127 prerequisite request")
    if normalized.get("next_required_authority") != BLK127_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-127 request must still require external BEO publication approval capture")
    if normalized.get("external_beo_publication_approval_capture_requested") is not True:
        raise ValueError("BLK-127 request must request external publication approval capture")
    if normalized.get("operator_identity") != CANONICAL_BLK127_OPERATOR_IDENTITY:
        raise ValueError("request package must match canonical BLK-127 operator identity")
    if normalized.get("requested_at") != CANONICAL_BLK127_REQUESTED_AT or normalized.get("expires_at") != CANONICAL_BLK127_EXPIRES_AT:
        raise ValueError("request package must match canonical BLK-127 approval-capture window")
    if normalized.get("external_beo_publication_approval_captured") is not False:
        raise ValueError("BLK-127 request must remain not approval-captured")
    if normalized.get("publication_execution_requires_separate_sprint_after_approval") is not True:
        raise ValueError("BLK-127 request must preserve separate execution sprint boundary")

    exact_values = {
        "upstream_decision_id": "BEO-PUBLICATION-PATH-DECISION-GATE-126-001",
        "upstream_interface_id": "BEO_RTM_IFACE_126",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "beo_status": "PASS",
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "rtm_authority": "DISABLED_INTERFACE_ONLY",
        "metadata_handoff_status": "BLK_REQ_TRACE_METADATA_ONLY",
    }
    for key, expected in exact_values.items():
        if normalized.get(key) != expected:
            raise ValueError("request package must match BLK-127 prerequisite request")
    if _required_hash(normalized.get("upstream_decision_gate_hash"), "upstream_decision_gate_hash") != CANONICAL_BLK127_DECISION_GATE_HASH:
        raise ValueError("request package must match canonical BLK-127 decision gate hash")
    if _required_hash(normalized.get("upstream_interface_hash"), "upstream_interface_hash") != CANONICAL_BLK127_INTERFACE_HASH:
        raise ValueError("request package must match canonical BLK-127 interface hash")
    normalized["exact_trace_identities"] = _validate_exact_trace_identities(normalized.get("exact_trace_identities"))
    if tuple(normalized["exact_trace_identities"]) != CANONICAL_BLK127_TRACE_IDENTITIES:
        raise ValueError("request package must match canonical BLK-127 trace identities")
    _required_exact_set(normalized.get("proof_obligations"), BLK127_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK127_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    for flag in BLK127_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"request_package {flag} must remain false")
    return normalized


def _validate_decision(decision: Any, request_pkg: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise ValueError("approval_decision must be a dictionary")
    unknown = sorted(set(decision) - _DECISION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = deepcopy(decision)

    _reject_laundered_decision_string(str(normalized.get("approval_decision_package_id", "")), "approval_decision_package_id")
    if normalized.get("approval_decision_package_id") != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError(f"approval_decision_package_id must be {APPROVAL_DECISION_PACKAGE_ID}")
    _reject_laundered_decision_string(str(normalized.get("operator_identity", "")), "operator_identity")
    if normalized.get("operator_identity") != request_pkg["operator_identity"]:
        raise ValueError("operator_identity must match BLK-127 request package")
    raw_text = _required_string(normalized.get("operator_approval_text_raw"), "operator_approval_text_raw")
    if raw_text != OPERATOR_APPROVAL_TEXT_RAW:
        _reject_laundered_decision_string(raw_text, "operator_approval_text_raw")
        raise ValueError("operator_approval_text_raw must match exact BLK-SYSTEM-128 operator approval text")
    if normalized.get("operator_approved_request_package_id_normalized") != BLK127_REQUEST_PACKAGE_ID:
        raise ValueError("operator_approved_request_package_id_normalized must match BLK-127 request package")
    if normalized.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if normalized.get("upstream_request_package_id") != request_pkg["request_package_id"]:
        raise ValueError("upstream_request_package_id must match BLK-127 request package")
    if normalized.get("upstream_request_package_hash") != request_pkg["request_package_hash"]:
        raise ValueError("upstream_request_package_hash must match BLK-127 request package")
    if normalized.get("upstream_request_status") != request_pkg["request_status"]:
        raise ValueError("upstream_request_status must match BLK-127 request package")
    if normalized.get("exact_upstream_decision_id") != request_pkg["upstream_decision_id"]:
        raise ValueError("exact_upstream_decision_id must match BLK-127 request package")
    if normalized.get("exact_upstream_decision_gate_hash") != request_pkg["upstream_decision_gate_hash"]:
        raise ValueError("exact_upstream_decision_gate_hash must match BLK-127 request package")
    if normalized.get("exact_upstream_interface_id") != request_pkg["upstream_interface_id"]:
        raise ValueError("exact_upstream_interface_id must match BLK-127 request package")
    if normalized.get("exact_upstream_interface_hash") != request_pkg["upstream_interface_hash"]:
        raise ValueError("exact_upstream_interface_hash must match BLK-127 request package")
    if normalized.get("exact_beo_id") != request_pkg["beo_id"]:
        raise ValueError("exact_beo_id must match BLK-127 request package")
    if normalized.get("exact_beb_id") != request_pkg["beb_id"]:
        raise ValueError("exact_beb_id must match BLK-127 request package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != request_pkg["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-127 request package")

    consumed_ids = {
        request_pkg["request_package_id"],
        request_pkg["upstream_decision_id"],
        request_pkg["upstream_interface_id"],
        request_pkg["beo_id"],
        request_pkg["beb_id"],
    }
    if normalized.get("approval_id") in consumed_ids:
        raise ValueError("approval_id must be fresh")
    if normalized.get("future_publication_execution_run_id") in consumed_ids or normalized.get(
        "future_publication_execution_run_id"
    ) == normalized.get("approval_id"):
        raise ValueError("future_publication_execution_run_id must be fresh")
    if normalized.get("approval_id") != APPROVAL_ID:
        raise ValueError(f"approval_id must be {APPROVAL_ID}")
    if normalized.get("future_publication_execution_run_id") != FUTURE_PUBLICATION_EXECUTION_RUN_ID:
        raise ValueError(f"future_publication_execution_run_id must be {FUTURE_PUBLICATION_EXECUTION_RUN_ID}")
    if normalized.get("decision_result") != DECISION_RESULT:
        _reject_laundered_decision_string(str(normalized.get("decision_result", "")), "decision_result")
        raise ValueError(f"decision_result must be {DECISION_RESULT}")

    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(normalized.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    normalized["operator_attestation"] = _validate_attestation(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    normalized["excluded_authorities"] = _required_exact_set(normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
        normalized[flag] = False
    return normalized


_EXTRA_DECISION_AUTHORITY_MARKERS = (
    "publicationauthorized",
    "publicationauthorised",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "publicationexecuted",
    "publicationperformed",
    "beoispublished",
    "publishedbeooutput",
    "externalpublicationperformed",
    "externalpublicationexecuted",
    "signinggranted",
    "signingauthorized",
    "signatureauthorized",
    "signergranted",
    "signerauthorized",
    "generatertm",
    "rtmgenerationauthorized",
    "rtmgenerationgranted",
    "protectedbodyreadsauthorized",
)


def _reject_laundered_decision_string(text: str, field: str) -> None:
    _reject_laundered_string(text, field)
    for variant in _decoded_variants(str(text)):
        compact = "".join(ch for ch in variant.casefold() if ch.isalnum())
        for marker in _EXTRA_DECISION_AUTHORITY_MARKERS:
            if marker in compact:
                raise ValueError(f"authority-laundering text in {field}")


def _validate_attestation(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown = sorted(set(value) - _ATTESTATION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized
