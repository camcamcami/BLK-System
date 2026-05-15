import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from post_metadata_rtm_blk_link_reconciliation_review import (
    build_post_metadata_rtm_blk_link_reconciliation_review,
    valid_post_reconciliation_review_context,
)
from test_post_metadata_rtm_blk_link_reconciliation_review import valid_blk155_execution_package

from metadata_bound_rtm_generation_decision_request import (
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    REQUEST_PACKAGE_ID,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    build_metadata_bound_rtm_generation_decision_request,
    valid_metadata_bound_rtm_generation_decision_request,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_rtm_generation_decision_request.py"


def valid_blk156_review_package():
    execution = valid_blk155_execution_package()
    context = valid_post_reconciliation_review_context(execution)
    return build_post_metadata_rtm_blk_link_reconciliation_review(execution, context)


def rehash_review_package(package):
    package["review_package_hash"] = _canonical_hash({k: v for k, v in package.items() if k != "review_package_hash"})
    return package


class MetadataBoundRtmGenerationDecisionRequestTest(unittest.TestCase):
    def test_builds_request_only_package_bound_to_exact_blk156_review(self):
        review = valid_blk156_review_package()
        request = valid_metadata_bound_rtm_generation_decision_request(review)

        package = build_metadata_bound_rtm_generation_decision_request(review, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["request_package_id"], REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["operator_identity"], "discord:684235178083745819")
        self.assertEqual(package["upstream_review_package_id"], "POST-METADATA-RTM-BLK-LINK-RECONCILIATION-REVIEW-156-001")
        self.assertEqual(package["upstream_review_package_hash"], "sha256:9dcbe35946b9320fc4aaf46cfb31273e38ccf56a49249f7eac91be37278f537e")
        self.assertEqual(package["upstream_reconciliation_record_hash"], "sha256:1a2e06f4cb0c539f44d55c49b798cc5251d2e9a821f47e8794ccc0719747d026")
        self.assertEqual(package["beo_id"], "BEO_126")
        self.assertEqual(package["beb_id"], "BEB_126")
        self.assertTrue(package["request_future_exact_metadata_bound_rtm_generation_approval"])
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["future_run_id_reserved"])
        self.assertFalse(package["rtm_generation_authorized"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["production_blk_link_executed"])
        self.assertEqual(package["decision_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(
            package["request_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "request_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_non_clean_blk156_review(self):
        review = valid_blk156_review_package()
        request = valid_metadata_bound_rtm_generation_decision_request(review)

        forged = copy.deepcopy(review)
        forged["review_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "review_package_hash does not match submitted BLK-156 package"):
            build_metadata_bound_rtm_generation_decision_request(forged, request)

        forged = copy.deepcopy(review)
        forged["review_package_id"] = "POST-METADATA-RTM-BLK-LINK-RECONCILIATION-REVIEW-157-001"
        rehash_review_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-156 review package required"):
            build_metadata_bound_rtm_generation_decision_request(
                forged,
                valid_metadata_bound_rtm_generation_decision_request(forged),
            )

        forged = copy.deepcopy(review)
        forged["next_frontier_granted"] = True
        rehash_review_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-156 review package required|next_frontier_granted must remain false"):
            build_metadata_bound_rtm_generation_decision_request(
                forged,
                valid_metadata_bound_rtm_generation_decision_request(forged),
            )

    def test_request_rejects_approval_execution_drift_coverage_protected_body_and_bad_sets(self):
        review = valid_blk156_review_package()
        base = valid_metadata_bound_rtm_generation_decision_request(review)
        cases = [
            ({"request_package_id": "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-１５７-001"}, "request_package_id must be"),
            ({"selected_frontier": "metadataBoundRTMGenerationApproved"}, "selected_frontier must be|authority-laundering text"),
            ({"approval_capture_performed": True}, "approval_capture_performed must remain false"),
            ({"future_run_id_reserved": True}, "future_run_id_reserved must remain false"),
            ({"rtm_generation_authorized": True}, "rtm_generation_authorized must remain false"),
            ({"rtm_generated": True}, "rtm_generated must remain false"),
            ({"rtm_drift_rejection_authorized": True}, "rtm_drift_rejection_authorized must remain false"),
            ({"coverage_truth_established": True}, "coverage_truth_established must remain false"),
            ({"protected_body_reads": True}, "protected_body_reads must remain false"),
            ({"reusable_blk_link_authority_granted": True}, "reusable_blk_link_authority_granted must remain false"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_decision_request(review, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        review = valid_blk156_review_package()
        base = valid_metadata_bound_rtm_generation_decision_request(review)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"request_scope": "REQUEST_AND_COVERAGE_TRUTH"}, "request_scope must be|authority-laundering text"),
            ({"request_package_id": "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"request_package_id": "METADATA-BOUND-RTM-GENERATION-DECISION-REQUEST-157-The%20system%20shall"}, "protected body text"),
            ({"curlWrapper": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
            ({"required_future_evidence": base["required_future_evidence"] + [{"reqBody": "The system shall remain hidden."}]}, "protected body text|authority-laundering text"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_rtm_generation_decision_request(review, request)

    def test_request_hash_is_bound_and_returned_inputs_are_defensively_copied(self):
        review = valid_blk156_review_package()
        base = valid_metadata_bound_rtm_generation_decision_request(review)
        alt = valid_metadata_bound_rtm_generation_decision_request(
            review,
            requested_at="2099-05-16T13:10:00+10:00",
            expires_at="2099-05-16T14:10:00+10:00",
        )

        base_package = build_metadata_bound_rtm_generation_decision_request(review, base)
        alt_package = build_metadata_bound_rtm_generation_decision_request(review, alt)

        self.assertEqual(base_package["decision_request_hash"], _canonical_hash(base))
        self.assertEqual(alt_package["decision_request_hash"], _canonical_hash(alt))
        self.assertNotEqual(base_package["decision_request_hash"], alt_package["decision_request_hash"])
        self.assertNotEqual(base_package["request_package_hash"], alt_package["request_package_hash"])

        base["operator_attestation"]["no_drift_rejection_or_coverage_truth"] = "mutated"
        review["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "9" * 64)
        self.assertIs(base_package["operator_attestation"]["no_drift_rejection_or_coverage_truth"], True)
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
