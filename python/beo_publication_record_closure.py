"""BLK-SYSTEM-151 BEO publication record closure.

This module consumes the exact BLK-SYSTEM-129 metadata-bound external BEO
publication execution record and emits a closure package that is ready for one
separately scoped authoritative signer/storage/ledger finality package. It does
not sign, write storage, append a ledger, generate RTM, reject drift, read
protected bodies, execute runtime tooling, or mutate target/source/Git state.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_execution import (
    EXECUTION_PACKAGE_ID as BLK129_EXECUTION_PACKAGE_ID,
    EXECUTION_STATUS as BLK129_EXECUTION_STATUS,
    EXACT_PROOF_OBLIGATIONS as BLK129_PROOF_OBLIGATIONS,
    RUN_ID as BLK129_RUN_ID,
    SIDE_EFFECT_FLAGS as BLK129_SIDE_EFFECT_FLAGS,
)

CLOSURE_STATUS = "BEO_PUBLICATION_RECORD_CLOSED_FOR_AUTHORITATIVE_FINALITY_REQUEST"
CLOSURE_PACKAGE_ID = "BEO-PUBLICATION-RECORD-CLOSURE-151-001"
CLOSURE_SCOPE = "CLOSE_EXACT_BLK129_PUBLICATION_RECORD_FOR_SIGNER_STORAGE_LEDGER_FINALITY_NOT_EXECUTION"
SELECTED_FRONTIER = "beo_publication_record_closure_for_authoritative_finality"
CANONICAL_BLK129_EXECUTION_PACKAGE_HASH = "sha256:80265ee8e5c5b4011b3e0c0e691f28b7fd74ca1c93b5a7b1d0a877300945af3c"
CANONICAL_BLK129_PUBLICATION_RECORD_HASH = "sha256:19aa4f377c06e103032fea28e91e82bec58f4f0c1f523e2f9797d8ab1df9d798"
NEXT_REQUIRED_AUTHORITY = "EXACT_AUTHORITATIVE_BEO_PUBLICATION_SIGNER_STORAGE_LEDGER_FINALITY_EXECUTION_REQUIRED"

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

EXACT_PROOF_OBLIGATIONS = {
    "BLK129_EXECUTION_PACKAGE_IDENTITY_AND_HASH_BOUND",
    "BLK129_PUBLICATION_RECORD_HASH_BOUND",
    "BEO_AND_BEB_IDENTITIES_BOUND_TO_METADATA_ONLY_TRACE",
    "PUBLICATION_RECORD_CLOSED_BEFORE_SIGNER_STORAGE_LEDGER_FINALITY",
    "SIGNER_STORAGE_LEDGER_FINALITY_NOT_EXECUTED_BY_CLOSURE",
    "RTM_AND_DRIFT_AUTHORITIES_EXCLUDED",
    "PROTECTED_BODY_ACCESS_EXCLUDED",
    "TARGET_SOURCE_GIT_MUTATION_EXCLUDED",
    "HOSTILE_REVIEW_REQUIRED_BEFORE_FINALITY_EXECUTION",
}

EXACT_EXCLUDED_AUTHORITIES = {
    "SIGNER_KEY_MATERIAL_ACCESS_BY_CLOSURE",
    "CRYPTOGRAPHIC_SIGNATURE_GENERATION_BY_CLOSURE",
    "IMMUTABLE_STORAGE_WRITE_BY_CLOSURE",
    "PUBLIC_LEDGER_APPEND_BY_CLOSURE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION",
    "RTM_DRIFT_REJECTION",
    "DRIFT_DECISION",
    "ACTIVE_VAULT_HASH_COMPARISON",
    "COVERAGE_MATRIX_OR_COVERAGE_TRUTH",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "TARGET_REPO_SCAN_OR_MUTATION",
    "SOURCE_OR_GIT_MUTATION_BY_FIXTURE",
    "BEB_DISPATCH",
    "BEO_CLOSEOUT_EXECUTION",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
}

_BLK129_PACKAGE_KEYS = frozenset(
    {
        "execution_status",
        "execution_package_id",
        "operator_identity",
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

_PUBLICATION_RECORD_KEYS = frozenset(
    {
        "publication_mode",
        "published_beo_id",
        "published_beb_id",
        "exact_trace_identities",
        "upstream_request_package_id",
        "upstream_request_package_hash",
        "approval_decision_package_id",
        "approval_capture_package_hash",
        "signature_status",
        "storage_status",
        "ledger_status",
        "rollback_status",
        "rtm_status",
        "publication_record_hash",
    }
)


def build_beo_publication_record_closure(blk129_execution_package: dict[str, Any]) -> dict[str, Any]:
    upstream = _validate_blk129_execution_package(blk129_execution_package)
    closure = {
        "closure_status": CLOSURE_STATUS,
        "closure_package_id": CLOSURE_PACKAGE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_status": upstream["execution_status"],
        "upstream_execution_package_id": upstream["execution_package_id"],
        "upstream_run_id_consumed": upstream["run_id_consumed"],
        "upstream_execution_package_hash": upstream["execution_package_hash"],
        "publication_record_hash": upstream["publication_record_hash"],
        "beo_id": upstream["beo_id"],
        "beb_id": upstream["beb_id"],
        "exact_trace_identities": list(upstream["exact_trace_identities"]),
        "publication_record_state": "CLOSED_FOR_AUTHORITATIVE_SIGNER_STORAGE_LEDGER_FINALITY",
        "signer_storage_ledger_finality_required": True,
        "signer_storage_ledger_finality_executed": False,
        "next_required_authority": NEXT_REQUIRED_AUTHORITY,
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        closure[flag] = False
    closure["closure_package_hash"] = _canonical_hash(
        {key: value for key, value in closure.items() if key != "closure_package_hash"}
    )
    return closure


def _validate_blk129_execution_package(package: Any) -> dict[str, Any]:
    if not isinstance(package, dict):
        raise ValueError("blk129_execution_package must be a dictionary")
    unknown = sorted(set(package) - _BLK129_PACKAGE_KEYS)
    if unknown:
        raise ValueError(f"unexpected field {unknown[0]!r}")
    normalized = deepcopy(package)
    publication_record = _validate_publication_record(normalized.get("publication_record"))
    submitted_record_hash = normalized.get("publication_record_hash")
    if submitted_record_hash != publication_record["publication_record_hash"]:
        raise ValueError("publication_record_hash must match nested publication record")
    if submitted_record_hash != CANONICAL_BLK129_PUBLICATION_RECORD_HASH:
        raise ValueError("BLK-129 publication record must match canonical publication evidence")
    submitted_execution_hash = normalized.get("execution_package_hash")
    recomputed_execution_hash = _canonical_hash(
        {key: value for key, value in normalized.items() if key != "execution_package_hash"}
    )
    if submitted_execution_hash != recomputed_execution_hash:
        raise ValueError("execution_package_hash does not match submitted BLK-129 package")
    early_expected = {
        "execution_status": BLK129_EXECUTION_STATUS,
        "execution_package_id": BLK129_EXECUTION_PACKAGE_ID,
        "run_id_consumed": BLK129_RUN_ID,
        "external_beo_publication_executed": True,
        "future_publication_execution_run_id_consumed": True,
        "beo_publication": "PUBLISHED_EXTERNAL_BEO_RECORD",
        "rtm_status": "NOT_GENERATED",
        "expired": False,
        "replayed": False,
        "stale": False,
    }
    for key, value in early_expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must be {value}")
    for flag in BLK129_SIDE_EFFECT_FLAGS:
        if normalized.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")
    if submitted_execution_hash != CANONICAL_BLK129_EXECUTION_PACKAGE_HASH:
        raise ValueError("BLK-129 execution package must match canonical publication evidence")
    for key, value in {"beo_id": "BEO_126", "beb_id": "BEB_126"}.items():
        if normalized.get(key) != value:
            raise ValueError(f"{key} must be {value}")
    if set(normalized.get("proof_obligations", [])) != set(BLK129_PROOF_OBLIGATIONS):
        raise ValueError("BLK-129 proof_obligations must match exact set")
    return normalized


def _validate_publication_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("publication_record must be a dictionary")
    unknown = sorted(set(record) - _PUBLICATION_RECORD_KEYS)
    if unknown:
        raise ValueError(f"publication_record rejects unexpected field {unknown[0]!r}")
    normalized = deepcopy(record)
    submitted = normalized.get("publication_record_hash")
    recomputed = _canonical_hash({key: value for key, value in normalized.items() if key != "publication_record_hash"})
    if submitted != recomputed:
        raise ValueError("publication_record_hash does not match submitted publication record")
    expected = {
        "publication_mode": "EXTERNAL_BEO_PUBLICATION_RECORD_ONLY",
        "published_beo_id": "BEO_126",
        "published_beb_id": "BEB_126",
        "signature_status": "NOT_SIGNED_NO_KEY_MATERIAL",
        "storage_status": "NOT_WRITTEN_REPOSITORY_RECORD_ONLY",
        "ledger_status": "NOT_APPENDED_REPOSITORY_RECORD_ONLY",
        "rollback_status": "NOT_EXECUTED_POLICY_BOUND_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            raise ValueError(f"publication_record {key} must be {value}")
    return normalized
