import contextlib
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from beb_l2_blk_pipe_route import (
    RouteError,
    build_hostile_review_record,
    build_clean_worktree_drop_manifest,
    build_ignored_residue_cleanup_plan,
    build_kuronode_codex_engine_args,
    build_route_commit_message,
    dispatch_inbox_once,
    main as route_main,
    preflight_drop_file,
    prepare_beb_l2_drop_package,
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

    def test_prepare_beb_l2_drop_package_writes_hash_bound_artifacts_ready_for_preflight(self):
        target_hash = self.init_git_workdir()
        package_dir = self.root / "packages" / "BLK-SYSTEM-232"

        package = prepare_beb_l2_drop_package(
            package_dir=package_dir,
            beb_id="BEB_232",
            l2_id="L2_232",
            work_dir=self.work_dir,
            target_branch="sprint/beb-222",
            target_hash=target_hash,
            objective="Add a visible Kuronode UI label through Codex.",
            l2_instructions="Modify only the approved UI file and keep tests passing.",
            allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
            allowed_new_files=[],
            validation_profiles=["python-unittest"],
            trace_artifacts=TRACE_ARTIFACTS,
        )

        self.assertEqual(package["status"], "BEB_L2_DROP_PACKAGE_READY")
        drop_path = Path(package["drop_path"])
        beb_path = Path(package["beb_path"])
        l2_path = Path(package["l2_path"])
        drop = json.loads(drop_path.read_text())
        self.assertEqual(package["approved_drop_sha256"], self.sha(drop_path))
        self.assertEqual(drop["beb_sha256"], self.sha(beb_path))
        self.assertEqual(drop["l2_sha256"], self.sha(l2_path))
        self.assertNotIn("engine", drop)
        self.assertNotIn("engine_args", drop)
        self.assertIn("BEB_ID: BEB_232", l2_path.read_text())
        self.assertIn("MODEL: gpt-5.5", l2_path.read_text())

        report = preflight_drop_file(
            drop_path,
            allowed_work_dirs=[self.work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=package["approved_drop_sha256"],
        )
        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["target_hash"], target_hash)

    def test_prepare_beb_l2_drop_package_rejects_caller_controlled_manifest_fields(self):
        target_hash = self.init_git_workdir()

        with self.assertRaisesRegex(RouteError, "caller-controlled"):
            prepare_beb_l2_drop_package(
                package_dir=self.root / "packages" / "bad",
                beb_id="BEB_232",
                l2_id="L2_232",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="bad package",
                l2_instructions="bad package",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                extra_manifest_fields={"engine": "sh", "l2_packet": "manual bypass"},
            )

    def test_prepare_beb_l2_drop_package_rejects_canonical_manifest_overrides(self):
        target_hash = self.init_git_workdir()
        attacker_l2 = self.root / "attacker-L2.md"
        attacker_l2.write_text("L2_ID: L2_232\nBEB_ID: BEB_232\nMODEL: gpt-5.5\nBypass helper packet.\n")

        with self.assertRaisesRegex(RouteError, "canonical manifest fields"):
            prepare_beb_l2_drop_package(
                package_dir=self.root / "packages" / "bad-canonical",
                beb_id="BEB_232",
                l2_id="L2_232",
                work_dir=self.work_dir,
                target_branch="sprint/beb-222",
                target_hash=target_hash,
                objective="bad package",
                l2_instructions="safe helper packet",
                allowed_modified_files=["src/components/CanonicalDataGrid.tsx"],
                allowed_new_files=[],
                validation_profiles=["python-unittest"],
                trace_artifacts=TRACE_ARTIFACTS,
                extra_manifest_fields={"l2_path": str(attacker_l2), "l2_sha256": self.sha(attacker_l2)},
            )

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

    def test_clean_worktree_manifest_retargets_drop_without_authorizing_dispatch_or_mutation(self):
        target_hash = self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"

        plan = build_clean_worktree_drop_manifest(
            self.drop_path,
            clean_work_dir=clean_work_dir,
            clean_worktree_roots=[clean_root],
            **self.route_kwargs(),
        )

        self.assertEqual(plan["status"], "CLEAN_WORKTREE_MANIFEST_READY")
        self.assertEqual(plan["source_work_dir"], str(self.work_dir.resolve()))
        self.assertEqual(plan["clean_work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(plan["drop_manifest"]["work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(plan["drop_manifest"]["target_hash"], target_hash)
        self.assertTrue(plan["manifest_approval_required"])
        self.assertFalse(plan["dispatch_authorized"])
        self.assertFalse(plan["source_mutation_authorized"])
        self.assertFalse(plan["worktree_creation_authorized"])

    def test_clean_worktree_manifest_rejects_unapproved_or_source_nested_destinations(self):
        self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        bad_cases = [
            (self.work_dir / "nested-clean", [self.work_dir], "must not be the source work_dir or inside it"),
            (self.root / "elsewhere" / "kuronode-clean", [clean_root], "clean_work_dir must be under a trusted root"),
        ]

        for clean_work_dir, clean_roots, pattern in bad_cases:
            with self.subTest(clean_work_dir=clean_work_dir):
                with self.assertRaisesRegex(RouteError, pattern):
                    build_clean_worktree_drop_manifest(
                        self.drop_path,
                        clean_work_dir=clean_work_dir,
                        clean_worktree_roots=clean_roots,
                        **self.route_kwargs(),
                    )

    def test_clean_worktree_manifest_can_preflight_ready_in_sterile_clone_while_source_is_blocked(self):
        self.init_git_workdir(ignored=True)
        source_report = preflight_drop_file(self.drop_path, **self.route_kwargs())
        self.assertEqual(source_report["status"], "BLOCKED")

        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"
        subprocess.run(["git", "clone", "--no-hardlinks", str(self.work_dir), str(clean_work_dir)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        plan = build_clean_worktree_drop_manifest(
            self.drop_path,
            clean_work_dir=clean_work_dir,
            clean_worktree_roots=[clean_root],
            **self.route_kwargs(),
        )
        clean_drop = self.root / "clean-drop.json"
        clean_drop.write_text(json.dumps(plan["drop_manifest"], sort_keys=True))

        report = preflight_drop_file(
            clean_drop,
            allowed_work_dirs=[clean_work_dir],
            trusted_roots=[self.root],
            approved_drop_sha256=self.sha(clean_drop),
        )

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["work_dir"], str(clean_work_dir.resolve()))
        self.assertEqual(report["blockers"], [])

    def test_clean_worktree_manifest_cli_emits_retargeted_manifest_without_dispatch(self):
        self.init_git_workdir(ignored=True)
        clean_root = self.root / "clean-worktrees"
        clean_work_dir = clean_root / "kuronode-clean"
        adapter = FakeAdapter()

        import io
        import contextlib
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = route_main([
                "--drop", str(self.drop_path),
                "--allowed-work-dir", str(self.work_dir),
                "--trusted-root", str(self.root),
                "--approved-drop-sha256", self.sha(self.drop_path),
                "--clean-worktree-manifest",
                "--clean-work-dir", str(clean_work_dir),
                "--clean-worktree-root", str(clean_root),
            ])

        report = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(report["status"], "CLEAN_WORKTREE_MANIFEST_READY")
        self.assertEqual(report["drop_manifest"]["work_dir"], str(clean_work_dir.resolve()))
        self.assertFalse(report["dispatch_authorized"])
        self.assertEqual(adapter.calls, [])

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
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args(beb_id="BEB_222", target_hash=target_hash))

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

    def test_route_rejects_protected_beb_or_l2_artifact_paths_before_reading(self):
        target_hash = self.init_git_workdir()
        adapter = FakeAdapter()
        protected_root = self.root / "docs" / "requirements" / "active"
        protected_root.mkdir(parents=True)
        protected_beb = protected_root / "REQ-001.md"
        protected_beb.write_text(self.beb_path.read_text())
        protected_l2 = protected_root / "REQ-001-L2.md"
        protected_l2.write_text(self.l2_path.read_text())

        cases = [
            ({"beb_path": str(protected_beb), "beb_sha256": self.sha(protected_beb)}, "beb_path"),
            ({"l2_path": str(protected_l2), "l2_sha256": self.sha(protected_l2)}, "l2_path"),
        ]
        for overrides, field_name in cases:
            with self.subTest(field_name=field_name):
                self.write_drop(target_hash=target_hash, **overrides)
                with self.assertRaisesRegex(RouteError, f"{field_name}.*protected BLK-req"):
                    self.process(adapter)
        self.assertEqual(adapter.calls, [])

    def test_inbox_dispatch_requires_processed_and_failed_dirs_under_trusted_roots(self):
        self.init_git_workdir()
        inbox = self.root / "inbox"
        inbox.mkdir()
        outside = self.root.parent / f"outside-route-state-{self.root.name}"
        drop = inbox / "BEB_222.drop.json"
        drop.write_text(self.drop_path.read_text())
        adapter = FakeAdapter()
        inbox_kwargs = self.route_kwargs()
        inbox_kwargs["approved_drop_sha256s"] = [inbox_kwargs.pop("approved_drop_sha256")]

        with self.assertRaisesRegex(RouteError, "processed_dir.*trusted root"):
            dispatch_inbox_once(inbox, outside / "processed", self.root / "failed", adapter=adapter, **inbox_kwargs)
        self.assertTrue(drop.exists())
        self.assertFalse((outside / "processed" / drop.name).exists())
        self.assertEqual(adapter.calls, [])

        with self.assertRaisesRegex(RouteError, "failed_dir.*trusted root"):
            dispatch_inbox_once(inbox, self.root / "processed", outside / "failed", adapter=adapter, **inbox_kwargs)
        self.assertTrue(drop.exists())
        self.assertFalse((outside / "failed" / drop.name).exists())
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

    def test_route_accepts_kuronode_worktree_static_validation_profile(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, validation_profiles=["kuronode-worktree-static"])
        adapter = FakeAdapter()

        result = self.process(adapter)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(adapter.calls[0]["validation_profiles"], ["kuronode-worktree-static"])

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
        self.assertEqual(payload["engine_args"], build_kuronode_codex_engine_args(target_hash=target_hash, beb_id="BEB_222"))
        self.assertEqual(payload["l2_packet"], self.l2_path.read_text())
        self.assertEqual(payload["trace_artifacts"], TRACE_ARTIFACTS)
        self.assertEqual(payload["target_hash"], target_hash)

        output_index = payload["engine_args"].index("--output-last-message") + 1
        final_message_artifact = Path(payload["engine_args"][output_index])
        self.assertTrue(final_message_artifact.is_absolute())
        self.assertFalse(final_message_artifact.is_relative_to(self.work_dir.resolve()))
        self.assertEqual(final_message_artifact.parent.name, target_hash[:12])
        self.assertEqual(final_message_artifact.parent.parent.name, "BEB_222")
        self.assertTrue(final_message_artifact.parent.is_dir())

    def test_route_main_progress_stderr_emits_operator_status_lines(self):
        self.init_git_workdir()
        fake_bin_dir = self.root / "bin"
        fake_bin_dir.mkdir()
        fake_blk_pipe = fake_bin_dir / "blk-pipe"
        fake_blk_pipe.write_text(
            textwrap.dedent(
                """
                #!/usr/bin/env python3
                import json

                print(json.dumps({
                    "status": "SUCCESS",
                    "commit_hash": "route-commit",
                    "validation_logs": {"go test ./...": "PASS"},
                }))
                """
            ).lstrip()
        )
        fake_blk_pipe.chmod(fake_blk_pipe.stat().st_mode | stat.S_IXUSR)

        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{fake_bin_dir}{os.pathsep}{old_path}"
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = route_main([
                    "--drop", str(self.drop_path),
                    "--allowed-work-dir", str(self.work_dir),
                    "--trusted-root", str(self.root),
                    "--approved-drop-sha256", self.sha(self.drop_path),
                    "--progress-stderr",
                ])
        finally:
            os.environ["PATH"] = old_path

        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["status"], "SUCCESS")
        status_lines = [
            line for line in stderr.getvalue().splitlines()
            if line.startswith("[BLK status]")
        ]
        self.assertTrue(any("BEB_222 started" in line for line in status_lines), status_lines)
        self.assertTrue(any("Codex started" in line for line in status_lines), status_lines)
        self.assertTrue(any("Codex completed: SUCCESS" in line for line in status_lines), status_lines)
        self.assertTrue(any("testing completed: SUCCESS" in line for line in status_lines), status_lines)
        self.assertFalse(any("blk_pipe_running" in line for line in status_lines), status_lines)

    def test_process_drop_file_rejects_symlinked_external_codex_artifact_directory(self):
        target_hash = self.init_git_workdir()
        artifact_beb_dir = Path("/tmp/blk-system-beb-l2-codex") / "BEB_222"
        shutil.rmtree(artifact_beb_dir, ignore_errors=True)
        self.addCleanup(lambda: shutil.rmtree(artifact_beb_dir, ignore_errors=True))
        artifact_beb_dir.mkdir(parents=True)
        os.symlink(self.work_dir, artifact_beb_dir / target_hash[:12])
        adapter = FakeAdapter()

        with self.assertRaisesRegex(RouteError, "Codex final-message artifact path"):
            self.process(adapter)

        self.assertEqual(adapter.calls, [])

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


    def test_preflight_reports_non_authorizing_companion_test_suggestions(self):
        self.init_git_workdir()
        companion = self.work_dir / "src" / "components" / "CanonicalDataGrid.test.tsx"
        companion.write_text("test('existing companion', () => {});\n")
        subprocess.run(["git", "add", "src/components/CanonicalDataGrid.test.tsx"], cwd=self.work_dir, check=True)
        subprocess.run(["git", "commit", "-m", "add companion test"], cwd=self.work_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.work_dir, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
        self.write_drop(target_hash=head)

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["blockers"], [])
        suggestions = report["allowlist_suggestions"]
        self.assertEqual(suggestions[0]["kind"], "existing_companion_test_not_authorized")
        self.assertEqual(suggestions[0]["source_file"], "src/components/CanonicalDataGrid.tsx")
        self.assertEqual(suggestions[0]["suggested_file"], "src/components/CanonicalDataGrid.test.tsx")
        self.assertFalse(suggestions[0]["auto_authorized"])

    def test_route_commit_message_is_beb_bound_and_newline_safe(self):
        self.assertEqual(build_route_commit_message("BEB_344"), "blk-pipe: BEB_344")
        with self.assertRaisesRegex(RouteError, "commit message"):
            build_route_commit_message("BEB_" + "X" * 200)

    def test_process_drop_file_passes_beb_bound_commit_message_to_adapter(self):
        self.init_git_workdir()
        adapter = FakeAdapter()

        self.process(adapter)

        self.assertEqual(adapter.calls[0]["commit_message"], "blk-pipe: BEB_222")

    def test_kuronode_focused_node_profile_is_allowed_by_drop_route(self):
        target_hash = self.init_git_workdir()
        self.write_drop(target_hash=target_hash, validation_profiles=["kuronode-worktree-focused-node"])

        report = preflight_drop_file(self.drop_path, **self.route_kwargs())

        self.assertEqual(report["status"], "READY")
        self.assertEqual(report["validation_profiles"], ["kuronode-worktree-focused-node"])

    def test_hostile_review_record_blocks_closeout_until_pass_and_requires_remediation_hashes(self):
        record = build_hostile_review_record(
            beb_id="BEB_349",
            parent_hash="a" * 40,
            feature_hash="b" * 40,
            verdict="BLOCKED",
            blockers=["raw provider error leaked to logs"],
            allowed_files=["packages/core/src/routes/agentAChat.ts"],
            retry_count=1,
        )

        self.assertEqual(record["state"], "HOSTILE_REVIEW_BLOCKED")
        self.assertEqual(record["next_required_state"], "REMEDIATION_PACKET_REQUIRED")
        self.assertFalse(record["closeout_ready"])
        self.assertFalse(record["remediation_auto_authorized"])
        self.assertFalse(record["beo_publication_authorized"])

        with self.assertRaisesRegex(RouteError, "remediation parent/feature hash"):
            build_hostile_review_record(
                beb_id="BEB_349",
                parent_hash="a" * 40,
                feature_hash="b" * 40,
                verdict="PASS",
                blockers=[],
                allowed_files=["packages/core/src/routes/agentAChat.ts"],
                retry_count=0,
            )

        pass_record = build_hostile_review_record(
            beb_id="BEB_349",
            parent_hash="a" * 40,
            feature_hash="b" * 40,
            verdict="PASS",
            blockers=[],
            allowed_files=["packages/core/src/routes/agentAChat.ts"],
            retry_count=2,
            remediation_parent_hash="b" * 40,
            remediation_feature_hash="c" * 40,
        )

        self.assertEqual(pass_record["state"], "HOSTILE_REVIEW_PASS")
        self.assertTrue(pass_record["closeout_ready"])
        self.assertEqual(pass_record["remediation_parent_hash"], "b" * 40)
        self.assertEqual(pass_record["remediation_feature_hash"], "c" * 40)

    def test_codex_args_are_not_caller_controlled(self):
        args = build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="high")

        self.assertEqual(args[0], "exec")
        self.assertIn("-", args)
        self.assertIn("--model", args)
        self.assertIn("gpt-5.5", args)
        self.assertIn("model_reasoning_effort=high", args)
        self.assertIn("--sandbox", args)
        self.assertEqual(args[args.index("--sandbox") + 1], "workspace-write")
        self.assertNotIn("--ask-for-approval", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertNotIn("danger-full-access", args)
        with self.assertRaisesRegex(RouteError, "model"):
            build_kuronode_codex_engine_args(model="gpt-5.4", reasoning_effort="high")
        with self.assertRaisesRegex(RouteError, "reasoning_effort"):
            build_kuronode_codex_engine_args(model="gpt-5.5", reasoning_effort="low")


if __name__ == "__main__":
    unittest.main()
