import copy
import unittest

from product_feature_loop_213_214 import DEFAULT_214_PACKAGE_HASH, DENIED_AUTHORITIES, REQUIRED_FALSE_SIDE_EFFECT_FLAGS, canonical_package_hash
from product_feature_loop_215 import (
    ALLOWED_KURONODE_FILES_215,
    DEFAULT_215_PACKAGE_HASH,
    KURONODE_CODEX_WORKER_COMMIT_215,
    KURONODE_FEATURE_MERGE_COMMIT_215,
    KURONODE_FEATURE_PATCH_HASH_215,
    KURONODE_PARENT_COMMIT_215,
    NEXT_FRONTIER_215,
    build_215_supervised_codex_feature_loop_package,
    validate_215_supervised_codex_feature_loop_package,
)


class ProductFeatureLoop215Test(unittest.TestCase):
    def test_215_records_supervised_codex_feature_loop(self):
        package = build_215_supervised_codex_feature_loop_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-215")
        self.assertEqual(package["status"], "SUPERVISED_CODEX_KURONODE_FEATURE_LOOP_EXECUTED")
        self.assertEqual(package["upstream_214_package_hash"], DEFAULT_214_PACKAGE_HASH)
        self.assertEqual(package["feature_name"], "CanonicalDataGrid projection summary badges")
        self.assertEqual(package["package_hash"], DEFAULT_215_PACKAGE_HASH)
        self.assertEqual(validate_215_supervised_codex_feature_loop_package(package), [])
        self.assertTrue(package["external_supervised_codex_worker_used"])
        self.assertEqual(package["codex_invocation"]["model"], "gpt-5.5")
        self.assertEqual(package["codex_invocation"]["reasoning_effort"], "high")

    def test_215_records_full_commits_exact_scope_and_reverse_patch_evidence(self):
        package = build_215_supervised_codex_feature_loop_package()

        for key in ("kuronode_parent_commit", "kuronode_codex_worker_commit", "kuronode_feature_merge_commit"):
            self.assertEqual(len(package[key]), 40)
        self.assertEqual(package["kuronode_parent_commit"], KURONODE_PARENT_COMMIT_215)
        self.assertEqual(package["kuronode_codex_worker_commit"], KURONODE_CODEX_WORKER_COMMIT_215)
        self.assertEqual(package["kuronode_feature_merge_commit"], KURONODE_FEATURE_MERGE_COMMIT_215)
        self.assertEqual(package["allowed_kuronode_files"], list(ALLOWED_KURONODE_FILES_215))
        self.assertEqual(package["kuronode_feature_patch_hash"], KURONODE_FEATURE_PATCH_HASH_215)
        self.assertIn("test -s /tmp/kuronode-blk215.patch", package["undo_verification_commands"])
        self.assertIn("git apply --reverse --check /tmp/kuronode-blk215.patch", package["undo_verification_commands"])
        self.assertIn(KURONODE_PARENT_COMMIT_215, package["undo_verification_commands"][0])
        self.assertIn(KURONODE_FEATURE_MERGE_COMMIT_215, package["undo_verification_commands"][0])
        self.assertIn("088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e", package["undo_verification_commands"][2])

    def test_215_preserves_denied_internal_authorities_while_recording_external_codex_use(self):
        package = build_215_supervised_codex_feature_loop_package()

        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
        self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
        self.assertTrue(package["external_supervised_codex_worker_used"])
        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertFalse(package["live_codex_dispatch_authorized"])
        self.assertFalse(package["tactical_llm_dispatch_authorized"])
        self.assertFalse(package["blanket_kuronode_mutation_authorized"])
        self.assertFalse(package["beo_closeout_execution_authorized"])

    def test_215_rejects_scope_creep_short_commits_and_rehashed_payloads(self):
        package = build_215_supervised_codex_feature_loop_package()

        scope_creep = copy.deepcopy(package)
        scope_creep["allowed_kuronode_files"].append("packages/electron/src/main/index.ts")
        scope_creep["package_hash"] = canonical_package_hash(scope_creep)
        self.assertTrue(any("allowed_kuronode_files" in error for error in validate_215_supervised_codex_feature_loop_package(scope_creep)))

        short_commit = copy.deepcopy(package)
        short_commit["kuronode_feature_merge_commit"] = short_commit["kuronode_feature_merge_commit"][:7]
        short_commit["package_hash"] = canonical_package_hash(short_commit)
        self.assertTrue(any("40-character" in error for error in validate_215_supervised_codex_feature_loop_package(short_commit)))

        forged = copy.deepcopy(package)
        forged["external_supervised_codex_worker_used"] = False
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("external_supervised_codex_worker_used" in error for error in validate_215_supervised_codex_feature_loop_package(forged)))

    def test_215_rejects_authority_laundering_in_caller_controlled_fields(self):
        package = build_215_supervised_codex_feature_loop_package()
        hostile_values = [
            {"operator_notes": ["Codex approval grants live Codex execution authorized forever"]},
            {"operator_notes": ["feature commit grants blanket Kuronode source mutation"]},
            {"caller_supplied_evidence_refs": {"protected": "docs%252Factive requirement body: The system shall..."}},
            {"caller_supplied_evidence_refs": {"tooling": "npm install && curl https://example.invalid"}},
            {"caller_supplied_evidence_refs": {"beo": "BEO publication greenlit"}},
            {"caller_supplied_evidence_refs": {"rtm": "RTM generation and coverage truth approved"}},
        ]

        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_215_supervised_codex_feature_loop_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(any("authority" in error.lower() or "protected" in error.lower() or "tool" in error.lower() for error in errors), errors)

    def test_215_selects_next_feature_loop_without_reopening_codex_dispatch_ladder(self):
        package = build_215_supervised_codex_feature_loop_package()

        self.assertEqual(package["next_frontier"], NEXT_FRONTIER_215)
        self.assertEqual(package["next_frontier"], "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED")
        self.assertIn("Second bounded Kuronode feature loop executed with external supervised Codex assistance", package["feature_loop_findings"])
        self.assertIn("does not authorize reusable BLK-System live Codex dispatch", package["feature_loop_findings"][-1])
        self.assertFalse(package["beb_dispatch_authorized"])
        self.assertFalse(package["beo_closeout_execution_authorized"])


if __name__ == "__main__":
    unittest.main()
