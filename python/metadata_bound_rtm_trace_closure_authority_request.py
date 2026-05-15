"""BLK-SYSTEM-130 metadata-bound RTM / blk-link trace-closure authority request.

This deterministic fixture consumes the exact BLK-SYSTEM-129 record-only
external BEO publication execution package and emits one review-only request for
a future local, non-authoritative RTM / blk-link trace-closure approval decision.
It does not capture approval, execute trace closure, generate RTM, reject drift,
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
from metadata_bound_external_beo_publication_execution import SIDE_EFFECT_FLAGS as BLK129_SIDE_EFFECT_FLAGS
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities

REQUEST_STATUS = "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY_AFTER_BLK129_EXTERNAL_BEO_PUBLICATION_NOT_GRANTED"
AUTHORITY_REQUEST_PACKAGE_ID = "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001"
SELECTED_FRONTIER = "metadata_bound_rtm_trace_closure_authority_request_after_external_beo_publication"
REQUEST_SCOPE = "RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_AFTER_BLK129_EXTERNAL_BEO_PUBLICATION_REVIEW_ONLY"
NEXT_REQUIRED_AUTHORITY = "EXACT_RTM_TRACE_CLOSURE_APPROVAL_DECISION_CAPTURE_REQUIRED_NOT_CAPTURED"
CANONICAL_BLK129_EXECUTION_PACKAGE_HASH = "sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c"
CANONICAL_BLK129_PUBLICATION_RECORD_HASH = "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798"
CANONICAL_BEO_ID = "BEO_126"
CANONICAL_BEB_ID = "BEB_126"
CANONICAL_TRACE_IDENTITIES = (
    "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
)
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T11:08:45+10:00")

SIDE_EFFECT_FLAGS = (
    "human_rtm_trace_closure_approval_granted",
    "rtm_trace_closure_authorized",
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
    "HUMAN_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE",
    "RUNTIME_RTM_TRACE_CLOSURE_EXECUTION",
    "PRODUCTION_OR_REUSABLE_BLK_LINK_EXECUTION",
    "RUNTIME_RTM_GENERATION",
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
    "BLK129_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK129_PUBLICATION_RECORD_HASH_BOUND",
    "METADATA_BOUND_BEO_AND_BEB_IDENTITIES_BOUND",
    "TRACE_METADATA_IDENTITIES_BOUND_WITHOUT_BODY_TEXT",
    "EXTERNAL_BEO_PUBLICATION_RECORD_CONSUMED_AS_PREREQUISITE_ONLY",
    "RTM_TRACE_CLOSURE_APPROVAL_REQUESTED_FOR_FUTURE_REVIEW_NOT_CAPTURED",
    "LOCAL_NON_AUTHORITATIVE_TRACE_CLOSURE_SELECTED_FOR_NEXT_RUNG",
    "PRODUCTION_BLK_LINK_NOT_AUTHORIZED",
    "RTM_GENERATION_NOT_PERFORMED_BY_REQUEST",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_TRACE_CLOSURE_EXECUTION",
}

_REQUEST_KEYS = frozenset(
    {
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
        "request_future_exact_rtm_trace_closure_approval",
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
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk129_publication_execution_reviewed",
        "external_beo_publication_record_is_hash_bound",
        "trace_metadata_only_no_protected_body_copy",
        "request_is_for_future_trace_closure_approval_not_execution",
        "local_non_authoritative_trace_closure_selected_for_next_rung",
        "production_blk_link_not_authorized",
        "rtm_generation_not_performed_by_request",
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

_BLK129_REQUIRED_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "execution_scope",
        "selected_frontier",
        "approval_decision_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_consumed",
        "execution_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "external_beo_publication_executed",
        "future_publication_execution_run_id_consumed",
        "beo_publication",
        "rtm_status",
        "publication_record",
        "publication_record_hash",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "execution_package_hash",
        *BLK129_SIDE_EFFECT_FLAGS,
    }
)

_FORBIDDEN_COMPACT_TOKENS = (
    "rtmgenerated",
    "rtmgenerationauthorized",
    "rtmgenerationgranted",
    "productionblklinkauthorized",
    "productionblklinkexecuted",
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


def build_metadata_bound_rtm_trace_closure_authority_request(
    blk129_execution_package: dict[str, Any], authority_request: dict[str, Any]
) -> dict[str, Any]:
    """Build a BLK-SYSTEM-130 request package from the exact BLK-129 record."""

    upstream = _validate_blk129_execution_package(blk129_execution_package)
    request = _validate_authority_request(authority_request, upstream)
    trace_identities = list(upstream["exact_trace_identities"])
    authority_request_hash = _canonical_hash(request)
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
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "requested_authority": "ONE_FUTURE_LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_APPROVAL",
        "request_future_exact_rtm_trace_closure_approval": True,
        "rtm_trace_closure_authority": "REQUEST_ONLY_NOT_GRANTED",
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "authority_request_hash": authority_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
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


def _validate_blk129_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("blk129_execution_package must be a dictionary")
    missing = sorted(_BLK129_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"blk129_execution_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("execution_package_hash"), "execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("execution_package_hash does not match submitted BLK-129 package")
    if submitted_hash != CANONICAL_BLK129_EXECUTION_PACKAGE_HASH:
        raise ValueError("package must match canonical BLK-129 publication execution record")
    expected = {
        "execution_status": "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK128_APPROVAL_RECORD_ONLY",
        "execution_package_id": "BEO-PUBLICATION-EXECUTION-129-001",
        "selected_frontier": "external_beo_publication_execution_record",
        "run_id_consumed": "RUN-BLK-SYSTEM-129-EXTERNAL-BEO-PUBLICATION-001",
        "publication_record_hash": CANONICAL_BLK129_PUBLICATION_RECORD_HASH,
        "beo_id": CANONICAL_BEO_ID,
        "beb_id": CANONICAL_BEB_ID,
        "beo_publication": "PUBLISHED_EXTERNAL_BEO_RECORD",
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("package must match canonical BLK-129 publication execution record")
    record = normalized.get("publication_record")
    if not isinstance(record, dict):
        raise ValueError("publication_record must be a dictionary")
    if record.get("publication_record_hash") != CANONICAL_BLK129_PUBLICATION_RECORD_HASH:
        raise ValueError("publication_record_hash must match canonical BLK-129 publication record")
    if record.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("BLK-129 publication record must not have generated RTM")
    if tuple(_validate_exact_trace_identities(normalized.get("exact_trace_identities"))) != CANONICAL_TRACE_IDENTITIES:
        raise ValueError("exact_trace_identities must match canonical BLK-129 trace metadata")
    for flag in BLK129_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-129 package {flag} must remain false")
    return normalized


def _validate_authority_request(request: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("authority_request must be a dictionary")
    unknown = sorted(set(request) - _REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_REQUEST_KEYS - set(request))
    if missing:
        raise ValueError(f"authority_request missing field {missing[0]!r}")
    normalized = deepcopy(request)
    for key in (
        "authority_request_package_id",
        "operator_identity",
        "request_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("authority_request_package_id") != AUTHORITY_REQUEST_PACKAGE_ID:
        raise ValueError(f"authority_request_package_id must be {AUTHORITY_REQUEST_PACKAGE_ID}")
    if normalized.get("operator_identity") != "discord:684235178083745819":
        raise ValueError("operator_identity must match canonical operator identity")
    if normalized.get("request_scope") != REQUEST_SCOPE:
        raise ValueError(f"request_scope must be {REQUEST_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    expected = {
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match canonical BLK-129 publication execution record")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != upstream["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match canonical BLK-129 publication execution record")
    if normalized.get("request_future_exact_rtm_trace_closure_approval") is not True:
        raise ValueError("request_future_exact_rtm_trace_closure_approval must be true")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"authority request must not be {flag}")
    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("authority request must not be calendar-expired")
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
