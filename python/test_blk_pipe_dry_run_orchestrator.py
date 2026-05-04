import tempfile
import textwrap
import unittest
from pathlib import Path

from blk_pipe_dry_run_orchestrator import (
    DryRunSprintInput,
    TraceArtifact,
    build_codex_dry_run_payload,
    load_dry_run_fixture,
)


TRACE_ARTIFACT = TraceArtifact(
    kind="REQ",
    id="REQ-DRY-001",
    version_hash="sha256:" + "a" * 64,
)


class DryRunOrchestratorPayloadTest(unittest.TestCase):
    def _input(self, **overrides):
        values = {
            "beb_id": "BEB_004",
            "profile": "codex-dry-run",
            "work_dir": "/tmp/blk-ephemeral-repo",
            "target_branch": "sprint/blk-pipe-004-dry-run",
            "l2_packet": "L2_ID: L2_004\nBEB_ID: BEB_004\nDo fixture work.\n",
            "trace_artifacts": [TRACE_ARTIFACT],
            "allowed_new_files": ["dry_run_output.txt"],
            "validation_commands": ["test -f dry_run_output.txt"],
        }
        values.update(overrides)
        return DryRunSprintInput(**values)

    def test_build_payload_uses_codex_dry_run_profile(self):
        payload = build_codex_dry_run_payload(self._input())

        self.assertEqual(payload["action"], "execute")
        self.assertEqual(payload["beb_id"], "BEB_004")
        self.assertEqual(payload["work_dir"], "/tmp/blk-ephemeral-repo")
        self.assertEqual(payload["target_branch"], "sprint/blk-pipe-004-dry-run")
        self.assertEqual(payload["engine"], "codex-dry-run")
        self.assertEqual(payload["engine_args"][:2], ["exec", "-"])
        self.assertEqual(payload["validation_commands"], ["test -f dry_run_output.txt"])
        self.assertEqual(payload["allowed_modified_files"], [])
        self.assertEqual(payload["allowed_new_files"], ["dry_run_output.txt"])

    def test_build_payload_includes_blk003_required_isolation_args(self):
        payload = build_codex_dry_run_payload(self._input())

        for arg in [
            "--json",
            "--isolated",
            "--yes",
            "--deny-read=**/.git/**",
            "--deny-read=**/node_modules/**",
            "--deny-read=**/.env*",
            "--dry-run",
        ]:
            self.assertIn(arg, payload["engine_args"])

    def test_build_payload_preserves_l2_packet_and_trace_artifacts(self):
        l2_packet = "L2_ID: L2_004\nBEB_ID: BEB_004\nfixture body\n"
        payload = build_codex_dry_run_payload(self._input(l2_packet=l2_packet))

        self.assertEqual(payload["l2_packet"], l2_packet)
        self.assertEqual(
            payload["trace_artifacts"],
            [
                {
                    "kind": "REQ",
                    "id": "REQ-DRY-001",
                    "version_hash": "sha256:" + "a" * 64,
                }
            ],
        )

    def test_build_payload_rejects_codex_live_profile(self):
        with self.assertRaisesRegex(ValueError, "codex-dry-run"):
            build_codex_dry_run_payload(self._input(profile="codex-live"))

    def test_build_payload_rejects_empty_unknown_and_cyber_profiles(self):
        for profile in ["", "dev-smoke", "strict-ci", "cyber-execution", "model-service"]:
            with self.subTest(profile=profile):
                with self.assertRaisesRegex(ValueError, "codex-dry-run"):
                    build_codex_dry_run_payload(self._input(profile=profile))

    def test_build_payload_uses_absolute_work_dir(self):
        with self.assertRaisesRegex(ValueError, "absolute work_dir"):
            build_codex_dry_run_payload(self._input(work_dir="relative/repo"))

    def test_build_payload_uses_l2_fixture_bytes_exactly(self):
        root = Path(__file__).resolve().parents[1]
        beb_path = root / "testdata" / "orchestrator" / "BEB_004_dry_run.md"
        l2_path = root / "testdata" / "orchestrator" / "L2_004_dry_run.md"
        l2_text = l2_path.read_text()

        fixture_input = load_dry_run_fixture(
            beb_path=beb_path,
            l2_path=l2_path,
            work_dir="/tmp/blk-ephemeral-repo",
        )
        payload = build_codex_dry_run_payload(fixture_input)

        self.assertEqual(payload["l2_packet"], l2_text)
        self.assertEqual(payload["beb_id"], "BEB_004")

    def test_build_payload_rejects_beb_l2_id_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            beb_path = tmp_path / "beb.md"
            l2_path = tmp_path / "l2.md"
            beb_path.write_text(
                textwrap.dedent(
                    """
                    ---
                    beb_id: "BEB_004"
                    l2_id: "L2_004"
                    iteration: 1
                    status: "FIXTURE"
                    sprint_base_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    traced_artifacts:
                      - kind: "REQ"
                        id: "REQ-DRY-001"
                        version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    ---
                    BEB body.
                    """
                ).lstrip()
            )
            l2_path.write_text("L2_ID: L2_OTHER\nBEB_ID: BEB_004\n")

            with self.assertRaisesRegex(ValueError, "L2"):
                load_dry_run_fixture(beb_path, l2_path, "/tmp/blk-ephemeral-repo")

    def test_build_payload_rejects_missing_trace_artifact_in_beb_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            beb_path = tmp_path / "beb.md"
            l2_path = tmp_path / "l2.md"
            beb_path.write_text(
                textwrap.dedent(
                    """
                    ---
                    beb_id: "BEB_004"
                    l2_id: "L2_004"
                    iteration: 1
                    status: "FIXTURE"
                    sprint_base_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                    ---
                    BEB body.
                    """
                ).lstrip()
            )
            l2_path.write_text("L2_ID: L2_004\nBEB_ID: BEB_004\n")

            with self.assertRaisesRegex(ValueError, "trace"):
                load_dry_run_fixture(beb_path, l2_path, "/tmp/blk-ephemeral-repo")


if __name__ == "__main__":
    unittest.main()
