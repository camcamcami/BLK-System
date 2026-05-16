import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_decision_execution_166 import (
    build_production_blk_link_rtm_trace_closure_decision_execution_166,
    valid_production_blk_link_rtm_trace_closure_decision_execution_166,
)
from test_production_blk_link_rtm_trace_closure_decision_execution_166 import valid_blk165_request_package

from production_blk_link_rtm_trace_closure_post_run_reconciliation_167 import (
    EXACT_EXCLUDED_AUTHORITIES_167,
    EXACT_PROOF_OBLIGATIONS_167,
    NEXT_FRONTIER_167,
    RECONCILIATION_PACKAGE_ID_167,
    RECONCILIATION_SCOPE_167,
    RECONCILIATION_STATUS_167,
    SELECTED_FRONTIER_167,
    SIDE_EFFECT_FLAGS_167,
    build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167,
    valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "production_blk_link_rtm_trace_closure_post_run_reconciliation_167.py"


def valid_blk166_decision_execution_package():
    request165 = valid_blk165_request_package()
    request166 = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)
    return build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, request166)


def rehash_blk166_package(package):
    package["execution_record"]["execution_record_hash"] = _canonical_hash(
        {key: value for key, value in package["execution_record"].items() if key != "execution_record_hash"}
    )
    package["execution_record_hash"] = package["execution_record"]["execution_record_hash"]
    package["decision_execution_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "decision_execution_package_hash"}
    )
    return package


class ProductionBlkLinkRtmTraceClosurePostRunReconciliation167Test(unittest.TestCase):
    def test_167_reconciles_clean_blk166_one_run_evidence_without_requiring_168(self):
        execution166 = valid_blk166_decision_execution_package()
        context = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166)

        package = build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, context)

        self.assertEqual(package["reconciliation_status"], RECONCILIATION_STATUS_167)
        self.assertEqual(package["reconciliation_package_id"], RECONCILIATION_PACKAGE_ID_167)
        self.assertEqual(package["reconciliation_scope"], RECONCILIATION_SCOPE_167)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER_167)
        self.assertEqual(package["upstream_decision_execution_package_id"], "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-DECISION-EXECUTION-166-001")
        self.assertEqual(
            package["upstream_decision_execution_package_hash"],
            "sha256:408f720d5b58a6addb5251fb3bb6142b5583a030af419e4d5cba9d85c72d6297",
        )
        self.assertEqual(package["upstream_execution_record_id"], "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-166-001")
        self.assertEqual(
            package["upstream_execution_record_hash"],
            "sha256:d1c3d267fba4d3ce144a63d54dc60057f917867eb2f27b3aad6998a9d2899889",
        )
        self.assertEqual(package["run_id_consumed"], "RUN-BLK-SYSTEM-166-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001")
        self.assertTrue(package["clean_record_only_evidence_reconciled"])
        self.assertFalse(package["observed_failure_requires_168"])
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER_167)
        self.assertEqual(package["reconciliation_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_167)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_167)
        for flag in SIDE_EFFECT_FLAGS_167:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["reconciliation_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "reconciliation_package_hash"}),
        )

    def test_167_rejects_forged_rehashed_or_side_effect_bearing_blk166_package(self):
        execution166 = valid_blk166_decision_execution_package()
        context = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166)

        forged = copy.deepcopy(execution166)
        forged["decision_execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "decision_execution_package_hash does not match submitted BLK-166 package"):
            build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(forged, context)

        forged = copy.deepcopy(execution166)
        forged["execution_record_id"] = "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-RECORD-166-999"
        rehash_blk166_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-166 decision execution package"):
            build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(
                forged, valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(forged)
            )

        forged = copy.deepcopy(execution166)
        forged["rtm_generated"] = True
        rehash_blk166_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-166 decision execution package"):
            build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(
                forged, valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(forged)
            )

    def test_167_rejects_bad_scope_retargeting_sets_stale_replay_and_side_effects(self):
        execution166 = valid_blk166_decision_execution_package()
        base = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166)
        cases = [
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-RUN-RECONCILIATION-１６７-００１"}, "reconciliation_package_id must be"),
            ({"selected_frontier": "reusableProductionBlkLinkAuthority"}, "selected_frontier must be|authority-laundering text"),
            ({"reconciliation_scope": "POST_RUN_RECONCILIATION_AND_RTM_GENERATION"}, "reconciliation_scope must be|authority-laundering text"),
            ({"upstream_decision_execution_package_hash": "sha256:" + "0" * 64}, "upstream_decision_execution_package_hash must match"),
            ({"run_id_consumed": "RUN-BLK-SYSTEM-１６６-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"}, "run_id_consumed must be"),
            ({"exact_trace_identities": ["REQ:REQ-１６７:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"stale": True}, "reconciliation context must not be stale"),
            ({"replayed": True}, "reconciliation context must not be replayed"),
            ({"observed_failure_requires_168": True}, "observed_failure_requires_168 must be false for clean BLK-167 reconciliation"),
            ({"reconciled_at": "2000-01-01T00:00:00+10:00"}, "reconciliation context must not be calendar-stale"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_167) + [sorted(EXACT_PROOF_OBLIGATIONS_167)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_167) + [sorted(EXACT_EXCLUDED_AUTHORITIES_167)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-RUN-RECONCILIATION-167-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"reconciliation_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-POST-RUN-RECONCILIATION-167-The%20system%20shall"}, "protected body text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            context = copy.deepcopy(base)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, context)

        for boolean_key in SIDE_EFFECT_FLAGS_167:
            context = copy.deepcopy(base)
            context[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, context)

    def test_167_context_hash_is_bound_and_inputs_are_defensively_copied(self):
        execution166 = valid_blk166_decision_execution_package()
        base = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166)
        alt = valid_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(
            execution166,
            reconciled_at="2099-05-16T15:49:00+10:00",
        )

        base_package = build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, base)
        alt_package = build_production_blk_link_rtm_trace_closure_post_run_reconciliation_167(execution166, alt)

        self.assertNotEqual(base_package["reconciliation_context_hash"], alt_package["reconciliation_context_hash"])
        self.assertNotEqual(base_package["reconciliation_package_hash"], alt_package["reconciliation_package_hash"])
        base["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        execution166["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

    def test_167_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
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
