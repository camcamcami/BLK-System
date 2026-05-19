import copy
import unittest

from test_exact_beo_publication_execution_package_269_271 import (
    _OPERATOR_IDENTITY,
    _execution_270,
)
import exact_beo_publication_execution_package_269_271 as beo_execution
import rtm_blk_link_drift_coverage_request_package_272_275 as request_package


_REQUESTED_AT = "2026-05-20T08:25:00+10:00"
_REQUEST_EXPIRES_AT = "2026-05-20T09:25:00+10:00"
_ISSUED_AT = "2026-05-20T08:26:00+10:00"
_CHALLENGE_EXPIRES_AT = "2026-05-20T08:56:00+10:00"
_EVALUATED_AT = "2026-05-20T08:27:00+10:00"
_CHALLENGE_NONCE = "BLK-SYSTEM-273-RTM-BLK-LINK-CHALLENGE-001"


def _reconciliation_271():
    return beo_execution.reconcile_exact_beo_publication_finality_271(_execution_270())


def _request_272():
    return request_package.build_rtm_blk_link_drift_coverage_request_272(
        _reconciliation_271(),
        operator_identity=_OPERATOR_IDENTITY,
        requested_at=_REQUESTED_AT,
        expires_at=_REQUEST_EXPIRES_AT,
    )


def _challenge_273():
    return request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
        _request_272(),
        operator_identity=_OPERATOR_IDENTITY,
        challenge_nonce=_CHALLENGE_NONCE,
        issued_at=_ISSUED_AT,
        expires_at=_CHALLENGE_EXPIRES_AT,
    )


def _blocked_preflight_274():
    return request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
        _challenge_273(),
        operator_reply="plan and execute the next blk-system sprint package",
        operator_identity=_OPERATOR_IDENTITY,
        evaluated_at=_EVALUATED_AT,
    )


class RtmBlkLinkDriftCoverageRequestPackage272To275Test(unittest.TestCase):
    def test_272_to_275_prepares_request_challenge_blocks_generic_directive_and_reconciles(self):
        request = _request_272()
        challenge = request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
            request,
            operator_identity=_OPERATOR_IDENTITY,
            challenge_nonce=_CHALLENGE_NONCE,
            issued_at=_ISSUED_AT,
            expires_at=_CHALLENGE_EXPIRES_AT,
        )
        preflight = request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply="plan and execute the next blk-system sprint package",
            operator_identity=_OPERATOR_IDENTITY,
            evaluated_at=_EVALUATED_AT,
        )
        reconciliation = request_package.reconcile_rtm_blk_link_drift_coverage_request_275(preflight)

        self.assertEqual(request["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_272_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY", request["markers"])
        self.assertEqual(request["operator_identity"], _OPERATOR_IDENTITY)
        self.assertEqual(
            request["beo_finality_reconciliation_hash"],
            beo_execution._CANONICAL_RECONCILIATION_271_HASH,
        )
        self.assertEqual(
            request["beo_finality_execution_hash"],
            beo_execution._CANONICAL_EXECUTION_270_HASH,
        )
        self.assertEqual(
            request["beo_finality_record_hash"],
            "sha256:25494d553bf17588f8adb0816f544d88d893821b82f9928b24cdde5898a0603d",
        )
        self.assertTrue(request["approval_rules"]["short_approve_requires_challenge_hash"])
        self.assertFalse(request["side_effects"]["approval_captured"])
        self.assertFalse(request["side_effects"]["run_id_reserved"])
        self.assertFalse(request["side_effects"]["rtm_generation"])
        self.assertFalse(request["side_effects"]["production_blk_link_execution"])
        self.assertFalse(request["side_effects"]["drift_rejection"])
        self.assertFalse(request["side_effects"]["coverage_truth"])
        self.assertFalse(request["side_effects"]["protected_body_access"])
        self.assertFalse(request["side_effects"]["target_source_git_mutation"])
        self.assertRegex(request["request_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(request["request_hash"], request_package._CANONICAL_REQUEST_272_HASH)

        self.assertEqual(challenge["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY_NOT_APPROVED")
        self.assertIn("BLK_SYSTEM_273_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_READY", challenge["markers"])
        self.assertEqual(challenge["request_hash"], request["request_hash"])
        self.assertEqual(challenge["short_approval_reply"], "Approve")
        self.assertTrue(challenge["challenge_rules"]["operator_reply_must_equal_short_approval_reply"])
        self.assertFalse(challenge["side_effects"]["approval_captured"])
        self.assertFalse(challenge["side_effects"]["run_id_consumed"])
        self.assertRegex(challenge["challenge_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(challenge["challenge_hash"], request_package._CANONICAL_CHALLENGE_273_HASH)

        self.assertEqual(preflight["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED")
        self.assertIn("BLK_SYSTEM_274_RTM_BLK_LINK_DRIFT_COVERAGE_APPROVAL_PREFLIGHT_BLOCKED", preflight["markers"])
        self.assertEqual(preflight["challenge_hash"], challenge["challenge_hash"])
        self.assertEqual(preflight["operator_reply_status"], "NOT_BOUND_APPROVE_FOR_CHALLENGE")
        self.assertEqual(
            preflight["evaluation_result"],
            "generic_or_unbound_operator_directive_is_not_rtm_blk_link_approval",
        )
        self.assertFalse(preflight["side_effects"]["approval_captured"])
        self.assertFalse(preflight["side_effects"]["short_approve_matched"])
        self.assertFalse(preflight["side_effects"]["production_blk_link_execution"])
        self.assertRegex(preflight["preflight_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(preflight["preflight_hash"], request_package._CANONICAL_PREFLIGHT_274_HASH)

        self.assertEqual(reconciliation["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED_APPROVAL_REQUIRED_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_275_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_RECONCILED", reconciliation["markers"])
        self.assertEqual(reconciliation["request_hash"], request["request_hash"])
        self.assertEqual(reconciliation["challenge_hash"], challenge["challenge_hash"])
        self.assertEqual(reconciliation["preflight_hash"], preflight["preflight_hash"])
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_BOUND_APPROVE_OR_EXACT_TEXT_REQUIRED_NOT_GRANTED",
        )
        self.assertFalse(reconciliation["side_effects"]["rtm_generation"])
        self.assertFalse(reconciliation["side_effects"]["production_blk_link_execution"])
        self.assertFalse(reconciliation["side_effects"]["protected_body_access"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(reconciliation["reconciliation_hash"], request_package._CANONICAL_RECONCILIATION_275_HASH)

    def test_short_approve_matches_only_inside_bound_challenge_without_execution(self):
        challenge = _challenge_273()
        matched = request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply="Approve",
            operator_identity=_OPERATOR_IDENTITY,
            evaluated_at=_EVALUATED_AT,
        )

        self.assertEqual(
            matched["status"],
            "RTM_BLK_LINK_DRIFT_COVERAGE_APPROVE_CHALLENGE_MATCHED_EXECUTION_NOT_PERFORMED",
        )
        self.assertEqual(matched["operator_reply_status"], "BOUND_APPROVE_FOR_CHALLENGE")
        self.assertEqual(matched["evaluation_result"], "short_approve_bound_to_challenge_but_no_execution_authority")
        self.assertTrue(matched["side_effects"]["short_approve_matched"])
        self.assertFalse(matched["side_effects"]["approval_captured"])
        self.assertFalse(matched["side_effects"]["run_id_reserved"])
        self.assertFalse(matched["side_effects"]["run_id_consumed"])
        self.assertFalse(matched["side_effects"]["rtm_generation"])
        self.assertFalse(matched["side_effects"]["production_blk_link_execution"])
        self.assertFalse(matched["side_effects"]["coverage_truth"])
        with self.assertRaisesRegex(ValueError, "current package reconciles only blocked preflight"):
            request_package.reconcile_rtm_blk_link_drift_coverage_request_275(matched)

        expired = request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply="Approve",
            operator_identity=_OPERATOR_IDENTITY,
            evaluated_at="2026-05-20T08:57:00+10:00",
        )
        self.assertEqual(expired["operator_reply_status"], "EXPIRED_CHALLENGE_NOT_APPROVAL")
        self.assertFalse(expired["side_effects"]["short_approve_matched"])

        premature = request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply="Approve",
            operator_identity=_OPERATOR_IDENTITY,
            evaluated_at="2026-05-20T08:25:00+10:00",
        )
        self.assertEqual(premature["operator_reply_status"], "CHALLENGE_NOT_YET_ISSUED_NOT_APPROVAL")
        self.assertFalse(premature["side_effects"]["short_approve_matched"])

        with self.assertRaisesRegex(ValueError, "operator_identity"):
            request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
                challenge,
                operator_reply="Approve",
                operator_identity="discord:000",
                evaluated_at=_EVALUATED_AT,
            )

    def test_rejects_rehashed_upstream_request_challenge_and_operator_reply_laundering(self):
        upstream = _reconciliation_271()
        forged_upstream = copy.deepcopy(upstream)
        forged_upstream["next_frontier"] = "NEXT_FRONTIER_RTM_GENERATION_APPROVED"
        forged_upstream["reconciliation_hash"] = request_package._hash_package(
            {key: value for key, value in forged_upstream.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-271|next_frontier|forbidden authority"):
            request_package.build_rtm_blk_link_drift_coverage_request_272(
                forged_upstream,
                operator_identity=_OPERATOR_IDENTITY,
                requested_at=_REQUESTED_AT,
                expires_at=_REQUEST_EXPIRES_AT,
            )

        request = _request_272()
        tampered_request = copy.deepcopy(request)
        tampered_request["rtm_generation_authorized"] = True
        tampered_request["request_hash"] = request_package._hash_package(
            {key: value for key, value in tampered_request.items() if key != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|unsupported field|forbidden authority"):
            request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
                tampered_request,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce=_CHALLENGE_NONCE,
                issued_at=_ISSUED_AT,
                expires_at=_CHALLENGE_EXPIRES_AT,
            )

        challenge = _challenge_273()
        matched = request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
            challenge,
            operator_reply="Approve",
            operator_identity=_OPERATOR_IDENTITY,
            evaluated_at=_EVALUATED_AT,
        )
        forged_bound = copy.deepcopy(matched)
        forged_bound["operator_reply_hash"] = request_package._hash_text("not Approve")
        forged_bound["preflight_hash"] = request_package._hash_package(
            {key: value for key, value in forged_bound.items() if key != "preflight_hash"}
        )
        with self.assertRaisesRegex(ValueError, "operator_reply_hash"):
            request_package.reconcile_rtm_blk_link_drift_coverage_request_275(forged_bound)

        tampered_challenge = copy.deepcopy(challenge)
        tampered_challenge["short_approval_reply"] = "Approve and run productionBlkLinkExecutionAuthorized"
        tampered_challenge["challenge_hash"] = request_package._hash_package(
            {key: value for key, value in tampered_challenge.items() if key != "challenge_hash"}
        )
        with self.assertRaisesRegex(ValueError, "challenge package|short_approval_reply|forbidden authority"):
            request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
                tampered_challenge,
                operator_reply="Approve",
                operator_identity=_OPERATOR_IDENTITY,
                evaluated_at=_EVALUATED_AT,
            )

        with self.assertRaisesRegex(ValueError, "operator_reply forbidden authority wording"):
            request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
                challenge,
                operator_reply="Approve; rtmGenerated; coverageTruthAuthorized; docs%252Frequirements%252Factive",
                operator_identity=_OPERATOR_IDENTITY,
                evaluated_at=_EVALUATED_AT,
            )

    def test_exact_denials_false_side_effects_nonce_and_window_are_hash_bound(self):
        request = _request_272()
        first = request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
            request,
            operator_identity=_OPERATOR_IDENTITY,
            challenge_nonce=_CHALLENGE_NONCE,
            issued_at=_ISSUED_AT,
            expires_at=_CHALLENGE_EXPIRES_AT,
        )
        original_canonical = request_package._CANONICAL_CHALLENGE_273_HASH
        request_package._CANONICAL_CHALLENGE_273_HASH = None
        try:
            second = request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
                request,
                operator_identity=_OPERATOR_IDENTITY,
                challenge_nonce="BLK-SYSTEM-273-RTM-BLK-LINK-CHALLENGE-002",
                issued_at=_ISSUED_AT,
                expires_at=_CHALLENGE_EXPIRES_AT,
            )
        finally:
            request_package._CANONICAL_CHALLENGE_273_HASH = original_canonical
        self.assertNotEqual(first["challenge_payload_hash"], second["challenge_payload_hash"])
        self.assertNotEqual(first["challenge_hash"], second["challenge_hash"])

        for mutation in ["remove_denial", "duplicate_denial", "extra_denial", "missing_false_flag"]:
            tampered = copy.deepcopy(first)
            if mutation == "remove_denial":
                tampered["denied_authorities"] = tampered["denied_authorities"][:-1]
            elif mutation == "duplicate_denial":
                tampered["denied_authorities"].append(tampered["denied_authorities"][0])
            elif mutation == "extra_denial":
                tampered["denied_authorities"].append("RTM_GENERATION_APPROVED")
            else:
                del tampered["side_effects"]["protected_body_access"]
            tampered["challenge_hash"] = request_package._hash_package(
                {key: value for key, value in tampered.items() if key != "challenge_hash"}
            )
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(ValueError, "denied_authorities|side_effects|forbidden authority"):
                    request_package.evaluate_rtm_blk_link_drift_coverage_approval_preflight_274(
                        tampered,
                        operator_reply="Approve",
                        operator_identity=_OPERATOR_IDENTITY,
                        evaluated_at=_EVALUATED_AT,
                    )

        for bad_nonce in ["", "nonce with spaces", "../nonce", "nonce%2Fescape"]:
            with self.subTest(bad_nonce=bad_nonce):
                with self.assertRaisesRegex(ValueError, "challenge_nonce"):
                    request_package.build_rtm_blk_link_drift_coverage_approve_challenge_273(
                        request,
                        operator_identity=_OPERATOR_IDENTITY,
                        challenge_nonce=bad_nonce,
                        issued_at=_ISSUED_AT,
                        expires_at=_CHALLENGE_EXPIRES_AT,
                    )


if __name__ == "__main__":
    unittest.main()
