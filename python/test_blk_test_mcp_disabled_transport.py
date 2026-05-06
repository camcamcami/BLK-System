import unittest
from pathlib import Path

from blk_test_mcp_disabled_transport import (
    build_disabled_transport_descriptor,
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
