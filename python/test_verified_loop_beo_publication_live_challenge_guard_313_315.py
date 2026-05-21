import copy
import unittest

from test_verified_loop_beo_publication_refresh_challenge_310_312 import (
    _refresh_challenge_311,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_OPERATOR_DISCORD_ID,
)
from verified_loop_beo_publication_live_challenge_guard_313_315 import (
    EXPECTED_313_LIVE_DIRECTIVE_HASH,
    EXPECTED_314_SHORT_APPROVE_GUARD_HASH,
    EXPECTED_315_RECONCILIATION_HASH,
    NEXT_FRONTIER_315,
    VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
    build_verified_loop_beo_publication_live_short_approve_guard_314,
    hash_package,
    reconcile_verified_loop_beo_publication_live_challenge_guard_315,
    record_live_verified_loop_beo_publication_non_approval_directive_313,
)
from verified_loop_beo_publication_refresh_challenge_310_312 import (
    EXPECTED_311_REFRESH_CHALLENGE_HASH,
    EXPECTED_312_RECONCILIATION_HASH,
    reconcile_verified_loop_beo_publication_refreshed_challenge_312,
)

_OPERATOR_STATEMENT = "plan and execute the next blk-system sprint package"
_LIVE_OBSERVED_AT = "2026-05-21T17:31:38+10:00"


def _refresh_reconciliation_312():
    return reconcile_verified_loop_beo_publication_refreshed_challenge_312(
        _refresh_challenge_311(),
    )


def _live_directive_313():
    return record_live_verified_loop_beo_publication_non_approval_directive_313(
        _refresh_challenge_311(),
        _refresh_reconciliation_312(),
        operator_statement=_OPERATOR_STATEMENT,
        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
        observed_at=_LIVE_OBSERVED_AT,
    )


def _short_approve_guard_314():
    return build_verified_loop_beo_publication_live_short_approve_guard_314(
        _live_directive_313(),
        _refresh_challenge_311(),
    )


class VerifiedLoopBeoPublicationLiveChallengeGuard313To315Test(unittest.TestCase):
    def test_313_to_315_records_live_generic_directive_without_capturing_approval_or_consuming_challenge(self):
        directive = _live_directive_313()
        guard = _short_approve_guard_314()
        reconciliation = reconcile_verified_loop_beo_publication_live_challenge_guard_315(guard)

        self.assertEqual(
            directive["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED_NOT_APPROVAL",
        )
        self.assertIn(
            "BLK_SYSTEM_313_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_GENERIC_DIRECTIVE_RECORDED",
            directive["markers"],
        )
        self.assertEqual(directive["refresh_challenge_hash"], EXPECTED_311_REFRESH_CHALLENGE_HASH)
        self.assertEqual(directive["refresh_reconciliation_hash"], EXPECTED_312_RECONCILIATION_HASH)
        self.assertEqual(directive["observed_at"], _LIVE_OBSERVED_AT)
        self.assertEqual(directive["challenge_issued_at"], "2026-05-21T14:45:00+10:00")
        self.assertEqual(directive["challenge_expires_at"], "2026-05-21T20:45:00+10:00")
        self.assertEqual(directive["operator_statement_classification"], "live_generic_sprint_directive_not_approval")
        self.assertFalse(directive["statement_matches_short_approve"])
        self.assertTrue(directive["challenge_remains_live"])
        self.assertFalse(directive["side_effects"]["approval_captured"])
        self.assertFalse(directive["side_effects"]["challenge_consumed"])
        self.assertFalse(directive["side_effects"]["beo_publication"])
        self.assertEqual(directive["live_directive_hash"], EXPECTED_313_LIVE_DIRECTIVE_HASH)

        self.assertEqual(
            guard["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_SHORT_APPROVE_GUARD_RECORDED_NOT_APPROVED",
        )
        self.assertIn(
            "BLK_SYSTEM_314_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_SHORT_APPROVE_GUARD_READY",
            guard["markers"],
        )
        self.assertEqual(guard["live_directive_hash"], directive["live_directive_hash"])
        self.assertEqual(guard["guard_result"], "NO_EXACT_SHORT_APPROVE_MATCH")
        self.assertFalse(guard["capture_allowed"])
        self.assertTrue(guard["future_capture_package_required"])
        self.assertFalse(guard["side_effects"]["approval_captured"])
        self.assertFalse(guard["side_effects"]["run_id_reserved"])
        self.assertFalse(guard["side_effects"]["beo_publication"])
        self.assertEqual(guard["short_approve_guard_hash"], EXPECTED_314_SHORT_APPROVE_GUARD_HASH)

        self.assertEqual(
            reconciliation["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED_APPROVAL_REQUIRED",
        )
        self.assertIn(
            "BLK_SYSTEM_315_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_LIVE_REFRESH_NON_APPROVAL_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER_315)
        self.assertFalse(reconciliation["side_effects"]["approval_captured"])
        self.assertFalse(reconciliation["side_effects"]["challenge_consumed"])
        self.assertFalse(reconciliation["side_effects"]["beo_publication"])
        self.assertEqual(reconciliation["reconciliation_hash"], EXPECTED_315_RECONCILIATION_HASH)

    def test_313_rejects_exact_live_approve_and_out_of_window_statements(self):
        challenge = _refresh_challenge_311()
        reconciliation = _refresh_reconciliation_312()

        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
            "approval-capture package",
        ):
            record_live_verified_loop_beo_publication_non_approval_directive_313(
                challenge,
                reconciliation,
                operator_statement="Approve",
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                observed_at=_LIVE_OBSERVED_AT,
            )

        for observed_at, expected_error in [
            ("2026-05-21T14:44:59+10:00", "not yet live"),
            ("2026-05-21T20:45:00+10:00", "no longer live"),
        ]:
            with self.subTest(observed_at=observed_at):
                with self.assertRaisesRegex(
                    VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
                    expected_error,
                ):
                    record_live_verified_loop_beo_publication_non_approval_directive_313(
                        challenge,
                        reconciliation,
                        operator_statement=_OPERATOR_STATEMENT,
                        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                        observed_at=observed_at,
                    )

    def test_314_rejects_forged_directive_hashes_and_publication_side_effects(self):
        directive = _live_directive_313()
        forged = copy.deepcopy(directive)
        forged["statement_matches_short_approve"] = True
        forged["side_effects"]["approval_captured"] = True
        forged["live_directive_hash"] = hash_package(
            {key: value for key, value in forged.items() if key != "live_directive_hash"}
        )

        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
            "statement match|side_effects|canonical hash",
        ):
            build_verified_loop_beo_publication_live_short_approve_guard_314(
                forged,
                _refresh_challenge_311(),
            )

        mismatch = copy.deepcopy(_refresh_challenge_311())
        mismatch["refresh_challenge_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
            "hash mismatch|canonical hash",
        ):
            build_verified_loop_beo_publication_live_short_approve_guard_314(
                directive,
                mismatch,
            )

    def test_315_rejects_tampered_guard_and_captured_approval_side_effects(self):
        guard = _short_approve_guard_314()
        tampered = copy.deepcopy(guard)
        tampered["capture_allowed"] = True
        tampered["side_effects"]["approval_captured"] = True
        tampered["side_effects"]["beo_publication"] = True
        tampered["short_approve_guard_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "short_approve_guard_hash"}
        )

        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationLiveChallengeGuardValidationError,
            "capture|side_effects|canonical hash|beo_publication",
        ):
            reconcile_verified_loop_beo_publication_live_challenge_guard_315(tampered)


if __name__ == "__main__":
    unittest.main()
