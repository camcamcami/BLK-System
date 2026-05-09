import ast
import unittest
from pathlib import Path

import blk_codex_invocation_profile as invocation_profile
import blk_codex_dispatch_envelope as envelope


NOW = "2026-05-09T13:45:00+10:00"


class CodexDeterministicDispatchEnvelopeTest(unittest.TestCase):
    def _codex_profile(self):
        return invocation_profile.build_codex_deterministic_invocation_profile(
            approved_model="gpt-5.4",
            worktree="/tmp/blk-system-codex-worktree",
            final_message_artifact="artifacts/codex/final-message.md",
            prompt="Execute the bounded tactical packet without expanding authority.",
        )

    def _approval(self, **overrides):
        value = {
            "approval_id": "CODEX-DISPATCH-APPROVAL-039-001",
            "source_system": "discord",
            "operator_identity": "discord:684235178083745819",
            "message_event_id": "1488733359072084070/blk-system-039",
            "timestamp": "2026-05-09T13:40:00+10:00",
            "expires_at": "2026-05-09T14:40:00+10:00",
            "exact_approved_scope": "BLK-SYSTEM-039 dispatch-envelope fixture validation only; no live execution",
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
        value.update(overrides)
        return value

    def _build(self, **overrides):
        values = {
            "codex_profile": self._codex_profile(),
            "approval_provenance": self._approval(),
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
            "run_id": "CODEX-DISPATCH-RUN-039-001",
            "used_approval_ids": set(),
            "used_run_ids": set(),
            "now": NOW,
        }
        values.update(overrides)
        return envelope.build_codex_deterministic_dispatch_envelope(**values)

    def test_valid_envelope_binds_valid_blk040_profile_and_records_no_execution(self):
        result = self._build()

        self.assertEqual(result["profile_id"], "codex_deterministic_dispatch_envelope")
        self.assertEqual(result["dispatch_status"], "CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY")
        self.assertEqual(result["codex_profile"]["profile_id"], "codex_deterministic_invocation_profile")
        self.assertFalse(result["dispatch_started_by_envelope_helper"])
        self.assertFalse(result["subprocess_started_by_envelope_helper"])
        self.assertFalse(result["profile_grants_execution_authority"])
        self.assertEqual(result["telemetry_authority"], "CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY")

    def test_requires_complete_approval_provenance_and_excluded_authorities(self):
        required = [
            "approval_id",
            "source_system",
            "operator_identity",
            "message_event_id",
            "timestamp",
            "expires_at",
            "exact_approved_scope",
            "explicit_excluded_authorities",
        ]
        for field in required:
            with self.subTest(field=field):
                approval = self._approval()
                approval.pop(field)
                with self.assertRaisesRegex(ValueError, field):
                    self._build(approval_provenance=approval)

        approval = self._approval(explicit_excluded_authorities=["live_codex_execution"])
        with self.assertRaisesRegex(ValueError, "excluded"):
            self._build(approval_provenance=approval)

    def test_rejects_expired_replayed_or_missing_replay_state(self):
        with self.assertRaisesRegex(ValueError, "expired"):
            self._build(approval_provenance=self._approval(expires_at="2026-05-09T13:00:00+10:00"))
        with self.assertRaisesRegex(ValueError, "replayed approval"):
            self._build(used_approval_ids={"CODEX-DISPATCH-APPROVAL-039-001"})
        with self.assertRaisesRegex(ValueError, "replayed run"):
            self._build(used_run_ids={"CODEX-DISPATCH-RUN-039-001"})
        with self.assertRaisesRegex(ValueError, "used_approval_ids"):
            self._build(used_approval_ids=None)
        with self.assertRaisesRegex(ValueError, "used_run_ids"):
            self._build(used_run_ids=None)

    def test_rejects_broad_or_protected_file_boundaries(self):
        bad_paths = [
            ".",
            "*",
            "src/*",
            ":(glob)**",
            "../escape.py",
            "/tmp/escape.py",
            "docs/active/REQ-001.md",
            "docs/requirements/staging/REQ.md",
            "docs/use_cases/staging/UC.md",
            ".git/config",
            "python/good.py; rm -rf .",
            "python/good.py && touch bad",
        ]
        for bad_path in bad_paths:
            with self.subTest(bad_path=bad_path):
                with self.assertRaises(ValueError):
                    self._build(allowed_modified_files=[bad_path])

    def test_rejects_missing_or_free_form_validation_gates(self):
        with self.assertRaisesRegex(ValueError, "validation"):
            self._build(validation_profiles=[])
        for bad_profile in ["python -m unittest", "npm install", "curl https://example.test", "codex exec"]:
            with self.subTest(bad_profile=bad_profile):
                with self.assertRaises(ValueError):
                    self._build(validation_profiles=[bad_profile])

    def test_rejects_escaping_or_unbounded_telemetry_paths(self):
        bad_paths = [
            "/tmp/events.jsonl",
            "../events.jsonl",
            "artifacts/codex/../events.jsonl",
            "docs/active/events.jsonl",
            "artifacts/codex/.git/events.jsonl",
            "artifacts/other/events.jsonl",
            "artifacts/codex/" + "x" * 200 + ".jsonl",
        ]
        for bad_path in bad_paths:
            with self.subTest(bad_path=bad_path):
                telemetry = dict(self._build()["telemetry_artifacts"])
                telemetry["jsonl_events"] = bad_path
                with self.assertRaises(ValueError):
                    self._build(telemetry_artifacts=telemetry)

    def test_requires_failure_ceiling_hostile_audit_and_escalation_cases(self):
        with self.assertRaisesRegex(ValueError, "failure_ceiling"):
            self._build(failure_ceiling={"max_iterations": 0})
        with self.assertRaisesRegex(ValueError, "hostile_audit"):
            self._build(hostile_audit={"required_checks": ["file_boundary_check"]})
        with self.assertRaisesRegex(ValueError, "operator_escalation"):
            self._build(operator_escalation={"required_cases": ["missing_approval"]})

    def test_rejects_live_execution_and_authority_laundering_even_when_nested(self):
        forbidden = [
            {"dispatch_started_by_envelope_helper": True},
            {"subprocess_started_by_envelope_helper": True},
            {"profile_grants_execution_authority": True},
            {"metadata": {"live_codex_execution_authorized": True}},
            {"metadata": {"blk_pipe_dispatch_authorized": True}},
            {"metadata": {"protected_body_read_authorized": True}},
            {"metadata": {"beo_publication_authorized": True}},
            {"metadata": {"rtm_generation_authority": "APPROVED"}},
            {"metadata": {"runtime_execution_authority": "APPROVED"}},
            {"metadata": {"generic_approval_claim": "APPROVED_FOR_LIVE_EXECUTION"}},
            {"metadata": {"drift_rejection_allowed": True}},
            {"metadata": {"claim": "CODEX_LIVE_APPROVAL"}},
            {"metadata": {"claim": "PRODUCTION_SANDBOX_ENFORCED"}},
            {"metadata": {"claim": "BLK_TEST_PASS grants execution authority"}},
        ]
        for override in forbidden:
            with self.subTest(override=override):
                result = self._build()
                result.update(override)
                with self.assertRaises(ValueError):
                    envelope.validate_codex_deterministic_dispatch_envelope(result, now=NOW, used_approval_ids=set(), used_run_ids=set())

    def test_rejects_invalid_embedded_codex_profile(self):
        codex_profile = self._codex_profile()
        codex_profile["argv"].remove("--ephemeral")
        with self.assertRaisesRegex(ValueError, "--ephemeral"):
            self._build(codex_profile=codex_profile)

    def test_validation_returns_envelope_when_shape_is_valid(self):
        result = self._build()
        self.assertIs(
            envelope.validate_codex_deterministic_dispatch_envelope(
                result, now=NOW, used_approval_ids=set(), used_run_ids=set()
            ),
            result,
        )

    def test_source_does_not_import_or_call_live_surfaces(self):
        source_path = Path(envelope.__file__)
        tree = ast.parse(source_path.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib"}
        forbidden_calls = {"system", "popen", "run", "Popen", "call", "check_call", "check_output", "exec", "eval"}
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
