import ast
import unittest
from pathlib import Path

import blk_codex_invocation_profile as invocation_profile
import blk_codex_dispatch_envelope as dispatch_envelope
import blk_codex_live_dispatch_readiness_gate as readiness_gate


NOW = "2026-05-09T14:25:00+10:00"


class CodexLiveDispatchReadinessGateTest(unittest.TestCase):
    def _codex_profile(self):
        return invocation_profile.build_codex_deterministic_invocation_profile(
            approved_model="gpt-5.4",
            worktree="/tmp/blk-system-codex-worktree",
            final_message_artifact="artifacts/codex/final-message.md",
            prompt="Execute the bounded tactical packet without expanding authority.",
        )

    def _dispatch_approval(self):
        return {
            "approval_id": "CODEX-DISPATCH-APPROVAL-040-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-040-dispatch-envelope",
            "timestamp": "2026-05-09T14:18:00+10:00",
            "expires_at": "2026-05-09T15:18:00+10:00",
            "exact_approved_scope": "BLK-SYSTEM-040 dispatch-envelope fixture only; no live execution",
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

    def _dispatch_envelope(self, **overrides):
        values = {
            "codex_profile": self._codex_profile(),
            "approval_provenance": self._dispatch_approval(),
            "allowed_modified_files": ["python/example_target.py"],
            "allowed_new_files": ["docs/outcomes/example.md"],
            "validation_profiles": ["python-unittest", "active-doctrine-gate"],
            "telemetry_artifacts": {
                "jsonl_events": "artifacts/codex/events.jsonl",
                "final_message": "artifacts/codex/final-message.md",
                "envelope_report": "artifacts/codex/dispatch-envelope.json",
            },
            "failure_ceiling": {"max_iterations": 3, "on_exhaustion": "OPERATOR_ESCALATION_REQUIRED"},
            "hostile_audit": {
                "required_checks": [
                    "file_boundary_check",
                    "validation_gate_check",
                    "telemetry_advisory_check",
                    "authority_non_expansion_check",
                ]
            },
            "operator_escalation": {
                "required_cases": [
                    "missing_approval",
                    "policy_block",
                    "validation_failure",
                    "failure_ceiling",
                    "malformed_telemetry",
                    "denied_authority",
                ]
            },
            "run_id": "CODEX-DISPATCH-RUN-040-001",
            "used_approval_ids": set(),
            "used_run_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return dispatch_envelope.build_codex_deterministic_dispatch_envelope(**values)

    def _runtime_approval(self, **overrides):
        value = {
            "approval_id": "CODEX-LIVE-DISPATCH-REVIEW-040-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-040-runtime-approval",
            "timestamp": "2026-05-09T14:20:00+10:00",
            "expires_at": "2026-05-09T15:20:00+10:00",
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
        value.update(overrides)
        return value

    def _evidence(self, kind, **overrides):
        value = {
            "status": "PRESENT_FOR_REVIEW_ONLY",
            "artifact_ref": f"artifacts/codex-readiness/{kind}.json",
            "summary": f"{kind} evidence is bounded and review-only",
            "authority": "REVIEW_ONLY_NOT_EXECUTION",
        }
        value.update(overrides)
        return value

    def _build(self, **overrides):
        values = {
            "dispatch_envelope": self._dispatch_envelope(),
            "runtime_approval": self._runtime_approval(),
            "blk_pipe_wiring_plan": self._evidence("blk-pipe-wiring"),
            "containment_evidence": self._evidence("containment"),
            "validation_execution_plan": self._evidence("validation-execution"),
            "telemetry_persistence_plan": self._evidence("telemetry-persistence"),
            "rollback_plan": self._evidence("rollback"),
            "monitoring_plan": self._evidence("monitoring"),
            "operator_controls": self._evidence("operator-controls"),
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
            "run_id": "CODEX-LIVE-DISPATCH-READINESS-RUN-040-001",
            "used_runtime_approval_ids": set(),
            "used_readiness_run_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return readiness_gate.build_codex_live_dispatch_readiness_gate(**values)

    def test_complete_readiness_record_is_review_ready_but_not_execution_authority(self):
        result = self._build()

        self.assertEqual(result["readiness_gate_id"], "codex_live_dispatch_readiness_gate")
        self.assertEqual(result["readiness_status"], "CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY")
        self.assertEqual(result["evaluation"], "READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION")
        self.assertEqual(result["blocked_reasons"], [])
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["codex_subprocess_started"])
        self.assertFalse(result["blk_pipe_dispatched"])
        self.assertFalse(result["source_mutation_authorized"])
        self.assertEqual(result["runtime_approval"]["validated_for_review_only"], True)

    def test_missing_runtime_approval_blocks_not_raises(self):
        result = self._build(runtime_approval=None)

        self.assertEqual(result["evaluation"], "BLOCKED_NOT_AUTHORIZED")
        self.assertIn("runtime_approval missing", result["blocked_reasons"])
        self.assertFalse(result["execution_authorized"])

    def test_missing_each_prerequisite_blocks_with_operator_reason(self):
        prerequisite_fields = [
            "blk_pipe_wiring_plan",
            "containment_evidence",
            "validation_execution_plan",
            "telemetry_persistence_plan",
            "rollback_plan",
            "monitoring_plan",
            "operator_controls",
            "failure_ceiling",
            "hostile_audit",
        ]
        for field in prerequisite_fields:
            with self.subTest(field=field):
                result = self._build(**{field: None})
                self.assertEqual(result["evaluation"], "BLOCKED_NOT_AUTHORIZED")
                self.assertTrue(any(field in reason for reason in result["blocked_reasons"]))

    def test_expired_or_replayed_runtime_approval_blocks(self):
        expired = self._runtime_approval(expires_at="2026-05-09T14:00:00+10:00")
        self.assertIn("runtime_approval expired", self._build(runtime_approval=expired)["blocked_reasons"])
        self.assertIn(
            "runtime_approval replayed",
            self._build(used_runtime_approval_ids={"CODEX-LIVE-DISPATCH-REVIEW-040-001"})["blocked_reasons"],
        )
        self.assertIn(
            "readiness run replayed",
            self._build(used_readiness_run_ids={"CODEX-LIVE-DISPATCH-READINESS-RUN-040-001"})["blocked_reasons"],
        )

    def test_invalid_dispatch_envelope_blocks(self):
        broken = self._dispatch_envelope()
        broken["dispatch_started_by_envelope_helper"] = True

        result = self._build(dispatch_envelope=broken)

        self.assertEqual(result["evaluation"], "BLOCKED_NOT_AUTHORIZED")
        self.assertTrue(any("dispatch_envelope invalid" in reason for reason in result["blocked_reasons"]))

    def test_live_execution_or_authority_laundering_fields_fail_closed(self):
        forbidden = [
            {"execution_authorized": True},
            {"codex_subprocess_started": True},
            {"blk_pipe_dispatched": True},
            {"source_mutation_authorized": True},
            {"metadata": {"live_codex_execution_authorized": True}},
            {"metadata": {"blk_pipe_dispatch_authorized": True}},
            {"metadata": {"production_sandbox_authority": "APPROVED"}},
            {"metadata": {"runtime_execution_authority": "APPROVED"}},
            {"metadata": {"generic_approval_claim": "APPROVED_FOR_LIVE_EXECUTION"}},
            {"metadata": {"claim": "READY_FOR_EXECUTION"}},
            {"metadata": {"claim": "BEO_PUBLICATION_APPROVAL"}},
            {"metadata": {"claim": "RTM_GENERATION_APPROVAL"}},
            {"metadata": {"claim": "DRIFT_REJECTION_AUTHORITY"}},
            {"metadata": {"claim": "PROTECTED_BODY_READ_ALLOWED"}},
            {"metadata": {"claim": "pip install package"}},
            {"metadata": {"claim": "curl https://example.test"}},
        ]
        for override in forbidden:
            with self.subTest(override=override):
                result = self._build()
                result.update(override)
                with self.assertRaises(ValueError):
                    readiness_gate.validate_codex_live_dispatch_readiness_gate(result, now=NOW, used_runtime_approval_ids=set(), used_readiness_run_ids=set())

    def test_rejects_malformed_evidence_paths_or_authority_status(self):
        bad_values = [
            {"artifact_ref": "/tmp/escape.json"},
            {"artifact_ref": "../escape.json"},
            {"artifact_ref": "artifacts/codex-readiness/../escape.json"},
            {"artifact_ref": "docs/active/REQ-001.md"},
            {"status": "EXECUTION_READY"},
            {"authority": "EXECUTION_AUTHORITY_GRANTED"},
        ]
        for bad in bad_values:
            with self.subTest(bad=bad):
                result = self._build(containment_evidence=self._evidence("containment", **bad))
                self.assertEqual(result["evaluation"], "BLOCKED_NOT_AUTHORIZED")
                self.assertTrue(any("containment_evidence" in reason for reason in result["blocked_reasons"]))

    def test_requires_replay_state_inputs(self):
        with self.assertRaisesRegex(ValueError, "used_runtime_approval_ids"):
            self._build(used_runtime_approval_ids=None)
        with self.assertRaisesRegex(ValueError, "used_readiness_run_ids"):
            self._build(used_readiness_run_ids=None)

    def test_source_does_not_import_or_call_live_surfaces(self):
        source_path = Path(readiness_gate.__file__)
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
