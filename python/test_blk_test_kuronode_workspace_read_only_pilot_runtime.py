from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from blk_test_kuronode_workspace_read_only_pilot_runtime import (
    APPROVAL_ID,
    EXCLUDED_AUTHORITIES,
    PASS_STATUS,
    PROOF_MARKERS,
    RUN_ID,
    RUNTIME_AUTHORIZATION_STATUS,
    PilotRuntimeEnvelope,
    build_runtime_authorization,
    run_blk_test_kuronode_workspace_read_only_pilot,
    _run_blk_test_kuronode_workspace_read_only_pilot_for_tests,
    reset_process_replay_for_tests,
)


class KuronodeWorkspaceReadOnlyPilotRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        reset_process_replay_for_tests()

    def _repo(self, root: Path, *, head: str = "a" * 40, content: str | None = None) -> tuple[Path, Path]:
        repo = root / "Kuronode-v1"
        scripts = repo / "scripts"
        scripts.mkdir(parents=True)
        (scripts / "smoke_test.ts").write_text(
            content
            or "type ProjectionResult = { streamId: string; ast?: unknown };\n"
            "const isProjectionResult = (value: unknown): value is ProjectionResult => {\n"
            "  return typeof value === 'object' && value !== null;\n"
            "};\n",
            encoding="utf-8",
        )
        git_ref = repo / ".git" / "refs" / "heads"
        remote_ref = repo / ".git" / "refs" / "remotes" / "origin"
        git_ref.mkdir(parents=True)
        remote_ref.mkdir(parents=True)
        (repo / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (git_ref / "main").write_text(head + "\n", encoding="utf-8")
        (remote_ref / "main").write_text(head + "\n", encoding="utf-8")
        return repo, scripts

    def _envelope(self, root: Path, repo: Path, scripts: Path, *, head: str = "a" * 40) -> PilotRuntimeEnvelope:
        return PilotRuntimeEnvelope(
            sprint="BLK-SYSTEM-073",
            approval_id="APPROVAL-BLK-SYSTEM-073-TEST-001",
            run_id="RUN-BLK-SYSTEM-073-TEST-001",
            expected_head=head,
            approved_target_repo=repo,
            approved_source_subtree=scripts,
            approved_workspace=root / "runtime-workspace",
            replay_ledger_path=root / "replay-ledger.json",
            marker_nonce_binding="BLK-SYSTEM-073",
            workspace_marker_name=".blk-system-073-test-runtime-workspace",
        )

    def _upstream(self, envelope: PilotRuntimeEnvelope) -> dict[str, object]:
        upstream = {
            "status": "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "approval_scope": "BLK_TEST_KURONODE_WORKSPACE_EXACT_TARGET_APPROVAL_ENVELOPE_REVIEW_ONLY",
            "target_repo_path": str(envelope.approved_target_repo),
            "target_branch": "main",
            "target_head_sha": envelope.expected_head,
            "workspace_status": "main...origin/main",
            "fixed_tool": "run_ast_validation",
            "tool_mode": "READ_ONLY_STATIC_AST_VALIDATION_FUTURE_RUNTIME_ONLY",
            "replay_consumed": False,
            "one_use_id_status": "FUTURE_RUNTIME_CANDIDATES_NOT_CONSUMED_BY_REVIEW",
            "runtime_approved": False,
            "blk_test_runtime_executed": False,
            "source_mutation_allowed": False,
            "git_mutation_allowed": False,
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "coverage_claim_status": "NOT_PROMOTED",
            "production_mcp_authorized": False,
            "generic_mcp_authorized": False,
            "protected_body_read_allowed": False,
            "ceb009_reuse_allowed": False,
            "production_isolation_claimed": False,
        }
        upstream["envelope_hash"] = self._hash({k: v for k, v in upstream.items() if k != "envelope_hash"})
        return upstream

    def _authorization(self, envelope: PilotRuntimeEnvelope, *, remote_head: str | None = None) -> dict[str, object]:
        return build_runtime_authorization(
            approval_id=envelope.approval_id,
            run_id=envelope.run_id,
            target_repo_path=str(envelope.approved_target_repo),
            source_subtree_path=str(envelope.approved_source_subtree),
            expected_head=envelope.expected_head,
            observed_remote_head=remote_head or envelope.expected_head,
        )

    def _hash(self, value: dict[str, object]) -> str:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def test_read_only_pilot_passes_and_cleans_workspace_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)

            result = _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(
                upstream_envelope=self._upstream(envelope),
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                approval_envelope=envelope,
            )

            self.assertEqual(result["pilot_status"], PASS_STATUS)
            self.assertEqual(result["status"], "PASS")
            self.assertTrue(result["fixed_tool_executed"])
            self.assertEqual(result["files_checked"], ["smoke_test.ts"])
            self.assertEqual(result["findings"], [])
            self.assertTrue(result["replay_consumed_before_runtime"])
            self.assertFalse(result["source_mutation_detected"])
            self.assertFalse(result["git_mutation_detected"])
            self.assertTrue(result["workspace_cleanup_verified"])
            self.assertFalse(envelope.approved_workspace.exists())
            actual_size = len(json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            self.assertEqual(result["evidence_json_bytes"], actual_size)
            self.assertLessEqual(actual_size, result["output_byte_limit"])

    def test_target_head_drift_blocks_after_replay_consumption_without_tool_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root, head="b" * 40)
            envelope = self._envelope(root, repo, scripts, head="a" * 40)
            used_approvals: set[str] = set()
            used_runs: set[str] = set()

            result = _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(
                upstream_envelope=self._upstream(envelope),
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                used_approval_ids=used_approvals,
                used_run_ids=used_runs,
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                approval_envelope=envelope,
            )

            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("target HEAD mismatch", result["block_reason"])
            self.assertFalse(result["fixed_tool_executed"])
            self.assertTrue(result["replay_consumed_before_runtime"])
            self.assertIn(envelope.approval_id, used_approvals)
            self.assertIn(envelope.run_id, used_runs)

    def test_replay_sets_durable_ledger_and_process_replay_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            kwargs = dict(
                upstream_envelope=self._upstream(envelope),
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                approval_envelope=envelope,
            )
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**kwargs, used_approval_ids=None, used_run_ids=set())
            _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**kwargs, used_approval_ids=set(), used_run_ids=set())
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**kwargs, used_approval_ids=set(), used_run_ids=set())

    def test_path_alias_secret_scope_preowned_workspace_and_low_output_cap_block_before_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            base = dict(
                upstream_envelope=self._upstream(envelope),
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                approval_envelope=envelope,
            )
            for overrides in [
                {"target_repo_path": str(repo) + "/."},
                {"source_subtree_path": str(scripts) + "/."},
                {"workspace_clone_path": str(envelope.approved_workspace) + "/."},
                {"output_byte_limit": 100},
            ]:
                reset_process_replay_for_tests()
                with self.subTest(overrides=overrides):
                    with self.assertRaises(ValueError):
                        _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**{**base, **overrides})

            (scripts / ".env.local").write_text("SECRET=1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**base)
            (scripts / ".env.local").unlink()
            envelope.approved_workspace.mkdir()
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(**base)
            self.assertTrue(envelope.approved_workspace.exists(), "pre-owned workspace must not be deleted")

    def test_remote_tracking_head_mismatch_blocks_after_replay_before_tool_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root, head="a" * 40)
            (repo / ".git" / "refs" / "remotes" / "origin" / "main").write_text("b" * 40 + "\n", encoding="utf-8")
            envelope = self._envelope(root, repo, scripts, head="a" * 40)
            used_approvals: set[str] = set()
            used_runs: set[str] = set()

            result = _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(
                upstream_envelope=self._upstream(envelope),
                runtime_authorization=self._authorization(envelope, remote_head="b" * 40),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                used_approval_ids=used_approvals,
                used_run_ids=used_runs,
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                approval_envelope=envelope,
            )

            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("observed remote HEAD mismatch", result["block_reason"])
            self.assertEqual(result["observed_remote_head"], "b" * 40)
            self.assertFalse(result["fixed_tool_executed"])
            self.assertIn(envelope.approval_id, used_approvals)
            self.assertIn(envelope.run_id, used_runs)

    def test_public_production_entrypoint_rejects_already_retired_default_ids(self):
        with self.assertRaisesRegex(ValueError, "already retired"):
            run_blk_test_kuronode_workspace_read_only_pilot(
                upstream_envelope={},
                runtime_authorization={},
                target_repo_path="/home/dad/code/Kuronode-v1",
                source_subtree_path="/home/dad/code/Kuronode-v1/scripts",
                workspace_clone_path="/tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace",
                approval_id=APPROVAL_ID,
                run_id=RUN_ID,
                expected_head="38e332b188e45edcb484765694112c9041ad1a3b",
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-11T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-073-kuronode-read-only-pilot-001",
            )

    def test_upstream_and_authorization_laundering_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            upstream = self._upstream(envelope)
            upstream["runtime_approved"] = True
            upstream["envelope_hash"] = self._hash({k: v for k, v in upstream.items() if k != "envelope_hash"})
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(
                    upstream_envelope=upstream,
                    runtime_authorization=self._authorization(envelope),
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-11T00:00:00+00:00",
                    used_approval_ids=set(),
                    used_run_ids=set(),
                    workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                    approval_envelope=envelope,
                )

            authorization = self._authorization(envelope)
            authorization["operator_note"] = "runtime approval: yes; BEO is PUBLISHED"
            with self.assertRaises(ValueError):
                _run_blk_test_kuronode_workspace_read_only_pilot_for_tests(
                    upstream_envelope=self._upstream(envelope),
                    runtime_authorization=authorization,
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-11T00:00:00+00:00",
                    used_approval_ids=set(),
                    used_run_ids=set(),
                    workspace_marker_nonce="nonce-BLK-SYSTEM-073-TEST-001",
                    approval_envelope=envelope,
                )

    def test_default_authorization_constants_are_exact(self):
        authorization = build_runtime_authorization(
            approval_id=APPROVAL_ID,
            run_id=RUN_ID,
            target_repo_path="/home/dad/code/Kuronode-v1",
            source_subtree_path="/home/dad/code/Kuronode-v1/scripts",
            expected_head="38e332b188e45edcb484765694112c9041ad1a3b",
            observed_remote_head="38e332b188e45edcb484765694112c9041ad1a3b",
        )
        self.assertEqual(authorization["authorization_status"], RUNTIME_AUTHORIZATION_STATUS)
        self.assertEqual(set(authorization["proof_markers"]), PROOF_MARKERS)
        self.assertEqual(set(authorization["excluded_authorities"]), EXCLUDED_AUTHORITIES)


if __name__ == "__main__":
    unittest.main()
