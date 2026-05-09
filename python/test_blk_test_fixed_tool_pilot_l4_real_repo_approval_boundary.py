import ast
import tempfile
import unittest
from pathlib import Path

from blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary import (
    APPROVAL_CHECKPOINT,
    BLOCKED,
    PREFLIGHT_READY,
    build_sprint047_l4_approval_record,
    build_sprint047_l4_approval_request,
    build_sprint047_l4_source_report,
    evaluate_blk_test_l4_real_repo_preflight,
    evaluate_l4_missing_exact_target_preflight,
    run_blk_test_l4_real_repo_pilot,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary.py"
NOW = "2026-05-09T11:30:00Z"
ISSUED = "2026-05-09T11:00:00Z"
EXPIRES = "2026-05-09T12:00:00Z"


class BlkTestFixedToolPilotL4ApprovalBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.target_repo = self.base / "target-repo"
        self.source_subtree = self.target_repo / "src"
        self.workspace = self.base / "approved-workspace-clone"
        self.marker_nonce = "nonce-BLK-SYSTEM-047-L4-001"
        self.source_subtree.mkdir(parents=True)
        (self.target_repo / ".git").mkdir()
        (self.source_subtree / "example.py").write_text("VALUE = 47\n")
        self.workspace.mkdir()
        (self.workspace / ".blk-system-047-l4-workspace").write_text(self.marker_nonce + "\n")
        self.used_approvals = set()
        self.used_runs = set()

    def tearDown(self):
        self.tmp.cleanup()

    def _request_and_approval(self, *, approval_id="BLKTEST-S47-L4-APPROVAL-001", run_id="BLK-SYSTEM-047-L4-RUN-001"):
        source_report = build_sprint047_l4_source_report(
            report_path="reports/BLK-SYSTEM-047/l4-source-report.json",
            beb_id="BEB_S47_L4_APPROVAL_BOUNDARY",
            commit_hash="sha256:" + "a" * 64,
            pre_engine_hash="sha256:" + "b" * 64,
        )
        request = build_sprint047_l4_approval_request(
            source_report=source_report,
            target_identity={
                "approved_repo_path": str(self.target_repo.resolve()),
                "approved_source_subtree": str(self.source_subtree.resolve()),
                "approved_branch": "blk-system-047-l4-approval-boundary",
                "approved_worktree_id": "worktree-BLK-SYSTEM-047-L4-001",
            },
            workspace_identity={
                "approved_workspace_path": str(self.workspace.resolve()),
                "workspace_clone_id": "workspace-BLK-SYSTEM-047-L4-001",
                "workspace_marker_nonce": self.marker_nonce,
                "source_path_policy": "read-only-real-repo-copy-no-mutation",
            },
            timeout_output_profile={
                "timeout_class": "bounded-blk-test-l4-readonly-short",
                "timeout_seconds": 5,
                "output_byte_limit": 4096,
                "compression": "line-dedupe-byte-bound-redacted",
            },
        )
        approval = build_sprint047_l4_approval_record(
            authorization_request=request,
            approval_id=approval_id,
            run_id=run_id,
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash="task-002-fixture",
            driver_hash="sha256:" + "c" * 64,
        )
        return source_report, request, approval

    def test_complete_exact_target_envelope_is_ready_but_not_executed(self):
        _source_report, request, approval = self._request_and_approval()

        preflight = evaluate_blk_test_l4_real_repo_preflight(
            authorization_request=request,
            approval_record=approval,
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-047-L4-RUN-001",
            now=NOW,
            pilot_enabled=False,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            target_repo_path=self.target_repo,
            source_subtree_path=self.source_subtree,
            workspace_path=self.workspace,
            implementation_commit_hash="task-002-fixture",
            driver_hash="sha256:" + "c" * 64,
        )

        self.assertEqual(preflight["decision"], PREFLIGHT_READY)
        self.assertEqual(preflight["sprint"], "BLK-SYSTEM-047")
        self.assertEqual(preflight["requested_tool"], "run_ast_validation")
        self.assertFalse(preflight["fixed_tool_executed"])
        self.assertFalse(preflight["subprocess_called"])
        self.assertFalse(preflight["source_write_allowed"])
        self.assertFalse(preflight["active_vault_read"])
        self.assertEqual(preflight["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(preflight["rtm_status"], "NOT_GENERATED")
        self.assertEqual(self.used_approvals, set())
        self.assertEqual(self.used_runs, set())

    def test_missing_exact_target_is_blocked_without_side_effects_or_replay_consumption(self):
        result = evaluate_l4_missing_exact_target_preflight(
            target_repo_path="",
            requested_tool="run_ast_validation",
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
        )

        self.assertEqual(result["pilot_status"], BLOCKED)
        self.assertEqual(result["blocked_reason"], "complete exact L4 target approval envelope required")
        self.assertFalse(result["fixed_tool_executed"])
        self.assertFalse(result["subprocess_called"])
        self.assertFalse(result["source_mutation_attempted"])
        self.assertFalse(result["protected_body_read_attempted"])
        self.assertEqual(self.used_approvals, set())
        self.assertEqual(self.used_runs, set())

    def test_runtime_entrypoint_is_disabled_even_with_ready_preflight(self):
        _source_report, request, approval = self._request_and_approval()

        with self.assertRaisesRegex(RuntimeError, "no L4 runtime execution in BLK-SYSTEM-047"):
            run_blk_test_l4_real_repo_pilot(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )
        self.assertEqual(self.used_approvals, set())
        self.assertEqual(self.used_runs, set())

    def test_rejects_primary_repo_protected_subtree_and_workspace_escape(self):
        _source_report, request, approval = self._request_and_approval()
        bad_request = dict(request)
        bad_request["target_identity"] = dict(request["target_identity"])
        bad_request["target_identity"]["approved_repo_path"] = str(ROOT)
        bad_request["target_identity"]["approved_source_subtree"] = str((ROOT / "python").resolve())
        bad_approval = build_sprint047_l4_approval_record(
            authorization_request=bad_request,
            approval_id="BLKTEST-S47-L4-APPROVAL-PRIMARY",
            run_id="BLK-SYSTEM-047-L4-RUN-PRIMARY",
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash="task-002-fixture",
            driver_hash="sha256:" + "c" * 64,
        )
        with self.assertRaisesRegex(ValueError, "primary BLK-System repo"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=bad_request,
                approval_record=bad_approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-PRIMARY",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=ROOT,
                source_subtree_path=ROOT / "python",
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

        protected = self.target_repo / "docs" / "active"
        protected.mkdir(parents=True)
        bad_request = dict(request)
        bad_request["target_identity"] = dict(request["target_identity"])
        bad_request["target_identity"]["approved_source_subtree"] = str(protected.resolve())
        bad_approval = build_sprint047_l4_approval_record(
            authorization_request=bad_request,
            approval_id="BLKTEST-S47-L4-APPROVAL-002",
            run_id="BLK-SYSTEM-047-L4-RUN-002",
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
            implementation_commit_hash="task-002-fixture",
            driver_hash="sha256:" + "c" * 64,
        )
        with self.assertRaisesRegex(ValueError, "protected BLK-req"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=bad_request,
                approval_record=bad_approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-002",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=protected,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

        outside = self.base / "outside-secret"
        outside.mkdir()
        (self.workspace / "escape").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink escape"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

    def test_rejects_laundered_authority_nested_fields_and_unknown_tool(self):
        _source_report, request, approval = self._request_and_approval()
        tainted = dict(approval)
        tainted["sprint047_l4_approval"] = dict(approval["sprint047_l4_approval"])
        tainted["sprint047_l4_approval"]["hostile_review_criteria"] = ["ok", "PASS means BEO publication approved"]
        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=tainted,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

        bad_request = dict(request)
        bad_request["rtm_generation"] = "APPROVED_FOR_LIVE_EXECUTION"
        with self.assertRaisesRegex(ValueError, "not allowed"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=bad_request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

        with self.assertRaisesRegex(ValueError, "requested_tool"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=approval,
                requested_tool="pytest",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

    def test_replay_sets_expiry_and_exact_approval_kind_are_required(self):
        _source_report, request, approval = self._request_and_approval()
        with self.assertRaisesRegex(ValueError, "used_approval_ids"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=None,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )
        with self.assertRaisesRegex(ValueError, "replay"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=approval,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids={"BLKTEST-S47-L4-APPROVAL-001"},
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )
        expired = dict(approval)
        expired["expires_at"] = "2026-05-09T11:10:00Z"
        with self.assertRaisesRegex(ValueError, "expired"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=expired,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )
        wrong_kind = dict(approval)
        wrong_kind["approval_kind"] = "blk-pipe-dispatch-approval"
        with self.assertRaisesRegex(ValueError, "approval_kind"):
            evaluate_blk_test_l4_real_repo_preflight(
                authorization_request=request,
                approval_record=wrong_kind,
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-047-L4-RUN-001",
                now=NOW,
                pilot_enabled=False,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_repo_path=self.target_repo,
                source_subtree_path=self.source_subtree,
                workspace_path=self.workspace,
                implementation_commit_hash="task-002-fixture",
                driver_hash="sha256:" + "c" * 64,
            )

    def test_source_ast_has_no_live_process_network_or_mutation_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "paramiko", "git"}
        forbidden_calls = {"eval", "exec", "compile", "open", "__import__"}
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_imports:
                        offenders.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in forbidden_imports:
                    offenders.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                    offenders.append(node.func.id)
                if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen", "Popen", "run"}:
                    offenders.append(node.func.attr)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
