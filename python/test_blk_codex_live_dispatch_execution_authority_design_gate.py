import ast
import unittest
from pathlib import Path

import blk_codex_invocation_profile as invocation_profile
import blk_codex_dispatch_envelope as dispatch_envelope
import blk_codex_live_dispatch_readiness_gate as readiness_gate
import blk_codex_live_dispatch_authority_request as authority_request
import blk_codex_live_dispatch_execution_authority_design_gate as design_gate


NOW = "2026-05-09T16:20:00+10:00"


class CodexLiveDispatchExecutionAuthorityDesignGateTest(unittest.TestCase):
    def _codex_profile(self):
        return invocation_profile.build_codex_deterministic_invocation_profile(
            approved_model="gpt-5.4",
            worktree="/tmp/blk-system-codex-worktree",
            final_message_artifact="artifacts/codex/final-message.md",
            prompt="Execute the bounded tactical packet without expanding authority.",
        )

    def _dispatch_approval(self):
        return {
            "approval_id": "CODEX-DISPATCH-APPROVAL-042-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-042-dispatch-envelope",
            "timestamp": "2026-05-09T16:00:00+10:00",
            "expires_at": "2026-05-09T17:00:00+10:00",
            "exact_approved_scope": "BLK-SYSTEM-042 dispatch-envelope fixture only; no live execution",
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
            run_id="CODEX-DISPATCH-RUN-042-001",
            used_approval_ids=set(),
            used_run_ids=set(),
            now=NOW,
        )

    def _review_evidence(self, kind, **overrides):
        value = {
            "status": "PRESENT_FOR_REVIEW_ONLY",
            "artifact_ref": f"artifacts/codex-readiness/{kind}.json",
            "summary": f"{kind} contract is bounded and review-only",
            "authority": "REVIEW_ONLY_NOT_EXECUTION",
        }
        value.update(overrides)
        return value

    def _runtime_approval(self):
        return {
            "approval_id": "CODEX-LIVE-DISPATCH-REVIEW-042-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-042-runtime-approval",
            "timestamp": "2026-05-09T16:01:00+10:00",
            "expires_at": "2026-05-09T17:01:00+10:00",
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
            "run_id": "CODEX-LIVE-DISPATCH-READINESS-RUN-042-001",
            "used_runtime_approval_ids": set(),
            "used_readiness_run_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return readiness_gate.build_codex_live_dispatch_readiness_gate(**values)

    def _human_grant(self, **overrides):
        value = {
            "grant_id": "CODEX-LIVE-DISPATCH-HUMAN-GRANT-042-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-042-human-grant",
            "timestamp": "2026-05-09T16:05:00+10:00",
            "expires_at": "2026-05-09T17:05:00+10:00",
            "exact_approved_scope": "Review Codex live-dispatch request package only; no execution",
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

    def _authority_request(self, **overrides):
        values = {
            "readiness_record": self._readiness_record(),
            "separate_human_grant": self._human_grant(),
            "request_scope": "Package BLK-SYSTEM-042 Codex live-dispatch authority request for human review only",
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
            "request_id": "CODEX-LIVE-DISPATCH-AUTHORITY-REQUEST-042-001",
            "used_request_ids": set(),
            "used_human_grant_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return authority_request.build_codex_live_dispatch_authority_request(**values)

    def _contract(self, kind, **overrides):
        value = {
            "status": "PRESENT_FOR_REVIEW_ONLY",
            "contract_ref": f"artifacts/codex-execution-authority-design/{kind}.json",
            "summary": f"{kind} contract remains review-only and grants no execution",
            "authority": "REVIEW_ONLY_NOT_EXECUTION",
            "side_effects_authorized": False,
        }
        value.update(overrides)
        return value

    def _build(self, **overrides):
        values = {
            "authority_request_package": self._authority_request(),
            "approval_envelope_contract": self._contract("approval-envelope"),
            "blk_pipe_integration_contract": self._contract("blk-pipe-integration"),
            "containment_contract": self._contract("containment"),
            "telemetry_contract": self._contract("telemetry"),
            "rollback_contract": self._contract("rollback"),
            "monitoring_operator_control_contract": self._contract("monitoring-operator-controls"),
            "failure_ceiling_contract": self._contract("failure-ceiling"),
            "replay_protection_contract": self._contract("replay-protection"),
            "hostile_audit_contract": {
                "required_checks": [
                    "authority_request_package_check",
                    "approval_envelope_check",
                    "blk_pipe_integration_check",
                    "containment_claim_check",
                    "telemetry_contract_check",
                    "rollback_contract_check",
                    "monitoring_operator_control_check",
                    "failure_ceiling_check",
                    "replay_protection_check",
                    "authority_non_expansion_check",
                ],
                "authority": "REVIEW_ONLY_NOT_EXECUTION",
            },
            "design_id": "CODEX-EXECUTION-AUTHORITY-DESIGN-042-001",
            "used_design_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return design_gate.build_codex_live_dispatch_execution_authority_design_gate(**values)

    def test_complete_design_gate_is_ready_for_review_but_not_execution(self):
        result = self._build()

        self.assertEqual(result["design_gate_id"], "codex_live_dispatch_execution_authority_design_gate")
        self.assertEqual(result["design_gate_status"], "CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY")
        self.assertEqual(result["evaluation"], "EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION")
        self.assertEqual(result["blocked_reasons"], [])
        self.assertFalse(result["execution_authorized"])
        self.assertFalse(result["codex_subprocess_started"])
        self.assertFalse(result["blk_pipe_dispatched"])
        self.assertFalse(result["source_mutation_authorized"])
        self.assertFalse(result["git_mutation_authorized"])
        self.assertFalse(result["protected_body_read_authorized"])
        self.assertFalse(result["production_sandbox_claimed"])

    def test_missing_design_contracts_block(self):
        required_contracts = [
            "approval_envelope_contract",
            "blk_pipe_integration_contract",
            "containment_contract",
            "telemetry_contract",
            "rollback_contract",
            "monitoring_operator_control_contract",
            "failure_ceiling_contract",
            "replay_protection_contract",
            "hostile_audit_contract",
        ]
        for contract in required_contracts:
            with self.subTest(contract=contract):
                result = self._build(**{contract: None})
                self.assertEqual(result["evaluation"], "EXECUTION_AUTHORITY_DESIGN_BLOCKED")
                self.assertTrue(any(contract in reason for reason in result["blocked_reasons"]))

    def test_blocked_authority_request_package_blocks_design_gate(self):
        blocked_request = self._authority_request(separate_human_grant=None)
        result = self._build(authority_request_package=blocked_request)

        self.assertEqual(result["evaluation"], "EXECUTION_AUTHORITY_DESIGN_BLOCKED")
        self.assertTrue(any("authority_request_package" in reason for reason in result["blocked_reasons"]))

    def test_side_effect_flags_block_builder_and_validator_paths(self):
        result = self._build(telemetry_contract=self._contract("telemetry", execution_authorized=True))
        self.assertEqual(result["evaluation"], "EXECUTION_AUTHORITY_DESIGN_BLOCKED")
        self.assertTrue(any("execution_authorized" in reason for reason in result["blocked_reasons"]))

        ready = self._build()
        ready["blk_pipe_dispatched"] = True
        with self.assertRaises(ValueError):
            design_gate.validate_codex_live_dispatch_execution_authority_design_gate(
                ready,
                now=NOW,
                used_design_ids=set(),
            )

    def test_authority_laundering_strings_block_builder_and_validator_paths(self):
        result = self._build(
            approval_envelope_contract=self._contract(
                "approval-envelope",
                nested={"claim": "APPROVED_FOR_LIVE_EXECUTION"},
            )
        )
        self.assertEqual(result["evaluation"], "EXECUTION_AUTHORITY_DESIGN_BLOCKED")
        self.assertTrue(any("APPROVED_FOR_LIVE_EXECUTION" in reason for reason in result["blocked_reasons"]))

        ready = self._build()
        ready["approval_envelope_contract"]["nested"] = {"claim": "READY_FOR_EXECUTION"}
        with self.assertRaises(ValueError):
            design_gate.validate_codex_live_dispatch_execution_authority_design_gate(
                ready,
                now=NOW,
                used_design_ids=set(),
            )

    def test_design_id_replay_and_missing_replay_state_block_or_raise(self):
        self.assertIn(
            "design_id replayed",
            self._build(used_design_ids={"CODEX-EXECUTION-AUTHORITY-DESIGN-042-001"})["blocked_reasons"],
        )
        with self.assertRaises(ValueError):
            self._build(used_design_ids=None)

    def test_source_contains_no_live_execution_surfaces(self):
        source = Path(design_gate.__file__).read_text()
        tree = ast.parse(source)
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http.client"}
        imports = set()
        forbidden_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                    forbidden_calls.append(node.func.id)
                if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen", "Popen", "run", "call", "check_call", "check_output"}:
                    forbidden_calls.append(node.func.attr)
        self.assertEqual(imports & forbidden_imports, set())
        self.assertEqual(forbidden_calls, [])


if __name__ == "__main__":
    unittest.main()
