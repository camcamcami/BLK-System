"""BLK-SYSTEM-200 Kuronode BLK-req vault bootstrap evidence.

This module converts the BLK-SYSTEM-199 BLK-req production gateway into a
Kuronode-facing sibling-vault bootstrap package. It deliberately avoids Kuronode
source/Git mutation, broad Kuronode document scans, protected body migration,
BEB/BEO dispatch, RTM generation, BLK-pipe/BLK-test/Codex runtime, and blanket
production `blk-link` authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

_KURONODE_SOURCE_ROOT = "/home/dad/code/Kuronode-v1"
_VAULT_ROOT = "/home/dad/BLK-req-Kuronode"
_MARKER_200 = "BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY"
_NEXT_FRONTIER_200 = "NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED"
_UPSTREAM_NEXT_FRONTIER = "NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT"
_DIRECTORY_LAYOUT = [
    "docs/requirements/staging",
    "docs/requirements/active",
    "docs/use_cases/staging",
    "docs/use_cases/active",
    "mappings",
    "exports",
]
_BOOTSTRAP_FILES = [
    "docs/.blk_req_baseline_approval_ledger.json",
    "mappings/kuronode-id-map.json",
    "exports/kuronode-requirements.json",
]
_UPSTREAM_MARKERS = [
    "BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN",
    "BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY",
    "BLK_SYSTEM_197_BLK_REQ_EXACT_ID_LIFECYCLE_SMOKE_PASSED",
    "BLK_SYSTEM_198_BLK_REQ_GATEWAY_HOSTILE_INPUTS_HARDENED",
    "BLK_SYSTEM_199_BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN",
]
_CANONICAL_UPSTREAM_CONTRACT_HASH = "sha256:fc8747b50e279836dd9bf1d45b707d7f9401b507e2ae4bb0b6568f8fd80edae6"
_CANONICAL_UPSTREAM_LIFECYCLE_HASH = "sha256:ab06d219a137cd524854564395eb72db49c9a1bd3c144db703ce63c5f051c837"
_CANONICAL_UPSTREAM_RECONCILIATION_HASH = "sha256:38597e0dc8374dfdb21019a52432d600e3ee2fa8fcc11b416639756dd957d3e0"
_UPSTREAM_AUTHORITY = {
    "exact_operation_blk_req_gateway_ready": True,
    "active_vault_body_scan": False,
    "active_vault_filename_listing_for_id_allocation": True,
    "body_access_without_exact_id": False,
    "beb_dispatch": False,
    "beo_publication": False,
    "rtm_generation": False,
    "target_source_git_mutation": False,
    "production_isolation_claim": False,
}
_BOOTSTRAP_AUTHORITY = {
    "non_git_sibling_vault_bootstrap": True,
    "kuronode_source_git_mutation": False,
    "protected_body_migration": False,
    "broad_kuronode_doc_scan": False,
    "body_text_export": False,
    "exact_id_mapping_blueprint": True,
    "exact_gateway_operations_only": True,
    "beb_dispatch": False,
    "beo_closeout_execution": False,
    "beo_publication": False,
    "rtm_generation": False,
    "drift_rejection": False,
    "coverage_truth": False,
    "production_blk_link": False,
    "blk_pipe_runtime": False,
    "blk_test_runtime": False,
    "live_codex_dispatch": False,
    "package_network_model_browser_cyber_tooling": False,
    "production_isolation_claim": False,
}
_ID_MAPPING_CONTRACT = {
    "kuronode_requirement_ids": "R-* source IDs map to exact REQ-### BLK-req IDs",
    "kuronode_use_case_ids": "UC-* source IDs map to exact UC-### BLK-req IDs",
    "mapping_source": "caller-supplied exact ID table only; no broad Kuronode doc scan",
    "body_handling": "metadata and IDs only during bootstrap; no body text migration or protected-body parsing",
    "promotion": "future baseline/revision promotion still requires exact Discord HITL approval per artifact",
}


def build_kuronode_blk_req_vault_bootstrap_200(upstream_reconciliation: dict[str, Any]) -> dict[str, Any]:
    """Emit the Kuronode BLK-req sibling-vault bootstrap blueprint."""

    _require_upstream_reconciliation_199(upstream_reconciliation)
    package = {
        "sprint": "BLK-SYSTEM-200",
        "status": "KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY",
        "upstream_reconciliation_hash": upstream_reconciliation["reconciliation_package_hash"],
        "markers": [
            _MARKER_200,
            "KURONODE_BLK_REQ_SIBLING_VAULT_SELECTED",
            "NO_KURONODE_SOURCE_GIT_MUTATION",
            "NO_PROTECTED_BODY_MIGRATION_OR_BROAD_DOC_SCAN",
        ],
        "kuronode_source_root": _KURONODE_SOURCE_ROOT,
        "vault_root": _VAULT_ROOT,
        "directory_layout": list(_DIRECTORY_LAYOUT),
        "bootstrap_files": list(_BOOTSTRAP_FILES),
        "id_mapping_contract": dict(_ID_MAPPING_CONTRACT),
        "authority_boundary": dict(_BOOTSTRAP_AUTHORITY),
        "next_frontier": _NEXT_FRONTIER_200,
    }
    package["bootstrap_package_hash"] = _hash_package(package)
    return _deepcopy(package)


def materialize_kuronode_blk_req_vault_skeleton_200(package: dict[str, Any], vault_root: str | Path) -> dict[str, Any]:
    """Create only the declared BLK-req vault skeleton in a non-Git workspace."""

    _require_bootstrap_package_200(package)
    root = Path(vault_root).resolve()
    if root.name != "BLK-req-Kuronode":
        raise ValueError("vault root must be named BLK-req-Kuronode")
    _reject_git_worktree_workspace(root)
    _reject_kuronode_source_descendant(root)

    created_dirs: list[str] = []
    created_files: list[str] = []
    for rel in _DIRECTORY_LAYOUT:
        path = root / rel
        _reject_unsafe_relative_path(rel)
        _reject_symlink_components(root, rel)
        path.mkdir(parents=True, exist_ok=True)
        _reject_symlink_components(root, rel)
        _require_resolved_descendant(root, path)
        created_dirs.append(rel)

    file_payloads = {
        "docs/.blk_req_baseline_approval_ledger.json": {"used_approval_ids": []},
        "mappings/kuronode-id-map.json": {
            "version": 1,
            "mappings": [],
            "body_text_included": False,
            "mapping_contract": package["id_mapping_contract"],
        },
        "exports/kuronode-requirements.json": {
            "version": 1,
            "requirements": [],
            "use_cases": [],
            "body_text_included": False,
            "protected_body_migration": False,
        },
    }
    for rel in _BOOTSTRAP_FILES:
        _reject_unsafe_relative_path(rel)
        _reject_symlink_components(root, str(Path(rel).parent))
        path = root / rel
        if path.exists() and path.is_dir():
            raise ValueError(f"bootstrap file path is a directory: {rel}")
        path.parent.mkdir(parents=True, exist_ok=True)
        _reject_symlink_components(root, str(Path(rel).parent))
        _reject_symlink_components(root, rel)
        _require_resolved_descendant(root, path)
        if path.exists():
            current = path.read_text(encoding="utf-8")
            expected = json.dumps(file_payloads[rel], ensure_ascii=False, sort_keys=True, indent=2) + "\n"
            if current != expected:
                raise ValueError(f"bootstrap file already exists with different content: {rel}")
        else:
            path.write_text(json.dumps(file_payloads[rel], ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        created_files.append(rel)

    result = {
        "sprint": "BLK-SYSTEM-200",
        "status": "KURONODE_BLK_REQ_VAULT_SKELETON_MATERIALIZED",
        "bootstrap_package_hash": package["bootstrap_package_hash"],
        "vault_root_name": root.name,
        "created_directories": created_dirs,
        "created_files": created_files,
        "kuronode_source_git_mutation": False,
        "protected_body_migration": False,
        "broad_kuronode_doc_scan": False,
        "body_text_export": False,
        "rtm_generation": False,
        "beo_publication": False,
        "production_blk_link": False,
    }
    result["materialization_hash"] = _hash_package(result)
    return _deepcopy(result)


def _require_upstream_reconciliation_199(package: dict[str, Any]) -> None:
    if not isinstance(package, dict):
        raise ValueError("upstream reconciliation package must be a dictionary")
    expected_keys = {
        "sprint",
        "status",
        "markers",
        "contract_package_hash",
        "lifecycle_evidence_hash",
        "production_ready_surface",
        "next_frontier",
        "authority_boundary",
        "reconciliation_package_hash",
    }
    if set(package) != expected_keys:
        raise ValueError("upstream reconciliation schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-199":
        raise ValueError("upstream reconciliation sprint mismatch")
    if package.get("status") != "BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN":
        raise ValueError("upstream reconciliation status mismatch")
    if package.get("markers") != _UPSTREAM_MARKERS:
        raise ValueError("upstream reconciliation markers mismatch")
    if package.get("next_frontier") != _UPSTREAM_NEXT_FRONTIER:
        raise ValueError("upstream reconciliation next frontier mismatch")
    if package.get("authority_boundary") != _UPSTREAM_AUTHORITY:
        raise ValueError("upstream reconciliation authority boundary mismatch")
    if package.get("contract_package_hash") != _CANONICAL_UPSTREAM_CONTRACT_HASH:
        raise ValueError("upstream reconciliation contract_package_hash mismatch")
    if package.get("lifecycle_evidence_hash") != _CANONICAL_UPSTREAM_LIFECYCLE_HASH:
        raise ValueError("upstream reconciliation lifecycle_evidence_hash mismatch")
    supplied = package.get("reconciliation_package_hash")
    if supplied != _CANONICAL_UPSTREAM_RECONCILIATION_HASH:
        raise ValueError("upstream reconciliation canonical hash mismatch")
    if not _is_sha256(supplied):
        raise ValueError("upstream reconciliation hash must be sha256:<64 hex>")
    clone = copy.deepcopy(package)
    clone.pop("reconciliation_package_hash", None)
    if _hash_package(clone) != supplied:
        raise ValueError("upstream reconciliation hash mismatch")


def _require_bootstrap_package_200(package: dict[str, Any]) -> None:
    if not isinstance(package, dict):
        raise ValueError("bootstrap package must be a dictionary")
    expected_keys = {
        "sprint",
        "status",
        "upstream_reconciliation_hash",
        "markers",
        "kuronode_source_root",
        "vault_root",
        "directory_layout",
        "bootstrap_files",
        "id_mapping_contract",
        "authority_boundary",
        "next_frontier",
        "bootstrap_package_hash",
    }
    if set(package) != expected_keys:
        raise ValueError("bootstrap package schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-200":
        raise ValueError("bootstrap package sprint mismatch")
    if package.get("status") != "KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY":
        raise ValueError("bootstrap package status mismatch")
    if package.get("markers") != [
        _MARKER_200,
        "KURONODE_BLK_REQ_SIBLING_VAULT_SELECTED",
        "NO_KURONODE_SOURCE_GIT_MUTATION",
        "NO_PROTECTED_BODY_MIGRATION_OR_BROAD_DOC_SCAN",
    ]:
        raise ValueError("bootstrap package markers mismatch")
    if package.get("kuronode_source_root") != _KURONODE_SOURCE_ROOT:
        raise ValueError("bootstrap package Kuronode source root mismatch")
    if package.get("vault_root") != _VAULT_ROOT:
        raise ValueError("bootstrap package vault_root mismatch")
    if package.get("directory_layout") != _DIRECTORY_LAYOUT:
        raise ValueError("bootstrap package directory_layout mismatch")
    if package.get("bootstrap_files") != _BOOTSTRAP_FILES:
        raise ValueError("bootstrap package bootstrap_files mismatch")
    if package.get("id_mapping_contract") != _ID_MAPPING_CONTRACT:
        raise ValueError("bootstrap package id_mapping_contract mismatch")
    if package.get("authority_boundary") != _BOOTSTRAP_AUTHORITY:
        raise ValueError("bootstrap package authority_boundary source_git_mutation mismatch")
    if package.get("next_frontier") != _NEXT_FRONTIER_200:
        raise ValueError("bootstrap package next_frontier mismatch")
    if not _is_sha256(package.get("upstream_reconciliation_hash")):
        raise ValueError("bootstrap package upstream_reconciliation_hash must be sha256:<64 hex>")
    supplied = package.get("bootstrap_package_hash")
    if not _is_sha256(supplied):
        raise ValueError("bootstrap package hash must be sha256:<64 hex>")
    clone = copy.deepcopy(package)
    clone.pop("bootstrap_package_hash", None)
    if _hash_package(clone) != supplied:
        raise ValueError("bootstrap package hash mismatch")


def _reject_git_worktree_workspace(root: Path) -> None:
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            raise ValueError("Kuronode BLK-req vault bootstrap refuses git worktree workspace mutation")
        if candidate.parent == candidate:
            break


def _reject_kuronode_source_descendant(root: Path) -> None:
    source = Path(_KURONODE_SOURCE_ROOT).resolve()
    try:
        root.relative_to(source)
    except ValueError:
        return
    raise ValueError("bootstrap vault must not be inside Kuronode source/Git workspace")


def _reject_unsafe_relative_path(rel: str) -> None:
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe bootstrap relative path: {rel}")


def _reject_symlink_components(root: Path, rel: str) -> None:
    if rel in ("", "."):
        candidates = [root]
    else:
        path = Path(rel)
        candidates = [root]
        cursor = root
        for part in path.parts:
            cursor = cursor / part
            candidates.append(cursor)
    for candidate in candidates:
        if candidate.is_symlink():
            raise ValueError(f"bootstrap path must not contain symlink component: {candidate}")


def _require_resolved_descendant(root: Path, path: Path) -> None:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("bootstrap path resolved outside declared vault root") from exc


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        return False
    return all(ch in "0123456789abcdef" for ch in value.removeprefix("sha256:"))


def _hash_package(package: dict[str, Any]) -> str:
    body = json.dumps(package, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _deepcopy(value: Any) -> Any:
    return copy.deepcopy(value)


__all__ = [
    "build_kuronode_blk_req_vault_bootstrap_200",
    "materialize_kuronode_blk_req_vault_skeleton_200",
]
