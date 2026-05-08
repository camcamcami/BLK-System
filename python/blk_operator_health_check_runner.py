"""Advisory health-check runner for BLK-SYSTEM-032/033.

The runner executes only repository-owned fixed profiles and returns bounded
advisory evidence. It is not a general command runner.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
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
TRUSTED_PATH = f"{Path.home() / '.local' / 'bin'}:/usr/bin:/bin"
DEFAULT_OUTPUT_BYTE_LIMIT = 64 * 1024


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


def _trusted_executable(name: str) -> str:
    if name == "python3":
        executable = Path(sys.executable).resolve()
        if executable.exists() and executable.is_file():
            return str(executable)
    resolved = shutil.which(name, path=TRUSTED_PATH)
    if not resolved:
        raise RuntimeError(f"trusted executable not found: {name}")
    return str(Path(resolved).resolve())


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
) -> dict[str, object]:
    if not isinstance(profile_id, str) or not re.fullmatch(r"[a-z0-9_]+", profile_id):
        raise ValueError("profile_id must name a fixed BLK-SYSTEM-033 profile")
    if profile_id not in PROFILES:
        raise ValueError("unknown health-check profile")
    if not isinstance(excerpt_max_chars, int) or not (32 <= excerpt_max_chars <= 4000):
        raise ValueError("excerpt_max_chars must be between 32 and 4000")
    if not isinstance(output_byte_limit, int) or not (1024 <= output_byte_limit <= 1024 * 1024):
        raise ValueError("output_byte_limit must be between 1024 and 1048576 bytes")

    profile = PROFILES[profile_id]
    argv = _validated_argv(profile.argv)
    cwd = str(_validated_repo_root(repo_root))
    env = _scrubbed_environment()

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
    if outcome.timed_out:
        status = BLOCKED_STATUS
        exit_code = None
        stderr = f"profile {profile_id} timed out after {profile.timeout_seconds}s; {stderr}"
    elif outcome.output_limit_exceeded:
        status = BLOCKED_STATUS
        exit_code = None
        stderr = f"output limit exceeded for profile {profile_id}; {stderr}"
    else:
        status = PASS_STATUS if exit_code == 0 else FAIL_STATUS

    clean_stdout, redacted_stdout = _redact(stdout)
    clean_stderr, redacted_stderr = _redact(stderr)
    stdout_excerpt = _bounded(clean_stdout, excerpt_max_chars)
    stderr_excerpt = _bounded(clean_stderr, excerpt_max_chars)
    evidence_hash = _evidence_hash(profile_id, argv, exit_code, clean_stdout, clean_stderr, status)

    return {
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
        "network_called": False,
        "package_manager_called": False,
        "git_mutated": False,
        "source_mutated": False,
        "approval_captured": False,
        "protected_body_read": False,
        "active_vault_scanned": False,
        "beo_published": False,
        "rtm_generated": False,
        "drift_decision_made": False,
        "production_authority_granted": False,
    }


def _validated_repo_root(repo_root: Path | str) -> Path:
    resolved = Path(repo_root).resolve()
    if resolved != REPO_ROOT:
        raise ValueError("repo_root must be the canonical BLK-System repository root")
    if not (resolved / ".git").exists():
        raise ValueError("repo_root is not a Git repository")
    return resolved


def _run_fixed_process(
    argv: Sequence[str], *, cwd: str, env: Mapping[str, str], timeout_seconds: int, output_byte_limit: int
) -> ProcessOutcome:
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            env=dict(env),
            shell=False,
            stdout=stdout_file,
            stderr=stderr_file,
        )
        timed_out = False
        try:
            process.communicate(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            process.wait(timeout=5)
        stdout_text, stdout_over = _read_limited_output(stdout_file, output_byte_limit)
        stderr_text, stderr_over = _read_limited_output(stderr_file, output_byte_limit)
        return ProcessOutcome(
            exit_code=None if timed_out else process.returncode,
            stdout=stdout_text,
            stderr=stderr_text,
            timed_out=timed_out,
            output_limit_exceeded=stdout_over or stderr_over,
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


def _scrubbed_environment() -> dict[str, str]:
    allowed = {}
    for key in ("HOME", "LANG", "LC_ALL", "TZ"):
        value = os.environ.get(key)
        if value and not _secret_key(key):
            allowed[key] = value
    allowed["PATH"] = TRUSTED_PATH
    allowed["PYTHONPATH"] = str(REPO_ROOT / "python")
    allowed["PYTHONDONTWRITEBYTECODE"] = "1"
    return allowed


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
