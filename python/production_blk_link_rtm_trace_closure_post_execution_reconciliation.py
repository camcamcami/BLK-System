"""BLK-SYSTEM-136 post-execution reconciliation for production trace closure.

This deterministic fixture consumes the exact BLK-SYSTEM-135 record-only
production blk-link / RTM trace-closure evidence and emits reconciliation
evidence only. It reconciles roadmap/current-state/runbook vocabulary without
grading record-only evidence into reusable production blk-link authority, RTM
generation, drift rejection, active-vault comparison, coverage truth,
protected-body access, signer/storage/ledger behavior, tooling/runtime, or
production-isolation claims.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_approval_capture import _validate_exact_trace_identities
from metadata_bound_rtm_trace_closure_approval_capture import (
    _parse_timestamp,
    _required_exact_set,
    _required_hash,
    _scan_value_strings,
)
from production_blk_link_rtm_trace_closure_execution_record import (
    EXECUTION_PACKAGE_ID as BLK135_EXECUTION_PACKAGE_ID,
    EXECUTION_RECORD_ID as BLK135_EXECUTION_RECORD_ID,
    EXECUTION_SCOPE as BLK135_EXECUTION_SCOPE,
    EXECUTION_STATUS as BLK135_EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as BLK135_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS as BLK135_PROOF_OBLIGATIONS,
    RUN_ID_CONSUMED as BLK135_RUN_ID_CONSUMED,
    SELECTED_FRONTIER as BLK135_SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS as BLK135_SIDE_EFFECT_FLAGS,
)

RECONCILIATION_STATUS = "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_EXECUTION_RECONCILED_FOR_EXACT_BLK135_RECORD_ONLY"
RECONCILIATION_PACKAGE_ID = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-001"
RECONCILIATION_SCOPE = "POST_EXECUTION_RECONCILIATION_ONLY_NO_NEW_RUNTIME_AUTHORITY"
SELECTED_FRONTIER = "production_blk_link_rtm_trace_closure_post_execution_reconciliation"
NEXT_FRONTIER = "NEXT_FRONTIER_NARROW_AUTHORITY_DECISION_AFTER_RECONCILIATION_NOT_GRANTED"
CANONICAL_BLK135_EXECUTION_PACKAGE_HASH = "sha256:4aeabf039037c8bc2f4ff61e271127df7f48698cd299a0901b88cc757f7d725a"
CANONICAL_BLK135_EXECUTION_RECORD_HASH = "sha256:d001e2dde10027884e071627d7ea8d572b99991a45f32612f1b906acfda161d8"
FIXTURE_EVALUATION_AT = datetime.fromisoformat("2026-05-15T15:34:48+10:00")

SIDE_EFFECT_FLAGS = (
    "reusable_blk_link_authority_granted",
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
    "POST_EXECUTION_RECONCILIATION_AS_RUNTIME_AUTHORITY",
    "REUSABLE_PRODUCTION_BLK_LINK_EXECUTION_AUTHORITY",
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
    "BLK135_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK135_EXECUTION_RECORD_IDENTITY_AND_HASH_BOUND",
    "BLK134_APPROVAL_CAPTURE_IDENTITY_AND_HASH_BOUND_THROUGH_BLK135",
    "RUN_ID_CONSUMPTION_RECONCILED_AS_RECORD_ONLY_EVIDENCE",
    "ROADMAP_NEXT_FRONTIER_RECONCILED_AFTER_EXECUTION_RECORD",
    "CURRENT_STATE_INDEX_RECONCILED_AFTER_EXECUTION_RECORD",
    "RUNBOOK_VOCABULARY_RECONCILED_AFTER_EXECUTION_RECORD",
    "REUSABLE_BLK_LINK_AUTHORITY_EXCLUDED",
    "RTM_GENERATION_NOT_AUTHORIZED_BY_RECONCILIATION",
    "DRIFT_REJECTION_AND_DRIFT_DECISION_EXCLUDED",
    "ACTIVE_VAULT_HASH_COMPARISON_EXCLUDED",
    "COVERAGE_TRUTH_EXCLUDED",
    "PROTECTED_BODY_NO_READ_GUARANTEE_BOUND",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_NO_SIDE_EFFECTS_CONFIRMED",
    "TARGET_REPO_SCAN_AND_MUTATION_EXCLUDED",
    "NEXT_AUTHORITY_DECISION_REQUIRED_BEFORE_ANY_NEW_RUNG",
}

_EXECUTION_PACKAGE_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "operator_identity",
        "execution_scope",
        "selected_frontier",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "run_id_consumed",
        "future_run_id_consumed",
        "execution_request_hash",
        "requested_at",
        "expires_at",
        "expired",
        "replayed",
        "stale",
        "upstream_authority_request_package_id",
        "upstream_authority_request_package_hash",
        "upstream_execution_package_id",
        "upstream_execution_package_hash",
        "upstream_trace_closure_record_id",
        "upstream_trace_closure_record_hash",
        "publication_record_hash",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "execution_record_id",
        "execution_record",
        "execution_record_hash",
        "production_blk_link_rtm_trace_closure_record_emitted",
        "next_required_authority",
        "operator_attestation",
        "proof_obligations",
        "excluded_authorities",
        "execution_package_hash",
        *BLK135_SIDE_EFFECT_FLAGS,
    }
)

_EXECUTION_RECORD_KEYS = frozenset(
    {
        "execution_record_id",
        "consumed_run_id",
        "approval_capture_package_id",
        "approval_capture_package_hash",
        "approval_id",
        "trace_closure_authority",
        "beo_id",
        "beb_id",
        "exact_trace_identities",
        "recorded_at",
        "reusable_blk_link_authority_granted",
        "rtm_generated",
        "rtm_drift_rejection_performed",
        "active_vault_hash_comparison_performed",
        "coverage_truth_established",
        "protected_body_reads",
        "public_ledger_mutation",
        "execution_record_hash",
    }
)

_RECONCILIATION_CONTEXT_KEYS = frozenset(
    {
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
        "reconciled_at",
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
        "exact_blk135_execution_package_reviewed",
        "roadmap_vocabulary_reconciled",
        "current_state_index_reconciled",
        "runbook_vocabulary_reconciled",
        "record_only_trace_closure_preserved",
        "no_reusable_blk_link_authority_claim",
        "rtm_generation_not_authorized",
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


def build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(
    execution_package: dict[str, Any], reconciliation_context: dict[str, Any]
) -> dict[str, Any]:
    """Reconcile exact BLK-135 record-only evidence without granting new authority."""

    execution = _validate_execution_package(execution_package)
    context = _validate_reconciliation_context(reconciliation_context, execution)
    trace_identities = list(execution["exact_trace_identities"])
    package = {
        "reconciliation_status": RECONCILIATION_STATUS,
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": context["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_execution_record_id": execution["execution_record_id"],
        "upstream_execution_record_hash": execution["execution_record_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "approval_capture_package_id": execution["approval_capture_package_id"],
        "approval_capture_package_hash": execution["approval_capture_package_hash"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": trace_identities,
        "reconciled_at": context["reconciled_at"],
        "replayed": False,
        "stale": False,
        "current_state_index_reconciled": True,
        "roadmap_reconciled": True,
        "runbook_vocabulary_reconciled": True,
        "record_only_trace_closure_preserved": True,
        "next_frontier": NEXT_FRONTIER,
        "reconciliation_context_hash": _canonical_hash(context),
        "operator_attestation": deepcopy(context["operator_attestation"]),
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        package[flag] = False
    package["reconciliation_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "reconciliation_package_hash"}
    )
    return package


def _validate_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("execution_package must be a dictionary")
    unknown = sorted(set(package) - _EXECUTION_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"execution_package rejects unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_PACKAGE_KEYS - set(package))
    if missing:
        raise ValueError(f"execution_package missing field {missing[0]!r}")
    normalized = deepcopy(package)
    submitted_hash = _required_hash(normalized.get("execution_package_hash"), "execution_package_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_package_hash"})
    if submitted_hash != recomputed:
        raise ValueError("execution_package_hash does not match submitted BLK-135 package")
    if submitted_hash != CANONICAL_BLK135_EXECUTION_PACKAGE_HASH:
        raise ValueError("execution package must match canonical BLK-135 execution package")
    record = _validate_execution_record(normalized.get("execution_record"))
    if record["execution_record_hash"] != normalized.get("execution_record_hash"):
        raise ValueError("execution_record_hash must match nested BLK-135 record")
    expected = {
        "execution_status": BLK135_EXECUTION_STATUS,
        "execution_package_id": BLK135_EXECUTION_PACKAGE_ID,
        "execution_scope": BLK135_EXECUTION_SCOPE,
        "selected_frontier": BLK135_SELECTED_FRONTIER,
        "approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001",
        "approval_capture_package_hash": "sha256:284bd944f7e854a9c589e923908053da37e27ce9c32d841090578837111e49bf",
        "approval_id": "APPROVAL-BLK-SYSTEM-133-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001",
        "run_id_consumed": BLK135_RUN_ID_CONSUMED,
        "future_run_id_consumed": True,
        "upstream_authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001",
        "upstream_authority_request_package_hash": "sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271",
        "upstream_execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-001",
        "upstream_execution_package_hash": "sha256:548934403cd71a4eebc27c4e164a43f9e2d7f71b8cfab7765b1f51e65f44fed5",
        "upstream_trace_closure_record_id": "RTM-TRACE-CLOSURE-RECORD-132-001",
        "upstream_trace_closure_record_hash": "sha256:2b78924d8d839dff65c2137cabf09362a23feec24fa21010238ef8c48703c3ca",
        "publication_record_hash": "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
        "execution_record_id": BLK135_EXECUTION_RECORD_ID,
        "execution_record_hash": CANONICAL_BLK135_EXECUTION_RECORD_HASH,
        "production_blk_link_rtm_trace_closure_record_emitted": True,
        "next_required_authority": "POST_EXECUTION_RECONCILIATION_REQUIRED_NOT_STARTED",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("execution package must match canonical BLK-135 execution package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("execution package trace identities must match canonical BLK-135 package")
    if tuple(normalized.get("exact_trace_identities", ())) != (
        "REQ:REQ-001:sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "UC:UC-001:sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    ):
        raise ValueError("execution package trace identities must match canonical BLK-135 package")
    for flag in ("expired", "replayed", "stale"):
        if normalized.get(flag) is not False:
            raise ValueError(f"BLK-135 execution package must not be {flag}")
    for flag in BLK135_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"execution package {flag} must remain false")
    _required_exact_set(normalized.get("proof_obligations"), BLK135_PROOF_OBLIGATIONS, "execution_package proof_obligations")
    _required_exact_set(normalized.get("excluded_authorities"), BLK135_EXCLUDED_AUTHORITIES, "execution_package excluded_authorities")
    return normalized


def _validate_execution_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("execution_record must be a dictionary")
    unknown = sorted(set(record) - _EXECUTION_RECORD_KEYS)
    if unknown:
        raise ValueError(f"execution_record rejects unexpected field {unknown[0]!r}")
    missing = sorted(_EXECUTION_RECORD_KEYS - set(record))
    if missing:
        raise ValueError(f"execution_record missing field {missing[0]!r}")
    normalized = deepcopy(record)
    submitted_hash = _required_hash(normalized.get("execution_record_hash"), "execution_record_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "execution_record_hash"})
    if submitted_hash != recomputed or submitted_hash != CANONICAL_BLK135_EXECUTION_RECORD_HASH:
        raise ValueError("execution_record_hash does not match canonical BLK-135 record")
    expected = {
        "execution_record_id": BLK135_EXECUTION_RECORD_ID,
        "consumed_run_id": BLK135_RUN_ID_CONSUMED,
        "approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-001",
        "approval_capture_package_hash": "sha256:284bd944f7e854a9c589e923908053da37e27ce9c32d841090578837111e49bf",
        "approval_id": "APPROVAL-BLK-SYSTEM-133-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001",
        "trace_closure_authority": "EXACT_APPROVED_PRODUCTION_TRACE_CLOSURE_RECORD_ONLY",
        "beo_id": "BEO_126",
        "beb_id": "BEB_126",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError("execution_record must match canonical BLK-135 record")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != normalized.get("exact_trace_identities"):
        raise ValueError("execution_record trace identities must match canonical BLK-135 record")
    for flag in (
        "reusable_blk_link_authority_granted",
        "rtm_generated",
        "rtm_drift_rejection_performed",
        "active_vault_hash_comparison_performed",
        "coverage_truth_established",
        "protected_body_reads",
        "public_ledger_mutation",
    ):
        if normalized.get(flag) is not False:
            raise ValueError(f"execution_record {flag} must remain false")
    return normalized


def _validate_reconciliation_context(context: Any, execution: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(context, dict):
        raise ValueError("reconciliation_context must be a dictionary")
    unknown = sorted(set(context) - _RECONCILIATION_CONTEXT_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    missing = sorted(_RECONCILIATION_CONTEXT_KEYS - set(context))
    if missing:
        raise ValueError(f"reconciliation_context missing field {missing[0]!r}")
    normalized = deepcopy(context)
    for key in (
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
    ):
        _scan_value_strings(normalized.get(key), key)
    if normalized.get("reconciliation_package_id") != RECONCILIATION_PACKAGE_ID:
        raise ValueError(f"reconciliation_package_id must be {RECONCILIATION_PACKAGE_ID}")
    if normalized.get("operator_identity") != execution["operator_identity"]:
        raise ValueError("operator_identity must match BLK-135 execution package")
    if normalized.get("reconciliation_scope") != RECONCILIATION_SCOPE:
        raise ValueError(f"reconciliation_scope must be {RECONCILIATION_SCOPE}")
    if normalized.get("selected_frontier") != SELECTED_FRONTIER:
        raise ValueError(f"selected_frontier must be {SELECTED_FRONTIER}")
    if normalized.get("run_id_consumed") != BLK135_RUN_ID_CONSUMED:
        raise ValueError(f"run_id_consumed must be {BLK135_RUN_ID_CONSUMED}")
    expected = {
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_execution_record_id": execution["execution_record_id"],
        "upstream_execution_record_hash": execution["execution_record_hash"],
        "approval_capture_package_id": execution["approval_capture_package_id"],
        "approval_capture_package_hash": execution["approval_capture_package_hash"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must match BLK-135 execution package")
    if _validate_exact_trace_identities(normalized.get("exact_trace_identities")) != execution["exact_trace_identities"]:
        raise ValueError("exact_trace_identities must match BLK-135 execution package")
    for flag in SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    for flag in ("stale", "replayed"):
        if normalized.get(flag) is not False:
            raise ValueError(f"reconciliation context must not be {flag}")
    reconciled_at = _parse_timestamp(normalized.get("reconciled_at"), "reconciled_at")
    if reconciled_at <= FIXTURE_EVALUATION_AT.astimezone(reconciled_at.tzinfo):
        raise ValueError("reconciliation context must not be calendar-stale")
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
