import unittest

import production_blk_test_mcp_transport_contract_337 as contract


class ProductionBlkTestMcpTransportContract337Test(unittest.TestCase):
    def test_builds_occam_transport_contract_ready_for_e2e_validation_request_only(self):
        package = contract.build_transport_contract_337()

        self.assertEqual(package["sprint"], "BLK-SYSTEM-337")
        self.assertEqual(
            package["status"],
            "PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_READY_NO_SERVER_START",
        )
        self.assertEqual(
            package["previous_frontier"],
            "NEXT_FRONTIER_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_REQUIRED_NOT_GRANTED",
        )
        self.assertEqual(
            package["prior_selection_hash"],
            "sha256:64e618ba82233f4940d8c1ce1dc94d4a37d28127a8dd570d10b76e77e58faeab",
        )
        self.assertEqual(
            package["next_frontier"],
            "NEXT_FRONTIER_OCCAM_END_TO_END_VALIDATION_RUN_REQUIRED_NOT_STARTED",
        )
        self.assertIn(
            "BLK_SYSTEM_337_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_READY",
            package["markers"],
        )
        self.assertEqual(package["transport_profile"]["protocol"], "stdio-jsonl-mcp-subset")
        self.assertEqual(
            package["transport_profile"]["methods"],
            ["initialize", "tools/list", "tools/call"],
        )
        self.assertEqual(package["fixed_tool_registry"], ["run_ast_validation"])
        self.assertEqual(package["verdict_vocabulary"], ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"])
        self.assertTrue(package["e2e_validation_readiness"]["contract_ready_for_exact_future_run_request"])
        self.assertFalse(package["e2e_validation_readiness"]["run_started"])
        self.assertTrue(package["e2e_validation_readiness"]["separate_operator_runtime_gate_required"])
        for value in package["side_effects"].values():
            self.assertIs(value, False)
        self.assertRegex(package["contract_hash"], r"^sha256:[0-9a-f]{64}$")
        contract.validate_transport_contract_337(package)

    def test_rejects_rehashed_server_start_or_tool_expansion(self):
        package = contract.build_transport_contract_337()
        tampered = contract._deepcopy(package)
        tampered["side_effects"]["server_started"] = True
        tampered["contract_hash"] = contract._hash_package(
            {key: value for key, value in tampered.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|server_started"):
            contract.validate_transport_contract_337(tampered)

        tampered = contract._deepcopy(package)
        tampered["fixed_tool_registry"].append("shell")
        tampered["contract_hash"] = contract._hash_package(
            {key: value for key, value in tampered.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "fixed_tool_registry"):
            contract.validate_transport_contract_337(tampered)

    def test_rejects_laundered_pass_as_approval_and_transport_enabled_wording(self):
        package = contract.build_transport_contract_337()
        tampered = contract._deepcopy(package)
        tampered["transport_profile"]["workspace_policy"] = (
            "PASS approves production and production BLK-test MCP transport enabled"
        )
        tampered["contract_hash"] = contract._hash_package(
            {key: value for key, value in tampered.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            contract.validate_transport_contract_337(tampered)

    def test_rejects_noncanonical_evidence_inputs(self):
        package = contract.build_transport_contract_337()
        tampered = contract._deepcopy(package)
        tampered["required_evidence_inputs"][0]["hash"] = "not-sha256"
        tampered["contract_hash"] = contract._hash_package(
            {key: value for key, value in tampered.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical sha256"):
            contract.validate_transport_contract_337(tampered)

    def test_builder_returns_defensive_copy(self):
        package = contract.build_transport_contract_337()
        package["side_effects"]["server_started"] = True
        fresh = contract.build_transport_contract_337()
        self.assertFalse(fresh["side_effects"]["server_started"])


if __name__ == "__main__":
    unittest.main()
