import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from active_vault_hash_comparison_ladder_168_171 import (
    build_metadata_bound_drift_coverage_decision_request_171,
    valid_metadata_bound_drift_coverage_decision_request_171,
)
from test_active_vault_hash_comparison_ladder_168_171 import valid_170_reconciliation_package

from metadata_bound_drift_coverage_decision_ladder_172_174 import (
    APPROVAL_ID_172,
    CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH,
    CANONICAL_BLK174_AUTHORITY_REQUEST_PACKAGE_HASH,
    DECISION_EXECUTION_STATUS_172,
    EXACT_EXCLUDED_AUTHORITIES_172,
    EXACT_EXCLUDED_AUTHORITIES_173,
    EXACT_EXCLUDED_AUTHORITIES_174,
    EXACT_OPERATOR_DECISION_TEXT_172,
    EXACT_PROOF_OBLIGATIONS_172,
    EXACT_PROOF_OBLIGATIONS_173,
    EXACT_PROOF_OBLIGATIONS_174,
    NEXT_FRONTIER_173_CLEAN,
    REQUEST_PACKAGE_ID_174,
    REQUEST_STATUS_174,
    RUN_ID_CONSUMED_172,
    SIDE_EFFECT_FLAGS_172,
    SIDE_EFFECT_FLAGS_173,
    SIDE_EFFECT_FLAGS_174,
    build_metadata_bound_drift_coverage_decision_execution_172,
    build_metadata_bound_drift_coverage_post_decision_reconciliation_173,
    build_protected_body_verification_authority_request_174,
    valid_metadata_bound_drift_coverage_decision_execution_172,
    valid_metadata_bound_drift_coverage_post_decision_reconciliation_173,
    valid_protected_body_verification_authority_request_174,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_drift_coverage_decision_ladder_172_174.py"


def valid_171_request_package():
    reconciliation170 = valid_170_reconciliation_package()
    request171 = valid_metadata_bound_drift_coverage_decision_request_171(reconciliation170)
    return build_metadata_bound_drift_coverage_decision_request_171(reconciliation170, request171)


def valid_172_decision_package():
    request171 = valid_171_request_package()
    decision172 = valid_metadata_bound_drift_coverage_decision_execution_172(request171)
    return build_metadata_bound_drift_coverage_decision_execution_172(request171, decision172)


def valid_173_reconciliation_package():
    decision172 = valid_172_decision_package()
    context173 = valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172)
    return build_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172, context173)


class MetadataBoundDriftCoverageDecisionLadder172174Test(unittest.TestCase):
    def test_172_captures_exact_operator_decision_and_records_metadata_bound_decision_only(self):
        request171 = valid_171_request_package()
        decision172 = valid_metadata_bound_drift_coverage_decision_execution_172(request171)

        package = build_metadata_bound_drift_coverage_decision_execution_172(request171, decision172)

        self.assertEqual(package["decision_execution_status"], DECISION_EXECUTION_STATUS_172)
        self.assertEqual(package["approval_id"], APPROVAL_ID_172)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_172)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_172)
        self.assertTrue(package["operator_decision_captured"])
        self.assertTrue(package["one_run_id_consumed_in_record_only_evidence"])
        self.assertTrue(package["metadata_bound_drift_coverage_decision_recorded"])
        self.assertEqual(package["metadata_drift_status"], "NO_METADATA_HASH_DRIFT_OBSERVED_NOT_AUTHORITATIVE_DRIFT_REJECTION")
        self.assertEqual(package["metadata_coverage_status"], "METADATA_TRACE_SET_COHERENT_NOT_COVERAGE_TRUTH")
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        self.assertEqual(package["upstream_authority_request_package_hash"], request171["authority_request_package_hash"])
        self.assertEqual(package["decision_execution_request_hash"], _canonical_hash(decision172))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_172)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_172)
        true_flags = {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "metadata_bound_drift_coverage_decision_recorded"}
        for flag in SIDE_EFFECT_FLAGS_172:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertEqual(package["decision_execution_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"}))
        self.assertEqual(package["decision_execution_package_hash"], CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH)

    def test_173_reconciles_clean_decision_and_selects_174_without_granting_it(self):
        decision172 = valid_172_decision_package()
        context173 = valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172)

        package = build_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172, context173)

        self.assertTrue(package["clean_metadata_bound_decision_reconciled"])
        self.assertFalse(package["observed_failure_requires_174_hardening"])
        self.assertEqual(package["recommended_next_frontier"], NEXT_FRONTIER_173_CLEAN)
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(package["upstream_decision_execution_package_hash"], CANONICAL_BLK172_DECISION_EXECUTION_PACKAGE_HASH)
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context173))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_173)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_173)
        for flag in SIDE_EFFECT_FLAGS_173:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK173_RECONCILIATION_PACKAGE_HASH)

    def test_174_needed_after_clean_173_emits_request_only_protected_body_verification_package(self):
        reconciliation173 = valid_173_reconciliation_package()
        request174 = valid_protected_body_verification_authority_request_174(reconciliation173)

        package = build_protected_body_verification_authority_request_174(reconciliation173, request174)

        self.assertEqual(package["request_status"], REQUEST_STATUS_174)
        self.assertEqual(package["authority_request_package_id"], REQUEST_PACKAGE_ID_174)
        self.assertTrue(package["request_future_exact_protected_body_verification_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["protected_body_hashing_attempted"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], reconciliation173["reconciliation_package_hash"])
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request174))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_174)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_174)
        for flag in SIDE_EFFECT_FLAGS_174:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["authority_request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}))
        self.assertEqual(package["authority_request_package_hash"], CANONICAL_BLK174_AUTHORITY_REQUEST_PACKAGE_HASH)

    def test_ladder_rejects_rehashed_upstream_laundering_and_adjacent_authority_flags(self):
        request171 = valid_171_request_package()
        base172 = valid_metadata_bound_drift_coverage_decision_execution_172(request171)

        for patch, message in [
            ({"decision_execution_package_id": "METADATA-BOUND-DRIFT-COVERAGE-DECISION-EXECUTION-１７２-００１"}, "decision_execution_package_id must be"),
            ({"selected_frontier": "coverageTruthAuthorized"}, "selected_frontier must be|authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-driftRejectionExecuted"}, "authority-laundering text"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_172) + [sorted(EXACT_EXCLUDED_AUTHORITIES_172)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"operator_attestation": base172["operator_attestation"] | {"ProtectedBodyReadsApproved": True}}, "unexpected field"),
        ]:
            decision = copy.deepcopy(base172)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_drift_coverage_decision_execution_172(request171, decision)

        for flag in SIDE_EFFECT_FLAGS_172:
            if flag in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "metadata_bound_drift_coverage_decision_recorded"}:
                continue
            decision = copy.deepcopy(base172)
            decision[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_metadata_bound_drift_coverage_decision_execution_172(request171, decision)

        mismatched_operator = copy.deepcopy(base172)
        mismatched_operator["operator_identity"] = "discord:other-operator"
        with self.assertRaisesRegex(ValueError, "operator_identity must match upstream operator_identity"):
            build_metadata_bound_drift_coverage_decision_execution_172(request171, mismatched_operator)

        forged171 = copy.deepcopy(request171)
        forged171["protected_body_reads"] = True
        forged171["authority_request_package_hash"] = _canonical_hash({k: v for k, v in forged171.items() if k != "authority_request_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-171 authority request package hash mismatch|protected_body_reads"):
            build_metadata_bound_drift_coverage_decision_execution_172(forged171, valid_metadata_bound_drift_coverage_decision_execution_172(forged171))

        decision172 = valid_172_decision_package()
        context173 = valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172)
        context173["operator_identity"] = "discord:other-operator"
        with self.assertRaisesRegex(ValueError, "operator_identity must match upstream operator_identity"):
            build_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172, context173)

        context173 = valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172)
        context173["operator_identity"] = 123
        with self.assertRaisesRegex(ValueError, "operator_identity must be a string|operator_identity must match upstream operator_identity"):
            build_metadata_bound_drift_coverage_post_decision_reconciliation_173(decision172, context173)

        decision172 = valid_172_decision_package()
        forged172 = copy.deepcopy(decision172)
        forged172["coverage_truth_established"] = True
        forged172["decision_execution_package_hash"] = _canonical_hash({k: v for k, v in forged172.items() if k != "decision_execution_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-172 decision execution package hash mismatch|coverage_truth_established"):
            build_metadata_bound_drift_coverage_post_decision_reconciliation_173(forged172, valid_metadata_bound_drift_coverage_post_decision_reconciliation_173(forged172))

        reconciliation173 = valid_173_reconciliation_package()
        request174 = valid_protected_body_verification_authority_request_174(reconciliation173)
        request174["operator_identity"] = "discord:other-operator"
        with self.assertRaisesRegex(ValueError, "operator_identity must match upstream operator_identity"):
            build_protected_body_verification_authority_request_174(reconciliation173, request174)

        reconciliation173 = valid_173_reconciliation_package()
        forged173 = copy.deepcopy(reconciliation173)
        forged173["next_frontier_granted"] = True
        forged173["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged173.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-173 reconciliation package hash mismatch|next_frontier_granted"):
            build_protected_body_verification_authority_request_174(forged173, valid_protected_body_verification_authority_request_174(forged173))

    def test_hash_binding_and_defensive_copies_prevent_post_hash_mutation(self):
        request171 = valid_171_request_package()
        decision172 = valid_metadata_bound_drift_coverage_decision_execution_172(request171)
        package = build_metadata_bound_drift_coverage_decision_execution_172(request171, decision172)
        alt = valid_metadata_bound_drift_coverage_decision_execution_172(
            request171,
            decided_at="2099-05-16T21:06:00+10:00",
            requested_at="2099-05-16T21:07:00+10:00",
            expires_at="2099-05-16T21:14:00+10:00",
        )
        alt_package = build_metadata_bound_drift_coverage_decision_execution_172(request171, alt)

        self.assertNotEqual(package["decision_execution_request_hash"], alt_package["decision_execution_request_hash"])
        self.assertNotEqual(package["decision_execution_package_hash"], alt_package["decision_execution_package_hash"])
        decision172["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        request171["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(package["operator_attestation"], decision172["operator_attestation"])
        self.assertIs(package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, package["exact_trace_identities"])

    def test_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib", "os"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request", "__import__"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    calls.add(func.attr)
                elif isinstance(func, ast.Name):
                    calls.add(func.id)
        self.assertEqual(imported & forbidden_imports, set())
        self.assertEqual(calls & forbidden_calls, set())


if __name__ == "__main__":
    unittest.main()
