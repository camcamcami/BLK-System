import copy
import unittest

from product_codex_config_containment_216 import DENIED_AUTHORITIES, REQUIRED_FALSE_SIDE_EFFECT_FLAGS, canonical_package_hash
from product_feature_loop_217 import DEFAULT_217_PACKAGE_HASH
from product_feature_loop_218 import (
    BLK218_CODEX_EVENTS_HASH,
    BLK218_CODEX_FINAL_MESSAGE_HASH,
    BLK218_CODEX_PROMPT_HASH,
    BLK218_KURONODE_CLOSEOUT_HASH,
    DEFAULT_218_PACKAGE_HASH,
    KURONODE_FEATURE_MERGE_COMMIT_218,
    KURONODE_FEATURE_PARENT_COMMIT_218,
    KURONODE_FEATURE_PATCH_HASH_218,
    KURONODE_FEATURE_WORKER_COMMIT_218,
    NEXT_FRONTIER_218,
    build_218_selected_requirement_badge_feature_package,
    validate_218_selected_requirement_badge_feature_package,
)


class ProductFeatureLoop218Test(unittest.TestCase):
    def test_218_records_third_bounded_kuronode_feature_loop(self):
        package = build_218_selected_requirement_badge_feature_package()

        self.assertEqual(package["sprint_id"], "BLK-SYSTEM-218")
        self.assertEqual(package["status"], "THIRD_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED")
        self.assertEqual(package["upstream_217_package_hash"], DEFAULT_217_PACKAGE_HASH)
        self.assertEqual(package["feature_name"], "CanonicalDataGrid selected requirement header badge")
        self.assertEqual(package["package_hash"], DEFAULT_218_PACKAGE_HASH)
        self.assertEqual(validate_218_selected_requirement_badge_feature_package(package), [])

    def test_218_binds_exact_kuronode_commits_patch_and_closeout(self):
        package = build_218_selected_requirement_badge_feature_package()

        self.assertEqual(package["kuronode_parent_commit"], KURONODE_FEATURE_PARENT_COMMIT_218)
        self.assertEqual(package["kuronode_feature_worker_commit"], KURONODE_FEATURE_WORKER_COMMIT_218)
        self.assertEqual(package["kuronode_feature_merge_commit"], KURONODE_FEATURE_MERGE_COMMIT_218)
        self.assertEqual(len(package["kuronode_parent_commit"]), 40)
        self.assertEqual(len(package["kuronode_feature_worker_commit"]), 40)
        self.assertEqual(len(package["kuronode_feature_merge_commit"]), 40)
        self.assertEqual(package["kuronode_feature_patch_hash"], KURONODE_FEATURE_PATCH_HASH_218)
        self.assertEqual(package["kuronode_feature_patch_hash"], "sha256:e05df098cc5cc331966d07cda102689f3cd3388c949c23b6076dd348faae3533")
        self.assertEqual(package["closeout_traceability"]["mcpCloseoutStatus"], "PASS_STRICT")
        self.assertEqual(package["closeout_traceability"]["closeout_hash"], BLK218_KURONODE_CLOSEOUT_HASH)

    def test_218_records_tdd_codex_invocation_and_validation(self):
        package = build_218_selected_requirement_badge_feature_package()

        self.assertTrue(package["external_supervised_codex_worker_used"])
        self.assertEqual(package["codex_invocation"]["model"], "gpt-5.5")
        self.assertEqual(package["codex_invocation"]["reasoning_effort"], "high")
        self.assertTrue(package["codex_invocation"]["ephemeral"])
        self.assertEqual(package["codex_telemetry"]["events_jsonl_sha256"], BLK218_CODEX_EVENTS_HASH)
        self.assertEqual(package["codex_telemetry"]["final_message_sha256"], BLK218_CODEX_FINAL_MESSAGE_HASH)
        self.assertEqual(package["codex_telemetry"]["prompt_sha256"], BLK218_CODEX_PROMPT_HASH)
        self.assertEqual(package["codex_telemetry"]["events_jsonl_line_count"], 43)
        self.assertFalse(package["codex_telemetry"]["authoritative_evidence"])
        self.assertIn("RED", package["tdd_evidence"]["red_focused_test"])
        self.assertIn("3 passed", package["tdd_evidence"]["green_focused_test"])
        self.assertIn("54 passed", package["validation_evidence"]["graph_test_suite"])

    def test_218_denies_adjacent_authority_and_broad_mutation(self):
        package = build_218_selected_requirement_badge_feature_package()

        self.assertEqual(package["denied_authorities"], list(DENIED_AUTHORITIES))
        self.assertEqual(len(package["denied_authorities"]), len(set(package["denied_authorities"])))
        for flag in REQUIRED_FALSE_SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertTrue(package["exact_kuronode_feature_commit_recorded"])
        self.assertFalse(package["live_codex_dispatch_authorized"])
        self.assertFalse(package["tactical_llm_dispatch_authorized"])
        self.assertFalse(package["blanket_kuronode_mutation_authorized"])
        self.assertFalse(package["beo_closeout_execution_authorized"])
        self.assertFalse(package["protected_body_access_authorized"])

    def test_218_rejects_forged_hashes_scope_creep_and_dirty_status(self):
        package = build_218_selected_requirement_badge_feature_package()

        forged = copy.deepcopy(package)
        forged["kuronode_feature_patch_hash"] = "sha256:" + "0" * 64
        forged["package_hash"] = canonical_package_hash(forged)
        self.assertTrue(any("kuronode_feature_patch_hash" in error for error in validate_218_selected_requirement_badge_feature_package(forged)))

        extra_file = copy.deepcopy(package)
        extra_file["allowed_kuronode_files"].append("package.json")
        extra_file["package_hash"] = canonical_package_hash(extra_file)
        self.assertTrue(any("allowed_kuronode_files" in error for error in validate_218_selected_requirement_badge_feature_package(extra_file)))

        dirty = copy.deepcopy(package)
        dirty["post_merge_git_status_short"] = " M package.json"
        dirty["package_hash"] = canonical_package_hash(dirty)
        self.assertTrue(any("post_merge_git_status_short" in error for error in validate_218_selected_requirement_badge_feature_package(dirty)))

    def test_218_rejects_authority_laundering_in_caller_controlled_fields(self):
        package = build_218_selected_requirement_badge_feature_package()
        hostile_values = [
            {"operator_notes": ["Codex approval grants live Codex execution authorized forever"]},
            {"operator_notes": ["feature commit proves blanket Kuronode source mutation"]},
            {"caller_supplied_evidence_refs": {"protected": "docs%252Frequirements%252Factive body text: The system shall..."}},
            {"caller_supplied_evidence_refs": {"tooling": "npm install && curl https://example.invalid"}},
            {"caller_supplied_evidence_refs": {"beo": "BEO closeout execution and publication greenlit"}},
            {"caller_supplied_evidence_refs": {"rtm": "RTM generation and coverage truth approved"}},
        ]

        for overrides in hostile_values:
            with self.subTest(overrides=overrides):
                candidate = copy.deepcopy(package)
                candidate.update(overrides)
                candidate["package_hash"] = canonical_package_hash(candidate)
                errors = validate_218_selected_requirement_badge_feature_package(candidate)
                self.assertTrue(errors, overrides)
                self.assertTrue(any("authority" in error.lower() or "protected" in error.lower() or "tool" in error.lower() for error in errors), errors)

    def test_218_next_frontier_is_operator_selected_not_granted(self):
        package = build_218_selected_requirement_badge_feature_package()

        self.assertEqual(package["next_frontier"], NEXT_FRONTIER_218)
        self.assertEqual(package["next_frontier"], "NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_OR_OBSERVED_FAILURE_HARDENING_NOT_GRANTED")
        self.assertFalse(package["beb_dispatch_authorized"])
        self.assertFalse(package["beo_closeout_execution_authorized"])
        self.assertFalse(package["blanket_kuronode_mutation_authorized"])


if __name__ == "__main__":
    unittest.main()
