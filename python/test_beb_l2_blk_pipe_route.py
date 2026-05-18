import hashlib
import json
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from beb_l2_blk_pipe_route import (
    RouteError,
    build_ignored_residue_cleanup_plan,
    build_kuronode_codex_engine_args,
    dispatch_inbox_once,
    preflight_drop_file,
    process_drop_file,
)
from blk_pipe_adapter import BlkPipeAdapter


TRACE_ARTIFACTS = [
    {"kind": "REQ", "id": "REQ-222", "version_hash": "sha256:" + "2" * 64},
]
TARGET_HASH = "a" * 40


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def execute_sprint(self, **kwargs):
        self.calls.append(kwargs)
        return {"status": "SUCCESS", "commit_hash": "abc123"}


class BebL2BlkPipeRouteTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.work_dir = self.root / "workspace" / "kuronode"
        self.work_dir.mkdir(parents=True)
        self.beb_path = self.root / "BEB_222.md"
        self.l2_path = self.root / "L2_222.md"
        self.drop_path = self.root / "drop.json"
        self.beb_path.write_text(
            "---\n"
            "beb_id: \"BEB_222\"\n"
            "l2_id: \"L2_222\"\n"
            "trace_artifacts:\n"
            "  - kind: \"REQ\"\n"
            "    id: \"REQ-222\"\n"
            "    version_hash: \"sha256:2222222222222222222222222222222222222222222222222222222222222222\"\n"
            "---\n"
            "# BEB 222\n"
        )
        self.l2_path.write_text(
            "L2_ID: L2_222\n"
            "BEB_ID: BEB_222\n"
            "MODEL: gpt-5.5\n"
            "Implement the exact bounded Kuronode task through Codex.\n"
        )
        self.write_drop()

    def sha(self, path: Path) -> str:
        return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

    def route_kwargs(self):
        return {
            "allowed_work_dirs": [self.work_dir],
            "trusted_roots": [self.root],
            "approved_drop_sha256": self.sha(self.drop_path),
        }

    def process(self, adapter):
        return process_drop_file(self.drop_path, adapter=adapter, **self.route_kwargs())

    def init_git_workdir(self, ignored: bool = False) -> str:
        subprocess.run(["git", "init", "-b", "sprint/beb-222"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.name", "test"], cwd=self.work_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.work_dir, check=True)
        tracked = self.work_dir / "src" / "components" / "CanonicalDataGrid.tsx"
        tracked.parent.mkdir(parents=True, exist_ok=True)
        tracked.write_text("export const marker = 'before';\n")
        if ignored:
            (self.work_dir / ".gitignore").write_text("node_modules/\n")
            ignored_file = self.work_dir / "node_modules" / "left-pad" / "index.js"
            ignored_file.parent.mkdir(parents=True, exist_ok=True)
            ignored_file.write_text("module.exports = {};\n")
        subprocess.run(["git", "add", "."], cwd=self.work_dir, check=True)
        subprocess.run(["git", "commit", "-m", "initial"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.work_dir, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
        self.write_drop(target_hash=head)
        return head

    def write_drop(self, **overrides):
        manifest = {
            "target_project": "kuronode",
            "beb_id": "BEB_222",
            "l2_id": "L2_222",
            "beb_path": str(self.beb_path),
            "beb_sha256": self.sha(self.beb_path),
            "l2_path": str(self.l2_path),
            "l2_sha256": self.sha(self.l2_path),
            "work_dir": str(self.work_dir),
            "target_branch": "sprint/beb-222",
            "target_hash": TARGET_HASH,
            "allowed_modified_files": ["src/components/CanonicalDataGrid.tsx"],
            "allowed_new_files": [],
            "validation_profiles": ["python-unittest"],
        }
        manifest.update(overrides)
        self.drop_path.write_text(json.dumps(manifest))
        return manifest

    def test_preflight_reports_clean_exact_target_ready_without_invoking_engine(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["target_hash"], target_hash)
        self.assertEqual(report["blockers"], [])
        self.assertEqual(report["allowed_modified_files"], ["src/components/CanonicalDataGrid.tsx"])
        self.assertEqual(adapter.calls, [])

    def test_preflight_blocks_kuronode_dependency_cache_before_codex(self):
        self.init_git_workdir(ignored=True)

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "BLOCKED")
        blocker_codes = {blocker["code"] for blocker in report["blockers"]}
        self.assertIn("PREEXISTING_IGNORED_OR_UNTRACKED", blocker_codes)
        self.assertTrue(any("node_modules" in path for blocker in report["blockers"] for path in blocker["paths"]))

    def test_cleanup_plan_reports_dry_run_paths_without_removing_ignored_residue(self):
        self.init_git_workdir(ignored=True)
        ignored_file = self.work_dir / "node_modules" / "left-pad" / "index.js"

        plan = build_ignored_residue_cleanup_plan(self.drop_path, **self.route_kwargs())

        self.assertEqual(plan["status"], "CLEANUP_REQUIRED")
        self.assertFalse(plan["cleanup_authorized"])
        self.assertFalse(plan["mutation_performed"])
        self.assertFalse(plan["dispatch_authorized"])
        self.assertEqual(plan["dry_run_command"], ["git", "clean", "-ndX"])
        self.assertTrue(any("node_modules" in path for path in plan["dry_run_paths"]))
        self.assertTrue(ignored_file.exists(), "cleanup planner must not remove ignored files")

    def test_cleanup_plan_refuses_dirty_or_retargeted_worktrees_before_cleanup_advice(self):
        self.init_git_workdir(ignored=True)
        tracked = self.work_dir / "src" / "components" / "CanonicalDataGrid.tsx"
        tracked.write_text("export const marker = 'dirty';\n")

        plan = build_ignored_residue_cleanup_plan(self.drop_path, **self.route_kwargs())

        self.assertEqual(plan["status"], "BLOCKED_BY_NON_CLEANUP_PREFLIGHT")
        self.assertFalse(plan["cleanup_authorized"])
        self.assertFalse(plan["mutation_performed"])
        self.assertEqual(plan["dry_run_paths"], [])
        self.assertEqual(plan["dry_run_command"], [])
        self.assertIn("GIT_DIRTY", {blocker["code"] for blocker in plan["blockers"]})

    def test_process_drop_file_invokes_blk_pipe_with_real_codex_engine_and_exact_l2_packet(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()

        result = self.process(adapter)

        self.assertEqual(result, {"status": "SUCCESS", "commit_hash": "abc123"})
        self.assertEqual(len(adapter.calls), 1)
        payload = adapter.calls[0]
        self.assertEqual(payload["beb_id"], "BEB_222")
        self.assertEqual(payload["work_dir"], str(self.work_dir.resolve()))
        self.assertEqual(payload["target_branch"], "sprint/beb-222")
        self.assertEqual(payload["target_hash"], target_hash)
        self.assertEqual(payload["engine"], "codex")
        self.assertEqual(payload["l2_packet"], self.l2_path.read_text())
        self.assertEqual(payload["validation_profiles"], ["python-unittest"])
        self.assertNotIn("validation_commands", payload)
        self.assertEqual(payload["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args())

    def test_drop_manifest_cannot_override_engine_or_inject_validation_commands(self):
        adapter = FakeAdapter()
        for forbidden_field, value in {
            "engine": "sh",
            "engine_args": ["-c", "printf bypass"],
            "engine_command": ["sh", "-c", "printf bypass"],
            "validation_commands": ["curl https://example.invalid"],
        }.items():
            with self.subTest(forbidden_field=forbidden_field):
                self.write_drop(**{forbidden_field: value})
                with self.assertRaisesRegex(RouteError, forbidden_field):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_drop_manifest_requires_kuronode_project_and_beb_l2_binding_before_dispatch(self):
        adapter = FakeAdapter()
        bad_cases = [
            {"target_project": "other"},
            {"beb_id": "BEB_OTHER"},
            {"l2_id": "L2_OTHER"},
        ]
        for overrides in bad_cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaises(RouteError):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_route_requires_trusted_workdir_roots_hashes_and_target_hash(self):
        adapter = FakeAdapter()
        outside = self.root.parent / "not-kuronode"
        outside.mkdir(exist_ok=True)
        cases = [
            ({"work_dir": str(outside)}, r"work_dir.*approved"),
            ({"beb_path": str(outside / "BEB.md"), "beb_sha256": "sha256:" + "1" * 64}, r"beb_path.*trusted root"),
            ({"beb_sha256": "sha256:" + "1" * 64}, r"beb_path sha256"),
            ({"l2_sha256": "sha256:" + "1" * 64}, r"l2_path sha256"),
            ({"target_hash": "main"}, r"target_hash"),
        ]
        for overrides, pattern in cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaisesRegex(RouteError, pattern):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_route_requires_approved_manifest_hash_from_trusted_config(self):
        adapter = FakeAdapter()
        approved = self.sha(self.drop_path)
        self.write_drop(target_branch="sprint/beb-222-retargeted")

        with self.assertRaisesRegex(RouteError, "drop_path sha256"):
            process_drop_file(
                self.drop_path,
                adapter=adapter,
                allowed_work_dirs=[self.work_dir],
                trusted_roots=[self.root],
                approved_drop_sha256=approved,
            )
        self.assertEqual(adapter.calls, [])

    def test_route_rejects_loose_validation_profiles_and_broad_allowlists(self):
        adapter = FakeAdapter()
        cases = [
            ({"validation_profiles": ["curl https://example.invalid"]}, "validation_profiles"),
            ({"validation_profiles": ["unknown-profile"]}, "validation_profiles"),
            ({"allowed_modified_files": ["."]}, "allowed_modified_files"),
            ({"allowed_modified_files": ["src/**/*.ts"]}, "allowed_modified_files"),
            ({"allowed_modified_files": [":(top)src/index.ts"]}, "allowed_modified_files"),
            ({"allowed_modified_files": ["docs/requirements/active/REQ-001.md"]}, "allowed_modified_files"),
        ]
        for overrides, pattern in cases:
            with self.subTest(overrides=overrides):
                self.write_drop(**overrides)
                with self.assertRaisesRegex(RouteError, pattern):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_process_drop_file_uses_adapter_payload_file_path_with_fake_blk_pipe(self):
        target_hash = self.init_git_workdir()
        capture_dir = self.root / "capture"
        fake_blk_pipe = self.root / "fake-blk-pipe"
        fake_blk_pipe.write_text(
            textwrap.dedent(
                """
                #!/usr/bin/env python3
                import json
                import os
                import sys
                from pathlib import Path

                payload_path = Path(sys.argv[2])
                payload = json.loads(payload_path.read_text())
                capture_dir = Path(os.environ["BLK_ROUTE_CAPTURE_DIR"])
                capture_dir.mkdir()
                (capture_dir / "argv.json").write_text(json.dumps(sys.argv[1:]))
                (capture_dir / "payload.json").write_text(json.dumps(payload))
                print(json.dumps({"status": "SUCCESS", "commit_hash": "route-commit"}))
                """
            ).lstrip()
        )
        fake_blk_pipe.chmod(fake_blk_pipe.stat().st_mode | stat.S_IXUSR)
        adapter = BlkPipeAdapter(binary_path=str(fake_blk_pipe))

        import os
        old_capture = os.environ.get("BLK_ROUTE_CAPTURE_DIR")
        os.environ["BLK_ROUTE_CAPTURE_DIR"] = str(capture_dir)
        try:
            result = self.process(adapter)
        finally:
            if old_capture is None:
                os.environ.pop("BLK_ROUTE_CAPTURE_DIR", None)
            else:
                os.environ["BLK_ROUTE_CAPTURE_DIR"] = old_capture

        payload = json.loads((capture_dir / "payload.json").read_text())
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.commit_hash, "route-commit")
        self.assertEqual(json.loads((capture_dir / "argv.json").read_text())[0], "--payload")
        self.assertEqual(payload["engine"], "codex")
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args())
        self.assertEqual(payload["l2_packet"], self.l2_path.read_text())
        self.assertEqual(payload["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(payload["target_hash"], target_hash)

    def test_inbox_dispatch_moves_successful_drop_after_invocation(self):
        self.init_git_workdir()
        inbox = self.root / "inbox"
        processed = self.root / "processed"
        failed = self.root / "failed"
        inbox.mkdir()
        drop = inbox / "BEB_222.drop.json"
        drop.write_text(self.drop_path.read_text())
        adapter = FakeAdapter()

        inbox_kwargs = self.route_kwargs()
        inbox_kwargs["approved_drop_sha256s"] = [inbox_kwargs.pop("approved_drop_sha256")]
        report = dispatch_inbox_once(inbox, processed, failed, adapter=adapter, **inbox_kwargs)

        self.assertEqual(report["status"], "SUCCESS")
        self.assertFalse(drop.exists())
        self.assertTrue((processed / drop.name).exists())
        self.assertFalse(failed.exists())
        self.assertEqual(len(adapter.calls), 1)

    def test_codex_args_are_not_caller_controlled(self):
        args = build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="high")

        self.assertEqual(args[:2], ["exec", "-"])
        self.assertIn("--model", args)
        self.assertIn("gpt-5.5", args)
        self.assertIn("model_reasoning_effort=high", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("--ask-for-approval", args)
        with self.assertRaisesRegex(RouteError, "model"):
            build_kuronode_codex_engine_args(model="gpt-5.4", reasoning_effort="high")
        with self.assertRaisesRegex(RouteError, "reasoning_effort"):
            build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="low")


if __name__ == "__main__":
    unittest.main()
