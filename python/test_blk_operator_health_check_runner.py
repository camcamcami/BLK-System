import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import blk_operator_health_check_runner as runner

ROOT = Path(__file__).resolve().parents[1]


class FakePopen:
    returncode = 0
    pid = 43210
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

    def communicate(self, input=None, timeout=None):
        if self.timeout:
            raise subprocess.TimeoutExpired(cmd=type(self).captured["argv"], timeout=timeout)
        stdout_target = type(self).captured.get("stdout")
        stderr_target = type(self).captured.get("stderr")
        if hasattr(stdout_target, "write"):
            stdout_target.write(self.stdout_text.encode("utf-8"))
        if hasattr(stderr_target, "write"):
            stderr_target.write(self.stderr_text.encode("utf-8"))
        return self.stdout_text, self.stderr_text

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

        with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
            runner.subprocess, "Popen", FakePopen
        ):
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
        self.assertEqual(captured["env"]["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertIn("PYTHONPYCACHEPREFIX", captured["env"])
        self.assertNotIn(str(ROOT.resolve()), str(Path(captured["env"]["PYTHONPYCACHEPREFIX"]).resolve()))
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
        self.assertFalse(result["workspace_status_changed"])
        self.assertEqual(result["git_mutated"], "NO_WORKSPACE_STATUS_CHANGE_OBSERVED")
        self.assertEqual(result["source_mutated"], "NOT_MEASURED_BY_PILOT")
        for flag in ["approval_captured", "production_authority_granted"]:
            self.assertFalse(result[flag], flag)
        for flag in [
            "network_called",
            "package_manager_called",
            "protected_body_read",
            "active_vault_scanned",
            "beo_published",
            "rtm_generated",
            "drift_decision_made",
        ]:
            self.assertEqual(result[flag], "NOT_MEASURED_BY_PILOT", flag)
        self.assertEqual(result["side_effect_observation_scope"], "GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY")
        self.assertFalse(result["repo_cache_artifacts_changed"])
        self.assertEqual(result["repo_cache_artifacts"], "NO_REPO_CACHE_ARTIFACT_CHANGE_OBSERVED")
        self.assertTrue(result["runner_temp_removed"])
        self.assertEqual(result["runner_temp_containment"], "RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO")
        self.assertEqual(result["production_sandbox_enforced"], "NOT_ENFORCED_BY_PILOT")
        self.assertEqual(result["network_firewall_enforced"], "NOT_ENFORCED_BY_PILOT")
        self.assertEqual(result["host_secret_isolation_enforced"], "NOT_ENFORCED_BY_PILOT")
        self.assertIn("TMPDIR", captured["env"])
        self.assertIn("TMP", captured["env"])
        self.assertIn("TEMP", captured["env"])
        for key in ["TMPDIR", "TMP", "TEMP", "PYTHONPYCACHEPREFIX"]:
            self.assertNotIn(str(ROOT.resolve()), str(Path(captured["env"][key]).resolve()), key)

    def test_expanded_profiles_use_exact_fixed_argv_tails_and_advisory_status(self):
        expected = {
            "git_status_short_branch": ("git", ["status", "--short", "--branch"], "ADVISORY_ONLY"),
            "active_doctrine_gate": (
                "python3",
                ["-m", "unittest", "python.test_active_doctrine_review_gates"],
                "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
            ),
            "python_unittest_discovery": (
                "python3",
                ["-m", "unittest", "discover", "-s", "python", "-p", "test_*.py"],
                "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED",
            ),
            "go_test_all": ("go", ["test", "./..."], "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
            "go_vet_all": ("go", ["vet", "./..."], "BLOCKING_IF_LATER_EXECUTION_AUTHORIZED"),
        }
        self.assertEqual(set(runner.PROFILES), set(expected))
        for profile_id, (exe_name, tail, classification) in expected.items():
            with self.subTest(profile_id=profile_id):
                profile = runner.PROFILES[profile_id]
                if exe_name == "python3":
                    self.assertRegex(Path(profile.argv[0]).name, r"^python3(?:\.\d+)?$")
                else:
                    self.assertEqual(Path(profile.argv[0]).name, exe_name)
                self.assertTrue(Path(profile.argv[0]).is_absolute(), profile.argv)
                self.assertEqual(list(profile.argv[1:]), tail)
                self.assertEqual(profile.classification, classification)
                FakePopen.stdout_text = f"{profile_id} ok\n"
                with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
                    runner.subprocess, "Popen", FakePopen
                ):
                    result = runner.run_health_check(profile_id, repo_root=ROOT)
                self.assertEqual(result["profile_id"], profile_id)
                self.assertEqual(result["status"], "PASS_ADVISORY_ONLY")
                self.assertEqual(result["argv"][1:], tail)
                self.assertFalse(result["health_check_pass_grants_authority"])
                self.assertFalse(result["production_authority_granted"])

    def test_malicious_path_does_not_change_resolved_executable_or_runner_path(self):
        with patch.dict(runner.os.environ, {"PATH": "/tmp/evil:/usr/bin:/bin", "GITHUB_TOKEN": "secret"}, clear=False):
            for profile_id in ["git_status_short_branch", "go_test_all", "go_vet_all"]:
                with self.subTest(profile_id=profile_id):
                    with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
                        runner.subprocess, "Popen", FakePopen
                    ):
                        runner.run_health_check(profile_id, repo_root=ROOT)
                    executable = Path(FakePopen.captured["argv"][0]).name
                    self.assertNotEqual(FakePopen.captured["argv"][0], f"/tmp/evil/{executable}")
                    self.assertNotIn("/tmp/evil", FakePopen.captured["env"].get("PATH", ""))
                    self.assertNotIn("GITHUB_TOKEN", FakePopen.captured["env"])

    def test_python_profile_does_not_trust_untrusted_current_interpreter(self):
        with patch.object(runner.sys, "executable", "/bin/sh"):
            self.assertNotEqual(runner._trusted_executable("python3"), str(Path("/bin/sh").resolve()))

    def test_trusted_executable_rejects_symlink_escape_from_trusted_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted_bin = Path(tmp) / "trusted-bin"
            trusted_bin.mkdir()
            (trusted_bin / "go").symlink_to("/bin/sh")
            with patch.object(runner, "TRUSTED_PATH", str(trusted_bin)):
                with self.assertRaises(ValueError):
                    runner._trusted_executable("go")

    def test_source_mutation_during_profile_is_detected_as_blocked(self):
        marker = ROOT / "python" / "__blk_runner_mutation_probe.tmp"

        class MutatingPopen(FakePopen):
            def communicate(self, timeout=None):
                marker.write_text("mutation")
                return super().communicate(timeout=timeout)

        try:
            with patch.object(runner, "_git_status_snapshot", side_effect=["clean", "dirty"]), patch.object(
                runner.subprocess, "Popen", MutatingPopen
            ):
                result = runner.run_health_check("git_status_short_branch", repo_root=ROOT)
            self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
            self.assertTrue(result["workspace_status_changed"])
            self.assertEqual(result["git_mutated"], "WORKSPACE_STATUS_CHANGED")
            self.assertEqual(result["source_mutated"], "WORKSPACE_STATUS_CHANGED")
            self.assertIn("workspace changed during health-check", result["stderr_excerpt"])
        finally:
            marker.unlink(missing_ok=True)

    def test_git_status_snapshot_uses_non_mutating_optional_lock_guard(self):
        captured = {}

        class Completed:
            stdout = ""
            stderr = ""
            returncode = 0

        def fake_run(argv, **kwargs):
            captured["argv"] = argv
            captured.update(kwargs)
            return Completed()

        with patch.object(runner.subprocess, "run", fake_run):
            snapshot = runner._git_status_snapshot(str(ROOT), {"PATH": "/usr/bin:/bin"})

        self.assertIn("status", captured["argv"])
        self.assertEqual(captured["env"]["GIT_OPTIONAL_LOCKS"], "0")
        self.assertIs(captured["shell"], False)
        self.assertEqual(snapshot, "\nexit=0")

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

        with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
            runner.subprocess, "Popen", FakePopen
        ):
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

        with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
            runner.subprocess, "Popen", FakePopen
        ):
            result = runner.run_health_check("git_status_short_branch", repo_root=ROOT, excerpt_max_chars=48, output_byte_limit=1024)

        self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
        self.assertIsNone(result["exit_code"])
        self.assertLessEqual(len(result["stdout_excerpt"]), 48)
        self.assertIn("output limit exceeded", result["stderr_excerpt"])
        self.assertFalse(result["raw_output_embedded"])
        self.assertFalse(result["health_check_pass_grants_authority"])

    def test_timeout_returns_blocked_advisory_result_without_authority(self):
        FakePopen.timeout = True
        killpg_calls = []

        def fake_killpg(pid, sig):
            killpg_calls.append((pid, sig))

        with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
            runner.subprocess, "Popen", FakePopen
        ), patch.object(runner.os, "killpg", fake_killpg):
            result = runner.run_health_check("active_doctrine_gate", repo_root=ROOT)

        self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
        self.assertIsNone(result["exit_code"])
        self.assertIn("timed out", result["stderr_excerpt"])
        self.assertTrue(FakePopen.captured["start_new_session"])
        self.assertEqual(killpg_calls, [(FakePopen.pid, runner.signal.SIGKILL)])
        self.assertFalse(result["health_check_pass_grants_authority"])
        self.assertEqual(result["rtm_generated"], "NOT_MEASURED_BY_PILOT")
        self.assertEqual(result["drift_decision_made"], "NOT_MEASURED_BY_PILOT")
        self.assertEqual(result["process_group_timeout_cleanup"], "PROCESS_GROUP_KILL_ATTEMPTED")

    def test_repo_local_cache_artifact_change_blocks_advisory_pass(self):
        with patch.object(runner, "_git_status_snapshot", return_value="clean"), patch.object(
            runner, "_repo_cache_snapshot", side_effect=[frozenset(), frozenset({"python/__pycache__/leak.pyc"})], create=True
        ), patch.object(runner.subprocess, "Popen", FakePopen):
            result = runner.run_health_check("git_status_short_branch", repo_root=ROOT)

        self.assertEqual(result["status"], "BLOCKED_ADVISORY_ONLY")
        self.assertTrue(result["repo_cache_artifacts_changed"])
        self.assertEqual(result["repo_cache_artifacts"], "REPO_CACHE_ARTIFACT_CHANGE_OBSERVED")
        self.assertIn("repo-local cache artifacts changed", result["stderr_excerpt"])

    def test_fixed_profile_set_remains_unchanged_by_side_effect_boundary(self):
        self.assertEqual(
            set(runner.PROFILES),
            {"git_status_short_branch", "active_doctrine_gate", "python_unittest_discovery", "go_test_all", "go_vet_all"},
        )


if __name__ == "__main__":
    unittest.main()
