"""BLK-SYSTEM-100 exact external BEO publication execution record.

This deterministic fixture consumes the exact BLK-SYSTEM-099 approval-decision
package and emits one hash-bound repository-local external BEO publication record.
It consumes the reserved BLK-SYSTEM-100 run ID exactly once inside the returned
package. It does not access signer key material, cryptographically sign, write
immutable storage, mutate a public ledger, execute rollback/revocation/
supersession, generate RTM, perform drift rejection, read protected BLK-req
bodies, scan/mutate target repos, mutate source/Git, run BLK-pipe/BLK-test/Codex
or tooling, or claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_external_publication_approval_decision import (
    APPROVAL_DECISION_PACKAGE_ID,
    APPROVAL_ID,
    CANONICAL_BLK098_REQUEST_PACKAGE_HASH,
    DECISION_RESULT as BLK099_DECISION_RESULT,
    DECISION_SCOPE as BLK099_DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as BLK099_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK099_PROOF_OBLIGATIONS,
    FUTURE_PUBLICATION_EXECUTION_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as BLK099_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK099_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK099_SIDE_EFFECT_FLAGS,
    STATUS as BLK099_STATUS,
    _decoded_variants,
    _enforce_allowed_keys,
    _normalize_authority_text,
    _parse_timestamp,
    _require_dict,
    _required_false,
    _scan_099_string,
    _validate_exact_string_set,
)
from beo_publication_prerequisite_request_after_evidence_refresh import (
    BEO_HASH,
    BEO_ID,
    BLK097_TARGET_HEAD,
    BLK097_TARGET_REPO_PATH,
    CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
    CANONICAL_BLK097_EVIDENCE_HASH,
)

EXECUTION_STATUS = "EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY"
EXECUTION_PACKAGE_ID = "BEO-PUBLICATION-EXECUTION-100-001"
SELECTED_FRONTIER = "external_beo_publication_execution"
EXECUTION_SCOPE = "EXACT_EXTERNAL_BEO_PUBLICATION_EXECUTION_FOR_BLK099_APPROVAL_RECORD_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM"
RUN_ID = FUTURE_PUBLICATION_EXECUTION_RUN_ID
CANONICAL_BLK099_APPROVAL_DECISION_PACKAGE_HASH = "sha256:c83ea7982632b587a8596550cfa0f1c36b546a70b8f2fa8cbefb4aedfeda383b"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-13T20:30:00+10:00")

SIDE_EFFECT_FLAGS = (
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
    "APPROVAL_RETARGETING_OR_SCOPE_EXPANSION",
    "RUN_ID_REUSE_AFTER_BLK_SYSTEM_100_CONSUMPTION",
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
    "BLK099_APPROVAL_DECISION_IDENTITY_AND_HASH_BOUND",
    "BLK098_REQUEST_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK097_AND_BLK087_EVIDENCE_HASHES_BOUND_BY_HASH_ONLY",
    "APPROVAL_ID_MATCHES_BLK099_CAPTURED_APPROVAL",
    "RUN_ID_MATCHES_BLK099_RESERVED_BLK100_RUN_ID_AND_CONSUMED_ONCE",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "EXTERNAL_PUBLICATION_RECORD_EMITTED_FOR_EXACT_BEO",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_POLICIES_BOUND_WITHOUT_SIDE_EFFECTS",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_AFTER_EXTERNAL_PUBLICATION_EXECUTION",
}

_APPROVAL_PACKAGE_KEYS = {
    "approval_decision_status",
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
    "upstream_blk097_evidence_hash",
    "upstream_blk087_execution_package_id",
    "upstream_blk087_execution_package_hash",
    "upstream_blk087_pilot_artifact_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path",
    "target_head_sha",
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
    "approval_decision_package_hash",
    *BLK099_SIDE_EFFECT_FLAGS,
}

_EXECUTION_REQUEST_KEYS = {
    "execution_package_id",
    "operator_identity",
    "execution_scope",
    "selected_frontier",
    "approval_decision_package_id",
    "approval_decision_package_hash",
    "approval_id",
    "run_id",
    "upstream_request_package_id",
    "upstream_request_package_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path",
    "target_head_sha",
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

_ATTESTATION_KEYS = {
    "exact_blk099_approval_decision_reviewed",
    "run_id_consumed_once_for_external_publication_record",
    "published_record_is_exact_beo_identity",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "rtm_generation_and_drift_excluded",
    "protected_body_reads_excluded",
    "target_source_git_mutation_excluded",
    "blk_pipe_blk_test_codex_tooling_excluded",
    "no_production_isolation_claim",
}

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


def build_beo_external_publication_execution(
    approval_package: dict[str, Any], execution_request: dict[str, Any]
) -> dict[str, Any]:
    """Emit one exact BLK-SYSTEM-100 external publication record package."""

    approval = _validate_approval_package(approval_package)
    request = _validate_execution_request(execution_request, approval)
    operator_attestation = deepcopy(request["operator_attestation"])

    publication_record = {
        "publication_mode": "EXTERNAL_BEO_PUBLICATION_RECORD_ONLY",
        "published_beo_id": approval["beo_id"],
        "published_beo_hash": approval["beo_hash"],
        "upstream_request_package_id": approval["upstream_request_package_id"],
        "upstream_request_package_hash": approval["upstream_request_package_hash"],
        "upstream_blk097_evidence_hash": approval["upstream_blk097_evidence_hash"],
        "upstream_blk087_execution_package_hash": approval["upstream_blk087_execution_package_hash"],
        "upstream_blk087_pilot_artifact_hash": approval["upstream_blk087_pilot_artifact_hash"],
        "target_repo_path_metadata_only": approval["target_repo_path"],
        "target_head_sha_metadata_only": approval["target_head_sha"],
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
        "approval_decision_package_hash": approval["approval_decision_package_hash"],
        "approval_id": approval["approval_id"],
        "run_id_consumed": RUN_ID,
        "upstream_request_package_id": approval["upstream_request_package_id"],
        "upstream_request_package_hash": approval["upstream_request_package_hash"],
        "beo_id": approval["beo_id"],
        "beo_hash": approval["beo_hash"],
        "target_repo_path": approval["target_repo_path"],
        "target_head_sha": approval["target_head_sha"],
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


def _validate_approval_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "approval_package")
    _enforce_allowed_keys(package, _APPROVAL_PACKAGE_KEYS, "approval_package")
    submitted_hash = package.get("approval_decision_package_hash")
    if not isinstance(submitted_hash, str):
        raise ValueError("approval_decision_package_hash must be a sha256 hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "approval_decision_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("approval_decision_package_hash does not match submitted BLK-099 package")

    if package.get("external_authoritative_publication_performed") is not False:
        raise ValueError("approval package must remain not published")
    if package.get("runtime_published_beo_output") is not False:
        raise ValueError("approval package must remain not published")
    if package.get("publication_execution_performed") is not False:
        raise ValueError("approval package must remain not published")
    if package.get("future_publication_execution_run_id_consumed") is not False:
        raise ValueError("approval package must not have consumed BLK-SYSTEM-100 run id")

    expected = {
        "approval_decision_status": BLK099_STATUS,
        "approval_decision_package_id": APPROVAL_DECISION_PACKAGE_ID,
        "decision_scope": BLK099_DECISION_SCOPE,
        "selected_frontier": BLK099_SELECTED_FRONTIER,
        "decision_result": BLK099_DECISION_RESULT,
        "upstream_request_package_hash": CANONICAL_BLK098_REQUEST_PACKAGE_HASH,
        "upstream_blk097_evidence_hash": CANONICAL_BLK097_EVIDENCE_HASH,
        "upstream_blk087_execution_package_hash": CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
        "upstream_blk087_pilot_artifact_hash": CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
        "beo_id": BEO_ID,
        "beo_hash": BEO_HASH,
        "target_repo_path": BLK097_TARGET_REPO_PATH,
        "target_head_sha": BLK097_TARGET_HEAD,
        "approval_id": APPROVAL_ID,
        "future_publication_execution_run_id": RUN_ID,
        "next_required_authority": BLK099_NEXT_REQUIRED_AUTHORITY,
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if package.get(key) != value:
            raise ValueError("approval package must match canonical BLK-099 approval decision")
    if submitted_hash != CANONICAL_BLK099_APPROVAL_DECISION_PACKAGE_HASH:
        raise ValueError("approval package must match canonical BLK-099 approval decision")
    for flag in BLK099_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    _validate_exact_string_set(package.get("proof_obligations"), BLK099_PROOF_OBLIGATIONS, "approval_package proof_obligations")
    _validate_exact_string_set(
        package.get("excluded_authorities"),
        BLK099_EXCLUDED_AUTHORITIES,
        "approval_package excluded_authorities",
        denied=True,
    )
    return package


def _validate_execution_request(request: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "execution_request")
    _enforce_allowed_keys(request, _EXECUTION_REQUEST_KEYS, "execution_request")
    for key in (
        "execution_package_id",
        "operator_identity",
        "approval_decision_package_id",
        "approval_decision_package_hash",
        "approval_id",
        "run_id",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "beo_id",
        "beo_hash",
        "target_repo_path",
        "target_head_sha",
    ):
        _scan_100_string(str(request.get(key, "")), key)

    if request.get("execution_package_id") != EXECUTION_PACKAGE_ID:
        raise ValueError(f"execution_package_id must be {EXECUTION_PACKAGE_ID}")
    if request.get("operator_identity") != approval["operator_identity"]:
        raise ValueError("operator_identity must match BLK-099 approval package")
    if request.get("execution_scope") != EXECUTION_SCOPE:
        raise ValueError(f"execution_scope must be {EXECUTION_SCOPE}")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if request.get("approval_decision_package_id") != approval["approval_decision_package_id"]:
        raise ValueError("approval_decision_package_id must match BLK-099 approval package")
    if request.get("approval_decision_package_hash") != approval["approval_decision_package_hash"]:
        raise ValueError("approval_decision_package_hash must match BLK-099 approval package")
    if request.get("approval_id") != approval["approval_id"]:
        raise ValueError("approval_id must match BLK-099 approval id")
    if request.get("run_id") != approval["future_publication_execution_run_id"]:
        raise ValueError("run_id must match BLK-099 future publication execution run id")
    if request.get("upstream_request_package_id") != approval["upstream_request_package_id"]:
        raise ValueError("upstream_request_package_id must match BLK-099 approval package")
    if request.get("upstream_request_package_hash") != approval["upstream_request_package_hash"]:
        raise ValueError("upstream_request_package_hash must match BLK-099 approval package")
    for key in ("beo_id", "beo_hash", "target_repo_path", "target_head_sha"):
        if request.get(key) != approval[key]:
            raise ValueError(f"{key} must match BLK-099 approval package")
    if request.get("execute_external_beo_publication") is not True:
        raise ValueError("execute_external_beo_publication must be true")
    for key in _REQUEST_FALSE_KEYS:
        if request.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValueError(f"execution request must not be {flag}")

    requested_at = _parse_timestamp(request.get("requested_at"), "requested_at")
    expires_at = _parse_timestamp(request.get("expires_at"), "expires_at")
    decided_at = _parse_timestamp(approval.get("decided_at"), "approval.decided_at")
    approval_expires = _parse_timestamp(approval.get("expires_at"), "approval.expires_at")
    if expires_at <= requested_at:
        raise ValueError("expires_at must be after requested_at")
    if expires_at <= FIXTURE_EVALUATION_AT.astimezone(expires_at.tzinfo):
        raise ValueError("execution request must not be calendar-expired")
    if requested_at < decided_at:
        raise ValueError("execution request must not predate BLK-099 approval decision")
    if requested_at >= approval_expires or expires_at > approval_expires:
        raise ValueError("execution request window must end within BLK-099 approval expiry")

    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_string_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_string_set(
        request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities", denied=True
    )
    return request


def _validate_attestation(attestation: dict[str, Any]) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_allowed_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")


def _scan_100_string(value: str, label: str) -> None:
    _scan_099_string(value, label)
    for candidate in _decoded_variants(str(value)):
        compact = "".join(char for char in str(candidate).casefold() if char.isalnum())
        normalized = _normalize_authority_text(candidate)
        for token in _FORBIDDEN_COMPACT_TOKENS:
            if token in compact:
                raise ValueError(f"authority-laundering text at {label}: {token}")
        if "protected body" in normalized and "excluded" not in normalized:
            raise ValueError(f"authority-laundering text at {label}: protected body")
