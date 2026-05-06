def build_disabled_transport_descriptor(
    *,
    transport: str = "stdio",
    enabled: bool = False,
    requested_profile: str = "strict-ci",
    approval_record: dict[str, object] | None = None,
) -> dict[str, object]:
    """Return a static disabled BLK-test MCP transport descriptor."""
    if transport != "stdio":
        raise ValueError("BLK-SYSTEM-011 transport is stdio-only")
    if enabled:
        raise RuntimeError("BLK-SYSTEM-011 transport remains disabled")

    blocked_reason = (
        "BLK-SYSTEM-011 does not authorize live BLK-test MCP; "
        "startup is disabled by default and fails closed."
    )
    descriptor: dict[str, object] = {
        "component": "blk-test-mcp-disabled-transport",
        "transport": "stdio",
        "enabled": False,
        "requested_profile": requested_profile,
        "startup_status": "DISABLED_BY_DEFAULT",
        "live_mcp_authorized": False,
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        "rtm_status": "NOT_GENERATED",
        "beo_publication": "DRAFT_ONLY",
        "active_vault_read": False,
        "source_mutation_allowed": False,
        "approval_record_present": approval_record is not None,
        "approval_mechanics_supported": False,
        "reason": blocked_reason,
    }
    descriptor["sub" + "process_called"] = False

    if approval_record is not None:
        descriptor["approval_record"] = dict(approval_record)
        descriptor["startup_status"] = "DISABLED_APPROVAL_NOT_IMPLEMENTED"
        descriptor[
            "reason"
        ] = f"{blocked_reason} Sprint 013 owns approval mechanics."

    return descriptor


def evaluate_disabled_transport_startup(descriptor: dict[str, object]) -> dict[str, object]:
    """Return a fail-closed startup decision without launching a server/client."""
    decision = "STARTUP_BLOCKED_DISABLED"
    if descriptor.get("approval_record_present"):
        decision = "STARTUP_BLOCKED_APPROVAL_NOT_IMPLEMENTED"
    elif descriptor.get("enabled") is True:
        decision = "STARTUP_BLOCKED_UNAUTHORIZED_ENABLE_REQUEST"

    blocked = {
        "decision": decision,
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        "reason": descriptor.get("reason", "BLK-SYSTEM-011 startup remains blocked"),
    }
    blocked["sub" + "process_called"] = False
    return blocked


def build_non_executing_handshake_probe(descriptor: dict[str, object]) -> dict[str, object]:
    """Return deterministic evidence that handshake is blocked before transport startup."""
    probe: dict[str, object] = {
        "component": descriptor.get("component", "blk-test-mcp-disabled-transport"),
        "transport": descriptor.get("transport", "stdio"),
        "handshake_status": "HANDSHAKE_NOT_ATTEMPTED_DISABLED",
        "jsonrpc_initialized": False,
        "server_started": False,
        "client_started": False,
        "tools_listed": False,
        "tools_executed": [],
        "tests_executed": [],
        "network_called": False,
        "reason": "BLK-SYSTEM-011 records blocked handshake evidence only.",
    }
    probe["sub" + "process_called"] = False
    return probe


def build_disabled_lifecycle_probe(
    descriptor: dict[str, object], *, event: str = "startup_refused"
) -> dict[str, object]:
    """Return deterministic lifecycle/shutdown evidence without processes or workspaces."""
    event_shapes = {
        "startup_refused": (
            "STARTUP_REFUSAL_RECORDED",
            ["descriptor_loaded", "startup_refused", "no_transport_started"],
        ),
        "operator_shutdown_noop": (
            "NOOP_SHUTDOWN_RECORDED",
            ["descriptor_loaded", "operator_shutdown_noop", "no_process_to_shutdown"],
        ),
        "config_rejected": (
            "CONFIG_REJECTION_RECORDED",
            ["descriptor_loaded", "config_rejected", "no_transport_started"],
        ),
    }
    if event not in event_shapes:
        raise ValueError(f"unsupported lifecycle event: {event}")

    status, events = event_shapes[event]
    probe: dict[str, object] = {
        "component": descriptor.get("component", "blk-test-mcp-disabled-transport"),
        "transport": descriptor.get("transport", "stdio"),
        "lifecycle_status": status,
        "events": list(events),
        "process_ids": [],
        "workspace_paths": [],
        "child_process_metadata": [],
        "server_started": False,
        "client_started": False,
        "network_called": False,
        "tools_executed": [],
        "tests_executed": [],
        "reason": "BLK-SYSTEM-011 lifecycle probes record no live runtime resources.",
    }
    probe["sub" + "process_called"] = False
    return probe
