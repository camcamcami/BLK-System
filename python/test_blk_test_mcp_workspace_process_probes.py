import tempfile
import unittest
from pathlib import Path

from blk_test_mcp_workspace_process_probes import (
    build_run_cache_paths,
    build_workspace_process_boundary_descriptor,
    decide_clone_strategy,
    validate_workspace_relative_path,
)


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
