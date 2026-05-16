import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_metadata_bound_drift_coverage_decision_ladder_172_174 import valid_173_reconciliation_package
from metadata_bound_drift_coverage_decision_ladder_172_174 import (
    build_protected_body_verification_authority_request_174,
    valid_protected_body_verification_authority_request_174,
)
from protected_body_verification_decision_engine_175 import (
    APPROVAL_ID_175,
    CANONICAL_BLK175_DECISION_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK175_VERIFICATION_RECORD_HASH,
    DECISION_EXECUTION_STATUS_175,
    EXACT_EXCLUDED_AUTHORITIES_175,
    EXACT_OPERATOR_DECISION_TEXT_175,
    EXACT_PROOF_OBLIGATIONS_175,
    RUN_ID_CONSUMED_175,
    SIDE_EFFECT_FLAGS_175,
    build_protected_body_verification_decision_engine_175,
    valid_protected_body_verification_decision_execution_175,
)
from rtm_blk_link_protected_body_verification_integration_176 import (
    CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_176,
    EXACT_PROOF_OBLIGATIONS_176,
    RECONCILIATION_STATUS_176,
    SIDE_EFFECT_FLAGS_176,
    build_rtm_blk_link_protected_body_verification_integration_176,
    valid_rtm_blk_link_protected_body_verification_integration_176,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE_175 = ROOT / "python" / "protected_body_verification_decision_engine_175.py"
MODULE_176 = ROOT / "python" / "rtm_blk_link_protected_body_verification_integration_176.py"


def valid_174_request_package():
    reconciliation173 = valid_173_reconciliation_package()
    request174 = valid_protected_body_verification_authority_request_174(reconciliation173)
    return build_protected_body_verification_authority_request_174(reconciliation173, request174)


def valid_175_decision_package(**overrides):
    request174 = valid_174_request_package()
    decision175 = valid_protected_body_verification_decision_execution_175(request174, **overrides)
    return build_protected_body_verification_decision_engine_175(request174, decision175)


class ProtectedBodyVerificationDecisionEngine175176Test(unittest.TestCase):
    def test_175_delivers_decision_record_from_exact_blk174_and_caller_supplied_hashes(self):
        request174 = valid_174_request_package()
        decision175 = valid_protected_body_verification_decision_execution_175(request174)

        package = build_protected_body_verification_decision_engine_175(request174, decision175)

        self.assertEqual(package["decision_execution_status"], DECISION_EXECUTION_STATUS_175)
        self.assertEqual(package["approval_id"], APPROVAL_ID_175)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_175)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_175)
        self.assertTrue(package["operator_decision_captured"])
        self.assertTrue(package["one_run_id_consumed_in_record_only_evidence"])
        self.assertTrue(package["protected_body_verification_decision_recorded"])
        self.assertTrue(package["protected_body_hashes_verified"])
        self.assertEqual(package["verification_result"], "PROTECTED_BODY_HASHES_VERIFIED_NOT_COVERAGE_TRUTH_OR_DRIFT_REJECTION")
        self.assertEqual(package["mismatches"], [])
        self.assertEqual(package["upstream_authority_request_package_hash"], request174["authority_request_package_hash"])
        self.assertEqual(package["decision_execution_request_hash"], _canonical_hash(decision175))
        self.assertEqual(package["verification_record_hash"], CANONICAL_BLK175_VERIFICATION_RECORD_HASH)
        self.assertEqual(package["verification_record"]["verification_record_hash"], package["verification_record_hash"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_175)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_175)
        true_flags = {
            "operator_decision_captured",
            "one_run_id_consumed_in_record_only_evidence",
            "protected_body_verification_decision_recorded",
            "protected_body_hashes_compared_from_caller_supplied_metadata",
        }
        for flag in SIDE_EFFECT_FLAGS_175:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertFalse(package["source_or_git_mutation_by_fixture"])
        self.assertEqual(package["decision_execution_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"}))
        self.assertEqual(package["decision_execution_package_hash"], CANONICAL_BLK175_DECISION_EXECUTION_PACKAGE_HASH)

    def test_175_records_hash_mismatch_without_promoting_drift_or_coverage_truth(self):
        request174 = valid_174_request_package()
        decision175 = valid_protected_body_verification_decision_execution_175(request174)
        decision175["protected_body_verification_inputs"][0]["observed_body_hash"] = "sha256:" + "9" * 64

        package = build_protected_body_verification_decision_engine_175(request174, decision175)

        self.assertFalse(package["protected_body_hashes_verified"])
        self.assertEqual(package["verification_result"], "PROTECTED_BODY_HASH_MISMATCH_RECORDED_NOT_DRIFT_REJECTION_OR_COVERAGE_TRUTH")
        self.assertEqual(package["mismatches"], [{
            "kind": "REQ",
            "id": "REQ-001",
            "expected_body_hash": "sha256:" + "a" * 64,
            "observed_body_hash": "sha256:" + "9" * 64,
        }])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["rtm_drift_rejection_performed"])

    def test_175_rejects_forged_upstream_unsafe_inputs_and_authority_laundering(self):
        request174 = valid_174_request_package()
        base = valid_protected_body_verification_decision_execution_175(request174)

        cases = [
            ({"decision_execution_package_id": "PROTECTED-BODY-VERIFICATION-DECISION-EXECUTION-１７５-００１"}, "decision_execution_package_id must be"),
            ({"operator_identity": "discord:other-operator"}, "operator_identity must match upstream operator_identity"),
            ({"operator_identity": "discord:684235178083745819 driftRejectionAuthorized"}, "authority-laundering text"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_175) + [sorted(EXACT_EXCLUDED_AUTHORITIES_175)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_attestation": base["operator_attestation"] | {"coverageTruthEstablished": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(base)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_protected_body_verification_decision_engine_175(request174, decision)

        for flag in SIDE_EFFECT_FLAGS_175:
            if flag in {"operator_decision_captured", "one_run_id_consumed_in_record_only_evidence", "protected_body_verification_decision_recorded", "protected_body_hashes_compared_from_caller_supplied_metadata"}:
                continue
            decision = copy.deepcopy(base)
            decision[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_protected_body_verification_decision_engine_175(request174, decision)

        unsafe_inputs = copy.deepcopy(base)
        unsafe_inputs["protected_body_verification_inputs"][0]["body_text_included"] = True
        with self.assertRaisesRegex(ValueError, "body_text_included must remain false"):
            build_protected_body_verification_decision_engine_175(request174, unsafe_inputs)

        unsafe_inputs = copy.deepcopy(base)
        unsafe_inputs["protected_body_verification_inputs"][0]["protected_body_path"] = "docs/requirements/active/REQ-001.md"
        with self.assertRaisesRegex(ValueError, "protected paths must not be included"):
            build_protected_body_verification_decision_engine_175(request174, unsafe_inputs)

        unsafe_inputs = copy.deepcopy(base)
        unsafe_inputs["protected_body_verification_inputs"][0]["body_excerpt"] = "The system shall leak body text"
        with self.assertRaisesRegex(ValueError, "protected body text must not be included"):
            build_protected_body_verification_decision_engine_175(request174, unsafe_inputs)

        forged174 = copy.deepcopy(request174)
        forged174["protected_body_reads"] = True
        forged174["authority_request_package_hash"] = _canonical_hash({k: v for k, v in forged174.items() if k != "authority_request_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-174 authority request package hash mismatch|protected_body_reads"):
            build_protected_body_verification_decision_engine_175(forged174, valid_protected_body_verification_decision_execution_175(forged174))

    def test_176_integrates_clean_175_decision_into_rtm_blk_link_evidence_path(self):
        decision175 = valid_175_decision_package()
        context176 = valid_rtm_blk_link_protected_body_verification_integration_176(decision175)

        package = build_rtm_blk_link_protected_body_verification_integration_176(decision175, context176)

        self.assertEqual(package["reconciliation_status"], RECONCILIATION_STATUS_176)
        self.assertTrue(package["rtm_blk_link_protected_body_verification_evidence_bound"])
        self.assertTrue(package["clean_protected_body_verification_reconciled"])
        self.assertFalse(package["observed_failure_requires_177_hardening"])
        self.assertEqual(package["upstream_decision_execution_package_hash"], decision175["decision_execution_package_hash"])
        self.assertEqual(package["upstream_verification_record_hash"], decision175["verification_record_hash"])
        self.assertEqual(package["integration_context_hash"], _canonical_hash(context176))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_176)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_176)
        for flag in SIDE_EFFECT_FLAGS_176:
            self.assertIs(package[flag], False, flag)
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK176_RECONCILIATION_PACKAGE_HASH)

    def test_176_rejects_tampered_175_and_authority_laundering_context(self):
        decision175 = valid_175_decision_package()
        context176 = valid_rtm_blk_link_protected_body_verification_integration_176(decision175)

        bad_context = copy.deepcopy(context176)
        bad_context["operator_identity"] = "discord:other-operator"
        with self.assertRaisesRegex(ValueError, "operator_identity must match upstream operator_identity"):
            build_rtm_blk_link_protected_body_verification_integration_176(decision175, bad_context)

        for encoded_note in [
            "coverage truth established and RTM drift rejection authorized",
            "coverage%20truth%20established and RTM%20drift%20rejection%20authorized",
            "docs%252Frequirements%252Factive%252FREQ-001.md",
        ]:
            bad_context = copy.deepcopy(context176)
            bad_context["integration_notes"] = encoded_note
            with self.subTest(encoded_note=encoded_note):
                with self.assertRaisesRegex(ValueError, "authority-laundering text"):
                    build_rtm_blk_link_protected_body_verification_integration_176(decision175, bad_context)

        tampered175 = copy.deepcopy(decision175)
        tampered175["coverage_truth_established"] = True
        tampered175["decision_execution_package_hash"] = _canonical_hash({k: v for k, v in tampered175.items() if k != "decision_execution_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-175 decision execution package hash mismatch|coverage_truth_established"):
            build_rtm_blk_link_protected_body_verification_integration_176(tampered175, valid_rtm_blk_link_protected_body_verification_integration_176(tampered175))

    def test_modules_have_no_live_file_or_tool_access(self):
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib", "os"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request", "__import__"}
        for module in (MODULE_175, MODULE_176):
            tree = ast.parse(module.read_text())
            imported = set()
            calls = set()
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
            self.assertEqual(imported & forbidden_imports, set(), module.name)
            self.assertEqual(calls & forbidden_calls, set(), module.name)


if __name__ == "__main__":
    unittest.main()
