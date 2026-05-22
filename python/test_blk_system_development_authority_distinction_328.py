import copy
import unittest

from blk_system_broad_side_effect_approval_guard_327 import (
    OPERATOR_APPROVAL_327,
    build_broad_side_effect_approval_guard_327,
)
from blk_system_development_authority_distinction_328 import (
    EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH,
    NEXT_FRONTIER_328,
    OPERATOR_CORRECTION_328,
    build_development_authority_distinction_328,
    validate_development_authority_distinction_328,
)
from blk_system_first_pass_9_9_322 import build_blk001_006_roadmap_first_pass_done_322
from blk_system_functional_9_ladder_326 import (
    OPERATOR_DIRECTIVE_326,
    build_functional_9_execution_ladder_326,
)
from blk_system_overall_9_guard_325 import (
    OPERATOR_DIRECTIVE_325,
    build_overall_9_development_directive_guard_325,
)
from blk_system_standing_development_approval_316 import (
    EXPECTED_316_OBSERVED_AT,
    EXPECTED_OPERATOR_DISCORD_ID,
    OPERATOR_STATEMENT_316,
    record_blk_system_standing_development_approval_316,
)
from blk_system_velocity_to_9_317_321 import (
    OPERATOR_DIRECTIVE_317,
    build_blk_system_9_of_10_readiness_matrix_320,
    build_blk_system_development_frontier_317,
    build_exact_no_clock_side_effect_request_318,
    evaluate_development_authority_laundering_guard_319,
    reconcile_blk_system_development_unblock_321,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    hash_package,
)


class BlkSystemDevelopmentAuthorityDistinction328Test(unittest.TestCase):
    def _broad_guard_327(self):
        record_316 = record_blk_system_standing_development_approval_316(
            operator_statement=OPERATOR_STATEMENT_316,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            observed_at=EXPECTED_316_OBSERVED_AT,
        )
        frontier = build_blk_system_development_frontier_317(
            record_316,
            operator_directive=OPERATOR_DIRECTIVE_317,
        )
        request = build_exact_no_clock_side_effect_request_318(frontier)
        guard = evaluate_development_authority_laundering_guard_319(
            request,
            operator_statement=OPERATOR_DIRECTIVE_317,
        )
        matrix = build_blk_system_9_of_10_readiness_matrix_320(guard)
        reconciliation = reconcile_blk_system_development_unblock_321(matrix)
        first_pass = build_blk001_006_roadmap_first_pass_done_322(
            reconciliation,
            operator_directive=(
                "plan an execute blk-system sprint for a first pass done of "
                "blk-001 to blk-006 and the blk-system roadmap"
            ),
            target_rating="9.9/10_not_10/10_pending_operator_review_and_verification",
        )
        guard_325 = build_overall_9_development_directive_guard_325(
            first_pass,
            operator_directive=OPERATOR_DIRECTIVE_325,
        )
        ladder = build_functional_9_execution_ladder_326(
            guard_325,
            operator_directive=OPERATOR_DIRECTIVE_326,
        )
        return build_broad_side_effect_approval_guard_327(
            ladder,
            operator_approval=OPERATOR_APPROVAL_327,
        )

    def test_328_records_development_authority_distinct_from_internal_requirements(self):
        record = build_development_authority_distinction_328(
            self._broad_guard_327(),
            operator_correction=OPERATOR_CORRECTION_328,
        )

        self.assertEqual(record["status"], "BLK_SYSTEM_328_DEVELOPMENT_AUTHORITY_DISTINCTION_RECORDED")
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_328)
        self.assertEqual(record["distinction_hash"], EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH)
        self.assertEqual(validate_development_authority_distinction_328(record), record)
        self.assertTrue(record["development_authority"]["all_blk_system_development_work_allowed"])
        self.assertFalse(record["development_authority"]["per_sprint_operator_approval_required"])
        self.assertTrue(record["development_authority"]["blk_system_repo_source_git_mutation_allowed"])
        self.assertTrue(record["internal_requirement_boundary"]["requirements_are_product_logic_not_development_approval"])
        self.assertTrue(record["internal_requirement_boundary"]["do_not_block_development_on_operator_approval_challenges"])
        self.assertIn("NON_BLK_SYSTEM_TARGET_MUTATION_BY_IMPLICATION", record["denied_confusions"])
        for side_effect in _FALSE_SIDE_EFFECTS:
            with self.subTest(side_effect=side_effect):
                self.assertIn(side_effect, record["side_effects"])
                self.assertFalse(record["side_effects"][side_effect])
        self.assertTrue(record["side_effects"]["development_authority_distinction_recorded"])
        self.assertTrue(record["side_effects"]["blk_system_development_work_unblocked"])
        self.assertTrue(record["side_effects"]["per_sprint_approval_requirement_removed"])
        self.assertTrue(record["side_effects"]["blk_system_repo_source_git_mutation_allowed"])

    def test_328_rejects_reintroducing_development_approval_requirements(self):
        record = build_development_authority_distinction_328(
            self._broad_guard_327(),
            operator_correction=OPERATOR_CORRECTION_328,
        )
        tampered = copy.deepcopy(record)
        tampered["development_authority"]["per_sprint_operator_approval_required"] = True
        tampered["distinction_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "distinction_hash"}
        )

        with self.assertRaisesRegex(ValueError, "development_authority|approval"):
            validate_development_authority_distinction_328(tampered)

    def test_328_rejects_using_internal_requirements_as_external_approval_gate(self):
        record = build_development_authority_distinction_328(
            self._broad_guard_327(),
            operator_correction=OPERATOR_CORRECTION_328,
        )
        tampered = copy.deepcopy(record)
        tampered["internal_requirement_boundary"]["do_not_block_development_on_operator_approval_challenges"] = False
        tampered["distinction_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "distinction_hash"}
        )

        with self.assertRaisesRegex(ValueError, "internal_requirement_boundary|development"):
            validate_development_authority_distinction_328(tampered)

    def test_328_rejects_adjacent_side_effect_grants(self):
        record = build_development_authority_distinction_328(
            self._broad_guard_327(),
            operator_correction=OPERATOR_CORRECTION_328,
        )

        for side_effect in _FALSE_SIDE_EFFECTS:
            with self.subTest(side_effect=side_effect):
                tampered = copy.deepcopy(record)
                tampered["side_effects"][side_effect] = True
                tampered["distinction_hash"] = hash_package(
                    {key: value for key, value in tampered.items() if key != "distinction_hash"}
                )
                with self.assertRaisesRegex(ValueError, "side_effects"):
                    validate_development_authority_distinction_328(tampered)


if __name__ == "__main__":
    unittest.main()
