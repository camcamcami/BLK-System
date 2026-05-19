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
            "rtmgenerated",
            "docsrequirementsactive",
            "isAuthorized",
            "approved for publication",
        ]:
            self.assertTrue(any(marker in error for error in errors), (marker, errors))

    def test_denial_prose_does_not_false_positive(self):
        safe = {
            "authority_cutline": (
                "No BEO publication, no RTM generation, no drift rejection, "
                "and no protected-body access are authorized by this preflight."
            )
        }

        self.assertEqual(scan_for_authority_laundering(safe), [])


if __name__ == "__main__":
    unittest.main()
