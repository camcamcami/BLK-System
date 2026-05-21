import copy
import unittest

from blk_system_first_pass_9_9_322 import build_blk001_006_roadmap_first_pass_done_322
from blk_system_overall_9_guard_325 import (
    EXPECTED_325_OVERALL_GUARD_HASH,
    NEXT_FRONTIER_325,
    OPERATOR_DIRECTIVE_325,
    build_overall_9_development_directive_guard_325,
    validate_overall_9_development_directive_guard_325,
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


class BlkSystemOverallNineGuard325Test(unittest.TestCase):
    def _first_pass_322(self):
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
        return build_blk001_006_roadmap_first_pass_done_322(
            reconciliation,
            operator_directive=(
                "plan an execute blk-system sprint for a first pass done of "
                "blk-001 to blk-006 and the blk-system roadmap"
            ),
            target_rating="9.9/10_not_10/10_pending_operator_review_and_verification",
        )

    def test_325_classifies_overall_9_directive_as_development_only(self):
        record = build_overall_9_development_directive_guard_325(
            self._first_pass_322(),
            operator_directive=OPERATOR_DIRECTIVE_325,
        )

        self.assertEqual(record["status"], "BLK_SYSTEM_325_OVERALL_9_DIRECTIVE_GUARDED")
        self.assertEqual(record["classification"], "development_directive_only_not_side_effect_approval")
        self.assertEqual(record["current_overall_rating"], "7/10_practical_overall_baseline")
        self.assertEqual(record["target_overall_rating"], "9/10_overall_requires_exact_side_effect_decision")
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_325)
        self.assertEqual(record["guard_hash"], EXPECTED_325_OVERALL_GUARD_HASH)
        self.assertEqual(validate_overall_9_development_directive_guard_325(record), record)
        self.assertTrue(record["side_effects"]["overall_9_directive_guarded"])
        self.assertFalse(record["side_effects"]["approval_captured"])
        self.assertFalse(record["side_effects"]["run_id_reserved"])
        self.assertFalse(record["side_effects"]["run_id_consumed"])
        self.assertFalse(record["side_effects"]["beo_publication"])
        self.assertFalse(record["side_effects"]["signature_generated"])
        self.assertFalse(record["side_effects"]["rtm_generation"])
        self.assertFalse(record["side_effects"]["production_blk_link"])
        self.assertFalse(record["side_effects"]["protected_body_access"])

    def test_325_rejects_side_effect_laundering_in_directive_and_lanes(self):
        first_pass = self._first_pass_322()
        for hostile_directive in [
            f"{OPERATOR_DIRECTIVE_325}; publish the BEO",
            f"{OPERATOR_DIRECTIVE_325}; reserve one run ID",
            f"{OPERATOR_DIRECTIVE_325}; generate RTM",
            f"{OPERATOR_DIRECTIVE_325}; production blk-link enabled",
            f"{OPERATOR_DIRECTIVE_325}; protected BLK-req body hashing authorized",
            f"{OPERATOR_DIRECTIVE_325}; signerStorageLedgerAction",
        ]:
            with self.subTest(hostile_directive=hostile_directive):
                with self.assertRaisesRegex(ValueError, "authority|operator_directive"):
                    build_overall_9_development_directive_guard_325(
                        first_pass,
                        operator_directive=hostile_directive,
                    )

        record = build_overall_9_development_directive_guard_325(
            first_pass,
            operator_directive=OPERATOR_DIRECTIVE_325,
        )
        tampered = copy.deepcopy(record)
        tampered["target_gap_closure_plan"][0]["required_decision"] = "approved_by_all_sprints_directive"
        tampered["guard_hash"] = hash_package({key: value for key, value in tampered.items() if key != "guard_hash"})
        with self.assertRaisesRegex(ValueError, "target_gap_closure_plan|authority"):
            validate_overall_9_development_directive_guard_325(tampered)

        tampered = copy.deepcopy(record)
        tampered["side_effects"]["run_id_reserved"] = True
        tampered["guard_hash"] = hash_package({key: value for key, value in tampered.items() if key != "guard_hash"})
        with self.assertRaisesRegex(ValueError, "side_effects|authority"):
            validate_overall_9_development_directive_guard_325(tampered)

    def test_325_rejects_rehashed_first_pass_or_overall_finality_claim(self):
        first_pass = self._first_pass_322()
        tampered_first_pass = copy.deepcopy(first_pass)
        tampered_first_pass["readiness_rating"] = "9.9/10_overall_complete"
        tampered_first_pass["first_pass_hash"] = hash_package(
            {key: value for key, value in tampered_first_pass.items() if key != "first_pass_hash"}
        )
        with self.assertRaisesRegex(ValueError, "322|first pass"):
            build_overall_9_development_directive_guard_325(
                tampered_first_pass,
                operator_directive=OPERATOR_DIRECTIVE_325,
            )

        record = build_overall_9_development_directive_guard_325(
            first_pass,
            operator_directive=OPERATOR_DIRECTIVE_325,
        )
        tampered = copy.deepcopy(record)
        tampered["target_overall_rating"] = "9/10_overall_finality_achieved"
        tampered["guard_hash"] = hash_package({key: value for key, value in tampered.items() if key != "guard_hash"})
        with self.assertRaisesRegex(ValueError, "target_overall_rating|authority"):
            validate_overall_9_development_directive_guard_325(tampered)


if __name__ == "__main__":
    unittest.main()
