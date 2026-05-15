import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from beo_publication_record_closure import build_beo_publication_record_closure
from metadata_bound_external_beo_publication_execution import build_metadata_bound_external_beo_publication_execution
from test_metadata_bound_external_beo_publication_execution import (
    valid_approval_capture_package,
    valid_execution_request,
)

from authoritative_beo_publication_finality import (
    FINALITY_PACKAGE_ID,
    FINALITY_RUN_ID,
    FINALITY_STATUS,
    OPERATOR_FINALITY_APPROVAL_TEXT_RAW,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_TRUE_FLAGS,
    build_authoritative_beo_publication_finality,
    valid_authoritative_finality_request,
)


def valid_closure_package():
    approval = valid_approval_capture_package()
    execution_request = valid_execution_request(approval)
    blk129 = build_metadata_bound_external_beo_publication_execution(approval, execution_request)
    return build_beo_publication_record_closure(blk129)


class AuthoritativeBeoPublicationFinalityTest(unittest.TestCase):
    def test_builds_authoritative_signature_storage_ledger_finality_for_exact_closure(self):
        closure = valid_closure_package()
        request = valid_authoritative_finality_request(closure)

        package = build_authoritative_beo_publication_finality(closure, request)

        self.assertEqual(package["finality_status"], FINALITY_STATUS)
        self.assertEqual(package["finality_package_id"], FINALITY_PACKAGE_ID)
        self.assertEqual(package["run_id_consumed"], FINALITY_RUN_ID)
        self.assertEqual(package["operator_approval_text_raw"], OPERATOR_FINALITY_APPROVAL_TEXT_RAW)
        self.assertEqual(package["upstream_closure_package_hash"], closure["closure_package_hash"])
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertEqual(package["beo_publication"], "AUTHORITATIVE_BEO_PUBLICATION_FINALITY_COMPLETE")
        self.assertEqual(package["rtm_status"], "NOT_GENERATED")
        for flag in REQUIRED_TRUE_FLAGS:
            self.assertIs(package[flag], True, flag)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
        signature = package["signature_receipt"]
        storage = package["immutable_storage_receipt"]
        ledger = package["public_ledger_entry"]
        self.assertEqual(signature["signature_status"], "CANONICAL_SIGNATURE_RECEIPT_GENERATED")
        self.assertEqual(storage["storage_status"], "IMMUTABLE_STORAGE_RECEIPT_WRITTEN")
        self.assertEqual(ledger["ledger_status"], "PUBLIC_LEDGER_APPEND_RECORDED")
        self.assertEqual(signature["signature_hash"], _canonical_hash({k: v for k, v in signature.items() if k != "signature_hash"}))
        self.assertEqual(storage["storage_receipt_hash"], _canonical_hash({k: v for k, v in storage.items() if k != "storage_receipt_hash"}))
        self.assertEqual(ledger["ledger_entry_hash"], _canonical_hash({k: v for k, v in ledger.items() if k != "ledger_entry_hash"}))
        self.assertEqual(package["finality_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "finality_package_hash"}))

    def test_rejects_forged_closure_and_non_exact_operator_approval(self):
        closure = valid_closure_package()
        request = valid_authoritative_finality_request(closure)

        forged = copy.deepcopy(closure)
        forged["beo_id"] = "BEO_999"
        forged["closure_package_hash"] = _canonical_hash({k: v for k, v in forged.items() if k != "closure_package_hash"})
        with self.assertRaisesRegex(ValueError, "closure package must match canonical BLK-151 closure"):
            build_authoritative_beo_publication_finality(forged, valid_authoritative_finality_request(forged))

        bad_request = copy.deepcopy(request)
        bad_request["operator_approval_text_raw"] = "approve publication maybe"
        with self.assertRaisesRegex(ValueError, "operator_approval_text_raw must match exact BLK-SYSTEM-152 operator approval"):
            build_authoritative_beo_publication_finality(closure, bad_request)

    def test_rejects_replay_stale_expiry_adjacent_authority_and_laundering(self):
        closure = valid_closure_package()
        base = valid_authoritative_finality_request(closure)
        cases = [
            ({"run_id": "RUN-BLK-SYSTEM-152-OTHER"}, "run_id must be"),
            ({"replayed": True}, "request must not be replayed"),
            ({"stale": True}, "request must not be stale"),
            ({"expired": True}, "request must not be expired"),
            ({"expires_at": base["requested_at"]}, "expires_at must be after requested_at"),
            ({"rtm_generation": True}, "rtm_generation must remain false"),
            ({"rtm_drift_rejection": True}, "rtm_drift_rejection must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"rollback_revocation_supersession_execution": True}, "rollback_revocation_supersession_execution must remain false"),
            ({"operator_note": "generateRTM"}, "unexpected field 'operator_note'"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_authoritative_beo_publication_finality(closure, request)

    def test_request_window_is_hash_bound(self):
        closure = valid_closure_package()
        first = valid_authoritative_finality_request(closure)
        second = valid_authoritative_finality_request(
            closure,
            requested_at="2099-05-15T11:10:00+10:00",
            expires_at="2099-05-15T11:50:00+10:00",
        )

        first_package = build_authoritative_beo_publication_finality(closure, first)
        second_package = build_authoritative_beo_publication_finality(closure, second)

        self.assertNotEqual(first_package["finality_request_hash"], second_package["finality_request_hash"])
        self.assertNotEqual(first_package["finality_package_hash"], second_package["finality_package_hash"])


if __name__ == "__main__":
    unittest.main()
