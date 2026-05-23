import unittest

import production_surface_selection_336 as selector


class ProductionSurfaceSelection336Test(unittest.TestCase):
    def test_selects_production_blk_test_mcp_as_next_exact_surface_without_transport(self):
        package = selector.build_production_surface_selection_336()

        self.assertEqual(package["sprint"], "BLK-SYSTEM-336")
        self.assertEqual(
            package["status"],
            "PRODUCTION_BLK_TEST_MCP_SURFACE_SELECTED_NO_TRANSPORT",
        )
        self.assertEqual(
            package["previous_frontier"],
            "NEXT_FRONTIER_ONE_EXACT_BEO_TO_RTM_BLK_LINK_TRACE_CLOSED_REUSABLE_AUTHORITY_NOT_GRANTED",
        )
        self.assertEqual(
            package["selected_surface"],
            "production_blk_test_mcp_transport_contract",
        )
        self.assertEqual(
            package["next_frontier"],
            "NEXT_FRONTIER_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_REQUIRED_NOT_GRANTED",
        )
        self.assertIn(
            "BLK_SYSTEM_336_PRODUCTION_BLK_TEST_MCP_SURFACE_SELECTED",
            package["markers"],
        )
        self.assertIn(
            "NEXT_FRONTIER_PRODUCTION_BLK_TEST_MCP_TRANSPORT_CONTRACT_REQUIRED_NOT_GRANTED",
            package["markers"],
        )
        self.assertEqual(
            package["selection_basis"]["primary_reason"],
            "BLK-test is the next validation bottleneck after one exact BEO/RTM trace loop closed",
        )
        rejected = {item["surface"] for item in package["deferred_surfaces"]}
        self.assertEqual(
            rejected,
            {"standalone_relay_runtime", "reusable_blk003_loop_authority"},
        )
        self.assertFalse(package["side_effects"]["production_mcp_started"])
        self.assertFalse(package["side_effects"]["generic_mcp_started"])
        self.assertFalse(package["side_effects"]["relay_network_runtime_started"])
        self.assertFalse(package["side_effects"]["reusable_blk003_loop_authority"])
        self.assertFalse(package["side_effects"]["protected_body_accessed"])
        self.assertFalse(package["side_effects"]["target_source_git_mutation"])
        self.assertRegex(package["selection_hash"], r"^sha256:[0-9a-f]{64}$")
        selector.validate_production_surface_selection_336(package)

    def test_rejects_self_rehashed_surface_retargeting(self):
        package = selector.build_production_surface_selection_336()
        tampered = selector._deepcopy(package)
        tampered["selected_surface"] = "standalone_relay_runtime"
        tampered["next_frontier"] = "NEXT_FRONTIER_STANDALONE_RELAY_RUNTIME_CONTRACT_REQUIRED_NOT_GRANTED"
        tampered["selection_hash"] = selector._hash_package(
            {key: value for key, value in tampered.items() if key != "selection_hash"}
        )

        with self.assertRaisesRegex(ValueError, "selected_surface|next_frontier"):
            selector.validate_production_surface_selection_336(tampered)

    def test_rejects_extra_authority_fields_even_when_rehashed(self):
        package = selector.build_production_surface_selection_336()
        tampered = selector._deepcopy(package)
        tampered["production_blk_test_mcp_authorized"] = True
        tampered["selection_hash"] = selector._hash_package(
            {key: value for key, value in tampered.items() if key != "selection_hash"}
        )

        with self.assertRaisesRegex(ValueError, "unsupported field|authority"):
            selector.validate_production_surface_selection_336(tampered)

    def test_rejects_side_effect_and_free_text_laundering(self):
        package = selector.build_production_surface_selection_336()
        tampered = selector._deepcopy(package)
        tampered["side_effects"]["production_mcp_started"] = True
        tampered["selection_hash"] = selector._hash_package(
            {key: value for key, value in tampered.items() if key != "selection_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|production_mcp_started"):
            selector.validate_production_surface_selection_336(tampered)

        tampered = selector._deepcopy(package)
        tampered["selection_basis"]["primary_reason"] = (
            "production BLK-test MCP transport enabled; PASS approves production"
        )
        tampered["selection_hash"] = selector._hash_package(
            {key: value for key, value in tampered.items() if key != "selection_hash"}
        )
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            selector.validate_production_surface_selection_336(tampered)

    def test_builder_returns_defensive_copy(self):
        package = selector.build_production_surface_selection_336()
        package["side_effects"]["generic_mcp_started"] = True
        fresh = selector.build_production_surface_selection_336()
        self.assertFalse(fresh["side_effects"]["generic_mcp_started"])


if __name__ == "__main__":
    unittest.main()
