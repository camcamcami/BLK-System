import json
import tempfile
import unittest
from pathlib import Path

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
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.target_repo = self.base / "disposable-real-repo"
        self.source_subtree = self.target_repo / "src"
        self.workspace = self.base / "approved-workspace"
        self.marker_nonce = "nonce-BLK-SYSTEM-048-L4-RUN-001"
        self.source_subtree.mkdir(parents=True)
        (self.target_repo / ".git").mkdir()
        (self.source_subtree / "good.py").write_text("VALUE = 48\n")
        self.workspace.mkdir()
        self.marker = {
            "workspace_marker_nonce": self.marker_nonce,
            "workspace_clone_id": "workspace-BLK-SYSTEM-048-L4-001",
            "approved_repo_path": str(self.target_repo.resolve()),
            "approved_source_subtree": str(self.source_subtree.resolve()),
            "approved_branch": "blk-system-048-disposable-l4-runtime",
            "approved_worktree_id": "worktree-BLK-SYSTEM-048-L4-001",
        }
        (self.workspace / ".blk-system-047-l4-workspace").write_text(json.dumps(self.marker, sort_keys=True) + "\n")
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
