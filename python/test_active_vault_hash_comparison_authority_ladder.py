import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from production_blk_link_rtm_trace_closure_post_execution_reconciliation import (
    build_production_blk_link_rtm_trace_closure_post_execution_reconciliation,
)
from test_production_blk_link_rtm_trace_closure_post_execution_reconciliation import (
    valid_blk135_execution_package,
    valid_reconciliation_context,
)

from active_vault_hash_comparison_decision_package import (
    DECISION_PACKAGE_ID,
    DECISION_SCOPE,
    DECISION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES as DECISION_EXCLUDED,
    EXACT_PROOF_OBLIGATIONS as DECISION_PROOFS,
    NEXT_REQUIRED_AUTHORITY as DECISION_NEXT,
    SELECTED_FRONTIER as DECISION_FRONTIER,
    SIDE_EFFECT_FLAGS as DECISION_FLAGS,
    build_active_vault_hash_comparison_decision_package,
)
from active_vault_hash_comparison_authority_request import (
    AUTHORITY_REQUEST_PACKAGE_ID,
    EXACT_EXCLUDED_AUTHORITIES as REQUEST_EXCLUDED,
    EXACT_PROOF_OBLIGATIONS as REQUEST_PROOFS,
    NEXT_REQUIRED_AUTHORITY as REQUEST_NEXT,
    REQUEST_SCOPE,
    REQUEST_STATUS,
    SELECTED_FRONTIER as REQUEST_FRONTIER,
    SIDE_EFFECT_FLAGS as REQUEST_FLAGS,
    build_active_vault_hash_comparison_authority_request,
)
from active_vault_hash_comparison_approval_capture import (
    APPROVAL_CAPTURE_PACKAGE_ID,
    APPROVAL_ID,
    DECISION_RESULT,
    DECISION_SCOPE as APPROVAL_SCOPE,
    EXACT_EXCLUDED_AUTHORITIES as APPROVAL_EXCLUDED,
    EXACT_OPERATOR_APPROVAL_TEXT,
    EXACT_PROOF_OBLIGATIONS as APPROVAL_PROOFS,
    FUTURE_RUN_ID,
    NEXT_REQUIRED_AUTHORITY as APPROVAL_NEXT,
    SELECTED_FRONTIER as APPROVAL_FRONTIER,
    SIDE_EFFECT_FLAGS as APPROVAL_FLAGS,
    STATUS as APPROVAL_STATUS,
    build_active_vault_hash_comparison_approval_capture,
)

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    ROOT / "python" / "active_vault_hash_comparison_decision_package.py",
    ROOT / "python" / "active_vault_hash_comparison_authority_request.py",
    ROOT / "python" / "active_vault_hash_comparison_approval_capture.py",
]


def valid_blk136_reconciliation_package():
    execution = valid_blk135_execution_package()
    context = valid_reconciliation_context(execution)
    return build_production_blk_link_rtm_trace_closure_post_execution_reconciliation(execution, context)


def valid_decision_context(reconciliation=None, **overrides):
    if reconciliation is None:
        reconciliation = valid_blk136_reconciliation_package()
    context = {
        "decision_package_id": DECISION_PACKAGE_ID,
        "operator_identity": reconciliation["operator_identity"],
        "decision_scope": DECISION_SCOPE,
        "selected_frontier": DECISION_FRONTIER,
        "upstream_reconciliation_package_id": reconciliation["reconciliation_package_id"],
        "upstream_reconciliation_package_hash": reconciliation["reconciliation_package_hash"],
        "upstream_execution_package_id": reconciliation["upstream_execution_package_id"],
        "upstream_execution_package_hash": reconciliation["upstream_execution_package_hash"],
        "upstream_execution_record_id": reconciliation["upstream_execution_record_id"],
        "upstream_execution_record_hash": reconciliation["upstream_execution_record_hash"],
        "beo_id": reconciliation["beo_id"],
        "beb_id": reconciliation["beb_id"],
        "exact_trace_identities": list(reconciliation["exact_trace_identities"]),
        "decided_at": "2099-05-15T13:00:00+10:00",
        "stale": False,
        "replayed": False,
        "operator_attestation": {
            "exact_blk136_reconciliation_reviewed": True,
            "selected_one_frontier_only": True,
            "metadata_hash_only_active_vault_comparison_selected": True,
            "no_active_vault_comparison_performed": True,
            "no_protected_body_reads": True,
            "no_rtm_generation": True,
            "no_drift_rejection": True,
            "no_coverage_truth": True,
            "no_reusable_blk_link_authority": True,
            "no_beb_dispatch_or_beo_closeout": True,
            "no_signer_storage_ledger_side_effects": True,
            "no_target_source_git_mutation": True,
            "no_blk_pipe_blk_test_codex_tooling": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(DECISION_PROOFS),
        "excluded_authorities": sorted(DECISION_EXCLUDED),
    }
    for flag in DECISION_FLAGS:
        context[flag] = False
    context.update(overrides)
    return context


def valid_decision_package():
    reconciliation = valid_blk136_reconciliation_package()
    return build_active_vault_hash_comparison_decision_package(reconciliation, valid_decision_context(reconciliation))


def valid_request_context(decision=None, **overrides):
    if decision is None:
        decision = valid_decision_package()
    request = {
        "authority_request_package_id": AUTHORITY_REQUEST_PACKAGE_ID,
        "operator_identity": decision["operator_identity"],
        "request_scope": REQUEST_SCOPE,
        "selected_frontier": REQUEST_FRONTIER,
        "upstream_decision_package_id": decision["decision_package_id"],
        "upstream_decision_package_hash": decision["decision_package_hash"],
        "upstream_reconciliation_package_id": decision["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": decision["upstream_reconciliation_package_hash"],
        "beo_id": decision["beo_id"],
        "beb_id": decision["beb_id"],
        "exact_trace_identities": list(decision["exact_trace_identities"]),
        "request_future_exact_metadata_hash_only_active_vault_comparison_approval": True,
        "requested_at": "2099-05-15T13:05:00+10:00",
        "expires_at": "2099-05-16T13:05:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk137_decision_reviewed": True,
            "request_is_for_future_approval_not_approval": True,
            "metadata_hash_only_scope_preserved": True,
            "approval_capture_not_performed": True,
            "comparison_not_performed": True,
            "protected_body_reads_excluded": True,
            "rtm_generation_excluded": True,
            "drift_rejection_excluded": True,
            "coverage_truth_excluded": True,
            "reusable_blk_link_excluded": True,
            "signer_storage_ledger_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(REQUEST_PROOFS),
        "excluded_authorities": sorted(REQUEST_EXCLUDED),
    }
    for flag in REQUEST_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def valid_request_package():
    decision = valid_decision_package()
    return build_active_vault_hash_comparison_authority_request(decision, valid_request_context(decision))


def valid_approval_decision(request=None, **overrides):
    if request is None:
        request = valid_request_package()
    decision = {
        "approval_capture_package_id": APPROVAL_CAPTURE_PACKAGE_ID,
        "operator_identity": request["operator_identity"],
        "decision_scope": APPROVAL_SCOPE,
        "selected_frontier": APPROVAL_FRONTIER,
        "upstream_authority_request_package_id": request["authority_request_package_id"],
        "upstream_authority_request_package_hash": request["authority_request_package_hash"],
        "upstream_decision_package_id": request["upstream_decision_package_id"],
        "upstream_decision_package_hash": request["upstream_decision_package_hash"],
        "upstream_reconciliation_package_id": request["upstream_reconciliation_package_id"],
        "upstream_reconciliation_package_hash": request["upstream_reconciliation_package_hash"],
        "beo_id": request["beo_id"],
        "beb_id": request["beb_id"],
        "exact_trace_identities": list(request["exact_trace_identities"]),
        "approval_id": APPROVAL_ID,
        "future_run_id": FUTURE_RUN_ID,
        "decision_result": DECISION_RESULT,
        "decided_at": "2099-05-15T13:10:00+10:00",
        "expires_at": "2099-05-16T13:10:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_approval_text_raw": EXACT_OPERATOR_APPROVAL_TEXT,
        "operator_attestation": {
            "exact_blk138_request_reviewed": True,
            "approval_limited_to_one_future_metadata_hash_only_comparison": True,
            "future_run_id_reserved_not_consumed": True,
            "comparison_not_executed_by_this_decision": True,
            "protected_body_reads_excluded": True,
            "rtm_generation_excluded": True,
            "drift_rejection_excluded": True,
            "coverage_truth_excluded": True,
            "reusable_blk_link_excluded": True,
            "signer_storage_ledger_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(APPROVAL_PROOFS),
        "excluded_authorities": sorted(APPROVAL_EXCLUDED),
    }
    for flag in APPROVAL_FLAGS:
        decision[flag] = False
    decision.update(overrides)
    return decision


class ActiveVaultHashComparisonAuthorityLadderTest(unittest.TestCase):
    def test_137_decision_selects_metadata_hash_only_comparison_without_execution(self):
        reconciliation = valid_blk136_reconciliation_package()
        context = valid_decision_context(reconciliation)

        package = build_active_vault_hash_comparison_decision_package(reconciliation, context)

        self.assertEqual(package["decision_status"], DECISION_STATUS)
        self.assertEqual(package["decision_package_id"], DECISION_PACKAGE_ID)
        self.assertEqual(package["decision_scope"], DECISION_SCOPE)
        self.assertEqual(package["selected_frontier"], DECISION_FRONTIER)
        self.assertEqual(package["selected_capability"], "METADATA_HASH_ONLY_ACTIVE_VAULT_COMPARISON")
        self.assertEqual(package["next_required_authority"], DECISION_NEXT)
        self.assertEqual(package["decision_context_hash"], _canonical_hash(context))
        self.assertEqual(set(package["proof_obligations"]), DECISION_PROOFS)
        self.assertEqual(set(package["excluded_authorities"]), DECISION_EXCLUDED)
        for flag in DECISION_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertRegex(package["decision_package_hash"], r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(package["decision_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "decision_package_hash"}))

    def test_138_request_binds_exact_137_decision_without_approval_or_execution(self):
        decision = valid_decision_package()
        request = valid_request_context(decision)

        package = build_active_vault_hash_comparison_authority_request(decision, request)

        self.assertEqual(package["request_status"], REQUEST_STATUS)
        self.assertEqual(package["authority_request_package_id"], AUTHORITY_REQUEST_PACKAGE_ID)
        self.assertEqual(package["request_scope"], REQUEST_SCOPE)
        self.assertEqual(package["selected_frontier"], REQUEST_FRONTIER)
        self.assertTrue(package["request_future_exact_metadata_hash_only_active_vault_comparison_approval"])
        self.assertFalse(package["approval_capture_performed"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertEqual(package["next_required_authority"], REQUEST_NEXT)
        self.assertEqual(package["authority_request_hash"], _canonical_hash(request))
        self.assertEqual(set(package["proof_obligations"]), REQUEST_PROOFS)
        self.assertEqual(set(package["excluded_authorities"]), REQUEST_EXCLUDED)
        for flag in REQUEST_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["authority_request_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "authority_request_package_hash"}))

    def test_139_captures_exact_approval_and_reserves_future_run_without_consuming_it(self):
        request = valid_request_package()
        approval = valid_approval_decision(request)

        package = build_active_vault_hash_comparison_approval_capture(request, approval)

        self.assertEqual(package["approval_capture_status"], APPROVAL_STATUS)
        self.assertEqual(package["approval_capture_package_id"], APPROVAL_CAPTURE_PACKAGE_ID)
        self.assertEqual(package["approval_id"], APPROVAL_ID)
        self.assertEqual(package["future_run_id"], FUTURE_RUN_ID)
        self.assertEqual(package["decision_result"], DECISION_RESULT)
        self.assertEqual(package["next_required_authority"], APPROVAL_NEXT)
        self.assertTrue(package["future_metadata_hash_only_active_vault_comparison_approved"])
        self.assertFalse(package["future_run_id_consumed"])
        self.assertFalse(package["active_vault_hash_comparison_performed"])
        self.assertEqual(package["approval_decision_hash"], _canonical_hash(approval))
        self.assertEqual(set(package["proof_obligations"]), APPROVAL_PROOFS)
        self.assertEqual(set(package["excluded_authorities"]), APPROVAL_EXCLUDED)
        for flag in APPROVAL_FLAGS:
            self.assertIs(package[flag], False, flag)
        self.assertEqual(package["approval_capture_package_hash"], _canonical_hash({k: v for k, v in package.items() if k != "approval_capture_package_hash"}))

    def test_rejects_forged_upstream_hashes_ids_stale_replay_expiry_sets_and_side_effects(self):
        reconciliation = valid_blk136_reconciliation_package()
        decision_context = valid_decision_context(reconciliation)
        forged = copy.deepcopy(reconciliation)
        forged["reconciliation_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "reconciliation_package_hash does not match submitted BLK-136 package"):
            build_active_vault_hash_comparison_decision_package(forged, decision_context)

        for patch, message in [
            ({"decision_package_id": "ACTIVE-VAULT-HASH-COMPARISON-DECISION-１３７-００１"}, "decision_package_id must be"),
            ({"selected_frontier": "rtmGeneration"}, "selected_frontier must be|authority-laundering text"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(DECISION_PROOFS) + [sorted(DECISION_PROOFS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"stale": True}, "decision context must not be stale"),
            ({"replayed": True}, "decision context must not be replayed"),
        ]:
            context = copy.deepcopy(decision_context)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_decision_package(reconciliation, context)
        for flag in DECISION_FLAGS:
            context = copy.deepcopy(decision_context)
            context[flag] = True
            with self.assertRaisesRegex(ValueError, f"{flag} must remain false"):
                build_active_vault_hash_comparison_decision_package(reconciliation, context)

        decision = valid_decision_package()
        request = valid_request_context(decision)
        forged_decision = copy.deepcopy(decision)
        forged_decision["decision_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "decision_package_hash does not match submitted BLK-137 package"):
            build_active_vault_hash_comparison_authority_request(forged_decision, request)
        for patch, message in [
            ({"expires_at": "2099-05-15T13:05:00+10:00"}, "expires_at must be after requested_at"),
            ({"expired": True}, "authority request must not be expired"),
            ({"approval_capture_performed": True}, "approval_capture_performed must remain false"),
            ({"operator_attestation": request["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]:
            candidate = copy.deepcopy(request)
            candidate.update(patch)
            with self.subTest(request_patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_authority_request(decision, candidate)

        request_package = valid_request_package()
        approval = valid_approval_decision(request_package)
        for patch, message in [
            ({"operator_approval_text_raw": "looks approved"}, "operator approval text must match exact approval string"),
            ({"future_run_id": "RUN-BLK-SYSTEM-１４０-ACTIVE-VAULT-HASH-COMPARISON-001"}, "future_run_id must be"),
            ({"expired": True}, "approval decision must not be expired"),
            ({"replayed": True}, "approval decision must not be replayed"),
            ({"stale": True}, "approval decision must not be stale"),
            ({"future_run_id_consumed": True}, "future_run_id_consumed must remain false"),
        ]:
            candidate = copy.deepcopy(approval)
            candidate.update(patch)
            with self.subTest(approval_patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_approval_capture(request_package, candidate)

    def test_rejects_authority_laundering_protected_body_text_tooling_and_extra_fields(self):
        reconciliation = valid_blk136_reconciliation_package()
        base_context = valid_decision_context(reconciliation)
        cases = [
            ({"operator_identity": "discord:684235178083745819-RTMGenerated"}, "authority-laundering text"),
            ({"decision_package_id": "ACTIVE-VAULT-HASH-COMPARISON-DECISION-137-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"decision_package_id": "ACTIVE-VAULT-HASH-COMPARISON-DECISION-137-The%20system%20shall"}, "protected body text"),
            ({"sourceMutationAttempted": False}, "unexpected field"),
            ({"operator_attestation": base_context["operator_attestation"] | {"body_text": False}}, "unexpected field"),
        ]
        for patch, message in cases:
            context = copy.deepcopy(base_context)
            context.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_active_vault_hash_comparison_decision_package(reconciliation, context)

    def test_returned_packages_are_defensive_copies_and_hash_bound(self):
        decision = valid_decision_package()
        request = valid_request_context(decision)
        request_package = build_active_vault_hash_comparison_authority_request(decision, request)
        approval = valid_approval_decision(request_package)
        approval_package = build_active_vault_hash_comparison_approval_capture(request_package, approval)

        request["operator_attestation"]["coverage_truth_excluded"] = "mutated"
        decision["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        approval["operator_attestation"]["drift_rejection_excluded"] = "mutated"

        self.assertIsNot(request_package["operator_attestation"], request["operator_attestation"])
        self.assertIs(request_package["operator_attestation"]["coverage_truth_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, request_package["exact_trace_identities"])
        self.assertIsNot(approval_package["operator_attestation"], approval["operator_attestation"])
        self.assertIs(approval_package["operator_attestation"]["drift_rejection_excluded"], True)

    def test_modules_have_no_live_runtime_tooling_or_protected_body_file_access(self):
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib", "os"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request", "__import__"}
        for module in MODULES:
            tree = ast.parse(module.read_text())
            imported = set()
            calls = set()
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
            self.assertEqual(imported & forbidden_imports, set(), module)
            self.assertEqual(calls & forbidden_calls, set(), module)


if __name__ == "__main__":
    unittest.main()
