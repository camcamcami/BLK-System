import os
import tempfile
import textwrap
import unittest
from copy import deepcopy
from pathlib import Path

from blk_test_mcp_approval_authorization import validate_blk_test_approval_record
from blk_test_mcp_disabled_transport import build_disabled_transport_descriptor
from blk_test_mcp_fixed_tool_live_smoke import (
    build_sprint014_live_smoke_authorization_request,
    evaluate_sprint014_live_smoke_preflight,
    fixed_sprint014_live_tool_registry_descriptor,
    resolve_sprint014_fixed_tool_command,
    run_sprint014_fixed_tool_stdio_smoke,
    validate_sprint014_smoke_workspace,
)

TRACE_S14 = {
    "kind": "REQ",
    "id": "REQ-S14-SMOKE-001",
    "version_hash": "sha256:" + "1" * 64,
}
SOURCE_REPORT_IDENTITY_S14 = {
    "report_path": "reports/BLK-SYSTEM-014/synthetic-source-report.json",
    "report_hash": "sha256:" + "2" * 64,
    "report_id": "source-report-BLK-SYSTEM-014-smoke",
}
SOURCE_REPORT_S14 = {
    "status": "SUCCESS",
    "source_report_identity": SOURCE_REPORT_IDENTITY_S14,
    "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
    "commit_hash": "synthetic-fixture-no-git-commit",
    "pre_engine_hash": "sha256:" + "3" * 64,
    "trace_artifacts": [TRACE_S14],
}
WORKSPACE_IDENTITY_S14 = {
    "target_branch": "synthetic-sprint-014-smoke",
    "workspace_clone_id": "workspace-BLK-SYSTEM-014-smoke-run-001",
    "source_path_policy": "synthetic-isolated-copy-only",
}
TIMEOUT_OUTPUT_PROFILE_S14 = {
    "timeout_class": "bounded-live-smoke-short",
    "timeout_seconds": 5,
    "output_byte_limit": 4096,
    "compression": "line-dedupe-byte-bound",
}
ISSUED_AT_S14 = "2026-05-07T00:00:00Z"
EXPIRES_AT_S14 = "2026-05-07T00:15:00Z"
NOW_S14 = "2026-05-07T00:05:00Z"


def valid_authorization_request():
    return build_sprint014_live_smoke_authorization_request(
        source_report=deepcopy(SOURCE_REPORT_S14),
        workspace_identity=deepcopy(WORKSPACE_IDENTITY_S14),
        timeout_output_profile=deepcopy(TIMEOUT_OUTPUT_PROFILE_S14),
    )


def valid_approval_record(request=None):
    request = request or valid_authorization_request()
    return {
        "approval_kind": "blk-test-mcp-live-smoke",
        "approval_id": "BLKTEST-S14-SMOKE-APPROVAL-001",
        "operator_identity": "operator:camcamcami",
        "approval_timestamp": "2026-05-07T00:01:00Z",
        "issued_at": ISSUED_AT_S14,
        "expires_at": EXPIRES_AT_S14,
        "source_evidence": deepcopy(request["source_evidence"]),
        "requested_tools": list(request["requested_tools"]),
        "test_profile": request["test_profile"],
        "workspace_identity": deepcopy(request["workspace_identity"]),
        "timeout_output_profile": deepcopy(request["timeout_output_profile"]),
    }


def valid_approval_decision(request=None, approval=None):
    request = request or valid_authorization_request()
    approval = approval or valid_approval_record(request)
    return validate_blk_test_approval_record(approval, request, now=NOW_S14)


class Sprint014LiveSmokePreflightTest(unittest.TestCase):
    def test_accepts_exact_approval_and_explicit_live_smoke_flag_without_starting_process(self):
        request = valid_authorization_request()
        approval_decision = valid_approval_decision(request)
        descriptor = build_disabled_transport_descriptor(transport="stdio")

        decision = evaluate_sprint014_live_smoke_preflight(
            descriptor=descriptor,
            authorization_request=request,
            approval_decision=approval_decision,
            requested_tool="run_ast_validation",
            live_smoke_enabled=True,
            human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
        )

        self.assertEqual(decision["decision"], "LIVE_SMOKE_PREFLIGHT_ACCEPTED")
        self.assertEqual(decision["sprint"], "BLK-SYSTEM-014")
        self.assertTrue(decision["live_smoke_authorized"])
        self.assertEqual(decision["live_mcp_authorized_scope"], "ONE_RUN_ONE_APPROVED_FIXED_TOOL_STDIO_ONLY")
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertFalse(decision["source_write_allowed"])
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")
        self.assertFalse(decision["active_vault_read"])

    def test_rejects_absent_live_smoke_flag(self):
        with self.assertRaisesRegex(ValueError, "live_smoke_enabled"):
            evaluate_sprint014_live_smoke_preflight(
                descriptor=build_disabled_transport_descriptor(transport="stdio"),
                authorization_request=valid_authorization_request(),
                approval_decision=valid_approval_decision(),
                requested_tool="run_ast_validation",
                live_smoke_enabled=False,
                human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
            )

    def test_codex_live_approval_cannot_validate_for_sprint014(self):
        request = valid_authorization_request()
        approval = valid_approval_record(request)
        approval["approval_kind"] = "codex-live"

        with self.assertRaisesRegex(ValueError, "codex-live"):
            validate_blk_test_approval_record(approval, request, now=NOW_S14)

    def test_rejects_mismatched_authorization_request_hash(self):
        request = valid_authorization_request()
        decision = valid_approval_decision(request)
        mutated = deepcopy(request)
        mutated["workspace_identity"]["workspace_clone_id"] = "other-workspace"

        with self.assertRaisesRegex(ValueError, "authorization_request_hash"):
            evaluate_sprint014_live_smoke_preflight(
                descriptor=build_disabled_transport_descriptor(transport="stdio"),
                authorization_request=mutated,
                approval_decision=decision,
                requested_tool="run_ast_validation",
                live_smoke_enabled=True,
                human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
            )

    def test_rejects_non_stdio_transport(self):
        descriptor = build_disabled_transport_descriptor(transport="stdio")
        descriptor["transport"] = "http"

        with self.assertRaisesRegex(ValueError, "stdio"):
            evaluate_sprint014_live_smoke_preflight(
                descriptor=descriptor,
                authorization_request=valid_authorization_request(),
                approval_decision=valid_approval_decision(),
                requested_tool="run_ast_validation",
                live_smoke_enabled=True,
                human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
            )

    def test_rejects_unknown_multi_wildcard_and_shell_like_tools(self):
        for requested_tool in ("run_architecture_lint", "*", "shell", "run_ast_validation;rm -rf /", ["run_ast_validation", "run_architecture_lint"]):
            with self.subTest(requested_tool=requested_tool):
                with self.assertRaisesRegex(ValueError, "requested_tool"):
                    evaluate_sprint014_live_smoke_preflight(
                        descriptor=build_disabled_transport_descriptor(transport="stdio"),
                        authorization_request=valid_authorization_request(),
                        approval_decision=valid_approval_decision(),
                        requested_tool=requested_tool,
                        live_smoke_enabled=True,
                        human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
                    )

    def test_rejects_missing_human_approval_checkpoint(self):
        with self.assertRaisesRegex(ValueError, "human approval"):
            evaluate_sprint014_live_smoke_preflight(
                descriptor=build_disabled_transport_descriptor(transport="stdio"),
                authorization_request=valid_authorization_request(),
                approval_decision=valid_approval_decision(),
                requested_tool="run_ast_validation",
                live_smoke_enabled=True,
                human_approval_checkpoint="",
            )


class Sprint014FixedToolStdioHarnessTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name) / "synthetic-workspace"
        (self.workspace / "src").mkdir(parents=True)
        (self.workspace / ".blk-system-014-synthetic-workspace").write_text("owned\n")
        (self.workspace / "src" / "smoke_fixture.py").write_text("SMOKE_FIXTURE = True\n")
        self.preflight = evaluate_sprint014_live_smoke_preflight(
            descriptor=build_disabled_transport_descriptor(transport="stdio"),
            authorization_request=valid_authorization_request(),
            approval_decision=valid_approval_decision(),
            requested_tool="run_ast_validation",
            live_smoke_enabled=True,
            human_approval_checkpoint="EXPLICIT_SPRINT014_OPERATOR_APPROVAL_RECORDED",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_registry_exposes_only_first_fixed_tool(self):
        descriptor = fixed_sprint014_live_tool_registry_descriptor()

        self.assertEqual(descriptor["tools"], ["run_ast_validation"])
        self.assertEqual(descriptor["transport"], "stdio-only")
        self.assertFalse(descriptor["arbitrary_shell_allowed"])
        self.assertFalse(descriptor["caller_supplied_command_allowed"])

    def test_static_command_rejects_caller_supplied_command_or_unknown_tool(self):
        command = resolve_sprint014_fixed_tool_command(tool_name="run_ast_validation", workspace_path=self.workspace)

        self.assertIsInstance(command, list)
        self.assertIn("--sprint014-stdio-child", command)
        self.assertIn("--tool", command)
        self.assertNotIn("-c", command)
        with self.assertRaisesRegex(ValueError, "caller-supplied"):
            resolve_sprint014_fixed_tool_command(
                tool_name="run_ast_validation",
                workspace_path=self.workspace,
                caller_supplied_command=["python", "-c", "print('unsafe')"],
            )
        with self.assertRaisesRegex(ValueError, "run_ast_validation"):
            resolve_sprint014_fixed_tool_command(tool_name="shell", workspace_path=self.workspace)

    def test_workspace_guard_rejects_primary_repo_home_root_git_protected_and_symlink_escape(self):
        blocked_paths = [Path("/home/dad/BLK-System"), Path("/"), Path.home()]
        for blocked in blocked_paths:
            with self.subTest(blocked=blocked):
                with self.assertRaisesRegex(ValueError, "workspace"):
                    validate_sprint014_smoke_workspace(
                        workspace_path=blocked,
                        workspace_identity=WORKSPACE_IDENTITY_S14,
                        authorization_request=valid_authorization_request(),
                    )
        (self.workspace / ".git").mkdir()
        with self.assertRaisesRegex(ValueError, "git metadata"):
            validate_sprint014_smoke_workspace(
                workspace_path=self.workspace,
                workspace_identity=WORKSPACE_IDENTITY_S14,
                authorization_request=valid_authorization_request(),
            )
        (self.workspace / ".git").rmdir()
        (self.workspace / "docs" / "requirements").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "protected"):
            validate_sprint014_smoke_workspace(
                workspace_path=self.workspace,
                workspace_identity=WORKSPACE_IDENTITY_S14,
                authorization_request=valid_authorization_request(),
            )
        (self.workspace / "docs" / "requirements").rmdir()
        (self.workspace / "docs").rmdir()
        os.symlink("/tmp", self.workspace / "escape")
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate_sprint014_smoke_workspace(
                workspace_path=self.workspace,
                workspace_identity=WORKSPACE_IDENTITY_S14,
                authorization_request=valid_authorization_request(),
            )

    def test_workspace_guard_accepts_synthetic_fixture_workspace(self):
        evidence = validate_sprint014_smoke_workspace(
            workspace_path=self.workspace,
            workspace_identity=WORKSPACE_IDENTITY_S14,
            authorization_request=valid_authorization_request(),
        )

        self.assertEqual(evidence["workspace_status"], "SYNTHETIC_WORKSPACE_ACCEPTED")
        self.assertFalse(evidence["active_vault_read"])

    def test_successful_stdio_smoke_returns_pass_and_non_authority(self):
        evidence = run_sprint014_fixed_tool_stdio_smoke(
            preflight_decision=self.preflight,
            workspace_path=self.workspace,
            timeout_seconds=5,
            output_byte_limit=4096,
        )

        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["tool_name"], "run_ast_validation")
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertFalse(evidence["source_write_allowed"])
        self.assertEqual(evidence["cleanup_status"], "CLEANED")

    def test_parse_error_returns_fail_with_bounded_output(self):
        (self.workspace / "src" / "smoke_fixture.py").write_text("def broken(:\n")

        evidence = run_sprint014_fixed_tool_stdio_smoke(
            preflight_decision=self.preflight,
            workspace_path=self.workspace,
            timeout_seconds=5,
            output_byte_limit=4096,
        )

        self.assertEqual(evidence["status"], "FAIL")
        self.assertLessEqual(evidence["output_bytes_returned"], 4096)
        self.assertIn("SyntaxError", "\n".join(evidence["output_excerpt"]))

    def test_missing_fixture_returns_blocked(self):
        (self.workspace / "src" / "smoke_fixture.py").unlink()

        evidence = run_sprint014_fixed_tool_stdio_smoke(
            preflight_decision=self.preflight,
            workspace_path=self.workspace,
            timeout_seconds=5,
            output_byte_limit=4096,
        )

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")

    def test_timeout_returns_fatal_timeout(self):
        (self.workspace / "src" / "smoke_fixture.py").write_text("SLEEP_FIXTURE = True\nSMOKE_FIXTURE = True\n")

        evidence = run_sprint014_fixed_tool_stdio_smoke(
            preflight_decision=self.preflight,
            workspace_path=self.workspace,
            timeout_seconds=1,
            output_byte_limit=4096,
        )

        self.assertEqual(evidence["status"], "FATAL_TIMEOUT")
        self.assertEqual(evidence["cleanup_status"], "CLEANED")

    def test_output_flood_returns_fatal_output_flood(self):
        (self.workspace / "src" / "smoke_fixture.py").write_text("FLOOD_FIXTURE = True\nSMOKE_FIXTURE = True\n")

        evidence = run_sprint014_fixed_tool_stdio_smoke(
            preflight_decision=self.preflight,
            workspace_path=self.workspace,
            timeout_seconds=5,
            output_byte_limit=64,
        )

        self.assertEqual(evidence["status"], "FATAL_OUTPUT_FLOOD")
        self.assertLessEqual(evidence["output_bytes_returned"], 64)

    def test_live_smoke_source_scan_rejects_unsafe_surfaces(self):
        source = Path("python/blk_test_mcp_fixed_tool_live_smoke.py").read_text()
        forbidden = [
            "shell=True", "os.system", "socket", "requests", "urllib", "http.server",
            "importlib", "pip ", "npm ", "npx ", "git commit", "git push",
        ]
        violations = [marker for marker in forbidden if marker in source]
        self.assertEqual(violations, [])
        for marker in ["docs/active", "docs/requirements", "docs/use_cases"]:
            self.assertIn(marker, source)


if __name__ == "__main__":
    unittest.main()
