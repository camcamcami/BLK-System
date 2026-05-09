"""BLK-SYSTEM-048 disposable real-repo L4 runtime fixture.

This module executes only the BLK-051 bounded runtime slice: in-process
``run_ast_validation`` over an exact-target disposable real Git repository created
by the sprint harness. It returns evidence only and does not mutate source/Git or
publish BEO/RTM artifacts.
"""

from __future__ import annotations

import ast
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary import (
    APPROVAL_CHECKPOINT as PREFLIGHT_APPROVAL_CHECKPOINT,
    PRIMARY_REPO_ROOT,
    evaluate_blk_test_l4_real_repo_preflight,
)

SPRINT = "BLK-SYSTEM-048"
APPROVAL_CHECKPOINT = "EXPLICIT_BLK_SYSTEM_048_L4_DISPOSABLE_REPO_RUNTIME_APPROVAL_RECORDED"
REQUESTED_TOOL = "run_ast_validation"
APPROVED_RUNTIME_SLICE = "L4_DISPOSABLE_REAL_REPO_RUN_AST_VALIDATION_ONLY_THIS_SPRINT"
L4_PASS = "BLK_TEST_L4_DISPOSABLE_REPO_PASS_EVIDENCE_ONLY"
L4_FAIL = "BLK_TEST_L4_DISPOSABLE_REPO_FAIL_EVIDENCE_ONLY"
L4_BLOCKED = "BLK_TEST_L4_DISPOSABLE_REPO_BLOCKED_EVIDENCE_ONLY"
RUNTIME_EXTENSION_KEYS = frozenset(
    {
        "approved_runtime_slice",
        "target_class",
        "runtime_notes",
        "fixed_tool_executed_after_preflight_only",
        "beo_publication",
        "rtm_status",
        "source_write_allowed",
        "git_mutation_allowed",
    }
)
AUTHORITY_TEXT_MARKERS = (
    "beo publication",
    "rtm generation",
    "drift rejection",
    "coverage truth",
    "source mutation",
    "git mutation",
    "production mcp",
    "generic mcp",
    "arbitrary shell",
    "network",
    "model service",
    "browser",
    "cyber",
    "package manager",
    "production isolation",
)


def build_sprint048_runtime_approval_record(base_approval_record: dict[str, Any]) -> dict[str, Any]:
    approval = deepcopy(base_approval_record)
    approval["sprint048_runtime"] = {
        "approved_runtime_slice": APPROVED_RUNTIME_SLICE,
        "target_class": "disposable-real-git-repository-created-by-blk-system-048-harness",
        "runtime_notes": "read-only AST validation evidence only",
        "fixed_tool_executed_after_preflight_only": True,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "source_write_allowed": False,
        "git_mutation_allowed": False,
    }
    return approval


def run_blk_test_l4_disposable_repo_runtime(
    *,
    authorization_request: dict[str, Any],
    approval_record: dict[str, Any],
    requested_tool: str,
    run_id: str,
    now: str,
    human_approval_checkpoint: str,
    used_approval_ids: set[str] | None,
    used_run_ids: set[str] | None,
    target_repo_path: str | Path,
    source_subtree_path: str | Path,
    workspace_path: str | Path,
    implementation_commit_hash: str,
    driver_hash: str,
) -> dict[str, Any]:
    if human_approval_checkpoint != APPROVAL_CHECKPOINT:
        raise ValueError("BLK-SYSTEM-048 disposable L4 runtime approval checkpoint is required")
    if used_approval_ids is None:
        raise ValueError("used_approval_ids caller-supplied replay set is required")
    if used_run_ids is None:
        raise ValueError("used_run_ids caller-supplied replay set is required")
    if requested_tool != REQUESTED_TOOL:
        raise ValueError("requested_tool must be run_ast_validation")
    repo = Path(target_repo_path).resolve()
    if repo == PRIMARY_REPO_ROOT or PRIMARY_REPO_ROOT in (repo, *repo.parents) or repo in PRIMARY_REPO_ROOT.parents:
        raise ValueError("target repo cannot overlap the primary BLK-System repo")
    _validate_runtime_extension(approval_record)
    preflight_approval = deepcopy(approval_record)
    preflight_approval.pop("sprint048_runtime", None)
    source_root = Path(source_subtree_path).resolve()
    _reject_runtime_source_scope(source_root)
    before = _snapshot_tree(source_root)
    preflight = evaluate_blk_test_l4_real_repo_preflight(
        authorization_request=deepcopy(authorization_request),
        approval_record=preflight_approval,
        requested_tool=requested_tool,
        run_id=run_id,
        now=now,
        pilot_enabled=False,
        human_approval_checkpoint=PREFLIGHT_APPROVAL_CHECKPOINT,
        used_approval_ids=used_approval_ids,
        used_run_ids=used_run_ids,
        target_repo_path=target_repo_path,
        source_subtree_path=source_subtree_path,
        workspace_path=workspace_path,
        implementation_commit_hash=implementation_commit_hash,
        driver_hash=driver_hash,
    )
    diagnostics: list[dict[str, Any]] = []
    files_checked: list[str] = []
    for path in sorted(source_root.rglob("*.py")):
        rel = path.relative_to(source_root).as_posix()
        files_checked.append(rel)
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text, filename=rel)
        except SyntaxError as exc:
            diagnostics.append({"path": rel, "line": exc.lineno, "message": exc.msg})
    after = _snapshot_tree(source_root)
    source_mutation_detected = before != after
    git_mutation_detected = _snapshot_tree(Path(target_repo_path).resolve() / ".git") != _snapshot_tree(
        Path(target_repo_path).resolve() / ".git"
    )
    status = "FAIL" if diagnostics else "PASS"
    pilot_status = L4_FAIL if diagnostics else L4_PASS
    if source_mutation_detected or git_mutation_detected:
        status = "BLOCKED"
        pilot_status = L4_BLOCKED
    return {
        "sprint": SPRINT,
        "pilot_status": pilot_status,
        "status": status,
        "preflight_decision": preflight["decision"],
        "approval_id": preflight["approval_id"],
        "run_id": run_id,
        "requested_tool": REQUESTED_TOOL,
        "files_checked": files_checked,
        "diagnostics": diagnostics,
        "fixed_tool_executed": True,
        "runtime_target_class": "disposable_real_git_repository",
        "replay_consumed": True,
        "source_snapshot_before": before,
        "source_snapshot_after": after,
        "source_mutation_detected": source_mutation_detected,
        "git_mutation_detected": git_mutation_detected,
        "source_write_allowed": False,
        "staging_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "active_vault_read": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "production_isolation_claimed": False,
        "network_called": False,
        "model_service_called": False,
        "browser_tooling_called": False,
        "cyber_tooling_called": False,
        "package_manager_called": False,
        "arbitrary_shell_called": False,
    }



def _reject_runtime_source_scope(source_root: Path) -> None:
    for candidate in source_root.rglob("*"):
        parts = candidate.relative_to(source_root).parts
        if ".git" in parts or candidate.name == ".git":
            raise ValueError("source scope must not include git metadata descendants")
        joined = "/".join(parts)
        if "docs/active" in joined or "docs/requirements" in joined or "docs/use_cases" in joined:
            raise ValueError("source scope must not include protected BLK-req descendant paths")
        if candidate.name in {".env", ".ssh", ".aws", ".gnupg", "credentials", "secrets", "tokens"}:
            raise ValueError("source scope must not include host-secret descendant paths")
        if candidate.is_symlink():
            resolved = candidate.resolve()
            if source_root not in (resolved, *resolved.parents):
                raise ValueError("source scope must not include symlink escapes")


def _validate_runtime_extension(approval_record: dict[str, Any]) -> None:
    extension = approval_record.get("sprint048_runtime")
    if not isinstance(extension, dict):
        raise ValueError("sprint048_runtime extension is required")
    extra = sorted(set(extension) - RUNTIME_EXTENSION_KEYS)
    if extra:
        raise ValueError(f"sprint048_runtime has unsupported keys: {extra}")
    if extension.get("approved_runtime_slice") != APPROVED_RUNTIME_SLICE:
        raise ValueError("approved_runtime_slice must match BLK-SYSTEM-048 runtime slice")
    if extension.get("target_class") != "disposable-real-git-repository-created-by-blk-system-048-harness":
        raise ValueError("target_class must be disposable real Git repository")
    if extension.get("fixed_tool_executed_after_preflight_only") is not True:
        raise ValueError("fixed_tool_executed_after_preflight_only must be true")
    if extension.get("beo_publication") != "DRAFT_ONLY" or extension.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("BEO/RTM authority must remain disabled")
    if extension.get("source_write_allowed") is not False or extension.get("git_mutation_allowed") is not False:
        raise ValueError("source/Git mutation authority must remain false")
    _reject_authority_laundering(extension)


def _reject_authority_laundering(value: Any) -> None:
    if isinstance(value, dict):
        for item in value.values():
            _reject_authority_laundering(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _reject_authority_laundering(item)
    elif isinstance(value, str):
        normalized = value.casefold().replace("_", " ").replace("-", " ")
        allowed = {
            "read only ast validation evidence only",
            "disposable real git repository created by blk system 048 harness",
            APPROVED_RUNTIME_SLICE.casefold().replace("_", " ").replace("-", " "),
            "draft only",
            "not generated",
        }
        if normalized in allowed:
            return
        for marker in AUTHORITY_TEXT_MARKERS:
            if marker in normalized:
                raise ValueError(f"forbidden authority marker in runtime approval: {marker}")


def _snapshot_tree(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    snapshot: dict[str, str] = {}
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file() and not candidate.is_symlink()):
        rel = path.relative_to(root).as_posix()
        snapshot[rel] = _hash_bytes(path.read_bytes())
    return snapshot


def _hash_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()
