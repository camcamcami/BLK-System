import copy
import unittest

from blk_system_standing_development_approval_316 import (
    EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH,
    NEXT_FRONTIER_316,
    OPERATOR_STATEMENT_316,
    StandingDevelopmentApproval316ValidationError,
    record_blk_system_standing_development_approval_316,
    validate_blk_system_standing_development_approval_316,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_OPERATOR_DISCORD_ID,
)

_OBSERVED_AT = "2026-05-21T19:09:37+10:00"


class BlkSystemStandingDevelopmentApproval316Test(unittest.TestCase):
    def _record(self):
        return record_blk_system_standing_development_approval_316(
            operator_statement=OPERATOR_STATEMENT_316,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            observed_at=_OBSERVED_AT,
        )

    def test_316_records_standing_blk_system_development_approval_without_expiring_clock(self):
        record = self._record()

        self.assertEqual(
            record["status"],
            "BLK_SYSTEM_STANDING_DEVELOPMENT_APPROVAL_RECORDED_NO_TIME_CLOCK",
        )
        self.assertIn(
            "BLK_SYSTEM_316_STANDING_BLK_SYSTEM_DEVELOPMENT_APPROVAL_RECORDED",
            record["markers"],
        )
        self.assertRegex(record["operator_statement_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertNotEqual(record["operator_statement_hash"], record["standing_development_approval_hash"])
        self.assertEqual(record["observed_at"], _OBSERVED_AT)
        self.assertFalse(record["time_clock_required"])
        self.assertTrue(record["approval_time_clock_retired_for_blk_system_development"])
        self.assertEqual(record["next_frontier"], NEXT_FRONTIER_316)
        self.assertNotIn("BEO_PUBLICATION", record["next_frontier"])
        self.assertNotIn("RUN_ID", record["next_frontier"])
        self.assertNotIn("issued_at", record)
        self.assertNotIn("expires_at", record)
        self.assertNotIn("challenge_expires_at", record)
        self.assertTrue(record["scope_limits"]["applies_to_blk_system_repository_development"])
        self.assertTrue(record["scope_limits"]["requires_tdd_hostile_review_and_closeout"])
        self.assertTrue(record["scope_limits"]["does_not_grant_beo_publication_or_run_id_movement"])
        self.assertTrue(record["side_effects"]["blk_system_repository_development_unblocked_from_time_clock"])
        self.assertFalse(record["side_effects"]["beo_publication"])
        self.assertFalse(record["side_effects"]["rtm_generation"])
        self.assertFalse(record["side_effects"]["production_blk_link"])
        self.assertFalse(record["side_effects"]["protected_body_access"])
        self.assertEqual(
            record["standing_development_approval_hash"],
            EXPECTED_316_STANDING_DEVELOPMENT_APPROVAL_HASH,
        )

    def test_316_rejects_reintroduced_expiry_or_challenge_clock_fields(self):
        record = self._record()
        for field in ["issued_at", "expires_at", "challenge_expires_at", "short_approval_reply"]:
            tampered = copy.deepcopy(record)
            tampered[field] = "2026-05-21T20:45:00+10:00"
            with self.subTest(field=field):
                with self.assertRaisesRegex(
                    StandingDevelopmentApproval316ValidationError,
                    "unsupported key|time clock",
                ):
                    validate_blk_system_standing_development_approval_316(tampered)

    def test_316_rejects_operator_or_statement_retargeting(self):
        with self.assertRaisesRegex(StandingDevelopmentApproval316ValidationError, "operator"):
            record_blk_system_standing_development_approval_316(
                operator_statement=OPERATOR_STATEMENT_316,
                operator_discord_id="000000000000000000",
                observed_at=_OBSERVED_AT,
            )

        with self.assertRaisesRegex(StandingDevelopmentApproval316ValidationError, "exact operator statement"):
            record_blk_system_standing_development_approval_316(
                operator_statement="Approve",
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                observed_at=_OBSERVED_AT,
            )

    def test_316_rejects_adjacent_runtime_publication_or_rtm_side_effects(self):
        record = self._record()
        for flag in [
            "approval_captured",
            "run_id_reserved",
            "beo_publication",
            "authoritative_beo_publication",
            "rtm_generation",
            "production_blk_link",
            "target_source_git_mutation",
            "runtime_tooling_executed",
        ]:
            tampered = copy.deepcopy(record)
            tampered["side_effects"][flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(
                    StandingDevelopmentApproval316ValidationError,
                    "side_effects|forbidden authority",
                ):
                    validate_blk_system_standing_development_approval_316(tampered)


if __name__ == "__main__":
    unittest.main()
