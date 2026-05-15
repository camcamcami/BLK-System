import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_metadata_bound_rtm_generation_execution_package import (
    valid_blk142_request_package,
    valid_execution_request,
)
from metadata_bound_rtm_generation_execution_package import build_metadata_bound_rtm_generation_execution_package

from post_rtm_generation_reconciliation import (
    CLEAN_RECONCILIATION_RESULT,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_FRONTIER_CLEAN,
    RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_SCOPE,
    RECONCILIATION_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_post_rtm_generation_reconciliation,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "post_rtm_generation_reconciliation.py"


def valid_blk143_execution_package():
    request_package = valid_blk142_request_package()
    execution_request = valid_execution_request(request_package)
    return build_metadata_bound_rtm_generation_execution_package(request_package, execution_request)


def valid_reconciliation_context(execution=None, **overrides):
    if execution is None:
        execution = valid_blk143_execution_package()
    context = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": execution["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution["execution_package_id"],
        "upstream_execution_package_hash": execution["execution_package_hash"],
        "upstream_rtm_record_id": execution["rtm_record_id"],
        "upstream_rtm_record_hash": execution["rtm_record_hash"],
        "upstream_authority_request_package_id": execution["upstream_authority_request_package_id"],
        "upstream_authority_request_package_hash": execution["upstream_authority_request_package_hash"],
        "upstream_authority_request_hash": execution["upstream_authority_request_hash"],
        "approval_id": execution["approval_id"],
        "run_id_consumed": execution["run_id_consumed"],
        "beo_id": execution["beo_id"],
        "beb_id": execution["beb_id"],
        "exact_trace_identities": list(execution["exact_trace_identities"]),
        "metadata_bound_rtm_generation_observed": execution["metadata_bound_rtm_generation_executed"],
        "rtm_record_metadata_only_observed": True,
        "reconciled_at": "2099-05-15T15:00:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk143_execution_reviewed": True,
            "rtm_record_hash_verified": True,
            "reconciliation_only_not_authority_request": True,
            "metadata_bound_generation_interpreted_without_drift_decision": True,
            "record_remains_metadata_only": True,
            "no_active_vault_filesystem_read": True,
            "no_protected_body_reads": True,
            "no_protected_body_copy_parse_hash_scan": True,
            "no_additional_rtm_generation": True,
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
    package["rtm_record"]["rtm_record_hash"] = _canonical_hash(
        {key: value for key, value in package["rtm_record"].items() if key != "rtm_record_hash"}
    )
    package["rtm_record_hash"] = package["rtm_record"]["rtm_record_hash"]
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class PostRtmGenerationReconciliationTest(unittest.TestCase):
    def test_clean_blk143_rtm_generation_reconciles_to_next_decision_frontier_without_granting_authority(self):
        execution = valid_blk143_execution_package()
        context = valid_reconciliation_context(execution)

        package = build_post_rtm_generation_reconciliation(execution, context)

        self.assertEqual(package["reconciliation_status"], RECONCILIATION_STATUS)
        self.assertEqual(package["reconciliation_package_id"], RECONCILIATION_PACKAGE_ID)
        self.assertEqual(package["reconciliation_scope"], RECONCILIATION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_execution_package_id"], execution["execution_package_id"])
        self.assertEqual(package["upstream_execution_package_hash"], execution["execution_package_hash"])
        self.assertEqual(package["upstream_rtm_record_id"], execution["rtm_record_id"])
        self.assertEqual(package["upstream_rtm_record_hash"], execution["rtm_record_hash"])
        self.assertEqual(package["approval_id"], execution["approval_id"])
        self.assertEqual(package["run_id_consumed"], execution["run_id_consumed"])
        self.assertTrue(package["metadata_bound_rtm_generation_reconciled"])
        self.assertTrue(package["rtm_record_metadata_only"])
        self.assertEqual(package["reconciliation_result"], CLEAN_RECONCILIATION_RESULT)
        self.assertEqual(package["recommended_next_frontier"], NEXT_FRONTIER_CLEAN)
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["rtm_drift_rejection_authorized"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["reusable_blk_link_authority_granted"])
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["reconciliation_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "reconciliation_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_non_metadata_only_blk143_execution_package(self):
        execution = valid_blk143_execution_package()
        context = valid_reconciliation_context(execution)

        forged = copy.deepcopy(execution)
        forged["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-143 package"):
            build_post_rtm_generation_reconciliation(forged, context)

        forged = copy.deepcopy(execution)
        forged["execution_package_id"] = "RTM-GENERATION-EXECUTION-１４４-001"
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-143 execution package required"):
            build_post_rtm_generation_reconciliation(forged, valid_reconciliation_context(forged))

        forged = copy.deepcopy(execution)
        forged["rtm_record"]["rtm_record_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "rtm_record_hash does not match submitted BLK-143 RTM record"):
            build_post_rtm_generation_reconciliation(forged, context)

        forged = copy.deepcopy(execution)
        forged["rtm_record"]["protected_body_reads"] = True
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-143 execution package required|rtm_record.protected_body_reads must remain false"):
            build_post_rtm_generation_reconciliation(forged, valid_reconciliation_context(forged))

    def test_rejects_context_retargeting_replay_expiry_side_effects_and_bad_exact_sets(self):
        execution = valid_blk143_execution_package()
        base_context = valid_reconciliation_context(execution)
        cases = [
            ({"upstream_execution_package_hash": "sha256:" + "0" * 64}, "upstream_execution_package_hash must match"),
            ({"upstream_rtm_record_hash": "sha256:" + "1" * 64}, "upstream_rtm_record_hash must match"),
            ({"metadata_bound_rtm_generation_observed": False}, "metadata_bound_rtm_generation_observed must match"),
            ({"rtm_record_metadata_only_observed": False}, "rtm_record_metadata_only_observed must be true"),
            ({"expired": True}, "reconciliation context must not be expired"),
            ({"replayed": True}, "reconciliation context must not be replayed"),
            ({"stale": True}, "reconciliation context must not be stale"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(base_context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_post_rtm_generation_reconciliation(execution, candidate)

    def test_rejects_authority_laundering_protected_paths_tooling_and_extra_fields(self):
        execution = valid_blk143_execution_package()
        context = valid_reconciliation_context(execution)
        cases = [
            ({"reconciliation_package_id": "POST-RTM-GENERATION-RECONCILIATION-144-docs%2525252Frequirements%2525252Factive"}, "protected body text"),
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"selected_frontier": "postRtmGenerationReconciliationAndDriftRejection"}, "selected_frontier must match|authority-laundering text"),
            ({"reconciliation_scope": "RECONCILE_AND_ESTABLISH_COVERAGE_TRUTH"}, "reconciliation_scope must match|authority-laundering text"),
            ({"curlWrapper": False}, "unexpected field"),
            ({"operator_attestation": context["operator_attestation"] | {"publishBEO": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            candidate = copy.deepcopy(context)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_post_rtm_generation_reconciliation(execution, candidate)

    def test_reconciliation_context_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        execution = valid_blk143_execution_package()
        base_context = valid_reconciliation_context(execution)
        alt_context = valid_reconciliation_context(execution, reconciled_at="2099-05-15T15:10:00+10:00")

        base_package = build_post_rtm_generation_reconciliation(execution, base_context)
        alt_package = build_post_rtm_generation_reconciliation(execution, alt_context)

        self.assertEqual(base_package["reconciliation_context_hash"], _canonical_hash(base_context))
        self.assertEqual(alt_package["reconciliation_context_hash"], _canonical_hash(alt_context))
        self.assertNotEqual(base_package["reconciliation_context_hash"], alt_package["reconciliation_context_hash"])
        self.assertNotEqual(base_package["reconciliation_package_hash"], alt_package["reconciliation_package_hash"])

        base_context["operator_attestation"]["no_coverage_truth"] = "mutated"
        execution["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)
        execution["rtm_record"]["trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)
        self.assertIs(base_package["operator_attestation"]["no_coverage_truth"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "9" * 64, base_package["exact_trace_identities"])

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
