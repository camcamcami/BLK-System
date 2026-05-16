import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_rtm_blk_link_followup_ladder_178_182 import valid_181_export_package
from rtm_blk_link_followup_ladder_178_182 import (
    CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH,
    build_rtm_blk_link_followup_post_export_reconciliation_182,
    valid_rtm_blk_link_followup_post_export_reconciliation_182,
)

from reusable_blk_link_readiness_kernel_183_186 import (
    APPROVAL_ID_185,
    CANONICAL_BLK183_DECISION_PACKAGE_HASH,
    CANONICAL_BLK184_CONTRACT_PACKAGE_HASH,
    CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH,
    CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_183,
    EXACT_EXCLUDED_AUTHORITIES_184,
    EXACT_EXCLUDED_AUTHORITIES_185,
    EXACT_EXCLUDED_AUTHORITIES_186,
    EXACT_OPERATOR_DECISION_TEXT_185,
    EXACT_PROOF_OBLIGATIONS_183,
    EXACT_PROOF_OBLIGATIONS_184,
    EXACT_PROOF_OBLIGATIONS_185,
    EXACT_PROOF_OBLIGATIONS_186,
    RUN_ID_CONSUMED_185,
    SIDE_EFFECT_FLAGS_183,
    SIDE_EFFECT_FLAGS_184,
    SIDE_EFFECT_FLAGS_185,
    SIDE_EFFECT_FLAGS_186,
    build_reusable_blk_link_readiness_decision_183,
    build_reusable_blk_link_readiness_kernel_contract_184,
    build_reusable_blk_link_readiness_kernel_dry_run_185,
    build_reusable_blk_link_readiness_kernel_reconciliation_186,
    valid_reusable_blk_link_readiness_decision_183,
    valid_reusable_blk_link_readiness_kernel_contract_184,
    valid_reusable_blk_link_readiness_kernel_dry_run_185,
    valid_reusable_blk_link_readiness_kernel_reconciliation_186,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "reusable_blk_link_readiness_kernel_183_186.py"


def valid_182_reconciliation_package():
    export181 = valid_181_export_package()
    context182 = valid_rtm_blk_link_followup_post_export_reconciliation_182(export181)
    return build_rtm_blk_link_followup_post_export_reconciliation_182(export181, context182)


def valid_183_decision_package():
    reconciliation182 = valid_182_reconciliation_package()
    decision183 = valid_reusable_blk_link_readiness_decision_183(reconciliation182)
    return build_reusable_blk_link_readiness_decision_183(reconciliation182, decision183)


def valid_184_contract_package():
    decision183 = valid_183_decision_package()
    contract184 = valid_reusable_blk_link_readiness_kernel_contract_184(decision183)
    return build_reusable_blk_link_readiness_kernel_contract_184(decision183, contract184)


def valid_185_dry_run_package():
    contract184 = valid_184_contract_package()
    dryrun185 = valid_reusable_blk_link_readiness_kernel_dry_run_185(contract184)
    return build_reusable_blk_link_readiness_kernel_dry_run_185(contract184, dryrun185)


class ReusableBlkLinkReadinessKernel183186Test(unittest.TestCase):
    def test_183_selects_reusable_kernel_path_without_granting_authority(self):
        reconciliation182 = valid_182_reconciliation_package()
        decision183 = valid_reusable_blk_link_readiness_decision_183(reconciliation182)

        package = build_reusable_blk_link_readiness_decision_183(reconciliation182, decision183)

        self.assertEqual(package["upstream_export_reconciliation_package_hash"], CANONICAL_BLK182_RECONCILIATION_PACKAGE_HASH)
        self.assertTrue(package["reusable_kernel_path_selected"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["production_blk_link_authority_granted"])
        self.assertFalse(package["reusable_production_blk_link_authority_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_183)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_183)
        for flag in SIDE_EFFECT_FLAGS_183:
            self.assertIs(package[flag], flag == "reusable_kernel_path_selected", flag)
        self.assertEqual(package["decision_package_hash"], CANONICAL_BLK183_DECISION_PACKAGE_HASH)
        self.assertEqual(package["decision_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "decision_package_hash"}))

    def test_184_emits_reusable_contract_not_reusable_authority(self):
        decision183 = valid_183_decision_package()
        contract184 = valid_reusable_blk_link_readiness_kernel_contract_184(decision183)

        package = build_reusable_blk_link_readiness_kernel_contract_184(decision183, contract184)

        self.assertEqual(package["upstream_decision_package_hash"], CANONICAL_BLK183_DECISION_PACKAGE_HASH)
        self.assertTrue(package["reusable_kernel_contract_emitted"])
        self.assertEqual(package["contract"]["contract_mode"], "REUSABLE_MECHANISM_PER_RUN_EXACT_APPROVAL_REQUIRED")
        self.assertIn("exact_approval_id", package["contract"]["required_per_run_fields"])
        self.assertIn("exact_run_id", package["contract"]["required_per_run_fields"])
        self.assertFalse(package["contract"]["allows_reusable_authority"])
        self.assertFalse(package["contract"]["allows_protected_body_text"])
        self.assertFalse(package["contract"]["allows_target_source_git_mutation"])
        self.assertEqual(package["contract_hash"], _canonical_hash(package["contract"]))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_184)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_184)
        for flag in SIDE_EFFECT_FLAGS_184:
            self.assertIs(package[flag], flag == "reusable_kernel_contract_emitted", flag)
        self.assertEqual(package["contract_package_hash"], CANONICAL_BLK184_CONTRACT_PACKAGE_HASH)

    def test_185_consumes_exact_per_run_approval_in_dry_run_without_live_production_execution(self):
        contract184 = valid_184_contract_package()
        dryrun185 = valid_reusable_blk_link_readiness_kernel_dry_run_185(contract184)

        package = build_reusable_blk_link_readiness_kernel_dry_run_185(contract184, dryrun185)

        self.assertEqual(package["upstream_contract_package_hash"], CANONICAL_BLK184_CONTRACT_PACKAGE_HASH)
        self.assertEqual(package["approval_id"], APPROVAL_ID_185)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_185)
        self.assertEqual(package["operator_decision_text_raw"], EXACT_OPERATOR_DECISION_TEXT_185)
        self.assertTrue(package["per_run_exact_approval_captured"])
        self.assertTrue(package["one_run_id_consumed_in_dry_run_evidence"])
        self.assertTrue(package["readiness_kernel_dry_run_evaluated"])
        self.assertEqual(package["readiness_kernel_result"], "READY_FOR_ONE_EXACT_PRODUCTION_WRAPPER_REQUEST_NOT_GRANTED")
        self.assertFalse(package["production_blk_link_live_execution_performed"])
        self.assertFalse(package["reusable_production_blk_link_authority_granted"])
        self.assertFalse(package["protected_body_reads"])
        self.assertFalse(package["target_source_git_mutation_performed"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_185)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_185)
        true_flags = {"per_run_exact_approval_captured", "one_run_id_consumed_in_dry_run_evidence", "readiness_kernel_dry_run_evaluated"}
        for flag in SIDE_EFFECT_FLAGS_185:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertEqual(package["dry_run_package_hash"], CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH)

    def test_186_reconciles_dry_run_and_names_one_exact_production_wrapper_request_without_granting_it(self):
        dryrun185 = valid_185_dry_run_package()
        context186 = valid_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185)

        package = build_reusable_blk_link_readiness_kernel_reconciliation_186(dryrun185, context186)

        self.assertEqual(package["upstream_dry_run_package_hash"], CANONICAL_BLK185_DRY_RUN_PACKAGE_HASH)
        self.assertTrue(package["clean_readiness_kernel_dry_run_reconciled"])
        self.assertEqual(package["recommended_next_frontier"], "NEXT_FRONTIER_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_REQUEST_NOT_GRANTED")
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["observed_failure_requires_hardening"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_186)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_186)
        for flag in SIDE_EFFECT_FLAGS_186:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK186_RECONCILIATION_PACKAGE_HASH)

    def test_kernel_rejects_rehashed_upstream_retargeting_laundering_and_false_side_effects(self):
        reconciliation182 = valid_182_reconciliation_package()
        forged182 = copy.deepcopy(reconciliation182)
        forged182["next_frontier_granted"] = True
        forged182["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged182.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-182 reconciliation package hash mismatch|next_frontier_granted"):
            build_reusable_blk_link_readiness_decision_183(forged182, valid_reusable_blk_link_readiness_decision_183(forged182))

        decision183 = valid_183_decision_package()
        contract184 = valid_reusable_blk_link_readiness_kernel_contract_184(decision183)
        bad_contracts = [
            ({"operator_identity": "discord:684235178083745819 reusableProductionBlkLinkAuthorityGranted"}, "authority-laundering text|operator_identity must match"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_184) + [sorted(EXACT_EXCLUDED_AUTHORITIES_184)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"contract_notes": "safe docs%252Frequirements%252Factive%252FREQ-001.md"}, "authority-laundering text|protected-body path"),
            ({"reusable_production_blk_link_authority_granted": True}, "reusable_production_blk_link_authority_granted must remain false"),
        ]
        for patch, message in bad_contracts:
            candidate = copy.deepcopy(contract184)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_reusable_blk_link_readiness_kernel_contract_184(decision183, candidate)

        contract184_package = valid_184_contract_package()
        dryrun185 = valid_reusable_blk_link_readiness_kernel_dry_run_185(contract184_package)
        for patch, message in [
            ({"operator_decision_text_raw": EXACT_OPERATOR_DECISION_TEXT_185 + " plus reusable production authority"}, "operator_decision_text_raw must be"),
            ({"requested_at": "2099-05-16T23:31:00+10:00"}, "approval request must be within approval decision window"),
            ({"runtime_notes": "RTMGeneration approved and coverageTruthEstablished"}, "authority-laundering text"),
            ({"production_blk_link_live_execution_performed": True}, "production_blk_link_live_execution_performed must remain false"),
        ]:
            candidate = copy.deepcopy(dryrun185)
            candidate.update(patch)
            with self.subTest(dryrun_patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_reusable_blk_link_readiness_kernel_dry_run_185(contract184_package, candidate)

    def test_hash_binding_and_defensive_copies_prevent_alias_mutation(self):
        contract184 = valid_184_contract_package()
        dryrun185 = valid_reusable_blk_link_readiness_kernel_dry_run_185(contract184)
        package = build_reusable_blk_link_readiness_kernel_dry_run_185(contract184, dryrun185)
        alt = valid_reusable_blk_link_readiness_kernel_dry_run_185(
            contract184,
            requested_at="2099-05-16T23:12:00+10:00",
            expires_at="2099-05-16T23:24:00+10:00",
        )
        alt_package = build_reusable_blk_link_readiness_kernel_dry_run_185(contract184, alt)

        self.assertNotEqual(package["dry_run_request_hash"], alt_package["dry_run_request_hash"])
        self.assertNotEqual(package["dry_run_package_hash"], alt_package["dry_run_package_hash"])
        dryrun185["operator_attestation"]["protected_body_reads_excluded"] = "mutated"
        contract184["contract"]["required_per_run_fields"].append("mutated")
        self.assertIs(package["operator_attestation"]["protected_body_reads_excluded"], True)
        self.assertNotIn("mutated", package["contract"]["required_per_run_fields"])

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
