import unittest

import codex_cli_capability_probe as probe


class CodexCliCapabilityProbeTest(unittest.TestCase):
    def test_help_inventory_requires_current_blk_route_baseline_flags(self):
        help_text = """
Usage: codex exec [OPTIONS]
      --sandbox <MODE>
      [possible values: read-only, workspace-write, danger-full-access]
      --ephemeral
      --ignore-user-config
      --ignore-rules
      --disable <FEATURE>
      --json
      --output-last-message <FILE>
"""

        inventory = probe.classify_exec_help_flags(help_text)

        self.assertEqual(inventory["status"], "READY")
        self.assertEqual(inventory["required_flags"], list(probe.REQUIRED_BASELINE_EXEC_FLAGS))
        self.assertEqual(inventory["missing_required_flags"], [])
        self.assertIn("--sandbox workspace-write", inventory["required_route_capabilities"])
        self.assertEqual(inventory["authority"], "DIAGNOSTIC_ONLY_NOT_DISPATCH_AUTHORITY")

    def test_help_inventory_blocks_when_required_flag_is_missing_even_if_doctor_is_ok(self):
        help_text = """
Usage: codex exec [OPTIONS]
      --sandbox <MODE>
      --ephemeral
      --ignore-user-config
      --disable <FEATURE>
      --json
      --output-last-message <FILE>
"""

        report = probe.build_codex_cli_capability_report(
            codex_version_output="codex-cli 0.135.0\n",
            npm_latest_output="0.135.0\n",
            exec_help_output=help_text,
            doctor_output="Codex doctor OK; all checks passed\n",
            private_bwrap_descriptor={"status": "READY", "blockers": []},
        )

        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("--ignore-rules", report["exec_help_inventory"]["missing_required_flags"])
        self.assertEqual(report["doctor_evidence"]["authority"], "ADVISORY_ONLY")
        self.assertFalse(report["side_effect_authority"]["live_codex_dispatch_authorized"])
        self.assertFalse(report["side_effect_authority"]["broad_blk_pipe_dispatch_authorized"])

    def test_report_records_version_help_doctor_and_private_bwrap_without_granting_authority(self):
        report = probe.build_codex_cli_capability_report(
            codex_version_output="codex-cli 0.135.0\n",
            npm_latest_output="0.135.0\n",
            exec_help_output="\n".join(probe.REQUIRED_BASELINE_EXEC_FLAGS + ("--sandbox <MODE>", "workspace-write")),
            doctor_output=(
                "Logged in as cam@example.invalid at /home/dad/.codex/auth.json\n"
                "Auth diagnostics: credential present\n"
            ),
            private_bwrap_descriptor={
                "status": "READY",
                "private_bwrap_path": "/opt/blk-system/codex-bwrap/bwrap",
                "blockers": [],
            },
        )

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["codex_cli_version"], "codex-cli 0.135.0")
        self.assertEqual(report["npm_latest_version"], "0.135.0")
        self.assertEqual(report["private_bwrap_descriptor"]["status"], "READY")
        self.assertEqual(
            report["doctor_evidence"]["text"],
            "Logged in as [REDACTED_EMAIL] at [REDACTED_HOME]/.codex/auth.json\nAuth diagnostics: credential present",
        )
        for key, value in report["side_effect_authority"].items():
            self.assertFalse(value, key)


    def test_help_inventory_blocks_when_workspace_write_mode_is_not_advertised(self):
        help_text = """
Usage: codex exec [OPTIONS]
      --sandbox <MODE>
      [possible values: read-only, danger-full-access]
      --ephemeral
      --ignore-user-config
      --ignore-rules
      --disable <FEATURE>
      --json
      --output-last-message <FILE>
"""

        inventory = probe.classify_exec_help_flags(help_text)

        self.assertEqual(inventory["status"], "BLOCKED")
        self.assertIn("--sandbox workspace-write", inventory["missing_required_capabilities"])

    def test_report_blocks_contradictory_ready_descriptor_with_blockers(self):
        report = probe.build_codex_cli_capability_report(
            codex_version_output="codex-cli 0.135.0\n",
            npm_latest_output="0.135.0\n",
            exec_help_output="\n".join(probe.REQUIRED_BASELINE_EXEC_FLAGS + ("workspace-write",)),
            doctor_output="Codex doctor OK\n",
            private_bwrap_descriptor={
                "status": "READY",
                "blockers": [{"code": "APPARMOR_PROFILE_NOT_LOADED"}],
            },
        )

        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("PRIVATE_BWRAP_DESCRIPTOR_CONTRADICTORY", {b["code"] for b in report["blockers"]})


    def test_report_blocks_ready_descriptor_with_malformed_nonempty_blockers(self):
        for blockers in [
            {"code": "APPARMOR_PROFILE_NOT_LOADED"},
            "APPARMOR_PROFILE_NOT_LOADED",
        ]:
            with self.subTest(blockers=blockers):
                report = probe.build_codex_cli_capability_report(
                    codex_version_output="codex-cli 0.135.0\n",
                    npm_latest_output="0.135.0\n",
                    exec_help_output="\n".join(probe.REQUIRED_BASELINE_EXEC_FLAGS + ("workspace-write",)),
                    doctor_output="Codex doctor OK\n",
                    private_bwrap_descriptor={"status": "READY", "blockers": blockers},
                )

                self.assertEqual(report["status"], "BLOCKED")
                self.assertIn("PRIVATE_BWRAP_DESCRIPTOR_BLOCKERS_MALFORMED", {b["code"] for b in report["blockers"]})

    def test_report_recursively_sanitizes_private_bwrap_descriptor(self):
        report = probe.build_codex_cli_capability_report(
            codex_version_output="codex-cli 0.135.0\n",
            npm_latest_output="0.135.0\n",
            exec_help_output="\n".join(probe.REQUIRED_BASELINE_EXEC_FLAGS + ("workspace-write",)),
            doctor_output="Codex doctor OK\n",
            private_bwrap_descriptor={
                "status": "BLOCKED",
                "blockers": [
                    {
                        "code": "APPARMOR_PROFILE_NOT_LOADED",
                        "path": "/home/dad/.codex/auth.json",
                        "note": "api_key: ghp_12cdef",
                    }
                ],
            },
        )

        descriptor_text = repr(report["private_bwrap_descriptor"])
        self.assertNotIn("/home/dad/.codex", descriptor_text)
        self.assertNotIn("ghp_12cdef", descriptor_text)
        self.assertIn("[REDACTED_HOME]/.codex/auth.json", descriptor_text)
        self.assertIn("[REDACTED_SECRET]", descriptor_text)

    def test_redaction_scrubs_tokens_api_keys_and_home_profile_paths(self):
        raw = """
OPENAI_API_KEY=sk-abc123
api_key: ghp_12cdef
/home/dad/.codex/auth.json
/home/dad/.hermes/.env
cam@example.com
"""

        redacted = probe.redact_sensitive_diagnostics(raw)

        self.assertNotIn("sk-abc123", redacted)
        self.assertNotIn("ghp_12cdef", redacted)
        self.assertNotIn("/home/dad/.codex", redacted)
        self.assertNotIn("/home/dad/.hermes", redacted)
        self.assertNotIn("cam@example.com", redacted)
        self.assertIn("OPENAI_API_KEY=[REDACTED_SECRET]", redacted)
        self.assertIn("[REDACTED_HOME]/.codex/auth.json", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)


if __name__ == "__main__":
    unittest.main()
