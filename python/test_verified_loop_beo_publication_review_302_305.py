import copy
from datetime import datetime
import unittest
from pathlib import Path
from unittest.mock import patch

from blk_authority_smuggling import scan_for_authority_laundering
from test_blk003_loop_oracle_verification_298_301 import _legacy_oracle_reconciliation, _record_300
from blk003_loop_oracle_verification_298_301 import reconcile_loop_oracle_verification_301
from reusable_beo_publication_ladder_247_251 import (
    build_exact_beo_publication_dry_run_249,
    build_reusable_beo_publication_contract_248,
    build_reusable_beo_publication_request_247,
    integrate_beo_publication_review_250,
    reconcile_reusable_beo_publication_frontier_251,
    sample_beo_publication_candidate_inputs,
)
from verified_loop_beo_publication_review_302_305 import (
    NEXT_FRONTIER_305,
    VerifiedLoopBeoPublicationReviewValidationError,
    build_verified_loop_beo_publication_review_contract_303,
    build_verified_loop_beo_publication_review_request_302,
    hash_package,
    record_verified_loop_beo_publication_review_304,
    reconcile_verified_loop_beo_publication_review_305,
    sample_verified_loop_beo_publication_review_report,
    validate_verified_loop_beo_publication_review_contract_303,
    validate_verified_loop_beo_publication_review_record_304,
    validate_verified_loop_beo_publication_review_reconciliation_305,
    validate_verified_loop_beo_publication_review_request_302,
)

ROOT = Path(__file__).resolve().parents[1]
BLK127 = ROOT / "docs" / "BLK-127_verified-loop-beo-publication-review-contract.md"

_REQUEST_ID = "BEO-REVIEW-REQUEST-BLK-SYSTEM-302-001"
_REQUESTED_AT = "2026-05-21T11:00:00+10:00"
_EXPIRES_AT = "2026-05-21T11:45:00+10:00"
_REVIEWED_AT = "2026-05-21T11:30:00+10:00"
_VALIDATION_NOW = "2026-05-21T10:15:00+10:00"


def _verification_reconciliation_301():
    context = _record_300()
    (
        upstream,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        package,
        preflight,
        record,
        reconciliation,
        oracle_reconciliation,
        verification_contract,
        verification_preflight,
        verification_record,
    ) = context
    final = reconcile_loop_oracle_verification_301(
        verification_contract,
        verification_preflight,
        verification_record,
        package,
        preflight,
        record,
        reconciliation,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
        oracle_reconciliation,
    )
    return final


def _reusable_beo_reconciliation_251():
    oracle = _legacy_oracle_reconciliation()
    request = build_reusable_beo_publication_request_247(oracle)
    contract = build_reusable_beo_publication_contract_248(request)
    dry_run = build_exact_beo_publication_dry_run_249(contract, sample_beo_publication_candidate_inputs())
    integration = integrate_beo_publication_review_250(dry_run)
    return reconcile_reusable_beo_publication_frontier_251(integration)


def _request_302():
    verification = _verification_reconciliation_301()
    beo = _reusable_beo_reconciliation_251()
    request = build_verified_loop_beo_publication_review_request_302(
        verification,
        beo,
        request_id=_REQUEST_ID,
        requested_at=_REQUESTED_AT,
        expires_at=_EXPIRES_AT,
    )
    return verification, beo, request


def _contract_303():
    verification, beo, request = _request_302()
    contract = build_verified_loop_beo_publication_review_contract_303(request, verification, beo)
    return verification, beo, request, contract


def _record_304():
    verification, beo, request, contract = _contract_303()
    report = sample_verified_loop_beo_publication_review_report(
        contract,
        verification,
        beo,
        reviewed_at=_REVIEWED_AT,
    )
    record = record_verified_loop_beo_publication_review_304(
        contract,
        request,
        verification,
        beo,
        review_report=report,
    )
    return verification, beo, request, contract, record


class VerifiedLoopBeoPublicationReview302To305Test(unittest.TestCase):
    def setUp(self):
        self._now_patch = patch(
            "verified_loop_beo_publication_review_302_305._validation_now",
            return_value=datetime.fromisoformat(_VALIDATION_NOW),
        )
        self._now_patch.start()
        self.addCleanup(self._now_patch.stop)

    def test_302_to_305_review_package_is_ready_for_exact_approval_request_only(self):
        verification, beo, request, contract, record = _record_304()
        final = reconcile_verified_loop_beo_publication_review_305(
            contract,
            request,
            record,
            verification,
            beo,
        )

        self.assertEqual(request["status"], "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY_NOT_GRANTED")
        self.assertIn("BLK_SYSTEM_302_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY", request["markers"])
        self.assertEqual(request["verification_reconciliation_hash"], verification["reconciliation_hash"])
        self.assertEqual(request["reusable_beo_reconciliation_hash"], beo["reconciliation_hash"])
        self.assertFalse(request["side_effects"]["beo_publication"])
        self.assertFalse(request["side_effects"]["beo_closeout_execution"])
        self.assertFalse(request["side_effects"]["run_id_reserved"])

        self.assertEqual(contract["status"], "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY")
        self.assertIn("BLK_SYSTEM_303_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY", contract["markers"])
        self.assertTrue(contract["review_rules"]["verified_loop_evidence_required"])
        self.assertTrue(contract["review_rules"]["exact_operator_approval_still_required"])
        self.assertFalse(contract["review_rules"]["publication_allowed_by_review"])
        self.assertFalse(contract["side_effects"]["signer_reuse"])
        self.assertFalse(contract["side_effects"]["immutable_storage_written"])

        self.assertEqual(record["status"], "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED")
        self.assertIn("BLK_SYSTEM_304_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED", record["markers"])
        self.assertEqual(record["review_result"], "READY_FOR_EXACT_APPROVAL_REQUEST")
        self.assertFalse(record["approval_captured"])
        self.assertFalse(record["publication_executed"])
        self.assertEqual(record["verified_hashes"]["verified_loop_reconciliation_hash"], verification["reconciliation_hash"])
        self.assertEqual(record["verified_hashes"]["reusable_beo_reconciliation_hash"], beo["reconciliation_hash"])

        self.assertEqual(final["status"], "VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED")
        self.assertIn("BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED", final["markers"])
        self.assertEqual(final["next_frontier"], NEXT_FRONTIER_305)
        self.assertEqual(final["reconciled_state"], "verified_loop_beo_publication_review_ready_for_exact_approval_request_not_granted")
        self.assertFalse(final["side_effects"]["beo_publication"])
        self.assertFalse(final["side_effects"]["rtm_generation"])
        self.assertFalse(final["side_effects"]["target_source_git_mutation"])
        self.assertRegex(final["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

        self.assertEqual(
            validate_verified_loop_beo_publication_review_reconciliation_305(
                final,
                contract,
                request,
                record,
                verification,
                beo,
            ),
            final,
        )

    def test_302_request_pins_canonical_301_and_251_hashes_not_self_consistent_rehashes(self):
        verification = _verification_reconciliation_301()
        beo = _reusable_beo_reconciliation_251()
        request = build_verified_loop_beo_publication_review_request_302(
            verification,
            beo,
            request_id=_REQUEST_ID,
            requested_at=_REQUESTED_AT,
            expires_at=_EXPIRES_AT,
        )
        self.assertEqual(
            validate_verified_loop_beo_publication_review_request_302(request, verification, beo),
            request,
        )

        forged_verification = copy.deepcopy(verification)
        forged_verification["blk_test_passed"] = False
        forged_verification["reconciliation_hash"] = hash_package(
            {key: value for key, value in forged_verification.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "BLK-SYSTEM-301|canonical"):
            build_verified_loop_beo_publication_review_request_302(
                forged_verification,
                beo,
                request_id="BEO-REVIEW-REQUEST-BLK-SYSTEM-302-FORGED",
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

        forged_beo = copy.deepcopy(beo)
        forged_beo["side_effects"]["beo_published"] = True
        forged_beo["reconciliation_hash"] = hash_package(
            {key: value for key, value in forged_beo.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "BLK-SYSTEM-251|side_effect"):
            validate_verified_loop_beo_publication_review_request_302(request, verification, forged_beo)

    def test_302_request_rejects_stale_windows_and_authority_laundering_ids(self):
        verification = _verification_reconciliation_301()
        beo = _reusable_beo_reconciliation_251()
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "expired/stale"):
            build_verified_loop_beo_publication_review_request_302(
                verification,
                beo,
                request_id="BEO-REVIEW-REQUEST-BLK-SYSTEM-302-STALE",
                requested_at="2020-01-01T00:00:00+00:00",
                expires_at="2020-01-01T01:00:00+00:00",
            )
        for request_id in [
            "BEO-REVIEW-REQUEST-BLK-SYSTEM-302-AUTHORIZED",
            "BEO-REVIEW-REQUEST-BLK-SYSTEM-302-APPROVED",
            "BEO-REVIEW-REQUEST-BLK-SYSTEM-302-RESERVED",
        ]:
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "forbidden authority segment"):
                build_verified_loop_beo_publication_review_request_302(
                    verification,
                    beo,
                    request_id=request_id,
                    requested_at=_REQUESTED_AT,
                    expires_at=_EXPIRES_AT,
                )

    def test_303_contract_closes_rules_denied_authorities_and_nested_policy_shape(self):
        verification, beo, request, contract = _contract_303()
        self.assertEqual(
            validate_verified_loop_beo_publication_review_contract_303(contract, request, verification, beo),
            contract,
        )

        tampered_rules = copy.deepcopy(contract)
        tampered_rules["review_rules"]["publication_allowed_by_review"] = True
        tampered_rules["contract_hash"] = hash_package(
            {key: value for key, value in tampered_rules.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "review_rules"):
            validate_verified_loop_beo_publication_review_contract_303(tampered_rules, request, verification, beo)

        duplicate_denial = copy.deepcopy(contract)
        duplicate_denial["denied_authorities"].append(duplicate_denial["denied_authorities"][0])
        duplicate_denial["contract_hash"] = hash_package(
            {key: value for key, value in duplicate_denial.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "denied_authorities"):
            validate_verified_loop_beo_publication_review_contract_303(duplicate_denial, request, verification, beo)

        nested_smuggle = copy.deepcopy(contract)
        nested_smuggle["publication_policies"]["signer_policy"]["notes"] = "signer reused and BEO publication greenlit"
        nested_smuggle["contract_hash"] = hash_package(
            {key: value for key, value in nested_smuggle.items() if key != "contract_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "publication_policies|forbidden authority wording|unsupported"):
            validate_verified_loop_beo_publication_review_contract_303(nested_smuggle, request, verification, beo)

    def test_304_record_binds_review_report_and_rejects_approval_or_missing_false_fields(self):
        verification, beo, request, contract = _contract_303()
        report = sample_verified_loop_beo_publication_review_report(
            contract,
            verification,
            beo,
            reviewed_at=_REVIEWED_AT,
        )

        bad_hash = copy.deepcopy(report)
        bad_hash["verified_hashes"]["verified_loop_reconciliation_hash"] = "sha256:" + "a" * 64
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "verified hash"):
            record_verified_loop_beo_publication_review_304(
                contract,
                request,
                verification,
                beo,
                review_report=bad_hash,
            )

        approval_smuggle = copy.deepcopy(report)
        approval_smuggle["review_notes"] = "BLK-test PASS approves BEO publication; signer reused; ledger appended"
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "forbidden authority wording|PASS"):
            record_verified_loop_beo_publication_review_304(
                contract,
                request,
                verification,
                beo,
                review_report=approval_smuggle,
            )

        for note in [
            "review grants BEO publication",
            "review grants publication authority",
            "review authorizes publication",
            "review grants BEO closeout execution",
            "review grants signer storage ledger reuse",
            "review grants RTM generation",
            "review grants production blk-link",
            "review grants protected-body access",
            "review grants target/source/Git mutation",
        ]:
            authority_smuggle = copy.deepcopy(report)
            authority_smuggle["review_notes"] = note
            with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "forbidden authority wording|PASS"):
                record_verified_loop_beo_publication_review_304(
                    contract,
                    request,
                    verification,
                    beo,
                    review_report=authority_smuggle,
                )

        blocked_report = copy.deepcopy(report)
        blocked_report["review_result"] = "BLOCKED_BY_REVIEW_GAP"
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "READY_FOR_EXACT_APPROVAL_REQUEST"):
            record_verified_loop_beo_publication_review_304(
                contract,
                request,
                verification,
                beo,
                review_report=blocked_report,
            )

        bad_review_id = copy.deepcopy(report)
        bad_review_id["review_id"] = "BEO-PUBLICATION-REVIEW-BLK-SYSTEM-304-APPROVED"
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "forbidden authority segment"):
            record_verified_loop_beo_publication_review_304(
                contract,
                request,
                verification,
                beo,
                review_report=bad_review_id,
            )

        missing_false = copy.deepcopy(report)
        del missing_false["denied_side_effects"]["run_id_reserved"]
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "denied_side_effects"):
            record_verified_loop_beo_publication_review_304(
                contract,
                request,
                verification,
                beo,
                review_report=missing_false,
            )

    def test_305_reconciliation_revalidates_record_schema_and_blocks_rehashed_side_effect_drift(self):
        verification, beo, request, contract, record = _record_304()

        side_effect_drift = copy.deepcopy(record)
        side_effect_drift["side_effects"]["beo_publication"] = True
        side_effect_drift["review_record_hash"] = hash_package(
            {key: value for key, value in side_effect_drift.items() if key != "review_record_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "side_effects"):
            reconcile_verified_loop_beo_publication_review_305(
                contract,
                request,
                side_effect_drift,
                verification,
                beo,
            )

        marker_smuggle = copy.deepcopy(record)
        marker_smuggle["markers"].append("BEO_PUBLICATION_AUTHORIZED")
        marker_smuggle["review_record_hash"] = hash_package(
            {key: value for key, value in marker_smuggle.items() if key != "review_record_hash"}
        )
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "markers|forbidden authority wording"):
            validate_verified_loop_beo_publication_review_record_304(
                marker_smuggle,
                contract,
                request,
                verification,
                beo,
            )

    def test_builders_return_defensive_copies(self):
        verification, beo, request, contract, record = _record_304()
        original_hash = record["review_record_hash"]
        record["verified_hashes"]["verified_loop_reconciliation_hash"] = "sha256:" + "b" * 64
        with self.assertRaisesRegex(VerifiedLoopBeoPublicationReviewValidationError, "hash mismatch|verified hash"):
            validate_verified_loop_beo_publication_review_record_304(record, contract, request, verification, beo)
        fresh = _record_304()[-1]
        self.assertEqual(fresh["review_record_hash"], original_hash)

    def test_blk127_doc_makes_review_boundary_and_next_frontier_review_obvious(self):
        verification, beo, request, contract, record = _record_304()
        final = reconcile_verified_loop_beo_publication_review_305(
            contract,
            request,
            record,
            verification,
            beo,
        )
        doc = BLK127.read_text()
        required = [
            "BLK_SYSTEM_302_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_REQUEST_READY",
            "BLK_SYSTEM_303_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_CONTRACT_READY",
            "BLK_SYSTEM_304_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECORDED",
            "BLK_SYSTEM_305_VERIFIED_LOOP_BEO_PUBLICATION_REVIEW_RECONCILED",
            request["review_request_hash"],
            contract["contract_hash"],
            record["review_record_hash"],
            final["reconciliation_hash"],
            NEXT_FRONTIER_305,
            "PASS is evidence, not approval",
            "no BEO closeout execution",
            "no BEO publication",
            "no signer reuse",
            "no storage reuse",
            "no ledger reuse",
            "no RTM generation",
            "no production `blk-link`",
            "no protected-body access",
            "no target/source/Git mutation",
        ]
        missing = [marker for marker in required if marker not in doc]
        self.assertEqual(missing, [])
        self.assertEqual(scan_for_authority_laundering(doc, path="BLK-127"), [])


if __name__ == "__main__":
    unittest.main()
