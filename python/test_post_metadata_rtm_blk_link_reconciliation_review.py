import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from bounded_metadata_rtm_blk_link_reconciliation_execution import (
    build_bounded_metadata_rtm_blk_link_reconciliation_execution,
    valid_bounded_metadata_reconciliation_execution_request,
)
from test_bounded_metadata_rtm_blk_link_reconciliation_execution import valid_blk154_request_package

from post_metadata_rtm_blk_link_reconciliation_review import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_FRONTIER,
    REVIEW_PACKAGE_ID,
    REVIEW_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_post_metadata_rtm_blk_link_reconciliation_review,
    valid_post_reconciliation_review_context,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "post_metadata_rtm_blk_link_reconciliation_review.py"
BLK077 = ROOT / "docs" / "BLK-077_blk-system-post-078-roadmap.md"
BLK079 = ROOT / "docs" / "BLK-079_post-078-current-state-authority-index.md"


def valid_blk155_execution_package():
    request_package = valid_blk154_request_package()
    execution_request = valid_bounded_metadata_reconciliation_execution_request(request_package)
    return build_bounded_metadata_rtm_blk_link_reconciliation_execution(request_package, execution_request)


def rehash_execution_package(package):
    package["reconciliation_record"]["record_hash"] = _canonical_hash(
        {k: v for k, v in package["reconciliation_record"].items() if k != "record_hash"}
    )
    package["reconciliation_record_hash"] = package["reconciliation_record"]["record_hash"]
    package["execution_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "execution_package_hash"})
    return package


class PostMetadataRtmBlkLinkReconciliationReviewTest(unittest.TestCase):
    def test_reviews_clean_blk155_reconciliation_and_selects_next_decision_without_authority(self):
        execution = valid_blk155_execution_package()
        context = valid_post_reconciliation_review_context(execution)

        package = build_post_metadata_rtm_blk_link_reconciliation_review(execution, context)

        self.assertEqual(package["review_status"], REVIEW_STATUS)
        self.assertEqual(package["review_package_id"], REVIEW_PACKAGE_ID)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["upstream_execution_package_hash"], execution["execution_package_hash"])
        self.assertEqual(package["upstream_reconciliation_record_hash"], execution["reconciliation_record_hash"])
        self.assertEqual(package["review_result"], "CLEAN_METADATA_RECONCILIATION_REVIEWED_NEXT_DECISION_REQUIRED")
        self.assertEqual(package["next_frontier"], NEXT_FRONTIER)
        self.assertFalse(package["next_frontier_granted"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["production_blk_link_executed"])
        self.assertFalse(package["rtm_drift_rejection_authorized"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        self.assertEqual(package["review_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["review_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "review_package_hash"}),
        )

    def test_rejects_forged_non_clean_or_non_canonical_execution_package(self):
        execution = valid_blk155_execution_package()
        context = valid_post_reconciliation_review_context(execution)

        forged = copy.deepcopy(execution)
        forged["execution_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "execution_package_hash does not match submitted BLK-155 package"):
            build_post_metadata_rtm_blk_link_reconciliation_review(forged, context)

        forged = copy.deepcopy(execution)
        forged["reconciliation_record"]["mismatch_count"] = 1
        forged["reconciliation_record"]["mismatches"] = ["REQ-001"]
        rehash_execution_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-155 execution package required|clean BLK-155 reconciliation required"):
            build_post_metadata_rtm_blk_link_reconciliation_review(forged, valid_post_reconciliation_review_context(forged))

    def test_rejects_review_laundering_side_effects_bad_sets_and_bad_frontier(self):
        execution = valid_blk155_execution_package()
        base = valid_post_reconciliation_review_context(execution)
        cases = [
            ({"selected_frontier": "postReviewAndGenerateRTM"}, "selected_frontier must be|authority-laundering text"),
            ({"next_frontier": "NEXT_FRONTIER_RTM_GENERATION_APPROVED"}, "next_frontier must be|authority-laundering text"),
            ({"next_frontier_granted": True}, "next_frontier_granted must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"review_package_id": "POST-METADATA-RTM-BLK-LINK-RECONCILIATION-REVIEW-156-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            context = copy.deepcopy(base)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_post_metadata_rtm_blk_link_reconciliation_review(execution, context)

    def test_roadmap_and_index_advance_to_post_generation_reconciliation_without_adjacent_authority(self):
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
                or "NEXT_FRONTIER_VALIDATION_PROFILES_CLOSED_BLK_TEST_SELECTION_NOT_GRANTED" in text
            )
            self.assertIn("reusable RTM generation", text)
            self.assertIn("no protected", text)
        self.assertNotIn("coverage truth established", index.lower())
        self.assertNotIn("production `blk-link` execution authorized", roadmap)

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
