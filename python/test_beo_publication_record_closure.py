import copy
import unittest

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_external_beo_publication_execution import build_metadata_bound_external_beo_publication_execution
from test_metadata_bound_external_beo_publication_execution import (
    valid_approval_capture_package,
    valid_execution_request,
)

from beo_publication_record_closure import (
    CANONICAL_BLK129_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK129_PUBLICATION_RECORD_HASH,
    CLOSURE_PACKAGE_ID,
    CLOSURE_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    SIDE_EFFECT_FLAGS,
    build_beo_publication_record_closure,
)


def valid_blk129_package():
    approval = valid_approval_capture_package()
    request = valid_execution_request(approval)
    return build_metadata_bound_external_beo_publication_execution(approval, request)


class BeoPublicationRecordClosureTest(unittest.TestCase):
    def test_closes_exact_blk129_record_for_signer_storage_ledger_finality_without_side_effects(self):
        blk129 = valid_blk129_package()

        closure = build_beo_publication_record_closure(blk129)

        self.assertEqual(closure["closure_status"], CLOSURE_STATUS)
        self.assertEqual(closure["closure_package_id"], CLOSURE_PACKAGE_ID)
        self.assertEqual(closure["upstream_execution_package_hash"], CANONICAL_BLK129_EXECUTION_PACKAGE_HASH)
        self.assertEqual(closure["publication_record_hash"], CANONICAL_BLK129_PUBLICATION_RECORD_HASH)
        self.assertEqual(closure["beo_id"], "BEO_126")
        self.assertEqual(closure["beb_id"], "BEB_126")
        self.assertEqual(closure["publication_record_state"], "CLOSED_FOR_AUTHORITATIVE_SIGNER_STORAGE_LEDGER_FINALITY")
        self.assertTrue(closure["signer_storage_ledger_finality_required"])
        self.assertFalse(closure["signer_storage_ledger_finality_executed"])
        self.assertEqual(set(closure["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(closure["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(closure[flag], False, flag)
        self.assertEqual(
            closure["closure_package_hash"],
            _canonical_hash({key: value for key, value in closure.items() if key != "closure_package_hash"}),
        )

    def test_rejects_forged_or_rehashed_blk129_publication_evidence(self):
        blk129 = valid_blk129_package()
        forged = copy.deepcopy(blk129)
        forged["publication_record"]["published_beo_id"] = "BEO_999"
        with self.assertRaisesRegex(ValueError, "publication_record_hash does not match submitted publication record"):
            build_beo_publication_record_closure(forged)

        forged = copy.deepcopy(blk129)
        forged["beo_id"] = "BEO_999"
        forged["execution_package_hash"] = _canonical_hash(
            {key: value for key, value in forged.items() if key != "execution_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "BLK-129 execution package must match canonical publication evidence"):
            build_beo_publication_record_closure(forged)

    def test_rejects_adjacent_authority_laundering_and_side_effect_claims(self):
        blk129 = valid_blk129_package()
        cases = [
            ({"rtm_status": "RTM_GENERATED"}, "rtm_status must be NOT_GENERATED"),
            ({"cryptographic_signature_generated": True}, "cryptographic_signature_generated must remain false"),
            ({"public_ledger_mutated": True}, "public_ledger_mutated must remain false"),
            ({"protected_body_read": True}, "protected_body_read must remain false"),
            ({"operator_note": "SignatureGenerated"}, "unexpected field 'operator_note'"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(blk129)
            candidate.update(patch)
            if "operator_note" not in patch:
                candidate["execution_package_hash"] = _canonical_hash(
                    {key: value for key, value in candidate.items() if key != "execution_package_hash"}
                )
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_beo_publication_record_closure(candidate)


if __name__ == "__main__":
    unittest.main()
