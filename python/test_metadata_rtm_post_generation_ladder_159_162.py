import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from test_metadata_bound_rtm_generation_approval_execution import valid_blk157_request_package
from metadata_bound_rtm_generation_approval_execution import (
    build_metadata_bound_rtm_generation_approval_execution,
    valid_metadata_bound_rtm_generation_approval_execution_request,
)

from metadata_rtm_post_generation_ladder_159_162 import (
    EXACT_EXCLUDED_AUTHORITIES_159,
    EXACT_EXCLUDED_AUTHORITIES_160,
    EXACT_EXCLUDED_AUTHORITIES_161,
    EXACT_EXCLUDED_AUTHORITIES_162,
    EXECUTION_PACKAGE_ID_161,
    NEXT_FRONTIER_162,
    POST_EXECUTION_REVIEW_ID_162,
    RECONCILIATION_PACKAGE_ID_159,
    REQUEST_PACKAGE_ID_160,
    REQUIRED_FALSE_FLAGS,
    RUN_ID_161,
    TRACE_CLOSURE_RECORD_ID_161,
    build_post_generation_reconciliation_159,
    build_post_trace_closure_review_162,
    build_trace_closure_authority_request_160,
    build_trace_closure_execution_161,
    valid_post_generation_reconciliation_context_159,
    valid_post_trace_closure_review_context_162,
    valid_trace_closure_authority_request_160,
    valid_trace_closure_execution_request_161,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_rtm_post_generation_ladder_159_162.py"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


def valid_blk158_execution_package():
    request_package = valid_blk157_request_package()
    execution_request = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)
    return build_metadata_bound_rtm_generation_approval_execution(request_package, execution_request)


def rehash(package, hash_key):
    package[hash_key] = _canonical_hash({k: v for k, v in package.items() if k != hash_key})
    return package


class MetadataRtmPostGenerationLadder159To162Test(unittest.TestCase):
    def test_159_reconciles_exact_blk158_record_without_new_authority(self):
        upstream = valid_blk158_execution_package()
        context = valid_post_generation_reconciliation_context_159(upstream)

        package = build_post_generation_reconciliation_159(upstream, context)

        self.assertEqual(package["reconciliation_package_id"], RECONCILIATION_PACKAGE_ID_159)
        self.assertEqual(package["upstream_execution_package_hash"], upstream["execution_package_hash"])
        self.assertEqual(package["upstream_rtm_record_hash"], upstream["rtm_record_hash"])
        self.assertEqual(package["reconciliation_result"], "CLEAN_METADATA_RTM_GENERATION_RECONCILED_NEXT_REQUEST_REQUIRED")
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_159)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["reconciliation_package_hash"],
            _canonical_hash({k: v for k, v in package.items() if k != "reconciliation_package_hash"}),
        )

    def test_160_requests_trace_closure_authority_without_approval_or_execution(self):
        rec159 = build_post_generation_reconciliation_159(
            valid_blk158_execution_package(),
            valid_post_generation_reconciliation_context_159(valid_blk158_execution_package()),
        )
        request = valid_trace_closure_authority_request_160(rec159)

        package = build_trace_closure_authority_request_160(rec159, request)

        self.assertEqual(package["request_package_id"], REQUEST_PACKAGE_ID_160)
        self.assertEqual(package["upstream_reconciliation_package_hash"], rec159["reconciliation_package_hash"])
        self.assertTrue(package["request_future_exact_trace_closure_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["future_run_id_consumed"])
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_160)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({k: v for k, v in package.items() if k != "request_package_hash"}),
        )

    def test_161_executes_one_bounded_metadata_trace_closure_record_after_exact_request(self):
        request160 = self._request160()
        execution_request = valid_trace_closure_execution_request_161(request160)

        package = build_trace_closure_execution_161(request160, execution_request)

        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID_161)
        self.assertEqual(package["upstream_request_package_hash"], request160["request_package_hash"])
        self.assertEqual(package["run_id_consumed"], RUN_ID_161)
        self.assertTrue(package["approval_capture_performed"])
        self.assertTrue(package["metadata_trace_closure_executed"])
        self.assertEqual(package["trace_closure_record_id"], TRACE_CLOSURE_RECORD_ID_161)
        self.assertEqual(package["trace_closure_record"]["trace_closure_record_id"], TRACE_CLOSURE_RECORD_ID_161)
        self.assertEqual(package["trace_closure_record"]["trace_identities"], request160["exact_trace_identities"])
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_161)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
            self.assertIs(package["trace_closure_record"][flag], False, flag)
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"}),
        )

    def test_162_reviews_exact_trace_closure_record_and_selects_next_frontier_without_granting_it(self):
        execution161 = self._execution161()
        context = valid_post_trace_closure_review_context_162(execution161)

        package = build_post_trace_closure_review_162(execution161, context)

        self.assertEqual(package["review_package_id"], POST_EXECUTION_REVIEW_ID_162)
        self.assertEqual(package["upstream_execution_package_hash"], execution161["execution_package_hash"])
        self.assertEqual(package["upstream_trace_closure_record_hash"], execution161["trace_closure_record_hash"])
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER_162)
        self.assertFalse(package["next_frontier_granted"])
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_162)
        for flag in REQUIRED_FALSE_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["review_package_hash"],
            _canonical_hash({k: v for k, v in package.items() if k != "review_package_hash"}),
        )

    def test_rejects_forged_upstreams_bad_hashes_side_effects_and_laundering(self):
        upstream = valid_blk158_execution_package()
        context = valid_post_generation_reconciliation_context_159(upstream)
        forged = copy.deepcopy(upstream)
        forged["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-158 package"):
            build_post_generation_reconciliation_159(forged, context)

        bad_context = copy.deepcopy(context)
        bad_context["selected_frontier"] = "PostGenerationAndDriftRejection"
        with self.assertRaisesRegex(ValueError, "authority-laundering text|selected_frontier must be"):
            build_post_generation_reconciliation_159(upstream, bad_context)

        bad_context = copy.deepcopy(context)
        bad_context["protected_body_reads"] = True
        with self.assertRaisesRegex(ValueError, "protected_body_reads must remain false"):
            build_post_generation_reconciliation_159(upstream, bad_context)

        request160 = self._request160()
        exec_req = valid_trace_closure_execution_request_161(request160)
        for patch, message in [
            ({"run_id": "RUN-BLK-SYSTEM-１６１-METADATA-TRACE-CLOSURE-001"}, "run_id must be|authority-laundering text"),
            ({"operator_approval_text_raw": "approved"}, "operator approval text must match exact BLK-SYSTEM-161 approval sentence"),
            ({"execution_package_id": "TRACE-CLOSURE-EXECUTION-161-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"execution_package_id": "TRACE-CLOSURE-EXECUTION-161-The%20system%20shall"}, "protected body text"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
        ]:
            candidate = copy.deepcopy(exec_req)
            candidate.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_trace_closure_execution_161(request160, candidate)

    def test_docs_and_state_advance_to_162_without_bloat_or_adjacent_authority(self):
        roadmap = BLK077.read_text()
        index = BLK079.read_text()
        for text in (roadmap, index):
            self.assertIn("BLK_SYSTEM_167_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_RUN_RECONCILED_CLEAN", text)
            self.assertIn("BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY", text)
            self.assertTrue(
                "NEXT_FRONTIER_METADATA_BOUND_DRIFT_COVERAGE_DECISION_APPROVAL_NOT_GRANTED" in text
                or "NEXT_FRONTIER_PROTECTED_BODY_VERIFICATION_DECISION_APPROVAL_NOT_GRANTED" in text
                or "NEXT_FRONTIER_RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_READY_NOT_REUSABLE_AUTHORITY" in text
                or "NEXT_FRONTIER_OPERATOR_SELECTED_RTM_BLK_LINK_DECISION_AFTER_METADATA_EXPORT_NOT_GRANTED" in text
                or "NEXT_FRONTIER_ONE_EXACT_PRODUCTION_BLK_LINK_WRAPPER_REQUEST_NOT_GRANTED" in text
                or "NEXT_FRONTIER_POST_SINGLE_PRODUCTION_WRAPPER_RUN_OPERATOR_REVIEW_NOT_GRANTED" in text
                or "NEXT_FRONTIER_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL_NOT_BLANKET_AUTHORITY" in text
                or "NEXT_FRONTIER_OPERATOR_SELECTED_BLK_REQ_USE_OR_NEXT_COMPONENT" in text
                or "NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED" in text
                or "NEXT_FRONTIER_BLK_REQ_CLOSED_NEXT_COMPONENT_SELECTION_NOT_GRANTED" in text
                or "NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_EXACT_UNDO_WITH_CODEX_PROFILE_CONTAINMENT_AVAILABLE_NOT_GRANTED" in text
            )
            self.assertIn("no protected", text)
            self.assertIn("no drift rejection", text)
            self.assertIn("no coverage truth", text)
        self.assertLessEqual(len(roadmap.splitlines()), 140)
        self.assertLessEqual(len(index.splitlines()), 180)
        for sprint in range(159, 163):
            self.assertTrue((ROOT / "docs" / "outcomes" / f"BLK-SYSTEM-{sprint}_sprint-closeout.md").exists())
            self.assertEqual(list((ROOT / "docs" / "outcomes").glob(f"BLK-SYSTEM-{sprint}_task-*-outcome.md")), [])
            self.assertEqual(list((ROOT / "docs").glob(f"BLK-{sprint}_*.md")), [])

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

    def _request160(self):
        upstream = valid_blk158_execution_package()
        rec159 = build_post_generation_reconciliation_159(upstream, valid_post_generation_reconciliation_context_159(upstream))
        return build_trace_closure_authority_request_160(rec159, valid_trace_closure_authority_request_160(rec159))

    def _execution161(self):
        request160 = self._request160()
        return build_trace_closure_execution_161(request160, valid_trace_closure_execution_request_161(request160))


if __name__ == "__main__":
    unittest.main()
