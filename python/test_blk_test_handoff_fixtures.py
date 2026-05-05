import unittest
from pathlib import Path
from unittest.mock import patch

from blk_test_handoff_fixtures import (
    build_blk_test_blocked_handoff,
    build_blk_test_fail_handoff,
    build_blk_test_pass_handoff,
)


TRACE_ARTIFACTS = [
    {
        "kind": "REQ",
        "id": "REQ-DRY-001",
        "version_hash": "sha256:" + "a" * 64,
    }
]


class BlkTestHandoffFixtureTest(unittest.TestCase):
    def _success_report(self, **overrides):
        report = {
            "status": "SUCCESS",
            "beb_id": "BEB_004",
            "commit_hash": "abc123",
            "pre_engine_hash": "def456",
            "staged_files": ["dry_run_output.txt"],
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "engine_logs": "line one\nline one\nline two\n",
        }
        report.update(overrides)
        return report

    def _non_success_report(self, **overrides):
        report = self._success_report(
            status="SYNTAX_GATE_FAILED",
            commit_hash="",
            staged_files=[],
        )
        report.update(overrides)
        return report

    def test_blk_test_pass_payload_preserves_trace_artifacts(self):
        handoff = build_blk_test_pass_handoff(self._success_report())

        self.assertEqual(handoff["status"], "PASS")
        self.assertEqual(handoff["beb_id"], "BEB_004")
        self.assertEqual(handoff["commit_hash"], "abc123")
        self.assertEqual(handoff["pre_engine_hash"], "def456")
        self.assertEqual(handoff["test_profile"], "strict-ci")
        self.assertEqual(handoff["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(
            handoff["checks"],
            [
                {
                    "name": "fixture-output-present",
                    "status": "PASS",
                    "summary": "dry_run_output.txt exists",
                }
            ],
        )

    def test_blk_test_pass_payload_rejects_non_success_blk_pipe_report(self):
        with self.assertRaisesRegex(ValueError, "SUCCESS"):
            build_blk_test_pass_handoff(self._non_success_report())

    def test_blk_test_pass_payload_rejects_uppercase_trace_hash(self):
        bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:" + "A" * 64}]
        with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
            build_blk_test_pass_handoff(self._success_report(trace_artifacts=bad))

    def test_blk_test_pass_payload_rejects_non_object_trace_entry(self):
        with self.assertRaisesRegex(ValueError, "trace_artifacts"):
            build_blk_test_pass_handoff(self._success_report(trace_artifacts=["not-an-object"]))

    def test_blk_test_pass_payload_rejects_empty_trace_artifacts(self):
        with self.assertRaisesRegex(ValueError, "non-empty trace_artifacts"):
            build_blk_test_pass_handoff(self._success_report(trace_artifacts=[]))

    def test_blk_test_fail_payload_rejects_non_success_blk_pipe_report(self):
        with self.assertRaisesRegex(ValueError, "SUCCESS"):
            build_blk_test_fail_handoff(self._non_success_report())

    def test_blk_test_fail_payload_rejects_short_trace_hash(self):
        bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:abc123"}]
        with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
            build_blk_test_fail_handoff(self._success_report(trace_artifacts=bad))

    def test_blk_test_fail_payload_rejects_missing_trace_hash(self):
        bad = [{"kind": "REQ", "id": "REQ-DRY-001"}]
        with self.assertRaisesRegex(ValueError, "version_hash"):
            build_blk_test_fail_handoff(self._success_report(trace_artifacts=bad))

    def test_blk_test_blocked_payload_handles_non_success_blk_pipe_report(self):
        handoff = build_blk_test_blocked_handoff(self._non_success_report())

        self.assertEqual(handoff["status"], "BLOCKED")
        self.assertEqual(handoff["beb_id"], "BEB_004")
        self.assertEqual(handoff["commit_hash"], "")
        self.assertEqual(handoff["pre_engine_hash"], "def456")
        self.assertEqual(handoff["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(handoff["checks"][0]["status"], "BLOCKED")
        self.assertIn("BLK-test did not run", handoff["checks"][0]["summary"])

    def test_blk_test_blocked_payload_records_trace_absence_reason_when_absent(self):
        handoff = build_blk_test_blocked_handoff(self._non_success_report(trace_artifacts=[]))

        self.assertEqual(handoff["status"], "BLOCKED")
        self.assertEqual(handoff["trace_artifacts"], [])
        self.assertEqual(
            handoff["trace_absence_reason"],
            "source report did not include decoded trace_artifacts",
        )

    def test_blk_test_blocked_payload_rejects_malformed_trace_when_present(self):
        bad = [{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "sha256:" + "g" * 64}]
        with self.assertRaisesRegex(ValueError, "sha256:<64-lowercase-hex>"):
            build_blk_test_blocked_handoff(self._non_success_report(trace_artifacts=bad))

    def test_blk_test_blocked_payload_rejects_non_object_trace_entry_when_present(self):
        with self.assertRaisesRegex(ValueError, "trace_artifacts"):
            build_blk_test_blocked_handoff(self._non_success_report(trace_artifacts=["not-an-object"]))

    def test_blk_test_blocked_payload_handles_fatal_output_flood_report(self):
        handoff = build_blk_test_blocked_handoff(
            self._non_success_report(
                status="FATAL_OUTPUT_FLOOD",
                engine_logs="engine output exceeded max_output_bytes",
            )
        )

        self.assertEqual(handoff["status"], "BLOCKED")
        self.assertEqual(handoff["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertIn("FATAL_OUTPUT_FLOOD", handoff["checks"][0]["summary"])
        self.assertIn("engine output exceeded", handoff["compressed_logs"])

    def test_blk_test_blocked_payload_handles_all_known_non_success_statuses(self):
        known_non_success_statuses = [
            "FATAL_SYSTEM_PANIC",
            "FATAL_ENGINE_FAILED",
            "INVALID_PAYLOAD",
            "SYNTAX_GATE_FAILED",
            "UNAUTHORIZED_FILE_MUTATION",
            "INVALID_REVERT_ANCHOR",
            "FATAL_OUTPUT_FLOOD",
            "ENGINE_TIMEOUT",
            "GIT_DIRTY",
            "INTERNAL_ERROR",
            "FATAL_CRASH",
            "FATAL_PYTHON_TIMEOUT",
        ]

        for status in known_non_success_statuses:
            with self.subTest(status=status):
                handoff = build_blk_test_blocked_handoff(self._non_success_report(status=status))
                self.assertEqual(handoff["status"], "BLOCKED")
                self.assertEqual(handoff["trace_artifacts"], TRACE_ARTIFACTS)
                self.assertIn(status, handoff["checks"][0]["summary"])

    def test_blk_test_fixture_rejects_legacy_output_flood_status(self):
        with self.assertRaisesRegex(ValueError, "unknown BLK-pipe status: OUTPUT_FLOOD"):
            build_blk_test_blocked_handoff(self._non_success_report(status="OUTPUT_FLOOD"))

    def test_blk_test_pass_payload_rejects_missing_commit_hash(self):
        with self.assertRaisesRegex(ValueError, "commit_hash"):
            build_blk_test_pass_handoff(self._success_report(commit_hash=""))

    def test_blk_test_pass_payload_requires_expected_staged_file(self):
        with self.assertRaisesRegex(ValueError, "dry_run_output.txt"):
            build_blk_test_pass_handoff(self._success_report(staged_files=["other.txt"]))

    def test_blk_test_fail_payload_preserves_trace_artifacts_when_present(self):
        handoff = build_blk_test_fail_handoff(self._success_report())

        self.assertEqual(handoff["status"], "FAIL")
        self.assertEqual(handoff["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(handoff["checks"][0]["status"], "FAIL")
        self.assertEqual(handoff["checks"][0]["summary"], "dry_run_output.txt missing")

    def test_blk_test_fail_payload_uses_fail_status_and_bounded_logs(self):
        long_logs = "alpha\n" * 400
        handoff = build_blk_test_fail_handoff(self._success_report(engine_logs=long_logs), max_log_bytes=64)

        self.assertEqual(handoff["status"], "FAIL")
        self.assertLessEqual(len(handoff["compressed_logs"].encode("utf-8")), 64)
        self.assertIn("alpha", handoff["compressed_logs"])

    def test_blk_test_fixture_rejects_unknown_status(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            build_blk_test_pass_handoff(self._success_report(status="MAYBE"))

    def test_blk_test_fixture_does_not_read_active_vault(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            handoff = build_blk_test_pass_handoff(self._success_report())

        self.assertEqual(handoff["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
