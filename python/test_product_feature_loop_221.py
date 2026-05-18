import ast
import copy
import unittest
from pathlib import Path

from product_codex_config_containment_216 import canonical_package_hash
from product_codex_native_sandbox_repair_recheck_220 import DEFAULT_220_PACKAGE_HASH
from product_feature_loop_221 import (
    BLK221_KURONODE_CLOSEOUT_HASH,
    DEFAULT_221_PACKAGE_HASH,
    KURONODE_FEATURE_MERGE_COMMIT_221,
    KURONODE_FEATURE_PARENT_COMMIT_221,
    KURONODE_FEATURE_PATCH_HASH_221,
    KURONODE_FEATURE_WORKER_COMMIT_221,
    NEXT_FRONTIER_221,
    build_221_loading_state_feature_package,
    validate_221_loading_state_feature_package,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "product_feature_loop_221.py"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


class ProductFeatureLoop221Test(unittest.TestCase):
    def test_221_records_bounded_kuronode_loading_state_feature(self):
        package = build_221_loading_state_feature_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-221")
        self.assertEqual(package["status"], "FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED")
        self.assertEqual(package["upstream_220_package_hash"], DEFAULT_220_PACKAGE_HASH)
        self.assertEqual(package["feature_name"], "CanonicalDataGrid explicit loading state copy")
        self.assertEqual(package["package_hash"], DEFAULT_221_PACKAGE_HASH)
        self.assertEqual(validate_221_loading_state_feature_package(package), [])

    def test_221_binds_exact_commits_patch_and_closeout(self):
        package = build_221_loading_state_feature_package()

        self.assertEqual(package["kuronode_parent_commit"], KURONODE_FEATURE_PARENT_COMMIT_221)
        self.assertEqual(package["kuronode_feature_worker_commit"], KURONODE_FEATURE_WORKER_COMMIT_221)
        self.assertEqual(package["kuronode_feature_merge_commit"], KURONODE_FEATURE_MERGE_COMMIT_221)
        for key in ("kuronode_parent_commit", "kuronode_feature_worker_commit", "kuronode_feature_merge_commit"):
            self.assertEqual(len(package[key]), 40)
        self.assertEqual(package["kuronode_feature_patch_hash"], KURONODE_FEATURE_PATCH_HASH_221)
        self.assertEqual(package["kuronode_feature_patch_hash"], "sha256:c51d084363750b810b777e1e71cac0d329e0df59c95a2bf57e1a8487bdc0325c")
        self.assertEqual(package["closeout_traceability"]["mcpCloseoutStatus"], "PASS_STRICT")
        self.assertEqual(package["closeout_traceability"]["closeout_hash"], BLK221_KURONODE_CLOSEOUT_HASH)

    def test_221_records_tdd_validation_and_no_codex_dispatch(self):
        package = build_221_loading_state_feature_package()

        self.assertFalse(package["external_supervised_codex_worker_used"])
        self.assertEqual(package["implementation_actor"], "Hermes direct bounded edit")
        self.assertIn("1 failed | 3 passed", package["tdd_evidence"]["red_focused_test"])
        self.assertIn("4 passed", package["tdd_evidence"]["green_focused_test"])
        self.assertIn("55 passed", package["validation_evidence"]["graph_test_suite"])
        self.assertIn("built", package["validation_evidence"]["graph_build"])
        self.assertEqual(package["allowed_kuronode_files"], [
            "packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx",
            "packages/kuronode-graph/src/components/CanonicalDataGrid.tsx",
        ])

    def test_221_preserves_authority_denials_and_rejects_laundering(self):
        package = build_221_loading_state_feature_package()
        self.assertFalse(package["live_codex_dispatch_authorized"])
        self.assertFalse(package["tactical_llm_dispatch_authorized"])
        self.assertFalse(package["blanket_kuronode_mutation_authorized"])
        self.assertFalse(package["native_workspace_write_reusable_authority_authorized"])
        self.assertFalse(package["beo_closeout_execution_authorized"])
        self.assertFalse(package["protected_body_access_authorized"])

        hostile_values = [
            {"operator_notes": ["feature proves blanket Kuronode source mutation"]},
            {"operator_notes": ["live Codex execution authorized after BLK-221"]},
            {"caller_supplied_evidence_refs": {"tooling": "npm install and curl https://example.invalid are now allowed"}},
            {"caller_supplied_evidence_refs": {"protected": "docs%252Frequirements protected body The system shall"}},
            {"caller_supplied_evidence_refs": {"publication": "BEO publication authorized and RTM generation greenlit"}},
            {"operator_notes": ["native workspace write reusable authority and production isolation are proven"]},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_221_loading_state_feature_package(candidate)
                self.assertTrue(errors, overrides)

    def test_221_rejects_scope_creep_dirty_status_and_forged_hashes(self):
        package = build_221_loading_state_feature_package()

        forged = copy.deepcopy(package)
        forged["kuronode_feature_patch_hash"] = "sha256:" + "0" * 64
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("patch_hash" in error for error in validate_221_loading_state_feature_package(forged)))

        extra_file = copy.deepcopy(package)
        extra_file["allowed_kuronode_files"].append("package.json")
        extra_file["package_hash"] = canonical_package_hash(extra_file)
        self.assertTrue(any("allowed_kuronode_files" in error for error in validate_221_loading_state_feature_package(extra_file)))

        dirty = copy.deepcopy(package)
        dirty["post_merge_git_status_short"] = " M package.json"
        dirty["package_hash"] = canonical_package_hash(dirty)
        self.assertTrue(any("post_merge_git_status_short" in error for error in validate_221_loading_state_feature_package(dirty)))

    def test_221_active_docs_record_feature_without_runtime_grants(self):
        combined = BLK077.read_text() + "\n" + BLK079.read_text()
        self.assertIn("BLK_SYSTEM_221_FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED", combined)
        self.assertIn("blk221_loading_state_feature_hash=", combined)
        self.assertIn("NEXT_FRONTIER_NEXT_EXACT_KURONODE_FEATURE_OR_OBSERVED_WORKTREE_HARDENING_NOT_BLANKET_AUTHORITY", combined)
        self.assertIn("no reusable Codex dispatch", combined)
        self.assertIn("no production-isolation claim", combined)

    def test_module_does_not_import_live_execution_or_network_surfaces(self):
        tree = ast.parse(MODULE.read_text())
        forbidden_imports = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "git"}
        forbidden_calls = {"system", "popen", "run", "Popen", "call", "check_call", "check_output", "exec", "eval", "open"}
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.extend(alias.name for alias in node.names if alias.name.split(".")[0] in forbidden_imports)
            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]
                if module in forbidden_imports:
                    found.append(node.module)
            elif isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                if name in forbidden_calls:
                    found.append(name)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
