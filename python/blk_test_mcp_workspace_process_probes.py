from pathlib import Path, PurePosixPath
import re

_PROTECTED_PREFIXES = ("docs/active", "docs/requirements", "docs/use_cases")
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
