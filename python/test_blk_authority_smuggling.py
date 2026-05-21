import unittest

from blk_authority_smuggling import scan_for_authority_laundering


class AuthoritySmugglingScannerTest(unittest.TestCase):
    def test_encoded_compact_and_protected_path_authority_claims_fail_closed(self):
        hostile = {
            "notes": [
                "BEO%20publication%20authorized",
                "publish%2542EO",
                "RTMGenerationAuthorized",
                "driftRejectionExecuted",
                "productionBlkLinkEnabled",
                "coverage truth established",
                "coverageTruthAuthorized",
                "coverageTruthGranted",
                "driftTruthEstablished",
                "driftTruthAuthorized",
                "productionBlkLinkAuthorized",
                "productionBlkLinkExecutionAuthorized",
                "generic operator directive is publication approval",
                "execute next sprints is publication approval",
                "rtmGenerated",
                "docs%2525252Frequirements%2525252Factive%2525252FREQ-001.md",
            ],
            "metadata": {
                "isAuthorized": False,
                "nestedApprovalStatus": "approved for publication",
            },
        }

        errors = scan_for_authority_laundering(hostile)

        for marker in [
            "beopublicationauthorized",
            "publishbeo",
            "rtmgenerationauthorized",
            "driftrejectionexecuted",
            "productionblklinkenabled",
            "coverage truth established",
            "coveragetruthauthorized",
            "coveragetruthgranted",
            "drifttruthestablished",
            "drifttruthauthorized",
            "productionblklinkauthorized",
            "productionblklinkexecutionauthorized",
            "generic operator directive is publication approval",
            "execute next sprints is publication approval",
            "rtmgenerated",
            "docsrequirementsactive",
            "isAuthorized",
            "approved for publication",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))

    def test_run_id_signature_and_protected_body_side_effect_claims_fail_closed(self):
        hostile = {
            "notes": [
                "run ID reserved",
                "run-ID reservation authorized",
                "consume at most one run ID",
                "runIdReserved",
                "signature generated",
                "protected body hashed",
                "protected BLK-req body hashing authorized",
                "protected body hash scan allowed",
                "signerStorageLedgerAction",
                "run ID reservation approved",
                "run ID consumption approved",
                "signerStorageLedgerAction approved",
                "relay message dispatch authorized",
                "relay message dispatch approved",
                "Kuronode mutation authorized",
                "protected body scanning authorized",
                "protected body hashing approved",
                "run ID reservation/consumption approved",
                "run-ID reservation/consumption approved",
                "run ID reservation is approved",
                "run ID consumption is approved",
                "signerStorageLedgerAction is approved",
                "protected body hashing is approved",
                "protected body scanning is authorized",
                "Kuronode mutation is authorized",
                "run ID reservation and consumption approved",
                "protected body scan authorized",
                "Kuronode mutation granted",
                "run ID reserved not consumed",
                "signature generation approved",
                "protected body hash authorized",
                "signer storage ledger action executed",
                "relay message dispatch executed",
                "signature generation is approved",
                "protected body hash is authorized",
                "signer storage ledger action is executed",
                "relay message dispatch is executed",
                "Kuronode mutation is executed",
                "BLK_SYSTEM_264_NO_RUN_ID_RESERVED_OR_CONSUMED run ID reserved",
                "BLK_SYSTEM_264_NO_RUN_ID_RESERVED_OR_CONSUMED_RUNIDRESERVED",
            ],
            "metadata": {
                "run_id_consumption_authorized": True,
                "signatureGenerationAuthorized": True,
                "relayMessageDispatchAuthorized": True,
                "run_id_reserved_approved": True,
                "runIdConsumedAuthorized": True,
                "signatureGenerationApproved": True,
                "protectedBodyHashAuthorized": True,
                "signerStorageLedgerActionExecuted": True,
                "relayMessageDispatchExecuted": True,
                "kuronodeMutationExecuted": True,
                "runIdReservedIsApproved": True,
                "run_id_reserved_authorized": True,
                "run_id_consumed_approved": True,
                "runIdConsumedIsAuthorized": True,
                "signatureGenerationIsApproved": True,
                "protectedBodyHashIsAuthorized": True,
                "signerStorageLedgerActionIsExecuted": True,
                "relayMessageDispatchIsExecuted": True,
            },
        }

        errors = scan_for_authority_laundering(hostile)

        for marker in [
            "run id reserved",
            "runidreservationauthorized",
            "consumeatmostonerunid",
            "runidreserved",
            "signature generated",
            "protected body hashed",
            "protectedblkreqbodyhashingauthorized",
            "protectedbodyhashscanallowed",
            "signerstorageledgeraction",
            "runidreservationapproved",
            "runidconsumptionapproved",
            "signerstorageledgeractionapproved",
            "relaymessagedispatchauthorized",
            "relaymessagedispatchapproved",
            "kuronodemutationauthorized",
            "protectedbodyscanningauthorized",
            "protectedbodyhashingapproved",
            "runidreservationconsumptionapproved",
            "runidreservationisapproved",
            "runidconsumptionisapproved",
            "signerstorageledgeractionisapproved",
            "protectedbodyhashingisapproved",
            "protectedbodyscanningisauthorized",
            "kuronodemutationisauthorized",
            "runidreservationandconsumptionapproved",
            "protectedbodyscanauthorized",
            "kuronodemutationgranted",
            "runidreserved",
            "signaturegenerationapproved",
            "protectedbodyhashauthorized",
            "signerstorageledgeractionexecuted",
            "relaymessagedispatchexecuted",
            "kuronodemutationexecuted",
            "signaturegenerationisapproved",
            "protectedbodyhashisauthorized",
            "signerstorageledgeractionisexecuted",
            "relaymessagedispatchisexecuted",
            "kuronodemutationisexecuted",
            "record.notes[38]",
            "record.notes[39]",
            "run_id_consumption_authorized",
            "signatureGenerationAuthorized",
            "relayMessageDispatchAuthorized",
            "run_id_reserved_approved",
            "runIdConsumedAuthorized",
            "signatureGenerationApproved",
            "protectedBodyHashAuthorized",
            "signerStorageLedgerActionExecuted",
            "relayMessageDispatchExecuted",
            "kuronodeMutationExecuted",
            "runIdReservedIsApproved",
            "run_id_reserved_authorized",
            "run_id_consumed_approved",
            "runIdConsumedIsAuthorized",
            "signatureGenerationIsApproved",
            "protectedBodyHashIsAuthorized",
            "signerStorageLedgerActionIsExecuted",
            "relayMessageDispatchIsExecuted",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))

    def test_denial_prose_does_not_false_positive(self):
        safe = {
            "authority_cutline": (
                "No BEO publication, no RTM generation, no drift rejection, "
                "and no protected-body access are authorized by this preflight."
            ),
            "markers": [
                "NO_RUN_ID_RESERVED_OR_CONSUMED",
                "FUTURE_RUN_ID_RESERVED_NOT_CONSUMED",
                "ONE_RUN_ID_RESERVED_NOT_CONSUMED",
                "BLK_SYSTEM_264_NO_RUN_ID_RESERVED_OR_CONSUMED",
            ],
            "flags": {
                "run_id_reserved_approved": False,
                "runIdConsumedAuthorized": False,
            },
        }

        self.assertEqual(scan_for_authority_laundering(safe), [])


if __name__ == "__main__":
    unittest.main()
