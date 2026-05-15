import ast
import copy
import unittest
from pathlib import Path

from authoritative_beo_publication_authority_request import _canonical_hash
from metadata_bound_rtm_trace_closure_approval_capture import build_metadata_bound_rtm_trace_closure_approval_capture
from test_metadata_bound_rtm_trace_closure_approval_capture import (
    valid_approval_decision,
    valid_blk130_request_package,
)

from metadata_bound_local_rtm_trace_closure_execution_record import (
    EXECUTION_PACKAGE_ID,
    EXECUTION_SCOPE,
    EXECUTION_STATUS,
    EXACT_EXCLUDED_AUTHORITIES,
    EXACT_PROOF_OBLIGATIONS,
    NEXT_REQUIRED_AUTHORITY,
    RUN_ID_CONSUMED,
    SELECTED_FRONTIER,
    SIDE_EFFECT_FLAGS,
    TRACE_CLOSURE_RECORD_ID,
    build_metadata_bound_local_rtm_trace_closure_execution_record,
)

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "python" / "metadata_bound_local_rtm_trace_closure_execution_record.py"


def valid_blk131_approval_package():
    request_package = valid_blk130_request_package()
    decision = valid_approval_decision(request_package)
    return build_metadata_bound_rtm_trace_closure_approval_capture(request_package, decision)


def valid_execution_request(approval_package=None, **overrides):
    if approval_package is None:
        approval_package = valid_blk131_approval_package()
    request = {
        "execution_package_id": EXECUTION_PACKAGE_ID,
        "operator_identity": approval_package["operator_identity"],
        "execution_scope": EXECUTION_SCOPE,
        "selected_frontier": SELECTED_FRONTIER,
        "approval_capture_package_id": approval_package["approval_capture_package_id"],
        "approval_capture_package_hash": approval_package["approval_capture_package_hash"],
        "approval_id": approval_package["approval_id"],
        "run_id_to_consume": RUN_ID_CONSUMED,
        "requested_at": "2099-05-15T12:05:00+10:00",
        "expires_at": "2099-05-15T12:09:00+10:00",
        "expired": False,
        "replayed": False,
        "stale": False,
        "operator_attestation": {
            "exact_blk131_approval_reviewed": True,
            "run_id_consumed_once_for_local_trace_closure_record": True,
            "local_trace_closure_record_only_not_production_blk_link": True,
            "rtm_generation_not_performed": True,
            "drift_rejection_excluded": True,
            "active_vault_hash_comparison_excluded": True,
            "coverage_truth_excluded": True,
            "protected_body_reads_excluded": True,
            "public_ledger_mutation_excluded": True,
            "signer_storage_ledger_rollback_side_effects_excluded": True,
            "target_source_git_mutation_excluded": True,
            "blk_pipe_blk_test_codex_tooling_excluded": True,
            "no_production_isolation_claim": True,
        },
        "proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS),
        "excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES),
    }
    for flag in SIDE_EFFECT_FLAGS:
        request[flag] = False
    request.update(overrides)
    return request


def rehash_approval_package(package):
    package["approval_capture_package_hash"] = _canonical_hash(
        {key: value for key, value in package.items() if key != "approval_capture_package_hash"}
    )
    return package


class MetadataBoundLocalRtmTraceClosureExecutionRecordTest(unittest.TestCase):
    def test_emits_local_non_authoritative_trace_closure_record_without_adjacent_authority(self):
        approval = valid_blk131_approval_package()
        request = valid_execution_request(approval)

        package = build_metadata_bound_local_rtm_trace_closure_execution_record(approval, request)

        self.assertEqual(package["execution_status"], EXECUTION_STATUS)
        self.assertEqual(package["execution_package_id"], EXECUTION_PACKAGE_ID)
        self.assertEqual(package["execution_scope"], EXECUTION_SCOPE)
        self.assertEqual(package["selected_frontier"], SELECTED_FRONTIER)
        self.assertEqual(package["approval_capture_package_id"], "RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-001")
        self.assertEqual(
            package["approval_capture_package_hash"],
            "sha256:c41c8bd4e7b5aba387a0db5b439d9bb664a1610f70eaff50488ed6cceabbbba0",
        )
        self.assertEqual(package["upstream_authority_request_package_id"], "RTM-TRACE-CLOSURE-AUTHORITY-REQUEST-130-001")
        self.assertEqual(package["upstream_execution_package_id"], "BEO-PUBLICATION-EXECUTION-129-001")
        self.assertEqual(package["run_id_consumed"], RUN_ID_CONSUMED)
        self.assertTrue(package["future_run_id_consumed"])
        self.assertTrue(package["local_rtm_trace_closure_record_emitted"])
        self.assertEqual(package["rtm_trace_closure_status"], "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_ONLY")
        self.assertEqual(package["trace_closure_record_id"], TRACE_CLOSURE_RECORD_ID)
        self.assertEqual(package["trace_closure_record"]["trace_closure_record_id"], TRACE_CLOSURE_RECORD_ID)
        self.assertEqual(package["trace_closure_record"]["trace_closure_status"], "LOCAL_NON_AUTHORITATIVE_RTM_TRACE_CLOSURE_RECORDED_ONLY")
        self.assertEqual(package["trace_closure_record"]["hash_binding_mode"], "METADATA_HASH_ONLY_NO_ACTIVE_VAULT_COMPARISON_NO_PROTECTED_BODY_READS")
        self.assertEqual(package["execution_request_hash"], _canonical_hash(request))
        self.assertEqual(package["requested_at"], request["requested_at"])
        self.assertEqual(package["expires_at"], request["expires_at"])
        self.assertEqual(set(package["proof_obligations"]), EXACT_PROOF_OBLIGATIONS)
        self.assertEqual(set(package["excluded_authorities"]), EXACT_EXCLUDED_AUTHORITIES)
        for flag in SIDE_EFFECT_FLAGS:
            self.assertIs(package[flag], False, flag)
        for flag in [
            "production_blk_link_authorized",
            "production_blk_link_executed",
            "rtm_generated",
            "rtm_drift_rejection_performed",
            "active_vault_hash_comparison_performed",
            "coverage_truth_established",
            "protected_body_reads",
            "public_ledger_mutation",
        ]:
            self.assertIs(package["trace_closure_record"][flag], False, flag)
        self.assertEqual(
            package["trace_closure_record_hash"],
            _canonical_hash({key: value for key, value in package["trace_closure_record"].items() if key != "trace_closure_record_hash"}),
        )
        self.assertEqual(
            package["execution_package_hash"],
            _canonical_hash({key: value for key, value in package.items() if key != "execution_package_hash"}),
        )
        self.assertRegex(package["execution_package_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_rejects_forged_rehashed_or_wrong_blk131_approval_package(self):
        approval = valid_blk131_approval_package()
        request = valid_execution_request(approval)

        forged = copy.deepcopy(approval)
        forged["approval_capture_package_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "approval_capture_package_hash does not match submitted BLK-131 package"):
            build_metadata_bound_local_rtm_trace_closure_execution_record(forged, request)

        forged = copy.deepcopy(approval)
        forged["future_run_id"] = "RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-999"
        rehash_approval_package(forged)
        forged_request = valid_execution_request(forged, run_id_to_consume=forged["future_run_id"])
        with self.assertRaisesRegex(ValueError, "canonical BLK-131 approval capture"):
            build_metadata_bound_local_rtm_trace_closure_execution_record(forged, forged_request)

        forged = copy.deepcopy(approval)
        forged["future_run_id_consumed"] = True
        rehash_approval_package(forged)
        with self.assertRaisesRegex(ValueError, "canonical BLK-131 approval capture"):
            build_metadata_bound_local_rtm_trace_closure_execution_record(forged, valid_execution_request(forged))

    def test_rejects_bad_scope_retargeting_replay_expiry_sets_unicode_ids_and_side_effects(self):
        approval = valid_blk131_approval_package()
        base_request = valid_execution_request(approval)
        cases = [
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-１３２-００１"}, "execution_package_id must be"),
            ({"selected_frontier": "production_blk_link_trace_closure"}, "selected_frontier must be"),
            ({"execution_scope": "PRODUCTION_RTM_TRACE_CLOSURE_EXECUTION"}, "execution_scope must be"),
            ({"approval_capture_package_id": "RTM-TRACE-CLOSURE-APPROVAL-CAPTURE-131-999"}, "approval_capture_package_id must match"),
            ({"approval_capture_package_hash": "sha256:" + "0" * 64}, "approval_capture_package_hash must match"),
            ({"approval_id": "APPROVAL-BLK-SYSTEM-132-OTHER"}, "approval_id must match"),
            ({"run_id_to_consume": "RUN-BLK-SYSTEM-１３２-RTM-TRACE-CLOSURE-001"}, "run_id_to_consume must match"),
            ({"run_id_to_consume": "RUN-BLK-SYSTEM-132-RTM-TRACE-CLOSURE-001-approved-for-production"}, "authority-laundering text"),
            ({"expired": True}, "execution request must not be expired"),
            ({"replayed": True}, "execution request must not be replayed"),
            ({"stale": True}, "execution request must not be stale"),
            ({"expires_at": base_request["requested_at"]}, "expires_at must be after requested_at"),
            ({"requested_at": "2000-01-01T00:00:00+10:00", "expires_at": "2000-01-01T01:00:00+10:00"}, "execution request must not predate approval decision"),
            ({"requested_at": "2099-05-15T12:11:00+10:00", "expires_at": "2099-05-15T12:12:00+10:00"}, "execution request window must end within BLK-131 approval expiry"),
            ({"proof_obligations": ["ok"]}, "proof_obligations must match exact set"),
            ({"proof_obligations": sorted(EXACT_PROOF_OBLIGATIONS) + [sorted(EXACT_PROOF_OBLIGATIONS)[0]]}, "proof_obligations must not contain duplicates"),
            ({"excluded_authorities": ["NOPE"]}, "excluded_authorities must match exact denied authority set"),
            ({"excluded_authorities": sorted(EXACT_EXCLUDED_AUTHORITIES) + [sorted(EXACT_EXCLUDED_AUTHORITIES)[0]]}, "excluded_authorities must not contain duplicates"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_local_rtm_trace_closure_execution_record(approval, request)

        for boolean_key in SIDE_EFFECT_FLAGS:
            request = copy.deepcopy(base_request)
            request[boolean_key] = True
            with self.subTest(boolean_key=boolean_key):
                with self.assertRaisesRegex(ValueError, f"{boolean_key} must remain false"):
                    build_metadata_bound_local_rtm_trace_closure_execution_record(approval, request)

    def test_rejects_nested_authority_laundering_protected_paths_body_text_tooling_and_extra_fields(self):
        approval = valid_blk131_approval_package()
        base_request = valid_execution_request(approval)
        cases = [
            ({"operator_identity": "discord:684235178083745819-productionBlkLinkExecuted"}, "authority-laundering text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-RTMGenerated"}, "authority-laundering text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-ActiveVaultHashComparison"}, "authority-laundering text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-docs%2525252Frequirements%2525252Factive"}, "authority-laundering text|protected body text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-The%20system%20shall"}, "protected body text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-coverageTruthEstablished"}, "authority-laundering text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-sourceMutationAuthorized"}, "authority-laundering text"),
            ({"execution_package_id": "RTM-TRACE-CLOSURE-EXECUTION-132-packageManagersAuthorized"}, "authority-laundering text"),
            ({"productionBlkLinkExecuted": False}, "unexpected field"),
            ({"operator_attestation": base_request["operator_attestation"] | {"RTMGenerated": True}}, "unexpected field"),
        ]
        for patch, message in cases:
            request = copy.deepcopy(base_request)
            request.update(patch)
            with self.subTest(patch=patch):
                with self.assertRaisesRegex(ValueError, message):
                    build_metadata_bound_local_rtm_trace_closure_execution_record(approval, request)

    def test_execution_window_is_hash_bound_and_returned_inputs_are_defensively_copied(self):
        approval = valid_blk131_approval_package()
        base_request = valid_execution_request(approval)
        alt_request = valid_execution_request(
            approval,
            requested_at="2099-05-15T12:06:00+10:00",
            expires_at="2099-05-15T12:09:30+10:00",
        )

        base_package = build_metadata_bound_local_rtm_trace_closure_execution_record(approval, base_request)
        alt_package = build_metadata_bound_local_rtm_trace_closure_execution_record(approval, alt_request)

        self.assertEqual(base_package["execution_request_hash"], _canonical_hash(base_request))
        self.assertEqual(alt_package["execution_request_hash"], _canonical_hash(alt_request))
        self.assertNotEqual(base_package["execution_request_hash"], alt_package["execution_request_hash"])
        self.assertNotEqual(base_package["execution_package_hash"], alt_package["execution_package_hash"])

        base_request["operator_attestation"]["protected_body_reads_excluded"] = "mutated"
        approval["exact_trace_identities"].append("REQ:REQ-999:sha256:" + "f" * 64)
        self.assertIsNot(base_package["operator_attestation"], base_request["operator_attestation"])
        self.assertIs(base_package["operator_attestation"]["protected_body_reads_excluded"], True)
        self.assertNotIn("REQ:REQ-999:sha256:" + "f" * 64, base_package["exact_trace_identities"])

    def test_module_has_no_live_runtime_tooling_or_protected_body_file_access(self):
        tree = ast.parse(MODULE.read_text())
        imported = set()
        calls = set()
        forbidden_imports = {"subprocess", "socket", "requests", "urllib3", "httpx", "shutil", "pathlib"}
        forbidden_calls = {"system", "popen", "Popen", "run", "call", "check_call", "check_output", "exec", "eval", "open", "read_text", "urlopen", "request"}
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
