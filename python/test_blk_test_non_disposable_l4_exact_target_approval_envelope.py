import hashlib
import unittest
from pathlib import Path

from blk_test_non_disposable_l4_exact_target_approval_envelope import (
    BLOCKED,
    ENVELOPE_READY,
    evaluate_non_disposable_l4_exact_target_approval_envelope,
)


class NonDisposableL4ExactTargetApprovalEnvelopeTest(unittest.TestCase):
    def _request_gate(self, **overrides):
        evidence = {
            "sprint": "BLK-SYSTEM-049",
            "decision": "NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME",
            "runtime_approved": False,
            "non_disposable_runtime_executed": False,
            "requested_future_tool": "run_ast_validation",
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "source_write_allowed": False,
            "protected_body_read_allowed": False,
            "production_mcp_authorized": False,
            "hostile_review_verdict": "PASS after remediation",
            "final_verification": "Ran 616 tests — OK",
        }
        evidence.update(overrides)
        return evidence

    def _envelope(self, **overrides):
        envelope = {
            "selected_frontier": "blk_test_non_disposable_l4_run_ast_validation",
            "target_repo_path": "/srv/blk-approved/non-disposable/example-repo",
            "source_subtree_path": "/srv/blk-approved/non-disposable/example-repo/src",
            "branch_or_worktree": "main@0123456789abcdef0123456789abcdef01234567",
            "workspace_clone_path": "/tmp/blk-system-050/non-disposable-workspace",
            "workspace_marker_nonce": "nonce-BLK-SYSTEM-050-0123456789abcdef",
            "fixed_tool": "run_ast_validation",
            "timeout_output_profile": {"timeout_seconds": 30, "output_byte_limit": 4096},
            "approval_id": "BLK-SYSTEM-050-APPROVAL-REQUEST-0001",
            "run_id": "BLK-SYSTEM-050-RUN-REQUEST-0001",
            "issued_at": "2026-05-10T08:47:47+10:00",
            "expires_at": "2026-05-10T09:47:47+10:00",
            "operator_identity": "discord:684235178083745819:camcamcami",
            "source_system": "discord-dm:1488733359072084070",
            "cleanup_rollback_obligations": [
                "delete wrapper-owned workspace after run",
                "preserve target repository read-only",
                "record non-success evidence on timeout or output cap",
            ],
            "operator_stop_control": "operator can stop before future runtime begins",
            "hostile_review_criteria": [
                "approval inheritance",
                "target inheritance",
                "replay and expiry bypass",
                "single-frontier enforcement",
                "protected-body leakage",
                "BEO/RTM/publication/drift laundering",
            ],
            "excluded_authorities": [
                "production BLK-test MCP",
                "generic BLK-test MCP",
                "live Codex execution",
                "source mutation",
                "protected BLK-req body reads",
                "BEO publication",
                "RTM generation",
                "drift rejection",
                "public ledger mutation",
                "signer/storage/rollback authority",
                "production isolation claims",
            ],
            "no_side_effects": {
                "runtime_executed": False,
                "subprocess_started": False,
                "source_mutation_detected": False,
                "git_mutation_detected": False,
                "staging_allowed": False,
                "commit_allowed": False,
                "push_allowed": False,
                "reset_allowed": False,
                "checkout_allowed": False,
                "revert_allowed": False,
                "active_vault_read": False,
                "beo_published": False,
                "rtm_generated": False,
                "drift_rejected": False,
                "network_called": False,
                "package_manager_called": False,
                "model_service_called": False,
                "browser_tooling_called": False,
                "cyber_tooling_called": False,
                "production_isolation_claimed": False,
            },
        }
        envelope.update(overrides)
        return envelope

    def _artifacts(self, **overrides):
        paths = {
            "request_gate_module": Path("python/blk_test_l4_evidence_trust_request_gate.py"),
            "request_gate_tests": Path("python/test_blk_test_l4_evidence_trust_request_gate.py"),
            "request_gate_boundary": Path("docs/BLK-052_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md"),
            "request_gate_closeout": Path("docs/outcomes/BLK-SYSTEM-049_sprint-closeout.md"),
            "request_gate_review": Path("docs/reviews/BLK-SYSTEM-049_blk-test-l4-evidence-trust-request-gate-hostile-review.md"),
        }
        artifacts = {}
        for key, path in paths.items():
            data = path.read_bytes()
            artifacts[key] = {"path": path.as_posix(), "sha256": hashlib.sha256(data).hexdigest()}
        artifacts.update(overrides)
        return artifacts

    def test_complete_single_frontier_envelope_returns_review_ready_not_runtime(self):
        decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
            request_gate_evidence=self._request_gate(),
            approval_envelope=self._envelope(),
            evidence_artifacts=self._artifacts(),
        )

        self.assertEqual(decision["decision"], ENVELOPE_READY)
        self.assertFalse(decision["runtime_approved"])
        self.assertFalse(decision["non_disposable_runtime_executed"])
        self.assertEqual(decision["selected_frontier"], "blk_test_non_disposable_l4_run_ast_validation")
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")

    def test_missing_or_failed_request_gate_evidence_blocks_readiness(self):
        for evidence in [
            self._request_gate(decision="BLOCKED"),
            self._request_gate(runtime_approved=True),
            self._request_gate(non_disposable_runtime_executed=True),
            self._request_gate(final_verification="NOT OK"),
        ]:
            decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=evidence,
                approval_envelope=self._envelope(),
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)
            self.assertFalse(decision["runtime_approved"])

    def test_multiple_or_wrong_frontiers_block(self):
        for envelope in [
            self._envelope(selected_frontier=["blk_test_non_disposable_l4_run_ast_validation", "codex_live_dispatch_l3_smoke"]),
            self._envelope(selected_frontier="codex_live_dispatch_l3_smoke"),
        ]:
            decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(),
                approval_envelope=envelope,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)
            self.assertIn("selected_frontier", " ".join(decision["errors"]))

    def test_target_workspace_traversal_blk_system_and_secret_paths_block(self):
        cases = [
            self._envelope(target_repo_path="/home/dad/BLK-System"),
            self._envelope(source_subtree_path="/srv/blk-approved/non-disposable/example-repo/../active"),
            self._envelope(workspace_clone_path="/srv/blk-approved/non-disposable/example-repo/workspace"),
            self._envelope(target_repo_path="/srv/blk-approved/non-disposable/example-repo/.ssh"),
        ]
        for envelope in cases:
            decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(),
                approval_envelope=envelope,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)

    def test_runtime_approval_keys_and_freeform_authority_laundering_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "runtime approval"):
            evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(),
                approval_envelope=self._envelope(runtimeApproval=True),
                evidence_artifacts=self._artifacts(),
            )
        with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
            evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(notes="APPROVED_FOR_LIVE_EXECUTION"),
                approval_envelope=self._envelope(),
                evidence_artifacts=self._artifacts(),
            )

    def test_beo_rtm_publication_drift_and_protected_body_laundering_are_rejected(self):
        for text in [
            "PASS authorizes authoritative BEO publication",
            "runtime RTM generation is allowed",
            "coverage truth and drift rejection approved",
            "read protected BLK-req body",
        ]:
            with self.assertRaisesRegex(ValueError, "forbidden authority marker"):
                evaluate_non_disposable_l4_exact_target_approval_envelope(
                    request_gate_evidence=self._request_gate(),
                    approval_envelope=self._envelope(operator_stop_control=text),
                    evidence_artifacts=self._artifacts(),
                )

    def test_replay_expiry_and_output_profile_gaps_block(self):
        cases = [
            self._envelope(approval_id=""),
            self._envelope(run_id="same", approval_id="same"),
            self._envelope(issued_at="not-a-date"),
            self._envelope(expires_at="2026-05-10T08:00:00+10:00"),
            self._envelope(timeout_output_profile={"timeout_seconds": 0, "output_byte_limit": 4096}),
            self._envelope(timeout_output_profile={"timeout_seconds": 30, "output_byte_limit": 9999999}),
        ]
        for envelope in cases:
            decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(),
                approval_envelope=envelope,
                evidence_artifacts=self._artifacts(),
            )
            self.assertEqual(decision["decision"], BLOCKED)

    def test_artifact_descriptors_must_bind_expected_paths_and_sha256(self):
        artifacts = self._artifacts()
        artifacts["request_gate_closeout"] = dict(artifacts["request_gate_closeout"])
        artifacts["request_gate_closeout"]["sha256"] = "0" * 64
        decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
            request_gate_evidence=self._request_gate(),
            approval_envelope=self._envelope(),
            evidence_artifacts=artifacts,
        )
        self.assertEqual(decision["decision"], BLOCKED)
        self.assertIn("artifact", " ".join(decision["errors"]))

    def test_no_side_effect_flags_must_be_complete_and_false(self):
        side_effects = dict(self._envelope()["no_side_effects"])
        side_effects["subprocess_started"] = True
        decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
            request_gate_evidence=self._request_gate(),
            approval_envelope=self._envelope(no_side_effects=side_effects),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)
        self.assertFalse(decision["subprocess_started"])

        side_effects = dict(self._envelope()["no_side_effects"])
        side_effects.pop("network_called")
        decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
            request_gate_evidence=self._request_gate(),
            approval_envelope=self._envelope(no_side_effects=side_effects),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)

    def test_nested_extra_keys_and_malformed_lists_block(self):
        with self.assertRaisesRegex(ValueError, "runtime approval"):
            evaluate_non_disposable_l4_exact_target_approval_envelope(
                request_gate_evidence=self._request_gate(),
                approval_envelope=self._envelope(timeout_output_profile={"timeout_seconds": 30, "output_byte_limit": 4096, "runtime_approved": True}),
                evidence_artifacts=self._artifacts(),
            )

        decision = evaluate_non_disposable_l4_exact_target_approval_envelope(
            request_gate_evidence=self._request_gate(),
            approval_envelope=self._envelope(hostile_review_criteria=["ok"]),
            evidence_artifacts=self._artifacts(),
        )
        self.assertEqual(decision["decision"], BLOCKED)


if __name__ == "__main__":
    unittest.main()
