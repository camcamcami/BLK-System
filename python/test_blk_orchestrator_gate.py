import unittest

from blk_orchestrator_gate import (
    build_blk_test_mcp_request,
    evaluate_profile_gate,
    map_blk_test_mcp_response,
    send_blk_test_mcp_request,
)


TRACE_HASH = "sha256:" + "a" * 64
APPROVAL_TOKEN = (
    "BLK_APPROVE_CODEX_LIVE "
    "beb_id=BEB_005 target_branch=sprint/blk-pipe-005 trace_hash=" + TRACE_HASH
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


class OrchestratorProfileGateTest(unittest.TestCase):
    def test_profile_gate_allows_dry_run_profiles(self):
        for profile in ["dev-smoke", "strict-ci", "codex-dry-run"]:
            with self.subTest(profile=profile):
                decision = evaluate_profile_gate(
                    profile,
                    beb_id="BEB_005",
                    target_branch="sprint/blk-pipe-005",
                    trace_hash=TRACE_HASH,
                )
                self.assertTrue(decision.allowed)
                self.assertFalse(decision.live_execution_authorized)
                self.assertEqual(decision.decision, "ALLOWED_LOCAL_ONLY")

    def test_profile_gate_rejects_codex_live_without_token(self):
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_005",
            target_branch="sprint/blk-pipe-005",
            trace_hash=TRACE_HASH,
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertEqual(decision.decision, "BLOCKED_APPROVAL_REQUIRED")
        self.assertIn("approval token", decision.reason)

    def test_profile_gate_accepts_codex_live_token_but_does_not_execute(self):
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_005",
            target_branch="sprint/blk-pipe-005",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN,
        )

        self.assertTrue(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertEqual(decision.decision, "APPROVED_BUT_NOT_EXECUTED")
        self.assertIn("Sprint 005", decision.reason)

    def test_profile_gate_rejects_codex_live_mismatched_token(self):
        decision = evaluate_profile_gate(
            "codex-live",
            beb_id="BEB_005",
            target_branch="sprint/blk-pipe-005",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN.replace("BEB_005", "BEB_OTHER"),
        )

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.decision, "BLOCKED_APPROVAL_MISMATCH")

    def test_profile_gate_always_rejects_cyber_execution_in_sprint_005(self):
        decision = evaluate_profile_gate(
            "cyber-execution",
            beb_id="BEB_005",
            target_branch="sprint/blk-pipe-005",
            trace_hash=TRACE_HASH,
            approval_token=APPROVAL_TOKEN,
        )

        self.assertFalse(decision.allowed)
        self.assertFalse(decision.live_execution_authorized)
        self.assertEqual(decision.decision, "BLOCKED_CYBER_EXECUTION")


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
        with self.assertRaisesRegex(RuntimeError, "disabled in Sprint 005"):
            build_blk_test_mcp_request(source_report(), enabled=True)

    def test_blk_test_mcp_stub_does_not_call_network_or_subprocess(self):
        request = build_blk_test_mcp_request(source_report("SYNTAX_GATE_FAILED"))
        response = send_blk_test_mcp_request(request)

        self.assertEqual(response["status"], "BLOCKED")
        self.assertEqual(response["reason"], "live BLK-test MCP disabled in Sprint 005")
        self.assertFalse(response["network_called"])
        self.assertFalse(response["subprocess_called"])

    def test_blk_test_mcp_response_mapping_accepts_future_fixture_statuses(self):
        for status in ["PASS", "FAIL", "BLOCKED"]:
            with self.subTest(status=status):
                mapped = map_blk_test_mcp_response(
                    {
                        "status": status,
                        "beb_id": "BEB_005",
                        "trace_artifacts": source_report()["trace_artifacts"],
                    }
                )
                self.assertEqual(mapped["status"], status)
                self.assertEqual(mapped["source"], "blk-test-mcp-response-shape")
                self.assertEqual(mapped["rtm_status"], "NOT_GENERATED")

    def test_blk_test_mcp_response_mapping_rejects_unknown_status(self):
        with self.assertRaisesRegex(ValueError, "unknown BLK-test MCP response status"):
            map_blk_test_mcp_response({"status": "AUTHORITY_PUBLISHED"})


if __name__ == "__main__":
    unittest.main()
