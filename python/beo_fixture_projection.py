"""Draft BEO projection fixtures for Sprint 004.

This module consumes deterministic BLK-test handoff dictionaries only. It does
not inspect BLK-req active vault files, generate RTMs, call live BLK-test MCP,
call Codex, or contact model/network services.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

_VALID_BLK_TEST_STATUSES = {"PASS", "FAIL"}
_SOURCE = "blk-test-fixture"
_RTM_STATUS = "NOT_GENERATED"


def project_blk_test_handoff_to_beo(
    blk_test_handoff: dict[str, Any],
    *,
    beo_id: str,
) -> dict[str, Any]:
    """Project a deterministic BLK-test PASS/FAIL handoff into a draft BEO fixture.

    PASS handoffs produce PASS BEO fixtures. FAIL handoffs produce failed BEO
    fixtures; they never get upgraded to success. The trace_artifacts list is
    copied verbatim as an opaque version_hash baton. RTM generation is explicitly
    out of scope for Sprint 004 fixture projection.
    """
    status = _required_status(blk_test_handoff)
    return {
        "beo_id": _required_string(beo_id, "beo_id"),
        "beb_id": _required_string(blk_test_handoff.get("beb_id"), "beb_id"),
        "status": status,
        "source": _SOURCE,
        "commit_hash": str(blk_test_handoff.get("commit_hash", "")),
        "pre_engine_hash": _required_string(
            blk_test_handoff.get("pre_engine_hash"), "pre_engine_hash"
        ),
        "trace_artifacts": _trace_artifacts(blk_test_handoff),
        "test_summary": _test_summary(blk_test_handoff),
        "rtm_status": _RTM_STATUS,
    }


def _required_status(blk_test_handoff: dict[str, Any]) -> str:
    status = str(blk_test_handoff.get("status", ""))
    if status not in _VALID_BLK_TEST_STATUSES:
        raise ValueError(f"unsupported BLK-test fixture status: {status}")
    return status


def _required_string(value: Any, field: str) -> str:
    text = str(value or "")
    if not text.strip():
        raise ValueError(f"BEO fixture requires non-empty {field}")
    return text


def _trace_artifacts(blk_test_handoff: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = blk_test_handoff.get("trace_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("BEO fixture requires non-empty trace_artifacts")
    normalized: list[dict[str, str]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("BEO fixture trace_artifacts must contain objects")
        kind = _required_string(artifact.get("kind"), "trace_artifacts.kind")
        artifact_id = _required_string(artifact.get("id"), "trace_artifacts.id")
        version_hash = _required_string(
            artifact.get("version_hash"), "trace_artifacts.version_hash"
        )
        normalized.append(
            {
                "kind": kind,
                "id": artifact_id,
                "version_hash": version_hash,
            }
        )
    return deepcopy(normalized)


def _test_summary(blk_test_handoff: dict[str, Any]) -> dict[str, Any]:
    profile = _required_string(blk_test_handoff.get("test_profile"), "test_profile")
    checks = blk_test_handoff.get("checks")
    if not isinstance(checks, list):
        raise ValueError("BEO fixture requires checks list")

    checks_passed = 0
    checks_failed = 0
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("BEO fixture checks must contain objects")
        check_status = str(check.get("status", ""))
        if check_status == "PASS":
            checks_passed += 1
        elif check_status == "FAIL":
            checks_failed += 1

    return {
        "profile": profile,
        "checks_passed": checks_passed,
        "checks_failed": checks_failed,
    }
