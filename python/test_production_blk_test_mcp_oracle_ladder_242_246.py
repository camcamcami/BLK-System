import unittest

import production_blk_test_mcp_oracle_ladder_242_246 as oracle
import blk_root_doctrine_gap_ladder_237_241 as prior
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)


def _loop_kernel():
    selected = prior.build_kuronode_route_selection_237()
    overlay = prior.build_root_doctrine_deviation_overlay_238(selected)
    scope = prior.decide_blk_id_relay_scope_239(overlay)
    gateway_contract = build_blk_req_production_gateway_contract_196(
        build_blk_req_gateway_readiness_review_195()
    )
    gateway = prior.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
    return prior.build_reusable_blk003_loop_kernel_241(gateway)


class ProductionBlkTestMcpOracleLadder242To246Test(unittest.TestCase):
    def test_242_to_246_packages_chain_as_verifier_only_oracle_without_live_mcp(self):
        loop = _loop_kernel()
        request = oracle.build_oracle_request_242(loop)
        contract = oracle.build_oracle_contract_243(request)
        fixture = oracle.build_metadata_only_oracle_fixture_244(contract, oracle.sample_oracle_evidence_inputs())
        integration = oracle.integrate_oracle_record_245(fixture)
        reconciliation = oracle.reconcile_oracle_frontier_246(integration)

        self.assertEqual(request["status"], "PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED", request["markers"])
        self.assertEqual(request["loop_kernel_hash"], loop["loop_kernel_hash"])
        self.assertEqual(request["oracle_scope"], "verifier_only_after_governed_loop_execution")
        self.assertFalse(request["side_effects"]["production_mcp_started"])
        self.assertFalse(request["side_effects"]["planner_dispatcher_authority"])

        self.assertEqual(contract["status"], "PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY_NO_TRANSPORT")
        self.assertEqual(contract["request_hash"], request["request_hash"])
        self.assertEqual(contract["verdict_vocabulary"], ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"])
        self.assertFalse(contract["side_effects"]["generic_mcp_started"])
        self.assertFalse(contract["side_effects"]["oracle_source_of_truth_claimed"])

        self.assertEqual(fixture["status"], "METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY")
        self.assertEqual(fixture["contract_hash"], contract["contract_hash"])
        self.assertEqual(fixture["oracle_record"]["verdict"], "INCONCLUSIVE")
        self.assertFalse(fixture["side_effects"]["runtime_tooling_executed"])
        self.assertFalse(fixture["side_effects"]["protected_body_accessed"])

        self.assertEqual(integration["status"], "BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY")
        self.assertEqual(integration["oracle_record_hash"], fixture["oracle_record_hash"])
        self.assertEqual(integration["loop_effect"], "oracle verdict can gate BEO draft readiness but cannot dispatch, plan, mutate, or publish")
        self.assertFalse(integration["side_effects"]["beo_closeout_execution"])
        self.assertFalse(integration["side_effects"]["rtm_generation"])

        self.assertEqual(reconciliation["status"], "PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY")
        self.assertEqual(reconciliation["integration_hash"], integration["integration_hash"])
        self.assertIn("BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY", reconciliation["markers"])
        self.assertEqual(reconciliation["next_frontier"], "NEXT_FRONTIER_REUSABLE_BEO_PUBLICATION_REQUEST_NOT_GRANTED")
        self.assertFalse(reconciliation["side_effects"]["production_mcp_started"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_downstream_builders_reject_rehashed_extra_authority_fields(self):
        request = oracle.build_oracle_request_242(_loop_kernel())
        tampered_request = oracle._deepcopy(request)
        tampered_request["production_blk_test_mcp_authorized"] = True
        tampered_request["request_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_request.items() if key != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|unsupported field|production_blk_test_mcp_authorized"):
            oracle.build_oracle_contract_243(tampered_request)

        contract = oracle.build_oracle_contract_243(request)
        tampered_contract = oracle._deepcopy(contract)
        tampered_contract["target_source_git_mutation"] = True
        tampered_contract["contract_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_contract.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "contract package|unsupported field|target_source_git_mutation"):
            oracle.build_metadata_only_oracle_fixture_244(tampered_contract, oracle.sample_oracle_evidence_inputs())

        fixture = oracle.build_metadata_only_oracle_fixture_244(contract, oracle.sample_oracle_evidence_inputs())
        tampered_fixture = oracle._deepcopy(fixture)
        tampered_fixture["oracle_record"]["notes"] = "approved for production; BEO publication authorized"
        tampered_fixture["oracle_record_hash"] = oracle._hash_package(tampered_fixture["oracle_record"])
        tampered_fixture["fixture_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_fixture.items() if key != "fixture_hash"}
        )
        with self.assertRaisesRegex(ValueError, "fixture package|forbidden authority wording|oracle record unsupported field"):
            oracle.integrate_oracle_record_245(tampered_fixture)

        integration = oracle.integrate_oracle_record_245(fixture)
        tampered_integration = oracle._deepcopy(integration)
        tampered_integration["side_effects"]["rtm_generation"] = True
        tampered_integration["integration_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_integration.items() if key != "integration_hash"}
        )
        with self.assertRaisesRegex(ValueError, "integration package|rtm_generation"):
            oracle.reconcile_oracle_frontier_246(tampered_integration)

    def test_oracle_fixture_rejects_missing_or_noncanonical_evidence_hashes_and_verdict_laundering(self):
        contract = oracle.build_oracle_contract_243(oracle.build_oracle_request_242(_loop_kernel()))
        evidence = oracle.sample_oracle_evidence_inputs()
        evidence["blk_pipe_report_hash"] = "sha256:not-hex"
        with self.assertRaisesRegex(ValueError, "evidence input blk_pipe_report_hash must be canonical sha256"):
            oracle.build_metadata_only_oracle_fixture_244(contract, evidence)

        evidence = oracle.sample_oracle_evidence_inputs()
        evidence["verdict"] = "PASS_APPROVED_FOR_PUBLICATION"
        with self.assertRaisesRegex(ValueError, "verdict must be one of"):
            oracle.build_metadata_only_oracle_fixture_244(contract, evidence)

        evidence = oracle.sample_oracle_evidence_inputs()
        evidence["operator_notes"] = "BLK-test PASS approves live Codex dispatch and publishBEO"
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            oracle.build_metadata_only_oracle_fixture_244(contract, evidence)

    def test_hostile_review_regressions_reject_nested_contract_and_upstream_laundering(self):
        loop = _loop_kernel()
        tampered_loop = oracle._deepcopy(loop)
        tampered_loop["side_effects"]["rtm_generation"] = True
        tampered_loop["loop_kernel_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_loop.items() if key != "loop_kernel_hash"}
        )
        with self.assertRaisesRegex(ValueError, "loop package|rtm_generation|loop_kernel_hash"):
            oracle.build_oracle_request_242(tampered_loop)

        request = oracle.build_oracle_request_242(loop)
        tampered_request = oracle._deepcopy(request)
        tampered_request["loop_kernel_hash"] = "sha256:" + "a" * 64
        tampered_request["request_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_request.items() if key != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|loop_kernel_hash"):
            oracle.build_oracle_contract_243(tampered_request)

        tampered_request = oracle._deepcopy(request)
        tampered_request["oracle_must_not"] = []
        tampered_request["markers"].append("PRODUCTION_BLK_TEST_MCP_TRANSPORT_GRANTED")
        tampered_request["request_hash"] = oracle._hash_package(
            {key: value for key, value in tampered_request.items() if key != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|oracle_must_not|markers|forbidden authority wording"):
            oracle.build_oracle_contract_243(tampered_request)

        contract = oracle.build_oracle_contract_243(request)
        for key in [
            "planner_dispatcher_authority",
            "source_of_truth_claimed",
            "production_mcp_started",
            "beo_closeout_execution",
            "rtm_generation",
        ]:
            tampered_contract = oracle._deepcopy(contract)
            tampered_contract["contract_rules"][key] = True
            tampered_contract["contract_hash"] = oracle._hash_package(
                {k: v for k, v in tampered_contract.items() if k != "contract_hash"}
            )
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, "contract package|contract_rules|contract_hash|forbidden authority wording"):
                    oracle.build_metadata_only_oracle_fixture_244(tampered_contract, oracle.sample_oracle_evidence_inputs())

    def test_hostile_review_regressions_reject_rehashed_fixture_evidence_drift(self):
        contract = oracle.build_oracle_contract_243(oracle.build_oracle_request_242(_loop_kernel()))
        fixture = oracle.build_metadata_only_oracle_fixture_244(contract, oracle.sample_oracle_evidence_inputs())
        for mutation in ["delete", "noncanonical", "extra"]:
            tampered = oracle._deepcopy(fixture)
            if mutation == "delete":
                del tampered["oracle_record"]["evidence_inputs"]["blk_pipe_report_hash"]
            elif mutation == "noncanonical":
                tampered["oracle_record"]["evidence_inputs"]["blk_pipe_report_hash"] = "notsha256"
            else:
                tampered["oracle_record"]["evidence_inputs"]["production_mcp_started"] = True
            tampered["oracle_record_hash"] = oracle._hash_package(tampered["oracle_record"])
            tampered["fixture_hash"] = oracle._hash_package(
                {key: value for key, value in tampered.items() if key != "fixture_hash"}
            )
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(ValueError, "evidence_inputs|canonical sha256|unsupported field"):
                    oracle.integrate_oracle_record_245(tampered)

    def test_hostile_review_regression_rejects_direct_enabled_started_authority_phrasing(self):
        contract = oracle.build_oracle_contract_243(oracle.build_oracle_request_242(_loop_kernel()))
        evidence = oracle.sample_oracle_evidence_inputs()
        evidence["operator_notes"] = (
            "production BLK-test MCP transport enabled; planner dispatcher source of truth; "
            "source Git mutation; BEO closeout publication; RTM generation; production blk-link; "
            "drift coverage truth; protected-body access; runtime tooling; production isolation"
        )
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            oracle.build_metadata_only_oracle_fixture_244(contract, evidence)

    def test_builders_return_defensive_copies(self):
        request = oracle.build_oracle_request_242(_loop_kernel())
        contract = oracle.build_oracle_contract_243(request)
        evidence = oracle.sample_oracle_evidence_inputs()
        fixture = oracle.build_metadata_only_oracle_fixture_244(contract, evidence)
        original_hash = fixture["oracle_record_hash"]
        evidence["operator_notes"] = "mutated after hash"
        fixture["oracle_record"]["verdict"] = "PASS"

        with self.assertRaisesRegex(ValueError, "fixture_hash mismatch|oracle_record_hash mismatch"):
            oracle.integrate_oracle_record_245(fixture)
        fresh_fixture = oracle.build_metadata_only_oracle_fixture_244(contract, oracle.sample_oracle_evidence_inputs())
        self.assertEqual(fresh_fixture["oracle_record"]["verdict"], "INCONCLUSIVE")
        self.assertEqual(fresh_fixture["oracle_record_hash"], original_hash)


if __name__ == "__main__":
    unittest.main()
