from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import shutil
import threading
import time

_INERT_FIXTURE_MARKER = ".blk-system-012-inert-fixture"
_OWNED_MARKER_NAME = ".blk-system-012-owned"
_OWNED_MARKER_TEXT = "BLK-SYSTEM-012-owned"
_PROTECTED_PREFIXES = ("docs/active", "docs/requirements", "docs/use_cases")
_SPRINT_012_WORKSPACE_PREFIX = ".blk-system-012-workspaces"
_SPRINT_012_CACHE_PREFIX = ".blk-system-012-cache"
_SPRINT_012_LOCK_PREFIX = ".blk-system-012-locks"
_SPRINT_012_PREFIXES = (
    _SPRINT_012_WORKSPACE_PREFIX,
    _SPRINT_012_CACHE_PREFIX,
    _SPRINT_012_LOCK_PREFIX,
)
_TERMINAL_STATUSES = frozenset(
    {
        "PASS",
        "FAIL",
        "BLOCKED",
        "FATAL_TIMEOUT",
        "FATAL_OUTPUT_FLOOD",
        "TRANSPORT_ERROR",
        "OPERATOR_INTERRUPTED",
    }
)
_LOCK_OPERATION_MUTEX = threading.RLock()
# Sprint 012 lock probes are deterministic cooperative local probes, not a
# production sandbox or adversarial same-user filesystem lock manager. The mutex
# serializes in-process probe operations; path guards keep lock files as direct
# children of the test-owned lock root so purge/teardown discovery matches the
# acquisition surface.
_FILESYSTEM_RACE_SCOPE = "COOPERATIVE_IN_PROCESS_ONLY"
_PRIMARY_REPO_ROOT = Path("/home/dad/BLK-System").resolve(strict=False)
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def build_workspace_process_boundary_descriptor() -> dict[str, object]:
    """Return Sprint 012 non-authority descriptor metadata."""
    return {
        "sprint": "BLK-SYSTEM-012",
        "authority": "PROBE_ONLY",
        "fixture_scope": "INERT_LOCAL_FIXTURES_ONLY",
        "live_mcp_authorized": False,
        "mcp_server_started": False,
        "mcp_client_started": False,
        "fixed_tool_tests_executed": [],
        "primary_repo_mutation_allowed": False,
        "source_staging_allowed": False,
        "source_commit_allowed": False,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
        "active_vault_read_allowed": False,
        "production_sandbox_claimed": False,
    }


def _resolved(path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def _device(path, provided_device) -> object:
    if provided_device is not None:
        return provided_device
    return _resolved(path).stat().st_dev


def _clone_decision(
    *,
    status: str,
    source_root: Path,
    scratch_root: Path,
    fallback_root: Path | None,
    source_device: object,
    scratch_device: object,
    fallback_device: object | None,
    workspace_parent: Path | None,
    clone_allowed: bool,
    same_filesystem: bool,
    fallback_used: bool,
    reason: str,
) -> dict[str, object]:
    return {
        "status": status,
        "source_root": str(source_root),
        "scratch_root": str(scratch_root),
        "fallback_root": str(fallback_root) if fallback_root is not None else None,
        "source_device": source_device,
        "scratch_device": scratch_device,
        "fallback_device": fallback_device,
        "workspace_parent": str(workspace_parent) if workspace_parent is not None else None,
        "clone_allowed": clone_allowed,
        "same_filesystem": same_filesystem,
        "fallback_used": fallback_used,
        "hardlinks_are_write_isolation": False,
        "primary_repo_mutation_allowed": False,
        "source_staging_allowed": False,
        "source_commit_allowed": False,
        "reason": reason,
    }


def decide_clone_strategy(
    source_root,
    scratch_root,
    *,
    fallback_root=None,
    source_device=None,
    scratch_device=None,
    fallback_device=None,
) -> dict[str, object]:
    """Return a fail-closed hardlink/same-filesystem clone decision."""
    source_path = _resolved(source_root)
    scratch_path = _resolved(scratch_root)
    fallback_path = _resolved(fallback_root) if fallback_root is not None else None
    resolved_source_device = _device(source_path, source_device)
    resolved_scratch_device = _device(scratch_path, scratch_device)
    resolved_fallback_device = (
        _device(fallback_path, fallback_device) if fallback_path is not None else None
    )

    if resolved_source_device == resolved_scratch_device:
        return _clone_decision(
            status="HARDLINK_CLONE_SELECTED",
            source_root=source_path,
            scratch_root=scratch_path,
            fallback_root=fallback_path,
            source_device=resolved_source_device,
            scratch_device=resolved_scratch_device,
            fallback_device=resolved_fallback_device,
            workspace_parent=scratch_path,
            clone_allowed=True,
            same_filesystem=True,
            fallback_used=False,
            reason="source and scratch roots are on the same filesystem",
        )

    if fallback_path is not None and resolved_source_device == resolved_fallback_device:
        return _clone_decision(
            status="SAME_FILESYSTEM_FALLBACK_SELECTED",
            source_root=source_path,
            scratch_root=scratch_path,
            fallback_root=fallback_path,
            source_device=resolved_source_device,
            scratch_device=resolved_scratch_device,
            fallback_device=resolved_fallback_device,
            workspace_parent=fallback_path,
            clone_allowed=True,
            same_filesystem=True,
            fallback_used=True,
            reason="scratch root is on a different filesystem; same-filesystem fallback selected",
        )

    return _clone_decision(
        status="CLONE_BLOCKED_DIFFERENT_FILESYSTEM",
        source_root=source_path,
        scratch_root=scratch_path,
        fallback_root=fallback_path,
        source_device=resolved_source_device,
        scratch_device=resolved_scratch_device,
        fallback_device=resolved_fallback_device,
        workspace_parent=None,
        clone_allowed=False,
        same_filesystem=False,
        fallback_used=False,
        reason="clone blocked because scratch/fallback roots are on a different filesystem",
    )


def _relative_parts(candidate_relative_path) -> tuple[str, ...]:
    return tuple(
        part
        for part in PurePosixPath(str(candidate_relative_path).replace("\\", "/")).parts
        if part not in ("", ".")
    )


def _protected_prefix_match(
    parts: tuple[str, ...], protected_prefixes: tuple[str, ...]
) -> str | None:
    for prefix in protected_prefixes:
        prefix_parts = _relative_parts(prefix)
        if len(parts) >= len(prefix_parts) and parts[: len(prefix_parts)] == prefix_parts:
            return "/".join(prefix_parts)
    return None


def _path_decision(
    *,
    status: str,
    workspace_root: Path,
    relative_path: str,
    resolved_path: Path | None,
    path_accepted: bool,
    reason: str,
) -> dict[str, object]:
    return {
        "status": status,
        "workspace_root": str(workspace_root),
        "relative_path": relative_path,
        "resolved_path": str(resolved_path) if resolved_path is not None else None,
        "path_accepted": path_accepted,
        "active_vault_read_allowed": False,
        "reason": reason,
    }


def validate_workspace_relative_path(
    workspace_root,
    candidate_relative_path,
    *,
    protected_prefixes=_PROTECTED_PREFIXES,
) -> dict[str, object]:
    """Validate a workspace-relative path without allowing escape or protected-vault access."""
    candidate_path = Path(candidate_relative_path)
    workspace_path = _resolved(workspace_root)

    if candidate_path.is_absolute():
        return _path_decision(
            status="PATH_REJECTED_ABSOLUTE",
            workspace_root=workspace_path,
            relative_path=str(candidate_relative_path),
            resolved_path=None,
            path_accepted=False,
            reason="workspace paths must be relative",
        )

    parts = _relative_parts(candidate_relative_path)
    normalized_relative = "/".join(parts)

    if ".." in parts:
        return _path_decision(
            status="PATH_REJECTED_TRAVERSAL",
            workspace_root=workspace_path,
            relative_path=normalized_relative,
            resolved_path=None,
            path_accepted=False,
            reason="parent traversal is not allowed in workspace paths",
        )

    protected_prefix = _protected_prefix_match(tuple(parts), tuple(protected_prefixes))
    if protected_prefix is not None:
        return _path_decision(
            status="PATH_REJECTED_PROTECTED_VAULT",
            workspace_root=workspace_path,
            relative_path=normalized_relative,
            resolved_path=None,
            path_accepted=False,
            reason=f"protected BLK-req vault prefix rejected: {protected_prefix}",
        )

    resolved_candidate = (workspace_path / normalized_relative).resolve(strict=False)
    if not resolved_candidate.is_relative_to(workspace_path):
        return _path_decision(
            status="PATH_REJECTED_SYMLINK_ESCAPE",
            workspace_root=workspace_path,
            relative_path=normalized_relative,
            resolved_path=resolved_candidate,
            path_accepted=False,
            reason="resolved workspace path escapes the workspace root",
        )

    resolved_relative = resolved_candidate.relative_to(workspace_path)
    resolved_protected_prefix = _protected_prefix_match(
        tuple(resolved_relative.parts),
        tuple(protected_prefixes),
    )
    if resolved_protected_prefix is not None:
        return _path_decision(
            status="PATH_REJECTED_PROTECTED_VAULT",
            workspace_root=workspace_path,
            relative_path=normalized_relative,
            resolved_path=resolved_candidate,
            path_accepted=False,
            reason=(
                "resolved workspace path targets protected BLK-req vault prefix: "
                f"{resolved_protected_prefix}"
            ),
        )

    return _path_decision(
        status="PATH_ACCEPTED",
        workspace_root=workspace_path,
        relative_path=normalized_relative,
        resolved_path=resolved_candidate,
        path_accepted=True,
        reason="workspace-relative path accepted",
    )


def _validate_run_id(run_id: str) -> str:
    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must be a non-empty relative token")
    if run_id in {".", ".."}:
        raise ValueError("run_id must not be a traversal token")
    return run_id


def build_run_cache_paths(
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
    """Return run-scoped cache paths outside source/workspace roots."""
    safe_run_id = _validate_run_id(run_id)
    scratch_path = _resolved(scratch_root)
    cache_root = scratch_path / ".blk-system-012-cache" / safe_run_id
    tool_cache = cache_root / "tool-cache"
    output_cache = cache_root / "output-cache"
    return {
        "status": "CACHE_JAIL_SELECTED",
        "scratch_root": str(scratch_path),
        "run_id": safe_run_id,
        "cache_root": str(cache_root),
        "tool_cache": str(tool_cache),
        "output_cache": str(output_cache),
        "paths_created": False,
        "inside_source_root": False,
        "inside_workspace_root": False,
        "source_staging_allowed": False,
        "source_commit_allowed": False,
    }


def _non_authority_fields() -> dict[str, object]:
    return {
        "authority": "PROBE_ONLY",
        "live_mcp_authorized": False,
        "mcp_server_started": False,
        "mcp_client_started": False,
        "primary_repo_mutation_allowed": False,
        "source_staging_allowed": False,
        "source_commit_allowed": False,
        "active_vault_read_allowed": False,
        "production_sandbox_claimed": False,
    }


def _source_decision(
    *,
    status: str,
    source_root: Path,
    source_accepted: bool,
    reason: str,
    **extra,
) -> dict[str, object]:
    decision = {
        "status": status,
        "source_root": str(source_root),
        "source_accepted": source_accepted,
        "reason": reason,
    }
    decision.update(_non_authority_fields())
    decision.update(extra)
    return decision


def _reserved_roots() -> tuple[Path, ...]:
    roots = [
        Path("/").resolve(strict=False),
        Path.home().resolve(strict=False),
        _PRIMARY_REPO_ROOT,
        Path.cwd().resolve(strict=False),
    ]
    unique_roots: list[Path] = []
    for root in roots:
        if root not in unique_roots:
            unique_roots.append(root)
    return tuple(unique_roots)


def _reserved_root_for(path: Path, *, include_descendants: bool = False) -> Path | None:
    for reserved in _reserved_roots():
        if path == reserved:
            return reserved
    if include_descendants and _PRIMARY_REPO_ROOT not in (Path("/"), Path.home().resolve(strict=False)):
        try:
            if path.is_relative_to(_PRIMARY_REPO_ROOT):
                return _PRIMARY_REPO_ROOT
        except ValueError:
            return None
    return None


def _is_owned_by_current_user(path: Path) -> bool:
    try:
        return path.stat(follow_symlinks=False).st_uid == os.geteuid()
    except (FileNotFoundError, PermissionError, OSError):
        return False


def _find_named_path(root: Path, name: str) -> Path | None:
    root_candidate = root / name
    if root_candidate.exists() or root_candidate.is_symlink():
        return root_candidate.resolve(strict=False)

    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(dirs)
        for entry_name in sorted((*dirs, *files)):
            if entry_name == name:
                return (current_path / entry_name).resolve(strict=False)
        dirs[:] = [entry_name for entry_name in dirs if not (current_path / entry_name).is_symlink()]
    return None


def _find_symlink_escape(root: Path) -> tuple[Path, Path] | None:
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(dirs)
        for entry_name in sorted((*dirs, *files)):
            entry_path = current_path / entry_name
            if not entry_path.is_symlink():
                continue
            target_path = entry_path.resolve(strict=False)
            if not target_path.exists() or not target_path.is_relative_to(root):
                return entry_path, target_path
        dirs[:] = [entry_name for entry_name in dirs if not (current_path / entry_name).is_symlink()]
    return None


def assert_inert_fixture_source(source_root) -> dict[str, object]:
    """Accept only marker-protected synthetic fixtures; reject real repos and unmarked roots."""
    raw_source = Path(source_root).expanduser()
    source_path = raw_source.resolve(strict=False)

    reserved_root = _reserved_root_for(source_path, include_descendants=True)
    if reserved_root is not None:
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_RESERVED_ROOT",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source resolves to a reserved root or repository-owned path",
            reserved_root=str(reserved_root),
        )

    if raw_source.is_symlink():
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_SYMLINK_ESCAPE",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source root must not be a symlink",
            escape_path=str(source_path),
        )

    if not source_path.exists():
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_MISSING_ROOT",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source root does not exist",
        )

    if not source_path.is_dir():
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_NOT_DIRECTORY",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source root is not a directory",
        )

    if not _is_owned_by_current_user(source_path):
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_UNOWNED_ROOT",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source root is not owned by the current user",
        )

    git_path = _find_named_path(source_path, ".git")
    if git_path is not None:
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_GIT_DIRECTORY",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source contains .git and is not inert",
            git_path=str(git_path),
        )

    marker_path = source_path / _INERT_FIXTURE_MARKER
    if marker_path.is_symlink() or not marker_path.is_file():
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_MISSING_MARKER",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source lacks the Sprint 012 inert marker file",
            marker_name=_INERT_FIXTURE_MARKER,
            marker_path=str(marker_path),
        )

    if not _is_owned_by_current_user(marker_path):
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_UNOWNED_MARKER",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source marker is not owned by the current user",
            marker_name=_INERT_FIXTURE_MARKER,
            marker_path=str(marker_path),
        )

    symlink_escape = _find_symlink_escape(source_path)
    if symlink_escape is not None:
        link_path, target_path = symlink_escape
        return _source_decision(
            status="INERT_FIXTURE_REJECTED_SYMLINK_ESCAPE",
            source_root=source_path,
            source_accepted=False,
            reason="fixture source contains a symlink that escapes the fixture root",
            symlink_path=str(link_path),
            escape_path=str(target_path),
        )

    return _source_decision(
        status="INERT_FIXTURE_SOURCE_ACCEPTED",
        source_root=source_path,
        source_accepted=True,
        reason="fixture source is marker-protected, synthetic, and locally owned",
        marker_name=_INERT_FIXTURE_MARKER,
        marker_path=str(marker_path),
    )


def _iter_manifest_files(source_path: Path) -> list[Path]:
    manifest_paths: list[Path] = []
    for current, dirs, files in os.walk(source_path, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(dirs)
        for file_name in sorted(files):
            manifest_paths.append(current_path / file_name)
        for dir_name in list(dirs):
            dir_path = current_path / dir_name
            if dir_path.is_symlink():
                manifest_paths.append(dir_path)
        dirs[:] = [dir_name for dir_name in dirs if not (current_path / dir_name).is_symlink()]
    return sorted(manifest_paths, key=lambda path: path.relative_to(source_path).as_posix())


def _file_manifest_entry(source_path: Path, file_path: Path) -> dict[str, object]:
    relative_path = file_path.relative_to(source_path).as_posix()
    stat_result = file_path.lstat()
    mode = stat_result.st_mode & 0o777

    if file_path.is_symlink():
        target = os.readlink(file_path)
        digest = hashlib.sha256(target.encode("utf-8")).hexdigest()
        return {
            "path": relative_path,
            "type": "symlink",
            "target": target,
            "size": len(target),
            "mode": mode,
            "sha256": digest,
        }

    data = file_path.read_bytes()
    return {
        "path": relative_path,
        "type": "file",
        "size": stat_result.st_size,
        "mode": mode,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def manifest_source_tree(source_root) -> dict[str, object]:
    """Return deterministic file metadata/hash manifest for primary-corruption checks."""
    source_validation = assert_inert_fixture_source(source_root)
    source_path = Path(source_validation["source_root"])
    if not source_validation["source_accepted"]:
        return {
            "status": "SOURCE_MANIFEST_REJECTED_SOURCE",
            "source_root": str(source_path),
            "manifest_created": False,
            "source_validation": source_validation,
            "files": [],
            "file_count": 0,
            **_non_authority_fields(),
        }

    files = [_file_manifest_entry(source_path, path) for path in _iter_manifest_files(source_path)]
    manifest_hash = hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "status": "SOURCE_MANIFEST_CREATED",
        "source_root": str(source_path),
        "manifest_created": True,
        "source_validation": source_validation,
        "files": files,
        "file_count": len(files),
        "manifest_sha256": manifest_hash,
        **_non_authority_fields(),
    }


def _root_decision(
    *,
    status: str,
    root_path: Path,
    root_accepted: bool,
    reason: str,
    **extra,
) -> dict[str, object]:
    decision = {
        "status": status,
        "root_path": str(root_path),
        "root_accepted": root_accepted,
        "reason": reason,
    }
    decision.update(_non_authority_fields())
    decision.update(extra)
    return decision


def _validate_scratch_root(scratch_root) -> dict[str, object]:
    raw_root = Path(scratch_root).expanduser()
    scratch_path = raw_root.resolve(strict=False)
    reserved_root = _reserved_root_for(scratch_path, include_descendants=True)
    if reserved_root is not None:
        return _root_decision(
            status="SCRATCH_ROOT_REJECTED_RESERVED_ROOT",
            root_path=scratch_path,
            root_accepted=False,
            reason="scratch root resolves to a reserved root or repository-owned path",
            reserved_root=str(reserved_root),
        )
    if raw_root.is_symlink():
        return _root_decision(
            status="SCRATCH_ROOT_REJECTED_SYMLINK",
            root_path=scratch_path,
            root_accepted=False,
            reason="scratch root must not be a symlink",
        )
    if not scratch_path.exists() or not scratch_path.is_dir():
        return _root_decision(
            status="SCRATCH_ROOT_REJECTED_MISSING_DIRECTORY",
            root_path=scratch_path,
            root_accepted=False,
            reason="scratch root must be an existing directory",
        )
    if not _is_owned_by_current_user(scratch_path):
        return _root_decision(
            status="SCRATCH_ROOT_REJECTED_UNOWNED_ROOT",
            root_path=scratch_path,
            root_accepted=False,
            reason="scratch root is not owned by the current user",
        )
    return _root_decision(
        status="SCRATCH_ROOT_ACCEPTED",
        root_path=scratch_path,
        root_accepted=True,
        reason="scratch root is locally owned and outside reserved roots",
    )


def _write_owned_marker(directory: Path) -> Path:
    marker_path = directory / _OWNED_MARKER_NAME
    marker_path.write_text(f"{_OWNED_MARKER_TEXT}\n")
    return marker_path


def create_inert_workspace_fixture(
    source_root,
    scratch_root,
    *,
    run_id: str,
) -> dict[str, object]:
    """Create a temp-root workspace fixture only after inert marker validation."""
    safe_run_id = _validate_run_id(run_id)
    source_validation = assert_inert_fixture_source(source_root)
    scratch_validation = _validate_scratch_root(scratch_root)
    source_path = Path(source_validation["source_root"])
    scratch_path = Path(scratch_validation["root_path"])
    run_root = scratch_path / _SPRINT_012_WORKSPACE_PREFIX / safe_run_id
    workspace_path = run_root / "workspace"
    base_decision = {
        "source_root": str(source_path),
        "scratch_root": str(scratch_path),
        "run_id": safe_run_id,
        "run_root": str(run_root),
        "workspace_path": str(workspace_path),
        "source_validation": source_validation,
        "scratch_validation": scratch_validation,
        "workspace_created": False,
        "hardlinks_are_write_isolation": False,
        **_non_authority_fields(),
    }

    if not source_validation["source_accepted"]:
        return {
            **base_decision,
            "status": "WORKSPACE_FIXTURE_REJECTED_SOURCE",
            "reason": "workspace fixture creation requires an accepted inert source fixture",
        }

    if not scratch_validation["root_accepted"]:
        return {
            **base_decision,
            "status": "WORKSPACE_FIXTURE_REJECTED_SCRATCH_ROOT",
            "reason": "workspace fixture creation requires a safe scratch root",
        }

    if not workspace_path.resolve(strict=False).is_relative_to(scratch_path):
        return {
            **base_decision,
            "status": "WORKSPACE_FIXTURE_REJECTED_SCRATCH_ESCAPE",
            "reason": "workspace path does not remain under scratch root",
        }

    if run_root.exists() or run_root.is_symlink():
        return {
            **base_decision,
            "status": "WORKSPACE_FIXTURE_REJECTED_EXISTING_RUN_PATH",
            "reason": "workspace run path already exists and will not be overwritten",
        }

    run_root.mkdir(parents=True)
    _write_owned_marker(run_root)
    shutil.copytree(source_path, workspace_path, symlinks=True, copy_function=shutil.copy2)
    _write_owned_marker(workspace_path)

    return {
        **base_decision,
        "status": "WORKSPACE_FIXTURE_CREATED",
        "workspace_created": True,
        "owned_marker_name": _OWNED_MARKER_NAME,
        "owned_marker_path": str(run_root / _OWNED_MARKER_NAME),
        "reason": "workspace fixture cloned under scratch root after inert marker validation",
    }


def _owned_directory(path: Path) -> bool:
    marker_path = path / _OWNED_MARKER_NAME
    if marker_path.is_symlink() or not marker_path.is_file():
        return False
    try:
        return marker_path.read_text().startswith(_OWNED_MARKER_TEXT)
    except (OSError, UnicodeDecodeError):
        return False


def _probe_lock_payload_owned(payload: object) -> bool:
    if not isinstance(payload, dict):
        return False
    if payload.get("sprint") != "BLK-SYSTEM-012":
        return False
    if payload.get("authority") != "PROBE_ONLY":
        return False
    run_id = payload.get("run_id")
    pid = payload.get("pid")
    if not isinstance(run_id, str):
        return False
    try:
        _validate_run_id(run_id)
    except ValueError:
        return False
    return isinstance(pid, int) and not isinstance(pid, bool)


def _read_json_lock_payload(path: Path) -> tuple[bool, dict[str, object] | None, str]:
    try:
        text = path.read_text()
    except FileNotFoundError:
        return False, None, "missing"
    except (OSError, UnicodeDecodeError):
        return False, None, "unreadable"
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return False, None, "malformed json"
    if not _probe_lock_payload_owned(payload):
        return False, None, "not a Sprint 012 PROBE_ONLY JSON lock"
    return True, payload, "owned"


def _owned_lock_file(path: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return False
    if _OWNED_MARKER_TEXT in text:
        return True
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return False
    return _probe_lock_payload_owned(payload)


def _lock_pid(path: Path) -> int | None:
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return None
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        payload = None
    if _probe_lock_payload_owned(payload):
        return int(payload["pid"])
    try:
        for line in text.splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "pid":
                return int(value.strip())
    except ValueError:
        return None
    return None


def _lock_run_id(path: Path) -> str | None:
    owned, payload, _reason = _read_json_lock_payload(path)
    if owned and payload is not None:
        return str(payload["run_id"])
    if _owned_lock_file(path):
        return path.stem
    return None


def _default_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _path_exists_or_symlink(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _symlink_ancestor_between(candidate: Path, stop_at: Path) -> Path | None:
    current = candidate.parent
    while current != stop_at and current.parent != current:
        if current.is_symlink():
            return current
        current = current.parent
    return None


def _probe_lock_path_guard(lock_path) -> dict[str, object]:
    raw_path = Path(lock_path).expanduser()
    resolved_path = raw_path.resolve(strict=False)
    guard: dict[str, object] = {
        "path_accepted": False,
        "raw_lock_path": str(raw_path),
        "lock_path": str(resolved_path),
        "scratch_root": None,
        "lock_root": None,
        "scratch_validation": None,
        "reason": "lock path rejected",
    }

    if not raw_path.is_absolute():
        return {
            **guard,
            "reason": "lock path must be absolute and root-anchored",
        }

    if raw_path.is_symlink():
        return {
            **guard,
            "reason": "lock path symlink preserved",
        }

    raw_anchor = _path_prefix_anchor(raw_path, (_SPRINT_012_LOCK_PREFIX,))
    if raw_anchor is None:
        return {
            **guard,
            "reason": "lock path is outside the Sprint 012 lock prefix",
        }

    raw_scratch_path, _prefix = raw_anchor
    scratch_validation = _validate_scratch_root(raw_scratch_path)
    scratch_path = Path(scratch_validation["root_path"])
    lock_root = scratch_path / _SPRINT_012_LOCK_PREFIX
    guard.update(
        {
            "scratch_root": str(scratch_path),
            "lock_root": str(lock_root),
            "scratch_validation": scratch_validation,
        }
    )

    if not scratch_validation["root_accepted"]:
        return {
            **guard,
            "lock_path": str(resolved_path),
            "reason": "lock path scratch anchor is unsafe",
        }

    if raw_path.parent.resolve(strict=False) != lock_root:
        return {
            **guard,
            "lock_path": str(resolved_path),
            "reason": "lock path must be a direct child of the Sprint 012 lock root",
        }

    resolved_path = raw_path.resolve(strict=False)
    if resolved_path == lock_root or not resolved_path.is_relative_to(lock_root):
        return {
            **guard,
            "lock_path": str(resolved_path),
            "reason": "resolved lock path escapes the Sprint 012 lock root",
        }

    symlink_ancestor = _symlink_ancestor_between(raw_path, raw_scratch_path)
    if symlink_ancestor is not None:
        return {
            **guard,
            "lock_path": str(resolved_path),
            "symlink_path": str(symlink_ancestor),
            "reason": "lock path contains a symlink ancestor",
        }

    if raw_path.exists() and raw_path.is_dir():
        return {
            **guard,
            "lock_path": str(resolved_path),
            "reason": "lock path is not a regular file",
        }

    return {
        **guard,
        "path_accepted": True,
        "lock_path": str(resolved_path),
        "reason": "lock path accepted under safe Sprint 012 scratch root",
    }


def _lock_result(status: str, lock_path: Path, **extra) -> dict[str, object]:
    decision = {
        "status": status,
        "sprint": "BLK-SYSTEM-012",
        "lock_path": str(lock_path),
        "filesystem_race_scope": _FILESYSTEM_RACE_SCOPE,
        **_non_authority_fields(),
    }
    decision.update(extra)
    return decision


def _blocked_unowned_lock_result(lock_path, *, guard: dict[str, object], reason: str) -> dict[str, object]:
    path = Path(guard.get("lock_path") or Path(lock_path).expanduser().resolve(strict=False))
    raw_path = Path(lock_path).expanduser()
    return _lock_result(
        "LOCK_BLOCKED_UNOWNED",
        path,
        lock_exists=_path_exists_or_symlink(raw_path),
        lock_owned=False,
        lock_json_valid=False,
        path_accepted=bool(guard.get("path_accepted")),
        scratch_root=guard.get("scratch_root"),
        lock_root=guard.get("lock_root"),
        reason=reason,
    )


def probe_lock_state(lock_path, *, pid_alive=None) -> dict[str, object]:
    """Inspect a probe-owned lock without killing arbitrary host PIDs."""
    guard = _probe_lock_path_guard(lock_path)
    lock_path_obj = Path(guard["lock_path"])
    if not guard["path_accepted"]:
        return _blocked_unowned_lock_result(
            lock_path,
            guard=guard,
            reason=str(guard["reason"]),
        )

    if not lock_path_obj.exists():
        return _lock_result(
            "LOCK_ABSENT",
            lock_path_obj,
            lock_exists=False,
            lock_owned=False,
            lock_json_valid=False,
            path_accepted=True,
            scratch_root=guard.get("scratch_root"),
            lock_root=guard.get("lock_root"),
            reason="lock path is absent",
        )

    if lock_path_obj.is_symlink() or not lock_path_obj.is_file():
        return _lock_result(
            "LOCK_BLOCKED_UNOWNED",
            lock_path_obj,
            lock_exists=True,
            lock_owned=False,
            lock_json_valid=False,
            path_accepted=True,
            scratch_root=guard.get("scratch_root"),
            lock_root=guard.get("lock_root"),
            reason="lock path is not a regular probe JSON lock",
        )

    owned, payload, reason = _read_json_lock_payload(lock_path_obj)
    if not owned or payload is None:
        return _lock_result(
            "LOCK_BLOCKED_UNOWNED",
            lock_path_obj,
            lock_exists=True,
            lock_owned=False,
            lock_json_valid=False,
            path_accepted=True,
            scratch_root=guard.get("scratch_root"),
            lock_root=guard.get("lock_root"),
            reason=reason,
        )

    owner_run_id = str(payload["run_id"])
    owner_pid = int(payload["pid"])
    pid_checker = pid_alive if pid_alive is not None else _default_pid_alive
    try:
        live = bool(pid_checker(owner_pid))
    except Exception:
        live = True
    status = "LOCK_BLOCKED_LIVE_PID" if live else "STALE_LOCK_DETECTED"
    return _lock_result(
        status,
        lock_path_obj,
        lock_exists=True,
        lock_owned=True,
        lock_json_valid=True,
        owner_run_id=owner_run_id,
        owner_pid=owner_pid,
        blocked_by_run_id=owner_run_id if live else None,
        blocked_by_pid=owner_pid if live else None,
        pid_alive=live,
        stale_lock=not live,
        path_accepted=True,
        scratch_root=guard.get("scratch_root"),
        lock_root=guard.get("lock_root"),
        reason="probe JSON lock is live" if live else "probe JSON lock has a dead pid",
    )


def _coerce_lock_pid(pid) -> int:
    if pid is None:
        return os.getpid()
    if isinstance(pid, bool) or not isinstance(pid, int):
        raise ValueError("pid must be an integer")
    return pid


def acquire_probe_lock(
    lock_path,
    *,
    run_id: str,
    pid=None,
    max_wait_seconds: float = 0.0,
    poll_interval_seconds: float = 0.01,
    pid_alive=None,
) -> dict[str, object]:
    """Acquire a lock with atomic exclusive creation and bounded wait."""
    safe_run_id = _validate_run_id(run_id)
    lock_pid = _coerce_lock_pid(pid)
    if max_wait_seconds < 0:
        raise ValueError("max_wait_seconds must be non-negative")
    if poll_interval_seconds <= 0:
        raise ValueError("poll_interval_seconds must be positive")

    guard = _probe_lock_path_guard(lock_path)
    lock_path_obj = Path(guard["lock_path"])
    if not guard["path_accepted"]:
        return _blocked_unowned_lock_result(
            lock_path,
            guard=guard,
            reason=str(guard["reason"]),
        )

    try:
        lock_path_obj.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return _lock_result(
            "LOCK_BLOCKED_UNOWNED",
            lock_path_obj,
            run_id=safe_run_id,
            pid=lock_pid,
            acquired=False,
            lock_exists=_path_exists_or_symlink(lock_path_obj),
            lock_owned=False,
            lock_json_valid=False,
            path_accepted=True,
            scratch_root=guard.get("scratch_root"),
            lock_root=guard.get("lock_root"),
            max_wait_seconds=max_wait_seconds,
            poll_interval_seconds=poll_interval_seconds,
            wait_expired=False,
            events=[],
            reason=f"lock parent could not be created: {exc}",
        )

    guard = _probe_lock_path_guard(lock_path_obj)
    lock_path_obj = Path(guard["lock_path"])
    if not guard["path_accepted"]:
        return _blocked_unowned_lock_result(
            lock_path_obj,
            guard=guard,
            reason=str(guard["reason"]),
        )

    deadline = time.monotonic() + float(max_wait_seconds)
    events: list[str] = []
    previous_status: str | None = None
    pid_checker = pid_alive if pid_alive is not None else _default_pid_alive
    payload = {
        "sprint": "BLK-SYSTEM-012",
        "authority": "PROBE_ONLY",
        "run_id": safe_run_id,
        "pid": lock_pid,
    }
    lock_text = json.dumps(payload, sort_keys=True) + "\n"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

    while True:
        sleep_seconds: float | None = None
        with _LOCK_OPERATION_MUTEX:
            try:
                fd = os.open(lock_path_obj, flags, 0o600)
            except FileExistsError:
                state = probe_lock_state(lock_path_obj, pid_alive=pid_checker)
                state_status = state["status"]
                if state_status == "LOCK_ABSENT":
                    continue
                if state_status == "STALE_LOCK_DETECTED":
                    current_state = probe_lock_state(lock_path_obj, pid_alive=pid_checker)
                    stale_state_still_current = (
                        current_state["status"] == "STALE_LOCK_DETECTED"
                        and current_state.get("owner_run_id") == state.get("owner_run_id")
                        and current_state.get("owner_pid") == state.get("owner_pid")
                    )
                    if not stale_state_still_current:
                        events.append("STALE_LOCK_CHANGED_BEFORE_REMOVAL")
                        continue
                    try:
                        lock_path_obj.unlink()
                    except FileNotFoundError:
                        events.append("STALE_LOCK_ALREADY_REMOVED")
                    except OSError as exc:
                        return _lock_result(
                            "LOCK_BLOCKED_UNOWNED",
                            lock_path_obj,
                            run_id=safe_run_id,
                            pid=lock_pid,
                            acquired=False,
                            lock_exists=_path_exists_or_symlink(lock_path_obj),
                            lock_owned=state.get("lock_owned", False),
                            lock_json_valid=state.get("lock_json_valid", False),
                            path_accepted=True,
                            scratch_root=guard.get("scratch_root"),
                            lock_root=guard.get("lock_root"),
                            max_wait_seconds=max_wait_seconds,
                            poll_interval_seconds=poll_interval_seconds,
                            wait_expired=False,
                            events=events,
                            previous_status=previous_status,
                            reason=f"stale lock could not be removed: {exc}",
                        )
                    else:
                        previous_status = "STALE_LOCK_REMOVED"
                        events.append("STALE_LOCK_REMOVED")
                    continue
                if state_status == "LOCK_BLOCKED_LIVE_PID":
                    now = time.monotonic()
                    if max_wait_seconds == 0 or now >= deadline:
                        return _lock_result(
                            "LOCK_BLOCKED_LIVE_PID",
                            lock_path_obj,
                            run_id=safe_run_id,
                            pid=lock_pid,
                            acquired=False,
                            lock_exists=True,
                            lock_owned=True,
                            lock_json_valid=True,
                            blocked_by_run_id=state.get("blocked_by_run_id"),
                            blocked_by_pid=state.get("blocked_by_pid"),
                            path_accepted=True,
                            scratch_root=guard.get("scratch_root"),
                            lock_root=guard.get("lock_root"),
                            max_wait_seconds=max_wait_seconds,
                            poll_interval_seconds=poll_interval_seconds,
                            wait_expired=max_wait_seconds > 0,
                            events=events,
                            previous_status=previous_status,
                            reason="live probe JSON lock preserved",
                        )
                    remaining = max(0.0, deadline - now)
                    sleep_seconds = min(float(poll_interval_seconds), remaining)
                else:
                    return _lock_result(
                        "LOCK_BLOCKED_UNOWNED",
                        lock_path_obj,
                        run_id=safe_run_id,
                        pid=lock_pid,
                        acquired=False,
                        lock_exists=state.get("lock_exists", True),
                        lock_owned=False,
                        lock_json_valid=state.get("lock_json_valid", False),
                        path_accepted=True,
                        scratch_root=guard.get("scratch_root"),
                        lock_root=guard.get("lock_root"),
                        max_wait_seconds=max_wait_seconds,
                        poll_interval_seconds=poll_interval_seconds,
                        wait_expired=False,
                        events=events,
                        previous_status=previous_status,
                        reason=str(state.get("reason", "existing lock is not owned by this probe")),
                    )
            except FileNotFoundError:
                lock_path_obj.parent.mkdir(parents=True, exist_ok=True)
                continue
            except OSError as exc:
                return _lock_result(
                    "LOCK_BLOCKED_UNOWNED",
                    lock_path_obj,
                    run_id=safe_run_id,
                    pid=lock_pid,
                    acquired=False,
                    lock_exists=_path_exists_or_symlink(lock_path_obj),
                    lock_owned=False,
                    lock_json_valid=False,
                    path_accepted=True,
                    scratch_root=guard.get("scratch_root"),
                    lock_root=guard.get("lock_root"),
                    max_wait_seconds=max_wait_seconds,
                    poll_interval_seconds=poll_interval_seconds,
                    wait_expired=False,
                    events=events,
                    previous_status=previous_status,
                    reason=f"atomic lock creation failed: {exc}",
                )
            else:
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as lock_file:
                        lock_file.write(lock_text)
                except Exception:
                    try:
                        lock_path_obj.unlink()
                    except OSError:
                        pass
                    raise
                return _lock_result(
                    "LOCK_ACQUIRED",
                    lock_path_obj,
                    run_id=safe_run_id,
                    pid=lock_pid,
                    acquired=True,
                    lock_exists=True,
                    lock_owned=True,
                    lock_json_valid=True,
                    path_accepted=True,
                    scratch_root=guard.get("scratch_root"),
                    lock_root=guard.get("lock_root"),
                    max_wait_seconds=max_wait_seconds,
                    poll_interval_seconds=poll_interval_seconds,
                    wait_expired=False,
                    events=events,
                    previous_status=previous_status,
                    reason="probe lock acquired with atomic exclusive creation",
                )
        if sleep_seconds is not None:
            time.sleep(sleep_seconds)
            continue


def release_probe_lock(lock_path, *, run_id: str) -> dict[str, object]:
    """Release only locks owned by this run_id."""
    safe_run_id = _validate_run_id(run_id)
    guard = _probe_lock_path_guard(lock_path)
    lock_path_obj = Path(guard["lock_path"])
    if not guard["path_accepted"]:
        return _lock_result(
            "LOCK_RELEASE_SKIPPED_NOT_OWNER",
            lock_path_obj,
            run_id=safe_run_id,
            released=False,
            lock_exists=_path_exists_or_symlink(Path(lock_path).expanduser()),
            lock_owned=False,
            lock_json_valid=False,
            path_accepted=False,
            scratch_root=guard.get("scratch_root"),
            lock_root=guard.get("lock_root"),
            reason=str(guard["reason"]),
        )

    with _LOCK_OPERATION_MUTEX:
        owned, payload, reason = _read_json_lock_payload(lock_path_obj)
        if not owned or payload is None or payload["run_id"] != safe_run_id:
            return _lock_result(
                "LOCK_RELEASE_SKIPPED_NOT_OWNER",
                lock_path_obj,
                run_id=safe_run_id,
                released=False,
                lock_exists=_path_exists_or_symlink(lock_path_obj),
                lock_owned=bool(owned),
                lock_json_valid=bool(owned),
                owner_run_id=payload.get("run_id") if isinstance(payload, dict) else None,
                owner_pid=payload.get("pid") if isinstance(payload, dict) else None,
                path_accepted=True,
                scratch_root=guard.get("scratch_root"),
                lock_root=guard.get("lock_root"),
                reason=reason if not owned else "lock is owned by a different run_id",
            )

        current_owned, current_payload, current_reason = _read_json_lock_payload(lock_path_obj)
        if not current_owned or current_payload != payload:
            return _lock_result(
                "LOCK_RELEASE_SKIPPED_NOT_OWNER",
                lock_path_obj,
                run_id=safe_run_id,
                released=False,
                lock_exists=_path_exists_or_symlink(lock_path_obj),
                lock_owned=bool(current_owned),
                lock_json_valid=bool(current_owned),
                owner_run_id=current_payload.get("run_id")
                if isinstance(current_payload, dict)
                else None,
                owner_pid=current_payload.get("pid")
                if isinstance(current_payload, dict)
                else None,
                path_accepted=True,
                scratch_root=guard.get("scratch_root"),
                lock_root=guard.get("lock_root"),
                reason=(
                    current_reason
                    if not current_owned
                    else "lock changed before owner release"
                ),
            )

        try:
            lock_path_obj.unlink()
        except FileNotFoundError:
            return _lock_result(
                "LOCK_RELEASE_SKIPPED_NOT_OWNER",
                lock_path_obj,
                run_id=safe_run_id,
                released=False,
                lock_exists=False,
                lock_owned=False,
                lock_json_valid=False,
                path_accepted=True,
                scratch_root=guard.get("scratch_root"),
                lock_root=guard.get("lock_root"),
                reason="lock was already absent",
            )
    return _lock_result(
        "LOCK_RELEASED",
        lock_path_obj,
        run_id=safe_run_id,
        released=True,
        lock_exists=False,
        lock_owned=True,
        lock_json_valid=True,
        owner_run_id=safe_run_id,
        owner_pid=payload["pid"],
        path_accepted=True,
        scratch_root=guard.get("scratch_root"),
        lock_root=guard.get("lock_root"),
        reason="probe lock released by owning run_id",
    )


def _remove_owned_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
        return
    path.unlink()


def startup_purge_owned_stale_paths(scratch_root, *, pid_alive=None) -> dict[str, object]:
    """Remove only marked Sprint 012 stale probe paths/locks under scratch root."""
    scratch_validation = _validate_scratch_root(scratch_root)
    scratch_path = Path(scratch_validation["root_path"])
    removed_paths: list[str] = []
    preserved_paths: list[str] = []
    pid_checker = pid_alive if pid_alive is not None else _default_pid_alive

    if not scratch_validation["root_accepted"]:
        return {
            "status": "STARTUP_PURGE_BLOCKED_UNSAFE_SCRATCH_ROOT",
            "scratch_root": str(scratch_path),
            "scratch_validation": scratch_validation,
            "removed_paths": removed_paths,
            "preserved_paths": preserved_paths,
            "purge_completed": False,
            **_non_authority_fields(),
        }

    live_lock_run_ids: set[str] = set()
    lock_root = scratch_path / _SPRINT_012_LOCK_PREFIX
    if lock_root.exists() and lock_root.is_dir() and not lock_root.is_symlink():
        for lock_path in sorted(lock_root.iterdir(), key=lambda child: child.name):
            lock_resolved = lock_path.resolve(strict=False)
            if not lock_resolved.is_relative_to(scratch_path):
                continue
            if lock_path.is_symlink() or not _owned_lock_file(lock_path):
                continue
            pid = _lock_pid(lock_path)
            try:
                live = bool(pid is not None and pid_checker(pid))
            except Exception:
                live = True
            if live:
                run_id = _lock_run_id(lock_path)
                if run_id is not None:
                    live_lock_run_ids.add(run_id)

    for prefix in (_SPRINT_012_WORKSPACE_PREFIX, _SPRINT_012_CACHE_PREFIX):
        prefix_root = scratch_path / prefix
        if not prefix_root.exists() or not prefix_root.is_dir() or prefix_root.is_symlink():
            continue
        for candidate in sorted(prefix_root.iterdir(), key=lambda child: child.name):
            candidate_resolved = candidate.resolve(strict=False)
            if not candidate_resolved.is_relative_to(scratch_path):
                preserved_paths.append(str(candidate_resolved))
                continue
            if candidate.name in live_lock_run_ids:
                preserved_paths.append(str(candidate_resolved))
                continue
            if candidate.is_symlink() or not _owned_directory(candidate):
                preserved_paths.append(str(candidate_resolved))
                continue
            _remove_owned_path(candidate)
            removed_paths.append(str(candidate_resolved))

    lock_root = scratch_path / _SPRINT_012_LOCK_PREFIX
    if lock_root.exists() and lock_root.is_dir() and not lock_root.is_symlink():
        for lock_path in sorted(lock_root.iterdir(), key=lambda child: child.name):
            lock_resolved = lock_path.resolve(strict=False)
            if not lock_resolved.is_relative_to(scratch_path):
                preserved_paths.append(str(lock_resolved))
                continue
            if lock_path.is_symlink() or not _owned_lock_file(lock_path):
                preserved_paths.append(str(lock_resolved))
                continue
            pid = _lock_pid(lock_path)
            try:
                live = bool(pid is not None and pid_checker(pid))
            except Exception:
                live = True
            if live:
                preserved_paths.append(str(lock_resolved))
                continue
            _remove_owned_path(lock_path)
            removed_paths.append(str(lock_resolved))

    return {
        "status": "STARTUP_PURGE_COMPLETED",
        "scratch_root": str(scratch_path),
        "scratch_validation": scratch_validation,
        "removed_paths": removed_paths,
        "preserved_paths": preserved_paths,
        "purge_completed": True,
        **_non_authority_fields(),
    }


def _path_prefix_anchor(path: Path, allowed_prefixes: tuple[str, ...]) -> tuple[Path, str] | None:
    parts = path.parts
    for prefix in allowed_prefixes:
        if prefix not in parts:
            continue
        index = parts.index(prefix)
        if index == 0:
            return None
        scratch_path = Path(*parts[:index])
        return scratch_path, prefix
    return None


def _has_owned_marker_between(path: Path, stop_at: Path) -> bool:
    current = path if path.is_dir() else path.parent
    while True:
        if _owned_directory(current):
            return True
        if current == stop_at or current.parent == current:
            return False
        current = current.parent


def _run_id_from_workspace_path(workspace_path: Path) -> str | None:
    parts = workspace_path.expanduser().resolve(strict=False).parts
    try:
        index = parts.index(_SPRINT_012_WORKSPACE_PREFIX)
    except ValueError:
        return None
    if index + 1 >= len(parts):
        return None
    run_id = parts[index + 1]
    try:
        return _validate_run_id(run_id)
    except ValueError:
        return None


def _lock_owned_for_teardown(path: Path, expected_run_id: str | None) -> bool:
    owned, payload, _reason = _read_json_lock_payload(path)
    if owned and payload is not None:
        return expected_run_id is not None and payload["run_id"] == expected_run_id
    if not _owned_lock_file(path):
        return False
    return expected_run_id is not None and path.stem == expected_run_id


def _remove_guarded_teardown_path(
    path,
    *,
    allowed_prefixes: tuple[str, ...],
    lock_file: bool,
    expected_run_id: str | None = None,
) -> tuple[bool, str, str]:
    candidate = Path(path).expanduser()
    if not candidate.exists() and not candidate.is_symlink():
        return False, str(candidate.resolve(strict=False)), "missing"

    if candidate.is_symlink():
        return False, str(candidate.resolve(strict=False)), "symlink preserved"

    resolved_candidate = candidate.resolve(strict=False)
    reserved_root = _reserved_root_for(resolved_candidate, include_descendants=True)
    if reserved_root is not None:
        return False, str(resolved_candidate), "reserved root preserved"

    anchor = _path_prefix_anchor(resolved_candidate, allowed_prefixes)
    if anchor is None:
        return False, str(resolved_candidate), "outside Sprint 012 prefix"
    scratch_path, prefix = anchor
    scratch_validation = _validate_scratch_root(scratch_path)
    if not scratch_validation["root_accepted"]:
        return False, str(resolved_candidate), "unsafe scratch anchor preserved"
    if not resolved_candidate.is_relative_to(scratch_path):
        return False, str(resolved_candidate), "scratch escape preserved"

    prefix_root = scratch_path / prefix
    if lock_file:
        if prefix != _SPRINT_012_LOCK_PREFIX:
            return False, str(resolved_candidate), "unowned lock preserved"
        with _LOCK_OPERATION_MUTEX:
            if not _lock_owned_for_teardown(candidate, expected_run_id):
                return False, str(resolved_candidate), "unowned lock preserved"
            if not _lock_owned_for_teardown(candidate, expected_run_id):
                return False, str(resolved_candidate), "lock changed before teardown removal"
            _remove_owned_path(candidate)
        return True, str(resolved_candidate), "removed"
    elif not _has_owned_marker_between(candidate, prefix_root):
        return False, str(resolved_candidate), "unowned path preserved"

    _remove_owned_path(candidate)
    return True, str(resolved_candidate), "removed"


def _cache_cleanup_candidates(cache_paths) -> list[Path]:
    if cache_paths is None:
        return []
    if isinstance(cache_paths, dict):
        ordered_paths: list[Path] = []
        for key in ("cache_root", "tool_cache", "output_cache"):
            if key in cache_paths and cache_paths[key] is not None:
                ordered_paths.append(Path(cache_paths[key]))
        for key, value in cache_paths.items():
            if key in {"cache_root", "tool_cache", "output_cache"} or value is None:
                continue
            if isinstance(value, (str, Path)):
                ordered_paths.append(Path(value))
        return ordered_paths
    if isinstance(cache_paths, (str, Path)):
        return [Path(cache_paths)]
    return [Path(path) for path in cache_paths if path is not None]


def teardown_run_paths(*, workspace_path, cache_paths, lock_path=None, status: str) -> dict[str, object]:
    """Root-anchored cleanup for terminal statuses after child death is confirmed."""
    removed_paths: list[str] = []
    preserved_paths: list[str] = []

    if status not in _TERMINAL_STATUSES:
        return {
            "status": "TEARDOWN_SKIPPED_NON_TERMINAL",
            "terminal_status": status,
            "cleanup_allowed": False,
            "removed_paths": removed_paths,
            "preserved_paths": preserved_paths,
            "child_death_confirmed_by_status": False,
            **_non_authority_fields(),
        }

    cleanup_targets = [(Path(workspace_path), (_SPRINT_012_WORKSPACE_PREFIX,), False)]
    expected_run_id = _run_id_from_workspace_path(Path(workspace_path))
    cleanup_targets.extend(
        (candidate, (_SPRINT_012_CACHE_PREFIX,), False)
        for candidate in _cache_cleanup_candidates(cache_paths)
    )
    if lock_path is not None:
        cleanup_targets.append((Path(lock_path), (_SPRINT_012_LOCK_PREFIX,), True))

    seen: set[Path] = set()
    for candidate, prefixes, lock_file in cleanup_targets:
        normalized = candidate.expanduser().resolve(strict=False)
        if normalized in seen:
            continue
        seen.add(normalized)
        removed, resolved_path, _reason = _remove_guarded_teardown_path(
            candidate,
            allowed_prefixes=prefixes,
            lock_file=lock_file,
            expected_run_id=expected_run_id if lock_file else None,
        )
        if removed:
            removed_paths.append(resolved_path)
        else:
            preserved_paths.append(resolved_path)

    return {
        "status": "TEARDOWN_COMPLETED",
        "terminal_status": status,
        "cleanup_allowed": True,
        "removed_paths": removed_paths,
        "preserved_paths": preserved_paths,
        "child_death_confirmed_by_status": True,
        **_non_authority_fields(),
    }


def verify_primary_repo_manifest(source_root, manifest) -> dict[str, object]:
    """Verify source fixture manifest remains unchanged after probes."""
    current_manifest = manifest_source_tree(source_root)
    expected_files = manifest.get("files", []) if isinstance(manifest, dict) else []
    expected_hash = manifest.get("manifest_sha256") if isinstance(manifest, dict) else None
    current_files = current_manifest.get("files", [])
    current_hash = current_manifest.get("manifest_sha256")
    manifest_match = expected_files == current_files and expected_hash == current_hash
    expected_paths = {entry.get("path") for entry in expected_files if isinstance(entry, dict)}
    current_paths = {entry.get("path") for entry in current_files if isinstance(entry, dict)}
    return {
        "status": "PRIMARY_MANIFEST_UNCHANGED"
        if manifest_match
        else "PRIMARY_MANIFEST_CHANGED",
        "source_root": str(Path(source_root).expanduser().resolve(strict=False)),
        "manifest_match": manifest_match,
        "current_manifest": current_manifest,
        "added_paths": sorted(current_paths - expected_paths),
        "removed_paths": sorted(expected_paths - current_paths),
        "expected_manifest_sha256": expected_hash,
        "current_manifest_sha256": current_hash,
        **_non_authority_fields(),
    }
