"""BEB-L2 drop route for Kuronode Codex work through BLK-pipe.

The route is deliberately closed: the drop manifest selects an exact approved
BEB/L2 artifact pair and exact target commit, while BLK-System injects the Codex
engine and validation-profile execution surface. Caller manifests cannot name a
shell engine, validation commands, trace artifacts, or the L2 body directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable

from blk_pipe_adapter import BlkPipeAdapter


class RouteError(ValueError):
    """Raised when a BEB-L2 drop is unsafe or malformed before BLK-pipe dispatch."""


_ALLOWED_DROP_FIELDS = {
    "target_project",
    "beb_id",
    "l2_id",
    "beb_path",
    "beb_sha256",
    "l2_path",
    "l2_sha256",
    "work_dir",
    "target_branch",
    "target_hash",
    "allowed_modified_files",
    "allowed_new_files",
    "validation_profiles",
}
_FORBIDDEN_DROP_FIELDS = {
    "engine",
    "engine_args",
    "engine_command",
    "validation_commands",
    "l2_packet",
    "trace_artifacts",
}
_TRACE_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_GIT_HASH_RE = re.compile(r"^[0-9a-f]{40}$")
_BEB_ID_RE = re.compile(r"^BEB_[A-Za-z0-9_-]+$")
_L2_ID_RE = re.compile(r"^L2_[A-Za-z0-9_-]+$")
_ALLOWED_VALIDATION_PROFILES = {
    "go-test",
    "go-vet",
    "go-full",
    "python-unittest",
    "docs-doctrine-gates",
    "kuronode-power-of-ten-static-fixture",
    "kuronode-worktree-static",
}
_PROTECTED_ALLOWLIST_PREFIXES = ("docs/active/", "docs/requirements/", "docs/use_cases/")
_GLOB_CHARS = set("*?[")


def build_kuronode_codex_engine_args(
    *,
    model: str = "gpt-5.5",
    reasoning_effort: str = "high",
    beb_id: str | None = None,
    target_hash: str | None = None,
) -> list[str]:
    """Return the BLK-System-owned Codex argv for Kuronode BEB-L2 dispatch."""
    model = _required_string(model, "model")
    reasoning_effort = _required_string(reasoning_effort, "reasoning_effort")
    if model != "gpt-5.5":
        raise RouteError("codex model must be gpt-5.5 for the current route contract")
    if reasoning_effort != "high":
        raise RouteError("reasoning_effort must be high for the current route contract")
    final_message_artifact = "artifacts/codex/final-message.md"
    if beb_id is not None or target_hash is not None:
        final_message_artifact = str(_prepare_external_codex_final_message_artifact(beb_id, target_hash))
    return [
        "exec",
        "--sandbox",
        "workspace-write",
        "-",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--disable",
        "hooks",
        "--disable",
        "plugins",
        "--disable",
        "goals",
        "--model",
        model,
        "-c",
        f"model_reasoning_effort={reasoning_effort}",
        "--output-last-message",
        final_message_artifact,
    ]


def process_drop_file(
    drop_path: str | Path,
    *,
    adapter: Any | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> Any:
    """Validate one exact BEB-L2 drop and invoke BLK-pipe through the adapter."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    work_dir = _require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir")
    beb_path = _require_under_roots(Path(drop["beb_path"]), roots, "beb_path")
    l2_path = _require_under_roots(Path(drop["l2_path"]), roots, "l2_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)

    _assert_bound_ids(drop, beb_metadata, l2_packet)
    trace_artifacts = _parse_trace_artifacts(beb_metadata)

    report = _preflight_validated_drop(drop, work_dir, trace_artifacts)
    if report["status"] != "READY":
        codes = ", ".join(blocker["code"] for blocker in report["blockers"])
        raise RouteError(f"drop preflight blocked before BLK-pipe dispatch: {codes}")
    runner = adapter if adapter is not None else BlkPipeAdapter()
    return runner.execute_sprint(
        beb_id=drop["beb_id"],
        work_dir=work_dir,
        target_branch=drop["target_branch"],
        engine="codex",
        engine_args=build_kuronode_codex_engine_args(beb_id=drop["beb_id"], target_hash=drop["target_hash"]),
        l2_packet=l2_packet,
        validation_profiles=drop["validation_profiles"],
        allowed_modified_files=drop["allowed_modified_files"],
        allowed_new_files=drop["allowed_new_files"],
        trace_artifacts=trace_artifacts,
        target_hash=drop["target_hash"],
    )


def preflight_drop_file(
    drop_path: str | Path,
    *,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> dict[str, Any]:
    """Validate one exact BEB-L2 drop and inspect repo readiness without running Codex."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    work_dir = _require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir")
    beb_path = _require_under_roots(Path(drop["beb_path"]), roots, "beb_path")
    l2_path = _require_under_roots(Path(drop["l2_path"]), roots, "l2_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)

    _assert_bound_ids(drop, beb_metadata, l2_packet)
    trace_artifacts = _parse_trace_artifacts(beb_metadata)
    return _preflight_validated_drop(drop, work_dir, trace_artifacts)


def build_ignored_residue_cleanup_plan(
    drop_path: str | Path,
    *,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> dict[str, Any]:
    """Return non-mutating cleanup evidence for ignored residue that blocks BEB-L2 dispatch."""
    report = preflight_drop_file(
        drop_path,
        allowed_work_dirs=allowed_work_dirs,
        trusted_roots=trusted_roots,
        approved_drop_sha256=approved_drop_sha256,
    )
    blockers = list(report["blockers"])
    ignored_blockers = [blocker for blocker in blockers if blocker["code"] == "PREEXISTING_IGNORED_OR_UNTRACKED"]
    non_cleanup_blockers = [blocker for blocker in blockers if blocker["code"] != "PREEXISTING_IGNORED_OR_UNTRACKED"]
    dry_run_command = ["git", "clean", "-ndX"]
    plan = {
        "status": "NO_CLEANUP_REQUIRED",
        "beb_id": report["beb_id"],
        "l2_id": report["l2_id"],
        "work_dir": report["work_dir"],
        "target_branch": report["target_branch"],
        "target_hash": report["target_hash"],
        "cleanup_authorized": False,
        "mutation_performed": False,
        "dispatch_authorized": False,
        "dry_run_command": dry_run_command,
        "ignored_residue_paths": sorted({path for blocker in ignored_blockers for path in blocker["paths"]}),
        "dry_run_paths": [],
        "blockers": blockers,
    }
    if non_cleanup_blockers:
        plan["status"] = "BLOCKED_BY_NON_CLEANUP_PREFLIGHT"
        plan["dry_run_command"] = []
        return plan
    if ignored_blockers:
        dry_run_paths = _git_clean_dry_run_paths(Path(report["work_dir"]))
        plan["status"] = "CLEANUP_REQUIRED"
        plan["dry_run_paths"] = dry_run_paths
    return plan


def build_clean_worktree_drop_manifest(
    drop_path: str | Path,
    *,
    clean_work_dir: str | Path,
    clean_worktree_roots: Iterable[str | Path] | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256: str | None = None,
) -> dict[str, Any]:
    """Retarget one approved drop to a clean worktree candidate without creating or dispatching it."""
    allowed_dirs = _required_resolved_roots(allowed_work_dirs, "allowed_work_dirs")
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    clean_roots = _required_resolved_roots(clean_worktree_roots, "clean_worktree_roots")
    approved_hash = _required_sha256(approved_drop_sha256, "approved_drop_sha256")
    drop_file = _require_under_roots(Path(drop_path), roots, "drop_path")
    drop = _load_drop_manifest(drop_file)
    _assert_file_sha256(drop_file, approved_hash, "drop_path")

    source_work_dir = Path(_require_exact_resolved_path(drop["work_dir"], allowed_dirs, "work_dir"))
    clean_dir = _require_under_roots(Path(clean_work_dir), clean_roots, "clean_work_dir")
    if clean_dir == source_work_dir or source_work_dir in clean_dir.parents:
        raise RouteError("clean_work_dir must not be the source work_dir or inside it")

    beb_path = _require_under_roots(Path(drop["beb_path"]), roots, "beb_path")
    l2_path = _require_under_roots(Path(drop["l2_path"]), roots, "l2_path")
    beb_text = _read_verified_text_file(beb_path, drop["beb_sha256"], "beb_path")
    l2_packet = _read_verified_text_file(l2_path, drop["l2_sha256"], "l2_path")
    beb_metadata = _parse_beb_frontmatter(beb_text)
    _assert_bound_ids(drop, beb_metadata, l2_packet)
    _parse_trace_artifacts(beb_metadata)

    clean_manifest = dict(drop)
    clean_manifest["work_dir"] = str(clean_dir)
    return {
        "status": "CLEAN_WORKTREE_MANIFEST_READY",
        "beb_id": drop["beb_id"],
        "l2_id": drop["l2_id"],
        "source_work_dir": str(source_work_dir),
        "clean_work_dir": str(clean_dir),
        "target_branch": drop["target_branch"],
        "target_hash": drop["target_hash"],
        "drop_manifest": clean_manifest,
        "drop_manifest_sha256": _json_sha256(clean_manifest),
        "manifest_approval_required": True,
        "worktree_creation_authorized": False,
        "source_mutation_authorized": False,
        "dispatch_authorized": False,
    }


def dispatch_inbox_once(
    inbox_dir: str | Path,
    processed_dir: str | Path,
    failed_dir: str | Path,
    *,
    adapter: Any | None = None,
    allowed_work_dirs: Iterable[str | Path] | None = None,
    trusted_roots: Iterable[str | Path] | None = None,
    approved_drop_sha256s: Iterable[str] | None = None,
) -> Any:
    """Process the first sorted `*.json` drop from an inbox directory."""
    roots = _required_resolved_roots(trusted_roots, "trusted_roots")
    approved_hashes = _required_approved_hashes(approved_drop_sha256s)
    inbox = _require_under_roots(Path(inbox_dir), roots, "inbox_dir")
    drops = sorted(inbox.glob("*.json"))
    if not drops:
        return {"status": "NOOP", "processed": 0}

    drop_path = drops[0]
    try:
        approved_hash = _file_sha256(drop_path)
        if approved_hash not in approved_hashes:
            raise RouteError("drop_path sha256 is not in trusted approved_drop_sha256s")
        report = process_drop_file(
            drop_path,
            adapter=adapter,
            allowed_work_dirs=allowed_work_dirs,
            trusted_roots=trusted_roots,
            approved_drop_sha256=approved_hash,
        )
    except Exception as exc:
        failed = Path(failed_dir)
        failed.mkdir(parents=True, exist_ok=True)
        destination = failed / drop_path.name
        shutil.move(str(drop_path), destination)
        (failed / f"{drop_path.name}.error.txt").write_text(f"{type(exc).__name__}: {exc}\n")
        raise

    processed = Path(processed_dir)
    processed.mkdir(parents=True, exist_ok=True)
    shutil.move(str(drop_path), processed / drop_path.name)
    return report


def _preflight_validated_drop(drop: dict[str, Any], work_dir: str, trace_artifacts: list[dict[str, str]]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    repo = Path(work_dir)
    head = _git_output(repo, ["rev-parse", "HEAD"])
    branch = _git_output(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    if head is None:
        blockers.append({"code": "GIT_HEAD_UNAVAILABLE", "message": "work_dir is not a readable Git repository", "paths": []})
    elif head != drop["target_hash"]:
        blockers.append({
            "code": "TARGET_HEAD_MISMATCH",
            "message": "current HEAD does not match target_hash",
            "paths": [],
            "actual": head,
            "expected": drop["target_hash"],
        })
    if branch is not None and branch != drop["target_branch"]:
        blockers.append({
            "code": "TARGET_BRANCH_MISMATCH",
            "message": "current branch does not match target_branch",
            "paths": [],
            "actual": branch,
            "expected": drop["target_branch"],
        })

    dirty_paths = _git_status_paths(repo, ["status", "--porcelain=v1", "--untracked-files=all"])
    if dirty_paths:
        blockers.append({
            "code": "GIT_DIRTY",
            "message": "tracked or untracked worktree changes exist before Codex dispatch",
            "paths": dirty_paths,
        })
    ignored_paths = _git_status_paths(repo, ["status", "--porcelain=v1", "--ignored=matching", "--untracked-files=all"], prefix="!!")
    if ignored_paths:
        blockers.append({
            "code": "PREEXISTING_IGNORED_OR_UNTRACKED",
            "message": "ignored residue exists and would make BLK-pipe cleanup destructive or noisy",
            "paths": ignored_paths,
        })

    return {
        "status": "BLOCKED" if blockers else "READY",
        "beb_id": drop["beb_id"],
        "l2_id": drop["l2_id"],
        "work_dir": work_dir,
        "target_branch": drop["target_branch"],
        "target_hash": drop["target_hash"],
        "allowed_modified_files": list(drop["allowed_modified_files"]),
        "allowed_new_files": list(drop["allowed_new_files"]),
        "validation_profiles": list(drop["validation_profiles"]),
        "trace_artifacts": list(trace_artifacts),
        "blockers": blockers,
    }


def _git_output(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _git_status_paths(repo: Path, args: list[str], prefix: str | None = None) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        if prefix is not None and not line.startswith(prefix):
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return sorted(set(paths))


def _git_clean_dry_run_paths(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "clean", "-ndX"],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    prefix = "Would remove "
    paths = []
    for line in result.stdout.splitlines():
        if line.startswith(prefix):
            paths.append(line[len(prefix) :].strip())
    return sorted(set(paths))


def _load_drop_manifest(drop_path: Path) -> dict[str, Any]:
    if not drop_path.is_file():
        raise RouteError(f"drop_path is not a file: {drop_path}")
    try:
        data = json.loads(drop_path.read_text())
    except json.JSONDecodeError as exc:
        raise RouteError(f"drop manifest is not valid JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise RouteError("drop manifest must be a JSON object")

    forbidden = sorted(field for field in data if field in _FORBIDDEN_DROP_FIELDS)
    if forbidden:
        raise RouteError(f"drop manifest cannot supply caller-controlled fields: {', '.join(forbidden)}")
    unknown = sorted(set(data) - _ALLOWED_DROP_FIELDS)
    if unknown:
        raise RouteError(f"drop manifest contains unsupported fields: {', '.join(unknown)}")

    missing = [field for field in sorted(_ALLOWED_DROP_FIELDS) if field not in data]
    if missing:
        raise RouteError(f"drop manifest missing required fields: {', '.join(missing)}")

    target_project = _required_string(data["target_project"], "target_project")
    if target_project != "kuronode":
        raise RouteError("target_project must equal kuronode")

    return {
        "target_project": target_project,
        "beb_id": _required_pattern(data["beb_id"], "beb_id", _BEB_ID_RE),
        "l2_id": _required_pattern(data["l2_id"], "l2_id", _L2_ID_RE),
        "beb_path": _required_absolute_path(data["beb_path"], "beb_path"),
        "beb_sha256": _required_sha256(data["beb_sha256"], "beb_sha256"),
        "l2_path": _required_absolute_path(data["l2_path"], "l2_path"),
        "l2_sha256": _required_sha256(data["l2_sha256"], "l2_sha256"),
        "work_dir": _required_absolute_path(data["work_dir"], "work_dir"),
        "target_branch": _required_string(data["target_branch"], "target_branch"),
        "target_hash": _required_pattern(data["target_hash"], "target_hash", _GIT_HASH_RE),
        "allowed_modified_files": _required_path_list(data["allowed_modified_files"], "allowed_modified_files"),
        "allowed_new_files": _required_path_list(data["allowed_new_files"], "allowed_new_files"),
        "validation_profiles": _required_validation_profiles(data["validation_profiles"]),
    }


def _required_resolved_roots(paths: Iterable[str | Path] | None, field_name: str) -> tuple[Path, ...]:
    if paths is None:
        raise RouteError(f"{field_name} must be supplied by trusted configuration")
    roots = tuple(Path(path).expanduser().resolve() for path in paths)
    if not roots:
        raise RouteError(f"{field_name} must not be empty")
    return roots


def _required_approved_hashes(hashes: Iterable[str] | None) -> set[str]:
    if hashes is None:
        raise RouteError("approved_drop_sha256s must be supplied by trusted configuration")
    approved = {_required_sha256(value, "approved_drop_sha256s[]") for value in hashes}
    if not approved:
        raise RouteError("approved_drop_sha256s must not be empty")
    return approved


def _file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _prepare_external_codex_final_message_artifact(beb_id: str | None, target_hash: str | None) -> Path:
    safe_beb_id = _required_pattern(beb_id, "beb_id", _BEB_ID_RE)
    safe_target_hash = _required_pattern(target_hash, "target_hash", _GIT_HASH_RE)
    artifact_root = Path("/tmp/blk-system-beb-l2-codex")
    artifact_dir = artifact_root / safe_beb_id / safe_target_hash[:12]
    _prepare_private_external_artifact_dir(artifact_root, artifact_dir)
    final_message = artifact_dir / "final-message.md"
    if final_message.is_symlink():
        raise RouteError("Codex final-message artifact path must not be a symlink")
    if final_message.exists():
        final_message.unlink()
    return final_message


def _prepare_private_external_artifact_dir(artifact_root: Path, artifact_dir: Path) -> None:
    _reject_symlinked_components(artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    _reject_symlinked_components(artifact_dir)
    try:
        artifact_root.chmod(0o700)
        artifact_dir.parent.chmod(0o700)
        artifact_dir.chmod(0o700)
    except PermissionError as exc:
        raise RouteError("Codex final-message artifact path must be private to the current user") from exc
    root_real = artifact_root.resolve(strict=True)
    dir_real = artifact_dir.resolve(strict=True)
    if dir_real != root_real and root_real not in dir_real.parents:
        raise RouteError("Codex final-message artifact path must remain under the external artifact root")


def _reject_symlinked_components(path: Path) -> None:
    current = Path(path.anchor or "/")
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise RouteError("Codex final-message artifact path must not contain symlinked components")


def _json_sha256(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _assert_file_sha256(path: Path, expected_sha256: str, field_name: str) -> None:
    actual = _file_sha256(path)
    if actual != expected_sha256:
        raise RouteError(f"{field_name} sha256 does not match trusted configuration")


def _require_under_roots(path: Path, roots: tuple[Path, ...], field_name: str) -> Path:
    resolved = path.expanduser().resolve()
    if not any(resolved == root or root in resolved.parents for root in roots):
        raise RouteError(f"{field_name} must be under a trusted root")
    return resolved


def _require_exact_resolved_path(path: str, allowed: tuple[Path, ...], field_name: str) -> str:
    resolved = Path(path).expanduser().resolve()
    if resolved not in allowed:
        raise RouteError(f"{field_name} must match an approved Kuronode work_dir")
    return str(resolved)


def _read_verified_text_file(path: Path, expected_sha256: str, field_name: str) -> str:
    if not path.is_file():
        raise RouteError(f"{field_name} does not point to a file")
    data = path.read_bytes()
    actual = "sha256:" + hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        raise RouteError(f"{field_name} sha256 does not match manifest")
    return data.decode()


def _parse_beb_frontmatter(text: str) -> list[str]:
    if not text.startswith("---\n"):
        raise RouteError("BEB file missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise RouteError("BEB file missing closing frontmatter fence")
    return text[4:end].splitlines()


def _frontmatter_scalar(lines: list[str], key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*\"([^\"]+)\"\s*$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1)
    raise RouteError(f"BEB frontmatter missing {key}")


def _assert_bound_ids(drop: dict[str, Any], beb_metadata: list[str], l2_packet: str) -> None:
    beb_id = _frontmatter_scalar(beb_metadata, "beb_id")
    l2_id = _frontmatter_scalar(beb_metadata, "l2_id")
    if drop["beb_id"] != beb_id:
        raise RouteError("drop beb_id does not match BEB frontmatter")
    if drop["l2_id"] != l2_id:
        raise RouteError("drop l2_id does not match BEB frontmatter")
    if f"BEB_ID: {beb_id}" not in l2_packet:
        raise RouteError("L2 packet does not bind to BEB identity")
    if f"L2_ID: {l2_id}" not in l2_packet:
        raise RouteError("L2 packet does not bind to L2 identity")


def _parse_trace_artifacts(lines: list[str]) -> list[dict[str, str]]:
    try:
        index = lines.index("trace_artifacts:") + 1
    except ValueError as exc:
        raise RouteError("BEB frontmatter missing trace_artifacts") from exc

    artifacts: list[dict[str, str]] = []
    while index < len(lines):
        line = lines[index]
        if line and not line.startswith("  "):
            break
        match = re.match(r"^\s{2}-\s+kind:\s*\"([^\"]+)\"\s*$", line)
        if not match:
            index += 1
            continue
        artifact = {"kind": match.group(1)}
        for next_line in lines[index + 1 : index + 3]:
            scalar = re.match(r"^\s{4}(id|version_hash):\s*\"([^\"]+)\"\s*$", next_line)
            if scalar:
                artifact[scalar.group(1)] = scalar.group(2)
        if set(artifact) != {"kind", "id", "version_hash"}:
            raise RouteError("BEB trace_artifacts entry is incomplete")
        if not _TRACE_HASH_RE.match(artifact["version_hash"]):
            raise RouteError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        artifacts.append(artifact)
        index += 3

    if not artifacts:
        raise RouteError("BEB frontmatter missing trace_artifacts entries")
    return artifacts


def _required_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RouteError(f"{field_name} must be a non-empty string")
    return value.strip()


def _required_pattern(value: Any, field_name: str, pattern: re.Pattern[str]) -> str:
    text = _required_string(value, field_name)
    if not pattern.match(text):
        raise RouteError(f"{field_name} has invalid format")
    return text


def _required_sha256(value: Any, field_name: str) -> str:
    return _required_pattern(value, field_name, _TRACE_HASH_RE)


def _required_absolute_path(value: Any, field_name: str) -> str:
    text = _required_string(value, field_name)
    if not Path(text).is_absolute():
        raise RouteError(f"{field_name} must be absolute")
    return text


def _required_validation_profiles(value: Any) -> list[str]:
    profiles = _required_string_list(value, "validation_profiles")
    unknown = sorted(set(profiles) - _ALLOWED_VALIDATION_PROFILES)
    if unknown:
        raise RouteError(f"validation_profiles contain unsupported profiles: {', '.join(unknown)}")
    return profiles


def _required_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise RouteError(f"{field_name} must be a non-empty list")
    return [_required_string(item, f"{field_name}[]") for item in value]


def _required_path_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise RouteError(f"{field_name} must be a list")
    paths: list[str] = []
    for item in value:
        raw_path = _required_string(item, f"{field_name}[]")
        path = raw_path.replace("\\", "/")
        if path.startswith("/"):
            raise RouteError(f"{field_name} entries must be relative")
        parts = [part for part in path.split("/") if part]
        if ".." in parts:
            raise RouteError(f"{field_name} entries must not contain path traversal")
        normalized = "/".join(parts)
        if normalized in {"", "."} or normalized.startswith(":") or any(char in normalized for char in _GLOB_CHARS):
            raise RouteError(f"{field_name} entries must be explicit relative files")
        if any(normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in _PROTECTED_ALLOWLIST_PREFIXES):
            raise RouteError(f"{field_name} entries must not target protected BLK-req paths")
        paths.append(normalized)
    return paths


def _jsonable_report(report: Any) -> Any:
    if is_dataclass(report):
        return asdict(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dispatch BEB-L2 drops through BLK-pipe/Codex")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--drop", help="absolute path to one drop manifest JSON")
    group.add_argument("--inbox", help="directory containing queued *.json drop manifests")
    parser.add_argument("--processed-dir", default=".blk-pipe/processed")
    parser.add_argument("--failed-dir", default=".blk-pipe/failed")
    parser.add_argument("--allowed-work-dir", action="append", required=True)
    parser.add_argument("--trusted-root", action="append", required=True)
    parser.add_argument("--approved-drop-sha256", action="append", required=True)
    parser.add_argument("--preflight", action="store_true", help="validate one --drop and inspect repo readiness without invoking BLK-pipe")
    parser.add_argument("--cleanup-plan", action="store_true", help="emit non-mutating ignored-residue cleanup evidence for one --drop")
    parser.add_argument("--clean-worktree-manifest", action="store_true", help="emit a retargeted drop manifest for a trusted clean worktree without dispatch")
    parser.add_argument("--clean-work-dir", help="absolute path to the clean worktree candidate for --clean-worktree-manifest")
    parser.add_argument("--clean-worktree-root", action="append", help="trusted root for clean worktree candidates")
    args = parser.parse_args(argv)

    planning_modes = [args.preflight, args.cleanup_plan, args.clean_worktree_manifest]
    if sum(1 for enabled in planning_modes if enabled) > 1:
        raise RouteError("--preflight, --cleanup-plan, and --clean-worktree-manifest are mutually exclusive")
    if any(planning_modes) and not args.drop:
        raise RouteError("--preflight/--cleanup-plan/--clean-worktree-manifest require --drop")
    if args.clean_worktree_manifest and (not args.clean_work_dir or not args.clean_worktree_root):
        raise RouteError("--clean-worktree-manifest requires --clean-work-dir and --clean-worktree-root")
    if not args.clean_worktree_manifest and (args.clean_work_dir or args.clean_worktree_root):
        raise RouteError("--clean-work-dir/--clean-worktree-root require --clean-worktree-manifest")

    if args.drop:
        if len(args.approved_drop_sha256) != 1:
            raise RouteError("--drop requires exactly one --approved-drop-sha256")
        if args.clean_worktree_manifest:
            report = build_clean_worktree_drop_manifest(
                args.drop,
                clean_work_dir=args.clean_work_dir,
                clean_worktree_roots=args.clean_worktree_root,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
        elif args.cleanup_plan:
            report = build_ignored_residue_cleanup_plan(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
        elif args.preflight:
            report = preflight_drop_file(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
        else:
            report = process_drop_file(
                args.drop,
                allowed_work_dirs=args.allowed_work_dir,
                trusted_roots=args.trusted_root,
                approved_drop_sha256=args.approved_drop_sha256[0],
            )
    else:
        report = dispatch_inbox_once(
            args.inbox,
            args.processed_dir,
            args.failed_dir,
            allowed_work_dirs=args.allowed_work_dir,
            trusted_roots=args.trusted_root,
            approved_drop_sha256s=args.approved_drop_sha256,
        )
    print(json.dumps(_jsonable_report(report), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
