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
import re
import zlib
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
    "authorizes",
    "authorized",
    "approval",
    "beo",
    "publish",
    "publication",
    "rtm",
    "drift",
    "coverage",
    "trace",
    "protected",
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
    "signer",
    "ledger",
    "storage",
    "rollback",
    "production isolation",
)
MIN_OUTPUT_BYTE_LIMIT = 512
MAX_LISTED_FILES = 50
MAX_DIAGNOSTICS = 20


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
    output_limit = int(preflight["timeout_output_profile"]["output_byte_limit"])
    if output_limit < MIN_OUTPUT_BYTE_LIMIT:
        raise ValueError("output_byte_limit is too small for bounded BLK-SYSTEM-048 evidence")

    repo = Path(target_repo_path).resolve()
    _require_disposable_real_git_repo(repo)
    source_root = Path(source_subtree_path).resolve()
    _reject_runtime_source_scope(source_root)
    before = _snapshot_tree(source_root, suffix=".py")
    git_before = _snapshot_git_metadata(repo / ".git")
    diagnostics: list[dict[str, Any]] = []
    files_checked: list[str] = []
    for path in sorted(source_root.rglob("*.py")):
        rel = path.relative_to(source_root).as_posix()
        files_checked.append(rel)
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text, filename=rel)
        except SyntaxError as exc:
            if len(diagnostics) < MAX_DIAGNOSTICS:
                diagnostics.append({"path": rel, "line": exc.lineno, "message": exc.msg})
    after = _snapshot_tree(source_root, suffix=".py")
    git_after = _snapshot_git_metadata(repo / ".git")
    source_mutation_detected = before != after
    git_mutation_detected = git_before != git_after
    status = "FAIL" if diagnostics else "PASS"
    pilot_status = L4_FAIL if diagnostics else L4_PASS
    if source_mutation_detected or git_mutation_detected:
        status = "BLOCKED"
        pilot_status = L4_BLOCKED
    evidence = {
        "sprint": SPRINT,
        "pilot_status": pilot_status,
        "status": status,
        "preflight_decision": preflight["decision"],
        "approval_id": preflight["approval_id"],
        "run_id": run_id,
        "requested_tool": REQUESTED_TOOL,
        "files_checked": files_checked[:MAX_LISTED_FILES],
        "files_checked_count": len(files_checked),
        "files_checked_truncated": len(files_checked) > MAX_LISTED_FILES,
        "diagnostics": diagnostics,
        "diagnostics_truncated": len(diagnostics) >= MAX_DIAGNOSTICS,
        "fixed_tool_executed": True,
        "runtime_target_class": "disposable_real_git_repository",
        "replay_consumed": True,
        "source_tree_hash_before": _tree_digest(before),
        "source_tree_hash_after": _tree_digest(after),
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
    evidence["output_byte_limit"] = output_limit
    evidence["evidence_json_bytes"] = 0
    for _ in range(4):
        evidence_bytes = len(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        if evidence_bytes == evidence["evidence_json_bytes"]:
            break
        evidence["evidence_json_bytes"] = evidence_bytes
    final_bytes = len(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    evidence["evidence_json_bytes"] = final_bytes
    if final_bytes > output_limit:
        raise ValueError("output_byte_limit exceeded by bounded BLK-SYSTEM-048 evidence")
    return evidence




def _require_disposable_real_git_repo(repo: Path) -> None:
    git_dir = repo / ".git"
    marker = repo / ".blk-system-048-disposable-repo"
    if not repo.exists() or not repo.is_dir():
        raise ValueError("target must be an existing disposable real Git repository")
    if not git_dir.exists() or not git_dir.is_dir() or git_dir.is_symlink():
        raise ValueError("target must be a disposable real Git repository with a non-symlink .git directory")
    required_git_shape = [git_dir / "HEAD", git_dir / "objects", git_dir / "refs"]
    if not required_git_shape[0].is_file() or not required_git_shape[1].is_dir() or not required_git_shape[2].is_dir():
        raise ValueError("target must be a disposable real Git repository with HEAD, objects, and refs")
    if not marker.is_file() or marker.is_symlink():
        raise ValueError("target must include a harness-owned BLK-SYSTEM-048 disposable repo marker")
    try:
        marker_data = json.loads(marker.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("disposable repo marker must be valid JSON") from exc
    if Path(str(marker_data.get("approved_repo_path", ""))).resolve() != repo:
        raise ValueError("disposable repo marker must bind to the approved repo path")
    marker_head = str(marker_data.get("git_head_commit", "")).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", marker_head):
        raise ValueError("disposable repo marker must include a canonical git_head_commit")
    actual_head = _resolve_git_head_commit(git_dir)
    if actual_head != marker_head:
        raise ValueError("target must be a real Git repository whose HEAD matches the disposable repo marker")
    _require_valid_loose_commit_object(git_dir, actual_head)



def _resolve_git_head_commit(git_dir: Path) -> str:
    head_text = _read_small_text(git_dir / "HEAD", max_bytes=256).strip()
    if re.fullmatch(r"[0-9a-f]{40}", head_text):
        return head_text
    if not head_text.startswith("ref: "):
        raise ValueError("target must be a real Git repository with a valid HEAD")
    ref_name = head_text[5:].strip()
    if not re.fullmatch(r"refs/[A-Za-z0-9._/\-]+", ref_name) or ".." in ref_name:
        raise ValueError("target must be a real Git repository with a safe HEAD ref")
    ref_path = (git_dir / ref_name).resolve()
    if git_dir.resolve() not in (ref_path, *ref_path.parents):
        raise ValueError("target must be a real Git repository with refs inside .git")
    ref_text = _read_small_text(ref_path, max_bytes=128).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", ref_text):
        raise ValueError("target must be a real Git repository with a canonical HEAD ref")
    return ref_text


def _require_valid_loose_commit_object(git_dir: Path, commit_hash: str) -> None:
    object_path = git_dir / "objects" / commit_hash[:2] / commit_hash[2:]
    if not object_path.is_file() or object_path.is_symlink():
        raise ValueError("target must be a real Git repository with a loose HEAD commit object")
    compressed = object_path.read_bytes()
    if len(compressed) > 1_000_000:
        raise ValueError("HEAD commit object is too large for BLK-SYSTEM-048 verification")
    try:
        decompressed = zlib.decompress(compressed)
    except zlib.error as exc:
        raise ValueError("target must be a real Git repository with a valid compressed commit object") from exc
    if len(decompressed) > 1_000_000:
        raise ValueError("HEAD commit object is too large for BLK-SYSTEM-048 verification")
    if hashlib.sha1(decompressed).hexdigest() != commit_hash:
        raise ValueError("target must be a real Git repository with a HEAD object matching its Git SHA-1")
    if not decompressed.startswith(b"commit ") or b"\x00tree " not in decompressed:
        raise ValueError("target must be a real Git repository with a valid HEAD commit object")
    tree_hash = _extract_commit_tree_hash(decompressed)
    _require_valid_loose_tree_object(git_dir, tree_hash)


def _extract_commit_tree_hash(decompressed_commit: bytes) -> str:
    try:
        body = decompressed_commit.split(b"\x00", 1)[1]
    except IndexError as exc:
        raise ValueError("target must be a real Git repository with a valid commit body") from exc
    first_line = body.splitlines()[0].decode("ascii", errors="strict")
    if not first_line.startswith("tree ") or not re.fullmatch(r"tree [0-9a-f]{40}", first_line):
        raise ValueError("target must be a real Git repository with a valid commit tree")
    return first_line.split(" ", 1)[1]


def _require_valid_loose_tree_object(git_dir: Path, tree_hash: str) -> None:
    object_path = git_dir / "objects" / tree_hash[:2] / tree_hash[2:]
    if not object_path.is_file() or object_path.is_symlink():
        raise ValueError("target must be a real Git repository with a loose HEAD tree object")
    compressed = object_path.read_bytes()
    if len(compressed) > 1_000_000:
        raise ValueError("HEAD tree object is too large for BLK-SYSTEM-048 verification")
    try:
        decompressed = zlib.decompress(compressed)
    except zlib.error as exc:
        raise ValueError("target must be a real Git repository with a valid compressed tree object") from exc
    if len(decompressed) > 1_000_000:
        raise ValueError("HEAD tree object is too large for BLK-SYSTEM-048 verification")
    if hashlib.sha1(decompressed).hexdigest() != tree_hash or not decompressed.startswith(b"tree ") or b"\x00" not in decompressed:
        raise ValueError("target must be a real Git repository with a valid HEAD tree object")


def _read_small_text(path: Path, *, max_bytes: int) -> str:
    if not path.is_file() or path.is_symlink():
        raise ValueError("target must be a real Git repository with required control files")
    data = path.read_bytes()
    if len(data) > max_bytes:
        raise ValueError("Git control file exceeds BLK-SYSTEM-048 bounded metadata limit")
    return data.decode("utf-8")


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
    keys = set(extension)
    missing = sorted(RUNTIME_EXTENSION_KEYS - keys)
    extra = sorted(keys - RUNTIME_EXTENSION_KEYS)
    if missing or extra:
        raise ValueError(f"sprint048_runtime keys must be exact; missing={missing} extra={extra}")
    if extension.get("approved_runtime_slice") != APPROVED_RUNTIME_SLICE:
        raise ValueError("approved_runtime_slice must match BLK-SYSTEM-048 runtime slice")
    if extension.get("target_class") != "disposable-real-git-repository-created-by-blk-system-048-harness":
        raise ValueError("target_class must be disposable real Git repository")
    _reject_authority_laundering(extension)
    if extension.get("runtime_notes") != "read-only AST validation evidence only":
        raise ValueError("runtime_notes must be the exact BLK-SYSTEM-048 non-authority marker")
    if extension.get("fixed_tool_executed_after_preflight_only") is not True:
        raise ValueError("fixed_tool_executed_after_preflight_only must be true")
    if extension.get("beo_publication") != "DRAFT_ONLY" or extension.get("rtm_status") != "NOT_GENERATED":
        raise ValueError("BEO/RTM authority must remain disabled")
    if extension.get("source_write_allowed") is not False or extension.get("git_mutation_allowed") is not False:
        raise ValueError("source/Git mutation authority must remain false")


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


def _snapshot_tree(root: Path, *, suffix: str | None = None) -> dict[str, str]:
    if not root.exists():
        return {}
    snapshot: dict[str, str] = {}
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file() and not candidate.is_symlink()):
        if suffix is not None and path.suffix != suffix:
            continue
        rel = path.relative_to(root).as_posix()
        snapshot[rel] = _hash_bytes(path.read_bytes())
    return snapshot


def _snapshot_git_metadata(git_dir: Path) -> dict[str, str]:
    if not git_dir.exists():
        return {}
    snapshot: dict[str, str] = {}
    for path in sorted(git_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError("git metadata symlinks are forbidden in disposable runtime targets")
        rel = path.relative_to(git_dir).as_posix()
        if path.is_dir():
            snapshot[rel] = "dir"
        elif path.is_file():
            stat = path.stat()
            snapshot[rel] = f"file:{stat.st_size}:{stat.st_mtime_ns}"
    return snapshot


def _tree_digest(snapshot: dict[str, str]) -> str:
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _hash_bytes(payload)


def _hash_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()
