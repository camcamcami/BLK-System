import unittest

from blk_test_mcp_approval_authorization import (
    build_authorization_request,
    validate_blk_test_approval_record,
)

TRACE_A = {
    "kind": "REQ",
    "id": "REQ-S13-001",
    "version_hash": "sha256:" + "a" * 64,
}
SOURCE_REPORT_IDENTITY = {
    "report_path": "reports/BEB_013/source-report.json",
    "report_hash": "sha256:" + "b" * 64,
    "report_id": "source-report-BEB_013",
}
WORKSPACE_IDENTITY = {
    "target_branch": "sprint/blk-system-013-fixture",
    "workspace_clone_id": "workspace-BEB_013-run-001",
    "source_path_policy": "isolated-copy-only",
}
TIMEOUT_OUTPUT_PROFILE = {
    "timeout_class": "bounded-short",
    "timeout_seconds": 30,
    "output_byte_limit": 8192,
    "compression": "line-dedupe-byte-bound",
}
NOW = "2026-05-06T10:05:00Z"


def valid_source_report():
    return {
        "status": "SUCCESS",
        "source_report_identity": dict(SOURCE_REPORT_IDENTITY),
        "beb_id": "BEB_013",
        "commit_hash": "abc123def456",
        "pre_engine_hash": "sha256:" + "c" * 64,
        "trace_artifacts": [dict(TRACE_A)],
        "staged_files": ["dry_run_output.txt"],
    }


def valid_request():
    return build_authorization_request(
        source_report=valid_source_report(),
        requested_tools=["run_ast_validation"],
        test_profile="strict-ci",
        workspace_identity=dict(WORKSPACE_IDENTITY),
        timeout_output_profile=dict(TIMEOUT_OUTPUT_PROFILE),
    )


def valid_approval_record(request=None):
    request = request or valid_request()
    return {
        "approval_kind": "blk-test-mcp",
        "approval_id": "BLKTEST-S13-APPROVAL-001",
        "operator_identity": "operator:camcamcami",
        "approval_timestamp": "2026-05-06T10:01:00Z",
        "issued_at": "2026-05-06T10:00:00Z",
        "expires_at": "2026-05-06T10:15:00Z",
        "source_evidence": dict(request["source_evidence"]),
        "requested_tools": list(request["requested_tools"]),
        "test_profile": request["test_profile"],
        "workspace_identity": dict(request["workspace_identity"]),
        "timeout_output_profile": dict(request["timeout_output_profile"]),
    }


class ApprovalRecordSchemaTest(unittest.TestCase):
    def test_valid_record_normalizes_required_fields_without_live_authority(self):
        request = valid_request()
        decision = validate_blk_test_approval_record(
            valid_approval_record(request),
            request,
            now=NOW,
        )

        self.assertEqual(decision["decision"], "APPROVAL_VALIDATED_SOURCE_BOUND")
        self.assertEqual(decision["approval_id"], "BLKTEST-S13-APPROVAL-001")
        self.assertEqual(decision["operator_identity"], "operator:camcamcami")
        self.assertFalse(decision["live_mcp_authorized"])
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertFalse(decision["network_called"])
        self.assertFalse(decision["subprocess_called"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertFalse(decision["source_write_allowed"])
        self.assertFalse(decision["staging_allowed"])
        self.assertFalse(decision["commit_allowed"])
        self.assertFalse(decision["push_allowed"])
        self.assertFalse(decision["active_vault_read"])
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")

    def test_missing_operator_identity_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval.pop("operator_identity")

        with self.assertRaisesRegex(ValueError, "operator_identity"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_missing_approval_timestamp_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval.pop("approval_timestamp")

        with self.assertRaisesRegex(ValueError, "approval_timestamp"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_missing_approval_id_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval.pop("approval_id")

        with self.assertRaisesRegex(ValueError, "approval_id"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_codex_live_approval_kind_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval["approval_kind"] = "codex-live"

        with self.assertRaisesRegex(ValueError, "codex-live"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_codex_live_token_text_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval["approval_token"] = "BLK_APPROVE_CODEX_LIVE beb_id=BEB_013"

        with self.assertRaisesRegex(ValueError, "codex-live"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_unknown_or_wildcard_requested_tools_reject(self):
        for tools in (["run_ast_validation", "run_unknown"], ["*"], ["shell"]):
            with self.subTest(tools=tools):
                with self.assertRaisesRegex(ValueError, "requested_tools"):
                    build_authorization_request(
                        source_report=valid_source_report(),
                        requested_tools=tools,
                        workspace_identity=dict(WORKSPACE_IDENTITY),
                        timeout_output_profile=dict(TIMEOUT_OUTPUT_PROFILE),
                    )

    def test_protected_vault_body_reference_rejects(self):
        source = valid_source_report()
        source["source_report_identity"]["protected_body_path"] = "docs/active/REQ.md"

        with self.assertRaisesRegex(ValueError, "protected"):
            build_authorization_request(
                source_report=source,
                requested_tools=["run_ast_validation"],
                workspace_identity=dict(WORKSPACE_IDENTITY),
                timeout_output_profile=dict(TIMEOUT_OUTPUT_PROFILE),
            )


if __name__ == "__main__":
    unittest.main()
