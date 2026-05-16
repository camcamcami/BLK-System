import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_authority_request_165 import (
    build_production_blk_link_rtm_trace_closure_authority_request_165,
    valid_production_blk_link_rtm_trace_closure_authority_request_165,
)
from test_production_blk_link_rtm_trace_closure_authority_request_165 import valid_blk162_review_package

from production_blk_link_rtm_trace_closure_decision_execution_166 import (
    APPROVAL_ID_166,
    DECISION_EXECUTION_PACKAGE_ID_166,
    DECISION_EXECUTION_SCOPE_166,
    DECISION_EXECUTION_STATUS_166,
    EXACT_EXCLUDED_AUTHORITIES_166,
    EXACT_PROOF_OBLIGATIONS_166,
    EXECUTION_RECORD_ID_166,
    NEXT_REQUIRED_AUTHORITY_166,
    RUN_ID_CONSUMED_166,
    SELECTED_FRONTIER_166,
    SIDE_EFFECT_FLAGS_166,
    build_production_blk_link_rtm_trace_closure_decision_execution_166,
    valid_production_blk_link_rtm_trace_closure_decision_execution_166,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "production_blk_link_rtm_trace_closure_decision_execution_166.py"


def valid_blk165_request_package():
    review = valid_blk162_review_package()
    request = valid_production_blk_link_rtm_trace_closure_authority_request_165(review)
    return build_production_blk_link_rtm_trace_closure_authority_request_165(review, request)


def rehash_blk165_request_package(package):
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


class ProductionBlkLinkRtmTraceClosureDecisionExecution166Test(unittest.TestCase):
    def test_166_captures_operator_decision_and_consumes_one_run_in_record_only_package(self):
        request165 = valid_blk165_request_package()
        decision_execution = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)

        package = build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, decision_execution)

        self.assertEqual(package["decision_execution_status"], DECISION_EXECUTION_STATUS_166)
        self.assertEqual(package["decision_execution_package_id"], DECISION_EXECUTION_PACKAGE_ID_166)
        self.assertEqual(package["decision_execution_scope"], DECISION_EXECUTION_SCOPE_166)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER_166)
        self.assertEqual(package["upstream_authority_request_package_id"], "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-165-001")
        self.assertEqual(
            package["upstream_authority_request_package_hash"],
            "sha256:858ecad7e6806932745501acfca4ac53c6912668a0fc5ce0a27ba097951cda3d",
        )
        self.assertEqual(package["approval_id"], APPROVAL_ID_166)
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED_166)
        self.assertTrue(package["operator_decision_captured"])
        self.assertTrue(package["one_run_id_consumed_in_record_only_evidence"])
        self.assertTrue(package["production_blk_link_rtm_trace_closure_record_emitted"])
        self.assertEqual(package["execution_record_id"], EXECUTION_RECORD_ID_166)
        self.assertEqual(package["execution_record"]["consumed_run_id"], RUN_ID_CONSUMED_166)
        self.assertEqual(package["execution_record"]["trace_closure_authority"], "EXACT_OPERATOR_APPROVED_PRODUCTION_TRACE_CLOSURE_RECORD_ONLY")
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY_166)
        self.assertEqual(package["decision_execution_request_hash"], _canonical_hash(decision_execution))
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS_166)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES_166)
        for flag in SIDE_EFFECT_FLAGS_166:
            self.assertIs(package[flag], False, flag)
        for nested_flag in (
            "reusable_blk_link_authority_granted",
            "rtm_generated",
            "rtm_drift_rejection_performed",
            "active_vault_hash_comparison_performed",
            "coverage_truth_established",
            "protected_body_reads",
            "public_ledger_mutation",
        ):
            self.assertIs(package["execution_record"][nested_flag], False, nested_flag)
        self.assertEqual(
            package["execution_record_hash"],
            _canonical_hash({key: value for key, value in package["execution_record"].items() if key != "execution_record_hash"}),
        )
        self.assertEqual(
            package["decision_execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "decision_execution_package_hash"}),
        )

    def test_166_rejects_forged_rehashed_or_side_effect_bearing_blk165_request(self):
        request165 = valid_blk165_request_package()
        decision_execution = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)

        forged = copy.deepcopy(request165)
        forged["authority_request_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "authority_request_package_hash does not match submitted BLK-165 package"):
            build_production_blk_link_rtm_trace_closure_decision_execution_166(forged, decision_execution)

        forged = copy.deepcopy(request165)
        forged["active_hardening_markers"] = forged["active_hardening_markers"][:-1]
        rehash_blk165_request_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-165 authority request"):
            build_production_blk_link_rtm_trace_closure_decision_execution_166(
                forged, valid_production_blk_link_rtm_trace_closure_decision_execution_166(forged)
            )

        forged = copy.deepcopy(request165)
        forged["production_blk_link_executed"] = True
        rehash_blk165_request_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-165 authority request"):
            build_production_blk_link_rtm_trace_closure_decision_execution_166(
                forged, valid_production_blk_link_rtm_trace_closure_decision_execution_166(forged)
            )

    def test_166_rejects_retargeting_laundering_bad_sets_windows_unicode_ids_and_side_effects(self):
        request165 = valid_blk165_request_package()
        base = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)
        cases = [
            ({"decision_execution_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-DECISION-EXECUTION-１６６-００１"}, "decision_execution_package_id must be"),
            ({"selected_frontier": "rtm_generation"}, "selected_frontier must be|authority-laundering text"),
            ({"decision_execution_scope": "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AND_RTM_GENERATION"}, "decision_execution_scope must be|authority-laundering text"),
            ({"upstream_authority_request_package_hash": "sha256:" + "0" * 64}, "upstream_authority_request_package_hash must match"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-166-OTHER"}, "approval_id must be"),
            ({"run_id_to_consume": "RUN-BLK-SYSTEM-１６６-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"}, "run_id_to_consume must be"),
            ({"exact_trace_identities": ["REQ:REQ-１６６:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"expired": True}, "decision execution request must not be expired"),
            ({"replayed": True}, "decision execution request must not be replayed"),
            ({"stale": True}, "decision execution request must not be stale"),
            ({"expires_at": base["decided_at"]}, "expires_at must be after decided_at"),
            ({"decided_at": "2000-01-01T00:00:00+10:00", "requested_at": "2000-01-01T00:01:00+10:00", "expires_at": "2000-01-01T00:02:00+10:00"}, "decision execution request must not be calendar-expired"),
            ({"decided_at": "2099-05-16T15:20:00+10:00"}, "decision must not predate BLK-165 request"),
            ({"decided_at": "2099-05-16T15:40:00+10:00", "requested_at": "2099-05-16T15:46:00+10:00", "expires_at": "2099-05-16T15:50:00+10:00"}, "decision/execution window must end within BLK-165 request expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS_166) + [sorted(EXACT_PROOF_OBLIGATIONS_166)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES_166) + [sorted(EXACT_EXCLUDED_AUTHORITIES_166)[0]]}, "excluded_authorities must not contain duplicates"),
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"decision_execution_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-DECISION-EXECUTION-166-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"decision_execution_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-DECISION-EXECUTION-166-The%20system%20shall"}, "protected body text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, request)

        for boolean_key in SIDE_EFFECT_FLAGS_166:
            request = copy.deepcopy(base)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, request)

    def test_166_decision_execution_window_is_hash_bound_and_inputs_are_defensively_copied(self):
        request165 = valid_blk165_request_package()
        base = valid_production_blk_link_rtm_trace_closure_decision_execution_166(request165)
        alt = valid_production_blk_link_rtm_trace_closure_decision_execution_166(
            request165,
            decided_at="2099-05-16T15:36:00+10:00",
            requested_at="2099-05-16T15:37:00+10:00",
            expires_at="2099-05-16T15:44:00+10:00",
        )

        base_package = build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, base)
        alt_package = build_production_blk_link_rtm_trace_closure_decision_execution_166(request165, alt)

        self.assertNotEqual(base_package["decision_execution_request_hash"], alt_package["decision_execution_request_hash"])
        self.assertNotEqual(base_package["decision_execution_package_hash"], alt_package["decision_execution_package_hash"])
        base["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        request165["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

    def test_166_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
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
