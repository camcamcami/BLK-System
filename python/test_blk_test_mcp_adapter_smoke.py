import unittest
from copy import deepcopy

from blk_orchestrator_gate import build_blk_test_mcp_request
from blk_test_mcp_adapter_smoke import run_disabled_blk_test_mcp_adapter_smoke


TRACE_HASH = "sha256:" + "a" * 64
TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-DRY-001",
        "version_hash": TRACE_HASH,
    }
]


def success_report(**overrides):
    report = {
        "status": "SUCCESS",
        "beb_id": "BEB_007",
        "commit_hash": "abc123",
        "pre_engine_hash": "def456",
        "staged_files": ["dry_run_output.txt"],
        "destroyed_files": [],
        "trace_artifacts": deepcopy(TRACE_ARTIFACTS),
    }
    report.update(overrides)
    return report


def non_success_report(status="SYNTAX_GATE_FAILED", **overrides):
    report = {
        "status": status,
        "beb_id": "BEB_007",
        "commit_hash": "",
        "pre_engine_hash": "def456",
        "staged_files": [],
        "destroyed_files": [],
        "trace_artifacts": deepcopy(TRACE_ARTIFACTS),
    }
    report.update(overrides)
    return report


def pass_response_for(source_request, **overrides):
    response = {
        "status": "PASS",
        "beb_id": source_request["beb_id"],
        "commit_hash": source_request["commit_hash"],
        "pre_engine_hash": source_request["pre_engine_hash"],
        "trace_artifacts": deepcopy(source_request["trace_artifacts"]),
        "checks": [
            {
                "name": "fixture-output-present",
                "status": "PASS",
                "summary": "deterministic fixture check",
            }
        ],
    }
    response.update(overrides)
    return response


class DisabledBlkTestMcpAdapterSmokeTest(unittest.TestCase):
    def test_disabled_adapter_smoke_without_response_blocks_send_only(self):
        result = run_disabled_blk_test_mcp_adapter_smoke(success_report())

        self.assertEqual(result["adapter_status"], "DISABLED_SEND_BLOCKED")
        self.assertEqual(result["source"], "disabled-blk-test-mcp-adapter-smoke")
        self.assertEqual(result["transport"], "DISABLED_STUB")
        self.assertEqual(result["request"]["method"], "blk_test.evaluate_execution")
        self.assertEqual(result["request"]["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(result["send_result"]["status"], "BLOCKED")
        self.assertFalse(result["network_called"])
        self.assertFalse(result["subprocess_called"])
        self.assertEqual(result["rtm_status"], "NOT_GENERATED")
        self.assertEqual(result["beo_publication"], "DRAFT_ONLY")
        self.assertNotIn("mapped_response", result)

    def test_disabled_adapter_smoke_builds_not_run_request_for_non_success_without_response(self):
        result = run_disabled_blk_test_mcp_adapter_smoke(non_success_report())

        self.assertEqual(result["adapter_status"], "DISABLED_SEND_BLOCKED")
        self.assertEqual(result["request"]["method"], "blk_test.not_run")
        self.assertEqual(result["request"]["source_status"], "SYNTAX_GATE_FAILED")
        self.assertEqual(result["request"]["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(result["request"]["rtm_status"], "NOT_GENERATED")
        self.assertEqual(result["request"]["beo_publication"], "DRAFT_ONLY")
        self.assertFalse(result["network_called"])
        self.assertFalse(result["subprocess_called"])
        self.assertNotIn("mapped_response", result)

    def test_disabled_adapter_smoke_maps_not_run_source_only_to_blocked_fixture(self):
        result = run_disabled_blk_test_mcp_adapter_smoke(
            non_success_report(),
            response_fixture={"status": "BLOCKED"},
        )

        self.assertEqual(result["adapter_status"], "FIXTURE_RESPONSE_MAPPED")
        self.assertEqual(result["request"]["method"], "blk_test.not_run")
        self.assertEqual(result["mapped_response"]["status"], "BLOCKED")
        self.assertEqual(result["mapped_response"]["commit_hash"], "")
        self.assertEqual(result["mapped_response"]["trace_artifacts"], TRACE_ARTIFACTS)

    def test_disabled_adapter_smoke_rejects_not_run_pass_fixture(self):
        response = {
            "status": "PASS",
            "beb_id": "BEB_007",
            "commit_hash": "",
            "pre_engine_hash": "def456",
            "trace_artifacts": deepcopy(TRACE_ARTIFACTS),
            "checks": [{"name": "fixture-output-present", "status": "PASS"}],
        }

        with self.assertRaisesRegex(ValueError, "source_status SUCCESS"):
            run_disabled_blk_test_mcp_adapter_smoke(non_success_report(), response_fixture=response)

    def test_disabled_adapter_smoke_maps_source_bound_pass_fixture(self):
        report = success_report()
        request = build_blk_test_mcp_request(report)
        response = pass_response_for(request)

        result = run_disabled_blk_test_mcp_adapter_smoke(report, response_fixture=response)

        self.assertEqual(result["adapter_status"], "FIXTURE_RESPONSE_MAPPED")
        self.assertEqual(result["mapped_response"]["status"], "PASS")
        self.assertEqual(result["mapped_response"]["beb_id"], report["beb_id"])
        self.assertEqual(result["mapped_response"]["commit_hash"], report["commit_hash"])
        self.assertEqual(result["mapped_response"]["pre_engine_hash"], report["pre_engine_hash"])
        self.assertEqual(result["mapped_response"]["trace_artifacts"], report["trace_artifacts"])
        self.assertFalse(result["network_called"])
        self.assertFalse(result["subprocess_called"])

    def test_disabled_adapter_smoke_maps_source_bound_fail_fixture(self):
        report = success_report()
        request = build_blk_test_mcp_request(report)
        response = pass_response_for(
            request,
            status="FAIL",
            checks=[
                {
                    "name": "fixture-output-present",
                    "status": "FAIL",
                    "summary": "deterministic fixture failed",
                }
            ],
        )

        result = run_disabled_blk_test_mcp_adapter_smoke(report, response_fixture=response)

        self.assertEqual(result["adapter_status"], "FIXTURE_RESPONSE_MAPPED")
        self.assertEqual(result["mapped_response"]["status"], "FAIL")
        self.assertEqual(result["mapped_response"]["trace_artifacts"], report["trace_artifacts"])

    def test_disabled_adapter_smoke_rejects_response_source_mismatch(self):
        report = success_report()
        request = build_blk_test_mcp_request(report)
        response = pass_response_for(request)
        response["beb_id"] = "BEB_OTHER"

        with self.assertRaisesRegex(ValueError, "beb_id"):
            run_disabled_blk_test_mcp_adapter_smoke(report, response_fixture=response)

    def test_disabled_adapter_smoke_rejects_enabled_live_path(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            run_disabled_blk_test_mcp_adapter_smoke(success_report(), enabled=True)


if __name__ == "__main__":
    unittest.main()
