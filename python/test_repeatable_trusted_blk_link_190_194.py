import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_single_production_blk_link_wrapper_run_187_189 import valid_188_execution_package
from single_production_blk_link_wrapper_run_187_189 import (
    CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH,
    build_single_production_blk_link_wrapper_reconciliation_189,
    valid_single_production_blk_link_wrapper_reconciliation_189,
)

from repeatable_trusted_blk_link_190_194 import (
    CANONICAL_BLK190_REVIEW_PACKAGE_HASH,
    CANONICAL_BLK191_CONTRACT_PACKAGE_HASH,
    CANONICAL_BLK192_LEDGER_PACKAGE_HASH,
    CANONICAL_BLK193_REPEAT_RUNS_PACKAGE_HASH,
    CANONICAL_BLK194_RECONCILIATION_PACKAGE_HASH,
    EXACT_EXCLUDED_AUTHORITIES_190,
    EXACT_EXCLUDED_AUTHORITIES_191,
    EXACT_EXCLUDED_AUTHORITIES_192,
    EXACT_EXCLUDED_AUTHORITIES_193,
    EXACT_EXCLUDED_AUTHORITIES_194,
    EXACT_PROOF_OBLIGATIONS_190,
    EXACT_PROOF_OBLIGATIONS_191,
    EXACT_PROOF_OBLIGATIONS_192,
    EXACT_PROOF_OBLIGATIONS_193,
    EXACT_PROOF_OBLIGATIONS_194,
    REPEATABLE_TRUSTED_BLK_LINK_NEXT_FRONTIER_194,
    SIDE_EFFECT_FLAGS_190,
    SIDE_EFFECT_FLAGS_191,
    SIDE_EFFECT_FLAGS_192,
    SIDE_EFFECT_FLAGS_193,
    SIDE_EFFECT_FLAGS_194,
    _operator_text,
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

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "repeatable_trusted_blk_link_190_194.py"


def valid_189_reconciliation_package():
    execution188 = valid_188_execution_package()
    context189 = valid_single_production_blk_link_wrapper_reconciliation_189(execution188)
    return build_single_production_blk_link_wrapper_reconciliation_189(execution188, context189)


def valid_190_review_package():
    reconciliation189 = valid_189_reconciliation_package()
    review190 = valid_repeatable_trusted_blk_link_post_run_review_190(reconciliation189)
    return build_repeatable_trusted_blk_link_post_run_review_190(reconciliation189, review190)


def valid_191_contract_package():
    review190 = valid_190_review_package()
    contract191 = valid_repeatable_trusted_blk_link_contract_191(review190)
    return build_repeatable_trusted_blk_link_contract_191(review190, contract191)


def valid_192_ledger_package():
    contract191 = valid_191_contract_package()
    ledger192 = valid_repeatable_trusted_blk_link_ledger_192(contract191)
    return build_repeatable_trusted_blk_link_ledger_192(contract191, ledger192)


def valid_193_repeat_runs_package():
    ledger192 = valid_192_ledger_package()
    repeat193 = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192)
    return build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, repeat193)


class RepeatableTrustedBlkLink190194Test(unittest.TestCase):
    def test_190_reviews_single_run_and_selects_repeatable_trusted_path_without_granting_blanket_authority(self):
        reconciliation189 = valid_189_reconciliation_package()
        review190 = valid_repeatable_trusted_blk_link_post_run_review_190(reconciliation189)

        package = build_repeatable_trusted_blk_link_post_run_review_190(reconciliation189, review190)

        self.assertEqual(package["upstream_reconciliation_package_hash"], CANONICAL_BLK189_RECONCILIATION_PACKAGE_HASH)
        self.assertTrue(package["single_run_reviewed_clean"])
        self.assertTrue(package["repeatable_trusted_path_selected"])
        self.assertFalse(package["blanket_production_blk_link_authority_granted"])
        self.assertFalse(package["reusable_run_id_authority_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_190)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_190)
        for flag in SIDE_EFFECT_FLAGS_190:
            self.assertIs(package[flag], flag in {"single_run_reviewed_clean", "repeatable_trusted_path_selected"}, flag)
        self.assertEqual(package["review_package_hash"], CANONICAL_BLK190_REVIEW_PACKAGE_HASH)
        self.assertEqual(package["review_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "review_package_hash"}))

    def test_191_emits_repeatable_trusted_contract_with_per_run_exact_approval_and_trust_rules(self):
        review190 = valid_190_review_package()
        contract191 = valid_repeatable_trusted_blk_link_contract_191(review190)

        package = build_repeatable_trusted_blk_link_contract_191(review190, contract191)

        self.assertEqual(package["upstream_review_package_hash"], CANONICAL_BLK190_REVIEW_PACKAGE_HASH)
        self.assertTrue(package["repeatable_trusted_contract_emitted"])
        self.assertEqual(package["contract"]["contract_mode"], "REPEATABLE_TRUSTED_BLK_LINK_PER_RUN_EXACT_APPROVAL")
        self.assertTrue(package["contract"]["allows_repeatable_runs_with_exact_approval"])
        self.assertFalse(package["contract"]["allows_blanket_authority"])
        self.assertIn("exact_approval_id", package["contract"]["required_per_run_fields"])
        self.assertIn("ledger_previous_hash", package["contract"]["required_per_run_fields"])
        self.assertIn("unique_run_id_not_previously_consumed", package["contract"]["trust_rules"])
        self.assertIn("canonical_upstream_hash_binding", package["contract"]["trust_rules"])
        self.assertEqual(package["contract_hash"], _canonical_hash(package["contract"]))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_191)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_191)
        for flag in SIDE_EFFECT_FLAGS_191:
            self.assertIs(package[flag], flag == "repeatable_trusted_contract_emitted", flag)
        self.assertEqual(package["contract_package_hash"], CANONICAL_BLK191_CONTRACT_PACKAGE_HASH)

    def test_192_initializes_caller_supplied_trust_ledger_without_filesystem_mutation_or_global_replay_claim(self):
        contract191 = valid_191_contract_package()
        ledger192 = valid_repeatable_trusted_blk_link_ledger_192(contract191)

        package = build_repeatable_trusted_blk_link_ledger_192(contract191, ledger192)

        self.assertEqual(package["upstream_contract_package_hash"], CANONICAL_BLK191_CONTRACT_PACKAGE_HASH)
        self.assertTrue(package["caller_supplied_trust_ledger_initialized"])
        self.assertEqual(package["ledger"]["used_run_ids"], [])
        self.assertEqual(package["ledger"]["ledger_entries"], [])
        self.assertEqual(package["ledger"]["current_ledger_hash"], package["ledger"]["genesis_ledger_hash"])
        self.assertFalse(package["global_replay_ledger_claimed"])
        self.assertFalse(package["filesystem_ledger_written"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_192)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_192)
        for flag in SIDE_EFFECT_FLAGS_192:
            self.assertIs(package[flag], flag == "caller_supplied_trust_ledger_initialized", flag)
        self.assertEqual(package["ledger_package_hash"], CANONICAL_BLK192_LEDGER_PACKAGE_HASH)

    def test_193_records_three_exact_repeat_runs_with_unique_ids_hash_chain_and_no_adjacent_authority(self):
        ledger192 = valid_192_ledger_package()
        repeat193 = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192)

        package = build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, repeat193)

        self.assertEqual(package["upstream_ledger_package_hash"], CANONICAL_BLK192_LEDGER_PACKAGE_HASH)
        self.assertTrue(package["repeatable_trusted_runs_executed"])
        self.assertEqual(package["repeat_run_count"], 3)
        self.assertEqual(package["trusted_repeatability_result"], "TRUSTED_REPEATABILITY_SAMPLE_3_OF_3_CLEAN")
        run_ids = [entry["run_id_consumed"] for entry in package["run_evidence"]]
        self.assertEqual(len(run_ids), len(set(run_ids)))
        previous = ledger192["ledger"]["current_ledger_hash"]
        for entry in package["run_evidence"]:
            self.assertEqual(entry["ledger_previous_hash"], previous)
            self.assertEqual(entry["entry_hash"], _canonical_hash({k: v for k, v in entry.items() if k != "entry_hash"}))
            self.assertTrue(entry["per_run_exact_approval_captured"])
            self.assertTrue(entry["production_wrapper_run_executed"])
            self.assertFalse(entry["rtm_generated"])
            self.assertFalse(entry["protected_body_reads"])
            previous = entry["entry_hash"]
        self.assertEqual(package["ledger"]["current_ledger_hash"], previous)
        self.assertFalse(package["blanket_production_blk_link_authority_granted"])
        self.assertFalse(package["reusable_rtm_generation_authorized"])
        self.assertFalse(package["target_source_git_mutation_performed"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_193)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_193)
        true_flags = {"per_run_exact_approval_captured", "repeatable_trusted_runs_executed", "production_wrapper_run_executed", "caller_supplied_ledger_advanced"}
        for flag in SIDE_EFFECT_FLAGS_193:
            self.assertIs(package[flag], flag in true_flags, flag)
        self.assertEqual(package["repeat_runs_package_hash"], CANONICAL_BLK193_REPEAT_RUNS_PACKAGE_HASH)

    def test_194_reconciles_repeatability_as_trusted_operator_use_ready_without_unbounded_authority(self):
        repeat193 = valid_193_repeat_runs_package()
        context194 = valid_repeatable_trusted_blk_link_reconciliation_194(repeat193)

        package = build_repeatable_trusted_blk_link_reconciliation_194(repeat193, context194)

        self.assertEqual(package["upstream_repeat_runs_package_hash"], CANONICAL_BLK193_REPEAT_RUNS_PACKAGE_HASH)
        self.assertTrue(package["repeatable_trusted_blk_link_reconciled_clean"])
        self.assertTrue(package["trusted_repeatable_mechanism_established"])
        self.assertEqual(package["trusted_repeatability_score"], "3/3")
        self.assertEqual(package["recommended_next_frontier"], REPEATABLE_TRUSTED_BLK_LINK_NEXT_FRONTIER_194)
        self.assertFalse(package["blanket_production_blk_link_authority_granted"])
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_194)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_194)
        for flag in SIDE_EFFECT_FLAGS_194:
            self.assertIs(package[flag], flag in {"repeatable_trusted_blk_link_reconciled_clean", "trusted_repeatable_mechanism_established"}, flag)
        self.assertEqual(package["reconciliation_package_hash"], CANONICAL_BLK194_RECONCILIATION_PACKAGE_HASH)

    def test_repeatable_ladder_rejects_rehashed_upstream_replay_laundering_and_false_side_effects(self):
        reconciliation189 = valid_189_reconciliation_package()
        forged189 = copy.deepcopy(reconciliation189)
        forged189["next_frontier_granted"] = True
        forged189["reconciliation_package_hash"] = _canonical_hash({k: v for k, v in forged189.items() if k != "reconciliation_package_hash"})
        with self.assertRaisesRegex(ValueError, "canonical BLK-189 reconciliation package hash mismatch|next_frontier_granted"):
            build_repeatable_trusted_blk_link_post_run_review_190(forged189, valid_repeatable_trusted_blk_link_post_run_review_190(forged189))

        ledger192 = valid_192_ledger_package()
        repeat193 = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192)
        for patch, message in [
            ({"operator_identity": "discord:684235178083745819 blanketProductionBlkLinkAuthorityGranted"}, "authority-laundering text|operator_identity must match"),
            ({"runtime_notes": "RTMGeneration approved and coverageTruthEstablished docs%252Frequirements%252Factive%252FREQ-001.md"}, "authority-laundering text"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_193) + [sorted(EXACT_EXCLUDED_AUTHORITIES_193)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"replayed": True}, "record must not be replayed"),
            ({"blanket_production_blk_link_authority_granted": True}, "blanket_production_blk_link_authority_granted must remain false"),
            ({"target_source_git_mutation_performed": True}, "target_source_git_mutation_performed must remain false"),
        ]:
            candidate = copy.deepcopy(repeat193)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, candidate)

        duplicate = copy.deepcopy(repeat193)
        duplicate["repeat_run_requests"][1]["run_id_to_consume"] = duplicate["repeat_run_requests"][0]["run_id_to_consume"]
        with self.assertRaisesRegex(ValueError, "run_id_to_consume must be unique and unused"):
            build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, duplicate)

        smuggled = copy.deepcopy(repeat193)
        smuggled_id = "APPROVAL-BLK-SYSTEM-193-blanketProductionBlkLinkAuthorityGranted-docs%252Frequirements%252Factive%252FREQ-001.md"
        smuggled["repeat_run_requests"][0]["approval_id"] = smuggled_id
        smuggled["repeat_run_requests"][0]["operator_decision_text_raw"] = _operator_text(
            smuggled_id,
            smuggled["repeat_run_requests"][0]["run_id_to_consume"],
            smuggled["repeat_run_requests"][0]["nonce"],
        )
        with self.assertRaisesRegex(ValueError, "authority-laundering text"):
            build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, smuggled)

        sentinel = copy.deepcopy(repeat193)
        sentinel["repeat_run_requests"][0]["ledger_previous_hash"] = "USE_CURRENT_LEDGER_HASH"
        before = copy.deepcopy(sentinel)
        with self.assertRaisesRegex(ValueError, "ledger_previous_hash must be canonical sha256|ledger_previous_hash must be exact current hash"):
            build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, sentinel)
        self.assertEqual(sentinel, before, "rejected repeat-run requests must not be mutated")

        stale_ledger = copy.deepcopy(ledger192)
        stale_ledger["ledger"]["used_run_ids"] = [repeat193["repeat_run_requests"][0]["run_id_to_consume"]]
        stale_ledger["ledger_package_hash"] = _canonical_hash({k: v for k, v in stale_ledger.items() if k != "ledger_package_hash"})
        with self.assertRaisesRegex(ValueError, "ledger_package_hash does not match submitted BLK package|canonical BLK-192 ledger package hash mismatch|upstream_ledger_package_hash must match"):
            build_repeatable_trusted_blk_link_repeat_runs_193(stale_ledger, repeat193)

    def test_hash_binding_and_defensive_copies_prevent_alias_mutation(self):
        ledger192 = valid_192_ledger_package()
        repeat193 = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192)
        original_repeat193 = copy.deepcopy(repeat193)
        package = build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, repeat193)
        alt = valid_repeatable_trusted_blk_link_repeat_runs_193(ledger192, requested_at_start="2099-05-17T01:30:00+10:00")
        alt_package = build_repeatable_trusted_blk_link_repeat_runs_193(ledger192, alt)

        self.assertNotEqual(package["repeat_runs_request_hash"], alt_package["repeat_runs_request_hash"])
        self.assertNotEqual(package["repeat_runs_package_hash"], alt_package["repeat_runs_package_hash"])
        self.assertEqual(repeat193, original_repeat193, "build must not normalize caller requests in place")
        repeat193["repeat_run_requests"][0]["operator_attestation"]["protected_body_reads_excluded"] = "mutated"
        ledger192["ledger"]["used_run_ids"].append("mutated")
        self.assertIs(package["run_evidence"][0]["operator_attestation"]["protected_body_reads_excluded"], True)
        self.assertNotIn("mutated", package["ledger"]["used_run_ids"])

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
