import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_execution_record import build_production_blk_link_rtm_trace_closure_execution_record
from test_production_blk_link_rtm_trace_closure_execution_record import (
    valid_blk134_approval_package,
    valid_execution_request,
)

from production_blk_link_rtm_trace_closure_post_execution_reconciliation import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_FRONTIER,
    RECONCILIATION_PACKAGE_ID,
    RECONCILIATION_SCOPE,
    RECONCILIATION_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_production_blk_link_rtm_trace_closure_post_execution_reconciliation,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "production_blk_link_rtm_trace_closure_post_execution_reconciliation.py"


def valid_blk135_execution_package():
    approval = valid_blk134_approval_package()
    request = valid_execution_request(approval)
    return build_production_blk_link_rtm_trace_closure_execution_record(approval, request)


def valid_reconciliation_context(execution_package=None, **overrides):
    if execution_package is None:
        execution_package = valid_blk135_execution_package()
    context = {
        "reconciliation_package_id": RECONCILIATION_PACKAGE_ID,
        "operator_identity": execution_package["operator_identity"],
        "reconciliation_scope": RECONCILIATION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_execution_package_id": execution_package["execution_package_id"],
        "upstream_execution_package_hash": execution_package["execution_package_hash"],
        "upstream_execution_record_id": execution_package["execution_record_id"],
        "upstream_execution_record_hash": execution_package["execution_record_hash"],
        "run_id_consumed": execution_package["run_id_consumed"],
        "approval_capture_package_id": execution_package["approval_capture_package_id"],
        "approval_capture_package_hash": execution_package["approval_capture_package_hash"],
        "beo_id": execution_package["beo_id"],
        "beb_id": execution_package["beb_id"],
        "exact_trace_identities": list(execution_package["exact_trace_identities"]),
        "reconciled_at": "2099-05-15T12:45:00+10:00",
        "stale": False,
        "replayed": False,
        "operator_attestation": {
            "exact_blk135_execution_package_reviewed": True,
            "roadmap_vocabulary_reconciled": True,
            "current_state_index_reconciled": True,
            "runbook_vocabulary_reconciled": True,
            "record_only_trace_closure_preserved": True,
            "no_reusable_blk_link_authority_claim": True,
            "rtm_generation_not_authorized": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
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
    package["execution_record"]["execution_record_hash"] = _canonical_hash(
        {key: value for key, value in package["execution_record"].items() if key != "execution_record_hash"}
    )
    package["execution_record_hash"] = package["execution_record"]["execution_record_hash"]
    package["execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "execution_package_hash"}
    )
    return package


class ProductionBlkLinkRtmTraceClosurePostExecutionReconciliationTest(unittest.TestCase):
    def test_reconciles_exact_blk135_record_only_evidence_without_new_authority(self):
        execution = valid_blk135_execution_package()
        context = valid_reconciliation_context(execution)

        package = build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, context)

        self.assertEqual(package["reconciliation_status"], RECONCILIATION_STATUS)
        self.assertEqual(package["reconciliation_package_id"], RECONCILIATION_PACKAGE_ID)
        self.assertEqual(package["reconciliation_scope"], RECONCILIATION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_execution_package_id"], "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-EXECUTION-135-001")
        self.assertEqual(
            package["upstream_execution_package_hash"],
            "sha256:4aeabf039037c8bc2f4ff61e271127df7f48698cd299a0901b88cc757f7d725a",
        )
        self.assertEqual(package["upstream_execution_record_id"], "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-135-001")
        self.assertEqual(
            package["upstream_execution_record_hash"],
            "sha256:d001e2dde10027884e071627d7ea8d572b99991a45f32612f1b906acfda161d8",
        )
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER)
        self.assertTrue(package["current_state_index_reconciled"])
        self.assertTrue(package["roadmap_reconciled"])
        self.assertTrue(package["runbook_vocabulary_reconciled"])
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertRegex(package["reconciliation_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            package["reconciliation_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "reconciliation_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_wrong_blk135_execution_package(self):
        execution = valid_blk135_execution_package()
        context = valid_reconciliation_context(execution)

        forged = copy.deepcopy(execution)
        forged["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-135 package"):
            build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(forged, context)

        forged = copy.deepcopy(execution)
        forged["execution_record_id"] = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-135-999"
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-135 execution package"):
            build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(forged, valid_reconciliation_context(forged))

        forged = copy.deepcopy(execution)
        forged["rtm_generated"] = True
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-135 execution package"):
            build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(forged, valid_reconciliation_context(forged))

    def test_rejects_bad_scope_retargeting_sets_unicode_ids_stale_replay_and_side_effects(self):
        execution = valid_blk135_execution_package()
        base_context = valid_reconciliation_context(execution)
        cases = [
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-１３６-００１"}, "reconciliation_package_id must be"),
            ({"selected_frontier": "reusableProductionBlkLinkAuthority"}, "selected_frontier must be|authority-laundering text"),
            ({"reconciliation_scope": "POST_EXECUTION_RECONCILIATION_AND_RTM_GENERATION"}, "reconciliation_scope must be|authority-laundering text"),
            ({"upstream_execution_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-EXECUTION-135-999"}, "upstream_execution_package_id must match"),
            ({"upstream_execution_package_hash": "sha256:" + "0" * 64}, "upstream_execution_package_hash must match"),
            ({"run_id_consumed": "RUN-BLK-SYSTEM-１３５-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"}, "run_id_consumed must be"),
            ({"exact_trace_identities": ["REQ:REQ-１３６:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"stale": True}, "reconciliation context must not be stale"),
            ({"replayed": True}, "reconciliation context must not be replayed"),
            ({"reconciled_at": "2000-01-01T00:00:00+10:00"}, "reconciliation context must not be calendar-stale"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            context = copy.deepcopy(base_context)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, context)

        for boolean_key in SIDE_EFFECT_FLAGS:
            context = copy.deepcopy(base_context)
            context[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, context)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        execution = valid_blk135_execution_package()
        base_context = valid_reconciliation_context(execution)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-ActiveVaultHashComparison"}, "authority-laundering text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-The%20system%20shall"}, "protected body text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-EXECUTION-RECONCILIATION-136-coverageTruthEstablished"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base_context["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            context = copy.deepcopy(base_context)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, context)

    def test_reconciliation_context_hash_is_bound_and_returned_inputs_are_defensively_copied(self):
        execution = valid_blk135_execution_package()
        base_context = valid_reconciliation_context(execution)
        alt_context = valid_reconciliation_context(execution, reconciled_at="2099-05-15T12:46:00+10:00")

        base_package = build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, base_context)
        alt_package = build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, alt_context)

        self.assertEqual(base_package["reconciliation_context_hash"], _canonical_hash(base_context))
        self.assertEqual(alt_package["reconciliation_context_hash"], _canonical_hash(alt_context))
        self.assertNotEqual(base_package["reconciliation_context_hash"], alt_package["reconciliation_context_hash"])
        self.assertNotEqual(base_package["reconciliation_package_hash"], alt_package["reconciliation_package_hash"])

        base_context["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        execution["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base_context["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

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
