import copy
import unittest
from pathlib import Path

from blk_authority_smuggling import scan_for_authority_laundering
from test_blk003_quarantine_gated_loop_execution_294_297 import _execution_record_296
import production_blk_test_mcp_oracle_ladder_242_246 as legacy_oracle
from test_production_blk_test_mcp_oracle_ladder_242_246 import _loop_kernel
from blk003_loop_oracle_verification_298_301 import (
    Blk003LoopOracleVerificationValidationError,
    NEXT_FRONTIER_301,
    build_loop_oracle_verification_contract_298,
    build_loop_oracle_verification_preflight_299,
    record_loop_oracle_verification_300,
    reconcile_loop_oracle_verification_301,
    sample_loop_oracle_verification_report,
    validate_loop_oracle_verification_contract_298,
    validate_loop_oracle_verification_preflight_299,
    validate_loop_oracle_verification_record_300,
    validate_loop_oracle_verification_reconciliation_301,
    hash_package,
)

ROOT = Path(__file__).resolve().parents[1]
BLK126 = ROOT / "docs" / "BLK-126_exact-blk-test-oracle-verification-after-loop-contract.md"

_REQUESTED_AT = "2026-05-21T10:21:00+10:00"
_EXPIRES_AT = "2026-05-21T10:50:00+10:00"
_PREFLIGHT_AT = "2026-05-21T10:25:00+10:00"
_VERIFIED_AT = "2026-05-21T10:30:00+10:00"
_CONTRACT_ID = "BLK-TEST-ORACLE-CONTRACT-BLK-SYSTEM-298-001"


def _legacy_oracle_reconciliation():
    request = legacy_oracle.build_oracle_request_242(_loop_kernel())
    contract = legacy_oracle.build_oracle_contract_243(request)
    fixture = legacy_oracle.build_metadata_only_oracle_fixture_244(
        contract,
        legacy_oracle.sample_oracle_evidence_inputs(),
    )
    integration = legacy_oracle.integrate_oracle_record_245(fixture)
    return legacy_oracle.reconcile_oracle_frontier_246(integration)


def _loop_context():
    upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record = _execution_record_296()
    reconciliation = reconcile_loop_execution_for_test(
        package,
        preflight,
        record,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream,
    )
    return upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record, reconciliation


def reconcile_loop_execution_for_test(
    package,
    preflight,
    record,
    contract,
    binding,
    request_preflight,
    request_reconciliation,
    upstream,
):
    from blk003_quarantine_gated_loop_execution_294_297 import reconcile_exact_loop_execution_package_297

    return reconcile_exact_loop_execution_package_297(
        package,
        preflight,
        record,
        contract,
        binding,
        request_preflight,
        request_reconciliation,
        upstream["approval_contract"],
        upstream["quarantine"],
        upstream["interaction"],
        upstream["gate"],
    )


def _contract_298():
    context = _loop_context()
    oracle_reconciliation = _legacy_oracle_reconciliation()
    upstream, contract, binding, request_preflight, request_reconciliation, package, preflight, record, reconciliation = context
    verification_contract = build_loop_oracle_verification_contract_298(
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
        contract_id=_CONTRACT_ID,
        requested_at=_REQUESTED_AT,
        expires_at=_EXPIRES_AT,
    )
    return (*context, oracle_reconciliation, verification_contract)


def _preflight_299():
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
    ) = _contract_298()
    verification_preflight = build_loop_oracle_verification_preflight_299(
        verification_contract,
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
        observed_loop_reconciliation_hash=reconciliation["reconciliation_hash"],
        observed_oracle_reconciliation_hash=oracle_reconciliation["reconciliation_hash"],
        observed_execution_record_hash=record["execution_record_hash"],
        transport_state="BLK_TEST_TRANSPORT_DISABLED_VERIFIER_ONLY",
        evaluated_at=_PREFLIGHT_AT,
    )
    return (
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
    )


def _record_300():
    context = _preflight_299()
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
    ) = context
    report = sample_loop_oracle_verification_report(
        verification_contract,
        record,
        reconciliation,
        oracle_reconciliation,
        verified_at=_VERIFIED_AT,
    )
    verification_record = record_loop_oracle_verification_300(
        verification_contract,
        verification_preflight,
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
        oracle_report=report,
    )
    return (*context, verification_record)


class Blk003LoopOracleVerification298To301Test(unittest.TestCase):
    def test_298_to_301_chain_verifies_exact_loop_evidence_without_mcp_or_approval(self):
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

        self.assertEqual(verification_contract["status"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY_NO_TRANSPORT")
        self.assertIn("BLK_SYSTEM_298_EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY", verification_contract["markers"])
        self.assertEqual(verification_contract["loop_execution_reconciliation_hash"], reconciliation["reconciliation_hash"])
        self.assertEqual(verification_contract["oracle_reconciliation_hash"], oracle_reconciliation["reconciliation_hash"])
        self.assertFalse(verification_contract["verification_rules"]["transport_start_allowed"])
        self.assertTrue(verification_contract["verification_rules"]["pass_is_evidence_not_approval"])
        self.assertFalse(verification_contract["side_effects"]["production_mcp_started"])
        self.assertFalse(verification_contract["side_effects"]["blk_test_pass_as_approval"])

        self.assertEqual(verification_preflight["status"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY")
        self.assertEqual(verification_preflight["preflight_result"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_READY")
        self.assertTrue(verification_preflight["verification_ready"])
        self.assertFalse(verification_preflight["mcp_transport_started"])
        self.assertFalse(verification_preflight["runtime_tooling_executed"])

        self.assertEqual(verification_record["status"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED")
        self.assertEqual(verification_record["verdict"], "PASS")
        self.assertTrue(verification_record["blk_test_passed"])
        self.assertFalse(verification_record["pass_is_approval"])
        self.assertEqual(verification_record["verified_hashes"]["beo_draft_hash"], record["beo_draft_hash"])
        self.assertFalse(verification_record["side_effects"]["beo_closeout_execution"])
        self.assertFalse(verification_record["side_effects"]["source_git_mutation"])

        self.assertEqual(final["status"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED_VERIFIER_ONLY")
        self.assertIn("BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED", final["markers"])
        self.assertEqual(final["next_frontier"], NEXT_FRONTIER_301)
        self.assertEqual(final["verified_loop_reconciliation_hash"], reconciliation["reconciliation_hash"])
        self.assertFalse(final["side_effects"]["beo_publication"])
        self.assertFalse(final["side_effects"]["production_blk_link"])
        self.assertRegex(final["reconciliation_hash"], r"^sha256:[0-9a-f]{64}$")

        self.assertEqual(
            validate_loop_oracle_verification_reconciliation_301(
                final,
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
            ),
            final,
        )

    def test_298_revalidates_full_loop_chain_and_legacy_oracle_contract(self):
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
        ) = _contract_298()

        self.assertEqual(
            validate_loop_oracle_verification_contract_298(
                verification_contract,
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
            ),
            verification_contract,
        )

        tampered_reconciliation = copy.deepcopy(reconciliation)
        tampered_reconciliation["final_result"] = "FAILED_TERMINAL"
        tampered_reconciliation["reconciliation_hash"] = hash_package(
            {key: value for key, value in tampered_reconciliation.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "loop execution reconciliation"):
            build_loop_oracle_verification_contract_298(
                package,
                preflight,
                record,
                tampered_reconciliation,
                contract,
                binding,
                request_preflight,
                request_reconciliation,
                upstream["approval_contract"],
                upstream["quarantine"],
                upstream["interaction"],
                upstream["gate"],
                oracle_reconciliation,
                contract_id="BLK-TEST-ORACLE-CONTRACT-BLK-SYSTEM-298-TAMPERED",
                requested_at=_REQUESTED_AT,
                expires_at=_EXPIRES_AT,
            )

        tampered_oracle = copy.deepcopy(oracle_reconciliation)
        tampered_oracle["side_effects"]["production_mcp_started"] = True
        tampered_oracle["reconciliation_hash"] = legacy_oracle._hash_package(
            {key: value for key, value in tampered_oracle.items() if key != "reconciliation_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "legacy oracle|production_mcp_started"):
            validate_loop_oracle_verification_contract_298(
                verification_contract,
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
                tampered_oracle,
            )

    def test_299_preflight_blocks_hash_drift_or_transport_state_without_launching_mcp(self):
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
            ready_preflight,
        ) = _preflight_299()

        self.assertEqual(
            validate_loop_oracle_verification_preflight_299(
                ready_preflight,
                verification_contract,
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
            ),
            ready_preflight,
        )

        drifted = build_loop_oracle_verification_preflight_299(
            verification_contract,
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
            observed_loop_reconciliation_hash="sha256:" + "a" * 64,
            observed_oracle_reconciliation_hash=oracle_reconciliation["reconciliation_hash"],
            observed_execution_record_hash=record["execution_record_hash"],
            transport_state="BLK_TEST_TRANSPORT_DISABLED_VERIFIER_ONLY",
            evaluated_at=_PREFLIGHT_AT,
        )
        self.assertEqual(drifted["preflight_result"], "EXACT_BLK_TEST_ORACLE_VERIFICATION_BLOCKED_BY_LOOP_HASH_DRIFT")
        self.assertFalse(drifted["verification_ready"])
        self.assertFalse(drifted["mcp_transport_started"])

        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "transport state|forbidden authority wording"):
            build_loop_oracle_verification_preflight_299(
                verification_contract,
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
                observed_loop_reconciliation_hash=reconciliation["reconciliation_hash"],
                observed_oracle_reconciliation_hash=oracle_reconciliation["reconciliation_hash"],
                observed_execution_record_hash=record["execution_record_hash"],
                transport_state="PRODUCTION_BLK_TEST_MCP_STARTED",
                evaluated_at=_PREFLIGHT_AT,
            )

    def test_300_record_binds_verified_hashes_and_rejects_pass_as_approval_or_missing_false_fields(self):
        context = _preflight_299()
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
        ) = context
        report = sample_loop_oracle_verification_report(
            verification_contract,
            record,
            reconciliation,
            oracle_reconciliation,
            verified_at=_VERIFIED_AT,
        )

        bad_hashes = copy.deepcopy(report)
        bad_hashes["verified_hashes"]["execution_record_hash"] = "sha256:" + "b" * 64
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "verified hash"):
            record_loop_oracle_verification_300(
                verification_contract,
                verification_preflight,
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
                oracle_report=bad_hashes,
            )

        pass_as_approval = copy.deepcopy(report)
        pass_as_approval["operator_notes"] = "BLK-test PASS approves BEO publication and production blk-link"
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "forbidden authority wording"):
            record_loop_oracle_verification_300(
                verification_contract,
                verification_preflight,
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
                oracle_report=pass_as_approval,
            )

        missing_false = copy.deepcopy(report)
        del missing_false["denied_side_effects"]["production_blk_link"]
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "denied_side_effects"):
            record_loop_oracle_verification_300(
                verification_contract,
                verification_preflight,
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
                oracle_report=missing_false,
            )

    def test_301_reconciliation_revalidates_record_schema_and_blocks_rehashed_side_effect_drift(self):
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

        tampered = copy.deepcopy(verification_record)
        tampered["side_effects"]["beo_publication"] = True
        tampered["verification_record_hash"] = hash_package(
            {key: value for key, value in tampered.items() if key != "verification_record_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "side_effects|BEO publication"):
            reconcile_loop_oracle_verification_301(
                verification_contract,
                verification_preflight,
                tampered,
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

        extra_marker = copy.deepcopy(verification_record)
        extra_marker["markers"].append("BEO_PUBLICATION_AUTHORIZED")
        extra_marker["verification_record_hash"] = hash_package(
            {key: value for key, value in extra_marker.items() if key != "verification_record_hash"}
        )
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "markers|forbidden authority wording"):
            validate_loop_oracle_verification_record_300(
                extra_marker,
                verification_contract,
                verification_preflight,
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

    def test_builders_return_defensive_copies(self):
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
        original_hash = verification_record["verification_record_hash"]
        verification_record["verified_hashes"]["beo_draft_hash"] = "sha256:" + "c" * 64
        with self.assertRaisesRegex(Blk003LoopOracleVerificationValidationError, "hash mismatch|verified hash"):
            validate_loop_oracle_verification_record_300(
                verification_record,
                verification_contract,
                verification_preflight,
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
        fresh = _record_300()[-1]
        self.assertEqual(fresh["verification_record_hash"], original_hash)

    def test_blk126_contract_doc_makes_verification_boundary_review_obvious(self):
        context = _record_300()
        verification_contract = context[-2]
        verification_record = context[-1]
        doc = BLK126.read_text()

        required = [
            "BLK_SYSTEM_298_EXACT_BLK_TEST_ORACLE_VERIFICATION_CONTRACT_READY",
            "BLK_SYSTEM_299_EXACT_BLK_TEST_ORACLE_VERIFICATION_PREFLIGHT_READY",
            "BLK_SYSTEM_300_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECORDED",
            "BLK_SYSTEM_301_EXACT_BLK_TEST_ORACLE_VERIFICATION_RECONCILED",
            verification_contract["verification_contract_hash"],
            verification_record["verification_record_hash"],
            NEXT_FRONTIER_301,
            "PASS is evidence, not approval",
            "no production BLK-test MCP transport",
            "no BEO closeout execution",
            "no BEO publication",
            "no RTM generation",
            "no production `blk-link`",
            "no durable target/source/Git mutation",
        ]
        missing = [marker for marker in required if marker not in doc]
        self.assertEqual(missing, [])
        self.assertEqual(scan_for_authority_laundering(doc, path="BLK-126"), [])


if __name__ == "__main__":
    unittest.main()
