import copy
import unittest

from blk_system_first_pass_9_9_322 import build_blk001_006_roadmap_first_pass_done_322
from blk_system_functional_9_ladder_326 import (
    EXPECTED_326_FUNCTIONAL_9_LADDER_HASH,
    NEXT_FRONTIER_326,
    OPERATOR_DIRECTIVE_326,
    build_functional_9_execution_ladder_326,
    validate_functional_9_execution_ladder_326,
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
from verified_loop_beo_publication_approval_request_306_309 import hash_package


class BlkSystemFunctionalNineLadder326Test(unittest.TestCase):
    def _guard_325(self):
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
        return build_overall_9_development_directive_guard_325(
            first_pass,
            operator_directive=OPERATOR_DIRECTIVE_325,
        )

    def test_326_records_functional_9_ladder_without_side_effect_execution(self):
        record = build_functional_9_execution_ladder_326(
            self._guard_325(),
            operator_directive=OPERATOR_DIRECTIVE_326,
        )

        self.assertEqual(record["status"], "BLK_SYSTEM_326_FUNCTIONAL_9_EXECUTION_LADDER_READY")
        self.assertEqual(record["classification"], "functional_9_plan_executed_to_authority_boundary")
        self.assertEqual(record["current_overall_rating"], "7/10_practical_overall_baseline")
        self.assertEqual(record["target_overall_rating"], "9/10_functional_target_requires_exact_side_effect_chain")
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_326)
        self.assertEqual(record["ladder_hash"], EXPECTED_326_FUNCTIONAL_9_LADDER_HASH)
        self.assertEqual(validate_functional_9_execution_ladder_326(record), record)
        self.assertTrue(record["side_effects"]["functional_9_ladder_recorded"])
        self.assertFalse(record["side_effects"]["approval_captured"])
        self.assertFalse(record["side_effects"]["run_id_reserved"])
        self.assertFalse(record["side_effects"]["run_id_consumed"])
        self.assertFalse(record["side_effects"]["beo_publication"])
        self.assertFalse(record["side_effects"]["signature_generated"])
        self.assertFalse(record["side_effects"]["rtm_generation"])
        self.assertFalse(record["side_effects"]["production_blk_link"])
        self.assertFalse(record["side_effects"]["protected_body_access"])

        ladder = record["functional_ladder"]
        self.assertEqual(ladder[0]["sprint"], "326")
        self.assertTrue(ladder[0]["can_execute_under_current_message"])
        self.assertEqual(ladder[1]["phase"], "current_verified_loop_beo_publication_decision")
        self.assertFalse(ladder[1]["can_execute_under_current_message"])
        self.assertEqual(ladder[1]["blocker"], "separate_exact_side_effect_decision_required")
        self.assertTrue(
            all(not item["can_execute_under_current_message"] for item in ladder[1:]),
            ladder,
        )

    def test_326_rejects_laundered_side_effects_in_directive_or_ladder(self):
        guard_325 = self._guard_325()
        for hostile_directive in [
            f"{OPERATOR_DIRECTIVE_326}; publish the BEO",
            f"{OPERATOR_DIRECTIVE_326}; run id consumed",
            f"{OPERATOR_DIRECTIVE_326}; signature generated",
            f"{OPERATOR_DIRECTIVE_326}; RTM generated",
            f"{OPERATOR_DIRECTIVE_326}; production blk-link enabled",
            f"{OPERATOR_DIRECTIVE_326}; protected body hashed",
        ]:
            with self.subTest(hostile_directive=hostile_directive):
                with self.assertRaisesRegex(ValueError, "authority|operator_directive"):
                    build_functional_9_execution_ladder_326(
                        guard_325,
                        operator_directive=hostile_directive,
                    )

        record = build_functional_9_execution_ladder_326(
            guard_325,
            operator_directive=OPERATOR_DIRECTIVE_326,
        )
        tampered = copy.deepcopy(record)
        tampered["functional_ladder"][1]["can_execute_under_current_message"] = True
        tampered["ladder_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "ladder_hash"}
        )
        with self.assertRaisesRegex(ValueError, "functional_ladder|side effect"):
            validate_functional_9_execution_ladder_326(tampered)

        tampered = copy.deepcopy(record)
        tampered["functional_ladder"][1]["blocker"] = "beo publication authorized by broad functional directive"
        tampered["ladder_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "ladder_hash"}
        )
        with self.assertRaisesRegex(ValueError, "functional_ladder|authority|publication"):
            validate_functional_9_execution_ladder_326(tampered)

        tampered = copy.deepcopy(record)
        tampered["side_effects"]["signature_generated"] = True
        tampered["ladder_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "ladder_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|authority"):
            validate_functional_9_execution_ladder_326(tampered)

    def test_326_rejects_tampered_325_dependency_or_finality_claim(self):
        guard_325 = self._guard_325()
        tampered_guard = copy.deepcopy(guard_325)
        tampered_guard["target_overall_rating"] = "9/10_overall_finality_achieved"
        tampered_guard["guard_hash"] = hash_package(
            {key: value for key, value in tampered_guard.items() if key != "guard_hash"}
        )
        with self.assertRaisesRegex(ValueError, "325|overall"):
            build_functional_9_execution_ladder_326(
                tampered_guard,
                operator_directive=OPERATOR_DIRECTIVE_326,
            )

        record = build_functional_9_execution_ladder_326(
            guard_325,
            operator_directive=OPERATOR_DIRECTIVE_326,
        )
        tampered = copy.deepcopy(record)
        tampered["target_overall_rating"] = "9/10_functional_finality_achieved"
        tampered["ladder_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "ladder_hash"}
        )
        with self.assertRaisesRegex(ValueError, "target_overall_rating|authority"):
            validate_functional_9_execution_ladder_326(tampered)


if __name__ == "__main__":
    unittest.main()
