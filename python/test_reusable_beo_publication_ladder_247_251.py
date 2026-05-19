import unittest

import production_blk_test_mcp_oracle_ladder_242_246 as oracle
import blk_root_doctrine_gap_ladder_237_241 as prior
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)

import reusable_beo_publication_ladder_247_251 as reusable_beo


def _loop_kernel():
    selected = prior.build_kuronode_route_selection_237()
    overlay = prior.build_root_doctrine_deviation_overlay_238(selected)
    scope = prior.decide_blk_id_relay_scope_239(overlay)
    gateway_contract = build_blk_req_production_gateway_contract_196(
        build_blk_req_gateway_readiness_review_195()
    )
    gateway = prior.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
    return prior.build_reusable_blk003_loop_kernel_241(gateway)


def _oracle_reconciliation():
    request = oracle.build_oracle_request_242(_loop_kernel())
    contract = oracle.build_oracle_contract_243(request)
    fixture = oracle.build_metadata_only_oracle_fixture_244(
        contract, oracle.sample_oracle_evidence_inputs()
    )
    integration = oracle.integrate_oracle_record_245(fixture)
    return oracle.reconcile_oracle_frontier_246(integration)


class ReusableBeoPublicationLadder247To251Test(unittest.TestCase):
    def test_247_to_251_packages_chain_as_reusable_beo_publication_review_kernel(self):
        reconciliation = _oracle_reconciliation()
        request = reusable_beo.build_reusable_beo_publication_request_247(reconciliation)
        contract = reusable_beo.build_reusable_beo_publication_contract_248(request)
        pilot = reusable_beo.build_exact_beo_publication_dry_run_249(
            contract, reusable_beo.sample_beo_publication_candidate_inputs()
        )
        integration = reusable_beo.integrate_beo_publication_review_250(pilot)
        final = reusable_beo.reconcile_reusable_beo_publication_frontier_251(integration)

        self.assertEqual(request["status"], "REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED_NOT_GRANTED")
        self.assertEqual(request["oracle_reconciliation_hash"], reconciliation["reconciliation_hash"])
        self.assertIn("BLK_SYSTEM_247_REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED", request["markers"])
        self.assertFalse(request["side_effects"]["reusable_beo_publication_authorized"])
        self.assertFalse(request["side_effects"]["signer_reuse_authorized"])

        self.assertEqual(contract["status"], "REUSABLE_BEO_PUBLICATION_CONTRACT_READY_PER_RUN_EXACT_APPROVAL")
        self.assertEqual(contract["request_hash"], request["request_hash"])
        self.assertTrue(contract["contract_rules"]["per_run_exact_approval_required"])
        self.assertTrue(contract["contract_rules"]["blk_test_pass_is_not_publication_approval"])
        self.assertIn("READY_FOR_OPERATOR_REVIEW", contract["publication_record_states"])
        self.assertFalse(contract["side_effects"]["future_run_authorized"])

        self.assertEqual(pilot["status"], "EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY_NOT_PUBLISHED")
        self.assertEqual(pilot["contract_hash"], contract["contract_hash"])
        self.assertEqual(pilot["candidate_record"]["oracle_verdict"], "PASS")
        self.assertEqual(pilot["candidate_record"]["publication_record_state"], "READY_FOR_OPERATOR_REVIEW")
        self.assertFalse(pilot["side_effects"]["beo_published"])
        self.assertFalse(pilot["side_effects"]["public_ledger_mutated"])

        self.assertEqual(integration["status"], "BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY")
        self.assertEqual(integration["candidate_record_hash"], pilot["candidate_record_hash"])
        self.assertEqual(
            integration["loop_effect"],
            "BEO publication candidate can be reviewed after oracle evidence but cannot publish, sign, store, ledger, mutate, or generate RTM",
        )
        self.assertFalse(integration["side_effects"]["beo_closeout_execution"])
        self.assertFalse(integration["side_effects"]["rtm_generation"])

        self.assertEqual(final["status"], "REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY")
        self.assertEqual(final["integration_hash"], integration["integration_hash"])
        self.assertIn("BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY", final["markers"])
        self.assertEqual(final["next_frontier"], "NEXT_FRONTIER_RTM_PRODUCTION_BLK_LINK_DRIFT_COVERAGE_REQUEST_NOT_GRANTED")
        self.assertFalse(final["side_effects"]["reusable_beo_publication_authorized"])
        self.assertRegex(final["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_downstream_builders_reject_rehashed_extra_authority_fields(self):
        reconciliation = _oracle_reconciliation()
        tampered_reconciliation = reusable_beo._deepcopy(reconciliation)
        tampered_reconciliation["reusable_beo_publication_authorized"] = True
        tampered_reconciliation["reconciliation_hash"] = reusable_beo._hash_package(
            {k: v for k, v in tampered_reconciliation.items() if k != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(ValueError, "oracle reconciliation|unsupported field|reconciliation_hash"):
            reusable_beo.build_reusable_beo_publication_request_247(tampered_reconciliation)

        request = reusable_beo.build_reusable_beo_publication_request_247(reconciliation)
        tampered_request = reusable_beo._deepcopy(request)
        tampered_request["publication_authorized"] = True
        tampered_request["request_hash"] = reusable_beo._hash_package(
            {k: v for k, v in tampered_request.items() if k != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|unsupported field|publication_authorized"):
            reusable_beo.build_reusable_beo_publication_contract_248(tampered_request)

        contract = reusable_beo.build_reusable_beo_publication_contract_248(request)
        tampered_contract = reusable_beo._deepcopy(contract)
        tampered_contract["contract_rules"]["blk_test_pass_is_publication_approval"] = True
        tampered_contract["contract_hash"] = reusable_beo._hash_package(
            {k: v for k, v in tampered_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "contract package|contract_rules|forbidden authority wording"):
            reusable_beo.build_exact_beo_publication_dry_run_249(
                tampered_contract, reusable_beo.sample_beo_publication_candidate_inputs()
            )

        pilot = reusable_beo.build_exact_beo_publication_dry_run_249(
            contract, reusable_beo.sample_beo_publication_candidate_inputs()
        )
        tampered_pilot = reusable_beo._deepcopy(pilot)
        tampered_pilot["candidate_record"]["nested"] = {"signerKeyMaterial": "stored"}
        tampered_pilot["candidate_record_hash"] = reusable_beo._hash_package(tampered_pilot["candidate_record"])
        tampered_pilot["pilot_hash"] = reusable_beo._hash_package(
            {k: v for k, v in tampered_pilot.items() if k != "pilot_hash"}
        )
        with self.assertRaisesRegex(ValueError, "pilot package|candidate record|forbidden authority wording|unsupported field"):
            reusable_beo.integrate_beo_publication_review_250(tampered_pilot)

        integration = reusable_beo.integrate_beo_publication_review_250(pilot)
        tampered_integration = reusable_beo._deepcopy(integration)
        tampered_integration["side_effects"]["rtm_generation"] = True
        tampered_integration["integration_hash"] = reusable_beo._hash_package(
            {k: v for k, v in tampered_integration.items() if k != "integration_hash"}
        )
        with self.assertRaisesRegex(ValueError, "integration package|rtm_generation"):
            reusable_beo.reconcile_reusable_beo_publication_frontier_251(tampered_integration)

    def test_candidate_inputs_reject_pass_as_approval_and_publication_laundering(self):
        contract = reusable_beo.build_reusable_beo_publication_contract_248(
            reusable_beo.build_reusable_beo_publication_request_247(_oracle_reconciliation())
        )
        candidate = reusable_beo.sample_beo_publication_candidate_inputs()
        candidate["oracle_verdict"] = "PASS_APPROVED_FOR_PUBLICATION"
        with self.assertRaisesRegex(ValueError, "oracle_verdict must be one of"):
            reusable_beo.build_exact_beo_publication_dry_run_249(contract, candidate)

        candidate = reusable_beo.sample_beo_publication_candidate_inputs()
        candidate["operator_notes"] = "BLK-test PASS approved for publication; publishBEO; BEO publication authorized"
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            reusable_beo.build_exact_beo_publication_dry_run_249(contract, candidate)

        candidate = reusable_beo.sample_beo_publication_candidate_inputs()
        candidate["signature_receipt_hash"] = "sha256:nothex"
        with self.assertRaisesRegex(ValueError, "signature_receipt_hash must be canonical sha256"):
            reusable_beo.build_exact_beo_publication_dry_run_249(contract, candidate)

    def test_contract_requires_exact_denials_and_record_only_policy(self):
        request = reusable_beo.build_reusable_beo_publication_request_247(_oracle_reconciliation())
        contract = reusable_beo.build_reusable_beo_publication_contract_248(request)

        for mutation in ["remove_denial", "duplicate_denial", "extra_denial", "policy_missing_false"]:
            tampered = reusable_beo._deepcopy(contract)
            if mutation == "remove_denial":
                tampered["denied_authorities"] = tampered["denied_authorities"][:-1]
            elif mutation == "duplicate_denial":
                tampered["denied_authorities"].append(tampered["denied_authorities"][0])
            elif mutation == "extra_denial":
                tampered["denied_authorities"].append("APPROVED_FOR_PUBLICATION")
            else:
                del tampered["record_only_policy"]["public_ledger_mutated"]
            tampered["contract_hash"] = reusable_beo._hash_package(
                {k: v for k, v in tampered.items() if k != "contract_hash"}
            )
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(ValueError, "contract_hash mismatch|denied_authorities|record_only_policy|forbidden authority wording"):
                    reusable_beo.build_exact_beo_publication_dry_run_249(
                        tampered, reusable_beo.sample_beo_publication_candidate_inputs()
                    )

    def test_hostile_review_rejects_self_consistent_forged_upstream_hashes(self):
        request = reusable_beo.build_reusable_beo_publication_request_247(_oracle_reconciliation())
        contract = reusable_beo.build_reusable_beo_publication_contract_248(request)
        pilot = reusable_beo.build_exact_beo_publication_dry_run_249(
            contract, reusable_beo.sample_beo_publication_candidate_inputs()
        )
        integration = reusable_beo.integrate_beo_publication_review_250(pilot)

        forged_contract = reusable_beo._deepcopy(contract)
        forged_contract["request_hash"] = "sha256:" + "0" * 64
        forged_contract["contract_hash"] = reusable_beo._hash_package(
            {k: v for k, v in forged_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "contract package request_hash mismatch|contract package contract_hash mismatch"):
            reusable_beo.build_exact_beo_publication_dry_run_249(
                forged_contract, reusable_beo.sample_beo_publication_candidate_inputs()
            )

        forged_pilot = reusable_beo._deepcopy(pilot)
        forged_pilot["contract_hash"] = "sha256:" + "1" * 64
        forged_pilot["pilot_hash"] = reusable_beo._hash_package(
            {k: v for k, v in forged_pilot.items() if k != "pilot_hash"}
        )
        with self.assertRaisesRegex(ValueError, "pilot package contract_hash mismatch|pilot package pilot_hash mismatch"):
            reusable_beo.integrate_beo_publication_review_250(forged_pilot)

        forged_integration = reusable_beo._deepcopy(integration)
        forged_integration["candidate_record_hash"] = "sha256:" + "2" * 64
        forged_integration["integration_hash"] = reusable_beo._hash_package(
            {k: v for k, v in forged_integration.items() if k != "integration_hash"}
        )
        with self.assertRaisesRegex(ValueError, "integration package candidate_record_hash mismatch|integration package integration_hash mismatch"):
            reusable_beo.reconcile_reusable_beo_publication_frontier_251(forged_integration)

    def test_hostile_review_rejects_oracle_fail_ready_state_and_completed_publication_claims(self):
        contract = reusable_beo.build_reusable_beo_publication_contract_248(
            reusable_beo.build_reusable_beo_publication_request_247(_oracle_reconciliation())
        )
        pilot = reusable_beo.build_exact_beo_publication_dry_run_249(
            contract, reusable_beo.sample_beo_publication_candidate_inputs()
        )
        forged = reusable_beo._deepcopy(pilot)
        forged["candidate_record"]["oracle_verdict"] = "FAIL"
        forged["candidate_record"]["publication_record_state"] = "READY_FOR_OPERATOR_REVIEW"
        forged["candidate_record_hash"] = reusable_beo._hash_package(forged["candidate_record"])
        forged["pilot_hash"] = reusable_beo._hash_package(
            {k: v for k, v in forged.items() if k != "pilot_hash"}
        )
        with self.assertRaisesRegex(ValueError, "oracle verdict and publication record state mismatch|pilot package pilot_hash mismatch|candidate_record_hash mismatch"):
            reusable_beo.integrate_beo_publication_review_250(forged)

        candidate = reusable_beo.sample_beo_publication_candidate_inputs()
        candidate["operator_notes"] = "BEO published; signer reused; storage written; ledger appended"
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            reusable_beo.build_exact_beo_publication_dry_run_249(contract, candidate)

    def test_builders_return_defensive_copies(self):
        request = reusable_beo.build_reusable_beo_publication_request_247(_oracle_reconciliation())
        contract = reusable_beo.build_reusable_beo_publication_contract_248(request)
        candidate = reusable_beo.sample_beo_publication_candidate_inputs()
        pilot = reusable_beo.build_exact_beo_publication_dry_run_249(contract, candidate)
        original_record_hash = pilot["candidate_record_hash"]

        candidate["operator_notes"] = "mutated after build"
        pilot["candidate_record"]["oracle_verdict"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "pilot_hash mismatch|candidate_record_hash mismatch"):
            reusable_beo.integrate_beo_publication_review_250(pilot)

        fresh = reusable_beo.build_exact_beo_publication_dry_run_249(
            contract, reusable_beo.sample_beo_publication_candidate_inputs()
        )
        self.assertEqual(fresh["candidate_record"]["oracle_verdict"], "PASS")
        self.assertEqual(fresh["candidate_record_hash"], original_record_hash)


if __name__ == "__main__":
    unittest.main()
