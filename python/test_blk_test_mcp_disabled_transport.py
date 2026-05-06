import ast
import unittest
from pathlib import Path

from blk_test_mcp_disabled_transport import (
    build_disabled_lifecycle_probe,
    build_disabled_transport_descriptor,
    build_non_executing_handshake_probe,
    evaluate_disabled_transport_startup,
    evaluate_disabled_tool_execution,
    evaluate_sprint013_approval_preflight,
    fixed_tool_registry_descriptor,
)


def assert_no_git_authority_fields(test_case, evidence):
    for key in (
        "source_write_allowed",
        "staging_allowed",
        "commit_allowed",
        "push_allowed",
    ):
        test_case.assertIn(key, evidence)
        test_case.assertFalse(evidence[key])


def _assert_disabled_transport_source_has_no_live_surfaces(source: str) -> None:
    forbidden_import_roots = {"subprocess", "socket", "requests", "http", "urllib", "asyncio"}
    forbidden_literals = ("shell=True", "publish_beo", "generate_rtm", "read_active_vault")
    literal_offenders = [marker for marker in forbidden_literals if marker in source]
    assert not literal_offenders, f"forbidden live literal markers: {literal_offenders}"

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in forbidden_import_roots:
                    offenders.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            if root in forbidden_import_roots:
                offenders.append(f"from {module}")
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in {"eval", "exec", "__import__"}:
                offenders.append(f"call {func.id}")
            elif isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name):
                    dotted = f"{func.value.id}.{func.attr}"
                    if dotted in {"os.system", "subprocess.Popen"}:
                        offenders.append(f"call {dotted}")
                if func.attr in {"Popen", "run_command"}:
                    offenders.append(f"call *.{func.attr}")
    assert not offenders, f"forbidden live surfaces: {offenders}"


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
        assert_no_git_authority_fields(self, descriptor)
        self.assertIn("does not authorize live BLK-test MCP", descriptor["reason"])

    def test_startup_decision_blocks_default_descriptor_without_side_effects(self):
        decision = evaluate_disabled_transport_startup(build_disabled_transport_descriptor())

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_DISABLED")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])
        assert_no_git_authority_fields(self, decision)

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

    def test_startup_decision_rejects_tainted_non_stdio_descriptor_metadata(self):
        descriptor = build_disabled_transport_descriptor()
        descriptor["transport"] = "tcp"

        with self.assertRaisesRegex(ValueError, "stdio-only"):
            evaluate_disabled_transport_startup(descriptor)

    def test_handshake_probe_rejects_tainted_non_stdio_descriptor_metadata(self):
        descriptor = build_disabled_transport_descriptor()
        descriptor["transport"] = "http"

        with self.assertRaisesRegex(ValueError, "stdio-only"):
            build_non_executing_handshake_probe(descriptor)

    def test_lifecycle_probe_rejects_tainted_non_stdio_descriptor_metadata(self):
        descriptor = build_disabled_transport_descriptor()
        descriptor["transport"] = "websocket"

        with self.assertRaisesRegex(ValueError, "stdio-only"):
            build_disabled_lifecycle_probe(descriptor, event="startup_refused")

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
        assert_no_git_authority_fields(self, probe)

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
        assert_no_git_authority_fields(self, probe)

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

    def test_fixed_tool_registry_is_descriptor_only_and_has_no_arbitrary_shell(self):
        registry = fixed_tool_registry_descriptor()
        names = {entry["name"] for entry in registry}

        self.assertEqual(
            names,
            {
                "run_ast_validation",
                "run_ipc_race_test",
                "run_svg_export_purity_test",
                "run_architecture_lint",
            },
        )
        forbidden = {
            "shell",
            "exec",
            "run_command",
            "bash",
            "python",
            "node",
            "npm",
            "curl",
            "wget",
            "git_write",
            "stage",
            "commit",
            "autofix",
            "publish_beo",
            "generate_rtm",
            "read_active_vault",
        }
        self.assertTrue(names.isdisjoint(forbidden))
        for entry in registry:
            self.assertEqual(entry["status"], "DESCRIPTOR_ONLY")
            self.assertFalse(entry["executor_available"])
            self.assertTrue(entry["requires_future_workspace_controls"])
            self.assertTrue(entry["requires_future_approval_controls"])
            self.assertFalse(entry["source_mutation_allowed"])
            self.assertFalse(entry["beo_publication_allowed"])
            self.assertFalse(entry["rtm_generation_allowed"])
            self.assertFalse(entry["active_vault_read_allowed"])
            assert_no_git_authority_fields(self, entry)

    def test_disabled_tool_execution_always_blocks_even_for_known_tool(self):
        result = evaluate_disabled_tool_execution("run_ast_validation", arguments={})

        self.assertEqual(result["decision"], "TOOL_EXECUTION_BLOCKED_DISABLED")
        self.assertEqual(result["tool_name"], "run_ast_validation")
        self.assertFalse(result["executor_available"])
        self.assertFalse(result["server_started"])
        self.assertFalse(result["client_started"])
        self.assertFalse(result["subprocess_called"])
        self.assertFalse(result["network_called"])
        self.assertFalse(result["source_mutation_allowed"])
        self.assertFalse(result["beo_publication_allowed"])
        self.assertFalse(result["rtm_generation_allowed"])
        self.assertFalse(result["active_vault_read_allowed"])
        assert_no_git_authority_fields(self, result)
        self.assertEqual(result["tools_executed"], [])
        self.assertEqual(result["tests_executed"], [])

    def test_disabled_tool_execution_blocks_unknown_tool_without_dynamic_dispatch(self):
        result = evaluate_disabled_tool_execution("shell", arguments={"cmd": "pytest"})

        self.assertEqual(result["decision"], "TOOL_EXECUTION_BLOCKED_UNKNOWN_TOOL")
        self.assertEqual(result["tool_name"], "shell")
        self.assertFalse(result["executor_available"])
        self.assertFalse(result["subprocess_called"])
        self.assertFalse(result["network_called"])
        self.assertEqual(result["tools_executed"], [])
        self.assertEqual(result["tests_executed"], [])

    def test_sprint013_validated_approval_still_blocks_live_startup_until_sprint014(self):
        approval_decision = {
            "decision": "APPROVAL_VALIDATED_SOURCE_BOUND",
            "approval_id": "BLKTEST-S13-APPROVAL-001",
            "approval_record_hash": "sha256:" + "c" * 64,
            "source_evidence_hash": "sha256:" + "d" * 64,
            "authorization_request_hash": "sha256:" + "e" * 64,
            "live_mcp_authorized": False,
        }
        descriptor = build_disabled_transport_descriptor(
            approval_record={"approval_id": "BLKTEST-S13-APPROVAL-001"}
        )
        decision = evaluate_sprint013_approval_preflight(descriptor, approval_decision)

        self.assertEqual(decision["decision"], "STARTUP_BLOCKED_SPRINT014_REQUIRED")
        self.assertEqual(decision["approval_id"], "BLKTEST-S13-APPROVAL-001")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertFalse(decision["live_mcp_authorized"])
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
        assert_no_git_authority_fields(self, decision)
        self.assertIn("Sprint 014", decision["reason"])

    def test_sprint013_approval_preflight_rejects_malformed_hash_evidence(self):
        descriptor = build_disabled_transport_descriptor()
        approval_decision = {
            "decision": "APPROVAL_VALIDATED_SOURCE_BOUND",
            "approval_id": "BLKTEST-S13-APPROVAL-001",
            "approval_record_hash": "sha256:short",
            "source_evidence_hash": "sha256:" + "d" * 64,
            "authorization_request_hash": "sha256:" + "e" * 64,
            "live_mcp_authorized": False,
        }

        with self.assertRaisesRegex(ValueError, "approval_record_hash"):
            evaluate_sprint013_approval_preflight(descriptor, approval_decision)

    def test_sprint013_approval_preflight_rejects_unvalidated_decision(self):
        descriptor = build_disabled_transport_descriptor()
        approval_decision = {
            "decision": "APPROVAL_REJECTED",
            "approval_id": "BLKTEST-S13-APPROVAL-001",
            "approval_record_hash": "sha256:" + "c" * 64,
            "source_evidence_hash": "sha256:" + "d" * 64,
            "authorization_request_hash": "sha256:" + "e" * 64,
            "live_mcp_authorized": False,
        }

        with self.assertRaisesRegex(ValueError, "APPROVAL_VALIDATED_SOURCE_BOUND"):
            evaluate_sprint013_approval_preflight(descriptor, approval_decision)

    def test_disabled_transport_module_does_not_import_live_execution_surfaces(self):
        text = Path(__file__).with_name("blk_test_mcp_disabled_transport.py").read_text()
        _assert_disabled_transport_source_has_no_live_surfaces(text)

    def test_live_surface_source_scan_rejects_ast_imports_and_calls_but_allows_public_evidence_keys(self):
        safe_public_evidence = "descriptor['subprocess_called'] = False"
        _assert_disabled_transport_source_has_no_live_surfaces(safe_public_evidence)

        bad_sources = [
            "import subprocess\n",
            "from socket import socket\n",
            "import os\nos.system('echo bad')\n",
            "eval('1 + 1')\n",
            "__import__('subprocess')\n",
            "subprocess.Popen(['true'])\n",
            "shell=True\n",
            "publish_beo\n",
            "generate_rtm\n",
            "read_active_vault\n",
        ]
        for source in bad_sources:
            with self.assertRaises(AssertionError, msg=source):
                _assert_disabled_transport_source_has_no_live_surfaces(source)
