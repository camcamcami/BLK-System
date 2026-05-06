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
