import unittest

import production_blk_test_mcp_oracle_ladder_242_246 as oracle
import blk_root_doctrine_gap_ladder_237_241 as root_gap
import reusable_beo_publication_ladder_247_251 as reusable_beo
from blk_req_production_gateway_195_199 import (
    build_blk_req_gateway_readiness_review_195,
    build_blk_req_production_gateway_contract_196,
)
from repeatable_trusted_blk_link_190_194 import (
    build_repeatable_trusted_blk_link_contract_191,
    build_repeatable_trusted_blk_link_ledger_192,
    build_repeatable_trusted_blk_link_post_run_review_190,
    build_repeatable_trusted_blk_link_reconciliation_194,
    build_repeatable_trusted_blk_link_repeat_runs_193,
    valid_repeatable_trusted_blk_link_contract_191,
    valid_repeatable_trusted_blk_link_ledger_192,
    valid_repeatable_trusted_blk_link_post_run_review_190,
    valid_repeatable_trusted_blk_link_reconciliation_194,
    valid_repeatable_trusted_blk_link_repeat_runs_193,
)
from test_repeatable_trusted_blk_link_190_194 import valid_189_reconciliation_package

import rtm_blk_link_drift_coverage_ladder_252_256 as rtm_dc


def _loop_kernel():
    selected = root_gap.build_kuronode_route_selection_237()
    overlay = root_gap.build_root_doctrine_deviation_overlay_238(selected)
    scope = root_gap.decide_blk_id_relay_scope_239(overlay)
    gateway_contract = build_blk_req_production_gateway_contract_196(
        build_blk_req_gateway_readiness_review_195()
    )
    gateway = root_gap.build_hitl_gateway_completion_slice_240(scope, gateway_contract)
    return root_gap.build_reusable_blk003_loop_kernel_241(gateway)


def _beo_reconciliation():
    request = oracle.build_oracle_request_242(_loop_kernel())
    contract = oracle.build_oracle_contract_243(request)
    fixture = oracle.build_metadata_only_oracle_fixture_244(
        contract, oracle.sample_oracle_evidence_inputs()
    )
    integration = oracle.integrate_oracle_record_245(fixture)
    oracle_reconciliation = oracle.reconcile_oracle_frontier_246(integration)
    beo_request = reusable_beo.build_reusable_beo_publication_request_247(oracle_reconciliation)
    beo_contract = reusable_beo.build_reusable_beo_publication_contract_248(beo_request)
    beo_pilot = reusable_beo.build_exact_beo_publication_dry_run_249(
        beo_contract, reusable_beo.sample_beo_publication_candidate_inputs()
    )
    beo_integration = reusable_beo.integrate_beo_publication_review_250(beo_pilot)
    return reusable_beo.reconcile_reusable_beo_publication_frontier_251(beo_integration)


def _blk_link_reconciliation():
    reconciliation189 = valid_189_reconciliation_package()
    review190 = valid_repeatable_trusted_blk_link_post_run_review_190(reconciliation189)
    review = build_repeatable_trusted_blk_link_post_run_review_190(reconciliation189, review190)
    contract191 = valid_repeatable_trusted_blk_link_contract_191(review)
    contract = build_repeatable_trusted_blk_link_contract_191(review, contract191)
    ledger192 = valid_repeatable_trusted_blk_link_ledger_192(contract)
    ledger = build_repeatable_trusted_blk_link_ledger_192(contract, ledger192)
    repeat193 = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger)
    runs = build_repeatable_trusted_blk_link_repeat_runs_193(ledger, repeat193)
    context194 = valid_repeatable_trusted_blk_link_reconciliation_194(runs)
    return build_repeatable_trusted_blk_link_reconciliation_194(runs, context194)


class RtmBlkLinkDriftCoverageLadder252To256Test(unittest.TestCase):
    def test_252_to_256_chain_requests_metadata_only_drift_coverage_without_truth_claim(self):
        beo_final = _beo_reconciliation()
        blk_link_final = _blk_link_reconciliation()

        review = rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(
            beo_final, blk_link_final
        )
        request = rtm_dc.build_rtm_blk_link_drift_coverage_request_253(review)
        contract = rtm_dc.build_drift_coverage_verifier_contract_254(request)
        dry_run = rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(
            contract, rtm_dc.sample_drift_coverage_metadata_inputs()
        )
        reconciliation = rtm_dc.reconcile_drift_coverage_frontier_256(dry_run)

        self.assertEqual(review["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_COMPLETE_NOT_AUTHORITY")
        self.assertEqual(review["beo_reconciliation_hash"], beo_final["reconciliation_hash"])
        self.assertEqual(review["blk_link_reconciliation_hash"], blk_link_final["reconciliation_package_hash"])
        self.assertIn("BLK_SYSTEM_252_RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_READY", review["markers"])
        self.assertFalse(review["side_effects"]["rtm_generation"])
        self.assertFalse(review["side_effects"]["coverage_truth"])

        self.assertEqual(request["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED_NOT_GRANTED")
        self.assertEqual(request["surface_review_hash"], review["surface_review_hash"])
        self.assertTrue(request["request_rules"]["authoritative_beo_publication_required_before_truth"])
        self.assertFalse(request["side_effects"]["approval_captured"])

        self.assertEqual(contract["status"], "DRIFT_COVERAGE_VERIFIER_CONTRACT_READY_PER_RUN_EXACT_APPROVAL")
        self.assertEqual(contract["request_hash"], request["request_hash"])
        self.assertTrue(contract["contract_rules"]["metadata_only_inputs_required"])
        self.assertTrue(contract["contract_rules"]["protected_body_content_forbidden"])
        self.assertFalse(contract["side_effects"]["production_blk_link_execution"])

        self.assertEqual(dry_run["status"], "EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_BLOCKED_BY_UNPUBLISHED_BEO")
        self.assertEqual(dry_run["contract_hash"], contract["contract_hash"])
        self.assertEqual(dry_run["verifier_record"]["record_state"], "BLOCKED_BY_MISSING_AUTHORITATIVE_BEO_METADATA")
        self.assertFalse(dry_run["verifier_record"]["record_only_policy"]["drift_truth_established"])
        self.assertFalse(dry_run["side_effects"]["coverage_truth"])

        self.assertEqual(reconciliation["status"], "RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED_BEO_PUBLICATION_REQUIRED")
        self.assertEqual(reconciliation["dry_run_hash"], dry_run["dry_run_hash"])
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED",
        )
        self.assertIn("BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED", reconciliation["markers"])
        self.assertRegex(reconciliation["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_upstream_packages_reject_claimed_hash_laundering(self):
        beo = _beo_reconciliation()
        blk_link = _blk_link_reconciliation()

        forged_beo = rtm_dc._deepcopy(beo)
        forged_beo["side_effects"]["beo_published"] = True
        forged_beo["reconciliation_hash"] = beo["reconciliation_hash"]
        with self.assertRaisesRegex(ValueError, "upstream validation failed|side_effects|forbidden authority"):
            rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(forged_beo, blk_link)

        forged_blk_link = rtm_dc._deepcopy(blk_link)
        forged_blk_link["beb_dispatch_authorized"] = True
        forged_blk_link["beo_publication_or_signing_authorized"] = True
        forged_blk_link["protected_body_text_included"] = True
        forged_blk_link["coverage_claim_promoted"] = True
        forged_blk_link["reconciliation_package_hash"] = blk_link["reconciliation_package_hash"]
        with self.assertRaisesRegex(ValueError, "upstream validation failed|must be False|forbidden authority"):
            rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(beo, forged_blk_link)

    def test_downstream_builders_reject_rehashed_extra_authority_fields(self):
        review = rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(
            _beo_reconciliation(), _blk_link_reconciliation()
        )
        tampered_review = rtm_dc._deepcopy(review)
        tampered_review["rtm_generation_authorized"] = True
        tampered_review["surface_review_hash"] = rtm_dc._hash_package(
            {k: v for k, v in tampered_review.items() if k != "surface_review_hash"}
        )
        with self.assertRaisesRegex(ValueError, "surface review|unsupported field|rtm_generation"):
            rtm_dc.build_rtm_blk_link_drift_coverage_request_253(tampered_review)

        request = rtm_dc.build_rtm_blk_link_drift_coverage_request_253(review)
        tampered_request = rtm_dc._deepcopy(request)
        tampered_request["request_rules"]["truth_from_reusable_beo_review_allowed"] = True
        tampered_request["request_hash"] = rtm_dc._hash_package(
            {k: v for k, v in tampered_request.items() if k != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "request package|request_rules|forbidden authority wording"):
            rtm_dc.build_drift_coverage_verifier_contract_254(tampered_request)

        contract = rtm_dc.build_drift_coverage_verifier_contract_254(request)
        tampered_contract = rtm_dc._deepcopy(contract)
        tampered_contract["contract_rules"]["protected_body_content_allowed"] = True
        tampered_contract["contract_hash"] = rtm_dc._hash_package(
            {k: v for k, v in tampered_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "contract package|contract_rules|forbidden authority wording"):
            rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(
                tampered_contract, rtm_dc.sample_drift_coverage_metadata_inputs()
            )

        dry_run = rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(
            contract, rtm_dc.sample_drift_coverage_metadata_inputs()
        )
        tampered_dry_run = rtm_dc._deepcopy(dry_run)
        tampered_dry_run["status"] = "EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_READY_FOR_OPERATOR_REVIEW"
        tampered_dry_run["verifier_record"]["record_state"] = "READY_FOR_OPERATOR_REVIEW_AFTER_EXACT_APPROVAL"
        tampered_dry_run["verifier_record"]["beo_publication_state"] = "AUTHORITATIVE_BEO_PUBLICATION_METADATA_PRESENT"
        tampered_dry_run["verifier_record_hash"] = rtm_dc._hash_package(tampered_dry_run["verifier_record"])
        tampered_dry_run["dry_run_hash"] = rtm_dc._hash_package(
            {k: v for k, v in tampered_dry_run.items() if k != "dry_run_hash"}
        )
        with self.assertRaisesRegex(ValueError, "dry-run package status mismatch|record_state|beo_publication_state"):
            rtm_dc.reconcile_drift_coverage_frontier_256(tampered_dry_run)

        tampered_dry_run = rtm_dc._deepcopy(dry_run)
        tampered_dry_run["verifier_record"]["nested"] = {"coverageTruth": "granted"}
        tampered_dry_run["verifier_record_hash"] = rtm_dc._hash_package(tampered_dry_run["verifier_record"])
        tampered_dry_run["dry_run_hash"] = rtm_dc._hash_package(
            {k: v for k, v in tampered_dry_run.items() if k != "dry_run_hash"}
        )
        with self.assertRaisesRegex(ValueError, "dry-run package|verifier record|forbidden authority wording|unsupported field"):
            rtm_dc.reconcile_drift_coverage_frontier_256(tampered_dry_run)

    def test_metadata_inputs_reject_protected_body_and_truth_laundering(self):
        review = rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(
            _beo_reconciliation(), _blk_link_reconciliation()
        )
        request = rtm_dc.build_rtm_blk_link_drift_coverage_request_253(review)
        contract = rtm_dc.build_drift_coverage_verifier_contract_254(request)

        bad = rtm_dc.sample_drift_coverage_metadata_inputs()
        bad["operator_notes"] = "coverage truth established; driftRejected; productionBlkLinkAuthorized"
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(contract, bad)

        bad = rtm_dc.sample_drift_coverage_metadata_inputs()
        bad["blk_req_metadata_ref"] = "docs%252Frequirements%252Factive%252FREQ-001.md"
        with self.assertRaisesRegex(ValueError, "protected path|forbidden authority wording"):
            rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(contract, bad)

        bad = rtm_dc.sample_drift_coverage_metadata_inputs()
        bad["beo_publication_state"] = "AUTHORITATIVE_BEO_PUBLICATION_METADATA_PRESENT"
        with self.assertRaisesRegex(ValueError, "cannot be self-attested"):
            rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(contract, bad)

        bad = rtm_dc.sample_drift_coverage_metadata_inputs()
        bad["coverage_probe_metadata_hash"] = "sha256:nothex"
        with self.assertRaisesRegex(ValueError, "coverage_probe_metadata_hash must be canonical sha256"):
            rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(contract, bad)

    def test_contract_requires_exact_denials_and_false_side_effects(self):
        review = rtm_dc.build_rtm_blk_link_drift_coverage_surface_review_252(
            _beo_reconciliation(), _blk_link_reconciliation()
        )
        request = rtm_dc.build_rtm_blk_link_drift_coverage_request_253(review)
        contract = rtm_dc.build_drift_coverage_verifier_contract_254(request)

        for mutation in ["remove_denial", "duplicate_denial", "extra_denial", "missing_false_flag"]:
            tampered = rtm_dc._deepcopy(contract)
            if mutation == "remove_denial":
                tampered["denied_authorities"] = tampered["denied_authorities"][:-1]
            elif mutation == "duplicate_denial":
                tampered["denied_authorities"].append(tampered["denied_authorities"][0])
            elif mutation == "extra_denial":
                tampered["denied_authorities"].append("APPROVED_FOR_COVERAGE_TRUTH")
            else:
                del tampered["record_only_policy"]["protected_body_accessed"]
            tampered["contract_hash"] = rtm_dc._hash_package(
                {k: v for k, v in tampered.items() if k != "contract_hash"}
            )
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(ValueError, "contract_hash mismatch|denied_authorities|record_only_policy|forbidden authority wording"):
                    rtm_dc.build_exact_metadata_only_drift_coverage_dry_run_255(
                        tampered, rtm_dc.sample_drift_coverage_metadata_inputs()
                    )


if __name__ == "__main__":
    unittest.main()
