"""Advisory health-check runner for BLK-SYSTEM-032/033.

The runner executes only repository-owned fixed profiles and returns bounded
advisory evidence. It is not a general command runner.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

RUNNER_STATUS = "HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY"
EXECUTION_STATUS = "HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE"
PASS_STATUS = "PASS_ADVISORY_ONLY"
FAIL_STATUS = "FAIL_ADVISORY_ONLY"
BLOCKED_STATUS = "BLOCKED_ADVISORY_ONLY"
REPO_ROOT = Path(__file__).resolve().parents[1]
TRUSTED_PATH = f"{Path.home() / '.local' / 'bin'}:{Path.home() / '.local' / 'opt' / 'go' / 'bin'}:/usr/bin:/bin"
DEFAULT_OUTPUT_BYTE_LIMIT = 64 * 1024
SOURCE_WORKSPACE_MODE = "source_repo"
ISOLATED_WORKSPACE_MODE = "isolated_copy"
_WORKSPACE_MODES = {SOURCE_WORKSPACE_MODE, ISOLATED_WORKSPACE_MODE}
ISOLATED_COPY_EXCLUDES = [".git", "docs/active", "docs/requirements", "docs/use_cases"]
_ISOLATED_COPY_EXCLUDED_DIRS = set(ISOLATED_COPY_EXCLUDES) | {".pytest_cache"}


@dataclass(frozen=True)
class HealthCheckProfile:
    profile_id: str
    argv: Sequence[str]
    classification: str
    timeout_seconds: int


@dataclass(frozen=True)
class ProcessOutcome:
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    output_limit_exceeded: bool = False
    startup_failed: bool = False
    timeout_cleanup: str = "PROCESS_GROUP_KILL_NOT_NEEDED"


def _trusted_executable(name: str) -> str:
    resolved = shutil.which(name, path=TRUSTED_PATH)
    if not resolved:
        raise RuntimeError(f"trusted executable not found: {name}")
    canonical = Path(resolved).resolve()
    if not _under_trusted_root(canonical):
        raise ValueError(f"trusted executable escaped approved roots: {name}")
    return str(canonical)


def _under_trusted_root(path: Path) -> bool:
    trusted_roots = [Path(part).resolve() for part in TRUSTED_PATH.split(":") if part]
    for root in trusted_roots:
        if path == root or root in path.parents:
            return True
    return False


def _path_inside(child: Path, parent: Path) -> bool:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()
    return child_resolved == parent_resolved or parent_resolved in child_resolved.parents


def _safe_temp_parent() -> Path:
    candidates = [Path(tempfile.gettempdir()), Path("/var/tmp"), Path("/tmp")]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists() and resolved.is_dir() and not _path_inside(resolved, REPO_ROOT):
            return resolved
    raise RuntimeError("no runner temp parent outside repository")


PROFILES: dict[str, HealthCheckProfile] = {
    "git_status_short_branch": HealthCheckProfile(
        "git_status_short_branch",
        (_trusted_executable("git"), "status", "--short", "--branch"),
        "ADVISORY_ONLY",
        10,
    ),
    "active_doctrine_gate": HealthCheckProfile(
        "active_doctrine_gate",
        (_trusted_executable("python3"), "-m", "unittest", "python.test_active_doctrine_review_gates"),
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        120,
    ),
    "python_unittest_discovery": HealthCheckProfile(
        "python_unittest_discovery",
        (_trusted_executable("python3"), "-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"),
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        180,
    ),
    "go_test_all": HealthCheckProfile(
        "go_test_all",
        (_trusted_executable("go"), "test", "./..."),
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        180,
    ),
    "go_vet_all": HealthCheckProfile(
        "go_vet_all",
        (_trusted_executable("go"), "vet", "./..."),
        "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
        180,
    ),
}

_FORBIDDEN_EXECUTABLES = {
    "bash",
    "sh",
    "zsh",
    "fish",
    "pwsh",
    "powershell",
    "cmd",
    "curl",
    "wget",
    "ssh",
    "scp",
    "nc",
    "ncat",
    "telnet",
    "npm",
    "pip",
    "pip3",
    "uv",
}
_FORBIDDEN_INLINE_FLAGS = {"-c", "-e"}
_GIT_MUTATIONS = {
    "commit",
    "push",
    "reset",
    "checkout",
    "stash",
    "clean",
    "revert",
    "merge",
    "rebase",
    "switch",
    "restore",
    "add",
}
_FORBIDDEN_ARG_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"docs/active",
        r"protected[-_/ ]?vault",
        r"protected[-_/ ]?body",
        r"requirement[-_/ ]?body",
        r"use[-_/ ]?case[-_/ ]?body",
        r"active[-_/ ]?vault",
        r"generate[_-]?rtm",
        r"\brtm\b",
        r"publish[_-]?authoritative[_-]?beo",
        r"\bbeo\b",
        r"drift[_-]?decision",
        r"reject[_-]?drift",
        r"\bdrift\b",
        r"coverage[_-]?matrix",
        r"\bsigner\b",
        r"\bledger\b",
        r"\bstorage\b",
        r"https?://",
        r"\b(alias|wrapper)\b",
    ]
]
_SECRET_PATTERNS = [
    re.compile(r"(GITHUB_TOKEN\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(API[_-]?KEY\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(AWS_ACCESS_KEY_ID\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(SECRET\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(TOKEN\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(PASSWORD\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(PASSPHRASE\s*[=:]\s*)\S+", re.IGNORECASE),
    re.compile(r"(Authorization:\s*(?:Bearer|Basic)\s+)\S+", re.IGNORECASE),
    re.compile(r"SSH_AUTH_SOCK\s*[=:]\s*\S+", re.IGNORECASE),
    re.compile(r"\.env\b", re.IGNORECASE),
]
_SECRET_ENV_TOKENS = (
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "PASSWD",
    "PASSPHRASE",
    "API_KEY",
    "APIKEY",
    "ACCESS_KEY",
    "PRIVATE_KEY",
    "AUTH",
    "SSH_AUTH_SOCK",
    "ASKPASS",
)


def validate_profile_registry(registry: Mapping[str, HealthCheckProfile]) -> None:
    default_argvs = {tuple(p.argv) for p in PROFILES.values()}
    for key, profile in registry.items():
        if key != profile.profile_id:
            raise ValueError("profile key must match profile_id")
        if not isinstance(profile.profile_id, str) or not re.fullmatch(r"[a-z0-9_]+", profile.profile_id):
            raise ValueError("invalid profile_id")
        argv = _validated_argv(profile.argv)
        if tuple(argv) not in default_argvs and registry is not PROFILES:
            raise ValueError("profile argv is not an authorized BLK-SYSTEM-033 fixed profile")
        if profile.classification not in {"ADVISORY_ONLY", "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"}:
            raise ValueError("unsupported profile classification")
        if not isinstance(profile.timeout_seconds, int) or not (1 <= profile.timeout_seconds <= 300):
            raise ValueError("invalid profile timeout")


def run_health_check(
    profile_id: str,
    *,
    repo_root: Path | str,
    excerpt_max_chars: int = 1000,
    output_byte_limit: int = DEFAULT_OUTPUT_BYTE_LIMIT,
    workspace_mode: str = SOURCE_WORKSPACE_MODE,
) -> dict[str, object]:
    if not isinstance(profile_id, str) or not re.fullmatch(r"[a-z0-9_]+", profile_id):
        raise ValueError("profile_id must name a fixed BLK-SYSTEM-033 profile")
    if profile_id not in PROFILES:
        raise ValueError("unknown health-check profile")
    if not isinstance(excerpt_max_chars, int) or not (32 <= excerpt_max_chars <= 4000):
        raise ValueError("excerpt_max_chars must be between 32 and 4000")
    if not isinstance(output_byte_limit, int) or not (1024 <= output_byte_limit <= 1024 * 1024):
        raise ValueError("output_byte_limit must be between 1024 and 1048576 bytes")
    if workspace_mode not in _WORKSPACE_MODES:
        raise ValueError("workspace_mode must be source_repo or isolated_copy")
    if workspace_mode == ISOLATED_WORKSPACE_MODE and profile_id == "git_status_short_branch":
        raise ValueError("git_status_short_branch is source-repository mode only")

    profile = PROFILES[profile_id]
    argv = _validated_argv(profile.argv)
    source_repo_path = _validated_repo_root(repo_root)
    runner_temp_path = Path(tempfile.mkdtemp(prefix="blk-system-health-check-", dir=str(_safe_temp_parent()))).resolve()
    isolated_workspace_path = None
    cleanup_error = None
    try:
        execution_path = source_repo_path
        if workspace_mode == ISOLATED_WORKSPACE_MODE:
            isolated_workspace_path = runner_temp_path / "isolated-workspace"
            _copy_isolated_workspace(source_repo_path, isolated_workspace_path)
            execution_path = isolated_workspace_path.resolve()
        cwd = str(execution_path)
        env = _scrubbed_environment(runner_temp_path, execution_path)
        source_before = _git_status_snapshot(str(source_repo_path), env)
        cache_before = _repo_cache_snapshot(source_repo_path)

        outcome = _run_fixed_process(
            argv,
            cwd=cwd,
            env=env,
            timeout_seconds=profile.timeout_seconds,
            output_byte_limit=output_byte_limit,
        )
        exit_code = outcome.exit_code
        stdout = outcome.stdout
        stderr = outcome.stderr
        source_after = _git_status_snapshot(str(source_repo_path), env)
        cache_after = _repo_cache_snapshot(source_repo_path)
        source_repo_status_changed = source_before != source_after
        source_repo_cache_artifacts_changed = cache_before != cache_after
        process_group_timeout_cleanup = outcome.timeout_cleanup
        if outcome.startup_failed:
            status = BLOCKED_STATUS
            exit_code = None
            stderr = f"subprocess startup failed for profile {profile_id}; {stderr}"
        elif outcome.timed_out:
            status = BLOCKED_STATUS
            exit_code = None
            stderr = f"profile {profile_id} timed out after {profile.timeout_seconds}s; {stderr}"
        elif outcome.output_limit_exceeded:
            status = BLOCKED_STATUS
            exit_code = None
            stderr = f"output limit exceeded for profile {profile_id}; {stderr}"
        elif source_repo_status_changed:
            status = BLOCKED_STATUS
            exit_code = None
            if workspace_mode == ISOLATED_WORKSPACE_MODE:
                stderr = f"source repository changed during isolated health-check profile {profile_id}; {stderr}"
            else:
                stderr = f"workspace changed during health-check profile {profile_id}; {stderr}"
        elif source_repo_cache_artifacts_changed:
            status = BLOCKED_STATUS
            exit_code = None
            if workspace_mode == ISOLATED_WORKSPACE_MODE:
                stderr = f"source repository cache artifacts changed during isolated health-check profile {profile_id}; {stderr}"
            else:
                stderr = f"repo-local cache artifacts changed during health-check profile {profile_id}; {stderr}"
        else:
            status = PASS_STATUS if exit_code == 0 else FAIL_STATUS

        clean_stdout, redacted_stdout = _redact(stdout)
        clean_stderr, redacted_stderr = _redact(stderr)
        stdout_excerpt = _bounded(clean_stdout, excerpt_max_chars)
        stderr_excerpt = _bounded(clean_stderr, excerpt_max_chars)
        evidence_hash = _evidence_hash(profile_id, argv, exit_code, clean_stdout, clean_stderr, status)
        result = {
            "runner_status": RUNNER_STATUS,
            "execution_status": EXECUTION_STATUS,
            "profile_id": profile_id,
            "classification": profile.classification,
            "argv": argv,
            "cwd": cwd,
            "status": status,
            "exit_code": exit_code,
            "stdout_excerpt": stdout_excerpt,
            "stderr_excerpt": stderr_excerpt,
            "evidence_hash": evidence_hash,
            "raw_output_embedded": False,
            "redaction_applied": bool(
                redacted_stdout
                or redacted_stderr
                or len(clean_stdout) > excerpt_max_chars
                or len(clean_stderr) > excerpt_max_chars
                or outcome.output_limit_exceeded
            ),
            "health_check_pass_grants_authority": False,
            "shell_used": False,
            "command_executed": True,
            "subprocess_started": True,
            "workspace_mode": workspace_mode,
            "execution_workspace": (
                "ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO"
                if workspace_mode == ISOLATED_WORKSPACE_MODE
                else "SOURCE_REPOSITORY"
            ),
            "source_repo_is_execution_cwd": execution_path.resolve() == source_repo_path.resolve(),
            "isolated_workspace_path_inside_repo": (
                False if isolated_workspace_path is None else _path_inside(isolated_workspace_path, source_repo_path)
            ),
            "isolated_workspace_copy_excludes": list(ISOLATED_COPY_EXCLUDES),
            "side_effect_observation_scope": (
                "SOURCE_STATUS_AND_CACHE_PLUS_ISOLATED_WORKSPACE_COPY_ONLY"
                if workspace_mode == ISOLATED_WORKSPACE_MODE
                else "GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY"
            ),
            "workspace_status_changed": source_repo_status_changed,
            "repo_cache_artifacts_changed": source_repo_cache_artifacts_changed,
            "source_repo_status_changed": source_repo_status_changed,
            "source_repo_cache_artifacts_changed": source_repo_cache_artifacts_changed,
            "repo_cache_artifacts": (
                "REPO_CACHE_ARTIFACT_CHANGE_OBSERVED"
                if source_repo_cache_artifacts_changed
                else "NO_REPO_CACHE_ARTIFACT_CHANGE_OBSERVED"
            ),
            "runner_temp_containment": "RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO",
            "runner_temp_path_inside_repo": _path_inside(runner_temp_path, source_repo_path),
            "process_group_timeout_cleanup": process_group_timeout_cleanup,
            "network_called": "NOT_MEASURED_BY_PILOT",
            "package_manager_called": "NOT_MEASURED_BY_PILOT",
            "git_mutated": "WORKSPACE_STATUS_CHANGED" if source_repo_status_changed else "NO_WORKSPACE_STATUS_CHANGE_OBSERVED",
            "source_mutated": "WORKSPACE_STATUS_CHANGED" if source_repo_status_changed else "NOT_MEASURED_BY_PILOT",
            "approval_captured": False,
            "protected_body_read": "NOT_MEASURED_BY_PILOT",
            "active_vault_scanned": "NOT_MEASURED_BY_PILOT",
            "beo_published": "NOT_MEASURED_BY_PILOT",
            "rtm_generated": "NOT_MEASURED_BY_PILOT",
            "drift_decision_made": "NOT_MEASURED_BY_PILOT",
            "production_sandbox_enforced": "NOT_ENFORCED_BY_PILOT",
            "network_firewall_enforced": "NOT_ENFORCED_BY_PILOT",
            "host_secret_isolation_enforced": "NOT_ENFORCED_BY_PILOT",
            "production_authority_granted": False,
        }
    finally:
        try:
            if runner_temp_path.exists():
                shutil.rmtree(runner_temp_path)
        except OSError as exc:
            cleanup_error = str(exc)
    result["runner_temp_removed"] = bool(runner_temp_path and not runner_temp_path.exists())
    result["isolated_workspace_removed"] = bool(
        isolated_workspace_path is None or not isolated_workspace_path.exists()
    )
    if cleanup_error:
        result["status"] = BLOCKED_STATUS
        result["exit_code"] = None
        result["stderr_excerpt"] = _bounded(
            f"cleanup failed for health-check profile {profile_id}: {cleanup_error}; {result['stderr_excerpt']}",
            excerpt_max_chars,
        )
        result["evidence_hash"] = _evidence_hash(
            profile_id,
            argv,
            result["exit_code"],
            str(result["stdout_excerpt"]),
            str(result["stderr_excerpt"]),
            str(result["status"]),
        )
    if not result["runner_temp_removed"] and result["status"] == PASS_STATUS:
        result["status"] = BLOCKED_STATUS
        result["exit_code"] = None
        result["stderr_excerpt"] = _bounded(
            f"runner-owned temp directory cleanup failed for profile {profile_id}; {result['stderr_excerpt']}",
            excerpt_max_chars,
        )
    if not result["isolated_workspace_removed"] and result["status"] == PASS_STATUS:
        result["status"] = BLOCKED_STATUS
        result["exit_code"] = None
        result["stderr_excerpt"] = _bounded(
            f"isolated workspace cleanup failed for profile {profile_id}; {result['stderr_excerpt']}",
            excerpt_max_chars,
        )
    return result


def _validated_repo_root(repo_root: Path | str) -> Path:
    resolved = Path(repo_root).resolve()
    if resolved != REPO_ROOT:
        raise ValueError("repo_root must be the canonical BLK-System repository root")
    if not (resolved / ".git").exists():
        raise ValueError("repo_root is not a Git repository")
    return resolved


def _git_status_snapshot(cwd: str, env: Mapping[str, str]) -> str:
    git_env = dict(env)
    git_env["GIT_OPTIONAL_LOCKS"] = "0"
    completed = subprocess.run(
        [_trusted_executable("git"), "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=cwd,
        env=git_env,
        shell=False,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return completed.stdout + completed.stderr + f"\nexit={completed.returncode}"


def _run_fixed_process(
    argv: Sequence[str], *, cwd: str, env: Mapping[str, str], timeout_seconds: int, output_byte_limit: int
) -> ProcessOutcome:
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        try:
            process = subprocess.Popen(
                list(argv),
                cwd=cwd,
                env=dict(env),
                shell=False,
                stdout=stdout_file,
                stderr=stderr_file,
                start_new_session=True,
            )
        except OSError as exc:
            return ProcessOutcome(exit_code=None, stdout="", stderr=str(exc), startup_failed=True)
        timed_out = False
        timeout_cleanup = "PROCESS_GROUP_KILL_NOT_NEEDED"
        try:
            process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
                timeout_cleanup = "PROCESS_GROUP_KILL_ATTEMPTED"
            except (ProcessLookupError, PermissionError, AttributeError):
                process.kill()
                timeout_cleanup = "DIRECT_CHILD_KILL_FALLBACK"
            process.wait(timeout=5)
        stdout_text, stdout_over = _read_limited_output(stdout_file, output_byte_limit)
        stderr_text, stderr_over = _read_limited_output(stderr_file, output_byte_limit)
        return ProcessOutcome(
            exit_code=None if timed_out else process.returncode,
            stdout=stdout_text,
            stderr=stderr_text,
            timed_out=timed_out,
            output_limit_exceeded=stdout_over or stderr_over,
            timeout_cleanup=timeout_cleanup,
        )


def _read_limited_output(handle, limit: int) -> tuple[str, bool]:
    handle.flush()
    size = handle.seek(0, os.SEEK_END)
    handle.seek(0)
    data = handle.read(limit + 1)
    over = size > limit or len(data) > limit
    if len(data) > limit:
        data = data[:limit]
    return _coerce_text(data), over


def _validated_argv(argv: Sequence[str]) -> list[str]:
    if isinstance(argv, (str, bytes)) or not isinstance(argv, Sequence):
        raise ValueError("argv must be a fixed sequence")
    values = list(argv)
    if not values or not all(isinstance(item, str) and item for item in values):
        raise ValueError("argv entries must be non-empty strings")
    executable_name = Path(values[0]).name
    if executable_name in _FORBIDDEN_EXECUTABLES:
        raise ValueError("forbidden executable in health-check profile")
    if any(item in _FORBIDDEN_INLINE_FLAGS for item in values[1:]):
        raise ValueError("inline interpreter execution is forbidden")
    if executable_name == "git" and any(item in _GIT_MUTATIONS for item in values[1:]):
        raise ValueError("Git mutation commands are forbidden")
    joined = " ".join(values)
    if any(pattern.search(joined) for pattern in _FORBIDDEN_ARG_PATTERNS):
        raise ValueError("health-check profile contains forbidden authority or protected-surface text")
    return values


def _scrubbed_environment(runner_temp: Path | None = None, workspace_root: Path | None = None) -> dict[str, str]:
    allowed = {}
    for key in ("HOME", "LANG", "LC_ALL", "TZ"):
        value = os.environ.get(key)
        if value and not _secret_key(key):
            allowed[key] = value
    temp_root = runner_temp.resolve() if runner_temp is not None else Path(tempfile.gettempdir()).resolve()
    pycache_root = temp_root / "pycache"
    tmp_root = temp_root / "tmp"
    pycache_root.mkdir(parents=True, exist_ok=True)
    tmp_root.mkdir(parents=True, exist_ok=True)
    python_root = (workspace_root.resolve() if workspace_root is not None else REPO_ROOT) / "python"
    if workspace_root is not None and workspace_root.resolve() != REPO_ROOT.resolve():
        allowed["BLK_HEALTH_CHECK_SKIP_GIT_ROOT_SELFTESTS"] = "1"
    allowed["PATH"] = TRUSTED_PATH
    allowed["PYTHONPATH"] = str(python_root)
    allowed["PYTHONDONTWRITEBYTECODE"] = "1"
    allowed["PYTHONPYCACHEPREFIX"] = str(pycache_root)
    allowed["TMPDIR"] = str(tmp_root)
    allowed["TMP"] = str(tmp_root)
    allowed["TEMP"] = str(tmp_root)
    return allowed


def _repo_cache_snapshot(repo_root: Path) -> frozenset[str]:
    entries: set[str] = set()
    for path in repo_root.rglob("*.pyc"):
        if path.is_file():
            stat = path.stat()
            rel = path.relative_to(repo_root).as_posix()
            entries.add(f"{rel}:{stat.st_size}:{stat.st_mtime_ns}")
    for path in repo_root.rglob("__pycache__"):
        if path.is_dir():
            stat = path.stat()
            rel = path.relative_to(repo_root).as_posix() + "/"
            entries.add(f"{rel}:{stat.st_mtime_ns}")
    return frozenset(entries)


def _copy_isolated_workspace(source_root: Path, target_root: Path) -> None:
    source = Path(source_root).resolve()
    target = Path(target_root).resolve()
    if _path_inside(target, source):
        raise ValueError("isolated workspace target must be outside source repository")
    if target.exists():
        raise ValueError("isolated workspace target already exists")

    def ignore(dir_path: str, names: list[str]) -> set[str]:
        current = Path(dir_path).resolve()
        try:
            current_rel = current.relative_to(source)
        except ValueError:
            return set(names)
        ignored: set[str] = set()
        for name in names:
            candidate = current / name
            rel = (current_rel / name).as_posix() if current_rel.as_posix() != "." else name
            if rel in _ISOLATED_COPY_EXCLUDED_DIRS or any(
                rel.startswith(prefix + "/") for prefix in _ISOLATED_COPY_EXCLUDED_DIRS
            ):
                ignored.add(name)
            elif name == "__pycache__" or name.endswith(".pyc"):
                ignored.add(name)
            elif candidate.is_symlink():
                ignored.add(name)
        return ignored

    shutil.copytree(source, target, ignore=ignore, symlinks=True)


def _secret_key(key: str) -> bool:
    upper = key.upper()
    return any(token in upper for token in _SECRET_ENV_TOKENS)


def _coerce_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _redact(text: str) -> tuple[str, bool]:
    redacted = text
    changed = False
    for pattern in _SECRET_PATTERNS:
        new = pattern.sub(lambda match: (match.group(1) if match.groups() else "") + "[REDACTED]", redacted)
        if new != redacted:
            changed = True
            redacted = new
    return redacted, changed


def _bounded(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len("...[truncated]")] + "...[truncated]"


def _evidence_hash(profile_id: str, argv: Sequence[str], exit_code: int | None, stdout: str, stderr: str, status: str) -> str:
    payload = "\n".join([profile_id, repr(list(argv)), repr(exit_code), status, stdout, stderr])
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


validate_profile_registry(PROFILES)
