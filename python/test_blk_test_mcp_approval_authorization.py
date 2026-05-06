import json
import unittest
from copy import deepcopy

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
        "source_evidence": deepcopy(request["source_evidence"]),
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


class ApprovalSourceBindingTest(unittest.TestCase):
    def assert_rejects_approval_mutation(self, mutator, marker):
        request = valid_request()
        approval = valid_approval_record(request)
        mutator(approval)

        with self.assertRaisesRegex(ValueError, marker):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_rejects_mismatched_beb_id(self):
        self.assert_rejects_approval_mutation(
            lambda approval: approval["source_evidence"].update({"beb_id": "BEB_999"}),
            "beb_id",
        )

    def test_rejects_mismatched_commit_hash(self):
        self.assert_rejects_approval_mutation(
            lambda approval: approval["source_evidence"].update({"commit_hash": "deadbeef"}),
            "commit_hash",
        )

    def test_rejects_mismatched_pre_engine_hash(self):
        self.assert_rejects_approval_mutation(
            lambda approval: approval["source_evidence"].update(
                {"pre_engine_hash": "sha256:" + "d" * 64}
            ),
            "pre_engine_hash",
        )

    def test_rejects_mismatched_trace_artifacts(self):
        def mutate(approval):
            approval["source_evidence"]["trace_artifacts"] = [
                {"kind": "REQ", "id": "REQ-S13-001", "version_hash": "sha256:" + "e" * 64}
            ]

        self.assert_rejects_approval_mutation(mutate, "trace_artifacts")

    def test_rejects_mismatched_source_report_identity(self):
        def mutate(approval):
            approval["source_evidence"]["source_report_identity"]["report_hash"] = "sha256:" + "f" * 64

        self.assert_rejects_approval_mutation(mutate, "source_report_identity")

    def test_rejects_extra_requested_tool(self):
        self.assert_rejects_approval_mutation(
            lambda approval: approval["requested_tools"].append("run_architecture_lint"),
            "requested_tools",
        )

    def test_rejects_mismatched_test_profile(self):
        self.assert_rejects_approval_mutation(
            lambda approval: approval.update({"test_profile": "dev-smoke"}),
            "test_profile",
        )

    def test_rejects_mismatched_workspace_identity(self):
        def mutate(approval):
            approval["workspace_identity"]["workspace_clone_id"] = "other-workspace"

        self.assert_rejects_approval_mutation(mutate, "workspace_identity")

    def test_rejects_mismatched_timeout_output_profile(self):
        def mutate(approval):
            approval["timeout_output_profile"]["output_byte_limit"] = 4096

        self.assert_rejects_approval_mutation(mutate, "timeout_output_profile")

    def test_rejects_authority_like_fields_in_approval(self):
        for field in ("shell", "command", "exec", "eval", "source_mutation", "publish_beo", "generate_rtm"):
            with self.subTest(field=field):
                self.assert_rejects_approval_mutation(
                    lambda approval, field=field: approval.update({field: True}),
                    field,
                )


class ApprovalReplayAuditTest(unittest.TestCase):
    def test_expired_approval_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval["expires_at"] = "2026-05-06T10:04:59Z"

        with self.assertRaisesRegex(ValueError, "expired"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_replayed_approval_id_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)

        with self.assertRaisesRegex(ValueError, "replay"):
            validate_blk_test_approval_record(
                approval,
                request,
                now=NOW,
                used_approval_ids={"BLKTEST-S13-APPROVAL-001"},
            )

    def test_malformed_timestamp_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval["approval_timestamp"] = "not-a-timestamp"

        with self.assertRaisesRegex(ValueError, "approval_timestamp"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_missing_expires_at_rejects(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval.pop("expires_at")

        with self.assertRaisesRegex(ValueError, "expires_at"):
            validate_blk_test_approval_record(approval, request, now=NOW)

    def test_approval_record_hash_is_stable_across_key_order(self):
        request = valid_request()
        approval_a = valid_approval_record(request)
        approval_b = dict(reversed(list(approval_a.items())))

        decision_a = validate_blk_test_approval_record(approval_a, request, now=NOW)
        decision_b = validate_blk_test_approval_record(approval_b, request, now=NOW)

        self.assertEqual(decision_a["approval_record_hash"], decision_b["approval_record_hash"])
        self.assertRegex(decision_a["approval_record_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(decision_a["authorization_request_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(decision_a["source_evidence_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_source_evidence_hash_changes_when_source_evidence_changes(self):
        request_a = valid_request()
        decision_a = validate_blk_test_approval_record(valid_approval_record(request_a), request_a, now=NOW)

        source_b = valid_source_report()
        source_b["trace_artifacts"] = [
            {"kind": "REQ", "id": "REQ-S13-002", "version_hash": "sha256:" + "d" * 64}
        ]
        request_b = build_authorization_request(
            source_report=source_b,
            requested_tools=["run_ast_validation"],
            test_profile="strict-ci",
            workspace_identity=dict(WORKSPACE_IDENTITY),
            timeout_output_profile=dict(TIMEOUT_OUTPUT_PROFILE),
        )
        decision_b = validate_blk_test_approval_record(valid_approval_record(request_b), request_b, now=NOW)

        self.assertNotEqual(decision_a["source_evidence_hash"], decision_b["source_evidence_hash"])

    def test_audit_evidence_omits_raw_secret_values(self):
        request = valid_request()
        approval = valid_approval_record(request)
        approval["audit_note"] = "contains redacted context only"
        decision = validate_blk_test_approval_record(approval, request, now=NOW)
        serialized = json.dumps(decision, sort_keys=True)

        self.assertNotIn("BLK_APPROVE_CODEX_LIVE", serialized)
        self.assertNotIn("docs/active/REQ.md", serialized)
        self.assertNotIn("secret", serialized.lower())


if __name__ == "__main__":
    unittest.main()
