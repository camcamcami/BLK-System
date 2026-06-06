import os
import stat
import tempfile
import unittest
from pathlib import Path
from typing import cast

from blk_pipe_adapter import _build_subprocess_env
from codex_private_bwrap_setup import (
    DEFAULT_INSTALL_DIR,
    DEFAULT_PROFILE_NAME,
    apparmor_profile_text,
    build_codex_private_bwrap_env,
    build_setup_summary,
    validate_private_bwrap_setup_descriptor,
)

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "runbooks" / "codex-private-bwrap-apparmor.md"
SETUP_SCRIPT = ROOT / "scripts" / "setup-codex-private-bwrap.sh"


class CodexPrivateBwrapSetup229Test(unittest.TestCase):
    def test_profile_text_targets_only_private_bwrap_path(self):
        private_bwrap = Path("/opt/blk-system/codex-bwrap/bwrap")

        profile = apparmor_profile_text(private_bwrap)

        self.assertIn(f"profile {DEFAULT_PROFILE_NAME} {private_bwrap} flags=(unconfined)", profile)
        self.assertIn("userns,", profile)
        self.assertNotIn("profile blk-codex-bwrap /usr/bin/bwrap", profile)
        self.assertNotIn("kernel.apparmor_restrict_unprivileged_userns=0", profile)

    def test_setup_summary_documents_rebuild_without_hostwide_sysctl_relaxation(self):
        summary = build_setup_summary()

        self.assertEqual(summary["install_dir"], str(DEFAULT_INSTALL_DIR))
        self.assertEqual(summary["profile_name"], DEFAULT_PROFILE_NAME)
        self.assertEqual(summary["required_sysctl"], "kernel.apparmor_restrict_unprivileged_userns=1")
        self.assertIn("sudo scripts/setup-codex-private-bwrap.sh", summary["operator_rebuild_commands"])
        self.assertTrue(any("apparmor_parser -r" in command for command in summary["operator_rebuild_commands"]))
        rebuild_commands = cast(list[str], summary["operator_rebuild_commands"])
        self.assertIsInstance(rebuild_commands, list)
        self.assertTrue(any("BLK_CODEX_PRIVATE_BWRAP_DIR" in command for command in rebuild_commands))
        commands = "\n".join(str(command) for command in rebuild_commands)
        self.assertIn("model_reasoning_effort='\"xhigh\"'", commands)
        self.assertNotIn("model_reasoning_effort='\"high\"'", commands)
        self.assertNotIn("kernel.apparmor_restrict_unprivileged_userns=0", commands)

    def test_build_codex_private_bwrap_env_prepends_private_directory(self):
        base_env = {"PATH": "/usr/bin:/bin", "KEEP": "yes"}

        env = build_codex_private_bwrap_env(base_env, private_bwrap_dir="/opt/blk-system/codex-bwrap")

        self.assertEqual(env["KEEP"], "yes")
        self.assertEqual(env["BLK_CODEX_PRIVATE_BWRAP_DIR"], "/opt/blk-system/codex-bwrap")
        self.assertEqual(env["PATH"], "/opt/blk-system/codex-bwrap:/usr/bin:/bin")

    def test_python_adapter_inherits_only_trusted_private_bwrap_path_for_blk_pipe_engine(self):
        old = os.environ.get("BLK_CODEX_PRIVATE_BWRAP_DIR")
        os.environ["BLK_CODEX_PRIVATE_BWRAP_DIR"] = str(DEFAULT_INSTALL_DIR)
        try:
            env = _build_subprocess_env("/tmp/workdir")
        finally:
            if old is None:
                os.environ.pop("BLK_CODEX_PRIVATE_BWRAP_DIR", None)
            else:
                os.environ["BLK_CODEX_PRIVATE_BWRAP_DIR"] = old

        self.assertEqual(env["BLK_CODEX_PRIVATE_BWRAP_DIR"], str(DEFAULT_INSTALL_DIR))
        self.assertTrue(env["PATH"].startswith(str(DEFAULT_INSTALL_DIR) + os.pathsep), env["PATH"])
        self.assertEqual(env["PWD"], "/tmp/workdir")

    def test_python_adapter_rejects_untrusted_private_bwrap_path_injection(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("BLK_CODEX_PRIVATE_BWRAP_DIR")
            os.environ["BLK_CODEX_PRIVATE_BWRAP_DIR"] = tmp
            try:
                with self.assertRaisesRegex(ValueError, "trusted BLK-SYSTEM-229 install dir"):
                    _build_subprocess_env("/tmp/workdir")
            finally:
                if old is None:
                    os.environ.pop("BLK_CODEX_PRIVATE_BWRAP_DIR", None)
                else:
                    os.environ["BLK_CODEX_PRIVATE_BWRAP_DIR"] = old

    def test_descriptor_rejects_global_symlinked_or_missing_private_bwrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_dir = root / "codex-bwrap"
            private_dir.mkdir()
            private = private_dir / "bwrap"
            private.write_text("#!/bin/sh\nexit 0\n")
            private.chmod(private.stat().st_mode | stat.S_IXUSR)
            symlink = private_dir / "bwrap-link"
            symlink.symlink_to(private)

            valid = validate_private_bwrap_setup_descriptor(
                private_bwrap_path=private,
                profile_names=[DEFAULT_PROFILE_NAME],
                apparmor_restrict_unprivileged_userns="1",
            )
            self.assertEqual(valid["status"], "READY")

            for bad_path, expected in [
                (Path("/usr/bin/bwrap"), "GLOBAL_BWRAP_PATH"),
                (symlink, "BWRAP_PATH_SYMLINK"),
                (private_dir / "missing-bwrap", "BWRAP_PATH_MISSING"),
            ]:
                with self.subTest(bad_path=bad_path):
                    report = validate_private_bwrap_setup_descriptor(
                        private_bwrap_path=bad_path,
                        profile_names=[DEFAULT_PROFILE_NAME],
                        apparmor_restrict_unprivileged_userns="1",
                    )
                    self.assertEqual(report["status"], "BLOCKED")
                    self.assertIn(expected, {blocker["code"] for blocker in report["blockers"]})

    def test_runbook_and_script_document_recreate_setup(self):
        self.assertTrue(RUNBOOK.exists(), "BLK-229 must document how to recreate the private-bwrap setup")
        self.assertTrue(SETUP_SCRIPT.exists(), "BLK-229 must provide a setup script for the private-bwrap setup")
        runbook = RUNBOOK.read_text()
        script = SETUP_SCRIPT.read_text()

        for marker in [
            "Native private-bwrap AppArmor setup",
            "sudo scripts/setup-codex-private-bwrap.sh",
            "kernel.apparmor_restrict_unprivileged_userns = 1",
            "BLK_CODEX_PRIVATE_BWRAP_DIR",
            "codex --model gpt-5.5",
            "--sandbox workspace-write",
            "model_reasoning_effort='\"xhigh\"'",
            "No host-wide AppArmor userns relaxation",
        ]:
            self.assertIn(marker, runbook)
        self.assertIn("profile blk-codex-bwrap", script)
        self.assertIn("userns,", script)
        self.assertNotIn("kernel.apparmor_restrict_unprivileged_userns=0", script)


if __name__ == "__main__":
    unittest.main()
