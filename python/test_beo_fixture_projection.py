import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from beo_fixture_projection import (
    project_blk_test_handoff_to_beo,
    project_live_smoke_evidence_to_draft_beo,
    project_mapped_mcp_response_to_beo,
)
from blk_pipe_dry_run_orchestrator import (
    invoke_blk_pipe_dry_run_fixture,
    run_blk_pipe_dry_run_fixture,
)
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


class BeoFixtureProjectionTest(unittest.TestCase):
    def _blk_test_pass(self, **overrides):
        handoff = {
            "status": "PASS",
            "beb_id": "BEB_004",
            "commit_hash": "abc123",
            "pre_engine_hash": "def456",
            "test_profile": "strict-ci",
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "checks": [
                {
                    "name": "fixture-output-present",
                    "status": "PASS",
                    "summary": "dry_run_output.txt exists",
                }
            ],
            "compressed_logs": "fixture passed",
        }
        handoff.update(overrides)
        return handoff

    def _blk_test_fail(self, **overrides):
        handoff = self._blk_test_pass(
            status="FAIL",
            checks=[
                {
                    "name": "fixture-output-present",
                    "status": "FAIL",
                    "summary": "dry_run_output.txt missing",
                }
            ],
        )
        handoff.update(overrides)
        return handoff

    def _mapped_mcp_pass_response(self, **overrides):
        mapped = {
            "status": "PASS",
            "source": "blk-test-mcp-response-shape",
            "beb_id": "BEB_007",
            "commit_hash": "abc123",
            "pre_engine_hash": "def456",
            "trace_artifacts": list(TRACE_ARTIFACTS),
            "checks": [
                {
                    "name": "fixture-output-present",
                    "status": "PASS",
                    "summary": "deterministic disabled MCP fixture check",
                }
            ],
            "rtm_status": "NOT_GENERATED",
            "beo_publication": "DRAFT_ONLY",
        }
        mapped.update(overrides)
        return mapped

    def _mapped_mcp_fail_response(self, **overrides):
        mapped = self._mapped_mcp_pass_response(
            status="FAIL",
            checks=[
                {
                    "name": "fixture-output-present",
                    "status": "FAIL",
                    "summary": "deterministic disabled MCP fixture failed",
                }
            ],
        )
        mapped.update(overrides)
        return mapped

    def _mapped_mcp_blocked_response(self, **overrides):
        mapped = self._mapped_mcp_pass_response(
            status="BLOCKED",
            commit_hash="",
            checks=[],
        )
        mapped.update(overrides)
        return mapped

    def _live_smoke_evidence(self, **overrides):
        evidence = {
            "sprint": "BLK-SYSTEM-014",
            "source": "blk-test-mcp-first-live-smoke",
            "run_id": "BLK-SYSTEM-014-SMOKE-001",
            "tool_name": "run_ast_validation",
            "status": "PASS",
            "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
            "commit_hash": "synthetic-fixture-no-git-commit",
            "pre_engine_hash": "sha256:" + "3" * 64,
            "test_profile": "bounded-live-smoke-short",
            "trace_artifacts": [
                {
                    "kind": "REQ",
                    "id": "REQ-S14-SMOKE-001",
                    "version_hash": "sha256:" + "1" * 64,
                }
            ],
            "checks": [
                {
                    "name": "run_ast_validation",
                    "status": "PASS",
                    "summary": "AST validation passed for synthetic isolated workspace",
                }
            ],
            "approval_record_hash": "sha256:" + "4" * 64,
            "authorization_request_hash": "sha256:" + "5" * 64,
            "source_evidence_hash": "sha256:" + "6" * 64,
            "transcript_hash": "sha256:" + "7" * 64,
            "cleanup_status": "CLEANED",
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read": False,
        }
        evidence.update(overrides)
        return evidence

    def test_live_smoke_pass_projects_to_draft_beo_only(self):
        evidence = self._live_smoke_evidence(status="PASS")
        beo = project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_001")

        self.assertEqual(beo["beo_id"], "BEO_S15_DRAFT_001")
        self.assertEqual(beo["beb_id"], evidence["beb_id"])
        self.assertEqual(beo["status"], "PASS")
        self.assertEqual(beo["source"], "blk-test-mcp-first-live-smoke")
        self.assertEqual(beo["commit_hash"], evidence["commit_hash"])
        self.assertEqual(beo["pre_engine_hash"], evidence["pre_engine_hash"])
        self.assertEqual(beo["trace_artifacts"], evidence["trace_artifacts"])
        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertEqual(beo["live_smoke_replay"]["run_id"], evidence["run_id"])
        self.assertEqual(beo["live_smoke_replay"]["transcript_hash"], evidence["transcript_hash"])
        self.assertNotIn("published_at", beo)
        self.assertNotIn("approved_by", beo)
        self.assertNotIn("signature", beo)
        self.assertNotIn("rtm", beo)

    def test_live_smoke_fail_projects_to_failed_draft_beo_only(self):
        evidence = self._live_smoke_evidence(
            status="FAIL",
            checks=[
                {
                    "name": "run_ast_validation",
                    "status": "FAIL",
                    "summary": "AST validation failed for synthetic isolated workspace",
                }
            ],
        )
        beo = project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_002")

        self.assertEqual(beo["status"], "FAIL")
        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertEqual(beo["test_summary"], {"profile": "bounded-live-smoke-short", "checks_passed": 0, "checks_failed": 1})

    def test_live_smoke_projection_requires_source_bound_fields(self):
        required_fields = (
            "beb_id",
            "commit_hash",
            "pre_engine_hash",
            "trace_artifacts",
            "checks",
            "approval_record_hash",
            "authorization_request_hash",
            "source_evidence_hash",
            "transcript_hash",
            "run_id",
            "tool_name",
            "cleanup_status",
        )
        for field in required_fields:
            evidence = self._live_smoke_evidence()
            evidence[field] = [] if field in {"trace_artifacts", "checks"} else ""
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_001")

    def test_live_smoke_projection_requires_canonical_replay_hashes(self):
        for field in (
            "approval_record_hash",
            "authorization_request_hash",
            "source_evidence_hash",
            "transcript_hash",
        ):
            evidence = self._live_smoke_evidence(**{field: "not-sha256"})
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_001")

    def test_live_smoke_projection_does_not_read_active_vault(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            beo = project_live_smoke_evidence_to_draft_beo(
                self._live_smoke_evidence(), beo_id="BEO_S15_DRAFT_001"
            )

        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")

    def test_pass_blk_test_result_projects_to_beo_shape(self):
        beo = project_blk_test_handoff_to_beo(self._blk_test_pass(), beo_id="BEO_004")

        self.assertEqual(
            beo,
            {
                "beo_id": "BEO_004",
                "beb_id": "BEB_004",
                "status": "PASS",
                "source": "blk-test-fixture",
                "commit_hash": "abc123",
                "pre_engine_hash": "def456",
                "trace_artifacts": TRACE_ARTIFACTS,
                "test_summary": {
                    "profile": "strict-ci",
                    "checks_passed": 1,
                    "checks_failed": 0,
                },
                "rtm_status": "NOT_GENERATED",
                "beo_publication": "DRAFT_ONLY",
            },
        )

    def test_beo_projection_preserves_trace_artifacts_exactly(self):
        source = self._blk_test_pass(trace_artifacts=list(TRACE_ARTIFACTS))
        beo = project_blk_test_handoff_to_beo(source, beo_id="BEO_004")

        self.assertEqual(beo["trace_artifacts"], source["trace_artifacts"])
        self.assertEqual(beo["trace_artifacts"][0]["version_hash"], "sha256:" + "a" * 64)

    def test_fail_blk_test_result_does_not_project_success_beo(self):
        beo = project_blk_test_handoff_to_beo(self._blk_test_fail(), beo_id="BEO_004")

        self.assertEqual(beo["status"], "FAIL")
        self.assertEqual(beo["test_summary"]["checks_passed"], 0)
        self.assertEqual(beo["test_summary"]["checks_failed"], 1)
        self.assertEqual(beo["trace_artifacts"], TRACE_ARTIFACTS)

    def test_beo_projection_marks_rtm_not_generated(self):
        beo = project_blk_test_handoff_to_beo(self._blk_test_pass(), beo_id="BEO_004")

        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertNotIn("rtm", beo)

    def test_mapped_disabled_mcp_pass_projects_to_draft_beo(self):
        mapped = self._mapped_mcp_pass_response()
        beo = project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")

        self.assertEqual(beo["beo_id"], "BEO_007")
        self.assertEqual(beo["beb_id"], "BEB_007")
        self.assertEqual(beo["status"], "PASS")
        self.assertEqual(beo["source"], "blk-test-mcp-response-shape")
        self.assertEqual(beo["commit_hash"], "abc123")
        self.assertEqual(beo["pre_engine_hash"], "def456")
        self.assertEqual(beo["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(
            beo["test_summary"],
            {"profile": "strict-ci", "checks_passed": 1, "checks_failed": 0},
        )
        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertNotIn("rtm", beo)
        self.assertNotIn("published_at", beo)
        self.assertNotIn("approved_by", beo)

    def test_mapped_disabled_mcp_fail_projects_to_failed_draft_beo(self):
        mapped = self._mapped_mcp_fail_response()
        beo = project_mapped_mcp_response_to_beo(
            mapped,
            beo_id="BEO_007",
            test_profile="disabled-mcp-fixture",
        )

        self.assertEqual(beo["status"], "FAIL")
        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertEqual(
            beo["test_summary"],
            {"profile": "disabled-mcp-fixture", "checks_passed": 0, "checks_failed": 1},
        )

    def test_mapped_disabled_mcp_blocked_does_not_project_to_beo(self):
        mapped = self._mapped_mcp_blocked_response()

        with self.assertRaisesRegex(ValueError, "PASS/FAIL"):
            project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")

    def test_mapped_disabled_mcp_projection_requires_source_bound_fields(self):
        required_fields = ("beb_id", "commit_hash", "pre_engine_hash", "trace_artifacts", "checks")

        for field in required_fields:
            mapped = self._mapped_mcp_pass_response()
            mapped[field] = [] if field in {"trace_artifacts", "checks"} else ""
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")

    def test_mapped_disabled_mcp_projection_rejects_non_mcp_source(self):
        mapped = self._mapped_mcp_pass_response(source="live-blk-test")

        with self.assertRaisesRegex(ValueError, "blk-test-mcp-response-shape"):
            project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")

    def test_mapped_disabled_mcp_projection_requires_canonical_trace_artifact_hashes(self):
        mapped = self._mapped_mcp_pass_response(
            trace_artifacts=[{"kind": "REQ", "id": "REQ-DRY-001", "version_hash": "not-sha256"}]
        )

        with self.assertRaisesRegex(ValueError, "version_hash"):
            project_mapped_mcp_response_to_beo(mapped, beo_id="BEO_007")

    def test_all_beo_fixture_outputs_are_draft_only(self):
        beo = project_blk_test_handoff_to_beo(self._blk_test_pass(), beo_id="BEO_004")

        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertNotIn("rtm", beo)

    def test_beo_projection_rejects_non_blk_test_fixture_status(self):
        with self.assertRaisesRegex(ValueError, "BLK-test fixture status"):
            project_blk_test_handoff_to_beo(self._blk_test_pass(status="BLOCKED"), beo_id="BEO_004")

    def test_beo_projection_does_not_read_active_vault(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")

        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""

        with patch.object(Path, "read_text", fail_forbidden_read):
            beo = project_blk_test_handoff_to_beo(self._blk_test_pass(), beo_id="BEO_004")

        self.assertEqual(beo["status"], "PASS")


class BeoFixtureEndToEndTraceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.binary_path = Path(os.environ.get("BLK_PIPE_TEST_BINARY", "/tmp/blk-pipe-sprint-005"))
        if not cls.binary_path.exists():
            go = shutil.which("go")
            if go is None:
                raise unittest.SkipTest("go binary not available to build blk-pipe test binary")
            subprocess.run(
                [go, "build", "-o", str(cls.binary_path), "./cmd/blk-pipe"],
                cwd=cls.root,
                check=True,
                capture_output=True,
                text=True,
            )

    def _init_repo(self, repo: Path):
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture Tester"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=repo, check=True)
        (repo / "README.md").write_text("baseline\n")
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "baseline"], cwd=repo, check=True)
        subprocess.run(
            ["git", "branch", "sprint/blk-pipe-004-dry-run"],
            cwd=repo,
            check=True,
        )

    def test_trace_baton_exact_across_dry_run_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            self._init_repo(repo)

            blk_pipe_report = run_blk_pipe_dry_run_fixture(
                binary_path=str(self.binary_path),
                beb_path=self.root / "testdata" / "orchestrator" / "BEB_004_dry_run.md",
                l2_path=self.root / "testdata" / "orchestrator" / "L2_004_dry_run.md",
                work_dir=str(repo),
                engine_dir=self.root / "testdata" / "engines",
                env_overrides={
                    "OPENAI_API_KEY": "poisoned-openai-key",
                    "ANTHROPIC_API_KEY": "poisoned-anthropic-key",
                    "CODEX_HOME": str(Path(tmp) / "poisoned-codex-home"),
                },
            )
            blk_test_pass = build_blk_test_pass_handoff(blk_pipe_report)
            beo = project_blk_test_handoff_to_beo(blk_test_pass, beo_id="BEO_004")

        self.assertEqual(blk_pipe_report["status"], "SUCCESS", json.dumps(blk_pipe_report, indent=2))
        self.assertEqual(blk_pipe_report["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(blk_test_pass["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(beo["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(beo["beb_id"], "BEB_004")
        self.assertEqual(beo["commit_hash"], blk_pipe_report["commit_hash"])
        self.assertEqual(beo["pre_engine_hash"], blk_pipe_report["pre_engine_hash"])
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")

    def test_dry_run_non_success_can_build_blocked_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_binary = tmp_path / "fake-blk-pipe.py"
            non_success_report = {
                "status": "FATAL_OUTPUT_FLOOD",
                "beb_id": "BEB_004",
                "commit_hash": "",
                "pre_engine_hash": "pre-engine-hash",
                "staged_files": [],
                "destroyed_files": ["oversized.log"],
                "trace_artifacts": TRACE_ARTIFACTS,
                "engine_logs": "engine output exceeded max_output_bytes",
            }
            fake_binary.write_text(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                f"print({json.dumps(json.dumps(non_success_report))})\n"
                "print('flood stderr', file=sys.stderr)\n"
                "raise SystemExit(5)\n"
            )
            fake_binary.chmod(0o755)

            result = invoke_blk_pipe_dry_run_fixture(
                binary_path=str(fake_binary),
                beb_path=self.root / "testdata" / "orchestrator" / "BEB_004_dry_run.md",
                l2_path=self.root / "testdata" / "orchestrator" / "L2_004_dry_run.md",
                work_dir=str(tmp_path / "repo"),
                engine_dir=self.root / "testdata" / "engines",
            )
            blocked = build_blk_test_blocked_handoff(result.report)

        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.status, "FATAL_OUTPUT_FLOOD")
        self.assertEqual(result.stderr.strip(), "flood stderr")
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual(blocked["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertIn("FATAL_OUTPUT_FLOOD", blocked["checks"][0]["summary"])


if __name__ == "__main__":
    unittest.main()
