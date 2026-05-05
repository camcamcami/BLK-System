"""Draft BEO projection fixtures for BLK-test and disabled MCP fixture data.

This module consumes deterministic BLK-test handoff dictionaries and source-bound
disabled BLK-test MCP mapped-response dictionaries only. It does not inspect
BLK-req active vault files, generate RTMs, call live BLK-test MCP, call Codex,
or contact model/network services.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

_VALID_BLK_TEST_STATUSES = {"PASS", "FAIL"}
_SOURCE = "blk-test-fixture"
_MCP_RESPONSE_SOURCE = "blk-test-mcp-response-shape"
_RTM_STATUS = "NOT_GENERATED"
_BEO_PUBLICATION = "DRAFT_ONLY"
_TRACE_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


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
        "beo_publication": _BEO_PUBLICATION,
    }


def project_mapped_mcp_response_to_beo(
    mapped_response: dict[str, object],
    *,
    beo_id: str,
    test_profile: str = "strict-ci",
) -> dict[str, object]:
    """Project a source-bound disabled MCP PASS/FAIL mapping into a draft BEO.

    This consumes only local mapped-response fixture data. It does not call live
    BLK-test profiles, generate RTM, or publish authoritative BEO data.
    """
    if str(mapped_response.get("source", "")) != _MCP_RESPONSE_SOURCE:
        raise ValueError(f"mapped_response source must be {_MCP_RESPONSE_SOURCE}")

    status = str(mapped_response.get("status", ""))
    if status not in _VALID_BLK_TEST_STATUSES:
        raise ValueError("mapped_response status must be PASS/FAIL")

    checks = mapped_response.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("BEO fixture requires non-empty checks")

    summary_source = dict(mapped_response)
    summary_source["test_profile"] = _required_string(test_profile, "test_profile")

    return {
        "beo_id": _required_string(beo_id, "beo_id"),
        "beb_id": _required_string(mapped_response.get("beb_id"), "beb_id"),
        "status": status,
        "source": _MCP_RESPONSE_SOURCE,
        "commit_hash": _required_string(mapped_response.get("commit_hash"), "commit_hash"),
        "pre_engine_hash": _required_string(
            mapped_response.get("pre_engine_hash"), "pre_engine_hash"
        ),
        "trace_artifacts": _trace_artifacts(mapped_response),
        "test_summary": _test_summary(summary_source),
        "rtm_status": _RTM_STATUS,
        "beo_publication": _BEO_PUBLICATION,
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
        if not _TRACE_HASH_PATTERN.match(version_hash):
            raise ValueError("trace_artifacts.version_hash must match sha256:<64-lowercase-hex>")
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
