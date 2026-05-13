import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import blk_test_non_disposable_l4_runtime_pilot as pilot_module
from blk_test_non_disposable_l4_runtime_pilot import (
    APPROVAL_ID,
    L4_BLOCKED,
    L4_PASS,
    RUN_ID,
    run_blk_test_non_disposable_l4_runtime_pilot,
)


class BlkTestNonDisposableL4RuntimePilotTest(unittest.TestCase):

    def test_source_scope_rejects_exact_protected_blk_req_roots(self):
        for root_name in ("docs/active", "docs/requirements", "docs/use_cases"):
            protected = self.repo / root_name
            protected.mkdir(parents=True, exist_ok=True)
            (protected / "REQ-001.md").write_text("protected body\n", encoding="utf-8")
            with self.subTest(root=root_name):
                with self.assertRaisesRegex(ValueError, "protected BLK-req"):
                    pilot_module._reject_source_scope(protected)

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
        self.process_approvals = set()
        self.process_runs = set()

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
        with patch.object(pilot_module, "APPROVED_TARGET_REPO", self.repo.resolve()), \
            patch.object(pilot_module, "APPROVED_SOURCE_SUBTREE", self.source.resolve()), \
            patch.object(pilot_module, "APPROVED_WORKSPACE", self.workspace.resolve()), \
            patch.object(pilot_module, "EXPECTED_HEAD", self.head), \
            patch.object(pilot_module, "REPLAY_LEDGER_PATH", self.base / "replay-ledger.json", create=True), \
            patch.object(pilot_module, "_PROCESS_CONSUMED_APPROVAL_IDS", self.process_approvals, create=True), \
            patch.object(pilot_module, "_PROCESS_CONSUMED_RUN_IDS", self.process_runs, create=True):
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
        (self.source / "after_approval.py").write_text("VALUE = 52\n", encoding="utf-8")
        subprocess.run(["git", "add", "python/after_approval.py"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "-c", "user.name=BLK Test", "-c", "user.email=blk-test@example.invalid", "commit", "-m", "advance head"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        evidence = self._run()

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
        with self.assertRaisesRegex(ValueError, "source_subtree_path must match the approved exact source subtree"):
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

        secret_like_names = [
            ".env.local",
            "credentials.json",
            "secrets.yaml",
            "secret.txt",
            "token.txt",
            "tokens.json",
            "id_rsa",
            "private_key.pem",
        ]
        for name in secret_like_names:
            candidate = self.source / name
            candidate.write_text("SECRET=value\n", encoding="utf-8")
            used_approvals: set[str] = set()
            used_runs: set[str] = set()
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "secret"):
                    self._run(used_approval_ids=used_approvals, used_run_ids=used_runs)
                self.assertFalse(self.workspace.exists())
                self.assertNotIn(APPROVAL_ID, used_approvals)
                self.assertNotIn(RUN_ID, used_runs)
            candidate.unlink()

        secret_dir = self.source / "secrets.d"
        secret_dir.mkdir()
        with self.assertRaisesRegex(ValueError, "secret"):
            self._run(used_approval_ids=set(), used_run_ids=set())
        secret_dir.rmdir()

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

    def test_exact_target_and_workspace_are_enforced_and_existing_workspace_is_not_deleted(self):
        other_repo = self.base / "other"
        other_source = other_repo / "python"
        other_source.mkdir(parents=True)
        subprocess.run(["git", "init", "-b", "main"], cwd=other_repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (other_source / "good.py").write_text("VALUE = 1\n", encoding="utf-8")
        subprocess.run(["git", "add", "python/good.py"], cwd=other_repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "-c", "user.name=BLK Test", "-c", "user.email=blk-test@example.invalid", "commit", "-m", "other"], cwd=other_repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with self.assertRaisesRegex(ValueError, "target_repo_path must match the approved exact target"):
            self._run(target_repo_path=other_repo, source_subtree_path=other_source, used_approval_ids=set(), used_run_ids=set())

        self.workspace.mkdir()
        sentinel = self.workspace / "do-not-delete.txt"
        sentinel.write_text("owned by caller\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "workspace_clone_path already exists"):
            self._run(used_approval_ids=set(), used_run_ids=set())
        self.assertTrue(sentinel.exists())

    def test_path_spelling_aliases_are_rejected_even_if_resolved_target_matches(self):
        with self.assertRaisesRegex(ValueError, "target_repo_path must use the approved exact spelling"):
            self._run(target_repo_path=f"{self.repo}/.", used_approval_ids=set(), used_run_ids=set())
        with self.assertRaisesRegex(ValueError, "source_subtree_path must use the approved exact spelling"):
            self._run(source_subtree_path=f"{self.source}/../python", used_approval_ids=set(), used_run_ids=set())
        with self.assertRaisesRegex(ValueError, "workspace_clone_path must use the approved exact spelling"):
            self._run(workspace_clone_path=f"{self.workspace.parent}/./{self.workspace.name}", used_approval_ids=set(), used_run_ids=set())

    def test_parameterized_envelope_uses_its_own_sprint_nonce_marker_workspace_and_ledger(self):
        future_workspace = self.base / "future-workspace"
        future_ledger = self.base / "future-replay-ledger.json"
        future_envelope = pilot_module.L4RuntimeApprovalEnvelope(
            sprint="BLK-SYSTEM-999",
            approval_id="APPROVAL-BLK-SYSTEM-999-001",
            run_id="RUN-BLK-SYSTEM-999-001",
            expected_head=self.head,
            approved_target_repo=self.repo.resolve(),
            approved_source_subtree=self.source.resolve(),
            approved_workspace=future_workspace.resolve(),
            replay_ledger_path=future_ledger,
            marker_nonce_binding="BLK-SYSTEM-999",
            workspace_marker_name=".blk-system-999-non-disposable-l4-runtime-workspace",
        )

        evidence = self._run(
            target_repo_path=self.repo,
            source_subtree_path=self.source,
            workspace_clone_path=future_workspace,
            approval_id="APPROVAL-BLK-SYSTEM-999-001",
            run_id="RUN-BLK-SYSTEM-999-001",
            expected_head=self.head,
            workspace_marker_nonce="nonce-BLK-SYSTEM-999-repeatable-approval-envelope",
            approval_envelope=future_envelope,
            used_approval_ids=set(),
            used_run_ids=set(),
        )

        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["sprint"], "BLK-SYSTEM-999")
        self.assertEqual(evidence["approval_id"], "APPROVAL-BLK-SYSTEM-999-001")
        self.assertEqual(evidence["run_id"], "RUN-BLK-SYSTEM-999-001")
        self.assertFalse(future_workspace.exists())
        self.assertTrue(future_ledger.exists())
        self.assertEqual(json.loads(future_ledger.read_text(encoding="utf-8"))["approval_ids"], ["APPROVAL-BLK-SYSTEM-999-001"])

    def test_parameterized_envelope_rejects_historical_nonce_laundering(self):
        future_envelope = pilot_module.L4RuntimeApprovalEnvelope(
            sprint="BLK-SYSTEM-999",
            approval_id="APPROVAL-BLK-SYSTEM-999-001",
            run_id="RUN-BLK-SYSTEM-999-001",
            expected_head=self.head,
            approved_target_repo=self.repo.resolve(),
            approved_source_subtree=self.source.resolve(),
            approved_workspace=(self.base / "future-workspace").resolve(),
            replay_ledger_path=self.base / "future-replay-ledger.json",
            marker_nonce_binding="BLK-SYSTEM-999",
            workspace_marker_name=".blk-system-999-non-disposable-l4-runtime-workspace",
        )

        with self.assertRaisesRegex(ValueError, "workspace_marker_nonce must bind to BLK-SYSTEM-999"):
            self._run(
                target_repo_path=self.repo,
                source_subtree_path=self.source,
                workspace_clone_path=self.base / "future-workspace",
                approval_id="APPROVAL-BLK-SYSTEM-999-001",
                run_id="RUN-BLK-SYSTEM-999-001",
                expected_head=self.head,
                workspace_marker_nonce="nonce-BLK-SYSTEM-051-only",
                approval_envelope=future_envelope,
                used_approval_ids=set(),
                used_run_ids=set(),
            )

    def test_parameterized_envelope_rejects_tool_expansion_and_marker_path_escape(self):
        with self.assertRaisesRegex(ValueError, "approval envelope fixed_tool must be run_ast_validation"):
            pilot_module.L4RuntimeApprovalEnvelope(
                sprint="BLK-SYSTEM-999",
                approval_id="APPROVAL-BLK-SYSTEM-999-001",
                run_id="RUN-BLK-SYSTEM-999-001",
                expected_head=self.head,
                approved_target_repo=self.repo.resolve(),
                approved_source_subtree=self.source.resolve(),
                approved_workspace=(self.base / "future-workspace").resolve(),
                replay_ledger_path=self.base / "future-replay-ledger.json",
                marker_nonce_binding="BLK-SYSTEM-999",
                workspace_marker_name=".blk-system-999-non-disposable-l4-runtime-workspace",
                fixed_tool="run_tests",
            )

        with self.assertRaisesRegex(ValueError, "workspace_marker_name must be a single hidden filename"):
            pilot_module.L4RuntimeApprovalEnvelope(
                sprint="BLK-SYSTEM-999",
                approval_id="APPROVAL-BLK-SYSTEM-999-001",
                run_id="RUN-BLK-SYSTEM-999-001",
                expected_head=self.head,
                approved_target_repo=self.repo.resolve(),
                approved_source_subtree=self.source.resolve(),
                approved_workspace=(self.base / "future-workspace").resolve(),
                replay_ledger_path=self.base / "future-replay-ledger.json",
                marker_nonce_binding="BLK-SYSTEM-999",
                workspace_marker_name="../escaped-marker",
            )

    def test_parameterized_envelope_rejects_weak_nonce_binding_consumed_ids_and_repo_ledger(self):
        base_kwargs = {
            "sprint": "BLK-SYSTEM-999",
            "approval_id": "APPROVAL-BLK-SYSTEM-999-001",
            "run_id": "RUN-BLK-SYSTEM-999-001",
            "expected_head": self.head,
            "approved_target_repo": self.repo.resolve(),
            "approved_source_subtree": self.source.resolve(),
            "approved_workspace": (self.base / "future-workspace").resolve(),
            "replay_ledger_path": self.base / "future-replay-ledger.json",
            "marker_nonce_binding": "BLK-SYSTEM-999",
            "workspace_marker_name": ".blk-system-999-non-disposable-l4-runtime-workspace",
        }

        with self.assertRaisesRegex(ValueError, "marker_nonce_binding must equal the approval envelope sprint"):
            pilot_module.L4RuntimeApprovalEnvelope(**{**base_kwargs, "marker_nonce_binding": "BLK"})

        with self.assertRaisesRegex(ValueError, "approval_id must bind to the approval envelope sprint"):
            pilot_module.L4RuntimeApprovalEnvelope(**{**base_kwargs, "approval_id": "APPROVAL-BLK-SYSTEM-051-001"})
        with self.assertRaisesRegex(ValueError, "run_id must bind to the approval envelope sprint"):
            pilot_module.L4RuntimeApprovalEnvelope(**{**base_kwargs, "run_id": "RUN-BLK-SYSTEM-052-001"})
        with self.assertRaisesRegex(ValueError, "approval_id must not reuse a consumed historical approval ID"):
            pilot_module.L4RuntimeApprovalEnvelope(**{**base_kwargs, "sprint": "BLK-SYSTEM-051", "approval_id": "APPROVAL-BLK-SYSTEM-051-001", "run_id": "RUN-BLK-SYSTEM-051-001", "marker_nonce_binding": "BLK-SYSTEM-051"})

        for ledger_path in [
            self.source / "replay-ledger.json",
            self.repo / ".git" / "replay-ledger.json",
            self.repo / "docs" / "active" / "replay-ledger.json",
        ]:
            with self.subTest(ledger_path=ledger_path):
                with self.assertRaisesRegex(ValueError, "replay_ledger_path must not overlap target_repo_path"):
                    pilot_module.L4RuntimeApprovalEnvelope(**{**base_kwargs, "replay_ledger_path": ledger_path})

    def test_durable_replay_ledger_blocks_fresh_caller_sets(self):
        first = self._run(used_approval_ids=set(), used_run_ids=set())
        self.assertEqual(first["status"], "PASS")
        with self.assertRaisesRegex(ValueError, "process approval replay"):
            self._run(used_approval_ids=set(), used_run_ids=set())
        (self.base / "replay-ledger.json").unlink()
        with self.assertRaisesRegex(ValueError, "process approval replay"):
            self._run(used_approval_ids=set(), used_run_ids=set())

    def test_detects_non_python_source_mutation_during_runtime(self):
        data_file = self.source / "data.txt"
        data_file.write_text("before\n", encoding="utf-8")
        real_parse = pilot_module.ast.parse

        def mutate_then_parse(*args, **kwargs):
            data_file.write_text("after\n", encoding="utf-8")
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=mutate_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["source_mutation_detected"])

    def test_detects_git_metadata_mutation_even_when_size_and_mtime_are_preserved(self):
        ref_path = self.repo / ".git" / "refs" / "heads" / "main"
        original = ref_path.read_text(encoding="utf-8")
        stat = ref_path.stat()
        replacement = "f" * 40 + "\n"
        self.assertEqual(len(original), len(replacement))
        real_parse = pilot_module.ast.parse

        def mutate_ref_then_parse(*args, **kwargs):
            ref_path.write_text(replacement, encoding="utf-8")
            import os
            os.utime(ref_path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=mutate_ref_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["git_mutation_detected"])

    def test_detects_directory_and_symlink_source_mutations_during_runtime(self):
        link = self.source / "link.py"
        other = self.source / "other.py"
        other.write_text("VALUE = 99\n", encoding="utf-8")
        link.symlink_to(self.source / "good.py")
        before_target = link.resolve()
        real_parse = pilot_module.ast.parse

        def mutate_entries_then_parse(*args, **kwargs):
            (self.source / "new_dir").mkdir(exist_ok=True)
            link.unlink()
            link.symlink_to(other)
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=mutate_entries_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["source_mutation_detected"])
        self.assertTrue((self.source / "new_dir").is_dir())
        self.assertNotEqual(before_target, link.resolve())

    def test_detects_symlink_payload_mutation_even_when_resolved_target_is_same(self):
        link = self.source / "same_link.py"
        link.symlink_to("good.py")
        real_parse = pilot_module.ast.parse

        def mutate_link_text_then_parse(*args, **kwargs):
            link.unlink()
            link.symlink_to("./good.py")
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=mutate_link_text_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["source_mutation_detected"])
        self.assertEqual(link.readlink(), Path("./good.py"))

    def test_replay_ledger_tmp_symlink_is_rejected_before_source_overwrite(self):
        innocent = self.source / "innocent.txt"
        innocent.write_text("do not overwrite\n", encoding="utf-8")
        ledger = self.base / "replay-ledger.json"
        tmp = ledger.with_suffix(ledger.suffix + ".tmp")
        tmp.symlink_to(innocent)
        with self.assertRaisesRegex(ValueError, "durable replay ledger temporary path already exists"):
            self._run()
        self.assertEqual(innocent.read_text(encoding="utf-8"), "do not overwrite\n")

    def test_detects_source_and_git_metadata_only_mutations(self):
        link = self.source / "meta_link.py"
        link.symlink_to("good.py")
        git_ref = self.repo / ".git" / "refs" / "heads" / "main"
        real_parse = pilot_module.ast.parse

        def mutate_metadata_then_parse(*args, **kwargs):
            import os
            (self.source / "good.py").chmod(0o600)
            os.utime(link, ns=(123456789, 123456789), follow_symlinks=False)
            git_ref.chmod(0o600)
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=mutate_metadata_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["source_mutation_detected"])
        self.assertTrue(evidence["git_mutation_detected"])

    def test_detects_transient_create_delete_root_directory_metadata_mutations(self):
        real_parse = pilot_module.ast.parse

        def transient_mutation_then_parse(*args, **kwargs):
            source_tmp = self.source / "transient_root.txt"
            source_tmp.write_text("brief\n", encoding="utf-8")
            source_tmp.unlink()
            git_tmp = self.repo / ".git" / "transient_git_root"
            git_tmp.write_text("brief\n", encoding="utf-8")
            git_tmp.unlink()
            return real_parse(*args, **kwargs)

        with patch.object(pilot_module.ast, "parse", side_effect=transient_mutation_then_parse):
            evidence = self._run()

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertTrue(evidence["source_mutation_detected"])
        self.assertTrue(evidence["git_mutation_detected"])

    def test_output_overflow_returns_blocked_bounded_evidence_and_cleans_workspace(self):
        for i in range(30):
            (self.source / f"f_{i}.py").write_text(f"VALUE_{i} = {i}\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "output_byte_limit must be at least"):
            self._run(output_byte_limit=300)

        evidence = self._run(output_byte_limit=1024)
        actual_size = len(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8"))

        self.assertEqual(evidence["status"], "BLOCKED")
        self.assertIn("output byte limit", evidence["block_reason"])
        self.assertLessEqual(actual_size, evidence["output_byte_limit"])
        self.assertEqual(evidence["evidence_json_bytes"], actual_size)
        self.assertFalse(evidence["fixed_tool_executed"] is False and evidence["workspace_cleanup_verified"] is False)
        self.assertFalse(self.workspace.exists())


if __name__ == "__main__":
    unittest.main()
