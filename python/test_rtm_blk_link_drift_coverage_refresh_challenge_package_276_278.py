import copy
import unittest

from test_rtm_blk_link_drift_coverage_request_package_272_275 import (
    _OPERATOR_IDENTITY,
    _challenge_273,
)
import rtm_blk_link_drift_coverage_request_package_272_275 as request_package
import rtm_blk_link_drift_coverage_refresh_challenge_package_276_278 as refresh_package


_EXPIRED_APPROVE_EVALUATED_AT = "2026-05-20T10:04:13+10:00"
_REFRESH_ISSUED_AT = "2026-05-20T10:41:00+10:00"
_REFRESH_EXPIRES_AT = "2026-05-20T11:41:00+10:00"
_REFRESH_NONCE = "BLK-SYSTEM-277-RTM-BLK-LINK-REFRESH-001"


def _expired_attempt_276():
    return refresh_package.record_expired_rtm_blk_link_drift_coverage_approve_attempt_276(
        _challenge_273(),
        operator_reply="Approve",
        operator_identity=_OPERATOR_IDENTITY,
        evaluated_at=_EXPIRED_APPROVE_EVALUATED_AT,
    )


def _refresh_challenge_277():
    return refresh_package.build_rtm_blk_link_drift_coverage_refresh_challenge_277(
        _expired_attempt_276(),
        operator_identity=_OPERATOR_IDENTITY,
        challenge_nonce=_REFRESH_NONCE,
        issued_at=_REFRESH_ISSUED_AT,
        expires_at=_REFRESH_EXPIRES_AT,
    )


class RtmBlkLinkDriftCoverageRefreshChallenge276To278Test(unittest.TestCase):
    def test_276_to_278_records_expired_approve_and_reissues_bounded_challenge_without_authority(self):
        expired_attempt = _expired_attempt_276()
        refresh_challenge = _refresh_challenge_277()
        reconciliation = refresh_package.reconcile_rtm_blk_link_drift_coverage_refresh_challenge_278(
            refresh_challenge
        )

        self.assertEqual(
            expired_attempt["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED_NOT_APPROVAL",
        )
        self.assertIn(
            "BLK_SYSTEM_276_RTM_BLK_LINK_DRIFT_COVERAGE_EXPIRED_APPROVE_ATTEMPT_RECORDED",
            expired_attempt["markers"],
        )
        self.assertEqual(expired_attempt["challenge_hash"], request_package._CANONICAL_CHALLENGE_273_HASH)
        self.assertEqual(expired_attempt["operator_reply_status"], "EXPIRED_CHALLENGE_NOT_APPROVAL")
        self.assertEqual(
            expired_attempt["evaluation_result"],
            "short_approve_seen_after_challenge_expiry_is_not_approval",
        )
        self.assertEqual(expired_attempt["evaluated_at"], _EXPIRED_APPROVE_EVALUATED_AT)
        self.assertFalse(expired_attempt["side_effects"]["approval_captured"])
        self.assertFalse(expired_attempt["side_effects"]["run_id_reserved"])
        self.assertFalse(expired_attempt["side_effects"]["production_blk_link_execution"])
        self.assertRegex(expired_attempt["expired_attempt_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            expired_attempt["expired_attempt_hash"],
            refresh_package._CANONICAL_EXPIRED_ATTEMPT_276_HASH,
        )

        self.assertEqual(
            refresh_challenge["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        )
        self.assertIn(
            "BLK_SYSTEM_277_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_APPROVE_CHALLENGE_READY",
            refresh_challenge["markers"],
        )
        self.assertEqual(refresh_challenge["previous_challenge_hash"], expired_attempt["challenge_hash"])
        self.assertEqual(refresh_challenge["expired_attempt_hash"], expired_attempt["expired_attempt_hash"])
        self.assertEqual(refresh_challenge["operator_identity"], _OPERATOR_IDENTITY)
        self.assertEqual(refresh_challenge["short_approval_reply"], "Approve")
        self.assertEqual(refresh_challenge["issued_at"], _REFRESH_ISSUED_AT)
        self.assertEqual(refresh_challenge["expires_at"], _REFRESH_EXPIRES_AT)
        self.assertTrue(refresh_challenge["challenge_rules"]["expired_prior_challenge_required"])
        self.assertFalse(refresh_challenge["side_effects"]["approval_captured"])
        self.assertFalse(refresh_challenge["side_effects"]["run_id_consumed"])
        self.assertFalse(refresh_challenge["side_effects"]["rtm_generation"])
        self.assertFalse(refresh_challenge["side_effects"]["production_blk_link_execution"])
        self.assertRegex(refresh_challenge["refresh_challenge_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            refresh_challenge["refresh_challenge_hash"],
            refresh_package._CANONICAL_REFRESH_CHALLENGE_277_HASH,
        )

        self.assertEqual(
            reconciliation["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        )
        self.assertIn(
            "BLK_SYSTEM_278_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESH_CHALLENGE_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED",
        )
        self.assertFalse(reconciliation["side_effects"]["approval_captured"])
        self.assertFalse(reconciliation["side_effects"]["run_id_reserved"])
        self.assertFalse(reconciliation["side_effects"]["coverage_truth"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            reconciliation["reconciliation_hash"],
            refresh_package._CANONICAL_RECONCILIATION_278_HASH,
        )

    def test_attempt_capture_fails_closed_if_approve_was_not_after_challenge_expiry(self):
        with self.assertRaisesRegex(ValueError, "expired challenge"):
            refresh_package.record_expired_rtm_blk_link_drift_coverage_approve_attempt_276(
                _challenge_273(),
                operator_reply="Approve",
                operator_identity=_OPERATOR_IDENTITY,
                evaluated_at="2026-05-20T08:27:00+10:00",
            )

        with self.assertRaisesRegex(ValueError, "operator_reply forbidden authority wording"):
            refresh_package.record_expired_rtm_blk_link_drift_coverage_approve_attempt_276(
                _challenge_273(),
                operator_reply="Approve; productionBlkLinkExecutionAuthorized",
                operator_identity=_OPERATOR_IDENTITY,
                evaluated_at=_EXPIRED_APPROVE_EVALUATED_AT,
            )

    def test_refresh_challenge_rejects_forged_expired_attempts_and_unsafe_windows(self):
        expired_attempt = _expired_attempt_276()

        forged_bound = copy.deepcopy(expired_attempt)
        forged_bound["operator_reply_status"] = "BOUND_APPROVE_FOR_CHALLENGE"
        forged_bound["side_effects"]["short_approve_matched"] = True
        forged_bound["expired_attempt_hash"] = refresh_package._hash_package(
            {key: value for key, value in forged_bound.items() if key != "expired_attempt_hash"}
        )
        with self.assertRaisesRegex(ValueError, "operator_reply_status|side_effects|expired attempt"):
            refresh_package.build_rtm_blk_link_drift_coverage_refresh_challenge_277(
                forged_bound,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce=_REFRESH_NONCE,
                issued_at=_REFRESH_ISSUED_AT,
                expires_at=_REFRESH_EXPIRES_AT,
            )

        with self.assertRaisesRegex(ValueError, "issued_at must be after previous challenge expiry"):
            refresh_package.build_rtm_blk_link_drift_coverage_refresh_challenge_277(
                expired_attempt,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce=_REFRESH_NONCE,
                issued_at="2026-05-20T08:55:00+10:00",
                expires_at=_REFRESH_EXPIRES_AT,
            )

        with self.assertRaisesRegex(ValueError, "challenge_nonce|forbidden authority"):
            refresh_package.build_rtm_blk_link_drift_coverage_refresh_challenge_277(
                expired_attempt,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce="productionBlkLinkAuthorized",
                issued_at=_REFRESH_ISSUED_AT,
                expires_at=_REFRESH_EXPIRES_AT,
            )

        refresh_challenge = _refresh_challenge_277()
        tampered_challenge = copy.deepcopy(refresh_challenge)
        tampered_challenge["side_effects"]["approval_captured"] = True
        tampered_challenge["refresh_challenge_hash"] = refresh_package._hash_package(
            {key: value for key, value in tampered_challenge.items() if key != "refresh_challenge_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|forbidden authority"):
            refresh_package.reconcile_rtm_blk_link_drift_coverage_refresh_challenge_278(tampered_challenge)


if __name__ == "__main__":
    unittest.main()
