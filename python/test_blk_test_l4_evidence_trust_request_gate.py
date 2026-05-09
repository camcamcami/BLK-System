import hashlib
import unittest
from pathlib import Path

from blk_test_l4_evidence_trust_request_gate import (
    BLOCKED,
    REQUEST_READY,
    evaluate_l4_evidence_trust_request_gate,
)


class BlkTestL4EvidenceTrustRequestGateTest(unittest.TestCase):
    def _evidence(self, **overrides):
        evidence = {
            "sprint": "BLK-SYSTEM-048",
            "pilot_status": "BLK_TEST_L4_DISPOSABLE_REPO_PASS_EVIDENCE_ONLY",
            "status": "PASS",
            "requested_tool": "run_ast_validation",
            "runtime_target_class": "disposable_real_git_repository",
            "replay_consumed": True,
            "fixed_tool_executed": True,
            "source_mutation_detected": False,
            "git_mutation_detected": False,
            "source_write_allowed": False,
            "staging_allowed": False,
            "commit_allowed": False,
            "push_allowed": False,
            "active_vault_read": False,
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "production_isolation_claimed": False,
            "network_called": False,
            "model_service_called": False,
            "browser_tooling_called": False,
            "cyber_tooling_called": False,
            "package_manager_called": False,
            "arbitrary_shell_called": False,
            "output_byte_limit": 4096,
            "evidence_json_bytes": 1200,
        }
        evidence.update(overrides)
        return evidence

    def _review(self, **overrides):
        review = {
            "review_document": "docs/reviews/BLK-SYSTEM-048_blk-test-fixed-tool-l4-disposable-real-repo-runtime-hostile-review.md",
            "verdict": "PASS after remediation",
            "blockers_remediated": True,
            "review_scope": [
                "replay ordering",
                "fake Git identity",
                "output cap enforcement",
                "authority laundering",
                "protected-body leakage",
            ],
        }
        review.update(overrides)
        return review

    def _verification(self, **overrides):
        verification = {
            "python_unittest_discovery": "Ran 603 tests — OK",
            "focused_runtime_tests": "Ran 10 tests — OK",
            "go_test": "PASS",
            "go_vet": "PASS",
            "git_diff_check": "PASS",
        }
        verification.update(overrides)
        return verification

    def _artifacts(self, **overrides):
        paths = {
            "runtime_module": Path("python/blk_test_fixed_tool_l4_disposable_repo_runtime.py"),
            "runtime_tests": Path("python/test_blk_test_fixed_tool_l4_disposable_repo_runtime.py"),
            "review_document": Path("docs/reviews/BLK-SYSTEM-048_blk-test-fixed-tool-l4-disposable-real-repo-runtime-hostile-review.md"),
            "closeout_document": Path("docs/outcomes/BLK-SYSTEM-048_sprint-closeout.md"),
            "boundary_document": Path("docs/BLK-051_blk-test-fixed-tool-l4-disposable-real-repo-runtime-boundary.md"),
        }
        artifacts = {}
        for key, path in paths.items():
            data = path.read_bytes()
            artifacts[key] = {"path": path.as_posix(), "sha256": hashlib.sha256(data).hexdigest()}
        artifacts.update(overrides)
        return artifacts

    def _proposal(self, **overrides):
        proposal = {
            "target_repo_path": "/srv/blk-approved/example-repo",
            "source_subtree_path": "/srv/blk-approved/example-repo/src",
            "branch_or_worktree": "main@abc123",
            "workspace_clone_path": "/tmp/blk-system-049/workspace",
            "workspace_marker_nonce": "nonce-BLK-SYSTEM-049-NONDISPOSABLE-REQUEST",
            "fixed_tool": "run_ast_validation",
            "timeout_output_profile": {"timeout_seconds": 30, "output_byte_limit": 4096},
            "replay_policy": {"approval_id_required": True, "run_id_required": True},
            "approval_window": {"issued_at_required": True, "expires_at_required": True},
            "operator_identity": "operator:camcamcami",
            "source_system": "discord-dm",
            "cleanup_rollback_obligations": ["remove workspace clone", "preserve source repo read-only"],
            "operator_stop_control": "Discord stop command before runtime starts",
            "hostile_review_criteria": ["authority laundering", "protected-body leakage", "source mutation"],
            "excluded_authorities": [
                "production BLK-test MCP",
                "generic BLK-test MCP",
                "source mutation",
                "protected BLK-req body reads",
                "BEO publication",
                "RTM generation",
                "drift rejection",
            ],
        }
        proposal.update(overrides)
        return proposal

    def test_complete_disposable_evidence_and_exact_target_proposal_returns_review_ready_not_runtime(self):
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(),
            future_target_proposal=self._proposal(),
            evidence_artifacts=self._artifacts(),
        )

        self.assertEqual(decision["decision"], REQUEST_READY)
        self.assertFalse(decision["runtime_approved"])
        self.assertFalse(decision["non_disposable_runtime_executed"])
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")

    def test_missing_or_failed_evidence_blocks_request_readiness(self):
        for evidence in [self._evidence(status="FAIL"), self._evidence(replay_consumed=False)]:
            decision = evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=evidence,
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(),
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)
            self.assertFalse(decision["runtime_approved"])

    def test_hostile_review_and_final_verification_must_pass(self):
        blocked_review = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(verdict="PASS maybe", blockers_remediated=False),
            final_verification=self._verification(),
            future_target_proposal=self._proposal(),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(blocked_review["decision"], BLOCKED)

        blocked_verification = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(go_vet="SKIPPED"),
            future_target_proposal=self._proposal(),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(blocked_verification["decision"], BLOCKED)

    def test_laundering_and_runtime_approval_wording_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(notes="PASS authorizes BEO publication and RTM generation"),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(),
                evidence_artifacts=self._artifacts(),
            )
        with self.assertRaisesRegex(ValueError, "runtime approval"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(runtime_approval=True),
                evidence_artifacts=self._artifacts(),
            )


    def test_nested_runtime_approval_keys_and_freeform_authority_terms_are_rejected(self):
        proposal = self._proposal()
        proposal["replay_policy"] = {"runtime_approved": True}
        with self.assertRaisesRegex(ValueError, "runtime approval"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=proposal,
                evidence_artifacts=self._artifacts(),
            )

        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(notes="production BLK-test MCP"),
                evidence_artifacts=self._artifacts(),
            )

    def test_malformed_target_paths_and_profiles_block(self):
        bad = self._proposal(
            target_repo_path="/home/dad/BLK-System",
            source_subtree_path="/home/dad/BLK-System",
            workspace_clone_path="/home/dad/BLK-System",
            timeout_output_profile="not-a-dict",
        )
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(),
            future_target_proposal=bad,
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)
        self.assertIn("target_repo_path", " ".join(decision["errors"]))
        self.assertIn("timeout_output_profile", " ".join(decision["errors"]))

    def test_final_verification_rejects_not_ok_and_artifact_hash_mismatch(self):
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(python_unittest_discovery="NOT OK actually failed"),
            future_target_proposal=self._proposal(),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)

        bad_artifacts = self._artifacts()
        bad_artifacts["closeout_document"] = dict(bad_artifacts["closeout_document"])
        bad_artifacts["closeout_document"]["sha256"] = "0" * 64
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(),
            future_target_proposal=self._proposal(),
            evidence_artifacts=bad_artifacts,
        )
        self.assertEqual(decision["decision"], BLOCKED)
        self.assertIn("artifact", " ".join(decision["errors"]))


    def test_hostile_bypass_cases_remain_blocked(self):
        for replay_policy in [
            {"runtimeApproval": True},
            {"runtimeApproved": True},
            {"approved_runtime": True},
            {"unexpected": "x"},
        ]:
            with self.subTest(replay_policy=replay_policy):
                if any("runtime" in key.lower() or "approved" in key.lower() for key in replay_policy):
                    with self.assertRaisesRegex(ValueError, "runtime approval"):
                        evaluate_l4_evidence_trust_request_gate(
                            disposable_runtime_evidence=self._evidence(),
                            hostile_review=self._review(),
                            final_verification=self._verification(),
                            future_target_proposal=self._proposal(replay_policy=replay_policy),
                            evidence_artifacts=self._artifacts(),
                        )
                else:
                    decision = evaluate_l4_evidence_trust_request_gate(
                        disposable_runtime_evidence=self._evidence(),
                        hostile_review=self._review(),
                        final_verification=self._verification(),
                        future_target_proposal=self._proposal(replay_policy=replay_policy),
                        evidence_artifacts=self._artifacts(),
                    )
                    self.assertEqual(decision["decision"], BLOCKED)

        for bad_proposal in [
            self._proposal(approval_window={"unexpected": "x"}),
            self._proposal(branch_or_worktree=["main"]),
            self._proposal(operator_identity={"name": "operator:camcamcami"}),
            self._proposal(workspace_clone_path="/srv/blk-approved/example-repo/workspace"),
            self._proposal(target_repo_path="docs/active/foo"),
            self._proposal(hostile_review_criteria=["approved for runtime"]),
        ]:
            decision = evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=bad_proposal,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)

        for bad_summary in ["Ran 1 tests NOT-OK OK", "Ran 1 tests NOT_OK OK", "Ran 1 tests garbage OK"]:
            decision = evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(python_unittest_discovery=bad_summary),
                future_target_proposal=self._proposal(),
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)

        runtime_module_artifact = self._artifacts()["runtime_module"]
        wrong_artifacts = {key: dict(runtime_module_artifact) for key in self._artifacts()}
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(),
            future_target_proposal=self._proposal(),
            evidence_artifacts=wrong_artifacts,
        )
        self.assertEqual(decision["decision"], BLOCKED)


    def test_second_hostile_bypass_cases_remain_blocked(self):
        for bad in [
            self._proposal(cleanup_rollback_obligations=["runtime approval accepted"]),
            self._proposal(target_repo_path="/home/dad/../dad/BLK-System", source_subtree_path="/home/dad/../dad/BLK-System/src"),
            self._proposal(workspace_clone_path="/srv/blk-approved/other/../example-repo/workspace"),
        ]:
            decision = evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=bad,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)

        with self.assertRaisesRegex(ValueError, "runtime approval"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(runtimeApproval=True),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(),
                evidence_artifacts=self._artifacts(),
            )

        for notes in ["runtime.approval", "approved/for/runtime", "production BLK.test MCP"]:
            with self.subTest(notes=notes):
                with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
                    evaluate_l4_evidence_trust_request_gate(
                        disposable_runtime_evidence=self._evidence(notes=notes),
                        hostile_review=self._review(),
                        final_verification=self._verification(),
                        future_target_proposal=self._proposal(),
                        evidence_artifacts=self._artifacts(),
                    )

        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(review_scope=self._review()["review_scope"] + ["approved for runtime"]),
            final_verification=self._verification(),
            future_target_proposal=self._proposal(),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)


    def test_dict_shaped_denial_lists_with_authority_values_are_blocked(self):
        bad_criteria = {"authority laundering": "approved for runtime", "protected-body leakage": "ok", "source mutation": "ok"}
        bad_excluded = {authority: "runtime approval" for authority in self._proposal()["excluded_authorities"]}
        for bad in [
            self._proposal(hostile_review_criteria=bad_criteria),
            self._proposal(excluded_authorities=bad_excluded),
        ]:
            decision = evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=bad,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)


    def test_runtime_authorization_key_variants_are_rejected(self):
        for key in ["runtimeAuthorized", "runtimeAuthorization"]:
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "runtime approval"):
                    evaluate_l4_evidence_trust_request_gate(
                        disposable_runtime_evidence=self._evidence(**{key: True}),
                        hostile_review=self._review(),
                        final_verification=self._verification(),
                        future_target_proposal=self._proposal(),
                        evidence_artifacts=self._artifacts(),
                    )

    def test_future_exact_target_proposal_must_be_complete_and_fixed_tool_only(self):
        missing = self._proposal()
        del missing["workspace_marker_nonce"]
        decision = evaluate_l4_evidence_trust_request_gate(
            disposable_runtime_evidence=self._evidence(),
            hostile_review=self._review(),
            final_verification=self._verification(),
            future_target_proposal=missing,
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)

        with self.assertRaisesRegex(ValueError, "fixed_tool"):
            evaluate_l4_evidence_trust_request_gate(
                disposable_runtime_evidence=self._evidence(),
                hostile_review=self._review(),
                final_verification=self._verification(),
                future_target_proposal=self._proposal(fixed_tool="pytest"),
                evidence_artifacts=self._artifacts(),
            )


if __name__ == "__main__":
    unittest.main()
