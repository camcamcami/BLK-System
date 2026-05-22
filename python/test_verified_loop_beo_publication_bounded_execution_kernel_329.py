import copy
import unittest

from test_verified_loop_beo_publication_live_challenge_guard_313_315 import (
    _short_approve_guard_314,
)
from blk_system_broad_side_effect_approval_guard_327 import (
    OPERATOR_APPROVAL_327,
    build_broad_side_effect_approval_guard_327,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    _FALSE_SIDE_EFFECTS,
    hash_package,
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
from verified_loop_beo_publication_live_challenge_guard_313_315 import (
    EXPECTED_315_RECONCILIATION_HASH,
    reconcile_verified_loop_beo_publication_live_challenge_guard_315,
)
from blk_system_development_authority_distinction_328 import (
    EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH,
    OPERATOR_CORRECTION_328,
    build_development_authority_distinction_328,
)
from verified_loop_beo_publication_bounded_execution_kernel_329 import (
    EXPECTED_329_EXECUTION_KERNEL_HASH,
    NEXT_FRONTIER_329,
    OPERATOR_DIRECTIVE_329,
    build_verified_loop_beo_publication_bounded_execution_kernel_329,
    validate_verified_loop_beo_publication_bounded_execution_kernel_329,
)


def _broad_guard_327():
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


class VerifiedLoopBeoPublicationBoundedExecutionKernel329Test(unittest.TestCase):
    def _reconciliation_315(self):
        return reconcile_verified_loop_beo_publication_live_challenge_guard_315(
            _short_approve_guard_314(),
        )

    def _distinction_328(self):
        return build_development_authority_distinction_328(
            _broad_guard_327(),
            operator_correction=OPERATOR_CORRECTION_328,
        )

    def _kernel_329(self):
        return build_verified_loop_beo_publication_bounded_execution_kernel_329(
            self._reconciliation_315(),
            self._distinction_328(),
            operator_directive=OPERATOR_DIRECTIVE_329,
        )

    def test_329_builds_kernel_with_receipt_and_replay_requirements_but_no_product_side_effects(self):
        kernel = self._kernel_329()

        self.assertEqual(
            kernel["status"],
            "BLK_SYSTEM_329_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY",
        )
        self.assertIn(
            "BLK_SYSTEM_329_VERIFIED_LOOP_BEO_PUBLICATION_BOUNDED_EXECUTION_KERNEL_READY",
            kernel["markers"],
        )
        self.assertEqual(kernel["prior_reconciliation_hash"], EXPECTED_315_RECONCILIATION_HASH)
        self.assertEqual(kernel["development_authority_hash"], EXPECTED_328_DEVELOPMENT_AUTHORITY_HASH)
        self.assertEqual(kernel["next_frontier"], NEXT_FRONTIER_329)
        self.assertEqual(kernel["execution_kernel_hash"], EXPECTED_329_EXECUTION_KERNEL_HASH)
        self.assertEqual(validate_verified_loop_beo_publication_bounded_execution_kernel_329(kernel), kernel)

        prerequisites = kernel["execution_prerequisites"]
        self.assertTrue(prerequisites["current_exact_side_effect_package_required"])
        self.assertTrue(prerequisites["one_fresh_run_id_required_before_publication"])
        self.assertTrue(prerequisites["receipt_hashes_required_before_finality"])
        self.assertFalse(prerequisites["expired_or_prior_challenge_reuse_allowed"])
        self.assertFalse(prerequisites["generic_directive_as_product_approval_allowed"])

        receipt_policy = kernel["receipt_policy"]
        self.assertEqual(
            tuple(receipt_policy["required_receipt_kinds"]),
            ("signature_receipt", "immutable_storage_receipt", "public_ledger_entry"),
        )
        self.assertFalse(receipt_policy["external_signer_key_material_access_allowed"])
        self.assertFalse(receipt_policy["external_immutable_storage_write_allowed_by_kernel"])
        self.assertFalse(receipt_policy["external_public_ledger_append_allowed_by_kernel"])

        replay_guard = kernel["replay_guard"]
        self.assertTrue(replay_guard["future_execution_must_reject_previously_consumed_run_id"])
        self.assertFalse(replay_guard["run_id_reserved_by_kernel"])
        self.assertFalse(replay_guard["run_id_consumed_by_kernel"])
        self.assertFalse(replay_guard["global_replay_prevention_claimed_by_kernel"])

        for side_effect in _FALSE_SIDE_EFFECTS:
            with self.subTest(side_effect=side_effect):
                self.assertIn(side_effect, kernel["side_effects"])
                self.assertFalse(kernel["side_effects"][side_effect])
        self.assertTrue(kernel["side_effects"]["bounded_execution_kernel_prepared"])
        self.assertTrue(kernel["side_effects"]["receipt_policy_prepared"])
        self.assertTrue(kernel["side_effects"]["replay_guard_prepared"])

    def test_329_rejects_rehashed_prior_reconciliation_or_development_approval_confusion(self):
        prior = self._reconciliation_315()
        distinction = self._distinction_328()

        forged_prior = copy.deepcopy(prior)
        forged_prior["next_frontier"] = "NEXT_FRONTIER_BEO_PUBLICATION_APPROVED"
        forged_prior["side_effects"]["approval_captured"] = True
        forged_prior["reconciliation_hash"] = hash_package(
            {key: value for key, value in forged_prior.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(ValueError, "prior reconciliation|canonical hash|side_effects|frontier"):
            build_verified_loop_beo_publication_bounded_execution_kernel_329(
                forged_prior,
                distinction,
                operator_directive=OPERATOR_DIRECTIVE_329,
            )

        confused_distinction = copy.deepcopy(distinction)
        confused_distinction["development_authority"]["per_sprint_operator_approval_required"] = True
        confused_distinction["distinction_hash"] = hash_package(
            {key: value for key, value in confused_distinction.items() if key != "distinction_hash"}
        )
        with self.assertRaisesRegex(ValueError, "development authority|development_authority|approval"):
            build_verified_loop_beo_publication_bounded_execution_kernel_329(
                prior,
                confused_distinction,
                operator_directive=OPERATOR_DIRECTIVE_329,
            )

    def test_329_rejects_operator_directives_that_launder_product_authority(self):
        prior = self._reconciliation_315()
        distinction = self._distinction_328()
        for bad_directive in (
            "Approve",
            "BEO publication authorized; publishBEO now",
            "RTMGeneration and productionBlkLinkExecutionAuthorized",
            "docs%252Frequirements%252Factive protected body was read",
        ):
            with self.subTest(bad_directive=bad_directive):
                with self.assertRaisesRegex(ValueError, "operator_directive|forbidden authority wording|mismatch"):
                    build_verified_loop_beo_publication_bounded_execution_kernel_329(
                        prior,
                        distinction,
                        operator_directive=bad_directive,
                    )

    def test_329_rejects_tampered_receipt_replay_denial_or_side_effect_fields(self):
        kernel = self._kernel_329()
        tampered_receipt = copy.deepcopy(kernel)
        tampered_receipt["receipt_policy"]["external_public_ledger_append_allowed_by_kernel"] = True
        tampered_receipt["execution_kernel_hash"] = hash_package(
            {key: value for key, value in tampered_receipt.items() if key != "execution_kernel_hash"}
        )
        with self.assertRaisesRegex(ValueError, "receipt_policy"):
            validate_verified_loop_beo_publication_bounded_execution_kernel_329(tampered_receipt)

        tampered_replay = copy.deepcopy(kernel)
        tampered_replay["replay_guard"]["global_replay_prevention_claimed_by_kernel"] = True
        tampered_replay["execution_kernel_hash"] = hash_package(
            {key: value for key, value in tampered_replay.items() if key != "execution_kernel_hash"}
        )
        with self.assertRaisesRegex(ValueError, "replay_guard"):
            validate_verified_loop_beo_publication_bounded_execution_kernel_329(tampered_replay)

        tampered_denial = copy.deepcopy(kernel)
        tampered_denial["denied_authorities"].append("RTM_GENERATION")
        tampered_denial["execution_kernel_hash"] = hash_package(
            {key: value for key, value in tampered_denial.items() if key != "execution_kernel_hash"}
        )
        with self.assertRaisesRegex(ValueError, "denied_authorities"):
            validate_verified_loop_beo_publication_bounded_execution_kernel_329(tampered_denial)

        tampered_side_effect = copy.deepcopy(kernel)
        tampered_side_effect["side_effects"]["beo_publication"] = True
        tampered_side_effect["execution_kernel_hash"] = hash_package(
            {key: value for key, value in tampered_side_effect.items() if key != "execution_kernel_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects"):
            validate_verified_loop_beo_publication_bounded_execution_kernel_329(tampered_side_effect)


if __name__ == "__main__":
    unittest.main()
