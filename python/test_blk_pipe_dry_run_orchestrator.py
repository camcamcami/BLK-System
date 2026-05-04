import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from blk_pipe_dry_run_orchestrator import (
    DryRunSprintInput,
    TraceArtifact,
    build_codex_dry_run_payload,
    load_dry_run_fixture,
    run_blk_pipe_dry_run_fixture,
)


TRACE_ARTIFACT = TraceArtifact(
    kind="REQ",
    id="REQ-DRY-001",
    version_hash="sha256:" + "a" * 64,
)


class DryRunOrchestratorPayloadTest(unittest.TestCase):
    def _input(self, **overrides):
        values = {
            "beb_id": "BEB_004",
            "profile": "codex-dry-run",
            "work_dir": "/tmp/blk-ephemeral-repo",
            "target_branch": "sprint/blk-pipe-004-dry-run",
            "l2_packet": "L2_ID: L2_004\nBEB_ID: BEB_004\nDo fixture work.\n",
            "trace_artifacts": [TRACE_ARTIFACT],
            "allowed_new_files": ["dry_run_output.txt"],
            "validation_commands": ["test -f dry_run_output.txt"],
        }
        values.update(overrides)
        return DryRunSprintInput(**values)

    def test_build_payload_uses_codex_dry_run_profile(self):
        payload = build_codex_dry_run_payload(self._input())

        self.assertEqual(payload["action"], "execute")
        self.assertEqual(payload["beb_id"], "BEB_004")
        self.assertEqual(payload["work_dir"], "/tmp/blk-ephemeral-repo")
        self.assertEqual(payload["target_branch"], "sprint/blk-pipe-004-dry-run")
        self.assertEqual(payload["engine"], "codex-dry-run")
        self.assertEqual(payload["engine_args"][:2], ["exec", "-"])
        self.assertEqual(payload["validation_commands"], ["test -f dry_run_output.txt"])
        self.assertEqual(payload["allowed_modified_files"], [])
        self.assertEqual(payload["allowed_new_files"], ["dry_run_output.txt"])

    def test_build_payload_includes_blk003_required_isolation_args(self):
        payload = build_codex_dry_run_payload(self._input())

        for arg in [
            "--json",
            "--isolated",
            "--yes",
            "--deny-read=**/.git/**",
            "--deny-read=**/node_modules/**",
            "--deny-read=**/.env*",
            "--dry-run",
        ]:
            self.assertIn(arg, payload["engine_args"])

    def test_build_payload_preserves_l2_packet_and_trace_artifacts(self):
        l2_packet = "L2_ID: L2_004\nBEB_ID: BEB_004\nfixture body\n"
        payload = build_codex_dry_run_payload(self._input(l2_packet=l2_packet))

        self.assertEqual(payload["l2_packet"], l2_packet)
        self.assertEqual(
            payload["trace_artifacts"],
            [
                {
                    "kind": "REQ",
                    "id": "REQ-DRY-001",
                    "version_hash": "sha256:" + "a" * 64,
                }
            ],
        )

    def test_build_payload_rejects_codex_live_profile(self):
        with self.assertRaisesRegex(ValueError, "codex-dry-run"):
            build_codex_dry_run_payload(self._input(profile="codex-live"))

    def test_build_payload_rejects_empty_unknown_and_cyber_profiles(self):
        for profile in ["", "dev-smoke", "strict-ci", "cyber-execution", "model-service"]:
            with self.subTest(profile=profile):
                with self.assertRaisesRegex(ValueError, "codex-dry-run"):
                    build_codex_dry_run_payload(self._input(profile=profile))

    def test_build_payload_uses_absolute_work_dir(self):
        with self.assertRaisesRegex(ValueError, "absolute work_dir"):
            build_codex_dry_run_payload(self._input(work_dir="relative/repo"))

    def test_build_payload_uses_l2_fixture_bytes_exactly(self):
        root = Path(__file__).resolve().parents[1]
        beb_path = root / "testdata" / "orchestrator" / "BEB_004_dry_run.md"
        l2_path = root / "testdata" / "orchestrator" / "L2_004_dry_run.md"
        l2_text = l2_path.read_text()

        fixture_input = load_dry_run_fixture(
            beb_path=beb_path,
            l2_path=l2_path,
            work_dir="/tmp/blk-ephemeral-repo",
        )
        payload = build_codex_dry_run_payload(fixture_input)

        self.assertEqual(payload["l2_packet"], l2_text)
        self.assertEqual(payload["beb_id"], "BEB_004")

    def test_build_payload_rejects_beb_l2_id_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            beb_path = tmp_path / "beb.md"
            l2_path = tmp_path / "l2.md"
            beb_path.write_text(
                textwrap.dedent(
                    """
                    ---
                    beb_id: "BEB_004"
                    l2_id: "L2_004"
                    iteration: 1
                    status: "FIXTURE"
                    sprint_base_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    traced_artifacts:
                      - kind: "REQ"
                        id: "REQ-DRY-001"
                        version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    ---
                    BEB body.
                    """
                ).lstrip()
            )
            l2_path.write_text("L2_ID: L2_OTHER\nBEB_ID: BEB_004\n")

            with self.assertRaisesRegex(ValueError, "L2"):
                load_dry_run_fixture(beb_path, l2_path, "/tmp/blk-ephemeral-repo")

    def test_build_payload_rejects_missing_trace_artifact_in_beb_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            beb_path = tmp_path / "beb.md"
            l2_path = tmp_path / "l2.md"
            beb_path.write_text(
                textwrap.dedent(
                    """
                    ---
                    beb_id: "BEB_004"
                    l2_id: "L2_004"
                    iteration: 1
                    status: "FIXTURE"
                    sprint_base_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    ---
                    BEB body.
                    """
                ).lstrip()
            )
            l2_path.write_text("L2_ID: L2_004\nBEB_ID: BEB_004\n")

            with self.assertRaisesRegex(ValueError, "trace"):
                load_dry_run_fixture(beb_path, l2_path, "/tmp/blk-ephemeral-repo")



class DryRunOrchestratorBlkPipeExecutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.binary_path = Path(os.environ.get("BLK_PIPE_TEST_BINARY", "/tmp/blk-pipe-sprint-004"))
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
        (repo / "dry_run_output.txt").write_text("placeholder\n")
        subprocess.run(["git", "add", "README.md", "dry_run_output.txt"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "baseline"], cwd=repo, check=True)
        subprocess.run(
            ["git", "branch", "sprint/blk-pipe-004-dry-run"],
            cwd=repo,
            check=True,
        )

    def _run_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            self._init_repo(repo)
            report = run_blk_pipe_dry_run_fixture(
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
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            head_files = subprocess.run(
                ["git", "show", "--name-only", "--format=", "HEAD"],
                cwd=repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            output_text = (repo / "dry_run_output.txt").read_text()
            return report, status, head_files, output_text

    def test_dry_run_fixture_invokes_blk_pipe_and_commits_allowed_file(self):
        report, status, head_files, output_text = self._run_fixture()

        self.assertEqual(report["status"], "SUCCESS", json.dumps(report, indent=2))
        self.assertEqual(report["beb_id"], "BEB_004")
        self.assertTrue(report["pre_engine_hash"])
        self.assertTrue(report["commit_hash"])
        self.assertEqual(report["staged_files"], ["dry_run_output.txt"])
        self.assertIn("dry_run_output.txt", head_files)
        self.assertNotIn("README.md", head_files)
        self.assertEqual(status, "")
        self.assertIn("BEB_ID: BEB_004", output_text)
        self.assertIn("L2_ID: L2_004", output_text)

    def test_dry_run_fixture_preserves_trace_artifacts_in_report(self):
        report, _, _, _ = self._run_fixture()

        self.assertEqual(
            report["trace_artifacts"],
            [
                {
                    "kind": "REQ",
                    "id": "REQ-DRY-001",
                    "version_hash": "sha256:" + "a" * 64,
                }
            ],
        )

    def test_dry_run_fixture_does_not_call_real_codex(self):
        report, _, _, output_text = self._run_fixture()

        self.assertIn("FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004", report["engine_logs"])
        self.assertIn("FAKE_CODEX_DRY_RUN_FIXTURE=BLK-PIPE-004", output_text)
        self.assertNotEqual(report.get("engine"), "codex-live")


if __name__ == "__main__":
    unittest.main()
