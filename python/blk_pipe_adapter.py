"""Python adapter for invoking blk-pipe with JSON payload files.

This module intentionally contains no tactical-engine or LLM integration. It is a
thin local subprocess adapter around the blk-pipe CLI contract.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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


def _build_subprocess_env(work_dir: str | None = None) -> dict[str, str]:
    env = os.environ.copy()
    for key in ("SSH_AUTH_SOCK", "SSH_AGENT_PID", "SSH_ASKPASS"):
        env.pop(key, None)
    if work_dir:
        env["PWD"] = work_dir
    return env


class BlkPipeAdapter:
    def __init__(self, binary_path: str = "blk-pipe") -> None:
        self.binary_path = binary_path

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
    ) -> ExecutionResult:
        if validation_profiles is not None and validation_commands is not None:
            raise ValueError("validation_profiles and validation_commands must not both be supplied")
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
        if validation_profiles is not None:
            payload["validation_profiles"] = validation_profiles
        else:
            payload["validation_commands"] = validation_commands or []
        if trace_artifacts is not None:
            payload["trace_artifacts"] = trace_artifacts
        _validate_execute_payload_policy(payload)
        return self._invoke_binary(payload)

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

    def _invoke_binary(self, payload: dict[str, Any]) -> ExecutionResult:
        temp_payload_path = ""
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_payload:
                temp_payload_path = temp_payload.name
                json.dump(payload, temp_payload)

            result = subprocess.run(
                [self.binary_path, "--payload", temp_payload_path],
                capture_output=True,
                text=True,
                check=False,
                timeout=1800,
                env=_build_subprocess_env(payload.get("work_dir")),
            )

            try:
                parsed_output = json.loads(result.stdout)
            except json.JSONDecodeError:
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
            )
        finally:
            if temp_payload_path:
                Path(temp_payload_path).unlink(missing_ok=True)
