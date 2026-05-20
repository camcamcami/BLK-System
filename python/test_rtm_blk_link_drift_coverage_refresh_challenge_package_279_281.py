import copy
import unittest

from test_rtm_blk_link_drift_coverage_request_package_272_275 import _OPERATOR_IDENTITY
from test_rtm_blk_link_drift_coverage_refresh_challenge_package_276_278 import _refresh_challenge_277
import rtm_blk_link_drift_coverage_refresh_challenge_package_276_278 as prior_refresh
import rtm_blk_link_drift_coverage_refresh_challenge_package_279_281 as refresh_again


_LATE_GENERIC_APPROVAL_EVALUATED_AT = "2026-05-20T17:37:50+10:00"
_SECOND_REFRESH_ISSUED_AT = "2026-05-20T17:39:00+10:00"
_SECOND_REFRESH_EXPIRES_AT = "2026-05-20T18:39:00+10:00"
_SECOND_REFRESH_NONCE = "BLK-SYSTEM-280-RTM-BLK-LINK-REFRESH-002"
_OPERATOR_DIRECTIVE = "you have my approval"


def _expired_refresh_attempt_279():
    return refresh_again.record_expired_rtm_blk_link_drift_coverage_refresh_attempt_279(
        _refresh_challenge_277(),
        operator_statement=_OPERATOR_DIRECTIVE,
        operator_identity=_OPERATOR_IDENTITY,
        evaluated_at=_LATE_GENERIC_APPROVAL_EVALUATED_AT,
    )


def _second_refresh_challenge_280():
    return refresh_again.build_rtm_blk_link_drift_coverage_second_refresh_challenge_280(
        _expired_refresh_attempt_279(),
        operator_identity=_OPERATOR_IDENTITY,
        challenge_nonce=_SECOND_REFRESH_NONCE,
        issued_at=_SECOND_REFRESH_ISSUED_AT,
        expires_at=_SECOND_REFRESH_EXPIRES_AT,
    )


class RtmBlkLinkDriftCoverageRefreshChallenge279To281Test(unittest.TestCase):
    def test_279_to_281_records_expired_refresh_and_issues_fresh_bound_challenge_without_authority(self):
        expired_refresh_attempt = _expired_refresh_attempt_279()
        second_refresh_challenge = _second_refresh_challenge_280()
        reconciliation = refresh_again.reconcile_rtm_blk_link_drift_coverage_second_refresh_challenge_281(
            second_refresh_challenge
        )

        self.assertEqual(
            expired_refresh_attempt["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL",
        )
        self.assertIn(
            "BLK_SYSTEM_279_RTM_BLK_LINK_DRIFT_COVERAGE_REFRESHED_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
            expired_refresh_attempt["markers"],
        )
        self.assertEqual(
            expired_refresh_attempt["refresh_challenge_hash"],
            prior_refresh._CANONICAL_REFRESH_CHALLENGE_277_HASH,
        )
        self.assertEqual(
            expired_refresh_attempt["operator_statement_status"],
            "EXPIRED_OR_UNBOUND_REFRESH_CHALLENGE_NOT_APPROVAL",
        )
        self.assertEqual(expired_refresh_attempt["evaluated_at"], _LATE_GENERIC_APPROVAL_EVALUATED_AT)
        self.assertFalse(expired_refresh_attempt["side_effects"]["approval_captured"])
        self.assertFalse(expired_refresh_attempt["side_effects"]["run_id_reserved"])
        self.assertFalse(expired_refresh_attempt["side_effects"]["production_blk_link_execution"])
        self.assertIsNotNone(refresh_again._CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH)
        self.assertRegex(expired_refresh_attempt["expired_refresh_attempt_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            expired_refresh_attempt["expired_refresh_attempt_hash"],
            refresh_again._CANONICAL_EXPIRED_REFRESH_ATTEMPT_279_HASH,
        )

        self.assertEqual(
            second_refresh_challenge["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        )
        self.assertIn(
            "BLK_SYSTEM_280_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_APPROVE_CHALLENGE_READY",
            second_refresh_challenge["markers"],
        )
        self.assertEqual(
            second_refresh_challenge["previous_refresh_challenge_hash"],
            expired_refresh_attempt["refresh_challenge_hash"],
        )
        self.assertEqual(
            second_refresh_challenge["expired_refresh_attempt_hash"],
            expired_refresh_attempt["expired_refresh_attempt_hash"],
        )
        self.assertEqual(second_refresh_challenge["short_approval_reply"], "Approve")
        self.assertEqual(second_refresh_challenge["issued_at"], _SECOND_REFRESH_ISSUED_AT)
        self.assertEqual(second_refresh_challenge["expires_at"], _SECOND_REFRESH_EXPIRES_AT)
        self.assertTrue(second_refresh_challenge["challenge_rules"]["expired_prior_refresh_required"])
        self.assertFalse(second_refresh_challenge["side_effects"]["approval_captured"])
        self.assertFalse(second_refresh_challenge["side_effects"]["run_id_consumed"])
        self.assertFalse(second_refresh_challenge["side_effects"]["rtm_generation"])
        self.assertFalse(second_refresh_challenge["side_effects"]["coverage_truth"])
        self.assertIsNotNone(refresh_again._CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH)
        self.assertEqual(
            second_refresh_challenge["second_refresh_challenge_hash"],
            refresh_again._CANONICAL_SECOND_REFRESH_CHALLENGE_280_HASH,
        )

        self.assertEqual(
            reconciliation["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        )
        self.assertIn(
            "BLK_SYSTEM_281_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESH_CHALLENGE_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_SECOND_REFRESHED_BOUND_APPROVE_REQUIRED_NOT_GRANTED",
        )
        self.assertFalse(reconciliation["side_effects"]["approval_captured"])
        self.assertFalse(reconciliation["side_effects"]["run_id_reserved"])
        self.assertFalse(reconciliation["side_effects"]["production_blk_link_execution"])
        self.assertIsNotNone(refresh_again._CANONICAL_RECONCILIATION_281_HASH)
        self.assertEqual(
            reconciliation["reconciliation_hash"],
            refresh_again._CANONICAL_RECONCILIATION_281_HASH,
        )

    def test_expired_refresh_attempt_requires_expired_or_unbound_statement_not_live_bound_approve(self):
        with self.assertRaisesRegex(ValueError, "challenge was still live"):
            refresh_again.record_expired_rtm_blk_link_drift_coverage_refresh_attempt_279(
                _refresh_challenge_277(),
                operator_statement="Approve",
                operator_identity=_OPERATOR_IDENTITY,
                evaluated_at="2026-05-20T10:55:00+10:00",
            )

        expired_refresh_attempt = _expired_refresh_attempt_279()
        forged = copy.deepcopy(expired_refresh_attempt)
        forged["operator_statement_status"] = "BOUND_APPROVE_FOR_REFRESH_CHALLENGE"
        forged["side_effects"]["approval_captured"] = True
        forged["expired_refresh_attempt_hash"] = refresh_again._hash_package(
            {key: value for key, value in forged.items() if key != "expired_refresh_attempt_hash"}
        )
        with self.assertRaisesRegex(ValueError, "operator_statement_status|side_effects|canonical BLK-SYSTEM-279"):
            refresh_again.build_rtm_blk_link_drift_coverage_second_refresh_challenge_280(
                forged,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce=_SECOND_REFRESH_NONCE,
                issued_at=_SECOND_REFRESH_ISSUED_AT,
                expires_at=_SECOND_REFRESH_EXPIRES_AT,
            )

    def test_second_refresh_rejects_unsafe_windows_and_authority_laundering(self):
        expired_refresh_attempt = _expired_refresh_attempt_279()

        with self.assertRaisesRegex(ValueError, "issued_at must be after previous refresh challenge expiry"):
            refresh_again.build_rtm_blk_link_drift_coverage_second_refresh_challenge_280(
                expired_refresh_attempt,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce=_SECOND_REFRESH_NONCE,
                issued_at="2026-05-20T11:20:00+10:00",
                expires_at=_SECOND_REFRESH_EXPIRES_AT,
            )

        with self.assertRaisesRegex(ValueError, "challenge_nonce|forbidden authority"):
            refresh_again.build_rtm_blk_link_drift_coverage_second_refresh_challenge_280(
                expired_refresh_attempt,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce="coverageTruthAuthorized",
                issued_at=_SECOND_REFRESH_ISSUED_AT,
                expires_at=_SECOND_REFRESH_EXPIRES_AT,
            )

        second_refresh_challenge = _second_refresh_challenge_280()
        tampered_challenge = copy.deepcopy(second_refresh_challenge)
        tampered_challenge["side_effects"]["run_id_reserved"] = True
        tampered_challenge["second_refresh_challenge_hash"] = refresh_again._hash_package(
            {key: value for key, value in tampered_challenge.items() if key != "second_refresh_challenge_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|canonical BLK-SYSTEM-280"):
            refresh_again.reconcile_rtm_blk_link_drift_coverage_second_refresh_challenge_281(tampered_challenge)


if __name__ == "__main__":
    unittest.main()
