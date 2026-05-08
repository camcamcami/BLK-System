import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import blk_operator_health_check_runner as runner

ROOT = Path(__file__).resolve().parents[1]


class FakePopen:
    returncode = 0
    stdout_text = ""
    stderr_text = ""
    timeout = False
    captured = {}
    killed = False

    def __init__(self, argv, **kwargs):
        type(self).captured = {"argv": argv, **kwargs}
        self.returncode = type(self).returncode
        self.stdout_text = type(self).stdout_text
        self.stderr_text = type(self).stderr_text
        self.timeout = type(self).timeout

    def communicate(self, timeout=None):
        if self.timeout:
            raise subprocess.TimeoutExpired(cmd=type(self).captured["argv"], timeout=timeout)
        type(self).captured["stdout"].write(self.stdout_text.encode("utf-8"))
        type(self).captured["stderr"].write(self.stderr_text.encode("utf-8"))
        return None, None

    def kill(self):
        type(self).killed = True

    def wait(self, timeout=None):
        return self.returncode


class AdvisoryHealthCheckRunnerTest(unittest.TestCase):
    def setUp(self):
        FakePopen.returncode = 0
        FakePopen.stdout_text = ""
        FakePopen.stderr_text = ""
        FakePopen.timeout = False
        FakePopen.captured = {}
        FakePopen.killed = False

    def test_known_profile_runs_absolute_trusted_executable_with_shell_false_and_advisory_pass(self):
        FakePopen.stdout_text = "## main...origin/main\n"

        with patch.object(runner.subprocess, "Popen", FakePopen):
            result = runner.run_health_check("git_status_short_branch", repo_root=ROOT)

        captured = FakePopen.captured
        self.assertTrue(Path(captured["argv"][0]).is_absolute(), captured["argv"])
        self.assertNotEqual(captured["argv"][0], "/tmp/evil/git")
        self.assertEqual(captured["argv"][1:], ["status", "--short", "--branch"])
        self.assertEqual(captured["cwd"], str(ROOT.resolve()))
        self.assertIs(captured["shell"], False)
        self.assertNotIn("GITHUB_TOKEN", captured["env"])
        self.assertNotIn("SSH_AUTH_SOCK", captured["env"])
        self.assertNotIn("/tmp/evil", captured["env"].get("PATH", ""))
        self.assertEqual(result["profile_id"], "git_status_short_branch")
        self.assertEqual(result["runner_status"], "HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY")
        self.assertEqual(result["execution_status"], "HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE")
        self.assertEqual(result["status"], "PASS_ADVISORY_ONLY")
        self.assertEqual(result["argv"][1:], ["status", "--short", "--branch"])
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["stdout_excerpt"], "## main...origin/main\n")
        self.assertRegex(result["evidence_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertFalse(result["health_check_pass_grants_authority"])
        self.assertFalse(result["shell_used"])
        self.assertTrue(result["command_executed"])
        self.assertTrue(result["subprocess_started"])
        for flag in [
            "network_called",
            "package_manager_called",
            "git_mutated",
            "source_mutated",
            "approval_captured",
            "protected_body_read",
            "active_vault_scanned",
            "beo_published",
            "rtm_generated",
            "drift_decision_made",
            "production_authority_granted",
        ]:
            self.assertFalse(result[flag], flag)

    def test_malicious_path_does_not_change_resolved_executable_or_runner_path(self):
        with patch.dict(runner.os.environ, {"PATH": "/tmp/evil:/usr/bin:/bin", "GITHUB_TOKEN": "secret"}, clear=False):
            with patch.object(runner.subprocess, "Popen", FakePopen):
                runner.run_health_check("git_status_short_branch", repo_root=ROOT)
        self.assertNotEqual(FakePopen.captured["argv"][0], "/tmp/evil/git")
        self.assertNotIn("/tmp/evil", FakePopen.captured["env"].get("PATH", ""))
        self.assertNotIn("GITHUB_TOKEN", FakePopen.captured["env"])

    def test_non_repository_root_fails_closed_before_subprocess(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(runner.subprocess, "Popen") as mocked_popen:
                with self.assertRaises(ValueError):
                    runner.run_health_check("active_doctrine_gate", repo_root=Path(tmp))
                mocked_popen.assert_not_called()

    def test_unknown_profiles_and_caller_supplied_commands_fail_closed_before_subprocess(self):
        with patch.object(runner.subprocess, "Popen") as mocked_popen:
            for bad in [
                "go_test",
                "bash -lc git status",
                "../git_status_short_branch",
                ["git", "status", "--short", "--branch"],
                {"profile_id": "git_status_short_branch"},
            ]:
                with self.subTest(bad=bad):
                    with self.assertRaises(ValueError):
                        runner.run_health_check(bad, repo_root=ROOT)
            mocked_popen.assert_not_called()

    def test_profile_registry_rejects_shell_inline_network_package_git_mutation_and_authority_laundering(self):
        forbidden = [
            ("bad_shell", ["bash", "-lc", "git status"]),
            ("bad_inline", ["python3", "-c", "print('x')"]),
            ("bad_network", ["curl", "https://example.invalid"]),
            ("bad_package", ["pip", "install", "requests"]),
            ("bad_git_mutation", ["git", "commit", "-m", "x"]),
            ("bad_protected", ["python3", "-m", "unittest", "docs/active/protected-vault/body.md"]),
            ("bad_rtm", ["python3", "-m", "generate_rtm"]),
        ]
        for profile_id, argv in forbidden:
            with self.subTest(profile_id=profile_id):
                with self.assertRaises(ValueError):
                    runner.validate_profile_registry({profile_id: runner.HealthCheckProfile(profile_id, argv, "ADVISORY_ONLY", 1)})

    def test_output_is_bounded_redacted_and_evidence_hash_is_deterministic(self):
        FakePopen.returncode = 1
        FakePopen.stdout_text = "prefix GITHUB_TOKEN=abc123 " + ("X" * 200)
        FakePopen.stderr_text = "Authorization: Bearer abc123\n"

        with patch.object(runner.subprocess, "Popen", FakePopen):
            first = runner.run_health_check("git_status_short_branch", repo_root=ROOT, excerpt_max_chars=48)
            second = runner.run_health_check("git_status_short_branch", repo_root=ROOT, excerpt_max_chars=48)

        self.assertEqual(first["status"], "FAIL_ADVISORY_ONLY")
        self.assertLessEqual(len(first["stdout_excerpt"]), 48)
        self.assertLessEqual(len(first["stderr_excerpt"]), 48)
        self.assertNotIn("abc123", first["stdout_excerpt"])
        self.assertNotIn("abc123", first["stderr_excerpt"])
        self.assertIn("[REDACTED]", first["stdout_excerpt"])
        self.assertTrue(first["redaction_applied"])
        self.assertFalse(first["raw_output_embedded"])
        self.assertEqual(first["evidence_hash"], second["evidence_hash"])

    def test_process_output_flood_returns_blocked_without_embedding_raw_output(self):
        FakePopen.stdout_text = "X" * 2048

        with patch.object(runner.subprocess, "Popen", FakePopen):
            result = runner.run_health_check("git_status_short_branch", repo_root=ROOT, excerpt_max_chars=48, output_byte_limit=1024)

        self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
        self.assertIsNone(result["exit_code"])
        self.assertLessEqual(len(result["stdout_excerpt"]), 48)
        self.assertIn("output limit exceeded", result["stderr_excerpt"])
        self.assertFalse(result["raw_output_embedded"])
        self.assertFalse(result["health_check_pass_grants_authority"])

    def test_timeout_returns_blocked_advisory_result_without_authority(self):
        FakePopen.timeout = True

        with patch.object(runner.subprocess, "Popen", FakePopen):
            result = runner.run_health_check("active_doctrine_gate", repo_root=ROOT)

        self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
        self.assertIsNone(result["exit_code"])
        self.assertIn("timed out", result["stderr_excerpt"])
        self.assertFalse(result["health_check_pass_grants_authority"])
        self.assertFalse(result["rtm_generated"])
        self.assertFalse(result["drift_decision_made"])


if __name__ == "__main__":
    unittest.main()
