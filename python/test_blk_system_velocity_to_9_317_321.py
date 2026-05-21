import copy
import unittest

from blk_system_standing_development_approval_316 import (
    EXPECTED_316_OBSERVED_AT,
    EXPECTED_OPERATOR_DISCORD_ID,
    OPERATOR_STATEMENT_316,
    record_blk_system_standing_development_approval_316,
)
from verified_loop_beo_publication_approval_request_306_309 import hash_package

from blk_system_velocity_to_9_317_321 import (
    EXPECTED_317_FRONTIER_HASH,
    EXPECTED_318_REQUEST_HASH,
    EXPECTED_319_GUARD_HASH,
    EXPECTED_320_READINESS_MATRIX_HASH,
    EXPECTED_321_RECONCILIATION_HASH,
    NEXT_FRONTIER_321,
    OPERATOR_DIRECTIVE_317,
    VelocityTo9ValidationError,
    build_blk_system_9_of_10_readiness_matrix_320,
    build_blk_system_development_frontier_317,
    build_exact_no_clock_side_effect_request_318,
    evaluate_development_authority_laundering_guard_319,
    reconcile_blk_system_development_unblock_321,
    validate_blk_system_9_of_10_readiness_matrix_320,
    validate_blk_system_development_frontier_317,
    validate_blk_system_development_unblock_reconciliation_321,
    validate_development_authority_laundering_guard_319,
    validate_exact_no_clock_side_effect_request_318,
)


class BlkSystemVelocityTo9Package317To321Test(unittest.TestCase):
    def _record_316(self):
        return record_blk_system_standing_development_approval_316(
            operator_statement=OPERATOR_STATEMENT_316,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            observed_at=EXPECTED_316_OBSERVED_AT,
        )

    def _frontier_317(self):
        return build_blk_system_development_frontier_317(
            self._record_316(),
            operator_directive=OPERATOR_DIRECTIVE_317,
        )

    def _request_318(self):
        return build_exact_no_clock_side_effect_request_318(self._frontier_317())

    def _guard_319(self):
        return evaluate_development_authority_laundering_guard_319(
            self._request_318(),
            operator_statement=OPERATOR_DIRECTIVE_317,
        )

    def _matrix_320(self):
        return build_blk_system_9_of_10_readiness_matrix_320(self._guard_319())

    def test_317_to_321_builds_repo_development_unblock_without_side_effects(self):
        frontier = self._frontier_317()
        request = self._request_318()
        guard = self._guard_319()
        matrix = self._matrix_320()
        reconciliation = reconcile_blk_system_development_unblock_321(matrix)

        self.assertEqual(frontier["status"], "BLK_SYSTEM_9_OF_10_DEVELOPMENT_FRONTIER_BOUND")
        self.assertIn("BLK_SYSTEM_317_9_OF_10_DEVELOPMENT_FRONTIER_BOUND", frontier["markers"])
        self.assertEqual(frontier["standing_development_approval_hash"], self._record_316()["standing_development_approval_hash"])
        self.assertFalse(frontier["time_clock_required"])
        self.assertFalse(frontier["side_effects"]["run_id_reserved"])
        self.assertFalse(frontier["side_effects"]["authoritative_beo_publication"])
        self.assertRegex(frontier["frontier_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(frontier["frontier_hash"], EXPECTED_317_FRONTIER_HASH)

        self.assertEqual(request["status"], "EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY_NOT_APPROVED")
        self.assertIn("BLK_SYSTEM_318_EXACT_NO_CLOCK_SIDE_EFFECT_REQUEST_READY", request["markers"])
        self.assertEqual(request["frontier_hash"], frontier["frontier_hash"])
        self.assertEqual(request["decision_mode"], "separate_exact_no_clock_side_effect_decision_required")
        self.assertNotIn("approved_at", request)
        self.assertNotIn("expires_at", request)
        self.assertNotIn("run_id", request)
        self.assertFalse(request["side_effects"]["approval_captured"])
        self.assertFalse(request["side_effects"]["beo_publication"])
        self.assertFalse(request["side_effects"]["rtm_generation"])
        self.assertFalse(request["side_effects"]["production_blk_link"])
        self.assertRegex(request["request_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(request["request_hash"], EXPECTED_318_REQUEST_HASH)

        self.assertEqual(guard["status"], "DEVELOPMENT_DIRECTIVE_GUARDED_NOT_SIDE_EFFECT_APPROVAL")
        self.assertIn("BLK_SYSTEM_319_DEVELOPMENT_DIRECTIVE_GUARD_RECORDED", guard["markers"])
        self.assertEqual(guard["operator_statement_hash"], hash_package({"operator_statement": OPERATOR_DIRECTIVE_317}))
        self.assertEqual(guard["classification"], "development_directive_only_not_side_effect_approval")
        self.assertFalse(guard["side_effects"]["approval_captured"])
        self.assertFalse(guard["side_effects"]["run_id_reserved"])
        self.assertRegex(guard["guard_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(guard["guard_hash"], EXPECTED_319_GUARD_HASH)

        self.assertEqual(matrix["status"], "BLK_SYSTEM_9_OF_10_READINESS_MATRIX_READY_SIDE_EFFECTS_SEPARATE")
        self.assertIn("BLK_SYSTEM_320_9_OF_10_READINESS_MATRIX_READY", matrix["markers"])
        self.assertEqual(matrix["readiness_rating"], "8.5/10_repo_development_ready_side_effects_blocked")
        self.assertTrue(matrix["lanes"]["repository_development"]["ready"])
        for lane in (
            "beo_publication_finality",
            "rtm_production_blk_link_trace_closure",
            "production_blk_test_mcp_verifier_pilot",
            "identity_relay_runtime_pilot",
            "reusable_blk003_loop",
        ):
            self.assertEqual(matrix["lanes"][lane]["required_decision"], "separate_exact_no_clock_decision_required")
        self.assertFalse(matrix["side_effects"]["protected_body_access"])
        self.assertRegex(matrix["readiness_matrix_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(matrix["readiness_matrix_hash"], EXPECTED_320_READINESS_MATRIX_HASH)

        self.assertEqual(reconciliation["status"], "BLK_SYSTEM_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED")
        self.assertIn("BLK_SYSTEM_321_9_OF_10_DEVELOPMENT_UNBLOCK_RECONCILED", reconciliation["markers"])
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER_321)
        self.assertFalse(reconciliation["side_effects"]["beo_publication"])
        self.assertFalse(reconciliation["side_effects"]["rtm_generation"])
        self.assertFalse(reconciliation["side_effects"]["production_blk_link"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(reconciliation["reconciliation_hash"], EXPECTED_321_RECONCILIATION_HASH)

    def test_rejects_tampered_316_and_reintroduced_time_clock_fields(self):
        record_316 = self._record_316()
        tampered = copy.deepcopy(record_316)
        tampered["next_frontier"] = "NEXT_FRONTIER_BEO_PUBLICATION_APPROVED"
        tampered["standing_development_approval_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "standing_development_approval_hash"}
        )
        with self.assertRaisesRegex(VelocityTo9ValidationError, "standing development approval"):
            build_blk_system_development_frontier_317(
                tampered,
                operator_directive=OPERATOR_DIRECTIVE_317,
            )

        frontier = self._frontier_317()
        for key in ("issued_at", "expires_at", "challenge_nonce", "short_approval_reply"):
            changed = copy.deepcopy(frontier)
            changed[key] = "2026-05-21T20:00:00+10:00"
            changed["frontier_hash"] = hash_package(
                {item_key: item for item_key, item in changed.items() if item_key != "frontier_hash"}
            )
            with self.subTest(key=key):
                with self.assertRaisesRegex(VelocityTo9ValidationError, "time clock"):
                    validate_blk_system_development_frontier_317(changed)

    def test_318_and_320_reject_side_effect_flag_flips_even_with_rehash(self):
        request = self._request_318()
        for flag in (
            "approval_captured",
            "run_id_reserved",
            "beo_publication",
            "authoritative_beo_publication",
            "rtm_generation",
            "production_blk_link",
            "protected_body_access",
            "runtime_tooling_executed",
        ):
            changed = copy.deepcopy(request)
            changed["side_effects"][flag] = True
            changed["request_hash"] = hash_package(
                {key: value for key, value in changed.items() if key != "request_hash"}
            )
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(VelocityTo9ValidationError, "side_effects|forbidden authority"):
                    validate_exact_no_clock_side_effect_request_318(changed, self._frontier_317())

        matrix = self._matrix_320()
        changed_matrix = copy.deepcopy(matrix)
        changed_matrix["lanes"]["beo_publication_finality"]["required_decision"] = "approved_by_standing_development_record"
        changed_matrix["readiness_matrix_hash"] = hash_package(
            {key: value for key, value in changed_matrix.items() if key != "readiness_matrix_hash"}
        )
        with self.assertRaisesRegex(VelocityTo9ValidationError, "lane decision"):
            validate_blk_system_9_of_10_readiness_matrix_320(changed_matrix, self._guard_319())

    def test_319_rejects_side_effect_approval_laundering_phrases(self):
        request = self._request_318()
        for statement in (
            "Approve",
            "APPROVE BLK-SYSTEM-269..271 EXACT BEO PUBLICATION EXECUTION PACKAGE; ONE RUN ID ONLY",
            "BEO publication authorized; production blk-link allowed",
            "publishBEO and rtmGenerated with docs%252Frequirements%252Factive body access",
        ):
            with self.subTest(statement=statement):
                with self.assertRaisesRegex(VelocityTo9ValidationError, "not a development directive|forbidden authority"):
                    evaluate_development_authority_laundering_guard_319(
                        request,
                        operator_statement=statement,
                    )

    def test_321_reconciliation_rejects_rehashed_matrix_or_adjacent_authority(self):
        matrix = self._matrix_320()
        tampered = copy.deepcopy(matrix)
        tampered["lanes"]["rtm_production_blk_link_trace_closure"]["required_decision"] = "approved"
        tampered["readiness_matrix_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "readiness_matrix_hash"}
        )
        with self.assertRaisesRegex(VelocityTo9ValidationError, "lane decision"):
            reconcile_blk_system_development_unblock_321(tampered)

        reconciliation = reconcile_blk_system_development_unblock_321(matrix)
        changed = copy.deepcopy(reconciliation)
        changed["side_effects"]["production_blk_link"] = True
        changed["reconciliation_hash"] = hash_package(
            {key: value for key, value in changed.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(VelocityTo9ValidationError, "side_effects|forbidden authority"):
            validate_blk_system_development_unblock_reconciliation_321(changed, matrix)


if __name__ == "__main__":
    unittest.main()
