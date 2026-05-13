"""BLK-SYSTEM-099 external BEO publication approval-decision capture.

This fixture records the operator's exact approval decision for the exact
BLK-SYSTEM-098 prerequisite request package. It reserves one future external BEO
publication execution run ID, but does not publish, sign, write immutable
storage, mutate a ledger, execute rollback/revocation/supersession, generate RTM,
perform drift rejection, read protected BLK-req bodies, scan/mutate target repos,
mutate source/Git, run BLK-pipe/BLK-test/Codex/tooling, or claim production
isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_prerequisite_request_after_evidence_refresh import (
    BEO_HASH,
    BEO_ID,
    BLK097_TARGET_HEAD,
    BLK097_TARGET_REPO_PATH,
    CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
    CANONICAL_BLK097_EVIDENCE_HASH,
    EXACT_EXCLUDED_AUTHORITIES as BLK098_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK098_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK098_NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID as BLK098_REQUEST_PACKAGE_ID,
    REQUEST_SCOPE as BLK098_REQUEST_SCOPE,
    REQUEST_STATUS as BLK098_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK098_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK098_SIDE_EFFECT_FLAGS,
    _decoded_variants,
    _enforce_allowed_keys,
    _normalize_authority_text,
    _parse_timestamp,
    _require_dict,
    _required_false,
    _scan_string as _scan_blk098_string,
    _validate_exact_string_set,
)

STATUS = "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_BLK098_REQUEST_NOT_PUBLISHED"
APPROVAL_DECISION_PACKAGE_ID = "BEO-PUBLICATION-APPROVAL-DECISION-099-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001"
FUTURE_PUBLICATION_EXECUTION_RUN_ID = "RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001"
SELECTED_FRONTIER = "external_beo_publication_approval_decision_capture"
DECISION_SCOPE = "EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_ONLY_NOT_PUBLICATION_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_EXTERNAL_BEO_PUBLICATION_EXECUTION_NOT_PUBLISHED"
NEXT_REQUIRED_AUTHORITY = "SEPARATELY_SCOPED_EXTERNAL_BEO_PUBLICATION_EXECUTION_REQUIRED_NOT_RUN"
OPERATOR_APPROVAL_TEXT_RAW = (
    "I approve external BEO publication for "
    "BEO-PUBLICATION-PREREQUISITE-REQUEST-098- 001 under BLK-SYSTEM-099"
)
CANONICAL_BLK098_REQUEST_PACKAGE_HASH = "sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T19:10:00+10:00")

SIDE_EFFECT_FLAGS = (
    "future_publication_execution_run_id_consumed",
    "external_authoritative_publication_performed",
    "runtime_published_beo_output",
    "publication_execution_performed",
    "signer_key_material_accessed",
    "cryptographic_signature_generated",
    "immutable_storage_written",
    "public_ledger_mutated",
    "ledger_append_attempted",
    "rollback_executed",
    "revocation_executed",
    "supersession_executed",
    "rtm_generated",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "protected_body_read",
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
    "PUBLICATION_AUTHORIZED_MARKER_OUTSIDE_BLK099_DECISION_RECORD",
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
    "PROTECTED_BLK_REQ_BODY_READ",
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
    "BLK098_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK098_REQUEST_STATUS_NOT_GRANTED_BOUND",
    "HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_CAPTURED_FOR_EXACT_REQUEST",
    "OPERATOR_RAW_TEXT_AND_NORMALIZED_REQUEST_ID_BOUND",
    "APPROVAL_ID_RESERVED_FOR_BLK099_DECISION",
    "FUTURE_PUBLICATION_EXECUTION_RUN_ID_RESERVED_NOT_CONSUMED",
    "EXTERNAL_PUBLICATION_NOT_EXECUTED_BY_APPROVAL_DECISION",
    "PUBLICATION_AUTHORIZED_AND_SIGNING_GRANTED_MARKERS_REJECTED_OUTSIDE_RECORD",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "TARGET_REPO_AND_SOURCE_GIT_MUTATION_EXCLUDED",
    "BLK_PIPE_BLK_TEST_CODEX_TOOLING_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_EXTERNAL_PUBLICATION_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = {
    "request_status",
    "request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "next_required_authority",
    "upstream_blk097_evidence_hash",
    "upstream_blk087_execution_package_id",
    "upstream_blk087_execution_package_hash",
    "upstream_blk087_pilot_artifact_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path",
    "target_head_sha",
    "future_external_publication_decision_requested",
    "external_publication_approval_granted",
    "blk097_evidence_summary",
    "blk087_trace_artifacts",
    "operator_attestation",
    "proof_obligations",
    "excluded_authorities",
    "request_package_hash",
    *BLK098_SIDE_EFFECT_FLAGS,
}

_DECISION_KEYS = {
    "approval_decision_package_id",
    "operator_identity",
    "operator_approval_text_raw",
    "operator_approved_request_package_id_normalized",
    "decision_scope",
    "selected_frontier",
    "upstream_request_package_id",
    "upstream_request_package_hash",
    "upstream_request_status",
    "exact_beo_id",
    "exact_beo_hash",
    "exact_target_repo_path",
    "exact_target_head_sha",
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

_ATTESTATION_KEYS = {
    "exact_blk098_request_reviewed",
    "operator_text_normalized_to_exact_request_id",
    "approval_limited_to_one_future_external_publication_execution_sprint",
    "external_publication_not_executed_by_this_decision",
    "future_run_id_reserved_not_consumed",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "rtm_generation_and_drift_excluded",
    "protected_body_reads_excluded",
    "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
}

_EXTRA_FORBIDDEN_COMPACT_TOKENS = (
    "publicationauthorized",
    "publicationauthorised",
    "beopublicationauthorized",
    "beopublicationauthorised",
    "publicationisconfirmed",
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
    "rtmgenerationauthorized",
    "rtmgenerationgranted",
    "protectedbodyreadsauthorized",
)

_EXTRA_FORBIDDEN_NORMALIZED_TOKENS = (
    "publication authorized",
    "publication authorised",
    "beo publication authorized",
    "beo publication authorised",
    "publication is confirmed",
    "publication executed",
    "publication performed",
    "beo is published",
    "external publication performed",
    "external publication executed",
    "signing granted",
    "signing authorized",
    "signature authorized",
    "signer granted",
    "signer authorized",
    "rtm generation authorized",
    "rtm generation granted",
    "protected body reads authorized",
)


def build_beo_external_publication_approval_decision(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Build an exact approval decision package without publication execution."""

    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    operator_attestation = deepcopy(decision["operator_attestation"])
    package = {
        "approval_decision_status": STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "operator_approval_text_raw": OPERATOR_APPROVAL_TEXT_RAW,
        "operator_approved_request_package_id_normalized": BLK098_REQUEST_PACKAGE_ID,
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "decision_result": DECISION_RESULT,
        "upstream_request_package_id": request["request_package_id"],
        "upstream_request_package_hash": request["request_package_hash"],
        "upstream_request_status": request["request_status"],
        "upstream_blk097_evidence_hash": request["upstream_blk097_evidence_hash"],
        "upstream_blk087_execution_package_id": request["upstream_blk087_execution_package_id"],
        "upstream_blk087_execution_package_hash": request["upstream_blk087_execution_package_hash"],
        "upstream_blk087_pilot_artifact_hash": request["upstream_blk087_pilot_artifact_hash"],
        "beo_id": request["beo_id"],
        "beo_hash": request["beo_hash"],
        "target_repo_path": request["target_repo_path"],
        "target_head_sha": request["target_head_sha"],
        "approval_id": APPROVAL_ID,
        "future_publication_execution_run_id": FUTURE_PUBLICATION_EXECUTION_RUN_ID,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "approval_decision_captured": True,
        "human_external_beo_publication_approval_granted": True,
        "future_external_beo_publication_execution_approved": True,
        "beo_publication_status": "APPROVAL_DECISION_CAPTURED_NOT_PUBLISHED",
        "rtm_status": "NOT_GENERATED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": operator_attestation,
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_decision_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_decision_package_hash"}
    )
    return package


def _validate_request_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "request_package")
    _enforce_allowed_keys(package, _REQUEST_PACKAGE_KEYS, "request_package")
    submitted_hash = package.get("request_package_hash")
    if not isinstance(submitted_hash, str):
        raise ValueError("request_package_hash must be a sha256 hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("request_package_hash does not match submitted BLK-098 package")

    if package.get("request_status") != BLK098_REQUEST_STATUS:
        raise ValueError("request package must be BLK-098 prerequisite request-ready")
    if package.get("request_package_id") != BLK098_REQUEST_PACKAGE_ID:
        raise ValueError("request_package_id must match BLK-098")
    if package.get("request_scope") != BLK098_REQUEST_SCOPE:
        raise ValueError("request_scope must remain BLK-098 review-only")
    if package.get("selected_frontier") != BLK098_SELECTED_FRONTIER:
        raise ValueError("selected_frontier must remain BLK-098 prerequisite request frontier")
    if package.get("next_required_authority") != BLK098_NEXT_REQUIRED_AUTHORITY:
        raise ValueError("BLK-098 request must still require external BEO publication approval")
    if package.get("future_external_publication_decision_requested") is not True:
        raise ValueError("BLK-098 request must request a future external publication decision")
    if package.get("external_publication_approval_granted") is not False:
        raise ValueError("BLK-098 request must remain not granted")

    canonical_values = {
        "upstream_blk097_evidence_hash": CANONICAL_BLK097_EVIDENCE_HASH,
        "upstream_blk087_execution_package_id": "BEO-PUBLICATION-PILOT-EXECUTION-087-001",
        "upstream_blk087_execution_package_hash": CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
        "upstream_blk087_pilot_artifact_hash": CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
        "beo_id": BEO_ID,
        "beo_hash": BEO_HASH,
        "target_repo_path": BLK097_TARGET_REPO_PATH,
        "target_head_sha": BLK097_TARGET_HEAD,
    }
    for key, expected in canonical_values.items():
        if package.get(key) != expected:
            raise ValueError("request package must match canonical BLK-098 prerequisite package")

    for flag in BLK098_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_string_set(package.get("proof_obligations"), BLK098_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _validate_exact_string_set(
        package.get("excluded_authorities"),
        BLK098_EXCLUDED_AUTHORITIES,
        "request_package excluded_authorities",
        denied=True,
    )
    if submitted_hash != CANONICAL_BLK098_REQUEST_PACKAGE_HASH:
        raise ValueError("request package must match canonical BLK-098 prerequisite package")
    return package


def _validate_decision(decision: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    _require_dict(decision, "approval_decision")
    _enforce_allowed_keys(decision, _DECISION_KEYS, "approval_decision")

    _scan_099_string(str(decision.get("approval_decision_package_id", "")), "approval_decision_package_id")
    if decision.get("approval_decision_package_id") != APPROVAL_DECISION_PACKAGE_ID:
        raise ValueError(f"approval_decision_package_id must be {APPROVAL_DECISION_PACKAGE_ID}")

    _scan_099_string(str(decision.get("operator_identity", "")), "operator_identity")
    if decision.get("operator_identity") != request["operator_identity"]:
        raise ValueError("operator_identity must match BLK-098 request package")

    _scan_099_string(str(decision.get("operator_approval_text_raw", "")), "operator_approval_text_raw")
    if decision.get("operator_approval_text_raw") != OPERATOR_APPROVAL_TEXT_RAW:
        raise ValueError("operator_approval_text_raw must match exact BLK-SYSTEM-099 operator approval text")
    if decision.get("operator_approved_request_package_id_normalized") != BLK098_REQUEST_PACKAGE_ID:
        raise ValueError("operator_approved_request_package_id_normalized must match BLK-098 request package")
    if decision.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if decision.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if decision.get("upstream_request_package_id") != request["request_package_id"]:
        raise ValueError("upstream_request_package_id must match BLK-098 request package")
    if decision.get("upstream_request_package_hash") != request["request_package_hash"]:
        raise ValueError("upstream_request_package_hash must match BLK-098 request package")
    if decision.get("upstream_request_status") != request["request_status"]:
        raise ValueError("upstream_request_status must match BLK-098 request package")
    if decision.get("exact_beo_id") != request["beo_id"]:
        raise ValueError("exact_beo_id must match BLK-098 request package")
    if decision.get("exact_beo_hash") != request["beo_hash"]:
        raise ValueError("exact_beo_hash must match BLK-098 request package")
    if decision.get("exact_target_repo_path") != request["target_repo_path"]:
        raise ValueError("exact_target_repo_path must match BLK-098 request package")
    if decision.get("exact_target_head_sha") != request["target_head_sha"]:
        raise ValueError("exact_target_head_sha must match BLK-098 request package")

    consumed_ids = {
        request["request_package_id"],
        request["upstream_blk087_execution_package_id"],
        request["beo_id"],
        request["target_head_sha"],
    }
    if decision.get("approval_id") in consumed_ids:
        raise ValueError("approval_id must be fresh")
    if decision.get("future_publication_execution_run_id") in consumed_ids or decision.get(
        "future_publication_execution_run_id"
    ) == decision.get("approval_id"):
        raise ValueError("future_publication_execution_run_id must be fresh")
    if decision.get("approval_id") != APPROVAL_ID:
        raise ValueError(f"approval_id must be {APPROVAL_ID}")
    if decision.get("future_publication_execution_run_id") != FUTURE_PUBLICATION_EXECUTION_RUN_ID:
        raise ValueError(f"future_publication_execution_run_id must be {FUTURE_PUBLICATION_EXECUTION_RUN_ID}")
    if decision.get("decision_result") != DECISION_RESULT:
        _scan_099_string(str(decision.get("decision_result", "")), "decision_result")
        raise ValueError(f"decision_result must be {DECISION_RESULT}")

    for flag in ("expired", "replayed", "stale"):
        if decision.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(decision.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(decision.get("expires_at"), "expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")

    for flag in SIDE_EFFECT_FLAGS:
        _required_false(decision.get(flag), flag)
    _validate_attestation(decision.get("operator_attestation"))
    _validate_exact_string_set(decision.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_string_set(
        decision.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities", denied=True
    )
    return decision


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_allowed_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _scan_099_string(value: str, label: str) -> None:
    _scan_blk098_string(value, label)
    for candidate in _decoded_variants(str(value)):
        normalized = _normalize_authority_text(candidate)
        compact = "".join(char for char in str(candidate).casefold() if char.isalnum())
        for token in _EXTRA_FORBIDDEN_NORMALIZED_TOKENS:
            if _normalize_authority_text(token) in normalized:
                raise ValueError(f"authority-laundering text at {label}: {token}")
        for token in _EXTRA_FORBIDDEN_COMPACT_TOKENS:
            if token in compact:
                raise ValueError(f"authority-laundering text at {label}: {token}")
