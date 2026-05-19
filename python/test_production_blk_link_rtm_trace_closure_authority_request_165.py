import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_generation_approval_execution import (
    build_metadata_bound_rtm_generation_approval_execution,
    valid_metadata_bound_rtm_generation_approval_execution_request,
)
from test_metadata_bound_rtm_generation_approval_execution import valid_blk157_request_package
from metadata_rtm_post_generation_ladder_159_162 import (
    build_post_generation_reconciliation_159,
    build_post_trace_closure_review_162,
    build_trace_closure_authority_request_160,
    build_trace_closure_execution_161,
    valid_post_generation_reconciliation_context_159,
    valid_post_trace_closure_review_context_162,
    valid_trace_closure_authority_request_160,
    valid_trace_closure_execution_request_161,
)

from production_blk_link_rtm_trace_closure_authority_request_165 import (
    ACTIVE_HARDENING_MARKERS,
    AUTHORITY_REQUEST_PACKAGE_ID_165,
    EXACT_EXCLUDED_AUTHORITIES_165,
    EXACT_PROOF_OBLIGATIONS_165,
    NEXT_FRONTIER_165,
    NEXT_REQUIRED_AUTHORITY_165,
    REQUEST_SCOPE_165,
    REQUEST_STATUS_165,
    SELECTED_FRONTIER_165,
    SIDE_EFFECT_FLAGS_165,
    build_production_blk_link_rtm_trace_closure_authority_request_165,
    valid_production_blk_link_rtm_trace_closure_authority_request_165,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "production_blk_link_rtm_trace_closure_authority_request_165.py"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


def valid_blk158_execution_package():
    request_package = valid_blk157_request_package()
    execution_request = valid_metadata_bound_rtm_generation_approval_execution_request(request_package)
    return build_metadata_bound_rtm_generation_approval_execution(request_package, execution_request)


def valid_blk162_review_package():
    upstream158 = valid_blk158_execution_package()
    rec159 = build_post_generation_reconciliation_159(upstream158, valid_post_generation_reconciliation_context_159(upstream158))
    req160 = build_trace_closure_authority_request_160(rec159, valid_trace_closure_authority_request_160(rec159))
    exec161 = build_trace_closure_execution_161(req160, valid_trace_closure_execution_request_161(req160))
    return build_post_trace_closure_review_162(exec161, valid_post_trace_closure_review_context_162(exec161))


def rehash_review_package(package):
    package["review_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "review_package_hash"})
    return package


class ProductionBlkLinkRtmTraceClosureAuthorityRequest165Test(unittest.TestCase):
    def test_165_emits_request_only_package_bound_to_162_review_and_164_hardening(self):
        review162 = valid_blk162_review_package()
        request = valid_production_blk_link_rtm_trace_closure_authority_request_165(review162)

        package = build_production_blk_link_rtm_trace_closure_authority_request_165(review162, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS_165)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID_165)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE_165)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER_165)
        self.assertEqual(package["upstream_review_package_id"], "POST-METADATA-TRACE-CLOSURE-REVIEW-162-001")
        self.assertEqual(
            package["upstream_review_package_hash"],
            "sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9",
        )
        self.assertEqual(
            package["upstream_trace_closure_record_hash"],
            "sha256:2ecb6d2a56e53d9460e0c91320393ae8246aed76d1bd5a1e3237584d79e0e940",
        )
        self.assertEqual(package["active_hardening_markers"], list(ACTIVE_HARDENING_MARKERS))
        self.assertEqual(package["requested_authority"], "ONE_FUTURE_EXACT_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_CAPTURE")
        self.assertEqual(package["production_blk_link_rtm_trace_closure_authority"], "REQUEST_ONLY_NOT_GRANTED")
        self.assertTrue(package["request_future_exact_production_blk_link_rtm_trace_closure_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["future_run_id_reserved_or_consumed"])
        self.assertFalse(package["production_blk_link_execution_performed"])
        self.assertFalse(package["rtm_trace_closure_executed"])
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER_165)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY_165)
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_165)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_165)
        for flag in SIDE_EFFECT_FLAGS_165:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["authority_request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "authority_request_package_hash"}),
        )

    def test_165_rejects_forged_rehashed_or_side_effect_bearing_162_review(self):
        review162 = valid_blk162_review_package()
        request = valid_production_blk_link_rtm_trace_closure_authority_request_165(review162)

        forged = copy.deepcopy(review162)
        forged["review_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "review_package_hash does not match submitted BLK-162 package"):
            build_production_blk_link_rtm_trace_closure_authority_request_165(forged, request)

        forged = copy.deepcopy(review162)
        forged["review_package_id"] = "POST-METADATA-TRACE-CLOSURE-REVIEW-１６２-001"
        rehash_review_package(forged)
        forged_request = valid_production_blk_link_rtm_trace_closure_authority_request_165(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-162 post trace-closure review package"):
            build_production_blk_link_rtm_trace_closure_authority_request_165(forged, forged_request)

        forged = copy.deepcopy(review162)
        forged["production_blk_link_executed"] = True
        rehash_review_package(forged)
        with self.assertRaisesRegex(ValueError, "production_blk_link_executed must remain false|canonical BLK-162"):
            build_production_blk_link_rtm_trace_closure_authority_request_165(
                forged, valid_production_blk_link_rtm_trace_closure_authority_request_165(forged)
            )

    def test_165_rejects_retargeting_laundering_bad_sets_window_and_side_effects(self):
        review162 = valid_blk162_review_package()
        base_request = valid_production_blk_link_rtm_trace_closure_authority_request_165(review162)
        cases = [
            ({"authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-１６５-００１"}, "authority_request_package_id must be"),
            ({"selected_frontier": "production_blk_link_rtm_trace_closure_execution"}, "authority-laundering text|selected_frontier must be"),
            ({"request_scope": "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_EXECUTION"}, "authority-laundering text|request_scope must be"),
            ({"upstream_review_package_hash": "sha256:" + "0" * 64}, "upstream_review_package_hash must match"),
            ({"active_hardening_markers": list(ACTIVE_HARDENING_MARKERS)[:-1]}, "active_hardening_markers must match exact BLK-162/163/164 state"),
            ({"request_future_exact_production_blk_link_rtm_trace_closure_approval": False}, "request_future_exact_production_blk_link_rtm_trace_closure_approval must be true"),
            ({"expired": True}, "authority request must not be expired"),
            ({"replayed": True}, "authority request must not be replayed"),
            ({"stale": True}, "authority request must not be stale"),
            ({"expires_at": base_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "authority request must not be calendar-expired"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_165) + [sorted(EXACT_PROOF_OBLIGATIONS_165)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_165) + [sorted(EXACT_EXCLUDED_AUTHORITIES_165)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819-approved-for-production"}, "authority-laundering text"),
            ({"authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-RTMGenerated"}, "authority-laundering text"),
            ({"authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-The%20system%20shall"}, "protected body text"),
            ({"operator_attestation": base_request["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
            ({"productionBlkLinkExecuted": False}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_authority_request_165(review162, request)

        for boolean_key in SIDE_EFFECT_FLAGS_165:
            request = copy.deepcopy(base_request)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_production_blk_link_rtm_trace_closure_authority_request_165(review162, request)

    def test_165_request_window_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        review162 = valid_blk162_review_package()
        base_request = valid_production_blk_link_rtm_trace_closure_authority_request_165(review162)
        alt_request = valid_production_blk_link_rtm_trace_closure_authority_request_165(
            review162,
            requested_at="2099-05-16T15:31:00+10:00",
            expires_at="2099-05-16T15:46:00+10:00",
        )

        base_package = build_production_blk_link_rtm_trace_closure_authority_request_165(review162, base_request)
        alt_package = build_production_blk_link_rtm_trace_closure_authority_request_165(review162, alt_request)

        self.assertNotEqual(base_package["authority_request_hash"], alt_package["authority_request_hash"])
        self.assertNotEqual(base_package["authority_request_package_hash"], alt_package["authority_request_package_hash"])
        base_request["operator_attestation"]["approval_capture_not_performed"] = "mutated"
        review162["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base_request["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["approval_capture_not_performed"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

    def test_165_docs_advance_to_approval_capture_frontier_without_bloat_or_extra_docs(self):
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
                or "NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED" in text
            )
            self.assertNotIn("NEXT_FRONTIER_FURTHER_HARDENING_OR_AUTHORITY_REQUEST_NOT_GRANTED", text)
            self.assertIn("no production `blk-link`", text)
            self.assertIn("no protected", text)
            self.assertIn("no drift rejection", text)
            self.assertIn("no coverage truth", text)
        self.assertLessEqual(len(roadmap.splitlines()), 185)
        self.assertLessEqual(len(index.splitlines()), 180)
        self.assertTrue((ROOT / "docs" / "outcomes" / "BLK-SYSTEM-165_sprint-closeout.md").exists())
        self.assertEqual(list((ROOT / "docs" / "outcomes").glob("BLK-SYSTEM-165_task-*-outcome.md")), [])
        self.assertEqual(list((ROOT / "docs").glob("BLK-165_*.md")), [])

    def test_165_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
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
