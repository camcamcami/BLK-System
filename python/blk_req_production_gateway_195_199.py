"""BLK-SYSTEM-195..199 production-ready BLK-req gateway evidence.

This module packages the already-implemented BLK-req legislative gateway
primitives into a production-ready, exact-operation contract and local smoke
fixture. It deliberately grants no broad active-vault body scan, no body access
outside exact-ID operations, no BEB/BEO dispatch, no RTM generation, no
BLK-pipe/BLK-test/Codex runtime, no target/source/Git mutation beyond exact
BLK-req vault writes in the supplied non-Git workspace, and no tooling or
production-isolation claim.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering
from lint_artifacts import (
    promote_staged_revision_to_active,
    promote_staging_draft_to_baseline,
    preview_staging_version_hash,
    retrieve_active_artifact_by_exact_id,
    write_staged_revision_draft,
    write_staging_draft,
)

_ALLOWED_OPERATIONS = [
    "lint_staging_draft",
    "write_new_staging_draft",
    "promote_new_baseline_with_exact_hitl_approval",
    "retrieve_active_artifact_by_exact_id",
    "write_staged_revision_draft_from_exact_id",
    "promote_staged_revision_with_parent_hash_lock",
]

_MARKERS_195_199 = [
    "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
    "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
    "BLK_SYSTEM_197_BLK_REQ_EXACT_ID_LIFECYCLE_SMOKE_PASSED",
    "BLK_SYSTEM_198_BLK_REQ_GATEWAY_HOSTILE_INPUTS_HARDENED",
    "BLK_SYSTEM_199_BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN",
]

_SIDE_EFFECTS = {
    "exact_id_retrieval": True,
    "body_access_without_exact_id": False,
    "active_vault_body_scan": False,
    "active_vault_filename_listing_for_id_allocation": True,
    "staging_write": True,
    "active_vault_write": True,
    "baseline_promotion": True,
    "revision_promotion": True,
    "beb_dispatch": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "blk_pipe_runtime": False,
    "blk_test_runtime": False,
    "live_codex_dispatch": False,
    "target_source_git_mutation": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}

_REQUIRED_PRIOR_MARKERS = [
    "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
    "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
    "BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE",
    "BLK_SYSTEM_122_EXACT_ID_RETRIEVAL_READY",
    "BLK_SYSTEM_123_STAGED_REVISION_DRAFT_READY",
    "BLK_SYSTEM_124_HITL_REVISION_PROMOTION_READY",
    "BLK_SYSTEM_127_METADATA_BOUND_BEO_PUBLICATION_PREREQUISITE_REQUEST_READY",
]

_DEFAULT_INPUTS = {
    "baseline_approval_id": "APPROVAL-BLK-SYSTEM-197-BASELINE-001",
    "revision_approval_id": "APPROVAL-BLK-SYSTEM-197-REVISION-001",
    "discord_user_id": "684235178083745819",
    "baseline_message_id": "1488733359072084070",
    "revision_message_id": "1488733359072084071",
    "baseline_timestamp": "2026-05-17T10:30:00+10:00",
    "revision_timestamp": "2026-05-17T10:45:00+10:00",
    "operator_note": "exact BLK-req lifecycle smoke, no adjacent runtime authority",
}

_SMOKE_ARTIFACT_ID = "REQ-001"
_SMOKE_FINAL_ACTIVE_RELATIVE_PATH = "docs/requirements/active/REQ-001.md"
_SMOKE_BASELINE_VERSION_HASH = "sha256:ad7b5a7625e33c2b718732ac80a775ff4fd92c01c2855afc4aba49b407ef1106"
_SMOKE_REVISION_VERSION_HASH = "sha256:ffcfc3f2fd806abe6f3d89d83760342e4f8c046a71b93898b6e230bf0975eb49"
_CANONICAL_READINESS_REVIEW_HASH = "sha256:55b889fedad49bb3a5ab7023c1613c4a54db139c1d399c0f54295b6219c7c2ea"


def build_blk_req_gateway_readiness_review_195() -> dict[str, Any]:
    """Review prior BLK-req lifecycle rungs and select production contract work."""

    review = {
        "sprint": "BLK-SYSTEM-195",
        "status": "BLK_REQ_GATEWAY_READY_FOR_PRODUCTION_CONTRACT",
        "markers": [
            "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
            "BLK_REQ_116_127_LIFECYCLE_PRIMITIVES_PRESENT",
            "PRODUCTION_CONTRACT_SELECTED_NOT_ADJACENT_AUTHORITY",
        ],
        "prior_markers_required": list(_REQUIRED_PRIOR_MARKERS),
        "selected_next_sprints": [
            "BLK-SYSTEM-196 production gateway contract",
            "BLK-SYSTEM-197 exact-ID lifecycle smoke",
            "BLK-SYSTEM-198 hostile input hardening",
            "BLK-SYSTEM-199 clean reconciliation",
        ],
        "authority_boundary": {
            "production_ready_gateway_contract_requested": True,
            "blanket_protected_body_access": False,
            "active_vault_body_scan": False,
            "active_vault_filename_listing_for_id_allocation": True,
            "beb_dispatch": False,
            "beo_publication": False,
            "rtm_generation": False,
            "target_source_git_mutation": False,
        },
    }
    review["review_package_hash"] = _hash_package(review)
    return _deepcopy(review)


def build_blk_req_production_gateway_contract_196(readiness_review: dict[str, Any]) -> dict[str, Any]:
    """Emit the exact-operation BLK-req production gateway contract."""

    _require_hash_bound_package(readiness_review, "review_package_hash", "BLK_REQ_GATEWAY_READY_FOR_PRODUCTION_CONTRACT")
    contract = {
        "sprint": "BLK-SYSTEM-196",
        "status": "BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
        "readiness_review_hash": readiness_review["review_package_hash"],
        "markers": [
            "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
            "BLK_REQ_PRODUCTION_GATEWAY_PER_EXACT_OPERATION_READY",
            "NO_BROAD_ACTIVE_VAULT_BODY_SCAN",
            "NO_BODY_ACCESS_WITHOUT_EXACT_ID_OPERATION",
            "NO_ADJACENT_BEB_BEO_RTM_RUNTIME_OR_MUTATION_AUTHORITY",
        ],
        "allowed_operations": list(_ALLOWED_OPERATIONS),
        "operator_input_contract": {
            "approval_ids": "exact caller-supplied ASCII-safe identifiers scanned for authority/protected-path text",
            "discord_identity": "ASCII decimal Discord snowflakes only",
            "active_retrieval": "REQ-### or UC-### exact ID only; direct path map for reads; baseline ID allocation may list filenames but never reads active bodies",
            "revision_concurrency": "parent_hash must match current active version_hash under active revision lock",
        },
        "side_effects": dict(_SIDE_EFFECTS),
        "authorized_exact_surface": {
            "staging_body_lint_and_write": True,
            "exact_hitl_new_baseline_promotion": True,
            "exact_id_active_artifact_retrieval": True,
            "exact_hitl_staged_revision_promotion": True,
        },
    }
    contract["contract_package_hash"] = _hash_package(contract)
    return _deepcopy(contract)


def validate_gateway_operator_inputs_196(contract: dict[str, Any], overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate caller-supplied operator fields before any gateway side effect."""

    _require_hash_bound_package(contract, "contract_package_hash", "BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY")
    values = dict(_DEFAULT_INPUTS)
    if overrides:
        unknown = sorted(set(overrides) - set(values))
        if unknown:
            raise ValueError(f"unsupported operator input field(s): {unknown}")
        values.update(overrides)

    scan_values = {key: value for key, value in values.items() if key in {"baseline_approval_id", "revision_approval_id", "operator_note"}}
    scan_errors = scan_for_authority_laundering(scan_values, path="operator_inputs")
    for key, value in scan_values.items():
        text_value = str(value)
        if not _ascii_printable(text_value):
            raise ValueError(f"{key} must contain ASCII-safe operator text only")
        compact = _compact_decoded(text_value)
        if "docsrequirementsactive" in compact or "docsactive" in compact:
            scan_errors.append(f"{key} contains protected active-vault path")
    if scan_errors:
        raise ValueError("; ".join(scan_errors))

    for key in ("discord_user_id", "baseline_message_id", "revision_message_id"):
        if not _ascii_digits(str(values[key]), minimum=17, maximum=20):
            raise ValueError(f"{key} must be an ASCII decimal Discord snowflake")
    return _deepcopy(values)


def execute_blk_req_lifecycle_smoke_197(
    *,
    workspace: str | Path,
    contract: dict[str, Any],
    operator_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the exact new-baseline -> exact retrieval -> revision lifecycle smoke."""

    inputs = validate_gateway_operator_inputs_196(contract, operator_inputs)
    root = Path(workspace).resolve()
    _reject_git_worktree_workspace(root)
    draft = write_staging_draft(
        workspace=root,
        artifact_type="REQ",
        title="Production Gateway Smoke",
        body="The gateway shall preserve exact requirement identity.",
        rationale="Needed for production BLK-req gateway smoke evidence.",
        linked_nodes=[],
    )
    if draft["status"] != "STAGING_DRAFT_WRITTEN":
        raise ValueError(f"baseline draft failed: {draft['diagnostics']}")
    draft_path = root / draft["relative_path"]
    baseline_approval = _approval_payload(
        approval_id=inputs["baseline_approval_id"],
        discord_user_id=inputs["discord_user_id"],
        discord_message_id=inputs["baseline_message_id"],
        timestamp=inputs["baseline_timestamp"],
        path=draft_path,
        workspace=root,
    )
    baseline = promote_staging_draft_to_baseline(
        draft_path,
        approval_payload=baseline_approval,
        workspace=root,
        used_approval_ids=[],
    )
    if baseline["status"] != "BASELINE_PROMOTED":
        raise ValueError(f"baseline promotion failed: {baseline['diagnostics']}")

    artifact_id = baseline["assigned_id"]
    initial = retrieve_active_artifact_by_exact_id(artifact_id, workspace=root)
    if initial["status"] != "ACTIVE_ARTIFACT_RETRIEVED":
        raise ValueError(f"initial exact-ID retrieval failed: {initial['diagnostics']}")

    revision = write_staged_revision_draft(
        workspace=root,
        artifact_id=artifact_id,
        body="The gateway shall preserve revised exact requirement identity.",
        rationale="Needed for production BLK-req revision evidence.",
        linked_nodes=[],
    )
    if revision["status"] != "REVISION_DRAFT_WRITTEN":
        raise ValueError(f"revision draft failed: {revision['diagnostics']}")
    revision_path = root / revision["relative_path"]
    revision_approval = _approval_payload(
        approval_id=inputs["revision_approval_id"],
        discord_user_id=inputs["discord_user_id"],
        discord_message_id=inputs["revision_message_id"],
        timestamp=inputs["revision_timestamp"],
        path=revision_path,
        workspace=root,
    )
    promoted_revision = promote_staged_revision_to_active(
        revision_path,
        approval_payload=revision_approval,
        workspace=root,
    )
    if promoted_revision["status"] != "REVISION_PROMOTED":
        raise ValueError(f"revision promotion failed: {promoted_revision['diagnostics']}")

    final = retrieve_active_artifact_by_exact_id(artifact_id, workspace=root)
    if final["status"] != "ACTIVE_ARTIFACT_RETRIEVED":
        raise ValueError(f"final exact-ID retrieval failed: {final['diagnostics']}")

    evidence = {
        "sprint": "BLK-SYSTEM-197",
        "status": "BLK_REQ_PRODUCTION_LIFECYCLE_SMOKE_PASSED",
        "contract_package_hash": contract["contract_package_hash"],
        "artifact_id": artifact_id,
        "baseline_promotion_status": baseline["status"],
        "initial_retrieval_status": initial["status"],
        "revision_draft_status": revision["status"],
        "revision_promotion_status": promoted_revision["status"],
        "final_retrieval_status": final["status"],
        "baseline_version_hash": baseline["version_hash"],
        "revision_parent_hash": revision["parent_hash"],
        "revision_version_hash": promoted_revision["version_hash"],
        "final_active_relative_path": final["active_relative_path"],
        "exact_id_retrieval_performed": True,
        "exact_id_only_read": True,
        "staging_write": True,
        "active_vault_write": True,
        "baseline_promotion": True,
        "revision_promotion": True,
        "active_vault_filename_listing_for_id_allocation": True,
        "active_vault_body_scan": False,
        "body_access_without_exact_id": False,
        "beb_dispatch": False,
        "beo_publication": False,
        "rtm_generation": False,
        "drift_rejection": False,
        "coverage_truth": False,
        "blk_pipe_runtime": False,
        "blk_test_runtime": False,
        "live_codex_dispatch": False,
        "target_source_git_mutation": False,
        "package_network_model_browser_cyber_tooling": False,
        "production_isolation_claim": False,
    }
    evidence["lifecycle_evidence_hash"] = _hash_package(evidence)
    return _deepcopy(evidence)


def reconcile_blk_req_gateway_production_readiness_199(contract: dict[str, Any], lifecycle_smoke: dict[str, Any]) -> dict[str, Any]:
    """Close the BLK-req gateway ladder as production-ready under exact operations."""

    _require_hash_bound_package(contract, "contract_package_hash", "BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY")
    _require_hash_bound_package(lifecycle_smoke, "lifecycle_evidence_hash", "BLK_REQ_PRODUCTION_LIFECYCLE_SMOKE_PASSED")
    if lifecycle_smoke.get("contract_package_hash") != contract.get("contract_package_hash"):
        raise ValueError("lifecycle smoke must bind the exact production gateway contract")
    reconciliation = {
        "sprint": "BLK-SYSTEM-199",
        "status": "BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN",
        "markers": list(_MARKERS_195_199),
        "contract_package_hash": contract["contract_package_hash"],
        "lifecycle_evidence_hash": lifecycle_smoke["lifecycle_evidence_hash"],
        "production_ready_surface": "exact-operation BLK-req lifecycle gateway",
        "next_frontier": "NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT",
        "authority_boundary": {
            "exact_operation_blk_req_gateway_ready": True,
            "active_vault_body_scan": False,
            "active_vault_filename_listing_for_id_allocation": True,
            "body_access_without_exact_id": False,
            "beb_dispatch": False,
            "beo_publication": False,
            "rtm_generation": False,
            "target_source_git_mutation": False,
            "production_isolation_claim": False,
        },
    }
    reconciliation["reconciliation_package_hash"] = _hash_package(reconciliation)
    return _deepcopy(reconciliation)


def _approval_payload(*, approval_id: str, discord_user_id: str, discord_message_id: str, timestamp: str, path: Path, workspace: Path) -> dict[str, Any]:
    preview = preview_staging_version_hash(path, workspace=workspace)
    if not preview["ok"]:
        raise ValueError(f"staging preview failed: {preview['diagnostics']}")
    return {
        "idp": "discord",
        "approved": True,
        "approval_id": approval_id,
        "discord_user_id": discord_user_id,
        "discord_message_id": discord_message_id,
        "interaction_timestamp": timestamp,
        "staging_relative_path": path.relative_to(workspace).as_posix(),
        "staging_version_hash": preview["version_hash"],
    }


def _require_hash_bound_package(package: dict[str, Any], hash_key: str, expected_status: str) -> None:
    if not isinstance(package, dict):
        raise ValueError("package must be a dictionary")
    if package.get("status") != expected_status:
        raise ValueError(f"package status must be {expected_status}")
    supplied = package.get(hash_key)
    if not isinstance(supplied, str) or not supplied.startswith("sha256:") or len(supplied) != 71:
        raise ValueError(f"{hash_key} must be sha256:<64 hex>")
    clone = copy.deepcopy(package)
    clone.pop(hash_key, None)
    if _hash_package(clone) != supplied:
        raise ValueError(f"{hash_key} does not match submitted package")
    if hash_key == "review_package_hash":
        _validate_readiness_review_schema(package)
    elif hash_key == "contract_package_hash":
        _validate_contract_schema(package)
    elif hash_key == "lifecycle_evidence_hash":
        _validate_lifecycle_evidence_schema(package)


def _validate_readiness_review_schema(package: dict[str, Any]) -> None:
    expected_keys = {"sprint", "status", "markers", "prior_markers_required", "selected_next_sprints", "authority_boundary", "review_package_hash"}
    if set(package) != expected_keys:
        raise ValueError("readiness review schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-195":
        raise ValueError("readiness review schema sprint mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
        "BLK_REQ_116_127_LIFECYCLE_PRIMITIVES_PRESENT",
        "PRODUCTION_CONTRACT_SELECTED_NOT_ADJACENT_AUTHORITY",
    ]:
        raise ValueError("readiness review schema markers mismatch")
    if package.get("prior_markers_required") != _REQUIRED_PRIOR_MARKERS:
        raise ValueError("readiness review schema prior markers mismatch")
    if package.get("selected_next_sprints") != [
        "BLK-SYSTEM-196 production gateway contract",
        "BLK-SYSTEM-197 exact-ID lifecycle smoke",
        "BLK-SYSTEM-198 hostile input hardening",
        "BLK-SYSTEM-199 clean reconciliation",
    ]:
        raise ValueError("readiness review schema selected_next_sprints mismatch")
    authority = package.get("authority_boundary")
    expected_authority = {
        "production_ready_gateway_contract_requested": True,
        "blanket_protected_body_access": False,
        "active_vault_body_scan": False,
        "active_vault_filename_listing_for_id_allocation": True,
        "beb_dispatch": False,
        "beo_publication": False,
        "rtm_generation": False,
        "target_source_git_mutation": False,
    }
    if authority != expected_authority:
        raise ValueError("readiness review schema authority_boundary mismatch")


def _validate_contract_schema(package: dict[str, Any]) -> None:
    expected_keys = {"sprint", "status", "readiness_review_hash", "markers", "allowed_operations", "operator_input_contract", "side_effects", "authorized_exact_surface", "contract_package_hash"}
    if set(package) != expected_keys:
        raise ValueError("contract schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-196":
        raise ValueError("contract schema sprint mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
        "BLK_REQ_PRODUCTION_GATEWAY_PER_EXACT_OPERATION_READY",
        "NO_BROAD_ACTIVE_VAULT_BODY_SCAN",
        "NO_BODY_ACCESS_WITHOUT_EXACT_ID_OPERATION",
        "NO_ADJACENT_BEB_BEO_RTM_RUNTIME_OR_MUTATION_AUTHORITY",
    ]:
        raise ValueError("contract schema markers mismatch")
    if package.get("allowed_operations") != _ALLOWED_OPERATIONS:
        raise ValueError("contract schema allowed_operations mismatch")
    if package.get("readiness_review_hash") != _CANONICAL_READINESS_REVIEW_HASH:
        raise ValueError("contract schema readiness_review_hash mismatch")
    if package.get("side_effects") != _SIDE_EFFECTS:
        raise ValueError("contract schema side_effects mismatch")
    if package.get("operator_input_contract") != {
        "approval_ids": "exact caller-supplied ASCII-safe identifiers scanned for authority/protected-path text",
        "discord_identity": "ASCII decimal Discord snowflakes only",
        "active_retrieval": "REQ-### or UC-### exact ID only; direct path map for reads; baseline ID allocation may list filenames but never reads active bodies",
        "revision_concurrency": "parent_hash must match current active version_hash under active revision lock",
    }:
        raise ValueError("contract schema operator_input_contract mismatch")
    if package.get("authorized_exact_surface") != {
        "staging_body_lint_and_write": True,
        "exact_hitl_new_baseline_promotion": True,
        "exact_id_active_artifact_retrieval": True,
        "exact_hitl_staged_revision_promotion": True,
    }:
        raise ValueError("contract schema authorized_exact_surface mismatch")


def _validate_lifecycle_evidence_schema(package: dict[str, Any]) -> None:
    false_flags = [
        "active_vault_body_scan",
        "body_access_without_exact_id",
        "beb_dispatch",
        "beo_publication",
        "rtm_generation",
        "drift_rejection",
        "coverage_truth",
        "blk_pipe_runtime",
        "blk_test_runtime",
        "live_codex_dispatch",
        "target_source_git_mutation",
        "package_network_model_browser_cyber_tooling",
        "production_isolation_claim",
    ]
    true_flags = [
        "exact_id_retrieval_performed",
        "exact_id_only_read",
        "staging_write",
        "active_vault_write",
        "baseline_promotion",
        "revision_promotion",
        "active_vault_filename_listing_for_id_allocation",
    ]
    required_keys = {
        "sprint", "status", "contract_package_hash", "artifact_id", "baseline_promotion_status",
        "initial_retrieval_status", "revision_draft_status", "revision_promotion_status", "final_retrieval_status",
        "baseline_version_hash", "revision_parent_hash", "revision_version_hash", "final_active_relative_path",
        "lifecycle_evidence_hash", *false_flags, *true_flags,
    }
    if set(package) != required_keys:
        raise ValueError("lifecycle evidence schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-197":
        raise ValueError("lifecycle evidence schema sprint mismatch")
    exact_scalars = {
        "status": "BLK_REQ_PRODUCTION_LIFECYCLE_SMOKE_PASSED",
        "baseline_promotion_status": "BASELINE_PROMOTED",
        "initial_retrieval_status": "ACTIVE_ARTIFACT_RETRIEVED",
        "revision_draft_status": "REVISION_DRAFT_WRITTEN",
        "revision_promotion_status": "REVISION_PROMOTED",
        "final_retrieval_status": "ACTIVE_ARTIFACT_RETRIEVED",
    }
    for key, expected in exact_scalars.items():
        if package.get(key) != expected:
            raise ValueError(f"lifecycle evidence {key} mismatch")
    if package.get("artifact_id") != _SMOKE_ARTIFACT_ID:
        raise ValueError("lifecycle evidence artifact_id must match deterministic smoke fixture")
    if package.get("final_active_relative_path") != _SMOKE_FINAL_ACTIVE_RELATIVE_PATH:
        raise ValueError("lifecycle evidence final_active_relative_path must match deterministic smoke fixture")
    if package.get("baseline_version_hash") != _SMOKE_BASELINE_VERSION_HASH:
        raise ValueError("lifecycle evidence baseline fixture hash mismatch")
    if package.get("revision_parent_hash") != package.get("baseline_version_hash"):
        raise ValueError("lifecycle evidence hash chain parent must equal baseline hash")
    if package.get("revision_version_hash") != _SMOKE_REVISION_VERSION_HASH:
        raise ValueError("lifecycle evidence revision fixture hash mismatch")
    for key in ("baseline_version_hash", "revision_parent_hash", "revision_version_hash", "contract_package_hash"):
        value = package.get(key)
        if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
            raise ValueError(f"lifecycle evidence {key} must be sha256:<64 hex>")
    for key in true_flags:
        if package.get(key) is not True:
            raise ValueError(f"lifecycle evidence {key} must be true")
    for key in false_flags:
        if package.get(key) is not False:
            raise ValueError(f"lifecycle evidence {key} must remain false")


def _reject_git_worktree_workspace(root: Path) -> None:
    cursor = root
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            raise ValueError("BLK-req lifecycle smoke refuses git worktree workspace mutation")
        if candidate.parent == candidate:
            break


def _hash_package(package: dict[str, Any]) -> str:
    body = json.dumps(package, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _deepcopy(value: Any) -> Any:
    return copy.deepcopy(value)


def _ascii_digits(value: str, *, minimum: int, maximum: int) -> bool:
    return minimum <= len(value) <= maximum and all("0" <= ch <= "9" for ch in value)


def _ascii_printable(value: str) -> bool:
    return all(32 <= ord(ch) <= 126 for ch in value)


def _compact_decoded(value: str) -> str:
    current = value
    variants = [current]
    for _ in range(5):
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
        variants.append(decoded)
        current = decoded
    return "".join(ch.casefold() for variant in variants for ch in variant if ch.isalnum())


def _percent_decode_once(value: str) -> str:
    out = []
    index = 0
    while index < len(value):
        if value[index] == "%" and index + 2 < len(value) and all(ch in "0123456789abcdefABCDEF" for ch in value[index + 1 : index + 3]):
            out.append(chr(int(value[index + 1 : index + 3], 16)))
            index += 3
        else:
            out.append(value[index])
            index += 1
    return "".join(out)


__all__ = [
    "build_blk_req_gateway_readiness_review_195",
    "build_blk_req_production_gateway_contract_196",
    "execute_blk_req_lifecycle_smoke_197",
    "reconcile_blk_req_gateway_production_readiness_199",
    "validate_gateway_operator_inputs_196",
]
