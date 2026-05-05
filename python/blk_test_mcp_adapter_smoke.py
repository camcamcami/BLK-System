"""Disabled BLK-test MCP adapter smoke fixture for Sprint 007.

This module composes the existing disabled BLK-test MCP request builder, send
stub, and source-bound response mapper. It is a dependency-free local fixture:
it does not open network sockets, spawn subprocesses, call live MCP servers,
call Codex or model services, generate RTM, or publish authoritative BEOs.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from blk_orchestrator_gate import (
    build_blk_test_mcp_request,
    map_blk_test_mcp_response,
    send_blk_test_mcp_request,
)

_SOURCE = "disabled-blk-test-mcp-adapter-smoke"


def run_disabled_blk_test_mcp_adapter_smoke(
    source_report: dict[str, object],
    *,
    response_fixture: dict[str, object] | None = None,
    enabled: bool = False,
) -> dict[str, object]:
    """Run a deterministic disabled BLK-test MCP adapter smoke path.

    With no response fixture this proves that the send path remains blocked and
    records that no network or subprocess call occurred. With a PASS/FAIL
    response fixture it additionally maps the response against the exact source
    request evidence.
    """
    if enabled:
        raise RuntimeError("live BLK-test MCP adapter smoke path is disabled in Sprint 007")

    request = build_blk_test_mcp_request(source_report, enabled=False)
    send_result = send_blk_test_mcp_request(request, enabled=False)

    result: dict[str, Any] = {
        "adapter_status": "DISABLED_SEND_BLOCKED",
        "source": _SOURCE,
        "transport": request["transport"],
        "request": deepcopy(request),
        "send_result": deepcopy(send_result),
        "network_called": bool(send_result.get("network_called", False)),
        "subprocess_called": bool(send_result.get("subprocess_called", False)),
        "rtm_status": request["rtm_status"],
        "beo_publication": request["beo_publication"],
    }

    if response_fixture is not None:
        mapped_response = map_blk_test_mcp_response(response_fixture, source_request=request)
        result["adapter_status"] = "FIXTURE_RESPONSE_MAPPED"
        result["mapped_response"] = deepcopy(mapped_response)

    return result
