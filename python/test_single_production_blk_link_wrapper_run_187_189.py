import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_reusable_blk_link_readiness_kernel_183_186 import valid_185_dry_run_package
from reusable_blk_link_readiness_kernel_183_186 import (
    CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
    CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH,
    build_reusable_blk_link_readiness_kernel_reconciliation_186,
    valid_reusable_blk_link_readiness_kernel_reconciliation_186,
)

from single_production_blk_link_wrapper_run_187_189 import (
    APPROVAL_ID_188,
    CANONICAL_BLK187_REQUEST_PACKAGE_HASH,
    CANONICAL_BLK188_EXECUTION_PACKAGE_HASH,
    CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_187,
    EXACT_EXCLUDED_AUTHORITIES_188,
    EXACT_EXCLUDED_AUTHORITIES_189,
    EXACT_OPERATOR_DECISION_TEXT_188,
    EXACT_PROOF_OBLIGATIONS_187,
    EXACT_PROOF_OBLIGATIONS_188,
    EXACT_PROOF_OBLIGATIONS_189,
    RUN_ID_CONSUMED_188,
    SIDE_EFFECT_FLAGS_187,
    SIDE_EFFECT_FLAGS_188,
    SIDE_EFFECT_FLAGS_189,
    build_single_production_blk_link_wrapper_execution_188,
    build_single_production_blk_link_wrapper_reconciliation_189,
    build_single_production_blk_link_wrapper_request_187,
    valid_single_production_blk_link_wrapper_execution_188,
    valid_single_production_blk_link_wrapper_reconciliation_189,
    valid_single_production_blk_link_wrapper_request_187,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "single_production_blk_link_wrapper_run_187_189.py"


def valid_186_reconciliation_package():
    dryrun185 = valid_185_dry_run_package()
    context186 = valid_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185)
    return build_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185, context186)


def valid_187_request_package():
    reconciliation186 = valid_186_reconciliation_package()
    request187 = valid_single_production_blk_link_wrapper_request_187(reconciliation186)
    return build_single_production_blk_link_wrapper_request_187(reconciliation186, request187)


def valid_188_execution_package():
    request187 = valid_187_request_package()
    execution188 = valid_single_production_blk_link_wrapper_execution_188(request187)
    return build_single_production_blk_link_wrapper_execution_188(request187, execution188)


class SingleProductionBlkLinkWrapperRun187189Test(unittest.TestCase):
    def test_187_requests_one_exact_production_wrapper_run_without_executing_it(self):
        reconciliation186 = valid_186_reconciliation_package()
        request187 = valid_single_production_blk_link_wrapper_request_187(reconciliation186)

        package = build_single_production_blk_link_wrapper_request_187(reconciliation186, request187)

        self.assertEqual(package["upstream_reconciliation_package_hash"], CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH)
        self.assertEqual(package["upstream_contract_package_hash"], CANONICAL_BLK184_CONTRACT_PACKAGE_HASH)
        self.assertTrue(package["request_one_exact_production_wrapper_run"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["production_wrapper_run_executed"])
        self.assertFalse(package["reusable_production_blk_link_authority_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_187)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_187)
        for flag in SIDE_EFFECT_FLAGS_187:
            self.assertIs(package[flag], flag == "request_one_exact_production_wrapper_run", flag)
        self.assertEqual(package["request_package_hash"], CANONICAL_BLK187_REQUEST_PACKAGE_HASH)
        self.assertEqual(package["request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"}))

    def test_188_executes_one_exact_production_wrapper_run_without_reusable_or_adjacent_authority(self):
        request187 = valid_187_request_package()
        execution188 = valid_single_production_blk_link_wrapper_execution_188(request187)

        package = build_single_production_blk_link_wrapper_execution_188(request187, execution188)

        self.assertEqual(package["upstream_request_package_hash"], CANONICAL_BLK187_REQUEST_PACKAGE_HASH)
        self.assertEqual(package["approval_id"], APPROVAL_ID_188)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_188)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_188)
        self.assertTrue(package["per_run_exact_approval_captured"])
        self.assertTrue(package["one_run_id_consumed_in_production_wrapper_evidence"])
        self.assertTrue(package["production_wrapper_run_executed"])
        self.assertEqual(package["wrapper_run_result"], "SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECORDED_CLEAN")
        self.assertFalse(package["reusable_production_blk_link_authority_granted"])
        self.assertFalse(package["runtime_rtm_generation_authorized"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["target_source_git_mutation_performed"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_188)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_188)
        true_flags = {"per_run_exact_approval_captured", "one_run_id_consumed_in_production_wrapper_evidence", "production_wrapper_run_executed"}
        for flag in SIDE_EFFECT_FLAGS_188:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertEqual(package["execution_package_hash"], CANONICAL_BLK188_EXECUTION_PACKAGE_HASH)

    def test_189_reconciles_single_run_and_names_operator_review_without_granting_reuse(self):
        execution188 = valid_188_execution_package()
        context189 = valid_single_production_blk_link_wrapper_reconciliation_189(execution188)

        package = build_single_production_blk_link_wrapper_reconciliation_189(execution188, context189)

        self.assertEqual(package["upstream_execution_package_hash"], CANONICAL_BLK188_EXECUTION_PACKAGE_HASH)
        self.assertTrue(package["clean_single_production_wrapper_run_reconciled"])
        self.assertFalse(package["observed_failure_requires_hardening"])
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(package["recommended_next_frontier"], "NEXT_FRONTIER_POST_SINGLE_PRODUCTION_WRAPPER_RUN_OPERATOR_REVIEW_NOT_GRANTED")
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_189)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_189)
        for flag in SIDE_EFFECT_FLAGS_189:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH)

    def test_ladder_rejects_rehashed_upstream_retargeting_laundering_and_false_side_effects(self):
        reconciliation186 = valid_186_reconciliation_package()
        forged186 = copy.deepcopy(reconciliation186)
        forged186["next_frontier_granted"] = True
        forged186["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged186.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-186 reconciliation package hash mismatch|next_frontier_granted"):
            build_single_production_blk_link_wrapper_request_187(forged186, valid_single_production_blk_link_wrapper_request_187(forged186))

        request187 = valid_187_request_package()
        execution188 = valid_single_production_blk_link_wrapper_execution_188(request187)
        for patch, message in [
            ({"operator_identity": "discord:684235178083745819 reusableProductionBlkLinkAuthorityGranted"}, "authority-laundering text|operator_identity must match"),
            ({"operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_188 + " and reusable authority forever"}, "operator_decision_text_raw must be"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_188) + [sorted(EXACT_EXCLUDED_AUTHORITIES_188)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"runtime_notes": "RTMGeneration approved and coverageTruthEstablished docs%252Frequirements%252Factive%252FREQ-001.md"}, "authority-laundering text"),
            ({"reusable_production_blk_link_authority_granted": True}, "reusable_production_blk_link_authority_granted must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"target_source_git_mutation_performed": True}, "target_source_git_mutation_performed must remain false"),
        ]:
            candidate = copy.deepcopy(execution188)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_single_production_blk_link_wrapper_execution_188(request187, candidate)

        replayed = copy.deepcopy(execution188)
        replayed["replayed"] = True
        with self.assertRaisesRegex(ValueError, "record must not be replayed"):
            build_single_production_blk_link_wrapper_execution_188(request187, replayed)

    def test_hash_binding_and_defensive_copies_prevent_alias_mutation(self):
        request187 = valid_187_request_package()
        execution188 = valid_single_production_blk_link_wrapper_execution_188(request187)
        package = build_single_production_blk_link_wrapper_execution_188(request187, execution188)
        alt = valid_single_production_blk_link_wrapper_execution_188(
            request187,
            requested_at="2099-05-17T00:12:00+10:00",
            expires_at="2099-05-17T00:24:00+10:00",
        )
        alt_package = build_single_production_blk_link_wrapper_execution_188(request187, alt)

        self.assertNotEqual(package["execution_request_hash"], alt_package["execution_request_hash"])
        self.assertNotEqual(package["execution_package_hash"], alt_package["execution_package_hash"])
        execution188["operator_attestation"]["protected_body_reads_excluded"] = "mutated"
        request187["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIs(package["operator_attestation"]["protected_body_reads_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, package["exact_trace_identities"])

    def test_module_has_no_shell_network_tooling_or_protected_body_file_access(self):
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
