"""Python adapter for invoking blk-pipe with JSON payload files.

This module intentionally contains no tactical-engine or LLM integration. It is a
thin local subprocess adapter around the blk-pipe CLI contract.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from codex_private_bwrap_setup import DEFAULT_INSTALL_DIR, build_codex_private_bwrap_env


@dataclass
class ExecutionResult:
    status: str
    exit_code: int
    pre_engine_hash: str = ""
    commit_hash: str = ""
    git_diff: str = ""
    engine_logs: str = ""
    validation_logs: dict[str, str] | None = None
    diff_summary: dict | None = None
    error: str | None = None
    untracked_files: list[str] | None = None
    staged_files: list[str] | None = None
    destroyed_files: list[str] | None = None
    trace_artifacts: list[dict[str, str]] | None = None
    validation_profiles: list[str] | None = None
    validation_profile_capabilities: list[str] | None = None
    validation_trust_boundary: str = ""
    payload_trust_boundary: str = ""
    timeout_seconds: int = 0
    max_output_bytes: int = 0
    allowed_modified_files: list[str] | None = None
    allowed_new_files: list[str] | None = None
    failure_class: str = ""
    denial_route: str = ""
    cleanup_status: str = ""
    resolved_validation_commands: list[str] | None = None
    resolved_validation_argv: list[list[str]] | None = None
    raw_report: dict | None = None
    stderr: str = ""
    blk_pipe_binary_path: str = ""


_DEFAULT_STATUS_BY_CODE = {
    0: "SUCCESS",
    1: "FATAL_SYSTEM_PANIC",
    2: "SYNTAX_GATE_FAILED",
    3: "UNAUTHORIZED_FILE_MUTATION",
    4: "INVALID_REVERT_ANCHOR",
    5: "FATAL_OUTPUT_FLOOD",
    6: "ENGINE_TIMEOUT",
    7: "GIT_DIRTY",
    8: "INVALID_PAYLOAD",
    9: "INTERNAL_ERROR",
}

_ALLOWED_STATUSES_BY_CODE = {
    0: {"SUCCESS"},
    1: {"FATAL_SYSTEM_PANIC", "FATAL_ENGINE_FAILED"},
    2: {"SYNTAX_GATE_FAILED"},
    3: {"UNAUTHORIZED_FILE_MUTATION", "TARGET_HEAD_MISMATCH"},
    4: {"INVALID_REVERT_ANCHOR"},
    5: {"FATAL_OUTPUT_FLOOD"},
    6: {"ENGINE_TIMEOUT"},
    7: {"GIT_DIRTY"},
    8: {"INVALID_PAYLOAD"},
    9: {"INTERNAL_ERROR"},
}

_TRACE_VERSION_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_MAX_VALIDATION_COMMANDS = 16
_MAX_VALIDATION_COMMAND_BYTES = 4096
_PROTECTED_BLK_REQ_PREFIXES = (
    "docs/active/",
    "docs/requirements/",
    "docs/use_cases/",
)


def _required_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _validate_trace_artifacts(trace_artifacts: Any) -> list[dict[str, str]]:
    if not isinstance(trace_artifacts, list) or not trace_artifacts:
        raise ValueError("trace_artifacts must be a non-empty list")
    validated: list[dict[str, str]] = []
    for index, artifact in enumerate(trace_artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be an object")
        kind = _required_non_empty_string(artifact.get("kind"), f"trace_artifacts[{index}].kind")
        artifact_id = _required_non_empty_string(artifact.get("id"), f"trace_artifacts[{index}].id")
        version_hash = _required_non_empty_string(
            artifact.get("version_hash"), f"trace_artifacts[{index}].version_hash"
        )
        if not _TRACE_VERSION_HASH_RE.match(version_hash):
            raise ValueError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        validated.append({"kind": kind, "id": artifact_id, "version_hash": version_hash})
    return validated


def _validate_path_list(paths: Any, field_name: str) -> list[str]:
    if paths is None:
        return []
    if not isinstance(paths, list):
        raise ValueError(f"{field_name} must be a list")
    validated: list[str] = []
    for index, path in enumerate(paths):
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"{field_name}[{index}] must be a non-empty relative path")
        normalized = path.strip().replace("\\", "/")
        if normalized.startswith("/"):
            raise ValueError(f"{field_name}[{index}] must be relative")
        parts = [part for part in normalized.split("/") if part]
        if ".." in parts:
            raise ValueError(f"{field_name}[{index}] must not contain path traversal")
        normalized = "/".join(parts)
        if not normalized:
            raise ValueError(f"{field_name}[{index}] must be a non-empty relative path")
        protected = any(
            normalized == prefix.rstrip("/") or normalized.startswith(prefix)
            for prefix in _PROTECTED_BLK_REQ_PREFIXES
        )
        if protected:
            raise ValueError(f"{field_name}[{index}] targets protected BLK-req path: {normalized}")
        validated.append(normalized)
    return validated


def _validate_validation_profiles(profiles: Any) -> list[str]:
    if profiles is None:
        return []
    if not isinstance(profiles, list):
        raise ValueError("validation_profiles must be a list")
    validated: list[str] = []
    seen: set[str] = set()
    for index, profile in enumerate(profiles):
        if not isinstance(profile, str) or not profile.strip():
            raise ValueError(f"validation_profiles[{index}] must be a non-empty string")
        profile = profile.strip()
        if profile in seen:
            raise ValueError(f"validation_profiles contains duplicate profile: {profile}")
        seen.add(profile)
        validated.append(profile)
    return validated


def _validate_validation_commands(commands: Any) -> list[str]:
    if commands is None:
        return []
    if not isinstance(commands, list):
        raise ValueError("validation_commands must be a list")
    if len(commands) > _MAX_VALIDATION_COMMANDS:
        raise ValueError(f"validation_commands exceeds maximum count of {_MAX_VALIDATION_COMMANDS}")
    validated: list[str] = []
    for index, command in enumerate(commands):
        if not isinstance(command, str) or not command.strip():
            raise ValueError(f"validation_commands[{index}] must be a non-empty string")
        if len(command.encode("utf-8")) > _MAX_VALIDATION_COMMAND_BYTES:
            raise ValueError(
                f"validation_commands[{index}] exceeds maximum size of {_MAX_VALIDATION_COMMAND_BYTES} bytes"
            )
        validated.append(command)
    return validated


def _validate_execute_payload_policy(payload: dict[str, Any]) -> None:
    _required_non_empty_string(payload.get("beb_id"), "beb_id")
    work_dir = _required_non_empty_string(payload.get("work_dir"), "work_dir")
    if not os.path.isabs(work_dir):
        raise ValueError("work_dir must be an absolute path")
    _required_non_empty_string(payload.get("target_branch"), "target_branch")
    _required_non_empty_string(payload.get("engine"), "engine")
    _required_non_empty_string(payload.get("l2_packet"), "l2_packet")
    if not isinstance(payload.get("engine_args"), list):
        raise ValueError("engine_args must be a list")
    payload["trace_artifacts"] = _validate_trace_artifacts(payload.get("trace_artifacts"))
    payload["allowed_modified_files"] = _validate_path_list(
        payload.get("allowed_modified_files"), "allowed_modified_files"
    )
    payload["allowed_new_files"] = _validate_path_list(
        payload.get("allowed_new_files"), "allowed_new_files"
    )
    has_profiles = "validation_profiles" in payload
    has_commands = "validation_commands" in payload
    if has_profiles and has_commands:
        raise ValueError("validation_profiles and validation_commands must not both be supplied")
    if has_profiles:
        payload["validation_profiles"] = _validate_validation_profiles(payload.get("validation_profiles"))
        if not payload["validation_profiles"]:
            raise ValueError("validation_profiles or validation_commands required")
    elif has_commands:
        payload["validation_commands"] = _validate_validation_commands(payload.get("validation_commands"))
        if not payload["validation_commands"]:
            raise ValueError("validation_profiles or validation_commands required")
    else:
        raise ValueError("validation_profiles or validation_commands required")


def resolve_blk_pipe_binary(binary_path: str = "blk-pipe") -> str:
    """Resolve the blk-pipe executable or build a repo-local temporary binary.

    The default route should not require an operator to hand-place /tmp/blk-pipe.
    Explicit binary paths are preserved. For the default command name, PATH wins;
    otherwise the BLK-System repo-local cmd/blk-pipe source is built into
    /var/tmp/blk-system-bin/blk-pipe.
    """
    if binary_path != "blk-pipe":
        return binary_path
    resolved = shutil.which(binary_path)
    if resolved:
        return resolved
    repo_root = Path(os.environ.get("BLK_SYSTEM_REPO_ROOT", Path(__file__).resolve().parents[1])).resolve()
    source_dir = repo_root / "cmd" / "blk-pipe"
    if source_dir.is_dir():
        output_dir = Path("/var/tmp/blk-system-bin")
        output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        output_path = output_dir / "blk-pipe"
        result = subprocess.run(
            ["go", "build", "-o", str(output_path), "./cmd/blk-pipe"],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=_build_subprocess_env(str(repo_root)),
        )
        if result.returncode == 0:
            return str(output_path)
        raise FileNotFoundError(
            "blk-pipe executable not found on PATH and repo-local build failed; "
            f"run: cd {repo_root} && go build -o {output_path} ./cmd/blk-pipe; stderr={result.stderr.strip()}"
        )
    raise FileNotFoundError(
        "blk-pipe executable not found on PATH and repo-local cmd/blk-pipe source was unavailable; "
        "run: go build -o /var/tmp/blk-system-bin/blk-pipe ./cmd/blk-pipe and put that directory on PATH"
    )


def _build_subprocess_env(work_dir: str | None = None) -> dict[str, str]:
    env = os.environ.copy()
    for key in ("SSH_AUTH_SOCK", "SSH_AGENT_PID", "SSH_ASKPASS"):
        env.pop(key, None)
    private_bwrap_dir = env.get("BLK_CODEX_PRIVATE_BWRAP_DIR")
    if private_bwrap_dir:
        resolved_private_dir = Path(private_bwrap_dir).expanduser().resolve()
        if resolved_private_dir != DEFAULT_INSTALL_DIR:
            raise ValueError(
                "BLK_CODEX_PRIVATE_BWRAP_DIR must be the trusted BLK-SYSTEM-229 install dir "
                f"{DEFAULT_INSTALL_DIR}; got {resolved_private_dir}"
            )
        env = build_codex_private_bwrap_env(env, private_bwrap_dir=resolved_private_dir)
    if work_dir:
        env["PWD"] = work_dir
    return env


class BlkPipeAdapter:
    def __init__(self, binary_path: str = "blk-pipe") -> None:
        self.binary_path = resolve_blk_pipe_binary(binary_path)

    def run_health_check(self) -> bool:
        result = subprocess.run(
            [self.binary_path, "--health"],
            capture_output=True,
            text=True,
            check=False,
            env=_build_subprocess_env(),
        )
        return result.returncode == 0

    def execute_sprint(
        self,
        beb_id: str,
        work_dir: str,
        target_branch: str,
        engine: str,
        engine_args: list[str],
        l2_packet: str,
        validation_commands: list[str] | None = None,
        allowed_modified_files: list[str] | None = None,
        allowed_new_files: list[str] | None = None,
        trace_artifacts: list[dict[str, str]] | None = None,
        validation_profiles: list[str] | None = None,
        target_hash: str | None = None,
        progress_callback: Any | None = None,
        progress_interval_seconds: Any = 30.0,
        commit_message: str | None = None,
    ) -> ExecutionResult:
        if validation_profiles is not None and validation_commands is not None:
            raise ValueError("validation_profiles and validation_commands must not both be supplied")
        if commit_message is not None:
            if not isinstance(commit_message, str) or not commit_message.strip():
                raise ValueError("commit_message must be a non-empty string when supplied")
            if commit_message.strip() != commit_message:
                raise ValueError("commit_message must not be silently normalized")
            if any(ch in commit_message for ch in "\r\n") or len(commit_message.encode("utf-8")) > 120:
                raise ValueError("commit_message must be one bounded single line")
        # Keep l2_packet opaque; blk-pipe validates size and delivers it to engine stdin.
        payload = {
            "action": "execute",
            "beb_id": beb_id,
            "work_dir": work_dir,
            "target_branch": target_branch,
            "engine": engine,
            "engine_args": engine_args,
            "l2_packet": l2_packet,
            "allowed_modified_files": allowed_modified_files or [],
            "allowed_new_files": allowed_new_files or [],
        }
        if target_hash is not None:
            payload["target_hash"] = target_hash
        if commit_message is not None:
            payload["commit_message"] = commit_message
        if validation_profiles is not None:
            payload["validation_profiles"] = validation_profiles
        else:
            payload["validation_commands"] = validation_commands or []
        if trace_artifacts is not None:
            payload["trace_artifacts"] = trace_artifacts
        _validate_execute_payload_policy(payload)
        return self._invoke_binary(
            payload,
            progress_callback=progress_callback,
            progress_interval_seconds=progress_interval_seconds,
        )

    def abort_sprint_and_revert(
        self,
        work_dir: str,
        target_branch: str,
        pre_engine_hash: str,
    ) -> ExecutionResult:
        payload = {
            "action": "revert",
            "work_dir": work_dir,
            "target_branch": target_branch,
            "target_hash": pre_engine_hash,
            "beb_id": "REVERT",
            "engine": "",
            "engine_args": [],
            "l2_packet": "",
            "validation_commands": [],
            "allowed_modified_files": [],
            "allowed_new_files": [],
        }
        return self._invoke_binary(payload)

    def _invoke_binary(
        self,
        payload: dict[str, Any],
        *,
        progress_callback: Any | None = None,
        progress_interval_seconds: Any = 30.0,
        commit_message: str | None = None,
    ) -> ExecutionResult:
        temp_payload_path = ""
        phase_progress_seen = False
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_payload:
                temp_payload_path = temp_payload.name
                json.dump(payload, temp_payload)

            if progress_callback is None:
                result = subprocess.run(
                    [self.binary_path, "--payload", temp_payload_path],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=1800,
                    env=_build_subprocess_env(payload.get("work_dir")),
                )

                def emit_progress(event: str, **fields: Any) -> None:
                    return
            else:
                started_at = time.monotonic()
                try:
                    interval = max(float(progress_interval_seconds), 0.0)
                except (TypeError, ValueError):
                    interval = 30.0
                next_progress_at = started_at + interval if interval else float("inf")
                progress_base = {
                    "beb_id": payload.get("beb_id", ""),
                    "work_dir": payload.get("work_dir", ""),
                    "target_branch": payload.get("target_branch", ""),
                    "binary_path": self.binary_path,
                }

                def emit_progress(event: str, **fields: Any) -> None:
                    if progress_callback is None:
                        return
                    payload_event = {
                        **progress_base,
                        "event": event,
                        "elapsed_seconds": round(time.monotonic() - started_at, 3),
                        **fields,
                    }
                    try:
                        progress_callback(payload_event)
                    except BaseException:
                        pass

                emit_progress("preflight_ready")
                emit_progress("blk_pipe_launching")
                try:
                    process = subprocess.Popen(
                        [self.binary_path, "--payload", temp_payload_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        env=_build_subprocess_env(payload.get("work_dir")),
                    )
                except OSError:
                    emit_progress("codex_failed", status="FATAL_LAUNCH_FAILED", failure_class="launch_failed")
                    emit_progress("blk_pipe_finished", status="FATAL_LAUNCH_FAILED", exit_code=1)
                    raise
                emit_progress("blk_pipe_started", elapsed_seconds=0.0)

                stdout_chunks: list[str] = []
                stderr_chunks: list[str] = []
                phase_progress_seen = False

                def read_stdout() -> None:
                    if process.stdout is not None:
                        with process.stdout as stream:
                            stdout_chunks.append(stream.read() or "")

                def read_stderr() -> None:
                    nonlocal phase_progress_seen
                    if process.stderr is None:
                        return
                    with process.stderr as stream:
                        for line in stream:
                            if line.startswith("BLK_PROGRESS_JSON "):
                                try:
                                    event = json.loads(line.removeprefix("BLK_PROGRESS_JSON "))
                                except json.JSONDecodeError:
                                    stderr_chunks.append(line)
                                    continue
                                event_name = event.get("event", "")
                                if event_name in {
                                    "codex_started",
                                    "codex_completed",
                                    "codex_failed",
                                    "validation_started",
                                    "validation_passed",
                                    "validation_failed",
                                    "testing_completed",
                                    "testing_failed",
                                }:
                                    phase_progress_seen = True
                                emit_progress(str(event_name), **{k: v for k, v in event.items() if k != "event"})
                            else:
                                stderr_chunks.append(line)

                stdout_thread = threading.Thread(target=read_stdout, daemon=True)
                stderr_thread = threading.Thread(target=read_stderr, daemon=True)
                stdout_thread.start()
                stderr_thread.start()
                deadline = started_at + 1800
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        process.kill()
                        process.wait()
                        stdout_thread.join(timeout=1)
                        stderr_thread.join(timeout=1)
                        stdout = "".join(stdout_chunks)
                        stderr = "".join(stderr_chunks)
                        emit_progress(
                            "codex_failed",
                            status="FATAL_PYTHON_TIMEOUT",
                            failure_class="python_adapter_timeout",
                            timeout_seconds=1800,
                        )
                        emit_progress("blk_pipe_finished", status="FATAL_PYTHON_TIMEOUT", exit_code=1)
                        return ExecutionResult(
                            status="FATAL_PYTHON_TIMEOUT",
                            exit_code=1,
                            pre_engine_hash="",
                            commit_hash="",
                            git_diff="",
                            engine_logs="",
                            validation_logs={},
                            trace_artifacts=[],
                            raw_report=None,
                            stderr=stderr,
                            error="Catastrophic Go deadlock. Python adapter killed process.",
                            blk_pipe_binary_path=self.binary_path,
                        )
                    if process.poll() is not None:
                        break
                    wait_seconds = min(0.1, remaining)
                    if interval:
                        wait_seconds = min(wait_seconds, max(next_progress_at - time.monotonic(), 0.01))
                    time.sleep(wait_seconds)
                    if interval and time.monotonic() >= next_progress_at:
                        emit_progress("blk_pipe_running")
                        next_progress_at = time.monotonic() + interval
                stdout_thread.join(timeout=1)
                stderr_thread.join(timeout=1)
                stdout = "".join(stdout_chunks)
                stderr = "".join(stderr_chunks)
                result = subprocess.CompletedProcess(
                    args=[self.binary_path, "--payload", temp_payload_path],
                    returncode=process.returncode,
                    stdout=stdout,
                    stderr=stderr,
                )


            try:
                parsed_output = json.loads(result.stdout)
            except json.JSONDecodeError:
                emit_progress("blk_pipe_finished", status="FATAL_CRASH", exit_code=result.returncode)
                return ExecutionResult(
                    status="FATAL_CRASH",
                    exit_code=result.returncode,
                    pre_engine_hash="",
                    commit_hash="",
                    git_diff="",
                    engine_logs="",
                    validation_logs={},
                    trace_artifacts=[],
                    raw_report=None,
                    stderr=result.stderr,
                    blk_pipe_binary_path=self.binary_path,
                    error=(
                        "No JSON returned. Go Panic or OS Kill. "
                        f"Stderr: {result.stderr.strip()}"
                    ),
                )

            parsed_status = parsed_output.get("status")
            allowed_statuses = _ALLOWED_STATUSES_BY_CODE.get(result.returncode)
            if allowed_statuses is None:
                final_status = "INTERNAL_ERROR"
            elif parsed_status in allowed_statuses:
                final_status = parsed_status
            else:
                final_status = _DEFAULT_STATUS_BY_CODE[result.returncode]

            progress_fields = {
                "status": final_status,
                "exit_code": result.returncode,
                "failure_class": parsed_output.get("failure_class") or "",
                "denial_route": parsed_output.get("denial_route") or "",
                "timeout_seconds": parsed_output.get("timeout_seconds") or 0,
                "error": parsed_output.get("error") or "",
            }
            if not phase_progress_seen:
                emit_progress("codex_started")
                if final_status in {"ENGINE_TIMEOUT", "FATAL_ENGINE_FAILED", "FATAL_OUTPUT_FLOOD"}:
                    emit_progress("codex_failed", **progress_fields)
                elif final_status in {"SUCCESS", "SYNTAX_GATE_FAILED", "UNAUTHORIZED_FILE_MUTATION"}:
                    emit_progress("codex_completed", **progress_fields)

                validation_fields = {
                    **progress_fields,
                    "validation_command_count": len(parsed_output.get("validation_logs") or {}),
                }
                if final_status in {"SUCCESS", "SYNTAX_GATE_FAILED"}:
                    emit_progress("validation_started", **validation_fields)
                if final_status == "SUCCESS":
                    emit_progress("validation_passed", **validation_fields)
                    emit_progress("testing_completed", **validation_fields)
                elif final_status == "SYNTAX_GATE_FAILED":
                    emit_progress("validation_failed", **validation_fields)
                    emit_progress("testing_failed", **validation_fields)

            emit_progress("blk_pipe_finished", status=final_status, exit_code=result.returncode)
            return ExecutionResult(
                status=final_status,
                exit_code=result.returncode,
                pre_engine_hash=parsed_output.get("pre_engine_hash", ""),
                commit_hash=parsed_output.get("commit_hash", ""),
                git_diff=parsed_output.get("git_diff", ""),
                engine_logs=parsed_output.get("engine_logs", ""),
                validation_logs=parsed_output.get("validation_logs", {}),
                diff_summary=parsed_output.get("diff_summary"),
                error=parsed_output.get("error"),
                untracked_files=parsed_output.get("untracked_files"),
                staged_files=parsed_output.get("staged_files"),
                destroyed_files=parsed_output.get("destroyed_files"),
                trace_artifacts=parsed_output.get("trace_artifacts") or [],
                validation_profiles=parsed_output.get("validation_profiles") or [],
                validation_profile_capabilities=parsed_output.get("validation_profile_capabilities") or [],
                validation_trust_boundary=parsed_output.get("validation_trust_boundary") or "",
                payload_trust_boundary=parsed_output.get("payload_trust_boundary") or "",
                timeout_seconds=parsed_output.get("timeout_seconds") or 0,
                max_output_bytes=parsed_output.get("max_output_bytes") or 0,
                allowed_modified_files=parsed_output.get("allowed_modified_files") or [],
                allowed_new_files=parsed_output.get("allowed_new_files") or [],
                failure_class=parsed_output.get("failure_class") or "",
                denial_route=parsed_output.get("denial_route") or "",
                cleanup_status=parsed_output.get("cleanup_status") or "",
                resolved_validation_commands=parsed_output.get("resolved_validation_commands") or [],
                resolved_validation_argv=parsed_output.get("resolved_validation_argv") or [],
                raw_report=parsed_output,
                stderr=result.stderr,
                blk_pipe_binary_path=self.binary_path,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status="FATAL_PYTHON_TIMEOUT",
                exit_code=1,
                pre_engine_hash="",
                commit_hash="",
                git_diff="",
                engine_logs="",
                validation_logs={},
                trace_artifacts=[],
                raw_report=None,
                stderr="",
                error="Catastrophic Go deadlock. Python adapter killed process.",
                blk_pipe_binary_path=self.binary_path,
            )
        finally:
            if temp_payload_path:
                Path(temp_payload_path).unlink(missing_ok=True)
