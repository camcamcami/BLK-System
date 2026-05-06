import unittest
from pathlib import Path

from blk_test_mcp_disabled_transport import (
    build_disabled_lifecycle_probe,
    build_disabled_transport_descriptor,
    build_non_executing_handshake_probe,
    evaluate_disabled_transport_startup,
)


class DisabledTransportStartupTest(unittest.TestCase):
    def test_default_descriptor_is_stdio_only_disabled_and_non_executing(self):
        descriptor = build_disabled_transport_descriptor()

        self.assertEqual(descriptor["component"], "blk-test-mcp-disabled-transport")
        self.assertEqual(descriptor["transport"], "stdio")
        self.assertFalse(descriptor["enabled"])
        self.assertEqual(descriptor["startup_status"], "DISABLED_BY_DEFAULT")
        self.assertFalse(descriptor["live_mcp_authorized"])
        self.assertFalse(descriptor["server_started"])
        self.assertFalse(descriptor["client_started"])
        self.assertFalse(descriptor["network_called"])
        self.assertFalse(descriptor["subprocess_called"])
        self.assertEqual(descriptor["tools_executed"], [])
        self.assertEqual(descriptor["rtm_status"], "NOT_GENERATED")
        self.assertEqual(descriptor["beo_publication"], "DRAFT_ONLY")
        self.assertFalse(descriptor["active_vault_read"])
        self.assertFalse(descriptor["source_mutation_allowed"])
        self.assertIn("does not authorize live BLK-test MCP", descriptor["reason"])

    def test_startup_decision_blocks_default_descriptor_without_side_effects(self):
        decision = evaluate_disabled_transport_startup(build_disabled_transport_descriptor())

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_DISABLED")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])

    def test_non_stdio_transport_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "stdio-only"):
            build_disabled_transport_descriptor(transport="http")

    def test_enabled_request_is_blocked_not_started(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            build_disabled_transport_descriptor(enabled=True)

    def test_approval_record_does_not_enable_transport_in_sprint011(self):
        descriptor = build_disabled_transport_descriptor(
            approval_record={"operator": "human", "approved": True}
        )
        decision = evaluate_disabled_transport_startup(descriptor)

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_APPROVAL_NOT_IMPLEMENTED")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertIn("Sprint 013 owns approval mechanics", decision["reason"])

    def test_non_executing_handshake_never_initializes_jsonrpc_or_lists_tools(self):
        probe = build_non_executing_handshake_probe(build_disabled_transport_descriptor())

        self.assertEqual(probe["handshake_status"], "HANDSHAKE_NOT_ATTEMPTED_DISABLED")
        self.assertFalse(probe["jsonrpc_initialized"])
        self.assertFalse(probe["server_started"])
        self.assertFalse(probe["client_started"])
        self.assertFalse(probe["tools_listed"])
        self.assertEqual(probe["tools_executed"], [])
        self.assertEqual(probe["tests_executed"], [])
        self.assertFalse(probe["network_called"])
        self.assertFalse(probe["subprocess_called"])

    def test_disabled_lifecycle_probe_records_startup_refusal_without_processes(self):
        probe = build_disabled_lifecycle_probe(
            build_disabled_transport_descriptor(),
            event="startup_refused",
        )

        self.assertEqual(probe["lifecycle_status"], "STARTUP_REFUSAL_RECORDED")
        self.assertEqual(
            probe["events"],
            ["descriptor_loaded", "startup_refused", "no_transport_started"],
        )
        self.assertEqual(probe["process_ids"], [])
        self.assertEqual(probe["workspace_paths"], [])
        self.assertFalse(probe["server_started"])
        self.assertFalse(probe["client_started"])

    def test_disabled_lifecycle_probe_records_shutdown_noop_without_processes(self):
        probe = build_disabled_lifecycle_probe(
            build_disabled_transport_descriptor(),
            event="operator_shutdown_noop",
        )

        self.assertEqual(probe["lifecycle_status"], "NOOP_SHUTDOWN_RECORDED")
        self.assertEqual(
            probe["events"],
            ["descriptor_loaded", "operator_shutdown_noop", "no_process_to_shutdown"],
        )
        self.assertEqual(probe["process_ids"], [])
        self.assertEqual(probe["workspace_paths"], [])
        self.assertFalse(probe["server_started"])
        self.assertFalse(probe["client_started"])

    def test_disabled_lifecycle_probe_records_config_rejection_without_processes(self):
        probe = build_disabled_lifecycle_probe(
            build_disabled_transport_descriptor(),
            event="config_rejected",
        )

        self.assertEqual(probe["lifecycle_status"], "CONFIG_REJECTION_RECORDED")
        self.assertEqual(
            probe["events"],
            ["descriptor_loaded", "config_rejected", "no_transport_started"],
        )
        self.assertEqual(probe["process_ids"], [])
        self.assertEqual(probe["workspace_paths"], [])
        self.assertFalse(probe["server_started"])
        self.assertFalse(probe["client_started"])

    def test_disabled_lifecycle_probe_rejects_unknown_event(self):
        with self.assertRaisesRegex(ValueError, "unsupported lifecycle event"):
            build_disabled_lifecycle_probe(
                build_disabled_transport_descriptor(),
                event="unexpected_restart",
            )

    def test_disabled_transport_module_does_not_import_live_execution_surfaces(self):
        text = Path(__file__).with_name("blk_test_mcp_disabled_transport.py").read_text()
        forbidden = [
            "import socket",
            "from socket",
            "subprocess",
            "Popen",
            "os.system",
            "requests",
            "http.server",
        ]
        offenders = [marker for marker in forbidden if marker in text]
        self.assertEqual(offenders, [])
