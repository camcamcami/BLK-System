"""Deterministic BLK-test PASS/FAIL/BLOCKED handoff fixtures.

This module consumes an already-supplied BLK-pipe report dictionary only. It does
not call BLK-test MCP, model services, LLMs, network services, or requirement
vault readers.
"""

from __future__ import annotations
from copy import deepcopy
import re
from typing import Any

_EXPECTED_STAGED_FILE = "dry_run_output.txt"
_DEFAULT_TEST_PROFILE = "strict-ci"
_MAX_TRACE_FIELD_BYTES = 256
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_VALID_SOURCE_STATUSES = {
    "SUCCESS",
    "FATAL_SYSTEM_PANIC",
    "FATAL_ENGINE_FAILED",
    "INVALID_PAYLOAD",
    "SYNTAX_GATE_FAILED",
    "UNAUTHORIZED_FILE_MUTATION",
    "INVALID_REVERT_ANCHOR",
    "FATAL_OUTPUT_FLOOD",
    "ENGINE_TIMEOUT",
    "GIT_DIRTY",
    "INTERNAL_ERROR",
    "FATAL_CRASH",
    "FATAL_PYTHON_TIMEOUT",
}


def build_blk_test_pass_handoff(
    source_report: dict[str, Any],
    *,
    test_profile: str = _DEFAULT_TEST_PROFILE,
    max_log_bytes: int = 4096,
) -> dict[str, Any]:
    """Build a deterministic BLK-test PASS handoff from a successful report."""
    _require_success_source_report(source_report)
    return _handoff(
        source_report,
        status="PASS",
        test_profile=test_profile,
        checks=[
            {
                "name": "fixture-output-present",
                "status": "PASS",
                "summary": "dry_run_output.txt exists",
            }
        ],
        max_log_bytes=max_log_bytes,
    )


def build_blk_test_fail_handoff(
    source_report: dict[str, Any],
    *,
    test_profile: str = _DEFAULT_TEST_PROFILE,
    max_log_bytes: int = 4096,
) -> dict[str, Any]:
    """Build a deterministic BLK-test FAIL handoff from a successful report.

    FAIL means fixture checks failed after BLK-pipe succeeded; it is not a route
    for non-success BLK-pipe reports.
    """
    _require_success_source_report(source_report)
    return _handoff(
        source_report,
        status="FAIL",
        test_profile=test_profile,
        checks=[
            {
                "name": "fixture-output-present",
                "status": "FAIL",
                "summary": "dry_run_output.txt missing",
            }
        ],
        max_log_bytes=max_log_bytes,
    )


def build_blk_test_blocked_handoff(
    source_report: dict[str, Any],
    *,
    test_profile: str = _DEFAULT_TEST_PROFILE,
    max_log_bytes: int = 4096,
) -> dict[str, Any]:
    """Build a deterministic BLOCKED handoff for a non-success BLK-pipe report."""
    status = _source_status(source_report)
    if status == "SUCCESS":
        raise ValueError("BLOCKED handoff requires a non-SUCCESS BLK-pipe report")
    return _handoff(
        source_report,
        status="BLOCKED",
        test_profile=test_profile,
        checks=[
            {
                "name": "blk-pipe-success-required",
                "status": "BLOCKED",
                "summary": f"BLK-test did not run because BLK-pipe status was {status}",
            }
        ],
        max_log_bytes=max_log_bytes,
        require_success_shape=False,
    )


def _require_success_source_report(source_report: dict[str, Any]) -> None:
    status = _source_status(source_report)
    if status != "SUCCESS":
        raise ValueError(f"BLK-test PASS/FAIL requires BLK-pipe status SUCCESS, got {status}")
    if not str(source_report.get("commit_hash", "")).strip():
        raise ValueError("BLK-pipe report must include non-empty commit_hash")
    if not str(source_report.get("pre_engine_hash", "")).strip():
        raise ValueError("BLK-pipe report must include non-empty pre_engine_hash")
    if source_report.get("staged_files") != [_EXPECTED_STAGED_FILE]:
        raise ValueError("BLK-pipe report must stage exactly dry_run_output.txt")
    _trace_artifacts(source_report, require_non_empty=True)


def _source_status(source_report: dict[str, Any]) -> str:
    status = str(source_report.get("status", ""))
    if status not in _VALID_SOURCE_STATUSES:
        raise ValueError(f"unknown BLK-pipe status: {status}")
    return status


def _handoff(
    source_report: dict[str, Any],
    *,
    status: str,
    test_profile: str,
    checks: list[dict[str, str]],
    max_log_bytes: int,
    require_success_shape: bool = True,
) -> dict[str, Any]:
    if require_success_shape:
        _require_success_source_report(source_report)
    else:
        _source_status(source_report)
    trace_artifacts = _trace_artifacts(source_report, require_non_empty=require_success_shape)
    handoff = {
        "status": status,
        "beb_id": str(source_report.get("beb_id", "")),
        "commit_hash": str(source_report.get("commit_hash", "")),
        "pre_engine_hash": str(source_report.get("pre_engine_hash", "")),
        "test_profile": test_profile,
        "trace_artifacts": trace_artifacts,
        "checks": deepcopy(checks),
        "compressed_logs": _compressed_logs(source_report, max_log_bytes=max_log_bytes),
    }
    if status == "BLOCKED" and not trace_artifacts:
        handoff["trace_absence_reason"] = "source report did not include decoded trace_artifacts"
    return handoff


def _trace_artifacts(source_report: dict[str, Any], *, require_non_empty: bool) -> list[dict[str, str]]:
    artifacts = source_report.get("trace_artifacts")
    if not isinstance(artifacts, list):
        if require_non_empty:
            raise ValueError("BLK-test handoff requires non-empty trace_artifacts")
        return []
    if require_non_empty and not artifacts:
        raise ValueError("BLK-test handoff requires non-empty trace_artifacts")
    safe_artifacts: list[dict[str, str]] = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise ValueError(f"trace_artifacts[{index}] must be an object")
        kind = _required_string(artifact.get("kind"), f"trace_artifacts[{index}].kind")
        artifact_id = _required_string(artifact.get("id"), f"trace_artifacts[{index}].id")
        version_hash = _required_string(artifact.get("version_hash"), f"trace_artifacts[{index}].version_hash")
        if not _TRACE_HASH_PATTERN.match(version_hash):
            raise ValueError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
        safe_artifacts.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
            }
        )
    return safe_artifacts


def _required_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    if len(value.encode("utf-8")) > _MAX_TRACE_FIELD_BYTES:
        raise ValueError(f"{field_name} exceeds maximum size of {_MAX_TRACE_FIELD_BYTES} bytes")
    return value


def _compressed_logs(source_report: dict[str, Any], *, max_log_bytes: int) -> str:
    if max_log_bytes <= 0:
        raise ValueError("max_log_bytes must be positive")
    raw_logs = str(source_report.get("engine_logs") or source_report.get("error") or "")
    unique_lines: list[str] = []
    seen: set[str] = set()
    for line in raw_logs.splitlines():
        if line in seen:
            continue
        seen.add(line)
        unique_lines.append(line)
    text = "\n".join(unique_lines)
    encoded = text.encode("utf-8")
    if len(encoded) <= max_log_bytes:
        return text
    marker = "...[truncated]"
    marker_bytes = marker.encode("utf-8")
    if max_log_bytes <= len(marker_bytes):
        return marker.encode("utf-8")[:max_log_bytes].decode("utf-8", errors="ignore")
    head = encoded[: max_log_bytes - len(marker_bytes)]
    return head.decode("utf-8", errors="ignore") + marker
