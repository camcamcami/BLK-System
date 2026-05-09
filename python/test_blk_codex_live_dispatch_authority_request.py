import ast
import unittest
from pathlib import Path

import blk_codex_invocation_profile as invocation_profile
import blk_codex_dispatch_envelope as dispatch_envelope
import blk_codex_live_dispatch_readiness_gate as readiness_gate
import blk_codex_live_dispatch_authority_request as authority_request


NOW = "2026-05-09T15:15:00+10:00"


class CodexLiveDispatchAuthorityRequestTest(unittest.TestCase):
    def _codex_profile(self):
        return invocation_profile.build_codex_deterministic_invocation_profile(
            approved_model="gpt-5.4",
            worktree="/tmp/blk-system-codex-worktree",
            final_message_artifact="artifacts/codex/final-message.md",
            prompt="Execute the bounded tactical packet without expanding authority.",
        )

    def _dispatch_approval(self):
        return {
            "approval_id": "CODEX-DISPATCH-APPROVAL-041-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-041-dispatch-envelope",
            "timestamp": "2026-05-09T15:00:00+10:00",
            "expires_at": "2026-05-09T16:00:00+10:00",
            "exact_approved_scope": "BLK-SYSTEM-041 dispatch-envelope fixture only; no live execution",
            "explicit_excluded_authorities": [
                "live_codex_execution",
                "blk_pipe_dispatch",
                "production_blk_test_mcp",
                "source_mutation",
                "git_mutation",
                "protected_body_read",
                "beo_publication",
                "rtm_generation",
                "drift_rejection",
                "production_sandbox_claim",
            ],
        }

    def _dispatch_envelope(self):
        return dispatch_envelope.build_codex_deterministic_dispatch_envelope(
            codex_profile=self._codex_profile(),
            approval_provenance=self._dispatch_approval(),
            allowed_modified_files=["python/example_target.py"],
            allowed_new_files=["docs/outcomes/example.md"],
            validation_profiles=["python-unittest", "active-doctrine-gate"],
            telemetry_artifacts={
                "jsonl_events": "artifacts/codex/events.jsonl",
                "final_message": "artifacts/codex/final-message.md",
                "envelope_report": "artifacts/codex/dispatch-envelope.json",
            },
            failure_ceiling={"max_iterations": 3, "on_exhaustion": "OPERATOR_ESCALATION_REQUIRED"},
            hostile_audit={
                "required_checks": [
                    "file_boundary_check",
                    "validation_gate_check",
                    "telemetry_advisory_check",
                    "authority_non_expansion_check",
                ]
            },
            operator_escalation={
                "required_cases": [
                    "missing_approval",
                    "policy_block",
                    "validation_failure",
                    "failure_ceiling",
                    "malformed_telemetry",
                    "denied_authority",
                ]
            },
            run_id="CODEX-DISPATCH-RUN-041-001",
            used_approval_ids=set(),
            used_run_ids=set(),
            now=NOW,
        )

    def _review_evidence(self, kind, **overrides):
        value = {
            "status": "PRESENT_FOR_REVIEW_ONLY",
            "artifact_ref": f"artifacts/codex-readiness/{kind}.json",
            "summary": f"{kind} evidence is bounded and review-only",
            "authority": "REVIEW_ONLY_NOT_EXECUTION",
        }
        value.update(overrides)
        return value

    def _runtime_approval(self):
        return {
            "approval_id": "CODEX-LIVE-DISPATCH-REVIEW-041-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-041-runtime-approval",
            "timestamp": "2026-05-09T15:01:00+10:00",
            "expires_at": "2026-05-09T16:01:00+10:00",
            "exact_approved_scope": "Review Codex live-dispatch readiness evidence only; do not execute Codex",
            "explicit_excluded_authorities": [
                "live_codex_execution",
                "blk_pipe_dispatch",
                "production_blk_test_mcp",
                "source_mutation",
                "git_mutation",
                "protected_body_read",
                "beo_publication",
                "rtm_generation",
                "drift_rejection",
                "production_sandbox_claim",
                "package_manager",
                "network_model_cyber_tooling",
            ],
            "validated_for_review_only": True,
        }

    def _readiness_record(self, **overrides):
        values = {
            "dispatch_envelope": self._dispatch_envelope(),
            "runtime_approval": self._runtime_approval(),
            "blk_pipe_wiring_plan": self._review_evidence("blk-pipe-wiring"),
            "containment_evidence": self._review_evidence("containment"),
            "validation_execution_plan": self._review_evidence("validation-execution"),
            "telemetry_persistence_plan": self._review_evidence("telemetry-persistence"),
            "rollback_plan": self._review_evidence("rollback"),
            "monitoring_plan": self._review_evidence("monitoring"),
            "operator_controls": self._review_evidence("operator-controls"),
            "failure_ceiling": {"max_iterations": 3, "on_exhaustion": "OPERATOR_ESCALATION_REQUIRED"},
            "hostile_audit": {
                "required_checks": [
                    "runtime_approval_check",
                    "blk_pipe_wiring_check",
                    "containment_evidence_check",
                    "validation_execution_check",
                    "telemetry_persistence_check",
                    "rollback_plan_check",
                    "monitoring_plan_check",
                    "operator_controls_check",
                    "authority_non_expansion_check",
                ]
            },
            "run_id": "CODEX-LIVE-DISPATCH-READINESS-RUN-041-001",
            "used_runtime_approval_ids": set(),
            "used_readiness_run_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return readiness_gate.build_codex_live_dispatch_readiness_gate(**values)

    def _human_grant(self, **overrides):
        value = {
            "grant_id": "CODEX-LIVE-DISPATCH-HUMAN-GRANT-041-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-041-human-grant",
            "timestamp": "2026-05-09T15:05:00+10:00",
            "expires_at": "2026-05-09T16:05:00+10:00",
            "exact_approved_scope": "Review Codex live-dispatch authority request package only; no execution",
            "explicit_excluded_authorities": [
                "live_codex_execution",
                "blk_pipe_dispatch",
                "production_blk_test_mcp",
                "source_mutation",
                "git_mutation",
                "protected_body_read",
                "beo_publication",
                "rtm_generation",
                "drift_rejection",
                "production_sandbox_claim",
                "package_manager",
                "network_model_cyber_tooling",
            ],
            "review_only": True,
        }
        value.update(overrides)
        return value

    def _build(self, **overrides):
        values = {
            "readiness_record": self._readiness_record(),
            "separate_human_grant": self._human_grant(),
            "request_scope": "Package BLK-SYSTEM-041 Codex live-dispatch authority request for human review only",
            "failure_ceiling": {"max_iterations": 1, "on_exhaustion": "OPERATOR_ESCALATION_REQUIRED"},
            "hostile_audit": {
                "required_checks": [
                    "ready_review_check",
                    "separate_human_grant_check",
                    "disabled_adapter_check",
                    "authority_non_expansion_check",
                ]
            },
            "operator_escalation": {
                "required_cases": [
                    "missing_ready_review",
                    "missing_human_grant",
                    "disabled_adapter_attempt",
                    "denied_authority",
                ]
            },
            "request_id": "CODEX-LIVE-DISPATCH-AUTHORITY-REQUEST-041-001",
            "used_request_ids": set(),
            "used_human_grant_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return authority_request.build_codex_live_dispatch_authority_request(**values)

    def test_complete_request_is_ready_for_human_review_but_not_execution(self):
        result = self._build()

        self.assertEqual(result["authority_request_id"], "codex_live_dispatch_authority_request")
        self.assertEqual(result["authority_request_status"], "CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY")
        self.assertEqual(result["adapter_status"], "CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY")
        self.assertEqual(result["evaluation"], "AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION")
        self.assertEqual(result["blocked_reasons"], [])
        self.assertTrue(result["separate_human_grant_required"])
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["codex_subprocess_started"])
        self.assertFalse(result["blk_pipe_dispatched"])
        self.assertFalse(result["source_mutation_authorized"])

    def test_disabled_adapter_always_blocks_without_side_effects(self):
        request = self._build()
        result = authority_request.simulate_disabled_codex_live_dispatch_adapter(request)

        self.assertEqual(result["adapter_result"], "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED")
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["codex_subprocess_started"])
        self.assertFalse(result["blk_pipe_dispatched"])
        self.assertFalse(result["source_mutation_authorized"])
        self.assertIn("disabled adapter", " ".join(result["blocked_reasons"]))

    def test_blocked_readiness_record_blocks_authority_request(self):
        blocked = self._readiness_record(runtime_approval=None)
        result = self._build(readiness_record=blocked)

        self.assertEqual(result["evaluation"], "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED")
        self.assertTrue(any("readiness" in reason for reason in result["blocked_reasons"]))

    def test_missing_expired_or_replayed_human_grant_blocks(self):
        self.assertIn("separate_human_grant missing", self._build(separate_human_grant=None)["blocked_reasons"])
        expired = self._human_grant(expires_at="2026-05-09T15:00:00+10:00")
        self.assertIn("separate_human_grant expired", self._build(separate_human_grant=expired)["blocked_reasons"])
        self.assertIn(
            "separate_human_grant replayed",
            self._build(used_human_grant_ids={"CODEX-LIVE-DISPATCH-HUMAN-GRANT-041-001"})["blocked_reasons"],
        )
        self.assertIn(
            "authority request replayed",
            self._build(used_request_ids={"CODEX-LIVE-DISPATCH-AUTHORITY-REQUEST-041-001"})["blocked_reasons"],
        )

    def test_missing_review_only_or_authority_wording_in_human_grant_blocks(self):
        self.assertTrue(
            any(
                "review_only" in reason
                for reason in self._build(separate_human_grant=self._human_grant(review_only=False))["blocked_reasons"]
            )
        )
        bad = self._human_grant(exact_approved_scope="APPROVED_FOR_LIVE_EXECUTION")
        blocked = self._build(separate_human_grant=bad)
        self.assertEqual(blocked["evaluation"], "DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED")
        self.assertTrue(any("forbidden authority wording" in reason for reason in blocked["blocked_reasons"]))
        with self.assertRaises(ValueError):
            authority_request.validate_codex_live_dispatch_authority_request(
                blocked, now=NOW, used_request_ids=set(), used_human_grant_ids=set()
            )

    def test_requires_replay_state_inputs(self):
        with self.assertRaisesRegex(ValueError, "used_request_ids"):
            self._build(used_request_ids=None)
        with self.assertRaisesRegex(ValueError, "used_human_grant_ids"):
            self._build(used_human_grant_ids=None)

    def test_live_execution_or_authority_laundering_fields_fail_closed(self):
        forbidden = [
            {"execution_authorized": True},
            {"codex_subprocess_started": True},
            {"blk_pipe_dispatched": True},
            {"source_mutation_authorized": True},
            {"metadata": {"live_codex_execution_authorized": True}},
            {"metadata": {"blk_pipe_dispatch_authorized": True}},
            {"metadata": {"authority": "APPROVED"}},
            {"metadata": {"runtime_execution_authority": "APPROVED"}},
            {"metadata": {"generic_approval_claim": "APPROVED_FOR_LIVE_EXECUTION"}},
            {"metadata": {"claim": "READY_FOR_EXECUTION"}},
            {"metadata": {"claim": "BEO_PUBLICATION_APPROVAL"}},
            {"metadata": {"claim": "RTM_GENERATION_APPROVAL"}},
            {"metadata": {"claim": "DRIFT_REJECTION_AUTHORITY"}},
            {"metadata": {"claim": "PROTECTED_BODY_READ_ALLOWED"}},
            {"metadata": {"claim": "pip install package"}},
            {"metadata": {"claim": "curl https://example.test"}},
            {"metadata": {"production_sandbox_authority": "APPROVED"}},
        ]
        for override in forbidden:
            with self.subTest(override=override):
                result = self._build()
                result.update(override)
                with self.assertRaises(ValueError):
                    authority_request.validate_codex_live_dispatch_authority_request(
                        result, now=NOW, used_request_ids=set(), used_human_grant_ids=set()
                    )

    def test_source_does_not_import_or_call_live_surfaces(self):
        source_path = Path(authority_request.__file__)
        tree = ast.parse(source_path.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib"}
        forbidden_calls = {"system", "popen", "run", "Popen", "call", "check_call", "check_output", "exec", "eval", "__import__"}
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_imports:
                        found.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]
                if module in forbidden_imports:
                    found.append(node.module)
            elif isinstance(node, ast.Call):
                func = node.func
                name = ""
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name in forbidden_calls:
                    found.append(name)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
