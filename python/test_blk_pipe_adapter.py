import json
import os
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from blk_pipe_adapter import BlkPipeAdapter, ExecutionResult


class BlkPipeAdapterTest(unittest.TestCase):
    def setUp(self):
        self._old_env = os.environ.copy()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.fake_binary = self._write_fake_blk_pipe()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._old_env)

    def _write_fake_blk_pipe(self):
        fake_path = Path(self.temp_dir.name) / "fake-blk-pipe"
        fake_path.write_text(
            textwrap.dedent(
                """
                #!/usr/bin/env python3
                import json
                import os
                import sys
                from pathlib import Path

                if sys.argv[1:] == ["--health"]:
                    raise SystemExit(int(os.environ.get("BLK_PIPE_FAKE_HEALTH_RC", "0")))

                if len(sys.argv) != 3 or sys.argv[1] != "--payload":
                    print("bad invocation", file=sys.stderr)
                    raise SystemExit(99)

                payload_path = Path(sys.argv[2])
                payload_text = payload_path.read_text()
                capture_dir = os.environ.get("BLK_PIPE_FAKE_CAPTURE_DIR")
                if capture_dir:
                    capture_path = Path(capture_dir)
                    capture_path.mkdir(parents=True, exist_ok=True)
                    (capture_path / "argv.json").write_text(json.dumps(sys.argv[1:]))
                    (capture_path / "payload_path.txt").write_text(str(payload_path))
                    (capture_path / "payload.json").write_text(payload_text)
                    (capture_path / "exists_during_run.txt").write_text(str(payload_path.exists()))

                return_code = int(os.environ.get("BLK_PIPE_FAKE_RC", "0"))
                if os.environ.get("BLK_PIPE_FAKE_STDOUT") == "non-json":
                    print("this is not json")
                    print("simulated stderr context", file=sys.stderr)
                    raise SystemExit(return_code)

                result = json.loads(os.environ.get("BLK_PIPE_FAKE_RESULT", "{}"))
                if not result:
                    result = {
                        "status": "SUCCESS",
                        "pre_engine_hash": "abc123",
                        "git_diff": "diff --git a/file b/file",
                        "engine_logs": "engine log text",
                        "validation_logs": {"go test ./...": "PASS"},
                        "diff_summary": {"files_changed": 1},
                        "error": None,
                        "untracked_files": ["new.txt"],
                    }
                print(json.dumps(result))
                raise SystemExit(return_code)
                """
            ).lstrip()
        )
        fake_path.chmod(fake_path.stat().st_mode | stat.S_IXUSR)
        return str(fake_path)

    def _adapter(self):
        return BlkPipeAdapter(binary_path=self.fake_binary)

    def test_execution_result_dataclass_defaults(self):
        result = ExecutionResult(status="SUCCESS", exit_code=0)

        self.assertEqual(result.pre_engine_hash, "")
        self.assertEqual(result.git_diff, "")
        self.assertEqual(result.engine_logs, "")
        self.assertIsNone(result.validation_logs)
        self.assertIsNone(result.diff_summary)
        self.assertIsNone(result.error)
        self.assertIsNone(result.untracked_files)

    def test_return_code_routes_strict_v47(self):
        routes = {
            0: "SUCCESS",
            1: "FATAL_SYSTEM_PANIC",
            2: "SYNTAX_GATE_FAILED",
            3: "UNAUTHORIZED_FILE_MUTATION",
            4: "INVALID_REVERT_ANCHOR",
            5: "FATAL_OUTPUT_FLOOD",
            6: "ENGINE_TIMEOUT",
            7: "GIT_DIRTY",
            9: "INTERNAL_ERROR",
        }

        for return_code, expected_status in routes.items():
            with self.subTest(return_code=return_code):
                os.environ["BLK_PIPE_FAKE_RC"] = str(return_code)
                os.environ["BLK_PIPE_FAKE_RESULT"] = json.dumps(
                    {
                        "status": "SUCCESS" if return_code == 0 else "SHOULD_BE_OVERRIDDEN",
                        "pre_engine_hash": "hash-value",
                        "git_diff": "diff-content",
                        "engine_logs": "engine-output",
                        "validation_logs": {"unit": "ok"},
                        "diff_summary": {"changed": ["a.py"]},
                        "error": "kernel error" if return_code else None,
                        "untracked_files": ["scratch.txt"],
                    }
                )

                result = self._adapter().execute_sprint(
                    ceb_id="CEB-1",
                    work_dir="/repo",
                    target_branch="main",
                    engine="fake-engine",
                    engine_args=["--safe"],
                    l2_packet="packet",
                    validation_commands=["python3 -m unittest"],
                    allowed_modified_files=["a.py"],
                    allowed_new_files=["scratch.txt"],
                )

                self.assertEqual(result.status, expected_status)
                self.assertEqual(result.exit_code, return_code)
                self.assertEqual(result.pre_engine_hash, "hash-value")
                self.assertEqual(result.git_diff, "diff-content")
                self.assertEqual(result.engine_logs, "engine-output")
                self.assertEqual(result.validation_logs, {"unit": "ok"})
                self.assertEqual(result.diff_summary, {"changed": ["a.py"]})
                self.assertEqual(result.untracked_files, ["scratch.txt"])

    def test_unknown_nonzero_return_code_never_reports_success(self):
        outputs = ["{}", json.dumps({"status": "SUCCESS"})]

        for stdout in outputs:
            with self.subTest(stdout=stdout):
                completed = subprocess.CompletedProcess(
                    args=[self.fake_binary, "--payload", "payload.json"],
                    returncode=42,
                    stdout=stdout,
                    stderr="unexpected rc",
                )
                with mock.patch("blk_pipe_adapter.subprocess.run", return_value=completed):
                    result = self._adapter()._invoke_binary({"action": "execute"})

                self.assertEqual(result.exit_code, 42)
                self.assertEqual(result.status, "INTERNAL_ERROR")

    def test_invalid_non_json_stdout_maps_to_fatal_crash_result(self):
        os.environ["BLK_PIPE_FAKE_RC"] = "1"
        os.environ["BLK_PIPE_FAKE_STDOUT"] = "non-json"

        result = self._adapter().execute_sprint(
            ceb_id="CEB-2",
            work_dir="/repo",
            target_branch="main",
            engine="fake-engine",
            engine_args=[],
            l2_packet="packet",
            validation_commands=[],
            allowed_modified_files=[],
            allowed_new_files=[],
        )

        self.assertEqual(result.status, "FATAL_CRASH")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.pre_engine_hash, "")
        self.assertEqual(result.git_diff, "")
        self.assertEqual(result.engine_logs, "")
        self.assertEqual(result.validation_logs, {})
        self.assertIn("simulated stderr context", result.error)

    def test_health_check_true_on_exit_zero_and_false_otherwise(self):
        os.environ["BLK_PIPE_FAKE_HEALTH_RC"] = "0"
        self.assertTrue(self._adapter().run_health_check())

        os.environ["BLK_PIPE_FAKE_HEALTH_RC"] = "7"
        self.assertFalse(self._adapter().run_health_check())

    def test_execute_sprint_writes_expected_payload_invokes_payload_and_removes_temp(self):
        capture_dir = Path(self.temp_dir.name) / "capture-execute"
        os.environ["BLK_PIPE_FAKE_CAPTURE_DIR"] = str(capture_dir)

        result = self._adapter().execute_sprint(
            ceb_id="CEB-3",
            work_dir="/repo",
            target_branch="feature/task",
            engine="codex-fake",
            engine_args=["--model", "none"],
            l2_packet="do work",
            validation_commands=["go test ./...", "python3 -m unittest"],
            allowed_modified_files=["python/blk_pipe_adapter.py"],
            allowed_new_files=["python/test_blk_pipe_adapter.py"],
        )

        payload = json.loads((capture_dir / "payload.json").read_text())
        payload_path = Path((capture_dir / "payload_path.txt").read_text())
        argv = json.loads((capture_dir / "argv.json").read_text())

        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(argv, ["--payload", str(payload_path)])
        self.assertTrue(str(payload_path).endswith(".json"))
        self.assertEqual((capture_dir / "exists_during_run.txt").read_text(), "True")
        self.assertFalse(payload_path.exists())
        self.assertEqual(
            payload,
            {
                "action": "execute",
                "ceb_id": "CEB-3",
                "work_dir": "/repo",
                "target_branch": "feature/task",
                "engine": "codex-fake",
                "engine_args": ["--model", "none"],
                "l2_packet": "do work",
                "validation_commands": ["go test ./...", "python3 -m unittest"],
                "allowed_modified_files": ["python/blk_pipe_adapter.py"],
                "allowed_new_files": ["python/test_blk_pipe_adapter.py"],
            },
        )

    def test_payload_temp_file_removed_when_payload_serialization_fails(self):
        temp_payload_dir = Path(self.temp_dir.name) / "serialization-failure"
        temp_payload_dir.mkdir()
        real_named_temporary_file = tempfile.NamedTemporaryFile

        def named_temp_file_in_test_dir(*args, **kwargs):
            kwargs["dir"] = temp_payload_dir
            return real_named_temporary_file(*args, **kwargs)

        with mock.patch(
            "blk_pipe_adapter.tempfile.NamedTemporaryFile",
            side_effect=named_temp_file_in_test_dir,
        ):
            with self.assertRaises(TypeError):
                self._adapter()._invoke_binary({"unserializable": object()})

        self.assertEqual(list(temp_payload_dir.iterdir()), [])

    def test_timeout_returns_timeout_result_and_removes_payload_temp_file(self):
        temp_payload_dir = Path(self.temp_dir.name) / "timeout"
        temp_payload_dir.mkdir()
        real_named_temporary_file = tempfile.NamedTemporaryFile
        payload_paths_seen = []

        def named_temp_file_in_test_dir(*args, **kwargs):
            kwargs["dir"] = temp_payload_dir
            return real_named_temporary_file(*args, **kwargs)

        def timeout_run(args, **kwargs):
            payload_path = Path(args[2])
            payload_paths_seen.append(payload_path)
            self.assertTrue(payload_path.exists())
            raise subprocess.TimeoutExpired(cmd=args, timeout=kwargs.get("timeout"))

        with mock.patch(
            "blk_pipe_adapter.tempfile.NamedTemporaryFile",
            side_effect=named_temp_file_in_test_dir,
        ):
            with mock.patch("blk_pipe_adapter.subprocess.run", side_effect=timeout_run):
                result = self._adapter()._invoke_binary({"action": "execute"})

        self.assertEqual(result.status, "FATAL_PYTHON_TIMEOUT")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(result.validation_logs, {})
        self.assertEqual(len(payload_paths_seen), 1)
        self.assertFalse(payload_paths_seen[0].exists())

    def test_abort_sprint_and_revert_writes_revert_payload(self):
        capture_dir = Path(self.temp_dir.name) / "capture-revert"
        os.environ["BLK_PIPE_FAKE_CAPTURE_DIR"] = str(capture_dir)

        result = self._adapter().abort_sprint_and_revert(
            work_dir="/repo",
            target_branch="main",
            pre_engine_hash="pre-hash",
        )

        payload = json.loads((capture_dir / "payload.json").read_text())
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(
            payload,
            {
                "action": "revert",
                "work_dir": "/repo",
                "target_branch": "main",
                "target_hash": "pre-hash",
                "ceb_id": "REVERT",
                "engine": "",
                "engine_args": [],
                "l2_packet": "",
                "validation_commands": [],
                "allowed_modified_files": [],
                "allowed_new_files": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
