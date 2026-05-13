"""BLK-SYSTEM-098 BEO publication prerequisite request after evidence refresh.

This fixture packages the exact BLK-SYSTEM-097 evidence-only BLK-test refresh
and the exact BLK-SYSTEM-087 local BEO publication-pilot package into a
human-review prerequisite request for a later external BEO publication decision.
It does not approve or perform publication, signing, storage, ledger mutation,
rollback, RTM generation, drift rejection, protected-body access, target/source
mutation, BLK-pipe/BLK-test/Codex runtime, tooling, or production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_pilot_execution import (
    EXECUTION_PACKAGE_ID as BLK087_EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS as BLK087_EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK087_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK087_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY as BLK087_NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER as BLK087_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK087_SIDE_EFFECT_FLAGS,
)

REQUEST_STATUS = "BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED"
REQUEST_PACKAGE_ID = "BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001"
SELECTED_FRONTIER = "external_beo_publication_prerequisite_request_after_blk_test_refresh"
REQUEST_SCOPE = "BEO_PUBLICATION_PREREQUISITE_REQUEST_REVIEW_ONLY_AFTER_BLK_TEST_REFRESH"
NEXT_REQUIRED_AUTHORITY = "EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_REQUIRED_NOT_GRANTED"

CANONICAL_BLK097_EVIDENCE_HASH = "sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580"
CANONICAL_BLK087_EXECUTION_PACKAGE_HASH = "sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e"
CANONICAL_BLK087_PILOT_ARTIFACT_HASH = "sha256:6ee76d749bdb809bb39ae2f6f26c22c302370f9bf30da54acfc208a6661e875a"

BLK097_APPROVAL_ID = "APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001"
BLK097_RUN_ID = "RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001"
BLK097_TARGET_REPO_PATH = "/home/dad/code/Kuronode-v1"
BLK097_SOURCE_SUBTREE_PATH = "/home/dad/code/Kuronode-v1/scripts"
BLK097_TARGET_HEAD = "aebea51bed911c781a537d84d38b2dcb838b1368"
BLK097_PILOT_STATUS = "BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY"
BEO_ID = "BEO-054-001"
BEO_HASH = "sha256:" + "a" * 64
NOT_GENERATED = "NOT_GENERATED"
DRAFT_ONLY = "DRAFT_ONLY"

SIDE_EFFECT_FLAGS = (
    "external_authoritative_publication_performed",
    "runtime_published_beo_output",
    "live_publication_approval_captured",
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
    "EXTERNAL_AUTHORITATIVE_BEO_PUBLICATION",
    "RUNTIME_PUBLISHED_BEO_OUTPUT",
    "LIVE_PUBLICATION_APPROVAL_CAPTURE",
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
    "BLK097_EVIDENCE_HASH_BOUND",
    "BLK097_PASS_STATUS_BOUND",
    "BLK097_TARGET_HEAD_AND_PATH_BOUND",
    "BLK097_SOURCE_AND_GIT_STERILITY_BOUND",
    "BLK087_LOCAL_PILOT_PACKAGE_HASH_BOUND",
    "BLK087_LOCAL_PILOT_NOT_EXTERNAL_PUBLICATION_DISCLOSED",
    "BEO_IDENTITY_AND_HASH_BOUND",
    "EXTERNAL_PUBLICATION_DECISION_REQUESTED_FOR_REVIEW_NOT_GRANTED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_SIDE_EFFECTS_EXCLUDED",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "ACTIVE_VAULT_AND_PROTECTED_BODY_ACCESS_EXCLUDED",
    "TARGET_REPO_AND_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_ANY_PUBLICATION_DECISION",
}

_RUNTIME_EVIDENCE_KEYS = {
    "active_vault_read",
    "actual_head",
    "approval_id",
    "arbitrary_shell_called",
    "beo_publication",
    "block_reason",
    "browser_tooling_called",
    "commit_allowed",
    "coverage_claim_promoted",
    "cyber_tooling_called",
    "evidence_json_bytes",
    "expected_head",
    "files_checked",
    "files_checked_count",
    "files_checked_truncated",
    "findings",
    "findings_count",
    "findings_emitted_count",
    "findings_truncated",
    "fixed_tool_executed",
    "generic_mcp_authority",
    "git_metadata_hash_after",
    "git_metadata_hash_before",
    "git_mutation_allowed",
    "git_mutation_detected",
    "live_codex_execution",
    "model_service_called",
    "network_called",
    "observed_remote_head",
    "output_byte_limit",
    "package_manager_called",
    "pilot_status",
    "production_isolation_claimed",
    "production_mcp_authority",
    "protected_body_read",
    "public_ledger_mutation",
    "push_allowed",
    "replay_consumed_before_runtime",
    "requested_tool",
    "reusable_service_started",
    "rtm_drift_rejection",
    "rtm_status",
    "run_id",
    "source_mutation_detected",
    "source_subtree_path",
    "source_tree_hash_after",
    "source_tree_hash_before",
    "source_write_allowed",
    "sprint",
    "staging_allowed",
    "status",
    "target_repo_path",
    "typescript_tooling_called",
    "workspace_cleanup_verified",
    "workspace_clone_path",
}

_REQUEST_KEYS = {
    "request_package_id",
    "operator_identity",
    "request_scope",
    "selected_frontier",
    "upstream_blk097_evidence_hash",
    "upstream_blk087_execution_package_id",
    "upstream_blk087_execution_package_hash",
    "upstream_blk087_pilot_artifact_hash",
    "beo_id",
    "beo_hash",
    "target_repo_path",
    "target_head_sha",
    "request_future_external_beo_publication_decision",
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
    "exact_blk097_evidence_reviewed",
    "exact_blk087_local_pilot_reviewed",
    "fresh_blk_test_pass_is_evidence_not_publication_approval",
    "local_pilot_artifact_is_not_external_publication",
    "request_is_for_future_human_decision_not_granted",
    "signer_storage_ledger_rollback_side_effects_excluded",
    "rtm_generation_and_drift_excluded",
    "protected_body_reads_excluded",
    "target_source_git_mutation_excluded",
    "no_adjacent_runtime_side_effects",
}

_CANONICAL_BLK087_FIELDS = {
    "execution_status": BLK087_EXECUTION_STATUS,
    "execution_package_id": BLK087_EXECUTION_PACKAGE_ID,
    "selected_frontier": BLK087_SELECTED_FRONTIER,
    "beo_id": BEO_ID,
    "beo_hash": BEO_HASH,
    "target_id": "BEO-PUBLICATION-TARGET-055-001",
    "target_ref": "fixture://beo-publication-targets/055/001",
    "beo_publication": "PILOT_LOCAL_PUBLISHED_BEO_OUTPUT_NOT_AUTHORITATIVE",
    "rtm_status": NOT_GENERATED,
    "next_required_authority": BLK087_NEXT_REQUIRED_AUTHORITY,
    "execution_package_hash": CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
    "pilot_publication_artifact_hash": CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
}

_FORBIDDEN_VALUE_TOKENS = (
    "beo publication authorized",
    "beo publication authorised",
    "publication authority granted",
    "publication approval granted",
    "approved for publication",
    "publication greenlit",
    "publication allowed",
    "publication permitted",
    "beo is published",
    "rtm generated",
    "rtm generation",
    "rtm drift rejection approved",
    "active vault hash comparison",
    "active-vault hash comparison",
    "coverage truth established",
    "drift decision made",
    "signature generated",
    "cryptographic signing",
    "signer key material",
    "private key",
    "key material",
    "api key",
    "public ledger mutated",
    "immutable storage written",
    "rollback executed",
    "source mutation authorized",
    "git mutation authorized",
    "beb dispatch authorized",
    "beo closeout authorized",
    "blk pipe success",
    "blk test pass approval",
    "codex approval",
    "approval inherited",
    "runtime execution authorized",
    "approved for runtime execution",
    "live execution authorized",
    "production isolation claimed",
    "production sandbox enforced",
    "protected blk req body reads authorized",
)

_FORBIDDEN_COMPACT_TOKENS = (
    "beopublicationauthorized",
    "beopublicationauthorised",
    "publicationauthoritygranted",
    "publicationapprovalgranted",
    "approvedforpublication",
    "publicationgreenlit",
    "publicationallowed",
    "publicationpermitted",
    "beoispublished",
    "publishedbeo",
    "publishbeo",
    "authoritativebeopublicationauthorized",
    "authoritativebeopublicationisauthorized",
    "authoritativebeopublicationgranted",
    "rtmgenerated",
    "rtmgeneration",
    "rtmid",
    "rtmdriftrejectionapproved",
    "activevaulthashcomparison",
    "activevaultcomparison",
    "coveragetruthestablished",
    "driftdecisionmade",
    "signaturegenerated",
    "cryptographicsigning",
    "signerkeymaterial",
    "privatekey",
    "keymaterial",
    "apikey",
    "publicledgermutated",
    "immutablestoragewritten",
    "rollbackexecuted",
    "sourcemutationauthorized",
    "gitmutationauthorized",
    "bebdispatchauthorized",
    "beocloseoutauthorized",
    "blkpipeSuccess".casefold(),
    "blktestpassapproval",
    "codexapproval",
    "approvalinherited",
    "runtimeexecutionauthorized",
    "approvedforruntimeexecution",
    "liveexecutionauthorized",
    "productionisolationclaimed",
    "productionsandboxenforced",
    "protectedblkreqbodyreadsauthorized",
)

_PROTECTED_PATH_COMPACT = (
    "docsactive",
    "docsrequirements",
    "docsusecases",
    "protectedblkreqbody",
)


class ValidationError(ValueError):
    """Validation error for BLK-SYSTEM-098 request packages."""


def build_beo_publication_prerequisite_request_after_evidence_refresh(
    blk097_runtime_evidence: dict[str, Any],
    blk087_local_pilot_package: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    """Build a review-only publication prerequisite request package."""

    evidence = _validate_blk097_evidence(blk097_runtime_evidence)
    local_pilot = _validate_blk087_local_pilot_package(blk087_local_pilot_package)
    approved_request = _validate_request(request, evidence, local_pilot)

    package = {
        "request_status": REQUEST_STATUS,
        "request_package_id": REQUEST_PACKAGE_ID,
        "operator_identity": approved_request["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "upstream_blk097_evidence_hash": CANONICAL_BLK097_EVIDENCE_HASH,
        "upstream_blk087_execution_package_id": BLK087_EXECUTION_PACKAGE_ID,
        "upstream_blk087_execution_package_hash": CANONICAL_BLK087_EXECUTION_PACKAGE_HASH,
        "upstream_blk087_pilot_artifact_hash": CANONICAL_BLK087_PILOT_ARTIFACT_HASH,
        "beo_id": BEO_ID,
        "beo_hash": BEO_HASH,
        "target_repo_path": BLK097_TARGET_REPO_PATH,
        "target_head_sha": BLK097_TARGET_HEAD,
        "future_external_publication_decision_requested": True,
        "external_publication_approval_granted": False,
        "blk097_evidence_summary": {
            "sprint": evidence["sprint"],
            "approval_id": evidence["approval_id"],
            "run_id": evidence["run_id"],
            "status": evidence["status"],
            "pilot_status": evidence["pilot_status"],
            "target_repo_path": evidence["target_repo_path"],
            "source_subtree_path": evidence["source_subtree_path"],
            "target_head_sha": evidence["actual_head"],
            "observed_remote_head": evidence["observed_remote_head"],
            "files_checked": deepcopy(evidence["files_checked"]),
            "findings_count": evidence["findings_count"],
            "source_tree_hash_before": evidence["source_tree_hash_before"],
            "source_tree_hash_after": evidence["source_tree_hash_after"],
            "git_metadata_hash_before": evidence["git_metadata_hash_before"],
            "git_metadata_hash_after": evidence["git_metadata_hash_after"],
        },
        "blk087_trace_artifacts": deepcopy(local_pilot["trace_artifacts"]),
        "operator_attestation": deepcopy(approved_request["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
        **{flag: False for flag in SIDE_EFFECT_FLAGS},
    }
    package["request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "request_package_hash"}
    )
    return package


def _validate_blk097_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    _require_dict(evidence, "BLK-SYSTEM-097 evidence")
    _enforce_allowed_keys(evidence, _RUNTIME_EVIDENCE_KEYS, "BLK-SYSTEM-097 evidence", "unexpected BLK-SYSTEM-097 evidence field")

    _required_equal(evidence.get("sprint"), "BLK-SYSTEM-097", "sprint")
    _required_equal(evidence.get("approval_id"), BLK097_APPROVAL_ID, "approval_id")
    _required_equal(evidence.get("run_id"), BLK097_RUN_ID, "run_id")
    if evidence.get("target_repo_path") != BLK097_TARGET_REPO_PATH:
        raise ValidationError("target_repo_path must be exact /home/dad/code/Kuronode-v1")
    _required_equal(evidence.get("source_subtree_path"), BLK097_SOURCE_SUBTREE_PATH, "source_subtree_path")
    _required_equal(evidence.get("expected_head"), BLK097_TARGET_HEAD, "expected_head")
    _required_equal(evidence.get("actual_head"), BLK097_TARGET_HEAD, "actual_head")
    _required_equal(evidence.get("observed_remote_head"), BLK097_TARGET_HEAD, "observed_remote_head")
    if evidence.get("status") != "PASS":
        raise ValidationError("BLK-SYSTEM-097 evidence status must be PASS")
    if evidence.get("pilot_status") != BLK097_PILOT_STATUS:
        raise ValidationError(f"pilot_status must be {BLK097_PILOT_STATUS}")
    if evidence.get("findings_count") != 0:
        raise ValidationError("findings_count must be 0")
    if evidence.get("findings_emitted_count") != 0:
        raise ValidationError("findings_emitted_count must be 0")
    if evidence.get("findings") != []:
        raise ValidationError("findings must be empty")
    if evidence.get("files_checked") != ["smoke_test.ts"]:
        raise ValidationError("files_checked must remain the exact BLK-SYSTEM-097 checked file list")
    if evidence.get("files_checked_count") != 1:
        raise ValidationError("files_checked_count must be 1")
    if evidence.get("beo_publication") != DRAFT_ONLY:
        raise ValidationError("beo_publication must remain DRAFT_ONLY")
    if evidence.get("rtm_status") != NOT_GENERATED:
        raise ValidationError("rtm_status must remain NOT_GENERATED")
    if evidence.get("requested_tool") != "run_ast_validation":
        raise ValidationError("requested_tool must remain run_ast_validation")
    if evidence.get("source_tree_hash_before") != evidence.get("source_tree_hash_after"):
        raise ValidationError("source_tree_hash before/after must match")
    if evidence.get("git_metadata_hash_before") != evidence.get("git_metadata_hash_after"):
        raise ValidationError("git metadata hash before/after must match")

    false_flags = {
        "active_vault_read",
        "arbitrary_shell_called",
        "browser_tooling_called",
        "commit_allowed",
        "coverage_claim_promoted",
        "cyber_tooling_called",
        "files_checked_truncated",
        "findings_truncated",
        "generic_mcp_authority",
        "git_mutation_allowed",
        "git_mutation_detected",
        "live_codex_execution",
        "model_service_called",
        "network_called",
        "package_manager_called",
        "production_isolation_claimed",
        "production_mcp_authority",
        "protected_body_read",
        "public_ledger_mutation",
        "push_allowed",
        "reusable_service_started",
        "rtm_drift_rejection",
        "source_mutation_detected",
        "source_write_allowed",
        "staging_allowed",
        "typescript_tooling_called",
    }
    for flag in sorted(false_flags):
        _required_false(evidence.get(flag), flag)
    if evidence.get("fixed_tool_executed") is not True:
        raise ValidationError("fixed_tool_executed must be true")
    if evidence.get("replay_consumed_before_runtime") is not True:
        raise ValidationError("replay_consumed_before_runtime must be true")
    if evidence.get("workspace_cleanup_verified") is not True:
        raise ValidationError("workspace_cleanup_verified must be true")

    computed_hash = _canonical_hash(evidence)
    if computed_hash != CANONICAL_BLK097_EVIDENCE_HASH:
        raise ValidationError("BLK-SYSTEM-097 evidence hash does not match canonical committed evidence")
    _scan_nested(
        {
            key: value
            for key, value in evidence.items()
            if key not in {"pilot_status", "beo_publication", "rtm_status"}
        },
        "BLK-SYSTEM-097 evidence",
    )
    return deepcopy(evidence)


def _validate_blk087_local_pilot_package(package: dict[str, Any]) -> dict[str, Any]:
    _require_dict(package, "BLK-SYSTEM-087 local pilot package")
    actual_hash = package.get("execution_package_hash")
    if not isinstance(actual_hash, str):
        raise ValidationError("BLK-SYSTEM-087 package must include execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"})
    if actual_hash != recomputed:
        raise ValidationError("BLK-SYSTEM-087 package hash does not match submitted package")
    for key, expected in _CANONICAL_BLK087_FIELDS.items():
        if package.get(key) != expected:
            raise ValidationError("BLK-SYSTEM-087 package must match canonical local pilot fixture")
    if set(package.get("proof_obligations", [])) != BLK087_PROOF_OBLIGATIONS:
        raise ValidationError("BLK-SYSTEM-087 proof obligations must match canonical local pilot fixture")
    if set(package.get("excluded_authorities", [])) != BLK087_EXCLUDED_AUTHORITIES:
        raise ValidationError("BLK-SYSTEM-087 excluded authorities must match canonical local pilot fixture")
    for flag in BLK087_SIDE_EFFECT_FLAGS:
        _required_false(package.get(flag), flag)
    return deepcopy(package)


def _validate_request(request: dict[str, Any], evidence: dict[str, Any], local_pilot: dict[str, Any]) -> dict[str, Any]:
    _require_dict(request, "request")
    _enforce_allowed_keys(request, _REQUEST_KEYS, "request")
    _scan_string(request.get("request_package_id", ""), "request.request_package_id")
    _scan_string(request.get("operator_identity", ""), "request.operator_identity")

    _required_equal(request.get("request_package_id"), REQUEST_PACKAGE_ID, "request_package_id")
    _required_equal(request.get("request_scope"), REQUEST_SCOPE, "request_scope")
    if request.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValidationError(f"selected_frontier must be {SELECTED_FRONTIER}")
    _required_equal(request.get("upstream_blk097_evidence_hash"), CANONICAL_BLK097_EVIDENCE_HASH, "upstream_blk097_evidence_hash")
    _required_equal(request.get("upstream_blk087_execution_package_id"), BLK087_EXECUTION_PACKAGE_ID, "upstream_blk087_execution_package_id")
    _required_equal(request.get("upstream_blk087_execution_package_hash"), CANONICAL_BLK087_EXECUTION_PACKAGE_HASH, "upstream_blk087_execution_package_hash")
    _required_equal(request.get("upstream_blk087_pilot_artifact_hash"), CANONICAL_BLK087_PILOT_ARTIFACT_HASH, "upstream_blk087_pilot_artifact_hash")
    _required_equal(request.get("beo_id"), BEO_ID, "beo_id")
    _required_equal(request.get("beo_hash"), BEO_HASH, "beo_hash")
    if request.get("target_repo_path") != BLK097_TARGET_REPO_PATH:
        raise ValidationError("target_repo_path must be exact /home/dad/code/Kuronode-v1")
    _required_equal(request.get("target_head_sha"), BLK097_TARGET_HEAD, "target_head_sha")
    if request.get("request_future_external_beo_publication_decision") is not True:
        raise ValidationError("request_future_external_beo_publication_decision must be true")
    for flag in SIDE_EFFECT_FLAGS:
        _required_false(request.get(flag), flag)
    for flag in ("expired", "replayed", "stale"):
        if request.get(flag) is not False:
            raise ValidationError(f"request must not be {flag}")
    _validate_timestamp_window(request.get("requested_at"), request.get("expires_at"))
    _validate_attestation(request.get("operator_attestation"))
    _validate_exact_string_set(request.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _validate_exact_string_set(request.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities", denied=True)

    if request["upstream_blk097_evidence_hash"] != _canonical_hash(evidence):
        raise ValidationError("upstream_blk097_evidence_hash does not match submitted BLK-SYSTEM-097 evidence")
    if request["upstream_blk087_execution_package_hash"] != local_pilot["execution_package_hash"]:
        raise ValidationError("upstream_blk087_execution_package_hash does not match submitted BLK-SYSTEM-087 package")
    if request["upstream_blk087_pilot_artifact_hash"] != local_pilot["pilot_publication_artifact_hash"]:
        raise ValidationError("upstream_blk087_pilot_artifact_hash does not match submitted BLK-SYSTEM-087 package")

    _scan_nested(
        {
            key: value
            for key, value in request.items()
            if key not in {"proof_obligations", "excluded_authorities", "request_scope", "selected_frontier"}
        },
        "request",
    )
    return deepcopy(request)


def _validate_attestation(attestation: Any) -> None:
    _require_dict(attestation, "operator_attestation")
    _enforce_allowed_keys(attestation, _ATTESTATION_KEYS, "operator_attestation")
    for key in sorted(_ATTESTATION_KEYS):
        if attestation.get(key) is not True:
            raise ValidationError(f"operator_attestation.{key} must be true")


def _validate_timestamp_window(requested_at: Any, expires_at: Any) -> None:
    requested = _parse_timestamp(requested_at, "requested_at")
    expires = _parse_timestamp(expires_at, "expires_at")
    if expires <= requested:
        raise ValidationError("expires_at must be after requested_at")


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{field} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{field} must be timezone-aware")
    return parsed


def _validate_exact_string_set(value: Any, expected: set[str], field: str, denied: bool = False) -> None:
    if not isinstance(value, list):
        raise ValidationError(f"{field} must match exact {'denied authority ' if denied else ''}set")
    if any(not isinstance(item, str) for item in value):
        raise ValidationError(f"{field} must contain only strings")
    if len(value) != len(set(value)):
        raise ValidationError(f"{field} must not contain duplicates")
    if set(value) != expected:
        raise ValidationError(f"{field} must match exact {'denied authority ' if denied else ''}set")


def _require_dict(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{field} must be a dictionary")
    return value


def _enforce_allowed_keys(value: dict[str, Any], allowed: set[str], field: str, message: str | None = None) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        prefix = message or "unexpected field"
        raise ValidationError(f"{prefix} in {field}: {extra[0]}")
    missing = sorted(allowed - set(value))
    if missing:
        raise ValidationError(f"missing field in {field}: {missing[0]}")


def _required_equal(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ValidationError(f"{field} must be {expected}")


def _required_false(value: Any, field: str) -> None:
    if value is not False:
        raise ValidationError(f"{field} must remain false")


def _scan_nested(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            _scan_nested(nested, key_path)
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _scan_nested(nested, f"{path}[{index}]")
    elif isinstance(value, str):
        _scan_string(value, path)


def _scan_string(value: Any, path: str) -> None:
    text = str(value)
    for variant in _decoded_variants(text):
        normalized = _normalize_authority_text(variant)
        compact = _compact_authority_text(variant)
        for token in _FORBIDDEN_VALUE_TOKENS:
            if _normalize_authority_text(token) in normalized:
                raise ValidationError(f"authority-laundering text at {path}: {token}")
        for token in _FORBIDDEN_COMPACT_TOKENS:
            if token in compact:
                raise ValidationError(f"authority-laundering text at {path}: {token}")
        for token in _PROTECTED_PATH_COMPACT:
            if token in compact:
                raise ValidationError(f"protected BLK-req body reference at {path}: {token}")


def _decoded_variants(text: str) -> list[str]:
    variants = [text]
    current = text
    for _ in range(5):
        decoded = unquote(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return variants


def _normalize_authority_text(text: str) -> str:
    chars: list[str] = []
    previous_space = False
    for char in str(text).casefold():
        if char.isalnum():
            chars.append(char)
            previous_space = False
        elif not previous_space:
            chars.append(" ")
            previous_space = True
    return " ".join("".join(chars).split())


def _compact_authority_text(text: str) -> str:
    return "".join(char for char in str(text).casefold() if char.isalnum())
