"""BLK-SYSTEM-129 metadata-bound external BEO publication execution record.

This deterministic fixture consumes the exact BLK-SYSTEM-128 approval-capture
package and emits one repository-local, record-only external BEO publication
execution package. It consumes the reserved BLK-SYSTEM-129 run ID inside the
returned evidence, but it does not sign, write immutable storage, append a public
ledger, execute rollback/revocation/supersession, generate RTM, perform drift
rejection, read protected BLK-req bodies, run BLK-pipe/BLK-test/Codex/tooling,
or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import (
    APPROVAL_DECISION_PACKAGE_ID as BLK128_APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID as BLK128_APPROVAL_ID,
    CANONICAL_BLK127_REQUEST_PACKAGE_HASH,
    CANONICAL_BLK127_TRACE_IDENTITIES,
    DECISION_RESULT as BLK128_DECISION_RESULT,
    DECISION_SCOPE as BLK128_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as BLK128_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK128_PROOF_OBLIGATIONS,
    FUTURE_PUBLICATION_EXECUTION_RUN_ID as BLK128_FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK128_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK128_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK128_SIDE_EFFECT_FLAGS,
    STATUS as BLK128_STATUS,
    _decoded_variants,
    _parse_timestamp,
    _reject_laundered_string,
    _required_exact_set,
    _required_hash,
    _required_string,
    _validate_exact_trace_identities,
)

EXECUTION_STATUS = "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK128_APPROVAL_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "BEO-PUBLICATION-EXECUTION-129-001"
SELECTED_FRONTIER = "external_beo_publication_execution_record"
EXECUTION_SCOPE = "EXACT_EXTERNAL_BEO_PUBLICATION_EXECUTION_FOR_BLK128_APPROVAL_RECORD_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM"
RUN_ID = BLK128_FUTURE_RUN_ID
CANONICAL_BLK128_APPROVAL_CAPTURE_PACKAGE_HASH = "sha256:d16e2631aac8b06c8aba711964f4c4568bfab3540091e0999a79f2ce6d467757"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T09:32:48+10:00")

SIDE_EFFECT_FLAGS = (
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
    "APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
    "RUN_ID_REUSE_WITHOUT_SEPARATE_REPLAY_LEDGER_AUTHORITY",
    "BEO_PUBLICATION_EXECUTION_BEYOND_RECORD_ONLY",
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
    "BLK128_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND",
    "BLK127_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "APPROVAL_ID_MATCHES_BLK128_CAPTURED_APPROVAL",
    "RUN_ID_MATCHES_BLK128_RESERVED_BLK129_RUN_ID_AND_MARKED_CONSUMED_IN_RECORD",
    "METADATA_BOUND_BEO_AND_BEB_IDENTITIES_BOUND",
    "TRACE_METADATA_IDENTITIES_BOUND_WITHOUT_BODY_TEXT",
    "EXTERNAL_PUBLICATION_RECORD_EMITTED_FOR_EXACT_METADATA_BOUND_BEO",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_AFTER_EXTERNAL_PUBLICATION_EXECUTION",
}

_APPROVAL_PACKAGE_KEYS = frozenset(
    {
        "approval_capture_status",
        "approval_decision_package_id",
        "operator_identity",
        "operator_approval_text_raw",
        "operator_approved_request_package_id_normalized",
        "decision_scope",
        "selected_frontier",
        "decision_result",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "upstream_request_status",
        "upstream_decision_id",
        "upstream_decision_gate_hash",
        "upstream_interface_id",
        "upstream_interface_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "approval_id",
        "future_publication_execution_run_id",
        "decided_at",
        "expires_at",
        "approval_decision_captured",
        "human_external_beo_publication_approval_granted",
        "future_external_beo_publication_execution_approved",
        "beo_publication_status",
        "rtm_status",
        "next_required_authority",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "approval_capture_package_hash",
        *BLK128_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_REQUEST_KEYS = frozenset(
    {
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_decision_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "execute_external_beo_publication",
        "signer_key_material_access",
        "cryptographic_signing",
        "immutable_storage_write",
        "public_ledger_mutation",
        "rollback_revocation_supersession_execution",
        "rtm_generation",
        "rtm_drift_rejection",
        "protected_body_reads",
        "target_repo_scan_or_mutation",
        "source_or_git_mutation_by_fixture",
        "blk_pipe_blk_test_codex_runtime",
        "package_network_model_browser_cyber_tooling",
        "production_isolation_claim",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk128_approval_capture_reviewed",
        "run_id_marked_consumed_in_record_only",
        "published_record_is_exact_metadata_bound_beo_identity",
        "trace_metadata_only_no_protected_body_copy",
        "signer_storage_ledger_rollback_side_effects_excluded",
        "rtm_generation_and_drift_excluded",
        "protected_body_reads_excluded",
        "target_source_git_mutation_excluded",
        "blk_pipe_blk_test_codex_tooling_excluded",
        "no_production_isolation_claim",
    }
)

_REQUEST_FALSE_KEYS = (
    "signer_key_material_access",
    "cryptographic_signing",
    "immutable_storage_write",
    "public_ledger_mutation",
    "rollback_revocation_supersession_execution",
    "rtm_generation",
    "rtm_drift_rejection",
    "protected_body_reads",
    "target_repo_scan_or_mutation",
    "source_or_git_mutation_by_fixture",
    "blk_pipe_blk_test_codex_runtime",
    "package_network_model_browser_cyber_tooling",
    "production_isolation_claim",
)

_FORBIDDEN_COMPACT_TOKENS = (
    "signinggranted",
    "signingauthorized",
    "signaturegenerated",
    "cryptographicsigning",
    "signerkeymaterial",
    "signerauthorized",
    "immutablestoragewrite",
    "immutablestoragewritten",
    "storageauthorized",
    "publicledgermutated",
    "publicledgerappend",
    "ledgerauthorized",
    "rollbackexecuted",
    "rollbackauthoritygranted",
    "revocationexecuted",
    "supersessionexecuted",
    "rtmgeneration",
    "rtmid",
    "rtmgenerated",
    "rtmdriftrejection",
    "driftdecision",
    "activevaulthashcomparison",
    "coverageclaim",
    "coveragematrix",
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "protectedbodyread",
    "targetreposcan",
    "targetrepomutation",
    "sourcegitauthorized",
    "sourcemutationattempted",
    "gitmutationauthorized",
    "bebdispatch",
    "beocloseoutexecution",
    "blkpipeexecution",
    "blktestruntime",
    "livecodexexecution",
    "packagemanagersauthorized",
    "networkaccessauthorized",
    "modelservicesauthorized",
    "browsertoolsauthorized",
    "cybertoolsauthorized",
    "productionsandboxauthorized",
    "productionisolationclaimed",
)


def build_metadata_bound_external_beo_publication_execution(
    approval_capture_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Emit one exact BLK-SYSTEM-129 external BEO publication record package."""

    approval = _validate_approval_capture_package(approval_capture_package)
    request = _validate_execution_request(execution_request, approval)
    operator_attestation = deepcopy(request["operator_attestation"])
    trace_identities = list(approval["exact_trace_identities"])
    execution_request_hash = _canonical_hash(request)

    publication_record = {
        "publication_mode": "EXTERNAL_BEO_PUBLICATION_RECORD_ONLY",
        "published_beo_id": approval["beo_id"],
        "published_beb_id": approval["beb_id"],
        "exact_trace_identities": trace_identities,
        "upstream_request_package_id": approval["upstream_request_package_id"],
        "upstream_request_package_hash": approval["upstream_request_package_hash"],
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "signature_status": "NOT_SIGNED_NO_KEY_MATERIAL",
        "storage_status": "NOT_WRITTEN_REPOSITORY_RECORD_ONLY",
        "ledger_status": "NOT_APPENDED_REPOSITORY_RECORD_ONLY",
        "rollback_status": "NOT_EXECUTED_POLICY_BOUND_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    publication_record["publication_record_hash"] = _canonical_hash(
        {key: value for key, value in publication_record.items() if key != "publication_record_hash"}
    )

    package = {
        "execution_status": EXECUTION_STATUS,
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_decision_package_id": approval["approval_decision_package_id"],
        "approval_capture_package_hash": approval["approval_capture_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID,
        "execution_request_hash": execution_request_hash,
        "requested_at": request["requested_at"],
        "expires_at": request["expires_at"],
        "expired": False,
        "replayed": False,
        "stale": False,
        "upstream_request_package_id": approval["upstream_request_package_id"],
        "upstream_request_package_hash": approval["upstream_request_package_hash"],
        "beo_id": approval["beo_id"],
        "beb_id": approval["beb_id"],
        "exact_trace_identities": trace_identities,
        "external_beo_publication_executed": True,
        "future_publication_execution_run_id_consumed": True,
        "beo_publication": "PUBLISHED_EXTERNAL_BEO_RECORD",
        "rtm_status": "NOT_GENERATED",
        "publication_record": publication_record,
        "publication_record_hash": publication_record["publication_record_hash"],
        "operator_attestation": operator_attestation,
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


def _validate_approval_capture_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("approval_capture_package must be a dictionary")
    unknown = sorted(set(package) - _APPROVAL_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"approval_capture_package rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("approval_capture_package_hash"), "approval_capture_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "approval_capture_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("approval_capture_package_hash does not match submitted BLK-128 package")
    if submitted_hash != CANONICAL_BLK128_APPROVAL_CAPTURE_PACKAGE_HASH:
        raise ValueError("approval package must match canonical BLK-128 approval capture")

    expected = {
        "approval_capture_status": BLK128_STATUS,
        "approval_decision_package_id": BLK128_APPROVAL_DECISION_PACKAGE_ID,
        "decision_scope": BLK128_DECISION_SCOPE,
        "selected_frontier": BLK128_SELECTED_FRONTIER,
        "decision_result": BLK128_DECISION_RESULT,
        "upstream_request_package_id": "BEO-PUBLICATION-PREREQUISITE-REQUEST-127-001",
        "upstream_request_package_hash": CANONICAL_BLK127_REQUEST_PACKAGE_HASH,
        "upstream_request_status": "METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_NOT_GRANTED",
        "upstream_decision_id": "BEO-PUBLICATION-PATH-DECISION-GATE-126-001",
        "upstream_interface_id": "BEO_RTM_IFACE_126",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "approval_id": BLK128_APPROVAL_ID,
        "future_publication_execution_run_id": RUN_ID,
        "beo_publication_status": "APPROVAL_CAPTURED_NOT_PUBLISHED",
        "rtm_status": "NOT_GENERATED",
        "next_required_authority": BLK128_NEXT_REQUIRED_AUTHORITY,
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("approval package must match canonical BLK-128 approval capture")
    if normalized.get("approval_decision_captured") is not True:
        raise ValueError("approval package must be BLK-128 approval-captured")
    if normalized.get("human_external_beo_publication_approval_granted") is not True:
        raise ValueError("approval package must contain human external BEO publication approval")
    if normalized.get("future_external_beo_publication_execution_approved") is not True:
        raise ValueError("approval package must approve one future publication execution")
    if tuple(_validate_exact_trace_identities(normalized.get("exact_trace_identities"))) != CANONICAL_BLK127_TRACE_IDENTITIES:
        raise ValueError("approval package must match canonical BLK-128 trace identities")
    _required_exact_set(normalized.get("proof_obligations"), BLK128_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK128_EXCLUDED_AUTHORITIES, "approval_package excluded_authorities")
    for flag in BLK128_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"approval_package {flag} must remain false")
    return normalized


def _validate_execution_request(request: Any, approval: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("execution_request must be a dictionary")
    unknown = sorted(set(request) - _EXECUTION_REQUEST_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = deepcopy(request)
    for key in (
        "execution_package_id",
        "operator_identity",
        "approval_decision_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "beo_id",
        "beb_id",
    ):
        _scan_129_string(str(normalized.get(key, "")), key)

    if normalized.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if normalized.get("operator_identity") != approval["operator_identity"]:
        raise ValueError("operator_identity must match BLK-128 approval package")
    if normalized.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if normalized.get("approval_decision_package_id") != approval["approval_decision_package_id"]:
        raise ValueError("approval_decision_package_id must match BLK-128 approval package")
    if normalized.get("approval_capture_package_hash") != approval["approval_capture_package_hash"]:
        raise ValueError("approval_capture_package_hash must match BLK-128 approval package")
    if normalized.get("approval_id") != approval["approval_id"]:
        raise ValueError("approval_id must match BLK-128 approval id")
    if normalized.get("run_id") != approval["future_publication_execution_run_id"]:
        raise ValueError("run_id must match BLK-128 future publication execution run id")
    if normalized.get("upstream_request_package_id") != approval["upstream_request_package_id"]:
        raise ValueError("upstream_request_package_id must match BLK-128 approval package")
    if normalized.get("upstream_request_package_hash") != approval["upstream_request_package_hash"]:
        raise ValueError("upstream_request_package_hash must match BLK-128 approval package")
    for key in ("beo_id", "beb_id"):
        if normalized.get(key) != approval[key]:
            raise ValueError(f"{key} must match BLK-128 approval package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != approval["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-128 approval package")
    if normalized.get("execute_external_beo_publication") is not True:
        raise ValueError("execute_external_beo_publication must be true")
    for key in _REQUEST_FALSE_KEYS:
        if normalized.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")

    requested_at = _parse_timestamp(normalized.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(normalized.get("expires_at"), "expires_at")
    decided_at = _parse_timestamp(approval.get("decided_at"), "approval.decided_at")
    approval_expires = _parse_timestamp(approval.get("expires_at"), "approval.expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at < decided_at:
        raise ValueError("execution request must not predate BLK-128 approval capture")
    if requested_at >= approval_expires or expires_at > approval_expires:
        raise ValueError("execution request window must end within BLK-128 approval expiry")

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
    normalized = {}
    for key in sorted(_ATTESTATION_KEYS):
        if value.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
        normalized[key] = True
    return normalized


def _scan_129_string(value: str, label: str) -> None:
    _reject_laundered_string(value, label)
    for candidate in _decoded_variants(str(value)):
        compact = "".join(char for char in str(candidate).casefold() if char.isalnum())
        for token in _FORBIDDEN_COMPACT_TOKENS:
            if token in compact:
                raise ValueError(f"authority-laundering text at {label}: {token}")
