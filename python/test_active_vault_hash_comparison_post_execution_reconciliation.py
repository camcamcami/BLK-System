import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_active_vault_hash_comparison_execution_record import (
    metadata_records_from_approval,
    valid_blk139_approval_package,
    valid_execution_request,
)
from active_vault_hash_comparison_execution_record import build_active_vault_hash_comparison_execution_record

from active_vault_hash_comparison_post_execution_reconciliation import (
    CLEAN_RECONCILIATION_RESULT,
    MISMATCH_RECONCILIATION_RESULT,
    NEXT_FRONTIER_CLEAN,
    NEXT_FRONTIER_MISMATCH,
    RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_SCOPE,
    RECONCILIATION_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    build_active_vault_hash_comparison_post_execution_reconciliation,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "active_vault_hash_comparison_post_execution_reconciliation.py"


def valid_blk140_execution_package(mismatch=False):
    approval = valid_blk139_approval_package()
    records = metadata_records_from_approval(approval)
    if mismatch:
        records = metadata_records_from_approval(approval, version_hash="sha256:" + "f" * 64)
    request = valid_execution_request(approval, active_metadata_records=records)
    return build_active_vault_hash_comparison_execution_record(approval, request)


def valid_reconciliation_context(execution=None, **overrides):
    if execution is None:
        execution = valid_blk140_execution_package()
    context = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": execution["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_comparison_record_id": execution["comparison_record_id"],
        "upstream_comparison_record_hash": execution["comparison_record_hash"],
        "upstream_approval_capture_package_id": execution["approval_capture_package_id"],
        "upstream_approval_capture_package_hash": execution["approval_capture_package_hash"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(execution["exact_trace_identities"]),
        "metadata_hashes_match_observed": execution["metadata_hashes_match"],
        "reconciled_at": "2099-05-15T13:40:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk140_execution_reviewed": True,
            "comparison_record_hash_verified": True,
            "reconciliation_only_not_authority_request": True,
            "metadata_match_or_mismatch_interpreted_without_drift_decision": True,
            "no_active_vault_filesystem_read": True,
            "no_protected_body_reads": True,
            "no_protected_body_copy_parse_hash_scan": True,
            "no_rtm_generation": True,
            "no_drift_rejection_or_authoritative_drift_decision": True,
            "no_coverage_truth": True,
            "no_reusable_blk_link_authority": True,
            "no_beb_dispatch_or_beo_closeout": True,
            "no_signer_storage_ledger_side_effects": True,
            "no_target_source_git_mutation": True,
            "no_blk_pipe_blk_test_codex_tooling": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def rehash_execution_package(package):
    package["comparison_record"]["comparison_record_hash"] = _canonical_hash(
        {key: value for key, value in package["comparison_record"].items() if key != "comparison_record_hash"}
    )
    package["comparison_record_hash"] = package["comparison_record"]["comparison_record_hash"]
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class ActiveVaultHashComparisonPostExecutionReconciliationTest(unittest.TestCase):
    def test_clean_blk140_comparison_reconciles_to_request_only_rtm_generation_frontier(self):
        execution = valid_blk140_execution_package()
        context = valid_reconciliation_context(execution)

        package = build_active_vault_hash_comparison_post_execution_reconciliation(execution, context)

        self.assertEqual(package["reconciliation_status"], RECONCILIATION_STATUS)
        self.assertEqual(package["reconciliation_package_id"], RECONCILIATION_PACKAGE_ID)
        self.assertEqual(package["reconciliation_scope"], RECONCILIATION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_execution_package_id"], execution["execution_package_id"])
        self.assertEqual(package["upstream_execution_package_hash"], execution["execution_package_hash"])
        self.assertEqual(package["upstream_comparison_record_hash"], execution["comparison_record_hash"])
        self.assertTrue(package["metadata_hashes_match"])
        self.assertEqual(package["reconciliation_result"], CLEAN_RECONCILIATION_RESULT)
        self.assertEqual(package["recommended_next_frontier"], NEXT_FRONTIER_CLEAN)
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["rtm_generation_authorized"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["reconciliation_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"}))

    def test_mismatch_blk140_comparison_reconciles_to_remediation_decision_not_drift_rejection(self):
        execution = valid_blk140_execution_package(mismatch=True)
        context = valid_reconciliation_context(execution)

        package = build_active_vault_hash_comparison_post_execution_reconciliation(execution, context)

        self.assertFalse(package["metadata_hashes_match"])
        self.assertEqual(package["reconciliation_result"], MISMATCH_RECONCILIATION_RESULT)
        self.assertEqual(package["recommended_next_frontier"], NEXT_FRONTIER_MISMATCH)
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["drift_decision_made"])
        self.assertFalse(package["rtm_drift_rejection_authorized"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertEqual(package["mismatch_count"], 1)
        self.assertEqual(package["mismatches"][0]["id"], "REQ-001")

    def test_rejects_forged_wrong_or_stale_execution_package_and_context(self):
        execution = valid_blk140_execution_package()
        context = valid_reconciliation_context(execution)

        forged = copy.deepcopy(execution)
        forged["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-140 package"):
            build_active_vault_hash_comparison_post_execution_reconciliation(forged, context)

        forged = copy.deepcopy(execution)
        forged["execution_package_id"] = "ACTIVE-VAULT-HASH-COMPARISON-EXECUTION-１４１-001"
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-140 execution package required"):
            build_active_vault_hash_comparison_post_execution_reconciliation(forged, valid_reconciliation_context(forged))

        for patch, message in [
            ({"upstream_execution_package_hash": "sha256:" + "0" * 64}, "upstream_execution_package_hash must match"),
            ({"metadata_hashes_match_observed": False}, "metadata_hashes_match_observed must match"),
            ({"expired": True}, "reconciliation context must not be expired"),
            ({"replayed": True}, "reconciliation context must not be replayed"),
            ({"stale": True}, "reconciliation context must not be stale"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"drift_decision_made": True}, "drift_decision_made must remain false"),
        ]:
            candidate = copy.deepcopy(context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_post_execution_reconciliation(execution, candidate)

    def test_rejects_authority_laundering_protected_paths_and_bad_exact_sets(self):
        execution = valid_blk140_execution_package()
        context = valid_reconciliation_context(execution)
        cases = [
            ({"reconciliation_package_id": "ACTIVE-VAULT-HASH-COMPARISON-RECONCILIATION-141-docs%2525252Frequirements%2525252Factive"}, "protected body text"),
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"selected_frontier": "activeVaultHashComparisonReconciliationAndDriftRejection"}, "selected_frontier must match|authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": context["operator_attestation"] | {"publishBEO": True}}, "unexpected field"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_post_execution_reconciliation(execution, candidate)

    def test_returned_package_is_defensively_copied_and_hash_bound(self):
        execution = valid_blk140_execution_package()
        context = valid_reconciliation_context(execution)
        package = build_active_vault_hash_comparison_post_execution_reconciliation(execution, context)

        context["operator_attestation"]["no_coverage_truth"] = "mutated"
        execution["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)
        execution["comparison_record"]["mismatches"].append({"id": "REQ-999"})

        self.assertIs(package["operator_attestation"]["no_coverage_truth"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "9" * 64, package["exact_trace_identities"])
        self.assertEqual(package["mismatch_count"], 0)

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
