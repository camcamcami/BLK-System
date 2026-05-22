"""BLK-SYSTEM-330..333 exact BEO side effect and trace closure.

This package consumes the BLK-SYSTEM-329 receipt/replay kernel and the latest
operator direction for one exact current-chain transition. It records official
BEO metadata for the verified loop, then closes RTM / ``blk-link`` traceability
from that metadata. It does not grant reusable publication, signer, storage,
ledger, RTM-generation, production ``blk-link``, drift/coverage, protected-body,
runtime/tooling, or non-BLK-System mutation authority.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    _hash_text,
    hash_package,
)
from verified_loop_beo_publication_bounded_execution_kernel_329 import (
    EXPECTED_329_EXECUTION_KERNEL_HASH,
    validate_verified_loop_beo_publication_bounded_execution_kernel_329,
)


class VerifiedLoopBeoPublicationTraceClosure330333ValidationError(ValueError):
    """Raised when BLK-SYSTEM-330..333 evidence crosses a boundary."""


OPERATOR_DIRECTIVE_330 = (
    "Build the exact BEO publication side-effect package.\n\n"
    "Once that works cleanly:\n\n"
    "Use that official BEO metadata to make blk-link / RTM traceability "
    "actually close the loop."
)
RUN_ID_330 = "RUN-BLK-SYSTEM-330-VERIFIED-LOOP-BEO-PUBLICATION-001"
BEO_ID_330 = "BEO-BLK-SYSTEM-330-VERIFIED-LOOP-001"
BEB_ID_330 = "BEB-BLK-SYSTEM-294-297-QUARANTINE-GATED-LOOP-001"
RTM_TRACE_CLOSURE_RUN_ID_332 = "RUN-BLK-SYSTEM-332-RTM-BLK-LINK-TRACE-CLOSURE-001"
RTM_TRACE_CLOSURE_ID_332 = "RTM-BLK-LINK-TRACE-CLOSURE-332-001"
NEXT_FRONTIER_333 = (
    "NEXT_FRONTIER_ONE_EXACT_BEO_TO_RTM_BLK_LINK_TRACE_CLOSED_"
    "REUSABLE_AUTHORITY_NOT_GRANTED"
)

EXPECTED_330_EXECUTION_PACKAGE_HASH: str | None = (
    "sha256:64074ea37ce818197d6a4a376725ac86bdb6958da5b3a175c3aadad1fa19a4ed"
)
EXPECTED_331_RECONCILIATION_HASH: str | None = (
    "sha256:7b078329fe657b34ccbc0343ad73d49cb13a9c4e0ab19132206efd1b093b28bf"
)
EXPECTED_332_TRACE_CLOSURE_PACKAGE_HASH: str | None = (
    "sha256:d353513147b0fb5ec6ea7dc60d7b16701b280a3c3bb80c6e943dce5bcde83ef4"
)
EXPECTED_333_RECONCILIATION_HASH: str | None = (
    "sha256:0cf714e86b0dcff83460dcaaa34597eaf8ad887934de21019fc2107ebef6dfa4"
)

_EXECUTION_SCOPE_330 = "one_exact_verified_loop_beo_metadata_publication_record"
_RECONCILIATION_SCOPE_331 = "official_beo_metadata_ready_for_trace_closure"
_TRACE_SCOPE_332 = "one_exact_rtm_blk_link_trace_closure_from_official_beo_metadata"

_MARKERS_330 = (
    "BLK_SYSTEM_330_VERIFIED_LOOP_BEO_PUBLICATION_SIDE_EFFECT_PACKAGE_EXECUTED",
    "ONE_EXACT_OFFICIAL_BEO_METADATA_RECORD",
    "NO_REUSABLE_BEO_RTM_BLK_LINK_AUTHORITY",
)
_MARKERS_331 = (
    "BLK_SYSTEM_331_VERIFIED_LOOP_BEO_PUBLICATION_FINALITY_RECONCILED",
    "OFFICIAL_BEO_METADATA_READY_FOR_RTM_BLK_LINK_TRACE_CLOSURE",
    "NO_REUSABLE_BEO_RTM_BLK_LINK_AUTHORITY",
)
_MARKERS_332 = (
    "BLK_SYSTEM_332_RTM_BLK_LINK_TRACE_CLOSURE_RECORDED_FROM_OFFICIAL_BEO_METADATA",
    "METADATA_ONLY_TRACEABILITY_LOOP_CLOSED",
    "NO_REUSABLE_RTM_BLK_LINK_OR_TRUTH_AUTHORITY",
)
_MARKERS_333 = (
    "BLK_SYSTEM_333_RTM_BLK_LINK_TRACE_CLOSURE_RECONCILED",
    NEXT_FRONTIER_333,
    "NO_REUSABLE_RUNTIME_OR_TRUTH_AUTHORITY",
)

_DENIED_AUTHORITIES_330 = (
    "OPERATOR_DIRECTIVE_REUSE_OR_RETARGETING",
    "SECOND_BEO_PUBLICATION_RUN_OR_RUN_ID_REPLAY",
    "REUSABLE_BEO_PUBLICATION_AUTHORITY",
    "BEO_CLOSEOUT_EXECUTION",
    "SIGNER_KEY_MATERIAL_ACCESS",
    "CRYPTOGRAPHIC_SIGNATURE_GENERATION",
    "EXTERNAL_IMMUTABLE_STORAGE_WRITE",
    "EXTERNAL_PUBLIC_LEDGER_APPEND",
    "SIGNER_STORAGE_LEDGER_REUSE",
    "ROLLBACK_REVOCATION_SUPERSESSION_EXECUTION",
    "RTM_GENERATION_OR_REUSABLE_RTM_GENERATION",
    "PRODUCTION_BLK_LINK_RUNTIME_OR_REUSABLE_AUTHORITY",
    "DRIFT_REJECTION_OR_COVERAGE_TRUTH",
    "ACTIVE_VAULT_COMPARISON_OR_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "BEB_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION_OUTSIDE_BLK_SYSTEM_DEVELOPMENT",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)
_DENIED_AUTHORITIES_332 = (
    "RTM_TRACE_CLOSURE_REUSE_OR_RETARGETING",
    "SECOND_RTM_BLK_LINK_TRACE_CLOSURE_RUN_OR_RUN_ID_REPLAY",
    "RUNTIME_RTM_GENERATION",
    "REUSABLE_RTM_GENERATION",
    "REUSABLE_PRODUCTION_BLK_LINK_AUTHORITY",
    "PRODUCTION_BLK_LINK_RUNTIME_BEYOND_EXACT_METADATA_RECORD",
    "DRIFT_REJECTION_OR_AUTHORITATIVE_DRIFT_DECISION",
    "COVERAGE_TRUTH_OR_COVERAGE_MATRIX_GENERATION",
    "ACTIVE_VAULT_COMPARISON_OR_SCAN",
    "PROTECTED_BLK_REQ_BODY_READ_COPY_PARSE_HASH_SCAN_MUTATION",
    "SIGNER_STORAGE_LEDGER_ROLLBACK_SIDE_EFFECTS",
    "BEO_PUBLICATION_REUSE_OR_SECOND_PUBLICATION",
    "BEO_CLOSEOUT_EXECUTION",
    "BLK_PIPE_BLK_TEST_CODEX_RUNTIME",
    "BEB_DISPATCH",
    "TARGET_SOURCE_GIT_MUTATION_OUTSIDE_BLK_SYSTEM_DEVELOPMENT",
    "PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING",
    "PRODUCTION_ISOLATION_CLAIM",
)

_SIDE_EFFECTS_330 = {
    **_FALSE_SIDE_EFFECTS,
    "run_id_consumed": True,
    "beo_publication": True,
    "authoritative_beo_publication": True,
    "official_beo_metadata_recorded": True,
    "rtm_blk_link_trace_closure_input_ready": False,
}
_SIDE_EFFECTS_331 = {
    **_SIDE_EFFECTS_330,
    "rtm_blk_link_trace_closure_input_ready": True,
}
_SIDE_EFFECTS_332 = {
    **_FALSE_SIDE_EFFECTS,
    "rtm_blk_link_trace_closure_recorded": True,
    "traceability_loop_closed": True,
    "runtime_rtm_generation": False,
    "reusable_rtm_generation": False,
    "reusable_production_blk_link": False,
    "active_vault_comparison": False,
}
_SIDE_EFFECTS_333 = dict(_SIDE_EFFECTS_332)

_KEYS_330 = frozenset(
    {
        "status",
        "markers",
        "upstream_execution_kernel_hash",
        "operator_directive_hash",
        "run_id_consumed",
        "run_id_replay_evidence",
        "requested_at",
        "executed_at",
        "expires_at",
        "execution_scope",
        "execution_request_hash",
        "signature_receipt",
        "signature_receipt_hash",
        "immutable_storage_receipt",
        "immutable_storage_receipt_hash",
        "public_ledger_entry",
        "public_ledger_entry_hash",
        "official_beo_metadata",
        "official_beo_metadata_hash",
        "beo_finality_record",
        "beo_finality_record_hash",
        "denied_authorities",
        "side_effects",
        "execution_package_hash",
    }
)
_KEYS_331 = frozenset(
    {
        "status",
        "markers",
        "execution_package_hash",
        "official_beo_metadata",
        "official_beo_metadata_hash",
        "beo_finality_record_hash",
        "signature_receipt_hash",
        "immutable_storage_receipt_hash",
        "public_ledger_entry_hash",
        "reconciliation_scope",
        "denied_authorities",
        "side_effects",
        "reconciliation_hash",
    }
)
_KEYS_332 = frozenset(
    {
        "status",
        "markers",
        "upstream_reconciliation_hash",
        "official_beo_metadata",
        "official_beo_metadata_hash",
        "beo_finality_record_hash",
        "trace_closure_id",
        "run_id_consumed",
        "run_id_replay_evidence",
        "requested_at",
        "executed_at",
        "expires_at",
        "execution_scope",
        "trace_closure_request_hash",
        "trace_closure_record",
        "trace_closure_record_hash",
        "denied_authorities",
        "side_effects",
        "trace_closure_package_hash",
    }
)
_KEYS_333 = frozenset(
    {
        "status",
        "markers",
        "trace_closure_package_hash",
        "trace_closure_record_hash",
        "official_beo_metadata_hash",
        "next_frontier",
        "denied_authorities",
        "side_effects",
        "reconciliation_hash",
    }
)


def execute_verified_loop_beo_publication_side_effect_package_330(
    kernel_329: dict[str, Any],
    *,
    operator_directive: str,
    requested_at: str,
    executed_at: str,
    expires_at: str,
    used_run_ids: tuple[str, ...] | list[str] = (),
) -> dict[str, Any]:
    """Record one exact official BEO metadata package from the 329 kernel."""

    try:
        kernel = validate_verified_loop_beo_publication_bounded_execution_kernel_329(kernel_329)
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"kernel validation failed: {exc}"
        ) from exc
    if operator_directive != OPERATOR_DIRECTIVE_330:
        _reject_freeform(operator_directive, "operator_directive", _DENIED_AUTHORITIES_330)
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            "operator_directive mismatch"
        )
    _require_window(requested_at, executed_at, expires_at)
    run_id_replay_evidence = _build_run_id_replay_evidence(
        RUN_ID_330,
        used_run_ids,
        "BLK-SYSTEM-330",
    )
    run_id_replay_evidence_hash = hash_package(run_id_replay_evidence)

    execution_request_hash = hash_package(
        {
            "upstream_execution_kernel_hash": kernel["execution_kernel_hash"],
            "operator_directive_hash": _hash_text(operator_directive),
            "run_id": RUN_ID_330,
            "run_id_replay_evidence_hash": run_id_replay_evidence_hash,
            "requested_at": requested_at,
            "executed_at": executed_at,
            "expires_at": expires_at,
            "execution_scope": _EXECUTION_SCOPE_330,
        }
    )
    signature_receipt = {
        "receipt_status": "SIGNATURE_RECEIPT_REPOSITORY_EVIDENCE_RECORDED",
        "receipt_scope": "deterministic_metadata_only_no_signer_key_material",
        "execution_request_hash": execution_request_hash,
        "run_id": RUN_ID_330,
        "signer_key_material_accessed": False,
        "signature_generated": False,
    }
    signature_receipt["signature_receipt_hash"] = hash_package(signature_receipt)

    immutable_storage_receipt = {
        "receipt_status": "IMMUTABLE_STORAGE_RECEIPT_REPOSITORY_EVIDENCE_RECORDED",
        "receipt_scope": "deterministic_metadata_only_no_external_storage_write",
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "run_id": RUN_ID_330,
        "immutable_storage_written": False,
    }
    immutable_storage_receipt["immutable_storage_receipt_hash"] = hash_package(
        immutable_storage_receipt
    )

    public_ledger_entry = {
        "entry_status": "PUBLIC_LEDGER_ENTRY_REPOSITORY_EVIDENCE_RECORDED",
        "entry_scope": "deterministic_metadata_only_no_external_ledger_append",
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt_hash": immutable_storage_receipt[
            "immutable_storage_receipt_hash"
        ],
        "run_id": RUN_ID_330,
        "public_ledger_mutated": False,
        "rollback_revocation_supersession": False,
    }
    public_ledger_entry["public_ledger_entry_hash"] = hash_package(public_ledger_entry)

    official_beo_metadata = {
        "metadata_status": "OFFICIAL_BEO_METADATA_RECORDED_FOR_CURRENT_VERIFIED_LOOP",
        "beo_id": BEO_ID_330,
        "beb_id": BEB_ID_330,
        "execution_kernel_hash": kernel["execution_kernel_hash"],
        "run_id_consumed": RUN_ID_330,
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt_hash": immutable_storage_receipt[
            "immutable_storage_receipt_hash"
        ],
        "public_ledger_entry_hash": public_ledger_entry["public_ledger_entry_hash"],
        "protected_body_access": False,
        "target_source_git_mutation": False,
    }
    official_beo_metadata["official_beo_metadata_hash"] = hash_package(official_beo_metadata)

    beo_finality_record = {
        "record_status": "BEO_FINALITY_RECORD_RECORDED_FOR_CURRENT_VERIFIED_LOOP",
        "execution_request_hash": execution_request_hash,
        "official_beo_metadata_hash": official_beo_metadata["official_beo_metadata_hash"],
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt_hash": immutable_storage_receipt[
            "immutable_storage_receipt_hash"
        ],
        "public_ledger_entry_hash": public_ledger_entry["public_ledger_entry_hash"],
        "run_id_consumed": RUN_ID_330,
        "rtm_generation": False,
        "production_blk_link": False,
        "protected_body_access": False,
    }
    beo_finality_record["beo_finality_record_hash"] = hash_package(beo_finality_record)

    package = {
        "status": "BLK_SYSTEM_330_VERIFIED_LOOP_BEO_PUBLICATION_SIDE_EFFECT_PACKAGE_EXECUTED",
        "markers": list(_MARKERS_330),
        "upstream_execution_kernel_hash": kernel["execution_kernel_hash"],
        "operator_directive_hash": _hash_text(operator_directive),
        "run_id_consumed": RUN_ID_330,
        "run_id_replay_evidence": run_id_replay_evidence,
        "requested_at": requested_at,
        "executed_at": executed_at,
        "expires_at": expires_at,
        "execution_scope": _EXECUTION_SCOPE_330,
        "execution_request_hash": execution_request_hash,
        "signature_receipt": signature_receipt,
        "signature_receipt_hash": signature_receipt["signature_receipt_hash"],
        "immutable_storage_receipt": immutable_storage_receipt,
        "immutable_storage_receipt_hash": immutable_storage_receipt[
            "immutable_storage_receipt_hash"
        ],
        "public_ledger_entry": public_ledger_entry,
        "public_ledger_entry_hash": public_ledger_entry["public_ledger_entry_hash"],
        "official_beo_metadata": official_beo_metadata,
        "official_beo_metadata_hash": official_beo_metadata["official_beo_metadata_hash"],
        "beo_finality_record": beo_finality_record,
        "beo_finality_record_hash": beo_finality_record["beo_finality_record_hash"],
        "denied_authorities": list(_DENIED_AUTHORITIES_330),
        "side_effects": dict(_SIDE_EFFECTS_330),
    }
    package["execution_package_hash"] = hash_package(package)
    return validate_verified_loop_beo_publication_side_effect_package_330(package)


def reconcile_verified_loop_beo_publication_finality_331(
    package_330: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile official BEO metadata as the exact RTM trace-closure input."""

    package = validate_verified_loop_beo_publication_side_effect_package_330(package_330)
    reconciliation = {
        "status": "BLK_SYSTEM_331_VERIFIED_LOOP_BEO_PUBLICATION_FINALITY_RECONCILED",
        "markers": list(_MARKERS_331),
        "execution_package_hash": package["execution_package_hash"],
        "official_beo_metadata": package["official_beo_metadata"],
        "official_beo_metadata_hash": package["official_beo_metadata_hash"],
        "beo_finality_record_hash": package["beo_finality_record_hash"],
        "signature_receipt_hash": package["signature_receipt_hash"],
        "immutable_storage_receipt_hash": package["immutable_storage_receipt_hash"],
        "public_ledger_entry_hash": package["public_ledger_entry_hash"],
        "reconciliation_scope": _RECONCILIATION_SCOPE_331,
        "denied_authorities": list(_DENIED_AUTHORITIES_330),
        "side_effects": dict(_SIDE_EFFECTS_331),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_verified_loop_beo_publication_finality_331(reconciliation)


def execute_rtm_blk_link_trace_closure_332(
    reconciliation_331: dict[str, Any],
    *,
    requested_at: str,
    executed_at: str,
    expires_at: str,
    used_run_ids: tuple[str, ...] | list[str] = (),
) -> dict[str, Any]:
    """Close RTM / blk-link traceability from the official BEO metadata."""

    reconciliation = validate_verified_loop_beo_publication_finality_331(reconciliation_331)
    _require_window(requested_at, executed_at, expires_at)
    run_id_replay_evidence = _build_run_id_replay_evidence(
        RTM_TRACE_CLOSURE_RUN_ID_332,
        used_run_ids,
        "BLK-SYSTEM-332",
    )
    run_id_replay_evidence_hash = hash_package(run_id_replay_evidence)
    trace_closure_request_hash = hash_package(
        {
            "upstream_reconciliation_hash": reconciliation["reconciliation_hash"],
            "official_beo_metadata_hash": reconciliation["official_beo_metadata_hash"],
            "beo_finality_record_hash": reconciliation["beo_finality_record_hash"],
            "run_id": RTM_TRACE_CLOSURE_RUN_ID_332,
            "run_id_replay_evidence_hash": run_id_replay_evidence_hash,
            "requested_at": requested_at,
            "executed_at": executed_at,
            "expires_at": expires_at,
            "execution_scope": _TRACE_SCOPE_332,
        }
    )
    trace_closure_record = {
        "trace_closure_status": "RTM_BLK_LINK_TRACE_CLOSURE_RECORDED_FROM_OFFICIAL_BEO_METADATA",
        "trace_closure_id": RTM_TRACE_CLOSURE_ID_332,
        "beo_id": reconciliation["official_beo_metadata"]["beo_id"],
        "beb_id": reconciliation["official_beo_metadata"]["beb_id"],
        "official_beo_metadata_hash": reconciliation["official_beo_metadata_hash"],
        "beo_finality_record_hash": reconciliation["beo_finality_record_hash"],
        "trace_closure_request_hash": trace_closure_request_hash,
        "hash_binding_mode": "HASH_ONLY_NO_PROTECTED_BODY_OR_ACTIVE_VAULT_SCAN",
        "trace_links": [
            {
                "kind": "BEO_METADATA",
                "id": BEO_ID_330,
                "version_hash": reconciliation["official_beo_metadata_hash"],
            },
            {
                "kind": "BEO_FINALITY_RECORD",
                "id": "BLK-SYSTEM-330-BEO-FINALITY-RECORD",
                "version_hash": reconciliation["beo_finality_record_hash"],
            },
        ],
        "runtime_rtm_generation": False,
        "active_vault_comparison": False,
        "protected_body_access": False,
        "drift_rejection": False,
        "coverage_truth": False,
    }
    trace_closure_record["trace_closure_record_hash"] = hash_package(trace_closure_record)
    package = {
        "status": "BLK_SYSTEM_332_RTM_BLK_LINK_TRACE_CLOSURE_RECORDED_FROM_OFFICIAL_BEO_METADATA",
        "markers": list(_MARKERS_332),
        "upstream_reconciliation_hash": reconciliation["reconciliation_hash"],
        "official_beo_metadata": reconciliation["official_beo_metadata"],
        "official_beo_metadata_hash": reconciliation["official_beo_metadata_hash"],
        "beo_finality_record_hash": reconciliation["beo_finality_record_hash"],
        "trace_closure_id": RTM_TRACE_CLOSURE_ID_332,
        "run_id_consumed": RTM_TRACE_CLOSURE_RUN_ID_332,
        "run_id_replay_evidence": run_id_replay_evidence,
        "requested_at": requested_at,
        "executed_at": executed_at,
        "expires_at": expires_at,
        "execution_scope": _TRACE_SCOPE_332,
        "trace_closure_request_hash": trace_closure_request_hash,
        "trace_closure_record": trace_closure_record,
        "trace_closure_record_hash": trace_closure_record["trace_closure_record_hash"],
        "denied_authorities": list(_DENIED_AUTHORITIES_332),
        "side_effects": dict(_SIDE_EFFECTS_332),
    }
    package["trace_closure_package_hash"] = hash_package(package)
    return validate_rtm_blk_link_trace_closure_332(package)


def reconcile_verified_loop_rtm_blk_link_trace_closure_333(
    trace_package_332: dict[str, Any],
) -> dict[str, Any]:
    """Reconcile the closed one-run traceability chain and stop."""

    package = validate_rtm_blk_link_trace_closure_332(trace_package_332)
    reconciliation = {
        "status": "BLK_SYSTEM_333_RTM_BLK_LINK_TRACE_CLOSURE_RECONCILED",
        "markers": list(_MARKERS_333),
        "trace_closure_package_hash": package["trace_closure_package_hash"],
        "trace_closure_record_hash": package["trace_closure_record_hash"],
        "official_beo_metadata_hash": package["official_beo_metadata_hash"],
        "next_frontier": NEXT_FRONTIER_333,
        "denied_authorities": list(_DENIED_AUTHORITIES_332),
        "side_effects": dict(_SIDE_EFFECTS_333),
    }
    reconciliation["reconciliation_hash"] = hash_package(reconciliation)
    return validate_verified_loop_rtm_blk_link_trace_closure_333(reconciliation)


def validate_verified_loop_beo_publication_side_effect_package_330(
    package_330: dict[str, Any],
) -> dict[str, Any]:
    package = _require_dict(package_330, "BLK-SYSTEM-330 package")
    _require_allowed_keys(package, _KEYS_330, "BLK-SYSTEM-330 package")
    _require_value(
        package.get("status"),
        "BLK_SYSTEM_330_VERIFIED_LOOP_BEO_PUBLICATION_SIDE_EFFECT_PACKAGE_EXECUTED",
        "status",
    )
    _require_exact_sequence(package.get("markers"), _MARKERS_330, "markers")
    _require_value(
        package.get("upstream_execution_kernel_hash"),
        EXPECTED_329_EXECUTION_KERNEL_HASH,
        "upstream_execution_kernel_hash",
    )
    _require_value(package.get("operator_directive_hash"), _hash_text(OPERATOR_DIRECTIVE_330), "operator_directive_hash")
    _require_value(package.get("run_id_consumed"), RUN_ID_330, "run_id")
    replay_evidence = _validate_run_id_replay_evidence(
        package.get("run_id_replay_evidence"),
        RUN_ID_330,
        "run_id_replay_evidence",
    )
    _require_window(package.get("requested_at"), package.get("executed_at"), package.get("expires_at"))
    _require_value(package.get("execution_scope"), _EXECUTION_SCOPE_330, "execution_scope")
    expected_request_hash = hash_package(
        {
            "upstream_execution_kernel_hash": package["upstream_execution_kernel_hash"],
            "operator_directive_hash": package["operator_directive_hash"],
            "run_id": package["run_id_consumed"],
            "run_id_replay_evidence_hash": hash_package(replay_evidence),
            "requested_at": package["requested_at"],
            "executed_at": package["executed_at"],
            "expires_at": package["expires_at"],
            "execution_scope": package["execution_scope"],
        }
    )
    _require_value(package.get("execution_request_hash"), expected_request_hash, "execution_request_hash")
    _validate_330_receipt_chain(package)
    _require_exact_sequence(package.get("denied_authorities"), _DENIED_AUTHORITIES_330, "denied_authorities")
    _require_exact_dict(package.get("side_effects"), _SIDE_EFFECTS_330, "side_effects")
    _require_hash(package, "execution_package_hash", "BLK-SYSTEM-330 package")
    _require_value(
        package.get("execution_package_hash"),
        hash_package({key: value for key, value in package.items() if key != "execution_package_hash"}),
        "execution_package_hash",
    )
    if EXPECTED_330_EXECUTION_PACKAGE_HASH is not None:
        _require_value(
            package["execution_package_hash"],
            EXPECTED_330_EXECUTION_PACKAGE_HASH,
            "canonical BLK-SYSTEM-330 hash",
        )
    return deepcopy(package)


def validate_verified_loop_beo_publication_finality_331(
    reconciliation_331: dict[str, Any],
) -> dict[str, Any]:
    package = _require_dict(reconciliation_331, "BLK-SYSTEM-331 reconciliation")
    _require_allowed_keys(package, _KEYS_331, "BLK-SYSTEM-331 reconciliation")
    _require_value(
        package.get("status"),
        "BLK_SYSTEM_331_VERIFIED_LOOP_BEO_PUBLICATION_FINALITY_RECONCILED",
        "status",
    )
    _require_exact_sequence(package.get("markers"), _MARKERS_331, "markers")
    if EXPECTED_330_EXECUTION_PACKAGE_HASH is not None:
        _require_value(
            package.get("execution_package_hash"),
            EXPECTED_330_EXECUTION_PACKAGE_HASH,
            "execution_package_hash",
        )
    _require_hash(package, "execution_package_hash", "BLK-SYSTEM-331 reconciliation")
    _validate_official_beo_metadata(
        package.get("official_beo_metadata"),
        package.get("official_beo_metadata_hash"),
        package.get("signature_receipt_hash"),
        package.get("immutable_storage_receipt_hash"),
        package.get("public_ledger_entry_hash"),
    )
    _require_hash(package, "beo_finality_record_hash", "BLK-SYSTEM-331 reconciliation")
    _require_value(package.get("reconciliation_scope"), _RECONCILIATION_SCOPE_331, "reconciliation_scope")
    _require_exact_sequence(package.get("denied_authorities"), _DENIED_AUTHORITIES_330, "denied_authorities")
    _require_exact_dict(package.get("side_effects"), _SIDE_EFFECTS_331, "side_effects")
    _require_hash(package, "reconciliation_hash", "BLK-SYSTEM-331 reconciliation")
    _require_value(
        package.get("reconciliation_hash"),
        hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}),
        "reconciliation_hash",
    )
    if EXPECTED_331_RECONCILIATION_HASH is not None:
        _require_value(
            package["reconciliation_hash"],
            EXPECTED_331_RECONCILIATION_HASH,
            "canonical BLK-SYSTEM-331 hash",
        )
    return deepcopy(package)


def validate_rtm_blk_link_trace_closure_332(package_332: dict[str, Any]) -> dict[str, Any]:
    package = _require_dict(package_332, "BLK-SYSTEM-332 package")
    _require_allowed_keys(package, _KEYS_332, "BLK-SYSTEM-332 package")
    _require_value(
        package.get("status"),
        "BLK_SYSTEM_332_RTM_BLK_LINK_TRACE_CLOSURE_RECORDED_FROM_OFFICIAL_BEO_METADATA",
        "status",
    )
    _require_exact_sequence(package.get("markers"), _MARKERS_332, "markers")
    if EXPECTED_331_RECONCILIATION_HASH is not None:
        _require_value(
            package.get("upstream_reconciliation_hash"),
            EXPECTED_331_RECONCILIATION_HASH,
            "upstream_reconciliation_hash",
        )
    _require_hash(package, "upstream_reconciliation_hash", "BLK-SYSTEM-332 package")
    _validate_official_beo_metadata(
        package.get("official_beo_metadata"),
        package.get("official_beo_metadata_hash"),
        None,
        None,
        None,
    )
    _require_hash(package, "beo_finality_record_hash", "BLK-SYSTEM-332 package")
    _require_value(package.get("trace_closure_id"), RTM_TRACE_CLOSURE_ID_332, "trace_closure_id")
    _require_value(package.get("run_id_consumed"), RTM_TRACE_CLOSURE_RUN_ID_332, "run_id")
    replay_evidence = _validate_run_id_replay_evidence(
        package.get("run_id_replay_evidence"),
        RTM_TRACE_CLOSURE_RUN_ID_332,
        "run_id_replay_evidence",
    )
    _require_window(package.get("requested_at"), package.get("executed_at"), package.get("expires_at"))
    _require_value(package.get("execution_scope"), _TRACE_SCOPE_332, "execution_scope")
    expected_request_hash = hash_package(
        {
            "upstream_reconciliation_hash": package["upstream_reconciliation_hash"],
            "official_beo_metadata_hash": package["official_beo_metadata_hash"],
            "beo_finality_record_hash": package["beo_finality_record_hash"],
            "run_id": package["run_id_consumed"],
            "run_id_replay_evidence_hash": hash_package(replay_evidence),
            "requested_at": package["requested_at"],
            "executed_at": package["executed_at"],
            "expires_at": package["expires_at"],
            "execution_scope": package["execution_scope"],
        }
    )
    _require_value(package.get("trace_closure_request_hash"), expected_request_hash, "trace_closure_request_hash")
    _validate_trace_closure_record(package)
    _require_exact_sequence(package.get("denied_authorities"), _DENIED_AUTHORITIES_332, "denied_authorities")
    _require_exact_dict(package.get("side_effects"), _SIDE_EFFECTS_332, "side_effects")
    _require_hash(package, "trace_closure_package_hash", "BLK-SYSTEM-332 package")
    _require_value(
        package.get("trace_closure_package_hash"),
        hash_package({key: value for key, value in package.items() if key != "trace_closure_package_hash"}),
        "trace_closure_package_hash",
    )
    if EXPECTED_332_TRACE_CLOSURE_PACKAGE_HASH is not None:
        _require_value(
            package["trace_closure_package_hash"],
            EXPECTED_332_TRACE_CLOSURE_PACKAGE_HASH,
            "canonical BLK-SYSTEM-332 hash",
        )
    return deepcopy(package)


def validate_verified_loop_rtm_blk_link_trace_closure_333(
    reconciliation_333: dict[str, Any],
) -> dict[str, Any]:
    package = _require_dict(reconciliation_333, "BLK-SYSTEM-333 reconciliation")
    _require_allowed_keys(package, _KEYS_333, "BLK-SYSTEM-333 reconciliation")
    _require_value(package.get("status"), "BLK_SYSTEM_333_RTM_BLK_LINK_TRACE_CLOSURE_RECONCILED", "status")
    _require_exact_sequence(package.get("markers"), _MARKERS_333, "markers")
    if EXPECTED_332_TRACE_CLOSURE_PACKAGE_HASH is not None:
        _require_value(
            package.get("trace_closure_package_hash"),
            EXPECTED_332_TRACE_CLOSURE_PACKAGE_HASH,
            "trace_closure_package_hash",
        )
    _require_hash(package, "trace_closure_package_hash", "BLK-SYSTEM-333 reconciliation")
    _require_hash(package, "trace_closure_record_hash", "BLK-SYSTEM-333 reconciliation")
    _require_hash(package, "official_beo_metadata_hash", "BLK-SYSTEM-333 reconciliation")
    _require_value(package.get("next_frontier"), NEXT_FRONTIER_333, "next_frontier")
    _require_exact_sequence(package.get("denied_authorities"), _DENIED_AUTHORITIES_332, "denied_authorities")
    _require_exact_dict(package.get("side_effects"), _SIDE_EFFECTS_333, "side_effects")
    _require_hash(package, "reconciliation_hash", "BLK-SYSTEM-333 reconciliation")
    _require_value(
        package.get("reconciliation_hash"),
        hash_package({key: value for key, value in package.items() if key != "reconciliation_hash"}),
        "reconciliation_hash",
    )
    if EXPECTED_333_RECONCILIATION_HASH is not None:
        _require_value(
            package["reconciliation_hash"],
            EXPECTED_333_RECONCILIATION_HASH,
            "canonical BLK-SYSTEM-333 hash",
        )
    return deepcopy(package)


def _build_run_id_replay_evidence(
    run_id: str,
    used_run_ids: tuple[str, ...] | list[str],
    context: str,
) -> dict[str, Any]:
    _require_run_id_token(run_id, f"{context} run_id")
    if not isinstance(used_run_ids, (tuple, list)):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} used_run_ids must be a tuple/list"
        )
    prior: list[str] = []
    seen: set[str] = set()
    for value in used_run_ids:
        _require_run_id_token(value, f"{context} used_run_ids")
        if value in seen:
            raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
                f"{context} duplicate prior run ID"
            )
        seen.add(value)
        prior.append(value)
    if run_id in seen:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} run_id replay: already consumed"
        )
    return {
        "replay_check_status": "NO_PRIOR_CONSUMPTION_FOR_EXACT_RUN_ID",
        "current_run_id": run_id,
        "prior_consumed_run_ids": prior,
        "replayed": False,
    }


def _validate_run_id_replay_evidence(
    value: Any,
    run_id: str,
    field: str,
) -> dict[str, Any]:
    evidence = _require_dict(value, field)
    _require_allowed_keys(
        evidence,
        frozenset(
            {
                "replay_check_status",
                "current_run_id",
                "prior_consumed_run_ids",
                "replayed",
            }
        ),
        field,
    )
    _require_value(
        evidence.get("replay_check_status"),
        "NO_PRIOR_CONSUMPTION_FOR_EXACT_RUN_ID",
        f"{field}.replay_check_status",
    )
    _require_value(evidence.get("current_run_id"), run_id, f"{field}.current_run_id")
    _require_value(evidence.get("replayed"), False, f"{field}.replayed")
    prior = evidence.get("prior_consumed_run_ids")
    if not isinstance(prior, list):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field}.prior_consumed_run_ids must be a list"
        )
    seen: set[str] = set()
    for item in prior:
        _require_run_id_token(item, f"{field}.prior_consumed_run_ids")
        if item in seen:
            raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
                f"{field}.prior_consumed_run_ids duplicate run ID"
            )
        seen.add(item)
    if run_id in seen:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} run_id replay: already consumed"
        )
    return deepcopy(evidence)


def _require_run_id_token(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must be a non-empty string"
        )
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    if any(ch not in allowed for ch in value):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} contains unsupported run ID characters"
        )


def _validate_330_receipt_chain(package: dict[str, Any]) -> None:
    signature = _require_dict(package.get("signature_receipt"), "signature_receipt")
    storage = _require_dict(package.get("immutable_storage_receipt"), "immutable_storage_receipt")
    ledger = _require_dict(package.get("public_ledger_entry"), "public_ledger_entry")
    metadata = _require_dict(package.get("official_beo_metadata"), "official_beo_metadata")
    finality = _require_dict(package.get("beo_finality_record"), "beo_finality_record")
    _require_value(
        signature.get("signature_receipt_hash"),
        hash_package({key: value for key, value in signature.items() if key != "signature_receipt_hash"}),
        "signature_receipt_hash",
    )
    _require_value(
        storage.get("immutable_storage_receipt_hash"),
        hash_package({key: value for key, value in storage.items() if key != "immutable_storage_receipt_hash"}),
        "immutable_storage_receipt_hash",
    )
    _require_value(
        ledger.get("public_ledger_entry_hash"),
        hash_package({key: value for key, value in ledger.items() if key != "public_ledger_entry_hash"}),
        "public_ledger_entry_hash",
    )
    _require_value(
        metadata.get("official_beo_metadata_hash"),
        hash_package({key: value for key, value in metadata.items() if key != "official_beo_metadata_hash"}),
        "official_beo_metadata_hash",
    )
    _require_value(
        finality.get("beo_finality_record_hash"),
        hash_package({key: value for key, value in finality.items() if key != "beo_finality_record_hash"}),
        "beo_finality_record_hash",
    )
    _require_value(signature.get("execution_request_hash"), package["execution_request_hash"], "signature execution_request_hash")
    _require_value(storage.get("signature_receipt_hash"), signature["signature_receipt_hash"], "storage signature_receipt_hash")
    _require_value(ledger.get("signature_receipt_hash"), signature["signature_receipt_hash"], "ledger signature_receipt_hash")
    _require_value(
        ledger.get("immutable_storage_receipt_hash"),
        storage["immutable_storage_receipt_hash"],
        "ledger immutable_storage_receipt_hash",
    )
    _validate_official_beo_metadata(
        metadata,
        package.get("official_beo_metadata_hash"),
        package.get("signature_receipt_hash"),
        package.get("immutable_storage_receipt_hash"),
        package.get("public_ledger_entry_hash"),
    )
    _require_value(finality.get("official_beo_metadata_hash"), metadata["official_beo_metadata_hash"], "finality official_beo_metadata_hash")
    _require_value(finality.get("signature_receipt_hash"), signature["signature_receipt_hash"], "finality signature_receipt_hash")
    _require_value(
        finality.get("immutable_storage_receipt_hash"),
        storage["immutable_storage_receipt_hash"],
        "finality immutable_storage_receipt_hash",
    )
    _require_value(finality.get("public_ledger_entry_hash"), ledger["public_ledger_entry_hash"], "finality public_ledger_entry_hash")
    _require_value(package.get("signature_receipt_hash"), signature["signature_receipt_hash"], "package signature_receipt_hash")
    _require_value(
        package.get("immutable_storage_receipt_hash"),
        storage["immutable_storage_receipt_hash"],
        "package immutable_storage_receipt_hash",
    )
    _require_value(package.get("public_ledger_entry_hash"), ledger["public_ledger_entry_hash"], "package public_ledger_entry_hash")
    _require_value(package.get("beo_finality_record_hash"), finality["beo_finality_record_hash"], "package beo_finality_record_hash")


def _validate_official_beo_metadata(
    metadata_value: Any,
    expected_metadata_hash: str | None,
    expected_signature_hash: str | None,
    expected_storage_hash: str | None,
    expected_ledger_hash: str | None,
) -> dict[str, Any]:
    metadata = _require_dict(metadata_value, "official_beo_metadata")
    _require_value(metadata.get("beo_id"), BEO_ID_330, "metadata beo_id")
    _require_value(metadata.get("beb_id"), BEB_ID_330, "metadata beb_id")
    _require_value(metadata.get("execution_kernel_hash"), EXPECTED_329_EXECUTION_KERNEL_HASH, "metadata execution_kernel_hash")
    _require_value(metadata.get("run_id_consumed"), RUN_ID_330, "metadata run_id")
    if expected_signature_hash is not None:
        _require_value(metadata.get("signature_receipt_hash"), expected_signature_hash, "metadata signature_receipt_hash")
    if expected_storage_hash is not None:
        _require_value(metadata.get("immutable_storage_receipt_hash"), expected_storage_hash, "metadata immutable_storage_receipt_hash")
    if expected_ledger_hash is not None:
        _require_value(metadata.get("public_ledger_entry_hash"), expected_ledger_hash, "metadata public_ledger_entry_hash")
    _require_value(metadata.get("protected_body_access"), False, "metadata protected_body_access")
    _require_value(metadata.get("target_source_git_mutation"), False, "metadata target_source_git_mutation")
    _require_hash(metadata, "official_beo_metadata_hash", "official_beo_metadata")
    _require_value(
        metadata.get("official_beo_metadata_hash"),
        hash_package({key: value for key, value in metadata.items() if key != "official_beo_metadata_hash"}),
        "official_beo_metadata_hash",
    )
    if expected_metadata_hash is not None:
        _require_value(metadata["official_beo_metadata_hash"], expected_metadata_hash, "official_beo_metadata_hash")
    return metadata


def _validate_trace_closure_record(package: dict[str, Any]) -> None:
    record = _require_dict(package.get("trace_closure_record"), "trace_closure_record")
    _require_value(record.get("trace_closure_id"), RTM_TRACE_CLOSURE_ID_332, "record trace_closure_id")
    _require_value(record.get("beo_id"), BEO_ID_330, "record beo_id")
    _require_value(record.get("beb_id"), BEB_ID_330, "record beb_id")
    _require_value(record.get("official_beo_metadata_hash"), package["official_beo_metadata_hash"], "record official_beo_metadata_hash")
    _require_value(record.get("beo_finality_record_hash"), package["beo_finality_record_hash"], "record beo_finality_record_hash")
    _require_value(record.get("trace_closure_request_hash"), package["trace_closure_request_hash"], "record trace_closure_request_hash")
    for field in (
        "runtime_rtm_generation",
        "active_vault_comparison",
        "protected_body_access",
        "drift_rejection",
        "coverage_truth",
    ):
        _require_value(record.get(field), False, f"record {field}")
    links = record.get("trace_links")
    if not isinstance(links, list) or len(links) != 2:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            "trace_links must contain exact BEO metadata and finality links"
        )
    expected_links = [
        {
            "kind": "BEO_METADATA",
            "id": BEO_ID_330,
            "version_hash": package["official_beo_metadata_hash"],
        },
        {
            "kind": "BEO_FINALITY_RECORD",
            "id": "BLK-SYSTEM-330-BEO-FINALITY-RECORD",
            "version_hash": package["beo_finality_record_hash"],
        },
    ]
    if links != expected_links:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            "trace_links mismatch"
        )
    _require_hash(record, "trace_closure_record_hash", "trace_closure_record")
    _require_value(
        record.get("trace_closure_record_hash"),
        hash_package({key: value for key, value in record.items() if key != "trace_closure_record_hash"}),
        "trace_closure_record_hash",
    )
    _require_value(package.get("trace_closure_record_hash"), record["trace_closure_record_hash"], "package trace_closure_record_hash")


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} must be a dictionary"
        )
    return value


def _require_allowed_keys(value: dict[str, Any], allowed: frozenset[str], context: str) -> None:
    extras = sorted(set(value) - set(allowed))
    missing = sorted(set(allowed) - set(value))
    if extras or missing:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} key mismatch extras={extras} missing={missing}"
        )


def _require_exact_sequence(value: Any, expected: tuple[str, ...], field: str) -> None:
    if not isinstance(value, list):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must be a list"
        )
    if tuple(value) != expected:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} mismatch"
        )
    if len(value) != len(set(value)):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must not contain duplicates"
        )


def _require_exact_dict(value: Any, expected: dict[str, bool], field: str) -> None:
    nested = _require_dict(value, field)
    _require_allowed_keys(nested, frozenset(expected), field)
    if nested != expected:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} mismatch"
        )


def _require_value(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} mismatch"
        )


def _require_hash(package: dict[str, Any], field: str, context: str) -> None:
    value = package.get(field)
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} {field} must be sha256:<64 hex>"
        )
    if not all(ch in "0123456789abcdef" for ch in value.removeprefix("sha256:")):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{context} {field} must be lowercase sha256"
        )


def _require_window(requested_at: Any, executed_at: Any, expires_at: Any) -> None:
    requested = _parse_timestamp(requested_at, "requested_at")
    executed = _parse_timestamp(executed_at, "executed_at")
    expires = _parse_timestamp(expires_at, "expires_at")
    if not (requested <= executed < expires):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            "requested_at/executed_at/expires_at window mismatch"
        )


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must be an ISO timestamp string"
        )
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must be an ISO timestamp string"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError(
            f"{field} must be timezone-aware"
        )
    return parsed


def _reject_freeform(value: Any, path: str, denied: tuple[str, ...]) -> None:
    findings = scan_for_authority_laundering(value, path, denied)
    if findings:
        raise VerifiedLoopBeoPublicationTraceClosure330333ValidationError("; ".join(findings))
