import unittest
from copy import deepcopy

from blk_orchestrator_gate import (
    approval_token_for,
    build_blk_test_mcp_request,
    evaluate_profile_gate,
    map_blk_test_mcp_response,
    send_blk_test_mcp_request,
)


TRACE_HASH = "sha256:" + "a" * 64
APPROVAL_TOKEN = approval_token_for(
    beb_id="BEB_006",
    target_branch="sprint/blk-pipe-006",
    trace_hash=TRACE_HASH,
)


def source_report(status="SUCCESS"):
    return {
        "status": status,
        "beb_id": "BEB_005",
        "commit_hash": "abc123" if status == "SUCCESS" else "",
        "pre_engine_hash": "def456",
        "staged_files": ["dry_run_output.txt"] if status == "SUCCESS" else [],
        "trace_artifacts": [
            {
                "kind": "REQ",
                "id": "REQ-DRY-001",
                "version_hash": TRACE_HASH,
            }
        ],
    }


def mcp_response_for(source_request, status="PASS", checks=None):
    if checks is None:
        checks = [
            {
                "name": "fixture-output-present",
                "status": status,
                "summary": "deterministic fixture check",
            }
        ]
    return {
        "status": status,
        "beb_id": source_request["beb_id"],
        "commit_hash": source_request["commit_hash"],
        "pre_engine_hash": source_request["pre_engine_hash"],
        "trace_artifacts": deepcopy(source_request["trace_artifacts"]),
        "checks": deepcopy(checks),
    }


class OrchestratorProfileGateTest(unittest.TestCase):
    def test_profile_gate_allows_dry_run_profiles(self):
        for profile in ["dev-smoke", "strict-ci", "codex-dry-run"]:
            with self.subTest(profile=profile):
                decision = evaluate_profile_gate(
                    profile,
                    beb_id="BEB_006",
                    target_branch="sprint/blk-pipe-006",
                    trace_hash=TRACE_HASH,
                )
                self.assertTrue(decision.allowed)
                self.assertFalse(decision.live_execution_authorized)
                self.assertFalse(decision.approval_recorded)
                self.assertEqual(decision.decision, "ALLOWED_LOCAL_ONLY")

    def test_profile_gate_rejects_codex_live_without_token(self):
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertFalse(decision.approval_recorded)
        self.assertEqual(decision.decision, "BLOCKED_APPROVAL_REQUIRED")
        self.assertIn("approval token", decision.reason)

    def test_codex_live_exact_token_records_approval_but_is_not_allowed(self):
        approval_token = approval_token_for(
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
        )
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
            approval_token=approval_token,
        )

        self.assertEqual(decision.decision, "APPROVED_BUT_NOT_EXECUTED")
        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertTrue(decision.approval_recorded)
        self.assertIn("Sprint 006", decision.reason)

    def test_profile_gate_rejects_codex_live_mismatched_token(self):
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN.replace("BEB_006", "BEB_OTHER"),
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertFalse(decision.approval_recorded)
        self.assertEqual(decision.decision, "BLOCKED_APPROVAL_MISMATCH")

    def test_profile_gate_always_rejects_cyber_execution_in_sprint_006(self):
        decision = evaluate_profile_gate(
            "cyber-execution",
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN,
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertFalse(decision.approval_recorded)
        self.assertEqual(decision.decision, "BLOCKED_CYBER_EXECUTION")

    def test_profile_gate_rejects_unknown_profile(self):
        decision = evaluate_profile_gate(
            "unknown-profile",
            beb_id="BEB_006",
            target_branch="sprint/blk-pipe-006",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN,
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertFalse(decision.approval_recorded)
        self.assertEqual(decision.decision, "BLOCKED_UNKNOWN_PROFILE")


class OrchestratorBlkTestMcpStubTest(unittest.TestCase):
    def test_build_blk_test_mcp_request_is_disabled_by_default(self):
        request = build_blk_test_mcp_request(source_report())

        self.assertFalse(request["enabled"])
        self.assertEqual(request["transport"], "DISABLED_STUB")
        self.assertEqual(request["source_status"], "SUCCESS")
        self.assertEqual(request["beb_id"], "BEB_005")
        self.assertEqual(request["rtm_status"], "NOT_GENERATED")
        self.assertEqual(request["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(request["trace_artifacts"], source_report()["trace_artifacts"])

    def test_build_blk_test_mcp_request_rejects_enabled_live_path(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            build_blk_test_mcp_request(source_report(), enabled=True)

    def test_build_blk_test_mcp_request_rejects_missing_source_evidence(self):
        cases = [
            ("status", "status"),
            ("beb_id", "beb_id"),
            ("pre_engine_hash", "pre_engine_hash"),
            ("trace_artifacts", "trace_artifacts"),
        ]
        for field, pattern in cases:
            with self.subTest(field=field):
                report = source_report()
                if field == "trace_artifacts":
                    report[field] = []
                else:
                    report[field] = ""

                with self.assertRaisesRegex(ValueError, pattern):
                    build_blk_test_mcp_request(report)

    def test_build_blk_test_mcp_request_rejects_unknown_source_status(self):
        report = source_report()
        report["status"] = "OUTPUT_FLOOD"

        with self.assertRaisesRegex(ValueError, "unknown BLK-pipe status"):
            build_blk_test_mcp_request(report)

    def test_build_blk_test_mcp_request_rejects_success_without_execution_evidence(self):
        cases = [
            ("commit_hash", "commit_hash", ""),
            ("staged_files", "staged_files", []),
        ]
        for field, pattern, value in cases:
            with self.subTest(field=field):
                report = source_report()
                report[field] = value

                with self.assertRaisesRegex(ValueError, pattern):
                    build_blk_test_mcp_request(report)

    def test_blk_test_mcp_request_rejects_non_success_as_evaluation_request(self):
        with self.assertRaisesRegex(ValueError, "status SUCCESS"):
            build_blk_test_mcp_request(source_report("SYNTAX_GATE_FAILED"))

    def test_blk_test_mcp_request_rejects_short_trace_hash(self):
        report = source_report()
        report["trace_artifacts"][0]["version_hash"] = "sha256:0123456789abcdef"

        with self.assertRaisesRegex(ValueError, "version_hash"):
            build_blk_test_mcp_request(report)

    def test_blk_test_mcp_stub_does_not_call_network_or_subprocess(self):
        request = build_blk_test_mcp_request(source_report())
        response = send_blk_test_mcp_request(request)

        self.assertEqual(response["status"], "BLOCKED")
        self.assertIn("live BLK-test MCP disabled", response["reason"])
        self.assertFalse(response["network_called"])
        self.assertFalse(response["subprocess_called"])

    def test_blk_test_mcp_response_mapping_requires_source_request(self):
        with self.assertRaises(TypeError):
            map_blk_test_mcp_response({"status": "PASS", "beb_id": "BEB_005"})

    def test_blk_test_mcp_response_mapping_accepts_future_fixture_statuses(self):
        source_request = build_blk_test_mcp_request(source_report())
        for status in ["PASS", "FAIL", "BLOCKED"]:
            with self.subTest(status=status):
                mapped = map_blk_test_mcp_response(
                    mcp_response_for(source_request, status=status),
                    source_request=source_request,
                )
                self.assertEqual(mapped["status"], status)
                self.assertEqual(mapped["source"], "blk-test-mcp-response-shape")
                self.assertEqual(mapped["beb_id"], source_request["beb_id"])
                self.assertEqual(mapped["commit_hash"], source_request["commit_hash"])
                self.assertEqual(mapped["pre_engine_hash"], source_request["pre_engine_hash"])
                self.assertEqual(mapped["trace_artifacts"], source_request["trace_artifacts"])
                self.assertEqual(mapped["rtm_status"], "NOT_GENERATED")

    def test_blk_test_mcp_response_mapping_rejects_pass_without_trace_artifacts(self):
        source_request = build_blk_test_mcp_request(source_report())
        response = mcp_response_for(source_request, status="PASS")
        response.pop("trace_artifacts")

        with self.assertRaisesRegex(ValueError, "trace_artifacts"):
            map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_rejects_trace_artifact_mismatch(self):
        source_request = build_blk_test_mcp_request(source_report())
        response = mcp_response_for(source_request, status="PASS")
        response["trace_artifacts"] = [
            {
                "kind": "REQ",
                "id": "REQ-OTHER",
                "version_hash": TRACE_HASH,
            }
        ]

        with self.assertRaisesRegex(ValueError, "trace_artifacts"):
            map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_rejects_pass_without_checks(self):
        source_request = build_blk_test_mcp_request(source_report())
        response = mcp_response_for(source_request, status="PASS", checks=[])

        with self.assertRaisesRegex(ValueError, "checks"):
            map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_rejects_source_evidence_mismatch(self):
        cases = [
            ("beb_id", "BEB_OTHER"),
            ("commit_hash", "other-commit"),
            ("pre_engine_hash", "other-pre-engine"),
        ]
        for field, value in cases:
            with self.subTest(field=field):
                source_request = build_blk_test_mcp_request(source_report())
                response = mcp_response_for(source_request, status="FAIL")
                response[field] = value

                with self.assertRaisesRegex(ValueError, field):
                    map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_rejects_pass_when_source_never_succeeded(self):
        source_request = build_blk_test_mcp_request(source_report())
        source_request["source_status"] = "SYNTAX_GATE_FAILED"
        source_request["method"] = "blk_test.not_run"
        response = mcp_response_for(source_request, status="PASS")

        with self.assertRaisesRegex(ValueError, "source_status SUCCESS"):
            map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_blocked_preserves_source_trace_artifacts(self):
        source_request = build_blk_test_mcp_request(source_report())
        source_request["source_status"] = "SYNTAX_GATE_FAILED"
        source_request["method"] = "blk_test.not_run"
        source_request["commit_hash"] = ""
        source_request["staged_files"] = []
        response = {
            "status": "BLOCKED",
            "beb_id": "BEB_OTHER",
            "pre_engine_hash": "other-pre-engine",
            "trace_artifacts": [],
        }

        mapped = map_blk_test_mcp_response(response, source_request=source_request)

        self.assertEqual(mapped["status"], "BLOCKED")
        self.assertEqual(mapped["beb_id"], source_request["beb_id"])
        self.assertEqual(mapped["commit_hash"], "")
        self.assertEqual(mapped["pre_engine_hash"], source_request["pre_engine_hash"])
        self.assertEqual(mapped["trace_artifacts"], source_request["trace_artifacts"])

    def test_blk_test_mcp_response_mapping_rejects_uppercase_trace_hash(self):
        source_request = build_blk_test_mcp_request(source_report())
        response = {
            "status": "PASS",
            "beb_id": "BEB_005",
            "commit_hash": source_request["commit_hash"],
            "pre_engine_hash": source_request["pre_engine_hash"],
            "trace_artifacts": source_report()["trace_artifacts"],
            "checks": [{"name": "fixture-output-present", "status": "PASS"}],
        }
        response["trace_artifacts"][0]["version_hash"] = "sha256:" + "A" * 64

        with self.assertRaisesRegex(ValueError, "version_hash"):
            map_blk_test_mcp_response(response, source_request=source_request)

    def test_blk_test_mcp_response_mapping_rejects_unknown_status(self):
        source_request = build_blk_test_mcp_request(source_report())
        with self.assertRaisesRegex(ValueError, "unknown BLK-test MCP response status"):
            map_blk_test_mcp_response({"status": "AUTHORITY_PUBLISHED"}, source_request=source_request)


if __name__ == "__main__":
    unittest.main()
