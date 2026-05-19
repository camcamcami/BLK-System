import unittest

from test_exact_beo_publication_approval_capture_264_265 import (
    _approval_contract,
    _approval_reconciliation,
    _package_selection,
    _OPERATOR_IDENTITY,
    _CAPTURED_AT,
)
import exact_beo_publication_approval_ladder_257_260 as exact_beo
import exact_beo_publication_approval_capture_264_265 as approval_capture
import exact_beo_publication_run_package_266_268 as run_package


_GENERIC_PACKAGE_DIRECTIVE = "plan and execute the next blk-system sprint package"
_REQUESTED_AT = "2026-05-19T22:05:00+10:00"
_EXPIRES_AT = "2026-05-20T22:05:00+10:00"
_EVALUATED_AT = "2026-05-19T22:06:00+10:00"


def _capture_264():
    return approval_capture.capture_exact_beo_publication_operator_approval_264(
        _approval_contract(),
        _approval_reconciliation(),
        _package_selection(),
        operator_text=exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258,
        operator_identity=_OPERATOR_IDENTITY,
        captured_at=_CAPTURED_AT,
    )


def _reconciliation_265(capture=None):
    return approval_capture.reconcile_exact_beo_publication_approval_capture_265(capture or _capture_264())


class ExactBeoPublicationRunPackage266To268Test(unittest.TestCase):
    def test_266_to_268_prepares_exact_run_package_but_blocks_generic_execution(self):
        capture = _capture_264()
        reconciliation_265 = _reconciliation_265(capture)

        package = run_package.build_exact_beo_publication_run_package_266(
            capture,
            reconciliation_265,
            operator_identity=_OPERATOR_IDENTITY,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
        )
        preflight = run_package.evaluate_exact_beo_publication_run_package_preflight_267(
            package,
            operator_text=_GENERIC_PACKAGE_DIRECTIVE,
            evaluated_at=_EVALUATED_AT,
        )
        reconciliation = run_package.reconcile_exact_beo_publication_run_package_268(preflight)

        self.assertEqual(package["status"], "EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY_NOT_EXECUTED")
        self.assertEqual(package["approval_capture_hash"], capture["approval_capture_hash"])
        self.assertEqual(package["approval_capture_reconciliation_hash"], reconciliation_265["reconciliation_hash"])
        self.assertEqual(package["operator_identity"], _OPERATOR_IDENTITY)
        self.assertEqual(package["requested_at"], _REQUESTED_AT)
        self.assertEqual(package["expires_at"], _EXPIRES_AT)
        self.assertRegex(package["execution_request_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(package["run_package_hash"], run_package._CANONICAL_RUN_PACKAGE_266_HASH)
        self.assertEqual(package["run_package_hash"], "sha256:7815590afd45c9ab978e6bcfffa09446b870e9c17d66688c31c5ca36905e4a23")
        self.assertEqual(package["required_exact_run_approval_text_hash"], run_package.EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_HASH_266)
        self.assertIn("BLK_SYSTEM_266_EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY", package["markers"])
        self.assertTrue(package["side_effects"]["operator_approval_captured"])
        self.assertTrue(package["side_effects"]["run_package_prepared"])
        self.assertFalse(package["side_effects"]["run_preflight_recorded"])
        self.assertFalse(package["side_effects"]["run_id_reserved"])
        self.assertFalse(package["side_effects"]["run_id_consumed"])
        self.assertFalse(package["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertFalse(package["side_effects"]["beo_published"])
        self.assertFalse(package["side_effects"]["cryptographic_signature_generated"])
        self.assertFalse(package["side_effects"]["immutable_storage_written"])
        self.assertFalse(package["side_effects"]["public_ledger_appended"])
        self.assertFalse(package["side_effects"]["rtm_generation"])
        self.assertFalse(package["side_effects"]["production_blk_link_execution"])
        self.assertFalse(package["side_effects"]["protected_body_access"])

        self.assertEqual(preflight["status"], "BLOCKED_BY_MISSING_EXACT_BEO_PUBLICATION_RUN_APPROVAL")
        self.assertEqual(preflight["operator_text_status"], "NOT_EXACT_RUN_APPROVAL_TEXT")
        self.assertEqual(preflight["run_package_hash"], package["run_package_hash"])
        self.assertEqual(preflight["preflight_hash"], run_package._CANONICAL_PREFLIGHT_267_HASH)
        self.assertEqual(preflight["preflight_hash"], "sha256:9ed5a7ee1139be7d48df8d2a6baaee10a8a24a7bdbd7abc469b062e5b95b2e5c")
        self.assertIn("BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_BLOCKED", preflight["markers"])
        self.assertTrue(preflight["side_effects"]["run_preflight_recorded"])
        self.assertFalse(preflight["side_effects"]["run_id_consumed"])
        self.assertFalse(preflight["side_effects"]["beo_published"])

        self.assertEqual(reconciliation["status"], "EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED_EXECUTION_NOT_GRANTED")
        self.assertEqual(reconciliation["preflight_hash"], preflight["preflight_hash"])
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_REQUIRED_NOT_GRANTED",
        )
        self.assertEqual(reconciliation["reconciliation_hash"], run_package._CANONICAL_RECONCILIATION_268_HASH)
        self.assertEqual(reconciliation["reconciliation_hash"], "sha256:e1602b1abd0c96badb12efca01e794f48da06e6d69ab1b3d8e86b27f0e882172")
        self.assertIn("BLK_SYSTEM_268_EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED", reconciliation["markers"])
        self.assertFalse(reconciliation["side_effects"]["run_id_reserved"])
        self.assertFalse(reconciliation["side_effects"]["run_id_consumed"])
        self.assertFalse(reconciliation["side_effects"]["beo_published"])

    def test_exact_run_approval_text_is_seen_but_not_executed_by_preparation_package(self):
        package = run_package.build_exact_beo_publication_run_package_266(
            _capture_264(),
            _reconciliation_265(),
            operator_identity=_OPERATOR_IDENTITY,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
        )

        preflight = run_package.evaluate_exact_beo_publication_run_package_preflight_267(
            package,
            operator_text=run_package.EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266,
            evaluated_at=_EVALUATED_AT,
        )

        self.assertEqual(preflight["status"], "EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_MATCHED_EXECUTION_NOT_PERFORMED")
        self.assertEqual(preflight["operator_text_status"], "EXACT_RUN_APPROVAL_TEXT_MATCHED")
        self.assertFalse(preflight["side_effects"]["run_id_reserved"])
        self.assertFalse(preflight["side_effects"]["run_id_consumed"])
        self.assertFalse(preflight["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertFalse(preflight["side_effects"]["cryptographic_signature_generated"])
        self.assertFalse(preflight["side_effects"]["immutable_storage_written"])
        self.assertFalse(preflight["side_effects"]["public_ledger_appended"])

    def test_rejects_rehashed_upstream_and_self_attested_run_side_effects(self):
        capture = _capture_264()
        reconciliation_265 = _reconciliation_265(capture)

        forged_capture = approval_capture._deepcopy(capture)
        forged_capture["operator_identity"] = "discord:000"
        forged_capture["approval_capture_hash"] = approval_capture._hash_package(
            {k: v for k, v in forged_capture.items() if k != "approval_capture_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-264|operator_identity"):
            run_package.build_exact_beo_publication_run_package_266(
                forged_capture,
                reconciliation_265,
                operator_identity=_OPERATOR_IDENTITY,
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

        forged_reconciliation = approval_capture._deepcopy(reconciliation_265)
        forged_reconciliation["approval_capture_hash"] = "sha256:" + "1" * 64
        forged_reconciliation["reconciliation_hash"] = approval_capture._hash_package(
            {k: v for k, v in forged_reconciliation.items() if k != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-265|approval_capture_hash"):
            run_package.build_exact_beo_publication_run_package_266(
                capture,
                forged_reconciliation,
                operator_identity=_OPERATOR_IDENTITY,
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

        package = run_package.build_exact_beo_publication_run_package_266(
            capture,
            reconciliation_265,
            operator_identity=_OPERATOR_IDENTITY,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
        )
        tampered = run_package._deepcopy(package)
        tampered["side_effects"]["run_id_consumed"] = True
        tampered["side_effects"]["beo_published"] = True
        tampered["run_package_hash"] = run_package._hash_package(
            {k: v for k, v in tampered.items() if k != "run_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|canonical BLK-SYSTEM-266|forbidden authority"):
            run_package.evaluate_exact_beo_publication_run_package_preflight_267(
                tampered,
                operator_text=_GENERIC_PACKAGE_DIRECTIVE,
                evaluated_at=_EVALUATED_AT,
            )

    def test_rejects_laundered_operator_text_and_bad_window(self):
        package = run_package.build_exact_beo_publication_run_package_266(
            _capture_264(),
            _reconciliation_265(),
            operator_identity=_OPERATOR_IDENTITY,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
        )

        for bad_text in (
            "BEO publication authorized; signer reused; ledger appended",
            "publishBEO with productionBlkLinkExecutionAuthorized",
            "docs%252Frequirements%252Factive body was read",
        ):
            with self.subTest(bad_text=bad_text):
                with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
                    run_package.evaluate_exact_beo_publication_run_package_preflight_267(
                        package,
                        operator_text=bad_text,
                        evaluated_at=_EVALUATED_AT,
                    )

        with self.assertRaisesRegex(ValueError, "operator_identity"):
            run_package.build_exact_beo_publication_run_package_266(
                _capture_264(),
                _reconciliation_265(),
                operator_identity="discord:000",
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

        with self.assertRaisesRegex(ValueError, "expires_at must be after requested_at"):
            run_package.build_exact_beo_publication_run_package_266(
                _capture_264(),
                _reconciliation_265(),
                operator_identity=_OPERATOR_IDENTITY,
                requested_at=_EXPIRES_AT,
                expires_at=_REQUESTED_AT,
            )


if __name__ == "__main__":
    unittest.main()
