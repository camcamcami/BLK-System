"""BLK-SYSTEM-137 active-vault hash-comparison decision package.

This deterministic fixture consumes the exact BLK-SYSTEM-136 post-execution
reconciliation record and selects metadata/hash-only active-vault comparison as
the next narrow authority path. It does not perform the comparison, read or hash
protected requirement bodies, generate RTM, reject drift, establish coverage
truth, run reusable production blk-link, mutate source/Git state, run tooling, or
claim production isolation.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any
from urllib.parse import unquote

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from production_blk_link_rtm_trace_closure_post_execution_reconciliation import (
    RECONCILIATION_PACKAGE_ID as BLK136_RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_STATUS as BLK136_RECONCILIATION_STATUS,
)

DECISION_STATUS = "ACTIVE_VAULT_HASH_COMPARISON_DECISION_PACKAGE_READY_NOT_REQUESTED"
DECISION_PACKAGE_ID = "ACTIVE-VAULT-HASH-COMPARISON-DECISION-137-001"
DECISION_SCOPE = "ACTIVE_VAULT_HASH_COMPARISON_DECISION_ONLY_NO_REQUEST_APPROVAL_OR_EXECUTION"
SELECTED_FRONTIER = "active_vault_hash_comparison_metadata_hash_only_decision"
SELECTED_CAPABILITY = "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON"
NEXT_REQUIRED_AUTHORITY = "EXACT_ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_REQUIRED_NOT_GRANTED"
CANONICAL_BLK136_RECONCILIATION_PACKAGE_HASH = "sha256:aff988888bbd0bb630f63a9463e166264cf6ddfa99c0ebbc958a098b4b30c9c4"

SIDE_EFFECT_FLAGS = (
    "authority_request_emitted",
    "approval_capture_performed",
    "future_run_id_reserved",
    "future_run_id_consumed",
    "active_vault_hash_comparison_performed",
    "active_vault_metadata_read_performed",
    "protected_body_reads",
    "protected_body_copy_attempted",
    "protected_body_hashing_attempted",
    "rtm_generated",
    "rtm_generation_authorized",
    "rtm_drift_rejection_authorized",
    "rtm_drift_rejection_performed",
    "drift_decision_made",
    "coverage_claim_promoted",
    "coverage_matrix_generated",
    "coverage_truth_established",
    "reusable_blk_link_authority_granted",
    "production_blk_link_executed",
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
    "ACTIVE_VAULT_HASH_COMPARISON_EXECUTION_THIS_SPRINT",
    "ACTIVE_VAULT_METADATA_READ_THIS_SPRINT",
    "ACTIVE_VAULT_DRIFT_DECISION_OR_REJECTION",
    "AUTHORITY_REQUEST_CAPTURE_THIS_SPRINT",
    "APPROVAL_CAPTURE_THIS_SPRINT",
    "FUTURE_RUN_ID_RESERVATION_THIS_SPRINT",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "RUNTIME_RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_MATRIX_GENERATION",
    "COVERAGE_TRUTH_OR_CLAIM_PROMOTION",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
    "PRODUCTION_BLK_LINK_EXECUTION",
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

EXACT_PROOF_OBLIGATIONS = {
    "BLK136_RECONCILIATION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK135_EXECUTION_RECORD_BOUND_THROUGH_BLK136",
    "ONE_FRONTIER_SELECTED_ONLY",
    "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON_SELECTED",
    "COMPARISON_NOT_PERFORMED_BY_DECISION",
    "AUTHORITY_REQUEST_NOT_EMITTED_BY_DECISION",
    "APPROVAL_CAPTURE_NOT_PERFORMED_BY_DECISION",
    "PROTECTED_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION_EXCLUDED",
    "RTM_GENERATION_NOT_AUTHORIZED_BY_DECISION",
    "DRIFT_REJECTION_AND_AUTHORITATIVE_DRIFT_DECISION_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "REUSABLE_PRODUCTION_BLK_LINK_EXCLUDED",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_AUTHORITY_REQUEST",
}

_CONTEXT_KEYS = frozenset(
    {
        "decision_package_id",
        "operator_identity",
        "decision_scope",
        "selected_frontier",
        "upstream_reconciliation_package_id",
        "upstream_reconciliation_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_execution_record_id",
        "upstream_execution_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "decided_at",
        "stale",
        "replayed",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        *SIDE_EFFECT_FLAGS,
    }
)

_ATTESTATION_KEYS = frozenset(
    {
        "exact_blk136_reconciliation_reviewed",
        "selected_one_frontier_only",
        "metadata_hash_only_active_vault_comparison_selected",
        "no_active_vault_comparison_performed",
        "no_protected_body_reads",
        "no_rtm_generation",
        "no_drift_rejection",
        "no_coverage_truth",
        "no_reusable_blk_link_authority",
        "no_beb_dispatch_or_beo_closeout",
        "no_signer_storage_ledger_side_effects",
        "no_target_source_git_mutation",
        "no_blk_pipe_blk_test_codex_tooling",
        "no_production_isolation_claim",
    }
)

_RECONCILIATION_REQUIRED_KEYS = frozenset(
    {
        "reconciliation_status",
        "reconciliation_package_id",
        "operator_identity",
        "reconciliation_scope",
        "selected_frontier",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_execution_record_id",
        "upstream_execution_record_hash",
        "run_id_consumed",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "next_frontier",
        "current_state_index_reconciled",
        "roadmap_reconciled",
        "runbook_vocabulary_reconciled",
        "reconciliation_context_hash",
        "reconciled_at",
        "stale",
        "replayed",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "reconciliation_package_hash",
    }
)

_DENIED_NORMALIZED_TOKENS = (
    "rtmgeneration",
    "rtmgenerated",
    "generatertm",
    "rtmdriftrejection",
    "driftrejectionexecuted",
    "authoritativedriftddecision",
    "authoritativedriftdecision",
    "coveragematrix",
    "coveragetruth",
    "protectedbodyread",
    "protectedbodycopy",
    "protectedbodyhash",
    "protectedbodytext",
    "blkreqbody",
    "reqbody",
    "bodytext",
    "beopublication",
    "publishbeo",
    "authoritativebeopublication",
    "beocloseout",
    "bebdispatch",
    "reusableproductionblklink",
    "productionblklinkexecuted",
    "publicledgermutation",
    "immutablestoragewrite",
    "cryptographicsigning",
    "signaturegenerated",
    "signerkeymaterial",
    "keymaterial",
    "privatekey",
    "apikey",
    "codexapproval",
    "blkpipesuccess",
    "blktestpassapproval",
    "livecodexexecution",
    "sourcemutation",
    "gitmutation",
    "packagemanager",
    "networktooling",
    "browsertooling",
    "cybertooling",
    "productionisolation",
)
_PROTECTED_BODY_TOKENS = ("thesystemshall", "docsrequirementsactive", "docsactive", "requirementsactive")


def build_active_vault_hash_comparison_decision_package(
    reconciliation_package: dict[str, Any], decision_context: dict[str, Any]
) -> dict[str, Any]:
    upstream = _validate_reconciliation_package(reconciliation_package)
    context = _validate_decision_context(decision_context, upstream)
    trace_identities = list(upstream["exact_trace_identities"])
    package = {
        "decision_status": DECISION_STATUS,
        "decision_package_id": DECISION_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "selected_capability": SELECTED_CAPABILITY,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_execution_record_id": upstream["upstream_execution_record_id"],
        "upstream_execution_record_hash": upstream["upstream_execution_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": trace_identities,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "decision_context_hash": _canonical_hash(context),
        "decided_at": context["decided_at"],
        "stale": False,
        "replayed": False,
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["decision_package_hash"] = _canonical_hash(package)
    return package


def _validate_reconciliation_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("reconciliation package must be a dictionary")
    missing = sorted(_RECONCILIATION_REQUIRED_KEYS - set(package))
    if missing:
        raise ValueError(f"reconciliation package missing fields: {missing}")
    submitted_hash = _required_hash(package.get("reconciliation_package_hash"), "reconciliation_package_hash")
    actual_hash = _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"})
    if submitted_hash != actual_hash:
        raise ValueError("reconciliation_package_hash does not match submitted BLK-136 package")
    if submitted_hash != CANONICAL_BLK136_RECONCILIATION_PACKAGE_HASH:
        raise ValueError("canonical BLK-136 reconciliation package hash required")
    if package.get("reconciliation_package_id") != BLK136_RECONCILIATION_PACKAGE_ID:
        raise ValueError("reconciliation_package_id must match exact BLK-136 package")
    if package.get("reconciliation_status") != BLK136_RECONCILIATION_STATUS:
        raise ValueError("reconciliation_status must match BLK-136 record-only status")
    _validate_exact_trace_identities(package.get("exact_trace_identities"))
    if package.get("stale") is not False or package.get("replayed") is not False:
        raise ValueError("BLK-136 reconciliation package must not be stale or replayed")
    return deepcopy(package)


def _validate_decision_context(context: Any, upstream: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("decision context must be a dictionary")
    unknown = sorted(set(context) - _CONTEXT_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_CONTEXT_KEYS - set(context))
    if missing:
        raise ValueError(f"decision context missing fields: {missing}")
    scan_context = {
        key: value
        for key, value in context.items()
        if key not in {"operator_attestation", "proof_obligations", "excluded_authorities"}
    }
    _scan_value_strings(scan_context, "decision_context", allow_selected=True)
    expected = {
        "decision_package_id": DECISION_PACKAGE_ID,
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_reconciliation_package_id": upstream["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": upstream["reconciliation_package_hash"],
        "upstream_execution_package_id": upstream["upstream_execution_package_id"],
        "upstream_execution_package_hash": upstream["upstream_execution_package_hash"],
        "upstream_execution_record_id": upstream["upstream_execution_record_id"],
        "upstream_execution_record_hash": upstream["upstream_execution_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
    }
    for key, value in expected.items():
        if context.get(key) != value:
            raise ValueError(f"{key} must be {value!r}")
    if context.get("operator_identity") != upstream.get("operator_identity"):
        raise ValueError("operator_identity must match BLK-136 reconciliation package")
    if context.get("exact_trace_identities") != upstream.get("exact_trace_identities"):
        raise ValueError("exact_trace_identities must match BLK-136 reconciliation package")
    _validate_exact_trace_identities(context.get("exact_trace_identities"))
    decided_at = _parse_timestamp(context.get("decided_at"), "decided_at")
    if decided_at < datetime.fromisoformat("2099-01-01T00:00:00+00:00"):
        raise ValueError("decision context must not be calendar-stale")
    if context.get("stale") is not False:
        raise ValueError("decision context must not be stale")
    if context.get("replayed") is not False:
        raise ValueError("decision context must not be replayed")
    attestation = context.get("operator_attestation")
    if not isinstance(attestation, dict):
        raise ValueError("operator_attestation must be a dictionary")
    unknown_attestation = sorted(set(attestation) - _ATTESTATION_KEYS)
    if unknown_attestation:
        raise ValueError(f"unexpected field {unknown_attestation[0]!r}")
    missing_attestation = sorted(_ATTESTATION_KEYS - set(attestation))
    if missing_attestation:
        raise ValueError(f"operator_attestation missing fields: {missing_attestation}")
    for key in _ATTESTATION_KEYS:
        if attestation.get(key) is not True:
            raise ValueError(f"operator_attestation.{key} must be true")
    _required_exact_set(context.get("proof_obligations"), EXACT_PROOF_OBLIGATIONS, "proof_obligations")
    _required_exact_set(context.get("excluded_authorities"), EXACT_EXCLUDED_AUTHORITIES, "excluded_authorities")
    for flag in SIDE_EFFECT_FLAGS:
        if context.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    return deepcopy(context)


def _required_exact_set(value: Any, required: set[str], field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field} must match exact set")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")
    if set(value) != required:
        raise ValueError(f"{field} must match exact denied authority set" if field == "excluded_authorities" else f"{field} must match exact set")
    return sorted(value)


def _required_hash(value: Any, field: str) -> str:
    if not isinstance(value, str) or len(value) != 71 or not value.startswith("sha256:"):
        raise ValueError(f"{field} must be canonical sha256")
    digest = value.split(":", 1)[1]
    if any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError(f"{field} must be canonical sha256")
    return value


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed


def _scan_value_strings(value: Any, label: str, allow_selected: bool = False) -> None:
    if isinstance(value, str):
        _scan_string(value, label, allow_selected=allow_selected)
    elif isinstance(value, dict):
        for key, nested in value.items():
            _scan_value_strings(nested, f"{label}.{key}", allow_selected=allow_selected)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _scan_value_strings(nested, f"{label}[{index}]", allow_selected=allow_selected)


def _scan_string(value: str, label: str, allow_selected: bool = False) -> None:
    variants = _decode_variants(value)
    normalized_variants = [_normalize(variant) for variant in variants]
    if any(token in normalized for normalized in normalized_variants for token in _PROTECTED_BODY_TOKENS):
        raise ValueError(f"protected body text in {label}")
    for normalized in normalized_variants:
        for token in _DENIED_NORMALIZED_TOKENS:
            if token in normalized:
                raise ValueError(f"authority-laundering text in {label}")
    if "approvedforproduction" in " ".join(normalized_variants) or "greenlit" in " ".join(normalized_variants):
        raise ValueError(f"authority-laundering text in {label}")


def _decode_variants(value: str) -> list[str]:
    variants = [value]
    current = value
    for _ in range(6):
        decoded = unquote(current)
        variants.append(decoded)
        if decoded == current:
            break
        current = decoded
    return variants


def _normalize(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isascii() and ch.isalnum())
