import unittest
from copy import deepcopy
from pathlib import Path

from lint_artifacts import (
    BLK_REQ_DENIED_AUTHORITIES,
    build_legislative_gateway_contract,
    validate_legislative_gateway_contract,
)

ROOT = Path(__file__).resolve().parents[1]
BLK116 = ROOT / "docs" / "BLK-116_blk-req-legislative-gateway-contract.md"


class BlkReqLegislativeGatewayContractTest(unittest.TestCase):
    def test_contract_pins_allowed_gateway_slices_without_adjacent_authority(self):
        contract = build_legislative_gateway_contract()

        self.assertEqual(contract["contract_marker"], "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT")
        self.assertEqual(contract["contract_status"], "CONTRACT_READY_NOT_EXECUTION_AUTHORITY")
        self.assertEqual(
            contract["allowed_local_backend_operations"],
            [
                "BLK_SYSTEM_117_STAGING_LINTER",
                "BLK_SYSTEM_118_STAGING_DRAFT_WRITER",
                "BLK_SYSTEM_119_CANONICAL_VERSION_HASH_ENGINE",
            ],
        )
        self.assertEqual(set(contract["denied_authorities"]), BLK_REQ_DENIED_AUTHORITIES)
        self.assertEqual(len(contract["denied_authorities"]), len(BLK_REQ_DENIED_AUTHORITIES))

        for flag, value in contract["side_effect_flags"].items():
            self.assertIs(value, False, flag)

        self.assertEqual(validate_legislative_gateway_contract(contract), [])

    def test_contract_validation_rejects_missing_extra_or_true_denied_authority_surfaces(self):
        base = build_legislative_gateway_contract()

        missing = deepcopy(base)
        missing["denied_authorities"] = missing["denied_authorities"][:-1]
        self.assertIn("denied_authorities must match exact BLK-116 set", validate_legislative_gateway_contract(missing))

        extra = deepcopy(base)
        extra["denied_authorities"].append("APPROVED_FOR_LIVE_EXECUTION")
        self.assertIn("denied_authorities must match exact BLK-116 set", validate_legislative_gateway_contract(extra))

        true_flag = deepcopy(base)
        true_flag["side_effect_flags"]["rtm_generation_performed"] = True
        self.assertIn("side_effect_flags.rtm_generation_performed must remain false", validate_legislative_gateway_contract(true_flag))

    def test_contract_validation_rejects_nested_authority_laundering_wording(self):
        contract = build_legislative_gateway_contract()
        contract["notes"].append({"operator_summary": "runtime execution approved; BEO publication granted"})

        errors = validate_legislative_gateway_contract(contract)

        self.assertTrue(any("runtimeexecutionapproved" in error for error in errors), errors)
        self.assertTrue(any("beopublicationgranted" in error for error in errors), errors)

    def test_blk116_boundary_doc_pins_contract_markers(self):
        self.assertTrue(BLK116.exists(), "BLK-116 boundary record missing")
        text = BLK116.read_text()
        required = [
            "BLK_SYSTEM_116_BLK_REQ_LEGISLATIVE_GATEWAY_CONTRACT",
            "CONTRACT_READY_NOT_EXECUTION_AUTHORITY",
            "ALLOWED_LOCAL_BACKEND_OPERATIONS_117_118_119_ONLY",
            "DENIED_ADJACENT_AUTHORITIES_EXACT_SET_PINNED",
            "NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_116",
            "BLK-test is a BLK-System functional module, not BLK-System's test suite",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-116 missing markers: {missing}")


if __name__ == "__main__":
    unittest.main()
