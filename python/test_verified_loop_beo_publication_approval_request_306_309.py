import copy
from datetime import datetime
import unittest
from pathlib import Path
from unittest.mock import patch

from test_verified_loop_beo_publication_review_302_305 import _record_304, _VALIDATION_NOW as _REVIEW_NOW
from verified_loop_beo_publication_review_302_305 import reconcile_verified_loop_beo_publication_review_305
from verified_loop_beo_publication_approval_request_306_309 import (
    EXPECTED_306_APPROVAL_REQUEST_HASH,
    EXPECTED_307_CONTRACT_HASH,
    EXPECTED_308_CHALLENGE_RECORD_HASH,
    EXPECTED_309_RECONCILIATION_HASH,
    EXPECTED_OPERATOR_DISCORD_ID,
    NEXT_FRONTIER_309,
    VerifiedLoopBeoPublicationApprovalRequestValidationError,
    build_verified_loop_beo_publication_approval_request_306,
    build_verified_loop_beo_publication_approval_request_contract_307,
    hash_package,
    record_verified_loop_beo_publication_approval_challenge_308,
    reconcile_verified_loop_beo_publication_approval_request_309,
    validate_verified_loop_beo_publication_approval_challenge_308,
    validate_verified_loop_beo_publication_approval_request_306,
    validate_verified_loop_beo_publication_approval_request_contract_307,
    validate_verified_loop_beo_publication_approval_request_reconciliation_309,
)

ROOT = Path(__file__).resolve().parents[1]
BLK128 = ROOT / "docs" / "BLK-128_verified-loop-beo-publication-approval-request-contract.md"

_REQUEST_ID = "BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-001"
_NONCE = "BEO-APPROVAL-NONCE-BLK-SYSTEM-306-001"
_REQUESTED_AT = "2026-05-21T12:30:00+10:00"
_EXPIRES_AT = "2026-05-21T13:00:00+10:00"
_RECORDED_AT = "2026-05-21T12:35:00+10:00"
_VALIDATION_NOW = "2026-05-21T12:35:00+10:00"


def _review_reconciliation_305():
    with patch(
        "verified_loop_beo_publication_review_302_305._validation_now",
        return_value=datetime.fromisoformat(_REVIEW_NOW),
    ):
        verification, beo, request, contract, record = _record_304()
        return reconcile_verified_loop_beo_publication_review_305(
            contract,
            request,
            record,
            verification,
            beo,
        )


def _request_306():
    review = _review_reconciliation_305()
    request = build_verified_loop_beo_publication_approval_request_306(
        review,
        request_id=_REQUEST_ID,
        requested_at=_REQUESTED_AT,
        expires_at=_EXPIRES_AT,
        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
        challenge_nonce=_NONCE,
    )
    return review, request


def _contract_307():
    review, request = _request_306()
    contract = build_verified_loop_beo_publication_approval_request_contract_307(request, review)
    return review, request, contract


def _challenge_308():
    review, request, contract = _contract_307()
    challenge = record_verified_loop_beo_publication_approval_challenge_308(
        contract,
        request,
        review,
        recorded_at=_RECORDED_AT,
    )
    return review, request, contract, challenge


class VerifiedLoopBeoPublicationApprovalRequest306To309Test(unittest.TestCase):
    def setUp(self):
        self._now_patch = patch(
            "verified_loop_beo_publication_approval_request_306_309._validation_now",
            return_value=datetime.fromisoformat(_VALIDATION_NOW),
        )
        self._now_patch.start()
        self.addCleanup(self._now_patch.stop)

    def test_306_to_309_package_prepares_exact_approval_request_without_capture_or_publication(self):
        review, request, contract, challenge = _challenge_308()
        final = reconcile_verified_loop_beo_publication_approval_request_309(
            contract,
            request,
            challenge,
            review,
        )

        self.assertEqual(request["status"], "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_306_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY", request["markers"])
        self.assertEqual(request["review_reconciliation_hash"], review["reconciliation_hash"])
        self.assertEqual(request["approval_request_hash"], EXPECTED_306_APPROVAL_REQUEST_HASH)
        self.assertEqual(request["operator_identity"]["discord_user_id"], EXPECTED_OPERATOR_DISCORD_ID)
        self.assertEqual(request["challenge"]["required_reply"], "Approve")
        self.assertRegex(request["challenge"]["required_reply_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertFalse(request["challenge"]["short_approve_is_approval_now"])
        self.assertFalse(request["side_effects"]["approval_captured"])
        self.assertFalse(request["side_effects"]["run_id_reserved"])
        self.assertFalse(request["side_effects"]["beo_publication"])

        self.assertEqual(contract["status"], "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY")
        self.assertEqual(contract["contract_hash"], EXPECTED_307_CONTRACT_HASH)
        self.assertIn("BLK_SYSTEM_307_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_CONTRACT_READY", contract["markers"])
        self.assertTrue(contract["approval_capture_rules"]["exact_request_hash_required"])
        self.assertTrue(contract["approval_capture_rules"]["exact_operator_identity_required"])
        self.assertFalse(contract["approval_capture_rules"]["capture_allowed_in_this_package"])
        self.assertFalse(contract["execution_prerequisites"]["run_id_reserved_by_request"])
        self.assertFalse(contract["execution_prerequisites"]["publication_execution_allowed_by_request"])

        self.assertEqual(challenge["status"], "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED_NOT_APPROVED")
        self.assertEqual(challenge["challenge_record_hash"], EXPECTED_308_CHALLENGE_RECORD_HASH)
        self.assertIn("BLK_SYSTEM_308_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_CHALLENGE_RECORDED", challenge["markers"])
        self.assertEqual(challenge["approval_state"], "PENDING_NOT_CAPTURED")
        self.assertFalse(challenge["approval_captured"])
        self.assertFalse(challenge["publication_execution_ready"])
        self.assertFalse(challenge["side_effects"]["beo_closeout_execution"])

        self.assertEqual(final["status"], "EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED")
        self.assertEqual(final["reconciliation_hash"], EXPECTED_309_RECONCILIATION_HASH)
        self.assertIn("BLK_SYSTEM_309_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED", final["markers"])
        self.assertEqual(final["next_frontier"], NEXT_FRONTIER_309)
        self.assertEqual(final["reconciled_state"], "verified_loop_beo_publication_approval_request_ready_not_granted")
        self.assertFalse(final["side_effects"]["approval_captured"])
        self.assertFalse(final["side_effects"]["run_id_consumed"])
        self.assertFalse(final["side_effects"]["beo_publication"])
        self.assertFalse(final["side_effects"]["target_source_git_mutation"])
        self.assertRegex(final["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

        self.assertEqual(
            validate_verified_loop_beo_publication_approval_request_reconciliation_309(
                final,
                contract,
                request,
                challenge,
                review,
            ),
            final,
        )

    def test_306_request_pins_canonical_305_review_hash_not_self_consistent_rehash(self):
        review = _review_reconciliation_305()
        request = build_verified_loop_beo_publication_approval_request_306(
            review,
            request_id=_REQUEST_ID,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            challenge_nonce=_NONCE,
        )
        self.assertEqual(validate_verified_loop_beo_publication_approval_request_306(request, review), request)

        forged_review = copy.deepcopy(review)
        forged_review["review_result"] = "BLOCKED_BY_REVIEW_GAP"
        forged_review["reconciliation_hash"] = hash_package(
            {key: value for key, value in forged_review.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "BLK-SYSTEM-305|canonical"):
            build_verified_loop_beo_publication_approval_request_306(
                forged_review,
                request_id="BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-FORGED",
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                challenge_nonce="BEO-APPROVAL-NONCE-BLK-SYSTEM-306-FORGED",
            )

    def test_306_rejects_noncanonical_or_nonlive_request_windows(self):
        review, request = _request_306()

        with patch(
            "verified_loop_beo_publication_approval_request_306_309._validation_now",
            return_value=datetime.fromisoformat("2026-05-21T12:00:00+10:00"),
        ):
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "not yet live"):
                validate_verified_loop_beo_publication_approval_request_306(request, review)

        with patch(
            "verified_loop_beo_publication_approval_request_306_309._validation_now",
            return_value=datetime.fromisoformat(_EXPIRES_AT),
        ):
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "expired|stale"):
                validate_verified_loop_beo_publication_approval_request_306(request, review)

        noncanonical = copy.deepcopy(request)
        noncanonical["requested_at"] = "2026-01-01T00:00:00+10:00"
        noncanonical["expires_at"] = "2026-12-31T00:00:00+10:00"
        noncanonical["challenge"]["requested_at"] = noncanonical["requested_at"]
        noncanonical["challenge"]["expires_at"] = noncanonical["expires_at"]
        noncanonical["challenge"]["challenge_hash"] = hash_package(
            {key: value for key, value in noncanonical["challenge"].items() if key != "challenge_hash"}
        )
        noncanonical["expired"] = False
        noncanonical["approval_request_hash"] = hash_package(
            {key: value for key, value in noncanonical.items() if key != "approval_request_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "canonical value mismatch|maximum TTL"):
            validate_verified_loop_beo_publication_approval_request_306(noncanonical, review)

        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "after requested_at"):
            build_verified_loop_beo_publication_approval_request_306(
                review,
                request_id=_REQUEST_ID,
                requested_at=_EXPIRES_AT,
                expires_at=_REQUESTED_AT,
                operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                challenge_nonce=_NONCE,
            )

    def test_challenge_artifact_requires_exact_operator_identity_and_short_reply_binding_without_approval(self):
        review, request, contract, challenge = _challenge_308()
        self.assertEqual(validate_verified_loop_beo_publication_approval_challenge_308(challenge, contract, request, review), challenge)

        forged_operator = copy.deepcopy(request)
        forged_operator["operator_identity"]["discord_user_id"] = "6842351780837458190"
        forged_operator["approval_request_hash"] = hash_package(
            {key: value for key, value in forged_operator.items() if key != "approval_request_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "operator"):
            validate_verified_loop_beo_publication_approval_request_306(forged_operator, review)

        generic_reply = copy.deepcopy(challenge)
        generic_reply["approval_state"] = "APPROVED"
        generic_reply["approval_captured"] = True
        generic_reply["challenge_record_hash"] = hash_package(
            {key: value for key, value in generic_reply.items() if key != "challenge_record_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "approval|captured"):
            validate_verified_loop_beo_publication_approval_challenge_308(generic_reply, contract, request, review)

    def test_free_text_and_nested_fields_reject_publication_authority_laundering(self):
        review, request, contract, challenge = _challenge_308()
        for note in [
            "Approve means BEO publication authorized",
            "approval request grants publication authority",
            "operator approval will reserve run id now",
            "approved for publication; signer reused; ledger appended",
            "read docs%252Factive protected body before publication",
        ]:
            bad_request = copy.deepcopy(request)
            bad_request["request_notes"] = note
            bad_request["approval_request_hash"] = hash_package(
                {key: value for key, value in bad_request.items() if key != "approval_request_hash"}
            )
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "unsupported|forbidden"):
                validate_verified_loop_beo_publication_approval_request_306(bad_request, review)

            bad_challenge = copy.deepcopy(challenge)
            bad_challenge["operator_instruction"] = note
            bad_challenge["challenge_record_hash"] = hash_package(
                {key: value for key, value in bad_challenge.items() if key != "challenge_record_hash"}
            )
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "unsupported|forbidden"):
                validate_verified_loop_beo_publication_approval_challenge_308(bad_challenge, contract, request, review)

    def test_exact_ids_reject_authority_segments_and_unicode_operator_digits(self):
        review = _review_reconciliation_305()
        for request_id, nonce, expected_error in [
            ("BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-APPROVED", _NONCE, "forbidden authority segment"),
            ("BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-APPROVED1", _NONCE, "forbidden authority segment"),
            (_REQUEST_ID, "BEO-APPROVAL-NONCE-BLK-SYSTEM-306-PUBLISHED1", "forbidden authority segment"),
            ("BEO-APPROVAL-REQUEST-BLK-SYSTEM-306-002", _NONCE, "canonical value mismatch"),
        ]:
            with self.subTest(request_id=request_id, nonce=nonce):
                with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, expected_error):
                    build_verified_loop_beo_publication_approval_request_306(
                        review,
                        request_id=request_id,
                        requested_at=_REQUESTED_AT,
                        expires_at=_EXPIRES_AT,
                        operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
                        challenge_nonce=nonce,
                    )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationApprovalRequestValidationError, "ASCII digits"):
            build_verified_loop_beo_publication_approval_request_306(
                review,
                request_id=_REQUEST_ID,
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
                operator_discord_id="６８４２３５１７８０８３７４５８１９",
                challenge_nonce=_NONCE,
            )

    def test_builders_return_defensive_copies(self):
        review = _review_reconciliation_305()
        request = build_verified_loop_beo_publication_approval_request_306(
            review,
            request_id=_REQUEST_ID,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
            operator_discord_id=EXPECTED_OPERATOR_DISCORD_ID,
            challenge_nonce=_NONCE,
        )
        review["review_result"] = "BLOCKED_BY_REVIEW_GAP"
        self.assertEqual(request["review_reconciliation_hash"], "sha256:02a3f5dc842961419965af4bb8f4e5c827a300c6207582d16f9e20cf7416a219")

        saved_hash = request["approval_request_hash"]
        returned = validate_verified_loop_beo_publication_approval_request_306(request, _review_reconciliation_305())
        request["operator_identity"]["discord_user_id"] = "000"
        self.assertEqual(returned["operator_identity"]["discord_user_id"], EXPECTED_OPERATOR_DISCORD_ID)
        self.assertEqual(returned["approval_request_hash"], saved_hash)

    def test_contract_document_exists_and_preserves_request_only_boundary(self):
        text = BLK128.read_text()
        for marker in [
            "BLK-128",
            "BLK_SYSTEM_306_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_READY",
            "BLK_SYSTEM_309_EXACT_VERIFIED_LOOP_BEO_PUBLICATION_APPROVAL_REQUEST_RECONCILED",
            NEXT_FRONTIER_309,
            "no approval capture",
            "no run-ID reservation or consumption",
            "no BEO closeout execution",
            "no BEO publication",
            "no RTM generation",
            "no production `blk-link`",
            "no protected-body access",
            "no target/source/Git mutation",
            EXPECTED_306_APPROVAL_REQUEST_HASH,
            EXPECTED_307_CONTRACT_HASH,
            EXPECTED_308_CHALLENGE_RECORD_HASH,
            EXPECTED_309_RECONCILIATION_HASH,
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
