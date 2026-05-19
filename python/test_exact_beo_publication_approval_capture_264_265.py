import unittest

from test_exact_beo_publication_approval_ladder_257_260 import (
    _beo_reconciliation,
    _drift_reconciliation,
)
import exact_beo_publication_approval_ladder_257_260 as exact_beo
import blk_sprint_package_granularity_guard_261_263 as package_guard
import exact_beo_publication_approval_capture_264_265 as approval_capture


_GENERIC_PACKAGE_DIRECTIVE = "plan and execute the next blk-system sprint package"
_EXACT_APPROVAL_FRONTIER = "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED"
_OPERATOR_IDENTITY = "discord:684235178083745819"
_CAPTURED_AT = "2026-05-19T21:35:49+10:00"


def _approval_contract():
    request = exact_beo.build_exact_beo_publication_run_request_257(
        _beo_reconciliation(), _drift_reconciliation()
    )
    return exact_beo.build_exact_beo_publication_operator_approval_contract_258(request)


def _approval_reconciliation():
    contract = _approval_contract()
    preflight = exact_beo.evaluate_exact_beo_publication_operator_approval_259(
        contract, "plan and execute the next 3-5 blk-system sprints"
    )
    return exact_beo.reconcile_exact_beo_publication_approval_frontier_260(preflight)


def _package_selection():
    review = package_guard.build_sprint_package_frontier_review_261(
        current_frontier=_EXACT_APPROVAL_FRONTIER,
        operator_directive=_GENERIC_PACKAGE_DIRECTIVE,
    )
    contract = package_guard.build_sprint_package_granularity_contract_262(review)
    return package_guard.evaluate_sprint_package_candidate_263(
        contract,
        {
            "candidate_id": "exact-beo-publication-approval-capture",
            "candidate_type": "authority_execution_package",
            "requested_sprints": [261, 262, 263],
            "operator_directive": _GENERIC_PACKAGE_DIRECTIVE,
            "frontier": _EXACT_APPROVAL_FRONTIER,
            "requires_exact_operator_approval_text": True,
            "exact_operator_approval_text_present": False,
            "independent_audit_boundaries": [
                "approval_capture",
                "run_id_assignment",
                "publication_execution",
            ],
            "planned_outputs": [
                "approval_capture",
                "publication_execution",
            ],
            "side_effects": package_guard.denied_side_effects(),
        },
    )


class ExactBeoPublicationApprovalCapture264To265Test(unittest.TestCase):
    def test_264_to_265_captures_exact_operator_text_but_does_not_publish(self):
        contract = _approval_contract()
        reconciliation_260 = _approval_reconciliation()
        selection_263 = _package_selection()

        capture = approval_capture.capture_exact_beo_publication_operator_approval_264(
            contract,
            reconciliation_260,
            selection_263,
            operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
            operator_identity=_OPERATOR_IDENTITY,
            captured_at=_CAPTURED_AT,
        )
        reconciliation = approval_capture.reconcile_exact_beo_publication_approval_capture_265(capture)

        self.assertEqual(capture["status"], "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED_NO_RUN")
        self.assertEqual(capture["operator_text_hash"], approval_capture.EXACT_OPERATOR_APPROVAL_TEXT_HASH_264)
        self.assertEqual(
            capture["approval_capture_hash"],
            "sha256:cdf22534b46214ebf8b57a580c183536f289e15a1e482d7726638e0628237399",
        )
        self.assertEqual(capture["operator_identity"], _OPERATOR_IDENTITY)
        self.assertEqual(capture["contract_hash"], contract["contract_hash"])
        self.assertEqual(capture["approval_reconciliation_hash"], reconciliation_260["reconciliation_hash"])
        self.assertEqual(capture["selection_hash"], selection_263["selection_hash"])
        self.assertEqual(capture["selection_hash"], "sha256:b3fbfbc3ba4384a4b60143f9ff66aae41ddfe156eed4706575f48c645861cbc8")
        self.assertTrue(capture["side_effects"]["operator_approval_captured"])
        self.assertFalse(capture["side_effects"]["run_id_reserved"])
        self.assertFalse(capture["side_effects"]["run_id_consumed"])
        self.assertFalse(capture["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertFalse(capture["side_effects"]["beo_published"])
        self.assertFalse(capture["side_effects"]["cryptographic_signature_generated"])
        self.assertFalse(capture["side_effects"]["immutable_storage_written"])
        self.assertFalse(capture["side_effects"]["public_ledger_appended"])
        self.assertFalse(capture["side_effects"]["rtm_generation"])
        self.assertFalse(capture["side_effects"]["production_blk_link_execution"])
        self.assertFalse(capture["side_effects"]["protected_body_access"])
        self.assertIn("BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED", capture["markers"])

        self.assertEqual(reconciliation["status"], "EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED_RUN_NOT_EXECUTED")
        self.assertEqual(reconciliation["approval_capture_hash"], capture["approval_capture_hash"])
        self.assertEqual(
            reconciliation["reconciliation_hash"],
            "sha256:c20f5a0a39383fbfdd811d15aab4f56fae7973d2ddf4f22d9e6b3337c7ca9b21",
        )
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_PACKAGE_REQUIRED_NOT_EXECUTED",
        )
        self.assertIn("BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED", reconciliation["markers"])
        self.assertTrue(reconciliation["side_effects"]["operator_approval_captured"])
        self.assertFalse(reconciliation["side_effects"]["beo_published"])
        self.assertFalse(reconciliation["side_effects"]["run_id_consumed"])

    def test_rejects_generic_approval_and_self_attested_publication_fields(self):
        contract = _approval_contract()
        reconciliation_260 = _approval_reconciliation()
        selection_263 = _package_selection()

        for bad_text in (
            "Approve",
            "publication approval captured",
            "BEO publication authorized",
            "BEO published; signer reused; ledger appended",
        ):
            with self.subTest(bad_text=bad_text):
                with self.assertRaisesRegex(ValueError, "exact operator approval text|forbidden authority"):
                    approval_capture.capture_exact_beo_publication_operator_approval_264(
                        contract,
                        reconciliation_260,
                        selection_263,
                        operator_text=bad_text,
                        operator_identity=_OPERATOR_IDENTITY,
                        captured_at=_CAPTURED_AT,
                    )

        capture = approval_capture.capture_exact_beo_publication_operator_approval_264(
            contract,
            reconciliation_260,
            selection_263,
            operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
            operator_identity=_OPERATOR_IDENTITY,
            captured_at=_CAPTURED_AT,
        )
        tampered = approval_capture._deepcopy(capture)
        tampered["side_effects"]["beo_published"] = True
        tampered["approval_capture_hash"] = approval_capture._hash_package(
            {k: v for k, v in tampered.items() if k != "approval_capture_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|canonical BLK-SYSTEM-264|forbidden authority"):
            approval_capture.reconcile_exact_beo_publication_approval_capture_265(tampered)

    def test_rejects_rehashed_upstream_and_bad_identity_or_time(self):
        contract = _approval_contract()
        reconciliation_260 = _approval_reconciliation()
        selection_263 = _package_selection()

        forged_contract = exact_beo._deepcopy(contract)
        forged_contract["request_hash"] = "sha256:" + "1" * 64
        forged_contract["contract_hash"] = exact_beo._hash_package(
            {k: v for k, v in forged_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-257|canonical BLK-SYSTEM-258"):
            approval_capture.capture_exact_beo_publication_operator_approval_264(
                forged_contract,
                reconciliation_260,
                selection_263,
                operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
                operator_identity=_OPERATOR_IDENTITY,
                captured_at=_CAPTURED_AT,
            )

        with self.assertRaisesRegex(ValueError, "operator_identity"):
            approval_capture.capture_exact_beo_publication_operator_approval_264(
                contract,
                reconciliation_260,
                selection_263,
                operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
                operator_identity="discord:000",
                captured_at=_CAPTURED_AT,
            )

        with self.assertRaisesRegex(ValueError, "captured_at"):
            approval_capture.capture_exact_beo_publication_operator_approval_264(
                contract,
                reconciliation_260,
                selection_263,
                operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
                operator_identity=_OPERATOR_IDENTITY,
                captured_at="2026-05-19T21:35:49",
            )


if __name__ == "__main__":
    unittest.main()
