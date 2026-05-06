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


if __name__ == "__main__":
    unittest.main()
