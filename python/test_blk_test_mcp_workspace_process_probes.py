import tempfile
import unittest
from pathlib import Path

import blk_test_mcp_workspace_process_probes as probes
from blk_test_mcp_workspace_process_probes import (
    build_run_cache_paths,
    build_workspace_process_boundary_descriptor,
    decide_clone_strategy,
    validate_workspace_relative_path,
)


_INERT_MARKER_NAME = ".blk-system-012-inert-fixture"
_OWNED_MARKER_NAME = ".blk-system-012-owned"
_OWNED_MARKER_TEXT = "BLK-SYSTEM-012-owned\n"
_TERMINAL_STATUSES = (
    "PASS",
    "FAIL",
    "BLOCKED",
    "FATAL_TIMEOUT",
    "FATAL_OUTPUT_FLOOD",
    "TRANSPORT_ERROR",
    "OPERATOR_INTERRUPTED",
)


def _create_inert_fixture(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / _INERT_MARKER_NAME).write_text("synthetic Sprint 012 fixture\n")
    (root / "src").mkdir()
    (root / "src" / "model.sysml").write_text("part def SyntheticProbe;\n")
    (root / "README.md").write_text("# inert fixture\n")
    return root


def _mark_owned(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / _OWNED_MARKER_NAME).write_text(_OWNED_MARKER_TEXT)
    return path


def _write_owned_lock(lock_path: Path, *, pid: int) -> Path:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(f"{_OWNED_MARKER_TEXT}pid={pid}\n")
    return lock_path


class WorkspaceProcessBoundaryDescriptorTest(unittest.TestCase):
    def test_descriptor_returns_required_non_authority_fields(self):
        descriptor = build_workspace_process_boundary_descriptor()

        expected = {
            "sprint": "BLK-SYSTEM-012",
            "authority": "PROBE_ONLY",
            "fixture_scope": "INERT_LOCAL_FIXTURES_ONLY",
            "live_mcp_authorized": False,
            "mcp_server_started": False,
            "mcp_client_started": False,
            "fixed_tool_tests_executed": [],
            "primary_repo_mutation_allowed": False,
            "source_staging_allowed": False,
            "source_commit_allowed": False,
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read_allowed": False,
            "production_sandbox_claimed": False,
        }
        for key, value in expected.items():
            self.assertEqual(descriptor[key], value, key)


class CloneStrategyDecisionTest(unittest.TestCase):
    def test_same_device_source_and_scratch_selects_hardlink_clone(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            scratch_root = Path(tmp) / "scratch"
            source_root.mkdir()
            scratch_root.mkdir()

            decision = decide_clone_strategy(
                source_root,
                scratch_root,
                source_device=42,
                scratch_device=42,
            )

        self.assertEqual(decision["status"], "HARDLINK_CLONE_SELECTED")
        self.assertTrue(decision["clone_allowed"])
        self.assertTrue(decision["same_filesystem"])
        self.assertFalse(decision["fallback_used"])
        self.assertEqual(decision["workspace_parent"], str(scratch_root.resolve()))
        self.assertFalse(decision["hardlinks_are_write_isolation"])
        self.assertFalse(decision["primary_repo_mutation_allowed"])

    def test_different_device_without_fallback_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            scratch_root = Path(tmp) / "scratch"
            source_root.mkdir()
            scratch_root.mkdir()

            decision = decide_clone_strategy(
                source_root,
                scratch_root,
                source_device=1,
                scratch_device=2,
            )

        self.assertEqual(decision["status"], "CLONE_BLOCKED_DIFFERENT_FILESYSTEM")
        self.assertFalse(decision["clone_allowed"])
        self.assertFalse(decision["same_filesystem"])
        self.assertFalse(decision["fallback_used"])
        self.assertIsNone(decision["workspace_parent"])
        self.assertIn("different filesystem", decision["reason"])

    def test_explicit_same_device_fallback_is_selected_only_when_provided(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            scratch_root = Path(tmp) / "scratch"
            fallback_root = Path(tmp) / "fallback"
            source_root.mkdir()
            scratch_root.mkdir()
            fallback_root.mkdir()

            no_fallback = decide_clone_strategy(
                source_root,
                scratch_root,
                source_device=7,
                scratch_device=8,
            )
            same_device_fallback = decide_clone_strategy(
                source_root,
                scratch_root,
                fallback_root=fallback_root,
                source_device=7,
                scratch_device=8,
                fallback_device=7,
            )
            different_device_fallback = decide_clone_strategy(
                source_root,
                scratch_root,
                fallback_root=fallback_root,
                source_device=7,
                scratch_device=8,
                fallback_device=9,
            )

        self.assertEqual(no_fallback["status"], "CLONE_BLOCKED_DIFFERENT_FILESYSTEM")
        self.assertFalse(no_fallback["clone_allowed"])
        self.assertEqual(
            same_device_fallback["status"],
            "SAME_FILESYSTEM_FALLBACK_SELECTED",
        )
        self.assertTrue(same_device_fallback["clone_allowed"])
        self.assertTrue(same_device_fallback["fallback_used"])
        self.assertEqual(
            same_device_fallback["workspace_parent"],
            str(fallback_root.resolve()),
        )
        self.assertEqual(
            different_device_fallback["status"],
            "CLONE_BLOCKED_DIFFERENT_FILESYSTEM",
        )
        self.assertFalse(different_device_fallback["clone_allowed"])


class WorkspacePathGuardTest(unittest.TestCase):
    def test_absolute_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            workspace_root.mkdir()
            absolute_candidate = workspace_root / "safe.txt"

            decision = validate_workspace_relative_path(workspace_root, absolute_candidate)

        self.assertEqual(decision["status"], "PATH_REJECTED_ABSOLUTE")
        self.assertFalse(decision["path_accepted"])

    def test_parent_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            workspace_root.mkdir()

            decision = validate_workspace_relative_path(workspace_root, "safe/../file.txt")

        self.assertEqual(decision["status"], "PATH_REJECTED_TRAVERSAL")
        self.assertFalse(decision["path_accepted"])

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace_root = root / "workspace"
            outside_root = root / "outside"
            workspace_root.mkdir()
            outside_root.mkdir()
            (outside_root / "secret.txt").write_text("secret")
            (workspace_root / "escape").symlink_to(outside_root, target_is_directory=True)

            decision = validate_workspace_relative_path(
                workspace_root,
                "escape/secret.txt",
            )

        self.assertEqual(decision["status"], "PATH_REJECTED_SYMLINK_ESCAPE")
        self.assertFalse(decision["path_accepted"])

    def test_symlink_alias_to_protected_vault_is_rejected_without_reads(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            protected_root = workspace_root / "docs" / "active"
            protected_root.mkdir(parents=True)
            (workspace_root / "alias").symlink_to(
                protected_root,
                target_is_directory=True,
            )

            decision = validate_workspace_relative_path(
                workspace_root,
                "alias/REQ-001.md",
            )

        self.assertEqual(decision["status"], "PATH_REJECTED_PROTECTED_VAULT")
        self.assertFalse(decision["path_accepted"])
        self.assertFalse(decision["active_vault_read_allowed"])

    def test_protected_vault_prefixes_are_rejected_without_reads(self):
        candidates = [
            "docs/active/REQ-001.md",
            "docs/requirements/REQ-001.md",
            "docs/use_cases/UC-001.md",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            workspace_root.mkdir()

            decisions = [
                validate_workspace_relative_path(workspace_root, candidate)
                for candidate in candidates
            ]

        self.assertEqual(
            [decision["status"] for decision in decisions],
            ["PATH_REJECTED_PROTECTED_VAULT"] * len(candidates),
        )
        self.assertTrue(all(not decision["path_accepted"] for decision in decisions))
        self.assertTrue(
            all(not decision["active_vault_read_allowed"] for decision in decisions)
        )

    def test_safe_relative_path_is_accepted_inside_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace_root = Path(tmp) / "workspace"
            workspace_root.mkdir()
            (workspace_root / "src").mkdir()

            decision = validate_workspace_relative_path(workspace_root, "src/model.sysml")

        self.assertEqual(decision["status"], "PATH_ACCEPTED")
        self.assertTrue(decision["path_accepted"])
        self.assertEqual(decision["relative_path"], "src/model.sysml")
        self.assertTrue(decision["resolved_path"].endswith("src/model.sysml"))
        self.assertFalse(decision["active_vault_read_allowed"])


class CachePathSelectionTest(unittest.TestCase):
    def test_cache_paths_are_run_scoped_under_scratch_and_outside_source_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch_root = Path(tmp) / "scratch"
            scratch_root.mkdir()

            decision = build_run_cache_paths(scratch_root, run_id="run-001")

        scratch_resolved = scratch_root.resolve()
        cache_root = Path(decision["cache_root"])
        tool_cache = Path(decision["tool_cache"])
        output_cache = Path(decision["output_cache"])

        self.assertEqual(decision["status"], "CACHE_JAIL_SELECTED")
        self.assertEqual(decision["run_id"], "run-001")
        self.assertTrue(cache_root.is_relative_to(scratch_resolved))
        self.assertTrue(tool_cache.is_relative_to(cache_root))
        self.assertTrue(output_cache.is_relative_to(cache_root))
        self.assertFalse(decision["inside_source_root"])
        self.assertFalse(decision["inside_workspace_root"])


class InertFixtureSourceGuardTest(unittest.TestCase):
    def test_unmarked_roots_reject_without_primary_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(tmp) / "source"
            source_root.mkdir()

            decision = probes.assert_inert_fixture_source(source_root)

        self.assertEqual(decision["status"], "INERT_FIXTURE_REJECTED_MISSING_MARKER")
        self.assertFalse(decision["source_accepted"])
        self.assertFalse(decision["primary_repo_mutation_allowed"])
        self.assertFalse(decision["source_staging_allowed"])
        self.assertFalse(decision["source_commit_allowed"])

    def test_roots_containing_git_reject_even_with_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = _create_inert_fixture(Path(tmp) / "source")
            (source_root / ".git").mkdir()

            decision = probes.assert_inert_fixture_source(source_root)

        self.assertEqual(decision["status"], "INERT_FIXTURE_REJECTED_GIT_DIRECTORY")
        self.assertFalse(decision["source_accepted"])
        self.assertEqual(decision["git_path"], str((source_root / ".git").resolve()))

    def test_real_blk_system_repo_path_rejects_as_reserved_root(self):
        repo_root = Path(__file__).resolve().parents[1]

        decision = probes.assert_inert_fixture_source(repo_root)

        self.assertEqual(decision["status"], "INERT_FIXTURE_REJECTED_RESERVED_ROOT")
        self.assertFalse(decision["source_accepted"])
        self.assertEqual(decision["reserved_root"], str(repo_root.resolve()))

    def test_marker_protected_temp_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = _create_inert_fixture(Path(tmp) / "source")

            decision = probes.assert_inert_fixture_source(source_root)

        self.assertEqual(decision["status"], "INERT_FIXTURE_SOURCE_ACCEPTED")
        self.assertTrue(decision["source_accepted"])
        self.assertEqual(decision["marker_name"], _INERT_MARKER_NAME)
        self.assertEqual(decision["source_root"], str(source_root.resolve()))
        self.assertEqual(decision["authority"], "PROBE_ONLY")
        self.assertFalse(decision["primary_repo_mutation_allowed"])

    def test_symlink_escape_inside_marked_fixture_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            source_root = _create_inert_fixture(temp_root / "source")
            outside_root = temp_root / "outside"
            outside_root.mkdir()
            (outside_root / "outside.txt").write_text("outside\n")
            (source_root / "escape").symlink_to(outside_root, target_is_directory=True)
            expected_escape_path = outside_root.resolve()
            expected_symlink_path = source_root / "escape"

            decision = probes.assert_inert_fixture_source(source_root)

        self.assertEqual(decision["status"], "INERT_FIXTURE_REJECTED_SYMLINK_ESCAPE")
        self.assertFalse(decision["source_accepted"])
        self.assertEqual(decision["symlink_path"], str(expected_symlink_path))
        self.assertEqual(decision["escape_path"], str(expected_escape_path))


class InertWorkspaceFixtureLifecycleTest(unittest.TestCase):
    def test_workspace_fixture_is_created_only_under_scratch_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            source_root = _create_inert_fixture(temp_root / "source")
            scratch_root = temp_root / "scratch"
            scratch_root.mkdir()

            decision = probes.create_inert_workspace_fixture(
                source_root,
                scratch_root,
                run_id="run-001",
            )

            workspace_path = Path(decision["workspace_path"])

            self.assertEqual(decision["status"], "WORKSPACE_FIXTURE_CREATED")
            self.assertTrue(decision["workspace_created"])
            self.assertTrue(workspace_path.is_relative_to(scratch_root.resolve()))
            self.assertFalse(workspace_path.is_relative_to(source_root.resolve()))
            self.assertEqual(
                workspace_path,
                scratch_root.resolve()
                / ".blk-system-012-workspaces"
                / "run-001"
                / "workspace",
            )
            self.assertTrue((workspace_path / "src" / "model.sysml").exists())
            self.assertTrue(
                (workspace_path.parent / _OWNED_MARKER_NAME).read_text().startswith(
                    "BLK-SYSTEM-012-owned"
                )
            )

    def test_source_manifest_is_unchanged_after_clone_and_teardown(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            source_root = _create_inert_fixture(temp_root / "source")
            scratch_root = temp_root / "scratch"
            scratch_root.mkdir()
            original_manifest = probes.manifest_source_tree(source_root)

            created = probes.create_inert_workspace_fixture(
                source_root,
                scratch_root,
                run_id="run-002",
            )
            cache_paths = build_run_cache_paths(scratch_root, run_id="run-002")
            cache_root = _mark_owned(Path(cache_paths["cache_root"]))
            (cache_root / "tool-cache").mkdir()
            (cache_root / "output-cache").mkdir()
            lock_path = _write_owned_lock(
                scratch_root / ".blk-system-012-locks" / "run-002.lock",
                pid=12345,
            )

            teardown = probes.teardown_run_paths(
                workspace_path=created["workspace_path"],
                cache_paths=cache_paths,
                lock_path=lock_path,
                status="PASS",
            )
            verification = probes.verify_primary_repo_manifest(source_root, original_manifest)

            self.assertEqual(teardown["status"], "TEARDOWN_COMPLETED")
            self.assertFalse(Path(created["workspace_path"]).exists())
            self.assertFalse(cache_root.exists())
            self.assertFalse(lock_path.exists())
            self.assertEqual(verification["status"], "PRIMARY_MANIFEST_UNCHANGED")
            self.assertTrue(verification["manifest_match"])
            self.assertEqual(original_manifest["files"], verification["current_manifest"]["files"])


class StartupPurgeOwnedStalePathsTest(unittest.TestCase):
    def test_startup_purge_removes_only_owned_stale_sprint_012_prefix_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch_root = Path(tmp) / "scratch"
            scratch_root.mkdir()
            stale_workspace = _mark_owned(
                scratch_root / ".blk-system-012-workspaces" / "stale-run"
            )
            (stale_workspace / "workspace").mkdir()
            (stale_workspace / "workspace" / "probe.txt").write_text("stale\n")
            stale_cache = _mark_owned(scratch_root / ".blk-system-012-cache" / "stale-run")
            (stale_cache / "tool-cache").mkdir()
            unmarked_sprint_path = scratch_root / ".blk-system-012-workspaces" / "unmarked"
            unmarked_sprint_path.mkdir(parents=True)
            (unmarked_sprint_path / "keep.txt").write_text("keep\n")
            unrelated_path = scratch_root / "unrelated-temp"
            unrelated_path.mkdir()
            (unrelated_path / "keep.txt").write_text("keep\n")

            decision = probes.startup_purge_owned_stale_paths(
                scratch_root,
                pid_alive=lambda pid: False,
            )

            removed = set(decision["removed_paths"])
            self.assertEqual(decision["status"], "STARTUP_PURGE_COMPLETED")
            self.assertIn(str(stale_workspace.resolve()), removed)
            self.assertIn(str(stale_cache.resolve()), removed)
            self.assertFalse(stale_workspace.exists())
            self.assertFalse(stale_cache.exists())
            self.assertTrue(unmarked_sprint_path.exists())
            self.assertTrue(unrelated_path.exists())
            self.assertFalse(decision["primary_repo_mutation_allowed"])

    def test_live_pid_locks_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch_root = Path(tmp) / "scratch"
            scratch_root.mkdir()
            lock_path = _write_owned_lock(
                scratch_root / ".blk-system-012-locks" / "live.lock",
                pid=4242,
            )

            decision = probes.startup_purge_owned_stale_paths(
                scratch_root,
                pid_alive=lambda pid: pid == 4242,
            )

            self.assertEqual(decision["status"], "STARTUP_PURGE_COMPLETED")
            self.assertTrue(lock_path.exists())
            self.assertIn(str(lock_path.resolve()), decision["preserved_paths"])
            self.assertNotIn(str(lock_path.resolve()), decision["removed_paths"])

    def test_dead_pid_locks_are_removed_only_under_owned_scratch_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            scratch_root = temp_root / "scratch"
            outside_root = temp_root / "outside"
            scratch_root.mkdir()
            outside_root.mkdir()
            scratch_lock = _write_owned_lock(
                scratch_root / ".blk-system-012-locks" / "dead.lock",
                pid=5151,
            )
            outside_lock = _write_owned_lock(
                outside_root / ".blk-system-012-locks" / "dead.lock",
                pid=5151,
            )

            decision = probes.startup_purge_owned_stale_paths(
                scratch_root,
                pid_alive=lambda pid: False,
            )

            self.assertEqual(decision["status"], "STARTUP_PURGE_COMPLETED")
            self.assertFalse(scratch_lock.exists())
            self.assertTrue(outside_lock.exists())
            self.assertIn(str(scratch_lock.resolve()), decision["removed_paths"])
            self.assertNotIn(str(outside_lock.resolve()), decision["removed_paths"])


class TeardownRunPathsTest(unittest.TestCase):
    def test_teardown_removes_workspace_cache_and_lock_for_terminal_statuses(self):
        for status in _TERMINAL_STATUSES:
            with self.subTest(status=status):
                with tempfile.TemporaryDirectory() as tmp:
                    scratch_root = Path(tmp) / "scratch"
                    scratch_root.mkdir()
                    run_id = status.lower().replace("_", "-")
                    run_root = _mark_owned(
                        scratch_root / ".blk-system-012-workspaces" / run_id
                    )
                    workspace_path = _mark_owned(run_root / "workspace")
                    (workspace_path / "probe.txt").write_text("workspace\n")
                    cache_root = _mark_owned(scratch_root / ".blk-system-012-cache" / run_id)
                    tool_cache = cache_root / "tool-cache"
                    output_cache = cache_root / "output-cache"
                    tool_cache.mkdir()
                    output_cache.mkdir()
                    (tool_cache / "tool.txt").write_text("tool\n")
                    (output_cache / "output.txt").write_text("output\n")
                    lock_path = _write_owned_lock(
                        scratch_root / ".blk-system-012-locks" / f"{run_id}.lock",
                        pid=6161,
                    )
                    cache_paths = {
                        "cache_root": str(cache_root),
                        "tool_cache": str(tool_cache),
                        "output_cache": str(output_cache),
                    }

                    decision = probes.teardown_run_paths(
                        workspace_path=workspace_path,
                        cache_paths=cache_paths,
                        lock_path=lock_path,
                        status=status,
                    )

                    self.assertEqual(decision["status"], "TEARDOWN_COMPLETED")
                    self.assertEqual(decision["terminal_status"], status)
                    self.assertTrue(decision["cleanup_allowed"])
                    self.assertFalse(workspace_path.exists())
                    self.assertFalse(cache_root.exists())
                    self.assertFalse(lock_path.exists())
                    self.assertIn(str(workspace_path.resolve()), decision["removed_paths"])
                    self.assertIn(str(cache_root.resolve()), decision["removed_paths"])
                    self.assertIn(str(lock_path.resolve()), decision["removed_paths"])
