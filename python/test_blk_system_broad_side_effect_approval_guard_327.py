import copy
import unittest

from blk_system_broad_side_effect_approval_guard_327 import (
    EXPECTED_327_BROAD_APPROVAL_GUARD_HASH,
    NEXT_FRONTIER_327,
    OPERATOR_APPROVAL_327,
    build_broad_side_effect_approval_guard_327,
    validate_broad_side_effect_approval_guard_327,
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
from verified_loop_beo_publication_approval_request_306_309 import hash_package


class BlkSystemBroadSideEffectApprovalGuard327Test(unittest.TestCase):
    def _functional_ladder_326(self):
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
        return build_functional_9_execution_ladder_326(
            guard_325,
            operator_directive=OPERATOR_DIRECTIVE_326,
        )

    def test_327_records_broad_approval_as_non_executable_split_required(self):
        record = build_broad_side_effect_approval_guard_327(
            self._functional_ladder_326(),
            operator_approval=OPERATOR_APPROVAL_327,
        )

        self.assertEqual(record["status"], "BLK_SYSTEM_327_BROAD_SIDE_EFFECT_APPROVAL_REJECTED")
        self.assertEqual(record["classification"], "broad_multi_surface_approval_not_exact_bounded_decision")
        self.assertEqual(record["prior_frontier"], "NEXT_FRONTIER_FUNCTIONAL_9_EXACT_BEO_SIDE_EFFECT_DECISION_REQUIRED_NOT_GRANTED")
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_327)
        self.assertEqual(record["guard_hash"], EXPECTED_327_BROAD_APPROVAL_GUARD_HASH)
        self.assertEqual(validate_broad_side_effect_approval_guard_327(record), record)
        self.assertTrue(record["side_effects"]["broad_approval_guard_executed"])
        self.assertTrue(record["side_effects"]["broad_approval_recorded_as_non_executable"])
        self.assertFalse(record["side_effects"]["approval_captured"])
        self.assertFalse(record["side_effects"]["run_id_reserved"])
        self.assertFalse(record["side_effects"]["run_id_consumed"])
        self.assertFalse(record["side_effects"]["beo_publication"])
        self.assertFalse(record["side_effects"]["signature_generated"])
        self.assertFalse(record["side_effects"]["rtm_generation"])
        self.assertFalse(record["side_effects"]["production_blk_link"])
        self.assertFalse(record["side_effects"]["protected_body_access"])
        self.assertFalse(record["side_effects"]["target_source_git_mutation"])

    def test_327_requires_broad_approval_to_be_rejected_not_partially_captured(self):
        record = build_broad_side_effect_approval_guard_327(
            self._functional_ladder_326(),
            operator_approval=OPERATOR_APPROVAL_327,
        )
        self.assertIn("BEO_PUBLICATION", record["requested_authorities"])
        self.assertIn("SOURCE_GIT_MUTATION_OUTSIDE_EXACT_SPRINT_DISCIPLINE", record["requested_authorities"])
        self.assertIn("PROTECTED_BODY_ACCESS", record["requested_authorities"])
        self.assertEqual(record["rejection_reasons"], [
            "approval_bundles_multiple_independent_authority_surfaces",
            "approval_includes_source_git_mutation_outside_exact_sprint_discipline",
            "approval_includes_protected_body_access_without_exact_id_or_hash_metadata_scope",
            "approval_includes_runtime_tooling_without_bounded_payload_or_replay_contract",
            "beo_publication_must_be_split_from_rtm_and_production_blk_link",
        ])

        tampered = copy.deepcopy(record)
        tampered["classification"] = "captured_exact_broad_approval"
        tampered["guard_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "guard_hash"}
        )
        with self.assertRaisesRegex(ValueError, "classification|authority|approval"):
            validate_broad_side_effect_approval_guard_327(tampered)

        tampered = copy.deepcopy(record)
        tampered["side_effects"]["approval_captured"] = True
        tampered["guard_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "guard_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|approval|authority"):
            validate_broad_side_effect_approval_guard_327(tampered)

    def test_327_rejects_partial_or_laundered_approval_text(self):
        ladder = self._functional_ladder_326()
        for approval_text in [
            "I approve BEO publication only",
            f"{OPERATOR_APPROVAL_327}\nAnd execute it now anyway",
            f"{OPERATOR_APPROVAL_327}\nprotected body hashed",
            f"{OPERATOR_APPROVAL_327}\nrun ID reserved",
        ]:
            with self.subTest(approval_text=approval_text):
                with self.assertRaisesRegex(ValueError, "operator_approval|authority|mismatch"):
                    build_broad_side_effect_approval_guard_327(
                        ladder,
                        operator_approval=approval_text,
                    )


if __name__ == "__main__":
    unittest.main()
