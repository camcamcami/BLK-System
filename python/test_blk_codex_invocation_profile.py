import ast
import unittest
from pathlib import Path

import blk_codex_invocation_profile as profile


class CodexDeterministicInvocationProfileTest(unittest.TestCase):
    def _build(self, **overrides):
        values = {
            "approved_model": "gpt-5.4",
            "worktree": "/tmp/blk-system-codex-worktree",
            "final_message_artifact": "artifacts/codex/final-message.md",
            "prompt": "Execute the bounded tactical packet without expanding authority.",
        }
        values.update(overrides)
        return profile.build_codex_deterministic_invocation_profile(**values)

    def test_valid_profile_includes_required_deterministic_flags_and_argv_order(self):
        result = self._build()

        self.assertEqual(result["profile_id"], "codex_deterministic_invocation_profile")
        self.assertEqual(result["argv"][:2], ["codex", "exec"])
        self.assertEqual(
            result["argv"],
            [
                "codex",
                "exec",
                "--model",
                "gpt-5.4",
                "-C",
                "/tmp/blk-system-codex-worktree",
                "-s",
                "danger-full-access",
                "-a",
                "never",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--disable",
                "hooks",
                "--disable",
                "plugins",
                "--disable",
                "goals",
                "--json",
                "--output-last-message",
                "artifacts/codex/final-message.md",
            ],
        )
        self.assertEqual(result["sandbox_mode"], "danger-full-access")
        self.assertEqual(result["sandbox_authority"], "CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST")

    def test_valid_profile_disables_ambient_hooks_plugins_and_goals(self):
        result = self._build()

        self.assertEqual(result["ambient_features"], {"hooks": "disabled", "plugins": "disabled", "goals": "disabled"})
        for feature in ["hooks", "plugins", "goals"]:
            self.assertIn(("--disable", feature), zip(result["argv"], result["argv"][1:]))

    def test_valid_profile_records_advisory_telemetry_and_no_authority_flags(self):
        result = self._build()

        self.assertEqual(result["jsonl_events_authority"], "CODEX_JSONL_EVENTS_ADVISORY_ONLY")
        self.assertEqual(result["final_message_artifact_authority"], "CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY")
        self.assertFalse(result["subprocess_started_by_profile_helper"])
        self.assertFalse(result["command_executed"])
        self.assertFalse(result["profile_grants_execution_authority"])
        for key in [
            "production_sandbox_claimed",
            "network_model_cyber_tooling_authorized",
            "package_manager_authorized",
            "protected_body_read_authorized",
            "beo_publication_authorized",
            "rtm_generation_authorized",
            "drift_rejection_authorized",
            "source_mutation_authorized",
            "git_mutation_authorized",
        ]:
            self.assertFalse(result[key], key)

    def test_validate_rejects_missing_required_flags(self):
        required_flags = ["--ephemeral", "--ignore-user-config", "--ignore-rules", "--json"]
        for flag in required_flags:
            with self.subTest(flag=flag):
                result = self._build()
                result["argv"] = [item for item in result["argv"] if item != flag]
                with self.assertRaisesRegex(ValueError, flag):
                    profile.validate_codex_deterministic_invocation_profile(result)

    def test_validate_requires_bounded_relative_output_last_message_artifact(self):
        for bad_path in [
            "/tmp/final.md",
            "../final.md",
            "artifacts/codex/../final.md",
            "docs/active/final.md",
            "artifacts/codex/.git/final.md",
            "artifacts/other/final.md",
            "artifacts/codex/" + "x" * 200 + ".md",
        ]:
            with self.subTest(bad_path=bad_path):
                result = self._build()
                index = result["argv"].index("--output-last-message") + 1
                result["argv"][index] = bad_path
                result["final_message_artifact"] = bad_path
                with self.assertRaises(ValueError):
                    profile.validate_codex_deterministic_invocation_profile(result)

    def test_builder_rejects_absolute_or_escaping_artifact_path(self):
        for bad_path in ["/tmp/final.md", "../final.md", "artifacts/codex/../final.md"]:
            with self.subTest(bad_path=bad_path):
                with self.assertRaises(ValueError):
                    self._build(final_message_artifact=bad_path)

    def test_validate_rejects_missing_or_enabled_ambient_feature_disables(self):
        result = self._build()
        result["ambient_features"]["hooks"] = "enabled"
        with self.assertRaisesRegex(ValueError, "hooks"):
            profile.validate_codex_deterministic_invocation_profile(result)

        result = self._build()
        result["argv"].remove("plugins")
        with self.assertRaisesRegex(ValueError, "plugins"):
            profile.validate_codex_deterministic_invocation_profile(result)

    def test_builder_rejects_caller_supplied_extra_codex_flags(self):
        for extra_flags in [
            ["--dangerously-bypass-approvals-and-sandbox"],
            ["--enable", "hooks"],
            ["--config", "model_provider=ambient"],
            ["--plugin", "anything"],
            ["--mcp-server", "ambient"],
        ]:
            with self.subTest(extra_flags=extra_flags):
                with self.assertRaises(ValueError):
                    self._build(extra_flags=extra_flags)

    def test_validate_rejects_dangerously_bypass_flag_in_profile_shape(self):
        result = self._build()
        result["argv"].append("--dangerously-bypass-approvals-and-sandbox")
        with self.assertRaisesRegex(ValueError, "dangerously"):
            profile.validate_codex_deterministic_invocation_profile(result)

    def test_validate_rejects_production_and_live_authority_claims_even_when_nested(self):
        forbidden_overrides = [
            {"profile_grants_execution_authority": True},
            {"production_sandbox_claimed": True},
            {"metadata": {"beo_publication_authorized": True}},
            {"metadata": {"rtm_generation_authorized": True}},
            {"metadata": {"drift_rejection_authorized": True}},
            {"metadata": {"protected_body_read_authorized": True}},
            {"metadata": {"claim": "PRODUCTION_SANDBOX_ENFORCED"}},
            {"metadata": {"claim": "CODEX_LIVE_APPROVAL"}},
            {"metadata": {"claim": "BLK_TEST_PASS grants execution authority"}},
        ]
        for override in forbidden_overrides:
            with self.subTest(override=override):
                result = self._build()
                result.update(override)
                with self.assertRaises(ValueError):
                    profile.validate_codex_deterministic_invocation_profile(result)

    def test_validation_returns_profile_when_shape_is_valid(self):
        result = self._build()
        self.assertIs(profile.validate_codex_deterministic_invocation_profile(result), result)

    def test_source_does_not_import_or_call_subprocess_shell_git_network_or_package_managers(self):
        source_path = Path(profile.__file__)
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
