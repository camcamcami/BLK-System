import subprocess
import tempfile
import unittest
from pathlib import Path

from blk_test_non_disposable_l4_runtime_pilot import (
    APPROVAL_ID,
    EXPECTED_HEAD,
    L4_BLOCKED,
    L4_PASS,
    RUN_ID,
    run_blk_test_non_disposable_l4_runtime_pilot,
)


class BlkTestNonDisposableL4RuntimePilotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base / "target"
        self.source = self.repo / "python"
        self.source.mkdir(parents=True)
        subprocess.run(["git", "init", "-b", "main"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (self.source / "good.py").write_text("VALUE = 51\n", encoding="utf-8")
        subprocess.run(["git", "add", "python/good.py"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([
            "git",
            "-c",
            "user.name=BLK Test",
            "-c",
            "user.email=blk-test@example.invalid",
            "commit",
            "-m",
            "initial",
        ], cwd=self.repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip()
        self.workspace = self.base / "workspace"
        self.used_approvals = set()
        self.used_runs = set()

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, **overrides):
        args = {
            "target_repo_path": self.repo,
            "source_subtree_path": self.source,
            "workspace_clone_path": self.workspace,
            "approval_id": APPROVAL_ID,
            "run_id": RUN_ID,
            "expected_head": self.head,
            "fixed_tool": "run_ast_validation",
            "expires_at": "2099-01-01T00:00:00Z",
            "now": "2026-05-10T00:00:00Z",
            "used_approval_ids": self.used_approvals,
            "used_run_ids": self.used_runs,
            "workspace_marker_nonce": "nonce-BLK-SYSTEM-051-test",
            "output_byte_limit": 8192,
        }
        args.update(overrides)
        return run_blk_test_non_disposable_l4_runtime_pilot(**args)

    def test_successful_one_run_returns_evidence_only_and_cleans_workspace(self):
        evidence = self._run()

        self.assertEqual(evidence["pilot_status"], L4_PASS)
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["files_checked"], ["good.py"])
        self.assertTrue(evidence["fixed_tool_executed"])
        self.assertTrue(evidence["replay_consumed_before_runtime"])
        self.assertFalse(evidence["source_mutation_detected"])
        self.assertFalse(evidence["git_mutation_detected"])
        self.assertFalse(evidence["source_write_allowed"])
        self.assertFalse(evidence["git_mutation_allowed"])
        self.assertFalse(evidence["active_vault_read"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertFalse(evidence["production_isolation_claimed"])
        self.assertFalse(self.workspace.exists())
        self.assertIn(APPROVAL_ID, self.used_approvals)
        self.assertIn(RUN_ID, self.used_runs)

    def test_target_head_mismatch_blocks_before_workspace_creation_or_tool_execution(self):
        evidence = self._run(expected_head=EXPECTED_HEAD)

        self.assertEqual(evidence["pilot_status"], L4_BLOCKED)
        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertIn("target HEAD mismatch", evidence["block_reason"])
        self.assertFalse(evidence["fixed_tool_executed"])
        self.assertFalse(self.workspace.exists())
        self.assertIn(APPROVAL_ID, self.used_approvals)
        self.assertIn(RUN_ID, self.used_runs)

    def test_replay_wrong_tool_and_expiry_block_before_workspace_creation(self):
        self.used_approvals.add(APPROVAL_ID)
        with self.assertRaisesRegex(ValueError, "approval replay"):
            self._run()
        self.used_approvals.clear()

        with self.assertRaisesRegex(ValueError, "fixed_tool must be run_ast_validation"):
            self._run(fixed_tool="run_tests")
        self.assertFalse(self.workspace.exists())

        evidence = self._run(expires_at="2026-05-09T00:00:00Z")
        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertIn("expired", evidence["block_reason"])
        self.assertFalse(evidence["fixed_tool_executed"])
        self.assertFalse(self.workspace.exists())

    def test_rejects_source_outside_target_git_descendant_secret_and_symlink_escape(self):
        outside = self.base / "outside"
        outside.mkdir()
        with self.assertRaisesRegex(ValueError, "source_subtree_path must resolve inside target_repo_path"):
            self._run(source_subtree_path=outside)

        nested_git = self.source / "nested" / ".git"
        nested_git.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "git metadata"):
            self._run(used_approval_ids=set(), used_run_ids=set())
        nested_git.rmdir()
        (self.source / "nested").rmdir()

        secret = self.source / ".env"
        secret.write_text("SECRET=value\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "secret"):
            self._run(used_approval_ids=set(), used_run_ids=set())
        secret.unlink()

        escape_target = self.base / "escape"
        escape_target.mkdir()
        (self.source / "escape_link").symlink_to(escape_target)
        with self.assertRaisesRegex(ValueError, "symlink escape"):
            self._run(used_approval_ids=set(), used_run_ids=set())

    def test_syntax_error_returns_fail_evidence_without_mutation_or_publication(self):
        (self.source / "bad.py").write_text("def broken(:\n", encoding="utf-8")

        evidence = self._run()

        self.assertEqual(evidence["status"], "FAIL")
        self.assertTrue(evidence["diagnostics"])
        self.assertFalse(evidence["source_mutation_detected"])
        self.assertFalse(evidence["git_mutation_detected"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertFalse(self.workspace.exists())

    def test_output_overflow_returns_blocked_and_cleans_workspace(self):
        for i in range(30):
            (self.source / f"f_{i}.py").write_text(f"VALUE_{i} = {i}\n", encoding="utf-8")

        evidence = self._run(output_byte_limit=300)

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertIn("output byte limit", evidence["block_reason"])
        self.assertFalse(evidence["fixed_tool_executed"] is False and evidence["workspace_cleanup_verified"] is False)
        self.assertFalse(self.workspace.exists())


if __name__ == "__main__":
    unittest.main()
