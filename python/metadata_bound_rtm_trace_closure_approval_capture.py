"""BLK-SYSTEM-131 metadata-bound RTM trace-closure approval capture.

This deterministic fixture captures the human/operator approval decision for the
exact BLK-SYSTEM-130 RTM trace-closure authority request. It reserves one future
local, non-authoritative RTM trace-closure run ID but does not consume that run,
execute trace closure, authorize production blk-link, generate RTM, reject drift,
compare active-vault hashes, establish coverage truth, read protected bodies,
mutate target/source/Git state, run BLK-pipe/BLK-test/Codex/tooling, or claim
production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_trace_closure_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID as BLK130_AUTHORITY_REQUEST_PACKAGE_ID,
    CANONICAL_BLK129_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK129_PUBLICATION_RECORD_HASH,
    CANONICAL_BEB_ID,
    CANONICAL_BEO_ID,
    CANONICAL_TRACE_IDENTITIES,
    EXACT_EXCLUDED_AUTHORITIES as BLK130_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK130_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK130_NEXT_REQUIRED_AUTHORITY,
    REQUEST_SCOPE as BLK130_REQUEST_SCOPE,
    REQUEST_STATUS as BLK130_REQUEST_STATUS,
    SELECTED_FRONTIER as BLK130_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK130_SIDE_EFFECT_FLAGS,
)

STATUS = "RTM_TRACE_CLOSURE_APPROVAL_CAPTURED_FOR_EXACT_BLK130_REQUEST_NOT_EXECUTED"
APPROVAL_CAPTURE_PACKAGE_ID = "RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001"
APPROVAL_ID = "APPROVAL-BLK-SYSTEM-130-RTM-TRACE-CLOSURE-001"
FUTURE_RUN_ID = "RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001"
SELECTED_FRONTIER = "metadata_bound_rtm_trace_closure_approval_capture"
DECISION_SCOPE = "RTM_TRACE_CLOSURE_APPROVAL_CAPTURE_ONLY_NOT_EXECUTION"
DECISION_RESULT = "APPROVED_FOR_ONE_FUTURE_LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_EXECUTION_NOT_EXECUTED"
NEXT_REQUIRED_AUTHORITY = "EXACT_LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_EXECUTION_REQUIRED_NOT_RUN"
CANONICAL_BLK130_REQUEST_PACKAGE_HASH = "sha256:cf59f9360d79226ff89e9743ea49b7824b0852908422c6de005ca7f9580a68b2"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T12:03:39+10:00")

SIDE_EFFECT_FLAGS = (
    "rtm_trace_closure_executed",
    "production_blk_link_authorized",
    "production_blk_link_executed",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "active_vault_hash_comparison_performed",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
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
    "RUNTIME_RTM_TRACE_CLOSURE_EXECUTION_THIS_SPRINT",
    "PRODUCTION_OR_REUSABLE_BLK_LINK_EXECUTION",
    "RUNTIME_RTM_GENERATION_THIS_SPRINT",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
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
    "GENERIC_BLK_TEST_MCP",
    "LIVE_CODEX_EXECUTION",
    "ARBITRARY_SHELL_OR_CALLER_SUPPLIED_COMMANDS",
    "PACKAGE_MANAGER_NETWORK_MODEL_BROWSER_OR_CYBER_TOOLING",
    "PRODUCTION_SANDBOX_OR_HOST_SECRET_ISOLATION_CLAIM",
}

EXACT_PROOF_OBLIGATIONS = {
    "BLK130_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK129_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK130",
    "HUMAN_RTM_TRACE_CLOSURE_APPROVAL_CAPTURED_FOR_EXACT_REQUEST",
    "APPROVAL_ID_RESERVED_FOR_BLK130_TRACE_CLOSURE",
    "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
    "TRACE_CLOSURE_NOT_EXECUTED_BY_APPROVAL_CAPTURE",
    "PRODUCTION_BLK_LINK_NOT_AUTHORIZED",
    "RTM_GENERATION_NOT_PERFORMED_BY_APPROVAL_CAPTURE",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_TRACE_CLOSURE_EXECUTION",
}

_REQUEST_PACKAGE_KEYS = frozenset(
    {
        "request_status",
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "requested_authority",
        "request_future_exact_rtm_trace_closure_approval",
        "rtm_trace_closure_authority",
        "next_required_authority",
        "authority_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "authority_request_package_hash",
        *BLK130_SIDE_EFFECT_FLAGS,
    }
)

_DECISION_KEYS = frozenset(
    {
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "approval_id",
        "future_run_id",
        "decision_result",
        "decided_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_approval_text_raw",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk130_request_reviewed",
        "approval_limited_to_one_future_local_non_authoritative_trace_closure_execution",
        "future_run_id_reserved_not_consumed",
        "trace_closure_not_executed_by_this_decision",
        "production_blk_link_not_authorized",
        "rtm_generation_not_performed_by_this_decision",
        "drift_rejection_excluded",
        "active_vault_hash_comparison_excluded",
        "coverage_truth_excluded",
        "protected_body_reads_excluded",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)

_FORBIDDEN_COMPACT_TOKENS = (
    "rtmgenerated",
    "rtmgenerationauthorized",
    "rtmgenerationgranted",
    "productionblklinkauthorized",
    "productionblklinkexecuted",
    "productionblklinkexecution",
    "runtimeblklinktraceclosureauthorized",
    "runtimeblklinktraceclosureexecuted",
    "authoritativetraceclosure",
    "rtmdriftrejection",
    "driftdecision",
    "driftrejectionauthorized",
    "activevaulthashcomparison",
    "coverageclaimpromoted",
    "coveragematrixgenerated",
    "coveragetruthestablished",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "protectedbodyread",
    "protectedbodycopy",
    "protectedbodyhash",
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
    "sourcemutationattempted",
    "gitmutationauthorized",
    "bebdispatch",
    "beocloseoutexecution",
    "blkpipeexecution",
    "blktestruntime",
    "livecodexexecution",
    "packagemanagerauthorized",
    "packagemanagersauthorized",
    "networkaccessauthorized",
    "modelserviceauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionisolationclaimed",
)
_BODY_TEXT_TOKENS = ("thesystemshall", "theusershall", "shall")


def build_metadata_bound_rtm_trace_closure_approval_capture(
    request_package: dict[str, Any], approval_decision: dict[str, Any]
) -> dict[str, Any]:
    """Capture exact BLK-SYSTEM-131 approval for the BLK-130 request only."""

    request = _validate_request_package(request_package)
    decision = _validate_decision(approval_decision, request)
    trace_identities = list(request["exact_trace_identities"])
    decision_hash = _canonical_hash(decision)
    package = {
        "approval_capture_status": STATUS,
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "publication_record_hash": request["publication_record_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "exact_trace_identities": trace_identities,
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decision_hash": decision_hash,
        "decided_at": decision["decided_at"],
        "expires_at": decision["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "approval_decision_captured": True,
        "human_rtm_trace_closure_approval_granted": True,
        "future_local_rtm_trace_closure_execution_approved": True,
        "future_run_id_consumed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "operator_approval_text_raw": decision["operator_approval_text_raw"],
        "operator_attestation": deepcopy(decision["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["approval_capture_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_capture_package_hash"}
    )
    return package


def _validate_request_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("request_package must be a dictionary")
    unknown = sorted(set(package) - _REQUEST_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"request_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"request_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("authority_request_package_hash"), "authority_request_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "authority_request_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("authority_request_package_hash does not match submitted BLK-130 package")
    if submitted_hash != CANONICAL_BLK130_REQUEST_PACKAGE_HASH:
        raise ValueError("request package must match canonical BLK-130 authority request")
    expected = {
        "request_status": BLK130_REQUEST_STATUS,
        "authority_request_package_id": BLK130_AUTHORITY_REQUEST_PACKAGE_ID,
        "request_scope": BLK130_REQUEST_SCOPE,
        "selected_frontier": BLK130_SELECTED_FRONTIER,
        "upstream_execution_package_id": "BEO-PUBLICATION-EXECUTION-129-001",
        "upstream_execution_package_hash": CANONICAL_BLK129_EXECUTION_PACKAGE_HASH,
        "publication_record_hash": CANONICAL_BLK129_PUBLICATION_RECORD_HASH,
        "beo_id": CANONICAL_BEO_ID,
        "beb_id": CANONICAL_BEB_ID,
        "requested_authority": "ONE_FUTURE_LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_APPROVAL",
        "rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": BLK130_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("request package must match canonical BLK-130 authority request")
    if tuple(_validate_exact_trace_identities(normalized.get("exact_trace_identities"))) != CANONICAL_TRACE_IDENTITIES:
        raise ValueError("request package trace identities must match canonical BLK-130 request")
    if normalized.get("request_future_exact_rtm_trace_closure_approval") is not True:
        raise ValueError("BLK-130 request must request future trace-closure approval")
    for flag in BLK130_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"request package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK130_PROOF_OBLIGATIONS, "request_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK130_EXCLUDED_AUTHORITIES, "request_package excluded_authorities")
    return normalized


def _validate_decision(decision: Any, request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise ValueError("approval_decision must be a dictionary")
    unknown = sorted(set(decision) - _DECISION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_DECISION_KEYS - set(decision))
    if missing:
        raise ValueError(f"approval_decision missing field {missing[0]!r}")
    normalized = deepcopy(decision)
    for key in (
        "approval_capture_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "approval_id",
        "future_run_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("approval_capture_package_id") != APPROVAL_CAPTURE_PACKAGE_ID:
        raise ValueError(f"approval_capture_package_id must be {APPROVAL_CAPTURE_PACKAGE_ID}")
    if normalized.get("operator_identity") != request["operator_identity"]:
        raise ValueError("operator_identity must match BLK-130 request package")
    if normalized.get("decision_scope") != DECISION_SCOPE:
        raise ValueError(f"decision_scope must be {DECISION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    expected = {
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_execution_package_id": request["upstream_execution_package_id"],
        "upstream_execution_package_hash": request["upstream_execution_package_hash"],
        "publication_record_hash": request["publication_record_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-130 request package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != request["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-130 request package")
    if normalized.get("approval_id") != APPROVAL_ID:
        raise ValueError(f"approval_id must be {APPROVAL_ID}")
    if normalized.get("future_run_id") != FUTURE_RUN_ID:
        raise ValueError(f"future_run_id must be {FUTURE_RUN_ID}")
    if normalized.get("decision_result") != DECISION_RESULT:
        raise ValueError(f"decision_result must be {DECISION_RESULT}")
    _scan_value_strings(normalized.get("decision_result"), "decision_result")
    _scan_value_strings(normalized.get("operator_approval_text_raw"), "operator_approval_text_raw")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"approval decision must not be {flag}")
    decided_at = _parse_timestamp(normalized.get("decided_at"), "decided_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    request_start = _parse_timestamp(request.get("requested_at"), "request.requested_at")
    request_expiry = _parse_timestamp(request.get("expires_at"), "request.expires_at")
    if expires_at <= decided_at:
        raise ValueError("expires_at must be after decided_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("approval decision must not be calendar-expired")
    if decided_at < request_start:
        raise ValueError("approval decision must not predate BLK-130 request")
    if decided_at >= request_expiry or expires_at > request_expiry:
        raise ValueError("decision window must end within BLK-130 request expiry")
    normalized["operator_attestation"] = _validate_attestation(normalized.get("operator_attestation"))
    normalized["proof_obligations"] = _required_exact_set(
        normalized.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations"
    )
    normalized["excluded_authorities"] = _required_exact_set(
        normalized.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities"
    )
    return normalized


def _validate_attestation(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown = sorted(set(value) - _ATTESTATION_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_ATTESTATION_KEYS - set(value))
    if missing:
        raise ValueError(f"operator_attestation missing field {missing[0]!r}")
    _scan_value_strings(value, "operator_attestation", scan_keys=False)
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized


def _required_exact_set(value: Any, required: set[str], field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must match exact set")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field} must match exact set")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")
    if set(value) != required:
        if field == "excluded_authorities":
            raise ValueError("excluded_authorities must match exact denied authority set")
        raise ValueError(f"{field} must match exact set")
    return sorted(value)


def _required_hash(value: Any, field: str) -> str:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{field} must be canonical sha256")
    digest = value.split(":", 1)[1]
    if any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError(f"{field} must be canonical sha256")
    return value


def _scan_value_strings(value: Any, label: str, scan_keys: bool = True) -> None:
    if isinstance(value, str):
        _scan_string(value, label)
    elif isinstance(value, dict):
        for key, nested in value.items():
            if scan_keys:
                _scan_string(str(key), f"{label}.{key}")
            _scan_value_strings(nested, f"{label}.{key}", scan_keys=scan_keys)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_value_strings(nested, f"{label}[{index}]", scan_keys=scan_keys)


def _scan_string(value: str, label: str) -> None:
    for candidate in _decoded_variants(value):
        compact = "".join(char for char in str(candidate).casefold() if char.isalnum())
        for token in _BODY_TEXT_TOKENS:
            if token in compact:
                raise ValueError(f"protected body text at {label}")
        for token in _FORBIDDEN_COMPACT_TOKENS:
            if token in compact:
                raise ValueError(f"authority-laundering text at {label}: {token}")


def _decoded_variants(value: str) -> list[str]:
    variants = [value]
    current = value
    for _ in range(8):
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
