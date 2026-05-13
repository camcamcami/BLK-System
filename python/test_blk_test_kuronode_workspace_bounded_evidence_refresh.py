from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from blk_test_kuronode_workspace_bounded_evidence_refresh import (
    APPROVAL_ID,
    BLOCKED_STATUS,
    EXCLUDED_AUTHORITIES,
    EXPECTED_HEAD,
    FAIL_STATUS,
    NO_SIDE_EFFECT_FLAGS,
    PASS_STATUS,
    PROOF_MARKERS,
    RUN_ID,
    RUNTIME_AUTHORIZATION_STATUS,
    EvidenceRefreshEnvelope,
    build_runtime_authorization,
    runtime_ids_are_retired_by_evidence,
    run_bounded_blk_test_evidence_refresh,
    _run_bounded_blk_test_evidence_refresh_for_tests,
    reset_process_replay_for_tests,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "docs" / "outcomes" / "BLK-SYSTEM-097_runtime-evidence.json"


class KuronodeWorkspaceBoundedEvidenceRefreshTest(unittest.TestCase):
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

    def _envelope(self, root: Path, repo: Path, scripts: Path, *, head: str = "a" * 40) -> EvidenceRefreshEnvelope:
        return EvidenceRefreshEnvelope(
            sprint="BLK-SYSTEM-097",
            approval_id="APPROVAL-BLK-SYSTEM-097-TEST-001",
            run_id="RUN-BLK-SYSTEM-097-TEST-001",
            expected_head=head,
            approved_target_repo=repo,
            approved_source_subtree=scripts,
            approved_workspace=root / "runtime-workspace",
            replay_ledger_path=root / "replay-ledger.json",
            marker_nonce_binding="BLK-SYSTEM-097",
            workspace_marker_name=".blk-system-097-test-runtime-workspace",
        )

    def _authorization(self, envelope: EvidenceRefreshEnvelope, *, remote_head: str | None = None) -> dict[str, object]:
        return build_runtime_authorization(
            approval_id=envelope.approval_id,
            run_id=envelope.run_id,
            target_repo_path=str(envelope.approved_target_repo),
            source_subtree_path=str(envelope.approved_source_subtree),
            expected_head=envelope.expected_head,
            observed_remote_head=remote_head or envelope.expected_head,
        )

    def test_exact_default_scope_uses_fresh_blk_system_097_ids_and_current_kuronode_head(self):
        self.assertEqual(APPROVAL_ID, "APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001")
        self.assertEqual(RUN_ID, "RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001")
        self.assertEqual(EXPECTED_HEAD, "aebea51bed911c781a537d84d38b2dcb838b1368")
        self.assertNotIn("073", APPROVAL_ID)
        self.assertNotIn("073", RUN_ID)
        authorization = build_runtime_authorization(
            approval_id=APPROVAL_ID,
            run_id=RUN_ID,
            target_repo_path="/home/dad/code/Kuronode-v1",
            source_subtree_path="/home/dad/code/Kuronode-v1/scripts",
            expected_head=EXPECTED_HEAD,
            observed_remote_head=EXPECTED_HEAD,
        )
        self.assertEqual(authorization["authorization_status"], RUNTIME_AUTHORIZATION_STATUS)
        self.assertEqual(set(authorization["proof_markers"]), PROOF_MARKERS)
        self.assertEqual(set(authorization["excluded_authorities"]), EXCLUDED_AUTHORITIES)
        self.assertEqual(set(authorization["no_side_effects"]), NO_SIDE_EFFECT_FLAGS)
        self.assertTrue(all(value is False for value in authorization["no_side_effects"].values()))

    def test_private_helper_passes_and_cleans_workspace_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)

            result = _run_bounded_blk_test_evidence_refresh_for_tests(
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
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

    def test_target_and_remote_head_drift_block_after_replay_without_tool_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root, head="b" * 40)
            envelope = self._envelope(root, repo, scripts, head="a" * 40)
            used_approvals: set[str] = set()
            used_runs: set[str] = set()

            result = _run_bounded_blk_test_evidence_refresh_for_tests(
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=used_approvals,
                used_run_ids=used_runs,
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                approval_envelope=envelope,
            )

            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["pilot_status"], BLOCKED_STATUS)
            self.assertIn("target HEAD mismatch", result["block_reason"])
            self.assertFalse(result["fixed_tool_executed"])
            self.assertIn(envelope.approval_id, used_approvals)
            self.assertIn(envelope.run_id, used_runs)

        reset_process_replay_for_tests()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root, head="a" * 40)
            (repo / ".git" / "refs" / "remotes" / "origin" / "main").write_text("b" * 40 + "\n", encoding="utf-8")
            envelope = self._envelope(root, repo, scripts, head="a" * 40)
            result = _run_bounded_blk_test_evidence_refresh_for_tests(
                runtime_authorization=self._authorization(envelope, remote_head="b" * 40),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                approval_envelope=envelope,
            )
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("observed remote HEAD mismatch", result["block_reason"])
            self.assertFalse(result["fixed_tool_executed"])

    def test_replay_path_alias_secret_scope_preowned_workspace_and_low_output_cap_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            base = dict(
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                approval_envelope=envelope,
            )
            with self.assertRaisesRegex(ValueError, "caller-owned replay sets are required"):
                _run_bounded_blk_test_evidence_refresh_for_tests(**{**base, "used_approval_ids": None})
            _run_bounded_blk_test_evidence_refresh_for_tests(**base)
            with self.assertRaisesRegex(ValueError, "replay detected"):
                _run_bounded_blk_test_evidence_refresh_for_tests(**{**base, "used_approval_ids": set(), "used_run_ids": set()})

        alias_cases = [
            lambda repo, scripts, envelope: {"target_repo_path": str(repo) + "/."},
            lambda repo, scripts, envelope: {"source_subtree_path": str(scripts) + "/."},
            lambda repo, scripts, envelope: {"workspace_clone_path": str(envelope.approved_workspace) + "/."},
            lambda repo, scripts, envelope: {"target_repo_path": Path(str(repo) + "/.")},
            lambda repo, scripts, envelope: {"source_subtree_path": Path(str(scripts) + "/.")},
            lambda repo, scripts, envelope: {"workspace_clone_path": Path(str(envelope.approved_workspace) + "/.")},
        ]
        for case in alias_cases:
            reset_process_replay_for_tests()
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo, scripts = self._repo(root)
                envelope = self._envelope(root, repo, scripts)
                used_approvals: set[str] = set()
                used_runs: set[str] = set()
                params = dict(
                    runtime_authorization=self._authorization(envelope),
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-13T00:00:00+00:00",
                    used_approval_ids=used_approvals,
                    used_run_ids=used_runs,
                    workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                    approval_envelope=envelope,
                )
                params.update(case(repo, scripts, envelope))
                result = _run_bounded_blk_test_evidence_refresh_for_tests(**params)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertFalse(result["fixed_tool_executed"])
                self.assertIn("pre-runtime validation failed", result["block_reason"])
                self.assertIn(envelope.approval_id, used_approvals)
                self.assertIn(envelope.run_id, used_runs)
                ledger = json.loads(envelope.replay_ledger_path.read_text(encoding="utf-8"))
                self.assertIn(envelope.approval_id, ledger["approval_ids"])
                self.assertIn(envelope.run_id, ledger["run_ids"])

        for secret_name in [".env.local", ".envrc.local", ".npmrc.local", "api_key.txt", "access_token.json", "private-key"]:
            reset_process_replay_for_tests()
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo, scripts = self._repo(root)
                envelope = self._envelope(root, repo, scripts)
                (scripts / secret_name).write_text("SECRET=1\n", encoding="utf-8")
                used_approvals: set[str] = set()
                used_runs: set[str] = set()
                result = _run_bounded_blk_test_evidence_refresh_for_tests(
                    runtime_authorization=self._authorization(envelope),
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-13T00:00:00+00:00",
                    used_approval_ids=used_approvals,
                    used_run_ids=used_runs,
                    workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                    approval_envelope=envelope,
                )
                self.assertEqual(result["status"], "BLOCKED")
                self.assertIn("secret descendant", result["block_reason"])
                self.assertFalse(result["fixed_tool_executed"])
                self.assertIn(envelope.approval_id, used_approvals)
                self.assertIn(envelope.run_id, used_runs)

        reset_process_replay_for_tests()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            used_approvals: set[str] = set()
            used_runs: set[str] = set()
            with self.assertRaisesRegex(ValueError, "output_byte_limit"):
                _run_bounded_blk_test_evidence_refresh_for_tests(
                    runtime_authorization=self._authorization(envelope),
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-13T00:00:00+00:00",
                    used_approval_ids=used_approvals,
                    used_run_ids=used_runs,
                    workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                    approval_envelope=envelope,
                    output_byte_limit=100,
                )
            self.assertIn(envelope.approval_id, used_approvals)
            self.assertIn(envelope.run_id, used_runs)

        reset_process_replay_for_tests()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            envelope.approved_workspace.mkdir()
            result = _run_bounded_blk_test_evidence_refresh_for_tests(
                runtime_authorization=self._authorization(envelope),
                target_repo_path=str(repo),
                source_subtree_path=str(scripts),
                workspace_clone_path=str(envelope.approved_workspace),
                approval_id=envelope.approval_id,
                run_id=envelope.run_id,
                expected_head=envelope.expected_head,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                approval_envelope=envelope,
            )
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("already exists", result["block_reason"])
            self.assertFalse(result["fixed_tool_executed"])
            self.assertTrue(envelope.approved_workspace.exists(), "pre-owned workspace must not be deleted")

    def test_authorization_laundering_and_exact_side_effect_sets_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, scripts = self._repo(root)
            envelope = self._envelope(root, repo, scripts)
            for note in [
                "PASS is approval; publish BEO; RTM generated",
                "docs%2Factive%2FREQ-001.md",
                "protected%20body%20read",
                "BEO%20is%20published",
                "activeVaultHashComparison",
                "hostSecretIsolationClaimed",
                "packageManagerAllowed networkAccess modelService browserTooling cyberTooling",
            ]:
                authorization = self._authorization(envelope)
                authorization["operator_note"] = note
                with self.subTest(note=note):
                    with self.assertRaises(ValueError):
                        _run_bounded_blk_test_evidence_refresh_for_tests(
                            runtime_authorization=authorization,
                            target_repo_path=str(repo),
                            source_subtree_path=str(scripts),
                            workspace_clone_path=str(envelope.approved_workspace),
                            approval_id=envelope.approval_id,
                            run_id=envelope.run_id,
                            expected_head=envelope.expected_head,
                            fixed_tool="run_ast_validation",
                            expires_at="2030-01-01T00:00:00+00:00",
                            now="2026-05-13T00:00:00+00:00",
                            used_approval_ids=set(),
                            used_run_ids=set(),
                            workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                            approval_envelope=envelope,
                        )

            authorization = self._authorization(envelope)
            authorization["no_side_effects"] = dict(authorization["no_side_effects"])
            authorization["no_side_effects"].pop("beo_published")
            with self.assertRaises(ValueError):
                _run_bounded_blk_test_evidence_refresh_for_tests(
                    runtime_authorization=authorization,
                    target_repo_path=str(repo),
                    source_subtree_path=str(scripts),
                    workspace_clone_path=str(envelope.approved_workspace),
                    approval_id=envelope.approval_id,
                    run_id=envelope.run_id,
                    expected_head=envelope.expected_head,
                    fixed_tool="run_ast_validation",
                    expires_at="2030-01-01T00:00:00+00:00",
                    now="2026-05-13T00:00:00+00:00",
                    used_approval_ids=set(),
                    used_run_ids=set(),
                    workspace_marker_nonce="nonce-BLK-SYSTEM-097-TEST-001",
                    approval_envelope=envelope,
                )

    def test_retired_ids_are_detected_from_exact_evidence_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_path = Path(tmp) / "evidence.json"
            evidence_path.write_text(json.dumps({"approval_id": APPROVAL_ID, "run_id": RUN_ID}), encoding="utf-8")
            self.assertTrue(runtime_ids_are_retired_by_evidence(evidence_path))
            evidence_path.write_text(json.dumps({"approval_id": APPROVAL_ID, "run_id": "other"}), encoding="utf-8")
            self.assertFalse(runtime_ids_are_retired_by_evidence(evidence_path))

    def test_production_entrypoint_rejects_committed_retired_ids_after_one_exact_run(self):
        if not EVIDENCE_PATH.exists():
            self.skipTest("BLK-SYSTEM-097 committed evidence is created by the exact runtime task")
        authorization = build_runtime_authorization(
            approval_id=APPROVAL_ID,
            run_id=RUN_ID,
            target_repo_path="/home/dad/code/Kuronode-v1",
            source_subtree_path="/home/dad/code/Kuronode-v1/scripts",
            expected_head=EXPECTED_HEAD,
            observed_remote_head=EXPECTED_HEAD,
        )
        with self.assertRaisesRegex(ValueError, "already retired by committed evidence"):
            run_bounded_blk_test_evidence_refresh(
                runtime_authorization=authorization,
                target_repo_path="/home/dad/code/Kuronode-v1",
                source_subtree_path="/home/dad/code/Kuronode-v1/scripts",
                workspace_clone_path="/tmp/blk-system-097-kuronode-evidence-refresh-workspace",
                approval_id=APPROVAL_ID,
                run_id=RUN_ID,
                expected_head=EXPECTED_HEAD,
                fixed_tool="run_ast_validation",
                expires_at="2030-01-01T00:00:00+00:00",
                now="2026-05-13T00:00:00+00:00",
                used_approval_ids=set(),
                used_run_ids=set(),
                workspace_marker_nonce="nonce-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001",
            )

    def test_persisted_runtime_evidence_is_evidence_only_and_bound_to_exact_target(self):
        self.assertTrue(EVIDENCE_PATH.exists(), "BLK-SYSTEM-097 runtime evidence must be persisted after the one exact run")
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(evidence["sprint"], "BLK-SYSTEM-097")
        self.assertEqual(evidence["approval_id"], APPROVAL_ID)
        self.assertEqual(evidence["run_id"], RUN_ID)
        self.assertEqual(evidence["target_repo_path"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(evidence["source_subtree_path"], "/home/dad/code/Kuronode-v1/scripts")
        self.assertEqual(evidence["expected_head"], EXPECTED_HEAD)
        self.assertEqual(evidence["actual_head"], EXPECTED_HEAD)
        self.assertEqual(evidence["observed_remote_head"], EXPECTED_HEAD)
        self.assertIn(evidence["status"], {"PASS", "FAIL", "BLOCKED"})
        self.assertIn(evidence["pilot_status"], {PASS_STATUS, FAIL_STATUS, BLOCKED_STATUS})
        self.assertTrue(evidence["replay_consumed_before_runtime"])
        self.assertFalse(evidence["source_mutation_detected"])
        self.assertFalse(evidence["git_mutation_detected"])
        self.assertTrue(evidence["workspace_cleanup_verified"])
        false_flags = [
            "source_write_allowed",
            "git_mutation_allowed",
            "staging_allowed",
            "commit_allowed",
            "push_allowed",
            "active_vault_read",
            "protected_body_read",
            "rtm_drift_rejection",
            "coverage_claim_promoted",
            "public_ledger_mutation",
            "production_isolation_claimed",
            "production_mcp_authority",
            "generic_mcp_authority",
            "reusable_service_started",
            "live_codex_execution",
            "arbitrary_shell_called",
            "typescript_tooling_called",
            "package_manager_called",
            "network_called",
            "model_service_called",
            "browser_tooling_called",
            "cyber_tooling_called",
        ]
        for key in false_flags:
            self.assertIs(evidence[key], False, key)
        self.assertEqual(evidence["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(evidence["rtm_status"], "NOT_GENERATED")
        actual_size = len(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        self.assertEqual(evidence["evidence_json_bytes"], actual_size)
        self.assertLessEqual(actual_size, evidence["output_byte_limit"])


if __name__ == "__main__":
    unittest.main()
