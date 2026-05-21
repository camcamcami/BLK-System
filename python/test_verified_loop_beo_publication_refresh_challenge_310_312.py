import copy
from datetime import datetime
import unittest
from unittest.mock import patch

from test_verified_loop_beo_publication_approval_request_306_309 import (
    _VALIDATION_NOW as _APPROVAL_REQUEST_NOW,
    _challenge_308,
    _review_reconciliation_305,
)
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_306_APPROVAL_REQUEST_HASH,
    EXPECTED_306_CHALLENGE_HASH,
    EXPECTED_308_CHALLENGE_RECORD_HASH,
    EXPECTED_309_RECONCILIATION_HASH,
    EXPECTED_OPERATOR_DISCORD_ID,
    reconcile_verified_loop_beo_publication_approval_request_309,
)
from verified_loop_beo_publication_refresh_challenge_310_312 import (
    EXPECTED_310_EXPIRED_ATTEMPT_HASH,
    EXPECTED_311_REFRESH_CHALLENGE_HASH,
    EXPECTED_312_RECONCILIATION_HASH,
    NEXT_FRONTIER_312,
    VerifiedLoopBeoPublicationRefreshChallengeValidationError,
    build_verified_loop_beo_publication_refreshed_approval_challenge_311,
    hash_package,
    reconcile_verified_loop_beo_publication_refreshed_challenge_312,
    record_expired_verified_loop_beo_publication_approval_attempt_310,
)

_OPERATOR_STATEMENT = "plan and execute the next blk-system sprint package"
_EXPIRED_EVALUATED_AT = "2026-05-21T14:25:00+10:00"
_REFRESH_ISSUED_AT = "2026-05-21T14:45:00+10:00"
_REFRESH_EXPIRES_AT = "2026-05-21T20:45:00+10:00"
_REFRESH_NONCE = "BEO-APPROVAL-REFRESH-NONCE-BLK-SYSTEM-311-001"


def _prior_309():
    with patch(
        "verified_loop_beo_publication_approval_request_306_309._validation_now",
        return_value=datetime.fromisoformat(_APPROVAL_REQUEST_NOW),
    ):
        review, request, contract, challenge = _challenge_308()
        reconciliation = reconcile_verified_loop_beo_publication_approval_request_309(
            contract,
            request,
            challenge,
            review,
        )
        return review, request, contract, challenge, reconciliation


def _expired_attempt_310():
    _review, _request, _contract, challenge, reconciliation = _prior_309()
    return record_expired_verified_loop_beo_publication_approval_attempt_310(
        challenge,
        reconciliation,
        operator_statement=_OPERATOR_STATEMENT,
        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
        evaluated_at=_EXPIRED_EVALUATED_AT,
    )


def _refresh_challenge_311():
    return build_verified_loop_beo_publication_refreshed_approval_challenge_311(
        _expired_attempt_310(),
        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
        challenge_nonce=_REFRESH_NONCE,
        issued_at=_REFRESH_ISSUED_AT,
        expires_at=_REFRESH_EXPIRES_AT,
    )


class VerifiedLoopBeoPublicationRefreshChallenge310To312Test(unittest.TestCase):
    def test_310_to_312_records_expired_generic_directive_and_reissues_bounded_challenge_without_authority(self):
        expired = _expired_attempt_310()
        challenge = _refresh_challenge_311()
        reconciliation = reconcile_verified_loop_beo_publication_refreshed_challenge_312(challenge)

        self.assertEqual(
            expired["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED_NOT_APPROVAL",
        )
        self.assertIn(
            "BLK_SYSTEM_310_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_EXPIRED_ATTEMPT_RECORDED",
            expired["markers"],
        )
        self.assertEqual(expired["approval_request_hash"], EXPECTED_306_APPROVAL_REQUEST_HASH)
        self.assertEqual(expired["prior_challenge_hash"], EXPECTED_306_CHALLENGE_HASH)
        self.assertEqual(expired["prior_challenge_record_hash"], EXPECTED_308_CHALLENGE_RECORD_HASH)
        self.assertEqual(expired["prior_reconciliation_hash"], EXPECTED_309_RECONCILIATION_HASH)
        self.assertEqual(expired["prior_challenge_expires_at"], "2026-05-21T13:00:00+10:00")
        self.assertEqual(expired["evaluated_at"], _EXPIRED_EVALUATED_AT)
        self.assertEqual(expired["operator_statement_status"], "EXPIRED_OR_UNBOUND_DIRECTIVE_NOT_APPROVAL")
        self.assertEqual(expired["operator_statement_classification"], "generic_sprint_directive_hash_only_not_approval")
        self.assertFalse(expired["side_effects"]["approval_captured"])
        self.assertFalse(expired["side_effects"]["run_id_reserved"])
        self.assertFalse(expired["side_effects"]["beo_publication"])
        self.assertEqual(expired["expired_attempt_hash"], EXPECTED_310_EXPIRED_ATTEMPT_HASH)

        self.assertEqual(
            challenge["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY_NOT_APPROVED",
        )
        self.assertIn(
            "BLK_SYSTEM_311_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_APPROVE_CHALLENGE_READY",
            challenge["markers"],
        )
        self.assertEqual(challenge["expired_attempt_hash"], expired["expired_attempt_hash"])
        self.assertEqual(challenge["operator_identity"]["discord_user_id"], EXPECTED_OPERATOR_DISCORD_ID)
        self.assertEqual(challenge["short_approval_reply"], "Approve")
        self.assertEqual(challenge["issued_at"], _REFRESH_ISSUED_AT)
        self.assertEqual(challenge["expires_at"], _REFRESH_EXPIRES_AT)
        self.assertTrue(challenge["challenge_rules"]["expired_prior_challenge_required"])
        self.assertFalse(challenge["side_effects"]["approval_captured"])
        self.assertFalse(challenge["side_effects"]["run_id_consumed"])
        self.assertFalse(challenge["side_effects"]["beo_publication"])
        self.assertEqual(challenge["refresh_challenge_hash"], EXPECTED_311_REFRESH_CHALLENGE_HASH)

        self.assertEqual(
            reconciliation["status"],
            "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED",
        )
        self.assertIn(
            "BLK_SYSTEM_312_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_REFRESH_CHALLENGE_RECONCILED",
            reconciliation["markers"],
        )
        self.assertEqual(reconciliation["next_frontier"], NEXT_FRONTIER_312)
        self.assertFalse(reconciliation["side_effects"]["approval_captured"])
        self.assertFalse(reconciliation["side_effects"]["run_id_reserved"])
        self.assertFalse(reconciliation["side_effects"]["beo_publication"])
        self.assertEqual(reconciliation["reconciliation_hash"], EXPECTED_312_RECONCILIATION_HASH)

    def test_310_rejects_live_prior_challenge_and_authority_laundering_statement(self):
        _review, _request, _contract, challenge, reconciliation = _prior_309()

        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationRefreshChallengeValidationError,
            "still live|not yet issued",
        ):
            record_expired_verified_loop_beo_publication_approval_attempt_310(
                challenge,
                reconciliation,
                operator_statement="Approve",
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                evaluated_at="2026-05-21T12:45:00+10:00",
            )

        for statement in [
            "execute next sprints is publication approval",
            "generic operator directive is publication approval",
            "beoPublicationAuthorized",
            "rtmGenerated",
            "docs%252Frequirements%252Factive",
        ]:
            with self.subTest(statement=statement):
                with self.assertRaisesRegex(
                    VerifiedLoopBeoPublicationRefreshChallengeValidationError,
                    "forbidden authority wording|protected",
                ):
                    record_expired_verified_loop_beo_publication_approval_attempt_310(
                        challenge,
                        reconciliation,
                        operator_statement=statement,
                        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                        evaluated_at=_EXPIRED_EVALUATED_AT,
                    )

    def test_311_rejects_forged_expired_attempts_unsafe_nonce_and_unsafe_windows(self):
        expired = _expired_attempt_310()

        forged = copy.deepcopy(expired)
        forged["operator_statement_status"] = "BOUND_APPROVE_FOR_CHALLENGE"
        forged["side_effects"]["approval_captured"] = True
        forged["expired_attempt_hash"] = hash_package(
            {key: value for key, value in forged.items() if key != "expired_attempt_hash"}
        )
        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationRefreshChallengeValidationError,
            "status|side_effects|canonical hash",
        ):
            build_verified_loop_beo_publication_refreshed_approval_challenge_311(
                forged,
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                challenge_nonce=_REFRESH_NONCE,
                issued_at=_REFRESH_ISSUED_AT,
                expires_at=_REFRESH_EXPIRES_AT,
            )

        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationRefreshChallengeValidationError,
            "issued_at must be after prior challenge expiry",
        ):
            build_verified_loop_beo_publication_refreshed_approval_challenge_311(
                expired,
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                challenge_nonce=_REFRESH_NONCE,
                issued_at="2026-05-21T12:59:00+10:00",
                expires_at=_REFRESH_EXPIRES_AT,
            )

        for nonce, expected_error in [
            ("BEO-APPROVAL-REFRESH-NONCE-BLK-SYSTEM-311-PUBLISHED", "forbidden authority segment"),
            ("BEO-APPROVAL-REFRESH-NONCE-BLK-SYSTEM-311-002", "canonical value mismatch"),
        ]:
            with self.subTest(nonce=nonce):
                with self.assertRaisesRegex(VerifiedLoopBeoPublicationRefreshChallengeValidationError, expected_error):
                    build_verified_loop_beo_publication_refreshed_approval_challenge_311(
                        expired,
                        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                        challenge_nonce=nonce,
                        issued_at=_REFRESH_ISSUED_AT,
                        expires_at=_REFRESH_EXPIRES_AT,
                    )

        with self.assertRaisesRegex(VerifiedLoopBeoPublicationRefreshChallengeValidationError, "refresh window exceeds maximum TTL"):
            build_verified_loop_beo_publication_refreshed_approval_challenge_311(
                expired,
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                challenge_nonce=_REFRESH_NONCE,
                issued_at=_REFRESH_ISSUED_AT,
                expires_at="2026-05-22T14:46:00+10:00",
            )

    def test_312_rejects_tampered_challenge_and_publication_side_effects(self):
        challenge = _refresh_challenge_311()
        tampered = copy.deepcopy(challenge)
        tampered["side_effects"]["beo_publication"] = True
        tampered["refresh_challenge_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "refresh_challenge_hash"}
        )
        with self.assertRaisesRegex(
            VerifiedLoopBeoPublicationRefreshChallengeValidationError,
            "side_effects|canonical hash|beo_publication",
        ):
            reconcile_verified_loop_beo_publication_refreshed_challenge_312(tampered)

        forged_hash = copy.deepcopy(challenge)
        forged_hash["refresh_challenge_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationRefreshChallengeValidationError, "hash mismatch|canonical hash"):
            reconcile_verified_loop_beo_publication_refreshed_challenge_312(forged_hash)


if __name__ == "__main__":
    unittest.main()
