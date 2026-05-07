"""Python adapter for invoking blk-pipe with JSON payload files.

This module intentionally contains no tactical-engine or LLM integration. It is a
thin local subprocess adapter around the blk-pipe CLI contract.
"""

from __future__ import annotations

import json
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
    resolved_validation_commands: list[str] | None = None
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
    9: "INTERNAL_ERROR",
}

_ALLOWED_STATUSES_BY_CODE = {
    0: {"SUCCESS"},
    1: {"FATAL_SYSTEM_PANIC", "FATAL_ENGINE_FAILED"},
    2: {"INVALID_PAYLOAD", "SYNTAX_GATE_FAILED"},
    3: {"UNAUTHORIZED_FILE_MUTATION"},
    4: {"INVALID_REVERT_ANCHOR"},
    5: {"FATAL_OUTPUT_FLOOD"},
    6: {"ENGINE_TIMEOUT"},
    7: {"GIT_DIRTY"},
    9: {"INTERNAL_ERROR"},
}


class BlkPipeAdapter:
    def __init__(self, binary_path: str = "blk-pipe") -> None:
        self.binary_path = binary_path

    def run_health_check(self) -> bool:
        result = subprocess.run(
            [self.binary_path, "--health"],
            capture_output=True,
            text=True,
            check=False,
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
                resolved_validation_commands=parsed_output.get("resolved_validation_commands") or [],
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
