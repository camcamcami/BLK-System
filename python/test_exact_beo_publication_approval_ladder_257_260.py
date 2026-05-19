import unittest

from test_rtm_blk_link_drift_coverage_ladder_252_256 import (
    _beo_reconciliation,
    _blk_link_reconciliation,
)
import rtm_blk_link_drift_coverage_ladder_252_256 as drift_coverage

import exact_beo_publication_approval_ladder_257_260 as exact_beo


_OPERATOR_GENERIC_DIRECTIVE = "plan and execute the next 3-5 blk-system sprints"


def _drift_reconciliation():
    review = drift_coverage.build_rtm_blk_link_drift_coverage_surface_review_252(
        _beo_reconciliation(), _blk_link_reconciliation()
    )
    request = drift_coverage.build_rtm_blk_link_drift_coverage_request_253(review)
    contract = drift_coverage.build_drift_coverage_verifier_contract_254(request)
    dry_run = drift_coverage.build_exact_metadata_only_drift_coverage_dry_run_255(
        contract, drift_coverage.sample_drift_coverage_metadata_inputs()
    )
    return drift_coverage.reconcile_drift_coverage_frontier_256(dry_run)


class ExactBeoPublicationApprovalLadder257To260Test(unittest.TestCase):
    def test_257_to_260_chain_scopes_exact_publication_but_blocks_generic_directive(self):
        beo = _beo_reconciliation()
        drift = _drift_reconciliation()

        request = exact_beo.build_exact_beo_publication_run_request_257(beo, drift)
        contract = exact_beo.build_exact_beo_publication_operator_approval_contract_258(request)
        preflight = exact_beo.evaluate_exact_beo_publication_operator_approval_259(
            contract, _OPERATOR_GENERIC_DIRECTIVE
        )
        reconciliation = exact_beo.reconcile_exact_beo_publication_approval_frontier_260(preflight)

        self.assertEqual(request["status"], "EXACT_BEO_PUBLICATION_RUN_REQUEST_READY_NOT_APPROVED")
        self.assertEqual(request["beo_reconciliation_hash"], beo["reconciliation_hash"])
        self.assertEqual(request["drift_coverage_reconciliation_hash"], drift["reconciliation_hash"])
        self.assertFalse(request["side_effects"]["authoritative_beo_publication_finalized"])
        self.assertIn("BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY", request["markers"])

        self.assertEqual(contract["status"], "EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY")
        self.assertEqual(contract["request_hash"], request["request_hash"])
        self.assertEqual(contract["exact_operator_approval_text"], exact_beo.EXACT_OPERATOR_APPROVAL_TEXT_258)
        self.assertTrue(contract["approval_rules"]["exact_text_required"])
        self.assertFalse(contract["side_effects"]["operator_approval_captured"])

        self.assertEqual(preflight["status"], "BLOCKED_BY_MISSING_EXACT_OPERATOR_APPROVAL")
        self.assertEqual(preflight["contract_hash"], contract["contract_hash"])
        self.assertEqual(preflight["operator_text_status"], "NOT_EXACT_APPROVAL_TEXT")
        self.assertFalse(preflight["side_effects"]["run_id_consumed"])
        self.assertFalse(preflight["side_effects"]["signer_storage_ledger_reuse"])
        self.assertFalse(preflight["side_effects"]["authoritative_beo_publication_finalized"])

        self.assertEqual(reconciliation["status"], "EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED")
        self.assertEqual(reconciliation["preflight_hash"], preflight["preflight_hash"])
        self.assertEqual(
            reconciliation["next_frontier"],
            "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED",
        )
        self.assertIn("BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED", reconciliation["markers"])

    def test_rejects_rehashed_extra_authority_fields_at_every_downstream_boundary(self):
        request = exact_beo.build_exact_beo_publication_run_request_257(
            _beo_reconciliation(), _drift_reconciliation()
        )
        tampered_request = exact_beo._deepcopy(request)
        tampered_request["request_scope"] = "generic operator directive is publication approval"
        tampered_request["request_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_request.items() if k != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-257|forbidden authority"):
            exact_beo.build_exact_beo_publication_operator_approval_contract_258(tampered_request)

        tampered_request = exact_beo._deepcopy(request)
        tampered_request["beo_published"] = True
        tampered_request["request_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_request.items() if k != "request_hash"}
        )
        with self.assertRaisesRegex(ValueError, "unsupported field|forbidden authority|request package"):
            exact_beo.build_exact_beo_publication_operator_approval_contract_258(tampered_request)

        contract = exact_beo.build_exact_beo_publication_operator_approval_contract_258(request)
        tampered_contract = exact_beo._deepcopy(contract)
        tampered_contract["request_hash"] = "sha256:" + "1" * 64
        tampered_contract["contract_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "canonical BLK-SYSTEM-257|canonical BLK-SYSTEM-258"):
            exact_beo.evaluate_exact_beo_publication_operator_approval_259(
                tampered_contract, _OPERATOR_GENERIC_DIRECTIVE
            )

        tampered_contract = exact_beo._deepcopy(contract)
        tampered_contract["approval_rules"]["approval_inherited"] = True
        tampered_contract["contract_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_contract.items() if k != "contract_hash"}
        )
        with self.assertRaisesRegex(ValueError, "approval_rules|forbidden authority|contract package"):
            exact_beo.evaluate_exact_beo_publication_operator_approval_259(
                tampered_contract, _OPERATOR_GENERIC_DIRECTIVE
            )

        preflight = exact_beo.evaluate_exact_beo_publication_operator_approval_259(
            contract, _OPERATOR_GENERIC_DIRECTIVE
        )
        tampered_preflight = exact_beo._deepcopy(preflight)
        tampered_preflight["status"] = "EXACT_OPERATOR_APPROVAL_TEXT_MATCHED_NOT_CAPTURED"
        tampered_preflight["operator_text_status"] = "EXACT_TEXT_MATCHED_BUT_CAPTURE_NOT_PERFORMED"
        tampered_preflight["operator_text_hash"] = exact_beo._hash_text(_OPERATOR_GENERIC_DIRECTIVE)
        tampered_preflight["evaluation_result"] = "generic sprint directive matched exact text"
        tampered_preflight["preflight_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_preflight.items() if k != "preflight_hash"}
        )
        with self.assertRaisesRegex(ValueError, "correlation|canonical BLK-SYSTEM-259|forbidden authority"):
            exact_beo.reconcile_exact_beo_publication_approval_frontier_260(tampered_preflight)

        tampered_preflight = exact_beo._deepcopy(preflight)
        tampered_preflight["side_effects"]["operator_approval_captured"] = True
        tampered_preflight["preflight_hash"] = exact_beo._hash_package(
            {k: v for k, v in tampered_preflight.items() if k != "preflight_hash"}
        )
        with self.assertRaisesRegex(ValueError, "side_effects|preflight package"):
            exact_beo.reconcile_exact_beo_publication_approval_frontier_260(tampered_preflight)

    def test_rejects_claimed_hash_upstream_and_publication_laundering(self):
        beo = _beo_reconciliation()
        drift = _drift_reconciliation()

        forged_beo = exact_beo._deepcopy(beo)
        forged_beo["side_effects"]["beo_published"] = True
        forged_beo["reconciliation_hash"] = beo["reconciliation_hash"]
        with self.assertRaisesRegex(ValueError, "upstream|side_effects|forbidden authority"):
            exact_beo.build_exact_beo_publication_run_request_257(forged_beo, drift)

        forged_drift = exact_beo._deepcopy(drift)
        forged_drift["next_frontier"] = "BEO_PUBLICATION_AUTHORIZED"
        forged_drift["reconciliation_hash"] = drift["reconciliation_hash"]
        with self.assertRaisesRegex(ValueError, "upstream|forbidden authority|next_frontier"):
            exact_beo.build_exact_beo_publication_run_request_257(beo, forged_drift)

        request = exact_beo.build_exact_beo_publication_run_request_257(beo, drift)
        contract = exact_beo.build_exact_beo_publication_operator_approval_contract_258(request)
        with self.assertRaisesRegex(ValueError, "forbidden authority wording"):
            exact_beo.evaluate_exact_beo_publication_operator_approval_259(
                contract, "BEO published; signer reused; ledger appended"
            )


if __name__ == "__main__":
    unittest.main()
