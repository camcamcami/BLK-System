"""BLK-SYSTEM-101 RTM trace-closure authority request after BLK-100.

This deterministic request fixture binds the exact BLK-SYSTEM-100 external BEO
publication record and packages one future local `blk-link` / RTM trace-closure
execution authority request. It does not capture approval, execute trace closure,
generate RTM, reject drift, compare active-vault hashes, read protected bodies,
mutate target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim
production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash

REQUEST_STATUS = "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED"
AUTHORITY_REQUEST_PACKAGE_ID = "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-101-001"
SELECTED_FRONTIER = "rtm_trace_closure_authority_request_after_external_beo_publication"
REQUEST_SCOPE = "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_EXTERNAL_BEO_PUBLICATION_REVIEW_ONLY"
NEXT_REQUIRED_AUTHORITY = "EXACT_RTM_TRACE_CLOSURE_APPROVAL_DECISION_REQUIRED_NOT_CAPTURED"
CANONICAL_BLK100_EXECUTION_PACKAGE_HASH = "sha256:5269146b6b46e27e38878a327b1ac6180068d5c9e427067604b611512a72289d"
CANONICAL_BLK100_PUBLICATION_RECORD_HASH = "sha256:1efbfd9b6b9d828b7b793c1c9c2b0f8115c36db69ef850e5a2f2ff94195923b4"
CANONICAL_BEO_ID = "BEO-054-001"
CANONICAL_BEO_HASH = "sha256:" + "a" * 64
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T20:50:00+10:00")

SIDE_EFFECT_FLAGS = (
    "human_rtm_trace_closure_approval_granted",
    "rtm_trace_closure_authorized",
    "rtm_trace_closure_executed",
    "rtm_generated",
    "rtm_drift_rejection_authorized",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "protected_body_reads",
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "beb_dispatch_authorized",
    "beo_closeout_execution_authorized",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

EXACT_EXCLUDED_AUTHORITIES = {
    "HUMAN_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
    "RUNTIME_RTM_TRACE_CLOSURE_EXECUTION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ",
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
    "BLK_PIPE_EXECUTION",
    "BLK_TEST_RUNTIME_EXECUTION",
    "PRODUCTION_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK100_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK100_PUBLICATION_RECORD_HASH_BOUND",
    "EXTERNAL_BEO_PUBLICATION_RECORD_CONSUMED_AS_PREREQUISITE_ONLY",
    "RTM_TRACE_CLOSURE_AUTHORITY_REQUESTED_FOR_FUTURE_REVIEW_NOT_GRANTED",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED_UNTIL_SEPARATE_EXECUTION",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_TRACE_CLOSURE_EXECUTION",
}

_REQUEST_KEYS = {
    "authority_request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_execution_package_id",
    "upstream_execution_package_hash",
    "publication_record_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path_metadata_only",
    "target_head_sha_metadata_only",
    "request_future_exact_rtm_trace_closure_authority",
    "requested_at",
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
    "exact_blk100_publication_execution_reviewed",
    "external_beo_publication_record_is_hash_bound",
    "request_is_for_future_trace_closure_authority_not_execution",
    "rtm_generation_not_performed_by_request",
    "drift_rejection_excluded",
    "active_vault_hash_comparison_excluded",
    "protected_body_reads_excluded",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "target_source_git_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_BLK100_KEYS = {
    "execution_status",
    "execution_package_id",
    "execution_package_hash",
    "publication_record_hash",
    "publication_record",
    "beo_id",
    "beo_hash",
    "run_id_consumed",
    "beo_publication",
    "rtm_status",
    "target_repo_path",
    "target_head_sha",
    "external_beo_publication_executed",
    "future_publication_execution_run_id_consumed",
}

_FORBIDDEN_TOKENS = (
    "rtmgenerated",
    "rtmgenerationauthorized",
    "rtmdriftrejection",
    "driftdecision",
    "driftrejectionauthorized",
    "activevaulthashcomparison",
    "protectedbodyread",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "signaturegenerated",
    "cryptographicsigning",
    "signerkeymaterial",
    "keymaterial",
    "privatekey",
    "apikey",
    "immutablestoragewrite",
    "publicledgermutation",
    "publicledgerappend",
    "rollbackexecuted",
    "revocationexecuted",
    "supersessionexecuted",
    "targetreposcan",
    "targetrepomutation",
    "sourcemutationauthorized",
    "gitmutationauthorized",
    "bebdispatch",
    "beocloseoutexecution",
    "blkpipeexecution",
    "blktestruntime",
    "livecodexexecution",
    "packagemanagerauthorized",
    "networkaccessauthorized",
    "modelserviceauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionisolationclaimed",
    "runblksystem100externalbeopublication001",
)


def build_rtm_trace_closure_authority_request(
    blk100_execution_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a BLK-SYSTEM-101 request package from the exact BLK-100 artifact."""

    upstream = _validate_blk100_execution_package(blk100_execution_package)
    request = _validate_authority_request(authority_request, upstream)
    package = {
        "request_status": REQUEST_STATUS,
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beo_hash": upstream["beo_hash"],
        "target_repo_path_metadata_only": upstream["publication_record"]["target_repo_path_metadata_only"],
        "target_head_sha_metadata_only": upstream["publication_record"]["target_head_sha_metadata_only"],
        "requested_authority": "ONE_FUTURE_LOCAL_RTM_TRACE_CLOSURE_EXECUTION",
        "request_future_exact_rtm_trace_closure_authority": True,
        "rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_attestation": deepcopy(request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


def _validate_blk100_execution_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "blk100_execution_package")
    missing = _BLK100_KEYS - set(package)
    if missing:
        raise ValueError(f"blk100_execution_package missing keys: {sorted(missing)}")
    submitted_hash = package.get("execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("execution_package_hash does not match submitted BLK-100 package")
    expected = {
        "execution_status": "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY",
        "execution_package_id": "BEO-PUBLICATION-EXECUTION-100-001",
        "execution_package_hash": CANONICAL_BLK100_EXECUTION_PACKAGE_HASH,
        "publication_record_hash": CANONICAL_BLK100_PUBLICATION_RECORD_HASH,
        "beo_id": CANONICAL_BEO_ID,
        "beo_hash": CANONICAL_BEO_HASH,
        "run_id_consumed": "RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001",
        "beo_publication": "PUBLISHED_EXTERNAL_BEO_RECORD",
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("BLK-100 package must match canonical BLK-100 publication execution record")
    record = package.get("publication_record")
    _require_dict(record, "publication_record")
    if record.get("publication_record_hash") != CANONICAL_BLK100_PUBLICATION_RECORD_HASH:
        raise ValueError("publication_record_hash must match canonical BLK-100 publication record")
    if record.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("BLK-100 publication record must not have generated RTM")
    for key in ("rtm_generated", "protected_body_read", "active_vault_hash_comparison_performed"):
        if package.get(key) is not False:
            raise ValueError(f"BLK-100 package {key} must remain false")
    return package


def _validate_authority_request(request: dict[str, Any], upstream: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "authority_request")
    _enforce_exact_keys(request, _REQUEST_KEYS, "authority_request")
    for string_key in (
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beo_hash",
        "target_repo_path_metadata_only",
        "target_head_sha_metadata_only",
    ):
        _scan_value_strings(request.get(string_key), f"authority_request.{string_key}")
    expected = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": "discord:684235178083745819",
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beo_hash": upstream["beo_hash"],
        "target_repo_path_metadata_only": upstream["publication_record"]["target_repo_path_metadata_only"],
        "target_head_sha_metadata_only": upstream["publication_record"]["target_head_sha_metadata_only"],
    }
    for key, value in expected.items():
        if request.get(key) != value:
            raise ValueError(f"{key} must match canonical BLK-100 publication execution record")
    if request.get("request_future_exact_rtm_trace_closure_authority") is not True:
        raise ValueError("request_future_exact_rtm_trace_closure_authority must be true")
    for flag in SIDE_EFFECT_FLAGS:
        if request.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"authority request must not be {flag}")
    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("authority request must not be calendar-expired")
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    return request


def _validate_attestation(attestation: Any) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_exact_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    _scan_value_strings(attestation, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _validate_exact_set(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{label} must match exact set")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{label} must match exact set")
    if len(value) != len(set(value)) or set(value) != expected:
        raise ValueError(f"{label} must match exact set")


def _scan_value_strings(value: Any, label: str) -> None:
    if isinstance(value, str):
        _scan_string(value, label)
        return
    if isinstance(value, dict):
        for key, nested in value.items():
            _scan_value_strings(nested, f"{label}.{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_value_strings(nested, f"{label}[{index}]")


def _scan_string(value: str, label: str) -> None:
    for candidate in _decoded_variants(value):
        compact = "".join(char for char in candidate.casefold() if char.isalnum())
        for token in _FORBIDDEN_TOKENS:
            if token in compact:
                if token == "runblksystem100externalbeopublication001":
                    raise ValueError(f"authority-laundering text at {label}: RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001")
                raise ValueError(f"authority-laundering text at {label}: {token}")


def _decoded_variants(value: str) -> list[str]:
    variants = [value]
    current = value
    for _ in range(3):
        decoded = unquote(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return parsed


def _require_dict(value: Any, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a dict")


def _enforce_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    extras = set(value) - expected
    missing = expected - set(value)
    if extras or missing:
        raise ValueError(f"{label} keys must match exact schema; extras={sorted(extras)} missing={sorted(missing)}")
