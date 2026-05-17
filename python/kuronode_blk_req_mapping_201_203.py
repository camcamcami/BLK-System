"""BLK-SYSTEM-201..203 Kuronode BLK-req exact-ID mapping bridge.

This module consumes the BLK-SYSTEM-200 Kuronode BLK-req sibling-vault
bootstrap and closes the metadata-only ID mapping bridge. It deliberately avoids
Kuronode source/Git mutation, broad Kuronode document scans, protected body
migration/body export, BLK-pipe/BLK-test/Codex runtime, BEO publication, RTM
generation, production `blk-link`, and production-isolation claims.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from blk_authority_smuggling import scan_for_authority_laundering

_CANONICAL_BOOTSTRAP_HASH = "sha256:8e0414e4564d7ae6567487e807374497fee337f20ec53eb47a6e7ca9a3958229"
_CANONICAL_BOOTSTRAP_UPSTREAM_HASH = "sha256:38597e0dc8374dfdb21019a52432d600e3ee2fa8fcc11b416639756dd957d3e0"
_CANONICAL_MAPPING_MANIFEST_HASH = "sha256:97cbec0a33c9cbd01aaf0c7a0256694997c3cfdff731f09897215037ed924a51"
_VAULT_ROOT_NAME = "BLK-req-Kuronode"
_KURONODE_SOURCE_ROOT = "/home/dad/code/Kuronode-v1"
_MARKERS_201_203 = [
    "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
    "BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
    "BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN",
]
_NEXT_FRONTIER_203 = "NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED"
_DEFAULT_MAPPINGS = [
    {
        "kind": "requirement",
        "kuronode_id": "R-VIS-001",
        "blk_req_id": "REQ-001",
        "label": "Kuronode visualization requirement metadata",
    },
    {
        "kind": "requirement",
        "kuronode_id": "R-ARC-001",
        "blk_req_id": "REQ-002",
        "label": "Kuronode architecture requirement metadata",
    },
    {
        "kind": "use_case",
        "kuronode_id": "UC-001",
        "blk_req_id": "UC-001",
        "label": "Kuronode primary use-case metadata",
    },
]
_MAPPING_AUTHORITY = {
    "exact_id_mapping_manifest": True,
    "metadata_only_mapping": True,
    "sibling_vault_file_write": True,
    "protected_body_migration": False,
    "body_text_included": False,
    "broad_kuronode_doc_scan": False,
    "kuronode_source_git_mutation": False,
    "baseline_promotion": False,
    "revision_promotion": False,
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
_BOOTSTRAP_EXPECTED_AUTHORITY = {
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
_BOOTSTRAP_EXPECTED_MARKERS = [
    "BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY",
    "KURONODE_BLK_REQ_SIBLING_VAULT_SELECTED",
    "NO_KURONODE_SOURCE_GIT_MUTATION",
    "NO_PROTECTED_BODY_MIGRATION_OR_BROAD_DOC_SCAN",
]
_BOOTSTRAP_EXPECTED_LAYOUT = [
    "docs/requirements/staging",
    "docs/requirements/active",
    "docs/use_cases/staging",
    "docs/use_cases/active",
    "mappings",
    "exports",
]
_BOOTSTRAP_EXPECTED_FILES = [
    "docs/.blk_req_baseline_approval_ledger.json",
    "mappings/kuronode-id-map.json",
    "exports/kuronode-requirements.json",
]
_BOOTSTRAP_EXPECTED_MAPPING_CONTRACT = {
    "kuronode_requirement_ids": "R-* source IDs map to exact REQ-### BLK-req IDs",
    "kuronode_use_case_ids": "UC-* source IDs map to exact UC-### BLK-req IDs",
    "mapping_source": "caller-supplied exact ID table only; no broad Kuronode doc scan",
    "body_handling": "metadata and IDs only during bootstrap; no body text migration or protected-body parsing",
    "promotion": "future baseline/revision promotion still requires exact Discord HITL approval per artifact",
}


def build_kuronode_blk_req_mapping_manifest_201(
    bootstrap_package: dict[str, Any],
    mappings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a metadata-only Kuronode ID -> BLK-req exact-ID manifest."""

    _require_bootstrap_package_200(bootstrap_package)
    validated_mappings = _validate_mapping_entries(_DEFAULT_MAPPINGS if mappings is None else mappings)
    if validated_mappings != _DEFAULT_MAPPINGS:
        raise ValueError("mapping manifest canonical mappings mismatch")
    package = {
        "sprint": "BLK-SYSTEM-201",
        "status": "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
        "bootstrap_package_hash": bootstrap_package["bootstrap_package_hash"],
        "markers": [
            "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
            "KURONODE_IDS_MAP_TO_EXACT_BLK_REQ_IDS_METADATA_ONLY",
            "NO_PROTECTED_BODY_TEXT_OR_KURONODE_SOURCE_MUTATION",
        ],
        "mappings": validated_mappings,
        "authority_boundary": dict(_MAPPING_AUTHORITY),
        "next_frontier": "NEXT_FRONTIER_KURONODE_BLK_REQ_MAPPING_MATERIALIZATION_NOT_RUNTIME_AUTHORITY",
    }
    package["mapping_manifest_hash"] = _hash_package(package)
    return _deepcopy(package)


def materialize_kuronode_blk_req_mapping_202(manifest: dict[str, Any], vault_root: str | Path) -> dict[str, Any]:
    """Write the metadata-only mapping/export files into the sibling vault."""

    _require_mapping_manifest_201(manifest)
    root = Path(vault_root).resolve()
    if root.name != _VAULT_ROOT_NAME:
        raise ValueError("vault root must be named BLK-req-Kuronode")
    _reject_git_worktree_workspace(root)
    _reject_kuronode_source_descendant(root)
    for rel in _BOOTSTRAP_EXPECTED_LAYOUT:
        _reject_unsafe_relative_path(rel)
        _reject_symlink_components(root, rel)
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        _reject_symlink_components(root, rel)
        _require_resolved_descendant(root, path)

    mapping_path = root / "mappings/kuronode-id-map.json"
    export_path = root / "exports/kuronode-requirements.json"
    for rel in ["mappings", "exports", "mappings/kuronode-id-map.json", "exports/kuronode-requirements.json"]:
        _reject_symlink_components(root, rel)
    for path in (mapping_path, export_path):
        _require_resolved_descendant(root, path)
        if path.exists() and path.is_dir():
            raise ValueError(f"mapping output path is a directory: {path}")

    requirements = [entry for entry in manifest["mappings"] if entry["kind"] == "requirement"]
    use_cases = [entry for entry in manifest["mappings"] if entry["kind"] == "use_case"]
    mapping_payload = _mapping_file_payload(manifest)
    export_payload = _export_file_payload(manifest)
    _write_json_if_absent_or_same(mapping_path, mapping_payload)
    _write_json_if_absent_or_same(export_path, export_payload)

    result = {
        "sprint": "BLK-SYSTEM-202",
        "status": "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
        "markers": [
            "BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
            "KURONODE_BLK_REQ_MAPPING_AND_EXPORT_METADATA_ONLY",
            "NO_KURONODE_SOURCE_GIT_MUTATION_OR_PROTECTED_BODY_MIGRATION",
        ],
        "mapping_manifest_hash": manifest["mapping_manifest_hash"],
        "mapping_relative_path": "mappings/kuronode-id-map.json",
        "export_relative_path": "exports/kuronode-requirements.json",
        "mapping_file_hash": _hash_package(mapping_payload),
        "export_file_hash": _hash_package(export_payload),
        "mapping_count": len(manifest["mappings"]),
        "requirement_count": len(requirements),
        "use_case_count": len(use_cases),
        "protected_body_migration": False,
        "body_text_included": False,
        "broad_kuronode_doc_scan": False,
        "kuronode_source_git_mutation": False,
        "baseline_promotion": False,
        "revision_promotion": False,
        "rtm_generation": False,
        "beo_publication": False,
        "production_blk_link": False,
        "runtime_tooling": False,
    }
    result["materialization_hash"] = _hash_package(result)
    return _deepcopy(result)


def reconcile_kuronode_blk_req_bridge_203(manifest: dict[str, Any], materialization: dict[str, Any]) -> dict[str, Any]:
    """Reconcile the Kuronode BLK-req bridge as closed under metadata-only exact IDs."""

    _require_mapping_manifest_201(manifest)
    _require_materialization_202(materialization, manifest)
    package = {
        "sprint": "BLK-SYSTEM-203",
        "status": "KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN",
        "markers": list(_MARKERS_201_203),
        "mapping_manifest_hash": manifest["mapping_manifest_hash"],
        "materialization_hash": materialization["materialization_hash"],
        "mapping_file_hash": materialization["mapping_file_hash"],
        "export_file_hash": materialization["export_file_hash"],
        "closed_surface": "Kuronode BLK-req metadata-only exact-ID bridge",
        "authority_boundary": dict(_MAPPING_AUTHORITY),
        "next_frontier": _NEXT_FRONTIER_203,
    }
    package["reconciliation_hash"] = _hash_package(package)
    return _deepcopy(package)


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
    exact_scalars = {
        "sprint": "BLK-SYSTEM-200",
        "status": "KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY",
        "upstream_reconciliation_hash": _CANONICAL_BOOTSTRAP_UPSTREAM_HASH,
        "kuronode_source_root": _KURONODE_SOURCE_ROOT,
        "vault_root": "/home/dad/BLK-req-Kuronode",
        "next_frontier": "NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED",
        "bootstrap_package_hash": _CANONICAL_BOOTSTRAP_HASH,
    }
    for key, expected in exact_scalars.items():
        if package.get(key) != expected:
            raise ValueError(f"bootstrap package {key} mismatch")
    if package.get("markers") != _BOOTSTRAP_EXPECTED_MARKERS:
        raise ValueError("bootstrap package markers mismatch")
    if package.get("directory_layout") != _BOOTSTRAP_EXPECTED_LAYOUT:
        raise ValueError("bootstrap package directory_layout mismatch")
    if package.get("bootstrap_files") != _BOOTSTRAP_EXPECTED_FILES:
        raise ValueError("bootstrap package bootstrap_files mismatch")
    if package.get("id_mapping_contract") != _BOOTSTRAP_EXPECTED_MAPPING_CONTRACT:
        raise ValueError("bootstrap package id_mapping_contract mismatch")
    if package.get("authority_boundary") != _BOOTSTRAP_EXPECTED_AUTHORITY:
        raise ValueError("bootstrap package authority_boundary mismatch")
    clone = copy.deepcopy(package)
    clone.pop("bootstrap_package_hash", None)
    if _hash_package(clone) != package["bootstrap_package_hash"]:
        raise ValueError("bootstrap package canonical hash mismatch")


def _require_mapping_manifest_201(package: dict[str, Any]) -> None:
    if not isinstance(package, dict):
        raise ValueError("mapping manifest package must be a dictionary")
    expected_keys = {
        "sprint",
        "status",
        "bootstrap_package_hash",
        "markers",
        "mappings",
        "authority_boundary",
        "next_frontier",
        "mapping_manifest_hash",
    }
    if set(package) != expected_keys:
        raise ValueError("mapping manifest schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-201":
        raise ValueError("mapping manifest sprint mismatch")
    if package.get("status") != "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY":
        raise ValueError("mapping manifest status mismatch")
    if package.get("bootstrap_package_hash") != _CANONICAL_BOOTSTRAP_HASH:
        raise ValueError("mapping manifest bootstrap_package_hash mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY",
        "KURONODE_IDS_MAP_TO_EXACT_BLK_REQ_IDS_METADATA_ONLY",
        "NO_PROTECTED_BODY_TEXT_OR_KURONODE_SOURCE_MUTATION",
    ]:
        raise ValueError("mapping manifest markers mismatch")
    if package.get("authority_boundary") != _MAPPING_AUTHORITY:
        raise ValueError("mapping manifest authority_boundary mismatch")
    if package.get("next_frontier") != "NEXT_FRONTIER_KURONODE_BLK_REQ_MAPPING_MATERIALIZATION_NOT_RUNTIME_AUTHORITY":
        raise ValueError("mapping manifest next_frontier mismatch")
    _validate_mapping_entries(package.get("mappings"))
    if package.get("mappings") != _DEFAULT_MAPPINGS:
        raise ValueError("mapping manifest canonical mappings mismatch")
    supplied = package.get("mapping_manifest_hash")
    if not _is_sha256(supplied):
        raise ValueError("mapping manifest hash must be sha256:<64 hex>")
    if supplied != _CANONICAL_MAPPING_MANIFEST_HASH:
        raise ValueError("mapping manifest canonical hash mismatch")
    clone = copy.deepcopy(package)
    clone.pop("mapping_manifest_hash", None)
    if _hash_package(clone) != supplied:
        raise ValueError("mapping manifest hash mismatch")


def _require_materialization_202(package: dict[str, Any], manifest: dict[str, Any]) -> None:
    if not isinstance(package, dict):
        raise ValueError("mapping materialization package must be a dictionary")
    expected_keys = {
        "sprint",
        "status",
        "markers",
        "mapping_manifest_hash",
        "mapping_relative_path",
        "export_relative_path",
        "mapping_file_hash",
        "export_file_hash",
        "mapping_count",
        "requirement_count",
        "use_case_count",
        "protected_body_migration",
        "body_text_included",
        "broad_kuronode_doc_scan",
        "kuronode_source_git_mutation",
        "baseline_promotion",
        "revision_promotion",
        "rtm_generation",
        "beo_publication",
        "production_blk_link",
        "runtime_tooling",
        "materialization_hash",
    }
    if set(package) != expected_keys:
        raise ValueError("mapping materialization schema has unsupported or missing fields")
    if package.get("sprint") != "BLK-SYSTEM-202":
        raise ValueError("mapping materialization sprint mismatch")
    if package.get("status") != "KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED":
        raise ValueError("mapping materialization status mismatch")
    if package.get("markers") != [
        "BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED",
        "KURONODE_BLK_REQ_MAPPING_AND_EXPORT_METADATA_ONLY",
        "NO_KURONODE_SOURCE_GIT_MUTATION_OR_PROTECTED_BODY_MIGRATION",
    ]:
        raise ValueError("mapping materialization markers mismatch")
    if package.get("mapping_manifest_hash") != manifest.get("mapping_manifest_hash"):
        raise ValueError("mapping materialization must bind exact manifest hash")
    if package.get("mapping_relative_path") != "mappings/kuronode-id-map.json":
        raise ValueError("mapping materialization mapping path mismatch")
    if package.get("export_relative_path") != "exports/kuronode-requirements.json":
        raise ValueError("mapping materialization export path mismatch")
    expected_mapping_hash = _hash_package(_mapping_file_payload(manifest))
    expected_export_hash = _hash_package(_export_file_payload(manifest))
    if package.get("mapping_file_hash") != expected_mapping_hash:
        raise ValueError("mapping materialization mapping_file_hash mismatch")
    if package.get("export_file_hash") != expected_export_hash:
        raise ValueError("mapping materialization export_file_hash mismatch")
    requirements = [entry for entry in manifest["mappings"] if entry["kind"] == "requirement"]
    use_cases = [entry for entry in manifest["mappings"] if entry["kind"] == "use_case"]
    if package.get("mapping_count") != len(manifest["mappings"]):
        raise ValueError("mapping materialization mapping_count mismatch")
    if package.get("requirement_count") != len(requirements):
        raise ValueError("mapping materialization requirement_count mismatch")
    if package.get("use_case_count") != len(use_cases):
        raise ValueError("mapping materialization use_case_count mismatch")
    for flag in [
        "protected_body_migration",
        "body_text_included",
        "broad_kuronode_doc_scan",
        "kuronode_source_git_mutation",
        "baseline_promotion",
        "revision_promotion",
        "rtm_generation",
        "beo_publication",
        "production_blk_link",
        "runtime_tooling",
    ]:
        if package.get(flag) is not False:
            raise ValueError(f"mapping materialization {flag} must remain false")
    supplied = package.get("materialization_hash")
    if not _is_sha256(supplied):
        raise ValueError("mapping materialization hash must be sha256:<64 hex>")
    clone = copy.deepcopy(package)
    clone.pop("materialization_hash", None)
    if _hash_package(clone) != supplied:
        raise ValueError("mapping materialization hash mismatch")


def _validate_mapping_entries(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("mapping entries must be a non-empty list")
    seen_kuronode: set[str] = set()
    seen_blk_req: set[str] = set()
    out: list[dict[str, str]] = []
    for index, raw in enumerate(value):
        if not isinstance(raw, dict):
            raise ValueError(f"mapping entry {index} must be a dictionary")
        if set(raw) != {"kind", "kuronode_id", "blk_req_id", "label"}:
            raise ValueError(f"mapping entry {index} has unsupported or missing fields")
        entry = {key: raw[key] for key in ("kind", "kuronode_id", "blk_req_id", "label")}
        if any(not isinstance(item, str) for item in entry.values()):
            raise ValueError(f"mapping entry {index} values must be strings")
        if not all(_ascii_printable(item) for item in entry.values()):
            raise ValueError(f"mapping entry {index} must contain ASCII-safe metadata only")
        if entry["kind"] not in {"requirement", "use_case"}:
            raise ValueError(f"mapping entry {index} kind mismatch")
        if entry["kind"] == "requirement":
            if not _valid_kuronode_requirement_id(entry["kuronode_id"]):
                raise ValueError("kuronode requirement IDs must be ASCII R-XXX-### identifiers")
            if not _valid_exact_id(entry["blk_req_id"], "REQ"):
                raise ValueError("requirement mappings must target ASCII REQ-### identifiers")
        else:
            if not _valid_exact_id(entry["kuronode_id"], "UC"):
                raise ValueError("kuronode use-case IDs must be ASCII UC-### identifiers")
            if not _valid_exact_id(entry["blk_req_id"], "UC"):
                raise ValueError("use-case mappings must target ASCII UC-### identifiers")
        _scan_mapping_text(entry, index)
        if entry["kuronode_id"] in seen_kuronode:
            raise ValueError(f"duplicate kuronode_id: {entry['kuronode_id']}")
        if entry["blk_req_id"] in seen_blk_req:
            raise ValueError(f"duplicate blk_req_id: {entry['blk_req_id']}")
        seen_kuronode.add(entry["kuronode_id"])
        seen_blk_req.add(entry["blk_req_id"])
        out.append(dict(entry))
    return out


def _scan_mapping_text(entry: dict[str, str], index: int) -> None:
    errors = scan_for_authority_laundering(entry, path=f"mapping_entries[{index}]")
    for key, value in entry.items():
        compact = _compact_decoded(value)
        if "docsrequirementsactive" in compact or "docsactive" in compact:
            errors.append(f"mapping entry {index} {key} contains protected active-vault path")
        if "thesystemshall" in compact or "bodytext" in compact or "protectedbody" in compact:
            errors.append(f"mapping entry {index} {key} contains protected body text")
    if errors:
        raise ValueError("; ".join(errors))


def _valid_kuronode_requirement_id(value: str) -> bool:
    parts = value.split("-")
    if len(parts) != 3 or parts[0] != "R":
        return False
    if not parts[1] or not all("A" <= ch <= "Z" or "0" <= ch <= "9" for ch in parts[1]):
        return False
    return len(parts[2]) == 3 and all("0" <= ch <= "9" for ch in parts[2])


def _valid_exact_id(value: str, prefix: str) -> bool:
    expected = prefix + "-"
    return value.startswith(expected) and len(value) == len(expected) + 3 and all("0" <= ch <= "9" for ch in value[len(expected) :])


def _mapping_file_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": 1,
        "sprint": "BLK-SYSTEM-202",
        "mapping_manifest_hash": manifest["mapping_manifest_hash"],
        "mappings": _deepcopy(manifest["mappings"]),
        "body_text_included": False,
        "protected_body_migration": False,
        "broad_kuronode_doc_scan": False,
        "kuronode_source_git_mutation": False,
    }


def _export_file_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": 1,
        "sprint": "BLK-SYSTEM-202",
        "mapping_manifest_hash": manifest["mapping_manifest_hash"],
        "requirements": _deepcopy([entry for entry in manifest["mappings"] if entry["kind"] == "requirement"]),
        "use_cases": _deepcopy([entry for entry in manifest["mappings"] if entry["kind"] == "use_case"]),
        "body_text_included": False,
        "protected_body_migration": False,
        "broad_kuronode_doc_scan": False,
        "kuronode_source_git_mutation": False,
    }


def _write_json_if_absent_or_same(path: Path, payload: dict[str, Any]) -> None:
    expected = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if current == expected:
            return
        try:
            current_payload = _loads_json_no_duplicate_keys(current)
        except json.JSONDecodeError as exc:
            raise ValueError(f"mapping output file already exists with invalid JSON: {path}") from exc
        if not _safe_bootstrap_scaffold_or_prior_mapping(current_payload, payload):
            raise ValueError(f"unsafe existing mapping output: {path}")
    tmp_path = path.with_name(path.name + ".tmp")
    if tmp_path.exists() or tmp_path.is_symlink():
        raise ValueError(f"mapping output temp path already exists: {tmp_path}")
    tmp_path.write_text(expected, encoding="utf-8")
    tmp_path.replace(path)


def _loads_json_no_duplicate_keys(text: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key in existing mapping output: {key}")
            result[key] = value
        return result

    return json.loads(text, object_pairs_hook=reject_duplicates)


def _safe_bootstrap_scaffold_or_prior_mapping(current: Any, payload: dict[str, Any]) -> bool:
    if not isinstance(current, dict):
        return False
    if current == payload:
        return True
    if "mappings" in payload:
        return current == {
            "version": 1,
            "mappings": [],
            "body_text_included": False,
            "mapping_contract": _BOOTSTRAP_EXPECTED_MAPPING_CONTRACT,
        }
    if "requirements" in payload and "use_cases" in payload:
        return current == {
            "version": 1,
            "requirements": [],
            "use_cases": [],
            "body_text_included": False,
            "protected_body_migration": False,
        }
    return False


def _reject_git_worktree_workspace(root: Path) -> None:
    for candidate in (root, *root.parents):
        if (candidate / ".git").exists():
            raise ValueError("Kuronode BLK-req mapping refuses git worktree workspace mutation")
        if candidate.parent == candidate:
            break


def _reject_kuronode_source_descendant(root: Path) -> None:
    source = Path(_KURONODE_SOURCE_ROOT).resolve()
    try:
        root.relative_to(source)
    except ValueError:
        return
    raise ValueError("mapping vault must not be inside Kuronode source/Git workspace")


def _reject_unsafe_relative_path(rel: str) -> None:
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe mapping relative path: {rel}")


def _reject_symlink_components(root: Path, rel: str) -> None:
    candidates = [root]
    cursor = root
    if rel not in ("", "."):
        for part in Path(rel).parts:
            cursor = cursor / part
            candidates.append(cursor)
    for candidate in candidates:
        if candidate.is_symlink():
            raise ValueError(f"mapping path must not contain symlink component: {candidate}")


def _require_resolved_descendant(root: Path, path: Path) -> None:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("mapping path resolved outside declared vault root") from exc


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
        return False
    return all(ch in "0123456789abcdef" for ch in value.removeprefix("sha256:"))


def _ascii_printable(value: str) -> bool:
    return all(32 <= ord(ch) <= 126 for ch in value)


def _compact_decoded(value: str) -> str:
    variants = []
    current = value
    for _ in range(6):
        variants.append(current)
        decoded = _percent_decode_once(current)
        if decoded == current:
            break
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


def _hash_package(package: dict[str, Any]) -> str:
    body = json.dumps(package, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _deepcopy(value: Any) -> Any:
    return copy.deepcopy(value)


__all__ = [
    "build_kuronode_blk_req_mapping_manifest_201",
    "materialize_kuronode_blk_req_mapping_202",
    "reconcile_kuronode_blk_req_bridge_203",
]
