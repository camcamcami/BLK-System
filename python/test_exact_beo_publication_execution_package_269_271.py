import copy
import unittest

from test_exact_beo_publication_run_package_266_268 import (
    _capture_264,
    _reconciliation_265,
    _OPERATOR_IDENTITY,
)
import exact_beo_publication_run_package_266_268 as run_package
import exact_beo_publication_execution_package_269_271 as execution_package


_APPROVAL_TEXT = (
    "APPROVE BLK-SYSTEM-269..271 EXACT BEO PUBLICATION EXECUTION PACKAGE; "
    "ONE RUN ID ONLY; ONE BEO PUBLICATION FINALITY RECORD ONLY; "
    "SIGNATURE RECEIPT, IMMUTABLE-STORAGE RECEIPT, AND PUBLIC-LEDGER ENTRY EVIDENCE ONLY; "
    "NO REUSABLE SIGNER STORAGE LEDGER AUTHORITY; NO RTM; NO PRODUCTION BLK-LINK; "
    "NO DRIFT TRUTH; NO COVERAGE TRUTH; NO PROTECTED BODY; NO TARGET SOURCE GIT MUTATION."
)
_REQUESTED_AT = "2026-05-19T22:05:00+10:00"
_EXPIRES_AT = "2026-05-20T22:05:00+10:00"
_EVALUATED_AT = "2026-05-19T22:06:00+10:00"
_APPROVED_AT = "2026-05-20T07:29:34+10:00"
_APPROVAL_EXPIRES_AT = "2026-05-20T08:29:34+10:00"
_EXECUTION_REQUESTED_AT = "2026-05-20T07:31:00+10:00"
_EXECUTION_EXPIRES_AT = "2026-05-20T08:00:00+10:00"
_EXECUTED_AT = "2026-05-20T07:32:00+10:00"


def _run_package_266():
    capture = _capture_264()
    return run_package.build_exact_beo_publication_run_package_266(
        capture,
        _reconciliation_265(capture),
        operator_identity=_OPERATOR_IDENTITY,
        requested_at=_REQUESTED_AT,
        expires_at=_EXPIRES_AT,
    )


def _preflight_267_exact_text_seen():
    return run_package.evaluate_exact_beo_publication_run_package_preflight_267(
        _run_package_266(),
        operator_text=run_package.EXACT_BEO_PUBLICATION_RUN_APPROVAL_TEXT_266,
        evaluated_at=_EVALUATED_AT,
    )


def _reconciliation_268():
    generic_preflight = run_package.evaluate_exact_beo_publication_run_package_preflight_267(
        _run_package_266(),
        operator_text="plan and execute the next blk-system sprint package",
        evaluated_at=_EVALUATED_AT,
    )
    return run_package.reconcile_exact_beo_publication_run_package_268(generic_preflight)


def _approval_269():
    return execution_package.capture_exact_beo_publication_execution_approval_269(
        _reconciliation_268(),
        operator_text=_APPROVAL_TEXT,
        operator_identity=_OPERATOR_IDENTITY,
        approved_at=_APPROVED_AT,
        expires_at=_APPROVAL_EXPIRES_AT,
    )


def _execution_270():
    return execution_package.execute_exact_beo_publication_finality_270(
        _approval_269(),
        requested_at=_EXECUTION_REQUESTED_AT,
        expires_at=_EXECUTION_EXPIRES_AT,
        executed_at=_EXECUTED_AT,
    )


class ExactBeoPublicationExecutionPackage269To271Test(unittest.TestCase):
    def test_269_to_271_captures_exact_approval_executes_one_finality_record_and_reconciles(self):
        approval = _approval_269()
        execution = execution_package.execute_exact_beo_publication_finality_270(
            approval,
            requested_at=_EXECUTION_REQUESTED_AT,
            expires_at=_EXECUTION_EXPIRES_AT,
            executed_at=_EXECUTED_AT,
        )
        reconciliation = execution_package.reconcile_exact_beo_publication_finality_271(execution)

        self.assertEqual(approval["status"], "EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED_ONE_RUN_ONLY")
        self.assertEqual(approval["operator_identity"], _OPERATOR_IDENTITY)
        self.assertEqual(approval["operator_text_hash"], execution_package.EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_TEXT_HASH_269)
        self.assertEqual(approval["operator_text_hash"], "sha256:bd140e194cb01fb336071fa8883e8bc5896760e802463d72c785d90755a18f39")
        self.assertEqual(approval["run_id"], "RUN-BLK-SYSTEM-270-EXACT-BEO-PUBLICATION-FINALITY-001")
        self.assertEqual(approval["upstream_reconciliation_hash"], run_package._CANONICAL_RECONCILIATION_268_HASH)
        self.assertTrue(approval["side_effects"]["execution_approval_captured"])
        self.assertTrue(approval["side_effects"]["run_id_reserved"])
        self.assertFalse(approval["side_effects"]["run_id_consumed"])
        self.assertFalse(approval["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertRegex(approval["approval_capture_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(approval["approval_capture_hash"], execution_package._CANONICAL_APPROVAL_269_HASH)
        self.assertEqual(approval["approval_capture_hash"], "sha256:856ae211896f2fe55cfac21ec955583399182a479ccbaf955ccb6c6612a8d9e9")

        self.assertEqual(execution["status"], "EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED_ONE_RUN_ONLY")
        self.assertEqual(execution["run_id_consumed"], approval["run_id"])
        self.assertEqual(execution["approval_capture_hash"], approval["approval_capture_hash"])
        self.assertEqual(execution["requested_at"], _EXECUTION_REQUESTED_AT)
        self.assertEqual(execution["expires_at"], _EXECUTION_EXPIRES_AT)
        self.assertEqual(execution["executed_at"], _EXECUTED_AT)
        self.assertTrue(execution["side_effects"]["run_id_consumed"])
        self.assertTrue(execution["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertTrue(execution["side_effects"]["beo_published"])
        self.assertTrue(execution["side_effects"]["signature_receipt_recorded"])
        self.assertTrue(execution["side_effects"]["immutable_storage_receipt_recorded"])
        self.assertTrue(execution["side_effects"]["public_ledger_receipt_recorded"])
        self.assertFalse(execution["side_effects"]["reusable_signer_storage_ledger_authority"])
        self.assertFalse(execution["side_effects"]["rtm_generation"])
        self.assertFalse(execution["side_effects"]["production_blk_link_execution"])
        self.assertFalse(execution["side_effects"]["drift_rejection"])
        self.assertFalse(execution["side_effects"]["coverage_truth"])
        self.assertFalse(execution["side_effects"]["protected_body_access"])
        self.assertFalse(execution["side_effects"]["target_source_git_mutation"])
        self.assertRegex(execution["signature_receipt_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(execution["immutable_storage_receipt_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(execution["public_ledger_entry_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(execution["finality_record_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertRegex(execution["execution_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(execution["signature_receipt_hash"], "sha256:68f2a0bf76534caa23cd00d8453bcfbbe2d01af351517147857e4296f122dd5f")
        self.assertEqual(execution["immutable_storage_receipt_hash"], "sha256:220c4f6afb42bbe758f97e2f7ecc15f6c1907884c42e44bd7507b1b723c874cc")
        self.assertEqual(execution["public_ledger_entry_hash"], "sha256:a83105a8638b0600a5fa8db766b337c91da14f326a7cd74e412e92f4a57c2250")
        self.assertEqual(execution["finality_record_hash"], "sha256:25494d553bf17588f8adb0816f544d88d893821b82f9928b24cdde5898a0603d")
        self.assertEqual(execution["execution_package_hash"], execution_package._CANONICAL_EXECUTION_270_HASH)
        self.assertEqual(execution["execution_package_hash"], "sha256:2cd4b38b78452fadd96456acfc2cbc6a218e46c4d0a9342220fbca6d9d8a389e")

        self.assertEqual(reconciliation["status"], "EXACT_BEO_PUBLICATION_FINALITY_RECONCILED_RTM_BLK_LINK_REQUEST_READY")
        self.assertEqual(reconciliation["execution_package_hash"], execution["execution_package_hash"])
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_AFTER_EXACT_BEO_PUBLICATION",
        )
        self.assertTrue(reconciliation["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertFalse(reconciliation["side_effects"]["rtm_generation"])
        self.assertFalse(reconciliation["side_effects"]["production_blk_link_execution"])
        self.assertFalse(reconciliation["side_effects"]["protected_body_access"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(reconciliation["reconciliation_hash"], execution_package._CANONICAL_RECONCILIATION_271_HASH)
        self.assertEqual(reconciliation["reconciliation_hash"], "sha256:19195c218d30eb18b5343d40b3177e3c1cce3260c8519810b3e424cdccc1d49c")

    def test_rejects_generic_approve_and_laundered_or_wrong_operator_text(self):
        reconciliation = _reconciliation_268()
        for bad_text in (
            "Approve",
            "I grant exact execution approval",
            "BEO publication authorized; RTM generation enabled",
            "publishBEO and productionBlkLinkExecutionAuthorized",
            "docs%252Frequirements%252Factive body was read",
        ):
            with self.subTest(bad_text=bad_text):
                with self.assertRaisesRegex(ValueError, "exact execution approval text|forbidden authority wording"):
                    execution_package.capture_exact_beo_publication_execution_approval_269(
                        reconciliation,
                        operator_text=bad_text,
                        operator_identity=_OPERATOR_IDENTITY,
                        approved_at=_APPROVED_AT,
                        expires_at=_APPROVAL_EXPIRES_AT,
                    )

        with self.assertRaisesRegex(ValueError, "operator_identity"):
            execution_package.capture_exact_beo_publication_execution_approval_269(
                reconciliation,
                operator_text=_APPROVAL_TEXT,
                operator_identity="discord:000",
                approved_at=_APPROVED_AT,
                expires_at=_APPROVAL_EXPIRES_AT,
            )

    def test_rejects_rehashed_upstream_and_retargeted_run_or_side_effects(self):
        reconciliation = _reconciliation_268()
        forged_upstream = copy.deepcopy(reconciliation)
        forged_upstream["next_frontier"] = "NEXT_FRONTIER_RTM_GENERATION_APPROVED"
        forged_upstream["reconciliation_hash"] = execution_package._hash_package(
            {key: value for key, value in forged_upstream.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-268|next_frontier|forbidden authority"):
            execution_package.capture_exact_beo_publication_execution_approval_269(
                forged_upstream,
                operator_text=_APPROVAL_TEXT,
                operator_identity=_OPERATOR_IDENTITY,
                approved_at=_APPROVED_AT,
                expires_at=_APPROVAL_EXPIRES_AT,
            )

        approval = _approval_269()
        for patch, message in (
            ({"run_id": "RUN-BLK-SYSTEM-270-OTHER"}, "run_id"),
            ({"operator_identity": "discord:000"}, "operator_identity"),
            ({"side_effects": approval["side_effects"] | {"run_id_consumed": True}}, "side_effects"),
            ({"side_effects": approval["side_effects"] | {"rtm_generation": True}}, "side_effects|forbidden authority"),
        ):
            tampered = copy.deepcopy(approval)
            tampered.update(patch)
            tampered["approval_capture_hash"] = execution_package._hash_package(
                {key: value for key, value in tampered.items() if key != "approval_capture_hash"}
            )
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    execution_package.execute_exact_beo_publication_finality_270(
                        tampered,
                        requested_at=_EXECUTION_REQUESTED_AT,
                        expires_at=_EXECUTION_EXPIRES_AT,
                        executed_at=_EXECUTED_AT,
                    )

    def test_execution_window_receipts_and_reconciliation_are_hash_bound(self):
        approval = _approval_269()
        first = execution_package.execute_exact_beo_publication_finality_270(
            approval,
            requested_at=_EXECUTION_REQUESTED_AT,
            expires_at=_EXECUTION_EXPIRES_AT,
            executed_at=_EXECUTED_AT,
        )
        original_canonical = execution_package._CANONICAL_EXECUTION_270_HASH
        execution_package._CANONICAL_EXECUTION_270_HASH = None
        try:
            second = execution_package.execute_exact_beo_publication_finality_270(
                approval,
                requested_at="2026-05-20T07:35:00+10:00",
                expires_at="2026-05-20T08:10:00+10:00",
                executed_at="2026-05-20T07:36:00+10:00",
            )
        finally:
            execution_package._CANONICAL_EXECUTION_270_HASH = original_canonical
        self.assertNotEqual(first["execution_request_hash"], second["execution_request_hash"])
        self.assertNotEqual(first["finality_record_hash"], second["finality_record_hash"])
        self.assertNotEqual(first["execution_package_hash"], second["execution_package_hash"])
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-270"):
            execution_package.execute_exact_beo_publication_finality_270(
                approval,
                requested_at="2026-05-20T07:35:00+10:00",
                expires_at="2026-05-20T08:10:00+10:00",
                executed_at="2026-05-20T07:36:00+10:00",
            )

        for patch, message in (
            ({"signature_receipt_hash": "sha256:" + "0" * 64}, "signature_receipt_hash"),
            ({"side_effects": first["side_effects"] | {"protected_body_access": True}}, "side_effects|forbidden authority"),
            ({"side_effects": first["side_effects"] | {"production_blk_link_execution": True}}, "side_effects|forbidden authority"),
            ({"run_id_consumed": "RUN-BLK-SYSTEM-270-OTHER"}, "run_id"),
        ):
            tampered = copy.deepcopy(first)
            tampered.update(patch)
            tampered["execution_package_hash"] = execution_package._hash_package(
                {key: value for key, value in tampered.items() if key != "execution_package_hash"}
            )
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    execution_package.reconcile_exact_beo_publication_finality_271(tampered)

        with self.assertRaisesRegex(ValueError, "approval window"):
            execution_package.execute_exact_beo_publication_finality_270(
                approval,
                requested_at="2026-05-20T08:10:00+10:00",
                expires_at="2026-05-20T08:40:00+10:00",
                executed_at="2026-05-20T08:20:00+10:00",
            )


if __name__ == "__main__":
    unittest.main()
