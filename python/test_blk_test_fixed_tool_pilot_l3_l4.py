import ast
import tempfile
import unittest
from pathlib import Path

from blk_test_fixed_tool_pilot_l3_l4 import (
    APPROVAL_CHECKPOINT,
    L3_PASS,
    L4_BLOCKED,
    build_sprint046_approval_record,
    build_sprint046_authorization_request,
    build_sprint046_synthetic_source_report,
    evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight,
    evaluate_l4_real_repo_pilot_preflight,
    run_blk_test_l3_synthetic_fixed_tool_pilot,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "blk_test_fixed_tool_pilot_l3_l4.py"
NOW = "2026-05-09T10:45:00Z"
ISSUED = "2026-05-09T10:30:00Z"
EXPIRES = "2026-05-09T11:00:00Z"


class BlkTestFixedToolPilotL3L4Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name) / "blk-system-046-synthetic-workspace"
        (self.workspace / "src").mkdir(parents=True)
        (self.workspace / ".blk-system-046-synthetic-workspace").write_text("owned\n")
        (self.workspace / ".blk-system-014-synthetic-workspace").write_text("compat-harness\n")
        (self.workspace / "src" / "smoke_fixture.py").write_text("SMOKE_FIXTURE = True\n")
        self.used_approvals = set()
        self.used_runs = set()

    def tearDown(self):
        self.tmp.cleanup()

    def _request_and_approval(self, *, output_byte_limit=4096):
        source_report = build_sprint046_synthetic_source_report()
        request = build_sprint046_authorization_request(
            source_report=source_report,
            workspace_identity={
                "target_branch": "synthetic-blk-system-046-pilot",
                "workspace_clone_id": "workspace-BLK-SYSTEM-046-L3-001",
                "source_path_policy": "synthetic-isolated-copy-only",
            },
            timeout_output_profile={
                "timeout_class": "bounded-blk-test-pilot-short",
                "timeout_seconds": 5,
                "output_byte_limit": output_byte_limit,
                "compression": "line-dedupe-byte-bound",
            },
        )
        approval = build_sprint046_approval_record(
            authorization_request=request,
            approval_id="BLKTEST-S46-L3-APPROVAL-001",
            run_id="BLK-SYSTEM-046-L3-RUN-001",
            operator_identity="operator:camcamcami",
            source_system="discord-dm",
            issued_at=ISSUED,
            expires_at=EXPIRES,
        )
        return source_report, request, approval

    def test_preflight_accepts_selected_frontier_without_starting_process(self):
        _source_report, request, approval = self._request_and_approval()

        preflight = evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
            authorization_request=request,
            approval_record=approval,
            selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-046-L3-RUN-001",
            now=NOW,
            pilot_enabled=True,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            target_mode="synthetic_l3",
        )

        self.assertEqual(preflight["decision"], "BLK_TEST_L3_SYNTHETIC_PREFLIGHT_ACCEPTED")
        self.assertEqual(preflight["selected_frontier"], "blk_test_fixed_tool_pilot_l3_l4")
        self.assertEqual(preflight["l4_real_repo_pilot"], L4_BLOCKED)
        self.assertFalse(preflight["subprocess_called"])
        self.assertFalse(preflight["source_write_allowed"])
        self.assertEqual(preflight["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(preflight["rtm_status"], "NOT_GENERATED")

    def test_successful_l3_synthetic_pilot_returns_evidence_only_and_cleans_workspace(self):
        source_report, request, approval = self._request_and_approval()

        evidence = run_blk_test_l3_synthetic_fixed_tool_pilot(
            source_report=source_report,
            authorization_request=request,
            approval_record=approval,
            workspace_path=self.workspace,
            selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-046-L3-RUN-001",
            now=NOW,
            pilot_enabled=True,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            implementation_commit_hash="synthetic-task-002",
            driver_hash="sha256:" + "4" * 64,
        )

        self.assertEqual(evidence["pilot_status"], L3_PASS)
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["tool_name"], "run_ast_validation")
        self.assertTrue(evidence["subprocess_called"])
        self.assertFalse(evidence["source_write_allowed"])
        self.assertFalse(evidence["active_vault_read"])
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        self.assertEqual(evidence["l4_real_repo_pilot"], L4_BLOCKED)
        self.assertEqual(evidence["cleanup_status"], "CLEANED")
        self.assertFalse(self.workspace.exists())
        self.assertIn("BLKTEST-S46-L3-APPROVAL-001", self.used_approvals)
        self.assertIn("BLK-SYSTEM-046-L3-RUN-001", self.used_runs)

    def test_replay_and_missing_replay_sets_fail_before_process_start(self):
        source_report, request, approval = self._request_and_approval()

        with self.assertRaisesRegex(ValueError, "used_approval_ids"):
            run_blk_test_l3_synthetic_fixed_tool_pilot(
                source_report=source_report,
                authorization_request=request,
                approval_record=approval,
                workspace_path=self.workspace,
                selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-046-L3-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=None,
                used_run_ids=self.used_runs,
                implementation_commit_hash="synthetic-task-002",
                driver_hash="sha256:" + "4" * 64,
            )

        with self.assertRaisesRegex(ValueError, "replay"):
            run_blk_test_l3_synthetic_fixed_tool_pilot(
                source_report=source_report,
                authorization_request=request,
                approval_record=approval,
                workspace_path=self.workspace,
                selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-046-L3-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids={"BLKTEST-S46-L3-APPROVAL-001"},
                used_run_ids=set(),
                implementation_commit_hash="synthetic-task-002",
                driver_hash="sha256:" + "4" * 64,
            )

    def test_wrong_frontier_l4_real_repo_and_adjacent_authority_fail_closed(self):
        _source_report, request, approval = self._request_and_approval()
        with self.assertRaisesRegex(ValueError, "selected_frontier"):
            evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
                authorization_request=request,
                approval_record=approval,
                selected_frontier="codex_live_dispatch_l3_smoke",
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-046-L3-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_mode="synthetic_l3",
            )
        with self.assertRaisesRegex(ValueError, "exact target approval"):
            evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
                authorization_request=request,
                approval_record=approval,
                selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-046-L3-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_mode="real_repo_l4",
            )
        tainted = dict(approval)
        tainted["approval_kind"] = "codex-live"
        with self.assertRaisesRegex(ValueError, "codex-live"):
            evaluate_blk_test_fixed_tool_pilot_l3_l4_preflight(
                authorization_request=request,
                approval_record=tainted,
                selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
                requested_tool="run_ast_validation",
                run_id="BLK-SYSTEM-046-L3-RUN-001",
                now=NOW,
                pilot_enabled=True,
                human_approval_checkpoint=APPROVAL_CHECKPOINT,
                used_approval_ids=self.used_approvals,
                used_run_ids=self.used_runs,
                target_mode="synthetic_l3",
            )

    def test_l4_preflight_reports_blocked_without_side_effects(self):
        result = evaluate_l4_real_repo_pilot_preflight(target_repo_path="/home/dad/BLK-System")

        self.assertEqual(result["pilot_status"], L4_BLOCKED)
        self.assertFalse(result["subprocess_called"])
        self.assertFalse(result["fixed_tool_executed"])
        self.assertFalse(result["source_mutation_attempted"])
        self.assertFalse(result["protected_body_read_attempted"])
        self.assertEqual(result["blocked_reason"], "exact L4 target approval required")

    def test_output_flood_is_bounded_and_non_success(self):
        source_report, request, approval = self._request_and_approval(output_byte_limit=64)
        (self.workspace / "src" / "smoke_fixture.py").write_text("FLOOD_FIXTURE = True\nSMOKE_FIXTURE = True\n")

        evidence = run_blk_test_l3_synthetic_fixed_tool_pilot(
            source_report=source_report,
            authorization_request=request,
            approval_record=approval,
            workspace_path=self.workspace,
            selected_frontier="blk_test_fixed_tool_pilot_l3_l4",
            requested_tool="run_ast_validation",
            run_id="BLK-SYSTEM-046-L3-RUN-001",
            now=NOW,
            pilot_enabled=True,
            human_approval_checkpoint=APPROVAL_CHECKPOINT,
            used_approval_ids=self.used_approvals,
            used_run_ids=self.used_runs,
            implementation_commit_hash="synthetic-task-002",
            driver_hash="sha256:" + "4" * 64,
        )

        self.assertEqual(evidence["status"], "FATAL_OUTPUT_FLOOD")
        self.assertLessEqual(evidence["output_bytes_returned"], 64)
        self.assertNotEqual(evidence["pilot_status"], L3_PASS)
        self.assertFalse(evidence["beo_publication"] == "PUBLISHED")

    def test_source_ast_has_no_direct_network_shell_or_mutation_calls(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"socket", "requests", "urllib", "http", "ftplib", "paramiko", "git"}
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
