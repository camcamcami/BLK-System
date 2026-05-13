import json
import shutil
import subprocess
import tempfile
import zlib
import unittest
from pathlib import Path
from unittest.mock import patch

import blk_test_fixed_tool_l4_disposable_repo_runtime as runtime_module

from blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary import (
    APPROVAL_CHECKPOINT as PREFLIGHT_APPROVAL_CHECKPOINT,
    build_sprint047_l4_approval_record,
    build_sprint047_l4_approval_request,
    build_sprint047_l4_source_report,
)
from blk_test_fixed_tool_l4_disposable_repo_runtime import (
    APPROVAL_CHECKPOINT,
    L4_BLOCKED,
    L4_FAIL,
    L4_PASS,
    build_sprint048_runtime_approval_record,
    run_blk_test_l4_disposable_repo_runtime,
)

VALID_SOURCE_COMMIT = "sha256:" + "0123456789abcdef" * 4
VALID_PRE_ENGINE = "sha256:" + "abcdef0123456789" * 4
VALID_IMPLEMENTATION = "sha256:" + "00112233445566778899aabbccddeeff" * 2
VALID_DRIVER = "sha256:" + "ffeeddccbbaa99887766554433221100" * 2
NOW = "2026-05-09T22:30:00Z"
ISSUED = "2026-05-09T22:00:00Z"
EXPIRES = "2026-05-09T23:00:00Z"


class BlkTestFixedToolL4DisposableRepoRuntimeTest(unittest.TestCase):

    def test_source_scope_rejects_exact_protected_blk_req_roots(self):
        for root_name in ("docs/active", "docs/requirements", "docs/use_cases"):
            protected = self.target_repo / root_name
            protected.mkdir(parents=True, exist_ok=True)
            (protected / "REQ-001.md").write_text("protected body\n", encoding="utf-8")
            with self.subTest(root=root_name):
                with self.assertRaisesRegex(ValueError, "protected BLK-req"):
                    runtime_module._reject_runtime_source_scope(protected)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.target_repo = self.base / "disposable-real-repo"
        self.source_subtree = self.target_repo / "src"
        self.workspace = self.base / "approved-workspace"
        self.marker_nonce = "nonce-BLK-SYSTEM-048-L4-RUN-001"
        self.source_subtree.mkdir(parents=True)
        subprocess.run(
            ["git", "init", "-b", "blk-system-048-disposable-l4-runtime"],
            cwd=self.target_repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        (self.source_subtree / "good.py").write_text("VALUE = 48\n")
        subprocess.run(["git", "add", "src/good.py"], cwd=self.target_repo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=BLK Test",
                "-c",
                "user.email=blk-test@example.invalid",
                "commit",
                "-m",
                "initial disposable fixture",
            ],
            cwd=self.target_repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.git_head_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.target_repo, text=True).strip()
        self.workspace.mkdir()
        self.marker = {
            "workspace_marker_nonce": self.marker_nonce,
            "workspace_clone_id": "workspace-BLK-SYSTEM-048-L4-001",
            "approved_repo_path": str(self.target_repo.resolve()),
            "approved_source_subtree": str(self.source_subtree.resolve()),
            "approved_branch": "blk-system-048-disposable-l4-runtime",
            "approved_worktree_id": "worktree-BLK-SYSTEM-048-L4-001",
        }
        self.repo_marker = dict(self.marker)
        self.repo_marker["git_head_commit"] = self.git_head_commit
        (self.workspace / ".blk-system-047-l4-workspace").write_text(json.dumps(self.marker, sort_keys=True) + "\n")
        (self.target_repo / ".blk-system-048-disposable-repo").write_text(json.dumps(self.repo_marker, sort_keys=True) + "\n")
        self.used_approvals = set()
        self.used_runs = set()

    def tearDown(self):
        self.tmp.cleanup()

    def _request_and_approval(self, *, approval_id="BLKTEST-S48-L4-APPROVAL-001", run_id="BLK-SYSTEM-048-L4-RUN-001"):
        source_report = build_sprint047_l4_source_report(
            report_path="reports/BLK-SYSTEM-048/disposable-l4-source-report.json",
            beb_id="BEB_S48_L4_DISPOSABLE_REPO_RUNTIME",
            commit_hash=VALID_SOURCE_COMMIT,
            pre_engine_hash=VALID_PRE_ENGINE,
        )
        request = build_sprint047_l4_approval_request(
            source_report=source_report,
            target_identity={
                "approved_repo_path": str(self.target_repo.resolve()),
                "approved_source_subtree": str(self.source_subtree.resolve()),
                "approved_branch": "blk-system-048-disposable-l4-runtime",
                "approved_worktree_id": "worktree-BLK-SYSTEM-048-L4-001",
            },
            workspace_identity={
                "approved_workspace_path": str(self.workspace.resolve()),
                "workspace_clone_id": "workspace-BLK-SYSTEM-048-L4-001",
                "workspace_marker_nonce": self.marker_nonce,
                "source_path_policy": "read-only-disposable-real-repo-copy-no-mutation",
            },
            timeout_output_profile={
                "timeout_class": "bounded-blk-test-l4-disposable-runtime-short",
                "timeout_seconds": 5,
                "output_byte_limit": 4096,
                "compression": "line-dedupe-byte-bound-redacted",
            },
        )
        base_approval = build_sprint047_l4_approval_record(
            authorization_request=request,
            approval_id=approval_id,
            run_id=run_id,
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )
        approval = build_sprint048_runtime_approval_record(base_approval)
        return request, approval

    def test_successful_disposable_real_repo_ast_validation_returns_evidence_only(self):
        request, approval = self._request_and_approval()

        evidence = run_blk_test_l4_disposable_repo_runtime(
            authorization_request=request,
            approval_record=approval,
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-048-L4-RUN-001",
            now=NOW,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            target_repo_path=self.target_repo,
            source_subtree_path=self.source_subtree,
            workspace_path=self.workspace,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )

        self.assertEqual(evidence["pilot_status"], L4_PASS)
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["files_checked"], ["good.py"])
        self.assertTrue(evidence["fixed_tool_executed"])
        self.assertFalse(evidence["source_write_allowed"])
        self.assertFalse(evidence["git_mutation_detected"])
        self.assertFalse(evidence["source_mutation_detected"])
        self.assertFalse(evidence["active_vault_read"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertIn("BLKTEST-S48-L4-APPROVAL-001", self.used_approvals)
        self.assertIn("BLK-SYSTEM-048-L4-RUN-001", self.used_runs)

    def test_syntax_error_returns_fail_evidence_not_publication_or_rtm(self):
        (self.source_subtree / "bad.py").write_text("def broken(:\n")
        request, approval = self._request_and_approval()

        evidence = run_blk_test_l4_disposable_repo_runtime(
            authorization_request=request,
            approval_record=approval,
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-048-L4-RUN-001",
            now=NOW,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            target_repo_path=self.target_repo,
            source_subtree_path=self.source_subtree,
            workspace_path=self.workspace,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )

        self.assertEqual(evidence["pilot_status"], L4_FAIL)
        self.assertEqual(evidence["status"], "FAIL")
        self.assertTrue(evidence["diagnostics"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")

    def test_replay_and_wrong_checkpoint_block_before_runtime(self):
        request, approval = self._request_and_approval()
        self.used_approvals.add("BLKTEST-S48-L4-APPROVAL-001")
        with self.assertRaisesRegex(ValueError, "replay"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        self.used_approvals.clear()
        with self.assertRaisesRegex(ValueError, "BLK-SYSTEM-048"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=PREFLIGHT_APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

    def test_primary_repo_protected_descendant_and_unknown_tool_block(self):
        request, approval = self._request_and_approval()
        with self.assertRaisesRegex(ValueError, "primary BLK-System repo"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=Path(__file__).resolve().parents[1],
                source_subtree_path=Path(__file__).resolve().parents[1] / "python",
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        (self.source_subtree / "docs" / "active").mkdir(parents=True)
        (self.source_subtree / "docs" / "active" / "REQ.md").write_text("protected\n")
        with self.assertRaisesRegex(ValueError, "protected BLK-req"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        (self.source_subtree / "docs" / "active" / "REQ.md").unlink()
        with self.assertRaisesRegex(ValueError, "requested_tool"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="pytest",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )


    def test_replay_blocks_before_any_source_hashing(self):
        request, approval = self._request_and_approval()
        self.used_approvals.add("BLKTEST-S48-L4-APPROVAL-001")
        with patch("blk_test_fixed_tool_l4_disposable_repo_runtime._hash_bytes", side_effect=AssertionError("hash before replay")):
            with self.assertRaisesRegex(ValueError, "replay"):
                run_blk_test_l4_disposable_repo_runtime(
                    authorization_request=request,
                    approval_record=approval,
                    requested_tool="run_ast_validation",
                    run_id="BLK-SYSTEM-048-L4-RUN-001",
                    now=NOW,
                    human_approval_checkpoint=APPROVAL_CHECKPOINT,
                    used_approval_ids=self.used_approvals,
                    used_run_ids=self.used_runs,
                    target_repo_path=self.target_repo,
                    source_subtree_path=self.source_subtree,
                    workspace_path=self.workspace,
                    implementation_commit_hash=VALID_IMPLEMENTATION,
                    driver_hash=VALID_DRIVER,
                )

    def test_missing_git_and_runtime_extension_placeholders_fail_closed(self):
        request, approval = self._request_and_approval()
        shutil.rmtree(self.target_repo / ".git")
        with self.assertRaisesRegex(ValueError, "real Git repository"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        (self.target_repo / ".git").mkdir()
        with self.assertRaisesRegex(ValueError, "real Git repository"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=set(),
                used_run_ids=set(),
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )
        shutil.rmtree(self.target_repo / ".git")
        fake_git = self.target_repo / ".git"
        (fake_git / "objects").mkdir(parents=True)
        (fake_git / "refs" / "heads").mkdir(parents=True)
        forged_hash = "f" * 40
        (fake_git / "HEAD").write_text("ref: refs/heads/blk-system-048-disposable-l4-runtime\n")
        (fake_git / "refs" / "heads" / "blk-system-048-disposable-l4-runtime").write_text(forged_hash + "\n")
        forged_object = fake_git / "objects" / forged_hash[:2] / forged_hash[2:]
        forged_object.parent.mkdir(parents=True, exist_ok=True)
        forged_object.write_bytes(zlib.compress(b"commit 21\x00tree " + (b"0" * 40) + b"\n"))
        forged_marker = dict(self.repo_marker)
        forged_marker["git_head_commit"] = forged_hash
        (self.target_repo / ".blk-system-048-disposable-repo").write_text(json.dumps(forged_marker, sort_keys=True) + "\n")
        with self.assertRaisesRegex(ValueError, "real Git repository"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=set(),
                used_run_ids=set(),
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        shutil.rmtree(self.target_repo / ".git")
        subprocess.run(
            ["git", "init", "-b", "blk-system-048-disposable-l4-runtime"],
            cwd=self.target_repo,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        missing = dict(approval)
        missing["sprint048_runtime"] = dict(approval["sprint048_runtime"])
        del missing["sprint048_runtime"]["runtime_notes"]
        with self.assertRaisesRegex(ValueError, "runtime_notes"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=missing,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

    def test_alt_pass_beo_rtm_laundering_and_tiny_output_limit_fail_closed(self):
        request, approval = self._request_and_approval()
        tainted = dict(approval)
        tainted["sprint048_runtime"] = dict(approval["sprint048_runtime"])
        tainted["sprint048_runtime"]["runtime_notes"] = "PASS authorizes BEO and RTM"
        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=tainted,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )

        tiny_request = dict(request)
        tiny_request["timeout_output_profile"] = dict(request["timeout_output_profile"])
        tiny_request["timeout_output_profile"]["output_byte_limit"] = 128
        tiny_approval = build_sprint047_l4_approval_record(
            authorization_request=tiny_request,
            approval_id="BLKTEST-S48-L4-APPROVAL-TINY",
            run_id="BLK-SYSTEM-048-L4-RUN-TINY",
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )
        tiny_approval = build_sprint048_runtime_approval_record(tiny_approval)
        marker = dict(self.marker)
        (self.workspace / ".blk-system-047-l4-workspace").write_text(json.dumps(marker, sort_keys=True) + "\n")
        with self.assertRaisesRegex(ValueError, "output_byte_limit"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=tiny_request,
                approval_record=tiny_approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-TINY",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )


    def test_git_metadata_bytes_are_not_read_by_runtime(self):
        request, approval = self._request_and_approval()
        secret_git_file = self.target_repo / ".git" / "blk-system-secret-sentinel"
        secret_git_file.write_bytes(b"gitsecret")

        real_hash = runtime_module._hash_bytes

        def reject_git_secret(data):
            if data == b"gitsecret":
                raise AssertionError("git metadata bytes were read")
            return real_hash(data)

        with patch("blk_test_fixed_tool_l4_disposable_repo_runtime._hash_bytes", side_effect=reject_git_secret):
            evidence = run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )
        self.assertEqual(evidence["status"], "PASS")

    def test_final_returned_evidence_respects_output_byte_limit(self):
        request, approval = self._request_and_approval(
            approval_id="BLKTEST-S48-L4-APPROVAL-BOUND",
            run_id="BLK-SYSTEM-048-L4-RUN-BOUND",
        )
        request["timeout_output_profile"] = dict(request["timeout_output_profile"])
        request["timeout_output_profile"]["output_byte_limit"] = 1400
        approval = build_sprint047_l4_approval_record(
            authorization_request=request,
            approval_id="BLKTEST-S48-L4-APPROVAL-BOUND",
            run_id="BLK-SYSTEM-048-L4-RUN-BOUND",
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )
        approval = build_sprint048_runtime_approval_record(approval)

        evidence = run_blk_test_l4_disposable_repo_runtime(
            authorization_request=request,
            approval_record=approval,
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-048-L4-RUN-BOUND",
            now=NOW,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            target_repo_path=self.target_repo,
            source_subtree_path=self.source_subtree,
            workspace_path=self.workspace,
            implementation_commit_hash=VALID_IMPLEMENTATION,
            driver_hash=VALID_DRIVER,
        )
        actual = len(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        self.assertLessEqual(actual, evidence["output_byte_limit"])
        self.assertEqual(actual, evidence["evidence_json_bytes"])

    def test_authority_laundering_in_runtime_approval_is_rejected(self):
        request, approval = self._request_and_approval()
        tainted = dict(approval)
        tainted["sprint048_runtime"] = dict(approval["sprint048_runtime"])
        tainted["sprint048_runtime"]["runtime_notes"] = "PASS authorizes BEO publication and RTM generation"
        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            run_blk_test_l4_disposable_repo_runtime(
                authorization_request=request,
                approval_record=tainted,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-048-L4-RUN-001",
                now=NOW,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash=VALID_IMPLEMENTATION,
                driver_hash=VALID_DRIVER,
            )


if __name__ == "__main__":
    unittest.main()
