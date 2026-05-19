import unittest

import blk_root_doctrine_gap_ladder_237_241 as ladder
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)


class BlkRootDoctrineGapLadder237To241Test(unittest.TestCase):
    def test_237_to_241_packages_chain_without_adjacent_authority(self):
        selected = ladder.build_kuronode_route_selection_237()
        overlay = ladder.build_root_doctrine_deviation_overlay_238(selected)
        scope = ladder.decide_blk_id_relay_scope_239(overlay)
        gateway_contract = build_blk_req_production_gateway_contract_196(
            build_blk_req_gateway_readiness_review_195()
        )
        gateway = ladder.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
        loop = ladder.build_reusable_blk003_loop_kernel_241(gateway)

        self.assertEqual(selected["status"], "KURONODE_FEATURE_DROP_ROUTE_SELECTED_NO_DISPATCH")
        self.assertIn("BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY", selected["markers"])
        self.assertFalse(selected["side_effects"]["kuronode_source_git_mutation"])
        self.assertFalse(selected["side_effects"]["live_codex_dispatch"])
        self.assertFalse(selected["side_effects"]["blk_pipe_runtime"])
        self.assertTrue(selected["next_exact_payload_required"])

        self.assertEqual(overlay["status"], "ROOT_DOCTRINE_DEVIATION_OVERLAY_READY")
        self.assertEqual(
            set(overlay["deviations_normalized"]),
            {
                "split_active_vault_paths",
                "current_codex_workspace_write_argv",
                "repository_owned_validation_profiles",
                "lean_beb_l2_helper_not_full_blk003_loop",
            },
        )
        self.assertFalse(overlay["side_effects"]["root_docs_modified"])

        self.assertEqual(scope["status"], "BLK_ID_RELAY_SCOPE_DECIDED")
        self.assertEqual(scope["blk_id_scope"], "target_architecture_name_boxed_until_service_charter")
        self.assertEqual(scope["blk_relay_scope"], "target_architecture_name_boxed_until_service_charter")
        self.assertFalse(scope["side_effects"]["standalone_blk_id_service_created"])
        self.assertFalse(scope["side_effects"]["standalone_blk_relay_service_created"])

        self.assertEqual(gateway["status"], "HITL_GATEWAY_COMPLETION_SLICE_READY")
        self.assertIn("retrieve_active_artifact_by_exact_id", gateway["allowed_gateway_operations"])
        self.assertTrue(gateway["approval_capture_required_per_operation"])
        self.assertFalse(gateway["side_effects"]["protected_body_access_without_exact_id"])
        self.assertFalse(gateway["side_effects"]["broad_gateway_runtime"])

        self.assertEqual(loop["status"], "REUSABLE_BLK003_LOOP_KERNEL_READY")
        self.assertEqual(loop["iteration_contract"]["failure_ceiling"], 3)
        self.assertEqual(loop["iteration_contract"]["route"], "BEB-L2 -> BLK-pipe -> Codex workspace-write")
        self.assertTrue(loop["iteration_contract"]["approval_required_per_iteration"])
        self.assertFalse(loop["side_effects"]["loop_runtime_execution"])
        self.assertFalse(loop["side_effects"]["beo_closeout_execution"])
        self.assertFalse(loop["side_effects"]["reusable_codex_dispatch"])
        self.assertRegex(loop["loop_kernel_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_downstream_builders_reject_rehashed_authority_laundering(self):
        selected = ladder.build_kuronode_route_selection_237()
        tampered = ladder._deepcopy(selected)
        tampered["side_effects"]["live_codex_dispatch"] = True
        tampered["markers"].append("BEO_PUBLICATION_AUTHORIZED")
        tampered["selection_hash"] = ladder._hash_package(
            {key: value for key, value in tampered.items() if key != "selection_hash"}
        )
        with self.assertRaisesRegex(ValueError, "selection package|forbidden authority wording|live_codex_dispatch"):
            ladder.build_root_doctrine_deviation_overlay_238(tampered)

        overlay = ladder.build_root_doctrine_deviation_overlay_238(selected)
        tampered_overlay = ladder._deepcopy(overlay)
        tampered_overlay["side_effects"]["root_docs_modified"] = True
        tampered_overlay["notes"] = "approved for production and reusable Codex dispatch"
        tampered_overlay["overlay_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_overlay.items() if key != "overlay_hash"}
        )
        with self.assertRaisesRegex(ValueError, "overlay package|forbidden authority wording|root_docs_modified"):
            ladder.decide_blk_id_relay_scope_239(tampered_overlay)

    def test_rehashed_extra_authority_fields_are_rejected_at_every_boundary(self):
        selected = ladder.build_kuronode_route_selection_237()
        tampered_selected = ladder._deepcopy(selected)
        tampered_selected["kuronode_source_git_mutation"] = True
        tampered_selected["selection_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_selected.items() if key != "selection_hash"}
        )
        with self.assertRaisesRegex(ValueError, "selection package|unsupported field|kuronode_source_git_mutation"):
            ladder.build_root_doctrine_deviation_overlay_238(tampered_selected)

        overlay = ladder.build_root_doctrine_deviation_overlay_238(selected)
        scope = ladder.decide_blk_id_relay_scope_239(overlay)
        tampered_scope = ladder._deepcopy(scope)
        tampered_scope["protected_body_access_without_exact_id"] = True
        tampered_scope["scope_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_scope.items() if key != "scope_hash"}
        )
        gateway_contract = build_blk_req_production_gateway_contract_196(
            build_blk_req_gateway_readiness_review_195()
        )
        with self.assertRaisesRegex(ValueError, "scope package|unsupported field|protected_body_access_without_exact_id"):
            ladder.build_hitl_gateway_completion_slice_240(tampered_scope, gateway_contract)

        gateway = ladder.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
        tampered_gateway = ladder._deepcopy(gateway)
        tampered_gateway["production_blk_test_mcp"] = True
        tampered_gateway["gateway_slice_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_gateway.items() if key != "gateway_slice_hash"}
        )
        with self.assertRaisesRegex(ValueError, "gateway package|unsupported field|production_blk_test_mcp"):
            ladder.build_reusable_blk003_loop_kernel_241(tampered_gateway)

        tampered_contract = ladder._deepcopy(gateway_contract)
        tampered_contract["target_source_git_mutation"] = True
        tampered_contract["contract_package_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_contract.items() if key != "contract_package_hash"}
        )
        with self.assertRaisesRegex(ValueError, "gateway contract|unsupported field|target_source_git_mutation"):
            ladder.build_hitl_gateway_completion_slice_240(scope, tampered_contract)

    def test_gateway_and_loop_require_canonical_upstream_hashes_and_exact_false_flags(self):
        selected = ladder.build_kuronode_route_selection_237()
        overlay = ladder.build_root_doctrine_deviation_overlay_238(selected)
        scope = ladder.decide_blk_id_relay_scope_239(overlay)
        tampered_scope = ladder._deepcopy(scope)
        tampered_scope["side_effects"]["standalone_blk_relay_service_created"] = True
        tampered_scope["scope_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_scope.items() if key != "scope_hash"}
        )
        gateway_contract = build_blk_req_production_gateway_contract_196(
            build_blk_req_gateway_readiness_review_195()
        )
        with self.assertRaisesRegex(ValueError, "scope package|standalone_blk_relay_service_created"):
            ladder.build_hitl_gateway_completion_slice_240(tampered_scope, gateway_contract)

        gateway = ladder.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
        tampered_gateway = ladder._deepcopy(gateway)
        tampered_gateway["side_effects"]["broad_gateway_runtime"] = True
        tampered_gateway["allowed_gateway_operations"].append("broad_active_vault_scan")
        tampered_gateway["gateway_slice_hash"] = ladder._hash_package(
            {key: value for key, value in tampered_gateway.items() if key != "gateway_slice_hash"}
        )
        with self.assertRaisesRegex(ValueError, "gateway package|broad_gateway_runtime|allowed_gateway_operations"):
            ladder.build_reusable_blk003_loop_kernel_241(tampered_gateway)


if __name__ == "__main__":
    unittest.main()
