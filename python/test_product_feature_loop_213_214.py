import copy
import unittest

from product_feature_loop_213_214 import (
    DEFAULT_213_PACKAGE_HASH,
    DEFAULT_214_PACKAGE_HASH,
    DENIED_AUTHORITIES,
    KURONODE_FEATURE_COMMIT,
    KURONODE_FEATURE_PARENT_COMMIT,
    KURONODE_FEATURE_PATCH_HASH,
    NEXT_FRONTIER,
    REQUIRED_FALSE_SIDE_EFFECT_FLAGS,
    build_213_blk_test_optional_unblock_package,
    build_214_kuronode_feature_loop_package,
    build_product_feature_loop_packages,
    canonical_package_hash,
    validate_213_blk_test_optional_unblock_package,
    validate_214_kuronode_feature_loop_package,
)


class ProductFeatureLoop213214Test(unittest.TestCase):
    def test_213_unblocks_feature_loops_without_granting_blk_test_runtime(self):
        package = build_213_blk_test_optional_unblock_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-213")
        self.assertEqual(package["status"], "BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY")
        self.assertEqual(package["decision"], "BLK_TEST_DOES_NOT_BLOCK_FIRST_BOUNDED_KURONODE_FEATURE_LOOP")
        self.assertEqual(package["package_hash"], DEFAULT_213_PACKAGE_HASH)
        self.assertEqual(validate_213_blk_test_optional_unblock_package(package), [])
        self.assertFalse(package["production_blk_test_mcp_authorized"])
        self.assertFalse(package["blk_test_oracle_authority_authorized"])
        self.assertIn("BLK-test is optional diagnostic evidence", package["unblock_findings"])

    def test_214_records_exact_kuronode_feature_commit_and_undo_check(self):
        unblock, feature = build_product_feature_loop_packages()

        self.assertEqual(validate_213_blk_test_optional_unblock_package(unblock), [])
        self.assertEqual(feature["sprint_id"], "BLK-SYSTEM-214")
        self.assertEqual(feature["status"], "BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED")
        self.assertEqual(feature["upstream_213_package_hash"], DEFAULT_213_PACKAGE_HASH)
        self.assertEqual(feature["kuronode_repo"], "/home/dad/code/Kuronode-v1")
        self.assertEqual(feature["kuronode_parent_commit"], KURONODE_FEATURE_PARENT_COMMIT)
        self.assertEqual(feature["kuronode_feature_commit"], KURONODE_FEATURE_COMMIT)
        self.assertEqual(feature["package_hash"], DEFAULT_214_PACKAGE_HASH)
        self.assertEqual(validate_214_kuronode_feature_loop_package(feature), [])
        self.assertEqual(feature["feature_name"], "GraphProjectionEngine projection summary metrics")
        self.assertEqual(feature["allowed_kuronode_files"], [
            "packages/kuronode-graph/src/utils/GraphProjectionEngine.ts",
            "packages/kuronode-graph/tests/GraphProjectionEngine.test.ts",
        ])
        self.assertEqual(feature["kuronode_feature_patch_hash"], KURONODE_FEATURE_PATCH_HASH)
        self.assertIn("test -s /tmp/kuronode-blk214.patch", feature["undo_verification_commands"])
        self.assertIn("git apply --reverse --check /tmp/kuronode-blk214.patch", feature["undo_verification_commands"])
        self.assertIn(KURONODE_FEATURE_PARENT_COMMIT, feature["undo_verification_commands"][0])
        self.assertIn(KURONODE_FEATURE_COMMIT, feature["undo_verification_commands"][0])
        self.assertIn("8a42772e1cbb54df6c94b4d162a3f8e9ba6b3179d758d19cb99ec0b2ff4be061", feature["undo_verification_commands"][2])
        self.assertTrue(feature["exact_kuronode_feature_commit_recorded"])
        self.assertFalse(feature["blanket_kuronode_mutation_authorized"])

    def test_every_package_preserves_denied_authorities_and_false_flags(self):
        for package in build_product_feature_loop_packages():
            with self.subTest(sprint_id=package["sprint_id"]):
                self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
                self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
                for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
                    self.assertIs(package[flag], False, flag)

        candidate = build_213_blk_test_optional_unblock_package()
        candidate["denied_authorities"] = candidate["denied_authorities"][:-1]
        candidate["package_hash"] = canonical_package_hash(candidate)
        self.assertTrue(any("denied_authorities" in error for error in validate_213_blk_test_optional_unblock_package(candidate)))

        positive_flag = build_214_kuronode_feature_loop_package(build_213_blk_test_optional_unblock_package())
        positive_flag["production_blk_test_mcp_authorized"] = True
        positive_flag["package_hash"] = canonical_package_hash(positive_flag)
        self.assertTrue(any("production_blk_test_mcp_authorized" in error for error in validate_214_kuronode_feature_loop_package(positive_flag)))

    def test_214_rejects_rehashed_213_and_scope_creep(self):
        unblock = build_213_blk_test_optional_unblock_package()
        forged = copy.deepcopy(unblock)
        forged["decision"] = "BLK-test approval grants production MCP runtime"
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertNotEqual(forged["package_hash"], DEFAULT_213_PACKAGE_HASH)
        self.assertTrue(validate_213_blk_test_optional_unblock_package(forged))
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-213"):
            build_214_kuronode_feature_loop_package(forged)

        feature = build_214_kuronode_feature_loop_package(unblock)
        feature["allowed_kuronode_files"].append("packages/electron/src/main/index.ts")
        feature["package_hash"] = canonical_package_hash(feature)
        self.assertTrue(any("allowed_kuronode_files" in error for error in validate_214_kuronode_feature_loop_package(feature)))

    def test_feature_loop_rejects_authority_laundering_in_notes_and_evidence(self):
        feature = build_214_kuronode_feature_loop_package(build_213_blk_test_optional_unblock_package())
        hostile_values = [
            {"operator_notes": ["BLK-test PASS approves production MCP runtime"]},
            {"operator_notes": ["feature commit grants blanket Kuronode source mutation"]},
            {"caller_supplied_evidence_refs": {"codex": "live Codex execution authorized"}},
            {"caller_supplied_evidence_refs": {"protected": "docs%252Factive requirement body: The system shall..."}},
            {"caller_supplied_evidence_refs": {"tooling": "npm install && curl https://example.invalid"}},
            {"caller_supplied_evidence_refs": {"beo": "BEO publication greenlit"}},
        ]
        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(feature)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_214_kuronode_feature_loop_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(any("authority" in error.lower() or "protected" in error.lower() or "tool" in error.lower() for error in errors), errors)

    def test_214_selects_next_feature_loop_without_reopening_closure_treadmill(self):
        _unblock, feature = build_product_feature_loop_packages()

        self.assertEqual(feature["next_frontier"], NEXT_FRONTIER)
        self.assertEqual(feature["next_frontier"], "NEXT_FRONTIER_SECOND_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED")
        self.assertIn("First bounded Kuronode feature loop executed", feature["feature_loop_findings"])
        self.assertIn("Undo/reverse-patch check passed without undoing committed work", feature["feature_loop_findings"])
        self.assertFalse(feature["beb_dispatch_authorized"])
        self.assertFalse(feature["beo_closeout_execution_authorized"])


if __name__ == "__main__":
    unittest.main()
