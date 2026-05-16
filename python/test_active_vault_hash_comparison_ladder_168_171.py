import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_decision_execution_166 import (
    build_production_blk_link_rtm_trace_closure_decision_execution_166,
    valid_production_blk_link_rtm_trace_closure_decision_execution_166,
)
from production_blk_link_rtm_trace_closure_post_run_reconciliation_167 import (
    build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167,
    valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167,
)
from test_production_blk_link_rtm_trace_closure_decision_execution_166 import valid_blk165_request_package

from active_vault_hash_comparison_ladder_168_171 import (
    APPROVAL_ID_169,
    EXACT_EXCLUDED_AUTHORITIES_168,
    EXACT_EXCLUDED_AUTHORITIES_169,
    EXACT_EXCLUDED_AUTHORITIES_170,
    EXACT_EXCLUDED_AUTHORITIES_171,
    EXACT_OPERATOR_DECISION_TEXT_169,
    EXACT_PROOF_OBLIGATIONS_168,
    EXACT_PROOF_OBLIGATIONS_169,
    EXACT_PROOF_OBLIGATIONS_170,
    EXACT_PROOF_OBLIGATIONS_171,
    NEXT_FRONTIER_170_CLEAN,
    REQUEST_PACKAGE_ID_168,
    REQUEST_STATUS_168,
    RUN_ID_CONSUMED_169,
    SIDE_EFFECT_FLAGS_168,
    SIDE_EFFECT_FLAGS_169,
    SIDE_EFFECT_FLAGS_170,
    SIDE_EFFECT_FLAGS_171,
    build_active_vault_hash_comparison_authority_request_168,
    build_active_vault_hash_comparison_decision_execution_169,
    build_active_vault_hash_comparison_post_run_reconciliation_170,
    build_metadata_bound_drift_coverage_decision_request_171,
    valid_active_vault_hash_comparison_authority_request_168,
    valid_active_vault_hash_comparison_decision_execution_169,
    valid_active_vault_hash_comparison_post_run_reconciliation_170,
    valid_metadata_bound_drift_coverage_decision_request_171,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "active_vault_hash_comparison_ladder_168_171.py"


def valid_blk167_reconciliation_package():
    request165 = valid_blk165_request_package()
    request166 = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)
    execution166 = build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, request166)
    context167 = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166)
    return build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, context167)


def valid_168_request_package():
    reconciliation167 = valid_blk167_reconciliation_package()
    request168 = valid_active_vault_hash_comparison_authority_request_168(reconciliation167)
    return build_active_vault_hash_comparison_authority_request_168(reconciliation167, request168)


def valid_169_execution_package():
    request168 = valid_168_request_package()
    execution169 = valid_active_vault_hash_comparison_decision_execution_169(request168)
    return build_active_vault_hash_comparison_decision_execution_169(request168, execution169)


def valid_170_reconciliation_package():
    execution169 = valid_169_execution_package()
    context170 = valid_active_vault_hash_comparison_post_run_reconciliation_170(execution169)
    return build_active_vault_hash_comparison_post_run_reconciliation_170(execution169, context170)


class ActiveVaultHashComparisonLadder168171Test(unittest.TestCase):
    def test_168_request_binds_clean_blk167_without_approval_or_comparison(self):
        reconciliation167 = valid_blk167_reconciliation_package()
        request168 = valid_active_vault_hash_comparison_authority_request_168(reconciliation167)

        package = build_active_vault_hash_comparison_authority_request_168(reconciliation167, request168)

        self.assertEqual(package["request_status"], REQUEST_STATUS_168)
        self.assertEqual(package["authority_request_package_id"], REQUEST_PACKAGE_ID_168)
        self.assertTrue(package["request_future_exact_metadata_hash_only_active_vault_comparison"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], reconciliation167["reconciliation_package_hash"])
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request168))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_168)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_168)
        for flag in SIDE_EFFECT_FLAGS_168:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["authority_request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}))

    def test_169_captures_operator_decision_consumes_one_run_and_records_metadata_hash_comparison(self):
        request168 = valid_168_request_package()
        execution169 = valid_active_vault_hash_comparison_decision_execution_169(request168)

        package = build_active_vault_hash_comparison_decision_execution_169(request168, execution169)

        self.assertEqual(package["approval_id"], APPROVAL_ID_169)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_169)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_169)
        self.assertTrue(package["operator_decision_captured"])
        self.assertTrue(package["one_run_id_consumed_in_record_only_evidence"])
        self.assertTrue(package["active_vault_hash_comparison_performed"])
        self.assertTrue(package["metadata_hashes_match"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertEqual(package["decision_execution_request_hash"], _canonical_hash(execution169))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_169)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_169)
        true_flags = {"active_vault_hash_comparison_performed", "operator_decision_captured", "one_run_id_consumed_in_record_only_evidence"}
        for flag in SIDE_EFFECT_FLAGS_169:
            if flag in true_flags:
                self.assertIs(package[flag], True, flag)
            else:
                self.assertIs(package[flag], False, flag)
        self.assertEqual(package["comparison_record_hash"], _canonical_hash({k: v for k, v in package["comparison_record"].items() if k != "comparison_record_hash"}))
        self.assertEqual(package["decision_execution_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "decision_execution_package_hash"}))

    def test_170_reconciles_clean_comparison_and_names_request_frontier_without_granting_it(self):
        execution169 = valid_169_execution_package()
        context170 = valid_active_vault_hash_comparison_post_run_reconciliation_170(execution169)

        package = build_active_vault_hash_comparison_post_run_reconciliation_170(execution169, context170)

        self.assertTrue(package["clean_metadata_hash_comparison_reconciled"])
        self.assertFalse(package["observed_failure_requires_171_hardening"])
        self.assertEqual(package["recommended_next_frontier"], NEXT_FRONTIER_170_CLEAN)
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context170))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_170)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_170)
        for flag in SIDE_EFFECT_FLAGS_170:
            self.assertIs(package[flag], False, flag)

    def test_171_emits_request_only_drift_coverage_decision_package_after_clean_170(self):
        reconciliation170 = valid_170_reconciliation_package()
        request171 = valid_metadata_bound_drift_coverage_decision_request_171(reconciliation170)

        package = build_metadata_bound_drift_coverage_decision_request_171(reconciliation170, request171)

        self.assertTrue(package["request_future_exact_metadata_bound_drift_coverage_decision_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertEqual(package["upstream_reconciliation_package_hash"], reconciliation170["reconciliation_package_hash"])
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request171))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_171)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_171)
        for flag in SIDE_EFFECT_FLAGS_171:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["authority_request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}))

    def test_ladder_rejects_forged_hashes_laundering_bad_sets_and_side_effects(self):
        reconciliation167 = valid_blk167_reconciliation_package()
        base168 = valid_active_vault_hash_comparison_authority_request_168(reconciliation167)
        for patch, message in [
            ({"authority_request_package_id": "ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-１６８-００１"}, "authority_request_package_id must be"),
            ({"selected_frontier": "RTMGeneration"}, "selected_frontier must be|authority-laundering text"),
            ({"operator_identity": "discord:684235178083745819-ActiveVaultHashComparisonAuthorized"}, "authority-laundering text"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_168) + [sorted(EXACT_EXCLUDED_AUTHORITIES_168)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"operator_attestation": base168["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
            ({"authority_request_package_id": "ACTIVE-VAULT-HASH-COMPARISON-AUTHORITY-REQUEST-168-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
        ]:
            request = copy.deepcopy(base168)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_authority_request_168(reconciliation167, request)

        request168 = valid_168_request_package()
        base169 = valid_active_vault_hash_comparison_decision_execution_169(request168)
        for flag in SIDE_EFFECT_FLAGS_169:
            if flag in {"active_vault_hash_comparison_performed", "operator_decision_captured", "one_run_id_consumed_in_record_only_evidence"}:
                continue
            execution = copy.deepcopy(base169)
            execution[flag] = True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                    build_active_vault_hash_comparison_decision_execution_169(request168, execution)

        forged = copy.deepcopy(request168)
        forged["authority_request_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "authority_request_package_hash does not match submitted BLK-168 package"):
            build_active_vault_hash_comparison_decision_execution_169(forged, base169)

        forged = copy.deepcopy(request168)
        forged["protected_body_reads"] = True
        forged["authority_request_package_hash"] = _canonical_hash({k: v for k, v in forged.items() if k != "authority_request_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-168 authority request package hash mismatch|protected_body_reads"):
            build_active_vault_hash_comparison_decision_execution_169(forged, valid_active_vault_hash_comparison_decision_execution_169(forged))

        execution169 = valid_169_execution_package()
        forged169 = copy.deepcopy(execution169)
        forged169["coverage_truth_established"] = True
        forged169["decision_execution_package_hash"] = _canonical_hash({k: v for k, v in forged169.items() if k != "decision_execution_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-169 decision execution package hash mismatch|coverage_truth_established"):
            build_active_vault_hash_comparison_post_run_reconciliation_170(forged169, valid_active_vault_hash_comparison_post_run_reconciliation_170(forged169))

        forged169 = copy.deepcopy(execution169)
        forged169["comparison_record"]["protected_body_reads"] = True
        forged169["comparison_record"]["comparison_record_hash"] = _canonical_hash({k: v for k, v in forged169["comparison_record"].items() if k != "comparison_record_hash"})
        forged169["comparison_record_hash"] = forged169["comparison_record"]["comparison_record_hash"]
        forged169["decision_execution_package_hash"] = _canonical_hash({k: v for k, v in forged169.items() if k != "decision_execution_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-169 decision execution package hash mismatch|comparison_record protected_body_reads"):
            build_active_vault_hash_comparison_post_run_reconciliation_170(forged169, valid_active_vault_hash_comparison_post_run_reconciliation_170(forged169))

        rec170 = valid_170_reconciliation_package()
        forged170 = copy.deepcopy(rec170)
        forged170["upstream_decision_execution_package_hash"] = "sha256:" + "0" * 64
        forged170["protected_body_reads"] = True
        forged170["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged170.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-170 reconciliation package hash mismatch|protected_body_reads"):
            build_metadata_bound_drift_coverage_decision_request_171(forged170, valid_metadata_bound_drift_coverage_decision_request_171(forged170))

        malformed = valid_active_vault_hash_comparison_decision_execution_169(request168)
        malformed["active_metadata_records"][0]["version_hash"] = {"not": "a canonical hash"}
        with self.assertRaisesRegex(ValueError, "version_hash must be canonical sha256"):
            build_active_vault_hash_comparison_decision_execution_169(request168, malformed)

    def test_hash_binding_and_defensive_copies_prevent_post_hash_mutation(self):
        request168 = valid_168_request_package()
        execution169 = valid_active_vault_hash_comparison_decision_execution_169(request168)
        package = build_active_vault_hash_comparison_decision_execution_169(request168, execution169)
        alt = valid_active_vault_hash_comparison_decision_execution_169(
            request168,
            decided_at="2099-05-16T20:36:00+10:00",
            requested_at="2099-05-16T20:37:00+10:00",
            expires_at="2099-05-16T20:44:00+10:00",
        )
        alt_package = build_active_vault_hash_comparison_decision_execution_169(request168, alt)

        self.assertNotEqual(package["decision_execution_request_hash"], alt_package["decision_execution_request_hash"])
        self.assertNotEqual(package["decision_execution_package_hash"], alt_package["decision_execution_package_hash"])
        execution169["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        request168["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(package["operator_attestation"], execution169["operator_attestation"])
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
