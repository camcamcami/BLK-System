import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_authority_request import build_production_blk_link_rtm_trace_closure_authority_request
from test_production_blk_link_rtm_trace_closure_authority_request import (
    valid_authority_request,
    valid_blk132_execution_package,
)

from production_blk_link_rtm_trace_closure_approval_capture import (
    APPROVAL_CAPTURE_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT,
    DECISION_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    STATUS,
    build_production_blk_link_rtm_trace_closure_approval_capture,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "production_blk_link_rtm_trace_closure_approval_capture.py"


def valid_blk133_request_package():
    upstream = valid_blk132_execution_package()
    request = valid_authority_request(upstream)
    return build_production_blk_link_rtm_trace_closure_authority_request(upstream, request)


def valid_approval_decision(request_package=None, **overrides):
    if request_package is None:
        request_package = valid_blk133_request_package()
    decision = {
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "operator_identity": request_package["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "upstream_authority_request_package_id": request_package["authority_request_package_id"],
        "upstream_authority_request_package_hash": request_package["authority_request_package_hash"],
        "upstream_execution_package_id": request_package["upstream_execution_package_id"],
        "upstream_execution_package_hash": request_package["upstream_execution_package_hash"],
        "upstream_trace_closure_record_id": request_package["upstream_trace_closure_record_id"],
        "upstream_trace_closure_record_hash": request_package["upstream_trace_closure_record_hash"],
        "publication_record_hash": request_package["publication_record_hash"],
        "beo_id": request_package["beo_id"],
        "beb_id": request_package["beb_id"],
        "exact_trace_identities": list(request_package["exact_trace_identities"]),
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": "2099-05-15T12:31:00+10:00",
        "expires_at": "2099-05-15T12:40:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_approval_text_raw": "plan and then execute all tasks in the next blk-system sprint",
        "operator_attestation": {
            "exact_blk133_request_reviewed": True,
            "approval_limited_to_one_future_production_blk_link_rtm_trace_closure_execution": True,
            "future_run_id_reserved_not_consumed": True,
            "production_trace_closure_not_executed_by_this_decision": True,
            "rtm_generation_not_performed_by_this_decision": True,
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
        decision[flag] = False
    decision.update(overrides)
    return decision


def rehash_request_package(package):
    package["authority_request_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "authority_request_package_hash"}
    )
    return package


class ProductionBlkLinkRtmTraceClosureApprovalCaptureTest(unittest.TestCase):
    def test_captures_exact_approval_without_executing_production_trace_closure_or_rtm(self):
        request_package = valid_blk133_request_package()
        decision = valid_approval_decision(request_package)

        package = build_production_blk_link_rtm_trace_closure_approval_capture(request_package, decision)

        self.assertEqual(package["approval_capture_status"], STATUS)
        self.assertEqual(package["approval_capture_package_id"], APPROVAL_CAPTURE_PACKAGE_ID)
        self.assertEqual(package["decision_scope"], DECISION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(
            package["upstream_authority_request_package_id"],
            "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-001",
        )
        self.assertEqual(
            package["upstream_authority_request_package_hash"],
            "sha256:8fa1f60ed592b4fda4b1b3cd2e2132a19fd74a24f80b559e8c1b57aa5221e271",
        )
        self.assertEqual(package["upstream_execution_package_id"], "RTM-TRACE-CLOSURE-EXECUTION-132-001")
        self.assertEqual(package["upstream_trace_closure_record_id"], "RTM-TRACE-CLOSURE-RECORD-132-001")
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["future_run_id"], FUTURE_RUN_ID)
        self.assertEqual(package["decision_result"], DECISION_RESULT)
        self.assertEqual(package["next_required_authority"], NEXT_REQUIRED_AUTHORITY)
        self.assertTrue(package["approval_decision_captured"])
        self.assertTrue(package["future_production_blk_link_rtm_trace_closure_execution_approved"])
        self.assertFalse(package["future_run_id_consumed"])
        self.assertFalse(package["production_blk_link_rtm_trace_closure_executed"])
        self.assertFalse(package["rtm_generated"])
        self.assertFalse(package["rtm_drift_rejection_performed"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertFalse(package["coverage_truth_established"])
        self.assertFalse(package["protected_body_reads"])
        self.assertEqual(package["decision_hash"], _canonical_hash(decision))
        self.assertEqual(package["decided_at"], decision["decided_at"])
        self.assertEqual(package["expires_at"], decision["expires_at"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertRegex(package["approval_capture_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(
            package["approval_capture_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "approval_capture_package_hash"}),
        )

    def test_rejects_forged_rehashed_or_wrong_blk133_request_package(self):
        request_package = valid_blk133_request_package()
        decision = valid_approval_decision(request_package)

        forged = copy.deepcopy(request_package)
        forged["beo_id"] = "BEO_999"
        with self.assertRaisesRegex(ValueError, "authority_request_package_hash does not match submitted BLK-133 package"):
            build_production_blk_link_rtm_trace_closure_approval_capture(forged, decision)

        forged = copy.deepcopy(request_package)
        forged["beo_id"] = "BEO_999"
        rehash_request_package(forged)
        forged_decision = valid_approval_decision(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-133 authority request"):
            build_production_blk_link_rtm_trace_closure_approval_capture(forged, forged_decision)

        forged = copy.deepcopy(request_package)
        forged["approval_capture_performed"] = True
        rehash_request_package(forged)
        forged_decision = valid_approval_decision(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-133 authority request"):
            build_production_blk_link_rtm_trace_closure_approval_capture(forged, forged_decision)

    def test_rejects_bad_scope_retargeting_replay_expiry_sets_unicode_ids_and_side_effects(self):
        request_package = valid_blk133_request_package()
        base_decision = valid_approval_decision(request_package)
        cases = [
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-１３４-００１"}, "approval_capture_package_id must be"),
            ({"selected_frontier": "production_blk_link_rtm_trace_closure_execution"}, "selected_frontier must be|authority-laundering text"),
            ({"decision_scope": "PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_APPROVAL_AND_EXECUTION"}, "decision_scope must be|authority-laundering text"),
            ({"upstream_authority_request_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-133-999"}, "upstream_authority_request_package_id must match"),
            ({"upstream_authority_request_package_hash": "sha256:" + "0" * 64}, "upstream_authority_request_package_hash must match"),
            ({"upstream_trace_closure_record_id": "RTM-TRACE-CLOSURE-RECORD-132-999"}, "upstream_trace_closure_record_id must match"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-134-OTHER"}, "approval_id must be"),
            ({"future_run_id": "RUN-BLK-SYSTEM-１３５-PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-001"}, "future_run_id must be"),
            ({"decision_result": "APPROVED_FOR_PRODUCTION_BLK_LINK_EXECUTION"}, "decision_result must be|authority-laundering text"),
            ({"exact_trace_identities": ["REQ:REQ-１３４:sha256:" + "a" * 64]}, "exact_trace_identities id must be exact"),
            ({"expired": True}, "approval decision must not be expired"),
            ({"replayed": True}, "approval decision must not be replayed"),
            ({"stale": True}, "approval decision must not be stale"),
            ({"expires_at": base_decision["decided_at"]}, "expires_at must be after decided_at"),
            ({"decided_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "approval decision must not be calendar-expired"),
            ({"decided_at": "2099-05-15T12:20:00+10:00", "expires_at": "2099-05-15T12:40:00+10:00"}, "approval decision must not predate BLK-133 request"),
            ({"decided_at": "2099-05-15T12:45:00+10:00", "expires_at": "2099-05-15T12:50:00+10:00"}, "decision window must end within BLK-133 request expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(base_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_approval_capture(request_package, decision)

        for boolean_key in SIDE_EFFECT_FLAGS:
            decision = copy.deepcopy(base_decision)
            decision[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_production_blk_link_rtm_trace_closure_approval_capture(request_package, decision)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        request_package = valid_blk133_request_package()
        base_decision = valid_approval_decision(request_package)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-productionBlkLinkExecuted"}, "authority-laundering text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-ActiveVaultHashComparison"}, "authority-laundering text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-The%20system%20shall"}, "protected body text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-coverageTruthEstablished"}, "authority-laundering text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-sourceMutationAuthorized"}, "authority-laundering text"),
            ({"approval_capture_package_id": "PRODUCTION-BLK-LINK-RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-134-packageManagersAuthorized"}, "authority-laundering text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base_decision["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            decision = copy.deepcopy(base_decision)
            decision.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_production_blk_link_rtm_trace_closure_approval_capture(request_package, decision)

    def test_decision_window_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        request_package = valid_blk133_request_package()
        base_decision = valid_approval_decision(request_package)
        alt_decision = valid_approval_decision(
            request_package,
            decided_at="2099-05-15T12:32:00+10:00",
            expires_at="2099-05-15T12:41:00+10:00",
        )

        base_package = build_production_blk_link_rtm_trace_closure_approval_capture(request_package, base_decision)
        alt_package = build_production_blk_link_rtm_trace_closure_approval_capture(request_package, alt_decision)

        self.assertEqual(base_package["decision_hash"], _canonical_hash(base_decision))
        self.assertEqual(alt_package["decision_hash"], _canonical_hash(alt_decision))
        self.assertNotEqual(base_package["decision_hash"], alt_package["decision_hash"])
        self.assertNotEqual(base_package["approval_capture_package_hash"], alt_package["approval_capture_package_hash"])

        base_decision["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        request_package["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base_decision["operator_attestation"])
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
